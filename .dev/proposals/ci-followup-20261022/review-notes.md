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
