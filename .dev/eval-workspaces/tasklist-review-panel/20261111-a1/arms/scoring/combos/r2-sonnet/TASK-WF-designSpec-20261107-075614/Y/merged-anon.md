review: 1 of 3
# Merged review 1 (coordinator script; panel of 4 reviewers)
candidate: <candidate file> sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- R3: report <redacted>, block ok true
- R2: report <redacted>, block ok true
- R4: report <redacted>, block ok true
- R1: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | R1, R2, R3, R4 |
| L2 | open | yes | overlap | CRITICAL | - | R2, R3, R4 |
| L3 | open | no | overlap | MAJOR | - | R1, R3 |
| L4 | open | no | overlap | MAJOR | - | R1, R2 |
| L5 | open | no | single | MAJOR | - | R2 |
| L6 | open | no | single | MINOR | - | R2 |
| L7 | open | no | single | MINOR | - | R2 |
| L8 | open | no | single | MINOR | - | R2 |
| L9 | open | no | single | MINOR | - | R1 |

## Blocking findings

### L1

#### L1.R3 (F1)

- claim: The plan assumes a pre-feature base, but the checkout already tracks the module, ref, script and tests, so Create would overwrite committed work and the named 43 test is absent.
- anchor: "Create `src/superclaude/pr_submit/merge_guard.py` following ./source.md sections 4.1, 4.2 and 4.6"
- anchor2: "the test `test_eventtype_is_43_members_with_silence_reviewer_and_conflict_events`"

#### L1.R3 (F3)

- claim: The observed count is never said to be relative to baseline, so a literal reading flags earlier author toggles as foreign and disables the guard.
- anchor: "`foreign` when observed transitions exceed `run_toggles + unsettled + failed_mutations`"
- anchor2: "phase_before_request, cycle_id, original_is_draft, baseline, run_toggles"

#### L1.R3 (F4)

- claim: A failed draft that actually landed leaves the PR draft under unavailable, and no exit text says to print the clear command.
- anchor: "`settled(draft, failed)` gives `RELEASE_PENDING`, increments `failed_mutations` and leaves `owned_draft` unchanged"
- anchor2: "`RELEASE_PENDING` with `owned_draft` true (`held`) and false (`unavailable`)"

#### L1.R3 (F5)

- claim: The Goal says engage at routing time, the owner decision says end of Wave 3, and they agree only if routing ends Wave 3, which is never stated.
- anchor: "a PR is turned into a draft as soon as a verified Medium-or-higher finding is routed to a fix"
- anchor2: "engage at the end of Wave 3"

#### L1.R3 (F6)

- claim: Row 4 has no ordinal condition, so a HELD guard at ordinal 2 with a landed dangling push gets a ready call that Task 11 forbids.
- anchor: "each re-enter `release_decision` with `push_completed=True`"
- anchor2: "held-guard reporting when the mode is `off` or the ordinal is below 3"

#### L1.R3 (F7)

- claim: The constraint says src only, but Tasks 2 and 13 edit tests and docs, and only the word canonical resolves the conflict.
- anchor: "Edit canonical files under `src/superclaude/` only, then run `make sync-dev`"

#### L1.R2 (F1)

- claim: A zero-edit cycle releases (PR marked ready) even when an earlier fixing cycle is held with its push unpublished, which the owner decision forbids.
- anchor: "unreadable timeline or unpublished exit keeps the PR draft"
- anchor2: "`release_decision` called with `applied_edits=0` for a new cycle while the guard record already holds an earlier fixing cycle returns `RELEASE` with cause `no_edits`"

#### L1.R2 (M2)

- claim: Medium: an armed auto-merge is only noted, so a release to ready could let GitHub merge before re-review; the candidate never states the handling. Promote to blocking if the owner confirms the merge behaviour (UNVERIFIED here).
- anchor: "`notes` carries `auto_merge_armed`"

#### L1.R2 (M3)

- claim: Medium: a draft call that fails on the client but lands leaves the PR draft with status unavailable, and no exit text says to print the clear command for that case.
- anchor: "`settled(draft, failed)` gives `RELEASE_PENDING`, increments `failed_mutations` and leaves `owned_draft` unchanged"
- anchor2: "`ENGAGE_PENDING` and `RELEASE_PENDING` with `owned_draft` true (`held`) and false (`unavailable`)"

#### L1.R2 (M4)

- claim: Medium: the Goal says engage as soon as routing happens, while the owner decision says engage at the end of Wave 3; the implementer can pick either timing.
- anchor: "a PR is turned into a draft as soon as a verified Medium-or-higher finding is routed to a fix"
- anchor2: "engage at the end of Wave 3"

#### L1.R2 (M6)

- claim: Medium: the plan's base does not match the checkout, which already tracks merge_guard.py, set-draft-state.sh, refs/merge-guard.md, a 45-member EventType and merge-guard bullets in SKILL.md; Create steps would overwrite them.
- anchor: "Create `src/superclaude/pr_submit/merge_guard.py` following ./source.md sections 4.1, 4.2 and 4.6"
- anchor2: "from \"exactly 43 members\" to 45"

#### L1.R2 (N1)

- claim: Minor: the clear command is spelled with "$REPO" in one task and <REPO> in another.
- anchor: "`gh pr ready <N> --repo \"$REPO\"`"
- anchor2: "`gh pr ready <N> --repo <REPO>`"

#### L1.R4 (F2)

- claim: Row 4 re-enters release with no target commit id in the resume inputs, so a landed push is either held or marked ready without a head check.
- anchor: "resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)"
- anchor2: "it returns `HOLD` for a head different from `target_sha`"

#### L1.R4 (F3)

- claim: Already-held does not retarget the cycle id, so resume can miss a later cycle's confirmed push and leave the pull request draft.
- anchor: "engage_decision(*, mode, ordinal, cycle_id, guard, read)` (all 11 rows, first match wins"

#### L1.R1 (F3)

- claim: The clear command is written in three forms, and Task 12 does not say which form is the exact one.
- anchor: "the clear command `gh pr ready <N> --repo <REPO>`"
- anchor2: "prints the clear command `gh pr ready <N> --repo \"$REPO\"` once"

### L2

#### L2.R3 (F2)

- claim: The Wave 0 test's match rule is unstated, and the required bullet text (off line naming L3, no draft call) cannot pass a literal word match.
- anchor: "contains no `L3 only` or `draft` gate wording"
- anchor2: "that applies at every ordinal and in both modes and carries no L3 or draft condition"

#### L2.R2 (M1)

- claim: Medium: the Wave 0 bullet must carry no L3 condition yet print the off line only at L3, so a correct bullet can fail the test that forbids naming L3.
- anchor: "carries no L3 or `draft` condition"
- anchor2: "at L3 with `--merge-guard off` the line"

#### L2.R4 (F1)

- claim: The Wave 0 bullet must name a level-3 condition, and the Wave 0 acceptance test must fail if the bullet names one, so the test cannot pass on the file the task requires.
- anchor: "and that at L3 with `--merge-guard off` the line \"Remediation is unprotected: --merge-guard off.\" is printed once"
- anchor2: "when it names an L3 or `draft` condition, or when the literal `off` line is missing"

## Other findings

- L3 (MAJOR, open, overlap): A gh line is undefined, so a usage comment naming gh or a multi-line gh call fails the line scan.
- L4 (MAJOR, open, overlap): Medium: the check compares only the literal start text, so it cannot prove byte-identity; the test passes while the rest of the sentence changes.
- L5 (MAJOR, open, single): Medium: the candidate does not say which mode a resumed run uses (the new command line or the mode in the run log), and the parsed value is not carried into RunConfig.
- L6 (MINOR, open, single): Minor: git status never lists gitignored .claude/ paths, so the mirrors clause is vacuous.
- L7 (MINOR, open, single): Minor: the conflict-cycle case appears in the case list but has no named test.
- L8 (MINOR, open, single): Minor: exit codes for not_open and verify_failed are not given in the candidate and rest on the missing source.
- L9 (MINOR, open, single): The grep for 43 still prints the 42nd-43rd conflict-event comment in models.py, so only a human reading, not the command output, can pass the criterion.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
