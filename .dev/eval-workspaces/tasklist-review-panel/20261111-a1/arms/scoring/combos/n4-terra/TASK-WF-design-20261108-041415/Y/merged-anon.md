review: 1 of 3
# Merged review 1 (coordinator script; panel of 4 reviewers)
candidate: TASK-WF-design-20261108-041415/candidate.md sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R2: report <redacted>, block ok true
- R3: report <redacted>, block ok true
- R4: report <redacted>, block ok true
- R1: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | R2, R3, R4 |
| L2 | open | yes | overlap | MAJOR | - | R2, R4 |
| L3 | open | no | single | MAJOR | - | R4 |

## Blocking findings

### L1

#### L1.R2 (F1)

- claim: The design doc must keep the claim-mode gh api user lookup yet Task 10 acceptance forbids any gh api path other than repos/<R>/... and the one orgs/ read, so the acceptance cannot pass without breaking claim mode.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "`--claim` behaviour and text stay unchanged, including its two-block part of the return contract."

#### L1.R2 (F2)

- claim: Task 12 orders writes under ./artifacts/ (owner check and checks log) that the edit-only constraint does not list, with no stated exception.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R2 (F3)

- claim: No text states what the field read-back value is compared against, so a direct comparison with Simple/Medium/Complex can report every successful Complexity write as not applied.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L1.R2 (F4)

- claim: Only the third block keys are fixed; its values are undefined, so an implementation can pass every test while reporting an issue type or field value that was never set.
- anchor: "add a third YAML block with exactly the keys `issue_type`, `complexity_field`, `classification_missing`"

#### L1.R2 (F6)

- claim: The kept maintainer gh label lines target a maintainer-chosen repo, so keeping them unchanged breaches the --repo <R> rule and rewriting them to <R> needs an unstated replacement instruction.
- anchor: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`."
- anchor2: "keep only the `bug` and `enhancement` lines in the maintainer block."

#### L1.R2 (F7)

- claim: The cited source.md is absent from the review package, so reason lists and sequences attributed to specification 2.1 to 2.4 cannot be verified from the candidate alone.
- anchor: "Source: ./source.md"

#### L1.R3 (F1)

- claim: The exactly-two-writes sentence literally excludes the mode label and the pushback comment that the rest of the plan requires, but no implementer can build that reading without failing Task 1's own acceptance criteria, so it is wording slack only.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

#### L1.R3 (F2)

- claim: The goal says the third block lists every unset classification while the block's definition covers only the not-set lines, the missing mode label being carried by labels_missing in block 1, so the printed contract still lists everything.
- anchor: "lists every classification it could not set in its final output and in a third return-contract block"
- anchor2: "add a third YAML block with exactly the keys `issue_type`, `complexity_field`, `classification_missing`"

#### L1.R3 (F3)

- claim: The pinned commit does not exist in this repository and several cited line numbers have drifted, but the plan's own mandatory re-read rule removes any buildable wrong outcome.
- anchor: "Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3` and must be re-read in the live file before each edit."

#### L1.R4 (F2)

- claim: Task 12 writes its check files to ./artifacts or the package folder, and neither location is in the allowed edit set.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "write `./artifacts/owner-manual-check.md` in this package."

#### L1.R4 (F3)

- claim: Several described edits are already in the live files, and the named source commit is absent from this clone, so the plan's premises are stale.
- anchor: "Remove the 11 `type: ...` labels, the 3 `complexity: ...` labels and their `gh label create` lines"

#### L1.R4 (F5)

- claim: The plan does not say whether an unsupported --type flag at create time stops the run, and it contradicts the non-fatal wording for a type that is not applied.
- anchor: "a failure of `gh issue create` is still STOP `E-CREATE-FAILED`"
- anchor2: "both listed and non-fatal"

#### L1.R4 (F6)

- claim: The kept label lines use the placeholder <owner/repo> where the constraint requires --repo <R>.
- anchor: "keep only the `bug` and `enhancement` lines in the maintainer block"

### L2

#### L2.R2 (F5)

- claim: Task 2 does not require the colon form of the label line inside create.md, so the Task 8 test as stated can fail a create.md that satisfies Task 2.
- anchor: "Fourth, `create.md` and `labels.md` carry the three exact line formats `not applied: label missing in repo:`, `not set: issue type` and `not set: field Complexity`."

#### L2.R4 (F1)

- claim: Seven tests as listed never assert Task 2 Wave 1 or the Task 3 error-table rows, so reverting those tasks leaves every test green and the acceptance criterion fails.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red: each new test asserts on the text that task adds."

## Other findings

- L3 (MAJOR, open, single): The quoted assertion and the line numbers do not match the live test file, so the implementer must search for the target.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
