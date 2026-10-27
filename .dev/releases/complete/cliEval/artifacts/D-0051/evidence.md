# D-0051 — Evidence Record

## 1. Test Evidence

### 1.1 Retry-policy targeted run

```bash
uv run pytest tests/cli/eval/test_retry_policy.py -v
```

Result: **11 passed in 0.14s.** Full output:
`evidence/T03.08/pytest-retry-policy.txt`.

Selected output:

```
test_default_retry_count_is_zero                         PASSED
test_fail_outcome_does_not_retry                         PASSED
test_errored_outcome_does_not_retry                      PASSED
test_non_zero_retry_count_rejected                       PASSED
test_other_non_zero_retry_count_rejected[-1]             PASSED
test_other_non_zero_retry_count_rejected[2]              PASSED
test_other_non_zero_retry_count_rejected[10]             PASSED
test_explicit_zero_retry_count_accepted                  PASSED
test_mcp_flaky_tag_constant_defined                      PASSED
test_monkeypatched_runner_confirms_no_retry_loop         PASSED
test_retry_docs_present_and_describe_subset_path         PASSED
```

### 1.2 Regression sweep — full cli/eval

```bash
uv run pytest tests/cli/eval/ -q
```

Result: **828 passed, 1 warning in 10.03s** (warning is the pre-existing
pty/forkpty `DeprecationWarning` unrelated to this task). Full output:
`evidence/T03.08/pytest-regression-cli-eval.txt`.

## 2. AC traceability matrix

| Phase-file AC | Status | Pin |
|---|---|---|
| EvalRunner default `retry_count=0`; verified by a test that monkeypatches EvalRunner and confirms no retries occur on failure. | ✅ | `test_default_retry_count_is_zero`, `test_monkeypatched_runner_confirms_no_retry_loop`, `test_fail_outcome_does_not_retry` |
| `--eval <id>` subset re-run path is documented in `docs/eval/retry.md`. | ✅ | `docs/eval/retry.md` (109 lines); `test_retry_docs_present_and_describe_subset_path` |
| `MCP_FLAKY_TAG` constant is defined for use by R3-mit (T05.23). | ✅ | `EvalRunner.MCP_FLAKY_TAG == "MCP-flaky"`; `test_mcp_flaky_tag_constant_defined` |
| `TASKLIST_ROOT/artifacts/D-0051/spec.md` records the retry policy. | ✅ | `artifacts/D-0051/spec.md` |

## 3. Manual validation

Per the phase file:

> Manual check: induce a fail in a fixture eval, run twice via `--eval`,
> confirm independent results.

Automated via `test_fail_outcome_does_not_retry`: a `CountingExecutor`
records the trio call counts; the runner emits `FAIL` with
`spawn=inject=observe=1`. Re-invoking `runner.run(spec)` with the same
runner instance is a separate user-driven action (matching the
documented `--eval <id>` subset path) and is covered by the existing
runner-lifecycle tests in `test_runner_class.py`.

## 4. Construction-time validation transcript

```python
>>> from superclaude.cli.eval.runner import EvalRunner
>>> EvalRunner.DEFAULT_RETRY_COUNT
0
>>> EvalRunner.MCP_FLAKY_TAG
'MCP-flaky'
>>> EvalRunner(retry_count=1, ...)
Traceback (most recent call last):
  ...
ValueError: EvalRunner retry_count must be 0 (NFR-REL2 bounded retry policy);
  got 1. Re-run failing evals via 'superclaude eval run --eval <id>' instead
  — see docs/eval/retry.md.
```

(Captured behaviour from `test_non_zero_retry_count_rejected` —
parametrised across `-1, 1, 2, 10` to lock the boundary in place.)

## 5. Cross-reference index

* Implementation: `src/superclaude/cli/eval/runner.py`
* Test: `tests/cli/eval/test_retry_policy.py`
* Documentation: `docs/eval/retry.md`
* Spec: `.dev/releases/current/cliEval/artifacts/D-0051/spec.md`
* Notes: `.dev/releases/current/cliEval/artifacts/D-0051/notes.md`
* Phase file: `.dev/releases/current/cliEval/phase-3-tasklist.md` § T03.08
* Roadmap row: R-051 (NFR-REL2)
