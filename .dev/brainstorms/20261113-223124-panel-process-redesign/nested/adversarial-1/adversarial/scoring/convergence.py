"""Per-point convergence from the advocates' position tables.

Strict agreement = at least 2 of 3 advocates chose the identical normalised set (V1, V2, V3, COMBINE sets, NONE).
Compatible agreement = at least 2 advocates whose sets are nested (one contains the other).
Round 2 updates replace Round 1 choices for the 11 contested points (their tables restate them).
Run: uv run python convergence.py <adversarial-dir>
"""
import re
import sys
from itertools import combinations
from pathlib import Path

D = Path(sys.argv[1]) / "debate"


def norm(s):
    s = s.strip().upper()
    if s.startswith("NONE"):
        return frozenset({"NONE"})
    return frozenset(re.findall(r"V(\d)", s)) or frozenset({"NONE"})


def table(path, key_cols=(0, 1), start_marker=None):
    rows, on = {}, start_marker is None
    for ln in Path(path).read_text().splitlines():
        if start_marker and start_marker in ln:
            on = True
        if not on or not ln.startswith("|"):
            continue
        c = [x.strip() for x in ln.strip("|").split("|")]
        if re.fullmatch(r"[SCXA]-\d{3}", c[0]):
            rows[c[0]] = norm(c[1])
    return rows


r1 = {n: table(D / f"round1-V{n}.md", start_marker="Position table") for n in (1, 2, 3)}
r2 = {n: table(D / f"round2-V{n}.md", start_marker="Contested points") for n in (1, 2, 3)}
pts = sorted(r1[1])
assert all(sorted(r1[n]) == pts for n in (2, 3)), "tables differ"


def score(pos):
    strict = comp = 0
    detail = {}
    for p in pts:
        ch = [pos[n][p] for n in (1, 2, 3)]
        s = any(ch[i] == ch[j] for i, j in combinations(range(3), 2))
        c = s or any(ch[i] <= ch[j] or ch[j] <= ch[i] for i, j in combinations(range(3), 2))
        strict += s
        comp += c
        detail[p] = (s, c)
    return strict, comp, detail


pos1 = {n: dict(r1[n]) for n in r1}
pos2 = {n: {**r1[n], **r2[n]} for n in r1}
for name, pos in (("Round 1", pos1), ("Round 2", pos2)):
    s, c, d = score(pos)
    print(f"{name}: strict {s}/{len(pts)} = {s/len(pts):.4f}; compatible {c}/{len(pts)} = {c/len(pts):.4f}")
    print("  not strict:", [p for p, (a, b) in d.items() if not a])
    print("  not even compatible:", [p for p, (a, b) in d.items() if not b])
print("points:", len(pts), "updated in round 2:", sorted(set(r2[1]) | set(r2[2]) | set(r2[3])))
