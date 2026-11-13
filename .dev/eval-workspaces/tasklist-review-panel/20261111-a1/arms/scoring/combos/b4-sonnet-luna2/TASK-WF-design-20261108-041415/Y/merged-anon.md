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
| L1 | open | yes | overlap | MAJOR | - | R1, R2, R3 |
| L2 | open | no | single | MAJOR | - | R1 |
| L3 | open | no | single | MAJOR | 2.1 | R1 |
| L4 | open | no | single | MINOR | - | R1 |
| L5 | open | no | overlap | MINOR | - | R2, R3 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: No task updates the exact-line gh api allowlist in test_worker_contract.py and Task 12 never runs it, so the rewritten and new gh api lines leave that test file red.
- anchor: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`"

#### L1.R1 (F2)

- claim: The design doc holds `gh api user -q .login` in the unchanged claim section, so the Task 10 acceptance line cannot pass as written.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`"

#### L1.R1 (F5)

- claim: The constraint says two writes besides the issue, but the plan also posts the pushback comment and applies the mode label.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "field POST and read-back; pushback comment; final output with every `not applied` and `not set` line"

#### L1.R1 (F6)

- claim: Task 12 writes files outside the four directories the constraints allow editing, and the artifacts path is ambiguous with the project-root artifacts folder.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."

#### L1.R3 (F1)

- claim: Following the two-write constraint can omit the required mode label, contradicting the goal.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

#### L1.R2 (F1)

- claim: Constraint 23 limits issue writes to two items, contradicting the required mode-label write.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "sets the issue type (Feature, Bug or Test) and the org's Complexity issue field on the new issue, applies only the mode label (`bug` or `enhancement`)"

#### L1.R2 (F2)

- claim: Task 12 requires creating an artifact outside the explicitly allowed edit paths.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

## Other findings

- L2 (MAJOR, open, single): None of the six listed new tests asserts on text only Task 3 adds to SKILL.md, so reverting Task 3 turns no new test red.
- L3 (MAJOR, open, single): The plan never says how to match the read-back row for a single-select field, so a literal name-to-value compare can report a false not-applied line after every successful write.
- L4 (MINOR, open, single): The quoted write-list entry omits --repo <R>, which the fork-safety scan requires on every gh issue line.
- L5 (MINOR, open, overlap): The plan does not specify how to compare the returned single-select option with the requested Complexity option.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
