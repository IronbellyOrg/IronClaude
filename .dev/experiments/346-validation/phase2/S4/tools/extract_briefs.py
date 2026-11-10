"""Extract every Agent / Skill brief of the I4 session verbatim (read-only on ~/.claude).

Writes into <out>/briefs/:
  one file per Agent call:   <stage>_L<jsonl line>.md   (content = the prompt string exactly as in the log)
  one file per task-file line referenced by those prompts: taskfile-L<n>_embedded-prompt.md
      (text between 'BEGIN AGENT PROMPT.' and 'END AGENT PROMPT.' of that line in the task file state that was live
       during the run: file-history 32d05845d5285d52@v2)
  INDEX.md (table with sha256 per file)
Usage: uv run --no-project python -I extract_briefs.py <out_dir>
"""
import hashlib
import json
import os
import re
import sys

ROOT = "/home/coder/.claude/projects/-home-coder-workspaces-worktrees-Coder-bmad-ponytail-global"
MAIN = ROOT + "/189f8649-3921-4435-bc6b-a15182a20399.jsonl"
TASKV2 = "/home/coder/.claude/file-history/189f8649-3921-4435-bc6b-a15182a20399/32d05845d5285d52@v2"
out = os.path.join(sys.argv[1], "briefs")
os.makedirs(out, exist_ok=True)


def stage_of(desc):
    d = desc
    m = re.match(r"Research agent (\d+)", d)
    if m:
        return f"W1-research-{m.group(1)}"
    m = re.match(r"Web research (web-\d+)", d)
    if m:
        return f"W2-{m.group(1)}"
    m = re.match(r"Synthesis agent (synth-\d+)", d)
    if m:
        return f"W3-{m.group(1)}"
    if d.startswith("Assemble final research report"):
        return "W4-assemble-report"
    if d.startswith("Compile Gate 1 gaps log"):
        return "G1-X-gaps-log"
    if d.startswith("Final validation"):
        return "Z-final-validation"
    m = re.match(r"Consolidate Gate (\d) ", d)
    if m:
        return f"G{m.group(1)}-C1-consolidate"
    m = re.match(r"Gate (\d) fix agent cycle (\d)", d)
    if m:
        return f"G{m.group(1)}-F{m.group(2)}-fix"
    m = re.match(r"Gate (\d) verification (structural|qualitative) c(\d)", d)
    if m:
        return f"G{m.group(1)}-R{int(m.group(3)) + 1}-verify-{m.group(2)}"
    m = re.match(r"Gate (\d) (.*)", d)
    if m:
        slug = re.sub(r"[^a-z0-9]+", "-", m.group(2).lower()).strip("-")
        return f"G{m.group(1)}-R1-{slug}"
    return re.sub(r"[^a-z0-9]+", "-", d.lower()).strip("-")


uses, calls, agent_ids, seen_ids = {}, [], {}, set()  # the log repeats each tool_use in a later line; keep the first
with open(MAIN, encoding="utf-8") as fh:
    for ln, line in enumerate(fh, 1):
        o = json.loads(line)
        content = (o.get("message") or {}).get("content")
        if not isinstance(content, list):
            continue
        for c in content:
            if c.get("type") == "tool_use" and c.get("name") in ("Agent", "Skill") and c["id"] not in seen_ids:
                seen_ids.add(c["id"])
                calls.append((ln, o.get("timestamp", "????-??-??T??:??:??"), c["name"], c["input"], c["id"]))
            elif c.get("type") == "tool_result":
                t = o.get("toolUseResult")
                if isinstance(t, dict) and t.get("agentId"):
                    agent_ids[c["tool_use_id"]] = t["agentId"]

rows = []
task_lines = {}
for ln, ts, name, inp, tid in calls:
    if name == "Skill":
        body = json.dumps(inp, ensure_ascii=False, indent=1)
        fn = f"S-skill-{inp.get('skill')}_L{ln}.json"
        open(os.path.join(out, fn), "w", encoding="utf-8").write(body)
        rows.append((fn, ln, ts[11:19], "Skill", inp.get("skill"), "", "", hashlib.sha256(body.encode()).hexdigest()[:12]))
        continue
    prompt = inp["prompt"]
    stage = stage_of(inp.get("description", ""))
    fn = f"{stage}_L{ln}.md"
    open(os.path.join(out, fn), "w", encoding="utf-8").write(prompt)
    m = re.search(r"offset=(\d+)", prompt)
    tl = m.group(1) if m else ""
    if tl:
        task_lines.setdefault(int(tl), []).append(stage)
    rows.append((fn, ln, ts[11:19], inp.get("subagent_type", ""), inp.get("description", ""), agent_ids.get(tid, ""), tl, hashlib.sha256(prompt.encode()).hexdigest()[:12]))

v2 = open(TASKV2, encoding="utf-8").read().split("\n")
emb_rows = []
for n in sorted(task_lines):
    text = v2[n - 1]
    m = re.search(r"BEGIN AGENT PROMPT\.(.*?)END AGENT PROMPT\.", text, re.S)
    if not m:  # step text without an embedded agent prompt: keep the whole line
        fn = f"taskfile-L{n}_step-text-full-line.md"
        open(os.path.join(out, fn), "w", encoding="utf-8").write(text)
        emb_rows.append((n, fn, hashlib.sha256(text.encode()).hexdigest()[:12]))
        continue
    fn = f"taskfile-L{n}_embedded-prompt.md"
    body = m.group(1).strip("\n") if False else m.group(1)
    open(os.path.join(out, fn), "w", encoding="utf-8").write(body)
    emb_rows.append((n, fn, hashlib.sha256(body.encode()).hexdigest()[:12]))

with open(os.path.join(out, "INDEX.md"), "w", encoding="utf-8") as fh:
    fh.write("# briefs/INDEX.md\n\nEvery file below is the prompt string of one Agent/Skill call, byte for byte as stored in the session log.\n")
    fh.write("`L` = 1-based jsonl line in the main session log (BM). The agent's own log: `<BM folder>/subagents/agent-<agentId>.jsonl`.\n")
    fh.write("`taskfile line` = the line of the task file that the wrapper tells the agent to read (the real, long brief).\n\n")
    fh.write("| file | L | time (UTC) | subagent_type | description | agentId | task-file line | sha256[:12] |\n|---|---|---|---|---|---|---|---|\n")
    for r in rows:
        fh.write("| " + " | ".join(str(x) for x in r) + " |\n")
    fh.write("\n## Embedded prompts (text between `BEGIN AGENT PROMPT.` and `END AGENT PROMPT.` on that task-file line, task file state `32d05845d5285d52@v2`)\n\n")
    fh.write("| task-file line | file | used by | sha256[:12] |\n|---|---|---|---|\n")
    for n, fn, h in emb_rows:
        fh.write(f"| {n} | {fn} | {', '.join(task_lines[n])} | {h} |\n")
print(len(rows), "calls;", len(emb_rows), "embedded prompts;", sum(1 for e in emb_rows if e[1] == 'NO MARKERS'), "without markers")
