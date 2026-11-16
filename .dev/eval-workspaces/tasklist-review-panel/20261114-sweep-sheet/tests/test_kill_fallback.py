"""REQ-18 (DESIGN 12.2) and REQ-12 (a): the pre-pass kill limit and the fallback. Task 26 holds the formula, Task 27 the rest."""

import time

import pytest
from panel_support import RIDS, brief_shas, make_world

from scaffold.clock import kill_s


def test_kill_formula():
    assert kill_s(100) == 10.0
    assert kill_s(122) == 12.2
    assert kill_s(200) == 15.0
    assert kill_s(150) == 15.0  # 0.10 b reaches the 15 s cap at b = 150


def z0_sha(w):
    """The sha256 of the Z0 brief of the document (one text for every reviewer)."""
    z0 = w.run("Z0", "z0")
    assert z0.returncode == 0, z0.stderr
    shas = set(brief_shas(z0.dir).values())
    assert len(shas) == 1
    return shas.pop()


def test_sleeping_stub_is_killed_and_falls_back(tmp_roots):
    w = make_world(tmp_roots)
    expected = z0_sha(w)
    t = time.monotonic()
    r = w.run("SS", "ss", env={"SW_PREPASS_CMD": "sleep 5", "SW_KILL_S": "1"})
    wall = time.monotonic() - t
    assert r.returncode == 0, r.stderr
    tm = r.json("timing.json")
    # the process group was killed after about 1 s, not after the 5 s of the stub
    assert 0.9 <= tm["prepass_s"] < 2.5, tm["prepass_s"]
    assert wall < 30
    assert not (r.dir / "prepass").exists() and not (r.dir / "prepass.tmp").exists()
    run = r.json("run.json")
    assert (run["fallback"], run["reason"], run["no_trigger"]) == (True, "kill", False)
    # the run used the Z0 brief: the same sha256 for every reviewer
    assert set(brief_shas(r.dir).values()) == {expected}
    assert set(run["briefs"]) == set(RIDS) and set(run["briefs"].values()) == {expected}
    # the run stays in arm SS and its reviewers all ran (intention to treat); no check ran
    assert (
        run["arm"] == "SS"
        and run["check_ran"] is False
        and not (r.dir / "check").exists()
    )
    assert len(r.calls()) == 6  # 3 for the Z0 control run, 3 here
    assert all(v["status"] == "ok" for v in run["reviewer_status"].values())
    assert (
        run["merge_refused"] is False and (r.dir / "merged" / "merged-1.md").is_file()
    )


@pytest.mark.parametrize(
    "env,reason",
    [
        ({"SW_PREPASS_CMD": "false"}, "error"),  # the pre-pass raises (DESIGN 10 row 1)
        ({"SW_RENDER_CMD": "false"}, "render"),  # the SS brief render raises
    ],
    ids=["prepass", "render"],
)
def test_forced_exception_in_prepass_and_render_falls_back(tmp_roots, env, reason):
    w = make_world(tmp_roots)
    expected = z0_sha(w)
    r = w.run("SS", "ss", env=env)
    assert r.returncode == 0, r.stderr
    run = r.json("run.json")
    assert (run["fallback"], run["reason"], run["arm"]) == (True, reason, "SS")
    assert set(brief_shas(r.dir).values()) == {
        expected
    }  # REQ-23: the fallback brief equals Z0's by hash
    assert not (r.dir / "prepass").exists() and not (r.dir / "prepass.tmp").exists()
    assert run["check_ran"] is False and run["check_skipped"] is False
    assert len(r.calls()) == 6 and all(
        v["status"] == "ok" for v in run["reviewer_status"].values()
    )
    assert (r.dir / "merged" / "merged-1.md").is_file()
    # the decision was taken before any reviewer started: the clock has the failed stage, then the reviewers
    tm = r.json("timing.json")
    assert tm["stage_t"]["prepass"][1] <= min(tm["rev_start"].values())
    assert tm["s5_s"] < 0.5
