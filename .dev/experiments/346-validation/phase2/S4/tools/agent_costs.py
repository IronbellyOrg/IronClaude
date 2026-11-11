"""Per-agent cost of the I4 run: tool calls, tokens, wall time. Read-only on ~/.claude.

Reads briefs/INDEX.md (stage name, agentId) and each subagent log. Token numbers are the `usage` fields of the
assistant messages, counted once per message id (the logs repeat a message once per content block).
Agents that a spawned agent started itself (the fix agents start gap researchers) are listed as extra rows named
<stage>-nested-<agentId>_L<parent line>.md so the round total includes them.
Output: TSV on stdout:  stage  L  agentId  tool_calls  assistant_msgs  in_tok  cache_create  cache_read  out_tok  first_ts  last_ts  secs
Usage: uv run --no-project python -I agent_costs.py <S4 folder>
"""
import json
import os
import re
import sys
from datetime import datetime

S4 = sys.argv[1]
SUB = "/home/coder/.claude/projects/-home-coder-workspaces-worktrees-Coder-bmad-ponytail-global/189f8649-3921-4435-bc6b-a15182a20399/subagents"
rows = []
for line in open(os.path.join(S4, "briefs", "INDEX.md"), encoding="utf-8"):
    m = re.match(r"\| ([^|]+\.md) \| (\d+) \| ([0-9:]+) \| ([^|]*) \| ([^|]*) \| (a[0-9a-f]+) \|", line)
    if m:
        rows.append((m.group(1).strip(), int(m.group(2)), m.group(6)))


def stats(path):
    tools, msgs, nested = set(), {}, []
    first = last = None
    for line in open(path, encoding="utf-8"):
        try:
            o = json.loads(line)
        except Exception:
            continue
        ts = o.get("timestamp")
        if ts:
            first = first or ts
            last = ts
        msg = o.get("message") or {}
        t = o.get("toolUseResult")
        if o.get("type") == "user" and isinstance(t, dict) and t.get("agentId") and t["agentId"] not in nested:
            nested.append(t["agentId"])
        if o.get("type") == "assistant":
            for c in msg.get("content") or []:
                if isinstance(c, dict) and c.get("type") == "tool_use":
                    tools.add(c["id"])
            u = msg.get("usage")
            if u and msg.get("id"):
                prev = msgs.get(msg["id"], (0, 0, 0, 0))
                cur = (u.get("input_tokens", 0), u.get("cache_creation_input_tokens", 0), u.get("cache_read_input_tokens", 0), u.get("output_tokens", 0))
                msgs[msg["id"]] = tuple(max(a, b) for a, b in zip(prev, cur))
    tot = [sum(v[i] for v in msgs.values()) for i in range(4)]
    secs = ""
    if first and last:
        f = datetime.fromisoformat(first.replace("Z", "+00:00"))
        l = datetime.fromisoformat(last.replace("Z", "+00:00"))
        secs = int((l - f).total_seconds())
    return len(tools), len(msgs), tot, (first or "")[11:19], (last or "")[11:19], secs, nested


def emit(fn, ln, aid, s):
    nt, nm, tot, f, l, secs, _ = s
    print(f"{fn}\t{ln}\t{aid}\t{nt}\t{nm}\t{tot[0]}\t{tot[1]}\t{tot[2]}\t{tot[3]}\t{f}\t{l}\t{secs}")


print("stage_file\tL\tagentId\ttool_calls\tassistant_msgs\tin_tok\tcache_create\tcache_read\tout_tok\tfirst_ts\tlast_ts\tsecs")
for fn, ln, aid in rows:
    path = f"{SUB}/agent-{aid}.jsonl"
    if not os.path.exists(path):
        print(f"{fn}\t{ln}\t{aid}\tMISSING")
        continue
    s = stats(path)
    emit(fn, ln, aid, s)
    stage = fn.split("_L")[0]
    for nid in s[6]:
        npath = f"{SUB}/agent-{nid}.jsonl"
        if os.path.exists(npath):
            emit(f"{stage}-nested-{nid}_L{ln}.md", ln, nid, stats(npath))
        else:
            print(f"{stage}-nested-{nid}_L{ln}.md\t{ln}\t{nid}\tMISSING")
