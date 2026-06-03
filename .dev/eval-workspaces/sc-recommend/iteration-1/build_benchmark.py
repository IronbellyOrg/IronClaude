#!/usr/bin/env python3
"""Build benchmark.json from per-eval grading.json + timing.json."""
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).parent
RUNS = []

for eval_dir in sorted(ROOT.glob("eval-*")):
    for cfg in ("with_skill", "without_skill"):
        rd = eval_dir / cfg
        if not (rd / "grading.json").exists():
            continue
        g = json.loads((rd / "grading.json").read_text())
        t = json.loads((rd / "timing.json").read_text()) if (rd / "timing.json").exists() else {}
        passed = sum(1 for e in g["expectations"] if e["passed"])
        total = len(g["expectations"])
        RUNS.append({
            "eval_id": g["eval_id"],
            "eval_name": g["eval_name"],
            "configuration": cfg,
            "run_number": 1,
            "result": {
                "pass_rate": passed / max(1, total),
                "passed": passed,
                "failed": total - passed,
                "total": total,
                "time_seconds": t.get("total_duration_seconds", 0.0),
                "tokens": t.get("total_tokens", 0),
                "tool_calls": t.get("tool_uses", 0),
                "errors": 0,
            },
            "expectations": g["expectations"],
            "notes": [t.get("summary", "")] if t.get("summary") else [],
        })


def stats(vals: list[float]) -> dict:
    if not vals:
        return {"mean": 0, "stddev": 0, "min": 0, "max": 0}
    return {
        "mean": round(statistics.mean(vals), 4),
        "stddev": round(statistics.stdev(vals), 4) if len(vals) > 1 else 0,
        "min": round(min(vals), 4),
        "max": round(max(vals), 4),
    }


def summarize(cfg: str, key: str) -> dict:
    vals = [r["result"][key] for r in RUNS if r["configuration"] == cfg]
    return stats(vals)


run_summary = {
    "with_skill": {
        "pass_rate": summarize("with_skill", "pass_rate"),
        "time_seconds": summarize("with_skill", "time_seconds"),
        "tokens": summarize("with_skill", "tokens"),
    },
    "without_skill": {
        "pass_rate": summarize("without_skill", "pass_rate"),
        "time_seconds": summarize("without_skill", "time_seconds"),
        "tokens": summarize("without_skill", "tokens"),
    },
    "delta": {
        "pass_rate": round(
            summarize("with_skill", "pass_rate")["mean"]
            - summarize("without_skill", "pass_rate")["mean"], 4),
        "time_seconds": round(
            summarize("with_skill", "time_seconds")["mean"]
            - summarize("without_skill", "time_seconds")["mean"], 4),
        "tokens": round(
            summarize("with_skill", "tokens")["mean"]
            - summarize("without_skill", "tokens")["mean"], 4),
    },
}

benchmark = {
    "metadata": {
        "skill_name": "sc-recommend",
        "skill_path": str(ROOT.parent.parent.parent / "src/superclaude/skills/sc-recommend"),
        "executor_model": "claude-opus-4-7 (parent) + general-purpose subagents (default model)",
        "analyzer_model": "claude-opus-4-7",
        "timestamp": "2026-06-02T13:35:00Z",
        "evals_run": sorted({r["eval_id"] for r in RUNS}),
        "runs_per_configuration": 1,
        "notes": "Iteration 1 — single run per configuration (12 subagents total, fanned out in one message). Length-cap assertions for evals 3 and 4 are overly tight; surfaced as a finding rather than a true skill regression."
    },
    "runs": RUNS,
    "run_summary": run_summary,
}

(ROOT / "benchmark.json").write_text(json.dumps(benchmark, indent=2) + "\n")
print(f"Wrote benchmark.json — {len(RUNS)} runs")
print(f"  with_skill pass_rate: {run_summary['with_skill']['pass_rate']['mean']*100:.0f}%")
print(f"  without_skill pass_rate: {run_summary['without_skill']['pass_rate']['mean']*100:.0f}%")
print(f"  delta: {run_summary['delta']['pass_rate']*100:+.0f}%")
print(f"  with_skill tokens (mean): {run_summary['with_skill']['tokens']['mean']:.0f}")
print(f"  without_skill tokens (mean): {run_summary['without_skill']['tokens']['mean']:.0f}")
print(f"  with_skill time (mean): {run_summary['with_skill']['time_seconds']['mean']:.1f}s")
print(f"  without_skill time (mean): {run_summary['without_skill']['time_seconds']['mean']:.1f}s")
