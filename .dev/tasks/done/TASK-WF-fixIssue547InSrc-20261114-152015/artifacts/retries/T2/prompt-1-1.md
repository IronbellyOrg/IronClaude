2f41f0909eb357809de16ba287395395b9034fd4
Review one task for spec compliance.

Task brief: ## Task 2: Change the git seam, the status template and the allow-list in probes.py

Edit `src/superclaude/cli/sweep/probes.py` only. In `ALLOWED_GIT` (currently one status template, `probes.py:65-67`): append `--ignore-submodules=all` to the status template, and add exactly three read-only templates: `("config", "--show-origin", "--list", "-z")`, `("ls-files", "-z")` and `("check-attr", "--stdin", "-z", "filter")`. Update the comment above the tuple (it says "one allowed git call"). In `_git` (`probes.py:301-326`): build the argv as `git --no-optional-locks -C <cwd> -c core.fsmonitor=false *args` (the `-c` pair comes after `-C <cwd>` so the existing `argv[:3]` and `argv[3]` pins still hold); add keyword parameters `stdin: bytes | None = None` (passed to `subprocess.run` as `input=`) and `binary: bool = False` (return the raw stdout bytes instead of decoded text, so paths that are not valid UTF-8 survive a round trip into `check-attr`). Keep `check_git_args` first, the `GIT_OPTIONAL_LOCKS=0` environment, the timeout and `OUTPUT_LIMIT` handling, and the `GitCallFailed` messages unchanged. Update the `_git` docstring to say fsmonitor is always disabled because repository configuration could otherwise start a program (measured in ./artifacts/validation.md).

Acceptance criteria:
- `probes.ALLOWED_GIT` holds exactly four templates in the order status, config, ls-files, check-attr; `probes.check_git_args` accepts each and still rejects every other argv.
- A real `_git` call builds argv `["git", "--no-optional-locks", "-C", <cwd>, "-c", "core.fsmonitor=false", *args]`, passes `input=stdin` when given and returns bytes when `binary=True`.
- The fsmonitor, include, per-worktree and environment cases of tests/sweep/test_git_config_hole.py now pass (the filter and submodule-filter cases need Task 4 for the filter refusal and pass for the submodule cases through `--ignore-submodules=all`).
- `_read_worktree`'s status call still uses `ALLOWED_GIT[0]` unchanged in position.


Global constraints: 
- Owner design A (2026-11-14): `--ignore-submodules=all` goes into the status template; a submodule's own changes are no longer reported. No new JSON key and no new file other than this package and tests; the refusal reuses the existing `unscanned` source row (`SourceCoverage(name, "unscanned", None, reason)` built by `_failed_worktree` in `src/superclaude/cli/sweep/probes.py`).
- The owner-signed git allow-list (`ALLOWED_GIT`) may change only by the three read-only entries named in Task 2; any other allow-list change is not authorized. `ALLOWED_ORCA` and `FORBIDDEN_TOKENS` stay untouched.
- The git-status scope stays separate from the contract allow-list and the transcript scans: `_worktree_paths` and the shared `paths` list in `collect` are not filtered.
- Out of scope: `CLAUDE.md`, `tests/core/test_claude_md_worktree_rule.py`, anything under `.claude/`, wording or alignment edits, new JSON keys, sidecar files.
- Python only through UV: `uv run pytest tests/sweep -q`, `uv run ruff check`, `uv run ruff format`. Never `python -m`, bare `python`, or `pip`.
- Stage named paths only (`git add -- <paths>`, never `git add -A` or `git add .`); the plan package under `.dev/tasks/` is staged with the T2 commit. Commit locally on the current branch with conventional messages ending with the line `Co-Authored-By: Claude Code <noreply@anthropic.com>`. The executor commits only; it never pushes, opens a PR or writes to GitHub (the owner's session pushes afterwards).
- T2 (Tasks 1 to 5) and T1 (Task 6) are two separate commits. The sweep tests forbid a real subprocess unless a test carries the `integration` mark (`tests/sweep/conftest.py` autouse guard); real-git tests must carry that mark.


Start sha: 2f41f0909eb357809de16ba287395395b9034fd4
Diff against the start snapshot: diff --git a/src/superclaude/cli/sweep/probes.py b/src/superclaude/cli/sweep/probes.py
index 8da515c28..243385d9c 100644
--- a/src/superclaude/cli/sweep/probes.py
+++ b/src/superclaude/cli/sweep/probes.py
@@ -61,9 +61,22 @@ ALLOWED_ORCA: tuple[tuple[str, ...], ...] = (
 
 FORBIDDEN_TOKENS = frozenset({"--include-remote"})  # rejected in any position
 
-# The one allowed git call; the seam prepends ``git --no-optional-locks -C <path>``.
+# The allowed git calls; the seam prepends
+# ``git --no-optional-locks -C <path> -c core.fsmonitor=false``. Index 0 is the status
+# call (submodules are ignored: a submodule's own config could start a program, issue 547).
+# Indexes 1 to 3 are the read-only inspections that decide whether a git filter could run.
 ALLOWED_GIT: tuple[tuple[str, ...], ...] = (
-    ("status", "--porcelain=v1", "-z", "--branch", "--untracked-files=all"),
+    (
+        "status",
+        "--porcelain=v1",
+        "-z",
+        "--branch",
+        "--untracked-files=all",
+        "--ignore-submodules=all",
+    ),
+    ("config", "--show-origin", "--list", "-z"),
+    ("ls-files", "-z"),
+    ("check-attr", "--stdin", "-z", "filter"),
 )
 
 ORCA_VERSION_FILE = Path("/opt/Orca/resources/app.asar.unpacked/out/package.json")
@@ -298,19 +311,37 @@ def _orca(*args: str, timeout: float) -> OrcaResult:
     return OrcaResult("call_failed", None, "orca call failed (invalid response)")
 
 
-def _git(cwd: Path, *args: str, timeout: float) -> str:
-    """Run the allowed git call in ``cwd`` and return its stdout as text.
-
-    The argv always starts ``git --no-optional-locks -C <cwd>`` and the child runs with
-    ``GIT_OPTIONAL_LOCKS=0``, so a caller cannot build a git argv without them.
+def _git(
+    cwd: Path,
+    *args: str,
+    timeout: float,
+    stdin: bytes | None = None,
+    binary: bool = False,
+) -> str | bytes:
+    """Run an allowed git call in ``cwd`` and return its stdout (text, or bytes if ``binary``).
+
+    The argv always starts ``git --no-optional-locks -C <cwd> -c core.fsmonitor=false`` and
+    the child runs with ``GIT_OPTIONAL_LOCKS=0``, so a caller cannot build a git argv
+    without them. Fsmonitor is always off: a command named by repository configuration or
+    by the inherited environment would otherwise run during status (issue 547). ``stdin``
+    is fed to the child; ``binary`` keeps paths that are not valid UTF-8 intact.
     """
     check_git_args(args)
-    argv = ["git", "--no-optional-locks", "-C", str(cwd), *args]
+    argv = [
+        "git",
+        "--no-optional-locks",
+        "-C",
+        str(cwd),
+        "-c",
+        "core.fsmonitor=false",
+        *args,
+    ]
     env = {**os.environ, "GIT_OPTIONAL_LOCKS": "0"}
+    extra = {} if stdin is None else {"input": stdin}
     # shortcut: same as ``_orca``: run buffers the output; see the note there (owner ruling 2026-11-12).
     try:
         proc = subprocess.run(
-            argv, capture_output=True, timeout=timeout, check=False, env=env
+            argv, capture_output=True, timeout=timeout, check=False, env=env, **extra
         )
     except subprocess.TimeoutExpired as exc:
         raise GitCallFailed(f"timeout after {timeout:g} s") from exc
@@ -323,7 +354,7 @@ def _git(cwd: Path, *args: str, timeout: float) -> str:
         raise GitCallFailed(
             f"git exited {proc.returncode}" + (f": {detail[0]}" if detail else "")
         )
-    return proc.stdout.decode("utf-8", "replace")
+    return proc.stdout if binary else proc.stdout.decode("utf-8", "replace")
 
 
 # The result key that must hold a list in each captured list reply (steps 1.0a and 1.4).

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
