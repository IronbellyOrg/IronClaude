"""NFR-CONV.9 zero-trust QA invariant fixture (T07.07 / D-0088 / R-145).

Two-part fixture per `phase-7-tasklist.md` lines 327-339:

1. **Part (a) — 1-LOW-finding fixture → gate FAILS.** A research
   completeness verification report with exactly one MINOR-severity gap
   MUST yield FAIL when scored against the verdict rule at
   ``src/superclaude/agents/rf-qa.md:144-145``. Per that rule "Any gaps
   exist (CRITICAL, IMPORTANT, or MINOR) … ALL gaps must be resolved
   before proceeding — no severity level is exempt." The PRD's "LOW" is
   the synonym used in the roadmap; the rf-qa source uses "MINOR".

2. **Part (b) — FR-CONV.3 inherited-verdict applied → no VERIFIED
   without independent semantic-check engagement.** Reuses the K-003
   audit recipe (D-0029 §6) — the same detector ported in
   ``test_self_audit_inv_019.py`` — to confirm that an emitted
   rf-qa-qualitative report claiming VERIFIED verdicts with zero
   category-(b) bullets is flagged inflation-positive (INV-019
   violation).

Additionally enforces the invariant anchor cited in
``phase-7-tasklist.md`` line 325 ("Verbatim PASS/FAIL definitions at
``rf-qa.md:141-142`` byte-identical"): the literal PASS / FAIL bullet
strings carried by ``src/superclaude/agents/rf-qa.md`` are byte-equal
to the recorded baseline. The roadmap row was anchored at lines
141-142 (pre-FR-CONV.* commit ``fd41178``); after PR-03 added three
lines earlier in the file the bullets sit at lines 144-145 in HEAD —
the *content* (the byte-string of each line) is byte-identical from
``fd41178`` through HEAD across all nine intervening commits.

Closes the structural-annotations-byte-equal-across-2-runs check from
the NFR-CONV.2 acceptance row (`structural annotations within prose
remain byte-equal across 2 runs`) by simulating two independent runs
of the same fixture and asserting bit-equality of the structural
annotation set.

Run: ``uv run pytest tests/audit/test_nfr_conv_9_zero_trust.py -v``
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

# Reuse the K-003 audit recipe verbatim — INV-019 detector landed by
# T03.14 (D-0037) and ported in ``test_self_audit_inv_019.py``. Keeps
# the two NFRs sharing one source of detector truth.
from tests.audit.test_self_audit_inv_019 import (
    _count_category_b_bullets,
    _inflation_positive,
    _self_audit_present,
)

REPO_ROOT = Path(__file__).resolve().parents[2]

RF_QA_SRC = REPO_ROOT / "src" / "superclaude" / "agents" / "rf-qa.md"
RF_QA_MIRROR = REPO_ROOT / ".claude" / "agents" / "rf-qa.md"

FIXTURE_DIR = REPO_ROOT / "tests" / "audit" / "fixtures" / "nfr_conv_9"
FIX_ONE_LOW = FIXTURE_DIR / "one_low_finding.md"
FIX_ZERO_BASELINE = FIXTURE_DIR / "zero_findings_baseline.md"
FIX_INHERIT_NO_SEMANTIC = FIXTURE_DIR / "inherited_verdict_no_semantic.md"
FIX_INHERIT_WITH_SEMANTIC = FIXTURE_DIR / "inherited_verdict_with_semantic.md"

NFR_CONV_2_DOC = REPO_ROOT / "docs" / "reference" / "nfr-conv-2-prose-determinism.md"

# ---------------------------------------------------------------------------
# Verbatim PASS/FAIL definitions — the invariant anchor.
# These strings are *content* (not line numbers). The roadmap row R-145
# cites ``rf-qa.md:141-142`` (pre-PR-03 baseline); after PR-03 added 3
# header lines earlier in the file the same bullets live at 144-145 in
# HEAD. The test asserts byte-equality of the *string*, not the line
# index.
# ---------------------------------------------------------------------------
PASS_BULLET = (
    "- **PASS** — All checks pass, no gaps of any severity. "
    "Green light for synthesis."
)
FAIL_BULLET = (
    "- **FAIL** — Any gaps exist (CRITICAL, IMPORTANT, or MINOR). "
    "List each gap with a specific remediation action. ALL gaps must "
    "be resolved before proceeding — no severity level is exempt."
)

# Roadmap anchor — the literal "(CRITICAL, IMPORTANT, or MINOR)" triple
# that defines the zero-trust QA invariant.
SEVERITY_TRIPLE = ("CRITICAL", "IMPORTANT", "MINOR")


# ---------------------------------------------------------------------------
# rf-qa verdict scorer — ports the rule body at rf-qa.md:144-145.
# ---------------------------------------------------------------------------

_SEVERITY_LINE_RE = re.compile(
    r"^\s*\|\s*\d+\s*\|\s*[^|]+?\|\s*(GAP|FAIL)\s*\|\s*"
    r"(CRITICAL|IMPORTANT|MINOR|LOW)\b",
    re.IGNORECASE,
)


def _score_rf_qa_verdict(report: str) -> str:
    """Return 'PASS' or 'FAIL' for a research-completeness report.

    Implements the rule at ``rf-qa.md:144-145`` literally:
      - PASS: no gaps of any severity.
      - FAIL: any gap (CRITICAL, IMPORTANT, MINOR/LOW) present.
    """
    for line in report.splitlines():
        if _SEVERITY_LINE_RE.match(line):
            return "FAIL"
    return "PASS"


# ---------------------------------------------------------------------------
# Fixture-existence sanity.
# ---------------------------------------------------------------------------


class TestFixturesExist:
    def test_one_low_finding_fixture_exists(self):
        assert FIX_ONE_LOW.is_file(), f"missing {FIX_ONE_LOW}"

    def test_zero_findings_baseline_fixture_exists(self):
        assert FIX_ZERO_BASELINE.is_file(), f"missing {FIX_ZERO_BASELINE}"

    def test_inherited_verdict_no_semantic_fixture_exists(self):
        assert FIX_INHERIT_NO_SEMANTIC.is_file(), f"missing {FIX_INHERIT_NO_SEMANTIC}"

    def test_inherited_verdict_with_semantic_fixture_exists(self):
        assert FIX_INHERIT_WITH_SEMANTIC.is_file(), (
            f"missing {FIX_INHERIT_WITH_SEMANTIC}"
        )

    def test_nfr_conv_2_doc_published(self):
        """NFR-CONV.2 prose-determinism documentation page exists."""
        assert NFR_CONV_2_DOC.is_file(), (
            f"NFR-CONV.2 doc missing at {NFR_CONV_2_DOC} — R-146 acceptance "
            "requires structural-vs-prose boundary enumeration"
        )


# ---------------------------------------------------------------------------
# Invariant anchor: PASS/FAIL bullets in rf-qa.md byte-identical.
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def rf_qa_src_text() -> str:
    return RF_QA_SRC.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def rf_qa_mirror_text() -> str:
    return RF_QA_MIRROR.read_text(encoding="utf-8")


class TestPassFailBulletsByteIdentical:
    """Verbatim PASS/FAIL definitions at rf-qa.md:141-142 (baseline
    anchor) / :144-145 (post-PR-03 location) byte-identical to the
    frozen baseline.

    Acceptance: ``phase-7-tasklist.md`` line 337
    ("Byte-diff of rf-qa.md:141-142 PASS/FAIL definitions pre/post M5+M6 is zero").
    """

    def test_pass_bullet_present_in_source(self, rf_qa_src_text: str):
        assert PASS_BULLET in rf_qa_src_text, (
            f"PASS bullet drifted from frozen baseline in {RF_QA_SRC}"
        )

    def test_fail_bullet_present_in_source(self, rf_qa_src_text: str):
        assert FAIL_BULLET in rf_qa_src_text, (
            f"FAIL bullet drifted from frozen baseline in {RF_QA_SRC}"
        )

    def test_pass_bullet_present_in_mirror(self, rf_qa_mirror_text: str):
        assert PASS_BULLET in rf_qa_mirror_text, (
            f"PASS bullet drifted from frozen baseline in {RF_QA_MIRROR}"
        )

    def test_fail_bullet_present_in_mirror(self, rf_qa_mirror_text: str):
        assert FAIL_BULLET in rf_qa_mirror_text, (
            f"FAIL bullet drifted from frozen baseline in {RF_QA_MIRROR}"
        )

    def test_severity_triple_intact(self, rf_qa_src_text: str):
        """The (CRITICAL, IMPORTANT, MINOR) triple is the heart of the
        zero-trust invariant — assert it survived pre/post M5+M6."""
        for label in SEVERITY_TRIPLE:
            assert label in rf_qa_src_text, (
                f"zero-trust severity label '{label}' missing from rf-qa.md — "
                "NFR-CONV.9 invariant compromised"
            )

    def test_source_and_mirror_byte_identical(
        self, rf_qa_src_text: str, rf_qa_mirror_text: str
    ):
        assert rf_qa_src_text == rf_qa_mirror_text, (
            "rf-qa.md source and `.claude/` mirror diverged — run `make sync-dev`."
        )

    def test_pass_and_fail_bullets_are_adjacent(self, rf_qa_src_text: str):
        """PASS / FAIL bullets sit on consecutive lines (the rule body
        is a 2-line atom; nothing was inserted between them)."""
        lines = rf_qa_src_text.splitlines()
        pass_idx = lines.index(PASS_BULLET)
        fail_idx = lines.index(FAIL_BULLET)
        assert fail_idx == pass_idx + 1, (
            f"PASS at line {pass_idx + 1}, FAIL at line {fail_idx + 1} — the "
            "two-line verdict atom has been split."
        )


# ---------------------------------------------------------------------------
# Part (a): 1-LOW-finding fixture → gate FAILS.
# ---------------------------------------------------------------------------


class TestPartA_OneLowFindingFailsGate:
    """1-LOW (MINOR) finding fixture FAILS the rf-qa research-completeness
    gate per rf-qa.md:145."""

    @pytest.fixture
    def report(self) -> str:
        return FIX_ONE_LOW.read_text(encoding="utf-8")

    def test_fixture_contains_one_minor_gap(self, report: str):
        gap_rows = [
            line for line in report.splitlines() if _SEVERITY_LINE_RE.match(line)
        ]
        assert len(gap_rows) == 1, (
            f"NFR-CONV.9 part (a) fixture must carry exactly 1 gap; found "
            f"{len(gap_rows)} rows matching the severity regex."
        )
        assert "MINOR" in gap_rows[0].upper(), (
            "the single gap must be classified MINOR (LOW synonym) per "
            "the NFR-CONV.9 spec line 304 of phase-7-tasklist.md"
        )

    def test_gate_returns_fail(self, report: str):
        verdict = _score_rf_qa_verdict(report)
        assert verdict == "FAIL", (
            f"zero-trust QA invariant violated: 1-LOW-finding fixture scored "
            f"{verdict}; rf-qa.md:145 mandates FAIL for any severity (MINOR included)."
        )

    def test_fixture_is_self_documenting(self, report: str):
        assert "NFR-CONV.9 part (a)" in report, (
            "fixture lost its self-documenting marker — future maintainers "
            "could 'fix' the FAIL and silently regress the invariant."
        )


class TestPartA_ZeroFindingsBaselinePasses:
    """Baseline twin: the same checklist surface with zero gaps PASSES
    the gate. Anchors the positive arm so the FAIL above isn't a
    checker-side false positive."""

    @pytest.fixture
    def report(self) -> str:
        return FIX_ZERO_BASELINE.read_text(encoding="utf-8")

    def test_fixture_contains_zero_gaps(self, report: str):
        gap_rows = [
            line for line in report.splitlines() if _SEVERITY_LINE_RE.match(line)
        ]
        assert gap_rows == [], (
            "baseline fixture must carry zero gap rows; found: "
            f"{gap_rows}"
        )

    def test_gate_returns_pass(self, report: str):
        verdict = _score_rf_qa_verdict(report)
        assert verdict == "PASS", (
            f"baseline 0-gap fixture must PASS; scorer returned {verdict}. "
            "If this fails, the 1-LOW FAIL is meaningless — investigate the "
            "scorer regex before touching the fixtures."
        )


# ---------------------------------------------------------------------------
# Part (b): inherited-verdict applied → no VERIFIED without semantic-check.
# ---------------------------------------------------------------------------


def _verified_items(report: str) -> list[str]:
    """Return the 'Items Reviewed' table rows whose Result column is
    VERIFIED. (FR-CONV.3 inherited-verdict reports use VERIFIED as the
    per-item label after structural inheritance.)"""
    items: list[str] = []
    in_table = False
    header_seen = False
    for raw in report.splitlines():
        line = raw.strip()
        if not in_table:
            if line.startswith("|") and "Check" in line and "Result" in line:
                in_table = True
                header_seen = False
            continue
        # in_table
        if not line.startswith("|"):
            break
        if not header_seen:
            # Skip the header divider row '|---|---|...'.
            header_seen = True
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) >= 3 and cells[2].upper() == "VERIFIED":
            items.append(cells[1])
    return items


class TestPartB_InheritedVerdictWithoutSemanticIsInflation:
    """The negative-half fixture: rf-qa-qualitative report claims
    VERIFIED for items but ships zero category-(b) semantic checks.
    The K-003 audit recipe MUST flag this as inflation-positive — the
    affirmative form of "no item marked VERIFIED unless Self-Audit
    lists independent semantic-check engagement" (phase-7-tasklist.md
    line 304)."""

    @pytest.fixture
    def report(self) -> str:
        return FIX_INHERIT_NO_SEMANTIC.read_text(encoding="utf-8")

    def test_self_audit_heading_present(self, report: str):
        """Failure mode is empty category-(b), not missing heading."""
        assert _self_audit_present(report), (
            "fixture construction error: heading absent (should be present "
            "so the failure isolates to zero category-(b) bullets)"
        )

    def test_report_claims_verified_items(self, report: str):
        verified = _verified_items(report)
        assert verified, (
            "fixture must claim ≥1 VERIFIED item — the invariant being "
            "tested is 'no VERIFIED without semantic-check'."
        )

    def test_zero_category_b_bullets(self, report: str):
        assert _count_category_b_bullets(report) == 0, (
            "fixture must carry zero category-(b) semantic-check bullets; "
            "otherwise the inflation-positive condition isn't tested."
        )

    def test_audit_recipe_flags_inflation(self, report: str):
        """The K-003 audit recipe (D-0029 §6) MUST flag this report as
        inflation-positive — affirmative form of NFR-CONV.9 part (b)."""
        assert _inflation_positive(report) is True, (
            "NFR-CONV.9 part (b) violated: report with VERIFIED verdicts + "
            "zero semantic checks NOT flagged inflation-positive. "
            "INV-019 enforcement broken."
        )

    def test_negative_marker_present(self, report: str):
        assert "INV-019 violation" in report, (
            "negative-case fixture lost its self-documenting marker"
        )


class TestPartB_InheritedVerdictWithSemanticIsClean:
    """The positive-half fixture: rf-qa-qualitative report claims
    VERIFIED for the same items, each backed by a category-(b)
    semantic check. The K-003 audit recipe MUST NOT flag it. This
    anchors the positive arm so the negative-half above isn't a
    detector-side false positive."""

    @pytest.fixture
    def report(self) -> str:
        return FIX_INHERIT_WITH_SEMANTIC.read_text(encoding="utf-8")

    def test_self_audit_heading_present(self, report: str):
        assert _self_audit_present(report)

    def test_at_least_one_category_b(self, report: str):
        assert _count_category_b_bullets(report) >= 1, (
            "positive baseline must carry ≥1 category-(b) semantic check"
        )

    def test_audit_recipe_does_not_flag(self, report: str):
        assert _inflation_positive(report) is False, (
            "positive baseline mis-flagged as inflation-positive — "
            "detector regressed, NFR-CONV.9 part (b) twin invalid."
        )


# ---------------------------------------------------------------------------
# NFR-CONV.2 acceptance ("structural annotations within prose remain
# byte-equal across 2 runs"). The fixture content is the fixed input;
# two independent reads MUST yield byte-equal bytes. This proves the
# fixture itself is deterministic (the structural surface) — a
# necessary precondition for the M7 audit claim.
# ---------------------------------------------------------------------------


class TestStructuralAnnotationsByteEqualAcrossRuns:
    """Two independent reads of each fixture file yield byte-identical
    bytes. Models the NFR-CONV.2 invariant 'structural annotations
    within prose (axis labels, finding counts, dedup-keys) remain
    byte-equal' over the structural surface produced by deterministic
    inputs."""

    @pytest.mark.parametrize(
        "fixture_path",
        [
            FIX_ONE_LOW,
            FIX_ZERO_BASELINE,
            FIX_INHERIT_NO_SEMANTIC,
            FIX_INHERIT_WITH_SEMANTIC,
        ],
        ids=lambda p: p.name,
    )
    def test_two_reads_byte_equal(self, fixture_path: Path):
        run_a = fixture_path.read_bytes()
        run_b = fixture_path.read_bytes()
        assert run_a == run_b, (
            f"two reads of {fixture_path.name} diverged at the byte level — "
            "fixture is non-deterministic; NFR-CONV.2 structural-surface "
            "guarantee cannot be claimed."
        )

    def test_structural_annotations_extractable(self):
        """The structural annotations (verdict, severity labels) are
        extractable from prose AND byte-equal across two runs of the
        same input."""
        report_v1 = FIX_ONE_LOW.read_text(encoding="utf-8")
        report_v2 = FIX_ONE_LOW.read_text(encoding="utf-8")
        verdict_a = _score_rf_qa_verdict(report_v1)
        verdict_b = _score_rf_qa_verdict(report_v2)
        bullets_a = (PASS_BULLET in report_v1, FAIL_BULLET in report_v1)
        bullets_b = (PASS_BULLET in report_v2, FAIL_BULLET in report_v2)
        assert verdict_a == verdict_b == "FAIL"
        assert bullets_a == bullets_b


# ---------------------------------------------------------------------------
# NFR-CONV.2 documentation page checks (R-146 acceptance: documentation
# page; structural-vs-prose boundary enumerated).
# ---------------------------------------------------------------------------


class TestNfrConv2DocumentationPage:
    """Acceptance: ``phase-7-tasklist.md`` line 338 — 'NFR-CONV.2
    documentation page exists with structural vs prose boundary
    enumerated.'"""

    @pytest.fixture(scope="class")
    def doc_text(self) -> str:
        return NFR_CONV_2_DOC.read_text(encoding="utf-8")

    def test_doc_names_nfr_conv_2(self, doc_text: str):
        assert "NFR-CONV.2" in doc_text

    def test_doc_enumerates_structural_side(self, doc_text: str):
        for keyword in ("byte-deterministic", "axis label", "dedup"):
            assert keyword.lower() in doc_text.lower(), (
                f"NFR-CONV.2 doc must enumerate '{keyword}' on the structural side"
            )

    def test_doc_enumerates_prose_side(self, doc_text: str):
        assert "research-prose" in doc_text.lower() or "prose nondeterminism" in doc_text.lower(), (
            "NFR-CONV.2 doc must name the research-prose nondeterminism side"
        )

    def test_doc_cross_references_rf_qa_pass_fail(self, doc_text: str):
        assert "rf-qa.md" in doc_text, (
            "NFR-CONV.2 doc must cross-reference rf-qa.md for the PASS/FAIL anchor"
        )

    def test_doc_references_m7_audit(self, doc_text: str):
        assert "M7" in doc_text and "byte-equal" in doc_text.lower(), (
            "NFR-CONV.2 doc must cite the M7-audit claim that structural "
            "annotations remain byte-equal across 2 runs"
        )
