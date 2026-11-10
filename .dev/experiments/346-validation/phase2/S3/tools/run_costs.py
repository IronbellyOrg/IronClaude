"""M5 for any run: per-subagent cost from a session's subagent logs (read-only).

Usage: uv run python -I run_costs.py <subagents_dir> [description-substring ...]
Prints one JSON line per agent (sorted by start time): agent id, description (from the .meta.json),
model, unique API messages, unique tool calls, wall seconds and output tokens.
Counts are de-duplicated by message id / tool_use id because the logs repeat records.
Cache tokens are omitted on purpose: compare output_tokens, api_messages and tool_calls.
"""
import json
import sys
from datetime import datetime
from pathlib import Path

d = Path(sys.argv[1])
want = sys.argv[2:]
rows = []
for log in sorted(d.glob("agent-*.jsonl")):
    meta = {}
    mp = log.with_suffix(".meta.json")
    if mp.exists():
        meta = json.loads(mp.read_text())
    if want and not any(w in meta.get("description", "") for w in want):
        continue
    msgs, tools, ts, model = {}, set(), [], None
    for line in log.open(encoding="utf-8"):
        rec = json.loads(line)
        if rec.get("timestamp"):
            ts.append(rec["timestamp"])
        m = rec.get("message") or {}
        if rec.get("type") == "assistant" and m.get("id"):
            msgs[m["id"]] = m.get("usage") or {}
            model = m.get("model") or model
            tools.update(b["id"] for b in (m.get("content") or []) if b.get("type") == "tool_use")
    if not ts:
        continue
    f = lambda s: datetime.fromisoformat(s.replace("Z", "+00:00"))
    rows.append({"agent": log.stem[6:], "description": meta.get("description"), "model": model,
                 "api_messages": len(msgs), "tool_calls": len(tools),
                 "start": ts[0], "wall_seconds": int((f(ts[-1]) - f(ts[0])).total_seconds()),
                 "output_tokens": sum(int(u.get("output_tokens") or 0) for u in msgs.values())})
for r in sorted(rows, key=lambda r: r["start"]):
    print(json.dumps(r))
