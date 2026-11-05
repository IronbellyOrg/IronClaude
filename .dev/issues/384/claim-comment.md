## Claimed by @ironbelly

- **ClickUp:** skipped (no_token)
- **Accuracy check:** out_of_date (see the accuracy-check comment on this issue)

### Summary

Agents, commands, skills and the Python package should stop relying on Claude Code's plain `opus`, `sonnet` and `haiku` aliases. Inside a ccsession tier workspace they should resolve to `claude-gw-tier1a`, `claude-gw-tier1b` and `claude-gw-tier2`; outside one they keep the plain names. The owner's comments of 2026-11-05 settled the mapping, the fallback and the Python scope; the remaining design question is how a static agent frontmatter `model:` can differ per environment.

- **Effort estimate:** 40 hours
- **Complexity:** complex
- **Type:** feature
- **First next step:** `/sc:workflow "<what to change, why, which files, owner decisions>" --depth standard --handoff none`

### Files

- Summary: `.dev/issues/384/issue-summary.md`
- Next steps: `.dev/issues/384/next-steps.md`
- Analysis: `.dev/issues/384/analysis/`

These links are paths in the repository; they open on GitHub only after someone commits and pushes the files.

<!-- sc:issue:claim -->
