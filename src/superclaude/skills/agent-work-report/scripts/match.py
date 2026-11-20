#!/usr/bin/env python3
"""Join GitHub items, ClickUp tasks and agent sessions into one item list, so nothing appears twice (FR-28).

usage: match.py <run_folder>

Reads github-items.json, clickup-items.json and sessions.json. Writes:
  items.json        every item once: each GitHub item, each ClickUp task that matched no GitHub item, and
                    each session that matched nothing. A matched ClickUp task or session is listed under
                    its item ("clickup", "sessions") with how it matched ("matched_by").
  merged-into.json  {ClickUp task or session URL: the item URL it is listed under}

Exact matches on ids seen in this run only, in this order:
  ClickUp task -> GitHub item: a GitHub URL in the task's text, link fields or comments; or the task's id in
                  a GitHub title, body or branch in ClickUp's link forms (collect.py's clickup_refs). A task
                  that matches several GitHub items is listed under the first by URL; the others are named.
  session -> item: the Orca workspace's linked pull request or issue; a pull request on the session's branch
                  (not a fork's, and not main, master, develop or dev);
                  an issue or pull request number at the start of a branch part ("412-fix", "feat/412-x");
                  a ClickUp id in the branch; else the one item named in the prompts it was given, if exactly
                  one, counting every report's prompts (an item it only looked up or mentioned does not count).
A source not read this run (ClickUp or sessions) keeps each item's tasks or sessions from the previous report,
and ClickUp not read keeps the previous report's ClickUp-only items, marked "carried", so sessions still join them.
A session that matches nothing becomes its own item, url orca://session/<id>, in "Other work in progress".
"""

import re
import sys
from pathlib import Path

from common import CONFIG, read_json, write_json

BRANCH_NUMBER = re.compile(r"(?:^|/)(?:issue-?|gh-?)?(\d{1,6})(?=[-_/]|$)")
# ClickUp's own branch names look like CU-<id>_<Task-Name>_<user>, so the id ends at any non-id character.
BRANCH_CU = re.compile(r"\bCU-([0-9a-z]+)(?![0-9a-z])", re.I)
GITHUB = "https://github.com/"
SHARED_BRANCHES = {"main", "master", "develop", "dev"}
# The fields of a ClickUp item that task_facts (the task as listed under a GitHub item) does not carry.
TASK_BASE = {
    "source": "clickup",
    "org": "ClickUp",
    "repo": "ClickUp",
    "kind": "task",
    "comments": 0,
    "draft": None,
    "review_requests": [],
    "closes": [],
    "involves_person": True,
}


def task_facts(t):
    return {
        k: t.get(k)
        for k in (
            "url",
            "number",
            "title",
            "assignees",
            "author",
            "boards",
            "location",
            "hierarchy",
            "waiting_on",
            "blocking",
            "updated",
            "created",
            "mentions_you",
            "labels",
            "github_links",
        )
    }


def session_facts(s, how):
    f = s["since_previous_report"]
    return {
        "session_id": s["session_id"],
        "url": f"orca://session/{s['session_id']}",
        "title": s["title"],
        "repo": s["repo"],
        "branch": s["branch"],
        "worktree": s["worktree"],
        "terminal_open": s["terminal_open"],
        "claude_running": s["claude_running"],
        "last_event": f["last_event"] or s.get("last_event"),
        "events_since": f["events"],
        "events_total": s["events_total"],
        "matched_by": how,
    }


def session_item(s):
    f = s["since_previous_report"]
    return {
        "source": "session",
        "org": "Orca",
        "repo": s["repo"] or "no repository",
        "kind": "session",
        "number": s["session_id"],
        "title": s["title"],
        "url": f"orca://session/{s['session_id']}",
        "author": CONFIG["person"],
        "assignees": [CONFIG["person"]],
        "labels": [],
        "created": "",
        "updated": f["last_event"] or s.get("last_event") or "",
        "comments": 0,
        "draft": None,
        "review_requests": [],
        "closes": [],
        "involves_person": True,
        "boards": [],
        "clickup": [],
        "sessions": [
            session_facts(s, "its own item: it matched no GitHub or ClickUp item")
        ],
        "matched_by": [],
    }


def main(run):
    run = Path(run)
    github = read_json(run / "github-items.json", [])
    tasks = read_json(run / "clickup-items.json", [])
    sessions = read_json(run / "sessions.json", [])
    items = {i["url"]: dict(i, clickup=[], sessions=[], matched_by=[]) for i in github}
    lower = {u.lower(): u for u in items}
    by_task_id = {t["number"].lower(): t for t in tasks}
    merged = {}

    refs = {}  # task id -> GitHub item URLs whose title, body or branch name it
    for i in github:
        for ref in i.get("clickup_refs", []):
            if ref in by_task_id:
                refs.setdefault(ref, set()).add(i["url"])
    for t in tasks:
        tid = t["number"].lower()
        linked = {
            lower[u.lower()] for u in t.get("github_links", []) if u.lower() in lower
        }
        targets = sorted(linked | refs.get(tid, set()))
        if not targets:
            items[t["url"]] = dict(t, clickup=[], sessions=[], matched_by=[])
            continue
        home = items[targets[0]]
        home["clickup"].append(task_facts(t))
        how = (
            "the task links it"
            if targets[0] in linked
            else "the GitHub item names the task"
        )
        home["matched_by"].append(
            f"ClickUp task {t['url']}: {how}"
            + (
                f"; the task also matches {', '.join(targets[1:])}"
                if targets[1:]
                else ""
            )
        )
        merged[t["url"]] = targets[0]

    prev = read_json(run / "run.json", {}).get("previous_completed_run")
    prev_items = (
        {i["url"]: i for i in read_json(run.parent / prev / "items.json", [])}
        if prev
        else {}
    )
    clickup_read = read_json(run / "clickup-status.json", {}).get("read")
    # What exclude.py left out because an orchestrator holds it: never restored from the previous report.
    held = {u.lower() for u in read_json(run / "excluded.json", [])}
    # Sessions that were listed under an issue now held follow the ClickUp tasks that were listed under it
    # (the issue is gone from this run, so each task is an item of its own).
    moved_sessions = {
        t["url"]: it.get("sessions", [])
        for url, it in prev_items.items()
        if url.lower() in held
        for t in it.get("clickup", [])
    }
    if not clickup_read:
        # ClickUp not read: the previous report's tasks stay listed as they were, so a session on a task still
        # finds it and nothing moves because of one failed read.
        for url, it in prev_items.items():
            if it.get("source") == "clickup" and url not in items:
                items[url] = dict(
                    it,
                    sessions=[],
                    carried=True,
                    matched_by=[
                        "carried from the previous report: ClickUp not read this run"
                    ],
                )
                by_task_id.setdefault(it["number"].lower(), it)
            elif url in items:
                for t in it.get("clickup", []):
                    by_task_id.setdefault(t["number"].lower(), t)
                    merged.setdefault(t["url"], url)
        # A task that was listed under an issue the orchestrator now holds (exclude.py removed the issue from
        # this run) would vanish with it: it stays listed as an item of its own, as it would if ClickUp were read.
        for url, it in prev_items.items():
            if url.lower() not in held:
                continue
            for t in it.get("clickup", []):
                if t["url"] in items:
                    continue
                items[t["url"]] = dict(
                    TASK_BASE,
                    **t,
                    clickup=[],
                    sessions=[],
                    carried=True,
                    matched_by=[
                        "carried from the previous report: ClickUp not read this run, and its issue is held by the orchestrator"
                    ],
                )
                by_task_id.setdefault(t["number"].lower(), t)

    def resolve(url):
        url = merged.get(url, url)
        return lower.get(url.lower(), url) if url.startswith(GITHUB) else url

    # A fork's pull request names a branch in the fork, and a shared branch says nothing about the work.
    prs_by_branch = {
        (i["url"].split("/pull/")[0].lower(), i["branch"]): i["url"]
        for i in github
        if i["kind"] == "pr"
        and i.get("branch")
        and not i.get("cross_repo")
        and i["branch"] not in SHARED_BRANCHES
    }
    for s in sessions:
        repo = (s.get("repo") or "").lower()
        base = f"{GITHUB}{repo}".lower()
        found, how = None, None
        for kind, n in (
            ("pull", s.get("linked_pr")),
            ("issues", s.get("linked_issue")),
        ):
            if n and f"{base}/{kind}/{n}" in lower:
                found, how = (
                    lower[f"{base}/{kind}/{n}"],
                    f"its Orca workspace is linked to {kind.rstrip('s')} #{n}",
                )
                break
        if not found and (base, s.get("branch")) in prs_by_branch:
            found, how = (
                prs_by_branch[(base, s["branch"])],
                f"a pull request is open on its branch {s['branch']}",
            )
        if not found:
            for n in BRANCH_NUMBER.findall(s.get("branch") or ""):
                for kind in ("issues", "pull"):
                    if f"{base}/{kind}/{n}" in lower:
                        found, how = (
                            lower[f"{base}/{kind}/{n}"],
                            f"its branch {s['branch']} names #{n}",
                        )
                        break
                if found:
                    break
        if not found:
            for cu in BRANCH_CU.findall(s.get("branch") or ""):
                target = (
                    resolve(by_task_id[cu.lower()]["url"])
                    if cu.lower() in by_task_id
                    else None
                )
                if target in items:
                    found, how = target, f"its branch {s['branch']} names CU-{cu}"
                    break
        if not found:
            asked = set(s.get("prompt_urls_all", [])) | set(
                s["since_previous_report"].get("prompt_urls", [])
            )
            named = {resolve(u) for u in asked} & set(items)
            if len(named) == 1:
                found, how = (
                    named.pop(),
                    "it was asked to work on this item and no other",
                )
        if found:
            items[found]["sessions"].append(session_facts(s, how))
            items[found]["matched_by"].append(f"agent session {s['title']}: {how}")
            merged[f"orca://session/{s['session_id']}"] = found
        else:
            item = session_item(s)
            items[item["url"]] = item

    # A source not read this run keeps each item's tasks or sessions from the previous report, so a failed read
    # never changes an item's group or makes it look changed.
    for key, read, label in (
        ("clickup", clickup_read, "ClickUp tasks"),
        (
            "sessions",
            read_json(run / "sessions-status.json", {}).get("read"),
            "agent sessions",
        ),
    ):
        if read:
            continue
        for url, it in items.items():
            old = prev_items.get(url, {}).get(key, [])
            if key == "sessions":
                old = old + moved_sessions.get(url, [])
            old = [x for x in old if x["url"].lower() not in held]
            if old and not it[key]:
                it[key] = [dict(x, carried=True) for x in old]
                it["matched_by"].append(
                    f"{len(old)} {label} carried from the previous report: not read this run"
                )

    out = sorted(items.values(), key=lambda i: i["url"])
    write_json(run / "items.json", out)
    write_json(run / "merged-into.json", merged)
    print(
        f"{len(out)} items: {len(github)} GitHub, {sum(1 for i in out if i.get('source') == 'clickup')} ClickUp only, "
        f"{sum(1 for i in out if i.get('source') == 'session')} sessions only; "
        f"{sum(1 for u in merged if 'clickup' in u)} ClickUp tasks and {sum(1 for u in merged if u.startswith('orca:'))} sessions joined to an item"
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
