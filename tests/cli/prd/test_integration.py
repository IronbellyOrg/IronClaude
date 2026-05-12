"""Integration tests for the PRD pipeline.

Section 8.2: 9 integration tests covering end-to-end flows.

1. test_prd_pipeline_dry_run -- config construction and validation
2. test_prd_pipeline_check_existing_integration -- existing work detection
3. test_prd_pipeline_budget_exhaustion -- TurnLedger budget guard
4. test_prd_pipeline_signal_shutdown -- graceful shutdown with resume state
5. test_prd_pipeline_gate_enforcement -- STRICT gate failures halt pipeline
6. test_prd_pipeline_fix_cycle_flow -- QA FAIL -> gap-fill -> re-QA
7. test_prd_pipeline_parallel_execution -- ThreadPoolExecutor concurrent agents
8. test_build_investigation_steps_standard_tier -- dynamic step generation standard
9. test_build_investigation_steps_heavyweight_tier -- dynamic step generation heavyweight

All tests use mocked ClaudeProcess (no real subprocess launches).
"""

from __future__ import annotations

import os
import signal
import time
import threading
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from superclaude.cli.prd.config import resolve_config
from superclaude.cli.prd.diagnostics import (
    DiagnosticCollector,
    FailureClassifier,
    PrdFailureCategory,
    ReportGenerator,
)
from superclaude.cli.prd.executor import (
    PrdExecutor,
    TurnLedger,
    _detect_sentinel,
)
from superclaude.cli.prd.inventory import check_existing_work
from superclaude.cli.prd.models import (
    ExistingWorkState,
    PrdConfig,
    PrdPipelineResult,
    PrdStepResult,
    PrdStepStatus,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def tmp_task_dir(tmp_path):
    """Create a temporary task directory structure."""
    task_dir = tmp_path / "prd-test"
    for subdir in ("research", "synthesis", "qa", "reviews", "results"):
        (task_dir / subdir).mkdir(parents=True)
    return task_dir


@pytest.fixture
def standard_config(tmp_task_dir):
    """Create a standard-tier PrdConfig for integration testing."""
    config = resolve_config(
        "test product",
        product="test-product",
        tier="standard",
        output=str(tmp_task_dir.parent),
        dry_run=False,
    )
    # Override task_dir to use our temp dir
    config.task_dir = tmp_task_dir
    return config


@pytest.fixture
def heavyweight_config(tmp_task_dir):
    """Create a heavyweight-tier PrdConfig for integration testing."""
    config = resolve_config(
        "test product heavyweight",
        product="test-heavyweight",
        tier="heavyweight",
        output=str(tmp_task_dir.parent),
        dry_run=False,
    )
    config.task_dir = tmp_task_dir
    return config


# ---------------------------------------------------------------------------
# Test 1: Dry-run pipeline (config validation only)
# ---------------------------------------------------------------------------


def test_prd_pipeline_dry_run():
    """Dry-run mode should validate config without executing subprocesses."""
    config = resolve_config(
        "test dry run product",
        product="dry-run-test",
        tier="standard",
        dry_run=True,
    )
    executor = PrdExecutor(config)
    result = executor.run()

    assert result.outcome == "dry_run"
    assert result.finished_at is not None
    assert len(result.step_results) == 0  # No steps executed


# ---------------------------------------------------------------------------
# Test 2: Existing work detection integration
# ---------------------------------------------------------------------------


def test_prd_pipeline_check_existing_integration(tmp_path):
    """check_existing_work should detect pre-existing PRD work."""
    config = resolve_config(
        "test existing",
        product="test-product",
        tier="standard",
        dry_run=True,
    )
    config.work_dir = tmp_path

    # No task directory -- should return NO_EXISTING
    state = check_existing_work(config)
    assert state == ExistingWorkState.NO_EXISTING

    # Create task directory with matching product slug
    task_root = tmp_path / ".dev" / "tasks" / "to-do" / "TASK-PRD-test-product"
    task_root.mkdir(parents=True)
    (task_root / "task.md").write_text("# Test\nSome content\n")
    state = check_existing_work(config)
    assert state == ExistingWorkState.RESUME_STAGE_A

    # Add research files
    research_dir = task_root / "research"
    research_dir.mkdir(parents=True)
    (research_dir / "01-overview.md").write_text(
        "# Research\nSome completed research.\n"
    )
    state = check_existing_work(config)
    assert state == ExistingWorkState.RESUME_STAGE_B

    # Add final results
    results_dir = task_root / "results"
    results_dir.mkdir(parents=True)
    (results_dir / "final-prd.md").write_text("# Final PRD\n")
    state = check_existing_work(config)
    assert state == ExistingWorkState.ALREADY_COMPLETE


# ---------------------------------------------------------------------------
# Test 3: Budget exhaustion halts pipeline
# ---------------------------------------------------------------------------


def test_prd_pipeline_budget_exhaustion(standard_config):
    """Pipeline should halt when TurnLedger reports insufficient budget."""
    # Create executor with very low budget
    standard_config.max_turns = 5  # Extremely low budget
    executor = PrdExecutor(standard_config)
    executor._ledger = TurnLedger(total_budget=5)

    # Allocate most of the budget
    executor._ledger.allocate(4)

    # The subprocess step should detect insufficient budget
    result = executor._run_subprocess_step(
        "build-task-file", "Build Task File", "build_task_file_prompt"
    )

    # Should fail with QA_FAIL_EXHAUSTED since 30 turns > 1 remaining
    assert result.status == PrdStepStatus.QA_FAIL_EXHAUSTED


# ---------------------------------------------------------------------------
# Test 4: Signal-aware shutdown
# ---------------------------------------------------------------------------


def test_prd_pipeline_signal_shutdown(standard_config):
    """SIGINT should trigger graceful shutdown with resume state."""
    executor = PrdExecutor(standard_config)

    # Simulate shutdown request
    executor._signal_handler.shutdown_requested = True

    result = PrdPipelineResult(config=standard_config)

    # Add a completed step result
    executor._step_results = [
        PrdStepResult(status=PrdStepStatus.PASS)
    ]

    executor._handle_shutdown(result)

    assert result.outcome == "interrupted"
    assert result.finished_at is not None


# ---------------------------------------------------------------------------
# Test 5: STRICT gate enforcement halts pipeline
# ---------------------------------------------------------------------------


def test_prd_pipeline_gate_enforcement(standard_config):
    """STRICT gate failures should halt the pipeline."""
    executor = PrdExecutor(standard_config)

    # Mock a gate evaluation that fails on a STRICT step
    from superclaude.cli.prd.gates import GATE_CRITERIA

    gate = GATE_CRITERIA["parse-request"]
    assert gate.enforcement_tier == "STRICT"

    # Test gate evaluation with content missing required fields
    passed = executor._evaluate_gate(
        "parse-request",
        gate,
        "This content has no GOAL or PRODUCT_SLUG or PRD_SCOPE or SCENARIO",
    )
    assert passed is False

    # Test gate evaluation with valid content
    valid_content = '''
    "GOAL": "Build a product"
    "PRODUCT_SLUG": "test-product"
    "PRD_SCOPE": "feature"
    "SCENARIO": "B"
    '''
    passed = executor._evaluate_gate("parse-request", gate, valid_content)
    assert passed is True


# ---------------------------------------------------------------------------
# Test 6: Fix cycle flow (QA FAIL -> gap-fill -> re-QA -> PASS)
# ---------------------------------------------------------------------------


def test_prd_pipeline_fix_cycle_flow(standard_config):
    """QA fix cycle should retry on QA_FAIL and halt on exhaustion."""
    executor = PrdExecutor(standard_config)

    # Track QA invocations
    call_count = [0]
    original_execute = executor._execute_step

    def mock_execute_step(step_id, step_name, builder_name):
        call_count[0] += 1

        # First QA call: FAIL, second: PASS
        if "qa" in step_id.lower() and "fix" not in step_id:
            if call_count[0] <= 2:  # First QA + first fix
                return PrdStepResult(
                    status=PrdStepStatus.QA_FAIL,
                    qa_verdict="FAIL",
                )
            else:
                return PrdStepResult(
                    status=PrdStepStatus.PASS,
                    qa_verdict="PASS",
                )
        return PrdStepResult(status=PrdStepStatus.PASS)

    executor._execute_step = mock_execute_step
    result = PrdPipelineResult(config=standard_config)

    executor._execute_qa_fix_cycle(
        result,
        qa_step_id="research-qa",
        qa_builder="build_qa_research_gate_prompt",
        fix_builder="build_gap_filling_prompt",
        max_cycles=3,
    )

    # Should have recorded fix cycles
    assert len(executor._diagnostics._fix_cycle_history) > 0
    # Should NOT have halted (eventually passed)
    assert result.outcome != "halt"


# ---------------------------------------------------------------------------
# Test 7: Parallel execution via ThreadPoolExecutor
# ---------------------------------------------------------------------------


def test_prd_pipeline_parallel_execution(standard_config):
    """ThreadPoolExecutor should run N agents concurrently."""
    executor = PrdExecutor(standard_config)

    # Track concurrent execution
    active_count = [0]
    max_concurrent = [0]
    lock = threading.Lock()

    original_execute = executor._execute_step

    def mock_execute_step(step_id, step_name, builder_name):
        with lock:
            active_count[0] += 1
            if active_count[0] > max_concurrent[0]:
                max_concurrent[0] = active_count[0]

        time.sleep(0.05)  # Simulate some work

        with lock:
            active_count[0] -= 1

        return PrdStepResult(status=PrdStepStatus.PASS)

    executor._execute_step = mock_execute_step
    result = PrdPipelineResult(config=standard_config)

    # Create 5 parallel steps
    steps = [
        (f"investigation-{i}", f"Agent {i}", "build_investigation_prompt")
        for i in range(5)
    ]

    executor._execute_parallel_steps(steps, result, "investigation")

    # Verify some degree of concurrency occurred
    assert max_concurrent[0] >= 2, (
        f"Expected concurrent execution, max concurrent was {max_concurrent[0]}"
    )
    # Verify all steps completed
    assert len(result.step_results) == 5


# ---------------------------------------------------------------------------
# Test 8: Dynamic step generation -- standard tier (F-012)
# ---------------------------------------------------------------------------


def test_build_investigation_steps_standard_tier(standard_config):
    """Standard tier should generate 5 investigation agents."""
    executor = PrdExecutor(standard_config)
    steps = executor._build_investigation_steps()

    assert len(steps) == 5  # Standard tier: 4-6 agents, we use 5
    for i, (step_id, step_name, builder) in enumerate(steps):
        assert step_id == f"investigation-{i + 1}"
        assert "Investigation" in step_name
        assert builder == "build_investigation_prompt"


# ---------------------------------------------------------------------------
# Test 9: Dynamic step generation -- heavyweight tier (F-012)
# ---------------------------------------------------------------------------


def test_build_investigation_steps_heavyweight_tier(heavyweight_config):
    """Heavyweight tier should generate 8 investigation agents."""
    executor = PrdExecutor(heavyweight_config)
    steps = executor._build_investigation_steps()

    assert len(steps) == 8  # Heavyweight tier: 6-10 agents, we use 8
    for i, (step_id, step_name, builder) in enumerate(steps):
        assert step_id == f"investigation-{i + 1}"
        assert "Investigation" in step_name
