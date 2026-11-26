"""T-17: collab_summary.py pre/post, R-23 keys, Jaccard, move_executed, elapsed and audits."""

import json

import pytest
from conftest import CAND_LONG, Pkg, finding, report

R23_PANEL = ["arm", "panel_finish_at", "elapsed_s", "baseline_elapsed_s", "overhead_pct", "own_line_jaccard", "pairwise_task_jaccard",
             "echo_rate", "ledger_rows", "values_sha256"]
R23_REVIEWER = ["msgs_sent", "msgs_received", "first_delivery_t", "seal_t", "resume_fallback", "phase2_s", "stop_blocks", "hook_calls",
                "hook_error", "hook_ms_p95", "reask_s", "attempts", "retry_s", "retry_isolated", "phase2_timeout", "p2_lines_salvaged",
                "n_planned", "n_launched", "k", "panel_finish_at", "finish_signal_t", "finish_would_fire", "hang_kill",
                "snapshot_missing", "late", "over_cap"]
R23_SLOT = ["slot_type", "card_form", "deal_r", "deal_c"]


def searcher_with_m2(p, then_cmd=None):
    """Searcher reads source.md, makes 5 more calls (M2 injected at call 6), then optionally one more call."""
    b = p.board
    clock = 1000
    b.call("t2b-1", "searcher", tool="Read", inp={"file_path": b.src})
    for _ in range(5):
        clock += 10
        b.set_clock(clock)
        out = b.call("t2b-1", "searcher")
    assert out
    if then_cmd:
        b.set_clock(clock + 10)
        b.call("t2b-1", "searcher", inp={"command": then_cmd})


def test_pre_post_and_r23_keys(pkg1):
    searcher_with_m2(pkg1)
    r = pkg1.summary("pre")
    assert r.returncode == 0, r.stderr + r.stdout
    assert pkg1.collab_json()["ledger_rows"] is None  # pre works without ledger.json and merged-anon.md
    (pkg1.d / "ledger.json").write_text(json.dumps({"rows": [{}, {}, {}]}))
    (pkg1.d / "merged-1.md").write_text(f"report {pkg1.d}/reviews/t2b-1.md\nReviewer t4-1 agrees.\n")
    from conftest import TOOLS, run
    out_dir = run(["bash", str(TOOLS / "anon.sh"), pkg1.row, pkg1.pkg, "--root", str(pkg1.root)]).stdout.strip()
    assert pkg1.summary("post").returncode == 0
    c = pkg1.collab_json()
    assert c["ledger_rows"] == 3 and c["anon_leak"] == 0 and pkg1.audit()["anon_leak"] == 0 and c["arm"] == "A6-F3"
    # a planted row id and reviewer id survive into merged-anon.md -> counted in collab.json and audit.json
    with open(f"{out_dir}/merged-anon.md", "a") as f:
        f.write(f"leaked {pkg1.row} and t3-1\n")
    assert pkg1.summary("post").returncode == 0
    c = pkg1.collab_json()
    assert c["anon_leak"] >= 2 and pkg1.audit()["anon_leak"] == c["anon_leak"]
    for k in R23_PANEL:
        assert k in c, k
    for rv in c["reviewers"].values():
        for k in R23_REVIEWER:
            assert k in rv, k
        assert rv["resume_fallback"] is None and rv["stop_blocks"] == 0 and rv["over_cap"] == 0 and rv["late"] == 0
    assert c["slots"] and all(k in s for s in c["slots"] for k in R23_SLOT)


def test_own_line_jaccard_hand_value(pkg1):
    pkg1.review("t2b-1", report(finding()))                                            # Task 1
    pkg1.review("t4-1", report(finding(), finding(id="F2", anchor=CAND_LONG[:60])))    # Task 1 and Task 3
    pkg1.review("t3-1", report())                                                      # no finding
    assert pkg1.summary("pre").returncode == 0
    c = pkg1.collab_json()
    assert c["task_sets"] == {"t2b-1": ["T1"], "t4-1": ["T1", "T3"], "t3-1": []}
    assert c["own_line_jaccard"] == pytest.approx((0.5 + 0 + 0) / 3)


@pytest.mark.parametrize("later,expect", [("grep -c x src/", True), ("ls", False)])
def test_move_executed(pkg1, later, expect):
    searcher_with_m2(pkg1, then_cmd=later)
    assert pkg1.summary("pre").returncode == 0
    slots = {s["move"]: s for s in pkg1.collab_json()["slots"]}
    assert slots["M2"]["move_executed"] is expect


def test_move_executed_null_for_reading_moves(pkg1):
    b = pkg1.board
    b.call("t4-1", "reader", tool="Read", inp={"file_path": b.src})
    for _ in range(8):
        b.call("t4-1", "reader")
    assert pkg1.summary("pre").returncode == 0
    s = [x for x in pkg1.collab_json()["slots"] if x["rid"] == "t4-1"]
    assert s and s[0]["slot_type"] == "static" and s[0]["move_executed"] is None


def test_elapsed_is_max_end_minus_t0(pkg1):
    pkg1.review("t3-1", report(), end_ms=150_500)
    assert pkg1.summary("pre").returncode == 0
    c = pkg1.collab_json()
    assert c["elapsed_s"] == 150.5 and c["overhead_pct"] == pytest.approx(100 * (150.5 / 116 - 1))


def test_audit_flags_gt_substring_in_board(pkg1):
    b = pkg1.board
    line = {"v": "panel-msg/1", "id": "m-t4-1-08", "run": "The guard keeps every retry", "from": "radar", "to": "t4-1", "t": 1, "kind": "move", "move": "M3"}
    (b.dir / "msgs").mkdir(exist_ok=True)
    (b.dir / "msgs" / "radar.jsonl").write_text(json.dumps(line) + "\n")
    (b.dir / "metrics").mkdir(exist_ok=True)
    with (b.dir / "metrics" / "t4-1.jsonl").open("a") as f:
        f.write(json.dumps({"ev": "inject", "id": "m-t4-1-08", "t": 1, "n": 8, "move": "M3", "slot_type": "static", "task_hint": [],
                            "text": __import__("conftest").CAT["moves"]["M3"]}) + "\n")
    r = pkg1.summary("pre")
    assert r.returncode == 3 and pkg1.audit()["gt_substrings_in_board"] == 1 and (pkg1.d / "QUARANTINED").exists()


def test_audit_flags_dirty_sandbox_and_changed_candidate(pkg1):
    (pkg1.sb / pkg1.pkg / "repo" / "src" / "a.py").write_text("changed\n")
    (pkg1.sb / "cand" / pkg1.pkg / "candidate.md").write_text("edited\n")
    r = pkg1.summary("pre")
    a = pkg1.audit()
    assert r.returncode == 3 and a["sandbox_clean"] is False and a["candidate_sha_unchanged"] is False


def test_collab0_coverage_from_transcripts_and_finish_would_fire(tmp_path, root):
    p = Pkg(tmp_path, root, row="el2-c0-r0", collab=0)
    p.run["FINISH_MS"] = 120_000
    p.write_run()
    p.review("t4-1", report(), end_ms=130_000)
    tr = [{"type": "assistant", "parent_tool_use_id": None, "message": {"content": [
        {"type": "tool_use", "name": "Bash", "input": {"command": "grep -c x src/"}}]}}]
    (p.d / "reviews" / "t2b-1.attempt1.json").write_text(json.dumps(tr))
    assert p.summary("pre").returncode == 0
    c = p.collab_json()
    assert c["arm"] == "A1" and c["moves_covered"]["M2"] == 1 and c["slots"] == []
    assert c["reviewers"]["t4-1"]["finish_would_fire"] is True and c["reviewers"]["t2b-1"]["finish_would_fire"] is False
    assert not (p.d / "board" / "msgs").exists() and not (p.d / "settings").exists()



