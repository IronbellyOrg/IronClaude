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
| L2 | open | no | single | MAJOR | 2.1 | R1 |
| L3 | open | no | single | MAJOR | 2.1, 3.4 | R1 |
| L4 | open | no | single | MINOR | 2.3 | R1 |
| L5 | open | no | single | MINOR | - | R1 |
| L6 | open | no | single | MINOR | - | R1 |
| L7 | open | no | single | MINOR | 3.4 | R1 |
| L8 | open | yes | overlap | MAJOR | - | R2, R3 |

## Blocking findings

### L8

#### L8.R3 (F1)

- claim: The plan both limits writes beyond issue creation to the type and field and requires a mode label plus a possible pushback comment.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

#### L8.R3 (F2)

- claim: The manual-check artifact location may violate the plan's edit-scope restriction.
- anchor: "- Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L8.R2 (F1)

- claim: The plan both prohibits edits outside its listed directories and requires creating two artifacts under `./artifacts/`.
- anchor: "- Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L8.R2 (F2)

- claim: The plan prohibits edits under `.claude/` while requiring a sync that updates generated copies there.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."

## Other findings

- L1 (MAJOR, open, single): Task 6 asks the --type row to say it no longer maps to a `type: <value>` label while its own criterion forbids any `type: <value>` label wording, so a literal reading fails the criterion.
- L2 (MAJOR, open, single): The constraint says two writes besides the issue, but the plan also keeps the mode label and the pushback comment, so the sentence is false as written.
- L3 (MAJOR, open, single): No rule covers a gh without the --type flag, so gh issue create fails with an unknown flag and the whole create stops with E-CREATE-FAILED.
- L4 (MINOR, open, single): The literal write-list item has no --repo <R>, which the existing fork-safety scan would reject if copied as written.
- L5 (MINOR, open, single): The live HOW-WE-WORK row is line 333 and the named test lines after 277 are about 53 lines off, so the line numbers cannot be used as written.
- L6 (MINOR, open, single): A loose orgs/ regex matches the bare 'orgs/' in the required 'no other orgs/ path' sentence and fails the equality test.
- L7 (MINOR, open, single): Task 12 counts four reversible defaults while the constraints and source section 3.4 list three.

## Reviser brief

Blocking finding ids: L8.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
