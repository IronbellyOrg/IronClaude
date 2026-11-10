import json, pathlib, re, collections
sel = json.load(open("adj-pass2-sel.json"))
TRUE = {"PATH": {0, 1}, "PHASE": {18}, "KV": set(), "COUNT": set()}
REF_FALSE = {82}
DEFECT = {0, 1, 18}
WHY = {
 "PATH": ("true", "original: the adversarial and workflow report paths differ from the WC-4 template and no text reconciles them", "revised text lists the places or says the child's legacy path applies only without --report-dir, or the row says 'also write'/'under --unattended write ... to --report-dir'"),
 "PHASE": ("true", "original: AC-0.4 (P0) requires 7.2 step 3 whose pass condition is the WC-4 contract path introduced in P1", "revised text handles it ('pre-contract forms', 'no WC-4 contract exists before P1'), or the section reference is a whole-section reference (3, 6, 2.1) that does not make the row depend on the later requirement"),
 "KV": ("", "", "different quantities (cap vs threshold vs heartbeat), not one value bound twice"),
}
out = []
for i, f in enumerate(sel["flags"]):
    c = f["check"]
    if c == "REF":
        v = "false" if i in REF_FALSE else "true"
        w = "NG-4 is defined inline in the Non-goals cell" if i in REF_FALSE else "id is not defined anywhere in this document (cross-document, test-matrix or revision-log reference)"
    else:
        t, wt, wf = WHY[c]
        v = "true" if i in TRUE[c] else "false"; w = wt if v == "true" else wf
    lines = pathlib.Path(f["path"]).read_text(errors="replace").split("\n")
    a = " ".join(lines[f["lines"][0]-1].split())[:160]
    b = " ".join(lines[f["other_lines"][0]-1].split())[:160] if f["other_lines"] else ""
    out.append({"doc_sha": f["doc_sha"], "lint_id": f["lint_id"], "check": c, "verdict": v, "defect": "yes" if i in DEFECT else "no",
                "why": w, "evidence": a + " || " + b, "dedupe_key": [c, f["quote"], f["message"]], "n_docs": f["n_docs"]})
with open("adjudication-pass2.jsonl", "w") as fh:
    for r in out: fh.write(json.dumps(r) + "\n")
print(dict(collections.Counter((r["check"], r["verdict"]) for r in out)))
