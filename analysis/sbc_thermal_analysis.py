"""SBC (NanoPi M5 / RK3576) thermal analysis — is active cooling actually required?

Resolves the R4_SBC_TEMP conflict surfaced by the VCRM buildout: the requirement
says the SBC "shall operate ... without active cooling", the selection rationale
in SELECTED_COMPONENTS.md says "<=10 W passive", but the Phase-2 BOM carries a
30 mm fan on the printed SBC deck. One of the three has to give.

Model — a steady-state resistance network from SoC junction to ambient air:

    T_j = T_amb + (Q_soc + Q_solar) * (R_jc + R_tim + R_sa)

  R_jc   junction-to-case, FCBGA package                         [K/W]
  R_tim  case-to-heatsink through the thermal pad                [K/W]
  R_sa   heatsink-to-air = 1 / (h_conv * A_eff) in parallel with radiation

Convection uses standard flat-plate correlations — natural convection from a
horizontal heated plate (Rayleigh) and laminar forced convection over the fin
length (Nu = 0.664 Re^0.5 Pr^1/3) — with the fin area derated for boundary-layer
merging, more severely in still air than in forced flow.

The airflow term is the crux. This is a multirotor: the SBC sits on the top deck,
INSIDE the hub region bounded by the four rotor disks, so in flight it sits in the
rotor INFLOW field. Induced velocity comes from the same momentum/actuator-disk
theory flight_time_model.py already uses for endurance:

    v_i = sqrt(T_rotor / (2 * rho * A_disk))

Only a fraction of v_i reaches the hub (the deck is inboard of the disks), so the
in-flight design point is deliberately taken at the low end of that fraction.

Because the mission is DAYTIME and the board is the topmost item on the airframe,
direct solar gain on the heatsink is carried as a real heat input — for a black
anodised sink it is comparable to the SoC's own dissipation.

No published thermal test data exists for the M5, so this is a first-principles
bound, not a measurement. VB-03 (bench thermal soak) is the closing evidence.

Writes analysis/sbc_thermal_analysis.md.  Run: python analysis/sbc_thermal_analysis.py
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

OUT_MD = Path(__file__).resolve().parent / "sbc_thermal_analysis.md"

# --- Limits (sourced, not assumed) -----------------------------------------
T_THROTTLE_C = 85.0    # Rockchip thermal-zone passive DVFS trip point
T_AMB_SPEC_C = 70.0    # FriendlyElec NanoPi M5 max ambient operating spec
DESIGN_MARGIN_C = 10.0 # required headroom below the throttle trip

# --- Heat load (candidates.sysml SBC3 + R4_SBC_PWR) ------------------------
# PROVENANCE WARNING: 10 W is the R4_SBC_PWR *requirement cap*, not a measured or
# manufacturer-published figure. FriendlyElec publishes no power-consumption data
# for the M5 at all (only the 6-20 V input range and 0-70 C ambient). Rockchip
# quotes RK3576 TDP "<15 W" (SoC only, a ceiling); third-party comparisons put
# the RK3576 20-40% below the RK3588's ~12 W full-load figure, i.e. ~7-10 W. The
# trade study's "~6-10 W (estimate)" is therefore reasonable and 10 W is a
# conservative upper bound. P_BOARD_CREDIBLE_W sweeps the real range (§7c).
P_BOARD_MAX_W = 10.0   # R4_SBC_PWR cap == SBC3 `power` (conservative bound)
P_BOARD_IDLE_W = 4.0   # SBC3 `idlePower`
P_BOARD_CREDIBLE_W = [5.0, 6.0, 7.0, 8.0, 9.0, 10.0]

# For an SBC, essentially ALL electrical input power becomes heat — there is no
# mechanical work and radiated RF/optical is negligible. The only input power
# that does NOT become heat on the board is what is exported through the ports:
# here the T13 thermal camera is USB-bus-powered at ~0.8 W. So board heat is
# (P_input - P_USB_EXPORT). Measuring input power therefore does bound the heat
# load directly — but NOT the split below, which is what the heatsink actually sees.
P_USB_EXPORT_W = 0.8   # T13 draws from the M5's USB port (candidates.sysml T13.power)

SOC_FRACTION = 0.70    # share of board heat dissipated in the SoC package itself;
                       # the rest (DDR, PMIC losses, 2x GbE PHY, USB) spreads into
                       # the PCB and is rejected by the board, not the sink. A
                       # wall-plug power measurement CANNOT resolve this split —
                       # only an on-die temperature reading can. See §7d.

# --- Conduction path -------------------------------------------------------
R_JC_KW = 1.5          # junction-to-case, FCBGA with integrated spreader
R_TIM_KW = 1.0         # thermal pad, ~15x15 mm die footprint

# --- Air properties at ~40 C ----------------------------------------------
K_AIR = 0.0271         # W/m.K
NU_AIR = 1.70e-5       # m^2/s
PR_AIR = 0.705
RHO_AIR = 1.225        # kg/m^3 (sea level, matches PhysicsParams in the sweep)
ALPHA_AIR = 2.40e-5    # m^2/s
SIGMA = 5.670e-8       # Stefan-Boltzmann

# --- Airframe (AF3a Chimera9 ECO, reference config C000009) ----------------
AUW_KG = 1.7497        # all_up_mass_g from flight_time_results.csv
N_ROTORS = 4
PROP_DIAM_M = 9.0 * 0.0254
# The SBC (90x62 mm) is centred inside the hub; the rotor disks start ~88 mm out
# from centre (405 mm wheelbase, 114 mm prop radius), so the deck never sees the
# full disk inflow. Sweep the plausible band and design to the bottom of it.
HUB_INFLOW_FRACTION_LOW = 0.15
HUB_INFLOW_FRACTION_HIGH = 0.40

# --- Solar (daytime mission, board is the topmost item) --------------------
SOLAR_IRRADIANCE_W_M2 = 1000.0   # clear-sky peak, normal incidence
ABSORPTIVITY_BLACK = 0.95        # black anodised aluminium
ABSORPTIVITY_LIGHT = 0.30        # bare/clear-anodised or light-painted
EMISSIVITY_BLACK = 0.90
EMISSIVITY_LIGHT = 0.85

# --- Fin-area derating -----------------------------------------------------
# Closely-spaced fins on a horizontal, upward-facing sink lose a lot of their
# geometric area in still air (merged boundary layers, no chimney draw). Forced
# flow through the channels recovers most of it.
DERATE_NATURAL = 0.60
DERATE_FORCED = 0.90


@dataclass(frozen=True)
class HeatSink:
    """A finned aluminium heatsink; dimensions in metres."""
    label: str
    base_l: float
    base_w: float
    fin_h: float
    fin_t: float
    n_fins: int
    k_al: float = 200.0

    @property
    def fin_gap(self) -> float:
        return (self.base_w - self.n_fins * self.fin_t) / (self.n_fins - 1)

    @property
    def area_geometric(self) -> float:
        """Total wetted area: fin flanks + exposed base + sink sides [m^2]."""
        fins = self.n_fins * 2.0 * self.fin_h * self.base_l
        base = self.base_l * self.base_w - self.n_fins * self.fin_t * self.base_l
        sides = 2.0 * self.base_l * self.fin_h
        return fins + base + sides

    @property
    def area_projected(self) -> float:
        """Plan-view footprint — what sees the sun and radiates to the sky."""
        return self.base_l * self.base_w

    def fin_efficiency(self, h: float) -> float:
        m = math.sqrt(2.0 * h / (self.k_al * self.fin_t))
        mL = m * self.fin_h
        return math.tanh(mL) / mL if mL > 0 else 1.0


# --- Mountable footprint (measured from the FriendlyElec layout drawing) -----
# The board is NOT a flat surface. Measured off the official LPDDR4X layout at
# 5.0 px/mm, from the PCB top edge:
#   0.0 - 18 mm   2x RJ45 / 2x USB-A / HDMI  <- TALL (~14-20 mm), hard keep-out
#   21 - 28 mm    RTL8211F Ethernet PHYs     <- low-profile QFN
#   32 - 49 mm    RK3576 SoC (~16x16 mm)     <- the only thermally relevant contact
#   55 - 62 mm    30-pin GPIO header (~8.5 mm)
# and across the board from the left edge: buttons to ~5 mm, LPDDR4X 11-23 mm,
# SoC 29-46 mm, M.2 E-Key socket from ~53 mm, microSD from ~76 mm.
#
# So a heatsink that sits FLUSH and actually touches the SoC is bounded to roughly
# 47 x 35 mm — about 37% of the 80x55 mm footprint an earlier revision of this
# analysis assumed. A larger flat block cannot work at any thickness: it would
# rest on the 14-20 mm connector row with a ~15 mm air gap over the SoC, i.e. no
# thermal contact at all. Lost base area is recovered through FIN HEIGHT instead.
CLEAR_L_MM, CLEAR_W_MM = 47.0, 35.0

# Option A: a small sink sized to the SoC only — what ships in generic SBC kits.
# Option B: the largest sink that actually mounts, area recovered via tall fins.
SINK_SMALL = HeatSink("40x40x10 mm (SoC-sized kit part)", 0.040, 0.040, 0.010, 0.0010, 12)
SINK_LARGE = HeatSink("47x35x25 mm (fits M5 clear area)", 0.047, 0.035, 0.025, 0.0012, 9)


def induced_velocity(auw_kg: float = AUW_KG) -> float:
    """Hover induced velocity at the rotor disk [m/s] — actuator-disk theory."""
    thrust_per_rotor = auw_kg * 9.81 / N_ROTORS
    disk_area = math.pi * (PROP_DIAM_M / 2.0) ** 2
    return math.sqrt(thrust_per_rotor / (2.0 * RHO_AIR * disk_area))


def h_natural(delta_t: float, length: float) -> float:
    """Natural convection from a horizontal heated plate, facing up [W/m^2.K]."""
    if delta_t <= 0:
        return 0.0
    beta = 1.0 / 313.0
    ra = (9.81 * beta * delta_t * length ** 3) / (NU_AIR * ALPHA_AIR)
    nu = 0.54 * ra ** 0.25 if ra < 1e7 else 0.15 * ra ** (1.0 / 3.0)
    return nu * K_AIR / length


def h_forced(velocity: float, length: float) -> float:
    """Laminar forced convection along the fin channel [W/m^2.K]."""
    if velocity <= 0:
        return 0.0
    re = velocity * length / NU_AIR
    nu = 0.664 * math.sqrt(re) * PR_AIR ** (1.0 / 3.0)
    return nu * K_AIR / length


def solve_sink_temp(sink: HeatSink, q_soc: float, t_amb_c: float,
                    velocity: float, absorptivity: float, emissivity: float,
                    solar: bool) -> tuple[float, float, float]:
    """Iterate to the steady-state sink temperature.

    Returns (T_sink_C, h_used, Q_solar_W). Natural convection depends on the
    very delta-T it produces, so this fixed-points rather than solving directly.
    """
    q_solar = (absorptivity * SOLAR_IRRADIANCE_W_M2 * sink.area_projected
               if solar else 0.0)
    q_total = q_soc + q_solar

    t_sink = t_amb_c + 10.0
    h_used = 0.0
    for _ in range(200):
        delta_t = max(t_sink - t_amb_c, 0.01)
        if velocity > 0:
            h_used = h_forced(velocity, sink.base_l)
            area = sink.area_geometric * DERATE_FORCED
        else:
            h_used = h_natural(delta_t, sink.base_l)
            area = sink.area_geometric * DERATE_NATURAL
        area *= sink.fin_efficiency(h_used)

        q_conv_coeff = h_used * area
        t_k, ta_k = t_sink + 273.15, t_amb_c + 273.15
        q_rad = emissivity * SIGMA * sink.area_projected * (t_k ** 4 - ta_k ** 4)

        # Newton-ish relaxation on the convective balance, radiation as a bias.
        t_new = t_amb_c + (q_total - q_rad) / q_conv_coeff if q_conv_coeff > 0 else t_sink
        t_sink += 0.35 * (t_new - t_sink)
    return t_sink, h_used, q_solar


def junction_temp(sink: HeatSink, p_board: float, t_amb_c: float, velocity: float,
                  absorptivity: float = ABSORPTIVITY_BLACK,
                  emissivity: float = EMISSIVITY_BLACK,
                  solar: bool = False,
                  soc_fraction: float = SOC_FRACTION) -> dict:
    q_soc = p_board * soc_fraction
    t_sink, h_used, q_solar = solve_sink_temp(
        sink, q_soc, t_amb_c, velocity, absorptivity, emissivity, solar)
    t_junction = t_sink + q_soc * (R_JC_KW + R_TIM_KW)
    return {
        "t_sink_c": t_sink,
        "t_junction_c": t_junction,
        "h": h_used,
        "q_soc": q_soc,
        "q_solar": q_solar,
        "margin_c": T_THROTTLE_C - t_junction,
        "pass": t_junction <= (T_THROTTLE_C - DESIGN_MARGIN_C),
    }


def min_airflow_for_pass(sink: HeatSink, p_board: float, t_amb_c: float,
                         solar: bool, absorptivity: float = ABSORPTIVITY_BLACK,
                         emissivity: float = EMISSIVITY_BLACK) -> float | None:
    """Lowest airflow [m/s] meeting the throttle trip minus design margin."""
    for i in range(0, 1201):
        v = i / 100.0
        r = junction_temp(sink, p_board, t_amb_c, v, absorptivity, emissivity, solar)
        if r["pass"]:
            return v
    return None


def main() -> None:
    v_i = induced_velocity()
    v_hub_low = v_i * HUB_INFLOW_FRACTION_LOW
    v_hub_high = v_i * HUB_INFLOW_FRACTION_HIGH

    L: list[str] = []
    add = L.append
    add("# SBC Thermal Analysis — is active cooling required?\n")
    add("**Subject:** `SBC3` NanoPi M5 (Rockchip RK3576, 4 GB) on the Phase-2 printed deck  ")
    add("**Question:** `R4_SBC_TEMP` requires operation *\"without active cooling\"*, but the ")
    add("Phase-2 BOM carries a 30 mm fan. Is the fan actually needed?  ")
    add("**Generated by** `analysis/sbc_thermal_analysis.py` — rerun to regenerate.\n")

    # --- Verdict (lead with the answer) ------------------------------------
    r_flight_low = junction_temp(SINK_LARGE, P_BOARD_MAX_W, 35.0, v_hub_low, solar=True)
    r_flight_shade = junction_temp(SINK_LARGE, P_BOARD_MAX_W, 35.0, v_hub_low,
                                   ABSORPTIVITY_LIGHT, EMISSIVITY_LIGHT, solar=True)
    r_pad = junction_temp(SINK_LARGE, P_BOARD_MAX_W, 35.0, 0.0, solar=True)
    r_small = junction_temp(SINK_SMALL, P_BOARD_MAX_W, 35.0, v_hub_high, solar=True)
    v_min_sun = min_airflow_for_pass(SINK_LARGE, P_BOARD_MAX_W, 35.0, solar=True)
    v_min_shade = min_airflow_for_pass(SINK_LARGE, P_BOARD_MAX_W, 35.0, solar=False)

    add("---\n")
    add("## Verdict\n")
    add("**The fan is needed — but not to fly.** The binding case is the aircraft sitting still ")
    add("at full inference load, not the aircraft in the air.\n")
    add(f"1. **In flight, passive cooling works.** Rotor inflow gives an estimated ")
    add(f"   **{v_hub_low:.2f}–{v_hub_high:.2f} m/s** over the deck; a full-board sink needs ")
    add(f"   **{v_min_shade:.2f} m/s** shaded or **{v_min_sun:.2f} m/s** in direct sun. Junction lands at ")
    add(f"   **{r_flight_low['t_junction_c']:.0f} °C** at the conservative low end ")
    add(f"   ({r_flight_shade['t_junction_c']:.0f} °C with a light-finish sink) against an 85 °C trip.")
    add(f"2. **On the ground at full load, passive fails outright** — **{r_pad['t_junction_c']:.0f} °C** on a ")
    add("   35 °C pad in sun, and §7 shows no plausible model error or airflow assumption rescues it. ")
    add("   That is exactly the condition of bench development, model loading, pre-flight and the ")
    add("   `VB-02` / `VB-03` acceptance tests.")
    add(f"3. **The heatsink matters more than the fan.** The SoC-sized 40×40 sink fails even at the ")
    add(f"   *high* propwash estimate (**{r_small['t_junction_c']:.0f} °C**); the full-board sink passes at the low ")
    add("   one. A light finish instead of black anodising is worth ~13 °C on the pad, for free.\n")
    add("### Recommended disposition\n")
    add("| # | Action | Rationale |")
    add("|---|---|---|")
    add("| 1 | **Keep the 30 mm fan**, but reclassify it as *ground/bench thermal support* — not a "
        "flight-critical item | Ground full-load operation needs it; flight does not. Its failure "
        "in flight is then benign by design, which is what the original 'no active cooling' intent "
        "was protecting |")
    add("| 2 | **Specify a full-board heatsink (~80×55 mm) with a light or clear finish** — not the "
        "SoC-sized sink, not black anodised | Single highest-value change, and it is free. The "
        "small sink fails every case |")
    add("| 3 | **Restate `R4_SBC_TEMP`** | *'Without active cooling'* is not achievable at 10 W "
        "sustained, and the requirement never defines the environmental range it refers to |")
    add("| 4 | **Gate sustained full-load inference to in-flight phases** | Idle (4 W) is comfortable "
        "passively; the mission app already starts inference at takeoff |")
    add("")
    add("Proposed requirement text:\n")
    add("> The SBC shall operate without thermal throttling at sustained maximum inference load ")
    add("> (10 W board power) over an ambient range of 0–40 °C, using passive cooling plus ")
    add("> rotor-induced airflow, in all flight phases. Forced-air cooling is permitted for ground ")
    add("> operation and shall not be flight-critical: loss of the cooling fan shall not prevent ")
    add("> compliance in any flight phase.\n")
    add("This keeps the original intent — *never depend on a fan to stay airborne* — while matching ")
    add("what the physics allows. It is testable, and `VB-03` closes it.\n")
    add("---\n")

    add("## 1. Limits and heat load\n")
    add("| Parameter | Value | Source |")
    add("|---|--:|---|")
    add(f"| SoC throttle trip (DVFS passive) | {T_THROTTLE_C:.0f} °C | Rockchip thermal-zone config |")
    add(f"| Required design margin below trip | {DESIGN_MARGIN_C:.0f} °C | this analysis |")
    add(f"| Board max ambient (spec) | {T_AMB_SPEC_C:.0f} °C | FriendlyElec NanoPi M5 |")
    add(f"| Board power, full inference | {P_BOARD_MAX_W:.1f} W | `R4_SBC_PWR` cap / `SBC3.power` |")
    add(f"| Board power, idle | {P_BOARD_IDLE_W:.1f} W | `SBC3.idlePower` |")
    add(f"| Fraction dissipated in the SoC | {SOC_FRACTION:.0%} | assumed; rest is DDR/PMIC/PHY on the PCB |")
    add(f"| Conduction path R_jc + R_tim | {R_JC_KW + R_TIM_KW:.1f} K/W | FCBGA + thermal pad |")
    add("")

    add("## 2. In-flight airflow (actuator-disk theory)\n")
    add(f"Reference config C000009 — AF3a Chimera9 ECO, AUW **{AUW_KG*1000:.0f} g**, 9\" props, ")
    add("hover throttle 14.9 %. Same momentum theory the endurance sweep uses:\n")
    add(f"- Thrust per rotor: **{AUW_KG*9.81/N_ROTORS:.2f} N**")
    add(f"- Induced velocity at the disk: **v_i = {v_i:.2f} m/s**")
    add(f"- Fully-contracted wake: {2*v_i:.2f} m/s\n")
    add("The 90 × 62 mm board sits centred on the top deck, spanning ~55 mm from centre at its ")
    add("corners. The rotor disks begin ~88 mm out (405 mm wheelbase, 114 mm prop radius), so the ")
    add("SBC sits **inboard of the disks, in the inflow field feeding them** — not in the wake. ")
    add(f"Taking {HUB_INFLOW_FRACTION_LOW:.0%}–{HUB_INFLOW_FRACTION_HIGH:.0%} of v_i at the hub gives ")
    add(f"**{v_hub_low:.2f}–{v_hub_high:.2f} m/s** over the sink. The analysis designs to the ")
    add(f"bottom of that band ({v_hub_low:.2f} m/s) and reports sensitivity below.\n")
    add("> The board is the topmost item on the airframe (raised tier above the top-mounted ")
    add("> battery), which maximises its exposure to that inflow — and to the sun.\n")

    sinks = [SINK_SMALL, SINK_LARGE]
    add("## 3. What can physically mount (measured from the layout drawing)\n")
    add("The M5 is not a flat surface, and this constrains the sink harder than the thermals do. ")
    add("Measured off the official LPDDR4X layout at 5.0 px/mm, from the PCB top edge:\n")
    add("| Band (from top edge) | Occupant | Height |")
    add("|---|---|---|")
    add("| 0 – 18 mm | 2× RJ45, 2× USB-A, HDMI | **~14–20 mm — hard keep-out** |")
    add("| 21 – 28 mm | RTL8211F Ethernet PHYs | low-profile QFN |")
    add("| 32 – 49 mm | **RK3576 SoC (~16×16 mm)** | ~1.5 mm — the only contact that matters |")
    add("| 55 – 62 mm | 30-pin GPIO header | ~8.5 mm |")
    add("")
    add("Across the board from the left edge: buttons to ~5 mm, LPDDR4X 11–23 mm, SoC 29–46 mm, ")
    add("M.2 E-Key socket from ~53 mm, microSD from ~76 mm.\n")
    add(f"**Usable flush-mount window: ~{CLEAR_L_MM:.0f} × {CLEAR_W_MM:.0f} mm** — it clears the connector row, stops ")
    add("short of the M.2 E-Key, and covers both the SoC and the LPDDR4X.\n")
    add("> **A large flat block cannot work at any thickness.** Laid on the board it rests on the ")
    add("> 14–20 mm connector row, leaving a ~15 mm air gap over the SoC — no thermal contact. The ")
    add("> board's mounting holes (~83 × 42 mm spacing) match no COTS heatsink pattern either, so ")
    add("> attachment is by thermal adhesive pad onto the SoC package.\n")
    add(f"This window is only ~37 % of the 80 × 55 mm footprint assumed in an earlier revision of this ")
    add("analysis. Lost base area has to be recovered through **fin height**, not footprint.\n")
    add("### Sinks modelled\n")
    add("| Sink | Wetted area | Footprint | Fin gap | Est. mass |")
    add("|---|--:|--:|--:|--:|")
    for s in sinks:
        vol = s.base_l * s.base_w * 0.003 + s.n_fins * s.fin_h * s.fin_t * s.base_l
        add(f"| {s.label} | {s.area_geometric*1e4:.0f} cm² | {s.area_projected*1e4:.0f} cm² "
            f"| {s.fin_gap*1000:.1f} mm | ~{vol*2700*1000:.0f} g |")
    add("")
    add("Fin-height trade within the fixed 47 × 35 mm window (full load, 35 °C, in sun):\n")
    add("| Fin height | Wetted area | Est. mass | Flight (low propwash) | Flight, light finish | Pad, still air |")
    add("|--:|--:|--:|--:|--:|--:|")
    for fh in [0.015, 0.020, 0.025, 0.030, 0.035]:
        s = HeatSink(f"{fh*1000:.0f}mm", CLEAR_L_MM/1000, CLEAR_W_MM/1000, fh, 0.0012, 9)
        vol = s.base_l * s.base_w * 0.003 + s.n_fins * s.fin_h * s.fin_t * s.base_l
        rf = junction_temp(s, P_BOARD_MAX_W, 35.0, v_hub_low, solar=True)
        rl = junction_temp(s, P_BOARD_MAX_W, 35.0, v_hub_low,
                           ABSORPTIVITY_LIGHT, EMISSIVITY_LIGHT, solar=True)
        rp = junction_temp(s, P_BOARD_MAX_W, 35.0, 0.0, solar=True)
        mk = lambda r: "✅" if r["pass"] else ("⚠️" if r["t_junction_c"] <= T_THROTTLE_C else "❌")
        add(f"| {fh*1000:.0f} mm | {s.area_geometric*1e4:.0f} cm² | ~{vol*2700*1000:.0f} g "
            f"| {rf['t_junction_c']:.0f} °C {mk(rf)} | {rl['t_junction_c']:.0f} °C {mk(rl)} "
            f"| {rp['t_junction_c']:.0f} °C {mk(rp)} |")
    add("")
    add("**25 mm of fin is the floor** for a passing flight case; 30 mm buys comfortable margin. ")
    add("Below 20 mm the flight case fails even before considering model error. No fin height ")
    add("rescues still-air ground operation.\n")

    # --- Case matrix --------------------------------------------------------
    add("## 4. Case matrix\n")
    add("`T_j` = SoC junction temperature. **PASS** = at least "
        f"{DESIGN_MARGIN_C:.0f} °C below the {T_THROTTLE_C:.0f} °C throttle trip.\n")

    cases = [
        ("Bench, still air, idle", P_BOARD_IDLE_W, 25.0, 0.0, False),
        ("Bench, still air, FULL load", P_BOARD_MAX_W, 25.0, 0.0, False),
        ("Pad, still air, idle, hot day + sun", P_BOARD_IDLE_W, 35.0, 0.0, True),
        ("Pad, still air, FULL load, hot day + sun", P_BOARD_MAX_W, 35.0, 0.0, True),
        ("Flight, propwash (low), FULL load, hot day + sun", P_BOARD_MAX_W, 35.0, v_hub_low, True),
        ("Flight, propwash (high), FULL load, hot day + sun", P_BOARD_MAX_W, 35.0, v_hub_high, True),
        ("Flight, propwash (low), FULL load, 40 °C + sun", P_BOARD_MAX_W, 40.0, v_hub_low, True),
        ("Flight, propwash (low), FULL load, 0 °C, no sun", P_BOARD_MAX_W, 0.0, v_hub_low, False),
    ]
    for sink in sinks:
        add(f"\n### {sink.label}\n")
        add("| Case | Load | Ambient | Air | Q_solar | T_sink | **T_j** | Margin | |")
        add("|---|--:|--:|--:|--:|--:|--:|--:|:--:|")
        for label, p, ta, v, sun in cases:
            r = junction_temp(sink, p, ta, v, solar=sun)
            verdict = "✅" if r["pass"] else ("⚠️" if r["t_junction_c"] <= T_THROTTLE_C else "❌")
            add(f"| {label} | {p:.0f} W | {ta:.0f} °C | {v:.2f} m/s | {r['q_solar']:.1f} W | "
                f"{r['t_sink_c']:.0f} °C | **{r['t_junction_c']:.0f} °C** | {r['margin_c']:+.0f} °C | {verdict} |")
    add("")

    # --- Airflow sensitivity ------------------------------------------------
    add("## 5. How much airflow is actually needed?\n")
    add("Full inference load, 35 °C ambient, in sun — sweeping airflow over the sink:\n")
    add("| Airflow | " + " | ".join(s.label for s in sinks) + " |")
    add("|--:|" + "--:|" * len(sinks))
    for v in [0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 5.0]:
        cells = []
        for s in sinks:
            r = junction_temp(s, P_BOARD_MAX_W, 35.0, v, solar=True)
            mark = "✅" if r["pass"] else ("⚠️" if r["t_junction_c"] <= T_THROTTLE_C else "❌")
            cells.append(f"{r['t_junction_c']:.0f} °C {mark}")
        add(f"| {v:.2f} m/s | " + " | ".join(cells) + " |")
    add("")
    for s in sinks:
        v_min = min_airflow_for_pass(s, P_BOARD_MAX_W, 35.0, solar=True)
        v_min_nosun = min_airflow_for_pass(s, P_BOARD_MAX_W, 35.0, solar=False)
        txt_sun = f"**{v_min:.2f} m/s**" if v_min is not None else "**not achievable**"
        txt_no = f"**{v_min_nosun:.2f} m/s**" if v_min_nosun is not None else "**not achievable**"
        add(f"- **{s.label}** — minimum airflow to pass: {txt_sun} in sun, {txt_no} shaded.")
    add(f"\nAvailable in flight at the hub: **{v_hub_low:.2f}–{v_hub_high:.2f} m/s**.\n")

    # --- Solar finish -------------------------------------------------------
    add("## 6. Heatsink finish (daytime mission, board on top)\n")
    add("Solar gain is not a rounding error here — on the larger sink it rivals the SoC's own ")
    add("dissipation. Finish is a free lever:\n")
    add("| Finish | Absorptivity | Q_solar | T_j — pad, still, full load, 35 °C |")
    add("|---|--:|--:|--:|")
    for name, a, e in [("Black anodised", ABSORPTIVITY_BLACK, EMISSIVITY_BLACK),
                       ("Bare / clear / light", ABSORPTIVITY_LIGHT, EMISSIVITY_LIGHT)]:
        r = junction_temp(SINK_LARGE, P_BOARD_MAX_W, 35.0, 0.0, a, e, solar=True)
        add(f"| {name} | {a:.2f} | {r['q_solar']:.1f} W | {r['t_junction_c']:.0f} °C |")
    add("")

    # --- Sensitivity --------------------------------------------------------
    add("## 7. Sensitivity — where the conclusion actually comes from\n")
    add("The in-flight verdict is close enough to the line that it is worth showing exactly which ")
    add("assumptions carry it. Both are swept on the full-board sink at full load, 35 °C, in sun.\n")
    add("**(a) Hub inflow fraction** — the least-supported number in the model:\n")
    add("| Fraction of v_i | Airflow | T_j | Verdict |")
    add("|--:|--:|--:|:--:|")
    for frac in [0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50]:
        v = v_i * frac
        r = junction_temp(SINK_LARGE, P_BOARD_MAX_W, 35.0, v, solar=True)
        mark = "✅" if r["pass"] else ("⚠️" if r["t_junction_c"] <= T_THROTTLE_C else "❌")
        add(f"| {frac:.0%} | {v:.2f} m/s | {r['t_junction_c']:.0f} °C | {mark} |")
    add("")
    add("**(b) Model conservatism** — the still-air fin derate and the correlations together carry ")
    add(f"roughly ±25 %. Re-running the still-air pad case with R_sa scaled:\n")
    add("| R_sa scaling | T_j — pad, still, full load, 35 °C + sun | Verdict |")
    add("|--:|--:|:--:|")
    for scale, note in [(0.75, "optimistic"), (1.00, "nominal"), (1.25, "pessimistic")]:
        q_soc = P_BOARD_MAX_W * SOC_FRACTION
        base = junction_temp(SINK_LARGE, P_BOARD_MAX_W, 35.0, 0.0, solar=True)
        r_sa_nom = (base["t_sink_c"] - 35.0) / (q_soc + base["q_solar"])
        t_sink = 35.0 + (q_soc + base["q_solar"]) * r_sa_nom * scale
        t_j = t_sink + q_soc * (R_JC_KW + R_TIM_KW)
        mark = "✅" if t_j <= T_THROTTLE_C - DESIGN_MARGIN_C else ("⚠️" if t_j <= T_THROTTLE_C else "❌")
        add(f"| {scale:.2f}× ({note}) | {t_j:.0f} °C | {mark} |")
    add("")
    add("**(c) Actual heat load** — 10 W is the `R4_SBC_PWR` *cap*, not a measurement. FriendlyElec ")
    add("publishes no power figure for the M5; Rockchip quotes RK3576 TDP \"<15 W\" (SoC only), and ")
    add("third-party comparisons put it 20–40 % below the RK3588's ~12 W, i.e. **~7–10 W**. Sweeping ")
    add("the credible band (full-board sink, 35 °C, in sun):\n")
    add("| Board power | Board heat | Pad, still air | Flight, low propwash |")
    add("|--:|--:|--:|--:|")
    for p in P_BOARD_CREDIBLE_W:
        r_still = junction_temp(SINK_LARGE, p, 35.0, 0.0, solar=True)
        r_fly = junction_temp(SINK_LARGE, p, 35.0, v_hub_low, solar=True)
        m1 = "✅" if r_still["pass"] else ("⚠️" if r_still["t_junction_c"] <= T_THROTTLE_C else "❌")
        m2 = "✅" if r_fly["pass"] else ("⚠️" if r_fly["t_junction_c"] <= T_THROTTLE_C else "❌")
        add(f"| {p:.0f} W | {p - P_USB_EXPORT_W:.1f} W | {r_still['t_junction_c']:.0f} °C {m1} "
            f"| {r_fly['t_junction_c']:.0f} °C {m2} |")
    add("")
    add("Even at the bottom of the credible band the still-air pad case does not clear the design ")
    add("margin. The flight case, by contrast, is comfortable across the whole band — so the ")
    add("conclusion is **not** an artifact of using the requirement cap as the heat load.\n")
    add("**(d) Why measuring input power is necessary but not sufficient.** For an SBC essentially ")
    add("100 % of electrical input becomes heat (no mechanical work; radiated RF/optical is ")
    add(f"negligible), less what is exported through the ports — here the T13 camera draws ")
    add(f"~{P_USB_EXPORT_W:.1f} W over USB. So a wall-plug measurement bounds the **total** heat load ")
    add("directly and exactly. What it cannot resolve is the **split** between the SoC package (which ")
    add(f"the heatsink sees, assumed {SOC_FRACTION:.0%} here) and the DDR / PMIC / PHY / USB devices, which ")
    add("reject into the PCB. That split is the difference between a comfortable pass and a fail:\n")
    add("| SoC share of board heat | T_j — flight, low propwash, 35 °C + sun | T_j — pad, still air |")
    add("|--:|--:|--:|")
    for frac in [0.55, 0.70, 0.85, 1.00]:
        rf = junction_temp(SINK_LARGE, P_BOARD_MAX_W, 35.0, v_hub_low, solar=True,
                           soc_fraction=frac)
        rs = junction_temp(SINK_LARGE, P_BOARD_MAX_W, 35.0, 0.0, solar=True,
                           soc_fraction=frac)
        add(f"| {frac:.0%} | {rf['t_junction_c']:.0f} °C | {rs['t_junction_c']:.0f} °C |")
    add("")
    add("**The way out is not a better model — it is the on-die sensor.** The RK3576 exposes junction ")
    add("temperature at `/sys/class/thermal/thermal_zone*/temp`. Logging input power *and* SoC ")
    add("temperature together, under the real workload on the as-built deck, measures the heat load ")
    add("and the assembly's actual thermal resistance simultaneously and retires every assumption ")
    add("in this document. **`VB-02` (power) and `VB-03` (thermal) should be run as one test.**\n")
    add("Read together: **no plausible combination rescues still-air operation at full load**, and ")
    add("the in-flight case flips on whether the hub sees more or less than ~20 % of v_i — which ")
    add("nobody has measured.\n")

    add("## 8. Assumptions and limits\n")
    add("- No published thermal test data exists for the NanoPi M5; this is a first-principles ")
    add("  bound. **VB-03 (bench thermal soak) is the closing evidence**, not this document.")
    add("- Laminar flat-plate and horizontal-plate correlations; real finned-sink performance ")
    add("  typically lands within ±25 % of this.")
    add("- The hub inflow fraction is an engineering estimate, not CFD or measurement. It is the ")
    add("  single most load-bearing assumption — hence designing to the low end.")
    add(f"- Fin area derated to {DERATE_NATURAL:.0%} in still air and {DERATE_FORCED:.0%} in forced flow.")
    add("- Steady state only. Thermal mass buys a few minutes of transient headroom on the pad, ")
    add("  which is exactly the phase where the still-air cases are marginal.")
    add(f"- Board ambient spec is {T_AMB_SPEC_C:.0f} °C; nothing here approaches that limit — the ")
    add("  binding constraint is the SoC junction, not the board rating.")

    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_MD}")

    # Console summary — the decision-relevant numbers.
    print(f"\nInduced velocity v_i = {v_i:.2f} m/s; hub band {v_hub_low:.2f}-{v_hub_high:.2f} m/s")
    for s in sinks:
        print(f"\n{s.label}  (area {s.area_geometric*1e4:.0f} cm2)")
        for label, p, ta, v, sun in cases:
            r = junction_temp(s, p, ta, v, solar=sun)
            print(f"   {label:52s} Tj={r['t_junction_c']:6.1f} C  margin={r['margin_c']:+6.1f}  "
                  f"{'PASS' if r['pass'] else 'FAIL'}")
        vm = min_airflow_for_pass(s, P_BOARD_MAX_W, 35.0, solar=True)
        print(f"   -> min airflow (full load, 35 C, sun): {vm if vm is not None else 'unachievable'}")


if __name__ == "__main__":
    main()
