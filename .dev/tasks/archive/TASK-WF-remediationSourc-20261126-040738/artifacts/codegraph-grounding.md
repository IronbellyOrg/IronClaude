# Codegraph grounding

## Run state

- index_state: fresh
- checked_at: 2026-11-26T04:07:38Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-393
- projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-393
- access: mcp (codegraph_status listed; 3747 files, 0 added, 0 modified, 0 removed since the index)
- graph tokens: none. Note: most named files are markdown and carry no code symbols, so for them Glob, Grep and Read are the evidence; codegraph answered for the Python test file only.

## Resolved symbols

- `src/superclaude/skills/sc-implement-protocol/refs/retry.md`: markdown; the Model ladder section runs from the `### Model ladder` heading (line 160) to `### Cost and caps`; relevant lines read: 162 (ladders), 164 (executor tier), 166 to 172 (escalation rule and worked sentence), 174 to 179 (worked table), 181 (adviser B resolution), 183 (the pinned `GPT spawn path:` line), 185 (the sentence to replace).
- `src/superclaude/skills/sc-implement-protocol/SKILL.md`: markdown; line 193 holds the final-summary sentence to widen.
- `plugins/superclaude/skills/sc-implement-protocol/refs/retry.md` and `plugins/superclaude/skills/sc-implement-protocol/SKILL.md`: exist; byte-identical to the src copies at plan time (checked with `diff -q` for `retry.md` earlier in this session).
- `tests/skills/test_task_workspace_lifecycle.py`: codegraph_node symbol outline. The four pinned worked-table rows (lines 598 to 604) sit inside `test_retry_ref_rules_text` (def at line 516, the next symbol `_TRANSIENT` starts at line 611). Other symbols of the file that read `retry.md`: `test_retry_ref_and_reason_lists` (670), `test_retry_ref_revert_block_present` (740), `test_skill_retry_wiring_text` (832), `test_parallel_rules_identical_in_skill_and_retry_ref` (794).
- `tests/skills/test_implement_adviser_family.py`: `_family`, `escalation_1`, `header`, `test_ac18_two_families_and_gpt_is_t1`, `test_ac19_spawn_path_pinned`, `test_ac19_no_gpt_reachable_gives_fallback_header_and_no_stop` (lines 21 to 86), read in full.
- `tests/skills/test_implement_launch_alias.py`: does not exist yet (new file).

## Dependents

Files in `tests/` that name `refs/retry.md` or `implement-retry-adviser` (Grep, file level; each is a dependent that must stay green): `tests/skills/test_task_workspace_lifecycle.py`, `tests/skills/test_implement_adviser_family.py`, `tests/skills/test_model_alias_policy.py`, `tests/skills/test_implement_severity_static.py`, `tests/skills/test_workflow_archive.py`, `tests/skills/test_implement_retry_citation.py`, `tests/skills/test_implement_retry_revert.py`, `tests/skills/test_worker_contract.py`, `tests/unit/test_cli_install.py`, `tests/hooks/test_launch_level_guard.py`, plus the fixture `tests/sweep/fixtures/captured-task-list.json`. Also `tests/commands/test_workflow_command.py:204-220`, which compares the plugin tree with the src tree byte for byte (it names the skill directory, not `retry.md`). The first six are named in the source; the others read blocks of the file (the retry citation and revert blocks, the launch-level guard test that extracts the `sc_retry_revert` block) and the plan runs them as well. No call-site claim is made: these are file-level references only.

## Pre-check

Run after the Wave 3 gate passed (read-only; Grep, Glob and Read, plus the codegraph outline above; no new readiness check).

- Task 1: `retry.md` exists; the headings `### Model ladder` and `### Cost and caps` each occur once; the sentence "The model tier comes from the Agent call" and the words "the strongest reachable model" each occur once. Resolved.
- Task 2: "Worked example with the fallback ladder:" occurs once; `1× GPT T1` occurs four times in `tests/skills/test_task_workspace_lifecycle.py`, inside `def test_retry_ref_rules_text` (once in the file). Resolved.
- Task 3: both stale phrases quoted in the task occur once each in `retry.md`. Resolved.
- Task 4: the phrase "every `family-fallback:` header line of an `advice-3-b.md`" occurs once in `SKILL.md`. Resolved.
- Task 5: both plugin files exist and `retry.md` is byte-identical to the source copy before the edits; the Makefile targets `sync-dev` (line 109) and `verify-sync` (line 166) exist. Resolved.
- Task 6: `docs/reference/model-aliases.md` has one line containing "takes the aliases"; all twelve test and plugin files named in the dependents list exist; `HEAD` holds `retry.md` for the red check. Resolved.
- Result: 6 of 6 tasks resolved, 0 unresolved symbols.

Dependents of the touched text that no task names (informational, they are documentation citations and do not break a test): `docs/reference/model-aliases.md` line 61 cites `retry.md` lines 162, 164, 168, 169 and 172, and `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` lines 717 and 893 cite `retry.md:498`, which moves by the lines Task 1 adds. These are recorded as follow-up in the troubleshoot report (follow-up tasks), not part of this plan.
