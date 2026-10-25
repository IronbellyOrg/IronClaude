# Follow-up to PR 280: four workflow and doc fixes

Goal: the sync job stops pushing unreviewed upstream content to master; the boundary guard stops claiming it blocks merges; the Codecov step is checked against its documentation; the docs describe what the workflows really do.

## Scope
- Edit only .github/workflows/pull-sync-framework.yml, .github/workflows/boundary-guard.yml, .github/workflows/test.yml (the Codecov step only), .github/workflows/README.md, and the one paragraph in scripts/README.md that describes publish-pypi.yml. Nothing under src/, tests/, Makefile, pyproject.toml or .claude/ changes.
- Evidence files go under ./artifacts/ in the plan package.

## Fix 1: pull-sync-framework.yml opens a pull request instead of pushing to master
- In step `Commit and Push Changes`, replace `git push origin HEAD:master` with a force-push of the commit to the branch `sync/framework`, then open a pull request into master only if none is open from that branch (check with `gh pr list` or `gh pr view` first).
- Every `gh pr` command passes `--repo "$GITHUB_REPOSITORY"`; the step sets `GH_TOKEN: ${{ github.token }}`; base is master, head is `sync/framework`.
- Job permissions become `contents: write` and `pull-requests: write`, and nothing more.
- The "no changes" path (no commit, no branch, no pull request), the protected-file check and the state-file handling stay unchanged.
- State these consequences in the plan: the state file docs/.framework-sync-commit is committed on the sync branch, so until the pull request merges, master still holds the old value and every 6-hourly run re-syncs and force-replaces the branch; an open pull request is reused; commits pushed to `sync/framework` by hand are lost at the next run.
- Prerequisites the plan cannot create: the repository setting "Allow GitHub Actions to create and approve pull requests" must be on (an earlier read said it already is; re-check with `gh api repos/IronbellyOrg/IronClaude/actions/permissions/workflow`). A pull request opened with the built-in token may not start the test workflows; this is unverified, so check it against current GitHub docs and note it as a known limitation, do not change the token.
- This fix cannot be verified locally. Report it as unverified until a `workflow_dispatch` run after merge; name that run as a user step and say where the result is recorded.

## Fix 2: boundary-guard.yml says what it does, and uses a three-dot diff
- The job only writes a warning and a summary; it cannot block anything. Reword, as advisory, the header comment about gating (lines 19-20), the job name, the `::warning` text ("Human review is required before merge") and summary item 3 ("branch protection must require this check").
- The job name must keep the word "boundary" (src/superclaude/pr_submit/ci.py matches on it). Re-read ci.py on the new base before choosing the name.
- Change the diff to the three-dot form `"$BASE_SHA...$HEAD_SHA"` with the same pathspec after `--`.
- The file name, the whole `on:` block and the five `paths:` entries stay byte-identical; tests/swarm/test_merge_boundary_guards.py must still pass (run it with `uv run pytest tests/swarm/test_merge_boundary_guards.py -v`).
- Keep the "Required reviewer checks" checklist heading and items; a file-wide search for the word "required" must not be used as a check, because that heading legitimately contains it.
- Render the merged step locally (script body with GITHUB_STEP_SUMMARY pointing at a temp file) before and after, and save both renders and their comparison; only the reworded sentences may differ and no backslash may appear before a backtick.
- Prove the three-dot change in a throwaway git repository created outside this repo: a branch behind master where only master changed one of the five guarded files; the old command lists it, the new one does not. Save the exact commands and output.
- Not included: turning the job into a real gate (a required label or CODEOWNERS); that is a repository-settings decision.

## Fix 3: Codecov step matches the action's documentation
- Before editing, read the official codecov/codecov-action v4 documentation (Context7 or the action's README) and record in ./artifacts/ whether the `file` input is deprecated in favor of `files` and whether a token is required for uploads from a push to master.
- Default: pass `token: ${{ secrets.CODECOV_TOKEN }}` and the correct file input name, and keep `fail_ci_if_error: false`. Alternative if the fork does not use Codecov: delete the step and its README mentions. Add no coverage threshold.
- Prerequisite the plan cannot create: a `CODECOV_TOKEN` repository secret. The upload is unverified until a run on GitHub.

## Fix 4: documentation matches the workflows
- .github/workflows/README.md: the status badge URLs point at IronbellyOrg/IronClaude (line 30); the Codecov troubleshooting bullet (line 124) matches Fix 3; the boundary-guard entry says the job is advisory; the pull-sync-framework entry says it opens a pull request from `sync/framework`.
- scripts/README.md line 7: the paragraph describes the deleted publish-pypi.yml. Read it and its neighbors; replace it with accurate text (the workflow no longer exists; the fork installs from git as CLAUDE.md states) or remove it if it only describes that workflow. Change nothing else in that file.

## Quality rules for every task in the plan
- Every acceptance bullet must fail on a wrong edit, not only pass on a right one. A YAML-parse bullet is a syntax check only. Proof logs must contain the exact commands run and their output.
- Do not use an unscoped `git diff --stat`, and do not use `master...HEAD`, as a scope check. Before the first task, save `git status --porcelain -uall` and a content hash of every changed file outside the allowed paths; at the end, only .github/workflows/, scripts/README.md and the plan package folder may differ from that baseline; also require positive greps showing the expected edits happened.
- Run every Python or pytest command through `uv run`. `Depends on:` lines name one task each; make real chains where order matters. No numbered or checkbox lines in the tasklist.
- Specific greps, not file-wide ones: for example check the header comment, the job `name:` line, the `::warning` line and summary item 3 separately.

## Decisions taken as defaults
- The boundary guard stays advisory. Codecov gets a token. scripts/README.md is in scope for its one paragraph. .dev/specs/pr-submit-ci-monitor.md mentions quick-check.yml (lines 18 and 28); it is a historical spec and is not edited; list it as an accepted leftover.

## Noticed, not in scope
- The Augment review bot said GitHub evaluates path filters against only the first 300 changed files, while the header comment in contract3-generator-constraint-lint.yml says 3,000. Do not add a task; raise it to me as a question after verifying against current GitHub docs.
