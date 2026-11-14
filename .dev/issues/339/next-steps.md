/model claude-gw-tier1a

# Next steps for #339

Run these in your own session, in order. `/sc:issue` does not run them.

1. `/sc:brainstorm "Orchestrator mode: run and manage all sessions within a worktree @.dev/issues/339/issue-summary.md" --depth deep --research deep --codebase --blind`
   - Input: `@.dev/issues/339/issue-summary.md`
2. `/sc:spec-panel @<brainstorm folder printed by step 1>/merged-requirements.md --mode critique --focus requirements,architecture`, then revise that spec from the panel's findings.
3. `/sc:design <revised spec from step 2> --type architecture --format spec --output docs/designs/orchestrator-mode.md`
4. `/task-builder "Build the task list for the orchestrator mode design at docs/designs/orchestrator-mode.md" --spec docs/designs/orchestrator-mode.md`
5. `/task <task file path printed by step 4>`
6. `/sc:pr-submit --monitor 3 --head ironbelly/issue-339-orchestrator-mode --title "<title>" --body "<body naming #339>"`

- Effort estimate: 40 hours
- Default row not used: Feature, complex (the owner directly instructed this chain on 2026-11-07: a deep brainstorm, a spec panel review, a design, then the task-file builder and executor, then `/sc:pr-submit --monitor 3`; `/sc:recommend` proposed `/sc:workflow` and `/sc:implement` in place of steps 4 and 5).
