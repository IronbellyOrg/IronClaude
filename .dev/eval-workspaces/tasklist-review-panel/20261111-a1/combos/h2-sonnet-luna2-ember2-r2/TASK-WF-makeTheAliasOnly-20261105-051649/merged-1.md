review: 1 of 3
# Merged review 1 (coordinator script; panel of 5 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/candidate.md sha256 cfd8f983d22ab8af1638ffb2a464215e56048f753f7902e3066435d8de176ca4
reviewers:
- t1b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/h2-sonnet-luna2-ember2-r2/t1b-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/h2-sonnet-luna2-ember2-r2/t4-1.md, block ok false
- t4-2: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/h2-sonnet-luna2-ember2-r2/t4-2.md, block ok true
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/h2-sonnet-luna2-ember2-r2/t2b-1.md, block ok true
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/h2-sonnet-luna2-ember2-r2/t3-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | t1b-1, t2b-1, t3-1, t4-1 |
| L2 | open | yes | overlap | CRITICAL | - | t1b-1, t2b-1, t3-1, t4-1, t4-2 |
| L3 | open | yes | overlap | MAJOR | - | t1b-1, t3-1 |
| L4 | open | no | single | MINOR | - | t1b-1 |
| L5 | open | no | overlap | MINOR | - | t2b-1, t3-1 |

## Blocking findings

### L1

#### L1.t1b-1 (F2)

- claim: The launcher spec exports tier1a, tier1b and tier2 for every tier-mode launch and never says to skip a tier the owner may not use or that is not defined, though the launcher already enforces that access rule.
- anchor: "and that they run only when tier mode is on, so a launch that is not in tier mode leaves the inherited environment untouched"

#### L1.t1b-1 (F6)

- claim: The copied module derives REPO_ROOT from its own location, so the scratch run fails on a missing launcher path instead of the required AssertionError unless REPO_ROOT is set explicitly.
- anchor: "copy the harness and the test into a scratch module under ./artifacts/t9-scratch/ with the harness addition applied"

#### L1.t4-1 (F3)

- claim: The required launcher anchors point to profile parsing and model-request code rather than the tier-mode check and custom-option exports, so the required quoted anchors are wrong.
- anchor: "the tier-mode block at lines 776-785, where the launcher also tests that CCSESSION_EXT_PROFILE is not 1 at line 777"
- anchor2: "the custom-option exports at lines 1099-1103"

#### L1.t2b-1 (F2)

- claim: Task 9 line anchors for the launcher block, custom exports, fake claude and env copy do not match the current files, so a scratch module copied by line number does not reproduce the stated AssertionError failure.
- anchor: "the tier-mode block at lines 776-785, where the launcher also tests that CCSESSION_EXT_PROFILE is not 1 at line 777, and the custom-option exports at lines 1099-1103"

#### L1.t2b-1 (F3)

- claim: Candidate states the alias mapping unconditionally in tier mode and never states the owner-usable-tier condition the launcher actually applies.
- anchor: "and that they run only when tier mode is on, so a launch that is not in tier mode leaves the inherited environment untouched"

#### L1.t3-1 (F3)

- claim: Unconditional launcher spec regresses the tested per-tier usable-gate exports
- anchor: "the tier-mode block at lines 776-785"
- anchor2: "export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a"

### L2

#### L2.t1b-1 (F3)

- claim: The tier-text test has no residual allow-list, and the repo has JSON files under src/superclaude/cli/review/data/ that contain claude-gw-tier, so the test can fail on the unchanged tree.
- anchor: "TIER_TEXT_ALLOWED (those three files, everything under src/superclaude/skills/sc-issue-protocol/, and src/superclaude/skills/ccsession-tag/ which is read-only here)"
- anchor2: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths."

#### L2.t1b-1 (F8)

- claim: Pairing the values by position with the t1, t2, t3 file order gives t1 the tier3 pin, which is wrong; the pairs are not named.
- anchor: "whose pinned values must equal claude-gw-tier3, claude-gw-tier2 and claude-gw-tier1a"

#### L2.t1b-1 (F1)

- claim: Read literally, the constraint forbids the tests, docs and plugin-mirror edits the tasks require, though its second sentence shows it only means not to edit .claude/.
- anchor: "Edit under src/ only; the .claude/ copies are gitignored sync output regenerated by make sync-dev."
- anchor2: "Create tests/skills/test_model_alias_policy.py"

#### L2.t4-1 (F1)

- claim: The tier-text test will flag existing review-data files, so the required unchanged-tree run cannot have exactly seven failures with all remaining tests passing.
- anchor: "TIER_TEXT_ALLOWED (those three files, everything under src/superclaude/skills/sc-issue-protocol/, and src/superclaude/skills/ccsession-tag/ which is read-only here)"

#### L2.t4-2 (F1)

- claim: The specified tier-text allow-list omits existing CLI review data containing claude-gw-tier, so the required policy test cannot pass.
- anchor: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths."

#### L2.t2b-1 (F1)

- claim: Tier-text test built from the stated allow-list fails on cli/review/data json files, so the exactly-seven-failures and final-green acceptance criteria cannot pass.
- anchor: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths."

#### L2.t2b-1 (F4)

- claim: Issue-worker pin values are listed without a per-file mapping, leaving t1/t2/t3 assignment ambiguous.
- anchor: "whose pinned values must equal claude-gw-tier3, claude-gw-tier2 and claude-gw-tier1a"

#### L2.t3-1 (F1)

- claim: Tier-text test fails permanently on cli/review/data hits with no fixing task
- anchor: "and TIER_TEXT_ALLOWED (those three files, everything under src/superclaude/skills/sc-issue-protocol/, and src/superclaude/skills/ccsession-tag/ which is read-only here)"
- anchor2: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths."

### L3

#### L3.t1b-1 (F4)

- claim: In a Coder workspace outside tier mode the inherited defaults-file exports still apply, so the page's statement that nothing is set is wrong for that case.
- anchor: "outside one nothing is set and opus, sonnet and haiku keep Claude Code's meaning"
- anchor2: "until then the workspace defaults file exports real model ids for the three variables"

#### L3.t1b-1 (F5)

- claim: A column-style mapping table would not contain the NAME=id strings the Task 1 test requires, so the mapping document test can fail.
- anchor: "the three exports spelled exactly as in the mapping table"
- anchor2: "states the three exports with the exact ids ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a"

#### L3.t3-1 (F2)

- claim: Seven expected red failures cannot occur on the already-fixed tree
- anchor: "fails exactly these seven tests: the Python constants test, the reflect default test, the D12 test, the chains test, the cleanup-audit test, the retry names test and the mapping document test"

#### L3.t3-1 (F4)

- claim: Mapping page omits per-tier usability gate and 1m suffix
- anchor: "opus to claude-gw-tier1a via ANTHROPIC_DEFAULT_OPUS_MODEL, sonnet to claude-gw-tier1b via ANTHROPIC_DEFAULT_SONNET_MODEL, haiku to claude-gw-tier2 via ANTHROPIC_DEFAULT_HAIKU_MODEL"

## Other findings

- L4 (MINOR, open, single): The notes state defaults-file values without a file version, and the current defaults release (20261112-1) has a different T3Model01 (glm-5.3).
- L5 (MINOR, open, overlap): Several cited line numbers no longer match the current checkout, though the named strings remain findable.

## Reviser brief

Blocking finding ids: L1, L2, L3.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
