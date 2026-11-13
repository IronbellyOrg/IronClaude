review: 1 of 3
# Merged review 1 (coordinator script; panel of 4 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/candidate.md sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/r2-sonnet/t4-1.md, block ok true
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/r2-sonnet/t3-1.md, block ok true
- t4-2: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/r2-sonnet/t4-2.md, block ok true
- t1b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/r2-sonnet/t1b-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | t1b-1, t3-1, t4-1, t4-2 |
| L2 | open | yes | overlap | MAJOR | - | t1b-1, t3-1, t4-1, t4-2 |
| L3 | open | no | overlap | MAJOR | - | t3-1, t4-1 |
| L4 | open | no | single | MINOR | - | t4-1 |
| L5 | open | no | single | MAJOR | - | t3-1 |
| L6 | open | no | overlap | MINOR | - | t3-1, t4-2 |

## Blocking findings

### L1

#### L1.t4-1 (F1)

- claim: The constraint allows only the type and field writes, but Task 2 keeps a pushback comment on the created issue.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "field POST and read-back; pushback comment; final output with every"

#### L1.t4-1 (F3)

- claim: The kept maintainer lines use a different placeholder than the rule requires, and the text does not say which one wins.
- anchor: "keep only the `bug` and `enhancement` lines in the maintainer block"
- anchor2: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`"

#### L1.t4-1 (F4)

- claim: The artifact path is ambiguous between the project-root artifacts folder and the package folder, and only one of them is named as writable.
- anchor: "write `./artifacts/owner-manual-check.md` in this package"
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`"

#### L1.t4-1 (F5)

- claim: Most tasks describe a pre-change state that the live tree already has, so the stated edits are no-ops or find nothing to remove.
- anchor: "Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3`"

#### L1.t4-1 (F7)

- claim: The read-back has no rule for comparing a single-select option id with an option name, so a correct write may be reported as not applied.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L1.t3-1 (F1)

- claim: The plan forbids any third write to the created issue but keeps a pushback comment on it, so an implementer must break one of the two.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "field POST and read-back; pushback comment; final output with every"

#### L1.t3-1 (F3)

- claim: The text does not say which artifacts folder is meant, so the owner check may be written to the project-root folder that is never staged and sits outside the edit limit.
- anchor: "write `./artifacts/owner-manual-check.md` in this package"
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and"

#### L1.t3-1 (F5)

- claim: On a gh build without the --type flag, every create with a listed type stops at E-CREATE-FAILED, and the text states no minimum gh version or fallback.
- anchor: "`--type` only when the type is listed under `### Repo issue types`"

#### L1.t4-2 (F1)

- claim: A create flow that obeys the two-write limit drops the pushback comment Task 2 requires, so a flag disagreement is never posted and E-POST-FAILED no longer has its stated meaning.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L1.t4-2 (F2)

- claim: The required --mode cell says the issue type is Feature or Bug, which is false for a feature whose area is tests.
- anchor: "the Feature or Bug issue type and the `enhancement` / `bug` label"
- anchor2: "mode `feature` with area `tests` gives Test"

#### L1.t4-2 (F3)

- claim: create.md written only from the task body does not contain the exception string the task's own acceptance criterion requires.
- anchor: "orgs/<owner of R>/issue-fields"
- anchor2: "orgs/<owner>/issue-fields"

#### L1.t1b-1 (F1)

- claim: Task 10's acceptance line allows only repos/<R> paths plus one orgs/ read, but the design doc keeps the unchanged claim line `gh api user -q .login` (docs/designs/sc-issue-command.md:157) and Task 2 and Task 3 allow the user path, so the check cannot pass.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`"

#### L1.t1b-1 (F2)

- claim: The command's Will Not text omits the skill's 'never writes a field other than Complexity', so Task 6's own 'lists agree' criterion may fail and no new test compares the two.
- anchor: "and the Will Not line (line 93) to also say it creates no issue types or issue fields."
- anchor2: "never creates an issue type or an issue field and never writes a field other than Complexity"

#### L1.t1b-1 (F3)

- claim: The constraint allows exactly two writes to the new issue, but Task 2's Wave 5 sequence also posts the pushback comment.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L1.t1b-1 (F5)

- claim: Because .claude/ is gitignored, git status never lists those paths, so the check passes whatever was written there.
- anchor: "`git status --short` shows no path under `.claude/` other than `.claude/settings.json` in the set of staged or tracked changes."

#### L1.t1b-1 (F7)

- claim: The local gh already shows the --type flag and the issueType JSON field, so only the POST body and the silent drop remain unverified.
- anchor: "The POST body, the `--type` flag and the silent-drop behaviour come from GitHub's docs and `gh` help and are UNVERIFIED by a real run"

### L2

#### L2.t4-1 (F2)

- claim: The seven listed tests assert nothing about Task 3's error-table rows or its SKILL.md call-rule exception, so reverting those leaves every new test green.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"

#### L2.t3-1 (F7)

- claim: The check is not defined precisely, so a plain substring match for 'type:' would also match prose such as 'issue type:' and an implementer cannot tell which check is meant.
- anchor: "contains no `type:` label, no `complexity:` label"

#### L2.t4-2 (F4)

- claim: The seven new tests, as listed, stay green if only Task 3 is reverted, so the revert criterion is false of that list.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"
- anchor2: "Write one test per rule, each failing when the behaviour breaks."

#### L2.t1b-1 (F4)

- claim: No new Task 8 test clearly depends on SKILL.md text, so reverting Task 3 turns red only Task 7's updated test.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"

#### L2.t1b-1 (F6)

- claim: The scanner does not say a bare `orgs/` token in prose is not a path, so a naive regex would flag the required 'no other `orgs/` path' sentence.
- anchor: "every `orgs/` path found by regex in the skill folder files and the `AGENTS` files"

## Other findings

- L3 (MAJOR, open, overlap): The reason list for the three output lines lives in a source file that is not beside the candidate, so the acceptance cannot be checked from here.
- L4 (MINOR, open, single): Several line numbers in Tasks 7 and 8 are stale against the live test file; the test names are correct.
- L5 (MAJOR, open, single): No planned test compares the command's Will lists with the skill's, and the existing Will test checks only a few tokens, so the agreement is never verified.
- L6 (MINOR, open, overlap): The before-state the tasks describe is already gone from the tree at 8c93e1d for several files, so those edit steps find nothing to change and the plan does not say what to do then.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
