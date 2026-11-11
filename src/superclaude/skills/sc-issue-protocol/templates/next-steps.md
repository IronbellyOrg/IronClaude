/model <claude-gw-tier2 for simple work | claude-gw-tier1b for medium and complex work; use claude-gw-tier2 when tier1b is not in your /model list>

# Next steps for #<N>

Plan boundary: after step <K>

Run these in order, after the `/model` line. `/sc:issue` itself does not run them: the agent it launches does (up to the plan boundary at the default level), or you do after `--pipeline none`.

1. `<command with its flags>`
   - Input: `@.dev/issues/<N>/issue-summary.md`
2. `<command with its flags, using the path printed by step 1>`

- Effort estimate: <hours> hours
- <Only when `/sc:recommend` chose a different route: "Default row not used: <type, complexity> (<reason>).">
