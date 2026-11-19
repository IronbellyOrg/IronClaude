#!/usr/bin/env python3
"""Write activity.md: what happened on each of the person's new or changed items since the last report.

usage: activity.py <run_folder>

Short on purpose: for each new or changed item in the person's groups and the candidates, its last
MAX_EVENTS GitHub events since the previous report (comments trimmed), a pull request's checks and review
state, its ClickUp tasks' new comments, and its agent sessions' last prompts and reply. Then every ClickUp
chat message to the person. The model writes the report's short notes from this file and calls nothing.
"""

import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from common import CONFIG, CommandError, gh_json, previous_notes, read_json, to_write
from common import local_time as when_local

SKIP = {
    "subscribed",
    "mentioned",
    "unsubscribed",
    "project_v2_item_status_changed",
    "added_to_project_v2",
    "issue_field_added",
    "issue_type_added",
    "labeled",
    "unlabeled",
}
MINE = {"assigned", "owned", "opened", "inprogress", "candidate"}
MAX_EVENTS = 8
BODY = 600


def when(e):
    """An event's time; commits carry theirs under author or committer, not created_at."""
    return (
        e.get("created_at")
        or e.get("submitted_at")
        or (e.get("author") or {}).get("date")
        or (e.get("committer") or {}).get("date")
        or ""
    )


def events(url, since):
    org, repo, _, n = url.replace("https://github.com/", "").split("/")[:4]
    try:
        pages = gh_json(
            "api",
            "--paginate",
            "--slurp",
            f"repos/{org}/{repo}/issues/{n}/timeline?per_page=100",
        )
    except CommandError as e:
        return [f"- could not read the timeline: {e}"]
    evs = [e for page in pages for e in page if e.get("event") not in SKIP]
    evs = ([e for e in evs if when(e) >= since] if since else evs)[-MAX_EVENTS:]
    lines = []
    for e in evs:
        t, who, ev = (
            when_local(when(e)),
            (e.get("actor") or e.get("user") or {}).get("login", ""),
            e.get("event"),
        )
        if ev in ("commented", "reviewed"):
            body = " ".join((e.get("body") or "").split())
            lines.append(f'- {t} {ev} by {who} {e.get("state", "")}: "{body[:BODY]}"')
        elif ev in ("assigned", "unassigned"):
            lines.append(
                f"- {t} {ev} {(e.get('assignee') or {}).get('login')} by {who}"
            )
        elif ev == "renamed":
            r = e.get("rename") or {}
            lines.append(f"- {t} renamed by {who}: {r.get('from')} -> {r.get('to')}")
        elif ev == "cross-referenced":
            src = (e.get("source") or {}).get("issue") or {}
            lines.append(
                f"- {t} referenced from {src.get('html_url')} ({src.get('state')}) {src.get('title', '')[:80]}"
            )
        elif ev == "committed":
            lines.append(
                f"- {when_local((e.get('author') or {}).get('date', ''))} commit {e.get('sha', '')[:8]}: {(e.get('message') or '').splitlines()[0][:100]}"
            )
        elif ev == "referenced":
            # GitHub's "referenced" is a commit message that names this item, not another issue or pull request.
            lines.append(
                f"- {t} a commit by {who} mentioned this item in its message (commit {(e.get('commit_id') or '')[:8]})"
            )
        elif ev:
            lines.append(f"- {t} {ev} by {who}")
    return lines


def pr_state(url):
    try:
        p = gh_json(
            "pr",
            "view",
            url,
            "--json",
            "mergeable,isDraft,reviewDecision,statusCheckRollup",
        )
    except CommandError as e:
        return f"- now: could not read ({e})"
    checks = {}
    for c in p.get("statusCheckRollup") or []:
        k = (c.get("conclusion") or c.get("state") or "PENDING").upper()
        checks[k] = checks.get(k, 0) + 1
    return (
        f"- now: mergeable={p.get('mergeable')} draft={p.get('isDraft')} "
        f"review={p.get('reviewDecision') or 'none'} checks={dict(sorted(checks.items()))}"
    )


def clickup_lines(t, comments):
    lines = [
        f"- ClickUp task [{t['title']}]({t['url']}): {t['boards'][0]['status']}; assignees "
        f"{', '.join(t['assignees']) or 'none'}; updated {when_local(t['updated'])}"
    ]
    for c in comments.get(t["url"], [])[-MAX_EVENTS:]:
        lines.append(
            f"  - {when_local(c['date'])} comment by {c['from']}{' (mentions you)' if c['mentions_you'] else ''}: "
            f'"{" ".join(c["text"].split())[:BODY]}"'
        )
    return lines


def session_lines(s):
    f = s["since_previous_report"]
    lines = [
        f"- Agent session {s['title']} (orca://session/{s['session_id']}), branch {s['branch'] or 'none'}: "
        f"Claude {'running' if s['claude_running'] else 'not running'}, {f['events']} events since the previous "
        f"report, last activity {when_local(s.get('last_event'))}"
    ]
    lines += [
        f'  - you asked {when_local(p["time"])}: "{" ".join(p["text"].split())[:300]}"'
        for p in f["prompts"][-3:]
    ]
    lines += [
        f'  - its last reply {when_local(r["time"])}: "{" ".join(r["text"].split())[:400]}"'
        for r in f["replies"][-1:]
    ]
    lines += [f"  - error: {e[:200]}" for e in f["errors"][-2:]]
    if f["pending_tool_call"]:
        lines.append(
            f"  - stopped on a {f['pending_tool_call']['tool']} call with no result since {when_local(f['pending_tool_call']['time'])}"
        )
    return lines


def main(run):
    run = Path(run)
    cls, cmp_ = read_json(run / "classified.json"), read_json(run / "compare.json")
    meta = read_json(run / "run.json", {})
    prev = meta.get("previous_completed_run")
    since = (
        read_json(run.parent / prev / "run.json", {}).get("started") if prev else None
    )
    items = {i["url"]: i for i in read_json(run / "items.json")}
    sessions = {s["session_id"]: s for s in read_json(run / "sessions.json", [])}
    cu_events = read_json(run / "clickup-events.json", {"comments": {}, "chat": []})
    notes = previous_notes(run)
    write = set(to_write(run))
    targets = [
        u
        for u in cls["order"]
        if u in write
        or (
            cls["items"][u]["group"] == "candidate"
            and (u in cmp_["new"] or u in cmp_["changed"])
        )
    ]

    def section(url):
        it = items[url]
        evs = []
        if it.get("source", "github") == "github":
            # A new item, or one never written up, gets its last events from the start, not just since.
            evs = events(url, None if url in cmp_["new"] or url not in notes else since)
            if "/pull/" in url:
                evs.append(pr_state(url))
        for t in ([it] if it.get("source") == "clickup" else []) + it.get(
            "clickup", []
        ):
            evs += clickup_lines(t, cu_events["comments"])
        evs += [
            ln
            for s in it.get("sessions", [])
            if s["session_id"] in sessions
            for ln in session_lines(sessions[s["session_id"]])
        ]
        return (
            [f"## {it['title']}", url]
            + (evs or ["- no activity in this window"])
            + [""]
        )

    with ThreadPoolExecutor(max_workers=6) as pool:
        parts = list(pool.map(section, targets))
    # Every item with no priority set may already state one in its text or a comment by someone else
    # (CLAY, 2026-11-17: a priority in a comment counts); the model judges each line.
    mentions = [
        "## Priority lines in the text or comments of items with no priority set",
        "",
    ]
    for u in cls["order"]:
        found = [
            m
            for m in items[u].get("priority_mentions", [])
            if m["by"] != CONFIG["person"]
        ]
        if (
            cls["items"][u]["group"] in MINE
            and cls["items"][u]["priority"] == "Unset"
            and found
        ):
            mentions.append(f"### {items[u]['title']} ({u})")
            mentions += [
                f'- {m["date"][:10]} {m["where"]} by {m["by"]}: "{m["line"]}"'
                for m in found[-3:]
            ]
    if len(mentions) == 2:
        mentions.append("- none")
    parts.append(mentions + [""])
    head = [
        f"# Activity since {when_local(since) if since else 'the start (first report: last events only)'}",
        "",
    ]
    chat = ["## ClickUp messages to you", ""]
    for m in cu_events["chat"]:
        chat.append(
            f"- {when_local(m['date'])} from {m.get('from') or m.get('from_user_id')}"
            f'{" (tags you)" if m.get("mentions_you") else ""}: "{" ".join(m["text"].split())[:BODY]}"'
        )
    if len(chat) == 2:
        chat.append("- none since the previous report")
    (run / "activity.md").write_text(
        "\n".join(head + [line for p in parts for line in p] + chat) + "\n"
    )
    print(
        f"activity for {len(targets)} items; {len(cu_events['chat'])} ClickUp chat messages"
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
