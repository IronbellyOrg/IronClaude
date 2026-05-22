# D-0028 — Evidence (Task T02.07)

## Acceptance-criteria check

| Criterion | Result |
|---|---|
| `HomeIsolation` exposes `setup`, `env`, `teardown(keep)`, `state_path(suffix)` | PASS — `src/superclaude/cli/eval/isolation.py` |
| Preserves the 4 existing IsolationLayers guarantees | PASS — `test_isolation_layers_probe_still_passes_after_extension` re-runs probe |
| `env()` returns `HOME`, `CLAUDE_SESSION_ID`, optional `CLAUDE_FAKE_TIME_OFFSET` | PASS — `test_env_includes_home_and_session_id`, `test_env_omits_time_offset_when_zero`, `test_env_includes_time_offset_when_nonzero` |
| Per-eval HOMEs are sibling directories under `home_root` (concurrency-safe) | PASS — `test_two_setups_under_same_root_are_siblings_and_isolated`, `test_parallel_setup_does_not_collide` |
| `D-0028/spec.md` records the method contract | PASS — `artifacts/D-0028/spec.md` |

## Test results

`uv run pytest tests/cli/eval/test_home_isolation_extend.py tests/cli/eval/test_isolation_dataclass.py tests/cli/eval/test_isolation_layers_probe.py -v`

Result: **83 passed in 0.21s** — see `evidence/T02.07/pytest-T02.07.log`.

Full eval suite (`uv run pytest tests/cli/eval/ -q`) — **402 passed in 1.00s**.

## Manual validation

> Build a HomeIsolation and confirm `setup()` creates a sibling HOME under home_root.

Equivalent test: `test_setup_creates_directory_under_home_root`
(`tests/cli/eval/test_home_isolation_extend.py`). The test creates a
`HomeIsolation(eval_id="E1", home_root=<scratch>, session_id="sess-001")`,
calls `setup()`, and asserts:

* The returned path exists on disk.
* It is a directory.
* Its parent equals the declared `home_root`.

## Files changed

* `src/superclaude/cli/eval/isolation.py` — module docstring rewritten, 4 new
  methods + `home_path` property + `is_set_up` predicate.
* `tests/cli/eval/test_home_isolation_extend.py` — new test module
  (35 tests).
* `.dev/releases/current/cliEval/artifacts/D-0028/{spec,notes,evidence}.md` —
  D-0028 deliverable artifacts.

## Files NOT changed (confirms preservation)

* `src/superclaude/cli/sprint/executor.py` — `IsolationLayers` untouched.
* `src/superclaude/cli/eval/__init__.py` — `HomeIsolation` already
  exported (T02.04).
