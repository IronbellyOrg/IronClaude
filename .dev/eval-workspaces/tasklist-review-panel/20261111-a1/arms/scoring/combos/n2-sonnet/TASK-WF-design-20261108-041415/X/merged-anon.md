review: 1 of 3
# Merged review 1 (coordinator script; panel of 4 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R2: report <redacted>, block ok true
- R3: report <redacted>, block ok true
- R4: report <redacted>, block ok true
- R1: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | R1, R2, R3, R4 |
| L2 | open | no | overlap | MAJOR | - | R2, R3 |
| L3 | open | yes | overlap | MAJOR | - | R1, R2, R3 |
| L4 | open | yes | single | MAJOR | - | R3 |
| L5 | open | no | overlap | MAJOR | - | R3, R4 |
| L6 | open | no | single | MAJOR | - | R3 |
| L7 | open | no | single | MINOR | - | R3 |

## Blocking findings

### L1

#### L1.R2 (F1)

- claim: The design document keeps the authorised gh api user claim lookup outside Task 10's edit scope, so its gh api acceptance criterion cannot pass without an unauthorised change.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "Replace the statements that labels come from a fixed set or that `type:` and `complexity:` labels are applied, at the places listed by grep for \"label\""

#### L1.R2 (F2)

- claim: Task 12 requires artifacts files outside every directory the edit-only constraint permits, so obeying either text fails the other.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R2 (F3)

- claim: Read literally, the exactly-two-writes sentence forbids the required mode label and pushback comment; the intended classification-only reading must be guessed.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

#### L1.R3 (F1)

- claim: Constraint 23 allows exactly two writes to a created issue, but Task 2's Wave 5 posts a pushback comment on that issue, a third write.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L1.R3 (F7)

- claim: HEAD 8c93e1d already holds the Wave 5 sequence, the three-block test and the new labels.md text, and the Will/Will Not test is at line 586, not 527, so an implementer may edit text that is already done.
- anchor: "replace the label step with the sequence of specification 2.1"
- anchor2: "Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3`"

#### L1.R3 (F8)

- claim: The artifacts path does not say whether it is the package folder or the project-root artifacts folder, which CLAUDE.md says is never staged.
- anchor: "write `./artifacts/owner-manual-check.md` in this package"

#### L1.R4 (F1)

- claim: Exactly two writes (type and Complexity) cannot be reconciled with the required mode label or the pushback comment.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

#### L1.R4 (F2)

- claim: Task 10's path check passes only by dropping `gh api user`, which claim lookup still runs and Task 2 still allows.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`, with one stated exception"

#### L1.R4 (F4)

- claim: The Task 2 body and its acceptance criterion name two different `orgs/` path strings.
- anchor: "`create.md` states the single `orgs/<owner>/issue-fields` exception"
- anchor2: "read-only GET of `orgs/<owner of R>/issue-fields`"

#### L1.R1 (F1)

- claim: The 'exactly two writes' constraint contradicts Wave 5, which also posts a pushback comment, and the mode label is a third write.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L1.R1 (F3)

- claim: The design doc also contains `gh api user -q .login`, so the criterion read literally cannot pass; the intended reading allows `user`.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."

#### L1.R1 (F4)

- claim: The edit-location constraint omits the package artifacts folder that Task 12 writes to.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "write `./artifacts/owner-manual-check.md` in this package"

### L3

#### L3.R2 (F5)

- claim: The POST test wording can be read as requiring every skill and agent file to contain a POST rather than the three files that carry the field write.
- anchor: "the skill folder and the agents contain `-X POST` together with `issue-field-values` and no `-X PUT`"

#### L3.R3 (F2)

- claim: Test 2 only restricts where orgs paths may appear, and no listed test reads Task 3's error rows, call rules or Will Not list, so reverting Task 3 leaves every new test green.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"
- anchor2: "and appears only in `create.md`, `SKILL.md` and `issue-worker-t3.md`"

#### L3.R1 (F2)

- claim: No new test in Task 8 asserts text only Task 3 adds, so the revert check cannot hold for Task 3 unless the per-file reading of the POST test is chosen.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"

### L4

#### L4.R3 (F3)

- claim: The command Will Not list gets no field-restriction sentence, so test_command_and_skill_agree_on_the_new_create_boundaries (tests/skills/test_issue_protocol.py:851) fails, and Task 6's own -k command run selects it.
- anchor: "the Will Not line (line 93) to also say it creates no issue types or issue fields"
- anchor2: "uv run pytest tests/skills/test_issue_protocol.py -k \"command\" -v"

## Other findings

- L2 (MAJOR, open, overlap): The candidate states the third block's keys but not its value rules, which are delegated to a specification file absent from the candidate directory.
- L5 (MAJOR, open, overlap): No comparison rule is stated for the read-back, whose documented value is a numeric option id, so a naive compare reports every good write as not applied.
- L6 (MAJOR, open, single): The three reason lists live only in ./source.md, which is not in the package, so the candidate alone cannot give the implementer the reasons.
- L7 (MINOR, open, single): No task sweeps the allowed roots for the old wording, so a leftover copy elsewhere would pass every listed check; the live repo has no hit today.

## Reviser brief

Blocking finding ids: L1, L3, L4.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
