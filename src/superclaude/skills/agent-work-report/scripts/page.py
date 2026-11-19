#!/usr/bin/env python3
"""Build the report page Clay reads (report.html) from the checked writing sheet and the run's files.

usage: page.py <run_folder>      build the page
       page.py --open            show it in Orca's browser (reuses the "Your Work Report" tab)

The page follows Clay's open-work.html (CLAY, 2026-11-04: "the HTML version is much better"): a card per
item with its state and priority, who opened it, who has it, its board, the next step, and its notes and
recent activity when opened; plus what the daily report adds: "Needs you", ClickUp tasks, agent sessions,
what changed since the previous report, and what closed or was not checked. Every fact comes from the run's
files; the only written text is the model's notes and "Needs you" in overview.md, which check.py has passed.

Writes <run>/report.html, <run>/notes.json (the previous notes with this run's on top: what the next run
reuses for an unchanged item), and copies the page to .dev/coordinator/report.html, the one place it lives.
"""

import hashlib
import html
import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

from common import (
    ITEM_SECTIONS,
    NEEDS_PARTS,
    NOTICES,
    REPORT_PORT,
    REPORT_URL,
    SKILL_DIR,
    SUGGESTED,
    TZ,
    entry_blocks,
    item_parts,
    item_written,
    local_time,
    needs_in_order,
    order_key,
    previous_notes,
    read_json,
    section,
    session_statuses,
    state_dir,
    workspace_path,
    write_json,
)
from render import GROUP_TITLES, LISTED, change_note, short

KIND = {
    "pr": "Pull request",
    "issue": "Issue",
    "task": "ClickUp task",
    "session": "Agent session",
}
LINK = re.compile(r"\[([^\]]*(?:\[[^\]]*\][^\]]*)*)\]\(([^)\s]+)\)")


def md(text):
    """One line of the writing sheet's Markdown as HTML: escaped, with links, bold and code."""
    out, last = [], 0
    for m in LINK.finditer(
        text
    ):  # links first, so their URLs are never touched by bold or code
        out.append(_inline(text[last : m.start()]))
        # A plain link: Orca's browser blocks links that open a new window, so they did nothing when clicked
        # (VERIFIED 2026-11-05); this one opens in the same tab, and Back returns to the report.
        out.append(f'<a href="{html.escape(m.group(2))}">{_inline(m.group(1))}</a>')
        last = m.end()
    return "".join(out) + _inline(text[last:])


def _inline(s):
    s = html.escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)\*(?![\w*])", r"<em>\1</em>", s)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", s)


def bullets_html(text):
    """'- ' lines, two spaces of indent per level, as nested lists."""
    out, depth = [], 0
    for line in text.splitlines():
        if not line.strip():
            continue
        level = (len(line) - len(line.lstrip())) // 2 + 1
        body = line.strip()[2:] if line.strip().startswith("- ") else line.strip()
        out += ["<ul>"] * max(0, level - depth) + ["</ul>"] * max(0, depth - level)
        depth = level
        out.append(f"<li>{md(body)}</li>")
    return "".join(out + ["</ul>"] * depth)


def parts_html(parts, labels):
    """The template's parts in its order, each one bullet: a one-line part inline, a bulleted part nested
    under its label (CLAY, 2026-11-05: bullets, every part shown, nothing behind a click)."""
    items = []
    for label in labels:
        value = parts.get(label) or "N/A"
        if any(ln.strip().startswith("- ") for ln in value.splitlines()):
            items.append(
                f"<li><strong>{html.escape(label)}:</strong>{bullets_html(value)}</li>"
            )
        else:
            items.append(
                f"<li><strong>{html.escape(label)}:</strong> {md(' '.join(value.split()))}</li>"
            )
    return '<ul class="parts">' + "".join(items) + "</ul>"


def needs_you(text):
    """Each "Needs you" entry, laid out by templates/needs-you-template.md, in the priority protocol's order:
    its item's level (set or suggested), then its state (CLAY, 2026-11-05)."""
    out = []
    for b in needs_in_order(text):
        parts = item_parts(b)
        out.append(
            {
                "title": md(parts["heading"][4:].strip()),
                "body": parts_html(parts, NEEDS_PARTS),
                "carried": "Carried from the previous report" in b,
            }
        )
    return out


def list_lines(text, heading):
    """The "- " lines of a section, as HTML."""
    return [
        md(ln.strip()[2:])
        for ln in section(text, heading).splitlines()
        if ln.strip().startswith("- ")
    ]


def likely_lines(text):
    """The "Likely yours" judgments: one line each, starting with the item's link."""
    return [
        md(ln.strip().removeprefix("- "))
        for ln in section(text, "Likely yours").splitlines()
        if ln.strip().removeprefix("- ").startswith("[")
    ]


def day(ts):
    return local_time(ts)[:10] if ts else ""


def change_of(url, cmp_):
    if url in cmp_["new"]:
        return "New"
    if url in cmp_["changed"]:
        return "Changed"
    return "Carried" if url in cmp_["carried"] else "No change"


def card(url, it, c, cmp_, block, statuses, as_of):
    """One item as the page shows it: the facts from the run's files, and every part of its block in the
    writing sheet in the item template's order (templates/item-template.md)."""
    parts = item_parts(block)
    sessions = []
    for s in it.get("sessions", []):
        st = statuses.get(s["session_id"], "")
        state, _, reason = st.partition(": ")
        sessions.append(
            {
                "title": s["title"],
                "url": s["url"],
                "branch": s.get("branch") or "",
                "running": bool(s.get("claude_running")),
                "last": local_time(s.get("last_event")),
                "state": state,
                "reason": md(reason),
            }
        )
    return {
        "url": url,
        "ref": short(url),
        "title": it["title"],
        "kind": KIND.get(it.get("kind"), "Item"),
        "source": it.get("source", "github"),
        "group": c["group"],
        "why": c.get("why") or GROUP_TITLES.get(c["group"], ""),
        # The priority protocol: a set level, else the one the model suggested ("Suggested High" on the page).
        "priority": parts.get("priority", "").removeprefix(SUGGESTED)
        if c["priority"] == "Unset"
        else c["priority"],
        "suggested": c["priority"] == "Unset",
        "rank": list(order_key(parts)),
        "prioritySource": c.get("priority_source", ""),
        # A ClickUp task tied to no GitHub issue, pull request or repository: listed on its own at the bottom
        # (CLAY, 2026-11-05: many are old and unmanaged, and they crowd the list).
        "clickupOnly": it.get("source") == "clickup" and not it.get("github_links"),
        "board": ", ".join(
            f"{b['board']}: {b['status']}"
            for b in it.get("boards", [])
            if b.get("status")
        ),
        "author": it.get("author") or "",
        "assignees": it.get("assignees") or [],
        "reviewers": it.get("review_requests") or [],
        "created": day(it.get("created")),
        "updated": day(it.get("updated")),
        "change": change_of(url, cmp_),
        "changeNote": change_note(url, cmp_),
        "owner": f"You ({c.get('why') or GROUP_TITLES.get(c['group'], 'yours')})",
        "state": parts.get("state", "").rstrip("."),
        "next": md(parts.get("next", "")),
        "asOf": as_of,
        "what": md(parts.get("What it is", "")),
        "sections": [
            label for label, _ in ITEM_SECTIONS
        ],  # the template's parts, in order
        "parts": parts_html(parts, [label for label, _ in ITEM_SECTIONS]),
        "sessions": sessions,
    }


def main(run):
    run = Path(run)
    text = (run / "overview.md").read_text()
    meta = read_json(run / "run.json")
    cls, cmp_ = read_json(run / "classified.json"), read_json(run / "compare.json")
    items = {i["url"]: i for i in read_json(run / "items.json")}
    snap = read_json(run / "snapshot.json", {})
    statuses = session_statuses(text)
    started = datetime.fromisoformat(meta["started"]).astimezone(TZ)
    today = started.strftime("%Y-%m-%d")

    # Every item's written parts as the sheet now has them; the next run starts from these (notes.json).
    prev_notes, found = previous_notes(run), entry_blocks(text)
    written_now = set(read_json(run / "to-write.json", []))
    listed = [u for u in cls["order"] if cls["items"][u]["group"] in LISTED]
    held = [
        u
        for u in cmp_["carried"]
        if snap.get(u, {}).get("group") in LISTED and u not in items
    ]
    notes = {}
    for u in sorted(set(listed) | set(held)):
        got = item_written(found.get(u, ""))
        if got:
            notes[u] = dict(
                got,
                as_of=today
                if u in written_now
                else prev_notes.get(u, {}).get("as_of", today),
            )
    write_json(run / "notes.json", notes)

    as_of = lambda u: notes.get(u, {}).get("as_of", "")  # noqa: E731
    cards = [
        card(u, items[u], cls["items"][u], cmp_, found.get(u, ""), statuses, as_of(u))
        for u in listed
    ]
    for u in held:  # its source was not read this run: shown from the previous snapshot
        s = snap[u]
        it = {
            "title": s["title"],
            "kind": s.get("kind"),
            "source": s.get("source", "github"),
            "assignees": s.get("assignees") or [],
        }
        c = {"group": s["group"], "priority": s.get("priority", "Unset")}
        cards.append(card(u, it, c, cmp_, found.get(u, ""), statuses, as_of(u)))

    head = text.split("\n## ", 1)[0]
    pick = lambda pattern: (re.search(pattern, head) or [None, ""])[1]  # noqa: E731
    prev = meta.get("previous_completed_run")
    data = {
        "date": started.strftime("%A %Y-%m-%d"),
        "generated": started.strftime("%Y-%m-%d %H:%M %Z"),
        "run": meta["run"],
        "previous": prev or "",
        "sources": md(pick(r"\*\*Sources read:\*\* (.+)")),
        "missed": [md(ln) for ln in head.splitlines() if ln.startswith(NOTICES)],
        "changes": md(pick(r"(?m)^\*\*Since the previous report:\*\* (.+)$")),
        "needs": needs_you(text),
        "items": cards,
        "likely": likely_lines(text),
        "closed": list_lines(text, "Closed since the previous report"),
        "notChecked": list_lines(text, "Not checked"),
        "how": list_lines(text, "How this was made"),
    }
    blob = json.dumps(data, separators=(",", ":")).replace("</", "<\\/")
    tpl = (SKILL_DIR / "templates" / "report-template.html").read_text()
    sha = hashlib.sha256(text.encode()).hexdigest()
    page = (
        tpl.replace("__OVERVIEW_SHA256__", sha)
        .replace("__DATA__", blob)
        .replace("__SCRIPT__", (SKILL_DIR / "templates" / "report.js").read_text())
    )
    (run / "report.html").write_text(page)
    shutil.copyfile(run / "report.html", state_dir() / "report.html")
    print(
        f"{run / 'report.html'} (also {state_dir() / 'report.html'}): {len(cards)} items, "
        f"{len(data['needs'])} Needs you, {len(page) // 1024} KB"
    )


def ensure_server():
    """Serve .dev/coordinator on 127.0.0.1 (this machine only) so REPORT_URL answers; start it if it is down."""
    import subprocess
    import urllib.request

    try:
        urllib.request.urlopen(REPORT_URL, timeout=3).close()
        return
    except OSError:
        pass
    subprocess.Popen(
        [
            sys.executable,
            "-m",
            "http.server",
            str(REPORT_PORT),
            "--bind",
            "127.0.0.1",
            "--directory",
            str(state_dir()),
        ],
        start_new_session=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
    )
    for _ in range(20):
        try:
            urllib.request.urlopen(REPORT_URL, timeout=1).close()
            return
        except OSError:
            import time

            time.sleep(0.5)
    raise SystemExit(f"the local report server did not start on {REPORT_URL}")


def open_tab():
    """Show the page in Orca's browser (CLAY, 2026-11-05: opening the file shows its code), always as the one
    "Your Work Report" tab of the coordinator workspace: reused and reloaded, extra copies closed, so Clay
    always finds it in the same place."""
    import orca_term  # only needed to deliver

    ensure_server()
    url = REPORT_URL
    where = f"path:{workspace_path()}"
    tabs = orca_term.orca("tab", "list", "--worktree", where).get("tabs", [])
    mine = [
        t for t in tabs if t.get("url") in (url, (state_dir() / "report.html").as_uri())
    ]
    for old in [
        t for t in mine if t.get("url") != url
    ]:  # a tab from before the local address: replace it
        orca_term.orca("tab", "close", "--page", old["browserPageId"])
    mine = [t for t in mine if t.get("url") == url]
    for extra in mine[1:]:
        orca_term.orca("tab", "close", "--page", extra["browserPageId"])
    if mine:
        orca_term.orca("tab", "switch", "--page", mine[0]["browserPageId"])
        # `orca reload` left the tab on the previous report (VERIFIED 2026-11-05); a reload from inside the
        # page fetches the new one.
        orca_term.orca(
            "eval",
            "--page",
            mine[0]["browserPageId"],
            "--expression",
            "location.reload()",
        )
    else:
        orca_term.orca("tab", "create", "--url", url, "--worktree", where)
    print(f'opened {url} in the coordinator workspace\'s "Your Work Report" tab')


if __name__ == "__main__":
    if sys.argv[1:] == ["--open"]:
        open_tab()
    elif len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        sys.exit(__doc__)
