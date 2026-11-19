#!/usr/bin/env python3
"""Compare this run with the previous completed run: new, changed, closed, unchanged, carried.

usage: compare.py <run_folder> [<previous_run_folder>]

With no previous folder given, uses the latest completed run (run.py tracks it). Writes:
  snapshot.json  the fields compared next time, one entry per open item; items carried from a
                 source not read this run keep their previous entry, marked "carried": true
  compare.json   new, changed (with the fields that changed), closed (with the reason),
                 unchanged, and carried (open before, not confirmed closed this run)
The urls in excluded.json (exclude.py: held by the orchestrator, PR C) are dropped from the previous snapshot
first, so an excluded item is neither new, changed, carried nor closed.

An item open last time but not listed now is looked up directly. A GitHub item is closed only when
GitHub says it is closed or not found; any other lookup error carries it forward (FR-19). A ClickUp
task closes with clickup.py's reason; an agent session leaves only after a report called it done
(sessions.py keeps it until then); either one now listed under another item says so.
Items in a repo, org or source that failed to read are carried without a lookup.
"""

import sys
from pathlib import Path

from common import CommandError, gh_json, read_json, write_json
from run import latest_completed

TRACKED = [
    "title",
    "updated",
    "comments",
    "assignees",
    "labels",
    "draft",
    "board_status",
    "group",
    "priority",
    "clickup_tasks",
    "agent_sessions",
]
NOT_FOUND = ("HTTP 404", "HTTP 410", "Could not resolve to")


def snapshot(items, classified):
    snap = {}
    for it in items:
        c = classified["items"][it["url"]]
        snap[it["url"]] = {
            "title": it["title"],
            "updated": it["updated"],
            "comments": it.get("comments", 0),
            "assignees": it.get("assignees", []),
            "labels": it.get("labels", []),
            "draft": it.get("draft"),
            "board_status": sorted(
                f"{b['board']}: {b['status']}" for b in it.get("boards", [])
            ),
            "group": c["group"],
            "priority": c["priority"],
            "kind": it["kind"],
            "source": it.get("source", "github"),
            # ClickUp comments move a task's updated time, so status plus updated catches every change.
            "clickup_tasks": sorted(
                f"{t['url']} {t['boards'][0]['status']} {t['updated']}"
                for t in it.get("clickup", [])
            ),
            "agent_sessions": sorted(
                f"{s['url']} {s['events_total']} events, terminal "
                f"{'open' if s['terminal_open'] else 'closed'}"
                for s in it.get("sessions", [])
            ),
            "last_activity": max(
                [it["updated"] or ""]
                + [t["updated"] or "" for t in it.get("clickup", [])]
                + [s["last_event"] or "" for s in it.get("sessions", [])]
            ),
        }
        if it.get(
            "carried"
        ):  # match.py kept it from the previous report because its source was not read
            snap[it["url"]]["carried"] = True
    return snap


def lookup_closed(url):
    """Ask GitHub directly. Returns a close reason, or None to carry the item forward."""
    kind = "pr" if "/pull/" in url else "issue"
    try:
        x = gh_json(
            kind,
            "view",
            url,
            "--json",
            "state,closedAt" + (",mergedAt" if kind == "pr" else ""),
        )
    except CommandError as e:
        return (
            "no longer visible (not found on GitHub)"
            if any(s in str(e) for s in NOT_FOUND)
            else None
        )
    if x.get("state") == "OPEN":
        return None
    if x.get("mergedAt"):
        return f"merged {x['mergedAt'][:10]}"
    return f"closed {(x.get('closedAt') or '')[:10]}".strip()


def unread_prefixes(coverage):
    """URL prefixes whose items were not read this run: failed repos and failed orgs."""
    bad = {
        f"https://github.com/{c['org']}/{c['repo']}/"
        for c in coverage.get("repos", [])
        if c.get("errors")
    }
    for err in coverage.get("source_errors", []):
        if " repo list:" in err:
            bad.add(f"https://github.com/{err.split(' repo list:')[0]}/")
    return bad


def main(run, prev=None):
    run = Path(run)
    items = read_json(run / "items.json")
    classified = read_json(run / "classified.json")
    snap = snapshot(items, classified)
    prev = Path(prev) if prev else latest_completed(exclude=run)
    old = read_json(prev / "snapshot.json", {}) if prev else {}
    # What exclude.py left out of this run (the orchestrator holds it) is left out of the previous snapshot
    # too, so it is neither new, changed, carried nor closed here.
    excluded = set(read_json(run / "excluded.json", []))
    old = {u: v for u, v in old.items() if u not in excluded}
    unread = unread_prefixes(read_json(run / "coverage.json", {}))
    read = {
        "github": True,
        "clickup": read_json(run / "clickup-status.json", {}).get("read", False),
        "session": read_json(run / "sessions-status.json", {}).get("read", False),
    }
    merged = read_json(run / "merged-into.json", {})
    gone = read_json(run / "clickup-gone.json", {})
    result = {
        "previous_run": prev.name if prev else None,
        "new": [],
        "changed": {},
        "closed": {},
        "unchanged": [],
        "carried": [],
    }
    for url in sorted(snap):
        if url not in old:
            result["new"].append(url)
            continue
        # A field the previous snapshot did not have yet (added in a later version) is not a change.
        diff = [k for k in TRACKED if k in old[url] and old[url][k] != snap[url].get(k)]
        if diff:
            result["changed"][url] = {
                k: {"was": old[url].get(k), "now": snap[url].get(k)} for k in diff
            }
        elif not snap[url].get("carried"):
            result["unchanged"].append(url)
        if snap[url].get("carried"):
            result["carried"].append(url)
    for url in sorted(set(old) - set(snap)):
        source = old[url].get("source", "github")
        if url in merged:
            reason = f"now listed under {snap.get(merged[url], {}).get('title', merged[url])} ({merged[url]})"
        elif not read[source] or (
            source == "github" and any(url.startswith(p) for p in unread)
        ):
            reason = None
        elif source == "github":
            reason = lookup_closed(url)
        elif source == "clickup":
            reason = gone.get(url, "no longer open or visible to you in ClickUp")
        else:
            # sessions.py keeps every session until a report calls it done, so one missing from a read is done.
            reason = "its agent session's work was reported done"
        if reason is None:
            result["carried"].append(url)
            snap[url] = dict(old[url], carried=True)
        else:
            result["closed"][url] = {
                "reason": reason,
                "title": old[url]["title"],
                "group": old[url]["group"],
            }
    write_json(run / "snapshot.json", snap)
    write_json(run / "compare.json", result)
    print(
        f"vs {result['previous_run'] or 'no previous run'}: {len(result['new'])} new, {len(result['changed'])} changed, "
        f"{len(result['closed'])} closed, {len(result['unchanged'])} unchanged, {len(result['carried'])} carried"
    )


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        sys.exit(__doc__)
    main(*sys.argv[1:])
