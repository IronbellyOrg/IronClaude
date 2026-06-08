# Research: MDTM template 02 + example tasklists

Status: In Progress
Date: 2026-06-04
Researcher: R6 (Template & Examples)

---

## AREA 1 — MDTM Template 02 (Complex) PART 1 + PART 2

**Source of truth:** `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` (1204 lines).

**SYNC NOTE (important for the builder):** the synced copy at `.claude/templates/workflow/02_mdtm_template_complex_task.md` **does NOT exist as a physical file in this worktree** — `make sync-dev` syncs only `.claude/{skills,agents,commands}`, not `templates/`. The task-builder SKILL.md nonetheless references the read path `.claude/templates/workflow/02_mdtm_template_complex_task.md` (SKILL.md:567-568, 1029-1030, 1568-1569) and writes `template_schema_doc: ".claude/templates/workflow/0[1|2]_mdtm_template_[generic|complex]_task.md"` into frontmatter (SKILL.md:1876). **For building this task, read the template from `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md`** (canonical), but the generated file's `template_schema_doc` frontmatter value should match what the skill emits (`.claude/templates/workflow/02_mdtm_template_complex_task.md`).

### 1.1 Required frontmatter fields (lines 1-44)

Exact keys + values from the template head:

```yaml
---
id: "TASK-[AGENT]-[TASKTYPE]-YYYYMMDD-HHMMSS"
title: "[Clear, Action-Oriented Task Title]"
description: "[Detailed description...]"
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
- path: "[path/to/process.md]"
  description: "Process document governing this task"
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

**Allowed/expected values (from template + F5/I11 protocol):**

- `status` lifecycle emoji values: `🟡 To Do` (initial) → `🟠 Doing` (F5/I11: first action) → `🟢 Done` (completion) → `⚪ Blocked` (if blocked). (lines 5, 947-949, 1044-1046)
- `type` emoji value in this template head is `📝 Documentation`. This is a doc/markdown-editing build, so `📝 Documentation` is correct for THIS task (the protocol-file edits are markdown). Other MDTM `type` emoji values used across examples: `🐞 Bug`, `🌟 Feature`, `🛠️ Refactor`, `🧪 Test` (see example frontmatter below).
- `priority` emoji: `🔼 High` (also `🔽 Low`, `▶️ Medium` seen elsewhere).
- `task_type`: `static` (fixed content; the default — use this) or `dynamic` (only if the worker must add checklist items during execution; see I6 lines 526-536). THIS build is `static`.
- `coordinator: orchestrator` is a literal default.

### 1.2 Required PART 2 sections (the actual task-file body, lines 890-1204)

Order is fixed:

1. `# [Task Title]`
2. `## Task Overview` — comprehensive description (line 892)
3. `## Key Objectives` — numbered bold objectives (line 896)
4. `## Prerequisites & Dependencies` (line 904) with sub-sections:
   - `### Parent Task & Dependencies`
   - `### Previous Stage Outputs (MANDATORY INPUTS)` — INFORMATIONAL ONLY, no checkboxes (line 914-926)
   - `### Handoff File Convention` — declares `.dev/tasks/TASK-NAME/phase-outputs/` + the 5 subdirs (line 928-941)
   - `### Frontmatter Update Protocol` (line 943-952)
5. `## Detailed Task Instructions` (line 954) — contains the **Phases**:
   - `### Phase 1: Preparation and Setup` — Step 1.1 status update (mandatory first), Step 1.2 create phase-outputs dirs (lines 1012-1050)
   - `### Phase 2: [Main Execution Phase Name]` — the L-pattern execution items (lines 1063+)
   - `### Phase Gate: Quality Verification` — QA gate items (optional, lines 1090-1096)
   - `### Phase [N]: Testing & Verification` — L3 test items if code-modifying (lines 1098-1104)
   - `### Phase 3: [Review and Quality Assessment]` — L4 review + L6 aggregate (lines 1106-1116)
6. `## Post-Completion Actions` (line 1118) — 4 items (see I17/I13 below)
7. `## Task Log / Notes 📋` (line 1128) — `### Task Summary`, `### Execution Log`, `### Phase N Findings`, `### Phase Gate Findings`, `### Follow-Up Items`, `### Deviations from Process`

**D3 CRITICAL RULE (line 269-272):** "NO CHECKLIST ITEMS may appear before Phase 1 begins." Frontmatter → Prerequisites (informational) → Phase 1 (first executable items). Previous-stage/context reading happens IN Phase 1, not in standalone items.

### 1.3 Rule A3 — COMPLETE GRANULAR BREAKDOWN (lines 91-96, verbatim)

```
A3. COMPLETE GRANULAR BREAKDOWN
   - Break down EVERY workflow phase into atomic, verifiable checklist items
   - Create individual checklist items for EVERY file, component, or iteration
   - NO high-level or bulk operations allowed - everything must be granular
   - Include exact file paths, specific requirements, and measurable outcomes
```

For THIS build: each of the two SKILL.md files, the command file, and templates gets its own item — do NOT batch "edit both SKILL files" into one item.

### 1.4 Rule A4 — ITERATIVE PROCESS STRUCTURE (lines 97-116, verbatim pattern)

```
A4. ITERATIVE PROCESS STRUCTURE
   - For ANY process involving multiple items (files, components, etc.):
     * Pre-enumerate ALL items to be processed in initial step
     * Create individual checklist item for each specific item
     * Require incremental updates after each item
     * Include consolidation step only after all items complete
   - Use this pattern:
     **Step X.1:** Scan and enumerate all [items] in [location]
     - [ ] Complete [item] listing generated: [count] items identified
     **Step X.2:** Process each [item] individually:
     - [ ] [Item 1]: [exact identifier] - [specific action] completed
     - [ ] [Item 2]: [exact identifier] - [specific action] completed
     **Step X.3:** Consolidate all individual results
     - [ ] All [count] items processed and results logged
```

### 1.5 Rule B2 — SELF-CONTAINED ITEM (the 6-element pattern, lines 142-149 verbatim)

```
B2. EVERY CHECKLIST ITEM MUST BE A COMPLETE, SELF-CONTAINED PROMPT THAT INCLUDES:
   1. Context Reference with WHY - What file(s) to read and why
   2. Action with WHY - What to do with that context and why
   3. Output Specification - exact output file name, location, content, template
   4. Integrated Verification - an "ensuring..." clause (DO NOT assume/hallucinate;
      100% accuracy from source; document negative evidence on failure)
   5. Evidence on Failure Only - log to task notes ONLY if blocked
   6. Explicit Completion Gate - "This item cannot be marked as done until the
      actions are completed in their entirety exactly as described. Once done,
      mark this item as complete."
```

B3 (line 150-153): each item is **ONE FULL PARAGRAPH** (not bullets/multi-line), verbose, readable as a standalone prompt.
B5 FORBIDDEN (lines 164-184): standalone "read context" items; missing context ref; multi-line/bulleted items; separate verification/confirmation items; overly-granular ("create directory" alone); separate REMINDER blocks.
J1 error-handling clause (lines 659-663, embed verbatim in EVERY item): "If unable to complete due to missing information, file access issues, or unclear requirements, log the specific blocker using the templated format in the ### Phase [N] Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete."

### 1.6 Section L — handoff patterns for subagent-spawning / multi-item flow (lines 711-836)

Handoff file convention (line 718-730): items write to `.dev/tasks/TASK-NAME/phase-outputs/{discovery,test-results,reviews,plans,reports}/`; files persist across batches/session-rollovers.

| Pattern | Use | Output dir |
|---|---|---|
| **L1 Discovery** | explore codebase/data, write structured findings | `discovery/` |
| **L2 Build-from-Discovery** | create output from discovery file + source | (real output path) |
| **L3 Test/Execute** | run command/test, capture raw + summary | `test-results/` |
| **L4 Review/QA** | assess output vs source, PASS/FAIL verdict | `reviews/` |
| **L5 Conditional-Action** | branch on prior result (MUST handle both branches) | `plans/` |
| **L6 Aggregation** | Glob + consolidate multiple outputs | `reports/` |

**M1 PHASE-GATE QA SEQUENCE (lines 843-851):** 2-3 items at a phase boundary — (1) L6 aggregation, (2) rf-qa spawn (+ rf-qa-qualitative in a SEPARATE following item if doc-type), (3) L5 conditional proceed/fix-cycle. I16 fix-cycle caps (lines 609-624): qualitative gate = 3 cycles then HALT+escalate; task-integrity = 2 then Open Questions.

**F2 (line 410):** subagents receive work from a SINGLE checklist item only; no delegating across phase boundaries; no delegating the F1 loop. F2 parallel-spawning exception (line 430): consecutive SAME-phase INDEPENDENT subagent items may be spawned in parallel.

### 1.7 Anti-orphaning rule — completion items inside the final phase

The literal string "anti-orphan" does not appear; the rule is expressed via **D3 + E1-E3 + C4/I13 + I17 + the PART 2 ordering**:

- **E1/E2/E3 (lines 278-365):** "Summary/parent checkboxes MUST come AFTER all their component items"; "Work flows TOP to BOTTOM only"; "Each phase must complete ALL its checkboxes before moving to next phase"; FORBIDDEN: any checklist structure requiring backward movement, "see checklist below", "return to phase and mark complete."
- **C4 / I13 (lines 225-230, 580-585):** Task completion (frontmatter status→Done, completion_date, Execution Log entry, Task Summary) lives ONLY in the `## Post-Completion Actions` section — the **final** section before the Task Log. Do NOT create a separate "Task Completion and Handoff Protocol" section.
- **I17 POST-COMPLETION VALIDATION (lines 626-635, verbatim intent):** before frontmatter→Done, the task MUST include validation items verifying: (1) all `- [ ]` marked `- [x]`, (2) all output files exist on disk (Glob), (3) blocker entries have resolution notes, (4) if source code modified, tests pass. These appear in `## Post-Completion Actions` BEFORE the frontmatter-update item.

So "completion items inside the final phase" = the 4 Post-Completion Actions items (lines 1120-1126), in order: (a) Glob-verify outputs exist, (b) run tests if code-modifying, (c) write Task Summary, (d) update frontmatter→🟢 Done + Execution Log entry. The Done-flip is the **very last** checkbox in the file.

---

## AREA 2 — Real example tasklists (structure mining)

Three real generated TASK-RF files studied. All three are MDTM Template 02; their frontmatter `template_schema_doc` points at `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` (the **src** path, not `.claude/` — see 135209:29).

### 2.1 `TASK-RF-20260602-135209` — THE GOLD-STANDARD for THIS build (proposal cites it)

663 lines, **81 checkbox items**, `type: 📝 Documentation`, `assigned_to: rf-task-executor`, `autogen_method: task-builder`. It edits `src/superclaude/skills/sc-reflect-protocol/SKILL.md` + 4 refs/, runs `make sync-dev`/`make verify-sync`, and scaffolds eval cases — **the same edit→sync→verify shape THIS build needs.**

**Phase structure + per-phase item counts:**

| Phase | Items | Role |
|---|---|---|
| Phase 1: Preparation, Setup, OQ Precondition Probes | 7 | status flip, mkdir phase-outputs, OQ probes |
| Phase 2: FR-7+FR-6 (one FR-pair) | 11 | edit items → sync (2.7) → verify-sync+markdownlint (2.8) → eval scaffold |
| Phase Gate PG-2 | 1 | rf-qa task-integrity gate |
| Phase 3: FR-1+FR-2 + contract bump | 17 | (largest edit phase) |
| Phase Gate PG-3 | 1 | rf-qa |
| Phases 4-7 (one FR each) + PG-4..PG-7 | 9/8/5/11 + 1 each | edit→sync→verify→eval, each gated |
| Phase 8: Final Verification | 3 | L6 aggregate (8.1) → rf-qa structural (8.2) → rf-qa-qualitative (8.3) |
| Post-Completion Actions | 4 | Glob-verify → tests/verify-sync confirm → Task Summary → Done flip |

**Effective patterns to copy (structure, NOT content):**

1. **Per-edit-phase "edit → sync → verify" triplet.** Each edit phase ends with: a `make sync-dev` item (135209 Step 2.7) that captures output to `phase-outputs/test-results/phaseN-sync-dev.txt` and embeds the "`.claude/` mirror MUST NEVER be staged (gitignored sync-dev output)" rule; then a `make verify-sync` + `npx markdownlint-cli <edited files>` item (Step 2.8) that writes a `phaseN-verify.md` summary recording verify-sync PASS/FAIL + exit code + markdownlint clean/violations, and mandates fixing any lint violation in `src/...` then re-running sync-dev before the gate.
2. **Per-phase rf-qa gate (M1).** Each Phase Gate is ONE self-contained item that spawns `rf-qa` in `QA_MODE: task-integrity` with `fix_authorization: true` and the **byte-exact adversarial stance** string (135209:210): `ADVERSARIAL STANCE: Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.` The item names the inputs, the verdict report path (`phase-outputs/reviews/pgN-...-qa.md`), and the fix-cycle policy: "up to two task-integrity fix cycles applying the retry ordering regression → monotonicity → hard-cap → proceed" with byte-exact halt strings, then "No later phase may begin unless this gate's verdict is PASS."
3. **Final-verification pair (Phase 8).** L6 aggregate of all `pg*-qa.md` reviews + `phase*-verify.md` → final rf-qa structural → final rf-qa-qualitative (structural-first, qualitative-after-PASS). Both adversarial + fix_authorization; structural=2 cycles, qualitative=3 then HALT+escalate.
4. **Verification items carry CONCRETE commands** embedded in the item paragraph: `make sync-dev`, `make verify-sync`, `npx --yes markdownlint-cli <files> 2>&1`, JSON-validity `uv run python -c "import json; json.load(...)"`. Tests/lint write raw output (`*.txt`) + structured summary (`*.md`) per L3.
5. **Per-file / per-delta-site granularity (A3).** Each edit is its own item naming the exact file, the anchor substring, the exact before→after text, and an "ensuring..." clause that pins what must NOT change (e.g. "the serena cluster stays contiguous, no existing tool token is removed").
6. **Post-Completion item #2 (tests) gracefully degrades for doc-only tasks** (135209:496): since it edits protocol markdown not Python, the item states "there are no pytest unit tests... Confirm instead that `make verify-sync` reported PASS... and markdownlint reported clean." THIS build DOES touch the audit/sprint test suites (per R4), so for THIS build that item should actually run `uv run pytest tests/audit/ tests/sprint/...`.
7. **Done-flip is explicitly LAST** (135209:500): "ensuring this is the LAST item completed (all validation items above must be done first)."

**TB-Add-2 bounds check:** 81 items is OVER the single-track ≤50 bound. TB-Add-2 (task-builder SKILL.md:1167, 1973) reads: *"Item count bounds — track ≥3 and ≤40 items; single-track ≥3 and ≤50. ADVISORY-fail until empirical calibration completes."* It is **ADVISORY-fail (not blocking) until calibration** (≥10 completed tasks across ≥3 task_types in `.dev/tasks/done/`), so 135209 over-shot the bound under advisory status. THIS build should AIM for ≤50.

### 2.2 `TASK-RF-20260603-031100` — the lighter doc/refactor pattern (RECOMMENDED model for sizing)

363 lines, **25 checkbox items**, 6 phases. A corrective remediation (4 findings F-1/F-2/G-1/G-2) editing `SKILL.md` + `refs/report-template.md` + eval fixtures. **Respects TB-Add-2 (25 ≤ 50).** This is the better sizing model for THIS build.

**Phase shape (per-finding phase):**

- Phase 1: Preparation (2 items — status flip 1.1, mkdir phase-outputs 1.2). No `discovery/` subdir created (031100:140 omits it — only test-results/reviews/plans/reports — because no L1 discovery items). THIS build SHOULD include `discovery/` since R1-R5 already did the anchor discovery, OR an explicit Phase-2 anchor-reverify item.
- Phases 2-5 (one finding each): edit src item(s) → reconcile dependent eval fixtures → ONE consolidated `sync-dev && verify-sync && markdownlint && JSON-validity` item (031100 Step 2.3 — note it folds sync+verify+lint+json into a single L3 item, tighter than 135209's two items) → rf-qa task-integrity gate (max 2 cycles).
- Phase 6: Final Validation — ONE whole-change validation sweep item (Step 6.1: verify-sync, all-rule markdownlint vs pre-edit `cp` baseline, JSON-validity, corrected-form `grep -c ...==0` guards, `git diff --cached --name-only | grep -c '^\.claude/'` MUST=0) → rf-qa structural gate (Step 6.2, max 3, HALT+Blocked on exhaust) → rf-qa-qualitative gate (Step 6.3, max 3, HALT) → Post-Completion closure (Step 6.4 Glob-verify + Task Summary + Done-flip folded into Phase 6, NOT a separate `## Post-Completion Actions` section).

**Two structural choices 031100 made that THIS build should weigh:**

- It folded Post-Completion INTO Phase 6 (Steps 6.4 a/b/c) rather than a separate `## Post-Completion Actions` heading. 135209 used the separate heading. The template (PART 2) prescribes the separate `## Post-Completion Actions` heading — **prefer 135209's separate-section form** for template fidelity.
- It put a `cp src/.../SKILL.md /tmp/skill-preedit-fN.md` markdownlint-baseline item FIRST inside each edit step (031100:150) because HEAD is not a valid pre-edit baseline (parent task uncommitted). **THIS build will likely have the same uncommitted-parent issue** (it edits committed src under a dirty worktree) — the builder should consider a pre-edit `cp` baseline if markdownlint-delta-must-be-0 enforcement is wanted, or simpler: just require "0 NEW markdownlint violations" judged against the file's own prior state.

### 2.3 `TASK-RF-20260603-024610` — code-modifying multi-stage (Python source)

649 lines, **75 items**, edits Python (sprint CLI). Phases mirror roadmap Stages 0-3, each with a `### Phase Gate: Stage N Quality Verification`. Has a `### Phase RC: Roadmap-Completion Items` inserted AFTER Phase 5 for post-reflect remediation (024610:421-446), added "after the `/sc:reflect --mode pre` coverage audit found 4 §3 roadmap actions MISSING" (024610:423). Demonstrates: (a) testing items use real `uv run pytest tests/sprint/...` commands (code-modifying ⇒ I18 testing phase required); (b) reflect can drive task structure (the PRE audit added Phase RC). Over the ≤50 bound (advisory).

### 2.4 Reflect-item finding across all three examples (KEY for Area 3)

**NONE of the three examples carries a `/sc:reflect --mode post` final-phase item.** They terminate with inline `rf-qa` structural + `rf-qa-qualitative` gates, then Post-Completion closure. `/sc:reflect --mode pre` appears only as a *build-time* audit that shaped 024610's Phase RC (not as an item inside the generated tasklist). This empirically confirms the **dogfooding gap** the proposal closes: today's task-builder does NOT template a fresh-session POST reflect item. THIS build's generated tasklist should be the FIRST to carry one (per proposal §6.2 / lines 196-227).

---

## AREA 3 — Dogfooding the POST reflect gate in THIS build's own tasklist

The proposal being implemented (`/sc:proposals/reflect-in-task-builder.md`) ADDS a templated POST reflect gate to task-builder. Since this build's own tasklist is produced by task-builder, it should itself carry that gate — proving the feature on its own output.

### 3.1 The proposal's templated POST item (reflect-in-task-builder.md:204-227, verbatim)

The proposal prescribes (Critical-Rule companion #16/#17/#18, line 202): *"the builder MUST emit, as the **penultimate item of the final phase** (immediately before the `Update task status to Done` item, preserving anti-orphaning per the validation checklist), a fresh-session reflect handoff item. The item MUST NOT run reflect inline; it writes a `reflect_post: PENDING` sentinel and HALTs until the operator records the verdict."*

The exact templated command (line 216): `/sc:reflect --mode post --remediate --diff <BASE>..HEAD --tasklist {TASK_FILE} [--spec {SPEC_PATH}] --depth {DEPTH} --executor-model {EXECUTOR_CLASS}`.

**CAVEAT for the builder — paragraph-collapse.** The proposal's item shape (lines 207-226) is written as a **multi-line bulleted block** (Context / Action / Output / Verification / Completion gate). MDTM Template 02 **B3/B5 FORBID multi-line/bulleted checklist items** — every item must be ONE paragraph. So the builder must **collapse** the proposal's 5 bullets into a single self-contained B2 paragraph (Context+WHY → Action+WHY → Output spec → "ensuring..." → completion gate), NOT copy the bulleted block verbatim.

### 3.2 Sketch of the POST reflect item for THIS task (single-paragraph, B2-compliant)

Grounded values for THIS build (Deep tier, single track, edits `src/superclaude/`):

- `--diff <BASE>..HEAD` → `<BASE>` = the commit at task start (frontmatter `start_commit`, or `git merge-base HEAD master` if unset). This build IS the `src/superclaude/` edit, so the diff range is the natural UC-2 input (input-resolution.md rule 2 — reflect self-resolves).
- `--spec` → the **two proposal files**: `.dev/proposals/reflect-in-task-builder.md` and `.dev/proposals/reflect-in-sc-tasklist.md` (these are the driving specs; UC-2 deviation audit checks adherence to them). Note `--spec` is single-valued in reflect's surface; if only one can be passed, pass `reflect-in-task-builder.md` (the larger/self-referential one) and cite the second in the item prose, OR pass the directory if reflect accepts it — **R5 owns the reflect-flag arity; defer the single-vs-multi `--spec` resolution to R5's findings.**
- `--depth standard` (floored at `standard` per proposal O4 — POST never runs `--depth quick`; Deep tier ⇒ `standard` or `deep`).
- `--tasklist {THIS_TASK_FILE}` and `--executor-model {EXECUTOR_CLASS}` (literal placeholder the operator fills with the model that ran `/task`).
- Run with `/task` for the surrounding tasklist, `/sc:reflect` for the gate — **NEVER `/sc:task`** (honors `feedback-no-sctask-on-task-builder-tasklists`).

**Recommended single-paragraph item text (builder adapts):**

> `- [ ]` All implementation, sync, test, and inline rf-qa items above are complete; because those gates ran in THIS executor's biased frame and cannot perform an executor-disjoint audit (per project memory `feedback_sc_reflect_vs_inline_rfqa`), perform an **independent fresh-session** post-execution reflection by writing `reflect_post: PENDING` to this file's frontmatter and then STOPPING to surface — for the operator to run in a NEW Claude session — the paste-ready command `/sc:reflect --mode post --remediate --diff <BASE>..HEAD --tasklist .dev/tasks/to-do/TASK-RF-20260604-042055/TASK-RF-20260604-042055.md --spec .dev/proposals/reflect-in-task-builder.md --depth standard --executor-model {EXECUTOR_CLASS}` (where `<BASE>` = frontmatter `start_commit` or `git merge-base HEAD master`, and the second driving spec `.dev/proposals/reflect-in-sc-tasklist.md` is named in this item for the operator to add if reflect's `--spec` accepts multiple), ensuring reflect is NOT run inline in this session, the command names `/sc:reflect` for the gate (never `/sc:task`), and the item does NOT self-resolve. **This item cannot be marked done until the operator has run `/sc:reflect --mode post` in a fresh session and recorded its verdict (`reflect_post: {verdict, run_id, report}`) in frontmatter — only THEN may the final `Update status to 🟢 Done` item proceed (HALT per `feedback_human_decision_items_must_halt`).** Once done, mark this item as complete.

### 3.3 Placement (grounded in anti-orphaning / I17)

Per the proposal (line 202) AND the template's I17 + E1-E3 ordering: this POST reflect item is the **penultimate** checkbox — it sits in `## Post-Completion Actions` **after** the Glob-verify-outputs item, the run-tests item, and the Task Summary item, but **immediately before** the final `Update status to 🟢 Done + Execution Log` item. Because it HALTs (does not self-resolve), the Done-flip item's completion is gated on the operator's recorded verdict — this is exactly the "completion items inside the final phase / Done-flip is LAST" anti-orphaning discipline (Area 1.7). Frontmatter must also gain a `reflect_post:` field (and a `reflect_pre:` + `spec_path:` per the proposal Output-Structure delta) — initialize `reflect_post: PENDING` is written by the item at runtime, not at build time; at build time frontmatter may carry `reflect_post: ""` / `spec_path: ".dev/proposals/reflect-in-task-builder.md"`.

---

## STATUS: COMPLETE

### Recommended task-file skeleton for THIS build (phase list + rough item counts)

Targets: `src/superclaude/skills/task-builder/SKILL.md` (proposal 1), `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` + `src/superclaude/commands/tasklist.md` + tasklist templates (proposal 2), shared `make sync-dev`. Deep tier, single track, `type: 📝 Documentation`, `task_type: static`. **Model: 031100's lighter per-phase shape, scaled to stay ≤50 items (TB-Add-2 single-track bound).**

| Phase | Step focus | ~Items |
|---|---|---|
| **Phase 1: Preparation & Setup** | 1.1 status→🟠 Doing + Execution Log; 1.2 mkdir `phase-outputs/{discovery,test-results,reviews,plans,reports}`; 1.3 capture `start_commit` + record baseline test state (`uv run pytest tests/audit tests/sprint` GREEN-or-note per R4); optional 1.4 re-verify R1-R3 line anchors against current files (anchors WILL have drifted per research-notes:46) | 3-4 |
| **Phase 2: Proposal 1 edits — task-builder SKILL.md** | one item per delta-site: `--spec` flag/input surface, A.2 spec_path resolution, A.10.7 PRE gate step, POST_REFLECT_GATE rule + Output-Structure frontmatter, depth→complexity mapping, S4 token-set TRIM; then sync-dev item; then verify-sync + markdownlint item | 8-11 |
| **Phase Gate PG-2** | rf-qa task-integrity (adversarial + fix_authorization, max 2) | 1 |
| **Phase 3: Proposal 2 edits — sc-tasklist SKILL.md + commands/tasklist.md + templates** | one item per delta-site (per-file granularity across the 4 files), incl. `--no-reflect` flag landing + checkpoint-is-last amendment; then sync-dev item; then verify-sync + markdownlint item | 7-10 |
| **Phase Gate PG-3** | rf-qa task-integrity (max 2) | 1 |
| **Phase 4: Testing & Verification (I18 — touches audit/sprint suites)** | run `uv run pytest tests/audit/ tests/sprint/...` (exact must-pass set per R4) capturing raw+summary (L3); L5 conditional fix-or-proceed on FAIL | 2-3 |
| **Phase 5: Final Validation** | 5.1 L6 aggregate all pg*-qa + verify summaries + test summary → `reports/final-consolidation.md`; 5.2 rf-qa structural whole-change (adversarial, max 3, HALT+Blocked); 5.3 rf-qa-qualitative whole-change (adversarial, max 3, HALT) | 3 |
| **Post-Completion Actions** | (a) Glob-verify all outputs exist; (b) confirm `uv run pytest tests/audit tests/sprint` PASS + verify-sync PASS + markdownlint clean + no `.claude/` staged; (c) write `### Task Summary`; **(d) POST reflect gate — penultimate, fresh-session `/sc:reflect --mode post` HALT item per Area 3.2**; (e) Update status→🟢 Done + Execution Log (LAST) | 5 |

**Total ≈ 33-41 items** — within the single-track ≤50 TB-Add-2 bound, above the ≥3 floor. Plus the standard `## Task Log / Notes 📋` scaffold (`### Task Summary`, `### Execution Log`, `### Phase N Findings` ×5, `### Phase Gate Findings`, `### Follow-Up Items`, `### Open Questions`, `### Deviations from Process`).

**Frontmatter for THIS build:** `type: "📝 Documentation"`, `priority: "🔼 High"`, `task_type: static`, `assigned_to: "rf-task-executor"`, `autogen_method: "task-builder"`, `parent_task: "ReflectInTaskList"`, `coordinator: orchestrator`, `template_schema_doc:` = `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` (match 135209:29 — src path) OR `.claude/templates/...` (match what task-builder emits, SKILL.md:1876) — **prefer the src path per the working example 135209**; add proposal-mandated `spec_path: ".dev/proposals/reflect-in-task-builder.md"`, `reflect_pre: ""`, `reflect_post: ""`; `related_docs` = the two proposal files + the two SKILL.md targets + `research/`.
