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
| L1 | open | yes | overlap | MAJOR | - | R1, R3 |
| L2 | open | no | single | MINOR | - | R1 |
| L3 | open | no | single | MINOR | - | R1 |
| L4 | open | yes | single | MAJOR | - | R2 |
| L5 | open | no | single | MAJOR | - | R2 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: Editing the pinned gh api lines and adding new gh api lines breaks test_every_write_verb_hit_is_classified and test_classification_table_has_no_stale_entries in test_worker_contract.py, and no task updates or runs that file.
- anchor: "then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`"
- anchor2: "and adds the single exception `orgs/<owner of R>/issue-fields` for this lookup only"

#### L1.R1 (F2)

- claim: The constraint says two writes besides the issue, but the tasks also write the mode label and the pushback comment.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "field POST and read-back; pushback comment; final output"

#### L1.R1 (F5)

- claim: ./artifacts/ read from the repo root is the never-staged project-root folder and is outside the listed edit paths; the package artifacts path is not named.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package"

#### L1.R3 (F1)

- claim: Following the two-write limit omits the required mode label and conflicts with the required pushback comment when one is due.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "Goal: `/sc:issue --create` sets the issue type (Feature, Bug or Test) and the org's Complexity issue field on the new issue, applies only the mode label (`bug` or `enhancement`),"

#### L1.R3 (F2)

- claim: The edit-scope constraint forbids the artifacts directory where Task 12 requires both the owner check and saved check log.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

### L4

#### L4.R2 (F1)

- claim: The plan both forbids writing the required owner-check artifact under `./artifacts/` and requires that artifact to exist.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/."

## Other findings

- L2 (MINOR, open, single): Named line numbers do not match the live files (test_st10 at 545-575, Will test at 580, self-check model at 695, HOW-WE-WORK row at 333), though each task also names the function or phrase.
- L3 (MINOR, open, single): A naive orgs/ regex would flag the bare `orgs/` in the required 'no other orgs/ path' sentence, so the scanner must require a path segment.
- L5 (MAJOR, open, single): The type read-back is not explicitly limited to cases where `--type` was passed, which may cause duplicate missing-type classifications.

## Reviser brief

Blocking finding ids: L1, L4.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report <redacted> byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
