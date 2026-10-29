"""Pass 1 (ID_REGEX) + Pass 2 (requirement-shaped line extraction) over the Phase 3 source.md.
usage: extract.py <source.md> <out.yaml>"""
import re, sys, yaml
src = open(sys.argv[1]).read().splitlines()
ID = re.compile(r"\b(R-\d+|REQ-\d+|SPEC-\d+|T-\d+)\b")
infence, sec, parsed, rows = False, "", [], []
def two(s):
    s = re.sub(r"\s+", " ", s.strip())
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z`*(])", s)
    return " ".join(parts[:2])[:600]
def add(i, section, text):
    rows.append({"id": f"INF-{len(rows)+1:03d}", "section": section, "quote": two(text), "citation": f"source.md:{i+1}"})
for i, l in enumerate(src):
    if l.lstrip().startswith("```"):
        infence = not infence; continue
    if infence: continue
    if l.startswith("#"):
        sec = l.lstrip("#").strip()[:60]; continue
    for m in ID.findall(l): parsed.append({"id": m, "citation": f"source.md:{i+1}"})
    if sec.startswith(("Decisions", "Review resolution", "2.")): continue   # rationale and brainstorm history, not requirements
    if sec.startswith("0.") and re.match(r"^\| G\d \|", l): add(i, sec, l)
    elif sec.startswith("1.1") and re.match(r"^\d\. \*\*", l): add(i, sec, l)
    elif sec.startswith("1.2") and re.match(r"^\| \d+ \|", l): add(i, sec, l)
    elif sec.startswith("1.2") and l.startswith("**Mirror rule"): add(i, sec, l)
    elif sec.startswith(("3.1", "3.2")) and re.match(r"^\| (Name|Inputs|Steps|Allowed|Outputs|Failure|Callers) ", l): add(i, sec, l)
    elif sec.startswith("3.3") and l.strip(): add(i, sec, l)
    elif sec.startswith("4.") and (re.match(r"^\d\. \*", l) or l.startswith("**Decision") or l.startswith("Primitives then")): add(i, sec, l)
    elif sec.startswith("5.") and (l.startswith("- ") or re.match(r"^\| \*\*T\d+", l)): add(i, sec, l)
    elif sec.startswith("6.") and re.match(r"^\d\. ", l): add(i, sec, l)
    elif sec.startswith("7.") and (l.startswith("- ") or l.startswith("**Never") or l.startswith("**Branch") or re.match(r"^\| H\d \|", l) or l.startswith("A mid-level") or l.startswith("**Decision log")): add(i, sec, l)
yaml.safe_dump({"pass": 2, "source": "source.md", "parsed_ids": parsed, "rows": rows}, open(sys.argv[2], "w"), sort_keys=False, width=200, allow_unicode=True)
print("parsed", len(parsed), "inferred", len(rows))
