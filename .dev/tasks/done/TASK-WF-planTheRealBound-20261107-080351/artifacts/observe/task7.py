"""Task 7: process-tree depth and the exhaustion behavior of the actor selector.

Run: uv run --no-project python -I artifacts/observe/task7.py
No real Claude run is spent. The measured depths are read from the ledger (run-status.jsonl) and from the
Task 4 artifact; one controlled case runs a very deep nested shell chain under a governed job and compares the
selector status with a shallow chain. Writes ./artifacts/ancestry-bound.md.
"""

import sys

sys.dont_write_bytecode = True

import json  # noqa: E402
import shlex  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402
import uuid  # noqa: E402
from pathlib import Path  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import observe as ob  # noqa: E402

ART = ob.ART
DEEP = 200  # more than the historical probe's 64-hop cap
HISTORICAL = ob.REPO / ".dev/tasks/to-do/TASK-WF-implementDocsDes-20261106-210206/artifacts/actor-context-probe.sh"
DESIGN = "docs/designs/sc-issue-launch-level-hook.md"
SCRIPT = """#!/bin/bash
n=$1; out=$2; helper=$3
if [ "$n" -gt 0 ]; then /bin/bash "$0" $((n-1)) "$out" "$helper"; exit $?; fi
sup=$(sed -E 's/^.*\\) //' /proc/$$/stat | awk '{print $4}')
p=$$; hops=0
while [ "$p" != "$sup" ] && [ "${p:-0}" -gt 1 ]; do
  p=$(sed -E 's/^[0-9]+ \\(.*\\) [A-Za-z] ([0-9]+) .*/\\1/' /proc/$p/stat); hops=$((hops+1))
done
res=$(/bin/bash "$helper" identify)
printf '%s %s\\n' "$hops" "$res" > "$out"
"""


def line_of(path, needle):
    for n, line in enumerate(Path(path).read_text().splitlines(), 1):
        if needle in line:
            return n
    return None


def chain(g, sid, depth):
    """Run a nested shell chain of the given depth under a governed job; return hops to the supervisor and the selector result."""
    script = g.tmp / "deep.sh"
    script.write_text(SCRIPT)
    out = g.tmp / ("deep-%d.out" % depth)
    cmd = "/bin/bash %s %d %s %s" % (shlex.quote(str(script)), depth, shlex.quote(str(out)), shlex.quote(str(ob.HELPER)))
    env = g.git_env()
    token = subprocess.run(["/bin/bash", str(ob.HELPER), "prepare", sid, cmd], env=env, capture_output=True, text=True, timeout=30).stdout.strip()
    mp = g.spawn(["/bin/bash", str(ob.HELPER), "run", token], "deep-%d" % depth, env=env)
    end = time.time() + 120
    while mp.p.poll() is None and time.time() < end:
        time.sleep(0.1)
    hops, _, raw = out.read_text().partition(" ") if out.exists() else ("", "", "")
    found = ob.identities(raw.strip())
    item = dict(found[0]) if found else {"status": "no selector line"}
    return {"requested_nesting": depth, "measured_hops_to_supervisor": int(hops) if hops.isdigit() else None, "selector": item, "run_exit": mp.p.returncode}


def main():
    ledger = [json.loads(x) for x in (ART / "run-status.jsonl").read_text().splitlines()]
    depths = []
    for e in ledger:
        d = e.get("depth")
        if e.get("real_claude") and isinstance(d, dict) and d.get("measured"):
            depths.append({"case": e["case_id"], "hops": d["hops"], "claude_reached": d["claude_process_reached"], "run_id": e["run_id"]})
    t4 = json.loads((ART / "background-jobs.json").read_text())
    t4_depths = []
    for name, shape in t4["shapes"].items():
        if shape.get("depth"):
            t4_depths.append({"case": "t4 %s (first call)" % name, "hops": shape["depth"]["hops"], "claude_reached": shape["depth"]["claude_process_reached"], "run_id": shape["run_id"]})
        sc = shape.get("second_bash_tool_call")
        if sc and sc.get("depth"):
            t4_depths.append({"case": "t4 %s (second Bash call)" % name, "hops": sc["depth"]["hops"], "claude_reached": sc["depth"]["claude_process_reached"], "run_id": shape["run_id"]})
    all_depths = depths + t4_depths
    rewritten = [d for d in all_depths if d["hops"] >= 3]
    plain = [d for d in all_depths if d["hops"] < 3]
    rw_hops, plain_hops = sorted({d["hops"] for d in rewritten}), sorted({d["hops"] for d in plain})
    max_hops = max(d["hops"] for d in all_depths)

    runner = ob.Runner()
    g = ob.Group.create("t7")
    try:
        t0 = ob.now()
        sid = str(uuid.uuid4())
        g.make_governed(sid)
        shallow, deep = chain(g, sid, 0), chain(g, sid, DEEP)
        unchanged = shallow["selector"] == deep["selector"] and deep["selector"].get("status") == "governed"
        runner.log(run_id=ob.new_rid(), case_id="t7-deep-chain", label="task7: very deep nested shell chain under a governed job, selector status vs a shallow chain (controlled)", group="t7",
                   start=t0, end=ob.now(), exit=0, real_claude=False, depth=None, result="controlled",
                   extra={"shallow_status": shallow["selector"].get("status"), "deep_status": deep["selector"].get("status"), "deep_hops": deep["measured_hops_to_supervisor"]})
    finally:
        td = g.teardown("task7")
        (ob.GROUPS / "t7.json").unlink()

    h = ob.HELPER
    rel = "src/superclaude/hooks/scripts/launch-job-identity.sh"
    L = {k: line_of(h, v) for k, v in {  # noqa: N806
        "sid": "_, sid, _ = proc(pid)", "jobs": "raw = read_file(jobs, str(sid) + '.json')", "stale": "start != value['start'] or boot() != value['boot']",
        "released": "'reason': 'released'", "unknown": "return {'status': 'unknown'}", "walk": "No bounded ancestry walk", "members": "def members(sid)",
        "ident": "def identify(pid)", "setsid": "os.setsid()"}.items()}
    hist = line_of(HISTORICAL, "LIMIT = 64")
    hist_rel = str(HISTORICAL.relative_to(ob.REPO))
    rows = "\n".join("| %s | %d | %s | %s |" % (d["case"], d["hops"], "yes" if d["claude_reached"] else "no", d["run_id"]) for d in all_depths)
    md = f"""# Actor-selector process-tree depth and exhaustion behavior (Task 7)

Evidence label: the depths are from real Claude runs (Tasks 2, 3 and 4); the deep-chain case is controlled (processes started by the runner under a governed job through the helper's own prepare and run actions). No real run was spent on this task.

## How the selector decides (helper lines, read now)

- `identify` starts at `{rel}:{L['ident']}`. It reads the target process's kernel session id (`{rel}:{L['sid']}`) and then the job record named after that session (`{rel}:{L['jobs']}`).
- The file itself states the method: `{rel}:{L['walk']}` reads "No bounded ancestry walk or truncated scan is interpreted as ordinary". The only scan is `members` (`{rel}:{L['members']}`), which lists processes whose kernel session equals the supervisor's session; it is used by the supervisor to wait for its own descendants, not by `identify` to climb parents.
- The supervisor makes its own session with `os.setsid()` (`{rel}:{L['setsid']}`), so membership, not parent distance, is what binds a process to a job.
- The record is accepted only while the supervisor's pid, start ticks and boot identity still match (`{rel}:{L['stale']}`); stale or unreadable state returns `unknown` (`{rel}:{L['unknown']}`); a deleted level record returns `ordinary` with reason `released` (`{rel}:{L['released']}`).

## Measured real process-tree depth (from run-status.jsonl and the Task 4 artifact)

Hops are parent links from the command's shell up to the Claude process, measured by the command itself. Ledger lines are in ./artifacts/run-status.jsonl (the run id column); the Task 4 numbers are in ./artifacts/background-jobs.json (their run ids are in the same ledger).

| Case | Hops to the Claude process | Claude process reached | Run id |
|---|---|---|---|
{rows}

Summary: Bash calls rewritten by the adapter (governed sessions) measured {rw_hops} hops; commands not wrapped by the adapter (the ordinary session and the Monitor command) measured {plain_hops} hops. The largest real depth observed in this plan is {max_hops} hops.

## Historical controller-ancestry probe

The historical probe in the blocked package walked parent links with a traversal cap of 64 hops (`{hist_rel}:{hist}`, "Diagnostic bound only; not a proven production ancestry limit"). The merged selector does not use that probe.

## Exhaustion behavior: not applicable

The bound question is recorded as **not applicable**. The selector checks kernel session membership and does not walk the parent chain (`{rel}:{L['walk']}`), so there is no walk to exhaust and no hop bound to choose. Unreadable or stale registered state selects `unknown` (`{rel}:{L['unknown']}`), and the design states that `unknown` is not a trusted-human verdict ({DESIGN} section 19.7); this artifact does not describe an exhausted or unreadable walk as a trusted human.

Controlled deep-chain case (label: controlled): a governed job ran a nested shell chain and called `identify` at the bottom.

| Chain | Nesting requested | Hops from the bottom shell to the supervisor | Selector status | Session id |
|---|---|---|---|---|
| shallow control | {shallow['requested_nesting']} | {shallow['measured_hops_to_supervisor']} | {shallow['selector'].get('status')} | {shallow['selector'].get('session_id')} |
| very deep | {deep['requested_nesting']} | {deep['measured_hops_to_supervisor']} | {deep['selector'].get('status')} | {deep['selector'].get('session_id')} |

Result: the selector status of the very deep chain is {'unchanged from' if unchanged else 'NOT the same as'} the shallow chain (same status and session id), at a depth well beyond the historical 64-hop cap.

## Statement on the historical cap

The historical 64-hop cap is **not adopted** as a production bound. It is not measured here as a requirement: the selector has no ancestry bound, and the largest real depth measured in this plan is {max_hops} hops. If a future design reintroduces a parent walk, that bound would need its own measurement and an explicit exhaustion rule.

Cleanup: the controlled chain's group teardown left {td['leftover_processes']} processes and removed its directories (./artifacts/phase2-cleanup.log).
"""
    (ART / "ancestry-bound.md").write_text(md)
    print(json.dumps({"unchanged": unchanged, "shallow": shallow, "deep": deep, "teardown": td, "max_real_hops": max_hops}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
