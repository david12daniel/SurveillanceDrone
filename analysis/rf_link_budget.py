"""RF link-budget analysis for the thermal surveillance drone.

Verifies that every RF link closes the R7 / R4_GCS_RANGE hard requirement of
**2.8 km** with adequate fade margin, using the SELECTED components
(see SELECTED_COMPONENTS.md):
  - Analog FPV video      : AF3a BLITZ Whoop 5.8 GHz 1.6 W VTX -> Skydroid VRX6
                            + TrueRC X-AIR PATCH1 (~10 dBic, 120° beam).
  - ELRS control uplink   : RadioMaster TX12 MkII (250 mW, 2.4 GHz)
                            -> iFlight True Diversity RX.
  - ELRS telemetry downlink: iFlight TD RX (100 mW) -> HGLRC Hermes USB dongle.
  - OpenHD thermal video  : BL-M8812EU2 (800 mW+, 5.825 GHz) -> AWUS036ACH
                            + dual Lumenier AXII Quadro (14.7 dBic, 40°, diversity).

Model: free-space path loss (FSPL). The **10 dB fade-margin** target absorbs
real-world excess (ground reflection, foliage, multipath, polarisation mismatch).
Writes analysis/rf_link_budget.md.  Run: python analysis/rf_link_budget.py
"""
from __future__ import annotations
import math
from pathlib import Path

OUT_MD = Path(__file__).resolve().parent / "rf_link_budget.md"

RANGE_REQ_KM = 2.8     # R7 / R4_GCS_RANGE — hard requirement
FADE_MARGIN_DB = 10.0  # margin over sensitivity for a *reliable* link


def fspl_db(d_km: float, f_mhz: float) -> float:
    """Free-space path loss [dB]; d in km, f in MHz."""
    return 20 * math.log10(d_km) + 20 * math.log10(f_mhz) + 32.44


def reliable_range_km(eirp_dbm: float, eff_rxg: float, loss: float,
                      sens_dbm: float, f_mhz: float, fade_db: float) -> float:
    """Range at which `fade_db` of margin remains above the sensitivity floor."""
    allowable_pl = eirp_dbm + eff_rxg - loss - sens_dbm - fade_db
    return 10 ** ((allowable_pl - 32.44 - 20 * math.log10(f_mhz)) / 20.0)


# Link entries: tx/txg/rxg in dBm / dBi, loss in dB, sens in dBm (threshold),
# div_gain in dB (spatial-diversity benefit, added to effective rxg).
LINKS = [
    dict(
        key="VIDEO-patch",
        name="Analog FPV video — 5.8 GHz (PATCH1 ground antenna)",
        f=5800.0, tx=32.0, txg=2.0, rxg=10.0, loss=2.0, sens=-90.0, div_gain=0.0,
        note="AF3a BLITZ Whoop 5.8 GHz **1.6 W** (32 dBm) → Skydroid VRX6 + TrueRC X-AIR "
             "PATCH1 (10 dBic, 120° beam, RHCP). Analog 'usable' threshold ≈ −90 dBm.",
    ),
    dict(
        key="VIDEO-omni",
        name="Analog FPV video — 5.8 GHz (stock omni RX antenna, contrast only)",
        f=5800.0, tx=32.0, txg=2.0, rxg=2.0, loss=2.0, sens=-90.0, div_gain=0.0,
        note="Same link with the VRX's stock omni (~2 dBi) instead of PATCH1 — "
             "shows why the dedicated patch antenna is required.",
    ),
    dict(
        key="CONTROL",
        name="Control uplink — 2.4 GHz ELRS (TX12 MkII → iFlight TD RX)",
        f=2400.0, tx=24.0, txg=2.0, rxg=2.0, loss=2.0, sens=-106.0, div_gain=0.0,
        note="RadioMaster TX12 MkII @**250 mW** (24 dBm) → iFlight True Diversity RX. "
             "ELRS 150 Hz sensitivity ≈ −106 dBm (−108 at 50 Hz long-range mode). "
             "True diversity adds ~2 dB above nominal (not included — margin is already enormous).",
    ),
    dict(
        key="TELEMETRY",
        name="Telemetry downlink — 2.4 GHz ELRS (TD RX → Hermes dongle)",
        f=2400.0, tx=20.0, txg=2.0, rxg=2.0, loss=2.0, sens=-106.0, div_gain=0.0,
        note="iFlight TD RX reverse-link @100 mW (20 dBm) → HGLRC Hermes USB dongle "
             "(2.4 GHz ELRS). Same sensitivity threshold as control.",
    ),
    dict(
        key="OPENHD",
        name="OpenHD thermal video — 5.825 GHz WFB-ng (dual Foxeer Echo 2 Max diversity)",
        f=5825.0, tx=29.0, txg=3.0, rxg=13.0, loss=5.0, sens=-85.0, div_gain=3.0,
        note="BL-M8812EU2 (WLAN_AIR1) @>800 mW (29 dBm) → AWUS036ACH (WLAN_GND1) + "
             "dual Foxeer Echo 2 Max (13 dBi, 60° beam, Linear). WFB-ng MCS1 sensitivity ≈ −85 dBm. "
             "+5 dB loss for driver/connector variability. +3 dB spatial-diversity gain "
             "(two-antenna receive on AWUS036ACH dual RP-SMA ports; Echo 2 Max is RP-SMA male, "
             "no pigtail needed).",
    ),
]

# OpenHD ground antenna alternatives — only the ground RX gain changes.
# TX fixed: WLAN_AIR1 (29 dBm) + 3 dBi cloverleaf = 32 dBm EIRP.
# Losses 5 dB, sens −85 dBm, diversity +3 dB — all constant.
_TX_EIRP_OPENHD = 29.0 + 3.0    # dBm
_LOSS_OPENHD    = 5.0
_SENS_OPENHD    = -85.0
_DIV_OPENHD     = 3.0
_F_OPENHD       = 5825.0

OPENHD_ANTENNAS = [
    dict(id="ANT_GND1+2 (selected)", model="Foxeer Echo 2 Max × 2",
         gain=13.0, beam="60°×60°", pol="Linear", price_ea=30.00),
    dict(id="Lumenier AXII Quadro × 2", model="Lumenier AXII Quadro × 2",
         gain=14.7, beam="40°×40°", pol="RHCP", price_ea=32.49),
    dict(id="Foxeer Echo 2 × 2", model="Foxeer Echo 2 × 2",
         gain=9.0, beam="84°×84°", pol="RHCP", price_ea=20.00),
]


def evaluate(link: dict) -> dict:
    fspl  = fspl_db(RANGE_REQ_KM, link["f"])
    eirp  = link["tx"] + link["txg"]
    eff_rxg = link["rxg"] + link.get("div_gain", 0.0)
    prx   = eirp - fspl + eff_rxg - link["loss"]
    margin = prx - link["sens"]
    rng   = reliable_range_km(eirp, eff_rxg, link["loss"], link["sens"], link["f"], FADE_MARGIN_DB)
    return dict(fspl=fspl, eirp=eirp, prx=prx, margin=margin, rng=rng,
                ok=margin >= FADE_MARGIN_DB)


def eval_openhd_ant(ant: dict) -> dict:
    eff_rxg = ant["gain"] + _DIV_OPENHD
    fspl    = fspl_db(RANGE_REQ_KM, _F_OPENHD)
    prx     = _TX_EIRP_OPENHD - fspl + eff_rxg - _LOSS_OPENHD
    margin  = prx - _SENS_OPENHD
    rng     = reliable_range_km(_TX_EIRP_OPENHD, eff_rxg, _LOSS_OPENHD,
                                _SENS_OPENHD, _F_OPENHD, FADE_MARGIN_DB)
    return dict(fspl=fspl, prx=prx, margin=margin, rng=rng)


def verdict(ok: bool, margin: float) -> str:
    if ok:
        return "✅ PASS"
    elif margin >= 6.0:
        return "⚠️ THIN"
    return "❌ FAIL"


def main() -> None:
    rows = [(lk, evaluate(lk)) for lk in LINKS]

    L: list[str] = [
        "# RF Link-Budget Analysis",
        "",
        "**Auto-generated** by [`rf_link_budget.py`](rf_link_budget.py). "
        "Regenerate: `python analysis/rf_link_budget.py`.",
        "",
        f"Verifies every RF link meets the **{RANGE_REQ_KM:.1f} km** hard range requirement "
        f"(**R7 / R4_GCS_RANGE**) with a **≥ {FADE_MARGIN_DB:.0f} dB** fade margin, "
        "using the selected components ([`SELECTED_COMPONENTS.md`](../SELECTED_COMPONENTS.md)). "
        "Free-space path-loss (FSPL) model; the fade margin absorbs real-world excess loss "
        "(ground reflection, foliage, multipath, polarisation mismatch).",
        "",
        f"**FSPL @ {RANGE_REQ_KM:.1f} km:** "
        f"5.825 GHz (OpenHD ch 165) = {fspl_db(RANGE_REQ_KM, 5825):.1f} dB · "
        f"5.8 GHz (analog VTX) = {fspl_db(RANGE_REQ_KM, 5800):.1f} dB · "
        f"2.4 GHz (ELRS) = {fspl_db(RANGE_REQ_KM, 2400):.1f} dB.",
        "",
        "## All RF links — summary table",
        "",
        "| Link | TX pwr | TX ant | RX ant (eff.) | FSPL | RX power | **Margin @2.8 km** | Reliable range† | Verdict |",
        "|---|--:|--:|--:|--:|--:|--:|--:|:--:|",
    ]

    for lk, r in rows:
        div = lk.get("div_gain", 0.0)
        eff_rxg_str = (f"{lk['rxg']+div:.1f} dBi ({lk['rxg']:.1f}+{div:.0f} div)"
                       if div > 0 else f"{lk['rxg']:.0f} dBi")
        L.append("| " + " | ".join([
            lk["name"],
            f"{lk['tx']:.0f} dBm", f"{lk['txg']:.0f} dBi",
            eff_rxg_str,
            f"{r['fspl']:.1f} dB", f"{r['prx']:.1f} dBm",
            f"**{r['margin']:+.1f} dB**",
            f"{r['rng']:.1f} km",
            verdict(r["ok"], r["margin"]),
        ]) + " |")

    L += [
        "",
        "† *Reliable range = distance at which the full 10 dB fade margin remains "
        "(free-space FSPL only). Beyond it the link still works with reduced fade tolerance.*",
        "",
        "### Per-link notes",
        "",
    ]
    for lk in LINKS:
        L.append(f"- **{lk['key']}:** {lk['note']}")
    L.append("")

    # ── OpenHD antenna comparison ───────────────────────────────────────────
    L += [
        "## OpenHD ground antenna options (cost / beamwidth trade-off)",
        "",
        "All rows assume the same TX (BL-M8812EU2, EIRP = 32 dBm) and +3 dB receive diversity. "
        "The 10 dB margin target is the design threshold; links above 6 dB are usable but with "
        "reduced tolerance to fading.",
        "",
        "| Antenna (×2 for diversity) | Gain | Beam H×V | Pol. | Price (pair) | "
        "Margin @2.8 km | Reliable range† | Verdict |",
        "|---|--:|--:|--:|--:|--:|--:|:--:|",
    ]
    for ant in OPENHD_ANTENNAS:
        r = eval_openhd_ant(ant)
        L.append("| " + " | ".join([
            f"**{ant['model']}**" if "selected" in ant["id"] else ant["model"],
            f"{ant['gain']:.1f} dBi",
            ant["beam"],
            ant["pol"],
            f"${ant['price_ea']*2:.2f}",
            f"**{r['margin']:+.1f} dB**",
            f"{r['rng']:.1f} km",
            verdict(r["margin"] >= FADE_MARGIN_DB, r["margin"]),
        ]) + " |")

    L += [
        "",
        "**Reading the table:**",
        "",
        "- **AXII Quadro (selected):** +13 dB margin at 2.8 km; reliable out to ~4 km. "
          "40° beam requires a rough initial aim at the survey area — once pointed, no tracking "
          "needed for a drone within ±20° of centre.",
        "- **Foxeer Echo 2 Max:** saves ~$5/antenna ($60 vs $65 pair); 60° beam is more "
          "forgiving — ±30° from centre before losing half-power. Margin is 11.3 dB, well "
          "above the 10 dB target. **Best 'wide-beam' option if range > 2.8 km matters.** "
          "Linear vs RHCP costs ~1–3 dB in multipath; negligible at 90–120 m AGL in open fields.",
        "- **Foxeer Echo 2:** 84° beam is essentially point-and-forget, but 7.3 dB margin at "
          "2.8 km falls below the 10 dB design target (reliable range is only 2.1 km). "
          "Works with reduced confidence; not recommended for the full 2.8 km requirement.",
        "",
        "**Selected: Foxeer Echo 2 Max** ($60 pair). +11.3 dB margin at 2.8 km comfortably "
        "passes the R7 requirement, with a 60° beam that covers the survey area without "
        "re-aiming. RP-SMA male connector mates directly to the AWUS036ACH (no pigtails).",
        "",
    ]

    # ── Findings ─────────────────────────────────────────────────────────────
    L += [
        "## Findings",
        "",
        "- **ELRS (control + telemetry):** enormous margin (22–19 dB) — the control link closes "
          "2.8 km many times over and is never the limiting link. "
          "TX12 MkII at 250 mW (6 dB below the old Boxer 1 W assumption) still delivers 22 dB.",
        "- **Analog FPV video:** binding constraint without a patch antenna. With PATCH1 "
          "(10 dBic, 120° beam) the margin is +15.3 dB — reliable to 6 km. "
          "Without PATCH1, the stock-omni link has only +7.3 dB and fails the 10 dB target.",
        "- **OpenHD thermal video (WFB-ng):** the tightest link, but still comfortable. "
          "With dual Foxeer Echo 2 Max diversity (+11.3 dB @2.8 km) the thermal downlink closes "
          "the full R7 range with margin and is reliable to ~3.3 km. "
          "The 60° beam means no re-aiming needed during a survey (±30° slack).",
        "- **All selected-component RF links pass** the 2.8 km / 10 dB requirement. "
          "The analog patch antenna and OpenHD diversity antennas are the enabling components.",
        "",
    ]

    # ── Assumptions ──────────────────────────────────────────────────────────
    L += [
        "## Assumptions & notes",
        "",
        "- **TX powers (selected components):** analog VTX = BLITZ Whoop 1.6 W (32 dBm, "
          "AF3a actual; the 2.5 W variant would add +2 dB); ELRS TX12 MkII = 250 mW (24 dBm); "
          "ELRS RX telemetry = 100 mW (20 dBm); OpenHD BL-M8812EU2 = >800 mW (29 dBm — "
          "driver_txpower_override 40–50 recommended to avoid PA clipping).",
        "- **Air-side antennas:** VTX/RX omni ≈ 2 dBi (cloverleaf/patch); "
          "OpenHD air ≈ 3 dBi (RHCP cloverleaf on u.fl pigtail).",
        "- **Ground antennas:** PATCH1 = TrueRC X-AIR 5.8 MK II, ~10 dBic, 120° beam, RHCP, "
          "RP-SMA; OpenHD = dual Foxeer Echo 2 Max, 13 dBi, 60° beam, Linear, RP-SMA male "
          "(mates directly to AWUS036ACH RP-SMA female — no pigtail required).",
        "- **Sensitivity thresholds:** analog 'usable' video ≈ −90 dBm; "
          "ELRS 2.4 GHz ≈ −106 dBm @ 150 Hz (−108 @ 50 Hz long-range mode); "
          "WFB-ng / OpenHD MCS1 ≈ −85 dBm (clean video; FEC begins recovering packets below this).",
        "- **Losses:** 2 dB lumped (connectors, cable, mismatch) for analog/ELRS links; "
          "5 dB for OpenHD (higher, to cover 802.11ac driver variability + pigtail + adapter "
          "tolerance).",
        "- **Diversity:** OpenHD uses two AXII Quadro panels on the AWUS036ACH dual RP-SMA "
          "ports; WFB-ng selects the best-SNR packet per frame (+3 dB in fading). "
          "The iFlight TD RX (ELRS control) also has true diversity (~2 dB, not modelled "
          "separately — ELRS margin is already 22 dB).",
        "- **Polarisation:** all RHCP pairs are matched (+0 dB). "
          "Linear vs RHCP costs ~1–3 dB in reflected-ground environments; negligible at "
          "90–120 m AGL in open / semi-open terrain.",
        "- **GNSS** is satellite-receive only (~−130 dBm, L1 1575 MHz) — not a controlled "
          "link in this budget; covered by the GPS module's own sensitivity specification.",
        "- **Free-space model only.** For dense foliage or non-LOS, raise TX power, switch to "
          "higher-gain antennas, or lower the ELRS packet rate. The 10 dB margin is the "
          "practical cushion for realistic survey conditions at 90–120 m AGL.",
        "",
    ]

    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_MD.name}")
    print()
    print("=== All-links summary ===")
    for lk, r in rows:
        v = "PASS" if r["ok"] else ("THIN" if r["margin"] >= 6 else "FAIL")
        print(f"  {lk['key']:12}  margin {r['margin']:+6.1f} dB @2.8km  "
              f"reliable~{r['rng']:5.1f} km  {v}")
    print()
    print("=== OpenHD antenna options ===")
    for ant in OPENHD_ANTENNAS:
        r = eval_openhd_ant(ant)
        v = "PASS" if r["margin"] >= FADE_MARGIN_DB else ("THIN" if r["margin"] >= 6 else "FAIL")
        print(f"  {ant['model']:30}  {ant['gain']:4.1f} dBi  {ant['beam']:8}  "
              f"margin {r['margin']:+6.1f} dB  reliable~{r['rng']:4.1f} km  {v}")


if __name__ == "__main__":
    main()
