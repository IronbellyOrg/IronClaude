Repo: IronbellyOrg/TUIBBS. Context: IronClaude (issue IronbellyOrg/IronClaude#323) removed the Serena MCP server.
Do:
1. docs/governance/post-merge-review-protocol.md has a Serena symbol cross-reference step: replace it with `rg -n -w <symbol>` plus Read of the call sites (codegraph later).
2. Delete .serena/project.yml; move .serena/memories/ files (including the brainstorming memory) to .superclaude/memory/; do not delete them.
Keep: the decision log and the historical paths.
Verify: `git grep -n -i serena -- . ':!.dev' ':!claudedocs'`.
