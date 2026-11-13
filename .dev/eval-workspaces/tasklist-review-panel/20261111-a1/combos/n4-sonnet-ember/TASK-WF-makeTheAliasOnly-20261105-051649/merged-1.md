review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/candidate.md sha256 cfd8f983d22ab8af1638ffb2a464215e56048f753f7902e3066435d8de176ca4
reviewers:
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/n4-sonnet-ember/t2b-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/n4-sonnet-ember/t4-1.md, block ok true
- t1b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/n4-sonnet-ember/t1b-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | t1b-1, t2b-1, t4-1 |
| L2 | open | yes | single | CRITICAL | - | t2b-1 |
| L3 | open | yes | overlap | CRITICAL | - | t1b-1, t2b-1, t4-1 |
| L4 | open | no | single | MAJOR | - | t2b-1 |
| L5 | open | no | single | MINOR | - | t4-1 |
| L6 | open | no | single | MINOR | - | t1b-1 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: Red-state criterion cannot pass: policy tests give 0 failures, not exactly 7.
- anchor: "fails exactly these seven tests: the Python constants test, the reflect default test, the D12 test, the chains test, the cleanup-audit test, the retry names test and the mapping document test"

#### L1.t2b-1 (F2)

- claim: Stated tier-text rule fails on cli/review/data JSONs outside the allow-list, contradicting the seven-failure count.
- anchor: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths."

#### L1.t4-1 (F1)

- claim: The tier-text rule fails on cli/review/data/review-tiers.default.json, which is outside TIER_TEXT_ALLOWED and is not edited by any task, so the seven-failure red list and Task 2's pass criterion cannot both hold.
- anchor: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths."
- anchor2: "run on the unchanged tree fails exactly these seven tests"

#### L1.t4-1 (F2)

- claim: On HEAD 8c93e1d Tasks 2 to 6 are already applied, so the listed red tests would pass there; the candidate never names the base commit.
- anchor: "run on the unchanged tree fails exactly these seven tests"

#### L1.t4-1 (F6)

- claim: The retry test omits T2Model01, which Task 5 renames and lists as a ladder variable.
- anchor: "retry.md names the primary-ladder variables T3Model01, T2Model02, T1Model02 and T1Model01"

#### L1.t1b-1 (F1)

- claim: The claude-gw-tier text test, as stated, fails on src/superclaude/cli/review/data/review-tiers.default.json and review-panel.live7.json, which are outside TIER_TEXT_ALLOWED and edited by no task, so the Task 1, Task 2 and Task 8 criteria that need it to pass cannot be met.
- anchor: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths."
- anchor2: "the remaining tests pass."

#### L1.t1b-1 (M2)

- claim: The values are listed without a file mapping, and in constraint order (t1, t2, t3) a pairing would be wrong; the real pins are t1=tier1a, t2=tier2, t3=tier3.
- anchor: "whose pinned values must equal claude-gw-tier3, claude-gw-tier2 and claude-gw-tier1a"

### L2

#### L2.t2b-1 (F3)

- claim: Stated edit target is absent: reflect default is already opus at line 37 with the required comment.
- anchor: "change `_DEFAULT_MODEL = \"claude-opus-4-8\"` (line 31) to `\"opus\"`"

### L3

#### L3.t2b-1 (F4)

- claim: Cited anchor is profile parsing; the launcher already exports tier values with a context suffix at line 896.
- anchor: "the tier-mode block at lines 776-785, where the launcher also tests that CCSESSION_EXT_PROFILE is not 1 at line 777"

#### L3.t4-1 (F3)

- claim: The instruction to create a file that already exists and is tracked would overwrite the existing spec instead of updating it.
- anchor: "Create .dev/issues/384/launcher-followup.md, the exact spec of the separate launcher pull request"

#### L3.t4-1 (F4)

- claim: The quoted line numbers point at the --profile parser on HEAD, not the tier-mode block at 880-885, and the harness line numbers are wrong too, so the spec would quote the wrong code.
- anchor: "the tier-mode block at lines 776-785, where the launcher also tests that CCSESSION_EXT_PROFILE is not 1 at line 777"

#### L3.t1b-1 (M1)

- claim: The spec exports all three tier ids in tier mode with no owner-usable-tier rule, so an owner without tier1a gets opus mapped to a tier they cannot use.
- anchor: "and that they run only when tier mode is on, so a launch that is not in tier mode leaves the inherited environment untouched"

## Other findings

- L4 (MAJOR, open, single): Tasks 3 to 6 replay edits already present on this tree.
- L5 (MINOR, open, single): The sk- pattern matches ordinary words such as task- and risk-, so a correct document can fail its acceptance grep.
- L6 (MINOR, open, single): Read literally this forbids the docs/, tests/ and .dev/ edits that tasks require; it means only do not edit .claude/.

## Reviser brief

Blocking finding ids: L1, L2, L3.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
