## Claimed by @ironbelly

- **ClickUp:** skipped (no_token)
- **Accuracy check:** current (see the accuracy-check comment on this issue)

### Summary

The issue watcher (`superclaude issue-watch`) is merged but has never run live, has no schedule and ships with `enabled: false`. This issue asks to turn it on safely: an owner-run live test that replaces the guessed fixtures with captured gh and Orca output, a reviewed 24-hour shadow run with the lock and restart tests, then the cron entry, plus two doc fixes (the stale status line and the 59-name reason table).

- **Effort estimate:** 20 hours
- **Complexity:** complex
- **Type:** feature
- **First next step:** `/sc:workflow "Roll out the issue watcher (issue #450, follow-up to #331): replace the _assumed_shape fixtures with captured real gh and Orca output after the owner-run live test (FU-1), fix the stale status line and the 59-name reason table in docs/designs/issue-watcher.md, prepare the shadow-run, lock, restart and cron steps (FU-2) as owner-run checklist items, keep enabled false until the owner flips it. Spec and runbook: docs/designs/issue-watcher.md, docs/designs/issue-watcher-setup.md. Code: src/superclaude/cli/issue_watch/, tests/issue_watch/" --depth standard --handoff none`

### Files

- Summary: `.dev/issues/450/issue-summary.md`
- Next steps: `.dev/issues/450/next-steps.md`
- Analysis: `.dev/issues/450/analysis/`

These links are paths in the repository; they open on GitHub only after someone commits and pushes the files.

<!-- sc:issue:claim -->
