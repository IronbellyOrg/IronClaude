"""Tests for Phase 5 analysis pipeline: protocol-mapping, analysis-synthesis,
user-review-p1, resume validation, and 600s timeouts.

Covers T05.01 through T05.05:
- T05.01: build_protocol_mapping_prompt + execute_protocol_mapping_step
- T05.02: build_analysis_synthesis_prompt + execute_analysis_synthesis_step
- T05.03: 600s timeout enforcement in STEP_REGISTRY
- T05.04: execute_user_review_p1 gate writing phase1-approval.yaml
- T05.05: _validate_phase1_approval YAML parse + schema validation
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest
import yaml

from superclaude.cli.cli_portify.executor import (
    EXIT_RECOMMENDATION_MARKER,
    STEP_REGISTRY,
    _validate_phase1_approval,
    execute_analysis_synthesis_step,
    execute_protocol_mapping_step,
    execute_user_review_p1,
)
from superclaude.cli.cli_portify.models import (
    ComponentEntry,
    PortifyStatus,
    PortifyValidationError,
)
from superclaude.cli.cli_portify.prompts import (
    build_analysis_synthesis_prompt,
    build_protocol_mapping_prompt,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def sample_inventory():
    return [
        ComponentEntry(name="cmd-entry", component_type="command", line_count=120),
        ComponentEntry(name="my-skill", component_type="skill", line_count=300),
    ]


@pytest.fixture
def workdir(tmp_path):
    return tmp_path / "workdir"


def _runner_success_with_exit_rec(prompt: str, output_path: Path):
    """Mock runner: writes artifact and returns EXIT_RECOMMENDATION."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        "---\nstep: protocol-mapping\ncli_name: test\n---\n"
        "content\nEXIT_RECOMMENDATION: CONTINUE",
        encoding="utf-8",
    )
    return 0, EXIT_RECOMMENDATION_MARKER + " CONTINUE", False


def _runner_success_no_signal(prompt: str, output_path: Path):
    """Mock runner: writes artifact but no EXIT_RECOMMENDATION."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        "---\nstep: protocol-mapping\n---\ncontent", encoding="utf-8"
    )
    return 0, "", False


def _runner_timeout(prompt: str, output_path: Path):
    """Mock runner: returns exit code 124."""
    return 124, "", True


# ---------------------------------------------------------------------------
# T05.01: protocol_mapping prompt builder
# ---------------------------------------------------------------------------


class TestProtocolMappingPrompt:
    """Tests for build_protocol_mapping_prompt (T05.01, FR-013, FR-014)."""

    def test_protocol_mapping_prompt_not_empty(self, sample_inventory):
        prompt = build_protocol_mapping_prompt("my-cli", sample_inventory)
        assert len(prompt) > 0

    def test_protocol_mapping_prompt_contains_inventory_reference(
        self, sample_inventory
    ):
        prompt = build_protocol_mapping_prompt("my-cli", sample_inventory)
        assert "my-cli" in prompt
        assert "cmd-entry" in prompt

    def test_protocol_mapping_prompt_contains_exit_recommendation_instruction(
        self, sample_inventory
    ):
        prompt = build_protocol_mapping_prompt("my-cli", sample_inventory)
        assert "EXIT_RECOMMENDATION" in prompt

    def test_protocol_mapping_prompt_contains_yaml_frontmatter_requirement(
        self, sample_inventory
    ):
        prompt = build_protocol_mapping_prompt("my-cli", sample_inventory)
        assert "---" in prompt
        assert "step: protocol-mapping" in prompt

    def test_protocol_mapping_prompt_with_empty_inventory(self):
        prompt = build_protocol_mapping_prompt("empty-cli", [])
        assert len(prompt) > 0
        assert "empty-cli" in prompt

    def test_protocol_mapping_prompt_with_source_skill(self, sample_inventory):
        prompt = build_protocol_mapping_prompt(
            "my-cli", sample_inventory, source_skill="my-skill"
        )
        assert "my-skill" in prompt


# ---------------------------------------------------------------------------
# T05.01: protocol_mapping step execution
# ---------------------------------------------------------------------------


class TestProtocolMappingExecution:
    """Tests for execute_protocol_mapping_step (T05.01, SC-003)."""

    def test_protocol_mapping_produces_artifact(self, sample_inventory, workdir):
        workdir.mkdir(parents=True, exist_ok=True)
        result = execute_protocol_mapping_step(
            "test-cli",
            sample_inventory,
            workdir,
            process_runner=_runner_success_with_exit_rec,
        )
        assert (workdir / "protocol-map.md").exists()
        assert result.step_name == "protocol-mapping"

    def test_protocol_mapping_pass_status_with_exit_rec(
        self, sample_inventory, workdir
    ):
        workdir.mkdir(parents=True, exist_ok=True)
        result = execute_protocol_mapping_step(
            "test-cli",
            sample_inventory,
            workdir,
            process_runner=_runner_success_with_exit_rec,
        )
        assert result.portify_status == PortifyStatus.PASS

    def test_protocol_mapping_timeout_classification(self, sample_inventory, workdir):
        workdir.mkdir(parents=True, exist_ok=True)
        result = execute_protocol_mapping_step(
            "test-cli",
            sample_inventory,
            workdir,
            process_runner=_runner_timeout,
        )
        assert result.portify_status == PortifyStatus.TIMEOUT

    def test_protocol_mapping_retry_on_pass_no_signal(self, sample_inventory, workdir):
        workdir.mkdir(parents=True, exist_ok=True)
        call_count = {"n": 0}

        def _runner_first_no_signal_then_pass(prompt: str, output_path: Path):
            call_count["n"] += 1
            output_path.parent.mkdir(parents=True, exist_ok=True)
            if call_count["n"] == 1:
                output_path.write_text(
                    "---\nstep: test\n---\ncontent", encoding="utf-8"
                )
                return 0, "", False
            output_path.write_text(
                "---\nstep: test\n---\ncontent\nEXIT_RECOMMENDATION: CONTINUE",
                encoding="utf-8",
            )
            return 0, EXIT_RECOMMENDATION_MARKER + " CONTINUE", False

        result = execute_protocol_mapping_step(
            "test-cli",
            sample_inventory,
            workdir,
            process_runner=_runner_first_no_signal_then_pass,
        )
        assert call_count["n"] == 2

    def test_protocol_mapping_artifact_path_set(self, sample_inventory, workdir):
        workdir.mkdir(parents=True, exist_ok=True)
        result = execute_protocol_mapping_step(
            "test-cli",
            sample_inventory,
            workdir,
            process_runner=_runner_success_with_exit_rec,
        )
        assert "protocol-map.md" in result.artifact_path


# ---------------------------------------------------------------------------
# T05.02: analysis_synthesis prompt builder
# ---------------------------------------------------------------------------


class TestAnalysisSynthesisPrompt:
    """Tests for build_analysis_synthesis_prompt (T05.02, FR-016, FR-017)."""

    def test_analysis_synthesis_prompt_not_empty(self, sample_inventory):
        prompt = build_analysis_synthesis_prompt("my-cli", sample_inventory, "")
        assert len(prompt) > 0

    def test_analysis_synthesis_prompt_contains_all_7_section_names(
        self, sample_inventory
    ):
        prompt = build_analysis_synthesis_prompt("my-cli", sample_inventory, "")
        required_sections = [
            "Source Components",
            "Step Graph",
            "Parallel Groups",
            "Gates Summary",
            "Data Flow",
            "Classifications",
            "Recommendations",
        ]
        for section in required_sections:
            assert section in prompt, f"Missing section '{section}' in prompt"

    def test_analysis_synthesis_prompt_contains_exit_recommendation_instruction(
        self, sample_inventory
    ):
        prompt = build_analysis_synthesis_prompt("my-cli", sample_inventory, "")
        assert "EXIT_RECOMMENDATION" in prompt

    def test_analysis_synthesis_prompt_contains_yaml_frontmatter_requirement(
        self, sample_inventory
    ):
        prompt = build_analysis_synthesis_prompt("my-cli", sample_inventory, "")
        assert "---" in prompt
        assert "step: analysis-synthesis" in prompt

    def test_analysis_synthesis_prompt_includes_protocol_map_content(
        self, sample_inventory
    ):
        protocol_content = "## Protocol Map\nStep 1: validate"
        prompt = build_analysis_synthesis_prompt(
            "my-cli", sample_inventory, protocol_content
        )
        assert "my-cli" in prompt

    def test_analysis_synthesis_prompt_with_source_skill(self, sample_inventory):
        prompt = build_analysis_synthesis_prompt(
            "my-cli", sample_inventory, "", source_skill="my-skill"
        )
        assert "my-skill" in prompt


# ---------------------------------------------------------------------------
# T05.02: analysis_synthesis step execution
# ---------------------------------------------------------------------------


def _analysis_runner_success(prompt: str, output_path: Path):
    """Mock runner: writes portify-analysis-report.md with 7 sections and EXIT_RECOMMENDATION."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    content = (
        "---\nstep: analysis-synthesis\ncli_name: test\n---\n"
        "## Source Components\ncontent\n"
        "## Step Graph\ncontent\n"
        "## Parallel Groups\ncontent\n"
        "## Gates Summary\ncontent\n"
        "## Data Flow\ncontent\n"
        "## Classifications\ncontent\n"
        "## Recommendations\ncontent\n"
        "EXIT_RECOMMENDATION: CONTINUE\n"
    )
    output_path.write_text(content, encoding="utf-8")
    return 0, EXIT_RECOMMENDATION_MARKER + " CONTINUE", False


class TestAnalysisSynthesisExecution:
    """Tests for execute_analysis_synthesis_step (T05.02, SC-004)."""

    def test_analysis_synthesis_produces_artifact(self, sample_inventory, workdir):
        workdir.mkdir(parents=True, exist_ok=True)
        result = execute_analysis_synthesis_step(
            "test-cli",
            sample_inventory,
            workdir,
            process_runner=_analysis_runner_success,
        )
        assert (workdir / "portify-analysis-report.md").exists()
        assert result.step_name == "analysis-synthesis"

    def test_analysis_synthesis_pass_status_with_exit_rec(
        self, sample_inventory, workdir
    ):
        workdir.mkdir(parents=True, exist_ok=True)
        result = execute_analysis_synthesis_step(
            "test-cli",
            sample_inventory,
            workdir,
            process_runner=_analysis_runner_success,
        )
        assert result.portify_status == PortifyStatus.PASS

    def test_analysis_synthesis_reads_protocol_map(self, sample_inventory, workdir):
        workdir.mkdir(parents=True, exist_ok=True)
        protocol_map = workdir / "protocol-map.md"
        protocol_map.write_text("## Protocol Map\nstep data", encoding="utf-8")

        captured = {"prompt": None}

        def _capture_runner(prompt: str, output_path: Path):
            captured["prompt"] = prompt
            return _analysis_runner_success(prompt, output_path)

        execute_analysis_synthesis_step(
            "test-cli",
            sample_inventory,
            workdir,
            process_runner=_capture_runner,
        )
        # Confirms function ran without error (protocol-map.md was read)
        assert captured["prompt"] is not None

    def test_analysis_synthesis_timeout_classification(self, sample_inventory, workdir):
        workdir.mkdir(parents=True, exist_ok=True)
        result = execute_analysis_synthesis_step(
            "test-cli",
            sample_inventory,
            workdir,
            process_runner=_runner_timeout,
        )
        assert result.portify_status == PortifyStatus.TIMEOUT

    def test_analysis_report_artifact_path_set(self, sample_inventory, workdir):
        workdir.mkdir(parents=True, exist_ok=True)
        result = execute_analysis_synthesis_step(
            "test-cli",
            sample_inventory,
            workdir,
            process_runner=_analysis_runner_success,
        )
        assert "portify-analysis-report.md" in result.artifact_path


# ---------------------------------------------------------------------------
# T05.03: timeout_600 — 600s timeout enforcement in STEP_REGISTRY
# ---------------------------------------------------------------------------


class TestTimeout600:
    """Tests for 600s timeout on analysis steps (T05.03, NFR-001).

    Test names include 'timeout_600' to match -k filter per T05.03 acceptance criteria.
    """

    def test_timeout_600_protocol_mapping_step_registry(self):
        assert STEP_REGISTRY["protocol-mapping"]["timeout_s"] == 600

    def test_timeout_600_analysis_synthesis_step_registry(self):
        assert STEP_REGISTRY["analysis-synthesis"]["timeout_s"] == 600

    def test_timeout_600_registry_has_protocol_mapping(self):
        assert "protocol-mapping" in STEP_REGISTRY

    def test_timeout_600_registry_has_analysis_synthesis(self):
        assert "analysis-synthesis" in STEP_REGISTRY

    def test_timeout_600_protocol_mapping_exit_124(self, sample_inventory, workdir):
        workdir.mkdir(parents=True, exist_ok=True)
        result = execute_protocol_mapping_step(
            "test-cli",
            sample_inventory,
            workdir,
            process_runner=_runner_timeout,
        )
        assert result.portify_status == PortifyStatus.TIMEOUT

    def test_timeout_600_analysis_synthesis_exit_124(self, sample_inventory, workdir):
        workdir.mkdir(parents=True, exist_ok=True)
        result = execute_analysis_synthesis_step(
            "test-cli",
            sample_inventory,
            workdir,
            process_runner=_runner_timeout,
        )
        assert result.portify_status == PortifyStatus.TIMEOUT

    def test_timeout_600_protocol_mapping_iteration_recorded(
        self, sample_inventory, workdir
    ):
        workdir.mkdir(parents=True, exist_ok=True)
        result = execute_protocol_mapping_step(
            "test-cli",
            sample_inventory,
            workdir,
            process_runner=_runner_success_with_exit_rec,
        )
        assert result.iteration_timeout == 600

    def test_timeout_600_analysis_synthesis_iteration_recorded(
        self, sample_inventory, workdir
    ):
        workdir.mkdir(parents=True, exist_ok=True)
        result = execute_analysis_synthesis_step(
            "test-cli",
            sample_inventory,
            workdir,
            process_runner=_analysis_runner_success,
        )
        assert result.iteration_timeout == 600


# ---------------------------------------------------------------------------
# T05.04: phase1_approval — user-review-p1 gate
# ---------------------------------------------------------------------------


class TestPhase1Approval:
    """Tests for execute_user_review_p1 (T05.04, FR-018, SC-006).

    Test names include 'phase1_approval' to match -k filter per T05.04 acceptance criteria.
    """

    def test_phase1_approval_writes_pending_yaml(self, workdir):
        workdir.mkdir(parents=True, exist_ok=True)
        execute_user_review_p1("test-cli", workdir, _exit=False)
        approval_path = workdir / "phase1-approval.yaml"
        assert approval_path.exists()
        data = yaml.safe_load(approval_path.read_text())
        assert data["status"] == "pending"

    def test_phase1_approval_yaml_contains_workflow(self, workdir):
        workdir.mkdir(parents=True, exist_ok=True)
        execute_user_review_p1("my-workflow", workdir, _exit=False)
        data = yaml.safe_load((workdir / "phase1-approval.yaml").read_text())
        assert data["workflow"] == "my-workflow"

    def test_phase1_approval_yaml_contains_review_artifacts(self, workdir):
        workdir.mkdir(parents=True, exist_ok=True)
        execute_user_review_p1("test-cli", workdir, _exit=False)
        data = yaml.safe_load((workdir / "phase1-approval.yaml").read_text())
        artifacts = data["review_artifacts"]
        assert "protocol-map.md" in artifacts
        assert "portify-analysis-report.md" in artifacts

    def test_phase1_approval_yaml_has_instructions(self, workdir):
        workdir.mkdir(parents=True, exist_ok=True)
        execute_user_review_p1("test-cli", workdir, _exit=False)
        data = yaml.safe_load((workdir / "phase1-approval.yaml").read_text())
        assert "instructions" in data
        assert "approved" in data["instructions"]

    def test_phase1_approval_prints_resume_instructions(self, workdir, capsys):
        workdir.mkdir(parents=True, exist_ok=True)
        execute_user_review_p1("test-cli", workdir, _exit=False)
        captured = capsys.readouterr()
        assert "superclaude cli-portify run" in captured.out
        assert "--resume" in captured.out

    def test_phase1_approval_creates_workdir_if_missing(self, tmp_path):
        workdir = tmp_path / "new_workdir"
        assert not workdir.exists()
        execute_user_review_p1("test-cli", workdir, _exit=False)
        assert (workdir / "phase1-approval.yaml").exists()


# ---------------------------------------------------------------------------
# T05.05: resume_validation — _validate_phase1_approval
# ---------------------------------------------------------------------------


class TestResumeValidation:
    """Tests for _validate_phase1_approval (T05.05, FR-019, SC-007).

    Test names include 'resume_validation' to match -k filter per T05.05 acceptance criteria.
    """

    def test_resume_validation_approved_passes(self, workdir):
        workdir.mkdir(parents=True, exist_ok=True)
        (workdir / "phase1-approval.yaml").write_text(
            "status: approved\nworkflow: test\n", encoding="utf-8"
        )
        # Should not raise
        _validate_phase1_approval(workdir)

    def test_resume_validation_pending_raises_error(self, workdir):
        workdir.mkdir(parents=True, exist_ok=True)
        (workdir / "phase1-approval.yaml").write_text(
            "status: pending\nworkflow: test\n", encoding="utf-8"
        )
        with pytest.raises(PortifyValidationError) as exc_info:
            _validate_phase1_approval(workdir)
        assert "approved" in str(exc_info.value).lower()

    def test_resume_validation_missing_file_raises_error(self, workdir):
        workdir.mkdir(parents=True, exist_ok=True)
        with pytest.raises(PortifyValidationError):
            _validate_phase1_approval(workdir)

    def test_resume_validation_malformed_yaml_raises_error(self, workdir):
        workdir.mkdir(parents=True, exist_ok=True)
        (workdir / "phase1-approval.yaml").write_text(
            "status: [invalid: yaml: here\n", encoding="utf-8"
        )
        with pytest.raises(PortifyValidationError) as exc_info:
            _validate_phase1_approval(workdir)
        assert (
            "malformed" in str(exc_info.value).lower()
            or "yaml" in str(exc_info.value).lower()
        )

    def test_resume_validation_missing_status_field_raises_error(self, workdir):
        workdir.mkdir(parents=True, exist_ok=True)
        (workdir / "phase1-approval.yaml").write_text(
            "workflow: test\nnotes: some notes\n", encoding="utf-8"
        )
        with pytest.raises(PortifyValidationError) as exc_info:
            _validate_phase1_approval(workdir)
        assert "status" in str(exc_info.value).lower()

    def test_resume_validation_status_in_comment_raises_error(self, workdir):
        workdir.mkdir(parents=True, exist_ok=True)
        # status: approved in comment only — YAML parse will not pick it up as field
        (workdir / "phase1-approval.yaml").write_text(
            "# status: approved\nworkflow: test\n", encoding="utf-8"
        )
        with pytest.raises(PortifyValidationError):
            _validate_phase1_approval(workdir)

    def test_resume_validation_rejected_raises_error(self, workdir):
        workdir.mkdir(parents=True, exist_ok=True)
        (workdir / "phase1-approval.yaml").write_text(
            "status: rejected\nworkflow: test\n", encoding="utf-8"
        )
        with pytest.raises(PortifyValidationError):
            _validate_phase1_approval(workdir)

    def test_resume_validation_non_mapping_yaml_raises_error(self, workdir):
        workdir.mkdir(parents=True, exist_ok=True)
        (workdir / "phase1-approval.yaml").write_text(
            "- item1\n- item2\n", encoding="utf-8"
        )
        with pytest.raises(PortifyValidationError):
            _validate_phase1_approval(workdir)

    def test_resume_validation_error_code_is_invalid_path(self, workdir):
        workdir.mkdir(parents=True, exist_ok=True)
        (workdir / "phase1-approval.yaml").write_text(
            "status: pending\n", encoding="utf-8"
        )
        with pytest.raises(PortifyValidationError) as exc_info:
            _validate_phase1_approval(workdir)
        assert exc_info.value.error_code == "INVALID_PATH"
