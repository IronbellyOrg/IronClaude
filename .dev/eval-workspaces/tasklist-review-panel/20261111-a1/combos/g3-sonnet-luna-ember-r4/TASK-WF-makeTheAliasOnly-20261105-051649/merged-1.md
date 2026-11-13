review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/candidate.md sha256 cfd8f983d22ab8af1638ffb2a464215e56048f753f7902e3066435d8de176ca4
reviewers:
- t1b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/g3-sonnet-luna-ember-r4/t1b-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/g3-sonnet-luna-ember-r4/t4-1.md, block ok true
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/g3-sonnet-luna-ember-r4/t2b-1.md, block ok false

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | MAJOR | - | t1b-1 |
| L2 | open | no | overlap | MAJOR | - | t1b-1, t2b-1 |
| L3 | open | yes | overlap | CRITICAL | - | t1b-1, t2b-1, t4-1 |
| L4 | open | no | overlap | MAJOR | - | t1b-1, t2b-1 |
| L5 | open | no | single | MINOR | - | t1b-1 |
| L6 | open | yes | single | MAJOR | - | t4-1 |
| L7 | open | yes | single | CRITICAL | - | t2b-1 |

## Blocking findings

### L1

#### L1.t1b-1 (F1)

- claim: src/superclaude/cli/review/data/review-tiers.default.json and review-panel.live7.json contain claude-gw-tier and are outside the stated allow-list, so the test fails on the unchanged tree and the Task 2 and Task 8 pass criteria cannot be met.
- anchor: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths."
- anchor2: "TIER_TEXT_ALLOWED (those three files, everything under src/superclaude/skills/sc-issue-protocol/, and src/superclaude/skills/ccsession-tag/ which is read-only here)"

#### L1.t1b-1 (F2)

- claim: The value order is the reverse of the t1, t2, t3 file order, so a positional reading pairs issue-worker-t1 with tier3 while the real pin is tier1a.
- anchor: "whose pinned values must equal claude-gw-tier3, claude-gw-tier2 and claude-gw-tier1a"

### L3

#### L3.t1b-1 (F4)

- claim: The harness derives REPO_ROOT from its own file location, so a copy in the artifacts folder fails on import models, not the AssertionError the criterion requires, unless the paths are repointed.
- anchor: "copy the harness and the test into a scratch module under ./artifacts/t9-scratch/ with the harness addition applied"

#### L3.t4-1 (F2)

- claim: The current fake Claude harness already records the three alias variables, making the specified harness addition redundant.
- anchor: "states the exact `json.dump` lines to add to capture ANTHROPIC_DEFAULT_OPUS_MODEL"

#### L3.t2b-1 (F2)

- claim: The stated launcher anchor is wrong: lines 776-785 are --profile parsing and the real tier-mode block is at lines 883-898, so the quoted-anchor acceptance criterion cannot pass as written.
- anchor: "the tier-mode block at lines 776-785, where the launcher also tests that CCSESSION_EXT_PROFILE is not 1 at line 777"

### L6

#### L6.t4-1 (F1)

- claim: The unchanged-tree policy test run passes all 13 tests on this checkout, so the required seven failures cannot be produced.
- anchor: "run on the unchanged tree fails exactly these seven tests"

### L7

#### L7.t2b-1 (F3)

- claim: The stated test-harness lines are wrong: tests/unit/test_ccsession_tiers.py lines 330-341 and 359 are not the fake-claude recorder or the os.environ copy, so the scratch-test acceptance criterion cannot be built as written.
- anchor: "the fake claude in that module records only a fixed set of keys (lines 330-341)"

## Other findings

- L2 (MAJOR, open, overlap): The constraint says edit under src/ only, but Tasks 2 to 9 edit docs/, tests/, plugins/ and .dev/.
- L4 (MAJOR, open, overlap): The notes present values of a mutable machine file as current; today's file has T3Model01=glm-5.3, so the stated rung families no longer hold.
- L5 (MINOR, open, single): The D12 source note on that line cites commands.py line numbers that drift when the _DEFAULT_MODEL comment is rewritten.

## Reviser brief

Blocking finding ids: L1, L3, L6, L7.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
