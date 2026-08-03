# CAD / 3D-model resources & modeling pathway

Resources for building a 3D CAD model of the **integration** (mounting the SBC +
thermal camera + battery on the locked **iFlight Chimera9 ECO** airframe) so the
"does it physically fit" question (see [`MODEL_ISSUES.md`](../MODEL_ISSUES.md) §C16)
moves from estimate to a measured, printable mount.

**Reality (verified 2026-06-29, web search):** none of the three locked components
has a ready-made, official **STEP/3D file** published online. You will *build or
commission* the models. The good news — authoritative **dimensions** for all three
are recorded below, so the models are buildable without further research.

Selections this supports: see [`SELECTED_COMPONENTS.md`](../SELECTED_COMPONENTS.md).

---

## 1. Recommended free CAD tool

| Tool | Cost / license | Best for | Caveats |
|---|---|---|---|
| **FreeCAD 1.0** ⭐ primary | Fully free / open-source, offline, no account | Parametric mechanical parts, STEP **import + export**, 3D-print STL | Steeper learning curve; use the **Part Design** + **Assembly** (built-in in 1.0) workbenches |
| **Onshape (Free)** | Free *if documents are public* | Easiest assemblies, browser-based, full STEP/STL export | Free tier makes docs public (fine for this non-secret project) |
| **Autodesk Fusion (Personal)** | Free for hobby use | FPV-community favorite, lots of mount tutorials | Licensing tier shifts; neutral-format **export is restricted** on the free tier |
| Tinkercad | Free, browser | Quick blocky keep-out solids only | Not precise/parametric enough for the final mount |

**Recommendation:** **FreeCAD 1.0** — truly free, imports the community STEP files
below, and exports both STEP (to share with your other AI / vendors) and STL (to
print). Onshape Free is the gentlest on-ramp if FreeCAD feels heavy.

---

## 2. Per-component CAD resources

### A. iFlight Chimera9 ECO — airframe (`AF3a` / `AF3b`)
- **Official 3D/STEP:** none. iFlight's [official 3D-file library](https://iflightrc.freshdesk.com/support/solutions/48000400496) has no Chimera9 (only Nazgul/iH3/Defender/MegaBee).
- **Official doc:** **Chimera9 ECO Frame Assembly Guide PDF** — on the [frame-kit page](https://shop.iflight.com/Chimera9-ECO-Frame-Kit-Pro2080) (`C015262-...-20231215.pdf`; download tab / `download_id=347`). **NB (verified 2026-07-28): this is an *exploded assembly diagram + bill-of-materials only* — NOT a dimensioned drawing. It has no to-scale orthographic plate view and no hole-coordinate table, so you CANNOT trace a plate outline from it.** What it *is* good for: the fastener/standoff BOM (M3×20 & M3×30 Al standoffs, 3×5×8 double-pass standoffs, stack screws → tells you available stack heights + thread sizes) and the plate stack-up / part layout. Get the actual plate outline via **calipers on the real frame**, a **community STEP donor** (below), or a **parametric approximation from the key dims** (further below). Local copy: [`Chimera9_ECO_Frame_Assembly_Guide.pdf`](Chimera9_ECO_Frame_Assembly_Guide.pdf).
- **Adaptable community models (same Chimera design language):**
  - [iFlight Chimera 7" frame replica — **STEP source** (MakerWorld)](https://makerworld.com/en/models/739796-iflight-chimera-7-inch-frame-replica)
  - [Chimera 7 Pro V2 GoPro/payload mount (Printables)](https://www.printables.com/model/385547-iflight-chimera-7-pro-v2-gopro-9-10-11-mount) — good SBC-deck starting point
  - [GrabCAD iFlight tag](https://grabcad.com/library/tag/iflight) (iFlight XL5 V3, HL7 LR frames) · [Cults3D iFlight](https://cults3d.com/en/tags/iflight) · [Printables iFlight](https://www.printables.com/tag/iflight)
- **Verified dimensions (from the frame-kit page):** wheelbase **405 mm**; overall **L360 × W235 × H34 mm**; arm **6 mm**; plates top **2 mm** / bottom **3 mm** / upper **3 mm**; **max flight-stack height 21 mm**; max VTX height **30 mm**; stack pattern **30.5 × 30.5 mm (φ3)**; VTX 30.5/25/20; motor 16×16 / 19×19 (φ3).

### B. NanoPi M5 — SBC (`SBC3`)
- **Official 3D/STEP:** none published. The [FriendlyELEC NanoPi M5 wiki](https://wiki.friendlyelec.com/wiki/index.php/NanoPi_M5) hosts the **PCB dimensional drawing + mounting-hole layout** (read the hole coords here) and the [schematic PDF](https://wiki.friendlyelec.com/wiki/images/9/97/NanoPi_M5_LP5_2411_SCH.pdf) (connector positions). FriendlyELEC also sells an official CNC case (CAD may be available on request).
- **Community:** [GrabCAD "nanopi"](https://grabcad.com/library/tag/nanopi) and [Thingiverse "nanopi"](https://www.thingiverse.com/tag:nanopi) exist but have **no confirmed M5** model (NEO/R-series only).
- **Verified dimensions:** PCB **90 × 62 mm**; passive heatsink (fan header present) → allow **~15–25 mm** vertical clearance above the board for heatsink + tall USB/HDMI/GPIO. Pull the exact 4 mounting-hole coordinates (typically M2.5) from the wiki drawing or by calipering the board.

### C. PurpleRiver Mini 640 — thermal camera (`T13`)
- **Official 3D/STEP:** none public; available only via **OEM/ODM request** (vendor pre-sales WhatsApp +86 130 1605 4201).
- **Official doc:** [Mini 640 specifications PDF](https://www.thermal-image.com/download/purpleriver-mini640-thermal-camera-specifications/) (≈140 KB).
- **Verified dimensions** (iRay OEM drawing — see [`iRay_MINI_384-640_Module_Manual_V1.10.pdf`](iRay_MINI_384-640_Module_Manual_V1.10.pdf)): core body **21 × 21 mm** (±0.10), depth ~8–10.3 mm, **< 20 g** core; **8 × M2 tapped holes** (4 front + 4 rear) on an **18.40 mm** pattern; Ø21 front lens boss; rear 50-pin Hirose DF40C-50DP. Lens options 4–75 mm — **T13 uses the 18 mm lens** (SELECTED 2026-07-29, was 13 mm). Overall with lens ≈ **21 × 21 × ~34 mm** (~24 mm barrel — estimate, caliper). Full spec: [`mini640_t13_cad_spec.md`](mini640_t13_cad_spec.md).

### D. Battery — `BAT09` Lumenier 6S 12 Ah Amprius / `BAT10` Upgrade Energy 6S3P 12 Ah
- No CAD needed — model as a **keep-out box** for strap routing / clearance:
  `BAT09` ≈ **125 × 40 × 70 mm**, ~920 g; `BAT10` ≈ **110 × 35 × 65 mm**, ~919 g (envelopes per [`candidates.sysml`](../candidates.sysml); BAT04 4S pack 80×45×70 is the one vendor-confirmed datapoint).

---

## 3. Full modeling pathway (FreeCAD 1.0)

Goal: a **printable SBC/payload deck** (and a nose bracket for the thermal cam)
that bolts to the Chimera9 ECO and is verified to fit. You do **not** need a perfect
frame model — you need the *mounting interface* (the 30.5 × 30.5 stack pattern +
standoff tops) plus each component's footprint and keep-out volume.

**Phase 0 — Setup**
1. Install **FreeCAD 1.0** (free). Edit → Preferences → General → Units → **mm**.
2. Make one project folder; save as `chimera9_integration.FCStd`.

**Phase 1 — Build the component bodies** (Part Design workbench; one Body each)
1. **Frame top-plate fixture:** the Assembly Guide PDF is an exploded/BOM view (no
   to-scale outline — see §2A), so **don't try to trace it.** Build the mounting
   reference from what you actually have: sketch the **30.5 × 30.5 stack hole pattern**
   (φ3) at the origin — that is the real bolt interface for the deck — inside a plate
   **envelope** approximated from the key dims (overall **360 × 235 mm**, wheelbase
   **405 mm**). **Pad** to 2 mm. Refine the true plate outline + exact hole positions
   later from **calipers on the real frame** or a **community STEP donor** (§2A). Add 4
   **standoff posts** at the stack pattern up to the 21 mm stack height as the deck's
   attachment points. (For the mount deliverable the stack pattern + envelope is what
   matters; the decorative plate edge is clearance context only.)
2. **NanoPi M5:** Pad a **90 × 62 × 1.6 mm** PCB; add the 4 mounting holes (coords
   from the wiki drawing); Pad a **keep-out box ~90 × 62 × 25 mm** above it for the
   heatsink + connectors. (For mount design the keep-out box is what matters.)
3. **Mini 640:** Pad a **21 × 21 × 21 mm** body + a Ø~14 mm × (lens) cylinder = nose unit.
4. **Battery:** Pad a keep-out box (125 × 40 × 70 for BAT09).

**Phase 2 — Assemble** (Assembly workbench, new in FreeCAD 1.0)
1. Insert the frame fixture as the **fixed/grounded** part.
2. Position the battery (Chimera9 is **top-mount** → on the top plate), then place the
   **SBC keep-out on a raised tier above the battery** (the §C16 "raised tier"
   verdict), and the thermal unit at the **nose**, tilted ~15–25°.
3. Check clearances: 9" prop disc, arms, **VTX ≤ 30 mm height**, stack ≤ 21 mm.

**Phase 3 — Design the mount** (the actual deliverable)
1. New Body "SBC_deck". Sketch a base that bolts to the **30.5 × 30.5** stack /
   standoff tops; Pad up to clear the battery; add **standoff bosses** matching the
   SBC's mounting holes (M2.5 + heat-set insert); add a **fan duct / vents** (the
   SBC dumps ~10 W — passive needs airflow); add a **nose bracket** for the Mini 640.
2. Make heights **parametric** (a spreadsheet of `deck_clearance`, `standoff_h`,
   `fan_dia`) so you can tune for cooling/clearance without re-sketching.

**Phase 4 — Validate fit** (the CAD version of the §C16 check)
1. Part → **Check geometry / Section view**, or Measure, to confirm no interference:
   SBC fits the ~110 × 70 usable deck (8 mm spare per §C16), clears VTX/arms, battery
   strap routes cleanly.

**Phase 5 — Export & print**
1. Mount Body → **Export STEP** (archive / share) **and STL** (slice).
2. Print in **PETG / ABS / ASA / nylon** — heat-tolerant + vibration-resistant near a
   10 W SBC and the motors; **avoid PLA** (softens). 3–4 walls, 30–40 % infill.

**Phase 6 — Iterate from measurements**
1. Caliper the real frame plate, SBC holes, and cam; update the parametric model and
   the EST deck dims in [`candidates.sysml`](../candidates.sysml) (→ sharpens the §C16
   fit numbers from estimate to measured); reprint.

---

## 4. Quick links (copy/paste)
- Chimera9 ECO frame kit + assembly PDF: https://shop.iflight.com/Chimera9-ECO-Frame-Kit-Pro2080
- Chimera 7" frame STEP (adapt): https://makerworld.com/en/models/739796-iflight-chimera-7-inch-frame-replica
- Chimera GoPro/payload mount: https://www.printables.com/model/385547-iflight-chimera-7-pro-v2-gopro-9-10-11-mount
- NanoPi M5 wiki (dimensional drawing): https://wiki.friendlyelec.com/wiki/index.php/NanoPi_M5
- NanoPi M5 schematic PDF: https://wiki.friendlyelec.com/wiki/images/9/97/NanoPi_M5_LP5_2411_SCH.pdf
- Mini 640 specs PDF: https://www.thermal-image.com/download/purpleriver-mini640-thermal-camera-specifications/
- FreeCAD: https://www.freecad.org/  · Onshape: https://www.onshape.com/en/products/free
