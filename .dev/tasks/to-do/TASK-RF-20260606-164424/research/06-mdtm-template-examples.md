# Research: Template & Examples — MDTM Template 02 (complex task)

Topic type: Template & Examples
Scope: `02_mdtm_template_complex_task.md` PART 1 + complex example task files in `.dev/tasks/to-do/`
Status: Complete
Date: 2026-06-06

Files cited:
- Template: `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md` (1205 lines total)
- Example: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260603-211955/TASK-RF-20260603-211955.md` (45 KB, complex, 5 phases + phase gate)

---

## 0. PART 1 vs PART 2 split (template structure)

The template file is ONE file with two halves, separated by HTML comment fences:

- **Frontmatter (L1-44)** — the YAML block at the very top IS part of the emitted template (L883: "The frontmatter at the top of this file is also part of the template").
- **PART 1: TASK BUILDING INSTRUCTIONS (L46-870)** — wrapped entirely in an HTML comment `<!-- ... -->` opened at L46 and NOT closed until L888. So all of Sections A-M are commented out and never render in the output task file. L57-58: "NONE of this content appears in the actual output task file. The clean template structure is in PART 2 below." This half is "FOR ORCHESTRATOR/TASK BUILDER ONLY" (L54).
- **PART 2: TASK FILE TEMPLATE (L872-1204)** — begins at the `# [Task Title]` line (L890). L880-882: "When creating a task, copy everything from `# [Task Title]` to the end of the file, replacing all placeholders." This is the structure the builder actually emits.

Template 02 = Template 01 + Section L (Intra-Task Handoff Patterns). L61-63: "Extends Template 01 with Section L... Use this template when tasks require discovery, testing, review, conditional logic, or aggregation between checklist items."

---

## 1. Required YAML frontmatter fields (template L1-44)

Exact field set, in order, with the template's literal placeholder/default values:

| Field | Template value (L#) | Notes |
|---|---|---|
| `id` | `"TASK-[AGENT]-[TASKTYPE]-YYYYMMDD-HHMMSS"` (L2) | |
| `title` | `"[Clear, Action-Oriented Task Title]"` (L3) | |
| `description` | `"[Detailed description...]"` (L4) | |
| `status` | `"🟡 To Do"` (L5) | enum — see below |
| `type` | `"📝 Documentation"` (L6) | enum — see below |
| `priority` | `"🔼 High"` (L7) | enum — see below |
| `created_date` | `"YYYY-MM-DD"` (L8) | |
| `updated_date` | `"YYYY-MM-DD"` (L9) | |
| `assigned_to` | `"[agent-name]"` (L10) | |
| `autogen` | `false` (L11) | |
| `autogen_method` | `""` (L12) | |
| `coordinator` | `orchestrator` (L13) | |
| `parent_task` | `"[PARENT-TASK-ID]"` (L14) | |
| `depends_on` | list (L15-17) | YAML list of dependency IDs |
| `related_docs` | list of `{path, description}` (L18-24) | |
| `tags` | list (L25-29) | |
| `template_schema_doc` | `""` (L30) | |
| `estimation` | `""` (L31) | |
| `sprint` | `""` (L32) | |
| `due_date` | `""` (L33) | |
| `start_date` | `""` (L34) | |
| `completion_date` | `""` (L35) | |
| `blocker_reason` | `""` (L36) | |
| `ai_model` | `""` (L37) | |
| `model_settings` | `""` (L38) | |
| `review_info` | `{last_reviewed_by, last_review_date, next_review_date}` (L39-42) | nested map |
| `task_type` | `static` (L43) | `static` or `dynamic` (see I6, L530-532) |

**Note vs the research-brief field list:** the brief listed a subset (id, title, status, type, priority, created_date, updated_date, assigned_to, template_schema_doc, estimation, task_type, related_docs, tags). The template's ACTUAL set is larger (the table above) — it additionally requires `description`, `autogen`, `autogen_method`, `coordinator`, `parent_task`, `depends_on`, `sprint`, `due_date`, `start_date`, `completion_date`, `blocker_reason`, `ai_model`, `model_settings`, `review_info`.

### Enum values (from defaults + Frontmatter Update Protocol L947-950 / F5 L447-451)

- **status:** `🟡 To Do` (default), `🟠 Doing` (on start), `🟢 Done` (on completion), `⚪ Blocked` (if blocked). These four emoji-prefixed strings are the observed set.
- **type:** `📝 Documentation` (template default). Example file uses `🛠 Code Fix` (example L6). So `type` is an emoji-prefixed free-ish label; observed values: `📝 Documentation`, `🛠 Code Fix`.
- **priority:** `🔼 High` (template default, L7). Emoji-prefixed; `🔼 High` is the only value observed in template + example.

---

## 2. Section A — Core building rules (granularity & iteration)

### A3. COMPLETE GRANULAR BREAKDOWN (template L91-95) — exact wording
```
A3. COMPLETE GRANULAR BREAKDOWN
   - Break down EVERY workflow phase into atomic, verifiable checklist items
   - Create individual checklist items for EVERY file, component, or iteration
   - NO high-level or bulk operations allowed - everything must be granular
   - Include exact file paths, specific requirements, and measurable outcomes
```
**What counts as a violation (batch items):** a single checklist item that processes multiple files/components in bulk ("update all the handlers", "create the configs") instead of one atomic item per file/component/iteration. "NO high-level or bulk operations allowed." Reinforced by I2 EXTREME GRANULARITY (L505-509): "Include exact file paths, not general directories ... If a step could be interpreted multiple ways, it needs more detail." And K2 (L694-696): the orchestrator MUST pre-enumerate ALL items; the worker MUST NEVER dynamically add checklist items.

### A4. ITERATIVE PROCESS STRUCTURE (template L97-116) — exact wording
```
A4. ITERATIVE PROCESS STRUCTURE
   - For ANY process involving multiple items (files, components, etc.):
     * Pre-enumerate ALL items to be processed in initial step
     * Create individual checklist item for each specific item
     * Require incremental updates after each item
     * Include consolidation step only after all items complete
   - Use this pattern:
     Step X.1: Scan and enumerate all [items] in [location]
       - [ ] Complete [item] listing generated: [count] items identified
     Step X.2: Process each [item] individually:
       - [ ] [Item 1]: [exact identifier] - [specific action] completed
       - [ ] [Item 2]: [exact identifier] - [specific action] completed
       [Continue for each item]
     Step X.3: Consolidate all individual results
       - [ ] All [count] items processed and results logged
       - [ ] Consolidated output created per requirements
```
Pattern = enumerate (discovery) → per-item processing → consolidate. Maps directly onto L1 (discovery) → L2 (build per item) → L6 (aggregate).

### Other Section A rules
- **A1 (L72-83):** Workflow document availability check. If governing workflow docs exist, follow WORKFLOW-DEPENDENT sections; if not, omit them and derive from user requirements (same detail level).
- **A2 (L85-89) [WORKFLOW-DEPENDENT]:** Deep-integrate the governing workflow — extract EVERY requirement/phase/step/standard, map each to a task element.
- **A5 (L118-122) [WORKFLOW-DEPENDENT]:** Cross-stage integration — every phase specifies inputs from previous stages with exact paths.
- **A6 (L124-128) [WORKFLOW-DEPENDENT]:** Workflow compliance enforcement — reference workflow sections throughout, copy quality standards verbatim.

---

## 3. Section B — Self-contained checklist items (the B2 pattern)

### B1 — Why (template L134-140)
Rigorflow executes in batches across sessions; session rollovers mean context loaded in batch 1 is NOT available in batch 3+. Therefore EVERY item MUST be self-contained. "Standalone 'read context' items that don't produce actionable output are USELESS because that context will be lost before it can be used."

### B2 — The 6 required elements per item (template L142-148) — exact field names
> B2. EVERY CHECKLIST ITEM MUST BE A COMPLETE, SELF-CONTAINED PROMPT THAT INCLUDES:
> 1. **Context Reference with WHY** — What file(s) to read and why that context is needed for this specific action
> 2. **Action with WHY** — What to do with that context and why it needs to be done
> 3. **Output Specification** — The exact output file name, location, what content to produce, and template to follow (if applicable)
> 4. **Integrated Verification** — An "ensuring..." clause that specifies what must be verified (DO NOT assume, hallucinate, or make up any information — all content MUST be derived from source files referenced in the checklist item, 100% accuracy based on source materials, document negative evidence when verification fails)
> 5. **Evidence on Failure Only** — Log to task notes ONLY if unable to complete due to blockers, missing info, or errors (successful completion is evidenced by the output file itself)
> 6. **Explicit Completion Gate** — "This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete."

**Exact field names confirmed (these are the labels the template uses):** `Context Reference with WHY`, `Action with WHY`, `Output Specification`, `Integrated Verification`, `Evidence on Failure Only`, `Explicit Completion Gate`. NOTE: the brief's guessed labels ("Context/Action/Output/Verification/Completion gate") are close but the template's literal names differ — element 4 is "Integrated Verification" (an `ensuring...` clause, NOT a separate item), element 5 is "Evidence on Failure Only" (NOT a generic output field), and there is no field literally named "Completion gate" — it is "Explicit Completion Gate".

PART 2 restates the same 6 elements in the orchestrator instruction block (L970-976), labeled: 1. Context Reference + WHY, 2. Action + WHY, 3. Output Specification, 4. Integrated Verification, 5. Evidence on Failure Only, 6. Completion Gate.

### B3 — Single-paragraph form (template L150-153)
Each item is ONE FULL PARAGRAPH (not multiple lines or bullets), verbose and explanatory, readable as a complete prompt executable without prior context.

### B4 — Canonical correct example (template L155-162)
The exemplar item is the `component-spec.md` → `BaseHandler.ts` → `ApiHandler.ts` paragraph (L157). It ends with the literal error-handling + completion clause:
> "...If unable to complete due to missing information, file access issues, or unclear requirements, log the specific blocker using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete."
L160-162 NOTE: "Do NOT create separate verification items. Verification requirements are integrated into the action item above (the 'ensuring...' clause). The QA process handles verification between batches."

### B5 — FORBIDDEN patterns (template L164-183)
- Standalone "read context" items that produce no output (e.g. `Read file X and log findings` ❌).
- Missing context reference / no source of truth (e.g. `Create ApiHandler.ts with proper methods` ❌ — what methods? from where?).
- Multi-line / bulleted items (must be single paragraph; `**Context:** ... **Action:** ... **Output:**` formatting ❌).
- Separate verification/confirmation items (integrate via "ensuring..." clause).
- Overly granular items (e.g. "create directory" alone).
- Separate REMINDER blocks between checklist items.

### B6 / B7 (template L185-196)
B6 preferential: context-source refs (when reading sources), output specs (when producing files). B7 key principles: each item is a complete independently-executable prompt; context embedded IN the action; verification embedded via "ensuring..."; output files = evidence; only log on FAIL/BLOCK; one verbose paragraph; QA handles inter-batch verification (do NOT create separate verification items).

---

## 4. Section C — Embedding requirements (NOT separate sections) (template L198-230)

These are collected during planning but MUST be EMBEDDED in items, never as standalone sections:
- **C1 Outputs & Deliverables** (L206-211) — embed exact path/name/content/template in the creating item; the output file IS the completion evidence. Do NOT create an "Outputs & Deliverables" section.
- **C2 Success Criteria** (L213-217) — embed as "ensuring..." clause. Do NOT create a "Success Criteria" section.
- **C3 Verification** (L219-223) — embed in action items via "ensuring..."; QA process handles inter-batch verification (I15 phase-gate, I17 post-completion). Do NOT create a "Verification Checklist" section.
- **C4 Task Completion** (L225-230) — handled by Post-Completion Actions; items for frontmatter update + Execution Log. Do NOT create a "Task Completion and Handoff Protocol" section; orchestrator/handoff info lives in `ib_agent_core.md`.

---

## 5. Section D + E — Mandatory sections & checklist structure

### D — Mandatory sections (template L232-272)
- D1 Workflow Compliance Declaration [WORKFLOW-DEPENDENT] — informational only, no checklist items.
- D2 Cross-Stage Integration Requirements [WORKFLOW-DEPENDENT] — informational only; actual read items go in Phase 1 Step 1.4.
- **D3 CRITICAL RULE (L269-272):** "NO CHECKLIST ITEMS may appear before Phase 1 begins." Order: Frontmatter → Workflow Compliance (informational) → Prerequisites (informational) → Phase 1 (executable). All context-review / previous-stage-input read items appear IN Phase 1, Steps 1.2-1.4.

### E — Checklist structure rules (anti-orphaning core) (template L274-388)
- **E1 (L278-292):** Every actionable item is a flat checkbox `- [ ]`. NO nested checkboxes, NO parent checkboxes summarizing children. Use `**Step X.Y:**` headers for grouping, not checkboxes. Items in exact completion order. Never reference checkboxes that appear later.
- **E2 (L294-348) FUNDAMENTAL RULE:** "Summary/parent checkboxes MUST come AFTER all their component items." Never put a parent checkbox before its children; always place summary checkboxes at the END. Indented checklists allowed ONLY when they have no parent checkbox above them. Forbidden: parent-before-children, summary-in-middle.
- **E3 (L350-365) SEQUENTIAL ORDER:** Work flows top→bottom only. Never require marking items above current position. Forbidden phrases: "Mark item complete in section above", "Update the section checklist", "See checklist below", "Return to phase and mark complete", any backward movement.
- **E4 (L367-388):** Never place checkboxes next to step numbers (bold headings, no checkbox). DO NOT include separate REMINDER blocks between items (worker agents only see batch items, not surrounding text) — integrate reminders INTO the item.

---

## 6. Section L — Intra-task handoff patterns (Template-02-specific) (template L710-836)

These are what makes Template 02 distinct from 01. Handoff files live in `.dev/tasks/TASK-NAME/phase-outputs/` with subdirs `discovery/`, `test-results/`, `reviews/`, `plans/`, `reports/` (L719-726). Files persist across all batches/rollovers; later items read them by path (L728-730). "WHEN TO USE (L732-735): when items depend on info produced by earlier items. If every item is independent, use template 01 instead."

| Pattern | When (template L#) | Key rule | Output dir |
|---|---|---|---|
| **L1 Discovery** | L737-747 — explore codebase/env/data, produce structured findings later items consume | The discovery file IS the deliverable; write machine-readable output | `discovery/` |
| **L2 Build-from-Discovery** | L749-759 — create output based on a discovery item's findings | Always reference BOTH the discovery file path AND the source file path (discovery = WHAT, source = CONTENT) | deliverable path |
| **L3 Test/Execute** | L761-771 — run a command/script/test suite, capture results | Capture BOTH raw output AND a structured summary | `test-results/` |
| **L4 Review/QA** | L773-783 — assess quality of a previous output vs source/spec | Produce a structured verdict (PASS/FAIL) with specific findings; never "looks good" | `reviews/` |
| **L5 Conditional-Action** | L785-797 — branch on a previous item's result | MUST handle BOTH branches (success AND failure); output file always created | `plans/` |
| **L6 Aggregation** | L799-809 — consolidate multiple outputs into one report (usually final item of a phase) | Use Glob to discover files dynamically; don't hardcode file lists | `reports/` |

**L7 Pattern Selection Guide (L811-835)** maps need→pattern and gives common phase structures:
- Discovery→Build→Review: `L1 → L2(per item) → L4(per item) → L6`
- Build→Test→Fix: `K1/K2 → L3 → L5`
- Full Lifecycle: `L1 → L2 → L3 → L5 → L4 → L6`
- Full Lifecycle with QA Gates: `L1 → L2 → M1(QA Gate) → L3 → L5 → L4 → L6 → M1(QA Gate)`

**Section M — Phase-gate composite patterns (L837-860):** M1 = a 2-3 item phase-gate QA sequence (Item1 L6 aggregation → Item2 rf-qa spawn (+ optional rf-qa-qualitative) → Item3 L5 conditional proceed/fix-cycle). M2 = applicability table (research tasks: research-gate/synthesis-gate/report-validation; document tasks: document-type gate; code tasks: after implement before test; task-building: research-gate + task-integrity).

---

## 7. Required document sections + order (PART 2, template L890-1204)

The emitted task file body order:
1. `# [Task Title]` (L890)
2. `## Task Overview` (L892) — comprehensive description of what + why.
3. `## Key Objectives` (L896) — numbered bold objectives ("The following objectives MUST be achieved...").
4. `## Prerequisites & Dependencies` (L904) with subsections:
   - `### Parent Task & Dependencies` (L906)
   - `### Previous Stage Outputs (MANDATORY INPUTS)` (L914) — INFORMATIONAL ONLY, no checklist items.
   - `### Handoff File Convention` (L928) — names the `phase-outputs/` dir + subdirs (Template-02-specific).
   - `### Frontmatter Update Protocol` (L943)
   - (Example also inserts a `### Execution Context Constraints` / `### Execution Environment Constraints` subsection here — see example L81-87 — this is the "optional Execution Context" the brief mentions; it carries branch/code-location/UV/assertion constraints.)
5. `## Detailed Task Instructions` (L954) — contains an orchestrator instruction block (HTML-commented, REMOVED from output) then the phases.
6. `### Phase 1: Preparation and Setup` (L1012) — Step 1.1 status update, Step 1.2 create handoff dirs. (Step 1.1 is ALWAYS the status-→Doing item per I11 L569-571.)
7. `### Phase 2: [Main Execution Phase Name]` (L1063) — uses L-patterns (Steps 2.1 discovery, 2.2 build, 2.3 test, 2.4 assess in the template skeleton).
8. `### Phase Gate: Quality Verification` (L1090) — QA-gate items (insert when Phase 3 depends on Phase 2 outputs; I15-I16, M1-M2).
9. `### Phase [N]: Testing & Verification` (L1098) — insert when task modifies source code (I18); use L3 pattern.
10. `### Phase 3: [Review and Quality Assessment]` (L1106) — Step 3.1 L4 review, Step 3.2 L6 aggregate.
11. `## Post-Completion Actions` (L1118) — see anti-orphaning below.
12. `## Task Log / Notes 📋` (L1128) with sub-sections: `### Task Summary` (filled in post-completion), `### Execution Log`, `### Phase N - [Name] Findings` (one per phase), `### Phase Gate Findings`, `### Follow-Up Items Identified`, `### Deviations from Process`.

---

## 8. Anti-orphaning rule — completion items inside the final section

**Where completion lives:** the `## Post-Completion Actions` section (template L1118-1126) holds the terminal items, placed AFTER all execution phases and BEFORE the Task Log. Per I13 (L580-585) and I17 (L626-635), the order WITHIN Post-Completion Actions is:
1. **Verify outputs** (L1120) — Glob-confirm every specified output file exists on disk; log missing ones to Follow-Up Items.
2. **Run tests if code modified** (L1122) — re-run relevant suite (or note "Tests verified in Phase [N]").
3. **Create Task Summary** (L1124) — fill `### Task Summary` at top of Task Log.
4. **Frontmatter update LAST** (L1126) — set `completion_date`/`updated_date` + `status` to `🟢 Done`, then append Execution Log entry.

I17 (L627-633): "Before the frontmatter status is set to Done" the task MUST validate (a) all `- [ ]` marked `- [x]`, (b) all output files exist (Glob), (c) blocker entries have resolution notes, (d) if source code modified, tests pass. "These items appear in the ## Post-Completion Actions section of PART 2, BEFORE the frontmatter update item." So the frontmatter-→Done item is structurally the LAST checkbox in the file — validation/verification items precede it; nothing is left orphaned after Done.

D3 (L269-272) is the front-end anti-orphaning rule (no checklist items before Phase 1); E2/E3 forbid backward-referencing/parent-first items; I17 + Post-Completion ordering is the back-end anti-orphaning rule (completion is the last item, gated by validation items above it).

---

## 9. Section F/I — Execution & additional building guidelines (selected)

- **F1 (L394-403):** Five-step loop READ → IDENTIFY → EXECUTE → UPDATE → REPEAT (one item at a time).
- **F2 (L405-412) / F2a (L414-430):** Prohibited — multi-item execution, skipping phases, delegating across phase boundaries, skipping phase-gate QA, skipping post-completion validation. Parallel-spawning exception (L430): consecutive SAME-phase items spawning INDEPENDENT subagents may be spawned in parallel; mark each individually.
- **F5 (L447-451):** Frontmatter update protocol (start→Doing, complete→Done, blocked→Blocked, each session→updated_date) — mirrored in PART 2 L943-952.
- **I8 (L546-555):** MANDATORY template usage — "create a complex task" implicitly = "use the 02 template"; never create tasks without templates.
- **I11 (L569-571):** Status→🟠 Doing must be the FIRST action; context review comes after.
- **I12 (L573-578):** Verification is integrated, NO separate verification items.
- **I15 (L599-607):** Phase-gate QA enforcement — every task with 2+ phases MUST have ≥1 phase-gate QA checkpoint (aggregation item + rf-qa spawn item + conditional-action item) between the primary execution phase and any dependent later phase.
- **I16 (L609-624):** QA gate verdicts are binary PASS/FAIL (any severity issue = FAIL). Fix-cycle caps by gate type: research-gate 3 / synthesis-gate 2 / report-validation 3 / task-integrity 2 / any qualitative gate 3. On max reached: HALT+escalate (research/report/qualitative) or unresolved→Open Questions (synthesis/task-integrity).
- **I17 (L626-635):** Post-completion validation protocol (see §8).
- **I18 (L637-646):** Testing required for code-modifying tasks — ≥1 testing item specifying command, pass criteria, results capture path, B2 pattern; use L3.

---

## 10. Example: fully-formed B2 item + frontmatter (from TASK-RF-20260603-211955)

### Frontmatter block (example L1-43) — verbatim
```yaml
---
id: "TASK-RF-20260603-211955"
title: "Broaden per-task error_max_turns recovery to accept tail completion-verdict evidence"
description: "Extend the merged per-task error_max_turns recovery gate in the sprint harness (_task_completed_before_overrun) so it ALSO recovers an overrun whose completion evidence is a strong completion verdict in the NDJSON tail (not a subtype:success / task_complete envelope), closing the detection gap surfaced by TUIBBS V1 MVP sprint Phase 7 / task T07.05."
status: "🟢 Done"
type: "🛠 Code Fix"
priority: "🔼 High"
created_date: "2026-06-03"
updated_date: "2026-06-03"
assigned_to: "rf-task-executor"
autogen: false
autogen_method: ""
coordinator: orchestrator
parent_task: ""
depends_on: []
related_docs:
- path: "/config/workspace/TUIBBS-scp/.dev/troubleshoot/phase7-gate-error-20260603/REPORT.md"
  description: "Full diagnosis of the Phase 7 / T07.05 detection gap this task closes"
- path: "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260603-211955/research/01-grounding-and-design.md"
  description: "Exact code, insertion line numbers, and tests to add"
- path: "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260603-211955/research-notes.md"
  description: "File inventory, patterns, test conventions, and constraints"
tags:
- "sprint-harness"
- "executor"
- "recovery-gate"
- "error-max-turns"
- "bugfix"
template_schema_doc: ""
estimation: "1-2h"
sprint: ""
due_date: ""
start_date: "2026-06-03"
completion_date: "2026-06-03"
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
Confirms the full field set from §1 is used in practice (every template field present; `depends_on: []` and `parent_task: ""` used for a standalone task; `related_docs` carries 3 entries pointing at the diagnosis report + research files).

### Representative fully-formed B2 item (example Step 2.1, L126) — verbatim
> - [x] Read the file `01-grounding-and-design.md` at `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260603-211955/research/01-grounding-and-design.md` (section "The fix", step 1) to obtain the EXACT regex and window constant to add and the reason they are tail-scoped and conservative, then read the file `executor.py` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py` around lines 1820-1823 to confirm the existing `_TASK_SUCCESS_ENVELOPE_PATTERN` module-level definition (the new pattern must sit immediately AFTER it, ~L1823, and the existing envelope pattern MUST be left intact), then update `executor.py` by inserting, immediately after the `_TASK_SUCCESS_ENVELOPE_PATTERN` definition, the new module-level `_TASK_TAIL_COMPLETION_PATTERN = re.compile(...)` together with `_TASK_TAIL_COMPLETION_WINDOW = 15`, preceded by the explanatory comment block ... ensuring the regex tokens and `re.IGNORECASE` flag match the design EXACTLY with no fabricated tokens, the existing `_TASK_SUCCESS_ENVELOPE_PATTERN` is unchanged, and no placeholder text remains. If unable to complete due to the source structure differing from the verified line numbers, file access issues, or unclear requirements, log the specific blocker using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

Maps to B2's 6 elements: **Context+WHY** = read design file + executor.py "to obtain the EXACT regex"/"to confirm the existing pattern"; **Action+WHY** = "update executor.py by inserting..."; **Output Spec** = exact symbol names + location "~L1823"; **Integrated Verification** = "ensuring the regex tokens and re.IGNORECASE flag match the design EXACTLY with no fabricated tokens... no placeholder text remains"; **Evidence on Failure Only** = "If unable to complete... log the specific blocker using the templated format in the ### Phase 2 Findings section..."; **Completion Gate** = "Once done, mark this item as complete." Single paragraph, verbose — matches B3.

### Phase structure of the example
Phase 1 Preparation (1.1 status→Doing, 1.2 branch from master, 1.3 baseline) → Phase 2 Implement (2.1 add pattern, 2.2 add branch, 2.3 docstring) → Phase 3 Add tests (3.1-3.3) → Phase 4 Testing/Validation/Regression (4.1 new tests, 4.2 full-suite diff, 4.3 make lint, 4.4 make verify-sync) → **Phase Gate: Final Quality Verification (PG.1 spawn rf-qa task-integrity, max 2 fix cycles)** → Phase 5 Commit and Ship PR. This is the "Build → Test → QA-gate → Ship" composite, an instance of M1 + I15/I16.

### How completion/verification items are phrased (example)
- The example embeds verification inside each action item via the "ensuring..." clause (no separate verify items), exactly per B2/C3/I12. E.g. Step 4.2 (L164): "...ensuring the diff demonstrates exactly 0 NEW failures... and treating any single NEW failure as a regression that MUST be fixed before proceeding..."
- The phase-gate item (PG.1, L180) is a self-contained rf-qa spawn item: names agent (`rf-qa`), mode (`task-integrity`), inputs (the modified files + design + Phase 4 evidence), output path (`phase-outputs/reviews/final-qa-report.md`), binary verdict handling ("IF FAIL... re-spawn rf-qa in fix-cycle mode... MAXIMUM of 2 fix cycles (task-integrity gate per I16)... if still FAIL after 2 cycles, record... as Open Questions... escalate by leaving status as ⚪ Blocked"), and the error clause — exactly the M1/I15 shape.
- Every item ends with the literal completion gate "Once done, mark this item as complete." and (for executed items) is marked `- [x]`.

---

## 11. Common pitfalls the template explicitly warns about

1. **Standalone "read context" items** (B1/B5, K-block L979) — read with no output; context lost after rollover. Most-emphasized pitfall.
2. **Missing context reference** (B5 L170-174) — "Create X with proper methods" with no source of truth.
3. **Multi-line / bulleted items** (B5 L175-180, B3) — must be ONE paragraph, not `**Context:**/**Action:**/**Output:**` bullets.
4. **Separate verification/confirmation items** (B5, C3, I12) — verification must be the "ensuring..." clause inside the action item; QA handles inter-batch verification.
5. **Parent-before-children / summary-in-middle checkboxes** (E2 L327-341, the PART 2 ⚠️ warning L963-964) — summaries go LAST.
6. **Checklist items before Phase 1** (D3 L269-272) — nothing executable before Phase 1.
7. **Backward-movement instructions** (E3 L357-365) — "mark item above", "see below", "return to phase".
8. **Separate REMINDER blocks between items** (E4 L371-372, B5) — worker agents only see batch items, not surrounding prose; integrate reminders into the item.
9. **Overly granular items** (B5 L182) — e.g. "create directory" alone; combine with the file creation that needs it.
10. **Worker dynamically adding checklist items** (K2 L694-696) — orchestrator MUST pre-enumerate ALL items; worker NEVER adds them.
11. **Creating standalone sections that should be embedded** (C1-C4) — no "Outputs & Deliverables" / "Success Criteria" / "Verification Checklist" / "Task Completion and Handoff Protocol" sections.
12. **Fabrication/hallucination** (I9 L557-561, I14 L587-597, B2 element 4) — 100% accuracy from source; document negative evidence on failure.
13. **Skipping QA gates / post-completion validation** (F2 L411-412, I15, I17) — a task with 2+ phases must have a phase-gate; Done must be preceded by validation items.
14. **Using Template 02 when 01 suffices** (L732-735, I8 L548) — if all items are independent (just creating files from specs), use Template 01; Template 02 is for handoff/discovery/test/review/conditional/aggregation flows.

---

## Summary

Template `02_mdtm_template_complex_task.md` is a single file split by HTML-comment fences into **PART 1 (build instructions, Sections A-M, L46-870, all inside one comment so never emitted)** and **PART 2 (the emittable task body, L872-1204)**; the YAML frontmatter (L1-44) is part of the emitted output. Template 02 = Template 01 + Section L handoff patterns.

Key building rules captured verbatim: **A3** (complete granular breakdown — atomic item per file/component/iteration, NO bulk operations = the batch-item violation), **A4** (iterative enumerate→per-item→consolidate), **B2** (the 6 mandatory self-contained-item elements: Context Reference with WHY / Action with WHY / Output Specification / Integrated Verification "ensuring..." clause / Evidence on Failure Only / Explicit Completion Gate — confirmed exact names; the brief's guessed labels were close but inexact), **E1-E3** (flat checkboxes, summaries LAST, top-to-bottom only), and **L1-L6** (Discovery / Build-from-Discovery / Test-Execute / Review-QA / Conditional-Action / Aggregation, writing to `phase-outputs/{discovery,test-results,reviews,plans,reports}/`).

The required frontmatter set is LARGER than the brief listed (full table in §1) — includes description, autogen, autogen_method, coordinator, parent_task, depends_on, sprint, due_date, start_date, completion_date, blocker_reason, ai_model, model_settings, review_info beyond the brief's subset. status enum = 🟡 To Do / 🟠 Doing / 🟢 Done / ⚪ Blocked; type observed = 📝 Documentation / 🛠 Code Fix; priority = 🔼 High.

Document section order (PART 2): Task Overview → Key Objectives → Prerequisites & Dependencies (Parent/Deps, Previous Stage Outputs [informational], Handoff File Convention, Frontmatter Update Protocol, + optional Execution Context constraints) → Detailed Task Instructions (Phase 1 Prep → Phase 2 main → Phase Gate → optional Testing phase → Phase 3 Review) → Post-Completion Actions → Task Log / Notes. **Anti-orphaning** is enforced at both ends: D3 forbids any checklist item before Phase 1; I17 + the Post-Completion ordering put validation items (all items checked, all outputs exist via Glob, tests pass) BEFORE the final frontmatter-→Done item, making the Done update the structurally-last checkbox.

The example file (TASK-RF-20260603-211955, a 🛠 Code Fix) demonstrates the patterns in practice: full frontmatter, single-paragraph B2 items each ending "Once done, mark this item as complete.", an `### Execution Environment Constraints` subsection, verification embedded as "ensuring..." clauses (no separate verify items), and a `Phase Gate: Final Quality Verification` step spawning rf-qa in task-integrity mode with a max-2-fix-cycle conditional (M1/I15/I16). The 14 documented pitfalls (§11) center on the session-rollover hazard that motivates self-containment.

Research file: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260606-164424/research/06-mdtm-template-examples.md`
