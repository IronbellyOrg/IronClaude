# Research: MDTM Template Selection + Sync/Lint Conventions — Change A

**Track:** 1 of 4 (Change A — escalation-rubric.md formula update)
**Topic type:** Template & Examples + Conventions
**Scope:** MDTM Template 01 + Makefile sync targets + pre-commit config + Change B precedent
**Status:** Complete
**Date:** 2026-05-27

---

## 1. Template Selection Rationale (Template 01 vs 02)

### Recommendation: **Template 01 (Generic Task)**

[CODE-VERIFIED] `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.claude/templates/workflow/01_mdtm_template_generic_task.md`

**Rationale (specific to Change A):**

1. **Documentation-only edit** — Change A modifies a single markdown file (`src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md`). No source code, no tests, no agent definitions. Per task `research-notes.md` line 64: `TESTING_REQUIREMENTS: NONE`.
2. **Spec fully known up front** — All paste-ready content (new dimension row, replaced formula line, Verdict-direction cap table, cross-tab table, new escalation rule) is captured in the proposal at `CROSS-ENV-PROPOSAL-MERGED.md` L43-109 (research-notes.md line 16). Researcher 1 (`spec-extraction`) extracts the paste-ready blocks; Researcher 2 (`target-file-state`) captures byte-level anchor strings; no discovery phase needed.
3. **No conditional logic, no parallel subagents, no test-then-fix loop** — Each phase feeds linearly into the next (edit → sync → verify-sync → lint → final QA). Template 02's Section L (intra-task handoff patterns) is not required.
4. **Quick/Standard tier; FINAL_ONLY QA gate** — Per research-notes.md line 62: `QA_GATE_REQUIREMENTS: FINAL_ONLY (matches Change B precedent — no per-phase QA agent spawning required)`. Template 01's B2 self-contained item pattern is sufficient.
5. **Direct precedent: Change B used Template 01 successfully** — The shipped task at `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.dev/tasks/done/TASK-RF-20260527-022700-change-b-hypothesis-card-schema/TASK-RF-20260527-022700-change-b-hypothesis-card-schema.md` is 353 lines, used Template 01 (frontmatter line 31 references `src/superclaude/templates/workflow/01_mdtm_template_generic_task.md`), shipped as PR #89, and the same builder/executor pipeline produced a clean PASS on `make sync-dev`, `make verify-sync`, and the markdownlint hook.

### Caveat for Change A vs Change B

Change A edits are NOT purely additive — they mix INSERT and REPLACE (per research-notes.md line 26):

- **REPLACE** the Evidence-grounding 1.0 anchor cell (proposal diff L57)
- **REPLACE** the formula line at L19 (proposal diff L64-65)
- **INSERT** the Verdict-direction modifier block
- **INSERT** the cross-tab section (6×6 table)
- **INSERT** a 5th sub-bullet under § 3 (escalation rule for `source_only_dynamic_claim`)

Template 01's B2 pattern accommodates both insert and replace via the Edit tool's `old_string`/`new_string` semantics; this does NOT change the template choice, only the per-item `old_string` capture rigor (Researcher 2's responsibility).

---

## 2. Sync-Dev + Verify-Sync Workflow (Verbatim from Makefile)

### `sync-dev` target

[CODE-VERIFIED] `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/Makefile:108-163`

Header comment (L108):

```text
# Sync src/superclaude/{skills,agents} → .claude/{skills,agents} for local dev
```

Target declaration (L109): `sync-dev:`

Recipe key behavior (verified against L109-L163):

- **L110:** prints `🔄 Syncing src/superclaude/ → .claude/ for local development...`
- **L111:** `@mkdir -p .claude/skills .claude/agents`
- **L112-125:** walks `src/superclaude/skills/*/`, skips `__*` dirs, mirrors each skill that has a `SKILL.md` or `skill.md` into `.claude/skills/<name>/`, copying every file except `__init__.py` and `__pycache__`. This is the block that mirrors the Change A target file at `src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` → `.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md`.
- **L126-130:** copies `src/superclaude/agents/*.md` (except `README.md`) to `.claude/agents/`. (Cross-reference: `src/superclaude/agents/confidence-calibrator.md` per research-notes.md line 15 is read-only for Change A, but will be mirrored on every sync regardless.)
- **L131-136:** copies `src/superclaude/commands/*.md` to `.claude/commands/sc/`.
- **L137-143:** copies `src/superclaude/hooks/scripts/*.sh` to `.claude/hooks/` with `chmod +x`.
- **L148-157:** copies `src/superclaude/templates/**` (excluding `agent-memory/` and `__pycache__`) to `.claude/templates/`.
- **L158-163:** success-path summary output:

  ```text
  ✅ Sync complete.
     Skills:    N directories
     Agents:    N files
     Commands:  N files
     Hooks:     N files
     Templates: N files
  ```

**Exit code on success:** 0 (no explicit exit; Make exits 0 if all `cp` succeed).
**Exit code on failure:** non-zero if any `cp` fails (e.g., write-protected `.claude/`).

**Command the task should run:** `make sync-dev` [CODE-VERIFIED — Makefile:109 target declaration]

### `verify-sync` target

[CODE-VERIFIED] `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/Makefile:165-`

Header comment (L165):

```text
# Verify src/superclaude/ and .claude/ are in sync (CI-friendly, exits 1 on drift)
```

Target declaration (L166): `verify-sync:`

Recipe key behavior (verified against L166-end):

- **L167:** prints `🔍 Verifying src/superclaude/ ↔ .claude/ sync...`
- **L168:** initializes `drift=0`.
- **L171-187:** walks `src/superclaude/skills/*/` and for each:
  - If the matching `.claude/skills/<name>/` directory is missing → prints `❌ MISSING in .claude/skills/: <name>` and sets `drift=1`.
  - Otherwise runs `diff -rq --exclude='__init__.py' --exclude='__pycache__' <src_dir> <claude_dir>`; if non-empty, prints `⚠️  DIFFERS: <name>` followed by the diff lines (indented), sets `drift=1`. If empty, prints `✅ <name>`.
- **L188+:** walks `.claude/skills/*/` in reverse direction; flags any `.claude/` skill missing from `src/superclaude/skills/` or any `.claude/skills/<name>/` that lacks a `SKILL.md`/`skill.md` (i.e., not a real skill, must be moved out).
- Performs identical bidirectional checks for `agents/`, `commands/`, `hooks/`, and `templates/`.
- Final block: if `drift=1`, prints `❌ Drift detected! Run 'make sync-dev' to fix...` and runs `exit 1`. Otherwise prints success and exits 0.

**Exit codes:** 0 (in sync), 1 (drift detected).

**Diff pattern used:** `diff -rq --exclude='__init__.py' --exclude='__pycache__'` (recursive, brief output, excludes Python bytecode caches).

**Recovery path on drift:** Re-run `make sync-dev` (per the error message text) then re-run `make verify-sync`. Change B's task executor documented one successful invocation of this recovery path in its execution log.

**Command the task should run:** `make verify-sync` [CODE-VERIFIED — Makefile:166 target declaration]

**Note on relevance to Change A:** The Change A target file `src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` is a skill ref file (under `src/superclaude/skills/`, NOT under `src/superclaude/templates/`). It is covered by the skill-mirror block (L112-125 in `sync-dev`, L171-187 in `verify-sync`).

---

## 3. Markdownlint Hook

[CODE-VERIFIED] `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.pre-commit-config.yaml:70-82`

Verbatim hook configuration:

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

Field-by-field capture:

- **Repo URL:** `https://github.com/igorshubovych/markdownlint-cli`
- **Hook version (rev):** `v0.38.0`
- **Hook id:** `markdownlint` (L74)
- **Args:** `['--fix']` (L75) — the hook AUTO-MODIFIES the file when lint violations are auto-fixable (e.g., trailing whitespace, missing blank lines around headings, list-style normalization). If `--fix` makes changes, pre-commit returns non-zero with `files were modified by this hook`; a re-run on the now-fixed file then exits 0.
- **Exclude regex (verbose-x mode, L76-82):**

  ```text
  (?x)^(
    CHANGELOG\.md|
    .*node_modules.*|
    .*\.min\.md$|
    \.dev/.*
  )$
  ```

  - `CHANGELOG.md` — excluded.
  - `.*node_modules.*` — excluded.
  - `.*\.min\.md$` — minified markdown excluded.
  - `\.dev/.*` — **this is critical for Change A**: the task file itself lives under `.dev/tasks/to-do/TASK-RF-track-1-change-a-rubric-formula-20260527-044000/`, so it is NOT linted by the hook. However, the **target file** at `src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` lives under `src/`, NOT under `.dev/`, so it IS subject to the markdownlint hook.

**Recommended verification command for the task:**

```text
pre-commit run markdownlint --files src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
```

This runs ONLY the markdownlint hook against the single edited file (faster than `pre-commit run --all-files`) and respects the same `--fix` configuration.

**Important `--fix` consequence:** If the hook modifies the file, the `.claude/` mirror becomes stale → re-run `make sync-dev` then re-run `make verify-sync` before re-running the lint command. Change B documented this in its Step 2.3 (per the done-task body, L238).

---

## 4. `block-claude-generated-mirrors` Hook

[CODE-VERIFIED] `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.pre-commit-config.yaml:98-109`

Verbatim hook configuration:

```yaml
# AC11 / R-017 / T01.20 — source-of-truth discipline gate
# Rejects generated `.claude/` mirrors on the commit path. Full mirror drift
# remains available via `make verify-sync`, but pre-commit must not require
# staging generated mirrors when this repository edits its own src/ sources.
- repo: local
  hooks:
    - id: block-claude-generated-mirrors
      name: Block generated .claude mirror commits (AC11)
      entry: scripts/precommit_block_claude_mirrors.sh
      language: script
      pass_filenames: false
      files: '^\.claude/(skills|agents|commands|hooks|templates)/'
```

Field-by-field capture:

- **Hook id:** `block-claude-generated-mirrors` (L104)
- **Name:** `Block generated .claude mirror commits (AC11)` (L105)
- **Entry script:** `scripts/precommit_block_claude_mirrors.sh` (L106)
- **Trigger pattern (`files`):** `^\.claude/(skills|agents|commands|hooks|templates)/` (L109) — the hook fires only when one of these five subtree paths under `.claude/` is in the staged change set.

**Script behavior** [CODE-VERIFIED] `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/scripts/precommit_block_claude_mirrors.sh:1-23`:

```bash
#!/usr/bin/env bash
set -euo pipefail

mapfile -t generated_paths < <(
  git diff --cached --name-only --diff-filter=ACMR -- \
    '.claude/skills' \
    '.claude/agents' \
    '.claude/commands' \
    '.claude/hooks' \
    '.claude/templates'
)

if [ "${#generated_paths[@]}" -eq 0 ]; then
  exit 0
fi

printf '❌ Generated .claude mirrors must not be committed.\n'
printf '   Edit src/superclaude/ first, run make sync-dev for local mirrors, and stage only src/.\n\n'
printf 'Staged generated mirror paths:\n'
printf '  - %s\n' "${generated_paths[@]}"
printf '\nAllowed exception: .claude/settings.json only.\n'
exit 1
```

**Blocked paths:** `.claude/skills/`, `.claude/agents/`, `.claude/commands/`, `.claude/hooks/`, `.claude/templates/`.

**Allowed exception:** `.claude/settings.json` only (per the error message text and per user memory `feedback_claude_dir_gitignored.md`: *"Never commit `.claude/skills,commands,agents,hooks` — those are sync-dev output of `src/superclaude/`. Only `.claude/settings.json` is tracked."*).

**Why it exists:** Per the comment block at L98-101: `sync-dev` output is gitignored; committing it would create source-of-truth ambiguity (which is canonical, `src/` or `.claude/`?). The hook is the enforcement gate; gitignore is the prevention layer; the source-of-truth rule in CLAUDE.md is the doctrinal layer.

**Applied to Change A:** When the executor finalizes the task and prepares to commit, it MUST stage only `src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` — NEVER `.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md`. `git add .claude/` would trip this hook.

---

## 5. Source-of-Truth Rule + Execution Invariants

### Source-of-truth rule

Per project CLAUDE.md and user global CLAUDE.md (both in session context):

1. **Edit `src/superclaude/`, never `.claude/`** — `src/superclaude/` is the canonical source of truth for all distributable skills, agents, commands, templates, and hooks. `.claude/` is the dev-runtime mirror, refreshed by `make sync-dev`.
2. **Workflow:** edit `src/` → `make sync-dev` → `make verify-sync` (exit 0) → run lint → commit only `src/` changes.
3. User memory `feedback_hooks_source_of_truth.md`: *"Never edit `~/.claude/` or `<project>/.claude/` directly; edit `src/superclaude/` then `make sync-dev`."*

### Execution invariants for Change A

- **INVARIANT 1:** All edits land in `src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md`. NEVER in `.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md`.
- **INVARIANT 2:** `make sync-dev` MUST run BEFORE `make verify-sync` (verify-sync fails on stale mirror — see Gotcha 1 below).
- **INVARIANT 3:** Markdownlint `--fix` may modify the file. If it does, re-run `make sync-dev` and `make verify-sync` before re-running the lint command, then verify the second lint pass returns exit 0.
- **INVARIANT 4:** If pre-commit's auto-fixer modifies staged files, the commit aborts. The user (or executor) must re-stage the modified file then re-commit. This is normal pre-commit behavior, not a hook bug.
- **INVARIANT 5:** Staged changes for commit must include ONLY `src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md`. Staging any `.claude/skills|agents|commands|hooks|templates/*` path will trip `block-claude-generated-mirrors` and abort the commit.

---

## 6. Known Gotchas (Change A — specific)

### Gotcha 1: `sync-dev` ordering — must precede `verify-sync`

[CODE-VERIFIED — Makefile final block in `verify-sync` recipe sets `exit 1` with `❌ Drift detected! Run 'make sync-dev' to fix...` when any `diff -rq` returns non-empty.] If the executor runs `make verify-sync` before `make sync-dev`, it WILL fail with drift detected (because `.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` still reflects the pre-edit state). Phase 2 of the eventual task file MUST order items: `sync-dev` first, `verify-sync` second.

### Gotcha 2: Markdownlint `--fix` may modify the file

[CODE-VERIFIED — `.pre-commit-config.yaml:75` `args: ['--fix']`] The hook auto-modifies on:

- Missing blank lines around headings (MD022)
- Trailing whitespace (MD009)
- Multiple consecutive blank lines (MD012)
- List style normalization (MD004, MD030)
- Table padding consistency (MD058 if enabled)

Change A inserts new tables (the 6×6 cross-tab + the Verdict-direction cap table) and new headings — both prime candidates for `--fix` to touch. The executor MUST handle the `files were modified by this hook` exit-1-on-first-pass case by re-running `sync-dev`, `verify-sync`, and re-invoking the lint command for a clean second-pass exit 0. Change B's Step 2.3 (per the done-task body L238) encodes this exact recovery loop and is a direct precedent.

### Gotcha 3: `block-claude-generated-mirrors` blocks staging `.claude/` paths

[CODE-VERIFIED — `.pre-commit-config.yaml:102-109` + `scripts/precommit_block_claude_mirrors.sh:1-23`] Staging anything under `.claude/skills|agents|commands|hooks|templates/` aborts the commit. This is separate from gitignore — even if `git add -f .claude/skills/...` succeeds (forcing past gitignore), the pre-commit hook still rejects it. The executor must use `git add src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` explicitly; avoid `git add .` or `git add .claude/`.

### Gotcha 4: `pre-commit` may not be on PATH — install via `uv pip install pre-commit`

[CODE-VERIFIED via Change B execution log] Per Change B's done-task body at L275: *"`pre-commit` was not on PATH in this worktree. Resolved by `uv pip install pre-commit` then running via `uv run pre-commit run markdownlint --files ...`. Tool-installation step, not a content blocker."*

The Change A task should anticipate this by either:

- (a) Including a precondition check in Phase 2 (e.g., `command -v pre-commit || uv pip install pre-commit`), OR
- (b) Invoking via `uv run pre-commit run ...` directly so UV resolves the executable from the project's `.venv`.

Change B chose (b) and it worked cleanly.

### Gotcha 5: Cross-environment line-number drift (Change-A-specific)

Per research-notes.md line 27: *"proposal's 'line 19' formula reference and 'lines 11-17' table reference are V1 source state. The current file may have drifted. Researcher MUST verify line numbers byte-by-byte against the actual current file."* This is Researcher 2's (`target-file-state`) responsibility, NOT a template/convention issue — flagged here for cross-track awareness so the eventual task file's `old_string` candidates reflect the CURRENT file state, not the proposal's snapshot state.

### Gotcha 6: Worktree CWD discipline

[CODE-VERIFIED via Change B done-task body L230] When the task runs inside a worktree at `.claude/worktrees/<name>/`, the executor must `cd` to the worktree root (the directory containing `Makefile`, `src/`, and `.dev/`) before invoking `make sync-dev` / `make verify-sync`. Hardcoding absolute paths breaks because the worktree path differs from the main checkout. Change B's Step 2.1 (L230) prose explicitly states: *"do NOT hardcode an absolute path because this task may run inside a worktree at `.claude/worktrees/<name>/` or in the main checkout"*.

---

## 7. Change B Precedent

### Change B's three research files

[CODE-VERIFIED via `ls /config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.dev/tasks/done/TASK-RF-20260527-022700-change-b-hypothesis-card-schema/research/`]

1. `01-target-file-state.md` — byte-level state of the target file, unique-match `old_string` candidates for all insertion anchors, code-fence boundary analysis, verbatim surrounding-context capture.
2. `02-change-b-spec-extraction.md` — paste-ready Insertion Blocks (with `+` stripped from the proposal diff), REQUIRED/OPTIONAL classification, final ordering rules, enum-count discrepancy notes, verbatim MUST/MUST NOT statements.
3. `03-template-and-conventions.md` — Template 01 selection rationale, verbatim Makefile target locations for `sync-dev` and `verify-sync`, pre-commit markdownlint hook configuration, source-of-truth rule, known gotchas.

**Change A mirrors this 3-file structure exactly:**

- Track 1 Researcher 1 = spec-extraction → `research/01-change-a-spec-extraction.md`
- Track 1 Researcher 2 = target-file-state → `research/02-target-file-state.md`
- Track 1 Researcher 3 = template-conventions (this file) → `research/03-template-and-conventions.md`

### Change B's executed task file structure

[CODE-VERIFIED via reading `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.dev/tasks/done/TASK-RF-20260527-022700-change-b-hypothesis-card-schema/TASK-RF-20260527-022700-change-b-hypothesis-card-schema.md` — 353 lines]

Frontmatter (L1-45):

- `template_schema_doc: "src/superclaude/templates/workflow/01_mdtm_template_generic_task.md"` (L31) — explicit Template 01 reference.
- `type: "📝 Documentation"`, `task_type: static`, `assigned_to: "rf-task-executor"`.
- `related_docs` cites Makefile L109/L166 and `.pre-commit-config.yaml:70-82` + `:102-109` directly in the frontmatter — Change A should follow the same pattern.

Body structure:

- **Task Overview** (L49-55) — narrative of what the additive edits do, expected line-count range, sync + lint chain.
- **Key Objectives** (L57-64) — 4 numbered objectives mirroring the spec.
- **Prerequisites & Dependencies** (L66-93) — parent task, blocking dependencies, what THIS task blocks, the three research files, frontmatter update protocol.
- **Execution Context** (L95+) — references block.
- **Phase 1: Edit target file** (one item per insertion block, ~6 items based on the 5 blocks plus a baseline-confirm item).
- **Phase 2: Sync + verify-sync + lint** (L224-238) — 3 items: `make sync-dev` (Step 2.1, L230), `make verify-sync` (Step 2.2, L234), `pre-commit run markdownlint` (Step 2.3, L238). Each item is a single-paragraph self-contained prompt with embedded R3-reference, embedded gotcha awareness, and embedded recovery-loop logic.
- **Phase 3: Final structural verification (QA gate — executor-performed, per FINAL_ONLY)** (L240-246) — single Step 3.1 item that re-reads the target file end-to-end and verifies (a) through (g) structural invariants. The header text at L242 explicitly notes: *"This is the task's final QA gate per the BUILD_REQUEST's `QA_GATE_REQUIREMENTS: FINAL_ONLY` directive. The executor performs the verification directly — no rf-qa spawning is required."*
- **Post-Completion Actions** (L248+) — 4 items: verify outputs exist via Glob + line-count check + diff check between src/ and .claude/ mirror; testing skip log entry (per `TESTING_REQUIREMENTS: NONE`); Task Summary content creation; frontmatter status flip to "🟢 Done" + Execution Log entry.
- **Task Log / Notes** with subsections: Task Summary, Risks/Known Limitations/Open Questions (carried forward from builder), Execution Log, per-Phase Findings, Follow-Up Items Identified, Deviations from Process.

### FINAL_ONLY QA mode pattern

Change B used FINAL_ONLY (no per-phase rf-qa spawning, only an executor-performed final structural check). Rationale, per Change B's Phase 3 header (L242):

- Per-task-file QA gates (A.10/A.10.5 in the task-builder skill) already gated the task file content at build time.
- For a single-file additive markdown edit, structural verification (heading order, fence integrity, char encoding, line-count range) is bounded enough that the executor can do it reliably in one item.
- No external rf-qa agent spawn cost or coordination overhead.

**Change A should use the same FINAL_ONLY mode** per research-notes.md L62 (`QA_GATE_REQUIREMENTS: FINAL_ONLY (matches Change B precedent)`). The executor's final structural verification item should check:

- (a) The 5 dimensions → 6 dimensions table now includes the new row.
- (b) The formula line at (current) L19 is replaced with the `min(arithmetic_mean(all_six_dimensions), evidence_grounding + 0.30, runtime_check + 0.30)` text.
- (c) The Verdict-direction modifier subsection is present and contains the REFUTE/REJECT → 0.70 and AFFIRM → 0.84 caps.
- (d) The 6×6 cross-tab section is present with the `[V2 merged]` provenance suffix.
- (e) The 5th sub-bullet under § 3 (Escalation Decision) is present for `source_only_dynamic_claim`.
- (f) Em-dashes are U+2014, `≤` is U+2264, `∈` is U+2208 (consistent with Change B's encoding checks).
- (g) Total line count is in the expected post-edit range (Researcher 2 will compute this from current baseline + spec deltas).

### Patterns that worked well in Change B (replicate for Change A)

1. **One self-contained item per insertion/replacement block** with the FULL `old_string` and FULL `new_string` embedded inline in the item prose, AND embedded gotcha awareness (e.g., "ensuring the `old_string` matches uniquely…").
2. **Phase 2 items embed R3 references inline** — e.g., Step 2.1 says *"Read the file `03-template-and-conventions.md` … Section 2 … to confirm the verbatim Makefile target behavior"* before running the command. This guards against session-rollover context loss.
3. **Recovery loops are encoded as IF-THEN prose inside the item** — e.g., Step 2.2 says *"If the command exits non-zero with `Drift detected`, re-run Step 2.1 exactly ONCE… then re-run this command and re-check exit code; if still non-zero, log the specific drift output…"*
4. **Post-completion verification uses Bash diff + wc -l + Glob** to confirm the mirror matches the source and the line-count is in range, not a separate rf-qa spawn.
5. **Risks/Known Limitations carried forward verbatim** from the builder into the task body (L287-298 in Change B), so the executor sees them inline rather than having to re-discover them.
6. **The execution log captures the `pre-commit not on PATH` resolution** (L275) — Change A should expect the same and either pre-install or invoke via `uv run pre-commit ...`.

---

## Summary

**Template choice:** Template 01 (Generic Task) — same as Change B / PR #89. Confirmed fit: documentation-only edit, spec fully known, no discovery phase, no parallel subagents, no test-fix loops; the additive INSERT + cell-level REPLACE mix is handled by Edit tool semantics without requiring Template 02's Section L handoff patterns.

**Makefile targets verified:** `sync-dev` declared at `Makefile:109` (recipe L109-L163, success path prints `✅ Sync complete.` and per-component counts, exit 0 on success); `verify-sync` declared at `Makefile:166` (recipe L166+, uses `diff -rq --exclude='__init__.py' --exclude='__pycache__'` bidirectionally across skills/agents/commands/hooks/templates, exit 1 on drift with `❌ Drift detected! Run 'make sync-dev' to fix...`).

**Pre-commit hooks verified:** `markdownlint` (`.pre-commit-config.yaml:70-82`, `igorshubovych/markdownlint-cli@v0.38.0`, `args: ['--fix']`, excludes `\.dev/.*` so the task file is NOT linted but the target under `src/` IS); `block-claude-generated-mirrors` (`.pre-commit-config.yaml:102-109`, local hook calling `scripts/precommit_block_claude_mirrors.sh` to reject any staged `.claude/{skills,agents,commands,hooks,templates}/*` paths, allows only `.claude/settings.json` as exception).

**Execution invariants:** Edit `src/` only; `sync-dev` before `verify-sync`; `--fix` may modify file → re-sync; pre-commit auto-fix aborts commit → re-stage and re-commit; stage `src/` paths only.

**Six gotchas captured:** (1) sync ordering, (2) `--fix` modifies file, (3) `block-claude-generated-mirrors` blocks `.claude/` staging, (4) `pre-commit` may need `uv pip install pre-commit`, (5) Change-A-specific line-number drift from proposal V1 baseline, (6) worktree CWD discipline.

**Change B precedent:** Three research files (`01-target-file-state.md`, `02-change-b-spec-extraction.md`, `03-template-and-conventions.md`); 353-line executed task file using Template 01 with 3 execution phases plus Post-Completion Actions; FINAL_ONLY QA mode with executor-performed structural check (no rf-qa spawning); shipped as PR #89; clean PASS on all gates. Change A should mirror this structure 1:1, adjusting only the per-item content for the rubric formula update.
