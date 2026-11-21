a1b599d43a85246ed89a2421040ce82e35134d50
Review one task for spec compliance.

Task brief: ## Task 7: Build the test support and the "facts the tests keep true" checks

Depends on: Task 6

Extend `tests/worktree_cleanup/conftest.py` (first created by Task 2) and create the shared `tests/worktree_cleanup/fixtures/` set and `tests/worktree_cleanup/test_git_facts.py` (new; layout as `tests/merged_pr_log/` has `__init__.py`, `fixtures/` and one test module that loads the script with `importlib.util.spec_from_file_location`). `conftest.py` provides: a loader of `scripts/worktree_cleanup.py`; a recording runner built on the script's `Runner` that answers `gh`, `orca` and `branch-landed.sh` from canned replies and runs real `git`, `tar` and `xargs` only inside throwaway folders under `tmp_path`; a builder for a throwaway repository with real linked worktrees (a clean one, one with a tracked edit, one with untracked and ignored `.dev/` files, one with an ignored environment file, one with only build output, one with a detached HEAD, a locked one) whose `origin` points at a local bare repository, and a second local bare repository standing in for the evidence repo; a fake `/proc` builder. `fixtures/` holds JSON in the recorded shape of `gh pr list`, `gh pr view`, `gh issue view`, `orca repo list`, `orca worktree ps --json`, `orca reference list` and `orca terminal list`; a README line in the module docstring says the shapes are hand-written from the spec and the Orca help, not literal captures (as `tests/merged_pr_log/test_merged_pr_log.py` says). `test_git_facts.py` keeps true the facts of source section 9 "Facts the tests keep true" in a throwaway repository: `git worktree remove` without force refuses a worktree with an untracked file and one with a modified tracked file and removes one that holds only ignored files; `git branch -d` refuses after a squash merge (the script's "branch kept" reporting is asserted in Task 13); `git clean -f -x --` with literal pathspecs removes exactly the listed files (including a name with a space) and leaves unlisted untracked and ignored files and tracked files alone. Use obvious placeholders for any token-shaped value, never a real one.

Acceptance criteria:
- `uv run pytest tests/worktree_cleanup/test_git_facts.py -v` passes using only `tmp_path` repositories; no test touches a real worktree.
- The recording runner exposes the full list of commands it was asked to run, and refuses (raises) any command the real `Runner.check_allowed` would refuse.
- The fixtures folder holds one recorded shape for each of the seven replies listed above.
- The three git facts are asserted, including the file name with a space.

AC ids (in source order): T7.AC1, T7.AC2, T7.AC3, T7.AC4
Global constraints: ## Constraints

- Safety for this whole run (set by the issue owner): tests use throwaway git repositories, a local bare repository standing in for the evidence repo, and a fake runner with recorded `gh`, `git` and `orca` replies. No task and no test runs the script with `--apply` against real worktrees, removes, moves or clears any real worktree or file, creates or switches on an Orca automation (the definition is a file, status "written, not switched on"), closes a real Orca terminal, or pushes to `IronbellyOrg/run-evidence`. The only run against the real workspace is a dry run (Task 20).
- The script never uses `--force` on `orca worktree rm` or `git worktree remove`, never `git branch -D`, never `rm`, never `git worktree prune`, never pushes anywhere but the evidence repo's clone, and never deletes a remote branch. The only force flag in the whole script is `git clean -f -x --` on exact paths listed in a verified `saved-paths.txt` (source sections 3, 6 and 8, decision 1).
- The script never deletes a file or folder itself (no `rm`, no `shutil.rmtree`, no `unlink`): its lock files stay in place under `fcntl.flock`, and a scratch folder left by a failed save stays and is named in the log. This plan chose that so "never rm" holds without exception.
- Python standard library only, no model call, no agent or model name in any output, credentials only from the environment (`GH_TOKEN`), no credential file is ever opened by the script, no secret is printed or written (source sections 5, 6 and 9).
- The 11 decisions of source section 8 are final. Out of scope (source section 10): where worktrees live (#289, #322), Jay's other pieces, the closeout itself (#668, so `/sc:closeout` and its files and tests are not changed), any shared or remote branch, anything that is not a git worktree of our repos.
- The change to the separate `IronbellyOrg/run-evidence` repo (source section 15, step 5) is prepared as text under `./artifacts/` and not applied by this plan; no other repo is pushed to.
- The spec mentions that `archive` by hand "can still save" tracked edits and later commits "as a patch and a bundle" (source section 7, "What is not saved"). It gives no step, format or folder for it, so it is not built; Task 12 records that in the verb's help text so it is not a silent drop.
- Where the spec is silent this plan decides, and says so in the task: `/sc:worktrees` goes on the never-as-worker list (Task 16); outside an IronClaude checkout the command stops and runs nothing (Task 14); the default `--out` folder is `~/.local/state/worktree-cleanup` so nothing is ever written inside a worktree (Task 2); `/sc:closeout` is left unchanged (this constraint).
- Edit only under `src/superclaude/`, `scripts/`, `tests/`, `docs/`, `plugins/superclaude/skills/sc-recommend/refs/`, `CHANGELOG.md` and `NOTICE`; run `make sync-dev` after editing `src/superclaude/` and never edit the `.claude/` copies. Plain English and no em or en dashes in every new file. A command file must not point at another primitive through a `src/superclaude/...` path.
- The pull request for this change is opened by the finishing step of the run, `/sc:pr-submit --monitor 3` (source section 15, step 7), after the last task; no task of this plan opens it.
- Corrections the implementer made to this plan before the first task started, from the advisory reflect review of the plan (the list is in `./artifacts/plan-corrections.md`): Task 1 (the item 1 fallback, the open pull request proof, item 7), Task 2 (a positive allowlist runner and its own first tests), Tasks 3 to 5 (their own tests, so no check waits for a later task), Task 7 (shared fixtures only), Tasks 11 and 12 (Orca read back, the command list in the JSON), Task 14 (the write-verb classification), Task 19 (15 rows), Task 20 (dependencies).
Start sha: a1b599d43a85246ed89a2421040ce82e35134d50
Diff against the start snapshot: diff --git a/tests/worktree_cleanup/conftest.py b/tests/worktree_cleanup/conftest.py
deleted file mode 100644
index 7de106a78..000000000
--- a/tests/worktree_cleanup/conftest.py
+++ /dev/null
@@ -1,144 +0,0 @@
-"""Shared test support for scripts/worktree_cleanup.py.
-
-Tests never touch a real worktree: git runs only on throwaway repositories under
-``tmp_path``, and ``gh``, ``orca`` and the landed-check helper are answered from
-canned replies by the recording runner below. The reply shapes are hand-written from
-the spec and the tool help, not literal captures of live output.
-"""
-
-from __future__ import annotations
-
-import importlib.util
-import os
-import subprocess
-import sys
-from pathlib import Path
-
-import pytest
-
-ROOT = Path(__file__).resolve().parents[2]
-SCRIPT = ROOT / "scripts" / "worktree_cleanup.py"
-
-# A made-up lookup location for the landed check: no real file is read or run from it.
-LANDED = "/h/.claude/skills/sc-closeout-protocol/scripts/branch-landed.sh"
-
-
-def load_script():
-    spec = importlib.util.spec_from_file_location("worktree_cleanup", SCRIPT)
-    mod = importlib.util.module_from_spec(spec)
-    sys.modules["worktree_cleanup"] = mod
-    spec.loader.exec_module(mod)
-    return mod
-
-
-@pytest.fixture(scope="session")
-def wc():
-    """The script module, loaded once."""
-    return load_script()
-
-
-@pytest.fixture(scope="session")
-def runner_cls(wc):
-    """A Runner whose outside programs are answered from canned replies.
-
-    ``replies`` maps a program name (``gh``, ``orca``, ``bash``) to a callable
-    ``(argv, cwd) -> Result | None``. ``git``, ``tar`` and ``xargs`` really run when
-    ``real_git`` is true (on throwaway folders only). A command with no canned reply
-    gets exit code 127 and is never started.
-    """
-
-    class RecordingRunner(wc.Runner):
-        def __init__(
-            self, replies=None, real_git=True, evidence_dir=None, landed_paths=(LANDED,)
-        ):
-            super().__init__(
-                evidence_dir=evidence_dir, landed_paths=tuple(landed_paths)
-            )
-            self.replies = dict(replies or {})
-            self.real_git = real_git
-
-        def _execute(self, argv, cwd, stdin):
-            prog = os.path.basename(argv[0])
-            handler = self.replies.get(prog)
-            if handler is not None:
-                answer = handler(argv, cwd)
-                if answer is not None:
-                    return answer
-            if prog in ("git", "tar", "xargs") and self.real_git:
-                return super()._execute(argv, cwd, stdin)
-            return wc.Result(127, "", f"no canned reply for {argv}")
-
-    return RecordingRunner
-
-
-class NeverRun:
-    """A reply table whose handlers fail the test if a process would start."""
-
-    def __getitem__(self, key):  # pragma: no cover - used only on failure
-        raise AssertionError(f"a process would have started: {key}")
-
-
-@pytest.fixture
-def never_run_runner(runner_cls, tmp_path):
-    """A runner that raises if a command is actually executed."""
-
-    class Guard(runner_cls):
-        def _execute(self, argv, cwd, stdin):
-            raise AssertionError(f"command reached execution: {argv}")
-
-    return Guard(evidence_dir=str(tmp_path / "evidence"))
-
-
-# --- a throwaway repository --------------------------------------------------------
-
-GITIGNORE = ".dev/local/\n.env\n__pycache__/\n.venv/\n"
-
-
-def git_in(cwd, *args):
-    """Run git on a throwaway repository only (never on a real worktree)."""
-    env = dict(os.environ)
-    env.update(
-        GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_NOSYSTEM="1", GIT_TERMINAL_PROMPT="0"
-    )
-    ident = ["-c", "user.name=t", "-c", "user.email=t@example.invalid"]
-    done = subprocess.run(
-        ["git", *ident, *args],
-        cwd=cwd,
-        env=env,
-        check=True,
-        capture_output=True,
-        text=True,
-    )
-    return done.stdout
-
-
-class ThrowawayRepo:
-    """A repository under ``tmp_path`` with an ``origin`` URL that is never contacted."""
-
-    def __init__(
-        self, root: Path, origin="https://github.com/IronbellyOrg/example.git"
-    ):
-        self.root = root
-        self.main = root / "main"
-        self.main.mkdir(parents=True)
-        git_in(self.main, "init", "-q", "-b", "main")
-        (self.main / ".gitignore").write_text(GITIGNORE, encoding="utf-8")
-        (self.main / "README.md").write_text("example\n", encoding="utf-8")
-        git_in(self.main, "add", "-A")
-        git_in(self.main, "commit", "-q", "-m", "first")
-        git_in(self.main, "remote", "add", "origin", origin)
-        # more ignored names, kept out of the tracked .gitignore so no test edits a tracked file
-        exclude = self.main / ".git" / "info" / "exclude"
-        with exclude.open("a", encoding="utf-8") as handle:
-            handle.write("node_modules/\ndist/\n.claude/agents/\n.serena/cache/\n")
-
-    def add_worktree(self, name: str) -> Path:
-        path = self.root / "wts" / name
-        path.parent.mkdir(exist_ok=True)
-        git_in(self.main, "worktree", "add", "-q", "-b", name, str(path))
-        return path
-
-
-@pytest.fixture
-def throwaway_repo(tmp_path):
-    return ThrowawayRepo(tmp_path / "repo")
diff --git a/tests/worktree_cleanup/fixtures/README.md b/tests/worktree_cleanup/fixtures/README.md
deleted file mode 100644
index e89fa8375..000000000
--- a/tests/worktree_cleanup/fixtures/README.md
+++ /dev/null
@@ -1,15 +0,0 @@
-# Fixtures for the worktree cleanup tests
-
-Every file here is a small made-up reply, written by hand. None is a capture of a real
-workspace: the paths, ids, titles and numbers are examples.
-
-- `orca_worktree_ps.json`: the shape of `orca worktree ps --json` (a reply envelope with
-  `ok` and `result.worktrees`). The field names are the ones seen in a real reply during the
-  survey for issue 687 (`worktreeId`, `path`, `lastActivityAt`, `isPinned`,
-  `liveTerminalCount`, `linkedPR`, `comment`); the values are not.
-- `orca_repo_list.json`, `orca_reference_list.json`, `orca_terminal_list.json`: the same
-  envelope with `result.repos`, `result.references` and `result.terminals`. These three
-  shapes are UNVERIFIED against a real reply (no real one was captured), so the parsers read
-  them tolerantly and report "Orca unavailable" for anything else.
-
-Later tasks reuse these files; do not put a real path, name or token in them.
diff --git a/tests/worktree_cleanup/test_facts.py b/tests/worktree_cleanup/test_facts.py
deleted file mode 100644
index ed7452bde..000000000
--- a/tests/worktree_cleanup/test_facts.py
+++ /dev/null
@@ -1,1073 +0,0 @@
-"""Facts the script reads: Orca (Task 3), then git and GitHub (Tasks 4 and 5).
-
-Orca replies come from the hand-written files in ``fixtures/``; no real Orca is started.
-"""
-
-from __future__ import annotations
-
-import ast
-import inspect
-import json
-from pathlib import Path
-
-import pytest
-
-FIXTURES = Path(__file__).parent / "fixtures"
-
-
-def fixture_text(name: str) -> str:
-    return (FIXTURES / name).read_text(encoding="utf-8")
-
-
-# --- Task 3: Orca, read only ----------------------------------------------------
-
-
-def test_repo_list_fixture_gives_id_path_and_name(wc):
-    read = wc.parse_orca_repos(fixture_text("orca_repo_list.json"))
-    assert read.ok and read.unavailable is None
-    assert [(r.name, r.path) for r in read.items] == [
-        ("IronClaude", "/work/example/IronClaude"),
-        ("Coder", "/work/example/Coder"),
-    ]
-    assert all(r.id for r in read.items)
-
-
-def test_worktree_ps_fixture_gives_every_named_field(wc):
-    read = wc.parse_orca_worktrees(fixture_text("orca_worktree_ps.json"))
-    assert read.ok
-    main, pinned, third = read.items
-    assert main.selector == "id:" + main.worktree_id
-    assert main.worktree_id.endswith("::/work/example/IronClaude")
-    assert main.path == "/work/example/IronClaude"
-    assert main.last_activity_ms == 1795095396714
-    assert main.is_pinned is False and main.live_terminal_count == 2
-    assert main.linked_pr_hint["state"] == "merged"
-    assert main.comment == ""
-    assert pinned.is_pinned is True and pinned.comment.startswith("keep until")
-    assert pinned.linked_pr_hint is None and pinned.live_terminal_count == 0
-    # a missing lastActivityAt and a null comment are accepted
-    assert third.last_activity_ms is None and third.comment == ""
-    assert third.linked_pr_hint["state"] == "open"
-
-
-def test_reference_and_terminal_fixtures(wc):
-    refs = wc.parse_orca_references(fixture_text("orca_reference_list.json"))
-    assert refs.ok and [r.raw["number"] for r in refs.items] == [687, 700]
-    terms = wc.parse_orca_terminals(fixture_text("orca_terminal_list.json"))
-    assert terms.ok
-    assert [t.handle for t in terms.items] == ["term_example_1", "term_example_2"]
-    assert terms.items[0].title == "claude"
-
-
-def test_empty_lists_are_a_valid_answer(wc):
-    for parse, key in (
-        (wc.parse_orca_repos, "repos"),
-        (wc.parse_orca_worktrees, "worktrees"),
-        (wc.parse_orca_references, "references"),
-        (wc.parse_orca_terminals, "terminals"),
-    ):
-        read = parse(json.dumps({"ok": True, "result": {key: []}}))
-        assert read.ok and read.items == ()
-
-
-def _ps_with(**change):
-    doc = json.loads(fixture_text("orca_worktree_ps.json"))
-    doc["result"]["worktrees"][0].update(change)
-    return json.dumps(doc)
-
-
-MALFORMED = [
-    ("repos", "not json at all"),
-    ("repos", ""),
-    ("repos", "null"),
-    ("repos", "[1, 2]"),
-    ("repos", '{"ok": false, "error": "boom"}'),
-    ("repos", '{"ok": true, "result": {"worktrees": []}}'),
-    ("repos", '{"ok": true, "result": {"repos": [{"id": "x"}]}}'),
-    ("repos", '{"ok": true, "result": {"repos": "no"}}'),
-    ("worktrees", '{"ok": true, "result": {"worktrees": [{"path": "/x"}]}}'),
-    ("worktrees", _ps_with(isPinned="no")),
-    ("worktrees", _ps_with(liveTerminalCount=-1)),
-    ("worktrees", _ps_with(liveTerminalCount=True)),
-    ("worktrees", _ps_with(liveTerminalCount="2")),
-    ("worktrees", _ps_with(lastActivityAt="yesterday")),
-    ("worktrees", _ps_with(linkedPR="merged")),
-    ("worktrees", _ps_with(comment=5)),
-    ("worktrees", _ps_with(path="")),
-    ("references", '{"ok": true, "result": {"terminals": []}}'),
-    ("references", '{"ok": true, "result": {"references": [1]}}'),
-    ("terminals", '{"ok": true, "result": {"terminals": [{"title": "x"}]}}'),
-    ("terminals", "{"),
-]
-
-
-@pytest.mark.parametrize(
-    "kind,text", MALFORMED, ids=[f"{k}-{i}" for i, (k, _) in enumerate(MALFORMED)]
-)
-def test_a_malformed_reply_is_orca_unavailable_not_an_exception(wc, kind, text):
-    parse = {
-        "repos": wc.parse_orca_repos,
-        "worktrees": wc.parse_orca_worktrees,
-        "references": wc.parse_orca_references,
-        "terminals": wc.parse_orca_terminals,
-    }[kind]
-    read = parse(text)
-    assert read.ok is False and read.items == ()
-    assert read.unavailable.startswith("Orca unavailable: ")
-
-
-# --- the reads go through the runner ----------------------------------------------
-
-
-@pytest.fixture
-def orca_runner(wc, runner_cls):
-    """Build a runner whose Orca answers come from ``{argv tuple: stdout or (code, stdout)}``."""
-
-    def build(replies):
-        def handler(argv, cwd):
-            answer = replies.get(tuple(argv))
-            if answer is None:
-                return None
-            code, out = answer if isinstance(answer, tuple) else (0, answer)
-            return wc.Result(code, out, "")
-
-        return runner_cls(replies={"orca": handler})
-
-    return build
-
-
-SEL = "id:11111111-1111-4111-8111-111111111111::/work/example/IronClaude"
-
-
-def test_each_read_issues_only_its_read_verb_and_returns_rows(wc, orca_runner):
-    runner = orca_runner(
-        {
-            ("orca", "repo", "list", "--json"): fixture_text("orca_repo_list.json"),
-            ("orca", "worktree", "ps", "--json"): fixture_text("orca_worktree_ps.json"),
-            (
-                "orca",
-                "reference",
-                "list",
-                "--worktree",
-                SEL,
-                "--json",
-            ): fixture_text("orca_reference_list.json"),
-            (
-                "orca",
-                "terminal",
-                "list",
-                "--worktree",
-                SEL,
-                "--json",
-            ): fixture_text("orca_terminal_list.json"),
-        }
-    )
-    assert wc.read_orca_repos(runner).ok
-    worktrees = wc.read_orca_worktrees(runner)
-    assert worktrees.ok and worktrees.items[0].selector == SEL
-    assert wc.read_orca_references(runner, SEL).ok
-    assert wc.read_orca_terminals(runner, SEL).ok
-    verbs = [tuple(c.argv[1:3]) for c in runner.commands]
-    assert verbs == [
-        ("repo", "list"),
-        ("worktree", "ps"),
-        ("reference", "list"),
-        ("terminal", "list"),
-    ]
-    flat = [t for c in runner.commands for t in c.argv]
-    assert "close" not in flat and "rm" not in flat and "--force" not in flat
-
-
-def test_a_failed_or_unanswered_read_is_orca_unavailable(wc, orca_runner):
-    runner = orca_runner({("orca", "worktree", "ps", "--json"): (1, "")})
-    read = wc.read_orca_worktrees(runner)
-    assert read.ok is False and "exited with 1" in read.unavailable
-    # no canned reply at all: the recording runner answers 127, as a missing program would
-    assert wc.read_orca_repos(runner).unavailable.startswith("Orca unavailable")
-    # a clean exit with a broken body
-    runner = orca_runner({("orca", "worktree", "ps", "--json"): "<html>"})
-    assert wc.read_orca_worktrees(runner).unavailable.startswith("Orca unavailable")
-
-
-def test_repo_list_falls_back_to_the_current_checkout_and_says_so(wc):
-    current = wc.OrcaRepo("current", "/work/example/IronClaude", "IronClaude")
-    good = wc.parse_orca_repos(fixture_text("orca_repo_list.json"))
-    repos, note = wc.repos_or_current(good, current)
-    assert [r.name for r in repos] == ["IronClaude", "Coder"] and note == ""
-    bad = wc.parse_orca_repos("nope")
-    repos, note = wc.repos_or_current(bad, current)
-    assert repos == [current]
-    assert "Orca unavailable" in note and "current checkout" in note
-
-
-# --- guard rails of Task 3 -------------------------------------------------------------
-
-
-def test_the_read_functions_never_name_a_close_or_remove_verb(wc):
-    for fn in (
-        wc.read_orca_repos,
-        wc.read_orca_worktrees,
-        wc.read_orca_references,
-        wc.read_orca_terminals,
-        wc._orca_read,
-    ):
-        src = inspect.getsource(fn)
-        for word in ('"close"', '"rm"', '"--force"', '"create"'):
-            assert word not in src, (fn.__name__, word)
-
-
-def test_linked_pr_hint_is_read_by_no_rule_function(wc):
-    """Only the parser sets it; nothing else in the script reads it as proof of a merge."""
-    tree = ast.parse(Path(wc.__file__).read_text(encoding="utf-8"))
-    readers = []
-    for fn in ast.walk(tree):
-        if isinstance(fn, ast.FunctionDef):
-            for node in ast.walk(fn):
-                if isinstance(node, ast.Attribute) and node.attr == "linked_pr_hint":
-                    readers.append(fn.name)
-    assert readers == []
-    # the field is still part of the record
-    assert "linked_pr_hint" in {f for f in wc.OrcaWorktree.__dataclass_fields__}
-    assert "linkedPR" in Path(wc.__file__).read_text(encoding="utf-8")
-
-
-def test_no_dash_characters_in_the_fixtures():
-    for path in FIXTURES.iterdir():
-        text = path.read_text(encoding="utf-8")
-        assert chr(0x2013) not in text and chr(0x2014) not in text, path
-
-
-# --- Task 4: git facts, local state and the process scan ----------------------------------
-
-import os  # noqa: E402
-import shutil  # noqa: E402
-
-from .conftest import git_in  # noqa: E402
-
-
-def write(path: Path, text: str = "x\n") -> Path:
-    path.parent.mkdir(parents=True, exist_ok=True)
-    path.write_text(text, encoding="utf-8")
-    return path
-
-
-def facts_for(wc, runner_cls, repo, path, orca=None):
-    runner = runner_cls()
-    found = wc.discover_worktrees(runner, [wc.OrcaRepo("r", str(repo.main), "example")])
-    entry = next(
-        w for w in found.worktrees if os.path.realpath(w.path) == os.path.realpath(path)
-    )
-    return runner, wc.gather_facts(runner, entry, orca)
-
-
-def test_discovery_finds_main_linked_detached_and_locked_worktrees(
-    wc, runner_cls, throwaway_repo
-):
-    linked = throwaway_repo.add_worktree("topic")
-    detached = throwaway_repo.root / "wts" / "loose"
-    git_in(throwaway_repo.main, "worktree", "add", "-q", "--detach", str(detached))
-    locked = throwaway_repo.add_worktree("held")
-    git_in(throwaway_repo.main, "worktree", "lock", str(locked))
-    gone = throwaway_repo.add_worktree("gone")
-    shutil.rmtree(gone)  # a throwaway folder: the entry stays listed as prunable
-    runner = runner_cls()
-    repo = wc.OrcaRepo("r", str(throwaway_repo.main), "example")
-    found = wc.discover_worktrees(
-        runner, [repo, repo]
-    )  # a repo listed twice counts once
-    by_name = {os.path.basename(w.path): w for w in found.worktrees}
-    assert set(by_name) == {"main", "topic", "loose", "held", "gone"}
-    assert by_name["main"].is_main and by_name["main"].branch == "main"
-    assert not by_name["topic"].is_main and by_name["topic"].branch == "topic"
-    assert by_name["loose"].detached and by_name["loose"].branch is None
-    assert by_name["held"].locked and not by_name["topic"].locked
-    assert by_name["gone"].prunable
-    assert all(len(w.head) == 40 for w in found.worktrees)
-    assert found.failures == ()
-    assert os.path.realpath(linked) == os.path.realpath(by_name["topic"].path)
-    # facts of a missing folder: not present, nothing read, nothing raised
-    _, gone_facts = facts_for(wc, runner_cls, throwaway_repo, gone)
-    assert gone_facts.present is False and gone_facts.head is None
-
-
-def test_a_failed_listing_is_a_note_not_an_exception(wc, never_run_runner):
-    class Fails(type(never_run_runner)):
-        def _execute(self, argv, cwd, stdin):
-            return wc.Result(128, "", "not a git repository")
-
-    found = wc.discover_worktrees(
-        Fails(evidence_dir="/x"), [wc.OrcaRepo("r", "/nowhere", "n")]
-    )
-    assert found.worktrees == () and "git worktree list failed" in found.failures[0]
-
-
-def test_clean_worktree_facts(wc, runner_cls, throwaway_repo):
-    path = throwaway_repo.add_worktree("clean")
-    _, f = facts_for(wc, runner_cls, throwaway_repo, path)
-    assert f.present and f.failures == []
-    assert f.head == git_in(path, "rev-parse", "HEAD").strip()
-    assert f.origin.owner == "IronbellyOrg" and f.origin.is_ours
-    assert f.state.changed_tracked == [] and f.state.untracked_outside_dev == []
-    assert f.state.untracked_dev == [] and f.state.ignored_dev == []
-    assert f.state.ignored_build == [] and f.state.ignored_unknown == []
-    assert f.git_dir.endswith(os.path.join("worktrees", "clean"))
-    assert f.keep_file is False and f.operations == [] and f.nested_checkouts == []
-    assert f.size_bytes > 0
-    assert f.last_commit_ts and f.git_file_mtime and f.created_ts
-    assert f.idle_days(f.newest_activity() + 86400 * 3) == pytest.approx(3.0)
-
-
-def test_changed_tracked_file_and_staged_file(wc, runner_cls, throwaway_repo):
-    path = throwaway_repo.add_worktree("edited")
-    write(path / "README.md", "changed\n")
-    write(path / "added.txt")
-    git_in(path, "add", "added.txt")
-    _, f = facts_for(wc, runner_cls, throwaway_repo, path)
-    assert sorted(f.state.changed_tracked) == ["README.md", "added.txt"]
-    assert f.state.untracked_outside_dev == []
-
-
-def test_untracked_file_outside_dev(wc, runner_cls, throwaway_repo):
-    path = throwaway_repo.add_worktree("loose-files")
-    write(path / "notes.txt")
-    write(path / "sub" / "deep.txt")
-    _, f = facts_for(wc, runner_cls, throwaway_repo, path)
-    assert sorted(f.state.untracked_outside_dev) == ["notes.txt", "sub/deep.txt"]
-    assert f.state.untracked_dev == [] and f.state.changed_tracked == []
-
-
-def test_untracked_and_ignored_files_under_dev(wc, runner_cls, throwaway_repo):
-    path = throwaway_repo.add_worktree("devfiles")
-    write(path / ".dev" / "tasks" / "a.md")
-    write(path / ".dev" / "local" / "run.log")  # ignored by the tracked .gitignore
-    _, f = facts_for(wc, runner_cls, throwaway_repo, path)
-    assert f.state.untracked_dev == [".dev/tasks/a.md"]
-    assert f.state.ignored_dev == [".dev/local/run.log"]
-    assert f.state.untracked_outside_dev == [] and f.state.ignored_unknown == []
-
-
-def test_ignored_environment_file_outside_dev_is_unknown_local_state(
-    wc, runner_cls, throwaway_repo
-):
-    path = throwaway_repo.add_worktree("envfile")
-    write(path / ".env", "NAME=value\n")
-    _, f = facts_for(wc, runner_cls, throwaway_repo, path)
-    assert f.state.ignored_unknown == [".env"]
-    assert f.state.ignored_build == [] and f.state.ignored_generated == []
-
-
-def test_only_build_output_and_generated_copies(wc, runner_cls, throwaway_repo):
-    path = throwaway_repo.add_worktree("buildonly")
-    write(path / "pkg" / "__pycache__" / "m.pyc")
-    write(path / ".venv" / "lib" / "x.py")
-    write(path / "node_modules" / "p" / "i.js")
-    write(path / "dist" / "a.whl")
-    write(path / ".claude" / "agents" / "a.md")
-    write(path / ".serena" / "cache" / "c.json")
-    _, f = facts_for(wc, runner_cls, throwaway_repo, path)
-    assert sorted(f.state.ignored_build) == [
-        ".venv/lib/x.py",
-        "dist/a.whl",
-        "node_modules/p/i.js",
-        "pkg/__pycache__/m.pyc",
-    ]
-    assert sorted(f.state.ignored_generated) == [
-        ".claude/agents/a.md",
-        ".serena/cache/c.json",
-    ]
-    assert f.state.ignored_unknown == [] and f.state.changed_tracked == []
-
-
-def test_classify_status_edge_cases(wc):
-    raw = "\0".join(
-        [
-            "R  new name.txt",
-            "old name.txt",
-            " D gone.txt",
-            "UU conflict.txt",
-            "?? .dev/a.md",
-            "!! .dev/pkg/__pycache__/x.pyc",
-            "!! .env",
-            "!! uv.lock",
-            "",
-        ]
-    )
-    s = wc.classify_status(raw)
-    assert s.changed_tracked == ["new name.txt", "gone.txt", "conflict.txt"]
-    assert s.untracked_dev == [".dev/a.md"]
-    assert s.ignored_dev == [".dev/pkg/__pycache__/x.pyc"]
-    assert s.ignored_unknown == [".env"] and s.ignored_build == ["uv.lock"]
-    assert wc.classify_status("").changed_tracked == []
-    assert wc.classify_status("junk\0??x\0").untracked_outside_dev == []
-
-
-def test_keep_file_git_operation_and_nested_checkout(wc, runner_cls, throwaway_repo):
-    path = throwaway_repo.add_worktree("busy")
-    write(path / ".worktree-keep", "")
-    nested = path / "inner"
-    nested.mkdir()
-    git_in(nested, "init", "-q")
-    _, f = facts_for(wc, runner_cls, throwaway_repo, path)
-    assert f.keep_file is True
-    assert f.nested_checkouts == ["inner/.git"]
-    write(Path(f.git_dir) / "MERGE_HEAD", "0" * 40 + "\n")
-    write(Path(f.git_dir) / "index.lock", "")
-    (Path(f.git_dir) / "rebase-merge").mkdir()
-    _, again = facts_for(wc, runner_cls, throwaway_repo, path)
-    assert again.operations == ["MERGE_HEAD", "rebase-merge", "index.lock"]
-
-
-def test_the_git_reads_change_nothing(wc, runner_cls, throwaway_repo):
-    path = throwaway_repo.add_worktree("readonly")
-    write(path / "untracked.txt")
-    git_dir = Path(git_in(path, "rev-parse", "--absolute-git-dir").strip())
-    before = {p.name: p.read_bytes() for p in git_dir.iterdir() if p.is_file()}
-    head_before = git_in(path, "rev-parse", "HEAD")
-    runner, _ = facts_for(wc, runner_cls, throwaway_repo, path)
-    after = {p.name: p.read_bytes() for p in git_dir.iterdir() if p.is_file()}
-    assert before == after
-    assert git_in(path, "rev-parse", "HEAD") == head_before
-    assert (path / "untracked.txt").exists()
-    verbs = {tuple(c.argv[1:3]) for c in runner.commands}
-    assert verbs <= {
-        ("worktree", "list"),
-        ("rev-parse", "HEAD"),
-        ("rev-parse", "--git-dir"),
-        ("remote", "get-url"),
-        ("status", "--porcelain"),
-        ("log", "-1"),
-    }
-    assert verbs >= {("worktree", "list"), ("status", "--porcelain"), ("log", "-1")}
-
-
-def test_git_runs_with_optional_locks_off(runner_cls):
-    assert runner_cls()._env_for(["git", "status"])["GIT_OPTIONAL_LOCKS"] == "0"
-
-
-def test_orca_activity_joins_the_idle_time(wc, runner_cls, throwaway_repo):
-    path = throwaway_repo.add_worktree("watched")
-    ps = wc.parse_orca_worktrees(fixture_text("orca_worktree_ps.json")).items[0]
-    _, plain = facts_for(wc, runner_cls, throwaway_repo, path)
-    _, with_orca = facts_for(wc, runner_cls, throwaway_repo, path, orca=ps)
-    assert plain.orca_activity_ts is None
-    assert with_orca.orca_activity_ts == 1795095396.714
-    assert with_orca.newest_activity() == max(plain.newest_activity(), 1795095396.714)
-
-
-def test_idle_and_age_arithmetic(wc):
-    wt = wc.GitWorktree("/x", "/r", "h" * 40, "b", False, False, False, False, False)
-    f = wc.WorktreeFacts(
-        worktree=wt,
-        git_file_mtime=1_000_000.0,
-        last_commit_ts=1_050_000.0,
-        orca_activity_ts=900_000.0,
-        created_ts=500_000.0,
-    )
-    assert f.newest_activity() == 1_050_000.0
-    assert f.idle_days(1_050_000.0 + 86400 * 8) == pytest.approx(8.0)
-    assert f.age_days(500_000.0 + 86400) == pytest.approx(1.0)
-    assert (
-        f.idle_days(0) == 0.0
-    )  # a clock before the activity never gives a negative age
-    assert wc.WorktreeFacts(worktree=wt).idle_days(5.0) is None
-
-
-@pytest.mark.parametrize(
-    "url,owner,repo,ours",
-    [
-        (
-            "https://github.com/IronbellyOrg/IronClaude.git",
-            "IronbellyOrg",
-            "IronClaude",
-            True,
-        ),
-        (
-            "https://github.com/IronbellyOrg/IronClaude",
-            "IronbellyOrg",
-            "IronClaude",
-            True,
-        ),
-        (
-            "https://user@github.com/ironbellygroup/Coder.git\n",
-            "ironbellygroup",
-            "Coder",
-            True,
-        ),
-        (
-            "git@github.com:IronbellyOrg/IronClaude.git",
-            "IronbellyOrg",
-            "IronClaude",
-            True,
-        ),
-        ("ssh://git@github.com/IronbellyGroup/x.git/", "IronbellyGroup", "x", True),
-        (
-            "https://github.com/SuperClaude-Org/SuperClaude_Framework.git",
-            "SuperClaude-Org",
-            "SuperClaude_Framework",
-            False,
-        ),
-        ("https://github.com/IronbellyOrgX/x.git", "IronbellyOrgX", "x", False),
-    ],
-)
-def test_origin_owner(wc, url, owner, repo, ours):
-    info = wc.parse_origin(url)
-    assert (info.owner, info.repo, info.is_ours) == (owner, repo, ours)
-
-
-def test_origin_that_is_not_github_or_not_a_url_is_none(wc):
-    for url in (
-        "https://example.com/IronbellyOrg/x.git",
-        "",
-        "github.com",
-        "/local/path",
-    ):
-        assert wc.parse_origin(url) is None
-
-
-def test_name_guard_is_anchored_at_the_start(wc):
-    for name in (
-        "orca-port-evidence",
-        "orca-recipe-x",
-        "orca-pristine-y",
-        "orca-old-patched",
-    ):
-        assert wc.name_guard(f"/some/dir/{name}"), name
-    for name in (
-        "coder-orca-port",
-        "orca-old-patched-2",
-        "my-orca-recipe-x",
-        "issue-687",
-    ):
-        assert not wc.name_guard(f"/some/dir/{name}"), name
-    assert wc.name_guard("/some/dir/orca-port-a/")
-
-
-def test_the_script_own_folder_is_compared_by_real_path(wc, tmp_path):
-    wt = tmp_path / "wt"
-    (wt / "sub").mkdir(parents=True)
-    other = tmp_path / "wt-sibling"
-    other.mkdir()
-    alias = tmp_path / "alias"
-    alias.symlink_to(wt)
-    assert wc.is_own_folder(str(wt), [str(wt / "sub")])
-    assert wc.is_own_folder(str(wt), [str(alias / "sub")])
-    assert wc.is_own_folder(str(alias), [str(wt)])
-    assert not wc.is_own_folder(str(wt), [str(other)])
-    assert not wc.is_own_folder(str(wt), [])
-
-
-# --- the process scan, on a fake /proc ------------------------------------------------------
-
-
-def fake_proc(root: Path, entries: dict) -> Path:
-    """entries: pid -> cwd target path, None for an entry with no cwd link, 'file' for a plain file."""
-    root.mkdir(parents=True, exist_ok=True)
-    for pid, target in entries.items():
-        entry = root / str(pid)
-        entry.mkdir()
-        write(entry / "comm", f"proc{pid}\n")
-        if target == "file":
-            write(entry / "cwd", "not a link\n")
-        elif target is not None:
-            (entry / "cwd").symlink_to(target)
-    (root / "self").mkdir()  # a non-numeric name is skipped
-    return root
-
-
-def test_scan_finds_a_process_inside_and_not_a_sibling_folder(wc, tmp_path):
-    wt = tmp_path / "wt"
-    (wt / "sub").mkdir(parents=True)
-    sibling = tmp_path / "wt2"
-    sibling.mkdir()
-    proc = fake_proc(tmp_path / "proc", {101: wt / "sub", 102: sibling, 103: wt})
-    scan = wc.scan_processes(str(proc))
-    assert scan.ok and scan.failure == ""
-    inside = wc.processes_inside(scan, str(wt))
-    assert inside == [(101, "proc101"), (103, "proc103")]
-    assert wc.processes_inside(scan, str(tmp_path / "elsewhere")) == []
-
-
-def test_scan_ignores_a_vanished_entry_and_another_users_entry(wc, tmp_path):
-    wt = tmp_path / "wt"
-    wt.mkdir()
-    proc = fake_proc(tmp_path / "proc", {201: wt, 202: None, 203: wt})
-
-    def readlink(path):
-        if "/203/" in path:
-            raise PermissionError(13, "Permission denied", path)
-        return os.readlink(path)
-
-    scan = wc.scan_processes(
-        str(proc), my_uid=1000, readlink=readlink, uid_of=lambda p: 0
-    )
-    assert scan.ok
-    assert [pid for pid, _, _ in scan.cwds] == [
-        201
-    ]  # 202 vanished, 203 is another user's
-    assert scan.notes == ("pid 203: another user's process, ignored",)
-
-    def exits_while_checking(path):
-        raise ProcessLookupError(3, "No such process", path)
-
-    assert wc.scan_processes(str(proc), readlink=exits_while_checking).cwds == ()
-
-
-def test_scan_fails_for_any_other_error(wc, tmp_path):
-    wt = tmp_path / "wt"
-    wt.mkdir()
-    # a cwd that is not a link: readlink gives EINVAL, which is neither of the ignored cases
-    proc = fake_proc(tmp_path / "p1", {301: wt, 302: "file"})
-    scan = wc.scan_processes(str(proc))
-    assert scan.ok is False and "pid 302" in scan.failure and scan.cwds == ()
-    # permission denied for a process of our own user
-    proc = fake_proc(tmp_path / "p2", {401: wt})
-
-    def denied(path):
-        raise PermissionError(13, "Permission denied", path)
-
-    own = wc.scan_processes(str(proc), my_uid=7, readlink=denied, uid_of=lambda p: 7)
-    assert own.ok is False and "401" in own.failure
-
-    # the owner check itself fails for another reason
-    def broken_owner(path):
-        raise OSError(5, "Input/output error", path)
-
-    scan = wc.scan_processes(str(proc), my_uid=7, readlink=denied, uid_of=broken_owner)
-    assert scan.ok is False
-    # the folder cannot be listed
-    assert wc.scan_processes(str(tmp_path / "missing")).ok is False
-
-
-def test_scan_reads_the_real_proc_without_failing_on_this_machine(wc):
-    scan = wc.scan_processes()
-    assert scan.ok or scan.failure  # a result either way, never an exception
-    if scan.ok:
-        mine = [pid for pid, _, _ in scan.cwds]
-        assert os.getpid() in mine
-
-
-# --- Task 5: GitHub facts, with a fake gh and a fake landed check -------------------------
-
-import dataclasses  # noqa: E402
-
-SLUG = "IronbellyOrg/IronClaude"
-
-
-def gh_key(argv):
-    """('pr', 'list') or ('issue', 'view', '373', 'owner/repo') from a full gh argument list."""
-    repo = argv[argv.index("--repo") + 1] if "--repo" in argv else ""
-    if argv[2] == "list":
-        return (argv[1], "list", repo)
-    return (argv[1], argv[2], argv[3], repo)
-
-
-def gh_fake(wc, table):
-    """A gh handler: ``table`` maps gh_key to (code, stdout, stderr); no entry means HTTP failure."""
-
-    def handler(argv, cwd):
-        code, out, err = table.get(gh_key(argv), (1, "", "HTTP 502: bad gateway"))
-        return wc.Result(code, out, err)
-
-    return handler
-
-
-def pr_row(number, state, **extra):
-    row = {
-        "number": number,
-        "state": state,
-        "headRefOid": "a" * 40,
-        "author": {"login": "someone"},
-        "mergedAt": None,
-        "title": "title",
-        "body": "",
-        "closingIssuesReferences": [],
-        "headRefName": "topic",
-    }
-    row.update(extra)
-    return row
-
-
-NOT_FOUND = (
-    1,
-    "",
-    "GraphQL: Could not resolve to an issue or pull request with the number",
-)
-
-
-def assert_every_gh_call_names_its_repo(runner):
-    gh_calls = [c.argv for c in runner.commands if c.argv[0] == "gh"]
-    assert gh_calls
-    for argv in gh_calls:
-        assert "--repo" in argv and argv[argv.index("--repo") + 1].count("/") == 1
-        assert "api" not in argv and "{owner}/{repo}" not in argv
-
-
-def test_newest_merged_pull_request_wins_and_fields_are_recorded(wc, runner_cls):
-    rows = [
-        pr_row(5, "OPEN"),
-        pr_row(7, "MERGED", mergedAt="2026-11-01T00:00:00Z", headRefOid="b" * 40),
-        pr_row(
-            9,
-            "MERGED",
-            mergedAt="2026-11-10T00:00:00Z",
-            headRefOid="c" * 40,
-            title="Later title",
-            body="Body #3",
-            closingIssuesReferences=[
-                {
-                    "number": 12,
-                    "repository": {
-                        "name": "IronClaude",
-                        "owner": {"login": "IronbellyOrg"},
-                    },
-                },
-                {"number": 13},
-            ],
-        ),
-    ]
-    runner = runner_cls(
-        replies={"gh": gh_fake(wc, {("pr", "list", SLUG): (0, json.dumps(rows), "")})}
-    )
-    found = wc.find_pull_request(runner, SLUG, "topic")
-    assert found.ok and found.pr.number == 9 and found.pr.state == "MERGED"
-    assert found.pr.head_oid == "c" * 40 and found.pr.author == "someone"
-    assert (
-        found.pr.merged_at == "2026-11-10T00:00:00Z" and found.pr.title == "Later title"
-    )
-    assert found.pr.body == "Body #3" and found.pr.branch == "topic"
-    assert found.pr.closing == (
-        wc.IssueRef("IronbellyOrg/IronClaude", 12),
-        wc.IssueRef(None, 13),
-    )
-    argv = runner.commands[0].argv
-    assert (
-        argv[:3] == ["gh", "pr", "list"] and argv[argv.index("--head") + 1] == "topic"
-    )
-    assert argv[argv.index("--state") + 1] == "all"
-    assert_every_gh_call_names_its_repo(runner)
-
-
-def test_with_no_merged_pull_request_the_newest_is_returned_and_the_rest_are_edge_cases(
-    wc, runner_cls
-):
-    reply = (0, json.dumps([pr_row(5, "OPEN"), pr_row(8, "CLOSED")]), "")
-    runner = runner_cls(replies={"gh": gh_fake(wc, {("pr", "list", SLUG): reply})})
-    assert wc.find_pull_request(runner, SLUG, "topic").pr.number == 8
-    empty = runner_cls(
-        replies={"gh": gh_fake(wc, {("pr", "list", SLUG): (0, "[]", "")})}
-    )
-    found = wc.find_pull_request(empty, SLUG, "topic")
-    assert found.ok and found.pr is None
-    assert wc.find_pull_request(empty, SLUG, None).ok  # a detached HEAD asks nothing
-    assert len(empty.commands) == 1
-    for reply in (
-        (1, "", "HTTP 502"),
-        (0, "not json", ""),
-        (0, '{"a": 1}', ""),
-        (0, '[{"state": "OPEN"}]', ""),
-    ):
-        bad = runner_cls(replies={"gh": gh_fake(wc, {("pr", "list", SLUG): reply})})
-        result = wc.find_pull_request(bad, SLUG, "topic")
-        assert result.ok is False and result.pr is None and result.reason
-    # a branch name shaped like an option is refused by the runner and reported, not run
-    refused = runner_cls(replies={"gh": gh_fake(wc, {})})
-    assert wc.find_pull_request(refused, SLUG, "--web").ok is False
-    assert refused.commands == []
-
-
-def test_a_squash_merged_pull_request_is_merged_from_its_state_without_ancestry(
-    wc, runner_cls
-):
-    """The pull request commits are not on the base; state alone answers, no git call is made."""
-    rows = [pr_row(9, "MERGED", mergedAt="2026-11-10T00:00:00Z", headRefOid="d" * 40)]
-    runner = runner_cls(
-        replies={"gh": gh_fake(wc, {("pr", "list", SLUG): (0, json.dumps(rows), "")})}
-    )
-    found = wc.find_pull_request(runner, SLUG, "topic")
-    assert found.pr.state == "MERGED"
-    assert [c.argv[0] for c in runner.commands] == ["gh"]
-
-
-def test_commits_after_the_pull_request(wc, runner_cls, throwaway_repo):
-    path = throwaway_repo.add_worktree("after")
-    first = git_in(path, "rev-parse", "HEAD").strip()
-    write(path / "more.txt")
-    git_in(path, "add", "more.txt")
-    git_in(path, "commit", "-q", "-m", "second")
-    write(path / "more2.txt")
-    git_in(path, "add", "more2.txt")
-    git_in(path, "commit", "-q", "-m", "third")
-    head = git_in(path, "rev-parse", "HEAD").strip()
-    runner = runner_cls()
-    same = wc.commits_after_pr(runner, str(path), head, head)
-    assert (same.relation, same.commits_after) == ("same", 0)
-    ahead = wc.commits_after_pr(runner, str(path), head, first)
-    assert (ahead.relation, ahead.commits_after) == ("ahead", 2)
-    behind = wc.commits_after_pr(runner, str(path), first, head)
-    assert (behind.relation, behind.commits_after) == ("ancestor", 0)
-    missing = wc.commits_after_pr(runner, str(path), head, "e" * 40)
-    assert (
-        missing.relation == "unknown"
-        and missing.commits_after is None
-        and missing.reason
-    )
-    assert wc.commits_after_pr(runner, str(path), None, head).relation == "unknown"
-    assert wc.commits_after_pr(runner, str(path), head, "").relation == "unknown"
-    verbs = {tuple(c.argv[1:3]) for c in runner.commands}
-    assert verbs <= {("merge-base", "--is-ancestor"), ("rev-list", "--count")}
-
-
-# -- the landed check --------------------------------------------------------------------
-
-
-def landed_setup(wc, runner_cls, tmp_path, present, answer, gh_table=None):
-    places = [
-        tmp_path / "home" / "b.sh",
-        tmp_path / "checkout" / "b.sh",
-        tmp_path / "src" / "b.sh",
-    ]
-    for index in present:
-        write(places[index], "#!/bin/bash\n")
-
-    def bash(argv, cwd):
-        code, out = answer
-        return wc.Result(code, out, "")
-
-    runner = runner_cls(
-        replies={"bash": bash, "gh": gh_fake(wc, gh_table or {})},
-        landed_paths=tuple(str(p) for p in places),
-    )
-    return runner, places
-
-
-def test_landed_check_runs_the_script_in_the_main_checkout_in_lookup_order(
-    wc, runner_cls, tmp_path
-):
-    main = tmp_path / "main"
-    main.mkdir()
-    for present, label in (
-        ([0, 1, 2], "installed copy"),
-        ([1, 2], "checkout copy"),
-        ([2], "in-checkout fallback"),
-    ):
-        runner, places = landed_setup(
-            wc, runner_cls, tmp_path, present, (0, "MERGED\n")
-        )
-        got = wc.landed_check(
-            runner, SLUG, 700, str(main), which=lambda name: "/usr/bin/jq"
-        )
-        assert (got.token, got.via) == ("MERGED", label)
-        call = runner.commands[0]
-        assert call.argv == [
-            "bash",
-            str(places[present[0]]),
-            "700",
-        ] and call.cwd == str(main)
-        assert all(c.argv[0] != "gh" for c in runner.commands)
-        for place in places:
-            if place.exists():
-                place.unlink()
-
-
-@pytest.mark.parametrize("token", ["OPEN", "CLOSED", "NONE", "UNKNOWN"])
-def test_landed_tokens_other_than_merged_are_passed_through(
-    wc, runner_cls, tmp_path, token
-):
-    runner, _ = landed_setup(wc, runner_cls, tmp_path, [0], (4, f"note\n{token}\n"))
-    got = wc.landed_check(runner, SLUG, 5, str(tmp_path), which=lambda n: "/usr/bin/jq")
-    assert got.token == token
-
-
-def test_landed_check_with_no_answer_or_no_jq_is_unknown(wc, runner_cls, tmp_path):
-    runner, _ = landed_setup(wc, runner_cls, tmp_path, [0], (127, ""))
-    got = wc.landed_check(runner, SLUG, 5, str(tmp_path), which=lambda n: "/usr/bin/jq")
-    assert got.token == "UNKNOWN" and "no answer" in got.reason
-    runner, _ = landed_setup(wc, runner_cls, tmp_path, [0], (0, "MERGED\n"))
-    got = wc.landed_check(runner, SLUG, 5, str(tmp_path), which=lambda n: None)
-    assert got.token == "UNKNOWN" and "jq" in got.reason
-    assert runner.commands == []  # the script was not even started
-
-
-def test_without_the_script_the_gh_pr_view_fallback_answers(wc, runner_cls, tmp_path):
-    key = ("pr", "view", "700", SLUG)
-    cases = [
-        (
-            (
-                0,
-                json.dumps({"state": "MERGED", "mergedAt": "2026-11-10T00:00:00Z"}),
-                "",
-            ),
-            "MERGED",
-        ),
-        ((0, json.dumps({"state": "OPEN", "mergedAt": None}), ""), "OPEN"),
-        ((0, json.dumps({"state": "CLOSED", "mergedAt": None}), ""), "CLOSED"),
-        ((0, json.dumps({"state": "MERGED", "mergedAt": None}), ""), "UNKNOWN"),
-        ((0, "garbage", ""), "UNKNOWN"),
-    ]
-    for reply, token in cases:
-        runner, _ = landed_setup(wc, runner_cls, tmp_path, [], (0, ""), {key: reply})
-        got = wc.landed_check(runner, SLUG, 700, str(tmp_path))
-        assert got.token == token and got.via == "gh pr view"
-        assert [c.argv[:3] for c in runner.commands] == [["gh", "pr", "view"]]
-        assert_every_gh_call_names_its_repo(runner)
-
-
-def test_when_the_fallback_also_fails_the_landed_check_said_unknown(
-    wc, runner_cls, tmp_path
-):
-    runner, _ = landed_setup(wc, runner_cls, tmp_path, [], (0, ""), {})
-    got = wc.landed_check(runner, SLUG, 700, str(tmp_path))
-    assert got.token == "UNKNOWN" and got.reason.startswith("landed check said UNKNOWN")
-
-
-# -- issues for rule 4 -------------------------------------------------------------------------
-
-
-def make_orca(wc):
-    ps = wc.parse_orca_worktrees(fixture_text("orca_worktree_ps.json")).items[0]
-    return dataclasses.replace(
-        ps,
-        comment="sc:issue IronbellyOrg/IronClaude#669 and more",
-        linked_issue=(None, 5),
-    )
-
-
-def issue_reply(state):
-    return (0, json.dumps({"state": state}), "")
-
-
-def test_issue_numbers_come_from_every_place_and_pull_request_numbers_are_dropped(
-    wc, runner_cls
-):
-    coder = "IronbellyGroup/Coder"
-    pr = wc.PullRequest(
-        number=9, state="MERGED", head_oid="a" * 40, author="x", merged_at="2026-11-10T00:00:00Z",
-        title="Fix thing (#20)",
-        body=f"Fixes #21. Related: {SLUG}#373 and {coder}#373. See also {SLUG}#999.",
-        closing=(wc.IssueRef(None, 10),), branch="docs-354-topic",
-    )  # fmt: skip
-    table = {
-        # closing reference: a known issue
-        ("issue", "view", "10", SLUG): issue_reply("CLOSED"),
-        # #20 and #21 in the title and body: not pull requests, issues
-        ("pr", "view", "20", SLUG): NOT_FOUND,
-        ("issue", "view", "20", SLUG): issue_reply("CLOSED"),
-        ("pr", "view", "21", SLUG): NOT_FOUND,
-        ("issue", "view", "21", SLUG): issue_reply("OPEN"),
-        # IronClaude 373 is a merged pull request, Coder 373 is an open issue
-        ("pr", "view", "373", SLUG): (0, json.dumps({"state": "MERGED"}), ""),
-        ("pr", "view", "373", coder): NOT_FOUND,
-        ("issue", "view", "373", coder): issue_reply("OPEN"),
-        # a number that is no issue anywhere is dropped
-        ("pr", "view", "999", SLUG): NOT_FOUND,
-        ("issue", "view", "999", SLUG): NOT_FOUND,
-        # the branch name number 354, the folder name number 687
-        ("pr", "view", "354", SLUG): NOT_FOUND,
-        ("issue", "view", "354", SLUG): issue_reply("CLOSED"),
-        ("pr", "view", "687", SLUG): NOT_FOUND,
-        ("issue", "view", "687", SLUG): issue_reply("CLOSED"),
-        # Orca card comment 669, linked issue 5
-        ("pr", "view", "669", SLUG): NOT_FOUND,
-        ("issue", "view", "669", SLUG): issue_reply("CLOSED"),
-        ("issue", "view", "5", SLUG): issue_reply("CLOSED"),
-    }
-    runner = runner_cls(replies={"gh": gh_fake(wc, table)})
-    refs = wc.parse_orca_references(fixture_text("orca_reference_list.json"))
-    facts = wc.collect_issues(
-        runner, SLUG, pr, "topic-354", "/w/issue-687", make_orca(wc), refs
-    )
-    got = {(i.repo, i.number): (i.state, i.sources) for i in facts.issues}
-    assert facts.failures == ()
-    assert set(got) == {
-        (SLUG, 10), (SLUG, 20), (SLUG, 21), (coder, 373),
-        (SLUG, 354), (SLUG, 687), (SLUG, 669), (SLUG, 5),
-    }  # fmt: skip
-    assert got[(SLUG, 10)][1] == ("closing reference",)
-    assert got[(SLUG, 20)][1] == ("title or body",)
-    assert got[(SLUG, 354)][1] == (
-        "branch name",
-    )  # branch topic-354 and PR branch agree
-    assert got[(SLUG, 687)][1] == ("folder name", "Orca reference")
-    assert got[(SLUG, 669)][1] == ("Orca card comment",)
-    assert got[(SLUG, 5)][1] == ("Orca linked issue",)
-    assert (SLUG, 373) not in got  # the pull request number is dropped
-    assert [i.number for i in facts.open_issues] == [21, 373]
-    assert_every_gh_call_names_its_repo(runner)
-
-
-def test_a_failed_issue_lookup_is_recorded_and_none_found_passes(wc, runner_cls):
-    pr = wc.PullRequest(9, "MERGED", "a" * 40, "x", "d", "t", "see #44", (), "topic")
-    flaky = {
-        ("pr", "view", "44", SLUG): NOT_FOUND
-    }  # the issue view then fails (HTTP 502)
-    runner = runner_cls(replies={"gh": gh_fake(wc, flaky)})
-    facts = wc.collect_issues(runner, SLUG, pr, "topic", "/w/plain")
-    assert facts.failures == (f"issue lookup failed: {SLUG}#44",)
-    assert not facts.none_found
-    # the pull request check itself fails
-    runner = runner_cls(replies={"gh": gh_fake(wc, {})})
-    assert wc.collect_issues(runner, SLUG, pr, "topic", "/w/plain").failures
-    # a known issue that cannot be found is a failure, not a pass
-    pr2 = wc.PullRequest(
-        9, "MERGED", "a" * 40, "x", "d", "t", "", (wc.IssueRef(None, 3),), "topic"
-    )
-    runner = runner_cls(
-        replies={"gh": gh_fake(wc, {("issue", "view", "3", SLUG): NOT_FOUND})}
-    )
-    assert wc.collect_issues(runner, SLUG, pr2, "topic", "/w/plain").failures
-    # nothing anywhere: passes with "none found"
-    runner = runner_cls(replies={"gh": gh_fake(wc, {})})
-    plain = wc.collect_issues(runner, SLUG, None, "topic", "/w/plain")
-    assert plain.none_found and plain.open_issues == [] and runner.commands == []
-
-
-def test_an_unreadable_orca_reference_list_keeps_the_worktree(wc, runner_cls):
-    runner = runner_cls(replies={"gh": gh_fake(wc, {})})
-    down = wc.parse_orca_references("not json")
-    facts = wc.collect_issues(runner, SLUG, None, "topic", "/w/plain", None, down)
-    assert not facts.none_found
-    assert facts.failures == (f"issue lookup failed: {down.unavailable}",)
-    assert runner.commands == []
-    # a read that worked and held nothing is still "none found"; so is no read at all
-    empty = wc.parse_orca_references('{"ok": true, "result": {"references": []}}')
-    assert wc.collect_issues(
-        runner, SLUG, None, "topic", "/w/plain", None, empty
-    ).none_found
-    assert wc.collect_issues(
-        runner, SLUG, None, "topic", "/w/plain", None, None
-    ).none_found
-
-
-def test_a_reference_to_a_repo_that_is_not_ours_is_a_failed_lookup_and_never_run(
-    wc, runner_cls
-):
-    pr = wc.PullRequest(
-        9,
-        "MERGED",
-        "a" * 40,
-        "x",
-        "d",
-        "t",
-        "SuperClaude-Org/SuperClaude_Framework#5",
-        (),
-        "topic",
-    )
-    runner = runner_cls(replies={"gh": gh_fake(wc, {})})
-    facts = wc.collect_issues(runner, SLUG, pr, "topic", "/w/plain")
-    assert facts.failures and facts.issues == ()
-    assert runner.commands == []  # the runner refused it before any process
-
-
-def test_text_and_name_parsers(wc):
-    refs = wc.refs_in_text(
-        "Fixes #1, see Org/Repo#22 and (#3). not a#4 and http://h/x#5"
-    )
-    assert [(r.repo, r.number) for r in refs] == [
-        (None, 1),
-        ("Org/Repo", 22),
-        (None, 3),
-    ]
-    assert wc.numbers_in_name("docs-354-foo") == [354]
-    assert wc.numbers_in_name("419-x-issue-655") == [419, 655]
-    assert wc.numbers_in_name("a-1-b-12345-c-99") == [99]
-    assert wc.numbers_in_name("") == []


===== new file: tests/worktree_cleanup/test_git_facts.py =====
"""Task 7: the test support itself, and the git facts the script relies on.

Everything runs in throwaway repositories under ``tmp_path``; no test touches a real
worktree. The reply shapes in ``fixtures/`` are hand-written from the spec and the Orca
help, not literal captures (see ``fixtures/README.md``), as in
``tests/merged_pr_log/test_merged_pr_log.py``.
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

from .conftest import STANDARD_NAMES, git_in

FIXTURES = Path(__file__).parent / "fixtures"

SEVEN_SHAPES = {
    "gh_pr_list.json": list,
    "gh_pr_view.json": dict,
    "gh_issue_view.json": dict,
    "orca_repo_list.json": dict,
    "orca_worktree_ps.json": dict,
    "orca_reference_list.json": dict,
    "orca_terminal_list.json": dict,
}


def write(path: Path, text: str = "x\n") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


# --- the support: fixtures, throwaway repos, the recording runner ------------------------------


@pytest.mark.parametrize("name,kind", SEVEN_SHAPES.items())
def test_one_recorded_shape_for_each_of_the_seven_replies(name, kind):
    doc = json.loads((FIXTURES / name).read_text(encoding="utf-8"))
    assert isinstance(doc, kind)
    assert "ghp_" not in (FIXTURES / name).read_text(encoding="utf-8")


def test_the_fixture_shapes_feed_the_script_parsers(wc):
    prs = wc.parse_pull_requests(
        (FIXTURES / "gh_pr_list.json").read_text(encoding="utf-8")
    )
    assert [(p.number, p.state) for p in prs] == [(700, "MERGED"), (650, "CLOSED")]
    assert prs[0].closing == (wc.IssueRef("IronbellyOrg/IronClaude", 21),)
    assert json.loads((FIXTURES / "gh_pr_view.json").read_text())["state"] == "MERGED"
    assert (
        json.loads((FIXTURES / "gh_issue_view.json").read_text())["state"] == "CLOSED"
    )


def test_the_standard_worktrees_cover_every_local_state(
    wc, runner_cls, local_origin_repo
):
    wts = local_origin_repo.add_standard_worktrees()
    assert set(wts) == set(STANDARD_NAMES)
    runner = runner_cls()
    repo = wc.OrcaRepo("r", str(local_origin_repo.main), "example")
    found = {
        os.path.basename(w.path): w
        for w in wc.discover_worktrees(runner, [repo]).worktrees
    }
    assert found["detached"].detached and found["locked"].locked
    states = {}
    for name in ("clean", "tracked-edit", "dev-files", "env-file", "build-only"):
        states[name] = wc.gather_facts(runner, found[name]).state
    assert (
        states["clean"].changed_tracked == [] and states["clean"].ignored_unknown == []
    )
    assert states["tracked-edit"].changed_tracked == ["README.md"]
    assert states["dev-files"].untracked_dev and states["dev-files"].ignored_dev
    assert states["env-file"].ignored_unknown == [".env"]
    assert (
        states["build-only"].ignored_build and not states["build-only"].ignored_unknown
    )
    # the origin is a local bare repository, and a second one stands in for the evidence repo
    assert git_in(local_origin_repo.main, "remote", "get-url", "origin").strip() == str(
        local_origin_repo.bare
    )


def test_a_second_bare_repository_stands_in_for_the_evidence_repo(
    evidence_bare, tmp_path
):
    clone = tmp_path / "evidence-clone"
    git_in(tmp_path, "clone", "-q", str(evidence_bare), str(clone))
    assert (clone / "README.md").read_text(encoding="utf-8") == "evidence\n"


def test_the_fake_proc_builder_is_shared(wc, tmp_path):
    from .conftest import make_fake_proc

    wt = tmp_path / "wt"
    wt.mkdir()
    proc = make_fake_proc(tmp_path / "proc", {11: wt})
    assert wc.processes_inside(wc.scan_processes(str(proc)), str(wt)) == [
        (11, "proc11")
    ]


def test_the_recording_runner_lists_every_command_and_refuses_what_the_real_runner_refuses(
    wc, runner_cls, local_origin_repo
):
    runner = runner_cls()
    runner.run(["git", "rev-parse", "--git-dir"], cwd=str(local_origin_repo.main))
    runner.run(
        ["orca", "repo", "list", "--json"]
    )  # no canned reply: answered 127, recorded
    assert [c.argv for c in runner.commands] == [
        ["git", "rev-parse", "--git-dir"],
        ["orca", "repo", "list", "--json"],
    ]
    real = wc.Runner(evidence_dir=None)
    for argv in (
        ["git", "reset", "--hard"],
        ["git", "branch", "-D", "x"],
        ["git", "worktree", "remove", "--force", "/x"],
        ["orca", "worktree", "rm", "--worktree", "id:1", "--force"],
        ["rm", "-rf", "/x"],
        ["gh", "pr", "merge", "1", "--repo", "IronbellyOrg/IronClaude"],
    ):
        with pytest.raises(wc.RefusedCommand):
            real.check_allowed(argv)
        with pytest.raises(wc.RefusedCommand):
            runner.run(argv)
    assert len(runner.commands) == 2  # the refused ones were never recorded or run


def test_a_real_process_never_starts_outside_the_test_tmp_folder(
    wc, runner_cls, throwaway_repo, tmp_path
):
    runner = runner_cls()
    outside = Path(__file__).resolve().parents[2]  # the real checkout
    refused = [
        (["git", "rev-parse", "--git-dir"], str(outside)),
        (["git", "rev-parse", "--git-dir"], None),
        (["git", "rev-parse", "--git-dir"], str(tmp_path.parent)),
        (
            ["git", "-C", str(outside), "rev-parse", "--git-dir"],
            str(throwaway_repo.main),
        ),
        (["git", "-C", "..", "rev-parse", "--git-dir"], str(tmp_path)),
        (["tar", "-tzf", str(outside / "README.md")], str(tmp_path)),
        (["xargs", "-0", "git", "clean", "-f", "-x", "--"], str(outside)),
    ]
    runner.register_saved(str(outside), ["x"])
    for argv, cwd in refused:
        with pytest.raises(AssertionError, match="outside the test tmp folder"):
            runner.run(argv, cwd=cwd, stdin=b"x\0")
    # inside the tmp folder (also through a symlink, which is resolved) it still runs
    link = tmp_path / "link"
    link.symlink_to(throwaway_repo.main)
    assert runner.run(["git", "rev-parse", "--git-dir"], cwd=str(link)).returncode == 0
    assert (
        runner.run(
            ["git", "-C", str(throwaway_repo.main), "rev-parse", "--git-dir"],
            cwd=str(tmp_path),
        ).returncode
        == 0
    )


# --- the git facts of source section 9 ------------------------------------------------------------


def test_worktree_remove_without_force_refuses_dirty_worktrees_and_removes_ignored_only(
    wc, runner_cls, throwaway_repo
):
    untracked = throwaway_repo.add_worktree("with-untracked")
    write(untracked / "new.txt")
    modified = throwaway_repo.add_worktree("with-edit")
    write(modified / "README.md", "edited\n")
    ignored_only = throwaway_repo.add_worktree("only-ignored")
    write(ignored_only / ".env", "NAME=placeholder\n")
    write(ignored_only / "pkg" / "__pycache__" / "m.pyc")
    runner = runner_cls()
    for path in (untracked, modified):
        res = runner.run(
            ["git", "worktree", "remove", str(path)], cwd=str(throwaway_repo.main)
        )
        assert res.returncode != 0 and path.is_dir()
        assert "contains modified or untracked files" in res.stderr
    res = runner.run(
        ["git", "worktree", "remove", str(ignored_only)], cwd=str(throwaway_repo.main)
    )
    assert res.returncode == 0, res.stderr
    assert not ignored_only.exists()
    listed = git_in(throwaway_repo.main, "worktree", "list", "--porcelain")
    assert str(ignored_only) not in listed and str(untracked) in listed


def test_branch_d_refuses_after_a_squash_merge(wc, runner_cls, throwaway_repo):
    main = throwaway_repo.main
    wt = throwaway_repo.add_worktree("squashed")
    write(wt / "feature.txt")
    git_in(wt, "add", "feature.txt")
    git_in(wt, "commit", "-q", "-m", "feature")
    git_in(main, "merge", "-q", "--squash", "squashed")
    git_in(main, "commit", "-q", "-m", "squash of squashed")
    git_in(main, "worktree", "remove", str(wt))  # the folder is gone; the branch is not
    runner = runner_cls()
    res = runner.run(["git", "branch", "-d", "squashed"], cwd=str(main))
    assert res.returncode != 0 and "not fully merged" in res.stderr
    assert "squashed" in git_in(main, "branch", "--list", "squashed")
    # a branch whose commits are on main is deleted by the same command
    plain = throwaway_repo.add_worktree("plain")
    git_in(main, "worktree", "remove", str(plain))
    assert runner.run(["git", "branch", "-d", "plain"], cwd=str(main)).returncode == 0


def test_git_clean_with_literal_pathspecs_removes_exactly_the_listed_files(
    wc, runner_cls, throwaway_repo
):
    wt = throwaway_repo.add_worktree("cleaning")
    listed = [".dev/a b.txt", ".dev/local/run [1].log", ".dev/tasks/*.md"]
    for rel in listed:
        write(wt / rel)
    unlisted = [
        ".dev/keep.txt",
        "loose.txt",
        ".env",
        ".dev/tasks/other.md",
        ".dev/local/run 1.log",
    ]
    for rel in unlisted:
        write(wt / rel)
    tracked = wt / "README.md"
    runner = runner_cls()
    runner.register_saved(str(wt), listed)
    stdin = "\0".join(listed).encode() + b"\0"
    res = runner.run(
        ["xargs", "-0", "git", "clean", "-f", "-x", "--"], cwd=str(wt), stdin=stdin
    )
    assert res.returncode == 0, res.stderr
    for rel in listed:
        assert not (wt / rel).exists(), rel
    for rel in unlisted:
        assert (wt / rel).exists(), (
            rel
        )  # a glob or a bracket in a name matched nothing else
    assert tracked.read_text(encoding="utf-8") == "example\n"
    assert " " in listed[0]  # the file name with a space was part of the case
    # the same call with an unlisted path is refused before any process starts
    with pytest.raises(wc.RefusedCommand):
        runner.run(
            ["xargs", "-0", "git", "clean", "-f", "-x", "--"],
            cwd=str(wt),
            stdin=b"loose.txt\0",
        )
    assert (wt / "loose.txt").exists()


def test_the_facts_tests_use_only_tmp_path(tmp_path, throwaway_repo):
    assert str(throwaway_repo.main).startswith(str(tmp_path))
    top = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=throwaway_repo.main,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    assert top.startswith(str(tmp_path))


===== new file: tests/worktree_cleanup/fixtures/gh_pr_list.json =====
[
  {
    "number": 700,
    "state": "MERGED",
    "headRefOid": "1111111111111111111111111111111111111111",
    "headRefName": "example/issue-687",
    "author": {"login": "example-user"},
    "mergedAt": "2026-11-10T12:00:00Z",
    "title": "Example change (#20)",
    "body": "Fixes #21. Related: IronbellyOrg/IronClaude#22.",
    "closingIssuesReferences": [
      {
        "number": 21,
        "repository": {"name": "IronClaude", "owner": {"login": "IronbellyOrg"}}
      }
    ]
  },
  {
    "number": 650,
    "state": "CLOSED",
    "headRefOid": "2222222222222222222222222222222222222222",
    "headRefName": "example/issue-687",
    "author": {"login": "example-user"},
    "mergedAt": null,
    "title": "Earlier try",
    "body": "",
    "closingIssuesReferences": []
  }
]


===== new file: tests/worktree_cleanup/fixtures/gh_pr_view.json =====
{"state": "MERGED", "mergedAt": "2026-11-10T12:00:00Z"}


===== new file: tests/worktree_cleanup/fixtures/gh_issue_view.json =====
{"state": "CLOSED"}


Codegraph context: index_state=fresh checked_at=2026-11-20T18:23:04Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-687 projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-687
call codegraph only when index_state: fresh, never to widen scope
Q2b ran on the Grep and Read floor for dependents of changed symbols (this task creates new files or edits registration lists; see the diff).

Delta diff from the previous reviewed tree (empty on the first review): diff --git a/tests/worktree_cleanup/conftest.py b/tests/worktree_cleanup/conftest.py
index 4ac429786..0c124d0e3 100644
--- a/tests/worktree_cleanup/conftest.py
+++ b/tests/worktree_cleanup/conftest.py
@@ -65,12 +65,43 @@ def runner_cls(wc):
                 if answer is not None:
                     return answer
             if prog in ("git", "tar", "xargs") and self.real_git:
+                self._require_throwaway(argv, cwd)
                 return super()._execute(argv, cwd, stdin)
             return wc.Result(127, "", f"no canned reply for {argv}")
 
+        def _require_throwaway(self, argv, cwd):
+            """A real process starts only inside this test's tmp folder: fail loudly otherwise."""
+            root = self.confine_root
+            places = [cwd]
+            for i, tok in enumerate(argv[:-1]):
+                if tok == "-C":
+                    places.append(os.path.join(cwd or "", argv[i + 1]))
+            if os.path.basename(argv[0]) == "tar":
+                places.append(argv[-1])
+            for place in places:
+                real = os.path.realpath(place) if place else ""
+                if (
+                    not root
+                    or not place
+                    or not (real == root or real.startswith(root + os.sep))
+                ):
+                    raise AssertionError(
+                        f"a real {argv[0]} would start outside the test tmp folder: "
+                        f"cwd={cwd!r} argv={argv}"
+                    )
+
+    RecordingRunner.confine_root = None
     return RecordingRunner
 
 
+@pytest.fixture(autouse=True)
+def _confine_real_processes(runner_cls, tmp_path):
+    """Real git, tar and xargs may start only under this test's tmp_path."""
+    runner_cls.confine_root = os.path.realpath(tmp_path)
+    yield
+    runner_cls.confine_root = None
+
+
 class NeverRun:
     """A reply table whose handlers fail the test if a process would start."""
 
diff --git a/tests/worktree_cleanup/test_git_facts.py b/tests/worktree_cleanup/test_git_facts.py
index 27480078d..667010d70 100644
--- a/tests/worktree_cleanup/test_git_facts.py
+++ b/tests/worktree_cleanup/test_git_facts.py
@@ -135,6 +135,40 @@ def test_the_recording_runner_lists_every_command_and_refuses_what_the_real_runn
     assert len(runner.commands) == 2  # the refused ones were never recorded or run
 
 
+def test_a_real_process_never_starts_outside_the_test_tmp_folder(
+    wc, runner_cls, throwaway_repo, tmp_path
+):
+    runner = runner_cls()
+    outside = Path(__file__).resolve().parents[2]  # the real checkout
+    refused = [
+        (["git", "rev-parse", "--git-dir"], str(outside)),
+        (["git", "rev-parse", "--git-dir"], None),
+        (["git", "rev-parse", "--git-dir"], str(tmp_path.parent)),
+        (
+            ["git", "-C", str(outside), "rev-parse", "--git-dir"],
+            str(throwaway_repo.main),
+        ),
+        (["git", "-C", "..", "rev-parse", "--git-dir"], str(tmp_path)),
+        (["tar", "-tzf", str(outside / "README.md")], str(tmp_path)),
+        (["xargs", "-0", "git", "clean", "-f", "-x", "--"], str(outside)),
+    ]
+    runner.register_saved(str(outside), ["x"])
+    for argv, cwd in refused:
+        with pytest.raises(AssertionError, match="outside the test tmp folder"):
+            runner.run(argv, cwd=cwd, stdin=b"x\0")
+    # inside the tmp folder (also through a symlink, which is resolved) it still runs
+    link = tmp_path / "link"
+    link.symlink_to(throwaway_repo.main)
+    assert runner.run(["git", "rev-parse", "--git-dir"], cwd=str(link)).returncode == 0
+    assert (
+        runner.run(
+            ["git", "-C", str(throwaway_repo.main), "rev-parse", "--git-dir"],
+            cwd=str(tmp_path),
+        ).returncode
+        == 0
+    )
+
+
 # --- the git facts of source section 9 ------------------------------------------------------------
 
 

Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B4 ac=scope at=tests/worktree_cleanup/conftest.py:67 anchor="runs real `git`, `tar` and `xargs` only inside throwaway folders under `tmp_path`" chk=n,y,n,y family=runner-confinement fix=in RecordingRunner._execute require a real cwd or -C value under the test tmp folder before running git, tar or xargs, and refuse cwd None; add a test first=A1 origin=new: nothing enforces that the recording runner runs real git, tar and xargs only inside throwaway folders.

Saved-probe re-check hit locations (may be empty): tests/worktree_cleanup/conftest.py:46:    ``real_git`` is true (on throwaway folders only). A command with no canned reply
tests/worktree_cleanup/conftest.py:52:            self, replies=None, real_git=True, evidence_dir=None, landed_paths=(LANDED,)
tests/worktree_cleanup/conftest.py:58:            self.real_git = real_git
tests/worktree_cleanup/conftest.py:60:        def _execute(self, argv, cwd, stdin):
tests/worktree_cleanup/conftest.py:67:            if prog in ("git", "tar", "xargs") and self.real_git:
tests/worktree_cleanup/conftest.py:68:                self._require_throwaway(argv, cwd)
tests/worktree_cleanup/conftest.py:69:                return super()._execute(argv, cwd, stdin)
tests/worktree_cleanup/conftest.py:72:        def _require_throwaway(self, argv, cwd):
tests/worktree_cleanup/conftest.py:117:        def _execute(self, argv, cwd, stdin):
tests/worktree_cleanup/test_facts.py:295:        def _execute(self, argv, cwd, stdin):


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
