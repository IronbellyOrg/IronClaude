"""O1 step 1: mechanical extraction of blocking findings from the 36 source reports."""
import json
import re
import common as c

ID_OVERRIDE = {  # arm-1 reports whose id line the C9.3 regex cannot read (see BUILD-NOTES)
    "a1-r2/R1": [f"F{i}" for i in range(1, 8)],
    "a1-r3/R1": [str(i) for i in range(1, 15)],
}
START = {"a1-r3/R1": "## Numbered findings list"}

QUOTE_RES = [re.compile(r"`([^`\n]+)`"), re.compile(r'"([^"\n]+)"'), re.compile(r"“([^”\n]+)”")]


def quotes_of(text):
    out = []
    for rx in QUOTE_RES:
        for m in rx.finditer(text):
            q = c.flat(m.group(1))
            for seg in re.split(r"\s*(?:\.\.\.|…)\s*", q):
                seg = seg.strip(" ,;:")
                if len(seg) >= 12 and seg not in out:
                    out.append(seg)
    return out


def main():
    rows = []
    stats = {}
    for s in c.sources():
        t = s["report"].read_text(errors="ignore")
        v = c.verdict_of(t)
        if s["source"] in ID_OVERRIDE:
            ids = ID_OVERRIDE[s["source"]] if v == "FAIL" else []
        else:
            ids = c.parse_ids(c.ids_from(s["report"])) if v == "FAIL" else []
        start = 0
        if s["source"] in START:
            start = next(i for i, l in enumerate(t.splitlines()) if l.startswith(START[s["source"]]))
        stats[s["source"]] = dict(verdict=v, ids=ids, missing=[])
        for order, fid in enumerate(ids):
            sec = c.find_section(t, fid, start)
            if sec is None:
                stats[s["source"]]["missing"].append(fid)
                rows.append(dict(source=s["source"], fid=fid, order=order, heading="", body="", theme="other",
                                 cited=[], quotes=[], section_found=False, doc=s["doc"]))
                continue
            text = sec["heading"] + "\n" + sec["body"]
            rows.append(dict(source=s["source"], fid=fid, order=order, heading=sec["heading"].strip(),
                             body=sec["body"], theme=c.tag(sec["heading"], sec["body"]),
                             cited=c.cited(text), quotes=quotes_of(text), section_found=True, doc=s["doc"]))
    with open(c.AB / "offline/findings_raw.jsonl", "w") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    print("findings", len(rows), "sources", len(stats))
    for k, v in stats.items():
        print(k, v["verdict"], len(v["ids"]), "missing:", v["missing"])
    # expected-theme check against C9.3 table (R1 / first audit of the 12 primary runs)
    exp = {"a3-r1": ("F1 T3,F2 T1", "B1 T1,B2 T2"), "a3-r2": ("R1-B1 T1,R1-B2 T2", "F-01 T3,F-02 T1"),
           "a3-r3": ("F1 T1,F2 T1,F3 T3", "F-1 T1,F-2 T2"), "a3-r4": ("F-01 T1", "A-01 other,A-02 T2"),
           "a3-r5": ("F-1 T1,F-2 T3,F-3 other", ""), "a3-r6": ("REQ-1 T2,REQ-2 T1,ARCH-1 T2", "F-01 T2"),
           "a2-r1": ("B-1 T3,B-2 T1", "F-1 T1,F-2 T2"), "a2-r2": ("B1 T1,B2 T2", "F-01 T2,F-02 T3"),
           "a2-r3": ("", "REQ-1 T1,REQ-2 T1,ARCH-1 T2"), "a2-r4": ("B-1 T1", "F-1 T1,F-2 T2,F-3 other"),
           "a2-r5": ("B-1 T2,B-2 T3", "F-1 T1"), "a2-r6": ("F-01 T1", "")}
    for run, (e1, e2) in exp.items():
        for step, e in (("R1", e1), ("AUD", e2)):
            got = ",".join(f"{r['fid']} {r['theme']}" for r in rows if r["source"] == f"{run}/{step}")
            print("THEME", "OK  " if got == e else "DIFF", run, step, "got:", got, "| expected:", e)


if __name__ == "__main__":
    main()
