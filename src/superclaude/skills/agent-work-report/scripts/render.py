#!/usr/bin/env python3
"""Stub the overview from its template: script facts in fixed lines, short slots for the model.

usage: render.py <run_folder>

Every item gets a title line and one facts line (link, why it is Clay's, board status, what changed), plus a
line per ClickUp task and agent session on it. An item new or changed since the previous report, or with no
notes yet, also gets the four note slots the page shows (State, What it is, Now, Next; listed in
`to-write.json`); every other item keeps its last notes from the previous run's notes.json. This overview is
the writing sheet; Clay reads the page that page.py builds from it. Slots left for the model: "Needs you",
each note, each changed session's status, "Likely yours".
Refuses to overwrite an overview that already exists (stub once, then populate in place).
"""

import re
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from common import (
    CONFIG,
    DASHES,
    NOT_ASKED,
    QUIET_REASON,
    SESSION_URL,
    SKILL_DIR,
    SUGGESTED,
    UPDATE_MARK,
    WRITTEN,
    answered_since,
    blocks,
    local_time,
    needs_link,
    previous_notes,
    read_json,
    report_days_between,
    section,
    session_statuses,
    to_write,
    write_json,
)

GROUP_TITLES = {
    "assigned": "assigned to you",
    "owned": "yours without assignment",
    "opened": "opened by you, nobody assigned",
}
LISTED = set(GROUP_TITLES) | {"inprogress"}
PRIORITY_ORDER = ["Urgent", "High", "Medium", "Low", "Unset"]
DEAD = "(dead link)"
CARRIED_NEEDS_YOU = "*Carried from the previous report: not answered yet.*"
CARRIED_NOTE = " (kept as it was: sessions not read this run)"
FIELD_NAMES = {
    "clickup_tasks": "ClickUp task",
    "agent_sessions": "agent session",
    "board_status": "board status",
}


def key(url):
    if url.startswith("orca://session/"):
        return "session-" + url.rsplit("/", 1)[1]
    if "app.clickup.com/t/" in url:
        return "clickup-task-" + url.rstrip("/").rsplit("/", 1)[1]
    org, repo, kind, n = url.replace("https://github.com/", "").split("/")[:4]
    return f"{org}-{repo}-{'pr' if kind == 'pull' else 'issue'}-{n}"


def short(url):
    if url.startswith("orca://session/"):
        return "agent session " + url.rsplit("/", 1)[1][:8]
    if "app.clickup.com/t/" in url:
        return "ClickUp task " + url.rstrip("/").rsplit("/", 1)[1]
    org, repo, kind, n = url.replace("https://github.com/", "").split("/")[:4]
    return f"{repo} {'pull request' if kind == 'pull' else 'issue'} #{n}"


def plain(v):
    """A compared value in words: a list as its items, nothing as "none"."""
    if isinstance(v, list):
        return ", ".join(str(x) for x in v) or "none"
    return "none" if v in (None, "") else str(v)


def change_note(url, cmp_):
    if url in cmp_["new"]:
        return "new" if cmp_["previous_run"] else "first report"
    if url in cmp_["changed"]:
        parts = []
        for f, d in sorted(cmp_["changed"][url].items()):
            if f in ("clickup_tasks", "agent_sessions"):
                parts.append(f"{FIELD_NAMES[f]} activity")
            elif f not in ("updated", "comments"):
                parts.append(
                    f"{FIELD_NAMES.get(f, f.replace('_', ' '))} {plain(d['was'])} to {plain(d['now'])}"
                )
            elif f == "comments":
                parts.append(
                    f"{d['now'] - (d['was'] or 0)} new comments"
                    if isinstance(d["now"], int)
                    else "new comments"
                )
        return "changed: " + ("; ".join(parts) or "new activity")
    if url in cmp_["carried"]:
        return "carried: its source was not read this run"
    return "no change"


def clickup_line(t):
    extra = [f"in {t['location']}"] if t.get("location") else []
    if t.get("waiting_on"):
        extra.append("waiting on " + ", ".join(t["waiting_on"]))
    if t.get("carried"):
        extra.append("carried: ClickUp not read this run")
    return (
        f"  - [{t['title']}]({t['url']}) · {t['boards'][0]['status']} · "
        + " · ".join(extra + [f"updated {local_time(t['updated'])[:10]}"])
    )


def session_line(s, status):
    return (
        f"  - [{s['title']}]({s['url']}) · branch {s['branch'] or 'none'} · "
        f"{'running' if s['claude_running'] else 'not running'} · last activity {local_time(s['last_event'])} · "
        f"status: {status}"
    )


def item_template():
    """The item template's body (after its <!-- ITEM --> line), without its comments."""
    body = (
        (SKILL_DIR / "templates" / "item-template.md")
        .read_text()
        .split("<!-- ITEM -->\n", 1)[1]
    )
    return re.sub(r"[ \t]*<!--.*?-->[ \t]*\n", "", body, flags=re.S)


MULTI = (
    "done",
    "todo",
    "happened",
)  # written as bullets on the lines under their label


def priority_why(c):
    """Where the priority came from, as a sentence (classify.py names the source)."""
    level, src = c["priority"], c.get("priority_source", "")
    if level == "Unset":
        return "None is set on GitHub, a Projects board or ClickUp, and you have not set one."
    if src.startswith("board ClickUp status"):  # a ClickUp task's own priority field
        rest = src.removeprefix("board ClickUp status").removeprefix(" of ")
        where = "the ClickUp task's priority" + (f" ({rest})" if rest else "")
    elif src.startswith("board "):
        where = (
            "the Priority field on the "
            + src.removeprefix("board ").replace(" of ", " board, on ", 1)
            + ("" if " of " in src else " board")
        )
    elif src.startswith("set by "):
        where = "what you told the helper" + (
            f" ({src.split(': ', 1)[1]})" if ": " in src else ""
        )
    else:
        where = src.removeprefix("from ")
    return f"{level}, from {where}."


def carried_status(prev, s):
    """An unchanged session: nothing happened in it, so "waiting on you" and "done" stay, the rest is stalled."""
    if prev and (prev.startswith("waiting on you") or prev.startswith("done")):
        return prev
    return f"stalled: no activity after {local_time(s.get('last_event'))}, and its work is not reported done"


def filed_orchestrator(filed):
    """The ` · **Orchestrator:** ...` part of the item's header line for an entry file (5.4, 5.7 point 6)."""
    orch = filed.get("orchestrator") or {}
    name = orch.get("tag") or orch.get("id")
    if not name:
        return " · **Orchestrator:** none recorded"
    link = orch.get("link") or (
        f"orca://session/{orch['session_id']}" if orch.get("session_id") else ""
    )
    who = f"[{name}]({link})" if link else name
    return f" · **Orchestrator:** {who}" + (
        f" ({orch['tier']})" if orch.get("tier") else ""
    )


def entry(url, it, c, cmp_, ctx, filed=None):
    """One item from templates/item-template.md. Its written parts: empty slots for a new or never-written
    item; yesterday's text plus an update marker for a changed one (each part is updated, not rewritten
    from nothing); yesterday's text for an unchanged one, with "nothing since" as what happened.

    With `filed` (the orchestrator's entry file for the issue, called by `run.py refresh`) every written part,
    `happened` and each session's `<status>: <reason>` come from that file: no slot is left for the model, no
    update marker is added, "Nothing since the previous report" is never printed and `carried_status` never
    replaces a status (it turns every status but waiting on you and done into stalled). A part the file lacks
    is "N/A". An escalation of such an issue is lines of its own "Needs you" part, never a heading of its own."""
    boards = (
        ", ".join(
            f"{b['board']}: {b['status']}"
            for b in it.get("boards", [])
            if b.get("status")
        )
        or "Not on a board"
    )
    fresh = url in cmp_["new"] or url in cmp_["changed"]
    k = key(url)
    prev = ctx["notes"].get(url, {})
    slot = lambda s: f"{{{{RF_PLACEHOLDER:{s}:{k}}}}}"  # noqa: E731
    sessions = []
    if filed is not None:
        written = {
            s: filed.get(s) or ("- N/A" if s in MULTI else "N/A") for s in WRITTEN
        }
        statuses = filed.get("session_status") or {}
        for s in it.get("sessions", []):
            status = (
                statuses.get(s["session_id"])
                or "stalled: the entry file has no status for this session"
            )
            sessions.append(session_line(s, status))
    else:
        written = {s: (prev.get(s) or slot(s)) for s in WRITTEN}
        if url in ctx["to_write"]:
            written["happened"] = slot("happened")
        else:
            written["happened"] = (
                "- Its source was not read this run, so this is the last report's text."
                if url in cmp_["carried"]
                else f"- Nothing since the previous report ({ctx['prev_date']})."
            )
        for s in it.get("sessions", []):
            sid = s["session_id"]
            if s.get("carried"):  # sessions not read: keep the last status as it was
                status = (
                    ctx["statuses"].get(sid) or "stalled: no status recorded yet"
                ).replace(CARRIED_NOTE, "") + CARRIED_NOTE
            elif fresh:
                status = f"{{{{RF_PLACEHOLDER:status:{sid}}}}}"
            else:
                status = carried_status(ctx["statuses"].get(sid), s)
            sessions.append(session_line(s, status))
    if c["priority"] == "Unset":
        # the priority protocol: nothing set one, so a suggestion stands (the model's, kept daily; for an
        # entry file the orchestrator's)
        if filed is not None:
            level = SUGGESTED + (filed.get("suggested") or "N/A")
            why = filed.get("priority_why") or "N/A"
        else:
            level, why = (
                SUGGESTED + (prev.get("suggested") or slot("suggested")),
                prev.get("priority_why") or slot("priority_why"),
            )
    elif filed is not None and filed.get("priority_why"):
        level, why = c["priority"], filed["priority_why"]
    else:
        level, why = c["priority"], priority_why(c)
    fills = {
        "identifier_link": f"[{short(url)}]({url})",
        "title": it["title"],
        "priority": level,
        "change": change_note(url, cmp_),
        "author": it.get("author") or "Unknown",
        "assignees": ", ".join(it.get("assignees") or []) or "Nobody",
        "owner": f"You ({c.get('why') or GROUP_TITLES.get(c['group'], 'yours')})",
        "board": boards,
        "clickup_links": "\n" + "\n".join(clickup_line(t) for t in it["clickup"])
        if it.get("clickup")
        else "N/A",
        "session_lines": "\n" + "\n".join(sessions) if sessions else "N/A",
        "priority_why": why,
        "orchestrator_part": filed_orchestrator(filed) if filed is not None else "",
    }
    text = ctx["template"]
    for name, value in fills.items():
        text = text.replace("{{" + name + "}}", value)
    for name, value in written.items():
        if name in MULTI:  # bullets under the label, indented
            value = "\n".join(
                "  " + ln if ln.strip() else ln for ln in value.splitlines()
            )
            text = text.replace("  {{RF_PLACEHOLDER:" + name + "}}", value)
        elif (
            filed is not None
        ):  # a part of several lines keeps its lines under its label
            value = value.strip("\n").replace("\n", "\n  ")
        text = text.replace("{{RF_PLACEHOLDER:" + name + "}}", value)
    if fresh and prev and filed is None:
        text = text.rstrip("\n") + (
            f"\n{UPDATE_MARK} changed since the previous report ({change_note(url, cmp_)}): update every"
            " part above from activity.md, keep what is still true, then delete this line -->\n"
        )
    return text.rstrip("\n") + "\n"


def missed(run_meta, tz):
    prev = run_meta.get("previous_completed_run")
    notes = []
    if run_meta.get("stuck_run_replaced"):
        notes.append(
            f"**Stuck run replaced:** {run_meta['stuck_run_replaced']['run']} never finished."
        )
    if prev:
        last = (
            datetime.strptime(prev[:16], "%Y%m%dT%H%M%SZ")
            .replace(tzinfo=ZoneInfo("UTC"))
            .astimezone(tz)
            .date()
        )
        today = datetime.fromisoformat(run_meta["started"]).astimezone(tz).date()
        gap = report_days_between(
            last, today
        )  # weekends are not report days, so they are never "missed"
        if gap:
            notes.append(
                f"**Missed reports:** no report on {', '.join(f'{d:%a %Y-%m-%d}' for d in gap)}."
            )
    return "\n".join(notes)


def still_waiting(prev_text, since, closed, held=()):
    """Previous "Needs you" entries (### blocks) led by an agent session, with no recorded answer since and the
    session still open. An entry led by anything else is not carried: "Needs you" holds only sessions waiting
    on Clay (CLAY, 2026-11-05), and that ask stays in its item's own "Needs you" part. An entry led by a
    session the orchestrator now holds (`held`, from exclude.py) is not carried either: the coordinator's list
    holds only what belongs to no orchestrated issue, and that issue's escalation lines live in its own entry.

    Returns (blocks kept, urls dropped because their item closed)."""
    done = answered_since(since)
    keep, dropped = [], []
    for b in blocks(section(prev_text, "Needs you"), 3):
        u = needs_link(b)
        if u in closed:
            dropped.append(u)
        elif u in held:
            continue
        elif u.startswith(SESSION_URL) and u not in done:
            keep.append(
                f"{b.replace(CARRIED_NEEDS_YOU, '').strip()}\n{CARRIED_NEEDS_YOU}\n"
            )
    return keep, dropped


def not_checked_lines(cov, cu, ses, autoruns, incomplete):
    repos = [r for r in cov["repos"] if not r.get("archived")]
    out = [
        f"- {r['org']}/{r['repo']}: {'; '.join(r['errors'])}"
        for r in repos
        if r["errors"]
    ]
    out += [f"- {e}" for e in cov["source_errors"]]
    if not cu["read"]:
        out.append(f"- ClickUp: not read ({cu['reason']})")
    else:
        for part, name in (
            ("chat", "ClickUp chat"),
            ("replies", "your ClickUp DM replies"),
        ):
            if not cu.get("parts", {}).get(part, {}).get("read", True):
                out.append(f"- {name}: not read ({cu['parts'][part].get('reason')})")
    if not ses["read"]:
        out.append(
            f"- Agent sessions in Orca: not read ({ses['reason']}); each item keeps its sessions from the previous report"
        )
    out += [f"- Agent session {m}" for m in ses.get("missing", [])]
    if not autoruns.get("read", True):
        out.append(
            f"- Orca automation run history: not copied ({autoruns.get('reason')})"
        )
    if incomplete:
        out.append(f"- Earlier runs that did not finish: {', '.join(incomplete)}")
    disabled = [
        f"{r['org']}/{r['repo']}" for r in repos if not r.get("issues_enabled", True)
    ]
    if disabled:
        out.append(
            f"- Issues are switched off in {len(disabled)} repos (pull requests still read): {', '.join(disabled)}"
        )
    return out + [f"- {NOT_ASKED}"]


def main(run):
    run = Path(run)
    out = run / "overview.md"
    if out.exists():
        sys.exit(f"{out} already exists; populate it in place")
    tz = ZoneInfo(CONFIG["timezone"])
    meta = read_json(run / "run.json")
    cov = read_json(run / "coverage.json")
    items = {i["url"]: i for i in read_json(run / "items.json")}
    cls = read_json(run / "classified.json")
    cmp_ = read_json(run / "compare.json")
    snap = read_json(run / "snapshot.json", {})
    cu = read_json(
        run / "clickup-status.json",
        {"read": False, "reason": "the ClickUp step did not run"},
    )
    ses = read_json(
        run / "sessions-status.json",
        {"read": False, "reason": "the agent session step did not run"},
    )
    prev_dir = run.parent / cmp_["previous_run"] if cmp_["previous_run"] else None
    prev_text = (
        (prev_dir / "overview.md").read_text()
        if prev_dir and (prev_dir / "overview.md").exists()
        else ""
    )
    write_list = to_write(run)
    write_json(run / "to-write.json", write_list)
    prev_meta = read_json(prev_dir / "run.json", {}) if prev_dir else {}
    ctx = {
        "statuses": session_statuses(prev_text),
        "to_write": set(write_list),
        "notes": previous_notes(run),
        "template": item_template(),
        "prev_date": datetime.fromisoformat(prev_meta["started"])
        .astimezone(tz)
        .strftime("%Y-%m-%d")
        if prev_meta.get("started")
        else "none",
    }

    repos = [r for r in cov["repos"] if not r.get("archived")]
    read_ok = [r for r in repos if not r["errors"]]
    quiet = cu.get("parts", {}).get("quiet", {})
    sources = (
        f"GitHub {len(read_ok)} of {len(repos)} repos; {len(cov['boards'])} Projects boards; "
        f"ClickUp {'read' if cu['read'] else 'not read'}; "
        + (
            f"{ses['sessions']} agent sessions"
            if ses["read"]
            else "agent sessions not read"
        )
    )
    counts = cls["counts"]
    rows = [f"| {GROUP_TITLES[g].capitalize()} | {counts[g]} |" for g in GROUP_TITLES]
    rows.append(
        f"| Other work in progress (agent sessions on no item) | {counts['inprogress']} |"
    )
    rows.append(f"| Named you, judged below | {counts['candidate']} |")
    carried = [
        u
        for u in cmp_["carried"]
        if snap.get(u, {}).get("group") in LISTED and u not in items
    ]
    n_carried = sum(
        1
        for u in cmp_["carried"]
        if (cls["items"].get(u) or snap.get(u, {})).get("group") in LISTED
    )
    if n_carried:
        rows.append(f"| Carried, source not read | {n_carried} |")
    listed = [u for u in cls["order"] if cls["items"][u]["group"] in LISTED]

    def by_priority(urls, held):
        lines = []
        for level in PRIORITY_ORDER:
            live = [u for u in urls if cls["items"][u]["priority"] == level]
            kept = [u for u in held if snap[u].get("priority") == level]
            if live or kept:
                lines.append(f"### {level} ({len(live) + len(kept)})\n")
                got = [entry(u, items[u], cls["items"][u], cmp_, ctx) for u in live]
                for u in kept:  # carried by compare: shown from the previous snapshot
                    c = {
                        "priority": snap[u]["priority"],
                        "why": GROUP_TITLES.get(
                            snap[u]["group"], "other work in progress"
                        ),
                    }
                    got.append(entry(u, {"title": snap[u]["title"]}, c, cmp_, ctx))
                lines += [
                    e for e in got if e.startswith("#")
                ]  # full entries first, then the one-line ones together
                quiet = [e for e in got if not e.startswith("#")]
                if quiet:
                    lines.append("\n".join(quiet) + "\n")
        return lines

    work = by_priority(
        [u for u in listed if cls["items"][u]["group"] != "inprogress"],
        [u for u in carried if snap[u]["group"] != "inprogress"],
    )
    other = by_priority(
        [u for u in listed if cls["items"][u]["group"] == "inprogress"],
        [u for u in carried if snap[u]["group"] == "inprogress"],
    )

    kept_needs, dropped = [], []
    if prev_text:
        kept_needs, dropped = still_waiting(
            prev_text,
            read_json(prev_dir / "run.json", {}).get("started", ""),
            set(cmp_["closed"]),
            set(read_json(run / "excluded.json", [])),
        )
    closed, went_quiet = [], 0
    for u, v in sorted(cmp_["closed"].items()):
        if v["reason"].startswith(QUIET_REASON) and u not in dropped:
            went_quiet += 1
        elif v["group"] in LISTED or v["group"] == "candidate" or u in dropped:
            dead = f" {DEAD}" if v["reason"].startswith("no longer visible") else ""
            note = (
                "; its open Needs you question was dropped because the item closed"
                if u in dropped
                else ""
            )
            closed.append(f"- [{v['title']}]({u}){dead}: {v['reason']}{note}")
    old = read_json(prev_dir / "snapshot.json", {}) if prev_dir else {}
    for u in sorted(
        old
    ):  # still open, but no longer in Clay's groups: it leaves the list once, here
        now = cls["items"].get(u)
        if old[u].get("group") in LISTED and now and now["group"] not in LISTED:
            closed.append(
                f"- [{old[u]['title']}]({u}): no longer yours: now {now['group']}"
            )
    if went_quiet:
        closed.append(
            f"- {went_quiet} ClickUp tasks left the list: still open, but nothing happened on them in "
            f"{quiet.get('days', 30)} days (counted, not listed)."
        )

    how = [
        f"- Scripts read GitHub, ClickUp ({cu.get('calls', 0)} API calls) and your agent sessions' transcripts, "
        f"joined them into one item each, and compared with {cmp_['previous_run'] or 'nothing (first report)'}.",
        "- Priority comes from board fields, ClickUp priority, labels and anything you told the helper.",
    ]
    if quiet.get("count"):
        how.append(
            f"- {quiet['count']} more ClickUp tasks are assigned to or created by you but had no activity in "
            f"{quiet['days']} days, so they are not listed."
        )

    # "Needs you" is only agent sessions waiting on Clay (CLAY, 2026-11-05); notices about the helper itself (a
    # stuck run, two coordinator sessions) go in the header instead.
    needs = list(kept_needs)
    notices = missed(meta, tz)
    doubled = sorted(
        {
            h
            for w in read_json(run / "wake-records.json", [])
            for h in w.get("other_live_sessions") or []
        }
    )
    if doubled:
        notices += (
            f"\n**Two coordinator sessions are running:** the wake went to the newest; close the others in Orca "
            f"({', '.join(f'`{h}`' for h in doubled)})."
        )

    judge = [u for u in cls["order"] if cls["items"][u]["group"] == "candidate"]
    new = sum(1 for u in listed if u in cmp_["new"])
    changed = sum(1 for u in listed if u in cmp_["changed"])
    text = (SKILL_DIR / "templates" / "overview-template.md").read_text()
    fills = {
        "date": datetime.fromisoformat(meta["started"])
        .astimezone(tz)
        .strftime("%A %Y-%m-%d"),
        "run": meta["run"],
        "previous": cmp_["previous_run"] or "none (first report)",
        "sources": sources,
        "missed": notices.strip("\n"),
        "count_rows": "\n".join(rows),
        "change_counts": f"{new} new, {changed} changed, {len(closed)} closed or off your list.",
        "entries": "\n".join(work) or "Nothing open is yours.",
        "other_work": "\n".join(other) or "None.",
        "closed": "\n".join(closed) or "Nothing closed.",
        "not_checked": "\n".join(
            not_checked_lines(
                cov,
                cu,
                ses,
                read_json(run / "automation-runs.json", {}),
                read_json(run / "incomplete-runs.json", []),
            )
        )
        or "Every source was read.",
        "how": "\n".join(how),
    }
    for k, v in fills.items():
        text = text.replace("{{" + k + "}}", v)
    if needs:
        text = text.replace(
            "{{RF_PLACEHOLDER:needs_you}}",
            "\n".join(needs) + "\n{{RF_PLACEHOLDER:needs_you}}",
        )
    # Every line also ends with the item's priority, set or suggested (CLAY, 2026-11-17: nothing without one).
    todo = " ".join(
        f"{u} ({'priority set: ' + cls['items'][u]['priority'] if cls['items'][u]['priority'] != 'Unset' else 'none set: suggest one'})"
        for u in judge
    )
    text = text.replace(
        "{{RF_PLACEHOLDER:likely_yours}}",
        f"<!-- judge each, ending each line `Priority: <level> (set)` or `Priority: <level> (suggested)`: {todo} -->\n"
        "{{RF_PLACEHOLDER:likely_yours}}"
        if judge
        else "No other item names you.",
    )
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")
    text = DASHES.sub("-", text)  # titles copied from GitHub or ClickUp can hold dashes
    out.write_text(text)
    print(
        f"{out}: {len(listed) + len(carried)} items, {text.count('{{RF_PLACEHOLDER:')} slots for the model, "
        f"{len(text.splitlines())} lines"
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
