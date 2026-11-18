# Codegraph grounding: TASK-WF-refactorScIssueC-20261118-041634

## Run state

- index_state: fresh (`codegraph_status` answered "Changes since index: 0 added, 0 modified, 0 removed")
- access: mcp (lookup tools listed)
- checked_at: 2026-11-18T04:16:47Z (taken from one `date -u` run right after the status call)
- worktree_root / projectPath: /home/coder/workspaces/worktrees/IronClaude/RefactorIssueClaimPipeline
- degraded: none. Most of the code under change is Markdown, which the graph does not index, so Grep and Read did the work there.

## Resolved symbols

- `build_claim_prompt` (function, `src/superclaude/cli/issue_watch/launch.py:84`): returns `/sc:issue --claim <n> --pipeline none`. Read before citing. This plan does not change it.
- `PROMPT_PATTERN` (`src/superclaude/cli/issue_watch/launch.py:33`): `^/sc:issue --claim [1-9][0-9]{0,8} --pipeline none$`.
- Markdown files that carry the default level or the simple feature row (resolved by Grep, then Read): `src/superclaude/commands/issue.md` (line 16 and the Options table), `src/superclaude/skills/sc-issue-protocol/SKILL.md` (line 17, error table), `src/superclaude/skills/sc-issue-protocol/refs/claim.md` (Wave 5 step 4), `src/superclaude/skills/sc-issue-protocol/refs/chains.md` (row `Feature, simple`), `src/superclaude/skills/sc-issue-protocol/templates/next-steps.md` (line 7), `docs/user-guide/commands.md` (lines 368 and 377), `src/superclaude/core/HOW-WE-WORK.md` (line 328, mirrored byte for byte in `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`), `docs/designs/sc-issue-claim-pipeline-flag.md` (lines 21, 43), `docs/designs/sc-issue-command.md` (lines 64, 494).

## Dependents

- Callers of `build_claim_prompt` (graph rows, 10 of 14 shown, `graph:truncated`; all are tests, `status_report` in `src/superclaude/cli/issue_watch/cycle.py:1270` and a dev artifact): none changes in this plan. Rows are def-line leads; the call sites were not confirmed, so the plan names them only as dependents that stay as they are.
- `tests/commands/test_issue_command.py::test_option_defaults` asserts `rows["--pipeline"][2] == "`worktree`"` (line 113): must change to `full`.
- `tests/commands/test_issue_command.py::test_st2_pipeline_and_submit_stop_rules_come_after_the_old_ones` pins the quoted message `"--submit needs --pipeline full"` and the rule order: both stay valid if the message and order are kept.
- `tests/skills/test_issue_protocol.py::test_brainstorm_steps_have_no_handoff_and_use_default_models` asserts 3 brainstorm steps across the 6 rows (line 662): must become 2.
- `tests/skills/test_model_alias_policy.py::test_issue_chains_use_the_default_brainstorm_models` (lines 191-196) asserts at least 3 `/sc:brainstorm` spans in `refs/chains.md`; Task 1 leaves 2, so Task 2 changes it to at least 2. The first pre-check and the first review missed it; the second fresh checker found it.
- `tests/skills/test_issue_protocol.py::test_every_chain_flag_exists_in_its_command` needs `--depth` and `--handoff` to exist in the workflow command file: they do.
- `tests/skills/test_issue_protocol.py::test_st7_plan_boundary_line_and_the_k_rule` and `test_st9_prompt_is_written_before_wave_7_and_wave_8_skips_none` pin sentences in Wave 5 and Wave 8 of `refs/claim.md`: edits there must only add words.
- `tests/commands/test_issue_command.py::test_no_source_tree_path` forbids the text `src/superclaude/` anywhere in the command file.
- `tests/issue_watch/test_launch.py` (lines 36, 43, 929-939) and `tests/issue_watch/test_security_invariants.py` already pin the watcher's explicit `--pipeline none` prompt and that the bare form no longer matches: no edit needed.
- `tests/commands/test_routing_plugin_parity.py` and `tests/core/test_how_we_work_routing_table.py` read `HOW-WE-WORK.md`: the plugin copy must stay byte-identical (it is identical today).
- Overlap: the worktree `claim-handoff-planb` (branch `ironbelly/no-sc-task-recommendation`) edits `HOW-WE-WORK.md`, `core/CLAUDE.md` and the launch-level hook files; its gated plan also edits lines 16 and 43-44 of `issue.md`, `SKILL.md` and `refs/claim.md`. Expect conflicts; rebase onto `origin/master` before any pull request.

## Dependents added in revision 2 (2026-11-18, from the advisory review; Grep and Read, each line re-read by the reviewers)

- `src/superclaude/skills/sc-issue-protocol/refs/claim.md:142` (the `launched` final-output text) and `:120` (Wave 8, `--level <L>`): Tasks 4 and 6.
- `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:1557` (default `worktree`) and `:1635` (old E-SUBMIT condition): Task 7.
- `docs/designs/sc-issue-claim-pipeline-flag.md:66`, `:78`, `:87` (old default text; `:85` is the correct stop rule and stays) and `docs/designs/sc-issue-command.md:44`, `:238` (old chain row): Task 8.
- `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`: `cmd_pending` (`:1515-1523`) writes only a pending record, the launch entry is written at `:1619-1631` and read at `:1703-1721`, `--level` is required (`:1873`, `:1883`) and `--submit` is refused unless the level is `full` (`:1900-1901`). Not edited; they are the basis of the known-risk constraint.
- Recorded out of scope: `src/superclaude/cli/issue_pipeline/templates/worker-brief.txt:17-19`, `docs/designs/issue-watcher-setup.md:616-619` and `:575`, `docs/designs/issue-watcher.md:41` and `:48`.

## Pre-check

Result: 10 tasks checked; every file a task names exists (17 paths checked); each sentence a task says to change was found exactly once (`Feature, simple` row, `at the default level` in the next-steps template, `where <L> is the --pipeline value` in `refs/claim.md`, `by default: plan, then wait for approval` in `HOW-WE-WORK.md`, `with the default --pipeline worktree` in `sc-issue-command.md`). No `graph:*` token.

Notes, no plan edit made:
- `docs/designs/sc-issue-command.md` has 7 lines containing "Amended 2026-11-07"; Task 8 means the one at line 64.
- `docs/designs/issue-watcher.md` line 41 also says the claim command's default level is `worktree`. It is a dated decision record of 2026-11-17, so no task edits it; a reader may find it stale after this change.
- `README.md` and `docs/user-guide/agents.md` mention "pipeline" but were not read; UNVERIFIED that they state the default level.
