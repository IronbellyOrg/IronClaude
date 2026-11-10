"""Rebuild refactor-plan.md at each review point by replaying the Write and Edit
tool calls recorded in the original session's subagent logs (read-only).

Usage: uv run python -I replay_plan.py <subagents_dir> <out_dir> [final_file_to_compare]
"""
import hashlib
import json
import sys
from pathlib import Path

SUB = Path(sys.argv[1])
OUT = Path(sys.argv[2])
FINAL = Path(sys.argv[3]) if len(sys.argv) > 3 else None
TARGET = "adversarial/adversarial/refactor-plan.md"

# (label, agent log id)
STAGES = [
    ("v0", "a6b78088fe4e8a5aa"),  # draft: Write + 16 Edits -> input of review 1
    ("v1", "a3c8e5c718996e77c"),  # fix cycle 1 -> input of review 2
    ("v2", "a20512cfaf86249a3"),  # fix cycle 2 -> input of review 3
]


def calls(agent_id):
    """Yield (line_no, tool_use, ok) for Write/Edit on the plan, in log order."""
    results = {}
    uses = []
    seen = set()  # the log repeats a tool_use block under the same id; count it once
    with open(SUB / f"agent-{agent_id}.jsonl", encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            rec = json.loads(line)
            content = (rec.get("message") or {}).get("content")
            if not isinstance(content, list):
                continue
            for blk in content:
                if blk.get("type") == "tool_use" and blk.get("name") in ("Write", "Edit"):
                    if str(blk["input"].get("file_path", "")).endswith(TARGET) and blk["id"] not in seen:
                        seen.add(blk["id"])
                        uses.append((n, blk))
                elif blk.get("type") == "tool_result":
                    results[blk.get("tool_use_id")] = bool(blk.get("is_error"))
    for n, blk in uses:
        yield n, blk, not results.get(blk["id"], True)


def sha(b):
    return hashlib.sha256(b).hexdigest()


text = None
OUT.mkdir(parents=True, exist_ok=True)
summary = {}
for label, agent in STAGES:
    applied = skipped = 0
    first = last = None
    for n, blk, ok in calls(agent):
        inp = blk["input"]
        if not ok:
            skipped += 1
            continue
        if blk["name"] == "Write":
            text = inp["content"]
        else:
            old, new = inp["old_string"], inp["new_string"]
            if text is None or old not in text:
                raise SystemExit(f"{label} line {n}: Edit does not apply")
            if inp.get("replace_all"):
                text = text.replace(old, new)
            else:
                if text.count(old) != 1:
                    raise SystemExit(f"{label} line {n}: old_string not unique")
                text = text.replace(old, new, 1)
        applied += 1
        first = first or n
        last = n
    data = text.encode("utf-8")
    (OUT / f"refactor-plan.{label}.md").write_bytes(data)
    summary[label] = {
        "agent": agent, "applied": applied, "skipped_errors": skipped,
        "log_lines": [first, last], "bytes": len(data),
        "lines": data.count(b"\n") + (0 if data.endswith(b"\n") else 1),
        "sha256": sha(data),
    }
if FINAL and FINAL.exists():
    fb = FINAL.read_bytes()
    summary["final_on_disk"] = {"bytes": len(fb), "sha256": sha(fb),
                                "equals_v2": sha(fb) == summary["v2"]["sha256"]}
print(json.dumps(summary, indent=2))
