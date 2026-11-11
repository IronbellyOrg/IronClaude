"""O1 steps 4-6: apply the hand adjudication, compute confirmed/residual, write catalog.json, catalog.md, BUILD-NOTES.md."""
import collections
import json
import os
import random
import sys
import common as c
import adjudication as A
import cluster as CL

OUTNAME = sys.argv[1] if len(sys.argv) > 1 else "catalog.json"
ORIG_TEXT = c.ORIG.read_text()
raw = {(r["source"], r["fid"]): r for r in map(json.loads, open(c.AB / "offline/findings_raw.jsonl"))}
anc = [json.loads(l) for l in open(c.AB / "offline/anchored.jsonl")]
anc_by = {(r["source"], r["fid"]): r for r in anc}
order = {(r["source"], r["fid"]): i for i, r in enumerate(anc)}
srcs = {s["source"]: s for s in c.sources()}

# --- validate the assignment covers every blocking finding exactly once-or-more
keys = set(anc_by)
assigned = set(A.ASSIGN) | set(A.REVISION_INTRODUCED)
assert keys == assigned, (sorted(keys - assigned), sorted(assigned - keys))
assert not (set(A.ASSIGN) & set(A.REVISION_INTRODUCED))
for k, v in A.DEFECTS.items():
    assert c.locate(ORIG_TEXT, v[1]), f"anchor does not locate in the original: {k}: {v[1]}"

# revision-introduced evidence
rev = []
for (s, f), q in A.REVISION_INTRODUCED.items():
    ft = srcs[s]["doc_path"].read_text()
    assert c.locate(ft, q) and not c.locate(ORIG_TEXT, q), (s, f, q)
    rev.append(dict(source=s, fid=f, quote=q))

# --- build clusters, renumber by first member
members = collections.defaultdict(list)
for key, ks in A.ASSIGN.items():
    for k in ks:
        members[k].append(key)
assert set(members) == set(A.DEFECTS), set(A.DEFECTS) ^ set(members)
firsts = {k: min(order[m] for m in ms) for k, ms in members.items()}
ranked = sorted(members, key=lambda k: firsts[k])
cid_of = {k: f"D{i}" for i, k in enumerate(ranked, 1)}
clusters = []
for k in ranked:
    label, anchor, reason = A.DEFECTS[k]
    ms = sorted(members[k], key=lambda m: order[m])
    themes = collections.Counter(anc_by[m]["theme"] for m in ms if anc_by[m]["theme"] != "other")
    theme = themes.most_common(1)[0][0] if themes else "other"
    span = list(c.locate(ORIG_TEXT, anchor)[0])
    mem = []
    for m in ms:
        a = anc_by[m]
        q = a["quote"] or (raw[m]["quotes"][0] if raw[m]["quotes"] else raw[m]["heading"][:120])
        mem.append(dict(source=m[0], fid=m[1], blocking=True, quote=q[:200], doc=raw[m]["doc"]))
    clusters.append(dict(cid=cid_of[k], theme=theme, label=label, anchor=anchor, orig_span=span, members=mem,
                         n_sources=len({x["source"] for x in mem}), confirmed=len({x["source"] for x in mem}) >= 2,
                         adjudication_reason=reason))

# --- overrides derived from the difference with the mechanical clusters
mech = json.load(open(c.AB / "offline/mech_clusters.json"))
mech_of = {tuple(m): mc["cid"] for mc in mech for m in mc["members"]}
# unanchored/revision findings are not in the mechanical clusters
overrides = []
by_mech = collections.defaultdict(set)
for cl in clusters:
    for m in cl["members"]:
        mc = mech_of.get((m["source"], m["fid"]))
        if mc:
            by_mech[mc].add(cl["cid"])
for mc, cids in sorted(by_mech.items(), key=lambda x: int(x[0][1:])):
    if len(cids) > 1:
        cs = sorted(cids, key=lambda x: int(x[1:]))
        q = next(c2["anchor"] for c2 in clusters if c2["cid"] == cs[0])
        overrides.append(dict(action="split", cids=cs, mechanical=mc, quote=q,
                              reason=f"mechanical cluster {mc} pooled findings that name different wrong outcomes"))
mech_in = collections.defaultdict(set)
for cl in clusters:
    for m in cl["members"]:
        mc = mech_of.get((m["source"], m["fid"]))
        if mc:
            mech_in[cl["cid"]].add(mc)
for cid, mcs in mech_in.items():
    if len(mcs) > 1:
        cl = next(x for x in clusters if x["cid"] == cid)
        overrides.append(dict(action="merge", cids=[cid], mechanical=sorted(mcs, key=lambda x: int(x[1:])),
                              quote=cl["anchor"], reason=f"members from {len(mcs)} mechanical clusters name the same wrong outcome: {cl['label']}"))
multi = collections.defaultdict(list)
for cl in clusters:
    for m in cl["members"]:
        multi[(m["source"], m["fid"])].append(cl["cid"])
for k, cids in sorted(multi.items(), key=lambda x: order[x[0]]):
    if len(cids) > 1:
        cl = next(x for x in clusters if x["cid"] == cids[0])
        overrides.append(dict(action="move", cids=cids, finding=list(k), quote=cl["anchor"],
                              reason="the finding names more than one distinct wrong outcome and is a member of each"))
for r in rev:
    overrides.append(dict(action="move", cids=[], finding=[r["source"], r["fid"]], quote=r["quote"],
                          reason="rests on text added by the revisions (quote is in the final spec, not in the original): revision_introduced"))

# --- residual
residual = {}
fin_text = {}
for run in c.ALL_RUNS:
    ft = c.final_spec(run).read_text()
    hits = {}
    for step in ("AUD", "AUD2"):
        src = f"{run}/{step}"
        if src in srcs:
            hits[step] = [cl["cid"] for cl in clusters if any(m["source"] == src for m in cl["members"])]
    reported = {x for v in hits.values() for x in v}
    present = [cl["cid"] for cl in clusters if c.locate(ft, cl["anchor"]) or cl["cid"] in reported]
    residual[run] = dict(present=present, audit_hits=hits)

cat = dict(schema="defect-catalog/1", doc_sha256=c.SPEC_SHA, built_by="pn3", sources=list(srcs),
           clusters=clusters, revision_introduced=rev,
           unanchored=[], overrides=overrides, residual=residual)
tmp = c.CAT / (OUTNAME + ".tmp")
json.dump(cat, open(tmp, "w"), indent=1)
os.replace(tmp, c.CAT / OUTNAME)

# --- human readable
md = ["# Defect catalog (defect-catalog/1, built by pn3)", "", f"doc sha256 `{c.SPEC_SHA}`", "",
      "| cid | theme | confirmed | sources | label | anchor span |", "|---|---|---|---|---|---|"]
for cl in clusters:
    md.append(f"| {cl['cid']} | {cl['theme']} | {'yes' if cl['confirmed'] else 'no'} | {cl['n_sources']} | {cl['label']} | {cl['orig_span']} |")
md += ["", "## Members", ""]
for cl in clusters:
    md.append(f"### {cl['cid']} {cl['label']}")
    md.append(f"anchor: `{cl['anchor']}`  ({cl['adjudication_reason']})")
    md.append(", ".join(f"{m['source']}:{m['fid']}" for m in cl["members"]))
    md.append("")
md += ["## Revision-introduced", ""] + [f"- {r['source']} {r['fid']}: `{r['quote']}`" for r in rev]
(c.CAT / (OUTNAME.replace(".json", ".md"))).write_text("\n".join(md) + "\n")
print("clusters", len(clusters), "confirmed", sum(cl["confirmed"] for cl in clusters), "overrides", len(overrides),
      "revision_introduced", len(rev))
