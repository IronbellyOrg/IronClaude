/model claude-gw-tier2

# Next steps for #642

Plan boundary: before step 1

Run these in order, after the `/model` line. `/sc:issue` itself does not run them: the launched agent does, at the level `--pipeline` names. (The first step is itself the change step, so there is no plan to stop at.)

1. `/sc:task "Create ob-442/T1.txt holding the single line ob-442 T1. Touch nothing else. Do not commit, push or merge."`
   - Input: `@.dev/issues/642/issue-summary.md`
2. Check that `ob-442/T1.txt` holds exactly one line, `ob-442 T1`, and that `git status` shows no other change. Then close the issue without merging anything, as the issue says.

- Effort estimate: 0.25 hours
- Default row not used: Feature, simple (brainstorm, workflow, implement). The issue names the one file and its exact content, so this is a level 2 direct change.
