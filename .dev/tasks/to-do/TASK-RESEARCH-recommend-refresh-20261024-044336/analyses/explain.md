# Research: /sc:explain recommendation accuracy

- **Topic type:** Command contract and recommendation routing
- **Scope:** Six-month history, current explanation capabilities, recommendation guide, classifier, installed legacy protocol, plugin mirror, and regression coverage
- **Status:** Research complete; no implementation or tests executed
- **Date:** 2026-10-24
- **Handoff:** Report text returned for the coordinator to save to `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/.dev/tasks/to-do/TASK-RESEARCH-recommend-refresh-20261024-044336/analyses/explain.md`

- **Persistence provenance:** Mechanically transcribed by the parent from `../artifacts/worker-returns/explain.txt`, worker `a09cf100b585929e9`. The source journal is `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-RecommendUpdate/076ab338-03dd-4322-a0dc-a343e620c69e/subagents/workflows/wf_da8a02a1-53f/journal.jsonl`. Worker claims and proposed changes are not independent verification.
- **Governing template:** `src/superclaude/templates/modularization-template-review/codebase-research_template.md` (Findings, Gaps, Key Takeaways scaffold).

## Findings

### Historical changes

[CODE-VERIFIED] Three commits changed the exact command during the inventory window, according to inspected Git history and patches:

- `89df2c11`, 2026-05-22: formatting only. Added blank lines and the missing final newline. No semantic delta.
- `3ae238b1`, 2026-09-30: substantive dependency correction. Removed Sequential MCP from frontmatter, replaced “Sequential MCP” analysis with native reasoning, and retained Context7 integration.
- `046a03ab`, 2026-10-03: removed the remaining Sequential-analysis comment from the architecture example. This completed the dependency-description cleanup without changing flags.

Historical evidence: those commits’ patches for `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/explain.md`. Current confirmation: that file, lines 6 and 33-44.

### Current command contract

[CODE-VERIFIED] The command explains code, concepts, system behavior, and framework-specific concepts. Its documented interface is:

```text
/sc:explain [target] [--level basic|intermediate|advanced] [--format text|examples|interactive] [--context domain]
```

The source does not specify default flag values or a mandatory target-validation rule. Recommendations must not invent defaults, `--depth`, `--output`, `--examples`, or a separate interactive boolean. Examples and interactive output are values of `--format`. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/explain.md:12-23,59-88`.

[CODE-VERIFIED] This is a self-contained Markdown command, not a skill dispatcher. It documents analysis, audience assessment, explanation construction, and validation; native reasoning handles complex analysis, while Context7 supplies framework documentation. There is no Activation section, delegated protocol, persistent ledger, resume procedure, or automatic implementation handoff. These are verified documentation contracts, not claims of observed execution. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/explain.md:25-57,92-104`.

[CODE-VERIFIED] The governing guide classifies explanation as Level 1 with `changes_files: no`. Therefore, educational complexity does not itself authorize editing code or starting implementation. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md:303`.

### Comparison with recommendation surfaces

[CODE-VERIFIED] The current guide already routes explanation requests to plain English or `/sc:explain <path>`. The principal deficiency is incomplete capability exposure, not command omission: the row only illustrates file targets and says nothing about audience level, examples, interactive explanation, or domain context. The command supports all of these. Evidence on both sides: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md:303` and `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/explain.md:12-23`.

[CODE-CONTRADICTED] Recommend’s strict flag-verification wording excludes this command’s documented flags. Rule R1 permits flags only from a “flag table” or `argument-hint`, but explain has neither; it publishes its complete signature under Usage. Following R1 literally would discard valid explanation controls. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md:335-337` versus `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/explain.md:19-23`.

[CODE-VERIFIED] The guide contains overlapping understanding intents: `ask` includes “how does something work,” while `research-first` includes “how does our system work.” The latter adds optional implementation steps. Explanation should be separated by requested deliverable and purpose: teaching an existing behavior versus producing an investigative report, feasibility assessment, or change analysis. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md:303,308`.

[CODE-VERIFIED] Matched guide routes bypass both cache lookup and cold-path write-back. Thus, changing only the classifier cannot correct normal guide-matched explanation recommendations. Conversely, the unmatched classifier broadly categorizes subsystem understanding as `codebase-research`; its native check also mixes read-and-explain work with edit-count restrictions. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md:58-61,83-86` and `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/prompts.py:55-59,87-92`.

[CODE-VERIFIED] Cache freshness is limited but relevant: the surface hash includes command paths and guide contents, while dispatch separately validates the selected candidate’s content hash. A guide change invalidates cached rows; a selected explain-command content change fails its source-hash check. This does not establish freshness for every supporting instruction. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/cache.py:63-103` and `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/dispatch.py:103-124`.

[CODE-VERIFIED] A globally installed legacy protocol remains a concrete false-routing source. Its learning category recommends document, analyze, and brainstorm, omitting explain. However, the current recommend command explicitly activates `sc-recommend`, not that legacy protocol. Evidence: `/config/.claude/skills/sc-recommend-protocol/SKILL.md:237-241` and `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/recommend.md:52-58`.

[CODE-VERIFIED] The plugin explain mirror still contains the Sequential-analysis comment removed from canonical source. Recommendation-tree parity tests enforce the recommend skill and bundled guide, not general explain-command parity. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/plugins/superclaude/commands/explain.md:77-82` and `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/commands/test_routing_plugin_parity.py:27-36`.

### Proposed recommendation changes

[UNVERIFIED] **MUST, proposed specification:** Update the existing `ask` row and section 3.5 in `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md` to distinguish educational explanation from investigative research. Retain native answers for simple questions; preserve explain for audience-tailored teaching, examples, concepts, and architecture walkthroughs. Do not add another keyword-routing table.

[UNVERIFIED] **MUST, proposed specification:** Amend Rule R1 and candidate extraction in `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md`, its surface-enumeration reference, and `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/prompts.py` to accept flags explicitly documented in a verified Usage signature. Preserve rejection of unsupported flags and values. Carry matching changes into plugin recommend mirrors.

[UNVERIFIED] **SHOULD, proposed specification:** In the classifier and native-versus-delegation guidance, distinguish files inspected from files changed. Reading several files for an explanation must not trigger implementation planning. Broad investigative reports may still warrant dedicated research.

[UNVERIFIED] **SHOULD, proposed specification:** Remove the stale Sequential claim from the plugin explain mirror and add a focused parity/dependency regression. Do not introduce a replacement explain protocol.

[CODE-VERIFIED] A paste-ready example using only documented controls is:

```text
/sc:explain microservices-system --level advanced --format interactive
```

For a supplied file target, preserve that target and add audience or presentation controls only when requested. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/explain.md:77-81`.

[UNVERIFIED] The user’s desired workflow-over-MDTM policy should apply only after an implementation request exists. Explanation should never automatically append either planning chain. If implementation is later requested, default most planned work to workflow plus implement; reserve MDTM for exceptional complexity and duration or explicit MDTM input. This is proposed policy, not the current guide’s broader escalation rule.

### Acceptance/regression scenarios

[UNVERIFIED] Proposed checks:

1. Beginner explanation with examples preserves `--level basic --format examples`; no invented flags.
2. Advanced interactive architecture explanation remains non-mutating and requires no Sequential MCP.
3. Multi-file educational walkthrough creates no implementation plan merely because several files are read.
4. Feasibility investigation produces the dedicated research route, not a superficial explanation.
5. Simple factual file question may remain native.
6. Guide-matched explanation bypasses classifier/cache; missing guide exercises verified fallback discovery.
7. Existing MDTM execution input remains an execution request, not an explanation request.
8. Plugin recommendations never describe retired Sequential capabilities.

## Gaps

[CODE-VERIFIED] Exact-path searches and `git ls-files` found no tracked legacy recommendation-protocol directory; the installed legacy file is present. Its installation provenance and actual runtime selection were not established.

[CODE-VERIFIED] The recommendation hook is explicitly fail-open and advisory, not mechanical prevention of stale routing. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/hooks/scripts/sc-recommend-phase0.sh:4-13`.

[CODE-VERIFIED] Existing routing tests inspect source text, route structure, flags, and mirror parity. No explain-specific behavioral regression appeared in the targeted recommendation searches. Tests were read, not executed.

## Key Takeaways

[CODE-VERIFIED] **CHANGE:** Preserve the already-correct Level 1 explanation route, but expose its full verified capabilities and fix the Usage-signature verification contradiction.

[UNVERIFIED] **MUST:** Clarify explanation versus investigation; permit verified Usage flags; prevent educational requests from acquiring implementation steps.

[UNVERIFIED] **SHOULD:** Align fallback classification and plugin dependency wording, then add the scenarios above.

[UNVERIFIED] **NONE:** No new command, explain protocol, fixed keyword table, automatic implementation handoff, or new flag is needed.
