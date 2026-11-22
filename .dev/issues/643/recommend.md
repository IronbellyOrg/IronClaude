# /sc:recommend output for #643

- Recorded: 2026-11-18T17:10:00Z
- Goal sent: Pick the next-step chain for GitHub issue https://github.com/IronbellyOrg/IronClaude/issues/643. Type: feature. Complexity: simple. Summary: .dev/issues/643/issue-summary.md. Suggested route: default row "Feature, simple" (brainstorm, workflow, implement).

The block below is the skill's output, copied verbatim.

````text
Goal: Create the one-line file ob-442/T2.txt (content: ob-442 T2) for the #442 disposable observation, touch nothing else.

Level: 2 (make a small, direct change) - guide section 1, 3.3, row `small-change`

Changes files: yes - creates one new file, ob-442/T2.txt. Verification evidence is recorded by /sc:implement; no related test exists for this file.

Run these in order:

1. /sc:implement "Create the single file ob-442/T2.txt containing exactly the one line `ob-442 T2`. Touch nothing else. Source: @.dev/issues/643/issue-summary.md"
2. inspect the recorded verification (the file exists and holds exactly that line); no related test applies.

Notes:
- The default row (Feature, simple: brainstorm, workflow, implement) was not used: the whole job is one new file with one known line, inside the guide's level-2 limit (one file, five edits or fewer). A written plan would cost more than the change.
- The issue says to close it without merging anything; closing is a person's step, not part of the chain.

Sources verified:
- ~/.claude/HOW-WE-WORK.md (routing table, row `small-change`; level table)
- ~/.claude/commands/sc/implement.md (Read; accepts `/sc:implement <prompt>`)
- auggie semantic rank: skipped (matched row)
````
