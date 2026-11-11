import json, pathlib, re
sel = json.load(open("adj-pass1-sel.json"))
T = {32,37,39,40,46,49,51,53,54,55,59}                      # REF true (mechanical fact: id never defined in that document)
DEFECT = {40}                                               # REF: leaked review id in a spec = plausible defect
why = {}
for i in range(len(sel["flags"])):
    f = sel["flags"][i]; c = f["check"]
    if c == "REF":
        why[i] = ("true" if i in T else "false",
                  "defect:yes" if i in DEFECT else "defect:no",
                  "id not defined anywhere in the document" if i in T else
                  {31:"mis-parse: 'Wave 0 step 3' read as section step",35:"fragment of compound id FR-L-16",36:"fragment of compound id FR-L-33",41:"fragment of compound id FR-L-44",
                   43:"fragment of T-ISO-9",45:"fragment of FR-L-46",50:"fragment of T-FC-3",56:"fragment of T-GH-14",44:"WC-5.2 defined in bold inside the WC-5 row cell",
                   38:"OB-9 defined inline in the 'Observed runs' sentence",48:"OB-5 defined inline in the 'Observed runs' sentence"}.get(i, "AC id defined in the ID column (second cell) of its table row"))
    elif c == "COUNT":
        why[i] = ("false", "defect:no", "the line is itself a list item / sentence about a different set; the list after it is the same numbered list, not the counted set")
    elif c == "PHASE":
        why[i] = ("false", "defect:no", "the P-row mentions the id to say it does not exist yet or to name the requirement P0/P1 writes; no dependency on a later phase")
    elif c == "KV":
        why[i] = ("false", "defect:no", "different quantities or different columns/keys sharing a word; no conflict")
    elif c == "PATH":
        why[i] = ("false", "defect:no", "bare filename mention, or a different command's own path, or a path the WC-4 rule text lists explicitly")
out = []
for i, f in enumerate(sel["flags"]):
    lines = pathlib.Path(f["path"]).read_text(errors="replace").split("\n")
    a = " ".join(lines[f["lines"][0]-1].split())[:160]
    b = " ".join(lines[f["other_lines"][0]-1].split())[:160] if f["other_lines"] else ""
    v, d, w = why[i]
    # n_docs: identical flags in other documents share the verdict (dedupe by quote+message)
    out.append({"doc_sha": f["doc_sha"], "lint_id": f["lint_id"], "check": f["check"], "verdict": "true" if v == "true" else "false",
                "defect": d.split(":")[1], "why": w, "evidence": a + " || " + b, "dedupe_key": [f["check"], f["quote"], f["message"]], "n_docs": f["n_docs"]})
with open("adjudication-pass1.jsonl", "w") as fh:
    for r in out: fh.write(json.dumps(r) + "\n")
import collections
c = collections.Counter((r["check"], r["verdict"]) for r in out); print(dict(c))
