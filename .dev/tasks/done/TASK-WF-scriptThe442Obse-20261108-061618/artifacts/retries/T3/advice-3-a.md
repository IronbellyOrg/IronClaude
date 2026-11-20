# advice-3-a.md — escalation 1, adviser A (executor family, top rung: opus)
# STATUS: COMPLETE. First answer saved below; the truncated steps tail was resent in
# full on 2026-11-09 ~10:45Z after the model-pool windows reopened, and steps 1-11 are
# now complete. Parent check (procedure step 4): outcome line OK, one row per
# T3.AC1-6, differs-by non-empty, citations within attempt-2.diff / review-2.md —
# PASSED. Pick: winner (tie with -b on 1 blocking finding cited; ties go to -a).

outcome: ready

| AC | why earlier attempts missed it (path:line) | change |
|---|---|---|
| T3.AC1 | Fine. Marked met at review-2.md:4. The four outcomes and NEEDS_INPUT cases are at attempt-2.diff:102-145. | No change. Keep these cases as they are. The new notice cases add about 30 s, so check that the whole driver self-test still finishes inside its 120 s bound at attempt-2.diff:333. |
| T3.AC2 | Fine. Marked met at review-2.md:5. The marker refusal is at attempt-2.diff:214-219 and attempt-2.diff:245, and its case is at attempt-2.diff:146-151. | No change. |
| T3.AC3 | Fine. Marked met at review-2.md:6. The baseline is taken before the send (attempt-2.diff:252), only an increase counts (attempt-2.diff:40), and the case is at attempt-2.diff:116-123. | No change. |
| T3.AC4 | Unmet (review-2.md:7, review-2.md:10). Two causes. (1) The code: the awk at attempt-2.diff:59-62 only makes a decision when it sees a Stop past the turn's own Stop (attempt-2.diff:61). When the log ends at the turn's Stop, awk reaches the end of the file and exits 0, which counts as "answered". It also reads the whole log from line 1, so a notice written before the send still counts. (2) The self-test never creates the in-between state where only the turn's Stop exists. The stub writes Stop, the notice prompt, Stop, Stop all in one `terminal send` call (attempt-2.diff:313-319), so on its first look the driver already sees the full sequence. The "never arrives" case has no Stop at all (attempt-2.diff:160-163), so the gate at attempt-2.diff:30 never calls `notice_answered`. The non-notice case writes its log before the send (attempt-2.diff:165-169), so `stop_before` is 2 (attempt-2.diff:251), no new Stop ever appears, and `notice_answered` is never called. That is how wrong notice logic passed its own self-test. | Read only the log lines added after a line count taken before the send. Replace the latch with a strict in-order match (turn Stop, then a `<task-notification>` prompt, then another Stop) that fails by default at end of file. Make the stub release log events one at a time, one per driver poll, so the self-test sees `send` still waiting while only the turn's Stop exists. Add these cases: the log ends at the turn's Stop; a non-notice prompt between two Stops; a notice from before the send. |
| T3.AC5 | Fine. Marked met at review-2.md:8. The answer path is at attempt-2.diff:266-277 and its cases are at attempt-2.diff:171-177. | No change. |
| T3.AC6 | Fine. Marked met at review-2.md:9. Nothing in this fix touches the help capture. | No change. |

differs-by: the self-test feeds the log to the driver one event per poll (released by the stub's `terminal wait` arm), so the state where only the turn's Stop exists is actually seen, and the notice check reads only lines added after a line count taken before the send. Both earlier attempts wrote every event at send time or before it, and counted Stop events from the start of the log.

Steps:
1. In `.dev/issues/442/scripts/driver.sh`, `send` branch, next to the `stop_before` line, take a line baseline before the send: `lines_before=0; [ -f "$log" ] && lines_before=$(wc -l < "$log")`. Pass it to `wait_turn` as an 8th argument.
2. In `.dev/issues/442/scripts/driver-helpers.sh`, update the `wait_turn` signature comment (line 3) and the locals so the new argument is accepted. Then call `notice_answered "$log" "$lines_before"` in place of the current call.
3. (rest) Rewrite the body of notice_answered in .dev/issues/442/scripts/driver-helpers.sh to read only the new lines, as a strict in-order match that fails by default:
   command timeout "${OB_TIMEOUT_S:-60}" tail -n +"$(( $2 + 1 ))" "$1" 2>/dev/null | awk '
     st == 0 && /"hook_event_name":"Stop"/ { st = 1; next }
     st == 1 && /"hook_event_name":"UserPromptSubmit"/ && /<task-notification>/ { st = 2; next }
     st == 2 && /"hook_event_name":"Stop"/ { st = 3 }
     END { exit (st == 3 ? 0 : 1) }'
   Do not use an exit inside a rule. The END result is the only success path.
4. In .dev/issues/442/scripts/selftest.sh, stub orca, 'terminal wait' arm: before the idle-on check, if $L/stages.txt is not empty, append its first line to $STUB_STOP_LOG and rewrite the file without that line (tail -n +2 into a temp file in $L, then mv). Remove the STUB_NOTICE branch in the 'terminal send' arm, because nothing will use it.
5. In .dev/issues/442/scripts/driver-selftest.sh, replace the "notice arrives and is answered" case. Empty the log, write three stage lines to $L/stages.txt (Stop, then a UserPromptSubmit whose prompt contains <task-notification>, then Stop), and send with timeout 30 and wait-notice. Pass only if the last line is "TURN_END stop" and $L/stages.txt is empty, which proves send ended only after the last staged event. Delete $L/stages.txt afterwards.
6. Add a case where the log ends at the turn's Stop: stage only a Stop, timeout 6, expect output line 2 to be "PENDING notice-not-arrived".
7. Replace the vacuous non-notice case (current lines 87-91). Stage Stop, then a UserPromptSubmit with "prompt":"just a user typing", then Stop. Use timeout 10 and expect "PENDING notice-not-arrived" on line 2.
8. Add a case for a notice from before the send. Before the send, write Stop, a <task-notification> UserPromptSubmit, and Stop into the log. Stage Stop and Stop, use timeout 8, and expect "PENDING notice-not-arrived" on line 2.
9. Keep the existing case where no event ever arrives (current lines 82-85). Update the header comment in driver-selftest.sh (it still mentions STUB_NOTICE) to describe stages.txt.
10. Run bash .dev/issues/442/scripts/selftest.sh and save its full output to .dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/artifacts/t3-selftest.txt. It must end SELFTEST_OK.
11. Before finishing, check by reasoning that the attempt 2 awk would fail steps 5, 6 and 8 under the staged stub. Step 5 fails because it would end at the first Stop and leave stages unused. Steps 6 and 8 fail because it would print "TURN_END stop".

Not checked: nothing was run (read-only role). The extra self-test time is estimated from the 2 s poll interval, not measured. delta-3-2.txt lists deletions of every script file, which does not match the live tree, so it was not used as evidence.
