start=03e5816196f4b9ac896c1f0d644304966686cd21
Review one task for spec compliance.

Task brief: Task 3: Add a live-test capture sheet to section 14.1 of docs/designs/issue-watcher-setup.md

Depends on: Task 2

Section 14.1 of `docs/designs/issue-watcher-setup.md` says the live test must capture Orca's real replies and the real shapes of the issue events, `lastEditedAt` and `projectItems`, and replace every `_assumed_shape` fixture, but it does not say which command produces each fixture. Add a subsection "14.1.1 Capture sheet" after the four bullets of 14.1 with one table row per fixture file in `tests/issue_watch/fixtures/_assumed_shape/`. Columns: fixture file; what it stands for (take it from the fixture's own `source` and `note` fields); the command or situation that produces the real reply (the argv comes from the builders in `src/superclaude/cli/issue_watch/github.py` and `src/superclaude/cli/issue_watch/launch.py`, written with placeholders such as `<test issue>` and `<project id>`, never real values); and whether it can be produced on demand.

The 19 rows, one each: `gh_issue_list.json`, `gh_issue_reread.json`, `gh_api_user_include.json`, `gh_api_user_include_429.json`, `rest_events_page.json`, `rest_comments_marker.json`, `graphql_edits.json`, `graphql_project_items.json`, `gh_graphql_rate_limited.json`, `gh_graphql_insufficient_scopes.json`, `gh_stderr_auth_401.json`, `gh_stderr_rate_403.json`, `gh_stderr_rate_429.json`, `gh_stderr_http_502.json`, `gh_stderr_scope_read_project.json`, `orca_launch_success.json`, `orca_launch_unknown.json`, `orca_launch_no_operation_id.json`, `orca_launch_empty_operation_id.json`.

Mark the error replies that cannot be provoked on demand (rate limits, HTTP 502, a lost Orca reply) as "capture if seen; otherwise the record says it stayed assumed". Below the table add three short rules: save each reply exactly as the command printed it (stdout, or stderr for the `gh_stderr_*` rows), one file per fixture named after it; before handing a file over, replace real logins, numeric ids, node ids, issue titles, bodies and any token with placeholder values of the same type; and list in the live-test record every fixture that was not captured. Do not change the existing four bullets or the paragraph that follows them.

Acceptance criteria:
T3.AC1: Section 14.1 of `docs/designs/issue-watcher-setup.md` has a "14.1.1 Capture sheet" subsection whose table has exactly 19 data rows, one per file listed above; the check (each file name grepped once in the section) is saved to `./artifacts/t3-sheet-check.log`.
T3.AC2: Every argv in the table matches a builder in `github.py` or `launch.py`; each row's builder function name is recorded in `./artifacts/t3-sheet-check.log`.
T3.AC3: The table holds no real login, issue number, node id or token: only placeholders in angle brackets.
T3.AC4: The redaction rule and the "list every uncaptured fixture in the record" rule are present.
T3.AC5: The original four bullets and the paragraph after them in 14.1 are byte-identical to before (shown by `git diff` of that section in the log).
Global constraints: 
- Agent tasks change only `docs/designs/issue-watcher.md`, `docs/designs/issue-watcher-setup.md` (Tasks 1 to 4) and, in Task 5, the 19 files under `tests/issue_watch/fixtures/_assumed_shape/` and `tests/issue_watch/test_github.py`. No file under `src/` or `.claude/` changes.
- `enabled` stays `false`: the example configuration in section 2 of `docs/designs/issue-watcher-setup.md` (`"enabled": false`) and the default `raw.get("enabled", False)` in `src/superclaude/cli/issue_watch/cycle.py` are not touched by any task.
- No agent runs `gh`, `orca` or `superclaude issue-watch` against real GitHub or Orca, writes to GitHub, launches an Orca agent, takes the lock on a real state directory, edits a crontab or scheduler, commits or pushes. Those are owner-run items (listed below); the plan only writes them down.
- No agent writes `docs/designs/issue-watcher-live-test.md`. The design (section 1, "Deployment gate") and the runbook (section 14.1) say the owner writes and commits it.
- Task 2 adds one row to the exit-code table in section 4.3 of `docs/designs/issue-watcher.md`, which shifts the design line numbers that the fixture `source` fields cite by one. That is accepted: Task 5 rewrites the `source` field of every captured fixture. New text cites sections and table rows by name, never by line number.
- Out of scope: follow-ups FU-3 to FU-12, the owner questions Q1 to Q4 in section 16 of the design, the low regression fix recorded in the build's worker final report, renaming the `_assumed_shape` fixture directory, and any change to the parsers in `src/superclaude/cli/issue_watch/github.py` or `launch.py` (a captured shape that breaks a parser is recorded for a follow-up plan, never patched here).


Start sha: 03e5816196f4b9ac896c1f0d644304966686cd21
Diff against the start snapshot: diff --git a/docs/designs/issue-watcher-setup.md b/docs/designs/issue-watcher-setup.md
index 5f43bed80..7ddeffccf 100644
--- a/docs/designs/issue-watcher-setup.md
+++ b/docs/designs/issue-watcher-setup.md
@@ -584,6 +584,36 @@ No cron entry is enabled and `enabled` stays `false` until you have run one live
 - capture Orca's real replies for a successful launch and for an `unknown` outcome, and the real shapes of the issue events, the `lastEditedAt` field and the `projectItems` field;
 - replace every `_assumed_shape` fixture in `tests/issue_watch/` with those captured replies, with `uv run pytest tests/issue_watch/` still passing.
 
+#### 14.1.1 Capture sheet
+
+These are owner-run commands, not commands run by the implementation. Replace angle-bracket placeholders before running them; `<orca>` is the binary accepted in section 1.2. The query and projection placeholders `<EDITS_QUERY>`, `<PROJECT_ITEMS_QUERY>`, `<EVENTS_JQ>`, `<MARKER_JQ>` and `<REREAD_JQ>` mean the exact string constants of those names in `src/superclaude/cli/issue_watch/github.py`, not the placeholder text itself. For another page, use `<page>` or append `-f 'after=<cursor>'` to the GraphQL commands, as their builders do. The Project query returns all items; compare `<project id>` locally, not as an extra command argument. Capturing gaps does not waive the deployment gate above.
+
+| Fixture file | What it stands for | Command or situation producing the reply | On demand? |
+|---|---|---|---|
+| `gh_issue_list.json` | Discovery JSON: issue number, label names, assignee logins and open state | `gh issue list --repo IronbellyOrg/IronClaude --state open --label '<trigger label>' --assignee '<owner login>' --json number,labels,assignees,state -L 100` | Yes, with prepared test issues |
+| `gh_issue_reread.json` | Projected REST issue re-read, including lower-case state and label/assignee arrays | `gh api --method GET 'repos/IronbellyOrg/IronClaude/issues/<test issue>' --jq '<REREAD_JQ>'` | Yes |
+| `gh_api_user_include.json` | Own login and account id with the HTTP status line, headers and blank line | `gh api user --include` | Yes |
+| `gh_api_user_include_429.json` | Rate-limited login reply with headers, Retry-After and accompanying stderr | `gh api user --include` when it returns HTTP 429; preserve stdout and accompanying stderr separately | No: capture if seen; otherwise the record says it stayed assumed |
+| `rest_events_page.json` | Projected label/unlabel/rename events, actor fields and nulls | `gh api --method GET 'repos/IronbellyOrg/IronClaude/issues/<test issue>/events' -F per_page=100 -F 'page=<page>' --jq '<EVENTS_JQ>'` | Yes for prepared events; record null/deleted-actor cases only if seen |
+| `rest_comments_marker.json` | Projected comment ids, logins, times and claim-marker booleans, including null login | `gh api --method GET 'repos/IronbellyOrg/IronClaude/issues/<test issue>/comments' -F per_page=100 -F 'page=<page>' --jq '<MARKER_JQ>'` | Yes for prepared comments; record null-login cases only if seen |
+| `graphql_edits.json` | Issue/comment edit timestamps, null lastEditedAt or author, and comment paging | `gh api graphql -f 'query=<EDITS_QUERY>' -F 'number=<test issue>'` | Yes for test issue edits; deleted-author cases only if seen |
+| `graphql_project_items.json` | Project items, archived flag, Project node id, Status value and paging | `gh api graphql -f 'query=<PROJECT_ITEMS_QUERY>' -F 'number=<test issue>'` | Yes with a test issue on `<project id>` |
+| `gh_graphql_rate_limited.json` | GraphQL RATE_LIMITED error type and message | `gh api graphql -f 'query=<PROJECT_ITEMS_QUERY>' -F 'number=<test issue>'` when rate limited | No: capture if seen; otherwise the record says it stayed assumed |
+| `gh_graphql_insufficient_scopes.json` | GraphQL INSUFFICIENT_SCOPES error type and message | `gh api graphql -f 'query=<PROJECT_ITEMS_QUERY>' -F 'number=<test issue>'` with a separate test credential lacking Project read access | With a controlled test credential, if GitHub returns this form |
+| `gh_stderr_auth_401.json` | HTTP 401 authentication-failure stderr and login advice | `gh api user --include` with a separate invalid test credential; capture stderr | With a controlled test credential |
+| `gh_stderr_rate_403.json` | HTTP 403 rate-limit stderr | `gh api user --include` when a secondary rate limit returns HTTP 403; capture stderr | No: capture if seen; otherwise the record says it stayed assumed |
+| `gh_stderr_rate_429.json` | HTTP 429 rate-limit stderr | `gh api user --include` when rate limited with HTTP 429; capture stderr | No: capture if seen; otherwise the record says it stayed assumed |
+| `gh_stderr_http_502.json` | HTTP 502 transient-failure stderr | `gh api --method GET 'repos/IronbellyOrg/IronClaude/issues/<test issue>/events' -F per_page=100 -F 'page=<page>' --jq '<EVENTS_JQ>'` during a gateway failure; capture stderr | No: capture if seen; otherwise the record says it stayed assumed |
+| `gh_stderr_scope_read_project.json` | Missing read:project scope stderr | `gh api graphql -f 'query=<PROJECT_ITEMS_QUERY>' -F 'number=<test issue>'` with a separate test credential lacking Project read access; capture stderr | With a controlled test credential, if GitHub returns this form |
+| `orca_launch_success.json` | Successful launch JSON, outcome, receipt detail and non-empty operation id | `<orca> agent launch --agent claude --worktree 'path:<worktree>' --surface terminal --prompt '/sc:issue --claim <test issue>' --json` | Yes: the single owner-run test launch |
+| `orca_launch_unknown.json` | Lost-reply error JSON on stderr, unknown-outcome code and error operation id | `<orca> agent launch --agent claude --worktree 'path:<worktree>' --surface terminal --prompt '/sc:issue --claim <test issue>' --json` if the launch reply is lost; preserve the actual error channel | No: capture if seen; otherwise the record says it stayed assumed |
+| `orca_launch_no_operation_id.json` | Exit-0 launch JSON with no operation id, treated as unknown | `<orca> agent launch --agent claude --worktree 'path:<worktree>' --surface terminal --prompt '/sc:issue --claim <test issue>' --json` if its exit-0 reply omits the id | No: capture if seen; otherwise the record says it stayed assumed |
+| `orca_launch_empty_operation_id.json` | Exit-0 launch JSON with an empty operation id, treated as unknown | `<orca> agent launch --agent claude --worktree 'path:<worktree>' --surface terminal --prompt '/sc:issue --claim <test issue>' --json` if its exit-0 reply has an empty id | No: capture if seen; otherwise the record says it stayed assumed |
+
+- Save each reply exactly as the command printed it, one file per fixture named after that fixture: stdout normally, stderr for the `gh_stderr_*` rows and the Orca error row; retain accompanying stderr separately where the fixture uses both channels, without rewriting the reply shape.
+- Before handing a file over, replace real logins, numeric ids, node ids, issue titles, bodies and any token with placeholder values of the same type, keeping JSON numbers numeric and nulls unchanged.
+- List every fixture that was not captured in the live-test record, explicitly saying it stayed assumed; never manufacture an error reply or repeat a launch to fill the sheet.
+
 You commit the record as `docs/designs/issue-watcher-live-test.md`. The design and the implementation do not write it. The design says only "one owner-run launch on a test issue" and does not say how to run it while `enabled` is `false`. Launch it by hand with the Orca CLI while `enabled` is still `false`, and say in the record exactly how you did it. Do not run a real `once` with `enabled` set to `true` for the test: such a cycle examines up to 10 candidates and launches the first eligible one, which need not be the test issue, and the safeguards of section 8.6 (list the issues that carry both labels first, keep the kill switch of section 9 at hand) apply only once the test has passed. `enabled` changes to `true` only in section 8.6.
 
 ### 14.2 Permissions of the launched session

Full new evidence files: .dev/tasks/to-do/TASK-WF-rollOutTheIssueW-20261109-000305/artifacts/t3-sheet-check.log and .dev/tasks/to-do/TASK-WF-rollOutTheIssueW-20261109-000305/artifacts/t3-check.py (read current contents).
Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

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
