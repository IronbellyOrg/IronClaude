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
| L2 | open | no | single | MINOR | - | R1 |
| L3 | open | yes | overlap | MAJOR | - | R1, R2 |
| L4 | open | no | single | MINOR | - | R1 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: The plan edits the exact lines that tests/skills/test_worker_contract.py classifies by text and adds new gh api lines, but never updates that table or runs that file, so two tests there go red.
- anchor: "then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`"

#### L1.R1 (F3)

- claim: The Task 3 span lacks --repo, which the fork-safety scan would flag if copied literally.
- anchor: "add the field POST and `gh issue create ... --type <name>` to the orchestrator's write list"
- anchor2: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`."

#### L1.R3 (F1)

- claim: The plan requires `make sync-dev` while prohibiting its generated updates under `.claude/`, so an implementer cannot satisfy both instructions.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`; fix any failure at its source in `src/superclaude/`, never by editing `.claude/`."

#### L1.R3 (F2)

- claim: Task 12 requires two files under `./artifacts/`, outside the plan's permitted edit locations, making the scope constraint and required deliverables incompatible.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R2 (F1)

- claim: The plan prohibits writing under `.claude/` while requiring a sync target that copies files there, so its instructions cannot both be followed.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`;"

### L3

#### L3.R1 (F4)

- claim: The command-file tests live in tests/commands/test_issue_command.py, which this check does not run.
- anchor: "`uv run pytest tests/skills/test_issue_protocol.py -k \"command\" -v` passes"

#### L3.R2 (F2)

- claim: The required `--mode` wording says feature mode selects Feature, contradicting the stated rule that feature mode with area `tests` selects Test.
- anchor: "the `--mode` row (line 41) to \"Picks the feature or bug template, the Feature or Bug issue type and the `enhancement` / `bug` label\""
- anchor2: "the issue type rule (mode `bug` gives Bug; mode `feature` with area `tests` gives Test; every other feature gives Feature; Task is never chosen)"

## Other findings

- L2 (MINOR, open, single): None of the seven new tests asserts on text that Task 3 adds, so reverting SKILL.md turns no new test red.
- L4 (MINOR, open, single): Line numbers are stale (329 vs live 333, test lines off) and Task 12 writes under ./artifacts/ against the edit-only-under list.

## Reviser brief

Blocking finding ids: L1, L3.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
