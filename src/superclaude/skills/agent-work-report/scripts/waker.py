#!/usr/bin/env python3
"""The waker: the Orca automation's only job (FR-25).

usage: waker.py morning | hourly | check-missed

morning       find the coordinator session (the terminal running Claude under the ccsession tag), starting
              one if there is none, and send it one wake line to run today's report
hourly        no hourly check exists: the orchestrator does every check-in itself and there is no session manager,
              so this mode only records that it was skipped
check-missed  report if no daily run has completed today (run at 09:00 local by a second automation), with why:
              the morning wake's outcome and any error the coordinator session shows

Every firing writes a wake record to .dev/coordinator/wakes/; the next run copies new records into its
folder. The last line printed is the outcome. When it starts with DM_NEEDED, this script itself tells
Clay: a ClickUp DM through the API, or an unread mark with a note on the coordinator workspace in Orca.
"""

import re
import sys
import time
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import clickup
import orca_term
from common import (
    CONFIG,
    CommandError,
    read_json,
    runs_dir,
    state_dir,
    workspace_path,
    write_json,
)

WAKE_LINES = {
    "morning": "Wake (daily report): run /agent-work-report for today's report.",
}
HOLD_RETRIES, HOLD_WAIT_S = (
    15,
    120,
)  # the morning wake keeps trying for 30 minutes before it asks for a DM


def local_gate(mode, now=None):
    """Why this firing should do nothing, or None.

    Orca's scheduler ignores an automation's time zone (VERIFIED 2026-10-30: the same 07:00 preset gave
    the same next run in UTC and Asia/Tokyo), so the automations fire at both UTC hours that can be the
    local hour across the clock change, and this gate keeps the one that matches local time."""
    tz = ZoneInfo(CONFIG["timezone"])
    now = (now or datetime.now(timezone.utc)).astimezone(tz)
    if now.strftime("%a") not in CONFIG["report_days"]:
        return f"no report on {now:%A}: reports run {', '.join(CONFIG['report_days'])}"
    if mode == "morning":
        if now.hour < int(CONFIG["daily_run_local"][:2]):
            return f"too early: it is {now:%H:%M} local, the report runs at {CONFIG['daily_run_local']}"
        started = daily_run_started(now)
        if started:
            return f"today's report already started ({started})"
    if mode == "check-missed" and now.hour != int(CONFIG["missed_run_dm_local"][:2]):
        return f"not {CONFIG['missed_run_dm_local']} local (it is {now:%H:%M})"
    return None


def daily_run_started(now_local):
    """The name of today's daily run folder (local date of `now_local`), or None."""
    for p in runs_dir().iterdir():
        meta = read_json(p / "run.json", {})
        if (
            meta.get("kind") == "daily"
            and datetime.fromisoformat(meta["started"])
            .astimezone(now_local.tzinfo)
            .date()
            == now_local.date()
        ):
            return p.name
    return None


def notify(text):
    """Tell Clay: a ClickUp DM through the API, or, if that fails, an unread mark with a note on the
    coordinator workspace in Orca. Returns what was done."""
    sent, detail = clickup.send_dm(f"Coordinator: {text}")
    if sent:
        return "ClickUp DM sent"
    try:
        orca_term.orca(
            "worktree",
            "set",
            "--worktree",
            f"path:{workspace_path()}",
            "--unread",
            "--comment",
            f"Coordinator: {text}"[:500],
        )
        return f"ClickUp DM not sent ({detail}); Orca workspace marked unread with the note"
    except CommandError as e:
        return f"ClickUp DM not sent ({detail}); Orca mark failed ({e})"


def record(rec, final=True):
    """Write (or rewrite) this firing's wake record. Called after every attempt, so a firing that is
    stopped part way still leaves a record; `time` stays the firing's start. On the final write, an
    outcome that needs Clay is sent to him (FR-25)."""
    d = state_dir() / "wakes"
    d.mkdir(exist_ok=True)
    rec.setdefault("time", datetime.now(timezone.utc).isoformat(timespec="seconds"))
    if final and rec["outcome"].startswith("DM_NEEDED"):
        rec["notified"] = notify(rec["outcome"][len("DM_NEEDED: ") :])
    write_json(d / (rec["time"].replace(":", "") + f"-{rec['mode']}.json"), rec)
    if final:
        print(rec["outcome"] + (f" [{rec['notified']}]" if rec.get("notified") else ""))


def stuck_run():
    lock = read_json(state_dir() / "run.lock")
    if not lock:
        return None
    age = datetime.now(timezone.utc) - datetime.fromisoformat(lock["started"])
    budget = CONFIG["time_budget_minutes"][
        "hourly" if lock["kind"] == "hourly" else "daily"
    ]
    return lock["run"] if age.total_seconds() > budget * 60 else None


def run_opened_since(t0, wait_s):
    """True once a daily or on-demand run folder records a start at or after t0 (waits up to wait_s)."""
    deadline = time.time() + wait_s
    while True:
        for p in runs_dir().iterdir():
            started = read_json(p / "run.json", {}).get("started")
            if started and datetime.fromisoformat(started).timestamp() >= t0:
                return True
        if time.time() >= deadline:
            return False
        time.sleep(5)


START_WAIT_S = 120
SHELL_WAIT_S = 30
RUN_WAIT_S = 120  # the session opens its run folder within seconds of the wake line (8 seconds on 2026-11-04)
NAME_QUESTION = "Session name"
# What the session's screen says when its turn failed (2026-11-18: "API Error: Request rejected (429) ... all
# Tier 1b models are out of usage", four minutes after the wake line, with nothing retrying it).
ERROR_LINE = re.compile(r"API Error|\b429\b|usage limit|out of usage|rate.?limit", re.I)


def session_error(handle):
    """The last line on the session's screen that reports an error, or ''."""
    try:
        tail = orca_term.screen(handle)["tail"]
    except CommandError:
        return ""
    return next(
        (ln.strip()[:200] for ln in reversed(tail) if ERROR_LINE.search(ln)), ""
    )


class SessionStartError(CommandError):
    pass


def last_line(handle):
    """The screen's last non-empty line (the tail can end in blank rows under the cursor)."""
    return next(
        (ln for ln in reversed(orca_term.screen(handle)["tail"]) if ln.strip()), ""
    )


def start_session(workspace, spare):
    """Start `ccsession coordinator`: in a terminal of the workspace that sits at ccsession's name question
    (left over after a Claude exited) with nobody typing there, else in a new terminal. Returns the handle once
    Claude runs there; raises SessionStartError if it never does."""
    tag = CONFIG["session_tag"]
    handle = next(
        (
            t["handle"]
            for t in spare
            if NAME_QUESTION in last_line(t["handle"])
            and not orca_term.typing_or_fresh(t)
        ),
        None,
    )
    if not handle:
        handle = orca_term.find(
            orca_term.orca("terminal", "create", "--worktree", f"path:{workspace}"),
            "handle",
        )
        if not handle:
            raise SessionStartError("Orca created a terminal but returned no handle")
        # A new workspace shell shows ccsession's name question once its startup finishes; wait for it, or
        # for a plain shell prompt, instead of guessing a delay.
        deadline = time.time() + SHELL_WAIT_S
        while (
            not re.search(NAME_QUESTION + r"|[$#>❯]\s*$", last_line(handle))
            and time.time() < deadline
        ):
            time.sleep(1)
    # The name question takes the tag; a plain shell takes the command.
    answer = tag if NAME_QUESTION in last_line(handle) else f"ccsession {tag}"
    orca_term.send(handle, answer, enter=True, wait_submit_s=5)
    deadline = time.time() + START_WAIT_S
    while orca_term.claude_processes().get(handle) != tag:
        if time.time() > deadline:
            raise SessionStartError(
                f"ccsession {tag} was started in terminal {handle}, but Claude was not running "
                f"there after {START_WAIT_S} seconds"
            )
        time.sleep(3)
    return handle


def wake(mode):
    rec = {"mode": mode, "workspace": workspace_path()}
    if mode == "hourly":
        rec["outcome"] = (
            "SKIPPED: there is no hourly check: the orchestrator does every check-in itself and there is no session manager"
        )
        return record(rec)
    gate = local_gate(mode)
    if gate:
        rec["outcome"] = f"SKIPPED: {gate}"
        return record(rec)
    # A stuck run gets a DM, but the wake still goes out: `run.py open` replaces the stale lock (FR-2).
    stuck = stuck_run()
    note = (
        f"DM_NEEDED: the coordinator run {stuck} was stuck past its time budget and is being replaced; "
        if stuck
        else ""
    )
    attempts = HOLD_RETRIES if mode == "morning" else 1
    for attempt in range(1, attempts + 1):
        rec.pop("session_error", None)
        try:
            outcome, extra = try_wake(mode, retry=attempt > 1)
        except SessionStartError as e:
            outcome, extra = (
                f"DM_NEEDED: the coordinator session did not start ({e})",
                {},
            )
        except CommandError as e:
            outcome, extra = f"DM_NEEDED: the waker could not reach Orca ({e})", {}
        rec.update(extra, attempts=attempt, outcome=outcome)
        if not outcome.startswith("HOLD"):
            break
        record(rec, final=False)
        if attempt < attempts:
            time.sleep(HOLD_WAIT_S)
    if outcome.startswith("HOLD"):
        outcome = (
            f"DM_NEEDED: today's report did not start after {attempts} tries over {attempts * HOLD_WAIT_S // 60} "
            f"minutes; the last one ended: {outcome[len('HOLD: ') :]}"
            if mode == "morning"
            else "SKIPPED" + outcome[4:]
        )
    if note:
        outcome = note + ("wake sent." if outcome.startswith("SENT") else outcome)
    rec["outcome"] = outcome
    return record(rec)


def try_wake(mode, retry=False):
    """One attempt. Returns (outcome, record fields); an outcome starting HOLD means try again later."""
    if (
        retry and mode == "morning"
    ):  # an earlier attempt's run may have opened while we waited
        started = daily_run_started(
            datetime.now(timezone.utc).astimezone(ZoneInfo(CONFIG["timezone"]))
        )
        if started:
            return f"SENT: the run opened after an earlier try ({started})", {}
    live, spare = orca_term.find_session(workspace_path(), CONFIG["session_tag"])
    if not live:
        handle = start_session(workspace_path(), spare)
        extra = {"started": True, "handle": handle}
        # A new Claude may still be loading; the next attempt finds it live and sends once it is idle.
        if not orca_term.is_idle(handle, wait_ms=90000):
            return "HOLD: the new session is still starting", extra
    else:
        # Two terminals running the same ccsession share one transcript; the newest one is the one in use.
        handle = live[0]["handle"]
        extra = {
            "handle": handle,
            "other_live_sessions": [t["handle"] for t in live[1:]],
        }
        unsafe = orca_term.typing_or_fresh(live[0])
        if unsafe:
            return f"HOLD: {unsafe}", extra
        if not orca_term.is_idle(handle):
            return "HOLD: the session is busy", extra
    if mode == "morning":
        # Each morning's report starts from an empty context, so it never pays to re-read yesterday's
        # conversation on every call (CLAY, 2026-11-03: about 546k tokens a call on 11-03). A session the
        # waker has just started is cleared too: ccsession resumes the saved conversation (2026-11-18: 40
        # hours old).
        orca_term.send(handle, "/clear", wait_submit_s=5)
        extra["cleared"] = True
        if not orca_term.is_idle(handle, wait_ms=30000):
            return "HOLD: the session is still clearing", extra
    sent_at = time.time()
    receipt = orca_term.send(handle, WAKE_LINES[mode])
    stages = receipt.get("stages") or []
    extra["receipt"] = receipt
    if mode != "morning":
        if "turn_started" in stages:
            return "SENT: " + ", ".join(stages), extra
        return (
            "DM_NEEDED: the wake line was sent but the session did not start a turn ("
            + ", ".join(stages)
            + ")",
            extra,
        )
    # A started turn only proves the session took the line: on 2026-11-18 its first request failed (429, out of
    # usage) and nothing retried, so the morning wake counts as sent only once the run folder opens. Orca can
    # also miss the turn start right after /clear (2026-11-04: "input_accepted" only, yet the report ran and
    # opened its run folder 8 seconds later), so an opened run folder proves the wake either way.
    if run_opened_since(sent_at - 5, wait_s=RUN_WAIT_S):
        return "SENT: " + ", ".join(
            stages if "turn_started" in stages else stages + ["run_opened"]
        ), extra
    error = session_error(handle)
    extra["session_error"] = error
    seen = f" (the session says: {error})" if error else ""
    if (
        "turn_started" in stages
    ):  # it took the line but is not running the report: send again next try
        return (
            f"HOLD: the session took the wake line but no report run opened{seen}",
            extra,
        )
    return (
        "DM_NEEDED: the wake line was sent but the session did not start a turn ("
        + ", ".join(stages)
        + ")"
        + seen,
        extra,
    )


def why_missed(tz, today):
    """What the morning left behind, in a sentence for the missed-report DM (2026-11-18: the DM only said
    "no daily report has finished", and Clay had to dig out that the wake had hit a usage limit)."""
    wakes = [
        r
        for r in (
            read_json(p, {})
            for p in sorted((state_dir() / "wakes").glob("*-morning.json"))
        )
        if r.get("time")
        and datetime.fromisoformat(r["time"]).astimezone(tz).date() == today
        and not r.get("outcome", "").startswith("SKIPPED")
    ]
    started = daily_run_started(datetime.now(tz))
    if started:
        why = f"the run {started} opened but has not finished"
    elif wakes:
        why = f"the 7 AM wake ended: {wakes[-1]['outcome'][:300]}"
    else:
        why = "no wake line was sent this morning (the 7 AM automation did not run or was skipped)"
    try:
        live = orca_term.find_session(workspace_path(), CONFIG["session_tag"])[0]
    except CommandError:
        live = []
    error = (wakes[-1].get("session_error") if wakes else "") or (
        session_error(live[0]["handle"]) if live else ""
    )
    return why + (f"; the coordinator session shows: {error}" if error else "")


def check_missed():
    tz = ZoneInfo(CONFIG["timezone"])
    today = datetime.now(tz).date()
    done = [
        p
        for p in runs_dir().iterdir()
        if (p / "complete.json").exists()
        and read_json(p / "complete.json")["kind"] != "hourly"
        and datetime.fromisoformat(read_json(p / "complete.json")["finished"])
        .astimezone(tz)
        .date()
        == today
    ]
    rec = {"mode": "check-missed"}
    gate = local_gate("check-missed")
    if gate:
        rec["outcome"] = f"SKIPPED: {gate}"
    else:
        rec["outcome"] = (
            f"OK: today's report finished ({done[-1].name})"
            if done
            else f"DM_NEEDED: no daily report has finished today ({today}) by {CONFIG['missed_run_dm_local']}; "
            + why_missed(tz, today)
        )
    return record(rec)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) == 2 else ""
    if mode in ("morning", "hourly"):
        wake(mode)
    elif mode == "check-missed":
        check_missed()
    else:
        sys.exit(__doc__)
