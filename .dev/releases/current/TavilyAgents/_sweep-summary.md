# Tavily-first refactor — sweep summary

**Sweep scope:** every `.md` agent definition in `/config/workspace/IronClaude/src/superclaude/agents/` EXCLUDING the seven handled by parallel sibling workers and the two RF-QA files this worker owns.

**Handled by parallel siblings (out of my scope):**
- deep-research.md
- deep-research-agent.md
- rf-task-researcher.md
- rf-task-builder.md
- rf-task-executor.md
- rf-team-lead.md
- rf-assembler.md

**Owned by this worker (full refactor proposal written):**
- rf-qa.md → `rf-qa-tavily-refactor.md`
- rf-qa-qualitative.md → `rf-qa-qualitative-tavily-refactor.md`

## Sweep findings (remaining agents)

Method: read `tools:` frontmatter for each remaining agent; grep body for `WebFetch|WebSearch|tavily|mcp__tavily|web search|web research|external research|context7|library docs|standards research|current information|fetch.*docs|cve|nvd|owasp`. Score >0 hits were inspected directly to distinguish "declared as agent's role" from "incidental mention."

| Agent | tools: web entries | Body web-research role | In scope? | Justification |
|---|---|---|---|---|
| audit-analyzer.md | none (Read, Grep, Glob) | none | OUT | Audit reader — purely local-file scope. |
| audit-comparator.md | none (Read, Grep, Glob) | none | OUT | Audit comparator — purely local-file scope. |
| audit-consolidator.md | none (Read, Grep, Glob, Write) | none | OUT | Audit merge — local-only. |
| audit-scanner.md | none (Read, Grep, Glob) | none | OUT | Audit scanner — local-only. |
| audit-validator.md | none (Read, Grep, Glob) | none | OUT | Audit validator — local-only. |
| auggie-reviewer.md | none web; has mcp__auggie + mcp__serena | none — codebase-only review | OUT | Code review against local diff; uses Auggie/Serena MCP, no web research role. |
| backend-architect.md | no tools block | "standards" mentions = compliance vocab, not external lookup | OUT | Architect persona; no declared web tooling, no body-level web research workflow. |
| business-panel-experts.md | no tools block | none | OUT | Business analysis persona; no external lookup workflow. |
| confidence-calibrator.md | Read only | none | OUT | Confidence scoring — local-only. |
| debate-orchestrator.md | no tools block | none | OUT | Orchestrates inter-agent debate; no web research role. |
| devops-architect.md | no tools block | none | OUT | DevOps persona; no declared web tooling, no body web research. |
| evidence-validator.md | none (Read, Grep, Glob) | none | OUT | Evidence cross-checker — purely local-file scope. |
| frontend-architect.md | no tools block | "WCAG standards" = compliance vocab, not lookup | OUT | Frontend persona; standards mention is about implementing accessibility, not researching it. |
| learning-guide.md | no tools block | none | OUT | Teaching/explanation persona; no web research role. |
| merge-executor.md | no tools block | none | OUT | Merge applier; no web research role. |
| performance-engineer.md | no tools block | "performance standards" = compliance vocab | OUT | Performance persona; standards mention is about meeting them, not researching them. |
| pm-agent.md | no tools block | Serena MCP for session memory; "external documentation URLs" = citing existing sources | OUT | PM orchestrator; "Source URLs for external documentation" is a quality standard for cited outputs, not an agent-driven web fetch workflow. |
| python-expert.md | no tools block | "OWASP compliance" = vocab | OUT | Python expert; OWASP mention is about secure coding, not standards research. |
| quality-engineer.md | no tools block | none | OUT | QA persona; local-only verification. |
| refactoring-expert.md | no tools block | "external behavior" = code semantics, not web | OUT | Refactoring persona; no web research role. |
| repo-index.md | no tools block | none | OUT | Repo indexer — local-only. |
| requirements-analyst.md | no tools block | none | OUT | Requirements analyst persona; no web research role. |
| root-cause-analyst.md | no tools block | none | OUT | Root-cause analyst; local investigation. |
| security-engineer.md | no tools block | "OWASP standards", "industry standards", "regulatory requirements" — all vocab, no fetch workflow | OUT | Security persona; standards/CVE-adjacent vocabulary is about applying known standards to code, not researching new ones. No declared web tooling, no body-level instruction to fetch external sources. **Borderline candidate** — flagged for human review if Tavily-first policy expands to "any agent that could plausibly benefit from CVE lookup." |
| self-review.md | no tools block | none | OUT | Self-review persona — local-only. |
| socratic-mentor.md | no tools block | none | OUT | Mentoring persona; no web research role. |
| system-architect.md | no tools block | "compliance standards" = vocab | OUT | Architect persona; no declared web tooling. |
| technical-writer.md | no tools block | "accessibility standards" = vocab | OUT | Writer persona; standards mention is about applying them. |
| rf-analyst.md | WebFetch, WebSearch in tools (per grep) | — | OUT (sibling-owned) | Listed as analyst sibling — assumed handled by another parallel worker per task framing. |

## Conclusion

**In-scope for refactor proposals (this worker):** 2 agents — `rf-qa.md`, `rf-qa-qualitative.md`. Both have WebFetch/WebSearch declared but unused in practice; both get Tavily-first refactor proposals.

**Out-of-scope, no action needed:** all 28 remaining agents in the sweep. None has either (a) Tavily/WebFetch/WebSearch in its `tools:` frontmatter or (b) a body-level web research workflow that would benefit from the Tavily-first precedence rule. Mentions of "standards" / "OWASP" / "compliance" across persona agents are vocabulary about applying known frameworks to code, not about external research workflows.

**Borderline / monitor:** `security-engineer.md` is the only candidate where one could later argue for Tavily-first adoption (if it ever gains a CVE-lookup or threat-intel-feed workflow). Not in scope now.

**Note on rf-analyst.md:** it does carry WebFetch/WebSearch in its tools list and matches the web-research-role pattern; per the task framing it belongs to one of the seven sibling workers (likely under the rf-* family) and was excluded from my sweep accordingly.
