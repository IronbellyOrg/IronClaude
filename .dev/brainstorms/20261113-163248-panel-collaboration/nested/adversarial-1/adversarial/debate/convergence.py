"""Convergence tally for the debate rounds: parses each advocate's '## Per-point positions' table.

Usage: uv run python convergence.py <round-tag> [<round-tag> ...]   (round-tag e.g. round1, round2)
A point is agreed when >= 2/3 of advocates (4 of 5) name the same winner.
"""
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
POINTS = ([f"S-{i:03d}" for i in range(1, 7)] + [f"C-{i:03d}" for i in range(1, 14)]
          + [f"X-{i:03d}" for i in range(1, 14)] + [f"A-{i:03d}" for i in range(1, 12)])
# L1 surface, L2 structural, L3 state mechanics (orchestrator auto-tag; L3 > L2 > L1)
L1 = {"S-003", "S-005", "S-006"}
L3 = {"C-006", "C-007", "C-013", "X-006", "X-009", "A-002", "A-005", "A-006", "A-008"}
ROW = re.compile(r"^\|\s*([SCXA]-\d{3})\s*\|\s*\**(V[1-5])\**\s*\|")


def positions(path):
    out = {}
    text = path.read_text()
    sec = text.split("## Per-point positions", 1)
    for line in (sec[1] if len(sec) == 2 else "").splitlines():
        m = ROW.match(line)
        if m:
            out[m.group(1)] = m.group(2)
    return out


def tally(tag):
    files = sorted(HERE.glob(f"{tag}-V[1-5].md"))
    pos = {f.stem.split("-")[-1]: positions(f) for f in files}
    n = len(pos)
    need = -(-2 * n // 3)  # ceil(2n/3)
    agreed, rows = 0, []
    for p in POINTS:
        votes = [pos[a].get(p) for a in sorted(pos)]
        c = Counter(v for v in votes if v)
        win, k = (c.most_common(1)[0] if c else (None, 0))
        ok = k >= need
        agreed += ok
        lvl = "L1" if p in L1 else "L3" if p in L3 else "L2"
        rows.append(f"| {p} | {lvl} | {' '.join(v or '-' for v in votes)} | {win} | {k}/{n} | {'agreed' if ok else 'split'} |")
    missing = {a: [p for p in POINTS if p not in pos[a]] for a in pos}
    print(f"# {tag}: advocates={n} need={need} agreed={agreed}/{len(POINTS)} convergence={agreed/len(POINTS):.3f}")
    for a, m in missing.items():
        if m:
            print(f"MISSING {a}: {','.join(m)}")
    print(f"| Point | Level | Votes ({' '.join(sorted(pos))}) | Leader | Count | Status |")
    print("|---|---|---|---|---|---|")
    print("\n".join(rows))
    for lvl in ("L1", "L2", "L3"):
        cov = sum(1 for p in POINTS if (("L1" if p in L1 else "L3" if p in L3 else "L2") == lvl))
        print(f"coverage {lvl}: {cov} points debated")


if __name__ == "__main__":
    for t in sys.argv[1:]:
        tally(t)
