review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/candidate.md sha256 cfd8f983d22ab8af1638ffb2a464215e56048f753f7902e3066435d8de176ca4
reviewers:
- t1b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/b4-sonnet-luna2/t1b-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/b4-sonnet-luna2/t4-1.md, block ok false
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/b4-sonnet-luna2/t3-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | t1b-1, t4-1 |
| L2 | open | no | single | MAJOR | - | t1b-1 |
| L3 | open | yes | single | MAJOR | - | t3-1 |

## Blocking findings

### L1

#### L1.t1b-1 (F1)

- claim: The launcher spec exports all three tier ids in every tier-mode launch with no per-owner access check, so a tier-limited owner would get opus mapped to a tier they cannot use.
- anchor: "they run only when tier mode is on, so a launch that is not in tier mode leaves the inherited environment untouched"

#### L1.t1b-1 (F2)

- claim: The harness derives REPO_ROOT from __file__ parents[2] and imports models from it, so a copy under the artifacts folder fails at import unless the paths are repointed, which the task never says.
- anchor: "copy the harness and the test into a scratch module under ./artifacts/t9-scratch/ with the harness addition applied"
- anchor2: "(not a KeyError and not an import error)"

#### L1.t1b-1 (F5)

- claim: Task 8 requires Tasks 2 to 4 to be done but its declared dependency chain does not include them.
- anchor: "all tests green after Tasks 2 to 7"
- anchor2: "Depends on: Task 7"

#### L1.t1b-1 (F6)

- claim: The test-file line numbers carry no re-verify mark and the D12 source note's commands.py line numbers go stale after the Task 2 comment grows.
- anchor: "records only a fixed set of keys (lines 330-341)"
- anchor2: "In docs/testing/v5.0.0/user/D12-reflect.md change the expected command at line 235"

#### L1.t1b-1 (F7)

- claim: Installed skill text points at a repo-only docs page that does not exist when the skill runs in another project.
- anchor: "see the model-alias reference page in docs/reference"

#### L1.t4-1 (F2)

- claim: The required follow-up spec cannot accurately quote the cited lines as the tier-mode block and custom-option exports because those lines contain unrelated code.
- anchor: "the tier-mode block at lines 776-785, where the launcher also tests that CCSESSION_EXT_PROFILE is not 1 at line 777, and the custom-option exports at lines 1099-1103"

### L3

#### L3.t3-1 (F1)

- claim: Task 5 requires running a pytest file that does not exist and does not specify creating it, so the listed acceptance command cannot pass.
- anchor: "tests/skills/test_workflow_archive.py tests/skills/test_task_workspace_lifecycle.py tests/skills/test_implement_adviser_family.py"

## Other findings

- L2 (MAJOR, open, single): The literal constraint forbids the tests, docs, plugins and .dev edits that nearly every task requires; the intended meaning is only 'do not edit .claude/'.

## Reviser brief

Blocking finding ids: L1, L3.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
