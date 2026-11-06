# lc11 (cleanup-audit) Step 5: transcript conditions

Session file: `/home/coder/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-p1-live-cleanup-audit/9b25f116-6e03-4fab-9468-13a4da4d306d.jsonl` (2274417 bytes at analysis time, sha256 `840b2ec067143a64cefcf1afcdc3d98cbf4c6a1a6d4e64ef5764ae7f63cab887`; the file keeps growing after worker_done, so this is the first recorded length). Top-level .jsonl files in the folder: 1; subagent session files: 3. Analysis: `lc11-session-analysis.txt` (P0 scripts `session-analysis.py` and `session-hbcover.py`).

Cadence quoted from the worker's preamble: "Send a heartbeat every 5 minutes while actively working on the task." Run length 5.4 min; heartbeats (3): ['20:10:56', '20:12:08', '20:15:03'].

Cross-check: `lc11-transcript-1.json` (page 1) holds 40 messages, `contentComplete: false`, clipping ["message_limit_or_scan_window","transcript_payload"]; `lc11-transcript-2.json` (page 2, read with the returned cursor) holds 0 messages. Final `check` call and `worker_done` in the session file: `20:15:56 check ` / `20:16:02 send worker_done`; page 1 ends with the same `orca orchestration check` and `orca orchestration send ... --type worker_done` calls (checked in `lc11-step5-crosscheck.txt`).

| # | Condition | Verdict | Evidence |
|---|---|---|---|
| 1 | No AskUserQuestion call (WC-2) | PASS | `lc11-session-analysis.txt`: "tool names containing ask/question (case-insensitive), all sessions: {}" |
| 2 | Command run in the worker's top-level session, not inside an Agent-tool call (WC-7) | PASS | assistant messages with isSidechain=true: 0; ## Agent launches (top-level): ['20:11:59', '20:12:03', '20:14:28']; Skill calls: 2026-11-05T20:10:55.562Z sidechain=False skill=sc:cleanup-audit-protocol. |
| 3 | A `check` call after the command finished and before `worker_done` (WC-12) | PASS | last non-Orca tool call at 20:15:51, `check` at 20:15:56, `worker_done` at 20:16:02. |
| 4 | Heartbeats within the cadence (WC-10), limits (a) and (b) of spec 7.2 step 5 | PASS | raw gaps (min) [1.2, 2.9]; brief to first heartbeat 0.3 min; last heartbeat to worker_done 1.0 min; max non-agent stretch 1.0 min (limit a: at most 5; limit b: at most 20 with nothing removed). |
| 5 | No worker-start, dispatch or task-create, no worktree create --agent or agent launch (WC-13) | PASS | WC-13 pattern hits: 0; orca verbs in all sessions: ['orca orchestration check', 'orca orchestration send'] |

Step 5 verdict: PASS
