import json,collections,re
d=json.load(open("stats.json"))
fl=[l.rstrip("\n").split("\t") for l in open("flags.tsv")][1:]
vi=[f for f in fl if f[0]=="2-verdict-inconsistent"]
print(collections.Counter(re.sub(r"\d+","N",f[5]) for f in vi))
print(collections.Counter(re.sub(r"\d+","N",f[5]) for f in fl if f[0]=="3-anchor-length").most_common(5))
print(d["pkgruns"],d["rows"],d["runs"],d["nwarn"],len(d["exclude_runs"]))
for m,s in sorted(d["stats"].items()):
    print(m,s[0],s[1],s[2],s[3], f"{s[2]/s[1]*100:.1f}% ws / {s[3]/s[1]*100:.1f}% exact" if s[1] else "")
print(collections.Counter(f[2][:18]+"|"+f[4] for f in fl))
