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
| L1 | open | yes | overlap | MAJOR | - | R1, R3 |
| L2 | open | no | single | MAJOR | - | R1 |
| L3 | open | no | single | MINOR | - | R1 |
| L4 | open | no | single | MINOR | - | R1 |
| L5 | open | yes | overlap | MAJOR | - | R2, R3 |
| L6 | open | no | single | MAJOR | - | R2 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: The implementer has no stated path for the POST input file and no stated format for classification_missing, so they must invent both.
- anchor: "the POST with `gh api -X POST repos/<R>/issues/<N>/issue-field-values --input <file>`"

#### L1.R3 (F1)

- claim: The command row can direct feature mode with area tests to Feature instead of the required Test issue type.
- anchor: "the `--mode` row (line 41) to \"Picks the feature or bug template, the Feature or Bug issue type and the `enhancement` / `bug` label\""
- anchor2: "the issue type rule (mode `bug` gives Bug; mode `feature` with area `tests` gives Test; every other feature gives Feature; Task is never chosen)"

### L5

#### L5.R3 (F2)

- claim: Task 12 requires an artifact outside the plan's permitted edit locations, so the scope constraint and required deliverable cannot both be satisfied.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L5.R2 (F1)

- claim: The plan requires a sync that writes under `.claude/` while prohibiting edits there.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`"

#### L5.R2 (F2)

- claim: The required owner-check artifact is outside the plan's permitted edit paths.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."

#### L5.R2 (F3)

- claim: The plan requires a mode-label write while stating that only the issue type and Complexity field are written to the issue.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

## Other findings

- L2 (MAJOR, open, single): Read literally, the Task 10 acceptance forces the claim gh api user line to be rewritten, contradicting the Task 2 user allowance.
- L3 (MINOR, open, single): The cited line 329 is stale (live row is 333), but the must re-read rule makes this cosmetic.
- L4 (MINOR, open, single): Keeping the old lowercase depth rule verbatim leaves a case mismatch against the new capitalized values.
- L6 (MAJOR, open, single): The plan does not specify the final-output reason when a type or field read-back request itself fails.

## Reviser brief

Blocking finding ids: L1, L5.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
