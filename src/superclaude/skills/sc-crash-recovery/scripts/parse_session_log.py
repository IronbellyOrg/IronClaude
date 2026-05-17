#!/usr/bin/env python3
"""parse_session_log.py — extract the most recent user prompts, assistant text,
and tool-call summaries from a Claude Code session JSONL.

Usage: parse_session_log.py <session.jsonl> [--turns N] [--max-chars N]

Output: compact JSON with the last N turns (default 6), each containing role,
text snippet (truncated), and last tool calls. Designed to feed a subagent or
the orchestrator without dumping the full log.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("path", type=Path)
    ap.add_argument("--turns", type=int, default=6)
    ap.add_argument("--max-chars", type=int, default=600)
    args = ap.parse_args()

    if not args.path.exists():
        print(json.dumps({"error": "not_found", "path": str(args.path)}))
        return 2

    events = []
    with args.path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    # Keep only real user/assistant message events. Drop file-history-snapshot,
    # meta-tagged caveats, sidechains, and tool-result echoes.
    turns = []
    for ev in events:
        if ev.get("isMeta"):
            continue
        if ev.get("isSidechain"):
            continue
        if ev.get("type") == "file-history-snapshot":
            continue
        msg = ev.get("message", {})
        role = msg.get("role") or ev.get("type")
        if role not in ("user", "assistant"):
            continue
        content = msg.get("content", "")
        text_parts, tool_calls = [], []
        if isinstance(content, str):
            text_parts.append(content)
        elif isinstance(content, list):
            for block in content:
                if not isinstance(block, dict):
                    continue
                btype = block.get("type")
                if btype == "text":
                    text_parts.append(block.get("text", ""))
                elif btype == "tool_use":
                    tool_calls.append({
                        "name": block.get("name", ""),
                        "input_summary": _summarize_input(block.get("input", {})),
                    })
                elif btype == "tool_result":
                    # Skip — too noisy. The triggering tool_use already captured it.
                    pass
        text = "\n".join(p for p in text_parts if p).strip()
        if not text and not tool_calls:
            continue
        # Filter out the system-reminder-only and caveat-only user turns.
        if role == "user" and text.startswith(("<local-command-caveat>", "<system-reminder>")):
            continue
        turns.append({
            "role": role,
            "ts": ev.get("timestamp", ""),
            "text": text[: args.max_chars] + (" […truncated]" if len(text) > args.max_chars else ""),
            "tool_calls": tool_calls[:5],
        })

    last = turns[-args.turns :]
    out = {
        "session_file": str(args.path),
        "total_events": len(events),
        "turn_count": len(turns),
        "returned_turns": len(last),
        "turns": last,
    }
    print(json.dumps(out, indent=2))
    return 0


def _summarize_input(inp: dict) -> str:
    if not isinstance(inp, dict):
        return ""
    # Prefer common signal fields, in priority order.
    for key in ("file_path", "command", "description", "prompt", "query", "path", "url"):
        v = inp.get(key)
        if isinstance(v, str) and v:
            return f"{key}={v[:120]}"
    keys = list(inp.keys())[:3]
    return f"keys={keys}"


if __name__ == "__main__":
    sys.exit(main())
