c611441c93a032ba0e8c69a8a340cf0bc1acffd7
Review one task for spec compliance.

Task brief: ## Task 1: Print gateway_port, shim_base_port and upstream in the `_real_launch` failure message

In `_real_launch` (tests/unit/test_ccsession_tiers.py:1669-1704), read the upstream URL into a local variable before `extra.pop("upstream")` at :1684 and use that variable for ANTHROPIC_BASE_URL. Replace the bare message of `assert proc.returncode == 0, proc.stderr` at :1702 with one that starts `gateway_port=<port> shim_base_port=<port> upstream=<url>` and then the full stderr. The gateway port is the port parsed from the upstream URL (`urllib.parse.urlsplit`); the shim base port is the `port` argument. Each value that is missing or cannot be parsed prints as `unobserved` (for example `shim_base_port=unobserved` when `port` is None). Add `import urllib.parse` to the import block (:10-26) if it is not already importable there.

Acceptance criteria:
- A launch with a non-zero exit fails with an AssertionError whose message contains `gateway_port=`, `shim_base_port=`, `upstream=` and the launcher stderr; with `port=None` it contains `shim_base_port=unobserved`.
- The environment `_real_launch` passes to ccsession is unchanged (same keys and values as before for every caller).
- `uv run pytest tests/unit/test_ccsession_tiers.py -q -p no:cacheprovider -k "busy_shim or tiers_off_launch or upgraded_code or relative_defaults or every_shim_launch"` passes; output saved to ./artifacts/t1-pytest.log.
Global constraints: ## Constraints

- Change only tests/unit/test_ccsession_tiers.py. Do not change src/superclaude/skills/ccsession-tag/models.py or src/superclaude/skills/ccsession-tag/ccsession: the refusal is the documented launcher contract (REPORT.md, Documentation Context).
- Leave the `shim` fixture pairing at tests/unit/test_ccsession_tiers.py:766-767, the line at :1075 and the gateway at :2098 unchanged (source.md).
- The forbidden windows are defined by `models.shim_upstream_problem(url, base)` (models.py:822-844): a gateway port 0..97 above `base + 101*k`, k in 0..5. Use that function; do not re-implement the window arithmetic in the test.
- Out of scope, record only: the `_real_launch` environment leak (test:1680 copies os.environ, :1689 removes only CC_SHIM_PORT), ccsession:985 treating every rc==1 as a refusal, the remaining #352 port races, and the 30 CI runs.
- pytest-xdist is not installed locally; CI installs it with `uv pip install "pytest-xdist>=3.5,<4"` (.github/workflows/test.yml:29). Install it the same way for the parallel runs; do not add it to pyproject.toml or uv.lock.
- UV only (`uv run ...`). Evidence goes under ./artifacts/ in this package.
Start sha: c611441c93a032ba0e8c69a8a340cf0bc1acffd7
Diff against the start snapshot: 
diff --git a/tests/unit/test_ccsession_tiers.py b/tests/unit/test_ccsession_tiers.py
index 0a1a90dd..00c1399c 100644
--- a/tests/unit/test_ccsession_tiers.py
+++ b/tests/unit/test_ccsession_tiers.py
@@ -22,6 +22,7 @@ import sys
 import threading
 import time
 import urllib.error
+import urllib.parse
 import urllib.request
 from pathlib import Path
 
@@ -1677,11 +1678,12 @@ def _real_launch(tmp_path: Path, port: int | None, *args: str, **extra: str):
     fake.parent.mkdir(exist_ok=True)
     fake.write_text('#!/bin/sh\necho "$ANTHROPIC_BASE_URL" > "$SEEN_FILE"\n')
     fake.chmod(0o755)
+    upstream = extra.pop("upstream")
     env = os.environ.copy()
     env.update(
         HOME=str(tmp_path / "home"),
         CLAUDE_BIN=str(fake),
-        ANTHROPIC_BASE_URL=extra.pop("upstream"),
+        ANTHROPIC_BASE_URL=upstream,
         CC_SHIM_SCRIPT=str(tmp_path / "shim-under-test.py"),
         SEEN_FILE=str(tmp_path / "seen"),
         AIDEV_AI_DEFAULTS_PATH=str(_defaults(tmp_path)),
@@ -1699,7 +1701,15 @@ def _real_launch(tmp_path: Path, port: int | None, *args: str, **extra: str):
         text=True,
         timeout=60,
     )
-    assert proc.returncode == 0, proc.stderr
+    try:
+        gateway_port = urllib.parse.urlsplit(upstream).port
+    except ValueError:
+        gateway_port = None
+    assert proc.returncode == 0, (
+        f"gateway_port={'unobserved' if gateway_port is None else gateway_port} "
+        f"shim_base_port={'unobserved' if port is None else port} "
+        f"upstream={upstream}\n{proc.stderr}"
+    )
     assert proc.stdout == ""  # the fake claude prints nothing; status is on stderr
     return proc.stderr, (tmp_path / "seen").read_text().strip()
 
diff --git a/.dev/tasks/to-do/TASK-WF-fixIronbellyOrgI-20261108-110741/artifacts/t1-pytest.log b/.dev/tasks/to-do/TASK-WF-fixIronbellyOrgI-20261108-110741/artifacts/t1-pytest.log
new file mode 100644
index 00000000..586984df
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-fixIronbellyOrgI-20261108-110741/artifacts/t1-pytest.log
@@ -0,0 +1,11 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-443
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, anyio-4.16.0
+collected 173 items / 168 deselected / 5 selected
+
+tests/unit/test_ccsession_tiers.py .....                                 [100%]
+
+====================== 5 passed, 168 deselected in 17.94s ======================
diff --git a/.dev/tasks/to-do/TASK-WF-fixIronbellyOrgI-20261108-110741/artifacts/t1-message-check.py b/.dev/tasks/to-do/TASK-WF-fixIronbellyOrgI-20261108-110741/artifacts/t1-message-check.py
new file mode 100644
index 00000000..5ed31201
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-fixIronbellyOrgI-20261108-110741/artifacts/t1-message-check.py
@@ -0,0 +1,31 @@
+import subprocess, sys
+from pathlib import Path
+import pytest
+sys.path.insert(0, "/home/coder/workspaces/worktrees/IronClaude/issue-443/tests/unit")
+import test_ccsession_tiers as t
+
+class P:  # a refused launch
+    returncode = 1
+    stdout = ""
+    stderr = "[ccsession] ERROR: refused"
+
+@pytest.mark.parametrize("port,expect", [(40000, "shim_base_port=40000"), (None, "shim_base_port=unobserved")])
+def test_message(tmp_path, monkeypatch, port, expect):
+    seen = {}
+    def fake_run(cmd, **kw):
+        seen["env"] = kw["env"]
+        return P()
+    monkeypatch.setattr(subprocess, "run", fake_run)
+    with pytest.raises(AssertionError) as e:
+        t._real_launch(tmp_path, port, upstream="http://127.0.0.1:33361")
+    msg = str(e.value)
+    print(msg.splitlines()[0])
+    assert "gateway_port=33361" in msg and expect in msg and "upstream=http://127.0.0.1:33361" in msg and "[ccsession] ERROR: refused" in msg
+    assert seen["env"]["ANTHROPIC_BASE_URL"] == "http://127.0.0.1:33361"
+    assert ("CC_SHIM_PORT" in seen["env"]) == (port is not None)
+
+def test_bad_url(tmp_path, monkeypatch):
+    monkeypatch.setattr(subprocess, "run", lambda cmd, **kw: P())
+    with pytest.raises(AssertionError) as e:
+        t._real_launch(tmp_path, 1, upstream="http://127.0.0.1:notaport")
+    assert "gateway_port=unobserved" in str(e.value)
diff --git a/.dev/tasks/to-do/TASK-WF-fixIronbellyOrgI-20261108-110741/artifacts/t1-message-check.log b/.dev/tasks/to-do/TASK-WF-fixIronbellyOrgI-20261108-110741/artifacts/t1-message-check.log
new file mode 100644
index 00000000..9099db1a
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-fixIronbellyOrgI-20261108-110741/artifacts/t1-message-check.log
@@ -0,0 +1,4 @@
+gateway_port=33361 shim_base_port=40000 upstream=http://127.0.0.1:33361
+.gateway_port=33361 shim_base_port=unobserved upstream=http://127.0.0.1:33361
+..
+3 passed in 0.30s
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
