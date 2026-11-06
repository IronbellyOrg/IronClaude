# lc16 (workflow) Step 5: transcript conditions

Session file: `/home/coder/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-p1-live-workflow/bd2c3553-e0a2-49ef-94c0-1052a189b459.jsonl` (4798222 bytes at analysis time, sha256 `05e687f944b47ad69e7a17e2de0d62d9a0f52364130ec70bfe319efaa4a773c3`; the file keeps growing after worker_done, so this is the first recorded length). Top-level .jsonl files in the folder: 1; subagent session files: 18. Analysis: `lc16-session-analysis.txt` (P0 scripts `session-analysis.py` and `session-hbcover.py`).

Cadence quoted from the worker's preamble: "Send a heartbeat every 5 minutes while actively working on the task." Run length 21.8 min; heartbeats (5): ['20:41:38', '20:44:29', '20:46:18', '20:50:37', '20:55:59'].

Cross-check: `lc16-transcript-1.json` (page 1) holds 40 messages, `contentComplete: false`, clipping ["message_limit_or_scan_window","transcript_payload"]; `lc16-transcript-2.json` (page 2, read with the returned cursor) holds 0 messages. Final `check` call and `worker_done` in the session file: `21:01:22 check ` / `21:01:29 send worker_done`; page 1 ends with the same `orca orchestration check` and `orca orchestration send ... --type worker_done` calls (checked in `lc16-step5-crosscheck.txt`).

| # | Condition | Verdict | Evidence |
|---|---|---|---|
| 1 | No AskUserQuestion call (WC-2) | PASS | `lc16-session-analysis.txt`: "tool names containing ask/question (case-insensitive), all sessions: {}" |
| 2 | Command run in the worker's top-level session, not inside an Agent-tool call (WC-7) | PASS | assistant messages with isSidechain=true: 0; ## Agent launches (top-level): ['20:43:18', '20:43:21', '20:43:25', '20:43:28', '20:44:20', '20:44:23', '20:44:25', '20:46:07', '20:46:10', '20:46:14', '20:48:40', '20:49:38', '20:50:33', '20:51:21', '20:51:50', '20:51:56', '20:55:36', '20:58:27']; Skill calls: 2026-11-05T20:40:01.576Z sidechain=False skill=sc-workflow-protocol;2026-11-05T20:41:03.922Z sidechain=False skill=sc-reflect-protocol;2026-11-05T20:44:55.170Z sidechain=False skill=sc-adversarial-protocol. |
| 3 | A `check` call after the command finished and before `worker_done` (WC-12) | PASS | last non-Orca tool call at 21:01:15, `check` at 21:01:22, `worker_done` at 21:01:29. |
| 4 | Heartbeats within the cadence (WC-10), limits (a) and (b) of spec 7.2 step 5 | PASS | raw gaps (min) [2.9, 1.8, 4.3, 5.4]; brief to first heartbeat 1.9 min; last heartbeat to worker_done 5.5 min; max non-agent stretch 2.7 min (limit a: at most 5; limit b: at most 20 with nothing removed). |
| 5 | No worker-start, dispatch or task-create, no worktree create --agent or agent launch (WC-13) | PASS | WC-13 pattern hits: 0; orca verbs in all sessions: ['orca orchestration check', 'orca orchestration send'] |

Step 5 verdict: PASS
