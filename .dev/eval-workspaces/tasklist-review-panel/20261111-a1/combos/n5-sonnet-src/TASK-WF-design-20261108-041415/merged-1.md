review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/candidate.md sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/n5-sonnet-src/t2b-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/n5-sonnet-src/t4-1.md, block ok true
- t1b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/n5-sonnet-src/t1b-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | t1b-1, t2b-1, t4-1 |
| L2 | open | no | single | MAJOR | - | t2b-1 |
| L3 | open | no | overlap | MAJOR | - | t1b-1, t2b-1 |
| L4 | open | no | overlap | MAJOR | - | t1b-1, t2b-1 |
| L5 | open | no | single | MINOR | - | t2b-1 |
| L6 | open | no | single | MAJOR | 3.4 | t1b-1 |
| L7 | open | no | single | MINOR | - | t1b-1 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: Task 12 requires writing owner-manual-check.md and t12-checks.log under ./artifacts/, a location the Constraints section forbids editing, so the owner's post-merge manual check lands in an unstaged, disallowed place.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.t2b-1 (F2)

- claim: The exactly-two-writes constraint forbids the pushback comment that Task 2 Wave 5 and the create-review-comment template require posting to the created issue, so honouring the constraint drops the comment and its E-POST-FAILED behaviour.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L1.t4-1 (F1)

- claim: Task 12 requires artifacts outside the plan's permitted edit locations, making the requirements incompatible.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."

#### L1.t1b-1 (F1)

- claim: The constraint caps issue writes at two, but the tasks also write the mode label and the pushback comment; the intent is clear from the tasks, so it is a Medium wording conflict.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "field POST and read-back; pushback comment; final output with every `not applied` and `not set` line"

#### L1.t1b-1 (F5)

- claim: No actor is named to write the Issue type row, and the T1 and T2 workers that write flags.md stay unchanged.
- anchor: "`flags.md` gets a derived `Issue type` row by the Q7 rule"

## Other findings

- L2 (MAJOR, open, single): Task 6's prescribed --mode row states feature picks the Feature issue type unconditionally while its --type row says a feature in tests selects Test, so the command file can tell users a feature never yields Test.
- L3 (MAJOR, open, overlap): Task 8's new orgs test also accepts the short orgs/<owner>/issue-fields form that Tasks 2, 3 and 5 never prescribe, so a file using the short form passes the pin while breaking the required text.
- L4 (MAJOR, open, overlap): The plan never states that the field read-back returns an option id with the name under single_select_option.name, so an implementer comparing the raw value to Simple/Medium/Complex reports the Complexity field as not applied after every successful POST.
- L5 (MINOR, open, single): Task 3 fixes the third block's keys but not its values, leaving the classification_missing format (each not-set line without its prefix) to be guessed from the cited source section.
- L6 (MAJOR, open, single): --type rides on the same gh issue create call, so an error caused by the type stops the whole create with E-CREATE-FAILED and the plan states no retry without --type.
- L7 (MINOR, open, single): Task 3 changes only the skill's Will Not list and the skill's Will list has no create line, so the agreement check has nothing to compare for Will.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
