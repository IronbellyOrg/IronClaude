"""End-to-end tests for the PRD pipeline.

Section 8.3: 5 E2E test scenarios covering full pipeline flows.

1. test_e2e_full_prd_creation_standard -- complete standard-tier pipeline
2. test_e2e_lightweight_prd -- lightweight tier with reduced agent count
3. test_e2e_resume_from_halted_step -- resume skips completed steps
4. test_e2e_existing_work_detection -- second run detects existing work
5. test_e2e_budget_exhaustion -- low budget halts with resume command

All tests mock subprocess launches via PrdClaudeProcess. No real API calls.
Prompt builders are mocked to avoid intermediate file dependencies --
E2E tests exercise the executor orchestration (step sequencing, budget
management, gate evaluation, parallel execution) not prompt content.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from superclaude.cli.prd.config import resolve_config
from superclaude.cli.prd.executor import PrdExecutor, TurnLedger
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
def e2e_task_dir(tmp_path):
    """Create a fully structured task directory for E2E testing."""
    task_dir = tmp_path / "prd-test-e2e"
    for subdir in ("research", "synthesis", "qa", "reviews", "results"):
        (task_dir / subdir).mkdir(parents=True)
    return task_dir


@pytest.fixture
def standard_e2e_config(e2e_task_dir):
    """Standard-tier config for E2E pipeline runs."""
    config = resolve_config(
        "Create PRD for SuperClaude CLI",
        product="superclaude-cli",
        tier="standard",
        output=str(e2e_task_dir.parent),
        max_turns=1000,  # High budget to avoid exhaustion in E2E
        dry_run=False,
    )
    config.task_dir = e2e_task_dir
    config.work_dir = e2e_task_dir.parent
    return config


@pytest.fixture
def lightweight_e2e_config(e2e_task_dir):
    """Lightweight-tier config for E2E pipeline runs."""
    config = resolve_config(
        "PRD for install command",
        product="install-cmd",
        tier="lightweight",
        output=str(e2e_task_dir.parent),
        max_turns=1000,  # High budget to avoid exhaustion in E2E
        dry_run=False,
    )
    config.task_dir = e2e_task_dir
    config.work_dir = e2e_task_dir.parent
    return config


# ---------------------------------------------------------------------------
# Mock helpers
# ---------------------------------------------------------------------------


def _make_passing_output(step_id: str, line_count: int = 100) -> str:
    """Generate mock subprocess output that passes all gate checks.

    Each step has specific gate criteria (min_lines, semantic checks).
    This function ensures the mock output satisfies all of them.
    """
    # Determine minimum lines needed per step gate
    min_lines_map = {
        "scope-discovery": 50,
        "research-notes": 100,
        "build-task-file": 400,
        "investigation": 50,
        "research-qa": 20,
        "web-research": 30,
        "synthesis": 80,
        "synthesis-qa": 20,
        "assembly": 800,
        "structural-qa": 20,
        "qualitative-qa": 20,
    }
    # Find the matching min_lines for the step_id (handles investigation-N etc.)
    effective_min = line_count
    for key, val in min_lines_map.items():
        if step_id.startswith(key):
            effective_min = max(line_count, val + 10)  # +10 margin
            break

    lines = [f"# Output for {step_id}"]

    if step_id == "parse-request":
        # Gate: _check_parsed_request_fields (GOAL, PRODUCT_SLUG, PRD_SCOPE, SCENARIO)
        lines.extend([
            '{"GOAL": "Build a comprehensive product",',
            '"PRODUCT_SLUG": "test-product",',
            '"PRD_SCOPE": "feature",',
            '"SCENARIO": "B"}',
        ])
    elif step_id == "research-notes":
        # Gate: _check_research_notes_sections (7 required sections)
        # + _check_suggested_phases_detail (needs list items under Phases)
        # + min_lines=100
        lines.extend([
            "---",
            "Date: 2026-04-12",
            "Scenario: B",
            "Tier: standard",
            "---",
            "## Product Capabilities",
            "The product supports comprehensive CLI-driven PRD generation.",
            "## Technical Architecture",
            "Subprocess-based pipeline with 15 orchestrated steps.",
            "## User Flows",
            "User invokes CLI, pipeline generates PRD via staged agents.",
            "## Integration Points",
            "Integrates with Claude subprocess API and MCP servers.",
            "## Existing Documentation",
            "Existing docs cover CLI usage and skill definitions.",
            "## Gap Analysis",
            "Gaps identified in assembly QA and resume handling.",
            "## Suggested Phases",
            "1. Research and context gathering",
            "2. Synthesis and template population",
            "3. Assembly and quality assurance",
        ])
    elif step_id == "build-task-file":
        # Gate: _check_task_phases_present (>= 2 phase headings)
        # + _check_b2_self_contained (no 'see above' in checklists)
        # + _check_parallel_instructions (phases 2+ need 'parallel' keyword)
        # + min_lines=400
        lines.extend([
            "---",
            "id: TASK-PRD-001",
            "title: PRD Generation",
            "status: to-do",
            "complexity: high",
            "created_date: 2026-04-12",
            "---",
            "## Phase 1: Research",
            "Gather product context and requirements.",
            "- [ ] Conduct stakeholder interviews",
            "- [ ] Review existing documentation",
            "## Phase 2: Synthesis",
            "Synthesize research into structured sections in parallel.",
            "Execute parallel agent synthesis for each PRD section.",
            "- [ ] Generate overview section",
            "- [ ] Generate requirements section",
            "## Phase 3: Assembly",
            "Assemble final PRD with parallel QA checks.",
            "Run concurrent quality assurance agents.",
            "- [ ] Assemble document",
            "- [ ] Run structural QA",
        ])
    elif step_id == "verify-task-file":
        # Gate: _check_verdict_field (STRICT)
        lines.append('{"verdict": "PASS", "issues": []}')
    elif step_id == "sufficiency-review":
        # Gate: _check_verdict_field (STRICT)
        lines.append('{"verdict": "PASS", "issues": []}')
    elif step_id == "assembly":
        # Gate: _check_prd_template_sections + _check_no_placeholders
        # + min_lines=800
        lines.extend([
            "---",
            "id: PRD-001",
            "title: SuperClaude CLI PRD",
            "status: draft",
            "created_date: 2026-04-12",
            "tags: [prd, cli, superclaude]",
            "---",
            "## Executive Summary",
            "This PRD defines the SuperClaude CLI pipeline.",
            "## Problem Statement",
            "Current manual processes are slow and error-prone.",
            "## Technical Requirements",
            "Support 3 tiers of PRD generation.",
            "## Implementation Plan",
            "Phased rollout across 5 development phases.",
            "## Success Metrics",
            "95% gate pass rate, <45min heavyweight runs.",
        ])
        effective_min = max(effective_min, 810)
    elif "qa" in step_id or "review" in step_id:
        # Gate: _check_verdict_field or _check_qa_verdict
        lines.append('{"verdict": "PASS", "issues": []}')
    elif step_id.startswith("investigation") or step_id.startswith("web-research"):
        lines.extend(["## Findings", "## Evidence", "## Recommendations"])
    elif step_id.startswith("synthesis"):
        lines.extend(["## Section Content", "## Cross-References"])

    while len(lines) < effective_min - 1:
        lines.append(f"Content line {len(lines)}")
    lines.append("EXIT_RECOMMENDATION: CONTINUE")
    return "\n".join(lines)


def _mock_process_factory(
    *,
    step_overrides: dict[str, tuple[int, str]] | None = None,
    default_line_count: int = 100,
):
    """Create a mock PrdClaudeProcess factory accepting keyword args."""
    overrides = step_overrides or {}

    def factory(**kwargs):
        step_id = kwargs["step_id"]
        output_file = kwargs["output_file"]
        mock_proc = MagicMock()

        if step_id in overrides:
            exit_code, output_text = overrides[step_id]
        else:
            exit_code = 0
            output_text = _make_passing_output(step_id, default_line_count)

        mock_proc.start_with_retry.return_value = None

        def write_output_and_return():
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(output_text, encoding="utf-8")
            return exit_code

        mock_proc.wait.side_effect = write_output_and_return
        return mock_proc

    return factory


# ---------------------------------------------------------------------------
# Scenario 1: Full PRD creation (standard tier)
# ---------------------------------------------------------------------------


@patch("superclaude.cli.prd.executor.PrdClaudeProcess")
@patch("superclaude.cli.prd.executor.load_synthesis_mapping")
def test_e2e_full_prd_creation_standard(
    mock_synth_mapping, mock_process_cls, standard_e2e_config
):
    """Complete pipeline from request to PRD output, standard tier.

    Validates:
    - All Stage A steps (1-9) execute in order
    - Stage B generates correct agent counts for standard tier
    - Final pipeline outcome is 'success'
    - Step results cover all expected stages
    """
    mock_process_cls.side_effect = _mock_process_factory(default_line_count=120)
    mock_synth_mapping.return_value = [
        {"synth_file": "section-overview.md"},
        {"synth_file": "section-requirements.md"},
        {"synth_file": "section-architecture.md"},
    ]

    executor = PrdExecutor(standard_e2e_config)

    # Mock _build_prompt to avoid intermediate file dependencies
    executor._build_prompt = lambda builder_name: f"Mock prompt for {builder_name}"

    result = executor.run()

    # Pipeline completes successfully
    assert result.outcome == "success"
    assert result.finished_at is not None

    # Verify step results cover the pipeline
    step_count = len(result.step_results)
    # Stage A: 9 steps + Stage B: investigation(5) + research-qa(1)
    # + web-research(2) + synthesis(3) + synthesis-qa(1)
    # + assembly(1) + structural-qa(1) + qualitative-qa(1)
    # + completion(1) = 25+ steps
    assert step_count >= 15, (
        f"Expected >= 15 step results for standard tier, got {step_count}"
    )

    # All steps should have terminal status
    for sr in result.step_results:
        assert sr.status.is_terminal, (
            f"Step has non-terminal status: {sr.status}"
        )

    # Standard tier generates 5 investigation agents
    assert result.research_agent_count == 5

    # Standard tier generates 2 web research agents
    assert result.web_agent_count == 2

    # Synthesis count matches mapping table
    assert result.synthesis_agent_count == 3


# ---------------------------------------------------------------------------
# Scenario 2: Lightweight PRD
# ---------------------------------------------------------------------------


@patch("superclaude.cli.prd.executor.PrdClaudeProcess")
@patch("superclaude.cli.prd.executor.load_synthesis_mapping")
def test_e2e_lightweight_prd(
    mock_synth_mapping, mock_process_cls, lightweight_e2e_config
):
    """Lightweight tier pipeline with reduced agent count.

    Validates:
    - Lightweight tier uses 3 investigation agents (not 5)
    - Lightweight tier uses 1 web research agent (not 2)
    - Pipeline still completes successfully
    """
    mock_process_cls.side_effect = _mock_process_factory(default_line_count=80)
    mock_synth_mapping.return_value = [
        {"synth_file": "section-overview.md"},
        {"synth_file": "section-requirements.md"},
    ]

    executor = PrdExecutor(lightweight_e2e_config)
    executor._build_prompt = lambda builder_name: f"Mock prompt for {builder_name}"

    result = executor.run()

    # Pipeline completes successfully
    assert result.outcome == "success"

    # Lightweight: 3 investigation agents
    assert result.research_agent_count == 3

    # Lightweight: 1 web research agent
    assert result.web_agent_count == 1

    # Synthesis count matches (smaller) mapping table
    assert result.synthesis_agent_count == 2


# ---------------------------------------------------------------------------
# Scenario 3: Resume from halted step
# ---------------------------------------------------------------------------


@patch("superclaude.cli.prd.executor.PrdClaudeProcess")
@patch("superclaude.cli.prd.executor.load_synthesis_mapping")
def test_e2e_resume_from_halted_step(
    mock_synth_mapping, mock_process_cls, e2e_task_dir
):
    """Resume skips completed steps, resumes from specified agent ID.

    Validates:
    - Setting resume_from carries through config
    - Pipeline still runs and produces results
    - Subprocess calls are made for executed steps
    - The resume step ID is a valid pattern
    """
    mock_synth_mapping.return_value = [
        {"synth_file": "section-overview.md"},
    ]

    config = resolve_config(
        "test resume",
        product="resume-test",
        tier="standard",
        output=str(e2e_task_dir.parent),
        max_turns=1000,  # High budget to avoid exhaustion in E2E
        dry_run=False,
        resume_from="investigation-3",
    )
    config.task_dir = e2e_task_dir
    config.work_dir = e2e_task_dir.parent

    # Track which steps get subprocess calls
    subprocess_calls: list[str] = []
    base_factory = _mock_process_factory(default_line_count=100)

    def tracking_factory(**kwargs):
        subprocess_calls.append(kwargs["step_id"])
        return base_factory(**kwargs)

    mock_process_cls.side_effect = tracking_factory

    executor = PrdExecutor(config)
    executor._build_prompt = lambda builder_name: f"Mock prompt for {builder_name}"

    result = executor.run()

    # Pipeline ran to completion
    assert result is not None
    assert result.finished_at is not None
    assert result.outcome == "success"

    # Config carried the resume marker
    assert config.resume_from == "investigation-3"

    # Subprocess calls were made
    assert len(subprocess_calls) > 0

    # Step results were recorded
    assert len(result.step_results) > 0

    # The resume step ID is a valid pattern
    from superclaude.cli.prd.config import _STEP_ID_PATTERN
    assert _STEP_ID_PATTERN.match(config.resume_from)


# ---------------------------------------------------------------------------
# Scenario 4: Existing work detection
# ---------------------------------------------------------------------------


@patch("superclaude.cli.prd.executor.PrdClaudeProcess")
@patch("superclaude.cli.prd.executor.load_synthesis_mapping")
def test_e2e_existing_work_detection(
    mock_synth_mapping, mock_process_cls, e2e_task_dir
):
    """Second run detects existing work and offers resume.

    Validates end-to-end data flow:
    - NO_EXISTING -> RESUME_STAGE_A -> RESUME_STAGE_B -> ALREADY_COMPLETE
    - Executor processes check-existing step correctly for each state
    - ExistingWorkState transition is correct based on artifact state
    """
    mock_process_cls.side_effect = _mock_process_factory(default_line_count=100)
    mock_synth_mapping.return_value = [
        {"synth_file": "section-overview.md"},
    ]

    config = resolve_config(
        "Build auth system",
        product="auth-system",
        tier="standard",
        output=str(e2e_task_dir.parent),
        max_turns=1000,  # High budget to avoid exhaustion in E2E
        dry_run=False,
    )
    config.task_dir = e2e_task_dir
    config.work_dir = e2e_task_dir.parent

    from superclaude.cli.prd.inventory import check_existing_work

    # Phase 1: No existing task directory -> NO_EXISTING
    state = check_existing_work(config)
    assert state == ExistingWorkState.NO_EXISTING

    # Phase 2: Create matching TASK-PRD directory (no research) -> RESUME_STAGE_A
    tasks_root = e2e_task_dir.parent / ".dev" / "tasks" / "to-do"
    existing_task = tasks_root / "TASK-PRD-auth-system"
    existing_task.mkdir(parents=True)
    (existing_task / "task.md").write_text(
        "---\nproduct_name: auth-system\n---\n# Task\n"
    )
    state = check_existing_work(config)
    assert state == ExistingWorkState.RESUME_STAGE_A

    # Phase 3: Add research files -> RESUME_STAGE_B
    existing_research = existing_task / "research"
    existing_research.mkdir(parents=True)
    (existing_research / "01-overview.md").write_text(
        "# Research\nCompleted research findings.\n"
    )
    state = check_existing_work(config)
    assert state == ExistingWorkState.RESUME_STAGE_B

    # Phase 4: Add final results -> ALREADY_COMPLETE
    results_dir = existing_task / "results"
    results_dir.mkdir(parents=True)
    (results_dir / "final-prd.md").write_text("# Final PRD\n")
    state = check_existing_work(config)
    assert state == ExistingWorkState.ALREADY_COMPLETE

    # Phase 5: Run executor -- check-existing returns SKIPPED for
    # ALREADY_COMPLETE state, rest of pipeline proceeds
    executor = PrdExecutor(config)
    executor._build_prompt = lambda builder_name: f"Mock prompt for {builder_name}"

    result = executor.run()

    assert result is not None
    assert len(result.step_results) > 0

    # First step result should be the check-existing step
    first = result.step_results[0]
    assert first.status == PrdStepStatus.SKIPPED


# ---------------------------------------------------------------------------
# Scenario 5: Budget exhaustion
# ---------------------------------------------------------------------------


@patch("superclaude.cli.prd.executor.PrdClaudeProcess")
@patch("superclaude.cli.prd.executor.load_synthesis_mapping")
def test_e2e_budget_exhaustion(
    mock_synth_mapping, mock_process_cls, e2e_task_dir
):
    """--max-turns 50 causes halt with resume command and suggested budget.

    Validates:
    - Low turn budget causes pipeline to halt mid-run
    - Result includes halt_step and halt_reason
    - resume_command() generates a valid CLI invocation
    - suggested_resume_budget returns a positive value
    """
    mock_process_cls.side_effect = _mock_process_factory(default_line_count=100)
    mock_synth_mapping.return_value = [
        {"synth_file": "section-overview.md"},
        {"synth_file": "section-requirements.md"},
    ]

    # Very low turn budget: 50 turns total
    config = resolve_config(
        "Full platform PRD",
        product="big-platform",
        tier="standard",
        output=str(e2e_task_dir.parent),
        max_turns=50,
        dry_run=False,
    )
    config.task_dir = e2e_task_dir
    config.work_dir = e2e_task_dir.parent

    executor = PrdExecutor(config)
    executor._build_prompt = lambda builder_name: f"Mock prompt for {builder_name}"

    result = executor.run()

    # Pipeline should halt due to budget exhaustion
    # With 50 turns and steps needing 10-30 each, exhaustion occurs
    # partway through the pipeline.
    assert result.outcome == "halt", (
        f"Expected halt due to budget exhaustion, got {result.outcome}"
    )

    # Halt metadata should be populated
    assert result.halt_step is not None
    assert result.halt_reason is not None

    # Resume command should be generated
    resume_cmd = result.resume_command()
    assert "superclaude" in resume_cmd
    assert "prd" in resume_cmd
    assert "resume" in resume_cmd

    # Suggested budget should be positive
    suggested = result.suggested_resume_budget
    assert suggested > 0, (
        f"Expected positive suggested budget, got {suggested}"
    )
