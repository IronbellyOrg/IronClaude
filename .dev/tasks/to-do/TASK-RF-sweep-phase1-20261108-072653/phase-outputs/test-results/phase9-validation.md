# Phase 9 validation (item 9.4)

Run 2026-11-12, in order. Each block: the command, its exit code, the last 30 output lines, then one PASS or FAIL line.

## ruff check

Command: `uv run ruff check src/superclaude/cli tests/sweep`
Exit code: 0

```text
All checks passed!
```

PASS: ruff check

## ruff format --check

Command: `uv run ruff format --check src/superclaude/cli/sweep src/superclaude/cli/main.py tests/sweep`
Exit code: 0

```text
11 files already formatted
```

PASS: ruff format --check

## sweep --help

Command: `uv run superclaude sweep --help`
Exit code: 0

```text
Usage: superclaude sweep [OPTIONS] COMMAND [ARGS]...

  Read-only sweep of Orca Runs, worktrees and sessions.

Options:
  --help  Show this message and exit.

Commands:
  run  Collect, classify and publish one read-only report; print one JSON...
```

PASS: sweep --help

## pytest tests/sweep tests/unit -v

Command: `uv run pytest tests/sweep tests/unit -v`
Exit code: 0

```text
tests/unit/test_review_translation.py::test_good_translation_validation PASSED [ 96%]
tests/unit/test_review_translation.py::test_bad_translation_detection PASSED [ 96%]
tests/unit/test_self_check.py::TestSelfCheckProtocol::test_validate_passing_implementation PASSED [ 96%]
tests/unit/test_self_check.py::TestSelfCheckProtocol::test_validate_failing_implementation PASSED [ 96%]
tests/unit/test_self_check.py::TestSelfCheckProtocol::test_check_tests_passing_with_output PASSED [ 96%]
tests/unit/test_self_check.py::TestSelfCheckProtocol::test_check_requirements_met PASSED [ 96%]
tests/unit/test_self_check.py::TestSelfCheckProtocol::test_check_assumptions_verified PASSED [ 97%]
tests/unit/test_self_check.py::TestSelfCheckProtocol::test_check_evidence_exists PASSED [ 97%]
tests/unit/test_self_check.py::TestSelfCheckProtocol::test_detect_hallucinations_tests_without_output PASSED [ 97%]
tests/unit/test_self_check.py::TestSelfCheckProtocol::test_detect_hallucinations_complete_without_evidence PASSED [ 97%]
tests/unit/test_self_check.py::TestSelfCheckProtocol::test_detect_hallucinations_complete_with_failing_tests PASSED [ 97%]
tests/unit/test_self_check.py::TestSelfCheckProtocol::test_detect_hallucinations_ignored_errors PASSED [ 97%]
tests/unit/test_self_check.py::TestSelfCheckProtocol::test_detect_hallucinations_uncertainty_language PASSED [ 97%]
tests/unit/test_self_check.py::TestSelfCheckProtocol::test_format_report_passing PASSED [ 98%]
tests/unit/test_self_check.py::TestSelfCheckProtocol::test_format_report_failing PASSED [ 98%]
tests/unit/test_self_check.py::test_self_check_marker_integration PASSED [ 98%]
tests/unit/test_token_budget.py::TestTokenBudgetManager::test_simple_complexity PASSED [ 98%]
tests/unit/test_token_budget.py::TestTokenBudgetManager::test_medium_complexity PASSED [ 98%]
tests/unit/test_token_budget.py::TestTokenBudgetManager::test_complex_complexity PASSED [ 98%]
tests/unit/test_token_budget.py::TestTokenBudgetManager::test_default_complexity PASSED [ 98%]
tests/unit/test_token_budget.py::TestTokenBudgetManager::test_invalid_complexity_defaults_to_medium PASSED [ 99%]
tests/unit/test_token_budget.py::TestTokenBudgetManager::test_token_usage_tracking PASSED [ 99%]
tests/unit/test_token_budget.py::TestTokenBudgetManager::test_budget_allocation_strategy PASSED [ 99%]
tests/unit/test_token_budget.py::TestTokenBudgetManager::test_complexity_examples PASSED [ 99%]
tests/unit/test_token_budget.py::test_complexity_marker_simple PASSED    [ 99%]
tests/unit/test_token_budget.py::test_complexity_marker_medium PASSED    [ 99%]
tests/unit/test_token_budget.py::test_complexity_marker_complex PASSED   [ 99%]
tests/unit/test_token_budget.py::test_token_budget_no_marker PASSED      [100%]

================== 726 passed, 2 skipped in 285.11s (0:04:45) ==================
```

PASS: pytest tests/sweep tests/unit -v
