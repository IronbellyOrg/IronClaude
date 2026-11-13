review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/candidate.md sha256 cfd8f983d22ab8af1638ffb2a464215e56048f753f7902e3066435d8de176ca4
reviewers:
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/g5-ember2-luna-r3/t2b-1.md, block ok true
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/g5-ember2-luna-r3/t3-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/g5-ember2-luna-r3/t4-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | t2b-1, t3-1, t4-1 |
| L2 | open | no | single | MAJOR | - | t2b-1 |
| L3 | open | no | overlap | MAJOR | - | t2b-1, t3-1 |
| L4 | open | no | single | MAJOR | - | t3-1 |
| L5 | open | no | single | MAJOR | - | t3-1 |
| L6 | open | no | single | MINOR | - | t3-1 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: Policy test as written fails on cli/review/data tier text, so seven-failure and final full-pass acceptances cannot both pass.
- anchor: "and TIER_TEXT_ALLOWED (those three files, everything under src/superclaude/skills/sc-issue-protocol/, and src/superclaude/skills/ccsession-tag/ which is read-only here)"
- anchor2: "- The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths."

#### L1.t2b-1 (F4)

- claim: Residual allow-list phrasing is too open and could be read to hide the required reflect failure.
- anchor: "A residual allow-list dict (path to reason) exists for any legitimate hit found when the test first runs"

#### L1.t3-1 (F1)

- claim: Pinned values are listed without per-file mapping, so file-order assignment is ambiguous.
- anchor: "whose pinned values must equal claude-gw-tier3, claude-gw-tier2 and claude-gw-tier1a"

#### L1.t4-1 (F1)

- claim: The listed file order and value order can be read as assigning tier3 to issue-worker-t1 and tier1a to issue-worker-t3, contrary to the existing mapping.
- anchor: "the three issue-worker agent files, whose pinned values must equal claude-gw-tier3, claude-gw-tier2 and claude-gw-tier1a"

## Other findings

- L2 (MAJOR, open, single): Capital-only Haiku check can pass while docs still say lowercase haiku for a sonnet-pinned agent.
- L3 (MAJOR, open, overlap): Mandated t5-notes model values do not match current defaults.sh exports.
- L4 (MAJOR, open, single): Scratch harness launcher path resolution from artifacts is unspecified.
- L5 (MAJOR, open, single): Open-ended docs search has no closed acceptance list.
- L6 (MINOR, open, single): Line-number anchors are not pinned to a base commit.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
