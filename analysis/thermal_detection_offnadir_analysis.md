# Thermal Detection Analysis — Off-Nadir Tilt & Lens Trade (15/18/25/35 mm)

> **DECISION (2026-07-29): the 18 mm lens was selected** (see §5). This analysis is the
> supporting rationale. `SELECTED_COMPONENTS.md`, `candidates.sysml` (T13), `BOM.md`, and the
> CAD spec/model are updated accordingly. R3_CAM_FOV (≥30°) re-tag is pending model approval.

**Purpose:** for the surveillance mission (IR is **not** used to fly — the FPV camera does
that), evaluate the available longer lenses **15, 18, 25, 35 mm** at **nadir** and at
**45° off-nadir**, quantify (a) detection/recognition pass-fail, (b) **how the ≥30° FOV
requirement arose and whether it can be relaxed**, and (c) **how much surveillance area
each lens costs** over one full-battery sortie. Extends the nadir baseline in
[`market_analyses_and_research/camera_market_analysis.md`](market_analyses_and_research/camera_market_analysis.md) §6.

**Fixed inputs:** sensor 640×512, **12 µm** pitch (7.68 × 6.14 mm active); target
**0.5 × 0.5 m** flat on the ground; model criteria — **detection ≥ 1.5 px** (R3_1, @120 m),
**recognition ≥ 4 px in each dimension** (R3_2 / R3_CAM_RES, @90 m). All numbers computed
in-script (`math` only).

---

## 1. Why the ≥30° FOV requirement exists (R3_CAM_FOV)

`model.sysml` states R3_CAM_FOV only as *"horizontal field of view of at least 30 degrees"*
with **no flight/piloting rationale** — and there isn't one: the drone is flown by the
separate **FPV camera**, never the thermal. The 30° figure is a **coverage (swath) floor**:
the camera trade study picked 13 mm because it "**keeps ground swath at ~52 m**" at 90 m,
i.e., enough width to sweep ground efficiently. So **≥30° is an area-scan-rate constraint,
not a safety/controllability one.** Relaxing it below 30° is therefore purely a
**coverage-vs-resolution trade** — exactly what §4 quantifies — and is acceptable for a
surveillance-only IR payload. (The requirement should be re-tagged as a *coverage* goal,
not a hard constraint, if a narrower lens is chosen — a `model.sysml` change needing approval.)

## 2. Off-nadir geometry (45°)

At altitude **H** (AGL), camera depressed **θ = 45°** from nadir, flat-ground target on axis:
- **Slant range** `R = H/cosθ` = **1.414·H**.
- **Cross-range GSD** `= R·IFOV = GSD_nadir/cosθ` → **×1.414**.
- **Along-range GSD** `= R·IFOV/cos²θ = GSD_nadir/cos²θ` → **×2.000** (the binding axis).
- Pixels-on-target scale **×cosθ (cross) / ×cos²θ (along)** → at 45°, **×0.707 / ×0.500**.

## 3. Lens evaluation — pixels on a 0.5 m target

| Lens | HFOV | Nadir @90 m | Nadir @120 m | 45° along @90 m | 45° along @120 m |
|---|---|---|---|---|---|
| 13 mm (current) | 32.9° | 6.02 | 4.51 | 3.01 | 2.26 |
| 15 mm | 28.7° | 6.94 | 5.21 | 3.47 | 2.60 |
| 18 mm | 24.1° | 8.33 | 6.25 | 4.17 | 3.13 |
| 25 mm | 17.5° | 11.57 | 8.68 | 5.79 | 4.34 |
| 35 mm | 12.5° | 16.20 | 12.15 | 8.10 | 6.08 |

**Pass/fail** (recognition ≥ 4 px each dim — along-range binding; detection ≥ 1.5 px):

| Lens | Nadir recog @90 | Nadir detect @120 | **45° recog @90** | **45° detect @120** |
|---|---|---|---|---|
| 13 mm | ✅ 6.02 | ✅ 4.51 | ❌ 3.01 | ✅ 2.26 |
| 15 mm | ✅ 6.94 | ✅ 5.21 | ❌ 3.47 | ✅ 2.60 |
| **18 mm** | ✅ 8.33 | ✅ 6.25 | ✅ **4.17** | ✅ 3.13 |
| 25 mm | ✅ 11.57 | ✅ 8.68 | ✅ 5.79 | ✅ 4.34 |
| 35 mm | ✅ 16.20 | ✅ 12.15 | ✅ 8.10 | ✅ 6.08 |

- **At nadir, every lens (13–35 mm) passes** both recognition and detection — the choice is
  pure coverage-vs-margin.
- **At 45°, recognition needs ≥ 18 mm.** 13 and 15 mm fall below 4 px along-range (3.0/3.5).
  Detection at 120 m survives for *all* lenses even at 45°.
- So **18 mm is the shortest lens that recognizes at a fixed 45° tilt** — and it keeps the most coverage of the passing options.

**Visual illustration** (pixels-on-target simulated for a deer and a person at 45° for 13/15/18 mm
× 90/120 m): [`thermal_sim/thermal_sim_deer_45deg.png`](thermal_sim/thermal_sim_deer_45deg.png),
[`thermal_sim/thermal_sim_person_45deg.png`](thermal_sim/thermal_sim_person_45deg.png)
(regenerate with `thermal_sim/generate_thermal_sim.py`). A 1.5 m deer stays a recognizable blob in
every case; a **standing person's 0.5 m width is the limiter** — it drops to ~3 px wide at 13 mm/120 m
(detect-only), which the 18 mm lifts back to ~4 px.

## 4. Surveillance area per sortie (coverage cost of a longer lens)

Swath is set by the wide axis: `swath = H · sensor_w / f`. Area mapped over a sortie
≈ `swath × path_length × coverage_efficiency`, where `path = cruise_speed × scan_time`.

**Assumptions** (state-and-scale — area is linear in each): endurance **57 min** (BAT10 hover,
[SELECTED_COMPONENTS.md](../SELECTED_COMPONENTS.md)); **20 % battery reserve**; **~4 min**
climb+descent+short return (per your "not far at turnaround" framing) → **~41.6 min scan**;
cruise **2.23 m/s** (R2) → **~5.57 km** ground path; sweep at **120 m AGL** (max swath, all
lenses still detect); **80 % coverage efficiency** (20 % sidelap + turnarounds).

| Lens | Swath @120 m | Effective area / sortie | vs 13 mm |
|---|---|---|---|
| 13 mm | 70.9 m | **31.6 ha (78 ac)** | 100 % |
| 15 mm | 61.4 m | 27.4 ha (68 ac) | 87 % |
| **18 mm** | 51.2 m | **22.8 ha (56 ac)** | **72 %** |
| 25 mm | 36.9 m | 16.4 ha (41 ac) | 52 % |
| 35 mm | 26.3 m | 11.7 ha (29 ac) | 37 % |

Area scales as **1/focal-length** (swath ∝ 1/f), so the ratios hold regardless of the
endurance/altitude/efficiency assumptions — only the absolute hectares move. Flying the
sweep at 90 m instead of 120 m shrinks every number by 25 % (0.75×) but leaves the ratios
unchanged. (These are nadir swaths; a 45° tilt looks *ahead* rather than down but the
lens-to-lens area **ratio** is the same.)

## 5. Findings & recommendation

1. **≥30° FOV was a coverage floor, not a flight requirement** — safe to relax for a
   surveillance-only IR. Doing so trades area for on-target resolution, nothing else.
2. **Nadir:** all lenses work; **13 mm maximizes coverage** (78 ac/sortie) and already meets
   recognition+detection. No reason to go longer *unless* you tilt or want more classify margin.
3. **Fixed 45° tilt:** **18 mm is the minimum** that keeps recognition (4.2 px) — at a **28 %
   coverage cost** (78 → 56 ac). 15 mm still fails recognition at 45°; 13 mm fails badly.
4. **25 / 35 mm** buy large resolution margin (useful for smaller/cooler targets, higher
   altitude, or higher classify confidence) but at **48 % / 63 % coverage loss** — only worth
   it if per-target ID confidence matters more than area swept.

**Recommendation:**
- **Staying nadir → keep 13 mm** (best coverage, all criteria met). This remains the baseline.
- **Want a fixed 45° oblique look → 18 mm** is the sweet spot (recognizes at 45°, best
  coverage of the passing lenses). Accept ~28 % less area and re-tag R3_CAM_FOV as a goal.
- **Best of both → 13 mm on a tilt servo:** sweep obliquely for situational awareness,
  revert to nadir to classify — keeps full coverage *and* recognition, no lens penalty
  (the `SweepAndDetect → InvestigateAndClassify` split already in the behavior model).

---

### Assumptions & method
- Flat 0.5 × 0.5 m ground target on the optical axis; small-angle IFOV = pitch / focal length.
- Off-nadir GSD: cross `R·IFOV`, along `R·IFOV/cosθ`, `R = H/cosθ`; pixels = target / GSD.
- Area: `swath = H·sensor_w/f`; `area = swath · (v · t_scan) · eff`. Nadir swath used for the
  lens-to-lens comparison; ratios are assumption-independent (∝ 1/f).
- Ignores atmospheric transmission and NETD/contrast (unchanged across lenses); pure spatial
  (Johnson pixels-on-target) treatment, matching the model's `PixelsAcrossTarget` /
  `DetectionCriterion` / `RecognitionCriterion`.
- 12 µm pitch throughout; the older camera_market_analysis table's 13 mm IFOV was slightly
  optimistic (0.87 vs 0.92 mrad) — a rounding difference, not geometry.
