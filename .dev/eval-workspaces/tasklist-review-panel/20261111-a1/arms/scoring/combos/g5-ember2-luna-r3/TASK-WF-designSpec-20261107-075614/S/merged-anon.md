review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- R1: report <redacted>, block ok true
- R2: report <redacted>, block ok true
- R3: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | - | R1 |
| L2 | open | yes | overlap | MAJOR | - | R1, R3 |
| L3 | open | no | single | MAJOR | - | R2 |
| L4 | open | no | single | MAJOR | - | R2 |
| L5 | open | no | single | MINOR | - | R2 |
| L6 | open | no | single | MINOR | - | R2 |

## Blocking findings

### L2

#### L2.R1 (F2)

- claim: The same task also requires an L3 off line in that bullet, so the no L3 condition wording is imprecise.
- anchor: "one new bullet under Wave 0, written as a flat line before the Wave 1 bullet, that applies at every ordinal and in both modes and carries no L3 or `draft` condition"

#### L2.R3 (F1)

- claim: The Wave 0 bullet must state the L3/off behavior, while its acceptance criterion requires failure whenever the bullet names an L3 condition, so the required implementation cannot pass that test.
- anchor: "one new bullet under Wave 0, written as a flat line before the Wave 1 bullet, that applies at every ordinal and in both modes"
- anchor2: "The Wave 0 test fails when the bullet is placed after the Wave 1 bullet, when it names an L3 or `draft` condition"

## Other findings

- L1 (MAJOR, open, single): The artifacts path is ambiguous against the git status list, so an implementer must guess the exact package folder.
- L3 (MAJOR, open, single): Task 8 and 12 last steps cover only gh pr/gh api lines, leaving git write verbs in the ref or command file unclassified as required by the governing constraint.
- L4 (MAJOR, open, single): The second object whose length must be 45 is not named, so the check can pass on a wrong pair of measurements.
- L5 (MINOR, open, single): Phase string values are not pinned, so held equality depends on the implementer choosing a str enum.
- L6 (MINOR, open, single): The artifacts path relative to .dev is ambiguous, so the status allowlist may not cover the two artifact files.

## Reviser brief

Blocking finding ids: L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
