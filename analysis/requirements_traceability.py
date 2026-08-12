"""
Requirements traceability matrix, generated from model.sysml.

SysON's Requirements Table view can't show cross-requirement traceability yet
(no relationship columns, no traceability-matrix feature — see the "Traceability
features" stub in its docs). This script derives the same information directly
from the model text and writes it to analysis/requirements_traceability.csv.

Two relationships are captured, both real SysML v2 constructs already in
model.sysml (not inferred):
  - `subsets`   : requirement -> parent requirement it decomposes (e.g.
                  R3_CAM_FOV subsets R3). This is the "traces up to" link.
  - `satisfy`   : structural or behavioral element -> requirement it fulfills
                  (e.g. part def Battery satisfies R4_BAT_VOLT; action flyRoute
                  satisfies R1_BHV_ALT_HOLD). Inverted here to requirement ->
                  satisfying element(s). Elements considered: part def, action
                  def, state def, and nested part/action/state usages.

The V&V half of the matrix (the VCRM) is joined in from
analysis/verification_methods.csv, which is the hand-authored engineering
judgement that model.sysml does not carry: how each requirement is verified
(I/A/D/T), at what level, under which V&V case, against what quantified
success criterion, at which gate, and its status as of CDR.

That side-car is the ONE file to hand-edit. The join is checked both ways and
raises on any mismatch, so a requirement added to model.sysml without a
verification method is a hard error rather than a silent hole in the VCRM.

Output columns: requirement_id, package, doc_summary, phase, subsets_parent,
subsets_root, satisfied_by, method, level, vv_case, gate, status_at_cdr,
success_criterion.

Never hand-edit the CSV — rerun this script after model.sysml or
verification_methods.csv changes.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parent.parent / "model.sysml"
OUTPUT_PATH = Path(__file__).resolve().parent / "requirements_traceability.csv"
VERIFICATION_PATH = Path(__file__).resolve().parent / "verification_methods.csv"

# Columns joined in from verification_methods.csv, in output order.
VERIFICATION_FIELDS = ["method", "level", "vv_case", "gate", "status_at_cdr", "success_criterion"]

_PACKAGE_RE = re.compile(r"\bpackage\s+(\w+)\s*\{")
_REQUIREMENT_RE = re.compile(r"\brequirement\s+(\w+)\s*\{")
# Any def or usage that can host a `satisfy` statement: part def/action def/
# state def, plus nested `part`/`action`/`state` usages (e.g. `action flyRoute {`).
# Order matters — the two-word alternatives must be tried before their
# single-word counterparts so `part def X` isn't parsed as a bare `part`.
_SATISFIER_RE = re.compile(
    r"\b(?:part def|action def|state def|part|action|state)\s+(\w+)\s*(?::\s*[\w:]+)?\s*\{"
)
_DOC_RE = re.compile(r"doc\s*/\*(.*?)\*/", re.DOTALL)
_SUBSETS_RE = re.compile(r"\bsubsets\s+(\w+)\s*;")
_SATISFY_RE = re.compile(r"\bsatisfy\s+(\w+)\s*;")
_PHASE_RE = re.compile(r"@PhaseTag\s*\{\s*phase\s*=\s*Phase::(\w+)\s*;")


def _block_end(text: str, open_brace_index: int) -> int:
    """Given the index of a block's opening '{', return the index of its matching '}'."""
    depth = 0
    i = open_brace_index
    n = len(text)
    while i < n:
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    raise ValueError("unbalanced braces")


def _innermost_span_name(pos: int, spans: list[tuple[int, int, str]]) -> str:
    """Return the name from the smallest (start, end, name) span containing pos."""
    best_name, best_size = "", None
    for start, end, name in spans:
        if start <= pos <= end:
            size = end - start
            if best_size is None or size < best_size:
                best_name, best_size = name, size
    return best_name


def _find_package_spans(text: str) -> list[tuple[int, int, str]]:
    spans = []
    for m in _PACKAGE_RE.finditer(text):
        brace = text.index("{", m.end() - 1)
        end = _block_end(text, brace)
        spans.append((m.start(), end, m.group(1)))
    return spans


def parse_requirements(text: str, package_spans: list[tuple[int, int, str]]) -> dict[str, dict]:
    requirements: dict[str, dict] = {}
    for m in _REQUIREMENT_RE.finditer(text):
        req_id = m.group(1)
        brace = text.index("{", m.end() - 1)
        end = _block_end(text, brace)
        body = text[brace + 1 : end]

        doc_match = _DOC_RE.search(body)
        doc_summary = " ".join(doc_match.group(1).split()) if doc_match else ""

        phase_match = _PHASE_RE.search(body)
        phase = phase_match.group(1) if phase_match else ""

        parents = _SUBSETS_RE.findall(body)

        requirements[req_id] = {
            "package": _innermost_span_name(m.start(), package_spans),
            "doc_summary": doc_summary,
            "phase": phase,
            "subsets_parent": ", ".join(parents),
        }
    return requirements


def _find_satisfier_spans(text: str) -> list[tuple[int, int, str]]:
    """Every part def/action def/state def or nested part/action/state usage, as (start, end, name)."""
    spans = []
    for m in _SATISFIER_RE.finditer(text):
        brace = text.index("{", m.end() - 1)
        end = _block_end(text, brace)
        spans.append((m.start(), end, m.group(1)))
    return spans


def parse_satisfy_map(text: str, satisfier_spans: list[tuple[int, int, str]]) -> dict[str, list[str]]:
    """Return {requirement_id: [satisfier_name, ...]} inverted from `satisfy` statements.

    Each `satisfy` is attributed to its *innermost* enclosing satisfier block, so a
    `satisfy` nested inside `action flyRoute { ... }` (itself inside `action def
    ExecuteSurveillance`) is attributed to `flyRoute`, not the outer action def.
    """
    satisfied_by: dict[str, list[str]] = {}
    for m in _SATISFY_RE.finditer(text):
        req_id = m.group(1)
        name = _innermost_span_name(m.start(), satisfier_spans)
        if name:
            satisfied_by.setdefault(req_id, []).append(name)
    return satisfied_by


def resolve_root(req_id: str, requirements: dict[str, dict]) -> str:
    """Walk subsets links to the top-level (no-parent) requirement."""
    seen = set()
    current = req_id
    while True:
        parents = requirements.get(current, {}).get("subsets_parent", "")
        if not parents:
            return current
        parent = parents.split(", ")[0]
        if parent in seen or parent not in requirements:
            return current
        seen.add(parent)
        current = parent


def load_verification(requirement_ids: set[str]) -> dict[str, dict]:
    """Load the VCRM side-car and check it covers exactly the modeled requirements.

    Verification coverage is the whole point of a cross-reference matrix, so both
    directions are errors: a requirement with no verification method would be a
    silent hole in the VCRM, and a verification row with no requirement means the
    side-car is referring to something the model no longer has.
    """
    with VERIFICATION_PATH.open(newline="", encoding="utf-8") as f:
        rows = {r["requirement_id"]: r for r in csv.DictReader(f)}

    missing = sorted(requirement_ids - rows.keys())
    orphaned = sorted(rows.keys() - requirement_ids)
    problems = []
    if missing:
        problems.append(
            f"{len(missing)} requirement(s) in model.sysml have no verification method: "
            + ", ".join(missing)
        )
    if orphaned:
        problems.append(
            f"{len(orphaned)} row(s) in {VERIFICATION_PATH.name} match no requirement: "
            + ", ".join(orphaned)
        )
    for req_id, row in sorted(rows.items()):
        blank = [c for c in VERIFICATION_FIELDS if not (row.get(c) or "").strip()]
        if blank:
            problems.append(f"{req_id}: empty {', '.join(blank)}")
    if problems:
        raise SystemExit(
            "VCRM coverage check failed — fix "
            f"{VERIFICATION_PATH.name}:\n  - " + "\n  - ".join(problems)
        )
    return rows


def main() -> None:
    text = MODEL_PATH.read_text(encoding="utf-8")
    package_spans = _find_package_spans(text)
    requirements = parse_requirements(text, package_spans)
    satisfier_spans = _find_satisfier_spans(text)
    satisfied_by = parse_satisfy_map(text, satisfier_spans)

    verification = load_verification(set(requirements))

    rows = []
    for req_id in sorted(requirements):
        info = requirements[req_id]
        row = {
            "requirement_id": req_id,
            "package": info["package"],
            "doc_summary": info["doc_summary"],
            "phase": info["phase"],
            "subsets_parent": info["subsets_parent"],
            "subsets_root": resolve_root(req_id, requirements) if info["subsets_parent"] else "",
            "satisfied_by": ", ".join(sorted(satisfied_by.get(req_id, []))),
        }
        row.update({c: verification[req_id][c] for c in VERIFICATION_FIELDS})
        rows.append(row)

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "requirement_id",
                "package",
                "doc_summary",
                "phase",
                "subsets_parent",
                "subsets_root",
                "satisfied_by",
            ]
            + VERIFICATION_FIELDS,
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} requirements to {OUTPUT_PATH}")
    print(f"VCRM coverage: {len(rows)}/{len(rows)} requirements carry a verification method")
    by_status: dict[str, int] = {}
    for r in rows:
        by_status[r["status_at_cdr"]] = by_status.get(r["status_at_cdr"], 0) + 1
    for status, count in sorted(by_status.items(), key=lambda kv: -kv[1]):
        print(f"  {count:3d}  {status}")


if __name__ == "__main__":
    main()
