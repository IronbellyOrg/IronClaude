---
spec_source: "spec-cross-framework-deep-analysis.compressed.md"
complexity_score: 0.85
complexity_class: HIGH
primary_persona: architect
adversarial: true
base_variant: "sonnet-architect"
variant_scores: "A(opus-architect):86 B(sonnet-architect):87"
convergence_score: 0.74
---
# Cross-Framework Deep Analysis (IronClaude × llm-workflows) — Project Roadmap

## Executive Summary

Deliver a phase-gated analytical sprint that inventories the IronClaude quality-enforcement layer (8 component groups) and the llm-workflows rigor stack (11 components), extracts per-component strategies with paired strengths and weaknesses, compares them adversarially across 8 enumerated IC↔LW pairs, synthesizes an evidence-backed "rigor without bloat" strategy, and emits downstream-ready improvement artifacts for `/sc:roadmap` and `/sc:tasklist`. The work is pure analysis: zero production-code change, 35+ markdown artifacts, two repositories, and a strict-sequential phase-gate contract that halts whenever a required artifact is missing or a coverage criterion fails. The control plane is the sprint executor's gate contract (DM-002) plus per-phase deterministic minima (DM-003); the entire pipeline is restartable from any gate via the CLI `--start` flag — a property proven early on a no-op gate at sprint launch and re-validated under real phase state at closing.

The dominant architectural risk is not implementation difficulty but cascade fragility: a weak M1 inventory poisons every downstream strategy, comparison, and improvement decision. The design front-loads evidence rigor (Auggie MCP primary with a Serena `get_symbols_overview` + Grep/Glob fallback), enforces anti-sycophancy (every strength paired with a documented weakness/cost), and applies the "adopt patterns not mass" rule so the improvement plan imports llm-workflows control/validation patterns without dragging in its bash/shell machinery.

**Business Impact:** Converts two large quality frameworks into a restartable, auditable, evidence-cited improvement pipeline that strengthens IronClaude's quality gates while avoiding wholesale import of llm-workflows machinery. The machine-readable `improvement-backlog.md` ingests directly into `/sc:roadmap` v3.0 and `final-improve-plan.md` sequences `/sc:tasklist` — with trivial rollback (delete the artifacts directory) and no blast radius on shipping code.

**Complexity:** HIGH (0.85) — 8 sequential gated phases, 35+ artifacts across two repositories, 19 components compared over 8 adversarial pairs, 100% evidence/anti-sycophancy/pattern-adoption verification targets, and a hard tooling dependency on Auggie MCP. Lowered from ~0.9 by zero production-code change, trivial rollback, and a frozen llm-workflows reference.

**Critical path:** M1 (inventories + contracts + artifact root + early resume smoke test) → M2 (per-component strategy extraction, both frameworks) → M3 (adversarial comparison ×8 pairs) → M4 (merged synthesis + prioritized improvement plan) → M5 (independent P0 validation → assembly → downstream-readiness). Every arrow is a strict pass/fail checkpoint that halts the sprint on failure; the 8 §5.2 phase gates persist inside the 5 milestone wrappers.

**Key architectural decisions:**

- Strict-sequential sprint gates are the control plane (DM-002), with Phases 2 and 3 parallelized only within the M2 boundary; per-phase deterministic minima (DM-003) govern halt logic over the approximate "35+" count.
- Foundation discipline: phase-gate and field contracts (DM-002/DM-003) are authored before the gates they govern, and a `--start` resume smoke test runs on a no-op gate at sprint launch (graft from Variant A) while full restartability validation (NFR-XFDA.5) remains at M5.
- Evidence sourcing is tool-mandated (Auggie MCP primary, Serena + Grep/Glob fallback with degraded-mode annotation); llm-workflows is a frozen reference (path verification only); `improvement-backlog.md` is the machine-readable downstream interface and `final-improve-plan.md` the execution-sequencing interface.

**Open risks requiring resolution before M1:**

- Canonical artifact root is ambiguous (`.dev/releases/current/cross-framework-deep-analysis/` vs bare `artifacts/...`); OI-4 must be fixed before the first artifact write or every downstream path reference and traceability claim drifts.

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|----|-------|------|----------|--------|--------------|--------------|------|
|M1|Inventory, Contracts, and Artifact Root|Foundation|P0|2w|—|24|HIGH|
|M2|Evidence-Based Strategy Extraction|Analysis|P0|3w|M1|4|HIGH|
|M3|Adversarial Cross-Framework Comparison|Analysis|P0|2w|M2|9|MEDIUM|
|M4|Synthesis and Improvement Planning|Planning|P0|3w|M3|4|HIGH|
|M5|Validation, Assembly, and Downstream Readiness|Validation|P0|2w|M4|5|MEDIUM|

## Dependency Graph

```
M1 (inventory IC+LW · contracts DM-002/DM-003 · artifact root · early --start smoke test)
 └─> M2 (strategy ×19: IC ×8 ‖ LW ×11, anti-sycophancy + Auggie evidence)
      └─> M3 (adversarial comparison ×8 pairs, dual-repo file:line verdicts)
           └─> M4 (merged synthesis + prioritized improvement plan + DM-001 backlog schema)
                └─> M5 (P0 validation gate → assembly → downstream readiness)
```

M1: FR-XFDA-001.1, FR-XFDA-001.2, COMP-001..COMP-019, DM-002, DM-003, NFR-XFDA.5a → M2: FR-XFDA-001.3, NFR-XFDA.1..3 → M3: FR-XFDA-001.4, FR-XFDA-001.4a..h → M4: FR-XFDA-001.5, FR-XFDA-001.6, NFR-XFDA.4, DM-001 → M5: FR-XFDA-001.7, FR-XFDA-001.8, NFR-XFDA.5, NFR-XFDA.6, FR-XFDA-001. Within M2 the IC-strategy track (Phase 2) and LW-strategy track (Phase 3) are parallelizable but BOTH gate M3. The independent P0 validation boundary (FR-XFDA-001.7) must close before assembly (FR-XFDA-001.8) begins inside M5. Downstream of M5, `improvement-backlog.md` feeds `/sc:roadmap` and `final-improve-plan.md` feeds `/sc:tasklist` (external consumers, not milestones).

## M1: Inventory, Contracts, and Artifact Root

**Objective:** Establish verified component inventories for both frameworks, fix the canonical artifact root, author the phase-gate and field contracts before the gates they govern, and prove restartability early on a no-op gate. | **Duration:** Weeks 1-2 (2w) | **Entry:** sprint spec approved; both repos accessible (`/config/workspace/IronClaude`, `/config/workspace/llm-workflows`); sprint CLI installed; artifact root resolved (OI-4). | **Exit:** IC+LW inventories, component map (≥8 IC→LW mappings), gate contracts (DM-002/DM-003) accepted and loaded by the executor; `--start` resume verified on a no-op gate.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-XFDA-001.1|IronClaude inventory|Inventory all 8 IronClaude quality component groups into `inventory-ironclaude.md` with verified paths, interfaces, internal deps, extension points, IC-only annotations; build `component-map.md` with ≥8 IC→LW mappings.|Inventory pipeline|OI-4|all 8 IC groups inventoried; verified paths + interfaces + internal deps + extension points per entry; ≥8 IC→LW mappings; no component without Auggie evidence; IC-only components annotated|L|P0|
|2|FR-XFDA-001.2|llm-workflows inventory (frozen reference)|Produce `inventory-llm-workflows.md` from the `artifacts/prompt.md` known list; Auggie path query confirms each path; missing paths flagged + annotated; frozen-reference status noted.|Inventory pipeline|OI-1, OI-4|inventory produced from `prompt.md` list; Auggie query confirms paths; ≥11 LW components present; any missing path flagged + annotated; frozen-reference noted|M|P0|
|3|COMP-001|roadmap-pipeline component|Inventory IC roadmap generation + fidelity/remediate/certify/spec_patch/gates/executor surfaces.|cli/roadmap|FR-XFDA-001.1|name:roadmap-pipeline; source_path:`cli/roadmap/`; role:roadmap generation+quality gates; internal_deps:gates,executor; extension_points:cited; Auggie_evidence:cited; source_ref:§4.5|M|P0|
|4|COMP-002|cleanup-audit-cli component|Inventory IC multi-pass structural repo audit: gates, anti-lazy, evidence-gate, executor, prompts.|cli/cleanup_audit|FR-XFDA-001.1|name:cleanup-audit-cli; source_path:`cli/cleanup_audit/`; role:multi-pass structural audit; internal_deps:executor,gates; extension_points:cited; Auggie_evidence:cited; source_ref:§4.5|M|P1|
|5|COMP-003|sprint-executor component|Inventory IC phase-gated sprint execution + resume subsystem: tmux, TUI, KPI, diagnostics, process, logging, phase gate, resume.|cli/sprint|FR-XFDA-001.1|name:sprint-executor; source_path:`cli/sprint/`; role:phase-gated sprint execution+resume; internal_deps:tmux,process,logging; extension_points:cited; Auggie_evidence:cited; source_ref:§4.5+§5.1|M|P0|
|6|COMP-004|pm-agent component|Inventory IC pre/post-execution confidence, validation, error-learning, and token-budget controls.|pm_agent|FR-XFDA-001.1|name:pm-agent; source_path:`pm_agent/`; role:confidence/self_check/reflexion/token_budget; internal_deps:—; extension_points:cited; Auggie_evidence:cited; source_ref:§4.5|S|P0|
|7|COMP-005|adversarial-pipeline component|Inventory IC structured adversarial debate/merge command + skill package.|sc/adversarial|FR-XFDA-001.1|name:adversarial-pipeline; source_path:`.claude/commands/sc/adversarial.md`+`skills/sc-adversarial-protocol/`; role:debate/merge; internal_deps:—; extension_points:cited; Auggie_evidence:cited; source_ref:§4.5|S|P0|
|8|COMP-006|task-unified component|Inventory IC tiered task execution + MCP-compliance command + skill surfaces.|sc/task-unified|FR-XFDA-001.1|name:task-unified; source_path:`.claude/commands/sc/task-unified.md`+`skills/sc-task-unified-protocol/`; role:tiered task execution+MCP compliance; internal_deps:—; extension_points:cited; Auggie_evidence:cited; source_ref:§4.5|S|P1|
|9|COMP-007|quality-agents component|Inventory IC specialized quality/analysis agent definitions.|agents|FR-XFDA-001.1|name:quality-agents; source_path:`agents/` (quality-engineer, root-cause-analyst, pm-agent, requirements-analyst); role:specialized quality/analysis agents; internal_deps:—; extension_points:cited; Auggie_evidence:cited; source_ref:§4.5|S|P1|
|10|COMP-008|pipeline-analysis component|Inventory IC structural pipeline analysis subsystem: FMEA, guards, invariants, contracts, dataflow, conflict.|cli/pipeline|FR-XFDA-001.1, OI-2|name:pipeline-analysis; source_path:`cli/pipeline/`; role:structural pipeline analysis; internal_deps:—; extension_points:cited; group-vs-split decision recorded (OI-2); Auggie_evidence:cited; source_ref:§4.5|M|P1|
|11|COMP-009|pablov reference (LW)|Inventory LW Programmatic Artifact-Based LLM Output Validation as reference pattern.|.gfdoc/rules|FR-XFDA-001.2|name:pablov; source_path:`.gfdoc/rules/core/ib_agent_core.md`; role:artifact-based output validation; internal_deps:—; Auggie_path_verify; flag if moved; source_ref:§4.5+App.A|S|P0|
|12|COMP-010|automated-qa-workflow reference (LW)|Inventory LW automated QA orchestration script as reference pattern.|.gfdoc/scripts|FR-XFDA-001.2|name:automated-qa-workflow; source_path:`.gfdoc/scripts/automated_qa_workflow.sh`; role:automated QA orchestration; internal_deps:—; Auggie_path_verify; flag if moved; source_ref:§4.5|S|P1|
|13|COMP-011|quality-gates reference (LW)|Inventory LW structured quality-gate rules.|.gfdoc/rules|FR-XFDA-001.2|name:quality-gates; source_path:`.gfdoc/rules/core/quality_gates.md`; role:structured quality gate rules; internal_deps:—; Auggie_path_verify; flag if moved; source_ref:§4.5|S|P0|
|14|COMP-012|anti-hallucination reference (LW)|Inventory LW task-completion anti-hallucination rules.|.gfdoc/rules|FR-XFDA-001.2|name:anti-hallucination; source_path:`.gfdoc/rules/core/anti_hallucination_task_completion_rules.md`; role:task-completion anti-hallucination; internal_deps:—; Auggie_path_verify; flag if moved; source_ref:§4.5|S|P1|
|15|COMP-013|anti-sycophancy reference (LW)|Inventory LW 12-pattern risk scoring / anti-sycophancy ruleset.|.gfdoc/rules|FR-XFDA-001.2|name:anti-sycophancy; source_path:`.gfdoc/rules/core/anti_sycophancy.md`+`RISK_PATTERNS_COMPREHENSIVE.md`; role:12-pattern risk scoring; internal_deps:—; Auggie_path_verify; flag if moved; source_ref:§1.1+§4.5|S|P0|
|16|COMP-014|dnsp-protocol reference (LW)|Inventory LW Detect-Nudge-Synthesize-Proceed batch recovery protocol.|.gfdoc/docs|FR-XFDA-001.2|name:dnsp-protocol; source_path:`.gfdoc/docs/guides/RIGORFLOW_BATCH_STATE_FLOW_GUIDE.md`; role:DNSP batch recovery protocol; internal_deps:—; Auggie_path_verify; flag if moved; source_ref:§4.5+App.A|S|P2|
|17|COMP-015|session-management reference (LW)|Inventory LW session/context rollover management scripts.|.gfdoc/scripts|FR-XFDA-001.2|name:session-management; source_path:`.gfdoc/scripts/session_message_counter.sh`+`rollover_context_functions.sh`; role:session/context rollover; internal_deps:—; Auggie_path_verify; flag if moved; source_ref:§4.5|S|P2|
|18|COMP-016|input-validation reference (LW)|Inventory LW input validation script behavior.|.gfdoc/scripts|FR-XFDA-001.2|name:input-validation; source_path:`.gfdoc/scripts/input_validation.sh`; role:input validation; internal_deps:—; Auggie_path_verify; flag if moved; source_ref:§4.5|S|P2|
|19|COMP-017|pipeline-orchestration reference (LW)|Inventory LW rf pipeline orchestration command.|rf/pipeline|FR-XFDA-001.2|name:pipeline-orchestration; source_path:`.claude/commands/rf/pipeline.md`; role:pipeline orchestration command; internal_deps:—; Auggie_path_verify; flag if moved; source_ref:§4.5|S|P1|
|20|COMP-018|task-builder reference (LW)|Inventory LW rf task builder command.|rf/taskbuilder|FR-XFDA-001.2|name:task-builder; source_path:`.claude/commands/rf/taskbuilder.md`; role:task builder command; internal_deps:—; Auggie_path_verify; flag if moved; source_ref:§4.5|S|P1|
|21|COMP-019|agent-definitions reference (LW)|Inventory LW rf-* agent definition family.|rf/agents|FR-XFDA-001.2|name:agent-definitions; source_path:`.claude/agents/rf-*.md`; role:rf-* agent definitions; internal_deps:—; Auggie_path_verify; flag if moved; source_ref:§4.5|S|P1|
|22|DM-002|phase-gate contract|Author the strict-sequential phase-gate enforcement contract governing all 8 phase transitions; authored before the gates it defines and loaded by the sprint executor at launch.|Gate contract|OI-4|enforcement:strict_sequential; rule:no_phase_starts_until_prior_checkpoint_passes; checkpoint_format:table_with_pass_fail_per_criterion; contract loaded by sprint CLI before Phase 1|S|P0|
|23|DM-003|gate-criteria rows (×8)|Define the per-phase gate-criteria row for each of the 8 phases with deterministic artifact minima and semantic checks; minima govern halt logic over the approximate "35+" count.|Gate contract|DM-002|phase:enum(1..8); gate:string; min_artifacts:int per phase; semantic_checks:string per phase; all 8 rows present; minima govern halt logic|S|P0|
|24|NFR-XFDA.5a|Early restartability smoke test|Run a `--start` resume smoke test on a no-op gate at sprint launch (before any of the 35+ artifacts exist) to discover a structurally broken executor — wrong `--start` semantics, gate registry not loading, checkpoint-format mismatch — at the cheapest point; full restartability validation remains at M5 (NFR-XFDA.5).|cli/sprint|DM-002|`--start` resumes a no-op gate at launch; executor loads gate registry + parses checkpoint format; smoke failure halts before M2; does not replace M5 NFR-XFDA.5 full validation|S|P0|

### Integration Points — M1

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|phase_gate_contract (DM-002)|Gate dispatch contract|Yes|M1|sprint executor (COMP-003); every checkpoint pass/fail table M1–M5|
|gate-criteria registry (DM-003)|Registry (8 rows)|Yes|M1|phase-gate validator per phase; M5 assembly validator|
|component-map.md|Cross-framework mapping registry|Yes|M1|M2 strategy extraction; M3 comparison pair routing; M4 orphan checks|
|artifact root decision (OI-4)|Path contract|Yes|M1|all artifact writers; artifact-index.md|
|`--start` resume hook|CLI dispatch|Yes|M1|early smoke test (NFR-XFDA.5a); M5 full validation (NFR-XFDA.5); operator restart after crash/halt|
|Auggie MCP evidence binding|Tool dispatch (primary→fallback)|Yes|M1|every inventory entry; re-verified in M5|

### Milestone Dependencies — M1

- None upstream (foundation milestone). External repos `/config/workspace/IronClaude` (target) and `/config/workspace/llm-workflows` (frozen reference) must be readable; Auggie MCP is primary with Serena + Grep/Glob fallback; `artifacts/prompt.md` must be available for the stable LW reference inventory.

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OI-1|Do llm-workflows paths in `prompt.md` still match the current repo?|Medium; stale paths waste inventory effort and corrupt LW inventory + Phase 4 dual-repo evidence|Architecture lead|Before M1 exit|
|2|OI-2|Treat pipeline-analysis (COMP-008) as one component group or split into sub-components?|Low; affects COMP-008 extraction depth and M3 comparison granularity|Architecture lead|Before M1 exit (before M2)|
|3|OI-3|Does `FR-XFDA-001` need registration in an FR registry for v3.0 planning?|Low; administrative traceability before downstream roadmap ingestion|Sprint owner|Before M1 exit|
|4|OI-4 (alias OQ-ROOT)|Canonical artifact root: bare `artifacts/...` or `.dev/releases/current/cross-framework-deep-analysis/`?|High; every artifact path and traceability ref drifts if unresolved|Sprint owner|Before M1 start|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Auggie MCP unavailable for IronClaude repo|HIGH|Low|Inventory lacks primary evidence|Serena `get_symbols_overview` + Grep/Glob fallback; annotate degraded mode in artifacts|Architecture lead|
|2|Auggie MCP unavailable for llm-workflows repo|HIGH|Low|Reference inventory loses verification depth|Same fallback; LW list partially known from `prompt.md`; annotate limitation|Architecture lead|
|3|llm-workflows paths changed since `prompt.md` (GAP-1)|MEDIUM|Medium|Wasted inventory effort; wrong file refs downstream|Verify all LW paths in M1 (FR-XFDA-001.2); flag + annotate missing|Architecture lead|
|4|Artifact root ambiguity causes artifact drift|MEDIUM|Medium|Writers and validators disagree on paths; orphaned artifacts in M5|Resolve OI-4 before first write; record root in component map and DM-003 paths|Sprint owner|
|5|IC component inventory incomplete (fast-moving codebase)|MEDIUM|Medium|Cascade error into every downstream phase|Broad Auggie queries; M5 cross-checks all file refs|Architecture lead|

## M2: Evidence-Based Strategy Extraction

**Objective:** Extract balanced strategy documents for all 8 IC and 11 LW components with Auggie-first evidence, explicit strength/weakness pairing, and a centralized verifiable citation index. | **Duration:** Weeks 3-5 (3w) | **Entry:** M1 component map and artifact root accepted. | **Exit:** 8 `strategy-ic-*.md` and 11 `strategy-lw-*.md` accepted, each with file:line evidence, paired weaknesses/costs, and checkpoint scans recorded.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-XFDA-001.3|Per-component strategy extraction|Create IC and LW strategy docs for every scoped component (`strategy-ic-{component}.md`, `strategy-lw-{component}.md`), pairing each strength with a weakness/cost and citing file:line evidence; LW docs note rigorous AND bloated/slow/expensive.|Strategy extraction|M1|8 IC docs (1 per COMP-001..008); 11 LW docs (1 per COMP-009..019); every strength has paired weakness/cost; every claim has file:line Auggie evidence; LW docs flag rigor AND bloat/cost; no orphaned component|XL|P0|
|2|NFR-XFDA.1|Auggie-primary code reading|Enforce Auggie MCP as the primary code-reading tool for all strategy-extraction tasks, with documented fallback when unavailable.|Evidence control|M1|100% of code-reading tasks use Auggie primary; R-RULE-01 checkpoint recorded per phase (Phase 2 + Phase 3); fallback (Serena get_symbols_overview + Grep/Glob) annotated where used|M|P0|
|3|NFR-XFDA.2|Anti-sycophancy pairing|Enforce that every stated strength carries a paired weakness/cost via a per-phase checkpoint scan.|Quality rule|FR-XFDA-001.3|100% of strength claims paired; checkpoint scan recorded per phase (Phase 2 + Phase 3); zero unpaired strengths at gate; unpaired claims fixed before exit|M|P0|
|4|NFR-XFDA.3|Citation verifiability|Centralize all file:line citations into a verification-ready index, each labeled with source repo, so downstream validation can resolve them.|Evidence control|FR-XFDA-001.3|100% citations recorded; source repo noted per claim; Phase 7 verification-ready index emitted|M|P0|

### Integration Points — M2

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|strategy-ic-{component}.md (×8)|Strategy artifact family|Yes|M2|M3 comparison pairs; M4 merged strategy|
|strategy-lw-{component}.md (×11)|Strategy artifact family|Yes|M2|M3 comparison pairs; M4 discard/adopt decisions|
|Auggie evidence index|Evidence registry|Yes|M2|M3 dual-repo citations; M5 validation report|
|anti-sycophancy scan results|Quality checkpoint|Yes|M2|gate evaluator (Phase 2 + Phase 3); M3 verdict confidence; M5 rigor assessment|

### Milestone Dependencies — M2

- Depends on M1: `component-map.md` (pairing source for IC↔LW strategy alignment) and the artifact-root decision must be complete. Auggie MCP must be attempted for every code-reading task with fallback output marked. Phase 2 and Phase 3 workstreams may run in parallel inside this milestone but both must finish before M3.

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Strategy docs become one-sided advocacy (sycophancy drift)|HIGH|Medium|Adversarial comparisons inherit biased inputs|Enforce NFR-XFDA.2 before M2 exit; reject unpaired strength claims at the gate|Architecture lead|
|2|Citation quality varies across repos|HIGH|Medium|Phase 7 verification burden increases; evidence collapses under M5|Centralize citation index; require source-repo label for every claim; Auggie-primary sourcing|Evidence owner|
|3|LW docs overfit to shell implementation details|MEDIUM|Medium|M4 adoption plan drifts into mass import|Record pattern-level learning and implementation-mass exclusions in each LW doc|Architecture lead|

## M3: Adversarial Cross-Framework Comparison

**Objective:** Debate the 8 enumerated IC↔LW component pairs via `/sc:adversarial`, each citing file:line from both repos and producing a conditioned verdict that verifies "adopt patterns not mass". | **Duration:** Weeks 6-7 (2w) | **Entry:** M2 strategy docs and evidence index accepted; pair set fixed (OI-5). | **Exit:** 8 `comparison-*.md` accepted, each with a verdict + dual-repo file:line evidence + adoption-boundary note; inconclusive verdicts explicitly stated as "no clear winner" with rationale.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-XFDA-001.4|Adversarial comparison set|Run the required comparison set through `/sc:adversarial`, producing evidence-backed verdicts with conditions; pair set fixed in M3 via OI-5.|Adversarial pipeline|M2, OI-5|≥8 comparisons; dual-repo file:line evidence; verdict + conditions per pair; "adopt patterns not mass" / adoption boundary verified; uses `/sc:adversarial`|XL|P0|
|2|FR-XFDA-001.4a|Roadmap gates comparison|Compare IC roadmap fidelity/certify/remediate gates against LW PABLOV + quality-gates.|Adversarial pair|FR-XFDA-001.4|`comparison-roadmap-gates-vs-pablov.md`; IC + LW file:line evidence; verdict + conditions; adopt-patterns-not-mass note|M|P0|
|3|FR-XFDA-001.4b|Task tier comparison|Compare IC task-unified tier system against LW pipeline-orchestration + task-builder.|Adversarial pair|FR-XFDA-001.4|`comparison-task-tiers-vs-orchestration.md`; IC + LW file:line evidence; verdict + conditions; tier implications noted|M|P0|
|4|FR-XFDA-001.4c|Sprint executor comparison|Compare IC sprint CLI executor against LW automated-qa-workflow.|Adversarial pair|FR-XFDA-001.4|`comparison-sprint-vs-autoqa.md`; IC + LW file:line evidence; verdict + conditions; resume implications noted|M|P0|
|5|FR-XFDA-001.4d|Adversarial systems comparison|Compare IC adversarial-pipeline against LW anti-sycophancy system.|Adversarial pair|FR-XFDA-001.4|`comparison-adversarial-vs-antisycophancy.md`; IC + LW file:line evidence; verdict + conditions; bias-control implications noted|M|P0|
|6|FR-XFDA-001.4e|PM-agent comparison|Compare IC pm-agent (confidence/reflexion/self-check) against LW anti-hallucination + failure-debugging patterns.|Adversarial pair|FR-XFDA-001.4|`comparison-pmagent-vs-antihallucination.md`; IC + LW file:line evidence; verdict + conditions; validation-loop implications noted|M|P1|
|7|FR-XFDA-001.4f|Quality agent comparison|Compare IC quality-agents against LW rf-* agent-definitions.|Adversarial pair|FR-XFDA-001.4|`comparison-qualityagents-vs-rfagents.md`; IC + LW file:line evidence; verdict + conditions; agent-boundary implications noted|M|P1|
|8|FR-XFDA-001.4g|Pipeline analysis comparison|Compare IC pipeline-analysis (FMEA/guards/invariants) against LW quality-gates + PABLOV structural patterns.|Adversarial pair|FR-XFDA-001.4, OI-2|`comparison-pipelineanalysis-vs-structural.md`; IC + LW file:line evidence; verdict + conditions; structural-control implications noted; honors OI-2 split decision|M|P1|
|9|FR-XFDA-001.4h|Cleanup audit comparison|Compare IC cleanup-audit-cli against LW automated-qa-workflow audit dimension.|Adversarial pair|FR-XFDA-001.4|`comparison-cleanupaudit-vs-autoqa.md`; IC + LW file:line evidence; verdict + conditions; audit-control implications noted|M|P1|

### Integration Points — M3

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`/sc:adversarial` debate engine|Strategy-pattern dispatch|Yes|M3|each of the 8 comparison pairs|
|comparison-{pair}.md (×8)|Comparison artifact family|Yes|M3|M4 merged-strategy decisions; M5 human-review spot-check|
|comparison pair registry|Dispatch table|Yes|M3|adversarial run selection; M5 traceability checks|
|verdict condition matrix|Decision registry|Yes|M3|M4 adoption/discard plan; M5 validation report|
|dual-repo citation map|Evidence registry|Yes|M3|M5 citation verification|

### Milestone Dependencies — M3

- Depends on M2: all 8 IC and 11 LW strategy docs must be accepted, and the M2 evidence index must supply dual-repo citations for every pair. `/sc:adversarial` must be available; OI-5 must fix the pair set and the M3 gate `min_artifacts` derived from it.

### Open Questions — M3

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OI-5 (alias OQ-PAIRSET)|Are the 8 enumerated comparison pairs fixed, or may additional ad-hoc pairs be added?|Medium; sets M3 gate `min_artifacts`, M4 synthesis coverage, and timeline discipline|Sprint owner|Before M3 exit|

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Comparison pairs produce inconclusive verdicts|MEDIUM|Medium|Forced/false conclusions bias M4 synthesis|Allow explicit "no clear winner" verdict with rationale and conditions rather than forcing a conclusion|Adversarial lead|
|2|Adversarial output favors framework mass over patterns|HIGH|Medium|Improvement plan violates scope boundary|Require adoption-boundary note in every pair artifact and M4 pattern filter|Architecture lead|
|3|Pair count ambiguity causes unplanned work expansion|MEDIUM|Medium|Schedule and validation scope drift; gate under/over-counts comparisons|Resolve OI-5 before M3 exit; extra pairs approved only if explicitly accepted|Sprint owner|

## M4: Synthesis and Improvement Planning

**Objective:** Convert comparison verdicts into a merged "rigor without bloat" strategy and a prioritized IronClaude improvement plan that adopts patterns without implementation mass, backed by a machine-readable backlog schema. | **Duration:** Weeks 8-10 (3w) | **Entry:** M3 comparison artifacts and verdict condition matrix accepted. | **Exit:** `merged-strategy.md`, 8 `improve-{component}.md`, `improve-master.md` with dependency graph, and DM-001 backlog schema accepted; "patterns not mass" verified per adopted item.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-XFDA-001.5|Merged strategy synthesis|Create `merged-strategy.md` covering all Phase 4 component areas with an explicit "rigor without bloat" section, "patterns not mass" applied + documented per adopted pattern, and justified discard decisions.|Strategy synthesis|M3|covers all comparison areas; explicit "rigor without bloat" section; adopted patterns documented per item; discard decisions justified incl. "discard both" (GAP-2) as "no adoption; why"; internally consistent; no orphaned area|L|P0|
|2|FR-XFDA-001.6|Prioritized improvement plan|Create 8 `improve-{component}.md` + `improve-master.md` with dependency graph; each item carries file path(s), change, why, priority, effort, dependencies, risk, and acceptance criteria, distinguishing new-code from strengthen-existing.|Improvement planning|FR-XFDA-001.5|8 improve docs (1 per IC group) + master dependency graph; each item: file path(s)+change+why+priority(P0–P3)+effort(XS–XL)+deps+AC+risk; new-code vs strengthen-existing marked|XL|P0|
|3|NFR-XFDA.4|Patterns-not-mass verification|Verify every llm-workflows adoption item extracts a transferable control/validation pattern and excludes shell/framework mass.|Adoption control|FR-XFDA-001.6|100% adoption items verified patterns-not-mass; control/validation patterns adopted, never bash/shell machinery; Phase 6 checkpoint passes; Phase 7 review-ready evidence recorded|M|P0|
|4|DM-001|improvement_backlog item contract|Define the machine-readable backlog row schema emitted per improvement item for `/sc:roadmap` ingestion.|Backlog schema|FR-XFDA-001.6|id:string(IC-{component}-{seq}); component:string; title:string; priority:enum(P0,P1,P2,P3); effort:enum(XS,S,M,L,XL); pattern_source:string(LW pattern or "IC-native"); rationale:string; file_targets:list[string]; acceptance_criteria:list[string]; risk:string; patterns_not_mass_verified:bool|M|P0|

### Integration Points — M4

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|merged-strategy.md|Synthesis artifact|Yes|M4|FR-XFDA-001.6 plans; M5 rigor assessment; M5 missing-connection check (Phase 5→6)|
|improve-{component}.md (×8)|Plan artifact family|Yes|M4|final-improve-plan.md; `/sc:tasklist` handoff|
|improve-master.md|Dependency graph|Yes|M4|M5 validation; downstream sequencing|
|improvement_backlog item (DM-001)|Schema contract|Yes|M4|improvement-backlog.md; `/sc:roadmap` ingestion|
|patterns-not-mass checklist (NFR-4)|Adoption guard|Yes|M4|M5 adversarial validation; scope-creep check|

### Milestone Dependencies — M4

- Depends on M3: the verdict condition matrix and all 8 comparison artifacts must be complete and cite both repositories (or document why dual evidence is unavailable). The M1 artifact-root decision must be applied consistently to all plan artifacts; each adopted pattern maps to ≥1 improvement item.

### Open Questions — M4

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|GAP-2|How is a "discard both" comparison verdict represented when it feeds the improvement plan?|Low; accepted — "discard both" is a valid synthesis outcome documented as "no adoption; why" with plan gap notes|Architecture lead|M4 exit|

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Phase 6 plans drift into implementation mass|HIGH|Medium|Scope creep; non-portable, mass-import recommendations|NFR-XFDA.4 checklist per item; reject mass-import language before exit; M5 adversarial check|Architecture lead|
|2|Discard-both verdicts lack follow-through|LOW|Medium|M4 may force unnecessary adoption|Represent discard-both as "no adoption; why" in merged strategy and plan gap notes|Architecture lead|
|3|Plan items lack file paths or acceptance criteria|HIGH|Medium|M5 cannot validate downstream readiness; backlog rows non-conformant to DM-001|Apply DM-001 field-completeness check before M4 exit; author rows against DM-001 from the start|Planning owner|

## M5: Validation, Assembly, and Downstream Readiness

**Objective:** Validate every improvement item at an independent P0 quality boundary that must close before assembly begins, assemble traceable consolidated outputs, prove restartability under real phase state, and prove downstream roadmap/tasklist compatibility. | **Duration:** Weeks 11-12 (2w) | **Entry:** M4 merged strategy, 8 component plans, master plan, and DM-001 backlog schema accepted. | **Exit:** validation report (P0, pass/fail per item) closed before assembly; final plan, artifact index, rigor assessment, backlog, and sprint summary accepted; `--start` full resume validated; feature-acceptance closure asserted.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-XFDA-001.7|Improvement plan validation (P0 boundary)|Validate every plan item for path accuracy, scope discipline, Phase 5→6 linkage, and pass/fail status; model as an independent P0 Quality gate that must close before FR-XFDA-001.8 assembly begins; emit corrected `final-improve-plan.md`.|Validation pipeline|M4|pass/fail per item; all file paths Auggie-verified; scope-creep check vs patterns-not-mass; missing-connection check (Phase 5→6); P0 gate closes before assembly starts; corrected final plan produced|L|P0|
|2|FR-XFDA-001.8|Consolidated output assembly|Assemble `artifact-index.md` (links all artifacts), `rigor-assessment.md`, `improvement-backlog.md` (sc:roadmap-compatible), and `sprint-summary.md` with end-to-end traceability; begins only after the FR-XFDA-001.7 P0 gate closes.|Assembly pipeline|FR-XFDA-001.7, OI-6|artifact-index links all artifacts; end-to-end traceability (component→strategy→comparison→merged→improvement); no orphans/dead refs; rigor assessment + backlog + sprint summary produced|L|P0|
|3|NFR-XFDA.5|Sprint restartability (full validation)|Validate the sprint resumes from any phase gate via `--start` under real incremental phase state and recovers from a mid-phase crash without rerunning passed phases.|Sprint executor|DM-002|`--start <phase>` resumes at named gate; incremental writes flush per-artifact; mid-phase crash (exit -9 class) recoverable without rerun of passed phases; complements the M1 NFR-XFDA.5a smoke test|M|P0|
|4|NFR-XFDA.6|Roadmap backlog compatibility|Verify `improvement-backlog.md` is directly consumable by `/sc:roadmap` against the `improvement_backlog_schema` without schema errors.|Backlog schema|DM-001, FR-XFDA-001.8|schema-compliant per DM-001; `/sc:roadmap` ingestion succeeds without schema errors; manual review recorded (GAP-3 accepted risk)|M|P0|
|5|FR-XFDA-001|Feature acceptance closure|Validate completion traceability for the full cross-framework deep-analysis feature across all eight phase requirements in one auditable assertion.|Assembly pipeline|FR-XFDA-001.8|8 child FRs traced; 6 NFRs validated; 19 components covered; 3 contracts covered; artifact index complete; single feature-done gate asserted|M|P0|

### Integration Points — M5

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|validation-report.md|Pass/fail ledger (P0 gate)|Yes|M5|final-improve-plan.md; risk register evidence; corrective loop|
|final-improve-plan.md|Corrected execution plan|Yes|M5|`/sc:tasklist` (downstream)|
|artifact-index.md|Traceability link registry|Yes|M5|human review; audit of end-to-end chain|
|rigor-assessment.md|Assessment report|Yes|M5|release decision; improvement backlog rationale|
|improvement-backlog.md|Schema-bound export (DM-001)|Yes|M5|`/sc:roadmap` v3.0 (downstream)|
|sprint-summary.md|Sprint summary|Yes|M5|stakeholder handoff; restart notes|

### Milestone Dependencies — M5

- Depends on M4: 8 improvement plans, master plan, and DM-001 backlog contract complete. `/sc:roadmap` and `/sc:tasklist` interfaces must be available for downstream compatibility checks; sprint executor resume behavior must be observable through `--start` gate selection (foundation proven early in M1 via NFR-XFDA.5a).

### Open Questions — M5

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OI-6 (alias OQ-COUNTS)|Should gate enforcement use approximate "35+ artifacts" or deterministic per-phase minimums from §5.2?|Medium; sets the final validation standard and artifact-index completeness checks|Validation owner|Before M5 exit|
|2|GAP-3|`improvement-backlog.md` schema is unvalidated by existing test tooling — is manual review sufficient?|Medium; accepted risk — manual review + trial `/sc:roadmap` ingestion in Phase 8 stands in for automated schema validation|Validation owner|M5 exit|

### Risk Assessment and Mitigation — M5

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Sprint crashes mid-phase (exit -9 class)|MEDIUM|Low|Validation or assembly must resume cleanly|Phase-gate checkpoints, `--start` resume, and incremental artifact writes; early smoke test (NFR-XFDA.5a) de-risked the executor in M1|Sprint owner|
|2|Backlog schema remains manually validated only (GAP-3)|MEDIUM|Medium|Downstream `/sc:roadmap` ingestion may fail late|DM-001 schema review + `/sc:roadmap` ingestion dry check before exit|Validation owner|
|3|Artifact count ambiguity weakens gate enforcement|MEDIUM|Medium|Validators chase approximate totals|Use deterministic §5.2 per-phase minimums (OI-6) as the authoritative gate checks|Validation owner|
|4|Scope-creep items survive validation|HIGH|Low|Mass-not-patterns recommendations ship to backlog|Independent P0 scope-creep check vs patterns-not-mass; failed items corrected in final plan before assembly|Architecture lead|
|5|file:line citations fail verification at scale|MEDIUM|Medium|Items fail; rework loop extends schedule|100% Auggie re-verification (NFR-XFDA.3 index); Auggie-primary sourcing upstream reduces failure rate|Quality lead|

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By Milestone|Status|Fallback|
|---|---|---|---|
|Auggie MCP (primary code-reader)|M1, M2, M3, M5|Hard dependency|Serena `get_symbols_overview` + Grep/Glob; annotate degraded mode|
|Serena MCP (get_symbols_overview)|M1, M2 (fallback)|Available|Grep/Glob secondary fallback|
|Grep/Glob tooling|M1, M2 (fallback)|Available|Manual file enumeration with limitation notes|
|superclaude sprint CLI executor|M1–M5 (all gates)|Available|None — required for phase-gate execution + `--start` resume|
|`/sc:adversarial` debate engine|M3, M5|Available|Architect-led debate transcript with explicit limitation note|
|`/sc:roadmap` v3.0|M5 (consumer)|External consumer|Schema review against DM-001 if command unavailable|
|`/sc:tasklist`|M5 (consumer)|External consumer|Manual tasklist conversion with limitation note|
|External repos: `/config/workspace/IronClaude` (target), `/config/workspace/llm-workflows` (frozen reference)|M1+|Available|Abort or defer affected phase if repo unreadable|

### Infrastructure Requirements

- Read access to both repositories; llm-workflows treated as frozen (path verification only, no implementation changes).
- Writable canonical artifact root resolved by OI-4 before M1 execution; trivial rollback = delete the artifacts directory.
- Sprint executor environment with tmux/TUI, KPI, diagnostics, and logging (COMP-003) for phase-gated execution, `--start` resume, and crash-resilient incremental writes.
- MCP access for Auggie primary retrieval and Serena fallback discovery; downstream `/sc:roadmap` and `/sc:tasklist` availability for compatibility checks.
- Reference inputs available: `artifacts/prompt.md` (LW component list), `.dev/releases/backlog/2.25-roadmap-v5/v2.25-spec-merged.md` (rigor-gap evidence), `src/superclaude/examples/release-spec-template.md` (spec template).

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|Mitigation|Owner|
|----|------|---------------------|-------------|--------|------------|-------|
|R-001|Auggie MCP unavailable for IronClaude repo|M1, M2, M3, M5|Low|High|Serena `get_symbols_overview` + Grep/Glob fallback; label evidence limitations|Architecture lead|
|R-002|Auggie MCP unavailable for llm-workflows repo|M1, M2, M3|Low|High|Known `prompt.md` list + Serena/Grep/Glob fallback; label evidence limitations|Architecture lead|
|R-003|llm-workflows paths changed since `prompt.md` (GAP-1)|M1, M3|Medium|Medium|Verify all LW paths in M1; flag + annotate missing|Architecture lead|
|R-004|Artifact root ambiguity causes artifact drift|M1, M4, M5|Medium|Medium|Resolve OI-4 before first write; apply root consistently in index + validators|Sprint owner|
|R-005|IC component inventory incomplete|M1, M2, M3|Medium|Medium|Broad repository queries + M5 file-reference cross-checks|Architecture lead|
|R-006|Strategy docs become one-sided advocacy|M2, M3, M4|Medium|High|Enforce anti-sycophancy pairing (NFR-XFDA.2) before M2 exit|Architecture lead|
|R-007|Citation quality varies across repos|M2, M3, M5|Medium|High|Centralize citation index; require source-repo labels|Evidence owner|
|R-008|LW docs overfit to shell implementation details|M2, M4|Medium|Medium|Record pattern-level learning + implementation-mass exclusions|Architecture lead|
|R-009|Comparison pairs produce inconclusive verdicts|M3, M4|Medium|Medium|Allow explicit no-clear-winner verdicts with rationale + conditions|Adversarial lead|
|R-010|Adversarial output favors framework mass over patterns|M3, M4, M5|Medium|High|Require adoption-boundary notes + pattern filter checks|Architecture lead|
|R-011|Pair count ambiguity causes unplanned work expansion|M3|Medium|Medium|Resolve OI-5 before M3 exit|Sprint owner|
|R-012|Phase 6 plans drift into implementation mass|M4, M5|Medium|High|NFR-XFDA.4 checklist per item; reject mass-import language|Architecture lead|
|R-013|Discard-both verdicts lack follow-through (GAP-2)|M4|Medium|Low|Represent discard-both as "no adoption; why" in merged strategy + plan gap notes|Architecture lead|
|R-014|Plan items lack file paths or acceptance criteria|M4, M5|Medium|High|Apply DM-001 field-completeness check before M4 exit|Planning owner|
|R-015|Sprint crashes mid-phase (exit -9 class)|M1, M5|Low|Medium|Phase gates, `--start`, incremental writes; early smoke test (NFR-XFDA.5a) de-risks executor in M1|Sprint owner|
|R-016|Backlog schema remains manually validated only (GAP-3)|M5|Medium|Medium|DM-001 schema review + `/sc:roadmap` ingestion check|Validation owner|
|R-017|Artifact count ambiguity weakens gate enforcement (OI-6)|M5|Medium|Medium|Use deterministic §5.2 phase minimums as authoritative|Validation owner|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|Milestone|
|---|---|---|---|---|
|Phase 1 inventory complete|Inventory artifacts + mappings|≥3 artifacts; ≥8 IC→LW mappings; ≥8 IC + ≥11 LW components|Phase 1 gate scan + artifact index|M1|
|IC strategy coverage|strategy-ic-*.md|8/8 with strength+weakness section|Phase 2 gate scan|M2|
|LW strategy coverage|strategy-lw-*.md|11/11 with rigor+bloat/cost section|Phase 3 gate scan|M2|
|Comparison coverage|comparison-*.md|8/8 with verdict + dual-repo file:line|Phase 4 adversarial output review|M3|
|Merged synthesis integrity|merged-strategy.md|"rigor without bloat" section; no orphaned area|Phase 5 synthesis review|M4|
|Improvement plan completeness|9 plans|8 component + master; P-tier+effort+file path per item|Phase 6 plan completeness review|M4|
|Validation completeness|validation-report + final plan|pass/fail per item; P0 gate closes before assembly; final corrects all failures|Phase 7 pass/fail item review|M5|
|Consolidated outputs|4 outputs|index+assessment+backlog+summary; sc:roadmap-compatible|Phase 8 assembly + ingestion check|M5|
|Auggie-primary compliance (NFR-1)|% code-reading tasks|100%|R-RULE-01 checkpoint per phase|M2|
|Anti-sycophancy pairing (NFR-2)|% strength claims paired|100%|Checkpoint scan per phase|M2|
|Citation verifiability (NFR-3)|% citations resolvable|100%|Auggie verification in Phase 7|M5|
|Patterns-not-mass (NFR-4)|% adoption items verified|100%|Phase 6 checklist + Phase 7 adversarial validation|M4|
|Sprint restartability (NFR-5)|`--start` resume|Smoke test at launch + full resume from any gate|CLI executor resume test (M1 smoke + M5 full)|M5|
|Backlog schema interoperability (NFR-6)|Schema compliance|Ingests into `/sc:roadmap` without errors|Phase 8 compatibility check|M5|
|Feature acceptance closure|Traceability assertion|8 FRs + 6 NFRs + 19 components + 3 contracts traced|Single feature-done gate (FR-XFDA-001)|M5|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|----------|--------|------------------------|----------|
|Orchestration / control plane|Strict-sequential sprint gates via DM-002|Manual/interactive process; fully parallel phases|Sequential gates reduce cascade risk from a bad Phase 1 and preserve restartability while allowing bounded M2 parallel work|
|Milestone decomposition|5 composite milestones / 12 weeks|8 milestones + standalone M0 / 13 weeks (Variant A)|The 8 §5.2 gates persist inside 5 wrappers; DM-003 delivers per-phase attribution, neutralizing the per-phase-milestone premium; the extra A week was author-conceded as the weakest point|
|Restartability proof timing|Early `--start` smoke test (M1, NFR-XFDA.5a) + full validation (M5, NFR-XFDA.5)|Verify only at M5 (Variant B); standalone M0 milestone (Variant A)|Debate resolution "keep both": cheapest-possible discovery of a broken executor at launch, without carrying a standalone foundation week|
|Validation/assembly boundary|Independent P0 validation gate that closes before assembly, co-located in M5|Separate Quality milestone (Variant A); co-located step with no gate prominence (Variant B)|Preserves A's "the transition is the check's teeth" prominence without re-adding a milestone wrapper|
|llm-workflows handling|Frozen reference with path verification|Full re-survey; implementation import|Frozen reference lowers discovery cost and enforces pattern-only adoption|
|Evidence sourcing|Auggie MCP primary + Serena/Grep-Glob fallback|Grep/Glob only; Serena only|AC-6/NFR-1 mandate Auggie primary; fallback preserves progress under MCP outage (R-001/R-002)|
|Adoption filter|Patterns not mass (DM-001 `patterns_not_mass_verified`)|Import shell machinery; ignore LW patterns|Maintains IronClaude architecture while capturing reusable validation logic|
|Backlog interface|DM-001 `improvement_backlog` item contract|Free-form markdown; separate tracker|Machine-readable contract makes `/sc:roadmap` ingestion testable|
|Comparison verdict handling|Allow conditional and no-clear-winner verdicts|Force winners for every pair|Avoids false certainty and supports discard-both outcomes (GAP-2)|
|pipeline-analysis granularity|Deferred to OI-2 (resolve before M2)|Force single group now; force split now|Affects M3 comparison granularity; premature lock risks wrong comparison scope|
|Artifact count authority|Deterministic §5.2 per-phase minima (DM-003)|Approximate "35+ artifacts" total|Per-phase minimums are testable and prevent count ambiguity (OI-6)|
|Component priorities|Retain P0/P1/P2 tiers as inert centrality documentation|Uniform P0 (Variant A); behavioral tiers|Under an all-19-required gate tiers carry no behavioral force, but document adoption-centrality (debate concession)|

## Timeline Estimates

|Milestone|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1|2w|Week 1|Week 2|Artifact root fixed; IC/LW inventories; component map (≥8 mappings); gate contracts (DM-002/DM-003); `--start` smoke test|
|M2|3w|Week 3|Week 5|8 IC + 11 LW strategy docs; anti-sycophancy pairing 100%; Auggie evidence index|
|M3|2w|Week 6|Week 7|8 adversarial comparison artifacts with dual-repo file:line; verdict condition matrix|
|M4|3w|Week 8|Week 10|merged-strategy.md ("rigor without bloat"); 8 improve docs + improve-master.md; DM-001 backlog contract|
|M5|2w|Week 11|Week 12|P0 validation report → final plan; artifact index; backlog; sprint summary; full `--start` resume + feature closure|

**Total estimated duration:** 12 weeks
