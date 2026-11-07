9065b12b2e512906ff5ad68c1ceb5a6476e7accc
Review one task for spec compliance.

Task brief: ## Task 12: Register the guard on both events in hooks.json

Depends on: Task 11

Edit src/superclaude/hooks/hooks.json and plugins/superclaude/hooks/hooks.json (byte-identical to each other where they are today) as specified in design section 13 (FR-L-60 to FR-L-66): append to UserPromptSubmit one entry whose hook is the command ~/.claude/hooks/launch-level-guard.sh with timeout 5; append to PreToolUse one entry with the matcher regular expression printed in design section 13 and the same command and timeout. Existing entries, including Bash block-bare-python.sh and Bash launch-job-identity.sh, stay unchanged. Insert the new PreToolUse entry before the launch-job-identity.sh entry so that entry remains the last PreToolUse registration, which tests/cli/test_install_hooks.py (test_real_hooks_json_registers_launch_identity_without_replacing_policy) asserts. No UserPromptExpansion, SessionStart or onFailure registration is added.

Add tests to tests/cli/test_install_hooks.py (or a new tests/hooks/test_launch_level_guard_registration.py) that read both hooks.json files and assert: the guard appears exactly once under UserPromptSubmit and once under PreToolUse with timeout 5; the PreToolUse matcher equals the design string; no onFailure key; the Bash entries for block-bare-python.sh and launch-job-identity.sh are still present; the set of commands registered with the literal matcher Bash in tests/hooks/test_freshness_subagent_start_policy.py is unchanged (the guard's matcher is not the literal Bash).

Acceptance criteria:
- src/superclaude/hooks/hooks.json and plugins/superclaude/hooks/hooks.json both contain the two guard registrations and are identical to each other.
- uv run pytest tests/cli/test_install_hooks.py tests/hooks/test_freshness_subagent_start_policy.py -v passes without any edit to the existing launch-identity registration test.
- The new registration test compiles the PreToolUse matcher as a regular expression and asserts it matches the tool names Bash, Skill, Agent, Task, Edit, Write, NotebookEdit, Monitor, Workflow, RemoteTrigger, SendMessage, CronCreate, ScheduleWakeup and mcp__x__merge_pull_request, and does not match Read, Grep, Glob or TaskCreate.

AC ids (source order):
T12.AC1: src/superclaude/hooks/hooks.json and plugins/superclaude/hooks/hooks.json both contain the two guard registrations and are identical to each other.
T12.AC2: uv run pytest tests/cli/test_install_hooks.py tests/hooks/test_freshness_subagent_start_policy.py -v passes without any edit to the existing launch-identity registration test.
T12.AC3: The new registration test compiles the PreToolUse matcher as a regular expression and asserts it matches the tool names Bash, Skill, Agent, Task, Edit, Write, NotebookEdit, Monitor, Workflow, RemoteTrigger, SendMessage, CronCreate, ScheduleWakeup and mcp__x__merge_pull_request, and does not match Read, Grep, Glob or TaskCreate.
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
Start sha: 9065b12b2e512906ff5ad68c1ceb5a6476e7accc
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t12-test.log b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t12-test.log
new file mode 100644
index 00000000..997157e8
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t12-test.log
@@ -0,0 +1,14 @@
+$ uv run pytest tests/hooks/test_launch_level_guard_registration.py tests/cli/test_install_hooks.py tests/hooks/test_freshness_subagent_start_policy.py -q
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-394-launch-level-hook
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, anyio-4.16.0
+collected 53 items
+
+tests/hooks/test_launch_level_guard_registration.py ............         [ 22%]
+tests/cli/test_install_hooks.py ....................................     [ 90%]
+tests/hooks/test_freshness_subagent_start_policy.py .....                [100%]
+
+============================== 53 passed in 2.27s ==============================
diff --git a/plugins/superclaude/hooks/hooks.json b/plugins/superclaude/hooks/hooks.json
index b7cfbf13..11e8668d 100644
--- a/plugins/superclaude/hooks/hooks.json
+++ b/plugins/superclaude/hooks/hooks.json
@@ -40,6 +40,15 @@
             "timeout": 3
           }
         ]
+      },
+      {
+        "hooks": [
+          {
+            "type": "command",
+            "command": "~/.claude/hooks/launch-level-guard.sh",
+            "timeout": 5
+          }
+        ]
       }
     ],
     "PreToolUse": [
@@ -63,6 +72,16 @@
           }
         ]
       },
+      {
+        "matcher": "^(Bash|Skill|Agent|Task|Edit|Write|NotebookEdit|Monitor|Workflow|RemoteTrigger|SendMessage|Cron[A-Za-z]*|Schedule[A-Za-z]*)$|^mcp__.*(merge|push|commit|pull_request|create_or_update_file|delete_file|update_ref|create_ref|create_branch)",
+        "hooks": [
+          {
+            "type": "command",
+            "command": "~/.claude/hooks/launch-level-guard.sh",
+            "timeout": 5
+          }
+        ]
+      },
       {
         "matcher": "Bash",
         "hooks": [
diff --git a/src/superclaude/hooks/hooks.json b/src/superclaude/hooks/hooks.json
index d5562dc9..993e17cd 100644
--- a/src/superclaude/hooks/hooks.json
+++ b/src/superclaude/hooks/hooks.json
@@ -59,6 +59,15 @@
             "timeout": 5
           }
         ]
+      },
+      {
+        "hooks": [
+          {
+            "type": "command",
+            "command": "~/.claude/hooks/launch-level-guard.sh",
+            "timeout": 5
+          }
+        ]
       }
     ],
     "SessionEnd": [
@@ -93,6 +102,16 @@
           }
         ]
       },
+      {
+        "matcher": "^(Bash|Skill|Agent|Task|Edit|Write|NotebookEdit|Monitor|Workflow|RemoteTrigger|SendMessage|Cron[A-Za-z]*|Schedule[A-Za-z]*)$|^mcp__.*(merge|push|commit|pull_request|create_or_update_file|delete_file|update_ref|create_ref|create_branch)",
+        "hooks": [
+          {
+            "type": "command",
+            "command": "~/.claude/hooks/launch-level-guard.sh",
+            "timeout": 5
+          }
+        ]
+      },
       {
         "matcher": "Bash",
         "hooks": [
diff --git a/tests/hooks/test_launch_level_guard_registration.py b/tests/hooks/test_launch_level_guard_registration.py
new file mode 100644
index 00000000..0dc12a7b
--- /dev/null
+++ b/tests/hooks/test_launch_level_guard_registration.py
@@ -0,0 +1,126 @@
+"""Registration of the launch-level guard in both hooks.json files (issue #394, Task 12).
+
+The guard is registered once on UserPromptSubmit and once on PreToolUse, each with a
+5 second timeout, and no onFailure key. The PreToolUse matcher is the string printed in
+design section 13. The launch-job-identity.sh registration stays the last PreToolUse entry.
+"""
+
+from __future__ import annotations
+
+import json
+import re
+from pathlib import Path
+
+import pytest
+
+ROOT = Path(__file__).resolve().parents[2]
+FILES = {
+    "src": ROOT / "src/superclaude/hooks/hooks.json",
+    "plugin": ROOT / "plugins/superclaude/hooks/hooks.json",
+}
+GUARD = "~/.claude/hooks/launch-level-guard.sh"
+DESIGN = ROOT / "docs/designs/sc-issue-launch-level-hook.md"
+
+
+def _hooks(name: str) -> dict:
+    return json.loads(FILES[name].read_text(encoding="utf-8"))["hooks"]
+
+
+def _guard_entries(hooks: dict, event: str) -> list[dict]:
+    return [
+        registration
+        for registration in hooks[event]
+        if any(h["command"] == GUARD for h in registration["hooks"])
+    ]
+
+
+def _design_matcher() -> str:
+    section = DESIGN.read_text(encoding="utf-8").split(
+        "## 13. Registration, install and claim-feature interface requests"
+    )[1]
+    return re.search(r'"matcher": "([^"]+)"', section).group(1)
+
+
+@pytest.mark.parametrize("name", sorted(FILES))
+def test_guard_registered_once_on_each_event_with_timeout_5(name):
+    hooks = _hooks(name)
+    for event in ("UserPromptSubmit", "PreToolUse"):
+        entries = _guard_entries(hooks, event)
+        assert len(entries) == 1, (name, event)
+        assert [h["timeout"] for h in entries[0]["hooks"]] == [5]
+    assert "matcher" not in _guard_entries(hooks, "UserPromptSubmit")[0]
+
+
+@pytest.mark.parametrize("name", sorted(FILES))
+def test_guard_is_not_registered_on_other_events(name):
+    hooks = _hooks(name)
+    for event, registrations in hooks.items():
+        if event in ("UserPromptSubmit", "PreToolUse"):
+            continue
+        assert not _guard_entries(hooks, event), (name, event)
+
+
+@pytest.mark.parametrize("name", sorted(FILES))
+def test_no_on_failure_key_anywhere(name):
+    assert "onFailure" not in FILES[name].read_text(encoding="utf-8")
+
+
+def test_pretooluse_matcher_equals_the_design_string():
+    expected = _design_matcher()
+    for name in FILES:
+        assert _guard_entries(_hooks(name), "PreToolUse")[0]["matcher"] == expected
+
+
+@pytest.mark.parametrize("name", sorted(FILES))
+def test_matcher_matches_the_guarded_tools_and_not_the_others(name):
+    matcher = re.compile(_guard_entries(_hooks(name), "PreToolUse")[0]["matcher"])
+    for tool in (
+        "Bash",
+        "Skill",
+        "Agent",
+        "Task",
+        "Edit",
+        "Write",
+        "NotebookEdit",
+        "Monitor",
+        "Workflow",
+        "RemoteTrigger",
+        "SendMessage",
+        "CronCreate",
+        "ScheduleWakeup",
+        "mcp__x__merge_pull_request",
+    ):
+        assert matcher.search(tool), tool
+    for tool in ("Read", "Grep", "Glob", "TaskCreate"):
+        assert not matcher.search(tool), tool
+
+
+@pytest.mark.parametrize("name", sorted(FILES))
+def test_existing_bash_registrations_stay_and_identity_hook_stays_last(name):
+    pre_tool = _hooks(name)["PreToolUse"]
+    commands = {
+        hook["command"]
+        for registration in pre_tool
+        if registration.get("matcher") == "Bash"
+        for hook in registration["hooks"]
+    }
+    assert commands == {
+        "~/.claude/hooks/block-bare-python.sh",
+        "~/.claude/hooks/launch-job-identity.sh",
+    }
+    assert (
+        pre_tool[-1]["hooks"][0]["command"] == "~/.claude/hooks/launch-job-identity.sh"
+    )
+    assert (
+        pre_tool.index(_guard_entries(_hooks(name), "PreToolUse")[0])
+        == len(pre_tool) - 2
+    )
+
+
+def test_guard_registrations_are_the_same_in_both_trees():
+    # The two files differ in other, older entries (the plugin copy is a subset);
+    # only the guard entries must be identical.
+    for event in ("UserPromptSubmit", "PreToolUse"):
+        assert _guard_entries(_hooks("src"), event) == _guard_entries(
+            _hooks("plugin"), event
+        )

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
