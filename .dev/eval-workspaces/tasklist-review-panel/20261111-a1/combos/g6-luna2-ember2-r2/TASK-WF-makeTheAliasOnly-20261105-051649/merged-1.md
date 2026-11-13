review: 1 of 3
# Merged review 1 (coordinator script; panel of 4 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/candidate.md sha256 cfd8f983d22ab8af1638ffb2a464215e56048f753f7902e3066435d8de176ca4
reviewers:
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/g6-luna2-ember2-r2/t4-1.md, block ok true
- t4-2: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/g6-luna2-ember2-r2/t4-2.md, block ok false
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/g6-luna2-ember2-r2/t2b-1.md, block ok false
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/g6-luna2-ember2-r2/t3-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | t2b-1, t3-1, t4-1 |
| L2 | open | no | single | MAJOR | - | t4-1 |
| L3 | open | no | single | MAJOR | - | t4-2 |
| L4 | open | yes | single | MAJOR | - | t3-1 |

## Blocking findings

### L1

#### L1.t4-1 (F1)

- claim: An implementer who follows the stated text as written builds a launcher that preserves inherited tier IDs on non-tier launches, and that is wrong because the spec says outside a tier workspace nothing is set and aliases keep Claude Code’s meaning.
- anchor: "nothing set outside"
- anchor2: "so a launch that is not in tier mode leaves the inherited environment untouched"

#### L1.t2b-1 (F2)

- claim: Task 9 anchor line numbers do not match the current launcher file; re-verify is already required by the stated text.
- anchor: "the tier-mode block at lines 776-785, where the launcher also tests that CCSESSION_EXT_PROFILE is not 1 at line 777"

#### L1.t3-1 (F2)

- claim: Task 9 line anchors are stale in the current checkout (tier check is at line 883), though the re-verify instruction mitigates it.
- anchor: "the tier-mode block at lines 776-785, where the launcher also tests that CCSESSION_EXT_PROFILE is not 1 at line 777"

### L4

#### L4.t3-1 (F1)

- claim: Task 1's tier-text allow-list omits src/superclaude/cli/review/data/, which contains claude-gw-tier text, so the exact-seven red phase fails.
- anchor: "TIER_TEXT_ALLOWED (those three files, everything under src/superclaude/skills/sc-issue-protocol/, and src/superclaude/skills/ccsession-tag/ which is read-only here)."
- anchor2: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths."

## Other findings

- L2 (MAJOR, open, single): The candidate describes an underscore-name defect that is absent from the checked-out retry reference, so Task 5's rename and behavior-change note may be a no-op against this checkout.
- L3 (MAJOR, open, single): The reference page may conflate variables not set by the launcher with variables absent from the inherited environment, leaving readers with conflicting expectations outside tier workspaces.

## Reviser brief

Blocking finding ids: L1, L4.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
