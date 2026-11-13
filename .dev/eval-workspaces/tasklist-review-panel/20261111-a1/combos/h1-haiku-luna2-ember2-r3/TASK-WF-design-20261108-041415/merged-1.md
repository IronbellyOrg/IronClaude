review: 1 of 3
# Merged review 1 (coordinator script; panel of 5 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/candidate.md sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- t2-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/h1-haiku-luna2-ember2-r3/t2-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/h1-haiku-luna2-ember2-r3/t4-1.md, block ok true
- t4-2: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/h1-haiku-luna2-ember2-r3/t4-2.md, block ok true
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/h1-haiku-luna2-ember2-r3/t2b-1.md, block ok true
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/h1-haiku-luna2-ember2-r3/t3-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | t2-1, t2b-1, t3-1 |
| L2 | open | yes | overlap | MAJOR | - | t2-1, t2b-1, t3-1 |
| L3 | open | yes | overlap | MAJOR | - | t2-1, t2b-1, t4-1 |
| L4 | open | no | single | MAJOR | - | t4-1 |
| L5 | open | no | single | MAJOR | 2.1 | t4-2 |
| L6 | open | no | single | MINOR | - | t2b-1 |

## Blocking findings

### L1

#### L1.t2-1 (F1)

- claim: The skill is told to write exactly two things to the created issue, yet the Wave 5 sequence also posts a pushback comment, so the two stated texts cannot both hold.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "field POST and read-back; pushback comment; final output with every"

#### L1.t2-1 (F2)

- claim: The artifact path is ambiguous between the project-root artifacts folder, which Constraint 19 forbids, and the package folder, so an implementer has to guess.
- anchor: "write `./artifacts/owner-manual-check.md` in this package"
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`"

#### L1.t2-1 (F5)

- claim: The live tree already has the new create steps, template headings and return-contract assertions, and the plan has no step to detect already-applied tasks.
- anchor: "Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3`"
- anchor2: "change `len(blocks) == 2` to 3"

#### L1.t2-1 (F6)

- claim: Cited test line numbers are stale: the return-contract test is at 545 and the Will test at 586.
- anchor: "(around lines 492 to 520)"
- anchor2: "Re-run the Will / Will Not test (`test_skill_will_and_will_not_match_the_command_file`, line 527)"

#### L1.t2b-1 (F2)

- claim: Task 12 writes under ./artifacts which is outside the stated edit roots and the package root is never defined, so the plan is ambiguous about where the two Task 12 files go.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/."
- anchor2: "write `./artifacts/owner-manual-check.md` in this package."

#### L1.t2b-1 (F3)

- claim: Note: Task 7 line numbers differ from the live test file; the re-read instruction covers it.
- anchor: "Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3` and must be re-read in the live file before each edit."

#### L1.t3-1 (F1)

- claim: The count of writes omits the mode label that the Goal and Tasks 1 and 2 require, so a literal reader under-counts what a created issue receives.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."

#### L1.t3-1 (F2)

- claim: Task 12 requires a file under `./artifacts/` that the allowed edit areas do not include, and the relative path does not say which folder it means.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.t3-1 (F4)

- claim: The maintainer label-creation lines kept by Task 1 use a different repo placeholder in the live file, and the plan never states their final form.
- anchor: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`."

### L2

#### L2.t2-1 (F3)

- claim: The six listed new tests do not assert Task 3's error-table rows or Task 2's never-stops sentence, so the reversion acceptance cannot pass as the list is written.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"
- anchor2: "Sixth, `labels.md` states Feature, Bug, Test and Simple, Medium, Complex"

#### L2.t2b-1 (F5)

- claim: Note: revert-red holds only if new tests assert per file, not on combined text.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red: each new test asserts on the text that task adds."

#### L2.t3-1 (F3)

- claim: No enumerated new test asserts on the SKILL.md text only Task 3 adds, so a Task 3 revert can stay green unless the file-list test is coded as an exact set.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red: each new test asserts on the text that task adds."

### L3

#### L3.t2-1 (F4)

- claim: The wording prescribed for the command and skill lacks the substrings the existing boundary test requires, so the command-test acceptance fails as written.
- anchor: "also say it creates no issue types or issue fields"
- anchor2: "add that the skill never creates an issue type or an issue field"

#### L3.t4-1 (F1)

- claim: Task 6 mandates mode wording that contradicts Task 1 by implying feature mode always selects Feature, even when the area selects Test.
- anchor: "the `--mode` row (line 41) to \"Picks the feature or bug template, the Feature or Bug issue type and the `enhancement` / `bug` label\""
- anchor2: "the issue type rule (mode `bug` gives Bug; mode `feature` with area `tests` gives Test; every other feature gives Feature; Task is never chosen)"

#### L3.t2b-1 (F1)

- claim: Plan never defines the single-select read-back shape (option id vs option name), so a literal implementer misdetects success as not applied.
- anchor: "the POST with `gh api -X POST repos/<R>/issues/<N>/issue-field-values --input <file>`"

## Other findings

- L4 (MAJOR, open, single): Task 1 does not require matching the field read-back by field id and comparing the single-select option name, so an implementation may compare the returned option id to the name and falsely report the field as unset.
- L5 (MAJOR, open, single): An implementer who follows the stated text as written could compare the single-select option ID to its name and report a successfully set Complexity value as missing; the required response interpretation is not specified.
- L6 (MINOR, open, single): Note: conditional CLAUDE.md handling differs from source re-run wording; live file needs no change.

## Reviser brief

Blocking finding ids: L1, L2, L3.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
