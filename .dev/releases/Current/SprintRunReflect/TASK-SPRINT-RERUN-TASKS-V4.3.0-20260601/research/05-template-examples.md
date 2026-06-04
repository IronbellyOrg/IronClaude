# Research 05 — Template & Examples

**Status:** Complete
**Researcher:** Agent #5
**Scope:** MDTM Template 02 rules + executable-impl task file examples + skeleton for sprint rerun-tasks task file
**Date:** 2026-06-01

---

## 1. Sources Examined

| Source | Path | Lines Read | Purpose |
|---|---|---|---|
| MDTM Template 02 PART 1 (rules) | `.claude/templates/workflow/02_mdtm_template_complex_task.md` | 1-806 | Sections A-L rules (granularity, self-contained items, phase gates, handoff patterns) |
| MDTM Template 02 PART 2 (template) | same | 807-1205 | Concrete section headers + frontmatter shape + Phase 1 boilerplate |
| Example A — full-cycle remediation | `.dev/tasks/to-do/TASK-MULTIMODELSWARM-AUDIT-REMEDIATION-20260531/TASK-MULTIMODELSWARM-AUDIT-REMEDIATION-20260531.md` | 1-379 | 5-phase remediation with Python source-code edits + pipeline re-run verification |
| Example B — large Python refactor (R0+R1) | `.dev/tasks/to-do/TASK-RF-20260531-042405/TASK-RF-20260531-042405.md` | 1-120 + 260-365 | New dataclass/module creation, gate wiring, fixture/test creation, lint/format/QA gate pattern |
| task-builder skill (TB-Add catalogue) | `src/superclaude/skills/task-builder/SKILL.md` | 1165-1979 | TB-Add-1..8 structural pre-write gates |
| Sprint models (for example item grounding) | `src/superclaude/cli/sprint/models.py` | 35-87 | `TaskStatus`, `GateDisplayState` enums — the surface where `FAIL_RECOVERABLE` would land |

---

## 2. MDTM Template 02 PART 1 — Complete Rule Catalogue (with line citations)

### Section A — Core Principles
- **A1** (`02_mdtm_template_complex_task.md:72-83`): Workflow document availability check — omit WORKFLOW-DEPENDENT sections if no governing workflow exists.
- **A2** (`:85-89`): Deep integration with workflow doc (WORKFLOW-DEPENDENT).
- **A3 — COMPLETE GRANULAR BREAKDOWN** (`:91-95`): "Break down EVERY workflow phase into atomic, verifiable checklist items … NO high-level or bulk operations allowed." Exact paths + measurable outcomes required per item.
- **A4 — ITERATIVE PROCESS STRUCTURE** (`:97-116`): For any multi-item process: pre-enumerate ALL items (Step X.1), one checklist item per specific item (Step X.2 ... Step X.N), consolidation step at end (Step X.last). Never bulk a "process all files" item.
- **A5/A6** (`:118-128`): Cross-stage integration + workflow compliance enforcement (WORKFLOW-DEPENDENT).

### Section B — Self-Contained Items (CRITICAL, `:130-196`)
- **B1**: Session rollover protection — every item must embed all context references because batch 1 context is not available in batch 3+. Standalone "read context" items are USELESS.
- **B2 — 6-element schema** (`:142-148`): every item MUST include:
  1. **Context Reference with WHY** — what files + why the context is needed
  2. **Action with WHY** — what to do + why
  3. **Output Specification** — exact file name/location/content + template if any
  4. **Integrated Verification** — `ensuring …` clause (no fabrication, derived from source)
  5. **Evidence on Failure Only** — log to Task Notes ONLY on blocker
  6. **Explicit Completion Gate** — "This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete."
- **B3** (`:150-154`): Each item is ONE FULL PARAGRAPH — verbose, explanatory, no bullets or multi-line within an item.
- **B4** (`:155-163`): Correct example — single-paragraph item with action + integrated `ensuring …`. Verification is INSIDE the action item.
- **B5 — Forbidden patterns** (`:164-184`):
  - Standalone "read context" with no output
  - Missing context reference (no source of truth)
  - Multi-line / bulleted checklist items
  - Separate verification/confirmation items (must use `ensuring …` integration)
  - Overly granular items (e.g. "create directory" alone — combine with the file it serves)
  - Separate REMINDER blocks between items
- **B6/B7** (`:185-196`): Preferential context source + output spec; key principles — one complete prompt that executes independently.

### Section C — Embedding Requirements (`:198-230`)
- **C1**: Outputs/deliverables embed IN items (not separate "Outputs" section).
- **C2**: Success criteria embed as `ensuring …` clauses (not separate criteria).
- **C3**: Verification embeds in action items, NEVER separate.
- **C4**: Task completion = Post-Completion Actions section only (frontmatter update + log + Task Summary). No "Task Completion and Handoff Protocol" section.

### Section D — Mandatory Sections (`:232-273`)
- **D1**: Workflow Compliance Declaration (WORKFLOW-DEPENDENT, informational only).
- **D2**: Cross-Stage Integration Requirements (INFORMATIONAL ONLY — actual checklist items appear in Phase 1).
- **D3 — CRITICAL RULE**: NO checklist items may appear before Phase 1 begins. Order: Frontmatter → Workflow Compliance (info) → Prerequisites (info) → Phase 1 (executable).

### Section E — Checklist Structure Rules (`:275-388`)
- **E1**: Every actionable item = checkbox; NO nested checkboxes; NO parent checkboxes summarizing children; use `**Step X.Y:**` headers (no checkbox) for grouping.
- **E2 — FUNDAMENTAL**: Summary/parent checkboxes ALWAYS come AFTER component items. Use descriptive headers for grouping, not parent checkboxes.
- **E3 — Sequential**: Top-to-bottom only. Forbidden: "go back and update", "see below", parent-with-children, summary-before-components, backward-movement to mark complete.
- **E4**: Step numbers are bold headings (no checkbox). Checkboxes ONLY on actionable items. No separate REMINDER blocks between items.

### Section F — Execution (for worker agents) (`:390-451`)
- **F1**: READ → IDENTIFY → EXECUTE → UPDATE → REPEAT (single-item loop).
- **F2**: Prohibited — working from memory, executing multiple items at once, skipping phases, delegating across phase boundaries, skipping phase-gate QA, skipping post-completion validation (I17).
- **F2a — Item Execution Discipline**: Multi-item execution = identifying multiple unchecked items + executing >1 before returning to READ. Parallel-spawning exception only when consecutive items spawn INDEPENDENT subagents.
- **F4**: Worker may ONLY mark items `[x]`, update frontmatter per protocol, add to Task Log, or fill DYNAMIC CONTENT MARKERs.
- **F5**: Frontmatter — on start (`🟠 Doing` + start_date), on done (`🟢 Done` + completion_date), on block (`⚪ Blocked` + blocker_reason), each session (updated_date).

### Section G — Context for Headless Agents (`:453-469`)
- Framework files (ib_agent_core.md, anti_hallucination_rules.md, etc.) NOT auto-loaded. Either reference rule file in item OR reference template that incorporates conventions (preferred).

### Section H — Tool Specification (`:471-490`)
- H1-H4: Default = let model pick tools; specify a tool ONLY when a specific tool is required (with why); examples — `Bash` for `npm test`, `Glob` for file pattern matching.

### Section I — Additional Guidelines (`:492-650`)
- **I1**: Use "YOU MUST" / "DO NOT" (explicit directive language).
- **I2**: Extreme granularity — exact file paths, exact content, no ambiguity.
- **I3**: Incremental file modification — never "complete entire files at once"; require save points after major sections.
- **I9**: Hallucination prevention — repeat "DO NOT assume, hallucinate, or make up any information" at content-creation points.
- **I12** (`:573-579`): Verification IS INTEGRATED — `ensuring …` clause in the action, not a separate item.
- **I13**: Post-Completion Actions — final task items only (frontmatter update + log + task summary).
- **I14**: Anti-hallucination controls — evidence tables for technical claims; negative-evidence documentation.
- **I15 — PHASE-GATE QA ENFORCEMENT** (`:599-607`): every task with 2+ phases MUST insert at least one phase-gate between primary execution and any dependent phase. Gate = (1) Aggregation item (L6) collecting outputs, (2) QA agent spawn item (rf-qa / rf-qa-qualitative) with binary PASS/FAIL, (3) Conditional-action item (L5) proceeding on PASS or triggering fix cycle on FAIL.
- **I16 — Fix cycle caps** (`:609-624`):
  | Gate Type | Max Cycles | After Max |
  |---|---|---|
  | research-gate | 3 | HALT + escalate |
  | synthesis-gate | 2 | Open Questions |
  | report-validation | 3 | HALT + escalate |
  | task-integrity | 2 | Open Questions |
  | Any qualitative gate | 3 | HALT + escalate |
- **I17 — POST-COMPLETION VALIDATION** (`:626-635`): Before status→Done, validate (1) all `[ ]` are `[x]`, (2) all output files exist on disk (Glob), (3) blocker entries have resolution notes, (4) all relevant tests pass.
- **I18 — TESTING for code-modifying tasks** (`:637-646`): MUST include ≥1 testing item with command, pass criteria, output capture path, B2-pattern. Use L3 (Test/Execute) pattern.

### Section J — Error Handling (`:651-673`)
- **J1**: Standard embedded pattern: "If unable to complete due to missing information, file access issues, or unclear requirements, log the specific blocker using the templated format in the ### Phase [N] Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete."
- **J2/J3**: Items are NEVER left unchecked. Block whole task only if ALL remaining items share the same blocker.

### Section K — Example Patterns (`:675-708`)
- **K1**: File-by-file processing — per-file self-contained item using `#### File: [filename]` header.
- **K2**: Multi-item processing — orchestrator MUST pre-enumerate ALL items at build time; worker NEVER dynamically adds items.

### Section L — Intra-Task Handoff Patterns (Template 02 unique, `:710-836`)
Handoff convention (`:718-730`): items write outputs to `.dev/tasks/TASK-NAME/phase-outputs/` with subdirectories `discovery/`, `test-results/`, `reviews/`, `plans/`, `reports/`. Files persist across batches.

- **L1 — DISCOVERY** (`:737-747`): item explores codebase/env and writes structured findings; the discovery file IS the deliverable. Example: Glob TS files → write `handler-inventory.md`.
- **L2 — BUILD-FROM-DISCOVERY** (`:749-759`): reads discovery file + source file, creates output. Always cite BOTH discovery path AND source path.
- **L3 — TEST/EXECUTE** (`:761-771`): runs command via Bash, captures BOTH raw output + structured summary. Example: `cd /project && python -m pytest tests/ -v 2>&1` → write `pytest-output.txt` + `test-summary.md`.
- **L4 — REVIEW/QA** (`:773-783`): assesses quality, produces structured verdict (PASS/FAIL + per-criterion checklist + severity-classified issues + recommendation).
- **L5 — CONDITIONAL-ACTION** (`:785-797`): reads status/result file, takes different actions per branch — MUST handle BOTH success AND failure; output file always created regardless of branch.
- **L6 — AGGREGATION** (`:799-809`): Glob to find all relevant outputs (don't hardcode), consolidate into a single report.

**Pattern Selection Guide (`:811-836`)** — common composites:
- Discovery → Build → Review: `L1 → L2 (per item) → L4 (per item) → L6`
- Build → Test → Fix: `K1/K2 → L3 → L5`
- Full Lifecycle: `L1 → L2 → L3 → L5 → L4 → L6`
- Full Lifecycle with QA Gates: `L1 → L2 → M1 (QA Gate) → L3 → L5 → L4 → L6 → M1 (QA Gate)`

### Section M — Phase-Gate Composite Patterns (`:838-860`)
- **M1 — PHASE-GATE QA SEQUENCE**: 3 items (Aggregation L6 → QA Agent Spawn → Conditional-Proceed L5). QA spawn item embeds: agent name (rf-qa / rf-qa-qualitative), phase type, input paths, output report path, verdict handling, error clause. Qualitative QA runs in a SEPARATE item AFTER structural passes.
- **M2 — Applicability**: code-modifying tasks need a gate after implementation phase before testing (if separate). Task-building tasks need research-gate + task-integrity gate.

---

## 3. PART 2 — Concrete Section Order (the SKELETON)

From `02_mdtm_template_complex_task.md:890-1205`, the required output structure is:

```
---
<frontmatter>
---

# [Task Title]                                       (:890)

## Task Overview                                     (:892)
## Key Objectives                                    (:896)
## Prerequisites & Dependencies                      (:904)
  ### Parent Task & Dependencies                     (:906)
  ### Previous Stage Outputs (MANDATORY INPUTS)      (:914) [INFORMATIONAL ONLY]
  ### Handoff File Convention                        (:928)
  ### Frontmatter Update Protocol                    (:943)

## Detailed Task Instructions                        (:954)

### Phase 1: Preparation and Setup                   (:1012)
  **Step 1.1:** Update task status                   (:1044)
  - [ ] <status flip to 🟠 Doing + Execution Log entry>
  **Step 1.2:** Create handoff directories            (:1048)
  - [ ] <mkdir phase-outputs/{discovery,test-results,reviews,plans,reports}>
  [optional 1.3+ context-load items if not embedded]

### Task-Specific Context Files                       (:1052) [reference list, not checklists]

### Phase 2: [Main Execution Phase Name]              (:1063)
  **Step 2.1:** [Discovery] — L1 pattern
  **Step 2.2:** [Build] — L2 pattern (per item or K2 enumerated)
  **Step 2.3:** [Test] — L3 pattern
  **Step 2.4:** [Assess/Conditional] — L5 pattern
  …

### Phase Gate: Quality Verification                  (:1090)
  **Step PG.1** — L6 aggregation
  **Step PG.2** — rf-qa task-integrity spawn
  **Step PG.3** — L5 conditional proceed/fix-cycle

### Phase [N]: Testing & Verification                 (:1098)
  **Step N.1** — L3 test execution (per I18)

### Phase 3: Review and Quality Assessment            (:1106)
  **Step 3.1** — L4 per-item review
  **Step 3.2** — L6 aggregate reviews

## Post-Completion Actions                            (:1118)
  - [ ] Verify all outputs (Glob check)
  - [ ] Run test suite if code modified
  - [ ] Create Task Summary (in Task Log section)
  - [ ] Frontmatter update to 🟢 Done + completion_date + Execution Log entry

## Task Log / Notes 📋                               (:1128)
  ### Task Summary                                    (:1130) [filled in Post-Completion]
  ### Execution Log                                   (:1156)
  ### Phase 1 - [Name] Findings                       (:1166)
  ### Phase 2 - [Name] Findings                       (:1176)
  ### Phase 3 - [Name] Findings                       (:1185)
  ### Phase Gate Findings                             (:1187)
  ### Follow-Up Items Identified                      (:1191)
  ### Deviations from Process                         (:1197)
```

---

## 4. Generated Task File SKELETON for `superclaude sprint rerun-tasks` v4.3.0

This is the structure the task-builder should emit. **Sized for ~5-7 phases of executable Python work** (mirroring `TASK-RF-20260531-042405` shape — see `:266-365`).

### 4.1 Frontmatter (required fields, with realistic values)

```yaml
---
id: "TASK-SPRINT-RERUN-TASKS-V4.3.0-20260601"
title: "Sprint rerun-tasks v4.3.0 — surgical task rerun for sprint pipeline"
description: "Add `superclaude sprint rerun-tasks <tasklist-index> --task-id <ID>` subcommand that re-executes a single tasklist item (or set of items) within an in-flight sprint without re-running prior PASS tasks. Wires `FAIL_RECOVERABLE` outcome plus a `--from-checkpoint` resume path, persists rerun history to `.sprint-state.json`, and adds end-to-end coverage."
status: "🟡 To Do"
type: "✨ Feature"
priority: "🔼 High"
created_date: "2026-06-01"
updated_date: "2026-06-01"
assigned_to: ""
autogen: false
coordinator: orchestrator
parent_task: ""
depends_on: []
related_docs:
  - path: "<spec/PRD path from researcher-1>"
    description: "Authoritative spec for rerun-tasks v4.3.0"
  - path: "src/superclaude/cli/sprint/commands.py"
    description: "Existing sprint CLI surface — adds new `rerun-tasks` subcommand"
  - path: "src/superclaude/cli/sprint/executor.py"
    description: "Sprint executor — adds rerun entrypoint + skip-prior-PASS logic"
  - path: "src/superclaude/cli/sprint/models.py"
    description: "TaskStatus enum — adds FAIL_RECOVERABLE variant"
  - path: "src/superclaude/cli/sprint/checkpoints.py"
    description: "Checkpoint persistence — extends with rerun history"
  - path: "tests/sprint/<test files from researcher-4>"
    description: "Sprint test suite — adds rerun-tasks coverage"
  - path: ".dev/tasks/to-do/TASK-SPRINT-RERUN-TASKS-V4.3.0-20260601/research/01-file-inventory.md"
    description: "Researcher-1: every file the feature touches"
  - path: ".dev/tasks/to-do/TASK-SPRINT-RERUN-TASKS-V4.3.0-20260601/research/02-patterns-conventions.md"
    description: "Researcher-2: code conventions verified at file:line"
  - path: ".dev/tasks/to-do/TASK-SPRINT-RERUN-TASKS-V4.3.0-20260601/research/03-integration-points.md"
    description: "Researcher-3: call-site and CLI wiring points"
  - path: ".dev/tasks/to-do/TASK-SPRINT-RERUN-TASKS-V4.3.0-20260601/research/04-test-and-verification.md"
    description: "Researcher-4: pytest patterns, fixtures, CLI coverage strategy"
tags:
  - feature
  - sprint-cli
  - rerun
  - checkpoint
  - v4.3.0
template_schema_doc: ".claude/templates/workflow/02_mdtm_template_complex_task.md"
estimation: "~6 phases (Discovery→Models→Executor→CLI→Tests→QA Gate); ~30-40 items"
task_type: static
compliance_tier: STRICT
---
```

### 4.2 Body section headings (skeleton)

```markdown
# Sprint rerun-tasks v4.3.0 — surgical task rerun for sprint pipeline

## Task Overview
[2-3 paragraphs: what feature, why, what was the prior pain (e.g. T07.11/T07.12 had to manually re-run by hand), what is the end state]

## Key Objectives
1. Add `FAIL_RECOVERABLE` variant to `TaskStatus` enum (`src/superclaude/cli/sprint/models.py`).
2. Add `superclaude sprint rerun-tasks` subcommand to `commands.py`.
3. Wire `--task-id` selector + `--from-checkpoint` resume path in `executor.py`.
4. Persist rerun history to `.sprint-state.json` via `checkpoints.py`.
5. Skip prior-PASS tasks on rerun unless `--force-all` is set.
6. End-to-end coverage: unit tests for new enum + executor branches, CLI smoke test, fixture-based integration test.

## Prerequisites & Dependencies
### Parent Task & Dependencies
- **Parent Task:** None
- **Blocking Dependencies:** None (research complete: see researcher-1..4 outputs)
- **This task blocks:** v4.3.0 release of sprint pipeline (T07.11/T07.12 manual rerun workflow)

### Previous Stage Outputs (MANDATORY INPUTS)
**INFORMATIONAL ONLY - NO CHECKLIST ITEMS HERE**
- Researcher-1 file inventory: <path>
- Researcher-2 patterns/conventions: <path>
- Researcher-3 integration points: <path>
- Researcher-4 test plan: <path>

### Handoff File Convention
`.dev/tasks/TASK-SPRINT-RERUN-TASKS-V4.3.0-20260601/phase-outputs/{discovery,test-results,reviews,plans,reports}/`

### Frontmatter Update Protocol
[Standard 4-checkpoint protocol from template :943-952]

## Execution Context
- **References:** R-001..R-004 → researcher 1..4 outputs
- **Source areas:** sprint CLI subcommand surface (`commands.py`), executor entrypoint (`executor.py`), TaskStatus enum (`models.py`), checkpoint persistence (`checkpoints.py`), pytest sprint suite (`tests/sprint/`)
- **Key constraints:** UV-only Python ops; `src/superclaude/` source-of-truth (never edit `.claude/` directly); single-line bash in commands (terminal limitation); preserve all existing TaskStatus enum members + existing CLI subcommands (additive only)

---

## Phase 1: Preparation and Setup
**Step 1.1** — [ ] Update task status to 🟠 Doing + log to Execution Log [standard frontmatter flip item from template :1046]
**Step 1.2** — [ ] Create phase-outputs directories [standard from :1050]
**Step 1.3** — [ ] Read all 4 researcher outputs and confirm scope — [L1 light discovery item that writes `phase-outputs/discovery/scope-confirmation.md` reconciling researcher 1-4 outputs into a single integration table]

---

## Phase 2: Models layer — add FAIL_RECOVERABLE to TaskStatus
**Step 2.1** — [ ] Add FAIL_RECOVERABLE variant to `TaskStatus` enum (SEE §4.3 below for FULL ITEM BODY)
**Step 2.2** — [ ] Update `is_failure` / `is_recoverable` properties on `TaskStatus`
**Step 2.3** — [ ] Add unit tests for new enum member in `tests/sprint/test_models.py`
**Step 2.4** — [ ] Run pytest + ruff on models layer; capture results [L3 pattern]
**Step 2.5** — [ ] Aggregate Phase 2 outputs [L6 light]

### Phase Gate: Phase 2 Quality Verification
**Step PG2.1** — [ ] L6 aggregation
**Step PG2.2** — [ ] Spawn rf-qa in `task-integrity` mode (verify enum additivity, no member rename, all properties cover new variant)
**Step PG2.3** — [ ] L5 conditional — PASS proceeds to Phase 3; FAIL triggers fix cycle (max 2 cycles per I16 task-integrity)

---

## Phase 3: Checkpoint layer — extend .sprint-state.json schema
**Step 3.1** — [ ] L1 Discovery — Read `checkpoints.py` and `.sprint-state.json` shape; inventory existing fields
**Step 3.2** — [ ] Add `rerun_history: list[dict]` field to checkpoint schema; backward-compat default `[]`
**Step 3.3** — [ ] Add `record_rerun()` helper writing `{task_id, timestamp, prior_status, new_status}`
**Step 3.4** — [ ] Unit tests + pytest run
**Step 3.5** — [ ] L6 aggregate

### Phase Gate: Phase 3 Quality Verification
(same M1 pattern as PG2)

---

## Phase 4: Executor layer — rerun entrypoint + skip-prior-PASS gate
**Step 4.1** — [ ] L1 Discovery — read `executor.py` to extract current `run_pipeline` entrypoint shape + checkpoint-load path
**Step 4.2** — [ ] Implement `rerun_tasks(tasklist_path, task_ids, force_all=False, from_checkpoint=True)` function
**Step 4.3** — [ ] Wire FAIL_RECOVERABLE return path for the rerun subset (prior PASS untouched)
**Step 4.4** — [ ] Unit tests for executor branches (rerun-single, rerun-multiple, --force-all, --from-checkpoint=false)
**Step 4.5** — [ ] L3 — run pytest for executor + lint
**Step 4.6** — [ ] L6 aggregate

### Phase Gate: Phase 4 Quality Verification (M1)

---

## Phase 5: CLI surface — `sprint rerun-tasks` subcommand
**Step 5.1** — [ ] L1 Discovery — read `commands.py` to extract existing subcommand decorator + arg-parsing conventions
**Step 5.2** — [ ] Add `rerun-tasks` click subcommand with args: `tasklist_index` (positional), `--task-id` (multi), `--force-all` (flag), `--from-checkpoint` (default True)
**Step 5.3** — [ ] Add `--help` text + register subcommand in `sprint` group
**Step 5.4** — [ ] CLI smoke test (`uv run superclaude sprint rerun-tasks --help`)
**Step 5.5** — [ ] L6 aggregate

### Phase Gate: Phase 5 Quality Verification (M1)

---

## Phase 6: End-to-end integration test
**Step 6.1** — [ ] L1 Discovery — pick a fixture tasklist with 3+ items (1 PASS + 1 FAIL + 1 SKIPPED)
**Step 6.2** — [ ] Write integration test that runs sprint to halt, runs `rerun-tasks --task-id <FAIL_ID>`, asserts PASS items untouched + FAIL re-executed
**Step 6.3** — [ ] L3 — run full sprint test suite (`uv run pytest tests/sprint/ -v`)
**Step 6.4** — [ ] L6 aggregate all Phase 6 outputs

### Phase Gate: Terminal Quality Verification
**Step PG6.1** — [ ] L6 final aggregation across all phases
**Step PG6.2** — [ ] Spawn rf-qa in `task-integrity` mode (full task audit; TB-Add-1..8 catalogue enforced)
**Step PG6.3** — [ ] Spawn rf-qa-qualitative (PR-04 verdict passthrough from PG6.2)
**Step PG6.4** — [ ] L5 conditional — PASS → Post-Completion; FAIL → max 2 cycles, then Open Questions

---

## Post-Completion Actions
- [ ] Verify all output files exist (Glob across phase-outputs/) per I17.2
- [ ] Run full sprint pytest suite (`uv run pytest tests/sprint/ -v`) and confirm 0 regressions per I17.4
- [ ] Confirm `superclaude sprint rerun-tasks --help` returns non-empty output per I17.2
- [ ] Create Task Summary in Task Log / Notes (work completed, files created/modified, blockers + resolutions)
- [ ] Update frontmatter to 🟢 Done + completion_date + Execution Log entry

## Task Log / Notes 📋
### Task Summary
[fill at Post-Completion]

### Execution Log
[timestamped entries]

### Phase 1 - Setup Findings
### Phase 2 - Models Findings
### Phase 3 - Checkpoint Findings
### Phase 4 - Executor Findings
### Phase 5 - CLI Findings
### Phase 6 - E2E Findings
### Phase Gate Findings
### Follow-Up Items Identified
### Deviations from Process
```

### 4.3 SAMPLE FULLY-POPULATED PHASE ITEM (Phase 2.1 — FAIL_RECOVERABLE enum add)

This is the **5-field schema-populated** item the builder should emit. Use it as the gold reference — every body item in the task file must follow this density and shape.

```markdown
- [ ] **2.1 — Add FAIL_RECOVERABLE variant to TaskStatus enum**
  - **Context:** Per researcher-2 patterns (`research/02-patterns-conventions.md` §<N>) and `src/superclaude/cli/sprint/models.py:39-53`, the existing `TaskStatus` enum has 4 variants (`PASS`, `FAIL`, `INCOMPLETE`, `SKIPPED`) with `is_success` and `is_failure` properties. The v4.3.0 spec adds a fifth variant `FAIL_RECOVERABLE` to mark a task that failed but is eligible for surgical rerun without rolling back prior PASS tasks. This is the foundational enum addition every downstream layer (checkpoints, executor, CLI) depends on, so it lands first.
  - **Action:** Use Edit tool on `src/superclaude/cli/sprint/models.py` to add `FAIL_RECOVERABLE = "fail_recoverable"` immediately after the `SKIPPED` member at line ~45, preserving the existing string-value lowercase-snake convention. Then add a new property `@property def is_recoverable(self) -> bool: return self == TaskStatus.FAIL_RECOVERABLE` immediately after the existing `is_failure` property. Update `is_failure` to include the new variant: `return self in (TaskStatus.FAIL, TaskStatus.INCOMPLETE, TaskStatus.FAIL_RECOVERABLE)` so existing `is_failure`-gated branches continue to treat the recoverable variant as a failure for halt purposes (the recoverable distinction matters only for the rerun selector, not for halt semantics). REMEMBER: this project is UV-only — never `python -m` or `pip install`. Component edits go to `src/superclaude/` first; if a corresponding `.claude/` mirror exists DO NOT edit it directly (run `make sync-dev` from the source side after the task completes per CLAUDE.md SoT rule).
  - **Output:** `src/superclaude/cli/sprint/models.py` contains a 5-variant `TaskStatus` enum with `is_recoverable` property and `is_failure` widened to include the new variant. No other enum members or properties are renamed or removed (additive change only).
  - **Verification:** Run `grep -c "FAIL_RECOVERABLE" src/superclaude/cli/sprint/models.py` returns ≥ 2 (one for the enum member, one for `is_failure` widening). Run `grep -c "is_recoverable" src/superclaude/cli/sprint/models.py` returns ≥ 1. Run `uv run python -c "from superclaude.cli.sprint.models import TaskStatus; assert TaskStatus.FAIL_RECOVERABLE.is_recoverable; assert TaskStatus.FAIL_RECOVERABLE.is_failure; assert not TaskStatus.PASS.is_recoverable"` exits 0. Ensuring the addition is purely additive (no existing variant renamed/removed), the string value follows the existing snake_case convention, the `is_failure` widening preserves halt semantics for callers that gate on `is_failure`, and no fabrication beyond what `research/02-patterns-conventions.md` §<N> documents as the project's enum-extension convention.
  - **Evidence on failure:** If unable to complete due to a missing file, ambiguous insertion point, or property-signature conflict, log the specific blocker using the templated format in the `### Phase 2 - Models Findings` section of the `## Task Log / Notes` at the bottom of this task file, then mark this item complete.
  - **Completion gate:** This item cannot be marked as done until the enum member is added, both properties are correct, the grep/import-assert checks all pass, and no other enum member or property has been modified except the documented `is_failure` widening. Once done, mark this item as complete.
```

**Why this item meets B2 schema:**
1. Context → cites `models.py:39-53` (S1 file:line evidence) + researcher-2 reference → S4 self-check passes
2. Action → embeds WHY (foundational; downstream depends), exact insertion location, additivity rule, UV / SoT discipline reminder
3. Output → measurable end state (5-variant enum, property added, others unchanged)
4. Verification → 2 grep checks + 1 importable-assertion smoke test + `ensuring …` clause covering additivity + convention + halt semantics
5. Evidence-on-failure → standard J1 blocker-log pattern with the exact Phase Findings section name
6. Completion gate → explicit "cannot be marked as done until …" closing line

### 4.4 Per-phase item density target

Based on `TASK-RF-20260531-042405:266-365` (R0.1 + R0.2 each shipped a similar shape):
- **Discovery item (L1):** 1 per phase
- **Build items (per-file or per-component K2):** 2-4 per phase
- **Test item (L3):** 1 per phase
- **Lint/format item (L3 with ruff):** 1 per phase
- **L6 aggregate:** 1 per phase
- **Phase Gate (M1 — 3 items):** aggregate + rf-qa spawn + L5 conditional
- **Phase totals:** ~8-12 items per Phase 2-5, ~4-6 for Phase 1, ~10-14 for terminal Phase 6 with full QA gate

This puts total item count at **~40-60 items** — comfortably within TB-Add-2 bounds (≥3 / ≤40 multi-track, ≥3 / ≤50 single-track ADVISORY); flag for splitting only if final count exceeds 50.

---

## 5. TB-Add-1..8 Pre-Write Structural Gates (with citations)

From `src/superclaude/skills/task-builder/SKILL.md:1165-1979`. The task-builder must self-check every item against this catalogue before writing the task file:

| ID | Check | Source line | Active for our task? |
|---|---|---|---|
| **TB-Add-1** | No `TBD`/`TODO`/`FIXME` tokens; no title-only items; 5-field schema enforced | `:1166`, `:1972` | YES — every item must populate Context + Action + Output + Verification + Completion gate |
| **TB-Add-2** | Item count bounds: track ≥3/≤40; single-track ≥3/≤50 (ADVISORY) | `:1167`, `:1973` | YES — target ~40-60 items; flag if >50 |
| **TB-Add-3** | Each blocked item references its blocking Open Question by index in Context | `:1168`, `:1974` | LIKELY INACTIVE — no Open Questions expected; if researcher-3 surfaces any, link them |
| **TB-Add-4** | Item-to-item dependencies form DAG (no cycles) | `:1169`, `:1975` | YES — Phase 2 (enum) blocks Phase 3 (checkpoint) blocks Phase 4 (executor) etc. — strictly linear, automatically DAG |
| **TB-Add-5** | XL/multi-file items split or carry justifying comment | `:1170`, `:1976` | YES — keep each item single-file; Phase 4.2 (rerun_tasks fn add) is the riskiest XL candidate — consider splitting into 4.2a (signature) + 4.2b (body) if it touches >2 functions |
| **TB-Add-6** | Uniform `Verify: …` prefix and `- ✅` / `- [x]` Acceptance Criteria form | `:1171`, `:1977` | YES — use exact phrasing from the sample item §4.3 |
| **TB-Add-7** | Every `## Execution Context` "Source areas:" entry reappears in ≥1 item Context; block contains no file:line | `:1172`, `:1978` | YES — see §4.2 Execution Context block; verify every entry is cited in at least one Phase 2-6 item |
| **TB-Add-8** | Every item Context that references a code surface has a file:line citation OR `<!-- evidence-absence: ... -->` justification | `:1173`, `:1979` | YES — every Context line that mentions `models.py`, `commands.py`, etc. must carry `:NN` line cite (sample 2.1 shows `models.py:39-53`) |

---

## 6. Common Pitfalls (with evidence-cited mitigations)

| Pitfall | Source | Mitigation in this task |
|---|---|---|
| Standalone "read context" item with no output | B5 `:166-169` | Every item has an explicit Output specification; reads are embedded in action items |
| Multi-line / bulleted checklist items | B5 `:175-180` | Sample item §4.3 is one paragraph per the B3 rule; the bold sub-labels above (Context/Action/etc.) are descriptive headers, not bullet items |
| Parent checkbox before children | E2 `:327-333` | All Step X.Y headers are bold-text, NOT checkboxes; only the `- [ ]` lines are checkboxes |
| Summary checkbox before component items | E2 `:335-341` | L6 aggregation always at END of each phase, never opening |
| Skipping phase-gate QA | F2 `:411`, I15 `:599-607` | M1 gate (aggregate + rf-qa + L5) at end of every Phase 2-6 |
| Skipping post-completion validation | F2 `:412`, I17 `:626-635` | Post-Completion Actions section has 4 mandatory items (Glob check, pytest, --help smoke, task summary) |
| Missing test phase for code-modifying task | I18 `:637-646` | Every implementation phase ends with an L3 test/lint item before the phase gate |
| Editing `.claude/` directly instead of `src/` | CLAUDE.md SoT rule | Every action item's REMEMBER clause restates "src/superclaude/ first; never .claude/" |
| Multi-line bash heredocs | global memory `feedback_no_multiline_paste` | Every L3 Bash item uses single-line commands with `cd … && … 2>&1 \| tee …` form |
| Bare `python`/`pip`/`pytest` | CLAUDE.md UV rule | Every test command prefixed `uv run` |
| Item Context citing code without file:line | TB-Add-8 `:1173` | Sample 2.1 shows `models.py:39-53` pattern |
| Cross-phase delegation | F2 `:410` | No item spawns subagents spanning phases; rf-qa spawn at phase gate is bounded to that gate |
| Worker dynamically adding checklist items | K2 `:693-696` | Orchestrator pre-enumerates every item at task-build time; Phase 4.4 "test branches" item lists all 4 branches by name |

---

## 7. Pattern Reuse Recommendations for Builder

When the task-builder writes the final file, **lift verbatim** from these MultiModelSwarm task patterns at the cited lines — they're already proven to clear rf-qa task-integrity:

| Pattern | Source line in `TASK-MULTIMODELSWARM-AUDIT-REMEDIATION-20260531.md` |
|---|---|
| Item header format `- [x] **X.Y — Title**` then `- **Context:**` etc. | `:77-82` (Phase 1.1) |
| Bash verification with grep return-count assertion | `:120` (`grep -c '"HTML"' src/... returns ≥ 1`) |
| Python import-assert smoke test | adapted in §4.3 sample for `is_recoverable` |
| Test-suite run as L3 with raw + summary outputs | `TASK-RF-20260531-042405:296` (Step 2.7) |
| rf-qa task-integrity spawn item shape | `TASK-RF-20260531-042405:310` (Step PG2.2) — copy the ADVERSARIAL STANCE + fix_authorization + HALT-PRECEDENCE GUARDS prompt verbatim, swap the verify-block |
| L5 conditional-proceed after QA gate | `TASK-RF-20260531-042405:314` (Step PG2.3) |
| Phase Findings section template at bottom | `02_mdtm_template_complex_task.md:1166-1196` |

---

## 8. Summary for the Builder

The builder receiving this research output should:

1. Use the §4.1 frontmatter shape, populating `related_docs` from researcher 1-4 outputs.
2. Use the §4.2 section ordering verbatim — no skipped sections, no added top-level headings.
3. For every implementation item, populate the §4.3 6-element schema (Context + Action + Output + Verification + Evidence-on-failure + Completion gate) with file:line citations from researcher-2 outputs.
4. Insert M1 phase gates (aggregate + rf-qa spawn + L5 conditional) after every Phase 2-6, lifting the rf-qa prompt shape from `TASK-RF-20260531-042405:310`.
5. Run the TB-Add-1..8 catalogue (§5) as the final pre-write self-check.
6. Watch the pitfall table (§6) — these are the failure modes rf-qa will flag.
7. Target ~40-60 items total (6 phases × 8-12 items + 4 post-completion).

The sample Phase 2.1 item in §4.3 is the gold reference for item density and shape.
