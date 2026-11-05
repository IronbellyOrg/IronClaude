import re, sys, yaml
plan = open(sys.argv[1]).read()
m = yaml.safe_load(open(sys.argv[2])); rows = {r["id"]: r for r in yaml.safe_load(open(sys.argv[3]))["rows"]}
ids = set(re.findall(r"\b([CSPD]\d+)\b", plan))
for a, b in re.findall(r"\b([CSPD]\d+)-[CSPD]?(\d+)\b", plan):
    pre, lo = a[0], int(a[1:])
    ids |= {f"{pre}{i}" for i in range(lo, int(b) + 1)}
secs = set(re.findall(r"§(\d+(?:\.\d+)?)", plan))
out = []
for x in m["matrix"]:
    if x["matched_task_ids"]: continue
    r = rows[x["requirement_id"]]; sec = str(r.get("section", ""))
    rid = re.search(r"\b([CSPD]\d+)\b", sec + " " + r["quote"][:40])
    s = re.match(r"(\d+(?:\.\d+)?)", sec)
    if rid and rid.group(1) in ids: how = f"row-ref {rid.group(1)}"
    elif s and (s.group(1) in secs or s.group(1).split(".")[0] in secs): how = f"section-ref §{s.group(1)}"
    elif re.match(r"8 (T\d+[a-c]?)", sec): how = "task-section (T-id mapped by order)"
    else: how = "NO-REF"
    out.append({"id": x["requirement_id"], "section": sec, "citation": r["citation"], "triage": how})
yaml.safe_dump(out, open(sys.argv[4], "w"), sort_keys=False, width=200)
from collections import Counter
print(Counter(o["triage"].split()[0] for o in out))
for o in out:
    if o["triage"] == "NO-REF": print(o["id"], o["section"], o["citation"], "|", rows[o["id"]]["quote"][:140])
