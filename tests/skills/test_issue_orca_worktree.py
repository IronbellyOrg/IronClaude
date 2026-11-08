"""Tests for ``scripts/orca_worktree.py`` (the Orca step of ``/sc:issue --claim``).

No test calls a real ``orca``, ``gh``, the network or a real agent. A fake
``orca`` executable is put first on ``PATH``; it logs every argv and answers
from JSON files the test writes. ``HOME`` is a temporary directory.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import stat
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = (
    REPO_ROOT
    / "src"
    / "superclaude"
    / "skills"
    / "sc-issue-protocol"
    / "scripts"
    / "orca_worktree.py"
)

# The fake logs one JSON argv per line to calls.jsonl and answers from
# "<subcommand words joined by ->.json" (for example "worktree-list.json").
# A response file holds {"responses": [{"stdout", "stderr", "rc", "sleep",
# "effect"}, ...]}; call number n gets responses[min(n, len - 1)], so a list
# called twice can answer differently the second time. "stdout" may be a string
# or any JSON value; "effect" is an argv run first (a real git command that
# makes the worktree the fake pretends Orca created).
FAKE_ORCA = textwrap.dedent(
    """\
    #!{python}
    import json, os, subprocess, sys, time
    d = os.environ["FAKE_ORCA_DIR"]
    argv = sys.argv[1:]
    with open(os.path.join(d, "calls.jsonl"), "a") as f:
        f.write(json.dumps(argv) + "\\n")
    pend = os.path.join(os.environ.get("HOME", ""), ".claude/state/launch-level/pending")
    with open(os.path.join(d, "pending-at-call.jsonl"), "a") as f:
        names = sorted(os.listdir(pend)) if os.path.isdir(pend) else None
        f.write(json.dumps({{"argv": argv, "pending": names}}) + "\\n")
    key = "status" if argv[:1] == ["status"] else "-".join(argv[:2])
    path = os.path.join(d, key + ".json")
    if not os.path.exists(path):
        sys.stderr.write("fake orca: no response for " + key + "\\n")
        sys.exit(1)
    counter = os.path.join(d, key + ".count")
    n = int(open(counter).read()) if os.path.exists(counter) else 0
    open(counter, "w").write(str(n + 1))
    responses = json.load(open(path))["responses"]
    r = responses[min(n, len(responses) - 1)]
    if r.get("effect"):
        subprocess.run(r["effect"], check=True, capture_output=True)
    time.sleep(r.get("sleep", 0))
    out = r.get("stdout", "")
    sys.stdout.write(out if isinstance(out, str) else json.dumps(out))
    sys.stderr.write(r.get("stderr", ""))
    sys.exit(r.get("rc", 0))
    """
)


class FakeOrca:
    def __init__(self, root: Path, home: Path) -> None:
        self.dir = root / "orca-state"
        self.bin = root / "orca-bin"
        self.dir.mkdir()
        self.bin.mkdir()
        self.home = home
        exe = self.bin / "orca"
        exe.write_text(FAKE_ORCA.format(python=sys.executable))
        exe.chmod(0o755)
        # Known jq and uv stubs (the IR-4 preflight only looks them up on PATH).
        self.tools = root / "tool-bin"
        self.tools.mkdir()
        for name in ("jq", "uv"):
            stub = self.tools / name
            stub.write_text("#!/bin/sh\nexit 0\n")
            stub.chmod(0o755)

    def path_without(self, *names: str) -> str:
        """A PATH holding orca, git and the tool stubs, minus ``names``."""
        bare = self.bin.parent / ("bare-" + "-".join(names))
        bare.mkdir()
        (bare / "git").symlink_to(shutil.which("git"))
        for stub in self.tools.iterdir():
            if stub.name not in names:
                (bare / stub.name).symlink_to(stub)
        return f"{self.bin}{os.pathsep}{bare}"

    def respond(self, key: str, *responses: dict) -> None:
        """Set the answers for one orca subcommand (``status``, ``worktree-list``...)."""
        (self.dir / f"{key}.json").write_text(
            json.dumps({"responses": list(responses)})
        )

    def calls(self) -> list[list[str]]:
        log = self.dir / "calls.jsonl"
        if not log.exists():
            return []
        return [json.loads(line) for line in log.read_text().splitlines() if line]

    def pending_at_calls(self) -> list[dict]:
        """For each orca call: its argv and the names in the pending store then."""
        log = self.dir / "pending-at-call.jsonl"
        if not log.exists():
            return []
        return [json.loads(line) for line in log.read_text().splitlines() if line]

    def env(self, **extra: str) -> dict[str, str]:
        env = dict(os.environ)
        env["PATH"] = os.pathsep.join([str(self.bin), str(self.tools), env["PATH"]])
        env.pop("CLAUDE_CONFIG_DIR", None)
        env["FAKE_ORCA_DIR"] = str(self.dir)
        env["HOME"] = str(self.home)
        # Hermetic git: the script's own git calls ignore the user's config.
        env["GIT_CONFIG_GLOBAL"] = "/dev/null"
        env["GIT_CONFIG_SYSTEM"] = "/dev/null"
        env.update(extra)
        return env


@pytest.fixture
def home(tmp_path: Path) -> Path:
    path = tmp_path / "home"
    path.mkdir()
    return path


@pytest.fixture
def fake_orca(tmp_path: Path, home: Path) -> FakeOrca:
    return FakeOrca(tmp_path, home)


def run_script(
    *args: str, env: dict[str, str], cwd: Path | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        env=env,
        cwd=cwd,
        timeout=60,
        check=False,
    )


def run_json(*args: str, env: dict[str, str], cwd: Path | None = None) -> dict:
    proc = run_script(*args, env=env, cwd=cwd)
    assert proc.returncode == 0, proc.stderr
    lines = proc.stdout.strip().splitlines()
    assert len(lines) == 1, f"expected one JSON object on stdout, got {proc.stdout!r}"
    data = json.loads(lines[0])
    assert isinstance(data, dict)
    return data


def git(cwd: Path, *args: str) -> str:
    env = dict(os.environ, GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_SYSTEM="/dev/null")
    proc = subprocess.run(
        ["git", "-C", str(cwd), *args],
        capture_output=True,
        text=True,
        env=env,
        check=True,
    )
    return proc.stdout.strip()


@pytest.fixture
def git_repo(tmp_path: Path) -> Path:
    """A throwaway checkout whose ``origin`` is a local bare repository."""
    bare = tmp_path / "origin.git"
    subprocess.run(
        ["git", "init", "--bare", "-b", "master", str(bare)],
        capture_output=True,
        check=True,
    )
    main = tmp_path / "main"
    subprocess.run(
        ["git", "init", "-b", "master", str(main)], capture_output=True, check=True
    )
    git(main, "config", "user.email", "test@example.invalid")
    git(main, "config", "user.name", "Test")
    git(main, "remote", "add", "origin", str(bare))
    (main / "README.md").write_text("fixture\n")
    git(main, "add", "README.md")
    git(main, "commit", "-m", "init")
    git(main, "push", "origin", "master")
    git(main, "fetch", "origin")
    return main


def test_fixture_git_repo_has_origin(git_repo: Path) -> None:
    assert git(git_repo, "rev-parse", "--verify", "origin/master")
    assert git(git_repo, "remote", "get-url", "origin").endswith("origin.git")


STATUS_OK = {"ok": True, "result": {"runtime": {"reachable": True}}}


def test_preflight_pf1_ok(fake_orca: FakeOrca) -> None:
    fake_orca.respond("status", {"stdout": STATUS_OK})
    data = run_json("preflight", env=fake_orca.env())
    assert data == {"ok": True}
    assert fake_orca.calls() == [["status", "--json"]]


@pytest.mark.parametrize(
    "response",
    [
        {"stdout": {"ok": True, "result": {"runtime": {"reachable": False}}}},
        {"stdout": {"ok": True, "result": {}}},
        {"stdout": {"ok": False, "result": {"runtime": {"reachable": True}}}},
        {"stdout": [1, 2]},
        {"stdout": "not json at all"},
        {"stdout": "", "stderr": "orca: runtime not running\nmore\n", "rc": 1},
    ],
    ids=[
        "unreachable",
        "no-runtime",
        "ok-false",
        "json-not-object",
        "invalid-json",
        "nonzero-exit",
    ],
)
def test_preflight_pf2_not_ok(fake_orca: FakeOrca, response: dict) -> None:
    fake_orca.respond("status", response)
    data = run_json("preflight", env=fake_orca.env())
    assert data["ok"] is False
    assert isinstance(data["detail"], str) and data["detail"].strip()


def test_preflight_pf2_nonzero_exit_detail_is_first_stderr_line(
    fake_orca: FakeOrca,
) -> None:
    fake_orca.respond(
        "status", {"stdout": "", "stderr": "orca: runtime not running\nmore\n", "rc": 1}
    )
    data = run_json("preflight", env=fake_orca.env())
    assert data == {"ok": False, "detail": "orca: runtime not running"}


def test_preflight_pf2_no_orca_on_path(tmp_path: Path, home: Path) -> None:
    empty = tmp_path / "empty-bin"
    empty.mkdir()
    env = dict(os.environ, PATH=str(empty), HOME=str(home))
    data = run_json("preflight", env=env)
    assert data["ok"] is False
    assert data["detail"].strip()


def test_preflight_hanging_orca_is_cut_by_the_timeout(fake_orca: FakeOrca) -> None:
    fake_orca.respond("status", {"stdout": STATUS_OK, "sleep": 30})
    data = run_json("preflight", env=fake_orca.env(SC_ORCA_TIMEOUT="0.5"))
    assert data == {"ok": False, "detail": "timed out"}


def test_arg1_bad_subcommand_and_missing_subcommand_exit_2(fake_orca: FakeOrca) -> None:
    assert run_script("nonsense", env=fake_orca.env()).returncode == 2
    assert run_script(env=fake_orca.env()).returncode == 2
    assert run_script("preflight", "--bogus", env=fake_orca.env()).returncode == 2
    assert fake_orca.calls() == []


# --- worktree ----------------------------------------------------------------

REPO = "IronbellyOrg/IronClaude"
NUMBER = 302
MARKER = f"sc:issue {REPO}#{NUMBER}"
FORBIDDEN_FLAGS = (
    "--issue",
    "--pr",
    "--reference",
    "--linear-issue",
    "--gitlab",
    "--agent",
    "--prompt",
    "--model",
    "--effort",
    "--surface",
    "--setup",
    "--branch",
    "--activate",
    "--run-hooks",
)


def row(
    path: Path | str,
    branch: str = "refs/heads/ironbelly/other",
    *,
    comment: str = "",
    main: bool = False,
    archived: bool = False,
    row_id: str | None = None,
) -> dict:
    """One row of ``orca worktree list --json`` (shape copied from a live run)."""
    return {
        "id": row_id or f"repo::{path}",
        "path": str(path),
        "branch": branch,
        "comment": comment,
        "isMainWorktree": main,
        "isArchived": archived,
    }


def listing(*rows: dict, truncated: bool = False, omitted: tuple = ()) -> dict:
    return {
        "ok": True,
        "result": {
            "worktrees": list(rows),
            "totalCount": len(rows),
            "truncated": truncated,
            "hostScope": {"omittedHostIds": list(omitted)},
        },
    }


def add_worktree(git_repo: Path, name: str, branch: str) -> Path:
    """A real linked worktree (the fake Orca only reports it)."""
    path = git_repo.parent / "wts" / name
    git(git_repo, "worktree", "add", "-b", branch, str(path), "origin/master")
    return path


@pytest.fixture
def issue_dir(tmp_path: Path) -> Path:
    path = tmp_path / "claim" / str(NUMBER)
    (path / "analysis").mkdir(parents=True)
    (path / "issue-summary.md").write_text("summary\n")
    (path / "next-steps.md").write_text("steps\n")
    (path / "analysis" / "notes.md").write_text("notes\n")
    return path


def main_row(git_repo: Path) -> dict:
    return row(git_repo, "refs/heads/master", main=True, row_id="main")


def run_wt(
    fake: FakeOrca,
    git_repo: Path,
    source: Path,
    base: str = "origin/master",
    **env: str,
) -> dict:
    return run_json(
        "worktree",
        "--repo",
        REPO,
        "--number",
        str(NUMBER),
        "--base",
        base,
        "--source",
        str(source),
        env=fake.env(**env),
        cwd=git_repo,
    )


def orca_calls(fake: FakeOrca, *words: str) -> list[list[str]]:
    return [c for c in fake.calls() if c[: len(words)] == list(words)]


def read_record(source: Path) -> dict:
    return json.loads((source / "worktree.json").read_text())


# An ok create reply with no setup and no default tabs (the envelope `--json` prints).
CREATE_OK = {"ok": True, "result": {"worktree": {"id": "wt-1"}}}
TAB_CLOSED = {"ok": True, "result": {"closed": 1}}


def terminal_row(handle: str = "term_plain", **extra: object) -> dict:
    return {"handle": handle, "title": None, "connected": True} | extra


def terminals(*rows: dict) -> dict:
    return {"ok": True, "result": {"terminals": list(rows)}}


def created_scene(
    fake: FakeOrca,
    git_repo: Path,
    *,
    effect: bool = True,
    name: str = "issue-302",
    reply: object = "opaque, not json",
) -> Path:
    """Orca lists only the main row, creates `name`, then lists the new row too.

    ``reply`` is the create's stdout: opaque text by default (no tab close can
    follow it), ``CREATE_OK`` for a reply the close step accepts.
    """
    wt = git_repo.parent / "wts" / name
    cmd = [
        "git", "-C", str(git_repo), "worktree", "add", "-b", f"ironbelly/{name}",
        str(wt), "origin/master",
    ]  # fmt: skip
    fake.respond(
        "worktree-create",
        {"stdout": reply} | ({"effect": cmd} if effect else {}),
    )
    fake.respond(
        "worktree-list",
        {"stdout": listing(main_row(git_repo))},
        {
            "stdout": listing(
                main_row(git_repo), row(wt, f"refs/heads/ironbelly/{name}")
            )
        },
    )
    return wt


def test_fo1_list_fails_with_guarded_record_reuses_it(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    wt = add_worktree(git_repo, "issue-302", "ironbelly/issue-302")
    (issue_dir / "worktree.json").write_text(
        json.dumps({"path": str(wt), "status": "created"})
    )
    fake_orca.respond("worktree-list", {"stdout": "", "stderr": "down\n", "rc": 1})
    data = run_wt(fake_orca, git_repo, issue_dir)
    assert data["status"] == "reused"
    assert data["match_key"] == "record"
    assert data["warning"] == "W-ORCA-LIST-FAILED"
    assert "unverified" in data["detail"]
    assert data["path"] == str(wt)
    assert (wt / ".dev/issues/302/analysis/notes.md").read_text() == "notes\n"
    assert orca_calls(fake_orca, "worktree", "create") == []


def test_fo1_list_fails_without_a_usable_record_fails(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path, tmp_path: Path
) -> None:
    fake_orca.respond("worktree-list", {"stdout": "", "stderr": "down\n", "rc": 1})
    assert run_wt(fake_orca, git_repo, issue_dir)["warning"] == "W-ORCA-LIST-FAILED"
    # A record whose path is a directory of some other repository is not trusted.
    other = tmp_path / "other"
    other.mkdir()
    subprocess.run(["git", "init", "-q", str(other)], check=True)
    (issue_dir / "worktree.json").write_text(json.dumps({"path": str(other)}))
    data = run_wt(fake_orca, git_repo, issue_dir)
    assert data["status"] == "failed" and data["warning"] == "W-ORCA-LIST-FAILED"
    assert orca_calls(fake_orca, "worktree", "create") == []
    assert not (other / ".dev").exists()


def test_fo2_marker_decides_before_basename(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    by_marker = add_worktree(git_repo, "renamed-by-hand", "ironbelly/renamed")
    by_name = add_worktree(git_repo, "issue-302", "ironbelly/issue-302")
    fake_orca.respond(
        "worktree-list",
        {
            "stdout": listing(
                main_row(git_repo),
                row(by_name),
                row(by_marker, comment=f"hello {MARKER} bye"),
            )
        },
    )
    data = run_wt(fake_orca, git_repo, issue_dir)
    assert (data["status"], data["match_key"], data["path"]) == (
        "reused",
        "marker",
        str(by_marker),
    )
    assert read_record(issue_dir) == {"path": str(by_marker), "status": "reused"}


def test_fo3_longer_issue_number_in_marker_does_not_match(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    wt = add_worktree(git_repo, "issue-302", "ironbelly/issue-302")
    fake_orca.respond(
        "worktree-list",
        {
            "stdout": listing(
                main_row(git_repo), row(wt, comment=f"{MARKER}0 and x{MARKER}")
            )
        },
    )
    data = run_wt(fake_orca, git_repo, issue_dir)
    assert (data["status"], data["match_key"]) == ("reused", "basename")


@pytest.mark.parametrize("name", ["issue-302", "issue-302-2"])
def test_fo4_basename_with_and_without_suffix(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path, name: str
) -> None:
    wt = add_worktree(git_repo, name, f"ironbelly/{name}")
    fake_orca.respond(
        "worktree-list", {"stdout": listing(main_row(git_repo), row(wt, comment=""))}
    )
    data = run_wt(fake_orca, git_repo, issue_dir)
    assert (data["status"], data["match_key"], data["path"]) == (
        "reused",
        "basename",
        str(wt),
    )


def test_fo4_issue_3020_is_not_issue_302(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    other = add_worktree(git_repo, "issue-3020", "ironbelly/issue-3020")
    wt = created_scene(fake_orca, git_repo)
    fake_orca.respond(
        "worktree-list",
        {"stdout": listing(main_row(git_repo), row(other))},
        {"stdout": listing(main_row(git_repo), row(other), row(wt))},
    )
    assert run_wt(fake_orca, git_repo, issue_dir)["status"] == "created"


def test_fo13_prefixed_branch_matches_on_its_last_segment(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    wt = add_worktree(git_repo, "picked-by-hand", "ironbelly/issue-302")
    fake_orca.respond(
        "worktree-list",
        {
            "stdout": listing(
                main_row(git_repo), row(wt, "refs/heads/ironbelly/issue-302")
            )
        },
    )
    data = run_wt(fake_orca, git_repo, issue_dir)
    assert (data["status"], data["match_key"]) == ("reused", "branch")
    assert data["branch"] == "ironbelly/issue-302"


def test_fo8_two_live_hits_are_ambiguous_and_nothing_is_created(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    a = add_worktree(git_repo, "issue-302", "ironbelly/issue-302")
    b = add_worktree(git_repo, "issue-302-2", "ironbelly/issue-302-2")
    fake_orca.respond(
        "worktree-list", {"stdout": listing(main_row(git_repo), row(a), row(b))}
    )
    data = run_wt(fake_orca, git_repo, issue_dir)
    assert data["status"] == "failed" and data["warning"] == "W-WORKTREE-AMBIGUOUS"
    assert str(a) in data["detail"] and str(b) in data["detail"]
    assert orca_calls(fake_orca, "worktree", "create") == []
    assert not (issue_dir / "worktree.json").exists()


def test_fo10_stale_hit_only_fails_without_creating(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path, tmp_path: Path
) -> None:
    gone = tmp_path / "wts" / "issue-302"
    fake_orca.respond(
        "worktree-list", {"stdout": listing(main_row(git_repo), row(gone))}
    )
    data = run_wt(fake_orca, git_repo, issue_dir)
    assert data["status"] == "failed" and data["warning"] == "W-WORKTREE-STALE"
    assert orca_calls(fake_orca, "worktree", "create") == []


def test_fo9_archived_row_is_ignored_and_a_worktree_is_created(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path, tmp_path: Path
) -> None:
    old = row(tmp_path / "wts" / "old-issue-302", archived=True, comment=MARKER)
    wt = created_scene(fake_orca, git_repo)
    fake_orca.respond(
        "worktree-list",
        {"stdout": listing(main_row(git_repo), old)},
        {"stdout": listing(main_row(git_repo), old, row(wt))},
    )
    data = run_wt(fake_orca, git_repo, issue_dir)
    assert data["status"] == "created"
    assert len(orca_calls(fake_orca, "worktree", "create")) == 1


def test_fo11_created_worktree_path_comes_from_the_list_not_the_create_json(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    wt = created_scene(fake_orca, git_repo)
    data = run_wt(fake_orca, git_repo, issue_dir)
    assert data["status"] == "created" and data["match_key"] is None
    assert data["path"] == str(wt) and data["branch"] == "ironbelly/issue-302"
    # An opaque create reply is unknown: the plain first tab is left, nothing is closed.
    assert data["warning"] == "W-FIRST-TAB-LEFT"
    assert orca_calls(fake_orca, "terminal") == []
    assert (wt / ".dev/issues/302/issue-summary.md").read_text() == "summary\n"
    assert read_record(issue_dir) == {"path": str(wt), "status": "created"}


def test_fo11_create_that_never_shows_up_in_the_list_fails(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    created_scene(fake_orca, git_repo, effect=False)
    fake_orca.respond("worktree-list", {"stdout": listing(main_row(git_repo))})
    data = run_wt(fake_orca, git_repo, issue_dir)
    assert data["status"] == "failed" and data["warning"] == "W-WORKTREE-CREATE-FAILED"
    assert "not listed" in data["detail"]
    assert not (issue_dir / "worktree.json").exists()
    assert len(orca_calls(fake_orca, "worktree", "create")) == 1


def test_fo11_two_new_rows_are_ambiguous_without_copy_or_record(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    a = add_worktree(git_repo, "issue-302", "ironbelly/issue-302")
    b = add_worktree(git_repo, "issue-302-2", "ironbelly/issue-302-2")
    fake_orca.respond("worktree-create", {"stdout": "{}"})
    fake_orca.respond(
        "worktree-list",
        {"stdout": listing(main_row(git_repo))},
        {"stdout": listing(main_row(git_repo), row(a), row(b))},
    )
    data = run_wt(fake_orca, git_repo, issue_dir)
    assert data["status"] == "failed" and data["warning"] == "W-WORKTREE-AMBIGUOUS"
    assert not (a / ".dev").exists() and not (b / ".dev").exists()
    assert not (issue_dir / "worktree.json").exists()


def test_fo11_create_nonzero_exit_is_failed_and_never_retried(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    fake_orca.respond("worktree-list", {"stdout": listing(main_row(git_repo))})
    fake_orca.respond(
        "worktree-create", {"stdout": "", "stderr": "no such base\nmore\n", "rc": 3}
    )
    data = run_wt(fake_orca, git_repo, issue_dir)
    assert data["status"] == "failed" and data["warning"] == "W-WORKTREE-CREATE-FAILED"
    assert data["detail"] == "no such base"
    assert len(orca_calls(fake_orca, "worktree", "create")) == 1
    assert len(orca_calls(fake_orca, "worktree", "list")) == 1


def test_fo6_create_timeout_is_followed_by_the_second_list(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    wt = created_scene(fake_orca, git_repo)
    cmd = [
        "git", "-C", str(git_repo), "worktree", "add", "-b", "ironbelly/issue-302",
        str(wt), "origin/master",
    ]  # fmt: skip
    fake_orca.respond("worktree-create", {"effect": cmd, "sleep": 30})
    data = run_wt(fake_orca, git_repo, issue_dir, SC_ORCA_TIMEOUT="3")
    assert data["status"] == "created" and data["path"] == str(wt)
    assert len(orca_calls(fake_orca, "worktree", "list")) == 2


def test_fo6_create_timeout_with_no_new_row_is_failed_not_a_crash(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    fake_orca.respond("worktree-list", {"stdout": listing(main_row(git_repo))})
    fake_orca.respond("worktree-create", {"sleep": 30})
    data = run_wt(fake_orca, git_repo, issue_dir, SC_ORCA_TIMEOUT="1")
    assert data["status"] == "failed" and data["warning"] == "W-WORKTREE-CREATE-FAILED"
    assert "timed out" in data["detail"]
    assert len(orca_calls(fake_orca, "worktree", "list")) == 2


def test_fo7_copy_error_is_failed_and_writes_no_record(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    wt = add_worktree(git_repo, "issue-302", "ironbelly/issue-302")
    (wt / ".dev/issues/302").mkdir(parents=True)
    (wt / ".dev/issues/302/analysis").write_text("a file where a directory belongs\n")
    fake_orca.respond("worktree-list", {"stdout": listing(main_row(git_repo), row(wt))})
    data = run_wt(fake_orca, git_repo, issue_dir)
    assert data["status"] == "failed" and data["warning"] == "W-WORKTREE-COPY-FAILED"
    assert "analysis" in data["detail"]
    assert not (issue_dir / "worktree.json").exists()


@pytest.mark.parametrize(
    "payload",
    [
        {"ok": False, "result": {}},
        "truncated",
        "omitted",
        "zero",
        "no-main",
        "garbage",
    ],
)
def test_fo12_unusable_list_never_creates(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path, payload: object
) -> None:
    main = main_row(git_repo)
    other = row("/nowhere/x")
    stdout: object = {
        "truncated": listing(main, other, truncated=True),
        "omitted": listing(main, other, omitted=("host-2",)),
        "zero": listing(),
        "no-main": listing(other),
        "garbage": "not json",
    }.get(payload if isinstance(payload, str) else "", payload)
    fake_orca.respond("worktree-list", {"stdout": stdout})
    data = run_wt(fake_orca, git_repo, issue_dir)
    assert data["status"] == "failed" and data["warning"] == "W-ORCA-LIST-FAILED"
    assert data["detail"]
    assert orca_calls(fake_orca, "worktree", "create") == []


def test_fo12_unusable_list_after_the_create_is_failed_too(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    created_scene(fake_orca, git_repo)
    fake_orca.respond(
        "worktree-list",
        {"stdout": listing(main_row(git_repo))},
        {"stdout": listing(main_row(git_repo), truncated=True)},
    )
    data = run_wt(fake_orca, git_repo, issue_dir)
    assert data["status"] == "failed" and data["warning"] == "W-ORCA-LIST-FAILED"
    assert not (issue_dir / "worktree.json").exists()


def test_fo14_prev_files_and_tracked_files(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    wt = add_worktree(git_repo, "issue-302", "ironbelly/issue-302")
    dest = wt / ".dev/issues/302"
    (dest / "analysis").mkdir(parents=True)
    (dest / "issue-summary.md").write_text("an older, hand-edited summary\n")
    (dest / "issue-summary.md.prev").write_text("even older\n")
    (dest / "analysis/notes.md").write_text("notes\n")  # identical: untouched
    (dest / "next-steps.md").write_text("tracked on the branch\n")
    git(wt, "add", ".dev/issues/302/next-steps.md")
    git(wt, "commit", "-m", "track next-steps")
    (issue_dir / "extra.md").write_text("new file\n")
    fake_orca.respond("worktree-list", {"stdout": listing(main_row(git_repo), row(wt))})
    data = run_wt(fake_orca, git_repo, issue_dir)
    assert data["status"] == "reused" and data["warning"] == "W-WORKTREE-COPY-FAILED"
    assert "issue-summary.md" in data["detail"] and "next-steps.md" in data["detail"]
    assert "analysis/notes.md" not in data["detail"]
    assert (dest / "issue-summary.md").read_text() == "summary\n"
    assert (
        dest / "issue-summary.md.prev"
    ).read_text() == "an older, hand-edited summary\n"
    assert (dest / "next-steps.md").read_text() == "tracked on the branch\n"
    assert (dest / "extra.md").read_text() == "new file\n"
    assert data["tracked_known"] is True
    assert data["tracked_files"] == [".dev/issues/302/next-steps.md"]


def test_fo14_when_git_cannot_say_what_is_tracked_nothing_is_overwritten(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    # git quotes an unusual file name in ls-files output, so the tracked set
    # cannot be trusted: copy only what is missing, rename or overwrite nothing.
    wt = add_worktree(git_repo, "issue-302", "ironbelly/issue-302")
    dest = wt / ".dev/issues/302"
    dest.mkdir(parents=True)
    (dest / "café.md").write_text("tracked version\n")
    git(wt, "add", ".")
    git(wt, "commit", "-m", "track cafe")
    (dest / "issue-summary.md").write_text("different\n")
    (issue_dir / "café.md").write_text("source version\n")
    fake_orca.respond("worktree-list", {"stdout": listing(main_row(git_repo), row(wt))})
    data = run_wt(fake_orca, git_repo, issue_dir)
    assert data["tracked_known"] is False and data["tracked_files"] == []
    assert data["warning"] == "W-WORKTREE-COPY-FAILED"
    assert (dest / "café.md").read_text() == "tracked version\n"
    assert (dest / "issue-summary.md").read_text() == "different\n"
    assert not list(dest.rglob("*.prev"))
    assert (dest / "next-steps.md").read_text() == "steps\n"  # missing: copied


def test_fo15_source_inside_the_worktree_is_not_copied_onto_itself(
    fake_orca: FakeOrca, git_repo: Path, tmp_path: Path
) -> None:
    wt = add_worktree(git_repo, "issue-302", "ironbelly/issue-302")
    source = wt / ".dev/issues/302"
    source.mkdir(parents=True)
    (source / "next-steps.md").write_text("steps\n")
    fake_orca.respond("worktree-list", {"stdout": listing(main_row(git_repo), row(wt))})
    data = run_wt(fake_orca, git_repo, source)
    assert data["status"] == "reused" and data["warning"] is None
    assert sorted(p.name for p in source.iterdir()) == [
        "next-steps.md",
        "worktree.json",
    ]


def test_fo16_worktree_json_is_never_copied_and_keeps_its_launch_entry(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    wt = add_worktree(git_repo, "issue-302", "ironbelly/issue-302")
    launch = {"level": "full", "submit": False, "at": "2026-11-07T07:00:00Z"}
    (issue_dir / "worktree.json").write_text(
        json.dumps({"path": str(wt), "status": "created", "launch": launch})
    )
    fake_orca.respond("worktree-list", {"stdout": listing(main_row(git_repo), row(wt))})
    data = run_wt(fake_orca, git_repo, issue_dir)
    assert data["status"] == "reused"
    assert not (wt / ".dev/issues/302/worktree.json").exists()
    assert read_record(issue_dir) == {
        "path": str(wt),
        "status": "reused",
        "launch": launch,
    }


def test_fo17_missing_base_ref_means_no_create(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    fake_orca.respond("worktree-list", {"stdout": listing(main_row(git_repo))})
    data = run_wt(fake_orca, git_repo, issue_dir, base="origin/no-such-branch")
    assert data["status"] == "failed" and data["warning"] == "W-ORIGIN-BASE-MISSING"
    assert orca_calls(fake_orca, "worktree", "create") == []


def test_fo17_failed_fetch_with_the_ref_present_warns_and_creates(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path, tmp_path: Path
) -> None:
    git(git_repo, "remote", "set-url", "origin", str(tmp_path / "gone.git"))
    created_scene(fake_orca, git_repo)
    data = run_wt(fake_orca, git_repo, issue_dir)
    assert data["status"] == "created" and data["warning"] == "W-ORIGIN-BASE-STALE"
    assert len(orca_calls(fake_orca, "worktree", "create")) == 1


def test_fo18_exact_commands_and_no_forbidden_flag(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    wt = created_scene(fake_orca, git_repo, reply=CREATE_OK)
    fake_orca.respond(
        "terminal-list", {"stdout": terminals(terminal_row("term_plain"))}
    )
    fake_orca.respond("terminal-close", {"stdout": TAB_CLOSED})
    data = run_wt(fake_orca, git_repo, issue_dir)
    assert data["status"] == "created" and data["warning"] is None
    main = os.path.realpath(git_repo)
    assert fake_orca.calls() == [
        ["worktree", "list", "--repo", f"path:{main}", "--limit", "500", "--json"],
        [
            "worktree",
            "create",
            "--repo",
            f"path:{main}",
            "--name",
            "issue-302",
            "--base-branch",
            "origin/master",
            "--no-parent",
            "--comment",
            MARKER,
            "--json",
        ],
        ["worktree", "list", "--repo", f"path:{main}", "--limit", "500", "--json"],
        ["terminal", "list", "--worktree", f"path:{wt}", "--json"],
        ["terminal", "close", "--terminal", "term_plain", "--tab", "--json"],
    ]
    for call in fake_orca.calls():
        for arg in call:
            assert not arg.startswith(FORBIDDEN_FLAGS), arg


def tab_scene(
    fake: FakeOrca,
    git_repo: Path,
    tab_list: dict | None = None,
    tab_close: dict | None = None,
    *,
    reply: object = CREATE_OK,
) -> Path:
    """A created worktree whose Orca answers the two ``terminal`` calls.

    Before each answer the fake runs ``test -f <copied file>``: a ``terminal`` call
    made before the issue directory was copied fails and shows up as a warning.
    """
    wt = created_scene(fake, git_repo, reply=reply)
    copied = ["test", "-f", str(wt / ".dev/issues/302/issue-summary.md")]
    answer_list = tab_list or {"stdout": terminals(terminal_row())}
    fake.respond("terminal-list", {"effect": copied} | answer_list)
    fake.respond(
        "terminal-close", {"effect": copied} | (tab_close or {"stdout": TAB_CLOSED})
    )
    return wt


def left_open(data: dict, fake: FakeOrca, *, closed: bool = False) -> None:
    """The create succeeded, only W-FIRST-TAB-LEFT is reported, and no tab was closed."""
    assert data["status"] == "created"
    assert data["warning"] == "W-FIRST-TAB-LEFT"
    assert data["detail"].startswith("the plain first tab was left open: ")
    assert "also" not in data["detail"]
    assert bool(orca_calls(fake, "terminal", "close")) is closed


@pytest.mark.parametrize("identity", ["absent", None, ""])
def test_ft1_a_created_worktree_gets_its_plain_first_tab_closed_after_the_copy(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path, identity: str | None
) -> None:
    only = terminal_row("term_plain")
    if identity != "absent":
        only["agentIdentity"] = identity
    wt = tab_scene(fake_orca, git_repo, {"stdout": terminals(only)})
    data = run_wt(fake_orca, git_repo, issue_dir)
    assert data["status"] == "created" and data["warning"] is None
    calls = fake_orca.calls()
    assert [c[:2] for c in calls] == [
        ["worktree", "list"],
        ["worktree", "create"],
        ["worktree", "list"],
        ["terminal", "list"],
        ["terminal", "close"],
    ]
    assert calls[3] == ["terminal", "list", "--worktree", f"path:{wt}", "--json"]
    assert calls[4] == [
        "terminal",
        "close",
        "--terminal",
        "term_plain",
        "--tab",
        "--json",
    ]
    assert (wt / ".dev/issues/302/issue-summary.md").read_text() == "summary\n"


@pytest.mark.parametrize(
    ("field", "value"),
    [("setup", {"ran": True}), ("defaultTabs", [{"title": "dev"}])],
)
def test_ft2_a_create_that_reports_setup_or_default_tabs_closes_nothing(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path, field: str, value: object
) -> None:
    created_scene(fake_orca, git_repo, reply={"ok": True, "result": {field: value}})
    data = run_wt(fake_orca, git_repo, issue_dir)
    left_open(data, fake_orca)
    assert "setup or default tabs" in data["detail"]
    assert orca_calls(fake_orca, "terminal") == []


@pytest.mark.parametrize(
    "reply", ["not json", {"ok": False, "result": {}}, {"ok": True}, [], "null"]
)
def test_ft3_an_unknown_create_reply_never_leads_to_a_close(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path, reply: object
) -> None:
    created_scene(fake_orca, git_repo, reply=reply)
    data = run_wt(fake_orca, git_repo, issue_dir)
    left_open(data, fake_orca)
    assert orca_calls(fake_orca, "terminal") == []


def test_ft4_a_timed_out_create_closes_nothing(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    wt = tab_scene(fake_orca, git_repo)
    cmd = [
        "git", "-C", str(git_repo), "worktree", "add", "-b", "ironbelly/issue-302",
        str(wt), "origin/master",
    ]  # fmt: skip
    fake_orca.respond("worktree-create", {"effect": cmd, "sleep": 30})
    data = run_wt(fake_orca, git_repo, issue_dir, SC_ORCA_TIMEOUT="3")
    left_open(data, fake_orca)
    assert orca_calls(fake_orca, "terminal") == []


def test_ft5_a_failed_terminal_list_leaves_the_tab_and_names_the_reason(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    tab_scene(fake_orca, git_repo, {"rc": 1, "stderr": "boom\n"})
    data = run_wt(fake_orca, git_repo, issue_dir)
    left_open(data, fake_orca)
    assert "boom" in data["detail"]


@pytest.mark.parametrize(
    "payload",
    [
        "garbage",
        {"ok": True, "result": {}},
        {"ok": True, "result": {"terminals": "x"}},
        {"ok": True, "result": {"terminals": ["x"]}},
        {"ok": False, "result": {"terminals": []}},
    ],
)
def test_ft6_a_malformed_terminal_list_reply_leaves_the_tab(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path, payload: object
) -> None:
    tab_scene(fake_orca, git_repo, {"stdout": payload})
    data = run_wt(fake_orca, git_repo, issue_dir)
    left_open(data, fake_orca)


@pytest.mark.parametrize(
    ("rows", "why"),
    [
        ([], "0 terminals"),
        ([terminal_row("a"), terminal_row("b")], "2 terminals"),
        ([terminal_row("a", agentIdentity="claude")], "runs an agent"),
        ([terminal_row("")], "no handle"),
    ],
)
def test_ft7_only_exactly_one_plain_terminal_is_closed(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path, rows: list, why: str
) -> None:
    tab_scene(fake_orca, git_repo, {"stdout": terminals(*rows)})
    data = run_wt(fake_orca, git_repo, issue_dir)
    left_open(data, fake_orca)
    assert why in data["detail"]


def test_ft8_a_failed_close_is_a_warning_and_the_status_stays_created(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    tab_scene(fake_orca, git_repo, None, {"rc": 1, "stderr": "nope\n"})
    data = run_wt(fake_orca, git_repo, issue_dir)
    left_open(data, fake_orca, closed=True)
    assert "nope" in data["detail"]
    assert read_record(issue_dir)["status"] == "created"


def test_ft9_a_failed_copy_closes_nothing_and_keeps_its_own_warning(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path, tmp_path: Path
) -> None:
    tab_scene(fake_orca, git_repo)
    data = run_wt(fake_orca, git_repo, tmp_path / "no-such-claim-dir")
    assert data["status"] == "failed" and data["warning"] == "W-WORKTREE-COPY-FAILED"
    assert orca_calls(fake_orca, "terminal") == []


def test_ft10_a_new_row_of_another_repository_is_failed_with_no_terminal_call(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    wt = created_scene(fake_orca, git_repo, effect=False, reply=CREATE_OK)
    fake_orca.respond(
        "worktree-create",
        {"stdout": CREATE_OK, "effect": ["git", "init", "-b", "master", str(wt)]},
    )
    data = run_wt(fake_orca, git_repo, issue_dir)
    assert data["status"] == "failed" and data["warning"] == "W-WORKTREE-STALE"
    assert orca_calls(fake_orca, "terminal") == []


def test_ft11_a_reused_worktree_makes_no_terminal_call(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    wt = add_worktree(git_repo, "issue-302", "ironbelly/issue-302")
    fake_orca.respond(
        "worktree-list",
        {"stdout": listing(main_row(git_repo), row(wt, comment=MARKER))},
    )
    fake_orca.respond("terminal-list", {"stdout": terminals(terminal_row())})
    data = run_wt(fake_orca, git_repo, issue_dir)
    assert data["status"] == "reused" and data["warning"] is None
    assert orca_calls(fake_orca, "terminal") == []
    assert orca_calls(fake_orca, "worktree", "create") == []


def test_ft12_the_tab_warning_ranks_below_a_copy_warning_and_never_raises(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path, tmp_path: Path
) -> None:
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    (issue_dir / "linked").symlink_to(elsewhere, target_is_directory=True)
    tab_scene(fake_orca, git_repo, {"rc": 1, "stderr": "boom\n"})
    data = run_wt(fake_orca, git_repo, issue_dir)
    assert data["status"] == "created"
    assert data["warning"] == "W-WORKTREE-COPY-FAILED"
    assert "also W-FIRST-TAB-LEFT" in data["detail"]


def test_arg1_worktree_bad_arguments_exit_2(
    fake_orca: FakeOrca, issue_dir: Path
) -> None:
    good = ["--repo", REPO, "--number", "302", "--base", "origin/master"]
    good += ["--source", str(issue_dir)]
    env = fake_orca.env()
    assert run_script("worktree", env=env).returncode == 2
    for flag in ("--repo", "--number", "--base", "--source"):
        i = good.index(flag)
        assert (
            run_script("worktree", *good[:i], *good[i + 2 :], env=env).returncode == 2
        )
    bad = {"--repo": "no-slash", "--number": "abc", "--base": "master"}
    for flag, value in bad.items():
        args = list(good)
        args[args.index(flag) + 1] = value
        assert run_script("worktree", *args, env=env).returncode == 2
    assert fake_orca.calls() == []


# --- prompt ------------------------------------------------------------------

TEMPLATE = SCRIPT.parents[1] / "templates" / "launch-prompt.md"
PR_TOKENS = ("/sc:pr-submit", "git push", "git commit", "--monitor")
PROMPT_NOT_RUN = (
    "Do not run `/sc:implement`, `/task`, `git commit`, `git push` or `/sc:pr-submit`."
)


def render(
    tmp_path: Path, level: str, *, submit: bool = False, template: Path = TEMPLATE
) -> tuple[subprocess.CompletedProcess[str], Path]:
    out = tmp_path / f"launch-prompt-{level}-{submit}.md"
    args = ["prompt", "--template", str(template), "--level", level]
    args += ["--number", "302", "--repo", REPO, "--out", str(out)]
    if submit:
        args.append("--submit")
    return run_script(*args, env=dict(os.environ)), out


def test_pr1_prompt_levels_keep_only_their_own_block(tmp_path: Path) -> None:
    worktree_proc, worktree_out = render(tmp_path, "worktree")
    full_proc, full_out = render(tmp_path, "full")
    for proc, out in ((worktree_proc, worktree_out), (full_proc, full_out)):
        assert proc.returncode == 0, proc.stderr
        assert json.loads(proc.stdout) == {"status": "written", "path": str(out)}
        text = out.read_text()
        assert "<!--" not in text and "block:" not in text
        assert "<N>" not in text and ".dev/issues/302/next-steps.md" in text
        assert "Never merge anything" in text  # the common block
    worktree, full = worktree_out.read_text(), full_out.read_text()
    assert "Level: worktree." in worktree and "Level: full." not in worktree
    assert "Level: full." in full and "Level: worktree." not in full
    assert "Waiting for approval" in worktree and "Waiting for approval" not in full
    assert "owner asked for the commit" not in worktree + full


def test_pr2_prompt_submit_adds_the_submit_block(tmp_path: Path) -> None:
    proc, out = render(tmp_path, "full", submit=True)
    assert proc.returncode == 0, proc.stderr
    text = out.read_text()
    assert "Level: full." in text and "owner asked for the commit" in text
    assert "/sc:pr-submit --monitor 3" in text
    assert text.index("Level: full.") < text.index("owner asked for the commit")
    plain = render(tmp_path, "full")[1].read_text()
    assert text.startswith(plain.rstrip("\n"))


def test_pr3_prompt_submit_with_worktree_level_is_a_bad_argument(
    tmp_path: Path,
) -> None:
    proc, out = render(tmp_path, "worktree", submit=True)
    assert proc.returncode == 2
    assert not out.exists()


def test_pr4_prompt_no_pr_tokens_outside_the_worktree_prohibition_and_submit(
    tmp_path: Path,
) -> None:
    full = render(tmp_path, "full")[1].read_text()
    worktree = render(tmp_path, "worktree")[1].read_text()
    for token in PR_TOKENS:
        assert token not in full, token
    assert PROMPT_NOT_RUN in worktree
    assert "--monitor" not in worktree
    common = worktree.split("Level: worktree.", 1)[0]
    for token in PR_TOKENS:
        assert token not in common, token


def test_prompt_unusable_template_is_reported_not_raised(tmp_path: Path) -> None:
    proc, out = render(tmp_path, "full", template=tmp_path / "missing.md")
    data = json.loads(proc.stdout)
    assert proc.returncode == 0 and data["status"] == "failed" and data["detail"]
    assert not out.exists()
    short = tmp_path / "short.md"
    short.write_text("<!-- block:common -->\nonly the common block\n")
    proc, out = render(tmp_path, "full", template=short)
    assert json.loads(proc.stdout)["status"] == "failed"
    assert "full" in json.loads(proc.stdout)["detail"] and not out.exists()


def test_arg1_prompt_bad_arguments_exit_2(tmp_path: Path) -> None:
    env = dict(os.environ)
    good = ["--template", str(TEMPLATE), "--level", "full", "--number", "302"]
    good += ["--repo", REPO, "--out", str(tmp_path / "x.md")]
    assert run_script("prompt", env=env).returncode == 2
    for flag in ("--template", "--level", "--number", "--repo", "--out"):
        i = good.index(flag)
        assert run_script("prompt", *good[:i], *good[i + 2 :], env=env).returncode == 2
    for flag, value in {
        "--level": "none",
        "--number": "0",
        "--repo": "no-slash",
    }.items():
        args = list(good)
        args[args.index(flag) + 1] = value
        assert run_script("prompt", *args, env=env).returncode == 2
    assert not (tmp_path / "x.md").exists()


def test_pr425_prompt_renders_the_origin_repo_into_the_submit_block(
    tmp_path: Path,
) -> None:
    out = tmp_path / "p.md"
    args = ["prompt", "--template", str(TEMPLATE), "--level", "full", "--submit"]
    args += ["--number", "302", "--repo", "Acme/Widgets", "--out", str(out)]
    assert (
        json.loads(run_script(*args, env=dict(os.environ)).stdout)["status"]
        == "written"
    )
    text = out.read_text()
    assert "gh pr list --repo Acme/Widgets --head <branch> --state all" in text
    assert "<R>" not in text and "IronbellyOrg" not in text


def test_pr425_full_level_forbids_commit_push_and_pr_without_the_pinned_tokens(
    tmp_path: Path,
) -> None:
    full = render(tmp_path, "full")[1].read_text()
    assert "Make no commit" in full and "open no pull request" in full
    for token in PR_TOKENS:
        assert token not in full, token


# --- launch ------------------------------------------------------------------

LAUNCH_OK = {"ok": True, "result": {"terminal": {"handle": "term_abc"}}}
SCREEN_OK = {
    "ok": True,
    "result": {"terminal": {"handle": "term_abc", "tail": "[ccsession] shim up"}},
}
SCREEN_QUESTION = {
    "ok": True,
    "result": {
        "terminal": {
            "handle": "term_abc",
            "tail": "Session name (Enter or Ctrl+C = untagged; untagged after 30s):",
        }
    },
}
SCREEN_PLAIN = {
    "ok": True,
    "result": {"terminal": {"handle": "term_abc", "tail": "claude> welcome"}},
}
PROMPT_RE = re.compile(
    r"^\[sc-launch:v1:([0-9a-f]{32})\] Read \.dev/issues/302/launch-prompt\.md "
    r"and follow it\.$"
)


def launch_scene(
    fake: FakeOrca, git_repo: Path, issue_dir: Path, *, hook: str | None = "exec"
) -> Path:
    """A real worktree with a guarded record, an Orca that launches and the guard.

    ``hook="exec"`` installs what the IR-4 preflight needs: the versioned,
    executable guard and a user settings.json holding the shipped hooks.json
    registrations (both guard entries and the identity entry). ``"plain"`` is
    the same without the executable bit; ``None`` creates nothing in HOME.
    """
    wt = add_worktree(git_repo, "issue-302", "ironbelly/issue-302")
    (issue_dir / "worktree.json").write_text(
        json.dumps({"path": str(wt), "status": "created"})
    )
    # the prompt rendered for this claim, already present in the worktree
    (issue_dir / "launch-prompt.md").write_text("the rendered prompt\n")
    (wt / ".dev/issues/302").mkdir(parents=True, exist_ok=True)
    (wt / ".dev/issues/302/launch-prompt.md").write_text("the rendered prompt\n")
    fake.respond("agent-launch", {"stdout": LAUNCH_OK})
    fake.respond("terminal-read", {"stdout": SCREEN_OK})
    if hook:
        script = fake.home / ".claude" / "hooks" / "launch-level-guard.sh"
        script.parent.mkdir(parents=True)
        script.write_text("#!/bin/sh\n# launch-level-guard-version: 1\n")
        script.chmod(0o755 if hook == "exec" else 0o644)
        user_settings(fake).write_text(HOOKS_JSON.read_text())
    return wt


HOOKS_JSON = REPO_ROOT / "src/superclaude/hooks/hooks.json"
GUARD = "~/.claude/hooks/launch-level-guard.sh"
IDENTITY = "~/.claude/hooks/launch-job-identity.sh"


def user_settings(fake: FakeOrca) -> Path:
    return fake.home / ".claude" / "settings.json"


def run_launch(
    fake: FakeOrca,
    git_repo: Path,
    source: Path,
    level: str = "full",
    *,
    submit: bool = False,
    **env: str,
) -> dict:
    args = ["launch", "--number", str(NUMBER), "--source", str(source)]
    args += ["--level", level] + (["--submit"] if submit else [])
    return run_json(*args, env=fake.env(SC_ORCA_SHIM_INTERVAL="0", **env), cwd=git_repo)


def pending_dir(fake: FakeOrca) -> Path:
    return fake.home / ".claude/state/launch-level/pending"


def launch_calls(fake: FakeOrca) -> list[list[str]]:
    return orca_calls(fake, "agent", "launch")


def tree_listing(root: Path) -> list[str]:
    return sorted(
        str(p.relative_to(root))
        for p in root.rglob("*")
        if ".git" not in p.relative_to(root).parts
    )


def test_la1_launch_argument_list_is_exact(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    wt = launch_scene(fake_orca, git_repo, issue_dir)
    data = run_launch(fake_orca, git_repo, issue_dir)
    assert data["status"] == "launched" and data["terminal"] == "term_abc"
    (argv,) = launch_calls(fake_orca)
    assert argv[:7] == [
        "agent",
        "launch",
        "--agent",
        "claude",
        "--worktree",
        f"path:{wt}",
        "--surface",
    ]
    assert argv[7] == "terminal" and argv[8] == "--prompt" and argv[10] == "--json"
    assert len(argv) == 11
    assert PROMPT_RE.match(argv[9]) and not argv[9].startswith("/")
    flags = {a for a in argv if a.startswith("--")}
    assert flags == {"--agent", "--worktree", "--surface", "--prompt", "--json"}
    for arg in argv:
        # Whole tokens only: "--prompt" must not trip the "--pr" link flag.
        assert arg not in ("--issue", "--pr", "--linear-issue"), arg
        assert not arg.startswith(("--reference", "--gitlab")), arg
        assert arg not in ("--model", "--effort")


@pytest.mark.parametrize(
    ("level", "submit", "word"),
    [
        ("worktree", False, "worktree"),
        ("full", False, "full"),
        ("full", True, "full-submit"),
    ],
)
def test_la2_launch_record_is_private_and_published_before_the_launch(
    fake_orca: FakeOrca,
    git_repo: Path,
    issue_dir: Path,
    level: str,
    submit: bool,
    word: str,
) -> None:
    launch_scene(fake_orca, git_repo, issue_dir)
    run_launch(fake_orca, git_repo, issue_dir, level, submit=submit)
    (argv,) = launch_calls(fake_orca)
    nonce = PROMPT_RE.match(argv[9]).group(1)
    record = pending_dir(fake_orca) / nonce
    assert record.is_file() and not record.is_symlink()
    assert stat.S_IMODE(record.stat().st_mode) == 0o600
    assert record.read_text() == word
    for part in ("state", "state/launch-level", "state/launch-level/pending"):
        mode = stat.S_IMODE((fake_orca.home / ".claude" / part).stat().st_mode)
        assert mode == 0o700, part
    launch_call = next(c for c in fake_orca.pending_at_calls() if "launch" in c["argv"])
    assert launch_call["pending"] == [nonce]  # already published when orca ran
    assert sorted(p.name for p in pending_dir(fake_orca).iterdir()) == [nonce]


def test_la2_launch_nonce_is_fresh_for_every_launch(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    wt = launch_scene(fake_orca, git_repo, issue_dir)
    first = run_launch(fake_orca, git_repo, issue_dir)
    (first_nonce,) = [p.name for p in pending_dir(fake_orca).iterdir()]
    # IR-5: with the launch entry in place a re-claim launches nothing and
    # writes no new pending record.
    again = run_launch(fake_orca, git_repo, issue_dir)
    assert again["status"] == "already_launched"
    assert len(launch_calls(fake_orca)) == 1
    assert [p.name for p in pending_dir(fake_orca).iterdir()] == [first_nonce]
    record = json.loads((issue_dir / "worktree.json").read_text())
    del record["launch"]
    (issue_dir / "worktree.json").write_text(json.dumps(record))
    # Launching again means clearing the entry in both files; the detail names them.
    mirror = (
        Path(git(wt, "rev-parse", "--absolute-git-dir")) / "sc-issue-launch-302.json"
    )
    blocked = run_launch(fake_orca, git_repo, issue_dir)
    assert blocked["status"] == "already_launched"
    assert (
        str(mirror) in blocked["detail"]
        and str(issue_dir / "worktree.json") in blocked["detail"]
    )
    assert first["status"] == "launched"
    assert len(list(pending_dir(fake_orca).iterdir())) == 1
    mirror.unlink()
    # Removed from both the record and the git-dir mirror: a new launch with a
    # new nonce, never a resumed earlier session.
    assert run_launch(fake_orca, git_repo, issue_dir)["status"] == "launched"
    calls = launch_calls(fake_orca)
    nonces = [PROMPT_RE.match(c[9]).group(1) for c in calls]
    assert len(calls) == 2 and nonces[0] == first_nonce != nonces[1]
    assert sorted(p.name for p in pending_dir(fake_orca).iterdir()) == sorted(nonces)
    assert not any("--resume" in arg or "--continue" in arg for c in calls for arg in c)


@pytest.mark.parametrize(
    "answer",
    [
        {"stdout": "", "stderr": "agent crashed\nmore\n", "rc": 4},
        {"stdout": {"ok": False}},
        {"stdout": "not json"},
        {"sleep": 30},
    ],
    ids=["nonzero", "ok-false", "not-json", "timeout"],
)
def test_la3_launch_failure_removes_the_record_and_prints_a_hand_command(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path, answer: dict
) -> None:
    wt = launch_scene(fake_orca, git_repo, issue_dir)
    fake_orca.respond("agent-launch", answer)
    data = run_launch(fake_orca, git_repo, issue_dir, SC_ORCA_TIMEOUT="1")
    assert data["status"] == "failed" and data["warning"] == "W-LAUNCH-FAILED"
    assert list(pending_dir(fake_orca).iterdir()) == []
    assert f"path:{wt}" in data["hand_command"]
    assert "sc-launch" not in data["hand_command"]
    assert "not governed by the launch-level hook" in data["hand_command"]
    assert "launch" not in json.loads((issue_dir / "worktree.json").read_text())
    if "sleep" in answer:
        assert "check Orca" in data["detail"]
    if answer.get("rc"):
        assert "agent crashed" in data["detail"]


def test_la3_launch_with_an_unwritable_record_store_makes_no_launch_call(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    launch_scene(fake_orca, git_repo, issue_dir)  # the IR-4 preflight passes
    (fake_orca.home / ".claude/state").write_text("a file where the store should be\n")
    data = run_launch(fake_orca, git_repo, issue_dir)
    assert data["status"] == "failed" and data["warning"] == "W-LAUNCH-FAILED"
    assert "launch record" in data["detail"]
    assert fake_orca.calls() == []


def test_la4_launch_entry_gives_already_launched_without_any_orca_call(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    wt = launch_scene(fake_orca, git_repo, issue_dir, hook=None)
    entry = {"level": "full", "submit": False, "at": "2026-11-07T07:00:00Z"}
    (issue_dir / "worktree.json").write_text(
        json.dumps({"path": str(wt), "status": "created", "launch": entry})
    )
    data = run_launch(fake_orca, git_repo, issue_dir)
    assert data["status"] == "already_launched"
    assert data["launched_at"] == "2026-11-07T07:00:00Z"
    assert data["enforcement_hook"] is None and data["warning"] is None
    assert fake_orca.calls() == []
    assert not (fake_orca.home / ".claude").exists()


@pytest.mark.skipif(os.geteuid() == 0, reason="root can write to a read-only directory")
def test_la4_launch_record_update_failure_never_says_to_rerun_the_claim(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    launch_scene(fake_orca, git_repo, issue_dir)
    issue_dir.chmod(0o500)  # the record can be read but not rewritten
    try:
        data = run_launch(fake_orca, git_repo, issue_dir)
    finally:
        issue_dir.chmod(0o755)
    # IR-7: the scene's worktree has no pre-push hook, so W-L2-ABSENT is the warning.
    assert data["status"] == "launched" and data["warning"] == "W-L2-ABSENT"
    assert data["launched_at"] and data["terminal"] == "term_abc"
    assert "the agent is running" in data["detail"]
    assert "do not re-run the claim" in data["detail"]
    assert "re-run the claim; the hand command" not in data["detail"]
    assert len(launch_calls(fake_orca)) == 1


def test_la4_launch_entry_is_written_even_when_the_shim_check_fails(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    wt = launch_scene(fake_orca, git_repo, issue_dir)
    fake_orca.respond("terminal-read", {"stdout": SCREEN_PLAIN})
    data = run_launch(fake_orca, git_repo, issue_dir, "worktree")
    assert data["status"] == "launched" and data["warning"] == "W-LAUNCH-NOT-CCSESSION"
    record = json.loads((issue_dir / "worktree.json").read_text())
    assert record["path"] == str(wt) and record["status"] == "created"
    assert set(record["launch"]) == {"level", "submit", "at"}
    assert (
        record["launch"]["level"] == "worktree" and record["launch"]["submit"] is False
    )
    assert re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", record["launch"]["at"])
    assert data["launched_at"] == record["launch"]["at"]
    assert len(list(pending_dir(fake_orca).iterdir())) == 1  # the record stays
    again = run_launch(fake_orca, git_repo, issue_dir, "worktree")
    assert again["status"] == "already_launched"
    assert len(launch_calls(fake_orca)) == 1


@pytest.mark.parametrize(
    "screen", [SCREEN_OK, SCREEN_QUESTION], ids=["tag", "question"]
)
def test_la5_launch_shim_check_passes_on_either_text(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path, screen: dict
) -> None:
    launch_scene(fake_orca, git_repo, issue_dir)
    fake_orca.respond("terminal-read", {"stdout": screen})
    data = run_launch(fake_orca, git_repo, issue_dir)
    assert data["status"] == "launched" and data["warning"] == "W-L2-ABSENT"
    assert orca_calls(fake_orca, "terminal", "read") == [
        ["terminal", "read", "--terminal", "term_abc", "--screen", "--json"]
    ]


def test_la5_launch_shim_check_retries_up_to_five_times(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    launch_scene(fake_orca, git_repo, issue_dir)
    plain = {"stdout": SCREEN_PLAIN}
    fake_orca.respond("terminal-read", plain, plain, {"stdout": SCREEN_OK})
    assert run_launch(fake_orca, git_repo, issue_dir)["warning"] == "W-L2-ABSENT"
    assert len(orca_calls(fake_orca, "terminal", "read")) == 3


def show_title(title: object) -> dict:
    return {"stdout": {"ok": True, "result": {"terminal": {"title": title}}}}


def test_la5_launch_shim_check_passes_on_the_session_name_in_the_tab_title(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    """The shim's screen text can be gone in 2 seconds; its session name stays."""
    launch_scene(fake_orca, git_repo, issue_dir)
    fake_orca.respond("terminal-read", {"stdout": SCREEN_PLAIN})
    # a title copied from a live launch (issue 452, 2026-11-08)
    title = "issue-452-sc-launch-v1-904e19fa400a-1108-073544-5732 · Claude Code"
    fake_orca.respond("terminal-show", show_title(title))
    data = run_launch(fake_orca, git_repo, issue_dir)
    assert data["status"] == "launched" and data["warning"] == "W-L2-ABSENT"
    assert len(orca_calls(fake_orca, "terminal", "read")) == 1
    assert orca_calls(fake_orca, "terminal", "show") == [
        ["terminal", "show", "--terminal", "term_abc", "--json"]
    ]


@pytest.mark.parametrize(
    "title",
    [
        "CoderOrchestrator · Claude Code",
        "issue-452 · Claude Code",
        "issue-452-sc-launch-v1-904e19fa400a · Claude Code",
        "sc-launch-v1-xyz-1108-073544-5732",
        "my-sc-launch-v1-904e19fa-1108-073544-57320 · Claude Code",
        None,
        42,
    ],
    ids=[
        "other",
        "no-stamp",
        "no-clock",
        "nonce-not-hex",
        "stamp-too-long",
        "none",
        "int",
    ],
)
def test_la5_launch_shim_check_ignores_a_title_that_is_not_ccsessions(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path, title: object
) -> None:
    launch_scene(fake_orca, git_repo, issue_dir)
    fake_orca.respond("terminal-read", {"stdout": SCREEN_PLAIN})
    fake_orca.respond("terminal-show", show_title(title))
    data = run_launch(fake_orca, git_repo, issue_dir)
    assert data["warning"] == "W-LAUNCH-NOT-CCSESSION"
    assert len(orca_calls(fake_orca, "terminal", "read")) == 5
    assert len(orca_calls(fake_orca, "terminal", "show")) == 5


def test_la5_launch_shim_check_title_may_appear_on_a_later_try(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    launch_scene(fake_orca, git_repo, issue_dir)
    fake_orca.respond("terminal-read", {"stdout": SCREEN_PLAIN})
    fake_orca.respond(
        "terminal-show",
        show_title("Claude Code"),
        show_title("Claude Code"),
        show_title("x-sc-launch-v1-0a1b2c3d4e5f-1108-073544-5a5a · Claude Code"),
    )
    assert run_launch(fake_orca, git_repo, issue_dir)["warning"] == "W-L2-ABSENT"
    assert len(orca_calls(fake_orca, "terminal", "read")) == 3


@pytest.mark.parametrize(
    ("answer", "reads"),
    [
        ({"stdout": SCREEN_PLAIN}, 5),
        ({"stdout": "", "stderr": "no such terminal\n", "rc": 1}, 5),
        ({"stdout": {"ok": True, "result": {}}}, 5),
    ],
    ids=["no-match", "unreadable", "no-tail"],
)
def test_la5_launch_shim_check_failure_keeps_the_launch_and_warns(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path, answer: dict, reads: int
) -> None:
    launch_scene(fake_orca, git_repo, issue_dir)
    fake_orca.respond("terminal-read", answer)
    data = run_launch(fake_orca, git_repo, issue_dir)
    assert data["status"] == "launched"
    assert data["warning"] == "W-LAUNCH-NOT-CCSESSION" and "close it" in data["detail"]
    assert "; also W-L2-ABSENT: " in data["detail"]  # the ccsession warning stays first
    assert len(orca_calls(fake_orca, "terminal", "read")) == reads


def test_la5_launch_without_a_terminal_handle_warns_and_reads_nothing(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    launch_scene(fake_orca, git_repo, issue_dir)
    fake_orca.respond("agent-launch", {"stdout": {"ok": True, "result": {"id": 1}}})
    data = run_launch(fake_orca, git_repo, issue_dir)
    assert data["status"] == "launched" and data["terminal"] is None
    assert data["warning"] == "W-LAUNCH-NOT-CCSESSION"
    assert orca_calls(fake_orca, "terminal", "read") == []
    assert "launch" in json.loads((issue_dir / "worktree.json").read_text())


def test_la5_launch_handle_is_found_anywhere_in_the_result(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    launch_scene(fake_orca, git_repo, issue_dir)
    nested = {
        "ok": True,
        "result": {"agent": {"sessions": [{"x": 1, "handle": "term_deep"}]}},
    }
    fake_orca.respond("agent-launch", {"stdout": nested})
    assert run_launch(fake_orca, git_repo, issue_dir)["terminal"] == "term_deep"
    assert orca_calls(fake_orca, "terminal", "read")[0][3] == "term_deep"


def assert_refused(fake: FakeOrca, data: dict, *names: str) -> None:
    """An IR-4 refusal: no agent, no launch record, and the condition is named."""
    assert data["status"] == "failed" and data["warning"] == "W-ENFORCEMENT-ABSENT"
    assert data["enforcement_hook"] == "missing" and data["hand_command"] is None
    assert data["terminal"] is None and data["launched_at"] is None
    assert "verified the claim process only" in data["detail"]
    assert "superclaude install" in data["detail"]  # the REMEDY text
    for name in names:
        assert name in data["detail"], (name, data["detail"])
    assert launch_calls(fake) == [] and orca_calls(fake, "terminal", "read") == []
    assert not (fake.home / ".claude/state").exists()  # so no pending/<nonce>


@pytest.mark.parametrize("hook", [None, "plain"], ids=["absent", "not-executable"])
def test_la6_launch_without_an_executable_hook_is_refused(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path, hook: str | None
) -> None:
    launch_scene(fake_orca, git_repo, issue_dir, hook=hook)
    data = run_launch(fake_orca, git_repo, issue_dir)
    assert_refused(
        fake_orca, data, "not installed" if hook is None else "not executable"
    )
    assert "launch" not in json.loads((issue_dir / "worktree.json").read_text())


@pytest.mark.parametrize(
    "env",
    [{}, {"CLAUDE_CONFIG_DIR": "same"}],
    ids=["default", "config-dir-same"],
)
def test_la6_launch_with_the_hook_installed_has_only_the_l2_warning(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path, env: dict
) -> None:
    launch_scene(fake_orca, git_repo, issue_dir)
    if env:
        env = {"CLAUDE_CONFIG_DIR": str(fake_orca.home / ".claude") + "/"}
    before = user_settings(fake_orca).read_bytes()
    data = run_launch(fake_orca, git_repo, issue_dir, **env)
    assert data["status"] == "launched"
    assert data["enforcement_hook"] == "installed"
    assert data["warning"] == "W-L2-ABSENT"  # the scene has no pre-push hook
    assert len(launch_calls(fake_orca)) == 1
    assert user_settings(fake_orca).read_bytes() == before


def test_la6_launch_refusal_comes_before_any_shim_check(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    launch_scene(fake_orca, git_repo, issue_dir, hook=None)
    fake_orca.respond("terminal-read", {"stdout": SCREEN_PLAIN})
    data = run_launch(fake_orca, git_repo, issue_dir)
    assert_refused(fake_orca, data)
    assert "W-LAUNCH-NOT-CCSESSION" not in data["detail"]


# --- IR-6: release instructions and layer status ------------------------------


def test_ir6_launched_result_states_the_release_and_both_layers(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    launch_scene(fake_orca, git_repo, issue_dir)
    data = run_launch(fake_orca, git_repo, issue_dir)
    assert data["status"] == "launched"
    store = fake_orca.home / ".claude/state/launch-level"
    release = data["release"]
    assert f'rm "{store}/sessions/<session id>" "{store}/sessions/<session id>.ok"' in (
        release
    )
    # The id is not printed by an ordinary block message (only LL-TAMPER names it),
    # so the instruction says where to find it instead.
    assert "own terminal" in release and "'Launch-level guard' block" not in release
    # The claim hands out the inode number of its own record: the guard binds the
    # session file as a hard link of it, so `ls -i` picks this launch's file out.
    (record,) = (store / "pending").iterdir()
    inode = record.stat().st_ino
    assert "named by a session id" in release and "ls -i" in release
    assert f"inode number {inode}" in release and f"whose number is {inode}" in release
    assert "newest" not in release and "exact rm command" in release
    l1, l2 = data["layers"]
    assert l1.startswith("L1 guard: effective")
    assert l2.startswith("L2 pre-push: absent")  # git init makes only *.sample hooks
    # Not launched: neither field is set.
    again = run_launch(fake_orca, git_repo, issue_dir)
    assert again["status"] == "already_launched"
    assert again["release"] is None and again["layers"] is None
    wave8, final = (
        (SCRIPT.parents[1] / "refs/claim.md").read_text().split("## Final output")
    )
    assert "sessions/<session id>.ok" in wave8 and "present-unverified" in wave8
    for text in ("`release`", "`layers`", "L1 guard", "L2 pre-push"):
        assert text in final, text


def test_ir6_refused_launch_has_no_release_or_layers(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    launch_scene(fake_orca, git_repo, issue_dir, hook=None)
    data = run_launch(fake_orca, git_repo, issue_dir)
    assert_refused(fake_orca, data)
    assert data["release"] is None and data["layers"] is None


@pytest.mark.parametrize(
    ("case", "expected"),
    [
        ("no-file", "absent"),
        ("not-executable", "absent"),
        ("foreign-executable", "present-unverified"),
        ("hooks-path", "present-unverified"),
        ("hooks-path-elsewhere", "absent"),
    ],
)
def test_ir6_l2_status_follows_the_git_hook_path(
    fake_orca: FakeOrca,
    git_repo: Path,
    issue_dir: Path,
    tmp_path: Path,
    case: str,
    expected: str,
) -> None:
    # The scene's worktree is a linked worktree: git keeps its hooks in the
    # main checkout's common directory, or in core.hooksPath when set.
    launch_scene(fake_orca, git_repo, issue_dir)
    default = git_repo / ".git/hooks/pre-push"
    elsewhere = tmp_path / "hooks-elsewhere"
    elsewhere.mkdir()
    hook = {
        "no-file": None,
        "not-executable": default,
        "foreign-executable": default,
        "hooks-path": elsewhere / "pre-push",
        "hooks-path-elsewhere": default,
    }[case]
    if case.startswith("hooks-path"):
        git(git_repo, "config", "core.hooksPath", str(elsewhere))
    if hook:
        hook.write_text("#!/bin/sh\n# someone else's hook\nexit 0\n")
        hook.chmod(0o644 if case == "not-executable" else 0o755)
        before = (hook.read_bytes(), hook.stat().st_mode)
    data = run_launch(fake_orca, git_repo, issue_dir)
    assert data["status"] == "launched"
    assert data["layers"][1].startswith(f"L2 pre-push: {expected} ")
    # IR-7: W-L2-ABSENT exactly when the L2 line says absent.
    assert (data["warning"] == "W-L2-ABSENT") is (expected == "absent")
    assert ("L2 layer is not built yet" in data["detail"]) is (expected == "absent")
    if hook:  # never modified, never adopted
        assert (hook.read_bytes(), hook.stat().st_mode) == before


# --- IR-7: a missing L2 layer is a warning, not a refusal ---------------------


def test_ir7_l2_absent_warns_and_the_launch_proceeds(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    launch_scene(fake_orca, git_repo, issue_dir)
    hooks = git_repo / ".git/hooks"
    before = {p.name: p.read_bytes() for p in hooks.iterdir()}
    data = run_launch(fake_orca, git_repo, issue_dir)
    assert data["status"] == "launched" and data["warning"] == "W-L2-ABSENT"
    assert data["enforcement_hook"] == "installed"
    assert "no executable pre-push hook" in data["detail"]
    assert "the L2 layer is not built yet" in data["detail"]
    assert "enforced by the L1 guard only" in data["detail"]
    assert data["layers"][1].startswith("L2 pre-push: absent ")
    (argv,) = launch_calls(fake_orca)
    nonce = PROMPT_RE.match(argv[9]).group(1)
    assert [p.name for p in pending_dir(fake_orca).iterdir()] == [nonce]
    assert "launch" in json.loads((issue_dir / "worktree.json").read_text())
    # No hook file is created, adopted or changed.
    assert {p.name: p.read_bytes() for p in hooks.iterdir()} == before


# --- IR-4 preflight: one refusal per failing condition ------------------------


def edit_settings(path: Path, change) -> None:
    data = json.loads(path.read_text()) if path.exists() else {}
    change(data)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))


def drop(event: str, command: str):
    def change(data: dict) -> None:
        data["hooks"][event] = [
            g
            for g in data["hooks"][event]
            if not any(h["command"] == command for h in g["hooks"])
        ]

    return change


def set_matcher(event: str, command: str, matcher: str):
    def change(data: dict) -> None:
        for group in data["hooks"][event]:
            if any(h["command"] == command for h in group["hooks"]):
                group["matcher"] = matcher

    return change


def disable_hooks(data: dict) -> None:
    data["disableAllHooks"] = True


def guard_script(fake: FakeOrca) -> Path:
    return fake.home / ".claude/hooks/launch-level-guard.sh"


# Each case: what to break (given the fake and the worktree; returns extra env)
# and the text the refusal must contain to name that condition.
IR4_CASES = {
    "no-jq": (
        lambda f, wt: {"PATH": f.path_without("jq")},
        ["jq is not on PATH"],
    ),
    "no-uv": (
        lambda f, wt: {"PATH": f.path_without("uv")},
        ["uv is not on PATH"],
    ),
    "script-not-executable": (
        lambda f, wt: guard_script(f).chmod(0o644),
        ["not executable", "superclaude install --force"],
    ),
    "wrong-version-line": (
        lambda f, wt: guard_script(f).write_text(
            "#!/bin/sh\n# launch-level-guard-version: 0\n"
        ),
        ["launch-level-guard-version: 1", "stale", "superclaude install --force"],
    ),
    "no-user-prompt-registration": (
        lambda f, wt: edit_settings(user_settings(f), drop("UserPromptSubmit", GUARD)),
        [f"no UserPromptSubmit registration of {GUARD}"],
    ),
    "no-pretooluse-registration": (
        lambda f, wt: edit_settings(user_settings(f), drop("PreToolUse", GUARD)),
        [f"no PreToolUse registration of {GUARD}"],
    ),
    "matcher-excludes-governed-tools": (
        lambda f, wt: edit_settings(
            user_settings(f), set_matcher("PreToolUse", GUARD, "^(Bash|Edit|Write)$")
        ),
        ["does not fire for Skill, Agent, Task", "ScheduleWakeup"],
    ),
    # The design matcher minus its mcp__ branch: the plain tools fire, the
    # GitHub write tools of an MCP server do not.
    "matcher-without-mcp-branch": (
        lambda f, wt: edit_settings(
            user_settings(f),
            set_matcher(
                "PreToolUse",
                GUARD,
                "^(Bash|Skill|Agent|Task|Edit|Write|NotebookEdit|Monitor|Workflow"
                "|RemoteTrigger|SendMessage|Cron[A-Za-z]*|Schedule[A-Za-z]*)$",
            ),
        ),
        ["does not fire for mcp__x__merge_it", "mcp__x__delete_file"],
    ),
    # A partly stale matcher that keeps only three of the nine MCP keywords.
    "matcher-with-partial-mcp-keywords": (
        lambda f, wt: edit_settings(
            user_settings(f),
            set_matcher(
                "PreToolUse",
                GUARD,
                "^(Bash|Skill|Agent|Task|Edit|Write|NotebookEdit|Monitor|Workflow"
                "|RemoteTrigger|SendMessage|Cron[A-Za-z]*|Schedule[A-Za-z]*)$"
                "|^mcp__.*(merge|push|create_or_update_file)",
            ),
        ),
        [
            "does not fire for mcp__x__commit_it",
            "mcp__x__pull_request_it",
            "mcp__x__delete_file",
            "mcp__x__update_ref",
            "mcp__x__create_ref",
            "mcp__x__create_branch",
        ],
    ),
    "user-prompt-matcher-cannot-fire": (
        lambda f, wt: edit_settings(
            user_settings(f), set_matcher("UserPromptSubmit", GUARD, "never")
        ),
        ["UserPromptSubmit registration", "may stop it firing"],
    ),
    "disable-all-hooks-user": (
        lambda f, wt: edit_settings(user_settings(f), disable_hooks),
        ["settings.json sets disableAllHooks"],
    ),
    "disable-all-hooks-project": (
        lambda f, wt: edit_settings(wt / ".claude/settings.json", disable_hooks),
        [".claude/settings.json sets disableAllHooks"],
    ),
    "disable-all-hooks-project-local": (
        lambda f, wt: edit_settings(wt / ".claude/settings.local.json", disable_hooks),
        ["settings.local.json sets disableAllHooks"],
    ),
    "config-dir-elsewhere": (
        lambda f, wt: {"CLAUDE_CONFIG_DIR": str(f.home / "other-claude")},
        ["CLAUDE_CONFIG_DIR is", "unset it"],
    ),
    "no-identity-registration": (
        lambda f, wt: edit_settings(user_settings(f), drop("PreToolUse", IDENTITY)),
        [f"no PreToolUse registration of {IDENTITY} that fires for Bash"],
    ),
}


@pytest.mark.parametrize("case", sorted(IR4_CASES))
def test_ir4_each_failing_condition_refuses_the_launch(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path, case: str
) -> None:
    wt = launch_scene(fake_orca, git_repo, issue_dir)
    breaker, names = IR4_CASES[case]
    env = breaker(fake_orca, wt)
    env = env if isinstance(env, dict) else {}
    files = [user_settings(fake_orca)] + [
        wt / ".claude" / n for n in ("settings.json", "settings.local.json")
    ]
    before = {p: p.read_bytes() for p in files if p.exists()}
    data = run_launch(fake_orca, git_repo, issue_dir, **env)
    assert_refused(fake_orca, data, *names)
    if "disable-all-hooks-project" in case:
        assert str(wt) in data["detail"]
    # The check never edits configuration.
    assert {p: p.read_bytes() for p in files if p.exists()} == before
    assert "launch" not in json.loads((issue_dir / "worktree.json").read_text())


@pytest.mark.parametrize("missing", ["cat", "sed", "tr", "mkdir", "mv", "ln", "rm"])
def test_ir4_a_missing_guard_command_refuses_the_launch(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path, missing: str
) -> None:
    # Without `cat` the guard reads an empty payload and allows, so a session
    # would run ungoverned; the other commands are what it needs to bind one.
    launch_scene(fake_orca, git_repo, issue_dir)
    bare = fake_orca.bin.parent / f"guard-commands-no-{missing}"
    bare.mkdir()
    for name in ("git", "cat", "sed", "tr", "mkdir", "mv", "ln", "rm"):
        if name != missing:
            (bare / name).symlink_to(shutil.which(name))
    for stub in fake_orca.tools.iterdir():
        (bare / stub.name).symlink_to(stub)
    path = f"{fake_orca.bin}{os.pathsep}{bare}"
    data = run_launch(fake_orca, git_repo, issue_dir, PATH=path)
    assert_refused(fake_orca, data, f"{missing} is not on PATH")


def test_ir4_stale_registrations_name_the_force_flag(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    launch_scene(fake_orca, git_repo, issue_dir)
    edit_settings(user_settings(fake_orca), set_matcher("PreToolUse", GUARD, "Bash"))
    data = run_launch(fake_orca, git_repo, issue_dir)
    assert_refused(
        fake_orca, data, "run superclaude install --force to replace the registration"
    )


def test_ir4_non_linux_host_is_refused(
    monkeypatch: pytest.MonkeyPatch,
    fake_orca: FakeOrca,
    git_repo: Path,
    issue_dir: Path,
) -> None:
    import importlib.util

    wt = launch_scene(fake_orca, git_repo, issue_dir)
    spec = importlib.util.spec_from_file_location("orca_worktree_ir4", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, spec.name, module)  # dataclasses need it
    spec.loader.exec_module(module)
    for key, value in fake_orca.env().items():
        monkeypatch.setenv(key, value)
    assert module.enforcement_preflight(str(wt)) == []
    monkeypatch.setattr(module.sys, "platform", "darwin")
    (reason,) = module.enforcement_preflight(str(wt))
    assert "not Linux" in reason and "job identity hook needs" in reason

    # The process interfaces the identity hook uses are probed on the claim
    # process itself, read-only: pidfd_open and the child-subreaper query.
    monkeypatch.undo()
    for key, value in fake_orca.env().items():
        monkeypatch.setenv(key, value)

    import ctypes

    class FakeLibc:
        def __init__(self, pidfd: int, prctl: int) -> None:
            self.pidfd, self.prctl_result = pidfd, prctl

        def pidfd_open(self, pid: int, flags: int) -> int:
            return self.pidfd

        def prctl(self, *_args) -> int:
            return self.prctl_result

    real_cdll = ctypes.CDLL
    monkeypatch.setattr(ctypes, "CDLL", lambda *a, **k: FakeLibc(-1, 0))
    (reason,) = module.enforcement_preflight(str(wt))
    assert "lacks pidfd_open" in reason and "prctl" not in reason
    monkeypatch.setattr(ctypes, "CDLL", lambda *a, **k: FakeLibc(-1, -1))
    (reason,) = module.enforcement_preflight(str(wt))
    assert "pidfd_open, prctl(PR_GET_CHILD_SUBREAPER)" in reason
    monkeypatch.setattr(ctypes, "CDLL", lambda *a, **k: object())  # no symbols
    (reason,) = module.enforcement_preflight(str(wt))
    assert "pidfd_open, prctl(PR_GET_CHILD_SUBREAPER)" in reason
    monkeypatch.setattr(ctypes, "CDLL", real_cdll)
    assert module.enforcement_preflight(str(wt)) == []


def test_ir4_pipeline_none_never_reaches_the_preflight(
    fake_orca: FakeOrca, issue_dir: Path
) -> None:
    # Nothing is installed in HOME; --level none is still a bad argument (exit 2),
    # and the claim runs Wave 8 only when --pipeline is not none.
    args = ["--number", "302", "--source", str(issue_dir), "--level", "none"]
    proc = run_script("launch", *args, env=fake_orca.env())
    assert proc.returncode == 2 and "W-ENFORCEMENT-ABSENT" not in proc.stdout
    assert fake_orca.calls() == [] and not (fake_orca.home / ".claude").exists()
    claim = (SCRIPT.parents[1] / "refs/claim.md").read_text()
    assert "Runs only when `--pipeline` is not `none`" in claim


def test_la7_launch_without_a_usable_worktree_record_calls_nothing(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path, tmp_path: Path
) -> None:
    launch_scene(fake_orca, git_repo, issue_dir)
    record = issue_dir / "worktree.json"
    other = tmp_path / "other"
    other.mkdir()
    subprocess.run(["git", "init", "-q", str(other)], check=True)
    for content in (
        None,
        "not json",
        json.dumps({"path": str(tmp_path / "gone")}),
        json.dumps({"path": str(other)}),
    ):
        record.unlink(missing_ok=True)
        if content is not None:
            record.write_text(content)
        data = run_launch(fake_orca, git_repo, issue_dir)
        assert data["status"] == "failed" and data["warning"] == "W-LAUNCH-FAILED"
        assert "no usable worktree record" in data["detail"]
    assert fake_orca.calls() == []
    assert not (fake_orca.home / ".claude/state").exists()


def test_launch_creates_no_file_in_the_worktree_or_the_source_directory(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    wt = launch_scene(fake_orca, git_repo, issue_dir)
    before = (
        tree_listing(wt),
        tree_listing(issue_dir),
        git(wt, "status", "--porcelain"),
    )
    run_launch(fake_orca, git_repo, issue_dir)
    assert tree_listing(wt) == before[0]
    assert tree_listing(issue_dir) == before[1]
    assert git(wt, "status", "--porcelain") == before[2]


def test_arg1_launch_bad_arguments_exit_2(fake_orca: FakeOrca, issue_dir: Path) -> None:
    good = ["--number", "302", "--source", str(issue_dir), "--level", "full"]
    env = fake_orca.env()
    assert run_script("launch", env=env).returncode == 2
    for flag in ("--number", "--source", "--level"):
        i = good.index(flag)
        assert run_script("launch", *good[:i], *good[i + 2 :], env=env).returncode == 2
    for flag, value in {"--level": "none", "--number": "0"}.items():
        args = list(good)
        args[args.index(flag) + 1] = value
        assert run_script("launch", *args, env=env).returncode == 2
    worktree = ["--number", "302", "--source", str(issue_dir), "--level", "worktree"]
    assert run_script("launch", *worktree, "--submit", env=env).returncode == 2
    assert fake_orca.calls() == []


# --- regression tests for the review findings of PR 425 ----------------------


@pytest.mark.parametrize("result", ["x", [1, 2], 5, True], ids=str)
def test_pr425_preflight_non_mapping_result_is_a_failed_check_not_a_traceback(
    fake_orca: FakeOrca, result: object
) -> None:
    fake_orca.respond("status", {"stdout": {"ok": True, "result": result}})
    data = run_json("preflight", env=fake_orca.env())
    assert data["ok"] is False and data["detail"]


def test_pr425_copy_refuses_a_symlinked_destination_directory(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path, tmp_path: Path
) -> None:
    wt = add_worktree(git_repo, "issue-302", "ironbelly/issue-302")
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "issue-summary.md").write_text("precious\n")
    (wt / ".dev/issues").mkdir(parents=True)
    (wt / ".dev/issues/302").symlink_to(outside, target_is_directory=True)
    fake_orca.respond("worktree-list", {"stdout": listing(main_row(git_repo), row(wt))})
    data = run_wt(fake_orca, git_repo, issue_dir)
    assert data["status"] == "failed" and data["warning"] == "W-WORKTREE-COPY-FAILED"
    assert "symlink" in data["detail"]
    assert (outside / "issue-summary.md").read_text() == "precious\n"
    assert sorted(p.name for p in outside.iterdir()) == ["issue-summary.md"]
    assert not (issue_dir / "worktree.json").exists()


def test_pr425_copy_refuses_a_symlinked_subdirectory(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path, tmp_path: Path
) -> None:
    wt = add_worktree(git_repo, "issue-302", "ironbelly/issue-302")
    outside = tmp_path / "outside"
    outside.mkdir()
    dest = wt / ".dev/issues/302"
    dest.mkdir(parents=True)
    (dest / "analysis").symlink_to(outside, target_is_directory=True)
    fake_orca.respond("worktree-list", {"stdout": listing(main_row(git_repo), row(wt))})
    data = run_wt(fake_orca, git_repo, issue_dir)
    assert data["status"] == "failed" and data["warning"] == "W-WORKTREE-COPY-FAILED"
    assert list(outside.iterdir()) == []
    assert not (issue_dir / "worktree.json").exists()


@pytest.mark.skipif(os.geteuid() == 0, reason="root reads every directory")
def test_pr425_copy_reports_an_unreadable_source_subdirectory(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    wt = add_worktree(git_repo, "issue-302", "ironbelly/issue-302")
    fake_orca.respond("worktree-list", {"stdout": listing(main_row(git_repo), row(wt))})
    locked = issue_dir / "analysis"
    locked.chmod(0o000)
    try:
        data = run_wt(fake_orca, git_repo, issue_dir)
    finally:
        locked.chmod(0o755)
    assert data["status"] == "failed" and data["warning"] == "W-WORKTREE-COPY-FAILED"
    assert "analysis" in data["detail"]
    assert not (issue_dir / "worktree.json").exists()


def test_pr425_record_writes_never_follow_a_planted_temp_symlink(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path, tmp_path: Path
) -> None:
    victim = tmp_path / "victim.txt"
    victim.write_text("keep me\n")
    wt = add_worktree(git_repo, "issue-302", "ironbelly/issue-302")
    fake_orca.respond("worktree-list", {"stdout": listing(main_row(git_repo), row(wt))})
    (issue_dir / "worktree.json.tmp").symlink_to(victim)
    data = run_wt(fake_orca, git_repo, issue_dir)
    assert data["status"] == "reused"
    assert victim.read_text() == "keep me\n"
    assert read_record(issue_dir)["path"] == str(wt)


def test_pr425_prompt_write_never_follows_a_planted_temp_symlink(
    tmp_path: Path,
) -> None:
    victim = tmp_path / "victim.txt"
    victim.write_text("keep me\n")
    out = tmp_path / "launch-prompt.md"
    (tmp_path / "launch-prompt.md.tmp").symlink_to(victim)
    args = ["prompt", "--template", str(TEMPLATE), "--level", "full"]
    args += ["--number", "302", "--repo", REPO, "--out", str(out)]
    proc = run_script(*args, env=dict(os.environ))
    assert json.loads(proc.stdout)["status"] == "written"
    assert victim.read_text() == "keep me\n" and out.read_text().strip()


def test_pr425_launch_record_never_follows_a_planted_temp_symlink(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path, tmp_path: Path
) -> None:
    victim = tmp_path / "victim.txt"
    victim.write_text("keep me\n")
    launch_scene(fake_orca, git_repo, issue_dir)
    (issue_dir / "worktree.json.tmp").symlink_to(victim)
    data = run_launch(fake_orca, git_repo, issue_dir)
    assert data["status"] == "launched"
    assert victim.read_text() == "keep me\n"
    assert "launch" in json.loads((issue_dir / "worktree.json").read_text())


def test_pr425_launch_is_remembered_when_the_issue_is_reclaimed_inside_the_worktree(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    wt = launch_scene(fake_orca, git_repo, issue_dir)
    run_launch(fake_orca, git_repo, issue_dir)  # first claim, from the main checkout
    assert len(launch_calls(fake_orca)) == 1
    inside = wt / ".dev/issues/302"  # the copy of the issue folder in the worktree
    inside.mkdir(parents=True, exist_ok=True)
    (inside / "next-steps.md").write_text("steps\n")
    fake_orca.respond("worktree-list", {"stdout": listing(main_row(git_repo), row(wt))})
    again = run_json(
        "worktree", "--repo", REPO, "--number", "302", "--base", "origin/master",
        "--source", str(inside), env=fake_orca.env(), cwd=wt,
    )  # fmt: skip
    assert again["status"] == "reused"
    data = run_json(
        "launch", "--number", "302", "--source", str(inside), "--level", "full",
        env=fake_orca.env(SC_ORCA_SHIM_INTERVAL="0"), cwd=wt,
    )  # fmt: skip
    assert data["status"] == "already_launched"
    assert len(launch_calls(fake_orca)) == 1


def test_pr425_launch_is_remembered_in_the_worktree_for_a_later_main_checkout_claim(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path, tmp_path: Path
) -> None:
    wt = launch_scene(fake_orca, git_repo, issue_dir)
    run_launch(fake_orca, git_repo, issue_dir)
    other = tmp_path / "second-claim" / "302"  # a fresh issue folder, no record
    other.mkdir(parents=True)
    (other / "next-steps.md").write_text("steps\n")
    fake_orca.respond("worktree-list", {"stdout": listing(main_row(git_repo), row(wt))})
    assert run_wt(fake_orca, git_repo, other)["status"] == "reused"
    assert run_launch(fake_orca, git_repo, other)["status"] == "already_launched"
    assert len(launch_calls(fake_orca)) == 1


def test_pr425_a_replacement_worktree_does_not_inherit_the_old_launch_entry(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    old = launch_scene(fake_orca, git_repo, issue_dir)
    run_launch(fake_orca, git_repo, issue_dir)
    git(git_repo, "worktree", "remove", "--force", str(old))
    new = created_scene(fake_orca, git_repo, name="issue-302-2")
    data = run_wt(fake_orca, git_repo, issue_dir)
    assert data["status"] == "created" and data["path"] == str(new)
    assert "launch" not in read_record(issue_dir)
    again = run_launch(fake_orca, git_repo, issue_dir)
    assert again["status"] == "launched"
    assert len(launch_calls(fake_orca)) == 2


def test_pr425_round2_a_tracked_prev_name_is_never_overwritten(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    wt = add_worktree(git_repo, "issue-302", "ironbelly/issue-302")
    dest = wt / ".dev/issues/302"
    dest.mkdir(parents=True)
    (dest / "issue-summary.md").write_text("differs from the source\n")
    (dest / "issue-summary.md.prev").write_text("tracked backup\n")
    git(wt, "add", ".dev/issues/302/issue-summary.md.prev")
    git(wt, "commit", "-m", "track the backup name")
    fake_orca.respond("worktree-list", {"stdout": listing(main_row(git_repo), row(wt))})
    data = run_wt(fake_orca, git_repo, issue_dir)
    assert data["warning"] == "W-WORKTREE-COPY-FAILED"
    assert "issue-summary.md" in data["detail"] and "tracked" in data["detail"]
    assert (dest / "issue-summary.md.prev").read_text() == "tracked backup\n"
    assert (dest / "issue-summary.md").read_text() == "differs from the source\n"
    assert (
        git(wt, "status", "--short", "--", ".dev/issues/302/issue-summary.md.prev")
        == ""
    )


def run_prompt(issue_dir: Path, out: Path, git_repo: Path, env: dict[str, str]) -> dict:
    args = ["prompt", "--template", str(TEMPLATE), "--level", "worktree"]
    args += ["--number", "302", "--repo", REPO, "--source", str(issue_dir)]
    args += ["--out", str(out)]
    return run_json(*args, env=env, cwd=git_repo)


def test_pr425_round2_prompt_of_a_live_launch_is_kept(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    launch_scene(fake_orca, git_repo, issue_dir)
    assert run_launch(fake_orca, git_repo, issue_dir)["status"] == "launched"
    out = issue_dir / "launch-prompt.md"
    out.write_text("the prompt the running agent read\n")
    data = run_prompt(issue_dir, out, git_repo, fake_orca.env())
    assert data["status"] == "kept"
    assert out.read_text() == "the prompt the running agent read\n"


def test_pr425_round2_prompt_is_rendered_again_for_a_replacement_worktree(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    old = launch_scene(fake_orca, git_repo, issue_dir)
    run_launch(fake_orca, git_repo, issue_dir, "full", submit=True)
    out = issue_dir / "launch-prompt.md"
    out.write_text("old full and submit prompt\n")
    git(git_repo, "worktree", "remove", "--force", str(old))
    # the claim renders the prompt (Wave 5) before it creates the worktree (Wave 7)
    data = run_prompt(issue_dir, out, git_repo, fake_orca.env())
    assert data["status"] == "written"
    assert "old full and submit prompt" not in out.read_text()
    created_scene(fake_orca, git_repo, name="issue-302-2")
    assert run_wt(fake_orca, git_repo, issue_dir)["status"] == "created"
    assert (
        run_launch(fake_orca, git_repo, issue_dir, "worktree")["status"] == "launched"
    )


def test_pr425_round2_prompt_without_a_launch_entry_is_written(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    launch_scene(fake_orca, git_repo, issue_dir)
    out = issue_dir / "launch-prompt.md"
    out.write_text("stale\n")
    assert run_prompt(issue_dir, out, git_repo, fake_orca.env())["status"] == "written"
    assert out.read_text() != "stale\n"


def no_launch_happened(fake: FakeOrca, source: Path) -> bool:
    pending = pending_dir(fake)
    return (
        not launch_calls(fake)
        and not (pending.exists() and list(pending.iterdir()))
        and "launch" not in read_record(source)
    )


def test_pr425_round3_a_tracked_older_prompt_blocks_the_launch(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    wt = launch_scene(fake_orca, git_repo, issue_dir)
    old = wt / ".dev/issues/302/launch-prompt.md"
    old.write_text("old prompt: implement, commit and push\n")
    git(wt, "add", ".dev/issues/302/launch-prompt.md")
    git(wt, "commit", "-m", "track an older prompt")
    (issue_dir / "launch-prompt.md").write_text("new prompt: stop at the plan\n")
    fake_orca.respond("worktree-list", {"stdout": listing(main_row(git_repo), row(wt))})
    copied = run_wt(fake_orca, git_repo, issue_dir)
    assert copied["status"] == "reused" and "launch-prompt.md" in copied["detail"]
    data = run_launch(fake_orca, git_repo, issue_dir, "worktree")
    assert data["status"] == "failed" and data["warning"] == "W-LAUNCH-FAILED"
    assert "launch-prompt.md" in data["detail"] and "re-run the claim" in data["detail"]
    assert data["hand_command"] is None
    assert old.read_text() == "old prompt: implement, commit and push\n"
    assert no_launch_happened(fake_orca, issue_dir)


def test_pr425_round3_an_untracked_older_prompt_blocks_the_launch_too(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    wt = launch_scene(fake_orca, git_repo, issue_dir)
    (wt / ".dev/issues/302/launch-prompt.md").write_text("an older prompt\n")
    data = run_launch(fake_orca, git_repo, issue_dir)
    assert data["status"] == "failed" and "differs" in data["detail"]
    assert no_launch_happened(fake_orca, issue_dir)


def test_pr425_round3_a_missing_prompt_blocks_the_launch(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    wt = launch_scene(fake_orca, git_repo, issue_dir)
    (wt / ".dev/issues/302/launch-prompt.md").unlink()
    assert run_launch(fake_orca, git_repo, issue_dir)["status"] == "failed"
    assert no_launch_happened(fake_orca, issue_dir)


def test_pr425_round3_a_source_without_a_rendered_prompt_blocks_the_launch(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    launch_scene(fake_orca, git_repo, issue_dir)
    (issue_dir / "launch-prompt.md").unlink()
    data = run_launch(fake_orca, git_repo, issue_dir)
    assert data["status"] == "failed" and "no prompt was rendered" in data["detail"]
    assert no_launch_happened(fake_orca, issue_dir)


def test_pr425_round3_a_symlinked_prompt_blocks_the_launch(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path, tmp_path: Path
) -> None:
    wt = launch_scene(fake_orca, git_repo, issue_dir)
    elsewhere = tmp_path / "elsewhere.md"
    elsewhere.write_text("the rendered prompt\n")  # same bytes, still refused
    target = wt / ".dev/issues/302/launch-prompt.md"
    target.unlink()
    target.symlink_to(elsewhere)
    data = run_launch(fake_orca, git_repo, issue_dir)
    assert data["status"] == "failed" and "symlink" in data["detail"]
    assert no_launch_happened(fake_orca, issue_dir)
