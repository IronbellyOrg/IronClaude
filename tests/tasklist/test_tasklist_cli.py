"""Tests for tasklist CLI contract -- help text, exit codes, module structure.

Covers T04.03 acceptance criteria:
- superclaude tasklist validate --help renders with all option descriptions
- CLI exits 1 on HIGH-severity deviations
- Output written to {output_dir}/tasklist-fidelity.md
- Module structure verified
"""

from __future__ import annotations

import logging
from datetime import timezone
from pathlib import Path

import pytest
from click.testing import CliRunner

from superclaude.cli.main import main
from superclaude.cli.pipeline.models import PipelineConfig, Step, StepStatus
from superclaude.cli.tasklist import executor as tasklist_executor
from superclaude.cli.tasklist.commands import tasklist_group
from superclaude.cli.tasklist.executor import (
    _build_steps,
    _collect_tasklist_files,
    _has_high_severity,
)
from superclaude.cli.tasklist.gates import TASKLIST_FIDELITY_GATE
from superclaude.cli.tasklist.models import TasklistValidateConfig

# ---------------------------------------------------------------------------
# RFMerger P1-P5 + cross-cutting content gates (source-of-truth markdown).
#
# These assert against src/superclaude/skills/sc-tasklist-protocol/SKILL.md and
# its source-side templates (the SOURCE OF TRUTH, never the .claude/ mirror) --
# equivalent to the content-gate style in tests/skills/test_task_builder_merge.py.
# ---------------------------------------------------------------------------

_REPO_ROOT = Path(__file__).resolve().parents[2]
_TASKLIST_SKILL_DIR = (
    _REPO_ROOT / "src" / "superclaude" / "skills" / "sc-tasklist-protocol"
)
TASKLIST_SKILL_PATH = _TASKLIST_SKILL_DIR / "SKILL.md"
PHASE_TEMPLATE_PATH = _TASKLIST_SKILL_DIR / "templates" / "phase-template.md"
INDEX_TEMPLATE_PATH = _TASKLIST_SKILL_DIR / "templates" / "index-template.md"


@pytest.fixture(scope="module")
def tasklist_skill_text() -> str:
    return TASKLIST_SKILL_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def phase_template_text() -> str:
    return PHASE_TEMPLATE_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def index_template_text() -> str:
    return INDEX_TEMPLATE_PATH.read_text(encoding="utf-8")


class TestTasklistCLIHelp:
    """superclaude tasklist validate --help renders correctly."""

    def test_tasklist_group_help(self):
        runner = CliRunner()
        result = runner.invoke(tasklist_group, ["--help"])
        assert result.exit_code == 0
        assert "validate" in result.output

    def test_validate_help_renders(self):
        runner = CliRunner()
        result = runner.invoke(tasklist_group, ["validate", "--help"])
        assert result.exit_code == 0

    def test_validate_help_has_roadmap_file_option(self):
        runner = CliRunner()
        result = runner.invoke(tasklist_group, ["validate", "--help"])
        assert "--roadmap-file" in result.output

    def test_validate_help_has_tasklist_dir_option(self):
        runner = CliRunner()
        result = runner.invoke(tasklist_group, ["validate", "--help"])
        assert "--tasklist-dir" in result.output

    def test_validate_help_has_model_option(self):
        runner = CliRunner()
        result = runner.invoke(tasklist_group, ["validate", "--help"])
        assert "--model" in result.output

    def test_validate_help_has_max_turns_option(self):
        runner = CliRunner()
        result = runner.invoke(tasklist_group, ["validate", "--help"])
        assert "--max-turns" in result.output

    def test_validate_help_has_debug_option(self):
        runner = CliRunner()
        result = runner.invoke(tasklist_group, ["validate", "--help"])
        assert "--debug" in result.output

    def test_validate_registered_on_main(self):
        """Validate command is registered on the main CLI group."""
        runner = CliRunner()
        result = runner.invoke(main, ["tasklist", "--help"])
        assert result.exit_code == 0
        assert "validate" in result.output


class TestTasklistModuleStructure:
    """T04.03: Module structure verification."""

    def test_init_exists(self):
        from superclaude.cli import tasklist

        assert hasattr(tasklist, "__all__")

    def test_commands_module_exists(self):
        from superclaude.cli.tasklist import commands

        assert hasattr(commands, "tasklist_group")
        assert hasattr(commands, "validate")

    def test_executor_module_exists(self):
        from superclaude.cli.tasklist import executor

        assert hasattr(executor, "execute_tasklist_validate")

    def test_gates_module_exists(self):
        from superclaude.cli.tasklist import gates

        assert hasattr(gates, "TASKLIST_FIDELITY_GATE")

    def test_prompts_module_exists(self):
        from superclaude.cli.tasklist import prompts

        assert hasattr(prompts, "build_tasklist_fidelity_prompt")

    def test_models_module_exists(self):
        from superclaude.cli.tasklist import models

        assert hasattr(models, "TasklistValidateConfig")


class TestTasklistValidateExitCode:
    """T04.03: CLI exits 1 on HIGH-severity deviations."""

    def test_has_high_severity_true_for_high_count(self, tmp_path):
        report = tmp_path / "tasklist-fidelity.md"
        report.write_text(
            "---\n"
            "high_severity_count: 2\n"
            "medium_severity_count: 0\n"
            "low_severity_count: 0\n"
            "total_deviations: 2\n"
            "validation_complete: true\n"
            "tasklist_ready: false\n"
            "---\n"
            "## Deviation Report\n"
            "- DEV-001: HIGH\n"
            "- DEV-002: HIGH\n"
        )
        assert _has_high_severity(report) is True

    def test_has_high_severity_false_for_zero(self, tmp_path):
        report = tmp_path / "tasklist-fidelity.md"
        report.write_text(
            "---\n"
            "high_severity_count: 0\n"
            "medium_severity_count: 1\n"
            "low_severity_count: 2\n"
            "total_deviations: 3\n"
            "validation_complete: true\n"
            "tasklist_ready: true\n"
            "---\n"
            "## Deviation Report\n"
            "- DEV-001: MEDIUM\n"
        )
        assert _has_high_severity(report) is False

    def test_has_high_severity_true_for_missing_report(self, tmp_path):
        report = tmp_path / "nonexistent.md"
        assert _has_high_severity(report) is True

    def test_has_high_severity_true_for_no_frontmatter(self, tmp_path):
        report = tmp_path / "tasklist-fidelity.md"
        report.write_text("No frontmatter here.\n")
        assert _has_high_severity(report) is True


class TestCollectTasklistFiles:
    """Executor helper tests."""

    def test_collects_markdown_files(self, tmp_path):
        (tmp_path / "phase-1-tasklist.md").write_text("# Phase 1\n")
        (tmp_path / "phase-2-tasklist.md").write_text("# Phase 2\n")
        (tmp_path / "notes.txt").write_text("Not markdown\n")
        files = _collect_tasklist_files(tmp_path)
        assert len(files) == 2
        assert all(f.suffix == ".md" for f in files)

    def test_raises_for_missing_dir(self, tmp_path):
        with pytest.raises(FileNotFoundError, match="Tasklist directory not found"):
            _collect_tasklist_files(tmp_path / "nonexistent")

    def test_raises_for_empty_dir(self, tmp_path):
        empty = tmp_path / "empty"
        empty.mkdir()
        with pytest.raises(FileNotFoundError, match="No markdown files found"):
            _collect_tasklist_files(empty)

    def test_files_sorted(self, tmp_path):
        (tmp_path / "b.md").write_text("b\n")
        (tmp_path / "a.md").write_text("a\n")
        (tmp_path / "c.md").write_text("c\n")
        files = _collect_tasklist_files(tmp_path)
        assert [f.name for f in files] == ["a.md", "b.md", "c.md"]


class TestBuildSteps:
    """Executor _build_steps tests."""

    def test_build_steps_creates_one_step(self, tmp_path):
        roadmap = tmp_path / "roadmap.md"
        roadmap.write_text("# Roadmap\n")
        tasklist_dir = tmp_path / "tasklists"
        tasklist_dir.mkdir()
        (tasklist_dir / "phase-1.md").write_text("# Phase 1\n")

        config = TasklistValidateConfig(
            output_dir=tmp_path,
            roadmap_file=roadmap,
            tasklist_dir=tasklist_dir,
        )
        steps = _build_steps(config)
        assert len(steps) == 1
        assert steps[0].id == "tasklist-fidelity"

    def test_build_steps_output_path(self, tmp_path):
        roadmap = tmp_path / "roadmap.md"
        roadmap.write_text("# Roadmap\n")
        tasklist_dir = tmp_path / "tasklists"
        tasklist_dir.mkdir()
        (tasklist_dir / "phase-1.md").write_text("# Phase 1\n")

        config = TasklistValidateConfig(
            output_dir=tmp_path,
            roadmap_file=roadmap,
            tasklist_dir=tasklist_dir,
        )
        steps = _build_steps(config)
        assert steps[0].output_file == tmp_path / "tasklist-fidelity.md"

    def test_build_steps_includes_roadmap_in_inputs(self, tmp_path):
        roadmap = tmp_path / "roadmap.md"
        roadmap.write_text("# Roadmap\n")
        tasklist_dir = tmp_path / "tasklists"
        tasklist_dir.mkdir()
        (tasklist_dir / "phase-1.md").write_text("# Phase 1\n")

        config = TasklistValidateConfig(
            output_dir=tmp_path,
            roadmap_file=roadmap,
            tasklist_dir=tasklist_dir,
        )
        steps = _build_steps(config)
        assert roadmap in steps[0].inputs

    def test_build_steps_includes_tasklist_files_in_inputs(self, tmp_path):
        roadmap = tmp_path / "roadmap.md"
        roadmap.write_text("# Roadmap\n")
        tasklist_dir = tmp_path / "tasklists"
        tasklist_dir.mkdir()
        (tasklist_dir / "phase-1.md").write_text("# Phase 1\n")
        (tasklist_dir / "phase-2.md").write_text("# Phase 2\n")

        config = TasklistValidateConfig(
            output_dir=tmp_path,
            roadmap_file=roadmap,
            tasklist_dir=tasklist_dir,
        )
        steps = _build_steps(config)
        # roadmap + 2 tasklist files = 3 inputs
        assert len(steps[0].inputs) == 3

    def test_build_steps_gate_is_tasklist_fidelity(self, tmp_path):
        roadmap = tmp_path / "roadmap.md"
        roadmap.write_text("# Roadmap\n")
        tasklist_dir = tmp_path / "tasklists"
        tasklist_dir.mkdir()
        (tasklist_dir / "phase-1.md").write_text("# Phase 1\n")

        config = TasklistValidateConfig(
            output_dir=tmp_path,
            roadmap_file=roadmap,
            tasklist_dir=tasklist_dir,
        )
        steps = _build_steps(config)
        assert steps[0].gate is TASKLIST_FIDELITY_GATE

    def test_build_steps_timeout_600s(self, tmp_path):
        roadmap = tmp_path / "roadmap.md"
        roadmap.write_text("# Roadmap\n")
        tasklist_dir = tmp_path / "tasklists"
        tasklist_dir.mkdir()
        (tasklist_dir / "phase-1.md").write_text("# Phase 1\n")

        config = TasklistValidateConfig(
            output_dir=tmp_path,
            roadmap_file=roadmap,
            tasklist_dir=tasklist_dir,
        )
        steps = _build_steps(config)
        assert steps[0].timeout_seconds == 600


class TestP4EvidenceAnchoredValidation:
    """P4 -- gate-results.txt passthrough + Stage-7 injection + 20-check hygiene."""

    def test_gate_results_passthrough(self, tasklist_skill_text):
        text = tasklist_skill_text
        # Stage-6 gate-results.txt emission instruction present at the source of truth.
        assert "TASKLIST_ROOT/validation/gate-results.txt" in text
        # Literal serialized line-format tokens (plain text, NOT JSON).
        assert "CHECK <n> PASS:" in text
        assert "CHECK <n> FAIL:" in text
        assert "GATE: PASS (20/20)" in text
        assert "GATE: FAIL (<n> failing)" in text
        # All-pass-still-emitted directive (passthrough evidence, not a failure log).
        assert "EVEN ON an all-pass gate" in text
        # Stage-7 injection of gate-results.txt content into the validation-agent prompt.
        assert "Pre-validation gate context" in text

    def test_gate_results_path_same_path_contract(self, tasklist_skill_text):
        # C2-07 (G1): the Stage-6 emit and the Stage-7 mentions all reference the SAME path.
        # >=4 occurrences pins the same-path contract (AC#6): 1x Gate-Results subsection emit,
        # 2x Stage-7 payload bullets (Agent A + Agent B), 1x Stage-7 blockquote.
        text = tasklist_skill_text
        assert text.count("TASKLIST_ROOT/validation/gate-results.txt") >= 4

    def test_gate_results_plain_text_not_json(self, tasklist_skill_text):
        # C2-08 (G2): AC#2 plain-text directive — the artifact is NOT JSON.
        text = tasklist_skill_text
        assert "NOT JSON" in text

    def test_no_stage_6_5_or_generation_evidence_regression(self, tasklist_skill_text):
        # C2-09 (G3): guard against re-introducing the rejected Stage 6.5 / generation-evidence.json surface.
        text = tasklist_skill_text
        assert "generation-evidence" not in text
        assert "Stage 6.5" not in text

    def test_gate_results_numeric_ordering_directive(self, tasklist_skill_text):
        # C2-10 (G4): one-line-per-check ordering directive is pinned in the source-of-truth prose.
        text = tasklist_skill_text
        assert "numeric order 1→20" in text

    def test_self_check_count_is_20_not_17(self, tasklist_skill_text):
        text = tasklist_skill_text
        # The Stage-6 completion string must say 20 checks, not the stale 17.
        assert "Self-Check: all 20 checks passed" in text
        # The stale "all 17 checks" string must not recur anywhere in the source.
        assert "all 17 checks" not in text
        assert "17 checks" not in text


class TestP1ContextArmedSteps:
    """P1 -- optional task-level ## Execution Context block + deterministic emission."""

    def test_execution_context_block_shape(self, tasklist_skill_text):
        text = tasklist_skill_text
        # The optional task-level block is present in the phase-file task-body template.
        assert "## Execution Context" in text
        # It declares the three reused task-builder sub-fields (verbatim names).
        assert "References" in text
        assert "Source areas" in text
        assert "Key constraints" in text
        # Deterministic emission rule: emit iff >=1 resolvable roadmap ref.
        assert "emit iff ≥1 resolvable roadmap ref" in text
        assert "if and only if" in text
        # References-only degradation + omit-when-none branches are both explicit.
        assert "References-only" in text
        assert "Omit the block entirely" in text
        # No-file:line-in-header discipline is stated (no src/ or path leakage in header).
        assert "NO specific `file:line` references" in text
        assert "not file paths" in text
        # No Ensuring: clause; Acceptance Criteria remain the single source of truth.
        assert "NO `Ensuring:` clause" in text
        assert "single source of truth" in text

    def test_execution_context_mirror_in_phase_template(self, phase_template_text):
        # The source-side phase-template mirror carries the same optional block, so the
        # SKILL.md inline copy and the human-review mirror stay in sync.
        text = phase_template_text
        assert "## Execution Context" in text
        assert "References" in text
        assert "Source areas" in text
        assert "Key constraints" in text
        # The mirror keeps the no-file:line-in-header discipline too.
        assert "NO specific `file:line` references" in text
        # C3-07/C3-08: the three sub-field hint lines are byte-identical to SKILL.md.
        assert (
            "- Source areas: <named module(s)/area(s), not file paths; "
            "listed when the roadmap supplies them, "
            "omitted in the References-only degraded form>"
        ) in text
        assert (
            "- Key constraints: <the first 1-3 stated invariants in roadmap "
            "appearance order; omitted when the roadmap supplies none>"
        ) in text
        # D-2 (POST-reflect remediation): parity with the SKILL.md-side block-shape
        # test — the mirror MUST also document the no-`Ensuring:`-clause discipline so a
        # future edit cannot reintroduce an `Ensuring:` clause into the mirror unguarded.
        assert "NO `Ensuring:` clause" in text

    def test_execution_context_block_not_in_index(self, index_template_text):
        # C3-10 (R-2 lock): the optional Execution Context block lives in the per-task
        # phase BODY, never the index. The index template must not carry the block.
        assert "## Execution Context" not in index_template_text

    def test_execution_context_no_goal_derived_refs(self, tasklist_skill_text):
        # C3-01: there is no GOAL input to this generator; `References:` is exactly the
        # resolved R-### roadmap reference(s). The GOAL-derived phrasing must be gone.
        text = tasklist_skill_text
        assert "GOAL-derived refs" not in text
        assert "the resolved R-### roadmap reference(s)" in text

    def test_execution_context_deterministic_extraction_rules(
        self, tasklist_skill_text
    ):
        # C3-02/C3-03/C3-04/C3-06: the §4.1d emission rule pins deterministic
        # Source-areas extraction, Key-constraints selection, a form-selection table,
        # and the canonical input set.
        text = tasklist_skill_text
        assert "roadmap appearance order" in text
        assert "De-dup case-insensitively" in text
        assert "Form-selection decision table" in text
        assert (
            "{resolved R-### refs, roadmap-supplied named source areas, "
            "roadmap-stated invariants}"
        ) in text
        # No GOAL input to this generator (no-inference contract).
        assert "There is no GOAL input to this generator" in text


class TestP3DnspSyntheticFindings:
    """P3 -- Stage-7 synthetic-dnsp finding reusing the task-builder DM-003 contract."""

    def test_dnsp_synthetic_provenance(self, tasklist_skill_text):
        text = tasklist_skill_text
        # DM-003 fixed-value fields (reused verbatim from task-builder).
        assert 'source: "synthetic-dnsp"' in text
        assert "severity: HIGH" in text
        # The never-blank dynamic fields are all named.
        assert "affected_range" in text
        assert "recommendation" in text
        # evidence: pin the never-blank stub in its DM-003 context (the bare
        # token "evidence" appears ~20x e.g. "evidence.md", so assert the
        # P3-exclusive evidence-absence stub string instead). CF-01 re-pinned
        # the stub to the canonical DM-003 / R-116 parametrized form.
        assert "<!-- evidence-absence: no-spawn-log: <reason> -->" in text
        # Fixed recommendation literal, em-dash preserved, no suffix.
        assert "Manual review required — partition agent failed twice" in text
        # dedup_key shape with the pinned Stage-7 retry-1 exhaust-point.
        assert '["<stage7_affected_range>", "retry-1"]' in text
        assert "retry-1" in text
        # found_n_times default value pinned (matches the authored phrasing
        # `found_n_times`: `1` on first emission).
        assert "`found_n_times`: `1`" in text
        # Strictly-additive, HIGH non-overridable, and no-sideband invariants.
        assert "strictly additive" in text
        assert "non-overridable" in text
        assert "NO sideband channel" in text

    def test_dnsp_all_agents_fail_escalates(self, tasklist_skill_text):
        text = tasklist_skill_text
        # Some-vs-zero branch: >=1 success + >=1 fail -> synthetic emits and PROCEEDS.
        assert "≥1 succeeded AND ≥1 failed" in text
        assert "PROCEEDS" in text
        # Zero success -> NO synthetic emit + existing escalation path.
        assert "ZERO succeeded (all-agents-fail)" in text
        assert "Emit **NO** synthetic finding" in text
        # No invented StageError symbol claimed as a reuse.
        assert "NOT a reuse of any existing `StageError` symbol" in text

    def test_dnsp_all_succeeded_branch(self, tasklist_skill_text):
        text = tasklist_skill_text
        # Exhaustive some-vs-zero gate: the all-succeeded (0 failed) branch ->
        # normal merge, NO synthetic, proceed.
        assert "ALL succeeded (zero failed)" in text
        assert "normal merge" in text
        # The three branches are declared mutually exclusive AND exhaustive.
        assert "mutually exclusive and exhaustive" in text
        # Zero-success branch points at the concrete report-validation-error
        # terminal, not an undefined path.
        assert "report-validation-error terminal" in text

    def test_dnsp_short_circuit_guard(self, tasklist_skill_text):
        text = tasklist_skill_text
        # A synthetic-dnsp record IS a finding -> the zero-finding short-circuit
        # MUST NOT fire when one is present.
        assert 'A `source: "synthetic-dnsp"` finding IS a finding' in text
        assert "MUST NOT be taken when one or more synthetic-dnsp records" in text
        # Treated FAIL until manual review; Stage-9 patch executor must not
        # auto-patch it. The C4-03 fix dropped the stale "gap-fill / patch
        # cycle" phrasing from the guard (the only legitimate remaining
        # "gap-fill" use is inside the DM-003 closed-vocab enumeration).
        assert "treated as FAIL until manual review" in text
        assert "Stage-9 patch executor MUST NOT auto-resolve / auto-patch it" in text
        assert "gap-fill / patch cycle MUST NOT auto-resolve" not in text

    def test_dnsp_excluded_from_patch_checklist(self, tasklist_skill_text):
        text = tasklist_skill_text
        # Non-patchable synthetic is excluded from the actionable PatchChecklist
        # and parked in a manual-review section of ValidationReport.md.
        assert (
            '`source: "synthetic-dnsp"` findings are EXCLUDED from the '
            "actionable PatchChecklist"
        ) in text
        assert "## Manual Review Required (synthetic-dnsp)" in text
        # Stage 9 reinforces: these are never fed to sc:task.
        assert "NEVER fed to `sc:task`" in text


class TestP2BoundedPatchLoop:
    """P2 -- bounded Stage-10->9 patch loop reusing PR-02 guards (RETAINED)."""

    def test_p2_bounded_loop_guards(self, tasklist_skill_text):
        text = tasklist_skill_text
        # The bounded loop-back replaced the old "does NOT loop" gate entirely.
        assert "does NOT loop" not in text
        assert "bounded patch loop" in text
        # Full-set Stage-7 re-validation each pass (not subset-only).
        assert "FULL Stage-7 2N validation set" in text
        # Strict-shrink monotonicity.
        assert "|F_{k+1}| >= |F_k|" in text
        assert "strictly shrank" in text
        # Regression detection with PRECEDENCE over monotonicity.
        assert "Regression check (precedence over monotonicity)" in text
        assert "regression → monotonicity → hard-cap → proceed" in text
        # Byte-exact PR-02 halt strings (em-dash preserved on the regression halt).
        assert "[HALT-MONOTONICITY] |F|=<n>" in text
        assert (
            "Regression detected on Item X.Y — previously PASS at cycle N, "
            "now FAIL. Halt overrides monotonicity check."
        ) in text
        # 2-TOTAL-pass cap (k in {2}), explicitly NOT task-builder's 3-cap.
        assert "2 TOTAL passes" in text
        assert "k ∈ {2}" in text
        assert "NOT task-builder's 3-cap" in text
        # C5-03: operative cap predicates pinned at the logic lines (not just
        # the co-located summary tokens) -- corrupting these ships green otherwise.
        assert "`k+1 > 2`" in text  # hard-cap predicate
        assert "`k < 2`" in text  # proceed/loop predicate
        # C5-04: monotonicity arm-condition -- consulted only when the patchable
        # failing set is non-empty.
        assert "`|F_k| > 0`" in text

    def test_p2_excludes_synthetic_dnsp_from_fk(self, tasklist_skill_text):
        # OQ-PRE-1: a persistent non-patchable synthetic must NOT trip the P2
        # monotonicity halt -- synthetic-dnsp records are excluded from F_k.
        text = tasklist_skill_text
        assert 'EXCLUDES `source: "synthetic-dnsp"` records' in text
        assert "patchable" in text
        # C5-05: the F_k sentence anchors its non-patchable exclusion on the
        # "patchable failing findings" qualifier, not bare "patchable".
        assert "**patchable** failing findings" in text

    def test_p2_stage_10_5_non_overlap(self, tasklist_skill_text):
        text = tasklist_skill_text
        # The disjointness predicate between P2-loop findings and Stage-10.5
        # reflect-pre findings is documented.
        assert (
            "set(P2_loop_findings) ∩ set(stage_10_5_reflect_pre_findings) == ∅"
        ) in text
        # The Stage-10.5 fence explicitly includes the P2 bounded loop-back
        # iterations (the loop must converge before Stage 10.5 fans out).
        assert "including any P2 bounded loop-back iterations" in text
        # C5-05: fence-ordering direction -- the P2 loop must terminate BEFORE
        # Stage 10.5 fans out (the converge-before-reflect-pre invariant).
        assert "BEFORE Stage 10.5" in text


class TestP5TierCalibrationAdvisory:
    """P5 -- index-level advisory-only ## Tier Calibration Advisory (RETAINED)."""

    def test_tier_calibration_advisory_shape(self, tasklist_skill_text):
        text = tasklist_skill_text
        # Index-level advisory section is present.
        assert "## Tier Calibration Advisory" in text
        # Read-only feedback-log source.
        assert "TASKLIST_ROOT/feedback-log.md" in text
        assert "best-effort and READ-ONLY" in text
        # Min-2-matching-overrides render threshold; omit whole section otherwise.
        assert "only when ≥2 matching overrides exist" in text
        assert "omit the WHOLE section" in text
        # Ascending T<PP>.<TT> row ordering + STRICT-downgrade warning.
        assert "ordered ascending by `T<PP>.<TT>`" in text
        assert "⚠ STRICT-downgrade" in text
        # Advisory-only / never auto-applied / never mutates scored tiers.
        assert "NEVER auto-applies" in text
        assert "MUST NOT mutate" in text
        # The exact spec table columns.
        assert (
            "| Task | Scored tier | Feedback-suggested tier | Observed count | Note |"
            in text
        )
        # The §5.3-header pure-function invariant (the P5 fence).
        assert "Pure-function invariant (P5 fence)" in text

    def test_p5_advisory_same_inputs_byte_identical(self, tasklist_skill_text):
        # C6-06: R-9 clause (b) -- same roadmap + same feedback-log -> byte-identical
        # advisory section. The source must state the same-inputs->byte-identical
        # determinism explicitly.
        text = tasklist_skill_text
        assert "same inputs → byte-identical section" in text
        # The reconciled match logic is keyed on the EXISTING feedback-log columns:
        # match on `Task ID`, suggested tier <- `Override Tier`.
        assert (
            "matches a scored task when its **`Task ID`** equals the task's `T<PP>.<TT>`"
            in text
        )
        assert "whose **`Override Tier`** is non-blank AND differs" in text
        # Deterministic per-(Task ID, Override Tier) emission + Observed count semantics.
        assert "one advisory row per distinct `(Task ID, Override Tier)` pair" in text
        assert (
            "`Observed count` for a row is the number of feedback-log rows for that "
            "`(Task ID, Override Tier)` pair"
        ) in text

    def test_p5_advisory_first_run_omission(self, tasklist_skill_text):
        # C6-07: first-run robustness -- absent feedback-log -> whole section omitted,
        # no error (best-effort read). Match the actual authored phrasing.
        text = tasklist_skill_text
        assert "best-effort and READ-ONLY" in text
        assert "when absent, the whole section is omitted, no error" in text
        # C6-04: malformed/empty/partial yields fewer matches; rows missing required
        # fields are ignored; <2 matches -> section omitted, no error.
        assert "Rows missing `Task ID` or `Override Tier` are ignored" in text
        assert "yields fewer matches" in text

    def test_p5_advisory_index_template_mirror(self, index_template_text):
        # C6-08: the index-template mirror must carry the advisory placeholder so
        # mirror drift fails a test (no P5 test previously read index_template_text).
        assert "## Tier Calibration Advisory" in index_template_text
        # The mirror reflects the reconciled match/order semantics.
        assert "`Task ID` equals the task's `T<PP>.<TT>`" in index_template_text
        assert "`Override Tier`" in index_template_text
        assert (
            "ordered ascending by `T<PP>.<TT>` then `Override Tier`"
            in index_template_text
        )

    def test_p5_advisory_does_not_mutate_scored_tiers(self, tasklist_skill_text):
        # R-9: model this as a source-of-truth content gate (the generator logic is
        # prose in SKILL.md, not callable Python) asserting the §5.3-header
        # pure-function invariant + the advisory's explicit non-mutation guarantee.
        # The advisory legitimately varies with feedback-log.md, so the determinism
        # claim is on the SCORED-TIER SLICE only: same roadmap -> same scored tiers,
        # NOT whole-bundle byte-equality across differing feedback logs.
        text = tasklist_skill_text
        # Scored tiers are a pure function of the roadmap; no feedback input.
        assert "scored tiers are a **pure function of the roadmap text**" in text
        assert "NO calibration/feedback input" in text
        assert "MUST NOT read `feedback-log.md`" in text
        # The advisory never feeds back into tier_scores; scored-tier slice is
        # invariant under feedback (same roadmap -> same scored tiers).
        assert "never feeds back into" in text
        assert "same roadmap → same scored tiers" in text


class TestCrossCuttingHygiene:
    """Phase 7 -- sc:task naming + stale-token prevention + carried-gap tests."""

    def test_sc_task_naming(self, tasklist_skill_text):
        text = tasklist_skill_text
        # The generator delegates to the real `sc:task` name ...
        assert "sc:task" in text
        # ... in a real delegate form (non-vacuous: the bare `sc:tasklist`
        # skill name would satisfy a plain `"sc:task" in text` substring check
        # even with every real `sc:task` delegation removed).
        assert "sc:task --compliance strict" in text
        # ... and NEVER the non-existent `sc:task-unified`.
        assert "sc:task-unified" not in text

    def test_no_stale_tokens_in_tasklist_source(self, tasklist_skill_text):
        text = tasklist_skill_text
        # R-12: none of these stale tokens may appear as operative content.
        for token in (
            "sc:task-unified",
            "/rf:",
            ".gfdoc",
            "llm-workflows",
            "/config/.claude",
        ):
            assert token not in text, f"stale token reintroduced: {token}"
        # A typed `StageError` must not be introduced as an operative symbol.
        # The ONLY permitted mention is the explicit no-reuse disclaimer that it
        # does not exist (P3 Stage-7 zero-success branch); no operative form.
        for operative in (
            "raise StageError",
            "class StageError",
            "except StageError",
            "StageError(",
        ):
            assert operative not in text, (
                f"operative StageError introduced: {operative}"
            )
        assert "NOT a reuse of any existing `StageError` symbol" in text
        # The disclaimer is the ONLY permitted `StageError` mention; a second
        # token (e.g. a newly introduced bare mention) must be caught.
        assert text.count("StageError") == 1

    def test_no_reflect_skips_stage_10_5(self, tasklist_skill_text):
        # Carried gap: the --no-reflect (and --dry-run) escape hatch skips the
        # Stage-10.5 pre-reflect advisory entirely.
        text = tasklist_skill_text
        assert "**Skip when disabled.**" in text
        assert (
            "If `--no-reflect` is set (or `--dry-run`), skip this stage entirely"
            in text
        )

    def test_stage_10_5_advisory_ships_all_verdicts(self, tasklist_skill_text):
        # Carried gap: every Stage-10.5 verdict (PASS/PARTIAL/FAIL) is recorded and
        # the bundle ships regardless (the advisory is non-blocking).
        text = tasklist_skill_text
        assert "PASS|PARTIAL|FAIL" in text
        assert "The bundle ships regardless of verdict" in text

    def test_slash_flag_parsing(self):
        # Carried gap: the tasklist CLI flags parse and appear in help, and an
        # invalid flag value produces a non-zero exit (CliRunner model).
        runner = CliRunner()
        help_result = runner.invoke(tasklist_group, ["validate", "--help"])
        assert help_result.exit_code == 0
        for flag in ("--roadmap-file", "--tasklist-dir", "--model", "--max-turns"):
            assert flag in help_result.output
        # An unknown flag is rejected with a non-zero exit.
        bad_result = runner.invoke(tasklist_group, ["validate", "--bogus-flag", "x"])
        assert bad_result.exit_code != 0


# ---------------------------------------------------------------------------
# C06 baseline characterization (item 2.12): the REAL tasklist_run_step path.
#
# tasklist_run_step runs unmodified; only the module-local ClaudeProcess name is
# replaced by an in-memory fake (no subprocess, no model). execute_pipeline is
# never mocked. Expected values are the observed behavior of the current code
# and must stay identical after the C06 helper extraction.
# ---------------------------------------------------------------------------

_TASKLIST_LOGGER = "superclaude.tasklist.executor"
_PREAMBLE_OUTPUT = "Hi\n---\nx: 1\n---\nbody"
_CLEANED_OUTPUT = "---\nx: 1\n---\nbody"


def _install_fake_process(monkeypatch, *, exit_code=0, output=None, polls=None):
    """Replace tasklist executor's module-local ClaudeProcess with a fake.

    ``output`` is written to the step output file on start (what the real CLI
    child would produce). ``polls`` is the sequence returned by
    ``_process.poll()``; None means no live child (``_process`` stays None).
    """
    rec: dict = {"kwargs": None, "events": []}

    class _FakePopen:
        def __init__(self, seq):
            self._seq = list(seq)

        def poll(self):
            rec["events"].append("poll")
            return self._seq.pop(0) if self._seq else 0

    class _FakeClaudeProcess:
        def __init__(self, **kwargs):
            rec["kwargs"] = kwargs
            self._output_file = kwargs["output_file"]
            self._process = None

        def start(self):
            rec["events"].append("start")
            if output is not None:
                self._output_file.write_text(output, encoding="utf-8")
            if polls is not None:
                self._process = _FakePopen(polls)

        def terminate(self):
            rec["events"].append("terminate")

        def wait(self):
            rec["events"].append("wait")
            return exit_code

    monkeypatch.setattr(tasklist_executor, "ClaudeProcess", _FakeClaudeProcess)
    return rec


def _make_step(tmp_path, *, inputs=None, model="", step_id="tasklist-fidelity"):
    return Step(
        id=step_id,
        prompt="PROMPT",
        output_file=tmp_path / "out" / "tasklist-fidelity.md",
        gate=None,
        timeout_seconds=600,
        inputs=list(inputs or []),
        model=model,
    )


def _prepare_out(step):
    step.output_file.parent.mkdir(parents=True, exist_ok=True)


def _records(caplog, name):
    return [r for r in caplog.records if r.name == name]


class TestTasklistRunStepRealPath:
    """G3.14/G3.16 + FR-06(c): real tasklist_run_step with a fake child."""

    def test_success_embeds_inputs_in_order_and_sanitizes(
        self, tmp_path, monkeypatch, caplog
    ):
        p = tmp_path / "p.md"
        p.write_text("", encoding="utf-8")
        q = tmp_path / "q.md"
        q.write_text("é", encoding="utf-8")
        step = _make_step(tmp_path, inputs=[p, p, q], model="step-model")
        _prepare_out(step)
        config = PipelineConfig(
            max_turns=7, model="cfg-model", permission_flag="--perm-x", dry_run=False
        )
        rec = _install_fake_process(monkeypatch, output=_PREAMBLE_OUTPUT)

        with caplog.at_level(logging.DEBUG):
            result = tasklist_executor.tasklist_run_step(step, config, lambda: False)

        expected_prompt = (
            f"PROMPT\n\n# {p}\n```\n\n```\n\n# {p}\n```\n\n```\n\n# {q}\n```\né\n```"
        )
        assert rec["kwargs"] == {
            "prompt": expected_prompt,
            "output_file": step.output_file,
            "error_file": step.output_file.with_suffix(".err"),
            "max_turns": 7,
            "model": "step-model",
            "permission_flag": "--perm-x",
            "timeout_seconds": 600,
            "output_format": "text",
            "extra_args": [],
        }
        # _process is None after start -> no poll loop; wait() exactly once.
        assert rec["events"] == ["start", "wait"]
        assert result.status == StepStatus.PASS
        assert result.step is step
        assert result.attempt == 1
        assert result.gate_failure_reason is None
        assert result.started_at.tzinfo is timezone.utc
        assert result.finished_at.tzinfo is timezone.utc
        assert result.started_at <= result.finished_at
        # Sanitized after exit 0: preamble removed, fixed .tmp gone.
        assert step.output_file.read_text(encoding="utf-8") == _CLEANED_OUTPUT
        assert not step.output_file.with_suffix(".md.tmp").exists()
        info = [
            r for r in _records(caplog, _TASKLIST_LOGGER) if r.levelno == logging.INFO
        ]
        assert [r.getMessage() for r in info] == [
            f"Stripped 3-byte preamble from {step.output_file}"
        ]

    def test_model_falls_back_to_config_and_empty_inputs_use_bare_prompt(
        self, tmp_path, monkeypatch
    ):
        step = _make_step(tmp_path, inputs=[], model="")
        _prepare_out(step)
        rec = _install_fake_process(monkeypatch, output=_CLEANED_OUTPUT)
        config = PipelineConfig(model="cfg-model", dry_run=False)

        result = tasklist_executor.tasklist_run_step(step, config, lambda: False)

        assert result.status == StepStatus.PASS
        assert rec["kwargs"]["prompt"] == "PROMPT"
        assert rec["kwargs"]["model"] == "cfg-model"
        assert rec["kwargs"]["max_turns"] == 100
        assert rec["kwargs"]["permission_flag"] == "--dangerously-skip-permissions"
        assert rec["kwargs"]["extra_args"] == []

    def test_already_frontmatter_output_is_untouched_and_not_logged(
        self, tmp_path, monkeypatch, caplog
    ):
        step = _make_step(tmp_path)
        _prepare_out(step)
        _install_fake_process(monkeypatch, output="  " + _CLEANED_OUTPUT)

        with caplog.at_level(logging.DEBUG):
            result = tasklist_executor.tasklist_run_step(
                step, PipelineConfig(dry_run=False), lambda: False
            )

        assert result.status == StepStatus.PASS
        assert step.output_file.read_text(encoding="utf-8") == "  " + _CLEANED_OUTPUT
        assert _records(caplog, _TASKLIST_LOGGER) == []

    def test_missing_output_still_passes(self, tmp_path, monkeypatch, caplog):
        step = _make_step(tmp_path)
        _prepare_out(step)
        _install_fake_process(monkeypatch, output=None)

        with caplog.at_level(logging.DEBUG):
            result = tasklist_executor.tasklist_run_step(
                step, PipelineConfig(dry_run=False), lambda: False
            )

        assert result.status == StepStatus.PASS
        assert not step.output_file.exists()
        assert _records(caplog, _TASKLIST_LOGGER) == []

    def test_poll_loop_sleeps_one_second_until_child_exits(self, tmp_path, monkeypatch):
        step = _make_step(tmp_path)
        _prepare_out(step)
        rec = _install_fake_process(
            monkeypatch, output=_PREAMBLE_OUTPUT, polls=[None, 0]
        )
        sleeps: list = []
        monkeypatch.setattr(tasklist_executor.time, "sleep", sleeps.append)
        checks: list = []

        def cancel_check():
            checks.append(1)
            return False

        result = tasklist_executor.tasklist_run_step(
            step, PipelineConfig(dry_run=False), cancel_check
        )

        assert result.status == StepStatus.PASS
        assert sleeps == [1]
        assert len(checks) == 1
        assert rec["events"] == ["start", "poll", "poll", "wait"]
        assert step.output_file.read_text(encoding="utf-8") == _CLEANED_OUTPUT


class TestTasklistRunStepBypass:
    """FR-06(c): dry-run, cancel, timeout and nonzero exit skip sanitation."""

    def _spy_sanitize(self, monkeypatch):
        calls: list = []
        monkeypatch.setattr(
            tasklist_executor, "_sanitize_output", lambda p: calls.append(p) or 0
        )
        return calls

    def test_dry_run_skips_embed_process_and_sanitize(
        self, tmp_path, monkeypatch, caplog
    ):
        step = _make_step(tmp_path, inputs=[tmp_path / "never-read.md"])

        def _boom(*a, **k):
            raise AssertionError("must not be called on dry-run")

        monkeypatch.setattr(tasklist_executor, "_embed_inputs", _boom)
        monkeypatch.setattr(tasklist_executor, "ClaudeProcess", _boom)
        monkeypatch.setattr(tasklist_executor, "_sanitize_output", _boom)

        with caplog.at_level(logging.DEBUG):
            result = tasklist_executor.tasklist_run_step(
                step, PipelineConfig(dry_run=True), lambda: False
            )

        assert result.status == StepStatus.PASS
        assert result.attempt == 1
        assert result.gate_failure_reason is None
        assert result.started_at.tzinfo is timezone.utc
        assert result.started_at <= result.finished_at
        assert [r.getMessage() for r in _records(caplog, _TASKLIST_LOGGER)] == [
            "[dry-run] Would execute step 'tasklist-fidelity'"
        ]

    def test_cancel_terminates_without_wait_or_sanitize(self, tmp_path, monkeypatch):
        step = _make_step(tmp_path)
        _prepare_out(step)
        rec = _install_fake_process(monkeypatch, output=_PREAMBLE_OUTPUT, polls=[None])
        calls = self._spy_sanitize(monkeypatch)

        result = tasklist_executor.tasklist_run_step(
            step, PipelineConfig(dry_run=False), lambda: True
        )

        assert result.status == StepStatus.CANCELLED
        assert result.gate_failure_reason == "Cancelled by external signal"
        assert result.attempt == 1
        assert result.started_at <= result.finished_at
        assert rec["events"] == ["start", "poll", "terminate"]
        assert calls == []
        assert step.output_file.read_text(encoding="utf-8") == _PREAMBLE_OUTPUT

    def test_timeout_exit_124_skips_sanitize(self, tmp_path, monkeypatch):
        step = _make_step(tmp_path)
        _prepare_out(step)
        _install_fake_process(monkeypatch, exit_code=124, output=_PREAMBLE_OUTPUT)
        calls = self._spy_sanitize(monkeypatch)

        result = tasklist_executor.tasklist_run_step(
            step, PipelineConfig(dry_run=False), lambda: False
        )

        assert result.status == StepStatus.TIMEOUT
        assert (
            result.gate_failure_reason
            == "Step 'tasklist-fidelity' timed out after 600s"
        )
        assert result.started_at <= result.finished_at
        assert calls == []
        assert step.output_file.read_text(encoding="utf-8") == _PREAMBLE_OUTPUT

    def test_nonzero_exit_skips_sanitize(self, tmp_path, monkeypatch):
        step = _make_step(tmp_path)
        _prepare_out(step)
        _install_fake_process(monkeypatch, exit_code=2, output=_PREAMBLE_OUTPUT)
        calls = self._spy_sanitize(monkeypatch)

        result = tasklist_executor.tasklist_run_step(
            step, PipelineConfig(dry_run=False), lambda: False
        )

        assert result.status == StepStatus.FAIL
        assert (
            result.gate_failure_reason == "Step 'tasklist-fidelity' exited with code 2"
        )
        assert calls == []
        assert step.output_file.read_text(encoding="utf-8") == _PREAMBLE_OUTPUT


class TestTasklistRunStepModuleSeams:
    """Module-local _embed_inputs/_sanitize_output/ClaudeProcess/_log lookups."""

    def test_embed_inputs_looked_up_on_module_at_call_time(self, tmp_path, monkeypatch):
        step = _make_step(tmp_path, inputs=[tmp_path / "a.md"])
        _prepare_out(step)
        seen: list = []

        def _fake_embed(paths):
            seen.append(list(paths))
            return "EMBED"

        monkeypatch.setattr(tasklist_executor, "_embed_inputs", _fake_embed)
        rec = _install_fake_process(monkeypatch, output=_CLEANED_OUTPUT)

        tasklist_executor.tasklist_run_step(
            step, PipelineConfig(dry_run=False), lambda: False
        )

        assert seen == [[tmp_path / "a.md"]]
        assert rec["kwargs"]["prompt"] == "PROMPT\n\nEMBED"

    def test_sanitize_output_looked_up_on_module_after_exit_zero(
        self, tmp_path, monkeypatch
    ):
        step = _make_step(tmp_path)
        _prepare_out(step)
        rec = _install_fake_process(monkeypatch, output=_PREAMBLE_OUTPUT)
        calls: list = []

        def _fake_sanitize(path):
            rec["events"].append("sanitize")
            calls.append(path)
            return 99

        monkeypatch.setattr(tasklist_executor, "_sanitize_output", _fake_sanitize)

        result = tasklist_executor.tasklist_run_step(
            step, PipelineConfig(dry_run=False), lambda: False
        )

        # Return value is discarded; PASS regardless; sanitize runs after wait().
        assert result.status == StepStatus.PASS
        assert calls == [step.output_file]
        assert rec["events"] == ["start", "wait", "sanitize"]
        assert step.output_file.read_text(encoding="utf-8") == _PREAMBLE_OUTPUT

    def test_runtime_reassigned_log_receives_success_message(
        self, tmp_path, monkeypatch, caplog
    ):
        step = _make_step(tmp_path)
        _prepare_out(step)
        _install_fake_process(monkeypatch, output=_PREAMBLE_OUTPUT)
        replacement = logging.getLogger("tests.tasklist.replacement_log")
        monkeypatch.setattr(tasklist_executor, "_log", replacement)

        with caplog.at_level(logging.DEBUG):
            result = tasklist_executor.tasklist_run_step(
                step, PipelineConfig(dry_run=False), lambda: False
            )

        assert result.status == StepStatus.PASS
        assert [
            r.getMessage() for r in _records(caplog, "tests.tasklist.replacement_log")
        ] == [f"Stripped 3-byte preamble from {step.output_file}"]
        assert _records(caplog, _TASKLIST_LOGGER) == []


class TestTasklistValidateRealPipeline:
    """execute_tasklist_validate -> real execute_pipeline -> real run_step."""

    def test_end_to_end_sanitized_report_passes_gate(
        self, tmp_path, monkeypatch, caplog
    ):
        roadmap = tmp_path / "roadmap.md"
        roadmap.write_text("# Roadmap\n", encoding="utf-8")
        tasklist_dir = tmp_path / "tasklists"
        tasklist_dir.mkdir()
        (tasklist_dir / "phase-1.md").write_text("# Phase 1\n", encoding="utf-8")
        out_dir = tmp_path / "out"
        out_dir.mkdir()
        body = "\n".join(f"- line {i}" for i in range(25))
        report = (
            "---\n"
            "high_severity_count: 0\n"
            "medium_severity_count: 0\n"
            "low_severity_count: 0\n"
            "total_deviations: 0\n"
            "validation_complete: true\n"
            "tasklist_ready: true\n"
            "---\n"
            f"## Deviation Report\n{body}\n"
        )
        rec = _install_fake_process(monkeypatch, output="Sure, here it is:\n" + report)
        config = TasklistValidateConfig(
            output_dir=out_dir, roadmap_file=roadmap, tasklist_dir=tasklist_dir
        )

        with caplog.at_level(logging.INFO):
            ok = tasklist_executor.execute_tasklist_validate(config)

        assert ok is True
        assert (out_dir / "tasklist-fidelity.md").read_text(encoding="utf-8") == report
        assert f"# {roadmap}\n```\n# Roadmap\n\n```" in rec["kwargs"]["prompt"]
        assert (
            f"# {tasklist_dir / 'phase-1.md'}\n```\n# Phase 1\n\n```"
            in (rec["kwargs"]["prompt"])
        )
        assert [
            r.getMessage()
            for r in _records(caplog, _TASKLIST_LOGGER)
            if r.getMessage().startswith("Stripped")
        ] == [f"Stripped 18-byte preamble from {out_dir / 'tasklist-fidelity.md'}"]
