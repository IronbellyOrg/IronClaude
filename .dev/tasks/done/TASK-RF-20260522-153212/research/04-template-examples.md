# Research 04 — Template & Examples (Phase-Structure Patterns)

**Task:** TASK-RF-20260522-153212 (cliEval remediation builder research)
**Scope:** `.claude/templates/workflow/02_mdtm_template_complex_task.md` PART 1 + four `TASK-RF-20260518-cliEval-P*` task files
**Goal:** Extract proven phase-structure patterns so the builder mirrors prior cliEval idiom.

---

## SECTION A — Template 02 PART 1 Rules (cited by line)

### Frontmatter fields (lines 1-44)

Required frontmatter keys (template lines 2-43):

| Field | Required example | Line |
|---|---|---|
| `id` | `TASK-[AGENT]-[TASKTYPE]-YYYYMMDD-HHMMSS` | 2 |
| `title` | action-oriented | 3 |
| `description` | detailed | 4 |
| `status` | `🟡 To Do` (start) | 5 |
| `type` | `📝 Documentation` etc | 6 |
| `priority` | `🔼 High` etc | 7 |
| `created_date` / `updated_date` | YYYY-MM-DD | 8-9 |
| `assigned_to` | agent-name | 10 |
| `autogen` / `autogen_method` | false / "" | 11-12 |
| `coordinator` | `orchestrator` | 13 |
| `parent_task` | parent id or "" | 14 |
| `depends_on` | list | 15-17 |
| `related_docs` | list of `{path, description}` | 18-24 |
| `tags` | list | 25-29 |
| `template_schema_doc` | "" | 30 |
| `estimation` / `sprint` / `due_date` / `start_date` / `completion_date` / `blocker_reason` | "" | 31-36 |
| `ai_model` / `model_settings` | "" | 37-38 |
| `review_info.{last_reviewed_by,last_review_date,next_review_date}` | "" | 39-42 |
| `task_type` | `static` (default) / `dynamic` | 43 |

### A3 — COMPLETE GRANULAR BREAKDOWN (lines 91-95, verbatim)

> A3. COMPLETE GRANULAR BREAKDOWN
>
> - Break down EVERY workflow phase into atomic, verifiable checklist items
> - Create individual checklist items for EVERY file, component, or iteration
> - NO high-level or bulk operations allowed - everything must be granular
> - Include exact file paths, specific requirements, and measurable outcomes

### A4 — ITERATIVE PROCESS STRUCTURE (lines 97-116, verbatim)

> A4. ITERATIVE PROCESS STRUCTURE
>
> - For ANY process involving multiple items (files, components, etc.):
>   - Pre-enumerate ALL items to be processed in initial step
>   - Create individual checklist item for each specific item
>   - Require incremental updates after each item
>   - Include consolidation step only after all items complete
> - Use this pattern:
>
>      ```markdown
>      **Step X.1:** Scan and enumerate all [items] in [location]
>      - [ ] Complete [item] listing generated: [count] items identified
>
>      **Step X.2:** Process each [item] individually:
>      - [ ] [Item 1]: [exact identifier] - [specific action] completed
>      - [ ] [Item 2]: [exact identifier] - [specific action] completed
>      [Continue for each item]
>
>      **Step X.3:** Consolidate all individual results
>      - [ ] All [count] items processed and results logged
>      - [ ] Consolidated output created per requirements
>      ```

### B2 — Self-contained item pattern (lines 142-148, verbatim 6 elements)

Every checklist item MUST be a complete, self-contained prompt that includes:

1. **Context Reference with WHY** — file(s) to read and why
2. **Action with WHY** — what to do with that context
3. **Output Specification** — exact file name, location, content, template
4. **Integrated Verification** — `ensuring…` clause (no hallucination, source-derived only)
5. **Evidence on Failure Only** — log to task notes only on blocker
6. **Explicit Completion Gate** — "This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete."

Format rule (B3, line 150-153): ONE FULL PARAGRAPH per item, verbose, explanatory, complete prompt.

### L1-L6 Handoff Patterns (lines 737-810)

- **L1 Discovery** (lines 737-747) — explore codebase/data and write structured findings to `phase-outputs/discovery/`.
- **L2 Build-from-Discovery** (lines 749-759) — read discovery file + source file, produce deliverable.
- **L3 Test/Execute** (lines 761-771) — run command, capture raw output + structured summary to `phase-outputs/test-results/`.
- **L4 Review/QA** (lines 773-783) — assess output against source; PASS/FAIL verdict to `phase-outputs/reviews/`.
- **L5 Conditional-Action** (lines 785-797) — branch on previous result; MUST handle both branches.
- **L6 Aggregation** (lines 799-809) — Glob discovered files, consolidate into report at `phase-outputs/reports/`.

L7 Pattern Selection Guide (lines 811-835) — common phase structures:

- **Build → Test → Fix:** K1/K2 (build) → L3 (run tests) → L5 (conditional: fix or proceed)
- **Full Lifecycle with QA Gates:** L1 → L2 → **M1 (QA Gate)** → L3 → L5 → L4 → L6 → **M1 (QA Gate)**

### M1 Phase-Gate QA Sequence (lines 843-850)

3 items between phases:

1. Aggregation (L6) — collect outputs
2. QA Agent Spawn — rf-qa or rf-qa-qualitative with phase type, inputs, report path, verdict handling, error clause
3. Conditional Proceed (L5) — PASS → next phase; FAIL → fix cycle per I16

### Mandatory Sections (PART 2 template, lines 890-1196)

| Section | Line(s) | Required |
|---|---|---|
| `# [Task Title]` | 890 | Yes |
| `## Task Overview` | 892 | Yes |
| `## Key Objectives` | 896 | Yes (numbered list) |
| `## Prerequisites & Dependencies` | 904 | Yes |
| `### Parent Task & Dependencies` | 906 | Yes (in Prerequisites) |
| `### Previous Stage Outputs (MANDATORY INPUTS)` | 914 | Yes (informational) |
| `### Handoff File Convention` | 928 | Yes (for complex tasks) |
| `### Frontmatter Update Protocol` | 943 | Yes |
| `## Detailed Task Instructions` | 954 | Yes (header) |
| `### Phase 1: Preparation and Setup` | 1012 | Yes |
| `### Phase 2: [Main Execution Phase Name]` | 1063 | Yes |
| `### Phase Gate: Quality Verification` | 1090 | Yes (when phase 2 outputs feed phase 3) |
| `### Phase [N]: Testing & Verification` | 1098 | Yes (I18 — when modifying source code) |
| `### Phase 3: [Review and Quality Assessment]` | 1106 | Yes (when QA gate applies) |
| `## Post-Completion Actions` | 1118 | Yes (I13, I17) |
| `## Task Log / Notes 📋` | 1128 | Yes |
| `### Task Summary` | 1130 | Yes (under Task Log) |
| `### Execution Log` | 1156 | Yes |
| `### Phase N - [Name] Findings` | 1166, 1176, 1185 | Yes (one per phase) |
| `### Phase Gate Findings` | 1187 | Yes (if PG exists) |
| `### Follow-Up Items Identified` | 1191 | Yes |
| `### Deviations from Process` | 1197 | Yes |

### Other rules cited

- **I15** (line 599-607) — every task with 2+ phases MUST include phase-gate QA between primary execution and dependent phases.
- **I16** (line 609-624) — PASS/FAIL only; fix cycle limits (research-gate=3, task-integrity=2, etc.).
- **I17** (line 626-635) — Post-Completion validation: all items checked, all output files exist (Glob), blocker entries resolved, tests pass for code tasks.
- **I18** (line 637-646) — code-modifying tasks MUST include test command, pass criteria, results capture, B2 pattern → use **L3** pattern.

---

## SECTION B — Prior cliEval-P* Task Patterns (cited per-file)

### B.1 Phase decomposition pattern (heaviest signal)

| Task | LOC | Phases (header + line) |
|---|---|---|
| **P1** pty-isolation-gates | 682 | 8 phases + 5 PG gates: Phase 1 Pre-Implementation Discovery (L145), **PG-1** (L183), Phase 2 Vendor ptytest Fork (L231), **PG-2** (L265), Phase 3 HomeIsolation (L313), **PG-3** (L335), Phase 4 Capability Gates + `eval doctor` (L377), **PG-4** (L395), Phase 5 Test Authoring (L437), **PG-5** (L455), Phase 6 Test Execution (L498), Phase 7 verify-sync POST (L520), Phase 8 Aggregation+AC Matrix+Completion (L534) |
| **P2** loader-models-expect | 375 | 4 phases + 3 PG gates: Phase 1 Prep/Dep/Discovery (L136), Phase 2 Data Models+Schema+Example (L164), **PG.1** (L188), Phase 3 Loader+DSL+CLI Subcommands (L204), **PG.2** (L232), Phase 4 Test Execution+Sync (L248), **PG.3** (L268), Post-Completion (L284) |
| **P3** orchestrator-runner-reporter | 429 | 7 phases (no separate PG-header — final QA inlined as Step 7.4/7.5): Phase 1 Merge Gate+Discovery (L153), Phase 2 Runner (~L180), … Phase 6 Tests, Phase 7 Final QA (Steps 7.1-7.5 incl. final rf-qa task-integrity at 7.4), Post-Completion Actions (L341 — Steps 8.1-8.3) |
| **P4** wire-and-ship | 211 | 7 phases: Phase 1 Setup+Prereq (L91), Phase 2 Wire eval_group (L101), Phase 3 Makefile+gitignore (L111), Phase 4 CliRunner Tests (L125), Phase 5 Post-P4 Validation (L135), Phase 6 Phase-Gate QA rf-qa (L147), Phase 7 Commit+PR+Completion (L155) |

**Pattern observations:**

1. **Phase count scales with file count.** P1 (14 files, ~400 LOC) used 8 phases; P4 (~5 files, ~50 LOC) used 7 phases. **Heavier scope ≠ more phases linearly** — it's *more PG gates* between phases.
2. **PG gate cadence:** P1/P2 use `#### PG-N: Phase-Gate QA` separator headers between phases; P3 inlines the final QA as Steps 7.4/7.5; P4 dedicates Phase 6 entirely to QA. All three idioms valid.
3. **Phase 1 is ALWAYS discovery/prereq verification** (status update + workspace check + design-spec read + open-question resolution). Never starts on code in Phase 1.
4. **Final phase is ALWAYS aggregation + AC matrix + frontmatter completion** (P1 §Phase 8, P2 §Post-Completion, P3 §Post-Completion Steps 8.1-8.3, P4 §Phase 7).

### B.2 Item granularity convention

**One item per concrete file or per acceptance criterion** — never per concern, never per directory.

Evidence:

- P1 Phase 2 Steps 2.2-2.7 = **6 items = 6 files** (`cli/eval/__init__.py`, `pty/__init__.py`, `pty/driver.py`, `pty/stream.py`, `pty/LICENSE`, `pty/PROVENANCE.md`) — P1:L239-261.
- P1 Phase 4 Steps 4.1-4.3 = **3 items** (2 files + 1 smoke test) — P1:L383-391.
- P2 Phase 2 Steps 2.1-2.5 = **5 items = 5 files** (`models.py`, `suite.schema.json`, `example.yaml`, `README.md`, `test_models.py`) — P2:L168-186.
- P4 Phase 2 Steps 2.1-2.3 = **3 items** (read insertion-point discovery + 2-line wiring edit + help-output smoke) — P4:L103-107.

**Items are full-paragraph self-contained prompts averaging 250-600 words** (B2/B3 compliance). Example: P1 Step 2.4 driver.py creation is one paragraph spanning L249, ~600 words.

### B.3 Verify clause format

Prior tasks **do not use a literal `Verify:` prefix** — they integrate verification via the **`ensuring …` clause** mandated by template B2(4) (L142-148). Search for `^Verify:` returns 0 hits in all four task files.

Instead, verification commands appear inline as part of the action paragraph:

| Verification kind | Idiomatic phrasing | Example file:line |
|---|---|---|
| Run tests | `Run the command \`uv run pytest tests/cli/test_eval/test_X.py -v 2>&1; echo "EXIT_CODE=$?"\` … capture … to phase-outputs/test-results/…` | P1:L504 (Step 6.1) |
| Capture verify-sync | `Run \`make verify-sync 2>&1; echo "EXIT_CODE=$?"\` … capture … expected EXIT_CODE=0` | P1:L167 (Step 1.5 PRE), L526 (Step 7.1 POST); P4:L97 (1.3 baseline), L137 (5.1 post) |
| Diff check | `Use \`git diff <path>\` to confirm the diff is precisely N lines added …` | P4:L105 (2.2), L113 (3.1), L117 (3.3) |
| Lint check | (NOT used in prior cliEval tasks — would be new) — typically `uv run ruff check --select F401,F821 <path>` |
| Click smoke | `uv run python -c "from … import …; from click.testing import CliRunner; r = CliRunner().invoke(eval_group, ['doctor']); print(r.output); print(f'EXIT_CODE={r.exit_code}')"` | P1:L391 (Step 4.3) |
| Help-output check | `uv run superclaude eval --help 2>&1 \| tee …; grep -E '^\s+(doctor\|list\|describe\|run)\s' …` | P4:L107 (2.3) |

**Implication for the remediation task:** the spec's three commands (§9) — `make verify-sync`, `uv run pytest tests/cli/eval/ -v`, `uv run ruff check --select F401,F821 src/superclaude/cli/eval/` — should be embedded inside the **action paragraph** of each phase-final or phase-gate item, NOT as a separate `Verify:` line. The capture pattern is consistent: `… 2>&1 | tee phase-outputs/test-results/NN-<name>.txt; echo "EXIT_CODE=$?" >> …` (P4:L97, L137).

### B.4 QA gate cadence

**Per-phase QA gates with a final composite gate.**

- **P1**: 5 PG gates (PG-1 → PG-5) between Phase 1-5 transitions + final composite rf-qa in Phase 8 Step 8.1 (P1:L540).
- **P2**: 3 PG gates (PG.1 → PG.3) — between Phase 2→3, 3→4, and final pre-Done (P2:L188, L232, L268).
- **P3**: No per-phase PG headers; one **final** rf-qa at Step 7.4 (P3:L331) + post-completion validation at Step 8.1 (P3:L347).
- **P4**: Final rf-qa concentrated in Phase 6 (P4:L147-151) + AC consolidation in Step 5.4 (P4:L143).

**Every gate uses the same self-contained item structure:**

1. Spawn `rf-qa` (or `rf-qa-qualitative`) with `subagent_type: "rf-qa"`, `mode: "bypassPermissions"`
2. Embed full prompt with `QA_MODE: task-integrity`, `fix_authorization: false` (per-phase) or `true` (final composite, P1:L545, P3:L331)
3. Prompt always includes the **ADVERSARIAL STANCE** block (P1:L195, P3:L331; matches `feedback_rfqa_adversarial_pattern.md`)
4. Always includes **ESCALATION — CRITICAL OVERRIDE: You have NO team context. Do NOT use SendMessage, TaskCreate, TaskUpdate, or TaskList.** (P1:L207)
5. Output to `phase-outputs/reviews/PG-N-rf-qa-report.md`
6. **Followed by L5 Conditional fix-cycle item** with Retry Monotonicity Protocol (regression check first, then `|F_n| >= |F_{n-1}|` halt) — P1:L227 PG-1.2, P1:L309 PG-2.2, etc.

### B.5 Execution Context block usage

| Task | Has `## Execution Context` block? | Citation |
|---|---|---|
| P1 | NO (TB-Add-7 marked INACTIVE in Step 8.1's rf-qa prompt: P1:L588) | P1:L588 |
| P2 | NO — uses Key Constraints in Prerequisites instead | P2:L130 |
| P3 | YES — `## Execution Context` between Prerequisites and Open Questions | P3:L132-138 |
| P4 | YES — same position, after Prerequisites, before `---` then Phase 1 | P4:L81-87 |

**Block contents (P3:L136 / P4:L85):**

- `**References:**` R-001..R-NNN — short labels, no file:line citations at task-header level
- `**Source areas:**` enumerated source-area list (P4 named 6 areas: superclaude top-level CLI dispatcher, cliEval Click group, project Makefile, repo-root gitignore, cliEval wiring tests, eval-run artifact root)
- `**Key constraints:**` (regression budget, sequencing dependencies, gate exits)

The block is preceded by an HTML comment: `<!-- Task-level READING aid. Per-item Context fields and research/*.md remain the evidence venue with file:line citations. This block contains NO specific path.py:NN references. -->` (P4:L83, P3:L134).

### B.6 Post-completion-phase ordering quirks

**P3 quirk (Step 8.1 → 8.2 → 8.3):** Post-completion validation phase numbered as **Phase 8 in Step IDs but lives under `## Post-Completion Actions`** (not `### Phase 8: …` header). P3:L341-355.

**P1 quirk (Phase 8 inlines final composite QA + AC matrix + frontmatter update):** P1's "Phase 8" is a real `### Phase 8` header but contains what other tasks call Post-Completion (Steps 8.1 final composite rf-qa + 8.2 AC verification matrix + 8.3 OQ update + 8.4 frontmatter Done). P1:L534-608.

**P4 quirk (numbered items `**X.Y**` not `Step X.Y`):** P4 uses bold-numbered list-item prefixes (`- [ ] **1.1**`) instead of `**Step X.Y:**` headers + checkbox below. P4:L93, L95, L97. Less verbose, more compact. Suitable for smaller-scope phases.

**P2 quirk (`### Phase Gate PG.N:`):** P2 uses `### Phase Gate PG.N: <Title>` (3-level heading) and inserts gates **between** phases at the same heading level. Other tasks use `#### PG-N:` (4-level). Both work; P2 chose 3-level for prominence.

---

## SECTION C — Synthesis: Recommendations for the cliEval Remediation Builder

### C.1 Phase count recommendation: **COLLAPSE 8 → 6 phases**

The spec's proposed 8 phases (test scaffolding → correctness → observability → layout → ordering → cross-cutting → Click symmetry → final regression) can be collapsed without losing fidelity by merging:

- **Phase 3 (observability) + Phase 6 (cross-cutting)** — both touch logging/error handling across files
- **Phase 4 (layout) + Phase 5 (ordering)** — both restructure existing code, no behavioral change

**Recommended 6-phase shape (matching prior P2's 4-phase + PG.1-3 idiom or P4's 7-phase compact idiom):**

| Phase | Name | Mirror of prior task |
|---|---|---|
| Phase 1 | Preparation & Discovery (read spec, inventory current state, baseline `make verify-sync` + pytest + ruff captures) | P1 Phase 1 + P4 Step 1.3 baseline pattern |
| Phase 2 | Test Scaffolding (write failing tests first — spec Phase 1) | New, but follows P1 Phase 5 test-file pattern |
| Phase 3 | Correctness + Observability fixes (spec Phases 2+3 merged) | P3 Phase 2 implementation pattern |
| Phase 4 | Layout + Ordering refactor (spec Phases 4+5 merged) | P3 Phase 3 pattern |
| Phase 5 | Click symmetry + cross-cutting cleanup (spec Phases 6+7) | P3 Phase 4-5 pattern |
| Phase 6 | Final Regression + AC Matrix + Completion (spec Phase 8) | P1 Phase 8 or P4 Phase 5-7 |

**Add PG gates:** PG-1 between Phase 2->3 (test-first contract sanity), PG-2 between Phase 4->5 (no-behavioral-change refactor verification), PG-FINAL inside Phase 6 (composite rf-qa task-integrity). This matches **P2's 3-gate cadence**.

**If the builder strongly prefers fidelity to the spec's 8 phases:** keep them, but the executor will read 8 short phases vs 6 medium phases — either is acceptable. The prior cliEval idiom skews toward **fewer, denser phases** (P3 = 7 phases over 440 LOC; P4 = 7 phases over 50 LOC).

### C.2 Verify command per phase

Per spec §9 the three required gate commands are:

1. `make verify-sync` (sync invariant)
2. `uv run pytest tests/cli/eval/ -v` (test pass)
3. `uv run ruff check --select F401,F821 src/superclaude/cli/eval/` (lint clean — F401 unused imports, F821 undefined names)

**Embedding pattern (matching P4:L97 baseline + P4:L137 post-state):**

```text
- [ ] [Phase-final or PG action item] … Run the command
`uv run pytest tests/cli/eval/ -v 2>&1 | tee
.dev/tasks/to-do/TASK-RF-20260522-153212/phase-outputs/test-results/NN-pytest-<phase>.txt;
echo "EXIT_CODE=$?" >>
.dev/tasks/to-do/TASK-RF-20260522-153212/phase-outputs/test-results/NN-pytest-<phase>.txt`
and confirm EXIT_CODE=0 with no NEW failures vs the Phase 1 baseline at
`phase-outputs/discovery/01-pytest-baseline.txt`, ensuring … If EXIT_CODE is non-0, …
```

**Per-phase verify cadence (recommended):**

| Phase | Verify commands at phase end |
|---|---|
| Phase 1 | All 3 baselines captured to `phase-outputs/discovery/` (PRE-state for regression check) |
| Phase 2 | `uv run pytest tests/cli/eval/ -v` — expect failures (tests-first; should fail until Phase 3) |
| Phase 3 | All 3 commands; pytest must now PASS |
| Phase 4 | `make verify-sync` + `uv run ruff check --select F401,F821` (refactor — no test change expected) |
| Phase 5 | All 3 commands |
| Phase 6 | All 3 commands POST-state + diff vs Phase 1 baselines (zero-new-failures check per P4:L139) |

### C.3 Execution Context block: **EMIT YES**

**Rationale:** Auto-emit rule triggered (>=3 source areas).

Source areas in this remediation:

1. `src/superclaude/cli/eval/commands.py` (Click symmetry + cross-cutting)
2. `src/superclaude/cli/eval/coverage.py` (correctness + observability)
3. `src/superclaude/cli/eval/config.py` (layout + ordering)
4. `src/superclaude/cli/eval/artifact_layout.py` (layout + ordering)
5. `src/superclaude/cli/eval/reporter.py` (observability)
6. `src/superclaude/cli/eval/run_report.py` (correctness + observability)
7. `tests/cli/eval/` (test scaffolding — Phase 1 of spec)

**That's 6 source areas under `src/superclaude/cli/eval/` plus the test tree — well above the >=3 threshold.** Emit per P4:L81-87 / P3:L132-138 form:

```text
## Execution Context

<!-- Task-level READING aid. Per-item Context fields and research/*.md remain the evidence venue with file:line citations. This block contains NO specific path.py:NN references. -->

- **References:** R-001: cliEval remediation spec at <path>; R-002: prior cliEval P1/P2/P3/P4 tasks for phase-pattern idiom; R-003: design-spec at .dev/releases/current/cliEval/design-spec.md; R-004: per-file research notes at .dev/tasks/to-do/TASK-RF-20260522-153212/research/.
- **Source areas:** cliEval Click commands surface, cliEval coverage tracker, cliEval config, cliEval artifact layout, cliEval reporter, cliEval run-report aggregator, cliEval pytest test tree.
- **Key constraints:** No behavioral changes during Phase 4 (layout/ordering) — refactor only; tests-first means Phase 2 pytest is EXPECTED to FAIL; all gate commands (`make verify-sync`, `uv run pytest tests/cli/eval/ -v`, `uv run ruff check --select F401,F821 src/superclaude/cli/eval/`) MUST exit 0 by Phase 6.
```

---

## SECTION D — Anti-Patterns to Avoid (from prior cliEval tasks)

### D.1 DO NOT skip baseline capture in Phase 1

P4:L97 (Step 1.3) captures **both** `pytest` and `make verify-sync` baselines BEFORE any edit. P1:L167 (Step 1.5) does the same for verify-sync. Without baselines, the Phase 6 regression check (P4:L139 "zero NEW failures vs pre-P4 baseline") is unmeasurable.

**Builder must include Phase 1 baseline-capture items** for all three gate commands.

### D.2 DO NOT create separate `Verify:` items

The template (B2 L142-148, I12 L573-578) explicitly forbids separate verification items. All four cliEval-P* tasks comply — zero items in any of the four match `^- \[ \] Verify:`. The builder must integrate verification via `ensuring … EXIT_CODE=0 …` clauses inside the action paragraph.

### D.3 DO NOT use `-A` or `.` when staging commits in Post-Completion

P4 Step 7.1 (P4:L157) explicitly warns: `do NOT use git add -A or git add . because those would pick up the phase-outputs/ evidence tree under .dev/tasks/to-do/`. Builder must list specific paths in any Post-Completion commit item.

**Reinforces:** the project's `.claude/` gitignore rule (memory `feedback_claude_dir_gitignored.md`) — if remediation touches `.claude/` paths, builder MUST route edits through `src/superclaude/` + `make sync-dev`, never direct-stage `.claude/*` (except `.claude/settings.json`).

### D.4 DO NOT spawn rf-qa without ADVERSARIAL STANCE + ESCALATION OVERRIDE

P1:L195, L207 + P3:L331 + P4:L149 all include the verbatim blocks:

- `**ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.`
- `ESCALATION — CRITICAL OVERRIDE: You have NO team context. Do NOT use SendMessage, TaskCreate, TaskUpdate, or TaskList. Return your verdict and report file path as your final output.`

This matches user memory `feedback_rfqa_adversarial_pattern.md`. Builder MUST include both blocks in every QA-gate spawn item.

### D.5 DO NOT forget Retry Monotonicity Protocol in fix-cycle items

P1:L227 (PG-1.2) is the canonical example:

1. Regression check FIRST — `Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.`
2. Monotonicity check — `[HALT-MONOTONICITY] |F|=<n>` when `|F_2| >= |F_1|`
3. Max 3 cycles per gate (task-integrity = 2 per template I16:L614)
4. **Each gate keeps its OWN F_n history** (P1:L227)

### D.6 DO NOT mix task-private and project-public paths in PR commits

P4:L157 warns about `.dev/tasks/to-do/.../phase-outputs/` staying task-private. Phase-outputs evidence trail is NEVER pushed.

### D.7 DO NOT omit `Once done, mark this item as complete.` terminator

All four tasks end every checklist item with this exact 11-word terminator. Builder must enforce this in every item.

### D.8 DO NOT use multi-line heredocs in user-facing paste-ready commands

User memory `feedback_no_multiline_paste.md` rule. P4:L159 contains a heredoc inside a `gh pr create` command — note this is **executor-only** (the agent runs it, not the user). Builder is safe to embed `cat <<'EOF' … EOF` blocks inside item action paragraphs because the executor agent runs them; only the **paste-ready prompts** surfaced to the user must be single-line.

---

## SECTION E — Summary Handoff for the Builder

**Recommended phase count:** **6 phases** (collapse spec's 8 by merging observability+cross-cutting and layout+ordering). Acceptable to keep 8 if the builder prefers literal spec fidelity.

**Per-phase verification cadence:** Embed all 3 spec §9 gate commands (`make verify-sync`, `uv run pytest tests/cli/eval/ -v`, `uv run ruff check --select F401,F821 src/superclaude/cli/eval/`) as **inline `ensuring … EXIT_CODE=0 …` clauses** inside the action paragraph of each phase-final item. Capture pattern: `… 2>&1 | tee phase-outputs/test-results/NN-<name>.txt; echo "EXIT_CODE=$?" >> …`. No separate `Verify:` items.

**Item granularity convention:** **One item per file or per acceptance criterion.** Each item is a single full paragraph (250-600 words) that is self-contained per template B2/B3.

**Execution Context block decision:** **EMIT YES** — 6+ source areas trigger auto-emission. Format per P4:L81-87. Include `<!-- Task-level READING aid … no path.py:NN references -->` comment.

**QA gate placement:** Mirror P2's 3-gate cadence — PG-1 after Phase 2 (test scaffolding contract), PG-2 after Phase 4 (refactor no-behavioral-change), PG-FINAL inside Phase 6 (composite rf-qa with `fix_authorization: true`). All gates use the ADVERSARIAL STANCE + ESCALATION OVERRIDE blocks plus Retry Monotonicity Protocol fix-cycle items.

**Frontmatter:** Use template (lines 1-44) with `template_schema_doc: ".claude/templates/workflow/02_mdtm_template_complex_task.md"`, `task_type: static`, `parent_task: ""` (or cliEval-release parent), `depends_on: []` if the remediation is standalone.

**Mandatory sections (in order):** Task Overview → Key Objectives → Prerequisites & Dependencies (Parent Task + Previous Stage Outputs + Handoff File Convention + Frontmatter Update Protocol) → **Execution Context** (this task) → Open Questions (if any from spec) → Detailed Task Instructions (header) → Phase 1..6 → Post-Completion Actions → Task Log / Notes (Task Summary + Execution Log + Phase N Findings + Phase Gate Findings + Follow-Up Items + Deviations).

**Anti-patterns to avoid:** No separate `Verify:` items; no missing Phase 1 baselines; no `git add -A` / `.`; no rf-qa spawn without ADVERSARIAL/ESCALATION blocks; no fix-cycle without Retry Monotonicity Protocol; no multi-line paste-ready commands surfaced to the user.

---

*End of research file 04 — Template & Examples.*
