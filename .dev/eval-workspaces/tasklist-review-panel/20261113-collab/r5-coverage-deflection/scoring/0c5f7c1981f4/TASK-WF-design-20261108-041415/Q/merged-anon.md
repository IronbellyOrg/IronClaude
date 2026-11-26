review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R2: report <redacted> block ok true
- R3: report <redacted> block ok true
- R1: report <redacted> block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | R1, R2, R3 |
| L2 | open | no | single | MINOR | - | R2 |
| L3 | open | no | single | MAJOR | - | R3 |

## Blocking findings

### L1

#### L1.R2 (F1)

- claim: The constraint allows exactly two writes to the created issue, but Wave 5 keeps the pushback comment, which is a third write.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "field POST and read-back; pushback comment; final output with every"

#### L1.R2 (F2)

- claim: No new test asserts on the SKILL.md text Task 3 adds, so reverting Task 3 leaves every new test green and the criterion cannot pass.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"
- anchor2: "plus two new rows (issue type not available or not applied, Complexity field not available or write failed)"

#### L1.R2 (F3)

- claim: tests/skills/test_worker_contract.py pins the exact skill and worker lines these tasks change and is never run, so the write-verb audit goes red unnoticed.
- anchor: "Run `make sync-dev`, then `make verify-sync`, `make lint` and"
- anchor2: "the ban on writes and on `-X` other than `GET` stays word for word"

#### L1.R2 (F4)

- claim: The regex is never specified, and the required prose token `orgs/` plus the spaced placeholder make a naive regex fail correct text.
- anchor: "every `orgs/` path found by regex in the skill folder files and the `AGENTS` files equals"
- anchor2: "no other `orgs/` path is allowed"

#### L1.R2 (F5)

- claim: Task 12 writes outside the four allowed folders, and the location is ambiguous between package and project-root artifacts.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`"
- anchor2: "write `./artifacts/owner-manual-check.md` in this package"

#### L1.R2 (F6)

- claim: The command's Will Not omits the Complexity-only clause that the skill's Will Not carries, so the two lists cannot agree.
- anchor: "to also say it creates no issue types or issue fields"
- anchor2: "never writes a field other than Complexity"

#### L1.R2 (F7)

- claim: The candidate does not restate what classification_missing holds or the new meaning of labels_applied; source 2.2 resolves it.
- anchor: "add a third YAML block with exactly the keys"

#### L1.R2 (F8)

- claim: The retained bug and enhancement label lines use --repo <owner/repo>, not <R>, and Task 1's check covers only gh issue lines.
- anchor: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`"

#### L1.R3 (F1)

- claim: The plan requires a pushback comment while also limiting writes beyond issue creation to exactly the issue type and Complexity field, so both requirements cannot be met.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "pushback comment"

#### L1.R1 (F1)

- claim: Task 12 requires writing an artifact outside the plan's allowed edit paths, so the implementer must either violate the constraint or fail the required deliverable.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."

#### L1.R1 (F2)

- claim: The planned mode-row wording says feature selects Feature while the planned area-row wording and source rule require a feature in the tests area to select Test.
- anchor: "the `--mode` row (line 41) to \"Picks the feature or bug template, the Feature or Bug issue type and the `enhancement` / `bug` label\""
- anchor2: "the `--type` row (line 42) to say the area of the change, which selects issue type Test for a feature in `tests`"

#### L1.R1 (F3)

- claim: The test requirement does not distinguish the orchestrator's POST write from worker text, despite the stated read-only worker boundary.
- anchor: "Third, the skill folder and the agents contain `-X POST` together with `issue-field-values` and no `-X PUT`."

## Other findings

- L2 (MINOR, open, single): Lines 233 and 277 are not inventory tests in the live file.
- L3 (MAJOR, open, single): When the Complexity field exists but lacks the wanted option, the plan does not explicitly require emitting the `option not found` line and continuing.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
