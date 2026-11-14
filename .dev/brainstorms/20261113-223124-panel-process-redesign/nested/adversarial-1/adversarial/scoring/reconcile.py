"""Compare the two qualitative passes criterion by criterion; print agreements, disagreements and subtotals.

Run: uv run python reconcile.py qual-pass1.md qual-pass2.md [resolved.json]
resolved.json (optional): {"CO1|V2": "MET", ...} final verdicts for criteria where the passes disagreed.
"""
import json
import re
import sys
from pathlib import Path


def parse(path):
    rows = {}
    for ln in Path(path).read_text().splitlines():
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        m = re.match(r"(?:CO|CR|ST|CL|RK|IV)\d\b", cells[0].strip("* "))
        if len(cells) >= 7 and m:
            cid = m.group(0)
            for i, v in enumerate(("V1", "V2", "V3")):
                verdict = cells[1 + 2 * i].replace("*", "").upper()
                ev = cells[2 + 2 * i]
                rows[(cid, v)] = ("MET" if verdict.startswith("MET") else "NOT MET", ev)
    return rows


p1, p2 = parse(sys.argv[1]), parse(sys.argv[2])
resolved = json.loads(Path(sys.argv[3]).read_text()) if len(sys.argv) > 3 else {}
dims = {"CO": "Completeness", "CR": "Correctness", "ST": "Structure", "CL": "Clarity", "RK": "Risk Coverage", "IV": "Invariant & Edge Case"}
print(f"criteria parsed: pass1={len(p1)//3} pass2={len(p2)//3} (expected 30 each)")
dis = [(k, p1[k], p2[k]) for k in sorted(p1) if k in p2 and p1[k][0] != p2[k][0]]
print(f"disagreements: {len(dis)} of {len(p1)}")
for (cid, v), a, b in dis:
    print(f"  {cid} {v}: pass1={a[0]} [{a[1][:90]}] | pass2={b[0]} [{b[1][:90]}] | final={resolved.get(f'{cid}|{v}', 'UNRESOLVED')}")
tot = {v: 0 for v in ("V1", "V2", "V3")}
sub = {d: {v: 0 for v in tot} for d in dims}
for (cid, v), a in p1.items():
    b = p2.get((cid, v), a)
    final = a[0] if a[0] == b[0] else resolved.get(f"{cid}|{v}", "NOT MET")
    if final == "MET":
        tot[v] += 1
        sub[cid[:2]][v] += 1
for d, name in dims.items():
    print(f"{name:24s}", " ".join(f"{v}={sub[d][v]}/5" for v in tot))
print("TOTAL", " ".join(f"{v}={tot[v]}/30={tot[v]/30:.4f}" for v in tot))
print("pass1 raw", {v: sum(1 for (c, vv), x in p1.items() if vv == v and x[0] == 'MET') for v in tot})
print("pass2 raw", {v: sum(1 for (c, vv), x in p2.items() if vv == v and x[0] == 'MET') for v in tot})
