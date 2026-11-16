"""Integration tests of bin/run-panel.sh and bin/run-reviewer.sh with the fake claude (TESTING F-FAKE, section 3 rows I).

REQ-12 (b), REQ-23 (whole run), REQ-30 (kill, no retry, absent from the merge), DD-8, DD-9. No model is started: every
environment from tmp_roots has tests/fakes first on PATH, and the scripts refuse to run otherwise (last tests).
"""

import os
import subprocess
import sys

import pytest
from helpers import SW
from panel_support import (
    ANCHOR,
    EMBER,
    RIDS,
    RUN_REVIEWER,
    brief_shas,
    make_world,
)

sys.path.insert(0, str(SW))
from scaffold import briefs  # noqa: E402


def models_called(r):
    return [m for _, _, m in r.calls()]


def test_prepass_finishes_before_first_reviewer(tmp_roots):
    w = make_world(tmp_roots)
    r = w.run("SS", "ss")
    assert r.returncode == 0, r.stderr
    run = r.json("run.json")
    assert (run["arm"], run["fallback"], run["no_trigger"]) == ("SS", False, False)
    assert (r.dir / "prepass" / "prepass.json").is_file()
    t = r.json("timing.json")
    prepass_start, prepass_end = t["stage_t"]["prepass"]
    first_call = min(c[0] for c in r.calls())
    assert len(r.calls()) == 3
    assert t["t0"] <= prepass_start < prepass_end < first_call
    # every reviewer starts after the pre-pass and the render, and the clock covers the pre-pass (REQ-29)
    assert all(s >= t["stage_t"]["render"][1] for s in t["rev_start"].values())
    assert t["panel_elapsed_s"] >= t["prepass_s"] > 0
    # the SS brief is not the Z0 brief: it carries the ledger rule and the sheet, and CB-1 with the source path
    text = (r.dir / "briefs" / "t4-1.txt").read_text()
    assert "## SWEEP SHEET ITEMS" in text and "Driving document:" in text
    assert run["briefs"] == brief_shas(r.dir) and set(run["briefs"]) == set(RIDS)


def test_no_trigger_run(tmp_roots):
    w = make_world(tmp_roots, plan="p_clean.md")
    z0 = w.run("Z0", "z0")
    ss = w.run("SS", "ss")
    assert z0.returncode == 0 and ss.returncode == 0, ss.stderr
    run = ss.json("run.json")
    assert run["no_trigger"] is True and run["fallback"] is False
    z0_sha = set(brief_shas(z0.dir).values())
    assert len(z0_sha) == 1  # one brief text for the document, whichever reviewer
    assert set(brief_shas(ss.dir).values()) == z0_sha  # REQ-23: equal to Z0's by hash
    # no ledger was required: S5 did not run, so no ledger_missing is counted
    assert run["check_ran"] is False and run["check_skipped"] is False
    assert not (ss.dir / "check").exists()
    assert run["reviewer_status"] == {
        rid: {"model": m, "status": "ok"}
        for rid, m in (("t2b-1", EMBER), ("t4-1", "gpt-6-luna"), ("t3-1", "gpt-6-luna"))
    }


def killed_run(w, name, b=3):
    """Z0 run in which the ember reviewer sleeps 30 s and the hang guard is 1.5 * b."""
    return w.run(
        "Z0",
        name,
        env={"FAKE_SCENARIOS": f"{EMBER}=sleep", "FAKE_SLEEP_S": "30"},
    )


def test_sleeping_reviewer_killed(tmp_roots):
    w = make_world(tmp_roots, b=3)
    r = killed_run(w, "z0")
    assert r.returncode == 0, r.stderr
    st = r.json("run.json")["reviewer_status"]
    assert st["t2b-1"]["status"] == "killed"
    assert st["t4-1"]["status"] == st["t3-1"]["status"] == "ok"
    meta = r.json("reviews/t2b-1.meta.json")
    assert (
        meta["killed"] is True
        and meta["status"] == "killed"
        and meta["exit"] in (124, 137)
    )
    assert (
        meta["hang_s"] <= 4.5 and meta["wall_s"] < 6
    )  # killed at the guard, not after the 30 s sleep
    cost = r.json("reviews/t2b-1.cost.json")
    assert cost["killed"] is True and cost["hang_s"] == meta["hang_s"]
    assert len(cost["prompt_sha256"]) == 64
    assert not (r.dir / "reviews" / "t2b-1.md").exists()  # no accepted report
    assert r.json("run.json")["hang_s"] == 4.5  # 1.5 * (3 + 0) for arm Z0
    # the others finish; the clock's slowest reviewer is the killed one
    t = r.json("timing.json")
    assert t["slowest_reviewer_s"] >= meta["wall_s"] > 2
    assert r.json("reviews/t4-1.meta.json")["killed"] is False


@pytest.mark.parametrize(
    "scenario,status",
    [("api_error", "error"), ("wrong_model", "invalid"), ("exit127", "error")],
)
def test_no_retry_on_failure(tmp_roots, scenario, status):
    w = make_world(tmp_roots)
    r = w.run("Z0", "z0", env={"FAKE_SCENARIOS": f"gpt-6-luna={scenario}"})
    assert r.returncode == 0, r.stderr
    # DD-8: one call per reviewer, even after a failure; no second attempt and no other model
    assert sorted(models_called(r)) == sorted(
        ["muse-ember-1.0", "gpt-6-luna", "gpt-6-luna"]
    )
    assert not list((r.dir / "reviews").glob("*.attempt2*"))
    st = r.json("run.json")["reviewer_status"]
    assert (st["t4-1"]["status"], st["t3-1"]["status"], st["t2b-1"]["status"]) == (
        status,
        status,
        "ok",
    )
    assert not (r.dir / "reviews" / "t4-1.fallback.log").exists()
    assert r.json("reviews/t4-1.meta.json")["attempt"] == 1


def test_killed_reviewer_absent_from_merge(tmp_roots):
    w = make_world(tmp_roots, b=3)
    control = w.run("Z0", "ctl")  # nobody fails: every reviewer is in the merge
    assert control.returncode == 0, control.stderr
    ledger = (control.dir / "merged" / "ledger.json").read_text()
    assert (
        "t2b-1" in ledger and "t4-1" in ledger
    )  # the control proves the ids would show up
    r = killed_run(w, "killed")
    assert r.returncode == 0, r.stderr
    assert r.json("run.json")["merge_refused"] is False
    assert sorted(p.name for p in (r.dir / "normalised").glob("*.md")) == [
        "t3-1.md",
        "t4-1.md",
    ]
    res = r.json("resolution.json")["reviewers"]
    assert sorted(x["reviewer_id"] for x in res) == ["t3-1", "t4-1"]
    merged = (r.dir / "merged" / "ledger.json").read_text() + (
        r.dir / "merged" / "merged-1.md"
    ).read_text()
    assert "t2b-1" not in merged and "t4-1" in merged


def test_forced_exception_in_check_merges_as_written(tmp_roots):
    w = make_world(tmp_roots)
    # control: S5 runs and adds the telemetry key `class` to the line that carries a probe
    env = {"FAKE_PROBE": "first", "FAKE_ANCHOR": ANCHOR}
    ok = w.run("SS", "ok", env=env)
    assert ok.returncode == 0, ok.stderr
    assert ok.json("run.json")["check_ran"] is True
    assert '"class"' in (ok.dir / "check" / "t4-1.checked.md").read_text()
    # CHECK_SCOPE=bogus makes the real check raise (REQ-12 b): the run goes on without S5
    r = w.run("SS", "skipped", env=dict(env, CHECK_SCOPE="bogus"))
    assert r.returncode == 0, r.stderr
    run = r.json("run.json")
    assert (
        run["check_skipped"] is True
        and run["check_ran"] is False
        and run["fallback"] is False
    )
    assert "ValueError" in (r.dir / "check" / "error.log").read_text()
    assert not (r.dir / "check" / "check.json").exists()
    assert (
        run["merge_refused"] is False and (r.dir / "merged" / "merged-1.md").is_file()
    )
    for rid in RIDS:  # the text given to the merge is the raw reviewer text
        raw = (r.dir / "reviews" / f"{rid}.md").read_text()
        assert (r.dir / "normalised" / f"{rid}.md").read_text() == raw
        assert '"class"' not in raw
    # S5 skipped, the clock still has its S5 stage (about 0 s)
    assert r.json("timing.json")["s5_s"] < 0.5


def test_order_s5_then_h2_then_merge(tmp_roots):
    w = make_world(tmp_roots)
    r = w.run("SS", "ss", env={"FAKE_SCENARIOS": f"{EMBER}=long_anchor"})
    assert r.returncode == 0, r.stderr
    d = r.dir
    check = [p.stat().st_mtime_ns for p in (d / "check").iterdir()]
    h2 = [p.stat().st_mtime_ns for p in (d / "normalised").iterdir()]
    merged = (d / "merged" / "merged-1.md").stat().st_mtime_ns
    assert check and h2 and max(check) < min(h2) and max(h2) < merged
    # S5 read the raw report (the 250-character anchor); H2 cut it afterwards, in the report that went to the merge
    raw_anchor = "x" * 250
    assert raw_anchor in (d / "reviews" / "t2b-1.md").read_text()
    assert raw_anchor in (d / "check" / "t2b-1.checked.md").read_text()
    norm = (d / "normalised" / "t2b-1.md").read_text()
    assert raw_anchor not in norm and "x" * 200 in norm
    h2_json = r.json("normalised/h2.json")
    assert h2_json["reports"]["t2b-1"]["changed"][0]["fields"] == ["anchor"]
    assert r.json("run.json")["reviewer_status"]["t2b-1"]["status"] == "ok"


def test_no_source_run(tmp_roots):
    w = make_world(tmp_roots, source=False)
    assert not (w.cand / "source.md").exists()
    cb1 = (
        (SW / "briefs" / "cb1.txt")
        .read_text()
        .strip()
        .split("{{SOURCE_ABS}}")[0]
        .strip()
    )
    assert len(cb1) >= 12
    # the snippet is what CB-1 contributes: a brief made with a source holds it
    with_src = briefs.render(
        "Z0", {"cand_sb": "/x/c.md", "sha": "0" * 64}, None, "/x/source.md"
    )
    assert cb1 in with_src["text"]
    r = w.run("SS", "ss")
    assert r.returncode == 0, r.stderr
    run = r.json("run.json")
    assert run["no_source"] is True and run["source_sha256"] is None
    shas = brief_shas(r.dir)
    assert set(shas) == set(RIDS)
    for rid in RIDS:
        assert cb1 not in (r.dir / "briefs" / f"{rid}.txt").read_text()
    # E5 had no source, so the pre-pass marks it not applicable (when it ran) or fell back
    assert run["fallback"] is False
    assert r.json("prepass/prepass.json")["no_source"] is True


def test_reviewer_unavailable_reassigns_with_one_replica(tmp_roots):
    w = make_world(tmp_roots)
    r = w.run("SS", "ss", args=("--unavailable", "t3-1"))
    assert r.returncode == 0, r.stderr
    run = r.json("run.json")
    assert run["reviewers"] == 2 and run["reviewers_unavailable"] == ["t3-1"]
    asg = r.json("prepass/assignment.json")
    assert sorted(asg["reviewers"]) == ["t2b-1", "t4-1"]
    assert set(asg["replicas"].values()) == {
        1
    }  # fewer than three reviewers: every item has one replica
    assert sorted(m for _, _, m in r.calls()) == ["gpt-6-luna", "muse-ember-1.0"]
    assert not (r.dir / "briefs" / "t3-1.txt").exists()


def test_ss_refused_without_time_budget(tmp_roots):
    w = make_world(tmp_roots, b=40)  # 0.35 * 40 - 13 = 1 s of budget, under 8 s
    r = w.run("SS", "ss")
    assert r.returncode == 4 and "no_budget" in r.stderr
    assert r.json("run.json")["no_budget"] is True
    assert r.calls() == []
    z0 = w.run("Z0", "z0")  # the other arms are not refused
    assert z0.returncode == 0, z0.stderr


def test_refuses_a_counted_run_in_a_used_folder(tmp_roots):
    w = make_world(tmp_roots)
    assert w.run("Z0", "z0").returncode == 0
    n = len(tmp_roots.call_log.read_text().splitlines())
    again = w.run("Z0", "z0")
    assert again.returncode == 2 and "E_RUN_EXISTS" in again.stderr
    assert len(tmp_roots.call_log.read_text().splitlines()) == n


def test_refuses_without_nofallback_and_a_verifier(tmp_roots):
    w = make_world(tmp_roots)
    env = {k: v for k, v in tmp_roots.with_env().items() if k != "NOFALLBACK"}
    r = subprocess.run(
        ["bash", str(SW / "bin" / "run-panel.sh"), "--arm", "Z0", "--panel", "primary", "--doc", w.doc,
         "--run", str(tmp_roots.runs / "x")],
        capture_output=True, text=True, env=env,
    )  # fmt: skip
    assert r.returncode == 2 and "E_NOFALLBACK" in r.stderr
    v = w.run("Z0", "v", env={"VERIFIER": "1"})
    assert v.returncode == 2 and "E_VERIFIER" in v.stderr
    assert v.calls() == []
    assert "VERIFIER=${VERIFIER:-0}" in (SW / "bin" / "run-panel.sh").read_text()


def reviewer(roots, *, model, env_extra=None, path=None, nofallback=True):
    """Call run-reviewer.sh directly with a brief on stdin; nothing is built, so every refusal must come first."""
    env = roots.with_env()
    env.update(env_extra or {})
    if path is not None:
        env["PATH"] = path
    if not nofallback:
        env.pop("NOFALLBACK")
    return subprocess.run(
        [
            "bash",
            str(RUN_REVIEWER),
            str(roots.runs / "r"),
            "TASK-WF-x-1",
            "t4-1",
            model,
            "30",
        ],
        input="brief text\n",
        capture_output=True,
        text=True,
        env=env,
    )


def test_refuses_model_outside_the_allowlist(tmp_roots):
    for bad in ("claude-opus-5-5", "Qwen3.8-max", "glm-5.3", "muse-ember-1.0 x"):
        r = reviewer(tmp_roots, model=bad)
        assert r.returncode == 2 and "E_MODEL" in r.stderr, bad
    assert not tmp_roots.call_log.exists()  # no call reached claude
    r = reviewer(tmp_roots, model="gpt-6-luna", nofallback=False)
    assert r.returncode == 2 and "E_NOFALLBACK" in r.stderr
    assert not tmp_roots.call_log.exists()


def test_no_model_starts_when_a_fake_variable_is_set_and_claude_is_not_the_fake(
    tmp_roots,
):
    marker = tmp_roots.root / "real-claude-started"
    stub_dir = tmp_roots.root / "bin"
    stub_dir.mkdir()
    stub = stub_dir / "claude"
    stub.write_text(f"#!/usr/bin/env bash\ntouch {marker}\n")
    stub.chmod(0o755)
    path = f"{stub_dir}{os.pathsep}{os.environ['PATH']}"
    r = reviewer(tmp_roots, model="gpt-6-luna", path=path)
    assert r.returncode == 2 and "E_NOT_FAKE" in r.stderr
    assert not marker.exists()
