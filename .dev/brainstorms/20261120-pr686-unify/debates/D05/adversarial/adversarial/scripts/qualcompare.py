"""Compare the two position-bias passes criterion by criterion, then apply the recorded
re-evaluations and print per-dimension subtotals (read-only on inputs).

Usage: uv run python -I qualcompare.py qual-pass-1.md qual-pass-2.md
"""
import re
import sys

DIMS = ["Completeness", "Correctness", "Structure", "Clarity", "Risk Coverage", "Invariant"]
# Final verdicts for the criterion-variant pairs on which the passes disagreed. Each was
# re-evaluated with both evidence cells side by side (see base-selection.md, resolution log).
RESOLVED = {
    ("Completeness", 4, "V2"): "MET",
    ("Correctness", 1, "V2"): "NOT MET",
    ("Structure", 3, "V2"): "MET",
    ("Clarity", 1, "V2"): "NOT MET",
    ("Risk Coverage", 3, "V1"): "NOT MET",
}


def parse(path):
    out = {}
    dim = -1
    for line in open(path, encoding="utf-8"):
        m = re.match(r"## (\d)\.", line)
        if m:
            dim = int(m.group(1)) - 1
            continue
        if dim < 0 or not line.startswith("|"):
            continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
        if len(cells) == 6 and cells[0].isdigit() and cells[2] in ("MET", "NOT MET"):
            out[(dim, int(cells[0]))] = {"V1": cells[2], "V2": cells[4], "name": cells[1]}
    return out


p1, p2 = parse(sys.argv[1]), parse(sys.argv[2])
assert len(p1) == 30 and len(p2) == 30, (len(p1), len(p2))
dis = []
final = {}
for k in sorted(p1):
    for v in ("V1", "V2"):
        key = (DIMS[k[0]], k[1], v)
        if p1[k][v] != p2[k][v]:
            dis.append((key, p1[k][v], p2[k][v], RESOLVED[key]))
            final[(k, v)] = RESOLVED[key]
        else:
            final[(k, v)] = p1[k][v]
assert {d[0] for d in dis} == set(RESOLVED), {d[0] for d in dis} ^ set(RESOLVED)
print("disagreements:", len(dis), "of 60 criterion-variant pairs")
for key, a, b, r in dis:
    print(f"  {key[0]} #{key[1]} {key[2]}: pass1={a} pass2={b} final={r}")
for name, src in (("pass1", lambda k, v: p1[k][v]), ("pass2", lambda k, v: p2[k][v]),
                  ("final", lambda k, v: final[(k, v)])):
    for v in ("V1", "V2"):
        subs = [sum(src(k, v) == "MET" for k in p1 if k[0] == d) for d in range(6)]
        print(name, v, subs, "total", sum(subs))
