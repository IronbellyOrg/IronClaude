"""Task 2: a governed and an ordinary session in one worktree, a nested subagent and Monitor.

Run: uv run --no-project python -I artifacts/observe/task2.py
At most four real Claude runs. If the first (governed) run fails before any tool ran, the
remaining cases are recorded unavailable with the observed failure category and no further
run is spent.
"""

import sys

sys.dont_write_bytecode = True

import json  # noqa: E402
import shlex  # noqa: E402
import uuid  # noqa: E402
from pathlib import Path  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import observe as ob  # noqa: E402
from real_case import public, real_case  # noqa: E402

ART = ob.ART


def summarize(case):
    sel = case["selector_captured_by_runner"]
    first = sel[0] if sel else None
    out = public(case)
    out["selector_status"] = first["status"] if first else "no selector line captured"
    out["selector_session_id"] = first.get("session_id") if first else None
    return out


def unavailable(why, detail):
    return {"result": "unavailable", "missing_interface": why, "detail": detail}


def subagent_prompt(script):
    return ("Use the Task tool exactly once to start a subagent. Tell the subagent to use Bash exactly once to execute this literal command and report only its output: /bin/bash "
            + shlex.quote(str(script)))


def monitor_prompt(script):
    return ("Use the Monitor tool exactly once with command: /bin/bash " + shlex.quote(str(script))
            + " , description: identity check, timeout_ms: 20000, persistent: false. Then report only what the monitor emitted.")


def main():
    runner = ob.Runner()
    g = ob.Group.create("t2")
    cases = {}
    stopped = None
    try:
        sid_g = str(uuid.uuid4())
        g.make_governed(sid_g)
        cases["governed"] = real_case(runner, g, "t2-governed", "governed", sid_g, "task2: governed print session, one Bash identify", timeout=120)
        gov = cases["governed"]
        if gov["ledger_exit"] != 0 and not gov["ran_a_tool"]:
            stopped = {"reason": "the first governed run failed before any tool ran", "ledger_exit": gov["ledger_exit"],
                       "result": gov["result"], "failure": gov["failure"],
                       "preflight_result": json.loads(ob.PREFLIGHT.read_text()).get("preflight_result")}
        if not stopped:
            sid_o = str(uuid.uuid4())
            cases["ordinary"] = real_case(runner, g, "t2-ordinary", "ordinary", sid_o, "task2: ordinary print session, no record, same worktree",
                                          timeout=120, record_sid=sid_g)
            sid_s = str(uuid.uuid4())
            g.make_governed(sid_s)
            cases["subagent"] = real_case(runner, g, "t2-subagent", "governed", sid_s, "task2: governed session, nested subagent runs the Bash command",
                                          tools=("Bash", "Task"), timeout=180, prompt=subagent_prompt)
            sid_m = str(uuid.uuid4())
            g.make_governed(sid_m)
            cases["monitor"] = real_case(runner, g, "t2-monitor", "governed", sid_m, "task2: governed session tries the Monitor tool",
                                         tools=("Bash", "Monitor"), timeout=120, prompt=monitor_prompt)
    finally:
        td = g.teardown("task2")
        (ob.GROUPS / "t2.json").unlink()

    if stopped:
        why = "a real Claude run could not complete in this environment; failure category recorded, no further run spent"
        same = {"task": 2, "result": "unavailable", "missing_interface": why, "stopped_after": stopped,
                "governed": summarize(cases["governed"]),
                "ordinary": unavailable(why, "not run: no run spent after the first governed run failed"),
                "ordinary_produced_while_governed_record_existed": "unavailable"}
        sub = {"task": 2,
               "subagent": unavailable(why, "not run: no run spent after the first governed run failed"),
               "monitor": unavailable(why, "not run: no run spent after the first governed run failed")}
    else:
        o = cases["ordinary"]
        same = {"task": 2, "result": "observed" if cases["governed"]["result"] == "observed" and o["result"] == "observed" else "blocked",
                "fixture_shared": True,
                "governed": summarize(cases["governed"]), "ordinary": summarize(o),
                "ordinary_produced_while_governed_record_existed": bool((o["store_check"] or {}).get("governed_record_exists"))}
        sub = {"task": 2, "subagent": summarize(cases["subagent"]), "monitor": summarize(cases["monitor"])}
    (ART / "same-worktree.json").write_text(json.dumps(same, indent=2, sort_keys=True) + "\n")
    (ART / "subagent-and-monitor.json").write_text(json.dumps(sub, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"stopped": bool(stopped), "teardown": td,
                      "cases": {k: {"exit": v["ledger_exit"], "result": v["result"], "selector": v["selector_captured_by_runner"], "failure": v["failure"]} for k, v in cases.items()}},
                     indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
