"""Fault injection F-1 to F-17 (DESIGN 6.2), fake `claude`, B values scaled to seconds.
F-3, F-4 and F-15 at hook level are in test_hook.py; F-10 is test_launch_preflight.py::test_f6_values_sum_mismatch.
"""
import json
import os

from conftest import (
    CT,
    DS,
    bin_,
    fake_log,
    finding,
    heading_anchor,
    report,
    run,
    write_values,
)
from r5 import read_json, read_jsonl

SURF = "The artifact is written outside the permitted edit locations."
ALL = [f"T{i}" for i in range(1, 13)]


def rep(tasks, claim="The stated mapping drops the budget input."):
    return report([finding(f"F{i}", heading_anchor(CT, t), claim=claim) for i, t in enumerate(tasks)])


def put(env, key, **files):
    for suffix, content in files.items():
        (env["fake"] / f"{key}.{suffix.replace('_', '.')}").write_text(str(content))


def base_scenario(env, recv_tasks=("T10",), scout_tasks=tuple(ALL[:9]), calls=15, gap=0.3):
    put(env, "claude-sonnet-5-5", md=rep(recv_tasks), calls=calls, callgap=gap)
    put(env, "gpt-6-luna", md=rep(scout_tasks))


def values(env, panel="sl2", **over):
    v = {"B_f_s": 8, "finish_offset_s": 10, "hang_offset_s": 12, "k": 2, "turn_p90_s": 0.5, "T_report_p90_s": 0.5}
    v.update(over)
    write_values(env["cfg"], panel, all=v)


def panel(env, row="row", panel_="sl2", collab=1, kit=0, pkg=CT):
    e = {**os.environ, "PANEL_COLLAB": str(collab), "PANEL_KIT": str(kit)}
    r = run(["bash", bin_("run-panel.sh"), row, panel_, pkg], env=e)
    assert r.returncode == 0, r.stderr
    return env["out"] / "runs" / row / pkg


def meta(d, rid, n=None):
    return read_json(d / "reviews" / (f"{rid}.attempt{n}.meta.json" if n else f"{rid}.meta.json"))


def test_f01_hang_kill(env):
    values(env, B_f_s=2, finish_offset_s=2.5, hang_offset_s=3)
    base_scenario(env, calls=0)
    put(env, "claude-sonnet-5-5", sleep=30)
    d = panel(env, collab=0)
    m = meta(d, "t1b-1", 1)
    c = read_json(d / "collab.json")
    assert m["hang_kill"] is True and c["slo"] == "SLO_BREACH"
    assert m["t_end_ms"] - read_json(d / "run.json")["hang_ms"] < 2000
    assert meta(d, "t4-1")["model_ok"] and meta(d, "t3-1")["model_ok"]
    assert not (d / "reviews" / "t1b-1.attempt2.meta.json").exists()


def test_f01_hang_kill_f6(env):
    values(env, B_f_s=2, finish_offset_s=2.5, hang_offset_s=3)
    base_scenario(env, calls=0)
    put(env, "claude-sonnet-5-5", sleep=30)
    d = panel(env, collab=1)
    assert meta(d, "t1b-1", 1)["hang_kill"] and read_json(d / "collab.json")["slo"] == "SLO_BREACH"


def test_f02_retry_isolated(env):
    values(env)
    base_scenario(env)
    put(env, "claude-sonnet-5-5", **{"1_md": "review without a block"})
    d = panel(env)
    calls = [a for a in fake_log(env) if "claude-sonnet-5-5" in a and "--resume" not in a]
    assert len(calls) == 2 and "--settings" in calls[0] and "--settings" not in calls[1]
    m2 = meta(d, "t1b-1", 2)
    assert m2["retry_isolated"] is True and m2["settings"] is False
    cost = read_json(d / "reviews" / "t1b-1.cost.json")
    assert cost["attempts"] == 2 and cost["total_output_tokens_all"] == 200
    hook = read_jsonl(env["fake"] / "hookout.claude-sonnet-5-5.jsonl")
    assert all(json.loads(h["out"]) for h in hook)  # hook ran in attempt 1 only (attempt 2 has no --settings)
    assert read_json(d / "collab.json")["reviewers"]["t1b-1"]["retry_isolated"] is True


def test_f05_late_card(env):
    values(env)
    base_scenario(env, calls=2, gap=0)
    d = panel(env)
    c = read_json(d / "collab.json")
    assert c["cards"] and all(x["status"] == "late" for x in c["cards"] if x["id"])
    assert c["reviewers"]["t1b-1"]["late"] >= 1 and c["requests_delivered"] == 0


def test_f06_scout_after_finish(env):
    values(env, finish_offset_s=1.5, hang_offset_s=12)
    base_scenario(env, calls=12, gap=0.3)
    put(env, "gpt-6-luna", sleep=3)
    d = panel(env)
    assert (d / "board" / "msgs" / "watcher.jsonl").read_text() == ""
    assert read_jsonl(d / "board" / "delivered" / "t1b-1.jsonl") == []


def test_f07_scout_wrong_model(env):
    values(env)
    base_scenario(env)
    put(env, "gpt-6-luna", obs="gpt-6-terra")
    d = panel(env)
    log = read_jsonl(d / "board" / "watcher.log")
    assert sum(e["event"] == "scout_unusable" for e in log) == 4  # 2 scouts x 2 attempts
    assert (d / "board" / "msgs" / "watcher.jsonl").read_text() == ""
    assert read_jsonl(d / "board" / "coverage.jsonl") == []


def test_f08_surface_only_task12(env):
    values(env)
    base_scenario(env, scout_tasks=ALL[:11])
    put(env, "gpt-6-luna", md=report([finding(f"F{i}", heading_anchor(CT, t)) for i, t in enumerate(ALL[:11])]
                                      + [finding("S12", heading_anchor(CT, "T12"), claim=SURF)]))
    d = panel(env)
    ranks = [e for e in read_jsonl(d / "board" / "watcher.log") if e["event"] == "rank"]
    assert ranks and "T12" in ranks[0]["rank"]
    assert read_jsonl(d / "board" / "msgs" / "watcher.jsonl")[0]["items"] == ["T12"]


def bad_sev_report():
    good = finding("F1", heading_anchor(CT, "T2"))
    bad = dict(finding("F2", heading_anchor(CT, "T3")), severity="HIGH")
    return report([good, bad])


def test_f09a_reask_used(env):
    values(env)
    base_scenario(env, calls=0)
    put(env, "claude-sonnet-5-5", md=bad_sev_report())
    put(env, "claude-sonnet-5-5.reask", md=rep(["T2", "T3"]))
    d = panel(env, collab=0)
    t = read_json(d / "reviews" / "t1b-1.timing.json")
    assert t["reask_s"] > 0 and t["dropped_lines"] == 0 and meta(d, "t1b-1")["reask_used"] is True
    assert '"HIGH"' not in (d / "reviews" / "t1b-1.md").read_text()
    rs = [a for a in fake_log(env) if "--resume" in a]
    assert rs and "stream-json" in rs[0] and "--verbose" in rs[0]


def test_f09b_no_time(env):
    values(env, turn_p90_s=100)
    base_scenario(env, calls=0)
    put(env, "claude-sonnet-5-5", md=bad_sev_report())
    d = panel(env, collab=0)
    t = read_json(d / "reviews" / "t1b-1.timing.json")
    assert t["reask_skipped"] is True and t["dropped_lines"] == 1


def test_f09c_reask_other_model(env):
    values(env)
    base_scenario(env, calls=0)
    put(env, "claude-sonnet-5-5", md=bad_sev_report())
    put(env, "claude-sonnet-5-5.reask", md=rep(["T2", "T3"]), obs="gpt-6-luna")
    d = panel(env, collab=0)
    t = read_json(d / "reviews" / "t1b-1.timing.json")
    assert t["reask_model_mismatch"] is True and t["dropped_lines"] == 1
    assert '"HIGH"' in (d / "reviews" / "t1b-1.md").read_text()
    assert meta(d, "t1b-1")["reask_model_ok"] is False


def judge_score(env):
    (env["fake"] / "judge.score.json").write_text(json.dumps({"gt_total": 2, "gt_covered_any": ["GT1"], "gt_covered_blocking": [],
        "ledger_rows_total": 1, "ledger_rows_blocking": 0, "blocking_rows_gt_matched": 0, "wrong_blockers": 0}))


def launch(env, row, pkgs, collab=0):
    e = {**os.environ, "PANEL_COLLAB": str(collab), "PANEL_KIT": "0"}
    return run(["bash", bin_("launch.sh"), "sl2", row, "--pkgs", ",".join(pkgs)], env=e)


def test_f11_merge_refused(env):
    values(env)
    base_scenario(env, calls=0)
    judge_score(env)
    for m in ("claude-sonnet-5-5", "gpt-6-luna"):
        put(env, m, badpkg=DS)
    r = launch(env, "rowm", [DS, CT])
    assert r.returncode == 1, r.stderr
    res = read_json(env["out"] / "results" / "rowm.json")
    assert res["status"] == "partial" and res["pkg_status"][DS]["merge"] == "merge_refused"
    assert res["pkg_status"][CT]["judge"] == "ok" and res["control_found_2"] == 1


def test_f12_judge_non_json(env):
    values(env)
    base_scenario(env, calls=0)
    (env["fake"] / "judge.nonjson").write_text("1")
    r = launch(env, "rowj", [CT])
    res = read_json(env["out"] / "results" / "rowj.json")
    assert r.returncode == 1 and res["status"] == "partial" and res["pkg_status"][CT]["judge"] == "judge_failed"
    assert res["control_found_2"] is None


def test_f13_reads_reflect(env):
    values(env)
    base_scenario(env, calls=0)
    put(env, "gpt-6-luna", toolinput=json.dumps({"file_path": "/repo/.dev/reflect/x.md"}))
    d = panel(env, collab=0)
    a = read_json(d / "audit.json")
    assert a["status"] == "quarantined" and not a["checks"]["transcripts"]["ok"]
    assert (d / "reviews" / "t4-1.md").exists()  # files kept


def test_f14_writes_sandbox(env):
    values(env)
    base_scenario(env, calls=0)
    put(env, "gpt-6-luna", touch=str(env["sb"] / CT / "repo" / "written.txt"))
    d = panel(env, collab=0)
    a = read_json(d / "audit.json")
    assert a["status"] == "quarantined" and not a["checks"]["read_only"]["ok"]


def test_f15_subagent_call_then_main(env):
    values(env)
    base_scenario(env, calls=20, gap=0.25)
    put(env, "claude-sonnet-5-5", agentcall=12)
    d = panel(env)
    mets = read_jsonl(d / "board" / "metrics" / "t1b-1.jsonl")
    assert any(m["event"] == "subagent_call" for m in mets)
    assert read_jsonl(d / "board" / "delivered" / "t1b-1.jsonl")


def test_f16_receiver_ignores_card(env):
    values(env)
    base_scenario(env, recv_tasks=("T1", "T2"))
    d = panel(env)
    a = read_json(d / "alarms.json")
    assert a["DEFLECTION"] is True and a["SLO"] == "ok"
    assert read_json(d / "audit.json")["status"] == "pass"


def test_f17_calls_after_finish(env):
    values(env, B_f_s=3, finish_offset_s=1.5, hang_offset_s=4.5)
    base_scenario(env, calls=40, gap=0.2)
    d = panel(env)
    mets = read_jsonl(d / "board" / "metrics" / "t1b-1.jsonl")
    assert sum(m["event"] == "finish_signal_t" for m in mets) == 1
    c = read_json(d / "collab.json")
    assert c["reviewers"]["t1b-1"]["finish_signal_t"] and c["slo"] == "SLO_BREACH"


def test_f17_over_cap_counts_in_budget(env):
    values(env, B_f_s=1, finish_offset_s=1, hang_offset_s=30)
    base_scenario(env, calls=0)
    put(env, "claude-sonnet-5-5", sleep=2)
    d = panel(env, collab=0)
    assert read_json(d / "collab.json")["slo"] == "over_cap"


def test_f17_slack_extends_over_cap(env, monkeypatch):
    """Same 2 s receiver as above (B 1 s): over_cap with no slack; with PANEL_SLACK_S=30 the cap is 31.35 s, so ok."""
    monkeypatch.setenv("PANEL_SLACK_S", "30")
    write_values(env["cfg"], "sl2", dirname="values-slack30",
                 all={"B_f_s": 1, "finish_offset_s": 31, "hang_offset_s": 30, "k": 2, "slack_s": 30})
    base_scenario(env, calls=0)
    put(env, "claude-sonnet-5-5", sleep=2)
    d = panel(env, collab=0)
    assert read_json(d / "run.json")["slack_s"] == 30
    assert read_json(d / "collab.json")["slo"] == "ok"


def test_ac10_el2_one_card_per_luna(env):
    values(env, panel="el2", k=2)
    put(env, "muse-ember-1.0", md=rep(ALL[:6]))
    put(env, "gpt-6-luna", md=rep(["T7"]), calls=15, callgap=0.3)
    d = panel(env, panel_="el2")
    cards = read_jsonl(d / "board" / "msgs" / "watcher.jsonl")
    assert {c["to"] for c in cards} == {"t4-1", "t3-1"} and len(cards) == 2
    assert not set(cards[0]["items"]) & set(cards[1]["items"])
    for rid in ("t4-1", "t3-1"):
        assert sum(x["status"] == "delivered" for x in read_jsonl(d / "board" / "delivered" / f"{rid}.jsonl")) <= 1


def test_happy_path_f6_delivery(env):
    values(env)
    base_scenario(env)
    d = panel(env)
    c = read_json(d / "collab.json")
    assert c["requests_delivered"] >= 1 and c["reviewers"]["t1b-1"]["hook_error"] == 0
    assert c["reviewers"]["t1b-1"]["snapshot_missing"] == 0 and read_json(d / "audit.json")["status"] == "pass"
    hook = [json.loads(h["out"]) for h in read_jsonl(env["fake"] / "hookout.claude-sonnet-5-5.jsonl")]
    assert any("Panel request" in h["hookSpecificOutput"]["additionalContext"] for h in hook)
    assert not any("--settings" in a for a in fake_log(env) if "gpt-6-luna" in a)
