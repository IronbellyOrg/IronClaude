# Research: Template & Examples
**Topic type:** Template & Examples
**Scope:** MDTM template 02 rules + prior skill-rebuild task folders
**Status:** Complete
**Date:** 2026-05-27
---

## Summary

The rf-task-builder MUST use `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` (1204 lines) as the canonical schema for the sc-reflect-protocol rebuild task file. PART 1 (lines 46-870) is orchestrator instructions and MUST be stripped from the output task file. PART 2 (lines 872-1204) plus the frontmatter (lines 1-44) IS the actual task file template that gets copied and filled. The closest analog by surface coverage (CLI + command + skill body + refs + installer + tests + sync + QA) is **TASK-RF-20260525-194356 (init-lite)** — 5 phases + post-completion, ~20 self-contained items, single task-integrity QA gate at the end. Secondary analogs: TASK-RF-20260522-151622 (skill body edit, 12 phases, FINAL_ONLY adversarial QA) and TASK-RF-20260520-230051 (skill remediation, 5 phases). Common QA-flagged pitfalls: (a) verbatim old_string drift when editing existing files, (b) fabricated/hallucinated flags/commands not in target system, (c) `make verify-sync` invoked for non-skill surfaces (RQ-4 violation), (d) phase ordering of `make sync-dev` BEFORE `make verify-sync` (never the reverse), (e) branch-base assumptions (`integration` may not exist on the fork).

---

## 1. Template 02 PART 1 — Mandatory Rules (verbatim citations)

### Frontmatter schema (file: `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:1-44`)

Mandatory frontmatter fields in order:
```yaml
id: "TASK-[AGENT]-[TASKTYPE]-YYYYMMDD-HHMMSS"     # L2
title: "[Clear, Action-Oriented Task Title]"        # L3
description: "[Detailed description...]"            # L4
status: "🟡 To Do"                                  # L5  (emoji REQUIRED)
type: "📝 Documentation"                            # L6  (emoji REQUIRED)
priority: "🔼 High"                                 # L7  (emoji REQUIRED)
created_date: "YYYY-MM-DD"                          # L8
updated_date: "YYYY-MM-DD"                          # L9
assigned_to: "[agent-name]"                         # L10
autogen: false                                      # L11
autogen_method: ""                                  # L12
coordinator: orchestrator                           # L13
parent_task: "[PARENT-TASK-ID]"                     # L14
depends_on: []                                      # L15-17
related_docs:                                       # L18-24 (list of {path, description})
tags: []                                            # L25-29
template_schema_doc: ""                             # L30
estimation: ""                                      # L31
sprint: ""                                          # L32
due_date: ""                                        # L33
start_date: ""                                      # L34
completion_date: ""                                 # L35
blocker_reason: ""                                  # L36
ai_model: ""                                        # L37
model_settings: ""                                  # L38
review_info:                                        # L39-42
task_type: static                                   # L43
```

Status emoji vocabulary (from prior task files): `🟡 To Do` (initial), `🟠 Doing` (in progress), `🟢 Done`, `⚪ Blocked`.

Type emoji vocabulary observed across analogs: `📝 Documentation`, `♻️ Refactor`, `🔧 Refactor`, `🐞 Bug Fix`, `🌟 Feature`. For a SKILL REBUILD (which creates new skill files + updates command + adds tests), recommended: `🌟 Feature` or `♻️ Refactor`.

### A3 — Complete Granular Breakdown (lines 91-95)
```
A3. COMPLETE GRANULAR BREAKDOWN
   - Break down EVERY workflow phase into atomic, verifiable checklist items
   - Create individual checklist items for EVERY file, component, or iteration
   - NO high-level or bulk operations allowed - everything must be granular
   - Include exact file paths, specific requirements, and measurable outcomes
```

Implication for sc-reflect rebuild: ONE checklist item per ref file, ONE item per fixture, ONE item per CLI subcommand, ONE item per test module. No item like "create all refs".

### A4 — Iterative Process Structure (lines 97-116)
Standard pattern:
```markdown
**Step X.1:** Scan and enumerate all [items] in [location]
- [ ] Complete [item] listing generated: [count] items identified

**Step X.2:** Process each [item] individually:
- [ ] [Item 1]: [exact identifier] - [specific action] completed
- [ ] [Item 2]: [exact identifier] - [specific action] completed
[Continue for each item]

**Step X.3:** Consolidate all individual results
```

### B2 — Self-Contained Checklist Item: the 6-element pattern (lines 142-148, VERBATIM)
```
B2. EVERY CHECKLIST ITEM MUST BE A COMPLETE, SELF-CONTAINED PROMPT THAT INCLUDES:
   1. Context Reference with WHY - What file(s) to read and why that context is needed for this specific action
   2. Action with WHY - What to do with that context and why it needs to be done
   3. Output Specification - The exact output file name, location, what content to produce, and template to follow (if applicable)
   4. Integrated Verification - An "ensuring..." clause that specifies what must be verified (DO NOT assume, hallucinate, or make up any information - all content MUST be derived from source files referenced in the checklist item, 100% accuracy based on source materials, document negative evidence when verification fails)
   5. Evidence on Failure Only - Log to task notes ONLY if unable to complete due to blockers, missing info, or errors (successful completion is evidenced by the output file itself)
   6. Explicit Completion Gate - "This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete."
```

B3 enforces SINGLE PARAGRAPH (no bullets/multi-line) — lines 150-153.

### B5 — FORBIDDEN PATTERNS (lines 164-184)
- Standalone "read context" items that don't produce output
- Missing context reference (no source of truth)
- Multi-line/bulleted checklist items
- Separate verification/confirmation items (integrate via "ensuring..." clause)
- Overly granular items (e.g., "create directory" alone)
- Separate REMINDER blocks between checklist items

### E1-E4 — Checklist structure rules (lines 278-388)
- E1: Flat structure, NO nested checkboxes, NO parent checkboxes summarizing children
- E2 FUNDAMENTAL RULE: Summary/parent checkboxes MUST come AFTER all their component items
- E3: Sequential order — no backward references, work flows TOP to BOTTOM only
- E4: NEVER place checkboxes next to step numbers; step numbers are bold headers

### F1-F5 — Execution requirements (lines 394-451)
Worker agents follow READ → IDENTIFY → EXECUTE → UPDATE → REPEAT loop. F5 frontmatter update protocol:
- Upon Task Start: status → "🟠 Doing", start_date
- Upon Completion: status → "🟢 Done", completion_date
- If Blocked: status → "⚪ Blocked", populate blocker_reason
- After Each Work Session: updated_date

### I15-I18 — QA gate + validation rules (lines 599-647)
- **I15:** Every task with 2+ execution phases MUST include at least one phase-gate QA checkpoint
- **I16 fix-cycle table:**
  | Gate Type | Max Fix Cycles | After Max Reached |
  | research-gate | 3 | HALT and escalate to user |
  | synthesis-gate | 2 | Unresolved → Open Questions |
  | report-validation | 3 | HALT and escalate to user |
  | task-integrity | 2 | Unresolved → Open Questions |
  | Any qualitative gate | 3 | HALT and escalate to user |
- **I17 Post-completion validation MUST verify:**
  1. All `- [ ]` items marked `- [x]`
  2. All output files exist on disk (verified via Glob)
  3. Blocker entries have resolution notes
  4. If task modified source code: all relevant tests pass
- **I18:** Code-modifying tasks MUST include a testing item with test command, pass criteria, results capture path, B2 self-contained pattern; use L3 (Test/Execute) pattern.

### L1-L6 — Intra-Task Handoff Patterns (lines 711-810)

| Pattern | When to use | Output dir |
|---------|------------|------------|
| **L1 Discovery** | Explore codebase/data, produce structured findings later items consume | `phase-outputs/discovery/` |
| **L2 Build-from-Discovery** | Create output using discovered info — reads discovery file + source file | (deliverable path) |
| **L3 Test/Execute** | Run command/test suite, capture raw output + structured summary | `phase-outputs/test-results/` |
| **L4 Review/QA** | Assess quality with PASS/FAIL verdict + structured findings | `phase-outputs/reviews/` |
| **L5 Conditional-Action** | Branch on previous result; MUST handle BOTH branches | `phase-outputs/plans/` |
| **L6 Aggregation** | Consolidate multiple outputs via Glob discovery into single report | `phase-outputs/reports/` |

L7 Pattern Selection Guide (lines 811-836) recommends for SKILL REBUILDS:
- **Full Lifecycle with QA Gates:** L1 → L2 → **M1 (QA Gate)** → L3 → L5 → L4 → L6 → **M1 (QA Gate)**

### M1-M2 — Phase-Gate Composite Patterns (lines 843-860)
M1 sequence:
1. **Aggregation (L6)** — collect all phase outputs via Glob
2. **QA Agent Spawn** — spawn rf-qa (structural) with phase type, input paths, output report path, verdict handling, error clause; if qualitative also required, spawn rf-qa-qualitative in SEPARATE item immediately after (sequential)
3. **Conditional Proceed (L5)** — IF PASS proceed; IF FAIL fix cycle up to I16 max

---

## 2. Closest Analog: TASK-RF-20260525-194356 (init-lite) — SKILL+CLI+command+installer+tests

**Title:** "Implement superclaude init-lite --context-optimized" (line 3 of task file)
**Surface coverage:** Identical to sc-reflect rebuild — new CLI subcommand + thin slash command + protocol skill source + installer mapping update + test coverage + sync + final QA gate.

### Phase structure (file: `.dev/tasks/to-do/TASK-RF-20260525-194356/TASK-RF-20260525-194356.md`):

```
### Phase 1: Preparation and Implementation Inventory          (L133-145)
  Step 1.1: Start task execution (status → Doing)
  Step 1.2: Create handoff directories
  Step 1.3: Build implementation inventory from research        (L1 Discovery pattern)

### Phase 2: Implement CLI, Command, Skill, and Installer Sources (L147-167)
  Step 2.1: Add focused init-lite CLI module
  Step 2.2: Register init-lite in the top-level CLI
  Step 2.3: Fix protocol skill installer mapping
  Step 2.4: Add thin /sc:init-lite command source
  Step 2.5: Add backing protocol skill source and any necessary lazy refs

### Phase 3: Add Focused Test Coverage                          (L169-181)
  Step 3.1: Add init-lite behavior tests
  Step 3.2: Update CLI registration regression tests
  Step 3.3: Add installer mapping tests in the nearest appropriate module

### Phase 4: Run Required Validation Commands and Capture Results (L183-207)
  Step 4.1: Run focused CLI behavior and registration tests     (L3 Test/Execute)
  Step 4.2: Run targeted installer mapping tests
  Step 4.3: Sync source-of-truth components to dev mirrors       (make sync-dev)
  Step 4.4: Verify source and dev mirror sync                    (make verify-sync)
  Step 4.5: Run lint validation
  Step 4.6: Assess validation results and remediate if needed   (L5 Conditional)

### Phase 5: Task-Integrity QA Gate                              (L209-221)
  Step 5.1: Aggregate implementation and validation outputs     (L6 Aggregation)
  Step 5.2: Spawn rf-qa for task-integrity review               (M1 step 2)
  Step 5.3: Apply task-integrity QA verdict and fix-cycle rules (L5 + M1 step 3)

## Post-Completion Actions                                       (L223-239)
  Step 6.1: Verify all task outputs exist + all items complete  (I17)
  Step 6.2: Confirm final validation evidence remains passing
  Step 6.3: Create task summary
  Step 6.4: Mark task complete (status → Done)

## Task Log / Notes                                              (L241+)
  ### Task Summary
  ### Execution Log
  ### Phase 1 - ... Findings
  ### Phase 2 - ... Findings
  ... (per phase)
```

**Total items:** ~20 across 5 execution phases + post-completion (4 items).
**Phase count for the sc-reflect rebuild SHOULD follow this skeleton** (verified by user's spawn prompt suggesting Phase 1: prep / Phase 2: skill body / Phase 3: refs / Phase 4: command / Phase 5: eval workspace / Phase 6: sync / Phase 7: QA gates / Phase 8: completion — but the init-lite collapses skill body + refs + command + CLI into one Phase 2; SUGGEST combining for fewer phases, OR splitting if the sc-reflect skill body is large).

### Verbatim example of a skill-body creation item (init-lite Step 2.5, lines 165-167 of task file)

The full paragraph is in the closest-analog source — single paragraph, ~600 words, includes:
- Discovery file references (`/config/.../phase-outputs/discovery/init-lite-implementation-inventory.md`)
- Research file references (`/config/.../research/02-command-skill-patterns.md`, etc.)
- Existing protocol skill examples to mirror (`src/superclaude/skills/sc-roadmap-protocol/SKILL.md`, `sc-cli-portify-protocol/SKILL.md`, `sc-recommend-protocol/SKILL.md`) with specific line ranges
- Output path `/config/.../src/superclaude/skills/sc-init-lite-protocol/SKILL.md`
- 7-element content spec (frontmatter + body sections)
- "ensuring..." clause covering: refs scope discipline, no `Edit` tool unless modifying, target-project `.claude/` as read-only, no fabrication, no placeholders
- Blocker logging clause pointing to specific Phase N Findings section
- Completion gate "Once done, mark this item as complete."

This is the canonical shape for sc-reflect's SKILL.md creation item.

---

## 3. Secondary Analog: TASK-RF-20260522-151622 (sc-troubleshoot wave insertion) — 12 phases

**Title:** "Add Wave 1.5 Documentation Grounding to sc:troubleshoot" — pure skill body edit + 1 new ref file (no CLI).
**Why this analog matters:** Phase structure scales when per-file edits multiply. 12 phases because 5 source-of-truth files × multiple edits each + sync + final QA + completion.

Phase outline:
```
Phase 1: Preparation and Setup (2 items)
Phase 2: Command File Edits (5 items including phase grep gate)
Phase 3: Create the new refs/doc-discovery.md file (2 items)
Phase 4: SKILL.md Frontmatter + Output Contract Extension (5 items)
Phase 5: SKILL.md Wave List Update + Wave 1.5 Block Insertion (3 items)
Phase 6: SKILL.md Downstream Wiring (5 items)
Phase 7: SKILL.md Refs Loader + Graceful Degradation + MCP Integration (6 items)
Phase 8: refs/hypothesis-card-template.md — Add field (2 items)
Phase 9: refs/report-template.md — Multiple insertions (5 items)
Phase 10: Sync & Validate (2 items: make sync-dev, then make verify-sync)
Phase 11: Final QA Gate (FINAL_ONLY rf-qa Adversarial) (3 items: L6 aggregate → rf-qa spawn → L5 conditional)
Phase 12: Post-Completion Actions (3 items: I17 validation + completion)
```

**Pattern observation:** Each phase ends with a "Phase N grep gate" verification item — a Bash command that grep-verifies all edits in that phase are present. This is **task-integrity defense in depth** that an old_string-heavy task should adopt.

---

## 4. Per-file item examples from prior rebuilds (verbatim shape)

### One item per ref file (from TASK-RF-20260525-194356 Step 2.5)
The init-lite task uses ONE item to create SKILL.md AND optionally refs/, but instructs "Edit not included unless implementation truly modifies existing files" — for sc-reflect rebuild with multiple refs (likely separate ref files), recommend **one item per ref file** following A3 Granularity.

### One item per fixture/scenario (from TASK-RF-20260525-150000 Steps 3.1-3.2)
```
**Step 3.1:** Author TUIBBS_HUB_SPEC synthetic fixture per RQ-1 Option A
**Step 3.2:** Author TUIBBS_HUB_ROADMAP synthetic fixture
```
For sc-reflect eval workspace: one item per `evals/*.json` scenario OR per fixture file.

### One item per test method (from TASK-RF-20260525-150000 Steps 3.4-3.10)
Seven items: `Step 3.4` t1, `3.5` t2, `3.6` t3, `3.7` t4, `3.8` t5, `3.9` t6, `3.10` t7. Each is a single paragraph self-contained item.

For sc-reflect: one test item per assertion/scenario in evals.json or per behavior test in `tests/`.

---

## 5. Phase-level QA gate items — verbatim invocation pattern

### From TASK-RF-20260525-194356 Step 5.2 (rf-qa spawn for task-integrity)

Key elements of the spawn item:
- Read inputs (QA input report, implementation inventory, validation verdict)
- Spawn `rf-qa` with: `qa_phase: task-integrity`, `fix_authorization: true`, explicit `ADVERSARIAL STANCE` instruction
- Verify against: task constraints, source-of-truth discipline, no target-project mutation, dry-run invariants, default report markers, installer protocol mapping, test coverage, validation command evidence
- Output path: `phase-outputs/reviews/rf-qa-task-integrity.md`
- Binary PASS/FAIL verdict
- Blocker handling

### From TASK-RF-20260525-194356 Step 5.3 (L5 conditional with fix-cycle)
Encodes:
- IF PASS: write `phase-outputs/plans/task-integrity-gate-verdict.md` containing PASS + statement
- IF FAIL: address findings, re-run validation, re-spawn rf-qa in fix-cycle mode up to **3 cycles** (note: I16 says task-integrity max is 2 — init-lite uses 3, may be project drift)
- Strict cycle ordering: `regression -> monotonicity -> hard-cap -> proceed`
- Regression detection halt: "Regression detected on Item X.Y — previously PASS at cycle N, now FAIL"
- Monotonicity halt: `[HALT-MONOTONICITY] |F|=<n>`
- After max cycles → halt + ask user (NOT auto-convert to Open Questions)

### From TASK-RF-20260522-151622 Phase 11 (FINAL_ONLY rf-qa Adversarial)
Three items:
- **Step 11.1:** L6 aggregate all Phase 2-10 gate outputs into `phase-outputs/reports/all-phase-gate-results.md`
- **Step 11.2:** Spawn rf-qa with adversarial stance + fix_authorization
- **Step 11.3:** L5 conditional-proceed

This is the **"single FINAL_ONLY QA gate"** pattern that simpler skill rebuilds can use (rather than per-phase gates).

---

## 6. Frontmatter conventions across analog tasks

| Field | TASK-RF-20260525-194356 (init-lite) | TASK-RF-20260522-151622 (sc-troubleshoot) | TASK-RF-20260525-150000 (refactor) | TASK-RF-20260520-230051 (skill remediation) |
|-------|--------|--------|--------|--------|
| `id` | `"TASK-RF-20260525-194356"` | `"TASK-RF-20260522-151622"` | `"TASK-RF-20260525-150000"` | `"TASK-RF-20260520-230051"` |
| `status` | `"To Do"` (no emoji — irregular) | `"🟢 Done"` | `"🟢 Done"` | `"🟢 Done"` |
| `type` | `"Implementation"` (irregular) | `"📝 Documentation"` | `"♻️ Refactor"` | `"🐞 Bug Fix"` |
| `assigned_to` | `"rf-task-executor"` | `"rf-task-executor"` | `"rf-task-executor"` | `"rf-task-executor"` |
| `coordinator` | `"rf-team-lead"` | `orchestrator` | `orchestrator` | `orchestrator` |
| `autogen_method` | `"rf-task-builder"` | `""` | `""` | `""` |
| `template_schema_doc` | absolute path | relative `.claude/templates/...` | relative | relative |
| `tracks` | `["implementation"]` (extra) | absent | absent | absent |
| `template` | `"02_mdtm_template_complex_task"` (extra) | absent | absent | absent |

**Recommendation for sc-reflect rebuild frontmatter:**
- Use emoji status: `"🟡 To Do"` (template canonical, not bare strings)
- Use emoji type: `"🌟 Feature"` or `"♻️ Refactor"` (skill rebuild)
- `assigned_to: "rf-task-executor"` (consistent across all analogs)
- `coordinator: orchestrator` (consistent except init-lite which used `rf-team-lead`)
- `autogen_method: "rf-task-builder"` (truthful provenance)
- `template_schema_doc: ".claude/templates/workflow/02_mdtm_template_complex_task.md"` (relative)
- `related_docs`: list ALL research files (research/01-...md through research/08-...md) + spec source + relevant src/ files (each with `path` + `description` keys)
- `tags`: `["sc-reflect", "skill-rebuild", "protocol-skill", "command", "skill-source", "tests"]` style
- `task_type: static`

---

## 7. Task Log / Notes section conventions

Template 02 PART 2 (lines 1128-1204) defines the exact structure:

```markdown
## Task Log / Notes 📋

### Task Summary
<!-- Fill this section in Post-Completion Actions -->
**Completion Date:** [YYYY-MM-DD]
**Work Completed:** ... (bullet list)
**Challenges Encountered:** ...
**Deviations from Process:** ...
**Blockers Logged:** ...
**Follow-Up Required:** [Yes/No]

### Execution Log
<!-- TEMPLATE: **[YYYY-MM-DD HH:MM]** - [Action]: [Description] -->
**[YYYY-MM-DD HH:MM]** - Task started: ...
**[YYYY-MM-DD HH:MM]** - Task completed: ...

### Phase 1 - [Phase Name] Findings
<!-- TEMPLATE: **[YYYY-MM-DD HH:MM]** - [Step X.Y]: [Finding/blocker]
  - **Status:** [Completed | Blocked]
  - **Details:** ...
  - **Blocker Reason (if blocked):** ...
  - **Files Affected:** ... -->

### Phase 2 - [Phase Name] Findings
### Phase 3 - [Phase Name] Findings
### Phase Gate Findings
<!-- QA gate verdicts, fix cycle counts, unresolved issues -->

### Follow-Up Items Identified
<!-- TEMPLATE: - **[Priority: High/Medium/Low]** [Description] - Identified in Step [X.Y] -->

### Deviations from Process
<!-- TEMPLATE: **[YYYY-MM-DD HH:MM]** - Deviation from [Step X.Y]:
  - **Expected:** ...
  - **Actual:** ...
  - **Rationale:** ... -->
```

**Important:** Every analog had a `### Phase N - [Name] Findings` subsection per phase. With 8 phases in the sc-reflect rebuild, this produces 8 Findings subsections + Phase Gate Findings + Follow-Up Items + Deviations.

---

## 8. Open Questions / Resolved Questions section format

From TASK-RF-20260525-150000 (line 64-87, evidenced by QA item #7 in `qa/qa-task-validation-report.md`):
- `## Resolved Questions` section appears immediately after `## Task Overview` and BEFORE `## Key Objectives`
- Each entry: `RQ-1:`, `RQ-2:`, etc. — question, resolution, citation
- If all questions resolved pre-execution, NO `## Open Questions` section is needed (QA marks this PASS-vacuous)

From TASK-RF-20260522-151622 (referenced in QA report item #7): "Open Questions section present at L1043, explicitly empty (BUILD_REQUEST locked all 5 placement decisions)" — alternative pattern: include the section but mark it empty.

**Recommendation:** For sc-reflect rebuild, include `## Resolved Questions` (with research-resolved decisions) and either omit `## Open Questions` OR include it explicitly marked empty if all questions are resolved.

---

## 9. Common pitfalls observed in prior QA reports (CRITICAL for rf-task-builder)

### From TASK-RF-20260525-150000 qa/qa-task-validation-report.md (Issue #1):
**Pitfall: Spurious `make verify-sync` / `make sync-dev` invocation for non-skill surfaces.**
- The task spuriously ran `make verify-sync` for a `src/superclaude/cli/` refactor where RQ-4 explicitly said sync-dev only applies to skills/agents/commands.
- **Fix applied:** Replaced with `git status -- .claude/` as defensive cleanliness check.
- **Lesson for sc-reflect:** Since sc-reflect rebuild DOES touch skills + commands, `make sync-dev` IS required. But the order must be: `make sync-dev` FIRST, then `make verify-sync` (NEVER reverse, see TASK-RF-20260522-151622 QA item E).

### From TASK-RF-20260525-150000 qa/qa-qualitative-review.md (Issue #1):
**Pitfall: Branch-base assumption (`integration` branch may not exist on the fork).**
- Step 1.3 invoked `git checkout integration` but the fork has only `master`/`origin/master`/`upstream/master`.
- **Fix applied:** Added `git branch -a | grep integration` discovery probe with fallback to `master`.
- **Lesson for sc-reflect:** Branch creation steps MUST include the `git branch -a` discovery probe. Or, since the current working directory is already a worktree on `feat-reflect-v2` branch (per session-context), the task should target that branch explicitly and NOT switch.

### From TASK-RF-20260522-151622 qa/qa-qualitative-review.md (Issues C1, C2, C3):
**Pitfall: Verbatim `old_string` drift in Edit-based items.**
- 3 CRITICAL old_string blocks didn't byte-match current source (SKILL.md L65, L143; report-template.md L18).
- Cause: task-builder cited content from earlier file revisions.
- **Fix applied:** Re-Read each cited line, replaced old_string AND new_string preamble to match current source.
- **Lesson for sc-reflect:** ANY Edit-based item against existing files MUST cite line numbers verified by Read in the SAME researcher pass; do NOT trust prior researcher claims of line numbers. The rf-task-builder should re-Read every cited line range during task file generation.

### From TASK-RF-20260522-151622 qa/qa-task-validation-report.md (Issue F):
**Pitfall: Fabricated/hallucinated flags or commands.**
- Step 6.3 referenced `--context-file <path>` flag on sc:adversarial — NOT a recognized flag (the recognized flags are `--compare`, `--source`, `--generate`, etc.).
- **Status: UNFIXABLE in QA pass; requires task-builder redesign.**
- **Lesson for sc-reflect:** Every CLI flag / command / function referenced in an item MUST be verified to exist by reading the actual command surface file. If recommending the use of an external skill/command, the task-builder must Read that command's source to enumerate valid flags.

### From TASK-RF-20260525-194356 (init-lite) — implicit patterns:
- Every item cites multiple research files by absolute path with line ranges where applicable (`research/02-command-skill-patterns.md`, evidence at `src/.../SKILL.md:1-6`)
- Multi-source evidence in single item is GOOD (the init-lite Step 2.5 cites 3 protocol skills, the project CLAUDE.md, plus the discovery file)
- Use absolute paths in CWD-bearing items, NOT relative — this prevents executor confusion

---

## 10. Suggested phase structure for sc-reflect rebuild (combining best practices)

Based on init-lite (closest analog) + sc-troubleshoot pattern (grep gate per phase) + spawn-prompt user-suggested phases:

```
Phase 1: Preparation and Implementation Inventory
  - Status update (Doing)
  - Create handoff dirs
  - Build implementation inventory (L1 Discovery)
  - [optional] Capture pre-edit baseline snapshots if existing sc:reflect surfaces are being modified

Phase 2: Skill body + command source
  - Create/rebuild SKILL.md
  - Create/update .claude/commands/sc/reflect.md (slash command)
  - [grep gate] Verify skill body + command edits present

Phase 3: Refs (ONE ITEM PER REF FILE per A3 Granularity)
  - Create refs/[file-1].md
  - Create refs/[file-2].md
  - ... (one item per ref)
  - [grep gate] Verify all refs created

Phase 4: CLI integration (if applicable)
  - Add CLI module (e.g., src/superclaude/cli/reflect.py)
  - Register in cli/main.py
  - Update installer mapping if needed

Phase 5: Eval workspace (.dev/eval-workspaces/sc-reflect-protocol/)
  - Create evals.json scenarios (ONE ITEM PER SCENARIO)
  - Create fixtures (ONE ITEM PER FIXTURE)

Phase 6: Tests + Sync + Validation
  - Run focused tests (L3 Test/Execute)
  - Run regression tests
  - make sync-dev (L3) — FIRST
  - make verify-sync (L3) — SECOND
  - make lint (L3)
  - Assess (L5 Conditional)

Phase 7: Final QA Gate (M1 Composite)
  - Aggregate (L6)
  - Spawn rf-qa task-integrity (adversarial stance + fix_authorization)
  - Spawn rf-qa-qualitative (sequential after structural)
  - Conditional proceed with fix-cycle rules per I16 (max 2 cycles, then halt+escalate)

Post-Completion Actions (I17 validation):
  - Verify all items marked complete + all output files exist (Glob)
  - Confirm final validation passing
  - Create task summary
  - Update frontmatter to Done
```

**Total estimated items:** ~30-40 (initial estimate based on init-lite ~20 + sc-troubleshoot wave ~45; the split depends on how many refs the sc-reflect skill needs). Each phase except QA has a grep-gate verification item appended per sc-troubleshoot pattern.

---

## 11. Cross-cutting requirements every item MUST include (synthesis of B2 + I12 + J1)

Every item MUST be a SINGLE PARAGRAPH containing, in order:

1. **Context references:** "Read the [file] at [absolute path] to [extract X], then read [file 2] at [path 2] to [extract Y]..."
2. **Action with WHY:** "...then create/update [output file] at [exact path] containing [description] following [template/pattern at path]..."
3. **Output spec embedded:** exact path, exact content requirements, line-range citations from sources
4. **Integrated verification ("ensuring..." clause):** "...ensuring [criterion 1], [criterion 2], no fabricated content, no placeholders, [project-specific invariants]..."
5. **Blocker logging:** "If unable to complete due to [specific failure modes], log the specific blocker using the templated format in the `### Phase N - [Name] Findings` section of the `## Task Log / Notes` at the bottom of this task file, then mark this item complete."
6. **Completion gate:** "Once done, mark this item as complete."

**Length:** ~400-800 words per item (single paragraph). The init-lite Step 2.5 is ~600 words.

---

## 12. Research file naming convention for the rf-task-builder

From the 4 analogs reviewed:
- `research/01-file-inventory.md` (TASK-RF-20260525-150000, TASK-RF-20260522-151622)
- `research/02-patterns-conventions.md` (variant: `02-patterns-and-conventions.md`)
- `research/03-integration-points.md` (TASK-RF-20260522-151622) / `03-template-examples.md` (TASK-RF-20260525-150000)
- `research/04-template-and-examples.md` (TASK-RF-20260522-151622) / `04-gap-fill.md` (TASK-RF-20260525-150000) / `04-test-verification.md` (TASK-RF-20260525-194356)

**Recommendation:** Use 2-digit zero-padded prefix + dash + kebab-case topic name (current task already follows this with `05-template-and-examples.md`).

---

## 13. Critical "do NOT" list extracted from QA reports (rf-task-builder MUST follow)

1. **NEVER reference flags/commands/functions without reading their source file** (qa-task-validation-report Issue F, TASK-RF-20260522-151622).
2. **NEVER trust prior researcher's cited line numbers without re-Reading the source file** (qa-qualitative-review Issues C1-C3, TASK-RF-20260522-151622).
3. **NEVER invoke `make verify-sync` BEFORE `make sync-dev`** — always sync-dev FIRST, verify-sync SECOND.
4. **NEVER assume `integration` branch exists on the fork** — discovery probe required, fallback to `master`.
5. **NEVER use `git add -f` on `.claude/*` paths** (project-level CLAUDE.md absolute rule).
6. **NEVER stage anything under `.claude/` except `.claude/settings.json`** — these are gitignored sync-dev outputs.
7. **NEVER batch items** ("create all refs") — one item per ref file (A3 Granularity).
8. **NEVER create standalone "read context" items** — context must be embedded in actionable items (B5).
9. **NEVER create multi-line/bulleted checklist items** — single paragraph only (B3).
10. **NEVER create separate verification items** — embed "ensuring..." clause in action item (B2.4, C3).
11. **NEVER omit the blocker-logging clause** — every item must reference its `### Phase N Findings` subsection (J1).
12. **NEVER target the upstream repo for PRs** — fork only (CLAUDE.md absolute rule).
13. **NEVER edit `.claude/` directly without editing `src/superclaude/` first** then `make sync-dev`.

---

## Cited file:line evidence (canonical references)

- Template canonical path: `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md`
- A3 Granular Breakdown: lines 91-95
- A4 Iterative Process Structure: lines 97-116
- B2 self-contained 6-element pattern: lines 142-148
- B3 single-paragraph rule: lines 150-153
- B4 verbatim correct example: lines 155-158
- B5 forbidden patterns: lines 164-184
- C1-C4 embedding requirements: lines 206-230
- E1-E4 checklist structure: lines 278-388
- F1-F5 execution requirements: lines 394-451
- I15 phase-gate enforcement: lines 599-607
- I16 fix-cycle table: lines 609-624
- I17 post-completion validation: lines 626-635
- I18 testing requirements for code-modifying tasks: lines 637-646
- L1-L6 handoff patterns: lines 737-810
- L7 pattern selection guide: lines 811-836
- M1-M2 phase-gate composite patterns: lines 843-860
- PART 2 template start: line 890
- Task Log / Notes section: lines 1128-1204

- Closest analog (init-lite) task file: `.dev/tasks/to-do/TASK-RF-20260525-194356/TASK-RF-20260525-194356.md`
  - Frontmatter: lines 1-50+
  - Phase 1 start: line 133
  - Phase 2 (CLI+command+skill+installer): line 147
  - Phase 3 (tests): line 169
  - Phase 4 (validation): line 183
  - Phase 5 (QA gate): line 209
  - Post-Completion: line 223
  - Task Log/Notes: line 241

- 12-phase analog (sc-troubleshoot wave) task file: `.dev/tasks/to-do/TASK-RF-20260522-151622/TASK-RF-20260522-151622.md`
  - Phase 10 sync order: lines 926-938 (make sync-dev BEFORE make verify-sync)
  - Phase 11 FINAL_ONLY rf-qa adversarial: lines 938-948

- QA pitfall sources:
  - `.dev/tasks/to-do/TASK-RF-20260525-150000/qa/qa-task-validation-report.md` (verify-sync pitfall)
  - `.dev/tasks/to-do/TASK-RF-20260525-150000/qa/qa-qualitative-review.md` (branch-base pitfall)
  - `.dev/tasks/to-do/TASK-RF-20260522-151622/qa/qa-qualitative-review.md` (old_string drift Issues C1-C3, fabricated flag Issue F)
  - `.dev/tasks/to-do/TASK-RF-20260522-151622/qa/qa-task-validation-report.md` (sync order Issue E, fabricated flag Issue F)
