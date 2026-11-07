"""Tests for ``scripts/orca_worktree.py`` (the Orca step of ``/sc:issue --claim``).

No test calls a real ``orca``, ``gh``, the network or a real agent. A fake
``orca`` executable is put first on ``PATH``; it logs every argv and answers
from JSON files the test writes. ``HOME`` is a temporary directory.
"""

from __future__ import annotations

import json
import os
import re
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
        env["PATH"] = f"{self.bin}{os.pathsep}{env['PATH']}"
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


def created_scene(
    fake: FakeOrca, git_repo: Path, *, effect: bool = True, name: str = "issue-302"
) -> Path:
    """Orca lists only the main row, creates `name`, then lists the new row too."""
    wt = git_repo.parent / "wts" / name
    cmd = [
        "git", "-C", str(git_repo), "worktree", "add", "-b", f"ironbelly/{name}",
        str(wt), "origin/master",
    ]  # fmt: skip
    fake.respond(
        "worktree-create",
        {"stdout": "opaque, not json"} | ({"effect": cmd} if effect else {}),
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
    assert data["warning"] is None
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
        json.dumps({"path": "/old", "status": "created", "launch": launch})
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
    created_scene(fake_orca, git_repo)
    run_wt(fake_orca, git_repo, issue_dir)
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
    ]
    for call in fake_orca.calls():
        for arg in call:
            assert not arg.startswith(FORBIDDEN_FLAGS), arg


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
    args += ["--number", "302", "--out", str(out)]
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
    good += ["--out", str(tmp_path / "x.md")]
    assert run_script("prompt", env=env).returncode == 2
    for flag in ("--template", "--level", "--number", "--out"):
        i = good.index(flag)
        assert run_script("prompt", *good[:i], *good[i + 2 :], env=env).returncode == 2
    for flag, value in {"--level": "none", "--number": "0"}.items():
        args = list(good)
        args[args.index(flag) + 1] = value
        assert run_script("prompt", *args, env=env).returncode == 2
    assert not (tmp_path / "x.md").exists()


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
    """A real worktree with a guarded record, an Orca that launches and a hook."""
    wt = add_worktree(git_repo, "issue-302", "ironbelly/issue-302")
    (issue_dir / "worktree.json").write_text(
        json.dumps({"path": str(wt), "status": "created"})
    )
    fake.respond("agent-launch", {"stdout": LAUNCH_OK})
    fake.respond("terminal-read", {"stdout": SCREEN_OK})
    if hook:
        script = fake.home / ".claude" / "hooks" / "launch-level-guard.sh"
        script.parent.mkdir(parents=True)
        script.write_text("#!/bin/sh\n")
        script.chmod(0o755 if hook == "exec" else 0o644)
    return wt


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
    launch_scene(fake_orca, git_repo, issue_dir)
    run_launch(fake_orca, git_repo, issue_dir)
    record = json.loads((issue_dir / "worktree.json").read_text())
    del record["launch"]
    (issue_dir / "worktree.json").write_text(json.dumps(record))
    run_launch(fake_orca, git_repo, issue_dir)
    nonces = {PROMPT_RE.match(c[9]).group(1) for c in launch_calls(fake_orca)}
    assert len(nonces) == 2 and len(list(pending_dir(fake_orca).iterdir())) == 2


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
    launch_scene(fake_orca, git_repo, issue_dir, hook=None)
    (fake_orca.home / ".claude").write_text("a file where the store should be\n")
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


def test_la4_launch_record_update_failure_never_says_to_rerun_the_claim(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    launch_scene(fake_orca, git_repo, issue_dir)
    (issue_dir / "worktree.json.tmp").mkdir()  # makes the record update fail
    data = run_launch(fake_orca, git_repo, issue_dir)
    assert data["status"] == "launched" and data["warning"] is None
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
    assert data["status"] == "launched" and data["warning"] is None
    assert orca_calls(fake_orca, "terminal", "read") == [
        ["terminal", "read", "--terminal", "term_abc", "--screen", "--json"]
    ]


def test_la5_launch_shim_check_retries_up_to_five_times(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    launch_scene(fake_orca, git_repo, issue_dir)
    plain = {"stdout": SCREEN_PLAIN}
    fake_orca.respond("terminal-read", plain, plain, {"stdout": SCREEN_OK})
    assert run_launch(fake_orca, git_repo, issue_dir)["warning"] is None
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


@pytest.mark.parametrize("hook", [None, "plain"], ids=["absent", "not-executable"])
def test_la6_launch_without_an_executable_hook_warns_and_still_launches(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path, hook: str | None
) -> None:
    launch_scene(fake_orca, git_repo, issue_dir, hook=hook)
    data = run_launch(fake_orca, git_repo, issue_dir)
    assert data["status"] == "launched"
    assert data["enforcement_hook"] == "missing"
    assert data["warning"] == "W-ENFORCEMENT-ABSENT"
    assert "#394" in data["detail"]
    assert len(launch_calls(fake_orca)) == 1


def test_la6_launch_with_the_hook_installed_has_no_warning(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    launch_scene(fake_orca, git_repo, issue_dir)
    data = run_launch(fake_orca, git_repo, issue_dir)
    assert data["enforcement_hook"] == "installed" and data["warning"] is None
    assert len(launch_calls(fake_orca)) == 1


def test_la6_launch_two_warnings_put_the_shim_one_first(
    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
) -> None:
    launch_scene(fake_orca, git_repo, issue_dir, hook=None)
    fake_orca.respond("terminal-read", {"stdout": SCREEN_PLAIN})
    data = run_launch(fake_orca, git_repo, issue_dir)
    assert data["warning"] == "W-LAUNCH-NOT-CCSESSION"
    assert "also W-ENFORCEMENT-ABSENT" in data["detail"]


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
    before = (tree_listing(wt), tree_listing(issue_dir))
    run_launch(fake_orca, git_repo, issue_dir)
    assert tree_listing(wt) == before[0]
    assert tree_listing(issue_dir) == before[1]
    assert git(wt, "status", "--porcelain") == ""


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
