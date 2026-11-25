/model claude-gw-tier2

# Next steps for #714

Plan boundary: after step 2 (the chain has no /sc:implement or /task step)

Run these in order, after the `/model` line. `/sc:issue` itself does not run them: you do, after `--pipeline none`.

1. Plain edit: create `ob-442/T3.txt` holding the single line `ob-442 T3`. Touch nothing else.
   - Input: `@.dev/issues/714/issue-summary.md`
2. Check the result: `git status` shows only `ob-442/T3.txt`, and the file holds exactly that one line (manual check; there is no test for it).

- Effort estimate: 0.1 hours
- Default row not used: Feature, simple (/sc:recommend chose the guide's `small-change` route: one new file, one edit, so a plan and /sc:implement would cost more than the change).
