## Claimed by @ironbelly

- **ClickUp:** skipped (no_token)
- **Accuracy check:** out_of_date (see the accuracy-check comment on this issue)

### Summary

The issue asks for an evaluation, not a build, of a sub-orchestrator or coordinator mode for the proposed `/sc:orchestrator`: a session that delegates to its own sessions inside a worktree while reporting to an orchestrator above. It is out of date in two ways: PR #449 already names "a coordinator under another orchestrator" in the installed rules without defining it, and the issue omits decision D5, which kept Orca nesting at depth 1 and rejected a design close to `--sub`. The evaluation has to start from rule WC-13, D5 and that undefined role.

- **Effort estimate:** 24 hours
- **Complexity:** complex
- **Type:** feature
- **First next step:** `/tech-research "Evaluate whether and how the proposed /sc:orchestrator should support a sub-orchestrator or coordinator mode ..."` (full command in `next-steps.md`; the chain stops at the research report)

### Files

- Summary: `.dev/issues/444/issue-summary.md`
- Next steps: `.dev/issues/444/next-steps.md`
- Analysis: `.dev/issues/444/analysis/`

These links are paths in the repository; they open on GitHub only after someone commits and pushes the files.

<!-- sc:issue:claim -->
