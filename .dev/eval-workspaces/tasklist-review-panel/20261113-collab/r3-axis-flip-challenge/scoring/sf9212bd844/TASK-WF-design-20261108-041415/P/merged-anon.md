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
| L1 | open | yes | single | CRITICAL | - | R1 |
| L2 | open | yes | single | CRITICAL | - | R1 |
| L3 | open | no | single | MAJOR | - | R1 |
| L4 | open | yes | overlap | MAJOR | - | R1, R3 |
| L5 | open | no | single | MINOR | - | R1 |
| L6 | open | no | single | MAJOR | - | R1 |
| L7 | open | yes | overlap | CRITICAL | - | R1, R2 |
| L8 | open | no | single | MAJOR | - | R3 |
| L9 | open | no | single | MAJOR | - | R2 |

## Blocking findings

### L1

#### L1.R1 (f1)

- claim: Task 3 can be reverted without turning any new Task 8 test red, so the stated acceptance criterion cannot pass as written.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red: each new test asserts on the text that task adds."
- anchor2: "Second, every `orgs/` path found by regex in the skill folder files and the `AGENTS` files equals `orgs/<owner of R>/issue-fields` or `orgs/<owner>/issue-fields` and appears only in `create.md`, `SKIL"

#### L1.R1 (f2)

- claim: Task 8 permits two orgs-path spellings while the rest of the candidate uses only one, with no stated equivalence.
- anchor: "equals `orgs/<owner of R>/issue-fields` or `orgs/<owner>/issue-fields` and appears only in `create.md`, `SKILL.md` and `issue-worker-t3.md`"

### L2

#### L2.R1 (f3)

- claim: The unchanged claim lookup 'gh api user' in docs/designs/sc-issue-command.md:157 violates the stated universal path rule, so the criterion cannot pass without breaking the claim flow.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."

### L4

#### L4.R1 (f4)

- claim: The candidate never states the complexity-field.json path under the renamed .dev/issues/<N>/ directory that the source failure table depends on.
- anchor: "the POST with `gh api -X POST repos/<R>/issues/<N>/issue-field-values --input <file>`"

#### L4.R1 (f5)

- claim: The --mode help cell names only Feature or Bug issue types, leaving out Test for a feature in tests, so the cell understates the Q7 rule stated in Task 1 and in Task 9.
- anchor: "Picks the feature or bug template, the Feature or Bug issue type and the `enhancement` / `bug` label"

#### L4.R3 (f1)

- claim: The command wording says feature mode selects Feature even though the stated rule selects Test for a feature in the tests area.
- anchor: "the `--mode` row (line 41) to \"Picks the feature or bug template, the Feature or Bug issue type and the `enhancement` / `bug` label\""
- anchor2: "mode `bug` gives Bug; mode `feature` with area `tests` gives Test; every other feature gives Feature"

### L7

#### L7.R1 (f6)

- claim: The exactly-two constraint excludes the mode label that the Goal and Tasks 1 and 2 require the skill to apply to the created issue, so the two stated requirements cannot both be met.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

#### L7.R2 (f1)

- claim: The plan both requires applying a mode label and limits writes to exactly two items besides the issue, but the label is a third write.
- anchor: "The skill never creates a label, an issue type or an issue field. It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Co"
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

## Other findings

- L3 (MAJOR, open, single): The candidate never states the third block values (read-back or null, prefix stripped from classification_missing), so tests pass on values the source forbids.
- L5 (MINOR, open, single): Cited line numbers are stale (HOW-WE-WORK.md:333, test_st10 at 545, Will/Will Not test at 580); the candidate already requires re-reading live lines, so this is a note only.
- L6 (MAJOR, open, single): No task in the candidate lists the eight reason strings from specification 2.4, so the every-reason requirement for labels.md is unstated in the tasks and the Task 8 format test checks only the line prefixes.
- L8 (MAJOR, open, single): The plan records the field data type but does not specify behavior when Complexity is not a single-select field.
- L9 (MAJOR, open, single): The plan requires artifacts at a relative path without stating whether that package directory is allowed by the edit-path constraint.

## Reviser brief

Blocking finding ids: L1, L2, L4, L7.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report <redacted> byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
