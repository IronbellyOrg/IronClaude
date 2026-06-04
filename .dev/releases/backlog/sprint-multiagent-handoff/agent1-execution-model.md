# Agent 1 — Per-task process / agent-swarm vs single per-phase session

## STEP-0 Finding (source-grounded)

Sprint today is HYBRID, defaulting to one Claude session per PHASE, with a conditional per-TASK subprocess path that is partially wired. The default/primary execution is per-phase: execute_sprint() iterates config.active_phases and, for each claude-mode phase, spawns exactly ONE ClaudeProcess(config, phase) whose build_prompt() emits a single `/sc:task Execute all tasks in @{phase_file}` prompt covering the whole phase. A SECOND path exists: _parse_phase_tasks(phase) and `if tasks:` delegates to execute_phase_tasks(), which loops `for i, task in enumerate(tasks)` spawning ONE subprocess per task via _run_task_subprocess (proc.start()/proc.wait() per task). BUT this per-task path is gated (only triggers when the phase file has `### T<PP>.<TT>` headings) and is incomplete: it hardcodes turns_consumed=0, bypasses build_prompt/sprint-context/isolation env vars, and is not wired into tmux/monitor. Execution is strictly SEQUENTIAL either way — NO parallelism. Budget is global: TurnLedger(initial_budget = config.max_turns * len(config.active_phases)), one shared ledger. tmux is ONE session with 3 panes, not per-agent. The spawn command is ['claude','--print','--verbose',permission_flag,'--no-session-persistence','--tools','default','--max-turns',N,'--output-format','stream-json','--model',M] via subprocess.Popen with os.setpgrp. Context hand-off between phases is via .md/filesystem + prompt-injection (build_prompt injects prior-phase artifact paths; build_task_context/get_git_diff_context/compress_context_summary build markdown summaries) — there is no agent-mail/mailbox.

**Source evidence:**

- `executor.py:1236 — for phase in config.active_phases (per-phase loop)`
- `executor.py:1324 — proc_manager = ClaudeProcess(config, phase) (ONE session per phase)`
- `executor.py:1340 — single while proc_manager._process.poll() loop (sequential)`
- `executor.py:1261-1262 — _parse_phase_tasks gate then if tasks: delegate to execute_phase_tasks`
- `executor.py:971 — for i, task in enumerate(tasks) (per-task loop, sequential)`
- `executor.py:1076-1115 — _run_task_subprocess proc.start();proc.wait(); turns_consumed hardcoded 0, incomplete`
- `executor.py:1118-1132 — _parse_phase_tasks returns None unless ### T<PP>.<TT> headings present`
- `executor.py:1200-1203 — TurnLedger initial_budget = max_turns * len(active_phases), single global ledger`
- `executor.py:933,1002-1010 — private _subprocess_factory test-injection hook (not a StepRunner Protocol)`
- `executor.py:1969-1972 — _write_preliminary_result documents single-thread assumption, needs O_EXCL if parallelized`
- `process.py:88-216 — ClaudeProcess.build_prompt builds ONE /sc:task-per-phase prompt`
- `process.py:123-124 — build_prompt docstring 'Build the /sc:task prompt for this phase'`
- `process.py:257-385 — build_task_context/get_git_diff_context/compress_context_summary (.md context injection)`
- `pipeline/process.py:79-95 — build_command claude --print --verbose ... --output-format stream-json --model`
- `pipeline/process.py:131-134 — os.setpgrp process group, single Popen`
- `monitor.py:1-37 — single-stream NDJSON monitor per phase output file`
- `tmux.py:97 — single tmux new-session, 3 panes (TUI/summary/tail), not per-agent`

## Options

### (a) Single per-PHASE session [current default]

**Pros:**
- Simplest control flow: one ClaudeProcess, one monitor, one poll loop, one tmux tail per phase — already shipped and battle-tested (executor.py:1308-1607)
- Agent sees full phase context in one window: cross-task reasoning (shared imports, multi-task refactors) is natural and free
- Cheapest tokens for cohesive phases: no per-task re-priming or per-task sprint-context header re-injection
- Crash-recovery/checkpoint inference already model phase granularity (_check_checkpoint_pass, PASS_RECOVERED at executor.py:2104-2108)
- Budget reconciliation is simple: one subprocess, one ledger, no concurrency race

**Cons:**
- One context window per whole phase → context-window exhaustion on big phases (detect_prompt_too_long → INCOMPLETE at executor.py:2093-2099)
- All-or-nothing blast radius: a STRICT-task failure/stall kills the phase; partial progress reconstructed only heuristically
- No intra-phase parallelism: independent tasks run serially, wall-clock bound by slowest chain
- Coarse per-phase turn accounting (monitor.state.turns), no per-task cost attribution
- Executor cannot enforce per-task budget caps; a runaway early task starves later tasks of max_turns

_Best when:_ Phases with tightly-coupled tasks, small/medium task counts, where cross-task context continuity outweighs isolation and the operator wants the simplest single-stream run.

### (b) One process per TASK [partially wired]

**Pros:**
- Bounded blast radius: task failure/stall/timeout isolated; already-passed siblings durable (TaskResult per task at executor.py:1032-1063)
- Per-task budget enforcement natural: debit(minimum_allocation) before launch + reconcile after already exists (executor.py:990-1031)
- Precise per-task turn/cost accounting once turns_consumed is wired (currently hardcoded 0 at executor.py:1114)
- Fresh context per task avoids phase-level context exhaustion
- 4-layer IsolationLayers (executor.py:106-182) maps cleanly to per-task scoping
- Per-task resume already modeled (build_resume_output --resume {task_id} at models.py:779-833)

**Cons:**
- Context discontinuity: each task must be re-primed via build_task_context/compress_context_summary; re-injection cost grows with task count and can itself trigger prompt-too-long
- Incomplete today: _run_task_subprocess skips build_prompt sprint-context, skips isolation env_vars, hardcodes turns=0, not wired to monitor/tmux (executor.py:1076-1115) — observability regresses
- Token overhead: N cold starts, N primings, N tool re-discovery cycles
- More lifecycle surface = more orphan-process risk (os.setpgrp cleanup per task)
- Still sequential: buys recovery, not speed

_Best when:_ Phases with many loosely-coupled tasks where partial-failure recovery and precise per-task budget/cost accounting matter more than cross-task continuity; the natural next step once turn-counting and monitor/tmux wiring are completed.

### (c) Swarm of parallel per-TASK agents

**Pros:**
- Wall-clock speedup proportional to independent-task width
- Maximal isolation: each agent own process group, own isolation dir, own stream
- Maps to a real DAG: TaskEntry.dependencies (models.py:34) can drive a topological scheduler
- Per-agent stream-json enables richer parallel observability with a multiplexed monitor

**Cons:**
- Concurrency hazards on shared state: single global TurnLedger (executor.py:1200) is NOT process-safe — debit/credit races corrupt budget; _write_preliminary_result explicitly warns single-threaded, needs O_EXCL (executor.py:1969-1972)
- Shared-filesystem races: parallel agents writing same repo (git index, shared config, same files) → lost writes/conflicts unless worktree-isolated
- Monitor/tmux are single-stream/single-session (monitor.py, tmux.py:97) — need multiplexing; large rewrite
- Sibling agents can't see each other's in-flight results; needs mailbox or join barrier
- Highest, least-predictable token cost: N concurrent primings + coordination + boundary redundancy
- Hardest partial-failure reasoning: repo-consistency requires transactional/worktree semantics

_Best when:_ Large phases with a wide, well-partitioned set of provably-independent tasks AND infrastructure investment in per-agent worktrees, a process-safe ledger, and a multiplexed monitor. Overkill for typical coupled phases.

### (d) Hybrid: per-phase default + per-task escalation + bounded swarm for independent islands

**Pros:**
- Right-sized cost: cheap per-phase for coupled phases; escalate to per-task only when flagged parallel or when a phase hits prompt-too-long/INCOMPLETE (executor.py:2093-2099 is the natural trigger)
- Reuses existing seams: _parse_phase_tasks gate (executor.py:1118) already chooses per-task vs per-phase; a StepRunner Protocol replacing _subprocess_factory (executor.py:933) makes strategy pluggable
- Bounded concurrency: max_parallel cap + DAG scheduler limits blast radius and budget contention
- Graceful degradation: fall back per-task → per-phase when worktree/process-safe-ledger infra absent
- Migration-safe: ships incrementally behind flags

**Cons:**
- Most moving parts: three strategies + scheduler + selector = highest test surface
- Strategy heuristics can mis-fire (declaring tasks independent when they share files) — needs explicit phase metadata, not inference
- Swarm tier still requires the prerequisite infra of (c)
- Three context hand-off modes (in-session / .md-injection / mailbox) must be specified per tier

_Best when:_ The pragmatic end-state: one engine picking per-phase/per-task/bounded-swarm by declared phase metadata and runtime signals, defaulting to cheap/observable per-phase and escalating only where recovery or speed payoff is proven.

## Roadmap Proposals (3)

### LEAN — Harden the per-task path that already exists (no swarm, no parallelism)  `[lean]`

| Phase | Goal | Test strategy |
|---|---|---|
| P1: Complete per-task subprocess wiring | Make _run_task_subprocess (executor.py:1076-1115) a first-class peer of the per-phase path: per-TASK sprint-context prompt, pass IsolationLayers.env_vars (executor.py:106-182), wire real turn counting from monitor NDJSON (replace hardcoded turns_consumed=0 at executor.py:1114). | Unit: assert _run_task_subprocess returns (exit_code, turns>0, output_bytes) parsed from a fixture stream-json; assert isolation env vars present in spawned env (patch Popen). Token-cost: golden test that per-task turns sum == ledger.consumed delta. Regression: existing _subprocess_factory tests pass (executor.py:933). |
| P2: Per-task observability + budget correctness | Attach a monitor to each per-task output file so TUI shows per-task progress; verify global TurnLedger debit/credit reconcile (executor.py:990-1031) is exact across N tasks. | Budget invariant: assert available()==initial-consumed+reimbursed after a 10-task phase with mixed pass/fail/timeout. Partial-failure: kill task 3 of 5 (124→INCOMPLETE), assert tasks 1-2 durable, 4-5 in remaining_task_ids, build_resume_output emits correct --resume {task_id} (models.py:779). Observability: TUI last_task_id advances. |
| P3: End-to-end + crash recovery parity | Give per-task phases the same checkpoint/crash-recovery treatment as per-phase (PASS_RECOVERED, contamination check); confirm _write_preliminary_result single-thread assumption (executor.py:1969) stays valid. | E2E: 2-phase tasklist (one per-phase, one per-task) under fake-claude; assert SprintResult, gate-kpi-report.md, execution-log.jsonl consistent. Crash recovery: non-zero exit with written checkpoint → PASS_RECOVERED + crash_recovery_log.md entry. |

### MODERATE — Pluggable StepRunner + dependency-aware per-task scheduling (single-process-at-a-time)  `[moderate]`

| Phase | Goal | Test strategy |
|---|---|---|
| P1: Extract a StepRunner Protocol | Replace the private _subprocess_factory hook (executor.py:933,1002-1010) with a StepRunner Protocol (run(task,config,phase)->TaskResult) and two impls: PerPhaseRunner, PerTaskRunner; execute_sprint selects via the _parse_phase_tasks gate. | Unit: Protocol conformance for both runners; assert per-phase path byte-for-byte equivalent to today (golden build_prompt, process.py:169-216). Config-race: assert runners never mutate SprintConfig. Token-cost: per-runner turns captured in TaskResult.turns_consumed. |
| P2: Dependency DAG + topological serial scheduler | Use TaskEntry.dependencies (models.py:34) to build a DAG; execute topo order (still one subprocess at a time); context hand-off injects only upstream-dependency results via build_task_context (process.py:257-319), not all-prior. | Unit: cycle detection raises; topo order respects deps. Partial-failure: upstream dep FAIL → dependents SKIPPED (not attempted), reported remaining, no wasted launch. Context-correctness: injected context contains only transitive-dependency TaskResults. |
| P3: Context hand-off policy + per-task budget caps | Make hand-off a typed policy (in-session for per-phase; dependency-scoped .md injection for per-task); add per-task budget caps from the global ledger to prevent early-task starvation. | Token-cost: assert compress_context_summary keeps recent N full, older compressed (process.py:347-385); golden injected-markdown size under threshold for 20-task phase. Budget: runaway task hitting per-task cap terminated (124) without eating phase budget; ledger solvent for later tasks. |
| P4: E2E + observability upgrade | Per-task TUI rows + per-task entries in gate-kpi-report.md and execution-log.jsonl; full E2E across per-phase and per-task phases. | E2E: mixed tasklist under fake-claude; KPI attributes turns/gate-outcome per task. Observability: one JSONL event per task transition; TUI dual progress bar reflects completed_task_estimate. Regression: suite green; verify-sync clean. |

### ROBUST — Bounded per-task swarm with worktree isolation, process-safe ledger, multiplexed monitor  `[robust]`

| Phase | Goal | Test strategy |
|---|---|---|
| P1: Concurrency-safe shared state | Make TurnLedger process/thread-safe (atomic debit/credit via lock or serialized accounting); replace _write_preliminary_result TOCTOU exists-then-write with O_EXCL atomic create (executor.py:1969-1972 flags this). | Race: K threads/processes hammer ledger.debit/credit; final available() matches serial oracle (property-based). O_EXCL: two concurrent writers to same result path → exactly one wins, no corruption. Stress: 100-iteration race loop under pytest-xdist. |
| P2: Per-agent worktree isolation | Each parallel agent runs in its own git worktree/scoped copy so concurrent writes don't collide; extend IsolationLayers (executor.py:106-182) to allocate/teardown per-agent worktree + CLAUDE_WORK_DIR. | FS race: two agents editing same module in separate worktrees → both succeed, defined join step reconciles, no lost writes. Cleanup: worktrees/isolation dirs removed on success AND crash (orphan-cleanup parity with executor.py:1226). Git-safety: GIT_CEILING_DIRECTORIES honored, no upward traversal. |
| P3: Bounded-concurrency DAG scheduler + mailbox hand-off | Topological scheduler with max_parallel cap launches independent islands concurrently; join barriers merge results; context hand-off via a mailbox (durable JSON/.md drop-box keyed by task_id) so siblings publish results without a shared session. | Partial-failure: fail one agent in a fan-out of 4 → siblings unaffected, dependents SKIPPED, remaining_task_ids correct, repo consistent. Mailbox: downstream reads exactly its upstream deps; ordering/idempotency under retry. Backpressure: max_parallel never exceeded; budget contention bounded by P1 ledger. |
| P4: Multiplexed monitor + per-agent observability | Replace single-stream OutputMonitor/single tmux session (monitor.py, tmux.py:97) with a multiplexer: one monitor per agent feeding an aggregated TUI; aggregate token-cost across agents. | Observability: aggregated MonitorState sums turns/tokens across agents correctly; each agent's stall watchdog fires independently (no cross-agent false stalls). Token-cost: end-of-sprint KPI == sum of per-agent ledgers. TUI: snapshot multi-agent layout. |
| P5: End-to-end, chaos, and rollback | Full E2E swarm on a real wide-independent phase; chaos tests (kill random agent, SIGINT mid-swarm, disk-full on one worktree); single-flag rollback to MODERATE serial path. | E2E: fake-claude swarm of 8 tasks; wall-clock < serial baseline AND correctness == serial oracle. Chaos: SIGINT mid-swarm → all agents terminated via process groups, partial results persisted, SprintOutcome.INTERRUPTED, no orphans. Rollback: max_parallel=1 reproduces MODERATE byte-for-byte (regression guard). |

## Recommendation

Adopt the HYBRID end-state (option d), sequenced LEAN → MODERATE → ROBUST, and STOP after MODERATE unless a concrete parallelism need is proven. Grounded in source: (1) The per-task path already exists but is unfinished and unsafe to lean on — _run_task_subprocess hardcodes turns_consumed=0, skips build_prompt's sprint-context header and the IsolationLayers env vars, and is invisible to monitor.py/tmux (executor.py:1076-1115). Finishing it (LEAN) is the highest-ROI, lowest-risk move: it buys per-task partial-failure recovery and cost attribution without touching the concurrency model. (2) The single global TurnLedger (executor.py:1200) plus _write_preliminary_result's explicitly-documented single-thread/TOCTOU assumption (executor.py:1969-1972) make a swarm (option c) unsafe TODAY — parallelism requires a process-safe ledger, O_EXCL writes, per-agent worktrees, and a multiplexed monitor, i.e. the entire ROBUST roadmap and a rewrite of monitor.py/tmux.py. Do not undertake speculatively (scope discipline). (3) The cleanest enabling refactor is to replace the private _subprocess_factory test hook (executor.py:933) with a StepRunner Protocol (MODERATE P1) — the seam that makes per-phase/per-task/swarm pluggable and testable, and it pays for itself even if the swarm is never built. Context hand-off: keep in-session continuity for per-phase; use dependency-scoped .md injection (build_task_context/compress_context_summary, process.py:257-385) for per-task; introduce a mailbox only if/when the ROBUST swarm is actually needed, since a mailbox solves sibling-to-sibling visibility under concurrency — a problem the sequential paths do not have. Net: ship LEAN now, MODERATE next, gate ROBUST behind a demonstrated wide-independent-phase workload.
