Repo: IronbellyOrg/shrapnel-gov. Context: IronClaude (issue IronbellyOrg/IronClaude#323) removed the Serena MCP server.
Do:
1. workflows/resolution-charter-rpt-workflow.md reads Serena memories and falls back to auto-memory: point the lookup at .superclaude/memory/ and keep the existing fallback.
2. Remove mcp__serena__* entries from .claude/settings.json.
3. Delete .serena/project.yml. Before touching .serena/memories/, ask the repository owner whether the memories are still needed; move them to .superclaude/memory/, never delete project knowledge.
Keep: the two memory records and the completed workflow log.
Verify: `git grep -n -i serena -- . ':!.dev' ':!claudedocs'`.
