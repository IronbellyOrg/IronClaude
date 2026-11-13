review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- R2: report <redacted>, block ok true
- R3: report <redacted>, block ok true
- R1: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | MAJOR | - | R2 |
| L2 | open | no | single | MAJOR | - | R2 |
| L3 | open | yes | overlap | MAJOR | - | R2, R3 |
| L4 | open | no | single | MAJOR | - | R2 |
| L5 | open | no | single | MAJOR | - | R2 |
| L6 | open | no | single | MINOR | - | R2 |
| L7 | open | no | single | MAJOR | - | R2 |

## Blocking findings

### L1

#### L1.R2 (F1)

- claim: The Goal says draft as soon as a finding is routed, while the owner decision fixes engage at the end of Wave 3, so the two timings cannot both be built.
- anchor: "a PR is turned into a draft as soon as a verified Medium-or-higher finding is routed to a fix"
- anchor2: "engage at the end of Wave 3"

#### L1.R2 (F6)

- claim: Constraint 22 requires entries for git write verbs, but the per-task classification steps cover only gh pr and gh api lines.
- anchor: "contains `gh pr`, `gh api` or a git write verb needs one entry"
- anchor2: "for every line of the ref that matches `gh pr` or `gh api`"

#### L1.R2 (F7)

- claim: The clear command is spelled with a shell variable in one task and a placeholder in another, and no task picks one exact string.
- anchor: "prints the clear command `gh pr ready <N> --repo"
- anchor2: "the clear command `gh pr ready <N> --repo <REPO>`"

### L3

#### L3.R2 (F3)

- claim: Without the baseline subtraction and a test for it, an absolute timeline count marks a PR with earlier toggles as foreign and leaves it draft.
- anchor: "`foreign` when observed transitions exceed `run_toggles + unsettled + failed_mutations`"
- anchor2: "`ok` when observed equals `run_toggles + failed_mutations`"

#### L3.R3 (F1)

- claim: A complete timeline shorter than run_toggles is classified unreadable, but engage_decision has no unreadable-result row and can proceed to ENGAGE instead of halting.
- anchor: "`classify_toggles(guard, read)` (the exact rule of ./source.md section 4.1: `unreadable` for a failed, incomplete or short timeline"
- anchor2: "The ref states that engage failure and an unreadable timeline at engage halt with `terminal_halted` reason `draft_guard_unavailable` before any edit"

## Other findings

- L2 (MAJOR, open, single): The Wave 0 bullet must both carry no L3 or draft condition and state an L3-gated off line, so the test's forbidden tokens are ambiguous.
- L4 (MAJOR, open, single): Reading the acceptance as AND makes mode off at ordinal 3 with no record report released instead of off.
- L5 (MAJOR, open, single): The CI-fix engage has no trigger, so an implementer may engage on every CI run or on none.
- L6 (MINOR, open, single): The acceptance lists gitignored .claude mirrors among what git status shows, and gitignored paths never appear there.
- L7 (MAJOR, open, single): Task 1 needs a base-commit record but names no base commit, and this checkout already contains the feature code.

## Reviser brief

Blocking finding ids: L1, L3.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
