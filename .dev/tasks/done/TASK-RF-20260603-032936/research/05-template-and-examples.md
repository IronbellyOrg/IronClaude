# Research: Template and Examples

Status: In Progress
Date: 2026-06-03

---

## 1. Template 02 — PART 1 Building Rules

Source: `.claude/templates/workflow/02_mdtm_template_complex_task.md` (85583 bytes). Template 02 = "Complex Task Template", extends Template 01 with **Section L: Intra-Task Handoff Patterns**. Use when tasks require discovery, testing, review, conditional logic, or aggregation between checklist items (lines 60-63).

### Frontmatter fields (lines 1-44)
Required YAML keys, in order:
- `id` ("TASK-[AGENT]-[TASKTYPE]-YYYYMMDD-HHMMSS"), `title`, `description`
- `status` ("🟡 To Do"), `type` (e.g. "📝 Documentation"), `priority` ("🔼 High")
- `created_date`, `updated_date`, `assigned_to`
- `autogen: false`, `autogen_method: ""`, `coordinator: orchestrator`
- `parent_task`, `depends_on` (list), `related_docs` (list of {path, description})
- `tags` (list), `template_schema_doc`, `estimation`, `sprint`, `due_date`, `start_date`, `completion_date`, `blocker_reason`, `ai_model`, `model_settings`
- `review_info` ({last_reviewed_by, last_review_date, next_review_date})
- `task_type: static`

### Section A — Core Principles (lines 68-128)
- **A1** Workflow Document Availability Check (72-83): if no governing workflow docs exist, OMIT all [WORKFLOW-DEPENDENT] sections and derive requirements from user input directly. (sc-recommend task has NO `.gfdoc`/`.roo` workflow doc → omit WORKFLOW-DEPENDENT sections.)
- **A2** Workflow Document Deep Integration [WORKFLOW-DEPENDENT] (85-89).
- **A3 COMPLETE GRANULAR BREAKDOWN (91-96):** Break EVERY phase into atomic verifiable items. Individual item for EVERY file/component/iteration. NO bulk operations. Exact file paths, specific requirements, measurable outcomes.
- **A4 ITERATIVE PROCESS STRUCTURE (97-116):** For multi-item processes: (1) Pre-enumerate ALL items in an initial step, (2) one item per specific item, (3) incremental updates after each, (4) consolidation step only after all complete. Pattern:
  - Step X.1: Scan/enumerate → `[ ] Complete listing generated: [count] identified`
  - Step X.2: Process each individually → one `[ ]` per item
  - Step X.3: Consolidate → `[ ] All [count] items processed and logged` + `[ ] Consolidated output created`
- **A5** Cross-Stage Integration [WORKFLOW-DEPENDENT] (118-122).
- **A6** Workflow Compliance Enforcement [WORKFLOW-DEPENDENT] (124-128).

### Section B — Self-Contained Checklist Items (CRITICAL) (130-196)
- **B1 (134-140):** Session-rollover protection — context from batch 1 gone by batch 3+, so EVERY item embeds all context/actions/outputs. Standalone "read context" items are USELESS.
- **B2 (142-148) — every item must include 6 elements:**
  1. **Context Reference with WHY** — what file(s) to read and why.
  2. **Action with WHY** — what to do and why.
  3. **Output Specification** — exact output file name, location, content, template to follow.
  4. **Integrated Verification** — "ensuring..." clause; no assume/hallucinate, 100% derived from source, document negative evidence on failure.
  5. **Evidence on Failure Only** — log to task notes ONLY if blocked/error; success evidenced by output file.
  6. **Explicit Completion Gate** — verbatim: "This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete."
- **B3 (150-153):** Each item = ONE FULL PARAGRAPH (not bullets), verbose, reads like a standalone executable prompt.
- **B4 (155-162):** Correct example is a single dense paragraph integrating read→read→create→"ensuring..."→failure-log→completion gate. Do NOT create separate verification items; QA handles verification between batches.
- **B5 FORBIDDEN (164-183):** standalone "read context" items; missing context ref; multi-line/bulleted items; separate verification/confirmation items; overly granular items ("create directory" alone); separate REMINDER blocks.
- **B7 Key principles (189-196):** each item a complete prompt; context embedded in action; verification embedded via "ensuring..."; output files = evidence; only log on FAIL/BLOCK; one verbose paragraph; QA handles verification (I15-I16 phase gates).

### Section C — Embedding Requirements (NOT separate sections) (198-230)
- **C1 (206-211):** Outputs embed in creating item; output file = evidence; NO "Outputs & Deliverables" section.
- **C2 (213-217):** Success criteria embed as "ensuring..." clause; NO separate success-criteria items/section.
- **C3 (219-223):** Verification embeds in action items; NO separate verification section; intra-task QA handles (I15 phase-gate, I17 post-completion).
- **C4 (225-230):** Completion handled by Post-Completion Actions only (update frontmatter status/completion_date, log to Execution Log). I17 handles output verification. NO "Task Completion and Handoff Protocol" section.

### Section D — Mandatory Sections / structural rule (lines 233-272)
- **D1/D2** are [WORKFLOW-DEPENDENT], informational only (no checklist items).
- **D3 CRITICAL RULE (269-272):** NO checklist items before Phase 1. Order: Frontmatter → Workflow Compliance (informational) → Prerequisites (informational) → Phase 1 (executable). All context-review/prior-stage-input items go IN Phase 1, Steps 1.2-1.4.

### Section E — Checklist Structure (274-388)
- **E1 (278-292):** Every actionable item is `- [ ] Action text`. FLAT structure only — NO nested checkboxes, NO parent checkboxes summarizing children. Use **Step X.Y:** bold headers for grouping (no checkbox on step numbers). Items in exact completion order; never reference later checkboxes.
- **E2 (294-348):** Summary/parent checkboxes come AFTER component items, never before. Indented checklists OK only if no parent checkbox above. Components first, summary last.
- **E3 (350-365):** Strictly top-to-bottom. FORBIDDEN: "mark item above", "see checklist below", any backward movement, parent-with-children, summary-before-components.
- **E4 (367-388):** No checkboxes next to step numbers; no separate REMINDER blocks between items (workers see only batch items, not surrounding prose) — integrate reminders INTO the item.

### Section F — Execution Requirements (390-451)
- **F1 (394-403):** READ → IDENTIFY (first unchecked) → EXECUTE (only that one) → UPDATE (`[x]`) → REPEAT.
- **F2 (405-412):** Prohibited: working from memory, multi-item execution, skipping phases, delegating across phase boundaries (subagent gets work from a SINGLE item only; never delegate the F1 loop), skipping phase-gate QA (I15-16), skipping post-completion validation (I17).
- **F2a (414-430):** Item-execution discipline (one item at a time within a session). **Parallel spawning exception (430):** when consecutive items in the SAME phase spawn INDEPENDENT subagents (no shared outputs), executor MAY spawn all in parallel via multiple Agent calls in one message; still mark each individually as its agent completes. Does NOT apply to data-dependent items.
- **F5 (447-451):** Frontmatter protocol — start: "🟠 Doing"+start_date; done: "🟢 Done"+completion_date; blocked: "⚪ Blocked"+blocker_reason; each session: updated_date.

### Section G — Headless Agent Context (453-468)
- Framework files (ib_agent_core.md, quality_gates.md, etc.) are NOT auto-loaded into headless workers. Reference the specific rule file (or a template incorporating it — preferred) IN the item. Embed task context in action items, not separate "context loading" steps.

### Section H — Tool Specification (470-490)
- H1/H2: only specify a tool when a SPECIFIC tool is required for a reason; otherwise let the model choose. H3: embed tool + reason in the item.

### Section I — Additional Guidelines (492-649) — key ones
- **I1** "YOU MUST"/"DO NOT" directive language. **I2** extreme granularity, exact paths. **I3** incremental file modification ("DO NOT complete entire files at once"). **I9/I14** hallucination prevention, 100% source accuracy, document negative evidence, evidence tables for technical claims. **I11** status→"🟠 Doing" must be FIRST action. **I12** verification integrated via "ensuring..." (no separate verify items).
- **I15 PHASE-GATE QA ENFORCEMENT (599-607):** Every task with 2+ execution phases MUST have ≥1 phase-gate QA checkpoint between the primary execution phase and any dependent subsequent phase. A checkpoint = (1) aggregation item collecting prior-phase outputs, (2) QA agent spawn item (rf-qa or rf-qa-qualitative) verifying outputs, (3) conditional-action item proceeding on PASS / fix cycle on FAIL. The QA spawn item is a self-contained B2 item naming: agent, phase type, input files, output report path, verdict handling, error clause.
- **I16 QA VERDICT + FIX CYCLES (609-624):** Verdicts are binary PASS/FAIL; ANY issue (CRITICAL/IMPORTANT/MINOR) = FAIL. Fix-cycle table:

  | Gate Type | Max Fix Cycles | After Max |
  |---|---|---|
  | research-gate | 3 | HALT and escalate to user |
  | synthesis-gate | 2 | Unresolved → Open Questions |
  | report-validation | 3 | HALT and escalate to user |
  | task-integrity | 2 | Unresolved → Open Questions |
  | Any qualitative gate | 3 | HALT and escalate to user |

  Each cycle re-verifies all previously failed items + checks new issues. Encode fix-cycle logic as L5 conditional-action items or explicit IF/ELSE in the QA gate item. **(Note: this is the template's native "HALT and escalate" mechanism — relevant to the 4 human-decision items.)**
- **I17 POST-COMPLETION VALIDATION (626-635):** Before status→Done, validate: (1) all `[ ]` marked `[x]`; (2) all output files exist on disk (Glob); (3) blocker entries have resolution notes; (4) if source code modified, tests pass. These items go in `## Post-Completion Actions` BEFORE the frontmatter-update item.
- **I18 TESTING FOR CODE-MODIFYING TASKS (637-646):** If task creates/modifies source code (not docs/config), MUST include ≥1 testing item specifying: test command, pass criteria, where results captured, B2 pattern. Use L3 pattern. Min: unit tests covering modified code.

### Section J — Error Handling (651-673)
- **J1:** every item ends with the embedded blocker clause: "If unable to complete due to missing information, file access issues, or unclear requirements, log the specific blocker using the templated format in the ### Phase [N] Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete."
- **J2/J3:** items never left unchecked; success = output file exists; failure = blocker logged; only mark whole task "⚪ Blocked" if ALL remaining items blocked by the same issue.

### Section K — Example Patterns (675-708)
- **K1** file-by-file processing; **K2** multi-item processing (orchestrator pre-enumerates ALL items at build time; worker NEVER adds items dynamically). One self-contained item per file, no separate verification items.

### Section L — Intra-Task Handoff Patterns (710-835) — subagent/handoff mechanics
**Handoff file convention (718-730):** items write to `.dev/tasks/TASK-NAME/phase-outputs/` with subdirs `discovery/`, `test-results/`, `reviews/`, `plans/`, `reports/`. Files persist across batches/session-rollovers; later items read by path. This is the cross-item information-flow mechanism.
- **L1 Discovery (737-747):** an item explores codebase/env/data → writes a structured machine-readable findings file; the file IS the deliverable. (e.g. Glob + Read → inventory markdown table with summary count.)
- **L2 Build-from-Discovery (749-759):** reads BOTH the discovery file (WHAT to process) AND the source file (CONTENT) → produces output. Always reference both paths.
- **L3 Test/Execute (761-771):** run a command/test, capture BOTH raw output file AND a structured summary file. Used for I18 testing items.
- **L4 Review/QA (773-783):** assess a prior output vs source/spec; MUST produce a structured PASS/FAIL verdict file with criteria checklist + specific issues (Severity Critical/Major/Minor) — never vague "looks good".
- **L5 Conditional-Action (785-797):** behavior depends on a prior result file. MUST handle BOTH branches (IF PASS … / IF FAIL …); output file always created regardless of branch. This is the pattern for "branch based on results".
- **L6 Aggregation (799-809):** Glob to discover all relevant files dynamically (don't hardcode lists), read each, produce consolidated report. Typically final item in a phase.
- **L7 Pattern Selection Guide (811-835):** table mapping need→pattern. Common phase structures: Discovery→Build→Review (L1→L2→L4→L6); Build→Test→Fix (K1/K2→L3→L5); Full Lifecycle (L1→L2→L3→L5→L4→L6); Full Lifecycle w/ QA Gates: L1→L2→**M1 gate**→L3→L5→L4→L6→**M1 gate**.

### Section M — Phase-Gate Composite Patterns (837-860)
- **M1 PHASE-GATE QA SEQUENCE (843-851):** 2-3 items inserted between phases: Item 1 = Aggregation (L6, Glob dynamic); Item 2 = QA Agent Spawn (rf-qa structural; if qualitative needed, rf-qa-qualitative in a SEPARATE following item — sequential, qualitative after structural passes) naming agent/phase type/input paths/output report path/verdict handling/error clause; Item 3 = Conditional Proceed (L5: PASS→next phase, FAIL→fix cycle up to I16 max).
- **M2 APPLICABILITY (852-860):** gate location by task type. **Task-building tasks: after research phase (research-gate), after task file creation (task-integrity).** Document creation: after content phase, before Post-Completion (document-type-specific gate). Code-modifying: after implementation, before testing. When in doubt, include a gate.

## 2. Template 02 — PART 2 Structure (the actual emitted task file)

PART 2 begins after the PART 1 `-->` close (line 888). Copy from `# [Task Title]` (890) to EOF, replacing placeholders. The frontmatter at the top of the file is also part of the template. Emitted structure in order:

1. `# [Task Title]` (890)
2. `## Task Overview` (892) — comprehensive description of what/why.
3. `## Key Objectives` (896) — numbered bold objectives with concrete outcomes.
4. `## Prerequisites & Dependencies` (904):
   - `### Parent Task & Dependencies` (906) — Parent Task, Blocking Dependencies, "This task blocks".
   - `### Previous Stage Outputs (MANDATORY INPUTS)` (914) — INFORMATIONAL ONLY, NO checklist items; lists prior-stage output paths read later in Phase 1 Step 1.4.
   - `### Handoff File Convention` (928) — declares `.dev/tasks/TASK-NAME/phase-outputs/` + subdirs (discovery/test-results/reviews/plans/reports).
   - `### Frontmatter Update Protocol` (943) — the 🟠/🟢/⚪ checkpoint rules.
5. `## Detailed Task Instructions` (954) — contains an ORCHESTRATOR INSTRUCTION BLOCK (HTML comment, lines 956-1010, **removed from output**) that restates B2's 6 required elements + the L1/L2 self-contained examples.
6. **`### Phase 1: Preparation and Setup`** (1012):
   - **Step 1.1 (1044-1046):** first executable item — update status→"🟠 Doing"+start_date AND add Execution Log entry. (I11: status update is the FIRST action.)
   - **Step 1.2 (1048-1050):** create `.dev/tasks/TASK-NAME/phase-outputs/` + 5 subdirs.
   - `### Task-Specific Context Files` (1052) — orchestrator reference list only (usage embedded in Phase 2+ items, not read separately).
7. **`### Phase 2: [Main Execution Phase Name]`** (1063): example steps 2.1 Discovery(L1) → 2.2 Build(L2) → 2.3 Test(L3) → 2.4 Assess/Conditional(L5). Each is a full self-contained B2 paragraph.
8. **`### Phase Gate: Quality Verification`** (1090): `Step PG.1` placeholder QA gate item — spawn rf-qa in [phase-type], write report, PASS/FAIL, fix-cycle on FAIL (max N per I16), blocker→`### Phase Gate Findings`. Remove section if no gate needed.
9. **`### Phase [N]: Testing & Verification`** (1098): placeholder L3 testing item — only when task modifies source code (I18). Remove if docs/config-only.
10. **`### Phase 3: [Review and Quality Assessment]`** (1106): Step 3.1 Review(L4) → Step 3.2 Aggregate(L6).
11. **`## Post-Completion Actions`** (1118) — exactly 4 items (I13/I17):
    - (1120) Glob-verify all output files exist on disk; gap→`### Follow-Up Items`.
    - (1122) If source code modified, run test suite / confirm no regressions (or note "Tests verified in Phase [N]").
    - (1124) Create `### Task Summary` (work completed, challenges, deviations+rationale, blockers+resolution).
    - (1126) Update completion_date/updated_date + status→"🟢 Done" + Execution Log entry. **(This is LAST — frontmatter Done flip comes after validation items.)**
12. **`## Task Log / Notes 📋`** (1128) — sub-sections:
    - `### Task Summary` (1130) — filled in Post-Completion; templated fields: Completion Date, Work Completed, Challenges, Deviations, Blockers Logged (Resolved/Unresolved), Follow-Up Required.
    - `### Execution Log` (1156) — `**[YYYY-MM-DD HH:MM]** - [Action]: [desc]` entries.
    - `### Phase 1 / Phase 2 / Phase 3 - [Name] Findings` (1166/1176/1185) — per-phase blocker/findings sinks (the J1 embedded clause writes here).
    - `### Phase Gate Findings` (1187) — "QA gate verdicts, fix cycle counts, and unresolved issues are recorded here."
    - `### Follow-Up Items Identified` (1191).
    - `### Deviations from Process` (1197).

### "## Execution Context" optional block — NOT PRESENT
Searched the full template (PART 1 + PART 2). There is **no `## Execution Context` block** anywhere in `02_mdtm_template_complex_task.md`. The nearest analogues are `### Context Loading Note` (1022, an orchestrator instruction block that is REMOVED from output) and `### Task-Specific Context Files` (1052, an orchestrator-reference list). If the builder wants an "Execution Context" block, it would be a non-template addition — there is no template-prescribed shape for it. (Unverified whether any done task introduced one — see example survey below.)

### Key takeaways for the sc-recommend lookup-cache build
- This is a **code-modifying task** (Python and/or skill files) → I18 applies → MUST include L3 testing items + Post-Completion test-suite item. M2 places the QA gate after the implementation phase / before testing.
- 2+ phases → I15 requires ≥1 phase-gate QA checkpoint (aggregation + rf-qa spawn + L5 conditional).
- Each item = one verbose B2 paragraph with the 6 elements + J1 blocker clause + completion-gate sentence.
- The native template "halt and escalate to user" mechanism is the **I16 fix-cycle table** (research-gate/report-validation/qualitative → "HALT and escalate to user" after max cycles). For the 4 `needs_human_decision` items, the precedent for HALT shape is found in done tasks (Section 3 below).

## 3. PENDING / HALT / needs_human_decision — exact item shapes (from done tasks)

The user requires "OQ1-3 are needs_human_decision items — write PENDING and halt" plus a Python-vs-skill boundary decision = 4 such items. Note: `needs_human_decision` itself is NOT a task-file checklist construct — it is a return-contract field used by sc-reflect (`.dev/tasks/pr-100-review-fixes/reflect-uc1/return-contract.yaml:62`, a boolean flag alongside `user_decision_required`/`spec_is_wrong`). In **task FILE bodies**, "halt and wait for a human decision" is expressed via two precedent shapes, both verified live:

### Shape 3A — L5 conditional HALT → `⚪ Blocked` + blocker_reason + "DO NOT proceed" (verified)
This is the canonical "stop and escalate" checklist-item shape, used for QA-gate failures AND for any decision the executor cannot make autonomously. Live examples (TASK-PRD-20260514-121039 lines 230, 238):
> "...IF verdict is `**Verdict:** FAIL after 3 fix cycles — HALT and escalate to user`, update the task frontmatter to `status: \"⚪ Blocked\"` and populate `blocker_reason: \"...see qa/...md for details.\"`, write a BLOCKED entry in the ### Phase N Findings section with the specific unresolved issues, and **DO NOT proceed** to [next step] (escalation required)..."

Structural elements of a HALT item:
1. Read the deciding input (report/state file or the source surfaces in question).
2. Branch: IF resolvable → write a PASS/proceed verdict file under `phase-outputs/plans/`; IF needs-human → set frontmatter `status: "⚪ Blocked"` + populate `blocker_reason`, write a BLOCKED entry in `### Phase N Findings`, and DO NOT proceed (subsequent dependent items are blocked).
3. "ensuring the verdict-gate decision is recorded explicitly" + standard J1 blocker clause + completion gate.
4. The verdict/plan file is ALWAYS created regardless of branch (L5 rule).

### Shape 3B — "PENDING" status marker + dedicated `### Open Questions Documented from Build Request` section (verified — best precedent for OQ1-3)
TASK-RF-20260517-213436 is the strongest precedent for "write PENDING and halt for a human decision." It carries 3 Open Questions (OQ-1/OQ-2/OQ-3) that are explicitly **NOT auto-fixed** but surfaced for the maintainer to decide in a separate PR. Mechanics:
- Each OQ is a **documented intentional deferral**, written verbatim into a bottom section titled **`### Open Questions Documented from Build Request`** (lines 443-448). Each entry records: the question, its EXPECTED observable behavior, the **decision the human must make** (e.g. OQ-3: "Decision: add to `_FRESHNESS_SCRIPTS` or document the absence as intentional"), and disposition ("DEFERRED to a separate maintainer PR").
- Acceptance criteria carry a **`PASS/PENDING`** status (line 400: "the AC-1.1 through AC-A.2 ... with their PASS/PENDING status") — i.e. `PENDING` is the literal token used for an acceptance criterion whose resolution awaits a human decision.
- The items that surface each OQ are normal L3/verification items whose "ensuring" clause asserts the EXPECTED-but-unresolved state is present (e.g. line 232: "this is the EXPECTED failure per Open Question OQ-2 ... NOT a regression"), and they do NOT fix it — they **document and defer**.
- Final disposition is carried into the PR description's `## Open Questions / Expected Failures` section verbatim (line 400) and the `### Task Summary` "Open Questions Outcomes" (lines 443-448).

### Recommended shape for THIS task's 4 needs_human_decision items
Combine 3A + 3B. For each of the 4 decisions (Python-vs-skill boundary; OQ1; OQ2; OQ3):
- Emit ONE self-contained checklist item (B2 paragraph) that: reads the relevant source surfaces, **states the decision and the options**, then writes a `PENDING` entry to a dedicated bottom section (e.g. `### Open Questions / Human Decisions Required` or `### Open Questions Documented from Build Request`) capturing question + options + recommendation, AND writes a marker file under `phase-outputs/plans/<decision-id>-PENDING.md`.
- The item MUST instruct: "DO NOT implement either option; this decision requires human input. Set the corresponding acceptance criterion status to `PENDING`. [If the decision blocks downstream items:] update frontmatter `status: \"⚪ Blocked\"` + `blocker_reason`, and HALT — do not proceed past this item until the operator resolves the decision."
- End with the standard J1 blocker clause + completion gate.
- Whether the item flips to `⚪ Blocked` (hard halt) vs. just records `PENDING` and continues (soft defer) depends on whether downstream items DEPEND on the decision:
  - Hard halt (3A: `⚪ Blocked` + DO NOT proceed) when the decision gates subsequent work (the Python-vs-skill boundary likely gates implementation → hard halt).
  - Soft defer (3B: record PENDING, surface in PR, continue) when the decision is orthogonal and only affects a separate follow-up PR (OQ1-3 in 213436 were soft-deferred — work continued, decision surfaced for a separate PR).

## 4. `## Execution Context` optional block — clarification

The block does NOT exist in `02_mdtm_template_complex_task.md` (Section 2 above confirms). HOWEVER it is an **established in-practice convention** emitted between `## Prerequisites & Dependencies` and `## Detailed Task Instructions`, verified live in two done tasks:
- `TASK-RF-20260527-043715-sc-reflect-rebuild.md:128` (`## Execution Context` with `**References:**`/`**Source areas:**`/`**Key constraints:**` at lines 132-134).
- `TASK-RF-20260520-230051.md:118` (same three labels at lines 123-125).

Emitter rules (from prior research file `04-template-examples.md` §10, R-033/R-034/R-035):
- **`**References:**`** — the driving spec / prior research / QA reports.
- **`**Source areas:**`** — directory/area-level groupings ONLY. **MUST NOT contain `file:line` paths** (those belong in each checklist item's Context field).
- **`**Key constraints:**`** — project rules in play (sync-dev/verify-sync parity, never stage `.claude/{skills,commands,agents,hooks,templates}/`, UV-only Python, PER_PHASE QA gate fix-cycle limits per I16).

## 5. Strong template-02 examples surveyed (for the builder)

| Task (path under `.dev/tasks/done/`) | Items / Phases | Why relevant |
|---|---|---|
| `TASK-RF-20260527-043715-sc-reflect-rebuild/` | 73 / 7 | NEW skill build (`src/superclaude/skills/.../SKILL.md` + 11 refs) + Makefile + `make sync-dev`/`verify-sync`/`lint-architecture` gating + per-phase rf-qa gates. Baseline `verify-sync` exit-0 check in Phase 1 (borrow). Refs = one-item-per-ref (textbook K2). Phase 7 `git status` grep guard against `.claude/` staging. |
| `TASK-RF-20260517-213436/` | ~ / 7 | **Best PENDING/OQ precedent.** Surfaces OQ-1/2/3 as documented human decisions, `PASS/PENDING` acceptance statuses, dedicated `### Open Questions Documented from Build Request` section, deferral to a separate PR. Per-phase + PG-5 (task-integrity) + PG-6 (aggregate) gates. Captures EXIT codes to `phase-outputs/test-results/`. |
| `TASK-RF-20260520-230051/` | 21 / 5 | Small surgical SKILL.md + hook + evals.json edits; single FINAL_ONLY rf-qa gate; L5 conditional verdict file for `verify-sync`; per-file syntax gates (`bash -n`/`markdownlint`/`jq .`) before sync; commit/push explicitly OUT OF SCOPE. |
| `TASK-PRD-20260514-121039/` (to-do) | ~ / 7 | Live HALT-item shape: two sequential QA gates (rf-qa report-validation → rf-qa-qualitative), each with `⚪ Blocked`+`blocker_reason`+"DO NOT proceed" HALT branch (3A). Adversarial-stance rf-qa spawn prompts embedded verbatim. |

### Builder takeaways
1. `template_schema_doc: ".claude/templates/workflow/02_mdtm_template_complex_task.md"` (all prior examples).
2. `assigned_to` per convention is `"rf-task-executor"`; `coordinator: orchestrator`.
3. Phase 1 Step 1.1 = status→🟠 Doing FIRST (I11); Step 1.2 = create `.dev/tasks/<TASK-ID>/phase-outputs/{discovery,test-results,reviews,plans,reports}/`.
4. Emit a Phase-1 baseline `make verify-sync` exit-0 check before edits (Example A precedent).
5. This is code-modifying (Python and/or skill) → I18 testing items (L3) + Post-Completion test re-run; M2 puts the QA gate after implementation, before testing.
6. Per-phase rf-qa M1 gates if >20 items; pair each rf-qa spawn with "ADVERSARIAL STANCE." + `fix_authorization: true` (user memory `feedback_rfqa_adversarial_pattern.md`) and the "NO team context — do NOT use SendMessage/TaskCreate/..." escalation override.
7. Final phase = Sync & Validate: `make sync-dev` → `make verify-sync` (exit 0, max 2 retries, L5 verdict file) → `make lint` (if `.py`) → `make lint-architecture` (if SKILL.md) → `git status --short` grep guard that NO `^[AM]  \.claude/(skills|commands|agents|hooks|templates)/` line matches.
8. Post-Completion Actions (I17, 4 items): Glob output-existence → test re-run → `### Task Summary` → frontmatter →🟢 Done LAST.
9. Every item ends with the J1 blocker clause + completion-gate sentence.
10. The 4 human-decision items: use Shape 3A (hard halt → `⚪ Blocked`) for the Python-vs-skill boundary if it gates implementation; Shape 3B (PENDING + dedicated Open-Questions section, soft-defer) for OQ1-3 unless they block downstream items.

## Status

**Status: Complete**

### Summary
- **Template source:** `.claude/templates/workflow/02_mdtm_template_complex_task.md` (85583 bytes). PART 1 = build instructions (Sections A-M, lines 68-860); PART 2 = the emitted task-file template (lines 890-1205). Fully documented above: frontmatter fields; A3 granular breakdown; A4 iterative pre-enumerate/process/consolidate; B2 6-element self-contained item; L1-L6 handoff/subagent patterns; M1/M2 phase-gate QA; I15-I18 (phase gates, post-completion validation, code-test requirement); F2a parallel-spawning exception.
- **`## Execution Context`:** NOT in the template, but an established convention (verified live in `TASK-RF-20260527-043715:128` and `TASK-RF-20260520-230051:118`) with `**References:**`/`**Source areas:**`/`**Key constraints:**` labels; Source areas must NOT carry `file:line`.
- **PENDING/HALT/needs_human_decision:** `needs_human_decision` is a sc-reflect return-contract field, not a task-file construct. The task-file precedents are Shape 3A (L5 conditional → `status: "⚪ Blocked"` + `blocker_reason` + "DO NOT proceed", verified in TASK-PRD-20260514-121039:230,238) and Shape 3B (`PENDING` acceptance status + dedicated `### Open Questions Documented from Build Request` bottom section, decisions deferred to operator/separate PR, verified in TASK-RF-20260517-213436:400,443-448). For this task's 4 decisions: hard-halt the implementation-gating boundary decision (3A); soft-defer OQ1-3 as PENDING Open Questions (3B) unless they gate downstream items.
