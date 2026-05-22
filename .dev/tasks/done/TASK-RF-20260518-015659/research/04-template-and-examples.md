# Research 04 — Template & Examples

**Researcher:** 4 of 5
**Topic:** MDTM Template 02 (complex task) + prior task examples for sprint runner / Python CLI internals
**Status:** In Progress
**Date:** 2026-05-18

---

## Section 1 — MDTM Template 02 Rule Catalogue (PART 1 Instructions)

**Source:** `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md`

### Frontmatter (lines 1–44)
Required fields: `id`, `title`, `description`, `status`, `type`, `priority`, `created_date`, `updated_date`, `assigned_to`, `autogen`, `autogen_method`, `coordinator: orchestrator`, `parent_task`, `depends_on[]`, `related_docs[]` (with path + description), `tags[]`, `template_schema_doc`, `estimation`, `sprint`, `due_date`, `start_date`, `completion_date`, `blocker_reason`, `ai_model`, `model_settings`, `review_info{last_reviewed_by,last_review_date,next_review_date}`, `task_type: static`.

### Section A — CORE PRINCIPLES (lines 68–128)
- **A1 Workflow Document Availability Check (lines 72–83):** Check if governing workflow docs exist; if not, omit "WORKFLOW-DEPENDENT" sections and derive from user input.
- **A2 Workflow Document Deep Integration (lines 85–89) [WORKFLOW-DEPENDENT]:** Extract every requirement/phase/step/quality standard from workflow, map every workflow element to task elements.
- **A3 Complete Granular Breakdown (lines 91–95):** Break down EVERY workflow phase into atomic, verifiable checklist items. Individual checklist item for every file/component/iteration. **NO high-level or bulk operations allowed.** Exact file paths + measurable outcomes.
- **A4 Iterative Process Structure (lines 97–116):** For multi-item processes: pre-enumerate ALL items first, create checklist item per item, require incremental updates, consolidate at end. Pattern: Step X.1 enumerate → Step X.2 process each individually → Step X.3 consolidate.
- **A5 Cross-Stage Integration (lines 118–122) [WORKFLOW-DEPENDENT]:** Every phase specifies inputs from previous stages with exact file paths.
- **A6 Workflow Compliance Enforcement (lines 124–128) [WORKFLOW-DEPENDENT]:** Reference specific workflow doc sections; copy quality standards directly.

### Section B — SELF-CONTAINED CHECKLIST ITEMS (lines 130–196) — CRITICAL
- **B1 Why This Matters (lines 134–140):** Session rollover protection. Standalone "read context" items USELESS because context lost before use.
- **B2 The 6-Field Schema (lines 142–148):** Every item MUST include:
  1. **Context Reference with WHY** — what file(s) to read and why
  2. **Action with WHY** — what to do and why
  3. **Output Specification** — exact file name + location + content + template
  4. **Integrated Verification** — "ensuring..." clause (NO hallucination, 100% source-derived, document negative evidence)
  5. **Evidence on Failure Only** — log to task notes ONLY if blocked
  6. **Explicit Completion Gate** — "This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete."
- **B3 The Self-Contained Pattern (lines 150–153):** ONE FULL PARAGRAPH (not multiple lines/bullets), verbose, explanatory; reads like an independent prompt.
- **B4 Correct Example (lines 155–161):** See verbatim excerpt below in Section 6.
- **B5 Forbidden Patterns (lines 164–183):** Standalone "read context" items; missing context reference; multi-line/bulleted items; separate verification items; overly granular items; separate REMINDER blocks.
- **B6 Preferential (lines 185–187):** Context source references when reading required; output specs when file produced.
- **B7 Key Principles (lines 189–196):** Each item = complete prompt; context embedded IN action; verification embedded IN action; output file = evidence; only log on failure; one paragraph verbose; QA process handles verification between batches.

### Section C — EMBEDDING REQUIREMENTS (lines 198–230)
- **C1 Outputs & Deliverables embedded (lines 206–212):** Embed in checklist items; do NOT create separate Outputs section.
- **C2 Success Criteria as "ensuring..." clause (lines 214–218):** Embed; do NOT create separate Success Criteria section.
- **C3 Verification embedded (lines 220–224):** Embed in action items; do NOT create separate Verification Checklist section. Intra-task QA between batches (I15 phase-gate, I17 post-completion).
- **C4 Task Completion as Post-Completion Actions (lines 226–230):** Only frontmatter update + Execution Log entry. Do NOT create Task Completion and Handoff Protocol section.

### Section D — MANDATORY TASK SECTIONS (lines 232–273)
- **D1 Workflow Compliance Declaration [WORKFLOW-DEPENDENT]:** Informational only, no checklist items.
- **D2 Cross-Stage Integration Requirements [WORKFLOW-DEPENDENT]:** Informational only; actual checklist items go in Phase 1 Step 1.4.
- **D3 CRITICAL RULE (lines 269–273):** NO CHECKLIST ITEMS may appear before Phase 1 begins. Order: Frontmatter → Workflow Compliance (info) → Prerequisites (info) → Phase 1 (executable).

### Section E — CHECKLIST STRUCTURE RULES (lines 275–388)
- **E1 Checkbox Format (lines 278–292):** Every actionable item = `- [ ]`. NO nested checkboxes (flat only). NO parent checkboxes summarizing children. Use `**Step X.Y:**` headers for grouping. Sequential order. Atomic, verifiable.
- **E2 Critical Structure Rules (lines 294–348):** Summary/parent checkboxes MUST come AFTER components. NEVER parent before children. Indented allowed only if no parent above. Use headers for grouping, summary at end verifies/confirms.
- **E3 Sequential Order (lines 350–365):** Exact completion order. NEVER backward references. FORBIDDEN: "mark item complete in section above," "see checklist below," "return to phase," parent-with-children, summary-before-components.
- **E4 Checkbox Formatting (lines 367–388):** NEVER place checkboxes next to step numbers. Step numbers = bold headings. NO separate REMINDER blocks between items (worker agents only see batch items, not surrounding text); integrate reminders INTO the item.

### Section F — EXECUTION REQUIREMENTS (lines 390+) [partial — continuing]
- **F1 Five-Step Execution Pattern (lines 394+):** READ → IDENTIFY → EXECUTE → UPDATE → REPEAT.

---

### Section F — EXECUTION REQUIREMENTS (lines 390–451)
- **F1 Five-Step Pattern (lines 394–403):** READ → IDENTIFY → EXECUTE → UPDATE → REPEAT (one unchecked item at a time).
- **F2 Prohibited Actions (lines 405–412):** No working from memory; no multi-item execution; no skipping phases; no cross-phase delegation; no skipping phase-gate QA (rf-qa after Phase 2+); no skipping post-completion validation (rf-qa structural + rf-qa-qualitative operational).
- **F2a Item Execution Discipline (lines 414–430):** One item per F1 loop within a session. **Parallel-spawning exception (line 430):** consecutive items in the SAME phase that spawn INDEPENDENT subagents (no cross-reading) MAY be spawned in parallel in a single message. Each item still marked individually.
- **F3 Universal Requirements (lines 432–438):** Every item required, exact sequential order, all referenced files reviewed, all mandatory elements included, no assumptions, every checkbox marked `[x]`.
- **F4 Task File Modification (lines 440–445):** Workers may only: check items, update frontmatter per protocol, add to Task Log, add items inside DYNAMIC markers (dynamic tasks only).
- **F5 Frontmatter Update Protocol (lines 447–451):** Start → 🟠 Doing + start_date; Done → 🟢 Done + completion_date; Blocked → ⚪ Blocked + blocker_reason; each session → updated_date.

### Section G — Context for Headless Agents (lines 453–468)
- **G1:** Framework context files NOT auto-loaded in headless workers.
- **G2:** Either reference the rule file OR a template embedding it (preferred).
- **G3:** Task-specific context embedded directly in action items.
- **G4:** Previous stage outputs format `[Output Type]: [path/to/output.md] - [Purpose]` embedded in action items that need them.

### Section H — Tool Specification (lines 470–490)
- **H1:** Default: let model pick tools.
- **H2/H3:** Only specify a tool when a SPECIFIC tool is required; embed in the item itself.
- **H4:** Matrix — Glob (file discovery), Grep (content search), Read/Write/Edit (rarely), Bash (commands).

### Section I — Additional Guidelines (lines 492–649)
- **I1 Explicit Directive Language:** "YOU MUST" / "DO NOT", no passive voice.
- **I2 Extreme Granularity:** exact paths, concrete content requirements.
- **I3 Incremental File Modification:** add content incrementally; never "complete entire files at once."
- **I4 Parent Task Relationships:** specify parent, depends_on, blocks.
- **I5 All Requirements Absolute:** no optional items.
- **I6 Dynamic Content Handling:** discovery → use → create → verify; `task_type: static` vs `dynamic`.
- **I7 Explicit Template Usage:** exact path, read with specific tool, list placeholders, specify output location.
- **I8 Mandatory Template Usage:** "create complex task" implicitly = template 02.
- **I9 Hallucination Prevention:** explicit warnings, 100% source accuracy, incremental saves, repeat "DO NOT assume, hallucinate, or make up".
- **I10 Critical Workflow Compliance Reinforcement:** multi-level compliance checks, re-read workflow after major deliverables.
- **I11 Early Status Update:** "🟠 Doing" must be the first task action.
- **I12 Verification Integrated:** NO separate verification items; embed via "ensuring..." clause.
- **I13 Post-Completion Actions:** frontmatter update + Execution Log only.
- **I14 Anti-Hallucination Controls Integration:** reference `anti-hallucination_task_completion_rules.md`, evidence table requirements, negative evidence documentation, strict "COMPLETE" definition.
- **I15 Phase-Gate QA Enforcement (lines 599–607):** Every task with 2+ phases MUST include at least one phase-gate QA checkpoint between primary execution phase and any subsequent dependent phase. Checkpoint = (1) aggregation item, (2) rf-qa or rf-qa-qualitative spawn item, (3) conditional-action item (PASS proceed / FAIL fix-cycle).
- **I16 QA Gate Verdict & Fix Cycles (lines 609–624):** Binary PASS/FAIL (any severity = FAIL). Fix-cycle caps: research-gate=3 HALT, synthesis-gate=2 open-question, report-validation=3 HALT, task-integrity=2 open-question, any-qualitative=3 HALT. Each cycle MUST re-verify ALL prior failed + check for new. Cycle issue-count increase = systemic problem.
- **I17 Post-Completion Validation Protocol (lines 626–635):** Before frontmatter Done, validation items MUST verify: (1) all `- [ ]` → `- [x]`, (2) all output files exist (Glob), (3) blockers have resolution notes, (4) code-modifying tasks: tests pass.
- **I18 Testing Requirements for Code-Modifying Tasks (lines 637–646):** MUST include at least one testing item with: (1) exact test command, (2) pass criteria, (3) results-capture location, (4) B2 self-contained pattern. Use L3 pattern.

### Section J — Error Handling (lines 651–673)
- **J1 Pattern (embedded in every item):** "If unable to complete due to missing information, file access issues, or unclear requirements, log the specific blocker using the templated format in the ### Phase [N] Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete."
- **J2 Principles:** items NEVER left unchecked; success = output file exists; failure = blocker logged; task continues.
- **J3:** Do NOT block whole task for individual failures; mark "⚪ Blocked" only if ALL remaining items blocked by same issue.

### Section K — Example Patterns (lines 675–708)
- **K1 File-by-File Processing Pattern:** per-file self-contained item with template-read + source-read + create.
- **K2 Multi-Item Processing Pattern:** orchestrator pre-enumerates ALL items (worker NEVER dynamically adds); per-item self-contained pattern.

### Section L — Intra-Task Handoff Patterns (lines 710–836) **THIS IS THE COMPLEX-TASK ADDITION**
Handoff file convention: `.dev/tasks/TASK-NAME/phase-outputs/{discovery,test-results,reviews,plans,reports}/`. Files persist across batches and session rollovers.

- **L1 Discovery Item Pattern (lines 737–747):** Explore codebase/data, write structured findings to `phase-outputs/discovery/`. The file IS the deliverable.
- **L2 Build-from-Discovery Item Pattern (lines 749–759):** Read both the discovery file AND original source. Discovery tells WHAT, source provides CONTENT.
- **L3 Test/Execute Item Pattern (lines 761–771):** Run command, capture BOTH raw output AND structured summary to `phase-outputs/test-results/`.
- **L4 Review/QA Item Pattern (lines 773–783):** Produce structured verdict (PASS/FAIL) with specific findings to `phase-outputs/reviews/`. Never "looks good".
- **L5 Conditional-Action Item Pattern (lines 785–797):** Read status file, branch on result. MUST handle BOTH success AND failure branches. Output file always created.
- **L6 Aggregation Item Pattern (lines 799–809):** Use Glob to dynamically find all relevant files, consolidate to `phase-outputs/reports/`. Don't hardcode file lists.
- **L7 Pattern Selection Guide (lines 811–836):** Common phase structures:
  - **Discovery → Build → Review:** Phase 2 = L1 → L2 (per item) → L4 (per item) → L6
  - **Build → Test → Fix:** Phase 2 = K1/K2 (build) → L3 (test) → L5 (conditional fix)
  - **Full Lifecycle:** L1 → L2 → L3 → L5 → L4 → L6
  - **Full Lifecycle with QA Gates:** L1 → L2 → **M1 QA Gate** → L3 → L5 → L4 → L6 → **M1 QA Gate**

### Section M — Phase-Gate Composite Patterns (lines 838–860)
- **M1 Phase-Gate QA Sequence (lines 843–850):** 2–3 items inserted between phases:
  - Item 1 (Aggregation, L6): Glob preceding-phase outputs into summary/inventory.
  - Item 2 (QA Agent Spawn): rf-qa structural with phase type, input paths, output report path, verdict handling, error clause. If qualitative also needed, rf-qa-qualitative in SEPARATE item immediately following (sequential, qualitative after structural PASS).
  - Item 3 (Conditional Proceed, L5): IF PASS proceed; IF FAIL execute fix cycle (max cycles per I16), re-run QA.
- **M2 Applicability (lines 852–860):** Code-modifying tasks: gate after implementation phase and before testing phase OR after combined implement+test phase. When in doubt — include a gate.

---

## Section 2 — PART 2 Mandatory Task File Sections

**Source:** Template PART 2, lines 894–1165.

### Required body sections in order:
1. **Frontmatter** (44-field YAML).
2. **`# [Task Title]`** (line 896)
3. **`## Task Overview`** (line 898).
4. **`## Key Objectives`** (line 902).
5. **`## Prerequisites & Dependencies`** (line 910): Parent Task & Dependencies → Previous Stage Outputs (informational) → Handoff File Convention → Frontmatter Update Protocol.
6. **`## Detailed Task Instructions`** (line 956).
7. **`### Phase 1: Preparation and Setup`** (line 1014) — Step 1.1 status update, Step 1.2 create handoff dirs.
8. **`### Task-Specific Context Files`** (line 1051) — informational list only.
9. **`### Phase 2: [Main Execution Phase]`** (line 1062).
10. **`### Phase Gate: Quality Verification`** (line 1088) — rf-qa spawn via M1.
11. **`### Phase [N]: Testing & Verification`** (line 1096) — L3 if code modified.
12. **`### Phase 3: Review and Quality Assessment`** (line 1104) — L4 + L6.
13. **`## Post-Completion Actions`** (line 1115) — 4 items.
14. **`## Task Log / Notes 📋`** (line 1125) — Task Summary + Execution Log + Phase N Findings.

---

## Section 3 — Prior Sprint-CLI Task Examples

### Example A: TASK-RF-20260325-cli-tdd (closest in-tree match)

**Path:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260325-cli-tdd/TASK-RF-20260325-cli-tdd.md`
**Why representative:** modifies multiple `src/superclaude/cli/{roadmap,tasklist}/` files — same surface as planned sprint-runner fix. 8 phases, ~29 items, `template: complex`.

**Frontmatter (lines 1–14) — VERBATIM:**
```yaml
---
id: TASK-RF-20260325-cli-tdd
title: "CLI TDD Integration — Dual Extract Prompt with --input-type Flag"
status: done-cli-layer
completion_date: 2026-03-26
start_date: 2026-03-26
updated_date: 2026-03-26
priority: high
created: 2026-03-25
type: implementation
template: complex
estimated_items: 29
estimated_phases: 8
---
```

**Phase 1 (lines 62–66) — VERBATIM:**
```markdown
## Phase 1: Setup and Handoff Directory Creation (2 items)

- [x] **1.1** Read this task file in full to understand all phases, objectives, and open questions. Update the `status` field in this file's YAML frontmatter from `to-do` to `in-progress`. Once done, mark this item as complete.

- [x] **1.2** Create the handoff directory structure for intra-task outputs: create the directory `.dev/tasks/to-do/TASK-RF-20260325-cli-tdd/phase-outputs/` and subdirectories `discovery/`, `test-results/`, `reviews/`, and `reports/`. These directories will hold intermediate outputs passed between phases. If any directory already exists, skip it. Once done, mark this item as complete.
```

**Phase 2 first item shape (line 74) — VERBATIM (single-paragraph B2 self-contained example):**
```markdown
- [x] **2.1** Read the file `commands.py` at `src/superclaude/cli/roadmap/commands.py` to understand the existing Click option decorators and `run()` function signature, then add a new `@click.option("--input-type", type=click.Choice(["spec", "tdd"], case_sensitive=False), default="spec", help="Type of input file for roadmap generation. Default: spec.")` decorator to the `run` command (place after the existing `--retrospective` option), add `input_type: str` as a keyword argument to the `run()` function signature, and add `"input_type": input_type` to the `config_kwargs` dict assembly before the `RoadmapConfig(**config_kwargs)` call, ensuring the decorator follows the exact Click pattern used by existing options like `--depth` which uses `click.Choice`, no existing options are modified, and the function signature change is additive only. If unable to complete due to unexpected file structure, log the specific blocker in the Phase 2 Findings section of the Task Log at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
```

**Notable shape conventions:**
- Phase headers carry item count: `## Phase 2: CLI and Config Layer (5 items)`.
- Each phase opens with `> **Purpose:**` blockquote.
- Item IDs: `**2.1**`, `**2.2**` bold prefix (NOT just `2.1`).
- Last item of each phase = verification item using `uv run python -c "..."` inline test or `uv run pytest`, capturing to `phase-outputs/test-results/phase[N]-verification.md`.
- Final phase = integration testing: pytest file creation, full suite run, backward-compat checks, final report.

### Example B: D-0023 release spec (smaller-scope shape)

**Path:** `/config/workspace/IronClaude/.dev/releases/current/task-builder-merge/artifacts/D-0023/spec.md`
**Why representative:** Per-task spec docs that rf-task-builder consumed. They model the LEVEL OF DETAIL expected per item.

**Verbatim shape (53 lines):**
```markdown
# D-0023 — T02.09 Spec: Commit TEST-004..006 fixtures

**Task:** T02.09 (Phase 2)
**Roadmap items:** R-043, R-044, R-045
**Date:** 2026-05-17

## Goal

Land three pytest fixtures + the corresponding test files asserting the
M2 `## Execution Context` block contract:

- **TEST-004 (R-043).** Fully-populated BUILD_REQUEST → header contains all
  three DM-001 labeled bullets (`**References:**`, `**Source areas:**`,
  `**Key constraints:**`) in declared order, between frontmatter and the
  first `### T<PP>.<TT>` phase task.
...

## Paths

- Fixtures:
  - `tests/audit/fixtures/execution_context/fully_populated.md`
  ...
- Tests:
  - `tests/audit/test_execution_context_full.py`
  ...

## Dependencies
...

## Verification command

```
uv run pytest \
  tests/audit/test_execution_context_full.py \
  tests/audit/test_execution_context_minimal_buildrequest.py \
  tests/audit/test_execution_context_no_file_paths.py -v
```

Expected: exit 0 with 16 PASSED (5 / 6 / 5 across the three files).
```

**Shape lessons:** Heading format `# D-XXXX — T<PP>.<TT> Spec: <imperative>`; bold key:value metadata block; sections Goal / Paths / Dependencies / Verification command (literal bash) / Expected outcome; ALL paths EXACT, no wildcards.

### Example C: D-0067 — MIG-005 landing (larger-scope shape)

**Path:** `/config/workspace/IronClaude/.dev/releases/current/task-builder-merge/artifacts/D-0067/spec.md`
- `## 1. Scope` paragraph block, `## 2. <FF_FLAG>` table, `## 3. Acceptance Criteria mapping` AC1..ACn→evidence table, `## 4. Per-guard disable rollback path` numbered procedure.
- Every claim cites `file:line` precisely (e.g. `rf-team-lead.md:417`, `rf-task-builder.md:360-366`) with byte-exact sha256s.
- Tone: declarative, verifiable, adversarial.

---

## Section 4 — Template-02 Features the Sprint-Runner Task SHOULD Use

Maps onto **Build → Test → Fix** with L-pattern composition:

| Phase | Pattern | Purpose | Items |
|---|---|---|---|
| Phase 1 | Setup | Status update + handoff dir | 2 (verbatim from template) |
| Phase 2 | L1 (Discovery) | Confirm file:line for each of 4 bugs (in case drifted since research) | 1 combined OR 1 per bug → `phase-outputs/discovery/sprint-runner-fix-targets.md` |
| Phase 3 | K1 (File-by-File Build) | Apply 4 fixes — one item per fix with exact `src/superclaude/cli/sprint/...:line` + before/after | 4 items, **parallel-spawning eligible per F2a** if fixes are in independent regions |
| Phase Gate | M1 | rf-qa structural verification of fix application (phase-type `task-integrity`, max 2 cycles per I16) | Aggregation (L6) + rf-qa spawn + conditional proceed (L5) = 2–3 items |
| Phase 4 | L3 (Test/Execute) | `uv run pytest tests/cli/sprint/ -v` → `phase-outputs/test-results/sprint-runner-test-results.md` per I18 | 1 test item + 1 L5 conditional (PASS→verdict / FAIL→fix-plan + retry, max 2 cycles) |
| Phase 5 | L4 + L6 | Per-fix review + aggregate quality report | 1 L4 per fix + 1 L6 aggregate |
| Post-Completion | I17 + I13 | Glob outputs exist, full suite green, Task Summary, frontmatter → 🟢 Done | 4 items (template lines 1117–1123 VERBATIM) |

### Parallel-spawning opportunity (F2a line 430)
Phase 3 items 3.1–3.4 (four independent fix items) parallel-eligible IF each fix is in an independent code region. Each item still marked individually. Phase 5 review items similarly parallel-eligible.

### Conditional flow (L5)
Required at Phase 4 (test result → verdict OR fix-plan + retry).

### Multi-phase QA gates (I15) per M2 line 857
"Code-modifying tasks: After implementation phase and before testing phase (if testing is separate)" — gate REQUIRED between Phase 3 (implementation) and Phase 4 (testing). Phase-type `task-integrity`, max 2 fix cycles per I16.

---

## Section 5 — TB-Add-1..8 Structural Checks (rf-qa enforced)

**Source:** `/config/workspace/IronClaude/.claude/skills/task-builder/SKILL.md` lines 1119–1127 (descriptive catalog) and 1906–1913 (checklist form). rf-qa enumerates dynamically from rf-qa.md (INV-010).

| ID | Name | Rule | Line |
|---|---|---|---|
| **TB-Add-1** | Placeholder scan | No `TBD`/`TODO`/`FIXME` tokens; no title-only items. 5-field schema (Context/Action/Output/Verification/Completion gate). | 1120 |
| **TB-Add-2** | Item count bounds | Track ≥3 ≤40; single-track ≥3 ≤50. **ADVISORY-fail until calibrated** (≥10 done tasks across ≥3 task_types). | 1121 |
| **TB-Add-3** | Clarification adjacency | Blocked items reference blocking Open Question by index in Context. | 1122 |
| **TB-Add-4** | Circular dependency detection | Item-to-item depends form DAG; no cycles. | 1123 |
| **TB-Add-5** | Granularity / XL splitting | Complex/multi-file items either split OR carry justifying comment. | 1124 |
| **TB-Add-6** | Confidence/Verification format | Uniform `Verify: ...` prefix; consistent `- ✅` / `- [x]` AC form. | 1125 |
| **TB-Add-7** | Execution Context source areas reappear | Every `## Execution Context` "Source areas:" entry reappears in ≥1 item Context; block contains NO file:line. INACTIVE if no Execution Context block. | 1126 |
| **TB-Add-8** | Per-item Context evidence binding | Every item Context referencing a code surface includes `file:line` OR `<!-- evidence-absence: ... -->` comment. (INV-015 scope-confinement.) | 1127 |

**Practical implications for the sprint-runner fix task:**
1. **TB-Add-1:** Every item ends with completion-gate sentence (B2 element 6). No placeholders survive.
2. **TB-Add-2:** Single-track → ≥3 ≤50. Projected ~16–20 items, in bounds.
3. **TB-Add-3:** Items blocked on research-file open questions MUST cite question index in Context.
4. **TB-Add-4:** Phase ordering linear; explicit depends_on form a DAG.
5. **TB-Add-5:** If any of 4 fixes touches multiple files/regions, split into sub-items.
6. **TB-Add-6:** Use `Verify: ...` prefix on the verification sentence; `- [x]` for AC.
7. **TB-Add-7:** Put bug locations under `## Execution Context` → `Source areas: src/superclaude/cli/sprint/, tests/cli/sprint/` (DIRECTORIES only, no `:line`). Items cite specific `file:line`. Header has no line numbers; items DO.
8. **TB-Add-8:** Every item naming a code surface MUST cite `src/superclaude/cli/sprint/<file>.py:<line>` OR carry `<!-- evidence-absence: <reason> -->`.

---

## Section 6 — Builder-Ready Item Schema (verbatim from B2 + B4)

**Section B4 verbatim example (lines 155–161) — TEMPLATE for every item:**

```markdown
- [ ] Read the file `component-spec.md` at `docs/specs/component-spec.md` to extract the API interface requirements including all method signatures, parameter types, and return values that must be implemented, then read the file `BaseHandler.ts` at `src/handlers/BaseHandler.ts` to understand the structural patterns and conventions used in existing handlers, then create the file `ApiHandler.ts` at `src/handlers/ApiHandler.ts` containing a TypeScript class that implements all methods defined in the component spec with proper error handling, type annotations, and JSDoc comments following the patterns from BaseHandler, ensuring the file includes the standard header comment block, exports the class as the default export, all methods from the spec are implemented with correct signatures, no content is fabricated or assumed beyond what the source explicitly states, and no placeholder or TODO comments remain. If unable to complete due to missing information, file access issues, or unclear requirements, log the specific blocker using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.
```

**The 6 required B2 elements in order:**
1. **Context Reference with WHY:** "Read the file `X` at `path/X` to extract ... that must be implemented" + "Read the file `Y` at `path/Y` to understand ..."
2. **Action with WHY:** "then create/modify the file `Z` at `path/Z` containing/with ..."
3. **Output Specification:** exact file name + exact path + content description + template if applicable.
4. **Integrated Verification (`ensuring...` clause):** "ensuring [specific requirements], no content fabricated, no placeholders remain..."
5. **Evidence on Failure Only:** "If unable to complete due to ..., log the specific blocker using the templated format in the ### Phase [N] Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete."
6. **Explicit Completion Gate:** "Once done, mark this item as complete."

**Single-paragraph requirement (B3):** ALL of the above is ONE paragraph — no bullets, no multi-line breakdowns inside the checklist item.

---

## Summary for the Builder

1. **Use Template 02** at `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md` PART 2 (lines 894–1165). Copy frontmatter + replace placeholders.
2. **Frontmatter:** match shape from `TASK-RF-20260325-cli-tdd` (id, title, status: "🟡 To Do", template: complex, estimated_items, estimated_phases, type: implementation, priority: high, dates).
3. **Mandatory sections:** Task Overview → Key Objectives → Prerequisites & Dependencies (Parent + Previous Stage Outputs + Handoff File Convention + Frontmatter Update Protocol) → Phase 1 Setup (2 items) → Phase 2..N (L-pattern composed) → Phase Gate (M1) → Post-Completion (4 items verbatim from template lines 1117–1123) → Task Log / Notes (Execution Log + Phase N Findings).
4. **Item shape:** EVERY item follows B2 6-element schema, ONE paragraph, with closing "Once done, mark this item as complete." (B4).
5. **L-pattern composition:** Phase 2 = L1 discovery → Phase 3 = K1 build (4 fixes, parallel-eligible) → Phase Gate = M1 (rf-qa task-integrity, max 2 cycles) → Phase 4 = L3 test + L5 conditional → Phase 5 = L4 review + L6 aggregate.
6. **TB-Add-1..8 compliance:** no placeholders; ≥3 ≤50 items; blocked items reference question index; DAG; XL splits or justify; `Verify:` prefix; Execution Context = directories only; per-item Context = `file:line`.
7. **Code-modifying → I18 mandatory:** Phase 4 MUST include `uv run pytest tests/cli/sprint/ -v` with pass criteria + results to `phase-outputs/test-results/`.
8. **Post-completion I17:** Glob output files exist + tests re-pass + Task Summary written + frontmatter → 🟢 Done.

---

## File Paths Referenced

- Template: `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md` (1165 lines)
- Closest prior task: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260325-cli-tdd/TASK-RF-20260325-cli-tdd.md`
- Release spec (small): `/config/workspace/IronClaude/.dev/releases/current/task-builder-merge/artifacts/D-0023/spec.md`
- Release spec (large): `/config/workspace/IronClaude/.dev/releases/current/task-builder-merge/artifacts/D-0067/spec.md`
- Release spec (mid): `/config/workspace/IronClaude/.dev/releases/current/task-builder-merge/artifacts/D-0040/spec.md`
- TB-Add catalog source: `/config/workspace/IronClaude/.claude/skills/task-builder/SKILL.md` lines 1119–1127 (descriptive) and 1906–1913 (checklist)

**Status: Complete**

