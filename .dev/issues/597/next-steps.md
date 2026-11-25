/model claude-gw-tier2

# Next steps for #597

Plan boundary: after step 2
Stage: debug
Level: none

Run these in order, after the `/model` line (use claude-gw-tier2 for simple work). `/sc:issue` itself does not run them: you do, after `--pipeline none`.

1. `/sc:troubleshoot "Research questions skip the Context7 and Tavily MCP tools: the orchestrator delegates to an agent without them (claude-code-guide) instead of doing the lookup itself; expected Context7 for docs, Tavily for web, or a delegate that has those tools" --type bug --depth quick --context .dev/issues/597/issue-summary.md --scope src/superclaude/core`
   - Input: `@.dev/issues/597/issue-summary.md`
   - Then read the `REPORT.md` it prints and keep its status and blockers. Diagnosis alone stops here; no `--fix` (level none, and `--depth quick` with `--fix` is refused).
2. Only if the report confirms a supported fix: `/sc:workflow "<the supported fix from REPORT.md, with a reproducing test>"`
3. `/sc:implement <plan path printed by step 2>`

- Last step of the launched agent, when one is used: write `.dev/issues/597/result.md` (`outcome`, `artifacts`, `pull_request`).
- Effort estimate: 3 hours
- Default row not used: Bug, simple (the guide's bug row plans with /sc:workflow before /sc:implement).
