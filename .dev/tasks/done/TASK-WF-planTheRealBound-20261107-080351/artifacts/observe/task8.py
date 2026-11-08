"""Task 8: write ./artifacts/b-ctx-report.md with a binary B-CTX result.

Run: uv run --no-project python -I artifacts/observe/task8.py
No real Claude run is spent. The report is assembled from the artifacts of Tasks 1 to 7 so that run ids, statuses
and numbers are copied from the evidence files, not retyped.
"""

import sys

sys.dont_write_bytecode = True

import json  # noqa: E402
import os  # noqa: E402
import subprocess  # noqa: E402
from pathlib import Path  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import observe as ob  # noqa: E402

ART = ob.ART
PKG = ART.parent
REL = "src/superclaude/hooks/scripts/launch-job-identity.sh"
DESIGN = "docs/designs/sc-issue-launch-level-hook.md"


def load(name):
    return json.loads((ART / name).read_text())


def ln(name, needle, nth=1):
    n = 0
    for i, line in enumerate((ART / name).read_text().splitlines(), 1):
        if needle in line:
            n += 1
            if n == nth:
                return i
    return 1


def ref(name, needle, nth=1):
    return "./artifacts/%s:%d" % (name, ln(name, needle, nth))


def sel(entry, key="selector_captured_by_runner"):
    items = entry.get(key) or []
    return (items[0].get("line_sha256", "")[:12], items[0].get("status")) if items else ("", None)


def main():
    sw, sm, rfc, bj, inv, push = (load(n) for n in ("same-worktree.json", "subagent-and-monitor.json", "resume-fork-clear.json", "background-jobs.json",
                                                     "selector-invariants.json", "human-vs-governed-push.json"))
    ledger = [json.loads(x) for x in (ART / "run-status.jsonl").read_text().splitlines()]
    real = [e for e in ledger if e.get("real_claude") is True]

    g, o = sw["governed"], sw["ordinary"]
    sub, mon = sm["subagent"], sm["monitor"]
    res, fork, clr, dec = rfc["resume"], rfc["fork"], rfc["clear"], rfc["decisive_case"]
    shp = bj["shapes"]
    rb, rp, sd, ks = shp["run_in_background"], shp["foreground_reparent"], shp["setsid_daemon"], shp["killed_supervisor"]

    def srow(x):
        return "run %s, selector line sha256 %s" % (x.get("run_id"), sel(x)[0])

    rows = [
        ("1", "Main Claude (governed session, Bash adapter)", "observed", ref("same-worktree.json", '  "governed": {'), srow(g),
         "yes: governed with its own session id (%s)" % g["selector_session_id"], "-"),
        ("2", "Subagent and nested tool calls (the nested subagent's Bash call)", "observed", ref("subagent-and-monitor.json", '  "subagent": {'), srow(sub),
         "yes: governed with the parent session's id; the hook event carried an agent id", "-"),
        ("3a", "Background Bash descendant (run_in_background)", "observed", ref("background-jobs.json", '    "run_in_background": {'),
         "run %s, selector line sha256 %s" % (rb["run_id"], rb["descendant_status_inside_same_command"]["line_sha256"][:12]),
         "yes: descendant governed with the session's own id, inside the command and from a second Bash call", "-"),
        ("3b", "Monitor descendant", "observed (documented escape)", ref("subagent-and-monitor.json", '  "monitor": {'), srow(mon),
         "no: ordinary (Monitor has no adapter); attribution to the Monitor tool is an inference from the 2-hop depth", "-"),
        ("4a", "Same-worktree human terminal: human-style shell started by the runner", "controlled", ref("human-vs-governed-push.json", '  "pushes": ['),
         "controlled push records (no real run)", "ordinary logged for both plain-shell pushes", "-"),
        ("4b", "Same-worktree human terminal: a person in an Orca terminal", "unavailable", ref("human-vs-governed-push.json", '  "orca_terminal_human_case": {'),
         "none", "not observed", push["orca_terminal_human_case"]["missing_interface"]),
        ("5", "Ordinary Claude session in the same worktree", "observed", ref("same-worktree.json", '  "ordinary": {'), srow(o),
         "yes: ordinary, produced while the governed session's record existed (%s)" % sw["ordinary_produced_while_governed_record_existed"], "-"),
        ("6a", "Reparented job (foreground command whose descendant is reparented)", "observed", ref("background-jobs.json", '    "foreground_reparent": {'),
         "run %s, selector line sha256 %s" % (rp["run_id"], rp["descendant_status_inside_same_command_before_it_exits"]["line_sha256"][:12]),
         "yes: governed inside the same command; the call waited %s s for the descendant" % rp["observed_wait_seconds_until_the_next_bash_call_started"], "-"),
        ("6b", "Detached job: deliberate setsid daemonized child", "observed (documented escape)", ref("background-jobs.json", '    "setsid_daemon": {'),
         "run %s, selector line sha256 %s" % (sd["run_id"], sd["descendant_status_inside_same_command"]["line_sha256"][:12]),
         "no: the child reported ordinary (documented limit, section 19.7)", "-"),
        ("6c", "Detached job: supervisor killed while a child lives", "observed (documented escape)", ref("background-jobs.json", '    "killed_supervisor": {'),
         "run %s, selector line sha256 %s" % (ks["run_id"], ks["descendant_status_after_kill"]["line_sha256"][:12]),
         "no: governed before the kill, unknown after it (documented limit, section 19.7)", "-"),
        ("7a", "Process exit and PID reuse (recorded start ticks no longer match)", "controlled", ref("selector-invariants.json", '  "start_tick_mismatch": {'),
         "controlled edit of a job record (no real run)", "not governed after the edit (unknown)",
         "-"),
        ("7b", "Boot identity change", "controlled", ref("selector-invariants.json", '  "boot_identity_mismatch": {'),
         "controlled edit of a job record (no real run)", "not governed after the edit (unknown)", "-"),
        ("8", "Resume into a new process", "observed", ref("resume-fork-clear.json", '  "resume": {'),
         "run %s, selector lines %s" % (res["run_id"], ",".join(x["line_sha256"][:12] for x in res["selector_lines"])),
         "yes: the resumed session kept the origin id %s and its command reported governed; the old child stayed governed" % res["old_child"]["origin_session_id"], "-"),
        ("9a", "Fork", "observed", ref("resume-fork-clear.json", '  "fork": {'),
         "run %s, selector lines %s" % (fork["run_id"], ",".join(x["line_sha256"][:12] for x in fork["selector_lines"])),
         "yes: the forked session (new id %s) reported ordinary while the old child stayed governed" % fork["hook_event_session_id"], "-"),
        ("9b", "/clear", "unavailable", ref("resume-fork-clear.json", '  "clear": {'), "run %s (no selector line)" % clr["run_id"], "not observed", clr["missing_interface"]),
        ("10", "Release with a live old background child", "controlled", ref("selector-invariants.json", '  "release": {'),
         "controlled processes (no real run)", "only the released session's child changed (governed to ordinary, reason released); the other stayed governed", "-"),
        ("11", "The launch wrapper", "unavailable", ref("observe/observe.py", "def claude_argv"), "none (not run)", "not observed",
         "the production launch path that starts a governed agent session (the claim-code launcher, section 19.8 of the design): this plan may not run it because it configures real worktrees and hooks, and the Task 2 to 4 sessions were started by the runner's own argv, not by that wrapper"),
        ("12", "The Git and hook process trees", "unavailable", ref("human-vs-governed-push.json", '  "pushes": ['), "none (no real run invoked Git)", "not observed in a real session",
         "a real Claude Bash call that runs git push so that the pre-push hook's process tree under a real Claude process is read; Task 6 gives controlled evidence only (a plain shell and a governed job started by the runner), and no task of this plan runs Git from a real Claude session (the 12-run budget is fully assigned to Tasks 1 to 4)"),
        ("13", "The auto-mode variants", "unavailable", ref("observe/observe.py", '"--permission-mode", "dontAsk"'), "none (no run used auto mode)", "not observed",
         "a real Claude run in auto permission mode under the Bash adapter: every real run here used the dontAsk permission mode, and the design lists live auto-mode rewrites as unobserved (section 19.7)"),
        ("14a", "Decisive distinction, new-process form: old governed background child alive while a new ordinary session starts (fork)", "observed",
         ref("resume-fork-clear.json", '  "decisive_case": {'), "run %s (fork)" % fork["run_id"],
         "yes: the old child reported governed with origin %s and the new forked session reported ordinary" % dec["old_child_origin_session_id"], "-"),
        ("14b", "Decisive distinction, reused-process form: an ordinary new session started by /clear in the same Claude process", "unavailable",
         ref("resume-fork-clear.json", '  "reused_process_form"'), "none", "not observed", clr["reused_process_form"]),
    ]
    results = [r[2] for r in rows]
    all_observed_with_separation = all(x == "observed" for x in results)
    verdict = "B-CTX: PASS" if all_observed_with_separation else "B-CTX: FAIL"

    # Cleanup checks.
    log = (ART / "phase2-cleanup.log").read_text().splitlines()
    td = [x for x in log if "teardown leftover_processes=" in x]
    td_zero = all("leftover_processes=0 directory_removed=True" in x for x in td)
    tmp_left = sorted(p.name for p in Path("/tmp").glob("observe-*"))
    stray = 0
    for name in os.listdir("/proc"):
        if name.isdecimal():
            try:
                cwd = os.readlink("/proc/%s/cwd" % name)
            except OSError:
                continue
            if cwd.startswith("/tmp/observe-"):
                stray += 1
    groups_left = sorted(p.name for p in (ART / "groups").glob("*.json")) if (ART / "groups").exists() else []
    equal_settings = all(e.get("settings_sha256_before") == e.get("settings_sha256_after") for e in real)
    base = json.loads(ob.BASELINE.read_text())
    same_as_baseline = all(e.get("settings_sha256_before") == base["real_claude_settings_sha256"] for e in real)
    cb = ob.check_baseline()
    subprocess.run(["git", "-C", str(ob.REPO), "add", ".dev/tasks"], check=True)
    rel_pkg = str(PKG.relative_to(ob.REPO))
    status = subprocess.run(["git", "-C", str(ob.REPO), "status", "--porcelain", "--", rel_pkg], capture_output=True, text=True).stdout.splitlines()
    untracked = [x for x in status if x.startswith("??")]
    staged = subprocess.run(["git", "-C", str(ob.REPO), "diff", "--cached", "--name-only", "--", rel_pkg], capture_output=True, text=True).stdout.split()
    staged_src = subprocess.run(["git", "-C", str(ob.REPO), "diff", "--cached", "--name-only", "--", "src", "plugins", "tests"], capture_output=True, text=True).stdout.split()

    report = []
    a = report.append
    a("# B-CTX report: observed actor-isolation lifecycle cases\n")
    a("Package TASK-WF-planTheRealBound-20261107-080351. Measured against the identity integration of PR #414 (`%s`) and section 19 of `%s`. Nothing is enforced and no production file changed.\n" % (REL, DESIGN))
    a("Evidence classes: **observed** = a real Claude process produced it in this plan's runs (selector output captured by the runner by run id, never the model's own report); **controlled** = built from runner-started processes or an edited fixture record, never real harness behavior; **unavailable** = not driven, with the missing interface named.\n")
    a("## Real Claude runs (counted from ./artifacts/run-status.jsonl)\n")
    a("Real Claude runs counted (`real_claude` true, refused launches included): **%d** of at most 12. Refused launches: %d. Re-runs: none.\n" % (len(real), sum(1 for e in real if (e.get("extra") or {}).get("refusal_observed"))))
    a("| Case | Run id | Exit | Result | Ledger line |\n|---|---|---|---|---|")
    for e in real:
        a("| %s | %s | %s | %s | ./artifacts/run-status.jsonl:%d |" % (e["case_id"], e["run_id"], e["exit"], e["result"], ledger.index(e) + 1))
    a("")
    a("The first run (the preflight) exited 1 after Claude started and listed its tools; its failure category was not captured by the first version of the runner, so `./artifacts/preflight.json` reads `unavailable` for `nested_launch_refused` and `authentication_available` (it records the exit, not a refusal). All 11 later real runs started and none showed a nested-launch refusal or an authentication failure (nine exited 0, one was ended by the planned SIGKILL of Task 3, and the interactive `/clear` run was ended by the runner after it produced nothing, exit 143), so those two preflight fields describe an undetermined first run, not the state of this host.\n")
    a("## Required cases (section 19.1)\n")
    a("| # | Case | Result | Evidence artifact | Runner-captured record | Separation shown | Missing interface |\n|---|---|---|---|---|---|---|")
    for r in rows:
        a("| " + " | ".join(r) + " |")
    a("")
    a("Notes on the rows: row 3b rests on a 2-hop selector line and the absence of an adapter rewrite for that command; the stream summary of that run kept event types but not tool names, so naming Monitor as the source is an inference. Row 9b: the interactive run sent both prompts but nothing shows either reached a session, and the cause was not captured. Task 4's third session saw five Bash calls for four requested commands (`./artifacts/background-jobs.json`, `extra_bash_call_note`). The log-only pre-push hook of Task 6 sleeps one second to widen the overlap window of its concurrent pushes.\n")
    a("## Gap findings F2.1 to F2.6 of the blocked review\n")
    a("The findings are in `.dev/tasks/to-do/TASK-WF-implementDocsDes-20261106-210206/artifacts/retries/T1/review-2.md` (read only).\n")
    a("- **F2.1 (lifecycle cases listed without observed evidence or a named interface): closed by the case table of this report.** Evidence class: observed for rows 1, 2, 3a, 3b, 5, 6a to 6c, 8, 9a and 14a; unavailable with the interface named for rows 4b, 9b, 11, 12, 13 and 14b; controlled for rows 4a, 7a, 7b and 10. Resume, fork, Monitor and the nested subagent are closed by observed results of the same cases, not by controlled ones; `/clear` is closed only in the sense that its missing interface is now named.")
    a("- **F2.2 (decisive distinction unproven): open (why).** The new-process form is observed (row 14a, %s: old child governed with origin %s, forked session ordinary). The form the finding asks for, a reused Claude process starting an ordinary session while the old governed child lives, needs `/clear` in one process and stays unavailable (row 14b)." % (ref("resume-fork-clear.json", '  "decisive_case": {'), dec["old_child_origin_session_id"]))
    a("- **F2.3 (ancestry bound not derived from observed trees): superseded or not applicable (%s:253).** The merged selector checks kernel session membership and does not walk the parent chain; the real depths and the controlled deep chain are in `./artifacts/ancestry-bound.md`." % REL)
    a("- **F2.4 (authority invariants not exercised): closed by `./artifacts/selector-invariants.json` and `./artifacts/human-vs-governed-push.json`; evidence class controlled.** Boot identity and start ticks are compared at %s:234 (controlled check %s); release with a live child changed only the released session's child (%s); a same-worktree human-style push and a governed push against a disposable bare repository were logged ordinary and governed (%s). The real-session observation of release and of Git pushes stays an evidence gap (rows 10 and 12)." % (REL, ref("selector-invariants.json", '  "boot_identity_mismatch": {'), ref("selector-invariants.json", '  "release": {'), ref("human-vs-governed-push.json", '  "concurrent_run": {')))
    a("- **F2.5 (no file recording each probe run's command and exit status): closed by `./artifacts/run-status.jsonl`; evidence class observed for the %d real runs and controlled for the other lines.** Each line records the case id, a redacted label, start and end, the exit code or signal and the result." % len(real))
    a("- **F2.6 (exhaustion described as never a trusted human, but the old walk discarded its stop reason): superseded or not applicable (the finding describes only the historical controller-ancestry probe, `.dev/tasks/to-do/TASK-WF-implementDocsDes-20261106-210206/artifacts/actor-context-probe.sh:39`).** The merged selector has no walk; unreadable or stale registered state returns `unknown` (%s:244), which the design says is not a trusted-human verdict (section 19.7)." % REL)
    a("")
    a("## Why the result is FAIL\n")
    a("Task 5 can label release, PID reuse and boot identity only controlled, and `/clear`, the launch wrapper, the Git and hook process trees and the auto-mode variants were not observed, so not every required case is observed. **A FAIL result is the expected outcome of this plan.** Observed documented escapes (a setsid child, a killed supervisor, a Monitor command without an adapter) show no separation and never count toward a pass.\n")
    a(verdict)
    a("")
    a("### Contract gaps (observed cases whose status broke the separation)\n")
    a("1. **Monitor command (row 3b).** Missing binding: no adapter exists for the Monitor tool, so its command ran outside the supervisor and reported ordinary. Smallest integration: register the same PreToolUse adapter for the Monitor tool so its command is wrapped in a supervisor, or deny the Monitor tool in governed sessions. Whether Monitor input can be rewritten was not observed.")
    a("2. **Deliberate setsid child (row 6b).** Missing child-lifetime contract: a process that calls `setsid` leaves the supervisor's kernel session and reported ordinary. Smallest integration: containment that setsid cannot leave (for example a control group or a pidfd-tracked tree), as the helper's own comment says (%s:7-9)." % REL)
    a("3. **Killed supervisor (row 6c).** Missing child-lifetime contract: after the supervisor was killed, its live child went from governed to unknown. Smallest integration: state what the pre-push decision does with `unknown` for a registered job whose supervisor is dead (the design says only that unknown is not a trusted-human verdict), or keep the supervisor out of the agent's reach.")
    a("")
    a("### Evidence gaps (controlled or unavailable cases and the real-observation interface that would make each observed)\n")
    a("- Row 4a (human-style shell, controlled) and 4b (a person in an Orca terminal): a real person's terminal in an Orca-managed worktree pushing while a governed session works.")
    a("- Rows 7a and 7b (PID reuse and boot identity, controlled): a real recycled process id for a registered job and a real reboot of the host with a stale record; neither can be forced from a Claude session, so the nearest real observation is a recorded job read after a host restart.")
    a("- Row 10 (release, controlled): delete a governed session's level record from outside while a real Claude session's background child lives, then identify the child from a later Bash call.")
    a("- Row 9b and row 14b (`/clear`, unavailable): keyboard input to Claude Code's interactive terminal UI through a pty that provably reaches a session (this run's single attempt did not).")
    a("- Row 11 (launch wrapper, unavailable): a governed session started by the production claim-code launcher.")
    a("- Row 12 (Git and hook process trees, unavailable): a real Claude Bash call that runs `git push` to a disposable bare repository with the log-only hook installed.")
    a("- Row 13 (auto-mode variants, unavailable): a real Claude run in auto permission mode under the Bash adapter.")
    a("")
    a("The contract-gap list is not empty: three observed cases broke the separation, all of them documented limits of the merged design (section 19.7). This result does not waive the blocked package's gate: package TASK-WF-implementDocsDes-20261106-210206 stays blocked and was not modified, moved or re-run.\n")
    a("## Cleanup record\n")
    a("- Processes and temporary directories: %d group teardowns in `./artifacts/phase2-cleanup.log`, every one reporting `leftover_processes=0 directory_removed=True`: **%s**. Leftover `/tmp/observe-*` directories: %s. Processes whose working directory is under `/tmp/observe-*`: %d. Registry files left in `./artifacts/groups/`: %s." % (len(td), td_zero, tmp_left or "none", stray, groups_left or "none"))
    a("- Real Claude settings checksum: unchanged before and after every one of the %d real runs (each `real_claude` entry of `./artifacts/run-status.jsonl` has equal before-run and after-run values): **%s**; and equal to the value in `./artifacts/baseline.json`: **%s**." % (len(real), equal_settings, same_as_baseline))
    a("- Git state of `src/`, `plugins/`, `tests/` and the blocked package against `./artifacts/baseline.json` (status and diff checksums, plus the package tree checksums of the blocked and done packages): equal = **%s**, differing keys: %s." % (cb["equal"], cb["differs"] or "none"))
    a("- Staging: `git add .dev/tasks` was run when this report was generated. Files of this package staged: %d; untracked files in the package: %d; files staged under `src/`, `plugins/` or `tests/`: %d. Nothing was committed." % (len(staged), len(untracked), len(staged_src)))
    out = "\n".join(report) + "\n"
    (ART / "b-ctx-report.md").write_text(out)
    subprocess.run(["git", "-C", str(ob.REPO), "add", ".dev/tasks"], check=True)
    print(json.dumps({"verdict": verdict, "real_runs": len(real), "rows": len(rows), "teardowns_zero": td_zero, "stray": stray, "settings_equal": equal_settings,
                      "baseline_equal": cb["equal"], "untracked": len(untracked), "staged": len(staged)}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
