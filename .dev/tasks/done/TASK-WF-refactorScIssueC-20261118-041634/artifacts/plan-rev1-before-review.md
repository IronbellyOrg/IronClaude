---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-refactorScIssueC-20261118-041634
version: "1"
priority: Medium
created_date: "2026-11-18"
---

# Refactor /sc:issue --claim: plan the simple feature directly, default to full for a person

Source: ./source.md
Goal: A person who types `/sc:issue --claim <N>` with no `--pipeline` gets level `full`, the simple feature chain no longer starts with `/sc:brainstorm`, and the issue watcher still claims with its explicit `--pipeline none`.

## Constraints

- Edit only source files: `src/superclaude/...`, `tests/...`, `docs/...` and the one mirror file `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`. Never edit or stage anything under `.claude/`; Task 10 regenerates those copies with `make sync-dev`.
- The default level applies to a bare `--claim`. The issue watcher always passes `--pipeline none` (`build_claim_prompt` in `src/superclaude/cli/issue_watch/launch.py`, pinned by `tests/issue_watch/test_launch.py`). Do not edit either file and do not add any human-versus-agent detection.
- `src/superclaude/commands/issue.md` must never contain the text `src/superclaude/` (a test forbids it).
- Leave the ship-gate sentences (OB-H1, OB-H2, OB-H3) and the `--pipeline none` coordinator-handoff paragraph exactly as written. The worktree `claim-handoff-planb` edits the same files (`issue.md`, `SKILL.md`, `refs/claim.md`, `HOW-WE-WORK.md`), so keep every edit narrow and rebase onto `origin/master` before any pull request.
- Out of scope: `/tech-research`, `/task-builder` and `/task` handling, the complex bug row, model tiers, `orca_worktree.py`, and every other chain row.

## Phase 1: Simple feature chain without brainstorm

## Task 1: Replace the Feature, simple row in the chain table

In `src/superclaude/skills/sc-issue-protocol/refs/chains.md`, change only the table row that starts `| Feature, simple |`. Keep its tier line `/model claude-gw-tier2`. Replace its chain cell with two steps in the row's existing `<br>` style: the first runs `/sc:workflow <S> --depth quick --handoff none` (`<S>` is the issue-summary path the file already defines), the second runs `/sc:implement <plan path printed by step 1>`. Under `Notes:` add one bullet saying the simple feature row has no brainstorm step because the issue summary already states the requirements, so it plans directly from it. Leave the other five rows and the paragraph about handoff flags unchanged.

Acceptance criteria:
- The `Feature, simple` row contains no `/sc:brainstorm` and exactly the two commands above; the other five rows are byte-identical to before.
- Because the first `/sc:implement` step is now step 2, the plan boundary for this row is `after step 1`, and the file's own rule for `Plan boundary` still reads correctly.
- Every flag in the new commands exists in the workflow and implement command files, so `test_every_chain_flag_exists_in_its_command` in `tests/skills/test_issue_protocol.py` still passes.

## Task 2: Update the chain tests for the new simple feature row

Depends on: Task 1

In `tests/skills/test_issue_protocol.py`, change `test_brainstorm_steps_have_no_handoff_and_use_default_models` so it expects 2 brainstorm steps across the 6 rows (it asserts 3 today). Add a new test next to it that finds the `Feature, simple` row of `src/superclaude/skills/sc-issue-protocol/refs/chains.md` and asserts it has no `/sc:brainstorm`, contains `/sc:workflow <S> --depth quick --handoff none` and contains `/sc:implement <plan path printed by step 1>`.

Acceptance criteria:
- `uv run pytest tests/skills/test_issue_protocol.py -v` passes.
- Restoring the old brainstorm step into the row makes the new test and the 2-step count fail.

## Phase 2: Default level full in the command and the protocol

## Task 3: Make full the default level in the command file

In `src/superclaude/commands/issue.md` make these narrow edits. In the paragraph that lists the levels (line 16), move "(the default)" from `worktree` to `full`. In the Options table, set the `--pipeline` row default to `` `full` `` and add "Omitted means `full`." to its meaning; leave its values cell as `worktree`, `full`, `none`. Under the table add one sentence: a person who types `--claim` with no `--pipeline` gets `full`, and the issue watcher never relies on the default because it always passes `--pipeline none`. In the STOP rules, change the `E-SUBMIT-NEEDS-FULL` rule to apply when `--submit` has a value or is combined with `--pipeline worktree` or `--pipeline none`, keep the quoted message `"--submit needs --pipeline full"`, and say a bare `--submit` runs at `full`. In the `--submit` row keep the words `--pipeline full` and add "(the default)". Add the example line `/sc:issue --claim 302 --pipeline worktree` to the Examples block.

Acceptance criteria:
- The Options table `--pipeline` row default cell is exactly `` `full` `` and its values cell still lists `worktree`, `full`, `none` in that order.
- `/sc:issue --claim 302 --pipeline worktree` is a line of the Examples block, and the existing examples for `none`, `full` and `full --submit` are still present.
- The STOP rule order is unchanged (create-only, claim-only, bad value, submit) and the text `src/superclaude/` does not appear in the file.

## Task 4: State the default in the protocol, the claim steps and the next-steps template

In `src/superclaude/skills/sc-issue-protocol/SKILL.md`: in the claim-mode summary (line 17) move "(default)" from `worktree` to `full`; in the error-handling table change the `E-SUBMIT-NEEDS-FULL` condition to match Task 3; in the return contract section say `pipeline_level` holds the resolved level, `full` when `--pipeline` was omitted. In `src/superclaude/skills/sc-issue-protocol/refs/claim.md` Wave 5 step 4, change "where `<L>` is the `--pipeline` value" to "where `<L>` is the `--pipeline` value, or `full` when the flag was omitted", adding words only. In `src/superclaude/skills/sc-issue-protocol/templates/next-steps.md` line 7, replace "(up to the plan boundary at the default level)" with "(up to the plan boundary at level `worktree`, to the last step at the default level `full`)".

Acceptance criteria:
- SKILL.md names `full` as the default and no longer calls `worktree` the default; the Wave 5 and Wave 8 sentences pinned by `test_st7_plan_boundary_line_and_the_k_rule` and `test_st9_prompt_is_written_before_wave_7_and_wave_8_skips_none` still appear verbatim.
- The `next-steps.md` template still starts with a `/model ` line and still contains `Plan boundary: after step <K>`.
- The `E-SUBMIT-NEEDS-FULL` wording in SKILL.md and in the command file describes the same condition.

## Task 5: Pin the new default in the command tests

Depends on: Task 3

In `tests/commands/test_issue_command.py`, change `test_option_defaults` so `rows["--pipeline"][2] == "`full`"`. Add a test that the command text says the issue watcher always passes `--pipeline none` and that `/sc:issue --claim 302 --pipeline worktree` is an example line. Add a test that the `E-SUBMIT-NEEDS-FULL` rule text names `--pipeline worktree` and `--pipeline none` and still carries the quoted message `"--submit needs --pipeline full"`. Do not edit `tests/issue_watch/test_launch.py`: its tests at lines 929-939 already assert `build_claim_prompt(9)` returns `/sc:issue --claim 9 --pipeline none` and that the bare form no longer matches `PROMPT_PATTERN`.

Acceptance criteria:
- `uv run pytest tests/commands/test_issue_command.py tests/issue_watch/test_launch.py tests/issue_watch/test_security_invariants.py -v` passes with `tests/issue_watch/` unchanged.
- Setting the Options table default back to `` `worktree` `` makes `test_option_defaults` fail.

## Task 6: Pin the default in the protocol tests

Depends on: Task 2, Task 4

In `tests/skills/test_issue_protocol.py` add one test asserting that SKILL.md says `full` is the default, that the Wave 5 text of `src/superclaude/skills/sc-issue-protocol/refs/claim.md` contains "or `full` when the flag was omitted", and that the `next-steps.md` template contains "default level `full`".

Acceptance criteria:
- `uv run pytest tests/skills/test_issue_protocol.py -v` passes.
- Removing "or `full` when the flag was omitted" from `refs/claim.md` makes the new test fail.

## Phase 3: User-facing documentation

## Task 7: Update the user guide for the new default

In `docs/user-guide/commands.md` update the `/sc:issue` section: in the options table (line 368) set the `--pipeline` default to `full` and say omitted means `full`; in the levels table move "(default)" from `worktree` (line 377) to `full` (line 378); in the paragraph after the options table, make the `E-SUBMIT-NEEDS-FULL` sentence say `--submit` with `--pipeline worktree` or `--pipeline none` stops; add `/sc:issue --claim 302 --pipeline worktree` to the examples; add one sentence that the issue watcher always passes `--pipeline none`. Leave the guard and ship-gate paragraph unchanged.

Acceptance criteria:
- `grep -n "worktree. (default)" docs/user-guide/commands.md` prints nothing and the `full` row of the levels table carries "(default)".
- The syntax block, the ClickUp table and the guard paragraph are unchanged.

## Task 8: Amend the two design records

In `docs/designs/sc-issue-claim-pipeline-flag.md` add a dated amendment note, "Amended 2026-11-18", under decision P2 and next to the levels table row at line 21: the default is `full` when a person types the command, and the issue watcher always passes `--pipeline none`. In `docs/designs/sc-issue-command.md` add the same dated note under the existing "Amended 2026-11-07" note (line 64) and in the sentence at line 494 change "with the default `--pipeline worktree`" to "with `--pipeline worktree`". Keep the original decision text; only add amendments.

Acceptance criteria:
- `grep -n "default .--pipeline worktree" docs/designs/sc-issue-command.md` prints nothing.
- Both design files contain "Amended 2026-11-18" with the new default and the watcher's explicit `none`.

## Phase 4: Routing guide mirror and dev-copy sync

## Task 9: Update the routing guide sentence and its mirror

In `src/superclaude/core/HOW-WE-WORK.md` line 328, change "`worktree` by default: plan, then wait for approval" so the sentence says `full` is the default when a person types the command (implement, no commit or push), `worktree` plans then waits for approval, and `--submit` with `full` still commits, pushes and opens the PR. Keep the rest of the line. Then copy the file byte for byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`. The level table is not touched, so `src/superclaude/core/CLAUDE.md` needs no change.

Acceptance criteria:
- `diff src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` prints nothing.
- `uv run pytest tests/commands/test_routing_plugin_parity.py tests/core/test_how_we_work_routing_table.py tests/core/test_claude_md_routing_block.py -v` passes.

## Task 10: Sync the dev copies

Depends on: Task 1, Task 3, Task 4, Task 9

Run `make sync-dev` so the gitignored `.claude/` copies of the edited command and skill files match `src/superclaude/`. Stage only the `src/`, `tests/`, `docs/` and `plugins/` side; never `git add` anything under `.claude/`.

Acceptance criteria:
- `make verify-sync` exits 0.
- `git status --short` lists no path under `.claude/` as staged.
