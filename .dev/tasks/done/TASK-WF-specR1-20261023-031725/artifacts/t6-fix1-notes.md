# Fix 1 notes: pull-sync-framework.yml opens a pull request (Task 6)

Status: UNVERIFIED. Nothing in this fix can be exercised on GitHub from this worktree. The local stub runs (./artifacts/t6-stub-run.log) prove the run body's git and gh call sequence; they do not prove that GitHub accepts the push, creates the pull request, or starts any workflow on it.

## Known consequences of Fix 1

1. docs/.framework-sync-commit is committed on `sync/framework`, not on master. Until that pull request merges, master keeps the old value, so every 6-hourly run finds "framework has updates", re-syncs, and force-replaces the `sync/framework` branch.
2. An open pull request from `sync/framework` is reused, not duplicated: the step runs `gh pr list ... --state open` and only calls `gh pr create` when the count is 0.
3. Commits pushed to `sync/framework` by hand are lost at the next run, because the step force-pushes the branch.

## Prerequisite result (from ./artifacts/t3-github-prereqs.md)

`gh api repos/IronbellyOrg/IronClaude/actions/permissions/workflow` returned `{"default_workflow_permissions":"read","can_approve_pull_request_reviews":true}` (exit 0, empty stderr). The repository setting "Allow GitHub Actions to create and approve pull requests" is on, so Fix 1 is not blocked on it.

## Known limitation (from ./artifacts/t3-github-prereqs.md, Task 3)

The pull request is opened with the built-in `GITHUB_TOKEN`. GitHub documents that `pull_request` events from a workflow using that token create workflow runs in an approval-required state; a user with write access must select "Approve workflows to run". So test workflows such as test.yml may not start by themselves on the sync pull request. This plan does not change the token (no personal access token or GitHub App token is introduced).

## What the user must do after merge

- Run the workflow once by hand from master:

  `gh workflow run pull-sync-framework.yml --repo IronbellyOrg/IronClaude --ref master`

- Record the run URL and the result (branch `sync/framework` pushed; pull request URL, or "reused" if one was already open) as a comment on the pull request that merges this branch.
- Until that run is recorded, treat Fix 1 as UNVERIFIED.

## Durability

This notes file is not durable: the plan package exists only in this worktree, so these notes are lost with the worktree unless they are copied into the merging pull request.
