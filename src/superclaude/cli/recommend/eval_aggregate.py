"""Per-model aggregation for the --eval pipeline.

Ports `stats()` and `summarize()` from
`.dev/eval-workspaces/sc-recommend/iteration-1/build_benchmark.py` (the math is
reused verbatim) but re-groups the aggregation axis from
`with_skill|without_skill` to `opus|sonnet|haiku` (the model axis the per-row
best_model selection needs). Adds the `MODE_MATRIX` mapping `none/quick/normal/deep`
to their `(models, runs_per_model)` panels. No model calls; no `anthropic` import.
"""

from __future__ import annotations

import statistics

# Mode -> (models in the panel, runs per model). merged-requirements.md:230-235.
MODE_MATRIX: dict[str, dict] = {
    "none": {"models": [], "runs_per_model": 0},
    "quick": {"models": ["opus"], "runs_per_model": 1},
    "normal": {"models": ["opus", "sonnet"], "runs_per_model": 2},
    "deep": {"models": ["opus", "sonnet", "haiku"], "runs_per_model": 3},
}


def make_run_record(
    *,
    eval_id: int | str,
    eval_name: str,
    model: str,
    run_number: int,
    grading: dict,
    timing: dict | None = None,
) -> dict:
    """Build one per-run record (build_benchmark.py:19-36), grouped by `model`."""
    timing = timing or {}
    passed = sum(1 for e in grading["expectations"] if e["passed"])
    total = len(grading["expectations"])
    return {
        "eval_id": eval_id,
        "eval_name": eval_name,
        "model": model,  # the regrouped axis (was "configuration")
        "run_number": run_number,
        "result": {
            "pass_rate": passed / max(1, total),
            "passed": passed,
            "failed": total - passed,
            "total": total,
            "time_seconds": timing.get("total_duration_seconds", 0.0),
            "tokens": timing.get("total_tokens", 0),
            "tool_calls": timing.get("tool_uses", 0),
            "errors": 0,
        },
        "notes": [timing.get("summary", "")] if timing.get("summary") else [],
    }


def stats(vals: list[float]) -> dict:
    """Mean/stddev/min/max — ported verbatim from build_benchmark.py:39-47."""
    if not vals:
        return {"mean": 0, "stddev": 0, "min": 0, "max": 0}
    return {
        "mean": round(statistics.mean(vals), 4),
        "stddev": round(statistics.stdev(vals), 4) if len(vals) > 1 else 0,
        "min": round(min(vals), 4),
        "max": round(max(vals), 4),
    }


def summarize(runs: list[dict], model: str, key: str) -> dict:
    """Aggregate `result[key]` over all runs of `model` (was grouped by configuration)."""
    vals = [r["result"][key] for r in runs if r["model"] == model]
    return stats(vals)


def aggregate_by_model(runs: list[dict]) -> dict[str, dict]:
    """Per-model summary of pass_rate / time_seconds / tokens across `runs`.

    Returns ``{model: {pass_rate, mean_tokens, mean_duration_s, n_runs}}`` — the
    shape the best_model tier selection consumes.
    """
    models = sorted({r["model"] for r in runs})
    out: dict[str, dict] = {}
    for model in models:
        model_runs = [r for r in runs if r["model"] == model]
        out[model] = {
            "pass_rate": summarize(runs, model, "pass_rate")["mean"],
            "mean_tokens": summarize(runs, model, "tokens")["mean"],
            "mean_duration_s": summarize(runs, model, "time_seconds")["mean"],
            "n_runs": len(model_runs),
        }
    return out
