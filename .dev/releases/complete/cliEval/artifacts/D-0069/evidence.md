# D-0069 — Evidence

## Acceptance criteria coverage

| AC | How verified | Evidence link |
|---|---|---|
| `Expect.stderr` and `Expect.stdout` return ExpectCallables producing ExpectResult; both operate on ANSI-stripped buffers. | `test_stdout_strips_ansi_csi_before_match`, `test_stderr_strips_ansi_osc_before_match`, `test_stdout_not_contains_after_ansi_strip` (23-case suite). | `evidence/T04.07/pytest-output.txt` |
| `not_contains` returns passed=True when the pattern is absent from the buffer. | `test_stdout_not_contains_passes_when_absent`, `test_stderr_not_contains_passes_when_absent`. | `evidence/T04.07/pytest-output.txt` |
| `tests/cli/eval/test_expect_stdio.py` covers `contains`, `regex`, `not_contains` for both primitives. | All 23 tests pass; full coverage matrix in `D-0069/spec.md` §"Test matrix". | `evidence/T04.07/pytest-output.txt` |
| `D-0069/spec.md` documents ANSI-strip dependency. | See `D-0069/spec.md` §"ANSI-strip dependency (COMP-011 / T02.17)". | `artifacts/D-0069/spec.md` |

## Test run

```text
$ uv run pytest tests/cli/eval/test_expect_stdio.py -v
============================== 23 passed in 0.17s ==============================
```

Full output (run on 2026-05-20): `evidence/T04.07/pytest-output.txt`.

## Files changed / added

| Path | Change |
|---|---|
| `tests/cli/eval/test_expect_stdio.py` | **NEW** — 23-case acceptance harness for `Expect.stdout` / `Expect.stderr`. |
| `.dev/releases/current/cliEval/artifacts/D-0069/spec.md` | **NEW** — primitive signatures, ANSI-strip contract, evaluation order, test matrix. |
| `.dev/releases/current/cliEval/artifacts/D-0069/notes.md` | **NEW** — implementation decisions, deferred followups. |
| `.dev/releases/current/cliEval/artifacts/D-0069/evidence.md` | **NEW** — this file. |
| `.dev/releases/current/cliEval/evidence/T04.07/pytest-output.txt` | **NEW** — verbatim pytest run. |

`src/superclaude/cli/eval/expect.py` was **not** modified — the
primitive bodies landed in T04.01. T04.07 is a per-primitive acceptance
harness on top of the already-shipped engine.

## Linked roadmap

* Deliverable: D-0069
* Task: T04.07
* Roadmap item: R-069 (COMP-010.5)
* Dependencies: T04.01 (D-0064), T02.17 (D-0037)
* Downstream consumers: T05.02 (E1), T05.04 (E3), T05.06..T05.16
  (E5..E15), T04.17 (TEST-007).
