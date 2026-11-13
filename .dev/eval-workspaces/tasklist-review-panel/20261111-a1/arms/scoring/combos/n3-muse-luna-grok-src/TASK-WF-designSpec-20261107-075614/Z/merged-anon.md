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
| L1 | open | no | overlap | MAJOR | - | R1, R3 |
| L2 | open | no | single | MAJOR | - | R1 |
| L3 | open | no | overlap | MAJOR | - | R1, R3 |
| L4 | open | no | single | MINOR | - | R1 |
| L5 | open | no | single | MAJOR | - | R3 |
| L6 | open | no | single | MAJOR | - | R3 |
| L7 | open | no | single | MINOR | - | R3 |

## Blocking findings

none.

## Other findings

- L1 (MAJOR, open, overlap): resume_decision is given no cycle_id, applied_edits or target_sha, yet row 4 must re-enter release_decision which requires all three, so whether a landed or normally completed push releases the PR depends on values the plan never supplies.
- L2 (MAJOR, open, single): The last-step classification instruction in Tasks 8 and 12 omits git write verbs that the plan constraint and WRITE_VERB_RE cover, so a git push line in refs/merge-guard.md or pr-submit.md would be unclassified and fail test_every_write_verb_hit_is_classified.
- L3 (MAJOR, open, overlap): Read as a substring check, the required Wave 0 test rejects the very bullet Task 9 mandates, because that bullet must contain an L3-scoped off clause; the candidate never states that only the resume clause must be ungated.
- L4 (MINOR, open, single): The script contract never states ok or the exit code for a timeline-only failure, so one build reports timeline_unreadable and another read_failed for the same GitHub failure.
- L5 (MAJOR, open, single): A repo-root ./artifacts/ file fails Task 13's git-status allowlist, while the package reading would pass.
- L6 (MAJOR, open, single): A failed draft settle later returns hold, and the plan never says that hold stops edits, so a later run can edit a PR that is still ready.
- L7 (MINOR, open, single): detect_crash_window returns the unfinished push event, not the branch word; only resolve_crash_window returns landed, not_landed, or ambiguous.

## Reviser brief

Blocking finding ids: none.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: PASS
