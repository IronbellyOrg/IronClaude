import json, sys, re
import common as c
raw = {(r["source"], r["fid"]): r for r in map(json.loads, open(c.AB/"offline/findings_raw.jsonl"))}
anc = {(r["source"], r["fid"]): r for r in map(json.loads, open(c.AB/"offline/anchored.jsonl"))}
pat = sys.argv[1]; n = int(sys.argv[2]) if len(sys.argv) > 2 else 700
for k, r in raw.items():
    if re.search(pat, k[0]):
        a = anc[k]
        body = " ".join(r["body"].split())
        print(f"### {k[0]} {k[1]} [{r['theme']}] span={a['orig_span']} st={a['status']} q={ (a['quote'] or '')[:70]!r}")
        print("H:", r["heading"][:260]); print("B:", body[:n]); print()
