import json, random, common as c
cat = json.load(open(c.CAT/"catalog.json"))
raw = {(r["source"], r["fid"]): r for r in map(json.loads, open("findings_raw.jsonl"))}
mem = [(cl["cid"], cl["label"], m["source"], m["fid"]) for cl in cat["clusters"] for m in cl["members"]]
rng = random.Random(0)
samp = rng.sample(mem, max(1, round(0.2*len(mem))))
print("memberships", len(mem), "sample", len(samp))
json.dump([list(s) for s in samp], open("recheck_sample.json","w"))
for cid, label, s, f in samp:
    r = raw[(s, f)]
    print(f"## {cid} [{label[:70]}]  <-  {s}:{f}\n   {' '.join(r['heading'].split())[:200]}\n   {' '.join(r['body'].split())[300:620]}")
