"""M5 per review round: tool calls, tokens, wall time of each reviewer subagent; executor tool calls in each window."""
import json
import sys
from pathlib import Path

SD = Path(sys.argv[1])  # subagents dir
MAIN = Path(sys.argv[2])
REV = {1: "a0d4eb0d0b16b7e1f", 2: "ad1d95b612f2d9bd6", 3: "a88ad232bf783d3a3", 4: "a40f02e69785bb0f5"}
SPAWN = {1: 2001, 2: 2157, 3: 2342, 4: 2499}
out = {}


def blocks(rec):
    c = rec.get("message", {}).get("content")
    return c if isinstance(c, list) else []


for k, aid in REV.items():
    ids, usage_ids, ts = set(), {}, []
    names = {}
    for ln in (SD / f"agent-{aid}.jsonl").read_text(encoding="utf-8").splitlines():
        r = json.loads(ln)
        if r.get("timestamp"):
            ts.append(r["timestamp"])
        if r.get("type") != "assistant":
            continue
        for b in blocks(r):
            if b.get("type") == "tool_use" and b["id"] not in ids:
                ids.add(b["id"])
                names[b["name"]] = names.get(b["name"], 0) + 1
        mid = r.get("message", {}).get("id")
        u = r.get("message", {}).get("usage")
        if mid and u:
            usage_ids[mid] = u  # last usage record per message id wins
    tot = {"input_tokens": 0, "output_tokens": 0, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0}
    for u in usage_ids.values():
        for key in tot:
            tot[key] += u.get(key, 0) or 0
    out[f"R{k}_reviewer"] = {
        "agent": aid, "tool_calls": len(ids), "tools": names, "api_messages": len(usage_ids),
        "first_ts": min(ts), "last_ts": max(ts), **tot,
    }

main = MAIN.read_text(encoding="utf-8").splitlines()
seen = set()
bounds = [SPAWN[1], SPAWN[2], SPAWN[3], SPAWN[4], 2560]
for k in (1, 2, 3, 4):
    a, b_ = bounds[k - 1], bounds[k]
    ids = set()
    for ln in main[a - 1:b_ - 1]:
        r = json.loads(ln)
        if r.get("type") != "assistant":
            continue
        for b in blocks(r):
            if b.get("type") == "tool_use" and b["id"] not in ids:
                ids.add(b["id"])
    out[f"R{k}_executor_window_L{a}_L{b_ - 1}"] = {"tool_calls": len(ids)}
print(json.dumps(out, indent=1))
