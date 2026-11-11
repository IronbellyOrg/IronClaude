# Fixture replacement blocked

Governing instruction: Task 5 precondition in `../TASK-WF-rollOutTheIssueW-20261109-000305.md`, paragraph beginning "This task can start only after the owner-run live test."

## Missing items

- Owner-written live-test record: `docs/designs/issue-watcher-live-test.md` is absent.
- Capture directory: `./artifacts/captured/` is absent in this package; all 19 required owner-redacted replies are missing:
  - `gh_api_user_include.json`
  - `gh_api_user_include_429.json`
  - `gh_graphql_insufficient_scopes.json`
  - `gh_graphql_rate_limited.json`
  - `gh_issue_list.json`
  - `gh_issue_reread.json`
  - `gh_stderr_auth_401.json`
  - `gh_stderr_http_502.json`
  - `gh_stderr_rate_403.json`
  - `gh_stderr_rate_429.json`
  - `gh_stderr_scope_read_project.json`
  - `graphql_edits.json`
  - `graphql_project_items.json`
  - `orca_launch_empty_operation_id.json`
  - `orca_launch_no_operation_id.json`
  - `orca_launch_success.json`
  - `orca_launch_unknown.json`
  - `rest_comments_marker.json`
  - `rest_events_page.json`

## Execution state

Blocked before Task 5 starts, as the plan expressly requires; there is no Task 5 start or completion record in `../progress.md`, so the next invocation selects Task 5 normally after the inputs arrive. No fixture, test, parser, source default or configuration example was changed for this task. All 19 fixtures still have `_assumed_shape: true`; `git diff --name-only HEAD -- tests/issue_watch` is empty. No live GitHub/Orca command, real watcher cycle, real-state lock, scheduler change, commit or push was run. No captured reply was fabricated and no live-test record was written.

Tasks 1 to 4 are independently reviewed and complete. The latest mocked watcher regression run passed all 2,655 tests (`t4-pytest.log`); that is not evidence of a live capture or of Task 5 completion. Lint/type checks were skipped for the Markdown-only delivery. The document-only `git diff --check` passed. A later `git diff --cached --check` reported trailing whitespace in saved raw diff context, logs containing those diffs and exact reviewer prompts; those historical evidence files are retained unchanged, not silently reformatted. This is an evidence-formatting warning, not a test failure or a live-runtime result. No whole-plan FINAL or archive runs while Task 5 remains unstarted.

The initial attempt to populate this note was blocked by the freshness hook because a Write did not count as a Read. The required Read was performed, then the dedicated Edit was retried; no alternative write path was used.

## Resume

The owner performs the live test and capture sheet in `docs/designs/issue-watcher-setup.md` sections 14.1 and 14.1.1, writes and commits `docs/designs/issue-watcher-live-test.md`, and supplies redacted replies under this package's `artifacts/captured/`, using the fixture filenames above. Each uncaptured error must be explicitly listed in the owner record as still assumed; recording a gap does not waive the original deployment gate. Keep `enabled` false.

After those owner-provided inputs exist, rerun:

```text
/sc:implement .dev/tasks/to-do/TASK-WF-rollOutTheIssueW-20261109-000305/TASK-WF-rollOutTheIssueW-20261109-000305.md
```

This invocation does not authorize any owner-only operation or acceptance of an unmet criterion.
