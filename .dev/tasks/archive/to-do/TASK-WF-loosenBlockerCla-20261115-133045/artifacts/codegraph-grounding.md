# Codegraph grounding for TASK-WF-loosenBlockerCla-20261115-133045

## Run state

- index_state: fresh
- checked_at: 2026-11-15T13:30:53Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
- projectPath: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
- access: mcp (lookup tools listed; `codegraph_status` answered "Changes since index: 0 added, 0 modified, 0 removed", 3543 files)
- degraded tokens: none
- note: the index does not cover Markdown, so the skill, agent, template and command files this plan edits were resolved with Grep and Read (the permanent floor), not codegraph.

## Resolved symbols

- `src/superclaude/cli/review/__init__.py`: `review_group` registers subcommand modules from a tuple of names (`panel_cmd`, `merge_cmd`, `ledger_cmd`, `telemetry_cmd`, `lint_cmd`, `estimate_cmd`, `cluster_cmd`, `verify_cmd`, `manifest_cmd`); each module exports `command`. A new `classify_cmd` joins by adding its name to that tuple. Read at lines 14-36.
- `src/superclaude/cli/review/ledger.py`: existing typed ledger, schema `review-ledger/1` (`new_ledger`, `load`, `save`, `merge_round`, `apply_revision`, `defer`, `verdict`, `capture`, `render_merged_report`). The new follow-up ledger is a separate Markdown ledger; the reuse-auditor must run before a new reader or writer is built.
- `src/superclaude/cli/review/card_convert.py:250` and `src/superclaude/cli/review/telemetry.py:162`: split table rows on every bare pipe (confirmed by Grep), so the follow-up ledger cell codec must not use a backslash before a pipe.
- `src/superclaude/cli/doctor.py`: `run_doctor`, `_check_skills_installed`, `_check_agents_installed`, `_check_configuration`; the new digest-version check is added here.
- `src/superclaude/cli/main.py`: registers `review_group` as `review` (line 568-570) and `doctor` (line 477).
- `Makefile`: target `doctor` runs `uv run superclaude doctor` (line 23).
- Markdown anchors read before citing: `src/superclaude/output-styles/pragmatic.md` lines 221, 225-231; `src/superclaude/skills/task/SKILL.md` lines 252, 254, 258, 361; `src/superclaude/agents/rf-qa.md` lines 83, 108, 152, 162, 327; `src/superclaude/agents/rf-qa-qualitative.md` lines 84, 108, 990; `src/superclaude/agents/rf-analyst.md` line 75; `src/superclaude/core/WORKER-CONTRACT.md` lines 33, 39; `src/superclaude/skills/tech-research/SKILL.md` line 415; `src/superclaude/commands/spec-panel.md` lines 259-261, 372, 455.
- Not existing yet (confirmed): `src/superclaude/skills/sc-review-severity/`.

## Dependents

- `run_doctor`: `doctor` in `src/superclaude/cli/main.py:477`; `tests/unit/test_cli_doctor.py` (`test_run_doctor_includes_the_codegraph_check`); `tests/cli/test_install_retired_mcp.py` (`test_update_and_doctor_never_mutate_and_never_change_their_exit_code`). Resolution: def-line.
- `merge_round` (ledger.py): `src/superclaude/cli/review/merge_cmd.py:71`, `tests/review/test_review_ledger.py` (10 of 20 callers shown, `graph:truncated`), and `.dev/research/346-review-loop-experiments/p18/ab5/full.py`. Resolution: def-line. The new follow-up ledger does not call it.
- `src/superclaude/cli/review/__init__.py`: used by 28 files including `src/superclaude/cli/main.py` and `tests/review/test_review_findings.py`. Adding a name to the tuple touches `review_group` only.
- Test modules that pin the rule text (named by the spec, existence confirmed): `tests/skills/test_review_severity_rule.py`, `test_review_severity_mapping.py`, `test_implement_severity_static.py`, `test_review_loop_extension.py`, `test_review_prompt_overrides.py`, `test_spec_panel_review_loop.py`, `tests/audit/test_nfr_conv_9_zero_trust.py`, `test_invariant_preservation_NFR_6_through_10.py`, `test_severity_floor_unweakened.py`, `test_dnsp_all_agents_fail_bypass.py`, `tests/review/test_review_rules_text.py`, and the fixtures `tests/skills/fixtures/review_severity_cap_edits.yaml` and `review_severity_sweep_edits.yaml`.

## Pre-check

Checked 2026-11-15 with `test -e` over every `src/`, `tests/` and `plugins/` path the plan names in backticks (71 distinct paths): 45 exist and 26 are files or folders the plan creates (the skill folder and its 5 refs, six modules under `src/superclaude/cli/review/`, the thresholds file, eight new test modules, and the plugin mirror folder). No named existing path is missing.
Line anchors the plan cites in Markdown files were read before citing (see Resolved symbols). Dependents the plan names: `tests/unit/test_cli_doctor.py` and `tests/cli/test_install_retired_mcp.py` (Task 18), the three `tests/skills` severity modules and the three `tests/audit` modules (Tasks 31 and 32), and `tests/review/test_review_rules_text.py` (Task 35).
Dependents of touched symbols that no task names: `src/superclaude/cli/main.py` (registers `review_group` and `doctor`; neither registration changes, only the tuple in `review/__init__.py` and `run_doctor`'s body); `tests/cli/test_update_command.py` (calls `run_doctor` indirectly; it is named in Task 18's acceptance command). No other gap found.
Not checked: whether the further `rf-qa.md` line numbers in Task 27 (`rf-qa.md` lines 168-170, 182-183, 221, 316, 333, 334, 389, 476, 494, 548) still match; Task 1 freezes them from a live Grep before those tasks run.
