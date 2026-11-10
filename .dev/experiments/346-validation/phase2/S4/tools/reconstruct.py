"""Forward-replay every logged mutation of ONE file of the I4 task folder, to rebuild its state at a chosen time.

Read-only on ~/.claude and on the Coder worktree. Writes only into the sandbox directory given by --sandbox.

How it works
  1. Collects, from the session log and all subagent logs, every successful Write / Edit tool call on the target
     file (target = path relative to the task folder, e.g. research/05-....md), plus Bash heredoc appends
     (`cat >> <path> <<'EOF' ... EOF`) to it. For the final report only, the assembler's `sed -n ... >> report`
     commands are re-run against the sandbox copy of synthesis/ (that is how the report body was built).
  2. Sorts them by timestamp and replays them on a sandbox copy, with the Edit tool's rules
     (unique match unless replace_all; curly-quote fallback; deleting a line when new_string is empty).
  3. Prints size, line count and sha256 prefix at each checkpoint time (HH:MM:SS.mmm, UTC, same clock as the logs).
  Any other Bash command that mentions the file with a write operator is reported as UNHANDLED (not replayed).

Usage:
  uv run --no-project python -I reconstruct.py --target research/05-startup-boot-test-docs-and-decision-trail.md \
      --sandbox /tmp/s4_recon --checkpoint 15:52:19 --out-at 15:52:19=/tmp/x.md
"""
import argparse
import glob
import hashlib
import json
import os
import re
import subprocess

ROOT = "/home/coder/.claude/projects/-home-coder-workspaces-worktrees-Coder-bmad-ponytail-global"
MAIN = ROOT + "/189f8649-3921-4435-bc6b-a15182a20399.jsonl"
SUB = ROOT + "/189f8649-3921-4435-bc6b-a15182a20399/subagents"
REAL_T = "/home/coder/workspaces/worktrees/Coder/bmad-ponytail-global/.dev/tasks/to-do/TASK-RESEARCH-bmad-first-use-20261107-075901"
QUOTES = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"'})
HEREDOC = re.compile(r"cat\s*(>>?)\s*(\S+)\s*<<\s*'(\w+)'\n(.*?)\n\3(?:\n|$)", re.S)


def collect(target):
    full = REAL_T + "/" + target
    base = os.path.basename(target)
    is_report = target == "RESEARCH-REPORT-bmad-first-use.md"
    ev, seen = [], set()  # the logs repeat some tool_result lines; apply each tool call once
    for path in [MAIN] + sorted(glob.glob(SUB + "/agent-*.jsonl")):
        label = "main" if path == MAIN else os.path.basename(path)[6:-6]
        uses = {}
        with open(path, encoding="utf-8") as fh:
            for ln, line in enumerate(fh, 1):
                try:
                    o = json.loads(line)
                except Exception:
                    continue
                content = (o.get("message") or {}).get("content")
                if not isinstance(content, list):
                    continue
                for c in content:
                    if c.get("type") == "tool_use":
                        uses[c["id"]] = (ln, o.get("timestamp", ""), c["name"], c.get("input", {}))
                    elif c.get("type") == "tool_result" and c.get("tool_use_id") in uses and not c.get("is_error"):
                        if c["tool_use_id"] in seen:
                            continue
                        seen.add(c["tool_use_id"])
                        ln0, ts, name, inp = uses[c["tool_use_id"]]
                        if name in ("Edit", "Write") and inp.get("file_path") == full:
                            ev.append((ts, label, ln0, name, inp))
                        elif name == "Bash":
                            cmd = inp.get("command", "")
                            if is_report and label.startswith("a9c6678f") and ('>> "$R"' in cmd or '>> "$S/RESEARCH-REPORT' in cmd):
                                ev.append((ts, label, ln0, "BashSed", inp))
                            elif full in cmd and any(m.group(2) == full for m in HEREDOC.finditer(cmd)):
                                ev.append((ts, label, ln0, "Heredoc", inp))
                            elif base in cmd and re.search(r"(>>?\s*\S*" + re.escape(base) + r"|tee\s.*" + re.escape(base) + r"|sed\s+-i.*" + re.escape(base) + ")", cmd):
                                ev.append((ts, label, ln0, "Unhandled", inp))
    ev.sort(key=lambda e: (e[0], e[2]))
    return ev


def apply_edit(text, old, new, replace_all):
    if old not in text:
        norm_t, norm_o = text.translate(QUOTES), old.translate(QUOTES)
        if norm_o in norm_t:
            i = norm_t.index(norm_o)
            old = text[i:i + len(old)]
        else:
            raise ValueError("old_string not found")
    if new == "" and not old.endswith("\n") and (old + "\n") in text:
        old = old + "\n"
    if replace_all:
        return text.replace(old, new)
    if text.count(old) != 1:
        raise ValueError(f"old_string not unique ({text.count(old)})")
    return text.replace(old, new, 1)


def stat(path):
    if not os.path.exists(path):
        return (0, 0, "absent")
    b = open(path, "rb").read()
    return len(b), b.count(b"\n"), hashlib.sha256(b).hexdigest()[:16]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True)
    ap.add_argument("--sandbox", required=True)
    ap.add_argument("--checkpoint", action="append", default=[])
    ap.add_argument("--out-at", action="append", default=[], help="HH:MM:SS=outpath")
    args = ap.parse_args()
    dst = os.path.join(args.sandbox, args.target)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.exists(dst):
        os.remove(dst)
    outs = sorted(a.split("=", 1) for a in args.out_at)
    cps = sorted(set(args.checkpoint + [o[0] for o in outs]))
    ev = collect(args.target)
    failed = unhandled = ci = 0

    def flush(limit):
        nonlocal ci
        while ci < len(cps) and (limit is None or cps[ci] < limit):
            print(f"CHECKPOINT <{cps[ci]}: size/lines/sha={stat(dst)} failed={failed} unhandled={unhandled}")
            for o in outs:
                if o[0] == cps[ci]:
                    open(o[1], "wb").write(open(dst, "rb").read() if os.path.exists(dst) else b"")
            ci += 1

    for ts, label, ln, name, inp in ev:
        flush(ts[11:23])
        if name == "Write":
            open(dst, "w", encoding="utf-8").write(inp["content"])
        elif name == "Edit":
            txt = open(dst, encoding="utf-8").read()
            try:
                open(dst, "w", encoding="utf-8").write(apply_edit(txt, inp["old_string"], inp["new_string"], bool(inp.get("replace_all"))))
            except ValueError as e:
                failed += 1
                print(f"EDIT FAILED {label} L{ln} {ts[11:23]}: {e}")
        elif name == "Heredoc":
            for m in HEREDOC.finditer(inp["command"]):
                if m.group(2) == REAL_T + "/" + args.target:
                    mode = "a" if m.group(1) == ">>" else "w"
                    with open(dst, mode, encoding="utf-8") as fh:
                        fh.write(m.group(4) + "\n")
        elif name == "BashSed":
            cmd = inp["command"].replace(REAL_T, args.sandbox)
            r = subprocess.run(["bash", "-c", cmd], capture_output=True, text=True, timeout=60)
            if r.returncode != 0:
                failed += 1
                print(f"BASH FAILED {label} L{ln}: {r.stderr[:200]}")
        else:
            unhandled += 1
            print(f"UNHANDLED BASH {label} L{ln} {ts[11:23]}: {inp['command'][:160]!r}")
    flush(None)
    print("FINAL", stat(dst), "events", len(ev), "failed", failed, "unhandled", unhandled)


if __name__ == "__main__":
    main()
