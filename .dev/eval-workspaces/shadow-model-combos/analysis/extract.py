"""Extract one record per experiment run (15) from the run folders and stream logs; write results.jsonl and results.md.

Read-only on the runs. Run: uv run python .dev/eval-workspaces/shadow-model-combos/analysis/extract.py
Sources: <run>/return-contract.yaml, <run>/adversarial/merged-verdict.yaml, <run>/panel/*, logs/<run>.{jsonl,time},
scripts/reflect_shadow_exit.py output (parity, EV-1, lint per run).
"""

from __future__ import annotations

import collections
import json
import re
import statistics
import subprocess
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
EVAL = HERE.parent
ROOT = EVAL.parents[2]
ID = "TASK-WF-designSpec-20261107-075614"
COMBOS = "ABCDE"
REPEATS = (1, 2, 3)


def load_yaml(path: Path) -> dict:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception:
        return {}


def tele(contract: dict, key: str):
    t = contract.get("telemetry")
    if isinstance(t, dict) and key in t:
        return t[key]
    return contract.get(key)


def stream(run: str) -> dict:
    """Served models per sub-agent call and usage, from the stream-json log."""
    path = EVAL / "logs" / f"{run}.jsonl"
    calls: dict[str, dict] = {}
    served: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    best = None
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        t = ev.get("type")
        if t == "assistant":
            msg = ev.get("message") or {}
            parent = ev.get("parent_tool_use_id")
            if parent and msg.get("model"):
                served[parent][msg["model"]] += 1
            for c in msg.get("content") or []:
                if isinstance(c, dict) and c.get("type") == "tool_use" and c.get("name") in ("Task", "Agent"):
                    inp = c.get("input") or {}
                    calls[c["id"]] = {"agent": inp.get("subagent_type"), "requested": inp.get("model")}
        elif t == "result":
            if best is None or (ev.get("total_cost_usd") or 0) >= (best.get("total_cost_usd") or 0):
                best = ev
    agents = []
    for cid, info in calls.items():
        s = served.get(cid)
        agents.append({**info, "served": s.most_common(1)[0][0] if s else None})
    usage = {}
    if best:
        for model, u in (best.get("modelUsage") or {}).items():
            usage[model] = {"in": u.get("inputTokens"), "out": u.get("outputTokens"), "usd": round(u.get("costUSD") or 0, 2)}
    return {
        "reviewers": [(a["requested"], a["served"]) for a in agents if a["agent"] == "reflect-reviewer"],
        "calibrators": [(a["requested"], a["served"]) for a in agents if a["agent"] == "confidence-calibrator"],
        "cost_usd": round((best or {}).get("total_cost_usd") or 0, 2),
        "usage": usage,
        "out_tokens": sum(v["out"] or 0 for v in usage.values()),
        "turns": (best or {}).get("num_turns"),
    }


def exit_report() -> dict[str, dict]:
    out = subprocess.run(
        [sys.executable, str(ROOT / "scripts/reflect_shadow_exit.py"), "--runs-root", str(EVAL / "runs"), "--required", "15"],
        capture_output=True, text=True, cwd=ROOT,
    ).stdout
    res: dict[str, dict] = collections.defaultdict(lambda: {"parity": None, "lint": []})
    section = None
    for line in out.splitlines():
        if line.startswith("parity assertion"):
            section = "parity"
        elif line.startswith("contract lint"):
            section = "lint"
        elif line.startswith("verdict replay"):
            section = None
        m = re.match(r"^  (pre-\S+?): (.*)$", line)
        if m and section == "parity":
            res[m.group(1)]["parity"] = m.group(2).startswith("holds")
            res[m.group(1)]["parity_note"] = m.group(2)
            cur = m.group(1)
        elif m and section == "lint":
            cur = m.group(1)
            res[cur]["lint_clean"] = m.group(2).strip() == "clean"
        elif section == "lint" and line.startswith("    ") and "cur" in dir():
            res[cur]["lint"].append(line.strip())
    return res


def record(x: str, r: int, exits: dict) -> dict:
    run = f"pre-{ID}-combo{x}-r{r}"
    d = EVAL / "runs" / run
    contract = load_yaml(d / "return-contract.yaml")
    verdict = load_yaml(d / "adversarial" / "merged-verdict.yaml") or load_yaml(d / "adversarial" / "adversarial" / "merged-verdict.yaml")
    manifest = {}
    try:
        manifest = json.loads((d / "panel" / "manifest.json").read_text())
    except Exception:
        pass
    clusters = {}
    try:
        clusters = json.loads((d / "panel" / "clusters.json").read_text())
    except Exception:
        pass
    t = (EVAL / "logs" / f"{run}.time").read_text().split()
    start = int(t[0])
    end = int(re.search(r"end=(\d+)", " ".join(t)).group(1))
    selfrep = []
    for f in sorted((d / "reviewer-cards").glob("*.md")) + sorted((d / "panel" / "cards").glob("*.md")):
        for line in f.read_text(errors="replace").splitlines():
            if "reviewer_model_self_report" in line:
                selfrep.append(line.strip()[:120])
                break
    leak = False
    for p in [d / "REPORT.md", *d.glob("reviewer-cards/*.md"), *d.glob("adversarial/*.md"), *d.glob("adversarial/adversarial/*.md")]:
        try:
            if f".dev/tasks/done/{ID}" in p.read_text(errors="replace"):
                leak = True
        except OSError:
            pass
    s = stream(run)
    revs = s["reviewers"]
    served = [sv for _, sv in revs]
    findings_total = sum(len(c.get("members", [])) for c in clusters.get("clusters", [])) if clusters else None
    ex = exits.get(run, {})
    return {
        "run": run, "combo": x, "repeat": r,
        "state": manifest.get("state"), "status": contract.get("status"), "merge_method": contract.get("merge_method"),
        "confidence": contract.get("confidence_calibrated"), "minutes": round((end - start) / 60, 1),
        "verdict": verdict.get("verdict"), "blocking": verdict.get("blocking_findings"),
        "medium": verdict.get("medium_findings"), "minor": verdict.get("minor_findings"),
        "convergence": verdict.get("convergence_score"), "findings_clustered": findings_total,
        "compliance_first_pass": tele(contract, "findings_block_compliance_rate"),
        "reviewers_complete": manifest.get("reviewers_complete"),
        "calibrator_diversity": contract.get("calibrator_diversity"),
        "identity_mismatch_suspected": tele(contract, "identity_mismatch_suspected"),
        "judge_identity": tele(contract, "judge_identity"),
        "parity": ex.get("parity"), "parity_note": ex.get("parity_note"), "lint_clean": ex.get("lint_clean"),
        "reviewer_requested_served": revs, "reviewer_distinct_served": len({s for s in served if s}),
        "calibrator_requested_served": s["calibrators"],
        "cost_usd": s["cost_usd"], "out_tokens": s["out_tokens"], "usage": s["usage"],
        "self_reports": selfrep, "leak": leak,
    }


def med(vals):
    v = [x for x in vals if isinstance(x, (int, float))]
    return (round(statistics.median(v), 2), round(min(v), 2), round(max(v), 2)) if v else None


def main() -> None:
    exits = exit_report()
    rows = [record(x, r, exits) for x in COMBOS for r in REPEATS]
    (EVAL / "results.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    lines = ["# Results (descriptive; generated by analysis/extract.py)", "",
             "| run | state | min | conf | blocking/medium/minor | clustered | compliance 1st pass | parity | lint clean | distinct served reviewers | cost USD | out tokens |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['combo']}{r['repeat']} | {r['state']} | {r['minutes']} | {r['confidence']} | {r['blocking']}/{r['medium']}/{r['minor']} | {r['findings_clustered']} | {r['compliance_first_pass']} | {r['parity']} | {r['lint_clean']} | {r['reviewer_distinct_served']} | {r['cost_usd']} | {r['out_tokens']} |")
    lines += ["", "## Per combination: median (min-max)", "", "| combo | minutes | confidence | blocking | medium | clustered findings | cost USD | out tokens | distinct served reviewers |", "|---|---|---|---|---|---|---|---|---|"]
    for x in COMBOS:
        g = [r for r in rows if r["combo"] == x]
        lines.append(f"| {x} | {med([r['minutes'] for r in g])} | {med([r['confidence'] for r in g])} | {med([r['blocking'] for r in g])} | {med([r['medium'] for r in g])} | {med([r['findings_clustered'] for r in g])} | {med([r['cost_usd'] for r in g])} | {med([r['out_tokens'] for r in g])} | {med([r['reviewer_distinct_served'] for r in g])} |")
    lines += ["", "## Requested class -> served model, per reviewer call", ""]
    for r in rows:
        lines.append(f"- {r['combo']}{r['repeat']}: reviewers {r['reviewer_requested_served']}; calibrators {r['calibrator_requested_served']}")
    (EVAL / "results.md").write_text("\n".join(lines) + "\n")
    print(f"wrote {len(rows)} records")


if __name__ == "__main__":
    main()
