# Codegraph grounding for TASK-WF-implementPartAOf-20261120-025240

## Run state

- index_state: fresh (status answer: 3465 files, "Changes since index: 0 added, 0 modified, 0 removed")
- checked_at: 2026-11-20T02:53:20Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook
- projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook
- access: mcp (codegraph_search, codegraph_node, codegraph_callers listed)
- tokens: none

## Resolved symbols

All ranges read from source before use.

- src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:183 `atomic_write_text(path, text)`: mkstemp plus os.replace; callers write_record (507), record_launch (1619), cmd_prompt (764).
- orca_worktree.py:204 `emit(payload)`: prints one JSON object, returns 0.
- orca_worktree.py:507 `write_record`, :1619 `record_launch`: write `worktree.json` (name constant `RECORD_NAME`, line 240) with a `launch` entry of only `level`, `submit`, `at`.
- orca_worktree.py:1646 `launch_result(status, notes, **fields)`: builds the nine-key launch JSON.
- orca_worktree.py:1696 `cmd_launch`: eight `return emit(...)` sites between lines 1696 and 1834 (no-usable-record failed, already_launched, stale-prompt failed, enforcement-absent failed, L2-refusal failed, launch-record-write failed, orca-launch failed, launched); registered by `build_parser` (1857) as the `launch` subcommand's callback; its only caller.
- tests/skills/test_issue_orca_worktree.py:1260 `launch_scene`, :1298 `run_launch`, :1741 `test_ir6_launched_result_states_the_release_and_both_layers`, :2136 `test_launch_creates_no_file_in_the_worktree_or_the_source_directory`.
- tests/skills/test_issue_protocol.py:486 `test_st9_final_output_lists_the_launch_results_and_every_launch_code` (reads refs/claim.md and SKILL.md through `_text`).
- src/superclaude/skills/sc-issue-protocol/refs/claim.md:125 the Wave 8 launch JSON description; SKILL.md "Return contract" section.

## Dependents

- Callers of `cmd_launch`: `build_parser` only. Callers of `emit`: all subcommands (unchanged).
- A test that this change contradicts as written: `test_launch_creates_no_file_in_the_worktree_or_the_source_directory` (tests/skills/test_issue_orca_worktree.py:2136) asserts the source directory listing is unchanged after a launch. The new file breaks it, so the plan updates it on purpose: the source directory may gain exactly `launch-result.json`; the worktree and `git status` stay unchanged.
- Other launch tests read `data` from stdout and `worktree.json`; none lists the source directory (grep of tree_listing, iterdir, glob in the three launch test files).
- tests/skills/test_issue_l2_install.py:620 calls `module.cmd_launch(args)` directly and checks `worktree.json` only.
- `.dev/issues/<N>/` is never staged by the skill (SKILL.md default D24), so the new file is an untracked per-issue file like `worktree.json`.
- No plugins/superclaude mirror of sc-issue-protocol exists.
- Not touched here (Part B): .dev/issues/442/scripts/session-gov.sh and observation-runbook.md.

## Pre-check

Checked 2026-11-20 (Read and Grep; no new readiness check): every file the four tasks name exists, except the one the plan creates by design (`launch-result.json`, a runtime file); the symbols `atomic_write_text`, `emit`, `launch_result`, `cmd_launch`, `RECORD_NAME`, `launch_scene`, `run_launch` and the two named tests resolve at the lines above. The Tier 2 review (reflect report in `.dev/reflect/pre-TASK-WF-implementPartAOf-20261120-025240-20261120025500/`) found dependents the plan does not name: `copy_issue_dir` (orca_worktree.py:466-467, copies the new file into worktrees), `src/superclaude/commands/issue.md:80` (file inventory). Count: 4 tasks, 0 missing files, 0 unresolved symbols, 2 unnamed dependents.
