"""Unit tests for the PRD pipeline executor.

Section 8.1 tests: sentinel detection and status determination.
5 test functions covering:
1. test_determine_status_pass -- EXIT_RECOMMENDATION: CONTINUE -> PASS
2. test_determine_status_halt -- EXIT_RECOMMENDATION: HALT -> HALT
3. test_determine_status_qa_fail -- verdict: FAIL -> QA_FAIL
4. test_determine_status_timeout -- exit code 124 -> TIMEOUT
5. test_sentinel_not_matched_in_code_block -- F-007 code block exclusion

All tests use mocked ClaudeProcess (no real subprocess launches).
"""

from __future__ import annotations

import pytest

from superclaude.cli.prd.config import resolve_config
from superclaude.cli.prd.executor import PrdExecutor, _detect_sentinel
from superclaude.cli.prd.models import PrdStepStatus

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def prd_config():
    """Create a test PrdConfig (dry-run to avoid side effects)."""
    return resolve_config(
        "test product for unit tests",
        product="test-product",
        tier="standard",
        dry_run=True,
    )


@pytest.fixture
def executor(prd_config):
    """Create a PrdExecutor instance for testing."""
    return PrdExecutor(prd_config)


# ---------------------------------------------------------------------------
# Test 1: EXIT_RECOMMENDATION: CONTINUE -> PASS
# ---------------------------------------------------------------------------


def test_determine_status_pass(executor):
    """EXIT_RECOMMENDATION: CONTINUE should produce PASS status."""
    output = (
        "Some subprocess output here...\n"
        "Analysis complete.\n"
        "EXIT_RECOMMENDATION: CONTINUE\n"
    )
    status = executor._determine_status(
        exit_code=0, output=output, step_id="parse-request"
    )
    assert status == PrdStepStatus.PASS


# ---------------------------------------------------------------------------
# Test 2: EXIT_RECOMMENDATION: HALT -> HALT
# ---------------------------------------------------------------------------


def test_determine_status_halt(executor):
    """EXIT_RECOMMENDATION: HALT should produce HALT status."""
    output = "Critical error detected.\nEXIT_RECOMMENDATION: HALT\n"
    status = executor._determine_status(
        exit_code=0, output=output, step_id="parse-request"
    )
    assert status == PrdStepStatus.HALT


# ---------------------------------------------------------------------------
# Test 3: verdict: FAIL -> QA_FAIL
# ---------------------------------------------------------------------------


def test_determine_status_qa_fail(executor):
    """QA step with verdict: FAIL should produce QA_FAIL status."""
    output = 'QA Review Results:\n"verdict": "FAIL"\nIssues found: missing sections\n'
    status = executor._determine_status(
        exit_code=0, output=output, step_id="research-qa"
    )
    assert status == PrdStepStatus.QA_FAIL


# ---------------------------------------------------------------------------
# Test 4: exit code 124 -> TIMEOUT
# ---------------------------------------------------------------------------


def test_determine_status_timeout(executor):
    """Exit code 124 should produce TIMEOUT status regardless of output."""
    output = "Partial output before timeout...\n"
    status = executor._determine_status(
        exit_code=124, output=output, step_id="investigation-1"
    )
    assert status == PrdStepStatus.TIMEOUT


# ---------------------------------------------------------------------------
# Test 5: EXIT_RECOMMENDATION inside code block is ignored (F-007)
# ---------------------------------------------------------------------------


def test_sentinel_not_matched_in_code_block():
    """EXIT_RECOMMENDATION inside a fenced code block must be ignored.

    F-007: Sentinel detection uses anchored regex with code block
    exclusion to prevent false matches from code examples.
    """
    output = (
        "Here is an example of how exit recommendations work:\n"
        "\n"
        "```\n"
        "EXIT_RECOMMENDATION: HALT\n"
        "```\n"
        "\n"
        "The above is just an example.\n"
        "EXIT_RECOMMENDATION: CONTINUE\n"
    )
    # The HALT inside the code block should be ignored;
    # only the CONTINUE outside should be detected.
    result = _detect_sentinel(output)
    assert result == "CONTINUE", (
        f"Expected CONTINUE (HALT is inside code block), got {result}"
    )

    # Also test: sentinel ONLY inside code block -> None
    output_only_in_block = (
        "Some output\n```\nEXIT_RECOMMENDATION: HALT\n```\nNo sentinel outside.\n"
    )
    result_none = _detect_sentinel(output_only_in_block)
    assert result_none is None, (
        f"Expected None when sentinel is only in code block, got {result_none}"
    )


# ---------------------------------------------------------------------------
# Layer 3 / Layer 1 hotfix acceptance tests (AC7, AC8)
# ---------------------------------------------------------------------------


def test_determine_status_reads_ndjson_channel_inv010(executor):
    """[AC7] Sentinel + verdict detection still read the NDJSON output_text channel.

    After gate content moved to disk (gate_content), _determine_status must
    still operate on the NDJSON output_text: the EXIT_RECOMMENDATION sentinel
    and the QA verdict live only in the assistant's stdout commentary, never in
    the on-disk artifact (INV-010).
    """
    continue_output = (
        "Assistant commentary in the NDJSON stream...\n"
        "EXIT_RECOMMENDATION: CONTINUE\n"
    )
    assert (
        executor._determine_status(
            exit_code=0, output=continue_output, step_id="parse-request"
        )
        == PrdStepStatus.PASS
    )

    qa_fail_output = 'QA Review Results:\n"verdict": "FAIL"\nmissing sections\n'
    assert (
        executor._determine_status(
            exit_code=0, output=qa_fail_output, step_id="research-qa"
        )
        == PrdStepStatus.QA_FAIL
    )


def test_persist_step_artifact_writes_canonical_name(tmp_path):
    """[AC8] _persist_step_artifact writes the canonical filename resume probes expect.

    Resume detection depends on the artifact existing at exactly
    task_dir / _STEP_ARTIFACT_FILES[step_id] (e.g. research-notes.md). This
    canonical-name write must be unchanged by the hotfix.
    """
    task_dir = tmp_path / "prd-persist"
    task_dir.mkdir()
    config = resolve_config(
        "persist test product",
        product="persist-test",
        tier="standard",
        output=str(tmp_path),
        dry_run=True,
    )
    config.task_dir = task_dir
    executor = PrdExecutor(config)

    content = "Persisted research notes line 1\nline 2\nline 3\n"
    executor._persist_step_artifact("research-notes", content)

    artifact = task_dir / "research-notes.md"
    assert artifact.exists() is True
    assert artifact.read_text(encoding="utf-8") == content


# ---------------------------------------------------------------------------
# _evaluate_gate: advisory semantic checks are non-fatal (the live PRD path)
# ---------------------------------------------------------------------------


def _gate_with(check):
    from superclaude.cli.pipeline.models import GateCriteria

    return GateCriteria(
        required_frontmatter_fields=[],
        min_lines=0,
        enforcement_tier="STRICT",
        semantic_checks=[check],
    )


def _check(name, advisory):
    from superclaude.cli.pipeline.models import SemanticCheck

    # check_fn returns a failure string (never True) -> the check "fails".
    return SemanticCheck(
        name=name,
        check_fn=lambda c: f"{name} failed",
        failure_message=f"{name} msg",
        advisory=advisory,
    )


def test_evaluate_gate_advisory_failure_does_not_halt(executor, caplog):
    """An advisory semantic check that fails must NOT fail the gate (the PRD
    executor path -- _evaluate_gate, not pipeline.gates.gate_passed)."""
    import logging

    gate = _gate_with(_check("advisory_check", advisory=True))
    with caplog.at_level(logging.WARNING, logger="superclaude.prd.executor"):
        result = executor._evaluate_gate("some-step", gate, "body line\nmore\n")
    assert result is True
    assert any(
        "advisory_check" in r.getMessage() and "some-step" in r.getMessage()
        for r in caplog.records
    )


def test_evaluate_gate_non_advisory_failure_still_halts(executor):
    gate = _gate_with(_check("strict_check", advisory=False))
    result = executor._evaluate_gate("some-step", gate, "body line\nmore\n")
    assert result is False


def test_evaluate_gate_advisory_then_strict_still_halts(executor):
    from superclaude.cli.pipeline.models import GateCriteria

    gate = GateCriteria(
        required_frontmatter_fields=[],
        min_lines=0,
        enforcement_tier="STRICT",
        semantic_checks=[
            _check("advisory_check", advisory=True),
            _check("strict_check", advisory=False),
        ],
    )
    result = executor._evaluate_gate("some-step", gate, "body line\nmore\n")
    assert result is False
