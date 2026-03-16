"""Tests for Phase 6 specification pipeline: step-graph-design, models-gates-design,
prompts-executor-design, pipeline-spec-assembly, user-review-p2.

Covers T06.01 through T06.06:
- T06.01: build_step_graph_design_prompt + execute_step_graph_design_step
- T06.02: build_models_gates_design_prompt + execute_models_gates_design_step
- T06.03: build_prompts_executor_design_prompt + execute_prompts_executor_design_step
- T06.04: assemble_specs_programmatic + execute_pipeline_spec_assembly_step
- T06.05: 600s timeout enforcement in STEP_REGISTRY for all 4 Phase 2 steps
- T06.06: execute_user_review_p2 gate + _validate_phase2_approval
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from superclaude.cli.cli_portify.executor import (
    EXIT_RECOMMENDATION_MARKER,
    STEP_REGISTRY,
    _validate_phase2_approval,
    assemble_specs_programmatic,
    execute_models_gates_design_step,
    execute_pipeline_spec_assembly_step,
    execute_prompts_executor_design_step,
    execute_step_graph_design_step,
    execute_user_review_p2,
)
from superclaude.cli.cli_portify.gates import (
    gate_models_gates_design,
    gate_pipeline_spec_assembly,
    gate_prompts_executor_design,
    gate_step_graph_design,
)
from superclaude.cli.cli_portify.models import (
    PortifyStatus,
    PortifyStepResult,
    PortifyValidationError,
)
from superclaude.cli.cli_portify.prompts import (
    build_models_gates_design_prompt,
    build_prompts_executor_design_prompt,
    build_spec_assembly_prompt,
    build_step_graph_design_prompt,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def workdir(tmp_path: Path) -> Path:
    return tmp_path / "workdir"


@pytest.fixture
def workdir_with_analysis(workdir: Path) -> Path:
    workdir.mkdir(parents=True, exist_ok=True)
    (workdir / "portify-analysis-report.md").write_text(
        "---\nstep: analysis-synthesis\ncli_name: test-cli\n---\n"
        "## Source Components\ncontent\n"
        "## Step Graph\ncontent\n"
        "EXIT_RECOMMENDATION: CONTINUE\n",
        encoding="utf-8",
    )
    return workdir


@pytest.fixture
def workdir_with_step_graph(workdir_with_analysis: Path) -> Path:
    (workdir_with_analysis / "step-graph-spec.md").write_text(
        "---\nstep: step-graph-design\ncli_name: test-cli\nstep_count: 5\n---\n"
        "## Step Definitions\n\n"
        "### Step 1: validate-config\n### Step 2: discover\n### Step 3: analyze\n"
        "### Step 4: design\n### Step 5: assemble\n"
        "EXIT_RECOMMENDATION: CONTINUE\n",
        encoding="utf-8",
    )
    return workdir_with_analysis


@pytest.fixture
def workdir_with_models_gates(workdir_with_step_graph: Path) -> Path:
    (workdir_with_step_graph / "models-gates-spec.md").write_text(
        "---\nstep: models-gates-design\ncli_name: test-cli\ngate_count: 5\n---\n"
        "## Data Models\n\n"
        "def gate_check(path: Path) -> tuple[bool, str]:\n"
        "    return True, ''\n",
        encoding="utf-8",
    )
    return workdir_with_step_graph


@pytest.fixture
def workdir_with_all_specs(workdir_with_models_gates: Path) -> Path:
    (workdir_with_models_gates / "prompts-executor-spec.md").write_text(
        "---\nstep: prompts-executor-design\ncli_name: test-cli\nbuilder_count: 5\n---\n"
        "## Prompt Builders\n\n"
        "## Executor Functions\n\n"
        "EXIT_RECOMMENDATION: CONTINUE\n",
        encoding="utf-8",
    )
    return workdir_with_models_gates


@pytest.fixture
def workdir_with_portify_spec(workdir_with_all_specs: Path) -> Path:
    (workdir_with_all_specs / "portify-spec.md").write_text(
        "---\nstep: pipeline-spec-assembly\npipeline_steps: 5\n---\n\n"
        "## Step Mapping\n\n"
        "### Step 1: validate-config\n"
        "### Step 2: discover-components\n"
        "### Step 3: analyze-workflow\n"
        "### Step 4: design-pipeline\n"
        "### Step 5: assemble-spec\n\n"
        "EXIT_RECOMMENDATION: CONTINUE\n",
        encoding="utf-8",
    )
    return workdir_with_all_specs


# ---------------------------------------------------------------------------
# Mock runners
# ---------------------------------------------------------------------------


def _runner_success_with_exit_rec(step_name: str):
    """Factory: create a runner that writes step-specific output with EXIT_RECOMMENDATION."""

    def _runner(prompt: str, output_path: Path):
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            f"---\nstep: {step_name}\ncli_name: test-cli\nstep_count: 5\n"
            f"gate_count: 5\nbuilder_count: 5\npipeline_steps: 5\n---\n\n"
            f"## Step Mapping\n\n"
            f"### Step 1: validate-config\n"
            f"### Step 2: discover\n"
            f"### Step 3: analyze\n"
            f"### Step 4: design\n"
            f"### Step 5: assemble\n\n"
            f"def gate_fn(path: Path) -> tuple[bool, str]:\n"
            f"    return True, ''\n\n"
            f"EXIT_RECOMMENDATION: CONTINUE\n",
            encoding="utf-8",
        )
        return 0, EXIT_RECOMMENDATION_MARKER + " CONTINUE", False

    return _runner


def _runner_success_with_return_type(prompt: str, output_path: Path):
    """Runner that writes output with return type pattern (for G-006).

    Includes EXIT_RECOMMENDATION in stdout so _determine_status yields PASS.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        "---\nstep: models-gates-design\ncli_name: test-cli\ngate_count: 3\n---\n\n"
        "## Gate Functions\n\n"
        "def gate_validate(path: Path) -> tuple[bool, str]:\n"
        "    return True, ''\n\n"
        "EXIT_RECOMMENDATION: CONTINUE\n",
        encoding="utf-8",
    )
    return 0, EXIT_RECOMMENDATION_MARKER + " CONTINUE", False


def _runner_timeout(prompt: str, output_path: Path):
    return 124, "", True


def _runner_no_signal(prompt: str, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("---\nstep: test\n---\ncontent", encoding="utf-8")
    return 0, "", False


# ---------------------------------------------------------------------------
# T06.01: step_graph prompt builder
# ---------------------------------------------------------------------------


class TestStepGraphDesignPrompt:
    """Tests for build_step_graph_design_prompt (T06.01, FR-020)."""

    def test_step_graph_prompt_not_empty(self):
        prompt = build_step_graph_design_prompt("my-cli", "## Analysis\ncontent")
        assert len(prompt) > 0

    def test_step_graph_prompt_contains_cli_name(self):
        prompt = build_step_graph_design_prompt("my-cli", "## Analysis\ncontent")
        assert "my-cli" in prompt

    def test_step_graph_prompt_references_analysis_report_content(self):
        analysis_content = "## Step Graph\nStep 1: validate"
        prompt = build_step_graph_design_prompt("my-cli", analysis_content)
        assert "Step 1: validate" in prompt

    def test_step_graph_prompt_contains_exit_recommendation_instruction(self):
        prompt = build_step_graph_design_prompt("my-cli", "content")
        assert "EXIT_RECOMMENDATION" in prompt

    def test_step_graph_prompt_contains_yaml_frontmatter_requirement(self):
        prompt = build_step_graph_design_prompt("my-cli", "content")
        assert "---" in prompt
        assert "step: step-graph-design" in prompt

    def test_step_graph_prompt_with_empty_analysis(self):
        prompt = build_step_graph_design_prompt("my-cli", "")
        assert len(prompt) > 0
        assert "my-cli" in prompt


# ---------------------------------------------------------------------------
# T06.01: step_graph step execution
# ---------------------------------------------------------------------------


class TestStepGraphExecution:
    """Tests for execute_step_graph_design_step (T06.01, FR-020)."""

    def test_step_graph_produces_artifact(self, workdir_with_analysis):
        result = execute_step_graph_design_step(
            "test-cli",
            workdir_with_analysis,
            process_runner=_runner_success_with_exit_rec("step-graph-design"),
        )
        assert (workdir_with_analysis / "step-graph-spec.md").exists()
        assert result.step_name == "step-graph-design"

    def test_step_graph_pass_status_with_exit_rec(self, workdir_with_analysis):
        result = execute_step_graph_design_step(
            "test-cli",
            workdir_with_analysis,
            process_runner=_runner_success_with_exit_rec("step-graph-design"),
        )
        assert result.portify_status == PortifyStatus.PASS

    def test_step_graph_reads_analysis_report(self, workdir_with_analysis):
        captured = {"prompt": None}

        def _capture_runner(prompt: str, output_path: Path):
            captured["prompt"] = prompt
            return _runner_success_with_exit_rec("step-graph-design")(prompt, output_path)

        execute_step_graph_design_step(
            "test-cli",
            workdir_with_analysis,
            process_runner=_capture_runner,
        )
        assert captured["prompt"] is not None
        assert "EXIT_RECOMMENDATION" in captured["prompt"]

    def test_step_graph_timeout_classification(self, workdir_with_analysis):
        result = execute_step_graph_design_step(
            "test-cli",
            workdir_with_analysis,
            process_runner=_runner_timeout,
        )
        assert result.portify_status == PortifyStatus.TIMEOUT

    def test_step_graph_artifact_path_set(self, workdir_with_analysis):
        result = execute_step_graph_design_step(
            "test-cli",
            workdir_with_analysis,
            process_runner=_runner_success_with_exit_rec("step-graph-design"),
        )
        assert "step-graph-spec.md" in result.artifact_path

    def test_step_graph_gate_tier_strict(self, workdir_with_analysis):
        result = execute_step_graph_design_step(
            "test-cli",
            workdir_with_analysis,
            process_runner=_runner_success_with_exit_rec("step-graph-design"),
        )
        assert result.gate_tier == "STRICT"

    def test_step_graph_retry_on_pass_no_signal(self, workdir_with_analysis):
        call_count = {"n": 0}

        def _runner_first_no_signal_then_pass(prompt: str, output_path: Path):
            call_count["n"] += 1
            output_path.parent.mkdir(parents=True, exist_ok=True)
            if call_count["n"] == 1:
                output_path.write_text("---\nstep: test\n---\ncontent", encoding="utf-8")
                return 0, "", False
            return _runner_success_with_exit_rec("step-graph-design")(prompt, output_path)

        execute_step_graph_design_step(
            "test-cli",
            workdir_with_analysis,
            process_runner=_runner_first_no_signal_then_pass,
        )
        assert call_count["n"] == 2


# ---------------------------------------------------------------------------
# T06.02: models_gates prompt builder
# ---------------------------------------------------------------------------


class TestModelsGatesDesignPrompt:
    """Tests for build_models_gates_design_prompt (T06.02, FR-021)."""

    def test_models_gates_prompt_not_empty(self):
        prompt = build_models_gates_design_prompt("my-cli", "## Steps\ncontent")
        assert len(prompt) > 0

    def test_models_gates_prompt_contains_cli_name(self):
        prompt = build_models_gates_design_prompt("my-cli", "content")
        assert "my-cli" in prompt

    def test_models_gates_prompt_references_step_graph_content(self):
        step_graph = "## Step Definitions\nStep 1: validate"
        prompt = build_models_gates_design_prompt("my-cli", step_graph)
        assert "Step 1: validate" in prompt

    def test_models_gates_prompt_contains_return_type_requirement(self):
        prompt = build_models_gates_design_prompt("my-cli", "content")
        assert "tuple[bool, str]" in prompt

    def test_models_gates_prompt_contains_yaml_frontmatter_requirement(self):
        prompt = build_models_gates_design_prompt("my-cli", "content")
        assert "---" in prompt
        assert "step: models-gates-design" in prompt


# ---------------------------------------------------------------------------
# T06.02: models_gates step execution
# ---------------------------------------------------------------------------


class TestModelsGatesExecution:
    """Tests for execute_models_gates_design_step (T06.02, FR-021)."""

    def test_models_gates_produces_artifact(self, workdir_with_step_graph):
        result = execute_models_gates_design_step(
            "test-cli",
            workdir_with_step_graph,
            process_runner=_runner_success_with_return_type,
        )
        assert (workdir_with_step_graph / "models-gates-spec.md").exists()
        assert result.step_name == "models-gates-design"

    def test_models_gates_pass_status_with_return_type(self, workdir_with_step_graph):
        result = execute_models_gates_design_step(
            "test-cli",
            workdir_with_step_graph,
            process_runner=_runner_success_with_return_type,
        )
        assert result.portify_status == PortifyStatus.PASS

    def test_models_gates_reads_step_graph(self, workdir_with_step_graph):
        captured = {"prompt": None}

        def _capture_runner(prompt: str, output_path: Path):
            captured["prompt"] = prompt
            return _runner_success_with_return_type(prompt, output_path)

        execute_models_gates_design_step(
            "test-cli",
            workdir_with_step_graph,
            process_runner=_capture_runner,
        )
        assert captured["prompt"] is not None
        assert "test-cli" in captured["prompt"]

    def test_models_gates_timeout_classification(self, workdir_with_step_graph):
        result = execute_models_gates_design_step(
            "test-cli",
            workdir_with_step_graph,
            process_runner=_runner_timeout,
        )
        assert result.portify_status == PortifyStatus.TIMEOUT

    def test_models_gates_artifact_path_set(self, workdir_with_step_graph):
        result = execute_models_gates_design_step(
            "test-cli",
            workdir_with_step_graph,
            process_runner=_runner_success_with_return_type,
        )
        assert "models-gates-spec.md" in result.artifact_path

    def test_models_gates_gate_tier_standard(self, workdir_with_step_graph):
        result = execute_models_gates_design_step(
            "test-cli",
            workdir_with_step_graph,
            process_runner=_runner_success_with_return_type,
        )
        assert result.gate_tier == "STANDARD"


# ---------------------------------------------------------------------------
# T06.03: prompts_executor prompt builder
# ---------------------------------------------------------------------------


class TestPromptsExecutorDesignPrompt:
    """Tests for build_prompts_executor_design_prompt (T06.03, FR-022)."""

    def test_prompts_executor_prompt_not_empty(self):
        prompt = build_prompts_executor_design_prompt("my-cli", "step graph", "models gates")
        assert len(prompt) > 0

    def test_prompts_executor_prompt_contains_cli_name(self):
        prompt = build_prompts_executor_design_prompt("my-cli", "content", "content")
        assert "my-cli" in prompt

    def test_prompts_executor_prompt_references_step_graph(self):
        step_graph = "## Steps\nStep 1: validate"
        prompt = build_prompts_executor_design_prompt("my-cli", step_graph, "")
        assert "Step 1: validate" in prompt

    def test_prompts_executor_prompt_references_models_gates(self):
        models_gates = "## Gates\ndef gate_validate()"
        prompt = build_prompts_executor_design_prompt("my-cli", "", models_gates)
        assert "gate_validate" in prompt

    def test_prompts_executor_prompt_contains_exit_recommendation_instruction(self):
        prompt = build_prompts_executor_design_prompt("my-cli", "content", "content")
        assert "EXIT_RECOMMENDATION" in prompt

    def test_prompts_executor_prompt_contains_yaml_frontmatter_requirement(self):
        prompt = build_prompts_executor_design_prompt("my-cli", "content", "content")
        assert "---" in prompt
        assert "step: prompts-executor-design" in prompt


# ---------------------------------------------------------------------------
# T06.03: prompts_executor step execution
# ---------------------------------------------------------------------------


class TestPromptsExecutorExecution:
    """Tests for execute_prompts_executor_design_step (T06.03, FR-022)."""

    def test_prompts_executor_produces_artifact(self, workdir_with_models_gates):
        result = execute_prompts_executor_design_step(
            "test-cli",
            workdir_with_models_gates,
            process_runner=_runner_success_with_exit_rec("prompts-executor-design"),
        )
        assert (workdir_with_models_gates / "prompts-executor-spec.md").exists()
        assert result.step_name == "prompts-executor-design"

    def test_prompts_executor_pass_status_with_exit_rec(self, workdir_with_models_gates):
        result = execute_prompts_executor_design_step(
            "test-cli",
            workdir_with_models_gates,
            process_runner=_runner_success_with_exit_rec("prompts-executor-design"),
        )
        assert result.portify_status == PortifyStatus.PASS

    def test_prompts_executor_reads_both_inputs(self, workdir_with_models_gates):
        captured = {"prompt": None}

        def _capture_runner(prompt: str, output_path: Path):
            captured["prompt"] = prompt
            return _runner_success_with_exit_rec("prompts-executor-design")(prompt, output_path)

        execute_prompts_executor_design_step(
            "test-cli",
            workdir_with_models_gates,
            process_runner=_capture_runner,
        )
        assert captured["prompt"] is not None
        assert "test-cli" in captured["prompt"]

    def test_prompts_executor_timeout_classification(self, workdir_with_models_gates):
        result = execute_prompts_executor_design_step(
            "test-cli",
            workdir_with_models_gates,
            process_runner=_runner_timeout,
        )
        assert result.portify_status == PortifyStatus.TIMEOUT

    def test_prompts_executor_gate_tier_strict(self, workdir_with_models_gates):
        result = execute_prompts_executor_design_step(
            "test-cli",
            workdir_with_models_gates,
            process_runner=_runner_success_with_exit_rec("prompts-executor-design"),
        )
        assert result.gate_tier == "STRICT"


# ---------------------------------------------------------------------------
# T06.04: spec_assembly programmatic assembler
# ---------------------------------------------------------------------------


class TestAssembleSpecsProgrammatic:
    """Tests for assemble_specs_programmatic (T06.04, FR-023, SC-005)."""

    def test_assemble_combines_three_sections(self):
        result = assemble_specs_programmatic("step graph", "models gates", "prompts executor")
        assert "step graph" in result
        assert "models gates" in result
        assert "prompts executor" in result

    def test_assemble_adds_section_headers(self):
        result = assemble_specs_programmatic("sg content", "mg content", "pe content")
        assert "## Step Graph Design" in result
        assert "## Models and Gates Design" in result
        assert "## Prompts and Executor Design" in result

    def test_assemble_empty_inputs_handled(self):
        result = assemble_specs_programmatic("", "", "")
        assert isinstance(result, str)

    def test_assemble_deduplicates_frontmatter(self):
        fm = "---\nstep: test\ncli_name: x\n---\n"
        result = assemble_specs_programmatic(
            fm + "content1", fm + "content2", fm + "content3"
        )
        # After deduplication, only one frontmatter block should remain
        fm_count = result.count("step: test")
        assert fm_count <= 1

    def test_assemble_partial_inputs_handled(self):
        result = assemble_specs_programmatic("step graph content", "", "prompts content")
        assert "step graph content" in result
        assert "prompts content" in result
        assert "## Models and Gates Design" not in result


# ---------------------------------------------------------------------------
# T06.04: spec_assembly step execution
# ---------------------------------------------------------------------------


class TestPipelineSpecAssemblyExecution:
    """Tests for execute_pipeline_spec_assembly_step (T06.04, FR-023, SC-005)."""

    def test_spec_assembly_produces_portify_spec(self, workdir_with_all_specs):
        result = execute_pipeline_spec_assembly_step(
            "test-cli",
            workdir_with_all_specs,
            process_runner=_runner_success_with_exit_rec("pipeline-spec-assembly"),
        )
        assert (workdir_with_all_specs / "portify-spec.md").exists()
        assert result.step_name == "pipeline-spec-assembly"

    def test_spec_assembly_pass_status_with_exit_rec(self, workdir_with_all_specs):
        result = execute_pipeline_spec_assembly_step(
            "test-cli",
            workdir_with_all_specs,
            process_runner=_runner_success_with_exit_rec("pipeline-spec-assembly"),
        )
        assert result.portify_status == PortifyStatus.PASS

    def test_spec_assembly_reads_all_three_inputs(self, workdir_with_all_specs):
        captured = {"prompt": None}

        def _capture_runner(prompt: str, output_path: Path):
            captured["prompt"] = prompt
            return _runner_success_with_exit_rec("pipeline-spec-assembly")(prompt, output_path)

        execute_pipeline_spec_assembly_step(
            "test-cli",
            workdir_with_all_specs,
            process_runner=_capture_runner,
        )
        assert captured["prompt"] is not None
        # All three input specs should be referenced in the assembled prompt
        assert "Step Graph Design" in captured["prompt"]
        assert "Models and Gates Design" in captured["prompt"]
        assert "Prompts and Executor Design" in captured["prompt"]

    def test_spec_assembly_timeout_classification(self, workdir_with_all_specs):
        result = execute_pipeline_spec_assembly_step(
            "test-cli",
            workdir_with_all_specs,
            process_runner=_runner_timeout,
        )
        assert result.portify_status == PortifyStatus.TIMEOUT

    def test_spec_assembly_gate_tier_strict(self, workdir_with_all_specs):
        result = execute_pipeline_spec_assembly_step(
            "test-cli",
            workdir_with_all_specs,
            process_runner=_runner_success_with_exit_rec("pipeline-spec-assembly"),
        )
        assert result.gate_tier == "STRICT"

    def test_spec_assembly_artifact_path_set(self, workdir_with_all_specs):
        result = execute_pipeline_spec_assembly_step(
            "test-cli",
            workdir_with_all_specs,
            process_runner=_runner_success_with_exit_rec("pipeline-spec-assembly"),
        )
        assert "portify-spec.md" in result.artifact_path


# ---------------------------------------------------------------------------
# T06.05: phase2_timeout — 600s timeout enforcement in STEP_REGISTRY
# ---------------------------------------------------------------------------


class TestPhase2Timeout:
    """Tests for 600s timeout on Phase 2 spec steps (T06.05, NFR-001).

    Test names include 'phase2_timeout' to match -k filter per T06.05 acceptance criteria.
    """

    def test_phase2_timeout_step_graph_design_registry(self):
        assert STEP_REGISTRY["step-graph-design"]["timeout_s"] == 600

    def test_phase2_timeout_models_gates_design_registry(self):
        assert STEP_REGISTRY["models-gates-design"]["timeout_s"] == 600

    def test_phase2_timeout_prompts_executor_design_registry(self):
        assert STEP_REGISTRY["prompts-executor-design"]["timeout_s"] == 600

    def test_phase2_timeout_pipeline_spec_assembly_registry(self):
        assert STEP_REGISTRY["pipeline-spec-assembly"]["timeout_s"] == 600

    def test_phase2_timeout_all_four_steps_registered(self):
        assert "step-graph-design" in STEP_REGISTRY
        assert "models-gates-design" in STEP_REGISTRY
        assert "prompts-executor-design" in STEP_REGISTRY
        assert "pipeline-spec-assembly" in STEP_REGISTRY

    def test_phase2_timeout_step_graph_iteration_timeout_recorded(self, workdir_with_analysis):
        result = execute_step_graph_design_step(
            "test-cli",
            workdir_with_analysis,
            process_runner=_runner_success_with_exit_rec("step-graph-design"),
        )
        assert result.iteration_timeout == 600

    def test_phase2_timeout_models_gates_iteration_timeout_recorded(self, workdir_with_step_graph):
        result = execute_models_gates_design_step(
            "test-cli",
            workdir_with_step_graph,
            process_runner=_runner_success_with_return_type,
        )
        assert result.iteration_timeout == 600

    def test_phase2_timeout_prompts_executor_iteration_timeout_recorded(
        self, workdir_with_models_gates
    ):
        result = execute_prompts_executor_design_step(
            "test-cli",
            workdir_with_models_gates,
            process_runner=_runner_success_with_exit_rec("prompts-executor-design"),
        )
        assert result.iteration_timeout == 600

    def test_phase2_timeout_spec_assembly_iteration_timeout_recorded(self, workdir_with_all_specs):
        result = execute_pipeline_spec_assembly_step(
            "test-cli",
            workdir_with_all_specs,
            process_runner=_runner_success_with_exit_rec("pipeline-spec-assembly"),
        )
        assert result.iteration_timeout == 600

    def test_phase2_timeout_step_graph_exit_124(self, workdir_with_analysis):
        result = execute_step_graph_design_step(
            "test-cli",
            workdir_with_analysis,
            process_runner=_runner_timeout,
        )
        assert result.portify_status == PortifyStatus.TIMEOUT


# ---------------------------------------------------------------------------
# T06.05: phase2_exit_rec — EXIT_RECOMMENDATION gate enforcement
# ---------------------------------------------------------------------------


class TestPhase2ExitRecEnforcement:
    """Tests for per-gate EXIT_RECOMMENDATION enforcement (T06.05, FR-024, NFR-001).

    Test names include 'phase2_exit_rec' to match -k filter per T06.05 acceptance criteria.
    """

    def test_phase2_exit_rec_g005_step_graph_passes_with_marker(self, tmp_path):
        artifact = tmp_path / "step-graph-spec.md"
        artifact.write_text(
            "---\nstep: step-graph-design\ncli_name: x\nstep_count: 3\n---\ncontent\n"
            "EXIT_RECOMMENDATION: CONTINUE\n",
            encoding="utf-8",
        )
        passed, _ = gate_step_graph_design(artifact)
        assert passed is True

    def test_phase2_exit_rec_g005_step_graph_fails_without_marker(self, tmp_path):
        artifact = tmp_path / "step-graph-spec.md"
        artifact.write_text(
            "---\nstep: step-graph-design\ncli_name: x\nstep_count: 3\n---\ncontent\n",
            encoding="utf-8",
        )
        passed, diagnostic = gate_step_graph_design(artifact)
        assert passed is False
        assert "EXIT_RECOMMENDATION" in diagnostic

    def test_phase2_exit_rec_g006_models_gates_passes_with_return_type(self, tmp_path):
        artifact = tmp_path / "models-gates-spec.md"
        artifact.write_text(
            "---\nstep: models-gates-design\ncli_name: x\ngate_count: 3\n---\n"
            "def gate_fn(p: Path) -> tuple[bool, str]: return True, ''\n",
            encoding="utf-8",
        )
        passed, _ = gate_models_gates_design(artifact)
        assert passed is True

    def test_phase2_exit_rec_g006_models_gates_fails_without_return_type(self, tmp_path):
        artifact = tmp_path / "models-gates-spec.md"
        artifact.write_text(
            "---\nstep: models-gates-design\ncli_name: x\ngate_count: 3\n---\ncontent only\n",
            encoding="utf-8",
        )
        passed, diagnostic = gate_models_gates_design(artifact)
        assert passed is False
        assert "return type" in diagnostic.lower() or "tuple" in diagnostic.lower()

    def test_phase2_exit_rec_g007_prompts_executor_passes_with_marker(self, tmp_path):
        artifact = tmp_path / "prompts-executor-spec.md"
        artifact.write_text(
            "---\nstep: prompts-executor-design\ncli_name: x\nbuilder_count: 3\n---\ncontent\n"
            "EXIT_RECOMMENDATION: CONTINUE\n",
            encoding="utf-8",
        )
        passed, _ = gate_prompts_executor_design(artifact)
        assert passed is True

    def test_phase2_exit_rec_g007_prompts_executor_fails_without_marker(self, tmp_path):
        artifact = tmp_path / "prompts-executor-spec.md"
        artifact.write_text(
            "---\nstep: prompts-executor-design\ncli_name: x\nbuilder_count: 3\n---\ncontent\n",
            encoding="utf-8",
        )
        passed, diagnostic = gate_prompts_executor_design(artifact)
        assert passed is False
        assert "EXIT_RECOMMENDATION" in diagnostic

    def test_phase2_exit_rec_g008_spec_assembly_passes_with_marker_and_consistent_steps(
        self, tmp_path
    ):
        artifact = tmp_path / "portify-spec.md"
        artifact.write_text(
            "---\nstep: pipeline-spec-assembly\npipeline_steps: 3\n---\n\n"
            "## Step Mapping\n\n"
            "### Step 1: validate\n### Step 2: analyze\n### Step 3: assemble\n\n"
            "EXIT_RECOMMENDATION: CONTINUE\n",
            encoding="utf-8",
        )
        passed, _ = gate_pipeline_spec_assembly(artifact)
        assert passed is True

    def test_phase2_exit_rec_g008_spec_assembly_fails_without_marker(self, tmp_path):
        artifact = tmp_path / "portify-spec.md"
        artifact.write_text(
            "---\nstep: pipeline-spec-assembly\npipeline_steps: 3\n---\ncontent\n",
            encoding="utf-8",
        )
        passed, diagnostic = gate_pipeline_spec_assembly(artifact)
        assert passed is False
        assert "EXIT_RECOMMENDATION" in diagnostic

    def test_phase2_exit_rec_g008_spec_assembly_fails_on_step_count_mismatch(self, tmp_path):
        artifact = tmp_path / "portify-spec.md"
        # Declares 5 steps but only defines 2
        artifact.write_text(
            "---\nstep: pipeline-spec-assembly\npipeline_steps: 5\n---\n\n"
            "## Step Mapping\n\n"
            "### Step 1: validate\n### Step 2: analyze\n\n"
            "EXIT_RECOMMENDATION: CONTINUE\n",
            encoding="utf-8",
        )
        passed, diagnostic = gate_pipeline_spec_assembly(artifact)
        assert passed is False
        assert "mismatch" in diagnostic.lower() or "count" in diagnostic.lower()

    def test_phase2_exit_rec_g005_returns_false_for_missing_artifact(self, tmp_path):
        artifact = tmp_path / "does-not-exist.md"
        passed, _ = gate_step_graph_design(artifact)
        assert passed is False

    def test_phase2_exit_rec_g006_returns_false_for_missing_artifact(self, tmp_path):
        artifact = tmp_path / "does-not-exist.md"
        passed, _ = gate_models_gates_design(artifact)
        assert passed is False

    def test_phase2_exit_rec_g007_returns_false_for_missing_artifact(self, tmp_path):
        artifact = tmp_path / "does-not-exist.md"
        passed, _ = gate_prompts_executor_design(artifact)
        assert passed is False

    def test_phase2_exit_rec_g008_returns_false_for_missing_artifact(self, tmp_path):
        artifact = tmp_path / "does-not-exist.md"
        passed, _ = gate_pipeline_spec_assembly(artifact)
        assert passed is False


# ---------------------------------------------------------------------------
# T06.06: phase2_approval — execute_user_review_p2
# ---------------------------------------------------------------------------


class TestPhase2Approval:
    """Tests for execute_user_review_p2 (T06.06, FR-025, SC-006).

    Test names include 'phase2_approval' to match -k filter per T06.06 acceptance criteria.
    """

    def test_phase2_approval_writes_completed_yaml(self, workdir_with_portify_spec):
        execute_user_review_p2("test-cli", workdir_with_portify_spec, _exit=False)
        approval_path = workdir_with_portify_spec / "phase2-approval.yaml"
        assert approval_path.exists()
        data = yaml.safe_load(approval_path.read_text())
        assert data["status"] == "completed"

    def test_phase2_approval_yaml_contains_workflow(self, workdir_with_portify_spec):
        execute_user_review_p2("my-workflow", workdir_with_portify_spec, _exit=False)
        data = yaml.safe_load(
            (workdir_with_portify_spec / "phase2-approval.yaml").read_text()
        )
        assert data["workflow"] == "my-workflow"

    def test_phase2_approval_yaml_contains_review_artifacts(self, workdir_with_portify_spec):
        execute_user_review_p2("test-cli", workdir_with_portify_spec, _exit=False)
        data = yaml.safe_load(
            (workdir_with_portify_spec / "phase2-approval.yaml").read_text()
        )
        artifacts = data["review_artifacts"]
        assert "portify-spec.md" in artifacts
        assert "step-graph-spec.md" in artifacts

    def test_phase2_approval_prints_resume_instructions(self, workdir_with_portify_spec, capsys):
        execute_user_review_p2("test-cli", workdir_with_portify_spec, _exit=False)
        captured = capsys.readouterr()
        assert "superclaude cli-portify run" in captured.out
        assert "--resume" in captured.out

    def test_phase2_approval_creates_workdir_if_missing(self, tmp_path):
        portify_spec_dir = tmp_path / "new_workdir"
        portify_spec_dir.mkdir()
        (portify_spec_dir / "portify-spec.md").write_text(
            "---\nstep: pipeline-spec-assembly\npipeline_steps: 2\n---\n\n"
            "## Step Mapping\n\n"
            "### Step 1: validate\n### Step 2: analyze\n",
            encoding="utf-8",
        )
        execute_user_review_p2("test-cli", portify_spec_dir, _exit=False)
        assert (portify_spec_dir / "phase2-approval.yaml").exists()

    def test_phase2_approval_raises_when_portify_spec_missing(self, workdir):
        workdir.mkdir(parents=True, exist_ok=True)
        with pytest.raises(PortifyValidationError) as exc_info:
            execute_user_review_p2("test-cli", workdir, _exit=False)
        assert "portify-spec.md" in str(exc_info.value).lower()

    def test_phase2_approval_raises_when_step_mapping_empty(self, workdir):
        workdir.mkdir(parents=True, exist_ok=True)
        (workdir / "portify-spec.md").write_text(
            "---\nstep: pipeline-spec-assembly\npipeline_steps: 0\n---\n\n"
            "## Step Mapping\n\n",
            encoding="utf-8",
        )
        with pytest.raises(PortifyValidationError) as exc_info:
            execute_user_review_p2("test-cli", workdir, _exit=False)
        assert "step mapping" in str(exc_info.value).lower() or "empty" in str(exc_info.value).lower()

    def test_phase2_approval_raises_when_blocking_gate_not_passed(
        self, workdir_with_portify_spec
    ):
        failed_result = PortifyStepResult(
            step_name="step-graph-design",
            portify_status=PortifyStatus.FAIL,
        )
        with pytest.raises(PortifyValidationError) as exc_info:
            execute_user_review_p2(
                "test-cli",
                workdir_with_portify_spec,
                step_results=[failed_result],
                _exit=False,
            )
        assert "step-graph-design" in str(exc_info.value)

    def test_phase2_approval_passes_when_all_gates_passed(self, workdir_with_portify_spec):
        passed_results = [
            PortifyStepResult(
                step_name="step-graph-design",
                portify_status=PortifyStatus.PASS,
            ),
            PortifyStepResult(
                step_name="models-gates-design",
                portify_status=PortifyStatus.PASS,
            ),
            PortifyStepResult(
                step_name="prompts-executor-design",
                portify_status=PortifyStatus.PASS,
            ),
            PortifyStepResult(
                step_name="pipeline-spec-assembly",
                portify_status=PortifyStatus.PASS,
            ),
        ]
        # Should not raise
        execute_user_review_p2(
            "test-cli",
            workdir_with_portify_spec,
            step_results=passed_results,
            _exit=False,
        )
        approval = workdir_with_portify_spec / "phase2-approval.yaml"
        assert approval.exists()


# ---------------------------------------------------------------------------
# T06.06: user_review_p2 resume validation — _validate_phase2_approval
# ---------------------------------------------------------------------------


class TestResumeValidationPhase2:
    """Tests for _validate_phase2_approval (T06.06, FR-026, SC-007)."""

    def test_user_review_p2_completed_passes(self, workdir):
        workdir.mkdir(parents=True, exist_ok=True)
        (workdir / "phase2-approval.yaml").write_text(
            "status: completed\nworkflow: test\n", encoding="utf-8"
        )
        # Should not raise
        _validate_phase2_approval(workdir)

    def test_user_review_p2_pending_raises_error(self, workdir):
        workdir.mkdir(parents=True, exist_ok=True)
        (workdir / "phase2-approval.yaml").write_text(
            "status: pending\nworkflow: test\n", encoding="utf-8"
        )
        with pytest.raises(PortifyValidationError) as exc_info:
            _validate_phase2_approval(workdir)
        assert "completed" in str(exc_info.value).lower()

    def test_user_review_p2_missing_file_raises_error(self, workdir):
        workdir.mkdir(parents=True, exist_ok=True)
        with pytest.raises(PortifyValidationError):
            _validate_phase2_approval(workdir)

    def test_user_review_p2_malformed_yaml_raises_error(self, workdir):
        workdir.mkdir(parents=True, exist_ok=True)
        (workdir / "phase2-approval.yaml").write_text(
            "status: [invalid: yaml: here\n", encoding="utf-8"
        )
        with pytest.raises(PortifyValidationError) as exc_info:
            _validate_phase2_approval(workdir)
        assert "malformed" in str(exc_info.value).lower() or "yaml" in str(exc_info.value).lower()

    def test_user_review_p2_missing_status_field_raises_error(self, workdir):
        workdir.mkdir(parents=True, exist_ok=True)
        (workdir / "phase2-approval.yaml").write_text(
            "workflow: test\nnotes: some notes\n", encoding="utf-8"
        )
        with pytest.raises(PortifyValidationError) as exc_info:
            _validate_phase2_approval(workdir)
        assert "status" in str(exc_info.value).lower()

    def test_user_review_p2_non_mapping_yaml_raises_error(self, workdir):
        workdir.mkdir(parents=True, exist_ok=True)
        (workdir / "phase2-approval.yaml").write_text(
            "- item1\n- item2\n", encoding="utf-8"
        )
        with pytest.raises(PortifyValidationError):
            _validate_phase2_approval(workdir)

    def test_user_review_p2_error_code_is_invalid_path(self, workdir):
        workdir.mkdir(parents=True, exist_ok=True)
        (workdir / "phase2-approval.yaml").write_text(
            "status: pending\n", encoding="utf-8"
        )
        with pytest.raises(PortifyValidationError) as exc_info:
            _validate_phase2_approval(workdir)
        assert exc_info.value.error_code == "INVALID_PATH"
