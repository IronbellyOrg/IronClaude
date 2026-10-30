Repo: IronbellyOrg/InfraDocs. Context: IronClaude (issue IronbellyOrg/IronClaude#323) removed the Serena MCP server.
Do:
1. configurations/jenkins/artifacts/phase5.1-context-refresh-requirements.md routes symbolic queries through mcp__serena tools: replace that guidance with Grep plus Read (codegraph later, where the workspace has it). It is Markdown guidance, not executable CI.
2. Delete .serena/project.yml; move any .serena/memories/ files to .superclaude/memory/.
Keep: the 11 historical paths, including dated incident and access-check records.
Verify: `git grep -n -i serena -- . ':!.dev' ':!claudedocs'`.
