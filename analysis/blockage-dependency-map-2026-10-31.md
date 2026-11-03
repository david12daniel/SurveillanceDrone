# Blockage Dependency Map — 2026-10-31

## Executive Summary

**Every non-human_only task in the Surveillance Drone project is blocked.** The entire project is stalled at the CDR gate (task #85 — Present CDR Briefing to Lisa, due Aug 3, past due). All Phase 1 ordering tasks (1.1–1.10) are gated on #85. All Phase 2+ work is gated on ordering first.

## The Dependency Chain

### Root Blocker
```
#85 [0.1] Present CDR Briefing to Lisa
  Status: Doing | Human: YES | Past due (2026-08-03)
  → Gates: ALL Phase 1 ordering tasks (#16-#25)
  → Those gate everything else
```

### Tier 1 — Ordering (#85 gates these)
```
#16 [1.1]  Order iFlight Chimera9 ECO              → gates #26, #27, #28, #29, #30, #31, #38
#17 [1.2]  Order ELRS receiver                      → gates #28
#18 [1.3]  Order TX12 Mark II radio                 → gates #28
#19 [1.4]  Order Hermes ELRS dongle                 → gates #28
#20 [1.5]  Order BAT10 battery                      → gates #37, #48, #49
#21 [1.6]  Order BAT22 dev packs                    → gates #37
#22 [1.7]  Order Skydroid VRX6                      → gates #32
#23 [1.8]  Order TrueRC patch antenna                → gates #32
#24 [1.9]  Order anti-spark filter                   → gates #26
#25 [1.10] Order HOTA D6 Pro charger                 → gates #26
#40 [2.2]  Order T13 thermal camera                 → gates #47, #51, #53
#41 [2.3]  Order NanoPi M5 SBC                      → gates #44, #50, #51
#42 [2.4]  Order UBEC + USB-C cable                 → gates #50, #79
#43 [2.5]  Order mount hardware                     → gates #47, #56
#77 [4.2]  Order WLAN_AIR1 + pigtails               → gates #79, #80, #81
#78 [4.3]  Order cloverleaf + WLAN_GND1             → gates #80, #82
```

### Tier 2 — Hardware tasks (gated on ordering)
```
#38 [1.23] Caliper the frame (needs #16, physical)       → gates #44, #48
#26 [1.11] Verify XT60 chain (needs #16, #20, #21, #24, #25)
#27 [1.12] Flash ArduPilot (needs #16)
#28 [1.13] Bind ELRS (needs #17, #18, #19, #27)
#29 [1.14] Calibrate sensors (needs #27)
#30 [1.15] Configure failsafe/arming (needs #5, #6, #27, #29)
#32 [1.17] Connect VRX6 + PATCH1 (needs #22, #23)
#39 [2.1]  Confirm T13 mass (vendor, 12d no reply)      → gates #45
#50 [2.12] Set UBEC 12V, power M5 (needs #41, #42)      → gates #52, #53, #54, #56, #62
#51 [2.13] Mount thermal + SBC (needs #40, #41, #47)
#52 [2.14] Wire SBC ↔ FC (needs #27, #50, #51)
#53 [2.15] Confirm T13 enumerates (needs #40, #50)      → gates #65
#79 [4.4]  Set UBEC 5V for air module (needs #42, #77)
#80 [4.5]  Mount air module (needs #51, #77, #78, #79)
#81 [4.6]  Build WFB-ng TX (needs #77, #80)
#47 [2.9]  Print & test-fit mounts (needs #40, #43, #44, #45)
```

### Tier 3 — Software/analysis tasks (all blocked by hardware)
```
#44 [2.6]  Design SBC deck          ← blocked by #38, #41 (estimate/order)
#45 [2.7]  Thermal mount v2         ← blocked by #39 (vendor reply)
#48 [2.10] Update candidates.sysml   ← blocked by #20, #38
#49 [2.11] Re-check mass/CG         ← blocked by #11(DONE), #39, #44, #48
#54 [2.16] mavlink-router on SBC    ← blocked by #50, #52 (need hardware)
#55 [2.17] Field-verify Johnson     ← blocked by #51, #53 (need hardware)
#56 [2.18] Bench-test SBC envelope  ← blocked by #43, #50, #53
#60 [D1.4] Training pipeline        ← blocked by #57 (data collection, human)
#61 [D1.6] RKNN quant conversion    ← blocked by #60
#64 [D1.9] AGPL-3.0 license check   ← blocked by #60
#65 [D2.5] UVC capture pipeline     ← blocked by #53 (need hardware)
#66 [D2.6] RKNN inference wrapper   ← blocked by #61, #65
#72 [3.1]  Deploy .rknn live        ← blocked by #51, #61, #66
#73 [3.2]  Detections→MAVLink       ← blocked by #34, #54, #67, #72
#74 [3.3]  SBC-failure fallback     ← blocked by #69, #73
```

## Tasks That Are Done (but still blocking downstream unverified)
```
#67 [D2.8] adjustOrbit loiter      — Done, unverified; but blocks #73 (which is blocked by much more anyway)
#69 [D2.12] Service hardening       — Done, unverified; blocks #74 (blocked anyway)
```

## Conclusion

The entire project is blocked on **CDR sign-off (#85)**. No amount of agent research or code work can advance the project until David completes the CDR briefing to Lisa and the orders are placed.

The only partial pre-work that could be done (T13 mass confirmation, #39) has been researched exhaustively over 8 weeks — the vendor inquiry was sent Oct 19 with no reply after 12 days. The estimate (15.0g) is sufficient for ordering.