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
    output = (
        "Critical error detected.\n"
        "EXIT_RECOMMENDATION: HALT\n"
    )
    status = executor._determine_status(
        exit_code=0, output=output, step_id="parse-request"
    )
    assert status == PrdStepStatus.HALT


# ---------------------------------------------------------------------------
# Test 3: verdict: FAIL -> QA_FAIL
# ---------------------------------------------------------------------------


def test_determine_status_qa_fail(executor):
    """QA step with verdict: FAIL should produce QA_FAIL status."""
    output = (
        "QA Review Results:\n"
        '"verdict": "FAIL"\n'
        "Issues found: missing sections\n"
    )
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
        "Some output\n"
        "```\n"
        "EXIT_RECOMMENDATION: HALT\n"
        "```\n"
        "No sentinel outside.\n"
    )
    result_none = _detect_sentinel(output_only_in_block)
    assert result_none is None, (
        f"Expected None when sentinel is only in code block, got {result_none}"
    )
