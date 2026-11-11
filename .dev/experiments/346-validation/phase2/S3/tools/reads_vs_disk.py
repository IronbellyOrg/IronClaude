"""For the six agents of the loop, rebuild every file they Read (from the Read
tool_results in the logs) and compare it with the file as it is on disk today.

Usage: uv run python -I reads_vs_disk.py <subagents_dir> <out_json> [--dump <dir>]
A dump dir receives the as-read text of files whose disk copy is missing or differs.
"""
import json
import re
import sys
from pathlib import Path

SUB = Path(sys.argv[1])
OUT = Path(sys.argv[2])
DUMP = Path(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[3] == "--dump" else None
AGENTS = {
    "a6b78088fe4e8a5aa": "draft", "a13bab688a9d224f8": "review1",
    "a3c8e5c718996e77c": "fix1", "a07f24eaf42c5449e": "review2",
    "a20512cfaf86249a3": "fix2", "a793527cfdd94457c": "review3",
}
row = re.compile(r"^(\d+)\t(.*)$")
report = {}
for agent, role in AGENTS.items():
    reads, results = {}, {}
    seen = set()
    with open(SUB / f"agent-{agent}.jsonl", encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            rec = json.loads(line)
            content = (rec.get("message") or {}).get("content")
            if not isinstance(content, list):
                continue
            for b in content:
                if b.get("type") == "tool_use" and b.get("name") == "Read" and b["id"] not in seen:
                    seen.add(b["id"])
                    reads[b["id"]] = (n, b["input"].get("file_path"))
                elif b.get("type") == "tool_result":
                    c = b.get("content")
                    if isinstance(c, list):
                        c = "".join(x.get("text", "") for x in c)
                    results[b.get("tool_use_id")] = c if isinstance(c, str) else ""
    per_file = {}
    for rid, (n, fp) in reads.items():
        d = per_file.setdefault(fp, {"lines": {}, "log_lines": []})
        d["log_lines"].append(n)
        for ln in results.get(rid, "").split("\n"):
            m = row.match(ln)
            if m:
                d["lines"][int(m.group(1))] = m.group(2)
    out = {}
    for fp, d in per_file.items():
        got = d["lines"]
        # the original worktree is gone; its files survive in the issue-394 worktree
        p = Path(str(fp).replace("/worktrees/IronClaude/hook-launch-level-394/",
                                 "/worktrees/IronClaude/issue-394-launch-level-hook/"))
        entry = {"log_lines": d["log_lines"], "lines_seen": len(got),
                 "max_line": max(got) if got else 0, "disk": "missing"}
        if p.is_file():
            disk = p.read_text(encoding="utf-8", errors="replace").split("\n")
            if disk and disk[-1] == "":
                disk.pop()
            entry["disk_lines"] = len(disk)
            same = all(got[k] == disk[k - 1] for k in got if k <= len(disk))
            full = len(got) >= len(disk) and set(range(1, len(disk) + 1)) <= set(got)
            entry["disk"] = ("identical_full" if same and full else
                             "identical_partial" if same else "DIFFERS")
        if DUMP and entry["disk"] in ("missing", "DIFFERS"):
            DUMP.mkdir(parents=True, exist_ok=True)
            name = fp.strip("/").replace("/", "__")
            (DUMP / f"{agent}__{name}").write_text(
                "\n".join(got[k] for k in sorted(got)) + "\n", encoding="utf-8")
        out[fp] = entry
    report[role] = {"agent": agent, "files": out}
OUT.write_text(json.dumps(report, indent=1))
for role, r in report.items():
    for fp, e in r["files"].items():
        print(f"{role:8} {e['disk']:18} lines_seen={e['lines_seen']:5} {fp.replace('/home/coder/workspaces/worktrees/IronClaude/hook-launch-level-394/.dev/brainstorms/20261105-170229-launch-level-hook/', '<BR>/')}")
