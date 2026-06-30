---
spec_source: "spec-cross-framework-deep-analysis.compressed.md"
complexity_score: 0.85
complexity_class: HIGH
primary_persona: architect
adversarial: false
base_variant: "none"
variant_scores: "none"
convergence_score: null
---
# Cross-Framework Deep Analysis — Project Roadmap

## Executive Summary

Deliver a phase-gated analytical sprint that inventories IronClaude and llm-workflows quality-enforcement systems, extracts per-component strategies, compares them adversarially, synthesizes an evidence-backed “rigor without bloat” strategy, and emits downstream-ready improvement artifacts for `/sc:roadmap` and `/sc:tasklist`.

**Business Impact:** Converts a broad cross-framework research effort into a restartable, auditable improvement pipeline that strengthens IronClaude quality gates while avoiding wholesale import of llm-workflows machinery.

**Complexity:** HIGH (0.85) — 8 sequential phases, 35+ artifacts, two repositories, 19 components, 8 adversarial comparison pairs, and 100% evidence/anti-sycophancy/pattern-adoption verification targets.

**Critical path:** M1 inventories and contracts → M2 strategy extraction → M3 adversarial comparisons → M4 synthesis and improvement plan → M5 validation, assembly, and downstream handoff.

**Key architectural decisions:**

- Use strict sequential sprint gates as the control plane, with Phases 2 and 3 parallelized only within the M2 boundary.
- Treat llm-workflows as a frozen reference: verify paths, extract patterns, and avoid implementation-mass adoption.
- Make `improvement-backlog.md` the machine-readable downstream interface and `final-improve-plan.md` the execution-sequencing interface.

**Open risks requiring resolution before M1:**

- Confirm canonical artifact root before sprint launch because extraction cites both bare `artifacts/...` paths and `.dev/releases/current/cross-framework-deep-analysis/`.

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|---|---|---|---|---|---|---|---|
|M1|Inventory, Contracts, and Artifact Root|Foundation|P0|2w|-|23|HIGH|
|M2|Evidence-Based Strategy Extraction|Analysis|P0|3w|M1|4|HIGH|
|M3|Adversarial Cross-Framework Comparison|Analysis|P0|2w|M2|9|MEDIUM|
|M4|Synthesis and Improvement Planning|Planning|P0|3w|M3|4|HIGH|
|M5|Validation, Assembly, and Downstream Readiness|Validation|P0|2w|M4|5|MEDIUM|

## Dependency Graph

M1 → M2 → M3 → M4 → M5

M1: FR-XFDA-001.1, FR-XFDA-001.2, COMP-001..COMP-019, DM-002, DM-003 → M2: FR-XFDA-001.3, NFR-XFDA.1..3 → M3: FR-XFDA-001.4, FR-XFDA-001.4a..h → M4: FR-XFDA-001.5, FR-XFDA-001.6, NFR-XFDA.4, DM-001 → M5: FR-XFDA-001.7, FR-XFDA-001.8, NFR-XFDA.5, NFR-XFDA.6, FR-XFDA-001

## M1: Inventory, Contracts, and Artifact Root

**Objective:** Establish verified component inventories, artifact-root decision, and phase-gate/data contracts. | **Duration:** Weeks 1-2 (2w) | **Entry:** sprint spec approved; repo paths accessible; artifact root resolved | **Exit:** IC+LW inventories, component map, gate contracts, and field contracts accepted

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-XFDA-001.1|IronClaude inventory|Inventory all 8 IronClaude quality component groups with verified paths, interfaces, dependencies, extension points, and IC-only annotations.|Inventory pipeline|OI-4|8 groups; verified paths; interfaces; dependencies; extension points; ≥8 IC→LW mappings; no unevidenced component|L|P0|
|2|FR-XFDA-001.2|llm-workflows inventory|Produce stable-reference inventory from `artifacts/prompt.md`, verify paths, and annotate missing references.|Inventory pipeline|OI-1, OI-4|inventory file produced; Auggie path query complete; missing paths flagged; stable-reference status noted|M|P0|
|3|COMP-001|roadmap-pipeline component|Inventory roadmap generation, fidelity, remediate, certify, spec_patch, gates, and executor surfaces.|IronClaude component|FR-XFDA-001.1|name:roadmap-pipeline; source_path:`cli/roadmap/`; role:roadmap generation+quality gates; dependencies:gates,executor; source_ref:§4.5|M|P0|
|4|COMP-002|cleanup-audit-cli component|Inventory cleanup audit gates, anti-lazy checks, evidence gate, executor, and prompts.|IronClaude component|FR-XFDA-001.1|name:cleanup-audit-cli; source_path:`cli/cleanup_audit/`; role:multi-pass structural audit; dependencies:executor,gates; source_ref:§4.5|M|P1|
|5|COMP-003|sprint-executor component|Inventory sprint tmux, TUI, KPI, diagnostics, process, logging, phase gate, and resume surfaces.|IronClaude component|FR-XFDA-001.1|name:sprint-executor; source_path:`cli/sprint/`; role:phase-gated sprint execution+resume; dependencies:tmux,process,logging; source_ref:§4.5+§5.1|M|P0|
|6|COMP-004|pm-agent component|Inventory confidence, self_check, reflexion, and token_budget quality controls.|IronClaude component|FR-XFDA-001.1|name:pm-agent; source_path:`pm_agent/`; role:confidence/self-check/reflexion/token budget; dependencies:dash; source_ref:§4.5|S|P0|
|7|COMP-005|adversarial-pipeline component|Inventory adversarial command and skill package used for debate and merge workflows.|IronClaude component|FR-XFDA-001.1|name:adversarial-pipeline; source_path:`.claude/commands/sc/adversarial.md`+`skills/sc-adversarial-protocol/`; role:debate/merge; dependencies:dash; source_ref:§4.5|S|P0|
|8|COMP-006|task-unified component|Inventory tiered task execution and MCP compliance command/skill surfaces.|IronClaude component|FR-XFDA-001.1|name:task-unified; source_path:`.claude/commands/sc/task-unified.md`+`skills/sc-task-unified-protocol/`; role:tiered task execution; dependencies:dash; source_ref:§4.5|S|P1|
|9|COMP-007|quality-agents component|Inventory quality-engineer, root-cause-analyst, pm-agent, and requirements-analyst definitions.|IronClaude component|FR-XFDA-001.1|name:quality-agents; source_path:`agents/`; role:specialized quality/analysis agents; dependencies:dash; source_ref:§4.5|S|P1|
|10|COMP-008|pipeline-analysis component|Inventory FMEA, guards, invariants, contracts, dataflow, and conflict subsystem boundaries.|IronClaude component|FR-XFDA-001.1, OI-2|name:pipeline-analysis; source_path:`cli/pipeline/`; role:structural pipeline analysis; dependencies:dash; source_ref:§4.5|M|P1|
|11|COMP-009|pablov reference|Inventory Programmatic Artifact-Based LLM Output Validation as LW reference pattern.|LW component|FR-XFDA-001.2|name:pablov; source_path:`.gfdoc/rules/core/ib_agent_core.md`; role:artifact-based output validation; dependencies:dash; source_ref:§4.5+App.A|S|P0|
|12|COMP-010|automated-qa-workflow reference|Inventory automated QA workflow orchestration as LW reference pattern.|LW component|FR-XFDA-001.2|name:automated-qa-workflow; source_path:`.gfdoc/scripts/automated_qa_workflow.sh`; role:automated QA orchestration; dependencies:dash; source_ref:§4.5|S|P1|
|13|COMP-011|quality-gates reference|Inventory llm-workflows structured quality gate rules.|LW component|FR-XFDA-001.2|name:quality-gates; source_path:`.gfdoc/rules/core/quality_gates.md`; role:structured quality gates; dependencies:dash; source_ref:§4.5|S|P0|
|14|COMP-012|anti-hallucination reference|Inventory task-completion anti-hallucination rules.|LW component|FR-XFDA-001.2|name:anti-hallucination; source_path:`.gfdoc/rules/core/anti_hallucination_task_completion_rules.md`; role:task-completion anti-hallucination; dependencies:dash; source_ref:§4.5|S|P1|
|15|COMP-013|anti-sycophancy reference|Inventory risk patterns and anti-sycophancy system.|LW component|FR-XFDA-001.2|name:anti-sycophancy; source_path:`.gfdoc/rules/core/anti_sycophancy.md`+`RISK_PATTERNS_COMPREHENSIVE.md`; role:12-pattern risk scoring; dependencies:dash; source_ref:§1.1+§4.5|S|P0|
|16|COMP-014|dnsp-protocol reference|Inventory Detect-Nudge-Synthesize-Proceed batch recovery protocol.|LW component|FR-XFDA-001.2|name:dnsp-protocol; source_path:`.gfdoc/docs/guides/RIGORFLOW_BATCH_STATE_FLOW_GUIDE.md`; role:batch recovery protocol; dependencies:dash; source_ref:§4.5+App.A|S|P2|
|17|COMP-015|session-management reference|Inventory session message counter and rollover context functions.|LW component|FR-XFDA-001.2|name:session-management; source_path:`.gfdoc/scripts/session_message_counter.sh`+`rollover_context_functions.sh`; role:session/context rollover; dependencies:dash; source_ref:§4.5|S|P2|
|18|COMP-016|input-validation reference|Inventory llm-workflows input validation script behavior.|LW component|FR-XFDA-001.2|name:input-validation; source_path:`.gfdoc/scripts/input_validation.sh`; role:input validation; dependencies:dash; source_ref:§4.5|S|P2|
|19|COMP-017|pipeline-orchestration reference|Inventory rf pipeline orchestration command as LW reference.|LW component|FR-XFDA-001.2|name:pipeline-orchestration; source_path:`.claude/commands/rf/pipeline.md`; role:pipeline orchestration command; dependencies:dash; source_ref:§4.5|S|P1|
|20|COMP-018|task-builder reference|Inventory rf task builder command as LW reference.|LW component|FR-XFDA-001.2|name:task-builder; source_path:`.claude/commands/rf/taskbuilder.md`; role:task builder command; dependencies:dash; source_ref:§4.5|S|P1|
|21|COMP-019|agent-definitions reference|Inventory rf-* agent definition family as LW reference.|LW component|FR-XFDA-001.2|name:agent-definitions; source_path:`.claude/agents/rf-*.md`; role:rf-* agent definitions; dependencies:dash; source_ref:§4.5|S|P1|
|22|DM-002|phase-gate contract|Define strict sequential phase-gate contract for sprint control flow.|Gate contract|OI-4|enforcement:strict_sequential; rule:no_phase_starts_until_prior_checkpoint_passes; checkpoint_format:table_with_pass_fail_per_criterion|S|P0|
|23|DM-003|gate criteria row|Define per-phase gate criteria row contract used for the 8 phase checkpoints.|Gate contract|DM-002|phase:value; gate:value; min_artifacts:int; semantic_checks:string|S|P0|

### Integration Points — M1

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|component-map.md|Mapping registry|Yes|M1|M2 strategy extraction; M3 comparison pair routing; M4 orphan checks|
|phase_gate_contract|Gate contract|Yes|M1|Sprint executor; all checkpoint pass/fail tables|
|gate-criteria row|Checkpoint schema|Yes|M1|Phase gate validator; M5 assembly validator|
|artifact root decision|Path contract|Yes|M1|All artifact writers; artifact-index.md|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Auggie MCP unavailable for IronClaude repo|HIGH|Low|Inventory lacks primary evidence|Use Serena `get_symbols_overview` plus Grep/Glob fallback; label limitation in artifacts|Architecture lead|
|2|Auggie MCP unavailable for llm-workflows repo|HIGH|Low|Reference inventory loses verification depth|Use known `prompt.md` list plus Serena/Grep/Glob fallback; label limitation|Architecture lead|
|3|Artifact root ambiguity causes artifact drift|MEDIUM|Medium|Writers and validators disagree on paths|Resolve OI-4 before first artifact write; record root in component map|Sprint owner|
|4|IC component inventory incomplete|MEDIUM|Medium|Later comparisons miss quality surfaces|Run broad repository queries and M5 file-reference cross-checks|Architecture lead|

### Milestone Dependencies — M1

- External repos `/config/workspace/IronClaude` and `/config/workspace/llm-workflows` must be readable.
- Auggie MCP is primary; Serena MCP and Grep/Glob are fallback discovery tools.
- `artifacts/prompt.md` must be available for stable LW reference inventory.

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OI-1|Do llm-workflows paths in `prompt.md` still match the current repo?|Blocks reliable LW inventory and Phase 4 dual-repo evidence|Architecture lead|Before M1 exit|
|2|OI-2|Treat pipeline-analysis as one component group or split into sub-components?|Affects COMP-008 extraction depth and comparison granularity|Architecture lead|Before M1 exit|
|3|OI-3|Does `FR-XFDA-001` need registration in an FR registry for v3.0 planning?|Affects administrative traceability before downstream roadmap ingestion|Sprint owner|Before M1 exit|
|4|OI-4|What is the canonical artifact root: bare `artifacts/...` or `.dev/releases/current/cross-framework-deep-analysis/`?|Blocks artifact writer and validator path contracts|Sprint owner|Before M1 start|

## M2: Evidence-Based Strategy Extraction

**Objective:** Extract balanced strategy documents for all scoped components with Auggie-first evidence and explicit strength/weakness pairing. | **Duration:** Weeks 3-5 (3w) | **Entry:** M1 component map and artifact root accepted | **Exit:** 8 IC and 11 LW strategy docs accepted with evidence, weaknesses, and checkpoint scans

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-XFDA-001.3|Per-component strategy extraction|Create IC and LW strategy docs for every scoped component, pairing each strength with weakness/cost and citing file:line evidence.|Strategy extraction|M1|8 IC docs; 11 LW docs; strength+weakness paired; file:line evidence; LW rigor+bloat/cost noted|XL|P0|
|2|NFR-XFDA.1|Auggie-primary code reading|Ensure all code-reading tasks use Auggie MCP as the primary evidence tool.|Evidence control|M1|100% phases record Auggie query; fallback use labeled; R-RULE-01 checkpoint passes|M|P0|
|3|NFR-XFDA.2|Anti-sycophancy pairing|Ensure every stated strength has a paired weakness or cost.|Quality rule|FR-XFDA-001.3|100% strength claims paired; checkpoint scan passes; unpaired claims fixed before exit|M|P0|
|4|NFR-XFDA.3|Citation verifiability|Ensure all file:line citations remain verifiable before downstream validation.|Evidence control|FR-XFDA-001.3|100% citations recorded; source repo noted; Phase 7 verification-ready index emitted|M|P0|

### Integration Points — M2

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|strategy-ic-{component}.md|Strategy artifact family|Yes|M2|M3 comparison pairs; M4 merged strategy|
|strategy-lw-{component}.md|Strategy artifact family|Yes|M2|M3 comparison pairs; M4 discard/adopt decisions|
|Auggie evidence index|Evidence registry|Yes|M2|M3 dual-repo citations; M5 validation report|
|anti-sycophancy scan results|Quality checkpoint|Yes|M2|M3 verdict confidence; M5 rigor assessment|

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Strategy docs become one-sided advocacy|HIGH|Medium|Adversarial comparisons inherit biased inputs|Enforce NFR-XFDA.2 before M2 exit; reject unpaired strength claims|Architecture lead|
|2|Citation quality varies across repos|HIGH|Medium|Phase 7 verification burden increases|Centralize citation index and require source repo label for every claim|Evidence owner|
|3|LW docs overfit to shell implementation details|MEDIUM|Medium|M4 adoption plan drifts into mass import|Record pattern-level learning and implementation-mass exclusions in each LW doc|Architecture lead|

### Milestone Dependencies — M2

- M1 component-map.md and artifact-root decision must be complete.
- Auggie MCP must be attempted for every code-reading task; fallback output must be marked.
- Phase 2 and Phase 3 workstreams may run in parallel inside this milestone but both must finish before M3.

## M3: Adversarial Cross-Framework Comparison

**Objective:** Debate the eight required IC↔LW component pairs and produce conditional verdicts backed by dual-repo evidence. | **Duration:** Weeks 6-7 (2w) | **Entry:** M2 strategy docs and evidence index accepted | **Exit:** 8 comparison artifacts accepted with verdicts, conditions, and adoption-boundary notes

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-XFDA-001.4|Adversarial comparison set|Run the required comparison set through `/sc:adversarial`, producing evidence-backed verdicts with conditions.|Adversarial pipeline|M2, OI-5|≥8 comparisons; dual-repo file:line evidence; verdict+conditions; adoption boundary verified|XL|P0|
|2|FR-XFDA-001.4a|Roadmap gates comparison|Compare roadmap fidelity/certify/remediate gates against PABLOV and quality-gates.|Adversarial pair|FR-XFDA-001.4|IC evidence cited; LW evidence cited; verdict; conditions; adopt-patterns-not-mass note|M|P0|
|3|FR-XFDA-001.4b|Task tier comparison|Compare task-unified tier system against pipeline-orchestration and task-builder.|Adversarial pair|FR-XFDA-001.4|IC evidence cited; LW evidence cited; verdict; conditions; tier implications noted|M|P0|
|4|FR-XFDA-001.4c|Sprint executor comparison|Compare sprint CLI executor against automated-qa-workflow.|Adversarial pair|FR-XFDA-001.4|IC evidence cited; LW evidence cited; verdict; conditions; resume implications noted|M|P0|
|5|FR-XFDA-001.4d|Adversarial systems comparison|Compare adversarial-pipeline against anti-sycophancy system.|Adversarial pair|FR-XFDA-001.4|IC evidence cited; LW evidence cited; verdict; conditions; bias-control implications noted|M|P0|
|6|FR-XFDA-001.4e|PM-agent comparison|Compare pm-agent confidence/reflexion/self-check against anti-hallucination and failure-debugging patterns.|Adversarial pair|FR-XFDA-001.4|IC evidence cited; LW evidence cited; verdict; conditions; validation-loop implications noted|M|P1|
|7|FR-XFDA-001.4f|Quality agent comparison|Compare quality-agents against rf-* agent-definitions.|Adversarial pair|FR-XFDA-001.4|IC evidence cited; LW evidence cited; verdict; conditions; agent-boundary implications noted|M|P1|
|8|FR-XFDA-001.4g|Pipeline analysis comparison|Compare pipeline-analysis FMEA/guards/invariants against quality-gates and PABLOV structural patterns.|Adversarial pair|FR-XFDA-001.4|IC evidence cited; LW evidence cited; verdict; conditions; structural-control implications noted|M|P1|
|9|FR-XFDA-001.4h|Cleanup audit comparison|Compare cleanup-audit-cli against automated-qa-workflow audit dimension.|Adversarial pair|FR-XFDA-001.4|IC evidence cited; LW evidence cited; verdict; conditions; audit-control implications noted|M|P1|

### Integration Points — M3

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|comparison-{pair}.md|Comparison artifact family|Yes|M3|M4 merged-strategy decisions|
|comparison pair registry|Dispatch table|Yes|M3|Adversarial run selection; M5 traceability checks|
|verdict condition matrix|Decision registry|Yes|M3|M4 adoption/discard plan; M5 validation report|
|dual-repo citation map|Evidence registry|Yes|M3|M5 citation verification|

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Comparison pairs produce inconclusive verdicts|MEDIUM|Medium|M4 synthesis lacks clear direction|Allow explicit “no clear winner” verdict with rationale and conditions|Adversarial lead|
|2|Adversarial output favors framework mass over patterns|HIGH|Medium|Improvement plan violates scope boundary|Require adoption-boundary note in every pair artifact and M4 pattern filter|Architecture lead|
|3|Pair count ambiguity causes unplanned work expansion|MEDIUM|Medium|Schedule and validation scope drift|Resolve OI-5 before M3 exit; treat extra pairs as approved only if explicitly accepted|Sprint owner|

### Milestone Dependencies — M3

- All 8 IC and 11 LW strategy docs must be accepted.
- `/sc:adversarial` must be available for structured debate/merge comparisons.
- The M2 evidence index must supply dual-repo citations for every pair.

### Open Questions — M3

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OI-5|Are the 8 enumerated comparison pairs fixed, or may additional ad-hoc pairs be added?|Affects M3 scope, M4 synthesis coverage, and timeline discipline|Sprint owner|Before M3 exit|

## M4: Synthesis and Improvement Planning

**Objective:** Convert comparison verdicts into a merged strategy and prioritized IronClaude improvement plan that adopts patterns without implementation mass. | **Duration:** Weeks 8-10 (3w) | **Entry:** M3 comparison artifacts accepted | **Exit:** merged strategy, 8 component plans, master dependency graph, and backlog schema accepted

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-XFDA-001.5|Merged strategy synthesis|Create `merged-strategy.md` covering all Phase 4 component areas with explicit rigor-without-bloat and discard-decision rationale.|Strategy synthesis|M3|all comparison areas covered; rigor without bloat section; adopted patterns documented; discard decisions justified; no orphaned area|L|P0|
|2|FR-XFDA-001.6|Prioritized improvement plan|Create 8 component plans and master plan with priorities, effort, file targets, dependencies, acceptance criteria, and risk per item.|Improvement planning|FR-XFDA-001.5|8 improve docs; master dependency graph; P0-P3; XS-XL; file paths; risks; new-code vs strengthen-existing marked|XL|P0|
|3|NFR-XFDA.4|Patterns-not-mass verification|Verify every llm-workflows adoption item extracts a transferable pattern and excludes shell or framework mass.|Adoption control|FR-XFDA-001.6|100% adoption items verified; Phase 6 checkpoint passes; Phase 7 review-ready evidence recorded|M|P0|
|4|DM-001|Improvement backlog item contract|Define the machine-readable backlog row contract consumed by `/sc:roadmap`.|Backlog schema|FR-XFDA-001.6|id:string(IC-{component}-{seq}); component:string; title:string; priority:enum(P0,P1,P2,P3); effort:enum(XS,S,M,L,XL); pattern_source:string(LW pattern or IC-native); rationale:string; file_targets:list[string]; acceptance_criteria:list[string]; risk:string; patterns_not_mass_verified:bool|M|P0|

### Integration Points — M4

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|merged-strategy.md|Synthesis artifact|Yes|M4|FR-XFDA-001.6 plans; M5 rigor assessment|
|improve-{component}.md|Plan artifact family|Yes|M4|final-improve-plan.md; `/sc:tasklist` handoff|
|improve-master.md|Dependency graph|Yes|M4|M5 validation; downstream sequencing|
|improvement_backlog item|Schema contract|Yes|M4|improvement-backlog.md; `/sc:roadmap` ingestion|
|patterns-not-mass checklist|Adoption guard|Yes|M4|M5 adversarial validation|

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Phase 6 plans drift into implementation mass|HIGH|Medium|Adoption violates core scope rule|Require NFR-XFDA.4 checklist per item and reject mass-import language before exit|Architecture lead|
|2|Discard-both verdicts lack follow-through|LOW|Medium|M4 may force unnecessary adoption|Represent discard-both as “no adoption; why” in merged strategy and plan gap notes|Architecture lead|
|3|Plan items lack file paths or acceptance criteria|HIGH|Medium|M5 cannot validate downstream readiness|Apply DM-001 field completeness check before M4 exit|Planning owner|

### Milestone Dependencies — M4

- M3 verdict condition matrix must be complete.
- All M3 comparison artifacts must cite both repositories or document why dual evidence is unavailable.
- The M1 artifact-root decision must be applied consistently to all plan artifacts.

## M5: Validation, Assembly, and Downstream Readiness

**Objective:** Validate every improvement item, assemble traceable consolidated outputs, and prove downstream roadmap/tasklist compatibility. | **Duration:** Weeks 11-12 (2w) | **Entry:** M4 merged strategy, component plans, master plan, and backlog schema accepted | **Exit:** validation report, final plan, artifact index, rigor assessment, backlog, and sprint summary accepted

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-XFDA-001.7|Improvement plan validation|Validate every plan item for path accuracy, scope discipline, Phase 5→6 linkage, pass/fail status, and corrections.|Validation pipeline|M4|pass/fail per item; all paths verified; scope-creep check; missing-connection check; corrected final plan produced|L|P0|
|2|FR-XFDA-001.8|Consolidated output assembly|Assemble artifact index, rigor assessment, improvement backlog, and sprint summary with end-to-end traceability.|Assembly pipeline|FR-XFDA-001.7, OI-6|artifact-index links all; traceability complete; no orphans; rigor assessment; backlog; sprint summary|L|P0|
|3|NFR-XFDA.5|Sprint restartability|Ensure sprint can resume from any phase gate via `--start` and preserves incremental artifacts.|Sprint executor|DM-002|`--start` works; phase gate resume verified; crash recovery documented; artifacts retained|M|P0|
|4|NFR-XFDA.6|Roadmap backlog compatibility|Ensure `improvement-backlog.md` is directly consumable by `/sc:roadmap` without schema errors.|Backlog schema|DM-001|schema-compliant; `/sc:roadmap` ingestion succeeds; validation errors absent|M|P0|
|5|FR-XFDA-001|Feature acceptance closure|Validate completion traceability for the full cross-framework deep-analysis feature across all eight phase requirements.|Assembly pipeline|FR-XFDA-001.8|8 child FRs traced; 6 NFRs validated; 19 components covered; 3 contracts covered; artifact index complete|M|P0|

### Integration Points — M5

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|validation-report.md|Validation artifact|Yes|M5|final-improve-plan.md; risk register evidence|
|final-improve-plan.md|Execution plan|Yes|M5|`/sc:tasklist`|
|artifact-index.md|Traceability index|Yes|M5|Human review; audit trail|
|rigor-assessment.md|Assessment report|Yes|M5|Release decision; improvement backlog rationale|
|improvement-backlog.md|Downstream backlog|Yes|M5|`/sc:roadmap`|
|sprint-summary.md|Sprint summary|Yes|M5|Stakeholder handoff; restart notes|

### Risk Assessment and Mitigation — M5

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Sprint crashes mid-phase|MEDIUM|Low|Validation or assembly must resume cleanly|Use phase-gate checkpoints, `--start`, and incremental artifact writes|Sprint owner|
|2|Backlog schema remains manually validated only|MEDIUM|Medium|Downstream `/sc:roadmap` ingestion may fail late|Run schema review against DM-001 and perform ingestion dry check before exit|Validation owner|
|3|Artifact count ambiguity weakens gate enforcement|MEDIUM|Medium|Validators may chase approximate totals|Use deterministic §5.2 phase minimums as the authoritative gate checks|Validation owner|

### Milestone Dependencies — M5

- M4 plans and backlog contract must be complete.
- `/sc:roadmap` and `/sc:tasklist` interfaces must be available for downstream compatibility checks.
- Sprint executor resume behavior must be observable through `--start` gate selection.

### Open Questions — M5

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OI-6|Should gate enforcement use approximate “35+ artifacts” or deterministic per-phase minimums from §5.2?|Affects final validation standard and artifact-index completeness checks|Validation owner|Before M5 exit|

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By Milestone|Status|Fallback|
|---|---|---|---|
|Auggie MCP|M1-M5|Required primary evidence tool|Serena `get_symbols_overview` plus Grep/Glob with limitation notes|
|Serena MCP|M1-M5|Fallback discovery tool|Grep/Glob searches with limitation notes|
|Grep/Glob tooling|M1-M5|Fallback discovery and verification support|Manual source review with limitation notes|
|superclaude sprint CLI executor|M1-M5|Required execution control plane|Manual phase log only for incident diagnosis, not gate bypass|
|`/sc:adversarial`|M3|Required comparison engine|Architect-led debate transcript with explicit limitation note|
|`/sc:roadmap`|M5|Required backlog consumer|Schema review against DM-001 if command unavailable|
|`/sc:tasklist`|M5|Required final-plan consumer|Manual tasklist conversion with limitation note|
|External repositories|M1-M5|IronClaude target and llm-workflows frozen reference|Abort or defer affected phase if repo unreadable|

### Infrastructure Requirements

- Read access to `/config/workspace/IronClaude` and `/config/workspace/llm-workflows` for evidence collection.
- Writable artifact root resolved by OI-4 before M1 execution.
- Sprint executor environment with phase-gate checkpoint persistence and `--start` resume support.
- MCP access for Auggie primary retrieval and Serena fallback discovery.
- Downstream command availability for `/sc:roadmap` and `/sc:tasklist` compatibility checks.

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|R-001|Auggie MCP unavailable for IronClaude repo|M1,M2,M3,M5|Low|High|Use Serena plus Grep/Glob fallback; label evidence limitations|Architecture lead|
|R-002|Auggie MCP unavailable for llm-workflows repo|M1,M2,M3,M5|Low|High|Use known `prompt.md` list plus fallback discovery; label evidence limitations|Architecture lead|
|R-003|llm-workflows paths changed since `prompt.md`|M1,M3|Medium|Medium|Verify all LW paths in M1; flag and annotate missing paths|Architecture lead|
|R-004|Artifact root ambiguity causes artifact drift|M1,M4,M5|Medium|Medium|Resolve OI-4 before first write; apply root consistently in index and validators|Sprint owner|
|R-005|IC component inventory incomplete|M1,M2,M3|Medium|Medium|Run broad repository queries and M5 file-reference cross-checks|Architecture lead|
|R-006|Strategy docs become one-sided advocacy|M2,M3,M4|Medium|High|Enforce anti-sycophancy pairing before M2 exit|Architecture lead|
|R-007|Citation quality varies across repos|M2,M3,M5|Medium|High|Centralize citation index and source repo labels|Evidence owner|
|R-008|LW docs overfit to shell implementation details|M2,M4|Medium|Medium|Record pattern-level learning and implementation-mass exclusions|Architecture lead|
|R-009|Comparison pairs produce inconclusive verdicts|M3,M4|Medium|Medium|Allow explicit no-clear-winner verdicts with rationale and conditions|Adversarial lead|
|R-010|Adversarial output favors framework mass over patterns|M3,M4,M5|Medium|High|Require adoption-boundary notes and pattern filter checks|Architecture lead|
|R-011|Pair count ambiguity causes unplanned work expansion|M3|Medium|Medium|Resolve OI-5 before M3 exit|Sprint owner|
|R-012|Phase 6 plans drift into implementation mass|M4,M5|Medium|High|Require NFR-XFDA.4 checklist per item and reject mass-import language|Architecture lead|
|R-013|Discard-both verdicts lack follow-through|M4|Medium|Low|Represent discard-both as no adoption with rationale|Architecture lead|
|R-014|Plan items lack file paths or acceptance criteria|M4,M5|Medium|High|Apply DM-001 field completeness check before M4 exit|Planning owner|
|R-015|Sprint crashes mid-phase|M5|Low|Medium|Use phase gates, `--start`, and incremental artifact writes|Sprint owner|
|R-016|Backlog schema remains manually validated only|M5|Medium|Medium|Run DM-001 schema review and `/sc:roadmap` ingestion check|Validation owner|
|R-017|Artifact count ambiguity weakens gate enforcement|M5|Medium|Medium|Use deterministic §5.2 phase minimums as authoritative|Validation owner|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|Milestone|
|---|---|---|---|---|
|Phase 1 gate|Inventory artifacts and mappings|≥3 artifacts; ≥8 mappings; ≥8 IC; ≥11 LW|Checkpoint table and artifact index|M1|
|Phase 2 gate|IC strategy coverage|8 `strategy-ic-*.md`; strength+weakness sections|Checkpoint scan|M2|
|Phase 3 gate|LW strategy coverage|11 `strategy-lw-*.md`; rigor and cost sections|Checkpoint scan|M2|
|Phase 4 gate|Comparison coverage|8 `comparison-*.md`; verdict and file:line evidence|Adversarial output review|M3|
|Phase 5 gate|Merged strategy quality|`merged-strategy.md`; rigor-without-bloat; no orphaned area|Synthesis review|M4|
|Phase 6 gate|Improvement plan coverage|9 plans; P-tier; effort; file paths; pattern verification|Plan completeness review|M4|
|Phase 7 gate|Validation outputs|`validation-report.md`; `final-improve-plan.md`; corrections applied|Pass/fail item review|M5|
|Phase 8 gate|Consolidated outputs|4 outputs; backlog compatible with `/sc:roadmap`|Assembly and ingestion check|M5|
|Auggie primary compliance|Auggie usage rate|100% code-reading tasks|R-RULE-01 checkpoint per phase|M1-M5|
|Anti-sycophancy pairing|Paired strength claims|100%|Checkpoint scan|M2-M5|
|Citation verifiability|Verified citations|100%|M5 Auggie verification pass|M5|
|Pattern adoption discipline|Verified adoption items|100%|Phase 6 checklist plus Phase 7 adversarial validation|M4-M5|
|Sprint restartability|Resume gate command|`--start` works from any phase gate|Sprint executor resume check|M5|
|Backlog schema compliance|Roadmap ingestion|No schema errors|`/sc:roadmap` compatibility check|M5|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|---|---|---|---|
|Execution control plane|Strict sequential sprint gates|Manual process; fully parallel phases|Sequential gates reduce cascade risk and preserve restartability while allowing bounded M2 parallel work|
|llm-workflows handling|Frozen reference with path verification|Full re-survey; implementation import|Frozen reference lowers discovery cost and enforces pattern-only adoption|
|Adoption filter|Patterns not mass|Import shell machinery; ignore LW patterns|Maintains IronClaude architecture while capturing reusable validation logic|
|Backlog interface|DM-001 `improvement_backlog` item|Free-form markdown only; separate tracker|Machine-readable contract makes `/sc:roadmap` ingestion testable|
|Comparison verdict handling|Allow conditional and no-clear-winner verdicts|Force winners for every pair|Avoids false certainty and supports discard-both outcomes|
|Artifact count authority|Deterministic §5.2 minimums|Approximate “35+ artifacts” total|Per-phase minimums are testable and prevent count ambiguity|

## Timeline Estimates

|Milestone|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1|2w|Week 1|Week 2|Artifact root; IC/LW inventories; component map; gate contracts|
|M2|3w|Week 3|Week 5|8 IC strategy docs; 11 LW strategy docs; evidence index|
|M3|2w|Week 6|Week 7|8 adversarial comparison artifacts; verdict matrix|
|M4|3w|Week 8|Week 10|merged-strategy.md; 8 improve docs; improve-master.md; backlog contract|
|M5|2w|Week 11|Week 12|validation report; final plan; artifact index; backlog; sprint summary|

**Total estimated duration:** 12 weeks
