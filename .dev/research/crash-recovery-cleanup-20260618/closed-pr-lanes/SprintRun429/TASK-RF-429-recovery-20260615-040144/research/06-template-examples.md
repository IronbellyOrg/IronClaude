# Research: Template & Examples
**Status:** Complete
**Date:** 2026-06-15
---

## 0. CORRECT TEMPLATE PATH (skill default is wrong for this worktree)

- **Authoritative template file:** `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` (120,364 bytes).
- **`.claude/templates/workflow/` DOES NOT EXIST in this worktree** — `ls .claude/templates/workflow/` returns non-zero (Exit code 2). The task-builder skill's documented default path (`.claude/templates/workflow/02_...`) is **WRONG for this worktree**. The builder MUST read from `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md`.
- Sibling templates present: `01_mdtm_template_generic_task.md`, `05_prd_template.md`, `99_mdtm_template_generic_task_old.md`, etc.
- Note: Template C1 example at line 226 itself references `.claude/templates/workflow/api-template.md` as an embed-path *illustration* inside the template body, NOT the location of THIS template.

## 1. FRONTMATTER (PART 2 header, lines 1-61)

The live YAML frontmatter the output file uses spans **lines 1-61**, in order:

| Field | Line | Notes / value shape |
|---|---|---|
| `id` | 2 | `"TASK-[AGENT]-[TASKTYPE]-YYYYMMDD-HHMMSS"` |
| `title` | 3 | action-oriented |
| `description` | 4 | what + purpose within larger workflow |
| `version` | 5 | `""` |
| `status` | 7 | enum (line 6 comment): `🔵 Backlog`/`🟡 To Do`/`🟠 Doing`/`🔴 Blocked`/`🟢 Done`/`⚪ Cancelled`; default `"🟡 To Do"` |
| `type` | 9 | enum (line 8) incl `✨ Feature`,`🐛 BugFix`,`🛠️ Tooling/Automation`,`🔬 Research/Spike`,etc. |
| `priority` | 11 | enum (line 10): `🔥 Highest`/`🔼 High`/`▶️ Medium`/`🔽 Low`/`🧊 Lowest` |
| `created_date` | 12 | `"YYYY-MM-DD"` |
| `updated_date` | 13 | `"YYYY-MM-DD"` |
| `assigned_to` | 14 | `"[agent-name]"` |
| `autogen` | 15 | `false` |
| `autogen_method` | 16 | `""` |
| `coordinator` | 17 | `orchestrator` |
| `parent_doc` | 18 | `""` |
| `parent_task` | 19 | `"[PARENT-TASK-ID]"` |
| `depends_on` | 20-22 | list |
| `spec_path` | 23 | driving spec/PRD/TDD path; populated by builder at **A.2**, empty if none |
| `reflect_pre` | 24-31 | PRE reflect-gate sign-off block: `verdict`("" / pass / fail / skipped), `coverage_pct`, `depth`(quick/standard/deep), `tcs`, `run_id`, `report`, `reviewed_at`; populated by builder at **A.10.7** |
| `reflect_post` | 32 | `""` POST reflect verdict; recorded by executor after final-phase reflect subagent runs |
| `related_docs` | 33-39 | list of `{path, description}` |
| `related_prd` | 40 | `""` |
| `related_tdd` | 41 | `""` |
| `tags` | 42-46 | list |
| `template_schema_doc` | 47 | `""` |
| `estimation` | 48 | `""` |
| `sprint` | 49 | `""` |
| `due_date` | 50 | `""` |
| `start_date` | 51 | `""` |
| `completion_date` | 52 | `""` |
| `blocker_reason` | 53 | `""` |
| `ai_model` | 54 | `""` |
| `model_settings` | 55 | `""` |
| `review_info` | 56-59 | `{last_reviewed_by, last_review_date, next_review_date}` |
| `task_type` | 60 | `static` |

NOTE for builder: of the R6-prompt's requested frontmatter list, `task_type` IS present (line 60); `start_commit` and `executor_model_class` are **NOT in the lines 1-61 frontmatter block**. Marked **Unverified** whether they are builder-injected elsewhere — pending Section I scan below.

## 2. PART 1 — SECTION A (Core Principles, lines 85-145)

- **A1** (89): workflow-doc availability check — if no governing workflow docs, OMIT all `[WORKFLOW-DEPENDENT]` sections, derive from user requirements.
- **A2** (102) [WORKFLOW-DEPENDENT]: deep-integrate governing workflow doc; map every element.
- **A3 COMPLETE GRANULAR BREAKDOWN** (108): break EVERY phase into atomic verifiable checklist items; individual item for EVERY file/component/iteration; NO bulk operations; exact paths + measurable outcomes.
- **A4 ITERATIVE PROCESS STRUCTURE** (114): for any multi-item process — pre-enumerate ALL items in an initial step, one item per item, incremental updates after each, consolidation step only after all complete. Pattern (120-133): `Step X.1` scan/enumerate → `Step X.2` process each individually → `Step X.3` consolidate.
- **A5** (135) [WORKFLOW-DEPENDENT]: cross-stage integration — every phase specifies prior-stage inputs w/ exact paths.
- **A6** (141) [WORKFLOW-DEPENDENT]: workflow compliance enforcement.

## 3. PART 1 — SECTION B (Self-Contained Items, lines 147-213) — CRITICAL

- **B1** (151): session-rollover protection — context from batch 1 is GONE by batch 3+. Standalone "read context" items are USELESS.
- **B2** (159): EVERY item is a complete self-contained prompt with **6 elements**:
  1. Context Reference with WHY (files + why)
  2. Action with WHY
  3. Output Specification (exact file name, location, content, template)
  4. Integrated Verification — an "ensuring…" clause (no fabrication; 100% source-derived; document negative evidence on failure)
  5. Evidence on Failure Only (log to task notes ONLY on blocker/error; success evidenced by output file)
  6. Explicit Completion Gate — literal: *"This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete."*
- **B3** (167): each item = ONE FULL PARAGRAPH, verbose, standalone-prompt style.
- **B5** (181-201): FORBIDDEN — standalone read-context items; missing context reference; multi-line/bulleted items; separate verification items; over-granular ("create directory" alone); separate REMINDER blocks.
- **B7** (206): output files = evidence; only log on FAIL/BLOCK; QA handles verification between batches (I15-I16).

## 4. PART 1 — SECTIONS C, D, E (Embedding / Mandatory Sections / Checklist Rules)

- **C1-C4** (216-247): outputs, success criteria, verification, completion are EMBEDDED in items — NEVER separate sections. C4: completion handled by Post-Completion Actions (frontmatter update status+completion_date, log to Execution Log); I17 handles output verification; do NOT create a "Task Completion and Handoff Protocol" section.
- **D1/D2** (255-284) [WORKFLOW-DEPENDENT]: informational-only Workflow Compliance + Cross-Stage Integration blocks (NO checklist items).
- **D3 CRITICAL RULE** (286): NO checklist items before Phase 1. Order: Frontmatter → Workflow Compliance (info) → Prerequisites (info) → Phase 1 (executable). Context-review + prior-stage-input items live IN Phase 1 Steps 1.2-1.4.
- **E1-E4** (295-401): flat checkboxes only, NO nested/parent checkboxes; `**Step X.Y:**` bold headers for grouping; strict top-to-bottom order; summary checkboxes AFTER components; no backward-movement; no REMINDER blocks between items.

## 5. PART 1 — SECTION I (key rules) + SECTION M (QA composite patterns)

### M3 — Lens-Based QA Sequence (template lines 1059-1096)
MANDATORY replacement for legacy M1. 8 steps, each an explicit `- [ ]` item (no collapsing, line 1096):
1. **Aggregation** (L6) — collect prior-phase outputs into a summary (Glob-discovered) at `${TASK_DIR}phase-outputs/reports/...`.
2. **Structural lens agents (PARALLEL)** — `rf-qa`, one per structural lens, `fix_authorization: false`, report to `${TASK_DIR}qa/qa-structural-[lens]-report.md`, adversarial framing.
3. **Content lens agents (PARALLEL)** — `rf-qa-qualitative`, one per content lens, `fix_authorization: false`, `qa-content-[lens]-report.md`. (Steps 2-3 may share one parallel batch, line 1080.)
4. **Domain-specific lens agents (PARALLEL, if any)**.
5. **Findings consolidation** → `${TASK_DIR}qa/qa-consolidated-findings.md` (deduped, severity + originating lens).
6. **Fix agent** — ONE `rf-qa`, `fix_authorization: true`, applies ALL fixes.
7. **Verification round (PARALLEL)** — min 2 (1 rf-qa + 1 rf-qa-qualitative), `fix_authorization: false`.
8. **Conditional proceed** (L5) — both PASS → proceed; else repeat Steps 5-7 to max cycles (I16), then HALT+escalate.

### M4 — Source Fidelity Gate (lines 1098-1121)
Runs AFTER M3 (line 788, 1099). Verifies output faithfully represents source docs (different from internal-consistency QA which reads only the output). 6 steps (source-id → fidelity agents PARALLEL min 2 / 3-4 if sources >1000 lines → cross-source contradiction agent → consolidate → fix agent → verification). Every step an explicit `- [ ]` item.

### Section I rules cited by R6 prompt
- **I15** (635) PHASE-GATE QA ENFORCEMENT: every task w/ 2+ phases needs ≥1 phase-gate checkpoint following M3 (+M4 if source-consuming). 1-2 agent gates PROHIBITED — FINAL/assembled gate floor = **6 agents** (3 rf-qa structural + 3 rf-qa-qualitative content); INTERMEDIATE gate floor = **5 agents** (2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative). Every step encoded as `- [ ]`.
- **I16** (653) verdict + fix cycles: binary PASS/FAIL; ANY issue of ANY severity = FAIL. Consolidated FAIL if any agent reports any issue. Max cycle table: research/report-validation/qualitative/source-fidelity=3 (HALT+escalate); synthesis/task-integrity=2 (Open Questions).
- **I17** (675) POST-COMPLETION VALIDATION: before status→Done, verify (1) all items `[x]`, (2) all output files exist (Glob), (3) blockers have resolution notes, (4) code-modifying → tests pass, (5) **MANDATORY lens-based QA per M3 on final output**, (6) **fidelity gate per M4 when source-consuming**. These items live in `## Post-Completion Actions` BEFORE the frontmatter-update item, encoded as explicit `- [ ]` (line 684).
- **I18** (688) testing for code-modifying tasks: ≥1 testing item (L3 pattern) w/ command, pass criteria, results path.
- **I19** (699) LENS-BASED QA MINIMUM AGENTS (full intensity). Final/assembled QA scaling table: `<500 lines`=3+3=6; `500-1500`=4+4=8; `1500-3000`=5+5=10; `>3000`=6+6=12 (before domain lenses). Standard 4 structural lenses (template-conformance, internal-consistency, evidence-quality, completeness) + 4 content lenses (actionability, numbers-metrics, crossref-chain, domain-accuracy). Adversarial-framing N scales 5/10/15/20 by size. Intermediate-gate table (research/synthesis/task-integrity = 5 agents each w/ specified types).
- **I20** (745) SERIALIZED FIX AUTHORIZATION: any gate with 3+ agents on same file → serialized. Protocol: report (all parallel, fix_authz:false) → consolidate → ONE fix agent (fix_authz:true) → verify (≥2). Parallel fix authorization PROHIBITED (line 746).
- **I21** (759) SOURCE-DOCUMENT FIDELITY GATE REQUIREMENT: mandatory for PRD/TDD/roadmap/tech-ref/tech-research/repo-cleanup/etc. (any task reading source docs to produce output). NOT required for pure mechanical transforms / config-only. ≥2 fidelity agents (3-4 if sources >1000 lines). Runs AFTER M3.
- **I22** (793) QA INTENSITY LEVELS: `lite` (Quick/Lightweight, <300 lines: intermediate 2, final 3, fidelity 1, 1 fix cycle, 1 verify), `standard` (300-1500 lines: intermediate 3, final 7, fidelity 2, 2 cycles, 2 verify), `full` (Deep/Heavyweight >1500 lines: per I19/I20/I21 in full). Serialized fix (I20) applies at ALL levels.

**Builder mapping note for R6 prompt's "M3 lens-based QA sequence / M4 source-fidelity gate / I19/I20/I21/I22":** the 429-recovery task is a **code-modifying task** (sprint/pipeline recovery logic + tests), NOT a source-document-derived doc. Per I21 (line 773-775) the M4 fidelity gate is **NOT required** unless code is derived from a spec doc; the M3 lens-based gate IS required (min 6 agents per I15/I19, or scaled by I22 intensity). The builder should select intensity per the task tier and include the I18 testing item (L3) since source code is modified.

## 6. PART 2 — EXACT SECTION SKELETON (lines 1157-1516)

Copy from `# [Task Title]` (line 1157) to EOF. Section order:

1. `# [Task Title]` (1157)
2. `## Task Overview` (1159) — comprehensive description + why.
3. `## Key Objectives` (1163) — numbered bold objectives, each a concrete outcome.
4. `## Prerequisites & Dependencies` (1171) — `### Parent Task & Dependencies` (1173) + `### Previous Stage Outputs (MANDATORY INPUTS)` (1180, INFORMATIONAL ONLY — no checklist items).
5. `## Execution Context` (1193) — builder MUST populate (line 1195): `### References` (1197), `### Source Areas` (1201), `### Key Constraints` (1205), `### Handoff File Convention` (1209, phase-outputs subdirs), `### Frontmatter Update Protocol` (1223).
6. `## Detailed Task Instructions` (1233) — wraps an orchestrator instruction block (removed from output) then the phases:
   - `### Phase 1: Preparation and Setup` (1291): Step 1.1 update status→Doing (1323), Step 1.2 create phase-outputs dirs (1326).
   - `### Phase 2: [Main Execution Phase Name]` (1339): Steps 2.1 Discovery(L1) / 2.2 Build(L2) / 2.3 Test(L3) / 2.4 Assess(L5).
   - `### Phase Gate: Quality Verification (M3 Lens-Based QA)` (1365): Steps PG.1-PG.6 (aggregate, structural lenses, content lenses, consolidate+fix, verify, fidelity gate).
   - `### Phase [N]: Testing & Verification` (1404): L3 testing items (I18) — remove if docs/config-only.
   - `### Phase 3: [Review and Quality Assessment]` (1412): Steps 3.1 Review(L4) / 3.2 Aggregate(L6).
7. `## Post-Completion Actions` (1423) — see §7 below (this is the FINAL PHASE's completion block).
8. `## Task Log / Notes 📋` (1443): `### Task Summary` (1445, templated), `### Execution Log` (1467), `### Phase N - [Name] Findings` (1477+), `### Phase Gate Findings` (1498), `### Follow-Up Items Identified` (1502), `### Deviations from Process` (1508).

## 7. `## Post-Completion Actions` — final-phase completion items (lines 1423-1441)

In order (these are the canonical completion items):
1. (1425) Verify all outputs exist via Glob; log gaps to Follow-Up Items.
2. (1427) If code modified, run test suite (or note "Tests verified in Phase [N]").
3. (1435) **POST-COMPLETION LENS-BASED QA placeholder** — orchestrator MUST expand into per-agent items (M3 Steps PG.2-PG.5), min 6 agents per I19, reports to `${TASK_DIR}qa/qa-post-completion-*.md`.
4. (1437) **POST-COMPLETION SOURCE FIDELITY GATE placeholder** — expand per M4 if I21-applicable; else note "Fidelity gate not applicable — [reason]".
5. (1439) Create `### Task Summary` (templated).
6. (1441) Update `completion_date`/`updated_date` + status→`🟢 Done`, log to Execution Log. **This is the LAST item.**

## 8. QUOTED — template's own self-contained item-format examples

**B4 CORRECT EXAMPLE (template lines 173-175, verbatim):**
> `- [ ] Read the file `component-spec.md` at `docs/specs/component-spec.md` to extract the API interface requirements including all method signatures, parameter types, and return values that must be implemented, then read the file `BaseHandler.ts` at `src/handlers/BaseHandler.ts` to understand the structural patterns and conventions used in existing handlers, then create the file `ApiHandler.ts` at `src/handlers/ApiHandler.ts` containing a TypeScript class that implements all methods defined in the component spec with proper error handling, type annotations, and JSDoc comments following the patterns from BaseHandler, ensuring the file includes the standard header comment block, exports the class as the default export, all methods from the spec are implemented with correct signatures, no content is fabricated or assumed beyond what the source explicitly states, and no placeholder or TODO comments remain. If unable to complete due to missing information, file access issues, or unclear requirements, log the specific blocker using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.`

**PART 2 L1-Discovery example (template line 1280, verbatim):**
> `- [ ] Use Glob to find all TypeScript files matching `src/handlers/**/*.ts` and for each file found use Read to extract the class name, exported methods (name, parameters, return type), and any JSDoc descriptions, then write a consolidated inventory to the file `handler-inventory.md` at `.dev/tasks/TASK-NAME/phase-outputs/discovery/handler-inventory.md` formatted as a markdown table with columns: File Path, Class Name, Method Name, Parameters, Return Type, Description (one row per method), ensuring every .ts file in `src/handlers/` is included with accurate method signatures extracted directly from the source code with no fabrication, and the inventory file includes a summary count at the top showing total files and total methods found. If unable to complete due to missing directories or file access issues, log the specific blocker using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.`

These show the required shape: single paragraph; Context(read X at path, WHY) → Action(then create Y) → Output(exact path+format) → "ensuring…" verification clause → "If unable to complete… log… then mark this item complete." → completion gate sentence.

## 9. POST REFLECT GATE ITEM — NOT in the template; injected by the task-builder SKILL

**CRITICAL for builder:** The POST reflect gate item is **NOT present in `02_mdtm_template_complex_task.md`** (grep for `reflect run` / `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` / `--promote` in the template returns ZERO hits). Only the frontmatter `reflect_post: ""` room-comment field (line 32) and the QA placeholders exist. The POST reflect item is emitted by **`src/superclaude/skills/task-builder/SKILL.md`** (O1 directive) when `POST_REFLECT_GATE: ENABLED`.

### Canonical emission (task-builder SKILL.md)
- **SKILL line 1075-1078:** O1 emits the FLAT wrapper shell-out `superclaude reflect run ${TASK_FILE} --depth deep --fix --promote` behind the `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` skip guard. `--depth` is fixed `deep`; the wrapper resolves the audit base from frontmatter `start_commit` and the reviewer-exclusion class from `executor_model_class`. (`--spec` flows to PRE only.)
- **SKILL line 1726:** POST = penultimate final-phase item `N.{X-1}` — flat wrapper shell-out behind the recursion-breaker skip guard.
- **SKILL line 2202 (canonical one-liner):** stage the diff (`git add -A`), then emit a single Bash command: first the §3.2 skip guard `if [ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1" ]; then echo "reflect-wrapper recursion breaker: nested gate suppressed"; exit 0; fi`, then `superclaude reflect run {TASK_FILE} --depth deep --fix --promote`. NO `--base` (wrapper resolves audit base from frontmatter `start_commit` as a SINGLE ref vs working tree, so uncommitted task edits ARE audited). `--depth deep` fixed (Tier-2 fan-out); `--fix` bounded auto-fix loop; `--promote` lets the `task` adapter move the dir to `done/` on clean/auto-fixed PASS. Emit NO `--reflect`, NO `--max-turns`, NO `<base>..HEAD` range, NO agent-spawn directive (flat shell-out, NFR-7-clean). Consume EXIT CODE: only `0` completes the gate; `10` (halted), `11` (degraded), `2` (blocked) all FAIL → surface report + HALT before status→Done. Uses `superclaude reflect run` (never `/sc:task`); re-execution uses `/task`.
- **SKILL line 2319 (rule 20) + 2260 (validation):** when `POST_REFLECT_GATE: ENABLED`, POST item MUST be penultimate (immediately before Update-status-to-Done, preserving anti-orphaning), the FLAT wrapper form. MALFORMED if omitted, or if it emits the legacy `/sc:reflect --mode post` self-run subagent form or a human-handoff/HALT form. Must NOT hand-author `reflect_post` (wrapper writes it back).

### Frontmatter keys the O1 wrapper depends on (builder-injected; NOT in template base block lines 1-61)
- **`start_commit`** (SKILL line 2152, 2165): `git merge-base HEAD <integration-branch>` captured at build time; the O1 wrapper's audit base when `--base` omitted. Resolve `<integration-branch>` from `git symbolic-ref --short refs/remotes/origin/HEAD`, falling back to `origin/master`/`origin/main`. Base precedence: `--base` > `start_commit` > `git merge-base HEAD master`.
- **`executor_model_class`** (SKILL line 2153, 2165): executor model-class alias (e.g. `sonnet`), passed to reflect as `--executor-model` to exclude the executor from the reviewer panel (anti-self-confirmation).
- **`reflect_post:`** (template line 32; SKILL 2154/2165): left as a room comment; the wrapper writes it back at execution time — never hand-author or lock.

**RESOLUTION of §1 Unverified:** `start_commit` and `executor_model_class` ARE required frontmatter fields for POST-reflect-enabled tasks, but they are **injected by the task-builder SKILL (O1 / contract §6), not present in template 02's base frontmatter block (lines 1-61).** The builder MUST add them. `task_type` IS in the template (line 60).

### Real prior-task example (verbatim shape)
`.dev/tasks/to-do/TASK-RF-reflect-marker-leak-20260611-175724/...md` Step 4.14 (the penultimate item) renders the guarded wrapper inline:
> `…use the Bash tool from <worktree-root> to run the standard guarded wrapper shell-out `if [ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1" ]; then echo "DEVIATION: dogfood deferred — nested-gate suppression, not proof"; exit 0; else superclaude reflect run <ABS_TASK_FILE> --depth deep --fix --no-promote; fi 2>&1`…`

(NOTE: that specific dogfood task used `--no-promote` because it was the wrapper-dev branch testing itself; the **canonical builder emission is `--depth deep --fix --promote`** per SKILL 1075/2202/2319.) Step 4.15 is the final status→Done item — confirming **anti-orphaning**: the POST item and the completion item both sit inside the final phase (here Phase 4), POST penultimate, Done last.

## 10. ANTI-ORPHANING RULE

- Completion items (POST reflect penultimate + status→Done last) MUST live **inside the final phase**, never as free-floating items after the last `### Phase` header's other content. The template encodes this via `## Post-Completion Actions` as the terminal block of `## Detailed Task Instructions` (template 1423-1441), and the task-builder enforces "POST reflect penultimate, immediately before Update-status-to-Done, preserving anti-orphaning" (SKILL 2260/2319).
- The real example confirms the pattern: Phase 4 ends with Step 4.13 (summary) → Step 4.14 (POST reflect, penultimate) → Step 4.15 (status→Done, last). No completion item floats outside a phase.

---

## SUMMARY

- **Correct template path** (worktree): `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md`. `.claude/templates/workflow/` does NOT exist here — the skill's default path is wrong for this worktree.
- **PART 1** rules documented with IDs + line numbers: A3/A4 (granular breakdown, iterative process), B2 (6-element self-contained item) / B3 / B5, C1-C4 (embed, no separate sections), D3 (no items before Phase 1), E1-E4 (flat checkboxes), I15/I16/I17/I18/I19/I20/I21/I22 (phase-gate QA enforcement, verdict/cycles, post-completion validation, testing, lens minimums, serialized fix, fidelity-gate applicability, intensity levels), M3 (8-step lens-based QA sequence) and M4 (6-step source-fidelity gate).
- **Frontmatter** base block (template lines 1-61) fully tabulated; `task_type` present; `start_commit` + `executor_model_class` are **builder-injected by the task-builder SKILL** (O1/contract §6), required for POST-reflect-enabled tasks.
- **PART 2 skeleton** fully mapped (Overview → Key Objectives → Prerequisites → Execution Context → Phases → Post-Completion Actions → Task Log) with line anchors.
- **POST reflect gate item** is NOT in template 02 — it's the task-builder SKILL's O1 emission: penultimate final-phase FLAT wrapper shell-out `superclaude reflect run {TASK_FILE} --depth deep --fix --promote` behind the `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` skip guard, consuming exit code (only 0 proceeds), with `start_commit`/`executor_model_class`/`reflect_post` frontmatter wiring. Canonical one-liner at SKILL.md:2202; malformed-output rules at SKILL.md:2260/2319.
- **Anti-orphaning**: POST penultimate + status→Done last, both inside the final phase; encoded via `## Post-Completion Actions`.
- Template's own item-format examples quoted verbatim (B4 line 173; L1 line 1280).
