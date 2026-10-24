# GitHub prerequisites re-check (Task 3)

Captured 2026-10-23 (UTC). Read-only; no repository setting was changed.

## 1. Actions pull-request setting

Command:

```
gh api repos/IronbellyOrg/IronClaude/actions/permissions/workflow
```

Exit code: 0

Raw stdout:

```
{"default_workflow_permissions":"read","can_approve_pull_request_reviews":true}
```

Raw stderr: (empty)

Result: `can_approve_pull_request_reviews` is `true`. The repository setting "Allow GitHub Actions to create and approve pull requests" is on, so Fix 1 is not blocked on that setting. (`default_workflow_permissions` is `read`; the sync job sets its own job-level permissions, so that default does not matter for it.) This task does not change the setting.

## 2. Events triggered by the built-in `GITHUB_TOKEN` (known limitation of Fix 1)

Source: https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow (the old URL https://docs.github.com/en/actions/using-workflows/triggering-a-workflow redirects here), section "Triggering a workflow from a workflow". Text fetched with curl on 2026-10-23.

Quoted sentence:

> When you use the repository's GITHUB_TOKEN to perform tasks, events triggered by the GITHUB_TOKEN will not create a new workflow run, with the following exceptions:

Exception that applies to a pull request opened by the sync job:

> pull_request events with the opened, synchronize, or reopened activity types: when a workflow using GITHUB_TOKEN creates or updates a pull request, the resulting pull_request event creates workflow runs in an approval-required state. The pull request displays a banner in the merge box, and a user with write access to the repository can start the runs by selecting Approve workflows to run.

Known limitation of Fix 1: the sync pull request is opened with the built-in token, so `pull_request` workflows such as test.yml are created in an approval-required state and do not run until a user with write access approves them. They may therefore not start on their own on the sync pull request. This plan proposes no token change (the page names a GitHub App token or a personal access token as the alternative; neither is introduced).

## 3. Path-filter changed-file limit

Source: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax (the old URL https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions redirects here), section on git diff comparisons for `on.<push|pull_request>.paths`. The same text is also on the trigger-a-workflow page above. Text fetched with curl on 2026-10-23.

Quoted sentence:

> If the generated diff contains more than 3,000 files and the files the workflow filter matches are not in the first 3,000 returned by the filter, the workflow will not run.

The limit is 3,000 changed files on github.com.
