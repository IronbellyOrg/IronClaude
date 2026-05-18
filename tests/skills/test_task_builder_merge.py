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
RF_TASK_BUILDER_PATH = (
    REPO_ROOT / "src" / "superclaude" / "agents" / "rf-task-builder.md"
)


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

    @pytest.mark.parametrize(
        "tag",
        [
            "TB-Add-1",
            "TB-Add-2",
            "TB-Add-3",
            "TB-Add-4",
            "TB-Add-5",
            "TB-Add-6",
            "TB-Add-7",
        ],
    )
    def test_rf_qa_contains_tb_add_tag(self, rf_qa_text: str, tag: str) -> None:
        assert tag in rf_qa_text, f"rf-qa.md missing structural-gate addition {tag}"

    @pytest.mark.parametrize(
        "tag",
        [
            "TB-Add-1",
            "TB-Add-2",
            "TB-Add-3",
            "TB-Add-4",
            "TB-Add-5",
            "TB-Add-6",
            "TB-Add-7",
        ],
    )
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
        for source_check in (
            "check 11",
            "check 13",
            "check 14",
            "check 15",
            "check 16",
            "check 17",
        ):
            assert source_check in rf_qa_text, (
                f"rf-qa.md missing source-check traceability for sc:tasklist {source_check}"
            )

    def test_skill_15item_validation_checklist_extended(self, skill_text: str) -> None:
        # The 15-item Task File Validation Checklist grows with 7 TB-Add entries.
        for tag in (
            "TB-Add-1",
            "TB-Add-2",
            "TB-Add-3",
            "TB-Add-4",
            "TB-Add-5",
            "TB-Add-6",
            "TB-Add-7",
        ):
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

    def test_execution_context_uses_source_areas_not_paths(
        self, skill_text: str
    ) -> None:
        # The block instructions must explicitly forbid file:line refs at the
        # task-level header.
        assert "NO specific file:line references" in skill_text
        assert "path.py:NN" in skill_text  # cited as the forbidden form

    def test_execution_context_optional_and_degrades_gracefully(
        self, skill_text: str
    ) -> None:
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


# ---------------------------------------------------------------------------
# PR-04: Gate Results Passthrough (Inherited Structural Verdict)
# ---------------------------------------------------------------------------


class TestPR04GateResultsPassthrough:
    """PR-04 lands third. Pipes rf-qa's A.10 structural verdict into
    rf-qa-qualitative's spawn prompt as `## Inherited Structural Verdict`
    with anti-inflation guardrails for INV-002, INV-010, INV-019."""

    def test_skill_documents_inherited_structural_verdict(
        self, skill_text: str
    ) -> None:
        assert "Inherited Structural Verdict" in skill_text
        # PR-04 callout cites the operationalised rule explicitly.
        assert "PR-04 Gate Results Passthrough" in skill_text

    def test_skill_inv_002_reinjection_on_fix_cycles(self, skill_text: str) -> None:
        # On every fix cycle re-spawn, the orchestrator MUST re-inject the
        # fresh verdict; never reuse a stale verdict.
        assert "INV-002" in skill_text
        assert "re-inject" in skill_text

    def test_skill_inv_010_dynamic_tb_add_enumeration(self, skill_text: str) -> None:
        # PR-04 prompt MUST dynamically enumerate TB-Add catalogue
        # from the rf-qa source so future TB-Adds are auto-picked-up.
        assert "INV-010" in skill_text
        assert (
            "dynamically enumerate" in skill_text
            or "live TB-Add catalogue" in skill_text
        )

    def test_skill_anti_inflation_inv_019(self, skill_text: str) -> None:
        assert "INV-019" in skill_text
        assert (
            "ANTI-INFLATION" in skill_text
            or "Reliance is not verification" in skill_text
        )

    def test_skill_passthrough_fallback_documented(self, skill_text: str) -> None:
        # Failure-mode #1 from proposal: missing/malformed verdict file -> fall
        # back to standalone rf-qa-qualitative behavior.
        assert "fall back" in skill_text or "fallback" in skill_text.lower()
        # Specifically near the passthrough section.
        assert "missing or malformed" in skill_text

    def test_rf_qa_qualitative_rule_11_references_passthrough(
        self, rf_qa_qualitative_text: str
    ) -> None:
        # Rule #11 must mention the passthrough mechanism so the agent's
        # behavior aligns with the orchestrator's delivery.
        assert "Inherited Structural Verdict" in rf_qa_qualitative_text
        assert "PR-04 Gate Results Passthrough" in rf_qa_qualitative_text

    def test_rf_qa_qualitative_anti_inflation_in_rule_11(
        self, rf_qa_qualitative_text: str
    ) -> None:
        # Anti-inflation prompt language: reliance != verification.
        assert "reliance" in rf_qa_qualitative_text.lower()
        assert "Self-Audit" in rf_qa_qualitative_text

    def test_rf_qa_qualitative_output_has_reliance_audit_section(
        self, rf_qa_qualitative_text: str
    ) -> None:
        # Output template requires a Reliance Audit subsection when an
        # Inherited Structural Verdict was provided.
        assert "Reliance Audit" in rf_qa_qualitative_text
        assert "INV-019" in rf_qa_qualitative_text


# ---------------------------------------------------------------------------
# PR-07: Adversarial Category Naming (5-axis overlay)
# ---------------------------------------------------------------------------


class TestPR07AdversarialCategoryNaming:
    """PR-07 lands fourth. Adds a 5-axis adversarial taxonomy overlay
    (drift, contradictions, omissions, weakened-criteria, invented-content)
    to rf-qa-qualitative's task-qualitative phase as a naming overlay --
    no new code path, no new stage, no new agent file."""

    @pytest.mark.parametrize(
        "axis",
        [
            "Drift",
            "Contradictions",
            "Omissions",
            "Weakened criteria",
            "Invented content",
        ],
    )
    def test_rf_qa_qualitative_contains_axis(
        self, rf_qa_qualitative_text: str, axis: str
    ) -> None:
        assert axis in rf_qa_qualitative_text, (
            f"rf-qa-qualitative.md missing 5-axis entry: {axis}"
        )

    def test_axes_are_overlay_not_replacement(
        self, rf_qa_qualitative_text: str
    ) -> None:
        # The axes overlay the 15-item checklist, not replace it.
        assert "Five Adversarial Axes" in rf_qa_qualitative_text
        assert (
            "sharpening overlay" in rf_qa_qualitative_text
            or "overlay" in rf_qa_qualitative_text
        )

    def test_drift_baseline_requirement(self, rf_qa_qualitative_text: str) -> None:
        # The drift axis MUST require a GOAL verbatim baseline; otherwise mark
        # drift-axis-inactive.
        assert "drift-axis-inactive" in rf_qa_qualitative_text
        assert (
            "GOAL verbatim" in rf_qa_qualitative_text
            or "BUILD_REQUEST.GOAL" in rf_qa_qualitative_text
        )

    def test_axis_annotation_required_in_items_reviewed(
        self, rf_qa_qualitative_text: str
    ) -> None:
        # R-078 / T04.07: Items Reviewed table carries the `axis` column
        # positioned between `Check` and `Result`. Header literal pinned.
        assert "| # | Check | axis | Result | Evidence |" in rf_qa_qualitative_text

    def test_skill_references_5_axis_lens(self, skill_text: str) -> None:
        # SKILL.md A.10.5 must cite the 5 Adversarial Axes overlay.
        assert (
            "5 Adversarial Axes" in skill_text or "Five Adversarial Axes" in skill_text
        )
        assert "PR-07" in skill_text

    def test_invented_content_axis_is_evidence_bound(
        self, rf_qa_qualitative_text: str
    ) -> None:
        # "Invented content" axis requires cross-checking against research/*.md
        # -- it is itself evidence-bound.
        # Find the Invented-content paragraph and check it references the
        # research evidence files.
        assert (
            "research/*.md" in rf_qa_qualitative_text
            or "research files" in rf_qa_qualitative_text
        )

    def test_weakened_axis_anti_inflation(self, rf_qa_qualitative_text: str) -> None:
        # "Weakened" only fires when BUILD_REQUEST or research demands
        # stronger phrasing -- speculation does NOT count.
        # Be tolerant of phrasing variation.
        lowered = rf_qa_qualitative_text.lower()
        assert "speculation" in lowered or "speculative" in lowered
        # Anti-inflation cross-reference.
        assert "anti-inflation" in lowered


# ---------------------------------------------------------------------------
# PR-02: Retry Monotonicity Guards
# ---------------------------------------------------------------------------


class TestPR02RetryMonotonicityGuards:
    """PR-02 lands fifth. Adds two stop conditions (monotonicity guard +
    regression detection) to every retry loop in task-builder. Strengthens
    zero-trust QA against oscillation (FINAL-REPORT 6.2 F2 documented 21
    retry files / 18 batches empirical oscillation pattern)."""

    def test_skill_documents_retry_monotonicity_protocol(self, skill_text: str) -> None:
        assert "Retry Monotonicity Protocol" in skill_text
        assert "PR-02" in skill_text

    def test_skill_monotonicity_guard_strict_shrink(self, skill_text: str) -> None:
        # The monotonicity guard fires on strict non-shrink, NOT slow shrink.
        assert "strictly shrink" in skill_text or "strict non-shrink" in skill_text
        # The failure-count math is referenced.
        assert "F_n" in skill_text or "|F_n|" in skill_text

    def test_skill_regression_detection_precedence(self, skill_text: str) -> None:
        assert (
            "regression detected" in skill_text.lower()
            or "Regression detection" in skill_text
        )
        # Regression > monotonicity precedence rule (PR-02 Round-2 spec).
        assert "Precedence rule (regression > monotonicity)" in skill_text

    def test_skill_independent_counters_preserved(self, skill_text: str) -> None:
        # Each retry counter keeps its own monotonicity history.
        assert (
            "Independent counters" in skill_text
            or "tracked independently" in skill_text
        )

    def test_skill_inv_012_dnsp_composition(self, skill_text: str) -> None:
        # PR-03 synthetic findings COUNT as failures BUT dedup-key collapses
        # repeat-same-partition synthetics so they are not regressions.
        assert "INV-012" in skill_text
        assert "dedup" in skill_text.lower()
        assert "assigned_files_range" in skill_text  # dedup key field
        assert "escalation_ladder_exhaust_point" in skill_text

    def test_rf_task_builder_has_protocol(self, rf_task_builder_text: str) -> None:
        # The per-gate fix-cycle table in rf-task-builder must reference the
        # protocol.
        assert "Retry Monotonicity Protocol" in rf_task_builder_text
        assert "byte-exact wire string" in rf_task_builder_text
        assert "regression detected" in rf_task_builder_text.lower()

    def test_rf_qa_has_protocol_in_fix_cycle(self, rf_qa_text: str) -> None:
        # rf-qa.md's 3-fix-cycle rules must adopt the same guards.
        assert "Retry Monotonicity Protocol" in rf_qa_text
        assert "PR-02" in rf_qa_text
        # Composition with PR-03 DNSP cited.
        assert "INV-012" in rf_qa_text

    def test_skill_rule_7_references_protocol(self, skill_text: str) -> None:
        # Critical Rule #7 (mandatory QA gates) must cite the protocol so the
        # guards are part of zero-trust QA.
        # The text is in the Critical Rules section near the bottom.
        # Locate the Rule 7 block and assert the cross-reference.
        rule_block = skill_text.split("7. **Quality gates are mandatory.**", 1)[-1]
        rule_block = rule_block.split("8. **No one-shotting", 1)[0]
        assert "Retry Monotonicity Protocol" in rule_block


# ---------------------------------------------------------------------------
# PR-03: DNSP Synthetic Finding (BASE proposal)
# ---------------------------------------------------------------------------


class TestPR03DnspSyntheticFinding:
    """PR-03 is the BASE proposal (combined score 0.959, the only ADOPT
    across the original 5 RF->SC ports). Adds a paradigm-neutral
    synthetic-finding emission contract for partition-agent failures.
    Lands sixth in sequencing (independent of gate-pipeline edits)."""

    def test_skill_documents_dnsp_protocol(self, skill_text: str) -> None:
        assert "DNSP Synthetic Finding Protocol" in skill_text
        assert "PR-03" in skill_text
        assert "paradigm-neutral" in skill_text

    @pytest.mark.parametrize(
        "field",
        [
            "severity: HIGH",
            'source: "synthetic-dnsp"',
            "affected_range",
            "evidence",
            "recommendation",
        ],
    )
    def test_skill_dnsp_emission_contract_fields(
        self, skill_text: str, field: str
    ) -> None:
        assert field in skill_text, (
            f"SKILL.md DNSP emission contract missing field: {field}"
        )

    def test_skill_all_agents_fail_guard(self, skill_text: str) -> None:
        # If zero partition agents succeeded, DNSP does NOT fire -- existing
        # escalation flow runs.
        assert (
            "All-agents-fail guard" in skill_text
            or "all-agents-fail" in skill_text.lower()
        )

    def test_skill_dedup_key_specified(self, skill_text: str) -> None:
        # Dedup key per refactor plan: (assigned_files_range,
        # escalation_ladder_exhaust_point) -- composes with PR-02 INV-012.
        assert "(assigned_files_range, escalation_ladder_exhaust_point)" in skill_text
        assert "found N times" in skill_text

    def test_skill_applies_to_a8_a10_a105(self, skill_text: str) -> None:
        # The protocol applies symmetrically to all three partition spawn sites.
        # Verify the protocol's "applies symmetrically" listing references
        # all three (A.8, A.10, A.10.5).
        for ref in ("A.8 research-gate", "A.10 task-integrity", "A.10.5 qualitative"):
            assert ref in skill_text, f"DNSP protocol missing applicability ref: {ref}"

    def test_rf_analyst_partition_protocol_has_dnsp(self, rf_analyst_text: str) -> None:
        assert "DNSP Synthetic Finding emission" in rf_analyst_text
        assert "synthetic-dnsp" in rf_analyst_text
        assert "PR-03" in rf_analyst_text

    def test_rf_analyst_has_output_format_example(self, rf_analyst_text: str) -> None:
        # The agent definition includes an Output Format example so an
        # implementer knows the shape of a synthetic finding.
        assert (
            "Synthetic-DNSP Finding" in rf_analyst_text
            or "synthetic-dnsp" in rf_analyst_text
        )
        # The example contains the contract fields.
        assert (
            "Affected range" in rf_analyst_text or "affected_range" in rf_analyst_text
        )

    def test_rf_qa_partition_protocol_has_dnsp(self, rf_qa_text: str) -> None:
        assert "DNSP Synthetic Finding emission" in rf_qa_text
        assert "synthetic-dnsp" in rf_qa_text
        # rf-qa's Items Reviewed table must accept synthetic-dnsp as a source.
        assert "source: synthetic-dnsp" in rf_qa_text

    def test_rf_qa_qualitative_partition_protocol_has_dnsp(
        self, rf_qa_qualitative_text: str
    ) -> None:
        assert "DNSP Synthetic Finding emission" in rf_qa_qualitative_text
        assert "synthetic-dnsp" in rf_qa_qualitative_text

    def test_inv_012_composition_documented_across_agents(
        self,
        skill_text: str,
        rf_qa_text: str,
        rf_analyst_text: str,
    ) -> None:
        # The PR-02 + PR-03 composition (INV-012) must be cited consistently:
        # synthetic findings COUNT as failures but dedup-key collapses
        # repeat-same-partition cases so they are not regressions.
        for body in (skill_text, rf_qa_text, rf_analyst_text):
            assert "INV-012" in body
