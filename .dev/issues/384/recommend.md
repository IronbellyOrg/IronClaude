# /sc:recommend output for #384

- Recorded: 2026-11-05T03:45:00Z
- Goal sent: Pick the next-step chain for GitHub issue https://github.com/IronbellyOrg/IronClaude/issues/384. Type: feature. Complexity: complex. Summary: .dev/issues/384/issue-summary.md. Suggested route (default row "Feature, complex"): /model claude-gw-tier1a; 1. /sc:brainstorm ... --depth deep --research deep --codebase --blind --models opus,sonnet; 2. /sc:design ...; 3. /sc:workflow <design doc> --depth deep --handoff none; 4. /sc:implement <plan path>. Context: the coordinator's brief fixes level 3 (/sc:workflow standard, then /sc:implement); owner decisions are final.

The block below is the skill's output, copied verbatim.

````text
Goal: Plan and implement #384 (primitives select models through ccsession tier ids with a plain-name fallback) from the written issue and the owner decisions of 2026-11-05.

Level: 3 - guide section 1, 3.3, row `simple-plan`

Changes files: yes. `/sc:workflow` writes a plan folder under .dev/tasks/to-do/<id>/ and its advisory check result; `/sc:implement` edits source, tests and docs and updates progress.md. Neither pushes or opens a PR.

Run these in order:

1. /sc:workflow "Make primitives (agents, commands, skills) and the Python package select models through ccsession tier ids inside a ccsession workspace and fall back to plain opus, sonnet, haiku outside one. Owner decisions (final): inside a ccsession workspace opus = tier1a (claude-gw-tier1a), sonnet = tier1b (claude-gw-tier1b), haiku = tier2 (claude-gw-tier2); outside: opus, sonnet, haiku; Python package code is in scope (cli/roadmap/models.py, cli/roadmap/executor.py, cli/recommend/eval_aggregate.py, cli/reflect/runner.py, cli/sprint/summarizer.py and every other hard-coded alias a grep finds). Settle the mechanism for a per-environment frontmatter model: field with evidence first. Read-only: skills/ccsession-tag/ and ccsession-orca. Files and evidence: @.dev/issues/384/issue-summary.md and @.dev/issues/384/analysis/analyze-superclaude.md" --depth standard --handoff none
2. Read the plan at the path step 1 prints (.dev/tasks/to-do/<id>/<id>.md) and its advisory check result.
3. Only when execution is requested: /sc:implement <the plan path printed by step 1>

Notes:
- Standard depth and no executing handoff are the defaults for this row.
- An approved plan goes directly to /sc:implement; do not rebuild it.
- No brainstorm step: the open decisions (mapping, fallback, Python scope) were settled by the owner's two comments on the issue.

Sources verified:
- src/superclaude/core/HOW-WE-WORK.md (routing table, row `simple-plan`)
- src/superclaude/commands/workflow.md and ~/.claude/commands/sc/workflow.md (--depth, --handoff verified)
- src/superclaude/commands/implement.md and ~/.claude/commands/sc/implement.md (Read)
- ~/.claude/skills/sc-workflow-protocol/SKILL.md, ~/.claude/skills/sc-implement-protocol/SKILL.md (present)
- auggie semantic rank: skipped (matched row)
````
