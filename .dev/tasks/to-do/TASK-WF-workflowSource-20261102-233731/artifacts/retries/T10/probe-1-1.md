39cd46549d761eb17bb124524ee65f682ac45c09
family=codegraph-agent-capability
defect form: capability list attributes codegraph_impact to agents that lack it
command: grep -n -E -e "impact lookups|Symbol, caller and impact" docs/user-guide/agents.md
before:
684:- **codegraph**: Symbol, caller and impact lookups for `auggie-reviewer`, `reflect-reviewer`, `reuse-auditor` and `troubleshoot-analyst`. They use the codegraph tools when the index is fresh and fall back to Grep and Read when it is not
coupled sites: src/superclaude/agents/{auggie-reviewer,reuse-auditor,reflect-reviewer,troubleshoot-analyst}.md:5 tools lines
after:
684:- **codegraph**: Symbol and caller lookups for `auggie-reviewer`, `reflect-reviewer`, `reuse-auditor` and `troubleshoot-analyst` (`reflect-reviewer` and `troubleshoot-analyst` can also run impact lookups). They use the codegraph tools when the index is fresh and fall back to Grep and Read when it is not
