---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-rollOutTheIssueW-20261108-235821
version: "1"
priority: Medium
created_date: "2026-11-08"
---

# Roll out the issue watcher: doc fixes and owner-run rollout preparation (issue #450)

Source: ./source.md
Goal: The two design drifts are fixed, and the owner has everything written down to run the live test (FU-1), swap the guessed fixtures for captured replies, run the shadow run, the lock test and the restart test, flip `enabled`, and install the cron entry (FU-2), with `enabled` still `false` when this plan ends.

## Constraints

- Documentation only. This plan changes `docs/designs/issue-watcher.md` and `docs/designs/issue-watcher-setup.md`. It changes nothing under `src/`, `tests/` or `.claude/`.
- `enabled` stays `false`: the example configuration in section 2 of `docs/designs/issue-watcher-setup.md` and the default read in `src/superclaude/cli/issue_watch/cycle.py` are not touched. Only the owner flips it, after the checklist of Task 5.
- No agent runs the live test, captures a real `gh` or Orca reply, replaces a fixture, runs the shadow run, takes the lock or restart test, enables the watcher or installs the cron entry. Those need the owner's own `gh` login and Orca. This plan prepares them as owner-run steps. The fixture replacement itself is NOT BUILT by this plan: it can only happen after the owner has captured the replies.
- This plan does not write `docs/designs/issue-watcher-live-test.md`. The design and the runbook say the owner writes it.
- No GitHub write, no Orca launch, no commit, no push in any task.
- Edits to `docs/designs/issue-watcher.md` shift the line numbers that the 19 fixture files under `tests/issue_watch/fixtures/_assumed_shape/` cite in their `source` fields. That is accepted: FU-1 replaces those files. New text added by this plan cites sections and table rows by name, never by line number.
- Out of scope: the unrechecked low regression fix R-1 recorded in the build's worker final report, and follow-ups FU-3 to FU-12.

## Phase 1: Correct the status line of the design

## Task 1: Replace the stale status line in docs/designs/issue-watcher.md

In `docs/designs/issue-watcher.md`, line 3 reads "**Status:** Design only, nothing implemented. Next: `/task-builder` with `--spec` on this file, then `/task`." The watcher was built and merged in PRs #447 and #448 (`src/superclaude/cli/issue_watch/`, `tests/issue_watch/`). Rewrite that one line so it states the true state: implemented and merged, never run live, `enabled` ships as `false`, no schedule installed, and the next step is the owner-run live test (FU-1) described in `docs/designs/issue-watcher-setup.md` section 14.1. Search the whole file for any other sentence that still says the watcher is not implemented and correct each one the same way. Leave the section 1 scope table as it is: its "built and tested with mocks only" wording is true.

Acceptance criteria:
- `grep -n "nothing implemented" docs/designs/issue-watcher.md` prints nothing.
- The new status line names PRs #447 and #448, says the watcher has never run live, and says `enabled` is `false` and nothing is scheduled.
- The new status line points at FU-1 and at `docs/designs/issue-watcher-setup.md` section 14.1 as the next step, and no longer names `/task-builder` or `/task`.
- The grep output of the search for other "not implemented" claims is saved to `./artifacts/t1-status-search.log`, and every hit is either corrected or shown to be about something else.

## Phase 2: List the full reason table in the design

## Task 2: List all 59 reason names in docs/designs/issue-watcher.md

Depends on: Task 1

The closed table `REASON_TABLE` in `src/superclaude/cli/issue_watch/audit.py` (lines 26 to 102) holds 59 names: 27 cycle reasons, 17 skip, 9 entry, 4 warning, 1 note (`re-approved`) and 1 skip/warning (`operator_reset`). The design names the table only as "the spec's reason table" (section 10.1, the `reason` row and the paragraph under the schema table) and its exit-code table (section 4.3) omits two names the code added: `cycle_complete` (kind cycle, exit 0, a cycle that ran to its end) and `cycle_crashed` (kind cycle, exit 1, an unexpected exception ended `once`; written to stderr only, no audit line). Make three edits in `docs/designs/issue-watcher.md`. First, in the section 4.3 table add `cycle_complete` to the exit 0 row and add an exit 1 row for `cycle_crashed`. Second, in section 10.1 replace the two "spec reason table" references with a statement that `audit.REASON_TABLE` holds 59 names, that the spec lists 57, and that `cycle_complete` and `cycle_crashed` are the two additions, marked [PROPOSAL] and to be confirmed or renamed after the shadow run, as `docs/designs/issue-watcher-setup.md` section 10.2 already says. Third, add a short subsection at the end of section 10.1 with a table of all 59 names, each with its kind and exit code copied from `audit.py`; meanings stay in `docs/designs/issue-watcher-setup.md` section 10.2, which the subsection links to instead of repeating.

Acceptance criteria:
- A command that imports `superclaude.cli.issue_watch.audit` through `uv run python` and checks that every key of `REASON_TABLE` occurs in `docs/designs/issue-watcher.md` reports 59 of 59 present. Its output is saved to `./artifacts/t2-reason-names.log`.
- The same command checks that the kind and exit code written for each name in the new table equal the values in `REASON_TABLE`, and reports no mismatch.
- The section 4.3 table has an exit 1 row naming `cycle_crashed` and lists `cycle_complete` under exit 0.
- `grep -n "spec reason table\|spec's reason table" docs/designs/issue-watcher.md` prints nothing.
- The text states the counts 59 and 57 and names `cycle_complete` and `cycle_crashed` as the two additions.

## Phase 3: Prepare the live test and the fixture swap

## Task 3: Add a live-test capture sheet to docs/designs/issue-watcher-setup.md

Depends on: Task 2

Add a new subsection 14.3, "Live-test capture sheet", to `docs/designs/issue-watcher-setup.md`, after section 14.2. It is a table with one row for each of the 19 files in `tests/issue_watch/fixtures/_assumed_shape/`: `gh_api_user_include.json`, `gh_api_user_include_429.json`, `gh_graphql_insufficient_scopes.json`, `gh_graphql_rate_limited.json`, `gh_issue_list.json`, `gh_issue_reread.json`, `gh_stderr_auth_401.json`, `gh_stderr_http_502.json`, `gh_stderr_rate_403.json`, `gh_stderr_rate_429.json`, `gh_stderr_scope_read_project.json`, `graphql_edits.json`, `graphql_project_items.json`, `orca_launch_empty_operation_id.json`, `orca_launch_no_operation_id.json`, `orca_launch_success.json`, `orca_launch_unknown.json`, `rest_comments_marker.json` and `rest_events_page.json`. Each row has: the fixture file, the call it stands for (the argv builders G1 to G7 in `src/superclaude/cli/issue_watch/github.py` and `launch_argv` in `src/superclaude/cli/issue_watch/launch.py`, lines 95 to 117), the exact read-only command the owner runs to capture it with the repository named explicitly as `IronbellyOrg/IronClaude`, the shape facts the capture must confirm (taken from the fixture's own `source` and `note` fields and from the UNVERIFIED rows of section 15 of `docs/designs/issue-watcher.md`), and the test files that read it. Rows for replies that cannot be produced on demand (HTTP 401 with a bad token, 403 or 429 rate limits, 502, Orca's `agent_session_operation_unknown`) say how to provoke the reply safely or, where no safe way exists, that the owner records "not provoked" with the reason in the live-test record and keeps that fixture labelled as assumed. Below the table, state what the live-test record must contain (the slash-command check of section 14.1, the permission mode of section 14.2, how the launch was run by hand while `enabled` is `false`, and one line per fixture saying captured or not provoked) and the redaction rule: never commit a token or an `Authorization` header, and a login or account id may be replaced by the test placeholders `owner-login` and `1001` only if the key names, nesting, value types and header layout stay as captured.

Acceptance criteria:
- The table in `docs/designs/issue-watcher-setup.md` has exactly 19 rows and each file name above appears in it once. A command that lists `tests/issue_watch/fixtures/_assumed_shape/*.json` and checks each basename against the section 14.3 text reports 19 of 19 present, with its output saved to `./artifacts/t3-fixture-rows.log`.
- Every capture command in the table is read-only against GitHub and Orca (no `--method POST`, `PATCH` or `DELETE`, no label, comment or assignee write) and no `gh` command in it lacks an explicit `IronbellyOrg/IronClaude` repository where the command takes one.
- Each capture command matches the argv built by the named builder in `github.py` or `launch.py`; a mismatch found while writing is reported in the task log, not silently changed.
- The text under the table states what the live-test record contains and the redaction rule, and names `docs/designs/issue-watcher-live-test.md` as written by the owner, not by this plan.

## Task 4: Add the fixture-swap procedure to docs/designs/issue-watcher-setup.md

Depends on: Task 3

Add a subsection 14.4, "Replacing the fixtures", to `docs/designs/issue-watcher-setup.md`. It tells the owner how to swap each guessed file for a captured one without breaking the suite. Read these before writing it: `tests/issue_watch/conftest.py` (`FIXTURE_DIR` at line 307 and `load_fixture` at line 323), `tests/issue_watch/test_github.py` (the guard tests at lines 575 to 596, which pin 19 files, require `"_assumed_shape": true` and a non-empty `source` string in each file, and require every file name to appear quoted in some `test_*.py`), `tests/issue_watch/test_launch.py` (`FIXTURES` at line 609 and the tests at lines 773 to 899 that pin `OPERATION_ID_PATHS`), `src/superclaude/cli/issue_watch/launch.py` (`OPERATION_ID_PATHS`, near line 41) and the stderr classifier and projections in `src/superclaude/cli/issue_watch/github.py` (`classify`, the `*_JQ` constants and `scope_stderr`). The procedure states: swap one fixture at a time; keep the file name so the loading tests keep working; run `uv run pytest tests/issue_watch/ -q` after each swap; when a capture contradicts a constant in the code (an operation id path, a stderr substring, a jq projection, a field name) the code constant changes in the same step with a failing-first test; the guard tests in `test_github.py` have to change at the end, because they require the `_assumed_shape` label that a captured file no longer carries, so state the new rule they should enforce (every file is either captured, with the command and capture date recorded, or still labelled assumed with the reason from the live-test record); and the closing check is a full `uv run pytest tests/issue_watch/` plus `make lint`, both passing. New fixture files cite the design and runbook by section name, never by line number.

Acceptance criteria:
- Section 14.4 names each of the five files above and the line or symbol the owner has to look at in each, and every named file, line and symbol exists as described (checked by reading each one; the check notes go to `./artifacts/t4-references.log`).
- Section 14.4 states the per-swap test command and the closing commands exactly: `uv run pytest tests/issue_watch/ -q`, `uv run pytest tests/issue_watch/` and `make lint`.
- Section 14.4 says the guard tests in `tests/issue_watch/test_github.py` must be reworked and states the replacement rule, and says nothing in this plan changes them.
- `git diff --stat` shows no change under `src/` or `tests/`.

## Phase 4: Write the owner rollout checklist

## Task 5: Add the owner-run rollout checklist to docs/designs/issue-watcher-setup.md

Depends on: Task 3, Task 4

Add a new section 16, "Rollout checklist (owner-run)", at the end of `docs/designs/issue-watcher-setup.md` as an ordered list of unchecked task-list items, with a one-line pointer to it at the end of the intro of section 8 ("Before cron"). Each item names who runs it (the owner), the section that holds the commands, the evidence to keep, and the condition for moving on. The items, in order: run the live test of section 14.1 and commit `docs/designs/issue-watcher-live-test.md` (section 8.5); swap the fixtures by sections 14.3 and 14.4 with `uv run pytest tests/issue_watch/` passing; run the 24-hour shadow run of section 7 and review it by section 8.1; run the two-process lock test of section 8.2 and expect `lock_held` with exit 75, then a normal run; run the state-directory restart test of section 8.3 and expect the same `created_at` and `status` not exiting 6; wire and check the staleness alert of section 8.4; list the issues that carry both labels and keep the kill switch of section 9 at hand, then change `"enabled"` to `true` as in section 8.6 and run `check-config`; install the six-field cron entry `"0 */5 * * * *"` (seconds first, every 5 minutes) on the host scheduler, running `superclaude issue-watch once` with `--config <path>` when the configuration file is not at the default path, and use a persisted `state_dir` if `$HOME` does not persist (FU-2, section 15.3); after the first real cycle ends with exit 0 and `cycle_complete`, confirm `superclaude issue-watch status` exits 0; schedule the SLO review of FU-10 for 7 days after going live. The checklist links to the existing sections for commands instead of copying them. The scheduler itself (the Coder template and its `coder_script` cron) is the owner's choice and out of scope, and the section says so.

Acceptance criteria:
- Section 16 exists in `docs/designs/issue-watcher-setup.md`, lists the ten stages above in that order, and every stage names a section number that exists in the file (checked by `grep -n "^## \|^### " docs/designs/issue-watcher-setup.md` against the cited numbers; output in `./artifacts/t5-section-refs.log`).
- The cron entry appears exactly as `0 */5 * * * *` with the six-field and seconds-first explanation, and it comes after the `enabled` stage and after the live-test, shadow-run, lock and restart stages.
- The text says `enabled` stays `false` until the owner flips it, and the example in section 2 still shows `"enabled": false` (`grep -n '"enabled": false' docs/designs/issue-watcher-setup.md` finds it).
- Section 8 carries a one-line pointer to section 16, and no existing command block in sections 8 and 14 is changed.
- `git diff --stat` shows changes only in `docs/designs/issue-watcher.md` and `docs/designs/issue-watcher-setup.md`, and `uv run pytest tests/issue_watch/ -q` still passes.
