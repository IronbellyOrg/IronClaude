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
| L1 | open | yes | single | MAJOR | - | R1 |
| L2 | open | no | single | MAJOR | - | R1 |
| L3 | open | no | overlap | MAJOR | - | R1, R3 |
| L4 | open | no | single | MAJOR | - | R1 |
| L5 | open | no | single | MINOR | - | R1 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: The seven-event exact-order assertion over RunLog.read_events() fails on a real run because the push triad writes push_initiated between fix_applied and push_completed.
- anchor: "asserts the exact event order `draft_guard_requested(draft)`, `draft_guard_settled(confirmed)`, `fix_applied`, `push_completed`"

## Other findings

- L2 (MAJOR, open, single): A ban on L3 wording in the Wave 0 bullet conflicts with the mandated off-at-L3 print clause, so the implementer must guess what the ban covers.
- L3 (MAJOR, open, overlap): The exit code for a failed timeline read is ambiguous (1 by the gh-failure rule, or 0 with ok true), and not_open and verify_failed have no exit code.
- L4 (MAJOR, open, single): Start-only constants cannot prove that the whole pinned sentence is byte-identical, so a change to its tail passes the test.
- L5 (MINOR, open, single): Gitignored .claude mirrors never appear in git status, so listing them in the expected output is a harmless no-op.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
