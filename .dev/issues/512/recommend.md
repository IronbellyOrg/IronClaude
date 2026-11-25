# /sc:recommend output for #512

- Recorded: 2026-11-12T02:20:00Z
- Goal sent: Pick the next-step chain for GitHub issue #512. Type: feature. Complexity: complex (12 hours; Complexity field Medium). The issue already holds exact edit specs E1-E9, so brainstorm and design are redundant; the similar issue #504 went workflow then implement.

The block below is the skill's output, copied verbatim.

````text
Goal: apply the nine reviewed MCP edits (E1-E9) of issue #512 across about 11 source files and their pinned tests.

Level: 3 (follow a checked implementation plan) - guide section 3.2, row `feature-existing` (plan via `simple-plan`, section 3.3). guide_status: matched. The brainstorm and design steps of the default "Feature, complex" row are skipped: requirements and exact edits already exist in the issue.

Changes files: yes. /sc:workflow writes one new package under .dev/tasks/to-do/<id>/; /sc:implement edits src/superclaude files, their tests, then make sync-dev (not staged).

Run these in order:

1. /sc:workflow "Apply the nine MCP edits E1-E9 of GitHub issue 512 exactly as specified in @.dev/issues/512/issue-summary.md and the issue body; correct the audit bookkeeping noted in @.dev/issues/512/accuracy-check.md first; include the pinned tests and sync-dev" --depth standard --handoff none
2. read the actual printed plan .dev/tasks/to-do/<id>/<id>.md and its advisory check result
3. only when execution is requested: /sc:implement <the exact plan path printed by step 1>

Notes:
- Default row not used: Feature, complex (brainstorm, design, workflow --depth deep, implement): the issue holds exact edit specs and the owner pointed to the #504 pattern.
- The edits are independent per file; /sc:implement runs them in one session, or split the plan by area into parallel sessions in one worktree as done for #504.
- Pins to respect (from the accuracy check): the em dash in "Only PASS or FAIL — no conditional pass.", the capital `Tools:` line, and the exact tool-list pins in tests/ and scripts/.
- The accuracy check found 4 wording and bookkeeping errors in the issue (30 items not 31, 21 unchanged not 20, document is the one empty field that changes, two follow-up anchors are not web-agent blocks); the plan must use the corrected values.

Sources verified:
- ~/.claude/HOW-WE-WORK.md (routing table, rows `feature-existing`, `simple-plan`)
- ~/.claude/commands/sc/workflow.md (--depth quick|standard|deep, --handoff none|design|implement|tasklist)
- ~/.claude/commands/sc/implement.md (<path-or-prompt>)
- auggie semantic rank: skipped (matched row)
````
