"""Fault injection (DESIGN 6.2): one test per failure mode, all with the fake `claude`."""
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time

from conftest import BIN, CAND_A, CONTROL, PKGS, PY, R2, report, run

sys.path.insert(0, str(PY))
import summarize_arm as SA  # noqa: E402

P = CONTROL
LS = {"tool": "Bash", "input": {"command": "ls"}, "response": {"stdout": "x"}}
BAD_SEV = {"id": "F2", "severity": "HIGH", "blocking": True, "category": "other", "anchor": CAND_A, "refs": [], "claim": "bad"}
GOOD = {"id": "F1", "severity": "MAJOR", "blocking": True, "category": "contradiction", "anchor": CAND_A, "refs": [], "claim": "ok"}


def values(world, **kw):
    v = {"panel": "EL2", "pkg": P, "B_f": 20, "turn_p90_crit": 1, "T_report_p90_crit": 1, "E_recv": 10, "turn_p90_recv": 1,
         "T_report_p90_recv": 1, "hooks_s": 2, "panel_finish_at_s": 60, "k": 2, "sweeper_kill_s": 50, "hang_s": 60,
         "source": "test", "n_runs": 0}
    v.update(kw)
    f = world.tmp / f"values-{len(list(world.tmp.glob('values-*')))}.json"
    f.write_text(json.dumps(v))
    return f


def pkg_run(world, vals, collab=1, panel="EL2", row="r", runid="abcd0001", timeout=180):
    run(["bash", str(BIN / "build-sandbox.sh"), P], env=world.env, check=True)
    r = run(["bash", str(BIN / "run-package.sh"), "--row", row, "--runid", runid, "--pkg", P, "--panel", panel,
             "--values", str(vals), "--collab", str(collab)], env=world.env, timeout=timeout)
    pd = world.out / "runs" / row / P
    return r, pd


def meta(pd, rid):
    return json.loads((pd / f"reviews/{rid}.meta.json").read_text())


def collab(pd):
    return json.loads((pd / "collab.json").read_text())


def luna(**kw):
    e = {"tool_calls": [LS] * 8, "report": report()}
    e.update(kw)
    return e


# ---------------------------------------------------------------- snapshot, board, hook crash, env (hook level)

def _two_receivers(world):
    world.board(k=2)
    world.seed(*[{"items": ["tests/test_other.py"]}] * 4)
    return world.hook_settings("t4-1", 0), world.hook_settings("t3-1", 1)


def test_snapshot_not_written(world):
    s0, s1 = _two_receivers(world)
    for _ in range(6):
        world.call_hook(s1)                       # t3-1 seals and receives before the fault
    os.chmod(world.B / "snap", 0o500)
    try:
        outs = [world.call_hook(s0) for _ in range(10)]
        outs1 = [world.call_hook(s1) for _ in range(3)]
    finally:
        os.chmod(world.B / "snap", 0o700)
    assert outs == [""] * 10 and not (world.B / "state/t4-1.delivered").exists()
    assert [m["ev"] for m in world.metrics("t4-1")].count("snapshot_missing") == 1
    assert len((world.B / "state/t3-1.delivered").read_text().split()) == 2 and any(outs1)


def test_snapshot_hash_fails(world):
    s0, s1 = _two_receivers(world)
    (world.B / "snap/t4-1.sha256").mkdir()
    outs = [world.call_hook(s0) for _ in range(10)]
    assert outs == [""] * 10 and (world.B / "state/t4-1.snapfail").exists()
    assert any(m["ev"] == "snapshot_missing" for m in world.metrics("t4-1"))
    assert any(world.call_hook(s1) for _ in range(6))


def test_corrupt_board_line(world):
    world.board()
    with open(world.B / "msgs/board.jsonl", "a") as f:
        f.write("{not json\n")
    s = world.hook_settings()
    outs = [world.call_hook(s) for _ in range(7)]       # call_hook asserts exit 0
    assert outs == [""] * 7 and any(m["ev"] == "hook_error" for m in world.metrics("t4-1"))


def test_hook_crash_missing_jq(world):
    world.board()
    world.seed({"items": ["tests/test_other.py"]})
    s = world.hook_settings(jq="/nonexistent/jq")
    assert [world.call_hook(s) for _ in range(7)] == [""] * 7
    assert all(m["ev"] == "hook_error" for m in world.metrics("t4-1"))


def test_environment_cleared(world):
    world.board()
    world.seed({"items": ["tests/test_other.py"]})
    s = world.hook_settings()
    outs = [world.call_hook(s, envi=True) for _ in range(6)]
    assert "Search result to check yourself" in outs[-1]


# ---------------------------------------------------------------- sweeper

def _posts(n):
    return [["--move", "M1", "--cmd", f"grep -rln w{i} tests/", "--item", "tests/test_other.py"] for i in range(n)]


def test_sweeper_floods(world):
    world.scenario_set({"muse-ember-1.0#sw": {"posts": _posts(6), "report": "done"},
                        "gpt-6-luna": luna(sleep_before=2, tool_calls=[LS] * 12), "default": {"report": report()}})
    r, pd = pkg_run(world, values(world, k=2))
    assert r.returncode == 0, r.stderr
    c = collab(pd)
    assert c["sweeper"]["facts_posted"] == 4 and c["sweeper"]["over_cap"] == 2
    assert all(v["msgs_received"] <= 2 for v in c["reviewers"].values())
    assert sum(v["msgs_received"] for v in c["reviewers"].values()) == 4


def test_facts_after_luna_finished(world):
    world.scenario_set({"muse-ember-1.0#sw": {"sleep_before": 3, "posts": _posts(2), "report": "done"},
                        "gpt-6-luna": luna(), "default": {"report": report()}})
    r, pd = pkg_run(world, values(world, k=2))
    c = collab(pd)
    assert c["reviewers"]["t4-1"]["late"] == 1 and c["reviewers"]["t3-1"]["late"] == 1
    assert sorted(c["isolated_for"]) == ["t3-1", "t4-1"]


def test_receiver_cites_unrun_fact(world):
    world.scenario_set({"muse-ember-1.0#sw": {"posts": _posts(2), "report": "done"},
                        "gpt-6-luna": luna(sleep_before=2, report=report([{**GOOD, "refs": ["{DELIVERED_PATH}"]}])),
                        "default": {"report": report()}})
    r, pd = pkg_run(world, values(world, k=1))
    rv = collab(pd)["reviewers"]
    assert sum(v["peer_lines"] for v in rv.values()) == 2
    assert sum(v["peer_lines_first_hand"] for v in rv.values()) == 0


def test_rerun_mismatch(world):
    world.scenario_set({"muse-ember-1.0#sw": {"posts": _posts(2), "report": "done"},
                        "gpt-6-luna": luna(sleep_before=2, rerun_delivered=True, rerun_output="tests/test_app.py\n"),
                        "default": {"report": report()}})
    r, pd = pkg_run(world, values(world, k=1))
    rv = collab(pd)["reviewers"]
    assert sum(v["reruns"] for v in rv.values()) == 2 and sum(v["rerun_mismatches"] for v in rv.values()) == 2
    row = {"row": "x", "wrong_blockers": 0, "collab": {"own_line_jaccard": {}, "echo_rate": {}, "reruns": 100, "rerun_mismatches": 11},
           "per_package": {}}
    assert "rerun_mismatch" in SA.summarize([row], [])["reasons"]


def test_ember_review_ends_late(world):
    world.scenario_set({"muse-ember-1.0#sw": {"posts": _posts(1)}, "muse-ember-1.0": {"sleep_before": 3, "report": report()},
                        "default": luna()})
    r, pd = pkg_run(world, values(world, sweeper_kill_s=12))
    sm = json.loads((pd / "sweeper/sw-1.meta.json").read_text())
    assert sm["skipped_late"] and not (pd / "sweeper/sw-1.json").exists()
    assert collab(pd)["sweeper"]["skipped_late"]
    assert [x for x in world.argv_log() if x["rid"] == "sw"] == []


def test_sweeper_overruns(world):
    world.scenario_set({"muse-ember-1.0#sw": {"hang": True}, "default": luna()})
    v = values(world, sweeper_kill_s=13)
    r, pd = pkg_run(world, v)
    sm = json.loads((pd / "sweeper/sw-1.meta.json").read_text())
    t0 = int((pd / "t0").read_text())
    assert sm["exit"] == 124 and sm["killed"]
    assert abs(sm["end_ms"] - (t0 + 13_000)) < 1000


def test_sweeper_misrouted(world):
    world.scenario_set({"muse-ember-1.0#sw": {"model_reported": "gpt-6.1-terra", "report": "done"}, "default": luna()})
    r = world.launch("--panel", "EL2", "--row", "mis", "--packages", P, "--planning-values")
    pd = world.out / "runs/mis" / P
    assert r.returncode == 1
    assert json.loads((pd / "sweeper/sw-1.meta.json").read_text())["model_ok"] is False
    assert "sweeper model_ok false" in (pd / "INVALID").read_text()


def test_reviewer_misrouted(world):
    world.scenario_set({"gpt-6-luna": luna(model_reported="gpt-6.1-terra"), "default": luna()})
    r, pd = pkg_run(world, values(world), collab=0)
    assert r.returncode == 1 and "reviewer t4-1 invalid" in (pd / "INVALID").read_text()
    for rid in ("t4-1", "t3-1"):
        assert meta(pd, rid)["attempts"] == 2 and not meta(pd, rid)["model_ok"]
    requested = {x["argv"][x["argv"].index("--model") + 1] for x in world.argv_log()}
    assert requested == {"gpt-6-luna", "muse-ember-1.0"}  # no fallback model was ever asked for


def _luna_hangs(world, collab):
    world.scenario_set({"gpt-6-luna#t4-1": {"hang": True}, "gpt-6-luna": {"hang": True}, "default": luna()})
    r, pd = pkg_run(world, values(world, hang_s=6, k=0), collab=collab, row=f"h{collab}")
    t0 = int((pd / "t0").read_text())
    m = meta(pd, "t4-1")
    assert m["hang_kill"] and m["slo_breach"] and m["attempts"] == 1 and m["retry_skipped_deadline"]
    assert abs(m["end_ms"] - (t0 + 6000)) < 1000
    assert json.loads((pd / "collab.json").read_text())["slo_breach"] is True


def test_luna_hangs_collab(world):
    _luna_hangs(world, 1)


def test_luna_hangs_isolated(world):
    _luna_hangs(world, 0)


def test_block_check_fails_retry_isolated(world):
    world.scenario_set({"gpt-6-luna#t4-1": luna(report="no block here"), "gpt-6-luna#t3-1": luna(),
                        "muse-ember-1.0#sw": {"posts": _posts(2), "report": "done"}, "default": luna()})
    r, pd = pkg_run(world, values(world, k=2))
    assert r.returncode == 0, (pd / "INVALID").read_text() if (pd / "INVALID").exists() else r.stderr
    m = meta(pd, "t4-1")
    assert m["attempt"] == 2 and m["retry_isolated"] and m["attempts"] == 2
    luna_calls = [x for x in world.argv_log() if x["argv"][x["argv"].index("--model") + 1] == "gpt-6-luna"]
    second = [x for x in luna_calls if x["rid"] is None]
    assert len(second) == 1 and "--settings" not in second[0]["argv"]
    a2 = json.loads((pd / "reviews/t4-1.attempt2.json").read_text())
    assert [e for e in a2 if e.get("subtype") == "hook_additional_context"] == []
    c = collab(pd)
    assert "t4-1" in c["isolated_for"] and c["reviewers"]["t4-1"]["retry_isolated"]
    t0 = int((pd / "t0").read_text())
    assert c["elapsed_s"] * 1000 >= m["end_ms"] - t0 - 5


def test_h2_reask(world):
    world.scenario_set({"gpt-6-luna@resume": {"report": report([GOOD, {**BAD_SEV, "id": "F3"}])},
                        "gpt-6-luna": luna(report=report([GOOD, BAD_SEV])), "default": luna()})
    r, pd = pkg_run(world, values(world), collab=0)
    resumes = [x for x in world.argv_log() if "--resume" in x["argv"]]
    assert len(resumes) == 2  # one per luna
    a = resumes[0]["argv"]
    assert a[a.index("--output-format") + 1] == "stream-json" and "--verbose" in a and "--settings" not in a
    m = meta(pd, "t4-1")
    assert m["reask"] and m["reask_s"] > 0 and m["dropped_lines"] == 1 and m["reask_model_ok"]
    assert (pd / "reviews/t4-1.reask.jsonl").exists() and (pd / "reviews/t4-1.pre-reask.md").exists()


def test_reask_has_no_time(world):
    world.scenario_set({"gpt-6-luna": luna(report=report([GOOD, BAD_SEV])), "default": luna()})
    r, pd = pkg_run(world, values(world, hang_s=10, turn_p90_recv=6.4), collab=0)
    m = meta(pd, "t4-1")
    assert not m["reask"] and m["reask_skipped_deadline"] and m["dropped_lines"] == 1
    assert [x for x in world.argv_log() if "--resume" in x["argv"]] == []


def _reask_hangs(world, collab):
    world.scenario_set({"gpt-6-luna@resume": {"hang": True}, "gpt-6-luna": luna(report=report([GOOD, BAD_SEV])),
                        "default": luna()})
    r, pd = pkg_run(world, values(world, hang_s=16, k=0), collab=collab, row=f"rh{collab}")
    t0 = int((pd / "t0").read_text())
    m = meta(pd, "t4-1")
    assert m["reask"] and m["hang_kill"] and m["slo_breach"]
    assert abs(m["end_ms"] - (t0 + 16_000)) < 1000
    c = json.loads((pd / "collab.json").read_text())
    assert c["slo_breach"] and c["elapsed_s"] >= 15.0


def test_reask_hangs_collab(world):
    _reask_hangs(world, 1)


def test_reask_hangs_isolated(world):
    _reask_hangs(world, 0)


def test_wrong_blockers_rise():
    base = [{"row": f"a{i}", "wrong_blockers": 1.0, "collab": {"own_line_jaccard": {}, "echo_rate": {}, "reruns": 0, "rerun_mismatches": 0},
             "per_package": {}} for i in range(3)]
    arm = [{**b, "row": f"f{i}", "wrong_blockers": 2.5} for i, b in enumerate(base)]
    s = SA.summarize(arm, base)
    assert s["fail"] and "wrong_blockers" in s["reasons"]


def test_finish_signal(world):
    world.scenario_set({"muse-ember-1.0#sw": {"sleep_before": 4, "posts": _posts(1), "report": "done"},
                        "muse-ember-1.0": {"report": report()},
                        "gpt-6-luna": luna(tool_calls=[LS] * 6, loop_until_ms=0)})
    # luna keeps calling tools until T0 + 6 s; the finish signal is at T0 + 3 s
    sc = json.loads(world.scenario.read_text())
    sc["entries"]["gpt-6-luna"]["loop_until_ms"] = int(time.time() * 1000) + 9000
    world.scenario.write_text(json.dumps(sc))
    r, pd = pkg_run(world, values(world, panel_finish_at_s=3, sweeper_kill_s=40))
    for rid in ("t4-1", "t3-1"):
        evs = [json.loads(x) for x in (pd / f"board/metrics/{rid}.jsonl").read_text().splitlines()]
        assert [e["ev"] for e in evs].count("finish_signal") == 1
        ft = next(e["t"] for e in evs if e["ev"] == "finish_signal")
        assert not any(e["ev"] == "deliver" and e["t"] > ft for e in evs)
        a1 = json.loads((pd / f"reviews/{rid}.attempt1.json").read_text())
        assert sum("finish now with what you have" in (e.get("content") or "") for e in a1) == 1
    rej = [json.loads(x) for x in (pd / "board/msgs/rejected.jsonl").read_text().splitlines()]
    assert rej and rej[0]["reason"] == "after_finish"
    sw = (pd / "sweeper/sw-1.json").read_text()
    assert "refused: finish" in sw


def test_merge_refused(world):
    world.scenario_set({"default": {"report": "no findings block at all"}, "muse-ember-1.0#sw": {"report": "done"}})
    r = world.launch("--panel", "EL2", "--row", "nm", "--packages", P, "--planning-values")
    pd = world.out / "runs/nm" / P
    assert r.returncode == 1 and (pd / "INVALID").exists() and not (pd / "merged-1.md").exists()
    assert not (world.out / "scoring").exists() or not any((world.out / "scoring").rglob("merged-anon.md"))
    assert not (world.tmp / "judge-calls.txt").exists()


def test_anonymiser_leak(world):
    h = world.tmp / "h"
    for d in ("bin", "config", "py"):
        shutil.copytree(R2 / d, h / d)
    body = (h / "bin/anon.sh").read_text()
    (h / "bin/anon.sh").write_text(re.sub(r"# BEGIN strip.*?# END strip\n", "", body, flags=re.S))
    world.scenario_set({"default": luna(report=report([{**GOOD, "claim": "fact from sw-1 says so"}])),
                        "muse-ember-1.0#sw": {"report": "done"}})
    e = world.env
    e["PANEL_COLLAB"] = "1"
    e["R2_FINDINGS_PY"] = str(R2.parents[4] / "src/superclaude/cli/review/findings.py")  # the copy sits outside the repo
    r = run(["bash", str(h / "bin/launch-panel.sh"), "--panel", "EL2", "--row", "leak", "--packages", P, "--planning-values"],
            env=e, timeout=300)
    pd = world.out / "runs/leak" / P
    assert r.returncode == 1 and "anonymiser exit 4" in (pd / "INVALID").read_text()
    assert not (world.tmp / "judge-calls.txt").exists()


def test_judge_file_changed(world):
    d = world.out / "scoring/op1" / P / "Q"
    d.mkdir(parents=True)
    (d / "merged-anon.md").write_text("x")
    world.write_manifest(judge_sha="1" * 64)
    r = run(["bash", str(BIN / "judge.sh"), "op1", P, "Q"], env=world.env)
    assert r.returncode == 5 and not (d / "score.json").exists()


def test_resume_after_merge_before_judge(world):
    world.scenario_set({"muse-ember-1.0#sw": {"report": "done"}, "default": luna()})
    r1 = world.launch("--panel", "EL2", "--row", "res", "--packages", P, "--planning-values", "--no-judge")
    rd = world.out / "runs/res"
    assert r1.returncode == 0, r1.stderr
    pd = rd / P
    runid, opaque = (rd / "runid").read_text(), (rd / "opaque").read_text()
    mt = (pd / "merged-1.md").stat().st_mtime_ns
    label = json.loads((world.out / f"scoring/{opaque.strip()}/{P}/label-key.json").read_text())["label"]
    n_calls = len(world.argv_log())
    r2 = world.launch("--panel", "EL2", "--row", "res", "--packages", P, "--planning-values")
    assert r2.returncode == 0, r2.stdout + r2.stderr
    assert len(world.argv_log()) == n_calls  # no model re-run
    assert (pd / "merged-1.md").stat().st_mtime_ns == mt
    assert (rd / "runid").read_text() == runid and (rd / "opaque").read_text() == opaque
    sd = world.out / f"scoring/{opaque.strip()}/{P}"
    assert json.loads((sd / "label-key.json").read_text())["label"] == label
    assert len(list(sd.rglob("score.json"))) == 1 and len([d for d in sd.iterdir() if d.is_dir()]) == 1


def test_resume_of_unfinished_package(world):
    p1, p2 = PKGS[1], PKGS[2]
    slow = luna(tool_calls=[{**LS, "sleep": 0.4}] * 30)
    world.scenario_set({"muse-ember-1.0#sw": {"posts": _posts(2), "report": "done"}, "gpt-6-luna": slow, "default": luna()})
    e = world.env
    e["PANEL_COLLAB"] = "1"
    proc = subprocess.Popen(["bash", str(BIN / "launch-panel.sh"), "--panel", "EL2", "--row", "un", "--packages", f"{p1} {p2}",
                             "--planning-values", "--no-judge"], env=e, start_new_session=True,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    rd = world.out / "runs/un"
    deadline = time.time() + 120
    target = None
    while time.time() < deadline:
        if (rd / "runid").exists():
            runid = (rd / "runid").read_text().strip()
            target = world.sbr / f"board/{runid}/{p2}/state/t4-1.delivered"
            if target.exists():
                break
        time.sleep(0.2)
    assert target is not None and target.exists(), "package 2 never delivered"
    os.killpg(proc.pid, signal.SIGKILL)
    proc.wait()
    time.sleep(1)
    subprocess.run(["pkill", "-f", str(world.tmp)], check=False)
    assert (rd / p1 / "DONE").exists() and not (rd / p2 / "DONE").exists()
    world.scenario_set({"muse-ember-1.0#sw": {"report": "done"}, "default": luna()})
    r = world.launch("--panel", "EL2", "--row", "un", "--packages", f"{p1} {p2}", "--planning-values", "--no-judge")
    assert r.returncode == 0, r.stdout + r.stderr
    assert list(rd.glob(f"{p2}.incomplete-*")) and list((world.sbr / f"board/{runid}").glob(f"{p2}.incomplete-*"))
    assert list((world.sbr / f"sb/{runid}").glob(f"{p2}.incomplete-*"))
    nb = world.sbr / f"board/{runid}/{p2}"
    calls = [json.loads(x) for x in (nb / "metrics/t4-1.jsonl").read_text().splitlines() if '"call"' in x]
    assert calls[0]["c"] == 1
    assert not (nb / "state/t4-1.sealed").exists() and not (nb / "state/t4-1.delivered").exists()
    assert (nb / "msgs/board.jsonl").read_text() == ""
