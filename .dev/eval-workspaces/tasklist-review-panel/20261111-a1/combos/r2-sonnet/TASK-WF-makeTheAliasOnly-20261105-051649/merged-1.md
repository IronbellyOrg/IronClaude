review: 1 of 3
# Merged review 1 (coordinator script; panel of 4 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/candidate.md sha256 cfd8f983d22ab8af1638ffb2a464215e56048f753f7902e3066435d8de176ca4
reviewers:
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/r2-sonnet/t4-1.md, block ok true
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/r2-sonnet/t3-1.md, block ok true
- t4-2: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/r2-sonnet/t4-2.md, block ok true
- t1b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/r2-sonnet/t1b-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | t3-1, t4-1, t4-2 |
| L2 | open | yes | overlap | MAJOR | - | t1b-1, t3-1, t4-1, t4-2 |
| L3 | open | no | overlap | MAJOR | - | t4-1, t4-2 |
| L4 | open | yes | overlap | MAJOR | - | t1b-1, t3-1, t4-1, t4-2 |
| L5 | open | no | single | MINOR | - | t1b-1 |
| L6 | open | no | single | MINOR | - | t1b-1 |

## Blocking findings

### L1

#### L1.t4-1 (F1)

- claim: On this checkout the policy test file already passes 13 of 13, so the required seven-failure red run cannot happen.
- anchor: "fails exactly these seven tests: the Python constants test, the reflect default test, the D12 test"

#### L1.t3-1 (M1)

- claim: On this checkout the reflect default, D12, chains, cleanup-audit and retry tests already pass, so the stated red list holds only for an unnamed base commit.
- anchor: "fails exactly these seven tests: the Python constants test, the reflect default test, the D12 test, the chains test"

#### L1.t4-2 (F2)

- claim: On this tree those seven tests pass because each named defect is already fixed, so the required red run cannot happen.
- anchor: "fails exactly these seven tests: the Python constants test, the reflect default test, the D12 test, the chains test, the cleanup-audit test, the retry names test and the mapping document test"

### L2

#### L2.t4-1 (F2)

- claim: Lines 776-785 are the --profile branch, which runs only when that flag is passed, so the exports would never run in a default tier launch, breaking the spec's own tier-mode rule.
- anchor: "the tier-mode block at lines 776-785, where the launcher also tests that CCSESSION_EXT_PROFILE is not 1 at line 777"

#### L2.t4-1 (F3)

- claim: The launcher already exports these variables with a [1m] suffix for usable tiers, so the unsuffixed spec lines duplicate and conflict with it, and the red run fails for the suffix rather than the missing change.
- anchor: "export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a"

#### L2.t4-1 (F4)

- claim: Lines 330-341 are unrelated shim and cache tests; the fake claude is at lines 392-402, so the stated location sends the harness edit to the wrong test.
- anchor: "The fake claude in that module records only a fixed set of keys (lines 330-341)"

#### L2.t3-1 (M2)

- claim: On this checkout lines 776-785 of the ccsession launcher are the --profile argument parser, and the fake claude helper is not at lines 330-341 of tests/unit/test_ccsession_tiers.py.
- anchor: "the tier-mode block at lines 776-785, where the launcher also tests that CCSESSION_EXT_PROFILE is not 1 at line 777"

#### L2.t3-1 (M3)

- claim: An implementer who reads the unset variables by direct indexing gets a KeyError, which the acceptance forbids, because the candidate never says to use get.
- anchor: "the exact `json.dump` lines to add to capture ANTHROPIC_DEFAULT_OPUS_MODEL"

#### L2.t4-2 (F3)

- claim: The quoted line numbers are profile parsing, a cache test, and cache-fetch Python, not the tier-mode block or the fake claude recorder.
- anchor: "the tier-mode block at lines 776-785, where the launcher also tests that CCSESSION_EXT_PROFILE is not 1 at line 777"
- anchor2: "the fake claude in that module records only a fixed set of keys (lines 330-341)"

#### L2.t4-2 (F5)

- claim: The follow-up exports bare ids for every tier-mode launch, but the launcher exports suffixed ids only for tiers the owner may use.
- anchor: "export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a, export ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b, export ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2"

#### L2.t1b-1 (F1)

- claim: Exports are unconditional in tier mode, so an owner limited to some tiers gets alias variables pointing at tiers that owner cannot use; the document never states a per-tier access check.
- anchor: "they run only when tier mode is on, so a launch that is not in tier mode leaves the inherited environment untouched"

#### L2.t1b-1 (F2)

- claim: The harness derives REPO_ROOT from its own file path; the scratch copy needs that path repointed or collection fails with an import error instead of the required AssertionError.
- anchor: "copy the harness and the test into a scratch module under ./artifacts/t9-scratch/ with the harness addition applied"

### L4

#### L4.t4-1 (F6)

- claim: The sk- pattern also matches ordinary hyphenated words such as task-builder, which already appears in docs/reference/nfr-conv-2-prose-determinism.md, so the acceptance can fail on prose.
- anchor: "grep -nE \"sk-|token=\" docs/reference/model-aliases.md"

#### L4.t4-1 (F7)

- claim: The pattern sits inside a code span whose backtick closes it early, so the regex an implementer types is ambiguous.
- anchor: "--models?[ =]+`?claude-(opus|sonnet|haiku|fable)-\\d"

#### L4.t4-1 (F9)

- claim: The rule does not say which file types are scanned, and a literal all-files scan flags cli/review/data JSON files that no task edits.
- anchor: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths"

#### L4.t3-1 (F1)

- claim: The tier-text rule fails on src/superclaude/cli/review/data/review-panel.live7.json and review-tiers.default.json, which no task edits or allows, so the remaining-tests-pass and Task 2 tier-text acceptance cannot hold.
- anchor: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths."
- anchor2: "TIER_TEXT_ALLOWED (those three files, everything under src/superclaude/skills/sc-issue-protocol/, and src/superclaude/skills/ccsession-tag/ which is read-only here)"

#### L4.t3-1 (M4)

- claim: Read by list position, the pins map t1 to tier3 and t3 to tier1a, which is wrong; the files actually pin tier1a, tier2 and tier3 respectively.
- anchor: "whose pinned values must equal claude-gw-tier3, claude-gw-tier2 and claude-gw-tier1a"

#### L4.t3-1 (N1)

- claim: The sk- pattern also matches substrings such as task- and risk-, so an ordinary mapping page can fail the check.
- anchor: "`grep -nE \"sk-|token=\" docs/reference/model-aliases.md` returns nothing"

#### L4.t4-2 (F1)

- claim: The tier-text test fails on cli/review/data JSON files that no task allow-lists, so the policy file cannot pass in full.
- anchor: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths."
- anchor2: "TIER_TEXT_ALLOWED (those three files, everything under src/superclaude/skills/sc-issue-protocol/, and src/superclaude/skills/ccsession-tag/ which is read-only here)"

#### L4.t4-2 (F6)

- claim: A non-tier launch inherits real model ids from defaults.sh, so the aliases do not keep Claude Code's built-in meaning.
- anchor: "outside one nothing is set and opus, sonnet and haiku keep Claude Code's meaning"
- anchor2: "today the workspace defaults file exports real model ids for them"

#### L4.t1b-1 (F5)

- claim: Only Task 5 names the mirror step; the other editing tasks leave the check to the implementer.
- anchor: "Where an edited src/superclaude file has a byte-identical copy under plugins/superclaude/, copy the edited file over that mirror so both stay identical."

#### L4.t1b-1 (F6)

- claim: Read positionally, the value order maps t1 to tier3, but issue-worker-t1.md pins claude-gw-tier1a.
- anchor: "whose pinned values must equal claude-gw-tier3, claude-gw-tier2 and claude-gw-tier1a"
- anchor2: "The three issue-worker agents (src/superclaude/agents/issue-worker-t1.md, issue-worker-t2.md, issue-worker-t3.md)"

#### L4.t1b-1 (F7)

- claim: Read literally, this forbids the docs, tests, plugins and .dev edits that the tasks require.
- anchor: "Edit under src/ only; the .claude/ copies are gitignored sync output"

## Other findings

- L3 (MAJOR, open, overlap): Stale line numbers point at unrelated code: RUNGS is at lines 798-806, the brainstorm test at line 653, and the ledger token at line 204.
- L5 (MINOR, open, single): The values quoted for the workspace defaults file differ from the file on disk now (T3Model01=glm-5.3), so the notes' rung-by-rung claim would not match it.
- L6 (MINOR, open, single): If JSON files under src/superclaude/cli contain claude-gw-tier at the base and the scan covers them, the tier-text test fails on the unchanged tree, so 'exactly seven fail' would not hold.

## Reviser brief

Blocking finding ids: L1, L2, L4.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
