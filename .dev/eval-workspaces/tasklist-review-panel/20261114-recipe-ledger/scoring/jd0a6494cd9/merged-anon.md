review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R1: report <path>, block ok true
- R2: report <path>, block ok true
- R3: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | - | R1 |
| L2 | open | no | single | MAJOR | - | R1 |
| L3 | open | yes | overlap | MAJOR | - | R1, R3 |
| L4 | open | no | single | MAJOR | - | R1 |
| L5 | open | no | single | MINOR | - | R1 |
| L6 | open | no | single | MINOR | - | R1 |
| L7 | open | no | single | MINOR | - | R1 |
| L8 | open | yes | overlap | MAJOR | 2.1 | R2, R3 |
| L9 | open | yes | single | MAJOR | 3.4 | R2 |
| L10 | open | no | single | MAJOR | 2.2 | R2 |

## Blocking findings

### L3

#### L3.t2b-1 (F4)

- claim: The exactly-two claim contradicts Wave 5 keeping the mode label and the pushback comment write.
- anchor: "It writes exactly two things to a created issue besides the issue itself"

#### L3.t2b-1 (F10)

- claim: Task 12 writes ./artifacts/t12-checks.log and ./artifacts/owner-manual-check.md outside the four edit roots.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`"

#### L3.t4-1 (F2)

- claim: The candidate forbids editing `.claude/` while requiring `make sync-dev`, which updates generated development copies under that directory.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."

#### L3.t4-1 (F3)

- claim: The candidate’s required `./artifacts/owner-manual-check.md` output is outside its allowed edit paths.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."

### L8

#### L8.t3-1 (F1)

- claim: An implementer who follows the stated text as written builds a create flow that applies the mode label while limiting writes to the issue type and Complexity field; that is wrong because the plan requires three classifications to be written but permits exactly two.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

#### L8.t4-1 (F1)

- claim: The candidate requires a pushback comment after creation but limits writes to the issue to its type and field, omitting the comment as a third issue write.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."

### L9

#### L9.t3-1 (F2)

- claim: An implementer who follows the stated text as written builds a plan that requires an artifact outside its allowed edit locations; that is wrong because the task both requires and forbids that write.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

## Other findings

- L1 (MAJOR, open, single): The plan never lists the not-set reasons, so labels.md can omit option not found and still match the formats as written.
- L2 (MAJOR, open, single): E-POST-FAILED sits beside the new Complexity POST, so it can be misread as making a field-write failure fatal instead of a not set line.
- L4 (MAJOR, open, single): Only the keys are specified, dropping the source semantics that classification_missing holds each not set line without the prefix.
- L5 (MINOR, open, single): The area recording in the pushback comment required by Q5 is dropped from the command file wording.
- L6 (MINOR, open, single): Line numbers are stale against live files (329 vs 333, 642 vs 695, 492-520 vs 545), relying on the re-read rule.
- L7 (MINOR, open, single): The same sentence stays not silently relabelled in refs/create.md while the design doc gets reclassified.
- L10 (MAJOR, open, single): The candidate requires the new return-contract keys but does not specify their values or meanings, which the source defines as read-back values or null and the missing-classification list.

## Reviser brief

Blocking finding ids: L3, L8, L9.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
