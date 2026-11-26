review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R3: report <redacted>, block ok true
- R1: report <redacted>, block ok true
- R2: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | R1, R2, R3 |
| L2 | open | no | single | MAJOR | - | R3 |
| L3 | open | no | single | MINOR | - | R3 |
| L4 | open | no | single | MINOR | - | R1 |

## Blocking findings

### L1

#### L1.R3 (F1)

- claim: Constraint 23 allows exactly two writes to a created issue, but Task 2 Wave 5 also posts the pushback comment, a third write.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L1.R3 (F2)

- claim: The seven tests Task 8 lists do not assert the flags row, the create-review wording or the Wave 1 lookup text, so reverting them leaves every new test green.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"
- anchor2: "In `flags-decision.md` add an `Issue type` row"

#### L1.R3 (F3)

- claim: The live checkout already has the target text and some of the tests, and the plan does not say what to do when they are present.
- anchor: "Remove the 11 `type: ...` labels, the 3 `complexity: ...` labels and their `gh label create` lines"
- anchor2: "Write one test per rule, each failing when the behaviour breaks"

#### L1.R3 (F4)

- claim: The artifact path is ambiguous between the package folder and project-root artifacts, and the second is outside the allowed edit trees.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`"

#### L1.R3 (F6)

- claim: Task 8 requires exact output strings in create.md, but Task 2 never requires them.
- anchor: "the final-output lines in the order of specification 2.1"
- anchor2: "Fourth, `create.md` and `labels.md` carry the three exact line formats"

#### L1.R3 (F7)

- claim: The owner check omits the API-version risk that turns a 404 into a silent not-set line.
- anchor: "It also records the three UNVERIFIED points from the source section 3.4"

#### L1.R3 (F8)

- claim: Keeping the two maintainer lines leaves --repo <owner/repo> in place, which a literal reading of --repo <R> rejects.
- anchor: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries"
- anchor2: "keep only the `bug` and `enhancement` lines in the maintainer block"

#### L1.R3 (F9)

- claim: The rule reads as forbidding the sync target that writes into .claude/.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`"
- anchor2: "run `make sync-dev` after the `src/superclaude/` edits"

#### L1.R3 (F10)

- claim: Line references differ from the source and from the live file; the plan does say to re-read them first.
- anchor: "Create section (lines 40 to 50)"
- anchor2: "test_skill_will_and_will_not_match_the_command_file, line 527"

#### L1.R3 (F11)

- claim: The constraint lists three defaults and Task 12 lists four.
- anchor: "the four defaults the owner may reverse"
- anchor2: "Decisions taken as defaults (the owner may reverse them later)"

#### L1.R3 (F12)

- claim: The rename is defined only in the source file, not in the candidate.
- anchor: "`gh issue create` and the rename"

#### L1.R1 (F1)

- claim: Verbatim-kept maintainer lines use <owner/repo>, not the required <R> placeholder.
- anchor: "keep only the `bug` and `enhancement` lines in the maintainer block."
- anchor2: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`."

#### L1.R1 (F2)

- claim: Task 12 artifact writes fall outside the stated edit-only directory list.
- anchor: "write `./artifacts/owner-manual-check.md` in this package"
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`"

#### L1.R2 (F1)

- claim: Following both statements is impossible: running the required sync writes into `.claude/`, while avoiding those writes skips the required sync.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`;"

#### L1.R2 (F2)

- claim: The plan requires artifact files without stating that the package artifacts directory is within the allowed edit scope.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

## Other findings

- L2 (MAJOR, open, single): The command's Will Not list and the skill's Will Not list will not agree on the field-write clause.
- L3 (MINOR, open, single): The leave-alone branch skips the repo rule to re-run the level-table copy; the live CLAUDE.md has no sc:issue row, so this is probably a no-op.
- L4 (MINOR, open, single): Historical gh api paths could make the universal path acceptance read ambiguous.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
