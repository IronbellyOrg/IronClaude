# Update 1: evidence supplied by ORCH-IronClaude, checked against primary artifacts

This file does not replace REPORT.md (status partial, validated). It records new evidence and what it changes. Everything below marked VERIFIED was re-read from a transcript or Orca's log in the turn that wrote this file. Everything marked CLAIM is the orchestrator's statement only.

## VERIFIED
1. Worker session 955b0bcc ran a bare worktree create. Transcript ~/.claude/projects/-home-coder-workspaces-IronClaude/955b0bcc-fb52-44eb-a8eb-6c3e6af79d52.jsonl, Bash tool call at 2026-11-07T20:35:28.903Z:
   `orca worktree create --name fix-flaky-parallel-thread-test --base-branch origin/master 2>&1 | tail -5; orca worktree list 2>&1 | grep -i flaky`
   There is no `--agent`. It is the only `orca worktree create` call in that transcript.
2. Orca's daemon log has exactly one session for that worktree at creation: `{"ts":"2026-11-07T20:35:31.197Z","pid":2935621,"event":"session-created", ... fix-flaky-parallel-thread-test ...}` and the paired `startup-command-delivery` row with `hasCommand=false` (tier1-observation.md O2 and the daemon.log capture from this run). Process 2935621 matches the PID the orchestrator named. The gap from create to tab is 2.3 seconds.
3. The same transcript shows the human-typed inputs the orchestrator listed: 20:32:38 "Pr 432 ci failure", 20:35:04 "Rerun", 20:35:23 "Then fix test", 20:37:11 "Commit and sc;pr-submit" (origin kind `human`).
4. CORRECTION to the orchestrator's third point. It says it created `install-core-stale-warning` at 06:15 with a bare create. Its 06:15:04 command (coordinator transcript 1779a921, tool call id toolu_01DBHStbNPUxVjsWmymPYkVH) FAILED before reaching `orca`: `cd: /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1: No such file or directory`, exit code 1, and the later commands in that chain never ran. The empty terminal in that worktree came from the 05:36:13Z bare create by session 7fd4f558 (the OrcaCLICommandRefactor-P1 session), with the daemon session at 05:36:16.234Z (tier1-observation.md O2).

## CLAIM (not independently verified here)
- The three terminals created 23:50 to 23:52 are UI-created because Orca tags them so; the orchestrator calls this its own inference. Consistent with my earlier finding that no `orca` Bash call in any active transcript fits the 23:52:18Z empty tab, but still not proven.
- The creator was released as a worker but its Claude session kept running and received human input (the transcript is consistent with human-origin inputs after the dispatch).

## What this changes
- Producer P1 (bare `orca worktree create`, no `--agent`) now has two observed agent-driven instances with the caller identified: session 7fd4f558 (05:36) and session 955b0bcc (20:35). Each is followed within about 3 seconds by one empty plain-shell tab and no Claude session. Neither used `orca terminal create`, and neither was an orchestrator waiting on a worker.
- The "empty terminals" half of the report is therefore supported by direct observation, not only by reading Orca source. It still does not show that an orchestrator chose "New Terminal" to start a Claude session.
- The "waiting orchestrator" half is still unobserved: neither instance had an orchestrator waiting on the empty tab.
- Tasklist row M-P1 moves from "true-case value observed on one worktree" to "observed on two worktrees, two callers named". Rows M-P3 (human keypress) and M-QE are unchanged for the reporter's case.
- Both bare creates ran in sessions whose loaded instructions had the repo CLAUDE.md bare example (line 308) and, on this host, lacked the #412 rule. That is consistent with the instruction-delivery cards but is an inference; the sessions' reasoning was not captured.

## Suggested next step
Re-run `/sc:troubleshoot` with this file passed through `--context` and `--fix`, scoped to the empty-terminals symptom. The earlier run stopped at partial for lack of an observed instance; this file supplies one.
