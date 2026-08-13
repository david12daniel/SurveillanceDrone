# cad-resources — downloaded files + generated CAD

Resources pulled from [`cad-resources.md`](cad-resources.md) (2026-07-28).

## Downloaded (official docs, direct links)
| File | Source | Notes |
|---|---|---|
| `Chimera9_ECO_Frame_Assembly_Guide.pdf` | shop.iflight.com Chimera9 ECO frame-kit page (download_id=347) | 2.7 MB. **Exploded assembly diagram + BOM only — NOT a dimensioned drawing** (no traceable plate outline). Useful for the fastener/standoff BOM + stack-up; get the plate outline via calipers or a community STEP donor. See §2A in cad-resources.md. |
| `NanoPi M5 - FriendlyELEC WiKi.pdf` | wiki.friendlyelec.com (full wiki page, user-saved) | 12 MB. Hardware spec + **labeled top/bottom layout diagrams** (pp.5-7). Board 90×62×1.6 confirmed; connector edges labeled. NB: labeled diagram only — **no dimensioned hole coordinates**. |
| `NanoPi_M5_schematic.pdf` | wiki.friendlyelec.com (`NanoPi_M5_LP5_2411_SCH.pdf`) | 1.1 MB. Connector nets. |
| `PurpleRiver_Mini640_specs.pdf` | thermal-image.com download-manager | 131 KB. Lite one-page spec sheet. |
| `PurpleRiver_Mini640_Mini2_specifications.pdf` | thermal-image.com (`.../mini2-purpleriver-mini640-...`) | 449 KB, 11 pp. Fuller rebrand manual — spec, pinout, and a **mechanical drawing (§5)** but embedded low-res (508×351 px, callouts blurry). Superseded by the iRay original below. |
| `iRay_MINI_384-640_Module_Manual_V1.10.pdf` ⭐ | liberal-technology.com (iRay/Raytron OEM manual V1.10) | 1.5 MB, 25 pp. **The authoritative source.** §6 mechanical drawing embedded at 1183×810 px — callouts legible. Title block = `WN640_384_9.1mm Assembly` (OEM core = Raytron/iRay **WN640**). See extracted dims in [`mini640_t13_cad_spec.md`](mini640_t13_cad_spec.md). |

## Generated — parametric CAD models
Built from the resources above (see the `*_cad_spec.md` files for the extracted dims).

**NanoPi M5 (SBC3)** — from `nanopi_m5_cad_spec.md`:
| File | Notes |
|---|---|
| `nanopi_m5.py` | **build123d** script → parametric model. Datum = bottom-left PCB corner. Uncertain values (hole inset/dia, keep-out heights) are labeled variables to confirm with calipers. |
| `nanopi_m5.step` | PCB solid (90×62×1.6) + 4 mounting holes. Verified: exact bbox, 4 holes Ø2.7. |
| `nanopi_m5_with_keepout.step` | PCB + top (22 mm) / bottom (5 mm) clearance boxes for the §C16 fit check. |
| `nanopi_m5.stl` | PCB only, for quick viewing / slicing. |

**Mini 640 / T13 thermal camera** — from `mini640_t13_cad_spec.md` (mounting interface is EXACT off the iRay drawing; lens barrel is an estimate):
| File | Notes |
|---|---|
| `mini640_t13.py` | **build123d** script. Datum = center of REAR mounting face; camera views +Z. EXACT: 21×21 body, 8× M2 blind holes on the 18.40 pattern (4 front + 4 rear). ESTIMATE (caliper): core depth, **18 mm** lens Ø/length. |
| `mini640_t13.step` | Camera solid: body + Ø20 **18 mm** lens barrel + 8× M2 holes. Verified bbox 21×21×34.3, 8 blind holes. |
| `mini640_t13_with_keepout.step` | + rear DF40 connector box + lens-sweep clearance. |
| `mini640_t13.stl` | Body+lens, quick view. |

**Thermal-camera nose mount** ("beak", v1) — bolts the T13 to the Chimera9 top-plate front, camera aimed at **NADIR** (straight down). **SUPERSEDED 2026-08-07 (TASKS.md 2.8)** by the 45° variant below — kept for reference only, do not build this one. The claim this section originally made ("any tilt breaks the R3_1/R3_2 pixel budget") turned out to be wrong: the 18 mm lens still recognizes at 45° (thin but passing, 4.17 px along-range @90 m — see `model.sysml` `OffNadirGsd`, 2026-08-12), which is why the tilt was chosen instead:
| File | Notes |
|---|---|
| `thermal_mount.py` | **build123d** beak bracket. EXACT camera interface (4× M2 clearance on 18.40 + DF40 cutout, camera hangs lens-down). PARAMETRIC/caliper: `FRAME_BOLT_PITCH` (assumed 30.5 side-by-side), `BEAK_LEN`. |
| `thermal_mount.step` / `.stl` | The printable bracket (42.5 × 51.2 × 3 mm flat plate). |
| `thermal_mount_with_camera.step` | Assembly: bracket + camera bolted lens-down (nadir) — for fit visualisation. |
| `thermal_mount_preview.png` | 3D preview render of the assembly. |

> **v1 open items:** frame-side bolt pattern is *assumed* (caliper the real top-plate front); flat cantilever may need a stiffening rib/gusset; consider soft-mount grommets for vibration; verify the lens tip (~31 mm below the plate) clears the bottom plate / landing gear.

**Thermal-camera nose mount — 45° DOWNLOOK variant** (v1) — aims the camera forward-and-down at 45° off-nadir (valid with the **18 mm** lens, which recognizes at 45°; see [`../analysis/thermal_detection_offnadir_analysis.md`](../analysis/thermal_detection_offnadir_analysis.md)):
| File | Notes |
|---|---|
| `thermal_mount_45.py` | **build123d**, `TILT_DEG=45` parametric. Same top-plate-front attach + EXACT camera interface (4× M2 @ 18.40 + DF40 cutout); adds a 45° camera face + support gusset. Lens verified at (0, +0.71, −0.71) = 45° forward-down. |
| `thermal_mount_45.step` / `.stl` | The printable 45° bracket. |
| `thermal_mount_45_with_camera.step` | Assembly with the camera at 45°. |
| `thermal_mount_45_preview.png` | 3D preview (side view shows the lens parallel to a 45° guide). |

> **v1 open items (45°):** same frame-bolt caveat; the bracket is chunky (crude box gusset + the camera-face plate over-extends above the bolt line) — a v2 could trim the face to the hole footprint and use clean triangular side-gussets; check the camera (extends ~+47 mm forward, ~−23 mm down) clears props/arms and landing.

**Regenerate:** `python nanopi_m5.py` / `python mini640_t13.py` / `python thermal_mount.py` (needs `pip install build123d`).
Two environment gotchas hit on this Windows machine (both handled/noted, not script bugs):
1. build123d scans system fonts at import and crashes on one corrupt font → the script installs a `fontTools` shim to skip it.
2. The **global** Python's `numpy`/`pandas`/`sklearn` are ABI-mismatched (pre-existing), and build123d hard-imports sklearn → `import build123d` fails there. Run instead from the isolated venv created for this: **`C:\Users\Josiah Laperriere\b123\Scripts\python.exe nanopi_m5.py`** (or make a fresh venv). The venv is disposable — delete `~/b123` anytime.

## NOT downloaded — require a (free) account login on the host site
These platforms gate STL/STEP downloads behind sign-in and block automated requests,
so they must be pulled manually with a browser + account:

- **iFlight Chimera 7" frame replica — STEP** — https://makerworld.com/en/models/739796-iflight-chimera-7-inch-frame-replica (MakerWorld account)
- **Chimera 7 Pro V2 GoPro/payload mount — STL** — https://www.printables.com/model/385547-iflight-chimera-7-pro-v2-gopro-9-10-11-mount (Printables account)

No official STEP/3D file exists for any of the three locked components (verified in
the reference doc) — build from the dimensions recorded there.
