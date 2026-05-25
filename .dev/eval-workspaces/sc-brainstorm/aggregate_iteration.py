#!/usr/bin/env python3
import json
import math
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def summarize(values: list[float]) -> dict:
    mean = sum(values) / len(values) if values else 0.0
    variance = sum((v - mean) ** 2 for v in values) / len(values) if values else 0.0
    return {"mean": mean, "stddev": math.sqrt(variance), "count": len(values)}


def run_record(eval_id: int, configuration: str, eval_dir: Path) -> dict:
    run_dir = eval_dir / configuration / "run-1"
    grading = read_json(run_dir / "grading.json")
    timing = read_json(run_dir / "timing.json")
    summary = grading["summary"]
    return {
        "eval_id": eval_id,
        "eval_name": eval_dir.name.removeprefix("eval-"),
        "configuration": configuration,
        "run_number": 1,
        "result": {
            "pass_rate": summary["pass_rate"],
            "passed": summary["passed"],
            "failed": summary["failed"],
            "total": summary["total"],
            "time_seconds": timing["total_duration_seconds"],
            "tokens": timing["total_tokens"],
            "tool_calls": timing.get("tool_uses", 0),
            "errors": summary["failed"],
        },
        "expectations": grading["expectations"],
        "notes": [],
    }


def build_benchmark(iter_dir: Path) -> dict:
    runs = []
    eval_ids = []
    for eval_dir in sorted(iter_dir.glob("eval-*")):
        meta = read_json(eval_dir / "eval_metadata.json")
        eval_id = int(meta["eval_id"])
        eval_ids.append(eval_id)
        runs.append(run_record(eval_id, "old_skill", eval_dir))
        runs.append(run_record(eval_id, "with_skill", eval_dir))

    groups = {"old_skill": [], "with_skill": []}
    for run in runs:
        groups[run["configuration"]].append(run)

    summary = {}
    for config, config_runs in groups.items():
        summary[config] = {
            "pass_rate": summarize([r["result"]["pass_rate"] for r in config_runs]),
            "time_seconds": summarize([r["result"]["time_seconds"] for r in config_runs]),
            "tokens": summarize([r["result"]["tokens"] for r in config_runs]),
            "tool_calls": summarize([r["result"]["tool_calls"] for r in config_runs]),
            "errors": sum(r["result"]["errors"] for r in config_runs),
        }

    return {
        "metadata": {
            "skill_name": "sc-brainstorm-protocol",
            "skill_path": "src/superclaude/skills/sc-brainstorm-protocol/SKILL.md",
            "executor_model": "claude-opus-4-7[1m]",
            "analyzer_model": "claude-opus-4-7[1m]",
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "evals_run": sorted(eval_ids),
            "runs_per_configuration": 1,
        },
        "runs": sorted(runs, key=lambda r: (r["configuration"], r["eval_id"])),
        "run_summary": summary,
    }


def write_markdown(iter_dir: Path, benchmark: dict) -> None:
    old = benchmark["run_summary"]["old_skill"]
    new = benchmark["run_summary"]["with_skill"]

    def fmt_metric(group: dict, key: str, suffix: str = "") -> str:
        s = group[key]
        return f"{s['mean']:.1f}{suffix} ± {s['stddev']:.1f}"

    pass_old = old["pass_rate"]["mean"] * 100
    pass_new = new["pass_rate"]["mean"] * 100
    delta_time = old["time_seconds"]["mean"] - new["time_seconds"]["mean"]
    delta_tokens = old["tokens"]["mean"] - new["tokens"]["mean"]
    quality = read_json(iter_dir / "quality-grading.json") if (iter_dir / "quality-grading.json").exists() else {}
    q = quality.get("aggregate_totals", {})
    lines = [
        "# Skill Benchmark: sc-brainstorm-protocol",
        "",
        "**Model**: claude-opus-4-7[1m]",
        f"**Date**: {benchmark['metadata']['timestamp']}",
        f"**Evals**: {', '.join(map(str, benchmark['metadata']['evals_run']))} (1 run per configuration)",
        "",
        "## Summary",
        "",
        "| Metric | Old Skill | With Skill | Delta |",
        "|--------|------------|------------|-------|",
        f"| Pass Rate | {pass_old:.0f}% | {pass_new:.0f}% | {pass_new - pass_old:+.0f}pp |",
        f"| Time | {fmt_metric(old, 'time_seconds', 's')} | {fmt_metric(new, 'time_seconds', 's')} | {delta_time:+.1f}s |",
        f"| Tokens | {fmt_metric(old, 'tokens')} | {fmt_metric(new, 'tokens')} | {delta_tokens:+.0f} |",
    ]
    if q:
        lines.extend([
            "",
            "## Strict Quality Re-grade",
            "",
            f"- Mean v2 strict quality: {q.get('mean_v2', 'n/a')}/50",
            f"- Mean v1 strict quality: {q.get('mean_v1', 'n/a')}/50",
            f"- Mean delta: +{q.get('mean_delta', 'n/a')} points",
            "- Calibration status: not run; SPEC §11.2 requires calibration before final trust.",
        ])
    iter_dir.joinpath("benchmark.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_review(iter_dir: Path, benchmark: dict) -> None:
    data = {"benchmark": benchmark}
    html = f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <title>sc-brainstorm iteration-2 review</title>
  <style>body{{font-family:system-ui,sans-serif;max-width:1100px;margin:2rem auto;line-height:1.4}}table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #ddd;padding:.4rem;text-align:left}}code,pre{{background:#f6f8fa;padding:.2rem}}</style>
</head>
<body>
  <h1>sc-brainstorm iteration-2 review</h1>
  <p>Static review artifact regenerated after expanding evals to cases 1-12.</p>
  <h2>Runs</h2>
  <table><thead><tr><th>Eval</th><th>Config</th><th>Pass</th><th>Time (s)</th><th>Tokens</th></tr></thead><tbody>
  {''.join(f'<tr><td>{r["eval_id"]}: {r["eval_name"]}</td><td>{r["configuration"]}</td><td>{r["result"]["passed"]}/{r["result"]["total"]}</td><td>{r["result"]["time_seconds"]}</td><td>{r["result"]["tokens"]}</td></tr>' for r in benchmark['runs'])}
  </tbody></table>
  <h2>Embedded JSON</h2>
  <pre id=\"data\"></pre>
  <script>const EMBEDDED_DATA = {json.dumps(data)}; document.getElementById('data').textContent = JSON.stringify(EMBEDDED_DATA, null, 2);</script>
</body>
</html>
"""
    iter_dir.joinpath("review.html").write_text(html, encoding="utf-8")


def main() -> None:
    iter_dir = ROOT / "iterations" / "iteration-2"
    benchmark = build_benchmark(iter_dir)
    iter_dir.joinpath("benchmark.json").write_text(json.dumps(benchmark, indent=2) + "\n", encoding="utf-8")
    write_markdown(iter_dir, benchmark)
    write_review(iter_dir, benchmark)
    print(f"Wrote {iter_dir / 'benchmark.json'}")
    print(f"Wrote {iter_dir / 'benchmark.md'}")
    print(f"Wrote {iter_dir / 'review.html'}")


if __name__ == "__main__":
    main()
