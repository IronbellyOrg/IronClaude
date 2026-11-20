#!/usr/bin/env python3
"""Collect every open GitHub issue and pull request in the configured orgs, plus board status.

usage: collect.py <run_folder>

Writes into the run folder:
  github-items.json  one record per open issue or pull request, sorted by URL
  coverage.json      every repo found, with its item count or the error that stopped the read,
                     and the result of each source (Projects boards, the "involves" search)

A failed read never stops the run: it is recorded so the report can list it under "Not checked".
ClickUp is read by clickup.py. The body is read only to find ClickUp task ids in it (FR-28) and is not kept.
"""

import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from common import CONFIG, CommandError, gh_json, write_json

ISSUE_FIELDS = (
    "number,title,author,assignees,labels,createdAt,updatedAt,url,comments,body"
)
PR_FIELDS = (
    ISSUE_FIELDS
    + ",isDraft,reviewRequests,closingIssuesReferences,headRefName,isCrossRepository"
)
# ClickUp's own link forms: CU-<id>, the task URL, and #<id> (kept only if it is a task id seen this run,
# which match.py checks; an id always has a letter, so GitHub's #123 never matches).
CLICKUP_REF = re.compile(
    r"\bCU-([0-9a-z]+)(?![0-9a-z])|app\.clickup\.com/t/(?:\d+/)?([0-9a-z]+)|#([0-9]*[a-z][0-9a-z]{5,})\b",
    re.I,
)


# A line that states a level for the item itself: "low priority", "high-priority", "priority: high". A P0-P4
# code is not matched: issue bodies use it for phases ("phases P0-P4"), not for priority.
PRIORITY_LINE = re.compile(
    r"\b(?:(urgent|high|medium|low)[ -]priority|priority\s*(?:is|:|=|to|of)?\s*[:=]?\s*(urgent|high|medium|low))\b",
    re.I,
)


def login(x):
    return (x or {}).get("login")


def priority_mentions(x):
    """Every line of the item's text or comments that states a priority level, with who wrote it and when
    (CLAY, 2026-11-17: a priority in a comment counts as one). classify.py takes the person's own; the model
    judges everyone else's."""
    texts = [("issue", login(x.get("author")), x["createdAt"], x.get("body"))]
    texts += [
        ("comment", login(c.get("author")), c.get("createdAt"), c.get("body"))
        for c in x.get("comments") or []
    ]
    out = []
    for where, who, when, body in texts:
        for line in (body or "").splitlines():
            m = PRIORITY_LINE.search(line)
            if m:
                out.append(
                    {
                        "by": who,
                        "date": when or "",
                        "where": where,
                        "level": (m.group(1) or m.group(2)).capitalize(),
                        "line": " ".join(line.split())[:200],
                    }
                )
    return out


def clickup_refs(*texts):
    return sorted(
        {
            next(g for g in m.groups() if g).lower()
            for t in texts
            for m in CLICKUP_REF.finditer(t or "")
        }
    )


def record(org, repo, kind, x):
    return {
        "org": org,
        "repo": repo,
        "kind": kind,
        "number": x["number"],
        "title": x["title"],
        "url": x["url"],
        "author": login(x.get("author")),
        "assignees": sorted(a["login"] for a in x.get("assignees") or []),
        "labels": sorted(lb["name"] for lb in x.get("labels") or []),
        "created": x["createdAt"],
        "updated": x["updatedAt"],
        "comments": len(x.get("comments") or []),
        "priority_mentions": priority_mentions(x),
        "draft": x.get("isDraft"),
        "review_requests": sorted(
            filter(
                None,
                (
                    q.get("login") or q.get("slug") or q.get("name")
                    for q in x.get("reviewRequests") or []
                ),
            )
        ),
        "closes": sorted(
            c["url"] for c in x.get("closingIssuesReferences") or [] if c.get("url")
        ),
        "branch": x.get("headRefName"),
        "cross_repo": x.get("isCrossRepository"),
        "clickup_refs": clickup_refs(x["title"], x.get("body"), x.get("headRefName")),
    }


def read_repo(org, repo):
    full = f"{org}/{repo['name']}"
    items, errors = [], []
    kinds = [("pr", PR_FIELDS)]
    if repo.get("hasIssuesEnabled"):
        kinds.insert(0, ("issue", ISSUE_FIELDS))
    for kind, fields in kinds:
        try:
            for x in gh_json(
                kind,
                "list",
                "--repo",
                full,
                "--state",
                "open",
                "--limit",
                "1000",
                "--json",
                fields,
            ):
                items.append(record(org, repo["name"], kind, x))
        except CommandError as e:
            errors.append(f"{kind}s: {e}")
    cov = {
        "org": org,
        "repo": repo["name"],
        "issues_enabled": bool(repo.get("hasIssuesEnabled")),
        "items": len(items),
        "errors": errors,
    }
    return items, cov


def read_boards(org):
    """Map item URL -> board fields, for every open board in the org."""
    status, boards, errors = {}, [], []
    try:
        projects = gh_json(
            "project", "list", "--owner", org, "--limit", "100", "--format", "json"
        )["projects"]
    except CommandError as e:
        return status, boards, [f"{org} boards: {e}"]
    for p in projects:
        if p.get("closed"):
            continue
        try:
            items = gh_json(
                "project",
                "item-list",
                str(p["number"]),
                "--owner",
                org,
                "--limit",
                "1000",
                "--format",
                "json",
            )["items"]
        except CommandError as e:
            errors.append(f"{org} board {p['title']}: {e}")
            continue
        boards.append(
            {
                "org": org,
                "number": p["number"],
                "title": p["title"],
                "items": len(items),
            }
        )
        for it in items:
            url = (it.get("content") or {}).get("url")
            if url:
                status.setdefault(url, []).append(
                    {
                        "board": p["title"],
                        "status": it.get("status"),
                        "priority": it.get("priority"),
                    }
                )
    return status, boards, errors


def involves(org, person):
    """Open items the person is involved in (author, assignee, mention, commenter)."""
    urls = set()
    for flag in ([], ["--include-prs"]):
        rows = gh_json(
            "search",
            "issues",
            "--owner",
            org,
            "--involves",
            person,
            "--state",
            "open",
            "--limit",
            "1000",
            "--json",
            "url",
            *flag,
        )
        urls.update(r["url"] for r in rows)
    return urls


def main(run):
    run = Path(run)
    person = CONFIG["person"]
    items, coverage, board_status, boards, source_errors, involved = (
        [],
        [],
        {},
        [],
        [],
        set(),
    )
    for org in CONFIG["orgs"]:
        try:
            repos = gh_json(
                "repo",
                "list",
                org,
                "--limit",
                "1000",
                "--json",
                "name,isArchived,hasIssuesEnabled",
            )
        except CommandError as e:
            source_errors.append(f"{org} repo list: {e}")
            continue
        live = sorted(
            (
                r
                for r in repos
                if not r["isArchived"] and r["name"] not in CONFIG["excluded_repos"]
            ),
            key=lambda r: r["name"],
        )
        for r in repos:
            if r["isArchived"]:
                coverage.append(
                    {
                        "org": org,
                        "repo": r["name"],
                        "archived": True,
                        "items": 0,
                        "errors": [],
                    }
                )
        with ThreadPoolExecutor(max_workers=8) as pool:
            for its, cov in pool.map(lambda r: read_repo(org, r), live):
                items += its
                coverage.append(cov)
        st, bd, errs = read_boards(org)
        board_status.update(st)
        boards += bd
        source_errors += errs
        try:
            involved |= involves(org, person)
        except CommandError as e:
            source_errors.append(f"{org} involves search: {e}")
    for it in items:
        it["boards"] = sorted(board_status.get(it["url"], []), key=lambda b: b["board"])
        it["involves_person"] = it["url"] in involved
    items.sort(key=lambda i: i["url"])
    coverage.sort(key=lambda c: (c["org"], c["repo"]))
    write_json(run / "github-items.json", items)
    write_json(
        run / "coverage.json",
        {
            "repos": coverage,
            "boards": sorted(boards, key=lambda b: (b["org"], b["number"])),
            "source_errors": sorted(source_errors),
        },
    )
    failed = sum(1 for c in coverage if c["errors"]) + len(source_errors)
    log = ["## Sources read", ""]
    for c in coverage:
        state = (
            "archived, skipped"
            if c.get("archived")
            else "; ".join(c["errors"]) or f"{c['items']} open items"
        )
        log.append(
            f"- {c['org']}/{c['repo']}: {state}{'' if c.get('issues_enabled', True) else ' (issues switched off)'}"
        )
    log += [f"- board {b['org']}/{b['title']}: {b['items']} items" for b in boards]
    log += [f"- FAILED {e}" for e in sorted(source_errors)]
    with open(run / "run-log.md", "a") as f:
        f.write("\n".join(log) + "\n\n")
    print(
        f"{len(items)} open items from {sum(1 for c in coverage if not c.get('archived'))} repos; "
        f"{len(boards)} boards; {failed} read failures"
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
