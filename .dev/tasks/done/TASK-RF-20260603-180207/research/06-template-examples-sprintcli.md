# R6 — Template & Examples & Sprint-CLI Compatibility

Status: Complete
Date: 2026-06-03
Researcher: R6 (task-builder)

Topic: MDTM Template 02 rules, prior `TASK-RF-*` examples, Sprint-CLI compatibility, phase-gate QA pattern, task-file placement convention.

---

## 1. Template 02 PART 1 Rules

Source: `.claude/templates/workflow/02_mdtm_template_complex_task.md` (1205 lines total)

### 1.1 Required Frontmatter Fields (lines 1-44)

The frontmatter block (YAML between `---`) contains:

- `id: "TASK-[AGENT]-[TASKTYPE]-YYYYMMDD-HHMMSS"` (line 2)
- `title`, `description`, `status: "🟡 To Do"`, `type`, `priority` (lines 3-7)
- `created_date`, `updated_date`, `assigned_to`, `autogen: false`, `autogen_method: ""` (lines 8-12)
- `coordinator: orchestrator` (line 13)
- `parent_task`, `depends_on` (list), `related_docs` (list of `{path, description}`) (lines 14-24)
- `tags` (list) (lines 25-29)
- `template_schema_doc`, `estimation`, `sprint`, `due_date`, `start_date`, `completion_date`, `blocker_reason`, `ai_model`, `model_settings` (lines 30-38)
- `review_info: {last_reviewed_by, last_review_date, next_review_date}` (lines 39-42)
- **`task_type: static`** (line 43) — CRITICAL for fixed-content tasks (see I6, line 531)

### 1.2 Section A — Core Principles

- **A3 Complete Granular Breakdown** (lines 91-96): break EVERY workflow phase into atomic verifiable checklist items; one item per file/component/iteration; NO bulk operations; exact paths + measurable outcomes.
- **A4 Iterative Process Structure** (lines 97-116): for multi-item processes — pre-enumerate ALL items in an initial step (`Step X.1: Scan and enumerate`), then one checklist item per item (`Step X.2`), then a consolidation step (`Step X.3`). Worker NEVER dynamically adds items.

### 1.3 Section B — Self-Contained Checklist Items (CRITICAL)

- **B1** (lines 134-141): session-rollover protection — context loaded in batch 1 is gone by batch 3+; every item must be self-contained; standalone "read context" items are USELESS.
- **B2** (lines 142-149): EVERY item is a complete self-contained prompt with 6 elements:
  1. Context Reference with WHY (what files to read + why)
  2. Action with WHY
  3. Output Specification (exact file path/name, content, template)
  4. Integrated Verification ("ensuring..." clause; no fabrication; 100% source-derived; document negative evidence)
  5. Evidence on Failure Only (log blocker to Task Log only on failure)
  6. Explicit Completion Gate ("This item cannot be marked as done until... Once done, mark this item as complete.")
- **B3** (lines 150-154): ONE FULL PARAGRAPH per item, verbose, reads like an independently-executable prompt.
- **B5 FORBIDDEN** (lines 164-184): standalone read-context items; missing context reference; multi-line/bulleted items; separate verification items; overly granular items; REMINDER blocks between items.
- **B7** (lines 189-197): verification embedded via "ensuring..." clause; output file IS the evidence; only log on FAIL; QA process handles inter-batch verification.

### 1.4 Section C — Embedding (no separate sections)

- Outputs/Deliverables (C1), Success Criteria (C2 as "ensuring..." clause), Verification (C3) are EMBEDDED in items, NOT separate sections.
- C4 (lines 225-231): Task Completion handled by Post-Completion Actions section (frontmatter update + Execution Log).

### 1.5 Section D — Mandatory Sections + Critical Rule

- D1 Workflow Compliance Declaration [workflow-dependent, informational].
- D2 Cross-Stage Integration Requirements [informational, no checklist items].
- **D3 CRITICAL RULE** (lines 269-273): NO checklist items before Phase 1. Order = Frontmatter → Workflow Compliance (informational) → Prerequisites (informational) → Phase 1 (executable). Context-review + prev-stage-input items live IN Phase 1 (Steps 1.2-1.4).

### 1.6 Section E — Checklist Structure Rules

- **E1** (lines 278-292): every actionable item is `- [ ]`; FLAT structure only (NO nested checkboxes); NO parent checkboxes summarizing children; use `**Step X.Y:**` headers for grouping; checkboxes in completion order; atomic + verifiable.
- **E2** (lines 294-348): summary/parent checkboxes come AFTER component items, never before. Components first, summary last.
- **E3** (lines 350-365): sequential top-to-bottom only; FORBIDDEN: "mark item above", "see below", backward movement, parent-with-children.
- **E4** (lines 367-388): step numbers are bold headings WITHOUT checkboxes; no REMINDER blocks between items.

### 1.7a Section I — Additional Guidelines (key QA rules)

- **I6** (lines 526-536): `task_type: "static"` for fixed content, `"dynamic"` for runtime-built lists.
- **I15 PHASE-GATE QA ENFORCEMENT** (lines 599-607): every task with 2+ execution phases MUST have ≥1 phase-gate QA checkpoint between the primary execution phase and any dependent subsequent phase. A checkpoint = (1) aggregation item, (2) QA agent spawn item (rf-qa or rf-qa-qualitative), (3) conditional-action item (proceed on PASS / fix cycle on FAIL). QA spawn item follows B2's 6-element pattern: agent name, phase type, input files, output report path, verdict handling, error clause.
- **I16 QA GATE VERDICT + FIX CYCLES** (lines 609-624): binary PASS/FAIL; ANY severity (CRITICAL/IMPORTANT/MINOR) = FAIL. Max fix cycles by gate type: research-gate=3 (HALT+escalate), synthesis-gate=2 (→Open Questions), report-validation=3 (HALT), task-integrity=2 (→Open Questions), any qualitative gate=3 (HALT+escalate). Each cycle re-verifies ALL previously-failed items + checks new issues; rising issue count = systemic problem. Encode as L5 conditional-action items.
- **I17 POST-COMPLETION VALIDATION** (lines 626-635): before status→Done, validate: all `- [ ]`→`- [x]`; all output files exist (Glob); blocker entries have resolution notes; if source code modified → tests pass.
- **I18 TESTING FOR CODE-MODIFYING TASKS** (lines 637-646): if task creates/modifies source code, MUST include ≥1 testing item specifying the test command, pass criteria, where results captured; follows B2; use L3 pattern.

### 1.7b Sections L & M — Handoff + Phase-Gate Composite Patterns

- **Handoff convention** (lines 718-730): items write to `.dev/tasks/TASK-NAME/phase-outputs/{discovery,test-results,reviews,plans,reports}/`. Files persist across batches/rollovers.
- **L1-L6** (lines 737-809): L1 Discovery, L2 Build-from-Discovery, L3 Test/Execute, L4 Review/QA, L5 Conditional-Action (MUST handle BOTH branches), L6 Aggregation (Glob-discover).
- **M1 PHASE-GATE QA SEQUENCE** (lines 843-851): 2-3 items between phases: (1) Aggregation (L6); (2) QA Spawn — rf-qa structural (+ rf-qa-qualitative in a SEPARATE sequential item if needed); (3) Conditional Proceed (L5).
- **M2 APPLICABILITY** (lines 852-860): code-modifying → gate after implementation, before testing (or after combined implement+test). "When in doubt, include a gate."

### 1.7c PART 2 — Concrete Task File Skeleton (lines 890-1205)

Emitted body structure: `# [Title]` → `## Task Overview` → `## Key Objectives` → `## Prerequisites & Dependencies` (Parent Task & Dependencies; Previous Stage Outputs [INFORMATIONAL, no items]; Handoff File Convention; Frontmatter Update Protocol) → `## Detailed Task Instructions` → `### Phase 1: Preparation and Setup` (1.1 status→Doing + Execution Log; 1.2 create phase-outputs dirs) → `### Phase 2: [Main Execution]` → `### Phase Gate: Quality Verification` (PG.1) → `### Phase [N]: Testing & Verification` → `## Post-Completion Actions` (Glob-verify outputs; run tests; write Task Summary; update completion_date + status→Done) → `## Task Log / Notes 📋` (`### Task Summary`, `### Execution Log`, `### Phase N Findings` per phase, `### Phase Gate Findings`, `### Follow-Up Items Identified`, `### Deviations from Process`).

### 1.7 Section F — Execution Requirements (worker agents)

- **F1 Five-Step** (lines 394-403): READ → IDENTIFY (first unchecked `- [ ]`) → EXECUTE (only that one) → UPDATE (mark only that `- [x]`) → REPEAT.
- **F2 Prohibited** (lines 405-413): multi-item execution; skipping ahead; delegating across phase boundaries (subagent gets a SINGLE item only); **skipping phase-gate QA (must spawn rf-qa after all items in Phase 2+)**; skipping post-completion validation (must run rf-qa structural + rf-qa-qualitative before Done).
- **F2a Item Execution Discipline** (lines 414-430): one item at a time within a session. **Parallel spawning exception**: consecutive items in the SAME phase that spawn INDEPENDENT subagents MAY be spawned in parallel; executor still marks each individually; NOT for data-dependent items.
- **F5 Frontmatter Update Protocol** (lines 447-451): start → status "🟠 Doing" + start_date; done → "🟢 Done" + completion_date; blocked → "⚪ Blocked" + blocker_reason; each session → updated_date.

---

## 2. Sprint-CLI Compatibility (CRITICAL DISTINCTION)

Source: `src/superclaude/cli/sprint/commands.py`, `src/superclaude/cli/sprint/config.py`, `src/superclaude/cli/sprint/process.py`

### 2.1 What `superclaude sprint run` actually expects

**`sprint run` does NOT take a single MDTM task file.** It takes a `tasklist-index.md` and discovers SEPARATE per-phase tasklist FILES, executing each as a fresh Claude Code session.

- `commands.py:72` — `run` takes `INDEX_PATH` = path to a `tasklist-index.md` (`commands.py:210`).
- `config.py:52 discover_phases(index_path)` — discovers phase FILES two ways:
  - **Strategy 1**: parse a markdown table in the index with a `File` column (and optional `Execution Mode` column: `claude` | `python` | `skip`, default `claude`; `config.py:67-118`). Unknown execution mode → `ClickException` (`config.py:112`).
  - **Strategy 2**: scan the index directory for files matching `PHASE_FILE_PATTERN` (`config.py:128-138`).
- **`PHASE_FILE_PATTERN`** (`config.py:20-26`) matches filenames: `phase-<N>-tasklist.md` | `p<N>-tasklist.md` | `phase_<N>_tasklist.md` | `tasklist-p<N>.md` (case-insensitive). **A file NOT matching this pattern is invisible to sprint.**
- Phases deduplicated by number, sorted ascending (`config.py:140`).
- Each phase is executed via `/sc:task` — `process.py:170`: `f"/sc:task Execute all tasks in @{phase_file} ..."`.
- `count_tasks_in_file` (`config.py:37`) pre-scans each phase file counting `### T<PP>.<TT>` headings (`_TASK_ID_HEADING_RE = ^###\s+T\d{2}\.\d{2}\b`, `config.py:31-34`) to drive the progress bar.

### 2.2 What makes a file FAIL to be Sprint-CLI-compatible

1. **Single-file task with no index** — `sprint run` requires a `tasklist-index.md`; pointing it at one MDTM `.md` file finds no phase files.
2. **Phase files not matching `PHASE_FILE_PATTERN`** — e.g. naming them `TASK-RF-<id>.md` or `phase2.md` → `discover_phases` returns empty / skips them.
3. **No `### T<PP>.<TT>` task headings** — `count_tasks_in_file` reports 0 tasks (progress bar empty; not fatal but signals a non-tasklist file).
4. **Bad `Execution Mode` value** in the index table → hard `ClickException`.

### 2.3 The right tool for THIS deliverable: `/task`, not `sprint`

The task-builder skill produces a **single self-contained MDTM task file** (Template 02), run via the **`task` skill / `/task <path>`** (F1 loop, batched across sessions), NOT `superclaude sprint run`. The prior example `TASK-RF-20260531-042405.md` is exactly this shape: ONE file, `### Phase N` headers (not `### T<PP>.<TT>`), executed by `/task`. Its frontmatter `sprint: ""` is empty.

**Conclusion:** "Sprint-CLI-compatible" for a task-builder deliverable means **Template-02-compliant + `/task`-executable** (phase-gate QA, self-contained items). It is NOT literally `sprint run`-discoverable unless split into a multi-file tasklist bundle (which is the `/sc:tasklist` output shape, a different surface). MEMORY `feedback-no-sctask-on-task-builder-tasklists.md` confirms task-builder MDTM files are run with `/task` directly.

---

## 3. Prior Example — Concrete Shape (`TASK-RF-20260531-042405.md`)

Source: `.dev/tasks/to-do/TASK-RF-20260531-042405/TASK-RF-20260531-042405.md`

### 3.1 Frontmatter shape (lines 1-76)

Standard Template-02 frontmatter PLUS task-specific keys. Key real values:
- `id: "TASK-RF-20260531-042405"` (line 2), `status: "🟢 Done"` (line 5), `type: "🔨 Refactor"` (line 6).
- `coordinator: orchestrator` (line 14), `parent_task: ""` (line 15), `depends_on: []` (line 16).
- `related_docs:` list of `{path, description}` — points at BUILD-REQUEST, master-report, vector analyses, AND the research files (`research/01-*.md`, `02-*.md`, `03-*.md`) (lines 17-33).
- `template_schema_doc: ".claude/templates/workflow/02_mdtm_template_complex_task.md"` (line 49).
- `task_type: static` (line 62); plus custom keys `category`, `phasing`, `preserves`, `inverts` (lines 63-75).
- `last_phase_completed:` — a long prose field recording the most-recent closed phase + carry-forwards (line 10). This is a project-local convention for resumability.

### 3.2 Phase + Phase-Gate structure (verified via grep, line numbers from full file)

```
### Phase 1: Preparation and Setup                          (line 233)
  Step 1.1 status→Doing; Step 1.2 verify handoff dirs
### Phase 2: R0.1 — Spec-ID Registry (Contract #9)          (line 190 region; body 239+)
  Steps 2.1..2.N (L1 discovery, L2 build, L3 test, lint/format)
### Phase Gate: R0.1 Quality Verification                   (line 302)
  Step PG2.1 Aggregate R0.1 outputs        (L6)             (line 304)
  Step PG2.2 Spawn rf-qa task-integrity    (QA spawn)       (line 308)
  Step PG2.3 Act on R0.1 QA verdict        (L5 conditional) (line 312)
### Phase 3: R0.2 ...                                        (line 316)
### Phase Gate: R0.2 Quality Verification  (PG3.1/3.2/3.3)
... (one Phase + one Phase Gate per R-item, through Phase 13) ...
### Phase Gate: Final Terminal QA Gate     (PG13.1 ...)
## Post-Completion Actions
## Task Log / Notes 📋
```

Every execution phase is followed by a `### Phase Gate: <name> Quality Verification` with a numbered `PGn.x` triplet. Terminal/acceptance gates use `rf-qa-qualitative` in `release-validation` mode; intermediate gates use `rf-qa` in `task-integrity` mode.

### 3.3 Concrete QA-gate triplet pattern (PG2.1-2.3, lines 304-314)

- **PG2.1 (Aggregate, L6):** "Use Glob to find all R0.1 phase outputs matching `...phase-outputs/{discovery,test-results}/r0-1-*.md`... then write an aggregation summary to `...reports/r0-1-aggregation.md` containing: every file discovered with size+summary; list of new/modified source files; test+lint summaries; Contract satisfaction assertion. Ensuring all referenced files accounted for with no fabrication. If unable... log blocker in `### Phase Gate Findings`... mark complete."
- **PG2.2 (rf-qa spawn):** "Spawn the rf-qa agent in `task-integrity` mode with the prompt: 'ADVERSARIAL STANCE: Assume [the deliverable] has subtle [Contract] violations until evidence proves otherwise. fix_authorization: true. Read the aggregation report at [path], then read every new/modified source file, then read [spec] §[anchor], then verify: (a)... (b)... (g)... and write the verdict to `...reviews/r0-1-rf-qa-task-integrity.md` as PASS/FAIL with severity-classified findings (CRITICAL/IMPORTANT/MINOR). HALT-PRECEDENCE GUARDS: regression check → monotonicity check → cap (max 2 fix cycles per Template 02 §I16 task-integrity gate; unresolved → Open Questions).' If the agent spawn fails, log the blocker... mark complete."
- **PG2.3 (Act, L5 conditional):** "Read the rf-qa verdict file [path], then: IF verdict is PASS, create `...plans/r0-1-proceed-decision.md`... and proceed to Phase 3; IF verdict is FAIL, read each finding, edit relevant source (in `src/superclaude/`, NEVER `.claude/`), re-run [tests], update summaries, then re-run PG2.2 (max 2 cycles per I16). If 2 cycles complete FAIL, write unresolved to Open Questions... and proceed. REMEMBER: UV-only; `src/superclaude/` only. Ensuring fix cycles obey halt-precedence... If unable... log blocker... mark complete."

Note the **rf-qa adversarial pattern** (MEMORY `feedback_rfqa_adversarial_pattern.md`): explicit "ADVERSARIAL STANCE" framing + `fix_authorization: true` in every gate spawn.

---

## 4. Phase-Gate QA Pattern (synthesis)

Per-phase gates are encoded as a **3-item `PGn.x` triplet** in a dedicated `### Phase Gate: <name>` section immediately after each execution phase:
1. **Aggregate (L6)** — Glob phase outputs → `phase-outputs/reports/<phase>-aggregation.md`.
2. **QA spawn** — rf-qa (`task-integrity`, max 2 cycles) for structural/intermediate phases; rf-qa-qualitative (`release-validation`/`documentation-alignment`, max 3 cycles) for acceptance/terminal/doc phases. ADVERSARIAL STANCE + `fix_authorization: true`. Verdict → `phase-outputs/reviews/<phase>-rf-qa-*.md`.
3. **Act (L5 conditional)** — IF PASS → write `phase-outputs/plans/<phase>-proceed-decision.md`, proceed; IF FAIL → fix in `src/`, re-run tests, re-spawn (cap per I16), then Open Questions or HALT.

For code-modifying phases, a **testing item (L3, I18)** lives inside the execution phase (e.g. `uv run pytest tests/roadmap/... -v`) BEFORE the gate, capturing results to `phase-outputs/test-results/`. The gate's aggregation reads those test summaries.

---

## 5. Where the Task File Goes

- **Convention:** `.dev/tasks/to-do/TASK-RF-<id>/TASK-RF-<id>.md` — confirmed by the prior example at `.dev/tasks/to-do/TASK-RF-20260531-042405/TASK-RF-20260531-042405.md`, and this research dir already lives at `.dev/tasks/to-do/TASK-RF-20260603-180207/research/`.
- The task FILE is a sibling of the `research/` and (created at execution) `phase-outputs/` directories, all under the `TASK-RF-<id>/` folder.
- **NOT under `.claude/`** — `.claude/{skills,commands,agents,hooks,templates}` is gitignored sync-dev output (CLAUDE.md ABSOLUTE RULE; MEMORY `feedback_claude_dir_gitignored.md`). Task files are tracked work artifacts under `.dev/`.
- For THIS task: `/config/workspace/IronClaude-RoadmapRewrite/.dev/tasks/to-do/TASK-RF-20260603-180207/TASK-RF-20260603-180207.md`.

---

## Summary

1. **Template 02** mandates: full frontmatter incl. `task_type: static`; B2 self-contained one-paragraph items (6 elements: context+WHY, action+WHY, output spec, "ensuring..." verification, evidence-on-failure-only, completion gate); flat checkboxes (E1-E4), no parent-before-children; F1 READ→IDENTIFY→EXECUTE→UPDATE→REPEAT; phase-gate QA between dependent phases (I15-I16, M1); post-completion validation (I17); testing items for code-modifying tasks (I18).
2. **Sprint-CLI** (`sprint run`) operates on a **`tasklist-index.md` + per-phase `phase-<N>-tasklist.md` files** discovered via `PHASE_FILE_PATTERN`, each run as `/sc:task`. A single MDTM task file is NOT `sprint run`-discoverable; it is run via **`/task`**. "Sprint-CLI-compatible" for a task-builder deliverable = Template-02-compliant + `/task`-executable with phase-gate QA.
3. **Prior example** `TASK-RF-20260531-042405.md` is the gold-standard shape: one file, `### Phase N` + `### Phase Gate: ...` (`PGn.x` triplet) per R-item, rf-qa/rf-qa-qualitative with ADVERSARIAL STANCE + `fix_authorization: true`, handoff to `phase-outputs/{discovery,test-results,reviews,plans,reports}/`.
4. **Per-phase QA** = Aggregate(L6) → rf-qa spawn → Act(L5 conditional) triplet; fix-cycle caps per I16.
5. **Placement** = `.dev/tasks/to-do/TASK-RF-<id>/TASK-RF-<id>.md`, never `.claude/`.

---

## Recommended Task-File Skeleton (THIS 5-item task, Template-02, PER_PHASE QA)

**File:** `/config/workspace/IronClaude-RoadmapRewrite/.dev/tasks/to-do/TASK-RF-20260603-180207/TASK-RF-20260603-180207.md`

**Frontmatter (fill from BUILD_REQUEST / scope):**
```yaml
---
id: "TASK-RF-20260603-180207"
title: "[5 brittleness follow-ups — concise title]"
description: "[what + why, references to the 5 code areas R1-R5]"
status: "🟡 To Do"
type: "🔨 Refactor"
priority: "🔼 High"
created_date: "2026-06-03"
updated_date: "2026-06-03"
assigned_to: ""
autogen: false
autogen_method: ""
coordinator: orchestrator
parent_task: ""
depends_on: []
related_docs:
- path: "[BUILD_REQUEST path]"
  description: "Authoritative spec for the 5 follow-ups"
- path: ".dev/tasks/to-do/TASK-RF-20260603-180207/research/01-...md"
  description: "R1 research"
# ... one related_docs entry per research file (R1-R7) ...
tags: ["refactor", "roadmap-pipeline", "follow-ups", ...]
template_schema_doc: ".claude/templates/workflow/02_mdtm_template_complex_task.md"
estimation: ""
sprint: ""
due_date: ""
start_date: ""
completion_date: ""
blocker_reason: ""
ai_model: ""
model_settings: ""
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
task_type: static
---
```

**Body / phase list** (one execution phase + one phase gate per follow-up; +1 testing phase if code-modifying spans multiple phases; +1 final acceptance):

```
# [Task Title]
## Task Overview
## Key Objectives                    (5 numbered objectives, one per follow-up)
## Prerequisites & Dependencies
  ### Parent Task & Dependencies
  ### Previous Stage Outputs (MANDATORY INPUTS)   [INFORMATIONAL — list research files + BUILD_REQUEST]
  ### Handoff File Convention                     [.dev/tasks/to-do/TASK-RF-20260603-180207/phase-outputs/]
  ### Frontmatter Update Protocol
## Detailed Task Instructions

### Phase 1: Preparation and Setup
  Step 1.1  status→"🟠 Doing" + start_date + Execution Log entry
  Step 1.2  create phase-outputs/{discovery,test-results,reviews,plans,reports}/

### Phase 2: [Follow-up #1 — name]            (L1 discover → L2 build → L3 test item per I18)
### Phase Gate: [#1] Quality Verification
  Step PG2.1  Aggregate #1 outputs (L6)
  Step PG2.2  Spawn rf-qa task-integrity (ADVERSARIAL STANCE + fix_authorization:true)
  Step PG2.3  Act on verdict (L5: PASS→proceed / FAIL→fix, max 2 cycles per I16)

### Phase 3: [Follow-up #2 — name]
### Phase Gate: [#2] Quality Verification     (PG3.1/3.2/3.3)

### Phase 4: [Follow-up #3 — name]
### Phase Gate: [#3] Quality Verification     (PG4.1/4.2/4.3)

### Phase 5: [Follow-up #4 — name]
### Phase Gate: [#4] Quality Verification     (PG5.1/5.2/5.3)

### Phase 6: [Follow-up #5 — name]
### Phase Gate: [#5] Quality Verification     (PG6.1/6.2/6.3)

### Phase 7: Final Acceptance                 (full test suite + cross-cutting checks)
### Phase Gate: Final Terminal QA Gate
  Step PG7.1  Spawn rf-qa-qualitative release-validation (ADVERSARIAL, max 3 cycles per I16)
  Step PG7.2  Act on final verdict (L5)

## Post-Completion Actions
  - Glob-verify all output files exist
  - Run full test suite (uv run pytest tests/roadmap/ -v) if code modified
  - Write ### Task Summary
  - Update completion_date + updated_date + status→"🟢 Done" + Execution Log

## Task Log / Notes 📋
  ### Task Summary
  ### Execution Log
  ### Phase 1 Findings  ... ### Phase 7 Findings   (one per phase)
  ### Phase Gate Findings
  ### Follow-Up Items Identified
  ### Deviations from Process
```

**Notes for the task-builder:**
- Each execution-phase step is ONE self-contained B2 paragraph (no separate verify items; "ensuring..." clause embedded).
- If a follow-up modifies `src/superclaude/` code, include an L3 testing item (`uv run pytest tests/roadmap/<relevant> -v`) inside that phase BEFORE its gate (I18); the gate's aggregation reads the test summary.
- ABSOLUTE RULE: source edits go to `src/superclaude/` then `make sync-dev`; NEVER edit/commit `.claude/`. Bake "REMEMBER: UV-only; `src/superclaude/` only" into every code-editing item (as the prior example does).
- intermediate gates → rf-qa `task-integrity` (cap 2); terminal gate → rf-qa-qualitative `release-validation` (cap 3).
- Run `/sc:reflect --mode pre` on the finished tasklist before execution (MEMORY `feedback_sc_reflect_vs_inline_rfqa.md`).

---

Status: Complete
