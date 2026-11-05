Repo: IronbellyOrg/Octodive. Context: IronClaude (issue IronbellyOrg/IronClaude#323) removed the Serena MCP server.
Do: delete .serena/project.yml; move any .serena/memories/ files to .superclaude/memory/. Check whether runtime cleanup beyond the project file is needed (UNVERIFIED).
Keep: the 159 historical release and investigation records (evidence, not live integrations).
Verify: `git grep -n -i serena -- . ':!.dev' ':!claudedocs'`.
