#!/usr/bin/env python3
"""T13 (PurpleRiver Mini 640) mass -> AUW / endurance / payload-cap sensitivity.

Companion to analysis/t13_mass_cg.py (which covers CG shift). This one answers the
OTHER question raised by a vendor mass reply: if the thermal camera really weighs
X grams instead of the modelled 15 g, what happens to all-up mass, hover endurance,
payload-cap compliance, and hover throttle?

It reuses the LIVE model and the model's own physics (flight_time_model.evaluate),
so nothing is hard-coded: the airframe, battery, SBC and peripherals are the ones
the sweep already recommends (AF3a + recommended pack + SBC3), and only the
thermal camera mass is varied.

Usage:
    python3 analysis/t13_mass_endurance_sensitivity.py
    python3 analysis/t13_mass_endurance_sensitivity.py --masses 15,23.9,270
    python3 analysis/t13_mass_endurance_sensitivity.py --masses 270 --json

Exit code 0 always (reporting tool). Verdict text is printed per row.
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import flight_time_model as ftm  # noqa: E402

# Reference masses that matter for this task's history:
#   15.0  = current modelled value (bare module + 18 mm Ge lens estimate)
#   23.9  = worst-case bound already analysed 2026-10-24 (14.9 g module + 9 g lens)
#   270.0 = the vendor's 2026-10-20 reply ("Weight: 0.27kg")
DEFAULT_MASSES = [15.0, 23.9, 270.0]

R6_MIN = 30.0          # R6 minimum endurance floor [min]
R3_CAM_WT_G = 200.0    # R3_CAM_WT camera-subsystem mass cap [g]
TOL_THROTTLE = 0.60    # model's "flyable" hover-throttle ceiling


def build_baseline():
    """Load the live model and pick the RECOMMENDED baseline config's parts.

    Uses flight_time_model's own sweep + pick_baseline() so this tool can never
    drift from the published baseline (it honours the voltage/compatibility
    filters that a naive per-battery loop would skip).
    """
    p = ftm.PhysicsParams()
    airframes, components, batteries, gcs_base_cost, _gcs_parts, vrx_by_format = ftm.load_model()
    reps = {c: ftm.lightest(components[c]) for c in ("vtx", "fpv", "gps", "rx")}
    rep_pow = {c: ftm.representative_power(components[c]) for c in ("vtx", "fpv", "gps", "rx")}

    stats = {"voltage_pruned": 0, "video_pruned": 0}
    # Consume the sweep WITHOUT its file-writing side effects (write_csv() would
    # rewrite the tracked CSV); the ranking is identical to the publisher's.
    rows = list(ftm.iter_configs(airframes, components, batteries, p, stats,
                                 gcs_base_cost, vrx_by_format))
    rows.sort(key=lambda r: r["max_flight_time_hover_min"], reverse=True)
    baseline = ftm.pick_baseline(rows[:ftm.SYSML_TOP_N])
    if baseline is None:
        raise SystemExit("no baseline config produced by the sweep")

    af = next(a for a in airframes if a.ident == baseline["airframe_id"])
    bat = next(b for b in batteries if b.name == baseline["battery"])
    thermal = next(c for c in components["thermal"] if c.ident == baseline["thermal_id"])
    sbc = next(c for c in components["sbc"] if c.ident == baseline["sbc_id"])
    return dict(p=p, af=af, bat=bat, thermal=thermal, sbc=sbc, reps=reps,
                rep_pow=rep_pow, gcs_base_cost=gcs_base_cost,
                vrx_by_format=vrx_by_format, config_id=baseline["config_id"])


def evaluate_at_mass(ctx, mass_g: float) -> dict:
    thermal = dataclasses.replace(ctx["thermal"], mass_g=float(mass_g))
    return ftm.evaluate(ctx["af"], ctx["bat"], thermal, ctx["sbc"], None, None,
                        ctx["reps"], ctx["rep_pow"], ctx["p"], f"T13@{mass_g:g}g",
                        ctx["gcs_base_cost"], ctx["vrx_by_format"])


def verdict(mass_g: float, row: dict, base_row: dict) -> str:
    flags = []
    if mass_g > R3_CAM_WT_G:
        flags.append(f"FAILS R3_CAM_WT ({R3_CAM_WT_G:.0f} g cap)")
    if not row["meets_r6_30min"]:
        flags.append("FAILS R6 (30 min)")
    if not row["payload_weight_ok"]:
        flags.append("OVER airframe payload cap")
    if not row["flyable"]:
        flags.append(f"hover throttle >{TOL_THROTTLE:.0%}")
    if not flags:
        d = row["max_flight_time_hover_min"] - base_row["max_flight_time_hover_min"]
        flags.append(f"ACCEPTABLE (hover {d:+.1f} min vs 15 g baseline)")
    return "; ".join(flags)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--masses", default=",".join(f"{m:g}" for m in DEFAULT_MASSES),
                    help="comma-separated thermal masses in grams")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    masses = [float(x) for x in args.masses.split(",") if x.strip()]
    ctx = build_baseline()
    base_row = evaluate_at_mass(ctx, ctx["thermal"].mass_g)

    rows = []
    for m in masses:
        r = evaluate_at_mass(ctx, m)
        rows.append({
            "thermal_mass_g": m,
            "delta_g": round(m - ctx["thermal"].mass_g, 1),
            "all_up_mass_g": r["all_up_mass_g"],
            "delta_auw_g": round(r["all_up_mass_g"] - base_row["all_up_mass_g"], 1),
            "hover_power_w": r["hover_power_w"],
            "hover_endurance_min": r["max_flight_time_hover_min"],
            "delta_endurance_min": round(r["max_flight_time_hover_min"]
                                         - base_row["max_flight_time_hover_min"], 2),
            "hover_throttle_pct": r["hover_throttle_pct"],
            "payload_weight_g": r["payload_weight_g"],
            "payload_capacity_g": r["payload_capacity_g"],
            "meets_r6_30min": r["meets_r6_30min"],
            "meets_r3_cam_wt": m <= R3_CAM_WT_G,
            "verdict": verdict(m, r, base_row),
        })

    if args.json:
        print(json.dumps({"context": {
            "airframe": f"{ctx['af'].ident} {ctx['af'].name}",
            "battery": ctx["bat"].name,
            "sbc": ctx["sbc"].ident,
            "modelled_thermal_mass_g": ctx["thermal"].mass_g,
            "baseline_auv_g": base_row["all_up_mass_g"],
            "baseline_hover_min": base_row["max_flight_time_hover_min"],
        }, "rows": rows}, indent=2))
        return

    print(f"Context: {ctx['af'].ident} {ctx['af'].name} + {ctx['bat'].name} + {ctx['sbc'].ident}")
    print(f"Baseline config {ctx['config_id']} (flight_time_model pick_baseline)")
    print(f"Modelled T13 mass: {ctx['thermal'].mass_g:g} g | "
          f"baseline AUW {base_row['all_up_mass_g']:.0f} g | "
          f"hover {base_row['max_flight_time_hover_min']:.1f} min | "
          f"payload cap {base_row['payload_capacity_g']} g")
    print()
    hdr = (f"{'T13 mass':>9} {'Δmass':>7} {'AUW':>7} {'ΔAUW':>7} "
           f"{'hover W':>8} {'hover min':>10} {'Δmin':>7} {'thr%':>6}  verdict")
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        print(f"{r['thermal_mass_g']:9.1f} {r['delta_g']:+7.1f} {r['all_up_mass_g']:7.0f} "
              f"{r['delta_auw_g']:+7.0f} {r['hover_power_w']:8.1f} {r['hover_endurance_min']:10.1f} "
              f"{r['delta_endurance_min']:+7.2f} {r['hover_throttle_pct']:6.1f}  {r['verdict']}")
    print()
    worst = max(rows, key=lambda r: r["thermal_mass_g"])
    if worst["thermal_mass_g"] > R3_CAM_WT_G:
        print(f"NOTE: {worst['thermal_mass_g']:g} g exceeds the R3_CAM_WT {R3_CAM_WT_G:.0f} g "
              "camera-subsystem cap — that is a REQUIREMENT breach, not just a model tweak.")
        print("      Confirm the vendor number refers to the bare core + lens before editing the model.")


if __name__ == "__main__":
    main()
