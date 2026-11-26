"""py/collab_metrics.py (R-20, R-23, R-25) on a synthetic package directory."""
import json
import sys

import pytest
from conftest import CANDIDATE, PY

sys.path.insert(0, str(PY))
import collab_metrics as CM  # noqa: E402

T0 = 1_000_000
A_T1 = "so that every greeting uses the new wording"   # Task 1
A_T2 = "all examples in the guide use it"              # Task 2
A_T3 = "Add one line to the release notes"             # Task 3


def tu(i, name, inp):
    return {"type": "assistant", "message": {"model": "gpt-6-luna", "content": [{"type": "tool_use", "id": f"t{i}", "name": name, "input": inp}]}}


def tr(i, text):
    return {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": f"t{i}", "content": text}]}}


def build(tmp, *, facts=(), metrics=None, transcripts=None, tags=None, metas=None, k=2, sweeper_tr=None, B=100, fin_s=120):
    pd = tmp / "pkg"
    (pd / "reviews").mkdir(parents=True)
    (pd / "sweeper").mkdir()
    (pd / "board/msgs").mkdir(parents=True)
    (pd / "board/metrics").mkdir()
    sb = tmp / "sb"
    (sb / "cand").mkdir(parents=True)
    (sb / "cand/candidate.md").write_text(CANDIDATE)
    (pd / "inputs.json").write_text(json.dumps({"sandbox": str(sb)}))
    (pd / "t0").write_text(str(T0))
    (pd / "deal_r").write_text("0")
    (pd / "elapsed_s").write_text("110.0")
    (pd / "values.json").write_text(json.dumps({"B_f": B, "k": k, "panel_finish_at_s": fin_s}))
    (pd / "board/msgs/board.jsonl").write_text("".join(json.dumps(f) + "\n" for f in facts))
    (pd / "board/msgs/rejected.jsonl").write_text(json.dumps({"reason": "over_cap"}) + "\n")
    for rid in ("t2b-1", "t4-1", "t3-1"):
        m = {"model_ok": True, "end_ms": T0 + 100_000, "attempts": 1, "reask_s": 0, "dropped_lines": 0, "hang_kill": False}
        m.update((metas or {}).get(rid, {}))
        (pd / f"reviews/{rid}.meta.json").write_text(json.dumps(m))
        (pd / f"reviews/{rid}.cost.json").write_text(json.dumps({"total_output_tokens_all": 10, "retry_s": 0}))
        (pd / f"reviews/{rid}.tags.json").write_text(json.dumps({"lines": (tags or {}).get(rid, [])}))
        (pd / f"reviews/{rid}.attempt1.json").write_text(json.dumps((transcripts or {}).get(rid, [])))
        (pd / f"board/metrics/{rid}.jsonl").write_text("".join(json.dumps(x) + "\n" for x in (metrics or {}).get(rid, [])))
    (pd / "sweeper/sw-1.meta.json").write_text(json.dumps({"model": "muse-ember-1.0", "model_ok": True, "start_ms": T0 + 1, "end_ms": T0 + 50, "output_tokens": 5}))
    (pd / "sweeper/sw-1.json").write_text(json.dumps(sweeper_tr or []))
    return pd


def fact(i, t, **kw):
    f = {"id": f"f-{i}", "t": t, "from": "sw-1", "move": "M1", "anchor": A_T1, "items": ["tests/test_other.py"], "cmd": "grep -rln greeting tests/"}
    f.update(kw)
    return f


def calls(n, t_last, start=1):
    return [{"ev": "call", "t": t_last - (n - c) * 10, "c": c, "ms": 20 + c} for c in range(start, n + 1)]


def run(pd, arm="F4"):
    return CM.compute(pd, "EL2", pd / "values.json", arm, "row", "pkg")


def test_schema_every_field(tmp_path):
    out = run(build(tmp_path))
    for k in CM.TOP_KEYS:
        assert k in out
    for r in out["reviewers"].values():
        assert all(k in r for k in CM.REVIEWER_KEYS)
    assert all(k in out["sweeper"] for k in CM.SWEEPER_KEYS)
    assert out["sweeper"]["over_cap"] == 1 and out["sweeper"]["facts_rejected"] == 1


def test_late_and_isolated(tmp_path):
    # fact 1 is dealt to t3-1 (index 1, r=0) and posted after t3-1's last call
    pd = build(tmp_path, facts=[fact(0, T0 + 1000), fact(1, T0 + 90_000)],
               metrics={"t3-1": calls(8, T0 + 80_000), "t4-1": calls(8, T0 + 80_000) +
                        [{"ev": "deliver", "t": T0 + 70_000, "c": 7, "fact": "f-0", "i": 0}]})
    out = run(pd)
    assert out["reviewers"]["t3-1"]["late"] == 1 and "t3-1" in out["isolated_for"] and "t4-1" not in out["isolated_for"]
    slots = {s["fact"]: s for s in out["slots"]}
    assert slots["f-1"]["late"] and slots["f-0"]["delivered"]


def test_partition_cap_and_other(tmp_path):
    facts = [fact(i, T0 + 1000) for i in range(0, 8, 1)]
    dl = [{"ev": "deliver", "t": T0 + 5000 + i, "c": 6 + i, "fact": f"f-{2 * i}", "i": 2 * i} for i in range(2)]
    pd = build(tmp_path, facts=facts, metrics={"t4-1": calls(10, T0 + 80_000) + dl, "t3-1": calls(10, T0 + 80_000)})
    r = run(pd)["reviewers"]
    assert r["t4-1"]["msgs_received"] == 2 and r["t4-1"]["not_delivered_cap"] == 2 and r["t4-1"]["late"] == 0
    assert r["t3-1"]["not_delivered_other"] == 4
    # every dealt fact is in exactly one class
    for rid in ("t4-1", "t3-1"):
        x = r[rid]
        assert x["msgs_received"] + x["late"] + x["not_delivered_cap"] + x["not_delivered_other"] == 4


def test_delivered_never_above_k(tmp_path):
    dl = [{"ev": "deliver", "t": T0 + i, "c": 6 + i, "fact": f"f-{2 * i}", "i": 2 * i} for i in range(3)]
    pd = build(tmp_path, facts=[fact(i, T0) for i in range(6)], metrics={"t4-1": calls(10, T0 + 9000) + dl}, k=2)
    with pytest.raises(ValueError):
        run(pd)


def _first_hand(tmp_path, read_after):
    reads = [tu(1, "Bash", {"command": "ls"}), tr(1, "x")]
    rd = [tu(9, "Read", {"file_path": "/sb/repo/tests/test_other.py"}), tr(9, "...")]
    seq = (reads * 1 + [tu(2, "Bash", {"command": "ls"})] * 6 + rd) if read_after else (rd + [tu(2, "Bash", {"command": "ls"})] * 7)
    tags = {"t4-1": [{"origin": "peer", "anchor": "x" * 12, "reasons": [{"fact": "f-0", "why": "path", "paths": ["tests/test_other.py"]}]}]}
    pd = build(tmp_path, facts=[fact(0, T0)], transcripts={"t4-1": seq}, tags=tags,
               metrics={"t4-1": calls(8, T0 + 9000) + [{"ev": "deliver", "t": T0 + 6000, "c": 6, "fact": "f-0", "i": 0}]})
    return run(pd)["reviewers"]["t4-1"]


def test_first_hand_read_after_delivery(tmp_path):
    r = _first_hand(tmp_path, True)
    assert r["peer_lines"] == 1 and r["peer_lines_first_hand"] == 1


def test_first_hand_false_when_read_before(tmp_path):
    r = _first_hand(tmp_path, False)
    assert r["peer_lines"] == 1 and r["peer_lines_first_hand"] == 0


@pytest.mark.parametrize("out,mism", [("tests/test_other.py\n", 0), ("tests/test_app.py\n", 1)])
def test_rerun_mismatch(tmp_path, out, mism):
    seq = [tu(i, "Bash", {"command": "ls"}) for i in range(1, 7)] + [tu(7, "Bash", {"command": "grep -rln greeting tests/"}), tr(7, out)]
    pd = build(tmp_path, facts=[fact(0, T0)], transcripts={"t4-1": seq},
               metrics={"t4-1": calls(8, T0 + 9000) + [{"ev": "deliver", "t": T0 + 6000, "c": 6, "fact": "f-0", "i": 0}]})
    r = run(pd)["reviewers"]["t4-1"]
    assert r["reruns"] == 1 and r["rerun_mismatches"] == mism


def test_rerun_count_mismatch(tmp_path):
    seq = [tu(i, "Bash", {"command": "ls"}) for i in range(1, 7)] + [tu(7, "Bash", {"command": "grep -rl x tests | wc -l"}), tr(7, "3\n")]
    f = fact(0, T0, cmd="grep -rl x tests | wc -l", items=[], n=2, move="M2")
    pd = build(tmp_path, facts=[f], transcripts={"t4-1": seq},
               metrics={"t4-1": calls(8, T0 + 9000) + [{"ev": "deliver", "t": T0 + 6000, "c": 6, "fact": "f-0", "i": 0}]})
    assert run(pd)["reviewers"]["t4-1"]["rerun_mismatches"] == 1


def test_cmd_unrun(tmp_path):
    sw = [tu(1, "Bash", {"command": "grep -rln greeting tests/"})]
    pd = build(tmp_path, facts=[fact(0, T0), fact(1, T0, cmd="grep -rn other .")], sweeper_tr=sw)
    assert run(pd)["sweeper"]["cmd_unrun"] == 1


def test_echo_rate(tmp_path):
    tags = {"t4-1": [{"origin": "peer", "anchor": A_T1, "reasons": [{"fact": "f-0", "why": "anchor"}]},
                     {"origin": "peer", "anchor": "every greeting uses the new", "reasons": [{"fact": "f-0", "why": "anchor"}]}]}
    pd = build(tmp_path, facts=[fact(0, T0)], tags=tags,
               metrics={"t4-1": calls(8, T0 + 9000) + [{"ev": "deliver", "t": T0 + 6000, "c": 6, "fact": "f-0", "i": 0}]})
    assert run(pd)["echo_rate"] == 0.5


def test_own_line_jaccard_ignores_peer(tmp_path):
    own = lambda a: {"origin": "own", "anchor": a, "reasons": []}  # noqa: E731
    peer = lambda a: {"origin": "peer", "anchor": a, "reasons": []}  # noqa: E731
    tags = {"t2b-1": [own(A_T1)], "t4-1": [own(A_T2), peer(A_T1)], "t3-1": [own(A_T3), peer(A_T1)]}
    out = run(build(tmp_path, tags=tags))
    assert out["own_line_jaccard"] == 0.0 and out["pairwise_task_jaccard"] > 0.0


def test_finish_would_fire(tmp_path):
    out = run(build(tmp_path, metas={"t4-1": {"end_ms": T0 + 130_000}}, fin_s=120), arm="A1")
    assert out["reviewers"]["t4-1"]["finish_would_fire"] and not out["reviewers"]["t3-1"]["finish_would_fire"]
    assert out["sweeper"] is None and out["isolated_for"] == []
