"""Quantitative layer of the hybrid score (RC, IC, SR, DC, SC) for the three variants.

Deterministic: same input gives the same numbers. Stdlib only.
Usage: uv run --no-project python -I quant.py <dir with variant-N-*.md> [--contradictions V1=0,V2=1,V3=0]
"""
import json
import re
import sys
from pathlib import Path

REQUIRED = (
    # the ten known contradictions of the seed brief
    [f"K{i}" for i in range(1, 11)]
    # the eight required sections of the output contract
    + ["Target architecture", "Interface table", "Staged migration", "Built today", "Open owner actions", "Risks", "Contradictions", "Summary"]
    # verdict ids that must be used
    + [f"D{i:02d}" for i in range(1, 16)] + ["Q01", "Q02", "Q03"]
    # interface names the seed brief requires in the interface table
    + ["wake", "ack", "per-repo", "dispatch.json", ".dev/coordinators", "sc-launch:v1", "go entry", "grants",
       "status --json", "session_id", "plan_body.py", "run-all", "flock", "held_incomplete", "held_backlog",
       "max_in_flight", "rollback", "Rollback", "preconditions", "Preconditions", "UNVERIFIED"]
)
VAGUE = ["appropriate", "as needed", "properly", "adequate", "should consider", "might", "various", "etc.", "best practices", "industry standard"]
CONCRETE = re.compile(r"(`[^`]+`|\b\d+(?:[.,]\d+)?\b|\b[A-Za-z_./-]+\.(?:py|md|sh|json|yaml)(?::\d+(?:-\d+)?)?\b|\b[A-Z]{1,4}-?\d+\b)")
REFS = re.compile(r"\b(S\d+|K\d+|MC-\d+|OA-\d+|RK-\d+|R\d+|C-INV-\d)\b")


def score(path: Path, contradictions: int) -> dict:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    low = text
    matched = [r for r in REQUIRED if r in low]
    rc = len(matched) / len(REQUIRED)
    claims = sum(1 for ln in lines if CONCRETE.search(ln) and len(ln.strip()) > 20)
    ic = 1 - contradictions / max(claims, 1)
    concrete = sum(len(CONCRETE.findall(ln)) for ln in lines if not ln.startswith("#"))
    vague = sum(low.lower().count(v) for v in VAGUE)
    sr = concrete / (concrete + vague) if concrete + vague else 0.0
    ids = set(REFS.findall(text))
    resolved = 0
    for i in ids:
        pat = re.compile(r"^\s*(?:\||[-*]|\d+\.)?\s*(?:\*\*)?" + re.escape(i) + r"\b", re.M)
        if pat.search(text):
            resolved += 1
    dc = resolved / len(ids) if ids else 1.0
    h2 = sum(1 for ln in lines if ln.startswith("## "))
    return {"file": path.name, "RC": rc, "IC": ic, "SR": sr, "DC": dc, "H2": h2,
            "missing_required": [r for r in REQUIRED if r not in low], "claims": claims,
            "contradictions": contradictions, "concrete": concrete, "vague": vague,
            "ids": len(ids), "ids_resolved": resolved}


def main() -> None:
    folder = Path(sys.argv[1])
    contra = {"V1": 0, "V2": 1, "V3": 0}
    if len(sys.argv) > 3 and sys.argv[2] == "--contradictions":
        contra = {kv.split("=")[0]: int(kv.split("=")[1]) for kv in sys.argv[3].split(",")}
    files = sorted(folder.glob("variant-[0-9]-*.md"))
    rows = []
    for f in files:
        key = "V" + f.name.split("-")[1]
        rows.append(score(f, contra.get(key, 0)))
    max_h2 = max(r["H2"] for r in rows)
    for r in rows:
        r["SC"] = r["H2"] / max_h2
        r["quant_score"] = 0.30 * r["RC"] + 0.25 * r["IC"] + 0.15 * r["SR"] + 0.15 * r["DC"] + 0.15 * r["SC"]
    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()
