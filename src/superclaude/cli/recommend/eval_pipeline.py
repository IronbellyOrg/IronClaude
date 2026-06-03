"""--eval pipeline driver (Option P: Python owns grade/aggregate/select/write/patch).

The model runs themselves are subprocess/Agent-based — the SKILL.md prose emits the
parallel per-(model, run) Agent-tool calls (the `anthropic` SDK is BANNED; there is
NO in-process model call here). Each Agent writes its deliverable
(`outputs/recommendation.md`) and a `timing.json` under the eval-runs tree. This
module then:
  1. collects + grades each run (eval_grader),
  2. aggregates per model (eval_aggregate),
  3. selects best_model deterministically (best_model),
  4. writes `row-<key>-results.json`,
  5. patches the lookup row's `best_model` + appends `eval_history` via the atomic
     `LookupCache.save()` writer.

Run-dir layout (NEW convention):
  .claude/cache/eval-runs/iteration-<N>/<key>/<model>/run-<i>/outputs/recommendation.md
  .claude/cache/eval-runs/iteration-<N>/<key>/<model>/run-<i>/timing.json
"""

from __future__ import annotations

import json
from pathlib import Path

from .best_model import select_best_model
from .cache import LookupCache, compute_surface_hash
from .eval_aggregate import MODE_MATRIX, aggregate_by_model, make_run_record
from .eval_grader import grade_text


def collect_run_records(
    *,
    eval_runs_dir: Path,
    key: str,
    mode: str,
    eval_name: str,
    assertions: list[dict],
) -> list[dict]:
    """Grade every per-(model, run) deliverable under the iteration dir for `key`.

    Reads each run's `outputs/recommendation.md` + `timing.json`, grades the text
    against `assertions`, and returns per-run records grouped by model.
    """
    panel = MODE_MATRIX.get(mode, MODE_MATRIX["none"])
    records: list[dict] = []
    key_dir = eval_runs_dir / key
    for model in panel["models"]:
        for run_number in range(1, panel["runs_per_model"] + 1):
            run_dir = key_dir / model / f"run-{run_number}"
            out = run_dir / "outputs" / "recommendation.md"
            text = out.read_text(encoding="utf-8") if out.exists() else ""
            timing_path = run_dir / "timing.json"
            timing = (
                json.loads(timing_path.read_text(encoding="utf-8"))
                if timing_path.exists()
                else {}
            )
            grading = grade_text(
                eval_id=key,
                eval_name=eval_name,
                configuration=model,
                assertions=assertions,
                text=text,
                output_exists=out.exists(),
            )
            records.append(
                make_run_record(
                    eval_id=key,
                    eval_name=eval_name,
                    model=model,
                    run_number=run_number,
                    grading=grading,
                    timing=timing,
                )
            )
    return records


def finalize_eval(
    *,
    key: str,
    iteration: int,
    mode: str,
    runs: list[dict],
    eval_runs_dir: Path,
    cache_path: Path,
    tier: str = "balanced",
    date: str | None = None,
) -> dict:
    """Aggregate runs, select best_model, write results JSON, patch the lookup row.

    Returns the results dict that was written to `row-<key>-results.json`.
    """
    per_model = aggregate_by_model(runs)
    run_id = f"iteration-{iteration}"
    best = select_best_model(per_model, tier=tier, based_on=run_id)

    results = {
        "key": key,
        "run_id": run_id,
        "eval_mode": mode,
        "models_tested": sorted(per_model.keys()),
        "per_model": per_model,
        "best_model": best,
        "runs": runs,
    }

    # 1. Write the results JSON.
    out_path = eval_runs_dir / f"row-{key}-results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")

    # 2. Patch the lookup row's best_model + append eval_history (atomic writer).
    surface_hash = compute_surface_hash()
    cache = LookupCache.load_or_create(cache_path, surface_hash)
    row = cache.get_row(key)
    if row is not None:
        # best_model is suppressed (model-agnostic) -> store None hint.
        row["best_model"] = None if best.get("suppressed") else best
        history = row.setdefault("eval_history", [])
        history.append(
            {
                "run_id": run_id,
                "date": date,
                "eval_mode": mode,
                "models_tested": results["models_tested"],
                "results": {
                    m: {
                        "pass_rate": v["pass_rate"],
                        "mean_tokens": v["mean_tokens"],
                        "mean_duration_s": v["mean_duration_s"],
                        "n_runs": v["n_runs"],
                    }
                    for m, v in per_model.items()
                },
                "verdict": "model-agnostic"
                if best.get("suppressed")
                else best["model"],
            }
        )
        cache.upsert_row(row)
        cache.save()

    return results
