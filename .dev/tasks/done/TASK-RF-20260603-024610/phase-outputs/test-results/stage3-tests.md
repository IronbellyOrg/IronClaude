# Stage 3 — Test & Lint Summary (Step 5.12)

**Captured:** 2026-06-03 21:10
**Raw output:** `stage3-tests.txt`
**Command:** `uv run pytest tests/sprint/test_handoff_concurrency.py tests/sprint/test_turn_ledger_concurrency.py tests/sprint/test_handoff_performance.py tests/sprint/test_backward_compat_regression.py tests/sprint/ tests/cli/eval/test_isolation_layers_probe.py tests/integration/test_sprint_wiring.py -q`

## Pytest counts (exact)

| Metric | Count |
|--------|-------|
| Passed | 1068 |
| Failed | 54 |
| Skipped | 0 |
| Warnings | 20 |
| Exit code | 1 |

Summary line: `54 failed, 1068 passed, 20 warnings in 19.68s`

## Lint

`make lint` initially reported **1** error (`I001` import-block-unsorted in
`executor.py`, from the new `from .scheduler import ...`). Fixed with
`ruff check --fix src/superclaude/cli/sprint/executor.py`. Re-run: **PASS**
("All checks passed!"). executor re-verified to import cleanly.

## Regression analysis vs `pre-change-baseline.md` — EXPLICIT, ZERO regressions

The failing node-id set is **IDENTICAL** to the Phase-1 baseline (54 tests),
verified by set diff:

- `comm -23 (stage3 failures) (baseline failures)` → **empty** (no new regressions)
- `comm -13 (stage3 failures) (baseline failures)` → **empty** (none of the 54 newly pass/fail differently)

All 54 are the pre-existing `.stdin` harness-double failures (+ the 6 downstream
`IndexError`) on the Path A single-session fallback — none in the per-task code
this task wired.

Passed count rose 1039 → 1068: the new Stage 0–3 tests (now collected in
`tests/sprint/`) plus 2 obsolete-assumption tests that were correctly updated
this stage (see below).

## Two pre-Stage-3 assumption tests updated (NOT regressions — corrected behavior)

During the full-suite run, 2 existing tests encoding pre-change assumptions
surfaced as failures and were updated to the corrected behavior:

1. `tests/sprint/test_resume_semantics.py::test_resume_command_includes_budget` —
   asserted the resume hint contains `--budget`. Stage 2 (Step 4.4) reconciled
   `build_resume_output` to use `--max-turns` (the REAL turn-budget flag; `--budget`
   is not a `sprint run` option), so the printed command is directly runnable. Test
   updated to assert `--max-turns` present and `--budget` absent. The budget-suggestion
   intent is preserved.
2. `tests/sprint/test_executor.py::test_backward_compat_no_gate_threads_in_executor`
   → renamed `test_backward_compat_no_leaked_daemon_threads_in_executor`. Asserted
   `"threading" not in` the executor source. Stage 3's headline deliverable
   (`--task-parallelism K`) legitimately adds a threading lock + a context-managed
   `ThreadPoolExecutor`. The real invariant is *no leaked daemon threads* — now
   asserted as: no raw `Thread(` / `daemon=True` spawns, and any `ThreadPoolExecutor`
   is context-managed (`with ThreadPoolExecutor`). The runtime no-leak guarantee
   remains enforced by the `threading.active_count()` backward-compat tests.

## New Stage-3 tests (all PASS)

- `test_handoff_concurrency.py` — 1 passed (≥4 threads × 300 = 1200 concurrent
  `_jsonl` writes; exact line count, every line parses, payload multiset intact —
  would fail against the lock-free writer).
- `test_turn_ledger_concurrency.py` — 1 passed (400 concurrent `try_launch` attempts
  on a 20-launch budget → EXACTLY 20 granted; no over-commit).
- `test_handoff_performance.py` — 2 passed ((a) K=4 wall-clock < 0.5× serial with a
  fixed-duration mock; (b) in-flight dependency with no handoff → dependent waits,
  launches strictly after its dependency on resume).

## Verdict

Stage-3 concurrency hardening is green: `_jsonl` + `TurnLedger` are thread-safe,
the atomic `try_launch` prevents budget over-commit, the DAG scheduler orders
waves and detects cycles, `--task-parallelism K>1` delivers the wall-clock win
(<0.5× at K=4) while K=1 stays byte-identical, lint is clean, and the failing-test
set is provably identical to the baseline (ZERO regressions).
