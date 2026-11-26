import os, re, json, glob, datetime
E = "/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1"
W = re.compile(r"(>\s*\S*cand/|\btee\b[^|]*cand/|sed\s+-i[^|;]*cand/|\b(cp|mv|rm|chmod|truncate|touch|ln)\b[^|;]*cand/|open\([^)]*cand/[^)]*['\"][wa]|write_text|write_bytes|\.write\()")
n = 0; hits = []; byrun = []
files = glob.glob(f"{E}/*/reviews/**/*.attempt*.json", recursive=True)
files = [f for f in files if re.search(r"attempt\d+\.json$", f)]
print("json files", len(files))
for f in files:
    try: j = json.load(open(f))
    except Exception: continue
    if not isinstance(j, list): continue
    for m in j:
        c = (m.get("message") or {}).get("content")
        if m.get("type") == "assistant" and isinstance(c, list):
            for b in c:
                if b.get("type") == "tool_use":
                    s = json.dumps(b.get("input", {}))
                    if "cand/" in s and W.search(s):
                        hits.append((f.replace(E, ""), b["name"], s[:260]))
print("cand-write-like tool_use:", len(hits))
for h in hits[:25]: print(h)
# timeline: earliest start of any attempt and files mtime around 17:50 / 18:06
mt = sorted((os.path.getmtime(f), f.replace(E, "")) for f in files)
print("earliest json mtime", datetime.datetime.fromtimestamp(mt[0][0], datetime.timezone.utc), mt[0][1])
for lo, hi in (("2026-11-11 17:45", "2026-11-11 17:51"), ("2026-11-11 18:00", "2026-11-11 18:07")):
    a = datetime.datetime.fromisoformat(lo).replace(tzinfo=datetime.timezone.utc).timestamp()
    b = datetime.datetime.fromisoformat(hi).replace(tzinfo=datetime.timezone.utc).timestamp()
    print(lo, hi, [x[1] for x in mt if a <= x[0] <= b][:8])
