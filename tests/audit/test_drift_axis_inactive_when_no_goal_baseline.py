"""TEST-013 — `drift-axis-inactive` Summary-block annotation (R-086 / FR-CONV.4 PR-07).

Phase-4 / T04.14 deliverable (D-0052). Asserts that the canonical-rules
subsection under "Five Adversarial Axes" binds the literal annotation
``drift-axis-inactive`` to the **Summary** block (NOT as an Axis-column
cell value, NOT in Recommendations) when the AX-1 Drift axis is INACTIVE
because no BUILD_REQUEST.GOAL verbatim baseline is available.

Also verifies that the canonical fixture under
``artifacts/D-0045/fixture-goal-baseline-absent.md`` emits the literal
``drift-axis-inactive`` annotation inside the Summary block, demonstrating
the rule is operationally honoured.

Acceptance reference (phase-4-tasklist.md T04.14 AC):
- ``uv run pytest tests/audit/test_drift_axis_inactive_when_no_goal_baseline.py -v`` exits 0.
- TEST-013 asserts ``drift-axis-inactive`` literal annotation in Summary block.
- Evidence at ``TASKLIST_ROOT/artifacts/D-0052/evidence.md``.

Run: ``uv run pytest tests/audit/test_drift_axis_inactive_when_no_goal_baseline.py -v``
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

AGENT_SRC = REPO_ROOT / "src" / "superclaude" / "agents" / "rf-qa-qualitative.md"
AGENT_MIRROR = REPO_ROOT / ".claude" / "agents" / "rf-qa-qualitative.md"
FIXTURE = (
    REPO_ROOT
    / ".dev"
    / "releases"
    / "current"
    / "task-builder-merge"
    / "artifacts"
    / "D-0045"
    / "fixture-goal-baseline-absent.md"
)

ANNOTATION = "drift-axis-inactive"


@pytest.fixture(scope="module")
def src_text() -> str:
    return AGENT_SRC.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def mirror_text() -> str:
    return AGENT_MIRROR.read_text(encoding="utf-8")


class TestDriftAnnotationRulePresent:
    """The `drift-axis-inactive` rule is documented in both surfaces."""

    def test_annotation_token_in_source(self, src_text: str):
        assert ANNOTATION in src_text, (
            f"`{ANNOTATION}` annotation rule not found in {AGENT_SRC}"
        )

    def test_annotation_token_in_mirror(self, mirror_text: str):
        assert ANNOTATION in mirror_text, (
            f"`{ANNOTATION}` annotation rule not found in {AGENT_MIRROR}"
        )

    def test_rule_binds_to_summary_block(self, src_text: str):
        """The rule must bind the annotation to the Summary block (not Recommendations,
        not an Axis-column cell value)."""
        # Find the rule paragraph (the one introducing the canonical annotation).
        # It must mention both `Summary` and `drift-axis-inactive` together.
        for paragraph in re.split(r"\n\s*\n", src_text):
            if ANNOTATION in paragraph and "Summary" in paragraph:
                # Found the binding; assert it also forbids alternative placements.
                assert "Axis-column" in paragraph or "Axis column" in paragraph, (
                    f"rule must forbid the annotation from appearing as an Axis-column cell: {paragraph!r}"
                )
                return
        pytest.fail(
            f"no paragraph in {AGENT_SRC} binds `{ANNOTATION}` to the Summary block"
        )

    def test_rule_forbids_cell_value_placement(self, src_text: str):
        """The rule explicitly states that drift-axis-inactive is NOT an
        Axis-column cell value."""
        assert "NOT as an Axis-column cell value" in src_text or "not as an Axis-column cell value" in src_text, (
            f"rule must explicitly forbid `{ANNOTATION}` as an Axis-column cell value in {AGENT_SRC}"
        )


class TestDriftFixtureEmitsAnnotation:
    """The canonical GOAL-baseline-absent fixture emits the annotation in the
    Summary block."""

    def test_fixture_exists(self):
        assert FIXTURE.is_file(), f"missing canonical fixture at {FIXTURE}"

    def test_fixture_contains_literal_annotation(self):
        text = FIXTURE.read_text(encoding="utf-8")
        assert ANNOTATION in text, (
            f"fixture must contain literal `{ANNOTATION}` annotation: {FIXTURE}"
        )

    def test_annotation_appears_inside_summary_block(self):
        """The literal annotation MUST appear inside the `## Summary` section
        (between `## Summary` and the next `## ` heading)."""
        text = FIXTURE.read_text(encoding="utf-8")
        lines = text.splitlines()
        summary_start = -1
        summary_end = len(lines)
        for idx, line in enumerate(lines):
            if line.strip().lower() == "## summary":
                summary_start = idx + 1
                continue
            if summary_start != -1 and line.startswith("## ") and line.strip().lower() != "## summary":
                summary_end = idx
                break
        assert summary_start != -1, f"`## Summary` heading not found in {FIXTURE}"
        summary_body = "\n".join(lines[summary_start:summary_end])
        assert ANNOTATION in summary_body, (
            f"`{ANNOTATION}` must appear inside the Summary block; "
            f"summary body was: {summary_body!r}"
        )

    def test_annotation_not_in_axis_column_cells(self):
        """The literal annotation MUST NOT appear as an Items-Reviewed
        Axis-column cell value (i.e., between two `|` table separators)."""
        text = FIXTURE.read_text(encoding="utf-8")
        # Match `| <something containing drift-axis-inactive> |` in a table row.
        cell_re = re.compile(r"\|\s*[^|]*" + re.escape(ANNOTATION) + r"[^|]*\s*\|")
        for line in text.splitlines():
            if line.lstrip().startswith("|") and cell_re.search(line):
                pytest.fail(
                    f"`{ANNOTATION}` must not appear as an Axis-column cell value; "
                    f"offending row: {line!r}"
                )


class TestDriftAnnotationSourceMirrorParity:
    """Source and mirror agree byte-for-byte at the annotation rule."""

    def test_files_byte_identical(self, src_text: str, mirror_text: str):
        assert src_text == mirror_text, (
            "src/superclaude/agents/rf-qa-qualitative.md and "
            ".claude/agents/rf-qa-qualitative.md must be byte-identical "
            "(run `make sync-dev`)"
        )
