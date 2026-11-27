"""T-20, AC-17: protecting the work outside the commit set S (FR-110 to FR-118; design 6.1).

Each case builds a real repository, a real ledger and sidecar, and runs the commit
procedure the way the executor does: plan, prepared line, candidate pin, add, the worktree
snapshot, the pin of that snapshot, and then a real ``git commit --only`` under the hook
emulator of ``conftest.py`` (it replays the framework's stash-and-restore sequence). The
helper is then asked with ``verify``. The snapshot is taken by ``take_snapshot`` below, a
test helper that mirrors the Q0 private-index method of ``sc-implement-protocol/SKILL.md``
(private index, ``read-tree HEAD``, ``add -A``, ``write-tree``) and pins it create-once,
the way the agent will.

What is pinned here: edits outside S (unstaged, staged, assume-unchanged, skip-worktree,
a deletion, a mode change) are recoverable byte for byte from the pinned worktree tree
with ``git restore --source=<saved-ref> -- <literal-paths>`` after an interrupted or a
rewriting hook; unrelated staged entries keep their meaning; a success with outside damage
is reported and never committed twice.

Observed with git 2.47.3 and the emulator of ``conftest.py`` (pre-commit 4.6.2 sequence);
other git versions are UNVERIFIED. A timeout is modelled as the tool killing the whole
process group (status 137); how the host reports a timeout is UNVERIFIED. The cases that
compare the emulator with the real framework carry the ``real_framework`` marker and are
skipped when ``pre-commit`` is not on ``PATH``.
"""

from __future__ import annotations

import importlib
import os
import shutil
import signal
import subprocess
import tempfile
import time
from pathlib import Path

import pytest

from .conftest import Repo, SidecarBuilder
from .test_hook_refusal import Flow
from .test_stage_plan import PIN

ZERO = "0" * 40
PERSON_UNSTAGED = "person: unstaged edit\n"
PERSON_STAGED = "person: staged edit\n"
PERSON_AU = "person: assume-unchanged edit\n"
PERSON_SW = "person: skip-worktree edit\n"
TRACKED = {  # written before the Flow commits its base, so every file is in HEAD
    "staged.txt": "staged base\n",
    "au.txt": "assume-unchanged base\n",
    "sw.txt": "skip-worktree base\n",
    "gone.txt": "gone base\n",
    "run.sh": "#!/bin/sh\n",
    "notes.txt": "notes base\n",
}
WATCHED = (
    "src/b.py",
    "staged.txt",
    "au.txt",
    "sw.txt",
    "gone.txt",
    "run.sh",
    "notes.txt",
)


@pytest.fixture
def vcs(scripts_dir):
    return importlib.import_module("vcs")


@pytest.fixture
def vcs_plan(scripts_dir):
    return importlib.import_module("vcs_plan")


@pytest.fixture
def flow(repo, vcs, hook_emulator):
    """``flow(files)`` writes tracked files into the base commit, then makes a Flow."""

    def make(files=TRACKED, managed=False):
        for rel, text in files.items():
            repo.write(rel, text)
        return Flow(repo, vcs, hook_emulator, managed)

    return make


# --- the snapshot, as the agent takes it --------------------------------------------------------
class SnapshotFailed(Exception):
    """The Q0 snapshot did not complete: the agent writes ``refused reason=snapshot-failed``."""


class PinConflict(Exception):
    """A saved ref exists with another target: ``refused reason=pin-conflict`` (FR-110)."""


def take_snapshot(repo):
    """SKILL.md Q0: a private index, ``read-tree HEAD``, ``add -A``, ``write-tree``."""
    with tempfile.TemporaryDirectory() as folder:
        env = {**os.environ, "GIT_INDEX_FILE": os.path.join(folder, "index")}
        out = ""
        for args in (["read-tree", "HEAD"], ["add", "-A"], ["write-tree"]):
            done = subprocess.run(
                ["git", *args], cwd=repo.work, env=env, capture_output=True, text=True
            )
            if done.returncode != 0:
                raise SnapshotFailed(f"git {args[0]} exited {done.returncode}")
            out = done.stdout.strip()
    return out


def pin_once(repo, ref, tree):
    """Create ``ref`` at ``tree``; an existing different target is ``PinConflict``."""
    code, current = repo.git("rev-parse", "--verify", "--quiet", ref, check=False)
    if code == 0:
        if current.strip() == tree:
            return
        raise PinConflict(f"{ref} already points at {current.strip()}")
    repo.git("update-ref", ref, tree, ZERO)  # create-only: git refuses a racing writer


def pin_worktree(f):
    pin_once(f.repo, f.worktree_ref, take_snapshot(f.repo))
    return f.repo.git("rev-parse", f.worktree_ref).strip()


# --- what the person's work looks like ----------------------------------------------------------
def person_edits(repo):
    """Edits outside S: unstaged, staged, assume-unchanged, skip-worktree, a deletion, a
    mode change and a new file. Made after Q0, so no product path is touched."""
    repo.write("src/b.py", PERSON_UNSTAGED)
    repo.write("staged.txt", PERSON_STAGED)
    repo.git("add", "--", "staged.txt")
    repo.git("update-index", "--assume-unchanged", "au.txt")
    repo.write("au.txt", PERSON_AU)
    repo.git("update-index", "--skip-worktree", "sw.txt")
    repo.write("sw.txt", PERSON_SW)
    os.remove(repo.work / "gone.txt")
    os.chmod(repo.work / "run.sh", 0o755)
    repo.write("fresh.txt", "person: a new file\n")


def state(repo, rel):
    """``(bytes, executable)`` of a work-tree file, or None when it is absent."""
    path = repo.work / rel
    if not path.exists():
        return None
    return path.read_bytes(), bool(path.stat().st_mode & 0o111)


def states(repo, names=WATCHED):
    return {rel: state(repo, rel) for rel in names}


def restore_from_pin(repo, ref, paths):
    """The FR-115 command shape, for saved paths only; returns git's exit status."""
    done = subprocess.run(
        ["git", "restore", f"--source={ref}", "--", *paths],
        cwd=repo.work,
        capture_output=True,
        text=True,
    )
    return done.returncode


def in_pin(repo, ref, rel):
    return repo.git("ls-tree", ref, "--", rel).strip() != ""


def recover(repo, ref, paths):
    """Restore the paths the pin holds; the rest is left for separate handling (FR-115): a
    path the pin does not hold is never part of a blanket restore, because git would delete
    it (see ``test_a_blanket_restore_deletes_a_tracked_path_the_pin_does_not_hold``)."""
    saved = [p for p in paths if in_pin(repo, ref, p)]
    unsaved = [p for p in paths if p not in saved]
    if saved:
        owner_clears_stale_locks(repo, ref, saved)
        assert restore_from_pin(repo, ref, saved) == 0
    return saved, unsaved


def owner_clears_stale_locks(repo, ref, saved):
    """SIGKILL leaves git's lock files. While one exists even the restore is refused and
    changes nothing; the owner removes it once no git or hook process runs (FR-116: the
    executor never reclaims a lock)."""
    stale = sorted((repo.work / ".git").glob("*.lock"))
    if not stale:
        return
    before = states(repo, saved)
    assert restore_from_pin(repo, ref, saved) != 0
    assert states(repo, saved) == before
    for lock in stale:
        lock.unlink()


# --- processes ----------------------------------------------------------------------------------
def group_members(pgid):
    """Live (not zombie) processes of a process group, read from ``/proc``."""
    found = []
    for entry in os.listdir("/proc"):
        if not entry.isdigit():
            continue
        try:
            raw = Path(f"/proc/{entry}/stat").read_text(encoding="utf-8")
        except OSError:
            continue
        fields = raw.rsplit(")", 1)[1].split()  # state, ppid, pgrp, ...
        if fields[2] == str(pgid) and fields[0] != "Z":
            found.append(int(entry))
    return found


def wait_quiet(pgid, limit=30):
    deadline = time.monotonic() + limit
    while group_members(pgid):
        assert time.monotonic() < deadline, "the hook group never stopped"
        time.sleep(0.05)


def interrupt(f, hook, how):
    """Start the commit with a blocked hook and end it; returns the shell status."""
    hook.set_action("block")
    proc = hook.start_blocked_commit(f.cand["commit_paths"], message=f.message())
    if how == "sigterm-group":
        hook.kill_group(proc, signal.SIGTERM)
    elif how == "sigkill":
        hook.kill_group(proc, signal.SIGKILL)
    else:  # the tool's timeout runs out and it kills the whole group
        with pytest.raises(subprocess.TimeoutExpired):
            proc.communicate(timeout=1)
        hook.kill_group(proc, signal.SIGKILL)
    wait_quiet(proc.pid)
    return 128 - proc.returncode


def refused_line(f, reason, uncertain=False):
    """The sidecar line the executor writes for a result; the parser accepts it."""
    line = SidecarBuilder(Path("unused")).refused(
        "1", key=f.key, attempt=1, reason=reason, uncertain=uncertain
    )
    parsed = importlib.import_module("vcs_plan").parse_sidecar(line.lines[0] + "\n")
    return parsed.terminal[f.key]


def count_new_commits(repo, parent):
    return int(repo.git("rev-list", "--count", f"{parent}..HEAD").strip())


# =============================================================================================
# An interrupted hook: SIGTERM to the group, SIGKILL, a timeout (FR-116, FR-118)
# =============================================================================================
@pytest.mark.parametrize("how", ["sigterm-group", "sigkill", "timeout"])
def test_every_edit_outside_s_is_restorable_after_an_interrupted_hook(
    flow, repo, vcs, how
):
    f = flow()
    person_edits(repo)
    before = states(repo)
    f.ready(pin_worktree=False)
    saved_tree = pin_worktree(f)

    status = interrupt(f, f.hook, how)

    assert status in (137, 143)
    assert f.head() == f.parent  # nothing was committed
    first = f.verify(status)  # FR-116: not classified, nothing compared yet
    assert (first["status"], first["reason"]) == ("interrupted", "commit-interrupted")
    assert (first["outside"], first["outside_changed"]) == ("deferred", None)

    res = f.verify(None)  # a later run, after the processes stopped
    assert res["status"] == "pending" and res["head_after"] == f.parent
    damaged = sorted(p for p, was in before.items() if state(repo, p) != was)
    assert {"src/b.py", "staged.txt", "gone.txt", "run.sh"} <= set(damaged)
    assert res["outside"] == "outside-changed"
    assert sorted(res["outside_paths"]) == damaged
    assert res["outside_changed"] == len(damaged)

    saved, unsaved = recover(repo, f.worktree_ref, res["outside_paths"])
    assert unsaved == ["gone.txt"]  # the deletion is not in the pin: separate handling
    os.remove(repo.work / "gone.txt")  # the owner's decision, not a blanket command
    assert states(repo) == before  # byte for byte, modes included
    assert repo.git("rev-parse", f.worktree_ref).strip() == saved_tree


def test_a_blanket_restore_deletes_a_tracked_path_the_pin_does_not_hold(flow, repo):
    """Why FR-115 names saved paths only: the hook put ``gone.txt`` back, the pin holds the
    person's deletion, and ``git restore --source`` would delete the file without asking."""
    f = flow()
    person_edits(repo)
    f.ready()
    interrupt(f, f.hook, "sigkill")
    assert state(repo, "gone.txt") is not None and not in_pin(
        repo, f.worktree_ref, "gone.txt"
    )
    owner_clears_stale_locks(repo, f.worktree_ref, ["gone.txt"])
    assert restore_from_pin(repo, f.worktree_ref, ["gone.txt"]) == 0
    assert (
        state(repo, "gone.txt") is None
    )  # gone: the report must leave this to the owner


@pytest.mark.parametrize("how", ["sigterm-group", "sigkill"])
def test_unrelated_staged_entries_keep_their_meaning_after_an_interruption(
    flow, repo, how
):
    f = flow()
    person_edits(repo)
    f.ready()
    interrupt(f, f.hook, how)

    staged = sorted(repo.git("diff", "--cached", "--name-only").split())
    assert staged == ["src/a.py", "staged.txt"]  # the set's add and the person's entry
    assert repo.git("show", ":staged.txt") == PERSON_STAGED
    owner_clears_stale_locks(repo, f.worktree_ref, ["staged.txt"])
    assert restore_from_pin(repo, f.worktree_ref, ["staged.txt"]) == 0
    # the work tree is again the staged content: the entry means what it meant before
    assert (
        repo.git("status", "--porcelain", "--", "staged.txt").rstrip()
        == "M  staged.txt"
    )


def test_the_index_lock_that_sigkill_leaves_is_reported_and_never_removed(
    flow, repo, vcs, scripts_dir
):
    repo.git("checkout", "-q", "-b", "feature/x")  # not a protected branch
    f = flow()
    person_edits(repo)
    f.ready()
    status = interrupt(f, f.hook, "sigkill")

    lock = repo.work / ".git" / "index.lock"
    assert lock.exists()  # git was killed while it held the lock
    pre = vcs.run_preflight(str(repo.work))
    assert (pre["status"], pre["reason"], pre["index_lock"]) == (
        "refused",
        "index-locked",
        True,
    )
    res = f.verify(None)  # reads only: a stale lock does not stop it
    assert res["status"] == "pending" and res["outside"] == "outside-changed"
    assert f.verify(status)["status"] == "interrupted"
    assert lock.exists()  # nothing here reclaims a lock (FR-116)
    assert repo.git(
        "diff", "--cached", "--name-only"
    ).split()  # and the index is readable


def test_sigterm_lets_git_remove_its_own_lock(flow, repo):
    f = flow()
    f.ready()
    interrupt(f, f.hook, "sigterm-group")
    assert not (repo.work / ".git" / "index.lock").exists()


ORPHAN = """#!/bin/sh
: > '{started}'
sleep {delay}
echo orphan-rewrite >> '{outside}'
echo orphan-rewrite >> '{inside}'
: > '{done}'
exit 0
"""


def test_an_orphan_hook_rewrites_files_after_git_was_killed(
    flow, repo, hook_emulator, tmp_path
):
    """SIGTERM reaches git alone. Its hook keeps running and rewrites files seconds later,
    so a comparison made at once says something else than the final one: the helper's
    interrupted status defers the comparison until the processes stopped (FR-116)."""
    f = flow()
    repo.write(
        "notes.txt", PERSON_UNSTAGED
    )  # unstaged: the hook stashes it for a while
    before = states(repo)
    f.ready(pin_worktree=False)
    pin_worktree(f)
    done = tmp_path / "orphan-done"
    hook_emulator.action_script.write_text(
        ORPHAN.format(
            started=hook_emulator.started,
            delay=2,
            outside=repo.work / "src/b.py",
            inside=repo.work / "src/a.py",
            done=done,
        ),
        encoding="utf-8",
    )
    proc = hook_emulator.start_blocked_commit(
        f.cand["commit_paths"], message=f.message()
    )
    os.kill(proc.pid, signal.SIGTERM)  # git alone, not the group
    proc.wait(timeout=30)  # not communicate(): the orphan still holds the output pipes
    assert group_members(proc.pid)  # the orphan hook is still running

    assert f.verify(143)["outside"] == "deferred"
    too_early = f.verify(None)
    assert too_early["outside_paths"] == [
        "notes.txt"
    ]  # the stash has not come back yet

    wait_quiet(proc.pid)
    assert done.exists()
    final = f.verify(None)
    assert final["status"] == "pending" and final["head_after"] == f.parent
    assert final["outside_paths"] == ["src/b.py"]  # the orphan's rewrite, not the stash
    assert final["outside_paths"] != too_early["outside_paths"]
    assert state(repo, "notes.txt") == before["notes.txt"]  # the hook did restore it
    restore_from_pin(repo, f.worktree_ref, final["outside_paths"])
    assert state(repo, "src/b.py") == (b"old\n", False)

    # the rewrite of a file in S is caught when the boundary is planned again (FR-074)
    again = f.s.plan(candidate=True)
    assert (again["status"], again["reason"]) == ("refused", "changed-after-review")
    assert again["paths"] == ["src/a.py"]


# =============================================================================================
# A hook that rewrites or fails, and a success with damage (FR-113, FR-114)
# =============================================================================================
def test_a_hook_that_rewrites_a_file_outside_s_and_fails_is_restorable(flow, repo):
    f = flow()
    person_edits(repo)
    before = states(repo)
    f.ready(pin_worktree=False)
    pin_worktree(f)

    done = f.commit("rewrite_exit1", "notes.txt")

    assert done.returncode == 1
    res = f.verify(1)
    assert res["status"] == "hook-failed" and res["head_after"] == f.parent
    # the rewrite, and the assume-unchanged edit the hook's checkout overwrote (Task 2);
    # every other edit of the person came back with the saved patch
    assert res["outside_paths"] == ["au.txt", "notes.txt"]
    assert sorted(res["outside_paths"]) == sorted(
        p for p, was in before.items() if state(repo, p) != was
    )
    assert restore_from_pin(repo, f.worktree_ref, res["outside_paths"]) == 0
    assert states(repo) == before


def assume_unchanged_case(flow, repo, visible_edit):
    f = flow()
    repo.git("update-index", "--assume-unchanged", "au.txt")
    repo.write("au.txt", PERSON_AU)
    if visible_edit:  # makes the framework's diff non-empty, so its checkout runs
        repo.write("notes.txt", "a visible unstaged edit\n")
    f.ready(pin_worktree=False)
    pin_worktree(f)
    done = f.commit()
    assert done.returncode == 0, done.stderr
    return f


def test_a_success_with_outside_damage_is_reported_and_never_committed_twice(
    flow, repo
):
    f = assume_unchanged_case(flow, repo, visible_edit=True)
    assert state(repo, "au.txt") == (b"assume-unchanged base\n", False)  # overwritten

    res = f.verify(0)

    assert res["status"] == "committed" and res["sha"] == f.head()  # not relabelled
    assert (res["outside"], res["outside_changed"]) == ("outside-changed", 1)
    assert res["outside_paths"] == ["au.txt"]
    assert count_new_commits(repo, f.parent) == 1
    # the executor's result line carries the count and the saved ref, and the parser takes it
    f.s.side.commit(
        "1", key=f.key, sha=res["sha"], outside_changed=1, wt=f.worktree_ref
    )
    plan = importlib.import_module("vcs_plan")
    side = plan.parse_sidecar("\n".join(f.s.side.lines) + "\n")
    assert side.terminal[f.key].outside_changed == 1
    again = f.s.plan()  # the boundary is settled: no second commit is planned
    assert again["reason"] == "no-due-boundary"
    assert count_new_commits(repo, f.parent) == 1
    assert restore_from_pin(repo, f.worktree_ref, res["outside_paths"]) == 0
    assert state(repo, "au.txt") == (PERSON_AU.encode(), False)
    assert f.verify(0)["status"] == "committed"  # asking again changes nothing
    assert count_new_commits(repo, f.parent) == 1


def test_an_assume_unchanged_edit_alone_survives_and_nothing_is_reported(flow, repo):
    """No other unstaged change exists, so the framework never checks out (git 2.47.3)."""
    f = assume_unchanged_case(flow, repo, visible_edit=False)
    assert state(repo, "au.txt") == (PERSON_AU.encode(), False)
    res = f.verify(0)
    assert (res["status"], res["outside"], res["outside_changed"]) == (
        "committed",
        "unchanged",
        0,
    )


def test_a_resumes_own_run_line_belongs_after_the_comparison(flow, repo):
    """FR-113: a legacy run folder is not committed, so it is outside S. The comparison is
    taken before the resume's own ``run`` line is appended; after it, the sidecar itself
    shows as a change. The ordering is the executor's, and this pins why it matters."""
    f = flow().ready()
    assert f.commit().returncode == 0
    assert f.verify(0)["outside_paths"] == []

    f.s.side.run(2, "on", ledger_lines=SidecarBuilder.ledger_k(f.s.ledger_path))
    f.s.write()

    later = f.verify(0)
    shown = os.path.relpath(f.s.side_path, repo.work)
    assert (later["status"], later["outside_paths"]) == ("committed", [shown])


def test_a_skip_worktree_edit_is_hidden_from_git_but_held_by_the_snapshot(flow, repo):
    """The flag hides the edit from ``git status``, yet the snapshot (a private index built
    from HEAD) holds it (FR-112). With a visible edit present the hook's checkout leaves
    it alone (git 2.47.3), so nothing is lost and the comparison says so."""
    f = flow()
    repo.git("update-index", "--skip-worktree", "sw.txt")
    repo.write("sw.txt", PERSON_SW)
    repo.write("notes.txt", "a visible unstaged edit\n")
    assert "sw.txt" not in repo.git("status", "--porcelain")  # hidden from git
    f.ready(pin_worktree=False)
    pin_worktree(f)
    assert repo.git("show", f"{f.worktree_ref}:sw.txt") == PERSON_SW  # but saved
    assert f.commit().returncode == 0

    res = f.verify(0)

    assert res["status"] == "committed"
    assert (res["outside"], res["outside_changed"]) == ("unchanged", 0)
    assert state(repo, "sw.txt") == (PERSON_SW.encode(), False)
    assert state(repo, "notes.txt") == (b"a visible unstaged edit\n", False)


def test_a_skip_worktree_edit_lost_to_a_kill_is_restorable_from_the_snapshot(
    flow, repo
):
    f = flow()
    repo.git("update-index", "--skip-worktree", "sw.txt")
    repo.write("sw.txt", PERSON_SW)
    repo.write("notes.txt", "a visible unstaged edit\n")
    before = states(repo)
    f.ready(pin_worktree=False)
    pin_worktree(f)
    interrupt(f, f.hook, "sigkill")
    for rel in ("sw.txt", "notes.txt"):  # a deliberate loss, as a worst case
        (repo.work / rel).write_text("lost\n", encoding="utf-8")

    res = f.verify(None)

    assert res["outside_paths"] == ["notes.txt", "sw.txt"]
    recover(repo, f.worktree_ref, res["outside_paths"])
    assert states(repo) == before


# =============================================================================================
# A snapshot that fails, and a configuration whose snapshot would lose content (FR-111, FR-112)
# =============================================================================================
@pytest.mark.skipif(os.geteuid() == 0, reason="root can read every file")
def test_a_snapshot_that_fails_makes_no_commit_and_no_pin(flow, repo, hook_emulator):
    f = flow().ready(pin_worktree=False)
    locked = repo.write("locked.txt", "unreadable\n")
    locked.chmod(0)
    try:
        with pytest.raises(SnapshotFailed):
            pin_worktree(f)  # the agent stops here: it makes no commit
        assert f.head() == f.parent
        assert not hook_emulator.started.exists() and hook_emulator.patches() == []
        assert (
            repo.git("for-each-ref", "refs/superclaude/implement/plan1/boundary-wt")
            == ""
        )
        assert refused_line(f, "snapshot-failed").kind == "refused"

        res = f.verify(None)  # no pin: the comparison cannot be made, and says so
        assert (res["status"], res["outside"]) == ("pending", "outside-unverified")
        assert (res["outside_changed"], res["outside_paths"]) == (None, [])
    finally:
        locked.chmod(0o644)


@pytest.mark.skipif(os.geteuid() == 0, reason="root can read every file")
def test_a_comparison_that_cannot_complete_is_never_read_as_no_changes(flow, repo):
    f = flow().ready()
    assert f.commit().returncode == 0
    locked = repo.write("locked.txt", "unreadable\n")
    locked.chmod(0)
    try:
        res = f.verify(0)
    finally:
        locked.chmod(0o644)
    assert res["status"] == "committed"
    assert (res["outside"], res["outside_changed"]) == ("outside-unverified", None)


def test_a_content_filter_makes_the_snapshot_unsupported(
    flow, repo, vcs, vcs_plan, hook_emulator, monkeypatch, tmp_path
):
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(home / ".config"))

    class Isolated(vcs_plan.GitRunner):
        def _environment(self, index_file):
            env = super()._environment(index_file)
            env["GIT_CONFIG_NOSYSTEM"] = "1"
            env["GIT_CONFIG_GLOBAL"] = "/dev/null"
            return env

    f = flow({".gitattributes": "*.up filter=up\n", "x.up": "base\n"})
    assert vcs.run_preflight(str(repo.work), make_runner=Isolated)["snapshot_lossless"]
    repo.git("config", "filter.up.clean", "tr a-z A-Z")
    repo.write("x.up", "an edit in lower case\n")
    f.ready(pin_worktree=False)

    pre = vcs.run_preflight(str(repo.work), make_runner=Isolated)
    assert pre["snapshot_lossless"] is False
    # why it matters: the snapshot stores the filtered bytes, not the person's bytes
    pin_once(repo, f.worktree_ref, take_snapshot(repo))
    assert repo.git("show", f"{f.worktree_ref}:x.up") == "AN EDIT IN LOWER CASE\n"
    # so the executor refuses the boundary before the commit (FR-112) and nothing runs
    assert refused_line(f, "snapshot-unsupported").kind == "refused"
    assert f.head() == f.parent
    assert not hook_emulator.started.exists() and hook_emulator.patches() == []


# =============================================================================================
# Pins: create-once, one name per attempt, and safe from git gc (FR-110)
# =============================================================================================
def test_a_second_attempt_cannot_overwrite_the_first_attempts_pin(flow, repo):
    f = flow().ready()
    first_pin = repo.git("rev-parse", f.worktree_ref).strip()
    assert f.commit("exit1").returncode == 1
    assert f.verify(1)["status"] == "hook-failed"
    f.s.side.refused("1", key=f.key, attempt=1, reason="hook-failed")

    repo.write("notes.txt", "changed between the attempts\n")
    second = f.s.plan()  # a refused attempt with HEAD at the parent may be retried
    assert second["status"] == "ok" and second["attempt"] == 2, second
    assert second["boundary_ref"].endswith(f"{f.key}-a2")
    f.s.side.prepared(
        "1", key=f.key, attempt=2, parent=f.parent,
        paths=second["pathspec_file"]["sha256"], accepted=",".join(second["accepted"]),
    )  # fmt: skip
    wt2 = f"{PIN}/plan1/boundary-wt/{f.key}-a2"
    assert wt2 != f.worktree_ref  # one sibling name per attempt, never a reused one
    new_tree = take_snapshot(repo)
    assert new_tree != first_pin

    with pytest.raises(PinConflict):  # a retry that reuses the old name is refused
        pin_once(repo, f.worktree_ref, new_tree)
    assert repo.git("rev-parse", f.worktree_ref).strip() == first_pin
    pin_once(repo, wt2, new_tree)
    pin_once(repo, wt2, new_tree)  # the same target again is not a conflict
    assert repo.git("rev-parse", f.worktree_ref).strip() == first_pin
    assert repo.git("rev-parse", wt2).strip() == new_tree
    # git itself refuses to move a create-only pin
    code, _ = repo.git("update-ref", f.worktree_ref, new_tree, ZERO, check=False)
    assert code != 0


def test_git_gc_prunes_an_unpinned_snapshot_but_not_a_pinned_one(flow, repo):
    f = flow()
    repo.write("src/b.py", "person: control edit, never pinned\n")
    unpinned = take_snapshot(repo)
    repo.write("src/b.py", PERSON_UNSTAGED)
    person_edits(repo)
    before = states(repo)
    f.ready(pin_worktree=False)
    pinned = pin_worktree(f)
    interrupt(f, f.hook, "sigkill")
    assert (
        repo.git("stash", "list").strip() == ""
    )  # no stash entry holds the edits either

    repo.git("gc", "-q", "--prune=now")

    assert repo.git("cat-file", "-t", pinned).strip() == "tree"
    assert repo.git("show", f"{f.worktree_ref}:src/b.py") == PERSON_UNSTAGED
    code, _ = repo.git("cat-file", "-e", unpinned, check=False)
    assert code != 0  # the control: without a pin the snapshot is gone
    res = f.verify(None)
    recover(repo, f.worktree_ref, res["outside_paths"])
    os.remove(repo.work / "gone.txt")
    assert states(repo) == before


# =============================================================================================
# The emulator against the real framework (skipped without pre-commit; FR-118)
# =============================================================================================
def prepared_pair(tmp_path, kind):
    """A repository whose pre-commit hook is the emulator or the real framework."""
    from .conftest import HookEmulator

    repo = Repo(tmp_path / kind)
    emulator = HookEmulator(repo, tmp_path / f"{kind}-hook")
    if kind == "real":
        repo.write(
            ".pre-commit-config.yaml",
            "repos:\n- repo: local\n  hooks:\n  - id: emu-action\n    name: emu-action\n"
            f"    entry: sh {emulator.action_script}\n"
            "    language: system\n    pass_filenames: false\n    always_run: true\n",
        )
    for rel in ("a.txt", "b.txt", "sw.txt", "gone.txt", "run.sh", "c.txt"):
        repo.write(rel, rel[0] + "\n")
    repo.commit("add files")
    if kind == "real":
        done = subprocess.run(
            ["pre-commit", "install", "--overwrite"],
            cwd=repo.work, capture_output=True, text=True,
        )  # fmt: skip
        assert done.returncode == 0, done.stderr
    repo.write("a.txt", "a changed by the task\n")
    return repo, emulator


def observe(repo, emulator, patch_dir, scenario):
    head = repo.git("rev-parse", "HEAD").strip()
    if scenario == "skip-worktree":
        repo.git("update-index", "--skip-worktree", "sw.txt")
        repo.write("sw.txt", PERSON_SW)
        repo.write("c.txt", "visible unstaged edit\n")
    else:  # a deletion and a mode change outside S
        os.remove(repo.work / "gone.txt")
        os.chmod(repo.work / "run.sh", 0o755)
        repo.write("b.txt", PERSON_UNSTAGED)
    emulator.set_action("pass" if scenario != "sigterm-group" else "block")
    if scenario == "sigterm-group":
        proc = emulator.start_blocked_commit(["a.txt"])
        emulator.kill_group(proc, signal.SIGTERM)
        code = proc.returncode
    else:
        code = emulator.commit(["a.txt"]).returncode
    names = ("a.txt", "b.txt", "c.txt", "sw.txt", "gone.txt", "run.sh")
    return {
        "returncode": code,
        "head_moved": repo.git("rev-parse", "HEAD").strip() != head,
        "files": states(repo, names),
        "patches": len(list(patch_dir.glob("patch*"))) if patch_dir.is_dir() else 0,
        "lock": (repo.work / ".git" / "index.lock").exists(),
    }


@pytest.mark.real_framework
@pytest.mark.parametrize(
    "scenario", ["skip-worktree", "deletion-and-mode", "sigterm-group"]
)
def test_the_emulator_matches_the_real_framework_on_the_edit_cases(
    scenario, tmp_path, monkeypatch
):
    if shutil.which("pre-commit") is None:
        pytest.skip("pre-commit is not on PATH")
    real_home = tmp_path / "pre-commit-home"
    monkeypatch.setenv("PRE_COMMIT_HOME", str(real_home))
    emu_repo, emu = prepared_pair(tmp_path, "emulator")
    real_repo, real = prepared_pair(tmp_path, "real")

    expected = observe(emu_repo, emu, emu.cache, scenario)
    actual = observe(real_repo, real, real_home, scenario)

    assert actual == expected
    assert expected["patches"] == 1  # the equality is not vacuous: an edit was saved
