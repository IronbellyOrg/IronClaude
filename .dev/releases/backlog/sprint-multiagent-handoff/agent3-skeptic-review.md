# Agent 3 — Adversarial Skeptic Review (Group 1)

## Adversarial review transcript

### Ground-truth re-check

I re-read the sprint executor and process code instead of trusting either agent's citations. The most important correction is that Agent 1's STEP-0 overstates "per-phase default." In `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1259-1268`, the sprint loop parses phase tasks first and delegates to `execute_phase_tasks()` when headings exist. The per-phase `ClaudeProcess(config, phase, env_vars=...)` path is only reached after the per-task branch `continue`s or no tasks are parsed, at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1301-1325`. So the current model is content-gated, not cleanly "default per-phase with secondary per-task."

Agent 1 is right that execution is sequential: `execute_sprint()` loops active phases, and `execute_phase_tasks()` loops `for i, task in enumerate(tasks)` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:971-1010`. Agent 1 is also right that `_run_task_subprocess()` is underwired: it builds a minimal task prompt, initializes the pipeline base directly, starts/waits, and returns hardcoded turns `0` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1076-1115`. It does not use the sprint `build_prompt()` header or the per-phase `CLAUDE_WORK_DIR` isolation env vars.

However, Agent 1's "not wired into monitor/tmux" claim needs narrowing. The per-task path is not wired into `OutputMonitor` or the tmux tail-pane update used by the per-phase path (`/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1309-1318`). But it does perform minimal TUI updates before and after each task at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:993-1000` and `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1065-1071`. Calling it wholly invisible is inaccurate.

Agent 1 also conflates production handoff with dead helper functions. Production `ClaudeProcess.build_prompt()` injects sprint context and prior artifact/phase directory paths at `/config/workspace/IronClaude/src/superclaude/cli/sprint/process.py:147-167`. The richer helpers `build_task_context()`, `get_git_diff_context()`, and `compress_context_summary()` exist at `/config/workspace/IronClaude/src/superclaude/cli/sprint/process.py:257-385`, but a repository search found only definitions and tests, not production executor/build-prompt callers. Agent 2's "dead code with test-only callers" claim is therefore supported; Agent 1's handoff description is not.

Agent 1's resume optimism is also unfounded. `build_resume_output()` exists at `/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py:779-813`, but the current per-task sprint branch ignores `remaining` after `execute_phase_tasks()` returns and reduces task results to a phase PASS/ERROR at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1277-1301`. That is not wired per-task resume.

Dependencies are parsed, but not executed as a DAG. `TaskEntry.dependencies` is defined at `/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py:31-34`, and parsing fills it at `/config/workspace/IronClaude/src/superclaude/cli/sprint/config.py:435-487`. Current execution ignores it and follows list order at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:971-1010`. Treat DAG scheduling as a future proposal only.

Agent 2's handoff summary is directionally right but too absolute. The prompt asks the agent to write a one-line `EXIT_RECOMMENDATION` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/process.py:208-215`, but the executor can later write a structured result report at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:2020-2063`. Also, "markdown alone survives a killed subprocess" is overstated because the pipeline process writes stdout/stderr to files and sends the prompt via stdin at `/config/workspace/IronClaude/src/superclaude/cli/pipeline/process.py:116-143`.

### Pre-mortems

#### Agent 1 LEAN

Failure after six months: per-task execution appears hardened but still fails operators during partial failures. Earlier tasks are durable, but the user cannot resume cleanly because the per-task branch throws away `remaining` and never emits the modeled resume output. Cost reporting remains suspect if turn parsing is only patched inside `_run_task_subprocess()` but not reconciled with phase reports and TUI state.

Root cause: the proposal focuses on subprocess launch wiring, but the semantic bug is also at the join point after `execute_phase_tasks()` returns.

#### Agent 1 MODERATE

Failure after six months: the StepRunner abstraction ships, but migration regressions appear because per-phase and per-task paths are not behaviorally equivalent. Prompt contracts, isolation env vars, result files, monitor state, and ledger accounting become runner-specific edge cases.

Root cause: the current code has many implicit contracts around subprocess launch, not a clean runner seam. A Protocol without golden parity tests just relocates complexity.

#### Agent 1 ROBUST

Failure after six months: the swarm corrupts sprint state under real concurrency. Result files and context artifacts race, budget debits are inconsistent, and multiple worktrees produce conflicting edits that the join step cannot reconcile deterministically.

Root cause: the current implementation is single-process-at-a-time by design. `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1969-1972` explicitly documents the preliminary result writer's single-thread assumption, and `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1198-1203` creates one in-memory global ledger.

#### Agent 2 Lean

Failure after six months: `build_task_context()` is wired into the wrong place, inflating prompts without providing correct dependency context. In per-phase mode there are no prior per-task `TaskResult` objects when `build_prompt()` runs.

Root cause: lifecycle mismatch. Rich per-task context must be built inside the per-task loop from completed upstream results, not injected into the initial per-phase prompt.

#### Agent 2 Moderate

Failure after six months: the bus becomes an unreliable second source of truth. Parallel or retried writers corrupt the seq index, readers see partial payloads, and debugging requires correlating bus envelopes, result files, and NDJSON streams.

Root cause: the proposal names schema/order but not atomicity, idempotency, or authority. A versioned envelope is not a concurrency model.

#### Agent 2 Robust

Failure after six months: the mailbox survives killed agents, but the sprint still fails because agents edit overlapping files, dependents read contradictory snapshots, and token cost explodes from repeated context priming.

Root cause: durable handoff is only one swarm prerequisite. It does not solve worktree isolation, merge semantics, process-safe budget accounting, dependency scheduling, or multiplexed observability.

### Coupling check

Swarm plus prompt-only handoff is incompatible because sibling results cannot appear in initial prompts. Swarm plus unstructured markdown is unsafe unless writes are atomic and task-addressed. Worktree-isolated swarm plus raw path references is also unsafe because paths may be stale or worktree-local. Conversely, serial per-task execution plus a full mailbox/ack system is over-engineered: it adds shared state without solving a concurrent visibility problem. Single per-phase execution plus a per-task mailbox is lifecycle-incoherent because there are no addressable child task processes.

### Triage

- Agent 1 LEAN: REVISE. Correct target, but must include resume/result semantics and precise observability scope.
- Agent 1 MODERATE: KEEP. Best next architecture if guarded by golden parity tests and no parallelism.
- Agent 1 ROBUST: REVISE. Keep only as a later gated experiment; not ready as a committed roadmap.
- Agent 2 Lean: REVISE. Use dependency-scoped context in per-task prompts, not blindly in per-phase `build_prompt()`.
- Agent 2 Moderate: REVISE. Convert the bus idea into an atomic disk journal with a single authority model.
- Agent 2 Robust: KILL. Mailbox-first swarm is premature and hides harder blockers.

### Strongest combined direction

The strongest combined direction is Agent 1's MODERATE serial StepRunner/dependency-aware per-task execution plus a revised Agent 2 Lean handoff: dependency-scoped markdown context generated from actual completed upstream `TaskResult` objects and injected into each per-task prompt. This preserves the current single-process-at-a-time safety model while fixing the real gaps: resume, budget attribution, prompt lifecycle, and observability.

### Top risks before build

1. Define the partial-failure recovery contract before claiming per-task recovery.
2. Measure token cost and prompt growth; per-task cold starts may cost more, not less.
3. Establish one authoritative state model across result files, NDJSON output, context markdown, and any future bus.
