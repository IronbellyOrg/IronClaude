"""T-18 and F-2: arm-level alarms."""

import json

from conftest import TOOLS, run

P = "TASK-WF-designSpec-20261107-075614"


def row(collab, rep, jac=0.2, ledger=10, elapsed=116.0, b_f=116.0, inj=None, snap=0, receivers=3):
    return {"row": f"el2-c{collab}-r{rep}", "panel": "el2", "collab": collab, "rep": rep,
            "packages": {P: {"status": "ok", "ledger_rows": ledger, "elapsed_s": elapsed, "B_f": b_f, "overhead_pct": 100 * (elapsed / b_f - 1)}},
            "collab_counters": {"own_line_jaccard": {P: jac}, "injections_by_move": inj or {"M2": 1}, "snapshot_missing": snap, "receivers": receivers}}


def alarms(root, rows):
    (root / "results").mkdir(exist_ok=True)
    (root / "results" / "results.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    r = run(["uv", "run", "python", str(TOOLS / "alarms.py"), "el2", "--root", str(root)])
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout), r.stderr


def test_convergence_slo_and_drift(root):
    rows = [row(0, 1), row(0, 2), row(0, 3, elapsed=140.0),                     # collab-0 mean Jaccard 0.2, ledger 10
            row(1, 1, jac=0.4), row(1, 2, ledger=7), row(1, 3, elapsed=170.0),  # jaccard fire, ledger fire, slow package
            row(1, 0, jac=0.9)]                                                 # rep 0 (smoke) is ignored
    rep, _ = alarms(root, rows)
    fired = {f["row"] for f in rep["convergence"]["fired"]}
    assert fired == {"el2-c1-r1", "el2-c1-r2"}
    assert rep["arms"]["collab1"]["slo_spent"] == [["el2-c1-r3", P]]  # 170 > 1.35 x B_c (median 116)
    used = {b["rep"]: b["used"] for b in rep["blocks"]}
    assert used == {1: True, 2: True, 3: False}  # block 3: drift 140/116 = 1.21 > 1.10


def test_snapshot_alarm(root):
    rep, _ = alarms(root, [row(0, 1), row(1, 1, snap=2)])
    assert rep["snapshot"]["fired"] == ["el2-c1-r1"]


def test_f2_same_gaps_reported_not_failed(root):
    rows = [row(0, i) for i in range(1, 6)] + [row(1, i, inj={"M2": 1, "M3": 2}) for i in range(1, 6)]
    rep, err = alarms(root, rows)
    assert rep["same_gaps"] is True and "SAME_GAPS" in err
    assert rep["arms"]["collab1"]["injections_by_move"] == {"M2": 5, "M3": 10}


def test_incomplete_row_never_a_partial_ledger_sum(root):
    q = "TASK-WF-design-20261108-041415"
    full = lambda c, rep: dict(row(c, rep), packages={P: row(c, rep)["packages"][P], q: dict(row(c, rep)["packages"][P])})  # noqa: E731
    bad = full(1, 1)
    bad["packages"][q]["status"] = "invalid"
    rep, _ = alarms(root, [full(0, 1), full(0, 2), bad])
    assert rep["convergence"]["fired"] == []  # 10 of 20 rows would have looked like a 50% drop
