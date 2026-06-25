# ELRS (ExpressLRS) Telemetry Range Analysis

**Date:** 2026-06-10  
**Context:** Evaluating whether a single ELRS receiver can serve as both the RC control input AND the telemetry downlink for the Surveillance Drone, eliminating the need for a separate TelemetryTransmitter component.

---

## Requirement

From model.md — requirement **R7**:

> Minimum linear distance during surveillance: **2800 meters** (2.8 km) when performing surveillance at 2.2 m/s in sustained wind conditions of 4.5 m/s.

From model.md — requirement **R4_GCS_RANGE**:

> The GCS control link and video receiver shall maintain a reliable connection with the drone at a slant range of at least **2800 meters** under clear line-of-sight conditions.

---

## ELRS Capability

Source: [ExpressLRS Official Long Range Competition Leaderboard](https://www.expresslrs.org/info/long-range/)

### 2.4 GHz ELRS on Quadcopters

| TX Power | Demonstrated Range (km) | Meets 2.8 km? | Confidence |
|----------|------------------------|---------------|------------|
| **25 mW** | **3.5 – 4.6 km** | ✅ Yes | Multiple entries on leaderboard |
| 100 mW | 10.2 km | ✅ Yes | ✅ High |
| 250 mW | 10 – 16 km | ✅ Yes | ✅ High |
| 500 mW | 5 – 13 km | ✅ Yes | ✅ High |

### 900 MHz ELRS on Quadcopters

| TX Power | Demonstrated Range (km) | Meets 2.8 km? | Confidence |
|----------|------------------------|---------------|------------|
| **10 mW** | **2.2 km** | ❌ No (borderline) | Single entry, failsafed |
| **50 mW** | **5.0 km** | ✅ Yes | ✅ High |
| 100 mW | 13.1 km | ✅ Yes | ✅ High |
| 500 mW | 50+ km | ✅ Yes | ✅ High |

---

## Key Findings

1. **2.4 GHz ELRS at 25 mW** — the most common BNF receiver config — comfortably exceeds 2.8 km on quadcopters (3.5+ km demonstrated). This is the default for most KOLAS7, Chimera, ROC7, and EMAX BNF options offered with ELRS.

2. **ELRS is bidirectional** — RC control goes uplink, telemetry (GPS, battery, flight mode, etc.) comes downlink on the **same RF link**. No separate telemetry radio module needed.

3. **900 MHz ELRS offers better penetration** through trees/foliage if needed, but 2.4 GHz is sufficient for open line-of-sight at our required range.

---

## Architecture Implication

The **TelemetryTransmitter** and **RadioReceiver** can be merged into a single component. When using ELRS:

- **Onboard:** ELRS receiver handles both RC control input and telemetry return
- **Ground:** RadioControlTransmitter (e.g., Radiomaster TX16S with ELRS module) receives telemetry and pipes it to the GCS via USB
- **Cost:** No separate telemetry radio — saves $30-60, ~10g weight, and a UART port
- **UART impact:** ELRS receiver uses one UART on the flight controller for bidirectional CRSF protocol

---

## Recommendation

✅ **Use a single ELRS receiver as the combined RC control + telemetry link.** This replaces the separate TelemetryTransmitter component. The RadioReceiver should carry a `telemetryCapable: Boolean = true` attribute (or the architecture can simply remove TelemetryTransmitter as a standalone part).

**Default recommendation: 2.4 GHz ELRS** since it's the most common BNF receiver option, has more than enough margin to 2.8 km, and avoids the larger antennas needed for 900 MHz.
