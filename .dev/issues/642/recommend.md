# /sc:recommend output for #642

- Recorded: 2026-11-18T18:58:00Z
- Goal sent: Pick the next-step chain for GitHub issue https://github.com/IronbellyOrg/IronClaude/issues/642. Type: feature. Complexity: simple. Summary: .dev/issues/642/issue-summary.md. Suggested route: default row "Feature, simple" (/sc:brainstorm, /sc:workflow, /sc:implement).

The block below is the skill's output, copied verbatim.

````text
Goal: Create the single file ob-442/T1.txt holding the line "ob-442 T1" and touch nothing else.

Level: 2 (make a small, direct change) - guide section 1, 3.3, row `small-change`

Changes files: yes (creates ob-442/T1.txt only)

Run these in order:

1. /sc:task "Create ob-442/T1.txt holding the single line ob-442 T1. Touch nothing else. Do not commit, push or merge." (a plain Write of the file is equally valid)
2. Inspect the recorded verification and confirm that the file holds exactly one line, "ob-442 T1", and that `git status` shows no other change. This is a text file, so no related test exists to run.

Notes:
- The default row (Feature, simple: brainstorm, workflow, implement) is not used. The issue names the file and its exact content, so it is one file and one edit, inside the level 2 limit. A written plan would add nothing.
- /sc:task has no matching-test step here: classification and manual verification of the one-line content are the evidence. Manual verification is not a test pass.

Sources verified:
- /home/coder/workspaces/IronClaude/src/superclaude/core/HOW-WE-WORK.md (routing table, row `small-change`)
- /home/coder/.claude/commands/sc/task.md (Read: `/sc:task [operation] [target] [flags]`)
- auggie semantic rank: skipped (matched row)
````
