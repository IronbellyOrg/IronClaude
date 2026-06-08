# Mastra/Beads Study — Adversarial Red-Team Transcript

# Hostile re-verification transcript: Mastra/Beads feasibility

## Bottom line

I do not endorse the study as written. The narrow seam-swap thesis has real evidence, but the headline recommendation over-merges three different projects: replacing a Claude subprocess seam, service-ifying orchestration, and delivering paid/DIY multi-tenant RBAC. Those have different risk profiles. My revised recommendation is **defer**: run a hard Phase-0 evidence spike and commercial/license check, but do not start the strangler roadmap until those gates pass.

## Source files re-read

- `/config/workspace/IronClaude/.dev/releases/backlog/mastra-beads-port-feasibility/merged-requirements.md`
- `/config/workspace/IronClaude/.dev/releases/backlog/mastra-beads-port-feasibility/adversarial/proposal-a.md`
- `/config/workspace/IronClaude/.dev/releases/backlog/mastra-beads-port-feasibility/adversarial/proposal-b.md`
- `/config/workspace/IronClaude/.dev/releases/backlog/mastra-beads-port-feasibility/adversarial/proposal-c.md`
- `/config/workspace/IronClaude/.dev/releases/backlog/mastra-beads-port-feasibility/adversarial/proposal-d.md`
- `/config/workspace/IronClaude/.dev/releases/backlog/mastra-beads-port-feasibility/enrichment/codebase-context.md`
- `/config/workspace/IronClaude/src/superclaude/cli/pipeline/process.py`
- `/config/workspace/IronClaude/src/superclaude/cli/pipeline/executor.py`
- `/config/workspace/IronClaude/src/superclaude/cli/sprint/process.py`
- `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py`
- `/config/workspace/IronClaude/src/superclaude/cli/sprint/monitor.py`
- `/config/workspace/IronClaude/src/superclaude/cli/sprint/commands.py`
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py`
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/gates.py`
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/convergence.py`
- `/config/workspace/IronClaude/src/superclaude/cli/audit/wiring_gate.py`
- `/config/workspace/IronClaude/src/superclaude/cli/pipeline/gates.py`
- `/config/workspace/IronClaude/src/superclaude/cli/pipeline/fmea_classifier.py`

## Claim re-verification

### 1. Only ~1.2K of ~73K LOC is Claude-coupled — PARTIAL

The arithmetic is real only for a narrow definition. `wc -l` confirms:

- `/config/workspace/IronClaude/src/superclaude/cli/pipeline/process.py`: 244 LOC
- `/config/workspace/IronClaude/src/superclaude/cli/sprint/process.py`: 385 LOC
- `/config/workspace/IronClaude/src/superclaude/cli/sprint/monitor.py`: 571 LOC

That totals 1,200 LOC. The CLI Python tree is 72,906 LOC, so the ~73K denominator is supported.

But the claim is too clean. `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py` embeds Claude assumptions outside those three files: lines 1135-1147 describe the main loop as launching a `claude -p` subprocess and preflight-check `shutil.which("claude")`; lines 1198-1203 build `TurnLedger(initial_budget=config.max_turns * len(config.active_phases))`; lines 1320-1324 set `CLAUDE_WORK_DIR` and instantiate `ClaudeProcess`. `/config/workspace/IronClaude/src/superclaude/cli/sprint/commands.py` lines 88-117 expose `--max-turns`, Claude model, and Claude permission flags. So: **1.2K is the narrow process+monitor seam, not the full Claude-coupled behavior surface.**

### 2. `pipeline/executor.py` runs against injected StepRunner Protocol — SUPPORTED

`/config/workspace/IronClaude/src/superclaude/cli/pipeline/executor.py` lines 41-60 define `class StepRunner(Protocol)`, and lines 63-72 define `execute_pipeline(..., run_step: StepRunner, ...)`. This is a real seam.

Hostile caveat: the docstring at lines 44-47 says the runner is responsible for launching the `claude -p` subprocess. That means the code is injectable, but the conceptual contract remains Claude-shaped.

### 3. `roadmap/executor.py` wraps runtime behind `claude_process_factory` / `_ClaudeRunner` — PARTIAL

The semantic/convergence path is wrapped: `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py` lines 1253-1287 define `_ClaudeRunner`, and lines 1358-1365 pass `claude_process_factory=lambda: _ClaudeRunner(config)` into `run_semantic_layer`.

But the ordinary roadmap step runner is not fully wrapped: lines 1107-1118 instantiate `ClaudeProcess` directly. The study's phrasing makes roadmap sound runtime-abstracted as a whole; source only supports that for the semantic-layer adapter path.

### 4. `sprint/executor.py` seam is private `_subprocess_factory` / hardcoded `ClaudeProcess`, not a clean Protocol — SUPPORTED

`/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py` lines 927-955 define `_subprocess_factory` as an optional testing callable. Lines 1001-1010 use it if supplied, otherwise delegate to `_run_task_subprocess`. Lines 1076-1115 show `_run_task_subprocess` manually constructs a `ClaudeProcess` via the base class and uses `output_format="stream-json"`. Lines 1320-1324 show the main phase fallback directly constructing `ClaudeProcess(config, phase, env_vars=_phase_env_vars)` with `CLAUDE_WORK_DIR`.

This is not a clean Protocol seam. Sprint is the highest-risk flagship, not the easy first target.

### 5. ~62K LOC gate/convergence/FMEA/audit is runtime-agnostic — PARTIAL

Representative files support the broad direction:

- `/config/workspace/IronClaude/src/superclaude/cli/pipeline/gates.py` lines 1-10 says pure Python, no subprocess, no LLM.
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/gates.py` lines 1-9 define pure GateCriteria/semantic checks.
- `/config/workspace/IronClaude/src/superclaude/cli/audit/wiring_gate.py` lines 1-14 is static AST/regex-style analysis and says zero pipeline imports.
- `/config/workspace/IronClaude/src/superclaude/cli/pipeline/fmea_classifier.py` lines 1-14 describes pure classifier logic and no sprint/roadmap imports.

But convergence is not perfectly runtime-neutral conceptually. `/config/workspace/IronClaude/src/superclaude/cli/roadmap/convergence.py` lines 24-40 defines turn-budget constants and conditionally imports `TurnLedger` from sprint models. That is not Claude subprocess coupling, but it is Claude-era accounting semantics. Also, I verified representative files and LOC bands, not every claimed one of the ~62K LOC.

## Pre-mortem: assume the port failed 18 months later

1. **Telemetry reconstruction failed.** ACP did not expose enough event richness to recreate stream-json turn, token, tool, and error semantics. The team shipped approximate monitoring, and sprint recoverability degraded.
2. **Mastra churn became a tax.** Workflow, auth, ACP, and observability APIs moved faster than the team budgeted for. Version pins delayed patches; upgrades broke adapters.
3. **EE licensing blocked the actual goal.** Phases 0-4 delivered a service shell but not company-grade multi-tenant RBAC. The EE quote or terms were unacceptable, and DIY RBAC became a new platform project.
4. **Python-behind-MCP became permanent.** The hybrid avoided a rewrite but created durable two-runtime operations: Python services, Node/Mastra, MCP/HTTP schema translation, dual tracing, and cross-boundary failure handling.
5. **The multi-tenant pilot lost to CLI+worktrees.** Users already had workable isolation with local worktrees and subagents. The service added queueing/auth/sync overhead without proving better outcomes.
6. **Task stores drifted.** Backlog.md became the human-facing task store, MDTM artifacts stayed executable, and Beads later appeared as a scheduling index. Three task graphs disagreed.

## V/C/L/R challenge

The study's **V33/C30/L29/R26** is too favorable. I would score the actual program as:

| Value | Complexity | Likelihood | Risk |
|---|---|---|---|
| 27 | 34 | 20 | 34 |

Rationale:

- **Value 27, not 33:** The reusable IP already works. The net-new prize is multi-tool/multi-tenant service operation, and the most strategic part is commercially gated.
- **Complexity 34, not 30:** Sprint is not Protocol-clean; monitor telemetry is load-bearing; Backlog mapping is not lossless; the hybrid adds permanent polyglot ops.
- **Likelihood 20, not 29:** The study blends likely seam-spike success with much less likely multi-tenant platform success.
- **Risk 34, not 26:** Permission semantics, turn accounting, tenant isolation, and task-store authority are not edge risks; they are central invariants.

## Attack on the five unresolved gates

1. **Mastra-early vs Mastra-late:** Decidable enough now: choose Mastra-late unless @mastra/acp licensing and ACP parity pass. Mastra-early adds dependency churn before proof.
2. **ACP parity:** Correctly unresolved, but mis-framed as one gate. Split into permission semantics, turn/token reconstruction, cancellation, workspace isolation, and Claude+one-tool execution.
3. **@mastra/acp license:** Decidable now via package/source/license inspection. It should be a day-zero legal/source artifact, not a later architectural gate.
4. **Per-tool parity:** Cursor/Gemini/Copilot parity is not all needed for go/no-go. Prove Claude plus one non-Claude tool first; defer breadth.
5. **Permanent polyglot vs transitional hybrid:** This is not optional later philosophy. If the org will not accept permanent Python+Node operations, the hybrid plan is incoherent.

## Phase triage

| Phase | Ruling | Reason |
|---|---|---|
| 0 | REVISE | Keep the spike, but make license/commercial verification day-zero and define measurable parity blockers. |
| 1 | REVISE | Do not wrap all ~62K LOC; expose a small set of high-value tools first and prove schemas/errors/latency/tracing. |
| 2 | REVISE | Do not start with sprint. It is the least substitution-clean flagship. Start with a smaller pipeline/roadmap path, then sprint. |
| 3 | REVISE | Backlog.md should begin as a mirror, not task-of-record, until round-trip loss is measured. |
| 4 | REVISE | Introduce Mastra only if it beats a thin Python ACP client on demonstrated value. |
| 5 | KILL | The RBAC decision is too late. If it is the strategic driver, decide EE-buy-vs-DIY before major buildout. |

## Revised recommendation

**DEFER.** Do a narrow, time-boxed Phase-0 verification package only: commercial/license evidence, ACP Claude parity, one second tool, and a telemetry reconstruction report against current stream-json outputs. Until that exists, the hybrid roadmap is not yet a conditional go; it is an attractive architecture story with unresolved load-bearing facts.

## Top risks

1. The central abstraction is overstated: pipeline is cleanly injected; roadmap only partly; sprint not.
2. The 1.2K coupling figure excludes important Claude assumptions in executor, commands, prompts, TurnLedger, and hooks.
3. `monitor.py` is a reliability component, not a replaceable parser.
4. EE licensing may block the actual strategic goal after sunk cost.
5. Backlog.md may be a lossy mirror for MDTM semantics.
6. Permanent Python+Node/MCP operations may become the main cost of ownership.
7. Multi-tool ACP may force lowest-common-denominator semantics below current Claude Code fidelity.
