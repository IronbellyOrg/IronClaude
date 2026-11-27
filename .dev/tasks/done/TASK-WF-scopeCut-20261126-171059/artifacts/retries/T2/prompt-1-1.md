3be33bb520d1f5d29fd5c861966e80bdbcfc5555
Review one task for spec compliance.

Task brief: ## Task 2: Add the allowlisted Runner and the shared FakeRunner

Depends on: Task 1

Add to `scripts/apply_org_rulesets.py` the types `Result(returncode, stdout, stderr)`, `CommandRecord(argv, stdin_name)` (it keeps the `name` of a posted body, not only a count), `RefusedCommand` and `Runner(read_only=False)`, modelled on `Runner` in `scripts/worktree_cleanup.py` (lines 246 to 586), as in source.md section 2.2. `Runner.run(argv, stdin=None)` does four things in order: `check_allowed` (a positive allowlist of the `gh api` shapes listed in section 2.2, all under `repos/<org>/<repo>`), the read-only check (refuses POST), appending a `CommandRecord`, and one call to `_execute(argv, stdin)`. `_execute` is the only method that starts a process; it passes the named constant `TIMEOUT_SECONDS` to `subprocess.run` and turns `subprocess.TimeoutExpired` into the one named result `TIMED_OUT` (a `Result` with return code 124), never a hang. Add `check_org(org)`, which refuses an empty value and the upstream org name `SuperClaude-Org` in any letter case.

Extend `tests/org_rulesets/conftest.py` with `FakeRunner(orr.Runner)` (built inside a session fixture `fake_runner_cls`) that overrides only `_execute`. Its answers are keyed by method and path; an answer may be a callable that receives argv and stdin, or a list served in order, so three POSTs to `rulesets` can return three ids. An answer with no canned reply gets return code 127. Create `tests/org_rulesets/test_runner.py`.

Acceptance criteria:
- A call outside the allowlist, an empty argv and a path with an option-like segment raise `RefusedCommand` when sent through `FakeRunner`, and the overridden `_execute` is never reached (a counter on the fake stays 0).
- A read-only runner refuses POST; a normal runner accepts POST only for `rulesets` under `repos/<org>/<repo>`.
- `check_org("SuperClaude-Org")`, `check_org("superclaude-org")` and `check_org("")` raise; `check_org("acme")` passes.
- Every accepted `gh api` call recorded by the fake is one of the allowed shapes and names `repos/<org>/<repo>` in full.
- A test replaces `subprocess.run` with a stub: a `subprocess.TimeoutExpired` gives the result `TIMED_OUT`, and the timeout argument passed equals `TIMEOUT_SECONDS`.
- The closing checks of the Constraints pass.

Global constraints: ## Constraints

- No task calls GitHub or touches any IronbellyGroup repo. Every GitHub call in a test goes through `FakeRunner` of `tests/org_rulesets/conftest.py`; no test starts the real `gh`.
- `.github/rulesets/*.json`, the commands in `docs/developer-guide/branch-protection.md` and `tests/docs/test_branch_protection_rulesets.py` stay unchanged. The only edit to the guide is the one link line of Task 7. The existing test must keep passing.
- Python 3.10, standard library only; ruff rules `E,F,I,N,W,TID` at line length 88 as set in `pyproject.toml`.
- No real private repo name and no real org login is written in any tracked file. Tests use synthetic names such as `acme-one`. The script holds no org or repo name, except the upstream org name it refuses.
- Only these paths may change: `scripts/apply_org_rulesets.py`, `tests/org_rulesets/`, `docs/developer-guide/branch-protection-multi-repo.md`, `docs/developer-guide/branch-protection.md` (one link line) and `docs/developer-guide/documentation-index.md`. Nothing under `.claude/` or `.github/` changes.
- "source.md section 2.3" names a heading of `./source.md`.
- Test setup follows `tests/worktree_cleanup/conftest.py` (the session fixture `wc` at lines 26 to 37 loads the script once; `RecordingRunner` at lines 68 to 109 subclasses the real `Runner` and overrides `_execute`). `tests/org_rulesets/conftest.py` defines the session fixture `orr` (the script module) and every shared fixture exactly once; a test module never imports a fixture from another module, because CI lists fixtures with `pytest --fixtures` and a duplicate crashes it.
- Location rule: the repo root is `Path(__file__).resolve().parent.parent`, the rule files are read from `<root>/.github/rulesets/`, and no function reads the current working folder. The before-state file is written into the folder given with `--out`.
- Choices for the owner's review (all are made inside the scope cut and listed in the pull request): one repo per run; the push check excuses no direct push by a named person; the tag ruleset is applied with a printed warning and a manual check of release workflows; rollback is manual.
- Every task ends with the same checks: `uv run pytest tests/org_rulesets/` passes (plus `tests/docs/test_branch_protection_rulesets.py` from Task 6 on), `uv run ruff check scripts/apply_org_rulesets.py tests/org_rulesets` reports nothing and `uv run ruff format --check scripts/apply_org_rulesets.py tests/org_rulesets` reports nothing.

Start sha: 3be33bb520d1f5d29fd5c861966e80bdbcfc5555
Diff against the start snapshot: diff --git a/scripts/apply_org_rulesets.py b/scripts/apply_org_rulesets.py
index 8adc00875..eafeb9141 100644
--- a/scripts/apply_org_rulesets.py
+++ b/scripts/apply_org_rulesets.py
@@ -6,14 +6,18 @@ renders them for a repo's branches, checks the repo (a dry run that prints what
 change) and, only with ``--apply --confirm <digest>``, creates the rulesets and reads
 each one back. It never edits or deletes a ruleset and it never posts the issue comment.
 
-This part holds the pure rendering and comparing functions. The command runner, the
-checks and the command line follow in the same file.
+The file holds the pure rendering and comparing functions and the command runner
+(``Runner``: the only place a ``gh`` process starts, behind a positive allowlist).
 """
 
 from __future__ import annotations
 
 import hashlib
 import json
+import os
+import re
+import subprocess
+from dataclasses import dataclass, field
 from pathlib import Path
 
 EXIT_OK = 0
@@ -128,3 +132,187 @@ def compare_bodies(rendered: dict, remote: dict) -> list[str]:
                 f"{key}: expected {_canon(rendered[key])}, got {_canon(kept[key])}"
             )
     return diffs
+
+
+# --- The command runner -------------------------------------------------------------
+
+# The organisation that must never be touched, compared without letter case.
+UPSTREAM_ORG = "superclaude-org"
+
+TIMEOUT_SECONDS = 60
+
+
+@dataclass(frozen=True)
+class Result:
+    returncode: int
+    stdout: str
+    stderr: str
+
+
+# What a call that ran into TIMEOUT_SECONDS returns (never a hang).
+TIMED_OUT = Result(124, "", f"timed out after {TIMEOUT_SECONDS} seconds")
+
+
+@dataclass
+class CommandRecord:
+    """One accepted call. ``stdin_name`` is the ``name`` of a posted ruleset body."""
+
+    argv: list[str]
+    stdin_name: str | None = None
+
+
+class RefusedCommand(Exception):
+    """A call the allowlist or the read-only mode refused; no process was started."""
+
+
+def check_org(org: str) -> str:
+    """The organisation name, or ValueError for an empty one or the upstream one."""
+    if not org or not _SEGMENT.fullmatch(org):
+        raise ValueError(f"not an organisation name: {org!r}")
+    if org.lower() == UPSTREAM_ORG:
+        raise ValueError("the upstream organisation is never touched")
+    return org
+
+
+# One path segment: starts with a letter, digit, underscore or dot (never a dash, so
+# it cannot look like an option); "." and ".." are rejected where segments are checked.
+_SEGMENT = re.compile(r"[A-Za-z0-9_.][A-Za-z0-9_.-]*")
+_QUERY_VALUE = re.compile(r"[A-Za-z0-9_.:/-]+")
+_SHA = re.compile(r"[0-9a-f]{7,40}")
+_ID = re.compile(r"[0-9]+")
+
+# The query keys each kind of call may carry; a kind not listed carries none.
+_QUERY_KEYS = {
+    "activity": {"ref", "time_period", "per_page"},
+    "commits": {"sha", "since", "per_page"},
+    "rulesets": {"per_page"},
+    "tags": {"per_page"},
+}
+# The list calls that may follow their pages.
+_PAGINATED = frozenset(_QUERY_KEYS)
+
+
+def _plain(parts: list[str]) -> bool:
+    return bool(parts) and all(
+        _SEGMENT.fullmatch(p) and p not in (".", "..") for p in parts
+    )
+
+
+def _kind(tail: list[str]) -> str:
+    """Which allowed call a path below ``repos/<org>/<repo>`` is, or RefusedCommand."""
+    if not tail:
+        return "repo"
+    if tail[0] == "branches" and _plain(tail[1:]):
+        return "protection" if len(tail) > 2 and tail[-1] == "protection" else "branch"
+    if tail == ["rulesets"]:
+        return "rulesets"
+    if len(tail) == 2 and tail[0] == "rulesets" and _ID.fullmatch(tail[1]):
+        return "ruleset"
+    if tail in (["activity"], ["commits"]):
+        return tail[0]
+    if len(tail) == 3 and tail[0] == "commits" and tail[2] == "pulls":
+        return "pulls" if _SHA.fullmatch(tail[1]) else ""
+    if tail == ["git", "matching-refs", "tags", "v"]:
+        return "tags"
+    return ""
+
+
+def _check_path(path: str) -> str:
+    """Check a ``gh api`` path against the allowed shapes; return its kind."""
+    base, _, query = path.partition("?")
+    parts = base.split("/")
+    if len(parts) < 3 or parts[0] != "repos" or not _plain(parts[1:3]):
+        raise RefusedCommand(f"path not under repos/<org>/<repo>: {path}")
+    try:
+        check_org(parts[1])
+    except ValueError as exc:
+        raise RefusedCommand(str(exc)) from exc
+    kind = _kind(parts[3:])
+    if not kind:
+        raise RefusedCommand(f"path not on the allowlist: {path}")
+    allowed = _QUERY_KEYS.get(kind, set())
+    for pair in query.split("&") if query else []:
+        key, eq, value = pair.partition("=")
+        if not eq or key not in allowed or not _QUERY_VALUE.fullmatch(value):
+            raise RefusedCommand(f"query not on the allowlist: {path}")
+    return kind
+
+
+@dataclass
+class Runner:
+    """The only way this script starts an outside program.
+
+    ``check_allowed`` is a positive allowlist: ``gh api`` calls under
+    ``repos/<org>/<repo>`` of the shapes this script needs, and nothing else. Every
+    accepted call is recorded. A runner built with ``read_only=True`` (the dry run)
+    refuses POST before any process starts.
+    """
+
+    read_only: bool = False
+    commands: list[CommandRecord] = field(default_factory=list)
+
+    def check_allowed(self, argv: list[str], stdin: str | None = None) -> str | None:
+        """Raise RefusedCommand unless ``argv`` is allowed. Return the ``name`` of the
+        posted body for a POST, else None."""
+        if not argv or argv[0] != "gh" or argv[1:2] != ["api"]:
+            raise RefusedCommand("only gh api calls are allowed")
+        method = source = path = None
+        paginate = False
+        i = 2
+        while i < len(argv):
+            token = argv[i]
+            if token == "--method" and method is None and i + 1 < len(argv):
+                method, i = argv[i + 1], i + 2
+            elif token == "--input" and source is None and i + 1 < len(argv):
+                source, i = argv[i + 1], i + 2
+            elif token == "--paginate" and not paginate:
+                paginate, i = True, i + 1
+            elif token and not token.startswith("-") and path is None:
+                path, i = token, i + 1
+            else:
+                raise RefusedCommand(f"gh api option not allowed: {token!r}")
+        if path is None:
+            raise RefusedCommand("gh api needs a path")
+        kind = _check_path(path)
+        if method is None:
+            if source is not None or (paginate and kind not in _PAGINATED):
+                raise RefusedCommand("option not allowed on this read")
+            return None
+        if method != "POST" or kind != "rulesets" or "?" in path:
+            raise RefusedCommand("POST is allowed only on repos/<org>/<repo>/rulesets")
+        if source != "-" or paginate or not stdin:
+            raise RefusedCommand("a POST sends its body on stdin (--input -)")
+        try:
+            name = json.loads(stdin)["name"]
+        except (ValueError, TypeError, KeyError) as exc:
+            raise RefusedCommand("a POST body must be a ruleset with a name") from exc
+        if not isinstance(name, str) or not name:
+            raise RefusedCommand("a POST body must be a ruleset with a name")
+        return name
+
+    def run(self, argv: list[str], stdin: str | None = None) -> Result:
+        name = self.check_allowed(argv, stdin)
+        if self.read_only and name is not None:
+            raise RefusedCommand("read-only runner: POST refused")
+        self.commands.append(CommandRecord(list(argv), name))
+        return self._execute(argv, stdin)
+
+    def _execute(self, argv: list[str], stdin: str | None) -> Result:
+        env = dict(os.environ, GH_PROMPT_DISABLED="1")
+        try:
+            proc = subprocess.run(
+                argv,
+                input=stdin,
+                capture_output=True,
+                text=True,
+                encoding="utf-8",
+                errors="replace",
+                timeout=TIMEOUT_SECONDS,
+                env=env,
+                check=False,
+            )
+        except subprocess.TimeoutExpired:
+            return TIMED_OUT
+        except OSError as exc:
+            return Result(127, "", f"{type(exc).__name__}: {exc}")
+        return Result(proc.returncode, proc.stdout, proc.stderr)
diff --git a/tests/org_rulesets/conftest.py b/tests/org_rulesets/conftest.py
index bd1a1dea3..2bca4720c 100644
--- a/tests/org_rulesets/conftest.py
+++ b/tests/org_rulesets/conftest.py
@@ -1,14 +1,16 @@
 """Shared test support for scripts/apply_org_rulesets.py.
 
-Tests never call GitHub: every ``gh`` call goes through a fake runner defined here that
-answers from canned replies. Names are synthetic (``acme-one``). Every shared fixture is
-defined in this file only: a fixture imported into several test modules is listed more
-than once by ``pytest --fixtures``, which crashes on the tie (CI runs that command).
+Tests never call GitHub: every ``gh`` call goes through the fake runner below, which
+subclasses the real ``Runner`` and overrides only ``_execute``, so each call still passes
+the real allowlist. Names are synthetic (``acme-one``). Every shared fixture is defined
+in this file only: a fixture imported into several test modules is listed more than
+once by ``pytest --fixtures``, which crashes on the tie (CI runs that command).
 """
 
 from __future__ import annotations
 
 import importlib.util
+import json
 import sys
 from pathlib import Path
 
@@ -30,3 +32,49 @@ def load_script():
 def orr():
     """The script module, loaded once."""
     return load_script()
+
+
+@pytest.fixture(scope="session")
+def fake_runner_cls(orr):
+    """A Runner that never starts a process.
+
+    ``replies`` maps ``(method, path)`` to an answer. The path is the full path with its
+    query or, failing that, without it. An answer is a ``Result``, a callable
+    ``(argv, stdin) -> Result``, or a list of those served in order (so three POSTs to
+    ``rulesets`` can return three ids). A call with no canned answer gets return code
+    127. ``executed`` lists every call that reached ``_execute`` (a refused call never
+    does).
+    """
+
+    class FakeRunner(orr.Runner):
+        def __init__(self, replies=None, read_only=False):
+            super().__init__(read_only=read_only)
+            self.replies = dict(replies or {})
+            self.executed = []
+
+        @staticmethod
+        def ok(data):
+            return orr.Result(0, json.dumps(data), "")
+
+        @staticmethod
+        def method_of(argv):
+            return argv[argv.index("--method") + 1] if "--method" in argv else "GET"
+
+        @staticmethod
+        def path_of(argv):
+            return next(t for t in argv[2:] if t.startswith("repos/"))
+
+        def _execute(self, argv, stdin):
+            self.executed.append((list(argv), stdin))
+            method, full = self.method_of(argv), self.path_of(argv)
+            for key in ((method, full), (method, full.partition("?")[0])):
+                if key in self.replies:
+                    answer = self.replies[key]
+                    if isinstance(answer, list):
+                        if not answer:
+                            break
+                        answer = answer.pop(0)
+                    return answer(argv, stdin) if callable(answer) else answer
+            return orr.Result(127, "", f"no canned reply for {argv}")
+
+    return FakeRunner
diff --git a/tests/org_rulesets/test_runner.py b/tests/org_rulesets/test_runner.py
new file mode 100644
index 000000000..eb50abdf7
--- /dev/null
+++ b/tests/org_rulesets/test_runner.py
@@ -0,0 +1,228 @@
+"""The allowlisted Runner, check_org and the fake runner of conftest."""
+
+from __future__ import annotations
+
+import json
+import re
+import subprocess
+
+import pytest
+
+REPO = "repos/acme/acme-one"
+BODY = json.dumps({"name": "protect-master"})
+
+ACCEPTED = [
+    ["gh", "api", REPO],
+    ["gh", "api", f"{REPO}/branches/master"],
+    ["gh", "api", f"{REPO}/branches/release/1.0"],
+    ["gh", "api", f"{REPO}/branches/master/protection"],
+    ["gh", "api", f"{REPO}/rulesets"],
+    ["gh", "api", "--paginate", f"{REPO}/rulesets?per_page=100"],
+    ["gh", "api", f"{REPO}/rulesets/12"],
+    [
+        "gh",
+        "api",
+        "--paginate",
+        f"{REPO}/activity?ref=refs/heads/master&time_period=quarter&per_page=100",
+    ],
+    ["gh", "api", f"{REPO}/commits?sha=master&since=2026-08-28T17:25:08Z"],
+    ["gh", "api", f"{REPO}/commits/abc1234def/pulls"],
+    ["gh", "api", f"{REPO}/git/matching-refs/tags/v"],
+    ["gh", "api", "--paginate", f"{REPO}/git/matching-refs/tags/v"],
+]
+POST = ["gh", "api", "--method", "POST", f"{REPO}/rulesets", "--input", "-"]
+
+REFUSED = [
+    [],
+    [""],
+    ["git", "status"],
+    ["gh"],
+    ["gh", "pr", "list"],
+    ["gh", "api"],
+    ["gh", "api", "user"],
+    ["gh", "api", f"{REPO}/hooks"],
+    ["gh", "api", f"{REPO}/keys"],
+    ["gh", "api", f"{REPO}/installations"],
+    ["gh", "api", f"{REPO}/branches"],
+    ["gh", "api", f"{REPO}/rulesets/abc"],
+    ["gh", "api", f"{REPO}/commits/xyz/pulls"],
+    ["gh", "api", f"{REPO}/git/matching-refs/heads/v"],
+    ["gh", "api", "repos/-x/acme-one"],
+    ["gh", "api", "repos/acme/-one"],
+    ["gh", "api", f"{REPO}/branches/-x"],
+    ["gh", "api", f"{REPO}/branches/../rulesets"],
+    ["gh", "api", f"{REPO}/branches/a~b"],
+    ["gh", "api", f"{REPO}/branches/master/protection/"],
+    ["gh", "api", "repos/acme/.."],
+    ["gh", "api", "repos/acme/acme-one/../other"],
+    ["gh", "api", "repos/SuperClaude-Org/acme-one"],
+    ["gh", "api", "repos/superclaude-org/acme-one"],
+    ["gh", "api", REPO, "--jq", ".name"],
+    ["gh", "api", REPO, "-X", "DELETE"],
+    ["gh", "api", "--method", "DELETE", f"{REPO}/rulesets/12"],
+    ["gh", "api", "--method", "PUT", f"{REPO}/rulesets/12", "--input", "-"],
+    ["gh", "api", "--method", "GET", REPO],
+    ["gh", "api", REPO, "--input", "-"],
+    ["gh", "api", "--paginate", REPO],
+    ["gh", "api", f"{REPO}/rulesets?evil=1"],
+    ["gh", "api", f"{REPO}/rulesets?per_page"],
+    ["gh", "api", REPO, f"{REPO}/rulesets"],
+    ["gh", "api", REPO, "--paginate", "--paginate"],
+]
+
+
+def test_refused_calls_never_reach_execute(fake_runner_cls, orr):
+    runner = fake_runner_cls()
+    for argv in REFUSED:
+        with pytest.raises(orr.RefusedCommand):
+            runner.run(argv)
+    assert runner.executed == []
+    assert runner.commands == []
+
+
+@pytest.mark.parametrize(
+    "bad_post",
+    [
+        POST[:-2],
+        POST[:-1] + ["x"],
+        ["gh", "api", "--method", "POST", REPO, "--input", "-"],
+        ["gh", "api", "--method", "POST", f"{REPO}/rulesets/12", "--input", "-"],
+        ["gh", "api", "--method", "POST", f"{REPO}/rulesets?x=1", "--input", "-"],
+        ["gh", "api", "--method", "POST", "--paginate", f"{REPO}/rulesets"]
+        + ["--input", "-"],
+    ],
+)
+def test_bad_posts_are_refused(fake_runner_cls, orr, bad_post):
+    runner = fake_runner_cls()
+    with pytest.raises(orr.RefusedCommand):
+        runner.run(bad_post, BODY)
+    assert runner.executed == []
+
+
+@pytest.mark.parametrize("stdin", [None, "", "not json", "[]", "{}", '{"name": 3}'])
+def test_a_post_needs_a_body_with_a_name(fake_runner_cls, orr, stdin):
+    runner = fake_runner_cls()
+    with pytest.raises(orr.RefusedCommand):
+        runner.run(POST, stdin)
+    assert runner.executed == []
+
+
+def test_read_only_runner_refuses_post_but_reads(fake_runner_cls, orr):
+    runner = fake_runner_cls(read_only=True)
+    with pytest.raises(orr.RefusedCommand):
+        runner.run(POST, BODY)
+    assert runner.executed == [] and runner.commands == []
+    runner.run(["gh", "api", REPO])
+    assert len(runner.executed) == 1
+
+
+def test_normal_runner_accepts_a_post_and_records_its_name(fake_runner_cls):
+    runner = fake_runner_cls(
+        {("POST", f"{REPO}/rulesets"): fake_runner_cls.ok({"id": 5})}
+    )
+    result = runner.run(POST, BODY)
+    assert result.returncode == 0
+    assert runner.commands[0].stdin_name == "protect-master"
+    assert runner.executed == [(POST, BODY)]
+
+
+def test_check_org(orr):
+    for bad in (
+        "SuperClaude-Org",
+        "superclaude-org",
+        "SUPERCLAUDE-ORG",
+        "",
+        "-x",
+        "a/b",
+    ):
+        with pytest.raises(ValueError):
+            orr.check_org(bad)
+    assert orr.check_org("acme") == "acme"
+
+
+def test_every_accepted_call_is_an_allowed_shape(fake_runner_cls):
+    runner = fake_runner_cls()
+    for argv in ACCEPTED:
+        runner.run(argv)
+    runner.run(POST, BODY)
+    assert len(runner.commands) == len(ACCEPTED) + 1
+    shape = re.compile(
+        r"^repos/acme/acme-one(/(branches/[\w./-]+|rulesets(/\d+)?|activity|commits"
+        r"|commits/[0-9a-f]+/pulls|git/matching-refs/tags/v))?(\?[\w=&:./-]+)?$"
+    )
+    for record in runner.commands:
+        assert record.argv[:2] == ["gh", "api"]
+        assert shape.match(runner.path_of(record.argv)), record.argv
+    assert len(runner.executed) == len(runner.commands)
+
+
+def test_replies_are_keyed_by_method_and_path(fake_runner_cls, orr):
+    ok = fake_runner_cls.ok
+    seen = []
+
+    def echo(argv, stdin):
+        seen.append(stdin)
+        return ok({"echo": True})
+
+    runner = fake_runner_cls(
+        {
+            ("GET", f"{REPO}/rulesets"): ok([]),
+            ("GET", f"{REPO}/rulesets?per_page=100"): ok(["paged"]),
+            ("POST", f"{REPO}/rulesets"): [ok({"id": 1}), ok({"id": 2}), echo],
+        }
+    )
+    assert json.loads(runner.run(["gh", "api", f"{REPO}/rulesets"]).stdout) == []
+    paged = runner.run(["gh", "api", f"{REPO}/rulesets?per_page=100"])
+    assert json.loads(paged.stdout) == ["paged"]
+    ids = [json.loads(runner.run(POST, BODY).stdout) for _ in range(2)]
+    assert ids == [{"id": 1}, {"id": 2}]
+    assert runner.run(POST, BODY).returncode == 0 and seen == [BODY]
+    # the list is used up, and a path with no reply gets 127
+    assert runner.run(POST, BODY).returncode == 127
+    assert runner.run(["gh", "api", REPO]).returncode == 127
+
+
+def test_timeout_becomes_the_named_result(orr, monkeypatch):
+    seen = {}
+
+    def stub(argv, **kwargs):
+        seen.update(kwargs)
+        raise subprocess.TimeoutExpired(argv, kwargs["timeout"])
+
+    monkeypatch.setattr(subprocess, "run", stub)
+    result = orr.Runner().run(["gh", "api", REPO])
+    assert result == orr.TIMED_OUT
+    assert result.returncode == 124
+    assert seen["timeout"] == orr.TIMEOUT_SECONDS
+
+
+def test_a_missing_program_is_a_127_result(orr, monkeypatch):
+    def stub(argv, **kwargs):
+        raise FileNotFoundError("gh")
+
+    monkeypatch.setattr(subprocess, "run", stub)
+    assert orr.Runner().run(["gh", "api", REPO]).returncode == 127
+
+
+def test_a_refused_call_starts_no_process(orr, monkeypatch):
+    def stub(argv, **kwargs):
+        raise AssertionError("a process was started")
+
+    monkeypatch.setattr(subprocess, "run", stub)
+    with pytest.raises(orr.RefusedCommand):
+        orr.Runner().run(["git", "status"])
+    with pytest.raises(orr.RefusedCommand):
+        orr.Runner(read_only=True).run(POST, BODY)
+
+
+def test_the_real_runner_passes_stdin_and_returns_output(orr, monkeypatch):
+    seen = {}
+
+    def stub(argv, **kwargs):
+        seen.update(kwargs)
+        return subprocess.CompletedProcess(argv, 0, stdout="out", stderr="err")
+
+    monkeypatch.setattr(subprocess, "run", stub)
+    result = orr.Runner().run(POST, BODY)
+    assert (result.returncode, result.stdout, result.stderr) == (0, "out", "err")
+    assert seen["input"] == BODY

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
