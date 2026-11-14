4874fd7e0861dfa267ea57f5d7198aaeb6b225ea
Review one task for spec compliance.

Task brief: ## Task 1: Add real-git regression tests for the git-config routes

Create `tests/sweep/test_git_config_hole.py` (module-level `pytestmark = pytest.mark.integration`). Each test builds a throwaway repository under `tmp_path` with a linked worktree (use `git init -b main`, a seed commit, `git worktree add`, with `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1` and a fixed identity set through `monkeypatch.setenv`, as `_FIXED_IDENTITY` in `tests/sweep/test_readonly.py` does), plants a command that writes a marker file under `tmp_path`, then calls `probes.read_worktree(worktree_path, probes.Budget())` (the real seam, no fake) and asserts the marker file does not exist. Method details are in ./artifacts/experiments/repro.sh, repro2.sh, repro3.sh and repro4.sh; a filter test makes the tracked file stat-dirty with `os.utime` and same-size content so git re-reads it. Cases, each its own test:
- `core.fsmonitor` command in the shared `.git/config`.
- `core.fsmonitor` set through a file named by `include.path`.
- per-worktree `core.fsmonitor` (`extensions.worktreeConfig=true`, then `git config --worktree`).
- `GIT_CONFIG_COUNT`, `GIT_CONFIG_KEY_0`, `GIT_CONFIG_VALUE_0` naming `core.fsmonitor` and the `GIT_CONFIG_PARAMETERS` form, both set with `monkeypatch.setenv`.
- `filter.<d>.clean` with `* filter=<d>` in `.gitattributes` and a tracked file: marker absent and the returned coverage row is `unscanned`.
- `filter.<d>.process`, same shape.
- a filter defined in a submodule's own config with the submodule modified (use `protocol.file.allow=always` for `git submodule add`): marker absent.
- a submodule's own `core.fsmonitor`: marker absent.
- control that must keep working: a filter defined but selected by no tracked path (the way `/etc/gitconfig` defines `lfs`): coverage is `read`, the branch is parsed, and no marker exists.
- positive controls: for the `core.fsmonitor` and filter cases, a plain `git status --porcelain=v1 -z --branch --untracked-files=all` run in the test itself does create the marker, so the test can detect a leak.
The file must not edit any existing test. Save the failing run of the new file to `./artifacts/t1-red.log` (command `uv run pytest tests/sweep/test_git_config_hole.py -q`).

Acceptance criteria:
- tests/sweep/test_git_config_hole.py exists and every route case above is a separate test with a docstring naming its route.
- Run on the unchanged `src/superclaude/cli/sweep/probes.py`, the leak tests (fsmonitor, include, per-worktree, environment, both filter forms, both submodule forms) fail because the marker exists; the unselected-filter control and the positive controls pass. The log ./artifacts/t1-red.log shows this.
- No marker file or temporary repository is left outside `tmp_path`.


Global constraints: 
- Owner design A (2026-11-14): `--ignore-submodules=all` goes into the status template; a submodule's own changes are no longer reported. No new JSON key and no new file other than this package and tests; the refusal reuses the existing `unscanned` source row (`SourceCoverage(name, "unscanned", None, reason)` built by `_failed_worktree` in `src/superclaude/cli/sweep/probes.py`).
- The owner-signed git allow-list (`ALLOWED_GIT`) may change only by the three read-only entries named in Task 2; any other allow-list change is not authorized. `ALLOWED_ORCA` and `FORBIDDEN_TOKENS` stay untouched.
- The git-status scope stays separate from the contract allow-list and the transcript scans: `_worktree_paths` and the shared `paths` list in `collect` are not filtered.
- Out of scope: `CLAUDE.md`, `tests/core/test_claude_md_worktree_rule.py`, anything under `.claude/`, wording or alignment edits, new JSON keys, sidecar files.
- Python only through UV: `uv run pytest tests/sweep -q`, `uv run ruff check`, `uv run ruff format`. Never `python -m`, bare `python`, or `pip`.
- Stage named paths only (`git add -- <paths>`, never `git add -A` or `git add .`); the plan package under `.dev/tasks/` is staged with the T2 commit. Commit locally on the current branch with conventional messages ending with the line `Co-Authored-By: Claude Code <noreply@anthropic.com>`. The executor commits only; it never pushes, opens a PR or writes to GitHub (the owner's session pushes afterwards).
- T2 (Tasks 1 to 5) and T1 (Task 6) are two separate commits. The sweep tests forbid a real subprocess unless a test carries the `integration` mark (`tests/sweep/conftest.py` autouse guard); real-git tests must carry that mark.


Start sha: 4874fd7e0861dfa267ea57f5d7198aaeb6b225ea
Diff against the start snapshot: diff --git a/tests/sweep/test_git_config_hole.py b/tests/sweep/test_git_config_hole.py
new file mode 100644
index 000000000..406a35f50
--- /dev/null
+++ b/tests/sweep/test_git_config_hole.py
@@ -0,0 +1,263 @@
+"""Issue 547: a sweep ``git status`` must not run a program that repository configuration
+or the inherited environment names.
+
+Each test plants a command that writes a marker file, proves with a plain ``git status``
+that the plant works (the positive control), then runs the sweep's own reader
+(``probes.read_worktree``, real git, no fake) and asserts the marker never appears.
+"""
+
+from __future__ import annotations
+
+import os
+import subprocess
+from pathlib import Path
+
+import pytest
+
+from superclaude.cli.sweep import probes
+
+integration = pytest.mark.integration
+
+PLAIN_STATUS = ["status", "--porcelain=v1", "-z", "--branch", "--untracked-files=all"]
+FILTER_REASON = "git filter could run a program"
+
+
+@pytest.fixture(autouse=True)
+def _isolated_git(monkeypatch):
+    """No host config, no inherited GIT_CONFIG_* keys, a fixed identity."""
+    for key in ("GIT_CONFIG_COUNT", "GIT_CONFIG_PARAMETERS"):
+        monkeypatch.delenv(key, raising=False)
+    for n in range(8):
+        monkeypatch.delenv(f"GIT_CONFIG_KEY_{n}", raising=False)
+        monkeypatch.delenv(f"GIT_CONFIG_VALUE_{n}", raising=False)
+    for key, value in {
+        "GIT_CONFIG_GLOBAL": "/dev/null",
+        "GIT_CONFIG_NOSYSTEM": "1",
+        "GIT_AUTHOR_NAME": "Sweep Test",
+        "GIT_AUTHOR_EMAIL": "sweep-test@example.com",
+        "GIT_COMMITTER_NAME": "Sweep Test",
+        "GIT_COMMITTER_EMAIL": "sweep-test@example.com",
+        "GIT_TERMINAL_PROMPT": "0",
+        "LC_ALL": "C",
+    }.items():
+        monkeypatch.setenv(key, value)
+
+
+def git(cwd: Path, *args: str) -> str:
+    proc = subprocess.run(
+        ["git", "-C", str(cwd), *args],
+        capture_output=True,
+        text=True,
+        timeout=60,
+        check=True,
+    )
+    return proc.stdout
+
+
+def make_repo(tmp_path: Path) -> tuple[Path, Path, Path]:
+    """A main repository with one commit, a linked worktree and a marker path."""
+    main = tmp_path / "main"
+    main.mkdir()
+    git(main, "init", "-q", "-b", "main")
+    (main / "f.txt").write_text("aaaa\n")
+    git(main, "add", "f.txt")
+    git(main, "commit", "-q", "-m", "seed")
+    wt = tmp_path / "wt"
+    git(main, "worktree", "add", "-q", str(wt), "-b", "wtb")
+    return main, wt, tmp_path / "marker"
+
+
+def make_stat_dirty(path: Path) -> None:
+    """Same bytes, newer mtime: git must re-read the file (and run a clean filter)."""
+    st = path.stat()
+    os.utime(path, ns=(st.st_atime_ns, st.st_mtime_ns + 5_000_000_000))
+
+
+def hook(marker: Path) -> str:
+    return f"touch {marker}; echo"
+
+
+def plain_status(wt: Path) -> None:
+    subprocess.run(
+        ["git", "-C", str(wt), *PLAIN_STATUS],
+        capture_output=True,
+        timeout=60,
+        check=False,
+    )
+
+
+def assert_plant_works(wt: Path, marker: Path) -> None:
+    """Positive control: an unguarded status does run the planted command."""
+    plain_status(wt)
+    assert marker.exists(), "control failed: the plant did not run on a plain status"
+    marker.unlink()
+
+
+def sweep_read(wt: Path):
+    return probes.read_worktree(wt, probes.Budget())
+
+
+@integration
+def test_fsmonitor_in_shared_config_does_not_run(tmp_path):
+    """Route 1: core.fsmonitor in the shared .git/config."""
+    main, wt, marker = make_repo(tmp_path)
+    git(main, "config", "core.fsmonitor", hook(marker))
+    assert_plant_works(wt, marker)
+
+    sweep_read(wt)
+
+    assert not marker.exists()
+
+
+@integration
+def test_fsmonitor_through_include_path_does_not_run(tmp_path):
+    """Route 4: include.path pulls in a file that sets core.fsmonitor."""
+    main, wt, marker = make_repo(tmp_path)
+    inc = tmp_path / "inc.cfg"
+    inc.write_text(f"[core]\n\tfsmonitor = {hook(marker)}\n")
+    git(main, "config", "include.path", str(inc))
+    assert_plant_works(wt, marker)
+
+    sweep_read(wt)
+
+    assert not marker.exists()
+
+
+@integration
+def test_per_worktree_fsmonitor_does_not_run(tmp_path):
+    """Route 5: per-worktree config (extensions.worktreeConfig)."""
+    main, wt, marker = make_repo(tmp_path)
+    git(main, "config", "extensions.worktreeConfig", "true")
+    git(wt, "config", "--worktree", "core.fsmonitor", hook(marker))
+    assert_plant_works(wt, marker)
+
+    sweep_read(wt)
+
+    assert not marker.exists()
+
+
+@integration
+def test_fsmonitor_from_git_config_count_env_does_not_run(tmp_path, monkeypatch):
+    """Route 6: GIT_CONFIG_COUNT / KEY_0 / VALUE_0 name core.fsmonitor."""
+    _main, wt, marker = make_repo(tmp_path)
+    monkeypatch.setenv("GIT_CONFIG_COUNT", "1")
+    monkeypatch.setenv("GIT_CONFIG_KEY_0", "core.fsmonitor")
+    monkeypatch.setenv("GIT_CONFIG_VALUE_0", hook(marker))
+    assert_plant_works(wt, marker)
+
+    sweep_read(wt)
+
+    assert not marker.exists()
+
+
+@integration
+def test_fsmonitor_from_git_config_parameters_env_does_not_run(tmp_path, monkeypatch):
+    """Route 6b: the GIT_CONFIG_PARAMETERS form of the environment route."""
+    _main, wt, marker = make_repo(tmp_path)
+    monkeypatch.setenv("GIT_CONFIG_PARAMETERS", f"'core.fsmonitor={hook(marker)}'")
+    assert_plant_works(wt, marker)
+
+    sweep_read(wt)
+
+    assert not marker.exists()
+
+
+def _select_filter(main: Path, wt: Path, name: str) -> None:
+    """Track a file and a .gitattributes that selects driver ``name``; no config yet."""
+    (wt / ".gitattributes").write_text(f"* filter={name}\n")
+    git(wt, "add", ".gitattributes")
+    git(wt, "commit", "-q", "-m", "select filter")
+
+
+@integration
+def test_filter_clean_selected_by_a_tracked_path_does_not_run(tmp_path):
+    """Route 2: filter.<d>.clean selected by a tracked path; the worktree is unscanned."""
+    main, wt, marker = make_repo(tmp_path)
+    _select_filter(main, wt, "x")
+    git(main, "config", "filter.x.clean", f"sh -c 'touch {marker}; cat'")
+    make_stat_dirty(wt / "f.txt")
+    assert_plant_works(wt, marker)
+    make_stat_dirty(wt / "f.txt")
+
+    _state, row = sweep_read(wt)
+
+    assert not marker.exists()
+    assert row.coverage == "unscanned"
+    assert row.unscanned == FILTER_REASON
+
+
+@integration
+def test_filter_process_selected_by_a_tracked_path_does_not_run(tmp_path):
+    """Route 3: filter.<d>.process selected by a tracked path; the worktree is unscanned."""
+    main, wt, marker = make_repo(tmp_path)
+    _select_filter(main, wt, "x")
+    git(main, "config", "filter.x.process", f"touch {marker}")
+    make_stat_dirty(wt / "f.txt")
+    assert_plant_works(wt, marker)
+    make_stat_dirty(wt / "f.txt")
+
+    _state, row = sweep_read(wt)
+
+    assert not marker.exists()
+    assert row.coverage == "unscanned"
+    assert row.unscanned == FILTER_REASON
+
+
+@integration
+def test_filter_defined_but_selected_by_no_path_is_still_read(tmp_path):
+    """Control: a filter defined (as /etc/gitconfig defines lfs) but selected by nothing."""
+    main, wt, marker = make_repo(tmp_path)
+    git(main, "config", "filter.lfs.clean", f"sh -c 'touch {marker}; cat'")
+    git(main, "config", "filter.lfs.process", f"touch {marker}")
+    make_stat_dirty(wt / "f.txt")
+
+    _state, row = sweep_read(wt)
+
+    assert not marker.exists()
+    assert row.coverage == "read"
+    assert row.unscanned is None
+
+
+def _add_submodule(main: Path, wt: Path, tmp_path: Path) -> Path:
+    src = tmp_path / "subsrc"
+    src.mkdir()
+    git(src, "init", "-q", "-b", "main")
+    (src / "s.txt").write_text("s\n")
+    git(src, "add", "s.txt")
+    git(src, "commit", "-q", "-m", "s")
+    git(main, "-c", "protocol.file.allow=always", "submodule", "add", "-q", str(src), "sub")
+    git(main, "commit", "-q", "-m", "add sub")
+    git(wt, "merge", "-q", "main")
+    git(wt, "-c", "protocol.file.allow=always", "submodule", "update", "--init", "-q")
+    return wt / "sub"
+
+
+@integration
+def test_submodule_fsmonitor_does_not_run(tmp_path):
+    """Route 8: a submodule's own core.fsmonitor (the outer status starts a child status)."""
+    main, wt, marker = make_repo(tmp_path)
+    sub = _add_submodule(main, wt, tmp_path)
+    git(sub, "config", "core.fsmonitor", hook(marker))
+    (sub / "s.txt").write_text("changed\n")
+    assert_plant_works(wt, marker)
+
+    sweep_read(wt)
+
+    assert not marker.exists()
+
+
+@integration
+def test_submodule_local_filter_does_not_run(tmp_path):
+    """Route 9: a filter named only in the submodule's own config."""
+    main, wt, marker = make_repo(tmp_path)
+    sub = _add_submodule(main, wt, tmp_path)
+    (sub / ".gitattributes").write_text("* filter=y\n")
+    git(sub, "config", "filter.y.clean", f"sh -c 'touch {marker}; cat'")
+    (sub / "s.txt").write_text("t\n")
+    make_stat_dirty(sub / "s.txt")
+    assert_plant_works(wt, marker)
+    make_stat_dirty(sub / "s.txt")
+
+    sweep_read(wt)
+
+    assert not marker.exists()

=== evidence file artifacts/t1-red.log (package-relative ./artifacts/t1-red.log) ===
============================= test session starts ==============================
platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
SuperClaude: 5.0.0
rootdir: /home/coder/workspaces/worktrees/IronClaude/sweep-git-fix
configfile: pyproject.toml
plugins: superclaude-5.0.0, anyio-4.16.0
collected 10 items

tests/sweep/test_git_config_hole.py FFFFFFF.FF                           [100%]

=================================== FAILURES ===================================
_________________ test_fsmonitor_in_shared_config_does_not_run _________________
tests/sweep/test_git_config_hole.py:109: in test_fsmonitor_in_shared_config_does_not_run
    assert not marker.exists()
E   AssertionError: assert not True
E    +  where True = exists()
E    +    where exists = PosixPath('/tmp/pytest-of-coder/pytest-98/test_fsmonitor_in_shared_confi0/marker').exists
_______________ test_fsmonitor_through_include_path_does_not_run _______________
tests/sweep/test_git_config_hole.py:123: in test_fsmonitor_through_include_path_does_not_run
    assert not marker.exists()
E   AssertionError: assert not True
E    +  where True = exists()
E    +    where exists = PosixPath('/tmp/pytest-of-coder/pytest-98/test_fsmonitor_through_include0/marker').exists
___________________ test_per_worktree_fsmonitor_does_not_run ___________________
tests/sweep/test_git_config_hole.py:136: in test_per_worktree_fsmonitor_does_not_run
    assert not marker.exists()
E   AssertionError: assert not True
E    +  where True = exists()
E    +    where exists = PosixPath('/tmp/pytest-of-coder/pytest-98/test_per_worktree_fsmonitor_do0/marker').exists
____________ test_fsmonitor_from_git_config_count_env_does_not_run _____________
tests/sweep/test_git_config_hole.py:150: in test_fsmonitor_from_git_config_count_env_does_not_run
    assert not marker.exists()
E   AssertionError: assert not True
E    +  where True = exists()
E    +    where exists = PosixPath('/tmp/pytest-of-coder/pytest-98/test_fsmonitor_from_git_config0/marker').exists
__________ test_fsmonitor_from_git_config_parameters_env_does_not_run __________
tests/sweep/test_git_config_hole.py:162: in test_fsmonitor_from_git_config_parameters_env_does_not_run
    assert not marker.exists()
E   AssertionError: assert not True
E    +  where True = exists()
E    +    where exists = PosixPath('/tmp/pytest-of-coder/pytest-98/test_fsmonitor_from_git_config1/marker').exists
__________ test_filter_clean_selected_by_a_tracked_path_does_not_run ___________
tests/sweep/test_git_config_hole.py:184: in test_filter_clean_selected_by_a_tracked_path_does_not_run
    assert not marker.exists()
E   AssertionError: assert not True
E    +  where True = exists()
E    +    where exists = PosixPath('/tmp/pytest-of-coder/pytest-98/test_filter_clean_selected_by_0/marker').exists
_________ test_filter_process_selected_by_a_tracked_path_does_not_run __________
tests/sweep/test_git_config_hole.py:201: in test_filter_process_selected_by_a_tracked_path_does_not_run
    assert not marker.exists()
E   AssertionError: assert not True
E    +  where True = exists()
E    +    where exists = PosixPath('/tmp/pytest-of-coder/pytest-98/test_filter_process_selected_b0/marker').exists
____________________ test_submodule_fsmonitor_does_not_run _____________________
tests/sweep/test_git_config_hole.py:246: in test_submodule_fsmonitor_does_not_run
    assert not marker.exists()
E   AssertionError: assert not True
E    +  where True = exists()
E    +    where exists = PosixPath('/tmp/pytest-of-coder/pytest-98/test_submodule_fsmonitor_does_0/marker').exists
___________________ test_submodule_local_filter_does_not_run ___________________
tests/sweep/test_git_config_hole.py:263: in test_submodule_local_filter_does_not_run
    assert not marker.exists()
E   AssertionError: assert not True
E    +  where True = exists()
E    +    where exists = PosixPath('/tmp/pytest-of-coder/pytest-98/test_submodule_local_filter_do0/marker').exists
=========================== short test summary info ============================
FAILED tests/sweep/test_git_config_hole.py::test_fsmonitor_in_shared_config_does_not_run
FAILED tests/sweep/test_git_config_hole.py::test_fsmonitor_through_include_path_does_not_run
FAILED tests/sweep/test_git_config_hole.py::test_per_worktree_fsmonitor_does_not_run
FAILED tests/sweep/test_git_config_hole.py::test_fsmonitor_from_git_config_count_env_does_not_run
FAILED tests/sweep/test_git_config_hole.py::test_fsmonitor_from_git_config_parameters_env_does_not_run
FAILED tests/sweep/test_git_config_hole.py::test_filter_clean_selected_by_a_tracked_path_does_not_run
FAILED tests/sweep/test_git_config_hole.py::test_filter_process_selected_by_a_tracked_path_does_not_run
FAILED tests/sweep/test_git_config_hole.py::test_submodule_fsmonitor_does_not_run
FAILED tests/sweep/test_git_config_hole.py::test_submodule_local_filter_does_not_run
========================= 9 failed, 1 passed in 0.94s ==========================

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
