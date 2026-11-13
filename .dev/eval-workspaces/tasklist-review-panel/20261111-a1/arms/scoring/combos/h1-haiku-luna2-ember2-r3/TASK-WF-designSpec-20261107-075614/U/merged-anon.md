review: 1 of 3
# Merged review 1 (coordinator script; panel of 5 reviewers)
candidate: <candidate file> sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- R1: report <redacted>, block ok true
- R4: report <redacted>, block ok false
- R5: report <redacted>, block ok true
- R2: report <redacted>, block ok false
- R3: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | overlap | MAJOR | - | R1, R3 |
| L2 | open | no | overlap | MAJOR | - | R1, R2, R3 |
| L3 | open | no | overlap | MAJOR | - | R1, R2 |
| L4 | open | no | single | MAJOR | - | R1 |
| L5 | open | no | single | MAJOR | - | R1 |
| L6 | open | no | single | MINOR | - | R1 |
| L7 | open | no | single | MINOR | - | R1 |
| L8 | open | yes | single | MAJOR | - | R5 |
| L9 | open | no | overlap | MAJOR | - | R2, R3 |

## Blocking findings

### L8

#### L8.R5 (F1)

- claim: After a normal push completes and the process crashes before release, resume cannot supply the push target SHA to the release decision, so it cannot verify that the PR head matches the pushed commit or release the PR.
- anchor: "resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)"

## Other findings

- L1 (MAJOR, open, overlap): Tasks 2 and 3 assume a pre-feature base, but this checkout already has the enum members, merge_guard.py and the 45-member test, so a literal run duplicates or overwrites them.
- L2 (MAJOR, open, overlap): The Wave 0 bullet must print an L3-gated line yet is required to carry no L3 condition, so the stated test wording cannot be met as written.
- L3 (MAJOR, open, overlap): The engage trigger for CI-fix cycles is contradictory, because a failing CI check has no defined verified-finding severity.
- L4 (MAJOR, open, single): The phase enum string values are never stated, so the asserted lowercase phase strings have no defined mapping to the named phases.
- L5 (MAJOR, open, single): No exit code is stated for a timeline-only failure or for the not_open case, so the script's exit behaviour in those cases is left to the implementer.
- L6 (MINOR, open, single): git status never prints gitignored paths, so the listed check cannot detect the .claude mirror case.
- L7 (MINOR, open, single): The project CLAUDE.md mandates the PR command without this flag, so the operator is not told how to add it in the PR step.
- L9 (MAJOR, open, overlap): Resume row 4 is said to re-enter release_decision, but resume_decision has no applied_edits or target_sha parameter to pass.

## Reviser brief

Blocking finding ids: L8.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
