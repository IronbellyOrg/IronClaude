/model claude-gw-tier2

# Next steps for #594

Plan boundary: before step 1

Run these in order, after the `/model` line. `/sc:issue` itself does not run them: you do, in your own session (this claim used `--pipeline none`).

1. Create `ob-442/T2.txt` at the repository root with the Write tool, holding exactly one line: `ob-442 T2`
   - Input: `@.dev/issues/594/issue-summary.md`
2. Read the file back, and run `git status --short` to confirm that `ob-442/T2.txt` is the only change (ignore the existing untracked `.dev/` folders). Do not merge anything; close the issue without merging, as the issue says.

- Effort estimate: 0.25 hours
- Default row not used: Feature, simple (the brainstorm, workflow and implement chain would plan a one-line file; `/sc:recommend` chose native tools under level 2).
