"""O1 step 2: anchor each finding to a span of the ORIGINAL spec (quote > cited lines > none)."""
import collections
import difflib
import json
import common as c

ORIG_TEXT = c.ORIG.read_text()
ORIG_LINES = ORIG_TEXT.split("\n")


def final_to_orig_map(final_text):
    """final line index -> original line index for `equal` lines only (C5 opcodes final -> original)."""
    fl = final_text.split("\n")
    m = {}
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, fl, ORIG_LINES, autojunk=False).get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                m[i1 + k] = j1 + k
    return m


def first_group(lines):
    """cited lines (1-based, ordered): the first line plus following ones within 3 lines of the previous."""
    g = [lines[0]]
    for n in lines[1:]:
        if 0 <= n - g[-1] <= 3:
            g.append(n)
        elif n < g[0] or n > g[-1] + 3:
            continue
    return g


def main():
    srcs = {s["source"]: s for s in c.sources()}
    maps = {}
    out = []
    for line in open(c.AB / "offline/findings_raw.jsonl"):
        f = json.loads(line)
        s = srcs[f["source"]]
        rec = dict(source=f["source"], fid=f["fid"], order=f["order"], theme=f["theme"], doc=f["doc"], status=None,
                   orig_span=None, lines=None, quote=None, reason=None, all_spans=[], heading=f["heading"][:200])
        final_text = None
        if f["doc"] == "final":
            final_text = s["doc_path"].read_text()
            if f["source"] not in maps:
                maps[f["source"]] = final_to_orig_map(final_text)
        mp = maps.get(f["source"])
        in_final = []  # (quote, span) located in the final but not in the original
        for q in f["quotes"]:
            o = c.locate(ORIG_TEXT, q)
            if o:
                rec["all_spans"].append([q[:80], o[0][0], o[0][1], len(o)])
                if rec["status"] is None:
                    rec.update(status="quote", orig_span=list(o[0]), quote=q, lines=list(range(o[0][0], o[0][1])))
            elif final_text is not None:
                fs = c.locate(final_text, q)
                if fs:
                    in_final.append((q, fs[0]))
        if rec["status"] is None and in_final:
            for q, (a, b) in in_final:
                mapped = [mp.get(i) for i in range(a, b)]
                if all(x is not None for x in mapped):
                    rec.update(status="quote", orig_span=[mapped[0], mapped[-1] + 1], quote=q, lines=mapped)
                    rec["reason"] = "final span mapped to original via equal lines"
                    break
            if rec["status"] is None:
                rec.update(status="revision_introduced", quote=in_final[0][0],
                           reason="quote found only in the final spec, its lines are not equal lines of the original")
        if rec["status"] is None and f["cited"]:
            g = first_group(f["cited"])
            if f["doc"] == "original":
                idx = [n - 1 for n in g if 1 <= n <= len(ORIG_LINES)]
            else:
                idx = [mp.get(n - 1) for n in g]
                idx = [i for i in idx if i is not None] if idx and all(i is not None for i in idx) else []
            if idx:
                rec.update(status="cited", orig_span=[min(idx), max(idx) + 1], lines=idx,
                           reason=f"first cited group {g}")
        if rec["status"] is None:
            rec.update(status="unanchored", reason="no quote located; "
                       + ("no cited lines" if not f["cited"] else "cited lines are not equal lines of the original"))
        out.append(rec)
    with open(c.AB / "offline/anchored.jsonl", "w") as fh:
        for r in out:
            fh.write(json.dumps(r) + "\n")
    by = collections.defaultdict(collections.Counter)
    for r in out:
        by[r["source"]][r["status"]] += 1
    tot = collections.Counter()
    for k, v in by.items():
        print(f"{k:12s}", dict(v))
        tot.update(v)
    print("TOTAL", dict(tot))


if __name__ == "__main__":
    main()
