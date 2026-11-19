#!/usr/bin/env python3
"""Sort the collected items into the person's groups and set each item's priority.

usage: classify.py <run_folder>

Reads items.json (match.py) and .dev/coordinator/priorities.json (the person's overrides). Writes classified.json.

Groups, decided by fixed rules only (FR-26), for the item and for each ClickUp task listed under it; the
item gets the first group in this order that any of them reaches:
  assigned    the person is an assignee, or a review is requested from them
  owned       not assigned, but the person wrote the pull request, or wrote an open pull
              request that closes the issue; or one of the person's agent sessions works on it
  opened      the person opened it and nobody is assigned
  inprogress  an agent session that matched no GitHub or ClickUp item ("Other work in progress")
  candidate   the person is involved (mentioned, commented) but no rule above applies;
              the model decides whether it is "likely" theirs and records why
  other       none of the above
Priority: the person's override, then the item's or its ClickUp tasks' board priority, then labels, then a level
the person wrote in the item's text or a comment (collect.py's priority_mentions).
"""

import sys
from pathlib import Path

from common import CONFIG, read_json, state_dir, write_json

PRIORITY_ORDER = ["Urgent", "High", "Medium", "Low", "Unset"]
GROUP_ORDER = ["assigned", "owned", "opened", "inprogress", "candidate", "other"]


def priority(item, overrides):
    if item["url"] in overrides:
        return (
            overrides[item["url"]]["level"],
            f"set by {CONFIG['person_name']}: {overrides[item['url']].get('why', '')}".strip(
                ": "
            ),
        )
    for src in [item] + item.get("clickup", []):
        for b in src.get("boards", []):
            if b.get("priority") in PRIORITY_ORDER:
                return b["priority"], f"board {b['board']}" + (
                    "" if src is item else f" of ClickUp task {src['url']}"
                )
    labels = CONFIG["priority_labels"]
    found = sorted(
        (
            (labels[lb.lower()], lb)
            for lb in item.get("labels", [])
            if lb.lower() in labels
        ),
        key=lambda f: PRIORITY_ORDER.index(f[0]),
    )
    if found:
        return found[0][0], f"from the `{found[0][1]}` label"
    # The person's own word in the item's text or a comment counts as set (CLAY, 2026-11-17); the latest wins.
    own = [m for m in item.get("priority_mentions", []) if m["by"] == CONFIG["person"]]
    if own:
        m = max(own, key=lambda m: m["date"])
        return (
            m["level"],
            f"{'a comment' if m['where'] == 'comment' else 'the issue text'} by {CONFIG['person_name']} on {m['date'][:10]}",
        )
    return "Unset", "none set"


def rule(it, person, authored_prs):
    """(group, why) for one GitHub item or ClickUp task by itself."""
    if person in it.get("assignees", []):
        return "assigned", "assigned to you"
    if person in it.get("review_requests", []):
        return "assigned", "your review is requested"
    if it.get("kind") == "pr" and it["author"] == person and not it.get("assignees"):
        return "owned", "you wrote this pull request"
    if it["url"] in authored_prs and not it.get("assignees"):
        return "owned", "your open pull request closes it: " + ", ".join(
            sorted(authored_prs[it["url"]])
        )
    if it["author"] == person and not it.get("assignees"):
        return "opened", "you opened it and nobody is assigned"
    if it.get("involves_person") or it.get("mentions_you"):
        return "candidate", "you are mentioned or commented; needs a judgment"
    return "other", ""


def classify(items, person):
    authored_prs = {}
    for it in items:
        if it["kind"] == "pr" and it["author"] == person:
            for url in it.get("closes", []):
                authored_prs.setdefault(url, []).append(it["url"])
    out = {}
    for it in items:
        if it.get("source") == "session":
            out[it["url"]] = {
                "group": "inprogress",
                "why": "your agent session, not tied to a GitHub or ClickUp item",
            }
            continue
        options = [rule(it, person, authored_prs)]
        options += [
            (g, f"{why} in ClickUp task {t['url']}")
            for t in it.get("clickup", [])
            for g, why in [rule(t, person, authored_prs)]
        ]
        if it.get("sessions"):
            options.append(("owned", "your agent session works on it"))
        group, why = min(options, key=lambda o: GROUP_ORDER.index(o[0]))
        out[it["url"]] = {"group": group, "why": why}
    return out


def main(run):
    run = Path(run)
    items = read_json(run / "items.json")
    overrides = read_json(state_dir() / "priorities.json", {})
    groups = classify(items, CONFIG["person"])
    for it in items:
        level, source = priority(it, overrides)
        groups[it["url"]].update({"priority": level, "priority_source": source})
    order = sorted(
        items,
        key=lambda i: (
            PRIORITY_ORDER.index(groups[i["url"]]["priority"]),
            i["created"],
            i["url"],
        ),
    )
    result = {
        "order": [i["url"] for i in order],
        "items": groups,
        "counts": {
            g: sum(1 for v in groups.values() if v["group"] == g) for g in GROUP_ORDER
        },
    }
    write_json(run / "classified.json", result)
    c = result["counts"]
    print(
        f"assigned {c['assigned']}, owned {c['owned']}, opened {c['opened']}, other work in progress {c['inprogress']}, "
        f"needs a judgment {c['candidate']}, other {c['other']}"
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
