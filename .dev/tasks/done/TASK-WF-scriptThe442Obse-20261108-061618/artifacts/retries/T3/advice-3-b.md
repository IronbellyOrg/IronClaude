model: opus family: claude rung: top
family-fallback: no GPT T1 model reachable on this install; strongest reachable model used
# advice-3-b.md — escalation 1, adviser B (other family; family-fallback)
# STATUS: COMPLETE. First answer saved below; the truncated steps tail was resent in
# full on 2026-11-09 ~10:45Z after the model-pool windows reopened, and steps 1-7 are
# now complete. Parent check (procedure step 4): outcome line OK, one row per
# T3.AC1-6, differs-by non-empty, citations within attempt-2.diff / review-2.md /
# extras-2.log — PASSED.

outcome: ready

| AC | why earlier attempts missed it or were fine (path:line) | change |
|---|---|---|
| T3.AC1 | Fine. The review marks it met (review-2.md:4). The stop, blocked, idle, timeout and NEEDS_INPUT cases are at attempt-2.diff:102-144. | No change. The stub edit in step 4 must keep `STUB_STOP=1` writing one Stop on `terminal send` (attempt-2.diff:313-314), because the send-stop case at attempt-2.diff:103-107 depends on it. |
| T3.AC2 | Fine (review-2.md:5). The marker refusal happens before any orca call (attempt-2.diff:245, 214-219), and the test is at attempt-2.diff:146-151. | No change. |
| T3.AC3 | Fine (review-2.md:6). The baseline case is at attempt-2.diff:116-123, and the block count is taken before the send (attempt-2.diff:252). | No change. |
| T3.AC4 | Unmet (review-2.md:7, 10). Three things are wrong. (1) The awk at attempt-2.diff:59-62 only decides inside the `s > a` branch. When the log ends at the turn's Stop, it reaches end of input and awk exits 0, so `notice_answered` reports success and `wait_turn` returns `stop` right away (attempt-2.diff:31-34). (2) `seen_notice` is set by any `<task-notification>` line anywhere in the file, including lines from before the send. Resetting `prompt` at `s == a` (attempt-2.diff:61) does not clear `seen_notice`. (3) None of the notice tests reaches the failing state. The stub writes Stop, notice, Stop, Stop all inside one `terminal send` (attempt-2.diff:315-319), so the log is never left ending at the turn's Stop. The PENDING case has no Stop at all, because `STUB_STOP` was unset at attempt-2.diff:158 and not set again before attempt-2.diff:160-163, so it times out before the notice check ever runs. The non-notice case writes its Stops before the send, so `stop_before` already counts them and no new Stop arrives (attempt-2.diff:165-169). All three pass without the notice logic doing anything. | Change the check so it reads only the log lines added after the send, and so it succeeds only on an explicit Stop, then notice, then Stop match, failing by default at end of input. Have the stub add the notice on a later poll, not inside `send`. Add tests for: log ends at the turn's Stop; a notice from before the send; and a late non-notice prompt. |
| T3.AC5 | Fine (review-2.md:8). The test is at attempt-2.diff:171-177. | No change. |
| T3.AC6 | Fine (review-2.md:9). | No change. |

differs-by: The earlier attempts scanned the whole log, decided by counting Stops, and treated falling through as success. This approach captures a line-count baseline before the send, reads only the lines added after it, and succeeds only when awk explicitly matches Stop, then a `<task-notification>` UserPromptSubmit line, then Stop (`END` exits 1 unless matched). The stub adds the notice on a later `terminal wait` poll, so the self-test actually sees `send` waiting while the log ends at the turn's Stop.

steps:
1. In driver.sh `send`, next to `stop_before` (attempt-2.diff:251), capture `lines_before=$( { wc -l < "$log"; } 2>/dev/null || printf 0)`, with a fallback to 0 when the log is missing. Pass it to `wait_turn` as an 8th argument (attempt-2.diff:255). Add it to the usage comment at the top of driver-helpers.sh and to the `local` list in `wait_turn`.
2. In driver-helpers.sh, replace `notice_answered` (attempt-2.diff:57-63) with `notice_answered <log> <lines_before>`. It should run `tail -n "+$((lines_before + 1))" "$log" 2>/dev/null | awk '...'`, wrapped in the same `command timeout "${OB_TIMEOUT_S:-60}"` pattern the file already uses. The awk is a state machine. State 0 goes to 1 on a line matching `"hook_event_name":"Stop"`. State 1 goes to 2 on a single line that matches both `"hook_event_name":"UserPromptSubmit"` and `<task-notification>`; other prompt lines leave the state alone. State 2 on a Stop line sets `ok=1` and exits. Use `END { exit (ok ? 0 : 1) }`. Do not keep a flag that carries over between lines (no `prompt` or `seen_notice` latch). Use the same Stop pattern as the existing grep (attempt-2.diff:28).
3. In `wait_turn`, call `notice_answered "$log" "$lines_before"` at the notice branch (attempt-2.diff:33). Leave the other stop conditions and the PENDING output (attempt-2.diff:50-53) unchanged.
4. In the selftest.sh stub, delete the burst that writes notice, Stop, Stop inside `terminal send` (attempt-2.diff:315-319). Add to the `terminal wait` arm (attempt-2.diff:322-324): when `STUB_LATE` and `STUB_STOP_LOG` are both set, increment a counter stored in `$L/wait-n`. When the counter equals `${STUB_LATE_AT:-2}`, append one line `{"hook_event_name":"UserPromptSubmit","prompt":"<STUB_LATE text>"}` and then one Stop line to `$STUB_STOP_LOG`, writing the text with a jq-escaped or fixed printf. Then fall through to the existing idle-on exit codes.
5. In driver-selftest.sh, replace the three notice cases (attempt-2.diff:153-169). Clear `$L/wait-n`, the screen and the stop log before each case, and unset `STUB_LATE` and `STUB_LATE_AT` after each.
   a. Answered: `STUB_STOP=1 STUB_LATE='<task-notification>x' STUB_LATE_AT=2`, timeout 30. Expect the last line to be `TURN_END stop`, and `cat "$L/wait-n"` to equal `2`. The counter proves `send` kept polling while the log ended at the turn's Stop.
   b. Log ends at the turn's Stop: `STUB_STOP=1` with no `STUB_LATE`, timeout 4. Expect line 2 to be `PENDING notice-not-arrived`. This case returns `TURN_END stop` in 0.07s against the attempt-2 code.
   c. Notice from before the send: seed the stop log with a `<task-notification>` UserPromptSubmit line and a Stop before the send, then send with `STUB_STOP=1` and no `STUB_LATE`, timeout 4. Expect `PENDING notice-not-arrived`.
   d. Late non-notice prompt: `STUB_STOP=1 STUB_LATE='just a user typing' STUB_LATE_AT=1`, timeout 4. Expect `PENDING notice-not-arrived`.
6. Run `timeout 120 bash .dev/issues/442/scripts/selftest.sh` and replace `.dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/artifacts/t3-selftest.txt` with the new output (extras-2.log:1 records it there). Confirm all the older OK lines still show, and the four new notice lines.
7. Check the old code against the new tests by reasoning, not by running it. With the attempt-2 awk, case 5a ends with `wait-n` empty and case 5b ends with `TURN_END stop`, so the new tests catch the review's failure (review-2.md:10).

Not run, not verified: worked from attempt-2.diff; the live driver.sh, driver-selftest.sh and selftest.sh were not read separately. The real hook log format (one JSON line per event, no space after the colon) is UNVERIFIED; assumed because the existing grep already depends on it (attempt-2.diff:28).
