"""O1 step 3: mechanical clustering (union-find) of anchored findings."""
import json
import common as c


def mech_clusters(rows):
    rows = [r for r in rows if r["status"] in ("quote", "cited")]
    parent = list(range(len(rows)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)

    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            a, b = rows[i], rows[j]
            sa, sb = a["orig_span"], b["orig_span"]
            near = sa[0] <= sb[1] + 3 and sb[0] <= sa[1] + 3
            if a["theme"] == b["theme"] and a["theme"] != "other" and near:
                union(i, j)
                continue
            A, B = set(a["lines"]), set(b["lines"])
            if A and B and len(A & B) / len(A | B) >= 0.5:
                union(i, j)
    groups = {}
    for i in range(len(rows)):
        groups.setdefault(find(i), []).append(rows[i])
    ordered = sorted(groups.values(), key=lambda g: min(rows.index(m) for m in g))
    return ordered


def main():
    rows = [json.loads(l) for l in open(c.AB / "offline/anchored.jsonl")]
    cl = mech_clusters(rows)
    out = []
    for n, g in enumerate(cl, 1):
        out.append(dict(cid=f"M{n}", members=[(m["source"], m["fid"]) for m in g]))
    json.dump(out, open(c.AB / "offline/mech_clusters.json", "w"), indent=1)
    print("mechanical clusters:", len(cl), "from", sum(len(g) for g in cl), "findings")
    for n, g in enumerate(cl, 1):
        print(f"M{n}", [(m["source"], m["fid"], m["theme"], tuple(m["orig_span"])) for m in g])


if __name__ == "__main__":
    main()
