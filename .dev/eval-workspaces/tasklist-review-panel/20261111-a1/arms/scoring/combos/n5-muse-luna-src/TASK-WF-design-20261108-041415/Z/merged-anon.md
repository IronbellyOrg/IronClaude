review: 1 of 3
# Merged review 1 (coordinator script; panel of 2 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R1: report <redacted>, block ok true
- R2: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | R1, R2 |
| L2 | open | no | single | MINOR | - | R1 |
| L3 | open | no | single | MINOR | - | R1 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: Task 10 acceptance cannot pass while the unchanged claim flow uses gh api user, so the implementer must fail the check or change claim text.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "`--claim` behaviour and text stay unchanged, including its two-block part of the return contract."

#### L1.R1 (F2)

- claim: The candidate names the Complexity read-back call but never states that the match must use issue_field_id and single_select_option.name rather than the numeric value.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L1.R1 (F3)

- claim: Keeping the maintainer label lines as written can keep --repo <owner/repo>, which conflicts with a literal reading of the --repo <R> constraint.
- anchor: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`."
- anchor2: "keep only the `bug` and `enhancement` lines in the maintainer block."

#### L1.R1 (F4)

- claim: Task 12 artifacts are outside the stated edit roots if ./artifacts is read from the repo root instead of the task package folder.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R2 (F1)

- claim: An implementer who follows the stated text as written builds a create flow that applies only the issue type and Complexity field, and that is wrong because the goal also requires applying the mode label.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

#### L1.R2 (F2)

- claim: An implementer who follows the stated text as written either writes the required artifact outside the permitted edit scope or skips a required deliverable.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."

#### L1.R2 (F3)

- claim: An implementer who follows the stated text as written either runs the required sync and changes files under `.claude/`, or skips the required sync.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."

## Other findings

- L2 (MINOR, open, single): The orgs scanner does not state that a bare orgs/ prose token is not a path, so a naive regex can flag required prose.
- L3 (MINOR, open, single): Task 11 calls a possible CLAUDE.md hit the level table copy, but the sc:issue phrase is not part of that copied level-table block.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
