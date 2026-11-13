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
| L2 | open | no | single | MINOR | - | R1 |
| L3 | open | no | single | MINOR | - | R1 |
| L4 | open | no | single | MAJOR | - | R2 |
| L5 | open | no | single | MAJOR | - | R2 |
| L6 | open | no | single | MAJOR | - | R2 |
| L7 | open | yes | single | CRITICAL | - | R3 |

## Blocking findings

### L7

#### L7.R3 (F1)

- claim: Resume can release a held PR after its published push even when the live PR head no longer matches that cycle's fix, because the specified resume inputs provide no expected target SHA.
- anchor: "resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)"

## Other findings

- L1 (MAJOR, open, single): Task 12 extends the same protocol test file as Tasks 9 and 10 but lists only Tasks 6 and 8 as dependencies, so Depends-on ordering alone does not order the test-file writes.
- L2 (MINOR, open, single): The bare grep for 43 still hits ordinal comments such as 42nd-43rd, so the criterion needs a judgement call rather than a literal zero-hit result.
- L3 (MINOR, open, single): The fence rule reads as forbidding a JSON output example in its own fence, which is stricter than the stated protocol steps need.
- L4 (MAJOR, open, single): An implementer who reads the constraint literally refuses the Task 13 docs edit and the usage-line acceptance fails; the plan needs one sentence saying docs are the exception.
- L5 (MAJOR, open, single): The fold effect table and the 11/9/9-row decision tables exist only in ./source.md, which is not in the package, so a reader of the candidate alone cannot build or verify the core.
- L6 (MAJOR, open, single): Tasks 1 and 13 write ./artifacts/pre-build-gate.md and ./artifacts/final-checks.md, which git status then reports outside the listed directories, so the acceptance as written fails on a strict reading.

## Reviser brief

Blocking finding ids: L7.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
