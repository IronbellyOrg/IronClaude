# Live check 1 (troubleshoot), Step 5: transcript conditions

Source named by ac-0.6.md: transcript (`worker-read --source transcript`). Worker: dispatch `ctx_e70499c8ef2d`, terminal `term_9e8c7204-7c7d-4b03-877d-e8b9b275c271`. Run length: first user message (the brief) 06:03:04 UTC, `worker_done` sent 06:48:42 UTC, so 45 min 38 s.

## worker-read completeness (a finding, carried to the phase report)

The plan says to read the whole transcript with `worker-read --source transcript --json` and follow `--cursor` until no next cursor remains. That cannot be done:

- Page 1 (`lc1-transcript-1.json`) returned 40 messages covering only 06:40:23 to 06:48:53 UTC, with `"contentComplete": false`, `"clipping": ["message_limit_or_scan_window","transcript_payload"]` and the warnings "Oversized transcript text was clipped." and "Oversized tool input was clipped." The run lasted 45 minutes.
- The returned cursor never ends: page 2 (`lc1-transcript-2.json`) returned 0 messages and the same cursor. The cursor decodes to byte position `p=6876333`. I followed it through page 60 (all empty); pages 3 to 60 were identical empty files and were deleted, page 2 is kept as the evidence. A cursor that never ends is a pointer to "new messages after this point", not a way back to earlier ones.
- `worker-read --limit 1000` (listed in the verb's `--help`, not in the plan; one read-only attempt, saved as `lc1-transcript-limit1000.json`) returned 50 messages, 06:37:39 to 06:48:53, with the same `contentComplete: false`.

So the prescribed read gives the last 40 to 50 messages only. To still check the five conditions over the whole run, I read the worker's own Claude Code session file, which is the file worker-read reads from (its size equals the cursor position: 6,876,333 bytes at read time; 6,877,095 when analysed, 762 bytes later):

`/home/coder/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-p0-live-troubleshoot/1f67f909-bb49-4ef5-ac82-85648989c522.jsonl` (sha256 `f7eb35e22edeb70afe5eccccfd31771bc8dd29716732006f6152c0b31cdbf747`).

This is a deviation from the plan's method. It is read-only, it creates no Orca object, and it is not a rerun of the check. The analysis is saved in `lc1-session-analysis.txt` (script: `lc1-session-analysis-hb.py`). The 23 session files in that project folder include the 22 subagent sessions; only the top-level session ran any `orca orchestration` command.

## The five conditions

| # | Condition | Verdict | Evidence |
|---|---|---|---|
| 1 | No `AskUserQuestion` call (WC-2) | PASS | Tool tally of the top-level session (`lc1-session-analysis.txt:6-20`): Bash 44, Write 43, Read 22, Agent 22, Edit 8, Grep 6, context7 3, Skill 2, and 6 others (tavily, context7 resolve, codegraph status, codegraph callers, TaskStop, SendMessage). No `AskUserQuestion` in the top-level session or in any of the 22 subagent sessions (a case-insensitive search of every session's tool names for "ask" or "question" matched only `TaskStop`, whose name contains "ask"). |
| 2 | The command was invoked in the top-level session, not inside an Agent-tool call (WC-7) | PASS | `lc1-session-analysis.txt:23`: `2026-11-04T06:03:20.276Z sidechain=false skill=sc-troubleshoot-protocol`, 16 s after the brief arrived (06:03:04). All 250 top-level assistant messages have `isSidechain=false`. The first Agent call is at 06:05:30, after the Skill call. Every `orca orchestration` command (17) is in the top-level session; no subagent session ran one. |
| 3 | A `check` call appears after the command finished and before `worker_done` (WC-12) | PASS | `lc1-session-analysis.txt:42-43`: `06:48:34.495Z orca orchestration check --terminal term_9e8c7204-...` then `06:48:42.905Z orca orchestration send ... --type worker_done`. The command's last write, `REPORT.md`, is at 06:48:24 (worker-read: `Write` of `.dev/p0-live/troubleshoot/REPORT.md`, timestamp 1793774904100). The same two calls are also in `lc1-transcript-limit1000.json` (Bash `command` values `orca orchestration check --terminal ... --json` and `orca orchestration send ... --type worker_done`). |
| 4 | Heartbeat `send` calls at most the preamble's cadence apart, except inside an Agent-tool call or a blocked `ask` / `check --wait` (WC-10) | PASS with a note | Cadence quoted from the dispatch preamble (first user message): "Send a heartbeat every 5 minutes while actively working on the task ... Skip heartbeats only while blocked inside `check --wait` or `ask`". 15 heartbeats at 06:03:19, 06:04:07, 06:07:10, 06:09:03, 06:11:35, 06:14:30, 06:17:02, 06:20:13, 06:20:59, 06:21:39, 06:29:09, 06:31:29, 06:37:51, 06:40:41, 06:44:43. Gaps in minutes: 0.8, 3.1, 1.9, 2.5, 2.9, 2.5, 3.2, 0.8, 0.7, **7.5**, 2.3, **6.4**, 2.8, 4.0; last heartbeat to `worker_done` 4.0. Two gaps are over 5 minutes. See the note below. |
| 5 | No `worker-start`, `dispatch` or `task-create` call and no `worktree create --agent` or `agent launch` call (WC-13) | PASS | Search of every Bash command in all 23 session files (52 Bash tool calls; the 68 in an earlier draft was a line count of `/tmp/ironclaude-p0live/lc1-all-bash.txt`, not kept, where multi-line commands count once per line) for `worker-start`, `orchestration dispatch`, `task-create`, `worktree create`, `agent launch`, `orca worktree`, `orca agent`: no match. The only Orca verbs used: `orca orchestration send` and `orca orchestration check`. |

Step 5 verdict: **PASS** (all five conditions hold), with the method deviation and the note below.

## Note on condition 4 (the two gaps over 5 minutes)

- 06:21:39 to 06:29:09 (7.5 min): the command's Agent fan-out was running the whole time: a background Agent launched 06:21:35 (finished 06:25:44 per its task notification), then four background advocate Agents launched 06:26:00 to 06:26:21, then the session wrote files (06:26:27 to 06:29:04) while they ran. The session was never blocked in `ask` or `check --wait`.
- 06:31:29 to 06:37:51 (6.4 min): the session was idle waiting for the background Agent launched 06:29:31, whose notification arrived 06:37:32; the heartbeat followed at 06:37:51.
- The Agent calls return at once ("Async agent launched successfully") so in the file their start and end are the same second. I judged both gaps as the "Agent-tool fan-out" gap that WC-10 accepts (`WORKER-CONTRACT.md:44`: "can hold the session longer than the cadence with no way to heartbeat; that gap is accepted"). A stricter reading, counting only time inside a blocking Agent call, would flag part of both gaps (for example 06:26:39 to 06:29:09, when the session was busy writing files with agents still running). This run is longer than the heartbeat cadence (45.6 min against 5 min), so the heartbeat condition was not passed vacuously.
- Added after check 2 (a measure that does not depend on the immediate Agent return): each subagent's own session file gives its first and last timestamp; removing that time from every heartbeat gap leaves a longest stretch of **2.2 min** without a heartbeat (table at the end of `lc1-session-analysis.txt`, script `session-hbcover.py`). On that measure no gap exceeds the 5-minute cadence. On the literal "inside an Agent-tool call" wording the two long gaps are still covered only by the WC-10 accepted-gap reading above.

## Read after release (added after Step 7)

After `worker-release` (`lc1-step7.txt` shows `archive.status: captured`), one more `worker-read --source transcript` (`lc1-transcript-after-release.json`) returned 40 messages, 06:37:39 to 06:47:34 UTC, still `contentComplete: false` with `clipping: [message_limit, message_limit_or_scan_window, transcript_payload]`. Releasing the worker does not make the whole transcript readable through worker-read.
