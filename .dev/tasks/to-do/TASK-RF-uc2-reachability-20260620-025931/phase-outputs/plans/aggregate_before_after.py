#!/usr/bin/env python3
"""Aggregate 3x-before vs 3x-after eval grading into a comparison table.

Reads with_skill/grading.json from each eval-<case>/ under the before-r{1,2,3}
and after-r{1,2,3} iteration dirs, tallies per-case and per-assertion pass
counts across the 3 reps, and prints a before-vs-after comparison plus a JSON
dump for the report.

Usage:
    uv run python .../aggregate_before_after.py
"""
from __future__ import annotations

import json
from pathlib import Path

WS = Path(
    "/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/eval-workspaces/sc-reflect"
)
ITER = WS / "iterations"
CASES = [
    "uc2-surface-positive-control",
    "uc2-surface-dynamic-dispatch",
    "uc2-surface-test-only-ref",
]
REPS = [1, 2, 3]


def load_grading(side: str, rep: int, case: str) -> dict | None:
    p = ITER / f"{side}-r{rep}" / f"eval-{case}" / "with_skill" / "grading.json"
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def tally(side: str) -> dict:
    out = {}
    for case in CASES:
        per_assertion: dict[str, list[bool]] = {}
        overall_pass = []  # full-pass per rep (all assertions pass)
        reps_present = 0
        for rep in REPS:
            g = load_grading(side, rep, case)
            if g is None:
                continue
            reps_present += 1
            full = g["summary"]["passed"] == g["summary"]["total"] and g["summary"]["total"] > 0
            overall_pass.append(full)
            for e in g["expectations"]:
                per_assertion.setdefault(e["text"], []).append(bool(e["passed"]))
        out[case] = {
            "reps_present": reps_present,
            "full_pass_reps": sum(overall_pass),
            "per_assertion": {
                t: f"{sum(v)}/{len(v)}" for t, v in per_assertion.items()
            },
        }
    return out


def main() -> None:
    before = tally("before")
    after = tally("after")
    report = {"before": before, "after": after}

    print("=" * 78)
    print(f"{'Case':<34}{'BEFORE full-pass':<20}{'AFTER full-pass':<20}")
    print("-" * 78)
    for case in CASES:
        b = before[case]
        a = after[case]
        bcol = f"{b['full_pass_reps']}/{b['reps_present']}" if b["reps_present"] else "n/a"
        acol = f"{a['full_pass_reps']}/{a['reps_present']}" if a["reps_present"] else "n/a"
        print(f"{case:<34}{bcol:<20}{acol:<20}")
    print("=" * 78)

    print("\nPer-assertion pass counts (passed-reps / reps-present):\n")
    for case in CASES:
        print(f"### {case}")
        all_texts = set(before[case]["per_assertion"]) | set(after[case]["per_assertion"])
        for t in sorted(all_texts):
            b = before[case]["per_assertion"].get(t, "—")
            a = after[case]["per_assertion"].get(t, "—")
            print(f"  before {b:<6} after {a:<6} | {t[:70]}")
        print()

    out = ITER.parent / "iterations-before-after-comparison.json"
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"JSON written: {out}")


if __name__ == "__main__":
    main()
