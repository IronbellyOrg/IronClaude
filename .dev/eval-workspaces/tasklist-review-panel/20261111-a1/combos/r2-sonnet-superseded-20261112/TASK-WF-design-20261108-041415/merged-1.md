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
| L1 | open | yes | overlap | CRITICAL | - | t1b-1, t3-1, t4-1, t4-2 |
| L2 | open | yes | overlap | MAJOR | - | t3-1, t4-1 |
| L3 | open | no | single | MAJOR | - | t4-1 |
| L4 | open | no | overlap | MAJOR | - | t1b-1, t3-1, t4-1 |
| L5 | open | no | overlap | MINOR | - | t3-1, t4-1 |
| L6 | open | no | single | MINOR | - | t4-1 |
| L7 | open | no | overlap | MAJOR | - | t3-1, t4-2 |

## Blocking findings

### L1

#### L1.t4-1 (F1)

- claim: Constraint 23 allows exactly two writes to a created issue, but Task 2 Wave 5 keeps a pushback comment, which is a third write.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "field POST and read-back; pushback comment; final output"

#### L1.t4-1 (F4)

- claim: The live user guide, labels.md and worker job 2 already carry the new text, so Tasks 1, 5 and 9 describe edits that are already made.
- anchor: "currently say labels from a fixed set and `type: <value>` labels"
- anchor2: "In job 2 \"Create lookup\" (line 22) add the two reads"

#### L1.t4-1 (F6)

- claim: The artifact path is outside the Constraint 19 edit list, and 'this package' does not say whether it means the package folder or the project root.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`"

#### L1.t3-1 (F1)

- claim: The constraint allows only the type and the field as writes, but the Goal, Task 1 and Task 2 require the mode label and the pushback comment.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type"
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

#### L1.t3-1 (F3)

- claim: GitHub documents issue types only at the org route, so the repo-scoped lookup fails every run and no issue type is ever set.
- anchor: "add the two reads `gh api repos/<R>/issue-types` and `gh api orgs/<owner of R>/issue-fields`"
- anchor2: "the T3 worker may read exactly `orgs/<owner of R>/issue-fields`"

#### L1.t3-1 (F4)

- claim: The rename step is undefined, so the implementer must guess its target path.
- anchor: "`gh issue create` and the rename; type read-back"

#### L1.t3-1 (F8)

- claim: The artifact location conflicts with the edit-scope constraint, and the candidate does not say whether package artifacts are exempt.
- anchor: "write `./artifacts/owner-manual-check.md` in this package"

#### L1.t4-2 (F1)

- claim: Following the two-write constraint omits the mode label the goal and Task 1 require on the new issue.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

#### L1.t4-2 (F2)

- claim: A literal check for the short orgs token fails if create.md contains only the longer token the task body names.
- anchor: "states the single `orgs/<owner>/issue-fields` exception"
- anchor2: "read-only GET of `orgs/<owner of R>/issue-fields`"

#### L1.t1b-1 (F1)

- claim: Task 10 requires every gh api path in the design doc to be repos/<R>/... except the orgs read, but the doc keeps the claim call gh api user -q .login at line 157, which Task 2 itself allows; the criterion cannot pass without rewriting unchanged claim behaviour.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`"

#### L1.t1b-1 (F2)

- claim: No task runs tests/commands/test_issue_command.py or tests/skills/test_issue_worker_agents.py, which pin the command file and the T3 worker that Tasks 6 and 5 edit, so a break there passes every stated check.
- anchor: "`make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`"

#### L1.t1b-1 (F4)

- claim: The sentence says two writes, but Wave 5 also applies the mode label and posts the pushback comment.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L1.t1b-1 (F5)

- claim: Task 12 writes under the package artifacts folder, which the edit-only list does not name.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "write `./artifacts/owner-manual-check.md` in this package"

#### L1.t1b-1 (F6)

- claim: The constraints list three default decisions and Task 12 records four.
- anchor: "Decisions taken as defaults (the owner may reverse them later)"
- anchor2: "the four defaults the owner may reverse"

### L2

#### L2.t4-1 (F2)

- claim: None of the six rule tests or the self-check reads the SKILL.md error rows or Will Not text, or the create.md Wave 1 and Wave 2 text, so reverting them keeps every new test green.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"
- anchor2: "Sixth, `labels.md` states Feature, Bug, Test and Simple, Medium, Complex."

#### L2.t4-1 (F5)

- claim: The file already holds issue-438 tests for the orgs scanner, label and POST checks and output lines, so the six new tests would duplicate them.
- anchor: "Add tests to `tests/skills/test_issue_protocol.py`, using the file's existing helpers"

#### L2.t4-1 (M2)

- claim: The fork-safety test is at line 701, not line 642.
- anchor: "in the style of `test_fork_safety_scan_fails_on_a_ref_without_repo` (line 642)"

#### L2.t3-1 (F2)

- claim: No new test covers flags-decision.md or the create-review wording, so reverting Task 4 leaves every new test green and the Task 8 criterion cannot pass.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"
- anchor2: "In `flags-decision.md` add an `Issue type` row"

#### L2.t3-1 (F5)

- claim: A whitespace-stopping regex captures orgs/<owner and fails on the correct path, and the candidate does not specify the regex.
- anchor: "every `orgs/` path found by regex in the skill folder files and the `AGENTS` files equals"

## Other findings

- L3 (MAJOR, open, single): HOW-WE-WORK.md line 329 is the /sc:index-repo row and the file has no fixed-set phrase, so the edit target does not exist.
- L4 (MAJOR, open, overlap): The reason strings and decisions live in ./source.md, which is not in the candidate folder, so Task 1's acceptance cannot be checked.
- L5 (MINOR, open, overlap): The Will / Will Not test is at line 586 and the st10 test at line 545, not the lines given.
- L6 (MINOR, open, single): The live error row is at line 169, and the Will Not list runs past the line range given.
- L7 (MAJOR, open, overlap): At HEAD 8c93e1d these edits are already present, so the plan's before-state is stale and no baseline check is given.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
