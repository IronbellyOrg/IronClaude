019b0e6c402d509f45092a2ded40c3f1d2577a06
Review one task for spec compliance.

Task brief: ## Task 3: Update the pinned tests and the git fake that the seam change forces

Depends on: Task 2

Edit only where Task 2 forces it, and list each edit with its reason in the commit body. `tests/sweep/test_probes_allowlist.py`: the `GIT_STATUS` constant (line 94) gains `"--ignore-submodules=all"` as its last element; the pin `probes.ALLOWED_GIT == (GIT_STATUS,)` (line 364) becomes the four-entry tuple (add constants for the three new templates); the argv assertion in `test_the_one_git_call_is_accepted` (line 503) now expects `["git", "--no-optional-locks", "-C", "/work/tree-a", "-c", "core.fsmonitor=false", *GIT_STATUS]`; the per-path argv assertion near lines 594 to 596 slices `a[6:]` instead of `a[4:]`; add positive checks that each new template passes `check_git_args` and that `status` with `--ignore-submodules=all` missing is now rejected. `tests/sweep/test_readonly.py`: `argv[4:] == list(STATUS_ARGS)` at lines 88 and 157 become `argv[6:]` and each asserts `argv[4:6] == ["-c", "core.fsmonitor=false"]`. `tests/sweep/conftest.py`: the `argv` the fake records (line 71) gains the `-c core.fsmonitor=false` pair; `GitFake.__call__` gains `stdin=None` and `binary=False` keyword parameters, records calls whose args are not the status template in a new list `precheck_calls` instead of `calls` (so the existing "one git call per worktree" assertions keep counting status calls only), and for those pre-check templates returns `""` (empty bytes when `binary`) unless `responses` holds an entry for the key `(str(cwd), args[0])`.

Acceptance criteria:
- `uv run pytest tests/sweep -q` passes except the tests that depend on Task 4 (the two filter-refusal cases of tests/sweep/test_git_config_hole.py).
- No assertion in these files is weakened: each changed line still pins the exact argv or tuple it pinned before, now including the new flag.
- tests/sweep/test_readonly.py `test_collect_makes_one_git_call_per_worktree_that_ps_reports` still passes with `len(patch_git.calls) == extra + 1`.


Global constraints: 
- Owner design A (2026-11-14): `--ignore-submodules=all` goes into the status template; a submodule's own changes are no longer reported. No new JSON key and no new file other than this package and tests; the refusal reuses the existing `unscanned` source row (`SourceCoverage(name, "unscanned", None, reason)` built by `_failed_worktree` in `src/superclaude/cli/sweep/probes.py`).
- The owner-signed git allow-list (`ALLOWED_GIT`) may change only by the three read-only entries named in Task 2; any other allow-list change is not authorized. `ALLOWED_ORCA` and `FORBIDDEN_TOKENS` stay untouched.
- The git-status scope stays separate from the contract allow-list and the transcript scans: `_worktree_paths` and the shared `paths` list in `collect` are not filtered.
- Out of scope: `CLAUDE.md`, `tests/core/test_claude_md_worktree_rule.py`, anything under `.claude/`, wording or alignment edits, new JSON keys, sidecar files.
- Python only through UV: `uv run pytest tests/sweep -q`, `uv run ruff check`, `uv run ruff format`. Never `python -m`, bare `python`, or `pip`.
- Stage named paths only (`git add -- <paths>`, never `git add -A` or `git add .`); the plan package under `.dev/tasks/` is staged with the T2 commit. Commit locally on the current branch with conventional messages ending with the line `Co-Authored-By: Claude Code <noreply@anthropic.com>`. The executor commits only; it never pushes, opens a PR or writes to GitHub (the owner's session pushes afterwards).
- T2 (Tasks 1 to 5) and T1 (Task 6) are two separate commits. The sweep tests forbid a real subprocess unless a test carries the `integration` mark (`tests/sweep/conftest.py` autouse guard); real-git tests must carry that mark.


Start sha: 019b0e6c402d509f45092a2ded40c3f1d2577a06
Diff against the start snapshot: diff --git a/tests/sweep/conftest.py b/tests/sweep/conftest.py
index 551133622..eda16f9b0 100644
--- a/tests/sweep/conftest.py
+++ b/tests/sweep/conftest.py
@@ -50,31 +50,54 @@ class GitFake:
     the ``env`` that the real ``_git`` would build. ``responses`` maps a worktree path
     (``str``) to canned porcelain output (``str`` or ``bytes``) or to an exception
     instance that is raised for that worktree (for example ``GitCallFailed``).
+
+    The read-only inspection calls (``config``, ``ls-files``, ``check-attr``) that decide
+    whether a git filter could run are recorded in ``precheck_calls``, not ``calls``, so
+    ``calls`` still holds one status call per worktree. They answer empty output unless
+    ``responses`` holds an entry for the key ``(str(cwd), <verb>)`` (``respond_inspect``).
     """
 
     calls: list[dict] = field(default_factory=list)
-    responses: dict[str, object] = field(default_factory=dict)
+    precheck_calls: list[dict] = field(default_factory=list)
+    responses: dict[object, object] = field(default_factory=dict)
     default: object = ""
 
     def respond(self, cwd: Path | str, output: object) -> None:
         self.responses[str(cwd)] = output
 
-    def __call__(self, cwd, *args, timeout=10.0):
+    def respond_inspect(self, cwd: Path | str, verb: str, output: object) -> None:
+        self.responses[(str(cwd), verb)] = output
+
+    def __call__(self, cwd, *args, timeout=10.0, stdin=None, binary=False):
         from superclaude.cli.sweep import probes
 
         probes.check_git_args(args)  # the real seam rejects anything else first
-        self.calls.append(
-            {
-                "cwd": Path(cwd),
-                "args": tuple(args),
-                "timeout": timeout,
-                "argv": ["git", "--no-optional-locks", "-C", str(cwd), *args],
-                "env": {**os.environ, "GIT_OPTIONAL_LOCKS": "0"},
-            }
-        )
-        out = self.responses.get(str(cwd), self.default)
+        record = {
+            "cwd": Path(cwd),
+            "args": tuple(args),
+            "timeout": timeout,
+            "stdin": stdin,
+            "argv": [
+                "git",
+                "--no-optional-locks",
+                "-C",
+                str(cwd),
+                "-c",
+                "core.fsmonitor=false",
+                *args,
+            ],
+            "env": {**os.environ, "GIT_OPTIONAL_LOCKS": "0"},
+        }
+        if args[0] == "status":
+            self.calls.append(record)
+            out = self.responses.get(str(cwd), self.default)
+        else:
+            self.precheck_calls.append(record)
+            out = self.responses.get((str(cwd), args[0]), b"")
         if isinstance(out, BaseException):
             raise out
+        if binary:
+            return out.encode() if isinstance(out, str) else out
         return out.decode("utf-8", "replace") if isinstance(out, bytes) else out
 
 
diff --git a/tests/sweep/test_probes_allowlist.py b/tests/sweep/test_probes_allowlist.py
index ee7d7fac4..764c3df86 100644
--- a/tests/sweep/test_probes_allowlist.py
+++ b/tests/sweep/test_probes_allowlist.py
@@ -91,7 +91,18 @@ _ID_RES = {
     "<run>": re.compile(r"run_[0-9a-f]{12}"),
     "<dispatch>": re.compile(r"ctx_[0-9a-f]{12}"),
 }
-GIT_STATUS = ("status", "--porcelain=v1", "-z", "--branch", "--untracked-files=all")
+GIT_STATUS = (
+    "status",
+    "--porcelain=v1",
+    "-z",
+    "--branch",
+    "--untracked-files=all",
+    "--ignore-submodules=all",
+)
+GIT_CONFIG_LIST = ("config", "--show-origin", "--list", "-z")
+GIT_LS_FILES = ("ls-files", "-z")
+GIT_CHECK_ATTR = ("check-attr", "--stdin", "-z", "filter")
+GIT_FSMONITOR_OFF = ["-c", "core.fsmonitor=false"]  # after ``-C <path>`` (issue 547)
 
 CONCRETE_ARGV = tuple(
     tuple(
@@ -361,7 +372,12 @@ def test_allowed_orca_names_seven_verbs():
 def test_other_allowlist_constants_are_pinned():
     assert probes.ORCA_BINARY_DEFAULT == "orca-ide"
     assert probes.FORBIDDEN_TOKENS == frozenset({"--include-remote"})
-    assert probes.ALLOWED_GIT == (GIT_STATUS,)
+    assert probes.ALLOWED_GIT == (
+        GIT_STATUS,
+        GIT_CONFIG_LIST,
+        GIT_LS_FILES,
+        GIT_CHECK_ATTR,
+    )
     assert probes.RUN_ID_RE == r"run_[0-9a-f]{12}"
     assert probes.DISPATCH_ID_RE == r"ctx_[0-9a-f]{12}"
 
@@ -500,7 +516,43 @@ def test_the_one_git_call_is_accepted(fake_run):
     probes._git(Path("/work/tree-a"), *GIT_STATUS, timeout=5.0)
 
     (argv,) = fake_run.git_argv
-    assert argv == ["git", "--no-optional-locks", "-C", "/work/tree-a", *GIT_STATUS]
+    assert argv == [
+        "git",
+        "--no-optional-locks",
+        "-C",
+        "/work/tree-a",
+        *GIT_FSMONITOR_OFF,
+        *GIT_STATUS,
+    ]
+
+
+@pytest.mark.parametrize(
+    "template", [GIT_CONFIG_LIST, GIT_LS_FILES, GIT_CHECK_ATTR], ids=lambda t: t[0]
+)
+def test_the_three_inspection_calls_are_accepted_with_fsmonitor_off(fake_run, template):
+    probes.check_git_args(template)
+
+    probes._git(Path("/work/tree-a"), *template, timeout=5.0)
+
+    (argv,) = fake_run.git_argv
+    assert argv[:4] == ["git", "--no-optional-locks", "-C", "/work/tree-a"]
+    assert argv[4:6] == GIT_FSMONITOR_OFF
+    assert argv[6:] == list(template)
+
+
+def test_git_passes_stdin_and_returns_bytes_when_asked(fake_run):
+    fake_run.git = (0, b"a\0filter\0lfs\0", b"")
+
+    out = probes._git(
+        Path("/work/tree-a"), *GIT_CHECK_ATTR, timeout=5.0, stdin=b"a\0", binary=True
+    )
+
+    assert out == b"a\0filter\0lfs\0"
+    assert fake_run.calls[-1]["kwargs"]["input"] == b"a\0"
+    assert isinstance(
+        probes._git(Path("/work/tree-a"), *GIT_CHECK_ATTR, timeout=5.0, stdin=b""),
+        str,
+    )
 
 
 # ===========================================================================================
@@ -593,7 +645,8 @@ def test_full_sweep_runs_one_lock_free_git_status_per_worktree(
     assert [a[:4] for a in fake_run.git_argv] == [
         ["git", "--no-optional-locks", "-C", p] for p in paths
     ]
-    assert all(a[4:] == list(GIT_STATUS) for a in fake_run.git_argv)
+    assert all(a[4:6] == GIT_FSMONITOR_OFF for a in fake_run.git_argv)
+    assert all(a[6:] == list(GIT_STATUS) for a in fake_run.git_argv)
 
 
 # ===========================================================================================
diff --git a/tests/sweep/test_readonly.py b/tests/sweep/test_readonly.py
index 6e435e04a..f2dc24190 100644
--- a/tests/sweep/test_readonly.py
+++ b/tests/sweep/test_readonly.py
@@ -85,7 +85,8 @@ def test_git_argv_and_env_are_lock_free(recorder, monkeypatch):
     assert argv[1] == "--no-optional-locks"
     assert argv[2] == "-C"
     assert argv[3] == str(worktree)
-    assert argv[4:] == list(STATUS_ARGS)
+    assert argv[4:6] == ["-c", "core.fsmonitor=false"]
+    assert argv[6:] == list(STATUS_ARGS)
     assert call["env"]["GIT_OPTIONAL_LOCKS"] == "0"
     assert call["kwargs"]["timeout"] == 5.0
     assert call["kwargs"]["check"] is False
@@ -154,7 +155,8 @@ def test_collect_reaches_git_with_a_lock_free_argv_for_each_worktree(
     assert [c["argv"][3] for c in recorder.calls] == [str(p) for p in expected]
     for call in recorder.calls:
         assert call["argv"][:3] == ["git", "--no-optional-locks", "-C"]
-        assert call["argv"][4:] == list(STATUS_ARGS)
+        assert call["argv"][4:6] == ["-c", "core.fsmonitor=false"]
+        assert call["argv"][6:] == list(STATUS_ARGS)
         assert call["env"]["GIT_OPTIONAL_LOCKS"] == "0"
 
 

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
