#!/usr/bin/env python3
"""
flight_time_model.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Purpose:
  High-fidelity multirotor endurance ("max flight time") model for the thermal
  surveillance drone, integrated with the SysML v2 model. Replaces the naive
  `flightTime = batteryEnergy / totalPower` calculation in
  DroneSystemModel::Analysis with a momentum-theory (actuator-disk) propulsion
  model plus a forward-flight parasitic-drag term.

  The script READS the SysML model (model.sysml + candidates.sysml) for every
  component candidate (including the real battery candidates BAT01–BAT21; it
  falls back to a generic LiPo/Li-ion grid only if none are present), SWEEPS
  complete drone configurations — fully crossing the flight-time drivers
  (airframe × battery × SBC × VTX × thermal camera) while holding the sub-1 W
  peripherals (FPV camera, GPS, RX) at a lightest representative — and FILTERS
  out interface-incompatible pairings (see Compatibility filtering below). The
  DVR is NOT crossed: it is excluded from the flight-time calc (SBC-stage build)
  but each thermal must still have a compatible DVR for the earlier stages. It
  then WRITES the results back out as:
    • flight_time_results.csv      — EVERY instance: all components (+ generic
                                     battery attributes) and its max flight time
    • flight_time_instances.sysml  — SysML v2 instance table for the baseline +
                                     top-N configs (validatable in Syside)
    • flight_time_results.md       — ranked summary + assumptions

  Component-inclusion logic (important):
    Some airframes are BNF/PNP bundles that already include a VTX, FPV camera,
    GPS, and/or receiver. For those, the script does NOT add a separate such
    component — the bundled part's MASS is already in the airframe's as-built
    weight, so only its POWER draw is added (propulsion power excludes avionics),
    using a representative draw for the category. Non-bundled peripherals are
    added with their own mass and power.

  Compatibility filtering (removes non-real configurations):
    The executable counterpart of the interface rules declared in
    DroneSystemModel::Architecture::Compatibility. A pairing is dropped if:
      • P1 battery↔airframe: the battery series-cell count (cells_s) falls
        outside the airframe's [minCells_s, maxCells_s] ESC/motor window — e.g.
        a 4S pack on a 6S-only frame, or a 6S pack on the 3–5S Darwin 129.
      • V2 thermal↔DVR: the thermal camera's video output must be recordable by
        SOME DVR (CVBS via DVR1-6, or digital HDMI/USB via DVR7-9). A thermal
        with no compatible recorder (raw SPI/CSI/CMOS only) can't be recorded in
        the pre-SBC stages and is dropped. The DVR is excluded from the flight-
        time calc (the SBC records at the SBC stage); it is kept only for
        earlier-stage compatibility and cost (see MODEL_ISSUES.md §C11/C12).
    Pruned counts are printed and reported in flight_time_results.md.

Traceability:
  R2  – cruise ground speed 2.23 m/s             (forward-flight regime)
  R6  – min sustained flight time 1800 s / 30 min (hover/still-air endurance)
  R7  – ≥ 2800 m range in 4.5 m/s wind           (headwind cruise scenario)
  R8  – stretch flight time 3600 s / 60 min       (hover/still-air endurance)
  R4_BAT_ENERGY / R4_BAT_WT – battery energy vs mass trade (this sweep)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHYSICS MODEL  (momentum / actuator-disk theory + forward-flight drag)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Same model family used by endurance calculators such as eCalc (xcopterCalc) and
the multirotor-energy literature (e.g. Bauersfeld & Scaramuzza 2022; Bershadsky
et al. 2016). Fully analytic.

  Hover induced velocity (actuator disk):
      v_h = sqrt( T / (2·ρ·A_total) )
  where T = total thrust, ρ = air density, A_total = N·π·(D/2)² (N rotors).

  Forward flight (level, low advance ratio) — Glauert induced-velocity:
      v_i = v_h² / sqrt( V² + v_i² )          (solved iteratively)
  Parasitic body drag and the thrust needed to overcome it:
      D_para = ½·ρ·V²·C_d·A_front
      T      = sqrt( (m·g)² + D_para² )
  Mechanical rotor power (Figure of Merit folds in profile/tip losses):
      P_induced  = T·v_i / FoM
      P_parasite = D_para·V
      P_mech     = P_induced + P_parasite
  Electrical power into the drivetrain, plus avionics/payload overhead:
      P_elec  = P_mech / η_drive
      P_total = P_elec + P_payload
  Endurance from usable battery energy:
      E_usable = V_nom · C_Ah · 3600 · DoD            [J]
      t        = E_usable / P_total                   [s]

  Hover (V=0) reduces to the classic closed form:
      P_hover = (m·g)^1.5 / ( FoM · sqrt(2·ρ·A_total) ) / η_drive  + P_payload

Assumptions (all tunable in PhysicsParams / documented per run):
  • N_rotors = 4 (all candidate airframes are quads).
  • ρ = 1.225 kg/m³ (ISA sea level; 90–120 m AGL ≈ sea level).
  • FoM = 0.65 (small-multirotor figure of merit, typical 0.6–0.7).
  • η_drive = 0.80 (combined motor×ESC efficiency, typical 0.75–0.85).
  • C_d = 1.0 (bluff-body), A_front ≈ wheelbase × 0.05 m body band.
  • Depth of discharge: LiPo 0.80, Li-ion 0.85 (usable fraction for cycle life).
  • "Max flight time" headline = still-air hover endurance (min-power regime).
  These are first-order estimates; treat results as comparative, not absolute.
  NOTE the "power bucket": slow forward flight uses LESS power than hover
  (translational lift cuts induced power), so cruise/wind endurance can exceed
  hover — that is correct, not a bug.

Usage:
  python analysis/flight_time_model.py            # parse model, sweep, write outputs
  from flight_time_model import endurance, propulsion_power   # importable
"""

from __future__ import annotations

import csv
import math
import re
import statistics
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

# ──────────────────────────────────────────────────────────────────────────
# Paths (script lives in analysis/, model files live in the repo root)
# ──────────────────────────────────────────────────────────────────────────
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MODEL_SYSML = ROOT / "model.sysml"
CANDIDATES_SYSML = ROOT / "candidates.sysml"

OUT_SYSML = HERE / "flight_time_instances.sysml"
OUT_MD = HERE / "flight_time_results.md"
OUT_CSV = HERE / "flight_time_results.csv"
OUT_VALUE_MD = HERE / "flight_time_value_ranking.md"
OUT_CHART = HERE / "cost_vs_flighttime.png"

G = 9.80665             # gravitational acceleration [m/s²]
RAIL_VOLTAGE_V = 5.0    # avionics rail voltage for deriving power from currentDraw
SYSML_TOP_N = 100       # how many top configs to emit as SysML instances / MD rows


# ──────────────────────────────────────────────────────────────────────────
# Physics parameters (documented assumptions; edit here to run sensitivities)
# ──────────────────────────────────────────────────────────────────────────
@dataclass
class PhysicsParams:
    n_rotors: int = 4
    air_density: float = 1.225          # ρ [kg/m³] ISA sea level
    figure_of_merit: float = 0.65       # FoM (rotor efficiency, 0.6–0.7)
    drivetrain_eff: float = 0.80        # η motor×ESC (0.75–0.85)
    drag_coeff: float = 1.0             # C_d bluff body
    body_height_m: float = 0.05         # frontal-area band height vs wheelbase
    cruise_speed_ms: float = 2.23       # R2 still-air cruise ground speed
    wind_speed_ms: float = 4.5          # R7 sustained wind (headwind worst case)


@dataclass
class Battery:
    name: str
    chemistry: str
    cells_s: int
    capacity_mah: float
    nominal_v: float
    usable_dod: float
    mass_g: float
    energy_wh: float
    usable_energy_j: float
    cost: float = 0.0


@dataclass
class Airframe:
    ident: str
    name: str
    mass_g: float
    prop_in: float
    wheelbase_mm: Optional[float]
    purchase_type: str
    vtx_incl: bool
    fpv_incl: bool
    gps_incl: bool
    rx_incl: bool
    min_cells: Optional[int] = None   # min battery series cells (ESC/motor rated)
    max_cells: Optional[int] = None   # max battery series cells (ESC/motor rated)
    max_thrust_g: Optional[float] = None  # published max static thrust per motor [g] (B5); None → prop-size heuristic
    cost: float = 0.0                     # airframe cost_USD (incl. bundled VTX/FPV/GPS/RX for BNF/PNP)


@dataclass
class Component:
    """A generic payload/avionics component candidate (mass + power)."""
    category: str
    ident: str
    name: str
    mass_g: float
    power_w: float
    video_formats: frozenset = frozenset()   # canonical video-link formats (see _video_formats)
    cost: float = 0.0                        # component cost_USD


# ──────────────────────────────────────────────────────────────────────────
# Core physics
# ──────────────────────────────────────────────────────────────────────────
def disk_area(prop_diameter_m: float, n_rotors: int) -> float:
    """Total actuator-disk area for N rotors of the given diameter [m²]."""
    return n_rotors * math.pi * (prop_diameter_m / 2.0) ** 2


def _induced_velocity_forward(v_h: float, v_fwd: float, tol: float = 1e-6) -> float:
    """Glauert forward-flight induced velocity, solved by fixed-point iteration."""
    if v_fwd <= 0.0:
        return v_h
    v_i = v_h
    for _ in range(200):
        new = v_h * v_h / math.sqrt(v_fwd * v_fwd + v_i * v_i)
        if abs(new - v_i) < tol:
            return new
        v_i = new
    return v_i


def propulsion_power(mass_kg: float, v_fwd: float, a_total: float,
                     a_front: float, p: PhysicsParams) -> float:
    """Electrical propulsion power [W] at forward speed v_fwd (0 = hover)."""
    weight = mass_kg * G
    drag = 0.5 * p.air_density * v_fwd * v_fwd * p.drag_coeff * a_front
    thrust = math.sqrt(weight * weight + drag * drag)
    v_h = math.sqrt(thrust / (2.0 * p.air_density * a_total))
    v_i = _induced_velocity_forward(v_h, v_fwd)
    p_induced = thrust * v_i / p.figure_of_merit
    p_parasite = drag * v_fwd
    p_mech = p_induced + p_parasite
    return p_mech / p.drivetrain_eff


def endurance(usable_energy_j: float, total_power_w: float) -> float:
    """Flight time [s] = usable energy / total power."""
    return usable_energy_j / total_power_w if total_power_w > 0 else 0.0


# Rough max static thrust per motor by prop size (6S-class, g) — throttle /
# feasibility estimate only. Interpolated; documented as approximate.
_THRUST_BY_PROP_IN = {3.0: 450, 4.0: 750, 5.0: 1150, 6.0: 1450, 7.0: 1750,
                      8.0: 2200, 10.0: 3000}


def _max_thrust_per_motor_g(prop_in: float) -> float:
    keys = sorted(_THRUST_BY_PROP_IN)
    if prop_in <= keys[0]:
        return _THRUST_BY_PROP_IN[keys[0]]
    if prop_in >= keys[-1]:
        return _THRUST_BY_PROP_IN[keys[-1]]
    for lo, hi in zip(keys, keys[1:]):
        if lo <= prop_in <= hi:
            f = (prop_in - lo) / (hi - lo)
            return _THRUST_BY_PROP_IN[lo] + f * (_THRUST_BY_PROP_IN[hi] - _THRUST_BY_PROP_IN[lo])
    return _THRUST_BY_PROP_IN[keys[-1]]


# ──────────────────────────────────────────────────────────────────────────
# Generic battery sweep (informs the future battery market analysis)
# ──────────────────────────────────────────────────────────────────────────
_CHEM = {
    #            Wh/kg(pack)  V/cell  usable DoD
    "LiPo":      (150.0,      3.7,    0.80),
    "Li-ion":    (220.0,      3.6,    0.85),
}
_CELL_COUNTS = [4, 6]
_CAPACITIES_MAH = [3000, 4000, 5000, 6000, 8000, 10000, 12000]


def generate_generic_batteries() -> list[Battery]:
    out: list[Battery] = []
    for chem, (wh_per_kg, v_cell, dod) in _CHEM.items():
        for s in _CELL_COUNTS:
            v_nom = round(s * v_cell, 1)
            for cap in _CAPACITIES_MAH:
                energy_wh = v_nom * cap / 1000.0
                mass_g = energy_wh / wh_per_kg * 1000.0
                usable_j = v_nom * (cap / 1000.0) * 3600.0 * dod
                out.append(Battery(f"{chem} {s}S {cap}mAh", chem, s, float(cap),
                                   v_nom, dod, round(mass_g, 1), round(energy_wh, 1),
                                   round(usable_j, 1)))
    return out


# ──────────────────────────────────────────────────────────────────────────
# Minimal SysML v2 parser (extracts `:>> key = value [unit];` from part blocks)
# ──────────────────────────────────────────────────────────────────────────
_PART_RE = re.compile(r"part\s+(\w+)\s*:\s*(\w+)\s*\{", re.MULTILINE)
_BIND_RE = re.compile(r":>>\s*(\w+)\s*=\s*([^;]+);")


def _parse_value(raw: str):
    raw = raw.strip()
    m = re.match(r'^"(.*)"$', raw)
    if m:
        return m.group(1)
    if raw in ("true", "false"):
        return raw == "true"
    num = re.match(r"^(-?\d+(?:\.\d+)?)\s*(\[\w+\])?", raw)
    if num:
        val = float(num.group(1))
        return int(val) if val.is_integer() and "." not in num.group(1) else val
    return raw


def parse_part_blocks(text: str) -> list[dict]:
    """Return [{ident, type, attrs:{}}] for every `part X : T { ... }` block."""
    blocks = []
    for m in _PART_RE.finditer(text):
        ident, ptype = m.group(1), m.group(2)
        depth, i, n = 0, m.end() - 1, len(text)
        while i < n:
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    break
            i += 1
        body = text[m.end():i]
        attrs = {k: _parse_value(v) for k, v in _BIND_RE.findall(body)}
        blocks.append({"ident": ident, "type": ptype, "attrs": attrs})
    return blocks


# SysML part-def type → component category label
_CATEGORY_BY_TYPE = {
    "CameraSubsystem": "thermal",
    "SingleBoardComputerPayload": "sbc",
    "ThermalVideoRecorder": "dvr",
    "VideoTransmitter": "vtx",
    "FpvCamera": "fpv",
    "GpsModule": "gps",
    "RadioReceiver": "rx",
}

# GCS cost (R4): the laptop is the ground station. PRIMARY link = cheapest
# standalone ELRS USB dongle (control + telemetry) + cheapest 5.8 GHz VRX with
# range margin (>= 4 km, e.g. the Skydroid true-diversity UVC). BOTH control and
# video are hard 2.8 km links (R4_GCS_RANGE); the video link needs a patch/
# directional ground antenna. A cheapest integrated handheld radio is added as the
# Phase-1 / backup manual control path. Fixed across configs (not swept).


# Map a free-text video-interface string (e.g. "CVBS / USB / UART") to the set
# of canonical video-LINK formats it can carry. This is the executable analogue
# of DroneSystemModel::Architecture::Compatibility::VideoFormat — a video link is
# real only when the source and sink share at least one format. Raw sensor buses
# (SPI/I2C/UART/CMOS/LVCMOS) are NOT video links and are intentionally ignored,
# so a sensor that only exposes those cannot feed a display/record chain.
def _video_formats(s: Optional[str]) -> frozenset:
    if not s:
        return frozenset()
    t = s.lower()
    out = set()
    if "cvbs" in t or "composite" in t or "analog" in t:
        out.add("CVBS")
    if "usb" in t:                              # USB UVC capture-capable
        out.add("USB")
    if "csi" in t or "mipi" in t:
        out.add("MIPI")
    if "hdmi" in t:
        out.add("HDMI")
    if "dji" in t:
        out.add("DJI")
    if "hdzero" in t:
        out.add("HDZERO")
    if "walksnail" in t:
        out.add("WALKSNAIL")
    return frozenset(out)


def load_model():
    """Parse airframes, payload component candidates, and battery candidates from candidates.sysml."""
    blocks = parse_part_blocks(CANDIDATES_SYSML.read_text(encoding="utf-8"))

    airframes: list[Airframe] = []
    components: dict[str, list[Component]] = {c: [] for c in _CATEGORY_BY_TYPE.values()}
    real_batteries: list[Battery] = []
    radio_min: Optional[float] = None; radio_name: Optional[str] = None  # handheld radio (Phase-1 / backup)
    tlm_min: Optional[float] = None; tlm_name: Optional[str] = None       # ELRS USB dongle (primary control+telemetry)
    vrx_min: Optional[float] = None; vrx_name: Optional[str] = None       # analog VRX w/ capture (live video)

    for b in blocks:
        a = b["attrs"]
        if b["type"] == "Airframe":
            if "mass" not in a or "propSize_in" not in a:
                continue  # skip airframes lacking the geometry we need
            airframes.append(Airframe(
                ident=b["ident"], name=a.get("name", b["ident"]),
                mass_g=float(a["mass"]), prop_in=float(a["propSize_in"]),
                wheelbase_mm=float(a["wheelbase"]) if "wheelbase" in a else None,
                purchase_type=a.get("purchaseType", ""),
                vtx_incl=bool(a.get("vtxIncluded", False)),
                fpv_incl=bool(a.get("fpvCameraIncluded", False)),
                gps_incl=bool(a.get("gpsIncluded", False)),
                rx_incl=bool(a.get("receiverIncluded", False)),
                min_cells=int(a["minCells_s"]) if "minCells_s" in a else None,
                max_cells=int(a["maxCells_s"]) if "maxCells_s" in a else None,
                max_thrust_g=float(a["maxThrustPerMotor_g"]) if "maxThrustPerMotor_g" in a else None,
                cost=float(a.get("cost_USD", 0.0)),
            ))
        elif b["type"] == "Battery":
            required = {"cells_s", "capacity_mAh", "nominalVoltage", "usableDoD", "mass"}
            if not required.issubset(a):
                continue
            v_nom = float(a["nominalVoltage"])
            cap_mah = float(a["capacity_mAh"])
            dod = float(a["usableDoD"])
            energy_wh = v_nom * cap_mah / 1000.0
            usable_j = energy_wh * 3600.0 * dod
            real_batteries.append(Battery(
                name=str(a.get("name", b["ident"])),
                chemistry=str(a.get("chemistry", "Li-ion")),
                cells_s=int(a["cells_s"]),
                capacity_mah=cap_mah,
                nominal_v=v_nom,
                usable_dod=dod,
                mass_g=float(a["mass"]),
                energy_wh=round(energy_wh, 1),
                usable_energy_j=round(usable_j, 1),
                cost=float(a.get("cost_USD", 0.0)),
            ))
        elif b["type"] in _CATEGORY_BY_TYPE:
            cat = _CATEGORY_BY_TYPE[b["type"]]
            if "mass" not in a:
                continue
            # Power: prefer an explicit `power`; else derive from currentDraw on
            # the 5 V avionics rail (ELRS receivers spec currentDraw, not power).
            if "power" in a:
                power_w = float(a["power"])
            elif "currentDraw" in a:
                power_w = round(float(a["currentDraw"]) * RAIL_VOLTAGE_V, 3)
            else:
                continue
            # Video-link capability: thermal cams expose their OUTPUT via
            # outputInterface; DVRs/VTX expose their INPUT via videoInput.
            fmt_src = a.get("outputInterface") or a.get("videoInput") or a.get("outputType")
            components[cat].append(Component(
                category=cat, ident=b["ident"], name=a.get("name", b["ident"]),
                mass_g=float(a["mass"]), power_w=power_w,
                video_formats=_video_formats(fmt_src),
                cost=float(a.get("cost_USD", 0.0)),
            ))
        elif b["type"] == "RadioControlTransmitter":
            # cheapest full integrated handheld radio (Phase-1 / backup manual control);
            # skip bare TX modules that need a host radio.
            c = float(a.get("cost_USD", 0.0))
            if c > 0 and "integrated" in str(a.get("txType", "")).lower() and (radio_min is None or c < radio_min):
                radio_min = c; radio_name = str(a.get("name", b["ident"]))
        elif b["type"] == "TelemetryGroundLink":
            # standalone laptop dongle only: cost > 0 and no extra hardware/soldering
            # (excludes the $0 "reuse your radio" option and DIY/2nd-RX approaches).
            c = float(a.get("cost_USD", 0.0))
            if c > 0 and str(a.get("extraHardwareNeeded", "")).strip().lower() == "none" and (tlm_min is None or c < tlm_min):
                tlm_min = c; tlm_name = str(a.get("name", b["ident"]))
        elif b["type"] == "VideoReceiver":
            # a real 5.8 GHz RF receiver (not a bare AV-capture dongle) with range
            # MARGIN over the hard 2.8 km video link — require >= 4 km so the costed
            # default isn't sitting exactly at the limit (VRX1 = 2.8 km, zero margin).
            c = float(a.get("cost_USD", 0.0))
            rng = float(a["range"]) if "range" in a else 0.0
            if (c > 0 and "ghz" in str(a.get("inputFrequency", "")).lower() and rng >= 4.0
                    and (vrx_min is None or c < vrx_min)):
                vrx_min = c; vrx_name = str(a.get("name", b["ident"]))
    gcs_cost = round((radio_min or 0.0) + (tlm_min or 0.0) + (vrx_min or 0.0), 2)
    gcs_parts = {"radio": radio_name, "radio_cost": radio_min or 0.0,
                 "dongle": tlm_name, "dongle_cost": tlm_min or 0.0,
                 "vrx": vrx_name, "vrx_cost": vrx_min or 0.0}
    return airframes, components, real_batteries, gcs_cost, gcs_parts


def lightest(comps: list[Component]) -> Component:
    return min(comps, key=lambda c: c.mass_g)


def representative_power(comps: list[Component]) -> float:
    """Median power of a category — used for an airframe-bundled peripheral."""
    return round(statistics.median(c.power_w for c in comps), 2)


# ──────────────────────────────────────────────────────────────────────────
# Sweep
# ──────────────────────────────────────────────────────────────────────────
# Column order for the per-instance CSV (every component + battery + result).
CSV_FIELDS = [
    "config_id",
    "airframe_id", "airframe", "purchase_type", "airframe_mass_g", "prop_in", "wheelbase_mm",
    "battery", "chemistry", "cells_s", "capacity_mah", "pack_voltage_v", "usable_dod",
    "battery_mass_g", "battery_energy_wh", "usable_energy_wh",
    "thermal_id", "thermal_name", "thermal_mass_g", "thermal_power_w",
    "sbc_id", "sbc_name", "sbc_mass_g", "sbc_power_w",
    "dvr_id", "dvr_name", "dvr_mass_g", "dvr_power_w",
    "vtx_id", "vtx_name", "vtx_source", "vtx_mass_g", "vtx_power_w",
    "fpv_id", "fpv_name", "fpv_source", "fpv_mass_g", "fpv_power_w",
    "gps_id", "gps_name", "gps_source", "gps_mass_g", "gps_power_w",
    "rx_id", "rx_name", "rx_source", "rx_mass_g", "rx_power_w",
    "added_payload_mass_g", "total_payload_power_w", "all_up_mass_g",
    "hover_power_w", "cruise_power_w", "headwind_power_w",
    "max_flight_time_hover_min", "flight_time_cruise_min", "flight_time_headwind_min",
    "hover_throttle_pct", "meets_r6_30min", "meets_r8_60min", "flyable",
    "airframe_cost_usd", "battery_cost_usd", "thermal_cost_usd", "sbc_cost_usd",
    "dvr_cost_usd", "vtx_cost_usd", "fpv_cost_usd", "gps_cost_usd", "rx_cost_usd",
    "drone_cost_usd", "gcs_cost_usd", "total_system_cost_usd", "endurance_per_1000usd",
    "meets_budget_r4",
]


def _peripheral(airframe_incl: bool, swept: Optional[Component],
                rep: Component, rep_power: float):
    """Resolve a peripheral to (id, name, source, mass_added_g, power_w, cost_added).

    If bundled with the airframe: mass AND cost are already in the airframe
    weight/price (0 added), power = representative category draw. Otherwise use
    the given component (adds its own mass, power, and cost).
    """
    if airframe_incl:
        return ("included", "bundled with airframe", "included", 0.0, rep_power, 0.0)
    c = swept if swept is not None else rep
    return (c.ident, c.name, "external", c.mass_g, c.power_w, c.cost)


def evaluate(af: Airframe, bat: Battery, thermal: Component, sbc: Component,
             dvr: Component, vtx: Optional[Component], reps: dict,
             rep_pow: dict, p: PhysicsParams, config_id: str,
             gcs_cost: float = 0.0) -> dict:
    # Resolve peripherals with inclusion logic.
    vtx_id, vtx_name, vtx_src, vtx_m, vtx_p, vtx_c = _peripheral(af.vtx_incl, vtx, reps["vtx"], rep_pow["vtx"])
    fpv_id, fpv_name, fpv_src, fpv_m, fpv_p, fpv_c = _peripheral(af.fpv_incl, None, reps["fpv"], rep_pow["fpv"])
    gps_id, gps_name, gps_src, gps_m, gps_p, gps_c = _peripheral(af.gps_incl, None, reps["gps"], rep_pow["gps"])
    rx_id, rx_name, rx_src, rx_m, rx_p, rx_c = _peripheral(af.rx_incl, None, reps["rx"], rep_pow["rx"])

    # Mission additions (never bundled) add mass + power. The DVR is EXCLUDED —
    # the headline endurance is the SBC-stage build (SBC present, no DVR); the
    # DVR (`dvr`) is the earlier-stage recorder, reported but not flown here.
    added_mass = (thermal.mass_g + sbc.mass_g
                  + vtx_m + fpv_m + gps_m + rx_m)
    payload_power = (thermal.power_w + sbc.power_w
                     + vtx_p + fpv_p + gps_p + rx_p)

    auw_g = af.mass_g + bat.mass_g + added_mass
    mass_kg = auw_g / 1000.0
    a_total = disk_area(af.prop_in * 0.0254, p.n_rotors)
    a_front = ((af.wheelbase_mm or 250.0) / 1000.0) * p.body_height_m

    p_hover = propulsion_power(mass_kg, 0.0, a_total, a_front, p) + payload_power
    p_cruise = propulsion_power(mass_kg, p.cruise_speed_ms, a_total, a_front, p) + payload_power
    p_hw = propulsion_power(mass_kg, p.cruise_speed_ms + p.wind_speed_ms, a_total, a_front, p) + payload_power

    t_hover = endurance(bat.usable_energy_j, p_hover) / 60.0
    t_cruise = endurance(bat.usable_energy_j, p_cruise) / 60.0
    t_hw = endurance(bat.usable_energy_j, p_hw) / 60.0

    # Per-motor max thrust: prefer the airframe's bound figure (B5); else the
    # prop-size heuristic (which under-rates LR motors — see MODEL_ISSUES B5).
    mt_per_motor = af.max_thrust_g if af.max_thrust_g else _max_thrust_per_motor_g(af.prop_in)
    throttle = (auw_g / p.n_rotors) / mt_per_motor

    # Cost (R4): bundled VTX/FPV/GPS/RX add $0 (already in the airframe price);
    # the DVR IS included (it is used in the earlier stages). The GCS is a fixed
    # system add-on (cheapest representative ground set).
    drone_cost = (af.cost + bat.cost + thermal.cost + sbc.cost + dvr.cost
                  + vtx_c + fpv_c + gps_c + rx_c)
    total_cost = drone_cost + gcs_cost

    return {
        "config_id": config_id,
        "airframe_id": af.ident, "airframe": af.name, "purchase_type": af.purchase_type,
        "airframe_mass_g": af.mass_g, "prop_in": af.prop_in,
        "wheelbase_mm": af.wheelbase_mm if af.wheelbase_mm is not None else "",
        "battery": bat.name, "chemistry": bat.chemistry, "cells_s": bat.cells_s,
        "capacity_mah": bat.capacity_mah, "pack_voltage_v": bat.nominal_v,
        "usable_dod": bat.usable_dod, "battery_mass_g": bat.mass_g,
        "battery_energy_wh": bat.energy_wh,
        "usable_energy_wh": round(bat.usable_energy_j / 3600.0, 1),
        "thermal_id": thermal.ident, "thermal_name": thermal.name,
        "thermal_mass_g": thermal.mass_g, "thermal_power_w": thermal.power_w,
        "sbc_id": sbc.ident, "sbc_name": sbc.name, "sbc_mass_g": sbc.mass_g,
        "sbc_power_w": sbc.power_w,
        "dvr_id": dvr.ident, "dvr_name": dvr.name, "dvr_mass_g": dvr.mass_g,
        "dvr_power_w": dvr.power_w,
        "vtx_id": vtx_id, "vtx_name": vtx_name, "vtx_source": vtx_src,
        "vtx_mass_g": vtx_m, "vtx_power_w": vtx_p,
        "fpv_id": fpv_id, "fpv_name": fpv_name, "fpv_source": fpv_src,
        "fpv_mass_g": fpv_m, "fpv_power_w": fpv_p,
        "gps_id": gps_id, "gps_name": gps_name, "gps_source": gps_src,
        "gps_mass_g": gps_m, "gps_power_w": gps_p,
        "rx_id": rx_id, "rx_name": rx_name, "rx_source": rx_src,
        "rx_mass_g": rx_m, "rx_power_w": rx_p,
        "added_payload_mass_g": round(added_mass, 1),
        "total_payload_power_w": round(payload_power, 2),
        "all_up_mass_g": round(auw_g, 1),
        "hover_power_w": round(p_hover, 1), "cruise_power_w": round(p_cruise, 1),
        "headwind_power_w": round(p_hw, 1),
        "max_flight_time_hover_min": round(t_hover, 1),
        "flight_time_cruise_min": round(t_cruise, 1),
        "flight_time_headwind_min": round(t_hw, 1),
        "hover_throttle_pct": round(throttle * 100.0, 1),
        "meets_r6_30min": t_hover >= 30.0, "meets_r8_60min": t_hover >= 60.0,
        "flyable": throttle <= 0.60,
        "airframe_cost_usd": round(af.cost, 2), "battery_cost_usd": round(bat.cost, 2),
        "thermal_cost_usd": round(thermal.cost, 2), "sbc_cost_usd": round(sbc.cost, 2),
        "dvr_cost_usd": round(dvr.cost, 2), "vtx_cost_usd": round(vtx_c, 2),
        "fpv_cost_usd": round(fpv_c, 2), "gps_cost_usd": round(gps_c, 2),
        "rx_cost_usd": round(rx_c, 2),
        "drone_cost_usd": round(drone_cost, 2), "gcs_cost_usd": round(gcs_cost, 2),
        "total_system_cost_usd": round(total_cost, 2),
        "endurance_per_1000usd": round(t_hover / total_cost * 1000.0, 2) if total_cost > 0 else 0.0,
        "meets_budget_r4": total_cost <= 2500.0,
    }


def iter_configs(airframes, components, batteries, p: PhysicsParams,
                 stats: Optional[dict] = None, gcs_cost: float = 0.0):
    """Yield one result dict per REAL (compatibility-filtered) configuration.

    Two interface-compatibility filters prune non-buildable pairings — the
    executable counterpart of the rules declared in
    DroneSystemModel::Architecture::Compatibility:
      • P1 battery↔airframe (BatteryVoltageCompatible): the battery series-cell
        count must fall within the airframe's [min_cells, max_cells] ESC/motor
        window. (Drops e.g. a 4S pack on a 6S-only frame.)
      • V2 thermal↔DVR (VideoFormatCompatible): the thermal camera's video
        output must share a format with SOME DVR's input (CVBS, HDMI, or USB —
        DVR1-6 are CVBS, DVR7-9 are digital). A thermal with no compatible
        recorder cannot be recorded in the pre-SBC stages and is dropped.

    DVR HANDLING: the DVR is NOT a flight-time sweep dimension and its mass/power
    are EXCLUDED from the endurance calc — the headline "max flight time" is the
    SBC-stage build (SBC present, DVR removed). The DVR is still required for the
    earlier (pre-SBC) stages, so each thermal must have a compatible DVR; the
    lightest compatible one is carried into the CSV for earlier-stage / cost
    reference (its cost rolls up in the SysML model's totalCost, not here).
    """
    reps = {cat: lightest(components[cat]) for cat in ("vtx", "fpv", "gps", "rx")}
    rep_pow = {cat: representative_power(components[cat]) for cat in ("vtx", "fpv", "gps", "rx")}
    thermals, sbcs, dvrs = components["thermal"], components["sbc"], components["dvr"]

    # Lightest DVR whose input format can record this thermal's output, or None.
    def compatible_dvr(thermal: Component) -> Optional[Component]:
        cands = [d for d in dvrs if thermal.video_formats & d.video_formats]
        return min(cands, key=lambda d: d.mass_g) if cands else None

    n = 0
    for af in airframes:
        # VTX is swept only when not bundled; otherwise a single "included" pass.
        vtx_opts = [None] if af.vtx_incl else components["vtx"]
        inner_per_bat = len(thermals) * len(sbcs) * len(vtx_opts)
        inner_per_thermal = len(sbcs) * len(vtx_opts)
        for bat in batteries:
            # ── Filter P1: battery cell count must fit the airframe window ──
            if af.min_cells is not None and not (af.min_cells <= bat.cells_s <= af.max_cells):
                if stats is not None:
                    stats["voltage_pruned"] += inner_per_bat
                continue
            for thermal in thermals:
                # ── Filter V2: thermal must have a compatible (recordable) DVR ──
                dvr = compatible_dvr(thermal)
                if dvr is None:
                    if stats is not None:
                        stats["video_pruned"] += inner_per_thermal
                    continue
                for sbc in sbcs:
                    for vtx in vtx_opts:
                        n += 1
                        yield evaluate(af, bat, thermal, sbc, dvr, vtx,
                                       reps, rep_pow, p, f"C{n:06d}", gcs_cost)


# ──────────────────────────────────────────────────────────────────────────
# Output writers
# ──────────────────────────────────────────────────────────────────────────
def _sysml_str(s) -> str:
    return '"' + str(s).replace('"', "'") + '"'


def write_csv(rows_iter) -> tuple[int, list[dict], list[dict]]:
    """Stream every instance to CSV; return (count, top-N by hover endurance,
    top-N by endurance-per-dollar among R6-viable & flyable configs)."""
    top: list[dict] = []
    top_val: list[dict] = []
    count = 0
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        for r in rows_iter:
            w.writerow(r)
            count += 1
            top.append(r)
            if r["meets_r6_30min"] and r["flyable"]:
                top_val.append(r)
            if len(top) > SYSML_TOP_N * 4:  # trim periodically to bound memory
                top.sort(key=lambda x: x["max_flight_time_hover_min"], reverse=True)
                del top[SYSML_TOP_N:]
            if len(top_val) > SYSML_TOP_N * 4:
                top_val.sort(key=lambda x: x["endurance_per_1000usd"], reverse=True)
                del top_val[SYSML_TOP_N:]
    top.sort(key=lambda x: x["max_flight_time_hover_min"], reverse=True)
    top_val.sort(key=lambda x: x["endurance_per_1000usd"], reverse=True)
    return count, top[:SYSML_TOP_N], top_val[:SYSML_TOP_N]


def pick_baseline(top: list[dict]) -> Optional[dict]:
    flyable = [r for r in top if r["flyable"]]
    meets = [r for r in flyable if r["meets_r6_30min"]]
    pool = meets or flyable or top
    return pool[0] if pool else None


# SysML instance attributes (subset of CSV — full component identity + results).
_SYSML_ATTRS = [
    ("configId", "String", "config_id"), ("airframeId", "String", "airframe_id"),
    ("airframe", "String", "airframe"), ("battery", "String", "battery"),
    ("chemistry", "String", "chemistry"), ("cellCountS", "Integer", "cells_s"),
    ("capacity_mAh", "Real", "capacity_mah"), ("packVoltage_V", "Real", "pack_voltage_v"),
    ("batteryMass_g", "Real", "battery_mass_g"), ("usableEnergy_Wh", "Real", "usable_energy_wh"),
    ("thermalCam", "String", "thermal_id"), ("sbc", "String", "sbc_id"),
    ("dvr", "String", "dvr_id"), ("vtx", "String", "vtx_id"), ("fpv", "String", "fpv_id"),
    ("gps", "String", "gps_id"), ("rx", "String", "rx_id"),
    ("addedPayloadMass_g", "Real", "added_payload_mass_g"),
    ("totalPayloadPower_W", "Real", "total_payload_power_w"),
    ("allUpMass_g", "Real", "all_up_mass_g"), ("hoverPower_W", "Real", "hover_power_w"),
    ("maxFlightTimeHover_min", "Real", "max_flight_time_hover_min"),
    ("flightTimeCruise_min", "Real", "flight_time_cruise_min"),
    ("flightTimeHeadwind_min", "Real", "flight_time_headwind_min"),
    ("hoverThrottle_pct", "Real", "hover_throttle_pct"),
    ("meetsR6_30min", "Boolean", "meets_r6_30min"),
    ("meetsR8_60min", "Boolean", "meets_r8_60min"), ("flyable", "Boolean", "flyable"),
    ("droneCost_USD", "Real", "drone_cost_usd"), ("gcsCost_USD", "Real", "gcs_cost_usd"),
    ("totalSystemCost_USD", "Real", "total_system_cost_usd"),
    ("endurancePer1000USD", "Real", "endurance_per_1000usd"),
    ("meetsBudgetR4", "Boolean", "meets_budget_r4"),
]


def write_sysml(top, baseline, total, p, reps, rep_pow) -> None:
    L = ["// ════════════════════════════════════════════════════════════════════",
         "// AUTO-GENERATED by analysis/flight_time_model.py — DO NOT EDIT BY HAND.",
         "// Regenerate:  python analysis/flight_time_model.py",
         "//",
         f"// Holistic endurance sweep — {total} total buildable configurations.",
         f"// This instance table holds the BASELINE + top {len(top)} by max flight time;",
         "// the COMPLETE per-instance set (all components + battery attrs + flight",
         "// time) is in flight_time_results.csv.",
         f"// Model: rotors={p.n_rotors}, rho={p.air_density}, FoM={p.figure_of_merit}, "
         f"eta={p.drivetrain_eff}, Cd={p.drag_coeff}, cruise={p.cruise_speed_ms} m/s, "
         f"wind={p.wind_speed_ms} m/s.",
         "// Inclusion logic: airframe-bundled VTX/FPV/GPS/RX add power only (mass is in",
         "// the airframe weight); non-bundled peripherals add mass+power. FPV/GPS/RX held",
         f"// at lightest reps (fpv={reps['fpv'].ident}, gps={reps['gps'].ident}, "
         f"rx={reps['rx'].ident}); VTX swept when not bundled.",
         "// ════════════════════════════════════════════════════════════════════",
         "package FlightTimeAnalysis {",
         " private import ScalarValues::*;",
         "",
         " part def FlightTimeResult {"]
    for name, typ, _ in _SYSML_ATTRS:
        L.append(f"  attribute {name} : {typ};")
    L.append(" }")
    L.append("")

    def emit(prefix, r):
        L.append(f" part {prefix} : FlightTimeResult {{")
        for name, typ, key in _SYSML_ATTRS:
            v = r[key]
            if typ == "Boolean":
                lit = "true" if v else "false"
            elif typ == "Integer":
                lit = str(int(v))
            elif typ == "Real":
                lit = str(v)
            else:
                lit = _sysml_str(v)
            L.append(f"  :>> {name} = {lit};")
        L.append(" }")
        L.append("")

    if baseline:
        L.append(" // ── Recommended baseline (best flyable config meeting R6) ──")
        emit("baseline", baseline)
    L.append(f" // ── Top {len(top)} configurations by max flight time ──")
    for r in top:
        emit(f"inst_{r['config_id']}", r)
    L.append("}")
    OUT_SYSML.write_text("\n".join(L) + "\n", encoding="utf-8")


def write_markdown(top, baseline, total, n_af, n_bat, n_comp, p, reps, rep_pow,
                   bat_label: str = "battery packs", stats: Optional[dict] = None,
                   unfiltered: Optional[int] = None, gcs_cost: float = 0.0) -> None:
    L = ["# Flight-Time Analysis — Holistic Configuration Sweep", "",
         "**Auto-generated** by [`flight_time_model.py`](flight_time_model.py). "
         "Regenerate with `python analysis/flight_time_model.py`.", "",
         "Momentum-theory (actuator-disk) propulsion model + forward-flight "
         "parasitic drag. \"Max flight time\" = still-air hover endurance "
         "(R6 ≥ 30 min / R8 ≥ 60 min metric).", "",
         "## Sweep scope", "",
         f"- **{total:,} real configurations** = airframe × battery × SBC × "
         "VTX × thermal camera, fully crossed (respecting airframe component "
         "inclusion) and **filtered for interface compatibility**. The DVR is "
         "compatibility-gated, not crossed, and excluded from flight time (it is "
         "an earlier-stage part; the SBC records at the SBC stage).",
         f"- Flight-time drivers swept in full; sub-1 W peripherals held at lightest "
         f"representatives: FPV `{reps['fpv'].ident}`, GPS `{reps['gps'].ident}`, "
         f"RX `{reps['rx'].ident}`.",
         "- **Inclusion logic:** airframe-bundled VTX/FPV/GPS/RX contribute power "
         "only (their mass is already in the airframe's as-built weight); non-bundled "
         "peripherals contribute mass + power.",
         f"- Candidates: {n_af} airframes (with mass data), {bat_label}, "
         f"{n_comp} swept payload components.",
         (f"- **Cost (R4 ≤ $2,500):** each config's drone cost + a fixed "
          f"laptop-based GCS (ELRS USB dongle + analog VRX/capture + a Phase-1/backup "
          f"handheld radio = ${gcs_cost:,.0f}; the laptop is the ground station); bundled "
          f"VTX/FPV/GPS/RX add $0 (already in the airframe price); the DVR is "
          f"included (earlier-stage part)."),
         (f"- **Compatibility filtering** (declared in "
          f"`DroneSystemModel::Architecture::Compatibility`): {unfiltered:,} raw "
          f"pairings reduced to {total:,} real configs — pruned "
          f"{stats['voltage_pruned']:,} on battery↔airframe cell-count (P1, e.g. a "
          f"4S pack on a 6S-only frame) and {stats['video_pruned']:,} on "
          f"thermal↔DVR video format (V2, a thermal whose output no DVR can "
          f"record — CVBS via DVR1-6 or digital HDMI/USB via DVR7-9)."
          if stats and unfiltered is not None else
          "- Compatibility filtering: not applied (no cell/format data)."),
         "",
         "## Model assumptions", "",
         f"- Rotors **{p.n_rotors}** · ρ **{p.air_density} kg/m³** · FoM "
         f"**{p.figure_of_merit}** · η **{p.drivetrain_eff}** · C_d **{p.drag_coeff}** "
         f"· cruise **{p.cruise_speed_ms} m/s** (R2) · wind **{p.wind_speed_ms} m/s** (R7)",
         "",
         "> **Why cruise/wind endurance can exceed hover** — the multirotor *power "
         "bucket*: in slow forward flight the rotors gain translational lift, so "
         "induced power drops faster than parasitic drag rises. **Max FT** uses hover "
         "(conservative); *Cruise* (2.23 m/s) is the realistic still-air surveillance "
         "endurance; *Wind* is airspeed = cruise + 4.5 m/s (R7).", "",
         "> **Caveats** — first-order comparative estimates (FoM, η, C_d, frontal "
         "area, thrust lookup are assumptions; battery mass derived from chemistry "
         "specific energy). Airframes missing mass/wheelbase are skipped "
         "(MODEL_ISSUES.md §D). Full per-instance data: "
         "[`flight_time_results.csv`](flight_time_results.csv).", ""]
    if baseline:
        L += ["## Recommended baseline", "",
              f"**{baseline['airframe']}** ({baseline['airframe_id']}) + "
              f"**{baseline['battery']}**, SBC {baseline['sbc_id']}, VTX "
              f"{baseline['vtx_id']}, thermal {baseline['thermal_id']} → "
              f"**{baseline['max_flight_time_hover_min']} min** hover "
              f"({baseline['all_up_mass_g']} g AUW, "
              f"{baseline['hover_throttle_pct']}% throttle; drone "
              f"${baseline['drone_cost_usd']:.0f} / system "
              f"${baseline['total_system_cost_usd']:.0f} "
              f"{'≤' if baseline['meets_budget_r4'] else '>'} $2,500 R4).", ""]
    L += [f"## Top {len(top)} configurations (ranked by max flight time)", "",
          "| Cfg | Airframe | Battery | SBC | VTX | Therm | AUW g | Pld W | "
          "Max FT | Cruise | Wind | Thr% | Drone $ | Sys $ | R4 | R6 | R8 | Fly |",
          "|" + "|".join(["---"] * 18) + "|"]
    tick = lambda b: "✅" if b else "—"
    for r in top:
        L.append("| " + " | ".join(str(x) for x in [
            r["config_id"], f"{r['airframe']} ({r['airframe_id']})", r["battery"],
            r["sbc_id"], r["vtx_id"], r["thermal_id"], r["all_up_mass_g"],
            r["total_payload_power_w"], r["max_flight_time_hover_min"],
            r["flight_time_cruise_min"], r["flight_time_headwind_min"],
            r["hover_throttle_pct"],
            r["drone_cost_usd"], r["total_system_cost_usd"], tick(r["meets_budget_r4"]),
            tick(r["meets_r6_30min"]),
            tick(r["meets_r8_60min"]), tick(r["flyable"])]) + " |")
    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")


def write_value_markdown(top_val, gcs_cost: float, gcs_parts: Optional[dict] = None) -> None:
    """Endurance-per-dollar ranking with the FULL per-instance bill of materials
    (every component by its actual product name)."""
    gcs_parts = gcs_parts or {}
    radio = gcs_parts.get("radio") or "cheapest integrated handheld radio"
    dongle = gcs_parts.get("dongle") or "cheapest ELRS USB dongle"
    vrx = gcs_parts.get("vrx") or "cheapest diversity VRX"
    L = ["# Flight-Time Analysis — Best Value (Endurance per Dollar)", "",
         "**Auto-generated** by [`flight_time_model.py`](flight_time_model.py). "
         "Regenerate with `python analysis/flight_time_model.py`.", "",
         "Ranked by **endurance-per-dollar** = max hover flight time (min) ÷ total "
         "system cost (USD) × 1000 — i.e. **minutes of hover per $1,000**. Only "
         "configs meeting R6 (≥ 30 min) and the thrust/feasibility check are ranked. "
         "Each entry lists the **complete system bill of materials** by actual product "
         "name. Peripherals shown as *included with airframe* are bundled in a BNF/PNP "
         "airframe (no separate part or cost); the DVR is an earlier-stage recorder "
         "(counted in cost, excluded from flight time).", "",
         "**Ground control station** (fixed — same on every instance; the laptop *is* "
         "the GCS and is existing kit, not costed):",
         f"- Control + telemetry, primary: **{dongle}** (${gcs_parts.get('dongle_cost', 0):.0f})",
         f"- Live video receiver: **{vrx}** (${gcs_parts.get('vrx_cost', 0):.0f})",
         f"- Manual control, Phase-1 / backup: **{radio}** (${gcs_parts.get('radio_cost', 0):.0f})",
         f"- **GCS subtotal: ${gcs_cost:,.0f}**",
         "",
         "Full per-config dataset: [`flight_time_results.csv`](flight_time_results.csv); "
         "endurance-ranked view: [`flight_time_results.md`](flight_time_results.md).", "",
         f"## Top {len(top_val)} by endurance-per-dollar", ""]

    def comp(name, ident) -> str:
        if str(ident).lower() == "included" or str(name).lower().startswith("bundled"):
            return "*included with airframe*"
        return f"{name} (`{ident}`)"

    for i, r in enumerate(top_val, 1):
        budget = "✅ R4" if r["meets_budget_r4"] else "⚠️ over R4"
        L.append(
            f"### {i}. {r['endurance_per_1000usd']} min/$1k — "
            f"{r['max_flight_time_hover_min']} min hover · "
            f"drone ${r['drone_cost_usd']:.0f} / system ${r['total_system_cost_usd']:.0f} · {budget}")
        L.append(f"- Airframe **{r['airframe']}** (`{r['airframe_id']}`) · "
                 f"Battery **{r['battery']}**")
        L.append(f"- Thermal camera: {comp(r['thermal_name'], r['thermal_id'])} · "
                 f"SBC: {comp(r['sbc_name'], r['sbc_id'])} · "
                 f"DVR: {comp(r['dvr_name'], r['dvr_id'])}")
        L.append(f"- VTX: {comp(r['vtx_name'], r['vtx_id'])} · "
                 f"FPV cam: {comp(r['fpv_name'], r['fpv_id'])} · "
                 f"GPS: {comp(r['gps_name'], r['gps_id'])} · "
                 f"RX: {comp(r['rx_name'], r['rx_id'])}")
        L.append("")
    OUT_VALUE_MD.write_text("\n".join(L) + "\n", encoding="utf-8")


def write_chart() -> bool:
    """Cost-vs-flight-time scatter of every real config (reads the CSV).

    Returns True if the PNG was written, False if matplotlib is unavailable.
    """
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return False
    import collections
    rows = list(csv.DictReader(OUT_CSV.open(encoding="utf-8")))
    if not rows:
        return False
    by_af: dict = collections.defaultdict(lambda: ([], []))
    for r in rows:
        xs, ys = by_af[r["airframe_id"]]
        xs.append(float(r["total_system_cost_usd"]))
        ys.append(float(r["max_flight_time_hover_min"]))

    fig, ax = plt.subplots(figsize=(10.0, 6.5))
    cmap = plt.get_cmap("tab20")
    for i, af in enumerate(sorted(by_af)):
        xs, ys = by_af[af]
        ax.scatter(xs, ys, s=10, color=cmap(i % 20), label=af, alpha=0.55, edgecolors="none")

    # Requirement reference lines
    ax.axhline(30.0, color="red", ls="--", lw=1.0)
    ax.text(ax.get_xlim()[1], 30.4, "R6  30 min", color="red", fontsize=8, ha="right", va="bottom")
    ax.axhline(60.0, color="darkorange", ls="--", lw=1.0)
    ax.text(ax.get_xlim()[1], 60.4, "R8  60 min", color="darkorange", fontsize=8, ha="right", va="bottom")
    ax.axvline(2500.0, color="green", ls="--", lw=1.0)
    ax.text(2500.0, ax.get_ylim()[0], " R4  $2,500", color="green", fontsize=8, ha="left", va="bottom")

    ax.set_xlabel("Total system cost (USD)")
    ax.set_ylabel("Max hover flight time (min)")
    ax.set_title("Cost vs. flight time — all real (compatibility-filtered) configurations")
    ax.grid(True, alpha=0.3)
    ax.legend(title="Airframe", fontsize=7, ncol=2, loc="lower right", framealpha=0.9)
    fig.tight_layout()
    fig.savefig(OUT_CHART, dpi=130)
    plt.close(fig)
    return True


# ──────────────────────────────────────────────────────────────────────────
def main() -> None:
    p = PhysicsParams()
    airframes, components, real_batteries, gcs_cost, gcs_parts = load_model()
    if real_batteries:
        batteries = real_batteries
        bat_label = f"{len(batteries)} real battery candidates"
    else:
        batteries = generate_generic_batteries()
        bat_label = f"{len(batteries)} generic battery packs (fallback)"
    reps = {cat: lightest(components[cat]) for cat in ("vtx", "fpv", "gps", "rx")}
    rep_pow = {cat: representative_power(components[cat]) for cat in ("vtx", "fpv", "gps", "rx")}

    stats = {"voltage_pruned": 0, "video_pruned": 0}
    total, top, top_val = write_csv(iter_configs(airframes, components, batteries, p, stats, gcs_cost))
    unfiltered = total + stats["voltage_pruned"] + stats["video_pruned"]
    baseline = pick_baseline(top)
    n_comp = sum(len(components[c]) for c in ("thermal", "sbc", "dvr", "vtx", "fpv", "gps", "rx"))
    write_sysml(top, baseline, total, p, reps, rep_pow)
    write_markdown(top, baseline, total, len(airframes), len(batteries), n_comp, p, reps, rep_pow,
                   bat_label, stats, unfiltered, gcs_cost)
    write_value_markdown(top_val, gcs_cost, gcs_parts)
    chart_ok = write_chart()

    print(f"Airframes (with mass) : {len(airframes)}")
    print(f"Batteries             : {bat_label}")
    for c in ("thermal", "sbc", "dvr", "vtx", "fpv", "gps", "rx"):
        print(f"  {c:8s} candidates  : {len(components[c])}")
    print(f"Peripheral reps       : fpv={reps['fpv'].ident}, gps={reps['gps'].ident}, "
          f"rx={reps['rx'].ident}  (vtx swept when not bundled)")
    print(f"Unfiltered pairings   : {unfiltered:,}")
    print(f"  pruned voltage (P1) : {stats['voltage_pruned']:,}  (battery cells vs airframe window)")
    print(f"  pruned video   (V2) : {stats['video_pruned']:,}  (thermal output vs CVBS DVR)")
    print(f"REAL configurations   : {total:,}")
    print(f"GCS (fixed) cost      : ${gcs_cost:,.0f}  (laptop dongle + VRX + backup radio)")
    if baseline:
        print(f"Recommended baseline  : {baseline['airframe']} ({baseline['airframe_id']}) + "
              f"{baseline['battery']} -> {baseline['max_flight_time_hover_min']} min hover, "
              f"drone ${baseline['drone_cost_usd']:.0f} / system ${baseline['total_system_cost_usd']:.0f}")
    print(f"Wrote: {OUT_CSV.name} (all {total:,}), {OUT_SYSML.name} (top {len(top)}), {OUT_MD.name}")
    print(f"       {OUT_VALUE_MD.name} (value top {len(top_val)})"
          + (f", {OUT_CHART.name}" if chart_ok else "  [chart skipped: matplotlib unavailable]"))


if __name__ == "__main__":
    main()
