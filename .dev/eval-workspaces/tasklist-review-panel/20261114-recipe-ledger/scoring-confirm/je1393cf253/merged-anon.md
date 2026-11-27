review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 9f610e5d808c275bde4f84a63cf17ff433dad6004e81609f02e3953c7c7c9df8
reviewers:
- R3: report <path>, block ok true
- R1: report <path>, block ok true
- R2: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | R3, R1, R2 |
| L2 | open | no | overlap | MAJOR | - | R3, R1, R2 |
| L3 | open | no | overlap | MAJOR | - | R3, R2 |
| L4 | open | no | single | MAJOR | WC-4 | R1 |

## Blocking findings

### L1

#### L1.t1b-1 (F1)

- claim: Candidate lets Task 2 pass while a named test file fails if judged not attributable to design.md; source section 6 requires the related tests to pass with no such exception.
- anchor: "The four named test files pass with `uv run pytest`, or any failure is shown in `./artifacts/t2-checks.log` and is not attributable to `design.md`."

#### L1.t3-1 (F4)

- claim: Allows named-test failures to pass if judged not attributable, which weakens the source requirement that the four files pass and hides attribution guesswork.
- anchor: "The four named test files pass with `uv run pytest`, or any failure is shown in"

#### L1.t4-1 (F3)

- claim: The candidate permits acceptance with logged unrelated test failures, whereas the driving document requires all four named test files to pass.
- anchor: "or any failure is shown in `./artifacts/t2-checks.log` and is not attributable to `design.md`"

## Other findings

- L2 (MAJOR, open, overlap): Tool map drops source call shapes: search {query, kind?}, node file/symbol keys, callers {symbol, limit:20}, and impact before proposing any change to an existing interface.
- L3 (MAJOR, open, overlap): Task 2 creates a repo-root artifacts log while the plan's constraint is to edit only design.md, leaving an untracked file outside the declared scope.
- L4 (MAJOR, open, single): Names neither return-contract.yaml nor the WC-4 field list, so the unstable writing place is ambiguous between the shared worker contract and the per-run contract.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
