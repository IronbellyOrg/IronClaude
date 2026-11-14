"""lib/collab.py (design 2.8; R-10, R-23, R-25, R-36)."""

import json
import shutil

import collab
from r4help import DE, EVAL, first_card_anchor, make_board, now_ms, post

R23 = ["arm", "msgs_sent", "msgs_received", "first_delivery_t", "seal_t", "resume_fallback", "phase2_s", "stop_blocks", "hook_calls",
       "hook_error", "hook_ms_p95", "reask_s", "attempts", "retry_s", "retry_isolated", "phase2_timeout", "p2_lines_salvaged",
       "n_planned", "n_launched", "k", "panel_finish_at", "finish_signal_t", "finish_would_fire", "hang_kill", "snapshot_missing",
       "late", "over_cap", "slot_type", "card_form", "deal_r", "deal_c", "elapsed_s", "baseline_elapsed_s", "overhead_pct",
       "own_line_jaccard", "pairwise_task_jaccard", "echo_rate", "ledger_rows", "values_sha256"]


def test_overlap12():
    base = "abcdefghijkl"
    assert collab.overlap12("xx " + base + " yy", "zz" + base + "ww") is True
    assert collab.overlap12("xx " + base[:11] + " yy", "zz" + base[:11] + "ww") is False


def test_task_of():
    cand = "# Plan\n\n## Constraints\n\nnever touch the database layer here\n\n## Task 3: Do it\n\nthe widget must render every row\n"
    assert collab.task_of(cand, "the widget must render every row") == "T3"
    assert collab.task_of(cand, "never touch the database layer") is None


def test_forms_and_deal():
    assert [collab.form_of(i, 0) for i in range(4)] == ["challenge", "finding", "finding", "challenge"]
    assert [collab.form_of(i, 1) for i in range(4)] == ["finding", "challenge", "challenge", "finding"]
    assert [collab.recipient_of(i, 0, ["t4-1", "t3-1"]) for i in range(4)] == ["t4-1", "t3-1", "t4-1", "t3-1"]


def test_jaccard_fixture():
    # R-25: peer-tagged lines raise all-line Jaccard but not own-line Jaccard
    own = [{"T1"}, {"T2"}, {"T3"}]
    allx = [{"T1", "T9"}, {"T2", "T9"}, {"T3", "T9"}]
    assert collab.own_line_jaccard(own) == 0
    assert collab.own_line_jaccard(allx) > collab.own_line_jaccard(own)
    assert collab.own_line_jaccard([set(), set(), set()]) is None


def report(findings):
    return "review: 1 of 3\n\n## Findings block\n\n```findings-v1\n" + "\n".join(json.dumps(f) for f in findings) + "\n```\n"


def f(fid, anchor, **kw):
    return {"id": fid, "severity": "MAJOR", "blocking": False, "category": "other", "anchor": anchor, "refs": [], "claim": "c", **kw} | kw


def make_pkg(tmp_path, cards=2, deliver=(), flagger_lines=(), luna_lines=None, passed=""):
    """A package dir with a board copy: `cards` accepted cards, delivered as listed."""
    pd = tmp_path / "pkg"
    (pd / "reviews").mkdir(parents=True)
    board, cf = make_board(tmp_path)
    anchors = [first_card_anchor(n=n, length=60) for n in range(cards)]
    for a in anchors:
        assert post(board, cf, anchor=a).returncode == 0
    for cid, rid, form in deliver:
        with open(board / "state" / f"{rid}.delivered", "a") as fh:
            fh.write(f"{cid} {now_ms()} {form}\n")
    shutil.copytree(board, pd / "board")
    cand = tmp_path / "candidate.md"
    shutil.copy(EVAL / DE / "candidate.md", cand)
    t0 = now_ms() - 10_000
    (pd / "panel.json").write_text(json.dumps({
        "row": "r", "pkg": DE, "panel": "EL2", "arm": "F7", "k": 2, "k0_isolated": False, "deliver": 1, "r": 0, "c": 0,
        "t0_ms": t0, "finish_ms": t0 + 5000, "hang_ms": t0 + 60000, "B_A1": 8.0, "cp_role": "adjudicator", "values_sha256": "ab",
        "cand": str(cand), "flagger": "t2b-1", "peers": ["t4-1", "t3-1"],
        "reviewers": [{"rid": "t2b-1"}, {"rid": "t4-1"}, {"rid": "t3-1"}]}))
    luna_lines = luna_lines or {}
    for rid in ("t2b-1", "t4-1", "t3-1"):
        lines = list(flagger_lines) if rid == "t2b-1" else luna_lines.get(rid, [])
        (pd / "reviews" / f"{rid}.final.md").write_text(report(lines) + (passed if rid == "t3-1" else ""))
        (pd / "reviews" / f"{rid}.meta.json").write_text(json.dumps({"t_end_ms": t0 + 9000, "attempts": 1, "hang_kill": False}))
    return pd, anchors


def test_peer_tags_conversion_and_overlap(tmp_path):
    a0 = first_card_anchor(n=0)
    luna = {"t4-1": [f("L1", a0[:12] + "Q" * 20), f("L2", a0[:11] + " other text here")]}
    pd, anchors = make_pkg(tmp_path, deliver=[("c0", "t4-1", "challenge")], flagger_lines=[f("E1", a0), f("E2", "unrelated anchor text abc")],
                           luna_lines=luna)
    out = collab.compute(str(pd))
    tags = json.load(open(pd / "tags" / "t4-1.json"))
    assert tags == {"L1": "peer", "L2": "own"}
    assert json.load(open(pd / "tags" / "t2b-1.json")) == {"E1": "own", "E2": "own"}
    s0 = [s for s in out["slots"] if s["id"] == "c0"][0]
    assert s0["status"] == "delivered" and s0["converted"] and s0["converted_fids"] == ["L1"]
    s1 = [s for s in out["slots"] if s["id"] == "c1"][0]
    assert s1["status"] == "late"  # dealt to t3-1, never delivered, nothing blocked it
    assert out["flag_finding_overlap"] == 0.5
    assert out["adjudication_agreement"] == 1.0


def test_collab_schema(tmp_path):
    pd, _ = make_pkg(tmp_path, deliver=[("c0", "t4-1", "challenge")], passed="\ncard c1: passed (ran grep)\n")
    out = collab.compute(str(pd))
    flat = set(out) | {k for v in out["reviewers"].values() for k in v} | {k for s in out["slots"] for k in s}
    missing = [k for k in R23 if k not in flat]
    assert not missing, missing
    for k in ("resume_fallback", "phase2_s", "phase2_timeout", "p2_lines_salvaged", "n_planned", "n_launched", "slot_type", "echo_rate"):
        assert out[k] is None
    assert out["slots"][1]["passed_line"] is True
    assert out["reviewers"]["t4-1"]["msgs_sent"] == 0 and out["reviewers"]["t2b-1"]["msgs_received"] == 0
