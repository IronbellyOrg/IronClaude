# Research: /sc:tdd recommendation refresh

- **Topic type:** Command-specific routing research
- **Scope:** Six-month command history, delegated TDD skill, recommendation discovery, guide, cache and plugin implications
- **Status:** Complete research; no implementation or runtime execution
- **Date:** 2026-10-24
- **Intended persistence path:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/.dev/tasks/to-do/TASK-RESEARCH-recommend-refresh-20261024-044336/analyses/tdd.md`
- **Persistence:** Returned directly because worker developer instructions prohibit writing report files.

- **Persistence provenance:** Mechanically transcribed by the parent from `../artifacts/worker-returns/tdd.txt`, worker `ad4f831f9de01269d`. The source journal is `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-RecommendUpdate/076ab338-03dd-4322-a0dc-a343e620c69e/subagents/workflows/wf_da8a02a1-53f/journal.jsonl`. Worker claims and proposed changes are not independent verification.
- **Governing template:** `src/superclaude/templates/modularization-template-review/codebase-research_template.md` (Findings, Gaps, Key Takeaways scaffold).

## Findings

### Historical changes

[CODE-VERIFIED] The exact command history contains three changes in the requested window:

- `89df2c1105c01caff199288f949d5783f6594e70`, 2026-05-22: blank-line formatting only. No semantic routing change.
- `021f715cda6d71faf1fc241be73bf6b34069f2cc`, 2026-05-27: renamed `Activation` to `Skill Invocation`, retaining `Skill tdd`. This is discovery-significant even though execution intent is unchanged.
- `3ae238b178fb7c67ca02809d24745de620c2bd50`, 2026-09-30: removed `sequential` from MCP metadata. It did not add command capabilities or change flags.

Evidence: inspected `git log -p` for `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/tdd.md`; current activation explanation is at lines 148-156.

[CODE-VERIFIED] The substantive delegated-skill change is `5495ba2863e03d1b7ba37fe792b9a1b2989c1ca3`, 2026-06-07: added orchestrator-level reuse investigation, recorded reuse findings and required their sufficiency review. Current wording makes pre-build reuse findings advisory, with an unavailable-agent fallback. This is useful design capability, not a reason to route the user through a separate generic task-builder invocation. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/tdd/SKILL.md:212,287-318`.

### Current command contract

[CODE-VERIFIED] `/sc:tdd` creates or populates a **Technical Design Document**, not test-driven development. A component/design description is mandatory; a PRD is optional. Supported options are `--tier/-t`, `--prd`, `--from-prd`, `--resume/-r`, `--output/-o` and `--focus/-f`. Standard is the default tier; focus accepts comma-separated files or directories. These are documented prompt contracts, not a runtime argument parser verified in this investigation. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/tdd.md:13-65`.

[CODE-VERIFIED] The dispatcher explicitly loads `tdd`; it is not self-contained. It promises evidence-backed investigation, PRD traceability and reviewed template-conformant documents, while prohibiting implementation and modification of existing source code. Documentation and research artifacts are written, so “no source changes” must not become “writes nothing.” Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/tdd.md:148-176`.

[CODE-VERIFIED] Existing TDD updates are a supported capability: research changed areas, edit relevant document sections in place, and update document information/history. Resumption uses persisted TDD task state; the command documents `--resume`, while the guidance describes `/task` resumption. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/tdd/refs/operational-guidance.md:111-126` and `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/tdd.md:28-29,48,95-99`.

### Comparison with recommendation surfaces

[CODE-VERIFIED] The guide already correctly identifies `/sc:tdd` as the same skill as `/tdd`, explicitly excludes test-driven development, and distinguishes full reviewed TDD creation from single-pass `/sc:design`. Preserve these distinctions. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md:244,283`.

[CODE-CONTRADICTED] Recommendation discovery describes command handoffs through literal `## Activation`, but TDD deliberately uses `## Skill Invocation`. The extraction instructions should recognize the actual mandatory `Skill tdd` directive rather than require a heading convention. Otherwise the documented candidate record can misclassify TDD as self-contained and fail to inspect its delegated contract. This is a contract mismatch; an observed runtime misclassification was not reproduced. Evidence on both sides: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/refs/surface-enumeration.md:58-60,75-80` and `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/tdd.md:148-156`.

[CODE-VERIFIED] Standalone TDD creation/update lacks a dedicated guide routing row. The guide offers the entire full-spec chain, existing-document critique, and generic document-built routes, while standalone `/sc:tdd` appears only under Other commands. Matched rows bypass ranking and cache; Other commands are considered only after no match. Therefore artifact-only intent needs explicit protection against unrelated full implementation chains. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md:283,309,315,320` and `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md:54-61`.

[CODE-VERIFIED] The classifier collapses PRD and TDD creation into `spec-generation`; dispatch retrieves one row by classification key and emits its envelope without a fresh request-to-candidate compatibility check. Thus a valid cached PRD envelope can be reused for a TDD request if both reach that key. This is a code-supported failure condition, not proof that a production cache currently contains that row. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/prompts.py:55-56` and `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/dispatch.py:103-137`.

[CODE-VERIFIED] Cache surface hashing covers file paths and guide contents, not every command/skill/ref’s contents. Per-row validation hashes only its selected source file. A TDD command-backed row therefore does not automatically notice a delegated-skill-only or ref-only change such as reuse-audit integration. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/cache.py:63-103` and `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/dispatch.py:116-124`.

### Proposed recommendation changes

[CODE-VERIFIED] **MUST, proposed policy:** Add a standalone technical-design authoring route in the governing guide, including create, populate and update requests. Stop after delivering the requested TDD unless implementation is also requested. Distinguish authoring from critique, implementation from a TDD, and test-first coding. Keep this in the existing guide-owned routing table, not an extra keyword table. Basis: the command’s documentation-only boundary and the guide’s current full-spec/critique split cited above.

[CODE-VERIFIED] **MUST, proposed discovery correction:** Update recommendation skill Phase 0, Rule R3 and surface-enumeration instructions to recognize both handoff headings and arbitrary verified skill names. Resolve/read `tdd`, rather than inventing `sc-tdd-protocol`. Preserve source-checkout freshness precedence and installed/project lookup behavior. Basis: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md:112-132` and the activation mismatch above.

[CODE-VERIFIED] **MUST, proposed downstream policy:** Prefer workflow plus implement for ordinary implementation requested after a TDD. TDD existence, many inspected files, resumability and its internal documentation task machinery are not sufficient reasons for generic MDTM implementation routing. Reserve task-builder plus task for the most complex, long-running work or explicit MDTM inputs. This is the user’s desired policy, not current guide behavior. Current guide still recommends MDTM for many files/multiple sessions. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md:243,305-309`.

[CODE-CONTRADICTED] The TDD builder ref currently offers to **create implementation tasks using `/task`**, although the guide identifies `/task` as an existing-task-file executor. Correct this optional handoff alongside governing recommendation changes, while retaining TDD’s internal documentation execution pipeline. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/tdd/refs/build-request-template.md:154-160` versus `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md:242`.

[CODE-VERIFIED] A grounded paste-ready pattern is `/sc:tdd "<component and design objective>" --from-prd <verified-PRD-path> --tier standard --focus <verified-scope> --output <requested-output-path>`. Omit unavailable optional inputs; do not invent paths or add implementation flags. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/tdd.md:41-51`.

### Acceptance/regression scenarios

[UNVERIFIED] Proposed tests, not executed:

1. Create/populate/update a TDD: recommend TDD only, preserving supplied PRD, focus, output and tier.
2. “Use test-driven development”: do not select Technical Design Document creation.
3. Critique an existing TDD: preserve the critique route rather than authoring.
4. Implement an existing TDD: default to workflow plus implement, not generic MDTM solely because a TDD exists.
5. Resume a supplied TDD MDTM task: preserve `/task` or documented TDD resume behavior.
6. Discover `Skill tdd` under `Skill Invocation`: record skill-indirected activation.
7. Warm PRD cache, then request TDD: never emit the PRD envelope.
8. Change only delegated TDD skill/ref content: prevent stale command-backed capability claims.
9. Plugin without TDD installed: mark the matched step unavailable, never invent availability.

## Gaps

[CODE-VERIFIED] Negative tracked-path search found no current `sc-recommend-protocol` directory and no plugin TDD command/skill. A globally installed legacy protocol nevertheless exists and advertises superseded flags. Do not restore or trust it as current truth. Evidence: inspected `git ls-files`; legacy content at `/config/.claude/skills/sc-recommend-protocol/SKILL.md:1-18`.

[CODE-VERIFIED] Existing recommendation routing tests assert source-text contracts, not these TDD behavioral cases. Plugin parity tests require mirrored recommendation files and the guide copy. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/skills/test_sc_recommend_routing_contract.py:1-81` and `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/commands/test_routing_plugin_parity.py:27-36`.

[CODE-VERIFIED] The recommendation hook is explicitly fail-open guidance, not mechanical execution enforcement. It cannot establish that candidate verification actually ran. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/hooks/scripts/sc-recommend-phase0.sh:4-13`.

## Key Takeaways

[CODE-VERIFIED] **CHANGE. MUST:** Protect standalone TDD intent, recognize its actual skill handoff, prevent cross-artifact cache reuse, and align optional implementation handoffs with workflow-first policy.

[CODE-VERIFIED] **SHOULD:** Track delegated-source freshness and preserve plugin parity while adding the regression scenarios.

[CODE-VERIFIED] **NONE:** No new flags, no recreated protocol directory, no replacement of TDD’s internal research/QA machinery, and no semantic capability expansion inferred from formatting or MCP metadata changes.
