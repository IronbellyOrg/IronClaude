"""T-14 tagger (R-10, D7) and T-15 collab.json (R-23, R-41)."""
import json

from conftest import CT, finding, heading_anchor, report
from r5 import collab, read_jsonl, tagger

R23 = {"resume_fallback", "phase2_s", "n_planned", "n_launched", "phase2_timeout", "p2_lines_salvaged", "slot_type", "card_form",
       "deal_c", "echo_rate", "stop_blocks", "msgs_sent", "over_cap", "arm", "k", "deal_r", "panel_finish_at", "finish_would_fire",
       "elapsed_s", "baseline_elapsed_s", "overhead_pct", "own_line_jaccard", "pairwise_task_jaccard", "ledger_rows", "values_sha256",
       "cards", "requests_posted", "requests_delivered", "requests_acted", "scout_covered_tasks", "receiver_anchored_tasks",
       "deflection_overlap", "union_anchored_tasks", "k0_isolated", "slo", "reviewers"}
PER_REV = {"msgs_received", "first_delivery_t", "seal_t", "hook_calls", "hook_error", "hook_ms_p95", "reask_s", "attempts", "retry_s",
           "retry_isolated", "finish_signal_t", "hang_kill", "snapshot_missing", "late"}


def make_run(env, arm="F6-sl2", recv_tasks=(("T9", "T3"), ("T5",)), scout_tasks=("T1", "T2"), delivered_items=("T9",), t_end=None):
    d = env["out"] / "runs" / "row" / CT
    (d / "reviews").mkdir(parents=True)
    T0 = 1_000_000
    info = {"row": "row", "arm": arm, "panel": "sl2", "pkg": CT, "T0": T0, "finish_ms": T0 + 12_000, "hang_ms": T0 + 15_000, "k": 2,
            "deal_r": 0, "values_sha256": "v", "B_f_s": 10, "receivers": ["t1b-1"], "scouts": ["t4-1", "t3-1"],
            "models": {"t1b-1": "claude-sonnet-5-5", "t4-1": "gpt-6-luna", "t3-1": "gpt-6-luna"}, "k0_isolated": False}
    (d / "run.json").write_text(json.dumps(info))
    fs = []
    for i, ts in enumerate(recv_tasks):
        f = finding(f"F{i}", heading_anchor(CT, ts[0]))
        if len(ts) > 1:
            f["anchor2"] = heading_anchor(CT, ts[1])
        fs.append(f)
    (d / "reviews" / "t1b-1.md").write_text(report(fs))
    for rid in ("t4-1", "t3-1"):
        (d / "reviews" / f"{rid}.md").write_text(report([finding(f"S{j}", heading_anchor(CT, t)) for j, t in enumerate(scout_tasks)]))
    for rid in info["models"]:
        end = t_end if (t_end and rid == "t1b-1") else T0 + 8000
        (d / "reviews" / f"{rid}.attempt1.meta.json").write_text(json.dumps({"attempt": 1, "wall_s": 8, "t_end_ms": end, "model_ok": True}))
        (d / "reviews" / f"{rid}.timing.json").write_text(json.dumps({"t_end_ms": end, "reask_s": 0}))
    if arm.startswith("F6"):
        b = d / "board"
        for s in ("msgs", "delivered", "state", "snap", "metrics"):
            (b / s).mkdir(parents=True)
        card = {"v": "panel-msg/1", "id": "c-t1b-1-1", "run": f"row/{CT}", "from": "watcher", "to": "t1b-1", "t": T0 + 3000,
                "kind": "coverage", "items": list(delivered_items)}
        (b / "msgs" / "watcher.jsonl").write_text(json.dumps(card) + "\n")
        (b / "delivered" / "t1b-1.jsonl").write_text(json.dumps({"id": "c-t1b-1-1", "t": T0 + 4000, "status": "delivered"}) + "\n")
        (b / "metrics" / "t1b-1.jsonl").write_text(json.dumps({"event": "call", "ms": 12}) + "\n")
    return d


def test_tagger(env):  # T-14
    d = make_run(env, recv_tasks=(("T9",), ("T5", "T9"), ("T5",)))
    before = (d / "reviews" / "t1b-1.md").read_bytes()
    res = tagger.tag(d, env["sb"] / "cand" / CT / "candidate.md")
    origins = {x["fid"]: x["origin"] for x in read_jsonl(d / "tags" / "t1b-1.jsonl")}
    assert origins == {"F0": "peer", "F1": "peer", "F2": "own"}
    assert all(x["origin"] == "own" for x in read_jsonl(d / "tags" / "t4-1.jsonl"))
    assert res["t1b-1"]["requests_acted"] == 1
    assert (d / "reviews" / "t1b-1.md").read_bytes() == before


def test_collab_keys_f6_and_a1(env):  # T-15
    d = make_run(env, t_end=1_000_000 + 13_000)
    tagger.tag(d, env["sb"] / "cand" / CT / "candidate.md")
    c = collab.build(d)
    assert R23 <= set(c)
    assert PER_REV <= set(c["reviewers"]["t1b-1"])
    assert c["finish_would_fire"] is True and c["requests_delivered"] == 1 and c["requests_acted"] == 1
    assert c["cards"][0]["status"] == "delivered"
    assert c["scout_covered_tasks"] == ["T1", "T2"]


def test_collab_a1_nulls(env):
    d = make_run(env, arm="A1-sl2")
    tagger.tag(d, env["sb"] / "cand" / CT / "candidate.md")
    c = collab.build(d)
    assert R23 <= set(c)
    for k in ("cards", "requests_posted", "requests_delivered", "requests_acted", "phase2_s", "echo_rate"):
        assert c[k] is None
    for k in ("msgs_received", "hook_calls", "seal_t", "snapshot_missing"):
        assert c["reviewers"]["t1b-1"][k] is None
    assert c["finish_would_fire"] is False
