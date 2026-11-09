## Claimed by @ironbelly

- **ClickUp:** skipped (no_token)
- **Accuracy check:** current (see the accuracy-check comment on this issue)

### Summary

BMAD and Ponytail should be available to the user in every project by default, not only where they were installed before. When BMAD is used in a project that never had it, it should create the directories it needs. The image installs only the BMAD command-line tool globally; project setup runs only for the recorded seed repo, and how Ponytail is installed is unverified in this repo.

- **Effort estimate:** 20 hours
- **Complexity:** complex
- **Type:** bug
- **First next step:** `/sc:troubleshoot "BMAD and Ponytail are only accessible on projects where the user previously installed them, and are not installed by default or available globally to the user; BMAD used in a never-installed project should create the directories it needs" --fix --context .dev/issues/478/issue-summary.md --scope templates/VSCode-AIDev02/image`

### Files

- Summary: `.dev/issues/478/issue-summary.md`
- Next steps: `.dev/issues/478/next-steps.md`
- Analysis: `.dev/issues/478/analysis/`

These links are paths in the repository; they open on GitHub only after someone commits and pushes the files.

<!-- sc:issue:claim -->
