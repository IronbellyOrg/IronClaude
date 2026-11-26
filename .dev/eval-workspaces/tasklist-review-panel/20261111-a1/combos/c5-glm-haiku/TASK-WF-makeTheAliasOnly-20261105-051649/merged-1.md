review: 1 of 3
# Merged review 1 (coordinator script; panel of 2 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/candidate.md sha256 cfd8f983d22ab8af1638ffb2a464215e56048f753f7902e3066435d8de176ca4
reviewers:
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/c5-glm-haiku/t3-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/c5-glm-haiku/t4-1.md.catfix.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | t3-1, t4-1 |
| L2 | open | no | overlap | MAJOR | - | t3-1, t4-1 |
| L3 | open | no | overlap | MAJOR | - | t3-1, t4-1 |
| L4 | open | yes | single | MAJOR | - | t4-1 |
| L5 | open | no | single | MAJOR | - | t4-1 |
| L6 | open | no | single | MINOR | - | t4-1 |

## Blocking findings

### L1

#### L1.t3-1 (F1)

- claim: The stated tier-text allow-list omits the tracked claude-gw-tier JSON under src/superclaude/cli/review/data/, so the tier-text test is an eighth failing test and the 'fails exactly these seven tests' red AC cannot hold as written; the executed test adds an allow-list entry the plan never states.
- anchor: "TIER_TEXT_ALLOWED (those three files, everything under src/superclaude/skills/sc-issue-protocol/, and src/superclaude/skills/ccsession-tag/ which is read-only here)"

#### L1.t4-1 (F1)

- claim: The claude-gw-tier text test cannot pass as specified: cli/review/data/review-tiers.default.json and review-panel.live7.json hold that text, lie outside TIER_TEXT_ALLOWED, and no task edits them, so the Task 1 exactly-seven-failures acceptance and the Task 2 text-test acceptance fail.
- anchor: "The text claude-gw-tier appears under src/superclaude/agents, commands, skills, cli, hooks and core only in TIER_TEXT_ALLOWED paths."
- anchor2: "the claude-gw-tier text test pass"

#### L1.t4-1 (F7)

- claim: Changing the reflect default to the opus alias silently changes the model for every non-tier user, because the alias no longer pins claude-opus-4-8, and the Known consequences section does not list it.
- anchor: "In src/superclaude/cli/reflect/commands.py change"
- anchor2: "a Known consequences section"

#### L1.t4-1 (F8)

- claim: The model-flag pattern is ambiguous because its inner backtick ends the code span, so a test built from it may or may not allow a backtick before the model id.
- anchor: "matched by `--models?[ =]+`?claude-(opus|sonnet|haiku|fable)-"

#### L1.t4-1 (F10)

- claim: The ANTHROPIC_MODEL fallback is at reflect commands.py line 365 on this checkout, not about line 359; the hedge keeps this a note.
- anchor: "about line 359"

### L4

#### L4.t4-1 (F2)

- claim: The scratch run cannot produce the required AssertionError: a copy under the task package makes REPO_ROOT the package folder, so SKILL_DIR points at a missing launcher folder and the run errors before any assertion.
- anchor: "copy the harness and the test into a scratch module under ./artifacts/t9-scratch/ with the harness addition applied"
- anchor2: "shows the scratch test failing with an AssertionError on the three variable values"

#### L4.t4-1 (F3)

- claim: The stated launcher export lines duplicate or conflict with ccsession lines 896-898, which already export these variables inside the usable-tier check with the [1m] suffix, and the spec does not say which version wins.
- anchor: "export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a"
- anchor2: "they run only when tier mode is on"

#### L4.t4-1 (F4)

- claim: The spec line anchors point at the wrong code on this checkout: the tier-mode check is at ccsession line 883, lines 1099-1103 are Python, and the fake claude is at test_ccsession_tiers.py lines 389-410, so following them edits unrelated lines.
- anchor: "the tier-mode block at lines 776-785"
- anchor2: "records only a fixed set of keys (lines 330-341)"

## Other findings

- L2 (MAJOR, open, overlap): Task 5's t5-notes spec misstates the workspace facts: /etc/aidev02/aienv.d/defaults.sh exports T3Model01=glm-5.3 (gpt-6.1-terra is T2bModel01), so the recorded 'rungs 0 and 2 are GPT models' is false for rung 0.
- L3 (MAJOR, open, overlap): Several cited line anchors (developer guide 411, commands.md 849/859, ccsession 776-785) do not match the current files; targets remain findable from the quoted text, so this is re-location cost only.
- L5 (MAJOR, open, single): The document never names its base commit, and on this checkout at least five of the seven failures it says will go red already pass, so the red-run evidence cannot be reproduced here.
- L6 (MINOR, open, single): The commit 70ef6486 cited as proof does not exist in this checkout, so the stated git check cannot be reproduced; the pin itself is correct.

## Reviser brief

Blocking finding ids: L1, L4.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
