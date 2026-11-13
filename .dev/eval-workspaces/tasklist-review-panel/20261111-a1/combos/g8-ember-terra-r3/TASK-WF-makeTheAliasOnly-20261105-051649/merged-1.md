review: 1 of 3
# Merged review 1 (coordinator script; panel of 2 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/candidate.md sha256 cfd8f983d22ab8af1638ffb2a464215e56048f753f7902e3066435d8de176ca4
reviewers:
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/g8-ember-terra-r3/t2b-1.md, block ok true
- t2-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/g8-ember-terra-r3/t2-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | t2-1, t2b-1 |
| L2 | open | no | single | MAJOR | - | t2b-1 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: The claude-gw-tier text test fails on cli/review/data JSON files outside TIER_TEXT_ALLOWED, so exactly seven failures and later passage cannot hold
- anchor: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths."
- anchor2: "tests/skills/test_model_alias_policy.py exists and `uv run pytest tests/skills/test_model_alias_policy.py` run on the unchanged tree fails exactly these seven tests"

#### L1.t2b-1 (F3)

- claim: ALIASES excludes fable while Task 6 treats fable as a valid model alias
- anchor: "Define ALIASES = opus, sonnet, haiku, inherit"
- anchor2: "the Agent-call model parameter takes only sonnet, opus, haiku and fable"

#### L1.t2-1 (F1)

- claim: The required seven-failure baseline cannot be reproduced because several specified failures are already fixed in the current checkout.
- anchor: "run on the unchanged tree fails exactly these seven tests"

#### L1.t2-1 (F2)

- claim: The tier-text test cannot pass with the specified allow-list because the current review configuration contains tier IDs outside it.
- anchor: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths."
- anchor2: "the remaining tests pass."

#### L1.t2-1 (F3)

- claim: The proposed follow-up omits the current launcher's per-tier availability checks and context suffixes, risking unavailable aliases for restricted owners.
- anchor: "the three export lines exactly (export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a"

#### L1.t2-1 (F4)

- claim: The documentation can be read as claiming inherited alias variables are absent outside tier mode although the launcher leaves them untouched.
- anchor: "outside one nothing is set and opus, sonnet and haiku keep Claude Code's meaning"
- anchor2: "a launch that is not in tier mode leaves the inherited environment untouched"

## Other findings

- L2 (MAJOR, open, single): The notes instruction counts four exported variables and omits T2Model01 while the task text exports five

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
