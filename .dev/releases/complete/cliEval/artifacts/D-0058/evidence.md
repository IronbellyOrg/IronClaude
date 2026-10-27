# D-0058 — Verification Evidence

## §1 — Primary suite (T03.16)

Command:

```
uv run pytest tests/cli/eval/test_parallel_15.py -v
```

Raw output: `../../evidence/T03.16/pytest-parallel-15.txt`

Summary:

```
============================== 7 passed in 2.21s ===============================
```

| Test | Result | AC coverage |
|---|---|---|
| `TestParallel15::test_runs_fifteen_evals_at_parallel_eight_exits_clean` | PASSED | AC1: 15 PASS at `--parallel 8`, exit clean |
| `TestParallel15::test_each_eval_receives_unique_home_path` | PASSED | AC2: unique HOME per eval |
| `TestParallel15::test_each_eval_receives_unique_session_id` | PASSED | AC2: unique `CLAUDE_SESSION_ID` per eval (record + JSONL + env) |
| `TestParallel15::test_each_eval_has_isolated_telemetry_namespace` | PASSED | AC2: unique + contained telemetry namespace per eval |
| `TestParallel15::test_per_eval_jsonl_contents_are_self_consistent` | PASSED | AC2: no JSONL cross-talk |
| `TestParallelClampAtFifteen::test_parallel_sixteen_clamps_to_fifteen` | PASSED | AC3: `parallel=16` clamps to 15 |
| `TestParallelClampAtFifteen::test_parallel_at_max_admits_fifteen_concurrent_workers` | PASSED | AC3: clamp is exact at 15, not over-restrictive |

## §2 — Regression (orchestrator + isolation)

Command:

```
uv run pytest tests/cli/eval/test_orchestrator.py tests/cli/eval/test_home_isolation.py -v
```

Summary:

```
============================== 47 passed in 0.50s ==============================
```

No regressions in:
- `tests/cli/eval/test_orchestrator.py` — 20/20 (T03.15)
- `tests/cli/eval/test_home_isolation.py` — 27/27 (T02.11)

## §3 — Combined (regression + new)

Raw output: `../../evidence/T03.16/pytest-regression.txt`

```
============================== 54 passed in 2.58s ==============================
```

## §4 — Acceptance Criteria Closure

| AC | Status | Evidence |
|---|---|---|
| File `tests/cli/eval/test_parallel_15.py` runs a 15-eval fixture suite at `--parallel 8` and exits 0 | ✅ | §1 row 1 |
| Each eval receives its own HOME, session_id, and telemetry namespace (verified by per-eval JSONL inspection) | ✅ | §1 rows 2–5 |
| `parallel=16` clamps to 15; recorded in test assertions | ✅ | §1 row 6 |
| `TASKLIST_ROOT/artifacts/D-0058/spec.md` documents the integration scenario | ✅ | `spec.md` |

## §5 — File manifest

```
tests/cli/eval/test_parallel_15.py                        — new, ~430 LOC, 7 tests
.dev/releases/current/cliEval/artifacts/D-0058/spec.md    — integration scenario
.dev/releases/current/cliEval/artifacts/D-0058/notes.md   — design notes
.dev/releases/current/cliEval/artifacts/D-0058/evidence.md — this file
.dev/releases/current/cliEval/evidence/T03.16/pytest-parallel-15.txt   — raw pytest
.dev/releases/current/cliEval/evidence/T03.16/pytest-regression.txt    — raw regression
```
