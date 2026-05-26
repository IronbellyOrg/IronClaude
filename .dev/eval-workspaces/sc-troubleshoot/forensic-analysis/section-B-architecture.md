# Section B — Architecture & Design

Source files (all under `/config/workspace/IronClaude/.dev/releases/backlog/v5.xxforensic/`):

- `tfep-architecture-design.md` (TAD) — 1402 lines, primary architecture
- `tfep-refactoring-context.md` (TRC) — 403 lines, why the refactor
- `forensic-refactor-handoff.md` (FRH) — 636 lines, phase-to-phase architectural handoff
- `sprint-runner-tfep-handoff.md` (SRTH) — 464 lines, sprint-runner integration spec

The acronym `TFEP` resolves to **Test Failure Escalation Protocol** (TRC:382, SRTH:3). The architecture has two distinct layers: a **protocol/skill layer** (refactor of `/sc:forensic` + `/sc:task-unified` skills) and a **CLI/runner layer** (new `sprint/tfep.py` module orchestrating Claude subprocesses).

## Component Shape (skill vs command vs CLI vs script)

The design splits into four concrete component types:

1. **Slash commands as wrappers** — `/sc:forensic`, `/sc:task-unified`, `/sc:troubleshoot`, `/sc:brainstorm`, `/sc:adversarial` are existing slash commands; TFEP coordinates them rather than replacing them (TRC:42-77 chooses "Artifact B: refactor forensic spec, task-unified calls it" over "Artifact A: bake into task-unified" by score 7.85 vs 4.62).
2. **Skill (protocol) layer** — `src/superclaude/skills/sc-task-unified-protocol/SKILL.md` gets a ~50-100 line addition implementing the *prohibition* + *trigger detection* + *forensic invocation* + *escalation gradient* + *resume* + *report* responsibilities (TRC:138-145).
3. **CLI orchestration layer (new module)** — `src/superclaude/cli/sprint/tfep.py` is a new Python module containing `ForensicOrchestrator`, `EscalationState`, `perform_rollback`, `inject_remediation_tasks`, `write_incident_report` (TAD:36-44; SRTH:344-346). Estimated ~450 new lines (TAD:1391).
4. **Subprocess agents** — Each "agent" in the forensic pipeline is literally a separate `claude --print` subprocess spawned by the runner, not an in-session skill invocation (SRTH:38-51 explicit decision; TAD:447-486 `ForensicProcess` extends `pipeline/process.py` `ClaudeProcess`).

Layer responsibilities are explicitly contracted: "`task-unified` should own **when** forensic analysis is required; `/sc:forensic` should own **how** forensic analysis is performed" (FRH:23-25). The sprint runner adds a third concern: "the sprint runner owns *runner-orchestrated* parallel forensic subprocesses, NOT in-session skill invocation" (SRTH:40-51).

Module map (TAD:36-44):

```
src/superclaude/cli/sprint/
├── tfep.py        ← NEW: ForensicOrchestrator, rollback, injection, prompts, incident reports
├── executor.py    ← MODIFIED: phase loop TFEP branch, git baseline capture
├── process.py     ← MODIFIED: ForensicProcess subclass, resume prompt builder
├── monitor.py     ← MODIFIED: TFEP marker detection patterns
├── models.py      ← MODIFIED: PhaseStatus enum, MonitorState fields, SprintConfig fields
├── commands.py    ← MODIFIED: --tfep-* Click options
└── diagnostics.py ← MODIFIED: FailureCategory.TFEP
```

Dependency direction is strictly downward (TAD:46-62): `commands.py → executor.py → tfep.py → process.py → monitor.py → models.py`. `tfep.py` imports only from `models.py`, `pipeline/process.py`, `monitor.py`, and stdlib (TAD:64-68); it deliberately does NOT import from `executor.py`, `commands.py`, or `diagnostics.py` to avoid circular dependencies (TAD:70-74).

## Pipeline / Wave Structure

Two-tier pipeline gated by an escalation counter.

**Light tier (4-step, ~5-8K tokens, 6 invocations)** (TAD:344-376, TRC:99-100, SRTH:185-191):

1. Spawn 2 parallel RCA agents (`alpha`/`bravo`), each prompted with `/sc:troubleshoot` + inline `failure_context.yaml`.
2. Spawn 1 adversarial judge subprocess: `/sc:adversarial --compare rca-alpha.md,rca-bravo.md --depth quick` → `rca-verdict.md`.
3. Spawn 2 parallel solution agents (`alpha`/`bravo`), each prompted with `/sc:brainstorm` + the RCA verdict.
4. Spawn 1 adversarial judge: `/sc:adversarial --compare solution-alpha.md,solution-bravo.md --depth quick` → `solution-verdict.md`.

**Standard tier (2-step, 3 invocations)** (TAD:380-395, SRTH:192-195):

1. Spawn 2 parallel full-investigation agents (each does end-to-end RCA + solution).
2. Spawn 1 adversarial judge.

Parallelism is implemented via `concurrent.futures.ThreadPoolExecutor(max_workers=len(names))` (TAD:525-532). Each agent gets an independent context window because each is a separate subprocess (SRTH:46-50 — "Independent subprocesses enable true parallel investigation with no shared-budget contention").

Quick-mode phase mapping versus the full forensic pipeline (TRC:88-97): Phase 0 (Recon) SKIPPED (caller provides context); Phase 1 (RCA) fixed at 2 Sonnet agents; Phase 2 (Hypothesis debate) uses `/sc:adversarial --depth quick`; Phase 3 (Fix) fixed at 2 Sonnet agents; Phase 3b (Fix debate) `/sc:adversarial --depth quick`; Phase 4 (Implement) SKIPPED (returns fix plan to caller); Phase 5 (Validate) SKIPPED (caller handles retesting); Phase 6 (Report) abbreviated `tfep-report.md`.

**Phase entry/exit contract** (TAD:1252-1306):

- Contract 1 (Phase subprocess → Runner): result file contains `EXIT_RECOMMENDATION: TFEP_HALT`; working directory contains `failure_context.yaml`; NDJSON output emits `TFEP_TRIGGERED`.
- Contract 2 (Runner → Forensic agent): RCA prompt prefixed with `/sc:troubleshoot`, inline failure context, no `--fix` flag; Solution prompt prefixed with `/sc:brainstorm`, inline `rca-verdict.md`, format as tasklist-compatible remediation block.
- Contract 3 (`ForensicOrchestrator` → Executor): `ForensicResult` dataclass with `status`, `rca_verdict_path`, `solution_verdict_path`, `rollback_needed`, `causal_files`, `remediation_tasks`, `tier`, `agent_outputs`, `incident_summary` (TAD:292-302 and 1280-1290).
- Contract 4 (Executor → Phase subprocess re-launch): `/sc:task-unified` prompt with `--compliance strict`, rollback notice, skip-prior-tasks instruction, git diff summary, result file path.

## Escalation State Machine

Per-phase, in-memory only (TAD:248-282, SRTH:235-244). `EscalationState` dataclass tracks `phase_number`, `trigger_count`, `failing_tests`, and `tier`. The `advance(new_failing_tests)` method returns one of `"light"`, `"standard"`, or `"halt"`. Critical reset rule: if `new_failing_tests != self.failing_tests`, the counter resets to 0 (different tests = treated as fresh TFEP, not escalation) (TAD:259-261).

Counter→tier→budget multiplier mapping:

| trigger_count | tier | budget_multiplier | action |
|---|---|---|---|
| 1 | light | 1.5 | run 4-step pipeline, re-launch phase |
| 2 | standard | 2.0 | run 2-step pipeline, re-launch phase |
| 3+ | — | — | hard halt sprint |

State is **not persisted to disk** and resets on sprint resume (SRTH:244 — "Counter stored in executor state, not persisted to disk (resets on sprint resume)").

## Agent Inventory

The TFEP design does **not** propose any new custom agents in `src/superclaude/agents/`. All "agents" are slash-command-prefixed Claude subprocesses spawned by the orchestrator:

| Name | Role | Prompt prefix | Model | Max turns | Timeout |
|---|---|---|---|---|---|
| RCA alpha | Root-cause hypothesis | `/sc:troubleshoot` | Sonnet (default) | 50 | 300s |
| RCA bravo | Root-cause hypothesis | `/sc:troubleshoot` | Sonnet (default) | 50 | 300s |
| RCA judge | Adversarial adjudication | `/sc:adversarial --compare ... --depth quick` | Sonnet | 50 | 300s |
| Solution alpha | Fix proposal | `/sc:brainstorm` | Sonnet | 50 | 300s |
| Solution bravo | Fix proposal | `/sc:brainstorm` | Sonnet | 50 | 300s |
| Solution judge | Adversarial adjudication | `/sc:adversarial` | Sonnet | 50 | 300s |
| Re-launched phase | Remediation execution | `/sc:task-unified --compliance strict` | config.model | max_turns × multiplier | extended +600s |

Source: TAD:344-395, 463-485, 542-575; TRC:206-242. Sonnet is the default per FR-TFEP-03 (SRTH:172-176) and TAD:1185 (`tfep_model: str = ""` empty means Sonnet). Why fixed at 2: TRC:91-94 — light mode fixes agent count at 2 regardless of complexity; configurable via `--tfep-agents` flag with range 2-4 (SRTH:198-199, TAD:1213).

Boundary preservation (FRH:521-538): `/sc:troubleshoot` is used in diagnosis-only mode (no `--fix` flag — TAD:1271 "No `--fix` flag (diagnosis only)"). `/sc:brainstorm` is requirements/proposal-only (does not implement). `/sc:adversarial` is the adjudication mechanism. These boundaries are inherited rather than reinvented.

## MCP Integration

MCP usage is **inherited from the underlying slash commands**, not specified per-phase by TFEP itself. The architecture documents have minimal direct MCP discussion:

- TRC:273 — "Section 11: MCP Routing Table (quick mode uses fewer MCP servers)" is listed as a forensic spec section needing minor update, but the routing table is not duplicated in TAD/SRTH.
- The judge prompt format is `/sc:adversarial --compare {file_list} --depth quick` (TAD:550) — inherits whatever MCP wiring `/sc:adversarial` already has.
- RCA agents inherit `/sc:troubleshoot` MCP wiring; Solution agents inherit `/sc:brainstorm` wiring.
- Adversarial judge is always pinned to `--depth quick` regardless of TFEP tier (SRTH:199, 383 — "Quick depth is sufficient for 2-variant comparison; saves tokens for the main work").

Notably absent from these four files: explicit per-phase routing for auggie / serena / context7 / tavily / sequential. The TRC:88-97 phase table mentions model tiers (Sonnet across all 4 agents for quick mode, "no Haiku/Opus tiering" — TRC:299) but not MCP servers. This is a gap that Group A or the forensic-spec.md (not in this slice) likely covers.

## Refactoring Story (what changed and why)

The refactor arc is documented across three artifacts that align on a consistent narrative:

**Pain point 1 — ad-hoc fixes** (TRC:13-35, FRH:30-46): `sc:task-unified` agents were observed patching test failures with zero root-cause analysis. The transcript example: 10 pre-existing tests fail with `KeyError: None`; agent immediately edits the tests rather than investigating whether the implementation broke. Called out as "huge risk" (FRH:43).

**Pain point 2 — original spec was too heavy for auto-invocation** (FRH:241-269, TRC:42-77): The pre-refactor forensic spec was a 7-phase generic pipeline (Phase 0 broad recon, multi-domain agents, full reporting) — appropriate for QA/debug/regression, but overkill for a single tasklist's failing test cluster. Token budget: 50-80K (standard) vs the ~5-8K needed for task-unified integration (TRC:99).

**Pain point 3 — naming/flag collision** (FRH:285-296, FRH:446-454): the existing spec used `--mode debug|qa|regression|auto` for *investigation intent* and `--depth quick|standard|deep` for *adversarial debate depth*. Adding a forensic operating tier created three overlapping semantic dimensions. The proposed resolution (FRH:462-470): split into `--intent`, `--tier`, `--debate-depth`.

**Adversarial debate decision** (TRC:42-77): Option A (bake into task-unified) scored 4.62/10; Option B (refactor forensic + task-unified calls it) scored 7.85/10. The 1:1 mapping between TFEP steps and forensic phases (TRC:65-77) was the deciding architectural argument: "Baking it into task-unified means writing a second, less-capable version of the same pipeline."

**Two-phase implementation strategy** (TRC:357-372): Phase 1 ships an immediate **guard** (prohibition rule + trigger detection that tells the user to run `/sc:forensic --depth quick` manually) with zero forensic dependency. Phase 2 wires automatic invocation once quick mode lands. This decouples the prohibition value from the orchestration work.

**Net architectural shift**: from "task-unified contains its own embedded sub-protocol for failure handling" → "task-unified contains a circuit-breaker that defers to `/sc:forensic --depth quick`, and forensic gains a new `--mode triage` profile" (FRH:9-25 executive summary).

## CLI / Sprint-Runner Integration

The integration is a **hybrid**: skill-level prohibition + CLI-level orchestration. SRTH is the dedicated integration spec.

**Critical constraint — no IPC** (SRTH:23-24, NFR-TFEP-01 at SRTH:316-322): the sprint runner uses `claude --print --verbose -p <prompt>` (batch, not interactive). The runner cannot send data to a live Claude subprocess. The pattern is always: "Claude exits → runner orchestrates → runner re-launches Claude." Claude's work is preserved on disk; the re-launched subprocess picks up via resume prompt + git diff context.

**Detection mechanism** (SRTH:122-138 FR-TFEP-01):

- Real-time: regex patterns `TFEP_TRIGGERED`, `TFEP_RESOLVED`, `TFEP_ESCALATED` scanned from NDJSON stdout (TAD:902-907).
- Post-hoc: result file contains `EXIT_RECOMMENDATION: TFEP_HALT` (distinct from generic `HALT`) — checked BEFORE generic HALT (higher priority) (TAD:947-959).
- `MonitorState` extended with `tfep_triggered: bool`, `tfep_trigger_count: int`, `tfep_status: str` (TAD:911-917).

**Phase-loop integration** (TAD:962-998): a new `PhaseStatus.TFEP_HALT` branch in `execute_sprint()` calls `_handle_tfep_halt(...)` which returns `"resolved"` | `"escalated"` | `"halt"`. `TFEP_HALT` is NOT in `is_failure` (TAD:1162-1170) — it triggers the TFEP branch, not the generic failure branch. `TFEP_RESOLVED` IS in `is_success` (TAD:1156-1159).

**`_handle_tfep_halt()` orchestration** (TAD:1002-1125, 10 steps): 1) get/create `EscalationState`; 2) read `failure_context.yaml`; 3) `esc.advance(failing_tests)` returns light/standard/halt; 4) run `ForensicOrchestrator.run()`; 5) `perform_rollback()`; 6) `inject_remediation_tasks()` into isolation-dir phase file; 7) `build_tfep_resume_prompt()`; 8) re-launch via `_PipelineClaudeProcess` with `extended_turns = int(config.max_turns * esc.budget_multiplier)` and `extended_timeout = extended_turns * 120 + 300 + 600` (+600s TFEP padding); 9) `_determine_phase_status()` on re-launched subprocess; 10) `write_incident_report()`.

**New CLI flags** (TAD:1209-1219, SRTH:181-182):

- `--tfep-model` (default `""` = Sonnet)
- `--tfep-agents` (default 2, range 2-4)
- `--tfep-budget-multiplier` (default 1.5, range 1.0-3.0)

**Git baseline capture** (TAD:704-719): `git rev-parse HEAD` at phase start, stored for rollback diff baseline. Wrapped in try/except for non-git repos.

**Rollback algorithm** (TAD:644-701, FR-TFEP-10 at SRTH:289-311): `git diff --name-only {baseline}` to identify files changed during the phase; save full patch to `results/phase-{N}-tfep-rollback.patch` regardless of scope; intersect causal files (from `rca-verdict.md`) with phase-changed files; full revert if all changed files are causal, selective `git checkout` if some. Only files changed during *this* phase are eligible — never reverts work from prior phases (SRTH:303-306).

**Remediation task injection** (TAD:723-815): inserts a `## Failure Remediation Plan (Adjudicated)` block into the isolation-dir copy of the phase file. Remediation tasks use `T{XX}.50+` IDs to avoid collision with original `T{XX}.01-T{XX}.20` tasks. Format matches existing `parse_tasklist()` regex `^###\s+(T\d{2}\.\d{2})\s*(?:--|-—|—)\s*(.+)`.

**Resume prompt** (TAD:818-893): `/sc:task-unified Execute remediation tasks in @{phase_file} --compliance strict --strategy systematic` with explicit "SKIP tasks T01-T{last_completed}", "EXECUTE remediation tasks starting from T{XX}.50", "After remediation tasks, re-run ALL verification/test tasks", and git diff summary inline.

## Failure Handling + Fallbacks

The architecture documents address several specific failure modes:

**All forensic agents fail** (TAD:534-540): explicit validation step after parallel agent wait — "at least one agent must succeed". If `len(successes) == 0`, logs an error but returns whatever output paths exist (may be partial). Downstream `_build_result()` is expected to handle missing artifacts gracefully. This is the weakest spot in the design — no explicit fallback path beyond "return partial".

**Subprocess cleanup** (TAD:578-603): `ForensicProcess` inherits `terminate()` from `pipeline/process.py`: SIGTERM → 10s wait → SIGKILL on the process group. `ForensicOrchestrator.run()` wraps execution in try/except and calls `_cleanup()` to terminate any still-running forensic subprocesses on exception.

**Judge subprocess failure** (TAD:572-575): non-zero exit code logs a warning but still returns the expected verdict path; subsequent `_build_result()` parsing is presumably defensive (not fully spelled out).

**Missing `failure_context.yaml`** (TAD:1031-1034): `_handle_tfep_halt` returns `"halt"` immediately if `_find_failure_context()` returns `None`. This converts a missing-context bug into a hard sprint halt rather than a silent skip.

**Required-field validation** (TAD:400-412): `_load_context()` raises `ValueError` if any of `test_names`, `test_files`, `error_output`, `expected_behavior`, `actual_behavior`, `changes_made`, `task_description` is absent from `failure_context.yaml`.

**Forensic produces `status="failed"`** (TAD:1054-1057): incident report written with `outcome="forensic_failed"`, return `"halt"`.

**Re-launch escalates again** (TAD:983-994): the loop intentionally re-enters the TFEP branch via `continue`, and `EscalationState.advance()` returns `"halt"` on count >= 3.

**Phase isolation dir cleanup overwriting forensic artifacts** (SRTH:435): mitigated by writing TFEP artifacts to `results/phase-{N}-tfep/`, NOT into the per-phase isolation dir. This separation is structural, not enforced by code.

**Non-git repo** (TAD:716-719): `git rev-parse HEAD` wrapped in `except (FileNotFoundError, _subprocess.TimeoutExpired)` — `git_baseline = ""` falls through, and `perform_rollback` returns `RollbackResult(performed=False, ..., scope="none")` when no phase-changed files exist (TAD:666-668).

**Backward compatibility** (NFR-TFEP-03, SRTH:332-336): sprints that never trigger TFEP behave identically to today; `--no-escalation` on `task-unified` bypasses TFEP entirely (Claude never writes `TFEP_HALT`); all new CLI flags optional with defaults.

**Notable gap** — no explicit MCP-unavailability fallback. The design assumes `/sc:adversarial`, `/sc:troubleshoot`, `/sc:brainstorm` always work. If those slash-command subprocesses fail to load their skills (e.g., serena/auggie down), the failure surfaces as a subprocess non-zero exit and falls into the "all agents fail / partial result" path. No graceful degradation specified.

**Risk register from SRTH:428-435** explicitly enumerates: forensic token over-consumption (mitigated by 300s/agent + 3-attempt cap), rollback reverting correct work (mitigated by selective rollback + preserved patch), re-launch re-executes prior tasks (mitigated by explicit "skip T01-T04" + git diff context), low-quality quick-depth verdict (judged low risk), wall-clock exhaustion (3-attempt limit), isolation-dir cleanup deleting forensic artifacts (mitigated by writing outside isolation dir).

---

## Summary (≤200 words)

**Top-3 architectural choices:**

1. **Subprocess-orchestrated parallel forensic agents, not in-session skill invocation** (SRTH:38-51, TAD:447-486). Solves context exhaustion: the failing phase subprocess may already be near token limit, so RCA/Solution/Judge agents each get fresh full context windows as separate `claude --print` processes. Trade-off: no IPC, so handoffs are strictly file-based (`failure_context.yaml`, `rca-verdict.md`, etc.).

2. **Split ownership: skill says *when*, CLI says *how*** (FRH:23-25, TRC:42-77). `sc:task-unified` skill owns the prohibition + circuit-breaker; `sprint/tfep.py` owns subprocess orchestration, rollback, and re-launch. Solves the original "bake forensic into task-unified" anti-pattern (scored 4.62/10 vs 7.85/10 for separation) — keeps `task-unified` lean and `/sc:forensic` reusable for non-sprint contexts.

3. **Two-tier in-memory escalation with selective git rollback** (TAD:248-282, 644-701). Light tier (4-step, 6 invocations) → Standard tier (2-step, 3 invocations) → Hard halt. Selective rollback intersects forensic-identified causal files with phase-only-changed files (git baseline at phase start) — solves the "revert too much" risk while preserving full patches as audit trail. Counter resets on different-failing-tests to avoid spurious escalation.
