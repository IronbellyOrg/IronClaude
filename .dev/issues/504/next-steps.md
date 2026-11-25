/model claude-gw-tier1a

# Next steps for #504

Plan boundary: after step 2

Run these in order, after the `/model` line. `/sc:issue` itself does not run them: you do after `--pipeline none`. Five sessions, one per area, in one worktree based on `origin/master`.

Command sessions (analyze, design, implement, workflow):

1. `/sc:design <that session's command file and backing skill> --type component --format spec`
   - Input: `@.dev/issues/504/issue-summary.md`
   - `/sc:design` has no `--depth` flag, so `--depth quick` is not used.
2. `/sc:workflow <design output printed by step 1> --depth quick --handoff none`
3. `/sc:implement <plan path printed by step 2>`

Agents session (ten general-purpose agent files):

1. `/sc:workflow "Add the one-line codegraph rule (use codegraph only when the caller passes index_state: fresh, otherwise Grep/Read) to the ten general-purpose agent files listed in @.dev/issues/504/issue-summary.md" --depth quick --handoff none`
2. `/sc:implement <plan path printed by step 1>`

- Effort estimate: 18 hours
- Default row not used: Feature, complex (brainstorm, design, workflow --depth deep, implement): you asked for per-file sessions with quick depth.
