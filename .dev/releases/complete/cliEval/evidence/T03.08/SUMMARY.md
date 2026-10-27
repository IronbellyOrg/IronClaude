# T03.08 — NFR-REL2 Bounded Retry Policy — Evidence Summary

**Task:** T03.08 (Phase 3, R-051, D-0051)
**Generated:** 2026-05-20
**Status:** PASS

## Deliverables

| Item | Path | Status |
|---|---|---|
| `DEFAULT_RETRY_COUNT` class constant | `src/superclaude/cli/eval/runner.py` | landed |
| `MCP_FLAKY_TAG` class constant | `src/superclaude/cli/eval/runner.py` | landed |
| `retry_count` constructor kwarg with non-zero guard | `src/superclaude/cli/eval/runner.py` (`EvalRunner.__init__`) | landed |
| Retry-policy test suite | `tests/cli/eval/test_retry_policy.py` | 11/11 PASS |
| `--eval <id>` subset re-run docs | `docs/eval/retry.md` | landed |
| D-0051 spec / notes / evidence | `artifacts/D-0051/{spec,notes,evidence}.md` | landed |

## Acceptance bullets

| Phase-file AC | Met by |
|---|---|
| Default `retry_count=0` enforced | `EvalRunner.DEFAULT_RETRY_COUNT == 0`; `test_default_retry_count_is_zero` |
| Monkeypatch test confirms no retries on failure | `test_monkeypatched_runner_confirms_no_retry_loop` + `test_fail_outcome_does_not_retry` |
| `--eval <id>` subset re-run documented | `docs/eval/retry.md` |
| `MCP_FLAKY_TAG` constant defined for R3-mit (T05.23) | `EvalRunner.MCP_FLAKY_TAG == "MCP-flaky"` |
| D-0051 spec records the retry policy | `artifacts/D-0051/spec.md` |

## Pytest evidence

* `pytest-retry-policy.txt` — `tests/cli/eval/test_retry_policy.py -v`,
  **11 passed in 0.14 s**.
* `pytest-regression-cli-eval.txt` — `tests/cli/eval/ -q`, **828
  passed, 1 warning in 10.03 s** (pre-existing pty/forkpty
  `DeprecationWarning`).

## Out-of-scope (deferred to T05.23)

* MCP-flaky retry-once code path (OQ-10 dependency).
* EvalSpec `tags` field for retry-once eligibility (schema bump).
* CLI surface change for `--retry-count` (not authored by NFR-REL2).
