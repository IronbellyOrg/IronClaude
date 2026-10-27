# D-0005: Agent Prompts Extraction Spec

| Field | Value |
|---|---|
| Task | T02.01 |
| Deliverable | `.claude/skills/prd/refs/agent-prompts.md` |
| Source | SKILL.md lines 553-967 |
| Method | `sed -n '553,967p'` verbatim extraction with 7-line purpose header prepended |
| Line count | 422 (7 header + 415 source) |

## Content

File contains:
1. Purpose header with extraction provenance
2. Section header "Agent Prompt Templates" and introductory paragraph (lines 553-557)
3. All 8 agent prompt templates extracted verbatim:
   - Codebase Research Agent Prompt
   - Web Research Agent Prompt
   - Synthesis Agent Prompt
   - Research Analyst Agent Prompt (rf-analyst)
   - Research QA Agent Prompt (rf-qa -- Research Gate)
   - Synthesis QA Agent Prompt (rf-qa -- Synthesis Gate)
   - Report Validation QA Agent Prompt (rf-qa -- Report Validation)
   - Assembly Agent Prompt (rf-assembler)
4. "Common web research topics for PRDs" list (lines 679-686)
