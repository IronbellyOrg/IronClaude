"""Tally per-point verdict tables from advocate round files.

Usage: uv run python tally.py <round-number>
Reads .work/round<N>-variant-{1,2,3}.md next to this script, checks that each
lists all 46 points once, checks A-001..A-004 responses, and prints the
agreement table (2/3 majority) plus the convergence score.
"""
import re
import sys
from pathlib import Path

WORK = Path(__file__).resolve().parent
POINTS = ([f"S-{i:03d}" for i in range(1, 13)] + [f"C-{i:03d}" for i in range(1, 21)]
          + [f"X-{i:03d}" for i in range(1, 11)] + [f"A-{i:03d}" for i in range(1, 5)])
ROW = re.compile(r"^\|\s*([SCXA]-\d{3})\s*\|\s*\**(V[123])\**\s*\|", re.M)


def table(text):
    start = text.find("## Per-Point Verdict Table")
    assert start >= 0, "verdict table heading missing"
    rows = ROW.findall(text[start:])
    ids = [r[0] for r in rows]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    missing = [p for p in POINTS if p not in ids]
    return dict(rows), missing, dup


def main(rnd):
    votes, problems = {}, []
    for v in (1, 2, 3):
        f = WORK / f"round{rnd}-variant-{v}.md"
        text = f.read_text()
        t, missing, dup = table(text)
        if missing or dup:
            problems.append(f"V{v}: missing={missing} dup={dup}")
        if "<!-- TODO" in text:
            problems.append(f"V{v}: TODO markers remain")
        for a in ("A-001", "A-002", "A-003", "A-004"):
            if not re.search(rf"{a}[^\n]*\b(ACCEPT|REJECT|QUALIFY)\b", text):
                problems.append(f"[OMISSION] Advocate V{v} did not address {a}")
        votes[f"V{v}"] = t
    agreed, rows = 0, []
    for p in POINTS:
        vs = [votes[a].get(p) for a in ("V1", "V2", "V3")]
        best = max(set(vs), key=vs.count)
        n = vs.count(best)
        ok = n >= 2
        agreed += ok
        rows.append((p, vs, best if ok else None, n))
    for p, vs, w, n in rows:
        print(f"{p} votes={'/'.join(str(x) for x in vs)} winner={w or 'UNRESOLVED'} n={n}")
    print(f"agreed={agreed}/{len(POINTS)} convergence={agreed/len(POINTS):.3f}")
    print("problems:", problems or "none")


assert len(POINTS) == 46
if __name__ == "__main__":
    main(sys.argv[1])
