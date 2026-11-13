"""Compare the two qualitative passes per criterion and variant. Usage: uv run python scoring/reconcile.py"""
import re
from pathlib import Path

D = Path(__file__).resolve().parent
ROW = re.compile(r"^\|\s*\**((?:CP|CR|ST|CL|RK|IV)\d)\**\s*\|\s*\**(MET|NOT MET)\**\s*\|(.*)\|\s*$")


def parse(name):
    out, cur = {}, None
    for line in (D / name).read_text().splitlines():
        m = re.match(r"^## (V[1-5])\b", line)
        if m:
            cur = m.group(1)
            continue
        m = ROW.match(line)
        if m and cur:
            out[(cur, m.group(1))] = (m.group(2), m.group(3).strip())
    return out


p1, p2 = parse("qual-pass1.md"), parse("qual-pass2.md")
print("rows", len(p1), len(p2))
dis = sorted(k for k in p1 if k in p2 and p1[k][0] != p2[k][0])
for v in [f"V{i}" for i in range(1, 6)]:
    a = sum(p1[k][0] == "MET" for k in p1 if k[0] == v)
    b = sum(p2[k][0] == "MET" for k in p2 if k[0] == v)
    iv1 = sum(p1[k][0] == "MET" for k in p1 if k[0] == v and k[1].startswith("IV"))
    iv2 = sum(p2[k][0] == "MET" for k in p2 if k[0] == v and k[1].startswith("IV"))
    print(v, "pass1", a, "pass2", b, "IV", iv1, iv2, "disagree", sum(1 for k in dis if k[0] == v))
print("DISAGREEMENTS", len(dis))
for k in dis:
    print(f"## {k[0]} {k[1]}\n P1 {p1[k][0]}: {p1[k][1][:300]}\n P2 {p2[k][0]}: {p2[k][1][:300]}")
