#!/usr/bin/env python3
"""
thermal_camera_analysis.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Purpose:
  Validate that the thermal camera subsystem requirements (R3_CAM_RES,
  R3_CAM_FOV, R3_CAM_NETD) are sufficient to support the mission-level
  requirements (R3, R3.1, R3.2) for detecting and classifying deer, turkey,
  other animals, and humans at 90–120 m AGL with a 5 °C minimum temperature
  differential.

  UPDATED 2026-08-12: pixels-on-target now account for the as-built 45°
  down-look mount (candidates.sysml T13.mountTilt_deg), not nadir. A tilted,
  non-gimbaled camera views an on-axis target at slant range alt/cos(tilt),
  which stretches the ground footprint of each pixel by 1/cos(tilt)
  cross-range and 1/cos(tilt)^2 along-range (x1.414 / x2.000 at 45°) — see
  analysis/thermal_detection_offnadir_analysis.md §2 and model.sysml's
  OffNadirGsd calc, which this mirrors. The along-range axis binds, so all
  single-dimension pixel checks below use it. Ground swath (check_fov) and
  motion blur (check_motion_blur) are left at their nadir approximation —
  neither correction has been derived for those; see the offnadir analysis
  doc's note that swath *ratios* between lenses are tilt-independent even
  though absolute swath isn't.

Traceability:
  R3     – detect AND classify at 90 to 120 m AGL, ΔT ≥ 5 °C
  R3.1   – detection at 120 m, ≥ 90 % confidence
  R3.2   – classification at 90 m, ≥ 80 % confidence
  R1     – nominal altitude 90–120 m
  R2     – cruise speed 2.23 m/s
  R3_CAM_RES  – 4 px across a 0.5 m target at 90 m → derived IFOV bound
  R3_CAM_FOV  – HFOV ≥ 30°
  R3_CAM_NETD – NETD ≤ 50 mK

Design:
  Modular functions returning dicts for JSON serialisation, so this module
  can be imported from a higher-level trade-space or sensitivity analysis.

Usage:
  python thermal_camera_analysis.py          # standalone
  from thermal_camera_analysis import analyse_camera_subsystem
  result = analyse_camera_subsystem()

Johnson Criteria Reference (Johnson 1958, updated by NVTherm):
  The classic Johnson criteria define the number of RESOLUTION CYCLES (line
  pairs) across the MINIMUM target dimension needed for a task at 50%
  probability:

    Detection:    1.0 cycle  (~2 px across target)
    Orientation:  1.4 cycles (~3 px)
    Recognition:  4.0 cycles (~8 px)
    Identification:  6.4 cycles (~13 px)

  Our requirements demand higher confidence levels:
    R3.1: detection at ≥ 90 % → roughly 1.5–2 cycles (~3–4 px)
    R3.2: classification at ≥ 80 % → roughly 6+ cycles (~12+ px)

  "Classification" here means distinguishing deer vs turkey vs human — this
  aligns with the Johnson "recognition" task level (4 cycles nominal).
  For 80 % confidence the required cycles increase to ~6–8 (12–16 px).

  The existing R3_CAM_RES (4 px across 0.5 m at 90 m) sits between the 50 %
  detection threshold (2 px) and the 50 % recognition threshold (8 px).  It
  does NOT guarantee 80 % classification — that is a deliberate engineering
  judgment about what level of pixels-on-target is adequate for the operator
  to distinguish species.

NOTE on the flying altitude:
  There IS a flying altitude requirement — R1 defines nominal altitude range
  of 90–120 m AGL.  R3 says detection AND classification must happen at
  "nominal cruising altitude (90m to 120m AGL)".  R3.1 then specifies
  detection AT 120 m (worst case).  R3.2 specifies classification AT 90 m
  (closest/least challenging).  This analysis respects that ordering.
"""

from __future__ import annotations
import math
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional


# ═══════════════════════════════════════════════════════════════════════════
# 1.  Domain constants  (from model.sysml system-level requirements)
# ═══════════════════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class MissionParameters:
    altitude_min_m: float          = 90.0      # R1 lower, R3.2 classification altitude
    altitude_max_m: float          = 120.0     # R1 upper, R3.1 detection altitude
    cruise_speed_m_s: float        = 2.23      # R2
    delta_t_min_K: float           = 5.0       # R3 – min target-to-background ΔT


@dataclass(frozen=True)
class JohnsonCriteria:
    """
    Classic Johnson criteria at 50 % probability.  "Cycles" are line pairs
    across the MINIMUM target dimension.
    """
    task: str                     = "reference"
    detection_50pct_cycles: float  = 1.0       # ~2 px
    recognition_50pct_cycles: float = 4.0      # ~8 px
    identification_50pct_cycles: float = 6.4   # ~13 px


@dataclass(frozen=True)
class TargetDimensions:
    """
    Characteristic thermal-signature sizes (metres).
    From above (aerial nadir view), the relevant dimensions are the profile
    presented to the camera — this is approximated as the smallest enclosing
    rectangle of the dorsal / top-down silhouette.
    """
    # Deer (top-down: body width ~0.5 m, body length ~1.0 m)
    deer_major_m: float            = 1.0       # length (long axis)
    deer_minor_m: float            = 0.5       # width (short axis — limits recognition)

    # Turkey (top-down: roughly oval, ~0.4-0.5 m long, ~0.3 m wide)
    turkey_major_m: float          = 0.5
    turkey_minor_m: float          = 0.3

    # Human (top-down: shoulders ~0.6 m, torso depth ~0.4 m)
    human_major_m: float           = 0.6       # shoulder width
    human_minor_m: float           = 0.4       # torso depth

    # Reference target used in R3_CAM_RES requirement text
    ref_quadrant_target_m: float   = 0.5       # 0.5 × 0.5 m square


@dataclass(frozen=True)
class CameraRequirements:
    mass_max_g: float              = 200.0     # R3_CAM_WT
    power_max_w: float             = 4.5       # R3_CAM_PWR
    hfov_min_deg: float            = 30.0      # R3_CAM_FOV
    netd_max_mk: float             = 50.0      # R3_CAM_NETD
    res_px_per_0_5m_at_90m: float  = 4.0       # R3_CAM_RES
    cost_max_usd: float            = 720.0     # R3_CAM_COST (raised from 600, David 2026-08-12)


# ═══════════════════════════════════════════════════════════════════════════
# 2.  Geometry helpers
# ═══════════════════════════════════════════════════════════════════════════

AS_BUILT_MOUNT_TILT_DEG = 45.0
# candidates.sysml T13.mountTilt_deg — 45° down-look bracket selected
# 2026-08-07 (TASKS.md 2.8). Recompute the off-nadir factors below if this
# changes; the coupling is the same hazard flagged in model.sysml's
# OffNadirGsd comment.


def deg2rad(deg: float) -> float:
    return deg * math.pi / 180.0


def compute_ifov(hfov_deg: float, h_resolution: int) -> float:
    """Instantaneous field of view (degrees per pixel)."""
    return hfov_deg / h_resolution


def gsd(altitude_m: float, ifov_deg: float, tilt_deg: float = 0.0) -> float:
    """
    Ground Sampling Distance (metres per pixel) along the ALONG-RANGE axis
    at a given altitude and off-nadir tilt. tilt_deg=0 (default) reduces to
    the plain nadir GSD used everywhere before 2026-08-12.

    A camera depressed `tilt` off nadir views an on-axis target at slant
    range alt/cos(tilt); each pixel's ground footprint stretches by
    1/cos(tilt) cross-range and 1/cos(tilt)^2 along-range. The along-range
    axis is larger and binds (analysis/thermal_detection_offnadir_analysis.md
    §2; mirrors model.sysml's OffNadirGsd).
    """
    theta = deg2rad(tilt_deg)
    slant_range_m = altitude_m / math.cos(theta)
    gsd_cross_m = slant_range_m * deg2rad(ifov_deg)
    return gsd_cross_m / math.cos(theta)


def pixels_on_target(target_size_m: float,
                     altitude_m: float,
                     ifov_deg: float,
                     tilt_deg: float = 0.0) -> float:
    """
    Number of pixels subtended by *target_size_m* on the along-range axis,
    at *altitude_m* AGL and *tilt_deg* off nadir (0 = nadir).

    Uses: GSD = off-nadir-adjusted range × IFOV, then pixels = target / GSD.
    """
    if ifov_deg <= 0 or altitude_m <= 0:
        return 0.0
    gsd_m = gsd(altitude_m, ifov_deg, tilt_deg)
    return target_size_m / gsd_m if gsd_m > 0 else float('inf')


def ground_swath(altitude_m: float, hfov_deg: float) -> float:
    return 2.0 * altitude_m * math.tan(deg2rad(hfov_deg / 2.0))


# ═══════════════════════════════════════════════════════════════════════════
# 3.  Core analysis
# ═══════════════════════════════════════════════════════════════════════════

def check_resolution(
    hfov_deg: float,
    h_res: int,
    v_res: int,
    mission: MissionParameters = MissionParameters(),
    targets: TargetDimensions = TargetDimensions(),
    johnson: JohnsonCriteria = JohnsonCriteria(),
    camera_req: CameraRequirements = CameraRequirements(),
    tilt_deg: float = AS_BUILT_MOUNT_TILT_DEG,
) -> Dict:
    """
    For a candidate camera (h_res x v_res, HFOV), compute pixels-on-target
    for each species at the REQUIRED altitudes per R3.1 and R3.2, on the
    binding along-range axis at *tilt_deg* off nadir (default: as-built 45°).

    Detection check  → 120 m (R3.1, worst altitude for detection)
    Classification check → 90 m (R3.2, specified altitude)
    Each species uses its MAJOR (largest) dimension for detection and its
    MINOR (smallest) dimension for classification — the minor axis is the
    limiting factor for distinguishing shapes.

    Also reports what the Johnson 50 % thresholds imply.
    """
    ifov_deg = compute_ifov(hfov_deg, h_res)
    ifov_mrad = ifov_deg * 1000.0 / 180.0 * math.pi

    gsd_90 = gsd(mission.altitude_min_m, ifov_deg, tilt_deg)
    gsd_120 = gsd(mission.altitude_max_m, ifov_deg, tilt_deg)
    gsd_90_nadir = gsd(mission.altitude_min_m, ifov_deg)
    gsd_120_nadir = gsd(mission.altitude_max_m, ifov_deg)

    results = {
        "sensor_config": {
            "hfov_deg": hfov_deg,
            "h_resolution": h_res,
            "v_resolution": v_res,
            "ifov_deg_per_px": round(ifov_deg, 6),
            "ifov_mrad_per_px": round(ifov_mrad, 3),
            "tilt_deg": tilt_deg,
            "gsd_at_90m_m": round(gsd_90, 4),
            "gsd_at_120m_m": round(gsd_120, 4),
            "gsd_at_90m_nadir_m": round(gsd_90_nadir, 4),
            "gsd_at_120m_nadir_m": round(gsd_120_nadir, 4),
        },
        "johnson_reference": asdict(johnson),
        "requirement_checks": {},
        "species_analysis": {},
        "summary": {"pass": True, "failures": []},
    }

    # ── R3_CAM_RES check (4 px across 0.5 m at 90 m) ────────────────
    px_ref = pixels_on_target(
        targets.ref_quadrant_target_m, mission.altitude_min_m, ifov_deg, tilt_deg
    )
    res_pass = px_ref >= camera_req.res_px_per_0_5m_at_90m
    if not res_pass:
        results["summary"]["failures"].append(
            f"R3_CAM_RES: {px_ref:.1f} px across 0.5 m at 90 m "
            f"(needs ≥ {camera_req.res_px_per_0_5m_at_90m})"
        )
    results["requirement_checks"]["R3_CAM_RES"] = {
        "target_m": targets.ref_quadrant_target_m,
        "range_m": mission.altitude_min_m,
        "pixels_on_target": round(px_ref, 2),
        "required_pixels": camera_req.res_px_per_0_5m_at_90m,
        "pass": res_pass,
    }

    # ── Species analysis ─────────────────────────────────────────────
    # Detection: R3.1 says "at 120 m" → use mission.altitude_max_m
    #   Use MAJOR dimension (the larger one, easier to detect)
    #
    # Classification: R3.2 says "at 90 m" → use mission.altitude_min_m
    #   Use MINOR dimension (the smaller one limits shape discrimination)
    species_list = [
        ("deer",  targets.deer_major_m,  targets.deer_minor_m),
        ("turkey", targets.turkey_major_m, targets.turkey_minor_m),
        ("human", targets.human_major_m, targets.human_minor_m),
    ]

    for name, major_m, minor_m in species_list:
        # DETECTION at 120 m using LARGEST target dimension
        px_detect = pixels_on_target(major_m, mission.altitude_max_m, ifov_deg, tilt_deg)
        det_50pct_pass = px_detect >= (johnson.detection_50pct_cycles * 2)
        # ~3 px for 90% confidence
        det_90pct_pass = px_detect >= 3.0

        # CLASSIFICATION at 90 m using SMALLEST target dimension
        #   (classification requires resolving the limiting axis)
        px_classify = pixels_on_target(minor_m, mission.altitude_min_m, ifov_deg, tilt_deg)
        cls_50pct_pass = px_classify >= (johnson.recognition_50pct_cycles * 2)
        # For 80% confidence, roughly 1.5x the 50% threshold ≈ 12 px
        cls_80pct_pass = px_classify >= 12.0

        results["species_analysis"][name] = {
            "dimensions_m": {"major": major_m, "minor": minor_m},
            "detection_at_120m": {
                "altitude_m": mission.altitude_max_m,
                "dimension_used": "major",
                "pixels_on_target": round(px_detect, 2),
                "johnson_50pct_detection_2px": det_50pct_pass,
                "estimated_90pct_detection_3px": det_90pct_pass,
            },
            "classification_at_90m": {
                "altitude_m": mission.altitude_min_m,
                "dimension_used": "minor",
                "pixels_on_target": round(px_classify, 2),
                "johnson_50pct_recognition_8px": cls_50pct_pass,
                "estimated_80pct_classification_12px": cls_80pct_pass,
            },
        }

        if not det_90pct_pass:
            results["summary"]["failures"].append(
                f"{name}: detection at 120 m = {px_detect:.1f} px "
                f"(estimated need ~3 px for ≥90 % confidence)"
            )
        if not cls_50pct_pass:
            # Not a hard failure — flagged for discussion
            results["summary"]["failures"].append(
                f"{name}: classification at 90 m = {px_classify:.1f} px "
                f"(at 50 % Johnson recognition threshold of 8 px: "
                f"{'PASS' if cls_50pct_pass else 'FAIL'}; "
                f"at estimated 80 % threshold ~12 px: "
                f"{'PASS' if cls_80pct_pass else 'FAIL'})"
            )

    results["summary"]["pass"] = len(results["summary"]["failures"]) == 0
    return results


def check_fov(hfov_deg: float,
              mission: MissionParameters = MissionParameters()) -> Dict:
    swath_90 = ground_swath(mission.altitude_min_m, hfov_deg)
    swath_120 = ground_swath(mission.altitude_max_m, hfov_deg)
    return {
        "hfov_deg": hfov_deg,
        "ground_swath_m": {
            "at_90m": round(swath_90, 1),
            "at_120m": round(swath_120, 1),
        },
    }


def check_netd(netd_mk: float,
               mission: MissionParameters = MissionParameters()) -> Dict:
    snr = mission.delta_t_min_K / (netd_mk / 1000.0)
    return {
        "netd_mK": netd_mk,
        "delta_T_K": mission.delta_t_min_K,
        "snr_ratio": round(snr, 1),
        "pass": snr >= 5.0,
        "interpretation": f"{'Adequate' if snr >= 5.0 else 'Marginal'} — "
                          f"{snr:.0f}x SNR for {mission.delta_t_min_K} °K target "
                          f"against {netd_mk:.0f} mK NETD",
    }


def check_motion_blur(speed_m_s: float,
                      altitude_m: float,
                      integration_s: float,
                      ifov_deg: float) -> Dict:
    ifov_rad = deg2rad(ifov_deg)
    gsd_m = altitude_m * ifov_rad
    blur_m = speed_m_s * integration_s
    blur_px = blur_m / gsd_m if gsd_m > 0 else float('inf')
    return {
        "speed_m_s": speed_m_s,
        "altitude_m": altitude_m,
        "integration_s": integration_s,
        "blur_px": round(blur_px, 2),
        "pass": blur_px < 1.0,
    }


# ═══════════════════════════════════════════════════════════════════════════
# 4.  Top-level entry point
# ═══════════════════════════════════════════════════════════════════════════

def analyse_camera_subsystem(
    hfov_deg: float = 30.0,
    h_res: int = 640,
    v_res: int = 512,
    netd_mk: float = 50.0,
    integration_s: float = 0.0167,
    mission: Optional[MissionParameters] = None,
    targets: Optional[TargetDimensions] = None,
    johnson: Optional[JohnsonCriteria] = None,
    camera_req: Optional[CameraRequirements] = None,
    tilt_deg: float = AS_BUILT_MOUNT_TILT_DEG,
) -> Dict:
    """
    Run all camera-subsystem requirement validation checks.

    Returns a nested dict, JSON-serialisable, for downstream processing.
    """
    mission = mission or MissionParameters()
    targets = targets or TargetDimensions()
    johnson = johnson or JohnsonCriteria()
    camera_req = camera_req or CameraRequirements()
    ifov_deg = compute_ifov(hfov_deg, h_res)

    resolution = check_resolution(
        hfov_deg, h_res, v_res, mission, targets, johnson, camera_req, tilt_deg,
    )
    return {
        "mission": asdict(mission),
        "camera_requirements": asdict(camera_req),
        "sensor_config": resolution["sensor_config"],
        "resolution_analysis": resolution,
        "fov_analysis": check_fov(hfov_deg, mission),
        "netd_analysis": check_netd(netd_mk, mission),
        "motion_blur": check_motion_blur(
            mission.cruise_speed_m_s,
            mission.altitude_min_m,
            integration_s,
            ifov_deg,
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════
# 5.  Standalone runner
# ═══════════════════════════════════════════════════════════════════════════

def _report(result: Dict) -> None:
    r = result
    sc = r["sensor_config"]
    ra = r["resolution_analysis"]

    print("=" * 72)
    print("  THERMAL CAMERA REQUIREMENT VALIDATION")
    print("=" * 72)
    print(f"  Sensor:       {sc['h_resolution']}×{sc['v_resolution']}")
    print(f"  HFOV:         {sc['hfov_deg']}°")
    print(f"  IFOV:         {sc['ifov_mrad_per_px']} mrad/px")
    print(f"  Mount tilt:   {sc['tilt_deg']}° off nadir (as-built)")
    print(f"  GSD @ 90 m:   {sc['gsd_at_90m_m']*100:.2f} cm/px along-range "
          f"(nadir would be {sc['gsd_at_90m_nadir_m']*100:.2f} cm/px)")
    print(f"  GSD @ 120 m:  {sc['gsd_at_120m_m']*100:.2f} cm/px along-range "
          f"(nadir would be {sc['gsd_at_120m_nadir_m']*100:.2f} cm/px)")
    print(f"  NETD:         {r['camera_requirements']['netd_max_mk']:.0f} mK")
    print(f"  Integration:  {r['motion_blur']['integration_s']*1000:.0f} ms")
    print()

    # ── Altitudes ─────────────────────────────────────────────────────
    print("── FLYING ALTITUDE REQUIREMENTS (from model.sysml) ──────")
    print(f"  R1: nominal altitude range = {r['mission']['altitude_min_m']}–"
          f"{r['mission']['altitude_max_m']} m AGL")
    print(f"  R3.1: detection at {r['mission']['altitude_max_m']} m (worst case)")
    print(f"  R3.2: classification at {r['mission']['altitude_min_m']} m (closest)")
    print()

    # ── R3_CAM_RES ────────────────────────────────────────────────────
    print("── R3_CAM_RES CHECK ──────────────────────────────────")
    rc = ra["requirement_checks"]["R3_CAM_RES"]
    print(f"  0.5 m × 0.5 m target at 90 m:")
    print(f"    Pixels on target: {rc['pixels_on_target']}")
    print(f"    Requirement: ≥ {rc['required_pixels']} px "
          f"→ {'✓ PASS' if rc['pass'] else '✗ FAIL'}")

    # ── What 4 px actually means ──────────────────────────────────────
    # Back-calculate: 4 px at 90 m → what target dimension?
    ifov_mrad = sc['ifov_mrad_per_px']
    print()
    gsd_90 = sc['gsd_at_90m_m']
    print("── WHAT R3_CAM_RES IMPLIES ───────────────────────────")
    print(f"  IFOV = {ifov_mrad} mrad/px")
    print(f"  GSD  = range × IFOV")
    print(f"       = 90 m × ({ifov_mrad}/1000) rad = {gsd_90*100:.2f} cm/px")
    print(f"  Pixels = target_size / GSD")
    target_4px = 4.0 * gsd_90
    print(f"  4 px at 90 m = 4 × {gsd_90*100:.1f} cm = {target_4px*100:.0f} cm across")
    target_8px = 8.0 * gsd_90
    print(f"  8 px at 90 m = 8 × {gsd_90*100:.1f} cm = {target_8px*100:.0f} cm across (Johnson 50% recognition)")
    target_12px = 12.0 * gsd_90
    print(f"  12 px at 90 m = 12 × {gsd_90*100:.1f} cm = {target_12px*100:.0f} cm across (est. 80% classification)")
    print()

    # ── Species table ────────────────────────────────────────────────
    print("── PER-SPECIES JOHNSON ANALYSIS ──────────────────────")
    print(f"  {'Species':<10} {'Dimension':<12} {'Alt':<5} {'Pixels':<8} "
          f"{'50%Det(2)':<10} {'90%Det(3)':<10} {'50%Rec(8)':<10} {'80%Cls(12)':<10}")
    print(f"  {'-'*70}")

    for name, data in ra["species_analysis"].items():
        det = data["detection_at_120m"]
        cls = data["classification_at_90m"]
        print(f"  {name:<10} {'major':<12} {det['altitude_m']:<5} "
              f"{det['pixels_on_target']:<8} "
              f"{'✓' if det['johnson_50pct_detection_2px'] else '✗':<10} "
              f"{'✓' if det['estimated_90pct_detection_3px'] else '✗':<10} "
              f"{'—':<10} {'—':<10}")
        print(f"  {'':<10} {'minor':<12} {cls['altitude_m']:<5} "
              f"{cls['pixels_on_target']:<8} "
              f"{'—':<10} {'—':<10} "
              f"{'✓' if cls['johnson_50pct_recognition_8px'] else '✗':<10} "
              f"{'✓' if cls['estimated_80pct_classification_12px'] else '✗':<10}")

    print()

    # ── FOV ───────────────────────────────────────────────────────────
    fov = r["fov_analysis"]
    print(f"── R3_CAM_FOV: {fov['hfov_deg']}° HFOV ───────────────────")
    for k, v in fov["ground_swath_m"].items():
        print(f"  Ground swath {k}: {v} m")

    # ── NETD ──────────────────────────────────────────────────────────
    nm = r["netd_analysis"]
    print(f"\n── R3_CAM_NETD: {nm['netd_mK']:.0f} mK ────────────────")
    print(f"  {nm['interpretation']}")

    # ── Motion blur ───────────────────────────────────────────────────
    mb = r["motion_blur"]
    print(f"\n── MOTION BLUR @ {mb['speed_m_s']} m/s ──────────────────")
    print(f"  Blur: {mb['blur_px']} px  {'✓' if mb['pass'] else '✗'}")
    print(f"  (needs < 1 px for sharp image)")

    # ── Summary ───────────────────────────────────────────────────────
    print(f"\n{'='*72}")
    fails = ra["summary"]["failures"]
    if fails:
        print(f"  ISSUES FOUND ({len(fails)}):")
        for f in fails:
            print(f"    • {f}")
    else:
        print(f"  ✓  All requirements validated.")
    print(f"{'='*72}\n")


def main():
    import json

    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  AS-BUILT: T13 PurpleRiver Mini 640, 18mm/24.1° HFOV,   ║")
    print("║  50 mK NETD, 45° down-look mount                        ║")
    print("╚══════════════════════════════════════════════════════════╝")
    result_asbuilt = analyse_camera_subsystem(hfov_deg=24.1, h_res=640, v_res=512)
    _report(result_asbuilt)

    with open(".openclaw/tmp/thermal_camera_analysis.json", "w") as f:
        json.dump(result_asbuilt, f, indent=2)
    print("Full JSON written to .openclaw/tmp/thermal_camera_analysis.json")

    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║    BASELINE: 640×512, 30° HFOV, 50 mK NETD, 45° tilt    ║")
    print("╚══════════════════════════════════════════════════════════╝")
    result = analyse_camera_subsystem(hfov_deg=30.0, h_res=640, v_res=512)
    _report(result)

    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║    COMPARISON: 320×240, 30° HFOV, 50 mK NETD, 45° tilt  ║")
    print("╚══════════════════════════════════════════════════════════╝")
    result2 = analyse_camera_subsystem(hfov_deg=30.0, h_res=320, v_res=240)
    _report(result2)


if __name__ == "__main__":
    main()