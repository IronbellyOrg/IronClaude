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
| L1 | open | yes | overlap | MAJOR | - | R1, R2, R3 |
| L2 | open | no | single | MAJOR | - | R1 |
| L3 | open | no | single | MAJOR | - | R1 |
| L4 | open | no | single | MINOR | - | R1 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: Task 12 writes files outside the listed edit scope and does not say which artifacts folder it means; the reader must guess the plan folder.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R1 (F4)

- claim: As specified, no new test asserts the SKILL.md edit of Task 3; only the updated Task 7 test fails if Task 3 is reverted.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"

#### L1.R1 (F5)

- claim: The skill also applies the mode label and posts the pushback comment, so 'exactly two things' is imprecise.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L1.R1 (F6)

- claim: The constraints list three reversible defaults and Task 12 lists four.
- anchor: "the four defaults the owner may reverse (the `orgs/` read exception, keeping the `--type` flag, keeping the mode labels, area `tests` giving Test)"
- anchor2: "Decisions taken as defaults (the owner may reverse them later): the T3 worker may read exactly `orgs/<owner of R>/issue-fields`"

#### L1.R1 (F8)

- claim: The required prose 'no other orgs/ path' can match the orgs/ scanner as a bad path unless the regex is written around it; the source's 'never typed from user input' clause is also dropped.
- anchor: "`create.md` states the single `orgs/<owner>/issue-fields` exception and that no other `orgs/` path is allowed."
- anchor2: "every `orgs/` path found by regex in the skill folder files and the `AGENTS` files equals"

#### L1.R3 (F1)

- claim: The scope constraint forbids writing the two `./artifacts/` files that Task 12 requires, so the task cannot satisfy both instructions.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R2 (F1)

- claim: The plan both limits writes to two classification writes and requires a pushback comment, so an implementation must either omit that comment or violate the stated write limit.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "pushback comment"

#### L1.R2 (F2)

- claim: The plan forbids `.claude/` edits while requiring a sync that writes the generated development copies there.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint`"

#### L1.R2 (F3)

- claim: The required owner-check artifact is outside the plan's allowed edit locations.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

## Other findings

- L2 (MAJOR, open, single): The path of the POST body file is not stated; the source puts it at .dev/issues/<N>/complexity-field.json and the failure-case table relies on that.
- L3 (MAJOR, open, single): Source 2.2 says labels_applied and labels_missing now describe the mode label only, but no task carries that statement into SKILL.md or the docs.
- L4 (MINOR, open, single): The live /sc:issue row is at line 333 in both HOW-WE-WORK.md copies; the re-read constraint covers it.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
