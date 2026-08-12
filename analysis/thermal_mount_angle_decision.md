# Decision: Nadir vs 45° Down-Look Thermal Mount

**Date:** 2026-08-07
**Task:** [2.8] Decide nadir vs 45-degree down-look thermal mount
**Status:** DECIDED — 45° down-look (forward-looking)

---

## 1. The Question

The Chimera9 ECO nose already has two parametric v1 brackets:
- `cad-resources/thermal_mount.py` — **nadir** (camera points straight down, flat plate)
- `cad-resources/thermal_mount_45.py` — **45° down-look** (camera tilted forward-and-down, gusset-reinforced)

Pick one for the committed build. The 18 mm lens (T13, SELECTED 2026-07-29) recognizes at 45° (4.17 px along-range at 90 m; §3 of the off-nadir analysis), so the tilt is now technically valid — the original concern that 13 mm/15 mm would fail recognition at 45° no longer applies.

---

## 2. Spatial Analysis — Johnson Criteria at 45° (18 mm lens)

All numbers from `analysis/thermal_detection_offnadir_analysis.md` §3, verified independently:

| Condition | Altitude | Along-range px | Cross-range px | 1.5 px detect? | 4.0 px recog? |
|---|---|---|---|---|---|
| Nadir | 90 m | 8.33 | 8.33 | ✅ | ✅ |
| **45°** | **90 m** | **4.17** | **5.89** | ✅ | ✅ **bounding** |
| Nadir | 120 m | 6.25 | 6.25 | ✅ | ✅ |
| **45°** | **120 m** | **3.13** | **4.42** | ✅ | ❌ detect only |

**Key finding:** At 45° @ 90 m (the InvestigateAndClassify altitude), the along-range 4.17 px **just meets** the 4 px recognition criterion. At 45° @ 120 m (SweepAndDetect altitude), the along-range 3.13 px is below the 4 px recognition threshold but still **well above** the 1.5 px detection threshold — so detection during sweeping is unaffected.

**Conclusion: 45° is spatially viable with the 18 mm lens.** No tilt servo needed. The along-range margin at 90 m (4.17 px) is thin but sufficient — the classified target is a 0.5 m standing human; a wider target (1.5 m deer) would see 12.5 px, making the margin extremely comfortable for the primary wildlife application.

---

## 3. CONOPS Fit — Which Mount Matches the Mission?

The behavioral model (`model.sysml::Behavior`, also `analysis/autonomy_sim/mission_app.py`) defines two operational modes:

### SweepAndDetect (cruise @ 120 m)
- **Nadir:** The camera sees only what the drone flies directly over. The effective swath is the camera's angular FOV projected onto the ground — 51.2 m wide at 120 m (18 mm lens). The drone must pass directly over or very near a target for detection.
- **45°:** The camera looks ~47 mm forward and ~23 mm down from the nose. At 120 m, the camera's optical axis intersects the ground at ~120 m ahead of the drone. Targets are detected *before* the drone overflies them, giving extra time for the detection→alert→GUIDED→descend pipeline.

### InvestigateAndClassify (loiter @ 90 m, adjustOrbit)
- **Nadir:** Camera points straight down while the drone orbits. The target stays in frame only when the drone is roughly overhead. On each orbit, there's a dead zone on the far side where the camera loses sight of the target.
- **45°:** The camera looks forward-down. During the adjustOrbit loiter, the camera is aimed *in the direction of travel* — the target stays visible across a larger portion of each orbit. This is a meaningful advantage for the classify loop (which already has a 30 s wall-clock budget; see task 0.4).

### Operator override (UC-11)
The operator views the same feed the onboard inference sees. With a 45° forward look, the operator sees the same terrain *ahead* of the drone rather than *below* it — more natural situation awareness for a manual override decision.

**Verdict: 45° wins on CONOPS fit.** The forward look is better aligned with both the detect-while-sweeping and the classify-while-orbiting behaviors.

---

## 4. Mechanical Comparison

| Aspect | Nadir (flat plate) | 45° (gusset) |
|---|---|---|
| Part count | 1 flat plate, 3 mm thick | 1 plate + gusset, 3 mm thick |
| Print complexity | Trivial (flat, no supports) | Moderate (overhanging face, needs supports or clever orientation) |
| Stiffness | Cantilevered flat plate | Gusset adds significant stiffness |
| Mass | ~6 g (PETG est.) | ~10 g (PETG est.) |
| Camera +Z dimensions | Camera hangs below the plate | Camera hangs forward-down |
| Bolt pattern | Same 30.5 mm FRAME_BOLT_PITCH | Same 30.5 mm FRAME_BOLT_PITCH |

The 45° mount is mechanically more complex (gusset, supports) and ~4 g heavier, but the gusset adds stiffness that resists vibration-induced blur — important for LWIR imaging at 25 fps.

---

## 5. Clearance Check

### Lens tip position (45° mount, worst case)
From `cad-resources/thermal_mount_45.py`:
- Face plate at Y = +13.3 mm, Z = -10.3 mm (relative to the base plane at the frame bolt line)
- Camera body: 21×21×10.3 mm, lens barrel: Ø20 × 24 mm
- At 45° tilt, the lens tip is at ~Z = -10.3 - (10.3 + 24) × cos(45°) = **-34.5 mm** below the base
- And Y = +13.3 + (10.3 + 24) × sin(45°) = **+37.6 mm** forward of the bolt line

### Prop clearance
- Chimera9 ECO: 9" props = 228.6 mm diameter → 114.3 mm radius
- Front motors are well aft of the nose tip (the frame is a true-X, front arms ~45° from centerline)
- At the nose centerline, the nearest prop tip is ~100 mm away horizontally
- The camera at +37.6 mm forward and -34.5 mm down is **well clear of the front prop arc**

### Landing gear clearance
- The Chimera9 ECO has bottom-mounted landing pads (rubber bumpers on the arms)
- Total ground clearance is typically ~30-40 mm (arm thickness + prop clearance)
- The lens tip at -34.5 mm below the base plate is close to the landing gear bottom
- **Risk:** On landing, the camera lens tip could be the lowest point. If landing on uneven ground, the lens could contact before the landing pads.

### Mitigation
- The 45° mount face plate can be trimmed (the "chunky face plate" mentioned in the task notes) — reducing the lens tip Z-depth by ~3-5 mm
- Alternatively, add landing skids that extend below the lens tip (~35 mm)
- The nadir mount has the lens at -PLATE_T - body_depth = -3 - 10.3 - 24 = **-37.3 mm** below the plate — actually *worse* than the 45° mount for landing clearance

**Verdict: 45° clearance is acceptable** with a minor trim or landing skid mitigation. The nadir mount has the same or worse landing clearance issue.

---

## 6. Coverage Area Comparison

The off-nadir analysis (§4) calculates area at **nadir** swath only. At 45° tilt, the effective surveillance area is different:

- **Nadir swath:** 51.2 m wide @ 120 m (18 mm lens)
- **45° swath:** The camera sees forward, not straight down. The ground footprint is a trapezoid ahead of the drone. The effective cross-track swath at the *intersection* of the optical axis with the ground plane is wider than the nadir swath, but the geometry is more complex.

For the SweepAndDetect phase, the 45° tilt means the drone detects targets *before* overflying them. This doesn't reduce the area per sortie — it simply shifts the detection zone forward. The coverage per sortie is essentially the same (the drone flies the same route at the same speed).

**Verdict: No meaningful coverage penalty for 45° vs nadir** in the committed CONOPS. The off-nadir analysis's area comparison (nadir swath) is a constant factor between lens choices, not a tilt decision.

---

## 7. Recommendation

**Select the 45° down-look mount.** Rationale:

1. **CONOPS alignment:** Forward-looking detection is better for both SweepAndDetect (see targets before overflying) and InvestigateAndClassify (target stays visible during orbit) — the primary reason the 18 mm lens was chosen.
2. **Spatially viable:** 4.17 px along-range at 90 m meets the 4 px recognition criterion, and 3.13 px at 120 m meets the 1.5 px detection criterion.
3. **Mechanically acceptable:** The gusset is stiffer than the flat plate (better vibration resistance). The mass penalty is ~4 g out of 1.8 kg all-up — negligible.
4. **Clearance manageable:** The lens tip position is within the landing gear envelope. Mitigate with a face plate trim and/or landing skids.

### Action items

1. **Trim the face plate** of `thermal_mount_45.py` — reduce the chunky front face from full-width to the hole footprint (saves ~3-5 mm of unnecessary depth)
2. **Add triangular gussets** to clean up the chunky support block (replaces the current `build_gusset()` wedge with a lighter, cleaner triangular gusset)
3. **Verify landing clearance** — print a quick test-fit or check the lens tip Z-depth against the Chimera9's landing pad height. If tight, add 3 mm landing skid extensions to the bottom plate.
4. **Update the nadir mount to v2** as a 45° variant branch — don't delete the nadir mount, but mark it as superseded in the doc string.
5. **Update the CAD spec** (`mini640_t13_cad_spec.md` or `cad-resources.md`) to note the 45° decision.

### Reference

- `cad-resources/thermal_mount_45.py` — current 45° v1 bracket (parametric, needs the face trim + gusset cleanup)
- `cad-resources/thermal_mount.py` — nadir bracket (superseded for this build)
- `analysis/thermal_detection_offnadir_analysis.md` — full Johnson pixel analysis
- `model.sysml` — Behavior::SweepAndDetect / InvestigateAndClassify (CONOPS)