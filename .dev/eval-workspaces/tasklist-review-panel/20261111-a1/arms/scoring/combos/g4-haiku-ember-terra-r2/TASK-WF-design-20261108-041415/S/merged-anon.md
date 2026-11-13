review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R3: report <redacted>, block ok true
- R2: report <redacted>, block ok true
- R1: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | R1, R2, R3 |
| L2 | open | yes | overlap | MAJOR | - | R2, R3 |
| L3 | open | no | single | MINOR | - | R3 |
| L4 | open | no | single | MINOR | - | R3 |
| L5 | open | yes | overlap | MAJOR | - | R1, R2 |
| L6 | open | no | single | MINOR | - | R2 |

## Blocking findings

### L1

#### L1.R3 (F1)

- claim: The skill is told to write exactly two things to the created issue, yet Wave 5 also posts a pushback comment and the mode label is a further write.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "field POST and read-back; pushback comment; final output with every `not applied` and `not set` line"

#### L1.R3 (M1)

- claim: The quoted before-states and the 1aa2e5c3 baseline are absent at HEAD, and the document gives no rule for a task whose change is already present.
- anchor: "Edit `src/superclaude/core/HOW-WE-WORK.md` at line 329"
- anchor2: "Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3`"

#### L1.R3 (M2)

- claim: The base of ./artifacts is undefined, so the implementer may write to the project-root artifacts folder, which constraint 19 forbids and the repo never stages.
- anchor: "write `./artifacts/owner-manual-check.md` in this package"

#### L1.R2 (F1)

- claim: The live tree already has the new wording at HOW-WE-WORK.md line 330 and the old phrase is absent, so several edit instructions describe text that no longer exists and the plan is largely a no-op on this tree.
- anchor: "Edit `src/superclaude/core/HOW-WE-WORK.md` at line 329 (the `/sc:issue` row that says \"labels from a fixed set\"): change that phrase to \"an issue type, the Complexity field and a mode label\"."

#### L1.R2 (F4)

- claim: Task 12 writes outputs to ./artifacts/ outside the plan's own edit scope and gives no staging rule for them.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."

#### L1.R1 (F1)

- claim: The required package artifacts cannot be written while obeying the stated edit-scope restriction.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R1 (F2)

- claim: The required pushback comment is an additional write to the created issue that the stated two-write limit forbids.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type"
- anchor2: "field POST and read-back; pushback comment; final output"

### L2

#### L2.R3 (F2)

- claim: No specified new test asserts any SKILL.md text, so reverting Task 3 leaves every new test green and the acceptance criterion cannot pass.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"
- anchor2: "plus two new rows (issue type not available or not applied, Complexity field not available or write failed)"

#### L2.R3 (M3)

- claim: The text uses an orgs/ scanner it never says to write, so the self-check has no defined helper to test.
- anchor: "that feeds the `orgs/` scanner a text with `orgs/other/issue-fields`"

#### L2.R3 (N1)

- claim: The text calls the claim block separately from the first block, but the claim block is the second block, so the wording is ambiguous.
- anchor: "keep the first block key for key and the claim block unchanged"

#### L2.R2 (F2)

- claim: The values of the three new return-contract keys are stated only in source.md section 2.2 and the candidate acceptance criteria check keys only, so a different value format would still pass.
- anchor: "add a third YAML block with exactly the keys `issue_type`, `complexity_field`, `classification_missing`"

#### L2.R2 (F7)

- claim: The test-count acceptance gives no baseline count to rise from.
- anchor: "`uv run pytest tests/skills/test_issue_protocol.py -v` passes and the new tests are collected (the count of collected tests rises by at least seven)."

### L5

#### L5.R2 (F3)

- claim: No rule states how the field read-back is compared (option name versus numeric value) or which casing is sent, allowing a false not-set report under one allowed reading.
- anchor: "the POST with `gh api -X POST repos/<R>/issues/<N>/issue-field-values --input <file>`"

#### L5.R2 (F5)

- claim: The constraint demands --repo <R> on every gh label line but the plan does not say whether the kept maintainer lines are rewritten from <owner/repo> to <R>.
- anchor: "keep only the `bug` and `enhancement` lines in the maintainer block"

#### L5.R1 (F3)

- claim: The required mode description says feature mode picks Feature even though a feature in the tests area must receive Test.
- anchor: "Picks the feature or bug template, the Feature or Bug issue type and the `enhancement` / `bug` label"
- anchor2: "mode `feature` with area `tests` gives Test"

## Other findings

- L3 (MINOR, open, single): Agreement between the two Will lists is checked only by reading, since the named test checks skill tokens only.
- L4 (MINOR, open, single): The test line numbers have drifted (the test now sits at line 545), which constraint 25 already covers.
- L6 (MINOR, open, single): Byte-identical Claim section is required with no baseline hash or diff step recorded, so the check is not reproducible from the plan alone.

## Reviser brief

Blocking finding ids: L1, L2, L5.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
