review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R1: report <redacted>, block ok true
- R2: report <redacted>, block ok true
- R3: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | R1, R2, R3 |
| L2 | open | yes | single | CRITICAL | 2.3 | R2 |
| L3 | open | no | single | MINOR | - | R2 |
| L4 | open | no | single | MINOR | - | R2 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: The required sync writes generated files under .claude even though the plan forbids editing those paths.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."

#### L1.R1 (F2)

- claim: The required package artifacts cannot be written within the plan's permitted edit locations.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R1 (F3)

- claim: The required pushback comment is an additional write beyond the two writes the plan permits.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "field POST and read-back; pushback comment; final output with every `not applied` and `not set` line"

#### L1.R1 (F4)

- claim: The prescribed mode description can lead readers to expect Feature for a feature in the tests area, although the area rule selects Test.
- anchor: "Picks the feature or bug template, the Feature or Bug issue type and the `enhancement` / `bug` label"
- anchor2: "mode `feature` with area `tests` gives Test"

#### L1.R2 (F2)

- claim: Exactly-two counting is ambiguous against the required mode label and pushback comment.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "the table of the only two labels the skill applies (`bug` for mode bug, `enhancement` for mode feature)"

#### L1.R2 (F3)

- claim: Task 12 writes outside the stated edit-only scope and the base directory is not pinned.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "write `./artifacts/owner-manual-check.md` in this package."

#### L1.R2 (F4)

- claim: Kept maintainer lines use --repo <owner/repo> instead of literal --repo <R>.
- anchor: "No file may contain a brace placeholder for owner and repo; use `<owner>` and `<R>`."
- anchor2: "keep only the `bug` and `enhancement` lines in the maintainer block."

#### L1.R2 (F5)

- claim: The plan never states comparing single_select_option.name instead of the numeric value.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L1.R3 (F1)

- claim: The plan both forbids edits to the required artifact location and requires creating an artifact there, so its constraints and acceptance criteria cannot both be met.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

### L2

#### L2.R2 (F1)

- claim: Task 10's universal gh api check cannot pass while the claim lookup keeps gh api user, which Task 2 allows.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`"

## Other findings

- L3 (MINOR, open, single): Scout heading order is listed differently in Tasks 4 and 2.
- L4 (MINOR, open, single): Two orgs placeholder spellings are allowed without a rule for which file uses which.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
