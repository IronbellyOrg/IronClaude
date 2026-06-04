---
proposal_id: B
persona: analyzer
model: sonnet
stance: strict-gate-asymmetric-cost
---

# Proposal B — Background Subprocess With Regression-Gate, Default-Strict

## T1 — Integration boundary

**Choice: Option B (background subprocess), with a soft-join checkpoint before phase N+1's first task.** Spawn reflect right after `notify_phase_complete()` at executor.py:1605. Phase N+1 starts immediately, but **before phase N+1's first task launches**, the executor checks whether reflect-N has produced its report. If yes, consume it; if no, allow phase N+1 to proceed (reflect-N will land mid-phase-N+1 and either get consumed by the next checkpoint or get archived as a late-arriving sidecar).

**Rejected**:
- Pure Option B (never blocks even at task boundary) — fine for sidecar but inadequate for gate semantics. The checkpoint barely costs anything because reflect-N has had the entire setup phase of N+1 to finish.
- Option A (strict block) — too costly; rejected.
- Option C — manual pattern is what we're replacing.
- Option D (per-task) — UC-2 is designed for milestone-grain, not task-grain.

## T2 — Gate semantics

**Choice: Option B (halt on `regression_present=true`), with the asymmetric-cost argument explicitly invoked.** sc-reflect §10.4 says regression is "the asymmetric-cost case" — letting a regression land in phase N+1 is *strictly worse* than pausing the sprint and asking the operator. Implementation: when reflect-N's report has `regression_present: true` in the deviation taxonomy section, the executor sets `sprint_result.status = PAUSED_REFLECT_REGRESSION` and emits an interactive prompt: "Reflect-N detected regression. Continue / Halt / View report?". Default action on no-reply (e.g., CI mode): halt.

**Configurable via flag** `--reflect-mode {none|sidecar|halt-on-regression|strict}`:
- `none` — disable reflect entirely (back-compat).
- `sidecar` — Option A from T2.
- `halt-on-regression` — default; halts only on regression_present=true.
- `strict` — halts on regression OR drift OR status=partial; only proceeds on status=success.

**Rationale**: The asymmetric cost is real. Drift is recoverable; regression is not. A `strict` mode exists for safety-critical sprints (releases) but the default is `halt-on-regression`.

## T3 — Tier/depth selection

**Choice: T2-deep always, no auto-routing.** The user explicitly said "deep" in the brainstorm topic. The reason to skip sc-reflect's §5.3 rubric is *consistency of signal*: when the operator sees a phase-N report, they want to know it was produced by the same procedure as phase-N-1, not "well, this one was T1 because the rubric said so". Trade off cost for predictability.

**Cost envelope**: 9 phases × T2-deep × ~50k tokens = ~450k tokens per sprint. Recommend a `--reflect-budget <N>` flag that caps total reflect spend; when exhausted, remaining phases force-downgrade to T1-quick with a warning logged.

**Rejected**: Auto-routing (Proposal A's choice) introduces signal-noise — different phases get different audit grades, making cross-phase trends in retrospective.py noisier.

## T4 — Parallelism details

- **Result surfacing**: a small in-memory `ReflectFleetState` updated by a polling thread that checks for `phase-N-report.md` every 2s. The state is queried by the next phase's task loop pre-gate, and by `monitor.py` for TUI display.
- **Race condition**: solved by **commit-pinning**. After `phase_complete`, executor runs `git rev-parse HEAD > .reflect/phase-N.sha` and passes `--commit-range <prev_sha>..<curr_sha>` to reflect. Reflect reads files via `git show <sha>:<path>` not working-tree. Race eliminated. If phases don't commit (no auto-commit hook), executor stages the working-tree to a temporary git index and `git stash create`s a snapshot SHA.
- **Token budget envelope**: `SprintReflectFleet` enforces total budget. When 80% consumed, emit WARN. When 100% consumed, force-downgrade to T1-quick for remaining phases. When 150% consumed (runaway), kill all live reflect Popens and stop spawning new ones.
- **Cleanup**: SIGTERM/SIGINT handler triggers `SprintReflectFleet.terminate_all(wait=5, then_kill=True)`. Atexit handler as belt-and-suspenders.

## T5 — Sc-reflect features leveraged

- **§14.5 Wave 7 promotion mutation** — *critical*: the strict-gate mode relies on `promotion_decision: blocked` propagating up. The integration honors that decision verbatim.
- **§4.1c auto-wire** — auto-applies via `.roadmap-state.json` presence in `<results_dir>`.
- **§15.1 metrics.json + runs.jsonl** — fed into `kpi.py` and `retrospective.py`.
- **§11.5 sampled citation budget** — auto.
- **§11.3 calibrator disjoint-set** — auto.
- **§4 Wave 0 step 0.9 budget pre-flight** — passed `--budget-remaining <per_phase_cap>`.

## T6 — Migration path

1. **v1** — opt-in `--reflect-mode {none|sidecar|halt-on-regression|strict}` flag. Default `none` to preserve back-compat. Document `halt-on-regression` as recommended for new sprints.
2. **v1.1** — change default to `sidecar` (passive, no behavior change but reports flow). Telemetry collection.
3. **v1.2** — change default to `halt-on-regression` once empirical data shows acceptable FPR.
4. **v2** — `strict` mode promoted to default for releases (release-pipeline only); `halt-on-regression` remains default for development.
5. **Resume compatibility**: SprintConfig.reflect_mode persisted to `.roadmap-state.json`; resume() honors the original mode of the sprint.

## T7 — Existing pipeline updates

- **`run_post_phase_wiring_hook`**: keep. Both gates evaluate independently; either can halt independently (analogous to anti-instinct + wiring independence per NFR-010).
- **`_verify_checkpoints`**: **simplify**. Today it checks cp-file existence + non-emptiness. Once reflect UC-2 is in the pipeline at higher grain, the cp-file check becomes a fast sanity gate (still useful for the < 1s feedback) while reflect carries the semantic load. Document the two-layer model.
- **`retrospective.py`**: **major extension**. Read `.dev/reflect/runs.jsonl` cross-sprint aggregator AND per-phase reports. Add new sections: "Calibrated confidence trend", "Regression count by phase", "Deviation taxonomy distribution". Haiku narrative consumes the structured data, not raw reports.
- **`monitor.py`/`tui.py`**: add reflect status column with color coding (green=success, yellow=partial/drift, red=regression). Updates every 2s from `ReflectFleetState`.
- **`kpi.py`**: new fields `reflect_per_phase_status`, `reflect_calibrated_confidence_per_phase`, `reflect_regression_count`, `reflect_drift_count`, `reflect_authorized_expansion_count`, `reflect_budget_consumed`.

## Implementation cost

- **Files changed**: executor.py (+~120 LOC for spawn + gate + soft-join checkpoint), notify.py (+~20 LOC), new reflect_fleet.py (~250 LOC with budget tracking + commit-pinning), config.py SprintConfig (+~20 LOC for mode/budget), CLI entry (+~30 LOC for two new flags), retrospective.py (+~100 LOC for trend analysis), kpi.py (+~50 LOC), monitor.py/tui.py (+~50 LOC), tests (~500 LOC for fleet, gate semantics, budget enforcement, race handling).
- **LOC delta**: ~1140 LOC including tests.
- **Dependencies**: none new.
- **Dev hours**: 22-28h including tests.

## Risks

- Strict-gate false-positives stall the sprint. Mitigation: `halt-on-regression` default (not `strict`); regression detection has high precision per sc-reflect §11.3.
- Commit-pinning fails if phases don't commit and the stash creation races with phase N+1's writes. Mitigation: stash creation happens in the same critical section as `phase_complete` write, before phase N+1 launches.
- The soft-join checkpoint adds 0-30s latency depending on how fast reflect-N is. Acceptable.

## Why not Proposal A's choice

Proposal A's sidecar-only v1 misses the strongest argument: when the cost of a false negative (missed regression) is asymmetrically worse than a false positive (false halt), the default should be conservative. Sc-reflect §10.4 explicitly makes this argument. Treating v1 as "data collection only" delays the actual value of the integration by 2-4 weeks.
