review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- R1: report <redacted>, block ok false
- R3: report <redacted>, block ok true
- R2: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | - | R1 |
| L2 | open | yes | single | MAJOR | - | R3 |
| L3 | open | yes | single | CRITICAL | - | R2 |

## Blocking findings

### L2

#### L2.R3 (F1)

- claim: A crash after the request is fsynced but before the draft call leaves the PR ready, yet resume at ordinal 2 reports it held and prints a clear command.
- anchor: "ordinal 2 with phase `ENGAGE_PENDING` and a non-empty `pending` returns `REPORT_HELD` (row 2 wins over row 3);"

### L3

#### L3.R2 (F1)

- claim: Resume lacks the target SHA or event data needed to verify that the fix push is the PR head, so it cannot safely meet the required release behavior.
- anchor: "resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)"

## Other findings

- L1 (MAJOR, open, single): Wave 0 bullet wording forces a guess about whether the required L3 off line may name L3.

## Reviser brief

Blocking finding ids: L2, L3.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
