"""K4 (DESIGN 1.2, TESTING section 4): reviewers are read-only; the launcher checks the sandbox before and after every run."""

import subprocess

from panel_support import make_world


def test_dirty_after_run_is_flagged(tmp_roots):
    w = make_world(tmp_roots)
    clean = w.run("Z0", "clean")
    assert clean.returncode == 0, clean.stderr
    assert (
        clean.json("run.json")["sandbox_dirty"] is False
    )  # the control: a clean run is not flagged
    assert not (clean.dir / "sandbox-dirty.txt").exists()

    # a fake reviewer that writes a file in the sandbox (its working folder is SB/<doc>/repo)
    dirty = w.run("Z0", "dirty", env={"FAKE_WRITE": "stray-note.txt"})
    assert dirty.returncode == 3 and "sandbox_dirty" in dirty.stderr
    assert (w.sandbox / "stray-note.txt").is_file()
    run = dirty.json("run.json")
    assert run["sandbox_dirty"] is True
    assert "stray-note.txt" in (dirty.dir / "sandbox-dirty.txt").read_text()
    # the run is still finished and recorded (the merge ran), only flagged
    assert (dirty.dir / "timing.json").is_file() and run["merge_refused"] is False

    # K4 before the run: the dirty sandbox is refused, no reviewer starts, nothing is written
    n = len(tmp_roots.call_log.read_text().splitlines())
    again = w.run("Z0", "again")
    assert again.returncode == 2 and "E_SANDBOX_DIRTY" in again.stderr
    assert len(tmp_roots.call_log.read_text().splitlines()) == n
    assert not (again.dir / "run.json").exists()


def test_the_real_repository_is_not_touched(tmp_roots):
    """The scripts run git only inside the sandbox (K5): a run leaves the source repository's status and HEAD as they were."""
    w = make_world(tmp_roots)

    def state():
        out = subprocess.run(
            ["git", "-C", str(w.repo), "status", "--porcelain", "--ignored"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        head = subprocess.run(
            ["git", "-C", str(w.repo), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        return out, head

    before = state()
    r = w.run("SS", "ss")
    assert r.returncode == 0, r.stderr
    assert state() == before
