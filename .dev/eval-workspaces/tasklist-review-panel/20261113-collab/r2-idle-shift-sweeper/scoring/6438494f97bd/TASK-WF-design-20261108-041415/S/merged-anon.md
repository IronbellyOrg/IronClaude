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
| L1 | open | no | single | MAJOR | 2.2 | R1 |
| L2 | open | yes | overlap | MAJOR | - | R1, R2, R3 |
| L3 | open | no | single | MINOR | - | R1 |
| L4 | open | no | single | MINOR | - | R1 |
| L5 | open | no | single | MINOR | - | R1 |
| L6 | open | yes | single | MAJOR | - | R2 |

## Blocking findings

### L2

#### L2.R1 (F2)

- claim: Task 12 writes under ./artifacts/ while the Constraints limit edits to four other directories, and which artifacts/ directory is meant is not stated
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."
- anchor2: "- Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."

#### L2.R3 (F1)

- claim: The plan forbids edits under `.claude/` while requiring a sync target that copies files there.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`;"

#### L2.R3 (F2)

- claim: The plan requires applying a mode label and may post a pushback comment, contradicting its claim that only two things are written to the issue.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

#### L2.R3 (F3)

- claim: The required artifact path may fall outside the plan's stated edit scope, so the permitted location is unclear.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L2.R2 (F1)

- claim: The plan prohibits edits under `.claude/` and requires a sync that copies files there.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`;"

### L6

#### L6.R2 (F2)

- claim: For feature mode with area tests, the command row specifies Feature while the issue-type rule specifies Test.
- anchor: "the `--mode` row (line 41) to \"Picks the feature or bug template, the Feature or Bug issue type and the `enhancement` / `bug` label\""
- anchor2: "the issue type rule (mode `bug` gives Bug; mode `feature` with area `tests` gives Test; every other feature gives Feature; Task is never chosen)"

## Other findings

- L1 (MAJOR, open, single): Task 3 never states what classification_missing holds, so its value format is left to the implementer to guess
- L3 (MINOR, open, single): Cited test line numbers are stale (actual lines 545, 580, 695); covered by the plan's own re-read rule
- L4 (MINOR, open, single): The /sc:issue row is at line 333 in both HOW-WE-WORK files, not 329
- L5 (MINOR, open, single): The cited test is at line 695, not 642

## Reviser brief

Blocking finding ids: L2, L6.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report <redacted> byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
