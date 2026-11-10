# /sc:recommend output for #478

- Recorded: 2026-11-07T07:29:00+00:00
- Goal sent: Pick the next-step chain for GitHub issue https://github.com/IronbellyOrg/Coder/issues/478. Type: bug. Complexity: complex. Summary: .dev/issues/478/issue-summary.md. Suggested route (default row "Bug, complex"): /model claude-gw-tier1a; 1. /sc:troubleshoot "<symptom>" --depth deep --fix --context .dev/issues/478/issue-summary.md --scope templates/VSCode-AIDev02/image; 2. /task <task file path printed by step 1>

The block below is the skill's output, copied verbatim.

````text
Goal: Diagnose issue #478 (BMAD and Ponytail only available where previously installed; not global by default) and, if the diagnosis is supported, get an ordinary checked fix plan.

Level: not on the six-level scale (diagnosis, then level 3 planning if accepted) - guide section 3.4, row `bug`

Changes files: step 1 writes a report under .dev/troubleshoot/<name>-<timestamp>/ and nothing else; accepting its planning offer writes a plan package under .dev/tasks/to-do/<id>/. No product code changes; no execution.

Run these in order:

1. /sc:troubleshoot "BMAD and Ponytail are only accessible on projects where the user previously installed them, and are not installed by default or available globally to the user; BMAD used in a never-installed project should create the directories it needs" --fix --context .dev/issues/478/issue-summary.md --scope templates/VSCode-AIDev02/image
2. Read .dev/troubleshoot/<name>-<timestamp>/REPORT.md (path printed by step 1) and keep its status and blockers. If it is blocked or inconclusive, stop here; no speculative fix.
3b. Only if the report is supported and you accept the planning offer: /sc:workflow "<supported fix from REPORT.md>" --depth standard --handoff none, then read the printed plan (.dev/tasks/to-do/<id>/<id>.md) and its advisory check result.
4. Only when execution is requested: /sc:implement <printed plan path>

Notes:
- Default row not used: "Bug, complex" (--depth deep --fix, then /task). Deep plus --fix couples to the MDTM task-file route, and the guide allows MDTM only on explicit request or a stated machinery need; neither is present, so the ordinary standard-depth plan route applies. Complexity is "complex" by the issue rubric (two subsystems), which alone does not select MDTM.
- Do not add --depth quick with --fix (invalid).
- Planning never authorizes execution; step 4 is a separate decision.

Sources verified:
- /home/coder/.claude/HOW-WE-WORK.md (routing table, row `bug`)
- /home/coder/.claude/commands/sc/troubleshoot.md (Read; --fix, --context, --scope, --depth verified)
- /home/coder/.claude/commands/sc/workflow.md (Read; --depth, --handoff verified)
- /home/coder/.claude/commands/sc/implement.md (argument-hint verified)
- auggie semantic rank: skipped (matched row)
````
