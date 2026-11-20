#!/usr/bin/env python3
"""Read Clay's ClickUp work and send him the report notice, through the ClickUp API (FR-3, FR-11, FR-26).

usage:
  clickup.py <run_folder>                    read everything for the report
  clickup.py dm <run_folder> <message_file>  send the file's text to the token owner's self DM

Uses the ClickUp REST API with the person's own token, never the ClickUp MCP connector (about 300 calls a
day per workspace; IronClaude #302). The token comes only from the environment: CLICKUP_API_TOKEN, from the
Coder `aienv` secret written to ~/.env. CLICKUP_WORKSPACE_ID is optional. The token is never printed.

What a read finds (shapes VERIFIED live 2026-10-30 against workspace 14226392):
  - every open task the token can see, in one paged sweep, sorted into: assigned to Clay; created by Clay
    with nobody assigned; watched by Clay (neither), kept only when it changed or mentions him
  - tasks updated since the previous report, open or closed, so a task that left Clay's list gets its
    real reason (closed, or reassigned)
  - comments and replies since the previous report on Clay's tasks and on every task updated since, which
    finds @mentions of him anywhere (a comment part {"type": "tag", "user": {"id": ...}})
  - chat since the previous report: his direct and group messages from others, channel messages that tag
    him ("[@Name](#user_mention#<id>)"), and their thread replies
  - each task's space, folder and list, parent and relationship fields, dependencies, and GitHub links
Writes into the run folder: clickup-items.json, clickup-events.json, clickup-gone.json, clickup-replies.json,
clickup-status.json. Any failure is recorded and shown under "Not checked"; nothing is guessed.
"""

import http.client
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from common import CONFIG, QUIET_REASON, read_json, state_dir, write_json

API = "https://api.clickup.com/api"
MAX_TASK_PAGES = 200
MAX_COMMENT_CALLS = 400
ACTIVE_DAYS = 30
FIRST_RUN_DAYS = 1
OVERLAP_MS = 10 * 60 * 1000
GITHUB_URL = re.compile(r"https://github\.com/[\w.-]+/[\w.-]+/(?:issues|pull)/\d+")
PRIORITY = {"urgent": "Urgent", "high": "High", "normal": "Medium", "low": "Low"}
NOTICE_PREFIXES = ("# Today's work report", "Coordinator:", "Coordinator test:")


class ClickUpError(Exception):
    pass


class Budget:
    calls = 0


def call(method, path, body=None):
    """One API call with rate-limit waits and retries. Raises ClickUpError on a final failure."""
    token = os.environ.get("CLICKUP_API_TOKEN")
    if not token:
        raise ClickUpError(
            "CLICKUP_API_TOKEN is not set in this workspace's environment"
        )
    data = json.dumps(body).encode() if body is not None else None
    # Only a read is retried after an error: ClickUp may already have taken a POST, and a second one would send
    # the same message twice. A 429 is safe to retry for both, because ClickUp refused the call.
    retries = 3 if method == "GET" else 0
    for attempt in range(6):
        req = urllib.request.Request(
            f"{API}{path}",
            method=method,
            data=data,
            headers={"Authorization": token, "Content-Type": "application/json"},
        )
        try:
            Budget.calls += 1
            with urllib.request.urlopen(req, timeout=60) as r:
                if r.headers.get("X-RateLimit-Remaining") == "0":
                    wait_for_reset(r.headers.get("X-RateLimit-Reset"))
                return json.loads(r.read() or b"null")
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait_for_reset(e.headers.get("X-RateLimit-Reset"))
                continue
            if e.code >= 500 and attempt < retries:
                time.sleep(2 ** (attempt + 1))
                continue
            raise ClickUpError(f"{method} {path.split('?')[0]}: HTTP {e.code}") from e
        except (
            urllib.error.URLError,
            OSError,
            http.client.HTTPException,
            ValueError,
        ) as e:
            # Connection drops, a body that stalls past the timeout, or a body that is not JSON.
            if attempt < retries:
                time.sleep(2 ** (attempt + 1))
                continue
            raise ClickUpError(
                f"{method} {path.split('?')[0]}: {getattr(e, 'reason', None) or type(e).__name__}"
            ) from e
    raise ClickUpError(
        f"{method} {path.split('?')[0]}: still rate limited after retries"
    )


def wait_for_reset(reset):
    try:
        delay = int(reset) - time.time() + 1
    except (TypeError, ValueError):
        delay = 60
    time.sleep(min(max(delay, 1), 65))


def finished(task):
    return bool(task.get("date_closed")) or (task.get("status") or {}).get("type") in (
        "done",
        "closed",
    )


def iso(ms):
    try:
        return datetime.fromtimestamp(int(ms) / 1000, timezone.utc).isoformat()
    except (TypeError, ValueError):
        return ""


def me_and_workspaces():
    me = call("GET", "/v2/user")["user"]["id"]
    ws = os.environ.get("CLICKUP_WORKSPACE_ID")
    teams = [ws] if ws else [t["id"] for t in call("GET", "/v2/team")["teams"]]
    return me, teams


def member_names(team):
    """{user id: name} for the workspace's members, so chat lines name the sender."""
    for t in call("GET", "/v2/team").get("teams", []):
        if str(t["id"]) == str(team):
            return {
                str(m["user"]["id"]): m["user"].get("username")
                or m["user"].get("email")
                for m in t.get("members", [])
                if m.get("user")
            }
    return {}


def sweep(team, query):
    tasks = []
    for page in range(MAX_TASK_PAGES):
        res = call("GET", f"/v2/team/{team}/task?{query}&page={page}")
        got = res.get("tasks", [])
        tasks += got
        # The API's own last_page flag decides; a short page counts as the last only if the flag is absent.
        if res.get("last_page", len(got) < 100):
            return tasks
    raise ClickUpError(f"more than {MAX_TASK_PAGES * 100} tasks in workspace {team}")


def comments_since(task_id, since_ms):
    """(comments newer than since, the first page). Newest first, 25 per page."""
    kept, first, query = [], None, ""
    while True:
        if Budget.calls >= Budget.comment_cap:
            raise ClickUpError(
                f"more than {MAX_COMMENT_CALLS} comment reads in one run"
            )
        page = call("GET", f"/v2/task/{task_id}/comment{query}").get("comments", [])
        first = page if first is None else first
        fresh = [c for c in page if int(c["date"]) > since_ms]
        kept += fresh
        if len(page) < 25 or len(fresh) < len(page):
            return kept, first
        query = f"?start={page[-1]['date']}&start_id={page[-1]['id']}"


def comment_record(c, me):
    tags = [
        p.get("user", {}).get("id")
        for p in c.get("comment") or []
        if p.get("type") == "tag"
    ]
    return {
        "id": c["id"],
        "date": iso(c["date"]),
        "from": (c.get("user") or {}).get("username"),
        "text": (c.get("comment_text") or "")[:2000],
        "mentions_you": me in tags,
        "assigned_to_you": ((c.get("assignee") or {}).get("id")) == me,
        "reply_count": c.get("reply_count", 0),
    }


REPLY_THREADS_CHECKED = 10


def read_comments(task_ids, since_ms, me):
    """{task_id: {"comments": [...]}} for each task id: comments since the report, and new replies on any of the
    task's latest threads (a reply can land under an older comment). Only tasks updated since the report are
    read, because a new comment or reply moves the task's updated time (VERIFIED live 2026-10-30, 8 of 8)."""
    out = {}
    Budget.comment_cap = Budget.calls + MAX_COMMENT_CALLS
    for tid in task_ids:
        kept, first = comments_since(tid, since_ms)
        recs = {c["id"]: comment_record(c, me) for c in kept}
        for c in [c for c in first if c.get("reply_count")][:REPLY_THREADS_CHECKED]:
            replies = [
                comment_record(r, me)
                for r in call("GET", f"/v2/comment/{c['id']}/reply").get("comments", [])
                if int(r["date"]) > since_ms
            ]
            if replies:
                rec = recs.setdefault(
                    c["id"], dict(comment_record(c, me), older_comment=True)
                )
                rec["replies"] = replies
        out[tid] = {"comments": sorted(recs.values(), key=lambda r: r["date"])}
    return out


def read_chat(team, since_ms, me):
    """Messages since the report from others in Clay's DMs and group DMs, and channel messages tagging him."""
    tag = f"#user_mention#{me}"
    found, cursor = [], ""
    while True:
        res = call(
            "GET",
            f"/v3/workspaces/{team}/chat/channels?limit=100&with_message_since={since_ms}{cursor}",
        )
        for ch in res.get("data", []):
            found += read_channel(team, ch, since_ms, me, tag)
        nxt = res.get("next_cursor")
        if not nxt:
            return sorted(found, key=lambda m: m["date"])
        cursor = f"&cursor={nxt}"


def read_channel(team, ch, since_ms, me, tag):
    kept, cursor = [], ""
    direct = ch.get("type") in ("DM", "GROUP_DM")
    while True:
        res = call(
            "GET",
            f"/v3/workspaces/{team}/chat/channels/{ch['id']}/messages?limit=100{cursor}",
        )
        msgs = res.get("data", [])
        for m in msgs:
            if int(m.get("date", 0)) <= since_ms or str(m.get("user_id")) == str(me):
                continue
            content = m.get("content") or ""
            if direct or tag in content:
                rec = {
                    "channel": ch["id"],
                    "channel_type": ch.get("type"),
                    "from_user_id": m.get("user_id"),
                    "date": iso(m["date"]),
                    "text": content[:2000],
                    "mentions_you": tag in content,
                    "github_links": sorted(set(GITHUB_URL.findall(content))),
                }
                if m.get("replies_count"):
                    reps = call(
                        "GET",
                        f"/v3/workspaces/{team}/chat/messages/{m['id']}/replies?limit=100",
                    ).get("data", [])
                    rec["replies"] = [
                        {
                            "from_user_id": r.get("user_id"),
                            "date": iso(r["date"]),
                            "text": (r.get("content") or "")[:1000],
                        }
                        for r in reps
                        if int(r.get("date", 0)) > since_ms
                    ]
                kept.append(rec)
        nxt = res.get("next_cursor")
        if not msgs or not nxt or int(msgs[-1].get("date", 0)) <= since_ms:
            return kept
        cursor = f"&cursor={nxt}"


def field_links(task):
    text = " ".join(str(task.get(k) or "") for k in ("text_content", "description"))
    for f in task.get("custom_fields") or []:
        if f.get("type") in ("url", "short_text", "text") and f.get("value"):
            text += " " + str(f["value"])
    return set(GITHUB_URL.findall(text))


def hierarchy(task, names):
    parts = []
    for key, label in (("top_level_parent", "Top task"), ("parent", "Parent task")):
        pid = task.get(key)
        if pid and not (key == "top_level_parent" and pid == task.get("parent")):
            parts.append(f"{label}: {names.get(pid, pid)}")
    for f in task.get("custom_fields") or []:
        if f.get("type") == "tasks" and f.get("value"):
            parts.append(
                f"{f.get('name')}: "
                + ", ".join(v.get("name") or v.get("id", "") for v in f["value"])
            )
    return parts


def normalize(task, me, names, spaces, ctx):
    def who(u):
        return (
            CONFIG["person"]
            if (u or {}).get("id") == me
            else ((u or {}).get("username") or (u or {}).get("email"))
        )

    prio = task.get("priority")
    prio = prio.get("priority") if isinstance(prio, dict) else prio
    tid = task["id"]
    deps = task.get("dependencies") or []
    c = ctx["comments"].get(tid, {})
    links = field_links(task) | {
        u for cm in c.get("comments", []) for u in GITHUB_URL.findall(cm["text"])
    }
    status = (task.get("status") or {}).get("status")
    return {
        "source": "clickup",
        "org": "ClickUp",
        "repo": (task.get("list") or {}).get("name", "ClickUp"),
        "kind": "task",
        "number": tid,
        "title": task.get("name", ""),
        "url": task.get("url") or f"https://app.clickup.com/t/{tid}",
        "author": who(task.get("creator")),
        "assignees": sorted(
            filter(None, (who(u) for u in task.get("assignees") or []))
        ),
        "labels": sorted(t.get("name", "") for t in task.get("tags") or []),
        "created": iso(task.get("date_created")),
        "updated": iso(task.get("date_updated")),
        "comments": 0,
        "draft": None,
        "review_requests": [],
        "closes": [],
        "involves_person": tid in ctx["watched"] or tid in ctx["mentioned"],
        "boards": [
            {
                "board": "ClickUp status",
                "status": status,
                "priority": PRIORITY.get(prio),
            }
        ],
        "location": " / ".join(
            filter(
                None,
                [
                    spaces.get((task.get("space") or {}).get("id")),
                    (task.get("folder") or {}).get("name")
                    if not (task.get("folder") or {}).get("hidden")
                    else None,
                    (task.get("list") or {}).get("name"),
                ],
            )
        ),
        "hierarchy": hierarchy(task, names),
        "waiting_on": sorted(
            names.get(d["depends_on"], d["depends_on"])
            for d in deps
            if d.get("task_id") == tid
        ),
        "blocking": sorted(
            names.get(d["task_id"], d["task_id"])
            for d in deps
            if d.get("depends_on") == tid
        ),
        "github_links": sorted(links),
        "mentions_you": tid in ctx["mentioned"],
    }


def since_ms(run):
    prev = read_json(run / "run.json", {}).get("previous_completed_run")
    started = (
        read_json(run.parent / prev / "run.json", {}).get("started") if prev else None
    )
    if started:
        return int(datetime.fromisoformat(started).timestamp() * 1000) - OVERLAP_MS
    return int((time.time() - FIRST_RUN_DAYS * 86400) * 1000)


def previous_snapshot(run):
    prev = read_json(run / "run.json", {}).get("previous_completed_run")
    return read_json(run.parent / prev / "snapshot.json", {}) if prev else {}


def main(run):
    run = Path(run)
    Budget.calls, Budget.comment_cap = 0, MAX_COMMENT_CALLS
    status = {"read": False, "parts": {}}
    try:
        me, teams = me_and_workspaces()
    except (ClickUpError, KeyError) as e:
        write_json(run / "clickup-status.json", {"read": False, "reason": str(e)})
        print(f"ClickUp not read: {e}")
        return
    since = since_ms(run)
    items, events, gone, still_open, quiet_urls = (
        [],
        {"comments": {}, "chat": []},
        {},
        set(),
        set(),
    )
    try:
        for team in teams:
            # A status of type "done" (done, complete, won't fix...) is finished work even though the API
            # still calls it open (VERIFIED live 2026-10-30: 448 "done" tasks came back as open).
            open_tasks = [
                t
                for t in sweep(team, "include_closed=false&subtasks=true")
                if not finished(t)
            ]
            still_open |= {
                t.get("url") or f"https://app.clickup.com/t/{t['id']}"
                for t in open_tasks
            }
            updated = sweep(
                team, f"include_closed=true&subtasks=true&date_updated_gt={since}"
            )
            names = {t["id"]: t.get("name", "") for t in open_tasks + updated}
            spaces = {
                s["id"]: s.get("name")
                for s in call("GET", f"/v2/team/{team}/space?archived=false").get(
                    "spaces", []
                )
            }
            ids_of = lambda pred: {t["id"] for t in open_tasks if pred(t)}  # noqa: E731
            assigned = ids_of(
                lambda t: any(a.get("id") == me for a in t.get("assignees") or [])
            )
            created = ids_of(
                lambda t: (
                    (t.get("creator") or {}).get("id") == me and not t.get("assignees")
                )
            )
            watched_all = (
                ids_of(
                    lambda t: any(w.get("id") == me for w in t.get("watchers") or [])
                )
                - assigned
                - created
            )
            updated_open = {t["id"] for t in updated if not finished(t)}
            mine = assigned | created
            to_read = sorted(updated_open)
            comments = read_comments(to_read, since, me)
            mentioned = {
                tid
                for tid, c in comments.items()
                if any(
                    cm["mentions_you"]
                    or cm["assigned_to_you"]
                    or any(r["mentions_you"] for r in cm.get("replies", []))
                    for cm in c["comments"]
                )
            }
            watched = watched_all & (updated_open | mentioned)
            # A task is Clay's work only if something happened on it in the last ACTIVE_DAYS; the rest is a
            # count (CLAY, 2026-11-03: 472 of 476 open tasks had sat untouched for over 30 days).
            cutoff = int((time.time() - ACTIVE_DAYS * 86400) * 1000)
            quiet = {
                t["id"]
                for t in open_tasks
                if t["id"] in mine and int(t.get("date_updated") or 0) < cutoff
            }
            keep = (
                (mine - quiet) | watched | (mentioned & {t["id"] for t in open_tasks})
            )
            status["parts"]["quiet"] = {"count": len(quiet - keep), "days": ACTIVE_DAYS}
            quiet_urls |= {
                t.get("url") or f"https://app.clickup.com/t/{t['id']}"
                for t in open_tasks
                if t["id"] in quiet - keep
            }
            ctx = {"comments": comments, "watched": watched, "mentioned": mentioned}
            by_id = {t["id"]: t for t in open_tasks}
            for tid in sorted(keep):
                items.append(normalize(by_id[tid], me, names, spaces, ctx))
                if comments.get(tid, {}).get("comments"):
                    events["comments"][items[-1]["url"]] = comments[tid]["comments"]
            for t in updated:
                url = t.get("url") or f"https://app.clickup.com/t/{t['id']}"
                if t["id"] in keep:
                    continue
                if finished(t):
                    when = iso(t.get("date_closed") or t.get("date_done"))[:10]
                    gone[url] = (
                        f"marked {(t.get('status') or {}).get('status')} {when}".strip()
                    )
                else:
                    others = [a.get("username") for a in t.get("assignees") or []]
                    gone[url] = (
                        "reassigned to " + ", ".join(filter(None, others))
                        if others
                        else "no longer assigned to you"
                    )
            status["parts"]["tasks"] = {
                "open_visible": len(open_tasks),
                "updated_since": len(updated),
                "yours": len(keep),
            }
            try:
                people = member_names(team)
                for m in read_chat(team, since, me):
                    m["from"] = people.get(
                        str(m["from_user_id"]), f"user {m['from_user_id']}"
                    )
                    for r in m.get("replies", []):
                        r["from"] = people.get(
                            str(r["from_user_id"]), f"user {r['from_user_id']}"
                        )
                    events["chat"].append(m)
                status["parts"]["chat"] = {
                    "read": True,
                    "messages": len(events["chat"]),
                }
            except (ClickUpError, KeyError) as e:
                status["parts"]["chat"] = {"read": False, "reason": str(e)}
    except (ClickUpError, KeyError) as e:
        write_json(
            run / "clickup-status.json",
            {"read": False, "reason": str(e), "calls": Budget.calls},
        )
        print(f"ClickUp not read: {e}")
        return
    snap = previous_snapshot(run)
    for url, s in snap.items():
        if (
            s.get("source") == "clickup"
            and url not in {i["url"] for i in items}
            and url not in gone
        ):
            # A task is listed only while something happens on it.
            gone[url] = (
                f"{QUIET_REASON} {ACTIVE_DAYS} days"
                if url in quiet_urls
                else "still open, but you only watch it and nothing new happened on it"
                if url in still_open
                else "no longer open or visible to you in ClickUp"
            )
    items.sort(key=lambda i: i["url"])
    write_json(run / "clickup-items.json", items)
    write_json(run / "clickup-events.json", events)
    write_json(run / "clickup-gone.json", gone)
    replies, status["parts"]["replies"] = read_replies(teams, since, run)
    status.update(
        read=True, workspaces=len(teams), calls=Budget.calls, since=iso(since)
    )
    write_json(run / "clickup-status.json", status)
    s = read_json(state_dir() / "settings.json", {})
    if s.get("clickup_user_id") != str(me):
        write_json(
            state_dir() / "settings.json",
            dict(s, clickup_user_id=str(me), clickup_workspaces=teams),
        )
    print(
        f"{len(items)} ClickUp tasks are yours; {sum(len(v) for v in events['comments'].values())} new comments; "
        f"{len(events['chat'])} chat messages to you; {len(gone)} left your list; {replies} DM replies; {Budget.calls} calls"
    )


def read_replies(teams, since, run):
    """Clay's own messages in the helper's self DM since the previous report, minus the helper's notices.
    Always writes a list; returns (count, read status)."""
    cid = read_json(state_dir() / "settings.json", {}).get("clickup_dm_channel")
    write_json(run / "clickup-replies.json", [])
    if not cid:
        return 0, {"read": True, "reason": "no DM sent yet"}
    try:
        res = call(
            "GET", f"/v3/workspaces/{teams[0]}/chat/channels/{cid}/messages?limit=100"
        )
    except ClickUpError as e:
        return 0, {"read": False, "reason": str(e)}
    msgs = [
        m
        for m in (res.get("data") or [])
        if int(m.get("date", 0)) > since
        and not str(m.get("content", "")).startswith(NOTICE_PREFIXES)
    ]
    write_json(
        run / "clickup-replies.json",
        [{"time": iso(m.get("date")), "text": m.get("content")} for m in msgs],
    )
    return len(msgs), {"read": True}


def send_dm(text):
    """Send text to the token owner's self DM (VERIFIED live 2026-10-30). Returns (sent, channel id or reason)."""
    try:
        _, teams = me_and_workspaces()
        # No user ids creates (or returns) the self DM, per the ClickUp docs.
        ch = call("POST", f"/v3/workspaces/{teams[0]}/chat/channels/direct_message", {})
        cid = (ch.get("data") or ch).get("id")
        call(
            "POST",
            f"/v3/workspaces/{teams[0]}/chat/channels/{cid}/messages",
            {"type": "message", "content": text, "content_format": "text/md"},
        )
    except (ClickUpError, KeyError, IndexError, AttributeError) as e:
        return False, str(e)
    s = read_json(state_dir() / "settings.json", {})
    if s.get("clickup_dm_channel") != cid:
        write_json(state_dir() / "settings.json", dict(s, clickup_dm_channel=cid))
    return True, cid


def dm(run, message_file):
    import run as runmod  # the run lock module; imported here because it is only needed to deliver

    ok, why = runmod.deliverable(run)
    if ok and Path(message_file).resolve() != (Path(run) / "summary.md").resolve():
        ok, why = False, "only the run's own summary.md is ever sent"
    if (
        not ok
    ):  # a report that has not passed its checks never reaches Clay (Clay, 2026-11-03)
        write_json(
            Path(run) / "clickup-dm.json", {"sent": False, "detail": f"blocked: {why}"}
        )
        sys.exit(f"DM not sent: blocked: {why}")
    sent, detail = send_dm(Path(message_file).read_text())
    write_json(Path(run) / "clickup-dm.json", {"sent": sent, "detail": detail})
    print("DM sent" if sent else f"DM not sent: {detail}")
    sys.exit(0 if sent else 1)


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) == 1:
        main(a[0])
    elif len(a) == 3 and a[0] == "dm":
        dm(a[1], a[2])
    else:
        sys.exit(__doc__)
