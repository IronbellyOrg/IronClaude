---
spec_source: "spec-roadmap-validate.compressed.md"
complexity_score: 0.65
complexity_class: MEDIUM
primary_persona: architect
adversarial: false
base_variant: "none"
variant_scores: "none"
convergence_score: none
---

# roadmap validate Subcommand — Project Roadmap

## Executive Summary

This roadmap delivers `superclaude roadmap validate`, an additive validation sub-pipeline that runs a Claude subprocess against completed roadmap pipeline artifacts (`roadmap.md`, `test-strategy.md`, `extraction.md`) to surface schema, structural, traceability, cross-file, and parseability defects before they reach `sc:tasklist`. It ships in two modes that share one code path: single-agent reflection (default `opus:architect`) and multi-agent adversarial reflection with a cross-checking merge step. The feature auto-invokes after a successful `roadmap run` unless `--no-validate` is passed, and runs standalone against any output directory.

**Business Impact:** Catches roadmap defects (duplicate deliverable IDs, broken milestone DAGs, missing bidirectional traceability) at the cheapest possible point — before downstream tasklist decomposition and sprint execution amplify them. The adversarial mode reduces false positives via BOTH_AGREE cross-checking, protecting the non-blocking UX contract that keeps validation advisory rather than obstructive.

**Complexity:** MEDIUM (0.65) — Above LOW due to multi-dimensional semantic validation (DAG acyclicity, bidirectional traceability, cross-file matching) plus parallel-reflect/sequential-merge subprocess orchestration. Below HIGH because the design is strictly additive: zero new pipeline infrastructure (reuses `execute_pipeline`, `ClaudeProcess`, `gate_passed`), no schema migration, no breaking changes, and a bounded blast radius of 3 new + 3 modified modules.

**Critical path:** `models.py` (DM-001 ValidateConfig) → (`validate_gates.py` ∥ `validate_prompts.py`) → `validate_executor.py` (step dispatch) → (`commands.py` ∥ `executor.py` auto-invoke wiring) → test + performance hardening. This ordering is mandated by the spec (§4.6) and is load-bearing: the executor cannot dispatch steps before gates and prompts exist, and the CLI cannot wire auto-invocation before the executor entry point is stable.

**Key architectural decisions:**

- One-directional dependency rule (hard architectural invariant): `validate_*` may import from `pipeline/*` and `roadmap/gates.py`, but `pipeline/*` MUST NOT import from `validate_*` — enforced by a static import-scan test to preserve NFR-007/NFR-050.2.
- Single code path for both modes: `_build_validate_steps` returns a list of 1 (single-agent) or list of N (multi-agent), eliminating mode-divergent branching and satisfying NFR-050.5.
- Subprocess isolation by design: validation runs as an out-of-session Claude subprocess specifically to eliminate confirmation bias — context independence is the feature, not an implementation detail.
- Non-blocking exit contract: blocking findings warn (enumerate B-IDs, set `tasklist_ready: false`) but never exit non-zero — validation is advisory.

**Open risks requiring resolution before M1:**

- Agent ID → filename derivation (OQ-001): the step-output filename contract (`reflect-{agent.id}.md` vs `reflect-opus-architect.md`) determines the executor's output-path construction and must be settled before the executor milestone; collision disambiguation for duplicate `opus:architect` specs is unspecified.

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|----|-------|------|----------|--------|--------------|--------------|------|
|M1|Foundation: Config & Type Contracts|Foundation|P0|M|—|10|Medium|
|M2|Validation Gates & Reflection Prompts|Core|P0|L|M1|12|Medium|
|M3|Validate Executor & Step Dispatch|Core|P0|L|M2|6|High|
|M4|CLI Integration & Auto-Invocation|Integration|P0|M|M3|8|Medium|
|M5|Testing, Performance & Hardening|Quality|P1|M|M4|12|Medium|

## Dependency Graph

```
M1 (Foundation: Config & Type Contracts)
  └─> M2 (Validation Gates & Reflection Prompts)
        └─> M3 (Validate Executor & Step Dispatch)
              └─> M4 (CLI Integration & Auto-Invocation)
                    └─> M5 (Testing, Performance & Hardening)
```

Linear critical path mandated by spec §4.6 implementation order. Internal parallelism within milestones: M2 builds `validate_gates.py` ∥ `validate_prompts.py`; M4 wires `commands.py` ∥ `executor.py`. No milestone-level fan-out — each milestone gates the next because the validate sub-pipeline is a strict layered dependency (types → gates/prompts → executor → CLI → tests).

## M1: Foundation — Config & Type Contracts

**Objective:** Establish `ValidateConfig` and the type/schema contracts every later module binds to, and lock the one-directional dependency invariant. | **Duration:** 1 week (Week 1) | **Entry:** Spec accepted; OQ-001 filename derivation triaged | **Exit:** `ValidateConfig` instantiable and extends `PipelineConfig`; all type contracts (DM-002..DM-007) documented; import-scan test green; reused infra (COMP-005, COMP-007) confirmed importable from `validate_*`.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|DM-001|ValidateConfig dataclass|Configuration DTO for the validate sub-pipeline; extends PipelineConfig via dataclass inheritance (§4.4 mandate)|models.py|—|extends PipelineConfig; output_dir:Path; validate_dir:Path(=output_dir/"validate"); agents:list[AgentSpec]; roadmap_file:Path(=output_dir/"roadmap.md"); test_strategy_file:Path(=output_dir/"test-strategy.md"); extraction_file:Path(=output_dir/"extraction.md"); inherits-all-PipelineConfig-fields|M|P0|
|2|DM-002|ValidationReport frontmatter contract|YAML frontmatter schema for validation-report.md|models.py|DM-001|blocking_issues_count:int; warnings_count:int; info_count:int; tasklist_ready:bool(true\|false); validation_agents:str(comma-sep-agent-ids); validation_mode:str(single\|adversarial)|S|P0|
|3|DM-004|SemanticCheck instantiation contract|Existing type reused to declare gate semantic checks|pipeline/models|—|name:str; check_fn:Callable[[str],bool]; failure_message:str; importable-without-validate-side-deps|S|P0|
|4|DM-005|Step instantiation contract|Existing type reused to declare validate steps|pipeline/models|—|id:str; prompt:str; output_file:Path; gate:GateCriteria; timeout_seconds:int(=300); inputs:list[Path]; retry_limit:int(=1); model:str(optional)|S|P0|
|5|DM-006|AgentSpec parse contract|Existing type; model:persona format identical to roadmap run (§7.2)|models.py|—|id:str; model:str; persona:str(from model:persona token); id-derives-{model}-{persona}|S|P0|
|6|DM-007|Agreement Analysis row contract|Table-row schema for the adversarial merge agreement table|validate_prompts (defn)|DM-002|columns:Finding; Agent A; Agent B; Resolution∈{BOTH_AGREE\|ONLY_A\|ONLY_B\|CONFLICT}|S|P0|
|7|COMP-005|pipeline/executor.py reuse confirmation|Confirm execute_pipeline is importable and stable as the generic step engine (reused, no edits)|pipeline/executor.py|—|execute_pipeline-importable-from-validate_executor; signature-accepts-list[Step\|list[Step]]; no-modification-required|S|P0|
|8|COMP-007|ClaudeProcess reuse confirmation|Confirm subprocess launcher is reusable for reflect/merge steps (reused, no edits)|ClaudeProcess|—|launches-claude-subprocess-per-step; honors-timeout_seconds; honors-retry_limit; no-new-infra(NFR-050.4)|S|P0|
|9|NFR-050.2|One-directional import invariant|Static import-scan test asserting no validate_* import in any pipeline/* module|tests/architecture|DM-001|zero-forbidden-imports; scan-covers-all-pipeline/*-modules; fails-CI-on-violation; preserves-NFR-007|M|P0|
|10|NFR-050.4|Infrastructure reuse audit|Verify validate sub-pipeline introduces zero new pipeline infra|validate_executor (audit)|COMP-005,COMP-007|reuses-execute_pipeline; reuses-ClaudeProcess; reuses-gate_passed/GateCriteria/SemanticCheck; new-infra-count=0|S|P0|

### Integration Points — M1

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|ValidateConfig→PipelineConfig|Dataclass inheritance|Yes|M1|validate_executor (M3), commands/executor (M4)|
|execute_pipeline|Reused step engine import|Yes|M1|validate_executor._build/execute (M3)|
|ClaudeProcess|Reused subprocess launcher|Yes|M1|Step execution at runtime (M3)|
|Import-scan architecture test|CI dependency-rule guard|Yes|M1|CI gate (all milestones)|

### Milestone Dependencies — M1

- None (foundation milestone).

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-001|Does `agent.id` resolve to `{model}-{persona}` (e.g. `opus-architect`), and how are duplicate `opus:architect` specs disambiguated for filenames?|Determines DM-006 id derivation and M3 output-path construction (`reflect-{agent.id}.md`)|architect|End of M1|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Circular dependency regression (validate_*→pipeline/*)|High|Medium|Breaks NFR-007/NFR-050.2 architecture invariant|One-directional import rule codified as NFR-050.2 import-scan CI test from M1; reuse-via-`.gates`-import pattern|architect|
|2|ValidateConfig inheritance drift from PipelineConfig|Low|Low|Field divergence breaks reuse of execute_pipeline|Mandated dataclass inheritance (§4.5); construct in integration test against real PipelineConfig|backend|

## M2: Validation Gates & Reflection Prompts

**Objective:** Build `validate_gates.py` and `validate_prompts.py` — the gate criteria and the reflection/merge prompt builders that encode all 7 validation dimensions and the report schema. | **Duration:** 1 week (Week 2) | **Entry:** M1 exit met; type contracts stable | **Exit:** REFLECT_GATE and ADVERSARIAL_MERGE_GATE constructed and unit-asserted; reflect prompt enumerates all 7 dimensions; merge prompt enumerates BOTH_AGREE/ONLY_A/ONLY_B categories; `_frontmatter_values_non_empty` imported from `.gates` (not duplicated).

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-002|validate_gates.py module|Defines gate criteria + semantic check functions for validate steps|validate_gates.py|DM-003,DM-004|defines REFLECT_GATE,ADVERSARIAL_MERGE_GATE; defines _has_agreement_table(content:str)->bool; imports _frontmatter_values_non_empty from .gates (no duplication, W-001); imports GateCriteria/SemanticCheck from pipeline/models|L|P0|
|2|COMP-003|validate_prompts.py module|Builds reflection and adversarial-merge prompts|validate_prompts.py|DM-006,DM-007|build_reflect_prompt(agent,roadmap_file,test_strategy_file,extraction_file)->str; build_adversarial_merge_prompt(reflect_files:list[Path],roadmap_file:Path)->str; depends-only-on-models.AgentSpec|L|P0|
|3|DM-003|GateCriteria instances|REFLECT_GATE + ADVERSARIAL_MERGE_GATE configuration DTOs|validate_gates.py|DM-004,OQ-002|REFLECT_GATE{required_frontmatter_fields=[blocking_issues_count,warnings_count,tasklist_ready]; min_lines=20; enforcement_tier="STANDARD"; semantic_checks=[frontmatter_values_non_empty]}; ADVERSARIAL_MERGE_GATE{required_frontmatter_fields=[blocking_issues_count,warnings_count,tasklist_ready,validation_mode,validation_agents]; min_lines=30; enforcement_tier="STRICT"; semantic_checks=[frontmatter_values_non_empty,has_agreement_table]}|M|P0|
|4|FR-050.5|7-dimension reflection prompt coverage|Reflect prompt covers all 7 validation dimensions, each finding severity-classified|validate_prompts.py|COMP-003|prompt-enumerates-7-dimensions; each-dimension-maps-to-severity; precision-constraint-"be thorough but precise"-present|M|P0|
|5|FR-050.5a|Schema dimension|YAML frontmatter fields present, non-empty, correctly typed|validate_prompts.py|FR-050.5|severity=BLOCKING; checks-presence+non-empty+type-of-frontmatter-fields|S|P0|
|6|FR-050.5b|Structure dimension|Milestone DAG acyclic, refs resolve, no duplicate deliverable IDs, heading hierarchy valid|validate_prompts.py|FR-050.5|severity=BLOCKING; checks-DAG-acyclicity+ref-resolution+duplicate-ID-detection+heading-hierarchy|S|P0|
|7|FR-050.5c|Traceability dimension|Bidirectional deliverable↔requirement mapping|validate_prompts.py|FR-050.5|severity=BLOCKING; every-deliverable→requirement; every-requirement→deliverable|S|P0|
|8|FR-050.5d|Cross-file dimension|test-strategy milestone refs match roadmap milestones|validate_prompts.py|FR-050.5|severity=BLOCKING; test-strategy-milestone-refs⊆roadmap-milestones|S|P0|
|9|FR-050.5e|Interleave dimension|interleave_ratio in [0.1,1.0]; test activities not back-loaded|validate_prompts.py|FR-050.5,OQ-003|severity=WARNING; interleave_ratio∈[0.1,1.0]; test-not-back-loaded; Dimension-string-emitted-for-WARNING|S|P0|
|10|FR-050.5f|Decomposition dimension|No compound deliverables needing split by sc:tasklist|validate_prompts.py|FR-050.5,OQ-003|severity=WARNING; flags-compound-deliverables; Dimension-string-emitted-for-WARNING|S|P0|
|11|FR-050.5g|Parseability dimension|Content parseable into items via headings/bullets/numbered lists|validate_prompts.py|FR-050.5|severity=BLOCKING; parse-simulation-over-headings+bullets+numbered-lists|S|P0|
|12|FR-050.6|Validation report schema embedding|Reflect prompt instructs the report frontmatter + body section contract|validate_prompts.py|DM-002|frontmatter:blocking_issues_count,warnings_count,info_count,tasklist_ready,validation_agents,validation_mode; body:#Validation Report,##Summary,##Blocking Issues(B-NNN:Dimension/Location/Detail/Fix),##Warnings(W-NNN),##Info(I-NNN),##Validation Metadata; Location=file:line\|file:section; Dimension∈{schema\|structure\|traceability\|cross-file\|parseability}|M|P0|

### Integration Points — M2

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|REFLECT_GATE.semantic_checks|Callback registry ([frontmatter_values_non_empty])|Yes|M2|gate_passed on reflect Step (M3)|
|ADVERSARIAL_MERGE_GATE.semantic_checks|Callback registry ([frontmatter_values_non_empty, has_agreement_table])|Yes|M2|gate_passed on merge Step (M3)|
|_frontmatter_values_non_empty|Imported check_fn from roadmap/gates.py|Yes|M2|Both gates' semantic_checks|
|_has_agreement_table|Local check_fn binding|Yes|M2|ADVERSARIAL_MERGE_GATE only|

### Milestone Dependencies — M2

- M1 (DM-001..DM-007 type contracts; reused gate primitives importable).

### Open Questions — M2

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-002|`info_count` is in DM-002 report schema but absent from both gates' `required_frontmatter_fields` — optional by design or omission?|Determines whether DM-003 gates must enforce info_count|backend|Mid-M2|
|2|OQ-003|`interleave` and `decomposition` (WARNING dims) are absent from FR-050.6's Dimension enumeration {schema\|structure\|traceability\|cross-file\|parseability} — what Dimension string do WARNING findings carry?|Determines FR-050.5e/5f Dimension emission and report parseability|architect|Mid-M2|

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Validation false positives from imprecise reflect prompt|High|Medium|Erodes user trust, wastes review time|Prompt precision constraint "be thorough but precise"; mandate every finding cite a specific Location; adversarial BOTH_AGREE cross-check (M3)|architect|
|2|Duplicated gate primitive instead of `.gates` import|Medium|Low|Drift between roadmap and validate frontmatter checks|Import `_frontmatter_values_non_empty` from `.gates` (W-001 resolution); assert identity in unit test|backend|
|3|WARNING-dimension Dimension-string ambiguity (OQ-003)|Low|Medium|Report consumers can't classify interleave/decomposition findings|Resolve OQ-003 before freezing report schema; default to dimension name string|architect|

## M3: Validate Executor & Step Dispatch

**Objective:** Build `validate_executor.py` — the single-code-path step builder that dispatches list-of-1 (single) or list-of-N (parallel reflect → sequential merge), and executes the validate sub-pipeline via reused `execute_pipeline`. | **Duration:** 2 weeks (Weeks 3-4) | **Entry:** M2 exit met; gates + prompts callable; OQ-001 resolved | **Exit:** `_build_validate_steps` returns correct layout for N=1 and N≥2; `execute_validate` runs reflect/merge steps with correct output paths; adversarial merge emits agreement table and recalculates blocking_issues_count/tasklist_ready; timeouts/retries honored.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-001|validate_executor.py module|Builds validate step layout and executes the validate sub-pipeline|validate_executor.py|COMP-002,COMP-003,COMP-005,DM-001|execute_validate(config:ValidateConfig); _build_validate_steps(config)->list[Step\|list[Step]]; calls-reused-execute_pipeline; writes-<output-dir>/validate/|L|P0|
|2|FR-050.2|Single-agent validation path|N==1 → single sequential reflect step|validate_executor.py|COMP-001,OQ-001|triggered-when-agents≤1; layout=[reflect](single subprocess); output=<output-dir>/validate/validation-report.md|M|P0|
|3|FR-050.3|Multi-agent adversarial path|N≥2 → parallel reflect group → sequential adversarial-merge|validate_executor.py|COMP-001,OQ-001,OQ-005|triggered-when-agents≥2; layout=[reflect-A,reflect-B](parallel)→adversarial-merge(sequential); per-agent-output=reflect-{agent.id}.md(e.g. reflect-opus-architect.md); final=validate/validation-report.md|M|P0|
|4|FR-050.7|Adversarial merge report|Merge step produces agreement analysis + recalculated counts|validate_executor.py|FR-050.3,DM-007|adds ## Agent Agreement Analysis table; resolutions BOTH_AGREE(high-conf)/ONLY_A(review)/ONLY_B(structural)/CONFLICT(escalate→higher/BLOCKING); recalculates-blocking_issues_count+tasklist_ready-from-merged-findings|M|P0|
|5|NFR-050.5|Shared single code path|Single-agent and multi-agent traverse identical code (list-of-1 vs list-of-N)|validate_executor.py|COMP-001|no-mode-specific-branch-outside-list-length; _build_validate_steps-returns-list; verified-by-test_build_validate_steps_single/multi|M|P0|
|6|NFR-IMP-3|Per-step timeout & retry|Each step timeout_seconds=300, retry_limit=1|validate_executor.py|DM-005|every-Step.timeout_seconds=300; every-Step.retry_limit=1; gate-failure-warns-not-exits(§8.3)|S|P1|

### Integration Points — M3

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|_build_validate_steps|Dispatch table (list-len → step layout)|Yes|M3|execute_validate (M3), commands/executor (M4)|
|Step.gate ← REFLECT_GATE|Gate→Step binding|Yes|M3|execute_pipeline gate_passed check|
|Step.gate ← ADVERSARIAL_MERGE_GATE|Gate→Step binding (merge only)|Yes|M3|execute_pipeline gate_passed check|
|reflect-{agent.id}.md|Output-path construction from AgentSpec.id|Yes|M3|adversarial-merge step inputs|
|execute_validate|Entry-point callback|Yes|M3|commands.validate (M4), executor auto-invoke (M4)|

### Milestone Dependencies — M3

- M2 (COMP-002 gates, COMP-003 prompts callable; DM-003 gate instances).

### Open Questions — M3

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-005|FR-050.7 agreement table is strictly A/B — what is the column layout and category set (ONLY_C?) for 3+ agents?|Determines _build_validate_steps + merge prompt for N≥3|architect|Start of M3|
|2|OQ-006|Is any N≥2 run `validation_mode: adversarial` regardless of N?|Determines DM-002 validation_mode value written by merge step|backend|Mid-M3|
|3|OQ-007|On gate failure, is a partial/zero-byte report still written, and does downstream sc:tasklist treat missing/incomplete report as tasklist_ready:false or "unknown"?|Determines §8.3 warn-and-continue artifact contract and downstream gating|architect|End of M3|

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Subprocess non-determinism / malformed frontmatter|Medium|Medium|Gate failure on otherwise-valid run (§8.3)|retry_limit=1; gate enforcement; explicit warn-and-continue on gate failure (resolve OQ-007 for artifact state)|backend|
|2|Adversarial merge over-blocking via CONFLICT escalation|Low|Medium|CONFLICT→higher/BLOCKING risks false BLOCKING|Evidence-evaluation step before escalation (§5.2); record escalation rationale in report|architect|
|3|N≥3 merge layout unspecified (OQ-005)|Medium|Medium|Multi-agent (>2) path undefined, runtime failure|Resolve OQ-005 before coding FR-050.3; constrain to documented N or extend category set|architect|
|4|Mode divergence violating NFR-050.5|Medium|Low|Two code paths drift, double maintenance|Single _build_validate_steps list contract; test_build_validate_steps_single/multi guard|backend|

## M4: CLI Integration & Auto-Invocation

**Objective:** Wire the `validate` subcommand into `commands.py` and the auto-invoke hook into `executor.py`, completing standalone + post-run validation with flag inheritance and the non-blocking exit contract. | **Duration:** 1 week (Week 5) | **Entry:** M3 exit met; execute_validate stable | **Exit:** `roadmap validate <dir>` runs standalone; `roadmap run` auto-invokes validation unless `--no-validate`; parent flags inherited; missing-file check errors clearly; blocking findings warn without non-zero exit.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-004|commands.py CLI dispatch|Adds validate subcommand + --no-validate flag on run|commands.py|COMP-001,COMP-006|registers-validate-subcommand; adds-run --no-validate; dispatches-to-execute_validate|M|P0|
|2|COMP-006|executor.py auto-invoke hook|execute_roadmap calls execute_validate after pipeline success|executor.py|COMP-001,COMP-005|execute_roadmap-calls-execute_validate-on-success; skips-when-pipeline-halts; inherits-agents/model/max-turns/debug|M|P0|
|3|FR-050.1|validate subcommand surface|Standalone subcommand validating an output-dir|commands.py|COMP-004|signature: superclaude roadmap validate <output-dir> [--agents model:persona,...] [--model MODEL] [--max-turns N] [--debug]; output_dir:click.Path(exists=True,path_type=Path); --agents default opus:architect; --model default ""; --max-turns int default 50; --debug is_flag; validates-presence-of roadmap.md+test-strategy.md+extraction.md|M|P0|
|4|FR-050.4|Auto-invocation from roadmap run|Post-pipeline auto-invoke unless --no-validate|executor.py|COMP-006|surface: superclaude roadmap run <spec-file> [--no-validate] [...]; validate-ON-by-default; inherits --agents/--model/--max-turns/--debug|M|P0|
|5|FR-050.4a|Run-only-after-success gate|Validation only runs after full pipeline success|executor.py|FR-050.4|if-pipeline-halts-on-failed-step→validation-skipped(no artifacts); if-resume-skipped-steps-but-gates-pass→validation-runs-on-final-artifacts(I-002)|S|P0|
|6|FR-050.4b|Parent-flag inheritance|Validate sub-pipeline inherits parent invocation flags|executor.py|FR-050.4|--agents,--model,--max-turns,--debug-passed-from-roadmap-run-into-ValidateConfig|S|P0|
|7|NFR-050.3|Standalone independence|validate works independently of roadmap run|commands.py|FR-050.1|validate-invocable-without-roadmap-run; standalone-path-fully-functional|S|P0|
|8|NFR-IMP-1|Non-blocking exit contract|Blocking findings warn but do not exit non-zero|commands.py|FR-050.1,FR-050.6|blocking-findings→warn(enumerate B-IDs §8.2)+tasklist_ready:false; never-exit-non-zero-on-blocking|S|P0|

### Integration Points — M4

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|validate subcommand|Click subcommand registration|Yes|M4|CLI users (standalone)|
|run --no-validate|Click flag registration|Yes|M4|execute_roadmap auto-invoke gate|
|execute_roadmap→execute_validate|Post-success callback hook|Yes|M4|Auto-validation after roadmap run|
|Parent→ValidateConfig flag inheritance|Config propagation|Yes|M4|execute_validate (agents/model/max-turns/debug)|

### Milestone Dependencies — M4

- M3 (execute_validate entry point + step dispatch stable).

### Open Questions — M4

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-004|When both `--model MODEL` (override all steps) and per-agent models in `--agents model:persona` are supplied, which wins?|Determines flag-resolution order in COMP-004/DM-001 config construction|architect|Mid-M4|

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Default agent-count mismatch between invocation modes|Medium|Medium|Standalone (single opus:architect) vs auto-invoke (inherited adversarial) produce different report shapes for same artifacts|Document in §7.2 (W-003); surface in CLI help; make inherited default explicit in executor hook|architect|
|2|Silent miss of real BLOCKING issues via warn-don't-fail|Medium|Medium|Users proceed past genuine BLOCKING findings|Prominent CLI warning lines enumerating B-IDs (§8.2); tasklist_ready:false flag; NFR-IMP-1 test|backend|
|3|Missing-file UX failure|Low|Low|Confusing error on dir lacking required inputs|FR-050.1 presence check + test_validate_missing_files clear-error exit|backend|
|4|--model vs --agents precedence ambiguity (OQ-004)|Low|Medium|Inconsistent model selection across steps|Resolve OQ-004 before wiring config construction; document precedence in CLI help|architect|

## M5: Testing, Performance & Hardening

**Objective:** Land the full test matrix (unit + integration + E2E), verify the ≤10% wall-time budget, and harden the false-positive and import-invariant guarantees. | **Duration:** 1 week (Week 6) | **Entry:** M4 exit met; feature functional end-to-end | **Exit:** All 10 named tests green; ≤2 min single-agent wall time confirmed; zero forbidden imports; false-positive precision validated against fixtures.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|TEST-001|test_build_validate_steps_single|Asserts single-agent layout is exactly 1 step|tests/roadmap|FR-050.2,NFR-050.5|agents=1→len(steps)==1; step.id=="reflect"; output=validation-report.md|S|P1|
|2|TEST-002|test_build_validate_steps_multi|Asserts multi-agent layout is parallel group + merge|tests/roadmap|FR-050.3,NFR-050.5|agents=2→[parallel reflect group]→adversarial-merge; per-agent reflect outputs present|S|P1|
|3|TEST-003|test_run_with_no_validate|Asserts --no-validate skips validation|tests/roadmap|FR-050.4|run --no-validate→execute_validate-not-called|S|P1|
|4|TEST-004|test_run_auto_validates|Asserts default run invokes validation after success|tests/roadmap|FR-050.4,FR-050.4a|run(no flag)+pipeline-success→execute_validate-called-once|S|P1|
|5|TEST-005|test_reflect_gate_criteria|Asserts REFLECT_GATE fields + non-empty check|tests/roadmap|DM-003|required_frontmatter_fields==[blocking_issues_count,warnings_count,tasklist_ready]; min_lines==20; tier=="STANDARD"; semantic_checks include frontmatter_values_non_empty|S|P1|
|6|TEST-006|test_merge_gate_has_agreement_table|Asserts ADVERSARIAL_MERGE_GATE extra fields + agreement-table check|tests/roadmap|DM-003,FR-050.7|required adds validation_mode+validation_agents; min_lines==30; tier=="STRICT"; semantic_checks include has_agreement_table|S|P1|
|7|TEST-007|test_reflect_prompt_contains_dimensions|Asserts reflect prompt enumerates all 7 dimensions|tests/roadmap|FR-050.5|prompt contains schema,structure,traceability,cross-file,interleave,decomposition,parseability|S|P1|
|8|TEST-008|test_merge_prompt_contains_categories|Asserts merge prompt enumerates resolution categories|tests/roadmap|FR-050.7|prompt contains BOTH_AGREE,ONLY_A,ONLY_B(,CONFLICT)|S|P1|
|9|TEST-009|test_validate_dry_run|Asserts plan printed without launching subprocesses|tests/roadmap|COMP-001|dry-run→step-plan-printed; zero-subprocess-launches|S|P1|
|10|TEST-010|test_validate_missing_files|Asserts clear error exit on missing required inputs|tests/roadmap|FR-050.1,NFR-IMP-1|dir-missing roadmap.md/test-strategy.md/extraction.md→clear-error-exit|S|P1|
|11|NFR-050.1|Wall-time budget validation|Validate adds ≤10% wall time (≤2 min single agent)|tests/perf|FR-050.2,NFR-IMP-3|single-agent-validate≤2min; ≤10%-of-pipeline-wall-time; per-step timeout_seconds=300 honored|M|P1|
|12|NFR-IMP-2|False-positive precision hardening|Low false-positive rate on the reflection prompt|tests/roadmap|FR-050.5|clean-roadmap-fixture→zero-BLOCKING; injected-duplicate-D-ID-fixture→exactly-one-B-xxx(E2E #3); precision-constraint-enforced|M|P1|

### Integration Points — M5

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Import-scan test (NFR-050.2)|CI gate re-run on full surface|Yes|M5 (created M1)|CI pipeline (regression guard)|
|E2E fixture harness (clean + injected-defect)|Test fixture wiring|Yes|M5|TEST-suite + NFR-IMP-2|

### Milestone Dependencies — M5

- M4 (feature functional end-to-end; CLI + auto-invoke wired).

### Risk Assessment and Mitigation — M5

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Wall-time budget breach on large roadmaps|Medium|Medium|Multi-agent parallel + merge exceeds ≤10%/≤2min (NFR-050.1)|per-step timeout_seconds=300; parallel reflect group; single-agent default for standalone; measure against large fixture|backend|
|2|False positives surviving to release|High|Low|Eroded trust on real artifacts|NFR-IMP-2 clean+injected fixtures; precision constraint; adversarial BOTH_AGREE cross-check verified in E2E|qa|
|3|Import-invariant regression late in cycle|Medium|Low|Circular dep slips past if test not re-run on full surface|Re-run NFR-050.2 scan over final module set in M5; keep as standing CI gate|architect|

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By Milestone|Status|Fallback|
|---|---|---|---|
|Click (CLI framework)|M4|Available (existing dep)|None needed; vendored in current toolchain|
|Model backends (opus, haiku; configurable via --model/--agents)|M3, M5|Available|Single-agent opus:architect default; degrade N≥2→N=1 if backend unavailable|
|Roadmap pipeline output artifacts (roadmap.md, test-strategy.md, extraction.md)|M3, M5 (runtime/E2E)|Produced by upstream roadmap run|FR-050.1 presence check errors clearly if absent|
|ClaudeProcess subprocess runtime (internal)|M3|Available (reused infra)|None; NFR-050.4 mandates reuse|
|pipeline/executor.py execute_pipeline (internal)|M3|Available (reused)|None|
|roadmap/gates.py primitives (_frontmatter_values_non_empty, GateCriteria, SemanticCheck, gate_passed)|M2|Available (reused)|None; import not duplication (W-001)|
|models.py base types (PipelineConfig, AgentSpec, Step)|M1|Available (extended)|None|

### Infrastructure Requirements

- No new pipeline infrastructure (NFR-050.4 hard mandate): reuse `execute_pipeline`, `ClaudeProcess`, `gate_passed`, `GateCriteria`, `SemanticCheck`.
- CI must host the static import-scan architecture test (NFR-050.2) as a standing gate across all `pipeline/*` modules.
- Test environment must provide model-backend access (or a deterministic subprocess simulation) for E2E reflect/merge runs; performance fixture for NFR-050.1 wall-time measurement.
- No `.roadmap-state.json` schema migration; validate state remains separate (state-separation constraint).

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|Mitigation|Owner|
|----|------|---------------------|-------------|--------|------------|-------|
|R-01|Validation false positives erode trust|M2, M5|Medium|High|Precision prompt constraint; mandatory Location citation; adversarial BOTH_AGREE cross-check; clean+injected fixtures (NFR-IMP-2)|architect|
|R-02|Circular dependency regression (validate_*→pipeline/*)|M1, M5|Medium|High|One-directional import rule; NFR-050.2 import-scan CI test from M1, re-run M5|architect|
|R-03|Subprocess non-determinism / malformed frontmatter|M3|Medium|Medium|retry_limit=1; gate enforcement; warn-and-continue on gate failure (resolve OQ-007)|backend|
|R-04|Wall-time budget breach (>10% / >2 min)|M3, M5|Medium|Medium|timeout_seconds=300; parallel reflect group; single-agent default; large-fixture measurement|backend|
|R-05|Default agent-count mismatch between invocation modes|M4|Medium|Medium|Document §7.2 (W-003); CLI help note; explicit inherited default in executor hook|architect|
|R-06|Silent miss of real BLOCKING issues (warn-don't-fail)|M4|Medium|Medium|Prominent CLI B-ID warnings (§8.2); tasklist_ready:false; NFR-IMP-1 test|backend|
|R-07|Adversarial merge over-blocking via CONFLICT escalation|M3|Medium|Low|Evidence-evaluation before escalation (§5.2); record escalation rationale|architect|
|R-08|Missing-file UX failure|M4|Low|Low|FR-050.1 presence check; test_validate_missing_files clear-error exit|backend|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|Milestone|
|---|---|---|---|---|
|validate runs to completion with all 3 files|Report written|<dir>/validate/validation-report.md exists|E2E #1|M4|
|Multi-agent produces per-agent + merged reports|Files + agreement table|reflect-opus-architect.md + reflect-haiku-architect.md + merged report with ## Agent Agreement Analysis|E2E #2; test_build_validate_steps_multi|M3|
|Step-count by mode|Layout shape|single=1 step; multi=parallel group+merge|test_build_validate_steps_single/multi|M3|
|Injected duplicate D-ID surfaces|BLOCKING finding|exactly one B-xxx in report|E2E #3 (FR-050.5b)|M5|
|--no-validate skips; default auto-validates|Invocation behavior|--no-validate→skip; default+success→validate|test_run_with_no_validate; test_run_auto_validates|M4|
|tasklist_ready truth condition|Flag value|true iff blocking_issues_count==0|Report assertion (§5.1, FR-050.6)|M3|
|Gate field enforcement|Gate criteria|REFLECT_GATE 3 fields+non-empty; MERGE adds validation_mode/agents+agreement table|test_reflect_gate_criteria; test_merge_gate_has_agreement_table|M2|
|Prompt dimension/category coverage|Prompt content|reflect=7 dimensions; merge=BOTH_AGREE/ONLY_A/ONLY_B|test_reflect_prompt_contains_dimensions; test_merge_prompt_contains_categories|M2|
|Wall-time budget|Elapsed|≤10% pipeline; ≤2 min single agent|Performance fixture (NFR-050.1)|M5|
|Import invariant|Static scan|zero validate_* imports in pipeline/*|Import-scan test (NFR-050.2)|M1/M5|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|----------|--------|------------------------|----------|
|Validation execution context|Out-of-session Claude subprocess|In-session reflection|Context independence eliminates confirmation bias (§3 design decision)|
|Single vs multi-agent dispatch|Shared code path: list-of-1 vs list-of-N|Separate single/multi functions|NFR-050.5 — one code path prevents drift, halves maintenance|
|Gate primitive sourcing|Import `_frontmatter_values_non_empty` from `.gates`|Duplicate the check locally|W-001 resolution — avoid drift between roadmap and validate frontmatter checks|
|Dependency direction|validate_*→pipeline/* only (one-directional)|Bidirectional convenience imports|NFR-007/NFR-050.2 — prevent circular dependency; enforced by import-scan test|
|Infrastructure|Reuse execute_pipeline/ClaudeProcess/gate_passed|New validate-specific engine|NFR-050.4 — zero new infra, additive scope, bounded blast radius|
|Exit on blocking findings|Warn + tasklist_ready:false, never exit non-zero|Non-zero exit on BLOCKING|NFR-IMP-1 — advisory UX contract; mitigate silent-miss via prominent B-ID warnings|
|CONFLICT resolution in merge|Escalate to higher/BLOCKING after evidence eval|Auto-escalate unconditionally|§5.2 — reduce over-blocking while preserving safety bias|
|Config typing|ValidateConfig extends PipelineConfig|Standalone config dataclass|§4.5 mandate — reuse execute_pipeline contract without adaptation|

## Timeline Estimates

|Milestone|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1|1 week|Week 1|Week 1|ValidateConfig + type contracts; import-scan test green; OQ-001 resolved|
|M2|1 week|Week 2|Week 2|validate_gates.py + validate_prompts.py; 7 dimensions; report schema; OQ-002/003 resolved|
|M3|2 weeks|Week 3|Week 4|validate_executor.py; single/multi dispatch; adversarial merge; OQ-005/006/007 resolved|
|M4|1 week|Week 5|Week 5|validate subcommand + --no-validate auto-invoke; flag inheritance; OQ-004 resolved|
|M5|1 week|Week 6|Week 6|Full test matrix green; ≤2 min wall time; zero forbidden imports; false-positive hardening|

**Total estimated duration:** 6 weeks (Week 1 → Week 6).
