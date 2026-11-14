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
| L1 | open | no | single | MAJOR | 4.5 | R1 |
| L2 | open | no | single | MAJOR | - | R1 |
| L3 | open | no | single | MINOR | 8 | R1 |
| L4 | open | yes | single | MAJOR | - | R3 |

## Blocking findings

### L4

#### L4.R3 (F1)

- claim: Resume cannot call the required release decision for a published cycle because its specified inputs omit target_sha and applied_edits.
- anchor: "resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)"
- anchor2: "each re-enter release_decision with push_completed=True"

## Other findings

- L1 (MAJOR, open, single): Wave 0 bullet wording allows a test that rejects the required L3 off-print clause.
- L2 (MAJOR, open, single): Resume test shorthand omits the phase HELD condition of row 5.
- L3 (MINOR, open, single): Command section names only G4 and G5 of the five OPEN release gates.

## Reviser brief

Blocking finding ids: L4.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
