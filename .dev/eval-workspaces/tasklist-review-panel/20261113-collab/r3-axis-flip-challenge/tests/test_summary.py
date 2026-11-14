from r3lib import metrics

P = "TASK-WF-design-20261108-041415"


def row(arm, el, reach=False, oj=0.2, lr=10):
    return {
        "panel": "el2",
        "arm": arm,
        "values_status": "frozen",
        "run_id": arm,
        "invalid_pkgs": [],
        "judge_ok": True,
        "contaminated": False,
        "found14": 1,
        "real_blocking8": 0,
        "judge_blocking": 0,
        "wrong_blockers": 0,
        "control_found2": 1,
        "reach": reach,
        "target_hits": ["I7"] if reach else [],
        "elapsed_s": {P: el},
        "slo_breach": {P: False},
        "collab": {
            "own_line_jaccard": {P: oj},
            "ledger_rows": {P: lr},
            "echo_rate": {P: 0.5},
        },
    }


def test_cap_and_convergence():
    rows = [row("A1", 100) for _ in range(3)] + [
        row("A3", 140),
        row("A3", 160, oj=0.5),
        row("A3", 120, lr=5),
    ]
    s = metrics.summarize(rows, "el2")
    cap = s["cap_check"][P]
    assert cap["median_ok"] is False and cap["over_135"] == 2 and cap["over_150"] == 1
    assert s["convergence"] == 2 and s["echo"] == 3
    d = metrics.summarize(rows, "el2", {P: 95.0})["baseline_drift"][P]
    assert abs(d["drift"] - 100 / 95) < 1e-9 and d["in_band"] is True
    assert (
        metrics.summarize(rows, "el2", {P: 80.0})["baseline_drift"][P]["in_band"]
        is False
    )


def test_fisher():
    assert abs(metrics.fisher_one_sided(0, 12, 4, 12) - 495 / 10626) < 1e-9


def test_refuses_planning_rows():
    import pytest

    r = row("A1", 100)
    r["values_status"] = "planning"
    with pytest.raises(SystemExit):
        metrics.summarize([r], "el2")
