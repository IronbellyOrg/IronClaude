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
Goal: A person who types `/sc:issue --claim <N>` with no `--pipeline` gets level `full`, the default simple feature row of the chain table no longer starts with `/sc:brainstorm`, and the issue watcher still claims with its explicit `--pipeline none`.

## Constraints

- Edit only source files: `src/superclaude/...`, `tests/...`, `docs/...` and the one mirror file `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`. Never edit or stage anything under `.claude/`; Task 10 regenerates those copies with `make sync-dev`.
- The default level applies to a bare `--claim`. The issue watcher always passes `--pipeline none` (`build_claim_prompt` in `src/superclaude/cli/issue_watch/launch.py`, pinned by `tests/issue_watch/test_launch.py`). Do not edit either file and do not add any human-versus-agent detection.
- The default level does not authorize a commit, a push or a pull request: `E-SUBMIT-NEEDS-FULL` keeps its meaning, so a `--submit` with no `--pipeline` still stops and `--submit` needs an explicit `--pipeline full` (the design record `docs/designs/sc-issue-claim-pipeline-flag.md` line 85 already says so).
- No file under `src/superclaude/skills/sc-issue-protocol/` and not `src/superclaude/commands/issue.md` may contain the text `src/superclaude/` (`tests/skills/test_issue_protocol.py::test_no_source_tree_path_in_skill_files` and `tests/commands/test_issue_command.py::test_no_source_tree_path` forbid it): in those files cite code by file name, never by its `src/superclaude/` path.
- New lines in command and skill files must not contain `git add`, `git commit`, `git push`, `git merge`, `gh pr` or `gh api`: `tests/skills/test_worker_contract.py` audits those verbs line by line.
- Leave the ship-gate sentences (OB-H1, OB-H2, OB-H3) and the `--pipeline none` coordinator-handoff paragraph exactly as written. The worktree `claim-handoff-planb` edits the same files (`issue.md`, `SKILL.md`, `refs/claim.md`, `HOW-WE-WORK.md`), so keep every edit narrow and rebase onto `origin/master` before any pull request.
- Out of scope: `/tech-research`, `/task-builder` and `/task` handling, the complex bug row, model tiers, `orca_worktree.py`, every other chain row, and the command version (it stays 1.1.0, which `tests/commands/test_issue_command.py` pins).
- Also out of scope, recorded on purpose: `src/superclaude/cli/issue_pipeline/templates/worker-brief.txt` lines 17-19 (the coordinator path keeps its brainstorm step for simple work); the owner-run bare launch prompts in `docs/designs/issue-watcher-setup.md` lines 616-619 (a launch with them now starts at `full`; update them before reuse if a claim-only capture is wanted); and the dated records `docs/designs/issue-watcher.md` lines 41 and 48 and `docs/designs/issue-watcher-setup.md` line 575.
- Known risk, not fixed here: a person's bare `/sc:issue --claim <N>` on an issue that a coordinator already owns reuses its worktree and starts a second agent, now at `full`, because only the claim's own launch step writes the launch record (`cmd_pending` in `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` writes only a pending record). Do not claim such an issue without `--pipeline none`.

## Phase 1: Simple feature chain without brainstorm

## Task 1: Replace the Feature, simple row in the chain table

In `src/superclaude/skills/sc-issue-protocol/refs/chains.md`, change only the table row that starts `| Feature, simple |`. Keep its tier line `/model claude-gw-tier2`. Replace its chain cell with two steps in the row's existing `<br>` style: the first runs `/sc:workflow <S> --depth quick --handoff none` (`<S>` is the issue-summary path the file already defines), the second runs `/sc:implement <plan path printed by step 1>`. Under `Notes:` add one bullet saying the simple feature row has no brainstorm step because the issue summary already states the requirements, so it plans directly from it. Leave the other five rows and the paragraph about handoff flags unchanged.

Acceptance criteria:
- The `Feature, simple` row contains no `/sc:brainstorm` and exactly the two commands above; the other five rows are byte-identical to before.
- Because the first `/sc:implement` step is now step 2, the plan boundary for this row is `after step 1`, and the `Plan boundary` rule in `src/superclaude/skills/sc-issue-protocol/refs/claim.md` (Wave 5 step 3) still reads correctly.
- Every flag in the new commands exists in the workflow and implement command files, so `test_every_chain_flag_exists_in_its_command` in `tests/skills/test_issue_protocol.py` still passes.

## Task 2: Update the chain tests for the new simple feature row

Depends on: Task 1

In `tests/skills/test_issue_protocol.py`, change `test_brainstorm_steps_have_no_handoff_and_use_default_models` so it expects 2 brainstorm steps across the 6 rows (it asserts 3 today). Add a new test next to it that finds the `Feature, simple` row of `src/superclaude/skills/sc-issue-protocol/refs/chains.md` and asserts it has no `/sc:brainstorm`, contains `/sc:workflow <S> --depth quick --handoff none` and contains `/sc:implement <plan path printed by step 1>`. Also change `test_issue_chains_use_the_default_brainstorm_models` in `tests/skills/test_model_alias_policy.py` (lines 191-196), which asserts at least 3 `/sc:brainstorm` spans in `chains.md`, to assert at least 2; keep its check that no span carries `--models`.

Acceptance criteria:
- `uv run pytest tests/skills/test_issue_protocol.py tests/skills/test_model_alias_policy.py -v` passes.
- Restoring the old brainstorm step into the row makes the new test and the 2-step count fail.

## Phase 2: Default level full in the command and the protocol

## Task 3: Make full the default level in the command file

In `src/superclaude/commands/issue.md` make these narrow edits. In the paragraph that lists the levels (line 16), move "(the default)" from `worktree` to `full`. In the Options table, set the `--pipeline` row default to `` `full` `` and add "Omitted means `full`." to its meaning; leave its values cell as `worktree`, `full`, `none`. Under the table add one sentence: a person who types `--claim` with no `--pipeline` gets `full`, and the issue watcher never relies on the default because it always passes `--pipeline none`; `--submit` still needs an explicit `--pipeline full`, even though `full` is the default. In the STOP rules keep the `E-SUBMIT-NEEDS-FULL` rule and its quoted message `"--submit needs --pipeline full"` and change its condition to "`--submit` with a value, without `--pipeline full`, or with no `--pipeline`" (the wording of `docs/designs/sc-issue-claim-pipeline-flag.md` line 85), so that the stated default cannot satisfy it. In the `--submit` row keep the words `--pipeline full` and add "an explicit `--pipeline full` is still required". Add the example line `/sc:issue --claim 302 --pipeline worktree` to the Examples block.

Acceptance criteria:
- The Options table `--pipeline` row default cell is exactly `` `full` `` and its values cell still lists `worktree`, `full`, `none` in that order.
- `/sc:issue --claim 302 --pipeline worktree` is a line of the Examples block, and the existing examples for `none`, `full` and `full --submit` are still present.
- The STOP rule order is unchanged (create-only, claim-only, bad value, submit) and the text `src/superclaude/` does not appear in the file.
- The `E-SUBMIT-NEEDS-FULL` rule still carries the quoted message and now also names the case of no `--pipeline`; the `--submit` row still contains `--pipeline full`.

## Task 4: State the default in the protocol, the claim steps and the next-steps template

Depends on: Task 3

In `src/superclaude/skills/sc-issue-protocol/SKILL.md`: in the claim-mode summary (line 17) move "(default)" from `worktree` to `full`; in the error-handling table change the `E-SUBMIT-NEEDS-FULL` condition to match Task 3; in the return contract section say `pipeline_level` holds the level requested in this run, `full` when `--pipeline` was omitted, and that an `already_launched` result keeps the level its running agent was launched with, which is read from the `launch` entry of `.dev/issues/<N>/worktree.json` or, when that file has none (a re-claim from inside the worktree), from the mirror file the helper's detail names, because the helper's `already_launched` output carries no level (both hold `{level, submit, at}`). In `src/superclaude/skills/sc-issue-protocol/refs/claim.md` Wave 5 step 4, change "where `<L>` is the `--pipeline` value" to "where `<L>` is the `--pipeline` value, or `full` when the flag was omitted", adding words only. In the same file add a sentence after the `orca_worktree.py launch ... --level <L>` command line of Wave 8 saying `<L>` is the same level as in Wave 5, leaving that command line exactly as it is (`test_st9_prompt_is_written_before_wave_7_and_wave_8_skips_none` pins it), and add the same sentence to Wave 8 in SKILL.md (line 92), and in the final-output item for `launched` (line 142 of `refs/claim.md`) make the sentence "It stops at the plan boundary and waits; run the printed implement command ... to let it continue." apply to level `worktree` only, keeping the separate sentence for `full`. In `src/superclaude/skills/sc-issue-protocol/templates/next-steps.md` line 7, replace "(up to the plan boundary at the default level)" with "(up to the plan boundary at level `worktree`, to the last step at the default level `full`)".

Acceptance criteria:
- SKILL.md names `full` as the default and no longer calls `worktree` the default; the Wave 5 and Wave 8 sentences pinned by `test_st7_plan_boundary_line_and_the_k_rule` and `test_st9_prompt_is_written_before_wave_7_and_wave_8_skips_none` still appear verbatim.
- The `next-steps.md` template still starts with a `/model ` line and still contains `Plan boundary: after step <K>`.
- The `E-SUBMIT-NEEDS-FULL` wording in SKILL.md and in the command file describes the same condition, including the case of no `--pipeline`.
- In `refs/claim.md` the `launched` text puts "run the printed implement command" under level `worktree` only, and Wave 8 says `<L>` is the same level as in Wave 5 in a sentence after the unchanged `orca_worktree.py launch ... --level <L>` command line.
- SKILL.md says an `already_launched` result keeps the level of the running agent and names the `launch` entry of `worktree.json` (or the mirror file when `worktree.json` has none) as where it is read.

## Task 5: Pin the new default in the command tests

Depends on: Task 3

In `tests/commands/test_issue_command.py`, change `test_option_defaults` so `rows["--pipeline"][2] == "`full`"`. Add a test that the command text says the issue watcher always passes `--pipeline none` and that `/sc:issue --claim 302 --pipeline worktree` is an example line. Add a test that the `E-SUBMIT-NEEDS-FULL` rule text says a `--submit` with no `--pipeline` stops (it contains "no `--pipeline`") and still carries the quoted message `"--submit needs --pipeline full"`. Do not edit `tests/issue_watch/test_launch.py`: its tests at lines 929-939 already assert `build_claim_prompt(9)` returns `/sc:issue --claim 9 --pipeline none` and that the bare form no longer matches `PROMPT_PATTERN`.

Acceptance criteria:
- `uv run pytest tests/commands/test_issue_command.py tests/issue_watch/test_launch.py tests/issue_watch/test_security_invariants.py -v` passes with `tests/issue_watch/` unchanged.
- Setting the Options table default back to `` `worktree` `` makes `test_option_defaults` fail.
- Removing "no `--pipeline`" from the stop rule makes the new submit-rule test fail.

## Task 6: Pin the default in the protocol tests

Depends on: Task 2, Task 4

In `tests/skills/test_issue_protocol.py` add one test asserting that SKILL.md says `full` is the default, that the Wave 5 text of `src/superclaude/skills/sc-issue-protocol/refs/claim.md` contains "or `full` when the flag was omitted", that the `next-steps.md` template contains "default level `full`", that in `refs/claim.md` the words "run the printed implement command" appear under the `worktree` wording only (the `full` branch does not carry them), and that Wave 8 says `<L>` is the same level as in Wave 5.

Acceptance criteria:
- `uv run pytest tests/skills/test_issue_protocol.py -v` passes.
- Removing "or `full` when the flag was omitted" from `refs/claim.md` makes the new test fail.
- Putting "run the printed implement command" back into the unconditional `launched` sentence makes the new test fail.

## Phase 3: User-facing documentation

## Task 7: Update the user guide and the architecture reference for the new default

In `docs/user-guide/commands.md` update the `/sc:issue` section: in the options table (line 368) set the `--pipeline` default to `full` and say omitted means `full`; in the levels table move "(default)" from `worktree` (line 377) to `full` (line 378); in the paragraph after the options table, make the `E-SUBMIT-NEEDS-FULL` sentence say `--submit` with `--pipeline worktree`, `--pipeline none` or no `--pipeline` stops; add `/sc:issue --claim 302 --pipeline worktree` to the examples; add one sentence that the issue watcher always passes `--pipeline none`. Leave the guard and ship-gate paragraph unchanged. In `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` change line 1557 (the `--pipeline` default `worktree`) to `full` and make line 1635 (`--submit` with a value or without `--pipeline full`) also name the case of no `--pipeline`; in the Impact cell of the row at line 1557 ("`--submit` with a pipeline other than `full`, or with a value, is refused") add that a `--submit` with no `--pipeline` is refused too.

Acceptance criteria:
- `grep -n "worktree. (default)" docs/user-guide/commands.md` prints nothing and the `full` row of the levels table carries "(default)".
- The syntax block, the ClickUp table and the guard paragraph are unchanged.
- Re-reading lines 1557 and 1635 of the architecture reference shows `full` as the default and the no `--pipeline` case in the `--submit` condition and in the Impact cell of the line 1557 row.

## Task 8: Amend the two design records for the new default

In `docs/designs/sc-issue-claim-pipeline-flag.md` add a dated amendment note, "Amended 2026-11-18", under decision P2 and next to the levels table row at line 21: the default is `full` when a person types the command, and the issue watcher always passes `--pipeline none`. In `docs/designs/sc-issue-command.md` add the same dated note under the existing "Amended 2026-11-07" note (line 64) and in the sentence at line 494 change "with the default `--pipeline worktree`" to "with `--pipeline worktree`". In `docs/designs/sc-issue-claim-pipeline-flag.md` (not the command design record) also add amendment notes beside lines 66 ("An unflagged claim is `--pipeline worktree`."), 78 (the options row) and 87 ("worktree level") saying the default is now `full` for a person, and beside line 274 (the `--submit` condition) saying a `--submit` with no `--pipeline` also stops; leave line 85 (the `--submit` stop rule) as it is, because it still holds. Lines 21, 43, 66, 78 and 274 are table rows: append each note inside the row's last cell (as decision P4 at line 45 does with its "Amended" text) and never as a new line under the row, which would split the table; line 87 is prose. In `docs/designs/sc-issue-command.md` also amend the sentence at line 44 (B17, "`worktree` (default, ...)") the same way and add a "Superseded 2026-11-18" bullet to the Notes list (lines 245-249), after the existing "Superseded by #384" bullet at line 248, naming the Feature, simple row at line 238 (do not put a plain line directly under the table row, which would split the table). Keep the original decision text; only add amendments.

Acceptance criteria:
- `grep -n "default .--pipeline worktree" docs/designs/sc-issue-command.md` prints nothing.
- Both design files contain "Amended 2026-11-18" with the new default and the watcher's explicit `none`.
- `docs/designs/sc-issue-claim-pipeline-flag.md` carries the note beside the lines that were 21, 43, 66, 78, 87 and 274 before the edit, the line that was 85 is unchanged, each note on a table row sits inside that row, and the tables still render as tables (no line without a leading `|` between two rows of one table).
- `docs/designs/sc-issue-command.md` carries the note at the lines that were 44 and 64 and a "Superseded 2026-11-18" bullet in its Notes list.

## Phase 4: Routing guide mirror and dev-copy sync

## Task 9: Update the routing guide sentence and its mirror

In `src/superclaude/core/HOW-WE-WORK.md` line 328, change "`worktree` by default: plan, then wait for approval" so the sentence says `full` is the default when a person types the command (implement, no commit or push), `worktree` plans then waits for approval, and `--submit` with `full` still commits, pushes and opens the PR. Keep the rest of the line. Then copy the file byte for byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`. The level table is not touched, so `src/superclaude/core/CLAUDE.md` needs no change. If `claim-handoff-planb` has already changed `HOW-WE-WORK.md` on `origin/master`, rebase first and redo the edit and the byte-for-byte copy on the rebased file instead of merging by hand.

Acceptance criteria:
- `diff src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` prints nothing.
- `uv run pytest tests/commands/test_routing_plugin_parity.py tests/core/test_how_we_work_routing_table.py tests/core/test_claude_md_routing_block.py -v` passes.

## Task 10: Sync the dev copies

Depends on: Task 1, Task 2, Task 3, Task 4, Task 5, Task 6, Task 7, Task 8, Task 9

Run `make sync-dev` so the gitignored `.claude/` copies of the edited command and skill files match `src/superclaude/`. Stage the `src/`, `tests/`, `docs/` and `plugins/` paths you changed and always `git add .dev/tasks`; never `git add` anything under `.claude/`.

Acceptance criteria:
- `make verify-sync` exits 0.
- `git status --short` lists no path under `.claude/` as staged and shows `.dev/tasks` staged.
