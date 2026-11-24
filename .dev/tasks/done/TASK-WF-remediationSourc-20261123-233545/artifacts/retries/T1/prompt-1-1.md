1fea3d4d7c682bd36860fae56105c77d1c6c1e4b
Review one task for spec compliance.

Task brief: ## Task 1: Add a read-only failed-step helper to first_run.py

In `src/superclaude/cli/issue_watch/first_run.py`, add a public function `failed_step(config_path: Path) -> tuple[str, datetime] | None` next to `_report_dir` (line 78) and `_write_report` (line 86). It reads the raw config with `_raw_config`, takes the report directory with `_report_dir` and the report file name with the same rule `first_run` uses at lines 141-145 (`first-run.txt` when the directory is the config's absolute `state_dir`, else `<config stem>-first-run.txt` beside the config). It reads only the first line of that file, opened with `os.O_NOFOLLOW` and a read bounded to 4096 bytes, and decodes it as UTF-8. When the line starts with `first-run: failed ` it returns the step name (the word after `failed `, up to the next colon) and the file's modification time as a timezone-aware UTC datetime. In every other case, including a missing file, a symlink, a decode error and any `OSError`, it returns `None`. It never writes. Share the report-name rule with `first_run` through one small private function so the two cannot drift. Source requirements 4 and 5.

Acceptance criteria:
- T1.AC1: `failed_step` returns `("config", <datetime>)` for a report whose first line is `first-run: failed config: worktree_invalid`, and `None` for `first-run: passed`, a missing file, a symlinked file and a non-UTF-8 first line.
- T1.AC2: With a relative or missing `state_dir` in the config, `failed_step` finds `<stem>-first-run.txt` beside the config.
- T1.AC3: `first_run()` writes the same report names as before (existing `tests/issue_watch/test_first_run.py` still pass unchanged).
Global constraints: ## Constraints

- Reuse the existing `first_run` function as the only setup path; do not add GitHub writes, label creation or store creation to `dispatch.py` or `cycle.py` (the boundary pinned by `tests/issue_watch/test_security_invariants.py` stays intact).
- Do not change the config schema (`_TOP_KEYS` in `src/superclaude/cli/issue_watch/cycle.py`) and do not change `ensure_config` in `src/superclaude/cli/issue_watch/generate.py`.
- A config with no first-run report, or whose report starts with `first-run: passed`, is never retried.
- A dry-run sweep makes no `first_run` call and writes no file.
- Do not edit anything under `.claude/`; change `src/` and `tests/` only.
Start sha: 1fea3d4d7c682bd36860fae56105c77d1c6c1e4b
Diff against the start snapshot: 
```diff
diff --git a/src/superclaude/cli/issue_watch/first_run.py b/src/superclaude/cli/issue_watch/first_run.py
index ea91d4763..9e73926c3 100644
--- a/src/superclaude/cli/issue_watch/first_run.py
+++ b/src/superclaude/cli/issue_watch/first_run.py
@@ -29,6 +29,7 @@ from __future__ import annotations
 
 import json
 import os
+import re
 from collections.abc import Callable
 from dataclasses import dataclass, field, replace
 from datetime import datetime, timezone
@@ -39,6 +40,7 @@ from .defaults import Defaults
 from .runner import Runner
 
 REPORT_FILE = "first-run.txt"
+_FAILED_HEAD = re.compile(r"first-run: failed ([a-z_]+):")
 LOCK_HELD_EXIT = 75
 
 STEPS = ("config", "label", "init_state", "dry_run", "lock", "restart")
@@ -83,6 +85,36 @@ def _report_dir(config_path: Path, raw: dict | None) -> Path:
     return config_path.parent
 
 
+def _report_name(config_path: Path, directory: Path) -> str:
+    """``first-run.txt`` in a state dir; ``<stem>-first-run.txt`` beside a config with none."""
+    if directory != config_path.parent:
+        return REPORT_FILE
+    return f"{config_path.stem}-{REPORT_FILE}"
+
+
+def failed_step(config_path: Path) -> tuple[str, datetime] | None:
+    """The step a failed first run stopped at and when its report was written, else None.
+
+    Read only. Looks where ``first_run`` writes the report, opens it without following a
+    symlink, reads at most 4096 bytes of its first line, and returns None for a missing,
+    unreadable or non-UTF-8 file and for any report that does not start ``first-run: failed``.
+    """
+    config_path = Path(config_path)
+    directory = _report_dir(config_path, _raw_config(config_path))
+    path = directory / _report_name(config_path, directory)
+    try:
+        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
+        with os.fdopen(fd, "rb") as handle:
+            head = handle.read(4096).split(b"\n", 1)[0].decode("utf-8")
+            written = os.fstat(handle.fileno()).st_mtime
+    except (OSError, ValueError):  # UnicodeDecodeError is a ValueError
+        return None
+    found = _FAILED_HEAD.match(head)
+    if found is None:
+        return None
+    return found.group(1), datetime.fromtimestamp(written, timezone.utc)
+
+
 def _write_report(directory: Path, text: str, name: str = REPORT_FILE) -> Path | None:
     path = directory / name
     try:
@@ -138,11 +170,7 @@ def first_run(
     directory = _report_dir(config_path, raw)
     # A config with no readable state_dir reports next to itself, under its own name, so two
     # repositories never overwrite one report.
-    report_name = (
-        REPORT_FILE
-        if directory != config_path.parent
-        else (f"{config_path.stem}-{REPORT_FILE}")
-    )
+    report_name = _report_name(config_path, directory)
     steps: list[Step] = []
     lines: list[str] = []
 
```

Codegraph context
index_state: fresh
checked_at: 2026-11-24T02:39:04Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-751
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-751
call codegraph only when index_state: fresh, never to widen scope
Dependents not in the diff (Q2b): first_run() in first_run.py now calls _report_name (same name rule as before); first_run's only production caller is run_sweep (dispatch.py:427), signature unchanged; failed_step has no caller yet (Task 2). Q2b: codegraph_callers first_run -> run_sweep, tests/issue_watch/test_first_run.py:125,:347

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
