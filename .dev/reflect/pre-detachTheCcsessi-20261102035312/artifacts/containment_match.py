"""Deterministic containment matcher (refs/coverage-mapping.md stage 3, INF rows).

Usage: python3 -I containment_match.py <inferred-rows.tsv> <tasklist.md> <out.tsv>
Case-folded content-word containment; fixed stopword set; threshold 0.6;
best ratio wins, first task in tasklist order breaks ties.
"""

import re
import sys

STOP = set(
    "a an the and or but nor so yet for of in on at to from by with into onto over "
    "under about as than then that this these those it its is are was were be been "
    "being am do does did has have had will would shall should can could may might must "
    "not no if when while which who whom whose what where why how all any each every "
    "same such only own up out off".split()
)


def words(text):
    return [w for w in re.findall(r"[a-z0-9_]+", text.lower()) if w not in STOP]


def tasks(md):
    out, cur, buf = [], None, []
    for line in md.splitlines():
        m = re.match(r"^## Task (\d+):", line)
        if m or re.match(r"^## Phase \d+:", line):
            if cur:
                out.append((cur, " ".join(buf)))
            cur, buf = (f"Task {m.group(1)}" if m else None), []
            if m:
                buf.append(line)
            continue
        if cur:
            buf.append(line)
    if cur:
        out.append((cur, " ".join(buf)))
    return out


def main():
    rows = [l.rstrip("\n").split("\t") for l in open(sys.argv[1]) if l.strip()]
    tl = tasks(open(sys.argv[2]).read())
    with open(sys.argv[3], "w") as f:
        f.write("id\tcitation\tmatch_method\tmatched_task\tratio\n")
        for rid, cite, quote in rows:
            q = set(words(quote))
            best = (0.0, None)
            for tid, text in tl:
                if not q:
                    break
                r = len(q & set(words(text))) / len(q)
                if r > best[0]:
                    best = (r, tid)
            method = "containment" if best[0] >= 0.6 else "none"
            f.write(f"{rid}\t{cite}\t{method}\t{best[1] if method != 'none' else ''}\t{best[0]:.2f}\n")


if __name__ == "__main__":
    main()
