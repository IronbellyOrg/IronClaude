review: 1 of 3
# Merged review 1 (coordinator script; panel of 4 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/candidate.md sha256 cfd8f983d22ab8af1638ffb2a464215e56048f753f7902e3066435d8de176ca4
reviewers:
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/r2-sonnet-src/t4-1.md, block ok true
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/r2-sonnet-src/t3-1.md, block ok true
- t4-2: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/r2-sonnet-src/t4-2.md, block ok true
- t1b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/r2-sonnet-src/t1b-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | t1b-1, t3-1, t4-1, t4-2 |
| L2 | open | yes | overlap | MAJOR | - | t1b-1, t3-1, t4-1 |
| L3 | open | no | single | MAJOR | - | t3-1 |
| L4 | open | no | single | MINOR | M-23, M-6 | t1b-1 |

## Blocking findings

### L1

#### L1.t4-1 (F1)

- claim: The text scan covers src/superclaude/cli, where review-tiers.default.json and review-panel.live7.json carry claude-gw-tier outside the allow-list, so the test fails and the Task 2 pass criterion cannot be met.
- anchor: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths."
- anchor2: "the Python constants test, the reflect default test, the D12 test and the claude-gw-tier text test pass"

#### L1.t4-1 (F3)

- claim: No base commit is named, commit 70ef6486 is absent from this repository, and the Task 1 to 7 changes are already present on this checkout, so the red-test list and line anchors cannot be reproduced here.
- anchor: "quoted with its line numbers at this branch's base commit"
- anchor2: "commit 70ef6486 replaced haiku defaults with sonnet"

#### L1.t4-1 (F4)

- claim: The launcher already exports the three variables at lines 896 to 898 with a [1m] suffix and a per-tier gate, so the spec's unsuffixed unconditional exports would override that gate.
- anchor: "the tier-mode block at lines 776-785, where the launcher also tests that CCSESSION_EXT_PROFILE is not 1 at line 777"
- anchor2: "export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a"

#### L1.t4-1 (F5)

- claim: The values are listed in the order tier3, tier2, tier1a against files listed as t1, t2, t3, but the actual pins are t1 to tier1a, t2 to tier2 and t3 to tier3, so a positional check pins the wrong ids.
- anchor: "whose pinned values must equal claude-gw-tier3, claude-gw-tier2 and claude-gw-tier1a"

#### L1.t4-1 (F6)

- claim: The code span closes early, so the trailing question mark sits outside the pattern and an implementer cannot tell whether it is part of the regex.
- anchor: "matched by `--models?[ =]+`?claude-(opus|sonnet|haiku|fable)"

#### L1.t4-1 (F7)

- claim: The reflect default run in a tier workspace now follows the alias target instead of the pinned claude-opus-4-8, and Known consequences does not state this change.
- anchor: "reflect reviewer diversity counts the three variable values"
- anchor2: "In src/superclaude/cli/reflect/commands.py change"

#### L1.t3-1 (F1)

- claim: The tier-text scan over cli also flags src/superclaude/cli/review/data JSON files that no task edits or allow-lists, so the test is an eighth red test and the seven-red acceptance cannot pass.
- anchor: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths."
- anchor2: "fails exactly these seven tests: the Python constants test, the reflect default test"

#### L1.t3-1 (F2)

- claim: Pairing of the three issue-worker files to tier values is unstated; file order pairs t1 with tier3, but t1 pins claude-gw-tier1a, t2 pins claude-gw-tier2 and t3 pins claude-gw-tier3.
- anchor: "whose pinned values must equal claude-gw-tier3, claude-gw-tier2 and claude-gw-tier1a"

#### L1.t3-1 (F3)

- claim: No base commit is named, and on this checkout the reflect default, D12, chains, retry, cleanup-audit and model-aliases target states already exist, so the stated red set and the Create instruction for an existing file cannot be checked.
- anchor: "run on the unchanged tree fails exactly these seven tests:"
- anchor2: "Create tests/skills/test_model_alias_policy.py (ROOT = Path(__file__).resolve().parents[2]"

#### L1.t3-1 (F4)

- claim: On this checkout the tier-mode block is at ccsession lines 880-886 and the harness already records the three variables at test_ccsession_tiers.py lines 399-410, so the quoted anchors and harness addition do not match.
- anchor: "the tier-mode block at lines 776-785, where the launcher also tests that CCSESSION_EXT_PROFILE is not 1 at line 777"

#### L1.t3-1 (F6)

- claim: Non-tier reflect runs change from a pinned model id to whatever Claude Code's opus alias resolves to, and Known consequences does not list this.
- anchor: "change `_DEFAULT_MODEL = \"claude-opus-4-8\"` (line 31) to `\"opus\"`"

#### L1.t3-1 (F7)

- claim: The regex sits in a code span with an embedded backtick, so the pattern can be copied inexactly.
- anchor: "`--models?[ =]+`?claude-(opus|sonnet|haiku|fable)-\\d`"

#### L1.t4-2 (F1)

- claim: Those seven checks already pass on this tree, so the required red run cannot fail exactly those tests.
- anchor: "fails exactly these seven tests: the Python constants test, the reflect default test, the D12 test, the chains test, the cleanup-audit test, the retry names test and the mapping document test"

#### L1.t4-2 (F2)

- claim: cli/review/data contains claude-gw-tier and is outside that allow-list, so the tier-text test fails at Task 1 and is still failing when Task 8 requires a full pass.
- anchor: "TIER_TEXT_ALLOWED (those three files, everything under src/superclaude/skills/sc-issue-protocol/, and src/superclaude/skills/ccsession-tag/ which is read-only here)"
- anchor2: "`uv run pytest tests/skills/test_model_alias_policy.py` passes in full (all tests green after Tasks 2 to 7)"

#### L1.t4-2 (F3)

- claim: Zipping the file list with that value list swaps t1 and t3, which neither the agent files nor tiers.md does.
- anchor: "whose pinned values must equal claude-gw-tier3, claude-gw-tier2 and claude-gw-tier1a"
- anchor2: "issue-worker-t1.md, issue-worker-t2.md, issue-worker-t3.md"

#### L1.t4-2 (F4)

- claim: Those lines are not the tier-mode block, and the launcher already exports the three variables with a [1m] suffix only for tiers the owner may use.
- anchor: "the tier-mode block at lines 776-785, where the launcher also tests that CCSESSION_EXT_PROFILE is not 1 at line 777"
- anchor2: "export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a, export ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b, export ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2"

#### L1.t1b-1 (F1)

- claim: The tier-text test scans all of src/superclaude/cli but allows no path for the two review data JSON files that contain claude-gw-tier, so it fails on the unchanged tree and the 'remaining tests pass' and 'passes in full' criteria cannot pass.
- anchor: "TIER_TEXT_ALLOWED (those three files, everything under src/superclaude/skills/sc-issue-protocol/, and src/superclaude/skills/ccsession-tag/ which is read-only here)"
- anchor2: "fails exactly these seven tests: the Python constants test, the reflect default test, the D12 test"

#### L1.t1b-1 (F2)

- claim: Unconditional exports map opus to claude-gw-tier1a even for an owner whose tier rules forbid that tier, which breaks helper agents for limited owners.
- anchor: "they run only when tier mode is on, so a launch that is not in tier mode leaves the inherited environment untouched"

#### L1.t1b-1 (F3)

- claim: The harness derives REPO_ROOT from its own file location, so a verbatim copy cannot import models and fails with an import error instead of the required AssertionError.
- anchor: "copy the harness and the test into a scratch module under ./artifacts/t9-scratch/ with the harness addition applied"

### L2

#### L2.t4-1 (F2)

- claim: defaults.sh exports T3Model01 as glm-5.3 at line 59, so rung 0 is not a GPT model and the notes would record a false workspace fact and a false adviser-selection effect.
- anchor: "as /etc/aidev02/aienv.d/defaults.sh does: T3Model01 gpt-6.1-terra, T2Model02 glm-5.3, T1Model02 gpt-6.1-sol, T1Model01 claude-opus-5-5"
- anchor2: "rung 1 is a non-Claude model, rungs 0 and 2 are GPT models"

#### L2.t3-1 (F8)

- claim: Source.md also lists the T1aModel01/02 and T1bModel01-03 exports, which the note omits.
- anchor: "The workspace exports T3Model01, T2Model01, T2Model02, T1Model01 and T1Model02 (no underscore)"

#### L2.t1b-1 (F5)

- claim: The prescribed t5-notes values no longer match defaults.sh release 20261110-1 (T3Model01 is now glm-5.3), so the notes would state a false rung layout if written today.
- anchor: "T3Model01 gpt-6.1-terra, T2Model02 glm-5.3, T1Model02 gpt-6.1-sol, T1Model01 claude-opus-5-5"

## Other findings

- L3 (MAJOR, open, single): commands.md lines 849 and 859 hold validate-tests examples and the workflow heading, and no brainstorm model-selection text exists, so the pointer has no target.
- L4 (MINOR, open, single): The markdown scan only catches model-flag uses, not full model ids elsewhere in markdown body text that the source asked to cover.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
