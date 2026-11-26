# Analyze report: src/superclaude/agents (focus architecture, depth quick)

Codegraph: index_state=fresh, checked_at=2026-11-24T20:40:56Z; degraded: graph:skipped (agents are .md files, not indexed symbols; Glob/Grep used)

## Facts (Grep/ls on this worktree, HEAD a7ae3dd30)
- src/superclaude/agents holds 51 entries: 49 agent .md files, README.md, __init__.py.
- 20 agent files have no `tools:` line (backend-architect, business-panel-experts, debate-orchestrator, devops-architect, frontend-architect, learning-guide, merge-executor, performance-engineer, pm-agent, python-expert, quality-engineer, refactoring-expert, repo-index, requirements-analyst, root-cause-analyst, security-engineer, self-review, socratic-mentor, system-architect, technical-writer). Matches the issue's "20".
- `memory: project` is on line 4 of 8 agents: rf-analyst, rf-assembler, rf-qa-qualitative, rf-qa, rf-task-builder, rf-task-executor, rf-task-researcher, rf-team-lead. The issue plans to delete it on six (all but rf-task-builder and rf-task-researcher). Not yet done.
- No agent file contains `disallowedTools` or `omitClaudeMd`. Not yet done.
- tests/agents has 3 files (test_codegraph_rosters.py, test_tavily_tool_parity.py, test_workflow_reviser_readonly.py); tests/agents/test_agent_frontmatter_policy.py does not exist.
- plugins/superclaude/agents mirror exists (23 entries).

## Findings
1. (Medium) Architecture: tool exposure is inconsistent. 20 agents inherit all tools, so they carry the Artifact trio; the rest use allowlists. A single table-driven frontmatter test is missing, so the policy is unpinned. Issue step 1 addresses this.
2. (Medium) `memory: project` on six rf agents that never write memory costs a large prompt block; not yet removed.
3. (Low) Two copies (src and plugins mirror) must be kept in step; issue step 2 says to mirror.

## Recommendation
Implement issue steps 1 and 2 first (tests, then frontmatter), as the issue states. No source modified by this run.
