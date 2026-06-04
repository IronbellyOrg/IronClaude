# Research 05: MDTM Template 02 Rules + Low-Spec Worked Example

**Status:** Complete
**Date:** 2026-06-02
**Track:** Implement 4 Medium-Complexity Serena Adoptions (FR-RV3-MED.1-4)
**Scope:** `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` + sibling low-complexity Serena task file

---

## Note on file location

The Template 02 file does NOT exist at `.claude/templates/workflow/` in this worktree (the `.claude/`
sync-dev mirror is not present here). It was read from the source-of-truth path:
`src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` (1205 lines total).
The builder reads the same content regardless of mirror path.

---

## 1. Template 02 PART 1 — Rules the Builder MUST Follow

PART 1 (lines 46-888, inside an HTML comment block) is orchestrator/builder-only guidance and does NOT
appear in the output task file. PART 2 (lines 890-1205) IS the literal task-file template to copy.

### Frontmatter — required fields (lines 1-44)

The builder MUST emit YAML frontmatter with these fields (template lines 2-43):
`id`, `title`, `description`, `status` (`"🟡 To Do"`), `type`, `priority`, `created_date`,
`updated_date`, `assigned_to`, `autogen`, `autogen_method`, `coordinator`, `parent_task`,
`depends_on` (list), `related_docs` (list of `{path, description}`), `tags` (list),
`template_schema_doc`, `estimation`, `sprint`, `due_date`, `start_date`, `completion_date`,
`blocker_reason`, `ai_model`, `model_settings`, `review_info` (`last_reviewed_by`/`last_review_date`/`next_review_date`),
`task_type` (line 43 — `static` for fixed content, `dynamic` for discovered content per I6).

### SECTION A — Core Principles

- **A1 Workflow doc availability (lines 72-83):** Check for governing workflow docs. If none exist,
  OMIT all `[WORKFLOW-DEPENDENT]` sections and derive requirements directly from the spec/user input —
  but keep the SAME granularity/structure. For the Medium track, the governing source is the spec
  `.dev/releases/current/Reflect-V3.5-Serena_Mediums/05-spec-medium-complexity.md` (FR-RV3-MED.1-4),
  so workflow-dependent ceremony (Stage X references, Cross-Stage Integration) is OMITTED; requirements
  come from the spec.
- **A3 Complete Granular Breakdown (lines 91-95):** Break EVERY phase into atomic, verifiable checklist
  items. Individual item for EVERY file/component/iteration. NO high-level or bulk operations. Include
  exact file paths, specific requirements, measurable outcomes.
- **A4 Iterative Process Structure (lines 97-116):** For any multi-item process: (1) pre-enumerate ALL
  items in an initial step, (2) one checklist item per specific item, (3) incremental update after each,
  (4) consolidation step only AFTER all items complete. The prescribed Step X.1 (enumerate) → X.2
  (process each) → X.3 (consolidate) shape.
- **A5/A6 (lines 118-128) are `[WORKFLOW-DEPENDENT]`** — omitted when no workflow doc (this track).

### SECTION B — Self-Contained Checklist Items (CRITICAL, lines 130-196)

- **B1 (lines 134-140):** Session-rollover protection. Rigorflow batches across sessions; context from
  batch 1 is GONE by batch 3+. So every item must be self-contained. Standalone "read context" items
  are USELESS (context lost before use).
- **B2 — the 6 mandatory elements (lines 142-148):** every item embeds (1) Context Reference + WHY,
  (2) Action + WHY, (3) Output Specification (exact path/name/content/template), (4) Integrated
  Verification ("ensuring..." clause; no fabrication, 100% source-derived, document negative evidence),
  (5) Evidence on Failure Only (log blocker to Task Log; success evidenced by output file), (6) Explicit
  Completion Gate ("This item cannot be marked as done until... Once done, mark this item as complete.").
- **B3 (lines 150-153):** Each item is ONE FULL PARAGRAPH (not bullets/multi-line), verbose, reads like
  a standalone prompt.
- **B5 FORBIDDEN (lines 164-184):** standalone "read context" items; missing context reference; multi-line/
  bulleted items; separate verification/confirmation items (integrate via "ensuring..."); overly granular
  items ("create directory" alone); separate REMINDER blocks between items.
- **B7 Key principles (lines 189-196):** output file = evidence of success; only log on FAILURE; QA
  process handles verification between batches (do NOT create separate verification items).

### SECTION C — Embedding (NOT separate sections, lines 198-230)

Outputs/Deliverables (C1), Success Criteria (C2), Verification (C3) are EMBEDDED in items, never their
own sections. C4: task completion handled by the Post-Completion Actions section only.

### SECTION D — Mandatory Sections (lines 232-272)

- D1 Workflow Compliance Declaration + D2 Cross-Stage Integration are `[WORKFLOW-DEPENDENT]` (omit here).
- **D3 CRITICAL RULE (lines 269-272):** NO checklist items may appear before Phase 1. Order is
  Frontmatter → (Workflow Compliance informational) → Prerequisites (informational) → Phase 1 (first
  executable items). Context-review/previous-stage-input items live IN Phase 1, Steps 1.2-1.4.

### SECTION E — Checklist Structure (lines 274-389)

- **E1 (lines 278-292):** Every actionable item is `- [ ]`. FLAT structure only — NO nested checkboxes,
  NO parent checkboxes summarizing children. Use `**Step X.Y:**` bold headers for grouping (not checkboxes).
- **E2 (lines 294-348):** Summary/parent checkboxes come AFTER component items, never before. Components
  first, summary last.
- **E3 (lines 350-366):** Sequential top-to-bottom only. FORBIDDEN: "mark item complete in section above",
  "see checklist below", any backward movement, parent-with-child checkboxes.
- **E4 (lines 367-388):** Never put checkboxes next to step numbers (step numbers are bold headers).
  NO separate REMINDER blocks between items (worker agents only see batch items, not surrounding prose) —
  integrate reminders INTO the item.

### SECTION F — Execution (worker-agent, lines 390-451)

- **F1 (lines 394-403):** READ → IDENTIFY → EXECUTE → UPDATE → REPEAT (one unchecked item at a time).
- **F2 / F2a (lines 405-430):** No multi-item execution within a session; no delegating across phase
  boundaries; a subagent gets work from a SINGLE checklist item only; no skipping phase-gate QA or
  post-completion validation. **Parallel spawning exception (line 430):** consecutive items in the SAME
  phase that spawn INDEPENDENT subagents may be spawned in parallel; each marked individually.
- **F5 (lines 447-451):** Frontmatter update protocol (Doing on start, Done on completion, Blocked +
  blocker_reason, updated_date each session).

### SECTION G — Headless Agent Context (lines 453-469)

G1: Framework context files (ib_agent_core.md, quality_gates.md, anti_hallucination_task_completion_rules.md,
anti_sycophancy.md, file_conventions.md) are NOT auto-loaded into headless workers. G2: reference the
specific rule file in the item OR (preferred) reference a template that incorporates the conventions.
G3: embed task-specific context directly in items, never separate "context loading" steps.

### SECTION H — Tool Specification (lines 471-490)

H1: by default let the model pick tools. H2/H3: only specify a tool when a SPECIFIC tool is required
(e.g., "use the Bash tool to run `uv run pytest`", "use Glob to find..."), embedded in the item.

### SECTION I — Additional Guidelines (lines 492-649)

- I1 explicit directive language ("YOU MUST"/"DO NOT"). I2 extreme granularity. I3 incremental file
  modification ("DO NOT attempt to complete entire files at once" + save points). I6 dynamic content
  (`task_type: static` vs `dynamic`). I7/I8 explicit/mandatory template usage. I9/I14 anti-hallucination
  controls. I11 status→Doing is the FIRST action. I12 verification integrated (no separate items).
  I13 Post-Completion Actions = final task items only.
- **I15 PHASE-GATE QA ENFORCEMENT (lines 599-607):** Any task with 2+ execution phases MUST include
  at least one phase-gate QA checkpoint between the primary execution phase and any dependent later phase.
  A gate = (1) aggregation item collecting outputs, (2) QA agent spawn item (rf-qa or rf-qa-qualitative,
  self-contained B2 shape, with phase type, input files, report path, verdict handling, error clause),
  (3) conditional-action item (proceed on PASS / fix cycle on FAIL).
- **I16 QA Verdict + Fix Cycles (lines 609-624):** Binary PASS/FAIL — ANY severity issue = FAIL. Fix-cycle
  caps by gate type (research-gate 3, synthesis-gate 2, report-validation 3, task-integrity 2, any
  qualitative 3). Each cycle re-verifies all prior failures + checks for new issues.
- **I17 POST-COMPLETION VALIDATION (lines 626-635):** Before status→Done, validate: (1) all `- [ ]`
  marked `- [x]`, (2) all output files exist on disk (via Glob), (3) blocker entries have resolution notes,
  (4) if source code modified, all relevant tests pass.
- **I18 TESTING for code-modifying tasks (lines 637-646):** If a task creates/modifies SOURCE CODE (not
  docs/config), MUST include ≥1 testing item that (1) specifies the test command, (2) defines pass
  criteria, (3) specifies where results are captured, (4) follows B2. Use the L3 (Test/Execute) pattern.

### SECTION J — Error Handling (lines 651-673)

Error handling embedded in every item: on failure, log blocker to `### Phase [N] Findings` in Task Log,
then mark the item complete. Items are NEVER left unchecked. Only mark whole task "⚪ Blocked" if ALL
remaining items are blocked by the same issue (J3).

### SECTION L — Intra-Task Handoff Patterns (lines 710-836)

Handoff file convention: items write to `.dev/tasks/TASK-NAME/phase-outputs/{discovery,test-results,reviews,plans,reports}/`
(persisted across batches/rollovers; later items read by path). Patterns:
- **L1 Discovery (lines 737-747):** explore + write structured findings file (the file IS the deliverable).
- **L2 Build-from-Discovery (lines 749-759):** read discovery file AND source file; create deliverable.
- **L3 Test/Execute (lines 761-771):** run command; capture BOTH raw output AND structured summary.
- **L4 Review/QA (lines 773-783):** assess output vs source; structured PASS/FAIL verdict (never "looks good").
- **L5 Conditional-Action (lines 785-797):** branch on prior result; MUST handle BOTH success+failure;
  always create output file.
- **L6 Aggregation (lines 799-809):** Glob to discover files dynamically; consolidate into report.
- **L7 Pattern Selection Guide (lines 811-835):** common structures — Discovery→Build→Review (L1→L2→L4→L6);
  Build→Test→Fix (K1/K2→L3→L5); Full Lifecycle with QA Gates (L1→L2→**M1**→L3→L5→L4→L6→**M1**).

### SECTION M — Phase-Gate Composite Patterns (lines 837-860)

M1: a phase-gate is a 2-3 item sequence (L6 aggregation → QA agent spawn → L5 conditional proceed).
M2 applicability table — **Code-modifying tasks: gate after implementation phase and before testing
phase (if separate), or after combined implement+test phase** (line 857).

### SECTION K — Example Patterns (lines 675-709)

K1 File-by-file processing; K2 Multi-item processing (orchestrator MUST enumerate ALL items at build
time; worker NEVER adds items dynamically).

---

## 2. Item Format — Exact Self-Contained Skeleton (5/6-field shape)

The canonical skeleton, quoted from B4 CORRECT EXAMPLE (template lines 155-158), shows all 6 B2 elements
woven into ONE paragraph:

> Read the file `component-spec.md` at `docs/specs/component-spec.md` to extract the API interface
> requirements ... [Context+WHY], then create the file `ApiHandler.ts` at `src/handlers/ApiHandler.ts`
> containing a TypeScript class that implements all methods ... [Action+Output], ensuring the file
> includes the standard header comment block, exports the class as the default export, all methods from
> the spec are implemented with correct signatures, no content is fabricated or assumed beyond what the
> source explicitly states, and no placeholder or TODO comments remain [Integrated Verification — "ensuring..."].
> If unable to complete due to missing information, file access issues, or unclear requirements, log the
> specific blocker using the templated format in the ### Phase 2 Findings section of the ## Task Log /
> Notes at the bottom of this task file, then mark this item complete [Evidence on Failure Only].
> Once done, mark this item as complete. [Completion Gate]

**Standard tail every item ends with (verbatim from B4/J1/K1):**
"If unable to complete due to missing information, file access issues, or unclear requirements, log the
specific blocker using the templated format in the ### Phase [N] Findings section of the ## Task Log /
Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete."

**Anti-orphaning (completion items inside final phase):** Per C4/I13/I17, all completion/validation items
live in the `## Post-Completion Actions` section (PART 2 lines 1118-1126), which is the LAST section
before the Task Log — never floating between phases. The four Post-Completion items are: (1) Glob-verify
all output files exist, (2) re-run tests if source modified, (3) write `### Task Summary`, (4) update
frontmatter to Done + Execution Log entry.

**Task Log section (PART 2 lines 1128-1205):** mandatory trailing section `## Task Log / Notes 📋` with
sub-sections: `### Task Summary` (filled in Post-Completion), `### Execution Log`, `### Phase N Findings`
(one per phase, blocker-entry template), `### Phase Gate Findings`, `### Follow-Up Items Identified`,
`### Deviations from Process`.

---

## 3. Worked Example — Sibling LOW-Complexity Serena Task (TASK-RF-20260602-135209)

File: `.dev/tasks/to-do/TASK-RF-20260602-135209/TASK-RF-20260602-135209.md` (596 lines). Same skill
(sc-reflect-protocol), same author intent, same Serena-adoption release. This is the CLOSEST possible
template for the Medium task file. It implements 8 LOW FRs; the Medium task implements 4 MED FRs.

### How it phased the FRs (lines 120-490)

It used the spec's **§4.6 implementation order** as the phase ordering, with ONE phase per FR (or per
co-shipping FR pair), each phase ending in its own QA gate:
- **Phase 1** (lines 120-154): Preparation + OQ precondition probes + a baseline-state gate. Status
  update is Step 1.1 (I11). Handoff dirs are Step 1.2 (D3/template Step 1.2). OQ probes are Steps 1.3-1.6.
  A `### Phase 1 Exit Gate` (line 152) blocks Phase 2 until the baseline gate logs PASS.
- **Phase 2** = FR-7+FR-6 (co-ship), **Phase 3** = FR-1+FR-2 (co-ship) + the 5-site contract bump,
  **Phase 4** = FR-4, **Phase 5** = FR-8, **Phase 6** = FR-3 (OQ-1-gated), **Phase 7** = FR-5 (pilot-gated, ships last).
- Each implementation phase is followed by a `### Phase Gate PG-N` (lines 206, 286, 334, 378, 410, 466)
  with a single rf-qa `task-integrity` spawn item (M1/I15 gate).
- **Phase 8** (line 474): terminal **structural (rf-qa) + qualitative (rf-qa-qualitative)** gate PAIR —
  Step 8.1 L6 aggregation, Step 8.2 structural (must PASS before 8.3), Step 8.3 qualitative.

### How granular the items are — PER-FR-FACET, finer than per-FR

Items decompose each FR into its constituent EDIT SITES, not one item per FR. A single FR yields many
items: allowed-tools edit → §4.0/§6.1 prose edit → §9.1 contract field → §9.2 telemetry → refs mirror
edit → sync-dev → verify-sync → eval fixtures → expected.yaml → evals.json append → QA gate. E.g. FR-7+FR-6
(Phase 2) is 11 items (Steps 2.1-2.11) + 1 gate. Each item targets ONE file region. This is A3-level
"individual checklist item for EVERY file/component/iteration" applied to skill-protocol edits.

### How it handled the inline §9 contract edits — atomic multi-site bump

The contract_version bump is a SINGLE item (Step 3.4, lines 230-232) that applies an "atomic 5-EDIT SET"
to five literal sites in SKILL.md §9.1/§9.4/§12.x in one Edit, with an embedded verification ("verify
with a fresh `grep -nE \"contract_version\"`... no `\"1.0\"` literal remains except the §9.4 rule-bullet
examples"). New contract FIELDS are separate per-FR items, each scoped to the matching `# UC-1 specific`/
`# UC-2 specific` banner inside the §9.1 fence (Steps 3.5, 3.6, 4.2). KEY: every contract/inline edit
item opens with a **fresh-Read relocate** instruction (see the global CRITICAL block at line 116) because
research line numbers drift after earlier edits.

### How it wrote sync-dev / verify-sync items (L3 Test/Execute pattern)

EVERY src-editing phase ends with a sync-dev item then a verify-sync+lint item (Steps 2.7/2.8, 3.10/3.11,
4.5/4.6, etc.). Representative pair:
- **sync-dev item (Step 2.7, line 188):** "Use the Bash tool to run `make sync-dev` from the repo root
  ... capturing the complete output to the file `phase2-sync-dev.txt` at `.dev/tasks/.../phase-outputs/
  test-results/phase2-sync-dev.txt`, ensuring the command exits successfully ...; the `.claude/` mirror
  MUST exist for Claude Code to read but MUST NEVER be staged (it is gitignored sync-dev output)."
- **verify item (Step 2.8, line 192):** runs `make verify-sync` + `npx markdownlint-cli <edited files> ||
  true`, writes a structured `phaseN-verify.md` summary recording PASS/FAIL + exit code + drift paths +
  lint violations, and embeds "any markdownlint violation in the edited files is fixed in `src/...` (then
  re-run sync-dev) before the gate." Later verify items add static greps (e.g. Step 3.11 confirms the
  5-site bump left no stale `"1.0"`, and `check_onboarding` returns 0).

Eval-workspace edits (`.dev/eval-workspaces/...`) explicitly carry "NOT under `src/superclaude/` so NO
sync-dev applies" (e.g. Step 2.9, line 196).

### How it documented OQs — `### Open Questions` in the Task Log + probe items in Phase 1

OQs are NOT left as task-blocking ambiguity. They are (a) recorded in a `### Open Questions` subsection
of the Task Log (lines 530-542), and (b) operationalized as **runtime-probe precondition items** in Phase 1
(Steps 1.3-1.6) that write a record file to `phase-outputs/plans/` and gate the dependent FR phase. The
opening note (line 532): "Task items are NOT based on unresolved external surfaces — those are encoded as
runtime-probe precondition items." Each OQ entry states status (BLOCKING / RESOLVED POSITIVE / RESOLVED /
piloted) and WHERE it is encoded (which Step). Intentional new conventions (colon-namespaced degrade
tokens, line 542) are flagged so QA does not "fix" them back.

### 2-3 representative items (quoted)

1. **Status-update opener (Step 1.1, line 126)** — the mandated first action (I11), self-contained:
   > "Update `status` to "🟠 Doing" and `start_date` to current date in the frontmatter of this file,
   > then add a timestamped entry to the ### Execution Log ... using the format `**[YYYY-MM-DD HH:MM]** -
   > Task started: ...`, ensuring no other frontmatter field is altered. Once done, mark this item as complete."

2. **allowed-tools edit with corrected-form guard (Step 2.1, line 164)** — Context+WHY → fresh Read →
   surgical Edit → "ensuring..." with the negative guard:
   > "Read research file `01-skill-insertion-points.md` ... to extract the frontmatter `allowed-tools`
   > edit shape ..., then perform a fresh Read of `src/superclaude/skills/sc-reflect-protocol/SKILL.md`
   > to locate the current `allowed-tools:` line ..., then edit ONLY `...SKILL.md` to insert
   > `mcp__serena__get_current_config` ... ensuring the tool is added exactly once, `check_onboarding_performed`
   > is NOT added (it was DELETED in Serena v1.5.0 ...), the serena cluster stays contiguous, and no
   > existing tool token is removed or reordered. If the anchor cannot be located, log the blocker in the
   > ### Phase 2 Findings section ..., then mark this item complete. Once done, mark this item as complete."

3. **QA gate spawn item (Step PG-2.1, line 210)** — the M1/I15 gate with byte-exact adversarial stance,
   `fix_authorization: true`, report path, and the fix-cycle retry ordering:
   > "Spawn rf-qa in `QA_MODE: task-integrity` with `fix_authorization: true` and the byte-exact
   > adversarial stance `ADVERSARIAL STANCE: Assume the work contains errors. ...` to verify all Phase 2
   > outputs ... directing the agent to write its PASS/FAIL verdict with an enumerated coverage checklist
   > to `.dev/tasks/.../phase-outputs/reviews/pg2-fr7-fr6-qa.md`. IF the verdict is FAIL, read the report,
   > fix every finding in the relevant `src/...`/eval files, re-run `make sync-dev` + `make verify-sync`,
   > then re-spawn rf-qa for up to two task-integrity fix cycles applying the retry ordering regression →
   > monotonicity → hard-cap → proceed ...; after 2 cycles without PASS, record unresolved issues as Open
   > Questions ... and HALT the phase. No later phase may begin unless this gate's verdict is PASS. ..."

### Frontmatter the sibling used (lines 1-43) — directly reusable shape for the MED task

`template_schema_doc: "src/superclaude/templates/workflow/02_mdtm_template_complex_task.md"`,
`autogen_method: "task-builder"`, `coordinator: orchestrator`, `parent_task: "Reflect-V3-Serena"`,
`assigned_to: "rf-task-executor"`, `type: "📝 Documentation"`, `task_type: static`, `status: "🟡 To Do"`.
`related_docs` points at the driving spec, the primary SKILL.md edit target, and the research/ dir.

### Reader-aid `## Execution Context` block (lines 102-108)

The sibling added a non-template `## Execution Context` rollup (References / Source areas / Key constraints)
AFTER Prerequisites and BEFORE `## Detailed Task Instructions`, with a disclaimer (line 104) that per-item
Context references remain authoritative. Also added three global CRITICAL preamble blocks before Phase 1
(lines 114-118): SOURCE-OF-TRUTH DISCIPLINE, FRESH PRE-EDIT READ, CORRECTED-FORM GUARDS — these apply to
every edit item. The MED task should carry the analogous globals (SoT discipline, fresh-Read, scope guards).

---

## 4. Common Pitfalls to Avoid (from template + sibling example)

1. **Batch items / multi-item paragraphs** — E1/A3: one atomic action per `- [ ]`. Do NOT fold "edit
   §6.1 AND §9.1 AND telemetry" into one item; the sibling splits these into separate Steps.
2. **Vague verification** — L4/C2/C3: never "looks good" / "verify the file". Verification is an embedded
   "ensuring..." clause naming concrete, source-derived checks (exact counts, "no stale literal remains",
   "tool added exactly once").
3. **One-shot file writes** — I3: "DO NOT attempt to complete entire files at once." Build incrementally;
   for evals.json the sibling does fresh-Read max-id → append-one-object (Steps 2.11/3.14/...).
4. **Staging `.claude/`** — CLAUDE.md ABSOLUTE RULE + sibling's per-sync-item reminder: `.claude/` mirror
   is gitignored sync-dev output; NEVER `git add` it; if `git add` needs `-f` on a `.claude/` path, STOP.
   Edit `src/superclaude/` → `make sync-dev` → `make verify-sync`; stage only the `src/` side.
5. **Standalone "read context" items** — B5/B1: forbidden; context read in batch 1 is lost by batch 3+.
   Every item embeds its own Context Reference + Action + Output.
6. **Stale research line numbers** — sibling's FRESH PRE-EDIT READ global: always re-Read the target to
   relocate the anchor before a line-specific Edit; do not trust research line numbers alone.
7. **Parent/summary checkbox before children** — E2/E3: summary checkboxes come AFTER components; flat
   structure only, no nested checkboxes.
8. **Separate REMINDER blocks between items** — E4: worker agents only see batch items, not surrounding
   prose; fold any reminder INTO the item text.
9. **Missing phase-gate / post-completion validation** — I15/I17/F2: a 2+-phase task MUST have a QA gate
   between dependent phases and Post-Completion validation (Glob output-file check, test re-run if source
   modified, frontmatter→Done as the LAST item).
10. **Wiring out-of-scope tools** — sibling's CORRECTED-FORM GUARDS: name the explicitly-excluded surfaces
    (deleted tools, project-mutating symbolic-editing tools) as negative "ensuring..." assertions.

---

## 5. Batch Size / Item-Count Bounds

Per the task-builder add-on rule **TB-Add-2** (named in this track's research scope): a single-track task
targets **3-50 checklist items**; the per-track (multi-track) bound is **3-40**. This MED track is a
single track. The sibling LOW task ran ~70+ items across 8 phases for 8 FRs (≈8-9 items/FR including the
eval scaffold + 2 sync/verify items + 1 gate per phase). For the MED track's **4 FRs**, expect roughly the
same per-FR density; if the natural decomposition exceeds 50 items, that is a signal to consolidate
genuinely-atomic sub-edits (e.g. a multi-site contract bump as ONE atomic item, as the sibling did in
Step 3.4) rather than to drop granularity. Keep one QA gate per phase + a terminal structural+qualitative
pair (Phase 8), which the bound must accommodate.

> NOTE: The exact "3-50 / 3-40" numbers come from the task-builder TB-Add-2 rule named in the track scope;
> they were NOT located inside Template 02 itself (Template 02 mandates granularity via A3 but sets no
> numeric item ceiling). The builder should treat TB-Add-2 as the authoritative bound.

---

## Summary

- **Template 02 source path:** `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md`
  (1205 lines; PART 1 = builder instructions inside an HTML comment, lines 46-888; PART 2 = the literal
  task-file template, lines 890-1205). Not present at `.claude/` in this worktree.
- **B2 6-element self-contained item** (Context+WHY / Action+WHY / Output / Integrated "ensuring..."
  Verification / Evidence-on-failure-only / Completion Gate), ONE paragraph each (B3); standard failure
  tail + "Once done, mark this item as complete." verbatim.
- **Mandatory structure:** frontmatter (28 fields incl. `task_type`), Task Overview, Key Objectives,
  Prerequisites & Dependencies, NO checklist before Phase 1 (D3), Phase 1 = status-update (I11) +
  handoff-dir create + context/probe items, execution phases using L1-L6 handoff patterns, M1/I15
  phase-gate QA between dependent phases (PASS/FAIL, fix-cycle caps per I16), I18 testing item if source
  code is modified, Post-Completion Actions (I17 validation → Task Summary → frontmatter→Done as LAST
  item), Task Log / Notes with per-phase Findings + Open Questions + Execution Log.
- **Closest worked example:** sibling LOW task `.dev/tasks/to-do/TASK-RF-20260602-135209/...md` — one
  phase per FR(-pair), per-FR-facet item granularity, atomic multi-site contract bump (Step 3.4), L3
  sync-dev+verify-sync pair per phase, eval scaffolds NOT sync-dev'd, OQs as Phase-1 runtime-probe
  precondition items + a `### Open Questions` Task-Log subsection, per-phase rf-qa task-integrity gates
  + terminal rf-qa + rf-qa-qualitative pair, three global CRITICAL preamble blocks (SoT / fresh-Read /
  scope guards).
- **Bounds:** TB-Add-2 single-track 3-50 items (per-track 3-40); Template 02 itself imposes no numeric cap.

**Status:** Complete
