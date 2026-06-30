---
spec_source: "spec-roadmap-remediate.compressed.md"
complexity_score: 0.7
complexity_class: HIGH
primary_persona: architect
adversarial: false
base_variant: "none"
variant_scores: "none"
convergence_score: null
---
# Roadmap Remediate — Project Roadmap

## Executive Summary

Extend `roadmap run` from a validate-only terminal workflow into a controlled 12-step remediate-and-certify pipeline. The architecture keeps the existing command surface intact while adding post-validation finding extraction, severity-scoped remediation, batch-by-file agent execution, rollback protection, and lightweight certification. The design prioritizes data integrity, operator control, and compatibility with existing roadmap state and gate mechanics.

**Business Impact:** Reduces manual roadmap validation cleanup by converting actionable findings into controlled edits, while preserving human choice over severity scope and preventing automatic remediation loops.

**Complexity:** HIGH (0.7) — 33 functional and 7 non-functional requirements add two new pipeline steps, concurrent file-group agents, rollback semantics, hash-gated resume, structured gates, parser fallback, and certification controls.

**Critical path:** Extend state and models → implement parser and gate definitions → wire interactive Phase A/B execution → add remediation executor with rollback → add certification prompt/gate → verify resume, isolation, and performance.

**Key architectural decisions:**

- Preserve `roadmap run` as the only operator command and handle the remediation prompt inside `execute_roadmap()`.
- Reuse `ClaudeProcess`, `execute_pipeline()`, `GateCriteria`, and existing roadmap state rather than creating new pipeline abstractions.
- Enforce batch-by-file parallelism with snapshot rollback so concurrent agents never edit the same target file.

**Open risks requiring resolution before M1:**

- Clarify retry ordering before rollback and global halt so executor behavior is deterministic.
- Confirm fallback `agreement_category` values for individual reflect-report findings.
- Confirm INFO-only path artifact expectations for `remediation-tasklist.md`.

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|---|---|---|---|---|---|---|---|
|M1|Contracts, Models, and Gates|foundation|P0|L|v2.20-WorkflowEvolution|25|Medium|
|M2|Validation Parsing and Scope Planning|backend|P0|L|M1|18|High|
|M3|Remediation Execution and Rollback|backend|P0|XL|M1,M2|21|High|
|M4|Certification and Resume Integration|backend|P0|L|M1,M2,M3|14|Medium|
|M5|Validation, Quality Gates, and Release Readiness|quality|P1|L|M1,M2,M3,M4|19|Medium|

## Dependency Graph

v2.20-WorkflowEvolution → M1 → M2 → M3 → M4 → M5
GateCriteria/SemanticCheck → M1 → M3,M4
ClaudeProcess → M1 → M3,M4
validate_executor.py → M2 → M3,M4
threading + os.replace → M3
sc:tasklist boundary → M4 → M5

## M1: Contracts, Models, and Gates

**Objective:** Establish additive contracts, gate criteria, model extensions, and pipeline step wiring boundaries before behavioral implementation. | **Duration:** Weeks 1-2 (2 weeks) | **Entry:** v2.20 pipeline infrastructure available; current roadmap tests pass. | **Exit:** Models, gates, state fields, step IDs, and import boundaries are defined with backward compatibility.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-001|12-step roadmap flow|Extend existing `roadmap run` into extract→generate-A→generate-B→diff→debate→score→merge→test-strategy→spec-fidelity→validate→remediate→certify without a new command.|executor.py|v2.20-WorkflowEvolution|step_order:12; command:roadmap run; no_new_cli:true; remediate_after:validate; certify_after:remediate|M|P0|
|2|FR-018|Remediate step boundary|Expose remediate as one pipeline step while using direct `ClaudeProcess` internals for per-file agents, aligned to `validate_run_step()` pattern.|remediate_executor.py|FR-001,NFR-002|outer_step:single; internal_process:ClaudeProcess; parallel:threading; not_execute_pipeline_internal:true|M|P0|
|3|FR-019|Remediate gate|Define `REMEDIATE_GATE` for `remediation-tasklist.md` with strict frontmatter and actionable-status semantic checks.|remediate_executor.py|DM-005|fields:type,source_report,source_report_hash,total_findings,actionable,skipped; min_lines:10; tier:STRICT; checks:frontmatter_values_non_empty,all_actionable_have_status|S|P0|
|4|FR-028|Certify gate|Define `CERTIFY_GATE` for `certification-report.md` with strict frontmatter and per-finding table semantic checks.|certify_gates.py|DM-006|fields:findings_verified,findings_passed,findings_failed,certified; min_lines:15; tier:STRICT; checks:frontmatter_values_non_empty,per_finding_table_present|S|P0|
|5|FR-029|Two-phase execution|Split execution so `execute_roadmap()` handles the prompt between Phase A steps 1-9 plus validation and Phase B remediate plus certify step.|executor.py|FR-001, FR-018|phase_a:execute_pipeline_steps_1_9+_auto_invoke_validate; prompt_location:execute_roadmap; phase_b:remediate_executor.execute+execute_pipeline_certify|L|P0|
|6|FR-030|Roadmap state extension|Extend `.roadmap-state.json` with additive validate, remediate, certify, validation lifecycle, and fidelity fields.|executor.py|DM-004,NFR-005|validate:blocking_count,warning_count,info_count,report_file; remediate:scope,findings_total/actionable/fixed/failed/skipped,agents_spawned,tasklist_file; certify:findings_verified/passed/failed,certified,report_file|M|P0|
|7|FR-032|Validation lifecycle|Maintain `validated-with-issues`→`remediated`→`certified` plus terminal `certified-with-caveats` state.|executor.py|FR-030|states:validated-with-issues,remediated,certified,certified-with-caveats; transitions:additive; persisted:true|S|P0|
|8|NFR-001|Atomic writes|Require tmp-file plus `os.replace()` for all generated tasklist, report, and state writes.|filesystem|FR-017, FR-025, FR-030|pattern:tmp+os.replace; torn_write:prevented; target_files:tasklist/report/state|S|P0|
|9|NFR-002|Process reuse|Avoid new subprocess abstractions and reuse `ClaudeProcess` for remediation and certification agents.|pipeline.process|COMP-009|subprocess_abstraction:ClaudeProcess; new_wrapper:false; inherited_model:true|S|P0|
|10|NFR-004 (inherited)|Pure prompt builders|Keep remediation and certification prompt builders pure with no I/O, subprocess calls, or side effects.|remediate_prompts.py,certify_prompts.py|COMP-002,COMP-004|inputs:models+strings; outputs:prompt_text; io:false; subprocess:false; side_effects:false|S|P0|
|11|NFR-005|Backward-compatible state|Keep `.roadmap-state.json` schema additive so existing consumers continue to operate.|executor.py|DM-004|schema_version:2; old_fields:preserved; new_fields:additive; consumers:unbroken|M|P0|
|12|NFR-006|Agent context isolation|Ensure each agent receives only prompt and `--file` inputs, with no continuation or session flags.|ClaudeProcess|COMP-009|inputs:prompt+--file; forbidden_flags:--continue/--session/--resume; isolation:per_process|M|P0|
|13|NFR-007 (inherited)|Unidirectional imports|Constrain new `remediate_*` and `certify_*` modules to import shared models without reverse imports.|module graph|COMP-001,COMP-002,COMP-003,COMP-004,COMP-005|allowed_imports:pipeline.models,roadmap.models,pipeline.process; forbidden_reverse_imports:true; cycle_count:0|S|P0|
|14|COMP-005|Certify gates module|Create `certify_gates.py` to hold certification gate criteria.|certify_gates.py|FR-028|name:certify_gates.py; role:define CERTIFY_GATE; dependencies:GateCriteria,SemanticCheck; source_ref:§4.1/§2.4.5|S|P0|
|15|COMP-006|Executor integration module|Modify `executor.py` for step construction, prompt flow, state save, resume application, and main roadmap execution.|executor.py|FR-029, FR-030|name:executor.py; role:_build_steps/post-validation prompt/_get_all_step_ids/_save_state/execute_roadmap/_apply_resume; dependencies:COMP-003,COMP-005,execute_pipeline; source_ref:§4.2/§2.5/§3.2|L|P0|
|16|COMP-007|Roadmap models module|Modify `models.py` with `Finding` dataclass and no new `RoadmapConfig` fields.|models.py|DM-001|name:models.py; role:add Finding dataclass and preserve RoadmapConfig shape; dependencies:dash; source_ref:§4.2/§2.3.1|M|P0|
|17|COMP-012|Remediate gate instance|Define `REMEDIATE_GATE` as a `GateCriteria` instance for remediation tasklist validation.|GateCriteria|FR-019,DM-005|name:REMEDIATE_GATE; role:validate remediation-tasklist.md; dependencies:GateCriteria,SemanticCheck; source_ref:§2.3.7|S|P0|
|18|COMP-013|Certify gate instance|Define `CERTIFY_GATE` as a `GateCriteria` instance for certification report validation.|GateCriteria|FR-028,DM-006|name:CERTIFY_GATE; role:validate certification-report.md; dependencies:GateCriteria,SemanticCheck; source_ref:§2.4.5|S|P0|
|19|COMP-014|Semantic check functions|Add semantic checks for non-empty frontmatter, actionable status coverage, and per-finding result table presence.|gates semantic checks|COMP-012,COMP-013|name:Semantic-check functions; role:_frontmatter_values_non_empty/_all_actionable_have_status/_has_per_finding_table; dependencies:dash; source_ref:§2.3.7/§2.4.5|M|P0|
|20|DM-001|Finding dataclass|Define structured validation finding object for parser, filtering, remediation, and certification flow.|models.py|COMP-007|id:str; severity:str; dimension:str; description:str; location:str; evidence:str; fix_guidance:str; files_affected:list[str]; status:str; agreement_category:str|M|P0|
|21|DM-002|Remediation tasklist frontmatter|Define `remediation-tasklist.md` frontmatter contract for gate validation and resume hashing.|remediation-tasklist.md|FR-017, FR-019|type:str(remediation-tasklist); source_report:str(path); source_report_hash:str(SHA-256); generated:str(ISO-8601); total_findings:int; actionable:int; skipped:int|S|P0|
|22|DM-003|Certification report frontmatter|Define `certification-report.md` frontmatter contract for certification outcomes.|certification-report.md|FR-025, FR-028|findings_verified:int; findings_passed:int; findings_failed:int; certified:bool; certification_date:str(ISO-8601)|S|P0|
|23|DM-004|Roadmap state schema|Define additive `.roadmap-state.json` v2 shape for validate, remediate, certify, lifecycle, and fidelity data.|.roadmap-state.json|FR-030,NFR-005|schema_version:int=2; steps:object; steps.validate:object(status,blocking_count,warning_count,info_count,report_file); steps.remediate:object(status,scope,findings_total,findings_actionable,findings_fixed,findings_failed,findings_skipped,agents_spawned,tasklist_file); steps.certify:object(status,findings_verified,findings_passed,findings_failed,certified,report_file); validation:object(status); fidelity_status:str|M|P0|
|24|DM-005|Remediate gate contract|Define `REMEDIATE_GATE` field and semantic criteria for tasklist acceptance.|GateCriteria|FR-019|required_frontmatter_fields:type,source_report,source_report_hash,total_findings,actionable,skipped; min_lines:10; enforcement_tier:STRICT; semantic_checks:frontmatter_values_non_empty,all_actionable_have_status|S|P0|
|25|DM-006|Certify gate contract|Define `CERTIFY_GATE` field and semantic criteria for certification acceptance.|GateCriteria|FR-028|required_frontmatter_fields:findings_verified,findings_passed,findings_failed,certified; min_lines:15; enforcement_tier:STRICT; semantic_checks:frontmatter_values_non_empty,per_finding_table_present|S|P0|

### Integration Points — M1

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`_build_steps()` step registry|dispatch table|Yes|M1|`execute_roadmap()`, `--resume`, step execution|
|`REMEDIATE_GATE`|gate registry entry|Yes|M1|`remediate_executor.py`, validation gate checks|
|`CERTIFY_GATE`|gate registry entry|Yes|M1|certify step, resume gate checks|
|`SemanticCheck` functions|callback wiring|Yes|M1|`GateCriteria` semantic validation|
|`.roadmap-state.json` v2 fields|state contract|Yes|M1|resume logic, operator reporting, downstream tasklist boundary|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|State schema additions break existing consumers|High|Low|Resume and validation commands may misread state|Keep fields additive, preserve existing keys, add compatibility tests before behavioral work|Architect|
|2|Gate semantics drift from artifact frontmatter|Medium|Medium|Valid outputs may fail gates or invalid outputs may pass|Define DM gate contracts first and test gate checks against positive and negative fixtures|Backend lead|
|3|Import direction violates pipeline layering|Medium|Low|Cycles make CLI imports brittle|Add import-linter or focused tests for `remediate_*`/`certify_*` dependencies|Architect|

### Milestone Dependencies — M1

- Requires v2.20-WorkflowEvolution pipeline infrastructure.
- Requires existing `GateCriteria`, `SemanticCheck`, `ClaudeProcess`, and roadmap executor modules to remain available.

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-010|Confirm no external HTTP or route surface is expected for this CLI-only feature.|Prevents accidental API work and keeps scope bounded to CLI artifacts.|Product owner|Before M1 exit|

## M2: Validation Parsing and Scope Planning

**Objective:** Convert validation reports into structured findings, terminal summaries, remediation scope decisions, and actionable tasklist planning. | **Duration:** Weeks 3-4 (2 weeks) | **Entry:** M1 contracts merged; gate and model tests pass. | **Exit:** Merged and fallback validation reports parse into deduplicated findings with correct severity filtering and tasklist status planning.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-002|Validation report counts|Parse merged validation report and extract BLOCKING, WARNING, and INFO counts.|remediate_parser.py|DM-001|sources:validate/reflect-merged.md,validate/merged-validation-report.md; severities:BLOCKING/WARNING/INFO; counts:int|M|P0|
|2|FR-003|Terminal summary box|Print concise terminal summary with finding counts plus IDs and descriptions per severity.|executor.py|FR-002|box:present; counts:all_severities; details:id+description; output:terminal|S|P0|
|3|FR-004|Tiered remediation prompt|Present `[1] BLOCKING only`, `[2] BLOCKING + WARNING`, `[3] All`, `[n] Skip` remediation choices.|executor.py|FR-002,OQ-008|options:1/2/3/n; scope_mapping:exact; prompt_location:execute_roadmap; interactive:true|M|P0|
|4|FR-005|Skip outcome|On `n`, end pipeline with `validated-with-issues` state and keep validation report for manual review.|executor.py|FR-004|input:n; state:validated-with-issues; report:retained; remediation:not_run|S|P0|
|5|FR-006|Selected scope tasklist|On selected scope, proceed to Step 10 and mark findings outside scope as SKIPPED in remediation tasklist.|remediate_executor.py|FR-004, FR-009|selected_scope:1/2/3; out_of_scope_status:SKIPPED; tasklist:remediation-tasklist.md|M|P0|
|6|FR-007|Auto path for low severity|Skip prompt when no BLOCKING and no WARNING; certify directly when zero findings or INFO-only findings exist.|executor.py|FR-002,OQ-008|condition:blocking=0+warning=0; info=0:certify; info>0:certify; prompt:skipped|M|P0|
|7|FR-008|Finding object extraction|Extract all ten `Finding` fields from validation reports for downstream filtering and prompts.|remediate_parser.py|DM-001|id; severity; dimension; description; location; evidence; fix_guidance; files_affected; status; agreement_category|L|P0|
|8|FR-009|Severity scope filtering|Filter findings by choice: BLOCKING only, BLOCKING+WARNING, or all severities with fix guidance.|remediate_executor.py|FR-004, FR-008|option1:BLOCKING_with_guidance; option2:BLOCKING+WARNING; option3:all_with_guidance; no_guidance:excluded|M|P0|
|9|FR-010|Always-skipped statuses|Mark `NO_ACTION_REQUIRED` and `OUT_OF_SCOPE` findings SKIPPED regardless of selected severity scope.|remediate_executor.py|FR-009|source_status:NO_ACTION_REQUIRED/OUT_OF_SCOPE; output_status:SKIPPED; selection_override:false|S|P0|
|10|FR-011|Zero actionable guard|Emit tasklist with actionable 0 and all entries SKIPPED, then certify with zero verified and certified true.|remediate_executor.py|FR-009, FR-010|tasklist:actionable=0; entries:SKIPPED; certification:findings_verified=0,certified=true|M|P0|
|11|FR-033|Fallback parser and dedup|When merged report is missing or malformed, parse individual reflect reports and deduplicate by location proximity and severity precedence.|remediate_parser.py|FR-008,OQ-007|fallback_sources:reflect-opus-architect.md,reflect-haiku-analyzer.md,reflect-*.md; dedup:file+overlap_or_within_5_lines; severity_order:BLOCKING>WARNING>INFO; guidance:merged_specific; none_parseable:skip_with_warning|XL|P0|
|12|COMP-001|Remediation parser module|Create parser module that reads reports into `Finding` objects and applies fallback dedup behavior.|remediate_parser.py|DM-001,FR-033|name:remediate_parser.py; role:parse validation reports to Finding objects with fallback and dedup; dependencies:roadmap.models,report files; source_ref:§4.1/§2.3.1|L|P0|
|13|COMP-008|Validate executor reference|Use existing validation executor output and direct-process pattern without modifying validation execution semantics.|validate_executor.py|FR-002, FR-018|name:validate_executor.py; role:structured finding counts and validate_run_step pattern; dependencies:ClaudeProcess; source_ref:§4.2/§2.3.7|S|P1|
|14|COMP-011|Auto validate integration|Reuse `_auto_invoke_validate()` as the boundary that produces validation reports consumed by remediation.|executor.py|FR-029|name:_auto_invoke_validate(); role:existing post-step-9 validation invocation; dependencies:dash; source_ref:§2.5|S|P0|
|15|COMP-021|Finding count extractor|Add parser routine for severity totals and per-severity finding summaries from merged validation text.|remediate_parser.py|FR-002, FR-003|name:finding-count extractor; role:derive counts and summary entries; dependencies:COMP-001,DM-001; source_ref:§2.2|M|P0|
|16|COMP-022|Severity scope filter|Add pure filtering routine that maps operator choice to actionable and skipped findings.|remediate_executor.py|FR-009, FR-010|name:severity-scope filter; role:map choices to FIX candidate set and skipped set; dependencies:DM-001; source_ref:§2.3.2|M|P0|
|17|COMP-023|Individual report fallback reader|Add reader for `reflect-*.md` reports when merged validation output cannot be parsed.|remediate_parser.py|FR-033|name:individual-report fallback reader; role:parse per-agent reflect reports; dependencies:report files,DM-001; source_ref:§2.8/OQ-003|M|P0|
|18|COMP-024|Finding dedup resolver|Add resolver for overlapping-location findings with severity precedence and merged guidance.|remediate_parser.py|FR-033|name:finding dedup resolver; role:deduplicate by file+line proximity and merge guidance; dependencies:COMP-023,DM-001; source_ref:§2.8/OQ-003|M|P0|

### Integration Points — M2

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Validation report parser selection|strategy pattern|Yes|M2|`remediate_executor.py`|
|Severity scope filter|dispatch table|Yes|M2|tasklist generator, remediation grouping|
|Fallback report reader|fallback chain|Yes|M2|parser when merged report is missing or malformed|
|Dedup resolver|callback wiring|Yes|M2|fallback parser result consolidation|
|Terminal prompt handler|interactive binding|Yes|M2|Phase B launch decision in `execute_roadmap()`|

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Report format changes break parser|High|Low|Remediation may skip actionable findings|Test merged and individual report formats; fall back gracefully; log warning when no reports parse|Backend lead|
|2|Dedup merges unrelated findings|Medium|Medium|Distinct remediation work may be lost|Require same file plus overlap or within five lines; keep higher severity and retain merged guidance|Architect|
|3|Operator prompt scope misclassifies INFO-only runs|Medium|Medium|Artifacts or certification path may diverge from spec intent|Resolve OQ-008 and encode branch tests for zero, INFO-only, WARNING, and BLOCKING cases|Product owner|

### Milestone Dependencies — M2

- Requires M1 `Finding`, gate, state, and execution contracts.
- Requires validation outputs from `_auto_invoke_validate()` and existing report naming conventions.

### Open Questions — M2

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-007|What `agreement_category` value should individual-report fallback findings use before merge context exists?|Blocks deterministic `Finding` construction under fallback parsing.|Architect|Before M2 exit|
|2|OQ-008|Should INFO-only auto-path runs still emit `remediation-tasklist.md`, and if so with what `actionable` value?|Blocks artifact and resume behavior for INFO-only validation reports.|Product owner|Before M2 exit|

## M3: Remediation Execution and Rollback

**Objective:** Execute scoped remediation safely through file-grouped agents, strict editable-file controls, tasklist emission, retries, snapshots, and rollback. | **Duration:** Weeks 5-7 (3 weeks) | **Entry:** M2 parser and scope planner accepted; OQ-007/OQ-008 resolved. | **Exit:** Actionable findings are grouped by target file, remediated in parallel, written atomically, and rolled back on failure.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-012|Batch-by-file grouping|Group actionable findings by primary target file so one agent owns all findings for a file and different files run in parallel.|remediate_executor.py|FR-009|group_key:primary_target_file; one_agent_per_file:true; same_file_parallel:false; different_files_parallel:true|M|P0|
|2|FR-013|Cross-file finding split|Include cross-file findings in each affected file agent prompt with file-scoped guidance and cross-agent note.|remediate_prompts.py|FR-012,OQ-009|files:roadmap.md,test-strategy.md,extraction.md; prompt_scope:YOUR_FILE; other_side_note:true; finding_represented_in_each_file:true|M|P0|
|3|FR-014|Constrained agent prompts|Build prompts that allow editing only one target file, only listed fixes, and preserve frontmatter, headings, and section order unless guidance requires change.|remediate_prompts.py|NFR-004, NFR-006|edit_scope:one_file; fixes:list_only; preserve_frontmatter:true; preserve_headings:true; reorder_only_if_guidance:true|M|P0|
|4|FR-015|Agent execution parameters|Run each remediation agent with 300-second timeout, one retry on failure, and parent-inherited model.|remediate_executor.py|FR-018,OQ-004|timeout_seconds:300; retries:1; model:parent_config; failure_policy:clarified_before_exit|S|P0|
|5|FR-016|Editable files constraint|Restrict remediation edits to `roadmap.md`, `extraction.md`, and `test-strategy.md`; exclude phase tasklists.|remediate_executor.py|NFR-006,OQ-009|allowed:roadmap.md,extraction.md,test-strategy.md; denied:phase-tasklist files; violations:0|M|P0|
|6|FR-017|Remediation tasklist artifact|Emit standalone `remediation-tasklist.md` with required frontmatter and BLOCKING/WARNING/SKIPPED sections.|remediation-tasklist.md|DM-002,FR-019|frontmatter:DM-002; sections:BLOCKING/WARNING/SKIPPED; phase_tasklist_format:false; atomic_write:true|M|P0|
|7|FR-020|Pre-remediation snapshots|Snapshot every target file to `<file>.pre-remediate` before spawning agents.|snapshot manager|FR-012,NFR-001|files:roadmap.md/test-strategy.md/extraction.md; snapshot_suffix:.pre-remediate; before_agents:true|S|P0|
|8|FR-021|Failure rollback|On non-zero exit or timeout, halt agents, restore snapshots, mark failed and cross-file findings FAILED, fail remediate, and halt pipeline.|remediate_executor.py|FR-020, FR-015,OQ-004|trigger:exit_nonzero_or_timeout; rollback:all_targets; statuses:FAILED; step:FAIL; pipeline:halt|XL|P0|
|9|FR-022|Success cleanup|On full success, delete snapshots and set agent-targeted findings to FIXED.|remediate_executor.py|FR-020, FR-021|success:all_agents_zero; snapshots:deleted; statuses:FIXED; step:remediated|S|P0|
|10|NFR-003|Runtime budget|Keep Steps 10-11 within 30% of the wall-clock duration of Steps 1-9 for the same run.|performance harness|FR-015, FR-023|metric:(t10+t11)/(t1_to_t9); target:<=0.30; baseline:same_run; reported:true|M|P1|
|11|COMP-002|Remediation prompts module|Create pure prompt builder for per-file groups and cross-file guidance.|remediate_prompts.py|FR-013, FR-014|name:remediate_prompts.py; role:build scoped fix prompts per file group; dependencies:pipeline.models,roadmap.models; source_ref:§4.1/§2.3.4|M|P0|
|12|COMP-003|Remediation executor module|Create executor for parse, filter, group, snapshot, spawn, collect, rollback, and tasklist updates.|remediate_executor.py|COMP-001,COMP-002|name:remediate_executor.py; role:orchestrate extract/filter/batch/snapshot/spawn/collect/rollback; dependencies:COMP-001,COMP-002,ClaudeProcess,threading; source_ref:§4.1/§2.3.7/§2.3.8|XL|P0|
|13|COMP-009|ClaudeProcess reuse|Use existing `ClaudeProcess` to spawn remediation agents with inherited model configuration.|pipeline.process|NFR-002, FR-015|name:ClaudeProcess; role:subprocess abstraction for agents; dependencies:dash; source_ref:§2.3.7/§5.1|S|P0|
|14|COMP-025|Batch-by-file grouper|Add grouping function from actionable findings to per-file agent work items.|remediate_executor.py|FR-012|name:batch-by-file grouper; role:group findings by primary target file; dependencies:DM-001,COMP-022; source_ref:§2.3.3|M|P0|
|15|COMP-026|Cross-file prompt splitter|Add routine that derives file-specific guidance fragments for findings spanning multiple target files.|remediate_prompts.py|FR-013|name:cross-file prompt splitter; role:create YOUR FILE guidance and peer-agent note; dependencies:DM-001; source_ref:§2.3.4|M|P0|
|16|COMP-027|Snapshot rollback manager|Add snapshot, restore, and cleanup routines for all editable target files.|remediate_executor.py|FR-020..022|name:snapshot rollback manager; role:snapshot/restore/delete .pre-remediate files; dependencies:os.replace,filesystem; source_ref:§2.3.8|L|P0|
|17|COMP-028|Agent thread runner|Add threaded runner for independent file-group remediation agents with result capture.|remediate_executor.py|FR-012, FR-015|name:agent thread runner; role:run one ClaudeProcess per file group in parallel; dependencies:threading,ClaudeProcess; source_ref:§2.3.7|L|P0|
|18|COMP-029|Remediation tasklist writer|Add atomic writer for frontmatter plus severity and skipped sections.|remediate_executor.py|FR-017,DM-002|name:remediation tasklist writer; role:write remediation-tasklist.md with statuses; dependencies:DM-002,NFR-001; source_ref:§2.3.6|M|P0|
|19|COMP-030|Editable file guard|Add guard that rejects attempted remediation targets outside the three allowed files.|remediate_executor.py|FR-016|name:editable file guard; role:enforce allowed target file set; dependencies:DM-001; source_ref:§2.3.5/§5.2|M|P0|
|20|COMP-031|Agent result collector|Add collector that maps process exits, timeouts, retries, and finding statuses into remediate state.|remediate_executor.py|FR-021, FR-022|name:agent result collector; role:collect process outcomes and update finding statuses; dependencies:COMP-028,DM-004; source_ref:§2.3.8|M|P0|
|21|COMP-032|Retry controller|Add failure retry control that executes the single allowed retry before final failure handling.|remediate_executor.py|FR-015,OQ-004|name:retry controller; role:apply one retry policy before rollback decision; dependencies:COMP-028,COMP-031; source_ref:§2.3.4/§2.3.8|S|P0|

### Integration Points — M3

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|File-group work item map|dispatch table|Yes|M3|agent thread runner|
|Cross-file guidance splitter|strategy pattern|Yes|M3|remediation prompt builder|
|Editable file guard|policy middleware|Yes|M3|grouping, snapshots, agent launch|
|Snapshot rollback manager|failure callback|Yes|M3|agent result collector|
|Retry controller|failure middleware|Yes|M3|agent thread runner, rollback manager|
|Remediation tasklist writer|artifact writer|Yes|M3|remediate gate, resume, certify input|

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Remediation agent introduces new issues|Medium|Medium|Roadmap artifacts may pass old finding checks but regress elsewhere|Constrain prompts, certify fixed findings, and leave full validate available to user|Backend lead|
|2|Cross-file findings cause conflicting edits|Medium|Low|Two agents may alter related content inconsistently|Assign one agent per file, include peer-agent note, and certify each finding after edits|Architect|
|3|User interruption leaves snapshots or partial edits|Low|Low|Workspace may retain pre-remediation files or inconsistent state|Write state after completed boundaries; restore snapshots on caught failures; resume from gates|Backend lead|
|4|Retry and rollback order remains ambiguous|High|Medium|Implementation may conflict with stakeholder expectation|Resolve OQ-004 before executor merge and encode tests for retry-before-rollback behavior|Product owner|

### Milestone Dependencies — M3

- Requires M2 actionable findings, skipped findings, and target file resolution.
- Requires M1 atomic write and isolation rules.
- Requires OQ-004 and OQ-009 decisions before exit.

### Open Questions — M3

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-004|Does the single retry occur before global halt and rollback, or can halt preempt retry?|Blocks failure-state and rollback implementation.|Product owner|Before M3 implementation exit|
|2|OQ-009|Confirm the on-disk extraction artifact filename targeted by remediation agents: `extraction.md` vs generated `extract` output name.|Blocks editable-file guard and snapshot coverage.|Backend lead|Before M3 implementation exit|

## M4: Certification and Resume Integration

**Objective:** Certify remediation outcomes with a single scoped verifier, integrate resume gates, and finalize terminal states without creating an automatic fix loop. | **Duration:** Weeks 8-9 (2 weeks) | **Entry:** M3 remediates and rolls back correctly; remediation tasklist gate passes. | **Exit:** Certification reports fixed-finding results, resume skips valid outputs, and terminal lifecycle states are persisted.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-023|Scoped certification pass|Run one lightweight certification agent to verify fixed findings via checklist without full adversarial validation.|certify_prompts.py|FR-022|agent_count:1; pass_count:1; scope:fixed_findings; full_debate:false; checklist:true|M|P0|
|2|FR-024|Relevant section context|Provide only relevant sections surrounding each finding location to the certify agent.|certify_prompts.py|FR-023|context:section_snippets; full_file:false; accuracy:preserved; token_cost:minimized|M|P0|
|3|FR-025|Certification report artifact|Emit `certification-report.md` with frontmatter, per-finding result table, and summary.|certification-report.md|DM-003,FR-028|frontmatter:DM-003; table:Finding/Severity/Result/Justification; summary:present; atomic_write:true|M|P0|
|4|FR-026|Certification outcomes|Set success state when all PASS; set `certified-with-caveats` when any FAIL; complete pipeline without looping.|executor.py|FR-025, FR-027,OQ-006|all_pass:certified=true+tasklist_ready=true; any_fail:certified-with-caveats; pipeline:complete; loop:false|M|P0|
|5|FR-027|Single-pass control|Prevent automatic remediation loops after certification failures; leave rerun choice to user.|executor.py|FR-026|auto_loop:false; user_action:rerun roadmap validate; terminal:reported|S|P0|
|6|FR-031|Resume gate behavior|Skip to remediate, certify, or complete based on gate-passing outputs and source report hash matching.|executor.py|DM-004,OQ-006|validate_gate_pass:skip_to_remediate; remediate_all_fixed+hash_match:skip_to_certify; hash_mismatch:rerun_remediate; certify_gate_pass:complete|L|P0|
|7|COMP-004|Certification prompts module|Create pure certification prompt builder using finding snippets and checklist instructions.|certify_prompts.py|FR-023, FR-024|name:certify_prompts.py; role:build single-agent certification verification prompt; dependencies:pipeline.models,roadmap.models; source_ref:§4.1/§2.4.2|M|P0|
|8|COMP-010|Pipeline runner reuse|Run certify as a standard single step through existing `execute_pipeline()`.|execute_pipeline()|FR-029|name:execute_pipeline(); role:outer non-interactive pipeline runner and certify step runner; dependencies:dash; source_ref:§2.5/§2.3.7|S|P0|
|9|COMP-015|Step builder wiring|Extend `_build_steps()` so validate, remediate, and certify step definitions are registered in order.|executor.py|FR-001, FR-029|name:_build_steps(); role:construct ordered step registry; dependencies:COMP-003,COMP-005; source_ref:§4.2|M|P0|
|10|COMP-016|Post-validation prompt handler|Add prompt decision logic between validation completion and remediation launch.|executor.py|FR-003..005, FR-007|name:post-validation prompt handler; role:show counts and collect severity scope decision; dependencies:COMP-021,COMP-022; source_ref:§2.2/§2.5|M|P0|
|11|COMP-017|All-step ID provider|Extend `_get_all_step_ids()` so resume and progress reporting know all 12 steps.|executor.py|FR-001, FR-031|name:_get_all_step_ids(); role:return complete step ID list; dependencies:step registry; source_ref:§4.2|S|P0|
|12|COMP-018|State save hook|Extend `_save_state()` to persist validate, remediate, certify, lifecycle, and report fields atomically.|executor.py|FR-030,NFR-001|name:_save_state(); role:persist additive state fields; dependencies:DM-004,os.replace; source_ref:§4.2/§3.1|M|P0|
|13|COMP-019|Roadmap execution orchestrator|Modify `execute_roadmap()` as the top-level coordinator for Phase A, prompt, remediate, and certify.|executor.py|FR-029|name:execute_roadmap(); role:coordinate Phase A prompt and Phase B execution; dependencies:execute_pipeline,_auto_invoke_validate,remediate_executor; source_ref:§2.5/§4.2|L|P0|
|14|COMP-020|Resume applicator|Extend `_apply_resume()` for validate, remediate hash checks, certification gate completion, and caveat handling.|executor.py|FR-031|name:_apply_resume(); role:skip completed validate/remediate/certify work based on gates and hashes; dependencies:DM-004,REMEDIATE_GATE,CERTIFY_GATE; source_ref:§3.2/§4.2|L|P0|

### Integration Points — M4

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Certify step definition|step registry|Yes|M4|`execute_pipeline([certify_step])`|
|Relevant-section extractor|context selection strategy|Yes|M4|certify prompt builder|
|Certification result table parser|report validation callback|Yes|M4|`CERTIFY_GATE`, state save|
|Resume hash comparison|state decision branch|Yes|M4|`_apply_resume()`|
|Lifecycle state writer|state transition hook|Yes|M4|CLI completion and downstream tasklist boundary|

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Certification agent is too lenient|Low|Medium|Unfixed findings may be marked PASS|Use checklist prompts, per-finding justifications, strict result table, and allow full validate rerun|QA lead|
|2|Resume skips stale remediation output|High|Low|Certify may validate edits against old report context|Require SHA-256 source report hash match before skip to certify|Backend lead|
|3|Caveat state semantics conflict with success criteria|Medium|Medium|Operator may misinterpret pipeline completion as full certification|Resolve OQ-006 and display explicit caveat state in report and state file|Product owner|

### Milestone Dependencies — M4

- Requires M3 successful remediation tasklist and fixed finding statuses.
- Requires M1 gates and state schema.
- Requires OQ-006 decision for caveat success semantics.

### Open Questions — M4

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-006|Does `certified-with-caveats` count as pipeline success when SC-002 still passes for BLOCKING findings?|Blocks final completion messaging and success metric interpretation.|Product owner|Before M4 exit|
|2|OQ-011|When a remediation tasklist has some FAILED entries but the source hash still matches, should resume rerun remediation or report caveats immediately?|Blocks `_apply_resume()` handling for partial-fixed tasklists.|Architect|Before M4 exit|

## M5: Validation, Quality Gates, and Release Readiness

**Objective:** Prove the 12-step pipeline meets functional, safety, compatibility, and performance criteria before release. | **Duration:** Weeks 10-11 (2 weeks) | **Entry:** M4 certification and resume behavior accepted; unresolved OQs closed or documented with decisions. | **Exit:** Success criteria pass, risk mitigations are verified, and downstream tasklist handoff is ready.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|SC-001|Twelve-step completion|Validate that `roadmap run` completes all 12 steps without manual intervention after remediation approval.|acceptance tests|M1,M2,M3,M4|metric:completed_steps; target:12/12; condition:user_approves_remediation|M|P0|
|2|SC-002|Blocking certification pass rate|Verify at least 90% of BLOCKING findings receive PASS in certification report.|certification tests|FR-025, FR-026|metric:blocking_findings_passed/blocking_findings_verified; target:>=0.90; source:certification-report.md|M|P0|
|3|SC-003|No false certification passes|Ensure certification identifies unfixed findings rather than marking them PASS.|certification negative tests|FR-023, FR-025|metric:false_passes; target:0; fixtures:unfixed_findings|M|P0|
|4|SC-004|Resume skip correctness|Validate `--resume` skips completed remediation and certification only when gates and hashes allow it.|resume tests|FR-031|metric:skip_decisions; target:matches_§3.2; cases:validate/remediate/certify/hash_mismatch|L|P0|
|5|SC-005|Editable file boundary|Verify remediation never edits files outside `roadmap.md`, `extraction.md`, and `test-strategy.md`.|file boundary tests|FR-016|metric:outside_edits; target:0; tracked_files:allowed_set_only|M|P0|
|6|SC-006|Performance overhead|Measure Steps 10-11 overhead against Steps 1-9 and keep it at or below 30%.|performance tests|NFR-003|metric:(t10+t11)/(t1_to_t9); target:<=0.30; baseline:same_run|M|P1|
|7|SC-007|Tasklist status fidelity|Verify remediation tasklist represents every finding and final status accurately.|artifact tests|FR-017,DM-002|metric:findings_represented_with_correct_status; target:100%; statuses:FIXED/FAILED/SKIPPED|M|P0|
|8|SC-008|State compatibility|Validate `.roadmap-state.json` remains backward-compatible with additive fields only.|state compatibility tests|DM-004,NFR-005|metric:consumer_breakage; target:0; field_policy:additive|M|P0|
|9|AC-1|Context isolation constraint|Verify inherited context isolation by passing only prompt and file inputs to agents.|isolation tests|NFR-006|constraint:context isolation; inherited_ref:FR-003; agent_inputs:prompt+--file; forbidden:--continue/--session/--resume|S|P0|
|10|AC-2|Pure prompt constraint|Verify prompt builders remain pure and side-effect free.|prompt tests|NFR-004|constraint:pure prompts; io:false; subprocess:false; side_effects:false|S|P0|
|11|AC-3|Import direction constraint|Verify unidirectional imports for remediate and certify modules.|import tests|NFR-007|constraint:unidirectional imports; allowed:remediate/certify→pipeline.models,roadmap.models; reverse:false|S|P0|
|12|AC-4|Atomic write constraint|Verify generated artifacts and state use tmp plus `os.replace()`.|write tests|NFR-001|constraint:atomic writes; pattern:tmp+os.replace; target:reports/tasklists/state|S|P0|
|13|AC-5|Process abstraction constraint|Verify executor uses existing `ClaudeProcess` and no new subprocess abstraction.|process tests|NFR-002|constraint:no new subprocess abstractions; required:ClaudeProcess; wrappers:0|S|P0|
|14|AC-6|Editable boundary constraint|Verify remediation agents may edit only roadmap, extraction, and test-strategy artifacts.|file boundary tests|FR-016|constraint:editable-files boundary; allowed:roadmap.md,extraction.md,test-strategy.md; denied:phase tasklists|M|P0|
|15|AC-7|Pipeline contract constraint|Verify prompt handling remains in `execute_roadmap()` and `execute_pipeline()` stays non-interactive.|executor tests|FR-029|constraint:pipeline contract; prompt_location:execute_roadmap; execute_pipeline_interactive:false|M|P0|
|16|AC-8|Single-pass constraint|Verify remediation and certification do not enter an automatic loop.|flow tests|FR-027|constraint:single pass; auto_loop:false; failure_result:reported|S|P0|
|17|AC-9|Validation scope constraint|Verify no full adversarial re-validation and no per-finding cherry-pick UI are added.|scope tests|FR-023, FR-027|constraint:scope; full_revalidation:false; tasklist_remediation:false; selection:severity_scope_only|S|P1|
|18|AC-10|Module placement constraint|Verify new code lives under `src/superclaude/cli/roadmap/`.|path tests|COMP-001,COMP-003,COMP-004,COMP-005|constraint:module placement; root:src/superclaude/cli/roadmap; violations:0|S|P0|
|19|AC-11|Infrastructure dependency constraint|Verify roadmap-remediate depends on v2.20 workflow infrastructure before release.|release gate|M1|constraint:dependency; requires:v2.20-WorkflowEvolution; release_without_dependency:false|S|P0|

### Integration Points — M5

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Acceptance test matrix|test dispatch table|Yes|M5|CI and release gate|
|Performance measurement hook|metrics callback|Yes|M5|SC-006 validation|
|Resume fixture matrix|test strategy|Yes|M5|SC-004 validation|
|File edit tracker|policy check|Yes|M5|SC-005 validation|
|Downstream tasklist handoff|integration boundary|Yes|M5|`sc:tasklist` after certification|

### Risk Assessment and Mitigation — M5

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Test coverage misses fallback parser paths|High|Medium|Malformed report regressions may reach users|Add merged, individual, malformed, empty, and duplicate-location fixtures|QA lead|
|2|Performance budget fails under large finding volume|Medium|Medium|Remediate/certify may exceed SC-006|Batch by file, pass relevant snippets to certify, and report timing separately for Steps 10-11|Performance owner|
|3|Downstream tasklist integration expects fully certified state only|Medium|Low|`certified-with-caveats` may be consumed incorrectly|Block tasklist-ready flag unless certification semantics explicitly allow it|Architect|

### Milestone Dependencies — M5

- Requires M1-M4 feature work complete and runnable through `roadmap run`.
- Requires all residual OQ decisions recorded in implementation notes or tests.

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By Milestone|Status|Fallback|
|---|---|---|---|
|v2.20-WorkflowEvolution pipeline infrastructure|M1|Required|Defer roadmap-remediate until infrastructure branch is available|
|`ClaudeProcess` from `pipeline.process`|M1,M3,M4|Available|Block implementation; no alternate subprocess abstraction allowed|
|`execute_pipeline()`|M1,M4|Available|Keep certify step out of release until runner supports single-step invocation|
|`validate_executor.py` reports|M2,M3,M4|Available|Use individual `reflect-*.md` fallback parser|
|`GateCriteria` / `SemanticCheck` framework|M1,M3,M4|Available|Block gate work until framework extension point is confirmed|
|`pipeline.models`|M1,M3,M4|Available|Keep prompt builder types local only until shared import is accepted|
|`roadmap.models`|M1,M2,M3,M4|Available|Add `Finding` locally in roadmap models before parser work|
|`threading` stdlib|M3|Available|Run file groups sequentially with warning if concurrency must be disabled|
|`os.replace` and filesystem snapshots|M1,M3|Available|Block release on platforms lacking atomic replace semantics|
|`sc:tasklist` downstream boundary|M4,M5|External consumer|Emit explicit `tasklist_ready` only after certification semantics are resolved|

### Infrastructure Requirements

- CI job for roadmap unit and regression tests using UV commands only.
- Fixture set covering merged reports, individual reflect reports, malformed reports, empty reports, duplicate-location findings, cross-file findings, INFO-only reports, and hash mismatch resume.
- File edit tracker for enforcing allowed remediation targets.
- Timing capture for Steps 1-9 baseline and Steps 10-11 overhead.
- Artifact directory permissions for `.pre-remediate` snapshots, `remediation-tasklist.md`, `certification-report.md`, and `.roadmap-state.json` writes.

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|R-001|State schema additions break existing consumers|M1|Low|High|Keep fields additive, preserve existing keys, add compatibility tests before behavioral work|Architect|
|R-002|Gate semantics drift from artifact frontmatter|M1|Medium|Medium|Define DM gate contracts first and test gate checks against positive and negative fixtures|Backend lead|
|R-003|Import direction violates pipeline layering|M1|Low|Medium|Add import-focused tests for `remediate_*` and `certify_*` dependencies|Architect|
|R-004|Report format changes break parser|M2|Low|High|Test merged and individual report formats; fall back gracefully; log warning when no reports parse|Backend lead|
|R-005|Dedup merges unrelated findings|M2|Medium|Medium|Require same file plus overlap or within five lines; keep higher severity and retain merged guidance|Architect|
|R-006|Operator prompt scope misclassifies INFO-only runs|M2|Medium|Medium|Resolve OQ-008 and encode branch tests for zero, INFO-only, WARNING, and BLOCKING cases|Product owner|
|R-007|Remediation agent introduces new issues|M3|Medium|Medium|Constrain prompts, certify fixed findings, and leave full validate available to user|Backend lead|
|R-008|Cross-file findings cause conflicting edits|M3|Low|Medium|Assign one agent per file, include peer-agent note, and certify each finding after edits|Architect|
|R-009|User interruption leaves snapshots or partial edits|M3|Low|Low|Write state after completed boundaries; restore snapshots on caught failures; resume from gates|Backend lead|
|R-010|Retry and rollback order remains ambiguous|M3|Medium|High|Resolve OQ-004 before executor merge and encode tests for retry-before-rollback behavior|Product owner|
|R-011|Certification agent is too lenient|M4|Medium|Low|Use checklist prompts, per-finding justifications, strict result table, and allow full validate rerun|QA lead|
|R-012|Resume skips stale remediation output|M4|Low|High|Require SHA-256 source report hash match before skip to certify|Backend lead|
|R-013|Caveat state semantics conflict with success criteria|M4|Medium|Medium|Resolve OQ-006 and display explicit caveat state in report and state file|Product owner|
|R-014|Test coverage misses fallback parser paths|M5|Medium|High|Add merged, individual, malformed, empty, and duplicate-location fixtures|QA lead|
|R-015|Performance budget fails under large finding volume|M5|Medium|Medium|Batch by file, pass relevant snippets to certify, and report timing separately for Steps 10-11|Performance owner|
|R-016|Downstream tasklist integration expects fully certified state only|M5|Low|Medium|Block tasklist-ready flag unless certification semantics explicitly allow it|Architect|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|Milestone|
|---|---|---|---|---|
|SC-001|Completed pipeline steps|12/12 steps after remediation approval|Acceptance run of `roadmap run` with validation findings and selected remediation scope|M5|
|SC-002|BLOCKING certification pass rate|>=90% PASS among verified BLOCKING findings|Certification report assertion over BLOCKING rows|M5|
|SC-003|False certification passes|0|Negative fixture with intentionally unfixed finding must produce FAIL|M5|
|SC-004|Resume skip correctness|Matches §3.2 branch matrix|Resume tests for validate pass, remediate hash match, hash mismatch, and certify gate pass|M5|
|SC-005|Out-of-bound file edits|0|File tracker diff limited to `roadmap.md`, `extraction.md`, `test-strategy.md`|M5|
|SC-006|Step 10-11 overhead|<=30% of Steps 1-9 wall-clock|Instrument same-run timestamps and calculate `(t10+t11)/(t1_to_t9)`|M5|
|SC-007|Finding status representation|100% represented with correct final status|Compare parsed findings to `remediation-tasklist.md` rows and statuses|M5|
|SC-008|State compatibility|0 existing consumer failures|Backward-compatibility tests against pre-v2 state fixtures and additive v2 state|M5|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|---|---|---|---|
|Command surface|Extend default `roadmap run`|New `roadmap remediate` command; separate validation repair tool|Spec requires no new CLI command and default workflow integration improves operator flow|
|Execution split|Phase A via `execute_pipeline()` plus validation, Phase B prompt/remediate/certify|Single monolithic step list; interactive prompt inside `execute_pipeline()`|Keeps `execute_pipeline()` non-interactive and isolates prompt logic in `execute_roadmap()`|
|Agent orchestration|One `ClaudeProcess` per file group through `threading`|Per-finding agents; sequential single agent; new process abstraction|Batch-by-file prevents concurrent same-file edits while retaining parallelism and reusing approved process primitive|
|Failure semantics|Snapshot all targets and roll back all on final agent failure|Partial commit of successful file groups; manual cleanup only|All-or-nothing preserves artifact consistency for cross-file validation findings|
|Certification scope|Single lightweight checklist verifier over relevant sections|Full adversarial re-validation; no certification|Balances confidence and runtime budget while preserving user option to rerun full validate|
|Resume gating|Gate pass plus SHA-256 source report hash|Timestamp-only skip; always rerun remediate|Hash match prevents stale remediation reuse without forcing unnecessary repeated work|
|Tasklist boundary|Certified roadmap hands off to downstream `sc:tasklist`|Remediate downstream phase tasklists directly|Spec excludes tasklist-level remediation and keeps generated downstream work out of Step 10 scope|

## Timeline Estimates

|Milestone|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1|2 weeks|Week 1|Week 2|Contracts, model fields, gate definitions, state schema, step wiring boundaries|
|M2|2 weeks|Week 3|Week 4|Merged parser, fallback parser, dedup, terminal summary, severity scope planning|
|M3|3 weeks|Week 5|Week 7|Batch-by-file execution, constrained prompts, snapshots, rollback, tasklist writer|
|M4|2 weeks|Week 8|Week 9|Certification prompt/report, resume hash gates, lifecycle terminal states|
|M5|2 weeks|Week 10|Week 11|Acceptance tests, performance verification, compatibility checks, release readiness|

**Total estimated duration:** 11 weeks
