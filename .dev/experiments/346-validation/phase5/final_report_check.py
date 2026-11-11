"""Recompute the final report's numeric companion; no model calls or experiments.

Run with UV and --write once to create final-summary.json, then without flags
for a read-only reproducibility and report-integrity check. Source measurements
are retained rather than overwritten when a comparison raises a disagreement.
"""

import argparse
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORKTREES = HERE.parents[4]
START = 57763


def load(path):
    return json.loads(path.read_text())


def growth(size):
    return (size - START) / START * 100


def build_summary():
    sources = {}
    runs = {}
    for arm in ("ctl-r1", "ctl-r2", "trt-r1", "trt-r2", "flg-r1", "flg-r2"):
        path = WORKTREES / f"exp346-ab-{arm}/.dev/experiments/346-validation/phase4/{arm}/metrics.json"
        doc = load(path)
        counts = [r["M2"]["critical_plus_major"] for r in doc["rounds"]]
        # One original recorder named the same per-round total all_findings.
        totals = [r["M2"]["all_findings" if arm == "trt-r2" else "findings_total"]
                  for r in doc["rounds"]]
        size = doc["rounds"][-1]["M4"]["bytes_at_review_start"]
        assert len(counts) == 3 and all(isinstance(n, int) for n in counts)
        runs[arm] = {"new_label_proxy": counts, "new_findings_total": totals,
                     "endpoint_bytes": size, "growth_percent": growth(size),
                     "source": str(path.relative_to(WORKTREES))}
        sources[str(path.relative_to(WORKTREES))] = hashlib.sha256(path.read_bytes()).hexdigest()

    variants = {}
    for variant in ("diffgate", "ponytail", "ledger"):
        path = WORKTREES / f"exp346-v-{variant}/.dev/experiments/346-validation/phase5/{variant}/metrics.json"
        doc = load(path)
        sources[str(path.relative_to(WORKTREES))] = hashlib.sha256(path.read_bytes()).hexdigest()
        if variant == "ledger":
            counts = [r["critical_plus_major_new"] for r in doc["rounds"]]
            size = doc["spec_sizes"]["v3_after_cycle2"]["bytes"]
            details = doc["separate_counts"]
            endpoint = {"unresolved_prior_labels": details["2_unresolved_prior_cm_labels_at_R3"]["count"],
                        "owner_deferred_including_sweep": details["4_owner_cumulative_cm_deferred_demoted_withdrawn"]["count"],
                        "script_headline": details["5_script_metrics"]["headline_raw"],
                        "audit_union_point": details["8_union_cm_audit_augmented"]["point_estimate"],
                        "audit_union_bounds": [details["8_union_cm_audit_augmented"]["lower_bound"], details["8_union_cm_audit_augmented"]["upper_bound"]]}
        else:
            counts = [r["M2"]["critical_plus_major"] for r in doc["rounds"]]
            size = (doc["growth_summary"]["after_cycle_2_endpoint_bytes"] if variant == "diffgate"
                    else doc["sizes"]["endpoint_after_audit"]["bytes"])
            endpoint = ({"unresolved_prior_labels": 0, "owner_deferred": 0,
                         "audit_union_recorder_point": 6, "audit_union_review_sensitive_bounds": [5, 6]}
                        if variant == "diffgate" else
                        {"unresolved_prior_blockers": 0, "owner_carry_conservative": 1,
                         "owner_carry_interpretation_bounds": [0, 1], "audit_saved_bytes": 91,
                         "full_document_audit_union": None})
        variants[variant] = {"completed_loops": 1, "new_label_proxy": counts,
                             "endpoint_bytes": size, "growth_percent": growth(size),
                             "valid_repeated_success": False, "endpoint_details": endpoint,
                             "source": str(path.relative_to(WORKTREES))}

    control_counts = [runs[n]["new_label_proxy"][-1] for n in ("ctl-r1", "ctl-r2")]
    assert control_counts == [8, 4]
    assert variants["diffgate"]["new_label_proxy"] == [7, 2, 2]
    assert variants["ponytail"]["new_label_proxy"] == [9, 7, 0]
    assert variants["ledger"]["new_label_proxy"] == [13, 9, 3]
    assert variants["ponytail"]["endpoint_bytes"] == 70488
    assert variants["ledger"]["endpoint_details"]["script_headline"] == 15
    return {"scenario": "S1 worker-contract specification", "starting_bytes": START,
            "convergence_proven": False, "original_427_runs": runs, "measured_variants": variants,
            "fixed_screen": {"control_mean_new_final_labels": 6, "label_limit": 3,
                             "control_label_range": 4, "rounded_control_mean_growth_percent": 63.51,
                             "fixed_growth_limit_percent": 44.457},
            "recomputed_control_mean_growth_percent": sum(runs[n]["growth_percent"] for n in ("ctl-r1", "ctl-r2")) / 2,
            "failed_or_unbuilt": {"stoprule": "invalidated at first-review transcript check; no completed loop",
                                  "minfix": "two tasks complete; task 3 halted; no runnable experiment command"},
            "exploratory_repeats": "paused; four first reviews only, no revised endpoints; not successful replicates",
            "union_caveat": "Audit unions are not directly comparable with unaudited control new-label counts.",
            "source_sha256": sources}


def check_report(summary):
    report = HERE / "FINAL-REPORT.md"
    text = report.read_text()
    assert "RF_PLACEHOLDER" not in text and "<!-- TODO -->" not in text
    assert "not proven" in text and "coordinator" in text.lower()
    assert all(glyph not in text for glyph in ("—", "–"))
    for n in ("63,717", "70,488", "70,565", "44.457%", "5-6", "11-14"):
        assert n in text, f"Missing report comparison token: {n}"
    for target in re.findall(r"\]\(([^)]+)\)", text):
        if target.startswith(("#", "http:", "https:")):
            continue
        assert (report.parent / target.split("#")[0]).exists(), target
    assert summary["measured_variants"]["diffgate"]["growth_percent"] < 10.31
    assert 22.02 < summary["measured_variants"]["ponytail"]["growth_percent"] < 22.04
    assert 22.15 < summary["measured_variants"]["ledger"]["growth_percent"] < 22.17


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    summary = build_summary()
    check_report(summary)
    path = HERE / "final-summary.json"
    if args.write:
        # Exclusive creation prevents silently replacing a prior calculation.
        with path.open("x") as output:
            json.dump(summary, output, indent=2)
            output.write("\n")
    assert load(path) == summary, "Summary differs from its pinned source measurements"
    print("PASS: 9 source measurements, endpoint arithmetic, numeric assertions, local report links and no placeholders")


if __name__ == "__main__":
    main()
