review: 1 of 3
# Merged review 1 (coordinator script; panel of 4 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/candidate.md sha256 cfd8f983d22ab8af1638ffb2a464215e56048f753f7902e3066435d8de176ca4
reviewers:
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/n4-sol/t2b-1.md, block ok false
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/n4-sol/t3-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/n4-sol/t4-1.md, block ok true
- t2-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/n4-sol/t2-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | t2b-1, t3-1, t4-1 |
| L2 | open | no | single | MAJOR | - | t2b-1 |
| L3 | open | yes | overlap | MAJOR | - | t3-1, t4-1 |
| L4 | open | no | single | MINOR | - | t3-1 |
| L5 | open | no | overlap | MAJOR | - | t3-1, t4-1 |
| L6 | open | no | single | MINOR | - | t3-1 |

## Blocking findings

### L1

#### L1.t2b-1 (F3)

- claim: The allow-list values are not tied to individual files, so the per-file pin mapping must be guessed.
- anchor: "ISSUE_WORKER_PINS (the three issue-worker agent files, whose pinned values must equal claude-gw-tier3, claude-gw-tier2 and claude-gw-tier1a"

#### L1.t3-1 (F1)

- claim: The enumerated allow-list omits src/superclaude/cli/review/data/ where claude-gw-tier text exists, so the tier-text test fails on the unchanged tree and Task 1's 'the remaining tests pass' and Task 2's tier-text criterion cannot pass.
- anchor: "TIER_TEXT_ALLOWED (those three files, everything under src/superclaude/skills/sc-issue-protocol/, and src/superclaude/skills/ccsession-tag/ which is read-only here)"
- anchor2: "the D12 test and the claude-gw-tier text test pass"

#### L1.t4-1 (F1)

- claim: An implementer who follows the stated allow-list builds a policy test that flags src/superclaude/cli/review/data JSON files containing claude-gw-tier, and X is wrong because no task edits or allow-lists them, so Task 8 cannot pass.
- anchor: "TIER_TEXT_ALLOWED (those three files, everything under src/superclaude/skills/sc-issue-protocol/, and src/superclaude/skills/ccsession-tag/ which is read-only here)"
- anchor2: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths."

#### L1.t4-1 (F3)

- claim: The red-first premise is not reproducible: the file is already tracked and passes 13 of 13, and no base commit is named.
- anchor: "Create tests/skills/test_model_alias_policy.py (ROOT = Path(__file__).resolve().parents[2]"
- anchor2: "run on the unchanged tree fails exactly these seven tests"

#### L1.t4-1 (F7)

- claim: The allow-list may be extended after the first red run with no reason required beforehand, which weakens the gate.
- anchor: "A residual allow-list dict (path to reason) exists for any legitimate hit found when the test first runs."

### L3

#### L3.t3-1 (F2)

- claim: Task 5 prescribes t5-notes.md content built on a wrong value: defaults.sh line 59 exports T3Model01=glm-5.3 (gpt-6.1-terra is T2bModel01), so the notes would record a false rung composition and the wrong adviser-family outcome.
- anchor: "T3Model01 gpt-6.1-terra, T2Model02 glm-5.3, T1Model02 gpt-6.1-sol, T1Model01 claude-opus-5-5"
- anchor2: "rung 1 is a non-Claude model, rungs 0 and 2 are GPT models"

#### L3.t4-1 (F2)

- claim: The stated workspace value for T3Model01 is wrong (defaults.sh line 59 sets glm-5.3), so rung 0 is not GPT and the notes would record a false fact.
- anchor: "T3Model01 gpt-6.1-terra, T2Model02 glm-5.3, T1Model02 gpt-6.1-sol, T1Model01 claude-opus-5-5"
- anchor2: "rungs 0 and 2 are GPT models"

#### L3.t4-1 (F4)

- claim: Several cited lines are stale and several edits are already applied, so the acceptance checks pass without any change.
- anchor: "change the RUNGS entries (lines 774-777) and the tier value in _rt (line 786)"

## Other findings

- L2 (MAJOR, open, single): The constraint forbids edits outside src/ that Tasks 2-9 explicitly require in docs/, tests/, plugins/ and .dev/issues/.
- L4 (MINOR, open, single): The cited commit is not verifiable in this snapshot; the git log -S command returns a different commit here.
- L5 (MAJOR, open, overlap): Task 9's launcher and harness line anchors have drifted from the current file; the quoted content matches and the plan itself requires re-verification after #315 merges.
- L6 (MINOR, open, single): Task 7's pre-edit line references have drifted; the content anchors are correct and the edits land on the right text.

## Reviser brief

Blocking finding ids: L1, L3.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
