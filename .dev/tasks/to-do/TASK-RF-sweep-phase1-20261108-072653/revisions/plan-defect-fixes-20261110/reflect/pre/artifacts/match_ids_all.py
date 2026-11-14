"""Read-only literal ID matcher, all 355 items (open and completed), reflect pre run 3 (UC-1).

Same method as match_ids.py (run 2) with two changes: the item regex accepts both '- [ ]' and '- [x]'
(match_ids.py saw only the 218 open items), and D10 is added to the D family (the current DESIGN has D10).
Usage: match_ids_all.py <tasklist> <out.json>
"""
import json
import re
import sys

tasklist, out = sys.argv[1], sys.argv[2]
lines = open(tasklist, encoding="utf-8").read().split("\n")
items = []  # (item_id, start_line, end_line, done)
cur = None
for i, ln in enumerate(lines, 1):
    m = re.match(r"^- \[( |x)\] \*\*(\d+\.\d+)", ln)
    if m or ln.startswith("## ") or ln.startswith("### "):
        if cur:
            items.append((cur[0], cur[1], i - 1, cur[2]))
            cur = None
        if m:
            cur = (m.group(2), i, m.group(1) == "x")
if cur:
    items.append((cur[0], cur[1], len(lines), cur[2]))


def item_of(n):
    for it, s, e, _ in items:
        if s <= n <= e:
            return it
    return None


ids = [f"FR-{n:03d}" for n in range(1, 27)] + [f"NFR-{n:03d}" for n in range(1, 16)]
ids += [f"GQ-{n}" for n in range(101, 114)] + [f"D{n}" for n in range(1, 11)]
ids += ["SP-07", "SP-09", "SP-16"] + [f"SP-{n}" for n in range(19, 30)]
ids += ["R3-B1", "R3-B2", "R3-B3", "G-1", "INV-005", "INV-017"]
steps = ["1.0a", "1.0b", "1.1", "1.2", "1.3", "1.4a", "1.4", "1.5", "1.6", "1.7", "1.8", "1.9", "1.10",
         "1.11", "1.12", "1.13", "1.14", "1.15", "1.16", "1.16a", "1.17", "1.18", "1.19", "1.20", "1.21",
         "1.22", "1.23", "1.24", "1.24a", "1.24b", "1.25", "1.26", "1.27", "1.28", "1.29"]
res = {}
for i_d in ids:
    pat = re.compile(r"(?<![\w-])" + re.escape(i_d) + r"(?![\w])")
    hits = []
    for n, ln in enumerate(lines, 1):
        if pat.search(ln):
            it = item_of(n)
            if it and it not in [h[0] for h in hits]:
                hits.append((it, n))
    res[i_d] = hits
for st in steps:
    hits = []
    for n, ln in enumerate(lines, 1):
        for m in re.finditer(r"(?<![\d.\w])" + re.escape(st) + r"(?![\d\w])", ln):
            pre = ln[max(0, m.start() - 40):m.start()]
            if re.search(r"[Ss]teps?\b", pre):
                it = item_of(n)
                if it and it not in [h[0] for h in hits]:
                    hits.append((it, n))
                break
    res["step-" + st] = hits
for r in range(1, 9):
    hits = []
    for n, ln in enumerate(lines, 1):
        for m in re.finditer(rf"(?<![\w-])R{r}(?![\w-])", ln):
            pre = ln[max(0, m.start() - 40):m.start()]
            if re.search(r"\brows?\b", pre):
                it = item_of(n)
                if it and it not in [h[0] for h in hits]:
                    hits.append((it, n))
                break
    res[f"R{r}"] = hits
fam = re.compile(r"\b(FR|NFR|GQ|SP)-(\d+)\s*(?:to|\.\.)\s*(?:\1-)?(\d+)\b")
stp = re.compile(r"[Ss]teps? (1\.\d+[ab]?)\s*(?:to|\.\.)\s*(1\.\d+[ab]?)\b")
rrw = re.compile(r"\bR(\d) (?:to|\.\.) R(\d)\b")
ranged = {}
for n, ln in enumerate(lines, 1):
    it = item_of(n)
    if not it:
        continue
    for m in fam.finditer(ln):
        f, a, b = m.group(1), int(m.group(2)), int(m.group(3))
        if b <= a or b - a > 30:
            continue
        w = 3 if f in ("FR", "NFR") else (2 if f == "SP" else 0)
        for k in range(a, b + 1):
            key = f"{f}-{k:0{w}d}" if w else f"{f}-{k}"
            ranged.setdefault(key, []).append((it, n))
    for m in stp.finditer(ln):
        a, b = m.group(1), m.group(2)
        if a in steps and b in steps and steps.index(b) > steps.index(a):
            for st in steps[steps.index(a):steps.index(b) + 1]:
                ranged.setdefault("step-" + st, []).append((it, n))
    for m in rrw.finditer(ln):
        a, b = int(m.group(1)), int(m.group(2))
        for k in range(a, b + 1):
            ranged.setdefault(f"R{k}", []).append((it, n))
for k, v in ranged.items():
    if k in res:
        for it, n in v:
            if it not in [h[0] for h in res[k]]:
                res[k].append((it, n))
json.dump({"item_count": len(items), "open_items": sum(1 for x in items if not x[3]),
           "hits": res, "ranged": ranged}, open(out, "w"), indent=0)
print(len(items))
for k, v in res.items():
    print(k, len(v), " ".join(f"{a}@{b}" for a, b in v[:16]))
