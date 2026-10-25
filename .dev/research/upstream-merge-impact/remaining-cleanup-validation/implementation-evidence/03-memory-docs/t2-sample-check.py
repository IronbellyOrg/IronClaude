# Task 2 static check. Parses the sample file and the two guides; does NOT import the memory code.
import json, re, sys
from datetime import datetime

SAMPLE = "docs/memory/reflexion.jsonl.example"
GUIDES = ["docs/user-guide/memory-system.md", "docs/memory/README.md"]
fails = []
def check(ok, msg):
    print(("PASS " if ok else "FAIL ") + msg)
    if not ok: fails.append(msg)

def sig(e):  # same rules as the guide describes (digits->N, first 100 chars, " | " join)
    p = []
    if "error_type" in e: p.append(e["error_type"])
    if "error_message" in e: p.append(re.sub(r"\d+", "N", e["error_message"])[:100])
    if "test_name" in e: p.append(e["test_name"])
    return " | ".join(p)
def words(e): return set(sig(e).lower().split())
def ratio(a, b):
    x, y = words(a), words(b)
    return len(x & y), len(x | y), len(x & y) / len(x | y)

lines = open(SAMPLE).read().split("\n")
check(lines[-1] == "" and all(lines[:-1]), "file ends with one newline and has no blank lines")
rows = []
for n, line in enumerate(lines[:-1], 1):
    try:
        row = json.loads(line)
    except json.JSONDecodeError as e:
        check(False, f"line {n} is valid JSON ({e})"); continue
    rows.append(row)
    check(isinstance(row, dict), f"line {n} is one JSON object")
check(len(rows) == 6, f"six rows (found {len(rows)})")

OLD_KEYS = {"ts", "task", "mistake", "evidence", "rule", "fix", "tests", "status"}
SECRET = [r"(?i)(api[_-]?key|secret|passw(or)?d|token)\s*[:=]", r"sk-[A-Za-z0-9]{10,}", r"AKIA[0-9A-Z]{16}",
          r"[\w.+-]+@[\w-]+\.\w+", r"\b\d{1,3}(\.\d{1,3}){3}\b", r"[A-Za-z0-9+/]{32,}", r"https?://"]
for n, row in enumerate(rows, 1):
    for k in ("error_type", "error_message", "test_name", "solution"):
        check(isinstance(row.get(k), str) and row[k].strip(), f"row {n} has non-empty string {k}")
    check(len(row.get("solution", "")) >= 20, f"row {n} solution is useful (>= 20 chars)")
    for k in ("root_cause", "prevention", "traceback"):
        check(isinstance(row.get(k), str) and row[k].strip(), f"row {n} has non-empty string {k}")
    try:
        datetime.fromisoformat(row["timestamp"]); ok = True
    except Exception: ok = False
    check(ok, f"row {n} timestamp parses as ISO")
    check(row.get("synthetic") is True, f"row {n} is marked synthetic")
    check(not (OLD_KEYS & set(row)), f"row {n} has no old-layout keys")
    blob = json.dumps(row)
    check(not any(re.search(p, blob) for p in SECRET), f"row {n} has no credential/personal-data pattern")

# no two sample rows match each other (so first-match order is not ambiguous)
pair_ok = all(ratio(a, b)[2] < 0.7 for i, a in enumerate(rows) for j, b in enumerate(rows) if i != j)
check(pair_ok, "no two sample rows match each other at 0.7")

# guides: example row equals sample row 1 minus the synthetic marker
row1 = {k: v for k, v in rows[0].items() if k != "synthetic"}
for g in GUIDES:
    text = open(g).read()
    blocks = re.findall(r"```json\n(\{\"error_type\".*?)\n```", text, re.S)
    check(len(blocks) == 1 and json.loads(blocks[0]) == row1, f"{g}: example row equals sample row 1 minus synthetic")
    check("older layout" not in text and "older task/mistake" not in text, f"{g}: no old-layout wording")
    check('"synthetic": true' in text and "reflexion.jsonl.example" in text, f"{g}: describes the synthetic marker and names the sample file")
    check("does not validate" in text, f"{g}: says the recorder does not validate (no schema-validation claim)")
    check(not re.search(r"status.{0,40}(affects|decid|determin)", re.sub(r"(?i)no other field[^.]*\.", "", text)), f"{g}: no claim that status affects matching")
    check("solutions_learned.jsonl" in text and "Do not copy" in text, f"{g}: says not to copy the sample into solutions_learned.jsonl")

# guide worked examples recomputed from the sample's first row
cur = [
    ({"error_type": "ValueError", "error_message": "invalid port value 9090 in config file", "test_name": "test_load_config"}, (9, 10, "0.90")),
    ({"error_type": "ValueError", "error_message": "port value 9090 in settings", "test_name": "test_load_config"}, (7, 10, "0.70")),
    ({"error_type": "ValueError", "error_message": "invalid timeout value 30 in settings", "test_name": "test_load_settings"}, (6, 12, "0.50")),
]
guide = open(GUIDES[0]).read()
for c, (s, u, r) in cur:
    got = ratio(c, row1)
    check(got[:2] == (s, u) and f"{got[2]:.2f}" == r, f"worked example {s}/{u} = {r} recomputed from sample row 1 -> {got}")
    check(f"Shared {s} words / {u} distinct words = {r}" in guide, f"guide states 'Shared {s} words / {u} distinct words = {r}'")
print("RESULT:", "FAIL" if fails else "ALL PASS", f"({len(fails)} failures)")
sys.exit(1 if fails else 0)
