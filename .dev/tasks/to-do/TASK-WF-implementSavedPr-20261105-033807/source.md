# Request: close the saved-reviewer-prompt gaps in /sc:implement

Revision 2. Revision 1 failed the advisory plan review (two blocking and four should-fix findings, in `.dev/reflect/pre-TASK-WF-implementSavedPr-20261104-230730-20261104230947/reviewer-cards/`). This revision states the rule in one place, adds the recovery trigger, defines the re-review basis, covers a task completed under a Ruling, and fixes the earlier-package check so it can see the defect.

## Why

The fence-fix run (`.dev/tasks/done/TASK-WF-devGuideFenceFix-20261104-204854/`) showed two gaps in the `/sc:implement` rule that compares each saved reviewer prompt with the closed reviewer template:

1. The comparison is byte-exact outside the slots. A hand-filled prompt that dropped one blank line (between "Saved-probe re-check hit locations (may be empty): " and "Do not trust the implementer's report.") blocked the managed archive twice, although no review criterion was added, removed or reworded.
2. There is no recovery path. A saved prompt may never be overwritten, so once a prompt differs from the template, every later FINAL returns `issues`, and the managed archive gate just stops (`E-ARCHIVE-BLOCKED`) with nothing that starts a fix. The package could only archive by an ad-hoc user instruction (here: moving the two prompts to `artifacts/superseded-prompts/` and an `ARCHIVE: Ruling:` line, ledger `progress.md` lines 7-11 of that package). The re-review that preceded the move (a second `complete` line per task with no new `start`, prompts named `prompt-1-2.md` with no repair file) is also not described by the protocol.
3. The earlier package `.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/` holds nine saved prompts (`artifacts/retries/T1/` to `T9/`, each `prompt-1-1.md`) with the same missing blank line; its FINAL passed without noticing.

## What to change

Rule source: `src/superclaude/skills/sc-implement-protocol/refs/qa.md` ("## FINAL derived test"; "## Managed FINAL review (archive gate)"; the "Saved prompts and paperwork-only reviews" bullets under "## Subagent prompt (when not inline)"), `refs/ledger.md` (record forms, Resume), `refs/managed-workspace.md` (the "Completion: fresh FINAL, then archive" steps, "Ledger, artifacts, pins", and the Enforcement-map row for saved reviewer prompts). The plugin mirror `plugins/superclaude/skills/sc-implement-protocol/` must stay byte-identical to `src/`.

A. Whitespace tolerance, stated once. The saved-prompts bullet in "## FINAL derived test" is the single statement of the comparison rule: FINAL compares the lines outside the slots; a difference only in blank lines (their number or position) or in trailing whitespace is not a template difference and FINAL records it as a note (cited `noted`); any other difference (a changed, added, removed or reordered non-blank line) stays `issues` (managed) or `FINAL:` evidence (legacy), as today. The first bullet under "Saved prompts and paperwork-only reviews" currently restates the rule ("... and return `issues` (managed) or record it in `FINAL:` evidence (legacy) when they differ"); rewrite that sentence to point to the FINAL derived-test rule instead of restating it, so that after the change the phrase "when they differ" no longer appears in `refs/qa.md`. The Enforcement-map row in `refs/managed-workspace.md` says the same (blank-line and trailing-whitespace differences are a note).

B. Recovery path for a defective saved prompt.
- Trigger. In `refs/managed-workspace.md`, step 6 of "Completion: fresh FINAL, then archive": when every `issues` item of the FINAL is a saved-prompt template difference, the executor runs the recovery below in the same invocation and then repeats the archive gate from step 1 (a new FINAL). STOP `E-ARCHIVE-BLOCKED` applies only if the recovery cannot finish or the new FINAL still returns `issues`. For a legacy run (advisory FINAL) the executor runs the same recovery before printing the final summary.
- Re-review. The executor re-runs that task's review with a template-exact prompt saved as a higher `j` of the same `k` (`prompt-<k>-<j>.md`), without reopening or reverting the task. The reviewed diff is `git diff <the task's start sha from its ledger start line> -- <the paths in the files= field of the task's latest complete line>`, so later tasks' edits are not in it. The reviewed tree is pinned as `r<k>-<j>` and that ref is deleted again when the `complete` line is appended.
- Ledger. A re-review with no blocking finding appends the task's `complete` line again with the same verdict fields as its latest `complete` line and no new `start` line: a `compliant` task stays `compliant`, and a task that was completed under a Ruling repeats its non-compliant verdict fields unchanged so the Ruling stays valid (`refs/ledger.md`, "Post-ruling complete line"). A re-review with a confirmed blocker appends `blocked` and follows the existing Resume rows.
- Move. The defective prompt is then moved unchanged (never edited or deleted) to `<pkg>/artifacts/superseded-prompts/T<id>-prompt-<k>-<j>.md` (managed) or `.dev/implement/<slug>/superseded-prompts/T<id>-prompt-<k>-<j>.md` (legacy), with a `README.md` there naming each moved file, its old path, the FINAL line that flagged it and the replacing prompt. This move is part of the protocol and needs no separate user approval.
- FINAL. Files under `superseded-prompts/` are history and are not compared. FINAL returns `issues` when a superseded prompt's task has no later saved prompt (a higher `j` of the same `k`) in `<retries>/T<id>/` that passes the saved-prompt comparison (exact, or differing only in blank lines or trailing whitespace), or when the README is missing.

C. Earlier package. With rule A in place, check mechanically that each of the nine `prompt-1-1.md` files in `.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T1..T9/` differs from the template outside the slots only in blank lines. The check script locates the seven slot labels in order and compares everything outside the slot contents, including the two junctions (the first line, then a blank line, then "Task brief:"; and the last slot label "Saved-probe re-check hit locations (may be empty): " then a blank line, then "Do not trust the implementer's report." to the end). It prints one line per file: `match` (byte-equal outside the slots), `blank-line-only` (equal after dropping blank lines and trailing whitespace, not byte-equal) or `differs`. The expected result is `blank-line-only` for all nine. Prove the script itself on a synthetic template-exact prompt (expected `match`) and on a copy of one real prompt with one non-blank template line changed (expected `differs`). Save the script and all outputs under the new plan package's `artifacts/`, and add a short note file `artifacts/prompt-template-check.md` to the earlier package recording the per-prompt result and pointing at the saved evidence by its package-relative path, saying the evidence package lives under `.dev/tasks/to-do/` until archived and `.dev/tasks/done/` after. Do not edit, move or delete the earlier package's prompts, ledger or other files.

## Checks

- Regression tests in `tests/skills/` that fail if: the phrase "when they differ" is still in `refs/qa.md`; rule A wording (blank-line and trailing-whitespace differences are a note) or the rule B recovery subsection is missing from `refs/qa.md`; the recovery trigger is missing from step 6 of `refs/managed-workspace.md`; the re-review `complete` line section is missing from `refs/ledger.md`; or any of those three files differs between `src/` and `plugins/`.
- The reviewer template block is unchanged (the existing `test_rec2_closed_reviewer_template_unchanged` passes) and the ledger-grammar blocks in `refs/ledger.md` are unchanged (a saved script extracts them from the working file and from `git show HEAD:` and the two extracts are `cmp`-equal).
- The number of lines containing `src/superclaude` in each of the three refs equals its count in `git show HEAD:`.
- `make sync-dev`, `make verify-sync`, and `uv run pytest tests/skills -q` pass (output saved as evidence).

## Out of scope

- A prompt-builder script, any other lesson from `docs/memory/reflect/deviation-patterns-OrcaCLICommandRefactor-Specs.md`, any other skill, command or agent.
- Changing the reviewer template text itself.
- Updating the globally installed copy under `~/.claude/skills/` (that changes when the user runs `superclaude install`).

## Constraints

- Never stage `.claude/` contents; edit `src/superclaude/` and the `plugins/` mirror, and run `make sync-dev` once after all edits to `src/superclaude/`.
- Installed primitives must not tell an agent to read anything through a `src/superclaude/...` path.
- `.dev/tasks/` is always staged (`git add .dev/tasks`); staging is not committing.
