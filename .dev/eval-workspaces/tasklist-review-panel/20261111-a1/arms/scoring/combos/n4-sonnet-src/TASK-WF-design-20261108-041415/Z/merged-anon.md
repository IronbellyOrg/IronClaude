review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R2: report <redacted>, block ok true
- R3: report <redacted>, block ok true
- R1: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | R1, R2, R3 |
| L2 | open | no | overlap | MAJOR | - | R2, R3 |
| L3 | open | no | overlap | MAJOR | - | R2, R3 |
| L4 | open | no | single | MAJOR | - | R3 |
| L5 | open | no | single | MAJOR | - | R3 |
| L6 | open | no | single | MINOR | - | R3 |

## Blocking findings

### L1

#### L1.R2 (F1)

- claim: The design doc must keep gh api user for the unchanged claim lookup, so an all-repos/<R> acceptance cannot pass without breaking claim mode.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "`--claim` behaviour and text stay unchanged, including its two-block part of the return contract."

#### L1.R2 (F2)

- claim: Read as a write count, exactly two things excludes the required pushback comment and its E-POST-FAILED stop.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L1.R2 (F4)

- claim: The subset and collective wordings of the second and third new tests can stay green when only the SKILL.md change of Task 3 is reverted.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red: each new test asserts on the text that task adds."
- anchor2: "appears only in `create.md`, `SKILL.md` and `issue-worker-t3.md`"

#### L1.R2 (F5)

- claim: The base of ./ is unstated, so the owner check can land in the root artifacts folder instead of the package artifacts folder.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R3 (F1)

- claim: The constraint allows exactly two writes besides the issue, but Task 2 keeps the pushback comment and Task 1 applies the mode label, so an implementer obeying the constraint drops the pushback comment and loses the record of disagreements with the user's flags.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "field POST and read-back; pushback comment; final output with every `not applied` and `not set` line"

#### L1.R3 (F2)

- claim: Baseline commit 1aa2e5c3 is absent and HEAD already carries the target text and the seven new tests (119 pass), so the edits find nothing to change and the test-count rule passes only by duplicating tests; the plan never states a baseline check.
- anchor: "Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3` and must be re-read in the live file before each edit."
- anchor2: "the count of collected tests rises by at least seven"

#### L1.R3 (F6)

- claim: Task 12 writes to ./artifacts, which is outside the four allowed edit trees and is not the package artifacts folder, so the implementer must guess where the owner check file goes.
- anchor: "write `./artifacts/owner-manual-check.md` in this package"

#### L1.R3 (F9)

- claim: The maintainer block keeps the placeholder <owner/repo>, which does not follow the <owner> and <R> spelling the constraint asks for, and the candidate does not say to rename it.
- anchor: "No file may contain a brace placeholder for owner and repo; use `<owner>` and `<R>`."

#### L1.R1 (F1)

- claim: The design doc keeps `gh api user -q .login` in its claim lookup, which the plan may not change, so the Task 10 line saying every gh api path spells repos/<R> cannot pass and also drops the allowed `user` path.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "`--claim` behaviour and text stay unchanged, including its two-block part of the return contract."

#### L1.R1 (F2)

- claim: No new test asserts on the text Task 3 adds to SKILL.md, so reverting Task 3 keeps every new test green under the restriction-only reading of the orgs test.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"
- anchor2: "appears only in `create.md`, `SKILL.md` and `issue-worker-t3.md`"

#### L1.R1 (F3)

- claim: A loose regex flags the bare `orgs/` in the required sentence 'no other `orgs/` path is allowed' and turns the new test red on text the plan itself requires.
- anchor: "every `orgs/` path found by regex in the skill folder files and the `AGENTS` files equals"
- anchor2: "`create.md` states the single `orgs/<owner>/issue-fields` exception and that no other `orgs/` path is allowed."

#### L1.R1 (F4)

- claim: The constraint allows exactly two writes to the created issue, but Wave 5 also posts the pushback comment and applies the mode label.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "field POST and read-back; pushback comment; final output with every `not applied` and `not set` line"

#### L1.R1 (F5)

- claim: Task 12 writes the owner check and the check log in the package artifacts folder, which the edit-only constraint does not list.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

## Other findings

- L2 (MAJOR, open, overlap): No read-back row shape is stated, so comparing the numeric option id value with the option name would report every successful Complexity write as not set.
- L3 (MAJOR, open, overlap): The command Will Not list is never told to add the never-writes-another-field sentence, so it can disagree with the skill list the acceptance says it matches.
- L4 (MAJOR, open, single): Line 329 of HOW-WE-WORK.md is the /sc:index-repo row, the /sc:issue row is line 330, and the phrase to change exists in neither HOW-WE-WORK.md nor core CLAUDE.md, so the edit cannot be made as written and its acceptance check passes with no edit.
- L5 (MAJOR, open, single): Spec 2.5 says a user-owned repo or an org without the field gives field not found in org, but the candidate records every failed read as lookup failed and never says how a 404 from the org read is classified.
- L6 (MINOR, open, single): Stale line numbers: the Will and Will Not test is at line 586, the return-contract test at 545, and the fork-safety test at 701, so the cited lines point at other tests.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
