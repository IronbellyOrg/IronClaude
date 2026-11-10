# /sc:recommend output for #450

- Recorded: 2026-11-08T23:58:00Z
- Goal sent: Pick the next-step chain for GitHub issue https://github.com/IronbellyOrg/IronClaude/issues/450. Type: feature. Complexity: complex. Summary: .dev/issues/450/issue-summary.md. Suggested route (default row "Feature, complex" of the /sc:issue chains): /model claude-gw-tier1a; 1. /sc:brainstorm ... --depth deep --research deep --codebase --blind; 2. /sc:design <brainstorm dir>/merged-requirements.md --type <...> --format spec; 3. /sc:workflow <design doc> --depth deep --handoff none; 4. /sc:implement <plan path>

The block below is the skill's output, copied verbatim.

````text
Goal: Turn the already-merged issue watcher (issue #450) into a safely running service: owner-run live test, shadow run, cron entry, and the two doc fixes.

Level: 3 (follow a checked implementation plan) — guide section 1, 3.3, row `simple-plan`

Changes files: yes. /sc:workflow writes a plan package under .dev/tasks/to-do/<id>/ and an advisory check result; /sc:implement (only when execution is requested) edits tests/issue_watch/fixtures, docs/designs/issue-watcher.md, docs/designs/issue-watcher-setup.md and may write docs/designs/issue-watcher-live-test.md, then archives the plan folder. The live test against real gh and Orca, the 24-hour shadow run, the lock and restart tests and the cron install are external, owner-run actions: they are not agent steps and no agent is authorized to run them.

Run these in order:

1. /sc:workflow "Roll out the issue watcher (issue #450, follow-up to #331): replace the _assumed_shape fixtures with captured real gh and Orca output after the owner-run live test (FU-1), fix the stale status line and the 59-name reason table in docs/designs/issue-watcher.md, prepare the shadow-run, lock, restart and cron steps (FU-2) as owner-run checklist items, keep enabled false until the owner flips it. Spec and runbook: docs/designs/issue-watcher.md, docs/designs/issue-watcher-setup.md. Code: src/superclaude/cli/issue_watch/, tests/issue_watch/. Summary: .dev/issues/450/issue-summary.md" --depth standard --handoff none
2. Read the actual printed plan .dev/tasks/to-do/<id>/<id>.md and its advisory check result.
3. Only when execution is requested: /sc:implement <actual printed plan path>

Notes:
- The default row (Feature, complex: brainstorm, design, deep workflow) was not used: the requirements are already fixed by the issue (FU-1, FU-2) and the design and runbook already exist, so a brainstorm and a new design add nothing (guide row `simple-plan`: ordinary checked planning, standard depth, no executing handoff).
- An adequate approved plan goes straight to its executor; do not rebuild it. Resume with step 3, never task-builder.
- Planning never authorizes execution, and implementation can never perform the owner-run live test or the cron install.
- Non-Linux managed archiving reports archive-blocked and keeps the plan folder in place.

Sources verified:
- /home/coder/workspaces/IronClaude/src/superclaude/core/HOW-WE-WORK.md (routing table, row `simple-plan`)
- /home/coder/.claude/commands/sc/workflow.md (Read; --depth standard and --handoff none declared)
- /home/coder/.claude/commands/sc/implement.md (Read; takes a plan path)
- /home/coder/.claude/skills/sc-workflow-protocol/SKILL.md and /home/coder/.claude/skills/sc-implement-protocol/SKILL.md (present)
- auggie semantic rank: skipped (matched row)
````
