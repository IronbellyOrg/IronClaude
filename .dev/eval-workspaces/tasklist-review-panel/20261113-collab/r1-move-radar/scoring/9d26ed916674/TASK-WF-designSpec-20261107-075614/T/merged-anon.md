review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- R1: report <redacted>, block ok true
- R3: report <redacted>, block ok true
- R2: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | R1, R3 |
| L2 | open | no | single | MAJOR | - | R1 |
| L3 | open | no | single | MAJOR | - | R1 |
| L4 | open | no | single | MAJOR | - | R1 |
| L5 | open | no | single | MAJOR | - | R1 |
| L6 | open | no | single | MINOR | - | R1 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: First-match order puts the unreadable-timeline halt before the already-draft skip, so an already-draft PR with an unreadable timeline halts the run, which contradicts the source rule that such a PR is settled skipped/already_draft and the run goes on.
- anchor: "`engage_decision(*, mode, ordinal, cycle_id, guard, read)` (all 11 rows, first match wins, `notes` carries `auto_merge_armed`)"
- anchor2: "`test_attach_and_create_preserve_preexisting_draft`"

#### L1.R1 (F4)

- claim: An exact-order assertion fails on a real run because the Wave 6 triad appends push_decision and push_initiated between fix_applied and push_completed.
- anchor: "The acceptance-trace test asserts the exact event order"
- anchor2: "`draft_guard_settled(confirmed)`, `fix_applied`, `push_completed`, `draft_guard_requested(ready)`"

#### L1.R1 (F8)

- claim: RECONCILE is the only stated result, so no text says resume_decision is re-entered to release after a not_applied ready settle.
- anchor: "a ready request settled `not_applied` that stays `HELD` and is released after the publication check"
- anchor2: "`resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)` (all 9 rows"

#### L1.R1 (F12)

- claim: The one-retry cap is stated in prose only, since release row 2 leaves RELEASE_PENDING open with no limit.
- anchor: "test_guard_release_failure_retries_once_and_reports"

#### L1.R3 (F1)

- claim: The release-retry scenario is not explicitly required to assert that an already-ready PR is treated as confirmed, leaving that specified behavior without a mandated scenario-test check.
- anchor: "Create `tests/pr_submit/test_merge_guard_scenarios.py` with a small test driver"

## Other findings

- L2 (MAJOR, open, single): No effect row sets the folded cycle_id, so a later cycle's completed push is not recognised as published on resume.
- L3 (MAJOR, open, single): A record in RELEASED after an earlier fixing cycle returns NOOP(not_held), so the RELEASE criterion only passes if the test first sets HELD, which the text does not say.
- L4 (MAJOR, open, single): The required Wave 0 bullet names L3 and draft in its off clause, which the stated acceptance test rejects.
- L5 (MAJOR, open, single): CI-log findings carry no severity, so the Medium-or-higher engage trigger has no input for CI-fix cycles.
- L6 (MINOR, open, single): The exit code for a failing timeline call is not stated, so the test may assert either 0 or 1.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
