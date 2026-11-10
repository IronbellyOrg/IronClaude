import json, re, sys
from collections import Counter
from pathlib import Path
SD = Path(sys.argv[1]); c = Counter()
rx = re.compile(r"(?<![\w/.-])((?:\.dev|src|docs|tests|plugins)/[A-Za-z0-9_./{},*-]+)")
for aid in ("a0d4eb0d0b16b7e1f","ad1d95b612f2d9bd6","a88ad232bf783d3a3","a40f02e69785bb0f5"):
    for ln in (SD/f"agent-{aid}.jsonl").read_text().splitlines():
        r = json.loads(ln)
        if r.get("type")!="assistant": continue
        for b in (r.get("message",{}).get("content") or []):
            if isinstance(b,dict) and b.get("type")=="tool_use":
                inp=b["input"]; s=" ".join(str(v) for v in inp.values()) if b["name"]!="Bash" else inp.get("command","")
                for m in rx.findall(s):
                    if "TASK-WF-writeTheP0LivePl" in m: continue
                    c[m.rstrip(".,:;")]+=1
for p,n in c.most_common(40): print(n,p)
