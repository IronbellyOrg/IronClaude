# /sc:recommend output for #611

- Recorded: 2026-11-26T14:01:00+00:00
- Goal sent: Pick the next-step chain for GitHub issue https://github.com/IronbellyOrg/IronClaude/issues/611. Type: feature. Complexity: medium. Summary: .dev/issues/611/issue-summary.md. Suggested route: default row "Feature, medium" (`/sc:brainstorm --blind`, `/sc:design`, `/sc:workflow --depth standard --handoff none`, `/sc:implement`).

The block below is the skill's output, copied verbatim.

````text
Goal: Plan and run the Jev-versus-keyword-table comparison on about 30 labelled prompts (issue 611, feature, medium).

Level: 3 (checked implementation plan) — guide section 3.2 and 3.3, routing rows `shape-idea` then `feature-existing` / `simple-plan`

Changes files: yes. brainstorm writes merged-requirements.md under its output folder; design writes a design document; workflow writes .dev/tasks/to-do/<id>/; implement writes the labelled corpus and result record under .dev/. No source file under src/ needs to change.

Run these in order, after `/model claude-gw-tier1b`:

1. /sc:brainstorm "Jev preflight step 2: compare Jev against the keyword table on about 30 labelled prompts @.dev/issues/611/issue-summary.md" --blind
2. /sc:design <brainstorm dir>/merged-requirements.md --type architecture --format spec
3. /sc:workflow <design doc> --depth standard --handoff none
4. /sc:implement <plan path printed by step 3>

Notes:
- Stop after step 3 to read the printed plan and its advisory check; run step 4 only when execution is requested.
- The owner's margin, acceptable median latency, spend cap and approval to send public prompts to TypeSafe must be fixed before any live call. They are an input to step 1, not something a step may invent.

Sources verified:
- src/superclaude/core/HOW-WE-WORK.md (routing table, rows `shape-idea`, `feature-existing`, `simple-plan`)
- src/superclaude/commands/brainstorm.md (`--blind` declared; merged-requirements.md named as output)
- src/superclaude/commands/design.md (usage line: `--type architecture|api|component|database`, `--format diagram|spec|code`)
- src/superclaude/commands/workflow.md (argument-hint: `--depth quick|standard|deep`, `--handoff none|design|implement`)
- src/superclaude/commands/implement.md (argument-hint: `<path-or-prompt>`)
- installed copies of the four commands and the brainstorm, workflow and implement skills exist under ~/.claude/
- auggie semantic rank: skipped (matched row)
````

Recorder's note: the chain matches the default row, so `next-steps.md` carries no "Default row not used" line. The step 2 `--type` value (`architecture`) was chosen here from the four values the command accepts. Step C was a read of each command's usage line and a file-exists check on the installed copies; the backing skills were not read line by line.
