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
| L1 | open | yes | single | MAJOR | - | R2 |
| L2 | open | yes | overlap | MAJOR | - | R2, R3 |
| L3 | open | no | overlap | MAJOR | - | R1, R2 |
| L4 | open | no | single | MINOR | - | R2 |
| L5 | open | no | single | MINOR | - | R2 |
| L6 | open | no | single | MINOR | - | R2 |
| L7 | open | no | single | MINOR | - | R2 |

## Blocking findings

### L1

#### L1.R2 (F1)

- claim: An unsettled or failed draft request reports unavailable with no clear command, while the Task 8 acceptance requires an uncertain exit to report held.
- anchor: "that an exit with unpublished or uncertain work leaves the PR draft and reports `held`"
- anchor2: "including `ENGAGE_PENDING` and `RELEASE_PENDING` with `owned_draft` true (`held`) and false (`unavailable`)"

### L2

#### L2.R2 (F2)

- claim: resume_decision has no applied_edits or target_sha input, so re-entering release_decision needs two values the task never supplies.
- anchor: "each re-enter `release_decision` with `push_completed=True`"
- anchor2: "`resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)`"

#### L2.R2 (F3)

- claim: After a release, a repeat engage for the same cycle id returns ENGAGE because only the HELD phase blocks it.
- anchor: "once per cycle id; review-fix cycles and CI-fix cycles"
- anchor2: "`engage_decision(*, mode, ordinal, cycle_id, guard, read)` (all 11 rows, first match wins"

#### L2.R2 (F6)

- claim: No task says the default waits for the owner gate or that the build stays unmerged until then.
- anchor: "`DEFAULT_MERGE_GUARD = \"draft\"`"
- anchor2: "before the feature is merged or turned on by default"

#### L2.R2 (F7)

- claim: A test that compares only the start text passes when the rest of the pinned sentence changes.
- anchor: "are asserted byte-identical by comparing the live text with string constants"
- anchor2: "the literal start text recorded in `./artifacts/pre-build-gate.md`"

#### L2.R2 (F8)

- claim: Two texts exist for the user-facing clear command, and Task 12 does not say which one is exact.
- anchor: "prints the clear command `gh pr ready <N> --repo \"$REPO\"` once"
- anchor2: "the clear command `gh pr ready <N> --repo <REPO>`"

#### L2.R2 (F9)

- claim: CI failures are not verified findings, so the Medium-or-higher trigger has no CI analogue, and the Wave 3 timing cannot apply to Wave 8 cycles.
- anchor: "a CI-fix cycle engages with kind `ci` and releases after `push_completed` before the CI re-poll"
- anchor2: "review-fix cycles and CI-fix cycles"

#### L2.R2 (F10)

- claim: The request step never says the event carries timeline_baseline or original_is_draft, so the fold gets no baseline and classify_toggles cannot compute.
- anchor: "append the `draft_guard_requested` event with fsync before the call"
- anchor2: "`fold_draft_guard(events)` implementing every row of the section 4.2 effect table"

#### L2.R2 (F12)

- claim: The protocol already keys push records on cycle_id, so minting a new id in Task 8 can collide with the existing one, and no branch covers that case.
- anchor: "mints the cycle id with `fix_cycle_id` in the single place named by Task 1 O1"
- anchor2: "O1 names one single place where the guard-enabled cycle id is minted"

#### L2.R2 (F16)

- claim: A PR that merges while held is reported as held with a gh pr ready command, which cannot apply to a merged PR.
- anchor: "the held-exit list with the clear command"

#### L2.R3 (F1)

- claim: When the timeline is complete but its transition count is below the guard's recorded toggle count, the prescribed engage decision can return ENGAGE instead of halting as required.
- anchor: "classify_toggles(guard, read)` (the exact rule of ./source.md section 4.1: `unreadable` for a failed, incomplete or short timeline"
- anchor2: "the ref states that engage failure and an unreadable timeline at engage halt with `terminal_halted` reason `draft_guard_unavailable` before any edit"

## Other findings

- L3 (MAJOR, open, overlap): The required bullet names L3 and draft, so a test that fails on any L3 or draft condition cannot pass on the real file under a literal reading.
- L4 (MINOR, open, single): The exit code for ok:false results such as not_open is not assigned or asserted.
- L5 (MINOR, open, single): The grep acceptance still matches a comment with 43 after the change, so pass or fail depends on judgment.
- L6 (MINOR, open, single): Gitignored .claude paths never appear in git status, so the expected output cannot contain them.
- L7 (MINOR, open, single): Other tests/pr_submit files that pin SKILL text are run only at Task 10, so breakage surfaces later than the edit that caused it.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
