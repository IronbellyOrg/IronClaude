d74617ddffa12304cba21c44149e1f39d6ea0e18
Review one task for spec compliance.

Task brief: ## Task 4: Refuse to read a worktree where a filter selected by a tracked path could run

Depends on: Task 3

In `src/superclaude/cli/sweep/probes.py` add `_filter_blocks_status(path: Path, timeout: float) -> bool` and call it in `_read_worktree` (`probes.py:921-945`) after the `budget.call_timeout()` check and before the status `_git` call, inside the same `try` so a `GitCallFailed` from any pre-check call is handled by the existing `except GitCallFailed` branch (reason "worktree not readable", or the budget reason on a timeout). Behaviour: run `_git(path, *CONFIG_LIST, timeout=timeout, binary=True)` and parse the `-z --show-origin` output as pairs (origin, then `key\nvalue`); a driver name is a key shaped `filter.<name>.clean` or `filter.<name>.process` (split on the first `filter.` and the last `.clean`/`.process`; keep the driver name's case, git keeps subsection case) with a non-empty value; no such driver means return False with no further call. Otherwise run `_git(path, *LS_FILES, binary=True)` and feed its bytes unchanged to `_git(path, *CHECK_ATTR, stdin=<those bytes>, binary=True)`; parse the `-z` output as triples (path, attribute, value) and return True when any value equals a driver name. Any parse surprise (a triple count that is not a multiple of three, a non-zero exit) fails closed: raise `GitCallFailed`. When it returns True, `_read_worktree` does not run status; it returns `_failed_worktree(path, packages, name, "git filter could run a program")` plus the package rows, exactly as the other failure branches do. Name the three template tuples as module constants next to `ALLOWED_GIT` entries by indexing (`ALLOWED_GIT[1]`, `[2]`, `[3]`), not by repeating the literals. Add a one-line `# shortcut:` comment noting that a filter named only in a submodule's own config is closed by `--ignore-submodules=all`, not by this check. Add unit tests in `tests/sweep/test_probes_allowlist.py` using `patch_git` responses (keys `(str(path), "config")` etc.): no driver means one status call and no ls-files; a driver with no selecting path means status runs; a driver selected by a path means no status call, coverage `unscanned`, reason "git filter could run a program"; a mixed-case driver name matches; a config failure produces "worktree not readable"; a non-UTF-8 tracked path is passed to check-attr byte-for-byte.

Acceptance criteria:
- tests/sweep/test_git_config_hole.py passes in full, including both filter cases (marker absent, coverage `unscanned`) and the unselected-filter control (coverage `read`).
- A filter defined only in `/etc/gitconfig` (the `lfs` shape) and selected by no tracked path leaves the worktree readable; measured against this host's worktrees the new check refuses none (see ./artifacts/validation.md, section "Stage 2").
- The new unit tests pass and the existing `tests/sweep/test_probes_allowlist.py::test_collect_*` source-row tests still pass without editing; the `unscanned` row has no new JSON key (`tests/sweep/test_cli_contract.py` and the report tests are untouched and green).
- `collect` (`probes.py:1217`) and `read_worktree` (`probes.py:948`), the two callers of `_read_worktree`, both get the new behaviour with no change to their own code.


Global constraints: 
- Owner design A (2026-11-14): `--ignore-submodules=all` goes into the status template; a submodule's own changes are no longer reported. No new JSON key and no new file other than this package and tests; the refusal reuses the existing `unscanned` source row (`SourceCoverage(name, "unscanned", None, reason)` built by `_failed_worktree` in `src/superclaude/cli/sweep/probes.py`).
- The owner-signed git allow-list (`ALLOWED_GIT`) may change only by the three read-only entries named in Task 2; any other allow-list change is not authorized. `ALLOWED_ORCA` and `FORBIDDEN_TOKENS` stay untouched.
- The git-status scope stays separate from the contract allow-list and the transcript scans: `_worktree_paths` and the shared `paths` list in `collect` are not filtered.
- Out of scope: `CLAUDE.md`, `tests/core/test_claude_md_worktree_rule.py`, anything under `.claude/`, wording or alignment edits, new JSON keys, sidecar files.
- Python only through UV: `uv run pytest tests/sweep -q`, `uv run ruff check`, `uv run ruff format`. Never `python -m`, bare `python`, or `pip`.
- Stage named paths only (`git add -- <paths>`, never `git add -A` or `git add .`); the plan package under `.dev/tasks/` is staged with the T2 commit. Commit locally on the current branch with conventional messages ending with the line `Co-Authored-By: Claude Code <noreply@anthropic.com>`. The executor commits only; it never pushes, opens a PR or writes to GitHub (the owner's session pushes afterwards).
- T2 (Tasks 1 to 5) and T1 (Task 6) are two separate commits. The sweep tests forbid a real subprocess unless a test carries the `integration` mark (`tests/sweep/conftest.py` autouse guard); real-git tests must carry that mark.


Start sha: d74617ddffa12304cba21c44149e1f39d6ea0e18
Diff against the start snapshot: diff --git a/src/superclaude/cli/sweep/probes.py b/src/superclaude/cli/sweep/probes.py
index 243385d9c..7081db623 100644
--- a/src/superclaude/cli/sweep/probes.py
+++ b/src/superclaude/cli/sweep/probes.py
@@ -949,6 +949,58 @@ def _package_active(pkg: PackageRecord, changed: tuple[str, ...]) -> bool:
     return any(p.startswith(prefixes) for p in changed)
 
 
+FILTER_REASON = "git filter could run a program"
+
+
+def _filter_drivers(config: bytes) -> set[bytes]:
+    """Filter driver names whose effective ``clean`` or ``process`` command is non-empty.
+
+    ``config`` is ``git config --show-origin --list -z`` output: for each entry the origin,
+    then ``key\\nvalue``. Anything else raises ``GitCallFailed`` (an unclear list is refused).
+    """
+    parts = config.split(b"\0")
+    if parts and parts[-1] == b"":
+        parts.pop()
+    if len(parts) % 2:
+        raise GitCallFailed("unreadable git configuration")
+    effective: dict[bytes, bytes] = {}
+    for entry in parts[1::2]:
+        key, _, value = entry.partition(b"\n")
+        effective[key] = value  # a later entry overrides an earlier one
+    return {
+        key[len(b"filter.") : key.rindex(b".")]
+        for key, value in effective.items()
+        if value
+        and key.startswith(b"filter.")
+        and key.endswith((b".clean", b".process"))
+        and key.count(b".") >= 2
+    }
+
+
+def _filter_blocks_status(path: Path, timeout: float) -> bool:
+    """True when a git filter with a command is selected by a tracked path of ``path``.
+
+    ``git status`` runs that command for a file it has to re-read. The three calls only
+    read; each runs with fsmonitor off (``_git``). A driver defined only in a submodule's
+    own config is not seen here; ``--ignore-submodules=all`` on the status call closes it.
+    Raises ``GitCallFailed`` when any call fails or its output cannot be parsed.
+    """
+    drivers = _filter_drivers(_git(path, *ALLOWED_GIT[1], timeout=timeout, binary=True))
+    if not drivers:
+        return False
+    tracked = _git(path, *ALLOWED_GIT[2], timeout=timeout, binary=True)
+    if not tracked:
+        return False
+    attrs = _git(
+        path, *ALLOWED_GIT[3], timeout=timeout, stdin=tracked, binary=True
+    ).split(b"\0")
+    if attrs and attrs[-1] == b"":
+        attrs.pop()
+    if len(attrs) % 3:  # path, attribute, value per tracked path
+        raise GitCallFailed("unreadable git attributes")
+    return any(value in drivers for value in attrs[2::3])
+
+
 def _read_worktree(
     path: Path, budget: Budget
 ) -> tuple[WorktreeState, tuple[SourceCoverage, ...]]:
@@ -966,6 +1018,9 @@ def _read_worktree(
         state, row = _failed_worktree(path, packages, name, reason)
         return state, (row, *package_rows)
     try:
+        if _filter_blocks_status(path, timeout):
+            state, row = _failed_worktree(path, packages, name, FILTER_REASON)
+            return state, (row, *package_rows)
         raw = _git(path, *ALLOWED_GIT[0], timeout=timeout)
     except GitCallFailed as exc:
         cut = str(exc).startswith("timeout") and budget.cut()
diff --git a/tests/sweep/test_probes_allowlist.py b/tests/sweep/test_probes_allowlist.py
index 764c3df86..dd1f10175 100644
--- a/tests/sweep/test_probes_allowlist.py
+++ b/tests/sweep/test_probes_allowlist.py
@@ -175,6 +175,11 @@ class FakeRun:
         self.calls: list[dict] = []
         self.orca: dict[tuple[str, ...], object] = {}
         self.git: object = (0, b"## main\0", b"")
+        self.git_inspect: object = (
+            0,
+            b"",
+            b"",
+        )  # reply to config, ls-files, check-attr
         self.default: object = (1, b"", b"no canned reply")
 
     def reply(self, *args, code=0, out=b"", err=b"", raises=None) -> None:
@@ -183,7 +188,8 @@ class FakeRun:
     def __call__(self, argv, **kwargs):
         self.calls.append({"argv": list(argv), "kwargs": kwargs})
         if argv[0] == "git":
-            reply = self.git
+            # The read-only inspections that precede status (issue 547) see an empty list.
+            reply = self.git if argv[6] == "status" else self.git_inspect
         else:
             reply = self.orca.get(tuple(argv[1:]), self.default)
         if isinstance(reply, BaseException):
@@ -199,7 +205,20 @@ class FakeRun:
 
     @property
     def git_argv(self) -> list[list[str]]:
-        return [c["argv"] for c in self.calls if c["argv"][0] == "git"]
+        """The status calls (the inspections before them are in ``git_inspect_argv``)."""
+        return [
+            c["argv"]
+            for c in self.calls
+            if c["argv"][0] == "git" and c["argv"][6] == "status"
+        ]
+
+    @property
+    def git_inspect_argv(self) -> list[list[str]]:
+        return [
+            c["argv"]
+            for c in self.calls
+            if c["argv"][0] == "git" and c["argv"][6] != "status"
+        ]
 
 
 @pytest.fixture
@@ -534,14 +553,14 @@ def test_the_three_inspection_calls_are_accepted_with_fsmonitor_off(fake_run, te
 
     probes._git(Path("/work/tree-a"), *template, timeout=5.0)
 
-    (argv,) = fake_run.git_argv
+    (argv,) = fake_run.git_inspect_argv
     assert argv[:4] == ["git", "--no-optional-locks", "-C", "/work/tree-a"]
     assert argv[4:6] == GIT_FSMONITOR_OFF
     assert argv[6:] == list(template)
 
 
 def test_git_passes_stdin_and_returns_bytes_when_asked(fake_run):
-    fake_run.git = (0, b"a\0filter\0lfs\0", b"")
+    fake_run.git_inspect = (0, b"a\0filter\0lfs\0", b"")
 
     out = probes._git(
         Path("/work/tree-a"), *GIT_CHECK_ATTR, timeout=5.0, stdin=b"a\0", binary=True
@@ -2068,6 +2087,128 @@ def test_read_worktree_untracked_dev_tasks_path_is_unsaved_and_marks_the_package
     assert package.active is True
 
 
+# ===========================================================================================
+# Issue 547: a worktree where a git filter could run is not read
+# ===========================================================================================
+
+LFS_CONFIG = b"file:/etc/gitconfig\0filter.lfs.clean\ngit-lfs clean -- %f\0"
+SELECTED = b"a.txt\0filter\0lfs\0"
+NOT_SELECTED = b"a.txt\0filter\0unspecified\0"
+
+
+def _verbs(calls) -> list[str]:
+    return [c["args"][0] for c in calls]
+
+
+def test_no_filter_driver_means_status_runs_after_one_config_read(
+    sweep_root, patch_git
+):
+    patch_git.respond_inspect(sweep_root.root, "config", b"file:/x\0core.bare\nfalse\0")
+
+    _state, row = probes.read_worktree(sweep_root.root, probes.Budget())
+
+    assert row.coverage == "read"
+    assert _verbs(patch_git.precheck_calls) == ["config"]
+    assert _verbs(patch_git.calls) == ["status"]
+
+
+def test_driver_selected_by_no_tracked_path_still_reads_status(sweep_root, patch_git):
+    root = sweep_root.root
+    patch_git.respond_inspect(root, "config", LFS_CONFIG)
+    patch_git.respond_inspect(root, "ls-files", b"a.txt\0")
+    patch_git.respond_inspect(root, "check-attr", NOT_SELECTED)
+
+    _state, row = probes.read_worktree(root, probes.Budget())
+
+    assert row.coverage == "read"
+    assert _verbs(patch_git.precheck_calls) == ["config", "ls-files", "check-attr"]
+    assert _verbs(patch_git.calls) == ["status"]
+
+
+def test_driver_selected_by_a_tracked_path_skips_status_and_is_unscanned(
+    sweep_root, patch_git
+):
+    root = sweep_root.root
+    patch_git.respond_inspect(root, "config", LFS_CONFIG)
+    patch_git.respond_inspect(root, "ls-files", b"a.txt\0")
+    patch_git.respond_inspect(root, "check-attr", SELECTED)
+
+    state, row = probes.read_worktree(root, probes.Budget())
+
+    assert patch_git.calls == []  # no status call was made
+    assert row.coverage == "unscanned"
+    assert row.unscanned == probes.FILTER_REASON == "git filter could run a program"
+    assert state.status_read is False
+
+
+def test_driver_name_keeps_its_case_when_matched_against_the_attribute(
+    sweep_root, patch_git
+):
+    root = sweep_root.root
+    config = b"file:/x\0filter.LFS.process\nsomething\0"
+    patch_git.respond_inspect(root, "config", config)
+    patch_git.respond_inspect(root, "ls-files", b"a.txt\0")
+    patch_git.respond_inspect(root, "check-attr", b"a.txt\0filter\0LFS\0")
+
+    _state, row = probes.read_worktree(root, probes.Budget())
+
+    assert row.unscanned == probes.FILTER_REASON
+    assert patch_git.calls == []
+
+
+def test_a_later_empty_entry_removes_the_driver(sweep_root, patch_git):
+    config = (
+        b"file:/a\0filter.x.clean\ncmd\0file:/b\0filter.x.clean\n\0"
+        b"file:/c\0filter.y.smudge\ncmd\0"  # smudge never runs during status
+    )
+    patch_git.respond_inspect(sweep_root.root, "config", config)
+
+    _state, row = probes.read_worktree(sweep_root.root, probes.Budget())
+
+    assert row.coverage == "read"
+    assert _verbs(patch_git.precheck_calls) == ["config"]
+
+
+@pytest.mark.parametrize(
+    ("verb", "output"),
+    [
+        ("config", probes.GitCallFailed("git exited 128")),
+        ("config", b"unpaired"),  # odd number of fields: unclear, refused
+        ("ls-files", probes.GitCallFailed("git exited 128")),
+        ("check-attr", probes.GitCallFailed("git exited 128")),
+        ("check-attr", b"a.txt\0filter\0"),  # not a multiple of three: unclear
+    ],
+    ids=["config-fails", "config-odd", "ls-files-fails", "attr-fails", "attr-odd"],
+)
+def test_a_failed_or_unclear_inspection_is_refused_as_not_readable(
+    sweep_root, patch_git, verb, output
+):
+    root = sweep_root.root
+    patch_git.respond_inspect(root, "config", LFS_CONFIG)
+    patch_git.respond_inspect(root, "ls-files", b"a.txt\0")
+    patch_git.respond_inspect(root, verb, output)
+
+    _state, row = probes.read_worktree(root, probes.Budget())
+
+    assert row.coverage == "unscanned"
+    assert row.unscanned == "worktree not readable"
+    assert patch_git.calls == []
+
+
+def test_tracked_paths_reach_check_attr_byte_for_byte(sweep_root, patch_git):
+    root = sweep_root.root
+    paths = b"\xff-not-utf8.txt\0b.txt\0"
+    patch_git.respond_inspect(root, "config", LFS_CONFIG)
+    patch_git.respond_inspect(root, "ls-files", paths)
+    patch_git.respond_inspect(root, "check-attr", b"x\0filter\0unspecified\0" * 2)
+
+    probes.read_worktree(root, probes.Budget())
+
+    check_attr = patch_git.precheck_calls[-1]
+    assert check_attr["args"][0] == "check-attr"
+    assert check_attr["stdin"] == paths
+
+
 # ===========================================================================================
 # R3-B1 (FR-010): the path-B time fields
 # ===========================================================================================
diff --git a/tests/sweep/test_readonly.py b/tests/sweep/test_readonly.py
index f2dc24190..f43a7f811 100644
--- a/tests/sweep/test_readonly.py
+++ b/tests/sweep/test_readonly.py
@@ -59,7 +59,9 @@ class _RunRecorder:
         self.calls.append(
             {"argv": list(argv), "kwargs": kwargs, "env": kwargs.get("env")}
         )
-        return SimpleNamespace(returncode=0, stdout=b"## main\0", stderr=b"")
+        # Only status prints a branch header; the inspections before it (issue 547) see none.
+        stdout = b"## main\0" if argv[6] == "status" else b""
+        return SimpleNamespace(returncode=0, stdout=stdout, stderr=b"")
 
 
 @pytest.fixture
@@ -152,8 +154,12 @@ def test_collect_reaches_git_with_a_lock_free_argv_for_each_worktree(
     _collect(sweep_root, fixed_now)
 
     expected = [sweep_root.root.resolve(), *(p.resolve() for p in others)]
-    assert [c["argv"][3] for c in recorder.calls] == [str(p) for p in expected]
-    for call in recorder.calls:
+    git_calls = [c for c in recorder.calls if c["argv"][0] == "git"]
+    status_calls = [c for c in git_calls if c["argv"][6] == "status"]
+    assert [c["argv"][3] for c in status_calls] == [str(p) for p in expected]
+    # Every worktree is inspected (config) before its one status; no driver, no more calls.
+    assert [c["argv"][6] for c in git_calls] == ["config", "status"] * len(expected)
+    for call in status_calls:
         assert call["argv"][:3] == ["git", "--no-optional-locks", "-C"]
         assert call["argv"][4:6] == ["-c", "core.fsmonitor=false"]
         assert call["argv"][6:] == list(STATUS_ARGS)

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
