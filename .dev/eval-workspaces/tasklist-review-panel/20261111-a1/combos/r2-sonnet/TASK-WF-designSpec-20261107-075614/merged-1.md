review: 1 of 3
# Merged review 1 (coordinator script; panel of 4 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/candidate.md sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/reviews/combos/r2-sonnet/t4-1.md, block ok true
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/reviews/combos/r2-sonnet/t3-1.md, block ok true
- t4-2: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/reviews/combos/r2-sonnet/t4-2.md, block ok true
- t1b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/reviews/combos/r2-sonnet/t1b-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | t1b-1, t3-1, t4-1 |
| L2 | open | no | overlap | MAJOR | - | t1b-1, t3-1, t4-1, t4-2 |
| L3 | open | yes | overlap | MAJOR | - | t1b-1, t3-1, t4-1, t4-2 |
| L4 | open | no | single | MAJOR | - | t3-1 |
| L5 | open | no | single | MAJOR | - | t3-1 |
| L6 | open | no | single | MAJOR | - | t3-1 |
| L7 | open | no | single | MINOR | - | t3-1 |
| L8 | open | no | single | MINOR | - | t3-1 |
| L9 | open | no | single | MINOR | - | t4-2 |
| L10 | open | no | single | MINOR | - | t1b-1 |

## Blocking findings

### L1

#### L1.t4-1 (F1)

- claim: The Goal makes the draft flip happen as soon as a finding is routed, while Constraint 26 and Task 8 fix engage at the end of Wave 3, so a PR can stay ready for the rest of Wave 3 with a routed Medium finding pending.
- anchor: "a PR is turned into a draft as soon as a verified Medium-or-higher finding is routed to a fix"
- anchor2: "engage at the end of Wave 3"

#### L1.t4-1 (F3)

- claim: Engage is gated on a verified Medium-or-higher finding, but a failing CI check has no severity, so the document does not say whether a CI-fix cycle engages.
- anchor: "a CI-fix cycle engages with kind `ci` and releases after `push_completed` before the CI re-poll"
- anchor2: "review-fix cycles and CI-fix cycles"

#### L1.t4-1 (F5)

- claim: Constraint 22 requires classification of git write verb lines as well as gh lines, but Task 8 classifies only gh lines while allowing fenced git command lines, so a ref with a git write line fails the classification test.
- anchor: "for every line of the ref that matches `gh pr` or `gh api`"
- anchor2: "that contains `gh pr`, `gh api` or a git write verb needs one entry in `WRITE_VERB_CLASSIFICATION`"

#### L1.t3-1 (F4)

- claim: An implementer who compares only the literal start text builds a check that stays green when the rest of the pinned sentence changes, so byte-identity is not established.
- anchor: "are asserted byte-identical by comparing the live text with string constants"

#### L1.t1b-1 (F5)

- claim: The engage trigger needs a verified finding of Medium severity or higher, which a failing CI check does not carry, so whether a CI fix engages is undefined.
- anchor: "a CI-fix cycle engages with kind `ci` and releases after `push_completed` before the CI re-poll"

### L3

#### L3.t4-1 (F4)

- claim: This checkout already contains merge_guard.py, the 45-member enum with the guard events, and the CORE_PURE_FILES entry, so the create steps overwrite committed code and the Task 1 baseline is not pre-feature.
- anchor: "Create `src/superclaude/pr_submit/merge_guard.py` following ./source.md sections 4.1, 4.2 and 4.6"
- anchor2: "Add `src/superclaude/pr_submit/merge_guard.py` to `CORE_PURE_FILES` in `tests/pr_submit/test_static_grep.py`"

#### L3.t3-1 (F2)

- claim: An implementer who follows resume row 4 as written may release a held PR at ordinal 2, and the text never gates that release below ordinal 3.
- anchor: "phase `HELD` with `dangling_branch == \"landed\"` and phase `HELD` with `dangling_branch is None`"
- anchor2: "never contains any `pr ready` call at ordinal 2 or with `off`"

#### L3.t4-2 (F1)

- claim: The 11-row engage table returns ENGAGE on a complete timeline shorter than run_toggles, so the run edits instead of halting.
- anchor: "an unreadable timeline at engage halt with `terminal_halted` reason `draft_guard_unavailable` before any edit"
- anchor2: "`engage_decision(*, mode, ordinal, cycle_id, guard, read)` (all 11 rows, first match wins, `notes` carries `auto_merge_armed`)"

#### L3.t4-2 (F2)

- claim: An engage read failure appends no event, so the exit field is released, but section 4.1 says that halt reports unavailable.
- anchor: "following ./source.md sections 4.1, 4.2 and 4.6"
- anchor2: "and no record at ordinal 3 (`released`)."

#### L3.t4-2 (F4)

- claim: Row 4 cannot both follow the stated signature and prove the pushed head before release.
- anchor: "`resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)`"
- anchor2: "re-enter `release_decision` with `push_completed=True`"

#### L3.t4-2 (F5)

- claim: After a failed first engage, resume is NOOP and the next engage is HOLD, so a resumed run can edit a ready pull request.
- anchor: "`settled(draft, failed)` gives `RELEASE_PENDING`, increments `failed_mutations` and leaves `owned_draft` unchanged"

#### L3.t1b-1 (F1)

- claim: The engage-failure halt is not required to name --merge-guard off or print the clear command, so a draft call that failed on the client but landed leaves a draft PR with no instruction.
- anchor: "halt with `terminal_halted` reason `draft_guard_unavailable` before any edit"

#### L3.t1b-1 (F2)

- claim: A guard kept held across cycles keeps its old cycle_id, so resume after a crash in a later cycle judges publication and target_sha on the wrong cycle and leaves the PR draft.
- anchor: "true when a `push_completed` event, normal or recovered, carries the guard's `cycle_id`"
- anchor2: "all 11 rows, first match wins, `notes` carries `auto_merge_armed`"

## Other findings

- L2 (MAJOR, open, overlap): The Wave 0 bullet must name an L3 condition and a draft call, yet its test must fail on a bullet that names an L3 or draft condition and pass on the real file, which needs an undefined reading of names.
- L4 (MAJOR, open, single): An implementer who follows the stated text as written creates files that already exist and are tracked, so the Create step overwrites committed work or forces a guess about reconciling it.
- L5 (MAJOR, open, single): An implementer who follows Task 6 as written parses `--merge-guard` into SkillArgs and leaves the run path untouched, so nothing in code is stated to read the value.
- L6 (MAJOR, open, single): An implementer who follows the stated exit codes must guess the exit code for not_open and verify_failed, which the protocol's halt depends on.
- L7 (MINOR, open, single): The named test does not exist; the repo's test is test_eventtype_is_45_members_with_silence_reviewer_conflict_and_guard_events, so an implementer cannot locate the symbol the step renames.
- L8 (MINOR, open, single): The acceptance line lists gitignored mirrors as allowed changes, but gitignored paths never appear in git status --short, so the line adds nothing and blurs the no-stage rule.
- L9 (MINOR, open, single): A raw grep for 43 still prints the 42nd-43rd conflict-cycle comment, which is not an enum-size claim.
- L10 (MINOR, open, single): A heading named Merge guard does not match grep for merge-guard, so the AC needs the flag in the heading, which the task does not say.

## Reviser brief

Blocking finding ids: L1, L3.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
