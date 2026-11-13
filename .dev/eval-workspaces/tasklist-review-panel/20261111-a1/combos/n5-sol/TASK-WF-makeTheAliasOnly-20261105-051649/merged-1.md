review: 1 of 3
# Merged review 1 (coordinator script; panel of 4 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/candidate.md sha256 cfd8f983d22ab8af1638ffb2a464215e56048f753f7902e3066435d8de176ca4
reviewers:
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/n5-sol/t2b-1.md, block ok true
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/n5-sol/t3-1.md, block ok false
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/n5-sol/t4-1.md, block ok true
- t2-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/n5-sol/t2-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | t2b-1, t4-1 |
| L2 | open | yes | overlap | CRITICAL | - | t2b-1, t4-1 |
| L3 | open | no | overlap | MAJOR | - | t2b-1, t3-1 |
| L4 | open | no | single | MINOR | - | t2b-1 |
| L5 | open | no | single | MINOR | - | t2b-1 |
| L6 | open | no | single | MINOR | - | t3-1 |
| L7 | open | no | single | MINOR | - | t3-1 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: The tier-text test scans src/superclaude/cli but the allow-list omits cli/review/data, whose JSON files contain claude-gw-tier by design, so the exactly-seven-failures acceptance and the final full pass can never hold.
- anchor: "TIER_TEXT_ALLOWED (those three files, everything under src/superclaude/skills/sc-issue-protocol/, and src/superclaude/skills/ccsession-tag/ which is read-only here)"
- anchor2: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths."

#### L1.t4-1 (F1)

- claim: The specified text scan finds existing CLI review tier data outside TIER_TEXT_ALLOWED, so the required red run has more than seven failures.
- anchor: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths."

### L2

#### L2.t2b-1 (F2)

- claim: Exporting all three plain tier ids in every tier-mode launch overwrites inherited values for tiers an owner may not use and drops the [1m] suffix, contradicting the launcher's owner tier-access behaviour and its pinned tier-launch tests.
- anchor: "the three export lines exactly (export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a, export ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b, export ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2)"
- anchor2: "and that they run only when tier mode is on, so a launch that is not in tier mode leaves the inherited environment untouched"

#### L2.t4-1 (F2)

- claim: The follow-up does not explicitly preserve per-owner tier access checks when setting aliases, so an implementation may expose a tier the owner cannot use.
- anchor: "and that they run only when tier mode is on, so a launch that is not in tier mode leaves the inherited environment untouched"

## Other findings

- L3 (MAJOR, open, overlap): The ordered notes record T3Model01 as gpt-6.1-terra and rung 0 as a GPT model, but the workspace defaults on disk export T3Model01=glm-5.3, so the record would be false.
- L4 (MINOR, open, single): The search-and-fix order and the keep-the-comment exception pull in opposite directions for the discover_components.py comment.
- L5 (MINOR, open, single): Written as a relative link from docs/reference/, this path does not resolve to an existing file.
- L6 (MINOR, open, single): Several exact line anchors (test_issue_protocol.py 268-282, sc-issue-command.md ~442, commands.md ~849/859, developer guide 411, RUNGS 774-777) have drifted from the current file layout; all edit targets are still findable by name, so this is friction only.
- L7 (MINOR, open, single): The 'four listed spec items' are never listed in the candidate, so the intended scope of the optional guard is not recoverable from the document.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
