# Live check 2 (workflow), Step 5: transcript conditions

Source named by ac-0.6.md: transcript (`worker-read --source transcript`; `ac-0.6.md` says yes). Worker: dispatch `ctx_5ba7416bd360`, terminal `term_dab36efa-1676-4c83-90e5-af470dbe9097`. Run length: brief arrived 06:58:42 UTC, `worker_done` sent 08:25:37 UTC, so 86 min 55 s (longer than the 5-minute heartbeat cadence).

## worker-read completeness (same finding as check 1, `lc1-step5.md`)

Page 1 (`lc2-transcript-1.json`) returned 40 messages from timestamp 1793780527288 (08:22:07 UTC) to 1793780748337 (08:25:48 UTC), `"contentComplete": false`, `"clipping": ["message_limit_or_scan_window","transcript_payload"]`. Page 2 (`lc2-transcript-2.json`, read with the returned cursor) returned 0 messages and a cursor again; the cursor decodes to byte position `p=5860827`, which is the exact size of the worker's session file. I stopped after page 2 (check 1 showed the cursor never ends).

So the prescribed read covers only the last 3 minutes of an 87-minute run. As for check 1, the five conditions were checked on the worker's own Claude Code session file (the file worker-read reads from):

`/home/coder/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-p0-live-workflow/eb1ade47-a572-4888-b9a4-9e16721ca41c.jsonl` (5,860,827 bytes, sha256 `36f78229f737e8ae864841fa242f4175c682cc2cc94e6f5b4f5b14618d593692`; the 23 subagent sessions are in its `subagents/` folder).

This is the same method deviation as in check 1: read-only, creates no Orca object, is not a rerun. The analysis is in `lc2-session-analysis.txt` (scripts: `session-analysis.py`, `session-hbcover.py`).

## The five conditions

| # | Condition | Verdict | Evidence |
|---|---|---|---|
| 1 | No `AskUserQuestion` call (WC-2) | PASS | `lc2-session-analysis.txt`, tool tally (Bash 47, Read 28, Write 25, Agent 23, Edit 8, Skill 3, Grep 3, codegraph status 1). The last line of that file searches the tool names of all 24 session files for "ask" or "question": `{}` (no match). |
| 2 | The command was invoked in the top-level session, not inside an Agent-tool call (WC-7) | PASS | `2026-11-04T06:58:57.925Z sidechain=False skill=sc-workflow-protocol`, 15 s after the brief arrived (06:58:42). Assistant messages with `isSidechain=true` in the top-level session: 0. The first Agent call is at 07:02:02. All 19 `orca orchestration` commands are in the top-level session; the search over all 24 session files found only the verbs `check` and `send`. |
| 3 | A `check` call appears after the command finished and before `worker_done` (WC-12) | PASS | The command's last write, `return-contract.yaml`, is at 08:25:20; then `08:25:27 orca orchestration check` ("Confirm the single new package, its status, worktree state, and coordinator follow-ups"), then `08:25:37 orca orchestration send ... --type worker_done`. |
| 4 | Heartbeat `send` calls at most the preamble's cadence apart, except inside an Agent-tool call or a blocked `ask` / `check --wait` (WC-10) | PASS | Cadence quoted from the dispatch preamble: "Send a heartbeat every 5 minutes while actively working on the task ... Skip heartbeats only while blocked inside `check --wait` or `ask`". 17 heartbeats. Raw gaps in minutes: 1.6, 1.5, 3.0, **9.4**, 1.2, 0.8, **5.9**, **7.7**, **8.2**, 3.7, 4.3, **9.5**, **14.5**, 3.7, 3.4, **6.1**; last heartbeat to `worker_done` 2.1. Six raw gaps are over 5 minutes. With the time that subagents were running removed (each subagent's first to last timestamp in its own session file), the longest stretch without a heartbeat is **2.0 min** (table at the end of `lc2-session-analysis.txt`). The session was never blocked in `ask` or `check --wait`. |
| 5 | No `worker-start`, `dispatch` or `task-create` call and no `worktree create --agent` or `agent launch` call (WC-13) | PASS | `lc2-session-analysis.txt`: 64 Bash commands in 24 session files, 0 matches for `worker-start`, `orchestration dispatch`, `task-create`, `worktree create`, `agent launch`, `orca worktree`, `orca agent`; the only Orca verbs are `orca orchestration check` and `orca orchestration send`. |

Step 5 verdict: **PASS** (all five conditions hold), with the method deviation above. Condition 4 passes on the "subagent time does not count" reading of WC-10 (`WORKER-CONTRACT.md:44`); on a literal reading of "inside an Agent-tool call" (the Agent calls return at once as "Async agent launched successfully") the six long raw gaps would not be covered, so the phase report carries this as a note, as for check 1.
