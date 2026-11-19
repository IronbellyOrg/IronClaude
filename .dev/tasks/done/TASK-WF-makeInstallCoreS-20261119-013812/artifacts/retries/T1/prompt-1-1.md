646e65a5a8c9535d7a54bb48b92110bd1e8b128b
Review one task for spec compliance.

Task brief: Task 1: Replace install_core's private comparison with install_keep.same_content. In `src/superclaude/cli/install_core.py`, delete the private `_same_content` (lines 121-125), add `from .install_keep import same_content` beside the other imports, and change its only caller (line 97, the `stale` list in `install_core_files`) to call `same_content`. Remove `import filecmp` (line 8), because line 123 is its only use in that file.
Acceptance criteria ids: T1.AC1: `install_core.py` has no `filecmp` import and no `_same_content`; `install_core_files` calls `same_content` from `install_keep` for the stale list. T1.AC2: Existing callers and tests keep working: `uv run pytest tests/cli -q -k install` passes, including `tests/cli/test_how_we_work_install.py::test_skip_without_force_names_only_stale_files`.
Global constraints: Change only `src/superclaude/cli/install_core.py` and one test in `tests/cli/test_how_we_work_install.py`; `src/superclaude/cli/install_keep.py` already has the fix and stays as it is. Nothing is committed or pushed; this is the issue 606 branch.
Start sha: 646e65a5a8c9535d7a54bb48b92110bd1e8b128b
Diff against the start snapshot: (repo root /home/coder/workspaces/worktrees/IronClaude/issue-606; run `git diff 646e65a5a8c9535d7a54bb48b92110bd1e8b128b -- src/superclaude/cli/install_core.py` to see it; the full text follows)
```
--- a/src/superclaude/cli/install_core.py
+++ b/src/superclaude/cli/install_core.py
@@ -5,11 +5,12 @@
 """
 
-import filecmp
 import shutil
 from pathlib import Path
 from typing import List, Tuple
 
+from .install_keep import same_content
+
 # Core files this version ships; list_installed_core_files reports only these.
@@ -94,7 +95,7 @@
         stale = [
-            n for n in skipped if not _same_content(core_source / n, target_path / n)
+            n for n in skipped if not same_content(core_source / n, target_path / n)
         ]
@@ -118,13 +119,6 @@
 
-def _same_content(a: Path, b: Path) -> bool:
-    try:
-        return filecmp.cmp(a, b, shallow=False)
-    except OSError:
-        return False
-
-
 def _get_core_source() -> Path:
```
Codegraph context: index_state: fresh; checked_at: 2026-11-19T01:43:08Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-606; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-606
call codegraph only when index_state: fresh, never to widen scope
Dependents of `install_core_files` (behaviour changed, signature unchanged) outside the diff, confirmed by Grep: src/superclaude/cli/main.py:178 and :365, tests/cli/test_how_we_work_install.py, tests/cli/test_bash_inspection_policy.py, tests/cli/test_issue_body_templates.py, tests/unit/test_cli_install.py:967. The test run log for this task is in .dev/tasks/to-do/TASK-WF-makeInstallCoreS-20261119-013812/artifacts/t1-checks.log (ruff: All checks passed!; pytest tests/cli -q -k install: 351 passed, 1 skipped).
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
