bdf9dd769057e58979faa45c8f73f77c8446ce1a
Review one task for spec compliance.

Task brief: Task 2: Prove a same-size same-mtime rewrite is reported as stale. Depends on: Task 1. In `tests/cli/test_how_we_work_install.py`, add a test next to `test_skip_without_force_names_only_stale_files`. Seed `target / "PRINCIPLES.md"` with the shipped bytes of `install_core._get_core_source() / "PRINCIPLES.md"` and call `install_core.install_core_files(target_path=target, force=False)` (this fills the stdlib comparison cache with "identical"). Then rewrite the target with different bytes of the same length, restore its old modification time with `os.utime(path, ns=(st_atime_ns, st_mtime_ns))`, call `install_core_files` again, and assert `PRINCIPLES.md` is listed in `message.split("NOT updated")[1]`. Add `import os` if the file lacks it.
Acceptance criteria ids: T2.AC1: The new test passes with Task 1 applied and fails when the old `filecmp.cmp` comparison is put back (check by running it with `filecmp.clear_cache` disabled through a throwaway pytest plugin, not by editing the source). T2.AC2: `uv run pytest tests/cli/test_how_we_work_install.py -q` and `uv run ruff check src/superclaude/cli/install_core.py tests/cli/test_how_we_work_install.py` pass.
Global constraints: Change only `src/superclaude/cli/install_core.py` and one test in `tests/cli/test_how_we_work_install.py`; `src/superclaude/cli/install_keep.py` already has the fix and stays as it is. Nothing is committed or pushed; this is the issue 606 branch.
Start sha: bdf9dd769057e58979faa45c8f73f77c8446ce1a
Diff against the start snapshot: (repo root /home/coder/workspaces/worktrees/IronClaude/issue-606; run `git diff bdf9dd769057e58979faa45c8f73f77c8446ce1a -- tests/cli/test_how_we_work_install.py` to see it; the full text follows)
```
--- a/tests/cli/test_how_we_work_install.py
+++ b/tests/cli/test_how_we_work_install.py
@@ -3,6 +3,7 @@
 from __future__ import annotations
 
+import os
 from pathlib import Path
 
 import pytest
@@ end of file
     assert "RULES.md" in stale_part
     assert "PRINCIPLES.md" not in stale_part
+
+
+def test_same_size_rewrite_with_old_mtime_is_reported_stale(tmp_path):
+    """filecmp caches answers by (size, mtime); a same-size rewrite that keeps
+    its old mtime must still be reported, not answered from the cache."""
+    target = tmp_path / ".claude"
+    shipped = (install_core._get_core_source() / "PRINCIPLES.md").read_bytes()
+    kept = target / "PRINCIPLES.md"
+    _seed(kept, shipped)
+    install_core.install_core_files(target_path=target, force=False)  # primes the cache
+
+    before = kept.stat()
+    kept.write_bytes(bytes([shipped[0] ^ 1]) + shipped[1:])  # same length, one byte differs
+    os.utime(kept, ns=(before.st_atime_ns, before.st_mtime_ns))
+
+    ok, message = install_core.install_core_files(target_path=target, force=False)
+
+    assert ok, message
+    assert "PRINCIPLES.md" in message.split("NOT updated")[1]
```
Codegraph context: index_state: fresh; checked_at: 2026-11-19T01:43:08Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-606; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-606
call codegraph only when index_state: fresh, never to widen scope
Q2b: the diff adds one new test function and changes no existing symbol, so there are no dependents outside the diff. The run log for this task is .dev/tasks/to-do/TASK-WF-makeInstallCoreS-20261119-013812/artifacts/t2-checks.log: lines 2-4 the file's 9 tests pass, line 6 ruff passes, lines 7-13 with `filecmp.clear_cache` disabled through the throwaway plugin /tmp/noclear_plugin.py (`filecmp.clear_cache = lambda: None`, loaded with `-p noclear_plugin`) the new test fails with IndexError at the `NOT updated` split, which means the stale notice was not printed.
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
