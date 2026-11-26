review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 9f610e5d808c275bde4f84a63cf17ff433dad6004e81609f02e3953c7c7c9df8
reviewers:
- R2: report <path>, block ok true
- R3: report <path>, block ok true
- R1: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | MAJOR | AC-6 | R2 |
| L2 | open | no | overlap | MAJOR | - | R3, R1 |
| L3 | open | no | overlap | MAJOR | - | R3, R1 |
| L4 | open | yes | single | MAJOR | - | R1 |

## Blocking findings

### L1

#### L1.t1b-1 (F1)

- claim: Candidate accepts a failing named test file as complete when the failure is not attributable to design.md, contradicting the driving document requirement that the related tests pass.
- anchor: "or any failure is shown in `./artifacts/t2-checks.log` and is not attributable to `design.md`"

### L4

#### L4.t4-1 (F1)

- claim: The mandatory sync-dev recipe overwrites files under .claude/, directly contradicting the candidate's blanket prohibition on edits there.
- anchor: "or anything under `.claude/`."
- anchor2: "Then run `make sync-dev` and `make verify-sync` from the repository root"

## Other findings

- L2 (MAJOR, open, overlap): Task 2 acceptance lets a test failure pass if logged and judged unrelated, while source requires the tests to pass.
- L3 (MAJOR, open, overlap): Fallback note omits return-contract.yaml; source section 3.2 item 6 names it.

## Reviser brief

Blocking finding ids: L1, L4.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
