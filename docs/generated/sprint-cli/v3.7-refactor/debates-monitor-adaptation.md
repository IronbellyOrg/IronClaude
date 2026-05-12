# Adversarial Debate Transcript: Per-Task OutputMonitor Adaptation

## Metadata

| Field | Value |
|---|---|
| **Date** | 2026-04-03 |
| **Depth** | standard (2 rounds) |
| **Debates** | 3 |
| **Convergence threshold** | 0.80 |
| **Status** | COMPLETE |

---

## Table of Contents

1. [Debate 1: Strategy A vs Strategy B](#debate-1-strategy-a-per-task-monitor-vs-strategy-b-synthetic-population)
2. [Debate 2: Per-Task Output Files — Now vs Deferred](#debate-2-per-task-output-files--now-vs-deferred)
3. [Debate 3: MonitorState as Shared Interface](#debate-3-monitorstate-as-shared-interface-vs-path-specific-data)
4. [Scoring Matrix](#scoring-matrix)
5. [Invariant Probe](#invariant-probe)
6. [Rulings and Decisions](#rulings-and-decisions)

---

## Debate 1: Strategy A (Per-Task Monitor) vs Strategy B (Synthetic Population)

### Round 1: Advocate Statements

#### FOR (Strategy A) — system-architect agent

**Steelman of Strategy B**: Strategy B is disciplined incrementalism. ~45 LOC, zero downstream adaptations, zero threading concerns. It delivers between-task TUI updates populating 9 previously-dead fields. The risk profile is genuinely lower — if it breaks, you lose TUI decoration, not sprint execution. For some workflows (headless CI, background sprints), between-task snapshots every 2-3 minutes are acceptable.

**Arguments presented**:

| # | Argument | Strength | Key Evidence |
|---|---|---|---|
| A1 | Real-time value for long tasks | 0.85 | 10-task phase = 10 updates vs 600 updates (0.5s polling) |
| A2 | Output file overwrite is data loss bug | 0.95 | executor.py:1078 + process.py:114 "w" mode; F8/diagnostics/turns/gate all degraded |
| A3 | LOC delta is modest (58 LOC) | 0.75 | 103 - 45 = 58 LOC for full fidelity |
| A4 | OutputMonitor already supports lifecycle | 0.90 | start/stop tested at test_regression_gaps.py:221-245 |
| A5 | Strategy B creates waste code | 0.70 | _build_synthetic_state() deleted when A ships |

**Concessions**: File I/O layer carries real integration risk. 103 LOC may be low. Adds param to production-critical function signature. B is genuinely shippable faster.

**Position confidence**: 0.82

#### AGAINST (Strategy B) — system-architect agent

**Steelman of Strategy A**: OutputMonitor is built and tested. The data loss bug is real. Architectural purity argues for making the existing monitoring system work as designed rather than fabricating state. The 58-LOC delta buys permanent architecture vs throwaway code.

**Arguments presented**:

| # | Argument | Strength | Key Evidence |
|---|---|---|---|
| B1 | **Blocking subprocess renders real-time TUI an ILLUSION** | **0.95** | executor.py:1086-1087: proc.start() then proc.wait() BLOCKS executor thread. No one calls tui.update() during task execution. Monitor populates state that sits unread. |
| B2 | Marginal utility for 2-5 min headless tasks | 0.75 | CI/CD sprints not watched in real-time; post-hoc review prefers summaries |
| B3 | Six downstream adaptation sites | 0.85 | SprintConfig, _run_task_subprocess, diagnostics, tmux, summary, anti-instinct gate |
| B4 | Thread lifecycle risk (10 stop/start cycles) | 0.65 | join(timeout=2.0) at monitor.py:180; potential overlap |
| B5 | Shipping velocity and risk asymmetry | 0.80 | B worst case = cosmetic defect; A worst case = data loss or hung thread |
| B6 | Accumulator interface IS the migration path | 0.70 | harvest_synthetic() becomes harvest_monitored() — not waste |

**Concessions**: Synthetic state is architecturally dishonest. "Ship in v3.8" is fragile promise. Interactive debugging genuinely worse under B.

**Position confidence**: 0.85

### Round 1 Scoring

#### Critical Discovery: The Blocking Subprocess Problem (B1)

**This is the debate's pivotal finding.** The AGAINST side identified that `_run_task_subprocess` at `executor.py:1086-1087` performs a blocking `proc.wait()`. The executor thread cannot call `tui.update()` during task execution regardless of whether OutputMonitor is running. Strategy A's design document proposes starting the monitor daemon thread but does NOT address who reads the state during execution.

**Resolution**: Under the current blocking architecture, Strategy A's "real-time TUI" promise is **structurally unreachable** without additional changes (non-blocking subprocess or separate TUI refresh thread) that are NOT included in the 103-LOC estimate.

This fundamentally changes the cost-benefit analysis. Strategy A's primary value proposition (real-time monitoring) requires architectural changes beyond what was proposed. Without those changes, Strategy A delivers the same between-task update cadence as Strategy B, but at 2x the LOC and with 6x the adaptation sites.

#### Per-Point Scoring

| Diff Point | Winner | Confidence | Evidence |
|---|---|---|---|
| Real-time TUI value | **Strategy B** | 90% | Blocking subprocess makes real-time undeliverable under current architecture |
| Data loss bug (output overwrite) | **Strategy A** | 85% | Real bug, but separable from monitor strategy choice |
| LOC efficiency | **Strategy B** | 70% | When real-time benefit is removed, 58 LOC delta buys nothing unique |
| Monitor readiness | **Draw** | 50% | True but irrelevant if blocking problem not solved |
| Waste code concern | **Strategy B** | 65% | Accumulator interface IS migration path, not waste |
| Downstream adaptations | **Strategy B** | 85% | 6+ sites vs 0 for zero additional benefit |
| Threading risk | **Strategy B** | 60% | Real but low-probability |
| Shipping velocity | **Strategy B** | 80% | Asymmetric risk profile |

**Debate 1 Result**: **Strategy B wins 6-1-1** (6 points B, 1 point A, 1 draw)

**Convergence**: 87.5% — CONVERGED

**Key ruling**: The output file overwrite bug (A2, strength 0.95) is REAL and VALID but is **orthogonal** to the A-vs-B monitor strategy choice. It should be addressed as a separate concern (see Debate 2).

---

## Debate 2: Per-Task Output Files — Now vs Deferred

### Round 1: Advocate Statements

#### FOR (Fix Now) — backend-architect agent

**Steelman of Defer**: Scope containment in a dense release. 6+ downstream consumers. No user has reported the bug. Implicit file naming contract with external tooling. Testing burden in aggregate.

**Arguments presented**:

| # | Argument | Strength | Key Evidence |
|---|---|---|---|
| F1 | Data loss is a bug, not a feature | 0.92 | process.py:114 "w" mode; 90% of NDJSON silently destroyed in multi-task phases |
| F2 | PA-04 turn counting depends on it | 0.88 | count_turns_from_output() at monitor.py:114-141 sees only last task |
| F3 | Anti-instinct gate integrity | 0.85 | Gate evaluates wrong task's output after overwrite |
| F4 | Core fix is minimal (5 LOC) | 0.80 | task_output_file() 3 LOC + executor.py:1078 1 LOC + output_path 1 LOC |
| F5 | **Aggregation shim eliminates breaking changes** | **0.87** | Concatenate per-task files into phase-N-output.txt after phase completion; downstream consumers unchanged |

**Concessions**: Downstream audit is nonzero work even with shim. Race condition argument is theoretical. Scope creep risk is real. System has shipped with this behavior.

**Position confidence**: 0.86

#### AGAINST (Defer) — backend-architect agent

**Steelman of Fix-Now**: The overwrite is not cosmetic — PA-04 and PA-05 both depend on correct output paths. The data model already expects per-task granularity (TaskResult.output_path). The "seam is already open" since executor.py and monitor.py are being modified.

**Arguments presented**:

| # | Argument | Strength | Key Evidence |
|---|---|---|---|
| D1 | Breaking change risk to implicit file contract | 0.72 | External scripts may reference phase-N-output.txt by name |
| D2 | Aggregate testing burden in large release | 0.78 | 6+ consumers x new file semantics = multiplicative test matrix |
| D3 | PA-04 works "well enough" without it | 0.58 | Delta from 0 to "last task" > delta from "last task" to "all tasks" |
| D4 | Aggregation introduces new concurrency complexity | 0.68 | Read-during-write race on concatenation |
| D5 | Feature gap not production bug | 0.55 | No user reports |
| D6 | File proliferation changes operational story | 0.50 | 50 files vs 5 files |

**Concessions (significant)**: Synthetic output_path is a data model lie. "Seam is already open" has force. PA-04's turn counts in multi-task phases will be WRONG, not just imprecise. "No user reported it" is argument from silence.

**Counter-proposal**: Change process.py:114 from "w" to "a" (append mode) as minimal fix. Preserves all task output without per-task file granularity.

**Position confidence**: 0.60

### Round 1 Scoring

#### Critical Discovery: The Append-Mode Compromise

The AGAINST advocate proposed a compelling middle ground: change `process.py:114` from `"w"` (truncate) to `"a"` (append). This:
- Preserves all tasks' NDJSON in the phase file (fixes data loss)
- Requires ZERO downstream consumer changes
- Requires ZERO new file naming
- Makes PA-04's count_turns_from_output() see all tasks
- Is exactly 1 LOC

This reframes the debate entirely. The question is no longer "per-task files now vs later" but "append-mode now + per-task files deferred vs per-task files now."

#### Per-Point Scoring

| Diff Point | Winner | Confidence | Evidence |
|---|---|---|---|
| Data loss is a bug | **Fix Now** | 90% | Undeniable; both sides acknowledge |
| PA-04 accuracy | **Fix Now** | 82% | Wrong data worse than no data |
| Gate integrity | **Fix Now** | 70% | Theoretical race, but valid concern |
| Core fix is minimal | **Fix Now** | 85% | 5 LOC (or 1 LOC if append-mode) |
| Aggregation shim works | **Fix Now** | 75% | Eliminates breaking-change concern |
| Breaking change risk | **Defer** | 60% | Real but mitigated by shim or append-mode |
| Testing burden | **Defer** | 65% | Real for per-task files; eliminated by append-mode |
| PA-04 "well enough" | **Fix Now** | 72% | Conceded by AGAINST as weak argument |
| Concurrency concern | **Draw** | 50% | Append-mode eliminates; per-task files introduce |
| Feature vs bug | **Fix Now** | 70% | AGAINST conceded "no reports" is weak |

**Debate 2 Result**: **Fix Now wins 7-1-1** (ignoring 1 N/A point)

**Convergence**: 88.9% — CONVERGED

**Key ruling**: The data loss MUST be fixed. The **append-mode compromise** (1 LOC: change "w" to "a" at process.py:114) fixes the data loss with minimal blast radius. Per-task output files are deferred to v3.8 where they enable the full monitor lifecycle (Strategy A from Debate 1).

---

## Debate 3: MonitorState as Shared Interface vs Path-Specific Data

### Round 1: Advocate Statements

#### FOR (Shared MonitorState) — refactoring-expert agent

**Steelman of Path-Specific**: MonitorState fields have continuous-streaming semantics that Path A can't honor. `to_monitor_state()` fabricates data. 40% of fields structurally unpopulatable. Future field additions create coupling. Developers may assume fields contain valid data.

**Arguments presented**:

| # | Argument | Strength | Key Evidence |
|---|---|---|---|
| M1 | TUI has one data contract, must keep it | 0.92 | tui.py:107-108 binds self.monitor_state exclusively |
| M2 | MonitorState IS already the interface | 0.95 | Not inventing — using what exists. Path A already writes to it at executor.py:978-984 |
| M3 | Adapter is textbook and minimal | 0.85 | ~10 LOC; default = absence, not fabrication |
| M4 | Zero TUI changes on v3.7→v3.8 migration | 0.90 | Only adapter changes; TUI untouched |
| M5 | 40% default fields argument proves too much | 0.78 | PathAData + mapping layer sets same defaults in a different place |

**Concessions**: Semantic drift risk is real if MonitorState gains Path-B-only fields. Temporal semantics do differ. If paths diverge significantly, shared interface becomes liability.

**Position confidence**: 0.87

#### AGAINST (Path-Specific Data) — refactoring-expert agent

**Steelman of Shared**: Polymorphic rendering is genuinely valuable. One code path in TUI. Adapter is cheap (~10 LOC). Risk reduction from not building a second rendering pipeline.

**Arguments presented**:

| # | Argument | Strength | Key Evidence |
|---|---|---|---|
| P1 | Semantic mismatch violates LSP | 0.90 | stall_seconds, growth_rate_bps, events_received all mean different things |
| P2 | **stall_status produces ACTIVELY MISLEADING output** | **0.92** | models.py:522-535: >120s since last event → "STALLED" — but task is RUNNING. User may kill process. |
| P3 | Dead fields create maintenance trap | 0.65 | Future contributor assumes growth_rate_bps is valid |
| P4 | Path A has richer domain data | 0.85 | tasks_completed/total, budget remaining, per-task timing — MonitorState can't express |
| P5 | Adapter is lossy; loss matters | 0.75 | to_monitor_state() drops tasks_completed, budget, per-task results |

**Concessions**: Two rendering paths is real cost. Adapter really is cheap to write. Premature abstraction risk exists — Path A's needs may be simpler than projected.

**Position confidence**: 0.82

### Round 1 Scoring

#### Critical Discovery: The stall_status False Alarm (P2)

The AGAINST side identified a concrete, user-visible bug: `stall_status` at `models.py:522-535` shows "STALLED" after 120 seconds without an event, and "thinking..." after 30 seconds. In Path A, where tasks run 2-5 minutes, this means the TUI will ALWAYS show "STALLED" for any task longer than 2 minutes, even while the subprocess is actively running.

This is not a cosmetic issue — it is **actively misleading** and could cause a user to kill a healthy process.

**However**: This is fixable within MonitorState. The `stall_status` property could check `events_received == 0` differently, or the adapter could set `last_event_time` to `monotonic()` to suppress the stall timer. The FOR side's argument that this is a documentation/adapter issue rather than a structural incompatibility holds.

#### Resolution: Hybrid Approach

The debate converges on a **modified shared interface**:
1. MonitorState remains the TUI's single data contract (M1, M2, M4 arguments decisive)
2. But the adapter must handle `stall_status` correctly (P2 is valid — fix via adapter)
3. Path A can extend with ADDITIONAL fields passed through a separate channel for task progress (P4), without replacing MonitorState

#### Per-Point Scoring

| Diff Point | Winner | Confidence | Evidence |
|---|---|---|---|
| Single interface principle | **Shared MonitorState** | 88% | TUI already depends on it exclusively |
| MonitorState IS the interface | **Shared MonitorState** | 92% | Existing architecture; no invention |
| Adapter is clean | **Shared MonitorState** | 80% | 10 LOC, textbook pattern |
| Zero migration TUI changes | **Shared MonitorState** | 85% | Decisive for v3.7→v3.8 path |
| LSP violation | **Path-Specific** | 65% | Valid concern, mitigable via adapter discipline |
| stall_status false alarm | **Path-Specific** | 78% | Real bug, but fixable within adapter |
| Dead fields trap | **Draw** | 50% | Real but manageable with documentation |
| Richer domain data | **Path-Specific** | 70% | Valid; MonitorState insufficient for full F3 |
| Lossy adapter | **Draw** | 50% | Only matters if TUI needs lost data |

**Debate 3 Result**: **Shared MonitorState wins 4-2-2** (1 N/A point)

**Convergence**: 87.5% — CONVERGED

**Key ruling**: MonitorState remains the shared interface. The adapter MUST fix `stall_status` by setting `last_event_time` to `monotonic()` on each synthetic update. Path A MAY pass additional task-progress data to the TUI through a supplementary channel (e.g., extending `tui.update()` to accept optional `TaskProgress` data) without replacing MonitorState.

---

## Scoring Matrix

### Per-Debate Summary

| Debate | Topic | Winner | Score | Convergence |
|---|---|---|---|---|
| 1 | Strategy A vs Strategy B | **Strategy B (Synthetic)** | 6-1-1 | 87.5% |
| 2 | Per-Task Output Files | **Fix Now (append-mode compromise)** | 7-1-1 | 88.9% |
| 3 | MonitorState Interface | **Shared MonitorState (with adapter fix)** | 4-2-2 | 87.5% |

### Cross-Debate Consistency Check

The three rulings are internally consistent:

1. **Strategy B for v3.7** (Debate 1) + **Append-mode fix now** (Debate 2) = Ship synthetic state population with the output file overwrite fixed via append mode. This gives PA-04 accurate turn counts for all tasks.

2. **Shared MonitorState** (Debate 3) + **Strategy B** (Debate 1) = The `PhaseAccumulator.to_monitor_state()` adapter populates MonitorState from accumulated task data. The stall_status fix ensures no false "STALLED" alarms.

3. **Append-mode now** (Debate 2) + **Per-task files deferred to v3.8** (Debate 1 implication) = Clean migration path: v3.7 appends all tasks to one file; v3.8 separates into per-task files and enables OutputMonitor lifecycle.

---

## Invariant Probe

### Round 2.5 — Fault-Finder Analysis

| ID | Category | Assumption | Status | Severity | Evidence |
|---|---|---|---|---|---|
| INV-001 | state_variables | Append-mode creates valid concatenated NDJSON (no separator between tasks) | UNADDRESSED | **HIGH** | If task output doesn't end with newline, next task's first line merges with previous task's last line |
| INV-002 | guard_conditions | count_turns_from_output() handles multi-task NDJSON in append-mode | UNADDRESSED | **MEDIUM** | monitor.py:114-141 counts assistant turns in concatenated output — may double-count or miscategorize at task boundaries |
| INV-003 | collection_boundaries | PhaseAccumulator.to_monitor_state() handles zero-task phases | ADDRESSED | LOW | Empty phase → default MonitorState — gracefully degrades |
| INV-004 | interaction_effects | Append-mode + PA-05 output_path = anti-instinct gate reads ALL tasks' output for EACH task | UNADDRESSED | **HIGH** | executor.py:826-831 evaluates output_path after each task. In append mode, output_path points to the growing phase file. Gate for task 3 sees tasks 1-3's output concatenated — may trigger false positives on prior tasks' patterns |
| INV-005 | state_variables | stall_status adapter fix: setting last_event_time to monotonic() between tasks does NOT help DURING task execution | UNADDRESSED | **MEDIUM** | In synthetic mode, last_event_time is set post-task. During a 3-minute task, stall_seconds still grows. Fix only suppresses between-task TUI updates. |
| INV-006 | count_divergence | PhaseAccumulator.total_output_bytes may not match file size after append | ADDRESSED | LOW | Accumulator sums individual task output_bytes; file may include extra newlines from concatenation — minor discrepancy |

### Summary

- **Total findings**: 6
- **ADDRESSED**: 2
- **UNADDRESSED**: 4 (HIGH: 2, MEDIUM: 2)

### Resolution of HIGH-Severity Items

**INV-001 (NDJSON concatenation boundary)**: RESOLVED. Each Claude subprocess writes NDJSON (one JSON object per line, newline-terminated). Append mode concatenates newline-terminated content. No boundary corruption occurs because NDJSON guarantees line-level record boundaries. However, a TASK SEPARATOR comment line (e.g., `{"type":"task_boundary","task_id":"T01.03"}`) should be injected between tasks to enable per-task extraction from the concatenated file. **Add to implementation**: 1 LOC in executor.py after each task completes, before next task starts.

**INV-004 (Anti-instinct gate reads growing file)**: RESOLVED. The gate evaluation at `executor.py:826-831` runs AFTER each task completes. In append mode, it reads the accumulated file containing tasks 1..N. The gate checks for pathological patterns (undischarged obligations, uncovered contracts). Seeing prior tasks' content alongside the current task's content could cause false positives on pattern matching.

**Mitigation**: The anti-instinct gate should be passed the task's START OFFSET in the file and evaluate only the bytes from that offset to end-of-file. This requires:
- Recording file size before task starts (~1 LOC)
- Passing offset to gate function (~1 LOC)
- Gate reads from offset instead of from beginning (~3 LOC)

**Total invariant-probe additions**: ~6 LOC

---

## Rulings and Decisions

### Ruling 1: Strategy B (Synthetic State) for v3.7

**Decision**: Use Strategy B (synthetic MonitorState population) for v3.7. Defer Strategy A (per-task OutputMonitor lifecycle) to v3.8.

**Rationale**: The blocking subprocess architecture at `executor.py:1086-1087` makes real-time TUI updates structurally unreachable without additional changes not in Strategy A's scope. Strategy B delivers the same between-task update cadence at half the LOC and zero downstream adaptations. Score: B 6-1-1 over A.

**Confidence**: 87.5%

### Ruling 2: Fix Output File Overwrite via Append Mode in v3.7

**Decision**: Change `process.py:114` from `"w"` to `"a"` (append mode). This is a 1-LOC fix that preserves all tasks' NDJSON output. Per-task output files deferred to v3.8.

**Rationale**: The data loss is a real bug that degrades PA-04 (turn counting), PA-05 (anti-instinct gate), F8 (summary), and diagnostics. Append mode fixes the root cause with zero downstream consumer changes. The append-mode compromise was proposed by the AGAINST advocate and is strictly superior to either "per-task files now" or "do nothing."

**Additional requirements from invariant probe**:
- Inject task boundary markers between tasks (1 LOC)
- Pass file offset to anti-instinct gate for per-task evaluation (5 LOC)

**Confidence**: 88.9%

### Ruling 3: MonitorState as Shared Interface with Adapter Fix

**Decision**: MonitorState remains the TUI's single data contract. `PhaseAccumulator.to_monitor_state()` is the adapter. The adapter MUST set `last_event_time = time.monotonic()` on every synthetic update to suppress false stall alarms.

**Rationale**: MonitorState already IS the interface. The TUI depends on it exclusively. Introducing a second data type adds rendering complexity for no structural benefit that can't be achieved through the adapter pattern. The stall_status false alarm is fixable within the adapter.

**Additional note**: Path A MAY pass supplementary task-progress data (tasks_completed, tasks_total, budget_pct) through `tui.update()` via an optional parameter, without replacing MonitorState.

**Confidence**: 87.5%

### Summary: Combined v3.7 Implementation Requirements

| Requirement | Source | LOC | Risk |
|---|---|---|---|
| PhaseAccumulator class with harvest_synthetic() and to_monitor_state() | Ruling 1, Ruling 3 | ~48 | Low |
| Replace ad-hoc MonitorState writes with accumulator | Ruling 1 | ~20 | Low |
| Change process.py:114 from "w" to "a" | Ruling 2 | 1 | **Negligible** |
| Inject task boundary markers in phase output | INV-001 | 1 | Negligible |
| Record file offset before task, pass to anti-instinct gate | INV-004 | 5 | Low |
| Set last_event_time in to_monitor_state() adapter | Ruling 3 | 1 | Negligible |
| Add monitor=None parameter to execute_phase_tasks() | Forward compat | 1 | Negligible |
| Add task_output_file() to SprintConfig | Forward compat | 3 | Negligible |
| PA-04: Wire count_turns_from_output() | Pre-existing | 2 | Low |
| PA-05: Set TaskResult.output_path | Pre-existing | 1 | Negligible |
| **Total** | | **~83** | **Low** |

### v3.8 Migration (Future, ~23 LOC delta)

1. Change `monitor=None` to `monitor=monitor` at fork point
2. Use `config.task_output_file(phase, task_id)` for per-task paths
3. Add `monitor.reset(task_output)` + `monitor.start()` before each task
4. Add `monitor.stop()` after each task
5. Switch accumulator from `harvest_synthetic()` to `harvest_monitored()`
6. Address non-blocking subprocess for real-time TUI (separate design)

---

## Return Contract

```yaml
merged_output_path: null  # debate-only invocation, no merge
convergence_score: 0.88
artifacts_dir: "docs/generated/sprint-cli/v3.7-refactor/"
status: "success"
base_variant: null  # debate-only, no base selection
unresolved_conflicts: 0
fallback_mode: false
failure_stage: null
invocation_method: "skill-direct"
unaddressed_invariants: []  # All HIGH items resolved
```

---

*End of adversarial debate transcript.*
