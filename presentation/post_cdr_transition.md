# Post-CDR Transition Plan — From Sign-Off to Parts on the Bench

**Purpose:** What happens in the 48 hours after Lisa approves the CDR.  
**Prerequisite:** Task #85 done → all ordering tasks (#16–25, #40–43, #77–78) unblock.

---

## Within 2 Hours of Sign-Off

### 1. Set the CDR date stamp (optional but recommended)
```bash
cd /path/to/SurveillanceDrone
CDR_DATE=2026-10-XX python3 presentation/build_cdr.py
python3 presentation/verify_cdr_deck.py   # should show PASS with new date
```
This updates the 41-slide deck's date stamp to the actual review date. Cosmetic — but presenting a deck stamped 3 months ago reads as stale.

### 2. Commit and push the sign-off
```bash
git add CDR_Thermal_Surveillance_Drone.pptx
git commit -m "CDR signed off YYYY-MM-DD by Lisa"
git push origin master
```
Updates task #85 status to Done Unverified → verified → Done.

---

## Within 24 Hours of Sign-Off

### 3. Place orders — in priority sequence

**Tier 1 — Long-lead / high-value (do first):**
- **#16** iFlight Chimera9 ECO 9in PNP (AF3a) + GPS — frame is the build foundation; 2–4 week lead
- **#20** Upgrade Energy GREEN V2 6S3P 12Ah Amprius (BAT10) — single-source battery; longest procurement risk
- **#40** PurpleRiver Mini 640 (T13) 18mm USB — thermal camera; longest lead of electronics

**Tier 2 — Electronics (order same day as Tier 1):**
- **#17** iFlight True Diversity ELRS receiver
- **#18** RadioMaster TX12 Mark II ELRS radio
- **#19** HGLRC Hermes ELRS USB dongle
- **#22** Skydroid 150CH 5.8GHz UVC VRX
- **#23** TrueRC X-AIR 5.8 MK II patch antenna
- **#24** iFlight Anti Spark Filter XT60
- **#25** HOTA D6 Pro charger + USB-A to C adapter
- **#41** NanoPi M5 4GB (SBC3)
- **#42** 2-6S→12V 3A UBEC (2-pack) + USB-C power-only cable

**Tier 3 — Miscellaneous (can batch with above):**
- **#43** Mount hardware (30mm fan, heat-set inserts, screws, standoffs)
- **#77** WLAN_AIR1 + USB-A stub + pigtails (Phase 4 deferred — can wait)
- **#78** Cloverleaf pair + WLAN_GND1 + Foxeer Echo 2 Max (Phase 4 deferred — can wait)

> **Recommended ordering tool:** Single-session checkout from iFlight (frame, RX, filter) + separate from GetFPV/RaceDayQuads (electronics) + AliExpress (NanoPi, thermal camera). Use the BOM in candidates.sysml for exact SKUs.

### 4. Update the project tracker
```bash
# After each order is placed, update the corresponding task:
#   status=Doing → Done Unverified (with completed_by="Thermal Surveillance Drone")
# This keeps the kanban board reflecting real procurement progress.
```

---

## Within 1 Week of Sign-Off

### 5. While parts ship — prepare the build environment
- **Flash the BLITZ F7 FC** (task #27) — requires the FC; if it arrives early, can be done before the frame
- **Bind ELRS RX → TX12 → Hermes dongle** (task #28) — can be done entirely on the bench
- **Stand up QGroundControl** on the laptop — zero-cost, zero-part prep
- **Re-verify slides 26/27/30** (thermal analysis) if the T13 vendor replies with an exact assembled mass (currently 15.0g estimate). Use `python3 analysis/t13_mass_cg.py --new-mass-g <n>` to apply.

### 6. Update the prep doc
- Mark §0 pre-briefing checklist items as done
- Remove the "Lisa's background" question (now answered by having presented)
- Archive the exec summary (it served its one-time purpose)

---

## Dependency Chain After Sign-Off

```
CDR sign-off (#85)
  ├─ Ordering tasks (#16-25, #40-43, #77-78) → all unblock
  │   └─ Parts arrive → build tasks unblock
  ├─ Flash FC (#27) ← unblocked by Chimera9 arrival
  │   └─ Calibrate sensors (#29) ← unblocked
  │       └─ Config failsafes (#30) ← partially unblocked (depends on tasks 5/6 too)
  ├─ Confirm T13 mass (#39) ← vendor reply or proceed at 15.0g
  │   └─ Order T13 (#40) ← already tier-1, unblocked by CDR alone
  └─ All other tasks → recursive unblock as their dependency chain clears
```

---

## What NOT to do right after sign-off

- ❌ Do NOT redesign based on CDR feedback — the review was the time for changes
- ❌ Do NOT order Phase 4 parts (digital downlink) — wait until Phases 1–3 are flying
- ❌ Do NOT re-run the full trade-space sweep — the baseline is baselined; save changes for v2
- ❌ Do NOT close #39 without weighing the T13 when it arrives (even if the vendor never replies)

---

## Key Contact Info Found During Prep

| Contact | Purpose |
|---------|---------|
| justin.lu@purpleriver.cn | PurpleRiver Mini 640 mass inquiry (sent Oct 19, pending reply) |

---

*Last updated: 2026-10-25.*