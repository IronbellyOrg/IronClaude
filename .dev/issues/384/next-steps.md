/model claude-gw-tier1a

# Next steps for #384

Run these in your own session, in order. `/sc:issue` does not run them.

1. `/sc:workflow "Make primitives (agents, commands, skills) and the Python package select models through ccsession tier ids inside a ccsession workspace and fall back to plain opus, sonnet, haiku outside one. Owner decisions (final): inside a ccsession workspace opus = tier1a (claude-gw-tier1a), sonnet = tier1b (claude-gw-tier1b), haiku = tier2 (claude-gw-tier2); outside: opus, sonnet, haiku; Python package code is in scope (cli/roadmap/models.py, cli/roadmap/executor.py, cli/recommend/eval_aggregate.py, cli/reflect/runner.py, cli/sprint/summarizer.py and every other hard-coded alias a grep finds). Settle the mechanism for a per-environment frontmatter model: field with evidence first. Read-only: skills/ccsession-tag/ and ccsession-orca. Files and evidence: @.dev/issues/384/issue-summary.md and @.dev/issues/384/analysis/analyze-superclaude.md" --depth standard --handoff none`
   - Input: `@.dev/issues/384/issue-summary.md`
2. Read the plan path printed by step 1 (`.dev/tasks/to-do/<id>/<id>.md`) and its advisory check result, then run `/sc:implement <the plan path printed by step 1>`

- Effort estimate: 40 hours
- Default row not used: Feature, complex (brainstorm, then design, then workflow --depth deep). The owner settled the mapping, the fallback and the Python scope in the issue comments, so `/sc:recommend` chose the level-3 route (`simple-plan`): workflow at standard depth, then implement.
