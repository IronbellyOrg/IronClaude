# /sc:recommend output for #606

- Recorded: 2026-11-18T04:40:00Z
- Goal sent: Pick the next-step chain for GitHub issue https://github.com/IronbellyOrg/IronClaude/issues/606. Type: feature. Complexity: complex. Summary: .dev/issues/606/issue-summary.md. Suggested route: the default row "Feature, complex" (brainstorm, design, workflow, implement), with the note that the issue body already carries a complete phased spec and prescribes /sc:workflow on it.

The block below is the skill's output, copied verbatim.

````text
Goal: Plan and implement observer visual parity (issue #606) from the phased spec that is already posted on the issue.

Level: 3 — guide section 1, 3.3, row `simple-plan` (row `feature-existing` also fits; the spec already exists, so the brainstorm and design steps of the suggested default row are not needed)

Changes files: /sc:workflow writes a plan package under .dev/tasks/to-do/<id>/; /sc:implement edits src/superclaude/cli/observe/, tests/observe/ and the spec files and writes a ledger; /sc:pr-submit pushes a branch and opens a PR on IronbellyOrg/IronClaude (external effect, only at the level that allows it).

Run these in order:

1. Assemble the spec from the issue comments into .dev/issues/409/visual-parity/REDESIGN-SPEC.md with the issue body's own gh + jq command (unless the file already exists on the branch); its sha256 must equal the one in the comment markers.
2. /sc:workflow @.dev/issues/409/visual-parity/REDESIGN-SPEC.md --depth standard --handoff none
3. Read the actual printed plan .dev/tasks/to-do/<id>/<id>.md and its advisory check result.
4. Only when execution is requested: /sc:implement <the plan path printed by step 2>
5. Rebase on origin/master, then, only when a PR is requested: /sc:pr-submit --monitor 3 --head <branch> --title "..." --body "..."

Notes:
- Standard depth and no executing handoff are the defaults of /sc:workflow; the issue itself asks for exactly these flags.
- An adequate approved plan goes directly to its executor; do not rebuild it. Resume with step 4, never task-builder.
- Phase 0 inputs (VP/inputs/tools/render_current.py, baseline captures) and the evidence trail are not on any branch; see the accuracy check.

Sources verified:
- src/superclaude/core/HOW-WE-WORK.md (routing table, row `simple-plan`)
- ~/.claude/commands/sc/workflow.md (--depth quick|standard|deep, --handoff none|design|implement|tasklist: Read)
- ~/.claude/commands/sc/implement.md (argument-hint: Read)
- ~/.claude/commands/sc/pr-submit.md (--monitor, --head, --title: Read)
- auggie semantic rank: skipped (matched row)
````
