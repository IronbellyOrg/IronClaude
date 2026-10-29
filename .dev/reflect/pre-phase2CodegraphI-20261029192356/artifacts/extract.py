"""Pass 1 (ID_REGEX) + Pass 2 (requirement-shaped line extraction) over source.md.
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
    if sec.startswith(("Decisions", "Review resolution", "0.")): continue
    if re.match(r"^\| (F\d+|U\d+) \|", l): add(i, sec, l)
    elif re.match(r"^\*\*T\d+b?\. ", l): add(i, sec, l)
    elif re.match(r"^Change: ", l): add(i, sec, l)
    elif sec.startswith("2.12") and l.startswith("- "): add(i, sec, l)
    elif sec.startswith("3.2") and re.match(r"^\d\. ", l): add(i, sec, l)
    elif sec.startswith("7.") and (re.match(r"^\| (Simple|Mid|Complex)", l) or re.match(r"^\d\. ", l) or l.startswith("Hard rules")): add(i, sec, l)
    elif sec.startswith("6.") and l.startswith("After each task-group"): add(i, sec, l)
    elif re.match(r"^\d\. (Save this|Leg A|X-25 check|Bands on D|Leg B|Decision:|Write `)", l): add(i, sec, l)
    elif sec.startswith("8.") and re.match(r"^\| \d \| IronClaude", l): add(i, sec, l)
yaml.safe_dump({"pass": 2, "source": "source.md", "parsed_ids": parsed, "rows": rows}, open(sys.argv[2], "w"), sort_keys=False, width=200, allow_unicode=True)
print("parsed", len(parsed), "inferred", len(rows))
