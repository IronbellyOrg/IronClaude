# Research: MDTM Template & Examples
**Topic type:** Template & Examples
**Scope:** `.claude/templates/workflow/02_mdtm_template_complex_task.md` PART 1 (lines 1-866); recent `TASK-RF-*` example
**Status:** Complete
**Date:** 2026-05-01

---

## 1. MDTM Template 02 — PART 1 Rules (Verbatim)

Source: `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md`
PART 1 spans lines 46-866. Template 02 = "extends Template 01 with Section L: Intra-Task Handoff Patterns. Use this template when tasks require discovery, testing, review, conditional logic, or aggregation between checklist items." Our 18-item task (mix of code edits, doc creation, GH issue batching, verification gates) qualifies — Template 02 is correct.

### 1.1 Frontmatter Schema (lines 1-44 — verbatim required fields)

The full schema from the template (line numbers 1-44):

```yaml
---
id: "TASK-[AGENT]-[TASKTYPE]-YYYYMMDD-HHMMSS"
title: "[Clear, Action-Oriented Task Title]"
description: "[Detailed description of what this task accomplishes and its purpose within the larger workflow]"
status: "🟡 To Do"
type: "📝 Documentation"
priority: "🔼 High"
created_date: "YYYY-MM-DD"
updated_date: "YYYY-MM-DD"
assigned_to: "[agent-name]"
autogen: false
autogen_method: ""
coordinator: orchestrator
parent_task: "[PARENT-TASK-ID]"
depends_on:
- "[DEPENDENCY-TASK-ID-1]"
- "[DEPENDENCY-TASK-ID-2]"
related_docs:
- path: "[path/to/governing/workflow.md]"
  description: "Parent workflow this task implements"
tags:
- "[relevant]"
- "[tags]"
template_schema_doc: ""
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

**Required fields confirmed:** `id`, `title`, `description`, `status`, `type`, `priority`, `created_date`, `updated_date`, `assigned_to`, `autogen`, `autogen_method`, `coordinator`, `parent_task`, `depends_on`, `related_docs`, `tags`, `template_schema_doc`, `estimation`, `sprint`, `due_date`, `start_date`, `completion_date`, `blocker_reason`, `ai_model`, `model_settings`, `review_info` (with 3 sub-fields), `task_type`.

**For our task:** `template_schema_doc` MUST be set to `".claude/templates/workflow/02_mdtm_template_complex_task.md"` (per reference example below). `task_type: static` (we know all 18 items at build time — no dynamic discovery). `autogen_method: "rf-task-builder"` per the reference example pattern.

### 1.2 SECTION A — Core Principles (the rules for granularity)

#### A3. COMPLETE GRANULAR BREAKDOWN (lines 91-95) — verbatim

```
A3. COMPLETE GRANULAR BREAKDOWN
   - Break down EVERY workflow phase into atomic, verifiable checklist items
   - Create individual checklist items for EVERY file, component, or iteration
   - NO high-level or bulk operations allowed - everything must be granular
   - Include exact file paths, specific requirements, and measurable outcomes
```

**Implication for our 18 items:** Each P-NNN/T-NNN item must be its own self-contained checklist item with exact file paths and measurable outcomes. **Phase 5's collapse of 13 deferred items into one GH-issue-creation item IS a documented deviation from A3** — it must be explicitly called out in the task body and in the Task Log / Notes "### Deviations from Process" section. The deviation rationale: per build request, the 13 deferred items are not in scope for this task — they are tracked externally as GitHub issues, so the single in-task item creates the issues (which IS atomic — it's one operation that produces N tickets). Document this deviation explicitly so QA does not flag it as an A3 violation.

#### A4. ITERATIVE PROCESS STRUCTURE (lines 97-116) — verbatim

```
A4. ITERATIVE PROCESS STRUCTURE
   - For ANY process involving multiple items (files, components, etc.):
     * Pre-enumerate ALL items to be processed in initial step
     * Create individual checklist item for each specific item
     * Require incremental updates after each item
     * Include consolidation step only after all items complete
   - Use this pattern:
     ``` markdown
     **Step X.1:** Scan and enumerate all [items] in [location]
     - [ ] Complete [item] listing generated: [count] items identified

     **Step X.2:** Process each [item] individually:
     - [ ] [Item 1]: [exact identifier] - [specific action] completed
     - [ ] [Item 2]: [exact identifier] - [specific action] completed
     [Continue for each item]

     **Step X.3:** Consolidate all individual results
     - [ ] All [count] items processed and results logged
     - [ ] Consolidated output created per requirements
     ```
```

**Implication:** Phase 5's GH-issue item is the one place we need A4-style enumeration internal to the item — the item must list all 13 issue titles inline (pre-enumerated) before invoking `gh issue create` in a loop. We do NOT split it into 13 items (that's the deviation), but the ONE item must internally enumerate all 13.

### 1.3 SECTION B — Self-Contained Items (THE critical section)

#### B1. WHY THIS MATTERS (lines 134-140) — verbatim

```
B1. WHY THIS MATTERS (SESSION ROLLOVER PROTECTION)
   Rigorflow executes tasks in batches across multiple sessions. Due to session
   rollovers (context limits), any context loaded in batch 1 will NOT be available
   in batch 3+. Therefore, EVERY checklist item MUST be self-contained - embedding
   all context references, actions, and outputs within a single item. Standalone
   "read context" items that don't produce actionable output are USELESS because
   that context will be lost before it can be used.
```

#### B2. THE 6-ELEMENT SELF-CONTAINED PATTERN (lines 142-148) — verbatim

```
B2. EVERY CHECKLIST ITEM MUST BE A COMPLETE, SELF-CONTAINED PROMPT THAT INCLUDES:
   1. **Context Reference with WHY** - What file(s) to read and why that context is needed for this specific action
   2. **Action with WHY** - What to do with that context and why it needs to be done
   3. **Output Specification** - The exact output file name, location, what content to produce, and template to follow (if applicable)
   4. **Integrated Verification** - An "ensuring..." clause that specifies what must be verified (DO NOT assume, hallucinate, or make up any information - all content MUST be derived from source files referenced in the checklist item, 100% accuracy based on source materials, document negative evidence when verification fails)
   5. **Evidence on Failure Only** - Log to task notes ONLY if unable to complete due to blockers, missing info, or errors (successful completion is evidenced by the output file itself)
   6. **Explicit Completion Gate** - "This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete."
```

#### B3. THE SELF-CONTAINED PATTERN (lines 150-153) — verbatim

```
B3. THE SELF-CONTAINED PATTERN
   Each checklist item should be written as ONE FULL PARAGRAPH (not multiple lines
   or bullets) that is verbose and explanatory. The item should read like a complete
   prompt that could be executed independently without any prior context.
```

**Critical rule for builder:** ONE PARAGRAPH per item. NO multi-line bullets. NO sub-bullets. NO formatted "Context:/Action:/Output:" labels. Single flowing paragraph.

#### B4. CORRECT EXAMPLE (lines 155-158) — verbatim

```markdown
- [ ] Read the file `component-spec.md` at `docs/specs/component-spec.md` to extract the API interface requirements including all method signatures, parameter types, and return values that must be implemented, then read the file `BaseHandler.ts` at `src/handlers/BaseHandler.ts` to understand the structural patterns and conventions used in existing handlers, then create the file `ApiHandler.ts` at `src/handlers/ApiHandler.ts` containing a TypeScript class that implements all methods defined in the component spec with proper error handling, type annotations, and JSDoc comments following the patterns from BaseHandler, ensuring the file includes the standard header comment block, exports the class as the default export, all methods from the spec are implemented with correct signatures, no content is fabricated or assumed beyond what the source explicitly states, and no placeholder or TODO comments remain. If unable to complete due to missing information, file access issues, or unclear requirements, log the specific blocker using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
```

#### B5. FORBIDDEN PATTERNS (lines 164-184) — summarized verbatim

- Standalone "read context" items that don't produce output (WRONG)
- Missing context reference (no source of truth) (WRONG)
- Multi-line/bulleted checklist items (must be single paragraph) (WRONG)
- Separate verification/confirmation items (integrate via "ensuring..." clause)
- Overly granular items (e.g., "create directory" alone)
- Separate REMINDER blocks between checklist items

#### Completion Gate Format (verbatim from B2.6)

```
"This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete."
```

In practice (B4 example, all reference task files), the shorter form is used at item end:

```
"...then mark this item complete. Once done, mark this item as complete."
```

This pairs with the failure-evidence clause to form the standard 2-sentence closer.

### 1.4 SECTION C — Embedding Requirements (anti-orphaning)

C1-C4 (lines 206-230): outputs, success criteria, verification, AND task completion are EMBEDDED IN ITEMS, not in separate sections. The relevant rule for our verification phase (Phase 6):

#### C3. VERIFICATION (lines 219-223) — verbatim

```
C3. VERIFICATION (embed in action items, NOT separate items)
   - Verification requirements MUST be embedded in each action item via "ensuring..." clause
   - Do NOT create separate verification checklist items
   - Do NOT create a "Verification Checklist" section in the task file
   - The intra-task QA process handles verification between batches — see I15 for phase-gate enforcement and I17 for post-completion validation
```

**Caveat for our Phase 6:** Phase 6 (verification gate) is NOT a "separate verification of one item" — it's the **post-completion validation phase** required by I17 (see below). I17 explicitly authorizes verification items in Post-Completion Actions. So Phase 6 items are LEGITIMATE per I17, not violations of C3.

#### C4. TASK COMPLETION (lines 225-230) — verbatim — ANTI-ORPHANING RULE

```
C4. TASK COMPLETION (final Post-Completion task items only)
   - Task completion is handled by the Post-Completion Actions section
   - Include items for: updating frontmatter (status, completion_date), logging completion to Execution Log
   - Post-completion validation items (I17) handle output verification; frontmatter update and task summary are the only Post-Completion Actions
   - Do NOT create a "Task Completion and Handoff Protocol" section in the task file
   - Orchestrator info about handoff lives in ib_agent_core.md, not in individual task files
```

**Anti-orphaning rule (where task-completion items go):** Task-completion items (status update to Done, completion_date, task summary, frontmatter close-out) go in the FINAL phase of the task — typically named **"Post-Completion Actions"** and placed as the last `### Phase N` block before `## Task Log / Notes`. Per the user's spec ("Phase 6 = verification gate"), Phase 6 in our build IS the verification phase but should ALSO contain the frontmatter close-out items (per I13 below). Alternatively, the builder MAY split into Phase 6 (verification gates) + a final "Post-Completion Actions" section with 2-3 frontmatter items — see reference example for pattern.

### 1.5 SECTION D — Mandatory Sections

#### D3. CRITICAL RULE (lines 269-272) — verbatim

```
D3. CRITICAL RULE
   NO CHECKLIST ITEMS may appear before Phase 1 begins. The template structure ensures:
   - Frontmatter → Workflow Compliance (informational) → Prerequisites (informational) → Phase 1 (executable)
   - All checklist items for context review and previous stage inputs appear IN Phase 1, Steps 1.2-1.4
```

### 1.6 SECTION E — Checklist Structure Rules

#### E1. CHECKBOX FORMAT (lines 278-292) — key rules

- EVERY actionable item MUST be a checkbox: `- [ ] Action text`
- NO nested checkboxes (flat structure only)
- NO parent checkboxes that summarize children
- Each checkbox is ONE atomic, verifiable action
- Use `**Step X.Y:**` headers for grouping, NOT checkboxes
- Checkboxes MUST appear in the exact order they will be completed

#### E2. CRITICAL CHECKLIST STRUCTURE RULES (lines 294-348) — summary

- Summary/parent checkboxes MUST come AFTER all their component items
- NEVER put a parent checkbox before its child components
- Use descriptive headers (`### Phase N` / `**Step X.Y:**`) instead of parent checkboxes
- Indented checklists allowed ONLY when they don't have a parent checkbox above them
- Work flows TOP to BOTTOM only

### 1.7 SECTION I — Additional Guidelines (key items for our task)

#### I15. PHASE-GATE QA ENFORCEMENT (lines 599-607) — verbatim

```
I15. PHASE-GATE QA ENFORCEMENT
   Every task with 2+ execution phases MUST include at least one phase-gate QA checkpoint between the primary execution phase and any subsequent phase that depends on its outputs. The orchestrator MUST insert QA gate checklist items at these boundaries.

   A phase-gate QA checkpoint consists of:
   1. An aggregation item that collects all outputs from the preceding phase
   2. A QA agent spawn item that verifies those outputs against defined criteria
   3. A conditional-action item that proceeds to the next phase on PASS or triggers a fix cycle on FAIL

   The QA agent spawn item MUST be a self-contained checklist item following B2's 6-element pattern. It MUST include: the agent to spawn (rf-qa or rf-qa-qualitative), the phase type, the input files, the output report path, the verdict handling (proceed on PASS, fix cycle on FAIL), and the error handling clause.
```

**Implication:** Our 6-phase task with code edits (Phase 1) → tests (Phase 2-3) → docs (Phase 4) → GH issues (Phase 5) → verification (Phase 6) needs at least one phase-gate. The user-specified Phase 6 verification gate satisfies the FINAL gate requirement. A phase-gate between Phase 3 (tests) and Phase 4 (docs) MAY be included if rigor demands it; the build request likely already specifies this — if not, builder should default to a single Phase 6 final gate.

#### I17. POST-COMPLETION VALIDATION PROTOCOL (lines 626-635) — verbatim

```
I17. POST-COMPLETION VALIDATION PROTOCOL
   Before the frontmatter status is set to Done, the task MUST include validation items that verify:
   1. All `- [ ]` items have been marked `- [x]` (no items skipped)
   2. All output files specified in checklist items exist on disk (verified via Glob)
   3. Any blocker entries in the Task Log have resolution notes
   4. If the task modified source code: all relevant tests pass

   These items appear in the ## Post-Completion Actions section of PART 2, BEFORE the frontmatter update item.

   The automated QA workflow references in C4 and I13 are satisfied by these validation items — no external workflow is required when the task file includes them.
```

**This is the source for our Phase 6 "4 verification gates":** the 4 gates ARE I17's 4 enumerated checks. Builder must produce 4 items mapping 1:1 to I17's enumerated list.

#### I18. TESTING REQUIREMENTS FOR CODE-MODIFYING TASKS (lines 637-646) — verbatim

```
I18. TESTING REQUIREMENTS FOR CODE-MODIFYING TASKS
   If a task creates or modifies source code files (not documentation, not configuration), the orchestrator MUST include at least one testing checklist item. This item MUST:
   1. Specify the test command to run (e.g., "Run `uv run pytest tests/path/ -v`")
   2. Define pass criteria (e.g., "all tests pass with no regressions")
   3. Specify where test results are captured (e.g., a test-results file in phase-outputs/)
   4. Follow the self-contained item pattern from B2

   For Template 02 tasks: use the L3 (Test/Execute) pattern for testing items.

   The orchestrator determines appropriate test scope based on the changes being made. At minimum, unit tests covering modified code are required.
```

**Implication:** Our task modifies code (P-006, P-009, P-011, P-012, T-012) → MUST include a testing item. Phase 3 (tests) likely fulfills this; if not, add an L3 test-execution item.

### 1.8 SECTION J — Error Handling (verbatim, lines 659-663)

```
J1. ERROR HANDLING PATTERN (embedded in every checklist item):
   "If unable to complete due to missing information, file access issues, or unclear
   requirements, log the specific blocker using the templated format in the ### Phase [N]
   Findings section of the ## Task Log / Notes at the bottom of this task file, then
   mark this item complete."
```

This is the standard B2.5 "Evidence on Failure" clause every item must include. Substitute `[N]` with the item's actual phase number.

### 1.9 SECTION L — Intra-Task Handoff Patterns (relevant patterns for our task)

L1-L6 (lines 711-836) define handoff item shapes. Patterns relevant to our task:

| Pattern | When | Our Items Using It |
|---------|------|---------------------|
| **L1 Discovery** | Item explores codebase/data and produces structured findings | (None — we know all sources up front) |
| **L2 Build-from-Discovery** | Item creates output based on discovery file | (None — no discovery phase) |
| **L3 Test/Execute** | Item runs a command/test suite and captures results | Phase 3 test-runs; verification gate items that run `pytest` |
| **L4 Review/QA** | Item assesses quality vs source/spec | Phase 6 verification gates |
| **L5 Conditional-Action** | Branch on previous item's result | Phase 6 final gate (PASS → mark Done; FAIL → mark Blocked) |
| **L6 Aggregation** | Consolidate multiple outputs | Phase 6 aggregation item collecting all phase outputs |

**L1-L6 handoff patterns DO apply to our Phase 6 verification phase.** They do NOT directly apply to Phase 4 doc-creation items (no upstream "discovery" feeds them — the build request itself is the source). The user's question about "Phase 4 ownership handoffs (branch-author → spec-keeper)" — these are SOCIAL handoffs (author → reviewer), not L-pattern handoffs (file-based information flow). L-patterns govern file artifacts; social ownership is documented in the item text itself ("...this item is assigned to the spec-keeper persona...") if the build request specifies persona ownership.

### 1.10 SECTION M — Phase-Gate Composite Patterns (lines 843-860)

M1 sequences 3 items at a phase boundary:
1. **Aggregation (L6):** Collect outputs from preceding phase
2. **QA Agent Spawn:** Spawn `rf-qa` (structural) or `rf-qa-qualitative` (operational); separate items if both required
3. **Conditional Proceed (L5):** Read QA report, proceed on PASS, fix cycle on FAIL

**M2 applicability table** says code-modifying tasks need a gate "after implementation phase and before testing phase (if testing is separate), or after combined implement+test phase". Our Phase 6 = the post-completion gate; whether to add an additional inter-phase gate is the builder's call based on rigor needs.

---

## 2. Reference Example: Recent Multi-Phase TASK-RF File

### 2.1 Selected Reference

**Path:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260402-baseline-repo/TASK-RF-20260402-baseline-repo.md`

**Why this reference:** 9 phases, 27 items, 352 lines, well-formed Template 02 task with verification gate (Phase 8) + Post-Completion Actions (Phase 9). Most directly mirrors our 6-phase + verification structure. Created by `rf-task-builder` (autogen_method confirmed in frontmatter). Done status, so passed QA validation.

### 2.2 Frontmatter Shape (verbatim, lines 1-43)

```yaml
---
id: "TASK-RF-20260402-baseline-repo"
title: "E2E Test 3: Run Spec Pipeline in Original Unmodified Repo (Baseline Comparison)"
description: "Execute the spec fixture through superclaude roadmap run in a git worktree of master (commit 4e0c621, pre-TDD changes), then compare Test 3 output against Test 2 (spec in modified repo) and Test 1 (TDD in modified repo) to prove spec-path behavior is unchanged and TDD expansion works correctly."
status: "Done"
type: "E2E Test"
priority: "high"
created_date: "2026-04-02"
updated_date: "2026-04-02"
assigned_to: ""
autogen: true
autogen_method: "rf-task-builder"
coordinator: orchestrator
parent_task: "TASK-E2E-20260326-tdd-pipeline"
depends_on:
- "TASK-E2E-20260326-tdd-pipeline (Test 1 and Test 2 must be complete)"
related_docs:
- path: ".dev/tasks/to-do/TASK-E2E-20260326-tdd-pipeline/E2E-TEST-PLAN.md"
  description: "Full E2E test plan specifying Test 3 verification and comparison criteria"
- path: ".dev/tasks/to-do/TASK-E2E-20260326-tdd-pipeline/BUILD-REQUEST-baseline-repo.md"
  description: "Build request with detailed phase descriptions and comparison tables"
- path: ".dev/tasks/to-do/TASK-RF-20260402-baseline-repo/research/"
  description: "Research workspace with 5 topic-specific research files"
tags:
- "e2e-test"
- "baseline-comparison"
- "roadmap-pipeline"
- "worktree"
template_schema_doc: ".claude/templates/workflow/02_mdtm_template_complex_task.md"
estimation: "2-3 hours (mostly pipeline execution wait time)"
sprint: ""
due_date: ""
start_date: "2026-04-02"
completion_date: "2026-04-02"
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

**Note:** This reference uses simplified statuses (`"Done"`, `"high"`) without emojis instead of the template's `"🟢 Done"` / `"🔼 High"`. Both forms are accepted by `rf-task-builder` outputs in this repo. Builder may use either; the simpler form matches the most recent reference.

### 2.3 Phase Structure (how phases group items in practice)

```
### Phase 1: Preparation and Setup (4 items)
  > Purpose: Update task status, verify prerequisites exist, and create handoff directories.
  **Step 1.1: Status Update and Prerequisites**
  - [ ] item 1
  - [ ] item 2
  **Step 1.2: Create Handoff Directories**
  - [ ] item 3
  **Step 1.3: Verify No Stale Worktree**
  - [ ] item 4

### Phase 2: ... (5 items)
  > Purpose: ...
  **Step 2.1: ...**
  - [ ] item

[... Phases 3-8 ...]

### Phase 8: Final QA Validation (3 items)
  > Purpose: Final quality gate. Per QA_GATE_REQUIREMENTS: FINAL_ONLY.
  **Step 8.1: Verify All Output Files Exist**
  - [ ] (I17.2 — Glob for output files)
  **Step 8.2: Verify Comparison Criteria Met**
  - [ ] (I17.4 — verify reports show PASS)
  **Step 8.3: Write Final Pass/Fail Verdict**
  - [ ] (final verdict aggregation)

### Phase 9: Post-Completion Actions (3 items)
  > Purpose: Verify all checklist items are complete, create task summary, update frontmatter to Done.
  **Step 9.1: Verify All Items Complete**
  - [ ] (I17.1 — count [x] vs [ ])
  **Step 9.2: Create Task Summary**
  - [ ] (update Task Log Task Summary)
  **Step 9.3: Update Frontmatter to Done**
  - [ ] (L5 conditional: PASS→Done, FAIL→Blocked)

## Task Log / Notes
### Task Summary
### Execution Log
### Phase 1 Findings
### Phase 2 Findings
[... one Findings section per phase ...]
### Follow-Up Items
```

**Key structural takeaways:**
- Each phase begins `### Phase N: [Name] (M items)` with item count in header
- Each phase has a `> **Purpose:** ...` blockquote immediately after the heading
- Items within a phase are grouped under `**Step X.Y: [Step Name]**` bold-text headers (NO checkbox on the step header itself)
- Tasks ARE allowed to have separate "Final QA Validation" + "Post-Completion Actions" phases (Phase 8 + Phase 9 pattern). Builder may collapse these into a single Phase 6 for our task, OR keep them split. The user-specified "Phase 6 = verification gate" maps cleanest to one phase containing BOTH the I17 checks AND frontmatter close-out — see fillable shape below.

### 2.4 Reference B2 Item — Quoted Verbatim

This is the most representative single-action Step 2.4 (Phase 2 of the reference task):

```markdown
- [x] Use the Bash tool to run `mkdir -p /Users/cmerritt/GFxAI/IronClaude-baseline/.dev/test-fixtures/results/test3-spec-baseline/` to create the test fixture and output directories in the worktree (`.dev/test-fixtures/` does not exist on master even though `.dev/` is tracked), then run `cp /Users/cmerritt/GFxAI/IronClaude/.dev/test-fixtures/test-spec-user-auth.md /Users/cmerritt/GFxAI/IronClaude-baseline/.dev/test-fixtures/test-spec-user-auth.md` to copy the spec fixture from the main repo into the worktree, then verify with `wc -l /Users/cmerritt/GFxAI/IronClaude-baseline/.dev/test-fixtures/test-spec-user-auth.md` that the file has approximately 312 lines, ensuring the spec fixture is present and complete in the worktree. If unable to complete due to missing source file or filesystem errors, log the specific blocker using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
```

This item demonstrates all 6 B2 elements in one paragraph: action (mkdir + cp + wc), why (directories don't exist on master / verify completeness), output (the copied file at exact path + 312 lines), ensuring clause (present and complete), failure-evidence clause, and explicit completion gate.

---

## 3. Builder-Specific Guidance — Fillable B2 Shapes Per Item Type

For each item type in our 18-item task, here is a fillable B2 template the builder can adapt. All templates produce ONE PARAGRAPH per item, single `- [ ]` checkbox, with all 6 B2 elements integrated.

### 3.1 Code-Fix Item Pattern (P-006, P-009, P-011, P-012, T-012)

For small, in-place source-code edits (1-line additions, 2-line captures, helper additions, format-string changes):

```markdown
- [ ] Read the file `<source-file>` at `<absolute/path/to/source-file>` to locate <the exact line/method/class to modify, identified by <unique anchor: function name, existing line content, line number range>>, then read the file `<spec-or-design-doc>` at `<absolute/path/to/spec.md>` <section heading or line range> to confirm the exact change required including <specific values, parameter names, format strings>, then use the Edit tool to <add | replace | insert> <N lines | the line containing X> in `<source-file>` so that <exact post-condition: e.g., "the function signature includes the new `cwd` parameter" or "PRD section 3.2 lists fingerprint `<value>`">, ensuring the change matches the spec exactly with no fabricated values, the surrounding code is not modified, no placeholder or TODO comments remain, and the file remains syntactically valid <Python | Markdown | YAML>. If unable to complete due to the anchor line being absent, ambiguous match, or spec mismatch, log the specific blocker using the templated format in the ### Phase <N> Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
```

**Filling guide:** `<source-file>` = exact target file (e.g., `src/superclaude/cli/spec_loader.py`). `<spec-or-design-doc>` = the design doc that authorizes the change (e.g., `RECONCILED_DESIGN.md` or `BEAT_2_BACKLOG.md`). `<N lines>` = literal count from build request. The "spec confirms exact change" embed satisfies B2.1 (context with WHY).

### 3.2 New-Test Item Pattern (P-007, P-008, T-013, T-014, T-015, T-016)

For creating a new test file from scratch:

```markdown
- [ ] Read the file `<spec-or-source-under-test>` at `<absolute/path>` to extract <the exact behavior to test, listed test cases, expected inputs and outputs>, then read the file `<existing-similar-test>` at `<absolute/path/to/existing/test.py>` to follow the project's pytest conventions including imports, fixture usage, naming, and assertion style, then create the file `<new-test-file>` at `<absolute/path/to/test_<feature>.py>` containing <a pytest test module with N test functions covering: test_case_1_description, test_case_2_description, ..., each function asserting <specific expected behavior> using <fixture names from existing tests>>, ensuring every test case from the spec is covered, all assertions reference real source-code symbols not placeholder names, no `# TODO` or `pass` stubs remain, the file imports follow the existing test conventions, and the test module runs (parses without SyntaxError) when invoked with `uv run pytest <new-test-file> --collect-only`. If unable to complete due to missing spec, missing source-under-test, or unclear test cases, log the specific blocker using the templated format in the ### Phase <N> Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
```

### 3.3 In-Place Test Edit Pattern (P-013)

For replacing an assertion block in an existing test:

```markdown
- [ ] Read the file `<existing-test-file>` at `<absolute/path/to/test_existing.py>` to locate the assertion block within the function `<test_function_name>` (identifiable by <existing assertion content, line range, or unique anchor>), then read the file `<spec-doc>` at `<absolute/path/to/spec.md>` section `<heading>` to confirm the new assertion semantics, then use the Edit tool to replace the existing assertion block with <a new assertion block that asserts: assertion_1, assertion_2, ...>, ensuring the replacement is exact (no surrounding code modified), the new assertions reference only real symbols from the source under test, the test function signature and fixtures remain unchanged, and the file remains parseable Python (verify with `uv run pytest <test-file> --collect-only` succeeding for `<test_function_name>`). If unable to complete because the anchor block is absent or matches multiple locations, log the specific blocker using the templated format in the ### Phase <N> Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
```

### 3.4 Doc-Creation Item Pattern (P-014, P-015)

For creating tracking documents (BEAT_2_BACKLOG.md, TRACEABILITY.md):

```markdown
- [ ] Read the file `<source-of-truth-1>` at `<absolute/path>` to extract <the items, fingerprints, or rows to populate the new doc>, then read the file `<source-of-truth-2>` at `<absolute/path>` to extract <complementary content: cross-references, ownership, status>, then create the file `<new-doc>` at `<absolute/path/to/<DOC_NAME>.md>` containing <document structure: H1 title, frontmatter (if applicable), sections H2: Overview, H2: <Section1>, H2: <Section2>, with a markdown table containing columns <Column1, Column2, Column3, ...> and one row per item from the source, plus a footer noting source files and date>, ensuring every item from the source-of-truth is represented as a row, all entries cite their source by file path or section, no fabricated entries are added, all markdown links resolve to real files, and the table is well-formed (no broken pipes, all rows have N columns). If unable to complete due to missing source data or ambiguous structure, log the specific blocker using the templated format in the ### Phase <N> Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
```

### 3.5 Build-Target Item Pattern (P-016)

For adding a Makefile target:

```markdown
- [ ] Read the file `Makefile` at `<absolute/path>/Makefile` to identify the location to insert the new target (typically at the end before `.PHONY` declarations or grouped with related targets like `<existing-target-name>`), then read the file `<design-doc>` at `<absolute/path>/<DESIGN_DOC>.md` section `<Build Targets>` to confirm the exact target name, command(s), and description required, then use the Edit tool to add a new Makefile target named `<target-name>` that runs `<exact-command-line>` with a `## <description>` comment for `make help` extraction, ensuring the target name matches the design doc exactly, indentation uses TAB (not spaces) per Makefile syntax, the target is added to `.PHONY` if non-file-producing, no existing targets are modified, and the Makefile parses without error (verify with `make -n <target-name>` showing the command without executing). If unable to complete due to Makefile syntax conflicts or missing prerequisite targets, log the specific blocker using the templated format in the ### Phase <N> Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
```

### 3.6 Spec-Amendment Item Pattern (P-010)

For editing a design document like RECONCILED_DESIGN.md:

```markdown
- [ ] Read the file `<design-doc>` at `<absolute/path/to/RECONCILED_DESIGN.md>` to locate <the section requiring amendment, identified by H2/H3 heading or unique paragraph anchor>, then read the file `<authoritative-source>` at `<absolute/path>` to extract the <new content / corrected values / additional rows> required by the amendment, then use the Edit tool to <add | replace | extend> the identified section with <the new content: paragraph, bullet list, table rows>, ensuring the amendment text is derived from the authoritative source with no fabricated content, the surrounding section structure (heading levels, neighboring content) is preserved, any cross-references to the amended section elsewhere in the doc are checked for consistency, the markdown remains well-formed, and the file's frontmatter (if present) `updated_date` field is updated to today's date. If unable to complete because the anchor section is absent, the authoritative source contradicts an existing claim, or the amendment introduces a circular reference, log the specific blocker using the templated format in the ### Phase <N> Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
```

### 3.7 GH-Issue-Batch Item Pattern (Phase 5 Collapsed Item)

For the single item that creates 13 GitHub issues in a loop:

```markdown
- [ ] Read the file `<deferred-items-spec>` at `<absolute/path/to/spec/listing/the/13/items>` to extract the list of 13 deferred items each with: title, body, labels, and milestone (this list is reproduced inline below for self-contained execution), then for each of the 13 items use the Bash tool to run `gh issue create --title "<title>" --body "<body>" --label "<label1,label2>" --milestone "<milestone>"` against the repository at `<owner/repo>`, capturing the returned issue URL for each, then write the consolidated mapping of all 13 created issues to the file `gh-issues-created.md` at `.dev/tasks/<TASK-NAME>/phase-outputs/reports/gh-issues-created.md` containing a markdown table with columns (Item ID, Issue Title, Issue URL, Labels, Milestone) and one row per created issue. The 13 deferred items to create are: (1) <ID-1>: <title-1> — <one-line body summary> [labels: ...]; (2) <ID-2>: <title-2> — ...; ... (13) <ID-13>: <title-13> — .... Ensuring all 13 issues are created (verify by counting rows in gh-issues-created.md), each issue title matches the item ID exactly, no fabricated content is added beyond what the spec provides, the issue URLs are real (HTTP 200 when accessed), and any `gh issue create` failure is logged with the failing item ID. If unable to complete because `gh` CLI is unauthenticated, the repository is unreachable, or any individual issue creation fails, log the specific blocker (including which items succeeded and which failed) using the templated format in the ### Phase 5 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

> **Deviation Note (per A3):** This single item collapses 13 individual deferred work items (originally one P-NNN per item) into one bulk gh-issue-creation operation. Per the build request, these 13 items are out of scope for this task and are tracked externally as GitHub issues. The collapse is intentional and is explicitly recorded in the ### Deviations from Process section of the ## Task Log / Notes.
```

**The deviation note (italic blockquote) IS allowed adjacent to the item** because it's prose context, not a checkbox. Place it directly under the `**Step 5.1: Create 13 GitHub Issues for Deferred Items**` step header. The same deviation must also be recorded in `### Deviations from Process` under `## Task Log / Notes` (which the template provides at line 1190).

### 3.8 Verification-Gate Item Pattern (Phase 6 — 4 Gates Mapping to I17)

The 4 gates correspond 1:1 to I17's 4 enumerated checks. Each is its own self-contained item:

**Gate 1 — All checkboxes marked (I17.1):**

```markdown
- [ ] Read the entire task file at `<absolute/path/to/this-task-file.md>` and use the Bash tool to run `grep -c "^- \[ \]" <absolute/path/to/this-task-file.md` to count remaining unchecked items and `grep -c "^- \[x\]" <absolute/path/to/this-task-file.md` to count checked items, then create a verification summary file `gate1-checkboxes.md` at `.dev/tasks/<TASK-NAME>/phase-outputs/reports/gate1-checkboxes.md` containing the unchecked count, checked count, total count, and a PASS/FAIL verdict (PASS only if unchecked count equals exactly the count of remaining gate items in this Phase 6 itself, including this gate item — i.e., no items in Phases 1-5 are unchecked), ensuring the counts are derived from the actual file contents with no fabricated numbers, and any unchecked items in Phases 1-5 are listed with their step number and line for follow-up. If unchecked items exist in Phases 1-5, the gate FAILs and a fix-cycle item should be triggered (re-execute the unchecked steps, then re-run this gate). If unable to read the task file, log the specific blocker using the templated format in the ### Phase 6 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
```

**Gate 2 — All output files exist (I17.2):**

```markdown
- [ ] Use Glob to find all output files specified by checklist items in Phases 1-5 of this task — the expected file paths are (enumerated inline): <path-1 from item P-006>, <path-2 from item P-007>, ..., <path-N from item P-016>, gh-issues-created.md from Phase 5 — then for each expected path verify via Glob that the file exists on disk, then create a verification summary file `gate2-outputs.md` at `.dev/tasks/<TASK-NAME>/phase-outputs/reports/gate2-outputs.md` containing a table with columns (Item ID, Expected Path, Exists Y/N, File Size) and a final PASS/FAIL verdict (PASS only if all expected files exist with non-zero size), ensuring all paths come from the actual checklist items in Phases 1-5 with no fabricated paths. If any expected file is missing, the gate FAILs and the missing items must be re-executed before re-running this gate. If unable to complete due to filesystem errors, log the specific blocker using the templated format in the ### Phase 6 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
```

**Gate 3 — Blocker entries have resolution notes (I17.3):**

```markdown
- [ ] Read the ## Task Log / Notes section of this task file at `<absolute/path/to/this-task-file.md>` (specifically the ### Phase 1 Findings through ### Phase 5 Findings subsections) to identify all blocker entries logged during execution, then for each blocker entry verify that a resolution note (either "RESOLVED: <how>" or "FOLLOW-UP: <ticket/issue-link>") has been added directly below the blocker, then create a verification summary file `gate3-blockers.md` at `.dev/tasks/<TASK-NAME>/phase-outputs/reports/gate3-blockers.md` containing a table with columns (Phase, Blocker Summary, Resolution Status, Note) and a final PASS/FAIL verdict (PASS if all blockers have resolution notes OR if no blockers were logged), ensuring all blocker entries are derived from the actual Task Log content with no fabrication. If any blocker lacks a resolution note, the gate FAILs and resolution notes must be added before re-running this gate. If unable to read the Task Log, log the specific blocker using the templated format in the ### Phase 6 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
```

**Gate 4 — Tests pass (I17.4 / I18, since this is a code-modifying task):**

```markdown
- [ ] Use the Bash tool to run `cd <repo-root> && uv run pytest <relevant-test-paths-covering-modified-code> -v 2>&1` and capture the complete output, then write the raw output to `.dev/tasks/<TASK-NAME>/phase-outputs/test-results/gate4-pytest-output.txt` and create a structured summary at `.dev/tasks/<TASK-NAME>/phase-outputs/reports/gate4-tests.md` containing: total tests run, passed count, failed count, skipped count, a table of any failed tests with (Test Name, Error Type, Brief Error Message), and a final PASS/FAIL verdict (PASS only if zero failures and zero errors — skipped tests are acceptable), ensuring the summary reflects the actual pytest output with no fabricated counts. If pytest fails to execute (not test failures — execution failures like missing pytest), log the specific blocker using the templated format in the ### Phase 6 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
```

**After the 4 gates, the L5 conditional + frontmatter close-out items finalize the task** (these are MANDATORY per C4/I13 and follow the reference example's Phase 9 pattern). Recommended additions to Phase 6 after Gates 1-4:

**Final-verdict aggregation item (L5/L6):**

```markdown
- [ ] Read the four gate report files at `.dev/tasks/<TASK-NAME>/phase-outputs/reports/gate1-checkboxes.md`, `gate2-outputs.md`, `gate3-blockers.md`, and `gate4-tests.md` to extract each gate's PASS/FAIL verdict, then create a final task verdict file `final-verdict.md` at `.dev/tasks/<TASK-NAME>/phase-outputs/reports/final-verdict.md` containing the four sub-verdicts, an overall verdict (PASS only if all four gates PASS), and a one-paragraph summary of any failures, ensuring the verdict is derived from the actual gate reports with no fabrication. If any gate report is missing, log the blocker using the templated format in the ### Phase 6 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
```

**Frontmatter close-out item (L5 conditional):**

```markdown
- [ ] Read the final verdict file at `.dev/tasks/<TASK-NAME>/phase-outputs/reports/final-verdict.md` to determine the overall task verdict, then update the ### Task Summary section of the ## Task Log / Notes at the bottom of this task file with the overall verdict, item count summary (18 items across 6 phases), and paths to all gate reports, then update the YAML frontmatter of this task file at `<absolute/path/to/this-task-file.md>`: IF verdict is PASS, set `status: "Done"`, `completion_date: "<today YYYY-MM-DD>"`, `updated_date: "<today YYYY-MM-DD>"`; IF verdict is FAIL, set `status: "Blocked"`, `blocker_reason: "<one-line summary of failing gates>"`, `updated_date: "<today YYYY-MM-DD>"`. In either case ensure the YAML remains valid and no other fields are modified. Once done, mark this item as complete.
```

**This brings Phase 6 total to 6 items** (4 gates + 1 aggregator + 1 frontmatter close-out). The user said "verification gate" + 18 items total. If the user's 18-item count includes ONLY work items (Phases 1-5), Phase 6's 6 items are added on top. If the user's 18-item count INCLUDES Phase 6's items, the builder must re-budget — recommend confirming with the build request that Phase 6 verification items are NOT counted in the 18.

---

## 4. Summary for the Builder

**Mandatory rules to enforce:**

1. **Frontmatter:** Use the full schema from §1.1. `template_schema_doc` MUST be `".claude/templates/workflow/02_mdtm_template_complex_task.md"`. `task_type: static`. `autogen_method: "rf-task-builder"`.
2. **Pre-Phase-1 content:** Frontmatter → Task Overview (prose) → Key Objectives → Prerequisites & Dependencies (informational, NO checklist items) → Phase 1 (D3 rule).
3. **B2 6-element pattern in EVERY item:** context+why, action+why, output spec, ensuring clause, failure-evidence clause, completion gate. Single paragraph, single `- [ ]`. No nesting, no parent items, no separate verification items.
4. **A3 deviation for Phase 5:** explicitly note the 13→1 collapse in the item itself (deviation note), in the Phase 5 step header, AND in `### Deviations from Process` under `## Task Log / Notes`.
5. **Phase 6 = I17 verification:** must produce 4 gate items mapping 1:1 to I17.1-I17.4, plus an aggregator and a frontmatter close-out item. Use the L5 conditional pattern for the close-out (PASS→Done, FAIL→Blocked).
6. **Task Log / Notes section** at the bottom must include `### Task Summary`, `### Execution Log`, `### Phase 1 Findings` through `### Phase 6 Findings`, `### Follow-Up Items`, AND `### Deviations from Process`.
7. **Reference shape:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260402-baseline-repo/TASK-RF-20260402-baseline-repo.md` is the closest known-good reference. Builder may model phase headers, step naming, blockquote purpose statements, and frontmatter style on it.

**Forbidden patterns to avoid (B5):**
- Standalone "read context" items
- Multi-line / bulleted items
- Separate verification or "confirm completion" items
- Parent checkboxes summarizing children
- Summary items placed BEFORE their components
- REMINDER blocks between items

---

**Status:** Complete.
