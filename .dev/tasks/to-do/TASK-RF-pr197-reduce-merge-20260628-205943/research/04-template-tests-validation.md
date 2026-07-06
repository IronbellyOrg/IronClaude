# R4 Research — Template, Examples, Tests, Validation-Commands

**Agent:** R4 (Template / Examples / Tests / Validation-Commands)
**Task:** PR #197 reduce-then-merge tasklist build
**CWD:** /config/workspace/IronClaude/.dev/worktrees/pr197-remediation
**Date:** 2026-06-28
**Status:** In progress

---

## 1. MDTM Template 02 — Rules the generated tasklist must follow

**Source:** `.claude/templates/workflow/02_mdtm_template_complex_task.md` PART 1 (lines 63–1442; PART 1 ends, PART 2 clean template follows). Read lines 1–705 directly; remaining sections grepped.

### Frontmatter field set (template lines 1–61, verbatim keys)
The base template REQUIRES this exact key set (in order):
`id, title, description, version, status, type, priority, created_date, updated_date, assigned_to, autogen, autogen_method, coordinator, parent_doc, parent_task, depends_on[], spec_path, reflect_pre{verdict,coverage_pct,depth,tcs,run_id,report,reviewed_at}, reflect_post, related_docs[], related_prd, related_tdd, tags[], template_schema_doc, estimation, sprint, due_date, start_date, completion_date, blocker_reason, ai_model, model_settings, review_info{last_reviewed_by,last_review_date,next_review_date}, task_type`.

- `status` enum (line 6): `"🔵 Backlog" | "🟡 To Do" | "🟠 Doing" | "🔴 Blocked" | "🟢 Done" | "⚪ Cancelled"`.
- `type` enum (line 8) includes `"🐛 BugFix"`, `"🔧 Refactor"` (used by rfmerge), `"⚙️ Maintenance"`, `"🧩 Integration"`, etc.
- `priority` enum (line 10): `"🔥 Highest" | "🔼 High" | "▶️ Medium" | "🔽 Low" | "🧊 Lowest"`.

### `start_commit` / `executor_model_class` — NOT in the base template
- `grep "start_commit\|executor_model_class"` over the template returns **zero hits**. These are **task-builder-injected** frontmatter fields, added immediately AFTER `depends_on` / `spec_path` and BEFORE `reflect_pre`.
- Confirmed by the most recent completed complex tasklist `TASK-RF-tasklist-rfmerge-20260619-041423.md` lines 20–21:
  ```
  spec_path: "..."
  start_commit: "300c06a6d53287893a446db8e859f5f1bc5434d8"
  executor_model_class: "sonnet"
  reflect_pre:
  ```
- **Builder action:** populate `start_commit` with the current `feat/rf-harness-sync` HEAD SHA at build time and `executor_model_class` with the chosen executor tier (e.g. `sonnet`).

### A3 — Complete Granular Breakdown (lines 108–112)
Break EVERY phase into atomic, verifiable checklist items; an individual item per file/component/iteration; NO bulk operations; exact file paths + measurable outcomes.

### A4 — Iterative Process Structure (lines 114–133)
For any multi-item process: pre-enumerate ALL items in an initial step, one checklist item per item, incremental update after each, consolidation step ONLY after all complete. Pattern = Step X.1 enumerate → Step X.2 per-item → Step X.3 consolidate.

### B2 — Self-Contained Checklist Item (lines 159–166)
Every item is a COMPLETE, standalone prompt (ONE full paragraph, B3 line 167) embedding all 6 elements:
1. Context reference WITH WHY (what file(s) to read + why);
2. Action WITH WHY;
3. Output specification (exact path/name/content/template);
4. Integrated verification — an "ensuring..." clause (no fabrication, 100% source-derived, document negative evidence);
5. Evidence on failure ONLY (log a blocker to `### Phase [N] Findings` in `## Task Log / Notes` only if blocked);
6. Explicit completion gate — "...then mark this item complete. Once done, mark this item as complete."
- FORBIDDEN (B5, lines 181–200): standalone "read context" items, missing context reference, multi-line/bulleted items, **separate verification/confirmation items** (verification is integrated via "ensuring..."), parent-with-child checkboxes.

### Checklist structure (Section E, lines 295–405)
Flat checkboxes only (no nesting); `**Step X.Y:**` bold headers for grouping (NEVER a checkbox next to a step number); summary/parent checkboxes come AFTER their components, never before; strictly top-to-bottom, no backward references.

### Anti-orphaning — completion items in the FINAL phase (Post-Completion Actions)
The template encodes completion as a dedicated final `## Post-Completion Actions` phase (PART 2, e.g. rfmerge "Phase 9: Post-Completion Actions"), NOT scattered. Required final items per I13 (lines 616–621) + I17 (lines 675–686):
- A verify-all-items-checked item (line 1425) — Glob-confirm every output file exists;
- A run-tests-if-code-modified item (line 1427);
- A `### Task Summary` creation item (line 1439);
- A frontmatter-finalize item: set `status: "🟢 Done"`, `completion_date`, `updated_date` + append `### Execution Log` entry (line 1441) — this MUST be the LAST item.
- I11 (lines 605–607): the FIRST executable item sets `status: "🟠 Doing"` + `start_date` and logs to `### Execution Log` (rfmerge line 1323 pattern).

### Task Log section (lines 1443+)
Mandatory `## Task Log / Notes 📋` at the bottom containing `### Task Summary`, `### Open Questions`, `### Execution Log`, and per-phase `### Phase [N] Findings` subsections (the blocker sinks referenced by B2 element 5).

### I18 — Testing requirement for code-modifying tasks (lines 688–697)
Because this task modifies source (`src/superclaude/skills/.../SKILL.md` + the reflect/task-builder edits), the tasklist MUST include explicit test-execution items (L3 pattern) specifying command + pass criteria + results-capture path.

---

## 2. Existing examples — house style

**`.dev/tasks/to-do/` contents (20 entries):** ISSUE-pipeline-one-shot-output.md, PRD_TASK_MANAGEMENT_SYSTEM.md, TASK-pr-submit-defaults-20260616, TASK-RF-20260525-rf-team-lead-tavily-pathC, TASK-RF-20260603-031100, TASK-RF-fr-drs-runtime-surface-20260622-000600, TASK-RF-fr-rh2-headless-ensemble-20260620-024238, TASK-RF-merge-prompt-wiring-directive-20260525-160000, TASK-RF-pr197-reduce-merge-20260628-205943 (this build), TASK-RF-reflect-ac-hybrid-20260628-205715 (sibling build, mid-flight — no main .md yet), TASK-RF-reflect-d1d4-fix-20260623-192000, TASK-RF-reflect-post-gate-wiring-20260611-022409, TASK-RF-sprint-runlock-20260617-020000, TASK-RF-tasklist-rfmerge-20260619-041423, TASK-RF-tavily-mcp-0-2-x-20260623-010952, TASK-RF-uc2-reachability-20260620-025931, TASK-RF-uc2-reachability-gate-20260620-043410, TASK-STDIN-RECON-REMEDIATION-20260501, TASK-TDD-20260619-235400, TASK-TDD-20260621-124414.

**Cited reference tasklist:** `.dev/tasks/to-do/TASK-RF-tasklist-rfmerge-20260619-041423/TASK-RF-tasklist-rfmerge-20260619-041423.md` (status 🟢 Done; closest analog — a code-modifying src/superclaude task with a final test+lint+format+sync phase).

**House-style header skeleton (from grep of `^#{2,3}`):**
- `## Task Overview`
- `## Key Objectives`
- `## Prerequisites & Dependencies` → `### Parent Task & Dependencies`, `### Previous Stage Outputs (MANDATORY INPUTS)`
- `## Execution Context` → `### References`, `### Source Areas`, `### Key Constraints`, `### Handoff File Convention`, `### Frontmatter Update Protocol`
- `## Detailed Task Instructions` → `### Phase 1: …` … `### Phase N: …` (each phase a `### Phase N: <title>` header; steps as `**Step N.M:**` bold; items as `- [ ]`)
- `### Phase 8: Full Test Convergence + Lint + Format + Sync Verification` (the validation phase — directly relevant model for this task's step-3 validation phase)
- `### Phase 9: Post-Completion Actions`
- `## Task Log / Notes 📋` → `### Task Summary`, `### Open Questions`, `### Execution Log`, `### Phase N Findings`

**Note for the builder:** the main task file lives at `<task-dir>/<TASK-ID>.md` (filename == dir name), and `phase-outputs/` subdirs hold intermediate artifacts.
---

## 3. Validation-command verification (every command resolves as-written)

### Make targets (grep `^<target>:` in `Makefile` — all exist)
- `sync-dev:` (Makefile:109) — recipe: `@echo "🔄 Syncing src/superclaude/ → .claude/ …"; @mkdir -p .claude/skills .claude/agents; for skill_dir in src/superclaude/skills/*/ … cp …`. **MUTATES `.claude/`. Do NOT run in audit; run only as a real build step.**
- `verify-sync:` (Makefile:166) — recipe: `@echo "🔍 Verifying src/superclaude/ ↔ .claude/ sync…"; diff -rq … per skill; sets drift=1 on mismatch`. Read-only; the authoritative SoT gate. This is the **only** validation step the user mandated for the task-builder-clause step (R3's step 4).
- `lint:` (Makefile:48) — `lint: lint-architecture` then `@echo "Running linter…"; uv run ruff check .`. ⚠️ **GOTCHA (confirmed in rfmerge note 8.7, file line 809):** `make lint` runs `lint-architecture` FIRST and can exit non-zero on a PRE-EXISTING architecture error (e.g. `src/superclaude/commands/recommend.md has ## Activation but no matching skill directory: sc-recommend-protocol`) that is unrelated to this task's changes. The tasklist's lint item MUST scope the pass/fail judgment to `uv run ruff check <changed .py files>` and treat a pre-existing `lint-architecture` failure as out-of-scope (verify via `git diff <start_commit> HEAD -- <path>` is empty). Do NOT run/auto-fix it broadly.
- `format:` (Makefile:53) — `uv run ruff format .` — **WRITE-MODE, mutates. Never use the bare target; use `--check` (read-only) for validation.**

### markdownlint
- `.markdownlint.json` EXISTS (132 bytes): `{ "default": true, "MD024": {"siblings_only": true}, "MD013": false, "MD029": false, "MD036": false, "MD033": false }`.
- The repo uses **`markdownlint-cli`** (igorshubovych) via the pre-commit hook `id: markdownlint` (`.pre-commit-config.yaml:75`), rev `v0.38.0`, `args: ['--fix']` (auto-fixes in place). NOT markdownlint-cli2.
- **Exclude block (`.pre-commit-config.yaml:77-85`):** `CHANGELOG.md`, `node_modules`, `*.min.md`, **`\.dev/.*`**, `tests/swarm/fixtures/bare_review_v1/golden/.*`. → The generated task file under `.dev/` is EXEMPT from markdownlint; only the SKILL.md edits under `src/` are gated.
- All 6 target SKILL.md files exist (verified): `src/superclaude/skills/{operational-guide,readme,roadmap,task,tech-reference,tech-research}/SKILL.md`.
- **Binary availability (verified):** `markdownlint` and `markdownlint-cli2` are NOT on PATH; `pre-commit` is NOT on PATH; `npx` IS on PATH (`/config/.nvm/.../bin/npx`).
- **Single-line invocation for the 6 SKILL.md files** (config picked up automatically from repo-root `.markdownlint.json`):
  ```
  npx -y markdownlint-cli@0.38.0 src/superclaude/skills/operational-guide/SKILL.md src/superclaude/skills/readme/SKILL.md src/superclaude/skills/roadmap/SKILL.md src/superclaude/skills/task/SKILL.md src/superclaude/skills/tech-reference/SKILL.md src/superclaude/skills/tech-research/SKILL.md
  ```
  Add `--fix` to auto-correct (matches the pre-commit hook behavior). **Pre-commit hook id to cite in the tasklist: `markdownlint`** (runs automatically on staged `src/...SKILL.md` at commit). ⚠️ FLAG: since neither markdownlint nor pre-commit is installed in this worktree, the tasklist must either (a) rely on the commit-time pre-commit hook, or (b) use the `npx markdownlint-cli@0.38.0 …` form above; a bare `markdownlint …` command would NOT resolve here.

### `uv run pytest tests/cli/reflect -q` — RESOLVES
- `tests/cli/reflect/` exists. Collect-only (`--co`): **163 tests collected in 0.15s**, clean.
- `test_no_nesting_guard.py` PRESENT; `test_inline_directive.py` PRESENT (both confirmed in dir listing).

### `uv run pytest tests/swarm -q` — RESOLVES
- `tests/swarm/` exists. Collect-only: **2272 tests collected in 1.18s**, clean. (Large suite — collect-only used; full run is slow.)

### `uv run ruff format --check src/ tests/` — READ-ONLY (check mode), but NOISY
- Exit code **1** (verified: `uv run ruff format --check …; echo $? → 1`) because **104 files "would be reformatted"** (e.g. `tests/troubleshoot/test_hardening_*.py`), 956 already formatted. This is the documented worktree `.venv` ruff-version-vs-CI mismatch (memory `ruff_version_mismatch_worktree`). **FLAG/RECOMMENDATION:** the tasklist MUST scope any actual format fix to THIS task's changed `.py` files only (none expected — the 6 SKILL.md are `.md`, and reflect/task-builder edits may be `.md` too); it MUST NOT run write-mode `ruff format` broadly (would reformat 104 unrelated files). If a changed `.py` file is in scope, check just that file: `uv run ruff format --check <file.py>`.

### `tests/skills/test_task_builder_merge.py` — RESOLVES (reference only)
- Exists. Collect-only: **68 tests collected in 0.04s**, clean. (Per the user, step-4 validation is just `make verify-sync`; this test is the deeper reference selector if a task-builder behavioral check is wanted.)
---

## 4. PR hygiene (step 6)

### Remote (verified `git remote -v`)
```
origin	https://github.com/IronbellyOrg/IronClaude.git (fetch)
origin	https://github.com/IronbellyOrg/IronClaude.git (push)
```
✅ origin = the fork `IronbellyOrg/IronClaude`. No `upstream` remote present in this worktree.

### Behind-count (verified, read-only)
- `git rev-list --count HEAD..origin/master` → **0**. Branch `feat/rf-harness-sync` is NOT behind origin/master — **no rebase needed at audit time** (re-check at execution time).
- Current branch (verified `git branch --show-current`): `feat/rf-harness-sync`.

### Single-line commands for the tasklist
- Rebase-if-behind guard:
  ```
  git fetch origin && [ "$(git rev-list --count HEAD..origin/master)" -gt 0 ] && git rebase origin/master || echo "up to date"
  ```
  (Simpler split form if a one-liner conditional is undesired: run `git fetch origin`, then `git rev-list --count HEAD..origin/master`; if `>0`, run `git rebase origin/master`.)
- Push:
  ```
  git push origin feat/rf-harness-sync
  ```
- Auggie-review comment (verb confirmed via `gh pr comment --help` → "Add a comment to a GitHub pull request", `USAGE gh pr comment [<number>|<url>|<branch>] [flags]`):
  ```
  gh pr comment 197 --repo IronbellyOrg/IronClaude --body "auggie review"
  ```
  ✅ `gh pr comment` is the correct verb. (Per memory `reference_augment_review_triggers`: pushes do NOT trigger Augment; the `auggie review` comment is required after each push to re-arm the review.)

### PR URL confirmation (verified — gh IS authed as `ironbelly`)
- `gh pr view 197 --repo IronbellyOrg/IronClaude --json url,number,headRefName,state` →
  ```
  {"headRefName":"feat/rf-harness-sync","number":197,"state":"OPEN","url":"https://github.com/IronbellyOrg/IronClaude/pull/197"}
  ```
  ✅ PR #197 is OPEN, head = `feat/rf-harness-sync`, URL = `https://github.com/IronbellyOrg/IronClaude/pull/197` (correct fork owner `IronbellyOrg`, NOT `SuperClaude-Org`). The tasklist's PR-hygiene phase should re-run this `gh pr view` and assert the URL owner is `IronbellyOrg` before/after pushing.
---

## 5. Commands flagged as NOT resolving as-written (for builder correction)

1. **`markdownlint <files>` (bare) — DOES NOT RESOLVE in this worktree.** Neither `markdownlint` nor `markdownlint-cli2` nor `pre-commit` is on PATH. Use the `npx -y markdownlint-cli@0.38.0 <6 SKILL.md paths>` form (section 3) OR rely on the commit-time pre-commit hook `id: markdownlint`. Builder must NOT embed a bare `markdownlint …` invocation.
2. **`make lint` — RESOLVES but its pass/fail is UNRELIABLE for this task.** It runs `lint-architecture` first, which exits non-zero on a PRE-EXISTING, unrelated `recommend.md`/`sc-recommend-protocol` architecture mismatch (rfmerge note 8.7, file line 809). Builder must scope the ruff judgment to changed `.py` and treat a pre-existing `lint-architecture` failure as out-of-scope (prove via empty `git diff <start_commit> HEAD -- <path>`).
3. **`uv run ruff format --check src/ tests/` — RESOLVES but exits 1 with 104 noise files** (worktree ruff-version mismatch). Builder must scope format checks/fixes to this task's changed `.py` only and never run write-mode `ruff format` broadly.
4. **`make sync-dev` / `make format` — RESOLVE but MUTATE.** Correct as real build steps; must NOT be used as read-only validation. (`make verify-sync` is the read-only SoT check; it is NOT a pre-commit hook id — pre-commit only blocks `.claude/` mirrors via `block-claude-generated-mirrors`.)

All other commands (`make verify-sync`, `uv run pytest tests/cli/reflect -q`, `uv run pytest tests/swarm -q`, `git remote -v`, `git rev-list …`, `git push origin feat/rf-harness-sync`, `gh pr comment 197 …`, `gh pr view 197 …`) RESOLVE as-written and were exercised read-only above.

---
**Status: Complete**
