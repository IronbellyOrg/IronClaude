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
| L1 | open | yes | overlap | CRITICAL | - | R1, R2, R3 |
| L2 | open | no | overlap | MAJOR | - | R1, R2 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: An implementer who follows the stated text as written posts a pushback comment, and that is wrong because the constraint allows only the type and the field value.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L1.R1 (F2)

- claim: An implementer who follows Task 12 writes four reversible defaults into the owner check, and that is wrong because constraint line 26 names three.
- anchor: "Decisions taken as defaults (the owner may reverse them later)"
- anchor2: "the four defaults the owner may reverse"

#### L1.R1 (F3)

- claim: An implementer who follows Task 12 writes into a project-root artifacts folder outside the four allowed roots, and the text does not say which folder the package uses.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`"
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R1 (F4)

- claim: No new test in Task 8 asserts text that Task 3 adds, so reverting Task 3 leaves every new test green.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"

#### L1.R1 (F5)

- claim: With an unspecified regex such as orgs/\S+, the required sentence in create.md is itself flagged by test 2.
- anchor: "every `orgs/` path found by regex in the skill folder files"
- anchor2: "that no other `orgs/` path is allowed"

#### L1.R1 (F6)

- claim: The command's Will Not list and the skill's Will Not list can differ by the field-write clause, so the Will/Will Not test may fail.
- anchor: "and the Will Not line (line 93) to also say it creates no issue types or issue fields"
- anchor2: "never writes a field other than Complexity"

#### L1.R1 (F7)

- claim: labels.md keeps gh label create lines that the skill may run, and the plan does not say the maintainer block is excluded from skill execution.
- anchor: "keep only the `bug` and `enhancement` lines in the maintainer block"
- anchor2: "The skill never creates a label, an issue type or an issue field."

#### L1.R1 (F8)

- claim: The no-edit rule and the sync-dev step both touch .claude/, and the text does not say generated output is allowed.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`"
- anchor2: "Run `make sync-dev`, then `make verify-sync`"

#### L1.R1 (F9)

- claim: The scanner the self-check feeds is not defined by any task.
- anchor: "feeds the `orgs/` scanner a text with `orgs/other/issue-fields`"

#### L1.R1 (F10)

- claim: The PUT check is narrower than the source, which says no file may contain -X PUT.
- anchor: "the skill folder and the agents contain `-X POST` together with `issue-field-values` and no `-X PUT`"

#### L1.R3 (F1)

- claim: Task 6 requires wording that says feature mode picks Feature even though the plan’s issue-type rule selects Test for a feature in the tests area.
- anchor: "the `--mode` row (line 41) to \"Picks the feature or bug template, the Feature or Bug issue type and the `enhancement` / `bug` label\""
- anchor2: "mode `bug` gives Bug; mode `feature` with area `tests` gives Test; every other feature gives Feature"

#### L1.R3 (F2)

- claim: The allowed edit scope excludes the artifacts directory where Task 12 requires the owner manual check to be written.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R2 (F1)

- claim: Task 12 requires artifact files outside the plan's allowed edit scope, so writing them violates the constraint and omitting them fails acceptance.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R2 (F2)

- claim: The required sync writes generated files under `.claude/`, contradicting the prohibition on editing that directory.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`"

## Other findings

- L2 (MAJOR, open, overlap): The flags-decision row and the create-review wording have no new test.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
