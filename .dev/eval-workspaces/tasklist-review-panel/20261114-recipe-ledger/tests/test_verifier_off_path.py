"""REQ-46: the optional verifier never sits on the critical path, cannot add claims, and its time is excluded. It is not
built; these tests guard the seam."""

import inspect
import re
import subprocess

import pytest
from panel_support import SCRIPT, ok_runs, run_panel, sandbox  # noqa: F401  (session fixtures)

from scaffold import clock


def test_no_verifier_step_in_clock():
    text = SCRIPT.read_text(encoding="utf-8")
    code = [ln for ln in text.splitlines() if not ln.lstrip().startswith("#")]
    hits = [ln for ln in code if re.search("verif", ln, re.I)]
    # the only code lines that name it: the default and the refusal of any other value
    assert (
        len(hits) == 2
        and "VERIFIER=${VERIFIER:-0}" in hits[0]
        and "E_VERIFIER" in hits[1]
    ), hits
    for name in (
        *inspect.signature(clock.timing_record).parameters,
        *inspect.signature(clock.panel_elapsed_s).parameters,
    ):
        assert "verif" not in name


@pytest.mark.slow
def test_verifier_default_off(ok_runs, sandbox):  # noqa: F811
    assert ok_runs.rl.js("run.json")["verifier"] == 0
    r = run_panel(sandbox, env={"VERIFIER": "1"})
    assert r.rc == 2 and "E_VERIFIER" in r.err and r.calls == [] and not r.run.exists()
    assert (
        subprocess.run(
            ["grep", "-c", "VERIFIER=${VERIFIER:-0}", str(SCRIPT)], capture_output=True
        ).stdout.strip()
        == b"1"
    )


@pytest.mark.slow
def test_verifier_time_excluded(ok_runs):  # noqa: F811
    timing = ok_runs.z0.js("timing.json")
    assert "verifier_s" not in timing
    last = max(timing["rev_end"].values())
    assert timing["panel_elapsed_s"] == round(last - timing["t0"], 3)
    # a verifier second added to a record changes nothing: the clock reads reviewer and check stamps only
    with_verifier = dict(timing, verifier_s=99.0)
    assert (
        clock.panel_elapsed_s("Z0", with_verifier["t0"], with_verifier["rev_end"])
        == timing["panel_elapsed_s"]
    )
    rl = ok_runs.rl.js("timing.json")
    assert (
        clock.panel_elapsed_s(
            "RL", rl["t0"], rl["rev_end"], r3_end=rl["t0"] + rl["panel_elapsed_s"]
        )
        == rl["panel_elapsed_s"]
    )
    assert "verifier_s" not in rl
