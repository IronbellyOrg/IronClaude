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
