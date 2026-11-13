review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- R2: report <redacted>, block ok false
- R1: report <redacted>, block ok true
- R3: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | MAJOR | - | R3 |

## Blocking findings

### L1

#### L1.R3 (F1)

- claim: An implementer who follows the stated text as written builds a Wave 0 bullet that says `at L3` for the `off` notice, and that is wrong because acceptance criterion 140 requires the bullet to fail if it names an L3 condition.
- anchor: "at L3 with `--merge-guard off` the line"
- anchor2: "when it names an L3 or `draft` condition"

## Other findings

none.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
