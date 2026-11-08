"""Task 4: background and detached jobs under the governed Bash adapter.

Run: uv run --no-project python -I artifacts/observe/task4.py
At most three real Claude runs (three governed print sessions, each with several Bash calls):
  run 1: setsid daemonized child, then a second Bash call
  run 2: killed supervisor with a live child, then a second Bash call
  run 3: run_in_background command, a second Bash call, the foreground reparent shape (it blocks, so it
         comes last among the shapes), then one call that records the time after it returned
Only identities, field names, hashes, selector results, tool names, exit codes, times and counts are written.
"""

import sys

sys.dont_write_bytecode = True

import json  # noqa: E402
import shlex  # noqa: E402
import uuid  # noqa: E402
from pathlib import Path  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import observe as ob  # noqa: E402
from task3 import read_hooks, tool_names  # noqa: E402

ART = ob.ART
LIMITS = ("A documented limit of the merged design (section 19.7 of docs/designs/sc-issue-launch-level-hook.md: deliberate setsid or "
          "daemonization escapes kernel-session selection, and killing the supervisor leaves stale state that selects unknown). This is an "
          "observed escape, not a failure of the harness, and nothing here claims the case is protected.")

HEAD = """#!/bin/bash
T={tmp}; R={rid}; TAG={tag}; H={helper}
W=$(cat "$T/claude-$R.pid" 2>/dev/null)
P=$$; N=0
while [ "$P" != "$W" ] && [ "${{P:-0}}" -gt 1 ]; do
  P=$(sed -E 's/^[0-9]+ \\(.*\\) [A-Za-z] ([0-9]+) .*/\\1/' "/proc/$P/stat" 2>/dev/null)
  [ -n "$P" ] || break
  N=$((N+1))
done
if [ "$P" = "$W" ]; then REACHED=yes; else REACHED=no; fi
printf 'HOPS=%s REACHED=%s\\n' "$N" "$REACHED" >> "$T/depth-$R-$TAG.txt"
now() {{ date +%s.%N; }}
ident() {{
  if [ -n "$2" ]; then out=$(/bin/bash "$H" identify "$2"); else out=$(/bin/bash "$H" identify); fi
  printf '%s\\n' "$out" | tee -a "$T/selector-$R.txt" >> "$T/sel-$R-$TAG-$1.txt"
}}
cstat() {{ sed -E 's/^.*\\) //' "/proc/$1/stat" 2>/dev/null | awk '{{print $20}}'; }}
"""

START = 'echo "$(now)" > "$T/t-$R-$TAG-start"\n'
SETSID = START + """setsid sleep 120 >/dev/null 2>&1 &
CH=$!
sleep 0.5
echo "$CH $(cstat $CH)" > "$T/child-$R-$TAG"
ident child "$CH"
ident self ""
"""
KILLED = START + """sleep 90 >/dev/null 2>&1 &
CH=$!
sleep 0.3
SS=$(sed -E 's/^.*\\) //' /proc/$CH/stat | awk '{print $4}')
echo "$CH $(cstat $CH) $SS $(cstat $SS)" > "$T/child-$R-$TAG"
ident child-before "$CH"
kill -9 "$SS"
sleep 0.5
ident child-after "$CH"
ident self ""
"""
BACKGROUND = START + """sleep 60 >/dev/null 2>&1 &
CH=$!
sleep 0.3
echo "$CH $(cstat $CH)" > "$T/child-$R-$TAG"
ident child "$CH"
ident self ""
"""
REPARENT = START + """( sleep 25 >/dev/null 2>&1 & echo $! > "$T/rp-$R" )
sleep 0.5
CH=$(cat "$T/rp-$R")
echo "$CH $(cstat $CH)" > "$T/child-$R-$TAG"
ident child "$CH"
ident self ""
echo "$(now)" > "$T/t-$R-$TAG-end-of-script"
"""
TIMESTAMP = START + 'ident self ""\n'


def second(prev):
    return (START + 'for i in $(seq 1 50); do [ -s "$T/child-$R-%s" ] && break; sleep 0.2; done\n'
            'read CH CST _ < "$T/child-$R-%s"\nident child "$CH"\nident self ""\n') % (prev, prev)


def mk(g, rid, tag, body):
    path = g.tmp / ("cmd-%s-%s.sh" % (rid, tag))
    path.write_text(HEAD.format(tmp=shlex.quote(str(g.tmp)), rid=rid, tag=tag, helper=shlex.quote(str(ob.HELPER))) + body)
    return path


def lines(g, rid, tag, label):
    p = g.tmp / ("sel-%s-%s-%s.txt" % (rid, tag, label))
    if not p.exists():
        return None
    for line in p.read_text(errors="replace").splitlines():
        try:
            found = ob.identities(json.loads(line))
        except ValueError:
            continue
        if found:
            return dict(found[0], line_sha256=ob.sha(line))
    return None


def start_time(g, rid, tag, suffix="start"):
    p = g.tmp / ("t-%s-%s-%s" % (rid, tag, suffix))
    return float(p.read_text().strip()) if p.exists() else None


def depth(g, rid, tag):
    p = g.tmp / ("depth-%s-%s.txt" % (rid, tag))
    if p.exists():
        import re
        m = re.search(r"HOPS=(\d+) REACHED=(yes|no)", p.read_text())
        if m:
            return {"hops": int(m.group(1)), "claude_process_reached": m.group(2) == "yes"}
    return None


def child(g, rid, tag):
    p = g.tmp / ("child-%s-%s" % (rid, tag))
    if p.exists():
        f = p.read_text().split()
        out = {"pid": int(f[0]), "start_ticks": int(f[1]) if len(f) > 1 and f[1].isdigit() else None}
        if len(f) > 3:
            out["supervisor_pid"] = int(f[2])
            out["supervisor_start_ticks"] = int(f[3]) if f[3].isdigit() else None
        return out
    return None


def session(runner, g, case_id, label, scripts, prompt, timeout):
    sid = str(uuid.uuid4())
    g.make_governed(sid)
    rid = ob.new_rid()
    paths = {tag: mk(g, rid, tag, body) for tag, body in scripts}
    log = g.tmp / ("hook-events-%s.jsonl" % rid)
    settings = ob.write_settings(g, "governed", log)
    argv = ob.claude_argv(ob.claude_bin(), settings, sid, prompt(paths), tools=("Bash",), persist=False)
    res = runner.run(g, case_id, argv, label=label, timeout=timeout, real_claude=True, ok_result="observed", classify=ob.classify_claude, rid=rid, sid=sid)
    events, init = ob.parse_stream(res["out"])
    ex = res["extra"]
    hooks = read_hooks(log)
    return {"run_id": rid, "session_id": sid, "ledger_exit": res["exit"], "result": res["result"], "held_s": res["held_s"],
            "timed_out": res["timed_out"], "tool_names": tool_names(res["out"]), "stream_event_types": [e["type"] for e in events if e.get("type")],
            "failure": {k: ex[k] for k in ("reason", "assistant_error_category", "result_subtype", "result_is_error", "api_error_status", "refusal_observed") if k in ex},
            "hook_events": hooks, "bash_calls_seen_by_hook": sum(1 for h in hooks if h.get("hook_event_name") == "PreToolUse"),
            "ran_a_tool": any(h.get("hook_event_name") == "PostToolUse" for h in hooks) or bool(list(g.tmp.glob("sel-%s-*" % rid)))}


def seq_prompt(paths, tags, bg_first=False):
    cmds = ["/bin/bash " + shlex.quote(str(paths[t])) for t in tags]
    text = ("Use the Bash tool to run these commands, each exactly once. Run them one at a time, in this order, starting each only after the "
            "previous one has returned")
    if bg_first:
        text = ("Use the Bash tool to run these commands, each exactly once, in this order. Run command 1 with the Bash tool parameter "
                "run_in_background set to true and do not wait for it. Then run commands 2 to %d in the foreground, one at a time, starting each only "
                "after the previous one has returned" % len(cmds))
    return text + ". Report only their outputs: " + " ".join("%d) %s" % (i + 1, c) for i, c in enumerate(cmds))


def shape_entry(name, run, **fields):
    e = {"shape": name, "run_id": run["run_id"], "session_id": run["session_id"], "result": "observed" if run["result"] == "observed" else "unavailable"}
    e.update(fields)
    return e


def unavailable(name, why):
    return {"shape": name, "result": "unavailable", "missing_interface": why}


def main():
    runner = ob.Runner()
    g = ob.Group.create("t4")
    out = {"task": 4, "runs": [], "shapes": {}}
    children = []
    stop_reason = None
    try:
        # Run 1: setsid daemonized child, then a second Bash tool call.
        r1 = session(runner, g, "t4-setsid", "task4: governed session, setsid daemon child and a second Bash call",
                     [("a", SETSID), ("b", second("a"))], lambda p: seq_prompt(p, ["a", "b"]), 150)
        out["runs"].append({k: v for k, v in r1.items() if k != "hook_events"})
        rid = r1["run_id"]
        if r1["ledger_exit"] != 0 and not r1["ran_a_tool"]:
            stop_reason = "the first run failed before any tool ran: %s" % r1["failure"]
        ch = child(g, rid, "a")
        children.append(("setsid-daemon", ch))
        out["shapes"]["setsid_daemon"] = shape_entry("setsid daemonized child", r1, descendant_pid=ch and ch["pid"],
            descendant_status_inside_same_command=lines(g, rid, "a", "child"), command_self_status_inside=lines(g, rid, "a", "self"),
            second_bash_tool_call={"is_a_governed_call": True, "descendant_status": lines(g, rid, "b", "child"), "own_status": lines(g, rid, "b", "self"),
                                   "depth": depth(g, rid, "b")}, depth=depth(g, rid, "a"), documented_limit=LIMITS)
        # Run 2: killed supervisor with a live child.
        if not stop_reason:
            r2 = session(runner, g, "t4-killed-supervisor", "task4: governed session, supervisor killed while a child lives, then a second Bash call",
                         [("a", KILLED), ("b", second("a"))], lambda p: seq_prompt(p, ["a", "b"]), 150)
            out["runs"].append({k: v for k, v in r2.items() if k != "hook_events"})
            rid = r2["run_id"]
            ch = child(g, rid, "a")
            children.append(("killed-supervisor", ch))
            out["shapes"]["killed_supervisor"] = shape_entry("command whose supervisor is killed while a child lives", r2, descendant_pid=ch and ch["pid"],
                supervisor_pid=ch and ch.get("supervisor_pid"), descendant_status_before_kill=lines(g, rid, "a", "child-before"),
                descendant_status_after_kill=lines(g, rid, "a", "child-after"), command_self_status_after_kill=lines(g, rid, "a", "self"),
                second_bash_tool_call={"is_a_governed_call": True, "descendant_status": lines(g, rid, "b", "child"), "own_status": lines(g, rid, "b", "self"),
                                       "depth": depth(g, rid, "b")}, depth=depth(g, rid, "a"), documented_limit=LIMITS)
        # Run 3: run_in_background, second call, foreground reparent (blocks), then a timestamp call.
        if not stop_reason:
            r3 = session(runner, g, "t4-background-reparent", "task4: governed session, run_in_background command, second call, foreground reparent, timestamp call",
                         [("a", BACKGROUND), ("b", second("a")), ("c", REPARENT), ("d", TIMESTAMP)], lambda p: seq_prompt(p, ["a", "b", "c", "d"], bg_first=True), 240)
            out["runs"].append({k: v for k, v in r3.items() if k != "hook_events"})
            rid = r3["run_id"]
            flags = [h.get("run_in_background") for h in r3["hook_events"] if h.get("hook_event_name") == "PreToolUse"]
            ch_a, ch_c = child(g, rid, "a"), child(g, rid, "c")
            children += [("run-in-background", ch_a), ("foreground-reparent", ch_c)]
            t_c, t_d = start_time(g, rid, "c"), start_time(g, rid, "d")
            out["shapes"]["run_in_background"] = shape_entry("ordinary run_in_background Bash command", r3, descendant_pid=ch_a and ch_a["pid"],
                bash_tool_calls_run_in_background_flags_seen_by_hook=flags, descendant_status_inside_same_command=lines(g, rid, "a", "child"),
                command_self_status_inside=lines(g, rid, "a", "self"),
                second_bash_tool_call={"is_a_governed_call": True, "descendant_status": lines(g, rid, "b", "child"), "own_status": lines(g, rid, "b", "self"),
                                       "depth": depth(g, rid, "b")}, depth=depth(g, rid, "a"))
            out["shapes"]["foreground_reparent"] = shape_entry("foreground command whose descendant is reparented", r3, descendant_pid=ch_c and ch_c["pid"],
                descendant_status_inside_same_command_before_it_exits=lines(g, rid, "c", "child"), command_self_status_inside=lines(g, rid, "c", "self"),
                observed_wait_seconds_until_the_next_bash_call_started=(round(t_d - t_c, 2) if t_c and t_d else None),
                descendant_sleep_seconds=25, depth=depth(g, rid, "c"),
                timestamp_call={"own_status": lines(g, rid, "d", "self"), "depth": depth(g, rid, "d")},
                wait_note="the wait is the time from the start of the foreground command to the start of the next Bash tool call, both written by the commands themselves")
    finally:
        # Account for every started child before the teardown stops what is still alive.
        for label, ch in children:
            if ch and ch.get("start_ticks"):
                state = "alive-at-teardown-start" if ob.alive(ch["pid"], ch["start_ticks"]) else "already-ended"
                ob.cleanup_log("group=t4 case=task4 child label=%s pid=%d start=%d %s" % (label, ch["pid"], ch["start_ticks"], state))
                if ch.get("supervisor_pid") and ch.get("supervisor_start_ticks"):
                    s2 = "alive-at-teardown-start" if ob.alive(ch["supervisor_pid"], ch["supervisor_start_ticks"]) else "already-ended"
                    ob.cleanup_log("group=t4 case=task4 supervisor label=%s pid=%d start=%d %s" % (label, ch["supervisor_pid"], ch["supervisor_start_ticks"], s2))
        out["teardown"] = g.teardown("task4")
        (ob.GROUPS / "t4.json").unlink()
    if stop_reason:
        for name in ("setsid_daemon", "killed_supervisor", "run_in_background", "foreground_reparent"):
            if name not in out["shapes"] or out["shapes"][name]["result"] == "unavailable":
                out["shapes"][name] = unavailable(name, "a real Claude run failed before any tool ran (%s); no further run spent" % stop_reason)
        out["stopped"] = stop_reason
    for name in ("setsid_daemon", "killed_supervisor", "run_in_background", "foreground_reparent"):
        out["shapes"].setdefault(name, unavailable(name, "the run that holds this shape did not run"))
        e = out["shapes"][name]
        if e["result"] == "observed" and not (e.get("descendant_status_inside_same_command") or e.get("descendant_status_inside_same_command_before_it_exits")
                                              or e.get("descendant_status_before_kill")):
            e["result"] = "unavailable"
            e["missing_interface"] = "no selector line was captured for this shape in its run (the command did not run, or the model did not follow the prompt)"
    (ART / "background-jobs.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: v["result"] for k, v in out["shapes"].items()}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
