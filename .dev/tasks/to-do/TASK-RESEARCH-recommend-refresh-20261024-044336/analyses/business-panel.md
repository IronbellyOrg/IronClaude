# Research: /sc:business-panel recommendation alignment

- **Topic type:** Command-routing research
- **Scope:** Six-month command history, current business-panel contract, recommendation guide and skill, plugin mirror, and routing tests
- **Status:** Complete, source inspection only; no files changed
- **Date:** 2026-10-24

- **Persistence provenance:** Mechanically transcribed by the parent from `../artifacts/worker-returns/business-panel.txt`, worker `a9a7cc234c17dcee9`. The source journal is `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-RecommendUpdate/076ab338-03dd-4322-a0dc-a343e620c69e/subagents/workflows/wf_da8a02a1-53f/journal.jsonl`. Worker claims and proposed changes are not independent verification.
- **Governing template:** `src/superclaude/templates/modularization-template-review/codebase-research_template.md` (Findings, Gaps, Key Takeaways scaffold).

## Findings

### Historical changes

[CODE-VERIFIED] Two commits touched the canonical command within the requested window:

- `89df2c1105c01caff199288f949d5783f6594e70`, 2026-05-22: formatting only. The patch adds blank lines around headings, lists, and code fences, plus a final newline. It does not introduce the modes, options, output boundary, or implementation handoffs.
- `046a03ab41ac98c39a11d940794c6e96cfab6ceb`, 2026-10-03: removes `Sequential (primary)` from the MCP integration declaration, leaving Context7. This changes the declared integration surface, not the business-analysis routing or output.

Both statements were verified with exact-path `git log` and `git show` against `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/business-panel.md`.

### Current command contract

[CODE-VERIFIED] Business-panel accepts a document path or inline content. Discussion is the default; debate, Socratic, and adaptive modes are documented. Expert selection supports explicit names, domain focus, or all nine experts. Output controls include synthesis-only, structured, verbose, and questions. These are existing capabilities, not new six-month additions. `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/business-panel.md:45-80`.

[CODE-VERIFIED] The command is self-contained: its complete source contains no `## Activation` handoff to a protocol skill. The named experts are simulated perspectives, not evidence that nine independent agents run. Recommendations should invoke `/sc:business-panel`, not invent a business-panel protocol skill or promise external expert participation. `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/business-panel.md:1-129`, particularly `:118-123`.

[CODE-VERIFIED] The canonical boundary is explicit: produce expert analysis and recommendations, stop with a synthesis document, make no code or architectural changes, and execute no decisions without user approval. The output includes perspectives, consensus, reasoned disagreements, and priority-ranked recommendations. No output-path flag, persisted execution ledger, or resume interface is specified. Subsequent design, implementation, or planning is a separate user-reviewed step. `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/business-panel.md:94-129`.

### Comparison with recommendation surfaces

[CODE-VERIFIED] Basic discovery already works at the documentation-contract level. The governing guide contains a stable `business-strategy` row invoking business-panel and marking the route as supporting work, not an implementation level. Its `changes_files: no` means answers or report outputs, not an absolute prohibition on writing a report. `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md:295-316`.

[CODE-VERIFIED] That row is materially narrower than the command: it says only “business strategy, not code,” assumes `@<file>`, and has no notes about modes, inline content, expert selection, or synthesis-only output. The command explicitly supports those capabilities. This is under-description rather than total absence. `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md:316`; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/business-panel.md:45-80`.

[CODE-VERIFIED] Matching is also important for business questions attached to PRDs. The guide separately routes “review a spec, PRD, or TDD” to spec-panel. Recommend’s matching rule prefers the more specific matching phrase, giving artifact names such as PRD as an example. The documentation therefore permits a business-oriented PRD review to be pulled toward artifact critique unless the distinction between business judgment and requirements quality is made explicit. This is a contract ambiguity, not an observed runtime failure. `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md:315-316`; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md:58`.

[CODE-CONTRADICTED] The plugin command is not equivalent to the canonical command. It still declares Sequential as its primary integration and ends after integration notes, omitting the canonical synthesis-only and no-implementation boundaries. A source-verified recommendation using that plugin file can therefore encounter stale dependency claims and incomplete authorization information. `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/plugins/superclaude/commands/business-panel.md:82-93` versus `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/business-panel.md:82-129`.

[CODE-VERIFIED] A matched guide row bypasses hot-cache lookup, cold-path write-back, and semantic ranking, but still verifies the target command. Consequently this command does not need a new classifier key or keyword table merely to become discoverable. Checkout source precedence and direct candidate reads already exist in the contract. `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md:60-67,112-135`.

### Proposed recommendation changes

[UNVERIFIED] **MUST, proposed policy:** Preserve business-panel as report-only while refreshing implementation routing. Business complexity, multiple documents, or a long discussion must not turn a strategy-analysis request into task-builder, workflow, or implementation. This proposal follows the verified boundary at `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/business-panel.md:94-116`.

[UNVERIFIED] **SHOULD, proposed guide change:** In `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md`, section 3.6 and existing `business-strategy` row, describe business-model, competitive-positioning, market-entry, strategic-risk, and strategic-learning analysis. Allow document or inline input. Add conditional notes preserving requested mode, experts, focus, and output format; state that the command stops at synthesis. Keep options optional rather than imposing debate or all-experts on every request. Grounding: canonical command `:45-80,94-123`.

[UNVERIFIED] **SHOULD, proposed shared matching clarification:** In `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md`, Step 0, clarify that the requested evaluation objective outranks the artifact extension or label. Business viability of a PRD belongs to business-panel; measurable requirements and specification quality belong to spec-panel. Use the existing clarification path only when both objectives genuinely remain unresolved. Grounding: existing matching rule `:58` and adjacent guide rows `:315-316`.

[UNVERIFIED] **MUST, proposed plugin alignment:** Align `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/plugins/superclaude/commands/business-panel.md` with the canonical contract before claiming recommendation parity. Carry guide changes into `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`; do not add an independent business keyword router.

[CODE-VERIFIED] Paste-ready examples grounded in the command’s actual options are:

```text
/sc:business-panel "Stress-test our proposed market-entry strategy. Report only." --mode debate --experts "porter,taleb,meadows"
```

```text
/sc:business-panel "Help me reason through competitive positioning." --mode socratic --questions
```

The first preserves requested challenge and expert perspectives; the second demonstrates supported inline input and strategic learning. `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/business-panel.md:50-80`.

### Acceptance/regression scenarios

[UNVERIFIED] Proposed checks:

1. A market-entry debate request preserves debate and requested experts, returns analysis only, and appends no executor.
2. A business-viability review of a PRD selects business-panel; a testability review selects spec-panel.
3. Inline strategy content does not acquire an invented file path.
4. An executive-summary request preserves synthesis-only; unspecified requests retain discussion default.
5. A matched business-strategy route bypasses cache classification and verifies the current command.
6. Plugin verification rejects the removed Sequential dependency and retains the synthesis-only boundary.
7. Only a subsequent explicit implementation request enters planning; under the user’s desired policy, workflow plus implement is the default, with MDTM reserved for the most complex, long-running work.

Existing tests pin the `business-strategy` identifier and command existence, but these are structural checks, not proof of the above semantic outcomes. `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/core/test_how_we_work_routing_table.py:55-81,184-201`.

## Gaps

[CODE-VERIFIED] A scoped literal search found no business-panel-specific references in the recommendation command, recommendation skill references, cache/classifier module, hooks, or recommendation/skill tests. This is not itself a defect because discovery is dynamic and the governing guide already provides the route.

[UNVERIFIED] No command execution, model-routing evaluation, or tests were run. Installed legacy recommendation-protocol behavior was not used as evidence for this command. Plugin behavior beyond its inspected contract remains unverified.

## Key Takeaways

**CHANGE:** enrich the existing business route, resolve business-versus-specification intent ambiguity, and repair plugin contract drift.

**NO CHANGE:** retain the command name, discussion default, supporting-task classification, and synthesis-only boundary. Neither inspected historical patch justifies replacing business-panel with implementation planning.

**MUST:** preserve authorization boundaries and align the plugin command.  
**SHOULD:** expose existing options through the guide and add semantic regression cases.  
**NONE:** new keyword table, dedicated cache category, invented protocol skill, or automatic implementation handoff.
