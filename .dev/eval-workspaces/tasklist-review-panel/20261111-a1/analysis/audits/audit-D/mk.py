import collections, csv
rows = list(csv.reader(open("/tmp/audit-D/flags.tsv"), delimiter="\t"))[1:]
code = {"2-blockok": "B", "1-path": "P", "5-stale": "S", "3-conserve": "C", "3-dropped-blocking": "V", "5-doc": "D", "6-model": "M", "1-panel": "N"}
pk = {"designSpec": "DS", "makeTheAlias": "AL", "design-2026": "DE"}
g = collections.defaultdict(lambda: collections.defaultdict(set))
for c, row, p, rid, sev, why in rows:
    if sev != "EXCLUDE":
        continue
    short = "DS" if "designSpec" in p else "AL" if "makeTheAlias" in p else "DE"
    g[row][rid].add((short, code.get(c, c)))
n = 0
out = []
for row in sorted(g):
    parts = []
    for rid, s in sorted(g[row].items()):
        by = collections.defaultdict(set)
        for sh, cd in s:
            by[cd].add(sh)
        parts.append(rid + "[" + " ".join(f"{cd}:{'/'.join(sorted(v))}" for cd, v in sorted(by.items())) + "]")
        n += len(s)
    out.append(f"{row}: " + ", ".join(parts))
open("/tmp/audit-D/exclude-list.txt", "w").write("\n".join(out) + "\n")
print(len(out), "rows")
print("\n".join(out))
