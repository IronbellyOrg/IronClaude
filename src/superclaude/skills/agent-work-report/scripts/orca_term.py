"""Terminal reads, typing and idle checks, and sends with receipts, through the Orca CLI (FR-22, FR-24, FR-25).

Shared by the waker now and by the coordinator and session manager later (FR-26: reused, never copied).
Handles change after an Orca restart, so callers look a terminal up every time and never store one.
"""

import glob
import json
import time
from pathlib import Path

from common import CommandError, run_cmd

FRESH_OUTPUT_SECONDS = 60


def orca(*args, timeout=60):
    out = json.loads(run_cmd(["orca", *args, "--json"], timeout=timeout))
    if not out.get("ok", True):
        raise CommandError(json.dumps(out.get("error") or out)[:500])
    return out.get("result", out)


def terminals(worktree_path):
    """The worktree's terminals. A truncated list could hide one, so it is an error, never a partial answer."""
    res = orca("terminal", "list", "--worktree", f"path:{worktree_path}")
    if res.get("truncated"):
        raise CommandError(
            f"the terminal list was cut short ({res.get('totalCount')} terminals)"
        )
    return [t for t in res["terminals"] if t.get("worktreePath") == worktree_path]


def claude_processes():
    """{ORCA_TERMINAL_HANDLE: CLAUDE_TOPIC or ""} for every running claude process this user can read.

    A terminal's title outlives the Claude that set it (VERIFIED 2026-11-03: a terminal back at the
    ccsession name question still read "coordinator · Claude Code"), so a live session is found by its
    running process, never by its title."""
    found = {}
    for env_path in glob.glob("/proc/[0-9]*/environ"):
        try:
            cmd = Path(env_path).with_name("cmdline").read_bytes().split(b"\0")[0]
            if not cmd.endswith(b"claude"):
                continue
            env = dict(
                kv.split("=", 1)
                for kv in Path(env_path)
                .read_bytes()
                .decode(errors="replace")
                .split("\0")
                if "=" in kv
            )
        except OSError:
            continue
        if env.get("ORCA_TERMINAL_HANDLE"):
            found[env["ORCA_TERMINAL_HANDLE"]] = env.get("CLAUDE_TOPIC", "")
    return found


def find_session(worktree_path, tag):
    """(terminals in the worktree running Claude under ccsession tag `tag`, newest output first;
    terminals in the worktree with no Claude running, which can be reused to start one)."""
    procs = claude_processes()
    terms = [t for t in terminals(worktree_path) if t.get("connected")]
    live = sorted(
        (t for t in terms if procs.get(t["handle"]) == tag),
        key=lambda t: -(t.get("lastOutputAt") or 0),
    )
    return live, [t for t in terms if t["handle"] not in procs]


def find(obj, key):
    """The first value of `key` anywhere in a nested Orca result (result shapes nest under varying keys)."""
    if isinstance(obj, dict):
        if key in obj:
            return obj[key]
        obj = list(obj.values())
    if isinstance(obj, list):
        for v in obj:
            got = find(v, key)
            if got is not None:
                return got
    return None


def screen(handle):
    """The rendered screen: {"tail": [lines], "draft": unsent typing or None}."""
    r = orca("terminal", "read", "--terminal", handle, "--screen")
    t = r.get("terminal", r)
    return {"tail": t.get("tail") or [], "draft": find(r, "draft")}


def is_idle(handle, wait_ms=4000):
    """True when the agent's interface is idle; a timeout or error counts as not idle."""
    try:
        r = orca(
            "terminal",
            "wait",
            "--terminal",
            handle,
            "--for",
            "tui-idle",
            "--timeout-ms",
            str(wait_ms),
            timeout=wait_ms // 1000 + 30,
        )
    except CommandError:
        return False
    return bool(find(r, "satisfied"))


def typing_or_fresh(term):
    """Why it is unsafe to send now, or None. Partial typing is only in `draft` (proof Follow-up 2)."""
    s = screen(term["handle"])
    if (s.get("draft") or "").strip():
        return f"someone is typing ({len(s['draft'])} characters not yet sent)"
    last = (term.get("lastOutputAt") or 0) / 1000
    if last and time.time() - last < FRESH_OUTPUT_SECONDS:
        return f"fresh output {int(time.time() - last)} seconds ago"
    return None


def send(handle, text, enter=True, wait_submit_s=15):
    args = ["terminal", "send", "--terminal", handle, "--text", text]
    if enter:
        args += ["--enter", "--wait-submit", str(wait_submit_s)]
    r = orca(*args, timeout=wait_submit_s + 60)
    return {
        "stages": find(r, "stages") or [],
        "accepted": find(r, "accepted"),
        "raw": r,
    }
