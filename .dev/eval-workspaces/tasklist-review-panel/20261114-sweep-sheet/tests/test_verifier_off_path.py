"""REQ-46: the optional verifier never sits on the critical path, cannot add claims, and its time is excluded.
The verifier itself is not built; these tests guard the seam."""

import json
import re
import subprocess

import pytest
from helpers import SW

from analysis import analyze
from fixtures.runs import make_runs
from scaffold import clock

RUN_PANEL = SW / "bin" / "run-panel.sh"


def test_no_verifier_step_in_clock():
    # the clock times three stages; a verifier stage is refused, and timing.json has no verifier field
    assert "verifier" not in " ".join(clock.PanelClock.STAGES).lower()
    pc = clock.PanelClock("SS", now=iter([0.0, 1.0, 2.0, 3.0, 4.0]).__next__)
    pc.start()
    with pytest.raises(clock.ClockError, match="unknown stage verifier"):
        pc.stage_start("verifier")
    assert "verifier" not in clock.PanelClock.__doc__.lower()
    # the launcher: every mention is a comment, the default, or the refusal; there is no step that runs one
    for n, line in enumerate(RUN_PANEL.read_text().splitlines(), 1):
        if re.search(r"verifier", line, re.I):
            assert re.match(
                r"\s*#|VERIFIER=\$\{VERIFIER:-0\}$|\[ \"\$VERIFIER\" = 0 \]", line
            ), (n, line)


def test_verifier_default_off(tmp_roots):
    assert "VERIFIER=${VERIFIER:-0}" in RUN_PANEL.read_text().splitlines()
    # any other value is refused before anything runs
    r = subprocess.run(
        [
            "bash",
            str(RUN_PANEL),
            "--arm",
            "Z0",
            "--panel",
            "primary",
            "--doc",
            "d",
            "--run",
            str(tmp_roots.root / "r"),
        ],
        capture_output=True,
        text=True,
        env=tmp_roots.with_env(VERIFIER="1"),
    )
    assert r.returncode == 2 and "E_VERIFIER" in r.stderr
    assert not (tmp_roots.root / "r").exists()


def test_verifier_time_excluded(tmp_path):
    # the clock: time that passes after the last reviewer (a verifier, H2, the merge, the judge) is not panel time
    ticks = iter(
        [100.0, 100.0, 130.0, 130.0, 150.0]
    )  # t0, start A, end A, start B, end B
    pc = clock.PanelClock("Z0", now=ticks.__next__)
    pc.start()
    pc.reviewer_start("a")
    pc.reviewer_end("a")
    pc.reviewer_start("b")
    pc.reviewer_end("b")
    t = pc.timing()
    assert t["panel_elapsed_s"] == 50.0 and "verifier_s" not in t
    assert clock.panel_elapsed_s("Z0", 100.0, {"a": 130.0, "b": 150.0}) == 50.0
    # the analysis: a `verifier_s` in timing.json is not in the elapsed time, and it adds no finding
    w = make_runs.build_stage_runs(tmp_path)
    before = {r.name: r for r in analyze.load_runs(w.runs)}["z0-stage-r1"]
    timing = w.runs / "z0-stage-r1" / "timing.json"
    data = json.loads(timing.read_text())
    timing.write_text(json.dumps({**data, "verifier_s": 30.0}))
    after = {r.name: r for r in analyze.load_runs(w.runs)}["z0-stage-r1"]
    assert before.elapsed == after.elapsed == 100.0
    assert analyze.nonprobe_findings(before) == analyze.nonprobe_findings(after)
    assert analyze.elapsed_s(after) == 100.0
