# ruff: noqa: N803  (B is the design's own symbol)
"""T-12: timing values and the Spike 4 turn extraction (R-41..R-43)."""

import importlib.util
import json

import pytest
from conftest import TOOLS, jload, run

spec = importlib.util.spec_from_file_location("values", TOOLS / "values.py")
V = importlib.util.module_from_spec(spec)
spec.loader.exec_module(V)


def ts(s):
    return f"2026-11-13T10:00:{s:06.3f}Z"


def attempt_fixture():
    a = lambda mid, t, kind="text": {"type": "assistant", "timestamp": ts(t), "parent_tool_use_id": None,  # noqa: E731
                                     "message": {"id": mid, "content": [{"type": kind}]}}
    tr = lambda t: {"type": "user", "timestamp": ts(t), "parent_tool_use_id": None,  # noqa: E731
                    "message": {"content": [{"type": "tool_result"}]}}
    return [
        {"type": "system", "subtype": "init"},                      # untimed
        a("r1", 1.0, "thinking"), a("r1", 1.5, "tool_use"),          # first response: no earlier tool result -> no turn
        tr(2.0),
        a("r2", 3.0, "thinking"), a("r2", 3.5, "tool_use"), a("r2", 4.0, "tool_use"),  # split over 3 entries, 2 parallel calls
        tr(4.5), tr(4.6),
        a("r3", 6.6, "tool_use"),                                    # 2.0 s after the latest tool result
        tr(7.0),
        {"type": "assistant", "timestamp": ts(8.0), "parent_tool_use_id": "sub", "message": {"id": "s1"}},  # subagent: ignored
        a("r4", 9.0, "thinking"), a("r4", 27.0, "text"),             # final report response: 20 s
        {"type": "result", "result": "x"},
    ]


def test_turn_extraction():
    inner, final = V.turns_of(attempt_fixture())
    assert inner == pytest.approx([2.0, 2.0])  # r2: 4.0 - 2.0; r3: 6.6 - 4.6; r1 left out
    assert final == pytest.approx(20.0)


@pytest.mark.parametrize("B,turn,trep,k", [(116, 6.4, 6.4, 2), (116, 6.4, 11.0, 1), (100, 6.4, 13.8, 1), (100, 6.4, 13.9, 0),
                                            # SL2: the exact bound is 51.795 s, which the design rounds to 51.8
                                            (273.7, 14, 51.79, 1), (273.7, 14, 51.81, 0), (238, 23, 23, 0), (238, 23, 12.3, 1),
                                            (238, 23, 12.4, 0)])
def test_r42(B, turn, trep, k):
    assert V.k_for(B, turn, trep) == k


def test_planning_values():
    cfg = jload(TOOLS.parent / "config" / "panels.json")
    el2, sl2, hl2 = (V.planning(p, cfg[p]) for p in ("el2", "sl2", "hl2"))
    assert el2["finish_offset_s"] == pytest.approx(143.8, abs=0.1)
    assert el2["guard_offset_s"] == pytest.approx(109.6, abs=0.1)
    assert sl2["guard_offset_s"] == pytest.approx(266.7, abs=0.1)
    assert hl2["guard_offset_s"] == pytest.approx(152.4, abs=0.1)
    assert hl2["k"] == {"searcher": 0, "reader": 2}  # A-2 reader k on hl2 planning
    assert el2["k"] == {"reader": 2, "searcher": 2}  # el2 never uses A-2: reader k = searcher k = crit k
    # el2 with a slow reader: the searcher still takes the critical k (no A-2)
    v = V.compute("el2", cfg["el2"], 116, {"searcher": 3.2, "reader": 6.4}, {"searcher": 3.2, "reader": 11.0}, {"reader": 140})
    assert v["k"] == {"reader": 1, "searcher": 1}
    assert el2["hang_offset_s"] == pytest.approx(174)


def _row(root, row, pkg, t0, ends, attempt):
    d = root / "runs" / row / pkg
    (d / "reviews").mkdir(parents=True)
    (d / "run.json").write_text(json.dumps({"T0_MS": t0}))
    for rid, end in ends.items():
        (d / "reviews" / f"{rid}.meta.json").write_text(json.dumps({"end_ms": end, "attempts": 1}))
        (d / "reviews" / f"{rid}.attempt1.json").write_text(json.dumps(attempt))


def test_spike4_refusals_and_write(root):
    pk = V.PKGS
    for i, row in enumerate(["el2-c0-r1", "el2-c0-r2", "el2-c0-r3"]):
        for p in pk:
            _row(root, row, p, 0, {"t2b-1": 100_000 + i * 1000, "t4-1": 110_000, "t3-1": 120_000 + i * 2000}, attempt_fixture())
    r = run(["uv", "run", "python", str(TOOLS / "values.py"), "spike4", "el2", "el2-c0-r1", "el2-c0-r2", "--root", str(root)])
    assert r.returncode == 2 and "at least 3" in r.stderr
    r = run(["uv", "run", "python", str(TOOLS / "values.py"), "spike4", "el2", "el2-c0-r1", "el2-c0-r2", "el2-c0-r3", "--root", str(root)])
    assert r.returncode == 0, r.stderr
    v = jload(root / "values" / "el2" / f"{pk[0]}.json")
    assert v["B_f"] == pytest.approx(122.0) and v["turn_p90"]["reader"] == pytest.approx(2.0) and v["T_report_p90"]["reader"] == pytest.approx(20.0)
    assert (root / "values" / "el2" / f"{pk[0]}.json.sha256").exists()
    r = run(["uv", "run", "python", str(TOOLS / "values.py"), "spike4", "el2", "el2-c0-r1", "el2-c0-r2", "el2-c0-r3", "--root", str(root)])
    assert r.returncode == 2 and "written once" in r.stderr
    d = json.loads(run(["uv", "run", "python", str(TOOLS / "values.py"), "deadlines", "el2", pk[0], "1", "1000", "--root", str(root)]).stdout)
    assert d["HANG_MS"] == 1000 + round(1000 * 1.5 * 122.0) and d["values"] != "planning"


def test_deadlines_planning_and_refusal(root):
    pk = V.PKGS[0]
    r = run(["uv", "run", "python", str(TOOLS / "values.py"), "deadlines", "sl2", pk, "1", "0", "--root", str(root)])
    assert r.returncode == 2
    d = json.loads(run(["uv", "run", "python", str(TOOLS / "values.py"), "deadlines", "sl2", pk, "0", "0", "--root", str(root)]).stdout)
    assert d["values"] == "planning" and d["HANG_MS"] == round(1000 * 2.0 * 273.7)  # 547.4 s
