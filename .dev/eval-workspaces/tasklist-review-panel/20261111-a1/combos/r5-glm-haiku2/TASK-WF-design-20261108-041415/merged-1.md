review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/candidate.md sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/r5-glm-haiku2/t3-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/r5-glm-haiku2/t4-1.md, block ok true
- t4-2: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/r5-glm-haiku2/t4-2.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | t3-1, t4-1, t4-2 |
| L2 | open | yes | single | MAJOR | - | t4-1 |
| L3 | open | no | single | MAJOR | - | t4-1 |
| L4 | open | no | single | MINOR | - | t4-1 |

## Blocking findings

### L1

#### L1.t3-1 (F1)

- claim: The plan states the Complexity field read-back step but never states what the read-back must equal, so an implementer compares the returned option id with the POSTed option name and reports every successful write as 'not set: field Complexity <value>: not applied after create'.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L1.t3-1 (F2)

- claim: The constraint's 'exactly two things written to a created issue' conflicts with Task 2's kept pushback comment and its E-POST-FAILED STOP code; harmless because the task text is explicit, but the constraint wording should say 'two classifications'.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L1.t3-1 (F3)

- claim: No task adds the new .dev/issues/<N>/complexity-field.json artifact to the command file's create-mode Outputs table or the skill's files-table note, so the file the protocol writes stays undocumented.
- anchor: "Edit `src/superclaude/commands/issue.md`. Source sections: decisions Q5, Q6; section 3.1."

#### L1.t4-1 (F1)

- claim: The constraint allows exactly two writes to the created issue, but Task 2 keeps the pushback comment, which is a third write.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L1.t4-1 (F4)

- claim: The text does not say to match by issue_field_id and compare single_select_option.name, so a value comparison reports false not-applied lines.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L1.t4-1 (F6)

- claim: Most target text already exists at HEAD 8c93e1d and the cited line numbers are stale, but the plan has no rule for a target already in its final state.
- anchor: "Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3` and must be re-read in the live file before each edit."

#### L1.t4-1 (F7)

- claim: The output path could resolve to the project-root artifacts folder that is never staged, and this package is not defined.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.t4-1 (F8)

- claim: The name --type is used for both the skill's area flag and gh's issue type flag, so an implementer may pass the area value to gh.
- anchor: "`--type` only when the type is listed under `### Repo issue types`"

#### L1.t4-1 (F9)

- claim: The rename is the local draft-directory rename, not the issue title, and the text does not say so.
- anchor: "`gh issue create` and the rename"

#### L1.t4-2 (F1)

- claim: The --mode row gives mode feature the Feature issue type, but the type rule gives Test for mode feature with area tests, so one input gets two answers.
- anchor: "Picks the feature or bug template, the Feature or Bug issue type and the `enhancement` / `bug` label"
- anchor2: "mode `feature` with area `tests` gives Test"

#### L1.t4-2 (F2)

- claim: The type lookup uses a repo route that GitHub's issue-types page does not document, and the plan forbids the org route, so no type is set and every run prints lookup failed.
- anchor: "add the two reads `gh api repos/<R>/issue-types` and `gh api orgs/<owner of R>/issue-fields`"
- anchor2: "the T3 worker may read exactly `orgs/<owner of R>/issue-fields`"

#### L1.t4-2 (F3)

- claim: Commit 1aa2e5c3 is absent here and the tree already has the target state, so most edit steps find nothing to change and Task 8's test-count rise has no true baseline.
- anchor: "Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3` and must be re-read in the live file before each edit."
- anchor2: "Remove the 11 `type: ...` labels, the 3 `complexity: ...` labels and their `gh label create` lines"

#### L1.t4-2 (F4)

- claim: The live maintainer label lines use --repo <owner/repo>, and Task 1 checks only gh issue lines, so the gh label rule is not enforced.
- anchor: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`."
- anchor2: "Every `gh issue` line in the file carries `--repo <R>`"

#### L1.t4-2 (F5)

- claim: Constraint 23 allows exactly two writes to the created issue, but Task 2 also posts a pushback comment on it and the label is applied at creation, so the count depends on how the words are read.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L1.t4-2 (F6)

- claim: The path could mean the project-root artifacts folder or the package folder, and neither is an edit root in Constraint 19.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."

#### L1.t4-2 (F7)

- claim: The skill text states the silent type drop without push access as fact, while the plan marks it unverified.
- anchor: "the silent-drop behaviour come from GitHub's docs and `gh` help and are UNVERIFIED by a real run"

### L2

#### L2.t4-1 (F2)

- claim: None of the six listed tests reads the Task 3 error rows or the Task 2 label-request removal, so reverting them leaves every test green and the acceptance line cannot pass.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"
- anchor2: "plus two new rows (issue type not available or not applied, Complexity field not available or write failed), both listed and non-fatal"

#### L2.t4-1 (F5)

- claim: Task 2 does not require the colon form in create.md, so following Task 2 alone leaves test 4 red.
- anchor: "Fourth, `create.md` and `labels.md` carry the three exact line formats"

## Other findings

- L3 (MAJOR, open, single): Line 329 is the sc-index-repo row, and the phrase to change does not exist in HOW-WE-WORK.md or core CLAUDE.md.
- L4 (MINOR, open, single): The source file is not in the candidate folder, so its decision and specification references cannot be checked here.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
