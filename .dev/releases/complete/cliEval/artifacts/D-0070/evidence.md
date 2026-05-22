# D-0070 — Evidence

## Acceptance criteria coverage

| AC | How verified | Evidence link |
|---|---|---|
| `Expect.duration(max_sec, min_sec)` returns an ExpectCallable producing ExpectResult. | All 19 tests instantiate the callable and assert `isinstance(result, ExpectResult)` / `result.name == "duration"`. | `evidence/T04.08/pytest-output.txt` |
| When only one bound is set, the primitive records duration informationally even if the (missing) other bound would have failed. | `test_duration_max_only_does_not_fail_on_missing_min_bound` (0.0s vs `max_sec=5`) and `test_duration_min_only_does_not_fail_on_missing_max_bound` (10000s vs `min_sec=1`) both PASS. | `evidence/T04.08/pytest-output.txt` |
| `tests/cli/eval/test_expect_duration.py` covers max-only, min-only, both, and neither cases. | Test matrix in `D-0070/spec.md` enumerates: no bounds (#1, #2), `max_sec` only (#3-#5), `min_sec` only (#6-#8), both (#9-#12), single-bound informational (#13-#14), declarative (#15-#17), envelope (#18-#19). | `artifacts/D-0070/spec.md` §"Test matrix" |
| `D-0070/spec.md` documents informational-PASS semantics. | See `D-0070/spec.md` §"Informational-PASS semantics". | `artifacts/D-0070/spec.md` |

## Validation example (from phase-4-tasklist.md)

The task validation step calls for:

* `Expect.duration(max_sec=3)` against `duration_sec=5` → **FAIL**
  → Covered by `test_duration_max_sec_fails_when_over_budget`.
* `Expect.duration(min_sec=2)` against `duration_sec=5` → **PASS**
  → Covered by `test_duration_min_sec_passes_when_above_floor`.

Both tests pass; see `evidence/T04.08/pytest-output.txt`.

## Test run

```text
$ uv run pytest tests/cli/eval/test_expect_duration.py -v
============================== 19 passed in 0.19s ==============================
```

Full output (run on 2026-05-21): `evidence/T04.08/pytest-output.txt`.

## Files changed / added

| Path | Change |
|---|---|
| `tests/cli/eval/test_expect_duration.py` | Pre-existing 19-case acceptance harness for `Expect.duration` (landed alongside T04.01 / D-0064). |
| `.dev/releases/current/cliEval/artifacts/D-0070/spec.md` | **NEW** — primitive signature, behaviour matrix, informational-PASS semantics, test matrix. |
| `.dev/releases/current/cliEval/artifacts/D-0070/notes.md` | **NEW** — implementation decisions, deferred followups. |
| `.dev/releases/current/cliEval/artifacts/D-0070/evidence.md` | **NEW** — this file. |
| `.dev/releases/current/cliEval/evidence/T04.08/pytest-output.txt` | **NEW** — verbatim pytest run. |

`src/superclaude/cli/eval/expect.py` was **not** modified — the
primitive body landed in T04.01. T04.08 is a per-primitive acceptance
harness on top of the already-shipped engine.

## Linked roadmap

* Deliverable: D-0070
* Task: T04.08
* Roadmap item: R-070 (COMP-010.6)
* Dependencies: T04.01 (D-0064)
* Downstream consumers: T05.x manifests; benchmarking dashboard (post-M5).
