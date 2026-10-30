Repo: IronbellyOrg/ClaudeCodeCodeAudit. Context: IronClaude (issue IronbellyOrg/IronClaude#323) removed the Serena MCP server; this repo's audit workflow documents prescribe Serena navigation and memory and require Serena tool evidence.
Do:
1. Rewrite the tool instructions and evidence requirements in README.md, 00-MASTER-PROCESS-OVERVIEW.md, 01-QUICK-START.md, 02-OUTPUT-SCHEMAS.md, 03-ACCEPTANCE-CRITERIA.md, 04-LITE-VARIANT.md, PHASE-0-DISCOVERY.md, PHASE-0A-PRD-VALIDATION.md, PHASE-2-CHUNKING.md, PHASE-3-NARROW-REVIEW.md, PHASE-4-HOLISTIC-REVIEW.md and PHASE-6-FINAL-REPORT.md: symbol navigation -> Grep plus Read (codegraph later); memory persistence -> plain files under .superclaude/memory/; acceptance evidence -> the replacement tools' output instead of Serena tool counts.
2. docs/generated/PROJECT_INDEX.md mentions a language-server dependency: check the real dependency file before removing anything (UNVERIFIED).
3. Delete .serena/project.yml; move any .serena/memories/ files to .superclaude/memory/.
Keep: the 12 historical audit and file-list records.
Verify: `git grep -n -i -E 'serena|mcp__serena' -- . ':!.dev' ':!claudedocs'`.
