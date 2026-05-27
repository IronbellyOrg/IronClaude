# Research: MDTM Template Selection + Project Conventions
**Topic type:** Template & Examples
**Scope:** MDTM templates 01/02 + Makefile + CLAUDE.md + recent done tasks
**Status:** Complete
**Date:** 2026-05-27
---

## 1. MDTM Template 01 vs 02 — Selection Rationale

### Template 01 (Generic Task)

[CODE-VERIFIED] `/config/workspace/IronClaude/src/superclaude/templates/workflow/01_mdtm_template_generic_task.md:43-149`

Core rules (PART 1):

- **A3 (Complete Granular Breakdown):** every phase broken into atomic, verifiable checklist items; one item per file/component/iteration; no bulk operations; exact file paths required.
- **A4 (Iterative Process Structure):** pre-enumerate items, one checklist item per item, consolidation step after all items complete.
- **B1 (Session Rollover Protection):** every item must be self-contained because context from batch 1 is NOT available in batch 3+.
- **B2 (Self-Contained Item Pattern):** each item must include (1) Context Reference with WHY, (2) Action with WHY, (3) Output Specification, (4) Integrated Verification ("ensuring..."), (5) Evidence on Failure Only, (6) Explicit Completion Gate.
- **B3:** each item is ONE FULL PARAGRAPH (not multiple bullets), readable as a complete prompt with no prior context.

### Template 02 (Complex Task)

[CODE-VERIFIED] `/config/workspace/IronClaude/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:60-65`

Verbatim header note:

> TEMPLATE 02: COMPLEX TASK TEMPLATE
> Extends Template 01 with Section L: Intra-Task Handoff Patterns
> Use this template when tasks require discovery, testing, review,
> conditional logic, or aggregation between checklist items.

Sections A/B are identical to Template 01; Template 02 adds Section L (intra-task handoff) for discovery → build → test → review chains.

### Recommendation: **Template 01 (Generic Task)**

**Rationale:**

1. The task is a fully-specified additive edit to a single markdown file (`src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md`). Inputs (the 5 Insertion Blocks from R2's spec) and outputs (edited file + sync mirror + lint pass) are fully known up front.
2. No discovery phase needed — R2 supplied the exact insertion blocks.
3. No conditional logic, no parallel subagents, no test-then-fix loop, no aggregation across checklist items — each phase feeds linearly into the next (edit → sync → verify → lint → QA).
4. Quick tier directive explicitly rules out the complex multi-phase patterns Template 02 is designed for.
5. Template 01's A3/A4/B2 rules are sufficient: each Insertion Block becomes one self-contained checklist item; each verification command (sync-dev, verify-sync, lint) becomes one self-contained item.

---

## 2. Sync-Dev + Verify-Sync Workflow (Verbatim From Makefile)

### `sync-dev` target

[CODE-VERIFIED] `/config/workspace/IronClaude/Makefile:108-163`

Header comment (line 108):

```text
# Sync src/superclaude/{skills,agents} → .claude/ for local dev
```

Recipe (selected key behavior — full recipe is 55 lines):

- Line 110: prints `🔄 Syncing src/superclaude/ → .claude/ for local development...`
- Lines 112-125: walks `src/superclaude/skills/*/`, skips `__*` dirs, mirrors each skill that has a `SKILL.md` or `skill.md` into `.claude/skills/<name>/`, copying every file except `__init__.py` and `__pycache__`.
- Lines 126-130: copies `src/superclaude/agents/*.md` (except `README.md`) to `.claude/agents/`.
- Lines 131-136: copies `src/superclaude/commands/*.md` to `.claude/commands/sc/`.
- Lines 137-143: copies `src/superclaude/hooks/scripts/*.sh` to `.claude/hooks/` and chmod +x.
- Lines 148-157: copies `src/superclaude/templates/**` (except `agent-memory/` and `__pycache__`) to `.claude/templates/` preserving relative paths.

**Command the task should run:** `make sync-dev` [CODE-VERIFIED — Makefile:109 target declaration]

### `verify-sync` target

[CODE-VERIFIED] `/config/workspace/IronClaude/Makefile:165-353`

Header comment (line 165):

```text
# Verify src/superclaude/ and .claude/ are in sync (CI-friendly, exits 1 on drift)
```

Recipe (selected key behavior — full recipe is 188 lines):

- Walks `src/superclaude/skills/*/` and compares each against `.claude/skills/<name>/` with `diff -rq --exclude='__init__.py' --exclude='__pycache__'`; flags `MISSING` or `DIFFERS`.
- Walks `.claude/skills/*/` in reverse direction; flags any `.claude/` skill missing from `src/superclaude/skills/`.
- Performs identical bidirectional checks for `agents/`, `commands/`, `hooks/`, **and `templates/`**.
- Template check (lines 280-305): iterates `find src/superclaude/templates -type f ! -path '*/__pycache__/*'`, compares with `diff -q`, flags `MISSING` or `DIFFERS`. Reverse walk skips files matching `*.legacy-rf-project.md`.
- Lines 308-326: verifies `_FRESHNESS_SCRIPTS` registration matches `src/superclaude/hooks/scripts/*.sh`.
- Lines 328-346: cross-checks `hooks.json` matcher prefixes against `auggie-flag-clear.sh` case body.
- Lines 348-353: if any drift, prints `❌ Drift detected! Run 'make sync-dev' to fix...` and `exit 1`.

**Command the task should run:** `make verify-sync` [CODE-VERIFIED — Makefile:166 target declaration]

**NOTE on relevance to this task:** The target file lives at `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` — it IS a skill ref file (NOT under `src/superclaude/templates/`), so it is covered by the skill-mirror block (lines 112-125), not the template-mirror block.

---

## 3. Markdownlint Gate

[CODE-VERIFIED] `/config/workspace/IronClaude/.pre-commit-config.yaml:70-82`

Markdownlint is wired as a **pre-commit hook** via `igorshubovych/markdownlint-cli@v0.38.0`:

```yaml
# Markdown linting
- repo: https://github.com/igorshubovych/markdownlint-cli
  rev: v0.38.0
  hooks:
    - id: markdownlint
      args: ['--fix']
      exclude: |
        (?x)^(
          CHANGELOG\.md|
          .*node_modules.*|
          .*\.min\.md$|
          \.dev/.*
        )$
```

Key observations:

- Hook runs with `--fix` (auto-fixes formatting issues where possible).
- Exclusion pattern excludes `\.dev/.*` — so task files under `.dev/tasks/` are NOT linted, but the **target file** at `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` IS linted (it's under `src/`, not `.dev/`).
- No standalone `make lint-md` target exists. [CODE-VERIFIED — `grep -n "markdownlint" Makefile` returns no matches.]
- `package.json` has no markdownlint script (only `eslint` for JS). [CODE-VERIFIED — `/config/workspace/IronClaude/package.json:5-10`]
- Pre-commit must be installed for the hook to run automatically (`pre-commit install`).

**Recommended command for the task to verify lint passes on the edited file:**

```bash
pre-commit run markdownlint --files src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md
```

This runs only the markdownlint hook against the single edited file (faster than `pre-commit run --all-files`) and respects the same `--fix` configuration.

[CODE-VERIFIED] hook id `markdownlint` is declared at `.pre-commit-config.yaml:74`. Pre-commit's `run --files <path>` invocation is the standard way to target a single file.

**Note on potential CI gate:** The pre-commit `block-claude-generated-mirrors` local hook (`.pre-commit-config.yaml:102-109`) blocks staging `.claude/` mirror paths on commit. The task should ensure only `src/` paths are staged.

---

## 4. Source-of-Truth Rule

[CODE-VERIFIED] `/config/workspace/IronClaude/CLAUDE.md:141-156` — quoted verbatim:

> **Source of truth**: `src/superclaude/` is the canonical location for all distributable components (skills, agents, commands, core files). The `superclaude install` CLI reads from here.
>
> **Dev copies**: `.claude/skills/` and `.claude/agents/` in the repo root are convenience copies that Claude Code reads directly during development.
>
> **Workflow when adding/editing components**:
>
> 1. Edit files in `src/superclaude/skills/` or `src/superclaude/agents/`
> 2. Run `make sync-dev` to copy changes to `.claude/`
> 3. Run `make verify-sync` to confirm sync (also run before committing)

[CODE-VERIFIED] `/config/workspace/IronClaude/CLAUDE.md:18` (project-specific gitignore note):

> `.claude/{skills,commands,agents,hooks,templates}/*` is **gitignored sync-dev output** of `src/superclaude/`. The ONLY tracked file under `.claude/` is `.claude/settings.json`.

[CODE-VERIFIED] User memory `feedback_claude_dir_gitignored.md` (already in context): "Never commit `.claude/skills,commands,agents,hooks` — those are sync-dev output of `src/superclaude/`."

### Applied to this task

- Edit target: `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` (the `src/` original).
- After `make sync-dev`, mirror appears at: `.claude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md`.
- Direct editing of `.claude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` is FORBIDDEN — it is gitignored output and will be overwritten by the next `make sync-dev`.
- The task builder must NOT generate any checklist item that edits the `.claude/` mirror.

---

## 5. Precedent Search

### Search results

```text
$ ls .dev/tasks/done/ | head -30
[30 entries including TASK-RF-20260517-213436, TASK-RF-track-3-20260517-032112, etc.]

$ grep -rl "make sync-dev" .dev/tasks/done/ 2>/dev/null | head -5
.dev/tasks/done/BUILD-REQUEST-C122-auto-detection.md
.dev/tasks/done/TASK-RF-track-3-20260517-032112/TASK-RF-track-3-20260517-032112.md
.dev/tasks/done/TASK-RF-20260517-213436/qa/qa-qualitative-review.md
.dev/tasks/done/TASK-RF-20260517-213436/phase-outputs/reviews/pg5-task-integrity-verdict.md
.dev/tasks/done/TASK-RF-20260517-213436/research/03-test-verification.md

$ grep -rl "make verify-sync" .dev/tasks/done/ 2>/dev/null | head -5
.dev/tasks/done/TASK-RF-track-3-20260517-032112/research-notes.md
.dev/tasks/done/TASK-RF-track-3-20260517-032112/phase-outputs/reviews/pg4-final-verdict.md
.dev/tasks/done/TASK-RF-track-3-20260518-231708/phase-outputs/reports/phase-3-aggregation.md
.dev/tasks/done/TASK-RF-20260517-213436/qa/qa-research-gate-report.md
.dev/tasks/done/TASK-RF-20260517-213436/phase-outputs/reviews/pg6-final-verdict.md
```

[CODE-VERIFIED — bash output above]

### Closest precedent

`/config/workspace/IronClaude/.dev/tasks/done/TASK-RF-20260517-213436/TASK-RF-20260517-213436.md` — this task referenced `make sync-dev` and `make verify-sync` across both research and QA artifacts, indicating these commands are an established convention in MDTM task files. However, this is a multi-phase complex task with `phase-outputs/`, `qa/`, and `research/` sub-directories — NOT a Quick-tier single-file-edit precedent.

`/config/workspace/IronClaude/.dev/tasks/done/TASK-RF-track-3-20260517-032112/TASK-RF-track-3-20260517-032112.md` — also referenced both commands; same caveat (complex multi-phase track task).

**No close precedent found in `.dev/tasks/done/` for a Quick-tier additive-frontmatter single-file edit using Template 01.** The existing precedents are all multi-phase Template-02-style tasks. The task builder will be establishing a new Quick-tier pattern; the relevant precedent is the *commands used* (`make sync-dev`, `make verify-sync`), not the overall phase structure.

---

## 6. Recommended Phase Structure (Quick Tier, Template 01)

### Phase 1: Edit target file (6 items)

1. **Read-and-confirm baseline** — Read the current file `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` end-to-end, verify it matches R1's reported baseline, and confirm the 5 insertion anchors from R2's spec are present.
2. **Insertion Block 1** — Apply Insertion Block 1 from R2's spec at the anchor R2 identified, using the exact text R2 supplied.
3. **Insertion Block 2** — Apply Insertion Block 2 at its anchor.
4. **Insertion Block 3** — Apply Insertion Block 3 at its anchor.
5. **Insertion Block 4** — Apply Insertion Block 4 at its anchor.
6. **Insertion Block 5** — Apply Insertion Block 5 at its anchor.

(One item per insertion = atomic + resumable per A3/A4. Each item is fully self-contained per B2/B3, including the exact `old_string`/`new_string` from R2's spec.)

### Phase 2: Sync + verify-sync + lint (3 items)

7. **Run `make sync-dev`** — Mirror `src/` edits to `.claude/`. Capture stdout. Verify exit code 0 and that the success line `✅ Sync complete.` is present.
8. **Run `make verify-sync`** — Confirm no drift. Capture stdout. Verify exit code 0 and that the final line is `✅ All components in sync.`
9. **Run `pre-commit run markdownlint --files src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md`** — Verify markdownlint passes (or that any `--fix` modifications are themselves still in-sync; if the lint hook modifies the file, re-run sync-dev + verify-sync).

### Phase 3: Final QA + status update (2 items, anti-orphan)

10. **Final QA gate** — Re-read the edited file, confirm all 5 Insertion Blocks are present in the expected anchors, no behavior change to surrounding markdown, no broken code fences, no malformed frontmatter. Document verification in task notes only on failure.
11. **Mark task complete** — Update task frontmatter `status: "🟢 Done"`, `completion_date: 2026-05-27`, append final task-log entry. (Final completion item lives INSIDE Phase 3 per anti-orphaning rule — never as a dangling top-level item.)

### Total: 11 items across 3 phases

Builder may merge items 5 and 6 if Insertion Blocks 4 and 5 land in the same code-fence region per R2's spec, in which case total = 10. Final shape depends on R2's block enumeration.

---

## 7. Known Gotchas

### Gotcha 1: Edits are INSIDE a markdown code fence

The target file `hypothesis-card-template.md` contains a code-fenced template (typically ```` ```markdown ... ``` ````). The Insertion Blocks from R2's spec are inserted INSIDE this fence — they are part of the rendered template, not file-level markdown. The `Edit` tool can edit content inside fences without issue (it does exact-string replacement). The task builder should NOT add markdown escape logic; the `old_string`/`new_string` from R2's spec already account for the fence context.

### Gotcha 2: `make verify-sync` FAILS if `.claude/` mirror is stale

[CODE-VERIFIED — `Makefile:348-353`] The script exits 1 with `❌ Drift detected! Run 'make sync-dev' to fix...` if any file in `src/superclaude/` differs from `.claude/`. The task MUST run `make sync-dev` BEFORE `make verify-sync`. Reversing the order will cause Phase 2 to fail on Item 7 (verify-sync before sync) — the task builder must order items 7 (`sync-dev`) then 8 (`verify-sync`).

### Gotcha 3: Markdownlint `--fix` may modify the file

[CODE-VERIFIED — `.pre-commit-config.yaml:75` `args: ['--fix']`] The markdownlint hook runs with `--fix`, meaning it may auto-modify the edited file (e.g., insert blank lines around headings, normalize bullet style). If `--fix` makes changes, the file is "modified by hook" and pre-commit returns non-zero. Item 9 should detect this and re-run sync-dev + verify-sync to propagate the fix. (Alternative: run with `--no-fix` to detect-only, but the project convention runs `--fix`, so embrace that and re-mirror.)

### Gotcha 4: No explicit line-length rule discovered

[UNVERIFIED] No `.markdownlint.json`, `.markdownlint.yaml`, or `.markdownlintrc` was found in the project (would require explicit check). markdownlint-cli defaults to enabling MD013 (line-length 80) unless overridden. The task builder may want to add a final read-check after Item 9 to confirm no line-length warnings, but since `--fix` is auto-applied, the most pragmatic stance is: if Item 9 returns 0, lint is satisfied.

### Gotcha 5: Pre-commit `block-claude-generated-mirrors` hook

[CODE-VERIFIED — `.pre-commit-config.yaml:102-109`] The local hook `block-claude-generated-mirrors` will REJECT any commit that stages `.claude/{skills,agents,commands,hooks,templates}/*` files. The task must ensure that when the user commits, only `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` is staged. `git add .claude/` would trip this hook. (This is a separate concern from sync-dev — verify-sync will pass even though `.claude/` is gitignored; the hook only blocks staging `.claude/` paths.)

---

## Summary

- **Template choice:** Template 01 (Generic). The task is a fully-specified, linear, atomic-per-block edit + verification chain — no discovery, no handoffs, no aggregation. Template 02's Section L (intra-task handoffs) adds no value here.
- **Workflow commands (verbatim from Makefile):** `make sync-dev` (Makefile:109), `make verify-sync` (Makefile:166). Both must run in that order; verify-sync exits 1 on drift.
- **Markdownlint gate:** Pre-commit hook `markdownlint` (markdownlint-cli@v0.38.0) with `--fix`, declared at `.pre-commit-config.yaml:70-82`. Recommended task command: `pre-commit run markdownlint --files src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md`. The `\.dev/.*` exclusion in the hook means the **task file itself** is not linted; the **target file** is.
- **Source-of-truth rule:** Edit `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md`; never edit the `.claude/` mirror. CLAUDE.md lines 141-156 and user memory `feedback_claude_dir_gitignored` both enforce this.
- **Precedent:** No Quick-tier single-file-edit Template-01 precedent found in `.dev/tasks/done/`. Existing precedents (e.g., TASK-RF-20260517-213436) use the same `make sync-dev`/`make verify-sync` commands but in complex multi-phase contexts. The task builder will establish the Quick-tier pattern; the cited commands are validated convention.
- **Recommended structure:** 3 phases / ~11 items: Phase 1 (6 edit items — 1 baseline read + 5 insertion blocks); Phase 2 (3 verification items — sync-dev, verify-sync, markdownlint); Phase 3 (2 completion items — final QA, status update).
- **Key gotcha:** `make sync-dev` MUST precede `make verify-sync` or Phase 2 fails. Markdownlint `--fix` may modify the file; if so, re-run sync-dev + verify-sync. The pre-commit `block-claude-generated-mirrors` hook will reject `.claude/` paths from being committed — only stage `src/` paths.
