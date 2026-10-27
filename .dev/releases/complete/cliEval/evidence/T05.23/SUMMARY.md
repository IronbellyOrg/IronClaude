# T05.23 — Evidence Summary

## Task

R3-mit MCP retry-once policy (D-0101).

## Verification

```bash
uv run pytest tests/cli/eval/test_mcp_retry_once.py -v
# 26 passed in 0.20s

uv run pytest tests/cli/eval/test_retry_policy.py tests/cli/eval/test_mcp_retry_once.py tests/cli/eval/test_runner_class.py -v
# 48 passed in 1.32s
```

## Evidence files

| File | Contents |
|---|---|
| `pytest-mcp-retry-once.txt` | Verbatim pytest output for the new test file (26 tests, all passing). |
| `pytest-regression-retry.txt` | Regression run covering: T03.08 NFR-REL2 baseline (`test_retry_policy.py`, 11 tests) + T05.23 R3-mit policy (`test_mcp_retry_once.py`, 26 tests) + T03.05 runner-class regression (`test_runner_class.py`, 11 tests). 48 tests total, all passing. |

## Acceptance criteria → evidence

| AC bullet | Pin | Evidence |
|---|---|---|
| Tagged spec retries once on MCP-flaky failure | `test_runner_retries_once_on_mcp_flaky_failure` PASSED | `pytest-mcp-retry-once.txt` |
| Persistent failure yields `FAIL` with `mcp_server_flaky` artifact | Same test (asserts `outcome.status == "FAIL"` and `outcome.artifacts["mcp_server_flaky"] == "true"`) | `pytest-mcp-retry-once.txt` |
| Non-tagged evals do not retry (NFR-REL2 default honored) | `test_runner_does_not_retry_untagged_eval` + `test_fail_outcome_does_not_retry` (T03.08 regression) | both .txt files |
| `D-0101/spec.md` documents the retry policy | `artifacts/D-0101/spec.md` written | n/a (artifact in tree) |
| OQ-10 decision recorded | Section 6 of `D-0101/spec.md` records the closure (R3-mit stays P1, opt-in tag) | `artifacts/D-0101/spec.md §6` |

## Notes

* No regression in pre-existing `test_retry_policy.py` (NFR-REL2 stays
  intact — the new `retry_policy` kwarg is orthogonal to
  `retry_count`).
* No regression in `test_runner_class.py` — the `run()` / `_execute_once()`
  refactor preserves the FR-LC1 lifecycle skeleton verbatim.
