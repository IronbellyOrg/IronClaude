#!/usr/bin/env python3
"""Aggregate metrics across all direct-mode eval runs. (RESTORED 2026-05-22)

Outputs:
  summary.csv (machine-readable)
  summary.md  (per-run table + aggregate stats per group)

Usage: ./aggregate.py [eval-dir]
"""
from __future__ import annotations
import csv
import re
import sys
from pathlib import Path
from statistics import mean, stdev
from typing import Any

EVAL_DIR = Path(sys.argv[1] if len(sys.argv) > 1 else ".")

YAML_VAL = re.compile(r'^\s*([\w_]+)\s*:\s*"?([^"#\n]+?)"?\s*(?:#.*)?$', re.MULTILINE)

def parse_simple_yaml(text: str) -> dict[str, str]:
    return {m.group(1): m.group(2).strip() for m in YAML_VAL.finditer(text)}

def parse_contract(p: Path) -> dict[str, Any]:
    return parse_simple_yaml(p.read_text()) if p.exists() else {}

def detect_winner(base_variant: str) -> str:
    bv = base_variant.lower()
    if "opus" in bv:
        return "opus"
    if "sonnet" in bv:
        return "sonnet"
    return "unknown"

def size_kb(p: Path) -> int:
    return p.stat().st_size // 1024 if p.exists() else 0

def collect_run(group: str, n: int) -> dict[str, Any]:
    run_dir = EVAL_DIR / f"group{group}-direct" / f"run{n}"
    adv = run_dir / "adversarial"
    if not adv.exists():
        return {"group": group, "run": n, "status": "MISSING_DIR"}

    contract_path = adv / "return-contract.yaml"
    if not contract_path.exists():
        contract_path = run_dir / "return-contract.yaml"
    contract = parse_contract(contract_path)

    variants = sorted(adv.glob("variant-*.md"))
    if not variants:
        variants = sorted(adv.glob("*-variant.md"))
    opus_v = next((v for v in variants if "opus" in v.name), None)
    sonnet_v = next((v for v in variants if "sonnet" in v.name), None)

    def persona(p: Path | None) -> str:
        if not p:
            return ""
        m = re.search(r"variant-\d+-(?:opus|sonnet)-(\w+)\.md", p.name)
        return m.group(1) if m else ""

    return {
        "group": group,
        "run": n,
        "status": contract.get("status", "UNKNOWN"),
        "convergence_score": contract.get("convergence_score", ""),
        "base_variant": contract.get("base_variant", ""),
        "winner": detect_winner(contract.get("base_variant", "")),
        "unresolved_conflicts": contract.get("unresolved_conflicts", ""),
        "fallback_mode": contract.get("fallback_mode", ""),
        "failure_stage": contract.get("failure_stage", ""),
        "opus_persona": persona(opus_v),
        "sonnet_persona": persona(sonnet_v),
        "opus_variant_kb": size_kb(opus_v) if opus_v else 0,
        "sonnet_variant_kb": size_kb(sonnet_v) if sonnet_v else 0,
        "has_debate_transcript": (adv / "debate-transcript.md").exists(),
        "has_per_round_files": any(adv.glob("round*-variant*-*.md")),
        "has_base_selection": (adv / "base-selection.md").exists(),
        "has_refactor_plan": (adv / "refactor-plan.md").exists(),
        "has_invariant_probe": (adv / "invariant-probe.md").exists(),
        "has_merge_log": (adv / "merge-log.md").exists(),
        "merged_output_kb": max(size_kb(adv / "merged-output.md"), size_kb(run_dir / "merged-output.md")),
    }

def aggregate(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    out = {}
    for group in ("A", "B"):
        group_rows = [r for r in rows if r["group"] == group and r["status"] not in ("MISSING_DIR", "UNKNOWN", "failed")]
        if not group_rows:
            out[group] = {"n": 0, "note": "no usable runs"}
            continue
        cs = [float(r["convergence_score"]) for r in group_rows if r["convergence_score"]]
        winners = [r["winner"] for r in group_rows]
        opus_wins = winners.count("opus")
        sonnet_wins = winners.count("sonnet")
        out[group] = {
            "n": len(group_rows),
            "convergence_mean": round(mean(cs), 3) if cs else None,
            "convergence_stdev": round(stdev(cs), 3) if len(cs) > 1 else None,
            "convergence_min": min(cs) if cs else None,
            "convergence_max": max(cs) if cs else None,
            "opus_wins": opus_wins,
            "sonnet_wins": sonnet_wins,
            "unknown_winners": len(winners) - opus_wins - sonnet_wins,
            "debate_transcript_rate": round(sum(1 for r in group_rows if r["has_debate_transcript"]) / len(group_rows), 3),
            "per_round_files_rate": round(sum(1 for r in group_rows if r["has_per_round_files"]) / len(group_rows), 3),
            "personas_seen_opus": sorted({r["opus_persona"] for r in group_rows if r["opus_persona"]}),
            "personas_seen_sonnet": sorted({r["sonnet_persona"] for r in group_rows if r["sonnet_persona"]}),
            "opus_variant_kb_mean": round(mean([r["opus_variant_kb"] for r in group_rows]), 1),
            "sonnet_variant_kb_mean": round(mean([r["sonnet_variant_kb"] for r in group_rows]), 1),
        }
    return out

def main() -> None:
    rows = [collect_run(g, n) for g in ("A", "B") for n in range(1, 6)]
    fields = list(rows[0].keys())

    csv_path = EVAL_DIR / "summary.csv"
    with csv_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    agg = aggregate(rows)

    md = ["# Eval summary — sc:adversarial direct-mode 5+5 runs\n"]
    md.append("## Per-run metrics\n")
    md.append("| Group | Run | Status | Convergence | Winner | Base variant | Unresolved | Opus persona | Sonnet persona | Opus KB | Sonnet KB | Debate? | Per-round? | Merged KB |")
    md.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        md.append(
            f"| {r['group']} | {r['run']} | {r.get('status','?')} | {r.get('convergence_score','')} | "
            f"{r.get('winner','')} | {r.get('base_variant','')} | {r.get('unresolved_conflicts','')} | "
            f"{r.get('opus_persona','')} | {r.get('sonnet_persona','')} | "
            f"{r.get('opus_variant_kb',0)} | {r.get('sonnet_variant_kb',0)} | "
            f"{'✓' if r.get('has_debate_transcript') else '✗'} | "
            f"{'✓' if r.get('has_per_round_files') else '✗'} | "
            f"{r.get('merged_output_kb',0)} |"
        )

    md.append("\n## Aggregate stats per group (usable runs only — excludes failed/missing)\n")
    for group, stats in agg.items():
        md.append(f"### Group {group}")
        for k, v in stats.items():
            md.append(f"- **{k}**: {v}")
        md.append("")

    summary_md = EVAL_DIR / "summary.md"
    summary_md.write_text("\n".join(md))

    print(f"Wrote {csv_path}")
    print(f"Wrote {summary_md}")

if __name__ == "__main__":
    main()
