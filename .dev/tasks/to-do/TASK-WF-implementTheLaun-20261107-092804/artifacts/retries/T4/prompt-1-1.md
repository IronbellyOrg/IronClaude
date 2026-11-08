a4bab76aa7e7d02540ebdca26dd5fa10f9dd73c0
Review one task for spec compliance.

Task brief: ## Task 4: Implement session binding on the first prompt

Depends on: Task 3

In src/superclaude/hooks/scripts/launch-level-guard.sh fill the UserPromptSubmit branch with the binding rules of design section 3 (FR-L-09 as revised B1 to B13, O-20) and the state rules of FR-L-01 to FR-L-07. The store is ~/.claude/state/launch-level/ with pending/<nonce> (name matches ^[0-9a-f]{32}$, content one word: worktree, full or full-submit), sessions/<sid> and sessions/<sid>.ok. A valid session id is a top-level JSON string matching ^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$; numbers and objects are never coerced. A strict marker is the first match of \[sc-launch:v1:([0-9a-f]{32})\] anywhere in the prompt; a loose marker is a prompt that starts, after whitespace or a byte-order mark, with [sc-launch:. A nonempty string agent_id makes the prompt branch exit 0 without binding. No marker and no session records allows the empty-store fast exit. Create the store directories with mkdir -p under umask 077; pending, session and approval entries must be regular, non-symlink files in directories owned by the user.

Binding order: read and parse the envelope once; an unparseable envelope or missing jq with a recognizable launch-marker prompt blocks with LL-NOBIND (no inferred binding); an invalid session id with a marker blocks with LL-NOBIND; an already bound session keeps its level (a newly supplied pending nonce may be consumed and its record removed); an unbound session with no marker is allowed; otherwise consume one pending nonce once and publish sessions/<sid> atomically without replacing an existing file (for example by writing a complete temporary file and linking it into place, which fails when the target exists), and when publication loses a race re-read the winner. A missing or already used nonce with a leading loose marker publishes the word degraded under the same no-replacement rule; a strict marker found only in the middle of a prompt with no usable record blocks with LL-NOBIND; a malformed marker in the middle is ignored. A read-only sessions directory blocks with LL-NOBIND.

Extend tests/hooks/test_launch_level_guard.py with every T-BIND case of MR section 8.2 and the T-ISO and T-FC cases that concern binding, plus a concurrency test that starts at least eight guard processes at once on the same session id and nonce and asserts exactly one binding survives, no sessions/<sid> is overwritten, and every loser reads back the winner's level.

Acceptance criteria:
- uv run pytest tests/hooks/test_launch_level_guard.py -k "bind or BIND" -v passes, covering strict and loose markers, reused nonce giving degraded, new marker in a bound session, read-only sessions directory, invalid id, agent_id prompt, and a malformed mid-prompt marker being ignored.
- The concurrency test passes ten consecutive runs.
- After a successful bind the file sessions/<sid> holds exactly one of worktree, full, full-submit or degraded, and the consumed pending file no longer exists.
- No code path overwrites an existing sessions/<sid>: a test that pre-creates the file with another word and then binds shows the pre-existing word unchanged.

AC ids (source order):
T4.AC1: uv run pytest tests/hooks/test_launch_level_guard.py -k "bind or BIND" -v passes, covering strict and loose markers, reused nonce giving degraded, new marker in a bound session, read-only sessions directory, invalid id, agent_id prompt, and a malformed mid-prompt marker being ignored.
T4.AC2: The concurrency test passes ten consecutive runs.
T4.AC3: After a successful bind the file sessions/<sid> holds exactly one of worktree, full, full-submit or degraded, and the consumed pending file no longer exists.
T4.AC4: No code path overwrites an existing sessions/<sid>: a test that pre-creates the file with another word and then binds shows the pre-existing word unchanged.
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
Start sha: a4bab76aa7e7d02540ebdca26dd5fa10f9dd73c0
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t4-test.log b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t4-test.log
new file mode 100644
index 00000000..ed7d2a3d
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t4-test.log
@@ -0,0 +1,94 @@
+$ uv run pytest tests/hooks/test_launch_level_guard.py -k "bind or BIND" -v
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0 -- /home/coder/workspaces/worktrees/IronClaude/issue-394-launch-level-hook/.venv/bin/python
+cachedir: .pytest_cache
+SuperClaude: 5.0.0
+rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-394-launch-level-hook
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, anyio-4.16.0
+collecting ... collected 158 items / 99 deselected / 59 selected
+
+tests/hooks/test_launch_level_guard.py::test_trap_in_prompt_branch_gives_nobind PASSED [  1%]
+tests/hooks/test_launch_level_guard.py::test_trap_after_marker_gives_nobind_bare_header PASSED [  3%]
+tests/hooks/test_launch_level_guard.py::test_bind_marker_with_record_binds_level[worktree] PASSED [  5%]
+tests/hooks/test_launch_level_guard.py::test_bind_marker_with_record_binds_level[full] PASSED [  6%]
+tests/hooks/test_launch_level_guard.py::test_bind_marker_with_record_binds_level[full-submit] PASSED [  8%]
+tests/hooks/test_launch_level_guard.py::test_bind_marker_at_start_without_record_binds_degraded PASSED [ 10%]
+tests/hooks/test_launch_level_guard.py::test_bind_malformed_marker_at_start_binds_degraded[[sc-launch:v1:ABCDEF0123456789ABCDEF0123456789]] PASSED [ 11%]
+tests/hooks/test_launch_level_guard.py::test_bind_malformed_marker_at_start_binds_degraded[[sc-launch:v1:01234567-89ab-cdef-0123-456789abcdef]] PASSED [ 13%]
+tests/hooks/test_launch_level_guard.py::test_bind_malformed_marker_at_start_binds_degraded[[sc-launch:v1:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa]] PASSED [ 15%]
+tests/hooks/test_launch_level_guard.py::test_bind_malformed_marker_at_start_binds_degraded[[sc-launch:v2:0123456789abcdef0123456789abcdef]] PASSED [ 16%]
+tests/hooks/test_launch_level_guard.py::test_bind_malformed_marker_at_start_binds_degraded[[sc-launch:v1:<nonce>]] PASSED [ 18%]
+tests/hooks/test_launch_level_guard.py::test_bind_marker_after_whitespace_or_bom_binds[   ] PASSED [ 20%]
+tests/hooks/test_launch_level_guard.py::test_bind_marker_after_whitespace_or_bom_binds[\n\n] PASSED [ 22%]
+tests/hooks/test_launch_level_guard.py::test_bind_marker_after_whitespace_or_bom_binds[\t\r\n ] PASSED [ 23%]
+tests/hooks/test_launch_level_guard.py::test_bind_marker_after_whitespace_or_bom_binds[\ufeff] PASSED [ 25%]
+tests/hooks/test_launch_level_guard.py::test_bind_marker_after_whitespace_or_bom_binds[ \ufeff\n\ufeff\t] PASSED [ 27%]
+tests/hooks/test_launch_level_guard.py::test_bind_loose_marker_after_whitespace_or_bom_binds_degraded[   ] PASSED [ 28%]
+tests/hooks/test_launch_level_guard.py::test_bind_loose_marker_after_whitespace_or_bom_binds_degraded[\n\n] PASSED [ 30%]
+tests/hooks/test_launch_level_guard.py::test_bind_loose_marker_after_whitespace_or_bom_binds_degraded[\t\r\n ] PASSED [ 32%]
+tests/hooks/test_launch_level_guard.py::test_bind_loose_marker_after_whitespace_or_bom_binds_degraded[\ufeff] PASSED [ 33%]
+tests/hooks/test_launch_level_guard.py::test_bind_loose_marker_after_whitespace_or_bom_binds_degraded[ \ufeff\n\ufeff\t] PASSED [ 35%]
+tests/hooks/test_launch_level_guard.py::test_bind_strict_marker_mid_prompt_with_record_binds PASSED [ 37%]
+tests/hooks/test_launch_level_guard.py::test_bind_strict_marker_mid_prompt_without_record_blocks_prompt PASSED [ 38%]
+tests/hooks/test_launch_level_guard.py::test_bind_failure_blocks_prompt PASSED [ 40%]
+tests/hooks/test_launch_level_guard.py::test_bind_sessions_dir_created PASSED [ 42%]
+tests/hooks/test_launch_level_guard.py::test_bind_nonce_single_use PASSED [ 44%]
+tests/hooks/test_launch_level_guard.py::test_bind_later_marker_consumes_record_keeps_level[worktree] PASSED [ 45%]
+tests/hooks/test_launch_level_guard.py::test_bind_later_marker_consumes_record_keeps_level[garbage] PASSED [ 47%]
+tests/hooks/test_launch_level_guard.py::test_bind_later_marker_consumes_record_keeps_level[] PASSED [ 49%]
+tests/hooks/test_launch_level_guard.py::test_bind_resume_same_id_governed PASSED [ 50%]
+tests/hooks/test_launch_level_guard.py::test_bind_rename_still_governed PASSED [ 52%]
+tests/hooks/test_launch_level_guard.py::test_bind_reclaim_new_session_new_level PASSED [ 54%]
+tests/hooks/test_launch_level_guard.py::test_bind_invalid_session_ids[.] PASSED [ 55%]
+tests/hooks/test_launch_level_guard.py::test_bind_invalid_session_ids[..] PASSED [ 57%]
+tests/hooks/test_launch_level_guard.py::test_bind_invalid_session_ids[x.ok] PASSED [ 59%]
+tests/hooks/test_launch_level_guard.py::test_bind_invalid_session_ids[a/b] PASSED [ 61%]
+tests/hooks/test_launch_level_guard.py::test_bind_invalid_session_ids[] PASSED [ 62%]
+tests/hooks/test_launch_level_guard.py::test_bind_invalid_session_ids[sid5] PASSED [ 64%]
+tests/hooks/test_launch_level_guard.py::test_bind_invalid_session_ids[7] PASSED [ 66%]
+tests/hooks/test_launch_level_guard.py::test_bind_invalid_session_ids[sid7] PASSED [ 67%]
+tests/hooks/test_launch_level_guard.py::test_bind_invalid_session_ids[None] PASSED [ 69%]
+tests/hooks/test_launch_level_guard.py::test_bind_marker_prompt_with_agent_id_ignored[agent-1] PASSED [ 71%]
+tests/hooks/test_launch_level_guard.py::test_bind_marker_prompt_with_agent_id_ignored[x] PASSED [ 72%]
+tests/hooks/test_launch_level_guard.py::test_bind_jq_missing_marker_prompt_blocked PASSED [ 74%]
+tests/hooks/test_launch_level_guard.py::test_bind_unparseable_marker_prompt_blocked PASSED [ 76%]
+tests/hooks/test_launch_level_guard.py::test_bind_loose_marker_mid_prompt_ignored[False] PASSED [ 77%]
+tests/hooks/test_launch_level_guard.py::test_bind_loose_marker_mid_prompt_ignored[True] PASSED [ 79%]
+tests/hooks/test_launch_level_guard.py::test_bind_two_sessions_isolated PASSED [ 81%]
+tests/hooks/test_launch_level_guard.py::test_bind_same_worktree_other_session_ordinary PASSED [ 83%]
+tests/hooks/test_launch_level_guard.py::test_bind_person_subagent_not_governed PASSED [ 84%]
+tests/hooks/test_launch_level_guard.py::test_bind_forged_nested_session_id PASSED [ 86%]
+tests/hooks/test_launch_level_guard.py::test_bind_jq_missing_ordinary_prompt_allows PASSED [ 88%]
+tests/hooks/test_launch_level_guard.py::test_bind_concurrent_same_session_same_nonce PASSED [ 89%]
+tests/hooks/test_launch_level_guard.py::test_bind_concurrent_other_sessions_same_nonce PASSED [ 91%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[F-LL-NOBIND] PASSED [ 93%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[FS-LL-NOBIND] PASSED [ 94%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[W-LL-NOBIND] PASSED [ 96%]
+tests/hooks/test_launch_level_guard.py::test_every_message_prints_the_design_text[WA-LL-NOBIND] PASSED [ 98%]
+tests/hooks/test_launch_level_guard.py::test_unknown_level_prints_bare_header[LL-NOBIND] PASSED [100%]
+
+====================== 59 passed, 99 deselected in 1.94s =======================
+
+$ for i in 1..10: uv run pytest tests/hooks/test_launch_level_guard.py -k concurren -q
+run 1: ====================== 2 passed, 156 deselected in 1.06s =======================
+run 2: ====================== 2 passed, 156 deselected in 0.14s =======================
+run 3: ====================== 2 passed, 156 deselected in 0.10s =======================
+run 4: ====================== 2 passed, 156 deselected in 0.09s =======================
+run 5: ====================== 2 passed, 156 deselected in 0.09s =======================
+run 6: ====================== 2 passed, 156 deselected in 0.08s =======================
+run 7: ====================== 2 passed, 156 deselected in 0.08s =======================
+run 8: ====================== 2 passed, 156 deselected in 0.08s =======================
+run 9: ====================== 2 passed, 156 deselected in 0.08s =======================
+run 10: ====================== 2 passed, 156 deselected in 0.08s =======================
+
+$ uv run pytest tests/hooks/test_launch_level_guard.py -q
+============================= 158 passed in 1.61s ==============================
+
+$ bash -n src/superclaude/hooks/scripts/launch-level-guard.sh
+syntax ok
+$ grep -c .claude/state src/superclaude/hooks/scripts/launch-level-guard.sh
+0
+$ uv run ruff check / format --check tests/hooks/test_launch_level_guard.py
+All checks passed!
+1 file already formatted
diff --git a/src/superclaude/hooks/scripts/launch-level-guard.sh b/src/superclaude/hooks/scripts/launch-level-guard.sh
index 3885b64d..951e06eb 100755
--- a/src/superclaude/hooks/scripts/launch-level-guard.sh
+++ b/src/superclaude/hooks/scripts/launch-level-guard.sh
@@ -170,20 +170,36 @@ if [ ! -d "$LL_STORE/sessions" ]; then
     *) exit 0 ;;
     esac
 fi
-# One parse of the top-level event and session id. Nested keys never count.
+# One parse of the top-level event, session id and, for a prompt only, the
+# agent_id flag and the prompt text (NUL made a space). Nested keys never count.
 LL_PARSED=$(jq -r '
-    (.hook_event_name | if . == "UserPromptSubmit" or . == "PreToolUse" then . else "OTHER" end)
-    + " " +
-    (.session_id | if type == "string" and test("\\A[A-Za-z0-9][A-Za-z0-9_-]{0,127}\\z") then . else "" end)
+    (.hook_event_name | if . == "UserPromptSubmit" or . == "PreToolUse" then . else "OTHER" end) as $e
+    | $e + " "
+    + (if $e == "UserPromptSubmit" then (.agent_id | if type == "string" and length > 0 then "1" else "0" end) else "0" end)
+    + " "
+    + (.session_id | if type == "string" and test("\\A[A-Za-z0-9][A-Za-z0-9_-]{0,127}\\z") then . else "" end)
+    + "\n"
+    + (if $e == "UserPromptSubmit" then (.prompt | if type == "string" then split("\u0000") | join(" ") else "" end) else "" end)
 ' <<<"$LL_INPUT" 2>/dev/null)
 LL_RC=$?
 if [ "$LL_RC" != 0 ]; then
-    # Identity loss (section 3): no positive binding evidence, allow without
-    # claiming enforcement.
+    # No jq or no parseable envelope: never infer a binding. A recognizable
+    # launch-marker prompt (marker text, no tool_name key) blocks rather than
+    # starting ungoverned; anything else is identity loss (section 3): allow
+    # without claiming enforcement.
+    case $LL_INPUT in
+    *'"tool_name"'*) ;;
+    *'[sc-launch:'*)
+        LL_BRANCH=prompt
+        LL_GOVERNED=1
+        ll_deny LL-NOBIND ;;
+    esac
     exit 0
 fi
-read -r LL_EVENT LL_SID <<<"$LL_PARSED"
+read -r LL_EVENT LL_AGENT LL_SID <<<"${LL_PARSED%%$'\n'*}"
 LL_SID=${LL_SID:-}
+LL_PROMPT=
+case $LL_PARSED in *$'\n'*) LL_PROMPT=${LL_PARSED#*$'\n'} ;; esac
 
 # A valid id with a record (of any file kind) is positively governed. Its level
 # is exactly one allowed word plus an optional newline; anything else is
@@ -215,9 +231,87 @@ PreToolUse) LL_BRANCH=tool ;;
     [ "$LL_GOVERNED" = 1 ] || exit 0 ;;
 esac
 
-# 5. Prompt branch (binding and approval: Task 4, Task 11)
+# 5. Prompt branch: binding (FR-L-09, B1 to B13); approval is Task 11.
+# Writes: mkdir -p sessions; take pending/<nonce> with one rename (mv) to
+# sessions/.take-<sid>, so a nonce is consumed once; publish sessions/<sid> with
+# a hard link (ln), which fails when the target exists, so the first binding is
+# never replaced. Temporary names start with a dot and are never a valid id.
+ll_publish() {
+    local tmp="$LL_SESS/.tmp-$LL_SID-$$"
+    rm -f -- "$tmp" 2>/dev/null
+    if (set -C; printf '%s' "$1" >"$tmp") 2>/dev/null; then
+        ln -- "$tmp" "$LL_SESS/$LL_SID" 2>/dev/null
+    fi
+    rm -f -- "$tmp" 2>/dev/null
+    return 0
+}
+# Publish from a taken record, ours or a racing prompt's for the same id.
+ll_link_take() {
+    local w=
+    { [ -f "$LL_TAKE" ] && [ ! -L "$LL_TAKE" ]; } || return 0
+    { IFS= read -r -N 13 w <"$LL_TAKE"; } 2>/dev/null
+    case $w in
+    worktree | full | full-submit | worktree$'\n' | full$'\n' | full-submit$'\n')
+        ln -- "$LL_TAKE" "$LL_SESS/$LL_SID" 2>/dev/null ;;
+    *) ll_publish degraded ;;
+    esac
+    # Drop the taken record only once a binding exists, so a failed link never loses it.
+    if [ -e "$LL_SESS/$LL_SID" ] || [ -L "$LL_SESS/$LL_SID" ]; then
+        rm -f -- "$LL_TAKE" 2>/dev/null
+    fi
+    return 0
+}
 if [ "$LL_BRANCH" = prompt ]; then
-    exit 0 # stub: prompt branch
+    [ "$LL_AGENT" = 1 ] && exit 0 # B5: a subagent prompt never binds or approves
+    # B6: strict marker anywhere; loose marker at the start after whitespace or a BOM.
+    LL_NONCE=
+    LL_RE='\[sc-launch:v1:([0-9a-f]{32})\]'
+    [[ $LL_PROMPT =~ $LL_RE ]] && LL_NONCE=${BASH_REMATCH[1]}
+    LL_WS=$' \t\r\n'
+    LL_P=$LL_PROMPT
+    while :; do
+        LL_P=${LL_P#"${LL_P%%[!$LL_WS]*}"}
+        case $LL_P in
+        $'\xef\xbb\xbf'*) LL_P=${LL_P:3} ;;
+        *) break ;;
+        esac
+    done
+    LL_LOOSE=0
+    case $LL_P in '[sc-launch:'*) LL_LOOSE=1 ;; esac
+    LL_SESS=$LL_STORE/sessions
+    LL_PEND=$LL_STORE/pending
+    LL_USABLE=0
+    if [ -n "$LL_NONCE" ] && [ -d "$LL_PEND" ] && [ ! -L "$LL_PEND" ] && [ -O "$LL_PEND" ] &&
+        [ -f "$LL_PEND/$LL_NONCE" ] && [ ! -L "$LL_PEND/$LL_NONCE" ]; then
+        LL_USABLE=1
+    fi
+    if [ "$LL_GOVERNED" = 1 ]; then
+        # B8: already bound; the level never changes, a supplied record is consumed.
+        [ "$LL_USABLE" = 1 ] && rm -f -- "$LL_PEND/$LL_NONCE" 2>/dev/null
+        exit 0 # the approval check (Task 11) runs here
+    fi
+    if [ -z "$LL_NONCE" ] && [ "$LL_LOOSE" = 0 ]; then
+        exit 0 # B9: unbound, no marker
+    fi
+    LL_GOVERNED=1 # a launch marker: any failure from here is LL-NOBIND
+    [ -n "$LL_SID" ] || ll_deny LL-NOBIND # B7
+    mkdir -p -- "$LL_SESS" 2>/dev/null
+    if ! { [ -d "$LL_SESS" ] && [ ! -L "$LL_SESS" ] && [ -O "$LL_SESS" ]; }; then
+        ll_deny LL-NOBIND
+    fi
+    LL_TAKE=$LL_SESS/.take-$LL_SID
+    if [ "$LL_USABLE" = 1 ] && [ ! -d "$LL_TAKE" ]; then
+        mv -- "$LL_PEND/$LL_NONCE" "$LL_TAKE" 2>/dev/null # B11: one rename wins the nonce
+    fi
+    ll_link_take
+    if [ "$LL_LOOSE" = 1 ] && [ ! -e "$LL_SESS/$LL_SID" ] && [ ! -L "$LL_SESS/$LL_SID" ]; then
+        ll_publish degraded # B12: missing or used nonce, leading marker
+    fi
+    # B13: whoever won, a regular binding file now exists or the prompt is blocked.
+    if [ -f "$LL_SESS/$LL_SID" ] && [ ! -L "$LL_SESS/$LL_SID" ]; then
+        exit 0
+    fi
+    ll_deny LL-NOBIND
 fi
 
 # 6. Fast paths
diff --git a/tests/hooks/test_launch_level_guard.py b/tests/hooks/test_launch_level_guard.py
index d648ec1f..ef016b67 100644
--- a/tests/hooks/test_launch_level_guard.py
+++ b/tests/hooks/test_launch_level_guard.py
@@ -1,4 +1,4 @@
-"""Behavioral tests for launch-level-guard.sh (issue #394, plan Task 3).
+"""Behavioral tests for launch-level-guard.sh (issue #394, plan Tasks 3 and 4).
 
 Each case runs the real script with a JSON payload on stdin, HOME inside
 tmp_path, CLAUDE_CONFIG_DIR unset and a PATH holding only a temporary bin
@@ -9,7 +9,7 @@ Two test-only routes reach paths the Task 3 skeleton cannot reach through a
 real payload; neither adds behaviour to the shipped script:
 - the printer block (between the ">>> printer" and "<<< printer" comments) is
   run on its own in bash, to check all eighteen message texts;
-- a copy of the script with a stub "exit 0" changed to "exit 7" drives the
+- a copy of the script with one known line changed to "exit 7" drives the
   real EXIT trap through a real payload.
 """
 
@@ -91,7 +91,9 @@ def _store(home: Path) -> Path:
 def _bin(tmp_path: Path, with_jq: bool = True) -> Path:
     bindir = tmp_path / "bin"
     bindir.mkdir(exist_ok=True)
-    tools = ["cat", "sed", "tr"] + (["jq"] if with_jq else [])
+    tools = ["cat", "sed", "tr", "mkdir", "mv", "ln", "rm"] + (
+        ["jq"] if with_jq else []
+    )
     for tool in tools:
         found = shutil.which(tool)
         assert found, tool
@@ -131,6 +133,58 @@ def _bind(tmp_path: Path, word: str = "full", ok: bool = False) -> Path:
     return sessions
 
 
+NONCE = "0123456789abcdef0123456789abcdef"
+NONCE2 = "fedcba9876543210fedcba9876543210"
+
+
+def _marker(nonce: str = NONCE) -> str:
+    return f"[sc-launch:v1:{nonce}]"
+
+
+def _pending(tmp_path: Path, word: str = "full", nonce: str = NONCE) -> Path:
+    """Write a launch record the way publish_pending does (one word, no newline)."""
+    pending = _store(tmp_path / "home") / "pending"
+    pending.mkdir(parents=True, exist_ok=True, mode=0o700)
+    (pending / nonce).write_text(word)
+    return pending / nonce
+
+
+def _prompt(text: str, sid=SID, **extra) -> dict:
+    payload = {"hook_event_name": "UserPromptSubmit", "prompt": text, **extra}
+    if sid is not None:
+        payload["session_id"] = sid
+    return payload
+
+
+def _assert_bound(tmp_path: Path, sid: str, word: str) -> None:
+    """sessions/<sid> holds exactly the word, and no temporary file is left."""
+    sessions = _store(tmp_path / "home") / "sessions"
+    path = sessions / sid
+    assert path.is_file() and not path.is_symlink()
+    assert path.read_text() == word
+    assert [p.name for p in sessions.iterdir() if p.name.startswith(".")] == []
+
+
+def _session_files(tmp_path: Path) -> list[str]:
+    sessions = _store(tmp_path / "home") / "sessions"
+    return sorted(p.name for p in sessions.iterdir()) if sessions.exists() else []
+
+
+def _governed_level(tmp_path: Path, sid: str = SID, **extra):
+    """A PostToolUse call on sid: the skeleton answers a bound id with LL-BROKEN
+    and the level header, so the result shows the level the guard reads."""
+    payload = {"hook_event_name": "PostToolUse", "session_id": sid, **extra}
+    return _run(payload, tmp_path)
+
+
+def _expected_level(tmp_path: Path, word: str, sid: str = SID) -> str:
+    store = str(_store(tmp_path / "home"))
+    level = {"worktree": "worktree", "full": "full", "full-submit": "full --submit"}
+    if word in level:
+        return _expected("LL-BROKEN", level[word], sid, store)
+    return _expected("LL-BROKEN", "worktree", sid, store) + STATE_NOTE + "\n"
+
+
 def _expected(msg_id: str, level: str | None, sid: str, store: str) -> str:
     blocked, why, you_can = _design_table()[msg_id]
     subst = {"{store}": store, "{sid}": sid}
@@ -162,10 +216,18 @@ def _printer(
     )
 
 
+FAULT_LINES = {
+    # First line of each branch; "marker" is the first write after a marker.
+    "tool": "exit 0 # stub: tool branch",
+    "prompt": '[ "$LL_AGENT" = 1 ] && exit 0 # B5: a subagent prompt never binds or approves',
+    "marker": 'mkdir -p -- "$LL_SESS" 2>/dev/null',
+}
+
+
 def _faulty_copy(tmp_path: Path, stub: str) -> Path:
-    """Copy of the script whose stub exits 7, to drive the real EXIT trap."""
+    """Copy of the script with one line made "exit 7", to drive the EXIT trap."""
     text = HOOK.read_text()
-    marker = f"exit 0 # stub: {stub} branch"
+    marker = FAULT_LINES[stub]
     assert text.count(marker) == 1
     copy = tmp_path / "guard-fault.sh"
     copy.write_text(text.replace(marker, "exit 7"))
@@ -227,7 +289,11 @@ VALID_PAYLOADS = {
 def test_empty_home_allows_silently(tmp_path, name):
     result = _run(VALID_PAYLOADS[name], tmp_path)
     assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
-    assert not (tmp_path / "home" / ".claude").exists()
+    if name == "marker-prompt":
+        # A launch marker with no record binds degraded (FR-L-09 B12).
+        _assert_bound(tmp_path, SID, "degraded")
+    else:
+        assert not (tmp_path / "home" / ".claude").exists()
 
 
 def test_empty_home_without_jq_allows_silently(tmp_path):
@@ -329,6 +395,352 @@ def test_trap_never_blocks_an_ordinary_session(tmp_path, stub, payload):
     assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
 
 
+def test_trap_after_marker_gives_nobind_bare_header(tmp_path):
+    # FR-L-09 B6: once a marker is seen, any internal failure blocks the prompt.
+    _pending(tmp_path)
+    result = _run(
+        _prompt(_marker() + " plan"), tmp_path, _faulty_copy(tmp_path, "marker")
+    )
+    store = str(_store(tmp_path / "home"))
+    assert result.returncode == 2
+    assert result.stderr.decode() == _expected("LL-NOBIND", None, SID, store)
+
+
+# --- binding on UserPromptSubmit (FR-L-09, T-BIND-*) -----------------------
+
+WORDS = ["worktree", "full", "full-submit"]
+
+
+def _nobind(tmp_path: Path) -> str:
+    return _expected("LL-NOBIND", None, SID, str(_store(tmp_path / "home")))
+
+
+@pytest.mark.parametrize("word", WORDS)
+def test_bind_marker_with_record_binds_level(tmp_path, word):
+    # T-BIND-1
+    record = _pending(tmp_path, word)
+    result = _run(_prompt(_marker() + " plan issue 7"), tmp_path)
+    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
+    _assert_bound(tmp_path, SID, word)
+    assert not record.exists()
+    assert _governed_level(tmp_path).stderr.decode() == _expected_level(tmp_path, word)
+
+
+def test_bind_marker_at_start_without_record_binds_degraded(tmp_path):
+    # T-BIND-2
+    result = _run(_prompt(_marker() + " plan"), tmp_path)
+    assert (result.returncode, result.stderr) == (0, b"")
+    _assert_bound(tmp_path, SID, "degraded")
+    later = _governed_level(tmp_path)
+    assert later.returncode == 2
+    assert later.stderr.decode() == _expected_level(tmp_path, "degraded")
+
+
+@pytest.mark.parametrize(
+    "marker",
+    [
+        "[sc-launch:v1:" + "ABCDEF0123456789" * 2 + "]",
+        "[sc-launch:v1:01234567-89ab-cdef-0123-456789abcdef]",
+        "[sc-launch:v1:" + "a" * 33 + "]",
+        "[sc-launch:v2:" + NONCE + "]",
+        "[sc-launch:v1:<nonce>]",
+    ],
+)
+def test_bind_malformed_marker_at_start_binds_degraded(tmp_path, marker):
+    # T-BIND-3: a record exists, but a malformed marker never names it.
+    record = _pending(tmp_path, "full-submit")
+    result = _run(_prompt(marker + " plan"), tmp_path)
+    assert (result.returncode, result.stderr) == (0, b"")
+    _assert_bound(tmp_path, SID, "degraded")
+    assert record.read_text() == "full-submit"
+
+
+LEADS = ["   ", "\n\n", "\t\r\n ", "﻿", " ﻿\n﻿\t"]
+
+
+@pytest.mark.parametrize("lead", LEADS)
+def test_bind_marker_after_whitespace_or_bom_binds(tmp_path, lead):
+    # T-BIND-4: with a record the strict marker binds its level ...
+    _pending(tmp_path, "full")
+    result = _run(_prompt(lead + _marker() + " plan"), tmp_path)
+    assert (result.returncode, result.stderr) == (0, b"")
+    _assert_bound(tmp_path, SID, "full")
+
+
+@pytest.mark.parametrize("lead", LEADS)
+def test_bind_loose_marker_after_whitespace_or_bom_binds_degraded(tmp_path, lead):
+    # ... and a loose marker after the same lead binds degraded.
+    result = _run(_prompt(lead + "[sc-launch:v1:<nonce>] plan"), tmp_path)
+    assert (result.returncode, result.stderr) == (0, b"")
+    _assert_bound(tmp_path, SID, "degraded")
+
+
+def test_bind_strict_marker_mid_prompt_with_record_binds(tmp_path):
+    # T-BIND-5
+    record = _pending(tmp_path, "full-submit")
+    result = _run(_prompt("Please start. " + _marker() + " plan"), tmp_path)
+    assert (result.returncode, result.stderr) == (0, b"")
+    _assert_bound(tmp_path, SID, "full-submit")
+    assert not record.exists()
+
+
+def test_bind_strict_marker_mid_prompt_without_record_blocks_prompt(tmp_path):
+    # T-BIND-6 (owner decision O-20)
+    result = _run(_prompt("Example: " + _marker() + " plan"), tmp_path)
+    assert result.returncode == 2
+    assert result.stdout == b""
+    assert result.stderr.decode() == _nobind(tmp_path)
+    assert _session_files(tmp_path) == []
+
+
+@pytest.mark.skipif(os.geteuid() == 0, reason="root ignores directory modes")
+def test_bind_failure_blocks_prompt(tmp_path):
+    # T-BIND-7: read-only sessions/; the record is left for a retry.
+    record = _pending(tmp_path, "full")
+    sessions = _store(tmp_path / "home") / "sessions"
+    sessions.mkdir(mode=0o700)
+    sessions.chmod(0o500)
+    try:
+        result = _run(_prompt(_marker() + " plan"), tmp_path)
+    finally:
+        sessions.chmod(0o700)
+    assert result.returncode == 2
+    assert result.stderr.decode() == _nobind(tmp_path)
+    assert _session_files(tmp_path) == []
+    assert record.read_text() == "full"
+
+
+def test_bind_sessions_dir_created(tmp_path):
+    # T-BIND-8
+    _pending(tmp_path, "worktree")
+    sessions = _store(tmp_path / "home") / "sessions"
+    assert not sessions.exists()
+    result = _run(_prompt(_marker() + " plan"), tmp_path)
+    assert (result.returncode, result.stderr) == (0, b"")
+    _assert_bound(tmp_path, SID, "worktree")
+    assert sessions.stat().st_mode & 0o777 == 0o700
+
+
+def test_bind_nonce_single_use(tmp_path):
+    # T-BIND-9
+    _pending(tmp_path, "full-submit")
+    assert _run(_prompt(_marker() + " plan"), tmp_path).returncode == 0
+    result = _run(_prompt(_marker() + " plan", sid="second-session"), tmp_path)
+    assert (result.returncode, result.stderr) == (0, b"")
+    _assert_bound(tmp_path, SID, "full-submit")
+    _assert_bound(tmp_path, "second-session", "degraded")
+
+
+@pytest.mark.parametrize("old", ["worktree", "garbage", ""])
+def test_bind_later_marker_consumes_record_keeps_level(tmp_path, old):
+    # T-BIND-10, and a pre-created file with another word stays unchanged.
+    sessions = _bind(tmp_path, old)
+    record = _pending(tmp_path, "full-submit")
+    result = _run(_prompt(_marker() + " plan"), tmp_path)
+    assert (result.returncode, result.stderr) == (0, b"")
+    assert (sessions / SID).read_text() == old
+    assert not record.exists()
+    assert _session_files(tmp_path) == [SID]
+
+
+def test_bind_resume_same_id_governed(tmp_path):
+    # T-BIND-11: a later ordinary prompt keeps the binding; a later call reads it.
+    _pending(tmp_path, "full")
+    _run(_prompt(_marker() + " plan"), tmp_path)
+    result = _run(_prompt("continue"), tmp_path)
+    assert (result.returncode, result.stderr) == (0, b"")
+    _assert_bound(tmp_path, SID, "full")
+    assert _governed_level(tmp_path).stderr.decode() == _expected_level(
+        tmp_path, "full"
+    )
+
+
+def test_bind_rename_still_governed(tmp_path):
+    # T-BIND-12: identity is the session id, never the cwd.
+    _pending(tmp_path, "worktree")
+    _run(_prompt(_marker() + " plan", cwd="/work/a"), tmp_path)
+    later = _governed_level(tmp_path, cwd="/work/renamed")
+    assert later.stderr.decode() == _expected_level(tmp_path, "worktree")
+
+
+def test_bind_reclaim_new_session_new_level(tmp_path):
+    # T-BIND-13
+    _pending(tmp_path, "worktree")
+    _run(_prompt(_marker() + " plan", sid="old-session"), tmp_path)
+    _pending(tmp_path, "full", NONCE2)
+    result = _run(_prompt(_marker(NONCE2) + " plan", sid="new-session"), tmp_path)
+    assert (result.returncode, result.stderr) == (0, b"")
+    _assert_bound(tmp_path, "old-session", "worktree")
+    _assert_bound(tmp_path, "new-session", "full")
+
+
+@pytest.mark.parametrize(
+    "sid", [".", "..", "x.ok", "a/b", "", "a" * 129, 7, {"id": SID}, None]
+)
+def test_bind_invalid_session_ids(tmp_path, sid):
+    # T-BIND-14 (prompt half; the PreToolUse half is Task 5).
+    record = _pending(tmp_path, "full")
+    result = _run(_prompt(_marker() + " plan", sid=sid), tmp_path)
+    assert result.returncode == 2
+    assert result.stderr.decode() == _nobind(tmp_path)
+    assert _session_files(tmp_path) == []
+    assert record.read_text() == "full"
+
+
+@pytest.mark.parametrize("agent_id", ["agent-1", "x"])
+def test_bind_marker_prompt_with_agent_id_ignored(tmp_path, agent_id):
+    # T-BIND-15
+    record = _pending(tmp_path, "full")
+    result = _run(_prompt(_marker() + " plan", agent_id=agent_id), tmp_path)
+    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
+    assert _session_files(tmp_path) == []
+    assert record.read_text() == "full"
+
+
+def test_bind_jq_missing_marker_prompt_blocked(tmp_path):
+    # T-BIND-16
+    _bin(tmp_path, with_jq=False)
+    record = _pending(tmp_path, "full")
+    result = _run(_prompt(_marker() + " plan"), tmp_path)
+    assert result.returncode == 2
+    assert result.stderr.decode() == _nobind(tmp_path)
+    assert _session_files(tmp_path) == []
+    assert record.read_text() == "full"
+
+
+def test_bind_unparseable_marker_prompt_blocked(tmp_path):
+    # FR-L-09 B4: a jq failure on a marker prompt acts as B3.
+    raw = b'{"hook_event_name": "UserPromptSubmit", "prompt": "[sc-launch:v1:'
+    result = _run(raw, tmp_path)
+    assert result.returncode == 2
+    assert result.stderr.decode() == _nobind(tmp_path)
+
+
+@pytest.mark.parametrize("store", [False, True])
+def test_bind_loose_marker_mid_prompt_ignored(tmp_path, store):
+    # T-BIND-17
+    if store:
+        sessions = _store(tmp_path / "home") / "sessions"
+        sessions.mkdir(parents=True)
+        (sessions / "someone-else").write_text("full")
+    result = _run(_prompt("see [sc-launch:v2:x] in the docs"), tmp_path)
+    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
+    assert SID not in _session_files(tmp_path)
+
+
+# --- isolation and fail-closed cases that concern binding ------------------
+
+
+def test_bind_two_sessions_isolated(tmp_path):
+    # T-ISO-2
+    _pending(tmp_path, "worktree")
+    _pending(tmp_path, "full-submit", NONCE2)
+    _run(_prompt(_marker() + " a", sid="session-a"), tmp_path)
+    _run(_prompt(_marker(NONCE2) + " b", sid="session-b"), tmp_path)
+    for sid, word in [("session-a", "worktree"), ("session-b", "full-submit")]:
+        got = _governed_level(tmp_path, sid).stderr.decode()
+        assert got == _expected_level(tmp_path, word, sid)
+
+
+def test_bind_same_worktree_other_session_ordinary(tmp_path):
+    # T-ISO-3
+    _pending(tmp_path, "worktree")
+    _run(_prompt(_marker() + " plan", cwd="/work/wt"), tmp_path)
+    result = _run(_prompt("hello", sid="other-session", cwd="/work/wt"), tmp_path)
+    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
+    assert _session_files(tmp_path) == [SID]
+
+
+def test_bind_person_subagent_not_governed(tmp_path):
+    # T-ISO-4 (X-004): unbound id, agent_id, the bound worktree's cwd.
+    _bind(tmp_path, "worktree")
+    _pending(tmp_path, "full")
+    payload = _prompt(
+        _marker() + " plan", sid="person-session", agent_id="a1", cwd="/work/wt"
+    )
+    result = _run(payload, tmp_path)
+    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
+    assert _session_files(tmp_path) == [SID]
+
+
+def test_bind_forged_nested_session_id(tmp_path):
+    # T-ISO-6: only the top-level session_id counts.
+    _bind(tmp_path, "worktree")
+    ordinary = _prompt(_marker() + " plan", sid="unbound-one", meta={"session_id": SID})
+    record = _pending(tmp_path, "full")
+    result = _run(ordinary, tmp_path)
+    assert (result.returncode, result.stderr) == (0, b"")
+    _assert_bound(tmp_path, "unbound-one", "full")
+    governed = _prompt(_marker(NONCE2) + " plan", meta={"session_id": "unbound-two"})
+    record = _pending(tmp_path, "full-submit", NONCE2)
+    result = _run(governed, tmp_path)
+    assert (result.returncode, result.stderr) == (0, b"")
+    assert not record.exists()
+    _assert_bound(tmp_path, SID, "worktree")
+    assert "unbound-two" not in _session_files(tmp_path)
+
+
+def test_bind_jq_missing_ordinary_prompt_allows(tmp_path):
+    # T-FC-1 (prompt half): no jq and no marker never blocks a prompt.
+    _bin(tmp_path, with_jq=False)
+    _bind(tmp_path, "full")
+    result = _run(_prompt("continue"), tmp_path)
+    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
+
+
+# --- concurrency (FR-L-09 B11: one nonce binds at most one session) --------
+
+
+def _race(tmp_path: Path, sids: list[str]) -> list[subprocess.CompletedProcess]:
+    home = tmp_path / "home"
+    home.mkdir(exist_ok=True)
+    env = _env(home, _bin(tmp_path))
+    procs = [
+        subprocess.Popen(
+            [BASH, str(HOOK)],
+            stdin=subprocess.PIPE,
+            stdout=subprocess.PIPE,
+            stderr=subprocess.PIPE,
+            env=env,
+        )
+        for _ in sids
+    ]
+    # Every guard is started and blocked on stdin; release them together.
+    payloads = [json.dumps(_prompt(_marker() + " plan", sid=s)).encode() for s in sids]
+    for proc, data in zip(procs, payloads):
+        proc.stdin.write(data)
+    for proc in procs:
+        proc.stdin.close()
+    results = []
+    for proc in procs:
+        out, err = proc.stdout.read(), proc.stderr.read()
+        rc = proc.wait(timeout=20)
+        results.append(subprocess.CompletedProcess(proc.args, rc, out, err))
+    return results
+
+
+def test_bind_concurrent_same_session_same_nonce(tmp_path):
+    record = _pending(tmp_path, "full-submit")
+    results = _race(tmp_path, [SID] * 12)
+    assert [(r.returncode, r.stderr) for r in results] == [(0, b"")] * 12
+    _assert_bound(tmp_path, SID, "full-submit")
+    assert _session_files(tmp_path) == [SID]
+    assert not record.exists()
+
+
+def test_bind_concurrent_other_sessions_same_nonce(tmp_path):
+    record = _pending(tmp_path, "full")
+    sids = [f"racer-{i}" for i in range(12)]
+    results = _race(tmp_path, sids)
+    assert [(r.returncode, r.stderr) for r in results] == [(0, b"")] * 12
+    words = sorted(
+        (_store(tmp_path / "home") / "sessions" / s).read_text() for s in sids
+    )
+    assert words == ["degraded"] * 11 + ["full"]
+    assert _session_files(tmp_path) == sorted(sids)
+    assert not record.exists()
+
+
 # --- message texts (printer block, test-only route) ------------------------
 
 

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
