# Owner manual check for issue 438

No step of this plan wrote to GitHub. Everything below needs a real run by the owner, after the change is merged.

## Observed follow-up checks (2026-11-09)

The owner authorized running the check before submission. The parent session exercised the same GitHub calls directly, not the new skill end to end:

- Feature probe https://github.com/IronbellyOrg/IronClaude/issues/460: type `Test` and label `enhancement` read back correctly; Complexity POST with option name `Medium` succeeded without an API-version header. GET returned the numeric option id in `value` and the name in `single_select_option.name`.
- Bug probe https://github.com/IronbellyOrg/IronClaude/issues/461: type `Bug`, label `bug`, Complexity `Simple` read back correctly.
- Repeating the same POST succeeded and kept one field value. A nonexistent option name returned HTTP 422 and left `Simple` unchanged.
- Both probes were closed as not planned after testing.
- No-push-access silent type drop remains untested; the token used has push access. This was an API-level check, not an end-to-end skill run.
- The parent fixed the classification-table follow-up below: 4 stale entries removed, 9 current entries added. The affected suites passed (2525 tests on 2026-11-08; 2526 after the read-back clarification on 2026-11-09).
- Submission preparation clarified field read-back in `refs/labels.md`: select by `issue_field_id`, compare `single_select_option.name`, never numeric `value` against an option name; a failed or unparseable read-back is not success. A static regression test pins this rule.

## Main-session live acceptance checks (2026-11-09)

This dated result supersedes the historical warnings below only where there is new evidence. Earlier plan verdicts and archived ledger entries are unchanged.

- Both specified `/sc:issue --create` commands were invoked through the Skill tool in the main session, one at a time, with the required tier-pinned lookup and drafting workers. `make sync-dev` refreshed project command/worker copies. The installed protocol was backed up and refreshed with `uv run superclaude install-skill sc-issue-protocol --force`; an excluding-cache comparison found no source differences. The Skill tool still returned its session-start cached text, so the main session explicitly read and followed the refreshed on-disk protocol and refs. This is not evidence that hot-reload of Skill tool cached descriptions works.
- Feature probe https://github.com/IronbellyOrg/IronClaude/issues/466: actual issue type `Test`, mode label `enhancement`, Complexity option name `Medium` (field id `49604587`, numeric option id `86847598`). Create, field POST, independent metadata GET and close all succeeded. Closed as `NOT_PLANNED`.
- Bug probe https://github.com/IronbellyOrg/IronClaude/issues/467: actual issue type `Bug`, mode label `bug`, Complexity option name `Simple` (same field, numeric option id `86847597`). Create, field POST, independent metadata GET and close all succeeded. Closed as `NOT_PLANNED`.
- Both checks matched `single_select_option.name`, not numeric `value`, and produced empty missing-classification and missing-label lists. No extra API-version header was used. The owner chose to drop additional material from the feature issue draft before it was posted.
- Requested regression command (`tests/commands tests/core tests/skills tests/recommend tests/cli/test_issue_body_templates.py`): first run had 2,564 passes and one 60-second fake-Orca launch timeout; isolated test retry passed in 0.43 seconds; unchanged full requested subset retry passed all 2,565 tests in 69.52 seconds. This is a subset, not a clean full-repository suite. The timeout's cause remains undetermined.
- Current `make verify-sync`, `make lint` and separate `uv run ruff format --check src/ tests/` passed; sync reported five command-size policy warnings, no errors. No source or guard change was made for either timing failure.
- Another session's full-repository submission preflight remains halted after its allowed retry: 24,609 passes and one launch-level-guard large-command timeout. Its isolated rerun passed four cases, which does not replace the failed full-suite gate. Evidence: `.dev/pr-monitor/issue-438-preflight/submission-status.json`.
- The owner then explicitly authorized exactly one additional full-suite attempt, with stop on failure. `make test` finished at 2026-11-09T13:14 UTC: 24,609 passed, 1 failed, 149 skipped, 2 xpassed, 32 warnings in 1,028.12 seconds. Failure: `tests/unit/test_ccsession_tiers.py::test_every_shim_launch_gets_the_port_for_its_settings`, expected `http://127.0.0.1:4013`, observed `http://127.0.0.1:4417`. Make exited 2 (pytest failed). Log: `.dev/issues/438/full-suite-authorized-retry.log`. The earlier guard timing failure did not recur in this run, but the suite is still not green. Submission stopped without another retry, new commit, push or PR; no source/guard changes or causal explanation are claimed.
- No-push-access silent issue-type drop remains untested because the current token has push access. Historical failure and permission paths are not proved by these happy-path live checks.
- Machine evidence and captured validation logs: `.dev/issues/438/live-acceptance-20261109.json`, `feature-created.json`, `bug-created.json`, `requested-tests-first.log`, `isolated-test-retry.log`, `requested-tests-retry.log`, `sync-lint-format.log`. Creation artifacts are retained in `.dev/issues/466/` and `.dev/issues/467/`.

## Owner-authorized test-only correction (2026-11-09)

- The owner directly authorized this session to correct only the settings-port assertion and its launcher diagnostics, prove occupied/free ports and wrong-family rejection, obtain independent review, run affected checks and one full validation, and stop on failure. Exclusive branch ownership was confirmed with the other session; no competing source edits or test runs were started there.
- One contiguous edit in `tests/unit/test_ccsession_tiers.py` retains stderr as `out` and checks exact URLs in the settings-derived candidate family using existing `models.SHIM_PORT_STEP` and `models.SHIM_PORT_ATTEMPTS`. Automatic selection, the nondefault check and cleanup remain unchanged. No production, guard, configuration, proxy or timeout changes.
- Real occupied preferred-port check passed in 2.09 seconds (preferred4013, actual4417); real free preferred-port check passed in 1.41 seconds (preferred/actual4031). A diagnostic fault-injection probe invokes the actual modified test and proves wrong-family URL rejection plus retained stderr, passing in0.58s. Its first diagnostic-only collection attempt failed to import `tests`; its loader was corrected to import the existing file by path, with the original error log retained.
- Independent adversarial review: PASS, no blocking findings. Candidate-family and diagnostic semantics checked; passing logs alone do not show selected URLs, so retained `occupied-seen.txt`/`free-seen.txt` provide the parent-collected observations. The negative case is one deliberate out-of-family URL, not an exhaustive matrix.
- Sync, lint and separate formatting gates passed. The affected suites then failed: 2,740 passed and1failed in233.07s. Failure: unchanged `test_a_busy_shim_is_never_stopped_by_a_new_launch`, launcher reported an incompatible shim on57419, tried57520 and returned `ERROR: shim failed to start`. The underlying startup cause is not diagnosed in this bounded fix.
- Stopped as authorized: no affected-test retry, no full-suite attempt started, no new commit, push or PR. The one-file correction is retained in the working tree; earlier ledger verdicts and all historical failures remain unchanged. Evidence: `.dev/issues/438/shim-port-fix/results.json`, `independent-review.json`, `affected-tests.log` and the focused logs beside them.

## Original checks to run

- Feature check: run `/sc:issue --create "<short test description>" --mode feature --type tests --depth standard` on `IronbellyOrg/IronClaude`. Confirm the new issue shows the issue type Test and the Complexity field Medium, carries the `enhancement` label, and that the final output lists a `not set` line for anything that did not apply.
- Bug check: run `/sc:issue --create "<short test description>" --mode bug --depth quick` on the same repo. Confirm the issue type is Bug, the Complexity field is Simple, the `bug` label is present, and any `not set` line is listed in the final output.
- Close both test issues afterwards.

## UNVERIFIED points (from the design, section 3.4)

- The POST body for the Complexity field (`{"issue_field_values":[{"field_id":<id>,"value":"<option name>"}]}`) comes from GitHub's documentation, not from a run. GitHub's example sends the header `X-GitHub-Api-Version: 2026-03-10`; the skill does not send it, so a 404 would show up as `not set: field Complexity ...: write failed`.
- The `--type` flag of `gh issue create` comes from `gh` help (gh 2.103.3), not from a run.
- GitHub drops the issue type silently when the caller has no push access. The skill detects this by reading the type back, and that read-back has not been exercised against a real issue.

## Defaults the owner may reverse

- The T3 lookup worker may read exactly one `orgs/` path (`orgs/<owner of R>/issue-fields`) to find the Complexity field id. Reversing it means giving the field id another way.
- The `--type` flag and its 11 area values are kept, but they no longer produce a label; the area only decides issue type Test for a feature in `tests`.
- The `bug` and `enhancement` mode labels are kept alongside the issue type.
- Area `tests` on a feature gives issue type Test; every other feature gives Feature, and mode bug always gives Bug.

## Known follow-up found while implementing

- `tests/skills/test_worker_contract.py` fails 2 tests (`test_every_write_verb_hit_is_classified`, `test_classification_table_has_no_stale_entries`). That file keeps the exact text of every `gh api` line in the skills, commands and agents, and Tasks 2, 3 and 5 rewrote four of those lines and added new ones. The plan did not include this file, so it was not changed. The fix is to update the classification table in that file from the new line text (GET lookups read-only, the POST lines never-worker); the log is `./artifacts/t12-extra-suite.log`.
