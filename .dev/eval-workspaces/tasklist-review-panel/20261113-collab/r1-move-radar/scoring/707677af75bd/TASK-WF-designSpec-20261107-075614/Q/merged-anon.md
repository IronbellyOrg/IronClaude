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
| L1 | open | yes | overlap | MAJOR | - | R1, R3 |
| L2 | open | no | single | MINOR | - | R1 |
| L3 | open | no | single | MINOR | - | R1 |
| L4 | open | no | single | MAJOR | - | R2 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: The Wave 0 bullet must carry no L3 or draft condition yet must name L3 and a draft call in its off sentence, so a substring test for those words cannot pass on the required text.
- anchor: "carries no L3 or `draft` condition"
- anchor2: "at L3 with `--merge-guard off` the line"

#### L1.R1 (F2)

- claim: Task 10 fixes the mint at the Wave 3 bullet while Task 8 defers the single mint place to the O1 finding, so an O1 result elsewhere leaves two mint sources.
- anchor: "once per cycle id, and mints the cycle id"
- anchor2: "in the single place named by Task 1 O1"

#### L1.R1 (F3)

- claim: Tasks 9, 10 and 12 consume the pre-build record but declare no direct dependency on Task 1, only a transitive one.
- anchor: "Depends on: Task 9"
- anchor2: "using the pins and line-content rules recorded in `./artifacts/pre-build-gate.md`"

#### L1.R1 (F4)

- claim: Classification instructions name only gh pr and gh api, while the table also requires entries for git write verbs on new lines.
- anchor: "for every line of the ref that matches `gh pr` or `gh api`"

#### L1.R3 (F1)

- claim: The Wave 0 bullet must both include the L3 `--merge-guard off` behavior and avoid any L3 condition, while its acceptance test rejects L3 wording, so the specified test cannot pass.
- anchor: "that applies at every ordinal and in both modes and carries no L3 or `draft` condition;"
- anchor2: "when it names an L3 or `draft` condition"

## Other findings

- L2 (MINOR, open, single): No function or step is named that builds the idempotency key or computes k, though pending_requests depends on it.
- L3 (MINOR, open, single): The value of ok when only the timeline call fails, and the exit code for not_open, are unspecified, which decides whether engage row 8 is reachable.
- L4 (MAJOR, open, single): The release table does not require push_completed to belong to cycle_id, so an implementation may accept a different cycle's completion as proof of publication.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
