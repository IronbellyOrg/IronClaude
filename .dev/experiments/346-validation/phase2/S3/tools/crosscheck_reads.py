"""Cross-check a replayed plan version against what a reviewer's own Read calls
returned (independent evidence of the document the reviewer saw).

Usage: uv run python -I crosscheck_reads.py <subagents_dir> <replay_dir>
"""
import json
import re
import sys
from pathlib import Path

SUB = Path(sys.argv[1])
REP = Path(sys.argv[2])
PAIRS = [  # (review, reviewer agent log, replayed version)
    ("review1", "a13bab688a9d224f8", "v0"),
    ("review2", "a07f24eaf42c5449e", "v1"),
    ("review3", "a793527cfdd94457c", "v2"),
]
row = re.compile(r"^(\d+)\t(.*)$")

for name, agent, ver in PAIRS:
    plan_reads = set()
    results = {}
    with open(SUB / f"agent-{agent}.jsonl", encoding="utf-8") as fh:
        for line in fh:
            rec = json.loads(line)
            content = (rec.get("message") or {}).get("content")
            if not isinstance(content, list):
                continue
            for b in content:
                if b.get("type") == "tool_use" and b.get("name") == "Read" and str(
                        b["input"].get("file_path", "")).endswith("adversarial/adversarial/refactor-plan.md"):
                    plan_reads.add(b["id"])
                elif b.get("type") == "tool_result":
                    c = b.get("content")
                    if isinstance(c, list):
                        c = "".join(x.get("text", "") for x in c)
                    results[b.get("tool_use_id")] = c if isinstance(c, str) else ""
    seen = {}
    for rid in plan_reads:
        for ln in results.get(rid, "").split("\n"):
            m = row.match(ln)
            if m:
                seen[int(m.group(1))] = m.group(2)
    rep_lines = (REP / f"refactor-plan.{ver}.md").read_text(encoding="utf-8").split("\n")
    if rep_lines and rep_lines[-1] == "":
        rep_lines.pop()
    last = max(seen) if seen else 0
    mism = [n for n in sorted(seen) if n <= len(rep_lines) and seen[n] != rep_lines[n - 1]]
    extra = [n for n in sorted(seen) if n > len(rep_lines)]
    missing = [n for n in range(1, len(rep_lines) + 1) if n not in seen]
    print(json.dumps({
        "review": name, "version": ver, "reads": len(plan_reads),
        "reviewer_last_line_number": last, "replay_lines": len(rep_lines),
        "mismatched_lines": len(mism), "first_mismatches": mism[:5],
        "reviewer_extra_lines": extra, "lines_never_read": len(missing),
        "extra_line_text": [seen[n] for n in extra],
    }))
