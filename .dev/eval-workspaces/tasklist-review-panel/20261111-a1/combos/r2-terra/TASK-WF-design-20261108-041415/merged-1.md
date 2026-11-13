review: 1 of 3
# Merged review 1 (coordinator script; panel of 4 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/candidate.md sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/r2-terra/t4-1.md, block ok true
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/r2-terra/t3-1.md, block ok true
- t4-2: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/r2-terra/t4-2.md, block ok true
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/r2-terra/t2b-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | MAJOR | - | t4-1 |
| L2 | open | yes | overlap | MAJOR | - | t3-1, t4-1, t4-2 |
| L3 | open | no | single | MAJOR | - | t4-1 |

## Blocking findings

### L1

#### L1.t4-1 (F1)

- claim: An implementer who follows the stated text as written builds the seven Task 8 tests, and X is wrong because reverting the flags-decision Issue type row, the create-review wording or the SKILL.md error rows turns none of them red, so the acceptance criterion cannot pass.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red: each new test asserts on the text that task adds."

### L2

#### L2.t4-1 (F2)

- claim: An implementer who follows Task 2 posts a pushback comment and attaches the mode label on the created issue, and X is wrong because Constraint 23 allows exactly two writes besides the issue itself.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "field POST and read-back; pushback comment; final output with every `not applied` and `not set` line"

#### L2.t4-1 (F3)

- claim: The issue-types lookup uses a repository path GitHub documents only at org level, so every type lookup fails and the one allowed orgs path cannot fix it (Medium under the first-review grading check).
- anchor: "add the two reads `gh api repos/<R>/issue-types` and `gh api orgs/<owner of R>/issue-fields`"

#### L2.t4-1 (F4)

- claim: The base commit is absent from this clone and the live files already carry the target wording, so the before-text and the seven-test count do not match the checkout (Medium).
- anchor: "Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3`"

#### L2.t4-1 (F5)

- claim: Decisions and specifications are cited but the source file is absent, and the reasons that Task 1 requires are never listed in the candidate (Medium).
- anchor: "Source: ./source.md"

#### L2.t4-1 (F7)

- claim: Another test file pins the exact T3, create and labels wording and the repos issue-types path, and no step runs it (Medium).
- anchor: "uv run pytest tests/skills/test_issue_protocol.py -v"

#### L2.t4-1 (F8)

- claim: Task 12 lists four owner-reversible defaults and the constraints list three.
- anchor: "Decisions taken as defaults (the owner may reverse them later)"

#### L2.t4-1 (F9)

- claim: The kept maintainer label lines use the placeholder owner/repo, not the <R> the constraint names.
- anchor: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`"

#### L2.t4-1 (F10)

- claim: The ban on editing .claude conflicts with the make sync-dev step, which writes there.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`"

#### L2.t4-1 (F11)

- claim: Task 12 writes its artifacts outside the .dev/tasks package folder that the repo rule requires.
- anchor: "./artifacts/owner-manual-check.md"

#### L2.t3-1 (F1)

- claim: The Constraints say the skill writes exactly two things besides the issue (the type and the field), but Task 1 and Task 2 also apply the mode label at create and post a pushback comment, so the two texts cannot both be met.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L2.t3-1 (F2)

- claim: The tasks describe the pre-change tree at commit 1aa2e5c3, but the live tree already has no type or complexity labels, already asserts three return blocks at test_issue_protocol.py line 549, and already has the issue-438 rule tests, so most edits are no-ops or duplicate tests.
- anchor: "Remove the 11 `type: ...` labels, the 3 `complexity: ...` labels and their `gh label create` lines"
- anchor2: "change `len(blocks) == 2` to 3"

#### L2.t3-1 (F3)

- claim: The plan does not say whether ./artifacts is the project-root folder or the package folder, and the project rules treat those as different places, so the owner-check file may land outside the allowed edit scope.
- anchor: "write `./artifacts/owner-manual-check.md` in this package"
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`"

#### L2.t3-1 (F4)

- claim: The plan gives no comparison rule for the read-back, and the live refs/labels.md says a single-select read-back returns an option id, so an implementer who compares names reports every successful write as not applied.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L2.t3-1 (F5)

- claim: GitHub's issue-types docs list only GET /orgs/{org}/issue-types and no repo-level route, so the repos/<R>/issue-types read likely fails every time and the no-other-orgs rule forbids the documented route; every type is then reported missing.
- anchor: "add the two reads `gh api repos/<R>/issue-types` and `gh api orgs/<owner of R>/issue-fields`"
- anchor2: "no other `orgs/` path is allowed"

#### L2.t3-1 (F6)

- claim: The three output line formats must carry the reasons from specification 2.4, but that source is not in the package folder and the candidate lists no reasons, so the exact reason set cannot be written.
- anchor: "with every reason listed in specification 2.4"
- anchor2: "Source: ./source.md"

#### L2.t3-1 (F7)

- claim: "for either" can mean type or complexity, or bug and enhancement too, and Task 1 keeps the bug and enhancement create lines, so the acceptance check reads two ways.
- anchor: "no `gh label create` line for either"

#### L2.t4-2 (F1)

- claim: Task 10's file-wide check cannot pass while the design doc keeps the required `gh api user` login call, and changing that call to pass the check removes the login lookup.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`, with one stated exception"

#### L2.t4-2 (F2)

- claim: A literal reading of exactly two writes drops the mode label the goal and Wave 5 require.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

#### L2.t4-2 (F3)

- claim: The plan never says to match `single_select_option.name` instead of the numeric read-back `value`, so a naive check reports a successful Complexity write as not set.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

## Other findings

- L3 (MAJOR, open, single): The phrase claim block can mean the ten-field block, which would contradict the kept create-mode-prints-none sentence (Medium).

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
