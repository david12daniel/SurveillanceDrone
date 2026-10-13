#!/usr/bin/env python3
"""
verify_cdr_deck.py — Nightly pre-briefing deck verification for task #85.

Checks the CDR deck is in the state the briefing prep doc (cdr_briefing_prep.md)
requires before David presents to Lisa:

  1. Deck opens cleanly; slide count matches expectation (~30+).
  2. Slide 14 (System Composition): the 33 hand-drawn shapes (IDs 9-41) are
     GONE, exactly one picture (the graphviz system_composition render) is
     present, and the caption / title / footer text is preserved.
  3. The embedded image on slide 14 matches assets/diagrams/system_composition.png
     (byte-identical extraction) — i.e., it is the model-derived diagram.
  4. Picture placement does not overlap the caption text box.
  5. Deck has a backup (.bak.pptx) so the swap is reversible.
  6. Broad integrity: every ISLIDE/RELATIONSHIP resolves; no dangling image refs.
  7. Date-stamp integrity: every slide footer carries the SAME review date, and
     the stamped date matches build_cdr.py's CDR_DATE default (hard FAIL on drift).
     A stamp > 14 days old prints a loud WARNING (overdue review — David must
     re-set CDR_DATE when the meeting is actually scheduled).

Also flags the known hazard: build_cdr.py regenerates slide 14 from hand-drawn
shapes, so re-running it clobbers the picture swap.

Usage: python3 presentation/verify_cdr_deck.py [--deck PATH]
Exits 0 if all checks pass, 1 otherwise. Prints a PASS/FAIL per check.
"""

import argparse, hashlib, os, sys, zipfile
from pptx import Presentation
from lxml import etree

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECK = os.path.join(PROJ, "CDR_Thermal_Surveillance_Drone.pptx")
EXPECTED_IMAGE = os.path.join(PROJ, "presentation", "assets", "diagrams", "system_composition.png")

NS = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
}

# The 33 hand-drawn shapes removed by apply_slide14_diagram.py
OLD_SHAPE_IDS = set(range(9, 42))

results = []
def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))

def md5(path_or_bytes):
    h = hashlib.md5()
    if isinstance(path_or_bytes, bytes):
        h.update(path_or_bytes)
    else:
        with open(path_or_bytes, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--deck", default=DECK)
    args = ap.parse_args()

    if not os.path.exists(args.deck):
        check("deck exists", False, args.deck); sys.exit(1)

    # 0. Backup present?
    bak = args.deck + ".bak.pptx"
    check("backup .bak.pptx exists", os.path.exists(bak),
          os.path.basename(bak) + (f" ({os.path.getsize(bak):,} B)" if os.path.exists(bak) else " MISSING"))

    # 1. Open + slide count
    try:
        prs = Presentation(args.deck)
        n = len(prs.slides.__iter__.__self__._sldIdLst) if hasattr(prs.slides, '_sldIdLst') else len(list(prs.slides))
        check("deck opens cleanly", True, f"{n} slides")
    except Exception as e:
        check("deck opens cleanly", False, str(e)); sys.exit(1)

    slide14 = prs.slides[13]  # 0-indexed

    # 2. Legacy hand-drawn blocks gone? The old sysml_box/def_panel shapes
    # carried distinctive label text ("AerialObservationSystem", "Drone",
    # "GCS") and part names ("platform", "Airframe", ...). The diagram image
    # carries that content as pixels, so none of these may appear as shape text.
    # (Raw-ID checking is not used: fresh builds renumber shapes, and the
    # framed_image card rectangle legitimately lands in the old ID range.)
    legacy_markers = ["AerialObservationSystem", "Drone", "GCS",
                      "platform", "Airframe", "AntiSparkFilter",
                      "IRCamera", "SBCPayload", "RadioReceiver",
                      "viewingComputer", "TelemetryGroundLink", "UsbCap"]
    legacy_hits = []
    for s in slide14.shapes:
        if s.has_text_frame:
            t = s.text_frame.text
            if any(m in t for m in legacy_markers):
                legacy_hits.append(t[:60])
    check("slide14: legacy hand-drawn blocks removed", not legacy_hits,
          "no legacy labels" if not legacy_hits else f"found: {legacy_hits}")

    # 3. Exactly one picture on slide 14 + extract it
    pics = [s for s in slide14.shapes if s.shape_type == 13]  # PICTURE
    check("slide14: exactly one picture", len(pics) == 1, f"{len(pics)} picture(s)")
    emb_md5 = None
    if pics:
        pic = pics[0]
        # pull the image part via the relationship
        rId = pic._element.find('.//p:blipFill/a:blip', NS).get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
        img_part = slide14.part.related_part(rId)
        emb_bytes = img_part.blob
        emb_md5 = md5(emb_bytes)
        check("slide14: picture is system_composition.png", emb_md5 == md5(EXPECTED_IMAGE),
              f"embedded md5 {emb_md5[:12]}... vs source {md5(EXPECTED_IMAGE)[:12]}...")

        # 4. Placement sane: picture box vs caption box (caption at ML, 6.82in)
        from pptx.util import Emu
        left, top = pic.left, pic.top
        w, h = pic.width, pic.height
        right, bottom = left + w, top + h
        # caption textbox: ML x, Inches(6.82) y => find text box containing caption phrase
        caption_ok = True
        for s in slide14.shapes:
            if s.has_text_frame and "Block-definition" in s.text_frame.text:
                if s.top < bottom and s.top < top + h:  # overlap test (caption top below pic bottom expected)
                    if bottom > s.top:
                        caption_ok = False
        check("slide14: picture does not overlap caption", caption_ok,
              f"pic @ ({Emu(left).inches:.2f}\", {Emu(top).inches:.2f}\") size {Emu(w).inches:.2f}x{Emu(h).inches:.2f}\"")

        # 5. Title/footer text preserved
        all_text = " | ".join(s.text_frame.text for s in slide14.shapes if s.has_text_frame)
        check("slide14: title text preserved", "System Composition" in all_text, "")
    else:
        check("slide14: picture is system_composition.png", False, "no picture to compare")

    # 6. Zip integrity: every slide rel target exists inside the package
    try:
        bad = 0
        with zipfile.ZipFile(args.deck) as z:
            names = set(z.namelist())
            for name in names:
                if name.startswith("ppt/slides/_rels/") and name.endswith(".rels"):
                    root = etree.fromstring(z.read(name))
                    for rel in root:
                        tgt = rel.get("Target", "")
                        if not tgt.startswith("http") and not tgt.startswith("https"):
                            resolved = os.path.normpath(os.path.join(os.path.dirname(name).replace("_rels", ""), tgt))
                            # rels live in ppt/slides/_rels; targets are relative to ppt/slides
                            base = name.split("/_rels/")[0]
                            resolved = os.path.normpath(os.path.join(base, tgt))
                            if resolved not in names:
                                bad += 1
        check("package: all slide rel targets resolve", bad == 0, f"{bad} dangling")
    except Exception as e:
        check("package: all slide rel targets resolve", False, str(e))

    # 6b. Date-stamp integrity: every slide footer carries the SAME review date
    #     (build_cdr.py stamps CDR_DATE on all 41 footers + title + closing),
    #     and the stamped date matches what build_cdr.py would emit today.
    #     Inconsistent stamps = a partial edit in a 200KB generator = must fail.
    #     A date far in the past = overdue review = loud warning, not a fail
    #     (the date is a planned-review marker; only David can re-set it).
    import re as _re
    # footer stamp "CDR  ·  2026-07-26" (all content slides), title meta
    # "Review date  2026-07-26", and closing strip
    # "...Critical Design Review · 2026-07-26 · ..." (slide 41)
    stamp_re = _re.compile(r"(?:CDR|Critical Design Review)\s*·\s*(\d{4}-\d{2}-\d{2})")
    all_dates = []
    for sl in prs.slides:
        for s in sl.shapes:
            if s.has_text_frame:
                all_dates += stamp_re.findall(s.text_frame.text)
    # title-slide meta line uses "Review date  YYYY-MM-DD"
    for sl in [prs.slides[0]]:
        for s in sl.shapes:
            if s.has_text_frame:
                all_dates += _re.findall(r"Review date\s+(\d{4}-\d{2}-\d{2})", s.text_frame.text)
    uniq = sorted(set(all_dates))
    check("deck: all date stamps consistent", len(uniq) == 1,
          f"{len(all_dates)} stamps, dates: {uniq}" if len(uniq) != 1 else f"stamped {uniq[0]} ({len(all_dates)} occurrences)")
    if uniq:
        stamped = uniq[0]
        bpath = os.path.join(PROJ, "presentation", "build_cdr.py")
        gen_src = open(bpath, encoding="utf-8", errors="replace").read() if os.path.exists(bpath) else ""
        m = _re.search(r'CDR_DATE\s*=\s*os\.environ\.get\("CDR_DATE",\s*"(\d{4}-\d{2}-\d{2})"\)', gen_src)
        env_date = os.environ.get("CDR_DATE")
        # Effective generator date: env override wins (same logic as build_cdr.py),
        # else the file's default.
        src_date = env_date if env_date else (m.group(1) if m else None)
        if src_date and src_date != stamped:
            check("deck: stamped date matches build_cdr.py CDR_DATE", False,
                  f"deck {stamped} vs effective generator date {src_date} ({'env CDR_DATE' if env_date else 'file default'}) — rebuild the deck")
        else:
            check("deck: stamped date matches build_cdr.py CDR_DATE", True,
                  f"{stamped} == effective generator date {src_date}")
        try:
            import datetime as _dt
            age_days = (_dt.date.today() - _dt.date.fromisoformat(stamped)).days
            if age_days > 14:
                print(f"\nWARNING  deck stamped {stamped} — {age_days} days ago. If the review was "
                      f"re-scheduled, update CDR_DATE in presentation/build_cdr.py "
                      f"(e.g. CDR_DATE={_dt.date.today().isoformat()} python3 presentation/build_cdr.py) "
                      f"and rebuild before presenting.")
        except Exception:
            pass

    # 7. Hazard flag no longer applies to native rebuilds (build_cdr.py now
    #    emits the diagram itself), but detect if the generator regressed to the
    #    legacy hand-drawn slide-14 code.
    if os.path.exists(bpath):
        if "def_panel" in gen_src and "system_composition.png" in gen_src:
            print("NOTE  build_cdr.py still defines def_panel for other slides, but slide 14 "
                  "emits system_composition.png natively — rebuilds preserve the diagram. "
                  "If a rebuild ever reverts slide 14 to hand-drawn shapes, re-run "
                  "apply_slide14_diagram.py or fix build_cdr.py.")

    fails = [r for r in results if not r[1]]
    print(f"\n{'ALL CHECKS PASS' if not fails else f'{len(fails)} CHECK(S) FAILED'}")
    sys.exit(0 if not fails else 1)

if __name__ == "__main__":
    main()