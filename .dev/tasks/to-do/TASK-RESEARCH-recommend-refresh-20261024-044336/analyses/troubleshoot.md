# Research: /sc:troubleshoot recommendation refresh

- **Topic type:** Command-history and routing-contract research
- **Scope:** Six-month command history, current diagnostic/remediation behavior, recommendation surfaces, plugin discrepancies, and regression requirements
- **Status:** Complete; documentation contracts inspected, not executed
- **Date:** 2026-10-24
- **Persistence:** Returned directly because higher-priority worker instructions prohibit writing report files.

- **Persistence provenance:** Mechanically transcribed by the parent from `../artifacts/worker-returns/troubleshoot.txt`, worker `a4c23cf3027698bc3`. The source journal is `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-RecommendUpdate/076ab338-03dd-4322-a0dc-a343e620c69e/subagents/workflows/wf_da8a02a1-53f/journal.jsonl`. Worker claims and proposed changes are not independent verification.
- **Governing template:** `src/superclaude/templates/modularization-template-review/codebase-research_template.md` (Findings, Gaps, Key Takeaways scaffold).

## Findings

### Historical changes

[CODE-VERIFIED] Exact-command history in the requested window contains substantive changes, not just formatting:

- `6633c54f`, 2026-05-21: replaced the earlier generic debugger with tiered diagnosis, protocol activation, independent calibration, escalation, and opt-in remediation. Removed the old `--trace` interface.
- `73d49c00`, 2026-05-22: introduced documentation grounding, `--no-doc-discovery`, and protection against changing code that already matches its documented contract.
- `71f16e13`, 2026-06-12: added topology-triggered Pipeline Hardening Closure and its reported evidence paths. Also labeled code fences; the commit was not formatting-only.
- `300c06a6`, 2026-06-17: added `--context` and `--caller` for the Test Failure Escalation Protocol handoff.
- `156f2829`, 2026-07-01: corrected the Tavily tool identifier. This was interface maintenance, not a new routing capability.
- `17d7cd77`, 2026-09-20: strengthened inconclusive/blocked reporting, execution-locus evidence, authorization restrictions, and conditional behavior-definition grounding.
- `3ae238b1`, 2026-09-30, and `782621f4`, 2026-10-01: removed Sequential MCP references in metadata and synthesis guidance.
- `046a03ab`, 2026-10-03: removed one blank line. Its troubleshoot patch was formatting-only.
- `f9a0ed54`, 2026-10-16: changed default `--fix` remediation from task-builder to workflow/implement; MDTM now requires `--fix --depth deep`.
- `dc9e5609`, 2026-10-16: aligned that route with managed workflow packages and the workflow's built-in pre-review.

Evidence: read-only `git log -p` for the exact command; current interface confirmed by E1, E3, and E4.

### Current command contract

[CODE-VERIFIED] The command requires an issue description or a scope accompanied by a brief symptom. It supports bug, build, performance, deployment, security, and test diagnosis. Default depth is standard, with escalation determined by the protocol; quick caps diagnosis at Tier 1, deep requests deeper diagnosis, and `--no-escalate` suppresses fan-out. `--depth quick --fix` is invalid. Other useful verified inputs include scope, output directory, model overrides, caller context, and explicitly degraded MCP/documentation-discovery modes. E1.

[CODE-VERIFIED] Output is an evidence-backed report and supporting artifacts, not an automatically applied repair. The command must preserve inconclusive, blocked, and failed outcomes rather than promising a root cause or recommending an unauthorized rerun. Its activation target is the troubleshoot protocol. E1.

[CODE-VERIFIED] Successful diagnosis plus `--fix` plus explicit acceptance permits **planning**, not automatic execution. Standard requested depth selects workflow, whose pre-review is consumed without duplication; the user subsequently runs implement. Deep requested depth selects task-builder and the user subsequently runs task. Auto-escalation to Tier 2 does not change this selection. A workflow package must never be handed to task. E3-E4.

### Comparison with recommendation surfaces

[CODE-CONTRADICTED] The governing guide still associates `--fix` with a larger/riskier task-file offer, then directs larger/riskier fixes to task-builder. The machine-readable `bug` row repeats this. Current troubleshoot instead makes plain `--fix` the workflow route. This is a direct, recommendation-affecting contradiction, not merely different wording. E1-E4.

[CODE-VERIFIED] Recommend reads the guide before ranking or cache lookup. A matched row bypasses both hot-cache dispatch and cold-path write-back and verifies the row's named targets directly. Therefore updating only the troubleshoot command or a cached recommendation cannot correct the stale `bug` row. E5.

[CODE-VERIFIED] The `bug` row lists implementation branches and `changes_files=yes` without an explicit diagnosis-only stopping condition. Its unconditional inconclusive-case advice to rerun with deeper analysis also lacks the current command's blocked/failed and authorization qualifications. The command expressly requires preserving those states. E1-E2.

[CODE-CONTRADICTED] The plugin troubleshoot command is materially older: it advertises `--trace`, omits the current depth and test/security interface, and says build fixes apply automatically. The current source command removes that interface and requires a separate user-run executor. Plugin recommendations cannot safely assume current source capabilities when verification resolves to this older file. E1, E6.

[CODE-VERIFIED] Cache freshness is relevant only to unmatched requests. Its surface fingerprint hashes command/skill/agent **paths** plus guide content; candidate content is separately hashed. It does not content-fingerprint delegated protocol references. Consequently a protocol/ref-only behavior change is not represented by that surface hash when paths, guide, and selected candidate remain unchanged. This is a source-level dependency observation, not an executed stale-cache reproduction. E5, E7.

### Proposed recommendation changes

[UNVERIFIED] **MUST: update guide section 3.4 and the existing `bug` row.** Preserve diagnosis as its own useful outcome. Make subsequent implementation conditional on the user's request and a supported report. Offer workflow/implement for most planned repairs; reserve MDTM for explicitly selected or exceptionally complex, long-running repair programs. File count, sessions, a spec, auditability, and resume needs must not independently select MDTM. This is the requested policy change, not the current guide rule. E2 identifies the replacement targets.

[UNVERIFIED] **MUST: describe the actual `--fix` boundary.** Plain `--fix` means “offer workflow planning after successful diagnosis and acceptance,” not “apply a repair” or “select task-builder.” Preserve the managed package handoff and avoid adding a second pre-review. Do not attach quick depth to this invocation. Proposed paste-ready example, using verified flags:

`/sc:troubleshoot "The nightly invoice job now raises KeyError for tenant_id after deployment; expected invoices for every tenant. Diagnose the failure and offer a remediation plan." --type bug --fix`

The example supplies a hypothetical symptom, not an assertion about repository code. E1, E3-E4.

[UNVERIFIED] **MUST: separate deep diagnosis from automatic MDTM recommendation.** Current flags couple deep-plus-fix to MDTM. If the user wants thorough diagnosis followed by ordinary planning, recommend deep diagnosis **without** `--fix`, then workflow from its supported report. Do not invent a selector that decouples those behaviors. Changing the command's coupling would be a separate implementation decision. E1, E3.

[UNVERIFIED] **MUST: preserve diagnosis-only and blocked-result off-ramps.** For report-only intent, stop after the report. For inconclusive results, follow the report's pending evidence requirements; for blocked/failed states, do not promise that deeper analysis or another rerun clears an external block. E1-E2.

[UNVERIFIED] **MUST: reconcile plugin availability before advertising modern behavior.** Synchronizing only recommend's plugin guide is insufficient while its troubleshoot command still advertises auto-fixes and an obsolete interface. Either deliver the verified modern command with its required protocol dependencies or report that capability as unavailable. E1, E6.

[UNVERIFIED] **SHOULD: handle shared cache freshness centrally.** Include verified delegated behavior dependencies, or revalidate them before replay, rather than adding a troubleshoot-specific keyword table. Guide updates already affect its digest; protocol-ref changes need an explicit freshness decision. E5, E7.

### Acceptance/regression scenarios

[UNVERIFIED] Add the following recommendation cases, grounded in E1-E5:

1. Stack trace plus “diagnosis only” recommends troubleshoot without fix and stops after the report.
2. Plain fix opt-in selects workflow planning, never task-builder, even after automatic Tier 2 escalation.
3. Deep diagnosis alone creates no MDTM handoff.
4. Explicit deep-plus-fix accurately announces the existing MDTM route and separate execution gate.
5. Quick-plus-fix is never emitted.
6. A repair spanning several files or sessions still defaults to workflow under the new policy.
7. A blocked report receives no unconditional deeper-rerun or auto-fix advice.
8. A workflow package is handed to implement, not task, with no duplicate pre-review.
9. Plugin-only verification never silently imports unsupported source flags or auto-fix promises.
10. A matched bug request bypasses an intentionally stale cache row.

[CODE-VERIFIED] Existing recommendation-contract tests check guide ordering, hard-limit text, mandatory flags, built-ins, and CLI gating. They do not establish these troubleshoot-specific behavioral outcomes. E8.

## Gaps

[CODE-VERIFIED] Tracked-file inspection found no source recommend-protocol directory and no plugin troubleshoot-protocol files. The installed legacy recommend protocol exists and still describes keyword categories and retired recommendation flags. Its presence is not evidence that current tracked recommend activates it. E9; current activation was inspected separately.

[CODE-VERIFIED] The hook inspected during this pass is fail-open context injection, not mechanical prevention of a missed enumeration gate. E10. This is a shared recommend finding, not a reason to duplicate routing logic here.

[UNVERIFIED] No diagnostic workflow, cache scenario, or regression suite was executed. No capacity or timing claims were independently measured. Broader legacy-protocol cleanup belongs with the recommend analyst.

## Key Takeaways

[UNVERIFIED] **CHANGE. MUST:** correct the authoritative bug route, preserve report-only and blocked outcomes, describe default workflow remediation accurately, and address the stale plugin capability surface. **SHOULD:** add behavioral regression cases and shared dependency-aware freshness. **NONE:** no new fixed keyword-routing table, fabricated flags, automatic execution, or claims that workflow supports unlimited complexity.

### Evidence register

- **E1:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/troubleshoot.md:24-84`
- **E2:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md:121-134,299-313`
- **E3:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-troubleshoot-protocol/refs/remediation-handoff.md:5-22`
- **E4:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:574-595`
- **E5:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md:39-88`
- **E6:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/plugins/superclaude/commands/troubleshoot.md:19-69`
- **E7:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/cache.py:63-103`
- **E8:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/skills/test_sc_recommend_routing_contract.py:35-80`
- **E9:** `/config/.claude/skills/sc-recommend-protocol/SKILL.md:9-43`
- **E10:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/hooks/scripts/sc-recommend-phase0.sh:2-19`
