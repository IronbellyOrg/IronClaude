Repo: IronbellyOrg/llm-workflows. Context: IronClaude (issue IronbellyOrg/IronClaude#323) removed the Serena MCP server.
Do: .claude/commands/rf/opinion.md mentions a future Serena integration while declaring an empty server list; delete or reword that sentence (do not describe Serena as installed).
Keep: the 8 historical paths.
Verify: `git grep -n -i serena -- . ':!.dev' ':!claudedocs'`.
