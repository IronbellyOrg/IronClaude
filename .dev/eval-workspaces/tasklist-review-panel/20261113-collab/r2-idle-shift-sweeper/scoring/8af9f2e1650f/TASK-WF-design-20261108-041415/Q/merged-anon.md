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
| L2 | open | yes | overlap | MAJOR | - | R1, R3 |
| L3 | open | no | single | MAJOR | - | R1 |
| L4 | open | no | single | MINOR | - | R1 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: Constraint 23 allows two writes to the created issue, but Task 2 keeps the pushback comment as a third write.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "field POST and read-back; pushback comment; final output with every `not applied` and `not set` line"

#### L1.R1 (F4)

- claim: A plain orgs/ regex matches the required prose and fails test 2, and the regex is not fixed.
- anchor: "states the single `orgs/<owner>/issue-fields` exception and that no other `orgs/` path is allowed"

#### L1.R1 (F5)

- claim: E-POST-FAILED is the pushback-comment STOP today, but its name reads like the field POST, which must not stop the run.
- anchor: "`E-CREATE-FAILED` and `E-POST-FAILED` keep their current meaning."
- anchor2: "a failed type or field never stops the run after the issue exists"

#### L1.R1 (F6)

- claim: The artifact path falls outside the four allowed edit roots and is ambiguous about where it lives.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."

#### L1.R1 (F8)

- claim: Task 12 lists four defaults where Constraint 26 lists three.
- anchor: "and the four defaults the owner may reverse"

#### L1.R1 (F9)

- claim: The rule forbids editing .claude/ while Task 12 requires make sync-dev, which rewrites it; the sync should be named as the allowed write.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`"

#### L1.R3 (F1)

- claim: The plan both forbids editing generated `.claude/` files and requires `make sync-dev` to update them.
- anchor: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`;"
- anchor2: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."

#### L1.R3 (F2)

- claim: The required manual-check artifact is outside the stated allowed edit paths, so the plan cannot satisfy both its scope constraint and its artifact acceptance criterion.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."

#### L1.R2 (F1)

- claim: Task 12 requires an artifact outside the candidate's permitted edit paths, so its acceptance criterion cannot be met while obeying the constraint.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."

#### L1.R2 (F2)

- claim: The goal requires applying a mode label in addition to the issue type and Complexity field, contradicting the constraint that exactly two things are written to the issue.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

### L2

#### L2.R1 (F2)

- claim: The seven listed tests assert nothing on the Task 3 error rows or the Task 4 flags row and wording, so reverting those keeps every new test green.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"

#### L2.R1 (F3)

- claim: The orgs scanner is never defined, and the cited line 642 is not a fork-safety test.
- anchor: "feeds the `orgs/` scanner a text with `orgs/other/issue-fields` and expects it to be reported"
- anchor2: "in the style of `test_fork_safety_scan_fails_on_a_ref_without_repo` (line 642)"

#### L2.R3 (F3)

- claim: The plan requires text-based tests and a happy-path manual check but no runnable regression check for non-fatal type or field write/read-back failures.
- anchor: "Write one test per rule, each failing when the behaviour breaks."

## Other findings

- L3 (MAJOR, open, single): If the phrase is absent, the implementer leaves the CLAUDE.md copy out of sync, though the project rule says tests check both files.
- L4 (MINOR, open, single): The same return-contract section gets both 'claim mode prints none of them' and 'create mode prints none of them'; the wording clash is minor.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report <redacted> byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
