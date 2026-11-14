"""Fault injection, one test per failure mode of design 6.2 that needs a launcher row.
Arm-level modes (STOP:no_cards over 12 rows, CONVERGENCE on ledger rows, no loss on wrong blockers) are in
test_arm_summary.py; hook-only modes are also in test_hook.py; the judge API error is in test_judge.py."""

import json
import shutil
from pathlib import Path

import pytest
from r4help import DE, DS, PKGS, R4, fixture, jsonl, make_sbr, run

import values

GOOD_JUDGE = {"score": {"gt_covered_any": ["GT1"], "gt_covered_blocking": [], "wrong_blockers": 0}}


def raw_values(env, name="faults.json", k=1, finish=25.0, hang=30.0, B=20.0, deliver=True):
    pk = {p: {"B_A1": B, "turn_p90": 0.5, "T_report_p90": 0.5, "finish_offset_s": finish, "hang_s": hang, "k": k,
              "deliver": deliver, "cp_role": "adjudicator", "n_runs": 0, "source_rows": []} for p in PKGS}
    d = Path(env["R4_OUT"]) / "values"
    d.mkdir(exist_ok=True)
    values.write_pinned(str(d / name), {"panel": "EL2", "kind": "test", "packages": pk})
    return d / name


def row(env, tmp_path, fake, name, collab=1, pkg=DE, judge=False, **vk):
    make_sbr(env, [pkg]) if not (Path(env["R4_SBR"]) / "sb" / pkg).exists() else None
    fake.setdefault("judge", GOOD_JUDGE)
    fixture(env, fake, tmp_path)
    v = raw_values(env, name=f"{name}.json", **vk)
    args = [R4 / "bin/run-panel.sh", "--panel", "EL2", "--row", name, "--values", v, "--packages", pkg, "--seed", "0"]
    if not judge:
        args.append("--no-judge")
    r = run(args, env=dict(env, PANEL_COLLAB=str(collab)), timeout=300)
    pd = Path(env["R4_OUT"]) / "runs" / name / pkg
    return r, pd


def meta(pd, rid):
    return json.load(open(pd / "reviews" / f"{rid}.meta.json"))


def collab(pd):
    return json.load(open(pd / "collab.json"))


FLAG = {"calls": 7, "call_sleep": 0.2, "posts": {str(i): {"anchor": f"AUTO:{i - 3}", "move": "M3", "category": "other", "severity": "MAJOR"} for i in range(3, 5)}}
LUNA = {"calls": 9, "call_sleep": 0.4}


def test_flagger_never_posts(env, tmp_path):
    r, pd = row(env, tmp_path, {"by_rid": {"t2b-1": {"calls": 5}}, "by_model": {"gpt-6-luna": LUNA}}, "nopost")
    assert collab(pd)["cards_sent"] == 0


def test_cards_on_early_tasks(env, tmp_path):
    flag = {"calls": 8, "call_sleep": 0.1, "posts": {str(i): {"anchor": "AUTO:0", "move": "M3", "category": "other", "severity": "MAJOR"} for i in (3, 4)}}
    r, pd = row(env, tmp_path, {"by_rid": {"t2b-1": flag}, "by_model": {"gpt-6-luna": LUNA}}, "early", pkg=DS, judge=True)
    assert r.returncode in (0, 1), r.stderr
    assert [s["card_task"] for s in collab(pd)["slots"]] == ["T1", "T1"]
    res = json.load(open(Path(env["R4_OUT"]) / "results" / "early.json"))
    assert res["collab"][DS]["early_tasks_only"] is True


def test_flags_like_findings(env, tmp_path):
    flag = dict(FLAG, posts={str(i): {"anchor": f"AUTO:{i - 3}", "move": "M3", "category": "other", "severity": "MAJOR"} for i in range(3, 7)},
                report_anchors=["AUTO:0", "AUTO:1", "AUTO:2"])
    r, pd = row(env, tmp_path, {"by_rid": {"t2b-1": flag}, "by_model": {"gpt-6-luna": LUNA}}, "ffo", k=2)
    assert collab(pd)["flag_finding_overlap"] == 0.75


def test_snapshot_not_written(env, tmp_path):
    luna = dict(LUNA, transcript_path="missing")
    r, pd = row(env, tmp_path, {"by_rid": {"t2b-1": FLAG, "t4-1": luna}, "by_model": {"gpt-6-luna": LUNA}}, "nosnap", k=2)
    c = collab(pd)
    assert c["reviewers"]["t4-1"]["snapshot_missing"] is True and c["reviewers"]["t4-1"]["msgs_received"] == 0
    assert (pd / "board" / "state" / "t4-1.nosnap").exists()
    assert meta(pd, "t4-1")["final_ok"] is True
    assert any(e["ev"] == "snapshot_missing" for e in jsonl(pd / "board" / "metrics" / "t4-1.jsonl"))


def test_luna_past_finish(env, tmp_path):
    luna = {"calls": 14, "call_sleep": 0.5}
    r, pd = row(env, tmp_path, {"by_rid": {"t2b-1": FLAG}, "by_model": {"gpt-6-luna": luna}}, "pastfin", finish=4.0)
    c = collab(pd)
    for rid in ("t4-1", "t3-1"):
        fin = c["reviewers"][rid]["finish_signal_t"]
        assert fin
        outs = [h["stdout"] for h in jsonl(Path(env["FAKE_LOG"]) / f"hooks.{rid}.jsonl")]
        assert sum("finish now with what you have" in o for o in outs) == 1
        delivered = [s for s in c["slots"] if s["recipient"] == rid and s["t_delivered"]]
        assert all(s["t_delivered"] < fin for s in delivered)


@pytest.mark.parametrize("collab_on", [0, 1])
def test_reviewer_hangs(env, tmp_path, collab_on):
    luna = {"sleep": 30, "calls": 1}
    r, pd = row(env, tmp_path, {"by_rid": {"t2b-1": FLAG, "t4-1": luna}, "by_model": {"gpt-6-luna": [luna, {"calls": 1}]}},
                f"hang{collab_on}", collab=collab_on, hang=4.0, finish=3.0)
    m = [meta(pd, r_) for r_ in ("t4-1", "t3-1")]
    killed = [x for x in m if x["hang_kill"]]
    assert killed, m
    panel = json.load(open(pd / "panel.json"))
    for x in killed:
        assert x["t_end_ms"] - panel["t0_ms"] <= 4000 + 6000
    assert collab(pd)["slo_breach"] is True
    assert meta(pd, "t2b-1")["final_ok"] is True


def test_hook_error_review_completes(env, tmp_path):
    luna = dict(LUNA, corrupt_calls=True)
    r, pd = row(env, tmp_path, {"by_rid": {"t2b-1": FLAG, "t4-1": luna}, "by_model": {"gpt-6-luna": LUNA}}, "hookerr")
    assert any(e["ev"] == "hook_error" for e in jsonl(pd / "board" / "metrics" / "t4-1.jsonl"))
    assert meta(pd, "t4-1")["final_ok"] is True
    assert collab(pd)["reviewers"]["t4-1"]["hook_error"] >= 1


def test_attempt1_fails_retry_isolated(env, tmp_path):
    r, pd = row(env, tmp_path, {"by_rid": {"t2b-1": FLAG, "t4-1": {"calls": 2, "no_block": True}}, "by_model": {"gpt-6-luna": LUNA}}, "retry")
    m = meta(pd, "t4-1")
    assert m["attempts"] == 2 and m["retry_isolated"] is True and m["final_ok"] is True
    a2 = [a for a in jsonl(Path(env["FAKE_LOG"]) / "argv.jsonl") if "gpt-6-luna" in a["argv"] and "--settings" not in a["argv"]]
    assert len(a2) == 1 and not a2[0]["brief_has_adjudicator"]
    a1 = json.load(open(pd / "reviews" / "t4-1.attempt1.meta.json"))
    a2m = json.load(open(pd / "reviews" / "t4-1.attempt2.meta.json"))
    assert m["t_start_ms"] == a1["t_start_ms"] and m["t_end_ms"] >= a2m["t_end_ms"]
    assert collab(pd)["elapsed_s"] * 1000 >= a2m["t_end_ms"] - json.load(open(pd / "panel.json"))["t0_ms"] - 1


BAD = ('review: 1 of 3\n\n## Findings block\n\n```findings-v1\n'
       '{"id":"F1","severity":"HIGH","blocking":true,"category":"other","anchor":"AAAA","refs":[],"claim":"c"}\n```\nverdict: FAIL\n')


def test_parser_drop_reask(env, tmp_path):
    bad = {"calls": 1, "report": BAD}
    r, pd = row(env, tmp_path, {"by_model": {"gpt-6-luna": {"calls": 1}, "muse-ember-1.0": bad}, "resume": {"report": BAD}},
                "reask", collab=0)
    m = meta(pd, "t2b-1")
    re_ = [a for a in jsonl(Path(env["FAKE_LOG"]) / "argv.jsonl") if "--resume" in a["argv"]]
    assert len(re_) == 1
    assert {"stream-json", "--verbose"} <= set(re_[0]["argv"]) and "--settings" not in re_[0]["argv"]
    assert m["reask"] is True and m["reask_s"] is not None and m["dropped_lines"] == 1


def test_wrong_model(env, tmp_path):
    r, pd = row(env, tmp_path, {"by_model": {"gpt-6-luna": {"calls": 1}, "muse-ember-1.0": {"calls": 1, "model": "gpt-6.1-sol"}}},
                "wrongmodel", collab=0, judge=True)
    m = meta(pd, "t2b-1")
    assert m["model_ok"] is False and m["model_mismatch"] is True
    assert (pd / "status").read_text().strip() == "invalid_model" and not (pd / "merged-1.md").exists()
    assert json.load(open(Path(env["R4_OUT"]) / "results" / "wrongmodel.json"))["valid"] is False


def test_one_reviewer_without_block(env, tmp_path):
    r, pd = row(env, tmp_path, {"by_model": {"gpt-6-luna": {"calls": 1}, "muse-ember-1.0": {"calls": 1, "no_block": True}}},
                "oneblock", collab=0, judge=True)
    assert (pd / "reviews" / "t2b-1.final.md").exists() and meta(pd, "t2b-1")["final_ok"] is False
    led = json.load(open(pd / "ledger.json"))
    assert (pd / "status").read_text().strip() == "ok" and (pd / "scoring" / "score.json").exists()
    assert "t2b-1" in json.dumps(led)  # recorded in the round, block not ok
    assert '"t2b-1": false' in (pd / "merge-stdout.txt").read_text().replace("\n", " ").replace("  ", " ") or "block ok false" in (pd / "merged-1.md").read_text()


def test_no_valid_block(env, tmp_path):
    nb = {"calls": 1, "no_block": True}
    r, pd = row(env, tmp_path, {"by_model": {"gpt-6-luna": nb, "muse-ember-1.0": nb}}, "noblock", collab=0, judge=True)
    assert (pd / "status").read_text().strip() == "merge_refused"
    assert not [a for a in jsonl(Path(env["FAKE_LOG"]) / "argv.jsonl") if "claude-opus-5-5" in a["argv"]]


def test_forged_board_lines(env, tmp_path):
    luna = dict(LUNA, forge=True)
    r, pd = row(env, tmp_path, {"by_rid": {"t2b-1": {"calls": 3}, "t4-1": luna}, "by_model": {"gpt-6-luna": LUNA}}, "forge")
    assert not (pd / "board" / "state" / "t4-1.delivered").exists()
    audit = json.load(open(pd.parent / "audit.json"))
    assert audit["board_lines_invalid"] == 2 and audit["audit_ok"] is False


@pytest.mark.parametrize("cmd,kind", [("cat /x/ground-truth.json", "path"), ("grep -r x /tmp", "broad_search"),
                                      ("cat /tmp/jdg.abcdefgh/p/L/judge.json", "path")])
def test_ground_truth_access(env, tmp_path, cmd, kind):
    luna = {"calls": 2, "commands": {"1": cmd}}
    r, pd = row(env, tmp_path, {"by_model": {"gpt-6-luna": luna, "muse-ember-1.0": {"calls": 1}}}, "gt", collab=0)
    audit = json.load(open(pd.parent / "audit.json"))
    assert audit["audit_ok"] is False and any(v["kind"] == kind for v in audit["violations"])
    assert (pd.parent / "QUARANTINED").exists()


def test_sandbox_write(env, tmp_path):
    r, pd = row(env, tmp_path, {"by_model": {"gpt-6-luna": {"calls": 1, "touch": "x"}, "muse-ember-1.0": {"calls": 1}}}, "write", collab=0)
    audit = json.load(open(pd.parent / "audit.json"))
    assert audit["sandbox_clean"] is False and any(v["kind"] == "sandbox_write" for v in audit["violations"])


def test_harness_text_leak(env, tmp_path):
    r, pd = row(env, tmp_path, {"by_model": {"gpt-6-luna": {"calls": 1}, "muse-ember-1.0": {"calls": 1}}}, "leak", collab=0)
    fz = tmp_path / "frozen"
    shutil.copytree(R4 / "frozen", fz)
    gt = json.load(open(R4.parents[0] / ".." / "20261111-a1" / DE / "ground-truth.json"))["items"][0]["plan_quote"]
    t = json.load(open(fz / "templates.json"))
    t["finish"] += " " + gt[:14]
    (fz / "templates.json").write_text(json.dumps(t))
    rr = run(["uv", "run", "--frozen", "--project", R4.parents[4], "python", R4 / "lib/audit.py", pd.parent], env=dict(env, R4_FROZEN=str(fz)))
    assert rr.returncode == 0, rr.stderr
    audit = json.load(open(pd.parent / "audit.json"))
    assert audit["harness_text_gt_overlap"] > 0 and any(v["kind"] == "harness_text_gt_overlap" for v in audit["violations"])
