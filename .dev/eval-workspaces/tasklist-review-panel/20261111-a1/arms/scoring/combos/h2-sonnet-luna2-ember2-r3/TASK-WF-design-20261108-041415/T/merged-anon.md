review: 1 of 3
# Merged review 1 (coordinator script; panel of 5 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R1: report <redacted>, block ok true
- R4: report <redacted>, block ok true
- R5: report <redacted>, block ok true
- R2: report <redacted>, block ok true
- R3: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | R1, R2, R3, R4, R5 |
| L2 | open | no | overlap | MAJOR | - | R1, R3 |
| L3 | open | no | overlap | MAJOR | - | R1, R2, R4, R5 |
| L4 | open | no | single | MAJOR | 2.2 | R1 |
| L5 | open | no | single | MINOR | - | R1 |
| L6 | open | no | single | MINOR | - | R2 |
| L7 | open | no | single | MAJOR | - | R3 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: The Task 10 check fails on the unchanged claim-flow line `gh api user -q .login` in docs/designs/sc-issue-command.md, and Task 2 itself allows the `user` path.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`"

#### L1.R1 (F5)

- claim: The literal span in Task 3 lacks --repo and would fail the existing repo-flag scan if copied as written.
- anchor: "`gh issue create ... --type <name>` to the orchestrator's write list"
- anchor2: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`"

#### L1.R1 (F6)

- claim: The plan also posts the pushback comment and applies the mode label, so 'exactly two things' is not true.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "field POST and read-back; pushback comment; final output with every `not applied` and `not set` line"

#### L1.R1 (F8)

- claim: Task 12 writes files outside the listed edit roots, and its manual check leaves real test issues open with no cleanup step.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R4 (F1)

- claim: An implementer who follows the stated text as written writes the required artifacts outside every permitted edit root, so the scope restriction and Task 12 cannot both be satisfied.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/."

#### L1.R5 (F1)

- claim: The plan both prohibits edits outside its listed directories and requires an artifact under `./artifacts/`, so the implementer cannot satisfy both requirements.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R2 (F1)

- claim: classification_missing entry shape is never pinned, so final output and return contract can disagree while both stay text-compliant
- anchor: "lists every classification it could not set in its final output and in a third return-contract block"
- anchor2: "add a third YAML block with exactly the keys `issue_type`, `complexity_field`, `classification_missing`"

#### L1.R2 (F2)

- claim: allowed orgs/ path is spelled two ways across tasks, splitting the protocol text from the worker rule
- anchor: "The T3 worker also runs `gh api repos/<R>/issue-types` and `gh api orgs/<owner of R>/issue-fields`"
- anchor2: "states the single `orgs/<owner>/issue-fields` exception"

#### L1.R2 (F4)

- claim: artifacts location is ambiguous between package artifacts and repo-root artifacts, which is never staged
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R3 (F2)

- claim: Task 12 names a relative artifacts path without fixing the package root, so the manual check could land where the next step cannot find it.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R3 (F4)

- claim: The repo flag rule never states the maintainer block placeholder form, so an implementer must guess between the by hand example and the flag form.
- anchor: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`."

## Other findings

- L2 (MAJOR, open, overlap): As described, no new test asserts on text only Task 3 adds, so reverting Task 3 leaves every new test green unless test 2 is built as an exact-set check.
- L3 (MAJOR, open, overlap): No rule says how to compare the read-back with the option name, and GitHub does not document whether `value` is a name or an id, so a naive comparison can wrongly report 'not applied after create'.
- L4 (MAJOR, open, single): A failed pushback comment stops the run before the final output, and the text does not say whether the not-set list and third block are still produced for an issue that already exists.
- L5 (MINOR, open, single): The --mode row names only Feature or Bug as the issue type, but a feature with area tests gets Test.
- L6 (MINOR, open, single): scout heading order is inconsistent between Task 2 and Task 4 but presence tests pass either way
- L7 (MAJOR, open, single): Task 10 leaves history filtering undefined, so an implementer could leave false label statements or rewrite history that should stay.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
