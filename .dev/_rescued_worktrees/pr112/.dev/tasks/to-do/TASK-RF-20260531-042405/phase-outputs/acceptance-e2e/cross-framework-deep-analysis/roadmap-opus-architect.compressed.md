---
spec_source: "spec-cross-framework-deep-analysis.compressed.md"
complexity_score: 0.85
complexity_class: HIGH
primary_persona: architect
adversarial: false
base_variant: "none"
variant_scores: "none"
convergence_score: none
---

# Cross-Framework Deep Analysis (IronClaude × llm-workflows) — Project Roadmap

## Executive Summary

This roadmap operationalizes an 8-phase analytical sprint that compares the IronClaude quality-enforcement layer (8 component groups) against the llm-workflows rigor stack (11 components), then synthesizes an actionable, schema-compliant improvement backlog. The work is pure analysis: zero production-code change, 35+ markdown artifacts, and a strict-sequential phase-gate contract that halts the sprint whenever a required artifact is missing or a coverage criterion fails. The architectural center of gravity is the phase-gate orchestration contract — every milestone's exit is a machine-checkable pass/fail gate, and the entire pipeline is restartable from any gate via the sprint CLI `--start` flag.

The dominant architectural risk is not implementation difficulty but cascade fragility: a weak Phase 1 inventory poisons every downstream strategy, comparison, and improvement decision. The design therefore front-loads evidence rigor (Auggie MCP as primary code-reader with a Serena+Grep/Glob fallback), enforces anti-sycophancy (every strength paired with a documented weakness), and applies the "adopt patterns not mass" R-RULE so the improvement plan adopts control/validation patterns from llm-workflows without importing its bash/shell machinery.

**Business Impact:** Produces a defensible, evidence-cited improvement backlog that ingests directly into `/sc:roadmap` v3.0 and a final plan that feeds `/sc:tasklist`, converting two large quality frameworks into a prioritized, traceable upgrade path for IronClaude's quality layer — with trivial rollback (delete the artifacts directory) and no blast radius on shipping code.

**Complexity:** HIGH (0.85) — 8 sequential gated phases, 35+ artifacts across two repositories, 19 components compared over 8 adversarial pairs, 100%-coverage verification NFRs, and a hard tooling dependency on Auggie MCP. Lowered from ~0.9 by zero production-code change, trivial rollback, and a frozen llm-workflows reference.

**Critical path:** M0 (gate infrastructure) → M1 (dual-framework inventory) → M2 (per-component strategy, both frameworks) → M3 (adversarial comparison) → M4 (merged synthesis) → M5 (improvement plan) → M6 (adversarial validation) → M7 (artifact assembly + backlog). Every arrow is a strict gate; no phase begins until the prior checkpoint passes.

**Key architectural decisions:**

- Phase-gate contract (`enforcement: strict_sequential`) is the primary orchestration mechanism — modeled as an explicit data contract (DM-002) with per-phase deterministic minima (DM-003), not as ad-hoc prose checks.
- Evidence sourcing is tool-mandated: Auggie MCP primary, Serena `get_symbols_overview` + Grep/Glob fallback, with degraded-mode annotation required in any artifact produced under fallback.
- Dual-output strategy: a multi-doc traceable artifact set AND a consolidated rigor-assessment + machine-readable improvement-backlog pair, decoupling human-traceability from downstream tool ingestion (DM-001 schema).

**Open risks requiring resolution before M1:**

- Canonical artifact root is ambiguous (`.dev/releases/current/cross-framework-deep-analysis/` vs bare `artifacts/...`); must be fixed in M0 before any artifact is written, or every downstream path reference drifts.

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|----|-------|------|----------|--------|--------------|--------------|------|
|M0|Sprint Foundation & Gate Infrastructure|Foundation|P0|S|—|3|MEDIUM|
|M1|Dual-Framework Component Inventory|Analysis|P0|L|M0|22|HIGH|
|M2|Per-Component Strategy Extraction (Both Frameworks)|Analysis|P0|XL|M1|2|MEDIUM|
|M3|Cross-Framework Adversarial Comparison|Analysis|P0|L|M2|9|MEDIUM|
|M4|Merged Strategy Synthesis|Analysis|P1|M|M3|2|MEDIUM|
|M5|Prioritized Improvement Plan|Analysis|P1|L|M4|2|HIGH|
|M6|Adversarial Validation of Improvement Plan|Quality|P0|M|M5|2|MEDIUM|
|M7|Artifact Assembly & Consolidated Outputs|Integration|P1|M|M6|2|MEDIUM|

## Dependency Graph

```
M0 (gate infra)
 └─> M1 (inventory: IC + LW)
      └─> M2 (strategy ×19: IC ×8 ‖ LW ×11)
           └─> M3 (adversarial comparison ×8 pairs)
                └─> M4 (merged strategy synthesis)
                     └─> M5 (prioritized improvement plan)
                          └─> M6 (adversarial validation)
                               └─> M7 (artifact assembly + backlog)
```

Notes: Within M2 the IC-strategy track (Phase 2) and LW-strategy track (Phase 3) are parallelizable, but BOTH gate M3. The phase-gate contract (DM-002) authored in M0 governs every arrow above; each arrow is a strict pass/fail checkpoint that halts the sprint on failure. Downstream of M7, `improvement-backlog.md` feeds `/sc:roadmap` and `final-improve-plan.md` feeds `/sc:tasklist` (external consumers, not milestones).

## M0: Sprint Foundation & Gate Infrastructure

**Objective:** Author the phase-gate contract and per-phase gate criteria, fix the canonical artifact root, and confirm restartability before any analysis artifact is written. | **Duration:** Week 1 (1 week) | **Entry:** Both repos accessible (`/config/workspace/IronClaude`, `/config/workspace/llm-workflows`); sprint CLI installed. | **Exit:** DM-002 + DM-003 authored and loaded by the sprint executor; artifact root fixed; `--start` resume verified on a no-op gate.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|DM-002|Phase-gate contract|Author the strict-sequential phase-gate enforcement contract that governs all 8 phase transitions; loaded by the sprint executor at launch.|COMP-003|—|enforcement:strict_sequential; rule:no_phase_starts_until_prior_checkpoint_passes; checkpoint_format:table_with_pass_fail_per_criterion; contract loaded by sprint CLI before Phase 1|S|P0|
|2|DM-003|Gate-criteria rows (×8)|Define the per-phase gate row for each of the 8 phases with deterministic artifact minima and semantic checks; governs gate enforcement over approximate "35+" counts.|COMP-003|DM-002|phase:enum(1..8); gate:string; min_artifacts:int per phase; semantic_checks:string per phase; all 8 rows present; minima govern halt logic|S|P0|
|3|NFR-XFDA.5|Sprint restartability|Verify the sprint is resumable from any phase gate via the CLI `--start` flag with incremental artifact writes for crash resilience.|COMP-003|DM-002|`--start <phase>` resumes at named gate; incremental writes flush per-artifact; resume verified on a no-op gate; mid-phase crash (exit -9 class) recoverable without rerun of passed phases|S|P0|

### Integration Points — M0

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|phase_gate_contract (DM-002)|Dispatch contract|M0|M0|sprint executor (COMP-003); every gate M1–M7|
|gate-criteria registry (DM-003)|Registry (8 rows)|M0|M0|phase-gate evaluator per phase|
|`--start` resume hook|CLI dispatch|M0|M0|operator restart after crash/halt|

### Milestone Dependencies — M0

- None (foundation milestone).

### Open Questions — M0

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OI-3|Does `FR-XFDA-001` need registration in an FR registry for v3.0 planning?|Low; administrative; blocks downstream roadmap generation if registry is mandatory|Roadmap owner|Before M7 roadmap handoff|
|2|OQ-ROOT|Canonical artifact root: `.dev/releases/current/cross-framework-deep-analysis/` vs bare `artifacts/...`?|High; every artifact path and traceability ref drifts if unresolved|Sprint lead|Before M1 (M0 exit)|
|3|OQ-PAIRSET|"≥8 comparison pairs" vs exactly-8 enumerated — are ad-hoc pairs permitted or is 8 the fixed set?|Medium; sets M3 gate min_artifacts and scope|Sprint lead|Before M3 gate definition (M0)|
|4|OQ-COUNTS|"35+ artifacts" approximate vs deterministic §5.2 per-phase minima — which governs gate enforcement?|Medium; gate halt logic depends on this|Sprint lead|M0 (resolved into DM-003)|

### Risk Assessment and Mitigation — M0

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Ambiguous artifact root causes path drift across all downstream refs|HIGH|Medium|Broken traceability; orphaned artifacts in M7|Fix canonical root in M0 (OQ-ROOT) before any write; encode in DM-003 paths|Sprint lead|
|2|Approximate "35+" artifact counts used for gate enforcement instead of deterministic minima|MEDIUM|Medium|Gate passes with missing artifacts|DM-003 deterministic per-phase minima govern; "35+" treated as informational only|Sprint lead|

## M1: Dual-Framework Component Inventory

**Objective:** Produce verified, evidence-backed inventories of all 8 IronClaude quality components and all 11 llm-workflows components, plus a cross-framework component map with ≥8 IC→LW mappings. | **Duration:** Weeks 2-3 (2 weeks) | **Entry:** M0 gate passed (DM-002/DM-003 loaded; artifact root fixed). | **Exit:** Phase 1 gate — `component-map.md` produced; ≥3 artifacts (2 inventories + map); ≥8 cross-framework mappings; ≥8 IC components inventoried; ≥11 LW components inventoried; every entry carries Auggie MCP evidence (or annotated fallback).

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-XFDA-001.1|Updated IronClaude component inventory|Inventory all 8 IC quality component groups into `inventory-ironclaude.md` with verified paths, interfaces, internal deps, extension points; build `component-map.md` with ≥8 IC→LW mappings.|COMP-003|DM-003|all 8 IC groups inventoried; each entry has file paths + interfaces + internal deps + extension points; no component without Auggie evidence; component-map ≥8 IC→LW mappings; IC-only components annotated|L|P0|
|2|FR-XFDA-001.2|llm-workflows component inventory (frozen reference)|Produce `inventory-llm-workflows.md` from the known list in `prompt.md`; Auggie verification query confirms each path; missing paths flagged + annotated.|COMP-003|DM-003|inventory produced from `prompt.md` known list; Auggie query confirms paths; any missing path flagged + annotated; ≥11 LW components present|M|P0|
|3|NFR-XFDA.1|Auggie-primary evidence compliance|Enforce Auggie MCP as the primary code-reading tool for all inventory tasks, with documented fallback when unavailable.|COMP-004|DM-003|100% of code-reading tasks use Auggie primary; R-RULE-01 checkpoint recorded per phase; fallback (Serena get_symbols_overview + Grep/Glob) annotated where used|S|P0|
|4|COMP-001|roadmap-pipeline inventory|Inventory IC roadmap generation + fidelity/remediate/certify quality gates.|cli/roadmap|FR-XFDA-001.1|path:`cli/roadmap/` (fidelity, remediate, certify, spec_patch, gates, executor); role:roadmap gen + quality gates; internal deps:gates,executor; extension points + Auggie evidence cited|M|P0|
|5|COMP-002|cleanup-audit-cli inventory|Inventory IC multi-pass structural repo audit with evidence gates.|cli/cleanup_audit|FR-XFDA-001.1|path:`cli/cleanup_audit/` (gates, anti-lazy, evidence-gate, executor, prompts); role:multi-pass structural audit; deps:executor,gates; extension points + Auggie evidence|M|P0|
|6|COMP-003|sprint-executor inventory|Inventory IC phase-gated sprint execution + resume subsystem.|cli/sprint|FR-XFDA-001.1|path:`cli/sprint/` (tmux, TUI, KPI, diagnostics, process, logging); role:phase-gated execution + resume; deps:tmux,process,logging; extension points + Auggie evidence|M|P0|
|7|COMP-004|pm-agent inventory|Inventory IC pre/post-execution confidence, validation, and error-learning components.|pm_agent|FR-XFDA-001.1|path:`pm_agent/` (confidence, self_check, reflexion, token_budget); role:confidence+validation+error learning; deps:—; extension points + Auggie evidence|M|P0|
|8|COMP-005|adversarial-pipeline inventory|Inventory IC structured adversarial debate/merge engine.|sc/adversarial|FR-XFDA-001.1|path:`.claude/commands/sc/adversarial.md` + `skills/sc-adversarial-protocol/`; role:adversarial debate/merge; deps:—; extension points + Auggie evidence|M|P0|
|9|COMP-006|task-unified inventory|Inventory IC tiered task execution + MCP-compliance component.|sc/task-unified|FR-XFDA-001.1|path:`.claude/commands/sc/task-unified.md` + `skills/sc-task-unified-protocol/`; role:tiered task exec + MCP compliance; deps:—; extension points + Auggie evidence|M|P0|
|10|COMP-007|quality-agents inventory|Inventory IC specialized quality/analysis agent definitions.|agents|FR-XFDA-001.1|path:`agents/` (quality-engineer, root-cause-analyst, pm-agent, requirements-analyst); role:quality/analysis agent defs; deps:—; extension points + Auggie evidence|M|P0|
|11|COMP-008|pipeline-analysis inventory|Inventory IC structural pipeline analysis subsystem (FMEA/guards/invariants).|cli/pipeline|FR-XFDA-001.1, OI-2|path:`cli/pipeline/` (FMEA, guards, invariants, contracts, dataflow, conflict); role:structural pipeline analysis; deps:—; group-vs-split decision recorded (OI-2); Auggie evidence|M|P0|
|12|COMP-009|pablov (LW) inventory|Inventory LW programmatic artifact-based LLM output validation.|.gfdoc/rules|FR-XFDA-001.2|path:`.gfdoc/rules/core/ib_agent_core.md`; role:programmatic artifact-based output validation; Auggie path-verify; flag if moved|S|P0|
|13|COMP-010|automated-qa-workflow (LW) inventory|Inventory LW automated QA orchestration script.|.gfdoc/scripts|FR-XFDA-001.2|path:`.gfdoc/scripts/automated_qa_workflow.sh`; role:automated QA orchestration; Auggie path-verify; flag if moved|S|P0|
|14|COMP-011|quality-gates (LW) inventory|Inventory LW structured quality-gate rules.|.gfdoc/rules|FR-XFDA-001.2|path:`.gfdoc/rules/core/quality_gates.md`; role:structured quality gate rules; Auggie path-verify; flag if moved|S|P0|
|15|COMP-012|anti-hallucination (LW) inventory|Inventory LW task-completion anti-hallucination rules.|.gfdoc/rules|FR-XFDA-001.2|path:`.gfdoc/rules/core/anti_hallucination_task_completion_rules.md`; role:task-completion anti-hallucination; Auggie path-verify; flag if moved|S|P0|
|16|COMP-013|anti-sycophancy (LW) inventory|Inventory LW 12-pattern risk scoring / anti-sycophancy ruleset.|.gfdoc/rules|FR-XFDA-001.2|path:`.gfdoc/rules/core/anti_sycophancy.md` + `RISK_PATTERNS_COMPREHENSIVE.md`; role:12-pattern risk scoring; Auggie path-verify; flag if moved|S|P0|
|17|COMP-014|dnsp-protocol (LW) inventory|Inventory LW Detect-Nudge-Synthesize-Proceed batch recovery guide.|.gfdoc/docs|FR-XFDA-001.2|path:`.gfdoc/docs/guides/RIGORFLOW_BATCH_STATE_FLOW_GUIDE.md`; role:DNSP batch recovery; Auggie path-verify; flag if moved|S|P0|
|18|COMP-015|session-management (LW) inventory|Inventory LW session/context rollover management scripts.|.gfdoc/scripts|FR-XFDA-001.2|path:`.gfdoc/scripts/session_message_counter.sh` + `rollover_context_functions.sh`; role:session/context rollover; Auggie path-verify; flag if moved|S|P0|
|19|COMP-016|input-validation (LW) inventory|Inventory LW input validation script.|.gfdoc/scripts|FR-XFDA-001.2|path:`.gfdoc/scripts/input_validation.sh`; role:input validation; Auggie path-verify; flag if moved|S|P0|
|20|COMP-017|pipeline-orchestration (LW) inventory|Inventory LW pipeline orchestration command.|rf/pipeline|FR-XFDA-001.2|path:`.claude/commands/rf/pipeline.md`; role:pipeline orchestration command; Auggie path-verify; flag if moved|S|P0|
|21|COMP-018|task-builder (LW) inventory|Inventory LW task builder command.|rf/taskbuilder|FR-XFDA-001.2|path:`.claude/commands/rf/taskbuilder.md`; role:task builder command; Auggie path-verify; flag if moved|S|P0|
|22|COMP-019|agent-definitions (LW) inventory|Inventory LW rf-* agent definitions.|rf/agents|FR-XFDA-001.2|path:`.claude/agents/rf-*.md`; role:rf-* agent definitions; Auggie path-verify; flag if moved|S|P0|

### Integration Points — M1

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|component-map.md|Cross-framework mapping registry|M1|M1|M2 strategy extraction; M3 comparison pairing|
|Auggie MCP evidence binding|Tool dispatch (primary→fallback)|M1|M1|every inventory entry; verified again in M6|

### Milestone Dependencies — M1

- Depends on M0: phase-gate contract (DM-002) and gate-criteria (DM-003) must be loaded; canonical artifact root (OQ-ROOT) fixed.

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OI-1|Do llm-workflows paths in `prompt.md` still match the current repo?|Medium; stale paths waste Phase 1 effort and corrupt LW inventory|Sprint lead|Phase 1 execution (T01.02)|
|2|OI-2|Treat pipeline-analysis (COMP-008) as one component group or split into sub-components for comparison?|Low; affects M3 comparison granularity|Architect|Before M2|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Auggie MCP unavailable for IronClaude repo|HIGH|Low|Inventory evidence gaps|Serena get_symbols_overview + Grep/Glob fallback; annotate limitation in artifacts|Sprint lead|
|2|Auggie MCP unavailable for llm-workflows repo|HIGH|Low|LW inventory evidence gaps|Same fallback; LW list partially known from `prompt.md`|Sprint lead|
|3|llm-workflows paths changed since `prompt.md` (GAP-1)|MEDIUM|Medium|Wasted Phase 1 effort; wrong file refs downstream|Phase 1 T01.02 verifies all LW paths; flag + annotate missing|Sprint lead|
|4|IC component inventory incomplete (fast-moving codebase)|MEDIUM|Medium|Cascade error into every downstream phase|Broad Auggie queries; M6 cross-checks all file refs|Architect|

## M2: Per-Component Strategy Extraction (Both Frameworks)

**Objective:** Produce strategy docs for all 8 IC component groups (Phase 2) and all 11 LW components (Phase 3), each pairing every strength with a documented weakness/cost and backing all claims with file:line Auggie evidence. | **Duration:** Weeks 4-6 (3 weeks) | **Entry:** M1 gate passed (inventories + component-map complete). | **Exit:** Phase 2 gate — all 8 `strategy-ic-*.md` produced, each with strength + weakness section; AND Phase 3 gate — all 11 `strategy-lw-*.md` produced, each noting rigorous AND bloat/cost.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-XFDA-001.3|Per-component strategy extraction|Produce 8 IC strategy docs (`strategy-ic-{component}.md`) and 11 LW strategy docs (`strategy-lw-{component}.md`); every strength paired with weakness/cost; all claims backed by file:line Auggie evidence; LW docs note rigorous AND bloated/slow/expensive.|cli/roadmap, .gfdoc|FR-XFDA-001.1, FR-XFDA-001.2|8 IC strategy docs (1 per COMP-001..008); 11 LW strategy docs (1 per COMP-009..019); every strength has paired weakness/cost; every claim has file:line Auggie evidence; LW docs flag rigor AND bloat/cost; no orphaned component|XL|P0|
|2|NFR-XFDA.2|Anti-sycophancy pairing enforcement|Enforce that every strength claim in every strategy doc carries a documented paired weakness/cost via a per-phase checkpoint scan.|COMP-013|FR-XFDA-001.3|100% of strength claims have paired weakness; checkpoint scan recorded per phase (Phase 2 + Phase 3); zero unpaired strengths at gate|M|P0|

### Integration Points — M2

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|strategy-ic-*.md (×8)|Per-component strategy set|M2|M2|M3 comparison pairs; M4 merged synthesis|
|strategy-lw-*.md (×11)|Per-component strategy set|M2|M2|M3 comparison pairs; M4 merged synthesis|
|anti-sycophancy checkpoint (NFR-2)|Strategy-pattern scan|M2|M2|gate evaluator (Phase 2 + Phase 3)|

### Milestone Dependencies — M2

- Depends on M1: both inventories and `component-map.md` (pairing source for IC↔LW strategy alignment).

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Strength claims emitted without paired weakness (sycophancy drift)|MEDIUM|Medium|Biased strategy docs poison comparison verdicts|NFR-2 per-phase checkpoint scan; gate halts on any unpaired strength|Quality lead|
|2|file:line citations unverifiable or hallucinated|MEDIUM|Medium|Evidence collapses under M6 verification, forcing rework|Auggie-primary sourcing; citations re-verified in M6 (NFR-3)|Architect|

## M3: Cross-Framework Adversarial Comparison

**Objective:** Debate the 8 enumerated comparison pairs via `/sc:adversarial`, each citing file:line from both repos and producing a clear conditioned verdict that verifies "adopt patterns not mass". | **Duration:** Weeks 7-8 (2 weeks) | **Entry:** M2 gate passed (all 19 strategy docs complete). | **Exit:** Phase 4 gate — all 8 `comparison-*.md` produced; each has a verdict + dual-repo file:line evidence; "adopt patterns not mass" verified per pair; inconclusive verdicts explicitly stated as "no clear winner" with rationale.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-XFDA-001.4|Cross-framework adversarial comparison|Debate ≥8 comparison pairs (set fixed in M0 via OQ-PAIRSET); each cites file:line from both repos and yields a clear conditioned verdict.|COMP-005|FR-XFDA-001.3, OQ-PAIRSET|≥8 pairs debated; each cites file:line from both repos; each yields verdict with conditions; "adopt patterns not mass" verified per pair; uses `/sc:adversarial`|L|P0|
|2|FR-XFDA-001.4a|Compare: roadmap gates vs PABLOV + quality-gates|Debate IC roadmap fidelity/certify/remediate gates against LW PABLOV + quality-gates.|COMP-005|FR-XFDA-001.4|`comparison-roadmap-gates-vs-pablov.md`; dual-repo file:line; verdict + conditions; patterns-not-mass verified|M|P0|
|3|FR-XFDA-001.4b|Compare: task-unified tiers vs pipeline-orchestration + task-builder|Debate IC task-unified tier system against LW pipeline-orchestration + task-builder.|COMP-005|FR-XFDA-001.4|`comparison-task-tiers-vs-orchestration.md`; dual-repo file:line; verdict + conditions; patterns-not-mass verified|M|P0|
|4|FR-XFDA-001.4c|Compare: sprint CLI executor vs automated-qa-workflow|Debate IC sprint CLI executor against LW automated-qa-workflow.|COMP-005|FR-XFDA-001.4|`comparison-sprint-vs-autoqa.md`; dual-repo file:line; verdict + conditions; patterns-not-mass verified|M|P0|
|5|FR-XFDA-001.4d|Compare: adversarial-pipeline vs anti-sycophancy system|Debate IC adversarial-pipeline against LW anti-sycophancy system.|COMP-005|FR-XFDA-001.4|`comparison-adversarial-vs-antisycophancy.md`; dual-repo file:line; verdict + conditions; patterns-not-mass verified|M|P0|
|6|FR-XFDA-001.4e|Compare: pm-agent vs anti-hallucination + failure-debugging|Debate IC pm-agent (confidence/reflexion/self-check) against LW anti-hallucination + failure-debugging.|COMP-005|FR-XFDA-001.4|`comparison-pmagent-vs-antihallucination.md`; dual-repo file:line; verdict + conditions; patterns-not-mass verified|M|P0|
|7|FR-XFDA-001.4f|Compare: quality-agents vs agent-definitions (rf-*)|Debate IC quality-agents against LW rf-* agent-definitions.|COMP-005|FR-XFDA-001.4|`comparison-qualityagents-vs-rfagents.md`; dual-repo file:line; verdict + conditions; patterns-not-mass verified|M|P0|
|8|FR-XFDA-001.4g|Compare: pipeline-analysis vs quality-gates + PABLOV (structural)|Debate IC pipeline-analysis (FMEA/guards/invariants) against LW quality-gates + PABLOV structural rules.|COMP-005|FR-XFDA-001.4, OI-2|`comparison-pipelineanalysis-vs-structural.md`; dual-repo file:line; verdict + conditions; patterns-not-mass verified; honors OI-2 split decision|M|P0|
|9|FR-XFDA-001.4h|Compare: cleanup-audit-cli vs automated-qa-workflow (audit)|Debate IC cleanup-audit-cli against LW automated-qa-workflow audit dimension.|COMP-005|FR-XFDA-001.4|`comparison-cleanupaudit-vs-autoqa.md`; dual-repo file:line; verdict + conditions; patterns-not-mass verified|M|P0|

### Integration Points — M3

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`/sc:adversarial` debate engine|Strategy-pattern dispatch|M3|M3|each of the 8 comparison pairs|
|comparison-*.md (×8)|Verdict set|M3|M3|M4 merged synthesis; M6 human-review spot-check|

### Milestone Dependencies — M3

- Depends on M2: all 19 strategy docs. Depends on M0: OQ-PAIRSET resolution fixes the pair set and M3 gate min_artifacts.

### Open Questions — M3

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|GAP-2|How is a "discard both" comparison verdict handled when it feeds M5?|Low; accepted — "discard both" is a valid M4 outcome documented as "no adoption; why"|Architect|M4 entry|

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Comparison pairs produce inconclusive verdicts|MEDIUM|Medium|Forced/false conclusions bias M4 synthesis|Require explicit "no clear winner" verdict with rationale rather than forcing a conclusion|Architect|
|2|Pair set ambiguity ("≥8" vs exactly 8)|MEDIUM|Medium|Gate under/over-counts comparisons|OQ-PAIRSET fixed in M0; M3 gate min_artifacts derived from it|Sprint lead|

## M4: Merged Strategy Synthesis

**Objective:** Synthesize a single `merged-strategy.md` covering all Phase 4 component areas, with an explicit "rigor without bloat" section, "patterns not mass" applied and documented per adopted pattern, and justified discard decisions. | **Duration:** Week 9 (1 week) | **Entry:** M3 gate passed (all 8 comparisons with verdicts). | **Exit:** Phase 5 gate — `merged-strategy.md` produced; has "rigor without bloat" section; no component area orphaned; internally consistent; discard decisions justified.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-XFDA-001.5|Merged strategy synthesis|Synthesize `merged-strategy.md` from all comparison verdicts; explicit "rigor without bloat" section; "patterns not mass" applied + documented per adopted pattern; discard decisions justified; internally consistent.|cli/roadmap|FR-XFDA-001.4|covers all Phase 4 component areas; explicit "rigor without bloat" section; patterns-not-mass documented per adopted pattern; discard decisions justified incl. "discard both" (GAP-2); internally consistent; no orphaned area|M|P1|
|2|NFR-XFDA.4|"Patterns not mass" verification|Verify "adopt patterns not mass" for every llm-workflows adoption recorded in the merged strategy.|COMP-008|FR-XFDA-001.5|100% of adoption items verified patterns-not-mass; control/validation patterns adopted, never bash/shell machinery; checkpoint recorded; re-checked in M5/M6|M|P1|

### Integration Points — M4

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|merged-strategy.md|Synthesis document|M4|M4|M5 improvement plan; M6 missing-connection check (Phase 5→6)|
|patterns-not-mass ledger (NFR-4)|Adoption registry|M4|M4|M5 per-item rationale; M6 scope-creep check|

### Milestone Dependencies — M4

- Depends on M3: all 8 comparison verdicts (including any "no clear winner" / "discard both" outcomes).

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Adoption drifts toward importing LW machinery (mass not patterns)|MEDIUM|Medium|Bloated, non-portable recommendations|NFR-4 checkpoint; record only control/validation patterns; bash/shell machinery excluded by R-RULE|Architect|
|2|Component area orphaned in synthesis|MEDIUM|Low|Incomplete coverage breaks traceability|Gate requires every Phase 4 area represented; cross-check against component-map|Architect|

## M5: Prioritized Improvement Plan

**Objective:** Produce per-component improvement plans for all 8 IC groups plus an `improve-master.md` with dependency graph, each item carrying file path(s), change, why, priority, effort, dependencies, risk, and acceptance criteria, distinguishing new-code from strengthen-existing. | **Duration:** Weeks 10-11 (2 weeks) | **Entry:** M4 gate passed (merged-strategy complete). | **Exit:** Phase 6 gate — 9 plans (8 component + master); each item has P-tier + effort + file path; "patterns not mass" verified; `improve-master.md` has dependency graph.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-XFDA-001.6|Prioritized improvement plan|Produce 8 `improve-{component}.md` + `improve-master.md` with dependency graph; each item: file path(s), change, why, priority P0–P3, effort XS–XL, dependencies, risk, acceptance criteria; new-code vs strengthen-existing distinguished.|cli/roadmap|FR-XFDA-001.5|per-component plans for all 8 IC groups; each item has file path(s)+change+why+priority(P0–P3)+effort(XS–XL)+deps+AC+risk; `improve-master.md` dependency graph; new-code vs strengthen-existing distinguished|L|P1|
|2|DM-001|improvement_backlog item schema|Define the machine-readable backlog row schema emitted per improvement item for `/sc:roadmap` ingestion.|cli/roadmap|FR-XFDA-001.6|id:string(IC-{component}-{seq}); component:string; title:string; priority:enum(P0,P1,P2,P3); effort:enum(XS,S,M,L,XL); pattern_source:string(LW pattern or "IC-native"); rationale:string; file_targets:list[string]; acceptance_criteria:list[string]; risk:string; patterns_not_mass_verified:bool|M|P1|

### Integration Points — M5

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|improve-master.md|Dependency graph|M5|M5|M6 validation; M7 backlog assembly|
|improvement_backlog item (DM-001)|Schema-bound row|M5|M5|M7 `improvement-backlog.md`; `/sc:roadmap` (downstream)|

### Milestone Dependencies — M5

- Depends on M4: merged-strategy + patterns-not-mass ledger (each adopted pattern maps to ≥1 improvement item).

### Risk Assessment and Mitigation — M5

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Phase 6 plans drift into implementation mass|HIGH|Medium|Scope creep; non-portable recommendations|"patterns not mass" R-RULE at checkpoint + M6 adversarial check|Architect|
|2|Backlog rows non-conformant to DM-001 schema|MEDIUM|Medium|`/sc:roadmap` ingestion fails in M7|Author rows against DM-001 from the start; M6 + M7 validate schema|Architect|

## M6: Adversarial Validation of Improvement Plan

**Objective:** Adversarially validate every improvement item (pass/fail), verify all file paths via Auggie, run scope-creep and missing-connection (Phase 5→6) checks, and produce a corrected final plan. | **Duration:** Week 12 (1 week) | **Entry:** M5 gate passed (9 plans + DM-001 rows). | **Exit:** Phase 7 gate — `validation-report.md` + `final-improve-plan.md`; pass/fail per item; final plan corrects all failures.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-XFDA-001.7|Adversarial validation of improvement plan|Produce `validation-report.md` with pass/fail per item; verify all file paths via Auggie; scope-creep check vs "patterns not mass"; missing-connection check (Phase 5→6); emit corrected `final-improve-plan.md`.|COMP-005|FR-XFDA-001.6|pass/fail per item; all file paths Auggie-verified; scope-creep check vs patterns-not-mass; missing-connection check Phase 5→6; corrected final plan produced|M|P0|
|2|NFR-XFDA.3|Citation verifiability|Verify 100% of file:line citations across all artifacts are resolvable via Auggie in the validation phase.|COMP-005|FR-XFDA-001.7|100% of citations verifiable; Auggie verification run in Phase 7; unresolved citations fail the owning item|M|P0|

### Integration Points — M6

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|validation-report.md|Pass/fail ledger|M6|M6|M7 rigor-assessment; corrective loop into final plan|
|final-improve-plan.md|Corrected plan|M6|M6|M7 assembly; `/sc:tasklist` (downstream)|

### Milestone Dependencies — M6

- Depends on M5: 9 improvement plans + DM-001 rows (the validation subject set).

### Risk Assessment and Mitigation — M6

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|file:line citations fail verification at scale|MEDIUM|Medium|Items fail; rework loop extends schedule|NFR-3 100% Auggie re-verification; Auggie-primary sourcing upstream reduces failure rate|Quality lead|
|2|Scope-creep items survive validation|HIGH|Low|Mass-not-patterns recommendations ship to backlog|Dedicated scope-creep check vs patterns-not-mass; failed items corrected in final plan|Architect|

## M7: Artifact Assembly & Consolidated Outputs

**Objective:** Assemble `artifact-index.md` linking all artifacts with end-to-end traceability, produce the rigor assessment, the sc:roadmap-compatible improvement backlog, and the sprint summary, with no orphans or dead refs. | **Duration:** Week 13 (1 week) | **Entry:** M6 gate passed (validation-report + final-improve-plan). | **Exit:** Phase 8 gate — 4 consolidated outputs (index + assessment + backlog + summary); `improvement-backlog.md` is sc:roadmap-compatible; full traceability with no orphans/dead refs.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-XFDA-001.8|Artifact assembly & consolidated outputs|Produce `artifact-index.md` (links all artifacts), `rigor-assessment.md`, `improvement-backlog.md` (sc:roadmap-compatible), `sprint-summary.md`; ensure end-to-end traceability (component→strategy→comparison→merged→improvement); no orphans/dead refs.|cli/roadmap|FR-XFDA-001.7|`artifact-index.md` links all artifacts; end-to-end traceability Phase 1→improvement; no orphans/dead refs; rigor-assessment + sc:roadmap-compatible backlog + sprint-summary produced|M|P1|
|2|NFR-XFDA.6|Backlog schema interoperability|Verify `improvement-backlog.md` is directly consumable by `/sc:roadmap` against the `improvement_backlog_schema`.|cli/roadmap|FR-XFDA-001.8, DM-001|backlog conforms to improvement_backlog_schema; ingests into `/sc:roadmap` without schema errors; manual review recorded (GAP-3 accepted risk)|M|P1|

### Integration Points — M7

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|artifact-index.md|Traceability link registry|M7|M7|human review; audit of end-to-end chain|
|improvement-backlog.md|Schema-bound export (DM-001)|M7|M7|`/sc:roadmap` v3.0 (downstream consumer)|
|final-improve-plan.md handoff|Sequencing export|M7|M6→M7|`/sc:tasklist` (downstream consumer)|

### Milestone Dependencies — M7

- Depends on M6: `validation-report.md` + `final-improve-plan.md` (corrected, validated inputs to the consolidated outputs).

### Open Questions — M7

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|GAP-3|`improvement-backlog.md` schema is unvalidated by existing test tooling — is manual review sufficient?|Medium; accepted risk — manual review in Phase 8 stands in for automated schema validation|Quality lead|M7 exit|

### Risk Assessment and Mitigation — M7

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|`improvement-backlog.md` schema unvalidated by test tooling (GAP-3)|MEDIUM|Medium|Schema error surfaces only at `/sc:roadmap` ingestion|DM-001 schema authored in M5; manual review in M7; trial ingestion into `/sc:roadmap`|Quality lead|
|2|Orphaned artifacts or dead references in the index|MEDIUM|Low|Traceability claim fails end-to-end check|`artifact-index.md` cross-checks every artifact against producing phase; dead-ref scan at gate|Sprint lead|

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By Milestone|Status|Fallback|
|---|---|---|---|
|Auggie MCP (primary code-reader)|M1, M2, M6|Hard dependency|Serena get_symbols_overview + Grep/Glob; annotate degraded mode|
|Serena MCP (get_symbols_overview)|M1 (fallback)|Available|Grep/Glob secondary fallback|
|Grep/Glob tooling|M1 (fallback)|Available|Manual file enumeration|
|superclaude sprint CLI executor|M0–M7 (all gates)|Available|None — required for phase-gate execution + `--start` resume|
|`/sc:adversarial` debate engine|M3, M6|Available|Manual adversarial review (degraded)|
|`/sc:roadmap` v3.0|Post-M7 (consumer)|External consumer|N/A — validated via trial ingestion in M7|
|`/sc:tasklist`|Post-M6 (consumer)|External consumer|N/A — sequencing handoff only|
|External repos: `/config/workspace/IronClaude` (target), `/config/workspace/llm-workflows` (frozen reference)|M1+|Available|None — both required for dual-repo evidence|

### Infrastructure Requirements

- Read access to both repositories; llm-workflows treated as frozen (path verification only, no implementation changes).
- Sprint CLI environment with tmux/TUI, KPI, diagnostics, and logging (COMP-003) for phase-gated execution and crash-resilient incremental writes.
- Canonical artifact root (fixed in M0) with write access; trivial rollback = delete the artifacts directory.
- Reference inputs available: `artifacts/prompt.md` (LW component list), `.dev/releases/backlog/2.25-roadmap-v5/v2.25-spec-merged.md` (rigor-gap evidence), `src/superclaude/examples/release-spec-template.md` (spec template).

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|Mitigation|Owner|
|----|------|---------------------|-------------|--------|------------|-------|
|R1|Auggie MCP unavailable for IronClaude repo|M1, M2, M6|Low|High|Serena get_symbols_overview + Grep/Glob fallback; annotate limitation|Sprint lead|
|R2|Auggie MCP unavailable for llm-workflows repo|M1, M2|Low|High|Same fallback; LW list partially known from `prompt.md`|Sprint lead|
|R3|llm-workflows paths changed since `prompt.md` (GAP-1)|M1|Medium|Medium|Phase 1 T01.02 verifies all LW paths; flag + annotate missing|Sprint lead|
|R4|Comparison pairs produce inconclusive verdicts|M3|Medium|Medium|Require explicit "no clear winner" verdict with rationale|Architect|
|R5|Phase 6 plans drift into implementation mass|M4, M5|Medium|High|"patterns not mass" R-RULE at checkpoint + M6 adversarial check|Architect|
|R6|Sprint crashes mid-phase (exit -9 class)|M0–M7|Low|Medium|Phase-gate checkpoints enable `--start` resume; incremental writes|Sprint lead|
|R7|IC component inventory incomplete (fast-moving codebase)|M1|Medium|Medium|Broad Auggie queries; M6 cross-checks all file refs|Architect|
|R8|GAP-1: LW path validity not pre-verified|M1|Medium|Medium|Phase 1 T01.02 verification gate|Sprint lead|
|R9|GAP-2: no explicit handling for "discard both" verdict feeding M5|M3, M5|Low|Low|Accepted — "discard both" documented as valid M4 outcome ("no adoption; why")|Architect|
|R10|GAP-3: `improvement-backlog.md` schema unvalidated by test tooling|M7|Medium|Medium|Accepted — manual review in M7 + trial `/sc:roadmap` ingestion|Quality lead|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|Milestone|
|---|---|---|---|---|
|Phase 1 inventory complete|Artifacts + mappings|≥3 artifacts; ≥8 IC→LW mappings; ≥8 IC + ≥11 LW components|Phase 1 gate scan|M1|
|IC strategy coverage|strategy-ic-*.md|8/8 with strength+weakness section|Phase 2 gate scan|M2|
|LW strategy coverage|strategy-lw-*.md|11/11 with rigor+bloat/cost section|Phase 3 gate scan|M2|
|Comparison coverage|comparison-*.md|8/8 with verdict + dual-repo file:line|Phase 4 gate scan|M3|
|Merged synthesis integrity|merged-strategy.md|"rigor without bloat" section; no orphaned area|Phase 5 gate scan|M4|
|Improvement plan completeness|9 plans|8 component + master; P-tier+effort+file path per item|Phase 6 gate scan|M5|
|Validation completeness|validation-report + final plan|pass/fail per item; final corrects all failures|Phase 7 gate scan|M6|
|Consolidated outputs|4 outputs|index+assessment+backlog+summary; sc:roadmap-compatible|Phase 8 gate scan|M7|
|Auggie-primary compliance (NFR-1)|% code-reading tasks|100%|R-RULE-01 checkpoint per phase|M1|
|Anti-sycophancy pairing (NFR-2)|% strength claims paired|100%|Checkpoint scan per phase|M2|
|Citation verifiability (NFR-3)|% citations resolvable|100%|Auggie verification in Phase 7|M6|
|Patterns-not-mass (NFR-4)|% adoption items verified|100%|Phase 6 + Phase 7 checkpoints|M4|
|Sprint restartability (NFR-5)|`--start` resume|Works from any gate|CLI executor resume test|M0|
|Backlog schema interoperability (NFR-6)|Schema compliance|Ingests into `/sc:roadmap` without errors|Phase 8 validation|M7|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|----------|--------|------------------------|----------|
|Orchestration model|Strict-sequential phase-gate via sprint CLI (DM-002)|Interactive/manual process; parallel-all phases|AC-1 mandate; cascade risk from bad Phase 1 demands gated halts; restartability needs deterministic gates|
|Milestone decomposition|8 milestones (M0 foundation + M1–M7 = 8 spec phases)|Per-phase 1:1 (no M0); merge Phases 2&3 into separate milestones|FR-XFDA-001.3 explicitly spans Phases 2&3 (one ID); M0 needed to fix artifact root + author gate contract before any write|
|Evidence sourcing|Auggie MCP primary + Serena/Grep-Glob fallback|Grep/Glob only; Serena only|AC-6/NFR-1 mandate Auggie primary; fallback preserves progress under MCP outage (R1/R2)|
|pipeline-analysis granularity|Deferred to OI-2 (resolve before M2)|Force single group now; force split now|Affects M3 comparison granularity; premature lock risks wrong comparison scope|
|Backlog validation|Manual review + trial `/sc:roadmap` ingestion (GAP-3 accepted)|Block on new automated schema test tooling|No existing test tooling validates the schema; manual + trial ingestion is sufficient for an analysis sprint with trivial rollback|

## Timeline Estimates

|Milestone|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M0|1 week|Week 1|Week 1|Gate contract (DM-002) + criteria (DM-003) loaded; artifact root fixed; `--start` verified|
|M1|2 weeks|Week 2|Week 3|2 inventories + component-map; ≥8 IC→LW mappings; all 19 COMP rows evidenced|
|M2|3 weeks|Week 4|Week 6|8 IC + 11 LW strategy docs; anti-sycophancy pairing 100%|
|M3|2 weeks|Week 7|Week 8|8 comparison verdicts with dual-repo file:line evidence|
|M4|1 week|Week 9|Week 9|merged-strategy.md; "rigor without bloat"; patterns-not-mass ledger|
|M5|2 weeks|Week 10|Week 11|9 improvement plans + dependency graph; DM-001 backlog rows|
|M6|1 week|Week 12|Week 12|validation-report + final-improve-plan; citations 100% verified|
|M7|1 week|Week 13|Week 13|4 consolidated outputs; sc:roadmap-compatible backlog; full traceability|

**Total estimated duration:** 13 weeks
