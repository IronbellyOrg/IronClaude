2912b48a697fa9d54be994797c7af6d1262ebe85
Review one task for spec compliance.

Task brief: ## Task 2: Add the observation fixtures, the log-only probe and the pending-observation tests

Depends on: Task 1

Create tests/hooks/fixtures/launch_level/ob_h1/ with one fixture file per OB-H1 item of design section 11, named item<n>-<shape>.json (DD-6): item 1 subagent and nested-subagent session_id, agent_id, agent_type; item 2 Skill input keys and name form; item 3 Agent name and isolation; item 4 a typed /sc:implement prompt; item 5 a Monitor line "approved" and background Bash and background subagent notices; item 6 TaskCreate against the anchored matcher; item 7 SendMessage and MCP names; item 8 claude without -p; item 9 Bash, Edit, Write and Skill tool names. Each is a synthetic payload in the documented hook input shape (top-level hook_event_name, session_id, tool_name, tool_input). Add tests/hooks/fixtures/launch_level/ob_h1/README.md saying every fixture is synthetic and listing, per item, what a real observation must capture.

Reuse the existing opt-in probe tests/hooks/fixtures/launch_level/live_probe.py where it already captures an item, and do not duplicate it. Create tests/hooks/fixtures/launch_level/ob_h1/log-only-probe.sh: a bash script that appends the stdin JSON as one line to the file named by the LAUNCH_LEVEL_PROBE_LOG environment variable and always exits 0, so it can be registered by a person for a real observation without ever blocking.

Create tests/hooks/test_launch_level_observations.py containing: real tests that the probe appends exactly one line per call, exits 0 when the log path is unwritable or unset, and never writes to stdout; and one skipped test per pending observation (OB-H1 items 1 to 9, OB-H2, OB-H3, OB-CTX) whose skip reason names the item and says it needs a real governed session and has not been run.

Acceptance criteria:
- tests/hooks/fixtures/launch_level/ob_h1/ holds nine item<n>-<shape>.json files that parse as JSON objects with a string hook_event_name, plus README.md and log-only-probe.sh (executable).
- uv run pytest tests/hooks/test_launch_level_observations.py -v shows the probe tests passing and exactly twelve skipped tests (nine OB-H1 items, OB-H2, OB-H3, OB-CTX), each with a reason that contains the item name.
- Running the probe with LAUNCH_LEVEL_PROBE_LOG unset prints nothing and exits 0.

AC ids (source order):
T2.AC1: tests/hooks/fixtures/launch_level/ob_h1/ holds nine item<n>-<shape>.json files that parse as JSON objects with a string hook_event_name, plus README.md and log-only-probe.sh (executable).
T2.AC2: uv run pytest tests/hooks/test_launch_level_observations.py -v shows the probe tests passing and exactly twelve skipped tests (nine OB-H1 items, OB-H2, OB-H3, OB-CTX), each with a reason that contains the item name.
T2.AC3: Running the probe with LAUNCH_LEVEL_PROBE_LOG unset prints nothing and exits 0.
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
Start sha: 2912b48a697fa9d54be994797c7af6d1262ebe85
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t2-test.log b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t2-test.log
new file mode 100644
index 00000000..b2bd6e09
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t2-test.log
@@ -0,0 +1,40 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0 -- /home/coder/workspaces/worktrees/IronClaude/issue-394-launch-level-hook/.venv/bin/python
+SuperClaude: 5.0.0
+rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-394-launch-level-hook
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, anyio-4.16.0
+collecting ... collected 17 items
+
+tests/hooks/test_launch_level_observations.py::test_fixtures_are_nine_json_objects_with_an_event_name PASSED [  5%]
+tests/hooks/test_launch_level_observations.py::test_probe_appends_exactly_one_line_per_call PASSED [ 11%]
+tests/hooks/test_launch_level_observations.py::test_probe_flattens_a_multiline_payload_to_one_line PASSED [ 17%]
+tests/hooks/test_launch_level_observations.py::test_probe_with_log_path_unset_prints_nothing_and_exits_zero PASSED [ 23%]
+tests/hooks/test_launch_level_observations.py::test_probe_with_unwritable_log_path_exits_zero_silently PASSED [ 29%]
+tests/hooks/test_launch_level_observations.py::test_pending_live_observation[OB-H1 item 1] SKIPPED [ 35%]
+tests/hooks/test_launch_level_observations.py::test_pending_live_observation[OB-H1 item 2] SKIPPED [ 41%]
+tests/hooks/test_launch_level_observations.py::test_pending_live_observation[OB-H1 item 3] SKIPPED [ 47%]
+tests/hooks/test_launch_level_observations.py::test_pending_live_observation[OB-H1 item 4] SKIPPED [ 52%]
+tests/hooks/test_launch_level_observations.py::test_pending_live_observation[OB-H1 item 5] SKIPPED [ 58%]
+tests/hooks/test_launch_level_observations.py::test_pending_live_observation[OB-H1 item 6] SKIPPED [ 64%]
+tests/hooks/test_launch_level_observations.py::test_pending_live_observation[OB-H1 item 7] SKIPPED [ 70%]
+tests/hooks/test_launch_level_observations.py::test_pending_live_observation[OB-H1 item 8] SKIPPED [ 76%]
+tests/hooks/test_launch_level_observations.py::test_pending_live_observation[OB-H1 item 9] SKIPPED [ 82%]
+tests/hooks/test_launch_level_observations.py::test_pending_live_observation[OB-H2] SKIPPED [ 88%]
+tests/hooks/test_launch_level_observations.py::test_pending_live_observation[OB-H3] SKIPPED [ 94%]
+tests/hooks/test_launch_level_observations.py::test_pending_live_observation[OB-CTX] SKIPPED [100%]
+
+=========================== short test summary info ============================
+SKIPPED [1] tests/hooks/test_launch_level_observations.py:84: OB-H1 item 1: needs a real governed session and has not been run
+SKIPPED [1] tests/hooks/test_launch_level_observations.py:84: OB-H1 item 2: needs a real governed session and has not been run
+SKIPPED [1] tests/hooks/test_launch_level_observations.py:84: OB-H1 item 3: needs a real governed session and has not been run
+SKIPPED [1] tests/hooks/test_launch_level_observations.py:84: OB-H1 item 4: needs a real governed session and has not been run
+SKIPPED [1] tests/hooks/test_launch_level_observations.py:84: OB-H1 item 5: needs a real governed session and has not been run
+SKIPPED [1] tests/hooks/test_launch_level_observations.py:84: OB-H1 item 6: needs a real governed session and has not been run
+SKIPPED [1] tests/hooks/test_launch_level_observations.py:84: OB-H1 item 7: needs a real governed session and has not been run
+SKIPPED [1] tests/hooks/test_launch_level_observations.py:84: OB-H1 item 8: needs a real governed session and has not been run
+SKIPPED [1] tests/hooks/test_launch_level_observations.py:84: OB-H1 item 9: needs a real governed session and has not been run
+SKIPPED [1] tests/hooks/test_launch_level_observations.py:84: OB-H2: needs a real governed session and has not been run
+SKIPPED [1] tests/hooks/test_launch_level_observations.py:84: OB-H3: needs a real governed session and has not been run
+SKIPPED [1] tests/hooks/test_launch_level_observations.py:84: OB-CTX: needs a real governed session and has not been run
+======================== 5 passed, 12 skipped in 0.08s =========================
diff --git a/tests/hooks/fixtures/launch_level/ob_h1/README.md b/tests/hooks/fixtures/launch_level/ob_h1/README.md
new file mode 100644
index 00000000..e08cdbfd
--- /dev/null
+++ b/tests/hooks/fixtures/launch_level/ob_h1/README.md
@@ -0,0 +1,19 @@
+# OB-H1 fixtures (synthetic)
+
+Every file in this folder is a synthetic hook payload in the documented input shape (top-level `hook_event_name`, `session_id`, and `tool_name` plus `tool_input`, or `prompt` for a prompt event). None of them was captured from a real session. They exist so tests can load a payload by item, and they are not evidence that any observation has been made.
+
+`log-only-probe.sh` is the hook a person registers for a real observation. It appends each hook input as one line to the file named by `LAUNCH_LEVEL_PROBE_LOG`, always exits 0 and never blocks. The existing opt-in probe `../live_probe.py` is reused for what it already records from an actual hook input (`session_id`, `agent_id`, `agent_type`, the top-level and `tool_input` key names and `run_in_background`), plus job-identity selector results. It runs one Bash call with only the Bash tool enabled, and it records the tool name only as `Bash` or `other`. So it can show the ids of item 1 for that one call, and it cannot show a Skill, Agent, Task, SendMessage or MCP call (items 2, 3, 6, 7, 9), a typed prompt or notice (items 4, 5) or a `claude` command (item 8). `log-only-probe.sh` is the way to capture those.
+
+What a real observation must capture, per item (design section 11, OB-H1):
+
+| Item | File | A real observation must capture |
+|---|---|---|
+| 1 | item1-subagent-ids.json | `session_id`, `agent_id` and `agent_type` of a subagent call and of a nested-subagent call (does the parent's `session_id` appear?) |
+| 2 | item2-skill-keys.json | the input keys of a Skill call and the form of the skill name (`skill` or `name`, with or without `sc:`) |
+| 3 | item3-agent-isolation.json | the tool name for an Agent or Task call and the `isolation` key |
+| 4 | item4-typed-implement-prompt.json | the exact prompt of a typed `/sc:implement x`, and whether the prompt event runs before expansion |
+| 5 | item5-monitor-approved-line.json | the exact prompt of a Monitor line `approved` and of background-Bash and background-subagent notices |
+| 6 | item6-taskcreate.json | whether `TaskCreate` matches the anchored tool matcher |
+| 7 | item7-sendmessage-mcp.json | the tool names of SendMessage and of MCP tools |
+| 8 | item8-claude-no-p.json | a `claude` command without `-p` |
+| 9 | item9-tool-names.json | the tool names of Bash, Edit, Write and Skill |
diff --git a/tests/hooks/fixtures/launch_level/ob_h1/item1-subagent-ids.json b/tests/hooks/fixtures/launch_level/ob_h1/item1-subagent-ids.json
new file mode 100644
index 00000000..b64ac700
--- /dev/null
+++ b/tests/hooks/fixtures/launch_level/ob_h1/item1-subagent-ids.json
@@ -0,0 +1 @@
+{"hook_event_name": "PreToolUse", "session_id": "parent-session-0001", "agent_id": "subagent-0001", "agent_type": "general-purpose", "tool_name": "Bash", "tool_input": {"command": "git status"}}
diff --git a/tests/hooks/fixtures/launch_level/ob_h1/item2-skill-keys.json b/tests/hooks/fixtures/launch_level/ob_h1/item2-skill-keys.json
new file mode 100644
index 00000000..3da837bc
--- /dev/null
+++ b/tests/hooks/fixtures/launch_level/ob_h1/item2-skill-keys.json
@@ -0,0 +1 @@
+{"hook_event_name": "PreToolUse", "session_id": "parent-session-0001", "tool_name": "Skill", "tool_input": {"skill": "sc:implement", "args": "plan.md"}}
diff --git a/tests/hooks/fixtures/launch_level/ob_h1/item3-agent-isolation.json b/tests/hooks/fixtures/launch_level/ob_h1/item3-agent-isolation.json
new file mode 100644
index 00000000..e1cb0f24
--- /dev/null
+++ b/tests/hooks/fixtures/launch_level/ob_h1/item3-agent-isolation.json
@@ -0,0 +1 @@
+{"hook_event_name": "PreToolUse", "session_id": "parent-session-0001", "tool_name": "Agent", "tool_input": {"subagent_type": "general-purpose", "description": "probe", "prompt": "probe", "isolation": "remote"}}
diff --git a/tests/hooks/fixtures/launch_level/ob_h1/item4-typed-implement-prompt.json b/tests/hooks/fixtures/launch_level/ob_h1/item4-typed-implement-prompt.json
new file mode 100644
index 00000000..28c387d7
--- /dev/null
+++ b/tests/hooks/fixtures/launch_level/ob_h1/item4-typed-implement-prompt.json
@@ -0,0 +1 @@
+{"hook_event_name": "UserPromptSubmit", "session_id": "parent-session-0001", "prompt": "/sc:implement x"}
diff --git a/tests/hooks/fixtures/launch_level/ob_h1/item5-monitor-approved-line.json b/tests/hooks/fixtures/launch_level/ob_h1/item5-monitor-approved-line.json
new file mode 100644
index 00000000..e48b8104
--- /dev/null
+++ b/tests/hooks/fixtures/launch_level/ob_h1/item5-monitor-approved-line.json
@@ -0,0 +1 @@
+{"hook_event_name": "UserPromptSubmit", "session_id": "parent-session-0001", "prompt": "approved"}
diff --git a/tests/hooks/fixtures/launch_level/ob_h1/item6-taskcreate.json b/tests/hooks/fixtures/launch_level/ob_h1/item6-taskcreate.json
new file mode 100644
index 00000000..08c87be4
--- /dev/null
+++ b/tests/hooks/fixtures/launch_level/ob_h1/item6-taskcreate.json
@@ -0,0 +1 @@
+{"hook_event_name": "PreToolUse", "session_id": "parent-session-0001", "tool_name": "TaskCreate", "tool_input": {"subject": "probe"}}
diff --git a/tests/hooks/fixtures/launch_level/ob_h1/item7-sendmessage-mcp.json b/tests/hooks/fixtures/launch_level/ob_h1/item7-sendmessage-mcp.json
new file mode 100644
index 00000000..2262571e
--- /dev/null
+++ b/tests/hooks/fixtures/launch_level/ob_h1/item7-sendmessage-mcp.json
@@ -0,0 +1 @@
+{"hook_event_name": "PreToolUse", "session_id": "parent-session-0001", "tool_name": "mcp__github__merge_pull_request", "tool_input": {"pull_number": 1}}
diff --git a/tests/hooks/fixtures/launch_level/ob_h1/item8-claude-no-p.json b/tests/hooks/fixtures/launch_level/ob_h1/item8-claude-no-p.json
new file mode 100644
index 00000000..2de6b4a5
--- /dev/null
+++ b/tests/hooks/fixtures/launch_level/ob_h1/item8-claude-no-p.json
@@ -0,0 +1 @@
+{"hook_event_name": "PreToolUse", "session_id": "parent-session-0001", "tool_name": "Bash", "tool_input": {"command": "claude --dangerously-skip-permissions"}}
diff --git a/tests/hooks/fixtures/launch_level/ob_h1/item9-tool-names.json b/tests/hooks/fixtures/launch_level/ob_h1/item9-tool-names.json
new file mode 100644
index 00000000..19392ac8
--- /dev/null
+++ b/tests/hooks/fixtures/launch_level/ob_h1/item9-tool-names.json
@@ -0,0 +1 @@
+{"hook_event_name": "PreToolUse", "session_id": "parent-session-0001", "tool_name": "Edit", "tool_input": {"file_path": "/tmp/probe.txt", "old_string": "a", "new_string": "b"}}
diff --git a/tests/hooks/fixtures/launch_level/ob_h1/log-only-probe.sh b/tests/hooks/fixtures/launch_level/ob_h1/log-only-probe.sh
new file mode 100755
index 00000000..72ed9cdc
--- /dev/null
+++ b/tests/hooks/fixtures/launch_level/ob_h1/log-only-probe.sh
@@ -0,0 +1,12 @@
+#!/bin/bash
+# Log-only probe for a real observation (OB-H1, OB-H2, OB-H3, OB-CTX): appends the hook input as one line to the
+# file named by LAUNCH_LEVEL_PROBE_LOG and always exits 0. It never blocks, never writes to stdout or stderr.
+input=$(cat 2>/dev/null) || exit 0
+[[ -n ${LAUNCH_LEVEL_PROBE_LOG:-} ]] || exit 0
+if command -v jq >/dev/null 2>&1 && line=$(printf '%s' "$input" | jq -c . 2>/dev/null) && [[ -n $line ]]; then
+    :
+else
+    line=$(printf '%s' "$input" | tr '\n' ' ')
+fi
+{ printf '%s\n' "$line" >> "$LAUNCH_LEVEL_PROBE_LOG"; } 2>/dev/null
+exit 0
diff --git a/tests/hooks/test_launch_level_observations.py b/tests/hooks/test_launch_level_observations.py
new file mode 100644
index 00000000..5077c5eb
--- /dev/null
+++ b/tests/hooks/test_launch_level_observations.py
@@ -0,0 +1,84 @@
+"""Pending live observations for the launch-level hook (issue #394), and tests of the log-only probe.
+
+The observations need a real governed session and have not been run: each is a skipped test with a reason.
+The synthetic payloads in fixtures/launch_level/ob_h1 are not observations.
+"""
+
+from __future__ import annotations
+
+import json
+import os
+import shutil
+import subprocess
+from pathlib import Path
+
+import pytest
+
+FIXTURES = Path(__file__).resolve().parent / "fixtures" / "launch_level" / "ob_h1"
+PROBE = FIXTURES / "log-only-probe.sh"
+BASH = shutil.which("bash") or "/bin/bash"
+
+
+def _run_probe(payload: bytes, log: str | None, tmp_path: Path):
+    env = {k: v for k, v in os.environ.items() if k != "LAUNCH_LEVEL_PROBE_LOG"}
+    env["HOME"] = str(tmp_path)
+    if log is not None:
+        env["LAUNCH_LEVEL_PROBE_LOG"] = log
+    return subprocess.run(
+        [BASH, str(PROBE)], input=payload, capture_output=True, env=env, timeout=10
+    )
+
+
+def test_fixtures_are_nine_json_objects_with_an_event_name():
+    files = sorted(FIXTURES.glob("item[1-9]-*.json"))
+    assert [f.name[4] for f in files] == list("123456789")
+    for f in files:
+        data = json.loads(f.read_text())
+        assert isinstance(data, dict) and isinstance(data["hook_event_name"], str), (
+            f.name
+        )
+    assert (FIXTURES / "README.md").is_file()
+    assert os.access(PROBE, os.X_OK)
+
+
+def test_probe_appends_exactly_one_line_per_call(tmp_path):
+    log = tmp_path / "probe.log"
+    payload = (FIXTURES / "item2-skill-keys.json").read_bytes()
+    for count in (1, 2):
+        result = _run_probe(payload, str(log), tmp_path)
+        assert result.returncode == 0
+        assert result.stdout == b"" and result.stderr == b""
+        lines = log.read_text().splitlines()
+        assert len(lines) == count
+    assert json.loads(lines[-1])["tool_name"] == "Skill"
+
+
+def test_probe_flattens_a_multiline_payload_to_one_line(tmp_path):
+    log = tmp_path / "probe.log"
+    pretty = json.dumps(
+        {"hook_event_name": "PreToolUse", "session_id": "s"}, indent=2
+    ).encode()
+    assert _run_probe(pretty, str(log), tmp_path).returncode == 0
+    assert len(log.read_text().splitlines()) == 1
+
+
+def test_probe_with_log_path_unset_prints_nothing_and_exits_zero(tmp_path):
+    result = _run_probe(b'{"hook_event_name": "PreToolUse"}', None, tmp_path)
+    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
+    assert list(tmp_path.iterdir()) == []
+
+
+def test_probe_with_unwritable_log_path_exits_zero_silently(tmp_path):
+    target_dir = tmp_path / "a-directory"
+    target_dir.mkdir()
+    for bad in (str(target_dir), str(tmp_path / "missing" / "dir" / "probe.log")):
+        result = _run_probe(b'{"hook_event_name": "PreToolUse"}', bad, tmp_path)
+        assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
+
+
+_PENDING = [f"OB-H1 item {n}" for n in range(1, 10)] + ["OB-H2", "OB-H3", "OB-CTX"]
+
+
+@pytest.mark.parametrize("item", _PENDING)
+def test_pending_live_observation(item):
+    pytest.skip(f"{item}: needs a real governed session and has not been run")

Delta diff from the previous reviewed tree (empty on the first review): diff --git a/tests/hooks/fixtures/launch_level/ob_h1/README.md b/tests/hooks/fixtures/launch_level/ob_h1/README.md
index 8ddddbd6..e08cdbfd 100644
--- a/tests/hooks/fixtures/launch_level/ob_h1/README.md
+++ b/tests/hooks/fixtures/launch_level/ob_h1/README.md
@@ -2,7 +2,7 @@
 
 Every file in this folder is a synthetic hook payload in the documented input shape (top-level `hook_event_name`, `session_id`, and `tool_name` plus `tool_input`, or `prompt` for a prompt event). None of them was captured from a real session. They exist so tests can load a payload by item, and they are not evidence that any observation has been made.
 
-`log-only-probe.sh` is the hook a person registers for a real observation. It appends each hook input as one line to the file named by `LAUNCH_LEVEL_PROBE_LOG`, always exits 0 and never blocks. The existing opt-in probe `../live_probe.py` captures job-identity selector results only; it does not capture the items below, so the two do not overlap.
+`log-only-probe.sh` is the hook a person registers for a real observation. It appends each hook input as one line to the file named by `LAUNCH_LEVEL_PROBE_LOG`, always exits 0 and never blocks. The existing opt-in probe `../live_probe.py` is reused for what it already records from an actual hook input (`session_id`, `agent_id`, `agent_type`, the top-level and `tool_input` key names and `run_in_background`), plus job-identity selector results. It runs one Bash call with only the Bash tool enabled, and it records the tool name only as `Bash` or `other`. So it can show the ids of item 1 for that one call, and it cannot show a Skill, Agent, Task, SendMessage or MCP call (items 2, 3, 6, 7, 9), a typed prompt or notice (items 4, 5) or a `claude` command (item 8). `log-only-probe.sh` is the way to capture those.
 
 What a real observation must capture, per item (design section 11, OB-H1):
 

Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B2 ac=scope at=tests/hooks/fixtures/launch_level/ob_h1/README.md:5 anchor=tests/hooks/fixtures/launch_level/live_probe.py:63-77 chk=n,y,n,n family=readme-live-probe-claim fix=reword README line 5 to say what live_probe.py records and what it cannot capture first=A1 origin=new: README says live_probe.py captures selector results only and does not overlap the items, but live_probe.py:63-77 records session_id, agent_id, agent_type, tool_name and tool_input_keys from the actual hook input.

Saved-probe re-check hit locations (may be empty): 5:`log-only-probe.sh` is the hook a person registers for a real observation. It appends each hook input as one line to the file named by `LAUNCH_LEVEL_PROBE_LOG`, always exits 0 and never blocks. The existing opt-in probe `../live_probe.py` is reused for what it already records from an actual hook input (`session_id`, `agent_id`, `agent_type`, the top-level and `tool_input` key names and `run_in_background`), plus job-identity selector results. It runs one Bash call with only the Bash tool enabled, and it records the tool name only as `Bash` or `other`. So it can show the ids of item 1 for that one call, and it cannot show a Skill, Agent, Task, SendMessage or MCP call (items 2, 3, 6, 7, 9), a typed prompt or notice (items 4, 5) or a `claude` command (item 8). `log-only-probe.sh` is the way to capture those.


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
