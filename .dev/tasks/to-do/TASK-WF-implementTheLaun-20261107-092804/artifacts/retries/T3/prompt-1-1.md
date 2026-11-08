f99d7bf8e27a7bfff0102f365a5d46e2dd03b66c
Review one task for spec compliance.

Task brief: ## Task 3: Create the guard script skeleton, messages and test harness

Depends on: Task 1

Create src/superclaude/hooks/scripts/launch-level-guard.sh (executable, first line #!/bin/bash) following the ten-part layout of design section 2 (DD-1): settings (LC_ALL=C, set -u -o pipefail, set -f, umask 077, no set -e, no ERR trap); the store path built from three literal parts so the script text never contains the string .claude/state (FR-L-01, T-TAM-8); the message table; dispatch on the parsed top-level hook_event_name equal to UserPromptSubmit or PreToolUse only (FR-L-08); the prompt branch and tool branch as stubs that allow; the empty-store fast exit using one directory test; an EXIT trap mapping any other exit code to LL-BROKEN (LL-NOBIND in the prompt branch); and a last line that denies with LL-BROKEN, exit 2. Add a line exactly "# launch-level-guard-version: 1" in the first ten lines; Task 18 reads it.

Messages: print every id of the design section 9 table (LL-IMPL, LL-COMMIT, LL-PUSH, LL-PUSH-FORM, LL-PROTECTED, LL-MERGE, LL-GH-WRITE, LL-SUBMIT, LL-REPO, LL-UNKNOWN, LL-MCP, LL-ESCAPE, LL-TURN, LL-TAMPER, LL-SKILL, LL-BIG, LL-BROKEN, LL-NOBIND) to stderr with the header "Launch-level guard: this session was started by /sc:issue --claim at level {level}." and the Blocked, Why and You can lines worded exactly as in that table; level names worktree, worktree (approved), full, full --submit; variables {level}, {store}, {sid} only; LL-NOBIND and LL-BROKEN print "Launch-level guard:" alone when the level is unknown; LL-TAMPER uses the LL-BROKEN wording when the session id is invalid; notes LL-STATE then LL-TEXT after the lines, only on a block. Amendment marks like B-1 are never printed (DD-3).

Create tests/hooks/test_launch_level_guard.py with the harness of tests/hooks/test_block_bare_python.py (real script through subprocess, temporary HOME, controlled PATH) and the first cases: ordinary session with no store allows silently; every message id prints the exact design text; the script text does not contain .claude/state; the script is executable and carries the version line; an event name other than the two allowed ones is handled by the identity-loss rule of design section 3.

Acceptance criteria:
- uv run pytest tests/hooks/test_launch_level_guard.py -v passes for the cases above, with the header, LL-BROKEN and LL-NOBIND checked against the design section 9 text. The other sixteen ids are asserted where their class becomes reachable (Tasks 5 to 11) and in Task 17; this task only requires that the printer holds all eighteen texts.
- grep for the string .claude/state in the script returns no match, and the file passes bash -n.
- With HOME pointing at an empty temporary directory, any valid hook payload exits 0 with empty stdout and stderr.
- A payload whose hook_event_name is neither UserPromptSubmit nor PreToolUse exits 0 without output when no governed session is positively identified.

AC ids (source order):
T3.AC1: uv run pytest tests/hooks/test_launch_level_guard.py -v passes for the cases above, with the header, LL-BROKEN and LL-NOBIND checked against the design section 9 text. The other sixteen ids are asserted where their class becomes reachable (Tasks 5 to 11) and in Task 17; this task only requires that the printer holds all eighteen texts.
T3.AC2: grep for the string .claude/state in the script returns no match, and the file passes bash -n.
T3.AC3: With HOME pointing at an empty temporary directory, any valid hook payload exits 0 with empty stdout and stderr.
T3.AC4: A payload whose hook_event_name is neither UserPromptSubmit nor PreToolUse exits 0 without output when no governed session is positively identified.
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
Start sha: f99d7bf8e27a7bfff0102f365a5d46e2dd03b66c
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t3-test.log b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t3-test.log
new file mode 100644
index 00000000..d0b1f892
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t3-test.log
@@ -0,0 +1,116 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0 -- /home/coder/workspaces/worktrees/IronClaude/issue-394-launch-level-hook/.venv/bin/python
+cachedir: .pytest_cache
+SuperClaude: 5.0.0
+rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-394-launch-level-hook
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, anyio-4.16.0
+collecting ... collected 105 items
+
+tests/hooks/test_launch_level_guard.py::test_script_is_executable_with_version_line PASSED [  0%]
+tests/hooks/test_launch_level_guard.py::test_script_text_never_names_the_joined_store_path PASSED [  1%]
+tests/hooks/test_launch_level_guard.py::test_script_passes_bash_syntax_check PASSED [  2%]
+tests/hooks/test_launch_level_guard.py::test_script_prints_no_amendment_marks PASSED [  3%]
+tests/hooks/test_launch_level_guard.py::test_empty_home_allows_silently[marker-prompt] PASSED [  4%]
+tests/hooks/test_launch_level_guard.py::test_empty_home_allows_silently[other-event] PASSED [  5%]
+tests/hooks/test_launch_level_guard.py::test_empty_home_allows_silently[pretooluse-bash] PASSED [  6%]
+tests/hooks/test_launch_level_guard.py::test_empty_home_allows_silently[pretooluse-skill] PASSED [  7%]
+tests/hooks/test_launch_level_guard.py::test_empty_home_allows_silently[prompt] PASSED [  8%]
+tests/hooks/test_launch_level_guard.py::test_empty_home_without_jq_allows_silently PASSED [  9%]
+tests/hooks/test_launch_level_guard.py::test_unbound_session_with_nonempty_store_allows_silently[marker-prompt] PASSED [ 10%]
+tests/hooks/test_launch_level_guard.py::test_unbound_session_with_nonempty_store_allows_silently[other-event] PASSED [ 11%]
+tests/hooks/test_launch_level_guard.py::test_unbound_session_with_nonempty_store_allows_silently[pretooluse-bash] PASSED [ 12%]
+tests/hooks/test_launch_level_guard.py::test_unbound_session_with_nonempty_store_allows_silently[pretooluse-skill] PASSED [ 13%]
+tests/hooks/test_launch_level_guard.py::test_unbound_session_with_nonempty_store_allows_silently[prompt] PASSED [ 14%]
+tests/hooks/test_launch_level_guard.py::test_other_event_unbound_allows_silently[missing-event] PASSED [ 15%]
+tests/hooks/test_launch_level_guard.py::test_other_event_unbound_allows_silently[nested-forged-event] PASSED [ 16%]
+tests/hooks/test_launch_level_guard.py::test_other_event_unbound_allows_silently[numeric-event] PASSED [ 17%]
+tests/hooks/test_launch_level_guard.py::test_other_event_unbound_allows_silently[post-tool-use] PASSED [ 18%]
+tests/hooks/test_launch_level_guard.py::test_unparseable_envelope_allows_silently PASSED [ 19%]
+tests/hooks/test_launch_level_guard.py::test_other_event_bound_session_blocks_broken[full-False-full-False] PASSED [ 20%]
+tests/hooks/test_launch_level_guard.py::test_other_event_bound_session_blocks_broken[full-submit\n-False-full --submit-False] PASSED [ 20%]
+tests/hooks/test_launch_level_guard.py::test_other_event_bound_session_blocks_broken[worktree-True-worktree (approved)-False] PASSED [ 21%]
+tests/hooks/test_launch_level_guard.py::test_other_event_bound_session_blocks_broken[garbage-False-worktree-True] PASSED [ 22%]
+tests/hooks/test_launch_level_guard.py::test_trap_in_tool_branch_gives_broken PASSED [ 23%]
+tests/hooks/test_launch_level_guard.py::test_trap_in_prompt_branch_gives_nobind PASSED [ 24%]
+tests/hooks/test_launch_level_guard.py::test_trap_never_blocks_an_ordinary_session[tool-pretooluse-bash] PASSED [ 25%]
+tests/hooks/test_launch_level_guard.py::test_trap_never_blocks_an_ordinary_session[prompt-prompt] PASSED [ 26%]
+tests/hooks/test_launch_level_guard.py::test_design_table_holds_all_eighteen_ids PASSED [ 27%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-IMPL] PASSED [ 28%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-COMMIT] PASSED [ 29%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-PUSH] PASSED [ 30%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-PUSH-FORM] PASSED [ 31%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-PROTECTED] PASSED [ 32%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-MERGE] PASSED [ 33%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-GH-WRITE] PASSED [ 34%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-SUBMIT] PASSED [ 35%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-REPO] PASSED [ 36%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-UNKNOWN] PASSED [ 37%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-MCP] PASSED [ 38%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-ESCAPE] PASSED [ 39%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-TURN] PASSED [ 40%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-TAMPER] PASSED [ 40%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-SKILL] PASSED [ 41%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-BIG] PASSED [ 42%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-BROKEN] PASSED [ 43%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-NOBIND] PASSED [ 44%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-IMPL] PASSED [ 45%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-COMMIT] PASSED [ 46%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-PUSH] PASSED [ 47%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-PUSH-FORM] PASSED [ 48%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-PROTECTED] PASSED [ 49%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-MERGE] PASSED [ 50%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-GH-WRITE] PASSED [ 51%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-SUBMIT] PASSED [ 52%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-REPO] PASSED [ 53%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-UNKNOWN] PASSED [ 54%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-MCP] PASSED [ 55%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-ESCAPE] PASSED [ 56%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-TURN] PASSED [ 57%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-TAMPER] PASSED [ 58%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-SKILL] PASSED [ 59%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-BIG] PASSED [ 60%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-BROKEN] PASSED [ 60%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-NOBIND] PASSED [ 61%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-IMPL] PASSED [ 62%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-COMMIT] PASSED [ 63%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-PUSH] PASSED [ 64%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-PUSH-FORM] PASSED [ 65%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-PROTECTED] PASSED [ 66%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-MERGE] PASSED [ 67%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-GH-WRITE] PASSED [ 68%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-SUBMIT] PASSED [ 69%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-REPO] PASSED [ 70%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-UNKNOWN] PASSED [ 71%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-MCP] PASSED [ 72%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-ESCAPE] PASSED [ 73%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-TURN] PASSED [ 74%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-TAMPER] PASSED [ 75%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-SKILL] PASSED [ 76%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-BIG] PASSED [ 77%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-BROKEN] PASSED [ 78%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-NOBIND] PASSED [ 79%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[WA-LL-IMPL] PASSED [ 80%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[WA-LL-COMMIT] PASSED [ 80%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[WA-LL-PUSH] PASSED [ 81%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[WA-LL-PUSH-FORM] PASSED [ 82%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[WA-LL-PROTECTED] PASSED [ 83%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[WA-LL-MERGE] PASSED [ 84%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[WA-LL-GH-WRITE] PASSED [ 85%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[WA-LL-SUBMIT] PASSED [ 86%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[WA-LL-REPO] PASSED [ 87%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[WA-LL-UNKNOWN] PASSED [ 88%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[WA-LL-MCP] PASSED [ 89%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[WA-LL-ESCAPE] PASSED [ 90%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[WA-LL-TURN] PASSED [ 91%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[WA-LL-TAMPER] PASSED [ 92%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[WA-LL-SKILL] PASSED [ 93%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[WA-LL-BIG] PASSED [ 94%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[WA-LL-BROKEN] PASSED [ 95%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[WA-LL-NOBIND] PASSED [ 96%]
+tests/hooks/test_launch_level_guard.py::test_unknown_level_prints_bare_header[LL-BROKEN] PASSED [ 97%]
+tests/hooks/test_launch_level_guard.py::test_unknown_level_prints_bare_header[LL-NOBIND] PASSED [ 98%]
+tests/hooks/test_launch_level_guard.py::test_tamper_with_invalid_sid_uses_broken_wording PASSED [ 99%]
+tests/hooks/test_launch_level_guard.py::test_notes_follow_the_lines_state_first PASSED [100%]
+
+============================= 105 passed in 0.65s ==============================
diff --git a/src/superclaude/hooks/scripts/launch-level-guard.sh b/src/superclaude/hooks/scripts/launch-level-guard.sh
new file mode 100755
index 00000000..3885b64d
--- /dev/null
+++ b/src/superclaude/hooks/scripts/launch-level-guard.sh
@@ -0,0 +1,233 @@
+#!/bin/bash
+# Launch-level guard (L1), IronbellyOrg/IronClaude issue #394.
+# Design: docs/designs/sc-issue-launch-level-hook.md (sections 2, 3, 8, 9).
+# Registered on UserPromptSubmit and PreToolUse. Exit 0 allows; exit 2 blocks
+# with a message on stderr; never exit 1, no onFailure. Only a session that the
+# claim script launched (a valid top-level session_id bound in the store) is
+# governed; every other session is ordinary and never blocked (FR-L-53).
+# Ten-part layout (DD-1); parts 5 and 6 are stubs until Tasks 4 and 5.
+# launch-level-guard-version: 1
+
+# 1. Settings
+export LC_ALL=C
+set -u -o pipefail
+set -f
+umask 077
+
+# >>> printer (parts 2 and 3; the tests run this block on its own)
+# 2. Store path: three literal parts, so this text never names the joined path.
+LL_S1=.claude
+LL_S2=state
+LL_S3=launch-level
+LL_STORE="${HOME:-}/$LL_S1/$LL_S2/$LL_S3"
+
+# 3. Messages (section 9). LL_LEVEL is W, WA, F, FS or empty (unknown).
+LL_LEVEL=
+LL_SID=
+LL_NOTE_STATE=0
+LL_NOTE_TEXT=0
+LL_DENIED=0
+
+ll_valid_sid() {
+    [[ $1 =~ ^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$ ]]
+}
+
+ll_say() {
+    local id=$1 lvl= b w y
+    if [ "$id" = LL-TAMPER ] && ! ll_valid_sid "$LL_SID"; then
+        id=LL-BROKEN
+    fi
+    case $id in
+    LL-IMPL)
+        b='starting /sc:implement, /task, /sc:improve, /sc:cleanup, /sc:spawn or /sc:build (or their skills).'
+        w='At the worktree level the agent stops at a plan until a person approves it.'
+        y='Read the plan, then type /sc:implement or /task, or reply approved, in this session.' ;;
+    LL-COMMIT)
+        b='creating a commit (git commit, cherry-pick, revert, am, or moving a branch with update-ref).'
+        w='Only a launch with --pipeline full --submit lets the agent commit.'
+        y='Review the changes and commit them yourself, or claim the issue again with --pipeline full --submit.' ;;
+    LL-PUSH)
+        b='a git push.'
+        w='Only a launch with --pipeline full --submit lets the agent push.'
+        y='Push the branch yourself after review, or claim the issue again with --pipeline full --submit.' ;;
+    LL-PUSH-FORM)
+        b='a push that is not one plain git push command, or a command that names git and push together.'
+        w='The guard can check a push only when the whole command is git push [-u] origin <branch> (or <source>:<branch>), with nothing before or after it; other forms (force, --all, another remote, variables, backticks, line continuations, chained or piped commands) can reach another remote or the main branch.'
+        y='Run the push as its own command, exactly: git push origin <branch> or git push -u origin <branch>, with the branch name written out.' ;;
+    LL-PROTECTED)
+        b='a push to master or main.'
+        w='No launch level may change the main branch.'
+        y='Push the feature branch by name, then merge it through a reviewed pull request.' ;;
+    LL-MERGE)
+        b='a merge (git merge, git pull, gh pr merge, a call to a GitHub merge URL, or an MCP merge tool).'
+        w='No launch level may merge; only a person reviews and merges.'
+        y='Leave the merge to a person. To update the branch, run git fetch, then git rebase.' ;;
+    LL-GH-WRITE)
+        b='a gh api call that is not one plain read command (it sets a method, a field or an input, calls graphql or a merge endpoint, or uses variables, quotes, pipes or other commands around it), or a gh command whose text mentions api, or a direct call to the GitHub API.'
+        w='In a launched session gh api may only read, and only in a form the guard can check: a gh api write can merge, comment or change the main branch.'
+        y='Run the read as one plain command with every value written out, for example gh api repos/o/r/pulls/5 --jq .state, or use a gh command for the step (gh pr view --json, gh pr comment, gh pr create --repo ...) at a level that allows it, or ask the person.' ;;
+    LL-SUBMIT)
+        b='/sc:pr-submit or a GitHub write (opening, editing, readying or commenting on a pull request or issue).'
+        w='Publishing work needs a launch with --pipeline full --submit.'
+        y='Run it yourself in your own session, or claim the issue again with --pipeline full --submit.' ;;
+    LL-REPO)
+        b='gh pr create without --repo.'
+        w='Without --repo, gh can open the pull request on the parent repository of a fork.'
+        y='Retry with --repo <owner>/<name> (or -R).' ;;
+    LL-UNKNOWN)
+        b='a git or gh command the guard does not recognise (an unknown subcommand, a git alias definition, or a subcommand built from a variable or a substitution), or a line continuation inside a word.'
+        w='In a launched session only known git and gh commands may run, so a renamed command or an alias cannot commit, push or merge.'
+        y='Use the standard command written out (for example git status, git diff, git add), or ask the person to run it. Write the command on one line.' ;;
+    LL-MCP)
+        b='a GitHub write through an MCP tool.'
+        w='The guard cannot check where an MCP write lands, so a launched session writes to GitHub only through git and gh.'
+        y='Use git or gh for this step.' ;;
+    LL-ESCAPE)
+        b='starting or messaging another agent or session (claude, ccsession, orca, SendMessage, /sc:issue, a remote subagent, a workflow, a remote trigger) or typing into a terminal (tmux, screen, xdotool).'
+        w="That work would run outside this session's launch level."
+        y='Do the work here (local subagents are allowed), or ask the person to start it.' ;;
+    LL-TURN)
+        b='scheduling a turn (a cron job or a wake-up) before the plan is approved.'
+        w='Its prompt text arrives later as a new turn and could look like a person replying approved.'
+        y='Wait until the person approves the plan, or use a background task or a monitor instead.' ;;
+    LL-TAMPER)
+        b='touching the launch-level state, the Claude Code settings or hooks, a git configuration file, or reinstalling the hooks.'
+        w='The session must not change its own limits.'
+        y="Ask the person. To release this session they run, in their own terminal: rm \"$LL_STORE/sessions/$LL_SID\" \"$LL_STORE/sessions/$LL_SID.ok\"" ;;
+    LL-SKILL)
+        b='a skill call whose name the guard cannot read.'
+        w='The guard cannot tell whether the skill is allowed at this level.'
+        y='Report it (the hook input format may have changed); the person can release the session.' ;;
+    LL-BIG)
+        b='a command longer than 64 KB.'
+        w='The guard cannot check a command that long in time.'
+        y='Write the content to a file with the Write tool, then run a short command.' ;;
+    LL-NOBIND)
+        b='this launch prompt.'
+        w='The session was started by /sc:issue --claim, but the guard could not register it, so its limits could not be enforced.'
+        y="Check that jq is installed and $LL_STORE is writable, then claim the issue again." ;;
+    *)
+        b='this action, because the launch-level guard could not run (jq missing, unreadable input or an internal error).'
+        w='In a launched session the guard fails closed.'
+        y="Install jq, or ask the person to release the session by deleting its files in $LL_STORE/sessions/." ;;
+    esac
+    case $LL_LEVEL in
+    W) lvl=worktree ;;
+    WA) lvl='worktree (approved)' ;;
+    F) lvl=full ;;
+    FS) lvl='full --submit' ;;
+    esac
+    if [ -n "$lvl" ]; then
+        printf '%s\n' "Launch-level guard: this session was started by /sc:issue --claim at level $lvl." >&2
+    else
+        printf '%s\n' 'Launch-level guard:' >&2
+    fi
+    printf '%s\n' "Blocked: $b" "Why: $w" "You can: $y" >&2
+    if [ "$LL_NOTE_STATE" = 1 ]; then
+        printf '%s\n' 'Note: the launch record was invalid or unreadable, so the strictest level (worktree) applies.' >&2
+    fi
+    if [ "$LL_NOTE_TEXT" = 1 ]; then
+        printf '%s\n' 'Note: the guard does not tell quoted text from commands. Any command that names git together with the word commit, push, merge or pull, or gh together with the word api, counts as that action, even if the words are only in a message, a title, a PR body or a search pattern. If that is the case here, write the text to a file with the Write tool and pass it with git commit -F <file> or gh ... --body-file <file>, or reword the search or title.' >&2
+    fi
+}
+
+ll_deny() {
+    LL_DENIED=1
+    ll_say "$1"
+    exit 2
+}
+# <<< printer
+
+# Any exit other than 0 or a deliberate deny is an internal failure. A governed
+# session fails closed (LL-BROKEN, LL-NOBIND in the prompt branch); an ordinary
+# session is never blocked by a failure.
+LL_GOVERNED=0
+LL_BRANCH=
+ll_on_exit() {
+    local rc=$?
+    trap - EXIT
+    if [ "$rc" = 0 ] || { [ "$rc" = 2 ] && [ "$LL_DENIED" = 1 ]; }; then
+        exit "$rc"
+    fi
+    if [ "$LL_GOVERNED" != 1 ]; then
+        exit 0
+    fi
+    if [ "$LL_BRANCH" = prompt ]; then
+        ll_say LL-NOBIND
+    else
+        ll_say LL-BROKEN
+    fi
+    exit 2
+}
+trap ll_on_exit EXIT
+
+# 4. Dispatch
+LL_INPUT=$(cat)
+# Empty-store fast exit: no session records and no launch marker.
+if [ ! -d "$LL_STORE/sessions" ]; then
+    case $LL_INPUT in
+    *'[sc-launch:'*) ;;
+    *) exit 0 ;;
+    esac
+fi
+# One parse of the top-level event and session id. Nested keys never count.
+LL_PARSED=$(jq -r '
+    (.hook_event_name | if . == "UserPromptSubmit" or . == "PreToolUse" then . else "OTHER" end)
+    + " " +
+    (.session_id | if type == "string" and test("\\A[A-Za-z0-9][A-Za-z0-9_-]{0,127}\\z") then . else "" end)
+' <<<"$LL_INPUT" 2>/dev/null)
+LL_RC=$?
+if [ "$LL_RC" != 0 ]; then
+    # Identity loss (section 3): no positive binding evidence, allow without
+    # claiming enforcement.
+    exit 0
+fi
+read -r LL_EVENT LL_SID <<<"$LL_PARSED"
+LL_SID=${LL_SID:-}
+
+# A valid id with a record (of any file kind) is positively governed. Its level
+# is exactly one allowed word plus an optional newline; anything else is
+# worktree with the LL-STATE note; .ok at worktree gives worktree (approved).
+if [ -n "$LL_SID" ] && { [ -e "$LL_STORE/sessions/$LL_SID" ] || [ -L "$LL_STORE/sessions/$LL_SID" ]; }; then
+    LL_GOVERNED=1
+    LL_FILE="$LL_STORE/sessions/$LL_SID"
+    LL_REC=
+    if [ -f "$LL_FILE" ] && [ ! -L "$LL_FILE" ] && [ -r "$LL_FILE" ]; then
+        IFS= read -r -N 13 LL_REC <"$LL_FILE"
+    fi
+    case $LL_REC in
+    worktree | worktree$'\n') LL_LEVEL=W ;;
+    full | full$'\n') LL_LEVEL=F ;;
+    full-submit | full-submit$'\n') LL_LEVEL=FS ;;
+    *) LL_LEVEL=W LL_NOTE_STATE=1 ;;
+    esac
+    if [ "$LL_LEVEL" = W ] && [ -f "$LL_FILE.ok" ] && [ ! -L "$LL_FILE.ok" ]; then
+        LL_LEVEL=WA
+    fi
+fi
+
+case $LL_EVENT in
+UserPromptSubmit) LL_BRANCH=prompt ;;
+PreToolUse) LL_BRANCH=tool ;;
+*)
+    # Unknown event shape: identity-loss allow unless positively governed,
+    # which falls through to the last line (LL-BROKEN).
+    [ "$LL_GOVERNED" = 1 ] || exit 0 ;;
+esac
+
+# 5. Prompt branch (binding and approval: Task 4, Task 11)
+if [ "$LL_BRANCH" = prompt ]; then
+    exit 0 # stub: prompt branch
+fi
+
+# 6. Fast paths
+if [ "$LL_BRANCH" = tool ]; then
+    exit 0 # stub: tool branch
+fi
+
+# 7. One jq read of the tool fields (Task 5)
+# 8. Classifiers adding classes (Tasks 5 to 10)
+# 9. One case on CLASS:LEVEL (Task 5)
+
+# 10. Default deny
+ll_deny LL-BROKEN
diff --git a/tests/hooks/test_launch_level_guard.py b/tests/hooks/test_launch_level_guard.py
new file mode 100644
index 00000000..d648ec1f
--- /dev/null
+++ b/tests/hooks/test_launch_level_guard.py
@@ -0,0 +1,373 @@
+"""Behavioral tests for launch-level-guard.sh (issue #394, plan Task 3).
+
+Each case runs the real script with a JSON payload on stdin, HOME inside
+tmp_path, CLAUDE_CONFIG_DIR unset and a PATH holding only a temporary bin
+directory, so the result does not depend on the developer's machine. Expected
+message texts are read from section 9 of the design, not copied here.
+
+Two test-only routes reach paths the Task 3 skeleton cannot reach through a
+real payload; neither adds behaviour to the shipped script:
+- the printer block (between the ">>> printer" and "<<< printer" comments) is
+  run on its own in bash, to check all eighteen message texts;
+- a copy of the script with a stub "exit 0" changed to "exit 7" drives the
+  real EXIT trap through a real payload.
+"""
+
+from __future__ import annotations
+
+import json
+import os
+import re
+import shutil
+import subprocess
+from pathlib import Path
+
+import pytest
+
+ROOT = Path(__file__).resolve().parents[2]
+HOOK = ROOT / "src" / "superclaude" / "hooks" / "scripts" / "launch-level-guard.sh"
+DESIGN = ROOT / "docs" / "designs" / "sc-issue-launch-level-hook.md"
+BASH = shutil.which("bash") or "/bin/bash"
+SID = "sess-abc_123"
+HEADER = "Launch-level guard: this session was started by /sc:issue --claim at level {level}."
+LEVELS = {
+    "W": "worktree",
+    "WA": "worktree (approved)",
+    "F": "full",
+    "FS": "full --submit",
+}
+STATE_NOTE = (
+    "Note: the launch record was invalid or unreadable, so the strictest level "
+    "(worktree) applies."
+)
+IDS = [
+    "LL-IMPL",
+    "LL-COMMIT",
+    "LL-PUSH",
+    "LL-PUSH-FORM",
+    "LL-PROTECTED",
+    "LL-MERGE",
+    "LL-GH-WRITE",
+    "LL-SUBMIT",
+    "LL-REPO",
+    "LL-UNKNOWN",
+    "LL-MCP",
+    "LL-ESCAPE",
+    "LL-TURN",
+    "LL-TAMPER",
+    "LL-SKILL",
+    "LL-BIG",
+    "LL-BROKEN",
+    "LL-NOBIND",
+]
+
+
+def _design_section_9() -> str:
+    text = DESIGN.read_text()
+    return text.split("## 9. Block messages", 1)[1].split("## 10.", 1)[0]
+
+
+def _design_table() -> dict[str, tuple[str, str, str]]:
+    rows = {}
+    for line in _design_section_9().splitlines():
+        m = re.match(r"^\| (LL-[A-Z-]+) \| (.*) \| (.*) \| (.*) \|$", line)
+        if m:
+            # Amendment marks such as [B-7] are not printed (DD-3).
+            cells = [re.sub(r" ?\[B-\d+\]", "", c) for c in m.groups()[1:]]
+            rows[m.group(1)] = tuple(cells)
+    return rows
+
+
+def _design_note(name: str) -> str:
+    m = re.search(rf"\*\*{name}\*\*[^`]*`(Note: [^`]*)`", _design_section_9())
+    assert m, name
+    return m.group(1)
+
+
+def _store(home: Path) -> Path:
+    return home / ".claude" / "state" / "launch-level"
+
+
+def _bin(tmp_path: Path, with_jq: bool = True) -> Path:
+    bindir = tmp_path / "bin"
+    bindir.mkdir(exist_ok=True)
+    tools = ["cat", "sed", "tr"] + (["jq"] if with_jq else [])
+    for tool in tools:
+        found = shutil.which(tool)
+        assert found, tool
+        (bindir / tool).symlink_to(found)
+    return bindir
+
+
+def _env(home: Path, bindir: Path) -> dict[str, str]:
+    env = {k: v for k, v in os.environ.items() if k != "CLAUDE_CONFIG_DIR"}
+    env["HOME"] = str(home)
+    env["PATH"] = str(bindir)
+    return env
+
+
+def _run(payload, tmp_path: Path, script: Path = HOOK, with_jq: bool = True):
+    home = tmp_path / "home"
+    home.mkdir(exist_ok=True)
+    stdin = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
+    bindir = tmp_path / "bin"
+    if not bindir.exists():
+        _bin(tmp_path, with_jq)
+    return subprocess.run(
+        [BASH, str(script)],
+        input=stdin,
+        capture_output=True,
+        env=_env(home, bindir),
+        timeout=10,
+    )
+
+
+def _bind(tmp_path: Path, word: str = "full", ok: bool = False) -> Path:
+    sessions = _store(tmp_path / "home") / "sessions"
+    sessions.mkdir(parents=True, exist_ok=True)
+    (sessions / SID).write_text(word)
+    if ok:
+        (sessions / f"{SID}.ok").write_text("")
+    return sessions
+
+
+def _expected(msg_id: str, level: str | None, sid: str, store: str) -> str:
+    blocked, why, you_can = _design_table()[msg_id]
+    subst = {"{store}": store, "{sid}": sid}
+    lines = []
+    for text in (blocked, why, you_can):
+        for key, value in subst.items():
+            text = text.replace(key, value)
+        lines.append(text)
+    first = HEADER.format(level=level) if level else "Launch-level guard:"
+    return f"{first}\nBlocked: {lines[0]}\nWhy: {lines[1]}\nYou can: {lines[2]}\n"
+
+
+def _printer(
+    tmp_path: Path, msg_id: str, level: str, sid: str = SID, notes: str = "00"
+):
+    """Run only the printer block of the script (test-only route)."""
+    driver = (
+        'eval "$(sed -n \'/^# >>> printer/,/^# <<< printer/p\' "$1")"\n'
+        "LL_LEVEL=$2 LL_SID=$3 LL_NOTE_STATE=${5:0:1} LL_NOTE_TEXT=${5:1:1}\n"
+        'll_say "$4"\n'
+    )
+    home = tmp_path / "home"
+    home.mkdir(exist_ok=True)
+    return subprocess.run(
+        [BASH, "-c", driver, "_", str(HOOK), level, sid, msg_id, notes],
+        capture_output=True,
+        env=_env(home, _bin(tmp_path)),
+        timeout=10,
+    )
+
+
+def _faulty_copy(tmp_path: Path, stub: str) -> Path:
+    """Copy of the script whose stub exits 7, to drive the real EXIT trap."""
+    text = HOOK.read_text()
+    marker = f"exit 0 # stub: {stub} branch"
+    assert text.count(marker) == 1
+    copy = tmp_path / "guard-fault.sh"
+    copy.write_text(text.replace(marker, "exit 7"))
+    return copy
+
+
+# --- script text -----------------------------------------------------------
+
+
+def test_script_is_executable_with_version_line():
+    assert os.access(HOOK, os.X_OK)
+    lines = HOOK.read_text().splitlines()
+    assert lines[0] == "#!/bin/bash"
+    assert "# launch-level-guard-version: 1" in lines[:10]
+
+
+def test_script_text_never_names_the_joined_store_path():
+    assert ".claude/state" not in HOOK.read_text()
+
+
+def test_script_passes_bash_syntax_check():
+    assert subprocess.run([BASH, "-n", str(HOOK)]).returncode == 0
+
+
+def test_script_prints_no_amendment_marks():
+    assert not re.search(r"\[B-\d+\]", HOOK.read_text())
+
+
+# --- ordinary sessions -----------------------------------------------------
+
+VALID_PAYLOADS = {
+    "pretooluse-bash": {
+        "hook_event_name": "PreToolUse",
+        "session_id": SID,
+        "tool_name": "Bash",
+        "tool_input": {"command": "git push origin main"},
+    },
+    "pretooluse-skill": {
+        "hook_event_name": "PreToolUse",
+        "session_id": SID,
+        "tool_name": "Skill",
+        "tool_input": {"skill": "sc:implement"},
+    },
+    "prompt": {
+        "hook_event_name": "UserPromptSubmit",
+        "session_id": SID,
+        "prompt": "hello",
+    },
+    "marker-prompt": {
+        "hook_event_name": "UserPromptSubmit",
+        "session_id": SID,
+        "prompt": "[sc-launch:v1:" + "a" * 32 + "] plan issue 1",
+    },
+    "other-event": {"hook_event_name": "PostToolUse", "session_id": SID},
+}
+
+
+@pytest.mark.parametrize("name", sorted(VALID_PAYLOADS))
+def test_empty_home_allows_silently(tmp_path, name):
+    result = _run(VALID_PAYLOADS[name], tmp_path)
+    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
+    assert not (tmp_path / "home" / ".claude").exists()
+
+
+def test_empty_home_without_jq_allows_silently(tmp_path):
+    _bin(tmp_path, with_jq=False)
+    result = _run(VALID_PAYLOADS["pretooluse-bash"], tmp_path)
+    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
+
+
+@pytest.mark.parametrize("name", sorted(VALID_PAYLOADS))
+def test_unbound_session_with_nonempty_store_allows_silently(tmp_path, name):
+    sessions = _store(tmp_path / "home") / "sessions"
+    sessions.mkdir(parents=True)
+    (sessions / "someone-else").write_text("worktree")
+    result = _run(VALID_PAYLOADS[name], tmp_path)
+    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
+
+
+# --- event dispatch and the identity-loss rule -----------------------------
+
+OTHER_EVENTS = {
+    "post-tool-use": {"hook_event_name": "PostToolUse", "session_id": SID},
+    "missing-event": {"session_id": SID, "tool_name": "Bash"},
+    "numeric-event": {"hook_event_name": 7, "session_id": SID},
+    "nested-forged-event": {
+        "hook_event_name": "Stop",
+        "session_id": SID,
+        "tool_input": {"hook_event_name": "PreToolUse"},
+    },
+}
+
+
+@pytest.mark.parametrize("name", sorted(OTHER_EVENTS))
+def test_other_event_unbound_allows_silently(tmp_path, name):
+    # Identity loss (design section 3): a nonempty store alone never proves
+    # this caller is governed; allow without claiming enforcement.
+    sessions = _store(tmp_path / "home") / "sessions"
+    sessions.mkdir(parents=True)
+    (sessions / "someone-else").write_text("full")
+    result = _run(OTHER_EVENTS[name], tmp_path)
+    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
+
+
+def test_unparseable_envelope_allows_silently(tmp_path):
+    _bind(tmp_path)
+    result = _run(b'{"hook_event_name": "PreToolUse", "session_id": ', tmp_path)
+    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
+
+
+@pytest.mark.parametrize(
+    "word, ok, level, note",
+    [
+        ("full", False, "full", False),
+        ("full-submit\n", False, "full --submit", False),
+        ("worktree", True, "worktree (approved)", False),
+        ("garbage", False, "worktree", True),
+    ],
+)
+def test_other_event_bound_session_blocks_broken(tmp_path, word, ok, level, note):
+    _bind(tmp_path, word, ok)
+    result = _run(OTHER_EVENTS["post-tool-use"], tmp_path)
+    store = str(_store(tmp_path / "home"))
+    expected = _expected("LL-BROKEN", level, SID, store)
+    if note:
+        expected += STATE_NOTE + "\n"
+    assert result.returncode == 2
+    assert result.stdout == b""
+    assert result.stderr.decode() == expected
+
+
+# --- EXIT trap through a real payload (fault-injected copy) ----------------
+
+
+def test_trap_in_tool_branch_gives_broken(tmp_path):
+    _bind(tmp_path, "full")
+    result = _run(
+        VALID_PAYLOADS["pretooluse-bash"], tmp_path, _faulty_copy(tmp_path, "tool")
+    )
+    store = str(_store(tmp_path / "home"))
+    assert result.returncode == 2
+    assert result.stderr.decode() == _expected("LL-BROKEN", "full", SID, store)
+
+
+def test_trap_in_prompt_branch_gives_nobind(tmp_path):
+    _bind(tmp_path, "worktree")
+    result = _run(VALID_PAYLOADS["prompt"], tmp_path, _faulty_copy(tmp_path, "prompt"))
+    store = str(_store(tmp_path / "home"))
+    assert result.returncode == 2
+    assert result.stderr.decode() == _expected("LL-NOBIND", "worktree", SID, store)
+
+
+@pytest.mark.parametrize(
+    "stub, payload", [("tool", "pretooluse-bash"), ("prompt", "prompt")]
+)
+def test_trap_never_blocks_an_ordinary_session(tmp_path, stub, payload):
+    # FR-L-53: an internal failure in an unbound session allows silently.
+    sessions = _store(tmp_path / "home") / "sessions"
+    sessions.mkdir(parents=True)
+    result = _run(VALID_PAYLOADS[payload], tmp_path, _faulty_copy(tmp_path, stub))
+    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
+
+
+# --- message texts (printer block, test-only route) ------------------------
+
+
+def test_design_table_holds_all_eighteen_ids():
+    assert sorted(_design_table()) == sorted(IDS)
+
+
+@pytest.mark.parametrize("msg_id", IDS)
+@pytest.mark.parametrize("level", sorted(LEVELS))
+def test_every_message_prints_the_design_text(tmp_path, msg_id, level):
+    result = _printer(tmp_path, msg_id, level)
+    store = str(_store(tmp_path / "home"))
+    assert result.returncode == 0
+    assert result.stdout == b""
+    assert result.stderr.decode() == _expected(msg_id, LEVELS[level], SID, store)
+
+
+@pytest.mark.parametrize("msg_id", ["LL-BROKEN", "LL-NOBIND"])
+def test_unknown_level_prints_bare_header(tmp_path, msg_id):
+    result = _printer(tmp_path, msg_id, "")
+    store = str(_store(tmp_path / "home"))
+    assert result.stderr.decode() == _expected(msg_id, None, SID, store)
+    assert result.stderr.decode().splitlines()[0] == "Launch-level guard:"
+
+
+def test_tamper_with_invalid_sid_uses_broken_wording(tmp_path):
+    result = _printer(tmp_path, "LL-TAMPER", "F", sid="")
+    store = str(_store(tmp_path / "home"))
+    assert result.stderr.decode() == _expected("LL-BROKEN", "full", "", store)
+
+
+def test_notes_follow_the_lines_state_first(tmp_path):
+    result = _printer(tmp_path, "LL-COMMIT", "W", notes="11")
+    store = str(_store(tmp_path / "home"))
+    assert result.stderr.decode() == (
+        _expected("LL-COMMIT", "worktree", SID, store)
+        + _design_note("LL-STATE")
+        + "\n"
+        + _design_note("LL-TEXT")
+        + "\n"
+    )
+    assert _design_note("LL-STATE") == STATE_NOTE

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
