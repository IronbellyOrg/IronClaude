review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 1f84077e475af7358384ebaf383d03500bc6d6e46b9a85e8a977a67a18341e0a
reviewers:
- R2: report <path>, block ok true
- R3: report <path>, block ok true
- R1: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | CRITICAL | - | R2 |
| L2 | open | yes | single | CRITICAL | - | R2 |
| L3 | open | no | single | MAJOR | - | R2 |
| L4 | open | no | single | MAJOR | - | R2 |
| L5 | open | no | single | MAJOR | - | R2 |
| L6 | open | no | single | MINOR | NP-1, NP-2, NP-5 | R2 |
| L7 | open | yes | single | MAJOR | - | R3 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: Absent Codex fields disable Codex in the candidate; design A0 requires fallback to shipped values, explicit empty/null disables
- anchor: "A local override YAML without Codex fields still loads (Codex identities empty, so Codex is disabled for that override)"

### L2

#### L2.t2b-1 (F2)

- claim: Two summary comments classify polling in the candidate; design A3 requires latest updated_at marker wins except ties
- anchor: "exactly one Codex-authored issue comment with one bounded"
- anchor2: "Running status, wrong head, two summary comments, malformed or duplicate-key JSON"

#### L2.t2b-1 (F3)

- claim: Completion is updated_at only; design A1 requires later of updated_at and newest expected-head review submitted_at
- anchor: "completion time = `updated_at`"

#### L2.t2b-1 (N2)

- claim: Artifact paths use ./artifacts while staging constraint covers .dev/tasks artifacts; confirm intended home
- anchor: "saving the output to ./artifacts/t7-dry-check-pr336.txt"

### L7

#### L7.t3-1 (F1)

- claim: The candidate forbids plugin mirror edits although the driving document requires implementing the change in plugins/superclaude.
- anchor: "plugins/superclaude/ has no pr-submit twin (design section 3), so no mirror edit is needed; do not create one."

## Other findings

- L3 (MAJOR, open, single): A6 later-of root createdAt selection rule and test_a6 fixtures/tests are never stated; PR 337 shape polls to timeout
- L4 (MAJOR, open, single): Already-absent/empty-identity immediate-absent input and merge_wait tuple shape omitted; disabled reviewer can stay pending
- L5 (MAJOR, open, single): rereview_requested timestamp field, resume watermark reconstruction and cycle_id reuse are never specified
- L6 (MINOR, open, single): Design file absent in NP-1 checkout; review used identical sibling copies at NP-2 to NP-5

## Reviser brief

Blocking finding ids: L1, L2, L7.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
