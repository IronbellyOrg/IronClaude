"""Census of file-mutating tool calls in the I4 session log and its subagent logs.

Read-only on ~/.claude. Output: one TSV line per mutating tool call:
  source  line  ts  tool  ok  path_or_cmd_hint
Usage: uv run python -I census.py > census.tsv
"""
import glob
import json
import os
import re
import sys

ROOT = "/home/coder/.claude/projects/-home-coder-workspaces-worktrees-Coder-bmad-ponytail-global"
MAIN = ROOT + "/189f8649-3921-4435-bc6b-a15182a20399.jsonl"
SUB = ROOT + "/189f8649-3921-4435-bc6b-a15182a20399/subagents"
MUT = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
BASH_WRITE = re.compile(r"(sed\s+-i|>>|\btee\b|\bcat\s*>|\bmv\b|\bcp\b|\bpython3?\b|\bperl\b|\bsponge\b|\bgit\s+(checkout|restore|add|stash))")


def scan(path, label):
    uses = {}
    with open(path, encoding="utf-8") as fh:
        for ln, line in enumerate(fh, 1):
            try:
                o = json.loads(line)
            except Exception:
                continue
            msg = o.get("message") or {}
            content = msg.get("content")
            if not isinstance(content, list):
                continue
            for c in content:
                if c.get("type") == "tool_use":
                    uses[c["id"]] = (ln, o.get("timestamp", ""), c["name"], c.get("input", {}))
                elif c.get("type") == "tool_result":
                    u = uses.get(c.get("tool_use_id"))
                    if not u:
                        continue
                    ln0, ts, name, inp = u
                    err = bool(c.get("is_error"))
                    if name in MUT:
                        hint = inp.get("file_path") or inp.get("notebook_path") or ""
                        print(f"{label}\t{ln0}\t{ts[11:19]}\t{name}\t{'ERR' if err else 'ok'}\t{hint}")
                    elif name == "Bash":
                        cmd = inp.get("command", "")
                        if "TASK-RESEARCH-bmad-first-use" in cmd and BASH_WRITE.search(cmd):
                            print(f"{label}\t{ln0}\t{ts[11:19]}\tBash\t{'ERR' if err else 'ok'}\t{cmd[:160].replace(chr(10), ' ')}")


scan(MAIN, "main")
for p in sorted(glob.glob(SUB + "/agent-*.jsonl")):
    scan(p, os.path.basename(p)[6:-6])
