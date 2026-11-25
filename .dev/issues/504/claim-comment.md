## Claimed by @ironbelly

- **ClickUp:** skipped (no_token)
- **Accuracy check:** current (see the accuracy-check comment on this issue)

### Summary

Add one codegraph readiness check to `/sc:analyze`, `/sc:design`, `/sc:implement` and `/sc:workflow` (in the command file, and in the backing skill for implement and workflow), using codegraph above the Grep/Read floor when the index is fresh and falling back to Grep/Read with a note otherwise. Ten general-purpose agent files also get the one-line rule "use codegraph only when the caller passes `index_state: fresh`". Work is in `src/superclaude/`, then `make sync-dev` and `make verify-sync`.

- **Effort estimate:** 18 hours
- **Complexity:** complex
- **Type:** feature
- **First next step:** `/sc:design <command file and backing skill> --type component --format spec`

### Files

- Summary: `.dev/issues/504/issue-summary.md`
- Next steps: `.dev/issues/504/next-steps.md`
- Analysis: `.dev/issues/504/analysis/`

These links are paths in the repository; they open on GitHub only after someone commits and pushes the files.

<!-- sc:issue:claim -->
