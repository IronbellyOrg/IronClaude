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
| L1 | open | yes | overlap | MAJOR | - | R2, R3 |
| L2 | open | yes | overlap | MAJOR | - | R2, R3, R4 |
| L3 | open | no | single | MAJOR | - | R2 |
| L4 | open | no | single | MINOR | - | R2 |
| L5 | open | no | single | MAJOR | - | R4 |
| L6 | open | no | single | MINOR | - | R4 |

## Blocking findings

### L1

#### L1.R3 (F1)

- claim: Following Task 3 as written replaces the tracked 605-line merge_guard.py that already exists on this tree, and Task 2's 43-R5 edit finds nothing to change.
- anchor: "Create `src/superclaude/pr_submit/merge_guard.py` following ./source.md sections 4.1, 4.2 and 4.6"
- anchor2: "change the module docstring and the `EventType` class docstring from \"exactly 43 members\" to 45"

#### L1.R3 (F2)

- claim: The effect table and the other decision tables are defined only in ./source.md, which is not in the package, so the row-count criteria cannot be checked from the package.
- anchor: "implementing every row of the section 4.2 effect table"

#### L1.R3 (F3)

- claim: An unsettled draft call that exits with owned_draft false reports unavailable instead of held, and prints no clear command even though the PR may be a draft.
- anchor: "an exit with unpublished or uncertain work leaves the PR draft and reports `held`"
- anchor2: "including `ENGAGE_PENDING` and `RELEASE_PENDING` with `owned_draft` true (`held`) and false (`unavailable`)"

#### L1.R3 (F4)

- claim: No exit status is named for a DISABLED guard whose cause is a foreign toggle, so the report state is left to the implementer.
- anchor: "`DISABLED` with `user_override` (`user_override`) and with `already_draft` (`off`)"
- anchor2: "foreign toggle disables the guard and the run continues"

#### L1.R3 (F6)

- claim: A draft call that finds the PR already drafted by someone else in the race window is recorded as owned, so a later release readies a PR the guard did not draft.
- anchor: "`settled(draft, confirmed, not changed)` gives `HELD` with `owned_draft` true and no toggle"

#### L1.R3 (F7)

- claim: The no-collision rule with CONFLICT_CYCLE_PREFIXES can only be met through is_conflict_cycle, since the import list excludes the constant.
- anchor: "The module imports only `enum`, `dataclasses`, `re` and `is_conflict_cycle` from `.conflicts`"

#### L1.R3 (F8)

- claim: A run that never engaged reports released, which implies a ready transition the run never made.
- anchor: "and no record at ordinal 3 (`released`)"

#### L1.R2 (F1)

- claim: Task 2 adds two enum members and renames a 43-member test, but models.py already has 45 members with these events, so following it duplicates the names and the import fails.
- anchor: "add `DRAFT_GUARD_REQUESTED = \"draft_guard_requested\"` and `DRAFT_GUARD_SETTLED = \"draft_guard_settled\"` to `EventType`"
- anchor2: "change the module docstring and the `EventType` class docstring from \"exactly 43 members\" to 45"

#### L1.R2 (F2)

- claim: Create and Edit verbs are given for files that already exist on disk, and the plan does not say how to reconcile them, so an implementer may overwrite committed work.
- anchor: "Create `src/superclaude/pr_submit/merge_guard.py` following ./source.md sections 4.1, 4.2 and 4.6"

### L2

#### L2.R3 (F5)

- claim: The Wave 0 bullet says it carries no L3 condition yet requires an L3-conditioned off line, and the test wording differs between Task 9's description and its acceptance text.
- anchor: "that applies at every ordinal and in both modes and carries no L3 or `draft` condition"
- anchor2: "at L3 with `--merge-guard off` the line \"Remediation is unprotected: --merge-guard off.\" is printed once"

#### L2.R2 (F3)

- claim: The Wave 0 bullet is said to carry no L3 condition, yet the same bullet requires an L3-only off line, so the placement test cannot be written as stated.
- anchor: "that applies at every ordinal and in both modes and carries no L3 or `draft` condition"
- anchor2: "at L3 with `--merge-guard off` the line \"Remediation is unprotected: --merge-guard off.\" is printed once"

#### L2.R4 (F1)

- claim: The required Wave 0 bullet must name an L3 condition, and the acceptance test fails when the bullet names an L3 condition, so the test cannot pass.
- anchor: "carries no L3 or `draft` condition"
- anchor2: "at L3 with `--merge-guard off` the line"

## Other findings

- L3 (MAJOR, open, single): The test compares only a start-text constant, which cannot prove the sentences are byte-identical as the acceptance criterion claims.
- L4 (MINOR, open, single): Gitignored mirrors never appear in git status, so listing them as allowed changes is vacuous.
- L5 (MAJOR, open, single): Row 4 re-enters release without a stated target SHA or this-cycle edit count, so a landed resume either cannot release or releases without the head check.
- L6 (MINOR, open, single): The constraints summary names a smaller release gate than Task 1, which records the live G1 and G2 checks and G6 as open too.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
