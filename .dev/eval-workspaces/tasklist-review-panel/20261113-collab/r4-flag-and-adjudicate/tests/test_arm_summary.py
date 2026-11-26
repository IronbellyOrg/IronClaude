"""lib/arm_summary.py (design 2.9) on fixture results rows, plus the arm-level fault injections of 6.2."""

import math

import arm_summary as asum
import pytest

P3 = {"DS": "TASK-WF-designSpec-20261107-075614", "AL": "TASK-WF-makeTheAliasOnly-20261105-051649", "DE": "TASK-WF-design-20261108-041415"}


def row(name, cards=2, ffo=0.0, jac=0.2, lrows=10, recv=1, miss=0, conv=(1, 2, 1, 2), el=100.0, reach=False, audit_ok=True,
        found=4, wb=2, cwb=1, hang=False, bf=100.0):
    collab = {}
    for i, p in enumerate(P3.values()):
        collab[p] = {"cards_sent": cards if i == 0 else 0, "flag_finding_overlap": ffo if i == 0 and cards else None,
                     "own_line_jaccard": jac, "ledger_rows": lrows, "receiving_lunas": recv if i == 0 else 0,
                     "snapshot_missing": miss if i == 0 else 0, "hang_kill": hang and i == 0, "baseline_elapsed_s": bf,
                     "conversions": {"challenge": {"converted": conv[0], "delivered": conv[1]},
                                     "finding": {"converted": conv[2], "delivered": conv[3]}} if i == 0 else {}}
    return {"row": name, "valid": True, "collab": collab, "elapsed_s": {s: el for s in P3}, "reach": reach,
            "reach_ids": ["DS:GT1"] if reach else [], "audit": {"audit_ok": audit_ok, "harness_text_gt_overlap": 0},
            "found_14": found, "wrong_blockers": wb, "control_wrong_blockers": cwb, "overhead_pct": {s: 10.0 for s in P3}}


A1 = [row(f"a{i}", cards=0, ffo=None) for i in range(12)]


def test_no_cards_stop():
    arm = [row(f"f{i}", cards=0 if i < 7 else 2) for i in range(12)]
    assert asum.summarize("EL2", A1, arm)["STOP:no_cards"] is True
    arm = [row(f"f{i}", cards=0 if i < 6 else 2) for i in range(12)]
    assert asum.summarize("EL2", A1, arm)["STOP:no_cards"] is False


def test_flag_finding_overlap_stop():
    out = asum.summarize("EL2", A1, [row(f"f{i}", ffo=0.6) for i in range(12)])
    assert out["STOP:flag_finding_overlap"] is True and out["flag_finding_overlap_pooled"] == pytest.approx(0.6)


def test_convergence_jaccard_and_rows():
    out = asum.summarize("EL2", A1, [row("f1", jac=0.2 + 0.16), row("f2", lrows=7.9), row("f3")])
    fired = {c["row"]: c["fired"] for c in out["CONVERGENCE"]}
    assert fired == {"f1": True, "f2": True, "f3": False}


def test_snapshot_alarm():
    arm = [row("f1", recv=1, miss=1), row("f2", recv=1, miss=1), row("f3", recv=1, miss=1), row("f4", recv=1, miss=0)]
    assert asum.summarize("EL2", A1, arm)["SNAPSHOT"] is True


def test_agreement_both_ways():
    assert asum.summarize("EL2", A1, [row("f", conv=(19, 20, 0, 0))])["AGREEMENT"] is True     # 0.95
    assert asum.summarize("EL2", A1, [row("f", conv=(1, 25, 0, 0))])["AGREEMENT"] is True      # 0.04
    assert asum.summarize("EL2", A1, [row("f", conv=(1, 2, 0, 0))])["AGREEMENT"] is False


def test_slo_budget():
    def arm_with(n_slow):
        rows = [row(f"f{i}") for i in range(12)]
        for i in range(n_slow):
            rows[i]["elapsed_s"]["DS"] = 136.0
        return rows
    assert asum.summarize("EL2", A1, arm_with(4))["slo"]["budget_exceeded"] is True   # 4/36
    assert asum.summarize("EL2", A1, arm_with(3))["slo"]["budget_exceeded"] is False  # 3/36


def test_independence_fails_on_audit():
    arm = [row(f"f{i}") for i in range(12)]
    arm[3]["audit"]["audit_ok"] = False
    assert asum.summarize("EL2", A1, arm)["independence"]["pass"] is False


@pytest.mark.parametrize("a,b,p", [(4, 0, 0.047), (6, 1, 0.034), (7, 2, 0.045)])
def test_fisher(a, b, p):
    assert round(asum.fisher_one_sided(a, 12, b, 12), 3) == p
    arm = [row(f"f{i}", reach=i < a) for i in range(12)]
    a1 = [row(f"a{i}", reach=i < b) for i in range(12)]
    assert round(asum.summarize("EL2", a1, arm)["reach"]["fisher_p"], 3) == p


def test_form_contrast():
    arm = [row("f1", conv=(2, 3, 1, 3)), row("f2", conv=(1, 2, 0, 2)), row("f3", conv=(1, 1, 0, 0))]
    fc = asum.summarize("EL2", A1, arm)["form_contrast"]
    assert fc["challenge"] == [4, 6] and fc["finding"] == [1, 5]
    p = 5 / 11
    z = (4 / 6 - 1 / 5) / math.sqrt(p * (1 - p) * (1 / 6 + 1 / 5))
    assert fc["z"] == pytest.approx(z)
    assert fc["run_paired_mean_diff"] == pytest.approx(((2 / 3 - 1 / 3) + (1 / 2 - 0)) / 2)


def test_no_loss_fails_on_wrong_blockers():
    out = asum.summarize("EL2", A1, [row(f"f{i}", wb=3.5) for i in range(12)])  # A1 2 + 1.5
    assert out["no_loss"]["pass"] is False


def test_no_cards_fault_row_counts():
    arm = [row(f"f{i}", cards=0) for i in range(7)] + [row(f"g{i}") for i in range(5)]
    assert asum.summarize("EL2", A1, arm)["no_cards_runs"] == 7


def test_drift_band():
    sched = [{"row": "a0", "block": "b1"}, {"row": "f0", "block": "b1"}, {"row": "a1", "block": "b2"}, {"row": "f1", "block": "b2"}]
    a1 = [row("a0", el=100.0), row("a1", el=120.0)]
    arm = [row("f0", el=100.0), row("f1", el=200.0)]
    out = asum.summarize("EL2", a1, arm, sched)
    assert out["blocks_excluded_from_time_verdict"] == ["b2"]
    assert out["time_verdict"]["DS"]["median"] == 100.0
