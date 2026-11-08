"""Task 5: release, PID reuse and boot-identity rejection with controlled processes.

Run: uv run --no-project python -I artifacts/observe/task5.py
No real Claude run is spent. Jobs are started through the helper's own prepare and run actions by this
runner (not by a person or a Claude session), and a job record in the throwaway HOME is edited. Every
result is labelled controlled and is never reported as real harness behavior.
"""

import sys

sys.dont_write_bytecode = True

import json  # noqa: E402
import os  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402
import uuid  # noqa: E402
from pathlib import Path  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import observe as ob  # noqa: E402

ART = ob.ART
HELPER = ob.HELPER


def helper_line(needle):
    """The 1-based line of the helper that holds the given text, found now rather than remembered."""
    for n, line in enumerate(HELPER.read_text().splitlines(), 1):
        if needle in line:
            return "src/superclaude/hooks/scripts/launch-job-identity.sh:%d" % n
    return "not found: " + needle


def identify(g, pid):
    r = subprocess.run(["/bin/bash", str(HELPER), "identify", str(pid)], env=g.env(), capture_output=True, text=True, timeout=30)
    found = ob.identities(r.stdout)
    item = dict(found[0]) if found else {"status": "no selector line"}
    item["line_sha256"] = ob.sha(r.stdout.strip())
    return item


def start_job(g, sid, name):
    """A registered job under a governed session, started with the helper's own prepare and run actions."""
    g.make_governed(sid)
    token = subprocess.run(["/bin/bash", str(HELPER), "prepare", sid, "sleep 600"], env=g.env(), capture_output=True, text=True, timeout=30).stdout.strip()
    mp = g.spawn(["/bin/bash", str(HELPER), "run", token], "job-" + name)
    jobs = g.store_dir() / "jobs"
    rec_path, rec = None, None
    for _ in range(100):
        if jobs.is_dir():
            for p in jobs.glob("*.json"):
                try:
                    v = json.loads(p.read_text())
                except ValueError:
                    continue
                if v.get("session_id") == sid:
                    rec_path, rec = p, v
        if rec:
            break
        time.sleep(0.1)
    if not rec:
        raise SystemExit("job record for %s did not appear" % name)
    sup = rec["pid"]
    child = None
    for _ in range(100):
        for entry in os.listdir("/proc"):
            if entry.isdecimal() and int(entry) != sup:
                f = ob.proc_fields(int(entry))
                if f and f["sid"] == sup and f["state"] != "Z":
                    child = int(entry)
        if child:
            break
        time.sleep(0.1)
    if not child:
        raise SystemExit("job child for %s did not appear" % name)
    return {"name": name, "session_id": sid, "record_path": rec_path, "record": rec, "supervisor_pid": sup, "child_pid": child, "runner_handle": mp}


def edit_record(job, field, value):
    """Replace one field of the job record, keeping it owner-only (0400) with one link."""
    path = job["record_path"]
    rec = json.loads(path.read_text())
    before = rec[field]
    rec[field] = value
    tmp = path.with_name(".edit-" + uuid.uuid4().hex)
    tmp.write_text(json.dumps(rec, separators=(",", ":")))
    os.chmod(tmp, 0o400)
    os.replace(tmp, path)
    st = os.stat(path)
    return {"field_edited": field, "mode_octal": oct(st.st_mode & 0o777), "link_count": st.st_nlink, "owner_is_current_user": st.st_uid == os.geteuid(),
            "value_changed": before != value}


def main():
    runner = ob.Runner()
    g = ob.Group.create("t5")
    cites = {
        "tick_and_boot_comparison": helper_line("start != value['start'] or boot() != value['boot']"),
        "release_returns_ordinary_released": helper_line("'reason': 'released'"),
        "owner_only_state_check": helper_line("st.st_mode & 0o077"),
        "single_link_check": helper_line("st.st_nlink != 1"),
        "job_record_built_at_registration": helper_line("record = {'pid': sid"),
        "job_record_published": helper_line("publish(jobs, name, record)"),
    }
    out = {"task": 5, "label": "controlled", "cites": cites,
           "why_controlled": "the processes were started by this runner through the helper's own prepare and run actions, not by a real Claude, Orca or Git actor, and the job record was edited in the throwaway HOME; none of this is real harness behavior"}
    jobs = {}
    try:
        t0 = ob.now()
        # Case 1: release while a governed child is alive; a second governed session's child stays governed.
        s1, s2 = str(uuid.uuid4()), str(uuid.uuid4())
        jobs["j1"], jobs["j2"] = start_job(g, s1, "release-1"), start_job(g, s2, "release-2")
        before1, before2 = identify(g, jobs["j1"]["child_pid"]), identify(g, jobs["j2"]["child_pid"])
        (g.store_dir() / "sessions" / s1).unlink()  # the person's release route: delete that session's level record
        after1, after2 = identify(g, jobs["j1"]["child_pid"]), identify(g, jobs["j2"]["child_pid"])
        out["release"] = {
            "label": "controlled", "reason": "two governed sessions each with one live job child started by the runner; the first session's level record deleted",
            "session_1": {"session_id": s1, "live_child_pid": jobs["j1"]["child_pid"], "before": before1, "after_release": after1},
            "session_2": {"session_id": s2, "live_child_pid": jobs["j2"]["child_pid"], "before": before2, "after_release": after2},
            "only_the_released_sessions_child_changed": before1["status"] == "governed" and after1["status"] == "ordinary" and after1.get("reason") == "released"
                                                          and before2["status"] == "governed" and after2["status"] == "governed" and after2.get("session_id") == s2,
            "cites": [cites["release_returns_ordinary_released"]]}
        runner.log(run_id=ob.new_rid(), case_id="t5-release", label="task5: release while a governed child is alive (controlled)", group="t5", start=t0, end=ob.now(),
                   exit=0, real_claude=False, depth=None, result="controlled", extra={"statuses": [before1["status"], after1["status"], before2["status"], after2["status"]]})

        # Case 2: recorded process start ticks no longer match the live process (as after PID reuse).
        t0 = ob.now()
        s3 = str(uuid.uuid4())
        jobs["j3"] = start_job(g, s3, "start-ticks")
        control3 = identify(g, jobs["j3"]["child_pid"])  # governed control child of the same record, before the edit
        edit3 = edit_record(jobs["j3"], "start", jobs["j3"]["record"]["start"] + 1)
        after3 = identify(g, jobs["j3"]["child_pid"])
        out["start_tick_mismatch"] = {
            "label": "controlled", "reason": "the recorded start ticks of a live registered job were edited so they no longer match the live supervisor, as after PID reuse",
            "control_before_edit": control3, "record_edit": edit3, "status_after_edit": after3,
            "never_governed_after_edit": after3["status"] != "governed", "cites": [cites["tick_and_boot_comparison"], cites["owner_only_state_check"], cites["single_link_check"]]}
        runner.log(run_id=ob.new_rid(), case_id="t5-start-ticks", label="task5: start ticks mismatch, PID-reuse stand-in (controlled)", group="t5", start=t0, end=ob.now(),
                   exit=0, real_claude=False, depth=None, result="controlled", extra={"statuses": [control3["status"], after3["status"]]})

        # Case 3: recorded boot identity differs from the host boot identity.
        t0 = ob.now()
        s4 = str(uuid.uuid4())
        jobs["j4"] = start_job(g, s4, "boot-identity")
        control4 = identify(g, jobs["j4"]["child_pid"])
        edit4 = edit_record(jobs["j4"], "boot", str(uuid.uuid4()))
        after4 = identify(g, jobs["j4"]["child_pid"])
        out["boot_identity_mismatch"] = {
            "label": "controlled", "reason": "the recorded boot identity of a live registered job was edited to a different value, as after a reboot",
            "control_before_edit": control4, "record_edit": edit4, "status_after_edit": after4,
            "never_governed_after_edit": after4["status"] != "governed", "cites": [cites["tick_and_boot_comparison"], cites["owner_only_state_check"], cites["single_link_check"]]}
        runner.log(run_id=ob.new_rid(), case_id="t5-boot-identity", label="task5: boot identity mismatch (controlled)", group="t5", start=t0, end=ob.now(),
                   exit=0, real_claude=False, depth=None, result="controlled", extra={"statuses": [control4["status"], after4["status"]]})
        # The unedited second release session is a standing control: its record was never edited and it is still governed.
        out["standing_control_unedited_record"] = {"session_id": s2, "status_at_end": identify(g, jobs["j2"]["child_pid"])}
    finally:
        for j in jobs.values():
            ob.cleanup_log("group=t5 case=task5 job=%s supervisor=%d child=%d (stopped by the group teardown sweep below)" % (j["name"], j["supervisor_pid"], j["child_pid"]))
        out["teardown"] = g.teardown("task5")
        (ob.GROUPS / "t5.json").unlink()
    (ART / "selector-invariants.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"release_only_released_changed": out["release"]["only_the_released_sessions_child_changed"],
                      "start_ticks_after_edit": out["start_tick_mismatch"]["status_after_edit"]["status"],
                      "boot_after_edit": out["boot_identity_mismatch"]["status_after_edit"]["status"], "teardown": out["teardown"]}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
