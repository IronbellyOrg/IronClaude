review: 1 of 3
# Merged review 1 (coordinator script; panel of 2 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R1: report <redacted>, block ok true
- R2: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | - | R1 |
| L2 | open | no | single | MAJOR | - | R1 |
| L3 | open | no | single | MAJOR | - | R1 |
| L4 | open | no | single | MAJOR | - | R1 |
| L5 | open | yes | overlap | CRITICAL | - | R1, R2 |
| L6 | open | no | single | MINOR | - | R1 |
| L7 | open | no | single | MINOR | - | R2 |

## Blocking findings

### L5

#### L5.R1 (F5)

- claim: The 'exactly two writes' constraint omits the mode label and the pushback comment that Tasks 2 and 3 keep.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "type read-back; field POST and read-back; pushback comment"

#### L5.R1 (F6)

- claim: Task 12 writes package artifacts outside the folders the constraint allows.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L5.R1 (F8)

- claim: The constraints name three reversible defaults and Task 12 asks the owner check to record four.
- anchor: "the four defaults the owner may reverse (the `orgs/` read exception, keeping the `--type` flag, keeping the mode labels, area `tests` giving Test)"
- anchor2: "Decisions taken as defaults (the owner may reverse them later)"

#### L5.R2 (F1)

- claim: Constraints limits create mode to exactly two writes while Goal and Task 1 require a third write (the mode label), so both texts cannot hold.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

#### L5.R2 (F2)

- claim: Task 12 writes under ./artifacts which the allowed-dirs constraint does not list; the package-local meaning is inferrable but unstated.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."

#### L5.R2 (F4)

- claim: Plan never says to normalize the retained maintainer gh label lines to --repo <R>; live file spells --repo <owner/repo>.
- anchor: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`."

## Other findings

- L1 (MAJOR, open, single): None of the seven listed tests asserts text that Task 3 adds to SKILL.md, so reverting Task 3 turns no new test red unless the implementer adds an unlisted test.
- L2 (MAJOR, open, single): Task 3 leaves the skill's Will list untouched and the two Will Not edits differ in wording, so 'agree' has two readings.
- L3 (MAJOR, open, single): The design doc keeps `gh api user -q .login`, which a literal reading of this criterion rejects, although the plan's rule elsewhere allows `user`.
- L4 (MAJOR, open, single): A gh build that does not know --type would make every create STOP, and the plan names no minimum gh version or retry without --type.
- L6 (MINOR, open, single): The source says labels_applied and labels_missing now describe the mode label only, and Task 3 does not list that wording change.
- L7 (MINOR, open, single): Pinned line number is stale (live file has the phrase at line 330); the plan re-read guard covers it.

## Reviser brief

Blocking finding ids: L5.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
