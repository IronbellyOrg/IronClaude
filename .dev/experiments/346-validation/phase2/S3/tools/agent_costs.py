"""Per-agent cost of the six loop agents from their session logs (read-only).

Counts unique assistant API messages (by message.id; the log repeats a message
once per content block), unique tool_use ids, wall time, and token usage taken
from the LAST record of each message id. Also checks that the brief handed to
each agent equals the first user message in that agent's own log.

Usage: uv run python -I agent_costs.py <subagents_dir> <briefs_dir>
"""
import hashlib
import json
import sys
from pathlib import Path

SUB, BRIEFS = Path(sys.argv[1]), Path(sys.argv[2])
AGENTS = [
    ("R0_draft", "a6b78088fe4e8a5aa", "R0-writer-draft-plan-L895.md"),
    ("R1_review", "a13bab688a9d224f8", "R1-reviewer-L919.md"),
    ("R1_fix", "a3c8e5c718996e77c", "R1-reviser-fix-cycle-1-L947.md"),
    ("R2_review", "a07f24eaf42c5449e", "R2-reviewer-L975.md"),
    ("R2_fix", "a20512cfaf86249a3", "R2-reviser-fix-cycle-2-L1000.md"),
    ("R3_review", "a793527cfdd94457c", "R3-reviewer-L1032.md"),
]
out = {}
for role, agent, brief in AGENTS:
    msgs, tools, ts, first_user = {}, {}, [], None
    with open(SUB / f"agent-{agent}.jsonl", encoding="utf-8") as fh:
        for line in fh:
            rec = json.loads(line)
            if rec.get("timestamp"):
                ts.append(rec["timestamp"])
            m = rec.get("message") or {}
            if rec.get("type") == "user" and first_user is None and isinstance(m.get("content"), str):
                first_user = m["content"]
            if rec.get("type") == "assistant" and m.get("id"):
                msgs[m["id"]] = m.get("usage") or {}
                model = m.get("model")
                for b in m.get("content") or []:
                    if b.get("type") == "tool_use":
                        tools[b["id"]] = b["name"]
    names = {}
    for n in tools.values():
        names[n] = names.get(n, 0) + 1
    u = lambda k: sum(int(x.get(k) or 0) for x in msgs.values())
    brief_txt = (BRIEFS / brief).read_text(encoding="utf-8")
    out[role] = {
        "agent_id": agent, "model": model, "api_messages": len(msgs),
        "tool_calls": len(tools), "tool_calls_by_name": names,
        "first_ts": ts[0], "last_ts": ts[-1],
        "input_tokens": u("input_tokens"), "output_tokens": u("output_tokens"),
        "cache_read_tokens": u("cache_read_input_tokens"),
        "cache_creation_tokens": u("cache_creation_input_tokens"),
        "brief_equals_first_user_message": first_user == brief_txt,
        "brief_sha256": hashlib.sha256(brief_txt.encode()).hexdigest(),
    }
print(json.dumps(out, indent=1))
