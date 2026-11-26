review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- R2: report <redacted> block ok true
- R3: report <redacted> block ok true
- R1: report <redacted> block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | CRITICAL | - | R2 |
| L2 | open | yes | overlap | MAJOR | - | R1, R2 |
| L3 | open | no | single | MAJOR | - | R2 |
| L4 | open | no | single | MINOR | - | R2 |
| L5 | open | no | single | MINOR | - | R2 |

## Blocking findings

### L1

#### L1.R2 (F1)

- claim: A zero-edit cycle releases the PR while an earlier held fix never reached the head, so the PR goes ready with that fix unpublished.
- anchor: "`release_decision` called with `applied_edits=0` for a new cycle while the guard record already holds an earlier fixing cycle returns `RELEASE` with cause `no_edits`"
- anchor2: "unreadable timeline or unpublished exit keeps the PR draft"

#### L1.R2 (F2)

- claim: The required Wave 0 bullet names an L3 condition, so the test that fails on an L3 or draft condition cannot pass on the real file.
- anchor: "carries no L3 or `draft` condition"
- anchor2: "and that at L3 with `--merge-guard off` the line"

#### L1.R2 (F5)

- claim: An unsettled draft request at ordinal 2 stays unreconciled and reports unavailable with no clear command.
- anchor: "ordinal 2 with phase `ENGAGE_PENDING` and a non-empty `pending` returns `REPORT_HELD` (row 2 wins over row 3)"

#### L1.R2 (F6)

- claim: Row 4 precedence lets a published push override an ambiguous remote tip, and no test covers that case.
- anchor: "`resume_decision` row 4 is tested for both entries"
- anchor2: "returns `HOLD(ambiguous_remote_tip)`"

#### L1.R2 (F7)

- claim: The Wave 0 resume hook changes ordinal 0 to 2 runs beyond the one report line the scope limit allows.
- anchor: "applies at every ordinal and in both modes"
- anchor2: "ordinals 0 to 2 change only by one report line"

### L2

#### L2.R2 (F3)

- claim: Zero-edit cycles have no protocol step that runs Release, so the PR may stay draft after a cycle with no edits.
- anchor: "Release runs after `push_completed` and before reply, resolve and the S5a re-trigger"

#### L2.R1 (F1)

- claim: A CI-fix cycle is specified to engage at both Wave 3 and Wave 8, although the existing flow reaches the CI-fix trigger only at Wave 8.
- anchor: "Engage at the end of Wave 3 (L3, only when at least one verified finding of Medium severity or higher is routed to a fix, once per cycle id; review-fix cycles and CI-fix cycles;"
- anchor2: "the Wave 8 bullet states that a CI-fix cycle engages with kind `ci` and releases after `push_completed` before the CI re-poll."

## Other findings

- L3 (MAJOR, open, single): A failed timeline call may also set ok to false, so the decision reports read_failed instead of timeline_unreadable.
- L4 (MINOR, open, single): A run that never engaged reports merge_guard released, which implies a draft was released.
- L5 (MINOR, open, single): The git status check names gitignored paths that never appear in git status, so the check text is misleading.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
