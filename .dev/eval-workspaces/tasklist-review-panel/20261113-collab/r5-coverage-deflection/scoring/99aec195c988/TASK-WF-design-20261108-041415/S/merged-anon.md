review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R1: report <redacted> block ok true
- R3: report <redacted> block ok true
- R2: report <redacted> block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | MAJOR | 2.3 | R1 |
| L2 | open | yes | overlap | MAJOR | - | R1, R2, R3 |
| L3 | open | no | single | MAJOR | - | R1 |
| L4 | open | no | single | MINOR | 2.1, 2.2 | R1 |
| L5 | open | no | single | MINOR | - | R1 |
| L6 | open | no | single | MINOR | 3.4 | R1 |
| L7 | open | yes | single | MAJOR | - | R3 |
| L8 | open | no | single | MAJOR | - | R3 |
| L9 | open | no | single | MAJOR | - | R2 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: Task 10's acceptance line fails on the retained `gh api user -q .login` claim lookup, because `user` is allowed everywhere else in the plan.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`"

### L2

#### L2.R1 (F2)

- claim: tests/skills/test_worker_contract.py pins create.md:9, SKILL.md:73-74 and issue-worker-t3.md:27 by exact text and flags every new gh api line, so two of its tests go red and no stated check runs it.
- anchor: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`"

#### L2.R1 (F4)

- claim: The pushback comment and the --label flag are also writes to the created issue, so the exactly-two claim has exceptions.
- anchor: "It writes exactly two things to a created issue besides the issue itself"

#### L2.R1 (F8)

- claim: Live lines differ from the task text: HOW-WE-WORK row 333 not 329, and the tests at 545, 580 and 695 not 492, 527 and 642.
- anchor: "Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3` and must be re-read in the live file before each edit."

#### L2.R3 (F1)

- claim: The required mode label makes the stated two-write limit contradict the required issue-type and field writes.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

#### L2.R2 (F1)

- claim: The plan both requires applying a mode label and limits writes besides issue creation to exactly two, making the required three classifications inconsistent with the constraint.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

#### L2.R2 (F2)

- claim: Task 12 requires an artifact outside the allowed edit locations, so the implementer must either violate the constraint or fail the required artifact check.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

### L7

#### L7.R3 (F2)

- claim: This acceptance criterion cannot pass while the existing `gh api user` claim-flow text is retained as instructed.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "Leave history and decision-log entries as they are except for wording that is now false."

## Other findings

- L3 (MAJOR, open, single): None of the seven listed new tests asserts on text only SKILL.md adds, so reverting Task 3 turns no new test red.
- L4 (MINOR, open, single): A failed pushback comment stops the run after the type and field steps, before the not-set list is printed, and the third block's content on that STOP is not defined.
- L5 (MINOR, open, single): For flags.md the task body edits only two option rows, so the acceptance line asks for more than the body edits.
- L6 (MINOR, open, single): If the installed gh rejects --type, gh issue create fails and the run stops with E-CREATE-FAILED, although a type problem is meant never to stop the run.
- L8 (MAJOR, open, single): The planned static text checks would not catch runtime regressions in the create-flow branching and failure handling.
- L9 (MAJOR, open, single): The plan does not define behavior for a Complexity field whose recorded data type is not single-select, so the worker may attempt a write that cannot use the specified option-name value.

## Reviser brief

Blocking finding ids: L1, L2, L7.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
