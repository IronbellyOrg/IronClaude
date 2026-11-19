#!/usr/bin/env python3
"""Find every Claude Code agent session in Orca and extract what it did since the previous report (FR-27).

usage: sessions.py <run_folder>

Orca is used only to find which transcript belongs to which terminal and whether that terminal still exists.
What Orca itself says about a session's state is never used: status is decided by the model from these facts.

Match (VERIFIED live 2026-10-30, 15 of 18 terminals; the other 3 ran no Claude):
  `orca terminal list` -> each pane key "tabId:leafId" -> Orca's agent hook file
  ~/.config/orca/agent-hooks/last-status.json (format version 2) -> Claude session id and transcript path.
  Fallback: the `claude` process whose environment carries ORCA_TERMINAL_HANDLE, its CLAUDE_TOPIC (ccsession
  tag) and the tag file that holds the session id.
Extract (from the transcript bytes after the previous report's read position; first report: the last 24 hours,
read from at most the last 30 MB): prompts given, assistant replies, tools used, files written, git and gh
commands, errors, repeated steps, the last event and its time, whether the session ends on a question or on a
tool call with no result, and every GitHub, ClickUp or Orca item URL it names.
Terminals in the coordinator's own workspace are skipped (the report would describe itself).
Writes sessions.json and sessions-status.json into the run folder.
"""

import glob
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

import orca_term
from common import (
    ITEM_URL,
    CommandError,
    read_json,
    session_statuses,
    workspace_path,
    write_json,
)

HOOK_FILE = Path(
    os.environ.get(
        "AWR_HOOK_FILE", Path.home() / ".config/orca/agent-hooks/last-status.json"
    )
)
PROJECTS = Path(os.environ.get("AWR_PROJECTS", Path.home() / ".claude/projects"))
FIRST_WINDOW_HOURS = 24
FIRST_READ_BYTES = 30_000_000
WRITE_TOOLS = {"Write", "Edit", "NotebookEdit", "MultiEdit"}
GIT_CMD = re.compile(
    r"\b(git (commit|push|merge|checkout -b|switch -c|branch)|gh (pr|issue|release) \w+)"
)
FINAL_TEXT = 600
QUESTION_TAIL = 400
EMPTY = {
    "events": 0,
    "first_event": None,
    "last_event": None,
    "prompts": [],
    "replies": [],
    "tools": {},
    "files_written": [],
    "commands": [],
    "errors": [],
    "error_count": 0,
    "repeated_steps": [],
    "ends_on_question": False,
    "last_turn": None,
    "pending_tool_call": None,
    "prompt_urls": [],
    "item_urls": [],
    "title": None,
}


def previous_reads(run):
    """({session id: record} from the latest completed report that read sessions, {session id: status} from
    that report and every later one, newest first). A report that could not read sessions loses nothing."""
    done = sorted(
        p
        for p in run.parent.iterdir()
        if p != run
        and (p / "complete.json").exists()
        and read_json(p / "complete.json", {}).get("kind") != "hourly"
    )
    statuses = {}
    for p in reversed(done):
        text = (p / "overview.md").read_text() if (p / "overview.md").exists() else ""
        for sid, st in session_statuses(text).items():
            statuses.setdefault(sid, st)
        if read_json(p / "sessions-status.json", {}).get("read"):
            return {
                s["session_id"]: s for s in read_json(p / "sessions.json", [])
            }, statuses
    return {}, statuses


claude_processes = orca_term.claude_processes


def find_transcript(session_id, hinted):
    if hinted and Path(hinted).exists():
        return Path(hinted)
    hits = glob.glob(str(PROJECTS / "*" / f"{session_id}.jsonl"))
    return Path(hits[0]) if hits else None


def tag_session(tag):
    for f in glob.glob(str(PROJECTS / "*" / "topics" / f"{tag}.txt")):
        sid = Path(f).read_text().strip()
        if sid:
            return sid
    return None


def git_repo(path):
    try:
        url = subprocess.run(
            ["git", "-C", path, "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            timeout=10,
        ).stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        return None
    m = re.search(r"github\.com[:/]([\w.-]+/[\w.-]+?)(?:\.git)?$", url)
    return m.group(1) if m else None


def text_of(content):
    if isinstance(content, str):
        return content
    return "\n".join(
        b.get("text", "")
        for b in content or []
        if isinstance(b, dict) and b.get("type") == "text"
    )


def extract(path, start, first_report):
    """Facts from the transcript bytes after `start`. Returns (facts, end offset)."""
    size = path.stat().st_size
    if start is None or start > size:
        start = max(0, size - FIRST_READ_BYTES)
        skip_partial = start > 0
    else:
        skip_partial = False
    cutoff = (
        (datetime.now(timezone.utc) - timedelta(hours=FIRST_WINDOW_HOURS)).isoformat()
        if first_report
        else ""
    )
    facts = {
        "prompts": [],
        "replies": [],
        "tools": Counter(),
        "files_written": set(),
        "commands": [],
        "errors": [],
        "events": 0,
        "first_event": None,
        "last_event": None,
        "urls": set(),
        "prompt_urls": set(),
        "titles": [],
    }
    pending, calls, last_role = {}, Counter(), None
    with open(path, "rb") as f:
        f.seek(start)
        if skip_partial:
            f.readline()
        end = f.tell()
        for raw in f:
            if not raw.endswith(b"\n"):
                break  # a line Claude is still writing: leave it for the next read
            end += len(raw)
            try:
                d = json.loads(raw)
            except ValueError:
                continue
            kind = d.get("type")
            if kind in ("ai-title", "custom-title"):
                facts["titles"].append(d.get("customTitle") or d.get("aiTitle"))
            if kind not in ("user", "assistant") or d.get("isSidechain"):
                continue
            ts = d.get("timestamp") or ""
            if ts < cutoff:
                continue
            facts["events"] += 1
            facts["first_event"] = facts["first_event"] or ts
            facts["last_event"] = ts
            content = (d.get("message") or {}).get("content")
            if kind == "user":
                results = (
                    [
                        b
                        for b in content or []
                        if isinstance(b, dict) and b.get("type") == "tool_result"
                    ]
                    if isinstance(content, list)
                    else []
                )
                for r in results:
                    pending.pop(r.get("tool_use_id"), None)
                    if r.get("is_error"):
                        facts["errors"].append(
                            text_of(r.get("content"))[:300]
                            if isinstance(r.get("content"), list)
                            else str(r.get("content"))[:300]
                        )
                prompt = text_of(content).strip()
                if (
                    prompt
                    and not results
                    and not d.get("isMeta")
                    and not d.get("isCompactSummary")
                    and not prompt.startswith("<")
                ):
                    facts["prompts"].append({"time": ts, "text": prompt[:800]})
                    last_role = "user"
                    facts["prompt_urls"] |= set(re.findall(ITEM_URL, prompt))
                continue
            for b in content or []:
                if not isinstance(b, dict):
                    continue
                if b.get("type") == "text" and b.get("text", "").strip():
                    facts["replies"].append(
                        {"time": ts, "text": b["text"].strip()[-FINAL_TEXT:]}
                    )
                    facts["urls"] |= set(re.findall(ITEM_URL, b["text"]))
                    last_role = "assistant"
                elif b.get("type") == "tool_use":
                    name, inp = b.get("name", ""), b.get("input") or {}
                    facts["tools"][name] += 1
                    pending[b.get("id")] = {"time": ts, "tool": name}
                    calls[(name, json.dumps(inp, sort_keys=True)[:500])] += 1
                    if name in WRITE_TOOLS and inp.get("file_path"):
                        facts["files_written"].add(inp["file_path"])
                    cmd = str(inp.get("command", ""))
                    if GIT_CMD.search(cmd):
                        facts["commands"].append(cmd[:200])
                    facts["urls"] |= set(re.findall(ITEM_URL, json.dumps(inp)))
                    last_role = "tool"
    last_reply = facts["replies"][-1]["text"] if facts["replies"] else ""
    return {
        "events": facts["events"],
        "first_event": facts["first_event"],
        "last_event": facts["last_event"],
        "prompts": facts["prompts"][-10:],
        "replies": facts["replies"][-5:],
        "tools": dict(facts["tools"].most_common(15)),
        "files_written": sorted(facts["files_written"])[:50],
        "commands": facts["commands"][-20:],
        "errors": facts["errors"][-5:],
        "error_count": len(facts["errors"]),
        "repeated_steps": [
            {"tool": k[0], "times": n} for k, n in calls.items() if n >= 3
        ][:10],
        # A reply that asks often ends on a plan or a table after its question, so any "?" in its last
        # paragraphs counts; whether the reply asks something without one is the model's judgment.
        "ends_on_question": last_role == "assistant"
        and "?" in last_reply[-QUESTION_TAIL:],
        # reply: it stopped on its own message to Clay; tool: on a tool call; prompt: on Clay's message.
        "last_turn": {"assistant": "reply", "tool": "tool", "user": "prompt"}.get(
            last_role
        ),
        "pending_tool_call": list(pending.values())[-1]
        if last_role == "tool" and pending
        else None,
        # Items named in what the session was asked (prompts) match it to an item; ones it only looked at do not.
        "prompt_urls": sorted(facts["prompt_urls"]),
        "item_urls": sorted(facts["urls"] | facts["prompt_urls"]),
        "title": (facts["titles"] or [None])[-1],
    }, end


def main(run):
    run = Path(run)
    status = {"read": False}
    hook = read_json(HOOK_FILE, None)
    if not hook or hook.get("version") != 2:
        status["reason"] = (
            f"Orca's agent hook file is missing or not format version 2 ({HOOK_FILE})"
        )
        write_json(run / "sessions-status.json", status)
        write_json(run / "sessions.json", [])
        print(f"sessions not read: {status['reason']}")
        return
    try:
        res = orca_term.orca("terminal", "list")
    except CommandError as e:
        write_json(
            run / "sessions-status.json",
            {"read": False, "reason": f"orca terminal list failed: {e}"},
        )
        write_json(run / "sessions.json", [])
        print("sessions not read: orca terminal list failed")
        return
    if res.get("truncated"):
        write_json(
            run / "sessions-status.json",
            {"read": False, "reason": "orca terminal list was cut short"},
        )
        write_json(run / "sessions.json", [])
        return
    prev, statuses = previous_reads(run)
    try:
        worktrees = {
            w["path"]: w
            for w in (orca_term.orca("worktree", "list").get("worktrees") or [])
        }
    except CommandError as e:
        worktrees, missing_links = (
            {},
            f"orca worktree list failed, so no session is joined by its Orca link: {e}",
        )
    else:
        missing_links = None
    procs = claude_processes()
    entries = hook.get("entries", {})
    sessions, missing, unused = [], [], []
    for t in res["terminals"]:
        path = t.get("worktreePath") or ""
        if not path or path == workspace_path():
            continue
        e = entries.get(f"{t.get('tabId')}:{t.get('leafId')}")
        sid = ((e or {}).get("providerSession") or {}).get("id")
        hinted = ((e or {}).get("providerSession") or {}).get("transcriptPath")
        tag = procs.get(t["handle"], "")
        if not sid and tag:
            sid = tag_session(tag)
        if not sid:
            continue  # a plain shell, or a terminal with no Claude session
        transcript = find_transcript(sid, hinted)
        if not transcript:
            # Claude writes no transcript until its first prompt, so a session that only started is not work yet.
            if not (e or {}).get("hasExplicitPrompt"):
                unused.append(t.get("title") or t["handle"])
            else:
                missing.append(
                    f"{t.get('title') or t['handle']}: transcript for session {sid} not found"
                )
            continue
        old = prev.get(sid, {})
        facts, end = extract(transcript, old.get("read_offset"), first_report=not old)
        wt = worktrees.get(path, {})
        sessions.append(
            {
                "session_id": sid,
                "handle": t["handle"],
                "terminal_title": t.get("title"),
                "tag": tag or None,
                # Named by its ccsession tag or Claude's own title, never Orca's terminal title (FR-28).
                "title": (
                    tag
                    or facts["title"]
                    or old.get("title")
                    or (
                        " ".join(facts["prompts"][0]["text"].split())[:80]
                        if facts["prompts"]
                        else f"session {sid[:8]}"
                    )
                ),
                "worktree": path,
                "branch": (t.get("branch") or "").replace("refs/heads/", ""),
                "repo": git_repo(path),
                "linked_issue": wt.get("linkedIssue"),
                "linked_pr": wt.get("linkedPR"),
                "terminal_open": bool(t.get("connected")),
                "claude_running": t["handle"] in procs,
                "transcript": str(transcript),
                "read_offset": end,
                "events_total": old.get("events_total", 0) + facts["events"],
                "since_previous_report": facts,
            }
        )
    # Nothing leaves the report until it is done: a session from an earlier report whose terminal is gone
    # stays, read on from where it was, until a report called it done.
    seen = {s["session_id"] for s in sessions}
    for sid, old in sorted(prev.items()):
        if sid in seen or statuses.get(sid, "").startswith("done"):
            continue
        transcript = Path(old["transcript"])
        facts, end = (
            extract(transcript, old.get("read_offset"), first_report=False)
            if transcript.exists()
            else (dict(EMPTY), old.get("read_offset"))
        )
        sessions.append(
            dict(
                old,
                terminal_open=False,
                claude_running=False,
                handle=None,
                read_offset=end,
                events_total=old.get("events_total", 0) + facts["events"],
                since_previous_report=facts,
            )
        )
    for s in sessions:
        old, facts = prev.get(s["session_id"], {}), s["since_previous_report"]
        s["last_event"] = facts["last_event"] or old.get("last_event")
        # The items a session was asked about in any report so far, so a match by prompt lasts.
        s["prompt_urls_all"] = sorted(
            set(old.get("prompt_urls_all", [])) | set(facts["prompt_urls"])
        )
        if not facts["events"] and old:
            # Nothing new: the session still ends where it did, so a question or open permission still waits.
            was = old["since_previous_report"]
            facts.update(
                ends_on_question=was["ends_on_question"],
                pending_tool_call=was["pending_tool_call"],
                last_turn=was.get("last_turn")
                or (
                    "reply"
                    if was.get("replies")
                    and was["replies"][-1]["time"] == was.get("last_event")
                    else None
                ),
                state_from_earlier=True,
            )
    sessions.sort(key=lambda s: s["session_id"])
    write_json(run / "sessions.json", sessions)
    write_json(
        run / "sessions-status.json",
        {
            "read": True,
            "sessions": len(sessions),
            "missing": missing,
            "started_no_prompt": unused,
            "worktree_links": missing_links or "read",
        },
    )
    active = sum(1 for s in sessions if s["since_previous_report"]["events"])
    print(
        f"{len(sessions)} agent sessions in Orca; {active} did something since the previous report; {len(missing)} transcripts missing"
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
