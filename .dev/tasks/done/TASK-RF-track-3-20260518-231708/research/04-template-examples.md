# Research: Template & Examples (Shared across all 3 tracks)

**Status:** Complete
**Scope:** MDTM Template 02 PART 1 + analogous tasks under `.dev/tasks/done/`
**Source of truth:** `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md`
**Audience:** Builders for TRACK 1 (FU-001 sprint-exitcode), TRACK 2 (FU-002 reflexion writer), TRACK 3 (FU-003 PRD-skill CWD)

---

## 1. MDTM Template 02 PART 1 — Key Rules

The full PART 1 instruction block runs from line 46 (`<!--`) to line 894 (`-->`) of the template. The rules below are the distillation each track builder MUST honor. All citations are `file:line` against the template path above.

### A. Granularity and Workflow Integration

| Rule | Citation | Distillation |
|---|---|---|
| **A1** Workflow doc check | template:72-83 | If no governing workflow doc exists in repo, OMIT `[WORKFLOW-DEPENDENT]` sections and derive requirements from user input. For these 3 bug-fix tracks, there is no `.gfdoc/workflows/` doc — so D1 (Workflow Compliance Declaration), D2 (Cross-Stage Integration), A5, A6, A2 sections may be omitted/trimmed. |
| **A3** Complete Granular Breakdown | template:91-95 | Break down EVERY workflow phase into atomic, verifiable checklist items. NO high-level/bulk operations. One checklist item per file, per fix, per assertion. Embed exact file paths + measurable outcomes. |
| **A4** Iterative Process Structure | template:97-116 | For ANY multi-item process: pre-enumerate items in initial step → individual checklist item per specific item → consolidation step only AFTER all items complete. Pattern: `Step X.1 enumerate → Step X.2 per-item rows → Step X.3 consolidate`. |

### B. Self-Contained Checklist Items (CRITICAL — load-bearing rule)

| Rule | Citation | Distillation |
|---|---|---|
| **B1** Session-rollover rationale | template:134-140 | Rigorflow runs tasks in batches across multiple sessions. Context loaded in batch 1 is NOT in batch 3. Every checklist item MUST be self-contained — standalone "read context" items that produce no output are USELESS. |
| **B2** Six required elements | template:142-148 | Every checklist item MUST embed: (1) **Context Reference + WHY** (which file(s) and why), (2) **Action + WHY**, (3) **Output Specification** (exact path/name/template), (4) **Integrated Verification** as `ensuring …` clause (no hallucination, 100% source-derived), (5) **Evidence on Failure Only** (log blocker to Task Notes), (6) **Explicit Completion Gate** ("Once done, mark this item as complete."). |
| **B3** One paragraph format | template:150-154 | Each item is ONE FULL PARAGRAPH (not bullets, not multi-line), verbose and explanatory, executable as an independent prompt. |
| **B4** Worked example | template:155-158 | A 7+ line single-paragraph example showing the 6-element pattern with `component-spec.md` → `BaseHandler.ts` → `ApiHandler.ts`. Mirror this density. |
| **B5** Forbidden patterns | template:164-184 | (1) standalone "read context" items, (2) missing context reference, (3) multi-line/bulleted items, (4) separate verification items, (5) overly granular items like "create directory" alone, (6) REMINDER blocks between items. |
| **B7** Key principles | template:189-196 | Item = complete prompt that executes independently; context embedded IN action item; verification embedded via `ensuring …`; output file IS evidence (no need to log success); only log on failure. |

### C. Embedding requirements (NEVER separate sections)

| Rule | Citation | Distillation |
|---|---|---|
| **C1** Outputs & Deliverables | template:206-211 | Embed output path + content requirements + template-to-follow IN the item that creates the file. Output file itself is success evidence. **DO NOT** create a separate "Outputs & Deliverables" section. |
| **C2** Success Criteria | template:213-217 | Embed as `ensuring …` clauses inside the action item. **DO NOT** create a separate "Success Criteria" section or separate criteria checklist items. |
| **C3** Verification | template:219-223 | Verification MUST be inside each action item as `ensuring …`. **DO NOT** create separate "Verify the file" items. QA process handles inter-batch verification — see I15. |
| **C4** Task Completion | template:225-230 | Task completion = Post-Completion Actions section only. Items: update frontmatter (status, completion_date) + log to Execution Log. Anti-orphaning: post-completion validation (I17) runs BEFORE frontmatter Done update. |

### D. Mandatory sections (D3 is the no-orphan-checklist rule)

| Rule | Citation | Distillation |
|---|---|---|
| **D3** No checklist items before Phase 1 | template:269-272 | Frontmatter → Workflow Compliance (informational, optional) → Prerequisites (informational) → Phase 1 (FIRST checklist items). NO checkboxes may appear before Phase 1 begins. |

### E. Checklist structure rules ("no batch items" + ordering)

| Rule | Citation | Distillation |
|---|---|---|
| **E1** Checkbox format | template:278-292 | Every actionable item is `- [ ]`. NO nested checkboxes. NO parent checkboxes summarizing children. Use `**Step X.Y:**` headers for grouping. Items in EXACT execution order. |
| **E2** Components-first, summary-last | template:294-348 | Summary/parent checkboxes ALWAYS at END of their sequence. NEVER place a parent checkbox BEFORE its child components — that's the "no batch items" rule. |
| **E3** Sequential order | template:350-365 | Top-to-bottom flow only. NO "go back and update", "see below", "return to phase and mark complete". |
| **E4** Step-number formatting | template:367-388 | Step numbers are bold headings WITHOUT checkboxes. Checkboxes go ONLY on actionable items. NO separate REMINDER blocks. |

### F. Execution discipline (one item at a time)

| Rule | Citation | Distillation |
|---|---|---|
| **F1** Five-step loop | template:394-403 | READ → IDENTIFY → EXECUTE → UPDATE → REPEAT. Worker reads task file, finds FIRST unchecked, executes ONLY that, marks ONLY that, returns to READ. |
| **F2** Prohibited | template:405-412 | No multi-item execution, no phase skipping, no skipping phase-gate QA (I15-I16), no skipping post-completion validation (I17). |

### I. Additional rules — phase-gate QA, post-completion validation, testing

| Rule | Citation | Distillation |
|---|---|---|
| **I3** Incremental file modification | template:511-515 | Items add content incrementally. "DO NOT attempt to complete entire files at once." Include save points after major sections. |
| **I11** Early status update | template:569-571 | Status update to "🟠 Doing" MUST be the first action in the task (Step 1.1). Context review comes AFTER status update. |
| **I12** Integrated verification | template:573-578 | No separate "verify the file" items — embed via `ensuring …` clause. Phase-gate (I15-I16) handles inter-batch verification. |
| **I13** Post-Completion Actions | template:580-585 | Every task MUST include a Post-Completion Actions section. Items: update frontmatter (status, completion_date, updated_date), log completion to Execution Log. Post-completion validation (I17) runs BEFORE the frontmatter update item. |
| **I15** Phase-gate QA enforcement | template:599-607 | Every task with 2+ execution phases MUST include at least one phase-gate QA checkpoint between primary execution phase and any subsequent phase that depends on its outputs. Gate = (aggregation item) + (rf-qa spawn item) + (conditional-action item PASS/FAIL). |
| **I16** QA gate verdicts | template:609-624 | Binary PASS/FAIL. Any CRITICAL/IMPORTANT/MINOR issue → FAIL. Fix-cycle caps: research-gate 3, synthesis-gate 2, report-validation 3, task-integrity 2, qualitative 3. After max → HALT or convert unresolved to Open Questions. |
| **I17** Post-completion validation | template:626-635 | BEFORE frontmatter set to Done: verify (1) all `- [ ]` marked `- [x]`, (2) all output files exist (Glob), (3) blockers have resolution notes, (4) if source modified — all relevant tests pass. These items live in Post-Completion Actions BEFORE the frontmatter update item. |
| **I18** Testing for code-modifying tasks | template:637-646 | If task creates/modifies source code (not docs, not config): MUST include at least one testing item with (1) test command, (2) pass criteria, (3) results capture path under `phase-outputs/test-results/`, (4) B2 self-contained pattern. Use L3 (Test/Execute) pattern. **All 3 of our tracks modify source code, so I18 applies to all.** |

### L. Handoff patterns (L1-L6) and pattern selection (L7)

| Pattern | Citation | When to use in our 3 tracks |
|---|---|---|
| **L1** Discovery item | template:737-747 | Scan codebase, write inventory to `phase-outputs/discovery/`. Track 1 may use for "enumerate every `.sprint-exitcode` reference"; Track 3 for "enumerate hook entry points". |
| **L2** Build-from-Discovery | template:749-759 | Read discovery + source, produce deliverable. All 3 tracks: read existing file → produce patched file. |
| **L3** Test/Execute | template:761-771 | `uv run pytest …` capture raw output to `phase-outputs/test-results/` + structured summary. All 3 tracks need this (I18). |
| **L4** Review/QA | template:773-783 | Compare output against source/spec, produce PASS/FAIL with specific findings. Used by rf-qa spawns. |
| **L5** Conditional-action | template:785-797 | IF test PASS → verdict file; IF FAIL → fix-plan file with root-cause analysis. Used at phase-gate. |
| **L6** Aggregation | template:799-809 | Final phase: consolidate review files into one report. Use for "Phase Gate PG-X: aggregate Phase N outputs". |
| **L7** Pattern selection guide | template:811-836 | Common phase structures: `Discovery→Build→Review`, `Build→Test→Fix`, `Full Lifecycle`. For these bug-fix tracks: `Build→Test→Fix` (K1/K2 → L3 → L5) is the natural fit. |

### M. Phase-gate composite patterns

| Pattern | Citation | When to use |
|---|---|---|
| **M1** Phase-gate QA sequence | template:843-850 | 2-3 items between phases: (aggregation L6) + (rf-qa or rf-qa-qualitative spawn) + (conditional proceed L5). Sequential if both structural and qualitative are needed. |
| **M2** Phase-gate applicability | template:852-860 | For **code-modifying tasks** (our case): gate after implementation phase and before testing phase (if separate), or after combined implement+test phase. |

### Single-paragraph anti-patterns to avoid

1. Splitting one item into multiple bullets (template:175-180).
2. Standalone "read context" items (template:165-169).
3. Parent checkbox + child checkboxes (template:327-333).
4. Summary checkbox in middle (template:335-341).
5. Separate verification or REMINDER items (template:181-183, 367-388).

---

## 2. Template 02 mandatory sections

### Frontmatter fields (template:1-44)

Required: `id`, `title`, `description`, `status` (start as 🟡 To Do), `type`, `priority`, `created_date`, `updated_date`, `assigned_to`, `autogen` (false), `autogen_method` (""), `coordinator` (orchestrator), `parent_task`, `depends_on` (list), `related_docs` (list with path + description), `tags`, `template_schema_doc`, `estimation`, `sprint`, `due_date`, `start_date`, `completion_date`, `blocker_reason`, `ai_model`, `model_settings`, `review_info` (last_reviewed_by, last_review_date, next_review_date), `task_type` (static or dynamic).

### Body sections (template:896-1099 = PART 2)

Order is mandatory:

1. **`# [Task Title]`** (template:896)
2. **`## Task Overview`** (template:898) — comprehensive description of what + why
3. **`## Key Objectives`** (template:902) — numbered list of 3+ concrete outcomes
4. **`## Prerequisites & Dependencies`** (template:910)
   - `### Parent Task & Dependencies` (template:912) — parent, blocking dependencies, what this blocks
   - `### Previous Stage Outputs (MANDATORY INPUTS)` (template:919) — informational, lists `[Output Type]: [path]` lines; actual reads happen in Phase 1, Step 1.4. (Omit if no upstream stage for these standalone bug fixes.)
   - `### Handoff File Convention` (template:932) — points to `.dev/tasks/TASK-NAME/phase-outputs/` with the 5 subdirs
   - `### Frontmatter Update Protocol` (template:946) — restates F5
5. **`## Detailed Task Instructions`** (template:956) — contains all phases
   - `### Phase 1: Preparation and Setup` (template:1014) — Step 1.1 status update + Step 1.2 create handoff dirs + (if applicable) Step 1.3 read inputs
   - `### Task-Specific Context Files` (template:1051) — informational, reference only (orchestrator notes — actual reads embedded in Phase 2+ items)
   - `### Phase 2: [Main Execution Phase]` (template:1062) — Step 2.1 discovery (L1), Step 2.2 build (L2), Step 2.3 test (L3), Step 2.4 assess (L5)
   - `### Phase Gate: Quality Verification` (template:1088) — Step PG.1 rf-qa spawn (M1 pattern), inserted between phases that depend on each other
   - `### Phase [N]: Testing & Verification` (template:1096) — for code-modifying tasks per I18
   - `### Phase [Final]: Commit and Open PR` — observed in done/ examples; add this for all 3 of our tracks
6. **`## Post-Completion Actions`** — I17 validation items first (verify all `- [x]`, output files exist, blockers resolved, tests pass), THEN frontmatter Done update + Execution Log entry
7. **`## Task Log / Notes`** — at bottom, contains:
   - `### Execution Log` — timestamped entries
   - `### Phase 1 Findings`, `### Phase 2 Findings`, etc. — one per phase for blocker logging
   - `### Phase Gate Findings` — for QA gate blockers

---

## 3. Analogous task examples from `.dev/tasks/done/`

The five `TASK-RF-track-*-20260517-032112` tasks (the 5-PR CI rot cleanup) are exact-shape matches for the 3 current tracks: each is a small focused bug-fix PR with discovery → execute → verify → commit phases. The examples below were selected to map directly onto the three current tracks.

### Example A — Track-5 (CONTRIBUTING.md + workflow patch)

**Path:** `/config/workspace/IronClaude/.dev/tasks/done/TASK-RF-track-5-20260517-032112/TASK-RF-track-5-20260517-032112.md`

**Title:** "PR5 — Add CONTRIBUTING.md CI Hygiene + Fix pull-sync workflow push target"

**Phase structure (item counts per phase):**

| Phase | Items | Pattern |
|---|---|---|
| Phase 1: Preparation and Setup | 4 | I11 status update + L1 baseline |
| Phase 2: Discovery — Confirm Workflow Bug and PROTECTED-List Staleness | 2 | L1 Discovery |
| Phase 3: Execute — Create CONTRIBUTING.md, Patch Workflow, Audit PROTECTED List | 3 | K1 file-by-file build |
| Phase Gate: Quality Verification of Edits | 1 | M1 phase-gate QA spawn |
| Phase 4: Verify — Workflow Dispatch, Verify-Sync, and Lint/Test Sanity | 4 | L3 Test/Execute |
| Phase 5: Commit + PR | 11 | branch/commit/push/PR sequence |

**Exemplifies (PART 1 rules):**
- **A3 + B2:** every fix is a separate self-contained item (patch workflow line 112, audit PROTECTED list, create CONTRIBUTING.md sections)
- **I15 / M1:** Phase Gate between Execute (Phase 3) and Verify (Phase 4)
- **I17:** Post-Completion Actions has multiple validation items before frontmatter Done
- **I18 + L3:** Phase 4 captures pytest output to `phase-outputs/test-results/`

### Example B — Track-4 (test-fixture repair + xfail isolation)

**Path:** `/config/workspace/IronClaude/.dev/tasks/done/TASK-RF-track-4-20260517-032112/TASK-RF-track-4-20260517-032112.md`

**Title:** "PR4 — Repair tests/audit/ fixtures + xfail genuinely-broken cases"

**Phase structure:**

| Phase | Items | Pattern |
|---|---|---|
| Phase 1: Preparation and Setup | 5 | I11 status update + L1 baseline |
| Phase 2: Discovery — Inventory all tests/audit/ failures | 4 | L1 Discovery with classification table |
| Phase Gate: Discovery Verification | 1 | M1 phase-gate QA |
| Phase 3: Execute — Per-failure fix application | 3 | A4 iterative process (worked example + per-failure fix + umbrella issue) |
| Phase 4: Verify | 3 | L3 Test/Execute (pytest tests/audit/ + regression sweep) |
| Phase Gate: Verify Verification | 1 | M1 phase-gate QA |
| Phase 5: Commit + PR (with AC6 in-line review comment) | 7 | commit/PR + AC6 in-line review |

**Exemplifies (PART 1 rules):**
- **A4 iterative process:** Discovery enumerates failures → Execute fixes one classification at a time → Verify
- **I18 + L3:** explicit `uv run pytest tests/audit/ -v` and regression sweep `uv run pytest -v --ignore=tests/audit`
- **B2 worked-example density:** the fixture-fix description (file:line citations, exact char counts, regex constraint reasoning) is the model of an embedded `ensuring …` clause
- **Two phase gates** (M1 used twice) — once after Discovery, once after Verify

### Example C — Track-1 (mechanical sweep + verify against acceptance criteria)

**Path:** `/config/workspace/IronClaude/.dev/tasks/done/TASK-RF-track-1-20260517-032112/TASK-RF-track-1-20260517-032112.md`

**Title:** "PR1 — ruff auto-fix sweep (F401 unused imports + I001 import order + F841 unused locals)"

**Phase structure:**

| Phase | Items | Pattern |
|---|---|---|
| Phase 1: Preparation and Baseline | 6 | I11 status + L1 baseline capture |
| Phase 2: Execute Auto-Fix | 2 | K2 multi-item (per-rule-class) |
| Phase 3: Verification (FINAL QA Gate — one item per Acceptance Criterion) | 3 | L4 Review per AC + L3 Test |
| Phase 4: Commit and Open PR | 6 | commit/branch/push/PR sequence |

**Exemplifies (PART 1 rules):**
- **Acceptance-Criterion-per-checklist-item** in Phase 3 — direct application of A3 (granular per-AC verification)
- **No middle Phase Gate** — instead Phase 3 IS the FINAL QA Gate (acceptable per I15 since Phase 2→3 is implement→verify in one continuous run)
- **L3 Test/Execute:** captures `ruff check src/ tests/` before/after counts
- **Single PR commit sequence in Phase 4** — useful template for our 3 tracks' final commit phase

### Search verdict for the 3 specific slot patterns requested

| Slot | Best match in done/ | Notes |
|---|---|---|
| New config field / env-var override (Tracks 1 & 2) | **No clean match.** Track-4 (Example B) is the closest analog because env-var-based test isolation in pytest is a "test fixture / env-dependent" pattern, but no done/ task introduces a new sprint-config field or new env-var override directly. Builders for Tracks 1 & 2 should follow Track-4's discovery-then-per-item-fix structure AND the generic Template 02 K1 file-by-file pattern for the config-field addition itself. |
| Test isolation / writer-output redirection (Track 2) | **Example B (Track-4 PR4)** — repairs test fixtures to match scanner reality + uses `@pytest.mark.xfail(strict=True, reason=…)` to isolate genuinely-broken cases. The pattern of "inventory failing tests → fix each → run regression sweep" is the exact shape Track 2 needs for reflexion writer test pollution. |
| PreToolUse hook addition + `_FRESHNESS_SCRIPTS` integration (Track 3) | **Example A (Track-5 PR5)** — patches a workflow YAML file (line 112) and audits a list (PROTECTED) — the structural shape (locate target file → patch with surgical edit → verify-sync → test) maps directly onto Track 3's hook addition. No done/ task touches `_FRESHNESS_SCRIPTS` specifically. |

---

## 4. Per-track applicability

### Track 1 (FU-001 sprint-exitcode migration: executor.py + tmux.py + config.py)

**Mirror:** **Example C (Track-1 PR1)** for overall shape — mechanical migration sweep — combined with **Example A (Track-5 PR5)** for the per-file patch sequence.

**Rationale:** Track 1 is a 3-file migration (config field added + 2 consumer files updated). Example A's "patch workflow file + audit PROTECTED list + verify-sync" sequence (Phase 3 = 3 items) is the cleanest mapping. Each of the 3 files (`config.py` add field, `executor.py` consume field, `tmux.py` consume field) becomes ONE self-contained checklist item under Phase 3, following K1 file-by-file pattern. Then Phase 4 = L3 pytest run + Phase Gate before commit. Use Example C's "AC-per-item" structure for Phase 3 verification.

**Recommended phase skeleton:**
- Phase 1: Preparation (4 items — status, handoff dirs, baseline pytest, read current config.py)
- Phase 2: Discovery — enumerate all `.sprint-exitcode` references and write inventory (1-2 L1 items)
- Phase 3: Execute — one K1 item per file: `config.py` add field, `executor.py` use field, `tmux.py` use field (3 items)
- Phase Gate: rf-qa structural review of patches (1 item, M1)
- Phase 4: Verify — `uv run pytest tests/sprint/ -v`, regression sweep (3-4 L3+L5 items)
- Phase 5: Commit + PR (6-7 items)
- Post-Completion: I17 validations + frontmatter Done

### Track 2 (FU-002 reflexion writer test pollution: reflexion.py + conftest.py + tests/unit/test_reflexion.py)

**Mirror:** **Example B (Track-4 PR4)** — exact shape match for "test isolation / fixture repair".

**Rationale:** Track 2 fixes test pollution caused by reflexion writer writing into the real workspace. The pattern is identical to Track-4 PR4: inventory which tests pollute / fail without isolation → fix each via conftest fixture override OR env-var override in reflexion writer → regression sweep across the rest of the suite. Example B's "discovery classification table → per-failure fix → umbrella issue → AC3 verify + NFR2 regression sweep" maps directly. Use Example B's TWO phase gates (one after Discovery, one after Verify) — test-isolation work benefits from QA validation that the fix doesn't break other tests.

**Recommended phase skeleton:**
- Phase 1: Preparation (4-5 items)
- Phase 2: Discovery — `uv run pytest tests/unit/test_reflexion.py -v` to inventory pollution, classify each (writer-output / env-leak / fixture-missing), produce classification table (3-4 L1 items)
- Phase Gate: Discovery Verification (1 item, M1)
- Phase 3: Execute — per-fix item: reflexion.py add env-var override, conftest.py add isolation fixture, test_reflexion.py update assertions (3 items K1)
- Phase 4: Verify — `uv run pytest tests/unit/test_reflexion.py -v` + regression sweep `uv run pytest -v --ignore=tests/unit/test_reflexion.py` (2-3 L3 items)
- Phase Gate: Verify Verification (1 item, M1)
- Phase 5: Commit + PR (6-7 items)
- Post-Completion: I17 validations + frontmatter Done

### Track 3 (FU-003 PRD-skill CWD-default output routing: tests/cli/prd/test_prompts.py + SKILL.md + hooks)

**Mirror:** **Example A (Track-5 PR5)** — workflow file patch + PROTECTED list audit is structurally identical to "hook entry add + `_FRESHNESS_SCRIPTS` registration + SKILL.md update + test add".

**Rationale:** Track 3 has 3 surfaces (test file + SKILL.md + hook script + `_FRESHNESS_SCRIPTS` registration in `.claude/settings.json`). Example A's Phase 3 = 3 items (create CONTRIBUTING.md, patch workflow, audit PROTECTED list) is the same shape. Use Example A's verify-sync sanity check (Phase 4) to catch hook-registration mistakes — Track 3 must run `make verify-sync` since it touches `.claude/` AND `src/superclaude/`.

**Recommended phase skeleton:**
- Phase 1: Preparation (4 items)
- Phase 2: Discovery — locate current hook entries + `_FRESHNESS_SCRIPTS` registrations + SKILL.md CWD references (2 L1 items)
- Phase 3: Execute — one K1 item per file: hook script add, settings.json register, SKILL.md update, test_prompts.py update (4 items)
- Phase Gate: rf-qa structural review (1 item, M1) — critical because hook changes have high blast radius
- Phase 4: Verify — `make verify-sync`, `uv run pytest tests/cli/prd/ -v`, regression sweep (3-4 L3+L5 items)
- Phase 5: Commit + PR (7-8 items, including `make sync-dev` step)
- Post-Completion: I17 validations + frontmatter Done

---

## 5. Quick-reference checklist for each builder

When writing each track's task file, verify before marking research complete:

- [ ] Status update is Step 1.1 (I11)
- [ ] Handoff dirs created in Step 1.2 (D from template)
- [ ] NO checkboxes appear before `### Phase 1` (D3)
- [ ] Every `- [ ]` item is ONE paragraph (B3)
- [ ] Every `- [ ]` item embeds all 6 B2 elements
- [ ] No parent/summary checkboxes precede their components (E2)
- [ ] At least one phase-gate QA item between Execute and Verify (I15)
- [ ] At least one pytest item under Phase 4 (I18 + L3)
- [ ] Post-Completion Actions has I17 validation items BEFORE the frontmatter Done update
- [ ] `## Task Log / Notes` at bottom has `### Execution Log` + `### Phase N Findings` per phase + `### Phase Gate Findings`
- [ ] No separate "Verification" or "Success Criteria" or "Outputs" sections (C1-C4)

---

## Sources

All citations against `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md`:

- A1-A6: lines 72-128
- B1-B7: lines 134-196
- C1-C4: lines 206-230
- D1-D3: lines 238-272
- E1-E4: lines 278-388
- F1-F5: lines 394-451
- I1-I18: lines 499-646
- J1-J3: lines 656-673
- K1-K2: lines 682-708
- L1-L7: lines 737-836
- M1-M2: lines 843-860
- PART 2 (template body): lines 896-1099+

Done/ task examples:

- Example A: `/config/workspace/IronClaude/.dev/tasks/done/TASK-RF-track-5-20260517-032112/TASK-RF-track-5-20260517-032112.md`
- Example B: `/config/workspace/IronClaude/.dev/tasks/done/TASK-RF-track-4-20260517-032112/TASK-RF-track-4-20260517-032112.md`
- Example C: `/config/workspace/IronClaude/.dev/tasks/done/TASK-RF-track-1-20260517-032112/TASK-RF-track-1-20260517-032112.md`
- Supplementary (also done/ track tasks, similar shape): Track-2 PR2 (format sweep) and Track-3 PR3 (manual renames) — same 5-PR release
