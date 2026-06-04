---
proposal_id: C
persona: devops
model: haiku
stance: event-driven-decoupled
---

# Proposal C — Event-Driven Worker Pool, Loose Coupling, Defer-Then-Continue Gate

## T1 — Integration boundary

**Choice: Hybrid Option B + Option C.** Keep the existing `execution-log.jsonl` `phase_complete` event as the SoT signal. Inside executor.py, spawn a long-lived `ReflectWorker` (one per sprint) at sprint start that *consumes* `phase_complete` events from a `multiprocessing.Queue` populated by the existing `logger.write_phase_*` calls. The worker spawns one `claude --print "/sc:reflect ..."` subprocess per consumed event and writes reports back to disk. The executor itself is unchanged except for two new lines: queue init at sprint start and queue.put(phase) after `notify_phase_complete`.

**Rationale**: minimizes coupling. The worker is a single, self-contained module; the executor's phase-loop stays clean. Easier to test in isolation. Matches the manual operator pattern (an external consumer of `execution-log.jsonl`) but bundles the consumer into the sprint process so there's no second terminal.

**Rejected**:
- Pure Option A — heavy executor coupling.
- Pure Option C — keeps the second-terminal pain.
- Option D — wrong grain.

## T2 — Gate semantics

**Choice: Option D (configurable) with `--reflect-mode {none|sidecar|defer-then-halt-on-regression}` as the three supported v1 modes.** Default `sidecar`.

The interesting middle ground is **defer-then-halt-on-regression**: phase N+1 starts immediately (no wait), but if reflect-N produces `regression_present=true` while phase N+1 is mid-flight, the executor cleanly halts phase N+1 *between tasks* (not mid-task), surfaces the regression, and asks the operator to continue/abort. This trades a small amount of wasted phase-N+1 work for the safety floor without the cost of always-waiting.

**Rejected**:
- Pure Option B (always halt) — too aggressive without empirical FPR data.
- Pure Option A (sidecar only) — leaves the safety floor on the table.
- `strict` mode — wait for v2 once data exists.

## T3 — Tier/depth selection

**Choice: Auto-routing via sc-reflect's §5.3 rubric (T1 vs T2) but with `--depth deep` always.** Same as Proposal A on the auto-rubric, but matches Proposal B's deep-depth-always. Rationale: depth controls *thoroughness within a tier*; tier controls *which agents run*. The rubric is well-tuned for tier selection; we shouldn't second-guess it. Depth is operator-visible and the operator asked for deep.

**Cost envelope**: 9 phases × rubric-mixed × deep ≈ 200-350k tokens per sprint. Mid-range between Proposal A and B.

## T4 — Parallelism details

- **Result surfacing**: the `ReflectWorker` writes reports to disk and emits its own `reflect_complete` jsonl event with `{phase, status, report_path, regression_present, calibrated_confidence}`. The executor's existing event-tail consumer surfaces this event in TUI and consults `regression_present` at task boundaries.
- **Race condition**: explicit two-snapshot strategy. (a) commit-pinning preferred (via `git stash create` if no auto-commit); (b) for non-git working sets, `cp -r --reflink=auto <results_dir> <results_dir>/.reflect/snapshots/phase-N/` for COW snapshot. Reflect reads from the snapshot path, never working-tree.
- **Token budget envelope**: `ReflectWorker` enforces budget via passing `--budget-remaining` per call and tracking cumulative consumption from sc-reflect's emitted `metrics.json`. When 100% consumed, worker stops spawning new reflects (subsequent events are dropped with WARN logged).
- **Cleanup**: worker is a daemon process; sprint's `signal_handler` joins worker with timeout, then kills if necessary. All subprocess Popens tracked in worker for transitive cleanup.

## T5 — Sc-reflect features leveraged

- **§14.5 Wave 7 promotion** — consumed by worker → `regression_present` propagation.
- **§4.1c auto-wire** — auto via `.roadmap-state.json`.
- **§15.1 metrics + runs.jsonl** — primary consumer for budget tracking and end-of-sprint aggregation.
- **§11.5 sampled citation budget** — auto.
- **§11.3 calibrator disjoint-set** — auto.
- **§4 Wave 0 budget pre-flight** — passed per-phase budget envelope.

## T6 — Migration path

1. **v1** — flag `--reflect post|none` (binary, simple). `--reflect post` enables sidecar by default; `--reflect-mode` flag for advanced selection. Default off.
2. **v1.1** — add `--reflect-mode defer-then-halt-on-regression`; recommend in docs.
3. **v1.2** — change default to `--reflect post` with mode `sidecar`. Telemetry.
4. **v1.3** — change mode default to `defer-then-halt-on-regression` once FPR < 10% confirmed.
5. **v2** — add `strict` mode for release pipelines.
6. **Resume compatibility**: SprintConfig.reflect_mode + SprintConfig.reflect_enabled both persisted to `.roadmap-state.json`.

## T7 — Existing pipeline updates

- **`run_post_phase_wiring_hook`**: keep, orthogonal.
- **`_verify_checkpoints`**: keep, orthogonal (fast mechanical vs slow semantic).
- **`retrospective.py`**: ingest `.dev/reflect/runs.jsonl` + per-phase reports for cross-phase trend section. Lightweight extension (~50 LOC).
- **`monitor.py`/`tui.py`**: new TUI cell per phase showing reflect status + calibrated confidence. Updates via the `reflect_complete` jsonl event tail.
- **`kpi.py`**: surface reflect aggregates (per-phase status, regression count, drift count, budget consumed).
- **`notify.py`**: extend `notify_phase_complete` to also publish to the worker queue. Single-line change.

## Implementation cost

- **Files changed**: new `reflect_worker.py` (~280 LOC for worker + budget + snapshot + queue), executor.py (+~30 LOC for worker lifecycle), notify.py (+~10 LOC for queue.put), config.py (+~15 LOC), CLI (+~25 LOC), retrospective.py (+~50 LOC), kpi.py (+~40 LOC), tui.py (+~30 LOC), tests (~450 LOC).
- **LOC delta**: ~930 LOC including tests.
- **Dependencies**: none new (stdlib `multiprocessing.Queue` + `subprocess`).
- **Dev hours**: 18-24h including tests.

## Risks

- `multiprocessing.Queue` adds inter-process complexity for what could be in-process. Mitigation: use `queue.Queue` + thread instead of `multiprocessing` if the worker doesn't need a separate process; subprocess.Popen already gives us process isolation for the actual `claude` invocation.
- Worker crash leaves orphan reports. Mitigation: worker writes a sentinel `phase-N.in-progress` file at spawn-time and removes it at completion; on sprint restart, sentinel cleanup is a startup task.
- Snapshot disk usage. Mitigation: cleanup snapshot after report written + 1 phase grace period.

## Why hybrid

Proposal A's pure-executor-spawn couples reflect lifecycle to executor; Proposal B's strict-gate is too aggressive for v1. A worker-pool decoupling is the standard pattern for "do this side-work in parallel without slowing down the main loop", lets us scale to multi-sprint scenarios later, and matches the operator's existing mental model (consumer of `execution-log.jsonl`).
