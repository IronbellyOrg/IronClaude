"""Unit tests for superclaude.cli.prd.models.

Section 8.1 test plan: 3 tests.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from superclaude.cli.prd.models import (
    ExistingWorkState,
    PrdConfig,
    PrdMonitorState,
    PrdPipelineResult,
    PrdStepResult,
    PrdStepStatus,
)


class TestPrdConfigDerivedPaths:
    """Verify research_dir, synthesis_dir, qa_dir resolve correctly from base paths."""

    def test_prd_config_derived_paths(self) -> None:
        config = PrdConfig(task_dir=Path("/tmp/my-task"))

        assert config.research_dir == Path("/tmp/my-task/research")
        assert config.synthesis_dir == Path("/tmp/my-task/synthesis")
        assert config.qa_dir == Path("/tmp/my-task/qa")

    def test_prd_config_default_task_dir(self) -> None:
        config = PrdConfig()
        assert config.research_dir == Path("research")
        assert config.synthesis_dir == Path("synthesis")
        assert config.qa_dir == Path("qa")


class TestPrdStepStatusProperties:
    """Verify is_terminal, is_success, is_failure, needs_fix_cycle for each status value."""

    def test_prd_step_status_properties(self) -> None:
        # Non-terminal, non-success, non-failure states
        assert not PrdStepStatus.PENDING.is_terminal
        assert not PrdStepStatus.PENDING.is_success
        assert not PrdStepStatus.PENDING.is_failure
        assert not PrdStepStatus.PENDING.needs_fix_cycle

        assert not PrdStepStatus.RUNNING.is_terminal
        assert not PrdStepStatus.RUNNING.is_success
        assert not PrdStepStatus.RUNNING.is_failure
        assert not PrdStepStatus.RUNNING.needs_fix_cycle

        # Success states (all terminal)
        for status in (PrdStepStatus.PASS, PrdStepStatus.PASS_NO_SIGNAL, PrdStepStatus.PASS_NO_REPORT):
            assert status.is_terminal, f"{status.name} should be terminal"
            assert status.is_success, f"{status.name} should be success"
            assert not status.is_failure, f"{status.name} should not be failure"
            assert not status.needs_fix_cycle, f"{status.name} should not need fix cycle"

        # Failure states (all terminal)
        for status in (
            PrdStepStatus.HALT,
            PrdStepStatus.TIMEOUT,
            PrdStepStatus.ERROR,
            PrdStepStatus.QA_FAIL_EXHAUSTED,
            PrdStepStatus.VALIDATION_FAIL,
        ):
            assert status.is_terminal, f"{status.name} should be terminal"
            assert not status.is_success, f"{status.name} should not be success"
            assert status.is_failure, f"{status.name} should be failure"
            assert not status.needs_fix_cycle, f"{status.name} should not need fix cycle"

        # SKIPPED: terminal but neither success nor failure
        assert PrdStepStatus.SKIPPED.is_terminal
        assert not PrdStepStatus.SKIPPED.is_success
        assert not PrdStepStatus.SKIPPED.is_failure
        assert not PrdStepStatus.SKIPPED.needs_fix_cycle

        # Fix-cycle states (non-terminal)
        for status in (PrdStepStatus.QA_FAIL, PrdStepStatus.INCOMPLETE):
            assert not status.is_terminal, f"{status.name} should not be terminal"
            assert not status.is_success, f"{status.name} should not be success"
            assert not status.is_failure, f"{status.name} should not be failure"
            assert status.needs_fix_cycle, f"{status.name} should need fix cycle"


class TestPrdPipelineResultResumeCommand:
    """Verify correct CLI string generation on halt."""

    def test_prd_pipeline_result_resume_command(self) -> None:
        config = PrdConfig(
            product_name="MyApp",
            model="opus",
            tier="heavyweight",
        )
        result = PrdPipelineResult(
            config=config,
            halt_step="research-notes",
            halt_reason="Gate failure",
        )

        cmd = result.resume_command()
        assert cmd == "superclaude prd resume research-notes --product MyApp --model opus --tier heavyweight"

    def test_resume_command_no_halt(self) -> None:
        result = PrdPipelineResult(config=PrdConfig())
        assert result.resume_command() == ""

    def test_resume_command_standard_tier_omitted(self) -> None:
        config = PrdConfig(product_name="Test", tier="standard")
        result = PrdPipelineResult(config=config, halt_step="step-7")
        cmd = result.resume_command()
        assert "--tier" not in cmd
        assert "--product Test" in cmd
