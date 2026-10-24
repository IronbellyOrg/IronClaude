Report returned directly because higher-priority subagent instructions prohibit writing report Markdown files. No files changed.

# Research: /sc:index recommendation coverage

- **Topic type:** Command contract and routing analysis
- **Scope:** Changes from 2026-04-24 through 2026-10-24; current recommendation surfaces
- **Status:** Research complete; proposals not implemented
- **Date:** 2026-10-24

## Evidence paths

All line references below use these exact files:

| ID | Absolute path |
|---|---|
| INDEX | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/index.md` |
| GUIDE | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md` |
| RECOMMEND | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md` |
| ENUMERATION | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/refs/surface-enumeration.md` |
| PROMPTS | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/prompts.py` |
| CACHE | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/cache.py` |
| DISPATCH | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/dispatch.py` |
| HOOK | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/hooks/scripts/sc-recommend-phase0.sh` |
| PLUGIN-GUIDE | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` |
| PLUGIN-INDEX | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/plugins/superclaude/commands/index.md` |
| GUIDE-TEST | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/core/test_how_we_work_routing_table.py` |
| DISPATCH-TEST | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/recommend/test_dispatch.py` |

- **Persistence provenance:** Mechanically transcribed by the parent from `../artifacts/worker-returns/index.txt`, worker `a452704178f73ec3f`. The source journal is `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-RecommendUpdate/076ab338-03dd-4322-a0dc-a343e620c69e/subagents/workflows/wf_da8a02a1-53f/journal.jsonl`. Worker claims and proposed changes are not independent verification.
- **Governing template:** `src/superclaude/templates/modularization-template-review/codebase-research_template.md` (Findings, Gaps, Key Takeaways scaffold).

## Findings

### Historical changes

[CODE-VERIFIED] Two commits touched INDEX within the inventory window. Commit `89df2c1105c01caff199288f949d5783f6594e70`, dated 2026-05-22, only inserted Markdown spacing and a final newline. Its actual patch does not change capabilities, inputs, permissions, or outputs.

[CODE-VERIFIED] Commit `3ae238b178fb7c67ca02809d24745de620c2bd50`, dated 2026-09-30, made a substantive dependency correction: it removed `sequential` from `mcp-servers`, replaced “Sequential MCP integration” with native reasoning, and retained Context7. Current corresponding text is INDEX:6,36-44. It did not retire `/sc:index` or change its documented flags.

### Current command contract

[CODE-VERIFIED] `/sc:index` generates and maintains project documentation, knowledge bases, API documentation, structure documentation, and cross-references. It is broader than a list of links. Its flow explicitly analyzes, organizes, generates, validates, and maintains documentation while preserving manual additions. INDEX:12-38.

[CODE-VERIFIED] The usage signature accepts optional `[target]`, `--type docs|api|structure|readme`, and `--format md|json|yaml`. No explicit defaults, required target, output-path flag, depth flag, resume option, or machine-readable return contract are specified. Examples demonstrate structure Markdown, API JSON, and knowledge-base generation. INDEX:19-23,60-84.

[CODE-VERIFIED] This command is self-contained: the complete command has no Activation section or delegated skill target. It names Write for documentation creation and prohibits overriding existing manual documentation without explicit update permission. Therefore it is documentation-mutating, not inherently report-only. INDEX:46-51,86-98.

### Comparison with recommendation surfaces

[CODE-VERIFIED] GUIDE describes `/sc:index` only as “Build a documentation index for a project,” immediately beside `/sc:index-repo`, which writes `PROJECT_INDEX.md` and JSON for later sessions. That summary underrepresents INDEX’s generation, maintenance, API, and knowledge-base capabilities. Both source contracts must inform the distinction. GUIDE:274-275; INDEX:14-17,27-38.

[CODE-VERIFIED] The difference affects discovery. RECOMMEND consults “Other commands” only when no routing row matches; a matched row fixes the route, bypasses cache lookup and semantic ranking, and verifies only that row’s steps. GUIDE’s `document-built` row covers API reference and README requests but offers only technical-reference, operational-guide, readme, and document. Thus project-wide documentation requests overlapping those phrases can lose `/sc:index` before semantic ranking. This is a verified contract risk, not a reproduced model execution. RECOMMEND:50-61,122,150; GUIDE:320.

[CODE-VERIFIED] There is a flag-verification mismatch. INDEX documents its flags in `Usage`, without a flag table or `argument-hint`. RECOMMEND R1 permits flags only from a flag table or argument hint, and ENUMERATION tells verification to extract an Options-section flag table. Literal compliance can suppress legitimate `--type` and `--format` arguments. INDEX:19-23; RECOMMEND:335-337; ENUMERATION:54-61. Runtime suppression was not tested.

[CODE-VERIFIED] RECOMMEND also incorrectly generalizes that commands are thin dispatchers delegating through Activation, although its verification schema supports `self-contained`. `/sc:index` supplies a concrete counterexample. RECOMMEND:114; ENUMERATION:75-80; INDEX:1-98.

[CODE-VERIFIED] PLUGIN-INDEX carries the same current dependency and usage contract. PLUGIN-GUIDE repeats the same narrow index description and documentation routing exclusion, so changing only the source guide would leave plugin recommendations outdated. PLUGIN-INDEX:6,22,36-43; PLUGIN-GUIDE:274-275,320.

[CODE-VERIFIED] PROMPTS contains no documentation-generation classification key and instructs unmatched requests to return `unknown`. DISPATCH then returns `miss_no_key` for unknown, permitting cold-path discovery. This is not evidence that every documentation request is classified correctly. PROMPTS:50-68; DISPATCH:95-108.

[CODE-VERIFIED] Cache invalidation already includes the routing guide’s content digest, while dispatch validates a cached target’s content hash. A guide correction therefore has an existing invalidation mechanism; a new fixed documentation keyword table is unnecessary. CACHE:63-94,118-140; DISPATCH:116-124.

### Proposed recommendation changes

[UNVERIFIED] **MUST, proposed policy:** Expand GUIDE section 3.9 and its existing `document-built` routing row with an explicit project-wide documentation branch: use `/sc:index` for coordinated documentation generation, knowledge bases, navigable structure documentation, or cross-referenced API documentation. Keep focused function/endpoint reference with `/sc:document`, reviewed feature architecture with `/tech-reference`, and template README work with `/readme`. This changes the sole existing routing source, not a second classifier table. Evidence anchors: GUIDE:179-184,320; INDEX:12-38.

[UNVERIFIED] **MUST, proposed contract repair:** Let RECOMMEND R1 and Phase 0 verification accept an explicit Usage signature as flag evidence, in addition to a flag table or argument hint. Carry that rule into ENUMERATION and PROMPTS’s cold-path R1. Preserve exact allowed values and reject unsupported flags. Grounded examples for the revised recommendation contract are:

```text
/sc:index . --type structure --format md
/sc:index src/api --type api --format json
/sc:index . --type docs
```

These use INDEX:22,65,73,81; they are not newly invented capabilities.

[UNVERIFIED] **SHOULD:** Expand GUIDE’s Other commands description to include generation and maintenance, and add an index versus index-repo distinction to section 5. Mirror relevant changes into PLUGIN-GUIDE and recommendation plugin primitives. Preserve self-contained activation and do not recommend installing Sequential MCP. Evidence anchors: GUIDE:238-248,274-275; INDEX:6,36-44.

[UNVERIFIED] **MUST, policy alignment:** Keep documentation work distinct from implementation planning. The user’s desired default is workflow plus implement for most planned implementation, not task-builder merely because many files or sessions are involved. Current GUIDE:305-307 still encodes those broader MDTM triggers. Correct them in the consolidated specification, but do not replace this specialized documentation command with implementation planning.

### Acceptance/regression scenarios

[UNVERIFIED] Proposed checks:

1. “Generate navigable, cross-referenced project structure documentation” recommends `/sc:index . --type structure --format md`, not index-repo or task-builder.
2. “Generate cross-referenced API documentation as JSON for this directory” retains index’s API/format capabilities; a focused endpoint-reference request still selects document.
3. “Write a short repository index for future sessions” selects index-repo instead.
4. Verification accepts index’s Usage-only flags, records self-contained activation, and rejects `--output`, `--depth`, and `--resume`.
5. Documentation no-match classification can fall through `unknown` to discovery; it is not forced into task-file generation.
6. Guide changes invalidate applicable cache rows, and plugin fallback exposes the same documentation distinction.
7. Updating manually maintained documentation retains the explicit permission boundary.

These extend existing structural guide checks and unknown-dispatch coverage, rather than claiming existing end-to-end routing tests. GUIDE-TEST:26-41,275-304; DISPATCH-TEST:70-78.

## Gaps

[CODE-VERIFIED] Scoped searches found no `/sc:index`-specific references in recommendation skill refs, CLI recommendation code, the Phase 0 hook, or recommendation tests. GUIDE-TEST explicitly requires index-repo in its Other commands set but not index. GUIDE-TEST:26-41. Existing generic command-existence checks do not demonstrate correct semantic selection.

[CODE-VERIFIED] HOOK is explicitly fail-open context injection, not blocking enforcement. Its text does not guarantee successful discovery of index. HOOK:4-13.

[UNVERIFIED] No live invocation, classifier evaluation, documentation generation, or tests were run. Output destinations, defaults, and interruption recovery remain unspecified by INDEX.

## Key Takeaways

[CODE-VERIFIED] **CHANGE:** Current recommendation descriptions understate a still-active command, matched documentation routing can exclude it, and flag verification omits its documented syntax.

[UNVERIFIED] **MUST:** Repair documentation routing and Usage-signature verification; add distinguishing regression cases. **SHOULD:** Improve index versus index-repo descriptions and mirror plugin guidance. **NONE:** No new fixed keyword table, command implementation, replacement protocol, or Sequential MCP prerequisite.
