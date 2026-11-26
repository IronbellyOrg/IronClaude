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
| L2 | open | no | overlap | MAJOR | - | R1, R3 |
| L3 | open | yes | overlap | MAJOR | - | R1, R2, R3 |
| L4 | open | no | overlap | MINOR | - | R1, R2 |
| L5 | open | no | single | MAJOR | - | R2 |
| L6 | open | no | single | MINOR | - | R2 |

## Blocking findings

### L3

#### L3.R1 (F3)

- claim: Resume cannot re-enter release without applied_edits and target_sha; defaults must be guessed.
- anchor: "`resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)`"
- anchor2: "each re-enter `release_decision` with `push_completed=True`"

#### L3.R2 (F1)

- claim: Row 4 cannot release on a normal push_completed before a crash because the stated signature supplies no target_sha, applied_edits, or cycle_id for the release_decision re-entry.
- anchor: "resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)"

#### L3.R2 (F3)

- claim: A HELD guard that a later cycle reuses never rebinds to the new cycle id, so held_cycle_published still matches the earlier cycle and the later push does not release.
- anchor: "engage_decision(*, mode, ordinal, cycle_id, guard, read)"

#### L3.R3 (F1)

- claim: Resume can release a held PR after a published push without a target SHA input for the required PR-head comparison, so it cannot satisfy the requirement to mark the PR ready only after confirming the fix is at the PR head.
- anchor: "resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)"
- anchor2: "release_decision(*, mode, ordinal, cycle_id, guard, read, applied_edits, target_sha, push_completed)"

## Other findings

- L1 (MAJOR, open, single): Wave 0 bullet wording allows two readings; the worse reading trips the bullet gate test.
- L2 (MAJOR, open, overlap): CI engage place is ambiguous; the worse reading engages before the CI failure exists.
- L4 (MINOR, open, overlap): Plain status omits gitignored mirrors, making the mirror clause vacuous.
- L5 (MAJOR, open, single): The required gh repo view resolution fallback carries neither --repo nor a repos/ path, so a literal every-gh-line test fails on the script the other criterion requires.
- L6 (MINOR, open, single): A literal grep for 43 also matches legitimate ordinal comments, so the check over-reports instead of testing only the enum-count claim.

## Reviser brief

Blocking finding ids: L3.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
