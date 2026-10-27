---
spec_source: "merged-requirements.compressed.md"
complexity_score: 0.85
complexity_class: HIGH
primary_persona: architect
adversarial: false
base_variant: "none"
variant_scores: "none"
convergence_score: null
---
# MultiModelSwarm — Project Roadmap

## Executive Summary

MultiModelSwarm delivers a Python-native `superclaude swarm` CLI that runs true-parallel multi-model jobs, normalizes worker outputs, emits durable state/contracts, and migrates `sc-bare-review` onto a thin CLI caller. The architecture centers on explicit contracts: Wave 0 preflight materializes a manifest and validates prompt-injection boundaries, Wave 1 dispatches through `ParallelExecutor`, Wave 2 normalizes with registered recipes, and Wave 3 determines status plus mechanical merge output without judging or reordering findings.

**Business Impact:** Enables reliable non-interactive swarm execution for Claude and non-Claude callers, reduces brittle shell orchestration, makes crash recovery auditable, and provides a reusable foundation for review, troubleshooting, spec analysis, and documentation completeness workflows.

**Complexity:** HIGH (0.85) — broad CLI surface, concurrency, atomic state, schema validation, prompt-injection controls, recipe/lens registries, detached execution, resume semantics, and skill migration all ship together.

**Critical path:** Freeze contracts and schema → implement atomic state/logging and true dispatch → implement recipe/reduce/merge boundaries → wire lenses and preflight guard parity → expose CLI/TUI/tmux surfaces → validate invariants and migrate `sc-bare-review`.

**Key architectural decisions:**

- Use Python-only ThreadPoolExecutor execution through `superclaude.execution.parallel.ParallelExecutor`; retire shell dispatch semantics.
- Make `manifest.json` the durable source of truth for resume; rehydrate `resolved_lens_entry` unless `--force-relens` is explicitly supplied.
- Keep `normalize+merge` mechanical only; `/sc:adversarial` remains the scored merge path.

**Open risks requiring resolution before M1:**

- Confirm open-question owners for hook policy, env-missing failure contract, and `caller_metadata.suspect` precedence before schema is finalized.

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|---|---|---|---|---|---|---|---|
|M1|Contract and module architecture|foundation|P0|XL|-|45|MEDIUM|
|M2|Dispatch, state, transport, observability|implementation|P0|XL|M1|26|HIGH|
|M3|Normalization, reduction, mechanical merge|implementation|P0|L|M1-M2|18|HIGH|
|M4|Lens registry, prompt guard, preflight resume|implementation|P0|XL|M1-M3|31|MEDIUM|
|M5|CLI, TUI, detached operator surface|implementation|P1|M|M2-M4|13|MEDIUM|
|M6|Invariant and integration validation|validation|P0|L|M1-M5|9|HIGH|
|M7|Skill migration and release packaging|migration|P1|M|M6|5|MEDIUM|
|M8|Operational rollout and documentation|release|P1|M|M7|6|MEDIUM|

## Dependency Graph

M1 → M2 → M3 → M4 → M5 → M6 → M7 → M8
M1 → M4; M2 → M5; M3 → M6; M4 → M6; M6 → M8

## M1: Contract and Module Architecture

**Objective:** Freeze schema, architectural constraints, core data models, and module boundaries before implementation | **Duration:** Week 1 (1 week) | **Entry:** Extraction approved; owners assigned | **Exit:** Job/result/state contracts reviewed; swarm module package created under `src/superclaude/cli/swarm/`; schema decisions captured

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|AC-001|Python and UV runtime rule|Enforce Python ≥3.10 and UV-only development workflow.|project|-|python>=3.10; uv_only:true; no_direct_pip:true; no_bare_python:true|S|P0|
|2|AC-002|Top-level swarm CLI verb|Create `superclaude swarm` as a new CLI verb under swarm package, not sprint or roadmap.|cli|-|verb:superclaude_swarm; path:src/superclaude/cli/swarm; not_child_of:sprint_roadmap|M|P0|
|3|AC-003|Sprint-shaped module layout|Mirror sprint module organization for operator familiarity.|architecture|-|mirror:src/superclaude/cli/sprint; package:src/superclaude/cli/swarm|M|P0|
|4|AC-004|ParallelExecutor invocation rule|Require ThreadPoolExecutor access through existing parallel abstraction.|dispatch|-|executor:superclaude.execution.parallel.ParallelExecutor; direct_threadpool:false|M|P0|
|5|AC-005|httpx transport library|Use httpx for Phase-1 openai-compatible transport.|transport|-|library:httpx; phase:1; scope:reference_transport|S|P1|
|6|AC-006|Click CLI dependency|Use Click ≥8.0.0 for group and subcommands.|cli|-|library:click>=8.0.0; surfaces:group+subcommands|S|P1|
|7|AC-007|Rich opt-in dashboard|Use Rich ≥13.0.0 only behind `--tui`; non-TTY stays plain.|tui|-|library:rich>=13.0.0; flag:--tui; default:false|S|P1|
|8|AC-008|Optional tmux dependency|Require tmux only for detached mode; inline remains default.|tmux|-|binary:tmux; required_when:--detached; default:inline|S|P1|
|9|AC-009|Future-integration boundary|Exclude openharness, openhands, Assistants SDK, LangGraph, CrewAI while keeping APIs non-precluding.|architecture|-|excluded:openharness+openhands+assistants+langgraph+crewai; future_non_precluding:true|S|P1|
|10|AC-010|No Anthropic routing|Prevent swarm transport from routing to Anthropic models in Phase 1.|transport|-|anthropic_routing:false; phase:1|S|P0|
|11|AC-011|No judging transforms|Forbid scoring, deduplication, reordering, rewriting, or filtering worker findings.|merge|-|scoring:false; dedupe:false; reorder:false; rewrite:false; filter:false|M|P0|
|12|AC-012|No new scored merge engine|Keep scored merge responsibility with `/sc:adversarial`; swarm merge stays mechanical.|merge|-|new_scored_engine:false; scored_owner:/sc:adversarial|S|P0|
|13|AC-013|Provider-neutral contract surface|Keep job spec, result contract, CLI, and monitoring names free of Claude-specific tool names.|contracts|-|job_spec:provider_neutral; result_contract:provider_neutral; cli:provider_neutral; monitoring:provider_neutral|S|P0|
|14|AC-014|Output directory boundary|Prevent writes outside configured output directory.|state|-|write_root:--output; outside_writes:false|M|P0|
|15|AC-015|No cross-run response cache|Avoid response caching across invocations.|dispatch|-|cross_invocation_cache:false|S|P1|
|16|AC-016|Phase-1 modality limits|Exclude streaming, function-calling, and vision input in Phase 1.|transport|-|streaming:false; function_calling:false; vision:false; phase:1|S|P1|
|17|AC-017|T2 proxy environment contract|Use T2 proxy env vars for model endpoint discovery.|transport|-|base_url_env:T2ProxyUrl; api_key_env:T2ProxyKey; model_env:T2Model0N|M|P0|
|18|AC-018|Mechanical merge LOC ceiling|Keep merge module body within ≤30 LOC excluding imports and docstring.|merge|-|file:swarm/merge.py; body_loc<=30; exclusions:imports+docstring|S|P0|
|19|AC-019|Source-of-truth edit discipline|Edit `src/superclaude/` first, sync dev copies after.|release|-|source:src/superclaude; sync:make_sync_dev; direct_dot_claude_edits:false|S|P0|
|20|DM-001|JobSpec model|Define top-level job specification dataclass/schema object.|models|-|spec_version; job_id; created; caller; lens; custom_prompt_dir; workers; transport; prompt; target; normalization; output; amalgamation_mode; status_policy; recommended_next_command_template; recommended_next_command_substitutions; runtime|L|P0|
|21|DM-002|WorkerSpec model|Define worker count, models, timeout, temperature, and retry policy.|models|DM-001|count; models; timeout_sec; temperature; retry.on_5xx; retry.on_5xx_backoff_sec; retry.on_4xx; retry.on_timeout|M|P0|
|22|DM-003|TargetSpec model|Define target ingestion, truncation, delimiters, and injection guard.|models|DM-001|kind; path; truncation.line_cap; truncation.byte_floor; delimiters.open; delimiters.close; injection_guard.enabled; injection_guard.required_substring|M|P0|
|23|DM-004|TransportSpec model|Define transport endpoint env resolution.|models|DM-001|kind; base_url_env; api_key_env|S|P0|
|24|DM-005|PromptSpec model|Define prompt fields and variable expansion contract.|models|DM-001|system; user_template; variables|M|P0|
|25|DM-006|NormalizationSpec model|Define recipe, template, version, args, and parse-error handling.|models|DM-001|recipe; template_path; schema_version; recipe_args; on_parse_error.salvage; on_parse_error.retain_raw|M|P0|
|26|DM-007|OutputSpec model|Define output directory, file naming, atomicity, and meta sidecar emission.|models|DM-001|dir; filename_template; lens_name; atomic_write; emit_meta_sidecar|M|P0|
|27|DM-008|StatusPolicy model|Define success/partial/failure thresholds.|models|DM-001|floor; success_first; partial_threshold|S|P0|
|28|DM-009|RuntimeSpec model|Define inline/detached runtime and completion behavior.|models|DM-001|mode; log_level; on_completion.write_done_sentinel; on_completion.print_contract_to_stdout|S|P1|
|29|DM-010|LensEntry model|Define registry entry shape for bundled lenses.|lenses|DM-001|name; description; system_prompt_fragment; user_template; output_template_path; recipe_name; default_workers; default_target_line_cap; suspect; tier; recommended_next_command_template; acceptance_notes; stability|L|P0|
|30|DM-011|ResolvedLensEntry model|Define manifest lens snapshot shape.|manifest|DM-010|name; system_prompt_fragment; user_template; recipe_name; default_workers; suspect; tier; recommended_next_command_template; stability|M|P0|
|31|DM-012|ResultContract model|Define final job result contract emitted to callers.|contracts|DM-001|contract_version; status; job_id; started; finished; elapsed_ms; caller; lens; lens_source; target.path; target.checksum; target.truncated; target.truncation_line_cap; workers_requested; workers_succeeded; workers_failed; output_files[]; amalgamation_mode; merged_path; caller_metadata; recommended_next_command; artifacts|L|P0|
|32|DM-013|WorkerResult model|Define per-worker result metadata for contracts.|contracts|DM-012|index; path; raw_path; meta_path; model_id; model_label; bytes; status; http_code; attempts; elapsed_ms|M|P0|
|33|DM-014|SwarmState model|Define persistent state machine values.|state|DM-001|state:preflight_ok/dispatching/normalizing/reducing/terminal|S|P0|
|34|DM-015|EventRecord model|Define JSONL event entry shape.|logging|DM-013|event_type; timestamp; worker_index; payload|S|P0|
|35|DM-016|Manifest model|Define preflight manifest artifact with durable lens snapshot.|manifest|DM-011|contract_version; job_id; resolved_lens_entry; extension_fields:preserved|M|P0|
|36|DM-017|DoneSentinel model|Define terminal marker artifact for monitoring.|state|DM-012|file:done.json; atomic_write:true; terminal_indicator:true|S|P1|
|37|DM-018|Artifacts model|Define path bundle included in result contract.|contracts|DM-012|manifest_path; state_path; event_log_jsonl; event_log_md; done_sentinel|S|P0|
|38|DM-019|CallerInfo model|Define caller identity metadata supplied by invocation.|contracts|DM-001|skill; skill_version; invocation_label; kind|S|P1|
|39|DM-020|CallerMetadata model|Define lens/caller output metadata.|contracts|DM-012|suspect; tier|S|P1|
|40|COMP-001|swarm package entry point|Create swarm package entry point exporting CLI group.|cli|-|file:cli/swarm/__init__.py; role:click_group_entry; deps:commands|S|P0|
|41|COMP-002|commands module outline|Define command module boundaries for run/status/logs/attach/kill/starter-spec/validate/validate-lenses.|cli|COMP-001|file:cli/swarm/commands.py; role:click_subcommands; deps:preflight+dispatch+normalize+reduce+state+tmux|M|P0|
|42|COMP-003|SwarmConfig module|Define configuration dataclass and path resolution behavior.|config|DM-001|file:cli/swarm/config.py; role:configuration_dataclass; deps:none|S|P0|
|43|COMP-004|models module|Create dataclass home for job, worker, result, state, and event records.|models|DM-001|file:cli/swarm/models.py; role:dataclasses; deps:none|M|P0|
|44|COMP-005|schema module|Create JSON Schema validator and cross-field rule home.|schema|DM-001|file:cli/swarm/schema.py; role:json_schema+cross_field_validators; deps:models|L|P0|
|45|COMP-006|preflight module boundary|Create Wave 0 module boundary for schema, lens materialization, prompt guard parity, and manifest preparation.|preflight|COMP-005|file:cli/swarm/preflight.py; role:wave0_lens_resolution+materialization; deps:schema+lenses+models+state|L|P0|

### Integration Points — M1

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`superclaude swarm` Click group|CLI registry|Yes: command group exported from package entry point|M1|M5 command handlers|
|JobSpec ↔ JSON Schema|contract validator|Yes: dataclass fields mapped to schema properties|M1|M2-M5 preflight and CLI validation|
|ResultContract ↔ Artifacts|contract composition|Yes: artifact paths embedded in contract model|M1|M2 state/log writers; M8 operators|
|LensEntry ↔ ResolvedLensEntry|snapshot mapping|Yes: manifest snapshot defined verbatim|M1|M4 resume and `--force-relens` logic|
|StatusPolicy ↔ reduce|strategy config|Yes: floor/success_first/partial_threshold modeled|M1|M3 status reducer|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Schema decisions drift after implementation begins|MEDIUM|MEDIUM|Rework across dispatch, preflight, and contract writers|Freeze M1 contracts; require migration notes for post-M1 field changes|Architect|
|2|Output boundary and caller metadata rules remain ambiguous|MEDIUM|MEDIUM|Security bugs or incompatible result contracts|Resolve OQ-006/OQ-008/OQ-009 before M1 exit|Architect+Security|

### Milestone Dependencies — M1

- Requires extraction document approval and explicit acceptance of Phase-1 exclusions.

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-006|Should concurrent use of the same `--output` dir STOP or remain caller-must-avoid for v1?|Controls state safety contract and schema defaults|Architect|M1 exit|
|2|OQ-008|For empty T2 model/env pool, should the run write `failed`/`env-missing` contract when output dir is creatable?|Controls failure contract and preflight behavior|Architect+DevOps|M1 exit|
|3|OQ-009|Can caller metadata override lens `suspect`, and what is precedence?|Controls ResultContract semantics and next-command templates|Architect|M1 exit|
|4|OQ-010|Should `validate-lenses` failure be blocking in CI or warning-only?|Controls validator exit codes and release gates|Architect+QA|M1 exit|

## M2: Dispatch, State, Transport, Observability

**Objective:** Implement true dispatch, atomic state/log artifacts, T2 transport, deterministic test transport, and terminal contract emission | **Duration:** Weeks 2-3 (2 weeks) | **Entry:** M1 contracts frozen | **Exit:** Inline run writes manifest/state/logs/worker outputs/return contract/done sentinel atomically; dispatch proves concurrent worker execution

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|IMM-3|True-parallel dispatch|Run one parallel group with N workers through Python ThreadPoolExecutor semantics.|dispatch|AC-004,COMP-007|N workers start concurrently; one ParallelGroup used; attention-mediated dispatch absent; tested with elapsed overlap|L|P0|
|2|IMM-4|Empty target guard|Stop before dispatch when truncated target has fewer than 50 non-whitespace bytes.|preflight|DM-003|byte_floor:50; terminal_status:failed; reason:target-too-small; dispatch_called:false; contract_written:true|M|P0|
|3|IMM-6|Atomic output writes|Write every state/output artifact by temp file plus `os.replace` and deterministic names.|state|DM-007|write_tmp:true; os_replace:true; deterministic_filename:true; partial_files_absent_on_kill|L|P0|
|4|INV-002|Python-only concurrency|Retire shell dispatch and PIPE_BUF assumptions; Python owns dispatch end-to-end.|dispatch|IMM-3|shell_dispatch:false; ThreadPoolExecutor_via_ParallelExecutor:true; PIPE_BUF_dependency:false|M|P0|
|5|FR-001|Run subcommand|Execute swarm job from spec file, stdin, or lens shortcut.|cli|COMP-002,COMP-007|inputs:spec_file/stdin/lens; emits:return-contract.yaml; supports:inline_default|L|P0|
|6|FR-017|Worker timeout and retry policy|Apply per-worker timeout and HTTP retry rules while recording every outcome.|dispatch|COMP-007,DM-002|timeout_default:180s; 5xx_retry_once:true; 5xx_backoff:true; 4xx_retry:false; timeout_retry:false; network_retry:false; outcome_recorded:true|L|P0|
|7|FR-018|Result contract emission|Emit `return-contract.yaml` with job, worker, output, metadata, command, and artifact fields.|contracts|DM-012,DM-013,DM-018|status; job_id; lens; amalgamation_mode; output_files.index/path/model_id/status/http_code/attempts; merged_path; caller_metadata; recommended_next_command; artifacts|L|P0|
|8|FR-022|OpenAI-compatible transport|Implement httpx-based Phase-1 transport for T2 proxy endpoint.|transport|AC-005,AC-017,COMP-032|library:httpx; reads:T2ProxyUrl/T2ProxyKey/T2Model0N; records:http_code; provider_neutral_contract:true|L|P0|
|9|FR-023|Deterministic test transport|Provide deterministic transport for tests without external network dependency.|transport|COMP-033|deterministic_outputs:true; external_network:false; worker_index_visible:true; error_modes_configurable:true|M|P0|
|10|FR-026|Dual-format logs|Emit append-only JSONL plus human-readable Markdown execution logs.|logging|COMP-012,DM-015|execution-log.jsonl:append_only+locked; execution-log.md:human_log; both_under_output:true|M|P0|
|11|FR-027|Done sentinel|Emit `done.json` via atomic write on terminal state.|state|DM-017|terminal_only:true; atomic_write:true; status_included:true; contract_path_included:true|S|P1|
|12|FR-030|Non-Claude caller compatibility|Support subprocess invocation from any language against provider-neutral CLI and contracts.|cli|AC-013,FR-001|subprocess.run_works:true; detached_spec_path_supported:true; contract_identical_to_claude_invocation:true|M|P1|
|13|NFR-001|ParallelExecutor-only concurrency|Route ThreadPoolExecutor execution through existing internal parallel executor.|dispatch|AC-004|direct_threadpool:false; ParallelExecutor_used:true; test_asserts_import_path:true|M|P0|
|14|NFR-002|Atomicity and locked appends|Use atomic state transitions and lock-coordinated JSONL appends.|state|IMM-6,COMP-012|state_tmp_replace:true; jsonl_lock:threading.Lock; torn_write_test:true|L|P0|
|15|NFR-004|Durable monitoring layers|Maintain state file, JSONL log, Markdown log, and done sentinel.|observability|FR-026,FR-027|.swarm-state.json; execution-log.jsonl; execution-log.md; done.json|M|P0|
|16|NFR-010|Worker hard timeout|Make 180s timeout default and configurable through worker spec.|dispatch|DM-002,FR-017|default:180s; config:workers.timeout_sec; timeout_status_recorded:true|S|P0|
|17|NFR-011|Retry semantics|Apply exactly one 5xx retry and zero retries for 4xx/timeout/network outcomes.|dispatch|FR-017|5xx_attempts_max:2; 4xx_attempts_max:1; timeout_attempts_max:1; network_attempts_max:1|M|P0|
|18|NFR-013|Filesystem write boundary|Ensure all generated artifacts are under `--output`.|state|AC-014|path_resolve_check:true; outside_output_rejected:true; symlink_escape_rejected:true|M|P0|
|19|NFR-014|No cross-invocation response caching|Prevent workers from reusing responses across runs.|dispatch|AC-015|cache_between_runs:false; response_replay:false; run_id_separates_artifacts:true|S|P1|
|20|NFR-016|Provider-neutral contract surface|Keep contracts/CLI/monitoring free of Claude tool names and survive caller death in detached mode.|contracts|AC-013|job_spec_neutral:true; result_contract_neutral:true; cli_neutral:true; monitoring_neutral:true; detached_survives_caller:true|M|P1|
|21|COMP-007|dispatch module|Implement Wave 1 dispatch with transports, state updates, logs, and ParallelExecutor.|dispatch|COMP-006|file:cli/swarm/dispatch.py; role:wave1_httpx_threadpool; deps:transports+state+logging_+ParallelExecutor|L|P0|
|22|COMP-011|state module|Implement atomic `.swarm-state.json` read/write helpers.|state|DM-014|file:cli/swarm/state.py; role:atomic_state_read_write; deps:none|M|P0|
|23|COMP-012|logging module|Implement lock-coordinated JSONL and Markdown event logs.|logging|DM-015|file:cli/swarm/logging_.py; role:dual_event_log; deps:none|M|P0|
|24|COMP-031|Transport Protocol|Define transport interface used by dispatch.|transport|COMP-007|file:cli/swarm/transports/__init__.py; role:protocol_interface; deps:none|M|P0|
|25|COMP-032|openai_compat transport|Implement httpx T2 proxy transport behind protocol interface.|transport|COMP-031|file:cli/swarm/transports/openai_compat.py; role:httpx_reference_transport; deps:httpx|L|P0|
|26|COMP-033|deterministic test transport|Implement deterministic transport for unit and integration tests.|transport|COMP-031|file:cli/swarm/transports/deterministic.py; role:deterministic_test_transport; deps:none|M|P0|

### Integration Points — M2

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|dispatch → ParallelExecutor|dependency injection|Yes: dispatch delegates worker fan-out to ParallelExecutor|M2|M6 concurrency tests|
|dispatch → Transport Protocol|strategy pattern|Yes: transport selected by `transport.kind`|M2|openai_compat and deterministic tests|
|dispatch → logging_|event binding|Yes: worker_start/progress/done events written through lock-coordinated logger|M2|status/logs/watch surfaces|
|state → return contract|artifact wiring|Yes: terminal state and output paths feed contract emission|M2|M5 CLI; M8 operations|
|done.json → monitoring|sentinel binding|Yes: terminal completion writes done sentinel atomically|M2|Monitor and background wait patterns|

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|ThreadPoolExecutor surprise: developers may not expect threading behavior|LOW|MEDIUM|Race-prone state/log writes|Document dispatch threading; protect JSONL appends with `threading.Lock`; prove with deterministic transport|Backend Lead|
|2|Partial artifact writes under crashes|HIGH|MEDIUM|Corrupt resume state or misleading contracts|Use temp+replace for every artifact; add mid-write termination test in M6|Backend Lead|
|3|T2 env misconfiguration blocks dispatch|MEDIUM|MEDIUM|Runs fail before worker output|Resolve OQ-008; emit structured env-missing failure when output dir is creatable|DevOps|

### Milestone Dependencies — M2

- M1 model and schema fields must be frozen before state and contract writers are implemented.

## M3: Normalization, Reduction, Mechanical Merge

**Objective:** Implement recipe protocol, normalizers, status reduction, parse salvage, and strictly mechanical merge | **Duration:** Week 4 (1 week) | **Entry:** M2 worker outputs and contracts available | **Exit:** Raw/normalize/normalize+merge modes work; status policy matches IMM-5; merge boundary guards are enforced

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|IMM-5|Success-first status policy|Determine success/partial/failed using M/N counts with configurable floor and success-first semantics.|reduce|DM-008|M==N:success; 2<=M<N:partial; M<2:failed; M==N==2:success; floor_default:2; success_first_default:true|M|P0|
|2|INV-010|Resume merge regeneration|Regenerate `merged.md` after redispatched workers finish when mode is normalize+merge.|reduce|FR-015,COMP-009|resume_wave3_runs:true; mode:normalize+merge; stale_merge_prevented:true; provenance_truthful:true|M|P0|
|3|FR-010|Recipe protocol registry|Implement recipe registry with six normalizers and dynamic custom-py loader.|recipes|COMP-015|recipes:bare_review_v1/findings_table_v1/hypothesis_table_v1/verdict_only_v1/passthrough/custom-py; registry_lookup:true|L|P0|
|4|FR-011|Amalgamation modes|Support raw, normalize, and normalize+merge modes.|normalize|COMP-008,COMP-010|raw:pass-through; normalize:recipe_per_worker; normalize+merge:recipe_then_concat; default:normalize|M|P0|
|5|FR-012|Mechanical merge module|Implement merge module with four structural guards and no judging behavior.|merge|AC-011,AC-018|docstring_allowed_disallowed_ops:true; body_loc<=30; pr_review_boundary_note:true; boundary_test:true|M|P0|
|6|FR-028|Parse-error salvage promotion|Promote parse_error to success when salvage succeeds in Wave 2.|normalize|COMP-008|parse_error_salvage:true; promoted_status:success; raw_retained_when_configured:true|M|P0|
|7|NFR-008|Merge module boundary size|Keep `swarm/merge.py` body ≤30 LOC excluding imports/docstring.|merge|FR-012|body_loc<=30; imports_excluded:true; docstring_excluded:true|S|P0|
|8|NFR-009|Mechanical boundary enforcement|Test three-worker concat order and transformations; CI flags changes to boundary test.|merge|FR-012|slot_order_preserved:true; sections:3; transformations:none_beyond_provenance_header; ci_flags_test_changes:true|M|P0|
|9|COMP-008|normalize module|Implement Wave 2 dispatcher and recipe registry invocation.|normalize|COMP-015|file:cli/swarm/normalize.py; role:wave2_recipe_dispatch; deps:recipes|L|P0|
|10|COMP-009|reduce module|Implement Wave 3 status determination and resume merge regeneration.|reduce|COMP-010|file:cli/swarm/reduce.py; role:status_policy+merge_regen; deps:merge+models|M|P0|
|11|COMP-010|merge module|Implement mechanical concatenation only.|merge|AC-018|file:cli/swarm/merge.py; role:mechanical_concat; deps:none|M|P0|
|12|COMP-015|Recipe Protocol module|Define protocol, registry dict, and custom-py loader integration point.|recipes|COMP-008|file:cli/swarm/recipes/__init__.py; role:protocol+REGISTRY+custom_loader; deps:none|M|P0|
|13|COMP-016|bare_review_v1 recipe|Port bare-review normalization logic into recipe module.|recipes|COMP-015|file:cli/swarm/recipes/bare_review_v1.py; role:bare_review_normalizer; output_shape:bare_review_template|M|P0|
|14|COMP-017|findings_table_v1 recipe|Normalize findings-table lenses.|recipes|COMP-015|file:cli/swarm/recipes/findings_table_v1.py; role:findings_table_normalizer|S|P1|
|15|COMP-018|hypothesis_table_v1 recipe|Normalize troubleshooting hypothesis tables.|recipes|COMP-015|file:cli/swarm/recipes/hypothesis_table_v1.py; role:hypothesis_table_normalizer|S|P1|
|16|COMP-019|verdict_only_v1 recipe|Normalize verdict-only outputs.|recipes|COMP-015|file:cli/swarm/recipes/verdict_only_v1.py; role:verdict_only_normalizer|S|P1|
|17|COMP-020|passthrough recipe|Implement pass-through normalizer for raw-compatible shape.|recipes|COMP-015|file:cli/swarm/recipes/passthrough.py; role:pass-through_normalizer|S|P1|
|18|COMP-021|custom-py recipe loader|Implement dynamic `custom-py:module:func` loader with validation.|recipes|COMP-015|file:cli/swarm/recipes/custom.py; role:dynamic_custom-py_loader|M|P1|

### Integration Points — M3

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Recipe REGISTRY|dispatch table|Yes: recipe_name resolves to normalizer function|M3|normalize Wave 2; lens validator|
|NormalizationSpec → recipes|strategy pattern|Yes: `normalization.recipe` selects registered recipe|M3|M4 lens defaults|
|reduce → merge|stage wiring|Yes: normalize+merge invokes mechanical concat after status inputs are known|M3|return contract merged_path|
|parse salvage → WorkerResult|status promotion|Yes: salvage result updates per-worker status before reduction|M3|IMM-5 status policy|
|custom-py loader|dynamic loader|Yes: loader validates module/function reference before invocation|M3|custom lens callers|

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Merge boundary erosion: normalize+merge drifts into judging|HIGH|MEDIUM|Swarm duplicates `/sc:adversarial` and corrupts provenance|Enforce ≤30 LOC, explicit allowed/disallowed docstring, boundary test, and PR review note|Architect|
|2|Normalizer output shapes diverge from lens templates|MEDIUM|MEDIUM|Downstream commands receive malformed tables|Validate recipe/template alignment in M4 registry validator and M6 tests|Backend Lead|

### Milestone Dependencies — M3

- M2 must provide stable worker result paths and statuses for normalization inputs.

## M4: Lens Registry, Prompt Guard, Preflight Resume

**Objective:** Implement lens registry, prompt-input guard parity, schema/preflight materialization, manifest resume semantics, and bundled templates | **Duration:** Week 5 (1 week) | **Entry:** M1-M3 contracts, dispatch, and recipes available | **Exit:** All bundled lenses validate; custom-prompt-dir has identical guard enforcement; resume uses manifest snapshot by default

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|§11.5|Prompt-injection guard|Delimit target content and require data-vs-instructions sentence across all prompt paths.|preflight|DM-003,DM-005|delimiters.open:<<<TARGET>>>; delimiters.close:<<<END TARGET>>>; required_substring_present:true; paths:lens_registry/json_schema/custom_prompt_dir|L|P0|
|2|INV-001|Manifest lens rehydration|Resume uses `manifest.resolved_lens_entry` verbatim unless force relens is supplied.|preflight|DM-011,DM-016|resume_re_resolve_default:false; manifest_snapshot_used:true; --force-relens_overrides:true|M|P0|
|3|INV-003|Custom prompt guard parity|Apply required-substring check to custom-prompt-dir exactly like lens and schema paths.|preflight|§11.5,FR-021|custom_prompt_dir_check:true; lens_path_check:true; schema_path_check:true; identical_rule:true|M|P0|
|4|INV-014|Escape-hatch isomorphism|Keep custom-prompt-dir behavior isomorphic to lens-driven guard enforcement.|preflight|INV-003|escape_hatch_guard_same:true; auto_inject_explicit_only:true|S|P0|
|5|INV-016|Manifest source of truth|Treat manifest as durable definition of intended swarm behavior.|manifest|DM-016|resume_honors_manifest:true; lens_mutation_ignored:true; resolved_lens_entry_verbatim:true|M|P0|
|6|U-008|Lens registry validator|Validate registry refs, recipe names, suspect coupling, uniqueness, and prompt guard substring.|lenses|COMP-023|file_refs_resolve:true; recipe_registered:true; suspect_requires_suspect_files:true; names_unique:true; system_prompt_fragment_has_guard:true|M|P0|
|7|FR-008|Validate-lenses subcommand|Expose bundled lens registry validation through CLI.|cli|U-008,COMP-002|command:swarm_validate-lenses; validates:bundled_registry; exit_mode:per_OQ-010|S|P0|
|8|FR-009|Initial lens registry|Ship eight initial lens entries for review, refactor, edge-case, spec, feasibility, troubleshooting, docs, and custom usage.|lenses|DM-010,COMP-022|entries:bare-review/refactor-find/edge-case-hunt/spec-completeness/feasibility-probe/troubleshoot-hypothesis/doc-completeness/custom; path:cli/swarm/lenses|L|P0|
|9|FR-016|Manifest emission|Emit manifest with resolved lens snapshot captured during Wave 0.|manifest|INV-016,DM-016|resolved_lens_entry_fields:system_prompt_fragment/user_template/recipe_name/defaults/suspect/tier/stability; emitted_in_wave0:true|M|P0|
|10|FR-019|Job spec schema validation|Validate job specs with JSON Schema and cross-field prompt guard rules.|schema|COMP-005,§11.5|json_schema:true; cross_field_rules:true; prompt.system_required_substring:true; spec_version_checked:true|L|P0|
|11|FR-020|Lens defaults expansion|Expand lens field into prompt, normalization, worker, target, output, recommendation, and metadata defaults.|preflight|FR-009,DM-010|expands:prompt.system/prompt.user_template/normalization.recipe/normalization.template_path/workers.count/target.truncation.line_cap/output.filename_template/lens_name/recommended_next_command_template/caller_metadata.suspect/caller_metadata.tier|L|P0|
|12|FR-021|Custom-prompt-dir path|Read custom prompt directory files when lens is custom and flag is supplied.|preflight|INV-003|requires:lens==custom; files:system.txt/user.txt/meta.yaml; guard_enforced:true|M|P1|
|13|FR-024|Auto-inject guard flag|Provide opt-in backward-compat flag that prepends canonical guard sentence for custom prompts.|preflight|FR-021|flag:--auto-inject-guard; scope:custom_prompt_dir; default:false; inserted_sentence:canonical_guard|S|P1|
|14|FR-025|Force relens flag|Allow resume to ignore manifest lens snapshot and re-resolve from current registry.|preflight|INV-001|flag:--force-relens; default:false; current_registry_used_when_true:true|S|P1|
|15|NFR-003|Prompt injection security|Enforce delimiters and required-substring preflight across all three prompt-input paths.|security|§11.5|delimiters:true; required_substring:true; paths:3; dispatch_blocked_on_violation:true|M|P0|
|16|NFR-005|Crash recovery source of truth|Resume from manifest, skip successful workers, and regenerate merge on resume.|resume|INV-016,INV-010|manifest_source:true; worker_skip_success:true; merge_regen:true|M|P0|
|17|NFR-006|Schema forward compatibility|Load spec 1.0 with orchestrator 1.1 on a best-effort basis.|schema|FR-019|orchestrator:1.1; loads_spec:1.0; unknown_fields_policy:documented|S|P1|
|18|NFR-012|Lens registry PR discipline|Require real caller, guard substring, recipe/template alignment, downstream command, and suspect scrutiny for new lenses.|lenses|U-008|real_caller_required:true; guard_required:true; recipe_template_alignment:true; downstream_command_reference:true; suspect_extra_review:true|S|P1|
|19|COMP-022|LENSES registry helpers|Implement registry dict, LensEntry dataclass, and lookup helpers.|lenses|DM-010|file:cli/swarm/lenses/__init__.py; role:registry+LensEntry+helpers; deps:none|M|P0|
|20|COMP-023|Lens validator module|Implement registry validator rules.|lenses|U-008|file:cli/swarm/lenses/_validate.py; role:file_refs+recipe_resolution+suspect_coupling+name_uniqueness+guard_substring; deps:recipes|M|P0|
|21|COMP-024|bare_review lens|Define stable T2 bare-review lens with suspect metadata and three workers.|lenses|COMP-022|file:cli/swarm/lenses/bare_review.py; role:native_instinct_review; suspect:true; tier:T2; workers:3; stability:stable|M|P0|
|22|COMP-025|refactor_find lens|Define experimental cleanup lens for correctness, readability, and efficiency.|lenses|COMP-022|file:cli/swarm/lenses/refactor_find.py; role:cleanup_findings; tier:T2-code; workers:3; stability:experimental|S|P1|
|23|COMP-026|edge_case_hunt lens|Define experimental edge-case discovery lens.|lenses|COMP-022|file:cli/swarm/lenses/edge_case_hunt.py; role:edge_case_discovery; tier:T2-edge; workers:4; stability:experimental|S|P1|
|24|COMP-027|spec_completeness lens|Define experimental specification completeness lens.|lenses|COMP-022|file:cli/swarm/lenses/spec_completeness.py; role:spec_gap_discovery; tier:T2-spec; workers:3; stability:experimental|S|P1|
|25|COMP-028|feasibility_probe lens|Define experimental feasibility review lens.|lenses|COMP-022|file:cli/swarm/lenses/feasibility_probe.py; role:approach_feasibility; tier:T2-feas; workers:3; stability:experimental|S|P1|
|26|COMP-029|troubleshoot_hypothesis lens|Define experimental troubleshooting root-cause lens.|lenses|COMP-022|file:cli/swarm/lenses/troubleshoot_hypothesis.py; role:root_cause_hypothesis; tier:T2-tshoot; workers:4; stability:experimental|S|P1|
|27|COMP-030|doc_completeness lens|Define experimental documentation completeness lens.|lenses|COMP-022|file:cli/swarm/lenses/doc_completeness.py; role:doc_gap_discovery; tier:T2-doc; workers:3; stability:experimental|S|P1|
|28|COMP-034|Bare-review output template|Provide compressed Markdown findings table template for bare-review output.|templates|COMP-016,COMP-024|file:refs/templates/bare-review-output.md; role:bare_review_output_shape|S|P0|
|29|COMP-035|Per-lens output templates|Provide lens-specific output templates for bundled lenses.|templates|COMP-022|file:refs/templates/<lens>-output.md; role:lens_specific_output_shapes|M|P1|
|30|INV-005|Worker count vs model pool guard|Validate workers requested against configured T2 model pool with v1 warning/STOP behavior resolved by owner.|preflight|DM-002,OQ-007|checks:T2Model0N_count; workers_exceed_pool_handled:true; severity:per_OQ-007; contract_or_warning_documented:true|M|P0|
|31|INV-007|Empty model pool failure path|Handle missing configured T2 models with structured failure when output dir can be created.|preflight|AC-017,OQ-008|empty_pool_detected:true; reason:env-missing; contract_written_when_output_creatable:true; pre_output_abort_when_not_creatable:true|M|P0|

### Integration Points — M4

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|LENSES registry|registry|Yes: lens name resolves to LensEntry|M4|preflight defaults expansion; validate-lenses|
|LensEntry → NormalizationSpec|strategy wiring|Yes: `recipe_name` maps to recipe registry entry|M4|Wave 2 normalize|
|LensEntry → prompt guard|validation hook|Yes: `system_prompt_fragment` must contain required substring|M4|preflight; registry validator|
|custom-prompt-dir → PromptSpec|escape-hatch wiring|Yes: system/user/meta files materialize PromptSpec with same guard rule|M4|custom lens runs|
|manifest → resume|state rehydration|Yes: resume uses `resolved_lens_entry` snapshot by default|M4|resume run flow|
|`--force-relens` → registry|explicit override|Yes: flag re-resolves from current LENSES only when supplied|M4|operator resume choices|

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Lens-registry sprawl: every new lens ships built-in entry|MEDIUM|MEDIUM|Registry bloats and weakens review discipline|Require real caller and downstream command reference; route one-off needs through custom prompts|Architect|
|2|Resume and lens mutation interaction|MEDIUM|MEDIUM|Resumed jobs change behavior unexpectedly|Use manifest lens snapshot by default; require explicit `--force-relens`; test both paths|Backend Lead|
|3|Custom prompt guard parity breaks for existing users|MEDIUM|MEDIUM|Prompt injection guard bypass or migration friction|Apply identical preflight rule; provide opt-in auto-inject flag|Security|

### Milestone Dependencies — M4

- M3 recipe registry must exist so lens validation can verify recipe names.
- M1 open questions OQ-008/OQ-009/OQ-010 must be resolved before final schema behavior is locked.

### Open Questions — M4

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-001|Should `validate-lenses` run as a pre-commit hook by default?|Controls release gate automation and contributor workflow|Architect+QA|M4 exit|
|2|OQ-002|Should lenses support explicit version pinning such as `--lens-version v2`?|Controls registry schema growth and resume compatibility|Architect|M4 exit|
|3|OQ-005|Should one swarm allow per-model overrides such as per-model temperature?|Controls WorkerSpec expansion and lens defaults|Architect|M4 exit|
|4|OQ-007|When workers exceed configured T2 models, should v1 warn or STOP?|Controls preflight validation severity|Architect+DevOps|M4 exit|

## M5: CLI, TUI, Detached Operator Surface

**Objective:** Expose operator-facing subcommands, watch/log/status patterns, opt-in TUI, detached tmux execution, and resume/kill/attach lifecycle | **Duration:** Week 6 (1 week) | **Entry:** M2-M4 runtime paths implemented | **Exit:** All CLI commands validate arguments, write/read contracts, avoid terminal control sequences by default, and support detached job lifecycle

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|INV-012|Opt-in TUI|Keep TUI behind `--tui`; non-TTY callers receive plain output only.|tui|AC-007,COMP-013|flag:--tui; default:false; non_tty_control_sequences:false|M|P0|
|2|FR-002|Status subcommand|Show terminal or in-flight job state from durable artifacts.|cli|COMP-002,COMP-011|command:swarm_status; reads:.swarm-state.json; terminal_status_visible:true; in_flight_status_visible:true|M|P0|
|3|FR-003|Logs subcommand|Tail or dump job execution logs.|cli|COMP-002,COMP-012|command:swarm_logs; modes:tail/dump; sources:execution-log.jsonl+execution-log.md|M|P1|
|4|FR-004|Attach subcommand|Reattach to a detached tmux job's TUI.|cli|COMP-014,COMP-013|command:swarm_attach; target:detached_job; tui_attach:true|M|P1|
|5|FR-005|Kill subcommand|Terminate a running detached job safely.|cli|COMP-014|command:swarm_kill; target:detached_job; terminal_contract_attempted:true|M|P1|
|6|FR-006|Starter job-spec subcommand|Emit a starter job-spec file for a named lens.|cli|COMP-002,COMP-022|command:starter_spec; lens_required:true; job_spec_validates:true; writes_under_requested_path:true|S|P1|
|7|FR-007|Validate subcommand|Validate a job-spec file without dispatching workers.|cli|COMP-002,COMP-005|command:swarm_validate; dispatch_called:false; schema_errors_reported:true|S|P0|
|8|FR-013|Monitoring patterns|Support background done-sentinel wait, Monitor JSONL tail, and `status --watch`.|observability|FR-026,FR-027,FR-002|patterns:done_json_wait/jsonl_tail/status_watch; terminal_states_visible:true|M|P1|
|9|FR-014|Detached tmux mode|Run jobs in detached tmux mode behind `--detached` while inline remains default.|tmux|AC-008,COMP-014|flag:--detached; default:inline; tmux_wrapper:true; sprint_pattern_mirrored:true|M|P1|
|10|FR-015|Resume and crash recovery command|Implement `run --resume <job_id>` with worker skip and redispatch semantics.|cli|INV-001,NFR-005|wave0_resume:true; skip_success_meta:true; redispatch_remaining:true; rerun_wave2:true; merge_regen:true|L|P0|
|11|NFR-015|Sprint-shaped module familiarity|Keep swarm module shape aligned to sprint for maintainability.|architecture|AC-003|shape_mirrors_sprint:true; tmux_pattern_mirrors_sprint:true; operator_familiarity:true|S|P1|
|12|COMP-013|TUI module|Implement Rich Live dashboard gated by `--tui`.|tui|INV-012|file:cli/swarm/tui.py; role:rich_live_dashboard; deps:Rich|M|P1|
|13|COMP-014|tmux module|Implement detached-run wrapper mirroring sprint tmux conventions.|tmux|FR-014|file:cli/swarm/tmux.py; role:detached_run_wrapper; deps:tmux_binary|M|P1|

### Integration Points — M5

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Click commands → runtime modules|command dispatch|Yes: command handlers call preflight/dispatch/normalize/reduce/state/tmux modules|M5|operators; skills; non-Claude callers|
|status --watch → state/logs|watch binding|Yes: watch mode polls state and log artifacts, not worker memory|M5|monitoring users|
|logs → JSONL/Markdown|log reader|Yes: tail/dump selects durable log sources|M5|debugging and incident review|
|attach/kill → tmux|process lifecycle|Yes: detached job IDs map to tmux sessions|M5|detached mode operators|
|TUI → Rich Live|dashboard binding|Yes: only `--tui` activates Rich terminal dashboard|M5|interactive users|

### Risk Assessment and Mitigation — M5

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Tmux dependency for detached mode|LOW|MEDIUM|Detached jobs unavailable on hosts without tmux|Keep detached optional; inline default; return clear validation error|DevOps|
|2|Non-TTY callers receive terminal control sequences|MEDIUM|LOW|Automation logs become unreadable|Gate TUI behind `--tui`; add non-TTY assertion in tests|CLI Lead|
|3|Operator surface grows faster than contracts|MEDIUM|MEDIUM|Commands diverge in output/error behavior|Route every command through shared schema/state/contract helpers|Architect|

### Milestone Dependencies — M5

- M2 durable state/log artifacts must exist for status/log/watch commands.
- M4 resume semantics and lens resolution must exist before `run --resume` is exposed.

### Open Questions — M5

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-003|Should `recommended_next_command` ever be auto-executed via an auto-handoff flag?|Controls CLI safety boundary and downstream command execution|Architect+Security|M5 exit|
|2|OQ-004|Should Prometheus/OpenMetrics output be emitted at event boundaries?|Controls observability scope and dependency footprint|Architect+DevOps|M5 exit|

## M6: Invariant and Integration Validation

**Objective:** Prove IMM/INV invariants, merge boundaries, lens validation, non-Claude caller compatibility, and migration parity before release packaging | **Duration:** Weeks 7-8 (2 weeks) | **Entry:** M1-M5 implementation complete | **Exit:** Full targeted test suite passes with UV; boundary and parity failures block release

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|NFR-007|Invariant test coverage|Implement tests for every IMM acceptance case and INV remediation case.|tests|M1-M5|IMM_tests:100%; INV_tests:100%; boundary_test:true; parity_test:true|L|P0|
|2|TEST-001|IMM acceptance suite|Validate parallelism, empty-target STOP, status policy, atomicity, and prompt guard edge cases.|tests|IMM-3,IMM-4,IMM-5,IMM-6,§11.5|parallel_overlap:true; 49_byte_target_fails:true; status_matrix_pass:true; mid_write_kill_safe:true; end_marker_target_safe:true|L|P0|
|3|TEST-002|INV remediation suite|Validate manifest lens resume, Python-only dispatch, custom prompt guard, merge regeneration, and guard parity.|tests|INV-001,INV-002,INV-003,INV-010,INV-014|manifest_lens_used:true; shell_dispatch_absent:true; custom_guard_enforced:true; resume_merge_regen:true; escape_hatch_parity:true|L|P0|
|4|TEST-003|Bare-review parity test|Compare thin caller output against current bare-review behavior on identical targets.|tests|FR-029|same_target:true; output_equivalence:true; contract_relayed:true|M|P0|
|5|TEST-004|Bundled lens validation gate|Run `swarm validate-lenses` for all non-custom bundled entries.|tests|U-008,FR-008,FR-009|non_custom_entries:7; validator_passes:true; guard_substring_verified:true|M|P0|
|6|TEST-005|Non-Claude caller integration|Invoke CLI through subprocess from a non-Python-language harness and compare result contract.|tests|FR-030,NFR-016|subprocess_invocation:true; detached_supported:true; contract_identical:true|M|P1|
|7|TEST-006|Mechanical merge boundary test|Assert three-worker concat preserves slot order and performs no transformations beyond provenance header.|tests|FR-012,NFR-009|workers:3; slot_order:true; all_sections_present:true; transformations:none_beyond_header|M|P0|
|8|TEST-007|Resume crash recovery E2E|Verify successful worker meta is skipped, remaining workers rerun, Wave 2 reruns, and merge regenerates.|tests|FR-015,NFR-005,INV-010|skip_success:true; redispatch_remaining:true; rerun_wave2:true; merged_regenerated:true|L|P0|
|9|TEST-008|Migration completion verification|Validate migrated skill caller, deleted shell scripts, sync state, and production release readiness.|tests|FR-029,AC-019|thin_caller:true; shell_scripts_removed:true; make_sync_dev_done:true; verify_sync_passes:true|M|P1|

### Integration Points — M6

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|UV test runner → tests/swarm|validation pipeline|Yes: all Python validation uses `uv run pytest`|M6|release gate|
|deterministic transport → dispatch tests|test dependency|Yes: transport simulates worker outcomes without network|M6|IMM/INV suites|
|boundary test → merge module|guardrail|Yes: CI blocks behavioral drift in mechanical merge|M6|future PR review|
|parity test → skill migration|acceptance binding|Yes: thin caller migration cannot ship without output equivalence|M6|M7 migration|
|validate-lenses → registry|release gate|Yes: bundled lens registry must pass before packaging|M6|M8 rollout|

### Risk Assessment and Mitigation — M6

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Invariant tests miss concurrent race behavior|HIGH|MEDIUM|False confidence in dispatch/state correctness|Use elapsed-overlap assertions plus mid-write termination tests|QA Lead|
|2|A/B parity under-specifies legacy behavior|MEDIUM|MEDIUM|Skill migration changes user output unexpectedly|Run parity against representative targets and compare normalized output plus contract|QA Lead|
|3|Boundary test becomes a weak gate|HIGH|LOW|Merge module begins filtering or rewriting findings|CI flags test changes and code review treats this test as protected|Architect|

### Milestone Dependencies — M6

- M1-M5 implementation must be complete enough for integration tests.
- Open questions marked for M1/M4/M5 must be resolved or explicitly deferred with documented rationale.

## M7: Skill Migration and Release Packaging

**Objective:** Migrate sc-bare-review to a thin swarm caller, remove legacy shell execution path, sync distributable components, and prepare release artifacts | **Duration:** Week 9 (1 week) | **Entry:** M6 validation green | **Exit:** Skill source uses `superclaude swarm run --lens bare-review`; dev copy synced; legacy scripts removed; packaging checks pass

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-029|sc-bare-review thin caller migration|Rewrite skill as a concise caller that builds bare-review job spec, executes CLI, and relays return contract.|skill|M6|source_path:src/superclaude/skills/sc-bare-review/SKILL.md; approx_lines:60; lens:bare-review; contract_relay:true; parity_test_pass:true; legacy_shell_scripts_removed:true|L|P0|
|2|MIG-001|Source-first sync workflow|Apply changes in `src/superclaude/` and sync generated dev copies afterward.|release|AC-019,FR-029|src_updated:true; make_sync_dev:true; direct_dev_copy_edits:false|M|P0|
|3|MIG-002|Package entry registration|Register swarm CLI package and command group in the distributable CLI entry points.|release|COMP-001,COMP-002|superclaude_swarm_available:true; command_help_lists_subcommands:true; package_imports_clean:true|M|P0|
|4|MIG-003|Legacy shell retirement|Remove old shell orchestration from skill package after parity gate passes.|release|TEST-003|shell_path_removed:true; python_cli_path_used:true; no_legacy_dispatch_refs:true|M|P1|
|5|MIG-004|Release notes and operator migration note|Document new CLI invocation, resume behavior, prompt guard requirement, and custom prompt migration path.|docs|MIG-001|run_examples:true; resume_notes:true; guard_requirement:true; custom_prompt_migration:true|S|P1|

### Integration Points — M7

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|sc-bare-review skill → swarm CLI|caller wiring|Yes: skill builds job spec and invokes `superclaude swarm run --lens bare-review`|M7|existing skill users|
|skill return contract → user output|contract relay|Yes: skill relays CLI contract and artifacts instead of reinterpreting worker output|M7|operators; downstream commands|
|src → dev copy sync|release pipeline|Yes: `make sync-dev` updates development copy after source edit|M7|local Claude Code runtime|
|package entry → CLI help|registration|Yes: swarm group appears in CLI help after install|M7|non-Claude callers|

### Risk Assessment and Mitigation — M7

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Skill migration bypasses source-of-truth rules|HIGH|LOW|Generated dev copies drift from source|Edit source first; run sync and verify; never stage generated `.claude` content|Release Lead|
|2|Legacy shell removal happens before parity proof|MEDIUM|LOW|Regression without easy comparison|Require TEST-003 green before removing legacy path|QA Lead|
|3|Release notes omit custom prompt guard migration|MEDIUM|MEDIUM|Existing custom users fail preflight unexpectedly|Document guard sentence and `--auto-inject-guard` escape path|Technical Writer|

### Milestone Dependencies — M7

- M6 validation must pass before production skill migration.
- M4 custom prompt guard behavior must be final before migration notes are written.

## M8: Operational Rollout and Documentation

**Objective:** Prepare operators, observability guidance, dependency checks, rollback procedures, and post-release maintenance policy | **Duration:** Week 10 (1 week) | **Entry:** M7 packaged release candidate | **Exit:** Operators can run, monitor, resume, and troubleshoot swarm jobs using documented commands and contracts

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|OPS-001|Operator runbook|Document run/status/logs/watch/resume/kill/attach workflows with single-line commands.|docs|M5,M7|commands:run/status/logs/watch/resume/kill/attach; single_line_examples:true; contract_paths_explained:true|M|P1|
|2|OPS-002|Environment readiness check|Document and validate Python, UV, httpx, Click, Rich, tmux, and T2 proxy prerequisites.|ops|M2,M5|python>=3.10; uv:true; httpx:true; click>=8; rich>=13; tmux_optional:true; T2_env:true|S|P1|
|3|OPS-003|Observability procedure|Define how to monitor state file, JSONL log, Markdown log, done sentinel, and return contract.|ops|FR-013,NFR-004|state_file; jsonl_log; markdown_log; done_sentinel; return_contract|S|P1|
|4|OPS-004|Rollback procedure|Describe reverting skill caller to previous release and disabling detached rollout if needed.|ops|M7|skill_rollback_steps:true; detached_disable_steps:true; artifacts_preserved:true|S|P1|
|5|OPS-005|Lens contribution policy|Document review requirements for adding or changing lens entries.|docs|NFR-012|real_caller_required:true; guard_required:true; template_alignment:true; downstream_command_required:true; suspect_review:true|S|P1|
|6|OPS-006|Post-release metrics review|Review validation failures, env-missing contracts, resume usage, and custom prompt guard failures after rollout.|ops|M8|metrics:validation_failures/env_missing/resume_count/guard_failures; review_window:post_release|S|P2|

### Integration Points — M8

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|runbook → CLI|operator workflow|Yes: documented commands map to released CLI flags|M8|operators|
|return-contract.yaml → troubleshooting|diagnostic contract|Yes: contract fields point to logs, state, outputs, and next command|M8|support and incident response|
|lens policy → PR review|governance hook|Yes: contribution rules map to validator and review checklist|M8|future lens authors|
|post-release metrics → backlog|feedback loop|Yes: failures and guard friction become follow-up tasks|M8|maintainers|

### Risk Assessment and Mitigation — M8

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Rollout starts without operator observability|MEDIUM|LOW|Incidents take longer to diagnose|Publish runbook and contract field map before release|Release Lead|
|2|Documentation diverges from CLI contract|MEDIUM|MEDIUM|Operators run wrong commands or expect wrong artifacts|Generate docs from final flag/contract review and verify examples manually|Technical Writer|
|3|Environment readiness gaps surface in production|MEDIUM|MEDIUM|Jobs fail due to missing tmux or T2 env vars|Provide readiness checks and structured env-missing failure contract|DevOps|

### Milestone Dependencies — M8

- M7 release candidate must be available for final command verification.
- M6 and M7 validation results must be summarized in release notes.

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By Milestone|Status|Fallback|
|---|---|---|---|
|Python ≥3.10|M1-M8|Required|Block install until runtime meets minimum|
|UV|M1-M8|Required|No fallback; all Python operations use UV|
|httpx|M2|Required for reference transport|Package dependency check before release|
|Click ≥8.0.0|M1,M5|Required for CLI|Package dependency check before release|
|Rich ≥13.0.0|M5|Optional unless `--tui` used|Plain non-TUI output remains default|
|pytest ≥7.0.0|M6|Required for validation|Block release if unavailable|
|tmux|M5,M8|Optional for detached mode|Inline mode remains default|
|T2 proxy endpoint|M2,M6,M8|Required for live dispatch|Deterministic transport for tests; structured env-missing contract for runtime|
|ParallelExecutor internal module|M2|Required|Block implementation until import path verified|
|Parent bare-review v1.3.0-draft spec|M4,M7|Required for parity|Defer migration if parity fixture cannot be reproduced|
|/sc:adversarial downstream caller|M3,M8|Referenced only|Do not auto-execute; emit recommended command only|

### Infrastructure Requirements

- Writable `--output` directory with path-resolution guard preventing writes outside it.
- Environment variables `T2ProxyUrl`, `T2ProxyKey`, and one or more `T2Model0N` values for live transport.
- Optional tmux binary for `--detached`, `attach`, and `kill` workflows.
- CI lane running `uv run pytest` for swarm unit, integration, boundary, and parity tests.
- Dev sync lane running `make sync-dev` and `make verify-sync` after source changes.

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|R-001|Schema decisions drift after implementation begins|M1|MEDIUM|MEDIUM|Freeze M1 contracts; require migration notes for post-M1 field changes|Architect|
|R-002|Output boundary and caller metadata rules remain ambiguous|M1|MEDIUM|MEDIUM|Resolve OQ-006/OQ-008/OQ-009 before M1 exit|Architect+Security|
|R-003|ThreadPoolExecutor surprise: developers may not expect threading behavior|M2|MEDIUM|LOW|Document dispatch threading; protect JSONL appends with lock; prove with deterministic transport|Backend Lead|
|R-004|Partial artifact writes under crashes|M2|MEDIUM|HIGH|Use temp+replace for every artifact; add mid-write termination test|Backend Lead|
|R-005|T2 env misconfiguration blocks dispatch|M2,M8|MEDIUM|MEDIUM|Emit structured env-missing failure when output dir is creatable|DevOps|
|R-006|Merge boundary erosion: normalize+merge drifts into judging|M3|MEDIUM|HIGH|Enforce ≤30 LOC, boundary docstring, boundary test, and PR review note|Architect|
|R-007|Normalizer output shapes diverge from lens templates|M3,M4|MEDIUM|MEDIUM|Validate recipe/template alignment in registry validator and tests|Backend Lead|
|R-008|Lens-registry sprawl: every new lens ships built-in entry|M4,M8|MEDIUM|MEDIUM|Require real caller and downstream command reference; route one-off needs through custom prompts|Architect|
|R-009|Resume and lens mutation interaction|M4|MEDIUM|MEDIUM|Use manifest lens snapshot by default; require explicit `--force-relens`; test both paths|Backend Lead|
|R-010|Custom prompt guard parity breaks for existing users|M4,M7|MEDIUM|MEDIUM|Apply identical preflight rule; provide opt-in auto-inject flag and migration docs|Security|
|R-011|Tmux dependency for detached mode|M5,M8|MEDIUM|LOW|Keep detached optional; inline default; return clear validation error|DevOps|
|R-012|Non-TTY callers receive terminal control sequences|M5|LOW|MEDIUM|Gate TUI behind `--tui`; add non-TTY assertion in tests|CLI Lead|
|R-013|Operator surface grows faster than contracts|M5|MEDIUM|MEDIUM|Route commands through shared schema/state/contract helpers|Architect|
|R-014|Invariant tests miss concurrent race behavior|M6|MEDIUM|HIGH|Use elapsed-overlap assertions plus mid-write termination tests|QA Lead|
|R-015|A/B parity under-specifies legacy behavior|M6,M7|MEDIUM|MEDIUM|Run parity against representative targets and compare normalized output plus contract|QA Lead|
|R-016|Boundary test becomes a weak gate|M6|LOW|HIGH|CI flags test changes and code review treats boundary test as protected|Architect|
|R-017|Skill migration bypasses source-of-truth rules|M7|LOW|HIGH|Edit source first; run sync and verify; never stage generated `.claude` content|Release Lead|
|R-018|Legacy shell removal happens before parity proof|M7|LOW|MEDIUM|Require TEST-003 green before removing legacy path|QA Lead|
|R-019|Release notes omit custom prompt guard migration|M7|MEDIUM|MEDIUM|Document guard sentence and `--auto-inject-guard` escape path|Technical Writer|
|R-020|Rollout starts without operator observability|M8|LOW|MEDIUM|Publish runbook and contract field map before release|Release Lead|
|R-021|Documentation diverges from CLI contract|M8|MEDIUM|MEDIUM|Verify examples against final CLI flags and contract fields|Technical Writer|
|R-022|Environment readiness gaps surface in production|M8|MEDIUM|MEDIUM|Provide readiness checks and structured env-missing failure contract|DevOps|
|R-023|Schema evolution drag breaks loaders|M4|LOW|LOW|Support best-effort forward compatibility for spec 1.0 under orchestrator 1.1|Architect|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|Milestone|
|---|---|---|---|---|
|IMM acceptance coverage|IMM tests passing|100%|`uv run pytest tests/swarm/ -k imm`|M6|
|INV remediation coverage|INV tests passing|100%|`uv run pytest tests/swarm/ -k inv`|M6|
|Bare-review migration parity|Output equivalence|Equivalent normalized output and relayed contract|A/B parity test on identical targets|M6-M7|
|Bundled lens validation|Non-custom lens entries passing|7/7|`superclaude swarm validate-lenses` in test lane|M4-M6|
|Non-Claude caller compatibility|Subprocess contract comparison|Identical result contract|Non-Python subprocess integration test|M6|
|Mechanical merge boundary|Concat behavior|All 3 sections in slot order; no transforms beyond header|`test_merge_mechanical_only.py` plus CI protection|M3-M6|
|Resume crash recovery|Worker skip and merge regeneration|Successful worker skipped; remaining workers rerun; merge regenerated|End-to-end resume test|M4-M6|
|Migration completion|10-phase migration complete|Thin caller, scripts removed, sync verified, release notes published|Release checklist and `make verify-sync`|M7-M8|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|---|---|---|---|
|Concurrency model|Python `ParallelExecutor` wrapping ThreadPoolExecutor|Shell fan-out; direct ThreadPoolExecutor|Internal abstraction preserves project idioms and makes concurrency testable while retiring brittle shell assumptions|
|Resume source of truth|Manifest snapshot by default|Re-resolve lenses every resume; cache responses|Manifest preserves intended job semantics across registry changes and avoids stale provenance|
|Prompt guard enforcement|Required substring plus delimiters across all prompt paths|Only lens-driven guard; warning-only custom prompts|Uniform enforcement closes escape hatch parity gaps and blocks dispatch before unsafe prompts leave preflight|
|Merge behavior|Mechanical concat only|Scored merge; dedupe/reorder/filter worker outputs|Keeps swarm as dispatch/normalization infrastructure and preserves `/sc:adversarial` as scored merge owner|
|TUI behavior|Opt-in `--tui`|Default live dashboard|Automation-safe default avoids terminal control sequences for non-TTY callers|
|Detached behavior|Optional tmux wrapper|Always-detached; no detached mode|Mirrors sprint pattern while preserving inline default and avoiding hard dependency|
|Custom prompts|Allowed with parity guard and auto-inject escape flag|Disallow custom prompts; bypass guard|Preserves extensibility while keeping security invariant explicit and testable|
|Skill migration|Thin CLI caller|Keep shell scripts; embed orchestration in SKILL.md|Centralizes swarm behavior in Python package and reduces skill-specific maintenance burden|

## Timeline Estimates

|Milestone|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1|1 week|Week 1|Week 1|Contracts, constraints, data models, module boundaries|
|M2|2 weeks|Week 2|Week 3|Dispatch, atomic state/logging, transport, result contract|
|M3|1 week|Week 4|Week 4|Recipes, status reduction, parse salvage, mechanical merge|
|M4|1 week|Week 5|Week 5|Lenses, prompt guard parity, manifest resume, validator|
|M5|1 week|Week 6|Week 6|Status/logs/attach/kill/validate/run-resume/TUI/tmux commands|
|M6|2 weeks|Week 7|Week 8|IMM/INV suites, parity, boundary, non-Claude integration|
|M7|1 week|Week 9|Week 9|Skill migration, release packaging, source sync|
|M8|1 week|Week 10|Week 10|Runbook, readiness, rollout, post-release metrics|

**Total estimated duration:** 10 weeks
