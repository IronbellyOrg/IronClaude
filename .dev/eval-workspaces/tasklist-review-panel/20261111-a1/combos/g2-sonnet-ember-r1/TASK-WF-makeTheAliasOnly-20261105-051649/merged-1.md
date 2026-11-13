review: 1 of 3
# Merged review 1 (coordinator script; panel of 2 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/candidate.md sha256 cfd8f983d22ab8af1638ffb2a464215e56048f753f7902e3066435d8de176ca4
reviewers:
- t1b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/g2-sonnet-ember-r1/t1b-1.md, block ok true
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/g2-sonnet-ember-r1/t2b-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | MAJOR | M-1 | t1b-1 |
| L2 | open | no | overlap | MAJOR | - | t1b-1, t2b-1 |
| L3 | open | no | overlap | MAJOR | - | t1b-1, t2b-1 |
| L4 | open | no | overlap | MAJOR | - | t1b-1, t2b-1 |
| L5 | open | no | single | MINOR | - | t1b-1 |
| L6 | open | no | single | MINOR | - | t1b-1 |
| L7 | open | no | single | MAJOR | - | t2b-1 |
| L8 | open | no | single | MINOR | - | t2b-1 |

## Blocking findings

### L1

#### L1.t1b-1 (F1)

- claim: The tier-text test as written fails on the unchanged tree because src/superclaude/cli/review/data/*.json contain claude-gw-tier and are not allow-listed, so the Task 1 and Task 2 acceptance criteria cannot pass.
- anchor: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths."
- anchor2: "everything under src/superclaude/skills/sc-issue-protocol/, and src/superclaude/skills/ccsession-tag/ which is read-only here"

## Other findings

- L2 (MAJOR, open, overlap): The pin order does not say which file gets which id, and a positional reading gives issue-worker-t1 the id claude-gw-tier3 when it is claude-gw-tier1a.
- L3 (MAJOR, open, overlap): The harness resolves the launcher through parents[2] of its own file, so the scratch copy misses the launcher unless REPO_ROOT is repointed, which the spec never states.
- L4 (MAJOR, open, overlap): The test needs literal NAME=value strings while Task 6 describes a table with variable and id as separate items, so a compliant table can fail the test.
- L5 (MINOR, open, single): Read literally, edit under src/ only contradicts the tasks that edit tests/, docs/, .dev/ and plugins/.
- L6 (MINOR, open, single): An installed primitive points at a docs/ path that is not installed to ~/.claude, so the pointer is dead outside a checkout.
- L7 (MAJOR, open, single): Open-ended sweep lacks a rule for history and exempt machinery.
- L8 (MINOR, open, single): Slot count reads as five in one place and four in another.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
