# Wave 1.5 Branch B (architectural-doc lookup), returned by troubleshoot-analyst, persisted by parent on receipt 2026-11-08T01:55Z; currency finalized by parent

Parent currency check: `stat -c %Y` at 2026-11-08T01:55Z gave 1794083730 for all six docs and for the code surfaces (orca_worktree.py, ccsession-tag/README.md): checkout-time mtimes, all equal, so Step 1 = fresh (but this only proves no doc is staler than its checkout, not real review freshness). Step 2 markers: none, or "Status: Design only" (not deprecated/archived). Verdict: current for all six, with that caveat.

Worker summary: none of the docs says what happens to a new worktree's first terminal; the docs disagree on when to pass --agent (root CLAUDE.md: bare create, no session guidance; core CLAUDE.md: `worktree create --agent` for a new checkout; /sc:issue design: create without --agent, then `orca agent launch`). Degraded: auggie unavailable (Grep/Read only).

```json
[
  {"doc_path": "/home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/CLAUDE.md",
   "summary": "Every project worktree must be created through Orca with `orca worktree create --name <name>`, plus --repo, --base-branch and --parent-worktree/--no-parent as needed (CLAUDE.md:307-310). Example `orca worktree create --name pm-agent --base-branch origin/master` with no --agent (CLAUDE.md:320). Never says how to start a Claude session in the new worktree or what happens to its first terminal.",
   "currency_verdict": "current", "reason": "no markers found; mtime equal to code (checkout time)"},
  {"doc_path": "/home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/src/superclaude/core/CLAUDE.md",
   "summary": "'Orca session launches': for a new ccsession-backed Claude session choose Claude (CLI), never New Terminal (core/CLAUDE.md:47); 'Use `agent launch` in an existing worktree or `worktree create --agent` for a new checkout' with `--surface terminal` (48-50); `terminal create` is for shells only (50-51).",
   "currency_verdict": "current", "reason": "no markers found; mtime equal to code (checkout time)"},
  {"doc_path": "/home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/src/superclaude/core/WORKER-CONTRACT.md",
   "summary": "WC-13: a worker's top-level session never calls `worktree create --agent` or `agent launch` (WORKER-CONTRACT.md:62). Child worktrees come from `worker-start --worktree new-child --base-branch <feature branch>` (:88). One worker is a top-level Claude session in its own Orca terminal (:5).",
   "currency_verdict": "current", "reason": "no markers found; mtime equal to code (checkout time)"},
  {"doc_path": "/home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/docs/designs/sc-issue-claim-pipeline-flag.md",
   "summary": "/sc:issue claim creates with no --agent (line 184; D2 line 370) and starts the agent with `orca agent launch --agent claude --worktree path:<wt> --surface terminal` (line 211). P7: 'Never a plain terminal, and never --surface chat' (line 45). Does not mention the first terminal the create step leaves.",
   "currency_verdict": "current", "reason": "Status: Design only (nothing implemented). (line 3) -- not a stale marker"},
  {"doc_path": "/home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/docs/designs/sc-issue-command.md",
   "summary": "--claim creates or reuses an Orca worktree issue-<N> and launches an agent at the --pipeline level (line 13; B16 line 43); B17: agent starts behind the ccsession shim via `orca agent launch --surface terminal` (line 44).",
   "currency_verdict": "current", "reason": "Status: Design only (nothing implemented). (line 3) -- not a stale marker"},
  {"doc_path": "/home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/docs/user-guide/commands.md",
   "summary": "/sc:issue --claim creates or reuses worktree issue-<N> and launches one Claude Code agent in it (line 349). Nothing about --agent or terminals.",
   "currency_verdict": "current", "reason": "no markers found; mtime equal to code (checkout time)"}
]
```

Worker notes: docs/designs/sc-issue-launch-level-hook.md:349 is a near miss (pending record before agent launch). Developer guide section 7.7 searched only.
