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
| L1 | open | no | overlap | MAJOR | - | R2, R3 |
| L2 | open | no | single | MAJOR | - | R2 |
| L3 | open | no | single | MAJOR | - | R2 |
| L4 | open | no | single | MINOR | - | R2 |
| L5 | open | no | overlap | MAJOR | - | R2, R3 |
| L6 | open | no | overlap | MAJOR | - | R2, R3 |
| L7 | open | no | single | MINOR | - | R2 |
| L8 | open | no | single | MAJOR | - | R3 |

## Blocking findings

none.

## Other findings

- L1 (MAJOR, open, overlap): A total reading of the src-only constraint forbids the test, fixture and documentation edits Tasks 10 and 15 require, so their acceptance criteria cannot pass under that reading.
- L2 (MAJOR, open, single): No task rewires crash recovery, so a crash between the two per-reviewer re-trigger posts resumes awaiting re-review and Codex is never re-triggered for that cycle.
- L3 (MAJOR, open, single): Neither ci-poll.md nor Wave 8 is in any task, so a Codex-only clean result has no stated path that arms the CI wait or sends transition(clean).
- L4 (MINOR, open, single): The fold never states deduplication, so repeated reviewer_absent events for one reviewer can rebuild to a list with duplicate entries.
- L5 (MAJOR, open, overlap): Two distinct findings on one path with line and original_line both None share the (path, None) key and are grouped as if they were the same location.
- L6 (MAJOR, open, overlap): _thread_findings expects a completion mapping read via _submission_ts, so the candidate never states the mapping an implementer must build from the Codex marker time.
- L7 (MINOR, open, single): That design path is absent from the reviewed checkout, so the section references the tasks rest on cannot be read or verified from this snapshot.
- L8 (MAJOR, open, single): augment_wait_outcome as specified cannot return declined, yet merge_wait must produce declined for the Augment declined row, so that row is unbuildable as written.

## Reviser brief

Blocking finding ids: none.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: PASS
