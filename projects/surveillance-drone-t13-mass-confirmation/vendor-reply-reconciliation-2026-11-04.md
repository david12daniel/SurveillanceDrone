# T13 vendor reply — reconciliation and resolution plan

**Date:** 2026-11-04 (nightly, task 2.1 / #39)
**Vendor message:** Gmail id `1a158dc0ced11c0a`, received 2026-10-20 06:29 local
(`Tue, 20 Oct 2026 18:29:26 +0800`), from **Zowen Gu `<zowen.gu@zichuan-tech.com>`**
(Guangzhou Purpleriver Electronic Technology Co., Ltd), subject
*"Mini 640 thermal module with an 18mm lens (USB variant)"*.
**Our outbound inquiry:** Gmail id `1a1551328fc097e5`, sent 2026-10-19 to
`justin.lu@purpleriver.cn` — a different address on a different domain.

## 0. Why this sat unprocessed for 15 days

Every nightly since 2026-10-19 searched the mailbox for `purpleriver` / `justin.lu`
and concluded "vendor has not replied" (Oct 24: "still unanswered after 5 days",
Oct 28: "9 days, no reply"). The reply arrived from **zichuan-tech.com**, not
`purpleriver.cn`, and the subject does not contain the word "PurpleRiver". Searching
`purpleriver` today still does **not** return it; only `from:(zichuan-tech.com OR
purpleriver...)` finds it.

**Lesson for future nightlies: search vendor replies by the *product* string
("Mini 640"), not by the address we mailed.** The vendor is the same company —
`zichuan-tech.com` is the trading/marketing domain; `purpleriver.cn` is the technical
contact.

## 1. What the vendor actually said

Verbatim (whitespace normalised):

> This model belongs to our MINI2 series. It supports thermal imaging but cannot
> output detailed temperature data. I have measured the product as requested.
> 1. Weight: 0.27kg  2. Dimension: 21mm*21mm  3. Lens: 18mm
> If you require detailed temperature data, we recommend our MINI1 series.
> Please provide information for the mounting flange and other required accessories.
> … delivery quantity … destination country … freight forwarder

Attachments (4 PNGs, saved to `vendor-reply-2026-10-20/att0–3.png`): two website
navigation strips ("Mini Series / LTC6 Module / 1280 Module / Phone Thermal /
Car/Truck Thermal"), and two product photos. OCR is text-only, so the photos need a
human eyeball — see §6.

## 2. Vendor figures vs the model

| Attribute | Model (`candidates.sysml` T13) | Vendor reply | Delta / status |
|---|---|---|---|
| Mass | 15.0 g (12–17 g estimate, midpoint) | **0.27 kg = 270 g** | **+255 g, 18× the model** |
| Dimensions | 21 × 21 × ~34 mm | 21 × 21 mm | Consistent with the bare core |
| Lens | 18 mm | 18 mm | ✅ Confirmed |
| Radiometric output | `radiometric = true` | "cannot output detailed temperature data" → **non-radiometric** | **Contradiction** |
| Product family | "Mini 640" (`thermal-image.com` product page) | "MINI2 series" | Mismatch in naming |

Two of the three numbers he "measured" agree with our model (footprint, lens), which
argues this *is* our module — but 270 g is physically implausible for a 21 × 21 mm
uncooled core whose own product page says **6 g without lens** and whose PDF spec sheet
says **< 20 g without lenses and flanges**.

## 3. Hypotheses, ranked

**H1 — Unit slip: he meant 0.027 kg = 27 g (most likely).**
27 g sits exactly where a *complete* deliverable should land: ~6 g core + ~6–9 g
18 mm Ge lens + ~8–12 g of housing/connector board/USB pigtail. It also fits the
21 × 21 mm footprint claim. A bare "0.27" typed where "0.027" was meant is a common
transcription error in a second-language email, and the same message states dimensions
that only make sense for the small core.

**H2 — He weighed an integrated (housed) SKU from the MINI2 line, not our core.**
The reply opens by re-identifying the product as "our MINI2 series" and steering us to
a different series for temperature data, i.e. he may have quoted/measured a different
catalogue item than the one in our inquiry URL. If so, 270 g is the *housed camera*
number and says nothing about our core.

**H3 — 270 g includes packaging/accessories** (flange, cable, box). Also plausible, and
if true the flight-relevant mass is still unknown.

**Ruled out:** that 270 g is the bare module + 18 mm lens. No 21 × 21 mm LWIR core
weighs 270 g; the vendor's own two published sources say otherwise.

## 4. Impact if 270 g were true

Both numbers below come from the live model, not hand arithmetic.

**CG shift** (`python3 analysis/t13_mass_cg.py --new-mass-g 270`):

```
ΔCG: +21.94 mm (arm 150) / +29.26 mm (arm 200) / +36.57 mm (arm 250) @ 1743 g AUW
VERDICT: SIGNIFICANT — exceeds the ±10 mm tolerance class; do NOT apply without a
         full mass/CG re-check (task 2.11).
```

**AUW / endurance** (new tool, `python3 analysis/t13_mass_endurance_sensitivity.py`):

| T13 mass | AUW | ΔAUW | Hover | Δ hover | Throttle | Verdict |
|---|---|---|---|---|---|---|
| 15.0 g (model) | 1744 g | — | 58.7 min | — | 14.9 % | baseline |
| 23.9 g (worst case already analysed) | 1753 g | +9 g | 58.3 min | −0.4 min | 14.9 % | acceptable |
| **270 g (vendor claim)** | **1999 g** | **+255 g** | **48.5 min** | **−10.2 min** | 17.0 % | **FAILS R3_CAM_WT (200 g cap)** |

Read together:

- **The aircraft still closes.** At 270 g the build is 1999 g AUW, 48.5 min hover —
  still clears R6 (30 min) and R9 (30 acres) with room to spare, and the 9 in frame's
  5145 g payload cap is nowhere near binding.
- **But R3_CAM_WT is breached** (`camera subsystem ≤ 200 g`). 270 g is over by 70 g
  before the mount bracket. That is a requirements problem, not a model tweak.
- **CG moves outside the tolerance class** (+20…+37 mm forward), so the battery would
  have to move aft or the nose arm shorten — a mechanical change to the S2 deck work.

Precedent exists for handling this: R3_CAM_COST already carries a documented
"NOT MET — waiver required" line (720 USD cap vs 700 USD as-purchased). R3_CAM_WT
can be handled the same way **if** the 270 g figure survives clarification — but a
waiver should not be raised on an unverified number.

## 5. Radiometric contradiction — requirement-neutral, model-wrong

`candidates.sysml` sets `T13.radiometric = true`, inherited from the 2026-10-14
finding that "the radiometric version only offers 9/13/18 mm lenses". The vendor now
says the 18 mm USB unit **cannot output detailed temperature data**.

Checked every requirement that could care (`model.sysml` CameraRequirements):

| Requirement | Text | Needs temperature data? |
|---|---|---|
| R3 | detect/classify heat signatures vs a 5 °C target background | No — imagery only |
| R3_CAM_NETD | NETD ≤ 50 mK | No — sensitivity, not calibration |
| R3_CAM_RES / FOV / WT / PWR / COST / IF | pixels, swath, mass, draw, cost, interface | No |

**No requirement demands radiometric (calibrated °C) output.** Detection and
classification (R3.1/R3.2, and the D1 YOLO pipeline) run on the 8-bit/16-bit image,
not on per-pixel temperature. So a non-radiometric 18 mm unit is **compliant** — the
model flag is simply over-specified.

Proposed (not applied tonight): set `T13.radiometric = false` with a comment recording
the vendor statement, and note that calibrated temperature output, if ever wanted
(e.g. species discrimination by body temperature), points at the vendor's **MINI1**
series — which would be a new candidate, new price, new mass, and a new task.

## 6. Decision I recommend (and what I need from David)

**Recommendation: do not touch `T13.mass` yet.** Applying 270 g on the strength of an
internally inconsistent email would corrupt the baseline, the CG analysis, the deck
and the flight-time table for a number that is most likely a typo. Instead, send one
clarification email — the draft is below, ready to paste.

Two things only David can do:

1. **Send the clarification email** (external send, so I have drafted but not sent it).
2. **Eyeball the two photos** in `vendor-reply-2026-10-20/att2.png` and `att3.png`.
   If either shows a scale/display reading, that settles H1 vs H2 immediately. I can
   OCR text but cannot see images.

If the answer comes back and it is not 27-ish g, this task becomes a design decision
(R3_CAM_WT waiver or camera re-selection), not a data-entry task.

## 7. Draft clarification email (reply-all to Zowen, cc justin.lu)

> **Subject:** Re: Mini 640 thermal module with an 18mm lens (USB variant) — three clarifications
>
> Hello Zowen,
>
> Thank you for measuring the module, and for the note about the temperature output.
> I need to reconcile your figures with the published specifications before I can
> place the order, because three points do not yet agree:
>
> 1. **Weight.** You measured 0.27 kg (270 g). Your product page lists the Mini 640
>    module at about 6 g without lens, and your PDF spec sheet says "less than 20 g
>    without lenses and flanges". Could you confirm whether 0.27 kg (a) is the weight
>    of the bare module **with** the 18 mm lens and nothing else, (b) includes a
>    housing, flange or cable, or (c) was a reading of 0.027 kg (27 g)? A photo of the
>    module alone on the scale with the display visible would settle it.
> 2. **Product identity.** You described this as the MINI2 series. My inquiry was for
>    the module on this page: `<product URL>`, described there as "Mini 640". Please
>    confirm the exact model number and part number of the unit you measured
>    (21 × 21 mm, 18 mm lens, USB output, 640 × 512, 25 Hz).
> 3. **Radiometric output.** We do not need calibrated temperature; we need 640 × 512
>    LWIR video at about 25 Hz over USB (UVC). Please confirm the 18 mm USB unit
>    delivers that, and tell me whether a radiometric 18 mm option exists in the same
>    form factor, in case we add temperature measurement later.
>
> Once those are clear I will confirm quantity (1 unit for evaluation, with a second
> unit likely), destination (United States), and shipping preference. The mounting
> flange is our own design; I will send the interface drawing separately.
>
> Best regards,
> David Laperriere

## 8. If/when the real number arrives

```bash
python3 analysis/t13_mass_cg.py --new-mass-g <n>            # CG impact + paste-ready edit
python3 analysis/t13_mass_endurance_sensitivity.py --masses 15,<n>   # AUW/endurance impact
```
Then apply the printed `:>> mass = …` edit in `candidates.sysml`, regenerate the export,
update TASKS.md row 2.1, and if the number exceeds 200 g raise the R3_CAM_WT question
before touching the deck (slide 26 camera card and slide 30 GSD tables both assume the
15 g nose payload only indirectly — verify with `presentation/verify_cdr_deck.py`).

## 9. Artefacts from tonight

- `analysis/t13_mass_endurance_sensitivity.py` — new, reusable: thermal mass → AUW,
  hover endurance, throttle, R6/R3_CAM_WT verdicts, reusing the model's own
  `evaluate()`; reproduces the published baseline (C000008, 1744 g, 58.7 min) exactly.
- `projects/surveillance-drone-t13-mass-confirmation/vendor-reply-2026-10-20/att0–3.png`
  — the four vendor attachments, preserved with the message.
- `candidates.sysml` — T13 comment updated: reply received, figures disputed, mass
  **unchanged** at 15.0 g, radiometric question flagged.
- `TASKS.md` row 2.1 — history appended.
