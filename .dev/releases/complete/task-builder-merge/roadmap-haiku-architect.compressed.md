---
spec_source: "TDD_TASK_BUILDER_CONVERGENCE.compressed.md"
complexity_score: 0.7
complexity_class: HIGH
primary_persona: architect
adversarial: true
base_variant: "haiku-architect"
variant_scores: "none"
convergence_score: null
---
# Task-Builder Convergence v3.9 — Project Roadmap

## Executive Summary

Task-Builder Convergence v3.9 ports six strictly-additive rigor mechanisms into the task-builder skill: structural rf-qa checks, an Execution Context header, inherited structural verdict handoff, adversarial-axis annotation, retry monotonicity guards, and synthetic DNSP findings. The roadmap is phased by technical layer while preserving the source-mandated serial landing order PR-06 → PR-01 → PR-04 → PR-07 → PR-02 → PR-03.

**Business Impact:** Reduces silent acceptance of malformed MDTM task files, limits retry oscillation cost, and preserves token-cost growth at ≤1.10 while avoiding new dependencies or network calls.

**Complexity:** HIGH (0.7) — six dependent FRs touch five agent/skill files across about 22 insertion points, require five invariant-preservation fixtures, and carry one critical pre-M1 schema decision.

**Critical path:** Q-DM-1 Engineering Lead decision → FR-CONV.1 TB-Add catalogue → FR-CONV.2 Execution Context header → FR-CONV.3 inherited verdict → FR-CONV.4 axes overlay → FR-CONV.5 retry guards → FR-CONV.6 DNSP emission → audit and token measurement.

**Key architectural decisions:**

- Preserve strict additive governance: no existing stage, checklist item, or agent rule is renamed, renumbered, removed, or weakened.
- Treat structural verdict inheritance as reliance context only; rf-qa-qualitative still performs independent semantic checks and emits Self-Audit evidence.
- Keep all runtime behavior local to existing markdown artifacts and tools; no external dependencies, databases, services, or synchronous network calls.

**Open risks requiring resolution before M1:**

- Q-DM-1 must resolve the PRD-vs-source per-item schema contradiction before FR-CONV.1 can land.

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|---|---|---|---|---|---|---|---|
|M1|Decision and Contract Foundation|Foundation|P0|XL|Q-DM-1|26|High|
|M2|Structural Gate and Execution Context|Core Logic|P0|XL|M1|18|Medium|
|M3|Inter-Agent Verdict and Adversarial Axes|Integration|P0|L|M2|17|Medium|
|M4|Retry Resilience and DNSP Emission|Hardening|P0|L|M3|12|Medium|
|M5|Validation, Rollout, and Operations|Production Readiness|P0|XL|M4|23|Medium|

## Dependency Graph

Q-DM-1 → M1 → M2 → M3 → M4 → M5

FR landing order within milestones: FR-CONV.1 → FR-CONV.2 → FR-CONV.3 → FR-CONV.4 → FR-CONV.5 → FR-CONV.6 → MIG-007.

## M1: Decision and Contract Foundation

**Objective:** Resolve critical schema ambiguity, lock source-of-truth contracts, and establish the component/data/API surfaces that later implementation must preserve. | **Duration:** Weeks 1-2 | **Entry:** TDD approved for planning; Engineering Lead owns Q-DM-1. | **Exit:** Q-DM-1 resolved; all contracts mapped to deliverables; sync and invariant gates defined.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|DM-001|Execution Context Header|Define the MDTM header emitted after frontmatter and before the checklist.|rf-task-builder|Q-DM-1|References:list[string] R-###; Source areas:list[string] named modules no file paths; Key constraints:list[string] 1-3 invariants; degradation:References-only with omitted absent lines|M|P0|
|2|DM-002|Inherited Structural Verdict Block|Define the rf-qa verdict block injected into rf-qa-qualitative spawn prompts.|task-builder/SKILL.md|DM-005|rf_qa_table_verbatim:byte-exact table; prompt_directive:fixed text; reinjection_rule:new cycle verdict; freshness_rule:INV-002; enumeration_rule:INV-010; consumer_obligation:INV-019; anti_inflation:preserved|M|P0|
|3|DM-003|Synthetic DNSP Finding|Define the partition-exhaust HIGH finding emitted into normal agent output.|rf-qa, rf-analyst, rf-qa-qualitative|API-003|severity:HIGH; source:synthetic-dnsp; affected_range:assigned_files slice; evidence:spawn-log path or log-absence citation; recommendation:Manual review required — partition agent failed twice; dedup_key:[range,exhaust_point]; found_n_times:int default 1|M|P0|
|4|DM-004|Per-Item Checklist Schema|Resolve and define the per-item checklist schema affected by TB-Add-8.|task-builder/SKILL.md|Q-DM-1|PRD fields:Description,Context,Acceptance,Confidence,Verification; current fields:Context,Action,Output,Verification,Completion gate; invariant:Context enforced in either schema; decision recorded before FR-CONV.1|L|P0|
|5|DM-005|Phase Contract|Define the rf-qa to rf-qa-qualitative contract governing inherited verdict use.|task-builder/SKILL.md|DM-002|producer:rf-qa; consumer:rf-qa-qualitative; artifact:Inherited Structural Verdict block; schema_version:1.0.0; delivery_semantics:at-most-once-per-cycle; freshness_rule:INV-002; enumeration_rule:INV-010; consumer_obligation:INV-019; anti_inflation:semantic verification required; failure_mode:no verdict halts before A.10.5|M|P0|
|6|API-001|BUILD_REQUEST Contract|Preserve the BUILD_REQUEST to MDTM task-file contract while adding Execution Context requirements.|task-builder/SKILL.md|DM-001|producer:task-builder; consumer:rf-task-builder; transport:Skill prompt plus on-disk MDTM; output:Execution Context block; auth:N/A; rate_limits:N/A; error:MALFORMED max 2|M|P0|
|7|API-002|Structural Verdict Handoff|Define rf-qa task-integrity to rf-qa-qualitative task-qualitative handoff.|task-builder/SKILL.md|DM-002,DM-005|producer:rf-qa; consumer:rf-qa-qualitative; transport:spawn-prompt injection; extraction:contiguous verdict table; placement:after TARGET FILES before INSTRUCTIONS; missing verdict:halt before A.10.5|M|P0|
|8|API-003|Partition Finding Stream|Define partition-agent synthetic DNSP emission into orchestrator merge logic.|rf-qa, rf-analyst, rf-qa-qualitative|DM-003|producer:any partition; consumer:task-builder merge; transport:normal output stream; cardinality:per partition; dedup:within-cycle increments found_n_times; all_fail:zero success routes to rf-team-lead.md:417 no DNSP|M|P0|
|9|API-004|Fix-Loop Halt Signals|Define monotonicity and regression halt messages consumed by retry loops.|rf-task-builder|FR-CONV.5|monotonicity_message:[HALT-MONOTONICITY] \|F\|=<n>; regression_message:verbatim PASS@N to FAIL@N+1; order:regression then monotonicity then hard cap; F_n:dedup-key set|M|P0|
|10|COMP-001|task-builder Orchestrator|Preserve the Stage A skill orchestrator as the central integration surface.|task-builder/SKILL.md|A-001|type:Internal Framework Skill; location:src/superclaude/skills/task-builder/SKILL.md; modifies:FR-CONV.1..6; dependencies:rf-task-researcher,rf-task-builder,rf-qa,rf-analyst,rf-qa-qualitative; forbidden:direct rf-team-lead invocation|L|P0|
|11|COMP-002|rf-task-builder Agent|Define the BUILD_REQUEST consumer and MDTM emitter surface.|rf-task-builder.md|API-001|type:Subagent; location:src/superclaude/agents/rf-task-builder.md; modifies:FR-CONV.5; returns:RESEARCH_NEEDED,MALFORMED,NEED_USER_INPUT; output:${TASK_DIR}${TASK_ID}.md; counters:separate|M|P0|
|12|COMP-003|rf-qa Agent|Define the structural QA agent and task-integrity gate surface.|rf-qa.md|FR-CONV.1|type:Structural QA Agent; location:src/superclaude/agents/rf-qa.md; phases:research-gate,synthesis-gate,report-validation,task-integrity; modifies:FR-CONV.1,FR-CONV.5,FR-CONV.6; anchors:141-142,268-287,49-77,308-315|L|P0|
|13|COMP-004|rf-qa-qualitative Agent|Define the content QA agent consuming inherited verdict and axes overlay.|rf-qa-qualitative.md|API-002|type:Content QA Agent; location:src/superclaude/agents/rf-qa-qualitative.md; phases:7 including task-qualitative; modifies:FR-CONV.3,FR-CONV.4,FR-CONV.6; anchors:527-583,675-714,766-775,786-795,794|L|P0|
|14|COMP-005|rf-analyst Agent|Define completeness and synthesis-review partition agent DNSP surface.|rf-analyst.md|API-003|type:Completeness verification and synthesis review; location:src/superclaude/agents/rf-analyst.md; modifies:FR-CONV.6; anchors:58-71; role:partition adversary at gates 1 and 2|M|P0|
|15|COMP-006|rf-team-lead Preservation|Preserve the existing all-agents-fail escalation guard without modification.|rf-team-lead.md|API-003|type:Project-mode orchestrator; location:src/superclaude/agents/rf-team-lead.md; modifies:none; preserved_anchor:line 417; behavior:max 3 cycles per phase HALT and ask user|S|P0|
|16|NFR-CONV.1|Structural Determinism|Make all structural outputs byte-identical across identical runs.|QA fixtures|M2-M5|TB-Add verdicts:byte-equal; DNSP fields:byte-equal; dedup_key:byte-equal; axis values:byte-equal; Items Reviewed structure:byte-equal|M|P0|
|17|NFR-CONV.2|Prose Determinism Exclusion|Exclude research-driven prose from byte-equality requirements while keeping structural annotations stable.|QA fixtures|NFR-CONV.1|Context prose:not byte-gated; semantic prose:not byte-gated; axis labels:byte-equal; finding counts:byte-equal; dedup_keys:byte-equal|S|P1|
|18|NFR-CONV.3|Hidden Input Determinism|Ensure `.dev/tasks/done/` contents do not alter structural output.|QA fixtures|A-002|empty_done:baseline; populated_done:10+ tasks 3 types; structural_fields:byte-identical; PR-05:rejected Phase-1|M|P0|
|19|NFR-CONV.4|Token-Cost Ceiling|Constrain post-merge token growth per equivalent BUILD_REQUEST.|QA metrics|M5|ratio:post/pre; target:≤1.10; sample:5 representative BUILD_REQUESTs; tiers:Quick/Standard/Deep; contingency:summarise verdict table if exceeded|M|P0|
|20|NFR-CONV.5|Local Checks Boundary|Prevent new dependencies, network calls, libraries, or MCP servers.|All components|A-001|external_deps:none; network_calls:none; libraries:none; allowed_tools:Read,Grep,Glob,Bash; wall_clock:local checks only|S|P0|
|21|NFR-CONV-R1|Single-Pass Gate PASS Rate|Maintain representative first-cycle task-integrity PASS health.|rf-qa|M5|sample:5 BUILD_REQUESTs; target:≥80%; measurement:first-cycle PASS count; failures:route to fix-cycle protocol|S|P1|
|22|NFR-CONV.6|Self-Contained Item Invariant|Preserve the five-field item schema selected by Q-DM-1.|task-builder/SKILL.md|Q-DM-1|fixture_all_5_fields:PASSES; fixture_one_field_stripped:FAILS TB-Add-1; schema:whichever Q-DM-1 selects; source:SKILL.md:~1452-1457|M|P0|
|23|NFR-CONV.7|Evidence-Bound Item Invariant|Require per-item Context to include file:line or justified absence.|task-builder/SKILL.md|FR-CONV.1|Context src/foo:FAIL; Context src/foo:42:PASS; Context <none — pure refactor> [justified-absence]:PASS; source:SKILL.md:1530 rule #2|M|P0|
|24|NFR-CONV.8|Persistent Artifact Invariant|Preserve `.dev/tasks/` directory layout and artifact names.|task-builder/SKILL.md|OPEN-INV-018|layout_changes:zero; dirs:research,qa,synthesis,reviews,adversarial unchanged; naming_pattern:unchanged; source:SKILL.md:1536 rule #5|M|P0|
|25|NFR-CONV.9|Zero-Trust QA Invariant|Preserve any-gap-fails verdict semantics.|rf-qa.md|FR-CONV.1|PASS:all checks pass no gaps; FAIL:any gap CRITICAL/IMPORTANT/MINOR; one_LOW_finding:FAIL; inherited_verdict:no VERIFIED without semantic Self-Audit|M|P0|
|26|NFR-CONV.10|Parallel-Research Invariant|Preserve concurrent partition behavior with within-agent DNSP emission.|rf-qa.md, rf-qa-qualitative.md|FR-CONV.6|spawn:N partitions concurrently; timing:overlap proves concurrency; exhausted_partition:synthesises DNSP; sibling_partitions:continue to completion; no cohort serialization|M|P0|

### Integration Points — M1

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|BUILD_REQUEST|Skill prompt contract|Yes|M1|rf-task-builder|
|Inherited Structural Verdict|Spawn-prompt block|Defined in M1, wired in M3|M3|rf-qa-qualitative|
|synthetic-dnsp finding|Agent output block|Defined in M1, wired in M4|M4|task-builder merge logic|
|Fix-loop halt messages|Retry-loop ABI|Defined in M1, wired in M4|M4|rf-task-builder|
|src/superclaude → .claude sync|Build tooling|Yes|M1-M5|all FR commits|

### Milestone Dependencies — M1

- Q-DM-1 Engineering Lead decision blocks M1 exit and FR-CONV.1 entry.
- A-001 source-of-truth workflow must be accepted before editing any component.

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|Q-DM-1|Per-Item Checklist Schema PRD-vs-source contradiction: PRD asserts {Description, Context, Acceptance, Confidence, Verification}; current SKILL.md shows {Context, Action, Output, Verification, Completion gate}. Source: TDD §22.|Blocks FR-CONV.1 and NFR-CONV.6 fixture target.|Engineering Lead|Pre-FR-CONV.1 implementation|
|2|OPEN-INV-018|If `.dev/tasks/` directory layout changes, all proposals require re-integration. Source: TDD §22.|Blocks persistent-artifact invariant and contract paths.|Engineering Lead|Before M2 implementation starts|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Q-DM-1 schema ambiguity leads to implementing checks against the wrong item fields.|High|Medium|FR-CONV.1 fixtures become invalid or non-additive.|Resolve Q-DM-1 before any TB-Add work; record selected schema in DM-004.|Engineering Lead|
|2|A-001 sync-discipline is bypassed during contract edits.|Medium|Low|Definitions drift between source and dev copies.|Edit only src/superclaude first; run make sync-dev and make verify-sync per FR.|Per-commit author|
|3|`.dev/tasks/` layout dependency changes after contracts are planned.|High|Low|All path-based contracts need re-integration.|Track OPEN-INV-018; add layout contract to M1 exit criteria.|Engineering Lead|

## M2: Structural Gate and Execution Context

**Objective:** Land FR-CONV.1 then FR-CONV.2, giving task-integrity deterministic structural checks and generated task files an executor-readable context header. | **Duration:** Weeks 3-5 | **Entry:** M1 exit complete; Q-DM-1 resolved. | **Exit:** FR-CONV.1 and FR-CONV.2 merged in order; TB-Add fixtures and Execution Context fixtures pass; make verify-sync passes after each FR.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-CONV.1|Structural Check Catalogue|Append TB-Add-1..8 to rf-qa A.10 and mirror the catalogue across all required definition surfaces.|rf-qa.md, task-builder/SKILL.md|M1|TB-Add-1/3/4/5/6/7/8:block; TB-Add-2:[ADVISORY] nonblocking; errors:name item ID; surfaces:rf-qa 20-item,SKILL A.10,SKILL validation block; no existing item renamed/removed|XL|P0|
|2|FR-CONV.2|Execution Context Header|Insert task-level Execution Context block after frontmatter and before checklist.|rf-task-builder, task-builder/SKILL.md|FR-CONV.1|full_build:References/Source areas/Key constraints; minimal_build:References-only; header_paths:zero src/ or file:line; per_item_Context:file:line or justified-absence retained|L|P0|
|3|TB-Add-1|Unresolved-Token Scan|Detect unresolved or title-only checklist items in generated MDTM files.|rf-qa.md|FR-CONV.1|tokens:TBD/TODO/title-only; severity:Hard; result:gate FAIL; message:names TB-Add-1 and item ID|S|P0|
|4|TB-Add-2|Item-Count Bounds Advisory|Warn when task item counts fall outside calibrated bounds.|rf-qa.md|FR-CONV.1|lower_bound:≥3; track_bound:≤40-track; single_track_bound:≤50-single-track; prefix:[ADVISORY]; blocking:false until OPEN-INV-006|S|P1|
|5|TB-Add-3|Clarification Adjacency|Ensure clarification items are adjacent to the item or decision they clarify.|rf-qa.md|FR-CONV.1|severity:Hard; violation:names item ID; gate:FAIL; no bundle-specific tasklist checks|S|P0|
|6|TB-Add-4|Dependency DAG Check|Detect circular dependencies within and across task phases.|rf-qa.md|FR-CONV.1|graph:intra/inter-phase; cycle:detected; severity:Hard; gate:FAIL; error:names dependency path and item ID|M|P0|
|7|TB-Add-5|Granularity Check|Detect oversized XL items that lack decomposed subtasks.|rf-qa.md|FR-CONV.1|XL_without_subtasks:FAIL; severity:Hard; item_ID:named; remediation:split item or justify smaller scope|S|P0|
|8|TB-Add-6|Confidence Verification Consistency|Validate Confidence and Verification format consistency per the selected schema.|rf-qa.md|DM-004|Confidence:HIGH/MEDIUM/LOW plus rationale when schema includes it; Verification:concrete command/inspection/test; mismatch:FAIL; item_ID:named|M|P0|
|9|TB-Add-7|Source Areas Cross-Validation|Require Execution Context source areas to reappear in item Context fields.|rf-qa.md|FR-CONV.2|header_source_area:present in ≥1 item Context; degraded_header:References-only tolerated; mismatch:FAIL; item_ID or header field named|M|P0|
|10|TB-Add-8|Context Citation Enforcement|Require each item Context to include a file:line citation or justified-absence comment.|rf-qa.md|DM-004|Context src/foo:FAIL; Context src/foo:42:PASS; Context justified-absence:PASS; resolves:INV-015; severity:Hard|M|P0|
|11|MIG-001|FR-CONV.1 Landing|Land PR-06 first as the structural gate foundation.|rf-qa.md, task-builder/SKILL.md|Q-DM-1|order:1st; dependency:Q-DM-1; rollback:revert TB-Add append lines or PR-06 commit; sync:make verify-sync PASS|M|P0|
|12|MIG-002|FR-CONV.2 Landing|Land PR-01 second after TB-Add catalogue is active.|task-builder/SKILL.md|MIG-001|order:2nd; dependency:MIG-001 PASS; rollback:disable header generation; per-item Context unchanged; sync:make verify-sync PASS|M|P0|
|13|TEST-001|TBD Scan Fixture|Verify TB-Add-1 detects TBD/TODO/title-only items.|Tests|TB-Add-1|input:item with TBD/TODO/title-only; assert:TB-Add-1 emits item-ID error; gate:FAIL|S|P0|
|14|TEST-002|DAG Cycle Fixture|Verify TB-Add-4 detects circular dependencies.|Tests|TB-Add-4|input:circular dependency; assert:TB-Add-4 emits; gate:FAIL; cycle path visible|S|P0|
|15|TEST-003|Evidence-Bound Fixture|Verify TB-Add-8 distinguishes bare path from file:line citation.|Tests|TB-Add-8|bare Context src/foo:FAIL; Context src/foo:42:PASS; justified-absence:PASS|S|P0|
|16|TEST-004|Execution Context Full Fixture|Verify full Execution Context renders three labeled lines.|Tests|FR-CONV.2|grep Execution Context:found; next 10 lines:References+Source areas+Key constraints; placement:after frontmatter before Phase 1|S|P0|
|17|TEST-005|Execution Context Minimal Fixture|Verify minimal BUILD_REQUEST degrades to References-only.|Tests|FR-CONV.2|minimal GOAL:References-only; Source areas:omitted; Key constraints:omitted; no blank labels|S|P0|
|18|TEST-006|Execution Context Path Guard Fixture|Verify the header contains no concrete file paths or line citations.|Tests|FR-CONV.2|grep -E src/ or /.*:[0-9]+ over header:0 hits; per-item Context citations remain outside header|S|P0|

### Integration Points — M2

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|TB-Add-1..8 catalogue|rf-qa checklist and SKILL mirror|Yes|M2|rf-qa task-integrity, rf-qa-qualitative inherited enumeration|
|Execution Context header|MDTM markdown section|Yes|M2|TB-Add-7, task executors|
|Per-item Context citations|MDTM item field|Yes|M2|TB-Add-8, rf-qa task-integrity|
|make verify-sync|Sync gate|Yes|M2|release checklist|

### Milestone Dependencies — M2

- M1 must resolve Q-DM-1 and freeze DM-004 before TB-Add-6 and TB-Add-8 fixtures can be final.
- FR-CONV.1 must land before FR-CONV.2 so TB-Add-7 and TB-Add-8 can validate the header/item boundary.

### Open Questions — M2

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OPEN-INV-006|Empirical calibration of TB-Add-2 item-count bounds (≥3 / ≤40 track / ≤50 single-track). Source: TDD §22.|TB-Add-2 remains advisory and cannot become blocking in v3.9.|Engineering|Phase-2 with PR-05|

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|TB-Add false positives waste fix cycles.|Low|Low|Extra cycles and operator review.|Keep TB-Add-2 advisory; make each TB-Add individually revertable; ensure errors cite item ID.|rf-qa maintainer|
|2|Execution Context header drifts from item Context fields.|Low|Low|Executor sees misleading task-level context.|TB-Add-7 cross-validates source areas against item Context fields.|task-builder maintainer|
|3|Per-item evidence gets moved from items into the header.|Medium|Low|Evidence-bound-item invariant weakens.|FR-CONV.2 negative criterion keeps file:line citations in item Context only.|Engineering|

## M3: Inter-Agent Verdict and Adversarial Axes

**Objective:** Wire rf-qa structural verdicts into rf-qa-qualitative without weakening semantic verification, then add task-qualitative adversarial-axis annotations. | **Duration:** Weeks 6-8 | **Entry:** M2 exit complete; TB-Add catalogue and Execution Context header active. | **Exit:** FR-CONV.3 and FR-CONV.4 merged in order; inherited verdict freshness, Self-Audit, axes, and severity-floor fixtures pass.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-CONV.3|Inherited Structural Verdict|Inject rf-qa task-integrity verdict into rf-qa-qualitative spawn prompt with Self-Audit obligation.|task-builder/SKILL.md, rf-qa-qualitative.md|FR-CONV.2|block:## Inherited Structural Verdict; table:byte-for-byte; directive:fixed PASS/FAIL text; rerun:new cycle verdict; output:## Self-Audit with PASS reliance and ≥1 semantic check; anti_inflation:unchanged|L|P0|
|2|FR-CONV.4|Five Adversarial Axes|Add axes subsection and Items Reviewed axis column before the 15-item task-qualitative checklist.|rf-qa-qualitative.md|FR-CONV.3|header:before 15-item checklist; axis column:populated per row; values:drift/contradictions/omissions/weakened-criteria/invented-content/none; drift-axis-inactive emitted when no GOAL baseline; checklist order unchanged|L|P0|
|3|AX-1|Drift Axis|Define stale citation/config/signature/count detection lens for task-qualitative review.|rf-qa-qualitative.md|FR-CONV.4|name:Drift; detects:cited fact no longer matches current source; values:AX-1 or none; inactive_annotation:drift-axis-inactive when no citations exist|S|P0|
|4|AX-2|Contradictions Axis|Define incompatibility lens for artifacts or sections about the same subject.|rf-qa-qualitative.md|FR-CONV.4|name:Contradictions; detects:mutually incompatible assertions; severity_floor:IMPORTANT/CRITICAL unchanged; values:AX-2 or none|S|P0|
|5|AX-3|Omissions Axis|Define missing touchpoint, consumer, dependency, or step detection lens.|rf-qa-qualitative.md|FR-CONV.4|name:Omissions; detects:required touchpoint/consumer/dependency/step absent; values:AX-3 or none; no new checklist count|S|P0|
|6|AX-4|Weakened Criteria Axis|Define softened acceptance or verification condition detection lens.|rf-qa-qualitative.md|FR-CONV.4|name:Weakened criteria; detects:unobservable/trivially satisfiable criteria; values:AX-4 or none; no severity weakening|S|P0|
|7|AX-5|Invented Content Axis|Define upstream-unsupported requirement or capability detection lens.|rf-qa-qualitative.md|FR-CONV.4|name:Invented content; detects:requirement/feature/capability not present upstream; values:AX-5 or none; no out-of-scope implementation added|S|P0|
|8|MIG-003|FR-CONV.3 Landing|Land PR-04 third after Execution Context and TB-Add catalogue are live.|task-builder/SKILL.md, rf-qa-qualitative.md|MIG-002|order:3rd; dependency:MIG-002 PASS; rollback:disable passthrough block; fallback:independent structural re-checking; audit:first 5 runs|M|P0|
|9|MIG-004|FR-CONV.4 Landing|Land PR-07 fourth as an overlay over the existing task-qualitative checklist.|rf-qa-qualitative.md|MIG-003|order:4th; dependency:MIG-003 PASS; rollback:remove axis column and drift-axis-inactive annotation; checklist:untouched|M|P0|
|10|TEST-007|Inherited Verdict Presence Fixture|Verify the inherited structural verdict block appears in the rf-qa-qualitative spawn prompt.|Tests|FR-CONV.3|grep block header:found; placement:under Inherited Structural Verdict; source table:from rf-qa task-integrity report|S|P0|
|11|TEST-008|Inherited Verdict Freshness Fixture|Verify fix-cycle reruns inject the current cycle verdict rather than an older verdict.|Tests|FR-CONV.3|cycle1_table:differs from cycle2_table; cycle2_spawn:contains cycle2 verdict; stale_verdict:absent|S|P0|
|12|TEST-009|Self-Audit Fixture|Verify rf-qa-qualitative lists reliance and independent semantic checks.|Tests|FR-CONV.3|output:## Self-Audit; relied_PASS_items:listed; semantic_checks:≥1; VERIFIED solely from inherited verdict:forbidden|S|P0|
|13|TEST-010|Dynamic Enumeration Fixture|Verify inherited verdict handling auto-picks up TB-Add catalogue growth.|Tests|FR-CONV.3|catalogue_change:reflected in task-qualitative context; fixed-count:none; INV-010:PASS|S|P0|
|14|TEST-011|Axes Ordering Fixture|Verify Five Adversarial Axes appears before the immutable 15-item checklist.|Tests|FR-CONV.4|grep order:axes header before checklist; checklist items:unchanged; total:15|S|P0|
|15|TEST-012|Axis Column Fixture|Verify every Items Reviewed row carries one canonical axis value.|Tests|FR-CONV.4|axis column:present; each row:AX-1/AX-2/AX-3/AX-4/AX-5/none; empty cells:0|S|P0|
|16|TEST-013|Drift Axis Inactive Fixture|Verify no GOAL-baseline item emits the drift-axis-inactive summary annotation.|Tests|FR-CONV.4|input:no GOAL restatement; output:drift-axis-inactive; not N/A; one annotation only|S|P1|
|17|TEST-014|Severity Floor Fixture|Verify rf-qa-qualitative severity floor remains unchanged.|Tests|FR-CONV.4|critical rules block:byte-stable; contradictions:IMPORTANT/CRITICAL; severity weakening:absent|S|P0|

### Integration Points — M3

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|rf-qa task-integrity table|QA report table|Yes|M3|Inherited Structural Verdict block|
|Inherited Structural Verdict block|Spawn-prompt injection|Yes|M3|rf-qa-qualitative|
|Self-Audit section|QA output section|Yes|M3|K-003 audit and release checklist|
|Axis column|Items Reviewed table field|Yes|M3|task-qualitative review consumers|
|Five Adversarial Axes|Checklist overlay|Yes|M3|rf-qa-qualitative reviewers|

### Milestone Dependencies — M3

- FR-CONV.3 depends on M2 so the inherited table includes the TB-Add catalogue and Execution Context validation results.
- FR-CONV.4 depends on FR-CONV.3 because the axes should focus on semantic review, not duplicate inherited structural PASS items.

### Open Questions — M3

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OPEN-X-002|PR-04 anti-inflation operational test: reliance versus verification is empirically observable, not structurally provable. Source: TDD §22.|Blocks declaring FR-CONV.3 stable until first 5 runs are audited.|QA Lead|First 5 rf-qa-qualitative runs after FR-CONV.3|

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Inherited verdict passthrough causes rf-qa-qualitative inflation.|Medium|Low|Semantic defects marked verified without independent evidence.|Require Self-Audit and audit first 5 runs; preserve anti-inflation text unchanged.|QA Lead|
|2|Axis annotation ambiguity over-flags items.|Low|Low|Review noise increases.|Keep axes annotation-only; tune axis rules after distribution audit.|rf-qa-qualitative maintainer|
|3|FR-CONV.3 lands before FR-CONV.1 catalogue is active.|Medium|Low|Dynamic enumeration misses TB-Add checks.|Enforce serial order through M2 dependency and release checklist.|Engineering Lead|

## M4: Retry Resilience and DNSP Emission

**Objective:** Add deterministic retry halt conditions and make partition escalation-ladder exhaust visible as HIGH findings without replacing the all-agents-fail halt path. | **Duration:** Weeks 9-10 | **Entry:** M3 exit complete; inherited verdict and axes are stable enough to feed fix-cycle verdict sets. | **Exit:** FR-CONV.5 and FR-CONV.6 merged in order; monotonicity, regression, DNSP, dedup, and concurrency fixtures pass.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-CONV.5|Retry Halt Guards|Add monotonicity and regression stop conditions to existing retry loops only.|rf-task-builder.md, rf-qa.md, task-builder/SKILL.md|FR-CONV.4|regression_precedence:first; regression_message:verbatim; monotonicity:halt if \|F_{n+1}\|>=\|F_n\|; monotonicity_message:[HALT-MONOTONICITY]\|F\|=<n>; strict_shrink:continues; counters:not collapsed|L|P0|
|2|FR-CONV.6|Synthetic DNSP Emission|Emit HIGH synthetic-dnsp finding when one partition exhausts and at least one sibling succeeds.|rf-qa.md, rf-analyst.md, rf-qa-qualitative.md, task-builder/SKILL.md|FR-CONV.5|condition:≥1 success and ≥1 exhaust; fields:severity/source/affected_range/evidence/recommendation/dedup_key/found_n_times; zero_success:no synthetic, rf-team-lead.md:417; dedup:within-cycle only|L|P0|
|3|MIG-005|FR-CONV.5 Landing|Land PR-02 fifth with existing-loop-only retry guards.|rf-task-builder.md, rf-qa.md|MIG-004|order:5th; dependency:MIG-004 PASS; rollback:disable guards individually; no new loop/stage; hard_cap:preserved|M|P0|
|4|MIG-006|FR-CONV.6 Landing|Land PR-03 sixth with per-partition synthetic DNSP emission.|rf-qa.md, rf-analyst.md, rf-qa-qualitative.md|MIG-005|order:6th; dependency:MIG-005 PASS; rollback:revert DNSP edit sites; all_agents_fail_guard:preserved; emission:after ladder exhaust only|M|P0|
|5|TEST-015|Monotonicity Halt Fixture|Verify non-shrinking failure sets halt before a third wasted cycle.|Tests|FR-CONV.5|input:\|F\|=5,5,5; halt:cycle 2; message:[HALT-MONOTONICITY]\|F\|=5; cycle3:not attempted|S|P0|
|6|TEST-016|Regression Halt Fixture|Verify PASS-to-FAIL flips halt before monotonicity check.|Tests|FR-CONV.5|input:Item 3.2 PASS@1 FAIL@2; message:verbatim regression text; order:before monotonicity; loop:exits|S|P0|
|7|TEST-017|Slow Shrink Fixture|Verify legitimate strict shrink continues.|Tests|FR-CONV.5|input:\|F\|=5,4; result:continues; slow-convergence threshold:absent; X-003:rejected|S|P0|
|8|TEST-018|DNSP Twice-Exhaust Fixture|Verify a twice-exhausted partition emits required synthetic-dnsp fields.|Tests|FR-CONV.6|trigger:partition timeout twice; fields:severity HIGH,source synthetic-dnsp,affected_range,evidence,recommendation; plus:dedup_key,found_n_times|S|P0|
|9|TEST-019|DNSP Dedup Fixture|Verify identical DNSP dedup keys collapse within one cycle.|Tests|FR-CONV.6|two identical dedup_key records; output:one record; found_n_times:2; real findings:preserved|S|P0|
|10|TEST-020|All-Agents-Fail Bypass Fixture|Verify zero partition successes route to existing rf-team-lead halt without DNSP.|Tests|FR-CONV.6|zero_success:true; synthetic-dnsp:absent; rf-team-lead.md:417 path:active; HALT asks user|S|P0|
|11|TEST-021|DNSP Cohort Concurrency Fixture|Verify one partition exhaust does not serialize sibling partitions.|Tests|FR-CONV.6,NFR-CONV.10|N partitions:timestamp overlap; exhausted partition:synthesises DNSP; N-1 siblings:continue to completion; serialisation:FAIL|M|P0|
|12|TEST-022|Synthetic Dedup Not Regression Fixture|Verify recurring identical DNSP finding is not treated as PASS-to-FAIL regression.|Tests|FR-CONV.5,FR-CONV.6|same dedup_key cycles 1+2; other findings shrink; regression:false; cycle3:attempted; monotonicity:uses dedup cardinality|M|P0|

### Integration Points — M4

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|F_n failure set|Retry-loop state model|Yes|M4|FR-CONV.5 halt guards|
|Regression halt message|String ABI|Yes|M4|fixtures and operator logs|
|[HALT-MONOTONICITY] message|String ABI|Yes|M4|fixtures and operator logs|
|synthetic-dnsp block|Agent finding block|Yes|M4|task-builder gate-result merge|
|rf-team-lead.md:417 path|Escalation guard|Preserved|M4|all-agents-fail branch|

### Milestone Dependencies — M4

- FR-CONV.5 lands before FR-CONV.6 so retry logic names the dedup-key shape before DNSP emits it.
- FR-CONV.6 depends on M1 API-003 and DM-003 for field identity and all-agents-fail precedence.

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Retry monotonicity halts legitimate slow-cycle correction.|Low|Low|Valid fix cycles stop early.|Only halt on non-shrink; any strict shrink continues; no slow-convergence threshold.|rf-task-builder maintainer|
|2|Synthetic DNSP findings mask real findings.|Low|Low|Operators miss root defect detail.|Emit HIGH findings alongside real findings; preserve real partition outputs.|rf-qa maintainer|
|3|DNSP all-agents-fail branch short-circuits existing escalation.|High|Low|Stop-the-line guard weakens.|Zero-success branch emits no DNSP and uses rf-team-lead.md:417.|Engineering Lead|

## M5: Validation, Rollout, and Operations

**Objective:** Complete post-merge audit, representative measurements, operational runbooks, logical flag cleanup, and release-readiness validation. | **Duration:** Weeks 11-14 | **Entry:** M4 exit complete; all six FRs landed in strict order. | **Exit:** 25 test fixtures pass, K-003 audit passes first 5 runs, token-cost ratio ≤1.10, make verify-sync passes, and v3.9 GA decision is ready.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|MIG-007|Post-Merge Audit and Token Measurement|Audit rf-qa-qualitative behavior and measure NFR-CONV.4 after all FRs land.|QA, task-builder|MIG-006|audit:first 5 rf-qa-qualitative runs; Self-Audit:100%; token_sample:5 BUILD_REQUESTs; token_ratio:≤1.10; duration:1-2 weeks; rollback:FR-CONV.3 or verdict summary|L|P0|
|2|TEST-023|Hidden Input Guard Fixture|Verify `.dev/tasks/done/` contents do not change structural output.|Tests|NFR-CONV.3|empty_done vs populated_done; structural output:byte-identical; PR-05 hidden-input behavior:absent|M|P0|
|3|TEST-024|Sequencing Fixture|Verify dynamic enumeration recovers if PR-04 is evaluated before PR-06 in a fixture.|Tests|FR-CONV.3|scenario:PR-04 before PR-06; catalogue activates; checklist richens; INV-010:PASS|S|P1|
|4|TEST-025|Invariant Preservation Composite|Verify NFR-CONV.6 through NFR-CONV.10 together.|Tests|NFR-CONV.6..10|self-contained:item PASS/FAIL; evidence-bound:PASS/FAIL; artifact-layout:unchanged; zero-trust:any gap FAIL; parallel-research:concurrent DNSP|L|P0|
|5|OPS-001|K-003 Audit Runbook|Operate the first-five-run anti-inflation audit after FR-CONV.3.|Operations|FR-CONV.3|symptoms:missing Self-Audit or zero semantic checks; diagnosis:read reviews report and grep Self-Audit; resolution:fix spawn prompt or disable passthrough; escalation:QA Lead immediate|M|P0|
|6|OPS-002|DNSP Triage Runbook|Operate synthetic-dnsp findings in production task-builder runs.|Operations|FR-CONV.6|symptoms:synthetic-dnsp HIGH; diagnosis:read evidence spawn log and dedup_key; resolution:manual review per recommendation; escalation:rf-qa maintainer, Engineering if ≥3 distinct/week|M|P0|
|7|OPS-003|All-Partitions-Exhaust Runbook|Operate the zero-success branch with no synthetic emission.|Operations|FR-CONV.6|symptoms:rf-team-lead HALT; diagnosis:confirm zero successes and no DNSP; resolution:user resolves findings before rerun; escalation:rf-team-lead maintainer if misfire|S|P0|
|8|OPS-004|Monotonicity Rate Runbook|Operate high monotonicity halt rates.|Operations|FR-CONV.5|symptoms:[HALT-MONOTONICITY] >50% batches; diagnosis:sample 3 events and inspect BUILD_REQUESTs; resolution:improve upstream requests or calibrate TB-Add-2; escalation:rf-task-builder maintainer|S|P1|
|9|OPS-005|Regression Halt Rate Runbook|Operate high regression halt rates.|Operations|FR-CONV.5|symptoms:regression halt >20% batches; diagnosis:sample 3 events and inspect cycle deltas; resolution:tighten fix-cycle prompts; escalation:Engineering Lead|S|P1|
|10|OPS-006|Sync Failure Runbook|Operate make verify-sync failures after FR merges.|Operations|A-001|symptoms:verify-sync FAIL; diagnosis:run make sync-dev and inspect git status; resolution:resync and commit only on PASS; escalation:per-commit author|S|P0|
|11|OPS-007|Layout Change Runbook|Operate INV-018 `.dev/tasks/` layout changes.|Operations|OPEN-INV-018|symptoms:directory schema differs; diagnosis:inspect all FR path references; resolution:re-integration commit covering all 6 FRs; escalation:Engineering Lead|M|P0|
|12|FLAG-TB-ADD-1-8|TB-Add Logical Flag|Track TB-Add catalogue rollout and cleanup.|Release Management|FR-CONV.1|default:enabled at merge; cleanup:GA+30 days; TB-Add-2:advisory until Phase-2; owner:rf-qa maintainer|S|P1|
|13|FLAG-EXECUTION-CONTEXT|Execution Context Logical Flag|Track Execution Context rollout and cleanup.|Release Management|FR-CONV.2|default:enabled at merge; cleanup:GA+30 days; owner:task-builder maintainer; fallback:References-only|S|P1|
|14|FLAG-INHERITED-VERDICT|Inherited Verdict Logical Flag|Track verdict passthrough rollout and audit-based stabilization.|Release Management|FR-CONV.3|default:enabled at merge; cleanup:after K-003 audit pass; owner:QA Lead; rollback:disable passthrough|S|P0|
|15|FLAG-FIVE-AXES|Five Axes Logical Flag|Track axis overlay rollout and cleanup.|Release Management|FR-CONV.4|default:enabled at merge; cleanup:GA+30 days; owner:rf-qa-qualitative maintainer; tuning:axis distribution audit|S|P1|
|16|FLAG-RETRY-GUARDS|Retry Guards Logical Flag|Track monotonicity and regression guard rollout.|Release Management|FR-CONV.5|default:enabled at merge; cleanup:GA+30 days; owner:rf-task-builder maintainer; rollback:disable guards individually|S|P0|
|17|FLAG-DNSP-EMISSION|DNSP Emission Logical Flag|Track synthetic DNSP rollout and cleanup.|Release Management|FR-CONV.6|default:enabled at merge; cleanup:GA+30 days; owner:rf-analyst/rf-qa maintainers; rollback:revert DNSP sites|S|P0|
|18|MET-001|Single-Pass PASS Rate Measurement|Measure representative first-cycle task-integrity PASS rate.|QA metrics|NFR-CONV-R1|sample:5 BUILD_REQUESTs; metric:first-cycle PASS fraction; target:≥80%; validation:gate reports|S|P1|
|19|MET-002|Detection Rate Measurement|Measure unresolved-token and DAG-cycle detection on synthetic fixtures.|QA metrics|TEST-001,TEST-002|unresolved_token_detection:100%; DAG_cycle_detection:100%; method:synthetic fixtures; validation:TB-Add-1/4 errors|S|P0|
|20|MET-003|Self-Audit Coverage Measurement|Measure Self-Audit presence and semantic-check coverage after FR-CONV.3.|QA metrics|OPS-001|window:first 5 runs; target:100%; semantic_checks:≥1 each; failure:block release|S|P0|
|21|MET-004|Halt Rate Measurement|Measure monotonicity and regression halt rates across fix-cycle batches.|QA metrics|OPS-004,OPS-005|monotonicity_alert:>50%; regression_alert:>20%; sample:post-merge batches; validation:grep logs|S|P1|
|22|MET-005|DNSP Emission Measurement|Measure DNSP emission on healthy and twice-exhaust fixtures.|QA metrics|FR-CONV.6|twice_exhaust:≥1; healthy_run:0; production_threshold:>0 triggers review; fields:all present|S|P0|
|23|MET-006|Token-Cost Measurement|Measure post/pre token cost ratio for equivalent BUILD_REQUESTs.|QA metrics|NFR-CONV.4|sample:5 BUILD_REQUESTs; tiers:Quick/Standard/Deep; target:≤1.10; contingency:summarise inherited verdict table|M|P0|

### Integration Points — M5

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|K-003 audit results|Manual QA evidence|Yes|M5|Release checklist|
|Token measurement report|Offline metric|Yes|M5|NFR-CONV.4 gate|
|Runbooks OPS-001..OPS-007|Operational procedures|Yes|M5|task-builder maintainers|
|Logical rollout flags|Release controls|Yes|M5|rollback and cleanup decisions|
|Fixture suite TEST-001..025|Validation suite|Yes|M5|CI and release criteria|

### Milestone Dependencies — M5

- M4 must complete because DNSP, retry halt, and synthetic-dedup fixtures are part of the release gate.
- The first-five-run audit starts after FR-CONV.3 lands but blocks M5 exit, not M3 exit.

### Open Questions — M5

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OPEN-PR05|When does `.dev/tasks/done/` reach ≥10 tasks across ≥3 task_types to re-evaluate PR-05? Source: TDD §22.|Determines Phase-2 timing; does not block v3.9 GA.|Engineering Lead|Each major release|
|2|OPEN-INV-017|Historical-file staleness check for PR-05 advisory citations. Source: TDD §22.|Deferred until PR-05 returns; no v3.9 deliverable impact.|Engineering|When PR-05 re-evaluated|
|3|OPEN-TOKEN|NFR-CONV.4 token-ceiling empirical measurement. Source: TDD §22.|Blocks v3.9 GA if token-cost ratio exceeds ≤1.10 without contingency.|Engineering Lead|Post-merge M5|

### Risk Assessment and Mitigation — M5

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Token ceiling exceeded by more than 10%.|Low|Low|Release cannot meet NFR-CONV.4.|Measure 5 representative BUILD_REQUESTs; summarise inherited verdict table if needed.|Engineering Lead|
|2|Post-merge audit finds semantic inflation.|Medium|Low|FR-CONV.3 cannot be declared stable.|Audit first 5 runs; disable passthrough if any VERIFIED item lacks semantic engagement.|QA Lead|
|3|Operational thresholds are measured but not acted on.|Medium|Low|Production readiness becomes observational only.|Bind each threshold to OPS runbooks and release checklist gates.|task-builder maintainer|

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By Milestone|Status|Fallback|
|---|---|---|---|
|None|M1-M5|NFR-CONV.5 forbids new external dependencies, network calls, MCP servers, and libraries.|Use existing Read/Grep/Glob/Bash-only local checks.|

### Infrastructure Requirements

- No database, service, queue, container, or network infrastructure is required.
- Existing repository tooling is required: `make sync-dev`, `make verify-sync`, and `uv run pytest`.
- Persistent artifacts remain under `.dev/tasks/to-do/TASK-*/` with existing `research/`, `qa/`, `synthesis/`, `reviews/`, and `adversarial/` directory names unchanged.

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|R-M1-1|Q-DM-1 schema ambiguity leads to implementing checks against wrong item fields.|M1,M2|Medium|High|Resolve Q-DM-1 before TB-Add work; record selected schema in DM-004.|Engineering Lead|
|R-M1-2|A-001 sync-discipline is bypassed during contract edits.|M1-M5|Low|Medium|Edit src/superclaude first; run make sync-dev and make verify-sync per FR.|Per-commit author|
|R-M1-3|`.dev/tasks/` layout dependency changes after contracts are planned.|M1-M5|Low|High|Track OPEN-INV-018; re-integrate all FRs if layout changes.|Engineering Lead|
|R-M2-1|TB-Add false positives waste fix cycles.|M2|Low|Low|Keep TB-Add-2 advisory; make each TB-Add individually revertable.|rf-qa maintainer|
|R-M2-2|Execution Context header drifts from item Context fields.|M2|Low|Low|TB-Add-7 cross-validates header source areas against items.|task-builder maintainer|
|R-M2-3|Per-item evidence gets moved from items into the header.|M2|Low|Medium|FR-CONV.2 keeps file:line citations in item Context only.|Engineering|
|R-M3-1|Inherited verdict passthrough causes rf-qa-qualitative inflation.|M3,M5|Low|Medium|Require Self-Audit and audit first 5 runs.|QA Lead|
|R-M3-2|Axis annotation ambiguity over-flags items.|M3|Low|Low|Keep axes annotation-only and tune after distribution audit.|rf-qa-qualitative maintainer|
|R-M3-3|FR-CONV.3 lands before FR-CONV.1 catalogue is active.|M3|Low|Medium|Enforce serial order through release checklist.|Engineering Lead|
|R-M4-1|Retry monotonicity halts legitimate slow-cycle correction.|M4|Low|Low|Only halt on non-shrink; any strict shrink continues.|rf-task-builder maintainer|
|R-M4-2|Synthetic DNSP findings mask real findings.|M4|Low|Low|Emit HIGH findings alongside real findings.|rf-qa maintainer|
|R-M4-3|DNSP all-agents-fail branch short-circuits existing escalation.|M4|Low|High|Zero-success branch emits no DNSP and uses rf-team-lead.md:417.|Engineering Lead|
|R-M5-1|Token ceiling exceeded by more than 10%.|M5|Low|Low|Measure 5 representative BUILD_REQUESTs; summarise inherited verdict table if needed.|Engineering Lead|
|R-M5-2|Post-merge audit finds semantic inflation.|M5|Low|Medium|Audit first 5 runs; disable passthrough on failure.|QA Lead|
|R-M5-3|Operational thresholds are measured but not acted on.|M5|Low|Medium|Bind thresholds to OPS runbooks and release checklist gates.|task-builder maintainer|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|Milestone|
|---|---|---|---|---|
|Single-pass gate health|First-cycle task-integrity PASS rate|≥80% of representative BUILD_REQUESTs|Run 5 BUILD_REQUESTs and count first-cycle PASS verdicts|M5|
|Unresolved-token detection|TB-Add-1 detection rate|100% on synthetic fixtures|Run TEST-001 and inspect item-ID-naming error|M2|
|DAG-cycle detection|TB-Add-4 detection rate|100% on synthetic fixtures|Run TEST-002 and inspect cycle error|M2|
|Self-Audit coverage|rf-qa-qualitative Self-Audit presence|100% on first 5 runs after FR-CONV.3|Manual audit plus grep for Self-Audit and semantic checks|M5|
|Monotonicity halt control|[HALT-MONOTONICITY] emission rate|<10%; >50% alerts upstream BUILD_REQUEST defect|Grep fix-loop logs over post-merge batches|M5|
|Synthetic DNSP behavior|DNSP emission count|≥1 on twice-exhaust fixture; 0 on healthy run|Run TEST-018 and healthy control|M4|
|Generation-cost efficiency|Token-cost ratio post/pre|≤1.10|Measure 5 representative BUILD_REQUESTs|M5|
|Gate convergence health|Fix-cycle convergence rate|≥75% baseline, expected ↑ post-merge|Compare PASS versus halt/cap outcomes over batches|M5|
|Structural determinism|Structural field diff|Byte-identical across two identical runs|Run NFR-CONV.1 deterministic diff|M5|
|Hidden-input determinism|Structural output with populated done/|Byte-identical to empty done/ baseline|Run TEST-023|M5|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|---|---|---|---|
|Porting strategy|Intent-port sc-tasklist mechanisms into task-builder idioms|Bulk implementation port; do nothing|Task-builder has single-MDTM topology, so intent preserves value without importing bundle-specific checks.|
|Governance|Strictly additive A-002|Rename or replace existing checks; single mega-merge|Additive changes keep rollback small and protect zero-trust QA invariants.|
|Verdict handoff|Inherited verdict as reliance context with Self-Audit|Pure passthrough; full re-check of every structural item|Balances token cost with anti-inflation assurance.|
|Axes design|Annotation overlay over existing 15-item checklist|Replace checklist; multiply checklist count by five|Overlay preserves proven checklist while making adversarial lenses explicit.|
|Retry termination|Regression precedence, then monotonicity non-shrink halt|Pure cardinality; slow-shrink threshold|Set identity catches regressions; strict shrink avoids false halts.|
|DNSP behavior|Emit only on mixed partition outcomes|Emit on all exhaust cases; emit never|Mixed-outcome DNSP closes silent partial failure while preserving all-agents-fail halt.|
|Hidden inputs|Reject PR-05 from Phase-1|Use `.dev/tasks/done/` advisory now|NFR-CONV.3 requires identical structural output regardless of historical task files.|

## Timeline Estimates

|Milestone|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1|2 weeks|Week 1, no earlier than 2026-05-21 design approval and Q-DM-1 ownership|Week 2|TDD Design Complete anchor 2026-05-21; Q-DM-1 resolved; DM/API/COMP/NFR contracts frozen|
|M2|3 weeks|Week 3|Week 5|Maps TDD Phase 1; FR-CONV.1 then FR-CONV.2; TEST-001..006 pass|
|M3|3 weeks|Week 6|Week 8|Maps TDD Phase 2; FR-CONV.3 then FR-CONV.4; TEST-007..014 pass|
|M4|2 weeks|Week 9|Week 10|Maps TDD Phase 3; FR-CONV.5 then FR-CONV.6; TEST-015..022 pass|
|M5|4 weeks|Week 11|Week 14, within 2026-Q3 GA target|Maps TDD Phase 4; TEST-023..025; K-003 audit; token measurement; runbooks; GA decision|

**Total estimated duration:** 14 weeks after Q-DM-1 resolution and design approval, with the default schedule constrained to the TDD's 2026-Q3 GA target.
