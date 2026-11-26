import json, glob
leg = json.load(open("/tmp/issue-legend.json"))
order = [l["label"] for l in leg if l["blocking"]] + [l["label"] for l in leg if not l["blocking"]]
direct = {r["panel"]: r for r in json.load(open("/tmp/issue-table-direct.json"))}
top = json.load(open("/tmp/top10.json"))
mism = 0; rows = []
for i, t in enumerate(top, 1):
    a = json.load(open(f"/tmp/issue-table/issue-{i:02d}.json"))
    d = direct[t["panel"]]
    for k in order:
        if a["found"].get(k) != d["found"][k]: mism += 1; print("MISMATCH", i, t["panel"], k, "agent", a["found"].get(k), "direct", d["found"][k])
        if a["blocking_credit"].get(k) != d["blk"][k]: mism += 1; print("MISMATCH-BLK", i, t["panel"], k, "agent", a["blocking_credit"].get(k), "direct", d["blk"][k])
    if a["n_runs"] != t["n"] or a["denominators"] != d["den"]: print("N/DEN differs", i, a["n_runs"], a["denominators"], d["den"])
    if a.get("issues"): print("agent", i, "issues:", str(a["issues"])[:200])
    rows.append((i, t["panel"], a))
print("total cell mismatches:", mism)
# final table: cell = found (blocking-row credit) for B labels; plain found for I labels
L = ["| # | Panel | Runs | " + " | ".join(order) + " | Found /14 |", "|---|---|---|" + "---|" * len(order) + "---|"]
for i, p, a in rows:
    cells = [str(a["found"][k]) + (f" ({a['blocking_credit'][k]})" if k.startswith("B") and a["found"][k] else "") for k in order]
    L.append(f"| {i} | {p} | {a['n_runs']} | " + " | ".join(cells) + f" | {top[i-1]['mean_found']} |")
open("/tmp/issue-table-final.md", "w").write("\n".join(L) + "\n")
print("\n".join(L))
