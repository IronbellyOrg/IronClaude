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

## Review Feedback (reflect cycle 1)

Source of these notes: the advisory reflect run on plan TASK-WF-spec-20261022-211556, verdict not ready (0 high, 10 medium, 8 low). Report: .dev/reflect/pre-TASK-WF-spec-20261022-211556-20261022211900/REPORT.md; merged findings: same folder, adversarial/merged-verdict.yaml. Every item below is a change to how the plan's tasks are written; none changes the scope or decisions above. The regenerated plan must apply all of them.

### Medium: acceptance checks that pass a wrong edit

- Task for boundary-guard.yml (Fix 2): check the header comment as a text-anchored block (from the line beginning `#   * (combined` to the line before `# This is the CI side`), which must not contain `requiring this check` or `gates` and must contain `advisory`. The `::warning` line must contain `advisory` and must not contain `before merge`. Never check by fixed line numbers.
- Task for pull-sync-framework.yml (Fix 1): assert that the base run-body lines from the first line through the `git commit` line are unchanged in the edited step (this covers the state-file `git add -f docs/.framework-sync-commit` block); compare the step's `if`, `working-directory` and `name` with the base; assert the single `gh pr create` invocation contains `--base master`, `--head sync/framework` and `--repo "$GITHUB_REPOSITORY"`.
- Tasks for pull-sync-framework.yml and test.yml: compare the whole parsed document with the base except the planned changes (the `on:` block, top-level keys, job-level keys, step count and every other step), so an inserted step or a changed schedule fails.
- Task for .github/workflows/README.md (Fix 4): both badge URLs must contain `IronbellyOrg/IronClaude/actions/workflows/test.yml`; the boundary-guard entry must say the job cannot block a merge and must not contain `gates` or `branch protection must require`; the pull-sync entry must say it does not push to master and must name `sync/framework`.

### Medium: the local stub run of the sync step

- The git stub logs its arguments and exits 0 only for `push`; every other git subcommand is passed to the real git by absolute path. The gh stub logs its arguments and prints a scripted count for `pr list`.
- Export `GITHUB_REPOSITORY=IronbellyOrg/IronClaude`. Run the body with the runner's default shell semantics for a `run:` step without `shell:`, which is `bash -e` without pipefail.
- Four runs, each with its log saved: (a) staged change, `pr list` prints 0: exactly one `gh pr create`; (b) a fresh staged change made after run (a)'s commit, `pr list` prints 1: one `gh pr list` call and zero `gh pr create`; (c) nothing staged and the paths in the add loop clean or absent: no push and no gh call; (d) staged change, the gh stub exits non-zero on `pr list`: the step fails (non-zero exit) and makes no `gh pr create` call.
- The step must fail closed when `gh pr list` fails: capture the count in a standalone assignment (so `bash -e` stops on failure) before comparing it.

### Medium: checks that fail a correct run

- Task 2's notes file: identify the decision by the line that begins `Decision:` (exactly one such line), not by position. Task 7 writes its UNVERIFIED note to its own artifact instead of appending to Task 2's file.
- Task 9's scope check: parse `git status --porcelain -uall -z`, take the path field, and record deleted or renamed paths explicitly. Paths written by the executor's own tooling after the baseline (`.dev/reflect/`, `.dev/troubleshoot/`, `.dev/workflow/`) are listed separately in the scope log as tooling output and do not fail the check; any other new or changed path outside `.github/workflows/`, `scripts/README.md` and the package folder fails. State this in Constraints as a necessary deviation from the scope rule, with the reason: the reflect and implement pipelines write their own records under `.dev/` during execution.
- Fix 1 run record: the plan package exists only in this worktree and is lost when the worktree is removed. Task 6's notes must tell the user to record the post-merge `workflow_dispatch` run URL and result as a comment on the pull request that merges this branch, and say the notes file itself is not durable.

### Low

- Placeholders: define in Constraints that `<t1-head>` means the single line in ./artifacts/t1-head.txt (use `$(cat ./artifacts/t1-head.txt)` in commands) and that the Codecov file-input name comes from Task 2's `Decision:` line; later tasks must fail if an angle-bracket placeholder survives into a command they run.
- Write the backslash-before-backtick check as a fenced command (a fixed-string grep for the two characters backslash and backtick on ./artifacts/t5-render-after.md) that must print 0.
- Summary item 3 check: the block from `3. **PR-review discipline**` to the line before `4. **Boundary test**` must contain `advisory` and must not contain `branch protection must require`.
- Throwaway repo: `git init -b master` and a local commit identity (for example `git config user.name t` and `git config user.email t@example.invalid` inside the temp repo).
- Render SHAs: HEAD_SHA is the latest commit that touched src/superclaude/cli/swarm/merge.py and BASE_SHA is its first parent; record both in the render artifacts.
- Path-filter note (source "Noticed, not in scope"): no new task. Task 3 also quotes the current GitHub docs sentence on the path-filter file limit; the planning session already found that github.com docs say 3,000 and only older GitHub Enterprise Server docs say 300, so the contract3 comment is correct. Task 9's leftovers file records this as an item for the user to confirm.
- scripts/README.md: keep the one-paragraph scope. Task 9 reads lines 1-30 before editing. The leftovers file states that the unchanged line 3 and the line 5 heading contradict the new paragraph, adds lines 34 and 64-66 to the list, and offers to extend the edit if the user agrees.
- Depends on: Task 7 depends on the Codecov research task, not on the sync task; the GitHub-settings task and the throwaway-repo proof depend on the baseline task. Order the documentation and final-scope tasks last so their single Depends on line names a task that already has the earlier edits as ancestors, and say so in that task.
