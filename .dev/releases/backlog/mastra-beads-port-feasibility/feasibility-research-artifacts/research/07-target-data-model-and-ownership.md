# Research: 07 - Target Data Model and Ownership Mapping
**Investigation type:** Architecture Analyst / Integration Mapper
**Scope:** `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/research/research-notes.md`, `.dev/tasks/` task folder patterns, `.dev/releases/backlog/mastra-beads-port-feasibility/seed-brief.md`, `src/superclaude/cli/sprint/config.py`, `src/superclaude/cli/sprint/models.py`, `src/superclaude/cli/pipeline/models.py`, `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md`, `src/superclaude/skills/sc-tasklist-protocol/`
**Status:** Complete
**Date:** 2026-06-02
---

## Source Inventory and Verification Baseline

| Source | Lines read | Current-state use in this report | Verification tag |
|---|---:|---|---|
| `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/research/research-notes.md` | 1-297 | Parent research plan, assigned scope, target outputs, and preliminary option framing. Doc-sourced target-stack claims remain uncertain until Phase 4 web validation. | [CODE-VERIFIED for file existence/content; UNVERIFIED for external Stack D claims] |
| `.dev/releases/backlog/mastra-beads-port-feasibility/seed-brief.md` | 1-59 | Seed problem statement, strategic constraints, known context, and open questions. Current-code claims are cross-checked below against source files where in scope. | [CODE-VERIFIED for file existence/content; mixed verification per claim] |
| `src/superclaude/cli/sprint/config.py` | 1-510 | Current tasklist index/phase/task parsing contract. | [CODE-VERIFIED] |
| `src/superclaude/cli/sprint/models.py` | 1-884 | Current sprint task/phase/result/runtime/telemetry/budget models. | [CODE-VERIFIED] |
| `src/superclaude/cli/pipeline/models.py` | 1-235 | Current shared pipeline step/gate/deliverable/config primitives. | [CODE-VERIFIED] |
| `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` | 1-1205 | Current complex MDTM task file schema, execution rules, handoff artifact convention, and QA gate semantics. | [CODE-VERIFIED] |

Key source-of-truth rule for this report: code and current task templates define the current SuperClaude artifact/state/task concepts. Mastra, Backlog.md, and Beads mappings are target-stack assumptions unless independently validated by Phase 4 web research.

## Model Group A: Current Artifact and Task Concepts

### Inventory Table

| Concept | Current representation | Owner today | Evidence | Target mapping hypothesis | Assumption status |
|---|---|---|---|---|---|
| Research task file | MDTM task markdown with YAML frontmatter (`id`, `title`, `status`, `type`, `priority`, dates, assignment, dependencies, related docs, tags) plus ordered checklist phases. | `.dev/tasks/` task file is the human/execution source of truth. | Current task frontmatter at `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/TASK-RESEARCH-20260602-211124.md` lines 1-44; MDTM template frontmatter at `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` lines 1-44. | Backlog.md should likely own durable markdown tasks/docs/decisions; Beads can mirror dependency/status graph; Mastra can hold workflow run state/traces. | [UNVERIFIED target-stack assumption] |
| MDTM execution item | Flat checkbox item under phase sections; each item must be self-contained and marked one at a time. | Task executor / `.dev/tasks` markdown. | `READ → IDENTIFY → EXECUTE → UPDATE → REPEAT` at template lines 394-403; prohibited multi-item behavior at lines 405-430. | Backlog.md tasks can store human-readable execution items; Mastra steps should execute/trace each item; Beads dependencies can represent item-to-item blockers where graph-level execution is needed. | [UNVERIFIED target-stack assumption] |
| Handoff artifact | Files under task workspace subdirectories such as `research/`, `synthesis/`, `qa/`, `reviews/`, and `phase-outputs/`; template defines `phase-outputs/{discovery,test-results,reviews,plans,reports}`. | Filesystem under `.dev/tasks/...`; downstream checklist items read by path. | Current task handoff convention lines 82-85; MDTM template handoff convention lines 718-731 and task overview lines 928-941. | Backlog.md can own associated docs/decisions; Mastra can own trace links to artifacts; Beads can point issues to artifact paths, not duplicate artifact bodies. | [UNVERIFIED target-stack assumption] |
| Sprint tasklist bundle | `tasklist-index.md` plus `phase-N-tasklist.md`, artifacts/evidence/checkpoints/validation/execution-log/feedback-log directories. | `sc-tasklist-protocol` output + Sprint CLI parser. | File emission rules at `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` lines 91-123; extracted rule file lines 7-59. | Backlog.md should likely map the index/phase markdown bundle into task/docs hierarchy; Beads mirrors `T<PP>.<TT>` nodes and dependency edges; Mastra executes phase/task workflow runs. | [UNVERIFIED target-stack assumption] |
| Roadmap item / deliverable traceability | `R-###` roadmap item IDs, `T<PP>.<TT>` task IDs, `D-####` deliverables, `D-CP...` checkpoint deliverables, traceability matrix. | Tasklist bundle index and phase files. | `sc-tasklist-protocol` lines 161-164, 291-300, 441-487, 647-653; index template lines 78-97. | Preserve IDs as cross-system stable keys: Backlog markdown IDs, Beads issue external IDs/labels, Mastra trace metadata. | [UNVERIFIED target-stack assumption] |
| Sprint phase | `Phase(number, file, name, execution_mode, prompt_preview)` discovered from index/directory and bounded by start/end config. | Sprint CLI config/parser. | `Phase` dataclass at `sprint/models.py` lines 281-309; discovery rules at `sprint/config.py` lines 52-140. | Mastra workflow stage/run group; Backlog.md phase document or milestone; Beads parent issue/epic. | [UNVERIFIED target-stack assumption] |
| Sprint task | `TaskEntry(task_id, title, description, dependencies, command, classifier)` parsed from phase markdown. | Sprint CLI parser plus phase markdown. | `TaskEntry` at `sprint/models.py` lines 24-37; parser extracts headings, dependencies, command, classifier at `sprint/config.py` lines 374-492. | Beads issue node for machine dependency graph; Backlog.md task body for prose; Mastra step/job for execution. | [UNVERIFIED target-stack assumption] |
| Pipeline step | `Step(id, prompt, output_file, gate, timeout_seconds, inputs, retry_limit, model, gate_mode, tool_write_mode, template_path)`. | Shared Python pipeline model. | `pipeline/models.py` lines 108-123. | Mastra workflow step equivalent; Backlog.md doc links for prompt/output; Beads optional only if step becomes schedulable work item. | [UNVERIFIED target-stack assumption] |
| Gate criteria | Required frontmatter, min lines, enforcement tier, semantic checks; gate mode blocking/trailing. | Shared Python pipeline model/executor/gates. | `GateCriteria` at `pipeline/models.py` lines 90-106; `GateMode` at lines 69-79. | Mastra scorer/validator or workflow branch; Backlog.md records gate reports; Beads records blocker edges only for failing gates that require work. | [UNVERIFIED target-stack assumption] |
| Runtime process run | `ClaudeProcess` constructs `claude --print --verbose ... --output-format <format>` and writes prompt over stdin, stdout/stderr to files. | Python process adapters. | `pipeline/process.py` lines 24-35 and 73-95; prompt via stdin lines 114-147; sprint subclass uses `output_format="stream-json"` at `sprint/process.py` lines 88-121. | Mastra runtime/agent tool invocation should eventually replace or wrap this seam; hybrid mode can call current Python/Claude subprocess. | [CODE-VERIFIED current seam; UNVERIFIED Mastra replacement] |

### Key Takeaways

- Current SuperClaude already separates several concepts that map cleanly to different ownership layers: human markdown task/doc artifacts, machine-readable task/phase/step models, execution traces/telemetry, and dependency metadata.
- Stable IDs (`TASK-*`, `T<PP>.<TT>`, `D-####`, `R-###`) are the best low-risk sync keys across Backlog.md, Beads, and Mastra because they already appear in current file formats and code parsers.
- The current runtime seam is verified as a Claude CLI subprocess wrapper; any target Mastra mapping must either wrap this seam first or replace it with a new model/provider adapter after parity gates.

## Model Group B: State, Status, Telemetry, and Quality Signals

### Inventory Table

| Concept | Current representation | Owner today | Evidence | Target mapping hypothesis | Assumption status |
|---|---|---|---|---|---|
| Task status | MDTM frontmatter status strings (`🟡 To Do`, `🟠 Doing`, `🟢 Done`, `⚪ Blocked`) and checkbox completion. | Markdown task file. | Template status fields lines 5, 447-451, 944-951; current task status line 5. | Backlog.md should own canonical human task status; Beads mirrors normalized status for graph/query; Mastra owns run-local step status. | [UNVERIFIED target-stack assumption] |
| Pipeline step status | `StepStatus` enum: `PENDING`, `PASS`, `FAIL`, `TIMEOUT`, `CANCELLED`, `SKIPPED`. | Pipeline execution result model. | `pipeline/models.py` lines 40-67. | Mastra step/run status; Backlog/Beads receive summarized outcomes after workflow events. | [UNVERIFIED target-stack assumption] |
| Sprint task status | `TaskStatus`: `PASS`, `FAIL`, `INCOMPLETE`, `SKIPPED`. | Sprint runtime result model. | `sprint/models.py` lines 39-54. | Mastra task-run result; Beads status update if task item is represented as issue; Backlog execution log for human record. | [UNVERIFIED target-stack assumption] |
| Gate outcome | `GateOutcome`: `PASS`, `FAIL`, `DEFERRED`, `PENDING`; display lifecycle adds `CHECKING`, `FAIL_DEFERRED`, `REMEDIATING`, `REMEDIATED`, `HALT`. | Sprint runtime and TUI display model. | `sprint/models.py` lines 56-124. | Mastra scorer/evaluation lifecycle; Backlog gate report; Beads blocker issue for unresolved fail/halt. | [UNVERIFIED target-stack assumption] |
| Phase status | `PhaseStatus`: pending/running/pass variants/prefight/missing-checkpoint/incomplete/halt/timeout/error/skipped. | Sprint runtime. | `sprint/models.py` lines 211-270. | Mastra workflow stage status; Backlog phase doc status; Beads parent issue status. | [UNVERIFIED target-stack assumption] |
| Sprint outcome | `SprintOutcome`: `SUCCESS`, `HALTED`, `INTERRUPTED`, `ERROR`. | Sprint aggregate result. | `sprint/models.py` lines 272-279. | Mastra workflow run terminal state; Backlog release decision/status; Beads root issue state. | [UNVERIFIED target-stack assumption] |
| Execution logs | `execution-log.jsonl`, `execution-log.md`, `results/phase-*-output.txt`, `results/phase-*-errors.txt`, `phase-*-result.md`, per-task output/error files. | Filesystem under release dir. | SprintConfig path properties at `sprint/models.py` lines 473-510; tasklist target directory layout lines 106-123. | Mastra traces/logs can own event stream; Backlog.md can retain summarized execution log; Beads should store pointers and outcome metadata only. | [UNVERIFIED target-stack assumption] |
| Monitor telemetry | `MonitorState` captures bytes, last event/growth times, activity log, turns, errors, assistant text, task progress estimate, token counts. | Sprint monitor/TUI runtime state. | `sprint/models.py` lines 622-690. | Mastra traces/observability should own time-series/runtime telemetry if validated; Backlog/Beads should not own high-volume telemetry except summaries. | [UNVERIFIED target-stack assumption] |
| Turn/economic ledger | `TurnLedger(initial_budget, consumed, reimbursed, reimbursement_rate, minimum_allocation, remediation budget, wiring budget metrics)`. | Sprint runtime budget model. | `sprint/models.py` lines 692-777. | Mastra run metadata/cost accounting or separate governance service; Backlog/Beads receive summarized budget outcomes only. | [UNVERIFIED target-stack assumption] |
| Checkpoint manifest | `CheckpointEntry(phase, name, expected_path, exists, recovered, recovery_source)` plus checkpoint report path conventions. | Sprint checkpoints module + filesystem reports. | `sprint/models.py` lines 311-341; tasklist checkpoint report path conventions at `sc-tasklist-protocol/SKILL.md` lines 343-391 and phase template lines 101-125. | Backlog.md owns checkpoint reports as docs; Mastra verifies/generates reports during workflow; Beads maps checkpoint task dependencies when checkpoints block follow-on work. | [UNVERIFIED target-stack assumption] |
| Remediation signals | `StepResult.remediated`, `remediations`; cosmetic remediator protocol. | Pipeline result model/executor. | `pipeline/models.py` lines 17-37 and 126-145. | Mastra remediation branch metadata; Backlog validation report/patch checklist; Beads follow-up issue only if remediation becomes human work. | [UNVERIFIED target-stack assumption] |

### Key Takeaways

- Current state is split between durable markdown/filesystem artifacts and runtime dataclasses. A target stack should not collapse these into one database without clear ownership rules.
- High-volume telemetry (`MonitorState`, stdout/stderr, stream events) belongs in the workflow/tracing layer, not task-of-record markdown or issue graph.
- Budget/cost attribution is currently a sprint-local `TurnLedger`; multi-tenant migration likely needs a stronger owner than Backlog.md or Beads. Mastra may help, but this is explicitly unverified until Phase 4 validates Mastra governance/observability capabilities.

## Model Group C: Tasklist Generation and Sprint Parser Contract

### Current Contract Table

| Contract surface | Current rule | Evidence | Ownership implication |
|---|---|---|---|
| Phase file discovery names | Sprint accepts `phase-N-tasklist.md`, `pN-tasklist.md`, `phase_N_tasklist.md`, and `tasklist-pN.md`; tasklist generator mandates canonical `phase-N-tasklist.md`. | Parser pattern at `sprint/config.py` lines 15-26 and 120-140; generator rule at `sc-tasklist-protocol/SKILL.md` lines 91-103. | Backlog.md adapter should emit canonical names only; Beads/Mastra should not introduce alias drift. |
| Execution mode | Index phase table may include `Execution Mode`; allowed values are `claude`, `python`, `skip`; default is `claude`. | `discover_phases` table parsing at `sprint/config.py` lines 67-119. | Mastra adapter could map execution mode to provider/runner selection; Backlog.md stores it in phase metadata; Beads likely stores as label/property. |
| Task heading format | Sprint parser expects `### T<PP>.<TT> -- Title` or dash/em-dash variant; tasklist protocol emits `### T<PP>.<TT> -- <Task Title>`. | Parser regex at `sprint/config.py` lines 374-377; protocol lines 291-300 and 860-865. | This is a stable external ID contract. Preserve verbatim across adapters. |
| Task dependency extraction | Parser reads `**Dependencies:**` and extracts `T<PP>.<TT>` references. | `sprint/config.py` lines 379-384 and 435-442. | Beads is the natural owner of queryable dependency graph, but Backlog.md should retain original dependency text for review. |
| Python execution command | Parser reads `**Command:**`; python-mode tasks must have command or parse fails. | `sprint/config.py` lines 386-390 and 443-479. | Mastra adapter needs a command-runner contract if preserving python/skip modes; Backlog.md stores command text; Beads marks executable type. |
| Classifier extraction | Parser reads a markdown table row `| Classifier | value |`. | `sprint/config.py` lines 392-396 and 449-453. | Classifier can map to Beads labels and Mastra routing metadata. |
| Description extraction | Parser derives `description` from the `**Deliverables:**` block. | `sprint/config.py` lines 455-473. | Avoid divergent descriptions across systems; Backlog.md task body should remain canonical prose. |
| Total task count | Sprint pre-scan counts `### T<PP>.<TT>` headings. | `count_tasks_in_file` at `sprint/config.py` lines 28-49 and config total lines 328-356. | Beads graph count and Mastra planned steps should be reconciled against parser-visible headings. |
| Release dir resolution | If index is inside `tasklist`, `tasklists`, or `tasks` and grandparent has `.roadmap-state.json` or spec/requirements file, release_dir resolves to grandparent; otherwise index parent. | `_resolve_release_dir` at `sprint/config.py` lines 236-272. | Adapter must preserve release-root semantics or explicitly migrate artifact path rules. |
| Checkpoint shape conflict | `sc-tasklist-protocol` current SKILL says checkpoints are numbered task headings; the extracted `phase-template.md` still includes older sibling `### Checkpoint:` guidance under inline checkpoints and mandatory end-of-phase sections. | Current SKILL lines 343-391 and 947-1027 vs `templates/phase-template.md` lines 101-125. | [CODE-CONTRADICTED within skill package docs] Backlog/Beads adapters must follow current SKILL numbered checkpoint task form if generating sprint-compatible bundles; the extracted template appears stale. |

### Key Takeaways

- The sprint parser imposes a narrow compatibility contract that any Backlog.md or Beads adapter must respect if `superclaude sprint run` remains a consumer.
- There is an internal documentation conflict in `sc-tasklist-protocol`: the main SKILL.md says checkpoint tasks are numbered `### T... -- Checkpoint` entries, while the extracted phase template still documents sibling `### Checkpoint:` sections. Treat the main SKILL.md and Sprint parser behavior as stronger current evidence, and list the template conflict under stale documentation.
- A target adapter should provide a parser compatibility test that round-trips Backlog/Beads/Mastra task state back to `tasklist-index.md` + `phase-N-tasklist.md` and verifies `parse_tasklist_file()` can read every task.

## Ownership Matrix

| Data / artifact class | Current primary owner | Proposed primary target owner | Proposed secondary/mirror owners | Sync direction | Rationale / boundary |
|---|---|---|---|---|---|
| Human-readable task body, acceptance criteria, checklist instructions, decisions | `.dev/tasks` / tasklist markdown | Backlog.md | Mastra trace links, Beads metadata | Backlog.md → adapters | Markdown is already the canonical human contract; do not make issue graph or workflow trace the prose source of truth. [UNVERIFIED target-stack assumption] |
| Machine dependency graph (`depends_on`, `Txx.yy` edges, blockers) | Markdown frontmatter + `**Dependencies:**` text | Beads | Backlog.md retains visible dependency text; Mastra reads graph for scheduling | Backlog.md/tasklist → Beads; Beads may propose graph patches | Queryable dependencies are graph-native; however, human-visible markdown should remain reviewable. [UNVERIFIED target-stack assumption] |
| Workflow run state, retries, step status, model/provider calls, traces | Python dataclasses/process outputs | Mastra | Backlog.md summaries; Beads issue status updates | Mastra → Backlog/Beads summaries | Runtime state is eventful/high-volume and should not be duplicated as long markdown/issue bodies. [UNVERIFIED target-stack assumption] |
| Execution outputs, logs, checkpoint reports, validation reports | Files under release/task workspace | Backlog.md docs or artifact files with Mastra trace references | Beads links only | Mastra/file outputs → Backlog docs; Beads stores pointers | Current system uses file paths for auditability; target should preserve linkable artifacts. [UNVERIFIED target-stack assumption] |
| Gate definitions and enforcement tiers | Python models + skill protocols | Mastra workflow/scorer layer for execution; Backlog.md for policy docs | Beads fail/remediation issues | Backlog policy → Mastra config; Mastra outcomes → Backlog/Beads | Gate policy must remain inspectable; execution/evaluation belongs in workflow. [UNVERIFIED target-stack assumption] |
| Stable IDs and traceability (`TASK-*`, `R-*`, `T*`, `D-*`, checkpoint IDs) | Markdown/tasklist generator | Shared cross-system IDs; Backlog.md should assign/preserve canonical external IDs | Mastra and Beads store IDs as metadata | Backlog/tasklist → all | IDs are the contract for reconciliation and drift detection. [CODE-VERIFIED current IDs; target uncertain] |
| Model/provider selection, permissions, execution mode | Sprint/pipeline configs and process adapter | Mastra/provider adapter registry | Backlog visible config, Beads labels | Backlog config → Mastra runtime | Current `PipelineConfig` and `SprintConfig` expose `model`, `permission_flag`, `max_turns`, and execution mode; target needs an explicit provider policy boundary. [CODE-VERIFIED current fields; target uncertain] |
| Multi-tenant auth/RBAC/cost attribution | Not represented in scoped current models beyond budget ledger | Unresolved: Mastra EE/governance service candidate | Backlog/Beads permissions if available | TBD | Seed brief makes multi-tenancy strategic, but current scoped code only proves runtime budget ledger, not tenant auth/RBAC. [UNVERIFIED] |

### Ownership Rules to Preserve During Migration

1. **One prose owner:** Backlog.md or markdown task files should own the human-readable task/decision text. Mastra traces and Beads issues should link to or mirror summaries, not fork prose.
2. **One graph owner:** Beads can own normalized dependencies only if an adapter continuously reconciles back to visible tasklist dependency fields; otherwise graph drift will silently change execution order.
3. **One run owner:** Mastra should own run/trace state only after Phase 4 validates its durability, replay, and observability model. Until then, current Python result files remain the current source of truth.
4. **Stable IDs are non-negotiable:** Every adapter must preserve current IDs verbatim and never regenerate them on import/export.
5. **Checkpoint reports remain artifacts:** Checkpoints are both tasks and reports; the task node and the report body should not be conflated.

## Adapter Contract Sketches

### Contract 1: Current Tasklist Bundle → Backlog.md Markdown Import

| Field | Source | Backlog.md target field/doc | Notes |
|---|---|---|---|
| Tasklist root | `TASKLIST_ROOT` from index metadata or path | Project/board/release container | Preserve path in metadata for round-trip. |
| Phase | `phase-N-tasklist.md` + `# Phase N -- Name` | Milestone/list/doc section | Sprint parser extracts name from H1 via `_extract_phase_name()` at `sprint/config.py` lines 143-154. |
| Task ID/title | `### T<PP>.<TT> -- Title` | Task key/title | Preserve ID as external ID, not display-only text. |
| Task body | Metadata table, artifacts, deliverables, steps, AC, validation, notes | Markdown body | Backlog.md should be prose owner. |
| Dependencies | `**Dependencies:** Txx.yy` | Dependency metadata + body text | Also exported to Beads. |
| Checkpoints | Numbered checkpoint tasks with `Checkpoint Report Path` | Verification task + linked doc | Use current SKILL.md checkpoint-task form, not stale phase-template sibling checkpoint form. |

Validation contract: import must export back to files such that `discover_phases()` and `parse_tasklist_file()` succeed and task counts match `count_tasks_in_file()`.

### Contract 2: Backlog.md / Tasklist → Beads Graph Sync

| Beads node/edge concept | Current source | Sync behavior | Conflict rule |
|---|---|---|---|
| Root issue/project | Tasklist root or MDTM parent task ID | Create/update by stable external ID | Backlog/tasklist wins for existence and title. |
| Phase parent | Phase number/name | Create parent issue/epic with `phase_number` metadata | Backlog/tasklist wins for phase order. |
| Task issue | `T<PP>.<TT>` and title | Create/update issue with status, tier, risk, classifier, deliverable IDs | Backlog/tasklist wins for title/body; Beads can own status only if explicitly configured. |
| Dependency edge | `TaskEntry.dependencies` | Upsert directed edges `dependency -> dependent` | If Beads graph diverges, write a proposed patch report; do not silently rewrite markdown. |
| Checkpoint node | `D-CP...` / checkpoint task | Create verification node linked to covered tasks | Checkpoint must not be treated as a regular implementation dependency unless it blocks next phase. |
| Artifact pointer | `TASKLIST_ROOT/artifacts`, `checkpoints`, evidence paths | Store path/URL metadata only | Never duplicate full artifact body into graph by default. |

Validation contract: graph export must produce a dependency list identical to parser-extracted `TaskEntry.dependencies` unless a human-approved graph patch exists.

### Contract 3: Backlog.md / Beads → Mastra Workflow Plan

| Mastra plan element | Source | Mapping rule | Open validation need |
|---|---|---|---|
| Workflow | Tasklist root / sprint config | One workflow per sprint/release/tasklist bundle. | Confirm Mastra supports required loops/checkpoints/retries. |
| Stage/group | Phase | One sequential stage per phase; phase execution mode selects runner type. | Confirm Mastra can represent sequential phases with resumable checkpoints. |
| Step/job | Task ID or pipeline `Step` | Use `T<PP>.<TT>` as step external ID; pipeline `Step.id` for generic pipeline workflows. | Confirm Mastra step metadata and trace APIs. |
| Inputs | Artifact paths + prior phase outputs + dependencies | Resolve from Backlog.md body and Beads graph. | Confirm filesystem/artifact integration. |
| Gate | Tier/gate criteria/checkpoint task | Blocking/trailing gate branch, scorer, or validation step. | Confirm Mastra evaluator/scorer semantics. |
| Trace metadata | `R-*`, `T*`, `D-*`, phase, tier, model, permission flag, max turns | Attach to every run/span. | Confirm trace schema and query support. |
| Provider invocation | Current ClaudeProcess or new provider adapter | Hybrid: call existing Python CLI first; native: invoke model/tool adapter. | Confirm support for multiple agent CLIs/models and subprocess/tool wrappers. |

Validation contract: workflow plan generation must be deterministic from Backlog.md + Beads graph and produce a dry-run plan with task order, gates, expected artifacts, and provider commands before execution.

### Contract 4: Mastra Run Results → Backlog.md and Beads Reconciliation

| Run result | Backlog.md update | Beads update | Current equivalent |
|---|---|---|---|
| Step PASS | Append/summarize execution log entry; mark task done if configured | Set issue status/pass or close | `TaskResult.status=PASS`, `StepStatus.PASS`. |
| Step FAIL/INCOMPLETE | Add failure note, gate report, artifact links | Mark blocked/failed and edge to remediation issue | `TaskStatus.FAIL/INCOMPLETE`, `gate_failure_reason`. |
| Gate DEFERRED/TRAILING | Add gate report with deferred status | Add advisory/remediation relation only if action needed | `GateOutcome.DEFERRED`, `GateDisplayState.FAIL_DEFERRED`. |
| HALT | Add sprint/phase halt report and resume command | Set root/phase issue blocked | `PhaseStatus.HALT`, `SprintOutcome.HALTED`, `build_resume_output()`. |
| Checkpoint report written | Link checkpoint doc; update checkpoint task status | Close/check verification node | `CheckpointEntry.exists=True`, checkpoint report path. |
| Telemetry/cost | Summarized budget/token line only | Optional labels/metrics; avoid high-volume data | `MonitorState`, `TurnLedger`. |

Validation contract: reconciliation must be idempotent; re-running the same Mastra result event must not duplicate Backlog log rows or Beads comments/edges.

## Mapping to Final Report Sections

| Report section | Findings contributed by this research |
|---|---|
| Section 3 — Target state | Proposed split: Backlog.md as prose/task/doc owner, Beads as dependency graph mirror/owner, Mastra as workflow run/traces owner; all target-stack capabilities remain assumptions pending web validation. |
| Section 4 — Gap analysis | Current state lacks explicit multi-tenant ownership model, has file-vs-runtime state split, has checkpoint documentation conflict, and has no validated target-stack adapter contracts yet. |
| Section 6 — Options | Hybrid adapter-first is favored by data-model risk: preserve markdown/file current contracts while adding graph/workflow adapters; native Mastra rewrite is higher-risk because it must replace subprocess, parser, telemetry, gates, and artifact ownership at once. |
| Section 7 — Recommendation | Recommend deciding task-of-record first; do not proceed to native workflow rewrite until Backlog/Beads/Mastra ownership boundaries and round-trip parser compatibility tests are proven. |
| Section 8 — Roadmap | Pilot sequence should be: ID/schema inventory → tasklist import/export → Beads graph mirror → Mastra dry-run planner → hybrid execution wrapper → native provider/gate migration only after parity. |

## High-Level Migration Implications

1. **Start with read-only adapters.** Build importers that read existing `.dev/tasks` and tasklist bundles into target metadata without changing the current files. This reduces risk while proving ID, graph, and artifact mapping.
2. **Add round-trip tests before any ownership transfer.** The sprint parser is strict enough that adapter drift will break execution. Use `discover_phases()`, `parse_tasklist_file()`, task counts, and dependency comparison as acceptance gates.
3. **Treat Backlog/Beads overlap as a product decision, not a technical afterthought.** If both can represent tasks, decide which one owns status, title, body, dependency edits, comments, and decisions before implementation.
4. **Keep current Python orchestration as the execution oracle during pilot.** The verified runtime seam can be wrapped; replacing it should wait until Mastra execution and trace capabilities are externally validated.
5. **Promote cost/tenant policy to a first-class model.** Current `TurnLedger` is not enough for company-wide multi-tenant governance; target design needs tenant, actor, provider, budget, permission, audit, and billing dimensions.

## Gaps and Questions

| Gap / question | Evidence / status | Why it matters |
|---|---|---|
| Can Mastra natively express SuperClaude's phase/task/checkpoint/gate loops, retries, trailing gates, and long-running subprocess wrappers? | [UNVERIFIED] Current code proves pipeline/sprint models and Claude subprocess seam, but Phase 4 must validate Mastra workflow/runtime capabilities. | Determines whether hybrid wrapper or native reimplementation is feasible. |
| Does Mastra OSS or EE own multi-tenant auth/RBAC/cost governance? | [UNVERIFIED] Seed brief line 31 claims Mastra EE auth/RBAC facts but this report did not web-validate them. | Strategic driver is company-wide multi-tenant orchestration; licensing/governance can decide go/no-go. |
| What exactly are Backlog.md's task/docs/decision schema and metadata extension points? | [UNVERIFIED] Mapping assumes markdown task/doc ownership but Phase 4 must verify Backlog.md current capabilities. | Determines whether Backlog.md can preserve MDTM/tasklist richness without lossy translation. |
| What exactly are Beads' issue/dependency graph schema, JSON contract, multi-writer behavior, and server/storage modes? | [UNVERIFIED] Mapping assumes Beads can mirror dependencies and issue metadata. | Determines whether Beads should be graph owner or only an auxiliary memory/index. |
| Backlog.md vs Beads status ownership remains unresolved. | [UNVERIFIED target decision] Current code has status in markdown/frontmatter and runtime models, not a graph DB. | Dual status owners will create drift unless one is canonical. |
| Current checkpoint documentation conflicts inside `sc-tasklist-protocol`. | [CODE-CONTRADICTED] Main `SKILL.md` lines 343-391 and 947-1027 define numbered checkpoint tasks; extracted `templates/phase-template.md` lines 101-125 still define sibling `### Checkpoint:` sections. | Adapter generation must know which shape to emit for sprint compatibility. |
| Current sprint `build_prompt()` still instructs agents to scan for sibling `### Checkpoint:` sections. | [CODE-CONTRADICTED / needs follow-up] `sprint/process.py` lines 187-195 mentions `### Checkpoint:` sections, while current tasklist protocol says checkpoint tasks are numbered headings. | Potential current-code/protocol drift: checkpoint reports may be skipped if generated as numbered tasks unless executor/checkpoint code handles both forms elsewhere. Requires dedicated sprint/checkpoint validation beyond this report's scope. |
| Target artifact storage policy is unresolved. | [UNVERIFIED target decision] Current code stores outputs and reports as files under task/release directories. | Mastra traces, Backlog docs, and Beads links need an artifact retention and deduplication policy. |
| Tenant/actor/audit identity is absent from scoped current dataclasses. | [CODE-VERIFIED absence in scoped model reads; broader repo not exhaustively searched] `PipelineConfig`, `SprintConfig`, `TaskResult`, `PhaseResult`, `MonitorState`, and `TurnLedger` have model/permission/budget fields but no tenant or actor fields in the read ranges. | Migration must add identity dimensions rather than assume existing models can carry multi-tenant context. |

## Stale Documentation Found

| Source | Stale / conflicting claim | Verification |
|---|---|---|
| `src/superclaude/skills/sc-tasklist-protocol/templates/phase-template.md` | Documents inline checkpoints as sibling `### Checkpoint:` sections and says every phase file must end with `### Checkpoint: End of Phase <N>`. | [CODE-CONTRADICTED] Current `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` says checkpoints are numbered task entries using `### T<PP>.<NN> -- Checkpoint:` at lines 343-391 and 947-1027. |
| `src/superclaude/cli/sprint/process.py` prompt text | Tells sprint subprocess to scan phase file for `### Checkpoint:` sections and skip checkpoint step if none exist. | [CODE-CONTRADICTED / needs broader code validation] This conflicts with current `sc-tasklist-protocol` numbered checkpoint task rule. It may be mitigated elsewhere by checkpoint verification code, but this scoped report did not validate that path. |
| `.dev/releases/backlog/mastra-beads-port-feasibility/seed-brief.md` Stack D facts | Claims Mastra 1.0/EE auth/RBAC, Backlog.md MCP alignment, Beads v1.0/SQLite/Dolt modes. | [UNVERIFIED external] Must be validated by Phase 4 web research before use in final recommendations. |
| `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/research/research-notes.md` option framing | Suggests Option A/B/C/D and target output mappings. | [UNVERIFIED target recommendation] Useful planning context, but target-stack and final recommendation claims require Phase 4 and synthesis validation. |

## Summary

This research maps current SuperClaude task/artifact/state concepts to a target ownership model: Backlog.md as the likely prose/task/doc/decision owner, Beads as the likely issue/dependency graph owner, and Mastra as the likely workflow run/tracing/gate execution owner. That split is an architecture hypothesis, not a validated target-stack fact; every Mastra/Backlog.md/Beads capability assumption must remain uncertain until Phase 4 web validation.

The current code provides strong, verified contracts to preserve: stable task/deliverable/roadmap IDs, tasklist bundle shapes, phase/task parser rules, shared pipeline step/gate models, sprint status/result/telemetry/budget models, and the Claude CLI subprocess seam. The safest migration path is adapter-first: read current markdown/tasklist files, preserve IDs, mirror dependencies into Beads, generate Mastra dry-run workflow plans, and only then attempt hybrid execution or native reimplementation.

The main immediate risk is ownership drift: Backlog.md and Beads can both plausibly represent tasks/status/dependencies, while Mastra can represent run state and task steps. The final feasibility report should require explicit source-of-truth decisions and idempotent sync contracts before any implementation roadmap proceeds.
