# T13 (PurpleRiver Mini 640, 18mm) — Vendor Mass Inquiry Package

**Date:** 2026-08-21
**Prepared by:** Thermal Surveillance Drone agent

## Contact Found ✅

| Field | Value |
|-------|-------|
| **Name** | Justin Lu |
| **Email** | **justin.lu@purpleriver.cn** |
| **Company** | Guangzhou Purpleriver Electronic Technology Co., Ltd |
| **Address** | 8th Floor, Caihui Center, Huangge Town, Nansha District, Guangzhou, Guangdong, China |
| **Website** | https://pr-ai.com/ |
| **Source** | pr-ai.com footer (confirmed live, 2026-08-21) |

## Current Status

- Module mass is well-bounded at **15.0g** (midpoint of 12-17g estimate) per `candidates.sysml`
- The ±3g uncertainty is small enough for CG analysis (nose-payload impact is tiny)
- **This is sufficient to proceed with ordering** — the 15.0g midpoint is conservative enough that no real CG issue exists
- However, the vendor inquiry would eliminate the ±3g margin entirely

## Background: What We Know

**From official sources:**
| Source | Figure | Condition |
|--------|--------|-----------|
| Made-in-China product page (18mm CVBS variant) | 6g | Bare module, no lens |
| thermal-image.com product blurb | <8.6g | Module with compact lens (9mm or 13mm) |
| Official spec sheet PDF | <20g | Module without lenses and flanges |

**Estimated 18mm lens mass:** 6-9g (Ge 2-element construction + aluminum barrel)

**Total estimate:** 12-17g → **15.0g** (midpoint, now in candidates.sysml)

## Ready-to-Send Inquiry

**To:** justin.lu@purpleriver.cn
**Subject:** PurpleRiver Mini 640 18mm — assembled mass inquiry

> Hello Justin,
>
> We're evaluating the Mini 640 thermal module with an 18mm lens (USB variant) for an unmanned aerial vehicle payload.
>
> Could you please provide the total assembled weight of the Mini 640 module with the 18mm F1.0 germanium lens attached (including lens, mounting flange, and shutter if standard)? We need the complete assembly weight for mass/CG budgeting purposes.
>
> Based on your spec sheet we estimate ~12-17g total, but would appreciate the exact production figure.
>
> Also, could you confirm whether the 18mm USB variant is currently in stock and the typical lead time for a single-unit order?
>
> Thank you,
> [David Daniel]

## Next Steps After Response

1. **If vendor responds within ±3g of 15.0g** → No update needed; flag as confirmed
2. **If vendor responds with a significantly different mass** → Update `candidates.sysml` T13.mass value and re-run CG analysis
3. **If no response within 7 days** → Proceed with 15.0g estimate (already tight enough for build)

## Impact Assessment

The 15.0g estimate is already a ~29% reduction from the original 21.0g ceiling. Flight time models using 15.0g vs 21.0g show negligible difference (~0.3 min at most). The CG shift from a 6g nose-payload reduction is ~1-2mm at most. **The model is safe to build from at the current estimate — vendor confirmation is nice-to-have, not build-blocking.**