Repo: IronbellyOrg/IronFlow. Context: IronClaude (issue IronbellyOrg/IronClaude#323) removed the Serena and codebase-memory MCP servers.
Do:
1. .claude/commands/sc/reflect.md and .claude/skills/sc-reflect-protocol/SKILL.md are copies of IronClaude's /sc:reflect; refresh them from the IronClaude release that contains the removal rather than hand-editing. If they are local forks, replace the Serena symbol and memory steps together (symbol steps -> Grep plus Read; memory -> .superclaude/memory/, reflect calibration -> docs/memory/reflect/).
2. Remove mcp__serena__* entries from .claude/settings.json.
3. Delete .serena/project.yml; move any .serena/memories/ files to .superclaude/memory/ (reflect calibration files to docs/memory/reflect/).
Keep: the 39 historical paths (.dev/, claudedocs/ and recorded logs).
Verify: `git grep -n -i -E 'serena|codebase-memory' -- . ':!.dev' ':!claudedocs'` returns only intentional history.
