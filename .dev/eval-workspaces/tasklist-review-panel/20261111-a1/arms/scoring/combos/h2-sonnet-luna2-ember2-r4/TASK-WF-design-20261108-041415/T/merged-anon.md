review: 1 of 3
# Merged review 1 (coordinator script; panel of 5 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R1: report <redacted>, block ok true
- R4: report <redacted>, block ok true
- R5: report <redacted>, block ok true
- R2: report <redacted>, block ok true
- R3: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | R1, R2, R3, R4, R5 |
| L2 | open | no | single | MAJOR | - | R1 |
| L3 | open | no | single | MINOR | - | R1 |
| L4 | open | no | overlap | MAJOR | - | R3, R4, R5 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: Edited gh api lines break the pinned inventory in tests/skills/test_worker_contract.py, which no task updates and Task 12 never runs.
- anchor: "`make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`; fix any failure at its source"

#### L1.R1 (F2)

- claim: The quoted gh issue create line has no --repo <R>, so copying it literally fails the fork-safety scan.
- anchor: "add the field POST and `gh issue create ... --type <name>` to the orchestrator's write list"
- anchor2: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`"

#### L1.R1 (F4)

- claim: No listed new test reads text that only SKILL.md adds, so reverting Task 3 turns no new test red unless an unlisted test is added.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"

#### L1.R1 (F5)

- claim: An unspecified regex can flag the bare `orgs/` in the required prose sentence.
- anchor: "every `orgs/` path found by regex in the skill folder files and the `AGENTS` files equals"
- anchor2: "states the single `orgs/<owner>/issue-fields` exception and that no other `orgs/` path is allowed"

#### L1.R1 (F6)

- claim: The pushback comment is a third write to the created issue, so the constraint sentence is false.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "field POST and read-back; pushback comment; final output with every"

#### L1.R1 (F8)

- claim: The source change that labels_applied and labels_missing now describe the mode label only is not carried into Task 3.
- anchor: "keep the first block key for key and the claim block unchanged"

#### L1.R4 (F1)

- claim: Task 12 requires artifact writes outside the plan's allowed edit scope, so its required outputs cannot satisfy the stated constraints.
- anchor: "- Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R4 (F2)

- claim: The required sync writes generated files under `.claude/`, which the plan separately forbids editing.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`;"
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`"

#### L1.R5 (F1)

- claim: The constraint's exact count excludes the mode label required by the goal, allowing an implementation that does not apply that label.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type"
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

#### L1.R5 (F2)

- claim: Task 12 requires package artifacts outside the permitted edit locations, so its artifact acceptance criteria cannot be met while obeying the scope constraint.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R2 (F1)

- claim: Task 12 requires writing outside the only edit locations the Constraints allow: an artifacts file at ./artifacts/.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R2 (F2)

- claim: The live tree already contains the issue-type tests and target text, so the plan baseline is stale and Task 8's count check has no current baseline.
- anchor: "Add tests to `tests/skills/test_issue_protocol.py`, using the file's existing helpers"

#### L1.R2 (F3)

- claim: Named line numbers have drifted from the live files even with the re-read rule.
- anchor: "Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3` and must be re-read in the live file before each edit."

#### L1.R3 (F1)

- claim: Reverting Task 3 alone may leave new tests green under the allowed-only-in reading, so the revert AC may not bite.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red: each new test asserts on the text that task adds."

#### L1.R3 (F2)

- claim: The allowed orgs/<owner>/issue-fields alternative may accept orgs/other, contradicting the self-check expectation.
- anchor: "`orgs/other/issue-fields` and expects it to be reported."

#### L1.R3 (F3)

- claim: Literal edit-only scope conflicts with the ./artifacts/ writes Task 12 requires.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R3 (F5)

- claim: Two spellings of the same orgs exception are used without a canonical form.
- anchor: "`create.md` states the single `orgs/<owner>/issue-fields` exception and that no other `orgs/` path is allowed."

## Other findings

- L2 (MAJOR, open, single): The design doc keeps `gh api user -q .login` at line 157, so the check cannot pass literally.
- L3 (MINOR, open, single): The named selector does not run the options-table test in tests/commands/test_issue_command.py that pins the --type values.
- L4 (MAJOR, open, overlap): The plan does not specify matching the returned field ID and option name, so an implementation that compares the numeric option ID to the text value can falsely report the field was not set.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
