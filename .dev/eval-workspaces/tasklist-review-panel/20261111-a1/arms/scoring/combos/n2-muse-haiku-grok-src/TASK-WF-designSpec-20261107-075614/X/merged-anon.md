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
| L1 | open | yes | overlap | CRITICAL | - | R1, R2, R3 |
| L2 | open | no | overlap | MAJOR | - | R1, R2 |
| L3 | open | no | overlap | MAJOR | - | R1, R2 |
| L4 | open | no | single | MINOR | - | R1 |
| L5 | open | yes | overlap | MAJOR | - | R2, R3 |
| L6 | open | no | single | MINOR | - | R2 |
| L7 | open | no | single | MINOR | - | R2 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: Resume row 4 must re-enter release_decision, whose head confirmation needs target_sha and applied_edits that no resume input or folded guard field supplies, so a published cycle either releases without head confirmation or never releases.
- anchor: "`resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)` (all 9 rows"
- anchor2: "`release_decision(*, mode, ordinal, cycle_id, guard, read, applied_edits, target_sha, push_completed)` (all 9 rows"

#### L1.R1 (F3)

- claim: A later cycle starting while the guard is HELD gets NOOP(already_held) and no new request, so the guard keeps the earlier cycle_id and publication is judged against the earlier cycle's push.
- anchor: "`held_cycle_published(events, guard)` (true when a `push_completed` event, normal or recovered, carries the guard's `cycle_id`)"

#### L1.R2 (F1)

- claim: The plan says to create or rename files and tests that already exist at HEAD, with no rule for an existing file, so following it overwrites committed code and the base-commit record cannot show a pre-feature baseline.
- anchor: "Create `src/superclaude/pr_submit/merge_guard.py` following ./source.md sections 4.1, 4.2 and 4.6"

#### L1.R2 (F3)

- claim: Resume re-enters release_decision without applied_edits or target_sha, so the head check has no defined source and an implementer may pass the live head, making it always pass.
- anchor: "each re-enter `release_decision` with `push_completed=True`"
- anchor2: "`resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)`"

#### L1.R2 (F6)

- claim: Without the baseline subtraction stated in the candidate, an implementer compares the absolute timeline count, so earlier human toggles read as foreign and disable the guard.
- anchor: "`foreign` when observed transitions exceed `run_toggles + unsettled + failed_mutations`"

#### L1.R2 (M4)

- claim: No test pins ordinal 2 with phase HELD and a dangling landed branch, the case where a release call would be wrong.
- anchor: "phases `RELEASED` and `DISABLED` skip row 2"

#### L1.R3 (F1)

- claim: A new cycle while the guard is held does nothing and resume marks the pull request ready from the old cycle's push, while the new fix is still local.
- anchor: "all 11 rows, first match wins"
- anchor2: "true when a `push_completed` event, normal or recovered, carries the guard's `cycle_id`"

### L5

#### L5.R2 (F4)

- claim: Start-text constants cannot prove the two pinned sentences are byte-identical, which is what the acceptance criterion requires.
- anchor: "are asserted byte-identical by comparing the live text with string constants"
- anchor2: "the literal start text recorded in `./artifacts/pre-build-gate.md`"

#### L5.R3 (F2)

- claim: Resume after a confirmed CI-fix push runs the review re-trigger instead of the CI re-poll.
- anchor: "(`published` true) releases before the re-trigger"
- anchor2: "releases after `push_completed` before the CI re-poll"

## Other findings

- L2 (MAJOR, open, overlap): The Wave 0 bullet must both carry no L3 condition and state the L3 off print, while its acceptance fails a bullet that names an L3 condition, so a literally written test rejects the mandated bullet.
- L3 (MAJOR, open, overlap): Tasks 7, 8 and 12 only require classification entries for gh pr or gh api lines, omitting the git write verbs the plan constraint requires, so a new git write line would fail the worker-contract test unclassified.
- L4 (MINOR, open, single): This assertion cannot detect a wrongly routed draft attempt on an already-draft PR, because the script makes no pr ready call in that case either.
- L6 (MINOR, open, single): The released status is printed for a PR that was never drafted, which reads as if a draft was released.
- L7 (MINOR, open, single): Gitignored .claude mirrors never appear in git status, so the acceptance wording is incoherent.

## Reviser brief

Blocking finding ids: L1, L5.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
