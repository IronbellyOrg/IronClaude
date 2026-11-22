/model claude-gw-tier2

# Next steps for #713

Plan boundary: before step 1

Run these in order, after the `/model` line. `/sc:issue` itself does not run them: you do, after `--pipeline none`.

1. `/sc:implement "Create the file ob-442/T2.txt at the repository root holding the single line: ob-442 T2. Touch nothing else. Do not commit or push. Source: .dev/issues/713/issue-summary.md"`
   - Input: `@.dev/issues/713/issue-summary.md`
2. Inspect the recorded verification: `ob-442/T2.txt` exists and holds exactly one line, `ob-442 T2`. No test applies.

- Effort estimate: 0.1 hours
- Default row not used: feature, simple (`/sc:workflow --depth quick` then `/sc:implement`): the change is one new file with one line, within the direct-change limit, so a written plan adds nothing.
