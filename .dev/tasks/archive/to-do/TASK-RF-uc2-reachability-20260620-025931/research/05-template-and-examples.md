# R5 Research — Template & Examples (MDTM Template 02 + complex TASK-RF example)

Status: Complete
Date: 2026-06-20
Researcher: R5 of 5 (Track 1)
Scope: `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` (PART 1 rules) + one complex TASK-RF example.

**Summary:** Documented the full MDTM Template 02 rule surface the builder must obey — PART 1 (lines 68-1127): Section A granular-breakdown (A3) + iterative-process (A4); Section B self-contained 6-field item (B2: Context+WHY / Action+WHY / Output / "ensuring" Verification / Evidence-on-failure-only / Completion-gate); Sections C-E embedding/mandatory-sections/checklist-structure; F execution loop; the I13-I22 QA-hardening core (I15 phase-gate, I16 verdict/cycles, I17 post-completion validation, I19 lens minimums, I20 serialized fix, I21 fidelity gate, I22 intensity); Section L L1-L6 handoff patterns + L7 selection guide; Section M M3 lens-QA 8-step sequence + M4 fidelity 6-step. PART 2 (lines 1143-EOF): frontmatter fields (incl. `spec_path`, `reflect_pre`, `reflect_post`, `template_schema_doc`; NOTE — no literal `start_commit`/`executor_model_class` in the bare template, they are builder-added), body-section order, the `## Execution Context` shape (References/Source-Areas/Key-Constraints — AREA-level, NO file:line), and the anti-orphaning Post-Completion ordering (POST reflect penultimate, Update-status-to-Done terminal). Cross-validated against the real example `TASK-RF-reflect-post-gate-wiring-20260611-022409.md` (M3 6-agent lens gate items 6.1/6.2, I20 serialized fix 6.2.1, and the POST `superclaude reflect run … --depth deep --fix --no-promote` wrapper item 6.3 behind the `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` skip guard, immediately before 6.4). Citations: `02:` = template, `ex:` = example task file.

---

## 1. Template file map

`src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` (120,364 bytes).
- **PART 1 — TASK BUILDING INSTRUCTIONS** = lines 68-1127 (orchestrator/builder only; NONE of it appears in the output task file). `02:68-82`.
- **PART 1 END** = line 1127. **PART 2 — TASK FILE TEMPLATE** (the clean structure that IS the output) starts line 1143. `02:1127`, `02:1143-1146`.
- Template 02 "Extends Template 01 with Section L: Intra-Task Handoff Patterns. Use this template when tasks require discovery, testing, review, conditional logic, or aggregation between checklist items." `02:78-80`.
- `.claude/templates/` is empty in this worktree — the LIVE template is the `src/` copy above (confirmed: only `src/superclaude/templates/workflow/` holds these files).

## 2. SECTION A — Core Principles (rules A1-A6)

- **A1 Workflow-document availability check** `02:89-100`: builder MUST check for governing workflow docs (`.gfdoc/workflows/`, `.roo/workflows/`). If they EXIST → follow workflow sections. If they DON'T → OMIT all `[WORKFLOW-DEPENDENT]` sections, replace workflow refs with direct user requirements, keep same detail/structure.
- **A2 Workflow deep integration** `[WORKFLOW-DEPENDENT]` `02:102-106`.
- **A3 COMPLETE GRANULAR BREAKDOWN** `02:108-112`: break EVERY phase into atomic verifiable checklist items; individual item for EVERY file/component/iteration; NO high-level/bulk ops; include exact file paths + measurable outcomes.
- **A4 ITERATIVE PROCESS STRUCTURE** `02:114-133`: for any multi-item process — (1) pre-enumerate ALL items in an initial step, (2) one checklist item per specific item, (3) incremental updates after each, (4) consolidation step ONLY after all complete. Pattern is `Step X.1 scan/enumerate → Step X.2 per-item → Step X.3 consolidate`.
- **A5 Cross-stage integration** `[WORKFLOW-DEPENDENT]` `02:135-139`. **A6 Workflow compliance enforcement** `[WORKFLOW-DEPENDENT]` `02:141-145`.

## 3. SECTION B — Self-contained checklist items (CRITICAL)

- **B1 Why** `02:151-157`: session-rollover protection — context from batch 1 is GONE by batch 3+, so every item must embed its own context; standalone "read context" items are USELESS.
- **B2 The 5(+1)-field self-contained item** `02:159-165`. Every checklist item MUST be a complete self-contained prompt including:
  1. **Context Reference with WHY** — what file(s) to read + why needed for THIS action.
  2. **Action with WHY** — what to do + why.
  3. **Output Specification** — exact output file name, location, content, template to follow.
  4. **Integrated Verification** — an "ensuring..." clause (DO NOT assume/hallucinate; 100% from source files; document negative evidence on failure).
  5. **Evidence on Failure Only** — log to task notes ONLY on blocker/missing-info/error (success is evidenced by the output file).
  6. **Explicit Completion Gate** — literal: "This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete."
- **B3 pattern** `02:167-170`: each item = ONE FULL PARAGRAPH (not bullets), verbose, reads like an independently-executable prompt.
- **B4 correct example** `02:172-179`: action + verification integrated; "Do NOT create separate verification items."
- **B5 FORBIDDEN** `02:181-200`: standalone "read context" items; missing context reference; multi-line/bulleted items; separate verification/confirmation items; overly granular items ("create directory" alone); separate REMINDER blocks between items.
- **B7 key principles** `02:206-213`: each item is a complete independently-executable prompt; context + verification embedded IN the action; output files = evidence; only log on FAIL/BLOCK; QA handles verification between batches (see I15-I16).

## 4. SECTION C — Embedding requirements (NOT separate sections)

Collected during planning but EMBEDDED into items, never their own sections `02:216-247`:
- **C1 Outputs/Deliverables** embed in the creating item; output file itself = evidence; NO "Outputs & Deliverables" section. `02:223-228`
- **C2 Success criteria** embed as "ensuring..." clause; NO separate criteria items/section. `02:230-234`
- **C3 Verification** embed in action items via "ensuring..."; NO separate verification items/section; intra-task QA handles between batches (I15 phase-gate, I17 post-completion). `02:236-240`
- **C4 Task completion** handled by the **Post-Completion Actions** section ONLY (frontmatter status/completion_date update, Execution-Log entry); I17 post-completion validation handles output verification; NO "Task Completion and Handoff Protocol" section. `02:242-247`

## 5. SECTION D — Mandatory sections & the "no items before Phase 1" rule

- **D1** Workflow Compliance Declaration `[WORKFLOW-DEPENDENT]`, informational only, no checklist items. `02:255-262`
- **D2** Cross-Stage Integration Requirements `[WORKFLOW-DEPENDENT]`, INFORMATIONAL ONLY; actual read/verify items live in Phase 1 Step 1.4. `02:264-284`
- **D3 CRITICAL RULE** `02:286-289`: NO checklist items before Phase 1. Order = Frontmatter → Workflow Compliance (info) → Prerequisites (info) → Phase 1 (executable). Context-review + prev-stage-input items appear IN Phase 1 Steps 1.2-1.4.

## 6. SECTION E — Checklist structure rules

- **E1 checkbox format** `02:295-309`: every actionable item = `- [ ] Action text`; FLAT (no nested checkboxes); NO parent checkboxes summarizing children; one atomic action per checkbox; `**Step X.Y:**` headers for grouping (not checkboxes); exact completion order; never reference later checkboxes.
- **E2** `02:311-365`: summary/parent checkboxes come AFTER component items; never parent-before-children; indented checklists OK only without a parent checkbox above. Correct = components first, summary last / headers for grouping. Forbidden = parent-before-children, summary-in-middle.
- **E3 sequential order** `02:367-382`: flow always top→bottom; never require marking items above current position; each phase completes ALL its checkboxes before next; FORBIDDEN: "mark complete in section above", "see checklist below", "return to phase and mark complete", any backward movement.
- **E4 formatting** `02:384-405`: never place checkboxes next to step numbers (step numbers = bold headings); NO separate REMINDER blocks between items (workers only see batch items — integrate reminders INTO the item).

## 7. SECTION F — Execution requirements (worker behavior)

- **F1 five-step loop** READ → IDENTIFY (first unchecked `- [ ]`) → EXECUTE (only that item) → UPDATE (mark only that `- [x]`) → REPEAT. `02:411-420`
- **F2 prohibited** `02:422-429`: working from memory; multi-item execution; skipping ahead; **delegating across phase boundaries** (a subagent receives work from a SINGLE checklist item only; must NOT delegate the F1 loop itself); **skipping phase-gate QA** (must spawn lens-based QA M3 after all items in Phase 2+); **skipping post-completion validation** (must run rf-qa structural + rf-qa-qualitative before Done — I17).
- **F2a item-execution discipline** `02:431-447`: one item at a time within a session; **Parallel spawning exception** `02:447` — consecutive items in the SAME phase that spawn INDEPENDENT subagents (no cross-reads) MAY be spawned in parallel via multiple Agent calls in one message; mark each item as its agent completes; does NOT apply to data-dependent items.
- **F5 frontmatter protocol** `02:464-468`: start → status "🟠 Doing" + start_date; completion → "🟢 Done" + completion_date; blocked → "⚪ Blocked" + blocker_reason.

## 8. SECTION I — Additional guidelines (the QA-hardening core: I13-I20)

- **I8/I7 template usage** `02:574-592`: "create a complex task" ALWAYS = read template 02, replace placeholders, write to location.
- **I11 early-status-update** `02:605-607`: status→"🟠 Doing" is the FIRST action; context review after.
- **I12 verification integrated** `02:609-614`: no separate verify items; "ensuring..." clause in each action.
- **I13 POST-COMPLETION ACTIONS (final items only)** `02:616-621`: every task has a Post-Completion Actions section; items for frontmatter update (status, completion_date, updated_date) + Execution-Log entry; I17 validation items precede the frontmatter update; NO separate "Task Completion and Handoff Protocol" section.
- **I15 PHASE-GATE QA ENFORCEMENT** `02:635-651`: every task with 2+ phases MUST have ≥1 phase-gate QA checkpoint between primary execution and dependent phases. **PROHIBITION:** 1-2-agent gates forbidden. FINAL/ASSEMBLED-output gate floor = **6 agents (3 rf-qa structural + 3 rf-qa-qualitative content)**; INTERMEDIATE gate floor = **5 agents (2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative)**. Checkpoint MUST follow **M3 (Lens-Based QA Sequence)**; if consuming source docs, ALSO **M4 (Source Fidelity Gate)**. Full checkpoint = (1) L6 aggregation item, (2) parallel lens-QA spawns ALL with `fix_authorization: false`, (3) findings-consolidation item, (4) ONE fix agent `fix_authorization: true` (I20 serialized), (5) verification round ≥2 agents, (6) conditional PASS→next / FAIL→another cycle (I16 max), (7) M4 fidelity items if applicable. Every QA step MUST be an explicit `- [ ]` item ("No QA lives only in prose" `02:651`). Each spawn item carries agent type, lens, input files, output report path, `fix_authorization: false`, and adversarial framing ("Assume this document has at least N errors focused on your lens. Find them.") `02:649`.
- **I16 verdict + fix cycles** `02:653-673`: binary PASS/FAIL; ANY issue of ANY severity = FAIL; consolidated verdict FAIL if any lens agent found any issue. Max-cycle table: research-gate 3 / synthesis-gate 2 / report-validation 3 / task-integrity 2 / any qualitative 3 / source-fidelity 3. **Serialized fix protocol (I20)** mandatory — parallel fix authorization PROHIBITED; cycle = report(`false`) → consolidate → ONE fix agent(`true`) → verify ≥2 → repeat only on verify-fail.
- **I17 POST-COMPLETION VALIDATION** `02:675-686`: before status=Done, validate (1) all items `[x]`, (2) all output files exist via Glob, (3) blocker entries have resolution notes, (4) if code modified → tests pass, (5) **MANDATORY lens-based QA (M3) on primary output(s)** — in ADDITION to phase-gate QA, verifies FINAL state, min counts per I19, (6) **source-fidelity (M4) when applicable**. These items go in `## Post-Completion Actions` BEFORE the frontmatter-update item; encoded as explicit `- [ ]` per I15.
- **I18 testing for code-modifying tasks** `02:688-697`: if code changes, ≥1 testing item (test command + pass criteria + results-capture path + B2 pattern); use L3 (Test/Execute) pattern.
- **I19 LENS-BASED QA MINIMUM AGENTS** `02:699-727`: FULL-intensity floors (lite/standard reduced per I22). Final/assembled-output size table: <500 lines 3+3=6; 500-1500 4+4=8; 1500-3000 5+5=10; >3000 6+6=12 (BEFORE domain lenses). 4 standard structural lenses (template-conformance, internal-consistency, evidence-quality, completeness) + 4 standard content lenses (actionability, numbers/metrics, cross-reference-chain-integrity, domain-accuracy). Note `02:701`: design-spec numbering offset — template's I19=spec I18, I20=spec I19, I21=spec I20.
- **I19 intermediate-gate table** `02:731-743`: research-gate(P3) 5 = 2 rf-analyst(completeness+cross-validation) + 2 rf-qa(evidence-quality+gap-detection) + 1 rf-qa-qualitative(research-depth); synthesis-gate(P5) 5 = 2 rf-analyst(synthesis-accuracy+source-tracing)+2 rf-qa(structure+content-quality)+1 rf-qa-qualitative(synthesis-coherence); task-integrity(P5.5) 5 = 2 rf-qa(structure+evidence-quality)+2 rf-qa-qualitative(actionability+domain-accuracy)+1 rf-analyst(completeness). Counts are per-lens-per-partition; partitioning applies if research files >6.
- **Adversarial-framing N scale** `02:729`: N=5 (<500 lines), 10 (500-1500), 15 (1500-3000), 20 (>3000). Each lens agent = own prompt, own report file, own focused checklist; "The lens is the agent's ONLY job."
- **I20 SERIALIZED FIX AUTHORIZATION** `02:745-757`: any gate with 3+ agents on same file → serialized. Protocol: (1) report (all parallel, `false`), (2) consolidate → `${TASK_DIR}qa/qa-consolidated-findings.md`, (3) ONE fix agent (`true`) applies ALL, (4) verify ≥2 (1 rf-qa + 1 rf-qa-qualitative, `false`), (5) cycle from consolidation on verify-fail, max per I16, HALT after 3. Why: parallel fixes cause churn/contradictions. Every step = explicit `- [ ]` item.
- **I21 SOURCE-DOCUMENT FIDELITY GATE** `02:759-789`: mandatory when outputs derived from source docs (PRD/TDD/roadmap/tech-reference/README/tech-research/repo-cleanup/"any task where orchestrator reads source docs"). NOT required for pure mechanical transforms / config-only. Checks: semantic coverage, detail preservation, cross-source contradiction, phantom-coverage detection, operational/compliance completeness. Min 2 agents (3-4 if source >1000 lines). Report `${TASK_DIR}qa/qa-source-fidelity-report.md`. Runs AFTER M3.
- **I22 QA INTENSITY LEVELS** `02:793-840`: lite / standard / full scale gate sizes. lite: intermediate 2, final 3, fidelity 1, 1 fix cycle, 1 verifier; standard: intermediate 3, final 7, fidelity 2, 2 cycles, 2 verifiers; full: per I19/I21 tables. Default map Quick/Lightweight→lite, Standard→standard, Deep/Heavyweight→full; user may override ("deep but lite QA"). Serialized fix (I20) applies at ALL levels (never bypassed). lite/standard DISABLE double-QA (skill-specific QA wins over /task auto phase-gate).

## 9. SECTION J / K / L / M — error handling, examples, handoff & composite patterns

- **J error handling** `02:842-864`: blocker embedded in every item ("If unable to complete... log the specific blocker using the templated format in the ### Phase [N] Findings section of the ## Task Log / Notes... then mark this item complete"); items NEVER left unchecked; only mark task "⚪ Blocked" if ALL remaining items blocked by same issue.
- **K example patterns** `02:866-899`: K1 file-by-file, K2 multi-item (orchestrator MUST pre-enumerate ALL items; worker NEVER dynamically adds items). One self-contained item per file, NO separate verification items.
- **SECTION L — INTRA-TASK HANDOFF PATTERNS** `02:901-1026` (this is what makes 02 "complex"). Handoff-file convention `02:909-921`: items write to `.dev/tasks/TASK-NAME/phase-outputs/` subdirs (`discovery/`, `test-results/`, `reviews/`, `plans/`, `reports/`); files persist across batches/rollovers; later items read by path. Use 01 instead if every item is independent.
  - **L1 Discovery** `02:928-938`: explore + write structured machine-readable output; the discovery file IS the deliverable.
  - **L2 Build-from-discovery** `02:940-950`: read discovery file (WHAT) AND source file (CONTENT).
  - **L3 Test/Execute** `02:952-962`: run command; capture BOTH raw output AND structured summary. (I18 testing items use this.)
  - **L4 Review/QA** `02:964-974`: produce structured PASS/FAIL verdict with specific findings; never "looks good".
  - **L5 Conditional-action** `02:976-988`: MUST handle BOTH branches (success AND failure); output file always created.
  - **L6 Aggregation** `02:990-1000`: use Glob to discover files dynamically (don't hardcode); consolidate. Used as the M3 Step-1 aggregation item and typically the final item in a phase.
  - **L7 selection guide + common phase structures** `02:1002-1026`: "Full Lifecycle with QA Gates" = L1 → L2 → **M3 (QA Gate)** → L3 → L5 → L4 → L6 → **M3 (QA Gate)**.
- **SECTION M — PHASE-GATE COMPOSITE PATTERNS** `02:1028-1121`:
  - **M1 (LEGACY single-agent)** `02:1034-1045`: DEPRECATED — spawns only 1-2 agents (below the 6-agent floor); new task files MUST use M3.
  - **M2 applicability** `02:1047-1057`: per task type, where gates are required + min protocol; ALL gates use M3 + I20; every spawn/consolidation/fix/verify = explicit `- [ ]` item.
  - **M3 LENS-BASED QA SEQUENCE (8 steps)** `02:1059-1096`: Step1 L6 aggregation → Step2 structural lens agents (parallel, `false`) → Step3 content lens agents (parallel, `false`) → Step4 domain lenses (parallel, if any) → Step5 consolidation → Step6 ONE fix agent (`true`) → Step7 verification round (≥2, `false`) → Step8 conditional proceed (L5; max cycles per I16; HALT after 3). Report paths `${TASK_DIR}qa/qa-structural-[lens]-report.md`, `qa-content-[lens]-report.md`, `qa-consolidated-findings.md`, `qa-verification-{structural,content}-report.md`. Partitioning is WITHIN a lens (each lens still full-doc coverage). EVERY step = explicit `- [ ]` item; orchestrator MUST NOT collapse steps.
  - **M4 SOURCE-DOCUMENT FIDELITY GATE (6 steps)** `02:1098-1121`: runs AFTER M3. Step1 identify sources (explicit, not dynamic) → Step2 fidelity agents (parallel, ≥2, full output + assigned source range) → Step3 cross-source contradiction agent (reads ALL sources, NOT output) → Step4 consolidation → Step5 ONE fix agent (`true`) → Step6 verification ≥2. Same per-step `- [ ]` encoding rule.

## 10. PART 2 — the actual output template (what the builder writes)

### 10a. Required frontmatter fields `02:1-61`
Builder copies + fills the YAML at the top. Fields: `id` ("TASK-[AGENT]-[TASKTYPE]-YYYYMMDD-HHMMSS"), `title`, `description`, `version`, `status` (enum: 🔵 Backlog | 🟡 To Do | 🟠 Doing | 🔴 Blocked | 🟢 Done | ⚪ Cancelled; default "🟡 To Do"), `type` (16-value enum), `priority` (5-value enum), `created_date`, `updated_date`, `assigned_to`, `autogen`, `autogen_method`, `coordinator`, `parent_doc`, `parent_task`, `depends_on[]`, **`spec_path`** (driving spec/PRD/TDD; populated by task-builder A.2, empty if none `02:23`), **`reflect_pre`** block (PRE reflect-gate sign-off populated by task-builder at A.10.7: `verdict` pass|fail|skipped, `coverage_pct`, `depth` quick|standard|deep, `tcs`, `run_id`, `report`, `reviewed_at` `02:24-31`), **`reflect_post`** (POST reflect verdict, recorded by executor after the final-phase reflect subagent runs `02:32`), `related_docs[]`, `related_prd`, `related_tdd`, `tags[]`, **`template_schema_doc`** `02:47`, `estimation`, `sprint`, `due_date`, `start_date`, `completion_date`, `blocker_reason`, `ai_model`, `model_settings`, `review_info{last_reviewed_by,last_review_date,next_review_date}`, `task_type` (static|dynamic `02:60`).
- NOTE: This worktree's template does NOT carry a literal `start_commit` or `executor_model_class` frontmatter field (the BUILD-REQUEST asked me to confirm — they are absent in `02_mdtm_template_complex_task.md`). Verified by reading `02:1-61` in full.

### 10b. Required body sections (PART 2 order) `02:1157-1441`
1. `# [Task Title]` `02:1157`
2. `## Task Overview` — comprehensive what/why `02:1159-1161`
3. `## Key Objectives` — numbered concrete outcomes `02:1163-1169`
4. `## Prerequisites & Dependencies` — Parent Task & Dependencies + "Previous Stage Outputs (MANDATORY INPUTS)" (INFORMATIONAL ONLY, no checklist items; actual reads in Phase 1 Step 1.4) `02:1171-1191`
5. `## Execution Context` `02:1193-1231` (see §11)
6. `## Detailed Task Instructions` → **Phase 1 Preparation** (Step 1.1 status→Doing, Step 1.2 create handoff dirs), **Phase 2 main execution** (L1/L2/L3 steps), **Phase Gate: Quality Verification (M3)** (Steps PG.1-PG.6), **Phase N Testing**, **Phase 3 Review** (L4/L6) `02:1233-1421`
7. `## Post-Completion Actions` `02:1423-1441` (see §12)
8. `## Task Log / Notes 📋` — Task Summary, Execution Log, per-Phase Findings, Phase Gate Findings, Follow-Up Items, Deviations from Process `02:1443-1516`
- **D3 confirmed in PART 2:** NO checklist items before Phase 1; Phase 1 Step 1.1 is the FIRST `- [ ]` item (status→Doing per I11) `02:1322-1323`.

## 11. `## Execution Context` section shape `02:1193-1231`

Builder-populated (required build step `02:1195`: "Every generated task file MUST have this section populated before the task file is marked ready"). Sub-bullets:
- **### References** — governing docs/specs/workflow files. Format `- [Document Name](path/to/doc.md): [one-line purpose]` `02:1197-1199`.
- **### Source Areas** — codebase dirs/modules/file-sets this task reads/modifies. Format `` - `path/to/area/`: [what it contains / why relevant] `` `02:1201-1203`.
- **### Key Constraints** — top governing constraints: QA intensity, scope limits, known blockers, standing prohibitions `02:1205-1207`.
- **### Handoff File Convention** — names `.dev/tasks/TASK-NAME/phase-outputs/` + the 5 subdirs `02:1209-1221`.
- **### Frontmatter Update Protocol** — the 4 checkpoints (start/completion/blocked/each-session) `02:1223-1231`.
- **CONFIRMED RULE:** Execution Context carries NO specific `file:line` — its References/Source-Areas list documents/dirs at the AREA level (paths + one-line purpose), while per-item Context (B2 field 1) carries the precise `file:line` each checklist item reads. The template comments at `02:1198`/`02:1202` specify area-level formats (`path/to/doc.md`, `path/to/area/`), not line-anchored citations.

## 12. Anti-orphaning rule — Post-Completion ordering `02:1423-1441`

`## Post-Completion Actions` items, IN ORDER (every task-completion item lives INSIDE this final section, never orphaned in an execution phase):
1. Verify all outputs exist via Glob `02:1425`.
2. If code modified, re-run test suite (no regressions) `02:1427`.
3. **POST-COMPLETION LENS-BASED QA (MANDATORY, I17 items 5-6)** — orchestrator expands placeholder into per-agent M3 items (Steps PG.2-PG.5), min 6 agents, all `fix_authorization: false`, consolidate → single fix agent (I20) → verification; reports to `${TASK_DIR}qa/qa-post-completion-*.md` `02:1429-1435`.
4. **POST-COMPLETION SOURCE FIDELITY GATE (MANDATORY if sources consumed, I21)** — M4 per-agent items; reports `${TASK_DIR}qa/qa-post-fidelity-*.md`; if N/A note reason in Task Log `02:1437`.
5. Create `### Task Summary` `02:1439`.
6. **PENULTIMATE→FINAL:** "Update `completion_date`/`updated_date` + status → '🟢 Done'" is the LAST item `02:1441`.
- **Anti-orphaning takeaway:** the Update-status-to-Done item is the terminal item; all QA/reflect/summary completion work precedes it INSIDE Post-Completion Actions. The POST reflect gate item (where a skill wires one) sits immediately before the Update-status-to-Done item — i.e. penultimate. The `reflect_post` frontmatter field (`02:32`) is the slot the executor writes after that final-phase reflect subagent runs. (The bare template does not hardcode a `superclaude reflect run` shell-out item — that wiring is added by the builder/skill, as seen in the example task in §13.)

## 13. Real-world example — `TASK-RF-reflect-post-gate-wiring-20260611-022409`

File: `.dev/tasks/to-do/TASK-RF-reflect-post-gate-wiring-20260611-022409/TASK-RF-reflect-post-gate-wiring-20260611-022409.md` (422 lines, status 🟠 Doing). This is the actual `.md` inside the folder (folder also holds `qa/`, `reflect/`, `research/`, `reviews/`, `research-notes.md`, `.task_id`).

### 13a. Frontmatter as used (vs template) `ex:1-72`
- Uses template fields: `id`, `title`, `description`, `status`, `type` ("🔧 Refactor" — a value NOT in the template's 16-value enum; real tasks extend the enum), `priority`, `created_date`, `updated_date`, `start_date`, `assigned_to`, `template_schema_doc: ".claude/templates/workflow/02_mdtm_template_complex_task.md"` (`ex:12`), `estimation`, `task_type`, `spec_path` (`ex:15`), `start_commit` (`ex:16` — the wrapper O1 base), `executor_model_class: "opus"` (`ex:17` — anti-self-confirmation), `related_docs[]`, `tags[]`.
- **`reflect_pre`** block populated by the PRE gate `ex:30-37`: `verdict: pass`, `coverage_pct: 1.00`, `depth: deep`, `tcs`, `report`, `reviewed_at`.
- **`reflect_post`** block written by the executor/wrapper `ex:20-29` AND a second machine-written block `ex:57-71` (verdict: degraded, status: success, run_id, tier_reached: 2, report, contract, reason: null-convergence, deviations{authorized/necessary/drift/regression}, head, reviewed_at). NOTE: the file has TWO `reflect_post:` keys (hand-annotated `ex:20` + machine `ex:57`) — a real-world artifact of the degraded/manual-record path, not a template-prescribed shape.
- CONFIRMS: `start_commit` + `executor_model_class` are NOT in the bare template frontmatter but ARE present here — they are added by the task-builder when POST_REFLECT_GATE is enabled (this is exactly the wiring this task itself was building).

### 13b. Phase / item structure
- 6 phases: P1 Preparation (branch/baseline/frontmatter-key plan) `ex:107`; P2 O1 wiring `ex:132`; P3 O2 wiring `ex:194`; P4 acceptance-test rewrite `ex:242`; P5 sync+validation `ex:276`; **P6 QA gate, independent reflection, completion** `ex:315`.
- **Per-item format is the 5-field bracketed variant** (not B2's single paragraph): each `- [ ] **N.X — title**` carries indented `**Context**` / `**Action**` / `**Output**` / `**Verification**` / `**Completion gate**` sub-bullets (e.g. items 6.1-6.4). This is a legitimate real-world rendering of B2's six elements as labeled sub-bullets rather than one prose paragraph — useful precedent for builder output.

### 13c. M3 lens-based QA gate encoding (Phase 6) — the I19/I20 pattern in practice
Phase 6 header `ex:317` declares: "Final-document QA gate per MDTM M3 (lens-based, parallel report-only) + I20 (serialized fix authorization) + I19 (≥6 agents: 3 rf-qa structural + 3 rf-qa-qualitative content)".
- **6.1** `ex:319-327`: spawn **3 rf-qa structural lens agents in PARALLEL, report-only** (`fix_authorization: false`, ONE message, `subagent_type: "rf-qa"`, `mode: "bypassPermissions"`). Each agent = named lens + own report path + VERDICT PASS/FAIL: Agent A contract-conformance → `qa/qa-task-contract-conformance.md`; Agent B NFR-7+skip-guard → `qa/qa-task-nfr7-guard.md`; Agent C structural-integrity → `qa/qa-task-structural-integrity.md`. **ADVERSARIAL STANCE** embedded: "assume errors; find ≥5 issues each; a 0-issue verdict needs proof of exhaustive checking" `ex:320`.
- **6.2** `ex:329-337`: spawn **3 rf-qa-qualitative content lens agents in PARALLEL, report-only** (`subagent_type: "rf-qa-qualitative"`): Agent D operational-correctness → `qa/qa-task-operational.md`; Agent E completeness/orphan-reference → `qa/qa-task-completeness.md`; Agent F test-correctness → `qa/qa-task-test-correctness.md`. Same adversarial stance.
- **6.2.1 — serialized fix round (I20)** `ex:339-344`: "Serialized fix authorization — NEVER multiple fix agents at once." Consolidate all 6 reports → `qa/qa-task-consolidated.md`; if any FAIL/finding, spawn ONE rf-qa fix agent (`fix_authorization: true`) with the consolidated list, then re-run grep+named-test. "Max 3 fix-verify cycles (governed by the Retry Monotonicity Protocol: regression → monotonicity → hard-cap → proceed)."

### 13d. POST reflect wrapper shell-out item (the canonical form to emulate)
**6.3 — "Independent post-execution reflection gate (wrapper shell-out)"** `ex:346-353` — sits as the **penultimate item, immediately before 6.4 Update-status-to-Done** (anti-orphaning confirmed in practice):
- Rationale `ex:347`: inline rf-qa ran in THIS executor's frame and cannot do an executor-disjoint audit; the canonical POST gate is a flat `superclaude reflect run` shell-out (wrapper internally launches `/sc:reflect --mode post` as a disjoint `claude --print` subprocess, preventing self-rubber-stamping).
- The exact command `ex:349` (behind the skip guard):
  `if [ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1" ]; then echo "reflect-wrapper recursion breaker: nested gate suppressed"; exit 0; fi; superclaude reflect run <ABS_TASK_FILE> --depth deep --fix --no-promote`
  (`--no-promote` because audited in place; base resolves from frontmatter `start_commit`). Uses `superclaude reflect run`, never `/sc:task`; any re-execution uses `/task`.
- **Exit-code consumption** `ex:350`: only `0` completes the gate; `10`/`11`/`2` → surface the report and HALT.
- **Output** `ex:351`: record `{verdict, run_id, report}` into frontmatter `reflect_post`; deviations → remediate or append to `### Open Questions` (never delete).
- **Completion gate** `ex:353`: wrapper exited 0 AND `reflect_post` recorded → THEN the Update-status item proceeds.
- **6.4 — Update task status to Done** `ex:355-360`: terminal item, sets `status: "🟢 Done"`.
- NOTE on O1 vs O2 emission forms (objectives `ex:86-87`): O1 (whole-tasklist terminal) = `superclaude reflect run <ABS_TASKLIST> --depth deep --fix --promote`; O2 (per-phase) = `superclaude reflect run <ABS_PHASE_FILE> --depth deep --fix --no-promote --base <PHASE_N_START_SHA> --output …`. Item 6.3 above is the O1-shaped gate dogfooded on the task's own file (with `--no-promote` because in-place).

### 13e. Execution Context as used `ex:99-103`
Three sub-bullets, all AREA-level (NO file:line) — confirms §11 rule:
- **References:** GOAL + the authoritative contract + research files 01-04 + qa report (named docs, not line-anchored).
- **Source areas:** the two skill bodies + phase-template + reflect CLI engine (READ-ONLY) + the Layer-A test file (module-level paths).
- **Key constraints:** contract conformance / exact skip-guard marker name / PRE gate intact / edit `src/` then `make sync-dev` / don't touch sibling worktrees or named tests. (Per-item Context sub-bullets carry the precise line anchors, e.g. item 2.1 `ex:138`.)

---

## Summary of builder-conformance rules (the load-bearing set)

1. Copy PART 2 (`02:1157`→EOF) + frontmatter (`02:1-61`); replace placeholders; populate `## Execution Context` (required build step) with References / Source Areas / Key Constraints / Handoff Convention / Frontmatter-Update-Protocol — AREA-level, NO file:line (file:line lives in per-item Context per B2).
2. Every checklist item = self-contained per B2's 6 elements (Context+WHY / Action+WHY / Output / Integrated-"ensuring" Verification / Evidence-on-failure-only / explicit Completion gate); single paragraph OR the bracketed 5-sub-bullet variant the example uses. NO standalone read-context, NO separate verification items, NO parent-before-children, flat checkboxes only (B5/E1/E2).
3. NO checklist items before Phase 1; Phase 1 Step 1.1 = status→"🟠 Doing" (D3/I11).
4. ≥2-phase tasks MUST carry an M3 lens-based phase-gate (I15): ≥6 agents final / ≥5 intermediate (I19), all spawned parallel report-only, then serialized fix (I20: consolidate → ONE fix agent `true` → verify ≥2), conditional proceed with I16 max-cycles. Add M4 fidelity gate if outputs derive from source docs (I21). Scale by I22 qa_intensity. Every QA step = explicit `- [ ]` item (no QA in prose).
5. Post-Completion Actions (final section) ordered: verify-outputs → re-run-tests → post-completion M3 lens QA → M4 fidelity (if applicable) → Task Summary → POST reflect gate (penultimate) → Update-status-to-Done (terminal). The POST reflect item is the flat `superclaude reflect run <ABS_FILE> --depth deep --fix [--promote|--no-promote --base <SHA>]` shell-out behind the `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` skip guard; consume exit code (only 0 proceeds); write `{verdict,run_id,report}` into frontmatter `reflect_post`.
6. Code-modifying tasks add an L3/I18 testing item. Use Section L handoff patterns (write to `phase-outputs/<subdir>/`) for any cross-item data flow — that's what distinguishes template 02 from 01.
