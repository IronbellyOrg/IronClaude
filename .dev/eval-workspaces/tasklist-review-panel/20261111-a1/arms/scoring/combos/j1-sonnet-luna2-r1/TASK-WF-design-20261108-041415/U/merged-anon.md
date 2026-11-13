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
| L2 | open | no | single | MINOR | - | R1 |
| L3 | open | no | overlap | MAJOR | - | R1, R3 |
| L4 | open | no | single | MINOR | - | R1 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: The plan rewrites exact gh api lines that test_worker_contract.py keys word for word and never updates it, so every named check passes while the full suite fails in CI.
- anchor: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`"

#### L1.R1 (F2)

- claim: None of the six new tests asserts on text only Task 3 adds, so reverting Task 3 leaves them green and the criterion fails for Task 3.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"

#### L1.R1 (F3)

- claim: The constraint says two writes, while the tasks also apply the mode label and post the pushback comment.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L1.R1 (F4)

- claim: With no regex given, a plain orgs/ token match flags the required prose sentence as a forbidden path and fails test 2 against the plan's own text.
- anchor: "every `orgs/` path found by regex in the skill folder files and the `AGENTS` files"
- anchor2: "that no other `orgs/` path is allowed"

#### L1.R3 (F1)

- claim: The plan requires writing the owner manual outside its permitted edit locations, so an implementer cannot satisfy both requirements.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R2 (F1)

- claim: The plan both requires applying the mode label and limits issue writes to the issue type and Complexity field, so an implementer cannot satisfy both statements.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "Goal: `/sc:issue --create` sets the issue type (Feature, Bug or Test) and the org's Complexity issue field on the new issue, applies only the mode label (`bug` or `enhancement`)"

## Other findings

- L2 (MINOR, open, single): Task 10 does not name the design doc's gh api path rule or orchestrator write list, so they can stay stale and the acceptance lines still pass.
- L3 (MAJOR, open, overlap): The POST body file path is never named, so an implementer may write it outside .dev/issues/<N>/ where the skill's artifact rule expects it.
- L4 (MINOR, open, single): The live line 'Print this return contract last' becomes misleading with a third block, and Task 3 does not say to reword it.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
