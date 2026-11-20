"""Shared helpers for the agent work report scripts.

Everything here is deterministic: the same inputs give the same files. Outputs are
written sorted and without wall-clock values except where a run identifier is the
point (run folders, lock, action log), so two runs on the same data compare cleanly.
"""

import json
import os
import re
import subprocess
import sys
import unicodedata
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

SKILL_DIR = Path(__file__).resolve().parent.parent
CONFIG = json.loads((SKILL_DIR / "config.json").read_text())


# The poll's own configuration file (IronClaude `superclaude issue-watch`): its key `orchestrator_repo`
# is the one place that holds the absolute path of the orchestrator repo (spec 4.4). This skill runs from
# `~/.claude/skills/agent-work-report/`, so the folder it sits in says nothing about where its state lives.
POLL_CONFIG = "~/.config/superclaude/issue-watch.json"


def repo_root():
    """The orchestrator repo that holds `.dev/coordinator/`: `$AWR_ROOT` when set (tests, a second host),
    else `orchestrator_repo` of the poll's configuration file, which must hold a `repos.yaml`.

    `repos.yaml` itself cannot say where its own repo is, so the path comes from the poll configuration and
    `repos.yaml` is only checked to be there. No YAML is read here: the installed scripts run under the
    system `python3`, which need not have PyYAML."""
    env = os.environ.get("AWR_ROOT")
    if env:
        return Path(env)
    path = Path(POLL_CONFIG).expanduser()
    try:
        repo = Path(json.loads(path.read_text())["orchestrator_repo"]).expanduser()
    except (OSError, ValueError, KeyError, TypeError):
        raise SystemExit(
            "the orchestrator repo is unknown: set AWR_ROOT, or set `orchestrator_repo` "
            f"(an absolute path) in {POLL_CONFIG}"
        ) from None
    if not repo.is_absolute() or not (repo / "repos.yaml").is_file():
        raise SystemExit(
            f"`orchestrator_repo` in {POLL_CONFIG} must be the absolute path of the "
            "orchestrator repo, which holds repos.yaml"
        )
    return repo


def workspace_path():
    """The coordinator's Orca workspace: the orchestrator repo's own worktree (DQ12)."""
    return str(repo_root())


def state_dir():
    d = repo_root() / ".dev" / "coordinator"
    d.mkdir(parents=True, exist_ok=True)
    return d


def runs_dir():
    d = state_dir() / "runs"
    d.mkdir(parents=True, exist_ok=True)
    return d


TITLE_MAX = 200


def safe_title(text, limit=TITLE_MAX):
    """A title other people wrote (an issue, a task, a session) as one short plain line before it goes into the
    writing sheet the model reads: control and format characters (escape codes, bidirectional overrides,
    zero-width marks) dropped, whitespace and line breaks folded, at most `limit` characters. A title stays
    data: SKILL.md Step 10 tells the model so."""
    text = "".join(
        c for c in str(text) if unicodedata.category(c)[0] != "C" or c in " \t\n"
    )
    return " ".join(text.split())[:limit].rstrip()


def read_json(path, default=None):
    p = Path(path)
    if not p.exists():
        return default
    return json.loads(p.read_text())


def write_json(path, data):
    """Write sorted, indented JSON so identical data gives identical bytes."""
    Path(path).write_text(
        json.dumps(data, indent=1, sort_keys=True, ensure_ascii=False) + "\n"
    )


class CommandError(Exception):
    pass


def run_cmd(args, timeout=120):
    """Run a command; return stdout. Raise CommandError with stderr on failure."""
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired as e:
        raise CommandError(f"timed out after {timeout}s: {' '.join(args)}") from e
    if r.returncode != 0:
        raise CommandError(
            (r.stderr or r.stdout).strip()[:500] or f"exit {r.returncode}"
        )
    return r.stdout


def gh_json(*args, timeout=120):
    return json.loads(run_cmd(["gh", *args], timeout=timeout) or "null")


def answered_since(since):
    """Item URLs with a recorded answer from the person in the action log at or after `since`."""
    path = state_dir() / "action-log.jsonl"
    if not path.exists():
        return set()
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    return {
        r["item"]
        for r in rows
        if r["action"] == "answer" and r["item"] and r["time"] >= (since or "")[:19]
    }


# The orchestrator's living report (spec DQ12, 6.4). The orchestrator keeps one entry file per issue it holds
# in `.dev/coordinator/orchestrated/<owner>__<repo>__<number>.json`; a closed issue's file moves to
# `orchestrated/closed/`, and an information item (a mention, an issue that could be assigned) lives in
# `orchestrated/info/<kind>__<key>.json`. `superclaude orchestrator report-entry` writes them; this skill
# reads them (exclude.py, run.py refresh, render.py entry) and moves a closed one (run.py refresh).
#
# One flat JSON object. The written parts use the slot names of WRITTEN (below): state, next, what, state_text,
# done, todo, happened, recommend, needs, how, plus suggested and priority_why when priority is "Unset"; each
# is the text of that part of templates/item-template.md (done, todo and happened are "- " bullets).
# `session_status` maps a session id to "<status>: <reason>" (a status of SESSION_STATUSES). The fixed fields:
#   url            the issue's url (else made from the file name)       title, kind, group, priority
#   assignees      logins                                                human_assignee   a login
#   author         the login that opened the issue ("Opened by"; never the assignee; "Unknown" when absent)
#   orchestrator   {"id", "tag", "session_id", "link", "tier"}           (link: orca://session/<session id>)
#   worker         {"session_ids": [...], "link", "title", "branch", "tier"}
#   pr_url         the worker's pull request, once there is one          last_update      ISO time (UTC)
#   closed_at, close_reason   added by run.py refresh when it moves the file to closed/
# Every field but the written parts is optional for the readers: a missing one gives a plainly worded
# fallback and never an exception, so one odd file cannot stop the daily run.
ORCHESTRATED = "orchestrated"
ESCALATION_LINES = (
    "Why this reaches you:",
    "Low-stakes options:",
    "If you do not answer:",
)


def orchestrated_dir():
    return state_dir() / ORCHESTRATED


def entry_files(folder=None):
    """{path: entry} for each entry file directly inside `folder` (default `orchestrated/`; the `closed/` and
    `info/` folders below it are not read). A file that does not parse is named on stderr and left out."""
    folder = Path(folder) if folder else orchestrated_dir()
    found = {}
    for p in sorted(folder.glob("*.json")) if folder.is_dir() else []:
        if p.is_symlink():  # a link could point at any file on the host
            print(f"entry file {p.name} left out: it is a symlink", file=sys.stderr)
            continue
        try:
            data = json.loads(p.read_text())
        except (OSError, ValueError) as e:
            print(f"entry file {p.name} left out: {e}", file=sys.stderr)
            continue
        if isinstance(data, dict):
            found[p] = data
        else:
            print(f"entry file {p.name} left out: not a JSON object", file=sys.stderr)
    return found


def entry_issue_url(entry, path):
    """The issue's url: the file's `url`, else the one the name `<owner>__<repo>__<number>` spells."""
    if entry.get("url"):
        return entry["url"]
    parts = Path(path).stem.split("__", 1)
    if len(parts) == 2 and "__" in parts[1]:
        repo, number = parts[1].rsplit("__", 1)
        return f"https://github.com/{parts[0]}/{repo}/issues/{number}"
    return ""


def entry_session_ids(entry):
    """Every session id an entry names: its worker's, its orchestrator's, and each in `session_status`."""
    ids = set(entry.get("session_status") or {})
    worker, orch = entry.get("worker") or {}, entry.get("orchestrator") or {}
    ids |= set(worker.get("session_ids") or [])
    if orch.get("session_id"):
        ids.add(orch["session_id"])
    for link in (worker.get("link"), orch.get("link")):
        if link and link.startswith(SESSION_URL):
            ids.add(link.removeprefix(SESSION_URL))
    return {i for i in ids if i}


# Reading the overview back (render carries parts of yesterday's report; check verifies today's).

ITEM_URL = r"(?:https://(?:github\.com/[^)\s>]+/(?:issues|pull)/\d+|app\.clickup\.com/t/[\w-]+)|orca://session/[\w-]+)"
ENTRY_SECTIONS = ("Your work by priority", "Other work in progress")
SESSION_STATUSES = (
    "working",
    "progressed",
    "waiting on you",
    "stuck",
    "stalled",
    "done",
)
SESSION_LINE = re.compile(r"\]\(orca://session/([\w-]+)\).*?· status: ([^\n]*)")


TZ = ZoneInfo(CONFIG["timezone"])
DASHES = re.compile("[\N{EN DASH}\N{EM DASH}]")
# Why a ClickUp task left the list when it is still open but quiet: the report counts these in one line.
QUIET_REASON = "still open, but nothing happened on it in"


def local_time(ts):
    """An ISO time as `2026-11-03 07:14 CST`: every time in the report is local and says its zone."""
    if not ts:
        return "unknown"
    try:
        return (
            datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
            .astimezone(TZ)
            .strftime("%Y-%m-%d %H:%M %Z")
        )
    except ValueError:
        return str(ts)


def report_days_between(first, last):
    """Report days (config report_days) strictly between two dates."""
    days, d = [], first + timedelta(days=1)
    while d < last:
        if d.strftime("%a") in CONFIG["report_days"]:
            days.append(d)
        d += timedelta(days=1)
    return days


def section(text, heading):
    """The body of the `## heading` section (up to the next `## `), or ''."""
    parts = re.split(r"\n(?=## )", "\n" + text)
    for p in parts:
        if p.startswith(f"## {heading}"):
            return p.split("\n", 1)[1] if "\n" in p else ""
    return ""


def blocks(text, level):
    """Split text into blocks that start with a heading of exactly `level` hashes."""
    out = []
    for chunk in re.split(r"\n(?=#{1,6} )", "\n" + text):
        if chunk.startswith("#" * level + " "):
            out.append(chunk)
    return out


def entry_blocks(text):
    """{item url: entry block} for every `#### ` entry in "Your work by priority" and "Other work in progress"."""
    found = {}
    for heading in ENTRY_SECTIONS:
        for b in blocks(section(text, heading), 4):
            m = re.search(r"\]\((" + ITEM_URL + r")\)", b)
            if m:
                found[m.group(1)] = b
    return found


def session_statuses(text):
    """{session id: its status line text} from every agent session line of a report."""
    return {sid: st.strip() for sid, st in SESSION_LINE.findall(text)}


# "Needs you" holds only agent sessions that stopped with their work not done and wait on Clay to answer,
# approve or unblock them (CLAY, 2026-11-05); every other ask stays in its item's own "Needs you" part.
SESSION_URL = "orca://session/"
NO_ONE_WAITING = "No agent session is waiting on you."
# Said once under "Not checked" every run, so a short "Needs you" is never read as "nothing is stuck".
NOT_ASKED = (
    "Agent sessions that stopped without asking anything were not asked what they need: the orchestrator "
    'does every check-in itself and there is no session manager, so "Needs you" lists only sessions whose own '
    "transcript shows them waiting on you."
)


def waiting_sessions(text):
    """{session url: url of the item it sits under} for every agent session whose status is "waiting on you"."""
    out = {}
    for item, block in entry_blocks(text).items():
        for sid, st in SESSION_LINE.findall(block):
            if st.startswith("waiting on you"):
                out[SESSION_URL + sid] = item
    return out


def needs_link(block):
    """The URL a "Needs you" entry's heading links, or ''."""
    m = re.match(r"### \[[^\]]*\]\((" + ITEM_URL + r")\)", block)
    return m.group(1) if m else ""


# The parts of one item, in the order of templates/item-template.md (CLAY, 2026-11-04: every item follows the
# template every day). (label, slot): slot is the model's written part, None where the script fills it.
ITEM_SECTIONS = (
    ("What it is", "what"),
    ("Current state", "state_text"),
    ("Done, with evidence", "done"),
    ("Still to do", "todo"),
    ("What happened since the previous report", "happened"),
    ("Recommendation", "recommend"),
    ("Needs you", "needs"),
    ("ClickUp tasks", None),
    ("Agent sessions", None),
    ("Why this priority", None),
    ("How I know", "how"),
)
# Parts written as bullets only, one point per bullet, never a paragraph (CLAY, 2026-11-05).
BULLET_SLOTS = ("done", "todo", "happened")
# The bullets of one "Needs you" entry, in the order of templates/needs-you-template.md.
NEEDS_PARTS = (
    "What it is",
    "Where it stands",
    "Question",
    "Why this reaches you",
    "Low-stakes options",
    "Options",
    "Recommendation",
    "If you do not answer",
    "Answer on",
)
# Every written part: the state (first on the status line), the Next line, and the sections above.
WRITTEN = ("state", "next") + tuple(s for _, s in ITEM_SECTIONS if s)
# The state on each card (CLAY, 2026-11-04: the page must show where each piece of work stands).
STATES = (
    "Waiting on you",
    "Waiting on others",
    "In progress",
    "Ready to merge",
    "Needs work",
    "Not started",
    "Blocked",
    "Can close",
    "Done",
)
WRITE_GROUPS = ("assigned", "owned", "opened", "inprogress")
# The priority protocol (templates/item-template.md, CLAY 2026-11-05): levels, then states, in report order.
LEVELS = ("Urgent", "High", "Medium", "Low")
STATE_ORDER = (
    "Waiting on you",
    "Needs work",
    "Blocked",
    "Waiting on others",
    "In progress",
    "Ready to merge",
    "Not started",
    "Can close",
    "Done",
)
SUGGESTED = "Suggested "  # the status line's priority when the model suggested it
UPDATE_MARK = "<!-- RF_UPDATE:"  # a changed item's carried parts: update each one, then delete the marker
# Where Clay opens the page: a local web address, which Orca opens in its own browser when clicked (a file://
# link opens the file as code; CLAY, 2026-11-05). page.py --open starts the local server when it is down.
REPORT_PORT = 8765
REPORT_URL = f"http://127.0.0.1:{REPORT_PORT}/report.html"
# Header lines about the helper itself; they lead the report, the page and the summary.
NOTICES = (
    "**Missed reports:**",
    "**Stuck run replaced:**",
    "**Two coordinator sessions are running:**",
)


def previous_notes(run):
    """{item url: notes} as the previous completed run left them (its notes.json), or {}."""
    prev = read_json(Path(run) / "run.json", {}).get("previous_completed_run")
    return read_json(Path(run).parent / prev / "notes.json", {}) if prev else {}


def to_write(run):
    """The listed items whose written parts need writing or updating this run: new or changed, or never
    written. Every other item gets its parts from the previous run's notes.json unchanged."""
    run = Path(run)
    cls, cmp_, notes = (
        read_json(run / "classified.json"),
        read_json(run / "compare.json"),
        previous_notes(run),
    )
    return [
        u
        for u in cls["order"]
        if cls["items"][u]["group"] in WRITE_GROUPS
        and (u in cmp_["new"] or u in cmp_["changed"] or u not in notes)
    ]


def item_parts(block):
    """{label: text} of one item block as the item template lays it out: "state" and "next" for the status
    and Next lines, and every "- **Label:**" section with its indented lines (stripped of the indent)."""
    lines = block.strip("\n").splitlines()
    out = {"heading": lines[0] if lines else ""}
    if len(lines) > 1:
        status = [s.strip() for s in lines[1].split(" · ")]
        out["state"] = status[0]
        out["priority"] = status[1] if len(status) > 1 else ""
    m = re.search(r"(?m)^\*\*Next:\*\* (.*)$", block)
    out["next"] = m.group(1).strip() if m else ""
    cur = None
    for line in lines:
        s = re.match(r"^- \*\*(.+?):\*\* ?(.*)$", line)
        if s:
            cur = s.group(1)
            out[cur] = s.group(2).strip()
        elif (
            cur
            and line.startswith("  ")
            and line.strip()
            and not line.strip().startswith("<!--")
        ):
            out[cur] = (out[cur] + "\n" + line[2:].rstrip()).strip("\n")
        elif not line.startswith("  "):
            cur = None
    return out


def item_written(block):
    """{slot: text} of the model's written parts of one item block (what notes.json carries to the next day)."""
    parts, out = item_parts(block), {}
    out["state"], out["next"] = parts.get("state", ""), parts.get("next", "")
    for label, slot in ITEM_SECTIONS:
        if slot:
            out[slot] = parts.get(label, "")
    if parts.get("priority", "").startswith(
        SUGGESTED
    ):  # a suggested level and its reason are written parts too
        out["suggested"] = parts["priority"].removeprefix(SUGGESTED)
        out["priority_why"] = parts.get("Why this priority", "")
    return {k: v for k, v in out.items() if v and "RF_PLACEHOLDER" not in v}


def order_key(parts):
    """Where an item, or the "Needs you" entry about it, sorts in the report (the priority protocol in
    templates/item-template.md): its level, set or suggested, then its state."""
    level = parts.get("priority", "").removeprefix(SUGGESTED)
    state = parts.get("state", "").rstrip(".")
    return (
        LEVELS.index(level) if level in LEVELS else len(LEVELS),
        STATE_ORDER.index(state) if state in STATE_ORDER else len(STATE_ORDER),
    )


def needs_in_order(text):
    """The "Needs you" entries of a writing sheet, highest priority first: each sorts by the item its session
    sits under (order_key of that item's entry); an entry whose item is not listed goes last, in written order."""
    items = {u: order_key(item_parts(b)) for u, b in entry_blocks(text).items()}
    under = waiting_sessions(text)
    entries = [
        b.strip("\n")
        for b in re.split(r"\n(?=### )", "\n" + section(text, "Needs you"))
        if b.startswith("### ")
    ]

    def key(b):
        u = needs_link(b)
        return items.get(under.get(u, u), (len(LEVELS) + 1, 0))

    return sorted(entries, key=key)  # sorted() keeps written order among equals
