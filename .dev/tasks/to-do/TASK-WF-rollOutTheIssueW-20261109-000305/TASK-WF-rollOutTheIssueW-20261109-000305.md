---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-rollOutTheIssueW-20261109-000305
version: "1"
priority: Medium
created_date: "2026-11-09"
---

# Roll out the issue watcher: fix the design drift, prepare the owner-run rollout, swap in captured fixtures (issue #450)

Source: ./source.md
Goal: The design's stale status line and incomplete reason list are fixed; the owner runbook gives the owner a capture sheet for the live test (FU-1) and one ordered checklist for the shadow run, the lock and restart tests, the enable step and the cron entry (FU-2); and, once the owner has captured real `gh` and Orca replies, the 19 guessed fixtures are replaced by them with `uv run pytest tests/issue_watch/` passing. `enabled` is still `false` when this plan ends.

## Constraints

- Agent tasks change only `docs/designs/issue-watcher.md`, `docs/designs/issue-watcher-setup.md` (Tasks 1 to 4) and, in Task 5, the 19 files under `tests/issue_watch/fixtures/_assumed_shape/` and `tests/issue_watch/test_github.py`. No file under `src/` or `.claude/` changes.
- `enabled` stays `false`: the example configuration in section 2 of `docs/designs/issue-watcher-setup.md` (`"enabled": false`) and the default `raw.get("enabled", False)` in `src/superclaude/cli/issue_watch/cycle.py` are not touched by any task.
- No agent runs `gh`, `orca` or `superclaude issue-watch` against real GitHub or Orca, writes to GitHub, launches an Orca agent, takes the lock on a real state directory, edits a crontab or scheduler, commits or pushes. Those are owner-run items (listed below); the plan only writes them down.
- No agent writes `docs/designs/issue-watcher-live-test.md`. The design (section 1, "Deployment gate") and the runbook (section 14.1) say the owner writes and commits it.
- Task 2 adds one row to the exit-code table in section 4.3 of `docs/designs/issue-watcher.md`, which shifts the design line numbers that the fixture `source` fields cite by one. That is accepted: Task 5 rewrites the `source` field of every captured fixture. New text cites sections and table rows by name, never by line number.
- Out of scope: follow-ups FU-3 to FU-12, the owner questions Q1 to Q4 in section 16 of the design, the low regression fix recorded in the build's worker final report, renaming the `_assumed_shape` fixture directory, and any change to the parsers in `src/superclaude/cli/issue_watch/github.py` or `launch.py` (a captured shape that breaks a parser is recorded for a follow-up plan, never patched here).

Owner-run items (done by the owner with their own `gh` login and Orca; no agent runs them):
- Pre-flight, runbook section 1: `gh` login and scopes, the Orca CLI, the worktree origin, `superclaude issue-watch check-config`.
- The live test (FU-1), runbook section 14.1: one hand launch on a test issue with the Orca CLI while `enabled` is `false`, recording the permission mode (section 14.2) and capturing the replies listed in the capture sheet that Task 3 adds; then committing `docs/designs/issue-watcher-live-test.md`.
- Handing the captured replies to Task 5: redacted copies saved as `./artifacts/captured/<fixture name>` in this package, one per fixture listed in Task 5.
- The 24-hour shadow run, runbook section 7, and its review, section 8.1.
- The two-process lock test, runbook section 8.2, and the state-directory restart test, section 8.3.
- The staleness alert, section 8.4, and the committed live-test record, section 8.5.
- Changing `enabled` to `true`, section 8.6, only after every item above.
- Installing the cron entry `0 */5 * * * *` (six fields, seconds first) with a persisted `state_dir` (FU-2), after FU-1 and the shadow run.

## Phase 1: Correct the status line of the design

## Task 1: Replace the stale status line in docs/designs/issue-watcher.md

In `docs/designs/issue-watcher.md`, line 3 reads "**Status:** Design only, nothing implemented. Next: `/task-builder` with `--spec` on this file, then `/task`." The watcher was built and merged in PRs #447 and #448 (`src/superclaude/cli/issue_watch/`, `tests/issue_watch/`). Rewrite that one line, in place, so it states: implemented and merged in PRs #447 and #448, never run live, `enabled` ships as `false`, no schedule is installed, and the next step is the owner-run live test (FU-1) in section 14.1 of `docs/designs/issue-watcher-setup.md`. Then search the whole file for any other sentence that says the watcher is not implemented or is design only, and correct each hit the same way. The "built and tested with mocks only" wording of the section 1 scope table is true and stays.

Acceptance criteria:
- `grep -n "nothing implemented" docs/designs/issue-watcher.md` prints nothing.
- Line 3 names PRs #447 and #448, says the watcher has never run live, says `enabled` is `false` and nothing is scheduled, and points at FU-1 and section 14.1 of `docs/designs/issue-watcher-setup.md`; it no longer names `/task-builder` or `/task`.
- The output of `grep -n -i -E "not implemented|design only|not yet built" docs/designs/issue-watcher.md` is saved to `./artifacts/t1-status-search.log`, and every hit is either corrected or noted in that log as being about something else.
- The file still has the same number of lines as before the task (the status line is replaced in place).

## Phase 2: Make the design's reason list match the code

## Task 2: Name all 59 reason codes in docs/designs/issue-watcher.md

Depends on: Task 1

`REASON_TABLE` in `src/superclaude/cli/issue_watch/audit.py` holds 59 names; `audit.REASONS` is the frozenset of its keys. The design never lists them: section 10.1 says the `reason` key is an "enum (spec reason table)" and that "`audit.REASONS` is a `frozenset` equal to the spec's reason table", and the exit-code table in section 4.3 has no row for exit 1 and does not name `cycle_complete`. The two names the build added are `cycle_complete` (cycle line, exit 0) and `cycle_crashed` (cycle line, exit 1, written by `once` only for an unexpected exception), both marked [PROPOSAL] in `audit.py`. The full 59-name table, grouped by exit code, already exists in section 10.2 of `docs/designs/issue-watcher-setup.md`; the design points at it rather than keeping a second copy.

Make these edits in `docs/designs/issue-watcher.md`:
- Section 10.1, the `reason` row of the audit line table: replace "enum (spec reason table)" with an enum reference to `audit.REASON_TABLE` (59 names).
- Section 10.1, the sentence that begins "`rate_remaining`, titles, bodies": replace "equal to the spec's reason table" with: the 59 keys of `audit.REASON_TABLE`, which are the spec's reason table plus the two [PROPOSAL] names `cycle_complete` and `cycle_crashed` added during the build; the full table, grouped by exit code, is section 10.2 of `issue-watcher-setup.md`. Keep the rest of that sentence (the `ValueError` rule) unchanged.
- Section 4.3: in the exit 0 row, add `cycle_complete` to the "Reasons that produce it" cell; add one row for exit 1 with the meaning "An unexpected exception out of the cycle, written by `once` only ([PROPOSAL])" and the reason `cycle_crashed`, placed between the 0 and 2 rows.

Acceptance criteria:
- `grep -c "cycle_complete" docs/designs/issue-watcher.md` and `grep -c "cycle_crashed" docs/designs/issue-watcher.md` each print at least 2.
- `grep -n "spec reason table\|equal to the spec's reason table" docs/designs/issue-watcher.md` prints nothing.
- The section 4.3 table has a row whose first cell is `1` naming `cycle_crashed`, and its exit 0 row names `cycle_complete`.
- Every reason name in section 4.3 of the design is a key of `REASON_TABLE`: the check (a loop over the backticked names in that table, each tested with `grep -c "\"<name>\":" src/superclaude/cli/issue_watch/audit.py`) and its output are saved to `./artifacts/t2-reason-check.log`, with zero misses.
- The section 10.2 table in `docs/designs/issue-watcher-setup.md` is unchanged (`git diff --stat docs/designs/issue-watcher-setup.md` shows no change from this task).

## Phase 3: Prepare the owner-run rollout in the runbook

## Task 3: Add a live-test capture sheet to section 14.1 of docs/designs/issue-watcher-setup.md

Depends on: Task 2

Section 14.1 of `docs/designs/issue-watcher-setup.md` says the live test must capture Orca's real replies and the real shapes of the issue events, `lastEditedAt` and `projectItems`, and replace every `_assumed_shape` fixture, but it does not say which command produces each fixture. Add a subsection "14.1.1 Capture sheet" after the four bullets of 14.1 with one table row per fixture file in `tests/issue_watch/fixtures/_assumed_shape/`. Columns: fixture file; what it stands for (take it from the fixture's own `source` and `note` fields); the command or situation that produces the real reply (the argv comes from the builders in `src/superclaude/cli/issue_watch/github.py` and `src/superclaude/cli/issue_watch/launch.py`, written with placeholders such as `<test issue>` and `<project id>`, never real values); and whether it can be produced on demand.

The 19 rows, one each: `gh_issue_list.json`, `gh_issue_reread.json`, `gh_api_user_include.json`, `gh_api_user_include_429.json`, `rest_events_page.json`, `rest_comments_marker.json`, `graphql_edits.json`, `graphql_project_items.json`, `gh_graphql_rate_limited.json`, `gh_graphql_insufficient_scopes.json`, `gh_stderr_auth_401.json`, `gh_stderr_rate_403.json`, `gh_stderr_rate_429.json`, `gh_stderr_http_502.json`, `gh_stderr_scope_read_project.json`, `orca_launch_success.json`, `orca_launch_unknown.json`, `orca_launch_no_operation_id.json`, `orca_launch_empty_operation_id.json`.

Mark the error replies that cannot be provoked on demand (rate limits, HTTP 502, a lost Orca reply) as "capture if seen; otherwise the record says it stayed assumed". Below the table add three short rules: save each reply exactly as the command printed it (stdout, or stderr for the `gh_stderr_*` rows), one file per fixture named after it; before handing a file over, replace real logins, numeric ids, node ids, issue titles, bodies and any token with placeholder values of the same type; and list in the live-test record every fixture that was not captured. Do not change the existing four bullets or the paragraph that follows them.

Acceptance criteria:
- Section 14.1 of `docs/designs/issue-watcher-setup.md` has a "14.1.1 Capture sheet" subsection whose table has exactly 19 data rows, one per file listed above; the check (each file name grepped once in the section) is saved to `./artifacts/t3-sheet-check.log`.
- Every argv in the table matches a builder in `github.py` or `launch.py`; each row's builder function name is recorded in `./artifacts/t3-sheet-check.log`.
- The table holds no real login, issue number, node id or token: only placeholders in angle brackets.
- The redaction rule and the "list every uncaptured fixture in the record" rule are present.
- The original four bullets and the paragraph after them in 14.1 are byte-identical to before (shown by `git diff` of that section in the log).

## Task 4: Add the ordered owner checklist and the cron install step to docs/designs/issue-watcher-setup.md

Depends on: Task 3

The runbook already describes each owner step (section 7 shadow run, 8.1 review, 8.2 lock test, 8.3 restart test, 8.4 staleness alert, 8.5 live-test record, 8.6 set enabled, 14.1 live test), but they are spread over two places, with the live test in section 14 although it must come first, and the cron entry (FU-2) has only a one-line mention at the end of 8.6. Make two edits:
- Add a subsection "8.7 Install the cron entry (FU-2)" after 8.6. It says: only after 8.6; the schedule is `0 */5 * * * *` (six fields, seconds first: every 5 minutes, at second 0); the scheduled command is `superclaude issue-watch once` (with `--config <path>` when the configuration file is not at the default path); run `superclaude issue-watch check-config` first and confirm the `state_dir` it prints is on storage that survives a workspace restart, setting `state_dir` in the configuration file when `$HOME` is not persistent; after the first scheduled cycles, `superclaude issue-watch status` exits 0. Keep the existing sentence that the scheduler is the owner's choice; do not name a scheduler product the runbook does not already name. Move the one-line cron mention from 8.6 into 8.7 rather than repeating it.
- Add a section "16. Rollout checklist" at the end of the file: a bulleted list (plain `-` bullets, no checkboxes, no numbers) in this order, each bullet one sentence that links to the section that holds the detail: pre-flight (section 1); configuration with `enabled: false` (section 2); approvers file, labels, `init-state` (sections 3 to 5); the live test with the capture sheet and the committed record (section 14.1, 14.1.1, 8.5); the captured replies replace the fixtures and `uv run pytest tests/issue_watch/` passes; the 24-hour shadow run (section 7) and its review (8.1); the lock test (8.2); the restart test (8.3); the staleness alert (8.4); set `enabled` to `true` (8.6); install the cron entry (8.7). The list opens with one sentence saying every item is run by the owner and nothing in the implementation runs any of it.

Acceptance criteria:
- `docs/designs/issue-watcher-setup.md` has a "8.7 Install the cron entry (FU-2)" subsection containing `0 */5 * * * *`, `superclaude issue-watch once`, `check-config`, `state_dir` and `status`, and section 8.6 no longer carries its own cron sentence (`grep -c '0 \*/5 \* \* \* \*'` counts one in 8.7 plus the unchanged FU-2 row of 15.3).
- A "16. Rollout checklist" section exists with the eleven bullets in the order above, each linking to its section; it has no `- [ ]` and no numbered lines.
- `grep -n '"enabled": false' docs/designs/issue-watcher-setup.md` still finds the section 2 example, and the checklist puts "set `enabled` to `true`" after the live test, shadow run, lock and restart bullets and before the cron bullet.
- The FU-1 and FU-2 rows of section 15.3 are unchanged.
- The checks above and their output are saved to `./artifacts/t4-checklist-check.log`.

## Phase 4: Replace the guessed fixtures with the owner's captured replies

## Task 5: Swap the captured replies into tests/issue_watch/fixtures/_assumed_shape/

Depends on: Task 4

This task can start only after the owner-run live test. Precondition, checked first: `docs/designs/issue-watcher-live-test.md` exists in the checkout, and `./artifacts/captured/` in this package holds the redacted replies the owner captured, one file per fixture name from the Task 3 list. If the precondition fails, the task stops as blocked, writes the missing items to `./artifacts/t5-blocked.md`, and changes no file.

For each of the 19 fixture files in `tests/issue_watch/fixtures/_assumed_shape/` that has a captured file: replace the `payload` value with the captured reply (stdout JSON parsed, or the stderr text in the same field layout the fixture already uses), set `"_assumed_shape": false`, set `source` to a string naming `docs/designs/issue-watcher-live-test.md` and the capture date from that record, and replace `note` with one sentence saying what was captured. A fixture with no captured file stays as it is, with `"_assumed_shape": true`, and must be listed as uncaptured in the live-test record.

In `tests/issue_watch/test_github.py`, change `test_every_assumed_shape_fixture_parses_and_is_labelled` so it still asserts 19 files and a non-empty `source`, asserts that `_assumed_shape` is a bool, and asserts that every file with `_assumed_shape` false has a `source` naming `issue-watcher-live-test.md`. Leave `test_every_assumed_shape_fixture_is_read_by_a_test__df32` and the loaders in `tests/issue_watch/conftest.py`, `test_github.py` and `test_launch.py` unchanged; the file names do not change.

If `uv run pytest tests/issue_watch/` then fails because a captured shape differs from what a parser in `src/superclaude/cli/issue_watch/github.py` or `launch.py` expects (for example the operation id path in `launch.OPERATION_ID_PATHS`), do not change `src/`: write each mismatch (fixture, failing test, expected and captured shape) to `./artifacts/t5-shape-mismatch.md` and stop the task as failed so a follow-up plan can change the parser.

Acceptance criteria:
- Every fixture with a captured file has `"_assumed_shape": false` and a `source` naming `docs/designs/issue-watcher-live-test.md`; the list of swapped and unswapped fixtures is saved to `./artifacts/t5-swap-list.md`, and every unswapped one appears as uncaptured in the live-test record.
- No fixture contains a token-shaped string: `grep -r -E "gh[pousr]_[A-Za-z0-9]{20,}|github_pat_" tests/issue_watch/fixtures/` prints nothing.
- `uv run pytest tests/issue_watch/ -q` passes; its output is saved to `./artifacts/t5-pytest.log`.
- `git diff --name-only` for this task lists only files under `tests/issue_watch/fixtures/_assumed_shape/` and `tests/issue_watch/test_github.py`.
