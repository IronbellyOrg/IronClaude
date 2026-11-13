review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/candidate.md sha256 cfd8f983d22ab8af1638ffb2a464215e56048f753f7902e3066435d8de176ca4
reviewers:
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/g4-haiku-ember-terra-r4/t4-1.md, block ok true
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/g4-haiku-ember-terra-r4/t2b-1.md, block ok true
- t2-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/g4-haiku-ember-terra-r4/t2-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | t2-1, t4-1 |
| L2 | open | yes | overlap | MAJOR | - | t2-1, t4-1 |
| L3 | open | no | single | MINOR | - | t4-1 |
| L4 | open | no | single | MAJOR | - | t4-1 |

## Blocking findings

### L1

#### L1.t4-1 (F1)

- claim: The tier-text rule fails on review-tiers.default.json (6 hits) and review-panel.live7.json (1 hit), which are outside TIER_TEXT_ALLOWED, so the test cannot pass as the plan says.
- anchor: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths."
- anchor2: "the remaining tests pass"

#### L1.t4-1 (F2)

- claim: On this checkout the reflect default (commands.py:37), D12 line 235, retry names, chains, cleanup-audit and model-aliases.md already show the target state, so the seven-failure red log cannot be produced.
- anchor: "run on the unchanged tree fails exactly these seven tests: the Python constants test, the reflect default test"

#### L1.t4-1 (F3)

- claim: Following the Create instruction overwrites the existing 63-line model-aliases.md and the existing policy test file, losing content the plan does not record.
- anchor: "Create docs/reference/model-aliases.md and add a row for it to the"
- anchor2: "Create tests/skills/test_model_alias_policy.py"

#### L1.t4-1 (F8)

- claim: The pattern sk- also matches task- and risk-, so a page naming task-builder fails the check although it holds no secret.
- anchor: "`grep -nE \"sk-|token=\" docs/reference/model-aliases.md` returns nothing"

#### L1.t2-1 (F1)

- claim: The seven specified failures cannot occur for their stated reasons because the checkout already contains several requested fixes and the policy test.
- anchor: "run on the unchanged tree fails exactly these seven tests"

#### L1.t2-1 (F2)

- claim: The required tier-text test fails on existing review-panel configuration excluded from the specified allow-list.
- anchor: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths."
- anchor2: "the remaining tests pass"

### L2

#### L2.t4-1 (F4)

- claim: Lines 776-785 are --profile parsing, the real tier block is at 882-898, the launcher already exports the three variables with a [1m] suffix at 896-898, and the 1099-1103 exports are Python code, so the exact lines drop the suffix and the red test fails for a different reason.
- anchor: "the tier-mode block at lines 776-785, where the launcher also tests that CCSESSION_EXT_PROFILE is not 1 at line 777"
- anchor2: "the three export lines exactly (export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a"

#### L2.t4-1 (F5)

- claim: The fake claude is at lines 389-411 and already records the three ANTHROPIC_DEFAULT keys at 408-410, and the environment copies are at 429, 850 and 1417, so the proposed json.dump addition would duplicate existing keys.
- anchor: "The fake claude in that module records only a fixed set of keys (lines 330-341)"
- anchor2: "the harness copies os.environ at line 359"

#### L2.t2-1 (F3)

- claim: The follow-up describes exports as absent and unconditional although the launcher already exports suffixed values subject to owner-tier access checks.
- anchor: "the three export lines exactly"
- anchor2: "Run the test: copy the harness and the test into a scratch module"

## Other findings

- L3 (MINOR, open, single): commands.md lines 845-860 contain no brainstorm model text and developer guide line 411 is a frontmatter fence, so both anchors point at the wrong text.
- L4 (MAJOR, open, single): defaults.sh line 57 sets T3Model01 to glm-5.3, so rung 0 is not GPT and the notes sentence that rungs 0 and 2 are GPT models is false.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
