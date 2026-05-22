# D-0060 — NFR-PERF4 Disk Budget Poller

**Task:** T03.19 (Phase 3, Roadmap R-060)
**Modules:** `src/superclaude/cli/eval/disk_budget.py` (new), `src/superclaude/cli/eval/orchestrator.py` (integration)
**Tests:** `tests/cli/eval/test_disk_budget.py`
**Status:** Implemented 2026-05-20

## 1. Goal

Bound the cumulative artifact size under `--output-dir` during a real
eval run so a runaway suite cannot fill the host disk. The cliEval
design-spec §4 / §13 (NFR-PERF4) commit the orchestrator to a five-
second polling cadence and a default 1024 MB budget; design-spec §10
risk R4 documents the failure mode the poller mitigates (a 15-eval
fan-out with PTY transcripts can grow past several hundred megabytes
on a slow eval and corrupt every neighbouring run).

On breach the harness must:

1. Stop scheduling new evals.
2. Allow in-flight evals to complete (no thread-kill).
3. Exit `2` (harness error) with a `disk_budget_exceeded.json` side-car
   the Reporter surfaces under `RunSummary.artifacts`.

## 2. Public Surface

```python
from superclaude.cli.eval.disk_budget import (
    DEFAULT_DISK_BUDGET_MB,             # 1024
    DEFAULT_DISK_POLL_TICK_SEC,         # 5.0
    DISK_BUDGET_EXCEEDED_ARTIFACT_NAME, # "disk_budget_exceeded.json"
    DISK_BUDGET_EXCEEDED_EXIT_CODE,     # 2
    DISK_BUDGET_EXCEEDED_REASON,        # "disk_budget_exceeded"
    BreachDetail,
    DiskBudgetPoller,
)
```

### 2.1 `DiskBudgetPoller`

| Attribute / method | Contract |
|---|---|
| `__init__(output_dir, *, max_disk_mb=1024, tick_sec=5.0, artifact_name=..., ensure_output_dir=False, clock=None)` | Construct the poller. `max_disk_mb < 0` → `ValueError`; non-`int` (or `bool`) → `TypeError`; `tick_sec ≤ 0` → `ValueError`. |
| `enabled` | `True` when `max_disk_mb > 0`. |
| `max_disk_mb`, `budget_bytes`, `tick_sec`, `output_dir`, `artifact_name` | Read-only configuration accessors. |
| `is_breached()` | One-shot flag flipped by the polling thread on the first breach. Stays `True` for the lifetime of the poller. |
| `breach_detail()` | `Mapping[str, object]` matching `BreachDetail.to_dict()`, or `None` while healthy. |
| `artifact_path()` | `Path` of the side-car file once written, or `None`. |
| `start()` | Spawn the background daemon thread. No-op when `max_disk_mb == 0` or the thread is already alive. |
| `stop(*, timeout=None)` | Signal the thread to exit and `join` it. Idempotent. Does **not** clear the breach flag. |
| `__enter__` / `__exit__` | Convenience context-manager form (`start` on enter, `stop` on exit). |

### 2.2 `BreachDetail`

Frozen dataclass serialised verbatim into the side-car JSON:

| Field | Type | Notes |
|---|---|---|
| `reason` | `str` | Always `DISK_BUDGET_EXCEEDED_REASON`. |
| `output_dir` | `str` | Absolute path of the watched directory. |
| `usage_bytes` | `int` | Measured cumulative size at the breach tick. |
| `budget_bytes` | `int` | `max_disk_mb * 1024 * 1024`. |
| `max_disk_mb` | `int` | Operator-configured budget. |
| `ticked_at` | `str` | ISO-8601 UTC (`Z`-suffixed) timestamp. |

### 2.3 Side-car shape

Written to `output_dir / DISK_BUDGET_EXCEEDED_ARTIFACT_NAME`:

```json
{
  "budget_bytes": 1073741824,
  "max_disk_mb": 1024,
  "output_dir": "/tmp/run-xyz",
  "reason": "disk_budget_exceeded",
  "ticked_at": "2026-05-20T13:28:09Z",
  "usage_bytes": 1099773888
}
```

`json.dumps(..., indent=2, sort_keys=True)` plus a trailing newline so
the file is review-friendly and round-trips through `jq`. The Reporter
(COMP-008) surfaces the path under
`RunSummary.artifacts["disk_budget_exceeded"]`.

## 3. Polling cadence & breach semantics

```python
while not self._stop_event.wait(self._tick_sec):
    usage_bytes = self._compute_usage()
    if usage_bytes > self._budget_bytes:
        self._record_breach(usage_bytes)
        return
```

* `threading.Event.wait(tick_sec)` is the cancellable sleep — `stop()`
  short-circuits the next tick instead of waiting up to `tick_sec` for
  the loop to notice.
* First tick fires *after* the initial sleep so an empty run directory
  does not trip the breach during start-up.
* `_compute_usage` walks the output tree with `rglob('*')`, skips
  symlinks (cannot be tricked into double-counting via a sibling-tree
  link), and swallows `OSError` / `FileNotFoundError` (in-flight
  runners reaping scratch files between `rglob` and `stat` must not
  crash the poller).
* On breach the poller writes the side-car, **publishes
  `_detail` / `_artifact_path`, and only then sets `_breach_event`**
  — release-then-set ordering so any consumer that observes
  `is_breached() is True` is guaranteed a non-`None` `breach_detail()`
  without explicit locking.
* The breach flag is one-shot. Once set, deleting the offending
  payload does not clear it; the orchestrator sees a stable signal
  for the rest of the run.

`max_disk_mb == 0` disables the poller entirely: `start()` is a no-op,
no thread is spawned, `is_breached()` always returns `False`. Design-
spec §4 documents this as the "disable the budget" invocation.

## 4. Orchestrator Integration

`RunOrchestrator.__init__` accepts `disk_budget_poller:
Optional[DiskBudgetPoller] = None`. When wired:

```python
poller = self._disk_budget_poller
if poller is not None:
    poller.start()
try:
    with ThreadPoolExecutor(...) as pool:
        for index, spec in enumerate(specs):
            if self._is_cancelled():
                cancelled_indices.append(index)
                continue
            if self._is_disk_budget_exceeded():
                disk_budget_skipped_indices.append(index)
                continue
            futures[pool.submit(self._invoke_worker, spec)] = index
        for future in as_completed(futures):
            ...
finally:
    if poller is not None:
        poller.stop()

for index in cancelled_indices:
    outcomes[index] = self._interrupted_outcome(specs[index])
for index in disk_budget_skipped_indices:
    outcomes[index] = self._disk_budget_skipped_outcome(specs[index])
```

The synthesised SKIPPED outcome carries:

| Field | Value |
|---|---|
| `status` | `"SKIPPED"` |
| `skip_reason` | `DISK_BUDGET_EXCEEDED_REASON` (`"disk_budget_exceeded"`) |
| `skip_flag_triggered` | `"--max-disk-mb"` |
| `expects` | `()` |
| `artifacts` | `{}` |
| `duration_sec` | `0.0` |

Priority: cancellation dominates a disk-budget breach when both fire
in the same submission iteration (operator intent overrides a
resource limit). Test:
`TestOrchestratorIntegration::test_cancellation_takes_priority_over_disk_breach`.

In-flight workers run to completion. The orchestrator never kills a
worker thread — `as_completed` still drains the pool before `stop()`
joins the poller. Test:
`TestOrchestratorIntegration::test_inflight_workers_complete_after_breach`.

## 5. Out of Scope

* **CLI flag wiring.** The Phase 4 dispatcher binds `--max-disk-mb`
  to the constructor and maps `DISK_BUDGET_EXCEEDED_EXIT_CODE = 2`
  to the process exit status. This deliverable owns the primitive,
  not the dispatch.
* **Reporter side-car surfacing.** COMP-008 / T03.13 read
  `output_dir / DISK_BUDGET_EXCEEDED_ARTIFACT_NAME` and stamp the
  path into `RunSummary.artifacts["disk_budget_exceeded"]`. The
  poller only writes the file; it does not mutate the summary.
* **Disk-space pre-flight checks.** The doctor command may grow a
  pre-flight that warns when free space is low, but that lives
  outside the polling loop.
* **Per-eval scratch teardown after breach.** Workers continue to
  use the HOME they already own; the harness does not reclaim disk
  proactively on breach.

## 6. Failure Modes & Containment

| Mode | Behaviour |
|---|---|
| `max_disk_mb < 0` | `ValueError` from `__init__`. |
| `max_disk_mb` not `int` (or `bool`) | `TypeError`. |
| `tick_sec ≤ 0` | `ValueError`. |
| `artifact_name == ""` | `ValueError`. |
| `output_dir` does not exist | `_compute_usage` returns `0`; no breach. The poller silently waits until the orchestrator creates the directory. |
| Filesystem unavailable on breach (write fails) | In-memory `BreachDetail` still published, `is_breached()` still flips, `artifact_path()` returns `None`. The orchestrator still aborts scheduling. |
| Symlink under output dir | Skipped — counted as `0` bytes. |
| File reaped between `rglob` and `stat` | `OSError` / `FileNotFoundError` swallowed; next tick re-measures. |
| Poller wired but `max_disk_mb == 0` | `start()` is no-op; `is_breached()` never fires; orchestrator behaves as if no poller were wired. |
| `stop()` called before `start()` | No-op; idempotent. |
| Cancellation + breach in same iteration | Cancellation wins; spec routed to `INTERRUPTED`, not `SKIPPED`. |

## 7. Acceptance Criteria → Test Mapping

| AC | Test |
|---|---|
| Default budget 1024 MB, default tick 5 s. | `TestPublicConstants::test_default_budget_is_1024_mb`, `TestPublicConstants::test_default_tick_is_5_seconds`, `TestDefaults::test_default_budget_uses_module_constant`, `TestDefaults::test_default_tick_uses_module_constant` |
| Breach triggers when usage exceeds budget. | `TestBreachDetection::test_breach_triggers_when_usage_exceeds_budget` |
| Side-car `disk_budget_exceeded.json` written with structured payload. | `TestBreachDetection::test_breach_writes_side_car_with_payload`, `TestBreachDetection::test_breach_detail_matches_side_car` |
| Exit code 2 reserved. | `TestPublicConstants::test_breach_exit_code_is_2` |
| Orchestrator stops scheduling on breach. | `TestOrchestratorIntegration::test_breach_stops_scheduling_but_preserves_outcome_per_spec` |
| In-flight evals complete after breach. | `TestOrchestratorIntegration::test_inflight_workers_complete_after_breach` |
| `--max-disk-mb 0` disables poller; no breach even when usage is large. | `TestDefaults::test_disabled_when_budget_zero`, `TestDisabledPoller::test_start_is_noop_when_disabled`, `TestDisabledPoller::test_breach_does_not_fire_when_disabled`, `TestOrchestratorIntegration::test_disabled_poller_does_not_change_behavior` |
| Breach state is one-shot (cleanup does not clear). | `TestBreachDetection::test_breach_is_one_shot` |
| Symlinks not double-counted. | `TestSymlinkHandling::test_symlinks_are_skipped` |
| SKIPPED outcomes carry the pinned `skip_reason` and `skip_flag_triggered`. | `TestPublicConstants::test_reason_token_is_pinned`, `TestOrchestratorIntegration::test_breach_stops_scheduling_but_preserves_outcome_per_spec` |
| Outcome order preserved despite SKIPPED backfills. | `TestOrchestratorIntegration::test_breach_outcome_order_matches_input_order` |
| Cancellation dominates breach. | `TestOrchestratorIntegration::test_cancellation_takes_priority_over_disk_breach` |
| Constructor guards (negative, non-int, zero tick, empty artifact name). | `TestConstructorGuards::*` (6 tests) |
| Poller thread joined on orchestrator exit. | `TestOrchestratorIntegration::test_breach_stops_poller_on_orchestrator_exit` |

See `evidence.md` for the recorded pytest output.

## 8. References

* Design-spec sources: `.dev/releases/current/cliEval/design-spec.md` §4
  (`--max-disk-mb` CLI flag), §10 (R4 risk row), §13 (NFR-PERF4
  polling cadence).
* Roadmap row: R-060.
* Upstream contracts: D-0057 (RunOrchestrator scheduling skeleton),
  D-0050 (cancellation token + INTERRUPTED outcome shape).
* Downstream consumers: T03.13 / COMP-008 Reporter
  (`RunSummary.artifacts["disk_budget_exceeded"]`), Phase 4 CLI
  dispatcher (`--max-disk-mb` flag, exit-code 2 translation).
