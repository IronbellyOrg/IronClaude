daf091791b274de69e219a80819834369813228d tree=4f5242b743204f608e6c93a9b6e99c0adf1f006a
T8.AC1 met docs/user-guide/flags.md:182
T8.AC2 met docs/user-guide/flags.md:1
F1.1 sev=blocking trigger=B2 ac=scope at=docs/user-guide/flags.md:9 anchor=src/superclaude/core/CLAUDE.md:22 chk=n,y,n,n family=hint-flag-definition-scope fix=Narrow the line 9 sentence so it covers only the flags with no installed definition (the analysis, behavioral mode and execution control flags), or say that the shipped ~/.claude/CLAUDE.md MCP table lists --c7, --tavily and --play as advisory flags first=A1 origin=new: Line 9 says "no installed file defines the hint flags in this section". That section includes the MCP Server Flags table, but the shipped ~/.claude/CLAUDE.md lists --c7, --tavily and --play in its MCP table (src/superclaude/core/CLAUDE.md:22-24). Line 29 of the same file says only --morph is missing from that table, so the page contradicts itself.
F1.1 resolved
