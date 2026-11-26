review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R2: report <redacted>, block ok true
- R1: report <redacted>, block ok true
- R3: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | R1, R2, R3 |
| L2 | open | yes | single | MAJOR | - | R2 |
| L3 | open | no | overlap | MAJOR | - | R1, R2 |
| L4 | open | no | single | MAJOR | - | R2 |
| L5 | open | no | single | MINOR | - | R2 |
| L6 | open | yes | single | MAJOR | - | R3 |
| L7 | open | no | single | MINOR | - | R3 |

## Blocking findings

### L1

#### L1.R2 (F1)

- claim: The constraint allows exactly two writes to the created issue, but Task 2 keeps the pushback comment, which is a third write.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L1.R2 (M2)

- claim: The artifact location is ambiguous between the project-root artifacts folder and the package folder, and only the first is outside the stated edit roots.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`"

#### L1.R2 (N1)

- claim: The live checkout already differs from the stated line numbers and from the labels.md and test state the plan assumes.
- anchor: "Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3` and must be re-read in the live file before each edit."

#### L1.R1 (F1)

- claim: The plan both forbids writes under `.claude/` and requires `make sync-dev`, which copies source files into `.claude/`.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`;"

#### L1.R1 (F2)

- claim: Task 12 requires an artifact outside the only permitted edit paths, so its acceptance criterion cannot be met under the stated scope constraint.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R3 (F1)

- claim: The plan both requires a mode label and limits issue writes to exactly two other values, so the create flow cannot satisfy both requirements.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type"
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

#### L1.R3 (F2)

- claim: The plan requires running a command that writes generated files under `.claude/` while forbidding edits there.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."

#### L1.R3 (F4)

- claim: Task 12 requires writing an artifact outside the directories allowed by Constraint 19.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

### L2

#### L2.R2 (F2)

- claim: The seven listed tests do not assert the Wave 1 names, the new error rows, or the flags row, so reverting those leaves every new test green and the acceptance line fails.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"

### L6

#### L6.R3 (F3)

- claim: Preserving the unchanged claim-mode `gh api user` lookup makes this acceptance criterion fail, while changing it would violate the requirement to leave claim behavior and text unchanged.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."

## Other findings

- L3 (MAJOR, open, overlap): The read-back match rule (name, option id or field id) is not stated, so a wrong guess gives a false not-applied line.
- L4 (MAJOR, open, single): The content and the STOP value of classification_missing are not stated, so the list may or may not include the not-applied lines.
- L5 (MINOR, open, single): The plan skips the level-table re-copy that the project rule requires, so the copy can stay stale when the phrase is absent.
- L7 (MINOR, open, single): The plan does not specify what to do when the Complexity field exists but is not single-select and therefore has no option name to POST.

## Reviser brief

Blocking finding ids: L1, L2, L6.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
