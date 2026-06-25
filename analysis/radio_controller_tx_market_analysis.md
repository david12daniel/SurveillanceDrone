# Radio Controller & ELRS TX Module Market Analysis

**File:** `analysis/radio_controller_tx_market.csv` — 15 entries (10 controllers + 5 standalone modules), 27 columns

---

## Summary

All **10 radio controllers** that have **≥250mW internal ELRS** can clear the 2.8km requirement with margin. Even the 100mW Pocket is *probably* fine at 2.8km (ELRS 100mW has been proven to 3.5+ km), but we want margin.

### At a Glance

| Tier | Option | Power | Price | Range™ |
|------|--------|-------|-------|--------|
| **🥇 Best Value** | **TX8: Jumper T20 V2** | **1W** | **$150** | ✅ 10+ km |
| **🥈 Budget King** | **TX9: Jumper T-Pro V2** | **1W** | **$110** | ✅ 10+ km |
| **🥈 Best Gamepad** | **TX1: RadioMaster Boxer** | **1W** | **$172** | ✅ 10+ km |
| **🔧 Upgrade Path** | **TX5: TX12 MKII** | 250mW | $130 | ✅ +Ranger=$200 |
| **🏆 Premium** | **TX4: TX15** | 1W dual-band | $260 | ✅ Best link |
| **💡 Module-only** | **TXM1: Ranger Module** | 1W | $70 | ✅ |

### GCS Cost Impact at $2,500 Budget

| Controller | Controller Cost | GCS Budget Remaining | Notes |
|-----------|----------------|---------------------|-------|
| **Jumper T-Pro V2 (TX9)** | **$110** | **Plenty** | $2400 left for other components |
| Jumper T20 V2 (TX8) | $150 | Plenty | Dual 21700 batteries |
| Boxer (TX1) | $172 | Plenty | Fan-cooled 1W |
| TX12 MKII + Ranger (TX5+TXM1) | $200 | OK | Upgrade path from 250mW→1W |
| TX15 (TX4) | $260 | Tightening | Dual-band built-in |
| TX16S MK3 (TX3) | $350 | 😬 Getting tight | Premium |

### Recommendation

**Jumper T20 V2 (TX8)** or **RadioMaster Boxer (TX1)** at $150-172 are the sweet spots: 1W internal ELRS, proven 10+ km range, full-size gimbals, EdgeTX. The **Boxer** has a larger community and better support; the **T20 V2** has dual 21700 batteries and dual-band capability for less money.

If you already own a JR-bay radio, the **Ranger module (TXM1) at $70** upgrades it to 1W — no need to buy a whole new radio.

## Mated Pair Compatibility

Our onboard receivers (from `analysis/ELRS_receivers.csv`) mate directly with these:

| Onboard RX | Best TX Pairing | Notes |
|-----------|----------------|-------|
| RadioMaster RP3 V2 (100mW telemetry) | Boxer, TX16S, T20 V2 | RP3 needs 100mW+ TX for balanced link |
| RadioMaster RP4TD (Gemini, 2×100mW) | TX16S MK3 or TX15 | Gemini mode for both = best link |
| Happymodel EP1 Dual (80mW telemetry) | Any 250mW+ TX | Plenty of margin |
| iFlight True Diversity (250mW telemetry) | Any 1W TX | High telemetry return = excellent link |

All pairings with ≥250mW TX power clear 2.8km easily.