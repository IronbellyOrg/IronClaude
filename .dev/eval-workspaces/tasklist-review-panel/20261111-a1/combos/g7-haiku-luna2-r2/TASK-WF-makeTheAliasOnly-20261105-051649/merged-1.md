review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/candidate.md sha256 cfd8f983d22ab8af1638ffb2a464215e56048f753f7902e3066435d8de176ca4
reviewers:
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/g7-haiku-luna2-r2/t4-1.md, block ok true
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/g7-haiku-luna2-r2/t3-1.md, block ok true
- t4-2: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/g7-haiku-luna2-r2/t4-2.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | MAJOR | - | t4-1 |
| L2 | open | yes | overlap | MAJOR | - | t3-1, t4-1, t4-2 |
| L3 | open | no | single | MAJOR | - | t4-1 |
| L4 | open | no | single | MAJOR | - | t4-1 |
| L5 | open | yes | overlap | MAJOR | - | t4-1, t4-2 |
| L6 | open | no | single | MINOR | - | t4-1 |

## Blocking findings

### L1

#### L1.t4-1 (F1)

- claim: On this checkout five of the seven named failing tests already pass, so the required seven-failure red run cannot be produced.
- anchor: "run on the unchanged tree fails exactly these seven tests"

### L2

#### L2.t4-1 (F2)

- claim: The rule read literally fails on src/superclaude/cli/review/data/review-tiers.default.json, which lists claude-gw-tier ids outside any allowed path, so the claimed passing tier-text test cannot pass.
- anchor: "appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths"
- anchor2: "TIER_TEXT_ALLOWED (those three files, everything under src/superclaude/skills/sc-issue-protocol/"

#### L2.t4-1 (F7)

- claim: ccsession:896-898 already exports tier ids with a [1m] suffix in tier workspaces, so the statement that only the defaults file sets them is wrong and the spec's exact exports would conflict.
- anchor: "until then the workspace defaults file exports real model ids for the three variables"

#### L2.t4-1 (F9)

- claim: Both files already exist, so a literal create overwrites them and the implementer must guess between updating and replacing.
- anchor: "Create docs/reference/model-aliases.md and add a row for it"
- anchor2: "Create tests/skills/test_model_alias_policy.py"

#### L2.t4-1 (F12)

- claim: tiers.md:21 records the same subagent docs as read 2026-11-04, so the two read dates disagree.
- anchor: "read 2026-11-05"

#### L2.t3-1 (F1)

- claim: The specified allow-list excludes src/superclaude/cli/review/data/review-tiers.default.json, so the required tier-text test flags an existing review-tier configuration that panel.py loads.
- anchor: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths."
- anchor2: "TIER_TEXT_ALLOWED (those three files, everything under src/superclaude/skills/sc-issue-protocol/, and src/superclaude/skills/ccsession-tag/ which is read-only here)."

#### L2.t4-2 (F2)

- claim: The document is required to say variables are unset outside tier workspaces while also stating that the defaults file currently exports model IDs for those variables.
- anchor: "outside one nothing is set and opus, sonnet and haiku keep Claude Code's meaning"
- anchor2: "until then the workspace defaults file exports real model ids for the three variables"

### L5

#### L5.t4-1 (F6)

- claim: Those lines are --profile parsing and a models fetch; the tier-mode check is at ccsession:883-886 and the exports at 896-898, so the spec points the edit at the wrong place.
- anchor: "the tier-mode block at lines 776-785, where the launcher also tests that CCSESSION_EXT_PROFILE is not 1 at line 777"
- anchor2: "the custom-option exports at lines 1099-1103"

#### L5.t4-1 (F8)

- claim: The fake claude writes its keys at tests/unit/test_ccsession_tiers.py:399-411; lines 330-341 are refresh-cache tests, so the harness addition is placed wrongly.
- anchor: "The fake claude in that module records only a fixed set of keys (lines 330-341)"

#### L5.t4-2 (F1)

- claim: The follow-up spec is directed to anchor the tier-mode block at lines that currently identify argument parsing instead.
- anchor: "the tier-mode block at lines 776-785, where the launcher also tests that CCSESSION_EXT_PROFILE is not 1 at line 777"

## Other findings

- L3 (MAJOR, open, single): The underscore names are not in the tree: retry.md already names the exported slots and RUNGS already uses T2Model02, so the rename and the activation note describe a change that is absent.
- L4 (MAJOR, open, single): That claim is absent from tiers.md, which already carries the new haiku wording, so the edit has no target.
- L6 (MINOR, open, single): _DEFAULT_MODEL is at commands.py:37, not line 31 as stated.

## Reviser brief

Blocking finding ids: L1, L2, L5.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
