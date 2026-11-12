/model claude-gw-tier2

# Next steps for #452

Plan boundary: after step 2

Run these in order, after the `/model` line. `/sc:issue` itself does not run them: the agent it launches does (up to the plan boundary at the default level), or you do after `--pipeline none`.

Note: issue #452 is a throwaway live-check issue and says "Do not work on this issue". The default chain below is written for form only; do not run it.

1. `/sc:brainstorm "[TEST] throwaway issue for /sc:issue --claim live check @.dev/issues/452/issue-summary.md" --depth quick`
   - Input: `@.dev/issues/452/issue-summary.md`
2. `/sc:workflow <brainstorm dir>/merged-requirements.md --depth quick --handoff none`
3. `/sc:implement <plan path printed by step 2>`

- Effort estimate: 0.5 hours
- Default row not used: none (`/sc:recommend` found no route, so the default Feature, simple row is kept).
