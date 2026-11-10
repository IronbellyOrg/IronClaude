"""List distinct file paths the four final reviewers touched through Read/Grep/Glob and Bash path tokens."""
import json
import re
import sys
from collections import Counter
from pathlib import Path

SD = Path(sys.argv[1])
REV = {1: "a0d4eb0d0b16b7e1f", 2: "ad1d95b612f2d9bd6", 3: "a88ad232bf783d3a3", 4: "a40f02e69785bb0f5"}
PKG = "TASK-WF-writeTheP0LivePl-20261103-215902"
paths = {}
rx = re.compile(r"(/home/coder/[^\s\"'`<>|;)\\]+)")
for k, aid in REV.items():
    for ln in (SD / f"agent-{aid}.jsonl").read_text(encoding="utf-8").splitlines():
        r = json.loads(ln)
        if r.get("type") != "assistant":
            continue
        c = r.get("message", {}).get("content")
        if not isinstance(c, list):
            continue
        for b in c:
            if b.get("type") != "tool_use":
                continue
            inp = b["input"]
            cand = []
            if b["name"] == "Read":
                cand.append(inp.get("file_path", ""))
            elif b["name"] in ("Grep", "Glob"):
                cand.append(inp.get("path", ""))
            elif b["name"] == "Bash":
                cand += rx.findall(inp.get("command", ""))
            for p in cand:
                p = p.rstrip(".,:")
                if p:
                    paths.setdefault(p, set()).add(k)
# group: outside package & outside ~/.claude/projects worker trees
out = {}
for p, ks in paths.items():
    if PKG in p or "/tmp/" in p:
        continue
    if "/.claude/projects/" in p:
        key = "SESSION:" + re.sub(r"(/\.claude/projects/[^/]+)/.*", r"\1", p)
    else:
        key = p
    out.setdefault(key, set()).update(ks)
for p in sorted(out):
    print(sorted(out[p]), p)
