review: 1 of 3
# Merged review 1 (coordinator script; panel of 5 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/candidate.md sha256 cfd8f983d22ab8af1638ffb2a464215e56048f753f7902e3066435d8de176ca4
reviewers:
- t2-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/h1-haiku-luna2-ember2-r1/t2-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/h1-haiku-luna2-ember2-r1/t4-1.md, block ok true
- t4-2: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/h1-haiku-luna2-ember2-r1/t4-2.md, block ok true
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/h1-haiku-luna2-ember2-r1/t2b-1.md, block ok true
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/h1-haiku-luna2-ember2-r1/t3-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | t2-1, t2b-1, t3-1 |
| L2 | open | no | single | MAJOR | - | t2-1 |
| L3 | open | yes | overlap | MAJOR | - | t2-1, t2b-1, t4-1, t4-2 |
| L4 | open | no | overlap | MAJOR | - | t2-1, t2b-1 |
| L5 | open | no | single | MAJOR | - | t3-1 |

## Blocking findings

### L1

#### L1.t2-1 (F1)

- claim: The tier-text rule as written fails on cli/review/data JSON files that contain claude-gw-tier1a, so the remaining-tests-pass criterion cannot be met.
- anchor: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths."
- anchor2: "the reflect default test, the D12 test and the claude-gw-tier text test pass"

#### L1.t2-1 (F3)

- claim: The pin mapping is listed in file order without per-file values, so a positional reading expects issue-worker-t1 to pin tier3, while it pins tier1a.
- anchor: "whose pinned values must equal claude-gw-tier3, claude-gw-tier2 and claude-gw-tier1a"

#### L1.t2b-1 (F1)

- claim: The claude-gw-tier text test fails on src/superclaude/cli/review/data/review-tiers.default.json, which is outside TIER_TEXT_ALLOWED and no task edits it, so the seven-test red list and Task 2's pass criterion cannot both hold.
- anchor: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths."
- anchor2: "the Python constants test, the reflect default test, the D12 test and the claude-gw-tier text test pass"

#### L1.t2b-1 (F4)

- claim: The ANTHROPIC_MODEL precedence use is at line 365 in this checkout, not about line 359.
- anchor: "about line 359"

#### L1.t3-1 (F1)

- claim: The tier-text test fails on src/superclaude/cli/review/data/ tier definitions, so the exact-seven count and the Task 2 acceptance cannot pass.
- anchor: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths."
- anchor2: "TIER_TEXT_ALLOWED (those three files, everything under src/superclaude/skills/sc-issue-protocol/, and src/superclaude/skills/ccsession-tag/ which is read-only here)"

#### L1.t3-1 (F3)

- claim: The residual allow-list wording could be read to allow-list the reflect default that must fail first.
- anchor: "A residual allow-list dict (path to reason) exists for any legitimate hit found when the test first runs."

### L3

#### L3.t2-1 (F4)

- claim: The launcher already exports these variables in tier mode with a [1m] suffix behind a usable-tier guard, so the unguarded exact lines conflict with it.
- anchor: "export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a"

#### L3.t2-1 (F5)

- claim: The cited line numbers point to unrelated code at this checkout, and the harness already records the three keys at lines 395-411.
- anchor: "The fake claude in that module records only a fixed set of keys (lines 330-341)"
- anchor2: "the tier-mode block at lines 776-785, where the launcher also tests that CCSESSION_EXT_PROFILE is not 1 at line 777"

#### L3.t4-1 (F1)

- claim: The specified line numbers do not identify the launcher sections the follow-up spec must quote, so its line-numbered anchor acceptance criterion cannot pass.
- anchor: "the tier-mode block at lines 776-785, where the launcher also tests that CCSESSION_EXT_PROFILE is not 1 at line 777, and the custom-option exports at lines 1099-1103"

#### L3.t4-2 (F1)

- claim: Clarify whether the outside-tier statement describes launcher behavior or guarantees the variables are unset, because Task 9 preserves inherited values.
- anchor: "outside one nothing is set and opus, sonnet and haiku keep Claude Code's meaning"
- anchor2: "a non-tier launch leaves them unset"

#### L3.t2b-1 (F2)

- claim: The cited ccsession and test lines do not match this checkout, and the fake claude already records the three alias keys, so the spec would quote wrong anchors and add duplicate keys; the base commit is not named.
- anchor: "The fake claude in that module records only a fixed set of keys (lines 330-341)"

## Other findings

- L2 (MAJOR, open, single): defaults.sh sets T3Model01 to glm-5.3, so rung 0 is not a GPT model and the notes would misstate the workspace.
- L4 (MAJOR, open, overlap): No base commit is named, and this checkout already contains the post-change text, so the red-run claim cannot be reproduced.
- L5 (MAJOR, open, single): The src-only constraint literally forbids the docs edits that later tasks require.

## Reviser brief

Blocking finding ids: L1, L3.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
