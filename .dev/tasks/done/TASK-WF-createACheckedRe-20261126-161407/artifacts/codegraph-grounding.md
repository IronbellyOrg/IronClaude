# Workflow code grounding

## Run state
index_state: fresh
checked_at: 2026-11-26T16:14:43Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-540-resume-marker
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-540-resume-marker
access: mcp
Baseline: a98d7b4280363f2bb506d7af5fb4eb1551953c41. No readiness repeat is needed.

## Resolved symbols
Read commands.py:1640-1719,1720-1859,1860-2004,2531-3009; models.py:1180-1204; preflight.py:1914-1993; commands.py:3897-3973. run_cmd calls _run_resume_branch at1688 (resolution: call-site-verified, 1/1 shown). Resume validates manifest identity, relens, inventory, provider input/checksum and transport before dispatch2802. Reduction-only skips remaining_indices branch and reaches reduce2942. No accepted-attempt marker retirement exists. Publication order2942/2962/2967 must stay contract, terminal, optional marker.

Ownership search: Grep lock/owner/flock/pid in swarm locates only logger's thread lock, not run ownership; exact repo search for flock/FileLock/active outputs/pidfile finds issue_watch loop_lock at dispatch.py:157-175. Read that context: it is tied to issue-watch Base state, not reusable by import as swarm output ownership. SwarmState fields1195-1197 contain no live owner. dispatching is explicitly crash-persistent at commands1935-1943. A phase-value guard is invalid. No two-process race was observed. Select a narrow process-local, non-reentrant active-output claim for the observed nested overlap, not the old unapproved file-lock design; cross-process ownership remains outside the guarantee and must not be represented as solved. An atomic thread-safe claim covers nested calls and TUI threads in this process; no persistent owner metadata is needed for recovery.

Four systematic phases: capture red regression (retained diagnosis and current tests -> new failing tests/log; checkpoint observed failures before product edit); bounded lifecycle repair (current run/resume -> claim and acceptance retirement; checkpoint both work/reduction entries safe); complete safety matrix (repair -> rejection/error/recovery cases; checkpoint related suites); executable real-boundary witness (matrix -> local stub harness and independent review artifact; checkpoint old hardening proof requirements explicitly resolved or remain blocked). Dependencies are sequential.

## Dependents
Graph direct caller run_cmd confirmed at commands.py1688-1693; fresh call sites dispatch_wave1 at1973 and1998 read, resume dispatch2802 and reduce2942 read. Graph impact:2 symbols (_run_resume_branch, run_cmd). Callees capped20/29, not an exhaustive dependency inventory (graph:truncated); source floor read complete resume body2531-2978. Existing tests read at test_resume_crash_recovery.py604-729 (fresh-marker absence/order, injected terminal persistence failure). Grep names confirms all-workers-success at395, unsafe inventory550. Baseline-tests.log7-14 records the historical 121 tests in resume_crash_recovery, commands_run, kill_cmd and imm6_atomic_write. Glob confirms done_sentinel, resume_context, resume_regenerates_merge, resume_uses_manifest_lens and tmux_detached sibling files exist. These are test dependents, not graph call-site claims.

## Pre-check
Full structural gate observed PASS (4 phases/4 tasks). All named delivery files exist; check_resume_boundary.py and other task-owned artifacts are proposed outputs, not existing sources. Confirmed changed symbols run_cmd and _run_resume_branch; guard helper explicitly new/proposed. Dependent sources read cover fresh/TUI dispatch, zero-remaining reduction, marker-order and kill preservation. Related regression files inventoried, not claimed executed. 4 tasks grounded, 0 nonexistent production symbols, 0 known unnamed directly changed dependents. Graph callee truncation is covered by full resume-body floor; broader test callers are not claimed exhaustive. Native freshness hook initially refused an Edit of this freshly written note; Read then Edit recovered without bypass. No production edits or tests executed in this planning run.
