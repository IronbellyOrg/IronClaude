# IronClaude 6.1.0: bring master into integration (the release pull request was squash-merged)

Clay's coordinating session (GeneralIronFlow) told the ic6-orchestrator, on Clay's instruction of 2026-11-19 01:18 UTC, to do this. Your orchestrator is the ic6-orchestrator session. Do the work below in this worktree only, open ONE pull request into `integration`, answer every review finding, make every check green, then STOP. Do NOT merge.

## Why

Release pull request #658 (`integration` to `master`) was merged as a SQUASH by mistake (`master` is now `3e6ced3f3`, one parent `89dc403d4`), so `integration` does not contain `master`'s squash commit. `integration` (`d619bc870`) is 8 commits ahead and 1 behind `master`. The trees differ only in two files, which are #659's doc fixes that `master` lacks: `docs/getting-started/installation.md` (the "Conversation retention" paragraph: `integration` says 90 days, `master` still says 365) and `docs/user-guide/commands.md` line 588 (`integration` dropped the `/task-builder` clause). A merge of `master` into `integration` conflicts only in `docs/getting-started/installation.md` (checked with `git merge-tree`); `commands.md` merges cleanly.

## What to do

1. Setup: `uv venv --python 3.10 && uv pip install -e '.[dev]' 'pytest-xdist>=3.5,<4' 'ruff==0.15.20' && make sync-dev`.
2. This worktree is on `clayphi/v61-merge-master`, created from `origin/integration`. `git fetch origin`, confirm `origin/integration` is `d619bc870` and `origin/master` is `3e6ced3f3` (if either moved, STOP and tell the orchestrator). Then `git merge origin/master` (a real merge, no rebase, no squash).
3. Expect exactly one conflict, in `docs/getting-started/installation.md`. Resolve it by keeping `integration`'s side (the 90-day paragraph from #659) entirely. If any other file conflicts, STOP and tell the orchestrator. After the merge, the tree must be IDENTICAL to `origin/integration`'s tree: check `git rev-parse HEAD^{tree}` equals `git rev-parse origin/integration^{tree}`. If it is not, STOP and tell the orchestrator what differs.
4. Run, and keep the output under `.dev/issues/v61-merge-master/` (do not commit that folder): `make lint`, `uv run ruff format --check src/ tests/`, `make verify-sync`, `git diff --check`, and the tests that read these docs (`uv run pytest tests/docs tests/core -q -n auto`). The full suite is not needed: the merged tree equals `integration`'s tree, which already passed (22585 passed, 70 skipped; eight load-sensitive ccsession PTY tests in `tests/unit/test_ccsession_tag.py` fail only under parallel load and pass alone). Say so in the PR body.
5. Commit the merge (keep git's default merge message, add the line `Co-Authored-By: Claude Code <noreply@anthropic.com>`). Push your branch `clayphi/v61-merge-master` only. Never force-push.
6. Open the PR with `gh pr create --repo IronbellyOrg/IronClaude --base integration --head clayphi/v61-merge-master --title "chore(release): merge master (6.1.0 squash) into integration" --body-file <file>` and then run the review loop by hand as the `sc:pr-submit` protocol describes (`/sc:pr-submit` has no `--base` or `--repo` flags). Body in plain English: why (the squash), the one conflict and how it was resolved, that the merged tree equals `integration`'s tree (the two tree ids), the check results, `Refs #647`. Say plainly that this pull request must be merged with a MERGE COMMIT (not squash), so that `master`'s commits become ancestors of `integration`. Do not add a `## Generator-Constraint Considered` section unless you touch a gate or validator file (you will not).
7. Answer every Augment and Codex finding (fix, or reply with evidence) and resolve threads.
8. When every check is green, both reviewers have finished on the final head and no thread is open: STOP. Do not merge. Do not comment to anyone else on the PR.

## Rules

Work in this worktree only. Never stage `.claude/` (except `.claude/settings.json`). Do not edit historical records and add no CHANGELOG entry. Do not launch subagents; do skill steps inline. Delete a throwaway home with a literal path. Never log or commit credentials. Do not touch `master`, any release branch or PR #662.

## Process notes for the orchestrator

Keep `.dev/issues/v61-merge-master/PROCESS-NOTES.md`: one line per step with roughly how long it took, what got in the way, and what would make the step easier next release.

## Finish

End with a plain-English report: the DONE / NEXT table, then What I did, How, Where it stands, What's next, My recommendation. Include the PR link, the two tree ids, and the state of every check and reviewer on the final head. Update the Orca comment at checkpoints: `orca worktree set --worktree active --comment "<short status>"`.
