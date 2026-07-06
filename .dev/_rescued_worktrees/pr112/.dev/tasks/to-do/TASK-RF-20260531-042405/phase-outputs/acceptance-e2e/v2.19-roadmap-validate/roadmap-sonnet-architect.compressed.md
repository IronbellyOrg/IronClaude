---
spec_source: "spec-roadmap-validate.compressed.md"
complexity_score: 0.65
complexity_class: MEDIUM
primary_persona: architect
adversarial: false
base_variant: "none"
variant_scores: "none"
convergence_score: null
---
# Roadmap Validate Subcommand — Project Roadmap

## Executive Summary

Implement `superclaude roadmap validate` as an additive validation sub-pipeline that runs independently or after successful `roadmap run`, reusing the existing roadmap pipeline executor, gate primitives, and Claude subprocess model. The roadmap prioritizes the one-directional dependency boundary, shared single/multi-agent execution path, precise report schema, and explicit validation dimensions so validation improves downstream tasklist readiness without changing roadmap state or failing CLI exits on findings.

**Business Impact:** Adds a predictable quality gate for generated roadmap artifacts, reducing tasklist rework by surfacing schema, structure, traceability, cross-file, interleave, decomposition, and parseability issues before implementation planning.

**Complexity:** MEDIUM (0.65) — bounded additive CLI scope with moderate branching, subprocess orchestration, adversarial merge behavior, and non-trivial semantic validation across three roadmap artifacts.

**Critical path:** Add `ValidateConfig` and shared validate step construction, define gates and prompts, wire CLI standalone invocation, wire post-run auto-validation, then prove behavior through unit, integration, E2E, performance, and architecture-import tests.

**Key architectural decisions:**

- Reuse `execute_pipeline`, `ClaudeProcess`, `GateCriteria`, `SemanticCheck`, `gate_passed`, and `_frontmatter_values_non_empty`; add no new pipeline infrastructure.
- Keep dependency direction validate → roadmap/pipeline only; forbid `pipeline/*` imports from `validate_*` modules.
- Build one code path where `_build_validate_steps()` returns either a single reflect step or a parallel reflect group followed by adversarial merge.

**Open risks requiring resolution before M1:**

- Confirm agent ID to filename derivation, `--model` versus `--agents` precedence, report warning dimension strings, and >2-agent merge layout before locking the public CLI/report contract.

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|---|---|---|---|---|---|---|---|
|M1|Validation contracts and architecture decisions|Architecture|P0|2w|-|14|High|
|M2|Validate pipeline construction, gates, and prompts|Backend|P0|2w|M1|18|High|
|M3|CLI standalone command and post-run invocation|CLI|P0|2w|M1,M2|12|Medium|
|M4|Report semantics, adversarial merge, and UX warnings|Validation|P1|2w|M2,M3|12|Medium|
|M5|Verification, performance, and release readiness|Testing/DevOps|P0|2w|M1,M2,M3,M4|14|Medium|

## Dependency Graph

M1 → M2 → M3 → M4 → M5
M1 → M3
M2 → M4
M3 → M5
M4 → M5

## M1: Validation Contracts and Architecture Decisions

**Objective:** Lock the public validate contract, data contracts, architectural boundaries, and unresolved decisions before implementation. | **Duration:** weeks 1-2 (2w) | **Entry:** extraction accepted; roadmap/test artifacts contract known | **Exit:** contracts reviewed; OQ-001..OQ-007 resolved or assigned; dependency boundary test design approved

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|DM-001|ValidateConfig model|Add validation configuration dataclass extending `PipelineConfig` with explicit artifact paths and agent list.|models.py|-|output_dir:Path; validate_dir:Path; agents:list[AgentSpec]; roadmap_file:Path; test_strategy_file:Path; extraction_file:Path; inherited:PipelineConfig|M|P0|
|2|DM-002|Validation report frontmatter|Define the report frontmatter contract consumed by gates and users.|validation-report.md|DM-001|blocking_issues_count:int; warnings_count:int; info_count:int; tasklist_ready:bool; validation_agents:str; validation_mode:single/adversarial|S|P0|
|3|DM-003|Validate gate DTOs|Define `REFLECT_GATE` and `ADVERSARIAL_MERGE_GATE` criteria using existing gate primitives.|validate_gates.py|DM-002|REFLECT_GATE.required_frontmatter_fields:[blocking_issues_count,warnings_count,tasklist_ready]; min_lines:20; enforcement_tier:STANDARD; semantic_checks:[frontmatter_values_non_empty]; ADVERSARIAL_MERGE_GATE.required_frontmatter_fields:[blocking_issues_count,warnings_count,tasklist_ready,validation_mode,validation_agents]; min_lines:30; enforcement_tier:STRICT; semantic_checks:[frontmatter_values_non_empty,has_agreement_table]|M|P0|
|4|DM-004|SemanticCheck usage|Instantiate existing semantic check type for validate-specific content checks.|validate_gates.py|DM-003|name:str; check_fn:Callable[[str],bool]; failure_message:str|S|P0|
|5|DM-005|Validate Step shape|Specify all `Step` fields used by reflect and merge steps.|validate_executor.py|DM-001,DM-003|id:str; prompt:str; output_file:Path; gate:GateCriteria; timeout_seconds:300; inputs:list[Path]; retry_limit:1; model:str|M|P0|
|6|DM-006|AgentSpec contract|Reuse existing agent spec parsing and persona identity for validate steps.|models.py|DM-001|id:str; model:str; persona:model:persona-format|S|P0|
|7|DM-007|Agreement analysis row|Define adversarial merge table contract before prompt and report work.|validation-report.md|DM-002|Finding:str; Agent A:str; Agent B:str; Resolution:BOTH_AGREE/ONLY_A/ONLY_B/CONFLICT|S|P1|
|8|NFR-050.2|Dependency boundary rule|Preserve NFR-007 by making validate modules depend on roadmap/pipeline only.|architecture|COMP-001|target:zero pipeline imports from validate_*; scope:pipeline/*; verification:static import scan|S|P0|
|9|NFR-050.4|Infrastructure reuse rule|Constrain implementation to existing executor, subprocess, and gate primitives.|architecture|COMP-005,COMP-007|execute_pipeline:reused; ClaudeProcess:reused; gate_passed:reused; GateCriteria:reused; SemanticCheck:reused; new_infra:zero|S|P0|
|10|NFR-050.5|Shared execution path rule|Ensure single-agent and multi-agent validation share the same step builder.|validate_executor.py|DM-005|single:list-of-1; multi:list-of-N-plus-merge; divergent_code_paths:zero|S|P0|
|11|COMP-008|Gate pass integration|Use existing `gate_passed` semantics for warn-and-continue validation outcomes.|validate_executor.py|NFR-050.4|gate_passed:called; failed_gate:warns; process_exit:zero; partial_report:flagged|M|P0|
|12|COMP-009|Agent filename resolver|Resolve agent IDs to stable reflect output filenames and collision behavior.|validate_executor.py|DM-006,OQ-001|pattern:reflect-{agent.id}.md; example:reflect-opus-architect.md; duplicate_policy:defined; path:validate_dir|S|P0|
|13|COMP-010|Model precedence resolver|Define precedence when `--model` and per-agent `--agents` are both present.|commands.py|OQ-004|inputs:--model; inputs:--agents; precedence:documented; applied_to:reflect+merge|S|P0|
|14|COMP-011|Validate artifact resolver|Centralize required input and output path derivation for validate invocations.|models.py|DM-001|required:roadmap.md,test-strategy.md,extraction.md; output:validate/validation-report.md; reflect_dir:validate; missing:clear_error|S|P0|

### Integration Points — M1

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|ValidateConfig → PipelineConfig|dataclass inheritance|Yes|M1|COMP-001,COMP-004,COMP-006|
|GateCriteria/SemanticCheck → validate gates|gate DTO wiring|Yes|M1|COMP-002,COMP-008|
|AgentSpec → reflect filename resolver|identity mapping|Yes|M1|COMP-001,COMP-009|
|ValidationReport frontmatter → gates|schema contract|Yes|M1|COMP-002,COMP-003,M4|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Circular dependency regression|High|Medium|Breaks NFR-007 and risks pipeline import cycles|Approve dependency rule in M1 and enforce with static import scan in M5|Architect|
|2|Unresolved CLI/report ambiguity|High|Medium|Public command or report shape changes after implementation|Resolve OQ-001..OQ-007 before M2 exit and record decisions in tests|Architect+CLI owner|

### Milestone Dependencies — M1

- None.

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-001|Does `agent.id` resolve to `{model}-{persona}`, and how are duplicate agent specs disambiguated?|Blocks reflect output path contract|Architect|Before M2 step builder|
|2|OQ-002|Is `info_count` intentionally omitted from gate required fields?|Blocks gate schema fidelity|Validation owner|Before M2 gate work|
|3|OQ-003|Which Dimension strings are used for `interleave` and `decomposition` warnings?|Blocks report prompt and report schema|Validation owner|Before M4 report finalization|
|4|OQ-004|When both `--model` and per-agent `--agents` models are supplied, which wins?|Blocks CLI config semantics|CLI owner|Before M3 CLI wiring|
|5|OQ-005|How does adversarial merge format agreement analysis for more than two agents?|Blocks merge prompt and report table shape|Architect|Before M4 merge prompt|
|6|OQ-006|Is any 2+ agent invocation always `validation_mode: adversarial`?|Blocks frontmatter values|Validation owner|Before M4 report finalization|
|7|OQ-007|When a gate fails, is a partial report written and how should downstream tasklist treat it?|Blocks warn-and-continue UX|CLI owner|Before M4 UX warnings|

## M2: Validate Pipeline Construction, Gates, and Prompts

**Objective:** Build validate step planning, gate definitions, and reflection/merge prompts on existing pipeline infrastructure. | **Duration:** weeks 3-4 (2w) | **Entry:** M1 contracts and OQ owners confirmed | **Exit:** single and multi-agent step layouts produce gated subprocess steps with all seven dimensions covered

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-001|Validate executor module|Create `validate_executor.py` to build step layouts and execute the validate sub-pipeline.|validate_executor.py|DM-001,DM-005|path:src/superclaude/cli/roadmap/validate_executor.py; methods:execute_validate(config),_build_validate_steps(config); deps:COMP-005,COMP-002,COMP-003,DM-001|L|P0|
|2|COMP-002|Validate gates module|Create gate criteria and semantic checks for reflect and adversarial merge outputs.|validate_gates.py|DM-003,DM-004|path:src/superclaude/cli/roadmap/validate_gates.py; members:REFLECT_GATE,ADVERSARIAL_MERGE_GATE,_has_agreement_table(content); imports:_frontmatter_values_non_empty from .gates|M|P0|
|3|COMP-003|Validate prompts module|Create prompt builders for context-independent reflection and adversarial merge.|validate_prompts.py|DM-006,DM-007|path:src/superclaude/cli/roadmap/validate_prompts.py; methods:build_reflect_prompt(agent,roadmap_file,test_strategy_file,extraction_file),build_adversarial_merge_prompt(reflect_files,roadmap_file); deps:AgentSpec|M|P0|
|4|COMP-005|Pipeline executor reuse|Route validation through the existing generic step engine instead of adding a new runner.|pipeline/executor.py|NFR-050.4|execute_pipeline:called; step_groups:supported; validation_state:separate; new_runner:zero|M|P0|
|5|COMP-007|ClaudeProcess reuse|Launch reflect and merge work through existing subprocess isolation.|pipeline subprocess|NFR-050.4|subprocess:ClaudeProcess; isolation:context-independent; timeout:per-step; retry:per-step|M|P0|
|6|FR-050.2|Single-agent validation|Implement default single reflect step and validation report output.|validate_executor.py|COMP-001|trigger:--agents omitted or length=1; layout:reflect sequential; output:<output-dir>/validate/validation-report.md|M|P0|
|7|FR-050.3|Multi-agent adversarial validation|Implement parallel reflect group followed by sequential adversarial merge.|validate_executor.py|COMP-001,COMP-009|trigger:agents>=2; layout:[reflect-opus,reflect-haiku]→adversarial-merge; outputs:reflect-{agent.id}.md+validation-report.md|L|P0|
|8|FR-050.5|Validation dimensions umbrella|Ensure reflect prompt instructs all seven dimensions and severities.|validate_prompts.py|COMP-003|dimensions:schema,structure,traceability,cross-file,interleave,decomposition,parseability; severity:blocking/warning; findings:cited|M|P0|
|9|FR-050.5a|Schema validation dimension|Check YAML frontmatter for required fields, non-empty values, and type correctness.|validate_prompts.py|FR-050.5|dimension:schema; checks:fields-present,non-empty,typed; severity:BLOCKING|S|P0|
|10|FR-050.5b|Structure validation dimension|Check milestone DAG, references, duplicate deliverable IDs, and headings.|validate_prompts.py|FR-050.5|dimension:structure; checks:DAG-acyclic,refs-resolve,unique-deliverable-IDs,heading-hierarchy; severity:BLOCKING|S|P0|
|11|FR-050.5c|Traceability validation dimension|Check bidirectional requirement and deliverable coverage.|validate_prompts.py|FR-050.5|dimension:traceability; checks:deliverable→requirement,requirement→deliverable; severity:BLOCKING|S|P0|
|12|FR-050.5d|Cross-file validation dimension|Check test-strategy milestone references against roadmap milestones.|validate_prompts.py|FR-050.5|dimension:cross-file; checks:test-strategy-milestones-match-roadmap; severity:BLOCKING|S|P0|
|13|FR-050.5e|Interleave validation dimension|Check test activity distribution and interleave ratio.|validate_prompts.py|FR-050.5|dimension:interleave; interleave_ratio:[0.1,1.0]; test_activity:not-back-loaded; severity:WARNING|S|P1|
|14|FR-050.5f|Decomposition validation dimension|Check for compound deliverables that need tasklist splitting.|validate_prompts.py|FR-050.5|dimension:decomposition; compound_deliverables:flagged; split_by:sc:tasklist; severity:WARNING|S|P1|
|15|FR-050.5g|Parseability validation dimension|Check roadmap content can be parsed into items by common markdown structures.|validate_prompts.py|FR-050.5|dimension:parseability; parse_inputs:headings,bullets,numbered-lists; severity:BLOCKING|S|P0|
|16|NFR-IMP-3|Timeout and retry limits|Apply bounded subprocess execution to every validate step.|validate_executor.py|DM-005|timeout_seconds:300; retry_limit:1; applies_to:reflect+merge; failure:warn-and-continue|S|P0|
|17|COMP-012|Reflect step factory|Create a builder path that emits reflect steps from agent specs and artifacts.|validate_executor.py|COMP-001,COMP-003|inputs:AgentSpec,roadmap_file,test_strategy_file,extraction_file; gate:REFLECT_GATE; output_file:validation-report-or-reflect-agent; model:resolved|M|P0|
|18|COMP-013|Adversarial merge step factory|Create merge step when agent count is two or more.|validate_executor.py|COMP-001,COMP-003,DM-007|inputs:reflect_files,roadmap_file; gate:ADVERSARIAL_MERGE_GATE; output_file:validation-report.md; model:resolved|M|P0|

### Integration Points — M2

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|_build_validate_steps → execute_pipeline|step dispatch table|Yes|M2|COMP-001,COMP-005|
|REFLECT_GATE → reflect Step|gate binding|Yes|M2|COMP-012|
|ADVERSARIAL_MERGE_GATE → merge Step|gate binding|Yes|M2|COMP-013|
|build_reflect_prompt → reflect Step.prompt|callback wiring|Yes|M2|COMP-012|
|build_adversarial_merge_prompt → merge Step.prompt|callback wiring|Yes|M2|COMP-013|
|ClaudeProcess → validate steps|subprocess strategy|Yes|M2|COMP-005,COMP-007|

### Milestone Dependencies — M2

- Depends on M1 for data contracts, filename decision, gate-field decision, and model precedence decision.

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Subprocess non-determinism or malformed frontmatter|Medium|Medium|Gates fail and users receive low-confidence validation artifacts|Use strict prompt schema, `retry_limit=1`, frontmatter gates, and clear warnings|Validation owner|
|2|Validation false positives|High|Medium|Users spend time reviewing non-issues and lose trust in validation|Require cited findings, precise dimension labels, and adversarial agreement analysis|Prompt owner|

## M3: CLI Standalone Command and Post-Run Invocation

**Objective:** Expose validation through the CLI and automatically invoke it after successful roadmap runs while preserving standalone usability and non-blocking exit behavior. | **Duration:** weeks 5-6 (2w) | **Entry:** M2 step builder and gates pass unit checks | **Exit:** standalone validate, default auto-validation, `--no-validate`, resume success gating, and flag inheritance all work through Click

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-050.1|Validate subcommand|Add `superclaude roadmap validate` with required artifact preflight and validation pipeline launch.|commands.py|COMP-011|positional:output_dir click.Path(exists=True,path_type=Path); options:--agents default opus:architect,--model default "",--max-turns int default 50,--debug flag; required_files:roadmap.md,test-strategy.md,extraction.md|M|P0|
|2|COMP-004|Roadmap commands module|Modify CLI dispatch to add validate subcommand and `--no-validate` flag on run.|commands.py|FR-050.1|path:src/superclaude/cli/roadmap/commands.py; adds:validate command,--no-validate; deps:COMP-001,COMP-006|M|P0|
|3|COMP-014|Validate command binding|Bind Click parameters into `ValidateConfig` and call `execute_validate`.|commands.py|COMP-004,DM-001|args:output_dir; options:agents,model,max_turns,debug; builds:ValidateConfig; calls:execute_validate|M|P0|
|4|NFR-050.3|Standalone validation usability|Ensure validate works without `roadmap run` state or previous invocation context.|commands.py|FR-050.1|standalone:yes; state_required:no; input_dir:existing artifacts; output_dir:validate|S|P0|
|5|FR-050.4|Roadmap run auto-invocation|Invoke validation after the eight-step roadmap pipeline succeeds unless disabled.|executor.py|COMP-001,COMP-006|trigger:pipeline success; default:validate on; skip_flag:--no-validate; failure_before_success:skip validate|M|P0|
|6|FR-050.4a|Success-only validation gate|Run validation only after full pipeline success or successful resume with gates passing.|executor.py|FR-050.4|full_success:runs; resume_skipped_steps+all_gates_pass:runs; halted_failed_step:skips|S|P0|
|7|FR-050.4b|Parent flag inheritance|Pass parent roadmap run validation-related flags into validate sub-pipeline.|executor.py|FR-050.4|inherits:--agents,--model,--max-turns,--debug; source:roadmap run config; target:ValidateConfig|S|P0|
|8|COMP-006|Roadmap executor module|Modify `execute_roadmap` orchestration to call `execute_validate` after success.|executor.py|FR-050.4|path:src/superclaude/cli/roadmap/executor.py; role:orchestrates execute_roadmap; calls:execute_validate; deps:COMP-005,COMP-001|M|P0|
|9|COMP-015|No-validate flag binding|Add explicit opt-out path for validation during roadmap run.|commands.py|COMP-004,FR-050.4|flag:--no-validate; default:false; effect:skip validate; help:clear|S|P0|
|10|COMP-016|Resume validation dispatcher|Handle resume completion versus halt interaction for final artifacts.|executor.py|FR-050.4a|resume_success:runs validate; resume_halt:skips validate; state_schema:.roadmap-state.json unchanged|M|P0|
|11|NFR-IMP-1|Non-blocking validation UX|Return successful CLI exit even when validation finds blocking issues, with prominent warnings.|commands.py|COMP-008|blocking_findings:warn; exit_code:0; tasklist_ready:false; B-IDs:shown|M|P0|
|12|OPS-001|Missing-file preflight|Fail early with a clear CLI error when required artifacts are absent.|commands.py|FR-050.1|checks:roadmap.md,test-strategy.md,extraction.md; missing:error lists files; subprocess:not launched|S|P0|

### Integration Points — M3

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Click command group → validate handler|CLI dispatch|Yes|M3|COMP-014|
|roadmap run config → ValidateConfig|dependency injection|Yes|M3|COMP-006,COMP-014|
|execute_roadmap success gate → execute_validate|callback wiring|Yes|M3|FR-050.4,FR-050.4a|
|--no-validate → validation dispatcher|flag gate|Yes|M3|COMP-015|
|Required artifact preflight → subprocess launch|middleware chain|Yes|M3|OPS-001,COMP-001|

### Milestone Dependencies — M3

- Depends on M1 for CLI contract and model precedence; depends on M2 for `execute_validate` and step construction.

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Default agent-count mismatch between standalone and auto-invoke|Medium|Medium|Same artifacts can yield different report shapes by invocation path|Document defaults in help and add tests for both default modes|CLI owner|
|2|Missing-file UX confusion|Low|Medium|Users may see subprocess errors instead of actionable artifact errors|Run preflight before subprocess launch and list absent files|CLI owner|

## M4: Report Semantics, Adversarial Merge, and UX Warnings

**Objective:** Make validation reports precise, schema-conformant, merged across agents when needed, and actionable without breaking the non-blocking UX contract. | **Duration:** weeks 7-8 (2w) | **Entry:** M3 CLI paths invoke validation reliably | **Exit:** reports include required frontmatter/body, agreement analysis, recalculated counts, cited findings, and CLI warning summaries

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-050.6|Validation report schema|Generate `validation-report.md` with required frontmatter and body sections.|validation-report.md|DM-002,FR-050.5|frontmatter:blocking_issues_count,warnings_count,info_count,tasklist_ready,validation_agents,validation_mode; sections:# Validation Report,Summary,Blocking Issues,Warnings,Info,Validation Metadata; finding_ids:B-NNN,W-NNN,I-NNN; finding_fields:Dimension,Location,Detail,Fix|L|P0|
|2|FR-050.7|Adversarial merge report|Add multi-agent agreement analysis and merged count recalculation.|validation-report.md|FR-050.3,DM-007|section:Agent Agreement Analysis; categories:BOTH_AGREE,ONLY_A,ONLY_B,CONFLICT; recalculates:blocking_issues_count,tasklist_ready|L|P0|
|3|NFR-IMP-2|Precision constraint|Constrain reflection output to cited, specific, low false-positive findings.|validate_prompts.py|FR-050.5|prompt_phrase:thorough-but-precise; citation:required; unsupported_finding:omitted; false_positive_control:explicit|S|P0|
|4|COMP-017|Report section contract enforcer|Ensure prompts require every report body section and entry field.|validate_prompts.py|FR-050.6|sections:Summary,Blocking Issues,Warnings,Info,Validation Metadata; blocking_entry:Dimension+Location+Detail+Fix; warnings_entry:Dimension+Location+Detail+Fix; info_entry:Dimension+Location+Detail+Fix|M|P0|
|5|COMP-018|Finding citation validator|Require every reported finding to cite a file line or section.|validate_prompts.py|FR-050.6,NFR-IMP-2|location:file:line-or-file:section; empty_location:invalid; applies_to:B/W/I|S|P0|
|6|COMP-019|Agreement categorizer|Map agent findings into agreement categories for merge output.|validate_prompts.py|FR-050.7,DM-007|inputs:agent A findings,agent B findings; categories:BOTH_AGREE,ONLY_A,ONLY_B,CONFLICT; confidence:BOTH_AGREE high|M|P0|
|7|COMP-020|Conflict severity escalator|Escalate severity conflicts to the higher severity, with blocking as the conservative ceiling.|validate_prompts.py|FR-050.7|input:severity conflict; rule:higher severity; CONFLICT:escalated; evidence_check:required|S|P0|
|8|COMP-021|Merged count recalculator|Recompute report counts after agreement resolution instead of copying agent counts.|validate_prompts.py|FR-050.7|blocking_issues_count:merged B count; warnings_count:merged W count; info_count:merged I count; source:merged findings|M|P0|
|9|COMP-022|Tasklist readiness calculator|Derive readiness from blocking issue count in single and adversarial modes.|validation-report.md|FR-050.6,FR-050.7|tasklist_ready:true iff blocking_issues_count==0; applies_to:single/adversarial; gate_visible:true|S|P0|
|10|OPS-002|Blocking warning summary|Print prominent CLI warnings for blocking validation findings while preserving exit zero.|commands.py|NFR-IMP-1,FR-050.6|warning:visible; includes:B-IDs; exit_code:0; next_action:review validation-report.md|S|P0|
|11|OPS-003|Gate-failure artifact policy|Handle malformed or incomplete report artifacts consistently after gate failure.|validate_executor.py|OQ-007,COMP-008|gate_failed:warns; report_missing:tasklist_ready unknown/false message; report_partial:marked; downstream_guidance:clear|M|P0|
|12|COMP-023|N-agent merge extension|Define behavior for 3+ reflect agents while keeping two-agent table compatibility.|validate_prompts.py|OQ-005,FR-050.7|agents:>=2; two_agent_columns:Agent A,Agent B; n_agent_policy:defined; validation_mode:adversarial|M|P1|

### Integration Points — M4

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Report frontmatter → REFLECT_GATE|schema validation|Yes|M4|COMP-002|
|Report frontmatter → ADVERSARIAL_MERGE_GATE|schema validation|Yes|M4|COMP-002|
|Agent findings → agreement categorizer|merge strategy|Yes|M4|COMP-019|
|Agreement categorizer → count recalculator|callback wiring|Yes|M4|COMP-021|
|Count recalculator → tasklist_ready|derived-field wiring|Yes|M4|COMP-022|
|Gate failure → CLI warning summary|error middleware|Yes|M4|OPS-002,OPS-003|

### Milestone Dependencies — M4

- Depends on M2 prompt/gate builders and M3 CLI invocation; depends on OQ-003, OQ-005, OQ-006, and OQ-007 resolution from M1.

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Silent miss of real blocking issues|Medium|Medium|Users may proceed to tasklist despite unresolved roadmap defects|Set `tasklist_ready:false`, print B-ID warning summary, and cite every finding|Validation owner|
|2|Adversarial merge over-blocking|Low|Medium|CONFLICT escalation can overstate uncertain findings|Require evidence-evaluation before escalation and label ONLY_A/ONLY_B as review recommended|Validation owner|

## M5: Verification, Performance, and Release Readiness

**Objective:** Prove the validate feature meets functional, non-functional, architecture, and E2E criteria before release. | **Duration:** weeks 9-10 (2w) | **Entry:** M4 reports and warning UX implemented | **Exit:** unit, integration, E2E, performance, and import-boundary tests pass; release notes document invocation modes

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|NFR-050.1|Wall-time budget|Validate step adds no more than target wall time in single-agent mode.|performance|COMP-001|target:≤10% pipeline wall-time; single_agent:≤2min; measurement:timed E2E|M|P0|
|2|TEST-001|Standalone validate E2E|Verify validate runs with all three files and writes the validation report.|tests|FR-050.1,FR-050.2|command:roadmap validate <dir>; inputs:roadmap.md,test-strategy.md,extraction.md; output:validate/validation-report.md|M|P0|
|3|TEST-002|Multi-agent E2E|Verify multi-agent mode writes both reflect files and merged agreement report.|tests|FR-050.3,FR-050.7|command:--agents opus,haiku; outputs:reflect-opus-architect.md,reflect-haiku-architect.md,validation-report.md; includes:Agent Agreement Analysis|M|P0|
|4|TEST-003|Step builder single unit|Verify `_build_validate_steps` returns exactly one reflect step for one agent.|tests|FR-050.2,COMP-012|agents:1; result:1 Step; gate:REFLECT_GATE; output:validation-report.md|S|P0|
|5|TEST-004|Step builder multi unit|Verify `_build_validate_steps` returns parallel reflect group plus merge for multiple agents.|tests|FR-050.3,COMP-013|agents:2; result:[Step,Step] then Step; merge_gate:ADVERSARIAL_MERGE_GATE|S|P0|
|6|TEST-005|Injected duplicate ID finding|Verify a known duplicate deliverable ID is reported as a blocking structure issue.|tests|FR-050.5b,FR-050.6|fixture:duplicate D-ID; report:B-xxx; Dimension:structure; severity:BLOCKING|M|P0|
|7|TEST-006|Auto-validate and skip tests|Verify default roadmap run validates and `--no-validate` skips validation.|tests|FR-050.4,COMP-015|default:runs validate; --no-validate:skips; pipeline_success_required:true|M|P0|
|8|TEST-007|Tasklist readiness rule|Verify readiness is true only when there are zero blocking issues.|tests|COMP-022,FR-050.6|blocking_issues_count:0=>tasklist_ready true; blocking_issues_count>0=>false|S|P0|
|9|TEST-008|Gate criteria tests|Verify reflect and merge gates enforce their required frontmatter and agreement table checks.|tests|DM-003,COMP-002|REFLECT_GATE fields:blocking_issues_count,warnings_count,tasklist_ready; MERGE_GATE fields:+validation_mode,validation_agents; agreement_table:required|S|P0|
|10|TEST-009|Prompt content tests|Verify reflect and merge prompts include required dimensions and categories.|tests|FR-050.5,FR-050.7|reflect:7 dimensions present; merge:BOTH_AGREE,ONLY_A,ONLY_B present; precision wording:present|S|P0|
|11|TEST-010|Import boundary scan|Verify no `validate_*` imports appear under `pipeline/*` modules.|tests|NFR-050.2|scan_scope:pipeline/*; forbidden:validate_*; expected_count:0|S|P0|
|12|TEST-011|Dry-run plan test|Verify validate dry-run prints the planned steps without launching subprocesses.|tests|COMP-001|dry_run:prints plan; subprocess:0 launches; steps:single/multi shown|S|P1|
|13|TEST-012|Missing-files test|Verify missing required files produce a clear error before subprocess launch.|tests|OPS-001|missing:any required file; error:clear; exit:nonzero for preflight; subprocess:0 launches|S|P0|
|14|TEST-013|Gate-failure warning test|Verify malformed validation output warns and continues according to non-blocking contract.|tests|OPS-003,NFR-IMP-1|malformed_frontmatter:gate fails; warning:shown; exit_code:0; guidance:report incomplete|M|P0|

### Integration Points — M5

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Unit tests → step builders|test binding|Yes|M5|TEST-003,TEST-004|
|Prompt tests → prompt builders|test binding|Yes|M5|TEST-009|
|Gate tests → validate_gates|test binding|Yes|M5|TEST-008|
|E2E tests → CLI command|test binding|Yes|M5|TEST-001,TEST-002,TEST-006|
|Import scan → architecture rule|static validation|Yes|M5|TEST-010|
|Performance timing → validate execution|measurement hook|Yes|M5|NFR-050.1|

### Milestone Dependencies — M5

- Depends on M1-M4 completion; no release until architecture boundary, validation reports, and CLI invocation paths are covered.

### Risk Assessment and Mitigation — M5

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Wall-time budget breach|Medium|Medium|Validation becomes too slow for default roadmap runs|Keep single-agent default lean, parallelize multi-agent reflection, and measure timed E2E|QA owner|
|2|Test coverage misses resume or gate-failure edge paths|Medium|Low|Production users hit untested workflow branches|Add explicit resume, dry-run, missing-files, and gate-failure tests before release|QA owner|

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By Milestone|Status|Fallback|
|---|---|---|---|
|ClaudeProcess subprocess runtime|M2,M4,M5|Existing internal runtime|Gate-fail warning with report guidance|
|execute_pipeline step engine|M2,M3,M5|Existing internal pipeline infra|Do not proceed; NFR-050.4 forbids new engine|
|roadmap gate primitives|M1,M2,M4,M5|Existing internal gate code|Use `_frontmatter_values_non_empty` import from `.gates`|
|PipelineConfig, AgentSpec, Step models|M1,M2,M3|Existing internal models|Block M2 until model imports are stable|
|Click CLI framework|M3,M5|Existing dependency|Keep command additive and align current command idioms|
|Roadmap output artifacts|M3,M4,M5|Runtime input dependency|Preflight missing files and exit before subprocess launch|
|Model backends: opus, haiku, configured models|M2,M4,M5|Externally available through Claude runtime|Use single-agent default and bounded retries|

### Infrastructure Requirements

- Existing `src/superclaude/cli/roadmap/pipeline/executor.py` remains the only validate execution engine.
- Existing Claude subprocess runtime must support per-step timeout, retry, model selection, and grouped parallel steps.
- Validate output directory `<output-dir>/validate/` must be created or reused without changing `.roadmap-state.json`.
- CI must include unit tests, import-boundary scan, and at least one E2E path with representative roadmap artifacts.
- Performance measurement must record single-agent validate wall time against the ≤2 minute / ≤10% target.

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|R-001|Circular dependency regression|M1,M5|Medium|High|Approve one-directional dependency rule and enforce `pipeline/*` import scan|Architect|
|R-002|Unresolved CLI/report ambiguity|M1,M3,M4|Medium|High|Resolve OQ-001..OQ-007 before locking CLI and report behavior|Architect+CLI owner|
|R-003|Subprocess non-determinism or malformed frontmatter|M2,M4,M5|Medium|Medium|Use strict prompt schema, `retry_limit=1`, frontmatter gates, and warnings|Validation owner|
|R-004|Validation false positives|M2,M4|Medium|High|Require cited findings, precise dimensions, and adversarial agreement analysis|Prompt owner|
|R-005|Default agent-count mismatch between standalone and auto-invoke|M3,M5|Medium|Medium|Document defaults and test standalone/default auto-invoke separately|CLI owner|
|R-006|Missing-file UX confusion|M3,M5|Medium|Low|Preflight required artifacts and list absent files before subprocess launch|CLI owner|
|R-007|Silent miss of real blocking issues|M4,M5|Medium|Medium|Set `tasklist_ready:false`, print B-ID summary, and cite every finding|Validation owner|
|R-008|Adversarial merge over-blocking|M4,M5|Medium|Low|Evaluate evidence before escalation and mark one-agent findings for review|Validation owner|
|R-009|Wall-time budget breach|M5|Medium|Medium|Default to single-agent lean path, parallelize reflect group, and measure timed E2E|QA owner|
|R-010|Test coverage misses resume or gate-failure edge paths|M5|Low|Medium|Add resume, dry-run, missing-files, malformed-output, and gate-failure tests|QA owner|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|Milestone|
|---|---|---|---|---|
|Standalone validate writes report|Report path exists|`<dir>/validate/validation-report.md`|E2E `roadmap validate <dir>` with three required files|M5|
|Multi-agent outputs are complete|Reflect+merged files|2 reflect files + merged report + agreement table|E2E `--agents opus,haiku`|M5|
|Step layout is correct|Step count/shape|Single:1 reflect; multi:parallel group + merge|Unit tests for `_build_validate_steps`|M5|
|Injected duplicate ID is blocking|Finding severity|`B-xxx` with Dimension `structure`|Fixture with duplicate deliverable ID|M5|
|Auto-validation default works|Invocation behavior|Default runs; `--no-validate` skips|Integration tests for roadmap run|M5|
|Readiness derivation is correct|Boolean rule|`tasklist_ready` true iff blocking count is zero|Report schema unit test|M5|
|Gate criteria enforce schema|Gate pass/fail|Reflect and merge required fields enforced|Gate criteria tests|M5|
|Prompt coverage is complete|Prompt terms|7 dimensions and merge categories present|Prompt content unit tests|M5|
|Performance target met|Wall time|≤2 min single agent and ≤10% added time|Timed E2E measurement|M5|
|Import boundary preserved|Forbidden imports|0 `validate_*` imports under `pipeline/*`|Static import scan|M5|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|---|---|---|---|
|Validation execution model|Claude subprocess via existing pipeline steps|In-session validation (0.35), new validator engine (0.20), existing pipeline subprocess (0.90)|Subprocess isolation reduces confirmation bias and satisfies NFR-050.4 with lowest architecture drift|
|Single vs multi-agent implementation|One shared `_build_validate_steps` path returning list-of-1 or list-of-N+merge|Separate single/multi code (0.40), shared builder (0.95)|Shared path satisfies NFR-050.5 and reduces branch-specific bugs|
|CLI failure contract|Warn on blocking findings but exit zero|Exit non-zero on blocking findings (0.45), warn-and-continue (0.85)|Spec mandates non-blocking UX while preserving tasklist readiness signal|
|Gate design|Reuse GateCriteria/SemanticCheck and `_frontmatter_values_non_empty`|Duplicate gate logic (0.25), reuse existing gates (0.95)|Preserves NFR-007/NFR-050.4 and avoids duplicated schema behavior|
|Report merge policy|Agreement table with conservative conflict escalation|Simple concatenation (0.35), agreement analysis (0.85)|Agreement categories improve reviewer trust and make multi-agent output actionable|
|State handling|Keep `.roadmap-state.json` unchanged|Add validation state to roadmap state (0.30), separate validate artifacts (0.90)|Avoids schema migration and keeps validation additive|

## Timeline Estimates

|Milestone|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1|2w|Week 1|Week 2|Contracts, data models, architecture boundary, OQ resolution|
|M2|2w|Week 3|Week 4|Validate executor, gates, prompts, single/multi step layouts|
|M3|2w|Week 5|Week 6|Click validate command, auto-invocation, flag inheritance, preflight|
|M4|2w|Week 7|Week 8|Report schema, agreement merge, warning UX, readiness calculation|
|M5|2w|Week 9|Week 10|Unit/integration/E2E coverage, performance, import-boundary release gate|

**Total estimated duration:** 10 weeks
