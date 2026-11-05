dbc6c007553df880bd8b6aeea3c8ea3665f2e234
Review one task for spec compliance.

Task brief: T2 (AC ids in order of the "Acceptance criteria:" bullets: T2.AC1,T2.AC2,T2.AC3,T2.AC4). Plan file: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/TASK-WF-implementSavedPr-20261105-034852.md, lines 43-54:
## Task 2: Add the recovery subsection and the superseded-prompts FINAL rules to refs/qa.md (rule B)

Depends on: Task 1

In `src/superclaude/skills/sc-implement-protocol/refs/qa.md`, at the end of section "## Subagent prompt (when not inline)" (after the "Saved prompts and paperwork-only reviews" bullets), add a subsection headed "### Defective saved prompt (recovery)" that states, in this order: when a FINAL flags a saved prompt as differing from the template, the executor re-runs that task's review with a template-exact prompt saved as the next unused `j` of the same `k` (`prompt-<k>-<j>.md`), without reopening or reverting the task, and skips the re-review when a later saved prompt of the task already passes the saved-prompt comparison (it then only moves the defective prompt); the delta-diff, earlier-findings and re-check slots of that prompt are empty; the reviewed diff is `git diff <the task's start sha from its ledger start line> -- <the paths in the files= field of the task's latest complete line>` plus the full contents of untracked files among those paths, edits by later tasks to the same paths are in that diff and the reviewer judges only this task's acceptance criteria, and when the start is not a tree (`nogit` or a HEAD fallback) the paths come from the Q0 tool trace as this file already says; the reviewed tree is pinned as `r<k>-<j>` and that ref is deleted again when the `complete` line is appended; a re-review with no blocking finding appends the task's `complete` line again with the same verdict fields as its latest `complete` line and no new `start` line, except that a re-review which writes new notes lines replaces the `notes@` token (a task completed after a user-accepted gap repeats its non-compliant verdict fields unchanged, so the accepted gap stays valid); in a managed run a re-review with a confirmed blocker appends `blocked` and follows the Resume rows of `refs/ledger.md`; the defective prompt is then moved unchanged, never edited or deleted, with an ordinary file move (the helper rule in `refs/managed-workspace.md` covers packages only), to `<pkg>/artifacts/superseded-prompts/T<id>-prompt-<k>-<j>.md` (managed) or `.dev/implement/<slug>/superseded-prompts/T<id>-prompt-<k>-<j>.md` (legacy), with a `README.md` in that folder naming each moved file, its old path, the `FINAL:` line that flagged it and the replacing prompt; this move is part of the protocol and needs no separate user approval. The subsection ends with the legacy trigger: "In a legacy run", when the legacy FINAL records a saved-prompt template difference in its `FINAL:` evidence, the executor runs the same recovery before printing the final summary, and a blocker found by the re-review is recorded in the `FINAL:` evidence and the summary and appends no `blocked` line, because the legacy FINAL never reopens a task. In section "## FINAL derived test", extend the "History:" bullet so files under `superseded-prompts/` are history and are not compared, and add a bullet that FINAL returns `issues` (managed) or records it in `FINAL:` evidence (legacy) when a superseded prompt's task has no later saved prompt (a higher `j` of the same `k`) in `<retries>/T<id>/` that passes the saved-prompt comparison above, or when the folder has no `README.md`. In section "## Managed FINAL review (archive gate)", add `superseded-prompts/` to what the FINAL reads. Keep every new or rewritten line free of the words listed in the second Constraints bullet. Copy the edited file byte for byte to the `plugins/` twin.

Acceptance criteria:
- `grep -n "### Defective saved prompt (recovery)" src/superclaude/skills/sc-implement-protocol/refs/qa.md` prints one heading line, and the subsection contains each phrase "next unused `j` of the same `k`", "skips the re-review when a later saved prompt", "untracked files", "deleted again when the `complete` line is appended", "appends the task's `complete` line again", "replaces the `notes@` token", "moved unchanged", "ordinary file move", "needs no separate user approval", "In a legacy run" and "appends no `blocked` line"; the grep output for each phrase is saved in `./artifacts/t2-grep.txt`.
- "## FINAL derived test" names `superseded-prompts/` as history and holds the bullet for a superseded prompt with no later passing saved prompt or no `README.md`, and "## Managed FINAL review (archive gate)" names `superseded-prompts/` among the files FINAL reads; the grep output is in `./artifacts/t2-grep.txt`. `grep -c "when they differ"` on `refs/qa.md` still prints 0.
- The `extract-blocks.py qa` output on the edited file is `cmp`-equal to its output on `git show HEAD:` of the same file (`./artifacts/t2-template-cmp.txt`, exit 0), and the number of lines containing `src/superclaude` equals that in `git show HEAD:` (`./artifacts/t2-srcpath.txt`).
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills -q -p no:cacheprovider` passes with no failures (`./artifacts/t2-pytest-skills.txt`), `git status --porcelain -- tests` shows no entry for `tests/skills/test_implement_severity_static.py` (`./artifacts/t2-tests-status.txt`), and `cmp` of the `src/` and `plugins/` copies of `refs/qa.md` exits 0 (`./artifacts/t2-cmp.txt`).


Global constraints: (plan ## Constraints, .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/TASK-WF-implementSavedPr-20261105-034852.md lines 17-27)
## Constraints

- Rule changes go only in `src/superclaude/skills/sc-implement-protocol/refs/qa.md`, `src/superclaude/skills/sc-implement-protocol/refs/ledger.md` and `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md`, each with a byte-identical copy at the same relative path under `plugins/superclaude/skills/sc-implement-protocol/`. No other skill, command, agent or core file changes, and the reviewer template block (the fenced block that begins "Review one task for spec compliance." under "## Subagent prompt (when not inline)" in `refs/qa.md`) and the `ledger-grammar-block` fenced blocks in `refs/ledger.md` do not change.
- `tests/skills/test_implement_severity_static.py` is not modified. Its classification test fails on any line in the protocol files that matches the words `Ruling` (capital R), `halt`, `halts`, `halted`, `halting`, `E-HALT-QA` or `E-ARCHIVE-BLOCKED` and is not already listed there, so every new or rewritten line in the three refs avoids those words (say "a user-accepted gap" and "stop"), and additions to step 6 of `refs/managed-workspace.md` stay inside the existing single step-6 line. The existing wording "`issues` → STOP `E-ARCHIVE-BLOCKED`" stays verbatim.
- A prompt-builder script, any other lesson in `docs/memory/reflect/deviation-patterns-OrcaCLICommandRefactor-Specs.md`, and the globally installed copy of this skill (it changes when the user runs `superclaude install`) are out of scope.
- Never stage `.claude/` contents. `make sync-dev` copies `src/superclaude/` into `.claude/` only and does not touch `plugins/`, so each task copies its edited ref into the `plugins/` twin by hand, and Task 5 runs `make sync-dev` once after all edits to `src/superclaude/`.
- Installed primitives (the three refs above) must not tell an agent to read anything through a `src/superclaude/...` path.
- In `.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/`, only the new file `artifacts/prompt-template-check.md` is added; its prompts, ledger and every other file stay byte-unchanged.
- Scripts and evidence for this plan go under this package's `./artifacts/`.
- `.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `artifacts/` included. Staging is not committing; commit only when the user asks.


Start sha: dbc6c007553df880bd8b6aeea3c8ea3665f2e234
Diff against the start snapshot: (git diff dbc6c007553df880bd8b6aeea3c8ea3665f2e234 -- src/superclaude/skills/sc-implement-protocol/refs/qa.md plugins/superclaude/skills/sc-implement-protocol/refs/qa.md, plus the task's new artifact files under .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/ listed after the diff)
diff --git a/plugins/superclaude/skills/sc-implement-protocol/refs/qa.md b/plugins/superclaude/skills/sc-implement-protocol/refs/qa.md
index 631b22b7..53d28ccb 100644
--- a/plugins/superclaude/skills/sc-implement-protocol/refs/qa.md
+++ b/plugins/superclaude/skills/sc-implement-protocol/refs/qa.md
@@ -293,8 +293,9 @@ This is the single statement for both FINALs (the managed archive FINAL and the
 
 - Both FINALs read the notes, probe, prompt and review files in `<retries>/T<id>/`, apply the severity test of "## Severity model" with the anchor Read-back to the end state, and return `issues` only for a blocking defect. The legacy FINAL applies the same test and stays advisory.
 - A notes entry whose answers are all `no` is cited `noted` and is not an unmet AC; a notes entry with a confirmed `yes` is `issues` even when its line labels it minor.
-- History: a blocking line of a `review-*.md` that a later status line or a later repair file marks `resolved`, and a notes line prefixed `superseded `, is history. FINAL judges the end state, not those lines.
+- History: a blocking line of a `review-*.md` that a later status line or a later repair file marks `resolved`, and a notes line prefixed `superseded `, is history, as is every file under `superseded-prompts/` (a moved saved prompt, which FINAL does not compare with the template). FINAL judges the end state, not those lines.
 - Saved prompts: line 1 of every saved prompt `prompt-<k>-<j>.md` is the task's start sha, and FINAL compares the lines after the start-sha header and outside the slots with the reviewer template. A prompt that differs only in blank lines or trailing whitespace (their number or position) is not a template difference: record it as a note (cited `noted`), not `issues`. Any changed, added, removed or reordered non-blank line is `issues` (managed) or recorded in `FINAL:` evidence (legacy), as before.
+- Superseded prompts: FINAL returns `issues` (managed) or records it in `FINAL:` evidence (legacy) when a superseded prompt's task has no later saved prompt (a higher `j` of the same `k`) in `<retries>/T<id>/` that passes the saved-prompt comparison above, or when the `superseded-prompts/` folder has no `README.md`.
 - The legacy FINAL trigger depends on task status, not on the verdict value, so the accepted-minor path leaves it unchanged. The accepted-minor path writes no `FINAL:` or `ARCHIVE:` line. For N=1 there is no legacy FINAL; that is existing behaviour, not a waiver.
 
 Residual risk, stated: the FINAL is defence in depth only. Legacy N=1 runs and `--skip-final-review` runs get no FINAL re-check of the notes. The primary gate against a misgraded finding is the mechanical derivation and the anchor Read-back; for those runs the final summary prints every recorded minor.
@@ -307,7 +308,7 @@ Residual risk, stated: the FINAL is defence in depth only. Legacy N=1 runs and `
 
 ## Managed FINAL review (archive gate)
 
-Same isolation as above: `Do not trust the implementer's report.` One fresh subagent per archive attempt (never inline, even N=1; never reused from an earlier attempt). Input: the current full plan, the full ledger, and the current contents of every delivery file the helper's `--print-state` lists, plus the plan's `## Constraints`. Output: `pass` or `issues` with `path:line` evidence per task AC, taken from the current files and the package's `./artifacts/` logs, not copied from the ledger; reading those logs is the one exception to the Isolation rule above. A per-task `evidence=` line number is a pointer recorded when that task was reviewed, and a later task can move it, so a moved line number alone is never `issues`. `issues` when an AC is unmet at the end state, no evidence for it can be found in the current files or logs, a later change contradicts it, a plan `## Constraints` item is violated, or a log cited on a task's latest `complete` line shows a failure at its outcome line. For a user-accepted gap, verify the current outcome matches the recorded scoped acceptance, cite the unmet AC honestly, and return `issues` for any new or changed unaccepted gap. Never mark unmet AC as met. This pass never rewrites per-task verdicts and is not a code-quality ensemble; the closed per-task verdict grammar is unchanged. The FINAL also reads every brief named by a `retry … step=revert` record and every file in `<retries>/T<id>/`, and judges WHAT against the plan; the forbidden-read rule of the Subagent prompt section never applies to the FINAL. Procedure: `refs/managed-workspace.md`.
+Same isolation as above: `Do not trust the implementer's report.` One fresh subagent per archive attempt (never inline, even N=1; never reused from an earlier attempt). Input: the current full plan, the full ledger, and the current contents of every delivery file the helper's `--print-state` lists, plus the plan's `## Constraints`. Output: `pass` or `issues` with `path:line` evidence per task AC, taken from the current files and the package's `./artifacts/` logs, not copied from the ledger; reading those logs is the one exception to the Isolation rule above. A per-task `evidence=` line number is a pointer recorded when that task was reviewed, and a later task can move it, so a moved line number alone is never `issues`. `issues` when an AC is unmet at the end state, no evidence for it can be found in the current files or logs, a later change contradicts it, a plan `## Constraints` item is violated, or a log cited on a task's latest `complete` line shows a failure at its outcome line. For a user-accepted gap, verify the current outcome matches the recorded scoped acceptance, cite the unmet AC honestly, and return `issues` for any new or changed unaccepted gap. Never mark unmet AC as met. This pass never rewrites per-task verdicts and is not a code-quality ensemble; the closed per-task verdict grammar is unchanged. The FINAL also reads every brief named by a `retry … step=revert` record and every file in `<retries>/T<id>/` and in `superseded-prompts/`, and judges WHAT against the plan; the forbidden-read rule of the Subagent prompt section never applies to the FINAL. Procedure: `refs/managed-workspace.md`.
 
 ## Subagent prompt (when not inline)
 
@@ -364,3 +365,15 @@ Saved prompts and paperwork-only reviews:
 
 - The orchestrator saves the exact prompt of review `r<k>-<j>` as `<retries>/T<id>/prompt-<k>-<j>.md`, line 1 the `start` sha, so no saved prompt is overwritten. The comparison of a saved prompt with this template, and its result, are stated once, in "## FINAL derived test".
 - A review whose only failure is reviewer paperwork (an AC mark with no citation or a bare or malformed one, an `unmet` mark that lists no finding id, or a missing or unparseable checklist answer) is unparseable: respawn once with the same input; a second such review is `E-RESUME-NEEDED reason=reviewer-down` (`refs/retry.md`). It never fails the attempt and never starts the ladder. An `unmet` mark whose listed findings are all non-blocking after the Read-back and the inherited cap is not paperwork; it counts as met with its citation ("## Verdict owner").
+
+### Defective saved prompt (recovery)
+
+When a FINAL flags a saved prompt as differing from the template (a changed, added, removed or reordered non-blank line, "## FINAL derived test"), the executor runs this recovery for each flagged prompt, in this order:
+
+- Re-review. Re-run that task's review with a template-exact prompt saved as the next unused `j` of the same `k` (`prompt-<k>-<j>.md`), that is one more than the highest `j` of that `k` in `<retries>/T<id>/` and in `superseded-prompts/`. Do not revert the task and write no new `start` line. The executor skips the re-review when a later saved prompt of the same `k` (a higher `j`) already passes the saved-prompt comparison; it then only moves the defective prompt.
+- Basis. The delta-diff, earlier-findings and re-check slots of that prompt are empty. The reviewed diff is `git diff <the task's start sha from its ledger start line> -- <the paths in the files= field of the task's latest complete line>` plus the full contents of untracked files among those paths. Edits by later tasks to the same paths are in that diff, and the reviewer judges only this task's acceptance criteria. When the start is not a tree (`nogit` or a HEAD fallback) the paths come from the Q0 tool trace, as in "## Reviewer contract", and no reviewed tree is pinned.
+- Pin. The reviewed tree is pinned as `r<k>-<j>`, and that ref is deleted again when the `complete` line is appended, or, in a legacy run, once the blocker has been reported.
+- No blocker. A re-review with no blocking finding appends the task's `complete` line again with the same verdict fields as its latest `complete` line and no new `start` line. For a compliant task whose re-review wrote new notes lines, the line replaces the `notes@` token. A task completed after a user-accepted gap repeats its latest `complete` line byte for byte, notes token included, so the accepted gap stays valid (`refs/ledger.md`, "Post-ruling complete line").
+- Blocker. In a managed run a re-review with a confirmed blocker appends `blocked` and follows the Resume rows of `refs/ledger.md`. A finding whose unmet check is the gap the user accepted is not a confirmed blocker of that task; only another confirmed blocker appends `blocked`.
+- Move. The defective prompt is then moved unchanged, never edited or deleted, with an ordinary file move (the helper rule in `refs/managed-workspace.md` covers packages only), to `<pkg>/artifacts/superseded-prompts/T<id>-prompt-<k>-<j>.md` (managed) or `.dev/implement/<slug>/superseded-prompts/T<id>-prompt-<k>-<j>.md` (legacy). A `README.md` in that folder names each moved file, its old path, the `FINAL:` line that flagged it and the replacing prompt. This move is part of the protocol and needs no separate user approval.
+- In a legacy run, when the legacy FINAL records a saved-prompt template difference in its `FINAL:` evidence, the executor runs this recovery before it prints the final summary. A blocker found by the re-review is recorded in the `FINAL:` evidence and the summary and appends no `blocked` line, because the legacy FINAL never reopens a task.
diff --git a/src/superclaude/skills/sc-implement-protocol/refs/qa.md b/src/superclaude/skills/sc-implement-protocol/refs/qa.md
index 631b22b7..53d28ccb 100644
--- a/src/superclaude/skills/sc-implement-protocol/refs/qa.md
+++ b/src/superclaude/skills/sc-implement-protocol/refs/qa.md
@@ -293,8 +293,9 @@ This is the single statement for both FINALs (the managed archive FINAL and the
 
 - Both FINALs read the notes, probe, prompt and review files in `<retries>/T<id>/`, apply the severity test of "## Severity model" with the anchor Read-back to the end state, and return `issues` only for a blocking defect. The legacy FINAL applies the same test and stays advisory.
 - A notes entry whose answers are all `no` is cited `noted` and is not an unmet AC; a notes entry with a confirmed `yes` is `issues` even when its line labels it minor.
-- History: a blocking line of a `review-*.md` that a later status line or a later repair file marks `resolved`, and a notes line prefixed `superseded `, is history. FINAL judges the end state, not those lines.
+- History: a blocking line of a `review-*.md` that a later status line or a later repair file marks `resolved`, and a notes line prefixed `superseded `, is history, as is every file under `superseded-prompts/` (a moved saved prompt, which FINAL does not compare with the template). FINAL judges the end state, not those lines.
 - Saved prompts: line 1 of every saved prompt `prompt-<k>-<j>.md` is the task's start sha, and FINAL compares the lines after the start-sha header and outside the slots with the reviewer template. A prompt that differs only in blank lines or trailing whitespace (their number or position) is not a template difference: record it as a note (cited `noted`), not `issues`. Any changed, added, removed or reordered non-blank line is `issues` (managed) or recorded in `FINAL:` evidence (legacy), as before.
+- Superseded prompts: FINAL returns `issues` (managed) or records it in `FINAL:` evidence (legacy) when a superseded prompt's task has no later saved prompt (a higher `j` of the same `k`) in `<retries>/T<id>/` that passes the saved-prompt comparison above, or when the `superseded-prompts/` folder has no `README.md`.
 - The legacy FINAL trigger depends on task status, not on the verdict value, so the accepted-minor path leaves it unchanged. The accepted-minor path writes no `FINAL:` or `ARCHIVE:` line. For N=1 there is no legacy FINAL; that is existing behaviour, not a waiver.
 
 Residual risk, stated: the FINAL is defence in depth only. Legacy N=1 runs and `--skip-final-review` runs get no FINAL re-check of the notes. The primary gate against a misgraded finding is the mechanical derivation and the anchor Read-back; for those runs the final summary prints every recorded minor.
@@ -307,7 +308,7 @@ Residual risk, stated: the FINAL is defence in depth only. Legacy N=1 runs and `
 
 ## Managed FINAL review (archive gate)
 
-Same isolation as above: `Do not trust the implementer's report.` One fresh subagent per archive attempt (never inline, even N=1; never reused from an earlier attempt). Input: the current full plan, the full ledger, and the current contents of every delivery file the helper's `--print-state` lists, plus the plan's `## Constraints`. Output: `pass` or `issues` with `path:line` evidence per task AC, taken from the current files and the package's `./artifacts/` logs, not copied from the ledger; reading those logs is the one exception to the Isolation rule above. A per-task `evidence=` line number is a pointer recorded when that task was reviewed, and a later task can move it, so a moved line number alone is never `issues`. `issues` when an AC is unmet at the end state, no evidence for it can be found in the current files or logs, a later change contradicts it, a plan `## Constraints` item is violated, or a log cited on a task's latest `complete` line shows a failure at its outcome line. For a user-accepted gap, verify the current outcome matches the recorded scoped acceptance, cite the unmet AC honestly, and return `issues` for any new or changed unaccepted gap. Never mark unmet AC as met. This pass never rewrites per-task verdicts and is not a code-quality ensemble; the closed per-task verdict grammar is unchanged. The FINAL also reads every brief named by a `retry … step=revert` record and every file in `<retries>/T<id>/`, and judges WHAT against the plan; the forbidden-read rule of the Subagent prompt section never applies to the FINAL. Procedure: `refs/managed-workspace.md`.
+Same isolation as above: `Do not trust the implementer's report.` One fresh subagent per archive attempt (never inline, even N=1; never reused from an earlier attempt). Input: the current full plan, the full ledger, and the current contents of every delivery file the helper's `--print-state` lists, plus the plan's `## Constraints`. Output: `pass` or `issues` with `path:line` evidence per task AC, taken from the current files and the package's `./artifacts/` logs, not copied from the ledger; reading those logs is the one exception to the Isolation rule above. A per-task `evidence=` line number is a pointer recorded when that task was reviewed, and a later task can move it, so a moved line number alone is never `issues`. `issues` when an AC is unmet at the end state, no evidence for it can be found in the current files or logs, a later change contradicts it, a plan `## Constraints` item is violated, or a log cited on a task's latest `complete` line shows a failure at its outcome line. For a user-accepted gap, verify the current outcome matches the recorded scoped acceptance, cite the unmet AC honestly, and return `issues` for any new or changed unaccepted gap. Never mark unmet AC as met. This pass never rewrites per-task verdicts and is not a code-quality ensemble; the closed per-task verdict grammar is unchanged. The FINAL also reads every brief named by a `retry … step=revert` record and every file in `<retries>/T<id>/` and in `superseded-prompts/`, and judges WHAT against the plan; the forbidden-read rule of the Subagent prompt section never applies to the FINAL. Procedure: `refs/managed-workspace.md`.
 
 ## Subagent prompt (when not inline)
 
@@ -364,3 +365,15 @@ Saved prompts and paperwork-only reviews:
 
 - The orchestrator saves the exact prompt of review `r<k>-<j>` as `<retries>/T<id>/prompt-<k>-<j>.md`, line 1 the `start` sha, so no saved prompt is overwritten. The comparison of a saved prompt with this template, and its result, are stated once, in "## FINAL derived test".
 - A review whose only failure is reviewer paperwork (an AC mark with no citation or a bare or malformed one, an `unmet` mark that lists no finding id, or a missing or unparseable checklist answer) is unparseable: respawn once with the same input; a second such review is `E-RESUME-NEEDED reason=reviewer-down` (`refs/retry.md`). It never fails the attempt and never starts the ladder. An `unmet` mark whose listed findings are all non-blocking after the Read-back and the inherited cap is not paperwork; it counts as met with its citation ("## Verdict owner").
+
+### Defective saved prompt (recovery)
+
+When a FINAL flags a saved prompt as differing from the template (a changed, added, removed or reordered non-blank line, "## FINAL derived test"), the executor runs this recovery for each flagged prompt, in this order:
+
+- Re-review. Re-run that task's review with a template-exact prompt saved as the next unused `j` of the same `k` (`prompt-<k>-<j>.md`), that is one more than the highest `j` of that `k` in `<retries>/T<id>/` and in `superseded-prompts/`. Do not revert the task and write no new `start` line. The executor skips the re-review when a later saved prompt of the same `k` (a higher `j`) already passes the saved-prompt comparison; it then only moves the defective prompt.
+- Basis. The delta-diff, earlier-findings and re-check slots of that prompt are empty. The reviewed diff is `git diff <the task's start sha from its ledger start line> -- <the paths in the files= field of the task's latest complete line>` plus the full contents of untracked files among those paths. Edits by later tasks to the same paths are in that diff, and the reviewer judges only this task's acceptance criteria. When the start is not a tree (`nogit` or a HEAD fallback) the paths come from the Q0 tool trace, as in "## Reviewer contract", and no reviewed tree is pinned.
+- Pin. The reviewed tree is pinned as `r<k>-<j>`, and that ref is deleted again when the `complete` line is appended, or, in a legacy run, once the blocker has been reported.
+- No blocker. A re-review with no blocking finding appends the task's `complete` line again with the same verdict fields as its latest `complete` line and no new `start` line. For a compliant task whose re-review wrote new notes lines, the line replaces the `notes@` token. A task completed after a user-accepted gap repeats its latest `complete` line byte for byte, notes token included, so the accepted gap stays valid (`refs/ledger.md`, "Post-ruling complete line").
+- Blocker. In a managed run a re-review with a confirmed blocker appends `blocked` and follows the Resume rows of `refs/ledger.md`. A finding whose unmet check is the gap the user accepted is not a confirmed blocker of that task; only another confirmed blocker appends `blocked`.
+- Move. The defective prompt is then moved unchanged, never edited or deleted, with an ordinary file move (the helper rule in `refs/managed-workspace.md` covers packages only), to `<pkg>/artifacts/superseded-prompts/T<id>-prompt-<k>-<j>.md` (managed) or `.dev/implement/<slug>/superseded-prompts/T<id>-prompt-<k>-<j>.md` (legacy). A `README.md` in that folder names each moved file, its old path, the `FINAL:` line that flagged it and the replacing prompt. This move is part of the protocol and needs no separate user approval.
+- In a legacy run, when the legacy FINAL records a saved-prompt template difference in its `FINAL:` evidence, the executor runs this recovery before it prints the final summary. A blocker found by the re-review is recorded in the `FINAL:` evidence and the summary and appends no `blocked` line, because the legacy FINAL never reopens a task.

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/t2-grep.txt ===
heading lines: 1
next unused `j` of the same `k` => 1
skips the re-review when a later saved prompt => 1
untracked files => 1
deleted again when the `complete` line is appended => 1
appends the task's `complete` line again => 1
replaces the `notes@` token => 1
moved unchanged => 1
ordinary file move => 1
needs no separate user approval => 1
In a legacy run => 1
appends no `blocked` line => 1
--- FINAL derived test and archive gate:
296: [## FINAL derived test] - History: a blocking line of a `review-*.md` that a later status line
298: [## FINAL derived test] - Superseded prompts: FINAL returns `issues` (managed) or records it i
311: [## Managed FINAL review (archive gate)] Same isolation as above: `Do not trust the implementer's report.` One 
373: [## Subagent prompt (when not inline)] - Re-review. Re-run that task's review with a template-exact prompt sa
378: [## Subagent prompt (when not inline)] - Move. The defective prompt is then moved unchanged, never edited or 
README.md bullet: 1
when they differ: 0

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/t2-template-cmp.txt ===
template cmp exit=0 lines=32

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/t2-srcpath.txt ===
src/superclaude lines: now 0 head 0

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/t2-cmp.txt ===
twin cmp exit=0

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/t2-pytest-skills.txt ===
============================= test session starts ==============================
platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
SuperClaude: 4.3.5
rootdir: /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs
configfile: pyproject.toml
plugins: superclaude-4.3.5, anyio-4.16.0
collected 804 items

tests/skills/test_brainstorm_protocol.py .                               [  0%]
tests/skills/test_codegraph_adoption.py ................................ [  4%]
..................                                                       [  6%]
tests/skills/test_implement_adviser_family.py ...                        [  6%]
tests/skills/test_implement_retry_citation.py .....................      [  9%]
tests/skills/test_implement_retry_revert.py ............................ [ 12%]
..........................                                               [ 16%]
tests/skills/test_implement_severity_replay.py ............              [ 17%]
tests/skills/test_implement_severity_static.py ......................... [ 20%]
...                                                                      [ 21%]
tests/skills/test_primitive_dual_surface_lookup.py ...                   [ 21%]
tests/skills/test_reflect_input_snapshot.py ...............              [ 23%]
tests/skills/test_repo_inventory_nongit.py .....                         [ 23%]
tests/skills/test_review_severity_rule.py .............................. [ 27%]
................................                                         [ 31%]
tests/skills/test_sc_recommend_routing_contract.py ..................... [ 34%]
......                                                                   [ 34%]
tests/skills/test_task_builder_merge.py ................................ [ 38%]
....................................                                     [ 43%]
tests/skills/test_task_workspace_lifecycle.py .......................... [ 46%]
...............................................                          [ 52%]
tests/skills/test_task_workspace_smoke.py ....                           [ 52%]
tests/skills/test_tier2_tavily_consistency.py .....                      [ 53%]
tests/skills/test_worker_contract.py ................................... [ 57%]
........................................................................ [ 66%]
........................................................................ [ 75%]
.................                                                        [ 77%]
tests/skills/test_workflow_archive.py .................................. [ 82%]
........................................................................ [ 91%]
.......................................................................  [100%]

============================= 804 passed in 12.83s =============================

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/t2-tests-status.txt ===

Delta diff from the previous reviewed tree (empty on the first review): 
diff --git a/plugins/superclaude/skills/sc-implement-protocol/refs/qa.md b/plugins/superclaude/skills/sc-implement-protocol/refs/qa.md
index afbe415b..53d28ccb 100644
--- a/plugins/superclaude/skills/sc-implement-protocol/refs/qa.md
+++ b/plugins/superclaude/skills/sc-implement-protocol/refs/qa.md
@@ -376,4 +376,4 @@ When a FINAL flags a saved prompt as differing from the template (a changed, add
 - No blocker. A re-review with no blocking finding appends the task's `complete` line again with the same verdict fields as its latest `complete` line and no new `start` line. For a compliant task whose re-review wrote new notes lines, the line replaces the `notes@` token. A task completed after a user-accepted gap repeats its latest `complete` line byte for byte, notes token included, so the accepted gap stays valid (`refs/ledger.md`, "Post-ruling complete line").
 - Blocker. In a managed run a re-review with a confirmed blocker appends `blocked` and follows the Resume rows of `refs/ledger.md`. A finding whose unmet check is the gap the user accepted is not a confirmed blocker of that task; only another confirmed blocker appends `blocked`.
 - Move. The defective prompt is then moved unchanged, never edited or deleted, with an ordinary file move (the helper rule in `refs/managed-workspace.md` covers packages only), to `<pkg>/artifacts/superseded-prompts/T<id>-prompt-<k>-<j>.md` (managed) or `.dev/implement/<slug>/superseded-prompts/T<id>-prompt-<k>-<j>.md` (legacy). A `README.md` in that folder names each moved file, its old path, the `FINAL:` line that flagged it and the replacing prompt. This move is part of the protocol and needs no separate user approval.
-- In a legacy run, when the legacy FINAL records a saved-prompt template difference in its `FINAL:` evidence, the executor runs this recovery before it prints the final summary. A blocker found by the re-review is reported in the summary and appends no `blocked` line, because the legacy FINAL never reopens a task.
+- In a legacy run, when the legacy FINAL records a saved-prompt template difference in its `FINAL:` evidence, the executor runs this recovery before it prints the final summary. A blocker found by the re-review is recorded in the `FINAL:` evidence and the summary and appends no `blocked` line, because the legacy FINAL never reopens a task.
diff --git a/src/superclaude/skills/sc-implement-protocol/refs/qa.md b/src/superclaude/skills/sc-implement-protocol/refs/qa.md
index afbe415b..53d28ccb 100644
--- a/src/superclaude/skills/sc-implement-protocol/refs/qa.md
+++ b/src/superclaude/skills/sc-implement-protocol/refs/qa.md
@@ -376,4 +376,4 @@ When a FINAL flags a saved prompt as differing from the template (a changed, add
 - No blocker. A re-review with no blocking finding appends the task's `complete` line again with the same verdict fields as its latest `complete` line and no new `start` line. For a compliant task whose re-review wrote new notes lines, the line replaces the `notes@` token. A task completed after a user-accepted gap repeats its latest `complete` line byte for byte, notes token included, so the accepted gap stays valid (`refs/ledger.md`, "Post-ruling complete line").
 - Blocker. In a managed run a re-review with a confirmed blocker appends `blocked` and follows the Resume rows of `refs/ledger.md`. A finding whose unmet check is the gap the user accepted is not a confirmed blocker of that task; only another confirmed blocker appends `blocked`.
 - Move. The defective prompt is then moved unchanged, never edited or deleted, with an ordinary file move (the helper rule in `refs/managed-workspace.md` covers packages only), to `<pkg>/artifacts/superseded-prompts/T<id>-prompt-<k>-<j>.md` (managed) or `.dev/implement/<slug>/superseded-prompts/T<id>-prompt-<k>-<j>.md` (legacy). A `README.md` in that folder names each moved file, its old path, the `FINAL:` line that flagged it and the replacing prompt. This move is part of the protocol and needs no separate user approval.
-- In a legacy run, when the legacy FINAL records a saved-prompt template difference in its `FINAL:` evidence, the executor runs this recovery before it prints the final summary. A blocker found by the re-review is reported in the summary and appends no `blocked` line, because the legacy FINAL never reopens a task.
+- In a legacy run, when the legacy FINAL records a saved-prompt template difference in its `FINAL:` evidence, the executor runs this recovery before it prints the final summary. A blocker found by the re-review is recorded in the `FINAL:` evidence and the summary and appends no `blocked` line, because the legacy FINAL never reopens a task.
Earlier blocking findings of this start (empty on the first review): 
F1.1 sev=blocking trigger=B4 ac=scope at=src/superclaude/skills/sc-implement-protocol/refs/qa.md:379 anchor="a blocker found by the re-review is recorded in the `FINAL:` evidence and the summary and appends no `blocked` line" chk=amiss:n,false:n,harm:n,constraint:y family=legacy-final-evidence fix=change "is reported in the summary" to "is recorded in the `FINAL:` evidence and the summary", then recopy the file to the `plugins/` twin covers="The subsection ends with the legacy trigger: ... a blocker found by the re-review is recorded in the `FINAL:` evidence and the summary" first=A1 origin=new: The legacy bullet says the blocker is only "reported in the summary" and leaves out the `FINAL:` evidence record that the task text requires.
Saved-probe re-check hit locations (may be empty): 
src/superclaude/skills/sc-implement-protocol/refs/qa.md:379
plugins/superclaude/skills/sc-implement-protocol/refs/qa.md:379

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
