# Research: Template & Examples (MDTM Template 01)
**Topic type:** Template & Examples
**Scope:** Template 01 PART 1 + smallest TASK-RF done example
**Status:** Complete
**Date:** 2026-05-26
**Template source:** `/config/workspace/IronClaude/.claude/templates/workflow/01_mdtm_template_generic_task.md` (997 lines)
---

## 1. PART 1 Mandatory Sections (from PART 2 template body, lines 730-996)

Every output task file MUST include these top-level sections (quoted verbatim):

| Section header | Template line | Required? | Notes |
|---|---|---|---|
| `# [Task Title]` | 730 | YES | H1 title |
| `## Task Overview` | 732 | YES | Comprehensive description |
| `## Key Objectives` | 736 | YES | Numbered list of concrete outcomes |
| `## Prerequisites & Dependencies` | 744 | YES | Has 3 subsections (below) |
| `### Parent Task & Dependencies` | 746 | YES | Parent / blocking deps / blocks |
| `### Previous Stage Outputs (MANDATORY INPUTS)` | 754 | YES | INFORMATIONAL ONLY; no checklist items |
| `### Frontmatter Update Protocol` | 768 | YES | Status update rules |
| `## Detailed Task Instructions` | 779 | YES | Container for phases |
| `### Phase 1: Preparation and Setup` | 821 | YES | First execution phase (status update only) |
| `**Step 1.1:** Update task status` | 853 | YES | First executable checklist item |
| `### Task-Specific Context Files` | 857 | YES | Reference list (not items) |
| `### Phase 2: [Main Execution Phase Name]` | 868 | YES | Main work phase |
| `### Phase Gate: Quality Verification` | 887 | Conditional | Required when Phase 2 outputs feed Phase 3 (I15) |
| `### Phase [N]: Testing & Verification` | 895 | Conditional | Required when task modifies source code (I18) |
| `### Phase 3: [Additional Phase if Needed]` | 903 | Optional | Add as needed |
| `## Post-Completion Actions` | 911 | YES | 4 items: glob verify, test verify, summary, frontmatter+log |
| `## Task Log / Notes 📋` | 921 | YES | Container for findings/logs |
| `### Task Summary` | 923 | YES | Filled in Post-Completion |
| `### Execution Log` | 948 | YES | Timestamped entries |
| `### Phase 1 - [Phase Name] Findings` | 958 | YES | One per phase |
| `### Phase 2 - [Phase Name] Findings` | 968 | YES | One per phase |
| `### Phase 3 - [Phase Name] Findings` | 977 | When Phase 3 exists | |
| `### Phase Gate Findings` | 979 | When QA gate exists | |
| `### Follow-Up Items Identified` | 983 | YES | |
| `### Deviations from Process` | 989 | YES | |

**FORBIDDEN sections** (per Section C): "Outputs & Deliverables", "Success Criteria", "Verification Checklist", "Task Completion and Handoff Protocol" — all of these are EMBEDDED into checklist items, not separate sections.

## 2. Item Structure Rules (Section B, lines 138-192)

Per **B2** (lines 138-144), EVERY checklist item is a **single-paragraph self-contained prompt** with 6 mandatory elements:

1. **Context Reference with WHY** — what file(s) to read and why (line 139)
2. **Action with WHY** — what to do and why (line 140)
3. **Output Specification** — exact file name, location, content, template (line 141)
4. **Integrated Verification** — `"ensuring..."` clause; "DO NOT assume, hallucinate, or make up any information — all content MUST be derived from source files referenced in the checklist item, 100% accuracy based on source materials, document negative evidence when verification fails" (line 142)
5. **Evidence on Failure Only** — log to task notes ONLY if blocked (line 143)
6. **Explicit Completion Gate** — verbatim string: *"This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete."* (line 144)

**B3** (line 146-149): Each item is ONE FULL PARAGRAPH — verbose, explanatory, not multi-line or bulleted.

**B4 canonical example** (line 153) — a single ~300-word paragraph with all 6 elements.

## 3. Granularity Rules (A3, A4)

**A3 — COMPLETE GRANULAR BREAKDOWN** (lines 87-91):
> Break down EVERY workflow phase into atomic, verifiable checklist items
> Create individual checklist items for EVERY file, component, or iteration
> NO high-level or bulk operations allowed - everything must be granular
> Include exact file paths, specific requirements, and measurable outcomes

**A4 — ITERATIVE PROCESS STRUCTURE** (lines 93-112): For any multi-item process:
- Pre-enumerate all items in initial step
- Create individual checklist item for EACH specific item
- Incremental updates after each item
- Consolidation step only after all items complete

For the PR A 7-step canonicalization fix: **each of the 7 steps MUST be its own atomic checklist item**. Batching is FORBIDDEN. If a step touches multiple files, per-file items are required.

## 4. Frontmatter Requirements (lines 1-44)

YAML frontmatter REQUIRED fields:
- `id: "TASK-[AGENT]-[TASKTYPE]-YYYYMMDD-HHMMSS"`
- `title:`
- `description:`
- `status: "🟡 To Do"` (initial)
- `type:` (e.g., "📝 Documentation", "✨ Feature", "🐛 Bug Fix")
- `priority:` (e.g., "🔼 High")
- `created_date: "YYYY-MM-DD"`
- `updated_date: "YYYY-MM-DD"`
- `assigned_to:`
- `autogen: false`
- `autogen_method: ""`
- `coordinator: orchestrator`
- `parent_task:`
- `depends_on:` (list)
- `related_docs:` (list of `path:` + `description:`)
- `tags:` (list)
- `template_schema_doc: ""`
- `estimation: ""`
- `sprint: ""`
- `due_date: ""`, `start_date: ""`, `completion_date: ""`, `blocker_reason: ""`
- `ai_model: ""`, `model_settings: ""`
- `review_info:` (last_reviewed_by/last_review_date/next_review_date)
- `task_type: static` (or `dynamic` per I6)

## 5. Common Pitfalls / FORBIDDEN Patterns

| Rule | Location | Prohibition |
|---|---|---|
| B5 | lines 161-179 | Standalone "read context" items with no output; missing context refs; multi-line/bulleted items; separate verification items; separate REMINDER blocks |
| C1 | lines 202-207 | No "Outputs & Deliverables" section |
| C2 | lines 209-213 | No separate "Success Criteria" items/section |
| C3 | lines 215-219 | No separate "Verification Checklist" items/section |
| C4 | lines 221-226 | No "Task Completion and Handoff Protocol" section |
| D3 | lines 265-268 | NO CHECKLIST ITEMS before Phase 1 begins |
| E1 | lines 274-288 | No nested checkboxes; no parent summary checkboxes; flat structure only |
| E2 | lines 290-344 | Parent-before-child FORBIDDEN (lines 323-329); summary-in-middle FORBIDDEN (lines 331-337) |
| E3 | lines 346-361 | No backward movement; no "see below"; no "return to phase" |
| E4 | lines 363-384 | No checkboxes on step-number headings; no REMINDER blocks between items |
| F2 | lines 401-409 | No working from memory; no multi-item execution; no skipping phases; no cross-phase subagent delegation; no skipping phase-gate QA (I15-I16); no skipping post-completion validation (I17) |
| I1 | lines 494-498 | No passive voice — use "YOU MUST" / "DO NOT" |
| I12 | lines 567-572 | NO separate "verify the file" / "confirm completion" items |
| I13 | lines 574-579 | No separate "Task Completion and Handoff Protocol" |

**I15 — Phase-Gate QA** (lines 593-601): Tasks with 2+ execution phases MUST include a QA checkpoint between primary phase and dependent phases. Must spawn `rf-qa` or `rf-qa-qualitative` with self-contained 6-element prompt.

**I16 — Fix Cycle Limits** (lines 603-618): Binary PASS/FAIL verdict; any-severity issue = FAIL. Max cycles: task-integrity gate = 2, qualitative gate = 3.

**I17 — Post-Completion Validation** (lines 620-629): Before frontmatter→Done, MUST verify all items checked, all output files exist (via Glob), blockers have resolution, modified-code tests pass.

**I18 — Code-Modifying Tasks** (lines 631-638): If code is modified, MUST include test items specifying (1) test command, (2) pass criteria, (3) results capture path, (4) self-contained pattern.

## 6. Done-Task Example: TASK-RF-20260518-cliEval-P4-wire-and-ship (211 lines)

Smallest TASK-RF reference example. Path: `/config/workspace/IronClaude/.dev/tasks/done/TASK-RF-20260518-cliEval-P4-wire-and-ship/TASK-RF-20260518-cliEval-P4-wire-and-ship.md`

**Overall structure (matches template 01):**
- Frontmatter (lines 1-52): all required fields populated
- `# Title` (line 54)
- `## Task Overview` (lines 56-60) — 2 paragraphs
- `## Key Objectives` (lines 62-70) — 7 bullets
- `## Prerequisites & Dependencies` (lines 72-80) — bullet list (does NOT use the deeper subsections from template; flat bullets acceptable for small tasks)
- `## Execution Context` (lines 82-87) — extra section (this task added References R-001..R-006 + Source areas + Key constraints; not part of base template but compatible)
- **7 Phases** with 17 checklist items total:
  - Phase 1: Setup & Prereq Verification (3 items: 1.1, 1.2, 1.3)
  - Phase 2: Wire eval_group (3 items: 2.1, 2.2, 2.3)
  - Phase 3: Makefile + gitignore + gitkeep (5 items: 3.1–3.5)
  - Phase 4: CliRunner wiring tests (3 items: 4.1–4.3)
  - Phase 5: Post-P4 Validation (4 items: 5.1–5.4)
  - Phase 6: Phase-Gate QA via rf-qa (2 items: 6.1, 6.2)
  - Phase 7: Commit + PR + completion (3 items: 7.1, 7.2, 7.3)
- `## Open Questions` (lines 165-171) — extra section, optional
- `## Task Log / Notes` (lines 175-211) — Execution Log + per-phase Findings + Follow-Up Items

**Item-format observations:**
- Each item is a single dense paragraph (200-500 words)
- Item numbering: `**N.M**` bolded prefix (e.g., `**1.1**`, `**2.3**`)
- Every item ends with: *"Once done, mark this item as complete."*
- Every item embeds the blocker-log pattern: *"log the specific blocker using the templated format in the ### Phase N Findings section of the ## Task Log / Notes at the bottom of this task file"*
- Output files use task-relative paths under `.dev/tasks/to-do/<TASK-ID>/phase-outputs/<discovery|test-results|reports|reviews>/`
- Verification clauses embedded via "ensuring..." — never separate items
- Phase headers are `## Phase N: ...` (H2) not H3 as the bare template shows; both work, this task uses H2

**Reference suitability for PR A 7-step canonicalization fix:**
- 7-step → likely 1 phase with 7 atomic items OR 2 phases (e.g., Phase 2 = 7-step canonicalization implementation, Phase 3 = tests/verification)
- This example demonstrates how to embed the rf-qa phase-gate (Phase 6) per I15 and the post-completion checklist (Phase 7) — both apply for a code-modifying canonicalization PR

---

## Summary

Template 01 PART 1 (lines 46-728) is the orchestrator's rulebook; PART 2 (lines 730-996) is the literal scaffold to copy. For PR A, the builder must produce: full frontmatter (28 fields), `# Title` -> `Task Overview` -> `Key Objectives` -> `Prerequisites` -> `Detailed Task Instructions` containing Phase 1 (status update), Phase 2 (the 7 canonicalization steps as 7 atomic single-paragraph items), Phase Gate (rf-qa per I15 since canonicalization is code-modifying), Phase 3/Testing (pytest per I18), Post-Completion Actions (4 items per I17), and Task Log / Notes container. Every item must contain all 6 B2 elements in ONE paragraph; A3 forbids batching; A4 mandates per-file granularity if a step touches multiples. The cliEval-P4 done example (211 lines, 7 phases, 17 items) confirms the shape, item density, and shows the rf-qa gate pattern verbatim — use it as the structural model.
