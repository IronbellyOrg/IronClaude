# Code Review: snapshot src/superclaude/cli/eval/

**Target**: snapshot `src/superclaude/cli/eval/` (sourced from `origin/cliEval`, the head of open PR #66)
**Reviewer**: `/sc:auggie-review` (depth=quick, focus=anti-patterns, architecture, quality)
**Generated**: 2026-05-21 03:55 UTC
**Source PR**: #66 (in-tree but not yet merged at review time)
**Base ↔ Head**: snapshot mode — no diff baseline
**Stats**: 29 files, ~10,746 Python LOC, 17 candidate findings emitted by Auggie → 14 dropped during grounding → **3 surviving findings** (0 Critical, 0 High, 2 Medium, 1 Low, 0 Nit)

---

## Summary

This review is **partial / inconclusive on the line-grounded layer**. Auggie's quick pass surfaced 14 single-file findings and 3 cross-cutting observations, but **every one of the 14 single-file findings cited a line number that landed in a docstring, an `__all__` entry, an import block, or an unrelated section** of the cited file — i.e. the file:line citations were decorative rather than evidence-bearing. The hallucination contract requires those findings be dropped, not downgraded.

After grounding, the only durable signal from the pass is a pair of size-based anti-pattern observations and one no-op except handler. There are **no Critical or High findings**. The directory is in noticeably better shape than Auggie's raw output suggests:

- PTY lifecycle (`pty_driver.py`) has explicit `__exit__` → `terminate()` → `close()` chaining with a force-close fallback for leaked fds (lines 195-200, 396-409). Auggie's "PTY fd leak" finding was outright refuted.
- Concurrency primitives in `signal_handler.py` use `threading.Event` + `threading.Lock` (the `CancellationToken` class, line 55+), not the unsynchronized global flag Auggie alleged.
- Path construction is already centralized in `artifact_layout.py` (`compose_run_dir`, `compose_per_eval_dir`) — Auggie's "copy-pasted in reporter/coverage/run_report" claim was refuted.
- `disk_budget.py` exposes a typed `@dataclass(frozen=True) BreachDetail` (line 161), refuting the primitive-obsession claim.
- Schema validation tests (`test_schema_load.py`, `test_schema_validate.py`) and integration tests (`test_pty_lifecycle.py`, `test_signal_handling.py`, `test_orchestrator.py`, `test_claude_process_adapter.py`) all exist on `origin/cliEval` — Auggie's "no integration tests" cross-cutting was refuted.

**Recommendation: Approve with comments.** The two anti-pattern findings (oversized `run()` and `EvalRunner`) are real but not blocking; the no-op except is a one-line cleanup. **Caveat**: this is a `quick`-depth pass with high Auggie-citation drop-rate. A **`standard` or `deep` re-run is recommended** before treating the absence of Critical/High findings as a clean bill of health — Auggie's behavior on this run suggests its index may have been working off stale/cached references rather than the actual `origin/cliEval` content.

## Findings

### 🔴 Critical (block merge)

_None._

### 🟠 High (should fix before merge)

_None._

### 🟡 Medium (fix in this PR if cheap, otherwise file follow-up)

#### M1. `RunOrchestrator.run()` is a 145-line method straddling scheduling, cancellation, disk-budget gating, and result backfill

- **File**: `src/superclaude/cli/eval/orchestrator.py:147-291`
- **Category**: anti-pattern (long function)
- **Source**: auggie (regrounded) + claude
- **Evidence**: `def run(...)` opens at line 147 and the next sibling method `_invoke_worker` opens at line 292 — the body spans 145 lines.
- **Why this matters**: The body interleaves five concerns (concurrency clamping, `outcomes` slot pre-allocation, cancellation-index bookkeeping, disk-budget-skipped-index bookkeeping, the ThreadPoolExecutor + `as_completed` loop with its nested `BaseException` translation, and the post-finally backfill loops). Each is well-commented in isolation, but the combined method body is past the "easy to hold in working memory while reading" threshold (~80-100 lines for a complex coordinator). Future changes to any single concern (e.g. adding a second budget poller, a different cancellation source, or an additional skipped-status) will need to thread through the same body and tend to grow it further.
- **Recommendation**: Extract the per-concern blocks into private helpers — at minimum (a) `_init_outcome_slots(specs)`, (b) `_drain_futures(futures, outcomes, ...)`, and (c) `_backfill_synthetic_outcomes(outcomes, cancelled_indices, disk_budget_skipped_indices, specs)`. The public `run()` then reads as ~30-40 lines of orchestration glue and each helper can be unit-tested in isolation.

#### M2. `EvalRunner` is a 535-line class with 9 methods spanning lifecycle, logging, home-proxying, and executor wiring

- **File**: `src/superclaude/cli/eval/runner.py:702-1237`
- **Category**: anti-pattern (god class)
- **Source**: auggie (regrounded) + claude
- **Evidence**: `class EvalRunner` opens at line 702 and the file ends at line 1237 — the class body is the final 535 lines of the module. The same module already factors out `_LifecycleState` (line 372), `_LogEvent` (501), `_JsonlLog` (529), `_LoggingHomeProxy` (581), `_LoggingExecutor` (636) — and yet `EvalRunner` still owns setup, teardown, observe, the executor protocol implementation, and the JSONL event-emission surface.
- **Why this matters**: The module is the eval-run "engine" and is the single class most likely to grow with each new lifecycle hook (retry, metrics, partial-summary, capability-gate side-effects). Each addition compounds the cognitive load. The fact that the module already has five private helper classes suggests the seam is recognized — but `EvalRunner` itself wasn't pulled apart along the same lines.
- **Recommendation**: Split `EvalRunner` along its already-named axes — at minimum (a) `_EvalLifecycle` (setup/teardown/observe) which receives the home-proxy by composition, and (b) keep `EvalRunner` as a thin coordinator that holds the lifecycle, the executor protocol target, and the JSONL log. This makes the test surface in `tests/cli/eval/test_runner_class.py` decomposable too.

### 🟢 Low (nice-to-have)

#### L1. `try/except BaseException: raise` no-op handler

- **File**: `src/superclaude/cli/eval/runner.py:596-605`
- **Category**: dead-code (no-op exception handler)
- **Source**: claude (regrounded from auggie F4)
- **Evidence**:
  ```python
  self._log.emit(EvalRunner.EVENT_SETUP_STARTED, step="setup")
  try:
      home_path = self._home.setup(config=config)
  except BaseException:
      raise
  self._log.emit(
      EvalRunner.EVENT_SETUP_COMPLETED,
      ...
  )
  ```
- **Why this matters**: The `try/except BaseException: raise` is structurally a no-op — it has no `else`, no `finally`, and the `except` body does nothing but re-raise. The only behavioural difference from removing the try/except entirely is a slightly different traceback shape. The pattern reads as "we intended to do something here and forgot" or "we used to catch and log and removed the log but left the try". Compare with the structurally-correct sibling `teardown` method (lines 607-635), which does emit a `EVENT_TEARDOWN_ERROR` before re-raising.
- **Recommendation**: Either (a) drop the try/except entirely if no error-path logging is intended, or (b) mirror `teardown`'s pattern and emit an `EVENT_SETUP_ERROR` before `raise`. The latter is probably what was intended — a setup failure should be observable in the same JSONL log that emits `EVENT_SETUP_STARTED`/`EVENT_SETUP_COMPLETED`, otherwise an external watcher sees `STARTED` with no terminal event.

### 💬 Nits

_None._

## Architectural / Cross-Cutting Observations

_None survived grounding._ The three cross-cutting observations Auggie emitted (naming inconsistency, missing integration tests, missing schema-sync tests) were each refuted by direct inspection — all classes are PascalCase, 74 test files exist under `tests/cli/eval/` on `origin/cliEval` (including `test_pty_lifecycle.py`, `test_signal_handling.py`, `test_orchestrator.py`, `test_claude_process_adapter.py`, `test_schema_load.py`, `test_schema_validate.py`), and models use `@dataclass(frozen=True)` rather than Pydantic so the suggested `parse_obj` schema-sync recipe was inapplicable.

### Meta-observation (not a finding, for the orchestrator's audit trail)

The single observable signal worth surfacing at the **review-process level** (rather than the code level) is that this Auggie pass had a **14-of-14 file:line miscitation rate** on single-file findings. Possible causes:

1. The reviewed code lived on a non-current branch (`origin/cliEval`) when the workspace-root index was last refreshed — Auggie may have been answering from a partially-indexed state.
2. The `quick` budget (`--max-turns 8`) may have prompted Auggie to emit findings from cached high-level summaries rather than from fresh per-file reads.
3. Auggie's general tendency to produce plausible-looking-but-decorative line numbers when not explicitly prompted to read-and-verify the cited line.

This is reported here so a future re-run knows to (a) bump depth to `standard` or `deep` for this module, (b) re-index the workspace before invoking, and (c) trust the rubric's grounding step rather than Auggie's `severity_hint`.

## Audit

- Auggie chunks: 1 (succeeded after one retry; first attempt failed with `augmentTooLarge` due to inline 29-file listing in the prompt — second attempt removed the listing and let Auggie's indexed retrieval enumerate).
- Findings emitted by Auggie: 14 single-file + 3 cross-cutting = **17**.
- Findings dropped during grounding: **14 single-file + 3 cross-cutting = 17 emitted citations failed verification**. Two single-file findings were *regrounded* (M1, M2) by locating the actual code the concern targeted, and one new finding (L1) was identified during the regrounding of F4. Net surviving findings: **3** (M1, M2, L1).
- Persona cross-check: disabled (`quick` depth does not spawn the `auggie-reviewer` independent pass).
- Auggie raw response: `auggie-raw-main.json` (19,547 bytes, wrapped envelope with `--max-turns` preamble).
- Auggie parsed response: `auggie-parsed.json` (unwrapped via the documented `tail -n +2 | jq -r .result | sed fence-extract | jq` pipeline).
- Token cost: Auggie ≈ 1 retry × ~99s wall (free retrieval tier). Claude orchestration kept to per-finding `Read`+`grep` validation, no full-file reads beyond the 5 hotspot files.

<!-- SC:AUGGIE-REVIEW:SUMMARY
status: partial
critical: 0 high: 0 medium: 2 low: 1 nit: 0
dropped: 14
auggie_chunks: 1
duration_sec: 99
-->
