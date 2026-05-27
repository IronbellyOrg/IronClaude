#!/usr/bin/env python3
"""Update iteration-2/benchmark.json runs[].result for cases 4-11 with_skill
configuration to reflect the new combined assertion grading produced by the
just-completed `grader.py iterations/iteration-2` regrade.

This produces an apples-to-apples baseline for the post-rerun comparison.
Old runs entries are preserved for cases 1-3 and 12 (not in the remediation
acceptance scope). Original `time_seconds`, `tokens`, `tool_calls`, `errors`
counters in the result are preserved (those are runtime telemetry from the
original execution, not assertion-set-dependent). Only `passed`, `failed`,
`total`, `pass_rate`, and `expectations` are updated to reflect the new grading.

Usage: uv run python update-benchmark-with-regraded.py
"""
import json
from pathlib import Path

ROOT = Path("/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2")
EVAL_WS = ROOT / ".dev/eval-workspaces/sc-brainstorm"
ITER2 = EVAL_WS / "iterations/iteration-2"
BENCHMARK = ITER2 / "benchmark.json"

ACCEPTANCE_CASES = {
    4: "code-migrate-pytest-vitest",
    5: "architecture-worker-pool-errors",
    6: "process-contributor-onboarding",
    7: "research-bun-vs-node",
    8: "code-api-caching-tasklist",
    9: "code-feature-flag-task",
    10: "incident-payment-webhook-q1",
    11: "code-duplicate-auth-blind",
}


def main():
    benchmark = json.loads(BENCHMARK.read_text())
    runs = benchmark["runs"]

    updates = []
    for run in runs:
        eval_id = run["eval_id"]
        if eval_id not in ACCEPTANCE_CASES:
            continue
        if run["configuration"] != "with_skill":
            continue

        name = ACCEPTANCE_CASES[eval_id]
        grading_path = ITER2 / f"eval-{name}" / "with_skill" / "grading.json"
        if not grading_path.exists():
            updates.append((eval_id, name, f"NO grading.json at {grading_path}"))
            continue

        grading = json.loads(grading_path.read_text())
        summary = grading["summary"]
        before = (run["result"]["passed"], run["result"]["total"])
        after = (summary["passed"], summary["total"])

        run["result"]["passed"] = summary["passed"]
        run["result"]["failed"] = summary["failed"]
        run["result"]["total"] = summary["total"]
        run["result"]["pass_rate"] = summary["pass_rate"]
        run["expectations"] = grading["expectations"]

        updates.append((eval_id, name, f"{before[0]}/{before[1]} -> {after[0]}/{after[1]} ({summary['pass_rate']:.2%})"))

    benchmark["metadata"]["regraded_at"] = "2026-05-27T16:20:00Z"
    benchmark["metadata"]["regraded_reason"] = "Phase-2 assertions wired additively; baseline regraded for apples-to-apples comparison"
    benchmark["metadata"]["regraded_cases"] = list(ACCEPTANCE_CASES.keys())

    BENCHMARK.write_text(json.dumps(benchmark, indent=2) + "\n")

    print(f"{'Case':<6} {'Name':<35} {'Before -> After':<40}")
    print("-" * 85)
    for eval_id, name, status in updates:
        print(f"{eval_id:<6} {name:<35} {status:<40}")


if __name__ == "__main__":
    main()
