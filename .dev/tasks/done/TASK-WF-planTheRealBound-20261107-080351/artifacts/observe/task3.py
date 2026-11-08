"""Task 3: resume, fork and /clear against an old live governed child.

Run: uv run --no-project python -I artifacts/observe/task3.py
At most four real Claude runs: initial, resume, fork, and one owner-authorized interactive
/clear run (300 second wall-clock timeout, exactly two prompts, no retry). Only identities,
field names, hashes, selector results, tool names, exit codes and counts are written.
"""

import sys

sys.dont_write_bytecode = True

import fcntl  # noqa: E402
import json  # noqa: E402
import os  # noqa: E402
import pty  # noqa: E402
import re  # noqa: E402
import select  # noqa: E402
import signal  # noqa: E402
import struct  # noqa: E402
import subprocess  # noqa: E402
import termios  # noqa: E402
import time  # noqa: E402
import uuid  # noqa: E402
from pathlib import Path  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import observe as ob  # noqa: E402

ART = ob.ART
SLEEP_S = 900
FIRST_BODY = """sleep %d >/dev/null 2>&1 &
CH=$!
SEL=$(/bin/bash %s identify "$CH")
printf '%%s\\n' "$SEL" | tee -a "$T/selector-$R.txt"
ST=$(sed -E 's/^.*\\) //' /proc/$CH/stat | awk '{print $20}')
SS=$(sed -E 's/^.*\\) //' /proc/$CH/stat | awk '{print $4}')
SST=$(sed -E 's/^.*\\) //' /proc/$SS/stat 2>/dev/null | awk '{print $20}')
BOOT=$(cat /proc/sys/kernel/random/boot_id)
printf 'child_pid=%%s child_start=%%s supervisor_pid=%%s supervisor_start=%%s boot=%%s\\n' "$CH" "$ST" "$SS" "$SST" "$BOOT" > "$T/ready-$R.tmp"
mv "$T/ready-$R.tmp" "$T/ready-$R"
"""
NEXT_BODY = """/bin/bash %s identify %d | tee -a "$T/selector-$R.txt"
/bin/bash %s identify | tee -a "$T/selector-$R.txt"
"""


def tool_names(path):
    names = []
    try:
        lines = Path(path).read_text(errors="replace").splitlines()
    except OSError:
        return names
    for line in lines:
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        msg = ev.get("message") if isinstance(ev, dict) else None
        if isinstance(msg, dict) and isinstance(msg.get("content"), list):
            for b in msg["content"]:
                if isinstance(b, dict) and b.get("type") == "tool_use" and isinstance(b.get("name"), str) and re.fullmatch(r"[A-Za-z_]{1,40}", b["name"]):
                    names.append(b["name"])
    return names


def read_hooks(path):
    out = []
    if Path(path).exists():
        for line in Path(path).read_text().splitlines():
            try:
                out.append(json.loads(line))
            except ValueError:
                pass
    return out


def child_state(pid, start):
    f = ob.proc_fields(pid)
    return {"pid": pid, "start_ticks_recorded": start, "alive": bool(f and f["state"] != "Z" and f["start"] == start),
            "identity_changed": bool(f and f["state"] != "Z" and f["start"] != start),
            "start_ticks_now": f["start"] if f and f["state"] != "Z" else None}


def runner_side_identify(g, pid):
    """The runner reads the old child's selector status itself; labelled as a runner-side read."""
    r = subprocess.run(["/bin/bash", str(ob.HELPER), "identify", str(pid)], env=g.env(), capture_output=True, text=True, timeout=30)
    found = ob.identities(r.stdout)
    return found[0] if found else {"status": "no selector line"}


def case(runner, g, case_id, sid, label, body, *, resume=None, fork=False, timeout=180, planned_kill=False, record_sid=None):
    rid = ob.new_rid()
    script = ob.write_cmd(g, rid, body)
    log = g.tmp / ("hook-events-%s.jsonl" % rid)
    settings = ob.write_settings(g, "governed", log)
    ready = g.tmp / ("ready-%s" % rid)
    argv = ob.claude_argv(ob.claude_bin(), settings, sid, ob.prompt_for(script), tools=("Bash",), persist=True, resume=resume, fork=fork)
    box = {"measured": False}

    def classify(rc, mp):
        found = ob.depth_capture(g, rid)
        if found:
            box.update(found, measured=True)
        if planned_kill and rc == -signal.SIGKILL and ready.exists():
            return "observed", {"end": "planned SIGKILL to the first Claude process after the ready file appeared"}
        return ob.classify_claude(rc, mp)

    kw = dict(ready=ready, signal_name="SIGKILL") if planned_kill else {}
    res = runner.run(g, case_id, argv, label=label, timeout=timeout, real_claude=True, ok_result="observed", classify=classify,
                     rid=rid, sid=record_sid or sid, depth=box, **kw)
    events, init = ob.parse_stream(res["out"])
    ex = res["extra"]
    return {
        "run_id": rid, "ledger_exit": res["exit"], "result": res["result"], "held_s": res["held_s"], "timed_out": res["timed_out"],
        "signal": res["signal"], "ready_file_seen": ready.exists(), "ready": read_ready(ready), "store_check": ex.get("store_check"),
        "failure": {k: ex[k] for k in ("reason", "assistant_error_category", "result_subtype", "result_is_error", "api_error_status", "refusal_observed") if k in ex},
        "tool_names": tool_names(res["out"]), "stream_event_types": [e["type"] for e in events if e.get("type")],
        "stream_session_ids": sorted({e["session_id"] for e in events if e.get("session_id")}),
        "hook_events": read_hooks(log), "selector_lines_in_order": ob.selector_capture(g, rid), "depth": box,
    }


def read_ready(path):
    out = {}
    if Path(path).exists():
        for kv in Path(path).read_text().split():
            if "=" in kv:
                k, v = kv.split("=", 1)
                out[k] = v
    return out


def hook_session(c):
    for h in c["hook_events"]:
        if h.get("hook_event_name") == "PreToolUse" and h.get("session_id"):
            return h["session_id"]
    return None


def entry_from(c, old, label):
    """One resume/fork entry from a run that identified the old child first and itself second."""
    sel = c["selector_lines_in_order"]
    ok = c["result"] == "observed" and len(sel) >= 2
    e = {"result": "observed" if ok else "unavailable", "run_id": c["run_id"], "ledger_exit": c["ledger_exit"], "tool_names": c["tool_names"],
         "check_before_run": c["store_check"], "hook_event_session_id": hook_session(c), "depth": c["depth"],
         "old_child": {"in_new_process_selector_status": sel[0]["status"] if sel else None,
                       "origin_session_id": sel[0].get("session_id") if sel else None,
                       "pid": old["pid"], "start_ticks_before_new_process": old["start"], "start_ticks_after_new_process": old.get("after")},
         "new_process": {"selector_status": sel[1]["status"] if len(sel) > 1 else None,
                         "session_id": sel[1].get("session_id") if len(sel) > 1 else None},
         "selector_lines": sel}
    if not ok:
        e["missing_interface"] = "the %s run did not produce both selector lines (exit %s, result %s, failure %s)" % (label, c["ledger_exit"], c["result"], c["failure"])
    return e


def interactive_clear(runner, g, sid_pty, old, sid_origin, timeout=300):
    """The one owner-authorized interactive run: pty, /clear, one governed command, then end the process.

    old is the old child's {"pid", "start"} (or None when it did not survive); sid_origin is the session id
    whose governed record the old child belongs to.
    """
    rid = ob.new_rid()
    old_pid = old["pid"] if old else 0
    if runner.real_count() >= runner.cap:
        raise ob.Refused("real Claude run cap reached")
    check_before = g.store_check(sid_origin)
    old_before = child_state(old["pid"], old["start"]) if old else None
    script = ob.write_cmd(g, rid, NEXT_BODY % (ob.shlex.quote(str(ob.HELPER)), old_pid, ob.shlex.quote(str(ob.HELPER))))
    log = g.tmp / ("hook-events-%s.jsonl" % rid)
    settings = ob.write_settings(g, "governed", log)
    argv = [ob.claude_bin(), "--setting-sources", "", "--settings", str(settings), "--session-id", sid_pty, "--tools", "Bash",
            "--allowedTools", "Bash", "--permission-mode", "dontAsk", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}', "--no-chrome"]
    flags = sorted({a for a in argv if a.startswith("--")})
    master, slave = pty.openpty()
    fcntl.ioctl(master, termios.TIOCSWINSZ, struct.pack("HHHH", 50, 160, 0, 0))
    settings_before = ob.real_settings_sha()
    t0 = time.time()
    started = ob.now()
    before = g.procs_under()
    p = subprocess.Popen(argv, env=g.env(), cwd=g.fixture, stdin=slave, stdout=slave, stderr=slave, start_new_session=True,
                         preexec_fn=lambda: fcntl.ioctl(0, termios.TIOCSCTTY, 0))
    os.close(slave)
    mp = ob.ManagedProc.__new__(ob.ManagedProc)
    mp.p, mp.pid, mp.name, mp.start, mp.boot = p, p.pid, "clear-" + rid, ob.proc_start(p.pid), ob.boot_id()
    (g.tmp / ("claude-%s.pid" % rid)).write_text(str(p.pid))
    buf = bytearray()
    last = [time.time()]
    seen = {"output_bytes": 0, "dialogs_answered": []}
    sel_file = g.tmp / ("selector-%s.txt" % rid)

    def pump(seconds):
        end = time.time() + seconds
        while time.time() < end and p.poll() is None:
            r, _, _ = select.select([master], [], [], 0.2)
            if r:
                try:
                    data = os.read(master, 65536)
                except OSError:
                    return
                if data:
                    buf.extend(data)
                    seen["output_bytes"] += len(data)
                    last[0] = time.time()
                    del buf[:-20000]

    def quiet(seconds, limit):
        end = time.time() + limit
        while time.time() < end and p.poll() is None and time.time() - t0 < timeout:
            pump(0.5)
            if time.time() - last[0] >= seconds and seen["output_bytes"] > 0:
                return True
        return False

    def dialogs():
        low = bytes(buf).lower()
        for key, needle in (("folder_trust", b"trust"), ("onboarding", b"press enter")):
            if needle in low and key not in seen["dialogs_answered"]:
                os.write(master, b"\r")
                seen["dialogs_answered"].append(key)
                del buf[:]
                return True
        return False

    stages = {}
    prompts = 0
    try:
        # Startup: answer a folder-trust or onboarding dialog at most once each, then wait for the screen to settle.
        for _ in range(6):
            stages["startup_quiet"] = quiet(4, 40)
            if not dialogs():
                break
        if p.poll() is None and stages["startup_quiet"]:
            os.write(master, b"/clear")
            time.sleep(0.5)
            os.write(master, b"\r")
            prompts += 1
            stages["after_clear_quiet"] = quiet(3, 30)
        if p.poll() is None and stages.get("after_clear_quiet"):
            os.write(master, ob.prompt_for(script).encode())
            time.sleep(0.5)
            os.write(master, b"\r")
            prompts += 1
            end = time.time() + 120
            while time.time() < min(end, t0 + timeout) and p.poll() is None:
                pump(0.5)
                if sel_file.exists() and len(sel_file.read_text().splitlines()) >= 2:
                    stages["selector_lines_seen"] = True
                    break
            quiet(3, 20)  # let the reply finish
    finally:
        timed_out = time.time() - t0 >= timeout
        end_action = None
        if p.poll() is None:
            res = mp.signal(signal.SIGTERM)
            end_action = {"signal": "SIGTERM", "target": "the spawned process only (own child handle, no process group)", "sent": res["sent"]}
            try:
                p.wait(timeout=8)
            except subprocess.TimeoutExpired:
                res = mp.signal(signal.SIGKILL)
                end_action["then"] = {"signal": "SIGKILL", "sent": res["sent"]}
                p.wait(timeout=5)
        mp.kill_group()
        screen_tail = bytes(buf).decode(errors="replace")
        os.close(master)
    rc = p.returncode
    swept = g.sweep(before, "t3-clear") if timed_out else 0
    old_after = child_state(old["pid"], old["start"]) if old else None
    sel = ob.selector_capture(g, rid)
    sessions, names = set(), []
    for f in (g.home / ".claude").rglob("*.jsonl"):
        if f.stat().st_mtime < t0:
            continue  # only transcripts written during this run, not those of earlier runs in the shared HOME
        for line in f.read_text(errors="replace").splitlines():
            try:
                ev = json.loads(line)
            except ValueError:
                continue
            if isinstance(ev, dict) and isinstance(ev.get("sessionId"), str) and ob.ID.fullmatch(ev["sessionId"]):
                sessions.add(ev["sessionId"])
        names += tool_names(f)
    hooks = read_hooks(log)
    done = len(sel) >= 2
    result = "blocked" if timed_out and not done else ("observed" if done else "unavailable")
    elapsed = round(time.time() - t0, 2)
    runner.log(run_id=rid, case_id="t3-clear-interactive", label="task3: owner-authorized interactive pty session, /clear, one governed command", group=g.name,
               start=started, end=ob.now(), exit=("signal:" + signal.Signals(-rc).name) if rc < 0 else rc, real_claude=True, depth=ob.depth_capture(g, rid) or {"measured": False},
               result=result, held_s=elapsed, timed_out=timed_out, swept=swept, settings_sha256_before=settings_before,
               settings_sha256_after=ob.real_settings_sha(),
               extra={"store_check": check_before, "prompts_sent": prompts, "dialogs_answered": seen["dialogs_answered"],
                      "flag_names": flags, "end_action": end_action, "stages": stages})
    entry = {
        "result": result if done else "unavailable", "run_id": rid, "prompts_sent": prompts, "elapsed_seconds": elapsed,
        "wall_clock_bound_seconds": timeout, "timed_out": timed_out, "dialogs_answered_before_prompts": seen["dialogs_answered"],
        "stages": stages, "how_the_process_was_ended": end_action, "flag_names_used": flags,
        "session_ids_in_hook_events": [h.get("session_id") for h in hooks if h.get("hook_event_name") == "PreToolUse"],
        "check_before_run": check_before,
        "old_child": {"pid": old_pid, "start_ticks_before_new_process": old_before and old_before["start_ticks_recorded"],
                      "alive_before": old_before and old_before["alive"], "start_ticks_after_new_process": old_after and old_after["start_ticks_now"],
                      "alive_after": old_after and old_after["alive"]},
        "printed_cost": sorted(set(re.findall(r"\$\s?\d+(?:\.\d+)?", screen_tail))) or "none seen in the retained screen tail (last 20000 bytes)",
        "session_ids_in_transcripts_written_during_this_run": sorted(sessions), "starting_session_id": sid_pty,
        "tool_names_in_transcripts_written_during_this_run": names,
        "old_child_selector_status": sel[0]["status"] if sel else None, "old_child_origin_session_id": sel[0].get("session_id") if sel else None,
        "new_session_selector_status": sel[1]["status"] if len(sel) > 1 else None, "new_session_selector_session_id": sel[1].get("session_id") if len(sel) > 1 else None,
        "selector_lines": sel, "hook_event_records": hooks,
    }
    if not done:
        entry["missing_interface"] = ("a pty-driven interactive Claude session could not be driven to a /clear plus one governed command within the %d second bound "
                                      "(stages reached: %s; output bytes read: %d; process exit: %s)" % (timeout, stages, seen["output_bytes"], rc))
    return entry


def main():
    runner = ob.Runner()
    g = ob.Group.create("t3")
    out = {"task": 3, "sleep_seconds_of_old_child": SLEEP_S}
    sid1 = str(uuid.uuid4())
    try:
        g.make_governed(sid1)
        first = case(runner, g, "t3-first", sid1, "task3: governed session starts one ordinary background child", FIRST_BODY % (SLEEP_S, ob.shlex.quote(str(ob.HELPER))),
                     timeout=120, planned_kill=True)
        rd = first["ready"]
        ok_ready = first["ready_file_seen"] and all(k in rd for k in ("child_pid", "child_start", "supervisor_pid", "supervisor_start", "boot"))
        entry = {"run_id": first["run_id"], "origin_session_id": sid1, "ledger_exit": first["ledger_exit"], "result": first["result"],
                 "call_returned_while_child_lived": (not first["ready_file_seen"]) and first["ledger_exit"] == 0,
                 "seconds_held": first["held_s"], "ready_file_sighted": first["ready_file_seen"], "tool_names": first["tool_names"],
                 "end_action": first["signal"], "child_selector_before_kill": first["selector_lines_in_order"], "failure": first["failure"],
                 "hook_event_session_id": hook_session(first), "depth": first["depth"], "same_boot": rd.get("boot") == ob.boot_id()}
        out["first_call"] = entry
        old = None
        if ok_ready:
            cp, cs, sp, ss = int(rd["child_pid"]), int(rd["child_start"]), int(rd["supervisor_pid"]), int(rd["supervisor_start"])
            before_kill = {"child": {"pid": cp, "start_ticks": cs}, "supervisor": {"pid": sp, "start_ticks": ss}, "boot_identity": rd["boot"]}
            after_kill = {"child": child_state(cp, cs), "supervisor": child_state(sp, ss), "boot_identity_unchanged": rd["boot"] == ob.boot_id()}
            entry["before_kill_from_ready_file"] = before_kill
            entry["after_kill_before_resume"] = after_kill
            if after_kill["child"]["alive"] and after_kill["supervisor"]["alive"]:
                g.register_survivor("t3-old-governed-child", cp, supervisor=sp)
                old = {"pid": cp, "start": cs, "sup": sp, "sup_start": ss}
                entry["runner_side_identify_before_resume"] = runner_side_identify(g, cp)
            else:
                entry["label"] = "job did not survive the first Claude process ending" if not (after_kill["child"]["identity_changed"]) else "child identity changed"
        else:
            entry["label"] = "job did not survive the first Claude process ending" if first["ready_file_seen"] is False else "ready file incomplete"
            entry["note"] = "the first Claude process ended before the ready file appeared or the file was incomplete; this end is recorded as observed, not as the planned kill"
        why_gone = "job did not survive the first Claude process ending"
        if not old:
            for k in ("resume", "fork", "decisive_case"):
                out[k] = {"result": "unavailable", "missing_interface": entry.get("label", why_gone), "detail": "no substitute child was started"}
        else:
            shell = ob.shlex.quote(str(ob.HELPER))
            body = NEXT_BODY % (shell, old["pid"], shell)
            for name, fork in (("resume", False), ("fork", True)):
                c = case(runner, g, "t3-" + name, sid1, "task3: %s the killed session in a new Claude process, identify old child and self" % name, body,
                         resume=sid1, fork=fork, timeout=180, record_sid=sid1)
                state = child_state(old["pid"], old["start"])
                old["after"] = state["start_ticks_now"]
                e = entry_from(c, old, name)
                e["old_child_alive_after_new_process"] = state["alive"]
                e["same_identities"] = bool(e["old_child"]["origin_session_id"] and e["new_process"]["session_id"] and e["old_child"]["origin_session_id"] == e["new_process"]["session_id"])
                e["runner_side_identify_after"] = runner_side_identify(g, old["pid"])
                out[name] = e
                if name == "resume" and e["result"] == "unavailable":
                    out["fork"] = {"result": "unavailable", "missing_interface": "the killed session could not be resumed: %s" % e.get("missing_interface"), "detail": "no retry"}
                    break
        # /clear: the one owner-authorized interactive run (still attempted when the old child is gone; its old-child line is then unreadable).
        out["clear"] = interactive_clear(runner, g, str(uuid.uuid4()), old, sid1)
    finally:
        out["teardown"] = g.teardown("task3")
        (ob.GROUPS / "t3.json").unlink()
    # The decisive case: an old governed child alive while a new ordinary session starts.
    dec = {"result": "unavailable", "missing_interface": "no run observed both an old governed child and a new ordinary session"}
    for src in ("fork", "clear"):
        e = out.get(src, {})
        if src == "fork" and e.get("result") == "observed":
            oc, npr = e["old_child"], e["new_process"]
            dec = {"result": "observed", "source": "fork", "old_child_status": oc["in_new_process_selector_status"], "old_child_origin_session_id": oc["origin_session_id"],
                   "new_session_status": npr["selector_status"], "new_session_id": npr["session_id"],
                   "distinct_identities": oc["in_new_process_selector_status"] == "governed" and npr["selector_status"] == "ordinary"}
            break
        if src == "clear" and e.get("result") == "observed":
            dec = {"result": "observed", "source": "clear", "old_child_status": e["old_child_selector_status"], "old_child_origin_session_id": e["old_child_origin_session_id"],
                   "new_session_status": e["new_session_selector_status"], "distinct_identities": e["old_child_selector_status"] == "governed" and e["new_session_selector_status"] == "ordinary"}
    if out.get("decisive_case", {}).get("result") != "unavailable":
        out["decisive_case"] = dec
    if "decisive_case" not in out:
        out["decisive_case"] = dec
    (ART / "resume-fork-clear.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: (v.get("result") if isinstance(v, dict) else v) for k, v in out.items()}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
