---
spec_source: "TDD_TASK_BUILDER_CONVERGENCE.compressed.md"
complexity_score: 0.7
complexity_class: HIGH
primary_persona: architect
adversarial: false
base_variant: "none"
variant_scores: "none"
convergence_score: null
---
# Task-Builder Convergence v3.9 — Project Roadmap

## Executive Summary

Task-Builder Convergence v3.9 delivers six strictly additive task-builder rigor mechanisms across the rf-* agent topology: structural gate additions, an Execution Context header, inherited structural verdict passthrough, adversarial axis annotation, retry monotonicity guards, and DNSP synthetic finding emission. The roadmap is phased by technical layer so architecture decisions and schema contracts land before prompt surfaces, integration wiring, retry behavior, and production audit gates.

**Business Impact:** Reduced downstream rework from structurally defective MDTM task files while holding the token-cost ratio post-merge / pre-merge to ≤1.10 on 5 representative BUILD_REQUESTs.

**Complexity:** HIGH (0.7) — six serial FRs touch five source files, preserve five load-bearing invariants, require 25 synthetic fixtures, and carry one CRITICAL schema contradiction that blocks FR-CONV.1 implementation.

**Critical path:** Resolve Q-DM-1 → land TB-Add catalogue and Execution Context contract → wire inherited verdict and adversarial axes → add retry/DNSP resilience → run fixture suite, sync verification, token measurement, and first-5-run qualitative audit.

**Key architectural decisions:**

- Use intent-port over implementation-port: adapt sc-tasklist rigor concepts to task-builder's existing A.1–A.11 pipeline rather than importing bundle-specific mechanics.
- Preserve A-002 strictly-additive governance: no existing checklist item, gate stage, output field, or `.dev/tasks/` layout entry is renamed, renumbered, or removed.
- Treat structured gate artifacts as contracts: fixed strings, byte-exact verdict injection, deterministic dedup keys, and per-cycle freshness rules are validation surfaces.

**Open risks requiring resolution before M1:**

- Q-DM-1: PRD §25.4 per-item schema `{Description, Context, Acceptance, Confidence, Verification}` conflicts with current SKILL.md `{Context, Action, Output, Verification, Completion gate}`; Engineering Lead decision blocks FR-CONV.1.

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|---|---|---|---|---|---|---|---|
|M1|Foundation and Architecture Contracts|Foundation|P0|L|Q-DM-1|20|High|
|M2|Structural Gate and Execution Context|Core Logic|P0|XL|M1|24|Medium|
|M3|Verdict Channel and Qualitative Axes|Integration|P0|XL|M2|20|Medium|
|M4|Retry and Partition Resilience|Hardening|P0|XL|M3|21|Medium|
|M5|Validation, Rollout, and Operations|Production Readiness|P0|XL|M4|25|High|

## Dependency Graph

Q-DM-1 → M1 → M2 → M3 → M4 → M5

FR-CONV.1 → FR-CONV.2 → FR-CONV.3 → FR-CONV.4 → FR-CONV.5 → FR-CONV.6 → MIG-007

DM-001 → API-001 → FR-CONV.2; DM-002 + DM-005 → API-002 → FR-CONV.3; DM-003 → API-003 + API-004 → FR-CONV.5/FR-CONV.6; COMP-001 routes all integration wiring; COMP-006 remains preserved escalation guard.

## M1: Foundation and Architecture Contracts

**Objective:** Resolve schema blockers, freeze governance constraints, and define contracts before editing prompt surfaces | **Duration:** 2026-05-14 to 2026-05-21 (1 week) | **Entry:** TDD/PRD/extraction accepted as source inputs | **Exit:** Q-DM-1 resolved; A-001/A-002/G6 decisions recorded; contract rows ready for implementation

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|Q-DM-1|Per-item schema decision|Resolve the PRD §25.4 versus SKILL.md schema contradiction before any TB-Add enforcement lands.|Governance|dash|TDD value documented; PRD value documented; chosen schema recorded; downstream rows cite Q-DM-1|M|P0|
|2|A-001|Sync discipline contract|Enforce `src/superclaude/` as source-of-truth with `make sync-dev` then `make verify-sync` before commit.|Tooling|dash|source first; sync-dev required; verify-sync 100%; direct `.claude/` edit reverted|S|P0|
|3|A-002|Strictly additive governance|Freeze the rule that existing rf-qa checks, qualitative checklist items, gate stages, output fields, and `.dev/tasks/` layout entries are not renamed, renumbered, or removed.|Governance|dash|additive only; no removal; no renumbering; no stage replacement; rollback per FR|M|P0|
|4|G6|Four-case conflict rule|Apply CASE A/B/C/D classification to every task-builder and sc-tasklist mechanism conflict.|Governance|A-002|CASE-D rows for PR-01/02/06/07/05; CASE-B PR-03/04 no register row; protected invariant named|M|P0|
|5|INV-002|Verdict freshness invariant|Define per-cycle reinjection of the current rf-qa verdict so stale structural verdicts cannot govern current qualitative review.|QA Contract|DM-002|cycle-N+1 reread; no memoized verdict; spawn prompt carries current table; stale verdict FAIL|S|P0|
|6|INV-010|Dynamic checklist enumeration|Define that downstream inherited-verdict consumers enumerate the active TB-Add catalogue dynamically rather than assuming a fixed row count.|QA Contract|FR-CONV.1|catalogue growth detected; row count not fixed; PR-04 richens after PR-06; no fixed 9/15/20 assumption|S|P0|
|7|INV-012|DNSP dedup composition|Define how synthetic-dnsp findings enter `F_n` and how identical dedup keys behave across cycles.|Retry Contract|DM-003|synthetic counts as failure; identical key not regression; cross-cycle dedup not collapsed; monotonicity still applies|M|P0|
|8|INV-015|Evidence-bound context invariant|Bind TB-Add-8 to the per-item `Context` field regardless of which 5-field schema Q-DM-1 selects.|Task Schema|Q-DM-1|Context field exists; file:line accepted; justified-absence accepted; bare path FAIL|S|P0|
|9|INV-019|Self-Audit invariant|Define rf-qa-qualitative's requirement to list relied-on PASS items and at least one semantic check beyond inherited structural PASS.|QA Contract|DM-002|PASS reliance listed; ≥1 semantic check listed; reliance not verification; first 5 runs auditable|S|P0|
|10|INV-021|Within-agent DNSP invariant|Define DNSP emission as within-partition-instance behavior that does not serialize sibling partitions.|Partition Contract|DM-003|N partitions concurrent; exhausted partition emits; N-1 continue; cohort not serialized|M|P0|
|11|NFR-CONV.1|Structural determinism SLO|Define byte-identical deterministic scope for TB-Add verdicts, synthetic-dnsp fields, dedup keys, axis values, and Items Reviewed table structure.|Quality|dash|same BUILD_REQUEST; same source tree; structural fields byte-identical; prose excluded|M|P0|
|12|NFR-CONV.2|Prose determinism exclusion|Define that LLM-driven per-item Context prose and semantic-check prose are not byte-equality gates while structural annotations remain byte-equal.|Quality|NFR-CONV.1|prose may vary; axis labels fixed; finding counts fixed; dedup keys fixed|S|P1|
|13|NFR-CONV.6|Self-contained-item invariant|Define the accepted 5-field per-item schema after Q-DM-1 and fail-closed behavior when any required field is absent.|Task Schema|Q-DM-1|all 5 fields populated PASS; one field absent FAIL; schema names match Q-DM-1 decision|M|P0|
|14|NFR-CONV.7|Evidence-bound-item invariant|Define the per-item context citation rule and justified-absence path.|Task Schema|INV-015|bare `Context: src/foo` FAIL; `src/foo:42` PASS; justified-absence PASS|S|P0|
|15|NFR-CONV.8|Persistent `.dev/tasks/` artifact invariant|Define the no-layout-change constraint across research, qa, synthesis, reviews, and task-file paths.|Storage|A-002|no mandatory subdir added; no path rename; no naming-pattern change; pre/post layout diff zero|S|P0|
|16|NFR-CONV.9|Zero-trust QA invariant|Define the preserved PASS/FAIL semantics: any gap of any severity fails the gate.|QA Contract|A-002|1 LOW finding FAIL; inherited verdict cannot independently verify semantic item; all gaps resolved before proceed|S|P0|
|17|NFR-CONV.10|Parallel-research invariant|Define the concurrency guarantee for rf-qa/rf-analyst/rf-qa-qualitative partition cohorts.|Partition Contract|INV-021|spawn timestamps overlap; exhaust does not stop siblings; DNSP fires within agent instance|M|P0|
|18|D-001|Internal dependency ledger|Freeze the internal dependency set used by implementation planning: release-spec, conflict-register, invariant-probe, FINAL-REPORT, source anchors, `.dev/tasks/`, sync tooling.|Governance|dash|10 internal dependencies listed; no external dependency; owners assigned; stale anchor risk tracked|S|P1|
|19|NG-001|Scope guardrail ledger|Record out-of-scope constraints so deliverables do not implement deferred or rejected capabilities.|Scope|dash|no bulk-port all checks; no history-based tier selection; no checklist replacement; no PR-05 in v3.9; no `.dev/tasks/` layout change|S|P0|
|20|JTBD-001|Primary job coverage map|Map PRD primary jobs to FR-CONV rows so generation-time defect detection, verdict handoff, and retry halting all have implementation coverage.|Product|FR-CONV.1,FR-CONV.3,FR-CONV.5|Job 1 maps FR-CONV.1/2; Job 2 maps FR-CONV.3/4; Job 3 maps FR-CONV.5/6|S|P1|

### Integration Points — M1

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|A-001 sync pipeline|Make target workflow|Yes|M1|All source edits in M2-M5|
|G6 conflict rule|Governance registry|Yes|M1|FR landing decisions|
|Q-DM-1 decision record|Open-question resolution|No|M1|FR-CONV.1, NFR-CONV.6, DM-004|
|Invariant map INV-002/010/012/015/019/021|Acceptance dependency map|Yes|M1|Tests and QA gates|

### Milestone Dependencies — M1

- Q-DM-1 must be resolved before M1 exit and before any M2 implementation row tied to FR-CONV.1 or DM-004 begins.

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|Q-DM-1|SC-1 CRITICAL: PRD §25.4 declares per-item 5-field schema `{Description, Context, Acceptance, Confidence, Verification}` preserved unchanged at SKILL.md:1452-1457, but current SKILL.md:1450-1460 holds `{Context, Action, Output, Verification, Completion gate}`. Which schema is authoritative?|Blocks FR-CONV.1, NFR-CONV.6, DM-004, and TB-Add-8 acceptance authoring|Engineering Lead|Before 2026-05-21|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Q-DM-1 remains unresolved and blocks structural gate work|High|Medium|M2 cannot begin safely|Treat as M1 exit blocker; choose one schema path and apply consistently|Engineering Lead|
|2|Scope guardrails are weakened during planning|Medium|Low|Out-of-scope PR-05 or bulk-port work enters v3.9|Use NG-001 as row-level review gate before emitting implementation tasks|Architect|

## M2: Structural Gate and Execution Context

**Objective:** Implement the TB-Add structural checks, Execution Context header, task schema, and core component touchpoints | **Duration:** 2026-05-22 to 2026-06-19 (4 weeks) | **Entry:** M1 exit complete; Q-DM-1 resolved | **Exit:** FR-CONV.1/2, DM-001/004, API-001, COMP-001/002, and TEST-001..006 pass with sync verification

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-CONV.1|TB-Add structural checks|Append TB-Add-1..8 to rf-qa task-integrity and mirror across all three definition surfaces.|rf-qa; task-builder/SKILL.md|Q-DM-1,A-002|TB-Add-1/3/4/5/6/7/8 FAIL on violation; TB-Add-2 emits `[ADVISORY]`; ≥3 grep hits per ID; no existing check renamed/removed; no bundle-specific sc-tasklist checks|XL|P0|
|2|FR-CONV.2|Execution Context header|Insert task-level `## Execution Context` block in generated MDTM files after prerequisites and before Phase 1.|task-builder/SKILL.md; rf-task-builder|FR-CONV.1|References line emitted; Source areas line emitted when derivable; Key constraints 1–3 when derivable; minimal BUILD_REQUEST References-only; header contains zero file paths or file:line citations|L|P0|
|3|DM-001|Execution Context data entity|Define the generated task-file header contract.|MDTM Task File|FR-CONV.2|References:list[string] required format `R-###: <ref-line>`; Source areas:list[string] required unless degraded and never paths/citations; Key constraints:list[string] 1–3 unless degraded; degraded form omits absent labels|M|P0|
|4|DM-004|Per-item checklist schema|Implement the per-item schema selected by Q-DM-1 and enforce the `Context` field citation path.|MDTM Task File|Q-DM-1,NFR-CONV.6|PRD path: Description:string|required|imperative; Context:string|required|file:line or justified-absence; Acceptance:string|required|observable; Confidence:HIGH/MEDIUM/LOW|required+rationale; Verification:string|required|command/inspection/test; if current schema chosen: Context, Action, Output, Verification, Completion gate all required|L|P0|
|5|API-001|BUILD_REQUEST to MDTM output contract|Extend existing BUILD_REQUEST-to-MDTM generation so Execution Context output is produced without new transport.|Skill Prompt; MDTM File|DM-001|Skill-tool prompt unchanged; MDTM contains Execution Context; malformed when References cannot derive; no auth/rate limits; no network dependency|M|P0|
|6|COMP-001|task-builder/SKILL.md orchestration surface|Edit the skill orchestrator at A.10/A.10.5/template/prompt surfaces for structural and header behavior.|Skill Orchestrator|FR-CONV.1,FR-CONV.2|Type:Skill orchestrator; Location:`src/superclaude/skills/task-builder/SKILL.md`; Modifying FRs:1/2/3/4/5/6; Dependencies:rf-task-researcher, rf-task-builder, rf-qa, rf-analyst, rf-qa-qualitative; Stage A only|XL|P0|
|7|COMP-002|rf-qa structural QA surface|Edit rf-qa task-integrity checklist and fix-cycle text without weakening zero-trust verdict semantics.|rf-qa.md|FR-CONV.1|Type:Structural QA agent; Phases:research-gate,synthesis-gate,report-validation,task-integrity; Location:`src/superclaude/agents/rf-qa.md`; Modifying FRs:1,5,6; Key anchors:zero-trust verdict; TB-Add appended only|XL|P0|
|8|TB-Add-1|Initial-text defect scan|Create the first added structural check for TBD/TODO/title-only item content.|rf-qa.md; SKILL.md|FR-CONV.1|detects TBD; detects TODO; detects title-only; emits item-ID-naming error; hard FAIL|S|P0|
|9|TB-Add-2|Item-count advisory bounds|Create advisory item-count bounds check while calibration remains open.|rf-qa.md; SKILL.md|FR-CONV.1,OPEN-INV-006|≥3 lower bound checked; ≤40 track checked; ≤50 single-track checked; `[ADVISORY]` prefix; does not block gate|S|P1|
|10|TB-Add-3|Clarification adjacency check|Create hard check that blocked items requiring clarification are adjacent to the relevant open question or decision dependency.|rf-qa.md; SKILL.md|FR-CONV.1|blocked item has adjacent clarification reference; missing adjacency emits item-ID-naming error; hard FAIL|S|P0|
|11|TB-Add-4|Circular-dependency DAG check|Create hard dependency graph validation for intra-phase and inter-phase cycles.|rf-qa.md; SKILL.md|FR-CONV.1|cycle detected; involved item IDs named; acyclic graph passes; hard FAIL on circular dependency|M|P0|
|12|TB-Add-5|Granularity and XL-subtask check|Create hard check that XL work carries subtask structure or is split before execution.|rf-qa.md; SKILL.md|FR-CONV.1|XL item with subtasks PASS; XL item without subtasks FAIL; non-XL unaffected; item ID named|S|P0|
|13|TB-Add-6|Confidence and Verification format check|Create hard check for consistent Confidence and Verification formatting in each item.|rf-qa.md; SKILL.md|FR-CONV.1,DM-004|Confidence enum/rationale present; Verification concrete; mismatched format FAIL; item ID named|S|P0|
|14|TB-Add-7|Execution Context cross-validation|Create hard check that each Source areas entry reappears in at least one per-item Context field.|rf-qa.md; SKILL.md|FR-CONV.2,DM-001|each source area referenced; degraded References-only tolerated; drift FAIL; item/header relation named|M|P0|
|15|TB-Add-8|Per-item Context citation check|Create hard check that per-item Context fields include at least one file:line citation or justified-absence comment.|rf-qa.md; SKILL.md|DM-004,NFR-CONV.7|`src/foo` FAIL; `src/foo:42` PASS; justified-absence PASS; item ID named|M|P0|
|16|NFR-CONV-R1|Single-pass gate baseline|Establish ≥80% first-cycle task-integrity PASS baseline across representative BUILD_REQUESTs.|QA Metrics|FR-CONV.1|representative set defined; first-cycle PASS counted; baseline ≥80%; failures route to fix-cycle|S|P1|
|17|TEST-001|test_tb_add_1_initial_text|Verify TB-Add-1 detects TBD/TODO/title-only generated items.|Tests|TB-Add-1|synthetic MDTM input; TB-Add-1 emits item-ID error; gate FAILs; no external service|S|P0|
|18|TEST-002|test_dag_cycle_tb_add_4|Verify TB-Add-4 detects circular dependencies across items and phases.|Tests|TB-Add-4|circular deps input; TB-Add-4 emits; gate FAILs; acyclic control passes|S|P0|
|19|TEST-003|test_evidence_bound_tb_add_8|Verify TB-Add-8 file:line and justified-absence behavior.|Tests|TB-Add-8|bare path FAIL; `src/foo:42` PASS; `<none — pure refactor> [justified-absence]` PASS|S|P0|
|20|TEST-004|test_execution_context_full|Verify full Execution Context emits all three labeled lines.|Tests|FR-CONV.2,DM-001|References present; Source areas present; Key constraints present; placement after prerequisites before Phase 1|S|P0|
|21|TEST-005|test_execution_context_minimal_buildrequest|Verify minimal BUILD_REQUEST degrades to References-only.|Tests|FR-CONV.2,DM-001|References present; Source areas omitted; Key constraints omitted; no blank labels|S|P0|
|22|TEST-006|test_execution_context_no_file_paths|Verify Execution Context header contains no code paths or file:line citations.|Tests|FR-CONV.2|header grep for `src/` returns zero; header grep for `/.*:[0-9]+` returns zero; per-item citations unaffected|S|P0|
|23|OPEN-INV-006|TB-Add-2 calibration question|Carry item-count bound calibration forward without blocking v3.9.|QA Metrics|TB-Add-2|bounds remain advisory; calibration owner named; Phase-2 target recorded; no hard fail before calibration|S|P2|
|24|K-001|TB-Add false-positive control|Implement review and rollback path for individual TB-Add false positives.|Risk Control|FR-CONV.1|source-check ID cited; specific append line revertable; TB-Add-2 advisory; false-positive class documented|S|P1|

### Integration Points — M2

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|TB-Add catalogue|Checklist registry|Yes|M2|rf-qa task-integrity; FR-CONV.3 dynamic enumeration|
|Execution Context header|MDTM header contract|Yes|M2|TB-Add-7; downstream executor agents|
|Per-item Context citation rule|Schema validation|Yes|M2|TB-Add-8; NFR-CONV.7|
|BUILD_REQUEST to MDTM output|Skill prompt transport|Yes|M2|rf-task-builder; rf-qa|

### Milestone Dependencies — M2

- M2 depends on M1 Q-DM-1 resolution, A-001 sync discipline, A-002 additive governance, and G6 conflict-rule classification.

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|TB-Add false positives consume fix cycles|Medium|Low|Gate noise and rework|Ship TB-Add-2 advisory; keep each TB-Add individually revertable|rf-qa maintainer|
|2|Execution Context drifts from item Context fields|Medium|Low|Downstream executor confusion|TB-Add-7 cross-validates source areas; degraded References-only form allowed|task-builder maintainer|
|3|Per-item schema decision applied inconsistently|High|Low|NFR-CONV.6 cannot be validated|Tie DM-004 and TB-Add-8 to Q-DM-1; block merge on mismatch|Engineering Lead|

## M3: Verdict Channel and Qualitative Axes

**Objective:** Wire rf-qa task-integrity verdicts into rf-qa-qualitative and add semantic axis annotation without weakening anti-inflation controls | **Duration:** 2026-06-22 to 2026-07-17 (4 weeks) | **Entry:** M2 structural gate and header tests pass | **Exit:** FR-CONV.3/4, DM-002/005, API-002, COMP-003, and TEST-007..014 pass with byte-exact verdict injection

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-CONV.3|Inherited structural verdict passthrough|Inject rf-qa task-integrity verdict table into rf-qa-qualitative spawn prompt and add Self-Audit output requirement.|task-builder/SKILL.md; rf-qa-qualitative.md|FR-CONV.1,FR-CONV.2|`## Inherited Structural Verdict` present; rf-qa Items Reviewed table byte-exact; directive fixed; cycle-N verdict refreshed; Self-Audit lists relied-on PASS items and ≥1 semantic check|XL|P0|
|2|FR-CONV.4|Five adversarial axes overlay|Add axis taxonomy before rf-qa-qualitative 15-item task-qualitative checklist and axis column in Items Reviewed output.|rf-qa-qualitative.md; task-builder/SKILL.md|FR-CONV.3|Five axes section before checklist; axis value in {drift,contradictions,omissions,weakened-criteria,invented-content,none}; drift-axis-inactive when no GOAL baseline; 15-item checklist unchanged|L|P0|
|3|DM-002|Inherited Structural Verdict block|Define the injected verdict-block data entity.|Spawn Prompt|FR-CONV.3|rf_qa_table_verbatim:string/markdown|required|byte-exact table+verdict+counts; prompt_directive:string|required|fixed text; reinjection_rule:string|required|fixed cycle refresh text|M|P0|
|4|DM-005|rf-qa to rf-qa-qualitative phase contract|Formalize producer, consumer, artifact, versioning, delivery, freshness, enumeration, Self-Audit, anti-inflation, and failure-mode contract.|Phase Contract|DM-002|producer:rf-qa; consumer:rf-qa-qualitative; artifact fixed; schema_version:1.0.0; delivery_semantics:at-most-once-per-cycle; freshness_rule INV-002; enumeration_rule INV-010; consumer_obligation INV-019; anti_inflation preserved; failure_mode halts before A.10.5|L|P0|
|5|API-002|Task-integrity to task-qualitative contract|Implement orchestrator extraction and injection path from rf-qa report to rf-qa-qualitative spawn.|Skill Prompt; QA Reports|DM-002,DM-005|extract contiguous Items Reviewed table; splice under inherited header; no-verdict halts at A.10; anti-inflation block byte-stable; cycle rerun reads new report|L|P0|
|6|COMP-003|rf-qa-qualitative content QA surface|Edit qualitative agent output schema, inherited verdict handling, axis section, and DNSP partition rule surfaces.|rf-qa-qualitative.md|FR-CONV.3,FR-CONV.4|Type:Content QA agent; Phases:7 including task-qualitative; Location:`src/superclaude/agents/rf-qa-qualitative.md`; Modifying FRs:3,4,6; anti-inflation preserved; severity floor preserved|XL|P0|
|7|AX-1|Drift axis annotation|Define and apply drift lens for cited facts that no longer match current source.|rf-qa-qualitative.md|FR-CONV.4|axis value `drift`; cites stale fact cases; inactive only when no citations/GOAL baseline; no structural recheck of inherited PASS|S|P1|
|8|AX-2|Contradictions axis annotation|Define and apply contradictions lens for mutually incompatible assertions across artifacts or sections.|rf-qa-qualitative.md|FR-CONV.4|axis value `contradictions`; conflict described; severity floor not weakened; finding tied to source sections|S|P1|
|9|AX-3|Omissions axis annotation|Define and apply omissions lens for absent required touchpoints, dependencies, or steps.|rf-qa-qualitative.md|FR-CONV.4|axis value `omissions`; missing requirement named; impacted item named; no invented requirement introduced|S|P1|
|10|AX-4|Weakened-criteria axis annotation|Define and apply weakened-criteria lens for acceptance softened below source standard.|rf-qa-qualitative.md|FR-CONV.4|axis value `weakened-criteria`; source criterion cited; weakened form identified; severity assigned per existing rules|S|P1|
|11|AX-5|Invented-content axis annotation|Define and apply invented-content lens for capabilities not present upstream.|rf-qa-qualitative.md|FR-CONV.4|axis value `invented-content`; upstream absence stated; non-goal guard checked; no out-of-scope capability accepted|S|P1|
|12|AX-0|None axis sentinel|Define the `none` sentinel for checks that pass through the axis lens.|rf-qa-qualitative.md|FR-CONV.4|axis value `none` allowed; not used as escape for uninspected rows; every row populated|S|P1|
|13|TEST-007|test_inherited_verdict_present|Verify inherited verdict header appears in rf-qa-qualitative spawn prompt.|Tests|FR-CONV.3|grep finds header; directive present; block located before qualitative instructions|S|P0|
|14|TEST-008|test_inherited_verdict_freshness_inv_002|Verify cycle-2 qualitative spawn receives cycle-2 verdict instead of stale cycle-1 verdict.|Tests|FR-CONV.3,INV-002|two-cycle fixture; cycle reports differ; spawn prompt byte-diffs to current verdict; stale verdict absent|M|P0|
|15|TEST-009|test_self_audit_inv_019|Verify Self-Audit contains relied-on PASS items and semantic checks beyond inherited PASS.|Tests|FR-CONV.3,INV-019|`## Self-Audit` present; relied-on PASS list nonempty when applicable; ≥1 semantic check; no item verified solely by inherited verdict|M|P0|
|16|TEST-010|test_dynamic_enumeration_inv_010|Verify qualitative consumer picks up TB-Add catalogue changes dynamically.|Tests|FR-CONV.1,FR-CONV.3|catalogue growth reflected; no fixed row-count assumption; enriched checklist after PR-06|M|P0|
|17|TEST-011|test_five_axes_overlay|Verify Five Adversarial Axes header appears before immutable 15-item checklist.|Tests|FR-CONV.4|grep ordering passes; checklist body byte-stable; overlay-only change|S|P0|
|18|TEST-012|test_axis_column_populated|Verify Items Reviewed rows carry populated axis values.|Tests|FR-CONV.4|parse table; axis column exists; every row nonempty; canonical vocabulary only|S|P0|
|19|TEST-013|test_drift_axis_inactive_when_no_goal_baseline|Verify no GOAL-baseline condition emits drift-axis-inactive annotation.|Tests|FR-CONV.4|fixture lacks GOAL baseline; summary contains `drift-axis-inactive`; no N/A substitute|S|P0|
|20|TEST-014|test_severity_floor_unweakened|Verify rf-qa-qualitative severity floor remains unchanged.|Tests|FR-CONV.4,NFR-CONV.9|critical rules block byte-stable; contradictions remain IMPORTANT/CRITICAL floor; anti-inflation unchanged|S|P0|

### Integration Points — M3

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`## Inherited Structural Verdict`|Spawn-prompt block|Yes|M3|rf-qa-qualitative task-qualitative phase|
|rf-qa Items Reviewed table|Markdown report extract|Yes|M3|DM-002/API-002 injection|
|`## Self-Audit`|Qualitative report section|Yes|M3|K-003 audit; NFR-CONV.9 validation|
|Five Adversarial Axes|Axis taxonomy|Yes|M3|Items Reviewed axis column|
|Axis column|Output table field|Yes|M3|TEST-012; qualitative report consumers|

### Milestone Dependencies — M3

- M3 depends on M2 TB-Add catalogue availability, Execution Context validation, and stable rf-qa task-integrity verdict output.

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Inherited verdict causes qualitative review inflation|High|Low|Semantic defects marked verified without tool engagement|Self-Audit obligation; first 5 runs audited; anti-inflation text preserved|QA Lead|
|2|Axis annotations over-classify benign rows|Medium|Low|Noisy qualitative findings|Axes are annotation-only; 15-item checklist remains authority; tune distribution after audit|rf-qa-qualitative maintainer|
|3|Stale verdict injected on fix-cycle rerun|High|Low|Qualitative review uses obsolete structural facts|INV-002 cycle reread; TEST-008 blocks release on stale content|task-builder maintainer|

## M4: Retry and Partition Resilience

**Objective:** Add halt-on-regression, halt-on-non-shrink, DNSP emission, partition dedup, and all-agents-fail preservation | **Duration:** 2026-07-20 to 2026-08-14 (4 weeks) | **Entry:** M3 verdict channel and axis overlay tests pass | **Exit:** FR-CONV.5/6, DM-003, API-003/004/005, COMP-004/005/006, and TEST-015..022 pass

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-CONV.5|Retry monotonicity guards|Add regression and monotonicity stop conditions to existing retry loops without adding a new loop or collapsing counters.|rf-task-builder.md; rf-qa.md; SKILL.md|FR-CONV.1,FR-CONV.6|PASS@N→FAIL@N+1 emits verbatim regression message before monotonicity; `|F_{n+1}|>=|F_n|` emits `[HALT-MONOTONICITY]|F|=<n>`; strict shrink continues; counters preserved|XL|P0|
|2|FR-CONV.6|DNSP synthetic finding|Emit HIGH-severity synthetic-dnsp finding after partition escalation ladder exhaust when at least one sibling partition succeeded.|rf-qa.md; rf-analyst.md; rf-qa-qualitative.md; SKILL.md|FR-CONV.5|all 5 fixed fields plus dedup_key/found_n_times; identical key collapses within cycle; zero partitions succeeded emits no synthetic; rf-team-lead escalation preserved|XL|P0|
|3|DM-003|Synthetic DNSP finding entity|Define DNSP finding fields and deterministic dedup identity.|Partition Output|FR-CONV.6|severity:HIGH fixed; source:`synthetic-dnsp` fixed; affected_range:string required; evidence:string required spawn-log or explicit absence; recommendation fixed; dedup_key:list[range,exhaust_point] required; found_n_times:int default 1|L|P0|
|4|API-003|Partition agent to orchestrator DNSP contract|Implement structured DNSP emission in normal partition output streams.|Partition Output; QA Merge|DM-003|one finding per exhausted partition; HIGH non-overridable; within-cycle dedup; sibling partitions continue; real findings retained|L|P0|
|5|API-004|Fix-loop halt signal contract|Implement halt message strings and precedence ordering for cycle transition decisions.|Fix Loop|FR-CONV.5,DM-003|regression check first; monotonicity second; hard cap third; otherwise continue; F_n identity is dedup-key; synthetic counts as failure|M|P0|
|6|API-005|All-partition-agents-fail escalation contract|Preserve existing zero-success escalation path through rf-team-lead rather than DNSP.|Orchestrator; rf-team-lead.md|FR-CONV.6|zero successes emits no synthetic; rf-team-lead.md:417 path active; HALT-and-ask-user preserved; no short-circuit|M|P0|
|7|COMP-004|rf-analyst DNSP partition surface|Add DNSP partition protocol to rf-analyst without changing parallel analysis responsibilities.|rf-analyst.md|FR-CONV.6|Type:completeness/synthesis-review agent; Location:`src/superclaude/agents/rf-analyst.md`; Modifying FR:6; concurrent with rf-qa; DNSP at partition protocol|M|P0|
|8|COMP-005|rf-task-builder fix-loop surface|Add retry monotonicity encoding to rf-task-builder I16 table and preserve BUILD_REQUEST transformation responsibilities.|rf-task-builder.md|FR-CONV.5|Type:BUILD_REQUEST→MDTM subagent; Location:`src/superclaude/agents/rf-task-builder.md`; Modifying FR:5; key contract BUILD_REQUEST schema retained|L|P0|
|9|COMP-006|rf-team-lead escalation guard|Preserve project-mode escalation behavior and ensure DNSP does not replace all-agents-fail handling.|rf-team-lead.md|API-005|Type:project-mode escalation orchestrator; Location:`src/superclaude/agents/rf-team-lead.md`; Modifying FRs:NONE; line 417 preserved; three-fix-cycle HALT preserved|M|P0|
|10|DNSP-EXH-1|Escalation exhaust vocabulary|Define deterministic exhaust-point vocabulary for DNSP dedup keys.|Partition Contract|DM-003|tokens include retry-1,retry-2,gap-fill-round-1,gap-fill-round-2,gap-fill-round-3; removals forbidden; additions additive|S|P0|
|11|DNSP-DEDUP-1|Within-cycle dedup merge|Implement within-cycle collapse for identical DNSP dedup keys.|QA Merge|DM-003,API-003|same key produces one record; found_n_times increments; no cross-cycle collapse; evidence retained|M|P0|
|12|RETRY-REG-1|Regression precedence check|Implement PASS-to-FAIL regression detection before monotonicity comparison.|Fix Loop|API-004|PASS@N/FAIL@N+1 detected; message exactly `Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.`; loop exits before monotonicity|M|P0|
|13|RETRY-MONO-1|Non-shrink monotonicity check|Implement failure-set cardinality halt for `|F_{n+1}|>=|F_n|` after regression check.|Fix Loop|API-004|message `[HALT-MONOTONICITY]|F|=<n>` emitted; strict shrink continues; no slow-shrink threshold|M|P0|
|14|TEST-015|test_monotonicity_halt_F_5_5_5|Verify repeated failure-set cardinality halts at cycle 2.|Tests|RETRY-MONO-1|`|F|=5,5,5`; cycle 2 halt; message grep passes; no cycle-3 log|S|P0|
|15|TEST-016|test_regression_halt_pass1_fail2|Verify PASS-to-FAIL regression halt precedence.|Tests|RETRY-REG-1|Item 3.2 PASS@1/FAIL@2; regression message emitted; monotonicity not evaluated first|S|P0|
|16|TEST-017|test_slow_shrink_continues|Verify strict shrink continues even by one finding.|Tests|FR-CONV.5|`|F|=5,4` continues; no slow-convergence halt; existing cap remains|S|P0|
|17|TEST-018|test_dnsp_twice_exhaust|Verify twice-timeout partition emits DNSP finding with required fields.|Tests|FR-CONV.6,DM-003|severity present; source present; affected_range present; evidence present; recommendation present; dedup_key present; found_n_times present|S|P0|
|18|TEST-019|test_dnsp_dedup_collapse|Verify identical DNSP keys collapse within a cycle.|Tests|DNSP-DEDUP-1|two identical exhaust events; one merged record; found_n_times=2; no data loss|S|P0|
|19|TEST-020|test_dnsp_all_agents_fail_bypass|Verify all-agents-fail path emits no DNSP and activates preserved escalation.|Tests|API-005|zero successes; no `synthetic-dnsp`; rf-team-lead HALT path visible|M|P0|
|20|TEST-021|test_dnsp_does_not_serialize_cohort|Verify sibling partitions continue while one partition exhausts.|Tests|NFR-CONV.10,INV-021|N spawn timestamps overlap; exhausted partition emits; N-1 complete; no serial cohort behavior|M|P0|
|21|TEST-022|test_synthetic_dnsp_dedup_not_regression|Verify same DNSP dedup key across cycles is not treated as PASS-to-FAIL regression.|Tests|INV-012,FR-CONV.5,FR-CONV.6|same key cycles 1+2; other findings shrink; no regression halt; cycle 3 attempted|M|P0|

### Integration Points — M4

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`[HALT-MONOTONICITY]` message|Fix-loop signal|Yes|M4|rf-task-builder loop; operators|
|Regression halt message|Fix-loop signal|Yes|M4|rf-task-builder loop; operators|
|synthetic-dnsp block|Structured finding|Yes|M4|QA merge; Risk review; OPS-002|
|dedup_key|Finding identity|Yes|M4|FR-CONV.5 F_n set; DNSP collapse|
|rf-team-lead.md:417 escalation|Escalation guard|Yes|M4|All-agents-fail path|

### Milestone Dependencies — M4

- M4 depends on M3 stable verdict tables and M2 deterministic failure-set item identities.

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Monotonicity guard halts legitimate slow-cycle correction|Medium|Low|Valid fix cycles stop early|Only non-shrink halts; strict shrink continues; no slow-shrink threshold|rf-task-builder maintainer|
|2|DNSP masks all-agents-fail escalation|High|Low|Total partition failure appears as partial finding|Zero-success branch emits no DNSP; API-005 test protects rf-team-lead path|Architect|
|3|Dedup-key instability creates false regressions|Medium|Low|Retry loop halts on same underlying failure|Canonical list form; closed exhaust vocabulary; INV-012 fixture|rf-qa maintainer|

## M5: Validation, Rollout, and Operations

**Objective:** Complete invariant fixtures, serial rollout, post-merge audits, token measurement, and operational runbooks for v3.9 GA | **Duration:** 2026-08-17 to 2026-09-30 (6.5 weeks) | **Entry:** M4 retry and DNSP fixtures pass | **Exit:** all 25 tests pass; `make verify-sync` 100%; first-5-run audit PASS; token-cost ratio ≤1.10; v3.9 GA readiness accepted

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|NFR-CONV.3|Hidden-input determinism guard|Validate `.dev/tasks/done/` contents do not alter structural output.|Determinism Tests|M4|fixture-populated done tree; empty done tree; byte-identical structural fields; PR-05 rejected in v3.9|M|P0|
|2|NFR-CONV.4|Token-cost ceiling measurement|Measure post-merge/pre-merge token-cost ratio on 5 representative BUILD_REQUESTs.|Cost Metrics|M4|5 representative requests; Quick/Standard/Deep covered; ratio ≤1.10; K-010 action if exceeded|M|P0|
|3|NFR-CONV.5|No new dependency verification|Verify no new external dependencies, network calls, or tools beyond Read/Grep/Glob/Bash are introduced.|Architecture QA|M4|diff inspected; no package added; no synchronous network call; only existing local tools referenced|S|P0|
|4|TEST-023|test_hidden_input_guard|Implement fixture proving hidden-input determinism against populated `.dev/tasks/done/`.|Tests|NFR-CONV.3|structural output byte-diff zero; same BUILD_REQUEST; same source tree|M|P0|
|5|TEST-024|test_sequencing_PR06_before_PR04|Implement sequencing inversion guard for dynamic enumeration.|Tests|FR-CONV.1,FR-CONV.3|if PR-04 observed before PR-06, catalogue richens once active; sequencing warning emitted; structural assertion passes|S|P1|
|6|TEST-025|test_invariant_preservation_NFR_6_through_10|Implement composite invariant preservation fixture.|Tests|NFR-CONV.6,NFR-CONV.7,NFR-CONV.8,NFR-CONV.9,NFR-CONV.10|self-contained item; evidence-bound item; `.dev/tasks/` layout; zero-trust QA; parallel-research all pass|L|P0|
|7|MIG-001|FR-CONV.1 landing|Land PR-06 structural checks first.|Rollout|Q-DM-1,M2|TB-Add lines append only; rollback per check or commit; sync verified; design approval complete|M|P0|
|8|MIG-002|FR-CONV.2 landing|Land PR-01 Execution Context second.|Rollout|MIG-001|header generation enabled; no paths in header; rollback disables header; M1.1 PASS prerequisite|S|P0|
|9|MIG-003|FR-CONV.3 landing|Land PR-04 inherited verdict third.|Rollout|MIG-002|passthrough enabled; rollback disables block; Self-Audit audit path active; M1.2 PASS prerequisite|M|P0|
|10|MIG-004|FR-CONV.4 landing|Land PR-07 adversarial axes fourth.|Rollout|MIG-003|axis column and section enabled; overlay-only; rollback removes axis column/annotation; checklist untouched|S|P0|
|11|MIG-005|FR-CONV.5 landing|Land PR-02 retry monotonicity fifth.|Rollout|MIG-004|two guards enabled in existing loops; rollback disables guards individually; no new stage|M|P0|
|12|MIG-006|FR-CONV.6 landing|Land PR-03 DNSP sixth.|Rollout|MIG-005|DNSP emits after exhaust; all-agents-fail preserved; rollback removes DNSP edit sites; M1.5 PASS prerequisite|M|P0|
|13|MIG-007|Post-merge audit and measurement|Run K-003 audit and NFR-CONV.4 token measurement after all FRs land.|Rollout|MIG-006,NFR-CONV.4|first 5 rf-qa-qualitative runs audited; 5 BUILD_REQUEST token ratio measured; contingency decisions recorded|L|P0|
|14|OPS-001|K-003 audit-target runbook|Document qualitative Self-Audit triage for first 5 runs post-FR-CONV.3.|Operations|FR-CONV.3|symptom missing Self-Audit; diagnosis grep report; resolution adjust prompt/disable passthrough; escalation QA Lead immediate|S|P0|
|15|OPS-002|DNSP triage runbook|Document HIGH synthetic-dnsp finding triage.|Operations|FR-CONV.6|symptom source synthetic-dnsp; diagnosis evidence log; resolution manual review; escalation ≥3 distinct keys/week|S|P0|
|16|OPS-003|All-partitions-exhaust runbook|Document preserved zero-success HALT path with no DNSP emitted.|Operations|API-005|zero successes confirmed; rf-team-lead.md:417 fired; no synthetic block; maintainer escalation on misfire|S|P1|
|17|OPS-004|Monotonicity halt rate runbook|Document `[HALT-MONOTONICITY]` triage for >50% of fix-cycle batches.|Operations|FR-CONV.5|sample 3 halt events; inspect BUILD_REQUESTs; improve upstream request; consider TB-Add-2 calibration|S|P1|
|18|OPS-005|Regression halt rate runbook|Document regression halt triage for >20% of fix-cycle batches.|Operations|FR-CONV.5|sample 3 events; inspect cycle diff; tighten fix-cycle prompts; Engineering Lead escalation|S|P1|
|19|OPS-006|Sync verification runbook|Document `make verify-sync` failure recovery.|Operations|A-001|rerun sync; inspect git status; revert direct `.claude/` edit if needed; immediate escalation per author|S|P0|
|20|OPS-007|Layout change runbook|Document INV-018 `.dev/tasks/` layout-change response.|Operations|NFR-CONV.8|detect schema drift; inspect all FR path references; re-integration commit covering all 6 FRs; Engineering Lead escalation|M|P0|
|21|SC-001|Single-pass gate PASS metric|Measure representative first-cycle gate PASS rate.|QA Metrics|NFR-CONV-R1|baseline ≥80%; trend upward expected; failures categorized by TB-Add and pre-existing checks|S|P1|
|22|SC-002|Structural defect detection metrics|Validate TB-Add-1 and TB-Add-4 detection targets.|QA Metrics|TEST-001,TEST-002|TB-Add-1 100%; TB-Add-4 100%; fixture report retained|S|P0|
|23|SC-003|Self-Audit coverage metric|Validate 100% Self-Audit coverage on first 5 real qualitative runs.|QA Metrics|OPS-001|5/5 reports contain Self-Audit; ≥1 semantic check each; release blocked on miss|M|P0|
|24|SC-004|Halt and DNSP operational metrics|Measure monotonicity, regression, and DNSP rates after landing.|QA Metrics|OPS-002,OPS-004,OPS-005|monotonicity <10% target; regression <5% target; DNSP healthy run 0; twice-exhaust fixture ≥1|M|P1|
|25|REL-001|v3.9 GA readiness gate|Confirm release checklist and timeline mapping are complete before GA.|Release|MIG-007,TEST-025|all 6 FRs done; no high/critical bugs open; Q-DM-1 resolved; verify-sync pass after each FR; serial order visible; end date ≤2026-09-30|M|P0|

### Integration Points — M5

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`make sync-dev` / `make verify-sync`|Release gate|Yes|M5|Every FR landing and GA readiness|
|Synthetic fixture suite TEST-001..025|Validation suite|Yes|M5|Release checklist|
|K-003 first-5-run audit|Manual QA gate|Yes|M5|FR-CONV.3 stabilization|
|NFR-CONV.4 token measurement|Cost gate|Yes|M5|GA readiness and K-010 contingency|
|Operational runbooks OPS-001..007|Runbook set|Yes|M5|Maintainers and QA Lead|

### Milestone Dependencies — M5

- M5 depends on all M1-M4 implementation rows, the serial landing order PR-06 → PR-01 → PR-04 → PR-07 → PR-02 → PR-03, and successful sync verification after each FR.

### Open Questions — M5

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OPEN-PR05|When does `.dev/tasks/done/` reach ≥10 tasks across ≥3 distinct task_types to re-evaluate PR-05?|Determines Phase-2 timing only; not a v3.9 blocker|Engineering Lead|Each major release|
|2|OPEN-INV-006|What calibrated item-count bounds should replace TB-Add-2 advisory thresholds?|TB-Add-2 remains advisory until calibrated|Engineering|Phase-2|
|3|OPEN-INV-017|How should historical-file staleness be checked if PR-05 returns in Phase-2?|Deferred with PR-05; no v3.9 impact|Engineering|When PR-05 re-evaluated|
|4|OPEN-INV-018|What formal contract governs future `.dev/tasks/` layout changes?|Layout changes require all-FR re-integration|Engineering Lead|Before any layout change|
|5|OPEN-X-002|Can reliance versus verification be empirically observed in first 5 rf-qa-qualitative runs?|K-003 audit determines whether FR-CONV.3 remains enabled|QA Lead|Post-MIG-003 first 5 runs|
|6|OPEN-TOKEN|Does the post-merge/pre-merge token ratio stay ≤1.10 on 5 representative BUILD_REQUESTs?|Blocks GA or triggers K-010 contingency|Engineering Lead|Post-MIG-006|

### Risk Assessment and Mitigation — M5

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Token-cost ratio exceeds ≤1.10|Medium|Low|Cost ceiling missed|Measure 5 representative BUILD_REQUESTs; summarize inherited verdict if exceeded|Engineering Lead|
|2|Sync verification fails late in rollout|High|Low|Source/dev copies diverge|Run verify-sync after each FR; revert direct `.claude/` edits|Per-commit author|
|3|`.dev/tasks/` layout changes before GA|High|Low|All path assumptions invalidated|Freeze layout through v3.9; re-integrate all 6 FRs if changed|Engineering Lead|

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By Milestone|Status|Fallback|
|---|---|---|---|
|None — NFR-CONV.5 forbids new external dependencies and synchronous network calls|M1-M5|Confirmed constraint|Use existing Read, Grep, Glob, Bash only|
|5 representative BUILD_REQUESTs for measurement|M5|Needed post-MIG-006|Use Quick/Standard/Deep internal fixtures if real samples unavailable|
|First 5 real rf-qa-qualitative runs after FR-CONV.3|M5|Needed post-MIG-003|Block FR-CONV.3 stabilization until enough runs exist|

### Infrastructure Requirements

- No database, queue, service, container, network endpoint, or deployment target is required.
- Existing local development stack only: UV for tests, Make targets for sync, Git for review and rollback.
- Git-tracked `.dev/tasks/to-do/TASK-*/` artifacts remain the persistence layer; no `.dev/tasks/` layout change is allowed in v3.9.
- Maintainer coverage required: task-builder, rf-qa, rf-qa-qualitative, rf-analyst, rf-task-builder, rf-team-lead, QA Lead, Engineering Lead.

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|R-001|Q-DM-1 remains unresolved and blocks structural gate work|M1,M2|Medium|High|Treat as M1 exit blocker; choose schema path before FR-CONV.1|Engineering Lead|
|R-002|Scope guardrails are weakened during planning|M1|Low|Medium|Use NG-001 and PRD scope guardrails before implementation rows ship|Architect|
|R-003|TB-Add false positives consume fix cycles|M2,M5|Low|Medium|Ship TB-Add-2 advisory; make each TB-Add individually revertable|rf-qa maintainer|
|R-004|Execution Context drifts from item Context fields|M2|Low|Medium|TB-Add-7 cross-validates source areas; degrade to References-only when needed|task-builder maintainer|
|R-005|Per-item schema decision applied inconsistently|M2|Low|High|Tie DM-004 and TB-Add-8 to Q-DM-1; block merge on mismatch|Engineering Lead|
|R-006|Inherited verdict causes qualitative review inflation|M3,M5|Low|High|Self-Audit obligation; first 5 runs audited; anti-inflation text preserved|QA Lead|
|R-007|Axis annotations over-classify benign rows|M3,M5|Low|Medium|Axes annotation-only; 15-item checklist remains authority; tune after audit|rf-qa-qualitative maintainer|
|R-008|Stale verdict injected on fix-cycle rerun|M3|Low|High|INV-002 cycle reread; TEST-008 blocks stale content|task-builder maintainer|
|R-009|Monotonicity guard halts legitimate slow-cycle correction|M4,M5|Low|Medium|Only non-shrink halts; strict shrink continues; no slow-shrink threshold|rf-task-builder maintainer|
|R-010|DNSP masks all-agents-fail escalation|M4|Low|High|Zero-success branch emits no DNSP; API-005 preserves rf-team-lead path|Architect|
|R-011|Dedup-key instability creates false regressions|M4|Low|Medium|Canonical list form; closed exhaust vocabulary; INV-012 fixture|rf-qa maintainer|
|R-012|Token-cost ratio exceeds ≤1.10|M5|Low|Medium|Measure 5 BUILD_REQUESTs; summarize inherited verdict if exceeded|Engineering Lead|
|R-013|Sync verification fails late in rollout|M5|Low|High|Run verify-sync after each FR; revert direct `.claude/` edits|Per-commit author|
|R-014|`.dev/tasks/` layout changes before GA|M5|Low|High|Freeze layout through v3.9; re-integrate all 6 FRs if changed|Engineering Lead|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|Milestone|
|---|---|---|---|---|
|Structural determinism|NFR-CONV.1 structural byte-diff|0 diff|Run identical BUILD_REQUEST twice and diff TB-Add verdicts, DNSP fields, axis values, Items Reviewed structure|M5|
|Hidden-input determinism|NFR-CONV.3 structural byte-diff|0 diff|Compare empty `.dev/tasks/done/` and populated `.dev/tasks/done/` outputs|M5|
|Token-cost containment|post-merge/pre-merge ratio|≤1.10|Measure 5 representative BUILD_REQUESTs across Quick/Standard/Deep|M5|
|No new dependency|external dependencies/network calls|0|Diff source and tool references; verify Read/Grep/Glob/Bash only|M5|
|Single-pass gate health|first-cycle PASS rate|≥80% baseline; trend upward|Representative BUILD_REQUEST gate run report|M5|
|TB-Add-1 detection|initial-text defect fixture|100%|TEST-001 synthetic fixture|M2|
|TB-Add-4 detection|DAG cycle fixture|100%|TEST-002 synthetic fixture|M2|
|Self-Audit coverage|first 5 qualitative runs|100%|OPS-001 audit of rf-qa-qualitative reports|M5|
|Monotonicity halt target|fix-cycle batches|<10% target; >50% investigation threshold|Grep `[HALT-MONOTONICITY]` in execution logs|M5|
|Regression halt target|fix-cycle batches|<5% target; >20% investigation threshold|Grep regression halt message in execution logs|M5|
|DNSP fixture behavior|twice-exhaust / healthy runs|≥1 on twice-exhaust; 0 on healthy|TEST-018 plus healthy-control run|M4|
|Sync discipline|verify-sync pass rate|100%|Run `make sync-dev` then `make verify-sync` after each FR|M5|
|Invariant preservation|NFR-CONV.6..10 composite|100%|TEST-025 composite fixture|M5|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|---|---|---|---|
|Merge approach|Intent-port sc-tasklist rigor into task-builder idioms|Implementation-port; do nothing|Avoids bundle-specific mechanics while closing known structural gaps|
|Governance|A-002 strictly additive|Single mega-change; replacement of checklists|Per-FR rollback granularity and invariant preservation matter more than one-shot simplicity|
|Structural checks|8 TB-Add checks only|Bulk-port all 17/20 sc-tasklist checks|Per-check classification avoids phase-file and bundle-only checks that do not apply to single MDTM output|
|Execution Context scope|Task-level header with no file paths; per-item citations retained|No header; path-rich header|Balances executor readability with hidden-input determinism and evidence-bound item invariant|
|Inherited verdict|Verbatim rf-qa table plus Self-Audit|Pure passthrough; full mechanical recheck|Focuses qualitative review on semantic risk while preserving anti-inflation control|
|Axis model|Five annotation axes plus `none` sentinel|Replace 15-item checklist; omit axes|Axes add taxonomy without weakening the validated qualitative checklist|
|Retry halt logic|Regression first, monotonicity second, hard cap third|Pure cardinality only; slow-shrink halt|Catches PASS-to-FAIL regressions while allowing legitimate strict-shrink progress|
|DNSP emission|Partial partition exhaust emits HIGH synthetic finding; all-fail escalates normally|Always emit DNSP; never emit DNSP|Preserves all-agents-fail HALT while surfacing partial silent exhaust|
|Timeline anchoring|Finish by 2026-09-30 within PRD due quarter 2026-Q3|Extend beyond Q3|Default schedule respects PRD due_date and TDD GA anchor|

## Timeline Estimates

|Milestone|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1|1 week|2026-05-14|2026-05-21|TDD Design Complete maps here; Q-DM-1 resolved; architecture contracts frozen|
|M2|4 weeks|2026-05-22|2026-06-19|TDD Phase 1 Structural Gate Reinforcement; PR-06/MIG-001 then PR-01/MIG-002|
|M3|4 weeks|2026-06-22|2026-07-17|TDD Phase 2 Inter-Agent Verdict Channel; PR-04/MIG-003 then PR-07/MIG-004|
|M4|4 weeks|2026-07-20|2026-08-14|TDD Phase 3 Retry & Exhaust Resilience; PR-02/MIG-005 then PR-03/MIG-006|
|M5|6.5 weeks|2026-08-17|2026-09-30|TDD Phase 4 Post-merge Audit + Measurement; MIG-007; v3.9 GA within PRD due_date 2026-Q3|

**Total estimated duration:** 19.5 weeks, 2026-05-14 to 2026-09-30, anchored to TDD Design Complete on 2026-05-21 and PRD v3.9 due quarter 2026-Q3.
