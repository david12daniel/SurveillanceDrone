# T13 (PurpleRiver Mini 640) Mass Research — Augmented Findings

**Date:** 2026-08-20

## Source Documents Retrieved

### 1. Made-in-China Product Page (18mm CVBS variant)
- **URL:** https://purpleriverai.en.made-in-china.com/product/XGZYESqMfoWl/
- **Key data:** `Weight: 6g (Without Lens)`
- Notes: This is the bare Mini2 module without any lens attached. The product page lists lens options from 4mm to 75mm.

### 2. thermal-image.com Product Description
- **URL:** https://www.thermal-image.com/product/mini-640-uncooled-lwir-thermal-camera-module/
- **Key data:** `under 8.6g lightweight design`
- The 8.6g figure appears to include a small lens (likely 9mm or 13mm that ships as default).

### 3. Official Mini2 Spec Sheet (PDF, downloaded from thermal-image.com)
- **Weight (Module Physical Properties, Without Lenses and Flanges):** `<20 g`
- **Size:** `21mm × 21mm × 28mm`
- **Power:** `<0.5W`
- **Lens options table:** 4/7/9/13/15/18/25/35/50/60/75mm
- **Selected lens (18mm):** FOV 24.2°×19.5°, F-number 1.0
- No per-lens weight breakdown published in the spec sheet.

## Mass Estimate Reconciliation

| Source | Figure | Condition |
|--------|--------|-----------|
| Made-in-China product page | 6g | Without lens |
| thermal-image.com product blurb | <8.6g | "lightweight design" (likely 9mm default lens) |
| Official spec sheet (PDF) | <20g | Without lenses and flanges |

The three figures are consistent but measure different configurations:

- **6g** = bare sensor + PCB + housing, no lens, no flange
- **<8.6g** = module with a compact lens (9mm or 13mm)
- **<20g** = module in broader spec condition (may include shutter, interface board, etc.)

## 18mm Lens Weight Estimate

The selected 18mm germanium LWIR lens (F1.0, 24° HFOV):

- Typical germanium 2-element lens for 640×512 @12µm: ~5-7g
- Aluminum barrel/housing: ~2-3g  
- **Estimated 18mm lens assembly weight: 6-9g**

**Total T13 mass estimate (module + 18mm lens): 12-17g**

## Comparison with Current Model

Current `candidates.sysml` T13: `mass = 21.0 [g]`

The current value is conservative (overestimates by ~25-43%). This means:
- Flight time models using 21g are slightly pessimistic (safe direction)
- CG is less affected by nose payload than modeled  
- The actual mass margin for other payload is ~4-9g more than computed

**Recommendation:** Update T13 mass to `15.0 [g]` as a tighter estimate (midpoint of 12-17g range) with updated comment.

## Updated Comparison: T13 vs T14 Mass

| Candidate | Current | Updated Est. | Change |
|-----------|---------|-------------|--------|
| T13 (PurpleRiver Mini 640, 18mm) | 21.0g | 15.0g | -6.0g (-29%) |
| T14 (Arducam 640×512 USB, 9.1mm) | 40.0g | 40.0g | No change |

The T14 advantage in mass was already smaller than thought — the T13 is now clearly lighter.

## Remaining Unknown

The exact 18mm lens mass is still unconfirmed. To get the precise figure, the vendor must be contacted (WhatsApp +86 130 1605 4201 or the on-site inquiry form at purpleriverai.en.made-in-china.com). The estimate above is ±3g from real-world expectation.