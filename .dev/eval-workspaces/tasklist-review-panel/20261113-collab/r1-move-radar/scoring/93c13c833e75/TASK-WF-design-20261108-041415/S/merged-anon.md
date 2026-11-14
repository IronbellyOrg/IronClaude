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
| L1 | open | no | single | MAJOR | - | R1 |
| L2 | open | no | single | MAJOR | - | R1 |
| L3 | open | no | single | MINOR | - | R1 |
| L4 | open | yes | overlap | MAJOR | - | R2, R3 |

## Blocking findings

### L4

#### L4.R3 (F1)

- claim: The plan both forbids changes under `.claude/` and requires a sync that updates those generated copies, so following either instruction violates the other.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`"

#### L4.R3 (F2)

- claim: Task 12 requires an artifact outside every location allowed by the plan's edit-scope constraint.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L4.R3 (F3)

- claim: Applying the required mode label means the plan writes three classifications to the issue, not the exactly two stated in the constraint.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

#### L4.R2 (F1)

- claim: The plan limits writes on a created issue to the type and field while also requiring a mode label and a pushback comment.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

#### L4.R2 (F2)

- claim: The design document's existing claim flow contains `gh api user`, so this acceptance criterion cannot pass while claim text stays unchanged.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "`--claim` behaviour and text stay unchanged, including its two-block part of the return contract."

#### L4.R2 (F3)

- claim: The required sync modifies generated files under `.claude/`, conflicting with the blanket prohibition on editing those files.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`"

## Other findings

- L1 (MAJOR, open, single): Task 8 acceptance cannot pass as written because no described new test asserts SKILL.md content for Task 3.
- L2 (MAJOR, open, single): No rule states which spelling is sent when a case-insensitive match differs from the API spelling.
- L3 (MINOR, open, single): Line 329 is stale; live /sc:issue row is at line 333 but the re-read constraint covers it.

## Reviser brief

Blocking finding ids: L4.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
