4c11643e16e94ee6df28c157dda026866c7376e0
Review one task for spec compliance.

Task brief: ## Task 19: Generate one repo's configuration, approvers file and state directory

Create `src/superclaude/cli/issue_watch/generate.py` with `ensure_config(repo_record, defaults, runner, base)` where `base` holds the config directory and the state directory (defaults `~/.config/superclaude` and `~/.local/state/superclaude`). For a repo that has no file at `<config dir>/issue-watch.d/<name>.json` it: reads the account id with `gh api user` (requirement R2); finds the Project with the GraphQL query `repository(owner, name){ projectsV2(first:10){ nodes{ id number title } } }` (R3): zero Projects gives a skip with reason `no_project`, several use the id from the defaults map or give the skip reason `project_ambiguous`; reads maintainers with `gh api "repos/<owner>/<name>/collaborators?permission=maintain"` and adds them to the fixed approvers' account ids (R4; fixed logins are turned into ids with `gh api users/<login>`); writes `<config dir>/issue-watch.d/<name>-approvers.txt` (mode 600, one id per line) and the config JSON (mode 600) with absolute `worktree` (`/home/coder/workspaces/worktrees/<name>/Coordinator`), `approvers_file`, an explicit absolute `state_dir` of `<state dir>/issue-watch/<name>` (R12), the `repo`, the Project id, the account id and `enabled: false`. The generator never writes the launch account's own id into a generated approvers file (the warn-only exclusion of Task 9 stays the owner's choice for a hand-written one). The result is validated with `cycle.load_config` and `cycle.validate_approvers` before it is kept; a file that exists is never overwritten.

Depends on: Task 9, Task 12, Task 16, Task 17, Task 18

Acceptance criteria:
- T19.AC1: New `tests/issue_watch/test_generate.py` covers: a repo with one Project, none, several with and without a defaults entry, a failed account read, maintainers added, the launch account id never written to the approvers file, an existing config left untouched, file modes 600, and two repos getting two different `state_dir` values; every path is under `tmp_path` and the test asserts nothing was written under the real home.
- T19.AC2: A generated config passes `cycle.load_config` in the test, and `uv run pytest tests/issue_watch -q` passes.
- T19.AC3: The module issues only read calls to GitHub (`gh api user`, `gh api users/<login>`, the Project query, the collaborators call), each REST call with `--method GET`, and its argv builders are covered by the scan Task 12 extends.
Global constraints: ## Constraints

- Scope is the IronClaude repository only. The Coder template work (requirements R1, R6, R9, R10, R17, R20, R21; Coder issues 515 and 516) is not implemented here; Task 27 hands it over with exact values.
- This plan applies requirement R33, which adopts the remediation proposal `.dev/remediation/watcher-plan-v3/remediation-proposal.md` with the owner's answers of 2026-11-19: the ship gate stays closed, the `updatedAt` observation is run, self-approval is warn-only, `~/.config/superclaude` joins the guard's tamper tokens, all four pipelines end at In review, and the extra guard refusals are confirmed. It also applies requirement R34, the five blocking corrections of the fourth review (P4-1 to P4-5): the coordinator's approval read names its repo (Tasks 15 and 16), an empty Pipeline has no time to compare (Tasks 3 and 5), the claim-time approval refusal is tested where it is enforced (Task 11), the guard pattern for `issue-pipeline complete` is anchored on the verb word (Task 13), and the worker brief is tested at level `none` only (Tasks 6, 10 and 11).
- This plan applies requirement R35 (owner decision of 2026-11-19): the approval is no longer the label `issue-watch:approved`. It is the organization issue field `Approved` (single select, one option `Yes`, field id 50144115 on `IronbellyOrg`) set to `Yes` by an allowed approver (IronBelly, Clay or a maintainer, the approvers file of today). The trigger label `issue-watch:trigger` stays. Who set the field and when comes from the issue's GraphQL timeline events `IssueFieldAddedEvent`, `IssueFieldChangedEvent` and `IssueFieldRemovedEvent` (each carries `actor`, `createdAt`, `issueField` and the value; verified read-only on 2026-11-19 against issue 675 with another field), because the REST events endpoint names the event but not the field or the value. Task 4a builds the read; the approval predicates, the approval-void rule and the claim-time refusal keep their logic and see the field events as label events named by `approval_label`. A real label with the old name never approves. Task 4 is amended to observe the field instead of the label; the plan was copied from `TASK-WF-requirements-20261119-143917` (Tasks 1 to 3 complete there) and edited by owner instruction, and `source.md` still carries the label wording of the requirements file (Task 28 updates the requirements file).
- Edit `src/superclaude/`, then run `make sync-dev` and `make verify-sync`. Never edit or stage anything under `.claude/` (only `.claude/settings.json` is tracked). The tracked plugin mirror `plugins/superclaude/hooks/scripts/launch-level-guard.sh` is changed together with its source.
- Python only through UV (`uv run pytest`, `uv run ruff`). Tests use the faked `gh` and Orca runners already in `tests/issue_watch/conftest.py`; no task runs the watcher against the real GitHub or Orca, except the read-only schema check of Task 3 and the read-only reads of Task 4.
- `src/superclaude/cli/issue_watch/github.py` stays read-only: no mutation, no POST to a REST path (security invariant NG-2, `tests/issue_watch/test_security_invariants.py`). The only modules that write to GitHub are two new ones outside `github.py`: `src/superclaude/cli/issue_pipeline/complete.py` (Task 12: result comment and Status move, run only by the coordinator) and `src/superclaude/cli/issue_watch/repo_init.py` (Task 20: labels).
- Only the coordinator writes to an issue, a label or a Project item (owner decision of 2026-11-19; `src/superclaude/core/WORKER-CONTRACT.md` lines 241 to 243 and 300), and only under that issue's grant row. An agent launched at Worktree, Full or Full Submit, and every worker, never runs `issue-pipeline complete`, never posts an issue comment and never changes a label or a Project field; it reports through its result file `.dev/issues/<N>/result.md`. The launch-level guard refuses every `gh issue`, `gh label` and `gh project` write at every level, Full Submit included (Task 13), and every `gh api` write at every level. This is a text check on `gh` commands only: a script or another HTTP client is not seen. The complete control is a token with no issues or projects write for launched agents (a Coder row, owner decision). This is the one place the plan goes beyond issue verbs.
- Governed means a session with a record in the launch-level store: the agents launched at Worktree, Full and Full Submit, and bound workers. Not governed: the watcher-launched `--pipeline none` claim session and the coordinator. The claim session's two marked comments are allowed by design, and it reads untrusted issue text under the launch login.
- The approval (the `Approved` issue field set to Yes, R35), the allowed Project Status, the approval-void rule of Task 5 and the "edited after approval" refusal (`predicates.py`) stay the gate. Nothing in this plan removes or auto-satisfies them. The plan-hash approval row (`src/superclaude/cli/issue_pipeline/approval_record.py`) is created only from a worker's `ask` that carries the plan hash (`WORKER-CONTRACT.md`, WC-17), never from claim-time fields. Approval by the launch account is accepted unless the owner sets the exclusion key `approval_excluded_ids` (Task 9, warn-first).
- The cron watcher may launch every Pipeline level as a capability (owner, 2026-11-19), but the ship gate of Task 8 is closed: until a reviewed commit flips `GOVERNED_LEVELS_ALLOWED` and un-skips the launch-level observations (`tests/hooks/test_launch_level_observations.py`), only Pipeline None launches and every other level ends `level_gated`. Full Submit commits, pushes a feature branch to `origin` and runs `/sc:pr-submit --monitor 3`; it never merges. For an issue the owner has put at Full Submit and approved with the `Approved` field after the last Project change, that setting is the person's go for that issue's push and pull request, and nothing else is pushed.
- `~/.config/superclaude` was not in the guard's tamper tokens (guard line 764); Task 13 adds it. Until that lands, the exclusion key and any future config key are as writable as the approvers file, so the exclusion limits an honest but injected session, not a hostile one.
- The term is "coordinator", never "orchestrator". The coordinator branch and worktree are both named `Coordinator`; the session is named `COORD-<RepoName>`.
- Tasks that edit the same file run in plan order, never in parallel: `cycle.py` (Tasks 4a, 5, 7, 8, 9, 16, 22), `launch.py` (Tasks 7, 8, 16), `github.py` (Tasks 3, 4a, 15), `predicates.py` (Tasks 1, 3, 5, 7, 9), `audit.py` (Task 8), `launch-level-guard.sh` (Task 13), `WORKER-CONTRACT.md` (Tasks 11, 14), `issue_pipeline/cli.py` (Tasks 14, 15, 16), `issue_pipeline/reads.py` (Task 15), `test_security_invariants.py` (Tasks 3, 4a, 7, 12, 15). Task 1 leaves `cycle.py` unchanged.
- Every new module that writes under the user's home takes an injectable base directory, and its tests run with every path inside `tmp_path` and assert nothing was written under the real home.
- Do not switch any real watcher on, claim a real issue, install a real cron entry, move a real issue's Status or start a worker for a real issue. Each generated config starts with `enabled: false` and only the automatic first-run check of Task 21 may turn it on.
Start sha: 4c11643e16e94ee6df28c157dda026866c7376e0
Diff against the start snapshot: diff --git a/tests/issue_watch/test_module_boundaries.py b/tests/issue_watch/test_module_boundaries.py
index ff77ab74b..b54c6e126 100644
--- a/tests/issue_watch/test_module_boundaries.py
+++ b/tests/issue_watch/test_module_boundaries.py
@@ -73,6 +73,10 @@ RULES: dict[str, Rule] = {
     "defaults": Rule(siblings=frozenset({"cycle", "github", "predicates"})),
     # plan Task 18: the Orca repo list; commands only through the Runner, no subprocess import.
     "repos": Rule(siblings=frozenset({"runner", "launch"})),
+    # plan Task 19: one repo's generated config; reads through the Runner, writes two files.
+    "generate": Rule(
+        siblings=frozenset({"cycle", "defaults", "github", "repos", "runner"})
+    ),
     "cli": Rule(
         siblings=frozenset({"cycle", "record", "audit", "launch", "runner"}),
         third_party=frozenset({"click"}),
diff --git a/tests/issue_watch/test_security_invariants.py b/tests/issue_watch/test_security_invariants.py
index 48e4989ec..1e4463bc6 100644
--- a/tests/issue_watch/test_security_invariants.py
+++ b/tests/issue_watch/test_security_invariants.py
@@ -1099,3 +1099,34 @@ def test_the_read_calls_of_complete_py_are_get_or_read_only_graphql():
         assert not _TEXT_FIELD.search(
             " ".join(a for a in argv if a.startswith("query="))
         ), argv
+
+
+def test_the_argv_builders_of_the_generator_are_reads_with_no_text_field():
+    """Plan Task 19: generate.py only reads; the scan covers its argv builders too."""
+    from superclaude.cli.issue_watch import generate
+
+    argvs = [
+        generate.argv_account(),
+        generate.argv_user_id("ironbelly"),
+        generate.argv_projects("IronbellyOrg/IronClaude"),
+        generate.argv_maintainers("IronbellyOrg/IronClaude"),
+    ]
+    for argv in argvs:
+        assert argv[:2] == ["gh", "api"], argv
+        assert not any(UPSTREAM.lower() in a.lower() for a in argv), argv
+        assert not any(a.upper() in ("POST", "PUT", "PATCH", "DELETE") for a in argv)
+        assert not any("mutation" in a.lower() for a in argv), argv
+        if argv[2] == "graphql":
+            query = next(a for a in argv if a.startswith("query="))
+            assert query.startswith("query=query(") and not _TEXT_FIELD.search(query)
+        else:
+            assert argv[2:4] == ["--method", "GET"], argv
+        assert not any(_TEXT_FIELD.search(a) for a in argv if a.startswith("query="))
+    for bad in ("a/b/c", "", "a b/c", "-a/b"):
+        with pytest.raises(ValueError):
+            generate.argv_projects(bad)
+        with pytest.raises(ValueError):
+            generate.argv_maintainers(bad)
+    for bad in ("-x", "a b", "", "a/b", "x" * 40):
+        with pytest.raises(ValueError):
+            generate.argv_user_id(bad)
diff --git a/src/superclaude/cli/issue_watch/generate.py b/src/superclaude/cli/issue_watch/generate.py
new file mode 100644
index 000000000..d4c35e82a
--- /dev/null
+++ b/src/superclaude/cli/issue_watch/generate.py
@@ -0,0 +1,285 @@
+"""Generate one repository's watcher configuration (plan Task 19, requirements R2 to R4, R12).
+
+For a repository with no ``<config dir>/issue-watch.d/<name>.json`` this module reads four things
+from GitHub (every call is a read), then writes the approvers file and the config, both mode 600:
+
+1. the launch account: ``gh api user`` (R2);
+2. the repository's Project: a GraphQL read of ``projectsV2`` (R3). None gives the skip reason
+   ``no_project``; several use the id of the defaults map when it names one of them, else give
+   ``project_ambiguous``;
+3. the approvers (R4): the fixed logins of the defaults, turned into account ids with
+   ``gh api users/<login>``, plus the repository's maintainers from
+   ``gh api repos/<owner>/<name>/collaborators?permission=maintain``. The launch account's own
+   id is never written to a generated approvers file (the warn-only exclusion of Task 9 stays the
+   owner's choice for a hand-written one).
+
+The result is checked with ``cycle.load_config`` and ``cycle.validate_approvers`` before it is
+kept. A file that exists is never overwritten, and a generated config starts ``enabled: false``.
+The ``state_dir`` is an explicit absolute path per repository (R12), so two repositories never
+share state; this module does not create it (the first run does).
+
+Every command runs through the ``Runner`` (an argv list, no shell). The GitHub calls are reads:
+each REST call carries ``--method GET`` and the GraphQL call is a query.
+"""
+
+from __future__ import annotations
+
+import json
+import os
+import re
+from dataclasses import dataclass
+from pathlib import Path
+
+from . import cycle
+from .defaults import Defaults
+from .github import _repo_arg
+from .repos import OrcaRepo
+from .runner import CommandResult, Runner
+
+TIMEOUT_S = 30.0
+WORKTREES_DIR = "/home/coder/workspaces/worktrees"
+DEFAULT_CONFIG_DIR = "~/.config/superclaude"
+DEFAULT_STATE_DIR = "~/.local/state/superclaude"
+SUBDIR = "issue-watch.d"
+
+_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,99}")
+_LOGIN = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}")
+_ID_MAX = 10**20 - 1
+
+PROJECTS_QUERY = """query($owner: String!, $name: String!) {
+  repository(owner: $owner, name: $name) {
+    projectsV2(first: 10) {
+      nodes { id number }
+    }
+  }
+}"""
+"""The repository's Projects (R3): only ids and numbers are read."""
+
+
+@dataclass(frozen=True)
+class Base:
+    """Where one generated configuration and its state live."""
+
+    config_dir: Path
+    state_dir: Path
+    worktrees_dir: Path
+
+    @classmethod
+    def default(cls) -> Base:
+        return cls(
+            Path(DEFAULT_CONFIG_DIR).expanduser(),
+            Path(DEFAULT_STATE_DIR).expanduser(),
+            Path(WORKTREES_DIR),
+        )
+
+
+@dataclass(frozen=True)
+class Outcome:
+    """``generated``, ``exists`` (left untouched) or ``skipped`` with a closed reason."""
+
+    status: str
+    name: str
+    reason: str | None = None
+    config_path: Path | None = None
+    approvers_path: Path | None = None
+    state_dir: Path | None = None
+
+
+# --- argv builders: every one is a read ---------------------------------------------------
+
+
+def argv_account() -> list[str]:
+    return ["gh", "api", "--method", "GET", "user", "--jq", "{id}"]
+
+
+def argv_user_id(login: str) -> list[str]:
+    if not _LOGIN.fullmatch(login):
+        raise ValueError("invalid login")
+    return ["gh", "api", "--method", "GET", f"users/{login}", "--jq", "{id}"]
+
+
+def argv_projects(repo: str) -> list[str]:
+    owner, name = _repo_arg(repo).split("/")
+    return [
+        "gh",
+        "api",
+        "graphql",
+        "-f",
+        f"query={PROJECTS_QUERY}",
+        "-f",
+        f"owner={owner}",
+        "-f",
+        f"name={name}",
+    ]
+
+
+def argv_maintainers(repo: str) -> list[str]:
+    return [
+        "gh",
+        "api",
+        "--method",
+        "GET",
+        f"repos/{_repo_arg(repo)}/collaborators?permission=maintain&per_page=100",
+        "--jq",
+        "[.[] | {id}]",
+    ]
+
+
+# --- reading -----------------------------------------------------------------------------
+
+
+def _json(result: CommandResult) -> object | None:
+    if result.timed_out or result.spawn_error is not None or result.returncode != 0:
+        return None
+    try:
+        parsed = json.loads(result.stdout)
+    except ValueError:
+        return None
+    if isinstance(parsed, dict) and parsed.get("errors"):
+        return None
+    return parsed
+
+
+def _account_id(value: object) -> int | None:
+    if type(value) is int and 1 <= value <= _ID_MAX:
+        return value
+    return None
+
+
+def _read_id(runner: Runner, argv: list[str]) -> int | None:
+    data = _json(runner.run(argv, TIMEOUT_S))
+    return _account_id(data.get("id")) if isinstance(data, dict) else None
+
+
+def _projects(runner: Runner, repo: str) -> list[str] | None:
+    data = _json(runner.run(argv_projects(repo), TIMEOUT_S))
+    try:
+        nodes = data["data"]["repository"]["projectsV2"]["nodes"]  # type: ignore[index]
+        ids = [n["id"] for n in nodes]
+    except (KeyError, TypeError):
+        return None
+    if not all(
+        isinstance(i, str) and re.fullmatch(r"PVT_[A-Za-z0-9_-]{1,64}", i) for i in ids
+    ):
+        return None
+    return ids
+
+
+def _maintainers(runner: Runner, repo: str) -> set[int] | None:
+    data = _json(runner.run(argv_maintainers(repo), TIMEOUT_S))
+    if not isinstance(data, list):
+        return None
+    ids = {_account_id(row.get("id")) for row in data if isinstance(row, dict)}
+    if len(ids) != len(data) or None in ids:
+        return None
+    return {i for i in ids if i is not None}
+
+
+# --- writing -----------------------------------------------------------------------------
+
+
+def _write_new(path: Path, text: str) -> None:
+    """Create ``path`` with mode 600; never overwrite (``FileExistsError``)."""
+    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
+    with os.fdopen(fd, "w", encoding="utf-8") as handle:
+        handle.write(text)
+
+
+def _skip(name: str, reason: str) -> Outcome:
+    return Outcome("skipped", name, reason)
+
+
+def ensure_config(
+    repo_record: OrcaRepo, defaults: Defaults, runner: Runner, base: Base | None = None
+) -> Outcome:
+    """Generate ``<config dir>/issue-watch.d/<name>.json`` for ``repo_record`` when it is absent."""
+    base = base or Base.default()
+    name = repo_record.name
+    if not _NAME.fullmatch(name):
+        return _skip(name, "bad_name")
+    try:
+        repo = _repo_arg(repo_record.slug)
+    except ValueError:
+        return _skip(name, "bad_repo")
+    directory = base.config_dir.expanduser() / SUBDIR
+    config_path = directory / f"{name}.json"
+    approvers_path = directory / f"{name}-approvers.txt"
+    if config_path.exists() or config_path.is_symlink():
+        return Outcome("exists", name, config_path=config_path)
+    if approvers_path.exists() or approvers_path.is_symlink():
+        return _skip(name, "approvers_file_exists")
+
+    account = _read_id(runner, argv_account())
+    if account is None:
+        return _skip(name, "account_read_failed")
+
+    projects = _projects(runner, repo)
+    if projects is None:
+        return _skip(name, "project_read_failed")
+    if not projects:
+        return _skip(name, "no_project")
+    if len(projects) == 1:
+        project_id = projects[0]
+    else:
+        mapped = defaults.projects.get(repo)
+        if mapped is None or mapped not in projects:
+            return _skip(name, "project_ambiguous")
+        project_id = mapped
+
+    approvers: set[int] = set()
+    for login in defaults.approver_logins:
+        found = _read_id(runner, argv_user_id(login))
+        if found is None:
+            return _skip(name, "approver_read_failed")
+        approvers.add(found)
+    maintainers = _maintainers(runner, repo)
+    if maintainers is None:
+        return _skip(name, "maintainers_read_failed")
+    approvers |= maintainers
+    approvers.discard(
+        account
+    )  # the launch account never approves from a generated file
+    if not approvers:
+        return _skip(name, "no_approvers")
+
+    state_dir = base.state_dir.expanduser() / "issue-watch" / name
+    raw = {
+        "schema_version": cycle.SCHEMA_VERSION,
+        "enabled": False,
+        "repo": repo,
+        "project_id": project_id,
+        "owner_account_id": account,
+        "worktree": str(base.worktrees_dir / name / "Coordinator"),
+        "approvers_file": str(approvers_path),
+        "state_dir": str(state_dir),
+    }
+    if defaults.trigger_label != cycle.DEFAULT_TRIGGER_LABEL:
+        raw["labels"] = {"trigger": defaults.trigger_label}
+
+    directory.mkdir(parents=True, exist_ok=True)
+    directory.chmod(0o700)
+    staged = directory / f".{name}.json.new"
+    wrote_approvers = False
+    try:
+        _write_new(approvers_path, "".join(f"{i}\n" for i in sorted(approvers)))
+        wrote_approvers = True
+        staged.unlink(missing_ok=True)
+        _write_new(staged, json.dumps(raw, indent=2, sort_keys=True) + "\n")
+        cycle.load_config(staged)
+        cycle.validate_approvers(approvers_path)
+        os.link(
+            staged, config_path
+        )  # fails if the config appeared meanwhile: no overwrite
+    except (cycle.ConfigError, OSError):
+        if wrote_approvers:  # only a file this call created
+            approvers_path.unlink(missing_ok=True)
+        return _skip(name, "generated_invalid")
+    finally:
+        staged.unlink(missing_ok=True)
+    return Outcome(
+        "generated",
+        name,
+        config_path=config_path,
+        approvers_path=approvers_path,
+        state_dir=state_dir,
+    )
diff --git a/tests/issue_watch/test_generate.py b/tests/issue_watch/test_generate.py
new file mode 100644
index 000000000..501c994d9
--- /dev/null
+++ b/tests/issue_watch/test_generate.py
@@ -0,0 +1,316 @@
+"""Task 19: generate one repo's config, approvers file and state directory.
+
+Every path is under ``tmp_path``; HOME is redirected there too, so a write to the real home
+would show as a file under ``tmp_path / "home"`` and the tests assert there is none.
+"""
+
+from __future__ import annotations
+
+import json
+import os
+import stat
+from pathlib import Path
+
+import pytest
+
+from superclaude.cli.issue_watch import cycle, defaults, generate, repos
+
+from .conftest import result
+
+LAUNCH_ID = 1001
+FIXED = {"ironbelly": 11, "clayphi": 22}
+
+
+def _record(name: str = "IronClaude", slug: str = "IronbellyOrg/IronClaude"):
+    return repos.OrcaRepo("id-1", name, f"/home/u/workspaces/{name}", slug)
+
+
+def _projects_reply(*ids: str) -> str:
+    nodes = [{"id": i, "number": n} for n, i in enumerate(ids, 1)]
+    return json.dumps({"data": {"repository": {"projectsV2": {"nodes": nodes}}}})
+
+
+def _world(
+    slug: str = "IronbellyOrg/IronClaude",
+    *,
+    account=LAUNCH_ID,
+    projects=("PVT_one",),
+    maintainers=(33,),
+    fixed=None,
+):
+    """A scripted gh for one repo, keyed by the exact argv the module builds."""
+    fixed = FIXED if fixed is None else fixed
+    script = {
+        tuple(generate.argv_account()): result(stdout=json.dumps({"id": account}))
+        if account is not None
+        else result(stderr="HTTP 401", returncode=1),
+        tuple(generate.argv_projects(slug)): result(stdout=_projects_reply(*projects)),
+        tuple(generate.argv_maintainers(slug)): result(
+            stdout=json.dumps([{"id": m} for m in maintainers])
+        ),
+    }
+    for login, ident in fixed.items():
+        script[tuple(generate.argv_user_id(login))] = result(
+            stdout=json.dumps({"id": ident})
+        )
+    return script
+
+
+class Runner:
+    def __init__(self, script: dict) -> None:
+        self.script = script
+        self.calls: list[tuple[str, ...]] = []
+
+    def run(self, argv, timeout, *, cwd=None):
+        key = tuple(argv)
+        self.calls.append(key)
+        assert key in self.script, f"unscripted argv: {argv}"
+        return self.script[key]
+
+
+@pytest.fixture
+def base(tmp_path, monkeypatch) -> generate.Base:
+    monkeypatch.setenv("HOME", str(tmp_path / "home"))
+    return generate.Base(
+        tmp_path / "config", tmp_path / "state", tmp_path / "worktrees"
+    )
+
+
+def _no_write_under_home(tmp_path: Path) -> None:
+    assert not (tmp_path / "home").exists()
+    real = Path(os.path.expanduser("~")).resolve()
+    assert not (real / ".config/superclaude/issue-watch.d/GenTestOnly.json").exists()
+
+
+def _mode(path: Path) -> int:
+    return stat.S_IMODE(path.stat().st_mode)
+
+
+def test_a_repo_with_one_project_gets_a_valid_disabled_config(tmp_path, base) -> None:
+    runner = Runner(_world())
+    out = generate.ensure_config(_record(), defaults.Defaults(), runner, base)
+    assert out.status == "generated" and out.reason is None
+    config = out.config_path
+    assert config == base.config_dir / "issue-watch.d" / "IronClaude.json"
+    raw = json.loads(config.read_text())
+    assert raw["enabled"] is False
+    assert raw["repo"] == "IronbellyOrg/IronClaude"
+    assert raw["project_id"] == "PVT_one"
+    assert raw["owner_account_id"] == LAUNCH_ID
+    assert raw["worktree"] == str(base.worktrees_dir / "IronClaude" / "Coordinator")
+    assert raw["state_dir"] == str(base.state_dir / "issue-watch" / "IronClaude")
+    assert raw["approvers_file"] == str(
+        base.config_dir / "issue-watch.d" / "IronClaude-approvers.txt"
+    )
+    loaded = cycle.load_config(config)  # the generated config passes the real loader
+    assert loaded.enabled is False and loaded.repo == "IronbellyOrg/IronClaude"
+    assert cycle.validate_approvers(loaded.approvers_file) == {11, 22, 33}
+    _no_write_under_home(tmp_path)
+
+
+def test_file_modes_are_600_and_the_directory_is_700(tmp_path, base) -> None:
+    out = generate.ensure_config(_record(), defaults.Defaults(), Runner(_world()), base)
+    assert _mode(out.config_path) == 0o600
+    assert _mode(out.approvers_path) == 0o600
+    assert _mode(out.config_path.parent) == 0o700
+    assert list(out.config_path.parent.glob(".*")) == []  # no staged file is left
+
+
+def test_no_project_is_a_skip_with_nothing_written(tmp_path, base) -> None:
+    runner = Runner(_world(projects=()))
+    out = generate.ensure_config(_record(), defaults.Defaults(), runner, base)
+    assert (out.status, out.reason) == ("skipped", "no_project")
+    assert not base.config_dir.exists()
+
+
+def test_several_projects_without_a_defaults_entry_are_ambiguous(
+    tmp_path, base
+) -> None:
+    runner = Runner(_world(projects=("PVT_a", "PVT_b")))
+    out = generate.ensure_config(_record(), defaults.Defaults(), runner, base)
+    assert (out.status, out.reason) == ("skipped", "project_ambiguous")
+    assert not base.config_dir.exists()
+
+
+def test_several_projects_use_the_id_of_the_defaults_map(tmp_path, base) -> None:
+    runner = Runner(_world(projects=("PVT_a", "PVT_b")))
+    mapped = defaults.Defaults(projects={"IronbellyOrg/IronClaude": "PVT_b"})
+    out = generate.ensure_config(_record(), mapped, runner, base)
+    assert out.status == "generated"
+    assert json.loads(out.config_path.read_text())["project_id"] == "PVT_b"
+
+
+def test_a_defaults_entry_that_is_not_one_of_the_projects_is_ambiguous(
+    tmp_path, base
+) -> None:
+    runner = Runner(_world(projects=("PVT_a", "PVT_b")))
+    mapped = defaults.Defaults(projects={"IronbellyOrg/IronClaude": "PVT_zzz"})
+    out = generate.ensure_config(_record(), mapped, runner, base)
+    assert (out.status, out.reason) == ("skipped", "project_ambiguous")
+
+
+def test_a_failed_account_read_is_a_skip_before_any_other_call(tmp_path, base) -> None:
+    runner = Runner(_world(account=None))
+    out = generate.ensure_config(_record(), defaults.Defaults(), runner, base)
+    assert (out.status, out.reason) == ("skipped", "account_read_failed")
+    assert runner.calls == [tuple(generate.argv_account())]
+    assert not base.config_dir.exists()
+
+
+def test_a_non_numeric_account_id_is_a_failed_read(tmp_path, base) -> None:
+    script = _world()
+    script[tuple(generate.argv_account())] = result(stdout='{"id": "12"}')
+    out = generate.ensure_config(_record(), defaults.Defaults(), Runner(script), base)
+    assert (out.status, out.reason) == ("skipped", "account_read_failed")
+
+
+def test_maintainers_are_added_to_the_fixed_approvers(tmp_path, base) -> None:
+    runner = Runner(_world(maintainers=(33, 44, 55)))
+    out = generate.ensure_config(_record(), defaults.Defaults(), runner, base)
+    assert cycle.validate_approvers(out.approvers_path) == {11, 22, 33, 44, 55}
+    assert out.approvers_path.read_text() == "11\n22\n33\n44\n55\n"
+
+
+def test_the_launch_account_id_is_never_written_to_the_approvers_file(
+    tmp_path, base
+) -> None:
+    # a maintainer and a fixed login both resolve to the launch account
+    runner = Runner(
+        _world(
+            maintainers=(33, LAUNCH_ID), fixed={"ironbelly": LAUNCH_ID, "clayphi": 22}
+        )
+    )
+    out = generate.ensure_config(_record(), defaults.Defaults(), runner, base)
+    assert out.status == "generated"
+    ids = cycle.validate_approvers(out.approvers_path)
+    assert LAUNCH_ID not in ids and ids == {22, 33}
+
+
+def test_a_launch_account_that_is_the_only_approver_leaves_no_approvers(
+    tmp_path, base
+) -> None:
+    runner = Runner(_world(maintainers=(LAUNCH_ID,), fixed={"ironbelly": LAUNCH_ID}))
+    out = generate.ensure_config(
+        _record(), defaults.Defaults(approver_logins=("ironbelly",)), runner, base
+    )
+    assert (out.status, out.reason) == ("skipped", "no_approvers")
+    assert not base.config_dir.exists()
+
+
+@pytest.mark.parametrize("failing", ["approver", "maintainers", "projects"])
+def test_a_failed_read_is_a_skip_and_writes_nothing(tmp_path, base, failing) -> None:
+    script = _world()
+    key = {
+        "approver": tuple(generate.argv_user_id("clayphi")),
+        "maintainers": tuple(generate.argv_maintainers("IronbellyOrg/IronClaude")),
+        "projects": tuple(generate.argv_projects("IronbellyOrg/IronClaude")),
+    }[failing]
+    script[key] = result(stderr="HTTP 502", returncode=1)
+    out = generate.ensure_config(_record(), defaults.Defaults(), Runner(script), base)
+    assert out.status == "skipped"
+    assert (
+        out.reason
+        == {
+            "approver": "approver_read_failed",
+            "maintainers": "maintainers_read_failed",
+            "projects": "project_read_failed",
+        }[failing]
+    )
+    assert not base.config_dir.exists()
+
+
+def test_an_existing_config_is_left_untouched_and_no_call_is_made(
+    tmp_path, base
+) -> None:
+    directory = base.config_dir / "issue-watch.d"
+    directory.mkdir(parents=True)
+    existing = directory / "IronClaude.json"
+    existing.write_text("hand written, do not touch")
+    runner = Runner({})
+    out = generate.ensure_config(_record(), defaults.Defaults(), runner, base)
+    assert out.status == "exists" and out.config_path == existing
+    assert existing.read_text() == "hand written, do not touch"
+    assert runner.calls == []
+
+
+def test_a_second_call_after_generation_changes_nothing(tmp_path, base) -> None:
+    out = generate.ensure_config(_record(), defaults.Defaults(), Runner(_world()), base)
+    before = out.config_path.read_bytes()
+    again = generate.ensure_config(_record(), defaults.Defaults(), Runner({}), base)
+    assert again.status == "exists" and out.config_path.read_bytes() == before
+
+
+def test_a_leftover_approvers_file_is_never_overwritten(tmp_path, base) -> None:
+    directory = base.config_dir / "issue-watch.d"
+    directory.mkdir(parents=True)
+    (directory / "IronClaude-approvers.txt").write_text("999\n")
+    out = generate.ensure_config(_record(), defaults.Defaults(), Runner(_world()), base)
+    assert (out.status, out.reason) == ("skipped", "approvers_file_exists")
+    assert (directory / "IronClaude-approvers.txt").read_text() == "999\n"
+    assert not (directory / "IronClaude.json").exists()
+
+
+def test_two_repos_get_two_different_state_dirs(tmp_path, base) -> None:
+    a = generate.ensure_config(_record(), defaults.Defaults(), Runner(_world()), base)
+    slug = "IronbellyOrg/Coder"
+    b = generate.ensure_config(
+        _record("Coder", slug), defaults.Defaults(), Runner(_world(slug)), base
+    )
+    assert a.status == b.status == "generated"
+    assert a.state_dir != b.state_dir
+    assert a.state_dir == base.state_dir / "issue-watch" / "IronClaude"
+    assert b.state_dir == base.state_dir / "issue-watch" / "Coder"
+    cfg_a, cfg_b = (cycle.load_config(o.config_path) for o in (a, b))
+    assert cfg_a.state_dir != cfg_b.state_dir
+    assert cfg_a.approvers_file != cfg_b.approvers_file
+    assert cfg_b.repo == slug
+
+
+def test_the_trigger_label_of_the_defaults_reaches_the_config(tmp_path, base) -> None:
+    custom = defaults.Defaults(trigger_label="watch:go")
+    out = generate.ensure_config(_record(), custom, Runner(_world()), base)
+    assert cycle.load_config(out.config_path).trigger_label == "watch:go"
+    plain = generate.ensure_config(
+        _record("Coder", "IronbellyOrg/Coder"),
+        defaults.Defaults(),
+        Runner(_world("IronbellyOrg/Coder")),
+        base,
+    )
+    assert "labels" not in json.loads(plain.config_path.read_text())
+
+
+@pytest.mark.parametrize("name", ["bad name", "-lead", "a/b", "", "x" * 101])
+def test_a_name_that_is_not_a_safe_file_name_is_skipped(tmp_path, base, name) -> None:
+    runner = Runner({})
+    out = generate.ensure_config(_record(name), defaults.Defaults(), runner, base)
+    assert (out.status, out.reason) == ("skipped", "bad_name")
+    assert runner.calls == [] and not base.config_dir.exists()
+
+
+def test_every_call_is_a_read_and_each_rest_call_carries_method_get(
+    tmp_path, base
+) -> None:
+    runner = Runner(_world())
+    generate.ensure_config(_record(), defaults.Defaults(), runner, base)
+    # the account, the Projects, the two fixed logins and the maintainers
+    assert len(runner.calls) == 5
+    for argv in runner.calls:
+        text = " ".join(argv)
+        assert argv[:2] == ("gh", "api")
+        assert "POST" not in argv and "mutation" not in text.lower()
+        if argv[2] == "graphql":
+            assert any(a.startswith("query=query(") for a in argv)
+        else:
+            assert argv[2:4] == ("--method", "GET"), argv
+
+
+def test_the_projects_query_asks_for_ids_and_numbers_only() -> None:
+    query = generate.PROJECTS_QUERY
+    assert query.startswith("query(") and "mutation" not in query.lower()
+    assert "title" not in query and "body" not in query
+    assert query.count("String!") == 2  # $owner and $name, both non-null
+
+
+def test_nothing_is_written_under_the_real_home(tmp_path, base) -> None:
+    generate.ensure_config(_record(), defaults.Defaults(), Runner(_world()), base)
+    _no_write_under_home(tmp_path)

Task 19 context. generate.py is new. Two small departures from the brief, both deliberate: the Projects query reads ids and numbers only (the brief names a title field too; the security scan of the watcher forbids any title or body field in a query, and the title is never used), and the account read is `gh api --method GET user --jq {id}` so every REST call carries --method GET. The module-boundaries table gained a "generate" row. The argv scan Task 12 extended gained a test for the generator builders. Tests run: tests/issue_watch 2915 passed; ruff clean; make verify-sync clean.

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
