pick: advice-3-a.md; runner-up: advice-3-b.md; reason: tie, -a

## Task 3: Write the Orca terminal driver

Acceptance criteria:
- With a stub `orca` whose `read --screen` output is scripted, the self-test shows each of the four outcomes of `send` (`stop`, `blocked`, `idle`, `timeout`), and `NEEDS_INPUT` for a screen holding a permission dialog. (T3.AC1)
- The self-test shows that `send` refuses a text starting with `[sc-launch:v1:` and exits non-zero without calling `orca`. (T3.AC2)
- The self-test shows two blocked prompts in a row: the second send does not report `blocked` from the first send's still-visible `Blocked:` line; it ends on its own new block or its Stop event. (T3.AC3)
- The self-test shows `wait-notice`: a scripted log where the Stop event precedes the `<task-notification>` prompt keeps `send` waiting until the notice and its answer (a further Stop) appear, and times out to `PENDING` when they never do. (T3.AC4)
- The self-test shows `answer` refusing a key line starting with `[sc-launch:v1:`, appending its line to the run log, and sending nothing else. (T3.AC5)
- The help output of the real `orca` for `terminal send`, `read`, `wait`, `create` and `list` is saved to `./artifacts/t3-orca-help.txt`. (T3.AC6)

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

differs-by: the self-test feeds the log to the driver one event per poll (released by the stub's `terminal wait` arm), so the state where only the turn's Stop exists is actually seen, and the notice check reads only lines added after a line count taken before the send. Both earlier attempts wrote every event at send time or before it, and counted Stop events from the start of the log.
