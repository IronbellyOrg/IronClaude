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
| L2 | open | no | single | MAJOR | - | R1 |
| L3 | open | no | single | MAJOR | - | R1 |
| L4 | open | no | single | MINOR | - | R1 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: The manual-check write sits outside the stated edit-only trees without a stated exception.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R3 (F1)

- claim: An implementer cannot satisfy both the edit-scope constraint and the required artifact path.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R3 (F2)

- claim: The plan requires two classification writes while also requiring that an unavailable type or field be skipped and reported.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "`--type` only when the type is listed under `### Repo issue types`"

#### L1.R3 (F3)

- claim: The candidate omits the required comparison of the read-back's single-select option name, allowing incorrect verification against the numeric option ID.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L1.R3 (F4)

- claim: The relative artifact path does not specify its base directory.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R2 (F1)

- claim: The plan simultaneously forbids edits under `.claude/` and requires a sync command that copies source files into `.claude/`.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`; fix any failure at its source in `src/superclaude/`, never by editing `.claude/`."

#### L1.R2 (F2)

- claim: The required manual-check artifact is outside the plan's permitted edit locations, so producing it violates the scope constraint.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R2 (F3)

- claim: The plan omits that single-select read-back returns an option ID and must be checked through `single_select_option.name`, which could cause an implementation to misreport a correctly set field.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

## Other findings

- L2 (MAJOR, open, single): The required bare orgs prose needs a stated scanner exception or a naive test fails on required text.
- L3 (MAJOR, open, single): Agreement is required without stating the matching SKILL.md Will change.
- L4 (MINOR, open, single): The scout data is named but the line layout needed for Wave 5 parsing is not fixed.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
