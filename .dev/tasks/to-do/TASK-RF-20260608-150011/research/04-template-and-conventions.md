# Research: Template & Conventions

Status: Complete

Scope: Template-02 (complex) structure + project conventions the task-builder must follow when
building a Template-02 MDTM task that fixes two sprint-recovery defects and adds two regression
tests. Evidence cites `02_mdtm_template_complex_task.md` (PART 1 + PART 2), the task-builder
`SKILL.md` (the authoritative source for the 5-field item schema and the POST reflect gate), one
in-repo code+test example, and both CLAUDE.md files.

Key files:
- Template: `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md`
- Skill (item schema + POST reflect gate): `/config/workspace/IronClaude/src/superclaude/skills/task-builder/SKILL.md`
- Worked example (CLI .py + tests): `/config/workspace/IronClaude/.dev/tasks/done/TASK-RF-20260602-sprint-auto-resume/TASK-RF-20260602-sprint-auto-resume.md`

---

## 1. Template-02 PART 1 structure

PART 1 (`02_...complex_task.md:51-867`) is orchestrator-only instructions; **none of it appears in
the output task file**. The clean output template is PART 2 (`:876` onward). The template is the
generic upstream form. The task-builder SKILL.md overlays a tighter **5-field per-item schema** on
top of it (see §3) — when the two differ, the SKILL.md 5-field schema is what the builder emits and
what rf-qa validates against. Both agree on: self-contained items, granularity, sequential flow,
anti-orphaning, and an integrated "ensuring..." verification clause.

### 1a. Required frontmatter fields (PART 2)

From the template frontmatter (`:1-44`): `id`, `title`, `description`, `status` (`"🟡 To Do"` →
`"🟠 Doing"` → `"🟢 Done"`), `type`, `priority`, `created_date`, `updated_date`, `assigned_to`,
`autogen`, `autogen_method`, `coordinator`, `parent_task`, `depends_on` (list), `related_docs`
(list of `{path, description}`), `tags`, `template_schema_doc`, `estimation`, `sprint`, `due_date`,
`start_date`, `completion_date`, `blocker_reason`, `ai_model`, `model_settings`, `review_info`,
`task_type` (`static`|`dynamic`; this fix task is `static`).

The SKILL.md PART-2 frontmatter (`SKILL.md:1935-1949`) adds two reflection-gate fields:
- `reflect_pre:` — a block with `verdict / coverage_pct / depth / tcs / run_id / report / reviewed_at`.
- `reflect_post: ""` — `# PENDING sentinel set by the final-phase POST reflect item; operator
  records {verdict, run_id, report} in a fresh session` (`SKILL.md:1942`).

The worked example sets `template_schema_doc: ".claude/templates/workflow/02_mdtm_template_complex_task.md"`
(`example:37`) — recommend the builder do the same.

### 1b. Mandatory section list (exact)

PART 1 Section D (`:233-272`) names the mandatory sections. Section D3 gives the exact ordering rule
(`:269-272`):

> D3. CRITICAL RULE
>    NO CHECKLIST ITEMS may appear before Phase 1 begins. The template structure ensures:
>    - Frontmatter → Workflow Compliance (informational) → Prerequisites (informational) → Phase 1 (executable)
>    - All checklist items for context review and previous stage inputs appear IN Phase 1, Steps 1.2-1.4

The PART-2 output skeleton headings, in order (`:890-1128`):
`# [Task Title]` → `## Task Overview` → `## Key Objectives` → `## Prerequisites & Dependencies`
(with `### Parent Task & Dependencies`, `### Previous Stage Outputs (MANDATORY INPUTS)`,
`### Handoff File Convention`, `### Frontmatter Update Protocol`) → `## Detailed Task Instructions`
→ `### Phase 1: Preparation and Setup` → `### Phase 2: [Main Execution]` →
`### Phase Gate: Quality Verification` → `### Phase [N]: Testing & Verification` →
`### Phase 3: [Review and Quality Assessment]` → `## Post-Completion Actions` →
`## Task Log / Notes 📋`.

The SKILL.md's own PART-2 skeleton (`SKILL.md:1951-2019`) is the simpler shape the builder actually
emits: `# Title` → `## Task Overview` → `## Key Objectives` → `## Prerequisites & Dependencies` →
`## Execution Context` (OPTIONAL — emit only with ≥3 inferable source areas; **no file:line refs**,
`SKILL.md:1970-1975`) → `## Phase 1..N` → `## Task Log / Notes` (with `### Execution Log`,
`### Phase Findings`, `### Follow-Up Items`). Workflow-compliance sections are WORKFLOW-DEPENDENT
(Section A1, `:72-83`) and OMITTED for this task (no governing `.gfdoc/.roo` workflow doc).

### 1c. Self-contained item pattern — the 5 required elements

Template Section B is titled CRITICAL (`:131`). B1 (`:134-140`) gives the rationale: Rigorflow
executes in batches across sessions; context loaded in batch 1 is GONE by batch 3, so every item
must be self-contained. B2 (`:142-148`) lists the **6 elements** a complete item embeds:

> 1. **Context Reference with WHY** — What file(s) to read and why...
> 2. **Action with WHY** — What to do with that context and why...
> 3. **Output Specification** — exact output file name, location, content, template...
> 4. **Integrated Verification** — an "ensuring..." clause (DO NOT assume/hallucinate; 100% from source; document negative evidence)
> 5. **Evidence on Failure Only** — Log to task notes ONLY if blocked/errored (success is evidenced by the output file)
> 6. **Explicit Completion Gate** — "This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete."

Template B3 (`:150-153`) requires **one full verbose paragraph per item** (not bullets). FORBIDDEN
patterns (B5, `:164-184`): standalone "read context" items, items with no context source, multi-line
bulleted items, separate verification/confirmation items, "create directory" alone, REMINDER blocks
between items.

**The 5-field schema the builder actually emits (SKILL.md / rf-qa validation form).** SKILL.md
collapses B2's 6 elements into a **5-field bullet structure** per item (`SKILL.md:1980-1985`,
validation criterion `SKILL.md:2030`: "Items follow B2 self-contained pattern (context + action +
output + verification + completion gate)"):

```markdown
- [ ] **N.M — [Step Title]**
  - **Context**: [What the executor needs to know — file:line citations for code surfaces]
  - **Action**: [Exactly what to do]
  - **Output**: [What gets created/modified]
  - **Verification**: [How to confirm it worked — the test command / observable check]
  - **Completion gate**: [When this item is done]
```

This 5-field form is what the worked example uses throughout (e.g. `example:94-138`) and is the form
this builder MUST use. (B2's "evidence-on-failure" element is folded into Context/Completion-gate;
the 6→5 mapping is intentional per SKILL.md.)

### 1d. Rule A3 — complete granular breakdown (`:91-95`)

> - Break down EVERY workflow phase into atomic, verifiable checklist items
> - Create individual checklist items for EVERY file, component, or iteration
> - NO high-level or bulk operations allowed - everything must be granular
> - Include exact file paths, specific requirements, and measurable outcomes

For this task: one item per defect fix (per modified function/file), one item per added regression
test, separate items for the pytest run and the lint/format run. No "fix both defects" mega-item.

### 1e. Rule A4 — iterative process structure (`:97-116`)

> - Pre-enumerate ALL items to be processed in initial step
> - Create individual checklist item for each specific item
> - Require incremental updates after each item
> - Include consolidation step only after all items complete

Pattern: `Step X.1` scan/enumerate → `Step X.2` process each item individually (one checkbox each)
→ `Step X.3` consolidate. For a fixed 2-defect/2-test scope, items can be pre-enumerated directly
(no dynamic discovery needed; `task_type: static`).

### 1f. Anti-orphaning — completion items INSIDE the final phase

Template C4 (`:225-230`) + I13 (`:580-585`): task completion is the `## Post-Completion Actions`
section; do NOT create a separate "Task Completion and Handoff Protocol" section. The
SKILL.md validation checklist states it as a hard rule (`SKILL.md:2040`):

> - [ ] Task completion items inside final phase (anti-orphaning)

So the "Update task status to Done" item and the POST reflect gate item live **as the last items of
the final phase** (the example does this — `5.7 — Update task status to Done` is the last item of
Phase 5, `example:328-333`), NOT in a detached trailing section.

### 1g. L1–L6 intra-task handoff patterns (Section L, `:711-835`)

Handoff files persist on disk across batches under `.dev/tasks/TASK-NAME/phase-outputs/` with
subdirs `discovery/`, `test-results/`, `reviews/`, `plans/`, `reports/` (`:718-726`). Patterns:

| Pattern | Use | Lines |
|---------|-----|-------|
| **L1 Discovery** | Explore codebase, write structured findings later items read | `:737-747` |
| **L2 Build-from-Discovery** | Create output from a discovery file + source files | `:749-759` |
| **L3 Test/Execute** | Run a command/test suite; capture BOTH raw output AND a structured summary | `:761-771` |
| **L4 Review/QA** | Assess a prior output vs source; produce PASS/FAIL + findings | `:773-783` |
| **L5 Conditional-Action** | Branch on a prior result; MUST handle BOTH success and failure | `:785-797` |
| **L6 Aggregation** | Glob all relevant files, consolidate into one report | `:799-809` |

Selection guide + common phase structures at `:811-835`. For a code+test fix, the relevant chain is
**"Build → Test → Fix"** (`:828-829`): `K1/K2 (build the fixes) → L3 (run pytest) → L5 (conditional:
fix or proceed)`. **I18** (`:637-646`) is binding here: any task that modifies source code MUST
include ≥1 testing item, specifying the test command, pass criteria, where results are captured, and
using the L3 pattern. **M1 phase-gate** (`:843-851`) applies to code-modifying tasks "after
implementation phase and before testing phase" (`:857`); in practice the example folds the lint/test
gate into per-phase verification items rather than spawning rf-qa mid-phase — acceptable for a small
2-defect fix, but the POST reflect gate (§4) is the mandatory independent verification.

---

## 2. Existing CLI-code + test examples

### 2a. PRIMARY example — `TASK-RF-20260602-sprint-auto-resume` (done)

Path: `.dev/tasks/done/TASK-RF-20260602-sprint-auto-resume/TASK-RF-20260602-sprint-auto-resume.md`.
This is the closest analog: it modifies CLI Python under `src/superclaude/cli/sprint/`, adds pytest
modules under `tests/sprint/`, runs `uv run pytest` + `uv run ruff check`, and uses the exact 5-field
item schema this builder should emit. Effective patterns to mirror:

**"Modify function X in file Y" item** (`example:108-112`, item 1.3):
> - **Context**: `_write_phase_result_json` is at `src/superclaude/cli/sprint/executor.py:2053`; payload dict at L2059-2067; atomic tmp+rename at L2070-2072 (`tmp.replace(out)`)...
> - **Action**: Extend the payload dict with one key: `tasklist_sha256 = _content_sha256_excluding_rerun_block(phase_obj.file)`... Reuse the existing atomic writer (do NOT add a second write)...
> - **Verification**: Locate the function by name; confirm the new key rides the existing tmp+rename path. `uv run pytest tests/ -k "phase_result_json or write_phase_result" -v` passes; manually confirm...

Takeaways: Context carries a precise `file.py:NN` citation for the symbol; Action says reuse the
existing path / no new machinery (scope discipline); Verification names a *specific* `-k`-scoped
pytest plus a manual observable check.

**"Add test to module/class Z" item** (`example:293-298`, item 5.2; `:287-291` item 5.1):
> - **Action**: Author `test_boundary_quarantine_nondestructive` (FR-2.5: ...) and `test_haiku_coherence_advisory_only` (...). Add an INV-001 test: stored ... and current ... use the same fn+file ⇒ Tier 0 matches on an unchanged tasklist.
> - **Output**: New test module(s) under `tests/` (e.g. `tests/sprint/test_resume_*.py`).
> - **Verification**: `uv run pytest tests/ -k "quarantine or coherence or inv001 or advisory" -v` passes; the advisory-only and non-destructive invariants are explicitly asserted.
> - **Completion gate**: Quarantine non-destructiveness, Haiku advisory-only, and INV-001 are test-locked.

Takeaways: each test is named explicitly with the behavior it locks; tests are tied to a concrete
file path; Completion gate phrases the *invariant* the test must prove, not just "test added".

**Lint / pytest validation item** (`example:307-312`, item 5.4):
> - **Action**: `uv run pytest tests/ -k "sprint" -v` and `uv run ruff check src/superclaude/cli/sprint/`. Fix any regression.
> - **Verification**: All sprint tests pass; no lint errors; explicit-flag paths unchanged.
> - **Completion gate**: Full sprint suite + lint green.

Per-phase mini-gate items also appear at `:137-138`, `:171-172`, `:219-220` — each runs the scoped
`uv run pytest ... -k "..."` plus `uv run ruff check <changed paths>`. **Regression-classification
discipline** worth copying: when tests fail, the example proves whether failures are pre-existing by
`git stash`-ing only the tracked change and re-running on base (`example:348`, `:361`, `:366`) —
recommend a Verification clause that says "if failures appear, confirm they are this change's
regressions vs pre-existing via git-stash before fixing."

### 2b. SECONDARY example — `TASK-RF-20260524-issue-60-ruff-debt` (done)

Path: `.dev/tasks/done/TASK-RF-20260524-issue-60-ruff-debt/`. A lint/ruff-debt remediation task —
useful as a second reference for how lint-only validation items are phrased (`make lint`/ruff
scoping). Cited as an additional precedent for the lint-validation item shape.

---

## 3. Project conventions binding on THIS task

Sources: global `~/.claude/CLAUDE.md` and project `/config/workspace/IronClaude/CLAUDE.md`.

### 3a. UV-only commands
- "Never use `python -m`, `pip install`, or `python script.py` directly." (project CLAUDE.md
  "🐍 Python Environment Rules"; global core rule #1 "UV only").
- The task's test command (per BUILD goal):
  `uv run pytest tests/sprint/test_recovery.py tests/sprint/test_checkpoints.py -v`
- Lint / format: `make lint` (ruff) and `make format` (project CLAUDE.md "Code Quality"). Builder
  may also use scoped `uv run ruff check src/superclaude/cli/sprint/` as the example does.
- Embed these verbatim in the L3/I18 testing items' Action and Verification fields.

### 3b. `make sync-dev` is NOT needed for CLI `.py` changes
- Source of truth is `src/superclaude/` (project CLAUDE.md:141). `make sync-dev` copies ONLY
  `src/superclaude/{skills,agents,commands}` → `.claude/` (CLAUDE.md:122, 147-148). The sync gate
  exists exclusively for distributable Markdown components (skills/agents/commands), NOT for CLI
  Python under `src/superclaude/cli/`.
- **Implication for the builder:** since this task edits CLI `.py` files (`src/superclaude/cli/...`)
  and `tests/`, do NOT emit any `make sync-dev` / `make verify-sync` item. Those would be no-ops for
  Python changes and risk confusion. Edits to `src/superclaude/cli/...` are the final state directly.

### 3c. Feature-branch-only — a NEW branch is required
- "feature branches only; never commit directly to master/main" (global rule #4; project
  "🌿 Git Workflow").
- Current branch is `fix/prd-document-capture-hotfix` — **unrelated** to sprint recovery. The builder
  must instruct the executor to create a fresh branch off the integration/master base (e.g.
  `git checkout -b fix/sprint-recovery-<slug>`) BEFORE editing, and NEVER commit to `master` or to
  the unrelated hotfix branch. (Commit/push only when the user asks.)

### 3d. ABSOLUTE rule — NEVER stage `.claude/` paths
- `.claude/{skills,commands,agents,hooks,templates}/*` is gitignored sync output; the only tracked
  `.claude/` file is `.claude/settings.json` (project CLAUDE.md "ABSOLUTE RULE: Never Stage or Commit
  `.claude/` Contents", `:18`, `:27`). Any `git add -f` on a `.claude/` path is the "violation siren."
- **Implication:** this task touches no `.claude/` paths at all (pure CLI `.py` + `tests/`). The
  builder should add no `.claude/` staging items, and any commit-guidance item must explicitly stage
  only `src/superclaude/cli/...` and `tests/...` paths.

### 3e. PR target (only if a PR item is emitted)
- If the BUILD scope ever includes a PR: `gh pr create --repo IronbellyOrg/IronClaude --base master
  --head <branch> ...` — NEVER a bare `gh pr create` (defaults to upstream). (project CLAUDE.md
  "ABSOLUTE RULE: PR Target = Fork".) For a fix+test task this is typically out of scope unless the
  user asks.

---

## 4. POST reflect gate — penultimate item shape (exact convention)

The raw Template-02 file contains **no** `reflect_post` field and no POST reflect item — that
convention is defined in the task-builder **SKILL.md** and is what the builder must emit. Trigger:
emitted when the BUILD_REQUEST specifies `POST_REFLECT_GATE: ENABLED` (`SKILL.md:2108`):

> 19. **POST reflect gate in generated task files.** When the BUILD_REQUEST specifies
> `POST_REFLECT_GATE: ENABLED`, the builder MUST emit, as the penultimate item of the final phase
> (immediately before the `Update task status to Done` item, preserving anti-orphaning per the
> validation checklist), a fresh-session reflect handoff item. The item MUST NOT run reflect inline
> in the executor's biased context; it writes a `reflect_post: PENDING` sentinel and HALTs until the
> operator records the verdict in a fresh session. The handoff command uses `/sc:reflect` for the
> gate and `/task` (never `/sc:task`) for any re-execution. A generated task file that omits the
> POST reflect item when `POST_REFLECT_GATE: ENABLED` is a MALFORMED output.

Position is also a validation criterion (`SKILL.md:2051`):

> - [ ] POST reflect item present and positioned penultimate (immediately before
> Update-status-to-Done) when POST_REFLECT_GATE is ENABLED — MALFORMED if omitted

Frontmatter sentinel (`SKILL.md:1942`): `reflect_post: ""   # PENDING sentinel ...`.

### 4a. Exact templated item (verbatim, `SKILL.md:1994-1999`)

```markdown
- [ ] **N.{X-1} — Independent post-execution reflection gate (fresh session, HALT)**
  - **Context**: All implementation/test/QA items above are complete. The inline rf-qa gates ran in THIS executor's frame and cannot perform an executor-disjoint audit. Per project memory `feedback_sc_reflect_vs_inline_rfqa`, an independent `/sc:reflect --mode post` ensemble catches spec-literal-token, invariant-arithmetic, and integration/orphan blindspots that same-frame QA misses.
  - **Action**: Do NOT run reflect inside this session. Write `reflect_post: PENDING` to this file's frontmatter, then STOP and surface this paste-ready command for the operator to run in a NEW session: `/sc:reflect --mode post --remediate --diff <BASE>..HEAD --tasklist {TASK_FILE} [--spec {SPEC_PATH}] --depth {DEPTH} --executor-model {EXECUTOR_CLASS}` — where `<BASE>` is the commit recorded at task start (frontmatter `start_commit`, or `git merge-base HEAD <integration>` if unset), `{DEPTH}` is floored at `standard` per O4 (the POST gate NEVER runs `--depth quick`), and the spawned reflect agent uses the default subagent model. The gate command uses `/sc:reflect` and never the `sc:task` execution command.
  - **Output**: Frontmatter `reflect_post: PENDING`; paste-ready `/sc:reflect --mode post` command surfaced for a fresh session.
  - **Verification**: `reflect_post` is PENDING and the operator has the exact `/sc:reflect` command. The item does NOT self-resolve.
  - **Completion gate**: Operator has run `/sc:reflect --mode post` in a fresh session and recorded its verdict (`reflect_post: {verdict, run_id, report}`) in frontmatter. Only THEN may the Update-status-to-Done item proceed (HALT per `feedback_human_decision_items_must_halt`).
```

### 4b. The final "Update status to Done" item (last item, `SKILL.md:2001-2006`)

```markdown
- [ ] **N.X — Update task status to Done**
  - **Context**: All phases complete.
  - **Action**: Update frontmatter: status to "🟢 Done", set completion_date.
  - **Output**: Task file updated.
  - **Verification**: Frontmatter shows "🟢 Done".
  - **Completion gate**: Task marked complete.
```

So the final phase ends with: ...→ [last test/lint item] → **N.{X-1} POST reflect gate (HALT)** →
**N.X Update status to Done**. The summary line in SKILL.md (`:1469`):
`POST (--mode post): TEMPLATED as final-phase item N.{X-1} (operator runs /sc:reflect in a fresh
session)`.

---

## Summary for the builder

1. **Emit the 5-field item schema** (`Context / Action / Output / Verification / Completion gate`)
   per item — this is SKILL.md's operationalization of Template B2 and what rf-qa validates
   (`SKILL.md:2030`). One verbose, self-contained item per fix and per test (A3 granularity).
2. **Phase shape = "Build → Test → Fix"** (Template `:828-829`): Phase 1 builds the two defect fixes
   (one item each, with `file.py:NN` Context citations); Phase 2 adds the two regression tests
   (one item each, named, tied to `tests/sprint/test_recovery.py` / `test_checkpoints.py`); a testing
   item runs `uv run pytest tests/sprint/test_recovery.py tests/sprint/test_checkpoints.py -v`
   (I18 + L3, mandatory for code-modifying tasks) and `make lint` / `make format`.
3. **Frontmatter**: full Template-02 set + `reflect_post: ""` sentinel; `task_type: static`;
   `template_schema_doc` pointing at the Template-02 path. Set a real `parent_task`/`related_docs`
   from the BUILD_REQUEST and the troubleshoot REPORT.
4. **Anti-orphaning**: completion items live INSIDE the final phase. Order the final phase as
   `... → POST reflect gate (penultimate, HALT, writes reflect_post: PENDING) → Update status to Done (last)`.
5. **Conventions**: UV-only (`uv run pytest ...`, `make lint`, `make format`); NO `make sync-dev`
   (CLI .py is not a synced component); create a NEW feature branch (current
   `fix/prd-document-capture-hotfix` is unrelated; never touch master); NEVER stage `.claude/` paths
   (this task touches none); if a PR is in scope use `--repo IronbellyOrg/IronClaude`.
6. **POST reflect gate**: emit the verbatim `N.{X-1}` item from §4a when `POST_REFLECT_GATE: ENABLED`;
   omitting it is a MALFORMED output (`SKILL.md:2051`, `:2108`).
