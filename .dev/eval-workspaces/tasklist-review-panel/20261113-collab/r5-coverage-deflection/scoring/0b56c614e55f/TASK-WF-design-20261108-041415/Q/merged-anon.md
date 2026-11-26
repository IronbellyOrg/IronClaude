review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R2: report <redacted> block ok true
- R3: report <redacted> block ok true
- R1: report <redacted> block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | R1, R2, R3 |
| L2 | open | yes | overlap | MAJOR | - | R1, R2 |
| L3 | open | no | single | MINOR | - | R2 |
| L4 | open | no | single | MINOR | - | R2 |

## Blocking findings

### L1

#### L1.R2 (F1)

- claim: The seven listed new tests cannot turn red when Task 3 (SKILL.md) is reverted, so the stated acceptance criterion cannot pass.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red: each new test asserts on the text that task adds."
- anchor2: "Write one test per rule, each failing when the behaviour breaks."

#### L1.R2 (F3)

- claim: The prose sentence in create.md may be caught by the orgs scanner, whose regex is not stated, so the scan can fail on its own wording.
- anchor: "that no other `orgs/` path is allowed"
- anchor2: "every `orgs/` path found by regex in the skill folder files"

#### L1.R2 (F5)

- claim: The relative ./artifacts path could be read as the project-root folder, which is never staged, instead of the package folder.
- anchor: "write `./artifacts/owner-manual-check.md` in this package."

#### L1.R2 (F8)

- claim: The never-edit rule sits beside a required make sync-dev, which writes under .claude/, with no note that the sync is the sanctioned exception.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`"

#### L1.R3 (F1)

- claim: The plan requires a pushback comment on the issue while also limiting writes besides issue creation to exactly the type and Complexity field.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L1.R3 (F2)

- claim: The required manual-check document and check log are outside the plan's allowed edit locations.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R3 (F3)

- claim: The required sync copies source files into `.claude/`, conflicting with the instruction never to edit there.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`;"

#### L1.R1 (F2)

- claim: Task 12 requires an artifact outside the plan's allowed edit paths, so the scope constraint and artifact acceptance criterion cannot both be satisfied.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R1 (F3)

- claim: The plan prohibits `.claude/` edits but requires a sync that updates `.claude/` development copies.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint`"

### L2

#### L2.R2 (F2)

- claim: The command Will Not list omits the Complexity-only clause that SKILL.md Will Not gains, so the agreement acceptance can fail unless the implementer guesses.
- anchor: "to also say it creates no issue types or issue fields"
- anchor2: "never writes a field other than Complexity"

#### L2.R2 (F4)

- claim: A successful create run with no unset classification has no defined value for classification_missing, so [] versus null is a guess.
- anchor: "on a STOP the fields that do not apply are `null`"

#### L2.R1 (F1)

- claim: The required mode-row wording says a feature uses the Feature type while the same task requires feature area `tests` to use Test.
- anchor: "the `--mode` row (line 41) to \"Picks the feature or bug template, the Feature or Bug issue type and the `enhancement` / `bug` label\""
- anchor2: "the `--type` row (line 42) to say the area of the change, which selects issue type Test for a feature in `tests`"

## Other findings

- L3 (MINOR, open, single): Stale line numbers: that test is at line 580 and the return-contract test is at 545, not 492 to 520.
- L4 (MINOR, open, single): Hand-editing CLAUDE.md skips the level-table copy that the project rule requires.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
