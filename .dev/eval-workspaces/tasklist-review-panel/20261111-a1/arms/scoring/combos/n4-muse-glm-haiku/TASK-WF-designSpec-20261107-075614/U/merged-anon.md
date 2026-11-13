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
| L1 | open | yes | single | CRITICAL | - | R1 |
| L2 | open | yes | overlap | MAJOR | - | R1, R3 |
| L3 | open | no | single | MAJOR | - | R1 |
| L4 | open | no | overlap | MAJOR | - | R2, R3 |
| L5 | open | no | overlap | MAJOR | - | R2, R3 |
| L6 | open | no | single | MAJOR | - | R3 |
| L7 | open | no | single | MAJOR | - | R3 |
| L8 | open | no | single | MINOR | - | R3 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: Resume row 4 must re-enter release_decision but is given no target_sha or applied_edits, so a landed or normally completed push cannot pass the head proof and the PR stays draft instead of releasing.
- anchor: "`resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)`"
- anchor2: "`release_decision(*, mode, ordinal, cycle_id, guard, read, applied_edits, target_sha, push_completed)`"

#### L1.R1 (F2)

- claim: No stated rule rebinds a held guard to a later cycle, so the guard can keep the earlier cycle_id and judge the later cycle's publication against the earlier push.
- anchor: "`engage_decision(*, mode, ordinal, cycle_id, guard, read)` (all 11 rows, first match wins, `notes` carries `auto_merge_armed`)"

### L2

#### L2.R1 (F3)

- claim: Resume never states that a released ci cycle resumes the CI wait with no re-trigger, so a resumed CI cycle can be sent down the review re-trigger path instead.
- anchor: "`published` computed with `held_cycle_published` so that a push that completed normally before the crash also releases"

#### L2.R3 (F1)

- claim: A CI-fix cycle that runs Waves 3-5 mints a fix id at Wave 3 and a ci id at Wave 8, so the guard and the push triad carry different ids and a published CI fix leaves the PR draft.
- anchor: "the Wave 8 bullet states that a CI-fix cycle engages with kind `ci` and releases after `push_completed` before the CI re-poll"
- anchor2: "mints the cycle id with `fix_cycle_id` in the single place named by Task 1 O1"

#### L2.R3 (F2)

- claim: The Goal says draft at routing, while Wave 3 says draft at the end of Wave 3, leaving a window where the PR stays ready after a trigger.
- anchor: "a PR is turned into a draft as soon as a verified Medium-or-higher finding is routed to a fix"
- anchor2: "Engage at the end of Wave 3 (L3, only when at least one verified finding of Medium severity or higher is routed to a fix"

#### L2.R3 (F6)

- claim: Resume below ordinal 3 may reach release rows that the text never defines for a HELD phase.
- anchor: "Resume, loaded from Wave 0 at every ordinal and in both modes"
- anchor2: "ordinals 0 to 2 change only by one report line"

## Other findings

- L3 (MAJOR, open, single): The exact run_toggles + 1 count ignores landed failed mutations that the toggle classifier already allows for, so an applied crashed request can reconcile as ambiguous and hold.
- L4 (MAJOR, open, overlap): The strict import whitelist forbids the package-style `from __future__ import annotations` the module would otherwise carry; harmless on Python 3.10+ and absent from the acceptance criteria.
- L5 (MAJOR, open, overlap): The Wave 0 test criterion can be read as forbidding any L3 mention while the same task mandates an L3-with-off sentence inside the bullet; only the passes-on-the-real-file clause resolves it toward gate wording.
- L6 (MAJOR, open, single): Under set -euo pipefail a failed gh call aborts before the JSON prints, and without pipefail it reports zero transitions, so the transitions null and complete false check cannot pass as written.
- L7 (MAJOR, open, single): A foreign ready toggle during a hold can leave the PR ready while a fix is unpushed, and the text does not say re-draft, halt or report-only.
- L8 (MINOR, open, single): git status never lists gitignored paths, so the expected list is vacuous for the .claude mirrors.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
