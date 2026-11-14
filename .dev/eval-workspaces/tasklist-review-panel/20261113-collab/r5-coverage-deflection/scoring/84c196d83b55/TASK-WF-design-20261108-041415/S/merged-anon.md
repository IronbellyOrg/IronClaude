review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R1: report <redacted> block ok true
- R3: report <redacted> block ok true
- R2: report <redacted> block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | R1, R2 |
| L2 | open | no | single | MAJOR | - | R1 |
| L3 | open | no | overlap | MAJOR | - | R1, R2 |
| L4 | open | no | single | MINOR | - | R1 |
| L5 | open | yes | overlap | MAJOR | - | R2, R3 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: The Task 10 criterion cannot pass because the design doc keeps `gh api user -q .login` (line 157), and Task 2 itself keeps `user` as an allowed path.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`"

#### L1.R1 (F3)

- claim: Final checks skip tests/skills/test_issue_worker_agents.py and tests/commands/test_issue_command.py, which check files edited by Tasks 5 and 6.
- anchor: "`make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`; fix any failure at its source"

#### L1.R1 (F4)

- claim: The Constraints say two writes to the created issue, but Wave 5 also applies a mode label and posts a pushback comment.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L1.R1 (F7)

- claim: Task 12 counts four reversible defaults while the Constraints and the source list three owner decisions.
- anchor: "the four defaults the owner may reverse (the `orgs/` read exception"
- anchor2: "Decisions taken as defaults (the owner may reverse them later): the T3 worker may read exactly"

#### L1.R1 (F8)

- claim: The path could be read as the project-root artifacts folder (never staged) and sits outside the four folders the Constraints allow.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R2 (F1)

- claim: The plan forbids editing `.claude/` and requires `make sync-dev`, whose target copies source files into `.claude/`, so the required sync violates the stated restriction.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`; fix any failure at its source in `src/superclaude/`, never by editing `.claude/`."

### L5

#### L5.R3 (F1)

- claim: The command-file instructions describe feature mode as selecting Feature, but also describe feature mode with area tests as selecting Test, so that input has conflicting issue-type outcomes.
- anchor: "the `--mode` row (line 41) to \"Picks the feature or bug template, the Feature or Bug issue type and the `enhancement` / `bug` label\""
- anchor2: "the `--type` row (line 42) to say the area of the change, which selects issue type Test for a feature in `tests`"

#### L5.R2 (F2)

- claim: The `--mode` row directs feature mode to Feature, contradicting the rule that feature mode with area `tests` must use Test.
- anchor: "the Feature or Bug issue type and the `enhancement` / `bug` label"
- anchor2: "the issue type rule (mode `bug` gives Bug; mode `feature` with area `tests` gives Test; every other feature gives Feature; Task is never chosen)"

#### L5.R2 (F3)

- claim: The plan does not carry forward the source requirement to include the `--type` area in the pushback comment as well as `flags.md`.
- anchor: "and is otherwise recorded in `flags.md`"

## Other findings

- L2 (MAJOR, open, single): No new test in Task 8 asserts text added by Task 3 (SKILL.md), so reverting Task 3 turns only Task 7's updated test red, not a new one.
- L3 (MAJOR, open, overlap): The live sentence 'Print this block last, in both modes' is not reworded, so it is false once create mode prints a third block.
- L4 (MINOR, open, single): Cited test and HOW-WE-WORK line numbers do not match the live files (545, 580, 695, 333) and the re-read rule covers only analysis line numbers.

## Reviser brief

Blocking finding ids: L1, L5.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
