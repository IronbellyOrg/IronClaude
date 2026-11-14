review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R1: report <redacted> block ok true
- R3: report <redacted> block ok true
- R2: report <redacted> block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | R1, R2, R3 |
| L2 | open | no | overlap | MAJOR | - | R1, R3 |
| L3 | open | no | single | MINOR | - | R1 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: tests/skills/test_worker_contract.py pins the exact text of the edited gh api lines and classifies every gh api hit, so the plan's edits and new gh api lines turn it red and no task updates or runs it.
- anchor: "the \"Read-only GitHub access\" bullet (line 27) keeps"
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`"

#### L1.R1 (F2)

- claim: Task 3 names a gh issue create span without --repo, which the fork-safety scan rejects if copied as written.
- anchor: "add the field POST and `gh issue create ... --type <name>` to the orchestrator's write list"
- anchor2: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`"

#### L1.R1 (F3)

- claim: The constraint says two writes to the created issue, but Wave 5 also applies the mode label and posts the pushback comment.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L1.R1 (F6)

- claim: Source 2.2 says labels_applied and labels_missing now describe the mode label only, and Task 3 does not carry that change.
- anchor: "keep the first block key for key and the claim block unchanged"

#### L1.R3 (F1)

- claim: The plan both limits writes to the created issue to the type and Complexity field and requires posting a pushback comment to that issue.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "Wave 5 (lines 61 to 69): replace the label step with the sequence of specification 2.1 (mode label only; `--type` when listed; `gh issue create` and the rename; type read-back; field POST and read-bac"

#### L1.R3 (F2)

- claim: The plan forbids edits outside the listed directories but requires creating artifact files under `./artifacts/`.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R2 (F1)

- claim: The goal requires a mode-label write while the constraint limits issue writes to the issue type and Complexity field, so both cannot be satisfied.
- anchor: "The skill never creates a label, an issue type or an issue field. It writes exactly two things to a created issue besides the issue itself:"
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

#### L1.R2 (F2)

- claim: Task 12 requires creating an artifact outside the permitted edit paths, so the plan cannot both obey the constraint and pass its artifact-existence criterion.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

## Other findings

- L2 (MAJOR, open, overlap): None of the six listed new tests reads SKILL.md content added by Task 3, so reverting Task 3 leaves every new test green unless test 2 is written as exact file-set equality.
- L3 (MINOR, open, single): The design doc holds `gh api user -q .login` at line 157 in the unchanged claim flow, so the criterion is false as written.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
