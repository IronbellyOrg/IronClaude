#!/usr/bin/env python3
"""O2: truth.json. For each corpus document: the audit / R1 reports that judged it and their blocking findings
(id, theme, cited line set, heading), by the C9.3 functions. Also uses catalog.json when present."""
import json, os, pathlib, re, glob
import c93
SP = pathlib.Path(os.environ["SP"]); AB = pathlib.Path(os.environ["AB"])
D = ".dev/orca-command-refactor"
corpus = json.load(open(AB/"offline/corpus.json"))
sha_of_label = {}
for r in corpus:
    for lab in r["labels"]: sha_of_label[lab] = r["sha256"]
ORIG_SHA = next(r["sha256"] for r in corpus if r["group"] == "orig")

def report_findings(path, source):
    p = pathlib.Path(path)
    if not p.exists(): return {"source": source, "path": str(p), "exists": False}
    t = p.read_text(errors="ignore")
    vs = re.findall(r"verdict:\s*\**\s*(PASS|FAIL|INCOMPLETE)", t, re.I)
    verdict = vs[-1].upper() if vs else "NONE"
    ids = c93.parse_ids(c93.ids_from(p)) if verdict != "PASS" else []
    fs = []
    for fid in ids:
        sec = c93.find_section(t, fid)
        if sec is None:
            fs.append({"id": fid, "theme": "other", "cited": [], "heading": None, "found": False}); continue
        head, body, a, b = sec
        text = head + "\n" + body
        fs.append({"id": fid, "theme": c93.tag(head, body), "cited": c93.cited(text), "heading": head.strip()[:160], "found": True})
    return {"source": source, "path": str(p), "exists": True, "verdict": verdict, "ids": ids, "findings": fs}

truth = {r["sha256"]: {"labels": r["labels"], "group": r["group"], "reports": []} for r in corpus}
# audits of finals
for r in corpus:
    for lab in r["labels"]:
        g, _, name = lab.partition(":")
        if g != "final": continue
        run = name
        a1 = SP/f"p11/runs/{run}/aud/ws/{D}/review/audit.md"
        truth[r["sha256"]]["reports"].append(dict(report_findings(a1, f"{run}/AUD"), kind="audit", run=run))
        if run.startswith("a3-"):
            a2 = SP/f"p12/baseline-audit2/{run}/ws/{D}/review/audit.md"
            truth[r["sha256"]]["reports"].append(dict(report_findings(a2, f"{run}/AUD2"), kind="audit", run=run))
# R1 reports on the original
for run in sorted(os.listdir(SP/"p11/runs")):
    arm = run[1]
    f = "spec-panel.md" if arm == "1" else "round1.md"
    truth[ORIG_SHA]["reports"].append(dict(report_findings(SP/f"p11/runs/{run}/ws/{D}/review/{f}", f"{run}/R1"), kind="r1", run=run))
# catalog, if present
cat = SP/"p13/catalog/catalog.json"
catalog = None
if cat.exists():
    catalog = json.load(open(cat))
    truth[ORIG_SHA]["catalog"] = {"clusters": catalog.get("clusters"), "residual": catalog.get("residual")}
json.dump({"orig_sha": ORIG_SHA, "catalog_present": bool(catalog), "docs": truth}, open(AB/"offline/truth.json", "w"), indent=1)
# summary
for sha, rec in truth.items():
    if not rec["reports"]: continue
    print(rec["group"], rec["labels"][0] if rec["group"]!="orig" else "orig", sha[:8])
    for rp in rec["reports"]:
        if not rp.get("exists"): print("   MISSING", rp["source"]); continue
        print("  ", rp["kind"], rp["source"], rp["verdict"], [(f["id"], f["theme"]) for f in rp["findings"]], "unfound:", [f["id"] for f in rp["findings"] if not f["found"]])
