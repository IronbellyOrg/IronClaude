"""Tests for the task-builder-merge release landings (PR-01 through PR-07, minus PR-05).

These are content-level assertion tests over the source-of-truth markdown files in
src/superclaude/skills/task-builder/SKILL.md and src/superclaude/agents/rf-*.md.

The skill and agents are text artifacts consumed by Claude Code at runtime; the
test surface here is "does the documented behavior contain the required markers
introduced by each landing?" — equivalent to a content gate.

If make sync-dev has run, the .claude/ copies should agree; we verify the source
side only because src/superclaude/ is the source of truth (see CLAUDE.md).
"""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_PATH = REPO_ROOT / "src" / "superclaude" / "skills" / "task-builder" / "SKILL.md"
RF_QA_PATH = REPO_ROOT / "src" / "superclaude" / "agents" / "rf-qa.md"
RF_QA_QUAL_PATH = REPO_ROOT / "src" / "superclaude" / "agents" / "rf-qa-qualitative.md"
RF_ANALYST_PATH = REPO_ROOT / "src" / "superclaude" / "agents" / "rf-analyst.md"
RF_TASK_BUILDER_PATH = REPO_ROOT / "src" / "superclaude" / "agents" / "rf-task-builder.md"


@pytest.fixture(scope="module")
def skill_text() -> str:
    return SKILL_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def rf_qa_text() -> str:
    return RF_QA_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def rf_qa_qualitative_text() -> str:
    return RF_QA_QUAL_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def rf_analyst_text() -> str:
    return RF_ANALYST_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def rf_task_builder_text() -> str:
    return RF_TASK_BUILDER_PATH.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# PR-06: Structural Gate Additions (TB-Add-1 through TB-Add-7)
# ---------------------------------------------------------------------------


class TestPR06StructuralGateAdditions:
    """PR-06 lands first per refactor plan. Adds TB-Add-1 through TB-Add-7 to
    both rf-qa.md task-integrity checklist and SKILL.md A.10 + 15-item
    validation checklist."""

    def test_rf_qa_checklist_count_extended(self, rf_qa_text: str) -> None:
        # Was 20 items; PR-06 grows it by 7 (TB-Add-1..7) -> 27. PR-01 then
        # adds TB-Add-8 -> 28. After both landings the count must be >= 27.
        # We assert the post-PR-01 final state to keep the test current.
        assert "#### Checklist (28 items)" in rf_qa_text

    @pytest.mark.parametrize("tag", [
        "TB-Add-1",
        "TB-Add-2",
        "TB-Add-3",
        "TB-Add-4",
        "TB-Add-5",
        "TB-Add-6",
        "TB-Add-7",
    ])
    def test_rf_qa_contains_tb_add_tag(self, rf_qa_text: str, tag: str) -> None:
        assert tag in rf_qa_text, f"rf-qa.md missing structural-gate addition {tag}"

    @pytest.mark.parametrize("tag", [
        "TB-Add-1",
        "TB-Add-2",
        "TB-Add-3",
        "TB-Add-4",
        "TB-Add-5",
        "TB-Add-6",
        "TB-Add-7",
    ])
    def test_skill_mirrors_tb_add_tag(self, skill_text: str, tag: str) -> None:
        # Both the A.10 spawn prompt and the 15-item validation checklist
        # mention each TB-Add tag at least once.
        assert tag in skill_text, f"SKILL.md missing structural-gate addition {tag}"

    def test_tb_add_2_marked_advisory(self, rf_qa_text: str) -> None:
        # TB-Add-2 must remain ADVISORY until empirical calibration completes.
        assert "ADVISORY" in rf_qa_text
        assert ".dev/tasks/done/" in rf_qa_text

    def test_tb_add_7_inactive_path_documented(self, rf_qa_text: str) -> None:
        # Inactive annotation is required when no Execution Context block exists.
        assert "tb-add-7-inactive" in rf_qa_text or "INACTIVE" in rf_qa_text

    def test_source_check_traceability(self, rf_qa_text: str) -> None:
        # Every TB-Add cites the originating sc:tasklist check ID for traceability.
        for source_check in ("check 11", "check 13", "check 14", "check 15", "check 16", "check 17"):
            assert source_check in rf_qa_text, (
                f"rf-qa.md missing source-check traceability for sc:tasklist {source_check}"
            )

    def test_skill_15item_validation_checklist_extended(self, skill_text: str) -> None:
        # The 15-item Task File Validation Checklist grows with 7 TB-Add entries.
        for tag in ("TB-Add-1", "TB-Add-2", "TB-Add-3", "TB-Add-4",
                    "TB-Add-5", "TB-Add-6", "TB-Add-7"):
            # Find the tag occurrence count >= 2: once in A.10 spawn prompt,
            # once in the Task File Validation Checklist near line 1491.
            assert skill_text.count(tag) >= 2, (
                f"SKILL.md does not reference {tag} in both A.10 prompt and "
                "Task File Validation Checklist"
            )


# ---------------------------------------------------------------------------
# PR-01: Execution Context Header (with REVISE acceptance criterion -> TB-Add-8)
# ---------------------------------------------------------------------------


class TestPR01ExecutionContextHeader:
    """PR-01 lands second. Adds an optional task-level `## Execution Context`
    block instruction to rf-task-builder spawn prompt and output schema, plus
    TB-Add-8 (per-item Context evidence binding) to enforce INV-015 scope-
    confinement."""

    def test_skill_documents_execution_context_block(self, skill_text: str) -> None:
        assert "EXECUTION CONTEXT BLOCK" in skill_text
        assert "## Execution Context" in skill_text

    def test_execution_context_uses_source_areas_not_paths(self, skill_text: str) -> None:
        # The block instructions must explicitly forbid file:line refs at the
        # task-level header.
        assert "NEVER write specific" in skill_text
        assert "path.py:NN" in skill_text  # cited as the forbidden form

    def test_execution_context_optional_and_degrades_gracefully(self, skill_text: str) -> None:
        assert "OPTIONAL" in skill_text
        # Minimal-BUILD_REQUEST degeneration case is documented.
        assert "GOAL-only" in skill_text or "References-only" in skill_text

    def test_execution_context_scope_confinement_rule(self, skill_text: str) -> None:
        # Per-item Context fields and research/*.md keep file:line citations.
        lowered = skill_text.lower()
        assert "per-item context fields" in lowered
        assert "file:line" in skill_text

    def test_output_schema_shows_execution_context_block(self, skill_text: str) -> None:
        # The output schema example (around the markdown ``` block near line
        # 1409) must include the Execution Context section as a template.
        # Count distinct mentions: instructions + schema example + checklist.
        assert skill_text.count("## Execution Context") >= 2

    def test_rf_qa_adds_tb_add_8(self, rf_qa_text: str) -> None:
        # PR-01 REVISE acceptance criterion: rf-qa task-integrity grows by one
        # more item to enforce per-item evidence binding (INV-015).
        assert "#### Checklist (28 items)" in rf_qa_text
        assert "TB-Add-8" in rf_qa_text
        assert "INV-015" in rf_qa_text  # rationale cited

    def test_tb_add_8_specifies_evidence_or_absence(self, rf_qa_text: str) -> None:
        # Either a file:line citation OR a justified-absence comment.
        assert "evidence-absence" in rf_qa_text
        assert "file:line citation" in rf_qa_text

    def test_skill_mirrors_tb_add_8(self, skill_text: str) -> None:
        # TB-Add-8 appears in BOTH the A.10 prompt and the validation checklist.
        assert skill_text.count("TB-Add-8") >= 2
