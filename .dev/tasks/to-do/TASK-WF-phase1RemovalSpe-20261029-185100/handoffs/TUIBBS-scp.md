Repo: IronbellyOrg/TUIBBS-scp. Context: IronClaude (issue IronbellyOrg/IronClaude#323) removed the Serena MCP server.
Do: delete .serena/project.yml; move any .serena/memories/ files to .superclaude/memory/.
Keep: the 11 prior audit, study, decision and .dev records.
Verify: `git grep -n -i serena -- . ':!.dev' ':!claudedocs'`.
