"""Tally the per-point tables of the advocate files for one debate round.

Usage: uv run python tally.py <debate-dir> <round-number>

Reads round<N>-A.md, round<N>-B.md, round<N>-C.md from <debate-dir>, takes the table
after the heading "### Per-point positions", and writes tally-round<N>.md and
tally-round<N>.json next to them. Prints a short summary.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

debate = Path(sys.argv[1])
rnd = sys.argv[2]
adv_dir = debate.parent
IDS = (
    [f"S-{i:03d}" for i in range(1, 7)]
    + [f"C-{i:03d}" for i in range(1, 27)]
    + [f"X-{i:03d}" for i in range(1, 15)]
    + [f"A-{i:03d}" for i in range(1, 5)]
)
A_LEVELS = {"A-001": "L3", "A-002": "L3", "A-003": "L2", "A-004": "L2"}
VALID = {"A", "B", "C", "NONE", "ACCEPT", "REJECT", "QUALIFY"}


def levels():
    lv = dict(A_LEVELS)
    for line in (adv_dir / "diff-analysis.md").read_text().splitlines():
        m = re.match(r"\|\s*([SCX]-\d{3})\s*\|", line)
        if m:
            cells = [c.strip() for c in line.split("|")]
            lv[m.group(1)] = cells[-2]
    return lv


def parse(path):
    text = path.read_text()
    if "### Per-point positions" not in text:
        return {}, ["missing heading '### Per-point positions'"]
    body = text.split("### Per-point positions", 1)[1]
    rows, problems = {}, []
    for line in body.splitlines():
        m = re.match(r"\|\s*([SCXA]-\d{3})\s*\|\s*([^|]*)\|", line)
        if not m:
            continue
        tok = re.sub(r"[^A-Za-z]", "", m.group(2).split()[0] if m.group(2).split() else "").upper()
        if tok not in VALID:
            problems.append(f"{m.group(1)}: bad winner token {m.group(2).strip()!r}")
            continue
        rows[m.group(1)] = tok
    for i in IDS:
        if i not in rows:
            problems.append(f"{i}: missing row")
    return rows, problems


def omissions(path):
    text = path.read_text()
    sec = text.split("### Shared-assumption responses", 1)
    if len(sec) < 2:
        return list(A_LEVELS)
    block = sec[1].split("###", 1)[0]
    return [a for a in A_LEVELS if not re.search(a + r".{0,80}(ACCEPT|REJECT|QUALIFY)", block, re.S)]


lv = levels()
data, problems, omit = {}, {}, {}
for x in "ABC":
    p = debate / f"round{rnd}-{x}.md"
    data[x], problems[x] = parse(p)
    omit[x] = omissions(p)

points = {}
agreed = 0
for i in IDS:
    toks = [data[x].get(i) for x in "ABC"]
    cnt = Counter(t for t in toks if t)
    top, n = (cnt.most_common(1)[0] if cnt else (None, 0))
    ok = n >= 2
    agreed += ok
    points[i] = {"level": lv.get(i, "L2"), "votes": toks, "agreed": ok, "winner": top if ok else None}

conv = agreed / len(IDS)
cov = Counter(p["level"] for p in points.values())
unresolved = [i for i, p in points.items() if not p["agreed"]]
own = {x: sum(1 for i in IDS if data[x].get(i) == x) for x in "ABC"}

out = [f"# Tally, round {rnd}", "", f"- Points: {len(IDS)}; agreed (at least 2 of 3 advocates name the same winner): {agreed}; convergence: {conv:.4f}"]
out += [f"- Taxonomy coverage (all points): {dict(cov)}"]
out += [f"- Unresolved ({len(unresolved)}): {', '.join(unresolved) or 'none'}"]
out += [f"- Own-variant picks: {own}"]
out += [f"- Parse problems: { {x: problems[x] for x in 'ABC' if problems[x]} or 'none'}"]
out += [f"- Shared-assumption omissions: { {x: omit[x] for x in 'ABC' if omit[x]} or 'none'}", ""]
out += ["| Point | Lvl | A | B | C | Agreed | Winner |", "|---|---|---|---|---|---|---|"]
for i in IDS:
    p = points[i]
    out.append(f"| {i} | {p['level']} | {p['votes'][0]} | {p['votes'][1]} | {p['votes'][2]} | {'yes' if p['agreed'] else 'NO'} | {p['winner'] or '-'} |")
(debate / f"tally-round{rnd}.md").write_text("\n".join(out) + "\n")
(debate / f"tally-round{rnd}.json").write_text(json.dumps({"convergence": conv, "points": points, "omissions": omit, "problems": problems}, indent=1))
print("\n".join(out[:8]))
