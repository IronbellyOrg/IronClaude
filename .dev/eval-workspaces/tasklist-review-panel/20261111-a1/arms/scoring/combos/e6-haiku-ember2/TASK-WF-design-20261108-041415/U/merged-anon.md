review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R3: report <redacted>, block ok true
- R1: report <redacted>, block ok true
- R2: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | R1, R2, R3 |
| L2 | open | yes | overlap | MAJOR | - | R1, R2, R3 |
| L3 | open | no | overlap | MAJOR | - | R2, R3 |

## Blocking findings

### L1

#### L1.R3 (F1)

- claim: The constraint allows only two writes to the created issue, but the Wave 5 sequence includes a pushback comment, a third write.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "field POST and read-back; pushback comment; final output with every `not applied` and `not set` line"

#### L1.R3 (M1)

- claim: A pushback-comment STOP before the final output may hide the unset type and field lines; STOP output is not defined.
- anchor: "`E-CREATE-FAILED` and `E-POST-FAILED` keep their current meaning."
- anchor2: "final output with every `not applied` and `not set` line"

#### L1.R3 (M2)

- claim: The repo already contains the target text and lacks commit 1aa2e5c3, so the stated baseline and line numbers do not match and the plan has no rule for an already-applied change.
- anchor: "Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3` and must be re-read in the live file before each edit."

#### L1.R3 (M3)

- claim: The relative artifacts path could resolve to the project-root artifacts folder, which is never staged and sits outside the edit list.
- anchor: "write `./artifacts/owner-manual-check.md` in this package"
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`"

#### L1.R3 (M4)

- claim: The read-back field name is unverified but is not on the owner's manual-check list, so a wrong name would show every typed issue as not set.
- anchor: "read-back with `gh issue view <N> --repo <R> --json issueType --jq .issueType.name`"
- anchor2: "It also records the three UNVERIFIED points from the source section 3.4"

#### L1.R3 (M6)

- claim: The plan's own text uses the placeholder `<owner of R>`, which the constraint does not allow.
- anchor: "No file may contain a brace placeholder for owner and repo; use `<owner>` and `<R>`."
- anchor2: "read-only GET of `orgs/<owner of R>/issue-fields`"

#### L1.R1 (F1)

- claim: Task 12 artifacts fall outside the stated edit boundary, so an implementer cannot satisfy both texts without guessing.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R1 (F3)

- claim: The maintainer gh label create lines have no stated --repo argument form.
- anchor: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`."
- anchor2: "keep only the `bug` and `enhancement` lines in the maintainer block"

#### L1.R1 (F4)

- claim: The Goal wording can be read to require the missing mode label in the third block, while Task 3 reports it only in labels_missing.
- anchor: "lists every classification it could not set in its final output and in a third return-contract block"
- anchor2: "add a third YAML block with exactly the keys `issue_type`, `complexity_field`, `classification_missing`"

#### L1.R2 (F1)

- claim: The manual check lands at repo-root ./artifacts/ instead of the staged package artifacts directory.
- anchor: "Then write ./artifacts/owner-manual-check.md in this package."
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."

### L2

#### L2.R3 (F2)

- claim: The seven listed tests cannot detect a revert of several Task 3, 4 and 5 texts, so the acceptance criterion fails as written.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"
- anchor2: "Write one test per rule, each failing when the behaviour breaks."

#### L2.R1 (F2)

- claim: No enumerated new test asserts on SKILL.md text added by Task 3, so reverting Task 3 alone turns no new test red.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red: each new test asserts on the text that task adds."
- anchor2: "every `orgs/` path found by regex in the skill folder files and the `AGENTS` files equals `orgs/<owner of R>/issue-fields` or `orgs/<owner>/issue-fields`"

#### L2.R2 (F3)

- claim: The test wording can require the read-only worker to contain write syntax it bans.
- anchor: "the skill folder and the agents contain `-X POST` together with `issue-field-values` and no `-X PUT`."

#### L2.R2 (F4)

- claim: The owner placeholder is spelled inconsistently across the plan.
- anchor: "equals `orgs/<owner of R>/issue-fields` or `orgs/<owner>/issue-fields`"

## Other findings

- L3 (MAJOR, open, overlap): The named test does not compare the command file, so the Will and Will Not agreement has no check, and the line number is stale.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
