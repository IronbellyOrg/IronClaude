review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- R3: report <path>, block ok true
- R2: report <path>, block ok true
- R1: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | CRITICAL | - | R3 |
| L2 | open | no | single | MAJOR | - | R3 |
| L3 | open | no | single | MAJOR | - | R3 |
| L4 | open | no | single | MAJOR | - | R1 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: An implementer who follows the stated text as written builds a script whose gh repo view resolution line fails this static scan, and the scan is wrong because the resolution line is required and carries neither token.
- anchor: "asserts every `gh` line carries `--repo` or a `repos/` path"

## Other findings

- L2 (MAJOR, open, single): Wave 0 bullet must state the L3 off case yet its acceptance test fails a bullet naming an L3 condition, so the two stated texts pull opposite ways.
- L3 (MAJOR, open, single): Candidate never states the Phase enum string values, yet Task 5 pins lowercase held and engage_pending, so no stated text tells the implementer what values to use.
- L4 (MAJOR, open, single): An implementer following the source-only edit constraint omits the required tests and user-guide changes, so the plan's required deliverables and acceptance criteria cannot all be met.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
