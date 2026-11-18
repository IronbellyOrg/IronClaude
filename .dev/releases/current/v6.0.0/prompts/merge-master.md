# IronClaude 6.0.0: bring master into integration (resolve the routing-guide conflict)

Clay's coordinating session (GeneralIronFlow) told the ic6-orchestrator on 2026-11-18 to do this. Your orchestrator is the ic6-orchestrator session. Do the work below in this worktree only, open ONE pull request into `integration`, answer every review finding, make every check green, then STOP. Do NOT merge.

## Why

`master` is 6 commits ahead of `integration` (#607 twice, #608, #619, #636, #637). GitHub's merge call returned 409 because two files conflict: `src/superclaude/core/HOW-WE-WORK.md` and its plugin copy `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (the two copies must stay byte-identical; a test checks it). The release pull request from `integration` to `master` needs `integration` to contain `master`.

## What to do

1. Setup: `uv venv --python 3.10 && uv pip install -e '.[dev]' 'pytest-xdist>=3.5,<4' ruff && make sync-dev`.
2. Create your branch from `origin/integration` (the worktree already is). `git fetch origin`, then `git merge origin/master` (a real merge, no rebase, no squash). Expect conflicts in exactly those two files; if any other file conflicts, STOP and tell the orchestrator.
3. Resolve each conflicting file in `src/superclaude/core/HOW-WE-WORK.md` and make the plugin copy byte-identical to it (`cp`, then `cmp`). There are two hunks:
   - **Command table (around `/sc:index`, `/sc:index-repo`, `/sc:issue`, `/sc:load`):** `master` changed the `/sc:issue` row (PR 636, default `--claim` pipeline level); `integration` deleted the rows of the removed commands (`/sc:index`, `/sc:index-repo`, `/sc:load`, and any other row of a command removed in 6.0.0: `build`, `cli-portify`, `improve`, `review-translation`, `roadmap`, `save`, `spawn`, `tasklist`, `validate-roadmap`). Keep master's `/sc:issue` row text; keep every removal.
   - **Routing rows `review-pr`, `resume`, `unsure`:** `master` reworded `review-pr` (PR 619, "drop built-in and local review steps from the shipping flow"); `integration` reworded `resume` and `unsure` because of the removals. For each row, compare the base, master and integration versions (`git show $(git merge-base origin/integration origin/master):<path>`, `git show origin/master:<path>`, `git show origin/integration:<path>`). If a row changed on BOTH sides for different reasons, COMBINE the two changes (do not pick one side); if it changed on one side only, take that side. Say in the pull request body, row by row, what you did and why.
   - Also check the whole merged file, not only the hunks, for a line that master added and that names a removed command or skill (`/sc:spawn`, `/sc:save`, `/sc:load`, `/sc:build`, `/sc:improve`, `/sc:index`, `/sc:index-repo`, `/sc:review-translation`, `/sc:cli-portify`, `/sc:roadmap`, `/sc:validate-roadmap`, `/sc:tasklist`): master was written without knowing the removals. If you find one, fix it the way the removal pull requests did (smallest edit that keeps the sentence true) and list it in the pull request body.
4. Run, and keep the output under `.dev/issues/v6-merge-master/` (do not commit that folder): the routing and worker-contract tests (`uv run pytest tests/core tests/skills tests/recommend tests/commands -q -n auto`), then the full suite as the `test` job of `.github/workflows/test.yml` runs it (without `--maxfail`), `make lint`, `uv run ruff format --check src/ tests/`, `make verify-sync`, `git diff --check`. Known failing test before your change (not yours): `tests/cli/test_install_keep.py::test_same_content_is_true_only_for_identical_readable_files`. Before you start, take the same baseline on `origin/integration` for comparison. Tests from master's six commits are expected to add to the pass count; report the added test ids.
5. Commit the merge (keep git's default merge message, add the attribution line `Co-Authored-By: Claude Code <noreply@anthropic.com>`). Push your branch `clayphi/v6-merge-master` only. Never force-push.
6. Open the PR: `/sc:pr-submit --base integration --head clayphi/v6-merge-master --monitor 3 --repo IronbellyOrg/IronClaude`. Body in plain English: the two hunks and what you did with each row, anything else you fixed, the before and after test counts, the check results, `Refs #571`. Say plainly that this pull request must be merged with a MERGE COMMIT (not squash), so that master's commits become ancestors of `integration`.
7. Answer every Augment and Codex finding (fix, or reply with evidence) and resolve threads. If Codex shows its usage-limit notice, say so.
8. When every check is green, both reviewers have finished on the final head and no thread is open: STOP. Do not merge. Do not comment to anyone else on the PR.

## Rules

Work in this worktree only. Never stage `.claude/` (except `.claude/settings.json`). Do not edit historical records (`docs/releases/`, `docs/testing/v5.0.0/`, `docs/designs/`, past `CHANGELOG.md` entries) and add no CHANGELOG entry. Do not launch subagents; do skill steps inline. Delete a throwaway home with a literal path. Never log or commit credentials.

## Process notes for the orchestrator

Keep `.dev/issues/v6-merge-master/PROCESS-NOTES.md`: one line per step with roughly how long it took, what got in the way, and what would make the step easier next release.

## Finish

End with a plain-English report: the DONE / NEXT table, then What I did, How, Where it stands, What's next, My recommendation. Include the PR link, the before and after test counts, and the state of every check and reviewer on the final head. Update the Orca comment at checkpoints: `orca worktree set --worktree active --comment "<short status>"`.
