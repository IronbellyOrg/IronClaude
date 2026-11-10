# Live check 3 (adversarial), Step 5: transcript conditions

Source named by ac-0.6.md: transcript (`worker-read --source transcript`; `ac-0.6.md` says yes). Worker: dispatch `ctx_40a6876cca04`. Run length: brief arrived 08:31:51 UTC, `worker_done` sent 09:03:31 UTC, so 31 min 40 s (longer than the 5-minute heartbeat cadence).

## worker-read completeness (same finding as checks 1 and 2)

Page 1 (`lc3-transcript-1.json`) returned 40 messages from timestamp 1793782622610 to 1793783021347 (about 08:57 to 09:03:41 UTC), `"contentComplete": false`, `"clipping": ["message_limit_or_scan_window","transcript_payload"]`. Page 2 (`lc3-transcript-2.json`, read with the returned cursor) returned 0 messages and a cursor again; the cursor decodes to byte position `p=4343356`, the exact size of the worker's session file. So the prescribed read covers only the last 6 minutes of a 32-minute run.

As in checks 1 and 2, the five conditions were checked on the worker's own Claude Code session file (the file worker-read reads from):

`/home/coder/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-p0-live-adversarial/1f377cc6-5882-4867-ab45-be13ad1408a6.jsonl` (4,343,356 bytes, sha256 `1822988c7312e4b0876d607f990e1fd7cf35d56e63c3b9780a76a367df1df246`; its 7 subagent sessions are in the `1f377cc6-...` folder next to it). This is the same method deviation as in checks 1 and 2: read-only, creates no Orca object, not a rerun. The analysis is in `lc3-session-analysis.txt` (scripts: `session-analysis.py`, `session-hbcover.py`).

## The five conditions

| # | Condition | Verdict | Evidence |
|---|---|---|---|
| 1 | No `AskUserQuestion` call (WC-2) | PASS | `lc3-session-analysis.txt`, tool tally (Edit 44, Bash 26, Read 22, Agent 7, Grep 4, Write 4, Glob 2, SendMessage 2, Skill 1). The tool names of all 8 session files contain no "ask" or "question": `{}`. |
| 2 | The command was invoked in the top-level session, not inside an Agent-tool call (WC-7) | PASS | `2026-11-04T08:32:06.701Z sidechain=False skill=sc-adversarial-protocol`, 15 s after the brief arrived (08:31:51). Assistant messages with `isSidechain=true` in the top-level session: 0. The first Agent call is at 08:34:17. All 9 `orca orchestration` commands are in the top-level session; the only Orca verbs in all 8 session files are `check` and `send`. (The two `SendMessage` calls go to the command's own subagents, not to Orca.) |
| 3 | A `check` call appears after the command finished and before `worker_done` (WC-12) | PASS | `09:03:21 orca orchestration check`, then `09:03:31 orca orchestration send ... --type worker_done`. The command's last Agent call (08:58:31, the merge) finished at 09:02:45 (its task notification), and the worker's last file write (09:03:15) precedes the check. |
| 4 | Heartbeat `send` calls at most the preamble's cadence apart, except inside an Agent-tool call or a blocked `ask` / `check --wait` (WC-10) | PASS | Cadence quoted from the dispatch preamble (line 31 of its first user message): "Send a heartbeat every 5 minutes while actively working on the task ... Skip heartbeats only while blocked inside `check --wait` or `ask`". 7 heartbeats at 08:32:04, 08:33:51, 08:38:12, 08:41:49, 08:47:03, 08:54:43, 08:57:35. Raw gaps in minutes: 1.8, 4.4, 3.6, **5.2**, **7.7**, 2.9; last heartbeat to `worker_done` **5.9**. With the time that subagents were running removed (first to last timestamp of each subagent's own session file), the longest stretch without a heartbeat is **3.3 min** (table at the end of `lc3-session-analysis.txt`). The session was never blocked in `ask` or `check --wait`. |
| 5 | No `worker-start`, `dispatch` or `task-create` call and no `worktree create --agent` or `agent launch` call (WC-13) | PASS | `lc3-session-analysis.txt`: 50 Bash commands in 8 session files, 0 matches for `worker-start`, `orchestration dispatch`, `task-create`, `worktree create`, `agent launch`, `orca worktree`, `orca agent`. |

Step 5 verdict: **PASS** (all five conditions hold), with the method deviation above.

Note on condition 4: it passes on the "subagent time does not count" reading of WC-10 (`WORKER-CONTRACT.md:44`), as in checks 1 and 2. In this run the stricter wall-clock count is also exceeded in three places, and one of them is not covered by a running subagent: from 08:41:49 the worker was editing files (08:41:54 to 08:46:25) with no subagent running after 08:43:42, and its next heartbeat came at 08:47:03, 5.2 min after the previous one (the 5-minute mark, 08:46:49, fell 14 s before the heartbeat). The phase report carries this as a note.
