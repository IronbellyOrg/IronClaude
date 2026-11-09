/model claude-gw-tier1a

# Next steps for #478

Run these in your own session, in order. `/sc:issue` does not run them.

1. `/sc:troubleshoot "BMAD and Ponytail are only accessible on projects where the user previously installed them, and are not installed by default or available globally to the user; BMAD used in a never-installed project should create the directories it needs" --fix --context .dev/issues/478/issue-summary.md --scope templates/VSCode-AIDev02/image`
   - Input: `@.dev/issues/478/issue-summary.md`
2. Read the `REPORT.md` that step 1 prints. If it is blocked or inconclusive, stop. If it is supported and you accept the planning offer: `/sc:workflow "<supported fix from REPORT.md>" --depth standard --handoff none`, then read the printed plan and its advisory check.
3. Only when execution is requested: `/sc:implement <plan path printed by step 2>`

- Effort estimate: 20 hours
- Default row not used: Bug, complex (`--depth deep --fix`, then `/task`). Deep with `--fix` selects the MDTM task-file route, which needs an explicit request or a stated machinery need; neither exists, so the standard-depth plan route applies (see `recommend.md`).
