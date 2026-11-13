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
| L1 | open | yes | single | CRITICAL | - | R2 |
| L2 | open | no | overlap | MAJOR | - | R2, R3 |
| L3 | open | no | overlap | MAJOR | - | R2, R3 |
| L4 | open | no | single | MINOR | - | R2 |
| L5 | open | no | single | MINOR | - | R3 |
| L6 | open | no | single | MINOR | - | R3 |
| L7 | open | no | single | MINOR | - | R3 |
| L8 | open | no | single | MINOR | - | R3 |

## Blocking findings

### L1

#### L1.R2 (F1)

- claim: Resume row 4 must re-enter release_decision, but resume_decision is given neither applied_edits nor target_sha, so the required head or zero-edit release proof cannot be checked and a resumed run either never releases or readies an unproven head.
- anchor: "`resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)` (all 9 rows"
- anchor2: "`release_decision(*, mode, ordinal, cycle_id, guard, read, applied_edits, target_sha, push_completed)` (all 9 rows"

## Other findings

- L2 (MAJOR, open, overlap): A new cycle can start while an earlier cycle still holds the guard, but no stated step moves the folded cycle_id to the new cycle, so publication is judged against the earlier cycle's push.
- L3 (MAJOR, open, overlap): The Wave 0 bullet must name L3 for the off line, yet the acceptance version of its test fails a bullet that names an L3 condition, so the two stated test wordings cannot both be implemented literally.
- L4 (MINOR, open, single): The per-task classification steps omit the git write verbs that the plan's own constraint requires entries for, so a task-faithful implementer can leave a hit unclassified and fail the classification tests run in the same task.
- L5 (MINOR, open, single): The Goal says engage happens as soon as a finding is routed, while the owner decision fixes it at the end of Wave 3, so the Goal wording reads as earlier than verification.
- L6 (MINOR, open, single): The git status criterion lists gitignored .claude mirrors as allowed changes, though they never appear in git status and the rules forbid staging them.
- L7 (MINOR, open, single): A plain grep for 43 in models.py matches the comment about the 42nd-43rd members, so the check needs a human judgment the criterion does not state.
- L8 (MINOR, open, single): The release rule keys on an error text that is not verified to come from gh, so an unexpected message holds a PR that could be released; the failure direction is safe.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
