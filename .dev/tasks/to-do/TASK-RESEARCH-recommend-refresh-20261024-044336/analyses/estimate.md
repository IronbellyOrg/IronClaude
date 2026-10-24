# Research: retired `/sc:estimate` and recommendation accuracy

- **Topic type:** Command retirement and recommendation routing
- **Scope:** Six-month history through 2026-10-24; current recommendation, installed remnants, cache, plugin mirrors, and regression coverage
- **Status:** Research complete; no files changed
- **Date:** 2026-10-24

- **Persistence provenance:** Mechanically transcribed by the parent from `../artifacts/worker-returns/estimate.txt`, worker `a5366a759278a4239`. The source journal is `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-RecommendUpdate/076ab338-03dd-4322-a0dc-a343e620c69e/subagents/workflows/wf_da8a02a1-53f/journal.jsonl`. Worker claims and proposed changes are not independent verification.
- **Governing template:** `src/superclaude/templates/modularization-template-review/codebase-research_template.md` (Findings, Gaps, Key Takeaways scaffold).

## Findings

### Historical changes

[CODE-VERIFIED] Two commits changed the assigned command during the requested window:

1. `89df2c1105c01caff199288f949d5783f6594e70`, **2026-05-22**, added blank lines around headings, lists, and fences. Its actual patch contains no semantic change.
2. `3ae238b178fb7c67ca02809d24745de620c2bd50`, **2026-09-30**, deleted the entire command. The commit explicitly says “Remove estimate, select-tool, sc dispatcher, and the post-release-update alias.”

The inspected historical path was `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/estimate.md`. It does not exist at HEAD. This is a retirement, not a recently enhanced capability requiring a new recommendation row.

### Current command contract

[CODE-VERIFIED] There is **no current canonical `/sc:estimate` contract** to activate. Its last historical contract was self-contained, with no delegated skill activation. It accepted a target and optional `--type time|effort|complexity`, `--unit hours|days|weeks`, and `--breakdown`. It did not specify defaults for those options. Its requested output included effort/time breakdown, complexity, confidence intervals, risks, and resource requirements.

[CODE-VERIFIED] A stale installed copy remains readable at `/config/.claude/commands/sc/estimate.md:19-38,100-121`. It explicitly requires an **estimation report only**, prohibits implementation and commitments, and leaves planning/execution to a later user decision. These are verified document instructions, not evidence that its estimation methodology or accuracy ever worked at runtime.

### Comparison with recommendation surfaces

[CODE-VERIFIED] The current dispatcher loads `sc-recommend`, not the legacy protocol. Its supported flags are only `--plugin`, `--eval`, and `--minstar`; it explicitly excludes `--estimate`. See `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/recommend.md:30-58`. Therefore, retiring `/sc:estimate` does **not** justify restoring recommendation’s old estimation flag.

[CODE-CONTRADICTED] Installed legacy material contradicts that current interface: `/config/.claude/skills/sc-recommend-protocol/SKILL.md:282-295` still describes `--estimate`, fixed project-duration ranges, experience multipliers, and percentage allocations. The tracked-file search found no current canonical `sc-recommend-protocol` package. This installed remnant must not be treated as the active protocol merely because the skill listing exposes it.

[CODE-VERIFIED] The most important defect is **retirement-blind source verification**. Current enumeration searches installed commands, project commands, plugin commands, and checkout sources. Checkout precedence is specified only when the **same name exists in several locations**. Verification then accepts a readable source from any enumerated location. See `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md:100-135`.

[CODE-VERIFIED] Consequently, the installed estimate file satisfies the documented existence check even though its canonical checkout command was removed. This is a structural route by which a retired shipped command can survive candidate verification. It is **not** proof that a live recommendation actually selected it. The corresponding plugin reference repeats the same enumeration and duplicate precedence rules at `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/plugins/superclaude/skills/sc-recommend/refs/surface-enumeration.md:17-25,54-67`.

[CODE-VERIFIED] Cache invalidation helps but does not settle retirement. Surface hashes incorporate command-path additions/deletions and routing-guide content; a changed surface discards cached rows. However, dispatch subsequently checks only the cached source path’s existence and byte hash before returning its envelope. It does not verify that the target remains an eligible current-distribution command. See `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/cache.py:63-94,117-140` and `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/dispatch.py:103-136`. A cold path can therefore rediscover an installed remnant after invalidation; invalidation alone is insufficient.

[CODE-VERIFIED] The condensed cold-path instructions repeat existence-only verification at `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/prompts.py:132-148`. Both full-skill and condensed-worker contracts need the same eligibility rule.

[CODE-VERIFIED] Current governing guide rows also conflict with the user’s desired planning policy. They route “many files,” “more than one session,” and “must not drift” to task-builder; clear existing-system features also route there. See `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md:305-308`. These are current rules, not evidence that workflow lacks capacity. An estimation request should not accidentally trigger those implementation routes simply because the subject is large.

### Proposed recommendation changes

[UNVERIFIED] **MUST: Add retirement-aware candidate eligibility**, as a proposed contract change, to Phase 0 and its surface-enumeration reference. A known retired **shipped** identity must not become an implicit current-framework recommendation solely because an old installed file remains readable. Preserve legitimate user-created commands and unrelated third-party skills. This requires provenance-aware retirement information, not a blanket “absent from checkout means forbidden” rule and not another keyword-routing table.

[UNVERIFIED] **MUST: Apply that eligibility decision consistently** to the condensed cold-path runbook and hot-cache validation. Reject cached retired targets even when their leftover source bytes still match. Include any retirement information used for eligibility in cache freshness decisions. Mirror the resulting contracts into the applicable plugin surfaces.

[UNVERIFIED] **MUST: Preserve report-only intent.** For an estimation-only request, explain that the former dedicated command is retired in the current distribution, then recommend evidence gathering or an appropriately scoped report. Do not promise the removed command’s confidence intervals, manufacture durations, or silently create implementation work.

A paste-ready fallback for an actual feasibility investigation is:

`/tech-research "Assess the feasibility, dependencies, effort drivers, and risks of the requested change in the code areas I identified. Use supplied historical delivery data where available; label missing evidence. Produce findings and options only, without implementing the change."`

Its investigation/report scope and required-question interface are documented at `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/tech-research/SKILL.md:51-72`. This is not a claim that it replaces every estimation capability.

[UNVERIFIED] **SHOULD: Separate any subsequent planning request.** If the user later asks to implement, use the proposed workflow-first policy for most planned work; reserve MDTM for the most complex and long-running work or explicit MDTM inputs. A supported planning example is `/sc:workflow "<agreed change, constraints, and code areas>" --depth standard`; the verified command accepts those inputs and remains plan-only at `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/workflow.md:18-42,63-80`. Adopting this preference requires changing the governing guide, not merely overriding it inside recommendation.

### Acceptance/regression scenarios

[UNVERIFIED] Proposed regression cases:

1. Installed estimate file remains, canonical estimate is retired: implicit recommendation never emits it.
2. A cached estimate target points to an unchanged installed remnant: eligibility rejects it despite a matching byte hash.
3. An estimation-only request names a large migration: output remains report-only, without automatic task-builder or implementation handoff.
4. A legitimate custom installed-only command remains eligible; absence from checkout alone does not retire it.
5. Explicit `/sc:estimate` discovery requests explain retirement rather than silently substituting execution.
6. A later request for an ordinary multi-file implementation uses workflow plus implement under the new policy; explicit MDTM execution remains `/task`.

## Gaps

[CODE-VERIFIED] Exact searches found no active estimate reference in the canonical recommendation skill, its references, current guide, or recommendation tests. Existing routing-contract tests pin guide precedence, mandatory flags, built-ins, hard limits, and cache availability, but not retired-command eligibility: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/skills/test_sc_recommend_routing_contract.py:35-80`.

[CODE-VERIFIED] The hook is explicitly fail-open and injects reminders, rather than mechanically proving verification occurred: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/hooks/scripts/sc-recommend-phase0.sh:4-19`. It cannot independently prevent retirement leakage.

[UNVERIFIED] No live recommendation or estimation was executed. Plugin execution and installed upgrade history were not established. Stale legacy root-command materials are follow-up cleanup, not evidence of current canonical behavior.

## Key Takeaways

- **CHANGE:** Close retirement leakage across enumeration, cold-path verification, and warm-cache eligibility.
- **MUST:** Preserve estimation-only intent and keep retired estimate/legacy estimation flags out of current recommendations.
- **SHOULD:** Align later implementation handoffs with the user’s workflow-first policy through the governing guide.
- **NONE:** Do not recreate `/sc:estimate`, invent replacement flags, or add a fixed keyword-routing table.
