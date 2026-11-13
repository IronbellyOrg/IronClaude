review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R1: report <redacted>, block ok true
- R3: report <redacted>, block ok true
- R2: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | 2.1 | R1 |
| L2 | open | no | single | MAJOR | 3.2 | R1 |
| L3 | open | no | single | MAJOR | 2.2 | R1 |
| L4 | open | no | single | MAJOR | 2.3 | R1 |
| L5 | open | no | single | MINOR | 2.1 | R1 |
| L6 | open | no | single | MINOR | - | R1 |
| L7 | open | no | overlap | MAJOR | - | R1, R2, R3 |
| L8 | open | yes | overlap | CRITICAL | - | R1, R2, R3 |
| L9 | open | no | single | MAJOR | - | R2 |

## Blocking findings

### L8

#### L8.R1 (F8)

- claim: Task 12 writes package artifacts and make sync-dev writes .claude/, both outside the edit-only list, though the intent is clear.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L8.R3 (F1)

- claim: Task 12 requires writing an artifact outside the only allowed edit roots, so the plan cannot be completed without violating Constraint 19.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L8.R2 (F1)

- claim: The exactly-two-writes rule omits the mode label the rest of the plan requires.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

#### L8.R2 (F2)

- claim: Task 12's artifact path is outside the allowed edit roots unless package-relative.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

## Other findings

- L1 (MAJOR, open, single): The plan never says how the read-back decides the value is present, and GitHub's read-back schema does not say whether value is an option name or id, so a comparison of value to the option name can report a false not applied.
- L2 (MAJOR, open, single): None of the six new tests asserts text only SKILL.md carries, so reverting Task 3 turns a new test red only if Task 7's updated test counts as new.
- L3 (MAJOR, open, single): Source 2.2 says labels_applied and labels_missing now describe the mode label only, but Task 3 does not ask for that wording, so the old description can stay.
- L4 (MAJOR, open, single): Task 6 adds no never-writes-another-field rule to the command's Will Not list although Task 3 adds it to the skill's list and Task 6's own criterion says they agree.
- L5 (MINOR, open, single): The constraint says exactly two writes to a created issue, but Task 2 also posts the pushback comment, so the wording needs to say two classification writes.
- L6 (MINOR, open, single): Q4's never typed from user input and never hard-coded field id and option names are not carried into the tasks.
- L7 (MAJOR, open, overlap): No minimum gh version is stated, and a gh without --type makes gh issue create fail as E-CREATE-FAILED when a type is listed.
- L9 (MAJOR, open, single): The POST test as worded conflicts with the worker read-only ban.

## Reviser brief

Blocking finding ids: L8.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
