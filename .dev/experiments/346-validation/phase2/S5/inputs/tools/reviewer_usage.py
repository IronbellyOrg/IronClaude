"""M5 for one reviewer subagent log: tool calls, tokens, wall time.

usage: uv run --no-project python -I reviewer_usage.py <agent-log.jsonl>
Same counting rules as the baseline (derivation-scripts/m5.py): tool_use blocks de-duplicated by id; tokens from
message.usage, last record per message id. The log is under ~/.claude/projects/<replay project>/<session>/subagents/.
"""
import json
import sys
from datetime import datetime
from pathlib import Path

ids, usage, ts = set(), {}, []
for ln in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines():
    r = json.loads(ln)
    if r.get("timestamp"):
        ts.append(r["timestamp"])
    if r.get("type") != "assistant":
        continue
    msg = r.get("message", {})
    for b in msg.get("content") or []:
        if isinstance(b, dict) and b.get("type") == "tool_use":
            ids.add(b["id"])
    if msg.get("id") and msg.get("usage"):
        usage[msg["id"]] = msg["usage"]
tot = {k: sum((u.get(k) or 0) for u in usage.values()) for k in
       ("input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")}
fmt = lambda s: datetime.fromisoformat(s.replace("Z", "+00:00"))
mins = round((fmt(max(ts)) - fmt(min(ts))).total_seconds() / 60, 2)
print(json.dumps({"tool_calls": len(ids), "api_messages": len(usage), **tot, "first_ts": min(ts), "last_ts": max(ts), "wall_minutes": mins}))
