review: 1 of 3
# Merged review 1 (coordinator script; panel of 2 reviewers)
candidate: <candidate file> sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- R1: report <redacted>, block ok true
- R2: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | MAJOR | - | R1 |
| L2 | open | yes | overlap | MAJOR | - | R1, R2 |
| L3 | open | no | single | MAJOR | - | R1 |
| L4 | open | no | single | MAJOR | - | R1 |
| L5 | open | no | single | MAJOR | - | R1 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: Resume row 4 cannot re-enter release_decision and pass its head-equals-target_sha row because neither resume_decision's stated inputs nor the folded guard record carry target_sha, applied_edits or a cycle id source, so the required landed-push release cannot be produced as written.
- anchor: "`resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)` (all 9 rows, with the row 2 precedence"
- anchor2: "crash after a dangling `push_initiated` with branch strings produced by the real `detect_crash_window` and `resolve_crash_window` (`landed` releases, `not_landed` holds, `ambiguous` holds)"

### L2

#### L2.R1 (F2)

- claim: A later cycle that reuses a held draft never moves the guard's cycle_id, so the published check judges it against the earlier cycle's push and a crash after its own push leaves the pull request held.
- anchor: "`held_cycle_published(events, guard)` (true when a `push_completed` event, normal or recovered, carries the guard's `cycle_id`)"

#### L2.R1 (F5)

- claim: The candidate never states whether the off rule or the held phase wins in guard_status when a held guard is reported with the mode off, so the same draft-held pull request can be reported off or held.
- anchor: "`guard_status(guard, mode, ordinal)` implementing the first-match mapping of section 4.1 (`off`, `released`, `held`, `user_override`, `unavailable`)"
- anchor2: "mode `OFF` at ordinal 3 with phase `HELD` returns `REPORT_HELD`"

#### L2.R2 (F1)

- claim: Resume cannot verify that the current PR head equals the published push target because its interface provides neither target_sha nor the push event, so it can mark the PR ready after the head has moved.
- anchor: "re-enter `release_decision` with `push_completed=True`"

## Other findings

- L3 (MAJOR, open, single): The Wave 0 bullet is required both to carry no L3 condition and to state an at-L3 off condition, leaving the wording its own test must accept or reject to a guess.
- L4 (MAJOR, open, single): A byte-identical assertion built from the literal start text recorded in Task 1 passes when the tail of either pinned sentence changes, so the Task 10 check cannot deliver the guarantee it claims.
- L5 (MAJOR, open, single): Tasks 8 and 12 close by classifying only gh pr and gh api lines, so a new git write-verb line in the ref or command file is left unclassified and fails the worker-contract tests those tasks run.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
