/model claude-gw-tier2

# Next steps for #645

Plan boundary: before step 1

Run these in order, after the `/model` line. `/sc:issue` itself does not run them: after `--pipeline none` you run them in your own session.

1. Write the file `ob-442/T4.txt` (native Write tool, no command) holding the single line `ob-442 T4`. Touch nothing else.
   - Input: `@.dev/issues/645/issue-summary.md`
2. Read the file back and check it holds exactly that one line. Do not commit, push or merge: the issue says to close it without merging anything.

- Effort estimate: 0.25 hours
- Default row not used: Feature, simple (the /sc:brainstorm, /sc:workflow, /sc:implement chain; /sc:recommend chose a direct edit because the change is one new one-line file, within the guide's level-2 limit).
