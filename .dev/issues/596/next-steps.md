/model claude-gw-tier2

# Next steps for #596

Plan boundary: before step 1

Run these in order, after the `/model` line. `/sc:issue` itself does not run them: the agent it launches does (up to the plan boundary at the default level), or you do after `--pipeline none`.

1. Use the Write tool to create `ob-442/T4.txt` under the repository root with exactly one line: `ob-442 T4`. (Same effect: `/sc:task "Create ob-442/T4.txt containing the single line: ob-442 T4. Touch nothing else."`)
   - Input: `@.dev/issues/596/issue-summary.md`
2. Read `ob-442/T4.txt` and run `git status --short` to confirm only that file is new. Do not stage or commit `.dev/issues/`; do not merge anything.

- Effort estimate: 0.25 hours
- Default row not used: feature, simple (brainstorm, workflow, implement). `/sc:recommend` chose the direct-change route because the change is one file and one line.
