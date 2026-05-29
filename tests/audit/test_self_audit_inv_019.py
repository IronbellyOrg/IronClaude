"""TEST-009 — Self-Audit / INV-019 fixture (R-065 / FR-CONV.3 PR-04).

Phase-3 / T03.14 deliverable (D-0037). Asserts the consumer-side INV-019
contract landed by T03.04 (D-0029 §6 / `## Self-Audit Schema Requirement`
at rf-qa-qualitative.md:823-889) and T03.10 (D-0034 "Handling the
Inherited Structural Verdict" + `## Self-Audit` output-schema block at
rf-qa-qualitative.md:893-964):

1. The literal `## Self-Audit` heading appears at or after line 794 in
   both the source-of-truth ``src/superclaude/agents/rf-qa-qualitative.md``
   and the ``.claude/agents/rf-qa-qualitative.md`` mirror (AC-1 in the
   phase-3-tasklist; line-794 floor per T03.04 spec).
2. The schema mandates BOTH category-(a) reliance bullets AND ≥1
   category-(b) independent semantic check (AC-2).
3. The INV-019 enforcement rule (zero category-(b) = violation) is
   documented (AC-3).
4. A synthetic emitted report with category-(b) ≥ 1 detector pattern
   passes the inflation check; a negative-case variant with zero
   category-(b) bullets is flagged INV-019-positive by the audit recipe
   (AC-4 — negative case MUST fail detection).

Acceptance reference (phase-3-tasklist.md L683-687):
- ``uv run pytest tests/audit/test_self_audit_inv_019.py -v`` exits 0.
- Fixture verifies ≥1 documented semantic check is present.
- Evidence at ``TASKLIST_ROOT/artifacts/D-0037/evidence.md``.
- A fixture variant with 0 semantic checks fails (verifies negative case).

The detection commands the K-003 audit window uses (D-0029 §6) are
ported as `_self_audit_present` and `_count_category_b_bullets`. The
negative-case test calls them on a synthetic zero-semantic-check report
and asserts the inflation flag fires — i.e., the audit recipe rejects
the inflation-positive output.

Run: ``uv run pytest tests/audit/test_self_audit_inv_019.py -v``
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

AGENT_SRC = REPO_ROOT / "src" / "superclaude" / "agents" / "rf-qa-qualitative.md"
AGENT_MIRROR = REPO_ROOT / ".claude" / "agents" / "rf-qa-qualitative.md"

LITERAL_SELF_AUDIT_HEADING = "## Self-Audit"
SCHEMA_HEADING = "## Self-Audit Schema Requirement (INV-019, K-003 Audit-Target)"
TEMPLATE_HEADING = "## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)"
HANDLING_HEADING = "## Handling the Inherited Structural Verdict"

# Two semantic-check detector patterns recognised by the K-003 audit
# recipe (D-0029 §6 detection command (2) + the embedded Output Format
# template at rf-qa-qualitative.md:728-733). Either form counts as a
# category-(b) bullet for INV-019 purposes — TEST-009 accepts both.
SEMANTIC_CHECK_PATTERNS = (
    re.compile(r"semantic counterpart verified", re.IGNORECASE),
    re.compile(r"verified by .+:\d+", re.IGNORECASE),
)

LINE_794_FLOOR = 794


# ---------------------------------------------------------------------------
# Synthetic emitted reports — positive + negative variants.
# ---------------------------------------------------------------------------

POSITIVE_REPORT = """# QA Report — task-qualitative

**Topic:** TASK-DEMO
**Date:** 2026-05-17
**Phase:** task-qualitative
**Fix cycle:** N/A

## Overall Verdict: PASS

## Items Reviewed
| # | Check | Result | Axis (PR-07) | Evidence |
|---|-------|--------|--------------|----------|
| 1 | scope coherence | PASS | drift | TASK-DEMO.md:12-40 |

## Summary
- Checks passed: 1 / 1
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0

## Issues Found
None.

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)
- Relied on rf-qa PASS for TB-Add-1 -> semantic counterpart verified: Read TASK-DEMO.md:12-40 confirmed scope matches BUILD-REQUEST.
- Relied on rf-qa PASS for TB-Add-3 -> semantic counterpart verified: grep -n "Clarification adjacency" TASK-DEMO.md returned items 4, 7 referencing OQ-1.

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- Relied on rf-qa PASS for TB-Add-1
- Relied on rf-qa PASS for TB-Add-3

**(b) Independent semantic checks (≥1 required, INV-019):**
- scope coherence — verified by Read TASK-DEMO.md:12-40 (semantic counterpart verified against BUILD-REQUEST scope clause)
- clarification adjacency content — verified by Read TASK-DEMO.md:40-60 (semantic counterpart verified — OQ refs resolve to live questions)

## QA Complete
"""

NEGATIVE_REPORT_NO_CATEGORY_B = """# QA Report — task-qualitative

**Topic:** TASK-DEMO-NEG
**Date:** 2026-05-17
**Phase:** task-qualitative
**Fix cycle:** N/A

## Overall Verdict: PASS

## Items Reviewed
| # | Check | Result | Axis (PR-07) | Evidence |
|---|-------|--------|--------------|----------|
| 1 | scope coherence | PASS | n/a | (relied on rf-qa) |

## Summary
- Checks passed: 1 / 1
- Checks failed: 0

## Issues Found
None.

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- Relied on rf-qa PASS for TB-Add-1
- Relied on rf-qa PASS for TB-Add-2
- Relied on rf-qa PASS for TB-Add-3
- Relied on rf-qa PASS for TB-Add-4

**(b) Independent semantic checks (≥1 required, INV-019):**
(none — inflation-positive: this run is an INV-019 violation)

## QA Complete
"""

NEGATIVE_REPORT_NO_HEADING = """# QA Report — task-qualitative

**Topic:** TASK-DEMO-NEG-2
**Date:** 2026-05-17
**Phase:** task-qualitative
**Fix cycle:** N/A

## Overall Verdict: PASS

## Items Reviewed
| # | Check | Result | Axis (PR-07) | Evidence |
|---|-------|--------|--------------|----------|
| 1 | scope coherence | PASS | n/a | (relied on rf-qa) |

## Summary
- Checks passed: 1 / 1

## Issues Found
None.

## QA Complete
"""


# ---------------------------------------------------------------------------
# Audit-recipe helpers — port of D-0029 §6 detection commands.
# ---------------------------------------------------------------------------


def _self_audit_present(report: str) -> bool:
    """D-0029 §6 detection command (1) — Self-Audit heading present?

    Either the literal ``## Self-Audit`` heading OR the embedded template
    realisation (``## Inherited Structural Verdict — Reliance Audit
    (PR-04, INV-019)``) is accepted, matching the equivalence statement
    at rf-qa-qualitative.md:944-951.
    """
    for line in report.splitlines():
        stripped = line.rstrip()
        if stripped == LITERAL_SELF_AUDIT_HEADING:
            return True
        if stripped == TEMPLATE_HEADING:
            return True
    return False


def _self_audit_span(report: str) -> str:
    """Return the slice of ``report`` from the first Self-Audit heading
    through (exclusive of) the next top-level ``## `` heading.
    """
    lines = report.splitlines()
    start = -1
    for idx, line in enumerate(lines):
        stripped = line.rstrip()
        if stripped == LITERAL_SELF_AUDIT_HEADING or stripped == TEMPLATE_HEADING:
            start = idx
            break
    if start == -1:
        return ""
    end = start + 1
    while end < len(lines) and not lines[end].startswith("## "):
        end += 1
    return "\n".join(lines[start:end])


def _count_category_b_bullets(report: str) -> int:
    """D-0029 §6 detection command (2) — count category-(b) bullets in
    the Self-Audit span. A bullet counts when it (i) is a list item
    (``- `` prefix after any indent) AND (ii) matches a semantic-check
    detector pattern (``semantic counterpart verified`` OR
    ``verified by <file>:<line>``).

    The embedded Output Format template's one-bullet-per-line form
    (``- Relied on ... -> semantic counterpart verified: ...``) counts
    as 1 category-(b) bullet per matching bullet — TEST-009 accepts the
    template form as schema-conformant per rf-qa-qualitative.md:944-951.
    """
    span = _self_audit_span(report)
    if not span:
        return 0
    count = 0
    for raw in span.splitlines():
        line = raw.lstrip()
        if not line.startswith("- "):
            continue
        if any(p.search(line) for p in SEMANTIC_CHECK_PATTERNS):
            count += 1
    return count


def _inflation_positive(report: str) -> bool:
    """Return True iff the report fails the K-003 audit (INV-019 violation):

    1. Self-Audit heading absent, OR
    2. zero category-(b) bullets in the Self-Audit span.
    """
    if not _self_audit_present(report):
        return True
    return _count_category_b_bullets(report) < 1


# ---------------------------------------------------------------------------
# Static schema checks — guards against accidental regression of the
# T03.04 spec section + T03.10 consumer-side wiring + sync parity.
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def src_text() -> str:
    return AGENT_SRC.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def mirror_text() -> str:
    return AGENT_MIRROR.read_text(encoding="utf-8")


def _line_of(path: Path, predicate) -> int:
    for idx, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if predicate(line):
            return idx
    return -1


class TestSelfAuditHeadingPresent:
    """The literal ``## Self-Audit`` heading is present at or after line
    794 (AC-1; phase-3-tasklist.md L684) in both source and mirror."""

    def test_agent_source_exists(self):
        assert AGENT_SRC.is_file(), (
            f"missing source rf-qa-qualitative.md at {AGENT_SRC}"
        )

    def test_agent_mirror_exists(self):
        assert AGENT_MIRROR.is_file(), (
            f"missing mirror rf-qa-qualitative.md at {AGENT_MIRROR}"
        )

    def test_self_audit_heading_at_or_after_line_794_source(self):
        line = _line_of(
            AGENT_SRC, lambda raw: raw.rstrip() == LITERAL_SELF_AUDIT_HEADING
        )
        assert line >= LINE_794_FLOOR, (
            f"AC-1 violated: literal `## Self-Audit` heading at line {line} in source "
            f"(< {LINE_794_FLOOR}). Phase-3 tasklist requires ≥ {LINE_794_FLOOR}."
        )

    def test_self_audit_heading_at_or_after_line_794_mirror(self):
        line = _line_of(
            AGENT_MIRROR, lambda raw: raw.rstrip() == LITERAL_SELF_AUDIT_HEADING
        )
        assert line >= LINE_794_FLOOR, (
            f"AC-1 violated: literal `## Self-Audit` heading at line {line} in mirror "
            f"(< {LINE_794_FLOOR}). Phase-3 tasklist requires ≥ {LINE_794_FLOOR}."
        )

    def test_schema_requirement_heading_present(self, src_text: str):
        """T03.04 EOF section (D-0029) — schema requirement heading exists."""
        assert SCHEMA_HEADING in src_text, (
            f"T03.04 spec section heading missing from {AGENT_SRC}: {SCHEMA_HEADING!r}"
        )

    def test_handling_heading_present(self, src_text: str):
        """T03.10 EOF append (D-0034) — `## Handling the Inherited Structural
        Verdict` consumer-handling section is present."""
        assert HANDLING_HEADING in src_text, (
            f"T03.10 consumer-handling section heading missing from {AGENT_SRC}: "
            f"{HANDLING_HEADING!r}"
        )

    def test_template_realisation_heading_present(self, src_text: str):
        """Embedded Output Format template carries the template-form heading
        (T03.01 landed this; T03.04 spec cites it as the canonical realisation)."""
        assert TEMPLATE_HEADING in src_text, (
            f"Output Format template heading missing from {AGENT_SRC}: {TEMPLATE_HEADING!r}"
        )


class TestSelfAuditSchemaBothCategoriesRequired:
    """The schema MANDATES both category-(a) reliance bullets AND ≥1
    category-(b) semantic check (AC-2; phase-3-tasklist.md L685)."""

    def test_category_a_label_present(self, src_text: str):
        assert (
            "Reliance list — rf-qa PASS items skipped for structural re-check"
            in src_text
        ), "category-(a) label missing from rf-qa-qualitative.md schema block"

    def test_category_b_label_present(self, src_text: str):
        assert "Independent semantic checks (≥1 required, INV-019)" in src_text, (
            "category-(b) label missing from rf-qa-qualitative.md schema block"
        )

    def test_inv019_enforcement_rule_documented(self, src_text: str):
        """D-0029 §6 audit recipe — zero category-(b) = INV-019 violation."""
        assert "zero entries" in src_text.lower() or "zero category-(b)" in src_text, (
            "INV-019 zero-category-(b) violation rule not documented at EOF spec section"
        )
        # The literal sentence from the schema requirement section.
        assert "INV-019 violation" in src_text, (
            "literal 'INV-019 violation' phrase missing — enforcement rule not stated"
        )


class TestSelfAuditMirrorParity:
    """Source and mirror are byte-identical (sync invariant)."""

    def test_source_and_mirror_byte_identical(self, src_text: str, mirror_text: str):
        assert src_text == mirror_text, (
            "rf-qa-qualitative.md source and `.claude/` mirror diverged — "
            "run `make sync-dev`."
        )


# ---------------------------------------------------------------------------
# Audit-recipe behaviour: positive + negative variants of an emitted report.
# ---------------------------------------------------------------------------


class TestAuditRecipePositiveCase:
    """A conformant report (Self-Audit heading + ≥1 category-(b) bullet)
    passes the K-003 inflation check (AC-2 positive: ≥1 semantic check
    present)."""

    @pytest.fixture
    def report(self) -> str:
        return POSITIVE_REPORT

    def test_self_audit_heading_detected(self, report: str):
        assert _self_audit_present(report), (
            "audit recipe failed to detect `## Self-Audit` heading in conformant report"
        )

    def test_category_b_count_at_least_one(self, report: str):
        count = _count_category_b_bullets(report)
        assert count >= 1, (
            f"AC-2 violated: conformant report has {count} category-(b) bullets; "
            "expected ≥ 1 (INV-019 floor). Detector patterns: "
            f"{[p.pattern for p in SEMANTIC_CHECK_PATTERNS]}"
        )

    def test_not_inflation_positive(self, report: str):
        assert _inflation_positive(report) is False, (
            "false-positive in K-003 audit recipe: conformant report flagged as "
            "inflation-positive"
        )

    def test_template_realisation_also_counts(self, report: str):
        """The embedded template form ('Relied on ... -> semantic counterpart
        verified: ...') also satisfies category-(b)."""
        # The positive report has 2 template-form bullets in the
        # `## Inherited Structural Verdict — Reliance Audit` section
        # AND 2 dedicated `## Self-Audit` bullets. The category-(b)
        # count over the first Self-Audit span MUST be ≥ 1; the span
        # function only inspects the first Self-Audit-style heading,
        # which appears as the template-form heading first.
        count = _count_category_b_bullets(report)
        assert count >= 1, (
            "template-form bullets failed to register as category-(b) — "
            "TEST-009 equivalence rule (rf-qa-qualitative.md:944-951) regressed"
        )


class TestAuditRecipeNegativeCase:
    """The negative-case variant (zero category-(b) bullets) MUST fail
    the audit recipe — AC-4 (phase-3-tasklist.md L687, validation note
    L690-691: 'reviewer confirms negative-case variant fails')."""

    @pytest.fixture
    def report(self) -> str:
        return NEGATIVE_REPORT_NO_CATEGORY_B

    def test_self_audit_heading_still_detected(self, report: str):
        """Negative case still has the heading — the failure mode is the
        empty category-(b), not a missing heading."""
        assert _self_audit_present(report), (
            "negative-case fixture construction error: heading absent (should be "
            "present so the failure mode isolates to zero category-(b) bullets)"
        )

    def test_category_b_count_zero(self, report: str):
        """Zero category-(b) bullets — the inflation-positive condition."""
        count = _count_category_b_bullets(report)
        assert count == 0, (
            f"AC-4 negative-case violated: expected 0 category-(b) bullets, got {count}. "
            "Fixture's NEGATIVE_REPORT_NO_CATEGORY_B has accidentally acquired a "
            "matching bullet."
        )

    def test_inflation_positive_flag_fires(self, report: str):
        """The audit recipe MUST flag this report as inflation-positive
        (INV-019 violation). This is the affirmative form of AC-4 'fixture
        variant with 0 semantic checks fails'."""
        assert _inflation_positive(report) is True, (
            "AC-4 violated: K-003 audit recipe did NOT flag the zero-semantic-check "
            "variant as inflation-positive. INV-019 enforcement broken."
        )

    def test_negative_case_documents_failure(self, report: str):
        """Sanity guard: the negative fixture explicitly labels itself as an
        INV-019 violation (prevents future maintainers from accidentally
        'fixing' it)."""
        assert "INV-019 violation" in report, (
            "negative-case fixture lost its self-documenting marker"
        )


class TestAuditRecipeMissingHeading:
    """A second negative variant: Self-Audit heading absent entirely.
    The audit recipe MUST flag this as inflation-positive as well
    (D-0029 §6 detection command (1))."""

    @pytest.fixture
    def report(self) -> str:
        return NEGATIVE_REPORT_NO_HEADING

    def test_self_audit_heading_absent(self, report: str):
        assert _self_audit_present(report) is False, (
            "negative-case fixture construction error: heading detected when it "
            "should be absent"
        )

    def test_inflation_positive_flag_fires(self, report: str):
        assert _inflation_positive(report) is True, (
            "D-0029 §6 detection command (1) broken: missing heading not flagged"
        )


class TestCrossReferenceWiring:
    """The Critical Rule #11 + TEST-009 cross-reference + fixture-name
    string MUST remain wired in rf-qa-qualitative.md so future readers
    can trace from spec to fixture and back."""

    def test_critical_rule_11_wired(self, src_text: str):
        """Critical Rule #11 names Self-Audit (a)+(b) obligation."""
        # NOTE (2026-05-24): markdownlint MD013 reflow per
        # TASK-RF-20260523-234320-markdownlint-remediation may split this
        # phrase across a line-break + indentation. Normalise whitespace
        # before the substring check so the audit remains content-pinned
        # without being byte-pinned to a specific line wrap.
        normalised = " ".join(src_text.split())
        assert "Your Self-Audit MUST list" in normalised, (
            "Critical Rule #11 consumer obligation phrasing missing from rf-qa-qualitative.md"
        )

    def test_test_009_named_in_schema_block(self, src_text: str):
        """The schema block (T03.04) names TEST-009 / T03.14 as the fixture."""
        assert "TEST-009" in src_text and "T03.14" in src_text, (
            "TEST-009 / T03.14 cross-reference missing from rf-qa-qualitative.md schema section"
        )

    def test_fixture_path_named_in_consumer_block(self, src_text: str):
        """The consumer-side handling block (T03.10) names this fixture file
        as the schema-conformance reference."""
        assert "tests/audit/test_self_audit_inv_019.py" in src_text, (
            "Consumer-side handling block does not name this fixture file — "
            "future readers cannot navigate spec → fixture"
        )
