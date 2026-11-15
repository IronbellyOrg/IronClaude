"""K4: the sandbox is read only. The launcher checks `git status --porcelain` before and after a run (DESIGN 8 row 5)."""

import os
import subprocess

import pytest
from conftest import FAKES
from panel_support import EMBER, L1, L2, own_sandbox, run_panel  # noqa: F401

pytestmark = pytest.mark.slow


def test_dirty_after_run_is_flagged(own_sandbox, tmp_path):  # noqa: F811
    box = own_sandbox
    wrap = tmp_path / "wrap"
    wrap.mkdir()
    # a fake reviewer that writes a file into the sandbox repo (its working folder) and then answers as the fake does
    (wrap / "claude").write_text(
        f'#!/usr/bin/env bash\necho x >reviewer-notes.txt\nexec {FAKES}/claude "$@"\n'
    )
    (wrap / "claude").chmod(0o755)
    r = run_panel(box, arm="Z0")
    assert r.rc == 0, r.err  # the control: a clean run leaves a clean sandbox
    assert r.js("run.json")["sandbox_dirty"] is False
    r = run_panel(
        box, arm="Z0", env={"PATH": f"{wrap}{os.pathsep}{os.environ['PATH']}"}
    )
    assert (box.repo / "reviewer-notes.txt").is_file()
    run = r.js("run.json")
    assert run["sandbox_dirty"] is True  # flagged
    assert r.rc == 2 and "E_SANDBOX_DIRTY" in r.err
    assert (
        sorted(run["reviewers"]) == sorted([EMBER, L1, L2])
        and (r.run / "merged" / "merged-1.md").is_file()
    )
    # the next run is refused until the sandbox is rebuilt
    again = run_panel(box, arm="Z0")
    assert again.rc == 2 and "E_SANDBOX_DIRTY" in again.err and again.calls == []


def test_dirty_before_run_is_refused(own_sandbox):  # noqa: F811
    box = own_sandbox
    subprocess.run(["bash", "-c", f"echo x >{box.repo}/stray.txt"], check=True)
    r = run_panel(box)
    assert (
        r.rc == 2
        and "E_SANDBOX_DIRTY" in r.err
        and r.calls == []
        and not r.run.exists()
    )


def test_missing_sandbox_is_refused(own_sandbox):  # noqa: F811
    box = own_sandbox
    subprocess.run(["rm", "-rf", str(box.repo)], check=True)
    r = run_panel(box)
    assert r.rc == 2 and "E_SANDBOX" in r.err and r.calls == []
