Repo: IronbellyOrg/IronOps. Context: IronClaude (issue IronbellyOrg/IronClaude#323) removed the Serena and codebase-memory MCP servers.
Do:
1. src/ironops/skills/ironops-troubleshoot-protocol/SKILL.md is owned distributable source: remove mcp__serena__* from its allowed-tools and rewrite its Serena symbol steps to Grep for the definition plus Read of the range (auggie first if the skill already uses it). Check whether a generated copy of this skill exists elsewhere (regeneration path UNVERIFIED) and regenerate it.
2. .claude/settings.json allows codebase-memory indexing/search tools: remove those permission entries.
3. Delete .serena/project.yml; move any .serena/memories/ files to .superclaude/memory/.
Keep: the 6 historical paths.
Verify: `git grep -n -i -E 'serena|codebase-memory|codebase_memory|mcp__codebase' -- . ':!.dev' ':!claudedocs'`.
