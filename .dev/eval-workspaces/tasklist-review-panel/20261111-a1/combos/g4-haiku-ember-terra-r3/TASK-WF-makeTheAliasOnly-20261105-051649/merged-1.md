review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/candidate.md sha256 cfd8f983d22ab8af1638ffb2a464215e56048f753f7902e3066435d8de176ca4
reviewers:
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/g4-haiku-ember-terra-r3/t4-1.md, block ok true
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/g4-haiku-ember-terra-r3/t2b-1.md, block ok true
- t2-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/g4-haiku-ember-terra-r3/t2-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | t2-1, t2b-1, t4-1 |
| L2 | open | yes | overlap | MAJOR | - | t2-1, t2b-1, t4-1 |
| L3 | open | no | overlap | MAJOR | - | t2b-1, t4-1 |
| L4 | open | no | single | MAJOR | - | t4-1 |
| L5 | open | no | single | MAJOR | - | t4-1 |
| L6 | open | no | single | MINOR | - | t4-1 |
| L7 | open | yes | single | MAJOR | - | t2-1 |

## Blocking findings

### L1

#### L1.t4-1 (F1)

- claim: The scratch copy under the package artifacts folder resolves REPO_ROOT to the package folder, so import models fails and the required AssertionError cannot occur.
- anchor: "copy the harness and the test into a scratch module under ./artifacts/t9-scratch/ with the harness addition applied"
- anchor2: "Task-owned evidence is written under ./artifacts/ in this package."

#### L1.t4-1 (F3)

- claim: The launcher already exports these variables with a [1m] suffix in tier mode, so the spec's premise and exact lines are wrong.
- anchor: "and that they run only when tier mode is on, so a launch that is not in tier mode leaves the inherited environment untouched"

#### L1.t4-1 (F4)

- claim: The quoted launcher line numbers point at argument parsing, not the tier-mode block.
- anchor: "the tier-mode block at lines 776-785, where the launcher also tests that CCSESSION_EXT_PROFILE is not 1 at line 777"

#### L1.t2b-1 (F2)

- claim: Line-number anchor for the launcher is stale relative to the current checkout; the named file and behaviour remain locatable so this is a note only.
- anchor: "the tier-mode block at lines 776-785"

#### L1.t2-1 (F3)

- claim: The specified unconditional exports override inherited aliases for tiers unavailable to the workspace owner, unlike the current launcher.
- anchor: "they run only when tier mode is on, so a launch that is not in tier mode leaves the inherited environment untouched"
- anchor2: "export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a, export ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b, export ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2"

### L2

#### L2.t4-1 (F2)

- claim: The stated allow-list omits cli/review/data, so the tier-text test fails on two tracked files and the remaining-tests-pass criterion cannot hold.
- anchor: "TIER_TEXT_ALLOWED (those three files, everything under src/superclaude/skills/sc-issue-protocol/, and src/superclaude/skills/ccsession-tag/ which is read-only here)"
- anchor2: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths."

#### L2.t2b-1 (F1)

- claim: The stated allow-list omits src/superclaude/cli/review/data/ which contains the tier text, so the tier-text test as written flags those files and cannot pass as the acceptance criteria require.
- anchor: "and TIER_TEXT_ALLOWED (those three files, everything under src/superclaude/skills/sc-issue-protocol/, and src/superclaude/skills/ccsession-tag/ which is read-only here)."

#### L2.t2-1 (F2)

- claim: Existing review configuration under the CLI contains tier IDs outside the specified allow-list, so the final policy check cannot pass under the planned changes.
- anchor: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths."

### L7

#### L7.t2-1 (F1)

- claim: The unchanged checkout already contains the fixes, so the required seven historical failure causes cannot all occur.
- anchor: "run on the unchanged tree fails exactly these seven tests"

## Other findings

- L3 (MAJOR, open, overlap): Removing the workaround before the launcher lands routes plain-session haiku proposals to glm-5.3.
- L4 (MAJOR, open, single): The reflect run default changes to the moving opus alias in non-tier sessions, and no consequence states it.
- L5 (MAJOR, open, single): The doc says nothing is set outside tier workspaces, but the defaults file exports real ids there.
- L6 (MINOR, open, single): The commands.md line anchors point at unrelated sections in this tree.

## Reviser brief

Blocking finding ids: L1, L2, L7.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
