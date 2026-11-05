---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-implementSavedPr-20261104-230730
version: "1"
priority: Medium
created_date: "2026-11-04"
---

# Close the saved-reviewer-prompt gaps in /sc:implement

Source: ./source.md
Goal: `/sc:implement` tolerates blank-line and trailing-whitespace drift when FINAL compares a saved reviewer prompt with the template (rule A), defines a recovery path for a saved prompt that really differs (rule B: template-exact re-review, repeated `complete` line, unchanged move to `superseded-prompts/` with a README, FINAL treats that folder as history), pins both rules with regression tests, and records that the nine first-round prompts of the earlier guide-refactor package differ from the template only in blank lines.

## Constraints

- Rule changes go only in `src/superclaude/skills/sc-implement-protocol/refs/qa.md`, `src/superclaude/skills/sc-implement-protocol/refs/ledger.md` and `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md`, each with a byte-identical copy at the same relative path under `plugins/superclaude/skills/sc-implement-protocol/`. No other skill, command, agent or core file changes, and the reviewer template text (the fenced block under "## Subagent prompt (when not inline)" in `refs/qa.md`) does not change.
- A prompt-builder script and every other lesson in `docs/memory/reflect/deviation-patterns-OrcaCLICommandRefactor-Specs.md` are out of scope.
- Never stage `.claude/` contents. After editing `src/superclaude/`, run `make sync-dev`; `.claude/` stays unstaged.
- Installed primitives (the three refs above) must not tell an agent to read anything through a `src/superclaude/...` path.
- In `.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/`, only the new file `artifacts/prompt-template-check.md` is added; its prompts, ledger and every other file stay byte-unchanged.
- Scripts and evidence for this plan go under this package's `./artifacts/`.
- `.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `artifacts/` included. Staging is not committing; commit only when the user asks.

## Phase 1: Tolerate whitespace drift in the saved-prompt comparison

## Task 1: Add rule A to the FINAL saved-prompt comparison

Before any edit, save `git status --porcelain -- docs src plugins tests` as `./artifacts/t1-status-before.txt`. In `src/superclaude/skills/sc-implement-protocol/refs/qa.md`, section "## FINAL derived test", replace the bullet that begins "- Saved prompts: compare each `prompt-<k>-<j>.md` with the reviewer template" so that it says: FINAL compares the sequence of non-blank lines of each saved prompt outside the slots, with trailing whitespace removed, against the template's non-blank lines; a prompt that differs from the template only in blank lines or trailing whitespace is recorded as a note (cited `noted`) and is not `issues`; any changed, added, removed or reordered non-blank line outside the slots is `issues` (managed) or recorded in `FINAL:` evidence (legacy), as before. Use the exact phrase "differs only in blank lines or trailing whitespace" in the bullet. Copy the edited file byte for byte to `plugins/superclaude/skills/sc-implement-protocol/refs/qa.md`.

Acceptance criteria:
- `grep -n "differs only in blank lines or trailing whitespace" src/superclaude/skills/sc-implement-protocol/refs/qa.md` prints one line inside "## FINAL derived test", and that bullet still says a changed, added, removed or reordered non-blank line outside the slots is `issues` (managed) or `FINAL:` evidence (legacy); output saved as `./artifacts/t1-grep.txt`.
- `cmp src/superclaude/skills/sc-implement-protocol/refs/qa.md plugins/superclaude/skills/sc-implement-protocol/refs/qa.md` exits 0; saved with its exit code in `./artifacts/t1-cmp.txt`.
- `git diff -- src/superclaude/skills/sc-implement-protocol/refs/qa.md`, saved as `./artifacts/t1-diff.txt`, touches only that bullet, and the lines of the reviewer template fenced block are unchanged.

## Phase 2: Define the recovery path for a defective saved prompt

## Task 2: Add rule B to the qa.md review and FINAL sections

Depends on: Task 1

In `src/superclaude/skills/sc-implement-protocol/refs/qa.md`, under "## Subagent prompt (when not inline)", after the bullet list "Saved prompts and paperwork-only reviews", add a short subsection headed "Defective saved prompt (recovery)" that states, in this order: when a FINAL flags a saved prompt as differing from the template, the executor re-runs that task's review with a template-exact prompt saved as the next free `prompt-<k>-<j>.md` of the same `start` (its reviewed tree pinned as `r<k>-<j>`), without reopening or reverting the task; a re-review with no blocking finding appends the task's `complete` line again (no new `start`); a re-review with a confirmed blocker appends `blocked` and follows the Resume rows of `refs/ledger.md`; the defective prompt is then moved unchanged, never edited or deleted, to `<pkg>/artifacts/superseded-prompts/T<id>-prompt-<k>-<j>.md` (managed) or `.dev/implement/<slug>/superseded-prompts/T<id>-prompt-<k>-<j>.md` (legacy), with a `README.md` in that folder naming each moved file, its old path, the `FINAL:` line that flagged it and the replacing prompt; this move is part of the protocol and needs no separate user approval. In "## FINAL derived test", extend the "History:" bullet so files under `superseded-prompts/` are history and are not compared, and add that FINAL returns `issues` when a superseded prompt's task has no later template-exact saved prompt in `<retries>/T<id>/` or the folder has no `README.md`. In "## Managed FINAL review (archive gate)", add `superseded-prompts/` to what the FINAL reads. Copy the edited file byte for byte to the `plugins/` twin.

Acceptance criteria:
- `grep -n "Defective saved prompt (recovery)" src/superclaude/skills/sc-implement-protocol/refs/qa.md` prints one heading line, and the subsection holds the phrases "next free `prompt-<k>-<j>.md`", "appends the task's `complete` line again", "moved unchanged", "superseded-prompts/" and "needs no separate user approval"; the grep output for each phrase is saved in `./artifacts/t2-grep.txt`.
- The "## FINAL derived test" History bullet names `superseded-prompts/` as history, and a bullet in that section returns `issues` for a superseded prompt with no later template-exact saved prompt or no `README.md`; the "## Managed FINAL review (archive gate)" paragraph names `superseded-prompts/` among the files FINAL reads; each shown in `./artifacts/t2-grep.txt`.
- `cmp` of the `src/` and `plugins/` copies of `refs/qa.md` exits 0, saved in `./artifacts/t2-cmp.txt`; `git diff` of the reviewer template fenced block is empty (`./artifacts/t2-template-diff.txt`, no output).
- The number of lines containing `src/superclaude` in `src/superclaude/skills/sc-implement-protocol/refs/qa.md` equals that in `git show HEAD:src/superclaude/skills/sc-implement-protocol/refs/qa.md` (both `grep -c` counts saved in `./artifacts/t2-srcpath.txt`).

## Task 3: Allow the re-review complete line in refs/ledger.md

Depends on: Task 2

In `src/superclaude/skills/sc-implement-protocol/refs/ledger.md`, after the section "## Post-ruling complete line", add a section "## Re-review complete line" stating that after a FINAL flags a saved prompt (`refs/qa.md`, "Defective saved prompt (recovery)"), a template-exact re-review with no blocking finding appends the task's `complete verdict=compliant` line again with no new `start` line; it uses the existing verdict grammar and regex, the latest record of the task counts, and it is legal only after a `FINAL:` line. In "## Managed-package extension", add one bullet saying the re-review complete lines and the later move to `superseded-prompts/` come before the fresh FINAL of the next archive attempt. Copy the edited file byte for byte to the `plugins/` twin.

Acceptance criteria:
- `grep -n "## Re-review complete line" src/superclaude/skills/sc-implement-protocol/refs/ledger.md` prints one line, and that section says "no new `start` line" and that the line is legal only after a `FINAL:` line; the Managed-package extension bullet names `superseded-prompts/`; grep output saved in `./artifacts/t3-grep.txt`.
- The verdict regex block and the record-form blocks marked `ledger-grammar-block` in `refs/ledger.md` are unchanged (`git diff` shows no change inside them), saved as `./artifacts/t3-diff.txt`.
- `cmp` of the `src/` and `plugins/` copies of `refs/ledger.md` exits 0, saved in `./artifacts/t3-cmp.txt`.

## Task 4: Update refs/managed-workspace.md for superseded prompts

Depends on: Task 3

In `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md`: in "## Ledger, artifacts, pins", add a bullet that a defective saved prompt moved under the recovery path lives at `<pkg>/artifacts/superseded-prompts/` with its `README.md` (see `refs/qa.md`, "Defective saved prompt (recovery)") and is moved, never deleted; in the "## Enforcement map" row that begins "| saved reviewer prompt (`<retries>/T<id>/prompt-<k>-<j>.md`) matches the reviewer template outside the slots", add that blank-line and trailing-whitespace differences are a note and that `superseded-prompts/` holds history the FINAL checks for a README and a later template-exact prompt. Copy the edited file byte for byte to the `plugins/` twin.

Acceptance criteria:
- `grep -n "superseded-prompts/" src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md` prints at least two lines, one in "## Ledger, artifacts, pins" and one in the "## Enforcement map" saved-prompt row, and that row also says blank-line and trailing-whitespace differences are a note; saved as `./artifacts/t4-grep.txt`.
- `cmp` of the `src/` and `plugins/` copies of `refs/managed-workspace.md` exits 0, saved in `./artifacts/t4-cmp.txt`.

## Phase 3: Pin the rules with regression tests

## Task 5: Add tests/skills/test_implement_saved_prompt_rule.py and run the checks

Depends on: Task 4

Create `tests/skills/test_implement_saved_prompt_rule.py` with tests that read the three refs from both `src/superclaude/skills/sc-implement-protocol/refs/` and `plugins/superclaude/skills/sc-implement-protocol/refs/` and fail when: `refs/qa.md` lacks "differs only in blank lines or trailing whitespace" or the heading "Defective saved prompt (recovery)" or the phrases "appends the task's `complete` line again" and "moved unchanged"; `refs/ledger.md` lacks "## Re-review complete line"; `refs/managed-workspace.md` lacks "superseded-prompts/"; or any of the three files differs between the `src/` and `plugins/` copies. Then run `make sync-dev`, `make verify-sync` and `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills -q -p no:cacheprovider`.

Acceptance criteria:
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_implement_saved_prompt_rule.py -q -p no:cacheprovider` passes, saved as `./artifacts/t5-new-tests.txt`, and each test asserts on a phrase or byte comparison listed above.
- `make verify-sync` reports "All components in sync." (`./artifacts/t5-verify-sync.txt`), and `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills -q -p no:cacheprovider` shows no failures (`./artifacts/t5-pytest-skills.txt`; the baseline before this plan was `804 passed`).
- `git status --porcelain -- .claude` shows nothing staged under `.claude/` (`./artifacts/t5-claude-status.txt`), and `git status --porcelain -- docs src plugins tests`, saved as `./artifacts/t5-status-after.txt`, shows, beyond the entries in `./artifacts/t1-status-before.txt`, only the three refs, their three `plugins/` twins and the new test file.

## Phase 4: Record the earlier package's prompts under rule A

## Task 6: Check the nine earlier prompts and add the note file

Depends on: Task 5

Write `./artifacts/prompt-check.py` (run with `PYTHONDONTWRITEBYTECODE=1 uv run python -I`) that takes the template from `src/superclaude/skills/sc-implement-protocol/refs/qa.md` (the fenced block under "## Subagent prompt (when not inline)") and, for each of `.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T1/prompt-1-1.md` through `.../T9/prompt-1-1.md`, checks: line 2 equals the template's first line; the seven slot labels ("Task brief:", "Global constraints:", "Start sha:", "Diff against the start snapshot:", "Delta diff from the previous reviewed tree (empty on the first review):", "Earlier blocking findings of this start (empty on the first review):", "Saved-probe re-check hit locations (may be empty):") start lines in that order; and the text from "Do not trust the implementer's report." to the end matches the template's tail byte for byte and, separately, as non-blank lines with trailing whitespace removed. It prints one line per file: `match`, `blank-line-only` or `differs`. Save its output as `./artifacts/t6-prompt-check.txt`. Then add `.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/prompt-template-check.md` stating the result per prompt, that under rule A (`refs/qa.md`, "## FINAL derived test") a blank-line-only difference is a note, and pointing at this package's `./artifacts/prompt-check.py` and `./artifacts/t6-prompt-check.txt` by their `.dev/tasks/` paths.

Acceptance criteria:
- `./artifacts/t6-prompt-check.txt` has nine lines, one per T1 to T9 prompt, each `blank-line-only` (or, if not, the note file reports the actual result and the difference).
- `.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/prompt-template-check.md` exists and states the per-prompt results matching `./artifacts/t6-prompt-check.txt`.
- `git ls-files -s -- .dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403`, saved before the note file is written as `./artifacts/t6-index-before.txt` and after `git add .dev/tasks` as `./artifacts/t6-index-after.txt`, differs only by the one added line for `artifacts/prompt-template-check.md` (`diff` of the two saved as `./artifacts/t6-index-diff.txt`).
