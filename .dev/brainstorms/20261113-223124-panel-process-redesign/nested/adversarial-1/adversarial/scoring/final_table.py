"""Emit the final qualitative CEV table (30 criteria x 3 variants) as markdown from the two passes plus resolved.json.

Run: uv run python final_table.py qual-pass1.md qual-pass2.md resolved.json
"""
import json
import re
import sys
from pathlib import Path

DIMS = [("CO", "Completeness"), ("CR", "Correctness"), ("ST", "Structure"), ("CL", "Clarity"), ("RK", "Risk Coverage"), ("IV", "Invariant & Edge Case Coverage")]


def parse(path):
    rows, names = {}, {}
    for ln in Path(path).read_text().splitlines():
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        m = re.match(r"((?:CO|CR|ST|CL|RK|IV)\d)\b\s*(.*)", cells[0].strip("* ")) if cells else None
        if len(cells) >= 7 and m:
            names[m.group(1)] = m.group(2)
            for i, v in enumerate(("V1", "V2", "V3")):
                verdict = "MET" if cells[1 + 2 * i].replace("*", "").upper().startswith("MET") else "NOT MET"
                rows[(m.group(1), v)] = (verdict, cells[2 + 2 * i].replace("|", "/"))
    return rows, names


p1, names = parse(sys.argv[1])
p2, _ = parse(sys.argv[2])
res = json.loads(Path(sys.argv[3]).read_text())
for code, dim in DIMS:
    print(f"\n### {dim} (5 criteria)\n")
    print("| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |")
    print("|---|---|---|---|---|---|---|")
    sub = {"V1": 0, "V2": 0, "V3": 0}
    for n in range(1, 6):
        cid = f"{code}{n}"
        cells = [f"{cid} {names.get(cid, '')}"]
        for v in ("V1", "V2", "V3"):
            a, b = p1[(cid, v)], p2[(cid, v)]
            if a[0] == b[0]:
                final, ev = a[0], a[1]
            else:
                final = res[f"{cid}|{v}"]
                ev = f"RE-EVALUATED (pass1 {a[0]}: {a[1]} / pass2 {b[0]}: {b[1]})"
            sub[v] += final == "MET"
            cells += [final, ev]
        print("| " + " | ".join(cells) + " |")
    print(f"| **Subtotal** | **{sub['V1']}/5** | | **{sub['V2']}/5** | | **{sub['V3']}/5** | |")
