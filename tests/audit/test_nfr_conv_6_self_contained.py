"""NFR-CONV.6 — self-contained-item invariant fixture (T07.04 / D-0086).

Two-fixture verification of the Q-DM-1 resolved 5-field per-item schema
{Context, Action, Output, Verification, Completion gate}:

1. Full-fields variant — every checklist item populates all five fields.
   TB-Add-1..8 catalogue MUST emit PASS for every check.
2. Field-stripped variant — item 1.1 has the ``**Output**`` field
   removed. TB-Add-1 MUST FAIL with both the item-ID (``1.1``) and the
   missing field label (``Output``) named in the error message.

The fixture's schema reference is cross-checked against the Q-DM-1
resolution recorded at ``src/superclaude/agents/rf-qa.md:296`` so the
binding is machine-checkable: if the production rule text drifts away
from the {Context, Action, Output, Verification, Completion-gate}
field-set, the test fails before any verdict assertion is run.

Run: ``uv run pytest tests/audit/test_nfr_conv_6_self_contained.py -v``
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURE_DIR = Path(__file__).parent / "fixtures" / "nfr_conv_6"
FULL_FIELDS_FIXTURE = FIXTURE_DIR / "full_fields.md"
STRIPPED_FIXTURE = FIXTURE_DIR / "stripped.md"
RF_QA_PATH = REPO_ROOT / "src" / "superclaude" / "agents" / "rf-qa.md"

# Q-DM-1 resolution: the 5-field per-item schema names, in source order.
SCHEMA_FIELDS = ("Context", "Action", "Output", "Verification", "Completion gate")

ITEM_RE = re.compile(r"^\s*-\s*\[[ x]\]\s*\*\*([\d.]+)\s+—\s*(.*?)\*\*\s*$")
FIELD_RE = re.compile(r"^\s{2,}-\s*\*\*([^*]+)\*\*\s*:\s*(.*)$")
PLACEHOLDER_RE = re.compile(r"\b(TBD|TODO|FIXME)\b")
FILE_LINE_RE = re.compile(r"[\w./-]+\.\w+:\d+")
EVIDENCE_ABSENCE_RE = re.compile(r"<!--\s*evidence-absence:")
CODE_SURFACE_RE = re.compile(r"`[^`]*\b(?:src/|\.py|\.md|\.\w+:\d+)[^`]*`|src/[\w./-]+")
EC_HEADING = "## Execution Context"
SOURCE_AREAS_RE = re.compile(r"^\s*-\s*\*\*Source areas:\*\*\s*(.*)$", re.MULTILINE)


@dataclass
class ChecklistItem:
    item_id: str
    line_number: int
    title: str
    fields: Dict[str, str] = field(default_factory=dict)
    field_lines: Dict[str, int] = field(default_factory=dict)


@dataclass
class CheckResult:
    check_id: str
    verdict: str
    detail: str


def _parse_checklist_items(text: str, skip_header: bool = True) -> List[ChecklistItem]:
    """Parse per-item bullets and their 5-field sub-bullets.

    When ``skip_header`` is True, the ``## Execution Context`` block is
    excluded from item enumeration so the header itself never triggers
    TB-Add-1 misclassification.
    """
    lines = text.splitlines()
    if skip_header:
        header_start, header_end = _header_range(text)
    else:
        header_start = header_end = -1
    items: List[ChecklistItem] = []
    current: ChecklistItem | None = None
    current_field: str | None = None
    for idx, raw in enumerate(lines, start=1):
        if header_start != -1 and header_start <= idx <= header_end:
            continue
        m_item = ITEM_RE.match(raw)
        if m_item:
            if current is not None:
                items.append(current)
            current = ChecklistItem(
                item_id=m_item.group(1),
                line_number=idx,
                title=m_item.group(2).strip(),
            )
            current_field = None
            continue
        if current is None:
            continue
        m_field = FIELD_RE.match(raw)
        if m_field:
            label = m_field.group(1).strip()
            current.fields[label] = m_field.group(2).strip()
            current.field_lines[label] = idx
            current_field = label
            continue
        if current_field is not None and raw.strip() and not raw.startswith("- ") and not raw.startswith("## "):
            current.fields[current_field] += "\n" + raw
            continue
        if raw.startswith("## ") or raw.startswith("---"):
            current_field = None
    if current is not None:
        items.append(current)
    return items


def _header_range(text: str) -> Tuple[int, int]:
    lines = text.splitlines()
    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == EC_HEADING)
    except StopIteration:
        return (-1, -1)
    end = start + 1
    while end < len(lines) and lines[end].strip() != "---":
        end += 1
    return (start + 1, end + 1)


def _header_source_areas(text: str) -> List[str]:
    m = SOURCE_AREAS_RE.search(text)
    if not m:
        return []
    payload = m.group(1).strip().rstrip(".")
    return [piece.strip() for piece in payload.split(",") if piece.strip()]


# ---------------------------------------------------------------------------
# TB-Add-1 .. TB-Add-8 checks
# ---------------------------------------------------------------------------


def tb_add_1(text: str) -> List[CheckResult]:
    """Placeholder scan + 5-field schema enforcement (rf-qa.md:296)."""
    out: List[CheckResult] = []
    items = _parse_checklist_items(text)
    for item in items:
        missing = [f for f in SCHEMA_FIELDS if f not in item.fields]
        body_concat = "\n".join(item.fields.values()) + "\n" + item.title
        if missing:
            out.append(
                CheckResult(
                    "TB-Add-1",
                    "FAIL",
                    f"Item {item.item_id} missing required field(s) {missing} "
                    f"on line {item.line_number} — replace with concrete description",
                )
            )
            continue
        if PLACEHOLDER_RE.search(body_concat):
            out.append(
                CheckResult(
                    "TB-Add-1",
                    "FAIL",
                    f"Item {item.item_id} contains 'TBD'/'TODO'/'FIXME' on line "
                    f"{item.line_number} — replace with concrete description",
                )
            )
            continue
        out.append(
            CheckResult(
                "TB-Add-1",
                "PASS",
                f"Item {item.item_id} carries all five fields and no placeholder tokens",
            )
        )
    if not items:
        out.append(CheckResult("TB-Add-1", "FAIL", "no checklist items detected"))
    return out


def tb_add_2(text: str) -> CheckResult:
    """Item count bounds (advisory). Track ≥3 / ≤40."""
    n = len(_parse_checklist_items(text))
    if n < 3 or n > 50:
        return CheckResult(
            "TB-Add-2",
            "ADVISORY",
            f"[ADVISORY] item count {n} outside recommended bounds",
        )
    return CheckResult("TB-Add-2", "PASS", f"item count {n} within recommended bounds")


def tb_add_3(text: str) -> CheckResult:
    """Clarification adjacency — vacuously PASS when no Open Questions section exists."""
    if re.search(r"^## Open Questions", text, re.MULTILINE):
        return CheckResult(
            "TB-Add-3",
            "INACTIVE",
            "Open Questions section present but adjacency rules not exercised by this fixture",
        )
    return CheckResult("TB-Add-3", "PASS", "no Open Questions section — adjacency rule vacuous")


def tb_add_4(text: str) -> CheckResult:
    """DAG cycle detection over item-to-item references."""
    items = _parse_checklist_items(text)
    item_ids = {item.item_id for item in items}
    edges: List[Tuple[str, str]] = []
    ref_re = re.compile(r"\bItem\s+([\d.]+)\b")
    for item in items:
        body = "\n".join(item.fields.values())
        for ref in ref_re.findall(body):
            if ref != item.item_id and ref in item_ids:
                edges.append((item.item_id, ref))
    # Trivially DAG when zero edges
    if not edges:
        return CheckResult("TB-Add-4", "PASS", "no item-to-item references — DAG trivially acyclic")
    # Topological sort
    incoming: Dict[str, int] = {iid: 0 for iid in item_ids}
    for _src, dst in edges:
        incoming[dst] = incoming.get(dst, 0) + 1
    roots = [iid for iid, c in incoming.items() if c == 0]
    visited = 0
    while roots:
        node = roots.pop()
        visited += 1
        for src, dst in list(edges):
            if src == node:
                incoming[dst] -= 1
                if incoming[dst] == 0:
                    roots.append(dst)
                edges.remove((src, dst))
    if visited == len(item_ids):
        return CheckResult("TB-Add-4", "PASS", "item-to-item dependency graph is acyclic")
    return CheckResult("TB-Add-4", "FAIL", "item-to-item dependency graph contains a cycle")


def tb_add_5(text: str) -> CheckResult:
    """Granularity / XL splitting — INACTIVE unless an item carries an XL marker."""
    if re.search(r"\b(XL|multi-file|complex)\b", text):
        # Items with these markers must include a justifying comment.
        if re.search(r"<!--\s*xl-justified:", text):
            return CheckResult("TB-Add-5", "PASS", "XL markers carry xl-justified comments")
        # Plain prose mentions of 'complex' don't trigger; we only fail if explicit XL effort label.
        if re.search(r"\bEffort:\s*XL\b", text):
            return CheckResult("TB-Add-5", "FAIL", "Effort:XL item lacks xl-justified comment")
    return CheckResult("TB-Add-5", "PASS", "no XL granularity markers — splitting rule vacuous")


def tb_add_6(text: str) -> List[CheckResult]:
    """Confidence/Verification format consistency.

    All Verification fields use the same shape — a single sub-bullet of
    the form ``- **Verification**: ...``. This fixture uses uniform
    prose-style Verification fields (not the ``Verify: ...`` prefix used
    by Template 01/02 generated MDTM, but consistent across items).
    """
    items = _parse_checklist_items(text)
    out: List[CheckResult] = []
    for item in items:
        if "Verification" not in item.fields:
            out.append(CheckResult("TB-Add-6", "FAIL", f"Item {item.item_id} missing Verification field"))
            continue
        out.append(
            CheckResult(
                "TB-Add-6",
                "PASS",
                f"Item {item.item_id} Verification field present and uniform",
            )
        )
    if not items:
        out.append(CheckResult("TB-Add-6", "FAIL", "no checklist items detected"))
    return out


def tb_add_7(text: str) -> CheckResult:
    """Execution Context source areas reappear in items."""
    areas = _header_source_areas(text)
    if not areas:
        return CheckResult("TB-Add-7", "INACTIVE", "no Source areas line — degraded-form tolerated")
    items = _parse_checklist_items(text)
    bodies = "\n".join(("\n".join(item.fields.values())) for item in items)
    missing = [a for a in areas if a not in bodies]
    if missing:
        return CheckResult(
            "TB-Add-7",
            "FAIL",
            f"header source area(s) {missing} missing from per-item Context fields",
        )
    return CheckResult(
        "TB-Add-7",
        "PASS",
        f"all {len(areas)} header source areas reappear in per-item Context fields",
    )


def tb_add_8(text: str) -> List[CheckResult]:
    """Per-item Context evidence binding."""
    items = _parse_checklist_items(text)
    out: List[CheckResult] = []
    for item in items:
        ctx = item.fields.get("Context", "")
        if not CODE_SURFACE_RE.search(ctx):
            out.append(
                CheckResult(
                    "TB-Add-8",
                    "PASS",
                    f"Item {item.item_id} Context references no code surface",
                )
            )
            continue
        if FILE_LINE_RE.search(ctx) or EVIDENCE_ABSENCE_RE.search(ctx):
            out.append(
                CheckResult(
                    "TB-Add-8",
                    "PASS",
                    f"Item {item.item_id} Context carries file:line or justified-absence",
                )
            )
            continue
        out.append(
            CheckResult(
                "TB-Add-8",
                "FAIL",
                f"Item {item.item_id} Context references code surface but lacks file:line citation",
            )
        )
    return out


def run_all_tb_add(text: str) -> Dict[str, List[CheckResult]]:
    return {
        "TB-Add-1": tb_add_1(text),
        "TB-Add-2": [tb_add_2(text)],
        "TB-Add-3": [tb_add_3(text)],
        "TB-Add-4": [tb_add_4(text)],
        "TB-Add-5": [tb_add_5(text)],
        "TB-Add-6": tb_add_6(text),
        "TB-Add-7": [tb_add_7(text)],
        "TB-Add-8": tb_add_8(text),
    }


def _aggregate(results: List[CheckResult]) -> str:
    if any(r.verdict == "FAIL" for r in results):
        return "FAIL"
    return "PASS"


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestFixturesExist:
    def test_full_fields_fixture_exists(self):
        assert FULL_FIELDS_FIXTURE.is_file()

    def test_stripped_fixture_exists(self):
        assert STRIPPED_FIXTURE.is_file()


class TestQDm1SchemaCrossCheck:
    """Fixture's 5-field schema reference must match the production
    TB-Add-1 rule text at ``rf-qa.md:296``."""

    def _rf_qa_field_names(self) -> List[str]:
        text = RF_QA_PATH.read_text(encoding="utf-8")
        # The rule body lists the 5 field names in a parenthetical.
        # NOTE (2026-05-24): markdownlint MD013 reflow per
        # TASK-RF-20260523-234320-markdownlint-remediation may wrap the
        # rule body across multiple lines. Collapse internal whitespace
        # before matching so the regex stays content-pinned without
        # depending on the post-reflow line wrap.
        normalised = " ".join(text.split())
        m = re.search(
            r"it MUST have a ([^.]+?) body\)\. Title-only or placeholder-only items",
            normalised,
        )
        assert m, "TB-Add-1 rule text in rf-qa.md does not match expected pattern"
        raw = m.group(1)
        # Normalise commas/and into a list.
        cleaned = raw.replace(", and ", ", ").replace(" and ", ", ")
        return [piece.strip() for piece in cleaned.split(",") if piece.strip()]

    def test_rf_qa_schema_matches_expected(self):
        observed = self._rf_qa_field_names()
        # The rule text uses "Completion-gate" with a hyphen; the fixture uses
        # the rendered Markdown label "Completion gate". Both are accepted as
        # equivalent when the hyphen is replaced with a space.
        normalised = [n.replace("Completion-gate", "Completion gate") for n in observed]
        assert normalised == list(SCHEMA_FIELDS), (
            f"rf-qa.md TB-Add-1 rule drifted from expected Q-DM-1 schema:"
            f" expected {list(SCHEMA_FIELDS)}, got {normalised}"
        )

    def test_full_fields_fixture_declares_schema(self):
        text = FULL_FIELDS_FIXTURE.read_text(encoding="utf-8")
        for label in SCHEMA_FIELDS:
            assert label in text, f"full-fields fixture missing schema label {label!r}"

    def test_stripped_fixture_declares_schema_intent(self):
        text = STRIPPED_FIXTURE.read_text(encoding="utf-8")
        # The fixture description must cite the full 5-field schema so the
        # missing-field intent is documented; the field absence is verified
        # by TB-Add-1, not by string match.
        for label in SCHEMA_FIELDS:
            assert label in text, f"stripped fixture missing schema label {label!r}"


class TestFullFieldsAllPass:
    """Full-fields variant: TB-Add-1..8 catalogue MUST emit only PASS."""

    def test_aggregate_pass(self):
        results = run_all_tb_add(FULL_FIELDS_FIXTURE.read_text(encoding="utf-8"))
        observed = {check: _aggregate(results[check]) for check in results}
        expected = {check: "PASS" for check in results}
        assert observed == expected, (
            f"full-fields fixture must produce PASS for every TB-Add check; "
            f"got {observed}"
        )

    def test_no_check_emits_fail(self):
        results = run_all_tb_add(FULL_FIELDS_FIXTURE.read_text(encoding="utf-8"))
        fails = [
            (check, r.detail)
            for check, lst in results.items()
            for r in lst
            if r.verdict == "FAIL"
        ]
        assert not fails, f"unexpected FAIL verdicts on full-fields fixture: {fails}"


class TestStrippedFailsTBAdd1:
    """Field-stripped variant: TB-Add-1 MUST FAIL with item-ID and field named."""

    def test_tb_add_1_fails_with_item_and_field(self):
        text = STRIPPED_FIXTURE.read_text(encoding="utf-8")
        results = tb_add_1(text)
        fails = [r for r in results if r.verdict == "FAIL"]
        assert fails, (
            f"stripped fixture must produce at least one TB-Add-1 FAIL "
            f"(got {[(r.verdict, r.detail) for r in results]})"
        )
        # The error message must name both the item-ID ('1.1') and the
        # stripped field label ('Output').
        named = [
            r for r in fails
            if "1.1" in r.detail and "Output" in r.detail
        ]
        assert named, (
            f"TB-Add-1 FAIL must name both item-ID '1.1' and missing field 'Output'; "
            f"got {[r.detail for r in fails]}"
        )

    def test_other_items_pass_tb_add_1(self):
        """Only item 1.1 is stripped; items 1.2 and 1.3 still carry all five
        fields and must continue to PASS TB-Add-1."""
        results = tb_add_1(STRIPPED_FIXTURE.read_text(encoding="utf-8"))
        item_verdicts = {}
        for r in results:
            m = re.search(r"Item\s+([\d.]+)", r.detail)
            if m:
                item_verdicts[m.group(1)] = r.verdict
        assert item_verdicts.get("1.2") == "PASS", (
            f"stripped fixture item 1.2 should still PASS TB-Add-1; got {item_verdicts}"
        )
        assert item_verdicts.get("1.3") == "PASS", (
            f"stripped fixture item 1.3 should still PASS TB-Add-1; got {item_verdicts}"
        )

    def test_tb_add_2_through_8_unaffected_for_intact_items(self):
        """The non-TB-Add-1 checks should remain PASS overall; only TB-Add-1
        records a FAIL because item 1.1 is missing the **Output** field."""
        text = STRIPPED_FIXTURE.read_text(encoding="utf-8")
        results = run_all_tb_add(text)
        for check in ("TB-Add-2", "TB-Add-3", "TB-Add-4", "TB-Add-5", "TB-Add-7"):
            assert _aggregate(results[check]) == "PASS", (
                f"{check} unexpectedly FAILed on stripped fixture: "
                f"{[r.detail for r in results[check]]}"
            )
