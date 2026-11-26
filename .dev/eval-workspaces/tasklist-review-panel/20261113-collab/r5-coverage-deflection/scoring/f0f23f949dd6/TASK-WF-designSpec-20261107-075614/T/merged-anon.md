review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- R2: report <redacted> block ok true
- R3: report <redacted> block ok true
- R1: report <redacted> block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | MAJOR | - | R2 |
| L2 | open | no | single | MAJOR | - | R2 |
| L3 | open | no | single | MAJOR | - | R2 |
| L4 | open | no | single | MAJOR | - | R2 |
| L5 | open | no | single | MAJOR | - | R2 |
| L6 | open | no | single | MINOR | - | R2 |
| L7 | open | no | single | MAJOR | - | R1 |

## Blocking findings

### L1

#### L1.R2 (F1)

- claim: The plan says ordinals 0 to 2 and off make no call, but Resume at every ordinal runs a read before resume_decision, which needs a live read.
- anchor: "ordinals 0 to 2 and `off` make no call, an originally draft PR is never made ready"
- anchor2: "Resume, loaded from Wave 0 at every ordinal and in both modes"

#### L1.R2 (F6)

- claim: Nothing tests that the guard, push and rereview events share one cycle id.
- anchor: "The acceptance-trace test asserts the exact event order `draft_guard_requested(draft)`"

#### L1.R2 (F7)

- claim: A confirmed push under resume with off leaves the PR draft and the plan does not say so.
- anchor: "held-guard reporting when the mode is `off` or the ordinal is below 3"

## Other findings

- L2 (MAJOR, open, single): The Wave 0 bullet must carry no L3 condition yet must print the off line at L3, and its test rejects L3 wording.
- L3 (MAJOR, open, single): A failed engage that landed leaves an unrecorded draft, which guard_status reports as unavailable instead of held.
- L4 (MAJOR, open, single): The head-mismatch criterion does not say applied_edits, and a zero-edit input releases before the head check.
- L5 (MAJOR, open, single): No exit code is stated for not_open or verify_failed, so an implementer may pick 0 or 1.
- L6 (MINOR, open, single): Gitignored mirrors cannot appear in git status, so the acceptance wording is confusing.
- L7 (MAJOR, open, single): The task does not require `guard` to be checked for `None` before phase-dependent rows, so a fresh active engage can raise an attribute error instead of reaching the no-record engage row.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
