## Claimed by @ironbelly

- **ClickUp:** skipped (no_token)
- **Accuracy check:** out_of_date (see the accuracy-check comment on this issue)

### Summary

The issue asks for an orchestrator session that every other session reports updates and questions through, with a periodic status report of all agents, sessions and worktrees, plus two new commands: `/sc:sweep` (find idle, stuck or timed-out sessions and resume or close them) and `/sc:close` (strictly checked worktree and branch removal). Comment 2 adds a security design for messages between sessions, and comment 3 sends the open questions to research and an adversarial debate. Much of the base model now exists as the Orca coordinator/worker contract, so the work is mostly extending it.

- **Effort estimate:** 40 hours
- **Complexity:** complex
- **Type:** feature
- **First next step:** `/sc:brainstorm "Orchestrator mode: run and manage all sessions within a worktree @.dev/issues/339/issue-summary.md" --depth deep --research deep --codebase --blind`

### Files

- Summary: `.dev/issues/339/issue-summary.md`
- Next steps: `.dev/issues/339/next-steps.md`
- Analysis: `.dev/issues/339/analysis/`

These links are paths in the repository; they open on GitHub only after someone commits and pushes the files.

<!-- sc:issue:claim -->
