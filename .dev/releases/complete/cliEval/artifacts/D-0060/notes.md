# D-0060 Disk-Budget Poller — Design Notes

Companion to `spec.md`. These notes capture the design decisions made
while implementing T03.19 (NFR-PERF4 disk-budget poller), the
alternatives considered, and the reasoning behind the chosen contract.

## Why a separate breach `Event` instead of reusing `CancellationToken`

The first sketch reused the `CancellationToken` the orchestrator already
threads through `EvalRunner`. That was rejected because the AC requires
"in-flight evals **complete**" — `CancellationToken` propagates to the
in-runner `EvalRunner._cancellation_token` which converts in-flight
work into `INTERRUPTED` outcomes (D-0050). Sharing the token would
truncate the in-flight evals on breach, violating the AC.

A dedicated `threading.Event` on the poller decouples the two signals:

| Signal | Semantics | In-flight outcome shape |
|---|---|---|
| `CancellationToken.is_cancelled()` | Operator pressed Ctrl-C / SIGTERM | `INTERRUPTED` (runner aborts pty wait) |
| `DiskBudgetPoller.is_breached()` | Disk budget exceeded | In-flight workers run to completion (`PASS` / `FAIL` / `TIMEOUT` per normal classification); only unsubmitted specs get `SKIPPED` |

The orchestrator polls both flags, but only the first one propagates
into the worker.

## Why `SKIPPED` for unsubmitted specs (not `INTERRUPTED` / `ERRORED`)

Three statuses were candidates:

1. **`INTERRUPTED`** — semantically wrong: there was no interruption.
   `INTERRUPTED` is reserved for operator-initiated cancellation
   (SIGINT/SIGTERM). Reusing it here would conflate two distinct
   exit paths and prevent the Reporter from distinguishing "user
   aborted" from "harness aborted on resource limit".
2. **`ERRORED`** — close, but `ERRORED` is for harness errors during
   eval execution (D-0049 lifecycle phases). The spec never ran, so
   there was nothing to error on.
3. **`SKIPPED`** — the natural fit. DM-001 already pairs `SKIPPED`
   with `skip_reason` and `skip_flag_triggered`, which are exactly
   the fields needed to surface the disk-budget abort. The Reporter
   can match on `skip_reason == "disk_budget_exceeded"` without
   parsing free-form text, and the `--max-disk-mb` flag is named
   explicitly via `skip_flag_triggered`.

The `DISK_BUDGET_EXCEEDED_REASON` constant pins the token so consumers
do not have to discover it by string-matching.

## Why `threading.Event.wait(tick_sec)` instead of `time.sleep`

`time.sleep` is uninterruptible — `stop()` would have to wait up to
`tick_sec` seconds before the next loop iteration noticed the stop
flag. `Event.wait(tick_sec)` returns immediately when `set()` is
called from another thread, so `stop()` is responsive even with the
5-second production cadence.

The boolean return of `wait` is exploited directly: `while not
self._stop_event.wait(self._tick_sec):` is the cleanest expression of
"sleep `tick_sec`, exit if stop was requested".

## Why release-then-set ordering for breach publication

The reader (orchestrator main thread) calls `is_breached()` and then,
on `True`, may call `breach_detail()`. Without ordering, the reader
could observe the flag without observing the detail.

Pattern:

```python
# In poller thread:
self._detail = detail               # publish first
self._artifact_path = artifact_path
self._breach_event.set()            # then flip the flag

# In orchestrator thread:
if poller.is_breached():            # observe the flag
    detail = poller.breach_detail() # detail is guaranteed populated
```

This is the standard release-store / acquire-load idiom adapted to
Python's `threading.Event` (which uses a `Condition` internally with
the implicit memory barriers of `Lock`). The reader observes the
detail via plain attribute access; the event provides the
synchronisation. No explicit lock is needed in the reader path
because the detail is only ever written once before the flag flips
and is never mutated thereafter.

## Why skip symlinks in the disk walk

Two attack vectors motivated this:

1. **Sibling-tree double-counting.** A symlink under `output_dir`
   pointing at a sibling tree would inflate the usage measurement
   relative to the actual on-disk footprint, triggering false-positive
   breaches.
2. **Cross-mount escape.** A symlink to `/var` (or another large
   filesystem) would let an unrelated file inflate the measurement
   and crash a healthy run.

Skipping symlinks entirely (rather than resolving them and de-
duplicating) is the simplest defensible policy: the poller measures
exactly what is allocated under the output tree, no more and no less.
A test (`TestSymlinkHandling::test_symlinks_are_skipped`) pins the
behaviour against regressions.

## Why swallow per-file `OSError` instead of crashing the poller

Production scenarios that produce transient `OSError` during the walk:

- A runner's scratch HOME is reaped between `rglob` and `stat`.
- The orchestrator deletes a partial artifact during teardown.
- The poller races a `Path.unlink()` from a finishing worker.

A poller that crashes on a transient missing file is worse than no
poller: the orchestrator never sees the breach flag flip and disk
keeps growing. Swallowing the error lets the next tick re-measure
correctly. The trade-off — that a corrupted filesystem returning
`EIO` consistently would silently produce `0`-byte usage — is
documented in the spec failure-mode table.

## Why `max_disk_mb == 0` is the disable sentinel (not `None`)

Three reasons:

1. **CLI ergonomics.** `--max-disk-mb 0` reads as "no budget" in shell
   syntax. `--max-disk-mb=None` is not a thing in Click; using `None`
   would force a separate `--no-disk-budget` flag.
2. **Constant type stability.** `DEFAULT_DISK_BUDGET_MB: int = 1024`
   stays an `int`. A sentinel `None` would force the type to
   `Optional[int]` everywhere and add `None` checks throughout the
   orchestrator.
3. **`start()` no-op idempotency.** The orchestrator can call
   `poller.start()` unconditionally; the disabled poller silently
   declines to spawn a thread. The integration code stays clean of
   conditional branching.

## Why cancellation dominates breach in the submission loop

The submission loop checks cancellation first, then disk budget:

```python
if self._is_cancelled():
    cancelled_indices.append(index)
    continue
if self._is_disk_budget_exceeded():
    disk_budget_skipped_indices.append(index)
    continue
```

If both fire simultaneously (operator presses Ctrl-C while disk is
already over budget), the spec is routed to `INTERRUPTED`. The
rationale is operator-intent precedence: a Ctrl-C is a deliberate
choice to stop, so the outcome should reflect *why the operator
aborted*, not the underlying resource state. The Reporter can still
inspect the side-car JSON to learn that the disk was also breached.

Test: `TestOrchestratorIntegration::test_cancellation_takes_priority_over_disk_breach`.

## Why no `--max-disk-mb` wiring in this deliverable

The poller is the primitive; the CLI flag is the dispatcher's
responsibility (Phase 4). Two reasons for the split:

1. **Scope discipline.** D-0060 owns the polling primitive and the
   orchestrator integration. Flag parsing and exit-code translation
   are CLI-shape concerns that change independently.
2. **Reusability.** A future component (eg. the `doctor` pre-flight,
   T03.06 follow-up) may want the polling primitive without the
   `--max-disk-mb` flag wiring. Keeping the primitive standalone
   makes that re-use trivial.

The `DISK_BUDGET_EXCEEDED_EXIT_CODE` constant lives in `disk_budget`
so the Phase 4 dispatcher has one obvious import target.

## Why a side-car JSON file instead of writing into `summary.json`

`summary.json` (DM-012) is written by the Reporter at the end of the
run from the in-memory `RunSummary`. The poller runs concurrently
with the orchestrator and must record the breach *before* the
Reporter assembles the summary — otherwise a crash between the
breach and the summary write would lose the diagnostic.

The side-car is independent of the Reporter's success and survives
process crash. The Reporter then reads the file at summary-assembly
time and stamps the path into `RunSummary.artifacts["disk_budget_exceeded"]`.

## Reference implementation

- Pattern source: `src/superclaude/cli/eval/orchestrator.py` D-0057
  scheduling loop (same `ThreadPoolExecutor + as_completed` shape
  the integration extends).
- Companion: D-0050 cancellation token + `INTERRUPTED` synthesis
  pattern (mirrored for `SKIPPED` synthesis here).

## Verification evidence

See `evidence.md` in this directory. Summary:

- 33/33 disk-budget tests pass in 1.16s.
- 20/20 D-0057 orchestrator regression tests pass in 0.49s.
- No regressions in the broader suite.
