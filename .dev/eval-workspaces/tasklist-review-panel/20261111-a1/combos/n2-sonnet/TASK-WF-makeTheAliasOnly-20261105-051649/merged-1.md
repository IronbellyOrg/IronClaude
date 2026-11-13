review: 1 of 3
# Merged review 1 (coordinator script; panel of 4 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/candidate.md sha256 cfd8f983d22ab8af1638ffb2a464215e56048f753f7902e3066435d8de176ca4
reviewers:
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/n2-sonnet/t2b-1.md, block ok false
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/n2-sonnet/t4-1.md, block ok true
- t4-2: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/n2-sonnet/t4-2.md, block ok true
- t1b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/n2-sonnet/t1b-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | t1b-1, t2b-1, t4-1, t4-2 |
| L2 | open | yes | overlap | CRITICAL | - | t1b-1, t2b-1, t4-1, t4-2 |
| L3 | open | no | single | MAJOR | - | t1b-1 |

## Blocking findings

### L1

#### L1.t2b-1 (F2)

- claim: The quoted anchor and harness lines name unrelated code and the fake claude already records the three alias variables, so the launcher spec and its red scratch test are built on the wrong code.
- anchor: "the tier-mode block at lines 776-785, where the launcher also tests that CCSESSION_EXT_PROFILE is not 1 at line 777"
- anchor2: "The fake claude in that module records only a fixed set of keys (lines 330-341)"

#### L1.t2b-1 (F3)

- claim: Blanket bare exports give every tier-mode owner all three tiers and drop the [1m] suffix, regressing per-owner tier access and the values the current launcher tests pin.
- anchor: "export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a, export ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b, export ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2"
- anchor2: "they run only when tier mode is on, so a launch that is not in tier mode leaves the inherited environment untouched"

#### L1.t2b-1 (F5)

- claim: Calling Task 8's acceptance-tested tests optional lets an implementer read them as skippable.
- anchor: "These tests are an optional guard beyond the four listed spec items; keep them small."

#### L1.t4-1 (F5)

- claim: The checkout's launcher already exports the variables with a [1m] suffix at lines 883-898, so the spec's exact lines and anchors would drop the suffix and point at the wrong lines.
- anchor: "export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a"
- anchor2: "the tier-mode block at lines 776-785"

#### L1.t4-2 (F2)

- claim: The follow-up spec points at the wrong lines and at bare tier ids for every tier-mode launch, while the launcher already exports the [1m] ids only for tiers the owner may use.
- anchor: "the tier-mode block at lines 776-785, where the launcher also tests that CCSESSION_EXT_PROFILE is not 1 at line 777, and the custom-option exports at lines 1099-1103"
- anchor2: "export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a, export ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b, export ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2"

#### L1.t1b-1 (F2)

- claim: The exports are unconditional in tier mode, but Members may use only Tiers 2 to 4, so their opus and sonnet aliases would point at tiers they cannot use.
- anchor: "and that they run only when tier mode is on, so a launch that is not in tier mode leaves the inherited environment untouched"

#### L1.t1b-1 (F4)

- claim: Task 8 depends only on the chain through Tasks 7, 6, 5 and 1, though its criterion needs Tasks 2, 3 and 4 done.
- anchor: "passes in full (all tests green after Tasks 2 to 7)"
- anchor2: "Depends on: Task 7"

### L2

#### L2.t2b-1 (F4)

- claim: The plan says both that nothing is set outside a tier workspace and that the workspace defaults file exports real model ids for the same variables.
- anchor: "outside one nothing is set and opus, sonnet and haiku keep Claude Code's meaning"
- anchor2: "today the workspace defaults file exports real model ids for them"

#### L2.t4-1 (F1)

- claim: The claude-gw-tier test fails on src/superclaude/cli/review/data/review-tiers.default.json and review-panel.live7.json, which the allow-list does not cover and no task changes, so Task 2's acceptance cannot pass.
- anchor: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths."
- anchor2: "the D12 test and the claude-gw-tier text test pass"

#### L2.t4-1 (F2)

- claim: Following the literal constraint means no tests/ or docs/ edits, so the test file and the doc edits that the tasks require are never made.
- anchor: "Edit under src/ only; the .claude/ copies are gitignored sync output regenerated by make sync-dev."
- anchor2: "Create tests/skills/test_model_alias_policy.py"

#### L2.t4-1 (F3)

- claim: Positional pairing maps issue-worker-t1 to tier3 and t3 to tier1a, but the files pin t1 to tier1a and t3 to tier3.
- anchor: "whose pinned values must equal claude-gw-tier3, claude-gw-tier2 and claude-gw-tier1a"

#### L2.t4-1 (F4)

- claim: Removing the workaround sends brainstorm haiku proposals to glm-5.3 on this workspace before the launcher change, and the note wrongly says aliases keep Claude Code's meaning here.
- anchor: "outside one they keep Claude Code's meaning"
- anchor2: "Drop the haiku workaround from the issue chains"

#### L2.t4-1 (F6)

- claim: No base commit is named and the checkout already has the Task 2, 3, 5 and 7 edits, so the red list cannot be reproduced.
- anchor: "run on the unchanged tree fails exactly these seven tests"

#### L2.t4-1 (F7)

- claim: The retry-names test omits T2Model01, which Task 5 renames.
- anchor: "retry.md names the primary-ladder variables T3Model01, T2Model02, T1Model02 and T1Model01"

#### L2.t4-1 (F8)

- claim: The stray backtick makes the model-flag regex ambiguous to implement.
- anchor: "matched by `--models?[ =]+`?claude-(opus|sonnet|haiku|fable)-\\d`"

#### L2.t4-2 (F1)

- claim: The Task 1 bar cannot be met: the seven named tests already pass on this tree, and the tier-text test fails because cli/review/data contains claude-gw-tier and is outside the stated allow-list.
- anchor: "the cleanup-audit test, the retry names test and the mapping document test; the remaining tests pass."
- anchor2: "TIER_TEXT_ALLOWED (those three files, everything under src/superclaude/skills/sc-issue-protocol/, and src/superclaude/skills/ccsession-tag/ which is read-only here)"

#### L2.t1b-1 (F1)

- claim: Two JSON files under src/superclaude/cli/review/data contain claude-gw-tier and are not in TIER_TEXT_ALLOWED, so the tier-text test stays red and the criteria that need it green cannot pass.
- anchor: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths."
- anchor2: "the remaining tests pass"

#### L2.t1b-1 (F5)

- claim: The pin is removed before the launcher sets the mapping, so until the later pull request lands haiku proposals run on the non-Claude model D25 excluded, and Known consequences does not say so.
- anchor: "remove ` --models opus,sonnet` from the three brainstorm steps"

#### L2.t1b-1 (F6)

- claim: The pin values are listed in the reverse of the file order t1, t2, t3, which would fail the frontmatter test if read in order.
- anchor: "whose pinned values must equal claude-gw-tier3, claude-gw-tier2 and claude-gw-tier1a"

#### L2.t1b-1 (F7)

- claim: The pattern sk- also matches words such as risk- and task-, so the check could fail on ordinary prose.
- anchor: "`grep -nE \"sk-|token=\" docs/reference/model-aliases.md`"

## Other findings

- L3 (MAJOR, open, single): defaults.sh release 20261110-1 sets T3Model01 to glm-5.3, so the notes would call rung 0 a GPT model wrongly, and rungs 0 and 1 share an id with no tie rule.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
