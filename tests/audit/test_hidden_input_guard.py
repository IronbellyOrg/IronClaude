"""TEST-023 — Hidden-input determinism guard (T07.08 / D-0089).

NFR-CONV.3 hidden-input determinism contract (release-spec row 9,
roadmap R-148): "Fixture-populated `.dev/tasks/done/` MUST produce
byte-identical structural output to empty `.dev/tasks/done/`. PR-05
(Tier-History Advisory) is DEFERRED to Phase-2 and REJECTED for
Phase-1."

This module verifies the contract holds at three layers:

1. **Rule-artifact layer (TestRuleArtifactsExcludeDoneReadback)** —
   `src/superclaude/agents/rf-task-builder.md` and
   `src/superclaude/skills/task-builder/SKILL.md` contain no
   behaviour-modifying instruction that reads `.dev/tasks/done/`
   for current-task emission. The single ADVISORY mention in the
   task-builder SKILL.md TB-Add-2 line is informational
   (describes the empirical-calibration threshold for TB-Add-2 to
   promote out of `[ADVISORY]`) and does not read the directory.

2. **Fixture-equivalence layer (TestStructuralOutputByteIdentical)** —
   the `## Execution Context` byte range of `header_empty_done.md`
   and `header_populated_done.md` is byte-equal (md5 + sha256).
   This is the TEST-023 primary assertion (release-spec test row,
   R-149).

3. **Invariant-guard layer (TestHiddenInputGuardGrep)** — for both
   fixtures the Execution Context byte range satisfies the
   `grep -cE "src/|/.*:[0-9]+"` invariant (R-039 / NFR-CONV.3
   no-file-paths rule). The companion `hidden_input_leak.md`
   fixture in `tests/audit/fixtures/execution_context/` provides
   the negative-path sanity check: the detector returns ≥1 hit on
   a known-leaking header.

4. **Cross-run stability layer (TestTwoReadsByteEqual)** — each
   fixture read twice yields byte-identical bytes (structural
   annotations remain byte-equal across two reads — the same
   invariant pattern as NFR-CONV.9 / D-0088 §6).

5. **PR-05 disposition layer (TestPR05RemainsRejectedForPhase1)** —
   `release-spec.md` and `roadmap.md` carry the DEFERRED-to-Phase-2
   / REJECTED-for-Phase-1 disposition for PR-05 (Tier-History
   Advisory). Drift in this disposition would re-activate the
   hidden-input risk.

Run: ``uv run pytest tests/audit/test_hidden_input_guard.py -v``
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import List

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURE_DIR = Path(__file__).parent / "fixtures" / "hidden_input_guard"
EMPTY_FIXTURE = FIXTURE_DIR / "header_empty_done.md"
POPULATED_FIXTURE = FIXTURE_DIR / "header_populated_done.md"
INVENTORY_FIXTURE = FIXTURE_DIR / "populated_done_inventory.md"

EXECUTION_CONTEXT_LEAK_FIXTURE = (
    Path(__file__).parent / "fixtures" / "execution_context" / "hidden_input_leak.md"
)

RF_TASK_BUILDER_PATH = (
    REPO_ROOT / "src" / "superclaude" / "agents" / "rf-task-builder.md"
)
TB_SKILL_PATH = (
    REPO_ROOT / "src" / "superclaude" / "skills" / "task-builder" / "SKILL.md"
)
RELEASE_SPEC_PATH = (
    REPO_ROOT
    / ".dev"
    / "releases"
    / "complete"
    / "task-builder-merge"
    / "release-spec.md"
)
ROADMAP_PATH = (
    REPO_ROOT / ".dev" / "releases" / "complete" / "task-builder-merge" / "roadmap.md"
)

EC_HEADING = "## Execution Context"
HIDDEN_INPUT_GREP_RE = re.compile(r"src/|/.*:[0-9]+")
DONE_DIR_LITERAL_RE = re.compile(r"\.dev/tasks/done/?")


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def _read_bytes(path: Path) -> bytes:
    return path.read_bytes()


def _execution_context_range(text: str) -> str:
    """Extract the bytes from the `## Execution Context` heading
    through the closing `---` separator that follows the labeled
    bullets. Mirrors the rf-task-builder.md:415 byte-range
    definition used by the no-file-paths invariant."""
    lines = text.splitlines(keepends=True)
    start = None
    for i, line in enumerate(lines):
        if line.rstrip("\n") == EC_HEADING:
            start = i
            break
    assert start is not None, "fixture missing `## Execution Context` heading"
    end = start + 1
    while end < len(lines) and lines[end].rstrip("\n") != "---":
        end += 1
    # Include the terminating `---` line so the byte range exactly
    # matches the rf-task-builder.md:415 definition.
    end = min(end + 1, len(lines))
    return "".join(lines[start:end])


def _md5(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# ---------------------------------------------------------------------------
# 0. Fixture-presence sanity
# ---------------------------------------------------------------------------


class TestFixturesExist:
    def test_empty_done_fixture_exists(self):
        assert EMPTY_FIXTURE.is_file(), f"missing fixture: {EMPTY_FIXTURE}"

    def test_populated_done_fixture_exists(self):
        assert POPULATED_FIXTURE.is_file(), f"missing fixture: {POPULATED_FIXTURE}"

    def test_inventory_fixture_exists(self):
        assert INVENTORY_FIXTURE.is_file(), f"missing fixture: {INVENTORY_FIXTURE}"

    def test_negative_leak_fixture_exists(self):
        assert EXECUTION_CONTEXT_LEAK_FIXTURE.is_file(), (
            f"missing companion negative fixture: {EXECUTION_CONTEXT_LEAK_FIXTURE}"
        )

    def test_rule_artifact_paths_exist(self):
        assert RF_TASK_BUILDER_PATH.is_file()
        assert TB_SKILL_PATH.is_file()
        assert RELEASE_SPEC_PATH.is_file()
        assert ROADMAP_PATH.is_file()


# ---------------------------------------------------------------------------
# 1. Rule-artifact layer
# ---------------------------------------------------------------------------


class TestRuleArtifactsExcludeDoneReadback:
    """`.dev/tasks/done/` MUST NOT appear in any behaviour-modifying
    rule for current-task header emission. The TB-Add-2 ADVISORY
    threshold line was formerly the single allowed informational
    mention; 804eb4f4 intentionally removed TB-Add-2, so NO mention
    remains — the strongest no-hidden-input posture.
    """

    def test_rf_task_builder_has_no_done_readback(self):
        text = RF_TASK_BUILDER_PATH.read_text(encoding="utf-8")
        hits = DONE_DIR_LITERAL_RE.findall(text)
        assert hits == [], (
            "rf-task-builder.md must not reference `.dev/tasks/done/`; "
            f"found {len(hits)} occurrences — would re-activate PR-05 risk"
        )

    def test_task_builder_skill_has_no_done_mention(self):
        """SUPERSEDES `test_task_builder_skill_done_mention_is_advisory_only`.
        The task-builder SKILL.md now references `.dev/tasks/done/` ZERO times.
        TB-Add-2's ADVISORY calibration line was the only (informational)
        mention; 804eb4f4 removed TB-Add-2, so the hidden-input pathway has no
        foothold at all. `== 0` is STRICTLY STRONGER than the prior `== 1`
        exception — any new `.dev/tasks/done/` mention now fails immediately,
        rather than being silently tolerated as "the one advisory line"."""
        text = TB_SKILL_PATH.read_text(encoding="utf-8")
        lines = text.splitlines()
        donelines = [
            (idx + 1, raw)
            for idx, raw in enumerate(lines)
            if DONE_DIR_LITERAL_RE.search(raw)
        ]
        assert len(donelines) == 0, (
            "task-builder SKILL.md must NOT reference `.dev/tasks/done/` "
            f"(TB-Add-2 removed in 804eb4f4). Found {len(donelines)} mention(s) "
            f"at line(s) {[ln for ln, _ in donelines]} — would re-activate the "
            "PR-05 hidden-input pathway."
        )

    def test_no_done_readback_for_header_emission(self):
        """Cross-check: the words ``Read``, ``Glob``, or ``Grep``
        never appear in the same line as `.dev/tasks/done/`. The
        rf-task-builder agent prompt MUST NOT instruct the agent
        to *read* the directory."""
        for path in (RF_TASK_BUILDER_PATH, TB_SKILL_PATH):
            text = path.read_text(encoding="utf-8")
            for ln, raw in enumerate(text.splitlines(), start=1):
                if not DONE_DIR_LITERAL_RE.search(raw):
                    continue
                lower = raw.lower()
                # Allow the literal word "read" only when describing
                # the OPEN-PR05 cardinality threshold (which is a
                # passive observation by the operator, not a
                # builder-time directory read).
                forbidden = re.search(r"\b(glob\(|grep\(|read\()", raw) or re.search(
                    r"(builder|agent)\s+(read|reads|reading)\s+", lower
                )
                assert not forbidden, (
                    f"{path.name}:{ln} appears to instruct a builder-time "
                    f"read of `.dev/tasks/done/` — PR-05 reactivation risk: {raw!r}"
                )


# ---------------------------------------------------------------------------
# 2. Fixture-equivalence layer — TEST-023 primary assertion
# ---------------------------------------------------------------------------


class TestStructuralOutputByteIdentical:
    """TEST-023 primary contract: the structural output (the
    `## Execution Context` byte range) is byte-identical across the
    empty-done baseline and the populated-done twin."""

    def test_execution_context_byte_range_identical(self):
        empty_ec = _execution_context_range(EMPTY_FIXTURE.read_text(encoding="utf-8"))
        populated_ec = _execution_context_range(
            POPULATED_FIXTURE.read_text(encoding="utf-8")
        )
        assert empty_ec == populated_ec, (
            "Execution Context byte range diverges between empty-done baseline "
            "and populated-done twin — NFR-CONV.3 hidden-input determinism violated"
        )

    def test_execution_context_md5_identical(self):
        empty_ec = _execution_context_range(
            EMPTY_FIXTURE.read_text(encoding="utf-8")
        ).encode("utf-8")
        populated_ec = _execution_context_range(
            POPULATED_FIXTURE.read_text(encoding="utf-8")
        ).encode("utf-8")
        assert _md5(empty_ec) == _md5(populated_ec)

    def test_execution_context_sha256_identical(self):
        empty_ec = _execution_context_range(
            EMPTY_FIXTURE.read_text(encoding="utf-8")
        ).encode("utf-8")
        populated_ec = _execution_context_range(
            POPULATED_FIXTURE.read_text(encoding="utf-8")
        ).encode("utf-8")
        assert _sha256(empty_ec) == _sha256(populated_ec)

    def test_structural_per_item_fields_byte_identical(self):
        """The structural per-item field rendering (T01.01 block,
        the `Field | Value` rows, the `**Steps:**` + `**Acceptance
        Criteria:**` headings) must also be byte-identical across
        the two fixtures. This guards against partial leaks where
        only the EC header is byte-stable but per-item fields drift."""
        empty_text = EMPTY_FIXTURE.read_text(encoding="utf-8")
        populated_text = POPULATED_FIXTURE.read_text(encoding="utf-8")

        # Extract from `### T01.01` through the end of the file.
        def _structural_tail(text: str) -> str:
            lines = text.splitlines(keepends=True)
            for i, line in enumerate(lines):
                if line.startswith("### T01.01"):
                    return "".join(lines[i:])
            pytest.fail("fixture missing `### T01.01` structural section")

        assert _structural_tail(empty_text) == _structural_tail(populated_text), (
            "Structural per-item field rendering diverges across the two fixtures"
        )


# ---------------------------------------------------------------------------
# 3. Invariant-guard layer
# ---------------------------------------------------------------------------


class TestHiddenInputGuardGrep:
    """R-039 / NFR-CONV.3 no-file-paths invariant: the Execution
    Context byte range MUST satisfy ``grep -cE "src/|/.*:[0-9]+"``
    returning 0 hits."""

    @pytest.mark.parametrize(
        "fixture_path", [EMPTY_FIXTURE, POPULATED_FIXTURE], ids=lambda p: p.name
    )
    def test_byte_range_has_zero_hidden_input_hits(self, fixture_path):
        ec_range = _execution_context_range(fixture_path.read_text(encoding="utf-8"))
        hits = HIDDEN_INPUT_GREP_RE.findall(ec_range)
        assert not hits, (
            f"{fixture_path.name} Execution Context block has {len(hits)} "
            f"hidden-input grep hits — NFR-CONV.3 violated: {hits[:5]}"
        )

    def test_negative_fixture_triggers_detector(self):
        """Sanity: the existing `hidden_input_leak.md` negative
        fixture MUST trigger the detector (otherwise the detector
        itself is broken and the positive-path tests above are
        meaningless)."""
        leak_text = EXECUTION_CONTEXT_LEAK_FIXTURE.read_text(encoding="utf-8")
        ec_range = _execution_context_range(leak_text)
        hits = HIDDEN_INPUT_GREP_RE.findall(ec_range)
        assert hits, (
            "Negative fixture `hidden_input_leak.md` should trip the detector, "
            "but the grep regex returned zero hits — detector is broken"
        )


# ---------------------------------------------------------------------------
# 4. Cross-run stability layer
# ---------------------------------------------------------------------------


class TestTwoReadsByteEqual:
    """Each fixture read twice yields byte-identical bytes (the
    same invariant pattern as NFR-CONV.9 / D-0088 §6)."""

    @pytest.mark.parametrize(
        "fixture_path",
        [EMPTY_FIXTURE, POPULATED_FIXTURE, INVENTORY_FIXTURE],
        ids=lambda p: p.name,
    )
    def test_two_reads_byte_equal(self, fixture_path):
        first = _read_bytes(fixture_path)
        second = _read_bytes(fixture_path)
        assert first == second, f"two reads of {fixture_path.name} diverged"
        assert _md5(first) == _md5(second)


# ---------------------------------------------------------------------------
# 5. PR-05 disposition layer
# ---------------------------------------------------------------------------


class TestPR05RemainsRejectedForPhase1:
    """PR-05 Tier-History Advisory MUST remain DEFERRED-to-Phase-2 /
    REJECTED-for-Phase-1 (release-spec §2.1 + roadmap)."""

    def test_release_spec_pr05_deferred(self):
        text = RELEASE_SPEC_PATH.read_text(encoding="utf-8")
        # Look for the release-spec line that pins the disposition.
        pat = re.compile(r"PR-05[^.\n]*deferred to Phase-2", re.IGNORECASE)
        assert pat.search(text), (
            "release-spec.md must declare PR-05 DEFERRED to Phase-2; "
            "disposition pin missing"
        )

    def test_roadmap_pr05_phase2_disposition(self):
        text = ROADMAP_PATH.read_text(encoding="utf-8")
        # Roadmap row carrying PR-05 with Phase-2 cadence.
        assert "PR-05" in text, "roadmap.md missing PR-05 disposition row"
        # The roadmap notes "Phase-2 deferral" and the OPEN-PR05
        # re-evaluation cadence.
        assert "Phase-2" in text and "OPEN-PR05" in text, (
            "roadmap.md PR-05 row should pin Phase-2 deferral and OPEN-PR05 trigger"
        )

    def test_nfr_conv_3_row_pins_pr05_rejection_for_phase1(self):
        """The NFR-CONV.3 acceptance criterion explicitly carries
        the `PR-05-advisory-mechanism:remains-REJECTED-for-Phase-1`
        clause. Drift here would re-open the hidden-input pathway."""
        text = ROADMAP_PATH.read_text(encoding="utf-8")
        assert "PR-05-advisory-mechanism:remains-REJECTED-for-Phase-1" in text, (
            "roadmap.md NFR-CONV.3 row missing the explicit PR-05 rejection clause"
        )


# ---------------------------------------------------------------------------
# 6. Inventory cross-check (synthetic populated-done payload)
# ---------------------------------------------------------------------------


class TestInventoryCrossesOpenPR05Threshold:
    """The synthetic populated-done inventory MUST cross the
    OPEN-PR05 re-evaluation threshold (≥10 TASK-RF-* / ≥3 distinct
    task_types). If it didn't, the populated-done fixture would not
    exercise the hidden-input invariant under the binding condition."""

    def test_inventory_cardinality(self):
        text = INVENTORY_FIXTURE.read_text(encoding="utf-8")
        task_rows = re.findall(r"\|\s*TASK-RF-\d+-\d+\s*\|", text)
        assert len(task_rows) >= 10, (
            f"inventory cardinality {len(task_rows)} is below the "
            f"OPEN-PR05 ≥10-tasks threshold"
        )

    def test_inventory_task_type_diversity(self):
        text = INVENTORY_FIXTURE.read_text(encoding="utf-8")
        types: List[str] = []
        for raw in text.splitlines():
            m = re.match(r"^\|\s*TASK-RF-\d+-\d+\s*\|\s*([\w-]+)\s*\|", raw.strip())
            if m:
                types.append(m.group(1))
        unique_types = set(types)
        assert len(unique_types) >= 3, (
            f"inventory only spans {len(unique_types)} task_types "
            f"(have {sorted(unique_types)}); OPEN-PR05 requires ≥3"
        )
