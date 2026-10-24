# Research: /sc:release-split

- **Topic type:** Command routing and recommendation fidelity
- **Scope:** Six-month command history, delegated protocol, recommendation surfaces, cache, plugin and regression coverage
- **Status:** Research complete; no files changed; returned directly under the subagent's higher-priority no-report-file instruction
- **Date:** 2026-10-24

- **Persistence provenance:** Mechanically transcribed by the parent from `../artifacts/worker-returns/release-split.txt`, worker `ad280088e8332d320`. The source journal is `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-RecommendUpdate/076ab338-03dd-4322-a0dc-a343e620c69e/subagents/workflows/wf_da8a02a1-53f/journal.jsonl`. Worker claims and proposed changes are not independent verification.
- **Governing template:** `src/superclaude/templates/modularization-template-review/codebase-research_template.md` (Findings, Gaps, Key Takeaways scaffold).

## Findings

### Historical changes

[CODE-VERIFIED] Read-only Git history for `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/release-split.md` establishes four changes during the inventory window:

- `f79b1bd54f65cf41a868a495a7c20820e078e2c3`, 2026-05-13: substantive output-location restriction, refusing distributable-component directories before writing.
- `89df2c1105c01caff199288f949d5783f6594e70`, 2026-05-22: formatting only, adding Markdown spacing. No semantic delta.
- `70ef6486ef878975fc61569292c340c6a79fccd9`, 2026-05-30: changed the default analysis partner and example from Haiku to Sonnet.
- `3ae238b178fb7c67ca02809d24745de620c2bd50`, 2026-09-30: removed Sequential from MCP metadata, not from the four-part behavioral contract.

[CODE-VERIFIED] Delegated-protocol patches add relevant October changes: `5c6a7d919ee1381f3c825f793161b45256131b74`, 2026-10-22, replaced a checkout-only adversarial prerequisite path with the installed location; `3fcb54175b844907a19c6b7cabb756683177954b`, the same day, restored acceptance of the project-local copy. The current contract accepts either surface. (`/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-release-split-protocol/SKILL.md:137`)

### Current command contract

[CODE-VERIFIED] This is a specialized release-boundary decision tool, not a general implementation planner. It evaluates a natural seam between two independently valuable, testable releases, keeps “do not split” valid, and explicitly rejects simply halving effort. Input is an existing release spec, roadmap, tasklist or refactor plan, including Markdown or YAML. Missing, empty or insufficient-scope inputs stop processing; tasklist input warrants user confirmation. (`/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-release-split-protocol/SKILL.md:29-37,61-88`)

[CODE-VERIFIED] Useful options are `--output`, `--depth quick|standard|deep`, `--interactive`, `--resume-from`, `--no-split`, `--r1-scope`, `--smoke-gate` and `--agents`. Defaults include standard depth, no interactive checkpoints, fidelity/schema emphasis for Release 1, smoke gate in Release 2, and `opus:architect,sonnet:analyzer`. Recommendation should normally preserve defaults rather than attach unnecessary flags. (`/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/release-split.md:48-60`)

[CODE-VERIFIED] It writes planning documents and a fidelity audit, delegates their preparation, and does not implement resulting plans or manage Git. The command loads `sc:release-split-protocol`. `--interactive` adds confirmation checkpoints; its default false does not promise approval before every phase. `--resume-from` consumes a validated proposal and skips discovery/debate. `--no-split` instead proceeds to single-release validation. Release 2 roadmap/tasklist generation remains gated on reviewed real-world Release 1 validation. (`/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/release-split.md:100-126`; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-release-split-protocol/SKILL.md:120-137,258-316`)

### Comparison with recommendation surfaces

[CODE-VERIFIED] The governing guide exposes release-split only as optional step 6 of the full-spec workflow, following PRD/TDD preparation. There is no standalone routing row for assessing an existing release boundary. By contrast, the actual command accepts several already-existing artifact types. This is incomplete discovery coverage, not proof that every live invocation misroutes. (`/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md:70-72,301-325`; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-release-split-protocol/SKILL.md:69-88`)

[CODE-VERIFIED] Recommendation matches guide rows before consulting its cache; a matched row bypasses cache lookup, cold-path write-back and semantic ranking. Otherwise it enumerates candidates and reads their command contracts. Consequently, improving only semantic candidate descriptions cannot repair a conflicting matched guide row. The governing guide is the correct place for a standalone route. (`/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md:39-61,120-135`)

[CODE-VERIFIED] Current guide rows escalate “many files,” “more than one session” and “must not drift” to task-builder. The recommendation skill and condensed cold-path prompt repeat the larger/longer/riskier distinction. These are current rules, not the user's desired workflow-first policy. They must not turn release-analysis outputs into implementation work merely because several artifacts are written. (`/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md:305-309`; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md:148-157`; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/prompts.py:160-175`)

[CODE-VERIFIED] Cache freshness is narrower than complete delegated-behavior freshness: the global fingerprint hashes discovered paths plus guide contents; dispatch hashes the single stored `source_path`. It does not traverse a command's activated skill and references. Therefore an unchanged command file can retain a valid cache entry after its delegated protocol changes. Guide edits invalidate the global fingerprint, and a dedicated matched route bypasses this cache altogether. (`/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/cache.py:63-103`; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/dispatch.py:104-136`)

### Proposed recommendation changes

[UNVERIFIED] **MUST, proposed policy:** Add one supporting route to the existing governing table, not a second keyword table. Its condition should be “assess whether an existing release artifact should remain intact or split at an independently valuable validation seam.” Route to `/sc:release-split <release-artifact>`, stop after its deliverables, and retain optional use within full-spec. Explain artifact writes without implying application-source mutation or implementation authorization. Target: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md`, sections 3.6 and Routing table. Grounding: current table omission and command boundary above.

[UNVERIFIED] **MUST, proposed examples:** Use `/sc:release-split <release-artifact>` for neutral assessment; append `--interactive` only when checkpoints are wanted, `--no-split` for intact-release validation, or `--resume-from <validated-proposal>` for the documented handoff. Leave missing paths as visible placeholders. Do not invent an analysis-only flag or describe resume as resuming application implementation. Grounding: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/release-split.md:48-60,80-90`.

[UNVERIFIED] **MUST, proposed policy alignment:** Preserve specialized release assessment before implementation selection. When the user separately requests implementation planning, default to workflow plus implement for most work; reserve task-builder plus task for the most complex, long-running work or explicit MDTM inputs. Do not use release size, existing specifications, auditability or resume alone as escalation triggers. Update governing level language and its recommendation/runbook copies together, rather than claiming current sources already implement this policy.

[UNVERIFIED] **SHOULD, delivery:** Mirror guide changes into `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`. That mirror currently carries the same full-spec-only release-split reference. A plugin-only installation lacking the command must retain the recommendation skill's explicit “not installed” handling, not fabricate availability or silently substitute implementation planning. (`/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md:309`; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md:135,150`)

### Acceptance/regression scenarios

[UNVERIFIED] Proposed tests should cover: standalone release-seam assessment selecting release-split without PRD/TDD regeneration; intact validation preserving `--no-split`; validated-proposal handoff preserving `--resume-from`; multi-artifact output not triggering task-builder; generic spec critique not becoming release splitting; ordinary multi-file implementation remaining workflow-first; and a plugin installation missing release-split showing an unavailable step. Existing recommendation tests pin guide-first, flags and availability text, but do not exercise these release-specific decisions. (`/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/skills/test_sc_recommend_routing_contract.py:35-81`)

## Gaps

[CODE-CONTRADICTED] The integration reference still names Haiku despite the command and protocol now defaulting to Sonnet. Record a source-consistency follow-up; do not copy the stale model into recommendation examples. (`/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-release-split-protocol/refs/adversarial-integration.md:26-40`; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/release-split.md:60`)

[CODE-VERIFIED] Searches found no tracked recommendation-protocol directory or release-split plugin command/protocol, but `/config/.claude/skills/sc-recommend-protocol/SKILL.md:1-44` exists globally with legacy flags and keyword mapping. It is stale installed evidence, not current repository authority. The current command activates `sc-recommend`, not this legacy protocol.

[CODE-VERIFIED] The recommendation hook is fail-open context injection, not mechanical enforcement, despite stronger command wording. (`/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/hooks/scripts/sc-recommend-phase0.sh:4-19`; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/recommend.md:60`)

[UNVERIFIED] No command, skill, classifier or test was executed. Behavioral findings verify written contracts and inspected Python logic, not observed end-to-end routing.

## Key Takeaways

[UNVERIFIED] **CHANGE. MUST:** expose standalone release-boundary assessment in the governing guide and preserve its non-implementation boundary while applying the user's workflow-first policy.

[UNVERIFIED] **SHOULD:** add focused routing regressions, mirror the guide, and track stale reference/default and delegated-cache-freshness follow-ups.

[UNVERIFIED] **NONE:** no additional keyword table, automatic implementation chain, mandatory split decision, invented flags or new classifier category is needed.
