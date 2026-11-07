e2250e78e573be9d957db38a9e3a8bb972e13265
Review one task for spec compliance.

Task brief: ## Task 14: Test the guard together with the job identity hook

Depends on: Task 13

Create tests/hooks/test_launch_level_guard_with_identity.py and ./artifacts/hook-order.md (finding F3). The test runs src/superclaude/hooks/scripts/launch-level-guard.sh and src/superclaude/hooks/scripts/launch-job-identity.sh against the same PreToolUse Bash payload with a temporary HOME and the UV environment used by tests/hooks/test_launch_job_identity.py (UV_PYTHON set to sys.executable, UV_PYTHON_DOWNLOADS never). Cases: a governed session at full-submit with an allowed command (guard exit 0, identity output rewrites only the command through updatedInput, and the guard saw the original command); a governed session at worktree with a blocked command (guard exit 2 with the block message; the identity output is recorded but irrelevant to the decision); an ordinary session (both silent); a session whose file holds the word degraded (record what the identity hook does with a word outside its supported worktree, full and full-submit set, and what the guard does). ./artifacts/hook-order.md records the observed results, states that the order in which Claude Code runs two matching PreToolUse hooks and how it combines a block with an updatedInput is not observed here (it needs a live session, listed as pending in tests/hooks/test_launch_level_observations.py), and records any mismatch found for the degraded word with a one-sentence proposed resolution. Do not edit launch-job-identity.sh. Do not assert a fixed position of the guard in an installed settings.json: on an upgrade the installer appends a new registration at the end, so only a fresh install matches the shipped hooks.json order.

Acceptance criteria:
- uv run pytest tests/hooks/test_launch_level_guard_with_identity.py -v passes for the four cases.
- ./artifacts/hook-order.md exists, lists the four observed outcomes, and says explicitly that hook ordering is unobserved.
- If the identity hook treats degraded as unsupported, the record says so and the guard's own handling of degraded (level worktree with the LL-STATE note) is asserted by a test.

AC ids (source order):
T14.AC1: uv run pytest tests/hooks/test_launch_level_guard_with_identity.py -v passes for the four cases.
T14.AC2: ./artifacts/hook-order.md exists, lists the four observed outcomes, and says explicitly that hook ordering is unobserved.
T14.AC3: If the identity hook treats degraded as unsupported, the record says so and the guard's own handling of degraded (level worktree with the LL-STATE note) is asserted by a test.
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
Start sha: e2250e78e573be9d957db38a9e3a8bb972e13265
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/hook-order.md b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/hook-order.md
new file mode 100644
index 00000000..a3bafd69
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/hook-order.md
@@ -0,0 +1,69 @@
+# Task 14: the guard and the job identity hook on the same payload (finding F3)
+
+Test: `tests/hooks/test_launch_level_guard_with_identity.py` (6 passed, log `t14-test.log`).
+Each case runs `src/superclaude/hooks/scripts/launch-level-guard.sh` and
+`src/superclaude/hooks/scripts/launch-job-identity.sh` one after the other on the
+same PreToolUse Bash payload, with a temporary HOME, `CLAUDE_CONFIG_DIR` unset, a
+PATH holding only a temporary bin directory (cat, sed, tr, mkdir, mv, ln, rm, jq,
+uv), `UV_PYTHON` set to the test interpreter and `UV_PYTHON_DOWNLOADS=never`. The
+real `~/.claude` is never read or written. Both hooks read the same store:
+`$HOME/.claude/state/launch-level/sessions/<session_id>`.
+
+## Observed results of the four cases
+
+| Case | Session file | Command | Guard | Identity hook |
+|---|---|---|---|---|
+| 1 | `full-submit` | `git status` | exit 0, silent | exit 0; `updatedInput` equal to `tool_input` except `command`, which becomes `/bin/bash <script> execute <sid> <tool_use_id> 'git status'`; no `permissionDecision` |
+| 2 | `worktree` | `git commit -m wip` | exit 2, header "level worktree", "Blocked: creating a commit", no LL-STATE note | exit 0 with the same kind of rewrite (recorded; not part of the decision, the guard's exit 2 blocks) |
+| 3 | none for this id (another session bound) | `git commit -m wip` | exit 0, silent | exit 0, silent |
+| 4 | `degraded` (with and without a trailing newline) | `git commit -m wip` | exit 2, header "level worktree", "Blocked: creating a commit", LL-STATE note | exit 2, stdout empty, stderr `launch job: governed Bash call cannot be wrapped safely` |
+| 4 | `degraded` | `git status` | exit 0, silent | exit 2, same message |
+
+Case 1 also checks that the guard decides on the original command. An extra test
+copies the identity script to `$HOME/.claude/hooks/launch-job-identity.sh`, where
+the installer puts it. Its rewrite then names that real path. Fed that rewrite,
+the guard blocks `git status` at full-submit as LL-TAMPER ("touching the
+launch-level state ...") because the text contains `.claude/hooks`. So the
+composition works only if Claude Code gives the guard the original input, not
+the identity hook's `updatedInput`.
+
+## Not observed here
+
+The order in which Claude Code runs two matching PreToolUse hooks is not
+observed. Neither is whether one hook's `updatedInput` reaches a later hook, or
+how Claude Code combines one hook's block (exit 2) with another hook's
+`updatedInput`. These tests run the scripts directly, not inside Claude Code.
+Finding the answer needs a live governed session. The pending live observations
+in `tests/hooks/test_launch_level_observations.py` (OB-H1 items 1 to 9, OB-H2,
+OB-H3, OB-CTX) are skipped tests that have not been run. None of them names hook
+ordering explicitly, so this check should be added to OB-H3 (live sessions at
+each level). The identity hook's own text also says "concurrent hook rewrite
+ordering ... unverified".
+
+Registration order for the record: since Task 13 the installer inserts a missing
+guard registration before the launch-job-identity registration on an upgrade.
+On a fresh install and on an upgrade the guard therefore comes before the
+identity hook in PreToolUse, as in the shipped `hooks.json`. The test does not
+assert any position in an installed `settings.json`, and a position in the file
+does not prove the order of execution.
+
+## The degraded word
+
+- **Identity hook:** its supported set is `LEVELS = {worktree, full, full-submit}`,
+  with one optional trailing newline. Any other word in an existing session file,
+  `degraded` included, fails `governed()`. In hook mode that prints
+  `launch job: governed Bash call cannot be wrapped safely` and exits 2 for
+  every Bash call of that session. It never treats the session as ordinary.
+- **Guard:** any word other than the three is level worktree with the LL-STATE
+  note. Allowed calls stay silent, and blocked calls show the note. Asserted by
+  `test_degraded_word_guard_worktree_with_state_note_identity_blocks_all`.
+- **Mismatch found:** the guard writes `degraded` itself (binding rules B11 and
+  B12: a used or missing nonce with a leading marker, and a bad taken record),
+  and treats it as worktree. The identity hook blocks every Bash call of such a
+  session, including read-only ones like `git status` that the guard allows. A
+  degraded session therefore cannot run Bash at all, which is stricter than
+  design section 9 describes. It fails closed, so it is not a safety gap.
+- **Proposed resolution:** in a separate change to `launch-job-identity.sh` (not
+  made here, per the plan's constraint), add `degraded` to its `LEVELS` so a
+  degraded session is wrapped and identified as governed like a worktree session,
+  and leave its strictness to the guard.
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t14-test.log b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t14-test.log
new file mode 100644
index 00000000..f4da47a2
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t14-test.log
@@ -0,0 +1,11 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-394-launch-level-hook
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, anyio-4.16.0
+collected 6 items
+
+tests/hooks/test_launch_level_guard_with_identity.py ......              [100%]
+
+============================== 6 passed in 1.08s ===============================
diff --git a/tests/hooks/test_launch_level_guard_with_identity.py b/tests/hooks/test_launch_level_guard_with_identity.py
new file mode 100644
index 00000000..3264ed85
--- /dev/null
+++ b/tests/hooks/test_launch_level_guard_with_identity.py
@@ -0,0 +1,212 @@
+"""The launch-level guard and the job identity hook on the same PreToolUse payload (plan Task 14, F3).
+
+Each case runs src/superclaude/hooks/scripts/launch-level-guard.sh and
+src/superclaude/hooks/scripts/launch-job-identity.sh one after the other on the
+same Bash payload, with HOME inside tmp_path, CLAUDE_CONFIG_DIR unset, a PATH
+holding only a temporary bin directory, and the UV environment of
+tests/hooks/test_launch_job_identity.py (UV_PYTHON set to sys.executable,
+UV_PYTHON_DOWNLOADS never). Both hooks read the same store,
+~/.claude/state/launch-level/sessions/<session_id>.
+
+Not observed here: the order in which Claude Code runs two matching PreToolUse
+hooks and how it combines a block with an updatedInput. That needs a live
+session (see artifacts/hook-order.md of the plan package).
+"""
+
+from __future__ import annotations
+
+import json
+import os
+import shlex
+import shutil
+import subprocess
+import sys
+from pathlib import Path
+
+import pytest
+
+ROOT = Path(__file__).resolve().parents[2]
+SCRIPTS = ROOT / "src" / "superclaude" / "hooks" / "scripts"
+GUARD = SCRIPTS / "launch-level-guard.sh"
+IDENTITY = SCRIPTS / "launch-job-identity.sh"
+BASH = "/bin/bash"
+SID = "sess-abc_123"
+TOOL_ID = "toolu_01ABC123"
+HEADER = "Launch-level guard: this session was started by /sc:issue --claim at level {level}."
+STATE_NOTE = (
+    "Note: the launch record was invalid or unreadable, so the strictest level "
+    "(worktree) applies."
+)
+IDENTITY_BLOCK = "launch job: governed Bash call cannot be wrapped safely\n"
+
+pytestmark = pytest.mark.skipif(
+    sys.platform != "linux", reason="the identity hook supports Linux only"
+)
+
+
+@pytest.fixture
+def scene(tmp_path):
+    home = tmp_path / "home"
+    home.mkdir(mode=0o700)
+    bindir = tmp_path / "bin"
+    bindir.mkdir()
+    for tool in ("cat", "sed", "tr", "mkdir", "mv", "ln", "rm", "jq", "uv"):
+        found = shutil.which(tool)
+        assert found, tool
+        (bindir / tool).symlink_to(found)
+    env = {k: v for k, v in os.environ.items() if k != "CLAUDE_CONFIG_DIR"}
+    env.update(
+        HOME=str(home),
+        PATH=str(bindir),
+        UV_PYTHON=sys.executable,
+        UV_PYTHON_DOWNLOADS="never",
+    )
+    return home, env
+
+
+def _bind(home: Path, word: str, sid: str = SID) -> None:
+    sessions = home / ".claude" / "state" / "launch-level" / "sessions"
+    sessions.mkdir(parents=True, exist_ok=True, mode=0o700)
+    for part in (
+        sessions.parent,
+        sessions.parent.parent,
+        sessions.parent.parent.parent,
+    ):
+        part.chmod(0o700)
+    path = sessions / sid
+    path.write_text(word)
+    path.chmod(0o600)
+
+
+def _payload(command: str, sid: str = SID) -> dict:
+    return {
+        "hook_event_name": "PreToolUse",
+        "tool_name": "Bash",
+        "session_id": sid,
+        "tool_use_id": TOOL_ID,
+        "cwd": "/not-binding-authority",
+        "tool_input": {"command": command, "description": "keep exactly"},
+    }
+
+
+def _hook(script: Path, payload: dict, env: dict):
+    return subprocess.run(
+        [BASH, str(script)],
+        input=json.dumps(payload),
+        capture_output=True,
+        text=True,
+        env=env,
+        timeout=20,
+    )
+
+
+def _both(payload: dict, env: dict):
+    return _hook(GUARD, payload, env), _hook(IDENTITY, payload, env)
+
+
+def _updated_input(result) -> dict:
+    assert result.returncode == 0, result.stderr
+    specific = json.loads(result.stdout)["hookSpecificOutput"]
+    assert specific["hookEventName"] == "PreToolUse"
+    assert "permissionDecision" not in specific
+    return specific["updatedInput"]
+
+
+def test_full_submit_allowed_command_guard_allows_identity_rewrites_only_command(scene):
+    home, env = scene
+    _bind(home, "full-submit")
+    original = "git status"
+    payload = _payload(original)
+    guard, identity = _both(payload, env)
+    # The guard reads the original payload and allows it silently.
+    assert (guard.returncode, guard.stdout, guard.stderr) == (0, "", "")
+    updated = _updated_input(identity)
+    assert identity.stderr == ""
+    # Only the command changes; every other tool_input field is kept.
+    assert {k: v for k, v in updated.items() if k != "command"} == {
+        k: v for k, v in payload["tool_input"].items() if k != "command"
+    }
+    wrapped = shlex.split(updated["command"])
+    assert wrapped[0] == BASH and wrapped[1].endswith("launch-job-identity.sh")
+    assert wrapped[2:] == ["execute", SID, TOOL_ID, original]
+    assert updated["command"] != original
+
+
+def test_guard_must_see_the_original_command_not_the_installed_rewrite(scene):
+    # Installed, the identity hook lives at ~/.claude/hooks/ and writes its own
+    # real path into the rewrite. Were that rewrite handed to the guard, the
+    # guard would see a .claude/hooks path and block as LL-TAMPER at any level.
+    home, env = scene
+    _bind(home, "full-submit")
+    installed = home / ".claude" / "hooks" / IDENTITY.name
+    installed.parent.mkdir(mode=0o700)
+    shutil.copy2(IDENTITY, installed)
+    payload = _payload("git status")
+    guard = _hook(GUARD, payload, env)
+    assert (guard.returncode, guard.stdout, guard.stderr) == (0, "", "")
+    updated = _updated_input(_hook(installed, payload, env))
+    assert shlex.split(updated["command"])[1] == str(installed)
+    chained = _hook(GUARD, {**payload, "tool_input": updated}, env)
+    assert chained.returncode == 2
+    assert chained.stderr.splitlines()[0] == HEADER.format(level="full --submit")
+    assert chained.stderr.splitlines()[1].startswith(
+        "Blocked: touching the launch-level state"
+    )
+
+
+def test_worktree_blocked_command_guard_blocks_identity_still_rewrites(scene):
+    home, env = scene
+    _bind(home, "worktree")
+    guard, identity = _both(_payload("git commit -m wip"), env)
+    assert guard.returncode == 2
+    assert guard.stdout == ""
+    lines = guard.stderr.splitlines()
+    assert lines[0] == HEADER.format(level="worktree")
+    assert lines[1].startswith("Blocked: creating a commit")
+    assert STATE_NOTE not in guard.stderr
+    # Recorded, not part of the decision: the identity hook rewrites the call
+    # as for any governed session; the guard's exit 2 is what blocks it.
+    updated = _updated_input(identity)
+    assert shlex.split(updated["command"])[2:] == [
+        "execute",
+        SID,
+        TOOL_ID,
+        "git commit -m wip",
+    ]
+
+
+def test_ordinary_session_both_hooks_silent(scene):
+    home, env = scene
+    _bind(home, "full-submit", sid="another-session")  # a nonempty store
+    guard, identity = _both(_payload("git commit -m wip", sid="ordinary-1"), env)
+    assert (guard.returncode, guard.stdout, guard.stderr) == (0, "", "")
+    assert (identity.returncode, identity.stdout, identity.stderr) == (0, "", "")
+
+
+@pytest.mark.parametrize("word", ["degraded", "degraded\n"])
+def test_degraded_word_guard_worktree_with_state_note_identity_blocks_all(scene, word):
+    home, env = scene
+    _bind(home, word)
+    # A command the guard blocks: level worktree with the LL-STATE note.
+    guard, identity = _both(_payload("git commit -m wip"), env)
+    assert guard.returncode == 2
+    lines = guard.stderr.splitlines()
+    assert lines[0] == HEADER.format(level="worktree")
+    assert lines[1].startswith("Blocked: creating a commit")
+    assert STATE_NOTE in lines
+    # The identity hook treats the word as outside worktree, full, full-submit
+    # and blocks every Bash call of the session.
+    assert (identity.returncode, identity.stdout, identity.stderr) == (
+        2,
+        "",
+        IDENTITY_BLOCK,
+    )
+    # Mismatch: a command the guard allows at worktree is still blocked by the
+    # identity hook, so a degraded session cannot run Bash at all.
+    guard, identity = _both(_payload("git status"), env)
+    assert (guard.returncode, guard.stdout, guard.stderr) == (0, "", "")
+    assert (identity.returncode, identity.stdout, identity.stderr) == (
+        2,
+        "",
+        IDENTITY_BLOCK,
+    )

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
