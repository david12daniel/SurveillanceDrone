#!/usr/bin/env python3
"""t13_mass_cg.py — CG-impact calculator for the T13 nose payload (task 2.1 / MC #39).

When the vendor (justin.lu@purpleriver.cn) replies with the exact assembled mass of
the PurpleRiver Mini 640 + 18 mm Ge lens, this tool makes applying it mechanical:

    1. Reads the CURRENT T13.mass straight from candidates.sysml (live parse via the
       same loader flight_time_model.py uses — can never read a stale model).
    2. Computes the CG shift of swapping the current estimate for the vendor's number:
            ΔCG = Δmass × nose_arm / AUW
       over the established nose-arm range (150–250 mm forward of aircraft CG) and
       both the modeled reference AUW (1743.0 g, config C000009 AF3a+BAT10+SBC3+T13)
       and the conservative ~1.9 kg figure used in the research notes.
    3. Rates the delta against the quad's CG tolerance class (±10–20 mm for a
       405 mm-wheelbase quad; the tool assumes the conservative ±10 mm end).
    4. Prints a paste-ready candidates.sysml edit (mass line + comment) so the model
       update is a 60-second copy-paste, comment included.

Anchor (must hold): Δ6 g (21→15 g change of 2026-08-20) over 150–250 mm arm at
~1.9 kg AUW ≈ 0.5–0.8 mm — reproduces research-findings-oct-2026.md exactly.

Usage:
    python3 analysis/t13_mass_cg.py                     # current state + sensitivity sweep
    python3 analysis/t13_mass_cg.py --new-mass-g 18.5   # vendor number -> verdict + edit
    python3 analysis/t13_mass_cg.py --new 18.5 --auw-g 1743 --arm 150 250 --tol-mm 10
    python3 analysis/t13_mass_cg.py --self-test         # assert the documented anchor

Exit code 0 always (informational); --self-test exits 1 if an anchor check fails.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CANDIDATES_SYSML = ROOT / "candidates.sysml"

# ---------------------------------------------------------------------------
# Live model read — reuse flight_time_model.py's own loaders so this tool always
# sees exactly the mass the sweep sees (sysmlv2mde live parse, export fallback).
# ---------------------------------------------------------------------------
sys.path.insert(0, str(HERE))
try:
    from flight_time_model import load_candidates_export, part_blocks_from_export
except Exception as exc:  # pragma: no cover - import failure should be loud
    sys.stderr.write(f"t13_mass_cg.py: cannot import flight_time_model: {exc}\n")
    sys.stderr.write("Place this script in analysis/ next to flight_time_model.py.\n")
    raise SystemExit(2)


def current_t13_mass_g() -> float:
    """Live T13.mass from candidates.sysml (falls back to the committed export)."""
    doc, src_label = load_candidates_export()
    for part in part_blocks_from_export(doc):
        if part["ident"] == "T13":
            m = part["attrs"].get("mass")
            if m is None:
                raise SystemExit(f"T13 part found but has no mass attr ({src_label})")
            # attrs values come back as number | string | raw; be lenient
            return float(str(m).replace("[g]", "").replace("g", "").strip())
    raise SystemExit(f"T13 part not found in candidates.sysml ({src_label})")


# ---------------------------------------------------------------------------
# CG math
# ---------------------------------------------------------------------------
def cg_shift_mm(delta_mass_g: float, arm_mm: float, auw_g: float) -> float:
    """CG shift [mm] from a nose-payload mass change: Δm×arm/AUW."""
    return delta_mass_g * arm_mm / auw_g


def nose_moment_mm(delta_mass_g: float, arm_mm: float, auw_g: float) -> float:
    """Nose payload's own additive CG contribution: m×arm/AUW (task 2.11 input)."""
    return delta_mass_g * arm_mm / auw_g  # same formula, different semantic — kept separate


def render_verdict(max_shift_mm: float, tol_mm: float) -> str:
    if max_shift_mm < 1.0:
        return ("NEGLIGIBLE — sub-millimetre; no model regeneration warranted, "
                "comment update only (matches the established 08-20/10-14 verdicts).")
    if max_shift_mm < tol_mm:
        return (f"ACCEPTABLE — within the ±{tol_mm:g} mm class tolerance but above 1 mm; "
                f"flag for the as-built CG re-check (task 2.11 / #49) at build time.")
    return (f"SIGNIFICANT — exceeds the ±{tol_mm:g} mm tolerance class; do NOT apply "
            f"without a full mass/CG re-check (task 2.11).")


# ---------------------------------------------------------------------------
# Paste-ready candidates.sysml edit
# ---------------------------------------------------------------------------
def sysml_edit_block(new_mass_g: float, now_iso: str) -> str:
    return (
        "--- paste-ready candidates.sysml edit (T13 part, ~line 1145) ------------------\n"
        f'   :>> mass = {new_mass_g:.1f} [g];             // VENDOR-CONFIRMED {now_iso}: exact assembled\n'
        f"                                    // mass (module + 18 mm Ge lens) per justin.lu@purpleriver.cn.\n"
        f"                                    // Replaces the 12–17 g estimate (midpoint 15.0 g,\n"
        f"                                    // set 2026-08-20). CG delta vs estimate: see\n"
        f"                                    // analysis/t13_mass_cg.py run on {now_iso}.\n"
        "-----------------------------------------------------------------------------------"
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--new-mass-g", "--new", type=float, default=None,
                    help="Vendor-confirmed assembled mass [g]; omit for current-state report")
    ap.add_argument("--auw-g", type=float, default=1743.0,
                    help="All-up mass [g] (default 1743.0 = modeled AF3a+BAT10+SBC3+T13, C000009)")
    ap.add_argument("--arm", nargs=2, type=float, default=(150.0, 250.0),
                    help="Nose moment-arm range [mm] forward of CG (default 150 250)")
    ap.add_argument("--tol-mm", type=float, default=10.0,
                    help="CG tolerance class, conservative end [mm] (default 10)")
    ap.add_argument("--self-test", action="store_true",
                    help="Assert the documented anchor (Δ6 g ≈ 0.5–0.8 mm) and exit")
    args = ap.parse_args()

    if args.self_test:
        lo = cg_shift_mm(6.0, 150.0, 1900.0)
        hi = cg_shift_mm(6.0, 250.0, 1900.0)
        ok = 0.40 <= lo <= 0.60 and 0.70 <= hi <= 0.90
        print(f"self-test: Δ6 g @150 mm/1900 g = {lo:.2f} mm (expect ~0.47)")
        print(f"self-test: Δ6 g @250 mm/1900 g = {hi:.2f} mm (expect ~0.79)")
        print(f"self-test: documented anchor 0.5–0.8 mm -> {'PASS' if ok else 'FAIL'}")
        return 0 if ok else 1

    current = current_t13_mass_g()
    arm_lo, arm_hi = min(args.arm), max(args.arm)
    arm_mid = (arm_lo + arm_hi) / 2.0
    tol = args.tol_mm

    print("T13 (PurpleRiver Mini 640) nose-payload CG impact")
    print(f"  current candidates.sysml mass : {current:.1f} g")

    if args.new_mass_g is None:
        # Sensitivity sweep across the whole plausible range (10–25 g), incl. the
        # 12–17 g estimate band and the <20 g spec ceiling.
        print("  (no --new-mass-g given -> sensitivity sweep vs all plausible masses)\n")
        print(f"  AUW {args.auw_g:.0f} g | arm {arm_lo:.0f}–{arm_hi:.0f} mm | tol ±{tol:g} mm")
        print(f"  {'new mass':>9} {'Δmass':>7} {'ΔCG min':>8} {'ΔCG max':>8}  verdict")
        for m in (10.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 22.0, 25.0):
            dm = m - current
            lo = cg_shift_mm(dm, arm_lo, args.auw_g)
            hi = cg_shift_mm(dm, arm_hi, args.auw_g)
            print(f"  {m:8.1f}g {dm:+6.1f}g {lo:7.2f}mm {hi:7.2f}mm  "
                  f"{render_verdict(max(abs(lo), abs(hi)), tol)}")
        print("\n  Note: even the <20 g spec ceiling moves CG <1 mm at these arms — "
              "the 15.0 g estimate is not build-sensitive.")
        return 0

    new = args.new_mass_g
    dm = new - current
    lo = cg_shift_mm(dm, arm_lo, args.auw_g)
    mid = cg_shift_mm(dm, arm_mid, args.auw_g)
    hi = cg_shift_mm(dm, arm_hi, args.auw_g)
    maxabs = max(abs(lo), abs(hi))

    print(f"  vendor number (--new-mass-g) : {new:.1f} g   (Δ {dm:+.1f} g vs model)")
    print(f"  AUW {args.auw_g:.0f} g | arm {arm_lo:.0f}–{arm_hi:.0f} mm (mid {arm_mid:.0f}) | "
          f"tol ±{tol:g} mm")
    print(f"  ΔCG: {lo:+.2f} mm (arm {arm_lo:.0f}) / {mid:+.2f} mm (arm {arm_mid:.0f}) / "
          f"{hi:+.2f} mm (arm {arm_hi:.0f})")
    print(f"  VERDICT: {render_verdict(maxabs, tol)}")
    print(f"  conservative AUW ({args.auw_g * 1.09:.0f} g ≈1.9 kg): "
          f"ΔCG {cg_shift_mm(dm, arm_lo, args.auw_g * 1.09):+.2f}.."
          f"{cg_shift_mm(dm, arm_hi, args.auw_g * 1.09):+.2f} mm")
    print()
    print(sysml_edit_block(new, "2026-10-20"))

    # T13's own contribution to the as-built CG (the term task 2.11 sums over all parts).
    print()
    print("  Task 2.11 input — T13's own additive CG contribution (m×arm/AUW):")
    print(f"    {new:.1f} g × {arm_lo:.0f}–{arm_hi:.0f} mm / {args.auw_g:.0f} g = "
          f"{nose_moment_mm(new, arm_lo, args.auw_g):.2f}–{nose_moment_mm(new, arm_hi, args.auw_g):.2f} mm "
          "forward of aircraft CG")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())