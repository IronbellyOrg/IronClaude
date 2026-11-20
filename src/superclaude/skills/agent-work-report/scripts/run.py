#!/usr/bin/env python3
"""Run lock, run folder and action log (FR-2, FR-4, FR-18).

usage:
  run.py open <kind>                  kind: daily | hourly | on-demand. Prints the run folder.
                                      Exits 3 if a live lock exists (the wake is recorded as skipped).
  run.py summary <run_folder>         writes summary.md (the session summary and ClickUp DM) by script from
                                      the passed overview
  run.py gate <run_folder>            exits 0 only if the report may reach Clay: every script check passed on
                                      the current text, and summary.md is the script's
  run.py close <run_folder>           marks the run complete and removes the lock (refused until the gate passes)
  run.py abandon <run_folder> <reason>  releases the lock of a run that cannot make a report; it never counts
                                      as a finished report
  run.py log <run_folder> <action> <item_url|-> <reason>    appends one action log entry
  run.py refresh [--run <run_folder>]  rebuilds the shared page .dev/coordinator/report.html from the last daily
                                      report plus the orchestrator's entry files, with no model call (the
                                      living report). Reconciles each entry file with GitHub first (a closed or
                                      unassigned issue moves to orchestrated/closed/) and deletes closed/ and
                                      info/ files older than info_ttl_days. With --run it builds from that run's
                                      overview.md while that run holds the lock and never writes <run>/report.html;
                                      without it, it does nothing while a daily run holds the lock
  run.py status                       prints the lock and the latest completed run

A lock older than its run's time budget is a stuck run: `open` reports it, replaces the
lock and proceeds, and the stuck run is named in the new run's folder for the report.
"""

import hashlib
import json
import re
import shutil
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from common import (
    CONFIG,
    DASHES,
    ENTRY_SECTIONS,
    ITEM_URL,
    NEEDS_PARTS,
    NO_ONE_WAITING,
    NOTICES,
    REPORT_URL,
    SESSION_URL,
    SKILL_DIR,
    CommandError,
    entry_blocks,
    entry_files,
    entry_issue_url,
    entry_session_ids,
    gh_json,
    item_parts,
    needs_in_order,
    orchestrated_dir,
    read_json,
    repo_root,
    run_cmd,
    runs_dir,
    section,
    state_dir,
    write_json,
)


def now():
    return datetime.now(timezone.utc)


def lock_path():
    return state_dir() / "run.lock"


def latest_completed(exclude=None):
    done = sorted(
        p
        for p in runs_dir().iterdir()
        if (p / "complete.json").exists()
        and p != exclude
        and read_json(p / "complete.json", {}).get("kind") != "hourly"
    )
    return done[-1] if done else None


def open_run(kind):
    lock = read_json(lock_path())
    stuck = None
    if lock:
        started = datetime.fromisoformat(lock["started"])
        budget = timedelta(
            minutes=CONFIG["time_budget_minutes"][
                "hourly" if lock["kind"] == "hourly" else "daily"
            ]
        )
        if now() - started < budget:
            d = state_dir() / "wakes"
            d.mkdir(exist_ok=True)
            t = now().isoformat(timespec="seconds")
            write_json(
                d / (t.replace(":", "") + "-skipped.json"),
                {
                    "mode": kind,
                    "time": t,
                    "outcome": f"SKIPPED: run {lock['run']} is still active",
                },
            )
            print(f"skipped: run {lock['run']} is still active", file=sys.stderr)
            sys.exit(3)
        stuck = lock
    run_id = now().strftime("%Y%m%dT%H%M%SZ") + f"-{kind}"
    folder, n = runs_dir() / run_id, 1
    while folder.exists():  # two runs in the same second
        n += 1
        folder = runs_dir() / f"{run_id}-{n}"
    run_id = folder.name
    folder.mkdir()
    write_json(lock_path(), {"run": run_id, "kind": kind, "started": now().isoformat()})
    prev = latest_completed(exclude=folder)
    write_json(
        folder / "run.json",
        {
            "run": run_id,
            "kind": kind,
            "started": now().isoformat(),
            "previous_completed_run": prev.name if prev else None,
            "stuck_run_replaced": stuck,
        },
    )
    since = read_json(prev / "run.json", {}).get("started", "") if prev else ""
    unfinished = sorted(
        p.name
        for p in runs_dir().iterdir()
        if p != folder
        and not (p / "complete.json").exists()
        and read_json(p / "run.json", {}).get("started", "") >= since
    )
    if unfinished:
        write_json(folder / "incomplete-runs.json", unfinished)
    wakes = (
        sorted(
            p
            for p in (state_dir() / "wakes").glob("*.json")
            if read_json(p).get("time", "") >= since[:19]
        )
        if (state_dir() / "wakes").exists()
        else []
    )
    write_json(folder / "wake-records.json", [read_json(p) for p in wakes])
    write_json(folder / "automation-runs.json", automation_runs(since))
    (folder / "run-log.md").write_text(f"# Run log {run_id}\n\n")
    print(folder)
    return folder


def automation_runs(since):
    """The waker automations' run history since the previous run (removing an automation deletes it)."""
    prefix = CONFIG["automation_prefix"]
    try:
        autos = [
            a
            for a in orca_result(["automations", "list"]).get("automations", [])
            if a.get("name", "").startswith(prefix)
        ]
        if not autos:
            return {
                "read": False,
                "reason": f"no Orca automation named {prefix}... exists",
                "runs": [],
            }
        keep = []
        for a in sorted(autos, key=lambda a: a["name"]):
            res = orca_result(["automations", "runs", "--id", a["id"]])
            rows = res.get("runs") or res.get("items") or []
            keep += [
                dict(r, automation=a["name"])
                for r in rows
                if not since or run_stamp(r) >= since[:19]
            ]
    except (CommandError, ValueError, KeyError) as e:
        return {"read": False, "reason": str(e)[:300], "runs": []}
    return {"read": True, "runs": keep}


def run_stamp(r):
    """A run row's start time as ISO text; Orca may give epoch milliseconds or ISO strings."""
    v = r.get("startedAt") or r.get("createdAt") or r.get("scheduledFor") or ""
    if isinstance(v, (int, float)):
        return datetime.fromtimestamp(v / 1000, timezone.utc).isoformat()
    return str(v)


def orca_result(args):
    out = json.loads(run_cmd(["orca", *args, "--json"], timeout=60))
    if not out.get("ok", True):
        raise CommandError(json.dumps(out.get("error"))[:300])
    return out.get("result", out)


REQUIRED_CHECKS = (
    "placeholders",
    "template",
    "sessions",
    "carry-forward",
    "needs-you",
    "candidates",
    "links",
)


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def passed(folder):
    """(True, "") only when every script check (links included) passed on the exact overview.md that exists
    now (its sha256). There is no review step (CLAY, 2026-11-03)."""
    folder = Path(folder)
    report, checks = folder / "overview.md", folder / "script-checks.md"
    if not report.exists():
        return False, "overview.md is missing"
    rows = (
        dict(re.findall(r"(?m)^\| ([\w-]+) \| (PASS|FAIL) \|", checks.read_text()))
        if checks.exists()
        else {}
    )
    missing = [c for c in REQUIRED_CHECKS if rows.get(c) != "PASS"]
    if missing:
        return (
            False,
            f"the script checks have not all passed ({', '.join(missing)}; run check.py --links)",
        )
    if f"overview sha256: {sha256(report)}" not in checks.read_text():
        return (
            False,
            "overview.md changed after the last script check; run check.py --links again",
        )
    return True, ""


def deliverable(folder):
    """The gate for anything that reaches Clay: the report passed, its page was built from that exact text,
    and the summary is the script's."""
    ok, why = passed(folder)
    if ok:
        ok, why = page_ok(folder)
    return summary_ok(folder) if ok else (ok, why)


def page_ok(folder):
    """(True, "") only when report.html (what Clay reads) was built by page.py from the current overview."""
    page = Path(folder) / "report.html"
    if not page.exists():
        return False, "report.html is missing (run page.py)"
    want = f'<meta name="overview-sha256" content="{sha256(Path(folder) / "overview.md")}">'
    if want not in page.read_text():
        return (
            False,
            "report.html was built from an older overview.md (run page.py again)",
        )
    return True, ""


def build_summary(folder):
    """The session summary and ClickUp DM, made by script from the checked overview only: its count table,
    its change line, each "Needs you" heading with its item link, and its "Not checked" lines. No model
    writing, so it can say nothing the report does not."""
    folder = Path(folder)
    report = folder / "overview.md"
    text = report.read_text()
    meta = read_json(folder / "run.json", {})
    tz = ZoneInfo(CONFIG["timezone"])
    table = re.search(
        r"(?ms)^\| Your work \| Count \|\n\|---\|---\|\n(.*?)(?:\n\n|\Z)", text
    )
    counts = []
    for name, n in re.findall(
        r"(?m)^\| ([^|]+) \| (\d+) \|$", table.group(1) if table else ""
    ):
        counts.append(
            f"{name.strip().replace('judged below', 'judged in the report')} {n}"
        )
    header = [
        ln for ln in text.split("\n## ", 1)[0].splitlines() if ln.startswith(NOTICES)
    ]
    changes = re.search(r"(?m)^\*\*Since the previous report:\*\* (.*)$", text)
    prev = meta.get("previous_completed_run")
    prev_date = (
        datetime.strptime(prev[:16], "%Y%m%dT%H%M%SZ")
        .replace(tzinfo=timezone.utc)
        .astimezone(tz)
        .strftime("%a %Y-%m-%d")
        if prev
        else "none, first report"
    )
    needs = []
    for b in needs_in_order(
        text
    ):  # highest priority first; heading and bullets but the options (CLAY, 2026-11-04)
        parts = item_parts(b)
        needs.append(
            "\n".join(
                [f"**{parts['heading'][4:].strip()}**"]
                + [
                    f"- **{lbl}:** {parts[lbl]}"
                    for lbl in NEEDS_PARTS
                    if lbl != "Options" and parts.get(lbl)
                ]
            )
            + "\n"
        )
    not_checked = [
        ln[2:]
        for ln in section(text, "Not checked").splitlines()
        if ln.startswith("- ")
    ]
    out = (SKILL_DIR / "templates" / "summary-template.md").read_text()
    fills = {
        "date": datetime.fromisoformat(meta["started"])
        .astimezone(tz)
        .strftime("%A %Y-%m-%d"),
        "counts_line": "; ".join(counts) or "none",
        "changes_line": changes.group(1) if changes else "not given",
        "previous_date": prev_date,
        "needs_you_count": str(len(needs)),
        "needs_you_lines": "\n".join(needs) or NO_ONE_WAITING,
        "not_checked_line": "; ".join(not_checked) or "Every source was read.",
        "report_link": REPORT_URL,
    }
    for k, v in fills.items():
        out = out.replace("{{" + k + "}}", v)
    if header:  # a missed report day or a replaced stuck run leads the summary, as it leads the report
        out = out.replace(
            "\n**Your work:**", "\n" + "\n".join(header) + "\n**Your work:**", 1
        )
    return DASHES.sub("-", out)


def write_summary(folder):
    (Path(folder) / "summary.md").write_text(build_summary(folder))
    print(f"wrote {Path(folder) / 'summary.md'}")


def summary_ok(folder):
    """(True, "") only when summary.md is exactly what build_summary makes from the current overview."""
    path = Path(folder) / "summary.md"
    if not path.exists():
        return False, "summary.md is missing (run.py summary)"
    if path.read_text() != build_summary(folder):
        return (
            False,
            "summary.md is not the one run.py summary makes from the current report",
        )
    return True, ""


def gate(folder):
    ok, why = deliverable(folder)
    print(
        "PASS: the report may be delivered"
        if ok
        else f"BLOCKED: {why}; fix it, do not deliver"
    )
    sys.exit(0 if ok else 1)


def close_run(folder):
    """Mark a run complete. A daily or on-demand run must have a passing report: a run that never made one is
    abandoned (`run.py abandon`), never counted as the day's report or used as the previous report."""
    folder = Path(folder)
    meta = read_json(folder / "run.json")
    if meta["kind"] != "hourly":
        ok, why = passed(folder)
        if not ok:
            sys.exit(f"not closed: {why}")
    write_json(
        folder / "complete.json",
        {"run": meta["run"], "kind": meta["kind"], "finished": now().isoformat()},
    )
    lock = read_json(lock_path())
    if lock and lock["run"] == meta["run"]:
        lock_path().unlink()
    print(f"closed {meta['run']}")


def abandon_run(folder, reason):
    """Give up a run that cannot make a report: release the lock and record why. It writes no complete.json,
    so the 09:00 check still says no report finished and the next report compares with the last real one."""
    folder = Path(folder)
    meta = read_json(folder / "run.json")
    write_json(
        folder / "abandoned.json",
        {"run": meta["run"], "reason": reason, "time": now().isoformat()},
    )
    lock = read_json(lock_path())
    if lock and lock["run"] == meta["run"]:
        lock_path().unlink()
    print(f"abandoned {meta['run']}: {reason}")


def log_action(folder, action, item, reason):
    folder = Path(folder)
    entry = {
        "time": now().isoformat(timespec="seconds"),
        "run": folder.name,
        "action": action,
        "item": None if item == "-" else item,
        "reason": reason,
        "overview": str(folder / "overview.md"),
    }
    with open(state_dir() / "action-log.jsonl", "a") as f:
        f.write(json.dumps(entry, sort_keys=True) + "\n")
    with open(folder / "run-log.md", "a") as f:
        f.write(f"- {entry['time']} {action} {item}: {reason}\n")


def status():
    print(
        json.dumps(
            {
                "lock": read_json(lock_path()),
                "latest_completed": (latest_completed() or Path("none")).name,
            },
            indent=1,
        )
    )


# The living report (spec DQ12, 6.4): `refresh` rebuilds the shared page `.dev/coordinator/report.html` from the
# last daily report's text for everything the orchestrator does not hold, plus one block per entry file the
# orchestrator keeps in `orchestrated/` (and `orchestrated/info/`). It reconciles the entry files with GitHub
# first and prunes `closed/` and `info/`. No model is called: page.py's own builder makes the page, fed a
# scratch run folder, so `<run>/report.html` (which `run.py gate` checks) is never written.
INFO_TTL_DEFAULT = 14
REFRESH_SCRATCH = ".refresh-build"
ISSUE_URL = re.compile(r"^https://github\.com/([^/]+/[^/]+)/issues/(\d+)$")


def info_ttl_days():
    """`info_ttl_days` (days a closed or information entry stays; 14 by default, one key for both folders) from
    `repos.yaml` of the orchestrator repo. Only that one top-level number is read, by line: the installed
    scripts run under the system python3, which need not have a YAML library."""
    try:
        text = (repo_root() / "repos.yaml").read_text()
    except OSError:
        return INFO_TTL_DEFAULT
    m = re.search(r"(?m)^info_ttl_days:\s*(\d+)\b", text)
    return int(m.group(1)) if m else INFO_TTL_DEFAULT


def entry_time(path, data):
    """When an entry file was last of interest: `closed_at`, else `last_update`, else the file's own time."""
    for field in ("closed_at", "last_update"):
        try:
            t = datetime.fromisoformat(str(data.get(field)).replace("Z", "+00:00"))
            return t if t.tzinfo else t.replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return datetime.fromtimestamp(Path(path).stat().st_mtime, timezone.utc)


def move_to_closed(path, entry, reason):
    closed = orchestrated_dir() / "closed"
    closed.mkdir(parents=True, exist_ok=True)
    entry = dict(entry, closed_at=now().isoformat(), close_reason=reason)
    write_json(closed / path.name, entry)
    path.unlink()


def reconcile_entries():
    """Move the entry of a closed issue, or of one the person is no longer assigned to, to `closed/` with
    GitHub's own reason (`COMPLETED`, `NOT_PLANNED`) or "no longer assigned to you". A read that fails closes
    nothing: it is returned as a warning and the entry stays (a failed read carries items, never closes them)."""
    moved, warnings = [], []
    for path, entry in entry_files().items():
        m = ISSUE_URL.match(entry_issue_url(entry, path))
        if not m:
            warnings.append(f"{path.name}: no issue url to ask GitHub about")
            continue
        try:
            x = gh_json(
                "issue",
                "view",
                m.group(2),
                "--repo",
                m.group(1),
                "--json",
                "state,stateReason,assignees",
            )
        except CommandError as e:
            warnings.append(f"{path.name}: GitHub was not read ({e})")
            continue
        logins = [a.get("login") for a in x.get("assignees") or []]
        if x.get("state") != "OPEN":
            reason = x.get("stateReason") or x.get("state") or "CLOSED"
        elif CONFIG["person"] not in logins:
            reason = "no longer assigned to you"
        else:
            continue
        move_to_closed(path, entry, reason)
        moved.append((path.name, reason))
    return moved, warnings


def prune_old_entries(days):
    """Delete the files in `closed/` and `info/` older than `days`."""
    cutoff = now() - timedelta(days=days)
    deleted = []
    for sub in ("closed", "info"):
        for path, entry in entry_files(orchestrated_dir() / sub).items():
            if entry_time(path, entry) < cutoff:
                path.unlink()
                deleted.append(f"{sub}/{path.name}")
    return deleted


def entry_record(url, e, key, info, base_started):
    """The run-file shapes (`items.json`, `classified.json`, `compare.json`) page.py reads for one entry file."""
    statuses = e.get("session_status") or {}
    worker, orch = e.get("worker") or {}, e.get("orchestrator") or {}
    sessions = []
    for sid in sorted(entry_session_ids(e)):
        is_orch = sid == orch.get("session_id") or (orch.get("link") or "").endswith(
            "/" + sid
        )
        sessions.append(
            {
                "session_id": sid,
                "url": SESSION_URL + sid,
                "title": (
                    (orch.get("tag") or orch.get("id") or "orchestrator")
                    if is_orch
                    else (worker.get("title") or f"worker for {key}")
                )
                + (
                    f" ({(orch if is_orch else worker)['tier']})"
                    if (orch if is_orch else worker).get("tier")
                    else ""
                ),
                "branch": "" if is_orch else (worker.get("branch") or ""),
                "claude_running": str(statuses.get(sid, "")).startswith("working"),
                "last_event": e.get("last_update") or "",
            }
        )
    assignees = e.get("assignees") or (
        [e["human_assignee"]] if e.get("human_assignee") else []
    )
    item = {
        "source": "github",
        "kind": "issue",
        "title": e.get("title") or key,
        "url": url,
        "author": e.get("author") or "",  # who opened the issue: never the assignee
        "assignees": assignees,
        "labels": [],
        "created": "",
        "updated": e.get("last_update") or "",
        "comments": 0,
        "draft": None,
        "review_requests": [],
        "closes": [],
        "involves_person": True,
        "boards": [],
        "clickup": [],
        "sessions": sessions,
        "matched_by": [],
    }
    group = "inprogress" if info else "assigned"
    cls = {
        "group": group,
        "priority": e.get("priority") or "Unset",
        "priority_source": "the priority the orchestrator recorded in its entry",
        "why": "information for you"
        if info
        else "assigned to you; the orchestrator holds it",
    }
    changed = (e.get("last_update") or "") > (base_started or "")
    return item, cls, changed


def replace_section(text, heading, fn):
    """`text` with the body of the `## heading` section replaced by fn(body)."""
    m = re.search(rf"(?ms)^(## {re.escape(heading)}[^\n]*\n)(.*?)(?=^## |\Z)", text)
    if not m:
        return text
    return text[: m.start(2)] + fn(m.group(2)) + text[m.end(2) :]


def drop_blocks(body, split, held):
    """`body` without the blocks (cut at `split`) whose first link is a url in `held` (lower case)."""
    keep = []
    for chunk in re.split(split, body):
        m = (
            re.search(r"\]\(" + "(" + ITEM_URL + r")\)", chunk)
            if chunk.startswith("#")
            else None
        )
        if m and m.group(1).lower() in held:
            continue
        keep.append(chunk)
    return "".join(keep)


def refresh(run=None):
    """Build the shared page from the last daily report plus the entry files. With `run` (called at the end of
    Step 12, while that run holds the lock) it builds from that run's `overview.md`; without it, from the last
    completed daily run, and it does nothing while a daily run holds the lock.

    Several orchestrators call this at their own milestones, so one refresh runs at a time (an exclusive lock on
    `.dev/coordinator/refresh.lock`, held until it ends): two builds would otherwise move the same entry twice
    and write the shared page over each other."""
    import fcntl

    with open(state_dir() / "refresh.lock", "w") as lock_file:
        fcntl.flock(lock_file, fcntl.LOCK_EX)
        return _refresh(run)


def _refresh(run=None):
    import page
    import render

    lock = read_json(lock_path())
    if lock and (run is None or lock["run"] != Path(run).name):
        print(
            f"refresh skipped: run {lock['run']} holds the run lock; the next milestone tries again"
        )
        return None
    moved, warnings = reconcile_entries()
    deleted = prune_old_entries(info_ttl_days())
    base = Path(run) if run else latest_completed()
    if base is not None and not (base / "overview.md").exists():
        sys.exit(
            f"refresh needs {base / 'overview.md'}; the run has not stubbed its report yet"
        )
    text = (base / "overview.md").read_text() if base else render_empty_overview()
    meta = read_json(base / "run.json", {}) if base else {}
    cls = (
        read_json(base / "classified.json", {"order": [], "items": {}, "counts": {}})
        if base
        else {"order": [], "items": {}, "counts": {}}
    )
    items = read_json(base / "items.json", []) if base else []
    cmp_ = read_json(base / "compare.json", {}) if base else {}
    for k, v in (
        ("new", []),
        ("changed", {}),
        ("closed", {}),
        ("unchanged", []),
        ("carried", []),
    ):
        cmp_.setdefault(k, v)
    cmp_["previous_run"] = meta.get("previous_completed_run")

    held_entries = entry_files()
    info_entries = entry_files(orchestrated_dir() / "info")
    held = set()
    for path, e in held_entries.items():
        held |= {entry_issue_url(e, path).lower(), (e.get("pr_url") or "").lower()}
        held |= {(SESSION_URL + sid).lower() for sid in entry_session_ids(e)}
    started = meta.get("started") or ""
    # An issue that was in the last daily report, was claimed and then closed (or unassigned) since: its entry
    # is in `closed/` already (reconcile_entries or `report-entry --closed` moved it), so it is not held, but
    # the baseline block would still show it as live work next to its closed line. Drop it too.
    if base is not None and started:
        began = datetime.fromisoformat(started)
        if began.tzinfo is None:
            began = began.replace(tzinfo=timezone.utc)
        for path, e in entry_files(orchestrated_dir() / "closed").items():
            if entry_time(path, e) > began:
                held |= {
                    entry_issue_url(e, path).lower(),
                    (e.get("pr_url") or "").lower(),
                }
                held |= {(SESSION_URL + sid).lower() for sid in entry_session_ids(e)}
    held.discard("")
    # What the orchestrator holds is not a block of the page's other half (a daily run already left it out).
    text = replace_section(
        text, "Needs you", lambda b: drop_blocks(b, r"(?m)^(?=### )", held)
    )
    for heading in ENTRY_SECTIONS:
        text = replace_section(
            text, heading, lambda b: drop_blocks(b, r"(?m)^(?=#{3,4} )", held)
        )
    # A candidate that has since become orchestrated is no longer a candidate: its "Likely yours" line goes too.
    text = replace_section(
        text,
        "Likely yours",
        lambda b: "".join(
            ln
            for ln in b.splitlines(keepends=True)
            if not any(f"]({u})" in ln.lower() for u in held)
        ),
    )
    cls["order"] = [u for u in cls["order"] if u.lower() not in held]
    cls["items"] = {u: v for u, v in cls["items"].items() if u.lower() not in held}
    baseline = {
        i["url"].lower(): i for i in items
    }  # the daily run's items, before the held ones are dropped
    items = [i for i in items if i["url"].lower() not in held]
    # page.py recreates an item from the snapshot when compare.json carries it, so a superseded url must leave
    # the carried list and the snapshot too, or it comes back as a card of its own.
    cmp_["carried"] = [u for u in cmp_["carried"] if u.lower() not in held]
    snapshot = {
        u: v
        for u, v in (read_json(base / "snapshot.json", {}) if base else {}).items()
        if u.lower() not in held
    }

    ctx = {
        "template": render.item_template(),
        "notes": {},
        "to_write": set(),
        "statuses": {},
        "prev_date": "",
    }
    mine, other = [], []
    # What the daily report lists: an item block, or a "Likely yours" line led by the item's link. A url that
    # only appears in another item's notes is not listed.
    daily_listed = {u.lower() for u in entry_blocks(text)} | {
        u.lower()
        for u in re.findall(
            r"(?m)^(?:- )?\[[^\]]*\]\(([^)\s]+)\)", section(text, "Likely yours")
        )
    }
    emitted = set()  # one card per url: the orchestrated entry is made first and wins over an information one
    for info, entries in ((False, held_entries), (True, info_entries)):
        for path, e in sorted(entries.items()):
            url = entry_issue_url(e, path) if not info else (e.get("url") or "")
            if not url:
                print(f"entry file {path.name} left out: no url", file=sys.stderr)
                continue
            if info and url.lower() in daily_listed:
                continue  # a block of the daily report already lists it (FR-28)
            if url.lower() in emitted:
                continue
            emitted.add(url.lower())
            item, c, changed = entry_record(url, e, path.stem, info, started)
            # ClickUp tasks the daily report listed under this issue stay on its card (ClickUp stays with the
            # daily run; only the orchestrator's own text replaces the baseline's).
            item["clickup"] = list((baseline.get(url.lower()) or {}).get("clickup", []))
            if changed:
                cmp_["changed"][url] = {
                    "updated": {"was": None, "now": e.get("last_update")}
                }
            else:
                cmp_["unchanged"].append(url)
            # The entry replaces any record the daily run kept for the url (an unlisted "other" item, say),
            # so the page never gets two cards for one url.
            cls["order"] = [u for u in cls["order"] if u.lower() != url.lower()]
            items = [i for i in items if i["url"].lower() != url.lower()]
            cls["order"].append(url)
            cls["items"][url] = c
            items.append(item)
            (other if info else mine).append(
                render.entry(url, item, c, cmp_, ctx, filed=e)
            )
    if mine:
        text = replace_section(
            text,
            "Your work by priority",
            lambda b: (
                b.rstrip("\n")
                + f"\n\n### Held by the orchestrator ({len(mine)})\n\n"
                + "\n".join(mine)
                + "\n"
            ),
        )
    if other:
        text = replace_section(
            text,
            "Other work in progress",
            lambda b: b.rstrip("\n") + "\n\n" + "\n".join(other) + "\n",
        )
    closed_lines = []
    for path, e in sorted(entry_files(orchestrated_dir() / "closed").items()):
        url = entry_issue_url(e, path)
        closed_lines.append(
            f"- [{e.get('title') or path.stem}]({url}): {e.get('close_reason') or 'closed'} (closed through the orchestrator)"
        )
    if closed_lines:
        text = replace_section(
            text,
            "Closed since the previous report",
            lambda b: b.rstrip("\n") + "\n" + "\n".join(closed_lines) + "\n",
        )

    scratch = Path(tempfile.mkdtemp(prefix=REFRESH_SCRATCH + "-", dir=state_dir()))
    cur = scratch / "cur"
    cur.mkdir()
    prev_name = meta.get("previous_completed_run")
    if prev_name and base is not None and (base / "notes.json").exists():
        (scratch / prev_name).mkdir()
        shutil.copyfile(base / "notes.json", scratch / prev_name / "notes.json")
    (cur / "overview.md").write_text(text)
    write_json(
        cur / "run.json",
        {
            "run": meta.get("run") or "none",
            "kind": "refresh",
            "started": now().isoformat(),
            "previous_completed_run": prev_name,
        },
    )
    write_json(cur / "classified.json", cls)
    write_json(cur / "items.json", items)
    write_json(cur / "compare.json", cmp_)
    write_json(cur / "snapshot.json", snapshot)
    write_json(cur / "to-write.json", [])
    try:
        page.main(cur)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    print(
        f"refresh: {len(mine)} orchestrated, {len(other)} information entries; {len(moved)} moved to closed/, {len(deleted)} old files deleted"
    )
    for name, reason in moved:
        print(f"  moved {name}: {reason}")
    for w in warnings:
        print(f"  kept an entry: {w}", file=sys.stderr)
    return cur


def render_empty_overview():
    """The writing sheet of a page built before any daily report has completed: only the orchestrator's entries."""
    text = (SKILL_DIR / "templates" / "overview-template.md").read_text()
    tz = ZoneInfo(CONFIG["timezone"])
    fills = {
        "date": now().astimezone(tz).strftime("%A %Y-%m-%d"),
        "run": "none",
        "previous": "none (first report)",
        "sources": "the orchestrator's entry files (no daily report has completed yet)",
        "missed": "",
        "count_rows": "",
        "change_counts": "none yet",
        "entries": "",
        "other_work": "None.",
        "closed": "Nothing closed.",
        "how": "- The orchestrator's entry files, with no daily report yet.",
        "not_checked": "- No daily report has completed yet, so only what the orchestrator holds is shown.",
    }
    for k, v in fills.items():
        text = text.replace("{{" + k + "}}", v)
    return text.replace("{{RF_PLACEHOLDER:needs_you}}", "").replace(
        "{{RF_PLACEHOLDER:likely_yours}}", "No other item names you."
    )


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["open"] and len(a) == 2:
        open_run(a[1])
    elif a[:1] == ["gate"] and len(a) == 2:
        gate(a[1])
    elif a[:1] == ["summary"] and len(a) == 2:
        write_summary(a[1])
    elif a[:1] == ["close"] and len(a) == 2:
        close_run(a[1])
    elif a[:1] == ["abandon"] and len(a) == 3:
        abandon_run(a[1], a[2])
    elif a[:1] == ["log"] and len(a) == 5:
        log_action(*a[1:])
    elif a[:1] == ["refresh"] and len(a) in (1, 3) and (len(a) == 1 or a[1] == "--run"):
        refresh(a[2] if len(a) == 3 else None)
    elif a == ["status"]:
        status()
    else:
        sys.exit(__doc__)
