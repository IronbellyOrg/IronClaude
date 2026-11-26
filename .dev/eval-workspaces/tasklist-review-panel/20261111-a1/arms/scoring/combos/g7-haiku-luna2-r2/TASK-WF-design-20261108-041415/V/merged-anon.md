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
| L1 | open | yes | overlap | MAJOR | - | R1, R2, R3 |
| L2 | open | yes | single | MAJOR | - | R2 |
| L3 | open | yes | single | MAJOR | - | R2 |
| L4 | open | no | single | MINOR | - | R2 |
| L5 | open | no | single | MINOR | - | R2 |
| L6 | open | no | single | MINOR | - | R1 |

## Blocking findings

### L1

#### L1.R2 (F1)

- claim: The pushback comment is a third write to the created issue, so the text either breaks Constraint 23 or silently drops the comment that Wave 5 keeps as today.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L1.R2 (F4)

- claim: Keeping the maintainer lines as they stand at HEAD (labels.md lines 63 and 64, --repo <owner/repo>) leaves gh label lines without --repo <R>, which Constraint 21 forbids.
- anchor: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`."
- anchor2: "keep only the `bug` and `enhancement` lines in the maintainer block"

#### L1.R2 (F5)

- claim: The base commit is absent from the clone and most of the target state is already in HEAD 8c93e1d, and the candidate gives no rule for a live file that already carries the change.
- anchor: "Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3` and must be re-read in the live file before each edit."
- anchor2: "change `len(blocks) == 2` to 3"

#### L1.R2 (F6)

- claim: The read-back does not say which property to compare, so comparing the numeric value with the option name reports a false not-applied line on a correct write.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L1.R2 (F7)

- claim: No gh minimum version is stated, and --type exists in gh 2.103.3 (checked locally), so an older gh stops every create in a repo with listed types with E-CREATE-FAILED.
- anchor: "`--type` when listed; `gh issue create` and the rename"

#### L1.R2 (F8)

- claim: The text does not say whether the POST sends the org's option spelling or the wanted spelling, and GitHub requires the value to match an existing option.
- anchor: "matched to the field's option names without case sensitivity"

#### L1.R2 (F9)

- claim: The path may mean the project-root artifacts folder, which is outside the allowed edit paths and which CLAUDE.md says is never staged.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."

#### L1.R2 (F10)

- claim: Task 12 lists four defaults while Constraint 26 lists three, so the owner file may carry a count that does not match.
- anchor: "the four defaults the owner may reverse"
- anchor2: "Decisions taken as defaults (the owner may reverse them later)"

#### L1.R1 (F1)

- claim: The plan requires a sync that writes under `.claude/` while expressly forbidding that write.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`"

#### L1.R1 (F2)

- claim: The required manual-check artifact is outside the plan's permitted edit locations.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R3 (F1)

- claim: The plan both forbids edits under `.claude/` and requires a sync command that writes files there.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`; fix any failure at its source in `src/superclaude/`."

#### L1.R3 (F2)

- claim: Task 12 requires artifacts outside the plan’s explicitly permitted edit locations.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

### L2

#### L2.R2 (F2)

- claim: For --mode feature with --type tests the --mode row sets Feature while the --type row and Q7 set Test.
- anchor: "Picks the feature or bug template, the Feature or Bug issue type and the `enhancement` / `bug` label"
- anchor2: "which selects issue type Test for a feature in `tests`"

### L3

#### L3.R2 (F3)

- claim: Reverting Task 3 (SKILL.md) turns no new Task 8 test red, so the acceptance line cannot pass for Task 3.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red: each new test asserts on the text that task adds."
- anchor2: "Third, the skill folder and the agents contain `-X POST` together with `issue-field-values` and no `-X PUT`."

## Other findings

- L4 (MINOR, open, single): The cited range is not the range in source 3.1 (lines 42 to 44); the re-read rule covers it, so this is a note only.
- L5 (MINOR, open, single): source.md was modified after the candidate, so the section references may point at decisions that changed after the candidate was written.
- L6 (MINOR, open, single): The plan does not define how a failed type or field read-back command is reported.

## Reviser brief

Blocking finding ids: L1, L2, L3.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
