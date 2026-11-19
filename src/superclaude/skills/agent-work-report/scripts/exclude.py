#!/usr/bin/env python3
"""Leave out what the orchestrator already holds, between Step 4 (agent sessions) and Step 5 (match.py).

usage: exclude.py <run_folder>

The orchestrator keeps one entry file per issue it holds in `.dev/coordinator/orchestrated/` (see common.py).
The daily run does not touch such an issue (owner ruling 1, 2026-11-19): while an entry file exists AND this run's
own collection shows the issue open, assigned to the person, in a repo it read without error (coverage.json),
this script removes from the run
  github-items.json   the issue and the pull request the entry names
  sessions.json       the worker and orchestrator sessions the entry names
and writes every removed url to excluded.json (a sorted list). Nothing after it sees those items, so
match.py, classify.py, compare.py, render.py, check.py and page.py need no rule of their own; compare.py and
check.py read excluded.json only to leave the same urls out of the previous snapshot.

An entry file whose issue the run does not show open and assigned (a person closed it, or took the assignment
away), or whose repo failed to read, excludes nothing: the daily run lists the issue as it would any other, and
`run.py refresh` moves that entry to `closed/`. Entry files in `orchestrated/closed/` and `orchestrated/info/`
exclude nothing. A ClickUp task linked to an excluded issue is matched to no GitHub item by match.py and
becomes an item of its own: ClickUp stays with the daily run.

Run twice, it gives the same result: the first run keeps the unreduced files as `github-items-before-exclude.json`
and `sessions-before-exclude.json`, and a rerun reads them.
"""

import sys
from pathlib import Path

from common import (
    CONFIG,
    SESSION_URL,
    entry_files,
    entry_issue_url,
    entry_session_ids,
    read_json,
    write_json,
)


def readable_repos(coverage):
    """{"org/repo"} of the repos this run read without error."""
    return {
        f"{r['org']}/{r['repo']}".lower()
        for r in coverage.get("repos", [])
        if not r.get("errors")
        and not r.get("archived")
        and r.get("issues_enabled", True)
    }


def original(run, name):
    """The run's file before this script first reduced it (kept as `<stem>-before-exclude.json`)."""
    path, kept = run / f"{name}.json", run / f"{name}-before-exclude.json"
    if not kept.exists() and path.exists():
        kept.write_text(path.read_text())
    return read_json(kept, [])


def main(run):
    run = Path(run)
    github = original(run, "github-items")
    sessions = original(run, "sessions")
    read_ok = readable_repos(read_json(run / "coverage.json", {}))
    me = CONFIG["person"]
    issues = {
        i["url"].lower(): i
        for i in github
        if i.get("kind") == "issue"
        and me in (i.get("assignees") or [])
        and f"{i['org']}/{i['repo']}".lower() in read_ok
    }
    gone, held = set(), []
    for path, entry in entry_files().items():
        url = entry_issue_url(entry, path)
        if url.lower() not in issues:
            continue  # not shown open and assigned to the person: the daily run lists it like any other item
        held.append(path.stem)
        gone.add(url.lower())
        if entry.get("pr_url"):
            gone.add(entry["pr_url"].lower())
        gone |= {(SESSION_URL + sid).lower() for sid in entry_session_ids(entry)}
    kept_items = [i for i in github if i["url"].lower() not in gone]
    kept_sessions = [
        s for s in sessions if (SESSION_URL + s["session_id"]).lower() not in gone
    ]
    removed = sorted(
        {i["url"] for i in github if i["url"].lower() in gone}
        | {
            SESSION_URL + s["session_id"]
            for s in sessions
            if (SESSION_URL + s["session_id"]).lower() in gone
        }
    )
    write_json(run / "github-items.json", kept_items)
    write_json(run / "sessions.json", kept_sessions)
    write_json(run / "excluded.json", removed)
    print(
        f"{len(held)} orchestrated issues left out of this run: {len(removed)} urls "
        f"(github {len(github) - len(kept_items)}, sessions {len(sessions) - len(kept_sessions)})"
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
