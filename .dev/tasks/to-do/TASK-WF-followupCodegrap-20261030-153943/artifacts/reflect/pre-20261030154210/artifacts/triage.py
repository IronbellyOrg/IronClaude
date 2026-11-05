import re, sys, yaml
from pathlib import Path
inf = {r["id"]: r for r in yaml.safe_load(Path(sys.argv[1]).read_text())["rows"]}
cov = yaml.safe_load(Path(sys.argv[2]).read_text())
plan = Path(sys.argv[3]).read_text()
tasks = re.split(r"^## Task (\d+):", plan, flags=re.M)
tasktext = {f"Task {tasks[i]}": tasks[i+1] for i in range(1, len(tasks), 2)}
constraints = plan.split("## Phase 1:")[0]
def secnum(s):
    m = re.search(r"§?\s*(\d+(?:\.\d+)?)", s or "")
    if "Decisions" in (s or ""): return "Decisions"
    return m.group(1) if m else None
def refs(text, n):
    if n == "Decisions": return "`## Decisions`" in text or "## Decisions" in text
    top = n.split(".")[0]
    pats = [rf"§{re.escape(n)}\b", rf"§{re.escape(top)}\b"] if "." not in n else [rf"§{re.escape(n)}\b"]
    return any(re.search(p, text) for p in pats)
out = []
for m in cov["matrix"]:
    if m["match_method"] != "none": continue
    r = inf[m["requirement_id"]]; n = secnum(r.get("section"))
    by = [t for t, tx in tasktext.items() if n and refs(tx, n)]
    if not by and n and refs(constraints, n): by = ["Constraints"]
    out.append({"id": r["id"], "section": r.get("section"), "citation": r["citation"],
                "triage": "covered-by-reference" if by else "needs-review", "referenced_by": by})
s = {"total_unmapped": len(out), "covered_by_reference": sum(o["triage"]=="covered-by-reference" for o in out),
     "needs_review": [o["id"] for o in out if o["triage"]=="needs-review"], "rows": out}
Path(sys.argv[4]).write_text(yaml.safe_dump(s, sort_keys=False))
print(s["total_unmapped"], s["covered_by_reference"], len(s["needs_review"]))
for o in out:
    if o["triage"]=="needs-review": print(o["id"], o["section"], o["citation"])
