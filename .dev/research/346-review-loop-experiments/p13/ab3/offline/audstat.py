import json, common as c, anchor
srcs={s["source"]:s for s in c.sources()}
maps={}
for l in open("findings_raw.jsonl"):
    r=json.loads(l)
    if r["doc"]!="final": continue
    s=srcs[r["source"]]
    if r["source"] not in maps: maps[r["source"]]=anchor.final_to_orig_map(s["doc_path"].read_text())
    mp=maps[r["source"]]
    ch=[n for n in r["cited"] if (n-1) not in mp]
    print(r["source"], r["fid"], "cited", r["cited"][:14], "CHANGED-in-final:", ch)
