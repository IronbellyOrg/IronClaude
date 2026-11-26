review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- R3: report <redacted>, block ok true
- R2: report <redacted>, block ok true
- R1: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | MAJOR | - | R3 |
| L2 | open | yes | single | MAJOR | - | R3 |
| L3 | open | no | overlap | MAJOR | - | R2, R3 |
| L4 | open | no | overlap | MAJOR | - | R2, R3 |
| L5 | open | no | single | MAJOR | - | R3 |
| L6 | open | no | single | MAJOR | - | R3 |
| L7 | open | no | single | MINOR | - | R3 |
| L8 | open | no | single | MINOR | - | R3 |
| L9 | open | no | single | MINOR | - | R2 |
| L10 | open | no | single | MINOR | - | R2 |

## Blocking findings

### L1

#### L1.R3 (F1)

- claim: The Goal says engage as soon as a finding is routed, but the owner decisions and Tasks 8 and 10 fix engage at the end of Wave 3, so no build satisfies both.
- anchor: "a PR is turned into a draft as soon as a verified Medium-or-higher finding is routed to a fix"
- anchor2: "Engage at the end of Wave 3 (L3, only when at least one verified finding of Medium severity or higher is routed to a fix, once per cycle id"

### L2

#### L2.R3 (F2)

- claim: Resume row 7 sends a ready call in phase RELEASE_PENDING whatever the dangling branch is, so a not_landed push can be made ready, which the plan says must keep the PR draft.
- anchor: "\"not_landed\"` returns `NOOP(held_through_redrive)`"
- anchor2: "(`landed` releases, `not_landed` holds, `ambiguous` holds)"

#### L2.R3 (F5)

- claim: The test does not state the starting phase, and from RELEASED the stated row 2 returns NOOP; the fold also never says a new request replaces cycle_id.
- anchor: "`release_decision` called with `applied_edits=0` for a new cycle while the guard record already holds an earlier fixing cycle returns `RELEASE` with cause `no_edits`"

## Other findings

- L3 (MAJOR, open, overlap): The Wave 0 test wording is undefined, so a bare substring check on draft rejects the required off-mode text.
- L4 (MAJOR, open, overlap): The Phase enum string values are never stated, so the test depends on a guessed spelling.
- L5 (MAJOR, open, single): The plan assumes a pre-feature base, but the checkout already contains the feature files, so the base record and the create steps do not match this tree.
- L6 (MAJOR, open, single): Under set -euo pipefail a failing timeline pipeline ends the script before it prints the JSON line, unless the plan says how to capture it.
- L7 (MINOR, open, single): The BRANCH_* strings already exist in conflicts.py and are exported, and the plan adds a second copy without saying so.
- L8 (MINOR, open, single): A run that never engaged reports the same word as a run that released a held PR, which may mislead the reader.
- L9 (MINOR, open, single): The one-extra-transition shorthand is ambiguous unless read with the exact rule that adds unsettled slack, so a test writer must confirm the guard has zero slack before asserting foreign.
- L10 (MINOR, open, single): A literal-start prefix comparison cannot prove byte-identical full sentences, so the plan overstates the strength of the pinned-sentence check.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
