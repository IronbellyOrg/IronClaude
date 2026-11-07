2e08cfbe0f231dcbea4d9887a017f686a608a579
Review one task for spec compliance.

Task brief: ## Task 10: Implement the remaining tool classifiers and the full grid oracle

Depends on: Task 9

In src/superclaude/hooks/scripts/launch-level-guard.sh add the classifiers of design section 5.2 not yet built: Agent and Task (FR-L-41) are NONE, background or not, unless isolation is remote (ESCAPE), and the prompt is never scanned; CronCreate, CronDelete, CronList and the Schedule tools give TURN (FR-L-43); RemoteTrigger, Workflow and SendMessage give ESCAPE (FR-L-46); MCP tools (FR-L-45) take N as the text after the last double underscore, lower-cased: no keyword from merge, push, commit, pull_request, create_or_update_file, delete_file, update_ref, create_ref, create_branch gives NONE, the prefixes list_, get_, search_ and read_ give NONE, a name holding merge gives MERGE, anything else gives MCP; anything else matched (FR-L-52) is NONE on an explicit allow path. The script re-checks tool names itself because the registration matcher anchors are unverified (FR-L-66, U15).

Extend tests/hooks/test_launch_level_guard.py with the T-TRN, T-MCP, T-COR and T-GAP cases of MR section 8.2 and complete the hand-written oracle EXPECTED so it covers all sixteen classes across W, WA, F and FS by driving real tool calls (T-GRID-1 to T-GRID-5), checking that every class has a test row and that the oracle is written independently of the script's case statement.

Acceptance criteria:
- CronCreate and ScheduleWakeup exit 2 with LL-TURN at W and exit 0 at WA, F and FS; a local Agent call exits 0 at every level; an Agent call with isolation remote, a Workflow call and a SendMessage call exit 2 with LL-ESCAPE.
- An MCP tool named mcp__github__merge_pull_request exits 2 with LL-MERGE, mcp__github__push_files exits 2 with LL-MCP, and mcp__github__list_issues exits 0.
- The pinned gaps of design section 4 row 33 (a variable-built git word, a bracketed binary name, a script file) exit 0 and their tests are marked as accepted leaks.
- uv run pytest tests/hooks/test_launch_level_guard.py -k "GRID or TRN or MCP or COR or GAP" -v passes, and the test module fails if any class in the grid has no oracle row.

AC ids (source order):
T10.AC1: CronCreate and ScheduleWakeup exit 2 with LL-TURN at W and exit 0 at WA, F and FS; a local Agent call exits 0 at every level; an Agent call with isolation remote, a Workflow call and a SendMessage call exit 2 with LL-ESCAPE.
T10.AC2: An MCP tool named mcp__github__merge_pull_request exits 2 with LL-MERGE, mcp__github__push_files exits 2 with LL-MCP, and mcp__github__list_issues exits 0.
T10.AC3: The pinned gaps of design section 4 row 33 (a variable-built git word, a bracketed binary name, a script file) exit 0 and their tests are marked as accepted leaks.
T10.AC4: uv run pytest tests/hooks/test_launch_level_guard.py -k "GRID or TRN or MCP or COR or GAP" -v passes, and the test module fails if any class in the grid has no oracle row.
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
Start sha: 2e08cfbe0f231dcbea4d9887a017f686a608a579
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t10-test.log b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t10-test.log
new file mode 100644
index 00000000..b6926137
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t10-test.log
@@ -0,0 +1,7 @@
+$ uv run pytest tests/hooks/test_launch_level_guard.py -k "GRID or TRN or MCP or COR or GAP" -q
+tests/hooks/test_launch_level_guard.py ................................. [100%]
+==================== 1143 passed, 1960 deselected in 19.69s ====================
+(-v run of the same selection: 1143 PASSED, 0 FAILED/ERROR)
+
+$ uv run pytest tests/hooks/test_launch_level_guard.py -q
+============================ 3103 passed in 52.38s =============================
diff --git a/src/superclaude/hooks/scripts/launch-level-guard.sh b/src/superclaude/hooks/scripts/launch-level-guard.sh
index ba7321bd..fb1a041c 100755
--- a/src/superclaude/hooks/scripts/launch-level-guard.sh
+++ b/src/superclaude/hooks/scripts/launch-level-guard.sh
@@ -5,8 +5,8 @@
 # with a message on stderr; never exit 1, no onFailure. Only a session that the
 # claim script launched (a valid top-level session_id bound in the store) is
 # governed; every other session is ordinary and never blocked (FR-L-53).
-# Ten-part layout (DD-1); Tasks 5 to 9 classify Skill, BIG, NM1a, git, gh, curl,
-# API text, tamper and escape; the rest is NONE until Task 10.
+# Ten-part layout (DD-1); part 8 holds the section 5.2 classifiers (Skill, Bash,
+# Monitor, edits, Agent/Task, Cron/Schedule, escape and MCP tools); others NONE.
 # launch-level-guard-version: 1
 
 # 1. Settings
@@ -372,7 +372,7 @@ if [ "$LL_BRANCH" = tool ]; then
     [ "$LL_BAD" = 1 ] && ll_deny LL-BROKEN # a nonstring tool field or an embedded NUL
 
     # 7. The tool fields come from the one jq parse in part 4.
-    # 8. Classifiers add classes to LL_CLASSES (Tasks 5 to 10); none gives NONE.
+    # 8. Classifiers add classes to LL_CLASSES (section 5.2); none gives NONE.
     LL_CLASSES=' '
     LL_TT= # the text the tamper tokens are looked for in (T or the edit path)
     if [ "$LL_TOOL" = Skill ]; then
@@ -655,6 +655,27 @@ if [ "$LL_BRANCH" = tool ]; then
         # FR-L-42, FR-L-51: the tamper check only; contents are never read.
         LL_TT=$EPATH
         case $EPATH in */../* | */..) LL_CLASSES+='TAMPER ' ;; esac
+    elif [ "$LL_TOOL" = Agent ] || [ "$LL_TOOL" = Task ]; then
+        # FR-L-41, FR-L-46: local or background is NONE; the prompt is never scanned.
+        [ "$LL_ISO" = remote ] && LL_CLASSES+='ESCAPE '
+    elif [[ $LL_TOOL =~ ^(Cron|Schedule)[A-Za-z]*$ ]]; then
+        LL_CLASSES+='TURN ' # FR-L-43
+    elif [ "$LL_TOOL" = RemoteTrigger ] || [ "$LL_TOOL" = Workflow ] || [ "$LL_TOOL" = SendMessage ]; then
+        LL_CLASSES+='ESCAPE ' # FR-L-46
+    elif [[ $LL_TOOL == mcp__* ]]; then
+        # FR-L-45: N is the text after the last "__", lower case.
+        LL_N=${LL_TOOL##*__}
+        LL_N=${LL_N,,}
+        case $LL_N in
+        *merge* | *push* | *commit* | *pull_request* | *create_or_update_file* | *delete_file* | *update_ref* | *create_ref* | *create_branch*)
+            case $LL_N in
+            list_* | get_* | search_* | read_*) ;;
+            *merge*) LL_CLASSES+='MERGE ' ;;
+            *) LL_CLASSES+='MCP ' ;;
+            esac ;;
+        esac
+    else
+        : # FR-L-66: any other tool the matcher let through is NONE.
     fi
     # FR-L-49: the tamper tokens in T or the edit path; the store part is
     # built from LL_S1 and LL_S2, so this text never names it joined.
diff --git a/tests/hooks/test_launch_level_guard.py b/tests/hooks/test_launch_level_guard.py
index e38e85cd..d980034c 100644
--- a/tests/hooks/test_launch_level_guard.py
+++ b/tests/hooks/test_launch_level_guard.py
@@ -1,4 +1,4 @@
-"""Behavioral tests for launch-level-guard.sh (issue #394, plan Tasks 3 to 7).
+"""Behavioral tests for launch-level-guard.sh (issue #394, plan Tasks 3 to 10).
 
 Each case runs the real script with a JSON payload on stdin, HOME inside
 tmp_path, CLAUDE_CONFIG_DIR unset and a PATH holding only a temporary bin
@@ -764,9 +764,82 @@ LEVEL_FILES = {
     "FS": ("full-submit", False),
 }
 
+# Hand-written oracle of the policy grid (design section 4), one row per class,
+# typed from the design table and never derived from the script: None allows,
+# otherwise the message id a call of that class alone is blocked with.
+GRID_CLASSES = (
+    "IMPL",
+    "TURN",
+    "SUBMIT",
+    "COMMIT",
+    "PUSH",
+    "PUSHFORM",
+    "PROTECTED",
+    "MERGE",
+    "GHWRITE",
+    "UNKNOWN",
+    "MCP",
+    "ESCAPE",
+    "TAMPER",
+    "SKILL",
+    "BIG",
+    "REPO",
+)
+EXPECTED = {
+    "NONE": {"W": None, "WA": None, "F": None, "FS": None},
+    "IMPL": {"W": "LL-IMPL", "WA": None, "F": None, "FS": None},
+    "TURN": {"W": "LL-TURN", "WA": None, "F": None, "FS": None},
+    "SUBMIT": {"W": "LL-SUBMIT", "WA": "LL-SUBMIT", "F": "LL-SUBMIT", "FS": None},
+    "COMMIT": {"W": "LL-COMMIT", "WA": "LL-COMMIT", "F": "LL-COMMIT", "FS": None},
+    "PUSH": {"W": "LL-PUSH", "WA": "LL-PUSH", "F": "LL-PUSH", "FS": None},
+    "SKILL": {"W": "LL-SKILL", "WA": "LL-SKILL", "F": "LL-SKILL", "FS": None},
+    "REPO": {"W": "LL-REPO", "WA": "LL-REPO", "F": "LL-REPO", "FS": "LL-REPO"},
+    "PUSHFORM": {
+        "W": "LL-PUSH-FORM",
+        "WA": "LL-PUSH-FORM",
+        "F": "LL-PUSH-FORM",
+        "FS": "LL-PUSH-FORM",
+    },
+    "PROTECTED": {
+        "W": "LL-PROTECTED",
+        "WA": "LL-PROTECTED",
+        "F": "LL-PROTECTED",
+        "FS": "LL-PROTECTED",
+    },
+    "MERGE": {"W": "LL-MERGE", "WA": "LL-MERGE", "F": "LL-MERGE", "FS": "LL-MERGE"},
+    "GHWRITE": {
+        "W": "LL-GH-WRITE",
+        "WA": "LL-GH-WRITE",
+        "F": "LL-GH-WRITE",
+        "FS": "LL-GH-WRITE",
+    },
+    "UNKNOWN": {
+        "W": "LL-UNKNOWN",
+        "WA": "LL-UNKNOWN",
+        "F": "LL-UNKNOWN",
+        "FS": "LL-UNKNOWN",
+    },
+    "MCP": {"W": "LL-MCP", "WA": "LL-MCP", "F": "LL-MCP", "FS": "LL-MCP"},
+    "ESCAPE": {
+        "W": "LL-ESCAPE",
+        "WA": "LL-ESCAPE",
+        "F": "LL-ESCAPE",
+        "FS": "LL-ESCAPE",
+    },
+    "TAMPER": {
+        "W": "LL-TAMPER",
+        "WA": "LL-TAMPER",
+        "F": "LL-TAMPER",
+        "FS": "LL-TAMPER",
+    },
+    "BIG": {"W": "LL-BIG", "WA": "LL-BIG", "F": "LL-BIG", "FS": "LL-BIG"},
+}
+# T-GRID-2 at import time too: a class without an oracle row fails the module.
+assert set(GRID_CLASSES) | {"NONE"} == set(EXPECTED), "grid class without oracle row"
+
 # Hand-written oracle for the Skill rows of the grid (design section 8):
 # None allows, otherwise the message id the call is blocked with.
-EXPECTED = {
+SKILL_EXPECTED = {
     "sc:implement": {"W": "LL-IMPL", "WA": None, "F": None, "FS": None},
     "sc:pr-submit": {"W": "LL-SUBMIT", "WA": "LL-SUBMIT", "F": "LL-SUBMIT", "FS": None},
     "sc:issue": {
@@ -810,11 +883,11 @@ def _assert_decision(result, tmp_path, msg_id, level, note=False, text=False):
 
 
 @pytest.mark.parametrize("level", sorted(LEVEL_FILES))
-@pytest.mark.parametrize("name", sorted(EXPECTED))
+@pytest.mark.parametrize("name", sorted(SKILL_EXPECTED))
 def test_skill_grid_matches_oracle(tmp_path, name, level):
     _bind(tmp_path, *LEVEL_FILES[level])
     result = _run(_skill(name), tmp_path)
-    _assert_decision(result, tmp_path, EXPECTED[name][level], level)
+    _assert_decision(result, tmp_path, SKILL_EXPECTED[name][level], level)
 
 
 IMPL_SPELLINGS = [
@@ -930,15 +1003,11 @@ def test_huge_fields_are_quick(tmp_path):
     "tool_name, tool_input",
     [
         ("Edit", {"file_path": "/x/settings.json"}),
-        ("Agent", {"isolation": "remote"}),
         ("Read", {"file_path": "/etc/passwd"}),
-        ("mcp__github__merge_pull_request", {}),
     ],
 )
-def test_other_tools_are_none_until_their_classifiers_exist(
-    tmp_path, tool_name, tool_input
-):
-    # Tasks 8 to 10 add these classifiers; until then such a call is NONE.
+def test_other_tools_are_none(tmp_path, tool_name, tool_input):
+    # FR-L-66: a tool no classifier names is NONE (Agent and MCP: Task 10 tests).
     _bind(tmp_path, "worktree")
     payload = {
         "hook_event_name": "PreToolUse",
@@ -984,7 +1053,7 @@ def test_input_error_allows_ordinary(tmp_path, name):
 
 
 @pytest.mark.parametrize("store", ["empty", "other-sessions"])
-@pytest.mark.parametrize("name", sorted(EXPECTED))
+@pytest.mark.parametrize("name", sorted(SKILL_EXPECTED))
 def test_ordinary_session_never_blocked(tmp_path, store, name):
     # T-ISO-1
     if store == "other-sessions":
@@ -2779,3 +2848,352 @@ def test_tamper_message_names_store_and_session(tmp_path, level):
     assert result.returncode == 2
     you_can = result.stderr.decode().splitlines()[3]
     assert you_can.startswith("You can: ") and you_can.endswith(f": {rm}")
+
+
+# --- the full grid, Agent/Task, TURN, MCP, escape tools, gaps, corpus (Task 10)
+
+
+def _tool(tool_name: str, sid: str = SID, **tool_input) -> dict:
+    return {
+        "hook_event_name": "PreToolUse",
+        "session_id": sid,
+        "tool_name": tool_name,
+        "tool_input": tool_input,
+    }
+
+
+def _text_note(payload: dict, msg_id) -> bool:
+    # LL-TEXT follows any block of a Bash or Monitor call (section 9).
+    return msg_id is not None and payload["tool_name"] in ("Bash", "Monitor")
+
+
+# T-GRID-1: real tool calls, at least one per class. A natural call can carry a
+# second class of higher precedence; such a row lists its own decisions, and at
+# FS (where that second class is allowed) its class's own oracle cell shows.
+_VIA_SUBMIT = {"W": "LL-SUBMIT", "WA": "LL-SUBMIT", "F": "LL-SUBMIT", "FS": "LL-REPO"}
+_VIA_PUSH = {"W": "LL-PUSH", "WA": "LL-PUSH", "F": "LL-PUSH", "FS": "LL-PUSH-FORM"}
+GRID_CASES = [
+    ("NONE", "skill-workflow", _skill("sc:workflow"), None),
+    ("NONE", "read", _tool("Read", file_path="/etc/passwd"), None),
+    ("NONE", "agent-local", _tool("Agent", prompt="git push origin main"), None),
+    ("NONE", "mcp-list", _tool("mcp__github__list_issues"), None),
+    ("NONE", "bash-ls", _bash("ls"), None),
+    ("IMPL", "skill-implement", _skill("sc:implement"), None),
+    ("TURN", "cron-create", _tool("CronCreate", prompt="approved"), None),
+    ("TURN", "schedule-wakeup", _tool("ScheduleWakeup"), None),
+    ("SUBMIT", "skill-pr-submit", _skill("sc:pr-submit"), None),
+    ("SUBMIT", "gh-pr-create-repo", _bash(f"gh pr create {REPO_FLAG} --title x"), None),
+    ("COMMIT", "git-commit", _bash("git commit -m x"), None),
+    ("PUSH", "git-push-canonical", _bash("git push -u origin feature"), None),
+    ("PUSHFORM", "git-push-force", _bash("git push --force origin f"), _VIA_PUSH),
+    ("PROTECTED", "git-push-main", _bash("git push origin main"), None),
+    ("MERGE", "gh-pr-merge", _bash("gh pr merge 5"), None),
+    ("MERGE", "mcp-merge", _tool("mcp__github__merge_pull_request"), None),
+    ("GHWRITE", "gh-api-graphql", _bash("gh api graphql"), None),
+    ("UNKNOWN", "git-alias", _bash("git ci"), None),
+    ("MCP", "mcp-push-files", _tool("mcp__github__push_files"), None),
+    ("ESCAPE", "skill-issue", _skill("sc:issue"), None),
+    ("ESCAPE", "agent-remote", _tool("Agent", isolation="remote"), None),
+    ("ESCAPE", "workflow", _tool("Workflow"), None),
+    ("TAMPER", "edit-settings", _edit("Edit", "~/.claude/settings.json"), None),
+    ("SKILL", "skill-empty", _skill(""), None),
+    ("BIG", "bash-big", _bash("echo " + "y" * 70_000), None),
+    ("REPO", "gh-pr-create", _bash("gh pr create --title x"), _VIA_SUBMIT),
+]
+
+
+def _grid_params():
+    for cls, case_id, payload, own in GRID_CASES:
+        for level in LEVEL_ORDER:
+            msg_id = (own or EXPECTED[cls])[level]
+            yield pytest.param(
+                payload, level, msg_id, id=f"GRID-{cls}-{case_id}-{level}"
+            )
+
+
+@pytest.mark.parametrize("payload, level, msg_id", list(_grid_params()))
+def test_grid_policy(tmp_path, payload, level, msg_id):
+    # T-GRID-1
+    _bind(tmp_path, *LEVEL_FILES[level])
+    result = _run(payload, tmp_path)
+    _assert_decision(result, tmp_path, msg_id, level, text=_text_note(payload, msg_id))
+
+
+def test_grid_complete():
+    # T-GRID-2: every class has an oracle row with W, WA, F and FS, and a case.
+    assert len(set(GRID_CLASSES)) == 16
+    assert set(EXPECTED) == set(GRID_CLASSES) | {"NONE"}
+    for cls, row in EXPECTED.items():
+        assert sorted(row) == sorted(LEVEL_ORDER), cls
+    assert {cls for cls, *_ in GRID_CASES} == set(EXPECTED)
+    for cls, _case_id, _payload, own in GRID_CASES:
+        if own:
+            assert own["FS"] == EXPECTED[cls]["FS"], cls
+
+
+_STEP_CASES = {
+    "skill-implement": _skill("sc:implement"),
+    "git-commit": _bash("git commit -m x"),
+    "git-push": _bash("git push -u origin feature"),
+    "skill-pr-submit": _skill("sc:pr-submit"),
+    "gh-pr-create-repo": _bash(f"gh pr create {REPO_FLAG} --title x"),
+    "write-plan": _edit("Write", ".dev/tasks/x/plan.md"),
+    "skill-workflow": _skill("sc:workflow"),
+}
+# T-GRID-3 (W), T-GRID-4 (F), T-GRID-5 (FS), typed from MR section 8.2.
+GRID_STEPS = {
+    "W": {
+        "skill-implement": "LL-IMPL",
+        "git-commit": "LL-COMMIT",
+        "git-push": "LL-PUSH",
+        "skill-pr-submit": "LL-SUBMIT",
+        "gh-pr-create-repo": "LL-SUBMIT",
+        "write-plan": None,
+        "skill-workflow": None,
+    },
+    "F": {
+        "skill-implement": None,
+        "git-commit": "LL-COMMIT",
+        "git-push": "LL-PUSH",
+        "skill-pr-submit": "LL-SUBMIT",
+        "gh-pr-create-repo": "LL-SUBMIT",
+    },
+    "FS": {
+        "git-commit": None,
+        "git-push": None,
+        "skill-pr-submit": None,
+        "gh-pr-create-repo": None,
+    },
+}
+
+
+@pytest.mark.parametrize(
+    "level, name, msg_id",
+    [
+        pytest.param(level, name, msg_id, id=f"GRID-step-{level}-{name}")
+        for level, rows in GRID_STEPS.items()
+        for name, msg_id in rows.items()
+    ],
+)
+def test_grid_level_steps(tmp_path, level, name, msg_id):
+    payload = _STEP_CASES[name]
+    _bind(tmp_path, *LEVEL_FILES[level])
+    result = _run(payload, tmp_path)
+    _assert_decision(result, tmp_path, msg_id, level, text=_text_note(payload, msg_id))
+
+
+TURN_TOOLS = ["CronCreate", "CronDelete", "CronList", "Cron", "ScheduleWakeup"]
+
+
+@pytest.mark.parametrize("level", LEVEL_ORDER)
+@pytest.mark.parametrize("tool", TURN_TOOLS)
+def test_trn_cron_schedule_turn_only_at_w(tmp_path, tool, level):
+    # T-TRN-1, T-TRN-2: FR-L-43, ^Cron[A-Za-z]*$ and ^Schedule[A-Za-z]*$.
+    _bind(tmp_path, *LEVEL_FILES[level])
+    msg_id = "LL-TURN" if level == "W" else None
+    _assert_decision(_run(_tool(tool, prompt="x"), tmp_path), tmp_path, msg_id, level)
+
+
+@pytest.mark.parametrize("tool", ["cronCreate", "XCronCreate", "Cron2", "Scheduler_x"])
+def test_trn_lookalike_names_stay_none(tmp_path, tool):
+    _bind(tmp_path, "worktree")
+    _assert_decision(_run(_tool(tool), tmp_path), tmp_path, None, "W")
+
+
+@pytest.mark.parametrize(
+    "payload, level, msg_id",
+    [
+        pytest.param(
+            _bash("git push origin main", tool="Monitor"),
+            "FS",
+            "LL-PROTECTED",
+            id="TRN-3-monitor-main",
+        ),
+        pytest.param(
+            _bash("git commit -m x", run_in_background=True),
+            "F",
+            "LL-COMMIT",
+            id="TRN-3-background-commit",
+        ),
+    ],
+)
+def test_trn_monitor_and_background_text_classified(tmp_path, payload, level, msg_id):
+    # T-TRN-3: FR-L-44, the command is classified like a foreground Bash command.
+    _bind(tmp_path, *LEVEL_FILES[level])
+    _assert_decision(_run(payload, tmp_path), tmp_path, msg_id, level, text=True)
+
+
+# T-TRN-4: every route that can start a turn, at W.
+TRN_ROUTES = [
+    ("cron-create", _tool("CronCreate", prompt="approved"), "LL-TURN"),
+    ("cron-delete", _tool("CronDelete"), "LL-TURN"),
+    ("schedule-wakeup", _tool("ScheduleWakeup"), "LL-TURN"),
+    ("orca-send", _bash("orca terminal send --text approved"), "LL-ESCAPE"),
+    ("orca-type", _bash("orca computer type-text approved"), "LL-ESCAPE"),
+    ("tmux-send-keys", _bash("tmux send-keys approved Enter"), "LL-ESCAPE"),
+    ("screen-stuff", _bash("screen -X stuff approved"), "LL-ESCAPE"),
+    ("xdotool", _bash("xdotool type approved"), "LL-ESCAPE"),
+    ("send-message", _tool("SendMessage", to="main", message="approved"), "LL-ESCAPE"),
+    ("tmux-split", _bash("tm\\\nux send-keys approved Enter"), "LL-UNKNOWN"),
+    ("monitor-ls", _bash("ls", tool="Monitor"), None),
+    ("bash-background", _bash("ls", run_in_background=True), None),
+    ("agent-background", _tool("Agent", prompt="x", run_in_background=True), None),
+    ("task-background", _tool("Task", prompt="x", run_in_background=True), None),
+]
+
+
+@pytest.mark.parametrize(
+    "payload, msg_id",
+    [pytest.param(p, m, id=f"TRN-4-{name}") for name, p, m in TRN_ROUTES],
+)
+def test_trn_route_table_at_w(tmp_path, payload, msg_id):
+    _bind(tmp_path, *LEVEL_FILES["W"])
+    result = _run(payload, tmp_path)
+    _assert_decision(result, tmp_path, msg_id, "W", text=_text_note(payload, msg_id))
+
+
+@pytest.mark.parametrize("level", LEVEL_ORDER)
+@pytest.mark.parametrize("tool", ["Agent", "Task"])
+@pytest.mark.parametrize(
+    "tool_input, msg_id",
+    [
+        pytest.param({"isolation": "remote"}, "LL-ESCAPE", id="remote"),
+        pytest.param({"isolation": "worktree"}, None, id="worktree"),
+        pytest.param({}, None, id="local"),
+        pytest.param({"run_in_background": True}, None, id="background"),
+        pytest.param(
+            {"prompt": "gh pr merge 5; git push origin main"}, None, id="prompt"
+        ),
+    ],
+)
+def test_esc_agent_task_isolation(tmp_path, tool, tool_input, msg_id, level):
+    # T-ESC-3, T-ISO-9: FR-L-41, FR-L-46; Agent and Task decide alike, and
+    # the prompt is never scanned.
+    _bind(tmp_path, *LEVEL_FILES[level])
+    result = _run(_tool(tool, **tool_input), tmp_path)
+    _assert_decision(result, tmp_path, msg_id, level)
+
+
+@pytest.mark.parametrize("level", LEVEL_ORDER)
+@pytest.mark.parametrize("tool", ["Workflow", "RemoteTrigger", "SendMessage"])
+def test_esc_escape_tools(tmp_path, tool, level):
+    # T-ESC-4: FR-L-46.
+    _bind(tmp_path, *LEVEL_FILES[level])
+    _assert_decision(_run(_tool(tool), tmp_path), tmp_path, "LL-ESCAPE", level)
+
+
+# T-MCP-1 to T-MCP-3: FR-L-45, N is the text after the last "__", lower case.
+MCP_CASES = [
+    ("mcp__github__merge_pull_request", "LL-MERGE"),
+    ("mcp__github__MERGE_PULL_REQUEST", "LL-MERGE"),
+    ("mcp__gitlab__accept_merge_request", "LL-MERGE"),
+    ("mcp__github__push_files", "LL-MCP"),
+    ("mcp__github__create_or_update_file", "LL-MCP"),
+    ("mcp__github__create_pull_request", "LL-MCP"),
+    ("mcp__github__delete_file", "LL-MCP"),
+    ("mcp__github__create_branch", "LL-MCP"),
+    ("mcp__github__update_ref", "LL-MCP"),
+    ("mcp__git__git_commit", "LL-MCP"),
+    ("mcp__github__list_commits", None),
+    ("mcp__github__get_commit", None),
+    ("mcp__github__list_issues", None),
+    ("mcp__github__get_pull_request", None),
+    ("mcp__github__search_pull_requests", None),
+    ("mcp__github__list_merge_requests", None),
+    ("mcp__github__read_file", None),
+    ("mcp__github__create_issue", None),
+    ("mcp__codegraph__codegraph_search", None),
+    # The keyword is in the server part, not in N: NONE.
+    ("mcp__merge_push__list_items", None),
+]
+
+
+@pytest.mark.parametrize("level", LEVEL_ORDER)
+@pytest.mark.parametrize("tool, msg_id", MCP_CASES)
+def test_mcp_tools(tmp_path, tool, msg_id, level):
+    _bind(tmp_path, *LEVEL_FILES[level])
+    _assert_decision(_run(_tool(tool), tmp_path), tmp_path, msg_id, level)
+
+
+@pytest.mark.parametrize(
+    "tool, tool_input",
+    [
+        ("mcp__github__merge_pull_request", {}),
+        ("mcp__github__push_files", {}),
+        ("CronCreate", {"prompt": "approved"}),
+        ("Workflow", {}),
+        ("Agent", {"isolation": "remote"}),
+    ],
+)
+def test_mcp_ordinary_session_allowed(tmp_path, tool, tool_input):
+    # T-MCP-4 (and the other Task 10 classes): an unbound session exits 0.
+    _bind(tmp_path, *LEVEL_FILES["W"])
+    result = _run(_tool(tool, sid="ordinary-session", **tool_input), tmp_path)
+    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
+
+
+# T-GAP-1: design section 4 row 33. ACCEPTED LEAKS of residual risk R1 (a
+# command name built from a variable, an escape or a glob, or a script file):
+# each is pinned as allowed at every level, so closing one is a deliberate
+# change (owner decision O-7), not a silent one.
+ACCEPTED_LEAKS = {
+    "T-ATK-26": "G=gi; ${G}t push origin main",
+    "T-ATK-27": "GH=gh; $GH pr merge 5",
+    "T-ATK-28": "$'\\x67it' push origin main",
+    "N-ATK-7": "/usr/bin/gi[t] push origin HEAD:main",
+    "row33-glob": "/usr/bin/gi[t] push origin main",
+    "row33-script": "bash ./push.sh",
+}
+
+
+@pytest.mark.parametrize("level", LEVEL_ORDER)
+@pytest.mark.parametrize(
+    "command",
+    [pytest.param(c, id=f"GAP-leak-R1-{k}") for k, c in ACCEPTED_LEAKS.items()],
+)
+def test_known_gaps_pinned(tmp_path, command, level):
+    _git_case(tmp_path, command, level, None)
+
+
+# T-COR-1 seed: rows of MR section 8.3/8.4 in its own layout (id, the class
+# shown at W, WA, F and FS or "allow", the command; <NL> is a newline). Tasks 16
+# and 17 append the rest of the corpus here; T-COR-2 (bare-remote replay) is
+# Task 16. Rows named in ACCEPTED_LEAKS are the R1 accepted leaks.
+CORPUS = r"""
+T-ATK-1    PUSH      PUSH      PUSH      PUSHFORM   git push origin a:b `echo c:main`
+T-ATK-2    PUSH      PUSH      PUSH      PUSHFORM   git push origin a:b \<NL>c:main
+T-ATK-3    PUSH      PUSH      PUSH      PUSHFORM   git-push origin main
+T-ATK-25   PUSH      PUSH      PUSH      PUSHFORM   GIT=git; $GIT push origin main
+T-ATK-26   allow     allow     allow     allow      G=gi; ${G}t push origin main
+T-ATK-27   allow     allow     allow     allow      GH=gh; $GH pr merge 5
+T-ATK-28   allow     allow     allow     allow      $'\x67it' push origin main
+T-ATK-55   TAMPER    TAMPER    TAMPER    TAMPER     cd ~/.claude && rm -rf state
+T-ATK-60   ESCAPE    ESCAPE    ESCAPE    ESCAPE     claude \<NL>-p x
+T-ATK-61   ESCAPE    ESCAPE    ESCAPE    ESCAPE     /usr/local/bin/claude --print x
+T-OK-1     allow     allow     allow     allow      git status
+T-OK-2     allow     allow     allow     allow      git diff
+T-OK-3     allow     allow     allow     allow      git log --oneline
+T-OVR-1    MERGE     MERGE     MERGE     MERGE      git log --grep merge
+N-ATK-1    UNKNOWN   UNKNOWN   UNKNOWN   UNKNOWN    gi\<NL>t push origin HEAD:main
+N-ATK-7    allow     allow     allow     allow      /usr/bin/gi[t] push origin HEAD:main
+"""
+CORPUS_IDS = {
+    "allow": None,
+    "PUSHFORM": "LL-PUSH-FORM",
+    "GHWRITE": "LL-GH-WRITE",
+}
+
+
+def _corpus_params():
+    for line in CORPUS.strip().splitlines():
+        row_id, *cells = line.split(None, 5)
+        command = cells.pop().replace("<NL>", "\n")
+        for level, cell in zip(LEVEL_ORDER, cells):
+            msg_id = CORPUS_IDS.get(cell, f"LL-{cell}")
+            yield pytest.param(command, level, msg_id, id=f"COR-{row_id}-{level}")
+
+
+@pytest.mark.parametrize("command, level, msg_id", list(_corpus_params()))
+def test_regression_corpus(tmp_path, command, level, msg_id):
+    # T-COR-1
+    _git_case(tmp_path, command, level, msg_id)

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
