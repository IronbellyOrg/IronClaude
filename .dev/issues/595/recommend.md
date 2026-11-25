# /sc:recommend output for #595

- Recorded: 2026-11-17T16:30:00+00:00
- Goal sent: Pick the next-step chain for GitHub issue https://github.com/IronbellyOrg/IronClaude/issues/595. Type: feature. Complexity: simple. Summary: .dev/issues/595/issue-summary.md. Suggested route: default row "Feature, simple" (brainstorm quick, workflow quick, implement).

The block below is the skill's output, copied verbatim.

````text
Goal: Create ob-442/T3.txt holding the single line "ob-442 T3" and touch nothing else (issue #595).

Level: 2 (a small, direct change) — guide section 1, 3.3, row `small-change`

Changes files: yes, one new file: ob-442/T3.txt (the new ob-442/ folder holds only that file).

Run these in order:

1. `/sc:task "Create the file ob-442/T3.txt containing the single line: ob-442 T3. Change nothing else."` (or make the same edit directly with Write)
2. Inspect the recorded verification evidence: read ob-442/T3.txt back, and run `git status --short` to confirm that only ob-442/T3.txt changed. No related test exists for a text file.

Notes:
- One new file, one edit: well under the five-edit limit, so no written plan is needed. The default row (brainstorm, workflow, implement) is heavier than the work needs.
- The issue says to close without merging anything; nothing here commits, pushes or merges.

Sources verified:
- src/superclaude/core/HOW-WE-WORK.md (routing table, row `small-change`; level table)
- /home/coder/.claude/commands/sc/task.md (exists)
- auggie semantic rank: skipped (matched row)
````

guide_status: matched; routing_row_id: small-change
