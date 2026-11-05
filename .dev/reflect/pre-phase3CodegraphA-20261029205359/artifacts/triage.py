"""Map each containment-unmatched INF row to the plan task that covers it by explicit reference.
usage: triage.py <inferred.yaml> <matrix.yaml> <out.yaml>"""
import re, sys, yaml
rows = {r["id"]: r for r in yaml.safe_load(open(sys.argv[1]))["rows"]}
mx = yaml.safe_load(open(sys.argv[2]))["matrix"]
ROW = [((1, 2, 3, 4, 36, 39), "Task 4"), (tuple(range(5, 13)), "Task 5"), (tuple(range(13, 19)), "Task 6"),
       ((19, 20, 21, 22, 23, 24, 25, 26, 28, 29), "Task 10"), ((27,), "Task 11"),
       (tuple(range(30, 39)) + (40,), "Task 7"), ((41, 42), "Task 1 (G6) + Task 13 check (3)")]
out = []
for m in mx:
    if m["matched_task_ids"]:
        continue
    r = rows[m["requirement_id"]]; sec = r["section"]; q = r["quote"]
    cover, ref = None, None
    if sec.startswith("0."):
        cover, ref = "Task 1", "Task 1 body: 'run every row G1-G6 of source §0'"
    elif sec.startswith("1.1"):
        cover, ref = "Constraints", "Constraints: 'Standing rules 1-9 of source §1.1 apply to every edited primitive'"
    elif sec.startswith("1.2"):
        n = int(re.match(r"\| (\d+) \|", q).group(1))
        cover = next(t for ns, t in ROW if n in ns); ref = f"{cover} body names 'source §1.2 rows' range containing {n}"
    elif sec.startswith("3.1"):
        cover = "Task 12" if q.startswith("| Callers") else "Task 9"; ref = f"{cover} body: built from DES §4/§5 with source §3.1"
    elif sec.startswith("3.2"):
        cover, ref = "Task 8", "Task 8 body: built from DES §2 with source §3.2 allowed tools and overrides"
    elif sec.startswith("4."):
        cover, ref = "Task 3", "Task 3 body: 'the seven sections of source §4'"
    elif sec.startswith("7."):
        cover, ref = "Constraints", "Constraints: 'the list in source §7 Decide alone' / 'human items H1-H5 of source §7'"
    out.append({"requirement_id": m["requirement_id"], "citation": r["citation"], "ratio": m["ratio"],
                "covered_by": cover, "coverage_kind": "by-reference" if cover else "gap", "reference": ref})
gaps = [o for o in out if o["covered_by"] is None]
yaml.safe_dump({"unmatched": len(out), "by_reference": len(out) - len(gaps), "real_gaps": len(gaps), "rows": out},
               open(sys.argv[3], "w"), sort_keys=False, width=200)
print("unmatched", len(out), "gaps", len(gaps))
