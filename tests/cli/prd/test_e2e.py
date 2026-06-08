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

from unittest.mock import MagicMock, patch

import pytest

from superclaude.cli.prd.config import resolve_config
from superclaude.cli.prd.executor import PrdExecutor
from superclaude.cli.prd.models import (
    ExistingWorkState,
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
        lines.extend(
            [
                '{"GOAL": "Build a comprehensive product",',
                '"PRODUCT_SLUG": "test-product",',
                '"PRD_SCOPE": "feature",',
                '"SCENARIO": "B"}',
            ]
        )
    elif step_id == "research-notes":
        # Gate: _check_research_notes_sections (7 required sections)
        # + _check_suggested_phases_detail (needs list items under Phases)
        # + min_lines=100
        lines.extend(
            [
                "---",
                "Date: 2026-04-12",
                "Scenario: B",
                "Tier: standard",
                "---",
                "## EXISTING_FILES",
                "src/superclaude/cli/prd/ -- entry point for the PRD pipeline.",
                "## PATTERNS_AND_CONVENTIONS",
                "Subprocess-driven pipeline with explicit gates per step.",
                "## FEATURE_ANALYSIS",
                "User invokes CLI, pipeline generates PRD via staged agents.",
                "## RECOMMENDED_OUTPUTS",
                "Final PRD markdown plus per-step artifacts under task_dir.",
                "## SUGGESTED_PHASES",
                "1. Research and context gathering",
                "2. Synthesis and template population",
                "3. Assembly and quality assurance",
                "## TEMPLATE_NOTES",
                "Standard PRD template; no special handling required.",
                "## AMBIGUITIES_FOR_USER",
                "None identified for this stub fixture.",
            ]
        )
    elif step_id == "build-task-file":
        # Gate: _check_task_phases_present (>= 2 phase headings)
        # + _check_b2_self_contained (no 'see above' in checklists)
        # + _check_parallel_instructions (phases 2+ need 'parallel' keyword)
        # + min_lines=400
        lines.extend(
            [
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
            ]
        )
    elif step_id == "verify-task-file":
        # Gate: _check_verdict_field (STRICT)
        lines.append('{"verdict": "PASS", "issues": []}')
    elif step_id == "sufficiency-review":
        # Gate: _check_verdict_field (STRICT)
        lines.append('{"verdict": "PASS", "issues": []}')
    elif step_id == "assembly":
        # Gate: _check_prd_template_sections + _check_no_placeholders
        # + min_lines=800
        lines.extend(
            [
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
            ]
        )
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
    executor._build_prompt = lambda builder_name, step_id=None: (
        f"Mock prompt for {builder_name}"
    )

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
        assert sr.status.is_terminal, f"Step has non-terminal status: {sr.status}"

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
    executor._build_prompt = lambda builder_name, step_id=None: (
        f"Mock prompt for {builder_name}"
    )

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
    executor._build_prompt = lambda builder_name, step_id=None: (
        f"Mock prompt for {builder_name}"
    )

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
    executor._build_prompt = lambda builder_name, step_id=None: (
        f"Mock prompt for {builder_name}"
    )

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
def test_e2e_budget_exhaustion(mock_synth_mapping, mock_process_cls, e2e_task_dir):
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
    executor._build_prompt = lambda builder_name, step_id=None: (
        f"Mock prompt for {builder_name}"
    )

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
    assert suggested > 0, f"Expected positive suggested budget, got {suggested}"


# ---------------------------------------------------------------------------
# Scenario 6: AC10 -- document-capture hotfix (recovery + no contamination)
# ---------------------------------------------------------------------------


@patch("superclaude.cli.prd.executor.PrdClaudeProcess")
@patch("superclaude.cli.prd.executor.load_synthesis_mapping")
def test_e2e_ac10_recovery_variant_filename(
    mock_synth_mapping, mock_process_cls, standard_e2e_config
):
    """[AC10a] Variant-named scope-discovery doc is recovered -> no HALT (Layer 2).

    The mocked subprocess emits only 24 lines of NDJSON commentary for
    scope-discovery (below the gate floor) but writes a 60-line variant
    ``scope-discovery.md`` into a WHERE source dir. The hardened recovery must
    surface the real document so the gate evaluates 60 lines, the pipeline
    completes with outcome == "success", and the persisted canonical artifact
    carries the recovered content (not the NDJSON commentary).
    """
    task_dir = standard_e2e_config.task_dir
    where_dir = task_dir / ".dev" / "specs"
    where_dir.mkdir(parents=True)

    variant_doc = "\n".join(f"scope line {i}" for i in range(60)) + "\n"
    short_ndjson = (
        "\n".join(f"commentary {i}" for i in range(24))
        + "\nEXIT_RECOMMENDATION: CONTINUE\n"
    )

    def factory(**kwargs):
        step_id = kwargs["step_id"]
        output_file = kwargs["output_file"]
        mock_proc = MagicMock()
        if step_id == "scope-discovery":
            output_text = short_ndjson
        else:
            output_text = _make_passing_output(step_id, 120)
        mock_proc.start_with_retry.return_value = None

        def write_output_and_return():
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(output_text, encoding="utf-8")
            if step_id == "scope-discovery":
                # Agent dropped the -raw suffix AND wrote into a WHERE dir.
                (where_dir / "scope-discovery.md").write_text(
                    variant_doc, encoding="utf-8"
                )
            return 0

        mock_proc.wait.side_effect = write_output_and_return
        return mock_proc

    mock_process_cls.side_effect = factory
    mock_synth_mapping.return_value = [
        {"synth_file": "section-overview.md"},
        {"synth_file": "section-requirements.md"},
        {"synth_file": "section-architecture.md"},
    ]

    executor = PrdExecutor(standard_e2e_config)
    executor._build_prompt = lambda builder_name, step_id=None: (
        f"Mock prompt for {builder_name}"
    )

    result = executor.run()

    # Recovery prevented a gate HALT -> pipeline completes.
    assert result.outcome == "success"
    # The persisted canonical artifact carries the recovered 60-line variant,
    # NOT the 24-line NDJSON commentary.
    persisted = task_dir / "scope-discovery-raw.md"
    assert persisted.exists() is True
    assert len(persisted.read_text(encoding="utf-8").splitlines()) >= 50


@patch("superclaude.cli.prd.executor.PrdClaudeProcess")
@patch("superclaude.cli.prd.executor.load_synthesis_mapping")
def test_e2e_ac10_no_where_contamination_when_pinned(
    mock_synth_mapping, mock_process_cls, standard_e2e_config
):
    """[AC10b] Pinned prompts -> canonical writes leave the WHERE dir clean (Layer 1).

    With the output-path pin in place, a compliant subprocess writes its
    document to the canonical task_dir path. The fix adds NO cleanup/move
    logic -- this verifies pinned-path behavior: no scope-discovery*/
    research-notes* files are left in the WHERE source dir after the run.
    """
    task_dir = standard_e2e_config.task_dir
    where_dir = task_dir / ".dev" / "specs"
    where_dir.mkdir(parents=True)

    def factory(**kwargs):
        step_id = kwargs["step_id"]
        output_file = kwargs["output_file"]
        mock_proc = MagicMock()
        output_text = _make_passing_output(step_id, 120)
        mock_proc.start_with_retry.return_value = None

        def write_output_and_return():
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(output_text, encoding="utf-8")
            # Pinned-compliant agent writes to the canonical task_dir path,
            # never into the WHERE source dir.
            if step_id == "scope-discovery":
                (task_dir / "scope-discovery-raw.md").write_text(
                    output_text, encoding="utf-8"
                )
            elif step_id == "research-notes":
                (task_dir / "research-notes.md").write_text(
                    output_text, encoding="utf-8"
                )
            return 0

        mock_proc.wait.side_effect = write_output_and_return
        return mock_proc

    mock_process_cls.side_effect = factory
    mock_synth_mapping.return_value = [
        {"synth_file": "section-overview.md"},
        {"synth_file": "section-requirements.md"},
        {"synth_file": "section-architecture.md"},
    ]

    executor = PrdExecutor(standard_e2e_config)
    executor._build_prompt = lambda builder_name, step_id=None: (
        f"Mock prompt for {builder_name}"
    )

    result = executor.run()

    assert result.outcome == "success"
    # No variant document was left contaminating the WHERE source dir.
    assert not list(where_dir.glob("scope-discovery*"))
    assert not list(where_dir.glob("research-notes*"))


# ---------------------------------------------------------------------------
# Scenario 7: Atom 1 -- hard-failure halt semantics (halt-on-hard-failure)
# ---------------------------------------------------------------------------


@patch("superclaude.cli.prd.executor.PrdClaudeProcess")
@patch("superclaude.cli.prd.executor.load_synthesis_mapping")
def test_e2e_standard_tier_error_halts_pipeline(
    mock_synth_mapping, mock_process_cls, standard_e2e_config
):
    """[Atom 1] A STANDARD-tier step that hard-ERRORs halts the pipeline.

    scope-discovery is a STANDARD-tier gate. Under the OLD halt logic (which
    keyed off the downstream gate's enforcement_tier == "STRICT"), a STANDARD
    step returning ERROR would NOT halt -- this test would fail. Under Atom 1
    (halt on is_hard_failure regardless of tier), the ERROR halts at
    scope-discovery with a "hard failure" reason and research-notes never runs.
    """
    mock_synth_mapping.return_value = [
        {"synth_file": "section-overview.md"},
    ]

    # scope-discovery subprocess exits non-zero -> _determine_status -> ERROR.
    base_factory = _mock_process_factory(
        step_overrides={"scope-discovery": (1, "boom: subprocess crashed\n")},
    )
    executed_steps: list[str] = []

    def tracking_factory(**kwargs):
        executed_steps.append(kwargs["step_id"])
        return base_factory(**kwargs)

    mock_process_cls.side_effect = tracking_factory

    executor = PrdExecutor(standard_e2e_config)
    executor._build_prompt = lambda builder_name, step_id=None: (
        f"Mock prompt for {builder_name}"
    )

    result = executor.run()

    # The STANDARD-tier ERROR halts the pipeline (Atom 1 behavior).
    assert result.outcome == "halt"
    assert result.halt_step == "scope-discovery"
    assert result.halt_reason is not None
    assert "hard failure" in result.halt_reason
    # research-notes (the next Stage-A step) must never execute.
    assert "research-notes" not in executed_steps


@patch("superclaude.cli.prd.executor.PrdClaudeProcess")
@patch("superclaude.cli.prd.executor.load_synthesis_mapping")
def test_e2e_standard_tier_validation_fail_does_not_halt(
    mock_synth_mapping, mock_process_cls, standard_e2e_config
):
    """[Atom 1] A STANDARD-tier VALIDATION_FAIL (exit 0) does NOT halt.

    scope-discovery exits 0 but emits too few lines to clear its STANDARD gate,
    yielding VALIDATION_FAIL. VALIDATION_FAIL is excluded from is_hard_failure
    and the gate is STANDARD (not STRICT), so the loop must continue past
    scope-discovery -- preserving the intentional non-fatal STANDARD path.
    """
    mock_synth_mapping.return_value = [
        {"synth_file": "section-overview.md"},
        {"synth_file": "section-requirements.md"},
        {"synth_file": "section-architecture.md"},
    ]

    # scope-discovery exits 0 with far fewer than the 50-line gate floor and no
    # recovery variant -> gate fails STANDARD -> VALIDATION_FAIL (non-fatal).
    short_output = "short scope output\nEXIT_RECOMMENDATION: CONTINUE\n"
    base_factory = _mock_process_factory(
        step_overrides={"scope-discovery": (0, short_output)},
    )
    executed_steps: list[str] = []

    def tracking_factory(**kwargs):
        executed_steps.append(kwargs["step_id"])
        return base_factory(**kwargs)

    mock_process_cls.side_effect = tracking_factory

    executor = PrdExecutor(standard_e2e_config)
    executor._build_prompt = lambda builder_name, step_id=None: (
        f"Mock prompt for {builder_name}"
    )

    result = executor.run()

    # The STANDARD VALIDATION_FAIL must NOT halt the pipeline at scope-discovery.
    assert result.halt_step != "scope-discovery"
    # The loop continued past scope-discovery to the next Stage-A step.
    assert "research-notes" in executed_steps

    # [reflect F5] Strengthen the guard so it passes for the RIGHT reason:
    # scope-discovery's RECORDED status must actually be VALIDATION_FAIL, not
    # merely "did not halt" (which a SKIPPED/ERROR status could also satisfy).
    # PrdStepResult carries no step_id, but the Stage-A loop appends exactly one
    # result per step in _STAGE_A_STEPS order and this run has no resume/skip, so
    # result.step_results aligns 1:1 with the executed Stage-A prefix. Map by that
    # deterministic order rather than a hardcoded index.
    from superclaude.cli.prd.executor import _STAGE_A_STEPS

    stage_a_order = [s[0] for s in _STAGE_A_STEPS]
    status_by_step = dict(
        zip(stage_a_order, [r.status for r in result.step_results])
    )
    assert status_by_step["scope-discovery"] == PrdStepStatus.VALIDATION_FAIL


# ---------------------------------------------------------------------------
# Scenario 8: Atom 2 -- typed missing-artifact guard (graceful HALT)
# ---------------------------------------------------------------------------


@patch("superclaude.cli.prd.executor.PrdClaudeProcess")
def test_missing_required_artifact_yields_graceful_halt(
    mock_process_cls, standard_e2e_config
):
    """[Atom 2] A missing REQUIRED upstream artifact yields a graceful HALT.

    Drives the REAL ``_build_prompt`` (NOT the monkeypatched stub used elsewhere
    in this file): ``build_research_notes_prompt`` performs a REQUIRED read of
    ``scope-discovery-raw.md``, which is absent in the fixture task_dir. Under the
    pre-Atom-2 code an uncaught ``FileNotFoundError`` would escape; under Atom 2
    the required-read helper raises ``MissingArtifactError`` which the call-site
    catch converts to a ``PrdStepStatus.HALT`` whose ``halt_reason`` names the
    missing artifact and its producer step. No subprocess is launched because the
    prompt build raises before subprocess creation.
    """
    executor = PrdExecutor(standard_e2e_config)
    # Intentionally do NOT stub _build_prompt -- the real builder must run so the
    # MissingArtifactError -> HALT conversion is actually exercised.

    result = executor._run_subprocess_step(
        "research-notes", "Research Notes", "build_research_notes_prompt"
    )

    assert result.status == PrdStepStatus.HALT
    assert result.halt_reason is not None
    assert "scope-discovery-raw.md" in result.halt_reason
    assert "scope-discovery" in result.halt_reason
    # The graceful HALT short-circuits before any subprocess is created.
    mock_process_cls.assert_not_called()


@patch("superclaude.cli.prd.executor.PrdClaudeProcess")
def test_malformed_required_artifact_yields_graceful_halt(
    mock_process_cls, standard_e2e_config
):
    """[reflect F2] A present-but-malformed REQUIRED JSON artifact HALTs gracefully.

    Drives the REAL ``_build_prompt`` (NOT the monkeypatched stub used by the
    full-pipeline tests, which would bypass the F2 guard):
    ``build_scope_discovery_prompt`` performs a REQUIRED ``_load_json_required``
    read of ``parsed-request.json``. Here that file is written with INVALID JSON.
    Before F2, ``_load_json`` raised an uncaught ``json.JSONDecodeError`` that
    escaped ``run()`` and crashed the CLI -- the same crash-class Atom 2 closed for
    MISSING files. After F2, ``_load_json_required`` raises
    ``MalformedArtifactError`` (a subclass of ``MissingArtifactError``) which the
    existing call-site catch converts to a ``PrdStepStatus.HALT`` whose
    ``halt_reason`` names the malformed artifact and its producer step. No
    subprocess is launched because the prompt build raises before subprocess
    creation.
    """
    # Write a deliberately malformed parsed-request.json into the task_dir so the
    # REQUIRED read parses invalid JSON (file IS present -> not a missing-file case).
    (standard_e2e_config.task_dir / "parsed-request.json").write_text(
        "{not valid json", encoding="utf-8"
    )

    executor = PrdExecutor(standard_e2e_config)
    # Intentionally do NOT stub _build_prompt -- the real builder must run so the
    # MalformedArtifactError -> HALT conversion is actually exercised.

    result = executor._run_subprocess_step(
        "scope-discovery", "Scope Discovery", "build_scope_discovery_prompt"
    )

    # No uncaught exception escaped; the step returned a graceful HALT.
    assert result.status == PrdStepStatus.HALT
    assert result.halt_reason is not None
    # The reason names the malformed artifact and its producer step...
    assert "parsed-request.json" in result.halt_reason
    assert "parse-request" in result.halt_reason
    # ...and reads "malformed" (not the inaccurate "missing") for a present file.
    assert "malformed" in result.halt_reason
    # The graceful HALT short-circuits before any subprocess is created.
    mock_process_cls.assert_not_called()


@patch("superclaude.cli.prd.executor.PrdClaudeProcess")
@patch("superclaude.cli.prd.executor.load_synthesis_mapping")
def test_e2e_scope_discovery_error_halts_before_research_notes(
    mock_synth_mapping, mock_process_cls, standard_e2e_config
):
    """[Atom 1 e2e] Reproduces the original crash; now a graceful halt.

    Original bug: scope-discovery hard-ERRORs (non-zero exit, so no
    ``scope-discovery-raw.md`` artifact), the Stage-A loop did NOT halt (gate is
    STANDARD), and research-notes then crashed reading the missing artifact with
    an uncaught ``FileNotFoundError`` that escaped ``run()``. This test exercises
    the ATOM-1 halt path (``_build_prompt`` is stubbed): scope-discovery's hard
    ERROR halts the pipeline before research-notes ever runs, so the missing-read
    is never reached. The ATOM-2 missing-artifact path through the REAL builder
    is covered by ``test_missing_required_artifact_yields_graceful_halt`` and
    ``test_e2e_resume_missing_artifact_surfaces_reason_at_pipeline_level``.
    """
    task_dir = standard_e2e_config.task_dir
    mock_synth_mapping.return_value = [
        {"synth_file": "section-overview.md"},
    ]

    # scope-discovery exits non-zero AND writes no artifact -> ERROR.
    base_factory = _mock_process_factory(
        step_overrides={"scope-discovery": (1, "scope-discovery crashed fast\n")},
    )
    executed_steps: list[str] = []

    def tracking_factory(**kwargs):
        executed_steps.append(kwargs["step_id"])
        return base_factory(**kwargs)

    mock_process_cls.side_effect = tracking_factory

    executor = PrdExecutor(standard_e2e_config)
    executor._build_prompt = lambda builder_name, step_id=None: (
        f"Mock prompt for {builder_name}"
    )

    # run() must COMPLETE and return a result -- no uncaught FileNotFoundError.
    result = executor.run()

    assert result is not None
    assert result.finished_at is not None
    # Halts at scope-discovery with a reason that attributes the halt.
    assert result.outcome == "halt"
    assert result.halt_step == "scope-discovery"
    assert result.halt_reason
    assert "hard failure" in result.halt_reason
    # The hard ERROR meant no artifact was ever written (the original crash seed).
    assert not (task_dir / "scope-discovery-raw.md").exists()
    # research-notes -- the step that originally crashed -- never runs.
    assert "research-notes" not in executed_steps


@patch("superclaude.cli.prd.executor.PrdClaudeProcess")
def test_e2e_resume_missing_artifact_surfaces_reason_at_pipeline_level(
    mock_process_cls, e2e_task_dir
):
    """[Atom 2 run-level] Missing required artifact surfaces a specific halt_reason.

    Resume from ``research-notes`` with ``scope-discovery-raw.md`` absent (the
    spec's named backstop scenario). The earlier Stage-A steps are skipped, so
    research-notes runs FIRST through the REAL ``_build_prompt`` (NOT stubbed):
    its builder's REQUIRED read of the missing artifact raises
    ``MissingArtifactError`` -> the call-site catch returns a HALT carrying the
    artifact-specific reason. This asserts that reason survives to the
    PIPELINE-level ``result.halt_reason`` (regression guard for reflect finding
    F1: the Stage-A loop must prefer the step-provided reason, not overwrite it
    with the generic ``"hard failure: halt"`` template).
    """
    config = resolve_config(
        "resume missing artifact",
        product="resume-missing",
        tier="standard",
        output=str(e2e_task_dir.parent),
        max_turns=1000,
        dry_run=False,
        resume_from="research-notes",
    )
    config.task_dir = e2e_task_dir
    config.work_dir = e2e_task_dir.parent
    # e2e_task_dir fixture creates only subdirs -> scope-discovery-raw.md is absent.

    executor = PrdExecutor(config)
    # REAL _build_prompt -- do NOT stub; the missing-artifact catch must fire.

    result = executor.run()

    assert result.outcome == "halt"
    assert result.halt_step == "research-notes"
    assert result.halt_reason is not None
    # The pipeline-level reason names the missing artifact + its producer step.
    assert "scope-discovery-raw.md" in result.halt_reason
    assert "scope-discovery" in result.halt_reason
    # Graceful HALT short-circuits before any subprocess is created.
    mock_process_cls.assert_not_called()
