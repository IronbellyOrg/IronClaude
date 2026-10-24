# Research: /sc:tasklist recommendation accuracy

- **Topic type:** Command routing and contract comparison
- **Scope:** Changes from 2026-04-24 through 2026-10-24; current tasklist contract, recommendation surfaces, plugin availability and regression coverage
- **Status:** Research complete; no files changed or commands executed
- **Date:** 2026-10-24

Evidence aliases below identify absolute file paths. Citations use `alias:line`.

| Alias | Source |
|---|---|
| TASKLIST | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/tasklist.md` |
| PROTOCOL | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-tasklist-protocol/SKILL.md` |
| GUIDE | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md` |
| RECOMMEND | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md` |
| PROMPTS | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/prompts.py` |
| CACHE | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/cache.py` |
| OVERLAP | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-workflow-protocol/refs/overlap-routing.md` |
| ROUTING-TESTS | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/core/test_how_we_work_routing_table.py` |
| SKILL-TESTS | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/skills/test_sc_recommend_routing_contract.py` |
| PLUGIN-TESTS | `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/commands/test_routing_plugin_parity.py` |

- **Persistence provenance:** Mechanically transcribed by the parent from `../artifacts/worker-returns/tasklist.txt`, worker `a687c50056ff1a984`. The source journal is `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-RecommendUpdate/076ab338-03dd-4322-a0dc-a343e620c69e/subagents/workflows/wf_da8a02a1-53f/journal.jsonl`. Worker claims and proposed changes are not independent verification.
- **Governing template:** `src/superclaude/templates/modularization-template-review/codebase-research_template.md` (Findings, Gaps, Key Takeaways scaffold).

## Findings

### Historical changes

[CODE-VERIFIED] Exact-command history contains three changes during the window:

- `89df2c11`, 2026-05-22: blank-line normalization only. The actual patch adds spacing around fences and lists; no semantic routing change.
- `7dd3f9bd`, 2026-06-04: substantive addition of `--no-reflect`, defaulting off, plus fence-language formatting. Its patch describes skipping the pre-reflect sign-off and generated post-reflect task.
- `3ae238b1`, 2026-09-30: removes `sequential` from command MCP metadata, leaving `context7`. This changes declared dependencies, not the roadmap input or bundle output.

These statements were verified with exact-path `git log` and each command patch; the surviving flag and dependency declarations are at TASKLIST:7 and TASKLIST:23-39.

[CODE-VERIFIED] Relevant delegated changes extend beyond the thin command. The inspected `fa4dc74c` patch, 2026-06-12, replaces the generated post-execution agent directive with the reflect wrapper and required phase frontmatter. The inspected `db87420a` patch, 2026-06-25, introduces roadmap-anchored enrichment, execution context and bounded validation improvements. Current contracts preserve roadmap-primary traceability and distinguish generated post-execution tasks from generator-time checks. These are substantive changes, not formatting updates. (PROTOCOL:47-69, PROTOCOL:928-938, PROTOCOL:1131-1179, PROTOCOL:1598-1635)

### Current command contract

[CODE-VERIFIED] `/sc:tasklist` requires an existing roadmap. It accepts positional or `@file` references, optional `--spec`, optional `--output`, and `--no-reflect`. The output root is derived from the roadmap’s release directory, then version token, then a fallback. Empty/unreadable input is rejected before generation. Its activation delegates to `sc:tasklist-protocol`; this research read that contract without invoking it. (TASKLIST:20-85)

[CODE-VERIFIED] The intended output is a Sprint-compatible index plus numbered phase files, with task IDs, compliance tiers, deliverables, traceability, checkpoints and validation artifacts. Generation includes roadmap comparison and correction. Default reflect behavior comprises generator-time per-phase pre-reflect sign-off plus **templated future post-execution tasks**, not execution of the entire implementation. Pre-reflect failure is advisory: the bundle can still ship with recorded findings. (PROTOCOL:14-16, PROTOCOL:88-110, PROTOCOL:1612-1635)

[CODE-VERIFIED] This is not report-only: it writes and may patch the generated planning bundle. It does not modify the source roadmap or launch Sprint execution. The command advertises no resume flag, and its documented handoff is reporting generated paths; runtime execution remains separate. Recommendation must not turn a generation request into authorization to implement, commit or push. (TASKLIST:103-119)

### Comparison with recommendation surfaces

[CODE-VERIFIED] The guide acknowledges `/sc:tasklist` only in its distinction between `/roadmap` and the separate release pipeline. However, neither its machine-readable routing table nor its other-commands block provides tasklist-generation selection. In contrast, the command explicitly triggers on roadmap conversion and Sprint-compatible bundle generation. This is a concrete discovery gap, not evidence that the command should disappear. (GUIDE:245, GUIDE:264-289, GUIDE:299-327; TASKLIST:16-18)

[CODE-VERIFIED] Recommendation reads machine-readable guide blocks first. A matched row bypasses cache lookup, cold-path write-back and semantic ranking, and only that row’s steps are verified. Therefore a broad planning match can prevent tasklist from being considered even though dynamic enumeration supports discovering it on an unmatched request. Adding another private keyword table would contradict the existing architecture. (RECOMMEND:50-61)

[CODE-VERIFIED] The classifier distinguishes MDTM task-file generation and `/roadmap` generation, but has no explicit Sprint-bundle distinction. Its example maps “Build a tasklist for this spec” to `/task-builder`’s category. That example should not establish either that every “tasklist” means MDTM or that an ordinary spec should automatically acquire a roadmap-to-Sprint chain. (PROMPTS:55-79; TASKLIST:18-39)

[CODE-CONTRADICTED] Workflow’s overlap reference prints `/sc:tasklist --source <roadmap>`, but tasklist’s verified interface uses a **positional** roadmap and contains no `--source` option. This directly contaminates paste-ready referral accuracy. The matching plugin reference contains the same unsupported flag. (OVERLAP:8; TASKLIST:23-39; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/plugins/superclaude/skills/sc-workflow-protocol/refs/overlap-routing.md`:8)

[CODE-VERIFIED] Existing tests check guide row structure, command existence, mandatory flags and recommendation protocol text, but the inspected files contain no tasklist-specific routing scenario. Plugin parity tests require the recommendation skill mirror and bundled guide to track their source equivalents. These are useful foundations, not proof of semantic selection correctness. (ROUTING-TESTS:170-201, ROUTING-TESTS:275-304; SKILL-TESTS:35-80; PLUGIN-TESTS:27-36)

### Proposed recommendation changes

[UNVERIFIED] **MUST, desired policy:** Extend GUIDE’s existing routing source with an artifact-specific condition: “Convert an existing roadmap into a Sprint-compatible multi-file tasklist bundle.” Recommend `/sc:tasklist`, preserve the user’s provided spec/output arguments, and stop at generation unless execution was explicitly requested. Do not replace ordinary planned implementation with this release pipeline.

[UNVERIFIED] **MUST, desired policy:** Alongside the broader recommendation refresh, make workflow plus implement the default for most planned implementation. Reserve task-builder plus task for explicitly requested MDTM work or the most complex, long-running workloads. File count, multiple sessions, an existing spec, auditability and resume must not independently trigger MDTM. This changes current GUIDE:243 and GUIDE:305-308; it is not a claim that current source already follows that policy.

[CODE-VERIFIED] A grounded paste-ready tasklist example is `/sc:tasklist <roadmap-path> --spec <spec-path> --output <output-dir>`. The placeholders must remain visible unless the user supplied real paths. Do not add `--source`, `--depth`, or default `--no-reflect`. (TASKLIST:23-39)

[UNVERIFIED] **MUST:** Correct OVERLAP:8 and its plugin mirror to positional syntax. **SHOULD:** Add negative examples to PROMPTS so “tasklist” alone does not select MDTM or Sprint generation; use the actual input artifact and requested deliverable. Requests outside the existing cache vocabulary can fall through to live verification rather than inventing another fixed keyword map.

[CODE-VERIFIED] Guide edits already invalidate the checkout cache because its hash includes guide bytes. Other command and skill entries contribute paths, not their contents; therefore a delegated-protocol-only edit does not necessarily invalidate a command-backed cache row. Preserve guide-first bypass and test delegated-source freshness if cached capability descriptions depend on that protocol. (CACHE:63-94)

### Acceptance/regression scenarios

[UNVERIFIED] Proposed checks:

1. Existing roadmap plus explicit Sprint-bundle intent selects tasklist, not workflow or task-builder.
2. Clear implementation across several files and sessions defaults to workflow plus implement.
3. Explicit MDTM execution remains `/task`; a workflow package is not converted to MDTM.
4. Spec-only “make a tasklist” does not fabricate a roadmap requirement or automatically choose MDTM.
5. Generated advice uses positional roadmap syntax and supported flags.
6. Generation-only advice does not start Sprint execution or claim generated post-reflect tasks already ran.
7. Missing plugin tasklist capability is reported honestly rather than silently replaced with a different artifact.
8. Guide changes invalidate cached answers; plugin guide parity remains enforced.

## Gaps

[CODE-VERIFIED] Exact tracked-path inspection found no tasklist command/protocol in the plugin distribution and no tracked `sc-recommend-protocol` source directory. The globally installed legacy protocol does exist at `/config/.claude/skills/sc-recommend-protocol/SKILL.md`; its opening contract describes old flags and keyword routing, not current recommendation authority.

[UNVERIFIED] Tasklist prose mentions `--dry-run` and supplementary `--tdd-file`/`--prd-file`, but the command flag table does not expose them. Do not recommend those flags until the interfaces are reconciled. (TASKLIST:39; PROTOCOL:49-53)

[UNVERIFIED] No generation, classifier evaluation or regression tests were executed. Findings establish documentation and implementation contracts, not successful runtime behavior.

## Key Takeaways

[UNVERIFIED] **CHANGE. MUST:** Surface tasklist for explicit roadmap-to-Sprint-bundle work, correct the unsupported referral flag, preserve generation-only authorization and add artifact-specific regressions.

[UNVERIFIED] **SHOULD:** Clarify classifier negative examples and delegated-source cache freshness; synchronize the bundled plugin guide.

[UNVERIFIED] **NONE:** No new tasklist capability, forced Sprint migration, extra routing table or source implementation is needed for this research handoff.
