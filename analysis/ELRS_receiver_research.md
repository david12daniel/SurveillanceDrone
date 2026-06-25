# ELRS 2.4 GHz RadioReceiver — Market Research

**Date:** 2026-06-10
**Purpose:** Phase 1 component selection — onboard ELRS receiver handles RC control + telemetry on one link.

> **Consolidated CSV:** All data plus airframe cross-references in `analysis/ELRS_receivers.csv` (18 columns, 21 receiver entries).

## Selection Criteria (for our application)
- **Range:** Must clear R7 (2.8 km linear surveillance distance) - 2.4 GHz ELRS with PA/LNA easily does this
- **Weight:** <5 g preferred (7" long-range airframe has payload to spare)
- **Cost:** $10-45 range
- **Interface:** CRSF (standard serial protocol for ELRS → FC)
- **Diversity:** Desirable for link robustness at long range
- **Telemetry Power:** Higher = better telemetry return link budget

## Candidate Receivers - Detailed Specs

### RadioMaster RP1 V2 ($12.99)
| Spec | Value |
|------|-------|
| **Cost** | ~$12.99 (amainhobbies.com, Amazon) |
| **MCU** | ESP8285 |
| **RF Chip** | SX1281 |
| **Antenna** | 1× external 65mm UFL T-antenna |
| **Weight** | 2.2 g (incl. antenna) |
| **Size** | 13 × 11 × 3 mm |
| **Telemetry Power** | 10 mW (no PA/LNA) |
| **Diversity** | None (single antenna) |
| **TCXO** | Yes |
| **Bus Interface** | CRSF |
| **Refresh Rate** | 25-500 Hz / F1000 |
| **Input Voltage** | 5 V DC |
| **Power Draw** | ~80-100 mA (est., ESP8285) |
| **Range (est.)** | ~2-3 km LOS (low telemetry power limits return link) |
| **Notes** | Budget option. No PA means weaker telemetry. Fine for close-range but marginal at 2.8 km. |

### RadioMaster RP2 V2 ($12.99)
| Spec | Value |
|------|-------|
| **Cost** | ~$12.99 |
| **MCU** | ESP8285 |
| **RF Chip** | SX1281 |
| **Antenna** | Built-in ceramic SMD |
| **Weight** | 0.55 g |
| **Size** | 13 × 11 mm (PP) |
| **Telemetry Power** | 10 mW (no PA/LNA) |
| **Diversity** | None |
| **TCXO** | Yes |
| **Bus Interface** | CRSF |
| **Range (est.)** | ~1-2 km (ceramic antenna has worse gain than external) |
| **Notes** | Too range-limited for our application. Better suited to whoops/racing. ❌ |

### RadioMaster RP3 V2 ($24.99-29.99) ⭐ Recommended
| Spec | Value |
|------|-------|
| **Cost** | ~$24.99 (buddyrc.com) - $29.99 (readymaderc.com) |
| **MCU** | ESP8285 |
| **RF Chip** | SX1281 |
| **Antenna** | 2× external 65mm UFL T-antenna |
| **Weight** | 4.6 g (incl. both antennas) |
| **Size** | 22 × 13 × 4 mm |
| **Telemetry Power** | 100 mW (Skyworks SE2431L PA/LNA) |
| **Diversity** | Antenna Diversity (switched) |
| **TCXO** | Yes |
| **Bus Interface** | CRSF |
| **Refresh Rate** | 25-500 Hz / F1000 |
| **Input Voltage** | 5 V DC |
| **Power Draw** | ~120-180 mA (est., PA active during telemetry TX) |
| **Range (est.)** | 3.5+ km LOS (confirmed in other long-range builds) |
| **Notes** | Sweet spot. LNA improves RX sensitivity, PA boosts telemetry to 100 mW. Antenna diversity adds link robustness. Widely used on 7" LR builds. |

### RadioMaster RP4TD ($39.99-44.99) ⭐ Premium
| Spec | Value |
|------|-------|
| **Cost** | ~$39.99 (Amazon, readymaderc.com) |
| **MCU** | ESP32 |
| **RF Chip** | 2× SX1281 (dual independent radios) |
| **Antenna** | 2× external 65mm UFL T-antenna |
| **Weight** | 1.4 g (without antennas) / ~3 g with antennas |
| **Size** | 23.7 × 16.3 × 4 mm |
| **Telemetry Power** | 2 × 100 mW (dual PA) |
| **Diversity** | True Diversity (dual independent RX chains) |
| **TCXO** | Dual TCXO |
| **Bus Interface** | CRSF + UART |
| **Refresh Rate** | 25-500 Hz / F1000 |
| **Input Voltage** | 4.5-12 V DC (DCDC regulator - runs cooler) |
| **Power Draw** | ~150-250 mA (est., dual ESP32 + dual PA) |
| **Range (est.)** | 5+ km LOS (true diversity + dual PA) |
| **Extra** | Gemini mode compatible, WiFi, WebUI config |
| **Notes** | Best SNR/RSSI in class. Gemini mode provides frequency diversity (two different freqs at once) for urban/interference environments. Wider voltage range is nice for direct battery connection. Probably overkill for 2.8 km requirement but gives headroom. |

### Happymodel EP1 TCXO ($11.99-14.39)
| Spec | Value |
|------|-------|
| **Cost** | ~$11.99 (Amazon) - $14.39 (Banggood) |
| **MCU** | ESP8285 |
| **RF Chip** | SX1280/SX1281 |
| **Antenna** | 1× external UFL |
| **Weight** | 0.41 g (without antenna) |
| **Size** | 10 × 10 × 6 mm |
| **Telemetry Power** | Not specified (no PA - <20 mW est.) |
| **Diversity** | None |
| **TCXO** | Yes |
| **Bus Interface** | CRSF |
| **Range (est.)** | ~2-3 km (adequate at 2.8 km with good antenna placement) |
| **Notes** | Ultr-light. No PA = weaker telemetry return link for QGC telemetry. OK for basic RC control at range but telemetry may drop sooner. |

### Happymodel EP1 Dual TCXO ($14.39-18.99)
| Spec | Value |
|------|-------|
| **Cost** | ~$14.39 (Banggood) - $18.99 (retail) |
| **MCU** | ESP32 PICO D4 |
| **RF Chip** | 2× SX1280/SX1281 |
| **Antenna** | 2× external UFL |
| **Weight** | 1 g (without antennas) |
| **Size** | 19 × 14 mm |
| **Telemetry Power** | >19 dBm (~80 mW) |
| **Diversity** | True Diversity |
| **TCXO** | Yes |
| **Bus Interface** | CRSF |
| **Range (est.)** | 4+ km LOS |
| **Notes** | Best value diversity option. True diversity at half the cost of RP4TD. Telemetry power lower than RP3 but still adequate. |

### Happymodel EP2 TCXO ($11.99)
| Spec | Value |
|------|-------|
| **Cost** | ~$11.99 |
| **Antenna** | Built-in ceramic SMD |
| **Weight** | 0.44 g |
| **Size** | 10 × 10 × 6 mm |
| **TCXO** | Yes |
| **Range (est.)** | ~1-2 km (ceramic antenna limitation) |
| **Notes** | Too range-limited for LR application. ❌ |

### BetaFPV SuperD ($24.99)
| Spec | Value |
|------|-------|
| **Cost** | ~$24.99 |
| **Size** | 22 × 14 mm |
| **Weight** | 1.1 g |
| **Telemetry Power** | 100 mW |
| **PA/LNA** | Yes |
| **Diversity** | True Diversity |
| **TCXO** | Yes |
| **Range (est.)** | 4+ km LOS |
| **Notes** | Good specs. Less common than RadioMaster/Happymodel for LR builds. Build quality/perception is mixed. |

### iFlight True Diversity ($29.99)
| Spec | Value |
|------|-------|
| **Cost** | ~$29.99 |
| **Size** | 24.5 × 18.6 mm |
| **Weight** | 3.3 g |
| **Telemetry Power** | 250 mW |
| **PA/LNA** | Yes |
| **Diversity** | True Diversity |
| **TCXO** | Yes |
| **Range (est.)** | 5+ km LOS |
| **Notes** | Highest telemetry power (250 mW). Bulkiest/heaviest option. Good for long range but overkill for our needs. |

## Range Budget Analysis (2.4 GHz ELRS)

From our prior analysis (`analysis/ELRS_telemetry_range_analysis.md`):
- 2.4 GHz ELRS at **25 mW** → 3.5+ km LOS on quads
- 2.4 GHz ELRS at **100 mW** → 5+ km LOS
- 2.4 GHz ELRS at **250 mW** → 8+ km LOS

All PA-enabled receivers (RP3, RP4TD, SuperD, iFlight) clear R7 (2.8 km) with margin.

The key differentiator is **telemetry return link** power - the receiver's telemetry PA determines how far back the FC's status/MAVLink data reaches the ground. For autonomous waypoint missions (Phase 2+), telemetry range matters for real-time position/heartbeat monitoring.

## Recommendation

**Primary pick: RadioMaster RP3 V2 (~$25)**
- Best balance of cost ($25), range (3.5+ km), reliability (antenna diversity, TCXO, PA/LNA)
- Proven in 7" long-range builds
- 4.6 g weight is negligible on a 500+ g airframe
- 100 mW telemetry power ensures solid return link at 2.8 km

**If budget allows: RadioMaster RP4TD (~$40)**
- True diversity provides rock-solid link in challenging RF conditions
- Gemini mode for interference-heavy environments
- Wider voltage range (4.5-12 V) for direct battery connection
- Overkill for 2.8 km but gives maximum headroom

**Budget alternative: Happymodel EP1 Dual TCXO (~$14)**
- True diversity at half the cost
- Telemetry power (~80 mW) slightly lower than RP3
- Good for tight budgets, but telemetry may be weaker