10d7c8f8dac0d54b499bdfabb570e335c2c3eb2f
Review one task for spec compliance.

Task brief: ## Task 5: Implement resolution, the policy grid and the Skill classifier

Depends on: Task 4

In src/superclaude/hooks/scripts/launch-level-guard.sh fill the PreToolUse branch with the resolution rules of design section 3 (FR-L-10 as revised P1 to P7, FR-L-11 to FR-L-14, identity loss) and the policy grid of section 4 (FR-L-20, FR-L-21).

Resolution: with an empty session store allow; otherwise one jq extraction of the top-level fields (session id, hook_event_name, tool_name and the typed tool_input fields, command kept as a string); remove the fixed-64 raw-id early-allow loop of MR. A nonstring tool field or an embedded NUL is an input error. skill is used if present and non-null, otherwise name; an explicit empty string stays empty and yields SKILL; the file-path fallback follows the same missing-or-null rule. A valid unbound id allows silently; a valid bound id reads its exact level from sessions/<sid> (exactly one allowed word plus an optional newline; empty, malformed or unreadable means worktree with the LL-STATE note on a block); sessions/<sid>.ok existing at worktree gives the worktree (approved) level. Missing or invalid id, or an unparseable envelope, without independent positive binding evidence allows without claiming enforcement (design section 3 identity loss); a positively identified governed input error or internal failure blocks with LL-BROKEN; jq missing with a positively bound session blocks LL-BROKEN. agent_id is not read on PreToolUse and no cwd fallback exists (FR-L-13, FR-L-14).

Policy: one literal case on CLASS:LEVEL implementing the grid of design section 4 for all sixteen classes and the four levels (W, WA, F, FS), message precedence BIG, TAMPER, MERGE, GHWRITE, PROTECTED, ESCAPE, MCP, UNKNOWN, SUBMIT, REPO, PUSH, PUSHFORM, COMMIT, TURN, IMPL, SKILL, and any blocked class blocking the whole call.

First classifier, FR-L-40: for the Skill tool take name via the skill-else-name rule, strip leading space, keep the first word, lower-case, drop one leading slash, keep the text after the last colon, drop one leading sc- and one trailing -protocol. implement, task, improve, cleanup, spawn, build give IMPL (owner decision O-13); pr-submit gives SUBMIT; issue gives ESCAPE; empty gives SKILL; anything else gives NONE (cleanup-audit and task-builder stay NONE).

Extend tests/hooks/test_launch_level_guard.py with the T-SKL cases, the T-ISO and T-FC cases that concern resolution, the identity-loss cases (missing id, invalid id, numeric id, nested forged id, unparseable envelope) and a hand-written oracle dictionary EXPECTED for the Skill rows of the grid across the four levels.

Acceptance criteria:
- uv run pytest tests/hooks/test_launch_level_guard.py -v passes the Skill grid rows: at W the Skill sc:implement call exits 2 with LL-IMPL, at WA, F and FS it exits 0; pr-submit exits 2 with LL-SUBMIT at W, WA and F and exits 0 at FS; issue exits 2 with LL-ESCAPE at every level; an empty skill name exits 2 with LL-SKILL at W, WA and F and 0 at FS.
- A session file containing garbage blocks a Skill sc:implement call at W with the LL-STATE note, and the same call is allowed when sessions/<sid>.ok exists.
- A payload with a missing or invalid session id and a nonempty store exits 0 and prints nothing, and a test comment states it is a declared fail-open limit.
- With jq removed from PATH, a bound session blocks with LL-BROKEN and an unbound session is allowed.

AC ids (source order):
T5.AC1: uv run pytest tests/hooks/test_launch_level_guard.py -v passes the Skill grid rows: at W the Skill sc:implement call exits 2 with LL-IMPL, at WA, F and FS it exits 0; pr-submit exits 2 with LL-SUBMIT at W, WA and F and exits 0 at FS; issue exits 2 with LL-ESCAPE at every level; an empty skill name exits 2 with LL-SKILL at W, WA and F and 0 at FS.
T5.AC2: A session file containing garbage blocks a Skill sc:implement call at W with the LL-STATE note, and the same call is allowed when sessions/<sid>.ok exists.
T5.AC3: A payload with a missing or invalid session id and a nonempty store exits 0 and prints nothing, and a test comment states it is a declared fail-open limit.
T5.AC4: With jq removed from PATH, a bound session blocks with LL-BROKEN and an unbound session is allowed.
Global constraints: - docs/designs/sc-issue-launch-level-hook.md is the authority for this plan. The requirements file .dev/brainstorms/20261105-170229-launch-level-hook/merged-requirements.md (called MR below) is the historical baseline for requirement ids and the test corpus; where the design says it overrides MR (design section 11, DD-2), the design wins. .dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/launch-levels-addendum.md defines the claim side; the hook interface rules IR-1 to IR-7 in design section 13 win over it.
- This branch builds on open PR 425 (ironbelly/sc-issue-claim-pipeline-flag). The claim code in src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py already writes the launch record and marks the prompt (IR-1, IR-2); do not rebuild that.
- The L1 guard is one flat bash script using only bash, jq, sed and tr: exit 0 allows, exit 2 blocks, no onFailure, no Python, no git or network call on ordinary classification. No new runtime service, managed settings deployment, shell parser, hook forwarding framework or git config migration (design section 1).
- Do not change src/superclaude/hooks/scripts/launch-job-identity.sh or tests/hooks/test_launch_job_identity.py. A conflict found with it goes into the record of Task 14, not into that file.
- Ordinary sessions are never blocked by any failure (FR-L-53). Only a positively identified governed session fails closed.
- Live observations (OB-H1, OB-H2, OB-H3, OB-CTX) need real governed sessions or real launches. This plan runs none of them and never launches a governed agent on a real issue or pushes to a real protected branch. They stay pending (a skipped test with a stated reason), never reported as passed. Tests use a temporary HOME and temporary bare remotes.
- Acceptance claims cover the routes the tests exercise. Nothing here claims universal merge protection or defence against a hostile agent (design sections 1 and 12).
- Gate: Task 1 writes the B-CTX verdict. If ./artifacts/b-ctx-verdict.md contains the line "L1: STOP", stop the run at Task 1 and report that verdict; do not start Task 2 or any later task. Every task after Task 1 depends on that verdict.
- Existing tests: any task that changes a check in src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py also migrates the shared test fixture launch_scene in tests/skills/test_issue_orca_worktree.py (it writes only a bare shell stub today) and names every test whose result changes. Test code must unset CLAUDE_CONFIG_DIR and control which jq is on PATH, so results do not depend on the developer's machine.
- Edit only under src/superclaude/, plugins/superclaude/hooks/, tests/, docs/ and this package's ./artifacts/; run make sync-dev after hook or skill edits. The plugin copy of every hook script and hooks.json stays byte-identical to its src copy. Generated .claude/ mirrors made by make sync-dev stay out of the commit.
- UV only: run tests with uv run pytest.
- Findings of the issue analysis that this plan answers: F2 (Task 15), F3 (Task 14), F4 (Tasks 18 to 20), F6 (Task 22), F7 (Task 1). F5 (pending records are not pruned) is accepted under owner decision O-15 and is stated in Task 22.
Start sha: 10d7c8f8dac0d54b499bdfabb570e335c2c3eb2f
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t5-test.log b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t5-test.log
new file mode 100644
index 00000000..69ceafd8
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t5-test.log
@@ -0,0 +1,323 @@
+$ uv run pytest tests/hooks/test_launch_level_guard.py -v   (after the fix pass)
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0 -- /home/coder/workspaces/worktrees/IronClaude/issue-394-launch-level-hook/.venv/bin/python
+cachedir: .pytest_cache
+SuperClaude: 5.0.0
+rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-394-launch-level-hook
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, anyio-4.16.0
+collecting ... collected 311 items
+
+tests/hooks/test_launch_level_guard.py::test_script_is_executable_with_version_line PASSED [  0%]
+tests/hooks/test_launch_level_guard.py::test_script_text_never_names_the_joined_store_path PASSED [  0%]
+tests/hooks/test_launch_level_guard.py::test_script_passes_bash_syntax_check PASSED [  0%]
+tests/hooks/test_launch_level_guard.py::test_script_prints_no_amendment_marks PASSED [  1%]
+tests/hooks/test_launch_level_guard.py::test_empty_home_allows_silently[marker-prompt] PASSED [  1%]
+tests/hooks/test_launch_level_guard.py::test_empty_home_allows_silently[other-event] PASSED [  1%]
+tests/hooks/test_launch_level_guard.py::test_empty_home_allows_silently[pretooluse-bash] PASSED [  2%]
+tests/hooks/test_launch_level_guard.py::test_empty_home_allows_silently[pretooluse-skill] PASSED [  2%]
+tests/hooks/test_launch_level_guard.py::test_empty_home_allows_silently[prompt] PASSED [  2%]
+tests/hooks/test_launch_level_guard.py::test_empty_home_without_jq_allows_silently PASSED [  3%]
+tests/hooks/test_launch_level_guard.py::test_unbound_session_with_nonempty_store_allows_silently[marker-prompt] PASSED [  3%]
+tests/hooks/test_launch_level_guard.py::test_unbound_session_with_nonempty_store_allows_silently[other-event] PASSED [  3%]
+tests/hooks/test_launch_level_guard.py::test_unbound_session_with_nonempty_store_allows_silently[pretooluse-bash] PASSED [  4%]
+tests/hooks/test_launch_level_guard.py::test_unbound_session_with_nonempty_store_allows_silently[pretooluse-skill] PASSED [  4%]
+tests/hooks/test_launch_level_guard.py::test_unbound_session_with_nonempty_store_allows_silently[prompt] PASSED [  4%]
+tests/hooks/test_launch_level_guard.py::test_other_event_unbound_allows_silently[missing-event] PASSED [  5%]
+tests/hooks/test_launch_level_guard.py::test_other_event_unbound_allows_silently[nested-forged-event] PASSED [  5%]
+tests/hooks/test_launch_level_guard.py::test_other_event_unbound_allows_silently[numeric-event] PASSED [  5%]
+tests/hooks/test_launch_level_guard.py::test_other_event_unbound_allows_silently[post-tool-use] PASSED [  6%]
+tests/hooks/test_launch_level_guard.py::test_unparseable_envelope_allows_silently PASSED [  6%]
+tests/hooks/test_launch_level_guard.py::test_other_event_bound_session_blocks_broken[full-False-full-False] PASSED [  6%]
+tests/hooks/test_launch_level_guard.py::test_other_event_bound_session_blocks_broken[full-submit\n-False-full --submit-False] PASSED [  7%]
+tests/hooks/test_launch_level_guard.py::test_other_event_bound_session_blocks_broken[worktree-True-worktree (approved)-False] PASSED [  7%]
+tests/hooks/test_launch_level_guard.py::test_other_event_bound_session_blocks_broken[garbage-False-worktree-True] PASSED [  7%]
+tests/hooks/test_launch_level_guard.py::test_trap_in_tool_branch_gives_broken PASSED [  8%]
+tests/hooks/test_launch_level_guard.py::test_trap_in_prompt_branch_gives_nobind PASSED [  8%]
+tests/hooks/test_launch_level_guard.py::test_trap_never_blocks_an_ordinary_session[tool-pretooluse-bash] PASSED [  8%]
+tests/hooks/test_launch_level_guard.py::test_trap_never_blocks_an_ordinary_session[prompt-prompt] PASSED [  9%]
+tests/hooks/test_launch_level_guard.py::test_trap_after_marker_gives_nobind_bare_header PASSED [  9%]
+tests/hooks/test_launch_level_guard.py::test_bind_marker_with_record_binds_level[worktree] PASSED [  9%]
+tests/hooks/test_launch_level_guard.py::test_bind_marker_with_record_binds_level[full] PASSED [  9%]
+tests/hooks/test_launch_level_guard.py::test_bind_marker_with_record_binds_level[full-submit] PASSED [ 10%]
+tests/hooks/test_launch_level_guard.py::test_bind_marker_at_start_without_record_binds_degraded PASSED [ 10%]
+tests/hooks/test_launch_level_guard.py::test_bind_malformed_marker_at_start_binds_degraded[[sc-launch:v1:ABCDEF0123456789ABCDEF0123456789]] PASSED [ 10%]
+tests/hooks/test_launch_level_guard.py::test_bind_malformed_marker_at_start_binds_degraded[[sc-launch:v1:01234567-89ab-cdef-0123-456789abcdef]] PASSED [ 11%]
+tests/hooks/test_launch_level_guard.py::test_bind_malformed_marker_at_start_binds_degraded[[sc-launch:v1:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa]] PASSED [ 11%]
+tests/hooks/test_launch_level_guard.py::test_bind_malformed_marker_at_start_binds_degraded[[sc-launch:v2:0123456789abcdef0123456789abcdef]] PASSED [ 11%]
+tests/hooks/test_launch_level_guard.py::test_bind_malformed_marker_at_start_binds_degraded[[sc-launch:v1:<nonce>]] PASSED [ 12%]
+tests/hooks/test_launch_level_guard.py::test_bind_marker_after_whitespace_or_bom_binds[   ] PASSED [ 12%]
+tests/hooks/test_launch_level_guard.py::test_bind_marker_after_whitespace_or_bom_binds[\n\n] PASSED [ 12%]
+tests/hooks/test_launch_level_guard.py::test_bind_marker_after_whitespace_or_bom_binds[\t\r\n ] PASSED [ 13%]
+tests/hooks/test_launch_level_guard.py::test_bind_marker_after_whitespace_or_bom_binds[\ufeff] PASSED [ 13%]
+tests/hooks/test_launch_level_guard.py::test_bind_marker_after_whitespace_or_bom_binds[ \ufeff\n\ufeff\t] PASSED [ 13%]
+tests/hooks/test_launch_level_guard.py::test_bind_loose_marker_after_whitespace_or_bom_binds_degraded[   ] PASSED [ 14%]
+tests/hooks/test_launch_level_guard.py::test_bind_loose_marker_after_whitespace_or_bom_binds_degraded[\n\n] PASSED [ 14%]
+tests/hooks/test_launch_level_guard.py::test_bind_loose_marker_after_whitespace_or_bom_binds_degraded[\t\r\n ] PASSED [ 14%]
+tests/hooks/test_launch_level_guard.py::test_bind_loose_marker_after_whitespace_or_bom_binds_degraded[\ufeff] PASSED [ 15%]
+tests/hooks/test_launch_level_guard.py::test_bind_loose_marker_after_whitespace_or_bom_binds_degraded[ \ufeff\n\ufeff\t] PASSED [ 15%]
+tests/hooks/test_launch_level_guard.py::test_bind_strict_marker_mid_prompt_with_record_binds PASSED [ 15%]
+tests/hooks/test_launch_level_guard.py::test_bind_strict_marker_mid_prompt_without_record_blocks_prompt PASSED [ 16%]
+tests/hooks/test_launch_level_guard.py::test_bind_failure_blocks_prompt PASSED [ 16%]
+tests/hooks/test_launch_level_guard.py::test_bind_sessions_dir_created PASSED [ 16%]
+tests/hooks/test_launch_level_guard.py::test_bind_nonce_single_use PASSED [ 17%]
+tests/hooks/test_launch_level_guard.py::test_bind_later_marker_consumes_record_keeps_level[worktree] PASSED [ 17%]
+tests/hooks/test_launch_level_guard.py::test_bind_later_marker_consumes_record_keeps_level[garbage] PASSED [ 17%]
+tests/hooks/test_launch_level_guard.py::test_bind_later_marker_consumes_record_keeps_level[] PASSED [ 18%]
+tests/hooks/test_launch_level_guard.py::test_bind_resume_same_id_governed PASSED [ 18%]
+tests/hooks/test_launch_level_guard.py::test_bind_rename_still_governed PASSED [ 18%]
+tests/hooks/test_launch_level_guard.py::test_bind_reclaim_new_session_new_level PASSED [ 18%]
+tests/hooks/test_launch_level_guard.py::test_bind_invalid_session_ids[.] PASSED [ 19%]
+tests/hooks/test_launch_level_guard.py::test_bind_invalid_session_ids[..] PASSED [ 19%]
+tests/hooks/test_launch_level_guard.py::test_bind_invalid_session_ids[x.ok] PASSED [ 19%]
+tests/hooks/test_launch_level_guard.py::test_bind_invalid_session_ids[a/b] PASSED [ 20%]
+tests/hooks/test_launch_level_guard.py::test_bind_invalid_session_ids[] PASSED [ 20%]
+tests/hooks/test_launch_level_guard.py::test_bind_invalid_session_ids[sid5] PASSED [ 20%]
+tests/hooks/test_launch_level_guard.py::test_bind_invalid_session_ids[7] PASSED [ 21%]
+tests/hooks/test_launch_level_guard.py::test_bind_invalid_session_ids[sid7] PASSED [ 21%]
+tests/hooks/test_launch_level_guard.py::test_bind_invalid_session_ids[None] PASSED [ 21%]
+tests/hooks/test_launch_level_guard.py::test_bind_marker_prompt_with_agent_id_ignored[agent-1] PASSED [ 22%]
+tests/hooks/test_launch_level_guard.py::test_bind_marker_prompt_with_agent_id_ignored[x] PASSED [ 22%]
+tests/hooks/test_launch_level_guard.py::test_bind_jq_missing_marker_prompt_blocked PASSED [ 22%]
+tests/hooks/test_launch_level_guard.py::test_bind_unparseable_marker_prompt_blocked PASSED [ 23%]
+tests/hooks/test_launch_level_guard.py::test_bind_loose_marker_mid_prompt_ignored[False] PASSED [ 23%]
+tests/hooks/test_launch_level_guard.py::test_bind_loose_marker_mid_prompt_ignored[True] PASSED [ 23%]
+tests/hooks/test_launch_level_guard.py::test_bind_two_sessions_isolated PASSED [ 24%]
+tests/hooks/test_launch_level_guard.py::test_bind_same_worktree_other_session_ordinary PASSED [ 24%]
+tests/hooks/test_launch_level_guard.py::test_bind_person_subagent_not_governed PASSED [ 24%]
+tests/hooks/test_launch_level_guard.py::test_bind_forged_nested_session_id PASSED [ 25%]
+tests/hooks/test_launch_level_guard.py::test_bind_jq_missing_ordinary_prompt_allows PASSED [ 25%]
+tests/hooks/test_launch_level_guard.py::test_bind_concurrent_same_session_same_nonce PASSED [ 25%]
+tests/hooks/test_launch_level_guard.py::test_bind_concurrent_other_sessions_same_nonce PASSED [ 26%]
+tests/hooks/test_launch_level_guard.py::test_bind_race_winner_level_governs_tool_calls PASSED [ 26%]
+tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[-F] PASSED [ 26%]
+tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[-FS] PASSED [ 27%]
+tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[-W] PASSED [ 27%]
+tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[-WA] PASSED [ 27%]
+tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[sc:implement-F] PASSED [ 27%]
+tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[sc:implement-FS] PASSED [ 28%]
+tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[sc:implement-W] PASSED [ 28%]
+tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[sc:implement-WA] PASSED [ 28%]
+tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[sc:issue-F] PASSED [ 29%]
+tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[sc:issue-FS] PASSED [ 29%]
+tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[sc:issue-W] PASSED [ 29%]
+tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[sc:issue-WA] PASSED [ 30%]
+tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[sc:pr-submit-F] PASSED [ 30%]
+tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[sc:pr-submit-FS] PASSED [ 30%]
+tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[sc:pr-submit-W] PASSED [ 31%]
+tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[sc:pr-submit-WA] PASSED [ 31%]
+tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[sc:workflow-F] PASSED [ 31%]
+tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[sc:workflow-FS] PASSED [ 32%]
+tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[sc:workflow-W] PASSED [ 32%]
+tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[sc:workflow-WA] PASSED [ 32%]
+tests/hooks/test_launch_level_guard.py::test_impl_name_spellings[sc:implement] PASSED [ 33%]
+tests/hooks/test_launch_level_guard.py::test_impl_name_spellings[sc:implement-protocol] PASSED [ 33%]
+tests/hooks/test_launch_level_guard.py::test_impl_name_spellings[sc-implement-protocol] PASSED [ 33%]
+tests/hooks/test_launch_level_guard.py::test_impl_name_spellings[task] PASSED [ 34%]
+tests/hooks/test_launch_level_guard.py::test_impl_name_spellings[sc:task] PASSED [ 34%]
+tests/hooks/test_launch_level_guard.py::test_impl_name_spellings[sc:task-protocol] PASSED [ 34%]
+tests/hooks/test_launch_level_guard.py::test_impl_name_spellings[sc:improve] PASSED [ 35%]
+tests/hooks/test_launch_level_guard.py::test_impl_name_spellings[sc:cleanup] PASSED [ 35%]
+tests/hooks/test_launch_level_guard.py::test_impl_name_spellings[sc:spawn] PASSED [ 35%]
+tests/hooks/test_launch_level_guard.py::test_impl_name_spellings[sc:build] PASSED [ 36%]
+tests/hooks/test_launch_level_guard.py::test_impl_name_spellings[SC:IMPLEMENT] PASSED [ 36%]
+tests/hooks/test_launch_level_guard.py::test_impl_name_spellings[/sc:implement args] PASSED [ 36%]
+tests/hooks/test_launch_level_guard.py::test_impl_name_spellings[superclaude:sc-implement-protocol] PASSED [ 36%]
+tests/hooks/test_launch_level_guard.py::test_impl_name_spellings[ \t\nsc:implement] PASSED [ 37%]
+tests/hooks/test_launch_level_guard.py::test_lookalike_skill_names_stay_none[sc:cleanup-audit-protocol] PASSED [ 37%]
+tests/hooks/test_launch_level_guard.py::test_lookalike_skill_names_stay_none[task-builder] PASSED [ 37%]
+tests/hooks/test_launch_level_guard.py::test_lookalike_skill_names_stay_none[sc:tasklist-protocol] PASSED [ 38%]
+tests/hooks/test_launch_level_guard.py::test_submit_name_spellings[F-sc:pr-submit] PASSED [ 38%]
+tests/hooks/test_launch_level_guard.py::test_submit_name_spellings[F-sc:pr-submit-protocol] PASSED [ 38%]
+tests/hooks/test_launch_level_guard.py::test_submit_name_spellings[FS-sc:pr-submit] PASSED [ 39%]
+tests/hooks/test_launch_level_guard.py::test_submit_name_spellings[FS-sc:pr-submit-protocol] PASSED [ 39%]
+tests/hooks/test_launch_level_guard.py::test_submit_name_spellings[W-sc:pr-submit] PASSED [ 39%]
+tests/hooks/test_launch_level_guard.py::test_submit_name_spellings[W-sc:pr-submit-protocol] PASSED [ 40%]
+tests/hooks/test_launch_level_guard.py::test_submit_name_spellings[WA-sc:pr-submit] PASSED [ 40%]
+tests/hooks/test_launch_level_guard.py::test_submit_name_spellings[WA-sc:pr-submit-protocol] PASSED [ 40%]
+tests/hooks/test_launch_level_guard.py::test_skill_name_keys[tool_input0] PASSED [ 41%]
+tests/hooks/test_launch_level_guard.py::test_skill_name_keys[tool_input1] PASSED [ 41%]
+tests/hooks/test_launch_level_guard.py::test_skill_name_keys[tool_input2] PASSED [ 41%]
+tests/hooks/test_launch_level_guard.py::test_skill_name_keys[tool_input3] PASSED [ 42%]
+tests/hooks/test_launch_level_guard.py::test_explicit_empty_skill_does_not_fall_back_to_name PASSED [ 42%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[F-name0] PASSED [ 42%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[F-] PASSED [ 43%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[F-   ] PASSED [ 43%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[F-\t\n] PASSED [ 43%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[F-/] PASSED [ 44%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[F-sc:] PASSED [ 44%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[F-sc:sc--protocol] PASSED [ 44%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[FS-name0] PASSED [ 45%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[FS-] PASSED [ 45%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[FS-   ] PASSED [ 45%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[FS-\t\n] PASSED [ 45%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[FS-/] PASSED [ 46%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[FS-sc:] PASSED [ 46%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[FS-sc:sc--protocol] PASSED [ 46%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[W-name0] PASSED [ 47%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[W-] PASSED [ 47%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[W-   ] PASSED [ 47%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[W-\t\n] PASSED [ 48%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[W-/] PASSED [ 48%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[W-sc:] PASSED [ 48%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[W-sc:sc--protocol] PASSED [ 49%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[WA-name0] PASSED [ 49%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[WA-] PASSED [ 49%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[WA-   ] PASSED [ 50%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[WA-\t\n] PASSED [ 50%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[WA-/] PASSED [ 50%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[WA-sc:] PASSED [ 51%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[WA-sc:sc--protocol] PASSED [ 51%]
+tests/hooks/test_launch_level_guard.py::test_issue_skill_escape[F-sc:issue] PASSED [ 51%]
+tests/hooks/test_launch_level_guard.py::test_issue_skill_escape[F-sc:issue-protocol] PASSED [ 52%]
+tests/hooks/test_launch_level_guard.py::test_issue_skill_escape[FS-sc:issue] PASSED [ 52%]
+tests/hooks/test_launch_level_guard.py::test_issue_skill_escape[FS-sc:issue-protocol] PASSED [ 52%]
+tests/hooks/test_launch_level_guard.py::test_issue_skill_escape[W-sc:issue] PASSED [ 53%]
+tests/hooks/test_launch_level_guard.py::test_issue_skill_escape[W-sc:issue-protocol] PASSED [ 53%]
+tests/hooks/test_launch_level_guard.py::test_issue_skill_escape[WA-sc:issue] PASSED [ 53%]
+tests/hooks/test_launch_level_guard.py::test_issue_skill_escape[WA-sc:issue-protocol] PASSED [ 54%]
+tests/hooks/test_launch_level_guard.py::test_skill_name_newline_does_not_shift_fields PASSED [ 54%]
+tests/hooks/test_launch_level_guard.py::test_huge_fields_are_quick PASSED [ 54%]
+tests/hooks/test_launch_level_guard.py::test_other_tools_are_none_until_their_classifiers_exist[Bash-tool_input0] PASSED [ 54%]
+tests/hooks/test_launch_level_guard.py::test_other_tools_are_none_until_their_classifiers_exist[Edit-tool_input1] PASSED [ 55%]
+tests/hooks/test_launch_level_guard.py::test_other_tools_are_none_until_their_classifiers_exist[Agent-tool_input2] PASSED [ 55%]
+tests/hooks/test_launch_level_guard.py::test_other_tools_are_none_until_their_classifiers_exist[Read-tool_input3] PASSED [ 55%]
+tests/hooks/test_launch_level_guard.py::test_other_tools_are_none_until_their_classifiers_exist[mcp__github__merge_pull_request-tool_input4] PASSED [ 56%]
+tests/hooks/test_launch_level_guard.py::test_input_error_blocks_governed_broken[bool-isolation] PASSED [ 56%]
+tests/hooks/test_launch_level_guard.py::test_input_error_blocks_governed_broken[list-path] PASSED [ 56%]
+tests/hooks/test_launch_level_guard.py::test_input_error_blocks_governed_broken[list-tool-input] PASSED [ 57%]
+tests/hooks/test_launch_level_guard.py::test_input_error_blocks_governed_broken[nul-command] PASSED [ 57%]
+tests/hooks/test_launch_level_guard.py::test_input_error_blocks_governed_broken[nul-skill] PASSED [ 57%]
+tests/hooks/test_launch_level_guard.py::test_input_error_blocks_governed_broken[numeric-command] PASSED [ 58%]
+tests/hooks/test_launch_level_guard.py::test_input_error_blocks_governed_broken[numeric-skill] PASSED [ 58%]
+tests/hooks/test_launch_level_guard.py::test_input_error_blocks_governed_broken[numeric-tool-name] PASSED [ 58%]
+tests/hooks/test_launch_level_guard.py::test_input_error_blocks_governed_broken[object-name] PASSED [ 59%]
+tests/hooks/test_launch_level_guard.py::test_input_error_allows_ordinary[bool-isolation] PASSED [ 59%]
+tests/hooks/test_launch_level_guard.py::test_input_error_allows_ordinary[list-path] PASSED [ 59%]
+tests/hooks/test_launch_level_guard.py::test_input_error_allows_ordinary[list-tool-input] PASSED [ 60%]
+tests/hooks/test_launch_level_guard.py::test_input_error_allows_ordinary[nul-command] PASSED [ 60%]
+tests/hooks/test_launch_level_guard.py::test_input_error_allows_ordinary[nul-skill] PASSED [ 60%]
+tests/hooks/test_launch_level_guard.py::test_input_error_allows_ordinary[numeric-command] PASSED [ 61%]
+tests/hooks/test_launch_level_guard.py::test_input_error_allows_ordinary[numeric-skill] PASSED [ 61%]
+tests/hooks/test_launch_level_guard.py::test_input_error_allows_ordinary[numeric-tool-name] PASSED [ 61%]
+tests/hooks/test_launch_level_guard.py::test_input_error_allows_ordinary[object-name] PASSED [ 62%]
+tests/hooks/test_launch_level_guard.py::test_ordinary_session_never_blocked[-empty] PASSED [ 62%]
+tests/hooks/test_launch_level_guard.py::test_ordinary_session_never_blocked[-other-sessions] PASSED [ 62%]
+tests/hooks/test_launch_level_guard.py::test_ordinary_session_never_blocked[sc:implement-empty] PASSED [ 63%]
+tests/hooks/test_launch_level_guard.py::test_ordinary_session_never_blocked[sc:implement-other-sessions] PASSED [ 63%]
+tests/hooks/test_launch_level_guard.py::test_ordinary_session_never_blocked[sc:issue-empty] PASSED [ 63%]
+tests/hooks/test_launch_level_guard.py::test_ordinary_session_never_blocked[sc:issue-other-sessions] PASSED [ 63%]
+tests/hooks/test_launch_level_guard.py::test_ordinary_session_never_blocked[sc:pr-submit-empty] PASSED [ 64%]
+tests/hooks/test_launch_level_guard.py::test_ordinary_session_never_blocked[sc:pr-submit-other-sessions] PASSED [ 64%]
+tests/hooks/test_launch_level_guard.py::test_ordinary_session_never_blocked[sc:workflow-empty] PASSED [ 64%]
+tests/hooks/test_launch_level_guard.py::test_ordinary_session_never_blocked[sc:workflow-other-sessions] PASSED [ 65%]
+tests/hooks/test_launch_level_guard.py::test_two_sessions_isolated PASSED [ 65%]
+tests/hooks/test_launch_level_guard.py::test_same_worktree_other_session_ordinary PASSED [ 65%]
+tests/hooks/test_launch_level_guard.py::test_person_subagent_not_governed PASSED [ 66%]
+tests/hooks/test_launch_level_guard.py::test_fail_open_shapes_ordinary[not-json] PASSED [ 66%]
+tests/hooks/test_launch_level_guard.py::test_fail_open_shapes_ordinary[truncated-unbound] PASSED [ 66%]
+tests/hooks/test_launch_level_guard.py::test_fail_open_shapes_ordinary[no-tool-input] PASSED [ 67%]
+tests/hooks/test_launch_level_guard.py::test_fail_open_shapes_ordinary[unknown-tool] PASSED [ 67%]
+tests/hooks/test_launch_level_guard.py::test_forged_nested_session_id PASSED [ 67%]
+tests/hooks/test_launch_level_guard.py::test_subagent_governed PASSED    [ 68%]
+tests/hooks/test_launch_level_guard.py::test_nested_subagent_governed PASSED [ 68%]
+tests/hooks/test_launch_level_guard.py::test_identity_loss_allows_silently[missing] PASSED [ 68%]
+tests/hooks/test_launch_level_guard.py::test_identity_loss_allows_silently[invalid] PASSED [ 69%]
+tests/hooks/test_launch_level_guard.py::test_identity_loss_allows_silently[numeric] PASSED [ 69%]
+tests/hooks/test_launch_level_guard.py::test_identity_loss_allows_silently[nested-forged] PASSED [ 69%]
+tests/hooks/test_launch_level_guard.py::test_identity_loss_allows_silently[unparseable] PASSED [ 70%]
+tests/hooks/test_launch_level_guard.py::test_jq_missing[True] PASSED     [ 70%]
+tests/hooks/test_launch_level_guard.py::test_jq_missing[False] PASSED    [ 70%]
+tests/hooks/test_launch_level_guard.py::test_bad_state_degrades_to_worktree[False-empty] PASSED [ 71%]
+tests/hooks/test_launch_level_guard.py::test_bad_state_degrades_to_worktree[False-garbage] PASSED [ 71%]
+tests/hooks/test_launch_level_guard.py::test_bad_state_degrades_to_worktree[False-degraded] PASSED [ 71%]
+tests/hooks/test_launch_level_guard.py::test_bad_state_degrades_to_worktree[False-mode-000] PASSED [ 72%]
+tests/hooks/test_launch_level_guard.py::test_bad_state_degrades_to_worktree[True-empty] PASSED [ 72%]
+tests/hooks/test_launch_level_guard.py::test_bad_state_degrades_to_worktree[True-garbage] PASSED [ 72%]
+tests/hooks/test_launch_level_guard.py::test_bad_state_degrades_to_worktree[True-degraded] PASSED [ 72%]
+tests/hooks/test_launch_level_guard.py::test_bad_state_degrades_to_worktree[True-mode-000] PASSED [ 73%]
+tests/hooks/test_launch_level_guard.py::test_not_json_governed[truncated] PASSED [ 73%]
+tests/hooks/test_launch_level_guard.py::test_not_json_governed[bound-id-after-another] PASSED [ 73%]
+tests/hooks/test_launch_level_guard.py::test_raw_id_scan_has_no_cap[10] PASSED [ 74%]
+tests/hooks/test_launch_level_guard.py::test_raw_id_scan_has_no_cap[70] PASSED [ 74%]
+tests/hooks/test_launch_level_guard.py::test_raw_id_scan_has_no_cap[500] PASSED [ 74%]
+tests/hooks/test_launch_level_guard.py::test_raw_id_scan_declared_limit_blocks_ordinary_with_nested_bound_id PASSED [ 75%]
+tests/hooks/test_launch_level_guard.py::test_design_table_holds_all_eighteen_ids PASSED [ 75%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-IMPL] PASSED [ 75%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-COMMIT] PASSED [ 76%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-PUSH] PASSED [ 76%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-PUSH-FORM] PASSED [ 76%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-PROTECTED] PASSED [ 77%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-MERGE] PASSED [ 77%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-GH-WRITE] PASSED [ 77%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-SUBMIT] PASSED [ 78%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-REPO] PASSED [ 78%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-UNKNOWN] PASSED [ 78%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-MCP] PASSED [ 79%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-ESCAPE] PASSED [ 79%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-TURN] PASSED [ 79%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-TAMPER] PASSED [ 80%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-SKILL] PASSED [ 80%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-BIG] PASSED [ 80%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-BROKEN] PASSED [ 81%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-NOBIND] PASSED [ 81%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-IMPL] PASSED [ 81%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-COMMIT] PASSED [ 81%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-PUSH] PASSED [ 82%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-PUSH-FORM] PASSED [ 82%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-PROTECTED] PASSED [ 82%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-MERGE] PASSED [ 83%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-GH-WRITE] PASSED [ 83%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-SUBMIT] PASSED [ 83%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-REPO] PASSED [ 84%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-UNKNOWN] PASSED [ 84%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-MCP] PASSED [ 84%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-ESCAPE] PASSED [ 85%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-TURN] PASSED [ 85%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-TAMPER] PASSED [ 85%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-SKILL] PASSED [ 86%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-BIG] PASSED [ 86%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-BROKEN] PASSED [ 86%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-NOBIND] PASSED [ 87%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-IMPL] PASSED [ 87%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-COMMIT] PASSED [ 87%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-PUSH] PASSED [ 88%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-PUSH-FORM] PASSED [ 88%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-PROTECTED] PASSED [ 88%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-MERGE] PASSED [ 89%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-GH-WRITE] PASSED [ 89%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-SUBMIT] PASSED [ 89%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-REPO] PASSED [ 90%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-UNKNOWN] PASSED [ 90%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-MCP] PASSED [ 90%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-ESCAPE] PASSED [ 90%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-TURN] PASSED [ 91%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-TAMPER] PASSED [ 91%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-SKILL] PASSED [ 91%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-BIG] PASSED [ 92%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-BROKEN] PASSED [ 92%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-NOBIND] PASSED [ 92%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[WA-LL-IMPL] PASSED [ 93%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[WA-LL-COMMIT] PASSED [ 93%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[WA-LL-PUSH] PASSED [ 93%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[WA-LL-PUSH-FORM] PASSED [ 94%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[WA-LL-PROTECTED] PASSED [ 94%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[WA-LL-MERGE] PASSED [ 94%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[WA-LL-GH-WRITE] PASSED [ 95%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[WA-LL-SUBMIT] PASSED [ 95%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[WA-LL-REPO] PASSED [ 95%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[WA-LL-UNKNOWN] PASSED [ 96%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[WA-LL-MCP] PASSED [ 96%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[WA-LL-ESCAPE] PASSED [ 96%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[WA-LL-TURN] PASSED [ 97%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[WA-LL-TAMPER] PASSED [ 97%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[WA-LL-SKILL] PASSED [ 97%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[WA-LL-BIG] PASSED [ 98%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[WA-LL-BROKEN] PASSED [ 98%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[WA-LL-NOBIND] PASSED [ 98%]
+tests/hooks/test_launch_level_guard.py::test_unknown_level_prints_bare_header[LL-BROKEN] PASSED [ 99%]
+tests/hooks/test_launch_level_guard.py::test_unknown_level_prints_bare_header[LL-NOBIND] PASSED [ 99%]
+tests/hooks/test_launch_level_guard.py::test_tamper_with_invalid_sid_uses_broken_wording PASSED [ 99%]
+tests/hooks/test_launch_level_guard.py::test_notes_follow_the_lines_state_first PASSED [100%]
+
+============================= 311 passed in 3.94s ==============================
diff --git a/src/superclaude/hooks/scripts/launch-level-guard.sh b/src/superclaude/hooks/scripts/launch-level-guard.sh
index 951e06eb..244f75aa 100755
--- a/src/superclaude/hooks/scripts/launch-level-guard.sh
+++ b/src/superclaude/hooks/scripts/launch-level-guard.sh
@@ -5,7 +5,8 @@
 # with a message on stderr; never exit 1, no onFailure. Only a session that the
 # claim script launched (a valid top-level session_id bound in the store) is
 # governed; every other session is ordinary and never blocked (FR-L-53).
-# Ten-part layout (DD-1); parts 5 and 6 are stubs until Tasks 4 and 5.
+# Ten-part layout (DD-1); Task 5 classifies Skill calls only, so until Tasks 6
+# to 10 add their classifiers every other tool call classifies as NONE.
 # launch-level-guard-version: 1
 
 # 1. Settings
@@ -170,36 +171,85 @@ if [ ! -d "$LL_STORE/sessions" ]; then
     *) exit 0 ;;
     esac
 fi
-# One parse of the top-level event, session id and, for a prompt only, the
-# agent_id flag and the prompt text (NUL made a space). Nested keys never count.
+# One parse of the top-level fields (FR-L-10; also part 7, the tool fields).
+# Line 1: event, agent_id flag (prompt only), input-error flag, session id.
+# Lines 2 to 5: tool name, skill name (skill unless missing or null, else
+# name), edit path (file_path unless missing or null, else notebook_path),
+# isolation, each with CR and LF made spaces. Then the prompt (NUL made a
+# space) or the command, kept whole, and a "." so no trailing newline is lost.
+# A nonstring tool field, a NUL in one or a nonobject tool_input is an input
+# error. Nested keys never count; agent_id is never read on PreToolUse.
 LL_PARSED=$(jq -r '
+    def str: if type == "string" then . else "" end;
+    def line: str | split("\u0000") | join(" ") | gsub("[\r\n]"; " ");
     (.hook_event_name | if . == "UserPromptSubmit" or . == "PreToolUse" then . else "OTHER" end) as $e
+    | (if $e == "PreToolUse" then . else {} end) as $p
+    | ($p.tool_input) as $ti
+    | ($ti | if type == "object" then . else {} end) as $o
+    | ($p.tool_name) as $tn
+    | ($tn | str) as $t
+    | (if $t != "Skill" then null elif $o.skill != null then $o.skill else $o.name end) as $sk
+    | (if ($t == "Edit" or $t == "Write" or $t == "NotebookEdit") | not then null
+        elif $o.file_path != null then $o.file_path else $o.notebook_path end) as $fp
+    | (if $t == "Agent" or $t == "Task" then $o.isolation else null end) as $iso
+    | (if $t == "Bash" or $t == "Monitor" then $o.command else null end) as $cmd
+    | (any($tn, $sk, $fp, $iso, $cmd; . != null and (type != "string" or (explode | any(. == 0))))
+        or ($ti != null and ($ti | type) != "object")) as $bad
     | $e + " "
     + (if $e == "UserPromptSubmit" then (.agent_id | if type == "string" and length > 0 then "1" else "0" end) else "0" end)
-    + " "
+    + " " + (if $bad then "1" else "0" end) + " "
     + (.session_id | if type == "string" and test("\\A[A-Za-z0-9][A-Za-z0-9_-]{0,127}\\z") then . else "" end)
-    + "\n"
-    + (if $e == "UserPromptSubmit" then (.prompt | if type == "string" then split("\u0000") | join(" ") else "" end) else "" end)
+    + "\n" + ($t | line) + "\n" + ($sk | line) + "\n" + ($fp | line) + "\n" + ($iso | line) + "\n"
+    + (if $e == "UserPromptSubmit" then .prompt else $cmd end | str | split("\u0000") | join(" "))
+    + "."
 ' <<<"$LL_INPUT" 2>/dev/null)
 LL_RC=$?
+LL_BAD=0 LL_TOOL= LL_SKILL= LL_PATH= LL_ISO= LL_TEXT= LL_PROMPT=
 if [ "$LL_RC" != 0 ]; then
-    # No jq or no parseable envelope: never infer a binding. A recognizable
-    # launch-marker prompt (marker text, no tool_name key) blocks rather than
-    # starting ungoverned; anything else is identity loss (section 3): allow
-    # without claiming enforcement.
+    # No jq or no parseable envelope: no level is inferred. A tool payload
+    # looks at every session_id value for one that has a record, only to find a
+    # positively bound session, which then falls through to the last line
+    # (LL-BROKEN); this can only block, never allow early. Declared limit: any
+    # bound id in the text counts, even a nested one, so an ordinary session
+    # sending broken JSON that contains a bound id is blocked. A recognizable launch-marker
+    # prompt (marker text, no tool_name key) blocks rather than starting
+    # ungoverned; anything else is identity loss (section 3): allow without
+    # claiming enforcement.
     case $LL_INPUT in
-    *'"tool_name"'*) ;;
+    *'"tool_name"'*)
+        LL_EVENT=FAILED
+        LL_RAWRE='"session_id"[[:space:]]*:[[:space:]]*"([A-Za-z0-9][A-Za-z0-9_-]{0,127})"(.*)'
+        LL_REST=$LL_INPUT
+        # No cap on the number of session_id values tried (a cap would let a payload with many forged ids hide the real bound one).
+        while :; do
+            [[ $LL_REST =~ $LL_RAWRE ]] || break
+            LL_REST=${BASH_REMATCH[2]}
+            if [ -e "$LL_STORE/sessions/${BASH_REMATCH[1]}" ] || [ -L "$LL_STORE/sessions/${BASH_REMATCH[1]}" ]; then
+                LL_SID=${BASH_REMATCH[1]}
+                break
+            fi
+        done
+        LL_REST= ;;
     *'[sc-launch:'*)
         LL_BRANCH=prompt
         LL_GOVERNED=1
         ll_deny LL-NOBIND ;;
+    *) exit 0 ;;
     esac
-    exit 0
+else
+    # read, not ${var#*$'\n'}: pattern removal is quadratic on a long line.
+    {
+        read -r LL_EVENT LL_AGENT LL_BAD LL_SID
+        IFS= read -r LL_TOOL
+        IFS= read -r LL_SKILL
+        IFS= read -r LL_PATH
+        IFS= read -r LL_ISO
+        IFS= read -r -d '' LL_TEXT
+    } <<<"$LL_PARSED"
+    LL_SID=${LL_SID:-}
+    LL_TEXT=${LL_TEXT%$'.\n'} # the here-string adds the newline after the "."
+    [ "$LL_EVENT" = UserPromptSubmit ] && LL_PROMPT=$LL_TEXT
 fi
-read -r LL_EVENT LL_AGENT LL_SID <<<"${LL_PARSED%%$'\n'*}"
-LL_SID=${LL_SID:-}
-LL_PROMPT=
-case $LL_PARSED in *$'\n'*) LL_PROMPT=${LL_PARSED#*$'\n'} ;; esac
 
 # A valid id with a record (of any file kind) is positively governed. Its level
 # is exactly one allowed word plus an optional newline; anything else is
@@ -314,14 +364,59 @@ if [ "$LL_BRANCH" = prompt ]; then
     ll_deny LL-NOBIND
 fi
 
-# 6. Fast paths
+# 6. Fast paths. An unbound valid id allows silently; a missing or invalid id is
+# identity loss, a declared fail-open limit (section 3). agent_id is never read
+# here and there is no cwd fallback.
 if [ "$LL_BRANCH" = tool ]; then
-    exit 0 # stub: tool branch
-fi
+    [ "$LL_GOVERNED" = 1 ] || exit 0 # unbound or identity loss
+    [ "$LL_BAD" = 1 ] && ll_deny LL-BROKEN # a nonstring tool field or an embedded NUL
+
+    # 7. The tool fields come from the one jq parse in part 4.
+    # 8. Classifiers add classes to LL_CLASSES (Tasks 5 to 10); none gives NONE.
+    LL_CLASSES=' '
+    if [ "$LL_TOOL" = Skill ]; then
+        # FR-L-40: first word, lower case, one leading "/", text after the last
+        # ":", one leading "sc-", one trailing "-protocol".
+        LL_N=
+        [[ $LL_SKILL =~ ^[[:space:]]*([^[:space:]]*) ]] && LL_N=${BASH_REMATCH[1]}
+        LL_N=${LL_N,,}
+        LL_N=${LL_N#/}
+        LL_N=${LL_N##*:}
+        LL_N=${LL_N#sc-}
+        LL_N=${LL_N%-protocol}
+        case $LL_N in
+        implement | task | improve | cleanup | spawn | build) LL_CLASSES+='IMPL ' ;;
+        pr-submit) LL_CLASSES+='SUBMIT ' ;;
+        issue) LL_CLASSES+='ESCAPE ' ;;
+        '') LL_CLASSES+='SKILL ' ;;
+        esac
+    fi
 
-# 7. One jq read of the tool fields (Task 5)
-# 8. Classifiers adding classes (Tasks 5 to 10)
-# 9. One case on CLASS:LEVEL (Task 5)
+    # 9. One case on CLASS:LEVEL, taken in message precedence; any blocked class
+    # blocks the call with the first blocked class's message.
+    for LL_C in BIG TAMPER MERGE GHWRITE PROTECTED ESCAPE MCP UNKNOWN SUBMIT REPO PUSH PUSHFORM COMMIT TURN IMPL SKILL; do
+        case $LL_CLASSES in *" $LL_C "*) ;; *) continue ;; esac
+        case $LL_C:$LL_LEVEL in
+        IMPL:WA | IMPL:F | IMPL:FS | TURN:WA | TURN:F | TURN:FS) ;;
+        SUBMIT:FS | COMMIT:FS | PUSH:FS | SKILL:FS) ;;
+        IMPL:W | TURN:W) ll_deny "LL-$LL_C" ;;
+        SUBMIT:W | SUBMIT:WA | SUBMIT:F | COMMIT:W | COMMIT:WA | COMMIT:F) ll_deny "LL-$LL_C" ;;
+        PUSH:W | PUSH:WA | PUSH:F | SKILL:W | SKILL:WA | SKILL:F) ll_deny "LL-$LL_C" ;;
+        REPO:W | REPO:WA | REPO:F | REPO:FS) ll_deny LL-REPO ;;
+        PUSHFORM:W | PUSHFORM:WA | PUSHFORM:F | PUSHFORM:FS) ll_deny LL-PUSH-FORM ;;
+        PROTECTED:W | PROTECTED:WA | PROTECTED:F | PROTECTED:FS) ll_deny LL-PROTECTED ;;
+        MERGE:W | MERGE:WA | MERGE:F | MERGE:FS) ll_deny LL-MERGE ;;
+        GHWRITE:W | GHWRITE:WA | GHWRITE:F | GHWRITE:FS) ll_deny LL-GH-WRITE ;;
+        UNKNOWN:W | UNKNOWN:WA | UNKNOWN:F | UNKNOWN:FS) ll_deny LL-UNKNOWN ;;
+        MCP:W | MCP:WA | MCP:F | MCP:FS) ll_deny LL-MCP ;;
+        ESCAPE:W | ESCAPE:WA | ESCAPE:F | ESCAPE:FS) ll_deny LL-ESCAPE ;;
+        TAMPER:W | TAMPER:WA | TAMPER:F | TAMPER:FS) ll_deny LL-TAMPER ;;
+        BIG:W | BIG:WA | BIG:F | BIG:FS) ll_deny LL-BIG ;;
+        *) ll_deny LL-BROKEN ;;
+        esac
+    done
+    exit 0
+fi
 
 # 10. Default deny
 ll_deny LL-BROKEN
diff --git a/tests/hooks/test_launch_level_guard.py b/tests/hooks/test_launch_level_guard.py
index ef016b67..9fa1a423 100644
--- a/tests/hooks/test_launch_level_guard.py
+++ b/tests/hooks/test_launch_level_guard.py
@@ -1,4 +1,4 @@
-"""Behavioral tests for launch-level-guard.sh (issue #394, plan Tasks 3 and 4).
+"""Behavioral tests for launch-level-guard.sh (issue #394, plan Tasks 3 to 5).
 
 Each case runs the real script with a JSON payload on stdin, HOME inside
 tmp_path, CLAUDE_CONFIG_DIR unset and a PATH holding only a temporary bin
@@ -218,7 +218,7 @@ def _printer(
 
 FAULT_LINES = {
     # First line of each branch; "marker" is the first write after a marker.
-    "tool": "exit 0 # stub: tool branch",
+    "tool": '[ "$LL_GOVERNED" = 1 ] || exit 0 # unbound or identity loss',
     "prompt": '[ "$LL_AGENT" = 1 ] && exit 0 # B5: a subagent prompt never binds or approves',
     "marker": 'mkdir -p -- "$LL_SESS" 2>/dev/null',
 }
@@ -741,6 +741,426 @@ def test_bind_concurrent_other_sessions_same_nonce(tmp_path):
     assert not record.exists()
 
 
+def test_bind_race_winner_level_governs_tool_calls(tmp_path):
+    # After the race, a PreToolUse call for the same id resolves the winner's level.
+    _pending(tmp_path, "worktree")
+    results = _race(tmp_path, [SID] * 8)
+    assert [r.returncode for r in results] == [0] * 8
+    result = _run(_skill("sc:implement"), tmp_path)
+    store = str(_store(tmp_path / "home"))
+    assert result.returncode == 2
+    assert result.stderr.decode() == _expected("LL-IMPL", "worktree", SID, store)
+
+
+# --- PreToolUse: Skill classifier and the policy grid (Task 5) -------------
+
+# Launch level -> (record word, .ok present).
+LEVEL_FILES = {
+    "W": ("worktree", False),
+    "WA": ("worktree", True),
+    "F": ("full", False),
+    "FS": ("full-submit", False),
+}
+
+# Hand-written oracle for the Skill rows of the grid (design section 8):
+# None allows, otherwise the message id the call is blocked with.
+EXPECTED = {
+    "sc:implement": {"W": "LL-IMPL", "WA": None, "F": None, "FS": None},
+    "sc:pr-submit": {"W": "LL-SUBMIT", "WA": "LL-SUBMIT", "F": "LL-SUBMIT", "FS": None},
+    "sc:issue": {
+        "W": "LL-ESCAPE",
+        "WA": "LL-ESCAPE",
+        "F": "LL-ESCAPE",
+        "FS": "LL-ESCAPE",
+    },
+    "": {"W": "LL-SKILL", "WA": "LL-SKILL", "F": "LL-SKILL", "FS": None},
+    "sc:workflow": {"W": None, "WA": None, "F": None, "FS": None},
+}
+
+_ABSENT = object()
+
+
+def _skill(name=_ABSENT, sid=SID, tool_input=None, **extra) -> dict:
+    """A Skill PreToolUse payload; name goes under tool_input.skill."""
+    tool_input = dict(tool_input or {})
+    if name is not _ABSENT:
+        tool_input["skill"] = name
+    payload = {"hook_event_name": "PreToolUse", "tool_name": "Skill", **extra}
+    payload["tool_input"] = tool_input
+    if sid is not None:
+        payload["session_id"] = sid
+    return payload
+
+
+def _assert_decision(result, tmp_path, msg_id, level, note=False):
+    if msg_id is None:
+        assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
+        return
+    store = str(_store(tmp_path / "home"))
+    expected = _expected(msg_id, LEVELS[level], SID, store)
+    if note:
+        expected += STATE_NOTE + "\n"
+    assert result.returncode == 2
+    assert result.stdout == b""
+    assert result.stderr.decode() == expected
+
+
+@pytest.mark.parametrize("level", sorted(LEVEL_FILES))
+@pytest.mark.parametrize("name", sorted(EXPECTED))
+def test_skill_grid_matches_oracle(tmp_path, name, level):
+    _bind(tmp_path, *LEVEL_FILES[level])
+    result = _run(_skill(name), tmp_path)
+    _assert_decision(result, tmp_path, EXPECTED[name][level], level)
+
+
+IMPL_SPELLINGS = [
+    "sc:implement",
+    "sc:implement-protocol",
+    "sc-implement-protocol",
+    "task",
+    "sc:task",
+    "sc:task-protocol",
+    "sc:improve",
+    "sc:cleanup",
+    "sc:spawn",
+    "sc:build",
+    "SC:IMPLEMENT",
+    "/sc:implement args",
+    "superclaude:sc-implement-protocol",
+    " \t\nsc:implement",
+]
+
+
+@pytest.mark.parametrize("name", IMPL_SPELLINGS)
+def test_impl_name_spellings(tmp_path, name):
+    # T-SKL-1
+    _bind(tmp_path, "worktree")
+    _assert_decision(_run(_skill(name), tmp_path), tmp_path, "LL-IMPL", "W")
+
+
+@pytest.mark.parametrize(
+    "name", ["sc:cleanup-audit-protocol", "task-builder", "sc:tasklist-protocol"]
+)
+def test_lookalike_skill_names_stay_none(tmp_path, name):
+    # T-SKL-1: names that only resemble an IMPL skill are NONE.
+    _bind(tmp_path, "worktree")
+    _assert_decision(_run(_skill(name), tmp_path), tmp_path, None, "W")
+
+
+@pytest.mark.parametrize("name", ["sc:pr-submit", "sc:pr-submit-protocol"])
+@pytest.mark.parametrize("level", sorted(LEVEL_FILES))
+def test_submit_name_spellings(tmp_path, name, level):
+    # T-SKL-2
+    _bind(tmp_path, *LEVEL_FILES[level])
+    msg_id = None if level == "FS" else "LL-SUBMIT"
+    _assert_decision(_run(_skill(name), tmp_path), tmp_path, msg_id, level)
+
+
+@pytest.mark.parametrize(
+    "tool_input",
+    [
+        {"skill": "sc:implement"},
+        {"name": "sc:implement"},
+        {"skill": None, "name": "sc:implement"},
+        {"skill": "sc:implement", "name": "sc:workflow"},
+    ],
+)
+def test_skill_name_keys(tmp_path, tool_input):
+    # T-SKL-3: skill, else name (a null skill counts as missing).
+    _bind(tmp_path, "worktree")
+    result = _run(_skill(tool_input=tool_input), tmp_path)
+    _assert_decision(result, tmp_path, "LL-IMPL", "W")
+
+
+def test_explicit_empty_skill_does_not_fall_back_to_name(tmp_path):
+    _bind(tmp_path, "full")
+    result = _run(_skill(tool_input={"skill": "", "name": "sc:workflow"}), tmp_path)
+    _assert_decision(result, tmp_path, "LL-SKILL", "F")
+
+
+@pytest.mark.parametrize(
+    "name", [_ABSENT, "", "   ", "\t\n", "/", "sc:", "sc:sc--protocol"]
+)
+@pytest.mark.parametrize("level", sorted(LEVEL_FILES))
+def test_skill_without_name(tmp_path, name, level):
+    # T-SKL-4: no readable name is SKILL; allowed only at full --submit.
+    _bind(tmp_path, *LEVEL_FILES[level])
+    msg_id = None if level == "FS" else "LL-SKILL"
+    _assert_decision(_run(_skill(name), tmp_path), tmp_path, msg_id, level)
+
+
+@pytest.mark.parametrize("name", ["sc:issue", "sc:issue-protocol"])
+@pytest.mark.parametrize("level", sorted(LEVEL_FILES))
+def test_issue_skill_escape(tmp_path, name, level):
+    # T-SKL-5
+    _bind(tmp_path, *LEVEL_FILES[level])
+    _assert_decision(_run(_skill(name), tmp_path), tmp_path, "LL-ESCAPE", level)
+
+
+def test_skill_name_newline_does_not_shift_fields(tmp_path):
+    # T-FC-8 (Skill variant): a newline in the name decides as the first word.
+    _bind(tmp_path, "worktree")
+    result = _run(_skill("sc:implement\nsc:workflow"), tmp_path)
+    _assert_decision(result, tmp_path, "LL-IMPL", "W")
+    result = _run(_skill("sc:workflow\nsc:implement"), tmp_path)
+    _assert_decision(result, tmp_path, None, "W")
+
+
+def test_huge_fields_are_quick(tmp_path):
+    # Line splitting must stay linear: _run's 10 s timeout fails a quadratic split.
+    _bind(tmp_path, "worktree")
+    result = _run(_skill("sc:implement " + "x" * 200_000), tmp_path)
+    _assert_decision(result, tmp_path, "LL-IMPL", "W")
+    bash = {**VALID_PAYLOADS["pretooluse-bash"], "session_id": SID}
+    bash["tool_input"] = {"command": "echo " + "y\n" * 100_000}
+    _assert_decision(_run(bash, tmp_path), tmp_path, None, "W")
+    # Not JSON (closing brace cut), the bound id after the long field: LL-BROKEN.
+    raw = json.dumps(_skill("sc:workflow", tool_input=bash["tool_input"])).encode()
+    _assert_decision(_run(raw[:-1], tmp_path), tmp_path, "LL-BROKEN", "W")
+
+
+@pytest.mark.parametrize(
+    "tool_name, tool_input",
+    [
+        ("Bash", {"command": "git push origin main"}),
+        ("Edit", {"file_path": "/x/settings.json"}),
+        ("Agent", {"isolation": "remote"}),
+        ("Read", {"file_path": "/etc/passwd"}),
+        ("mcp__github__merge_pull_request", {}),
+    ],
+)
+def test_other_tools_are_none_until_their_classifiers_exist(
+    tmp_path, tool_name, tool_input
+):
+    # Tasks 6 to 10 add these classifiers; until then a non-Skill call is NONE.
+    _bind(tmp_path, "worktree")
+    payload = {
+        "hook_event_name": "PreToolUse",
+        "session_id": SID,
+        "tool_name": tool_name,
+        "tool_input": tool_input,
+    }
+    _assert_decision(_run(payload, tmp_path), tmp_path, None, "W")
+
+
+BAD_FIELDS = {
+    "numeric-skill": {"tool_name": "Skill", "tool_input": {"skill": 7}},
+    "object-name": {"tool_name": "Skill", "tool_input": {"name": {"a": 1}}},
+    "nul-skill": {"tool_name": "Skill", "tool_input": {"skill": "sc:work\u0000flow"}},
+    "numeric-tool-name": {"tool_name": 5, "tool_input": {}},
+    "list-tool-input": {"tool_name": "Skill", "tool_input": ["sc:implement"]},
+    "numeric-command": {"tool_name": "Bash", "tool_input": {"command": 1}},
+    "nul-command": {"tool_name": "Bash", "tool_input": {"command": "ls\u0000"}},
+    "list-path": {"tool_name": "Write", "tool_input": {"file_path": ["a"]}},
+    "bool-isolation": {"tool_name": "Task", "tool_input": {"isolation": True}},
+}
+
+
+@pytest.mark.parametrize("name", sorted(BAD_FIELDS))
+def test_input_error_blocks_governed_broken(tmp_path, name):
+    _bind(tmp_path, "full-submit")
+    payload = {"hook_event_name": "PreToolUse", "session_id": SID, **BAD_FIELDS[name]}
+    _assert_decision(_run(payload, tmp_path), tmp_path, "LL-BROKEN", "FS")
+
+
+@pytest.mark.parametrize("name", sorted(BAD_FIELDS))
+def test_input_error_allows_ordinary(tmp_path, name):
+    _bind(tmp_path, "worktree")
+    payload = {
+        "hook_event_name": "PreToolUse",
+        "session_id": "other",
+        **BAD_FIELDS[name],
+    }
+    _assert_decision(_run(payload, tmp_path), tmp_path, None, "W")
+
+
+# --- PreToolUse resolution: isolation and fail-closed (Task 5) -------------
+
+
+@pytest.mark.parametrize("store", ["empty", "other-sessions"])
+@pytest.mark.parametrize("name", sorted(EXPECTED))
+def test_ordinary_session_never_blocked(tmp_path, store, name):
+    # T-ISO-1
+    if store == "other-sessions":
+        sessions = _store(tmp_path / "home") / "sessions"
+        sessions.mkdir(parents=True)
+        (sessions / "someone-else").write_text("worktree")
+    result = _run(_skill(name, sid="unbound-session"), tmp_path)
+    _assert_decision(result, tmp_path, None, "W")
+
+
+def test_two_sessions_isolated(tmp_path):
+    # T-ISO-2
+    sessions = _store(tmp_path / "home") / "sessions"
+    sessions.mkdir(parents=True)
+    (sessions / "session-a").write_text("worktree")
+    (sessions / "session-b").write_text("full-submit")
+    a = _run(_skill("sc:pr-submit", sid="session-a"), tmp_path)
+    b = _run(_skill("sc:pr-submit", sid="session-b"), tmp_path)
+    store = str(_store(tmp_path / "home"))
+    assert a.returncode == 2
+    assert a.stderr.decode() == _expected("LL-SUBMIT", "worktree", "session-a", store)
+    assert (b.returncode, b.stderr) == (0, b"")
+
+
+def test_same_worktree_other_session_ordinary(tmp_path):
+    # T-ISO-3: cwd is never read on PreToolUse.
+    _bind(tmp_path, "worktree")
+    result = _run(_skill("sc:implement", sid="other", cwd="/work/wt"), tmp_path)
+    _assert_decision(result, tmp_path, None, "W")
+
+
+def test_person_subagent_not_governed(tmp_path):
+    # T-ISO-4 (X-004): unbound id plus agent_id plus the bound worktree's cwd.
+    _bind(tmp_path, "worktree")
+    payload = _skill("sc:implement", sid="person", agent_id="a1", cwd="/work/wt")
+    _assert_decision(_run(payload, tmp_path), tmp_path, None, "W")
+
+
+@pytest.mark.parametrize(
+    "payload",
+    [
+        b"this is not json",
+        b'{"hook_event_name": "PreToolUse", "tool_name": "Skill", "session_id": "unbound-x", ',
+        {"hook_event_name": "PreToolUse", "session_id": SID, "tool_name": "Skill"},
+        {"hook_event_name": "PreToolUse", "session_id": SID, "tool_name": "Frobnicate"},
+    ],
+    ids=["not-json", "truncated-unbound", "no-tool-input", "unknown-tool"],
+)
+def test_fail_open_shapes_ordinary(tmp_path, payload):
+    # T-ISO-5: with an empty store, and with a store that holds only other ids.
+    result = _run(payload, tmp_path)
+    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
+    sessions = _store(tmp_path / "home") / "sessions"
+    sessions.mkdir(parents=True)
+    (sessions / "someone-else").write_text("worktree")
+    if isinstance(payload, dict):
+        payload = {**payload, "session_id": "unbound-x"}
+    result = _run(payload, tmp_path)
+    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
+
+
+def test_forged_nested_session_id(tmp_path):
+    # T-ISO-6: only the top-level session_id counts.
+    _bind(tmp_path, "worktree")
+    ordinary = _skill("sc:implement", sid="unbound-one", meta={"session_id": SID})
+    _assert_decision(_run(ordinary, tmp_path), tmp_path, None, "W")
+    governed = _skill("sc:implement", tool_input={"session_id": "unbound-two"})
+    _assert_decision(_run(governed, tmp_path), tmp_path, "LL-IMPL", "W")
+
+
+def test_subagent_governed(tmp_path):
+    """T-ISO-7: parent id plus agent_id is governed (pending OB-H1: hand-written
+    shape; agent_id is never read on PreToolUse)."""
+    _bind(tmp_path, "worktree")
+    payload = _skill("sc:implement", agent_id="subagent-0001")
+    _assert_decision(_run(payload, tmp_path), tmp_path, "LL-IMPL", "W")
+
+
+def test_nested_subagent_governed(tmp_path):
+    """T-ISO-8: nested shape with agent_type is governed (pending OB-H1:
+    hand-written shape)."""
+    _bind(tmp_path, "full")
+    payload = _skill("sc:pr-submit", agent_id="nested-0002", agent_type="Explore")
+    _assert_decision(_run(payload, tmp_path), tmp_path, "LL-SUBMIT", "F")
+
+
+@pytest.mark.parametrize(
+    "shape",
+    ["missing", "invalid", "numeric", "nested-forged", "unparseable"],
+)
+def test_identity_loss_allows_silently(tmp_path, shape):
+    # Declared fail-open limit (design section 3; overrides MR T-FC-6): with no
+    # readable top-level session_id the guard cannot tell a governed session
+    # from an ordinary one, so the call is allowed with no message, even while
+    # the store holds a bound session. A governed session that loses its id is
+    # therefore not enforced; this is accepted, not a bug.
+    _bind(tmp_path, "worktree")
+    payloads = {
+        "missing": _skill("sc:implement", sid=None),
+        "invalid": _skill("sc:implement", sid="bad id!"),
+        "numeric": _skill("sc:implement", sid=12345),
+        "nested-forged": _skill("sc:implement", sid=None, meta={"session_id": SID}),
+        "unparseable": b'{"hook_event_name": "PreToolUse", "tool_input": {',
+    }
+    result = _run(payloads[shape], tmp_path)
+    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
+
+
+@pytest.mark.parametrize("bound", [True, False])
+def test_jq_missing(tmp_path, bound):
+    # T-FC-1: governed gives LL-BROKEN at the bound level; ordinary exits 0.
+    _bin(tmp_path, with_jq=False)
+    _bind(tmp_path, "full")
+    sid = SID if bound else "unbound-session"
+    result = _run(_skill("sc:workflow", sid=sid), tmp_path)
+    if bound:
+        _assert_decision(result, tmp_path, "LL-BROKEN", "F")
+    else:
+        assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
+
+
+@pytest.mark.parametrize("state", ["empty", "garbage", "degraded", "mode-000"])
+@pytest.mark.parametrize("ok", [False, True])
+def test_bad_state_degrades_to_worktree(tmp_path, state, ok):
+    # T-FC-2: W column plus LL-STATE; an existing .ok still counts (WA, allowed).
+    if state == "mode-000" and os.geteuid() == 0:
+        pytest.skip("root reads a mode-000 file")
+    word = {"empty": "", "garbage": "rm -rf /", "degraded": "degraded"}.get(
+        state, "full"
+    )
+    sessions = _bind(tmp_path, word, ok)
+    if state == "mode-000":
+        (sessions / SID).chmod(0)
+    result = _run(_skill("sc:implement"), tmp_path)
+    if ok:
+        _assert_decision(result, tmp_path, None, "WA")
+    else:
+        _assert_decision(result, tmp_path, "LL-IMPL", "W", note=True)
+
+
+@pytest.mark.parametrize(
+    "raw",
+    [
+        b'{"hook_event_name": "PreToolUse", "session_id": "sess-abc_123", "tool_name": "Skill", ',
+        b'{"hook_event_name": "PreToolUse", "tool_input": {"session_id": "x"}, '
+        b'"session_id": "sess-abc_123", "tool_name": "Bash" garbage',
+    ],
+    ids=["truncated", "bound-id-after-another"],
+)
+def test_not_json_governed(tmp_path, raw):
+    # T-FC-5: a tool payload that is not JSON but holds a bound id: LL-BROKEN.
+    _bind(tmp_path, "full-submit")
+    _assert_decision(_run(raw, tmp_path), tmp_path, "LL-BROKEN", "FS")
+
+
+@pytest.mark.parametrize("forged", [10, 70, 500])
+def test_raw_id_scan_has_no_cap(tmp_path, forged):
+    # A payload with many unbound session_id strings before the bound one must
+    # still find it: a fixed cap would be a fail-open (plan Task 5 constraint).
+    _bind(tmp_path, "full")
+    nested = ", ".join(f'"session_id": "forged{n}"' for n in range(forged))
+    raw = (
+        '{"hook_event_name": "PreToolUse", "tool_input": {' + nested + "}, "
+        f'"session_id": "{SID}", "tool_name": "Bash" garbage'
+    ).encode()
+    _assert_decision(_run(raw, tmp_path), tmp_path, "LL-BROKEN", "F")
+
+
+def test_raw_id_scan_declared_limit_blocks_ordinary_with_nested_bound_id(tmp_path):
+    # Declared limit (design section 3 versus T-FC-5): on a failure path a bound
+    # id anywhere in broken JSON counts, so an ordinary session that sends
+    # broken JSON containing a bound id is blocked.
+    _bind(tmp_path, "full")
+    raw = (
+        b'{"hook_event_name": "PreToolUse", "session_id": "ordinary1", '
+        b'"tool_input": {"session_id": "'
+        + SID.encode()
+        + b'"}, "tool_name": "Bash" garbage'
+    )
+    _assert_decision(_run(raw, tmp_path), tmp_path, "LL-BROKEN", "F")
+
+
 # --- message texts (printer block, test-only route) ------------------------
 
 

Delta diff from the previous reviewed tree (empty on the first review): diff --git a/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t5-test.log b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t5-test.log
index 0d6841a1..69ceafd8 100644
--- a/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t5-test.log
+++ b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t5-test.log
@@ -1,3 +1,4 @@
+$ uv run pytest tests/hooks/test_launch_level_guard.py -v   (after the fix pass)
 ============================= test session starts ==============================
 platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0 -- /home/coder/workspaces/worktrees/IronClaude/issue-394-launch-level-hook/.venv/bin/python
 cachedir: .pytest_cache
@@ -5,7 +6,7 @@ SuperClaude: 5.0.0
 rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-394-launch-level-hook
 configfile: pyproject.toml
 plugins: superclaude-5.0.0, anyio-4.16.0
-collecting ... collected 307 items
+collecting ... collected 311 items
 
 tests/hooks/test_launch_level_guard.py::test_script_is_executable_with_version_line PASSED [  0%]
 tests/hooks/test_launch_level_guard.py::test_script_text_never_names_the_joined_store_path PASSED [  0%]
@@ -37,19 +38,19 @@ tests/hooks/test_launch_level_guard.py::test_trap_never_blocks_an_ordinary_sessi
 tests/hooks/test_launch_level_guard.py::test_trap_never_blocks_an_ordinary_session[prompt-prompt] PASSED [  9%]
 tests/hooks/test_launch_level_guard.py::test_trap_after_marker_gives_nobind_bare_header PASSED [  9%]
 tests/hooks/test_launch_level_guard.py::test_bind_marker_with_record_binds_level[worktree] PASSED [  9%]
-tests/hooks/test_launch_level_guard.py::test_bind_marker_with_record_binds_level[full] PASSED [ 10%]
+tests/hooks/test_launch_level_guard.py::test_bind_marker_with_record_binds_level[full] PASSED [  9%]
 tests/hooks/test_launch_level_guard.py::test_bind_marker_with_record_binds_level[full-submit] PASSED [ 10%]
 tests/hooks/test_launch_level_guard.py::test_bind_marker_at_start_without_record_binds_degraded PASSED [ 10%]
-tests/hooks/test_launch_level_guard.py::test_bind_malformed_marker_at_start_binds_degraded[[sc-launch:v1:ABCDEF0123456789ABCDEF0123456789]] PASSED [ 11%]
+tests/hooks/test_launch_level_guard.py::test_bind_malformed_marker_at_start_binds_degraded[[sc-launch:v1:ABCDEF0123456789ABCDEF0123456789]] PASSED [ 10%]
 tests/hooks/test_launch_level_guard.py::test_bind_malformed_marker_at_start_binds_degraded[[sc-launch:v1:01234567-89ab-cdef-0123-456789abcdef]] PASSED [ 11%]
 tests/hooks/test_launch_level_guard.py::test_bind_malformed_marker_at_start_binds_degraded[[sc-launch:v1:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa]] PASSED [ 11%]
-tests/hooks/test_launch_level_guard.py::test_bind_malformed_marker_at_start_binds_degraded[[sc-launch:v2:0123456789abcdef0123456789abcdef]] PASSED [ 12%]
+tests/hooks/test_launch_level_guard.py::test_bind_malformed_marker_at_start_binds_degraded[[sc-launch:v2:0123456789abcdef0123456789abcdef]] PASSED [ 11%]
 tests/hooks/test_launch_level_guard.py::test_bind_malformed_marker_at_start_binds_degraded[[sc-launch:v1:<nonce>]] PASSED [ 12%]
 tests/hooks/test_launch_level_guard.py::test_bind_marker_after_whitespace_or_bom_binds[   ] PASSED [ 12%]
-tests/hooks/test_launch_level_guard.py::test_bind_marker_after_whitespace_or_bom_binds[\n\n] PASSED [ 13%]
+tests/hooks/test_launch_level_guard.py::test_bind_marker_after_whitespace_or_bom_binds[\n\n] PASSED [ 12%]
 tests/hooks/test_launch_level_guard.py::test_bind_marker_after_whitespace_or_bom_binds[\t\r\n ] PASSED [ 13%]
 tests/hooks/test_launch_level_guard.py::test_bind_marker_after_whitespace_or_bom_binds[\ufeff] PASSED [ 13%]
-tests/hooks/test_launch_level_guard.py::test_bind_marker_after_whitespace_or_bom_binds[ \ufeff\n\ufeff\t] PASSED [ 14%]
+tests/hooks/test_launch_level_guard.py::test_bind_marker_after_whitespace_or_bom_binds[ \ufeff\n\ufeff\t] PASSED [ 13%]
 tests/hooks/test_launch_level_guard.py::test_bind_loose_marker_after_whitespace_or_bom_binds_degraded[   ] PASSED [ 14%]
 tests/hooks/test_launch_level_guard.py::test_bind_loose_marker_after_whitespace_or_bom_binds_degraded[\n\n] PASSED [ 14%]
 tests/hooks/test_launch_level_guard.py::test_bind_loose_marker_after_whitespace_or_bom_binds_degraded[\t\r\n ] PASSED [ 14%]
@@ -65,196 +66,200 @@ tests/hooks/test_launch_level_guard.py::test_bind_later_marker_consumes_record_k
 tests/hooks/test_launch_level_guard.py::test_bind_later_marker_consumes_record_keeps_level[] PASSED [ 18%]
 tests/hooks/test_launch_level_guard.py::test_bind_resume_same_id_governed PASSED [ 18%]
 tests/hooks/test_launch_level_guard.py::test_bind_rename_still_governed PASSED [ 18%]
-tests/hooks/test_launch_level_guard.py::test_bind_reclaim_new_session_new_level PASSED [ 19%]
+tests/hooks/test_launch_level_guard.py::test_bind_reclaim_new_session_new_level PASSED [ 18%]
 tests/hooks/test_launch_level_guard.py::test_bind_invalid_session_ids[.] PASSED [ 19%]
 tests/hooks/test_launch_level_guard.py::test_bind_invalid_session_ids[..] PASSED [ 19%]
-tests/hooks/test_launch_level_guard.py::test_bind_invalid_session_ids[x.ok] PASSED [ 20%]
+tests/hooks/test_launch_level_guard.py::test_bind_invalid_session_ids[x.ok] PASSED [ 19%]
 tests/hooks/test_launch_level_guard.py::test_bind_invalid_session_ids[a/b] PASSED [ 20%]
 tests/hooks/test_launch_level_guard.py::test_bind_invalid_session_ids[] PASSED [ 20%]
-tests/hooks/test_launch_level_guard.py::test_bind_invalid_session_ids[sid5] PASSED [ 21%]
+tests/hooks/test_launch_level_guard.py::test_bind_invalid_session_ids[sid5] PASSED [ 20%]
 tests/hooks/test_launch_level_guard.py::test_bind_invalid_session_ids[7] PASSED [ 21%]
 tests/hooks/test_launch_level_guard.py::test_bind_invalid_session_ids[sid7] PASSED [ 21%]
-tests/hooks/test_launch_level_guard.py::test_bind_invalid_session_ids[None] PASSED [ 22%]
+tests/hooks/test_launch_level_guard.py::test_bind_invalid_session_ids[None] PASSED [ 21%]
 tests/hooks/test_launch_level_guard.py::test_bind_marker_prompt_with_agent_id_ignored[agent-1] PASSED [ 22%]
 tests/hooks/test_launch_level_guard.py::test_bind_marker_prompt_with_agent_id_ignored[x] PASSED [ 22%]
-tests/hooks/test_launch_level_guard.py::test_bind_jq_missing_marker_prompt_blocked PASSED [ 23%]
+tests/hooks/test_launch_level_guard.py::test_bind_jq_missing_marker_prompt_blocked PASSED [ 22%]
 tests/hooks/test_launch_level_guard.py::test_bind_unparseable_marker_prompt_blocked PASSED [ 23%]
 tests/hooks/test_launch_level_guard.py::test_bind_loose_marker_mid_prompt_ignored[False] PASSED [ 23%]
-tests/hooks/test_launch_level_guard.py::test_bind_loose_marker_mid_prompt_ignored[True] PASSED [ 24%]
+tests/hooks/test_launch_level_guard.py::test_bind_loose_marker_mid_prompt_ignored[True] PASSED [ 23%]
 tests/hooks/test_launch_level_guard.py::test_bind_two_sessions_isolated PASSED [ 24%]
 tests/hooks/test_launch_level_guard.py::test_bind_same_worktree_other_session_ordinary PASSED [ 24%]
-tests/hooks/test_launch_level_guard.py::test_bind_person_subagent_not_governed PASSED [ 25%]
+tests/hooks/test_launch_level_guard.py::test_bind_person_subagent_not_governed PASSED [ 24%]
 tests/hooks/test_launch_level_guard.py::test_bind_forged_nested_session_id PASSED [ 25%]
 tests/hooks/test_launch_level_guard.py::test_bind_jq_missing_ordinary_prompt_allows PASSED [ 25%]
-tests/hooks/test_launch_level_guard.py::test_bind_concurrent_same_session_same_nonce PASSED [ 26%]
+tests/hooks/test_launch_level_guard.py::test_bind_concurrent_same_session_same_nonce PASSED [ 25%]
 tests/hooks/test_launch_level_guard.py::test_bind_concurrent_other_sessions_same_nonce PASSED [ 26%]
 tests/hooks/test_launch_level_guard.py::test_bind_race_winner_level_governs_tool_calls PASSED [ 26%]
-tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[-F] PASSED [ 27%]
+tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[-F] PASSED [ 26%]
 tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[-FS] PASSED [ 27%]
 tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[-W] PASSED [ 27%]
-tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[-WA] PASSED [ 28%]
-tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[sc:implement-F] PASSED [ 28%]
+tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[-WA] PASSED [ 27%]
+tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[sc:implement-F] PASSED [ 27%]
 tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[sc:implement-FS] PASSED [ 28%]
 tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[sc:implement-W] PASSED [ 28%]
-tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[sc:implement-WA] PASSED [ 29%]
+tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[sc:implement-WA] PASSED [ 28%]
 tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[sc:issue-F] PASSED [ 29%]
 tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[sc:issue-FS] PASSED [ 29%]
-tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[sc:issue-W] PASSED [ 30%]
+tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[sc:issue-W] PASSED [ 29%]
 tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[sc:issue-WA] PASSED [ 30%]
 tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[sc:pr-submit-F] PASSED [ 30%]
-tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[sc:pr-submit-FS] PASSED [ 31%]
+tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[sc:pr-submit-FS] PASSED [ 30%]
 tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[sc:pr-submit-W] PASSED [ 31%]
 tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[sc:pr-submit-WA] PASSED [ 31%]
-tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[sc:workflow-F] PASSED [ 32%]
+tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[sc:workflow-F] PASSED [ 31%]
 tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[sc:workflow-FS] PASSED [ 32%]
 tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[sc:workflow-W] PASSED [ 32%]
-tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[sc:workflow-WA] PASSED [ 33%]
+tests/hooks/test_launch_level_guard.py::test_skill_grid_matches_oracle[sc:workflow-WA] PASSED [ 32%]
 tests/hooks/test_launch_level_guard.py::test_impl_name_spellings[sc:implement] PASSED [ 33%]
 tests/hooks/test_launch_level_guard.py::test_impl_name_spellings[sc:implement-protocol] PASSED [ 33%]
-tests/hooks/test_launch_level_guard.py::test_impl_name_spellings[sc-implement-protocol] PASSED [ 34%]
+tests/hooks/test_launch_level_guard.py::test_impl_name_spellings[sc-implement-protocol] PASSED [ 33%]
 tests/hooks/test_launch_level_guard.py::test_impl_name_spellings[task] PASSED [ 34%]
 tests/hooks/test_launch_level_guard.py::test_impl_name_spellings[sc:task] PASSED [ 34%]
-tests/hooks/test_launch_level_guard.py::test_impl_name_spellings[sc:task-protocol] PASSED [ 35%]
+tests/hooks/test_launch_level_guard.py::test_impl_name_spellings[sc:task-protocol] PASSED [ 34%]
 tests/hooks/test_launch_level_guard.py::test_impl_name_spellings[sc:improve] PASSED [ 35%]
 tests/hooks/test_launch_level_guard.py::test_impl_name_spellings[sc:cleanup] PASSED [ 35%]
-tests/hooks/test_launch_level_guard.py::test_impl_name_spellings[sc:spawn] PASSED [ 36%]
+tests/hooks/test_launch_level_guard.py::test_impl_name_spellings[sc:spawn] PASSED [ 35%]
 tests/hooks/test_launch_level_guard.py::test_impl_name_spellings[sc:build] PASSED [ 36%]
 tests/hooks/test_launch_level_guard.py::test_impl_name_spellings[SC:IMPLEMENT] PASSED [ 36%]
-tests/hooks/test_launch_level_guard.py::test_impl_name_spellings[/sc:implement args] PASSED [ 37%]
-tests/hooks/test_launch_level_guard.py::test_impl_name_spellings[superclaude:sc-implement-protocol] PASSED [ 37%]
+tests/hooks/test_launch_level_guard.py::test_impl_name_spellings[/sc:implement args] PASSED [ 36%]
+tests/hooks/test_launch_level_guard.py::test_impl_name_spellings[superclaude:sc-implement-protocol] PASSED [ 36%]
 tests/hooks/test_launch_level_guard.py::test_impl_name_spellings[ \t\nsc:implement] PASSED [ 37%]
-tests/hooks/test_launch_level_guard.py::test_lookalike_skill_names_stay_none[sc:cleanup-audit-protocol] PASSED [ 38%]
-tests/hooks/test_launch_level_guard.py::test_lookalike_skill_names_stay_none[task-builder] PASSED [ 38%]
+tests/hooks/test_launch_level_guard.py::test_lookalike_skill_names_stay_none[sc:cleanup-audit-protocol] PASSED [ 37%]
+tests/hooks/test_launch_level_guard.py::test_lookalike_skill_names_stay_none[task-builder] PASSED [ 37%]
 tests/hooks/test_launch_level_guard.py::test_lookalike_skill_names_stay_none[sc:tasklist-protocol] PASSED [ 38%]
-tests/hooks/test_launch_level_guard.py::test_submit_name_spellings[F-sc:pr-submit] PASSED [ 39%]
-tests/hooks/test_launch_level_guard.py::test_submit_name_spellings[F-sc:pr-submit-protocol] PASSED [ 39%]
+tests/hooks/test_launch_level_guard.py::test_submit_name_spellings[F-sc:pr-submit] PASSED [ 38%]
+tests/hooks/test_launch_level_guard.py::test_submit_name_spellings[F-sc:pr-submit-protocol] PASSED [ 38%]
 tests/hooks/test_launch_level_guard.py::test_submit_name_spellings[FS-sc:pr-submit] PASSED [ 39%]
-tests/hooks/test_launch_level_guard.py::test_submit_name_spellings[FS-sc:pr-submit-protocol] PASSED [ 40%]
-tests/hooks/test_launch_level_guard.py::test_submit_name_spellings[W-sc:pr-submit] PASSED [ 40%]
+tests/hooks/test_launch_level_guard.py::test_submit_name_spellings[FS-sc:pr-submit-protocol] PASSED [ 39%]
+tests/hooks/test_launch_level_guard.py::test_submit_name_spellings[W-sc:pr-submit] PASSED [ 39%]
 tests/hooks/test_launch_level_guard.py::test_submit_name_spellings[W-sc:pr-submit-protocol] PASSED [ 40%]
-tests/hooks/test_launch_level_guard.py::test_submit_name_spellings[WA-sc:pr-submit] PASSED [ 41%]
-tests/hooks/test_launch_level_guard.py::test_submit_name_spellings[WA-sc:pr-submit-protocol] PASSED [ 41%]
+tests/hooks/test_launch_level_guard.py::test_submit_name_spellings[WA-sc:pr-submit] PASSED [ 40%]
+tests/hooks/test_launch_level_guard.py::test_submit_name_spellings[WA-sc:pr-submit-protocol] PASSED [ 40%]
 tests/hooks/test_launch_level_guard.py::test_skill_name_keys[tool_input0] PASSED [ 41%]
-tests/hooks/test_launch_level_guard.py::test_skill_name_keys[tool_input1] PASSED [ 42%]
-tests/hooks/test_launch_level_guard.py::test_skill_name_keys[tool_input2] PASSED [ 42%]
+tests/hooks/test_launch_level_guard.py::test_skill_name_keys[tool_input1] PASSED [ 41%]
+tests/hooks/test_launch_level_guard.py::test_skill_name_keys[tool_input2] PASSED [ 41%]
 tests/hooks/test_launch_level_guard.py::test_skill_name_keys[tool_input3] PASSED [ 42%]
 tests/hooks/test_launch_level_guard.py::test_explicit_empty_skill_does_not_fall_back_to_name PASSED [ 42%]
-tests/hooks/test_launch_level_guard.py::test_skill_without_name[F-name0] PASSED [ 43%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[F-name0] PASSED [ 42%]
 tests/hooks/test_launch_level_guard.py::test_skill_without_name[F-] PASSED [ 43%]
 tests/hooks/test_launch_level_guard.py::test_skill_without_name[F-   ] PASSED [ 43%]
-tests/hooks/test_launch_level_guard.py::test_skill_without_name[F-\t\n] PASSED [ 44%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[F-\t\n] PASSED [ 43%]
 tests/hooks/test_launch_level_guard.py::test_skill_without_name[F-/] PASSED [ 44%]
 tests/hooks/test_launch_level_guard.py::test_skill_without_name[F-sc:] PASSED [ 44%]
-tests/hooks/test_launch_level_guard.py::test_skill_without_name[F-sc:sc--protocol] PASSED [ 45%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[F-sc:sc--protocol] PASSED [ 44%]
 tests/hooks/test_launch_level_guard.py::test_skill_without_name[FS-name0] PASSED [ 45%]
 tests/hooks/test_launch_level_guard.py::test_skill_without_name[FS-] PASSED [ 45%]
-tests/hooks/test_launch_level_guard.py::test_skill_without_name[FS-   ] PASSED [ 46%]
-tests/hooks/test_launch_level_guard.py::test_skill_without_name[FS-\t\n] PASSED [ 46%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[FS-   ] PASSED [ 45%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[FS-\t\n] PASSED [ 45%]
 tests/hooks/test_launch_level_guard.py::test_skill_without_name[FS-/] PASSED [ 46%]
-tests/hooks/test_launch_level_guard.py::test_skill_without_name[FS-sc:] PASSED [ 47%]
-tests/hooks/test_launch_level_guard.py::test_skill_without_name[FS-sc:sc--protocol] PASSED [ 47%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[FS-sc:] PASSED [ 46%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[FS-sc:sc--protocol] PASSED [ 46%]
 tests/hooks/test_launch_level_guard.py::test_skill_without_name[W-name0] PASSED [ 47%]
-tests/hooks/test_launch_level_guard.py::test_skill_without_name[W-] PASSED [ 48%]
-tests/hooks/test_launch_level_guard.py::test_skill_without_name[W-   ] PASSED [ 48%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[W-] PASSED [ 47%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[W-   ] PASSED [ 47%]
 tests/hooks/test_launch_level_guard.py::test_skill_without_name[W-\t\n] PASSED [ 48%]
-tests/hooks/test_launch_level_guard.py::test_skill_without_name[W-/] PASSED [ 49%]
-tests/hooks/test_launch_level_guard.py::test_skill_without_name[W-sc:] PASSED [ 49%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[W-/] PASSED [ 48%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[W-sc:] PASSED [ 48%]
 tests/hooks/test_launch_level_guard.py::test_skill_without_name[W-sc:sc--protocol] PASSED [ 49%]
-tests/hooks/test_launch_level_guard.py::test_skill_without_name[WA-name0] PASSED [ 50%]
-tests/hooks/test_launch_level_guard.py::test_skill_without_name[WA-] PASSED [ 50%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[WA-name0] PASSED [ 49%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[WA-] PASSED [ 49%]
 tests/hooks/test_launch_level_guard.py::test_skill_without_name[WA-   ] PASSED [ 50%]
-tests/hooks/test_launch_level_guard.py::test_skill_without_name[WA-\t\n] PASSED [ 51%]
-tests/hooks/test_launch_level_guard.py::test_skill_without_name[WA-/] PASSED [ 51%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[WA-\t\n] PASSED [ 50%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[WA-/] PASSED [ 50%]
 tests/hooks/test_launch_level_guard.py::test_skill_without_name[WA-sc:] PASSED [ 51%]
-tests/hooks/test_launch_level_guard.py::test_skill_without_name[WA-sc:sc--protocol] PASSED [ 52%]
-tests/hooks/test_launch_level_guard.py::test_issue_skill_escape[F-sc:issue] PASSED [ 52%]
+tests/hooks/test_launch_level_guard.py::test_skill_without_name[WA-sc:sc--protocol] PASSED [ 51%]
+tests/hooks/test_launch_level_guard.py::test_issue_skill_escape[F-sc:issue] PASSED [ 51%]
 tests/hooks/test_launch_level_guard.py::test_issue_skill_escape[F-sc:issue-protocol] PASSED [ 52%]
-tests/hooks/test_launch_level_guard.py::test_issue_skill_escape[FS-sc:issue] PASSED [ 53%]
-tests/hooks/test_launch_level_guard.py::test_issue_skill_escape[FS-sc:issue-protocol] PASSED [ 53%]
+tests/hooks/test_launch_level_guard.py::test_issue_skill_escape[FS-sc:issue] PASSED [ 52%]
+tests/hooks/test_launch_level_guard.py::test_issue_skill_escape[FS-sc:issue-protocol] PASSED [ 52%]
 tests/hooks/test_launch_level_guard.py::test_issue_skill_escape[W-sc:issue] PASSED [ 53%]
-tests/hooks/test_launch_level_guard.py::test_issue_skill_escape[W-sc:issue-protocol] PASSED [ 54%]
-tests/hooks/test_launch_level_guard.py::test_issue_skill_escape[WA-sc:issue] PASSED [ 54%]
+tests/hooks/test_launch_level_guard.py::test_issue_skill_escape[W-sc:issue-protocol] PASSED [ 53%]
+tests/hooks/test_launch_level_guard.py::test_issue_skill_escape[WA-sc:issue] PASSED [ 53%]
 tests/hooks/test_launch_level_guard.py::test_issue_skill_escape[WA-sc:issue-protocol] PASSED [ 54%]
-tests/hooks/test_launch_level_guard.py::test_skill_name_newline_does_not_shift_fields PASSED [ 55%]
-tests/hooks/test_launch_level_guard.py::test_huge_fields_are_quick PASSED [ 55%]
-tests/hooks/test_launch_level_guard.py::test_other_tools_are_none_until_their_classifiers_exist[Bash-tool_input0] PASSED [ 55%]
-tests/hooks/test_launch_level_guard.py::test_other_tools_are_none_until_their_classifiers_exist[Edit-tool_input1] PASSED [ 56%]
-tests/hooks/test_launch_level_guard.py::test_other_tools_are_none_until_their_classifiers_exist[Agent-tool_input2] PASSED [ 56%]
-tests/hooks/test_launch_level_guard.py::test_other_tools_are_none_until_their_classifiers_exist[Read-tool_input3] PASSED [ 56%]
-tests/hooks/test_launch_level_guard.py::test_other_tools_are_none_until_their_classifiers_exist[mcp__github__merge_pull_request-tool_input4] PASSED [ 57%]
-tests/hooks/test_launch_level_guard.py::test_input_error_blocks_governed_broken[bool-isolation] PASSED [ 57%]
-tests/hooks/test_launch_level_guard.py::test_input_error_blocks_governed_broken[list-path] PASSED [ 57%]
+tests/hooks/test_launch_level_guard.py::test_skill_name_newline_does_not_shift_fields PASSED [ 54%]
+tests/hooks/test_launch_level_guard.py::test_huge_fields_are_quick PASSED [ 54%]
+tests/hooks/test_launch_level_guard.py::test_other_tools_are_none_until_their_classifiers_exist[Bash-tool_input0] PASSED [ 54%]
+tests/hooks/test_launch_level_guard.py::test_other_tools_are_none_until_their_classifiers_exist[Edit-tool_input1] PASSED [ 55%]
+tests/hooks/test_launch_level_guard.py::test_other_tools_are_none_until_their_classifiers_exist[Agent-tool_input2] PASSED [ 55%]
+tests/hooks/test_launch_level_guard.py::test_other_tools_are_none_until_their_classifiers_exist[Read-tool_input3] PASSED [ 55%]
+tests/hooks/test_launch_level_guard.py::test_other_tools_are_none_until_their_classifiers_exist[mcp__github__merge_pull_request-tool_input4] PASSED [ 56%]
+tests/hooks/test_launch_level_guard.py::test_input_error_blocks_governed_broken[bool-isolation] PASSED [ 56%]
+tests/hooks/test_launch_level_guard.py::test_input_error_blocks_governed_broken[list-path] PASSED [ 56%]
 tests/hooks/test_launch_level_guard.py::test_input_error_blocks_governed_broken[list-tool-input] PASSED [ 57%]
-tests/hooks/test_launch_level_guard.py::test_input_error_blocks_governed_broken[nul-command] PASSED [ 58%]
-tests/hooks/test_launch_level_guard.py::test_input_error_blocks_governed_broken[nul-skill] PASSED [ 58%]
+tests/hooks/test_launch_level_guard.py::test_input_error_blocks_governed_broken[nul-command] PASSED [ 57%]
+tests/hooks/test_launch_level_guard.py::test_input_error_blocks_governed_broken[nul-skill] PASSED [ 57%]
 tests/hooks/test_launch_level_guard.py::test_input_error_blocks_governed_broken[numeric-command] PASSED [ 58%]
-tests/hooks/test_launch_level_guard.py::test_input_error_blocks_governed_broken[numeric-skill] PASSED [ 59%]
-tests/hooks/test_launch_level_guard.py::test_input_error_blocks_governed_broken[numeric-tool-name] PASSED [ 59%]
+tests/hooks/test_launch_level_guard.py::test_input_error_blocks_governed_broken[numeric-skill] PASSED [ 58%]
+tests/hooks/test_launch_level_guard.py::test_input_error_blocks_governed_broken[numeric-tool-name] PASSED [ 58%]
 tests/hooks/test_launch_level_guard.py::test_input_error_blocks_governed_broken[object-name] PASSED [ 59%]
-tests/hooks/test_launch_level_guard.py::test_input_error_allows_ordinary[bool-isolation] PASSED [ 60%]
-tests/hooks/test_launch_level_guard.py::test_input_error_allows_ordinary[list-path] PASSED [ 60%]
+tests/hooks/test_launch_level_guard.py::test_input_error_allows_ordinary[bool-isolation] PASSED [ 59%]
+tests/hooks/test_launch_level_guard.py::test_input_error_allows_ordinary[list-path] PASSED [ 59%]
 tests/hooks/test_launch_level_guard.py::test_input_error_allows_ordinary[list-tool-input] PASSED [ 60%]
-tests/hooks/test_launch_level_guard.py::test_input_error_allows_ordinary[nul-command] PASSED [ 61%]
-tests/hooks/test_launch_level_guard.py::test_input_error_allows_ordinary[nul-skill] PASSED [ 61%]
+tests/hooks/test_launch_level_guard.py::test_input_error_allows_ordinary[nul-command] PASSED [ 60%]
+tests/hooks/test_launch_level_guard.py::test_input_error_allows_ordinary[nul-skill] PASSED [ 60%]
 tests/hooks/test_launch_level_guard.py::test_input_error_allows_ordinary[numeric-command] PASSED [ 61%]
-tests/hooks/test_launch_level_guard.py::test_input_error_allows_ordinary[numeric-skill] PASSED [ 62%]
-tests/hooks/test_launch_level_guard.py::test_input_error_allows_ordinary[numeric-tool-name] PASSED [ 62%]
+tests/hooks/test_launch_level_guard.py::test_input_error_allows_ordinary[numeric-skill] PASSED [ 61%]
+tests/hooks/test_launch_level_guard.py::test_input_error_allows_ordinary[numeric-tool-name] PASSED [ 61%]
 tests/hooks/test_launch_level_guard.py::test_input_error_allows_ordinary[object-name] PASSED [ 62%]
-tests/hooks/test_launch_level_guard.py::test_ordinary_session_never_blocked[-empty] PASSED [ 63%]
-tests/hooks/test_launch_level_guard.py::test_ordinary_session_never_blocked[-other-sessions] PASSED [ 63%]
+tests/hooks/test_launch_level_guard.py::test_ordinary_session_never_blocked[-empty] PASSED [ 62%]
+tests/hooks/test_launch_level_guard.py::test_ordinary_session_never_blocked[-other-sessions] PASSED [ 62%]
 tests/hooks/test_launch_level_guard.py::test_ordinary_session_never_blocked[sc:implement-empty] PASSED [ 63%]
-tests/hooks/test_launch_level_guard.py::test_ordinary_session_never_blocked[sc:implement-other-sessions] PASSED [ 64%]
-tests/hooks/test_launch_level_guard.py::test_ordinary_session_never_blocked[sc:issue-empty] PASSED [ 64%]
-tests/hooks/test_launch_level_guard.py::test_ordinary_session_never_blocked[sc:issue-other-sessions] PASSED [ 64%]
-tests/hooks/test_launch_level_guard.py::test_ordinary_session_never_blocked[sc:pr-submit-empty] PASSED [ 65%]
-tests/hooks/test_launch_level_guard.py::test_ordinary_session_never_blocked[sc:pr-submit-other-sessions] PASSED [ 65%]
-tests/hooks/test_launch_level_guard.py::test_ordinary_session_never_blocked[sc:workflow-empty] PASSED [ 65%]
-tests/hooks/test_launch_level_guard.py::test_ordinary_session_never_blocked[sc:workflow-other-sessions] PASSED [ 66%]
-tests/hooks/test_launch_level_guard.py::test_two_sessions_isolated PASSED [ 66%]
-tests/hooks/test_launch_level_guard.py::test_same_worktree_other_session_ordinary PASSED [ 66%]
-tests/hooks/test_launch_level_guard.py::test_person_subagent_not_governed PASSED [ 67%]
-tests/hooks/test_launch_level_guard.py::test_fail_open_shapes_ordinary[not-json] PASSED [ 67%]
-tests/hooks/test_launch_level_guard.py::test_fail_open_shapes_ordinary[truncated-unbound] PASSED [ 67%]
-tests/hooks/test_launch_level_guard.py::test_fail_open_shapes_ordinary[no-tool-input] PASSED [ 68%]
-tests/hooks/test_launch_level_guard.py::test_fail_open_shapes_ordinary[unknown-tool] PASSED [ 68%]
-tests/hooks/test_launch_level_guard.py::test_forged_nested_session_id PASSED [ 68%]
-tests/hooks/test_launch_level_guard.py::test_subagent_governed PASSED    [ 69%]
-tests/hooks/test_launch_level_guard.py::test_nested_subagent_governed PASSED [ 69%]
-tests/hooks/test_launch_level_guard.py::test_identity_loss_allows_silently[missing] PASSED [ 69%]
-tests/hooks/test_launch_level_guard.py::test_identity_loss_allows_silently[invalid] PASSED [ 70%]
-tests/hooks/test_launch_level_guard.py::test_identity_loss_allows_silently[numeric] PASSED [ 70%]
-tests/hooks/test_launch_level_guard.py::test_identity_loss_allows_silently[nested-forged] PASSED [ 70%]
-tests/hooks/test_launch_level_guard.py::test_identity_loss_allows_silently[unparseable] PASSED [ 71%]
-tests/hooks/test_launch_level_guard.py::test_jq_missing[True] PASSED     [ 71%]
-tests/hooks/test_launch_level_guard.py::test_jq_missing[False] PASSED    [ 71%]
+tests/hooks/test_launch_level_guard.py::test_ordinary_session_never_blocked[sc:implement-other-sessions] PASSED [ 63%]
+tests/hooks/test_launch_level_guard.py::test_ordinary_session_never_blocked[sc:issue-empty] PASSED [ 63%]
+tests/hooks/test_launch_level_guard.py::test_ordinary_session_never_blocked[sc:issue-other-sessions] PASSED [ 63%]
+tests/hooks/test_launch_level_guard.py::test_ordinary_session_never_blocked[sc:pr-submit-empty] PASSED [ 64%]
+tests/hooks/test_launch_level_guard.py::test_ordinary_session_never_blocked[sc:pr-submit-other-sessions] PASSED [ 64%]
+tests/hooks/test_launch_level_guard.py::test_ordinary_session_never_blocked[sc:workflow-empty] PASSED [ 64%]
+tests/hooks/test_launch_level_guard.py::test_ordinary_session_never_blocked[sc:workflow-other-sessions] PASSED [ 65%]
+tests/hooks/test_launch_level_guard.py::test_two_sessions_isolated PASSED [ 65%]
+tests/hooks/test_launch_level_guard.py::test_same_worktree_other_session_ordinary PASSED [ 65%]
+tests/hooks/test_launch_level_guard.py::test_person_subagent_not_governed PASSED [ 66%]
+tests/hooks/test_launch_level_guard.py::test_fail_open_shapes_ordinary[not-json] PASSED [ 66%]
+tests/hooks/test_launch_level_guard.py::test_fail_open_shapes_ordinary[truncated-unbound] PASSED [ 66%]
+tests/hooks/test_launch_level_guard.py::test_fail_open_shapes_ordinary[no-tool-input] PASSED [ 67%]
+tests/hooks/test_launch_level_guard.py::test_fail_open_shapes_ordinary[unknown-tool] PASSED [ 67%]
+tests/hooks/test_launch_level_guard.py::test_forged_nested_session_id PASSED [ 67%]
+tests/hooks/test_launch_level_guard.py::test_subagent_governed PASSED    [ 68%]
+tests/hooks/test_launch_level_guard.py::test_nested_subagent_governed PASSED [ 68%]
+tests/hooks/test_launch_level_guard.py::test_identity_loss_allows_silently[missing] PASSED [ 68%]
+tests/hooks/test_launch_level_guard.py::test_identity_loss_allows_silently[invalid] PASSED [ 69%]
+tests/hooks/test_launch_level_guard.py::test_identity_loss_allows_silently[numeric] PASSED [ 69%]
+tests/hooks/test_launch_level_guard.py::test_identity_loss_allows_silently[nested-forged] PASSED [ 69%]
+tests/hooks/test_launch_level_guard.py::test_identity_loss_allows_silently[unparseable] PASSED [ 70%]
+tests/hooks/test_launch_level_guard.py::test_jq_missing[True] PASSED     [ 70%]
+tests/hooks/test_launch_level_guard.py::test_jq_missing[False] PASSED    [ 70%]
 tests/hooks/test_launch_level_guard.py::test_bad_state_degrades_to_worktree[False-empty] PASSED [ 71%]
-tests/hooks/test_launch_level_guard.py::test_bad_state_degrades_to_worktree[False-garbage] PASSED [ 72%]
-tests/hooks/test_launch_level_guard.py::test_bad_state_degrades_to_worktree[False-degraded] PASSED [ 72%]
+tests/hooks/test_launch_level_guard.py::test_bad_state_degrades_to_worktree[False-garbage] PASSED [ 71%]
+tests/hooks/test_launch_level_guard.py::test_bad_state_degrades_to_worktree[False-degraded] PASSED [ 71%]
 tests/hooks/test_launch_level_guard.py::test_bad_state_degrades_to_worktree[False-mode-000] PASSED [ 72%]
-tests/hooks/test_launch_level_guard.py::test_bad_state_degrades_to_worktree[True-empty] PASSED [ 73%]
-tests/hooks/test_launch_level_guard.py::test_bad_state_degrades_to_worktree[True-garbage] PASSED [ 73%]
-tests/hooks/test_launch_level_guard.py::test_bad_state_degrades_to_worktree[True-degraded] PASSED [ 73%]
-tests/hooks/test_launch_level_guard.py::test_bad_state_degrades_to_worktree[True-mode-000] PASSED [ 74%]
-tests/hooks/test_launch_level_guard.py::test_not_json_governed[truncated] PASSED [ 74%]
-tests/hooks/test_launch_level_guard.py::test_not_json_governed[bound-id-after-another] PASSED [ 74%]
+tests/hooks/test_launch_level_guard.py::test_bad_state_degrades_to_worktree[True-empty] PASSED [ 72%]
+tests/hooks/test_launch_level_guard.py::test_bad_state_degrades_to_worktree[True-garbage] PASSED [ 72%]
+tests/hooks/test_launch_level_guard.py::test_bad_state_degrades_to_worktree[True-degraded] PASSED [ 72%]
+tests/hooks/test_launch_level_guard.py::test_bad_state_degrades_to_worktree[True-mode-000] PASSED [ 73%]
+tests/hooks/test_launch_level_guard.py::test_not_json_governed[truncated] PASSED [ 73%]
+tests/hooks/test_launch_level_guard.py::test_not_json_governed[bound-id-after-another] PASSED [ 73%]
+tests/hooks/test_launch_level_guard.py::test_raw_id_scan_has_no_cap[10] PASSED [ 74%]
+tests/hooks/test_launch_level_guard.py::test_raw_id_scan_has_no_cap[70] PASSED [ 74%]
+tests/hooks/test_launch_level_guard.py::test_raw_id_scan_has_no_cap[500] PASSED [ 74%]
+tests/hooks/test_launch_level_guard.py::test_raw_id_scan_declared_limit_blocks_ordinary_with_nested_bound_id PASSED [ 75%]
 tests/hooks/test_launch_level_guard.py::test_design_table_holds_all_eighteen_ids PASSED [ 75%]
 tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-IMPL] PASSED [ 75%]
-tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-COMMIT] PASSED [ 75%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-COMMIT] PASSED [ 76%]
 tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-PUSH] PASSED [ 76%]
 tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-PUSH-FORM] PASSED [ 76%]
-tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-PROTECTED] PASSED [ 76%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-PROTECTED] PASSED [ 77%]
 tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-MERGE] PASSED [ 77%]
 tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-GH-WRITE] PASSED [ 77%]
-tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-SUBMIT] PASSED [ 77%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-SUBMIT] PASSED [ 78%]
 tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-REPO] PASSED [ 78%]
 tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-UNKNOWN] PASSED [ 78%]
-tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-MCP] PASSED [ 78%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-MCP] PASSED [ 79%]
 tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-ESCAPE] PASSED [ 79%]
 tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-TURN] PASSED [ 79%]
-tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-TAMPER] PASSED [ 79%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-TAMPER] PASSED [ 80%]
 tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-SKILL] PASSED [ 80%]
 tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-BIG] PASSED [ 80%]
-tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-BROKEN] PASSED [ 80%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-BROKEN] PASSED [ 81%]
 tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-NOBIND] PASSED [ 81%]
 tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-IMPL] PASSED [ 81%]
 tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-COMMIT] PASSED [ 81%]
@@ -270,19 +275,19 @@ tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_tex
 tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-ESCAPE] PASSED [ 85%]
 tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-TURN] PASSED [ 85%]
 tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-TAMPER] PASSED [ 85%]
-tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-SKILL] PASSED [ 85%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-SKILL] PASSED [ 86%]
 tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-BIG] PASSED [ 86%]
 tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-BROKEN] PASSED [ 86%]
-tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-NOBIND] PASSED [ 86%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-NOBIND] PASSED [ 87%]
 tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-IMPL] PASSED [ 87%]
 tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-COMMIT] PASSED [ 87%]
-tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-PUSH] PASSED [ 87%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-PUSH] PASSED [ 88%]
 tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-PUSH-FORM] PASSED [ 88%]
 tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-PROTECTED] PASSED [ 88%]
-tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-MERGE] PASSED [ 88%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-MERGE] PASSED [ 89%]
 tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-GH-WRITE] PASSED [ 89%]
 tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-SUBMIT] PASSED [ 89%]
-tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-REPO] PASSED [ 89%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-REPO] PASSED [ 90%]
 tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-UNKNOWN] PASSED [ 90%]
 tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-MCP] PASSED [ 90%]
 tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-ESCAPE] PASSED [ 90%]
@@ -315,4 +320,4 @@ tests/hooks/test_launch_level_guard.py::test_unknown_level_prints_bare_header[LL
 tests/hooks/test_launch_level_guard.py::test_tamper_with_invalid_sid_uses_broken_wording PASSED [ 99%]
 tests/hooks/test_launch_level_guard.py::test_notes_follow_the_lines_state_first PASSED [100%]
 
-============================= 307 passed in 3.61s ==============================
+============================= 311 passed in 3.94s ==============================
diff --git a/src/superclaude/hooks/scripts/launch-level-guard.sh b/src/superclaude/hooks/scripts/launch-level-guard.sh
index 0bb07da8..244f75aa 100755
--- a/src/superclaude/hooks/scripts/launch-level-guard.sh
+++ b/src/superclaude/hooks/scripts/launch-level-guard.sh
@@ -206,10 +206,12 @@ LL_PARSED=$(jq -r '
 LL_RC=$?
 LL_BAD=0 LL_TOOL= LL_SKILL= LL_PATH= LL_ISO= LL_TEXT= LL_PROMPT=
 if [ "$LL_RC" != 0 ]; then
-    # No jq or no parseable envelope: never infer a binding. A tool payload
-    # looks for a session_id value with a record only to find a positively
-    # bound session, which then falls through to the last line (LL-BROKEN);
-    # this can only block, never allow early. A recognizable launch-marker
+    # No jq or no parseable envelope: no level is inferred. A tool payload
+    # looks at every session_id value for one that has a record, only to find a
+    # positively bound session, which then falls through to the last line
+    # (LL-BROKEN); this can only block, never allow early. Declared limit: any
+    # bound id in the text counts, even a nested one, so an ordinary session
+    # sending broken JSON that contains a bound id is blocked. A recognizable launch-marker
     # prompt (marker text, no tool_name key) blocks rather than starting
     # ungoverned; anything else is identity loss (section 3): allow without
     # claiming enforcement.
@@ -218,8 +220,8 @@ if [ "$LL_RC" != 0 ]; then
         LL_EVENT=FAILED
         LL_RAWRE='"session_id"[[:space:]]*:[[:space:]]*"([A-Za-z0-9][A-Za-z0-9_-]{0,127})"(.*)'
         LL_REST=$LL_INPUT
-        # shortcut: only the first 64 session_id values are tried, then it is identity loss; raise if a real payload holds more.
-        for _ in {1..64}; do
+        # No cap on the number of session_id values tried (a cap would let a payload with many forged ids hide the real bound one).
+        while :; do
             [[ $LL_REST =~ $LL_RAWRE ]] || break
             LL_REST=${BASH_REMATCH[2]}
             if [ -e "$LL_STORE/sessions/${BASH_REMATCH[1]}" ] || [ -L "$LL_STORE/sessions/${BASH_REMATCH[1]}" ]; then
diff --git a/tests/hooks/test_launch_level_guard.py b/tests/hooks/test_launch_level_guard.py
index 88885c79..9fa1a423 100644
--- a/tests/hooks/test_launch_level_guard.py
+++ b/tests/hooks/test_launch_level_guard.py
@@ -1134,6 +1134,33 @@ def test_not_json_governed(tmp_path, raw):
     _assert_decision(_run(raw, tmp_path), tmp_path, "LL-BROKEN", "FS")
 
 
+@pytest.mark.parametrize("forged", [10, 70, 500])
+def test_raw_id_scan_has_no_cap(tmp_path, forged):
+    # A payload with many unbound session_id strings before the bound one must
+    # still find it: a fixed cap would be a fail-open (plan Task 5 constraint).
+    _bind(tmp_path, "full")
+    nested = ", ".join(f'"session_id": "forged{n}"' for n in range(forged))
+    raw = (
+        '{"hook_event_name": "PreToolUse", "tool_input": {' + nested + "}, "
+        f'"session_id": "{SID}", "tool_name": "Bash" garbage'
+    ).encode()
+    _assert_decision(_run(raw, tmp_path), tmp_path, "LL-BROKEN", "F")
+
+
+def test_raw_id_scan_declared_limit_blocks_ordinary_with_nested_bound_id(tmp_path):
+    # Declared limit (design section 3 versus T-FC-5): on a failure path a bound
+    # id anywhere in broken JSON counts, so an ordinary session that sends
+    # broken JSON containing a bound id is blocked.
+    _bind(tmp_path, "full")
+    raw = (
+        b'{"hook_event_name": "PreToolUse", "session_id": "ordinary1", '
+        b'"tool_input": {"session_id": "'
+        + SID.encode()
+        + b'"}, "tool_name": "Bash" garbage'
+    )
+    _assert_decision(_run(raw, tmp_path), tmp_path, "LL-BROKEN", "F")
+
+
 # --- message texts (printer block, test-only route) ------------------------
 
 

Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B4 ac=scope at=src/superclaude/hooks/scripts/launch-level-guard.sh:222 anchor="for _ in {1..64}; do" chk=n,n,n,y family=raw-id-cap fix=drop the 64 cap so every session_id value is tried covers="remove the fixed-64 raw-id early-allow loop of MR" first=A1 origin=new: the failure-path scan still tries only 64 session_id values, so 70 forged ids before the real bound id allow the call.

Saved-probe re-check hit locations (may be empty): 224:        while :; do
322:    while :; do


Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
