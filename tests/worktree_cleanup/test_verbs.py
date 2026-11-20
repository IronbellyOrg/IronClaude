"""The four verbs (Task 12): list, archive, retire and prune, their lock, files and exit codes.

Git runs on throwaway repositories under ``tmp_path`` with a local bare evidence remote;
``gh`` and ``orca`` answer from canned replies. Nothing here touches a real worktree.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import os
import time
from pathlib import Path

import pytest

from .conftest import git_in, make_fake_proc
from .test_archive import git_identity  # noqa: F401 - autouse: the evidence commit needs an identity
from .test_facts import write

FAR = time.time() + 30 * 86400  # every worktree looks 30 days idle and old enough


class World:
    """A throwaway repo with worktrees, canned gh and orca replies, and an evidence remote."""

    def __init__(self, wc, runner_cls, repo, evidence_bare, tmp_path, listed=()):
        self.wc, self.repo, self.tmp, self.bare = wc, repo, tmp_path, evidence_bare
        self.clone = str(tmp_path / "evidence-clone")
        self.out = tmp_path / "out"
        self.proc = str(make_fake_proc(tmp_path / "proc", {}))
        self.states: dict[str, str] = {}  # branch -> pull request state
        self.paths: dict[str, Path] = {}
        self.listed = set(listed)  # worktrees Orca lists
        self.gh_override = {}
        self.orca_calls: list[list[str]] = []
        self.runner = runner_cls(
            evidence_dir=self.clone, replies={"gh": self.gh, "orca": self.orca}
        )

    def add(self, name, state="MERGED", dev=True):
        path = self.repo.add_worktree(name)
        if dev:
            write(path / ".dev" / "tasks" / "note.md", f"{name}\n")
        self.paths[name] = path
        self.states[name] = state
        return path

    def head(self, name):
        return git_in(self.paths[name], "rev-parse", "HEAD").strip()

    def gh(self, argv, cwd):
        wc = self.wc
        key = tuple(argv[1:3])
        if key in self.gh_override:
            return self.gh_override[key](argv)
        if key == ("pr", "list"):
            branch = argv[argv.index("--head") + 1]
            state = self.states.get(branch)
            rows = []
            if state:
                rows = [
                    {
                        "number": 700, "state": state, "headRefOid": self.head(branch),
                        "headRefName": branch, "author": {"login": "example-user"},
                        "mergedAt": "2026-11-10T12:00:00Z" if state == "MERGED" else None,
                        "title": "t", "body": "", "closingIssuesReferences": [],
                    }
                ]  # fmt: skip
            return wc.Result(0, json.dumps(rows), "")
        if key == ("pr", "view"):
            return wc.Result(
                0,
                json.dumps({"state": "MERGED", "mergedAt": "2026-11-10T12:00:00Z"}),
                "",
            )
        return wc.Result(1, "", "unexpected gh call")

    def orca(self, argv, cwd):
        wc = self.wc
        self.orca_calls.append(list(argv))
        key = tuple(argv[1:3])
        if key == ("repo", "list"):
            repos = [
                {"id": "r1", "path": str(self.repo.main), "displayName": "example"}
            ]
            return wc.Result(
                0, json.dumps({"ok": True, "result": {"repos": repos}}), ""
            )
        if key == ("worktree", "ps"):
            rows = [
                {
                    "worktreeId": f"id-{n}", "path": str(p), "isPinned": False,
                    "liveTerminalCount": 0, "lastActivityAt": None, "linkedPR": None, "comment": "",
                }
                for n, p in self.paths.items() if n in self.listed and p.exists()
            ]  # fmt: skip
            return wc.Result(
                0, json.dumps({"ok": True, "result": {"worktrees": rows}}), ""
            )
        if key == ("worktree", "list"):
            return wc.Result(0, '{"ok": true, "result": {"worktrees": []}}', "")
        if key == ("reference", "list"):
            return wc.Result(0, '{"ok": true, "result": {"references": []}}', "")
        if key == ("worktree", "rm"):
            name = next(n for n, p in self.paths.items() if f"id:id-{n}" == argv[4])
            git_in(self.repo.main, "worktree", "remove", str(self.paths[name]))
            return wc.Result(0, "", "")
        return wc.Result(0, "", "")

    def env(self):
        return {"RUN_EVIDENCE_DIR": self.clone, "RUN_EVIDENCE_REPO": str(self.bare)}

    def run(self, *argv, cwd=None, out=True):
        extra = ["--out", str(self.out)] if out else []
        self.runner.commands.clear()
        return self.wc.main(
            [*argv, *extra], runner=self.runner, env=self.env(), now=FAR,
            proc_root=self.proc, cwd=cwd or str(self.tmp),
        )  # fmt: skip

    def verbs(self):
        return [" ".join(c.argv[:3]) for c in self.runner.commands]

    def removal_commands(self):
        return [
            c.argv for c in self.runner.commands
            if c.argv[:3] in (["git", "worktree", "remove"], ["orca", "worktree", "rm"])
            or c.argv[:2] == ["xargs", "-0"]
            or c.argv[1:3] == ["branch", "-d"]
            or c.argv[:3] == ["orca", "terminal", "close"]
            or "push" in c.argv
        ]  # fmt: skip

    def snapshot(self):
        seen = {}
        for path in self.paths.values():
            for dirpath, _dirs, names in os.walk(path):
                if ".git" in Path(dirpath).parts:
                    continue
                for n in names:
                    full = os.path.join(dirpath, n)
                    seen[full] = hashlib.sha256(Path(full).read_bytes()).hexdigest()
        return seen


@pytest.fixture
def world(wc, runner_cls, throwaway_repo, evidence_bare, tmp_path):
    return World(wc, runner_cls, throwaway_repo, evidence_bare, tmp_path)


def table_lines(text):
    return [ln for ln in text.splitlines() if ln.startswith("| ")]


# -- list and prune without --apply: a table, no removal ---------------------------------------


def test_list_prints_the_table_and_records_no_removal_command(world, capsys):
    world.add("done")
    world.add("open", state="OPEN")
    before = world.snapshot()
    assert world.run("list", out=False) == 0
    shown = capsys.readouterr().out
    lines = table_lines(shown)
    assert (
        lines[0].startswith("| repo | folder | branch | in orca |")
        and lines[0].count(" | ") == 10
    )
    by_folder = {
        ln.split(" | ")[1]: ln for ln in lines[1:]
    }  # the dashes row is not a "| " line
    assert (
        "removable" in by_folder["done"]
        and "pull request #700 is open" in by_folder["open"]
    )
    assert "main" in by_folder and "main checkout" in by_folder["main"]
    assert world.removal_commands() == []
    assert world.snapshot() == before
    assert (
        "summary: removed 0, kept 3, failed 0 (1 removable; dry run, nothing was removed)"
        in shown
    )
    assert not world.out.exists()  # list writes no files


def test_prune_without_apply_writes_both_files_and_nothing_inside_a_worktree(
    wc, world, capsys
):
    world.add("done")
    before = world.snapshot()
    assert world.run("prune") == 0
    md = list(world.out.glob("prune-*.md"))
    js = list(world.out.glob("prune-*.json"))
    assert len(md) == 1 and len(js) == 1
    doc = json.loads(js[0].read_text())
    assert set(doc) >= {"columns", "rows", "commands", "summary"}
    assert {r["folder"] for r in doc["rows"]} == {"main", "done"}
    assert (
        all(set(c) == {"argv", "cwd", "stdin_paths"} for c in doc["commands"])
        and doc["commands"]
    )
    assert doc["summary"]["dry_run"] is True and doc["summary"]["removed"] == 0
    assert md[0].read_text() == wc.render_markdown(doc["rows"])
    assert world.removal_commands() == [] and world.snapshot() == before
    # both files are under --out, which is outside every worktree
    assert all(
        not str(p).startswith(str(path))
        for p in (*md, *js)
        for path in world.paths.values()
    )
    assert (
        world.paths["done"].exists()
        and (world.paths["done"] / ".dev" / "tasks" / "note.md").exists()
    )
    assert "(1 removable; dry run, nothing was removed)" in capsys.readouterr().out


def test_removable_row_with_terminals_open_says_they_will_be_closed_first(
    wc, world, capsys
):
    world.add("done")
    world.listed = {"done"}

    def with_terminals(argv, cwd):
        if tuple(argv[1:3]) == ("worktree", "ps"):
            rows = [{"worktreeId": "id-done", "path": str(world.paths["done"]), "isPinned": False,
                     "liveTerminalCount": 2, "lastActivityAt": None, "linkedPR": None, "comment": ""}]  # fmt: skip
            return wc.Result(
                0, json.dumps({"ok": True, "result": {"worktrees": rows}}), ""
            )
        return World.orca(world, argv, cwd)

    world.runner.replies["orca"] = with_terminals
    assert world.run("list", out=False) == 0
    assert "its Orca terminals will be closed first" in capsys.readouterr().out
    assert not any(
        a[:3] == ["orca", "terminal", "close"]
        for a in [c.argv for c in world.runner.commands]
    )


# -- prune --apply: only removable rows are processed ------------------------------------------------


def test_prune_apply_removes_only_the_removable_rows_and_a_second_run_has_nothing_to_do(
    world, capsys
):
    world.add("done")
    world.add("open", state="OPEN")
    world.add("plain", dev=False)
    assert world.run("prune", "--apply") == 0
    shown = capsys.readouterr().out
    assert not world.paths["done"].exists() and not world.paths["plain"].exists()
    assert (
        world.paths["open"].exists()
        and (world.paths["open"] / ".dev" / "tasks" / "note.md").exists()
    )
    assert "summary: removed 2, kept 2, failed 0" in shown
    removed_paths = {
        c[-1]
        for c in world.removal_commands()
        if c[:3] == ["git", "worktree", "remove"]
    }
    assert removed_paths == {str(world.paths["done"]), str(world.paths["plain"])}
    cleared = [c for c in world.runner.commands if c.argv[:2] == ["xargs", "-0"]]
    assert len(cleared) == 1 and cleared[0].cwd == str(world.paths["done"])
    doc = json.loads(next(world.out.glob("prune-*.json")).read_text())
    decisions = {r["folder"]: r["decision"] for r in doc["rows"]}
    assert decisions == {
        "main": "kept",
        "done": "removed",
        "plain": "removed",
        "open": "kept",
    }
    # the save reached the evidence remote before the clear
    assert (
        git_in(world.bare, "ls-tree", "-r", "--name-only", "main").count("note.md") == 1
    )
    # a second run after the removal: nothing more to do
    assert world.run("prune", "--apply") == 0
    assert "nothing more to do" in capsys.readouterr().out
    assert world.removal_commands() == []


def test_removal_through_orca_when_orca_lists_the_worktree(world, capsys):
    world.add("done")
    world.listed = {"done"}
    assert world.run("prune", "--apply") == 0
    assert ["orca", "worktree", "rm", "--worktree", "id:id-done"] in world.orca_calls
    assert not world.paths["done"].exists()
    assert not any(
        c.argv[:3] == ["git", "worktree", "remove"] for c in world.runner.commands
    )


# -- the lock ---------------------------------------------------------------------------------------------


def test_a_second_run_cannot_remove_what_a_run_holding_the_lock_is_removing(
    wc, world, capsys
):
    world.add("done")
    holder = wc.RepoLocks(world.out)
    assert holder.acquire(str(world.repo.main)) is True
    try:
        assert world.run("prune", "--apply") == 0
    finally:
        holder.release_all()
    shown = capsys.readouterr().out
    assert "another run holds the lock" in shown
    assert world.paths["done"].exists() and world.removal_commands() == []
    locks = list(world.out.glob("lock-*.lock"))
    assert len(locks) == 1 and locks[0].exists()  # the lock file is never deleted
    # once the first run is over the lock is free and the removal goes through
    assert world.run("prune", "--apply") == 0
    assert (
        not world.paths["done"].exists()
        and len(list(world.out.glob("lock-*.lock"))) == 1
    )


def test_the_lock_is_per_repo(wc, tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    a.mkdir()
    b.mkdir()
    one, two = wc.RepoLocks(tmp_path / "o"), wc.RepoLocks(tmp_path / "o")
    assert one.acquire(str(a)) and one.acquire(str(a))  # the same run may ask again
    assert two.acquire(str(a)) is False and two.acquire(str(b)) is True
    one.release_all()
    two.release_all()
    assert wc.RepoLocks(tmp_path / "o").acquire(str(a)) is True


# -- retire ------------------------------------------------------------------------------------------------


def test_retire_by_folder_name_or_path_removes_one_worktree_under_apply(world, capsys):
    world.add("done")
    world.add("other")
    assert world.run("retire", "done") == 0  # dry run: nothing happens
    assert world.paths["done"].exists() and "dry run" in capsys.readouterr().out
    assert world.removal_commands() == []
    assert world.run("retire", str(world.paths["done"]) + "/", "--apply") == 0
    assert not world.paths["done"].exists() and world.paths["other"].exists()
    assert world.run("retire", "other", "--apply") == 0
    assert not world.paths["other"].exists()


def test_retire_exit_64_for_unknown_ambiguous_not_removable_or_run_from_inside(
    wc, world, runner_cls, capsys
):
    world.add("done")
    world.add("open", state="OPEN")
    assert world.run("retire", "nope", "--apply") == 64
    assert "is not a git worktree of one of our repos" in capsys.readouterr().err
    assert world.run("retire", "open", "--apply") == 64
    assert "not removable: pull request #700 is open" in capsys.readouterr().err
    assert (
        world.run("retire", "main", "--apply") == 64
    )  # the main checkout is never removable
    assert (
        world.run("retire", "done", "--apply", cwd=str(world.paths["done"] / ".dev"))
        == 64
    )
    assert "outside the worktree" in capsys.readouterr().err
    assert world.paths["done"].exists() and world.removal_commands() == []
    # two worktrees with the same folder name in two repos: ambiguous
    found = wc.Found(
        [(wc.GitWorktree(f"/a/{n}", "/a", "h", "b", False, False, False, False, False), None) for n in ("same",)]
        + [(wc.GitWorktree("/b/same", "/b", "h", "b", False, False, False, False, False), None)],
        [], [],
    )  # fmt: skip
    match, problem = wc.resolve_selector(found, "same")
    assert match is None and "matches 2 worktrees" in problem
    assert wc.resolve_selector(found, "/b/same")[0] is found.worktrees[1]


# -- archive -------------------------------------------------------------------------------------------------


def test_archive_saves_and_prints_verified_and_removes_nothing(world, capsys):
    world.add("done")
    before = world.snapshot()
    assert world.run("archive", "done") == 0
    shown = capsys.readouterr().out
    assert any(
        ln.startswith("VERIFIED IronClaude/") or ln.startswith("VERIFIED example/")
        for ln in shown.splitlines()
    )
    assert world.snapshot() == before and world.paths["done"].exists()
    assert not any(
        c[:3] == ["git", "worktree", "remove"] for c in world.removal_commands()
    )
    assert world.run("archive", "done") == 0  # a repeat verifies the same folder


def test_archive_refuses_a_worktree_with_a_tracked_edit_or_without_a_merged_request(
    world, capsys
):
    path = world.add("edited")
    (path / "README.md").write_text("edited\n", encoding="utf-8")
    assert world.run("archive", "edited") == 64
    assert "cannot archive: 1 changed tracked file" in capsys.readouterr().err
    world.add("unmerged", state="OPEN")
    assert world.run("archive", "unmerged") == 64
    assert not Path(world.clone).exists()  # nothing was cloned or saved


# -- exit codes --------------------------------------------------------------------------------------------------


def test_exit_69_when_a_lookup_fails_and_the_table_still_shows_it(wc, world, capsys):
    world.add("done")
    world.gh_override[("pr", "list")] = lambda argv: wc.Result(1, "", "HTTP 502")
    assert world.run("prune") == 69
    shown = capsys.readouterr().out
    assert "pull request lookup failed" in shown and "failed 1" in shown
    assert world.removal_commands() == []


def test_exit_69_when_a_removal_fails_and_the_summary_carries_the_three_counts(
    wc, runner_cls, throwaway_repo, evidence_bare, tmp_path, capsys
):
    w = World(wc, runner_cls, throwaway_repo, evidence_bare, tmp_path)
    w.add("done")

    def refuse(argv, cwd):
        if argv[1:3] == ["worktree", "remove"]:
            return wc.Result(128, "", "fatal: refused")
        return None

    w.runner.replies["git"] = refuse
    assert w.run("prune", "--apply") == 69
    shown = capsys.readouterr().out
    assert "summary: removed 0, kept 1, failed 1" in shown
    assert w.paths["done"].exists()


def test_exit_64_when_out_is_inside_a_worktree(world, capsys):
    path = world.add("done")
    assert world.run("prune", "--out", str(path / "inside"), out=False) == 64
    assert "--out must not be inside a worktree" in capsys.readouterr().err
    assert not (path / "inside").exists()
    assert world.removal_commands() == []


def test_exit_69_when_no_repo_can_be_found(wc, runner_cls, tmp_path, capsys):
    runner = runner_cls(evidence_dir=str(tmp_path / "e"))
    code = wc.main(
        ["list"], runner=runner, env={}, cwd=str(tmp_path), proc_root=str(tmp_path)
    )
    assert code == 69
    assert "not a git checkout" in capsys.readouterr().err


def test_a_folder_that_is_not_a_git_worktree_never_appears(world, capsys):
    world.add("done")
    stray = world.repo.root / "wts" / "stray-folder"
    stray.mkdir()
    write(stray / "file.txt")
    assert world.run("list", out=False) == 0
    assert "stray-folder" not in capsys.readouterr().out
    assert (stray / "file.txt").exists()


def test_the_orca_repo_list_failing_falls_back_to_the_current_repo_and_says_so(
    wc, world, capsys
):
    world.add("done")

    def orca_down(argv, cwd):
        return wc.Result(1, "", "down")

    world.runner.replies["orca"] = orca_down
    # unreadable Orca facts (pinned, terminals) are a lookup failure: exit 69, nothing removable
    assert world.run("list", out=False, cwd=str(world.repo.main)) == 69
    shown = capsys.readouterr().out
    assert "note: Orca unavailable" in shown and "current checkout" in shown
    assert "| done |" in shown
    assert "Orca unavailable, so whether it is pinned is unknown" in shown
    assert "removable" not in shown.replace("no worktree can be removed", "")


def test_an_unreadable_orca_never_lets_a_pinned_worktree_be_removed(wc, world, capsys):
    world.add("done")
    world.listed = {"done"}

    def pinned_but_unreadable(argv, cwd):
        if tuple(argv[1:3]) == ("worktree", "ps"):
            return wc.Result(0, "<html>", "")  # Orca answered, but not with a list
        return World.orca(world, argv, cwd)

    world.runner.replies["orca"] = pinned_but_unreadable
    assert world.run("prune", "--apply") == 69
    assert world.paths["done"].exists() and world.removal_commands() == []
    assert "failed 1" in capsys.readouterr().out
    assert world.run("retire", "done", "--apply") == 69
    assert world.paths["done"].exists() and world.removal_commands() == []


# -- every unreadable fact is a lookup failure (exit 69), for every verb ----------------------------------------------


def test_a_landed_check_that_says_unknown_is_exit_69_for_prune_retire_and_archive(
    wc, world, capsys
):
    world.add("done")
    world.gh_override[("pr", "view")] = lambda argv: wc.Result(1, "", "HTTP 502")
    assert world.run("prune") == 69
    assert "landed check said UNKNOWN" in capsys.readouterr().out
    assert world.run("retire", "done", "--apply") == 69
    assert world.run("archive", "done") == 69
    assert world.paths["done"].exists() and world.removal_commands() == []


def test_a_pull_request_lookup_that_fails_is_exit_69_for_retire_and_archive(
    wc, world, capsys
):
    world.add("done")
    world.gh_override[("pr", "list")] = lambda argv: wc.Result(1, "", "HTTP 502")
    assert world.run("retire", "done", "--apply") == 69
    assert "pull request lookup failed" in capsys.readouterr().err
    assert world.run("archive", "done") == 69
    assert world.run("prune") == 69


def test_a_selector_in_a_repo_whose_worktree_list_failed_is_exit_69(wc, world, capsys):
    world.add("done")

    def list_fails(argv, cwd):
        return (
            wc.Result(128, "", "fatal") if argv[1:3] == ["worktree", "list"] else None
        )

    world.runner.replies["git"] = list_fails
    assert world.run("retire", "done", "--apply") == 69
    assert "git worktree list failed" in capsys.readouterr().err


# -- the output folder -------------------------------------------------------------------------------------------


def test_archive_and_retire_also_refuse_an_output_folder_inside_a_worktree(
    world, capsys
):
    path = world.add("done")
    for verb in (("archive", "done"), ("retire", "done", "--apply"), ("list",)):
        assert world.run(*verb, "--out", str(path / ".dev" / "out"), out=False) == 64
        assert "--out must not be inside a worktree" in capsys.readouterr().err
    assert not (path / ".dev" / "out").exists() and world.removal_commands() == []
    assert path.exists()


def test_an_output_folder_that_cannot_be_used_stops_before_any_removal(world, capsys):
    world.add("done")
    blocker = world.tmp / "a-file"
    blocker.write_text("not a folder\n", encoding="utf-8")
    assert world.run("prune", "--apply", "--out", str(blocker / "sub"), out=False) == 69
    assert "--out cannot be used" in capsys.readouterr().err
    assert world.paths["done"].exists() and world.removal_commands() == []
    # retire and archive hit the same problem when they take the lock
    assert (
        world.run("retire", "done", "--apply", "--out", str(blocker / "sub"), out=False)
        == 69
    )
    assert "lock could not be taken" in capsys.readouterr().out
    assert world.paths["done"].exists() and world.removal_commands() == []
    assert world.run("archive", "done", "--out", str(blocker / "sub"), out=False) == 69
    assert "lock could not be taken" in capsys.readouterr().err


def test_output_files_that_cannot_be_written_give_exit_69_after_the_table(
    wc, world, capsys, monkeypatch
):
    world.add("done")

    def refuse(self, *a, **k):
        raise OSError(30, "Read-only file system")

    monkeypatch.setattr(Path, "write_text", refuse)
    assert world.run("prune") == 69
    shown = capsys.readouterr()
    assert "summary:" in shown.out  # the table and the summary were printed first
    assert "the output files could not be written" in shown.err


# -- a fact that cannot be read at the re-check is a failure (exit 69); a change is a plain "kept" -----------------------


def _break_the_recheck(wc, world, monkeypatch, case):
    """Let the first read of the worktree through; make the read after the save fail."""
    plain = str(world.paths["plain"])
    if case == "scan":
        calls = []
        real_scan = wc.scan_processes

        def scan(*a, **k):
            calls.append(1)
            return (
                real_scan(*a, **k)
                if len(calls) == 1
                else wc.ProcScan(False, failure="x")
            )

        monkeypatch.setattr(wc, "scan_processes", scan)
        return
    seen = []
    real = wc.gather_facts

    def facts(runner, wt, orca=None):
        got = real(runner, wt, orca)
        if wt.path != plain:
            return got
        seen.append(1)
        if len(seen) == 1:
            return got
        if case == "status":
            return dataclasses.replace(got, state=None)
        return dataclasses.replace(got, present=False)

    monkeypatch.setattr(wc, "gather_facts", facts)


@pytest.mark.parametrize("case", ["status", "folder", "scan"])
def test_prune_apply_exits_69_when_the_re_check_cannot_read_a_fact(
    wc, world, capsys, monkeypatch, case
):
    world.add("plain", dev=False)
    _break_the_recheck(wc, world, monkeypatch, case)
    assert world.run("prune", "--apply") == 69
    shown = capsys.readouterr().out
    assert "failed 1" in shown
    doc = json.loads(next(world.out.glob("prune-*.json")).read_text())
    assert {r["folder"]: r["decision"] for r in doc["rows"]}["plain"] == "failed"
    assert doc["summary"]["failed"] == 1
    assert world.paths["plain"].exists()
    assert world.removal_commands() == []


@pytest.mark.parametrize("case", ["status", "folder", "scan"])
def test_retire_apply_exits_69_when_the_re_check_cannot_read_a_fact(
    wc, world, capsys, monkeypatch, case
):
    world.add("plain", dev=False)
    _break_the_recheck(wc, world, monkeypatch, case)
    assert world.run("retire", "plain", "--apply") == 69
    assert world.paths["plain"].exists() and world.removal_commands() == []


def test_a_real_change_during_the_terminal_close_is_still_kept(wc, world, capsys):
    world.add("done")
    world.listed = {"done"}
    path = world.paths["done"]

    def busy(argv, cwd):
        key = tuple(argv[1:3])
        if key == ("worktree", "ps"):
            rows = [{"worktreeId": "id-done", "path": str(path), "isPinned": False,
                     "liveTerminalCount": 1, "lastActivityAt": None, "linkedPR": None, "comment": ""}]  # fmt: skip
            return wc.Result(
                0, json.dumps({"ok": True, "result": {"worktrees": rows}}), ""
            )
        if key == ("terminal", "close"):
            write(path / "made-by-the-terminal.txt")  # an agent was still working
            return wc.Result(0, "", "")
        return World.orca(world, argv, cwd)

    world.runner.replies["orca"] = busy
    assert world.run("prune", "--apply") == 0
    assert "changed since the terminals were closed" in capsys.readouterr().out
    assert path.exists()
    assert not any(c[:2] == ["xargs", "-0"] for c in world.removal_commands())
    assert world.run("retire", "done", "--apply") == 64
    assert path.exists()
