15479d67c88a1cf7a70d68a8e56acbee00b13641
Review one task for spec compliance.

Task brief: ## Task 9: Add the CHANGELOG entry and README sentence, then run the full ccsession and eval test files

Depends on: Task 5, Task 6, Task 7, Task 8

In `CHANGELOG.md`, add a new section at the top of `## [Unreleased]` in the file's existing style: a heading `### ccsession: status lines go to standard error (#389)` and a `#### Fixed (ccsession output streams)` list. The bullets say: every informational `[ccsession]` line (shim, profile and tier, session start and resume, the model cache and model list notes, and the Orca reopen notices) now goes to standard error, so a scripted `claude --version`, `claude mcp list` or `claude -p ... --output-format stream-json` that runs through `ccsession-orca` gets only Claude's own output on standard output; `superclaude eval` therefore reads the real Claude version instead of `127.0.0` taken from the shim address `127.0.0.1:<port>`, because its probe reads standard output first; the lines still show in a terminal; the values printed by `--ask`, `--auto-name`, `--list`, `--rm`, `--refresh-models` and `--models-status`, and the `models.py` output the launcher captures, stay on standard output; redirecting `ccsession` standard output to a file no longer collects the status lines; and the fix reaches a workspace only after `superclaude install` is run again. Add a `#### Added (ccsession output streams)` bullet naming the new tests. Say that it unblocks IronbellyOrg/Coder PR 458.

In `src/superclaude/skills/ccsession-tag/README.md`, add one sentence near the line that says `--ask` prints the question on the terminal and only the answer on standard output (around line 366): ccsession prints its own status lines (`[ccsession] ...`) on standard error, so standard output carries only Claude's output and the results of commands such as `--ask`, `--auto-name` and `--list`; on a terminal both streams look the same. Do not write any `src/superclaude/` path in the README.

Then run the checks: `uv run pytest tests/unit/test_ccsession_tag.py tests/unit/test_ccsession_tiers.py tests/cli/eval -q -p no:cacheprovider`, `uv run ruff check tests/unit/test_ccsession_tag.py tests/unit/test_ccsession_tiers.py tests/cli/eval/test_doctor_version.py`, `uv run ruff format --check` on the same three files, and `make sync-dev` followed by `make verify-sync`.

Acceptance criteria:
- `CHANGELOG.md` has the new `### ccsession: status lines go to standard error (#389)` section as the first entry under `## [Unreleased]`, and the README has the new sentence without a `src/superclaude/` path.
- The full pytest run passes with the replay test passing and the six updated tests passing; its output is saved to `./artifacts/t9-full-run.log`, together with the ruff and `make verify-sync` results in `./artifacts/t9-lint-sync.log`.
- `git status --short` shows changes only under `src/superclaude/skills/ccsession-tag/`, `tests/unit/`, `tests/cli/eval/`, `CHANGELOG.md` and the plan package (no `.claude/` path is staged or edited by hand), and `src/superclaude/skills/ccsession-tag/models.py` and `src/superclaude/cli/eval/commands.py` are unchanged.

AC ids:
T9.AC1: `CHANGELOG.md` has the new `### ccsession: status lines go to standard error (#389)` section as the first entry under `## [Unreleased]`, and the README has the new sentence without a `src/superclaude/` path.
T9.AC2: The full pytest run passes with the replay test passing and the six updated tests passing; its output is saved to `./artifacts/t9-full-run.log`, together with the ruff and `make verify-sync` results in `./artifacts/t9-lint-sync.log`.
T9.AC3: `git status --short` shows changes only under `src/superclaude/skills/ccsession-tag/`, `tests/unit/`, `tests/cli/eval/`, `CHANGELOG.md` and the plan package (no `.claude/` path is staged or edited by hand), and `src/superclaude/skills/ccsession-tag/models.py` and `src/superclaude/cli/eval/commands.py` are unchanged.

(Repository root: /home/coder/workspaces/worktrees/IronClaude/ic-issue-389. The task's own evidence files `./artifacts/...` live in /home/coder/workspaces/worktrees/IronClaude/ic-issue-389/.dev/tasks/to-do/TASK-WF-fixIssue389Ironb-20261105-174606/artifacts/ .)
Global constraints: - Scope is the launcher scripts `src/superclaude/skills/ccsession-tag/ccsession` and `src/superclaude/skills/ccsession-tag/ccsession-orca`, the tests that read their output, `CHANGELOG.md` and the skill `README.md`. `src/superclaude/skills/ccsession-tag/models.py` is not edited: its two `[ccsession]` notes (line 313 `model list updated`, line 837 `model data check`) are routed to standard error at their one call site in `ccsession` (line 1733), so the documented `ccsession --refresh-models` report keeps printing on standard output.
- `src/superclaude/cli/eval/commands.py` (the version probe and `_parse_version`) is not edited. Hardening it (treat a non-zero exit code as "not callable", prefer the `X.Y.Z (Claude Code)` form) is a separate pending decision and must not be added here. Its failure-path behavior (stdout empty because the launcher exited early) is deliberately not pinned by any test in this plan.
- These stay on standard output because the shell captures them: every `models.py` print captured with `$(...)` in `ccsession` (the `PROFILE_*=` lines, digests, shim port, tier lists, compact settings, the `models` and `status` reports), and the values printed by `ccsession --ask`, `--auto-name`, `--list`, `--rm`, `--refresh-models` and `--models-status`.
- Existing `>&2` warnings and errors (`ccsession` lines 823, 944, 973, 980, 1002, 1013, 1080, 1856; `ccsession-orca` lines 136, 211) are correct and stay as they are.
- Edit only under `src/superclaude/skills/ccsession-tag/`, `tests/` and `CHANGELOG.md`. Do not edit `.claude/` mirrors by hand; `make sync-dev` is the only way they change and they are never staged.
- Hardening closure for this fix: the replay run recorded in Task 2 is the positive witness (the negative witness was run before this plan on the unfixed tree), Task 8 supplies the parser fixtures, and the executor's final independent review is the off-path review.
- Evidence the tasks name (logs, outputs) is written under `./artifacts/` in this package.
Start sha: 15479d67c88a1cf7a70d68a8e56acbee00b13641
Diff against the start snapshot: 
diff --git a/CHANGELOG.md b/CHANGELOG.md
index 8655f830..00323b1b 100644
--- a/CHANGELOG.md
+++ b/CHANGELOG.md
@@ -4,6 +4,20 @@ All notable changes to IronClaude are documented in this file.
 
 ## [Unreleased]
 
+### ccsession: status lines go to standard error (#389)
+
+#### Fixed (ccsession output streams)
+
+- Every informational `[ccsession]` line (shim, profile and tier, session start and resume, the model cache and model list notes, and the Orca reopen notices) now goes to standard error. A scripted `claude --version`, `claude mcp list` or `claude -p ... --output-format stream-json` that runs through `ccsession-orca` gets only Claude's own output on standard output. This unblocks IronbellyOrg/Coder PR 458.
+- `superclaude eval` therefore reads the real Claude version. Before, the launcher's lines came first and the version check took `127.0.0` from the shim address `127.0.0.1:<port>`, because its probe reads standard output first.
+- The lines still show in a terminal. Redirecting `ccsession` standard output to a file no longer collects them.
+- The values printed by `--ask`, `--auto-name`, `--list`, `--rm`, `--refresh-models` and `--models-status`, and the `models.py` output the launcher captures, stay on standard output.
+- The fix reaches a workspace only after `superclaude install` is run again.
+
+#### Added (ccsession output streams)
+
+- Tests that pin the streams: a replay of `ccsession-orca --version` with a stand-in Claude (`test_version_through_orca_keeps_stdout_clean`), `test_launch_status_lines_are_on_stderr_only` (six launch variants), `test_model_list_update_note_goes_to_stderr_at_launch`, `test_refresh_models_report_stays_on_stdout`, a source guard for the lines a launch test cannot reach (`test_status_lines_in_launcher_scripts_go_to_stderr`), and three version-parsing tests in `tests/cli/eval/test_doctor_version.py`.
+
 ### onboarding deck: a 15-slide page for new team members, built from the routing guide
 
 #### Added (onboarding deck)
diff --git a/src/superclaude/skills/ccsession-tag/README.md b/src/superclaude/skills/ccsession-tag/README.md
index 1edd920e..08acc160 100644
--- a/src/superclaude/skills/ccsession-tag/README.md
+++ b/src/superclaude/skills/ccsession-tag/README.md
@@ -362,6 +362,10 @@ ran. So the tab reopens its own session instead of asking:
 - A session belongs to one tab: when another tab opens it, the first tab
   forgets it, so two tabs never reopen the same session.
 
+ccsession prints its own status lines (`[ccsession] ...`) on standard error, so
+standard output carries only Claude's output and the results of commands such as
+`--ask`, `--auto-name` and `--list`; on a terminal both streams look the same.
+
 The question itself is `ccsession --ask [<hint>]`: it prints the list and the
 question on the terminal and only the answer on standard output. A `@LIMIT@`
 in the hint becomes the time limit in seconds. When there is no limit, the hint

--- new untracked file .dev/tasks/to-do/TASK-WF-fixIssue389Ironb-20261105-174606/artifacts/t9-full-run.log ---
============================= test session starts ==============================
platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
SuperClaude: 5.0.0
rootdir: /home/coder/workspaces/worktrees/IronClaude/ic-issue-389
configfile: pyproject.toml
plugins: superclaude-5.0.0, anyio-4.16.0
collected 1906 items

tests/unit/test_ccsession_tag.py ....................................... [  2%]
........................................................................ [  5%]
........................................................................ [  9%]
........................................................................ [ 13%]
.............                                                            [ 14%]
tests/unit/test_ccsession_tiers.py ..................................... [ 16%]
........................................................................ [ 19%]
...........................                                              [ 21%]
tests/cli/eval/test_artifact_layout.py ...................               [ 22%]
tests/cli/eval/test_artifact_reproducibility.py ........                 [ 22%]
tests/cli/eval/test_atomic_setup.py ...................                  [ 23%]
tests/cli/eval/test_ban_import_rule.py ...                               [ 23%]
tests/cli/eval/test_capability_classifications.py ....................   [ 24%]
tests/cli/eval/test_capability_dataclass.py ................             [ 25%]
tests/cli/eval/test_capability_gates.py ..................               [ 26%]
tests/cli/eval/test_capability_report.py ..........                      [ 27%]
tests/cli/eval/test_claude_process_adapter.py .............              [ 27%]
tests/cli/eval/test_config.py ......                                     [ 28%]
tests/cli/eval/test_containment.py ...............................       [ 29%]
tests/cli/eval/test_coverage_gate.py ...........................         [ 31%]
tests/cli/eval/test_coverage_gate_integration.py ......                  [ 31%]
tests/cli/eval/test_defense_in_depth.py ...................              [ 32%]
tests/cli/eval/test_describe.py .........................                [ 33%]
tests/cli/eval/test_disk_budget.py .................................     [ 35%]
tests/cli/eval/test_doctor.py .......................................... [ 37%]
......                                                                   [ 38%]
tests/cli/eval/test_doctor_version.py .................                  [ 38%]
tests/cli/eval/test_eval_context.py .............................        [ 40%]
tests/cli/eval/test_eval_group.py .....                                  [ 40%]
tests/cli/eval/test_eval_id_regex.py ................................... [ 42%]
................................                                         [ 44%]
tests/cli/eval/test_eval_lifecycle.py ......................             [ 45%]
tests/cli/eval/test_eval_outcome.py ........................             [ 46%]
tests/cli/eval/test_eval_result.py ................                      [ 47%]
tests/cli/eval/test_eval_run.py .................                        [ 48%]
tests/cli/eval/test_exit_codes.py .s.s.                                  [ 48%]
tests/cli/eval/test_expect_duration.py ...................               [ 49%]
tests/cli/eval/test_expect_exit_code.py ....................             [ 50%]
tests/cli/eval/test_expect_failure.py .............                      [ 51%]
tests/cli/eval/test_expect_file.py ..................                    [ 52%]
tests/cli/eval/test_expect_jsonl.py ...................                  [ 53%]
tests/cli/eval/test_expect_primitives.py ...........................     [ 54%]
tests/cli/eval/test_expect_result.py ............                        [ 55%]
tests/cli/eval/test_expect_settings_json.py .....................        [ 56%]
tests/cli/eval/test_expect_stdio.py .......................              [ 57%]
tests/cli/eval/test_hard_guard_real_home.py ......                       [ 57%]
tests/cli/eval/test_home_isolation.py ...........................        [ 59%]
tests/cli/eval/test_home_isolation_extend.py ........................... [ 60%]
............                                                             [ 61%]
tests/cli/eval/test_hook_adapter.py ............                         [ 62%]
tests/cli/eval/test_isolation_dataclass.py ............................. [ 63%]
...                                                                      [ 63%]
tests/cli/eval/test_isolation_layers_probe.py .............              [ 64%]
tests/cli/eval/test_list.py ...................                          [ 65%]
tests/cli/eval/test_mcp_retry_once.py ..........................         [ 66%]
tests/cli/eval/test_no_mcp_skip.py ...........s                          [ 67%]
tests/cli/eval/test_no_pty_exclusion.py ..............                   [ 68%]
tests/cli/eval/test_no_shared_state.py ..........                        [ 68%]
tests/cli/eval/test_orchestrator.py ......................               [ 69%]
tests/cli/eval/test_parallel_15.py .......                               [ 70%]
tests/cli/eval/test_path_containment.py ................................ [ 71%]
...............                                                          [ 72%]
tests/cli/eval/test_path_traversal.py ...............                    [ 73%]
tests/cli/eval/test_perf_home_setup.py .                                 [ 73%]
tests/cli/eval/test_perf_resource_bounds.py ..                           [ 73%]
tests/cli/eval/test_phase_report_probe.py .........................      [ 74%]
tests/cli/eval/test_pty_driver.py .....................                  [ 76%]
tests/cli/eval/test_pty_lifecycle.py .....                               [ 76%]
tests/cli/eval/test_pty_stream.py ..............................         [ 77%]
tests/cli/eval/test_reporter.py .........................                [ 79%]
tests/cli/eval/test_reporter_contract.py ....                            [ 79%]
tests/cli/eval/test_retention_policy.py ....s.                           [ 79%]
tests/cli/eval/test_retry_policy.py ...........                          [ 80%]
tests/cli/eval/test_run_report.py ...................                    [ 81%]
tests/cli/eval/test_run_summary.py .........................             [ 82%]
tests/cli/eval/test_runner_class.py ...........                          [ 83%]
tests/cli/eval/test_schema_id_rejection.py ....................          [ 84%]
tests/cli/eval/test_schema_load.py .............                         [ 84%]
tests/cli/eval/test_schema_validate.py ..............                    [ 85%]
tests/cli/eval/test_scratch_root_allowlist.py ....................       [ 86%]
tests/cli/eval/test_scratch_root_policy.py ..................            [ 87%]
tests/cli/eval/test_signal_handling.py .........................         [ 88%]
tests/cli/eval/test_single_command.py ..                                 [ 89%]
tests/cli/eval/test_suite_loader.py .........................            [ 90%]
tests/cli/eval/test_suite_runtime.py .......                             [ 90%]
tests/cli/eval/test_summary_schema.py .................                  [ 91%]
tests/cli/eval/test_symlink_attacks.py ..............                    [ 92%]
tests/cli/eval/test_tavily_eval_capability.py ...                        [ 92%]
tests/cli/eval/test_validation_commands.py ..................            [ 93%]
tests/cli/eval/test_workflow_vs_task_builder_companion.py .............. [ 94%]
........................................................................ [ 97%]
.......................................                                  [100%]

================= 1902 passed, 4 skipped in 298.25s (0:04:58) ==================

--- new untracked file .dev/tasks/to-do/TASK-WF-fixIssue389Ironb-20261105-174606/artifacts/t9-lint-sync.log ---
== ruff check
All checks passed!
exit=0
== ruff format --check
3 files already formatted
exit=0
== make sync-dev
   Skills:    39 directories
   Agents:    48 files
   Commands:  46 files
   Hooks:     13 files
   Templates: 52 files
exit=0
== make verify-sync

=== Installer Registration ===
  ✅ _FRESHNESS_SCRIPTS matches src/superclaude/hooks/scripts/*.sh and *.js

=== Hooks Cross-Consistency ===
  ✅ hooks.json matcher and auggie-flag-clear.sh case body agree on auggie prefixes

✅ All components in sync.
exit=0

Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

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
