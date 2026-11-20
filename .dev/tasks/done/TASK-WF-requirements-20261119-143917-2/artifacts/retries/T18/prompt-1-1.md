6773b49565ded7b521ed636b04a56ef4a2314ce0
Review one task for spec compliance.

Task brief: ## Task 18: List and filter the Orca repos

Create `src/superclaude/cli/issue_watch/repos.py` with a function that runs `orca repo list` through the `Runner` of `src/superclaude/cli/issue_watch/runner.py` and returns one record per usable repo: Orca id, name, local path, and `owner/name` read from the path's git `origin`. A failed or timed-out `orca repo list`, or output that cannot be read, raises an error (requirement R15), never an empty list. Skip, and report with a reason, a repo whose path is under `/tmp`, whose origin is not on github.com, or whose origin owner is not in the allowed owners of Task 17. Parse the real format: one line per repo, `<id>  <name>  <path>` (checked on 2026-11-18).

Depends on: Task 17

Acceptance criteria:
- T18.AC1: New `tests/issue_watch/test_repos.py` uses the fake runner and covers: six repos with one in `/tmp` skipped, a non-GitHub origin skipped, a foreign owner skipped, a failed list raising, a timed-out list raising, an empty but successful list returning no repos.
- T18.AC2: The module uses no shell and passes `tests/issue_watch/test_no_shell.py` and `test_module_boundaries.py`.
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
Start sha: 6773b49565ded7b521ed636b04a56ef4a2314ce0
Diff against the start snapshot: diff --git a/src/superclaude/cli/issue_watch/repos.py b/src/superclaude/cli/issue_watch/repos.py
deleted file mode 100644
index 3fe331135..000000000
--- a/src/superclaude/cli/issue_watch/repos.py
+++ /dev/null
@@ -1,144 +0,0 @@
-"""List the Orca repositories the watcher may serve (plan Task 18, requirement R15).
-
-``orca repo list`` prints one line per repository: ``<id>  <name>  <path>`` (fields joined by
-two or more spaces; checked on 2026-11-18). For each line this module reads the path's git
-``origin`` and keeps the repository only when it is usable. A repository that is not usable is
-skipped with a closed reason, never silently:
-
-* ``path_in_tmp``: the path is ``/tmp`` or under it (a throwaway checkout);
-* ``origin_unreadable``: ``git remote get-url origin`` failed, timed out or printed nothing;
-* ``origin_not_github``: the origin is not a ``github.com`` ``owner/name`` URL;
-* ``foreign_owner``: the origin owner is not one of ``allowed_owners`` (case-insensitive).
-
-A failed or timed-out ``orca repo list``, or output that cannot be read, raises
-``RepoListError``: it never gives an empty list, because an empty list would look like "nothing
-to watch". An empty but successful list returns no repositories.
-
-Every command runs through the ``Runner`` (an argv list, no shell).
-"""
-
-from __future__ import annotations
-
-import re
-from collections.abc import Iterable
-from dataclasses import dataclass
-from pathlib import PurePosixPath
-
-from .launch import parse_origin
-from .runner import CommandResult, Runner
-
-LIST_TIMEOUT_S = 30.0
-GIT_TIMEOUT_S = 15.0
-
-_FIELDS = re.compile(r" {2,}")
-_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}")
-
-
-class RepoListError(Exception):
-    """``orca repo list`` could not be run or read. ``reason`` is a closed word."""
-
-    def __init__(self, reason: str) -> None:
-        super().__init__(reason)
-        self.reason = reason
-
-
-@dataclass(frozen=True)
-class OrcaRepo:
-    """One usable repository."""
-
-    orca_id: str
-    name: str
-    path: str
-    slug: str
-    """``owner/name`` read from the path's git ``origin``."""
-
-
-@dataclass(frozen=True)
-class Skipped:
-    """One repository the watcher will not serve, and why."""
-
-    orca_id: str
-    name: str
-    path: str
-    reason: str
-
-
-@dataclass(frozen=True)
-class RepoList:
-    repos: tuple[OrcaRepo, ...]
-    skipped: tuple[Skipped, ...]
-
-
-def _in_tmp(path: str) -> bool:
-    parts = PurePosixPath(path).parts
-    return len(parts) >= 2 and parts[0] == "/" and parts[1] == "tmp"
-
-
-def _parse_lines(text: str) -> list[tuple[str, str, str]]:
-    rows: list[tuple[str, str, str]] = []
-    for line in text.splitlines():
-        line = line.strip()
-        if not line:
-            continue
-        fields = _FIELDS.split(line, maxsplit=2)
-        if len(fields) != 3:
-            raise RepoListError("unreadable_list")
-        orca_id, name, path = (f.strip() for f in fields)
-        if not _ID.fullmatch(orca_id) or not name or not path.startswith("/"):
-            raise RepoListError("unreadable_list")
-        rows.append((orca_id, name, path))
-    return rows
-
-
-def _failed(result: CommandResult) -> bool:
-    return result.timed_out or result.spawn_error is not None or result.returncode != 0
-
-
-def _origin(runner: Runner, path: str, timeout: float) -> str | None:
-    """The ``owner/name`` of the path's origin; ``""`` for a non-GitHub URL; None when unread."""
-    argv = ["git", "-C", path, "remote", "get-url", "origin"]
-    result = runner.run(argv, timeout)
-    if _failed(result) or not result.stdout.strip():
-        return None
-    return parse_origin(result.stdout) or ""
-
-
-def list_repos(
-    runner: Runner,
-    orca: str,
-    allowed_owners: Iterable[str],
-    *,
-    list_timeout: float = LIST_TIMEOUT_S,
-    git_timeout: float = GIT_TIMEOUT_S,
-) -> RepoList:
-    """Run ``orca repo list`` and return the usable repositories and the skipped ones.
-
-    ``orca`` is the Orca CLI path or name the caller already proved (``launch.find_orca``).
-    Raises ``RepoListError`` (``list_failed``, ``list_timeout`` or ``unreadable_list``).
-    """
-    owners = {o.lower() for o in allowed_owners}
-    result = runner.run([orca, "repo", "list"], list_timeout)
-    if result.timed_out:
-        raise RepoListError("list_timeout")
-    if result.spawn_error is not None or result.returncode != 0:
-        raise RepoListError("list_failed")
-    repos: list[OrcaRepo] = []
-    skipped: list[Skipped] = []
-    for orca_id, name, path in _parse_lines(result.stdout):
-
-        def skip(reason: str) -> None:
-            skipped.append(Skipped(orca_id, name, path, reason))
-
-        if _in_tmp(path):
-            skip("path_in_tmp")
-            continue
-        slug = _origin(runner, path, git_timeout)
-        if slug is None:
-            skip("origin_unreadable")
-        elif not slug:
-            skip("origin_not_github")
-        elif slug.split("/")[0].lower() not in owners:
-            skip("foreign_owner")
-        else:
-            repos.append(OrcaRepo(orca_id, name, path, slug))
-    return RepoList(tuple(repos), tuple(skipped))
diff --git a/tests/issue_watch/test_repos.py b/tests/issue_watch/test_repos.py
deleted file mode 100644
index 09bf595e5..000000000
--- a/tests/issue_watch/test_repos.py
+++ /dev/null
@@ -1,211 +0,0 @@
-"""Task 18: ``orca repo list`` and the origin filter, over the fake runner."""
-
-from __future__ import annotations
-
-import pytest
-
-from superclaude.cli.issue_watch import repos
-from superclaude.cli.issue_watch.repos import RepoListError, list_repos
-
-from .conftest import result
-
-ORCA = "/home/u/.local/bin/orca-ide"
-LIST_ARGV = (ORCA, "repo", "list")
-OWNERS = ("IronbellyOrg",)
-
-
-def _git(path: str) -> tuple[str, ...]:
-    return ("git", "-C", path, "remote", "get-url", "origin")
-
-
-def _line(n: int, name: str, path: str) -> str:
-    return f"00000000-0000-4000-8000-{n:012d}  {name}  {path}"
-
-
-def _script(lines: list[str], origins: dict[str, object]) -> dict:
-    script: dict = {LIST_ARGV: result(stdout="\n".join(lines) + "\n")}
-    for path, url in origins.items():
-        script[_git(path)] = url if not isinstance(url, str) else result(stdout=url)
-    return script
-
-
-SIX = [
-    _line(1, "IronClaude", "/home/u/workspaces/IronClaude"),
-    _line(2, "Coder", "/home/u/workspaces/Coder"),
-    _line(3, "scratch", "/tmp/scratch-checkout"),
-    _line(4, "gitlab-thing", "/home/u/workspaces/gitlab-thing"),
-    _line(5, "forkofsomeone", "/home/u/workspaces/forkofsomeone"),
-    _line(6, "Ironeye", "/home/u/workspaces/Ironeye"),
-]
-SIX_ORIGINS = {
-    "/home/u/workspaces/IronClaude": "https://github.com/IronbellyOrg/IronClaude.git\n",
-    "/home/u/workspaces/Coder": "git@github.com:IronbellyOrg/Coder.git\n",
-    "/home/u/workspaces/gitlab-thing": "https://gitlab.com/IronbellyOrg/x.git\n",
-    "/home/u/workspaces/forkofsomeone": "https://github.com/SomeoneElse/IronClaude.git\n",
-    "/home/u/workspaces/Ironeye": "https://github.com/ironbellyorg/Ironeye\n",
-}
-
-
-def test_six_repos_with_one_in_tmp_skipped_and_the_other_skips_reported(
-    fake_runner,
-) -> None:
-    runner = fake_runner(_script(SIX, SIX_ORIGINS))
-    got = list_repos(runner, ORCA, OWNERS)
-    assert [(r.name, r.slug) for r in got.repos] == [
-        ("IronClaude", "IronbellyOrg/IronClaude"),
-        ("Coder", "IronbellyOrg/Coder"),
-        ("Ironeye", "ironbellyorg/Ironeye"),
-    ]
-    assert [(s.name, s.reason) for s in got.skipped] == [
-        ("scratch", "path_in_tmp"),
-        ("gitlab-thing", "origin_not_github"),
-        ("forkofsomeone", "foreign_owner"),
-    ]
-    first = got.repos[0]
-    assert first.orca_id == "00000000-0000-4000-8000-000000000001"
-    assert first.path == "/home/u/workspaces/IronClaude"
-    # the /tmp repo's origin was never read
-    assert _git("/tmp/scratch-checkout") not in [argv for argv, _ in runner.calls]
-
-
-def test_a_non_github_origin_is_skipped(fake_runner) -> None:
-    path = "/home/u/workspaces/x"
-    runner = fake_runner(
-        _script([_line(1, "x", path)], {path: "https://gitlab.com/IronbellyOrg/x.git"})
-    )
-    got = list_repos(runner, ORCA, OWNERS)
-    assert got.repos == () and [s.reason for s in got.skipped] == ["origin_not_github"]
-
-
-def test_a_foreign_owner_is_skipped_and_an_allowed_one_matches_any_case(
-    fake_runner,
-) -> None:
-    a, b = "/home/u/workspaces/a", "/home/u/workspaces/b"
-    runner = fake_runner(
-        _script(
-            [_line(1, "a", a), _line(2, "b", b)],
-            {
-                a: "https://github.com/Other/a.git",
-                b: "https://github.com/IRONBELLYORG/b",
-            },
-        )
-    )
-    got = list_repos(runner, ORCA, ["ironbellyorg"])
-    assert [r.name for r in got.repos] == ["b"]
-    assert [(s.name, s.reason) for s in got.skipped] == [("a", "foreign_owner")]
-
-
-@pytest.mark.parametrize(
-    ("reply", "reason"),
-    [
-        (result(stderr="boom", returncode=1), "list_failed"),
-        (result(returncode=127), "list_failed"),
-        (result(spawn_error="FileNotFoundError"), "list_failed"),
-        (result(timed_out=True), "list_timeout"),
-    ],
-)
-def test_a_failed_or_timed_out_list_raises_never_an_empty_list(
-    fake_runner, reply, reason
-) -> None:
-    runner = fake_runner({LIST_ARGV: reply})
-    with pytest.raises(RepoListError) as err:
-        list_repos(runner, ORCA, OWNERS)
-    assert err.value.reason == reason
-
-
-@pytest.mark.parametrize(
-    "text",
-    [
-        "just-one-field\n",
-        "only  two\n",
-        "id-1  name  relative/path\n",
-        "bad id!  name  /home/u/x\n",
-        "<html>not a list</html>\n",
-    ],
-)
-def test_output_that_cannot_be_read_raises(fake_runner, text) -> None:
-    runner = fake_runner({LIST_ARGV: result(stdout=text)})
-    with pytest.raises(RepoListError) as err:
-        list_repos(runner, ORCA, OWNERS)
-    assert err.value.reason == "unreadable_list"
-
-
-@pytest.mark.parametrize("text", ["", "\n", "\n\n  \n"])
-def test_an_empty_but_successful_list_returns_no_repos(fake_runner, text) -> None:
-    runner = fake_runner({LIST_ARGV: result(stdout=text)})
-    got = list_repos(runner, ORCA, OWNERS)
-    assert got.repos == () and got.skipped == ()
-
-
-def test_an_unreadable_origin_is_skipped_not_fatal(fake_runner) -> None:
-    ok_path, bad, silent = "/home/u/a", "/home/u/b", "/home/u/c"
-    runner = fake_runner(
-        _script(
-            [_line(1, "a", ok_path), _line(2, "b", bad), _line(3, "c", silent)],
-            {
-                ok_path: "https://github.com/IronbellyOrg/a.git",
-                bad: result(returncode=128, stderr="fatal: not a git repository"),
-                silent: result(stdout="\n"),
-            },
-        )
-    )
-    got = list_repos(runner, ORCA, OWNERS)
-    assert [r.name for r in got.repos] == ["a"]
-    assert [(s.name, s.reason) for s in got.skipped] == [
-        ("b", "origin_unreadable"),
-        ("c", "origin_unreadable"),
-    ]
-
-
-def test_a_timed_out_git_call_is_an_unreadable_origin(fake_runner) -> None:
-    path = "/home/u/a"
-    runner = fake_runner(_script([_line(1, "a", path)], {path: result(timed_out=True)}))
-    got = list_repos(runner, ORCA, OWNERS)
-    assert [s.reason for s in got.skipped] == ["origin_unreadable"]
-
-
-def test_a_path_with_spaces_and_a_name_with_dots_are_read(fake_runner) -> None:
-    path = "/home/u/my work/repo"
-    runner = fake_runner(
-        _script(
-            [_line(1, "coder-bmad.live", path)],
-            {path: "https://github.com/IronbellyOrg/repo.git"},
-        )
-    )
-    got = list_repos(runner, ORCA, OWNERS)
-    assert [(r.name, r.path) for r in got.repos] == [("coder-bmad.live", path)]
-
-
-@pytest.mark.parametrize("path", ["/tmp", "/tmp/x", "/tmp/a/b/c"])
-def test_every_path_at_or_under_tmp_is_skipped(fake_runner, path) -> None:
-    runner = fake_runner({LIST_ARGV: result(stdout=_line(1, "t", path) + "\n")})
-    got = list_repos(runner, ORCA, OWNERS)
-    assert [s.reason for s in got.skipped] == ["path_in_tmp"] and got.repos == ()
-
-
-@pytest.mark.parametrize("path", ["/tmpfoo/x", "/home/u/tmp/x", "/var/tmp/x"])
-def test_a_path_that_only_looks_like_tmp_is_not_skipped_for_it(
-    fake_runner, path
-) -> None:
-    runner = fake_runner(
-        _script([_line(1, "t", path)], {path: "https://github.com/IronbellyOrg/t.git"})
-    )
-    got = list_repos(runner, ORCA, OWNERS)
-    assert [r.name for r in got.repos] == ["t"]
-
-
-def test_the_commands_are_argv_lists_with_the_given_timeouts(fake_runner) -> None:
-    path = "/home/u/a"
-    runner = fake_runner(
-        _script([_line(1, "a", path)], {path: "https://github.com/IronbellyOrg/a.git"})
-    )
-    list_repos(runner, ORCA, OWNERS, list_timeout=7.0, git_timeout=3.0)
-    assert [argv for argv, _ in runner.calls] == [LIST_ARGV, _git(path)]
-    assert runner.timeouts == [7.0, 3.0]
-    assert all(cwd is None for _, cwd in runner.calls)
-
-
-def test_the_module_has_no_shell_and_no_process_import() -> None:
-    source = open(repos.__file__, encoding="utf-8").read()
-    for banned in ("subprocess", "os.system", "shell=True", "os.popen"):
-        assert banned not in source
diff --git a/src/superclaude/cli/issue_watch/repos.py b/src/superclaude/cli/issue_watch/repos.py
new file mode 100644
index 000000000..3fe331135
--- /dev/null
+++ b/src/superclaude/cli/issue_watch/repos.py
@@ -0,0 +1,144 @@
+"""List the Orca repositories the watcher may serve (plan Task 18, requirement R15).
+
+``orca repo list`` prints one line per repository: ``<id>  <name>  <path>`` (fields joined by
+two or more spaces; checked on 2026-11-18). For each line this module reads the path's git
+``origin`` and keeps the repository only when it is usable. A repository that is not usable is
+skipped with a closed reason, never silently:
+
+* ``path_in_tmp``: the path is ``/tmp`` or under it (a throwaway checkout);
+* ``origin_unreadable``: ``git remote get-url origin`` failed, timed out or printed nothing;
+* ``origin_not_github``: the origin is not a ``github.com`` ``owner/name`` URL;
+* ``foreign_owner``: the origin owner is not one of ``allowed_owners`` (case-insensitive).
+
+A failed or timed-out ``orca repo list``, or output that cannot be read, raises
+``RepoListError``: it never gives an empty list, because an empty list would look like "nothing
+to watch". An empty but successful list returns no repositories.
+
+Every command runs through the ``Runner`` (an argv list, no shell).
+"""
+
+from __future__ import annotations
+
+import re
+from collections.abc import Iterable
+from dataclasses import dataclass
+from pathlib import PurePosixPath
+
+from .launch import parse_origin
+from .runner import CommandResult, Runner
+
+LIST_TIMEOUT_S = 30.0
+GIT_TIMEOUT_S = 15.0
+
+_FIELDS = re.compile(r" {2,}")
+_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}")
+
+
+class RepoListError(Exception):
+    """``orca repo list`` could not be run or read. ``reason`` is a closed word."""
+
+    def __init__(self, reason: str) -> None:
+        super().__init__(reason)
+        self.reason = reason
+
+
+@dataclass(frozen=True)
+class OrcaRepo:
+    """One usable repository."""
+
+    orca_id: str
+    name: str
+    path: str
+    slug: str
+    """``owner/name`` read from the path's git ``origin``."""
+
+
+@dataclass(frozen=True)
+class Skipped:
+    """One repository the watcher will not serve, and why."""
+
+    orca_id: str
+    name: str
+    path: str
+    reason: str
+
+
+@dataclass(frozen=True)
+class RepoList:
+    repos: tuple[OrcaRepo, ...]
+    skipped: tuple[Skipped, ...]
+
+
+def _in_tmp(path: str) -> bool:
+    parts = PurePosixPath(path).parts
+    return len(parts) >= 2 and parts[0] == "/" and parts[1] == "tmp"
+
+
+def _parse_lines(text: str) -> list[tuple[str, str, str]]:
+    rows: list[tuple[str, str, str]] = []
+    for line in text.splitlines():
+        line = line.strip()
+        if not line:
+            continue
+        fields = _FIELDS.split(line, maxsplit=2)
+        if len(fields) != 3:
+            raise RepoListError("unreadable_list")
+        orca_id, name, path = (f.strip() for f in fields)
+        if not _ID.fullmatch(orca_id) or not name or not path.startswith("/"):
+            raise RepoListError("unreadable_list")
+        rows.append((orca_id, name, path))
+    return rows
+
+
+def _failed(result: CommandResult) -> bool:
+    return result.timed_out or result.spawn_error is not None or result.returncode != 0
+
+
+def _origin(runner: Runner, path: str, timeout: float) -> str | None:
+    """The ``owner/name`` of the path's origin; ``""`` for a non-GitHub URL; None when unread."""
+    argv = ["git", "-C", path, "remote", "get-url", "origin"]
+    result = runner.run(argv, timeout)
+    if _failed(result) or not result.stdout.strip():
+        return None
+    return parse_origin(result.stdout) or ""
+
+
+def list_repos(
+    runner: Runner,
+    orca: str,
+    allowed_owners: Iterable[str],
+    *,
+    list_timeout: float = LIST_TIMEOUT_S,
+    git_timeout: float = GIT_TIMEOUT_S,
+) -> RepoList:
+    """Run ``orca repo list`` and return the usable repositories and the skipped ones.
+
+    ``orca`` is the Orca CLI path or name the caller already proved (``launch.find_orca``).
+    Raises ``RepoListError`` (``list_failed``, ``list_timeout`` or ``unreadable_list``).
+    """
+    owners = {o.lower() for o in allowed_owners}
+    result = runner.run([orca, "repo", "list"], list_timeout)
+    if result.timed_out:
+        raise RepoListError("list_timeout")
+    if result.spawn_error is not None or result.returncode != 0:
+        raise RepoListError("list_failed")
+    repos: list[OrcaRepo] = []
+    skipped: list[Skipped] = []
+    for orca_id, name, path in _parse_lines(result.stdout):
+
+        def skip(reason: str) -> None:
+            skipped.append(Skipped(orca_id, name, path, reason))
+
+        if _in_tmp(path):
+            skip("path_in_tmp")
+            continue
+        slug = _origin(runner, path, git_timeout)
+        if slug is None:
+            skip("origin_unreadable")
+        elif not slug:
+            skip("origin_not_github")
+        elif slug.split("/")[0].lower() not in owners:
+            skip("foreign_owner")
+        else:
+            repos.append(OrcaRepo(orca_id, name, path, slug))
+    return RepoList(tuple(repos), tuple(skipped))
diff --git a/tests/issue_watch/test_repos.py b/tests/issue_watch/test_repos.py
new file mode 100644
index 000000000..09bf595e5
--- /dev/null
+++ b/tests/issue_watch/test_repos.py
@@ -0,0 +1,211 @@
+"""Task 18: ``orca repo list`` and the origin filter, over the fake runner."""
+
+from __future__ import annotations
+
+import pytest
+
+from superclaude.cli.issue_watch import repos
+from superclaude.cli.issue_watch.repos import RepoListError, list_repos
+
+from .conftest import result
+
+ORCA = "/home/u/.local/bin/orca-ide"
+LIST_ARGV = (ORCA, "repo", "list")
+OWNERS = ("IronbellyOrg",)
+
+
+def _git(path: str) -> tuple[str, ...]:
+    return ("git", "-C", path, "remote", "get-url", "origin")
+
+
+def _line(n: int, name: str, path: str) -> str:
+    return f"00000000-0000-4000-8000-{n:012d}  {name}  {path}"
+
+
+def _script(lines: list[str], origins: dict[str, object]) -> dict:
+    script: dict = {LIST_ARGV: result(stdout="\n".join(lines) + "\n")}
+    for path, url in origins.items():
+        script[_git(path)] = url if not isinstance(url, str) else result(stdout=url)
+    return script
+
+
+SIX = [
+    _line(1, "IronClaude", "/home/u/workspaces/IronClaude"),
+    _line(2, "Coder", "/home/u/workspaces/Coder"),
+    _line(3, "scratch", "/tmp/scratch-checkout"),
+    _line(4, "gitlab-thing", "/home/u/workspaces/gitlab-thing"),
+    _line(5, "forkofsomeone", "/home/u/workspaces/forkofsomeone"),
+    _line(6, "Ironeye", "/home/u/workspaces/Ironeye"),
+]
+SIX_ORIGINS = {
+    "/home/u/workspaces/IronClaude": "https://github.com/IronbellyOrg/IronClaude.git\n",
+    "/home/u/workspaces/Coder": "git@github.com:IronbellyOrg/Coder.git\n",
+    "/home/u/workspaces/gitlab-thing": "https://gitlab.com/IronbellyOrg/x.git\n",
+    "/home/u/workspaces/forkofsomeone": "https://github.com/SomeoneElse/IronClaude.git\n",
+    "/home/u/workspaces/Ironeye": "https://github.com/ironbellyorg/Ironeye\n",
+}
+
+
+def test_six_repos_with_one_in_tmp_skipped_and_the_other_skips_reported(
+    fake_runner,
+) -> None:
+    runner = fake_runner(_script(SIX, SIX_ORIGINS))
+    got = list_repos(runner, ORCA, OWNERS)
+    assert [(r.name, r.slug) for r in got.repos] == [
+        ("IronClaude", "IronbellyOrg/IronClaude"),
+        ("Coder", "IronbellyOrg/Coder"),
+        ("Ironeye", "ironbellyorg/Ironeye"),
+    ]
+    assert [(s.name, s.reason) for s in got.skipped] == [
+        ("scratch", "path_in_tmp"),
+        ("gitlab-thing", "origin_not_github"),
+        ("forkofsomeone", "foreign_owner"),
+    ]
+    first = got.repos[0]
+    assert first.orca_id == "00000000-0000-4000-8000-000000000001"
+    assert first.path == "/home/u/workspaces/IronClaude"
+    # the /tmp repo's origin was never read
+    assert _git("/tmp/scratch-checkout") not in [argv for argv, _ in runner.calls]
+
+
+def test_a_non_github_origin_is_skipped(fake_runner) -> None:
+    path = "/home/u/workspaces/x"
+    runner = fake_runner(
+        _script([_line(1, "x", path)], {path: "https://gitlab.com/IronbellyOrg/x.git"})
+    )
+    got = list_repos(runner, ORCA, OWNERS)
+    assert got.repos == () and [s.reason for s in got.skipped] == ["origin_not_github"]
+
+
+def test_a_foreign_owner_is_skipped_and_an_allowed_one_matches_any_case(
+    fake_runner,
+) -> None:
+    a, b = "/home/u/workspaces/a", "/home/u/workspaces/b"
+    runner = fake_runner(
+        _script(
+            [_line(1, "a", a), _line(2, "b", b)],
+            {
+                a: "https://github.com/Other/a.git",
+                b: "https://github.com/IRONBELLYORG/b",
+            },
+        )
+    )
+    got = list_repos(runner, ORCA, ["ironbellyorg"])
+    assert [r.name for r in got.repos] == ["b"]
+    assert [(s.name, s.reason) for s in got.skipped] == [("a", "foreign_owner")]
+
+
+@pytest.mark.parametrize(
+    ("reply", "reason"),
+    [
+        (result(stderr="boom", returncode=1), "list_failed"),
+        (result(returncode=127), "list_failed"),
+        (result(spawn_error="FileNotFoundError"), "list_failed"),
+        (result(timed_out=True), "list_timeout"),
+    ],
+)
+def test_a_failed_or_timed_out_list_raises_never_an_empty_list(
+    fake_runner, reply, reason
+) -> None:
+    runner = fake_runner({LIST_ARGV: reply})
+    with pytest.raises(RepoListError) as err:
+        list_repos(runner, ORCA, OWNERS)
+    assert err.value.reason == reason
+
+
+@pytest.mark.parametrize(
+    "text",
+    [
+        "just-one-field\n",
+        "only  two\n",
+        "id-1  name  relative/path\n",
+        "bad id!  name  /home/u/x\n",
+        "<html>not a list</html>\n",
+    ],
+)
+def test_output_that_cannot_be_read_raises(fake_runner, text) -> None:
+    runner = fake_runner({LIST_ARGV: result(stdout=text)})
+    with pytest.raises(RepoListError) as err:
+        list_repos(runner, ORCA, OWNERS)
+    assert err.value.reason == "unreadable_list"
+
+
+@pytest.mark.parametrize("text", ["", "\n", "\n\n  \n"])
+def test_an_empty_but_successful_list_returns_no_repos(fake_runner, text) -> None:
+    runner = fake_runner({LIST_ARGV: result(stdout=text)})
+    got = list_repos(runner, ORCA, OWNERS)
+    assert got.repos == () and got.skipped == ()
+
+
+def test_an_unreadable_origin_is_skipped_not_fatal(fake_runner) -> None:
+    ok_path, bad, silent = "/home/u/a", "/home/u/b", "/home/u/c"
+    runner = fake_runner(
+        _script(
+            [_line(1, "a", ok_path), _line(2, "b", bad), _line(3, "c", silent)],
+            {
+                ok_path: "https://github.com/IronbellyOrg/a.git",
+                bad: result(returncode=128, stderr="fatal: not a git repository"),
+                silent: result(stdout="\n"),
+            },
+        )
+    )
+    got = list_repos(runner, ORCA, OWNERS)
+    assert [r.name for r in got.repos] == ["a"]
+    assert [(s.name, s.reason) for s in got.skipped] == [
+        ("b", "origin_unreadable"),
+        ("c", "origin_unreadable"),
+    ]
+
+
+def test_a_timed_out_git_call_is_an_unreadable_origin(fake_runner) -> None:
+    path = "/home/u/a"
+    runner = fake_runner(_script([_line(1, "a", path)], {path: result(timed_out=True)}))
+    got = list_repos(runner, ORCA, OWNERS)
+    assert [s.reason for s in got.skipped] == ["origin_unreadable"]
+
+
+def test_a_path_with_spaces_and_a_name_with_dots_are_read(fake_runner) -> None:
+    path = "/home/u/my work/repo"
+    runner = fake_runner(
+        _script(
+            [_line(1, "coder-bmad.live", path)],
+            {path: "https://github.com/IronbellyOrg/repo.git"},
+        )
+    )
+    got = list_repos(runner, ORCA, OWNERS)
+    assert [(r.name, r.path) for r in got.repos] == [("coder-bmad.live", path)]
+
+
+@pytest.mark.parametrize("path", ["/tmp", "/tmp/x", "/tmp/a/b/c"])
+def test_every_path_at_or_under_tmp_is_skipped(fake_runner, path) -> None:
+    runner = fake_runner({LIST_ARGV: result(stdout=_line(1, "t", path) + "\n")})
+    got = list_repos(runner, ORCA, OWNERS)
+    assert [s.reason for s in got.skipped] == ["path_in_tmp"] and got.repos == ()
+
+
+@pytest.mark.parametrize("path", ["/tmpfoo/x", "/home/u/tmp/x", "/var/tmp/x"])
+def test_a_path_that_only_looks_like_tmp_is_not_skipped_for_it(
+    fake_runner, path
+) -> None:
+    runner = fake_runner(
+        _script([_line(1, "t", path)], {path: "https://github.com/IronbellyOrg/t.git"})
+    )
+    got = list_repos(runner, ORCA, OWNERS)
+    assert [r.name for r in got.repos] == ["t"]
+
+
+def test_the_commands_are_argv_lists_with_the_given_timeouts(fake_runner) -> None:
+    path = "/home/u/a"
+    runner = fake_runner(
+        _script([_line(1, "a", path)], {path: "https://github.com/IronbellyOrg/a.git"})
+    )
+    list_repos(runner, ORCA, OWNERS, list_timeout=7.0, git_timeout=3.0)
+    assert [argv for argv, _ in runner.calls] == [LIST_ARGV, _git(path)]
+    assert runner.timeouts == [7.0, 3.0]
+    assert all(cwd is None for _, cwd in runner.calls)
+
+
+def test_the_module_has_no_shell_and_no_process_import() -> None:
+    source = open(repos.__file__, encoding="utf-8").read()
+    for banned in ("subprocess", "os.system", "shell=True", "os.popen"):
+        assert banned not in source

Task 18 context. The T18 files (repos.py, test_repos.py) were written before the T18 start line was recorded, because the T17 re-review ran in parallel; the T18 start snapshot therefore already holds them, and the review diff for T18 is the working tree against HEAD for those two files plus the test_module_boundaries.py row. Review the two files whole. Tests run: tests/issue_watch 2886 passed; ruff clean; make verify-sync clean.

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
