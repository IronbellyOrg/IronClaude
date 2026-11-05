## Claimed by @ironbelly

- **ClickUp:** skipped (no_token)
- **Accuracy check:** out_of_date (see the accuracy-check comment on this issue)

### Summary

Agent-launched Claude sessions stop at ccsession's session-name question, or their first typed command is taken as the name. This claim covers the IronClaude part of the plan approved on 2026-11-04: one naming-question rule, an automatic unique name, a 30-second timer on every question, and Ctrl+C cancelling back to the shell, in `ccsession` and `ccsession-orca`, with tests. The Coder part (retiring the New Terminal hook, the `claude` wrapper handoff) is not part of this claim.

- **Effort estimate:** 24 hours
- **Complexity:** complex
- **Type:** bug
- **First next step:** `/sc:workflow "Fix GitHub issue #315, IronClaude part only ..." --depth standard --handoff none` (full command in `next-steps.md`)

### Files

- Summary: `.dev/issues/315/issue-summary.md`
- Next steps: `.dev/issues/315/next-steps.md`
- Analysis: `.dev/issues/315/analysis/`

These links are paths in the repository; they open on GitHub only after someone commits and pushes the files.

<!-- sc:issue:claim -->
