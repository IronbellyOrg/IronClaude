review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/candidate.md sha256 cfd8f983d22ab8af1638ffb2a464215e56048f753f7902e3066435d8de176ca4
reviewers:
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/n5-muse-glm-luna/t2b-1.md, block ok true
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/n5-muse-glm-luna/t3-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/n5-muse-glm-luna/t4-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | t2b-1, t3-1, t4-1 |
| L2 | open | yes | overlap | CRITICAL | - | t2b-1, t3-1 |
| L3 | open | no | single | MINOR | - | t2b-1 |
| L4 | open | yes | overlap | MAJOR | - | t3-1, t4-1 |
| L5 | open | no | single | MAJOR | - | t3-1 |
| L6 | open | no | single | MINOR | - | t3-1 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: The tier-text test as specified fails on pre-existing src/superclaude/cli/review/data/*.json tier files that no task fixes, so the exact-seven-red criterion and the final full-pass criterion cannot both pass.
- anchor: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths."
- anchor2: "TIER_TEXT_ALLOWED (those three files, everything under src/superclaude/skills/sc-issue-protocol/, and src/superclaude/skills/ccsession-tag/ which is read-only here)"

#### L1.t2b-1 (F4)

- claim: The pin list gives no per-file pairing, so a reader can map t1 to tier3 and t3 to tier1a, the reverse of the actual agent pins.
- anchor: "whose pinned values must equal claude-gw-tier3, claude-gw-tier2 and claude-gw-tier1a"

#### L1.t3-1 (F1)

- claim: The stated tier-text allow-list excludes the tracked files src/superclaude/cli/review/data/review-tiers.default.json and review-panel.live7.json, which contain claude-gw-tier, so the tier-text test fails on the tree and the Task 1 AC 'the remaining tests pass' cannot pass as written.
- anchor: "TIER_TEXT_ALLOWED (those three files, everything under src/superclaude/skills/sc-issue-protocol/, and src/superclaude/skills/ccsession-tag/ which is read-only here)"
- anchor2: "fails exactly these seven tests"

#### L1.t4-1 (F1)

- claim: The specified allow-list omits existing claude-gw-tier text under src/superclaude/cli/review/data/, so the required unchanged-tree run has an extra failing test.
- anchor: "TIER_TEXT_ALLOWED (those three files, everything under src/superclaude/skills/sc-issue-protocol/, and src/superclaude/skills/ccsession-tag/ which is read-only here)"

### L2

#### L2.t2b-1 (F2)

- claim: Outside tier mode the candidate simultaneously claims nothing is set and that inherited values (which the defaults file sets to real model ids) are untouched, so the prescribed reference text misstates how the aliases resolve outside a tier workspace.
- anchor: "outside one nothing is set and opus, sonnet and haiku keep Claude Code's meaning"
- anchor2: "they run only when tier mode is on, so a launch that is not in tier mode leaves the inherited environment untouched"

#### L2.t2b-1 (F3)

- claim: The launcher spec exports all three tier ids to every tier-mode user, so a limited owner gets opus remapped to tier1a they cannot use instead of keeping their inherited model as the touched launcher code requires.
- anchor: "export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a, export ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b, export ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2"
- anchor2: "and that they run only when tier mode is on, so a launch that is not in tier mode leaves the inherited environment untouched"

#### L2.t2b-1 (F5)

- claim: No relative link target is given, so the prescribed probe link can be written as a dead path under docs/reference/ and still pass Task 6 acceptance.
- anchor: "linking .dev/issues/384/analysis/probe-alias-remap.md"

#### L2.t3-1 (F5)

- claim: The launcher already exports the three variables in an access-aware form with [1m] suffixes at lines 896-898, so the follow-up spec's anchor and exact export lines no longer match the tree it names.
- anchor: "the three export lines exactly (export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a, export ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b, export ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2)"

### L4

#### L4.t3-1 (F2)

- claim: defaults.sh exports T3Model01=glm-5.3 (gpt-6.1-terra is T2bModel01), so the required t5-notes.md and the Task 6 reference page record a false workspace fact and a false model-family analysis (rung 0 is GLM, not GPT).
- anchor: "as /etc/aidev02/aienv.d/defaults.sh does: T3Model01 gpt-6.1-terra, T2Model02 glm-5.3, T1Model02 gpt-6.1-sol, T1Model01 claude-opus-5-5"
- anchor2: "rung 1 is a non-Claude model, rungs 0 and 2 are GPT models"

#### L4.t4-1 (F2)

- claim: The requested prose implies all five named variables are required for the primary ladder, contradicting the four-variable activation described in the task and the optional status of T2Model01.
- anchor: "the fallback ladder (haiku, sonnet, opus) applies when they are not all set"
- anchor2: "the primary ladder now replaces the alias fallback ladder"

## Other findings

- L3 (MINOR, open, single): The base directory for ./artifacts/ is unnamed, so evidence can land in the repo-root artifacts/ directory instead of the task package.
- L5 (MAJOR, open, single): Commit 70ef6486 does not exist in this repository and the prescribed git log -S command returns a different commit, so the plan's evidence citation cannot be verified as written (the edit direction itself is correct).
- L6 (MINOR, open, single): Tasks 2-4 and 7 pin bare line numbers without Task 9's base-commit qualifier; several have drifted, so implementers must match the quoted content rather than the numbers.

## Reviser brief

Blocking finding ids: L1, L2, L4.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
