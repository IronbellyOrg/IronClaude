"""Compare qual-pass1.md and qual-pass2.md verdicts; list disagreements.

Usage: uv run python qualdiff.py
"""
import re
from pathlib import Path

WORK = Path(__file__).resolve().parent
CRIT = [f"{d}{i}" for d in ("CO", "CR", "ST", "CL", "RK", "IE") for i in range(1, 6)]
ROW = re.compile(r"^\|\s*(CO|CR|ST|CL|RK|IE)(\d)\s*\|.*\|\s*\**(MET|NOT MET)\**\s*\|\s*$")


def parse(name):
    out, cur = {}, None
    for ln in (WORK / name).read_text().splitlines():
        h = re.match(r"^##\s+Variant\s+(V?\d)", ln)
        if h:
            cur = "V" + h.group(1).lstrip("V")
            continue
        m = ROW.match(ln.strip())
        if m and cur:
            out[(cur, m.group(1) + m.group(2))] = m.group(3)
    return out


p1, p2 = parse("qual-pass1.md"), parse("qual-pass2.md")
for v in ("V1", "V2", "V3"):
    for p, n in ((p1, 1), (p2, 2)):
        miss = [c for c in CRIT if (v, c) not in p]
        assert not miss, f"pass{n} {v} missing {miss}"
dis = [(v, c, p1[(v, c)], p2[(v, c)]) for v in ("V1", "V2", "V3") for c in CRIT
       if p1[(v, c)] != p2[(v, c)]]
for v in ("V1", "V2", "V3"):
    print(v, "pass1", sum(p1[(v, c)] == "MET" for c in CRIT),
          "pass2", sum(p2[(v, c)] == "MET" for c in CRIT))
print("disagreements:", len(dis))
for d in dis:
    print(" ", *d)
