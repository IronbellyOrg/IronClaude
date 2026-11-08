33f50bf4faac4080ddef3a0abe35d95ae83934e3
Review one task for spec compliance.

Task brief: ## Task 3: Observe resume, fork and clear against an old live governed child

Depends on: Task 2

Using the runner of Task 1, observe the three lifecycle events that the blocked gate called unproven. All runs of this task share one run group of Task 1, so the throwaway HOME and its launch-level store persist from the initial run through resume, fork and /clear; the group is torn down only after the last of them. First start a governed real Claude session whose Bash command starts one ordinary background child (a bounded sleep with its output redirected away, not through setsid, nohup or run_in_background), runs the identify action on it, and writes the selector line, the child's process id, start ticks and boot identity to a ready file in the run group's temporary directory. The adapter's supervisor waits for ordinary background descendants, so this governed call is not expected to return while the child lives and the first Claude process is not expected to exit by itself; record whether the call returned and for how many seconds it was held, and record a return while the child lived as an observed contradiction. Mark the job as surviving (no runner cleanup). When the ready file appears, the runner sends SIGKILL to the first Claude process's own process id only, never a process group, the supervisor or the child, and records the signal, the target and the time. If the first Claude process ends any other way before the ready file appears (the Bash tool's own timeout, the case timeout, or a returned call), record that end and the child's state as observed and do not treat it as the planned kill. After the kill and before any resume, read the child's process id, start ticks and boot identity from /proc and compare them with the ready file (a mismatch is recorded as unobserved with the reason "child identity changed" and never as a selector status), read the supervisor's process id and start ticks, and record whether each is alive; survival of the kill is not assumed. If the child or supervisor is gone, record resume, fork and the decisive case as unavailable with the reason "job did not survive the first Claude process ending" and start no substitute child. If the killed session cannot be resumed, record resume and fork as unavailable and name the refusal. Background scheduling with run_in_background is a separate unobserved case (section 19.7 of docs/designs/sc-issue-launch-level-hook.md) and is observed in Task 4, not here. If the child is alive, resume the same session id in a new Claude process (claude --resume) and run the identify action in the resumed process, and run a fork (claude --fork-session) the same way. For /clear, run the one owner-authorized interactive Claude session (decision M2-02, 2026-11-08), the fourth real run of this task: a pty-driven interactive Claude process in the throwaway HOME with the same isolation as the other runs (disposable HOME and CLAUDE_CONFIG_DIR, explicit --settings file, --setting-sources ""), but without --print, without --max-budget-usd (the installed help restricts it to --print) and without --disable-slash-commands, which would disable /clear. This run is bounded by construction: a wall-clock timeout of 300 seconds recorded as blocked, exactly two prompts (send /clear, then one prompt that runs one governed Bash command), no retry, and the runner ends the process with the one-process signal procedure of Task 1 once the second reply is complete or the timeout expires. The CLI does not cap its cost; the run record holds the number of prompts, the elapsed seconds and any cost the session prints. If a pty-driven session cannot be driven within that bound, record /clear as unavailable and name the missing interface. In every case record the session id carried by the hook event of the resume, fork and /clear runs (the id the adapter selects on) next to the old child's origin session id. The pty /clear session is the one run that reuses a single Claude process for a new ordinary session; a resume or fork starts a new process and cannot test that form, so if the pty session cannot be driven the reused-process form is recorded unavailable with the interface named. In every case record whether the old child and the new work report the same or different session identities, and whether a new ordinary session started in a reused process is selected as ordinary. Task 3 uses at most four real Claude runs (initial, resume, fork, /clear) and no retries.

Acceptance criteria:
- ./artifacts/resume-fork-clear.json has one entry each for resume, fork and /clear. Each entry holds the old child's selector status and origin session id, the new process's selector status and session id, the old child's process id and start ticks read before and after the new process started (proving it was the same live child), a check that the launch-level store and governed session record still existed before the run, and a result of observed or unavailable; the /clear entry also records the number of prompts sent (two), the elapsed seconds, how the process was ended, and the flag names used (neither --disable-slash-commands nor --max-budget-usd appears); an unavailable entry names the missing interface. The first-call entry also holds whether the call returned and the seconds it was held, the ready-file sighting, the end action (signal name and that the target was the first Claude process only), the child's and the supervisor's process ids and start ticks before the kill and again after the kill and before the resume, and the label "job did not survive the first Claude process ending" when that applies.
- The decisive case is answered from observation or marked unavailable with its interface: an old governed background child stays alive while a new ordinary session starts, and the two report different identities (child governed with the old origin, new session ordinary), or the entry states exactly what could not be observed.
- No entry is written as observed without a selector line captured in ./artifacts/run-status.jsonl-linked output, and every started child and every surviving supervisor is accounted for as stopped in ./artifacts/phase2-cleanup.log.
Global constraints: ## Constraints

- The authoritative design is docs/designs/sc-issue-launch-level-hook.md, section 19 (19.1 for the required cases and 19.7 for the merged job-identity contract). The gap list is the six findings F2.1 to F2.6 in review-2.md of the blocked package, at artifacts/retries/T1/ inside package TASK-WF-implementDocsDes-20261106-210206 (a package in the to-do folder of .dev/tasks/). The identity helper under test is src/superclaude/hooks/scripts/launch-job-identity.sh; the earlier real-CLI observation helper is tests/hooks/fixtures/launch_level/live_probe.py. Read all of them; edit none of them.
- Do not modify, move or re-run package TASK-WF-implementDocsDes-20261106-210206, and do not modify the done package TASK-WF-authorizedNarrow-20261106-214325. Their files are read-only inputs.
- This plan observes and reports only. It adds no production hook, no registration, no installer change, no change under src/, plugins/ or tests/, and it never configures a real repository's hooks. Git experiments run only in disposable local repositories and disposable local bare repositories created under a temporary directory. No push to a real origin or any protected branch of a real remote. No interaction with the SuperClaude upstream repository.
- Real Claude runs use a throwaway HOME and CLAUDE_CONFIG_DIR, an explicit --settings file and --setting-sources "", exactly like tests/hooks/fixtures/launch_level/live_probe.py. Never edit the user's real Claude settings. Each real Claude run is capped with --max-budget-usd 0.25 and a bounded timeout, except the one interactive /clear run in Task 3, which the owner authorized on 2026-11-08 (review decision M2-02) as a separately bounded run because the installed CLI restricts --max-budget-usd to --print, and the whole plan makes at most twelve real Claude runs, counting every start of Claude including a refused launch and allowing no retries. Run budget: the preflight one, Task 2 four, Task 3 four and Task 4 three (its shapes share governed sessions as separate commands, grouped so that no shape runs after a call that stays blocked in the same session), twelve in all. Keep CLAUDECODE and existing auth variables intact: a nested-session refusal or missing authentication is recorded as unavailable and is never worked around.
- A case counts as observed only when a real Claude, Orca or Git process produced it in this plan's runs. Cases built from controlled processes or edited fixture state are labelled controlled and are never reported as real harness behavior. A case that cannot be driven is recorded as unavailable with the exact missing interface named. Never fabricate payload logs, and never write an unsupported or unobserved case as passed.
- Redact credentials, environment values, command text and process arguments from every artifact: keep identities, field names, hashes, selector results, exit codes and counts only.
- Use UV for Python (uv run --no-project python -I ...). Evidence belongs under ./artifacts/ in this package. No commit, push or issue comment is authorized. Stage .dev/tasks, including package evidence, throughout execution. Do not change this plan once implementation starts.
Start sha: 33f50bf4faac4080ddef3a0abe35d95ae83934e3
Diff against the start snapshot: Tracked files: `git diff 33f50bf4faac4080ddef3a0abe35d95ae83934e3` shows no change to any tracked source file (the ledger progress.md and earlier notes are not product). The touched files of this task are new or appended, so read each one in full from disk:
- /home/coder/workspaces/worktrees/IronClaude/finish-leftover-implement-plans/.dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/artifacts/observe/task3.py
- /home/coder/workspaces/worktrees/IronClaude/finish-leftover-implement-plans/.dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/artifacts/resume-fork-clear.json
- /home/coder/workspaces/worktrees/IronClaude/finish-leftover-implement-plans/.dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/artifacts/run-status.jsonl
- /home/coder/workspaces/worktrees/IronClaude/finish-leftover-implement-plans/.dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/artifacts/phase2-cleanup.log
run-status.jsonl and phase2-cleanup.log also hold earlier lines; this task's lines are the t3-* cases and the group=t3 lines. artifacts/observe/observe.py is the Task 1 runner this task imports and artifacts/preflight.json its earlier output (both unchanged in this task). Reading ./artifacts/ files other than the retries folder is allowed. src/superclaude/hooks/scripts/launch-job-identity.sh is an unchanged read-only input.
Delta diff from the previous reviewed tree (empty on the first review): diff --git a/.dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/artifacts/observe/task3.py b/.dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/artifacts/observe/task3.py
index a93180d4..cdf27bc2 100644
--- a/.dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/artifacts/observe/task3.py
+++ b/.dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/artifacts/observe/task3.py
@@ -155,11 +155,18 @@ def entry_from(c, old, label):
     return e
 
 
-def interactive_clear(runner, g, sid_pty, old_pid, timeout=300):
-    """The one owner-authorized interactive run: pty, /clear, one governed command, then end the process."""
+def interactive_clear(runner, g, sid_pty, old, sid_origin, timeout=300):
+    """The one owner-authorized interactive run: pty, /clear, one governed command, then end the process.
+
+    old is the old child's {"pid", "start"} (or None when it did not survive); sid_origin is the session id
+    whose governed record the old child belongs to.
+    """
     rid = ob.new_rid()
+    old_pid = old["pid"] if old else 0
     if runner.real_count() >= runner.cap:
         raise ob.Refused("real Claude run cap reached")
+    check_before = g.store_check(sid_origin)
+    old_before = child_state(old["pid"], old["start"]) if old else None
     script = ob.write_cmd(g, rid, NEXT_BODY % (ob.shlex.quote(str(ob.HELPER)), old_pid, ob.shlex.quote(str(ob.HELPER))))
     log = g.tmp / ("hook-events-%s.jsonl" % rid)
     settings = ob.write_settings(g, "governed", log)
@@ -255,12 +262,16 @@ def interactive_clear(runner, g, sid_pty, old_pid, timeout=300):
                 end_action["then"] = {"signal": "SIGKILL", "sent": res["sent"]}
                 p.wait(timeout=5)
         mp.kill_group()
+        screen_tail = bytes(buf).decode(errors="replace")
         os.close(master)
     rc = p.returncode
     swept = g.sweep(before, "t3-clear") if timed_out else 0
+    old_after = child_state(old["pid"], old["start"]) if old else None
     sel = ob.selector_capture(g, rid)
     sessions, names = set(), []
     for f in (g.home / ".claude").rglob("*.jsonl"):
+        if f.stat().st_mtime < t0:
+            continue  # only transcripts written during this run, not those of earlier runs in the shared HOME
         for line in f.read_text(errors="replace").splitlines():
             try:
                 ev = json.loads(line)
@@ -277,14 +288,20 @@ def interactive_clear(runner, g, sid_pty, old_pid, timeout=300):
                start=started, end=ob.now(), exit=("signal:" + signal.Signals(-rc).name) if rc < 0 else rc, real_claude=True, depth=ob.depth_capture(g, rid) or {"measured": False},
                result=result, held_s=elapsed, timed_out=timed_out, swept=swept, settings_sha256_before=settings_before,
                settings_sha256_after=ob.real_settings_sha(),
-               extra={"store_check": g.store_check(sid_pty), "prompts_sent": prompts, "dialogs_answered": seen["dialogs_answered"],
+               extra={"store_check": check_before, "prompts_sent": prompts, "dialogs_answered": seen["dialogs_answered"],
                       "flag_names": flags, "end_action": end_action, "stages": stages})
     entry = {
         "result": result if done else "unavailable", "run_id": rid, "prompts_sent": prompts, "elapsed_seconds": elapsed,
         "wall_clock_bound_seconds": timeout, "timed_out": timed_out, "dialogs_answered_before_prompts": seen["dialogs_answered"],
         "stages": stages, "how_the_process_was_ended": end_action, "flag_names_used": flags,
         "session_ids_in_hook_events": [h.get("session_id") for h in hooks if h.get("hook_event_name") == "PreToolUse"],
-        "session_ids_in_transcripts": sorted(sessions), "starting_session_id": sid_pty, "tool_names_in_transcripts": names,
+        "check_before_run": check_before,
+        "old_child": {"pid": old_pid, "start_ticks_before_new_process": old_before and old_before["start_ticks_recorded"],
+                      "alive_before": old_before and old_before["alive"], "start_ticks_after_new_process": old_after and old_after["start_ticks_now"],
+                      "alive_after": old_after and old_after["alive"]},
+        "printed_cost": sorted(set(re.findall(r"\$\s?\d+(?:\.\d+)?", screen_tail))) or "none seen in the retained screen tail (last 20000 bytes)",
+        "session_ids_in_transcripts_written_during_this_run": sorted(sessions), "starting_session_id": sid_pty,
+        "tool_names_in_transcripts_written_during_this_run": names,
         "old_child_selector_status": sel[0]["status"] if sel else None, "old_child_origin_session_id": sel[0].get("session_id") if sel else None,
         "new_session_selector_status": sel[1]["status"] if len(sel) > 1 else None, "new_session_selector_session_id": sel[1].get("session_id") if len(sel) > 1 else None,
         "selector_lines": sel, "hook_event_records": hooks,
@@ -349,8 +366,7 @@ def main():
                     out["fork"] = {"result": "unavailable", "missing_interface": "the killed session could not be resumed: %s" % e.get("missing_interface"), "detail": "no retry"}
                     break
         # /clear: the one owner-authorized interactive run (still attempted when the old child is gone; its old-child line is then unreadable).
-        old_pid = old["pid"] if old else 0
-        out["clear"] = interactive_clear(runner, g, str(uuid.uuid4()), old_pid)
+        out["clear"] = interactive_clear(runner, g, str(uuid.uuid4()), old, sid1)
     finally:
         out["teardown"] = g.teardown("task3")
         (ob.GROUPS / "t3.json").unlink()
diff --git a/.dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/artifacts/resume-fork-clear.json b/.dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/artifacts/resume-fork-clear.json
index 4b9e5364..a69438c5 100644
--- a/.dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/artifacts/resume-fork-clear.json
+++ b/.dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/artifacts/resume-fork-clear.json
@@ -1,5 +1,18 @@
 {
   "clear": {
+    "check_before_run": {
+      "captured_for_this_run": false,
+      "nearest_preceding_check": {
+        "from_run": "fork",
+        "note": "taken immediately before the fork run, the last run before this one; nothing deleted the store between the two runs",
+        "origin_session_record_and_store": {
+          "governed_record_exists": true,
+          "store_exists": true
+        },
+        "run_id": "a2d1d6b085c5"
+      },
+      "reason": "the first version of the driver took its only store check after the pty process ended and for the pty session's own starting id (ledger row run-status.jsonl:23 shows governed_record_exists false for that id, which was never made governed), so no pre-run check of the old child's origin session record exists for this run"
+    },
     "dialogs_answered_before_prompts": [],
     "elapsed_seconds": 129.91,
     "flag_names_used": [
@@ -22,25 +35,35 @@
     "missing_interface": "Keyboard input to the interactive Claude Code terminal UI through a pty: the runner sent the two prompts (\"/clear\", then one governed-command prompt) after the screen settled, but nothing shows that either reached a session. There is no transcript for the pty session's starting id, no PreToolUse hook event, and no selector line, after 129.9 seconds and 6288 bytes of terminal output. The cause was not captured (the screen contents were not retained), so no cause is claimed. One attempt, no retry, as the plan bounds it.",
     "new_session_selector_session_id": null,
     "new_session_selector_status": null,
+    "old_child": {
+      "alive_after_new_process": true,
+      "pid": 1416828,
+      "source_of_after_value": "the identity check at group teardown, which ran after the pty process had ended: phase2-cleanup.log:11 stopped the child only after verifying its pid and start ticks still matched the recorded ones. No selector status for the old child was read in this run (the interactive session ran no command).",
+      "start_ticks_after_new_process": 98576077,
+      "start_ticks_before_new_process": 98576077
+    },
     "old_child_origin_session_id": null,
     "old_child_selector_status": null,
+    "printed_cost": "not captured: the first version of the driver did not retain the terminal output (6288 bytes were read and discarded), so any cost the session printed is unknown",
     "prompts_sent": 2,
+    "provenance_note": "Produced by the first version of interactive_clear in artifacts/observe/task3.py. After the first review, task3.py was corrected (pre-run store check for the origin session, old child state before and after, screen tail kept for any printed cost, transcript scan limited to files written during the run). The interactive run was not repeated because the plan allows one attempt and no retry, so the values that version did not capture are recorded above as not captured, with the evidence that does exist and where it came from.",
+    "pty_session_transcript_found": false,
     "result": "unavailable",
     "reused_process_form": "unavailable: the single-process /clear form (a new ordinary session started in a reused Claude process) was not observed; the resume and fork runs start new processes and cannot test it",
     "run_id": "26ebfaffd570",
     "selector_lines": [],
-    "session_ids_in_hook_events": [],
-    "session_ids_in_transcripts": [
+    "session_ids_in_all_group_transcripts": [
       "64b3f68b-b483-42dc-90cf-1a64b2984088",
       "a590b456-1cb9-4c51-91ec-1bbc34f499c4"
     ],
+    "session_ids_in_hook_events": [],
     "stages": {
       "after_clear_quiet": true,
       "startup_quiet": true
     },
     "starting_session_id": "ebb112e0-5ce0-42f7-ace7-8277dbdba1b9",
     "timed_out": false,
-    "tool_names_in_transcripts": [
+    "tool_names_in_all_group_transcripts": [
       "Bash",
       "Bash",
       "Bash",
@@ -54,6 +77,7 @@
       "Bash",
       "Bash"
     ],
+    "transcript_fields_note": "session_ids_in_all_group_transcripts and tool_names_in_all_group_transcripts were read from every transcript in the shared throwaway HOME, so they list the earlier runs of this group (first call, resume, fork) and say nothing about the pty session; the pty session's own starting id is absent (pty_session_transcript_found), which supports the entry's finding that the typed input never reached a session.",
     "wall_clock_bound_seconds": 300
   },
   "decisive_case": {
Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B1 ac=T3.AC1 at=.dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/artifacts/resume-fork-clear.json:2-58 anchor="a check that the launch-level store and governed session record still existed before the run" chk=y,n,n,n family=clear-entry-fields fix=In `interactive_clear` (`task3.py:158`), take `g.store_check(<origin sid1>)` before launching the pty process and write it into the entry as `check_before_run`. The current call at `task3.py:280` runs after the process ended and checks the pty session id, which was never made governed, so `run-status.jsonl:23` shows `governed_record_exists: false`. covers="a check that the launch-level store and governed session record still existed before the run" first=A1 origin=new: The `/clear` entry has no `check_before_run`. The only store check is the ledger row, taken after the run on the wrong session id.
F1.2 sev=blocking trigger=B1 ac=T3.AC1 at=.dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/artifacts/resume-fork-clear.json:2-58 anchor="the old child's process id and start ticks read before and after the new process started (proving it was the same live child)" chk=y,n,n,n family=clear-entry-fields fix=Pass the old child's recorded `pid` and `start` into `interactive_clear` (`task3.py:353` passes only the pid). Read /proc before launch and after the process ended, and write both values to the entry as `old_child.start_ticks_before_new_process` and `old_child.start_ticks_after_new_process`. covers="old child's process id and start ticks read before and after" first=A1 origin=new: The `/clear` entry has no old-child pid or start ticks, although the old child was registered as a survivor and alive for the whole run (`phase2-cleanup.log:11` shows it stopped only at teardown).
F1.3 sev=blocking trigger=B4 ac=scope at=.dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/artifacts/resume-fork-clear.json:2-58 anchor="the run record holds the number of prompts, the elapsed seconds and any cost the session prints" chk=n,n,n,y family=clear-entry-fields fix=Record a cost field in the `/clear` entry. Either keep the last part of the terminal output and take any printed cost from it, or write "no cost seen in the retained output, screen not retained". `task3.py:182-199` keeps only the last 20000 bytes and the entry never stores or searches it. Do this with the F1.1 and F1.2 fix, if any further `/clear` change is made. first=A1 origin=new: The task text requires the run record to hold any cost the session prints. The entry has no cost field and does not say that none was captured.
F1.4 sev=blocking trigger=B2 ac=T3.AC1 at=.dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/artifacts/observe/task3.py:263 anchor=task3.py:263-271 (`for f in (g.home / ".claude").rglob("*.jsonl")` scans every transcript in the shared HOME) chk=n,y,n,n family=clear-entry-fields fix=Restrict the transcript scan to the pty session's own `<sid_pty>.jsonl`. Alternatively, drop `session_ids_in_transcripts` and `tool_names_in_transcripts` from the `/clear` entry, or label them as the whole group's transcripts. Rewrite `resume-fork-clear.json:33-56` accordingly. first=A1 origin=new: In the `/clear` entry, `tool_names_in_transcripts` lists 12 Bash calls and `session_ids_in_transcripts` lists the first-call and fork sessions (`resume-fork-clear.json:33-56`). These come from the earlier runs in the same HOME, not from the pty session. The same entry says there was no transcript for the pty session and no hook event (`resume-fork-clear.json:22`), so the entry contradicts itself.
Saved-probe re-check hit locations (may be empty): artifacts/resume-fork-clear.json:3:    "check_before_run": {
artifacts/resume-fork-clear.json:42:      "start_ticks_after_new_process": 98576077,
artifacts/resume-fork-clear.json:43:      "start_ticks_before_new_process": 98576077
artifacts/resume-fork-clear.json:47:    "printed_cost": "not captured: the first version of the driver did not retain the terminal output (6288 bytes 
artifacts/resume-fork-clear.json:162:    "check_before_run": {
artifacts/resume-fork-clear.json:181:      "start_ticks_after_new_process": 98576077,
artifacts/resume-fork-clear.json:182:      "start_ticks_before_new_process": 98576077
artifacts/resume-fork-clear.json:210:    "check_before_run": {
artifacts/resume-fork-clear.json:229:      "start_ticks_after_new_process": 98576077,
artifacts/resume-fork-clear.json:230:      "start_ticks_before_new_process": 98576077
artifacts/observe/task3.py:146:         "check_before_run": c["store_check"], "hook_event_session_id": hook_session(c), "depth": c["depth"],
artifacts/observe/task3.py:149:                       "pid": old["pid"], "start_ticks_before_new_process": old["start"], "start_ticks_after_new_proces
artifacts/observe/task3.py:168:    check_before = g.store_check(sid_origin)
artifacts/observe/task3.py:298:        "check_before_run": check_before,
artifacts/observe/task3.py:299:        "old_child": {"pid": old_pid, "start_ticks_before_new_process": old_before and old_before["start_ticks_recorded
artifacts/observe/task3.py:300:                      "alive_before": old_before and old_before["alive"], "start_ticks_after_new_process": old_after an
artifacts/observe/task3.py:302:        "printed_cost": sorted(set(re.findall(r"\$\s?\d+(?:\.\d+)?", screen_tail))) or "none seen in the retained scree
artifacts/observe/task3.py:303:        "session_ids_in_transcripts_written_during_this_run": sorted(sessions), "starting_session_id": sid_pty,
artifacts/observe/task3.py:304:        "tool_names_in_transcripts_written_during_this_run": names,

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
