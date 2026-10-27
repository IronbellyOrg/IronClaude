---
spec_source: extraction.md
complexity_score: 0.82
complexity_class: HIGH
primary_persona: architect
adversarial: false
base_variant: none
variant_scores: none
convergence_score: null
---

# MultiModelSwarm — Project Roadmap

## Executive Summary

This roadmap plans the implementation of `superclaude swarm`, a new top-level CLI verb for single-shot parallel multi-model fan-out. It introduces 9 subcommands, 17 modules, 10 data models, an 8-entry lens registry, a 6-entry recipe registry, and a 3-layer observability contract. The orchestrator enforces parallelism via Python ThreadPoolExecutor (NFR-001), maintains prompt-injection guards across three input paths (NFR-002), and guarantees atomic-write durability (NFR-004). Six parent-spec invariants (IMM-3/4/5/6 + INV-001/002/003/010/014/016) must be remediated with acceptance tests. The final milestone migrates `sc-bare-review` to a thin caller (~60 lines) with A/B parity validation.

**Business Impact:** Replaces shell-script-mediated multi-model dispatch with a code-enforced, resumable, observable orchestrator. Eliminates dual-writer races, enables crash recovery, and provides a reusable policy registry (lenses + recipes) for future multi-model workflows beyond bare-review.

**Complexity:** HIGH (0.82) — driven by code-enforced parallelism with multiple lock disciplines, four structural guards on merge boundary, dual prompt-input-path validation, and six invariant remediation tests.

**Critical path:** Foundation data models → schema validators → preflight (Wave 0) → dispatch (Wave 1) with ThreadPoolExecutor → normalize (Wave 2) recipes → reduce/merge (Wave 3) → observability + TUI → integration + invariant tests → sc-bare-review migration.

**Key architectural decisions:**

- ThreadPoolExecutor via `superclaude.execution.parallel.ParallelExecutor` — not shell scripts, not asyncio (AC-005, FR-041)
- Lens registry as bundled Python dataclasses under `cli/swarm/lenses/` — not a plugin system (AC-003)
- Module layout mirrors `cli/sprint/` for operator continuity (NFR-007, AC-004)
- Merge module ≤30 LOC, mechanical concat only — no scoring/dedup/reorder (NFR-006, AC-009)
- Transport layer pluggable with OpenAI-compatible reference + stub transport (AC-006)

**Open risks requiring resolution before M1:**

- OQ-007 (workers > T2Models guard semantics): confirm warn-on-exceed vs STOP before dispatch module interface is finalized
- OQ-008 (empty-pool failure path): confirm write-on-failure vs pre-output-dir abort before reduce module state machine is designed

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|----|-------|------|----------|--------|--------------|--------------|------|
|M1|Foundation + Core Data Models|Foundation|P0|M|Project kickoff|16|Medium|
|M2|Schema + Lens Registry + Config|Policy|P0|M|M1|15|Medium|
|M3|Preflight (Wave 0)|Core|P0|L|M2|13|Medium|
|M4|Dispatch (Wave 1)|Core|P0|XL|M3|14|High|
|M5|Normalize (Wave 2)|Core|P0|L|M4|14|Medium|
|M6|Reduce + Merge (Wave 3)|Core|P0|L|M5|13|High|
|M7|TUI + Detached + Monitoring|UX|P1|L|M3, M4, M6|13|Medium|
|M8|Integration + Invariant Tests|Verification|P0|XL|M1–M7|18|High|
|M9|sc-bare-review Migration|Migration|P1|L|M8|8|Medium|

## Dependency Graph

M1 → M2 → M3 → M4 → M5 → M6 → M7
M3 ────────────────→ M7
M4 ────────────────→ M7
M6 ────────────────→ M7
M1 → M8 ← M2
M3 → M8
M4 → M8
M5 → M8
M6 → M8
M7 → M8
M8 → M9

## M1: Foundation + Core Data Models

**Objective:** Create module skeleton, core data models, and internal transport interfaces | **Duration:** Weeks 1–2 | **Entry:** Project kickoff complete | **Exit:** All DM-xxx dataclasses compile, all COMP-xxx module stubs import cleanly, REGISTRY dicts empty but typed

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-001|swarm_group Click group|Create top-level Click group at `src/superclaude/cli/swarm/__init__.py` exposed as `superclaude swarm`|COMP-001|—|swarm_group importable; registered under superclaude CLI|S|P0|
|2|COMP-002|commands module stub|Create commands module at `src/superclaude/cli/swarm/commands.py` with placeholder subcommand registrations|COMP-002|COMP-001|module imports; Click subcommands registered but raise NotImplementedError|S|P0|
|3|COMP-003|SwarmConfig dataclass|Create config dataclass at `src/superclaude/cli/swarm/config.py` with path resolution helpers|COMP-003|—|SwarmConfig dataclass with output_dir, log_level, mode fields; path resolution tested|S|P0|
|4|DM-001|JobSpec dataclass|Define JobSpec dataclass with all 15 fields: spec_version:str; job_id:str; created:str; caller:dict; lens:str|None; custom_prompt_dir:str|None; workers:WorkerSpec; transport:dict; prompt:dict; target:dict; normalization:dict; output:dict; amalgamation_mode:Literal; status_policy:dict; recommended_next_command_template:str; recommended_next_command_substitutions:dict; runtime:dict|COMP-004|—|all fields typed; frozen dataclass; round-trip serialize/deserialize|S|P0|
|5|DM-002|WorkerSpec dataclass|Define WorkerSpec dataclass with all 5 fields: count:int; models:list[str]; timeout_sec:int; temperature:float; retry:dict|COMP-004|DM-001|all fields typed; count >= 1 validation; retry sub-fields typed|S|P0|
|6|DM-003|ResultContract dataclass|Define ResultContract dataclass with all 17 fields: contract_version:str; status:Literal; job_id:str; started:str; finished:str; elapsed_ms:int; caller:dict; lens:str|None; lens_source:Literal|None; target:dict; workers_requested:int; workers_succeeded:int; workers_failed:int; output_files:list; amalgamation_mode:Literal; merged_path:str|None; caller_metadata:dict; recommended_next_command:str; artifacts:dict|COMP-004|DM-001, DM-002, DM-004|all fields typed; Literal enums correct; round-trip serialize|S|P0|
|7|DM-004|WorkerResult dataclass|Define WorkerResult dataclass with all 11 fields: index:int; path:str|None; raw_path:str|None; meta_path:str; model_id:str; model_label:str; bytes:int; status:Literal; http_code:int; attempts:int; elapsed_ms:int|COMP-004|DM-003|all fields typed; status Literal covers success/timeout/proxy_error/parse_error|S|P0|
|8|DM-005|SwarmState dataclass|Define SwarmState dataclass with all fields: state:Literal; job_id:str; transition_timestamp:str; current_wave:int; worker_progress:dict|COMP-004|DM-004|state Literal covers preflight_ok/dispatching/normalizing/reducing/terminal; atomic read/write interface|S|P0|
|9|DM-006|EventRecord dataclass|Define EventRecord dataclass with all fields: event_type:str; timestamp:str; worker_index:int|None; payload:dict|COMP-004|DM-005|event_type covers worker_start/worker_progress/worker_done/wave_transition/final; JSON-serializable|S|P0|
|10|DM-007|LensEntry dataclass|Define frozen LensEntry dataclass with all 13 fields: name:str; description:str; system_prompt_fragment:str; user_template:str; output_template_path:str|None; recipe_name:str; default_workers:int; default_target_line_cap:int; suspect:bool; tier:str; recommended_next_command_template:str; acceptance_notes:str; stability:Literal|COMP-004|DM-006|frozen=True; name kebab-case validation; stability Literal covers stable/experimental|S|P0|
|11|DM-008|Manifest dataclass|Define Manifest dataclass with all fields: contract_version:str; job_id:str; resolved_lens_entry:dict|COMP-004|DM-007|resolved_lens_entry snapshot captures all LensEntry fields; JSON-serializable|M|P0|
|12|DM-009|RecipeProtocol interface|Define Recipe Protocol ABC with normalize method signature: normalize(raw_text:str, args:dict, template_path:str|None) -> tuple[str, dict]; ParseError exception class|COMP-014|DM-009|ABC defines normalize signature; ParseError inherits from ValueError; docstring specifies return contract|S|P0|
|13|DM-010|TransportProtocol interface|Define Transport Protocol ABC with dispatch method signature: dispatch(body:dict, timeout_sec:int) -> dict; typed exceptions for 4xx/5xx/timeout|COMP-018|DM-010|ABC defines dispatch signature; TransportError, TransportTimeoutError, TransportAuthError classes|S|P0|
|14|COMP-004|models module container|Create `src/superclaude/cli/swarm/models.py` hosting all DM-001 through DM-010 dataclasses|COMP-004|—|all 10 dataclasses importable; no circular imports; __all__ exported|S|P0|
|15|COMP-018|transports package stub|Create transports package at `src/superclaude/cli/swarm/transports/` with `__init__.py` exposing TransportProtocol; stub `openai_compat.py` and `stub.py` module shells|COMP-018|DM-010|package imports; protocol exposed; openai_compat.py has class shell; stub.py has class shell|S|P0|
|16|COMP-010|state module stub|Create state module at `src/superclaude/cli/swarm/state.py` with read/write function shells for `.swarm-state.json`|COMP-010|DM-005|module imports; read/write signatures defined; atomic-write pattern documented|S|P0|

### Integration Points — M1

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|DM-001..DM-010|Data model definitions|Yes|M1|M2 (schema), M3 (preflight), M4 (dispatch)|
|COMP-004|models module|Yes|M1|All downstream modules|
|COMP-018|transports package|Interface only|M1|M4 (dispatch)|
|DM-009|RecipeProtocol|Interface only|M1|M5 (normalize)|

### Milestone Dependencies — M1

- None — project foundation

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-007|Workers > configured T2Models: warn-on-exceed-with-defaults (V1) or STOP (V2)?|Determines dispatch module validation behavior and error contract|Architect|M2|
|2|OQ-008|Empty-pool failure path: write failed/env-missing contract OR pre-output-dir abort?|Determines reduce module state machine and exit-code mapping|Architect|M3|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Data model field mismatch with parent spec|High|Medium|All downstream modules break|Cross-reference every field against extraction DM-xxx definitions; add field-count assertions in tests|Architect|
|2|Circular import between models and schema|Medium|Low|Import failures cascade|schema imports models, never reverse; enforce via import-order lint|Architect|

## M2: Schema + Lens Registry + Config

**Objective:** Create JSON Schema validators, lens registry with 8 entries, and cross-field validation rules | **Duration:** Weeks 2–3 | **Entry:** M1 data models compile | **Exit:** `swarm validate` passes on valid spec; lens registry validator catches all defined violations

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-005|JSON Schema module|Create `src/superclaude/cli/swarm/schema.py` with JSON Schema for JobSpec; cross-field validators; §11.5 required-substring rule on prompt.system|COMP-005|COMP-004|Schema validates all DM-001 fields; rejects missing required fields; §11.5 substring check|M|P0|
|2|FR-017|JSON Schema validation|Implement JSON Schema validation of job spec with cross-field rules and §11.5 required-substring rule|COMP-005|COMP-004|Valid spec passes; invalid spec raises ValidationError with field path|M|P0|
|3|COMP-016|lenses package|Create lenses package at `src/superclaude/cli/swarm/lenses/` with `__init__.py` exposing LENSES dict and LensEntry|COMP-016|COMP-004, DM-007|package imports; LENSES dict typed Dict[str, LensEntry]|S|P0|
|4|COMP-019|bare-review lens entry|Create bare_review.py lens entry: stable, suspect:true, T2 tier, default_workers=3, next-cmd references /sc:adversarial|COMP-019|COMP-016|entry in LENSES; §11.5 substring present; recipe_name resolves|S|P0|
|5|COMP-020|refactor-find lens entry|Create refactor_find.py lens entry: experimental, T2-code, default_workers=3, suspect:false|COMP-020|COMP-016|entry in LENSES; recipe_name resolves|S|P1|
|6|COMP-021|edge-case-hunt lens entry|Create edge_case_hunt.py lens entry: experimental, T2-edge, default_workers=4, suspect:false|COMP-021|COMP-016|entry in LENSES; recipe_name resolves|S|P1|
|7|COMP-022|spec-completeness lens entry|Create spec_completeness.py lens entry: experimental, T2-spec, default_workers=3, suspect:false|COMP-022|COMP-016|entry in LENSES; recipe_name resolves|S|P1|
|8|COMP-023|feasibility-probe lens entry|Create feasibility_probe.py lens entry: experimental, T2-feas, default_workers=3, suspect:false|COMP-023|COMP-016|entry in LENSES; recipe_name resolves|S|P1|
|9|COMP-024|troubleshoot-hypothesis lens entry|Create troubleshoot_hypothesis.py lens entry: experimental, T2-tshoot, default_workers=4, suspect:false|COMP-024|COMP-016|entry in LENSES; recipe_name resolves|S|P1|
|10|COMP-025|doc-completeness lens entry|Create doc_completeness.py lens entry: experimental, T2-doc, default_workers=3, suspect:false|COMP-025|COMP-016|entry in LENSES; recipe_name resolves|S|P1|
|11|COMP-026|custom lens entry|Create custom lens entry as escape hatch: caller-supplied via --custom-prompt-dir|COMP-026|COMP-016|entry in LENSES; marks custom_prompt_dir required|S|P0|
|12|COMP-017|lens validator submodule|Create `_validate.py` at `cli/swarm/lenses/_validate.py`: file refs resolve, recipe resolution including custom-py:, suspect→suspect_files coupling, name uniqueness, §11.5 substring|COMP-017|COMP-016|validator catches all 5 violation types; returns diagnostic list|M|P0|
|13|FR-009|validate-lenses CLI|Implement `swarm validate-lenses` subcommand: assert each entry's refs resolve, recipe_name registered, suspect entries include {suspect_files}, name uniqueness, §11.5 substring|COMP-002, COMP-017|COMP-016|exit 0 on clean registry; exit 2 with diagnostics on violations|S|P0|
|14|FR-008|validate CLI subcommand|Implement `swarm validate <spec.yaml>` subcommand: load spec, run JSON Schema validation, report errors without dispatching|COMP-002|COMP-005|valid spec → exit 0; invalid → exit 2 with field-level errors|S|P0|
|15|NFR-008|PR-review gate doc|Document lens entry PR-review discipline: real caller existence, injection-guard presence, normalizer fit, downstream-command validity, suspect-flag justification|COMP-016|—|Doc in `docs/swarm-lens-review-checklist.md`|S|P1|

### Integration Points — M2

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|COMP-005|JSON Schema|Yes|M2|M3 (preflight validation)|
|COMP-016|Lens registry|Yes|M2|M3 (lens resolution)|
|COMP-017|Lens validator|Yes|M2|M7 (validate-lenses CLI)|
|COMP-019..COMP-026|Lens entries|Yes|M2|All dispatch workflows|

### Milestone Dependencies — M2

- M1 (DM-001, DM-007, COMP-004)

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Lens-registry sprawl|Medium|Medium|Package bloat, maintenance drag|PR-review discipline requires real caller; entries without caller deferred to custom-py:|Architect|
|2|§11.5 substring check inconsistency across paths|High|Medium|Injection guard bypass in custom-prompt-dir path|Single canonical check function reused by schema validator, lens validator, and preflight|Architect|

## M3: Preflight (Wave 0)

**Objective:** Implement Wave 0: lens resolution, custom-prompt-dir guard, target ingest/checksum, IMM-4 empty-target guard, manifest emission | **Duration:** Weeks 3–4 | **Entry:** M2 schema + lens registry complete | **Exit:** Preflight produces manifest.json + .swarm-state.json with state=preflight_ok

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-006|preflight module|Create `src/superclaude/cli/swarm/preflight.py` orchestrating Wave 0: lens resolution, target ingest, checksum, IMM-4 guard, manifest emission|COMP-006|COMP-005, COMP-016, COMP-010|module imports; all Wave 0 steps callable|M|P0|
|2|FR-018|Lens resolution and materialization|Resolve --lens against cli/swarm/lenses/ registry; materialize resolved_lens_entry snapshot into manifest.json capturing name, system_prompt_fragment, user_template, recipe_name, default_workers, suspect, tier, recommended_next_command_template, stability|COMP-006|COMP-016, DM-008|manifest.json contains full resolved_lens_entry snapshot; verbatim copy of LensEntry|M|P0|
|3|FR-020|Target read, truncate, checksum|Read + truncate target; compute sha256[:12] provenance checksum; enforce IMM-4: <50 non-whitespace bytes → write failed/target-too-small contract and STOP|COMP-006|COMP-010|49-byte target triggers failed contract; 50+ byte target produces checksum; truncation at line_cap|S|P0|
|4|FR-021|Prompt composition with delimiters|Wrap target in <<<TARGET>>> / <<<END TARGET>>> delimiters; system-prompt states data-vs-instructions separation; enforce across all three input paths|COMP-006|COMP-006|prompt output contains delimiters; target content between delimiters; system text references separation|M|P0|
|5|FR-023|Custom-prompt-dir guard parity|When lens == 'custom', read <dir>/system.txt, <dir>/user.txt, <dir>/meta.yaml; §11.5 substring check applies identically; default STOP with actionable error if absent; --auto-inject-guard opts into auto-prepending|COMP-006|COMP-005|custom prompt without §11.5 → STOP with error; with --auto-inject-guard → canonical sentence prepended|M|P0|
|6|FR-019|Environment resolution|Resolve env vars T2ProxyUrl, T2ProxyKey, T2Model0N defaults|COMP-006|—|env vars resolved into transport config; missing vars → actionable error|S|P0|
|7|FR-022|Manifest + state emission|Emit manifest.json + .swarm-state.json (state=preflight_ok) at preflight completion|COMP-006|COMP-010, DM-008|manifest.json written atomically; .swarm-state.json written atomically with state=preflight_ok|S|P0|
|8|NFR-010|Spec-version forward compatibility|Orchestrator at 1.1 loads specs at 1.0; forward-compat best-effort with warnings|COMP-005|—|1.0 spec loads with warning; structural mismatch raises clear error|M|P1|
|9|FR-010|--lens flag|Implement `swarm run --lens <name>` flag: resolve lens-registry entry; caller may omit prompt/recipe/template fields|COMP-002|COMP-006|lens name resolves to entry; defaults expanded into spec|M|P0|
|10|FR-011|--custom-prompt-dir flag|Implement `swarm run --custom-prompt-dir <path>` flag: when --lens custom, point at directory containing system.txt, user.txt, meta.yaml|COMP-002|COMP-006|path validated; files read; meta.yaml parsed|S|P0|
|11|FR-012|--auto-inject-guard flag|Implement `swarm run --auto-inject-guard` flag: backward-compat for custom-prompt-dir users; auto-prepends canonical §11.5 sentence|COMP-002|COMP-006|flag toggles auto-prepend; canonical sentence injected before validation|S|P0|
|12|FR-039|Lens-driven defaults expansion|When lens set, preflight expands defaults into spec: prompt.system, prompt.user_template, normalization.recipe, normalization.template_path, workers.count, target.truncation.line_cap, output.filename_template, output.lens_name, recommended_next_command_template, caller_metadata.suspect, caller_metadata.tier|COMP-006|COMP-016|all defaults expanded; caller-supplied overrides lens; missing → schema validation error|M|P0|
|13|AC-001|Three-layer separation verification|Verify mechanism/policy/caller separation: orchestrator owns mechanism, lens+recipe own policy, caller owns choice|COMP-006|—|Docstring in preflight.py documents separation; no policy hardcoded in mechanism|S|P1|

### Integration Points — M3

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|manifest.json|Durable artifact|Yes|M3|M4 (dispatch), M7 (resume)|
|.swarm-state.json|State file|Yes|M3|M4 (dispatch), M7 (status, resume)|
|COMP-006|preflight module|Yes|M3|M4 (dispatch wave orchestration)|

### Milestone Dependencies — M3

- M2 (COMP-005 schema, COMP-016 lenses, COMP-017 validator)

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Resume + lens-mutation interaction|Medium|Medium|Stale dispatch on --resume|Default rehydrates from manifest.resolved_lens_entry; --force-relens opts into re-resolution|Architect|
|2|IMM-4 guard false positive|Medium|Low|Valid small targets rejected|Byte count is non-whitespace only; test with 49 and 50 byte targets|QA|

## M4: Dispatch (Wave 1)

**Objective:** Implement Wave 1: ThreadPoolExecutor dispatch via ParallelExecutor, httpx per-worker HTTP, retry policy, hard timeout, event log emission | **Duration:** Weeks 4–6 | **Entry:** M3 preflight complete, transport stub working | **Exit:** N workers dispatched in parallel, each writes .raw + .meta.json sidecar, event log has worker_start/progress/done

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-007|dispatch module|Create `src/superclaude/cli/swarm/dispatch.py` with ThreadPoolExecutor dispatch via execution.parallel.ParallelExecutor; per-worker timeout, 5xx retry, sidecar emission, event logging|COMP-007|COMP-013, COMP-011, COMP-006|module imports; dispatch() callable with JobSpec; returns list of WorkerResult|M|P0|
|2|FR-024|ThreadPoolExecutor dispatch|Use single Python ThreadPoolExecutor via superclaude.execution.parallel.ParallelExecutor; all N workers in one ParallelGroup; code-enforced parallelism|COMP-007|COMP-013|N workers complete in max(per_worker_elapsed) + ε, not Σ(per_worker_elapsed)|M|P0|
|3|FR-025|Per-worker HTTP dispatch|Each task: build HTTP request body via json.dumps; POST via httpx with per-worker timeout; write .raw + .meta.json sidecar|COMP-007, COMP-018|COMP-013|.raw contains response body; .meta.json contains model_id, elapsed_ms, http_code, status, attempts|M|P0|
|4|FR-026|Retry policy|On 5xx: retry once after retry.on_5xx_backoff_sec; on 4xx/timeout/network: no retry; always-record (no silent drops)|COMP-007|COMP-018|5xx triggers exactly 1 retry; 4xx does not retry; meta records attempts count|S|P0|
|5|FR-027|Per-worker hard timeout|Apply per-worker hard timeout (default 180s) to each worker|COMP-007|COMP-018|worker exceeding timeout → status=timeout; .raw not written; .meta.json records timeout|S|P0|
|6|FR-028|Event log emission|Emit worker_start / worker_progress / worker_done events; append under threading.Lock-guarded write|COMP-007, COMP-011|COMP-011|JSONL contains all 3 event types per worker; lock prevents interleaving|S|P0|
|7|NFR-003|No shell interpolation|HTTP request bodies built via json.dumps with target_content via --arg-equivalent — never shell-interpolated|COMP-007|COMP-018|grep confirms no os.system, no subprocess shell=True, no f-string URL interpolation|M|P0|
|8|NFR-005|Lock-coordinated append|JSONL writes under threading.Lock-guard; .swarm-state.json updates under lock + atomic rename|COMP-011|COMP-010|concurrent append test shows no interleaving; state update is atomic|S|P0|
|9|COMP-013|openai_compat transport|Implement OpenAI-compatible transport at `transports/openai_compat.py`: httpx-based POST with T2 proxy env resolution, 4xx/5xx/timeout typed exceptions|COMP-013|DM-010|dispatch() returns parsed JSON on 200; raises TransportAuthError on 401; TransportError on 5xx; TransportTimeoutError on timeout|M|P0|
|10|COMP-013|stub transport|Implement deterministic stub transport at `transports/stub.py`: returns fixed response after configurable delay for testing|COMP-013|DM-010|stub returns deterministic markdown; configurable delay; no network calls|S|P0|
|11|AC-005|ParallelExecutor reuse|Invoke ThreadPoolExecutor via superclaude.execution.parallel.ParallelExecutor — not direct concurrent.futures usage|COMP-007|—|grep confirms no direct concurrent.futures.ThreadPoolExecutor import in dispatch.py|S|P0|
|12|FR-041|Python-only dispatch|Retire V2-style swarm_dispatch.sh shell script; Python ThreadPoolExecutor owns dispatch end-to-end|COMP-007|—|No shell script dispatch path exists; all parallelism via Python|S|P0|
|13|FR-016|Exit codes|Implement exit codes: 0 = run reached Wave 3; 2 = spec validation failure; 3 = preflight failure; 10 = orchestrator internal error|COMP-002|COMP-005, COMP-006|each error path returns correct RC; test suite validates all 4 codes|S|P0|
|14|FR-048|Detached mode tmux wrapper|Create `src/superclaude/cli/swarm/tmux.py` mirroring sprint/tmux.py; support --detached flag|COMP-013|—|tmux session created with swarm run command; session name matches job_id; detach/attach works|M|P1|

### Integration Points — M4

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|.raw files|Worker output|Yes|M4|M5 (normalize)|
|.meta.json files|Worker metadata|Yes|M4|M5 (normalize), M6 (reduce)|
|execution-log.jsonl|Event log|Yes|M4|M7 (status, monitoring)|
|COMP-007|dispatch module|Yes|M4|M5 (wave orchestration)|

### Milestone Dependencies — M4

- M3 (preflight produces manifest, resolved target, transport config)

### Open Questions — M4

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-005|Per-model overrides (e.g., per-model temperature) within one swarm?|Affects WorkerSpec schema and dispatch loop|Architect|Future phase|

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|ThreadPoolExecutor surprise|Low|Low|Operators expect async or process-based parallelism|Documented in dispatch.py docstring; tested with stub transport|Architect|
|2|T2 proxy flakiness|Medium|Medium|Worker failures mask orchestrator bugs|Stub transport for all invariant tests; real transport only for integration tests|QA|

## M5: Normalize (Wave 2)

**Objective:** Implement Wave 2: Recipe Protocol dispatcher + 6-entry recipe registry + parse-error salvage | **Duration:** Weeks 6–7 | **Entry:** M4 dispatch produces .raw + .meta.json files | **Exit:** Each worker's .raw normalized to deterministic final path via configured recipe

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-008|normalize module|Create `src/superclaude/cli/swarm/normalize.py` as Wave 2 dispatcher: invoke configured Recipe per worker; atomic write to deterministic final path|COMP-008|COMP-014|module imports; normalize_all() iterates .raw files, applies recipe, writes final output|M|P0|
|2|COMP-014|recipes package|Create recipes package at `src/superclaude/cli/swarm/recipes/` with `__init__.py` exposing REGISTRY dict and Recipe Protocol; ship all recipe modules|COMP-014|DM-009|package imports; REGISTRY dict maps recipe name to Recipe instance|M|P0|
|3|COMP-027|bare_review_v1 recipe|Port t2_normalize.py logic to bare_review_v1.py recipe: normalize bare-review output shape|COMP-027|COMP-014|recipe normalizes raw worker output to expected findings + verdict structure|M|P0|
|4|COMP-028|findings_table_v1 recipe|Create findings_table_v1.py recipe: extracted shape for findings-table lenses|COMP-028|COMP-014|recipe parses raw into findings table format|S|P1|
|5|COMP-029|hypothesis_table_v1 recipe|Create hypothesis_table_v1.py recipe: hypothesis table output shape|COMP-029|COMP-014|recipe parses raw into hypothesis table format|S|P1|
|6|COMP-030|verdict_only_v1 recipe|Create verdict_only_v1.py recipe: verdict-only output shape|COMP-030|COMP-014|recipe extracts verdict from raw; discards non-verdict content|S|P1|
|7|COMP-031|passthrough recipe|Create passthrough.py recipe: returns raw body unchanged|COMP-031|COMP-014|recipe returns input as-is; metadata marks pass-through|S|P1|
|8|COMP-032|custom recipe (custom-py loader)|Create custom.py recipe: dynamic loader for custom-py:module:func|COMP-032|COMP-014|loads arbitrary module:func via importlib; raises on missing module or non-callable|S|P0|
|9|FR-029|Recipe Protocol invocation per worker|For each worker, invoke configured Recipe; atomic write to deterministic final path (IMM-6)|COMP-008|COMP-014|each .raw produces final output at deterministic path; written atomically|M|P0|
|10|FR-030|Parse-error salvage promotion|Promote parse_error → success if §7.4 salvage succeeds|COMP-008|COMP-014|salvage path tested; parse_error becomes success when salvage produces valid output|S|P0|
|11|AC-007|custom-py: dynamic loader|custom-py:<module>:<callable> is Python-only; non-Python harnesses use passthrough and post-process raw bodies|COMP-032|COMP-014|importlib.util.spec_from_file_location loads module; callable resolved; error on non-Python|M|P0|
|12|NFR-014|Idempotency on re-dispatch|Wave 2 re-runs over all .raw files; existing successes re-write deterministically (no-op outcome)|COMP-008|COMP-008|re-running normalize produces identical final files; checksums match|S|P0|
|13|NFR-006|Merge module LOC ceiling|Document merge module ≤30 LOC ceiling; explicit allowed/disallowed ops in docstring|COMP-015|—|merge.py body ≤30 LOC excluding imports + docstring; docstring lists allowed/disallowed|S|P0|
|14|FR-047|Atomic-write idempotency|Every output file written via write-to-tmp + os.replace + deterministic filename (IMM-6)|COMP-008|COMP-014|grep confirms os.replace used; no partial files after mid-write kill|S|P0|

### Integration Points — M5

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|COMP-014|Recipe registry|Yes|M5|M6 (reduce uses normalized outputs)|
|Final output files|Normalized worker output|Yes|M5|M6 (reduce, merge)|
|COMP-008|normalize dispatcher|Yes|M5|M6 (wave orchestration)|

### Milestone Dependencies — M5

- M4 (dispatch produces .raw + .meta.json files)

### Risk Assessment and Mitigation — M5

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Recipe parse failures on unexpected output shapes|Medium|Medium|Workers marked parse_error reduce success count|§7.4 salvage path; passthrough recipe as fallback|Architect|
|2|custom-py: loader security|High|Low|Arbitrary code execution via custom-py path|Document as trusted-input-only; no sandboxing in Phase 1|Architect|

## M6: Reduce + Merge (Wave 3)

**Objective:** Implement Wave 3: success-first status determination, three amalgamation modes, mechanical merge, return contract emission, done sentinel | **Duration:** Weeks 7–8 | **Entry:** M5 normalized outputs available | **Exit:** return-contract.yaml written, done.json sentinel emitted, exit 0

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-009|reduce module|Create `src/superclaude/cli/swarm/reduce.py` with status determination per IMM-5; resume merge regeneration; contract emission|COMP-009|COMP-015, COMP-010|module imports; reduce() consumes normalized outputs, writes contract|M|P0|
|2|FR-032|Success-first status determination|M==N → success; 2≤M<N → partial; M<2 → failed; M==N==2 → success; floor and success_first configurable (defaults floor=2, success_first=true)|COMP-009|—|parametrized test covers M==N, M==N==2, 2≤M<N, M<2; success_first ordering confirmed|S|P0|
|3|FR-033|Three amalgamation modes|Support raw (Wave 2 no-op), normalize (default, Recipe per worker), normalize+merge (normalize + mechanical concat)|COMP-009|COMP-015|raw skips Wave 2; normalize uses recipes; normalize+merge adds concat|M|P0|
|4|FR-034|Mechanical merge module|Create `src/superclaude/cli/swarm/merge.py`: ≤30 LOC; read each worker's final_path, strip frontmatter, prepend ## From {model_label} provenance header, concat in slot-index order; no reorder/dedup/scoring/claim-rewriting|COMP-015|COMP-008|merge body ≤30 LOC; provenance headers present; slot-index order preserved; no transformations|M|P0|
|5|FR-035|Merge edge cases|M=0 (failed): merged_path=null; M=1 (failed-by-floor): merged_path=null; M≥2: merged_path with only successful workers; --resume + normalize+merge: ALWAYS regenerate merged.md|COMP-009|COMP-015|M=0 → null merged_path; M=1 → null; M≥2 → populated; resume regenerates|S|P0|
|6|FR-036|Return contract emission|Write return-contract.yaml with contract_version, status, job_id, timing, target info, worker counts, output_files array, amalgamation_mode, merged_path, caller_metadata, recommended_next_command, artifacts paths|COMP-009|COMP-004|contract.yaml written atomically; all fields present per DM-003|M|P0|
|7|FR-037|Done sentinel emission|Write done.json sentinel atomically; emit final event; exit 0 (status lives in contract, not RC)|COMP-009|COMP-010, COMP-011|done.json written atomically after contract; final event in JSONL; exit 0|M|P0|
|8|FR-042|Crash semantics|Orchestrator crash mid-dispatch: .swarm-state.json retains last-known state; completed workers have .meta.json sidecars; no done.json|COMP-009|COMP-010|kill test confirms .swarm-state.json intact; no done.json; .meta.json present for completed workers|S|P0|
|9|FR-043|Resume workflow|Implement `swarm run --resume <job_id>`: re-run Wave 0 in resume mode; lens rehydration from manifest; skip success workers; re-dispatch remaining; re-run Wave 2; regenerate merged.md for normalize+merge; reduce + contract emit|COMP-009|COMP-006, COMP-007, COMP-008, COMP-015|resume skips completed workers; re-dispatches failures; merged.md regenerated; contract re-emitted|L|P0|
|10|FR-044|Manifest-as-source-of-truth|manifest.resolved_lens_entry is durable definition of "what this swarm was supposed to do"; --resume honors it; lens-registry mutations between runs do not affect resumed job|COMP-009|COMP-006|resume test confirms mutated registry ignored; manifest entry used verbatim|S|P0|
|11|FR-015|--force-relens flag|On --resume, ignore manifest's resolved_lens_entry and re-resolve from current registry|COMP-002|COMP-009|flag overrides manifest rehydration; re-resolves from current registry|S|P1|
|12|FR-013|--amalgamation-mode flag|Implement `swarm run --amalgamation-mode {raw,normalize,normalize+merge}` flag; default normalize|COMP-002|COMP-009|flag accepted; mode passed through to reduce; invalid value → validation error|S|P0|
|13|AC-009|No scored merge|Scored merging remains /sc:adversarial's job; normalize+merge is mechanical-concat-only|COMP-015|—|merge.py docstring explicitly disallows scoring/dedup/reorder; boundary test confirms|S|P0|

### Integration Points — M6

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|return-contract.yaml|Return contract|Yes|M6|All callers (skill, CLI, harness)|
|done.json|Terminal sentinel|Yes|M6|Monitoring (Bash run_in_background, Monitor tool)|
|merged.md|Merged output|Yes|M6|Downstream /sc:adversarial (for normalize+merge)|

### Milestone Dependencies — M6

- M5 (normalized outputs from all workers)

### Risk Assessment and Mitigation — M6

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Merge boundary erosion|High|Medium|normalize+merge drifts into judging via incremental PRs|Four structural guards: docstring allowed/disallowed + ≤30 LOC + PR-review note + boundary test + CI rule|Architect|
|2|Resume merge regeneration missed|Medium|Low|--resume + normalize+merge uses stale merged.md|INV-010 test: always regenerate merged.md after Wave 2 on resume|QA|

## M7: TUI + Detached + Monitoring

**Objective:** Create Rich Live TUI dashboard, detached mode lifecycle, and three monitoring caller patterns | **Duration:** Weeks 8–9 | **Entry:** M4 dispatch + M6 reduce emitting state + events | **Exit:** `swarm status --watch` refreshes every 1s; `swarm attach`/`kill` work; all three monitoring patterns demonstrated

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-012|TUI module|Create `src/superclaude/cli/swarm/tui.py` with Rich Live dashboard; flag-gated --tui (NOT default — INV-012)|COMP-012|COMP-010, COMP-011|module imports; Rich Live renders state + worker progress; non-TTY → no terminal control sequences|M|P1|
|2|FR-014|--tui flag|Implement `swarm run --tui` flag: opt-in Rich Live dashboard; non-TTY callers do not get terminal control sequences|COMP-002, COMP-012|COMP-012|flag enables TUI; non-TTY session → graceful fallback to text output|S|P1|
|3|FR-003|status CLI subcommand|Implement `swarm status [--watch]` subcommand: show job state (terminal or in-flight); watch mode refreshes every 1s via Rich-rendered status table|COMP-002|COMP-010, COMP-011|status shows current state; --watch refreshes every 1s; terminal state shows final summary|S|P0|
|4|FR-004|logs CLI subcommand|Implement `swarm logs` subcommand: tail or dump job's execution log|COMP-002|COMP-011|logs dumps execution-log.md; tail mode follows JSONL|S|P0|
|5|FR-005|attach CLI subcommand|Implement `swarm attach <job_id>` subcommand: re-attach to detached tmux job's TUI|COMP-002|COMP-013|attach re-attaches to tmux session by job_id; error if session not found|S|P1|
|6|FR-006|kill CLI subcommand|Implement `swarm kill <job_id>` subcommand: terminate running detached job|COMP-002|COMP-013|kill terminates tmux session; .swarm-state.json updated to terminal|S|P1|
|7|FR-007|scaffold CLI subcommand|Implement `swarm scaffold --lens <name>` subcommand: emit starter job-spec file for named lens|COMP-002|COMP-016|scaffold outputs valid YAML spec pre-filled with lens defaults|M|P1|
|8|FR-045|Three-layer observability|Provide .swarm-state.json (atomic on transition), execution-log.jsonl (append-only, lock-coordinated), execution-log.md (human log), done.json (terminal sentinel)|COMP-010, COMP-011|COMP-007|all 4 artifacts emitted; state transitions atomic; JSONL append-only|M|P0|
|9|FR-046|Three monitoring patterns|Support: (1) Bash run_in_background + until [ -f done.json ]; (2) Monitor tool tailing JSONL; (3) swarm status --watch|COMP-002|COMP-010, COMP-011, COMP-012|demo script shows all 3 patterns; each pattern detects job completion|S|P1|
|10|FR-048|Detached mode lifecycle|Support --detached via tmux wrapper; detached + --resume + swarm attach/kill lifecycle|COMP-013|COMP-001, COMP-007|detached job survives caller termination; resume re-attaches; kill terminates|L|P1|
|11|NFR-012|TUI opt-in|Rich Live dashboard NOT default; non-TTY callers do not receive terminal control sequences|COMP-012|—|default run produces no Rich control sequences; --tui enables|M|P1|
|12|COMP-011|logging_ module|Create `src/superclaude/cli/swarm/logging_.py` with dual JSONL + Markdown event log; lock-coordinated append|COMP-011|COMP-006|JSONL appends under Lock; Markdown log human-readable; both stay in sync|S|P0|
|13|NFR-004|Atomic-write durability|All output files atomically written; state transitions atomic; JSONL appends lock-coordinated; durable across crashes|COMP-010|COMP-011|mid-write kill test confirms no partial files; state file survives crash|M|P0|

### Integration Points — M7

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|COMP-012|TUI module|Yes|M7|swarm run --tui, swarm status --watch|
|COMP-011|logging_ module|Yes|M7|All monitoring patterns|
|.swarm-state.json|State artifact|Yes|M7|status, attach, kill|

### Milestone Dependencies — M7

- M3 (preflight produces state files)
- M4 (dispatch produces events)
- M6 (reduce produces terminal state + done.json)

### Risk Assessment and Mitigation — M7

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|tmux dependency for detached mode|Medium|Medium|Same risk as sprint — tmux not available on all systems|Detached mode is optional; inline mode is default; tmux absence detected at preflight|Architect|
|2|TUI terminal incompatibility|Low|Medium|Some terminals do not support Rich Live|Non-TTY detection at startup; fallback to text output|Architect|

## M8: Integration + Invariant Tests

**Objective:** End-to-end integration tests + all 9 invariant remediation acceptance tests (NFR-013) | **Duration:** Weeks 9–11 | **Entry:** M1–M7 modules functional | **Exit:** SC-001 through SC-016 all passing; full pipeline from `swarm run` to return-contract verified

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|SC-001|A/B parity test|swarm run --lens bare-review --target X --output Y --workers 3 produces return-contract.yaml byte-for-byte equivalent (modulo timestamps + checksums) to current sc-bare-review output|TEST-001|COMP-001, COMP-008, COMP-009|parity test passes; byte-for-byte match modulo timestamps|L|P0|
|2|SC-002|IMM-3 parallelism test|N stub workers complete within max(per_worker_elapsed) + ε, NOT Σ(per_worker_elapsed)|TEST-002|COMP-007|stub transport test confirms parallel execution timing|S|P0|
|3|SC-003|IMM-4 empty-target test|Target with <50 non-whitespace bytes triggers failed/target-too-small contract before any dispatch|TEST-003|COMP-006|49-byte target → failed contract; no dispatch events in log|S|P0|
|4|SC-004|IMM-5 status test|Parametrized status test covering M==N, M==N==2, 2≤M<N, M<2 cases with success_first=true ordering|TEST-004|COMP-009|all 4 cases produce correct status; M==N==2 → success|S|P0|
|5|SC-005|IMM-6 atomic-write test|Process killed during output write leaves no partial file at deterministic final path|TEST-005|COMP-008|kill during write → no file at final path; tmp file cleaned up|S|P0|
|6|SC-006|§11.5 injection test|Target text containing <<<END TARGET>>> literal does not allow injection past the delimiter|TEST-006|COMP-006|target with end-marker literal → delimiter escape blocked; no injection|M|P0|
|7|SC-007|INV-001 resume manifest test|--resume reads resolved_lens_entry from manifest, ignores mutated registry|TEST-007|COMP-006, COMP-009|mutated registry entry ignored; manifest entry used for resume|S|P0|
|8|SC-008|INV-002 Python-only test|No shell-script dispatch path exercised; all parallelism via Python ThreadPoolExecutor|TEST-008|COMP-007|grep + import audit confirms no shell dispatch; all via ParallelExecutor|S|P0|
|9|SC-009|INV-003 custom-prompt-dir test|--custom-prompt-dir without §11.5 substring STOPs with actionable error; with --auto-inject-guard prepends canonical sentence|TEST-009|COMP-006|without guard → STOP with error; with --auto-inject-guard → prepends sentence; passes|M|P0|
|10|SC-010|INV-010 resume merge test|--resume + normalize+merge always regenerates merged.md after Wave 2|TEST-010|COMP-009|resume test confirms merged.md regenerated even if unchanged|S|P0|
|11|SC-011|INV-014 escape-hatch parity test|Escape-hatch (custom-prompt-dir) path enforces injection guard identically to lens-driven and JSON-Schema paths|TEST-011|COMP-006|all 3 input paths produce identical guard behavior|S|P0|
|12|SC-012|Merge boundary test|3-worker concat produces all 3 sections in slot-index order with no transformations beyond provenance header; merge module body ≤30 LOC|TEST-012|COMP-015|3 provenance headers in slot order; no reordering/dedup/scoring; LOC ≤30|M|P0|
|13|SC-013|validate-lenses test|swarm validate-lenses returns exit 0 on bundled 8-entry registry; exit non-zero with diagnostics for: missing templates, unregistered recipes, suspect:true missing {suspect_files}, duplicate names, missing §11.5|TEST-013|COMP-017|5 violation types each trigger exit non-zero with correct diagnostic|S|P0|
|14|SC-015|Non-precluding contract audit|Zero references to Claude tool names in models.py, schema.py, result-contract YAML output, and CLI --help text|TEST-014|COMP-004, COMP-005, COMP-002|header-grep audit confirms zero Claude tool name references|S|P0|
|15|FR-050|Non-precluding contract surface|Job spec, result contract, CLI surface, monitoring contract have zero references to Claude tool names; caller.kind informational only; subprocess.run callable from any language|COMP-002, COMP-004|—|subprocess.run invocation works from Python script; YAML/JSON parseable|S|P1|
|16|FR-016|Exit code integration|Exit codes: 0 = Wave 3 reached; 2 = spec validation failure; 3 = preflight failure; 10 = orchestrator internal error — verified end-to-end|TEST-015|COMP-002, COMP-005, COMP-006, COMP-009|each error path returns correct RC in integration test|S|P0|
|17|NFR-013|Full invariant test suite|Every IMM-N + INV-NNN invariant has acceptance test: IMM-3/4/5/6, §11.5, INV-001/002/003/010/014, §10.2 boundary|TEST-016|All|all 10 invariant tests pass; coverage report confirms|M|P0|
|18|FR-048|Detached mode E2E|Long-running job survives caller-process termination; resumes via swarm run --resume; attaches via swarm attach; terminates via swarm kill|TEST-017|COMP-013, COMP-007, COMP-009|E2E demo confirms all 4 lifecycle operations succeed|L|P1|

### Integration Points — M8

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|TEST-001..TEST-017|Test suite|Yes|M8|CI gate before M9 migration|
|stub transport|Test double|Yes|M8|All invariant tests (no network)|

### Milestone Dependencies — M8

- M1 (data models)
- M2 (schema, lenses)
- M3 (preflight)
- M4 (dispatch)
- M5 (normalize)
- M6 (reduce)
- M7 (observability, TUI)

### Risk Assessment and Mitigation — M8

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|A/B parity test flakiness due to model response variance|High|Medium|SC-001 fails intermittently|Compare structural shape (section count, finding count) not byte-for-byte; allow timestamp/model-id variance|QA|
|2|Stub transport masks real transport bugs|Medium|Medium|Integration tests pass but real proxy fails|Run subset of tests against real T2 proxy in CI; stub for invariant tests only|QA|

## M9: sc-bare-review Migration

**Objective:** Rewrite sc-bare-review SKILL.md as ~60-line thin caller; A/B parity test; delete scripts/*.sh | **Duration:** Weeks 11–12 | **Entry:** M8 all tests passing; swarm CLI production-ready | **Exit:** sc-bare-review SKILL.md is ~60 lines; scripts/*.sh deleted; A/B parity observed across test window

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-033|Thin-caller SKILL.md|Rewrite sc-bare-review SKILL.md as ~60-line skill: builds --lens bare-review job spec, exec's superclaude swarm run, relays return contract|COMP-033|COMP-001|SKILL.md is ~60 lines; builds spec; exec's CLI; relays contract|S|P0|
|2|FR-049|sc-bare-review migration|Migrate sc-bare-review to thin caller calling --lens bare-review; A/B parity test against current bare-review output|COMP-033|COMP-001, COMP-008, COMP-009|A/B test passes; output shape matches pre-migration|M|P0|
|3|SC-016|Migration completeness|After migration, sc-bare-review SKILL.md is ~60 lines (vs current); all scripts/*.sh deleted; production parity observed across A/B test window|COMP-033|—|SKILL.md line count ~60; scripts/*.sh all deleted; A/B window passes|S|P0|
|4|NFR-009|Backward compat migration|--auto-inject-guard flag preserves existing --custom-prompt-dir callers during §11.5 substring enforcement rollout|COMP-002|COMP-006|existing custom-prompt-dir users work with --auto-inject-guard|S|P1|
|5|FR-001|swarm CLI group registration|Register swarm_group in superclaude CLI so `superclaude swarm` is available alongside `superclaude sprint` and `superclaude roadmap`|COMP-001|—|`superclaude swarm --help` shows subcommands; registered alongside sprint and roadmap|S|P0|
|6|FR-002|swarm run subcommand|Implement `swarm run <spec.yaml>` subcommand: execute swarm job from spec file, stdin, or --lens shortcut|COMP-002|COMP-006, COMP-007, COMP-008, COMP-009|run executes full Wave 0→1→2→3 pipeline; returns exit 0 on success|M|P0|
|7|NFR-007|Module layout mirrors sprint|Module shape mirrors src/superclaude/cli/sprint/ so operators familiar with sprint immediately understand swarm|All|—|directory structure comparison: same modules (commands, config, models, schema, preflight, dispatch, normalize, reduce, state, logging_, tui, tmux, recipes, lenses, transports, merge)|S|P1|
|8|AC-002|CLI as orchestrator home|ThreadPoolExecutor enforces parallelism in code where SKILL.md prose cannot; subprocess.run callability extends to non-Claude callers; durable observability + detached + resume are first-class|COMP-001|—|subprocess.run from external Python script successfully invokes swarm run|S|P1|

### Integration Points — M9

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|COMP-033|Thin-caller skill|Yes|M9|All existing sc-bare-review callers|
|return-contract.yaml|Return contract|Yes|M9|Thin caller relays to downstream|

### Milestone Dependencies — M9

- M8 (all integration + invariant tests passing)

### Risk Assessment and Mitigation — M9

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Migration risk — A/B parity failure|Medium|Medium|sc-bare-review output differs post-migration|A/B test window with structural comparison; fallback to old skill if parity not achieved|Architect|
|2|Existing --custom-prompt-dir users break|Medium|Low|Users need to add §11.5 sentence to system.txt|--auto-inject-guard flag for backward compatibility during migration window|Architect|

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By Milestone|Status|Fallback|
|---|---|---|---|
|httpx (Python HTTP client)|M4|External pip package|requests (refactor transport layer)|
|tmux (system binary)|M7|System dependency|Inline mode only — detached mode disabled if tmux absent|
|T2 proxy (external HTTP service)|M4, M8|External service (env: T2ProxyUrl, T2ProxyKey)|Stub transport for all tests; real proxy for integration subset|
|rich (Python TUI library)|M7|External pip package|Text output fallback for non-TTY|
|click (CLI framework)|M1|External pip package (already in deps)|None — core dependency|
|threading.Lock (Python stdlib)|M4, M7|Python stdlib|None|
|os.replace (Python stdlib)|M1, M5, M6|Python stdlib|None|
|Parent spec bare-review v1.3.0-draft|M1, M3, M5|Reference for invariants|None — invariants carry forward verbatim|
|/sc:adversarial downstream command|M6|Existing skill referenced|None — recommendation only, not auto-executed|
|sprint/tmux.py (internal sibling)|M7|Internal reference for pattern mirror|None — pattern copy, not runtime dependency|
|superclaude.execution.parallel.ParallelExecutor|M4|Internal module|None — mandated by AC-005|

### Infrastructure Requirements

- Python 3.10+ (per pyproject.toml)
- httpx package for Phase-1 reference transport
- rich package for TUI (opt-in)
- tmux system binary (optional, detached mode only)
- T2 proxy service available with T2ProxyUrl, T2ProxyKey, T2Model0N env vars
- CI environment capable of running pytest with stub transport (no network required for invariant tests)

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|Mitigation|Owner|
|----|------|---------------------|-------------|--------|------------|-------|
|R-001|Lens-registry sprawl|M2, M3|Medium|Medium|PR-review discipline requires real caller; entries without caller deferred to custom-py:|Architect|
|R-002|Merge boundary erosion|M5, M6, M8|Medium|High|Four structural guards: docstring allowed/disallowed + ≤30 LOC + PR-review note + boundary test + CI rule|Architect|
|R-003|Resume + lens-mutation interaction|M3, M6, M8|Medium|Medium|Default rehydrates from manifest.resolved_lens_entry; --force-relens opts into re-resolution|Architect|
|R-004|tmux dependency for detached mode|M4, M7, M8|Medium|Medium|Detached mode is optional; inline mode is default; tmux absence detected at preflight|Architect|
|R-005|ThreadPoolExecutor surprise|M4, M8|Low|Low|Documented in dispatch.py docstring; tested with stub transport|Architect|
|R-006|Custom-prompt-dir guard parity backward-compat|M3, M9|Medium|Medium|--auto-inject-guard flag for backward compatibility during migration window|Architect|
|R-007|Schema evolution drag|M2, M3|Low|Low|Orchestrator at 1.1 loads specs at 1.0; forward-compat best-effort|Architect|
|R-008|A/B parity test flakiness|M8, M9|Medium|High|Compare structural shape not byte-for-byte; allow timestamp/model-id variance|QA|
|R-009|T2 proxy flakiness|M4, M8|Medium|Medium|Stub transport for all invariant tests; real transport only for integration subset|QA|
|R-010|Data model field mismatch|M1, M2|Medium|High|Cross-reference every field against extraction DM-xxx definitions; add field-count assertions in tests|Architect|
|R-011|Custom-py: loader security|M5|Low|High|Document as trusted-input-only; no sandboxing in Phase 1|Architect|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|Milestone|
|---|---|---|---|---|
|SC-001: A/B parity|Byte-for-byte equivalent contract (modulo timestamps)|100% match|Integration test with real target|M8|
|SC-002: IMM-3 parallelism|N workers in max(per_worker) + ε|< 1.5× max elapsed|Stub transport timing test|M8|
|SC-003: IMM-4 empty-target|<50 non-whitespace bytes → failed|Contract written before dispatch|Unit test with 49-byte target|M8|
|SC-004: IMM-5 status|Correct status for M==N, M==N==2, 2≤M<N, M<2|4/4 cases pass|Parametrized pytest|M8|
|SC-005: IMM-6 atomic-write|No partial file after mid-write kill|0 partial files|Kill test during write|M8|
|SC-006: §11.5 injection|End-marker literal in target blocked|No injection past delimiter|Unit test with crafted target|M8|
|SC-007: INV-001 resume|Manifest lens used on resume|Registry mutation ignored|Resume test with mutated registry|M8|
|SC-008: INV-002 Python-only|No shell dispatch path|0 shell dispatch imports|Import audit + grep|M8|
|SC-009: INV-003 custom-prompt-dir|§11.5 guard enforced identically|3 input paths match behavior|Unit test per path|M8|
|SC-010: INV-010 resume merge|merged.md regenerated on resume|Always regenerated|Resume test with normalize+merge|M8|
|SC-011: INV-014 escape-hatch|Guard parity across all paths|Identical behavior|Parity test across 3 paths|M8|
|SC-012: Merge boundary|Mechanical concat only, ≤30 LOC|3 sections in slot order; LOC ≤30|Boundary test + LOC count|M8|
|SC-013: validate-lenses|5 violation types detected|Exit non-zero for each|Unit test per violation type|M8|
|SC-014: Detached mode E2E|All 4 lifecycle operations succeed|survive, resume, attach, kill|End-to-end demo|M8|
|SC-015: Non-precluding contract|Zero Claude tool name references|0 references in audit|Header-grep audit of models.py, schema.py, contract, --help|M8|
|SC-016: Migration completeness|SKILL.md ~60 lines, scripts/*.sh deleted|Line count ~60; 0 .sh files|File audit + A/B parity|M9|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|----------|--------|------------------------|----------|
|Dispatch mechanism|ThreadPoolExecutor via ParallelExecutor|Shell script dispatch, asyncio, multiprocessing|AC-005 mandates ParallelExecutor; eliminates dual-writer races (INV-002); code-enforced parallelism (NFR-001); simpler than multiprocessing for I/O-bound workers|
|Lens registry format|Bundled Python dataclasses|Separate plugin system, YAML config files|AC-003 mandates bundled inside CLI package; dataclasses enable type safety, PR-review validation, import-time loading|
|Merge strategy|Mechanical concat only|Scored merge, dedup, reordering|AC-009: scored merging is /sc:adversarial's job; mechanical concat preserves PR-review boundary; ≤30 LOC enforces discipline (NFR-006)|
|TUI default|Opt-in (--tui flag)|Default TUI, always-on|NFR-012: non-TTY callers must not receive terminal control sequences; opt-in avoids breaking automated callers|
|Resume lens source|Manifest-as-source-of-truth|Always re-resolve from current registry|INV-001/INV-016: lens mutations between runs must not affect resumed jobs; manifest snapshot is durable definition of intent|
|Transport protocol|Pluggable with OpenAI-compatible reference|Anthropic-specific, custom protocol|AC-011: workers route only to T2-proxy-compatible external models; pluggable design supports future transports without orchestrator changes|

## Timeline Estimates

|Milestone|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1|Weeks 1–2|Week 1|Week 2|All DM-xxx dataclasses defined; COMP-xxx module stubs import; REGISTRY dicts typed|
|M2|Weeks 2–3|Week 2|Week 3|JSON Schema validates JobSpec; 8 lens entries registered; validate-lenses catches violations|
|M3|Weeks 3–4|Week 3|Week 4|Preflight produces manifest.json + .swarm-state.json; IMM-4 guard working|
|M4|Weeks 4–6|Week 4|Week 6|N workers dispatched in parallel; .raw + .meta.json sidecars written; event log populated|
|M5|Weeks 6–7|Week 6|Week 7|Recipe Protocol invoked per worker; normalized outputs at deterministic paths|
|M6|Weeks 7–8|Week 7|Week 8|return-contract.yaml written; done.json emitted; resume workflow functional|
|M7|Weeks 8–9|Week 8|Week 9|TUI dashboard operational; attach/kill working; 3 monitoring patterns demonstrated|
|M8|Weeks 9–11|Week 9|Week 11|SC-001 through SC-016 passing; full pipeline integration verified|
|M9|Weeks 11–12|Week 11|Week 12|sc-bare-review migrated to thin caller; scripts/*.sh deleted; A/B parity confirmed|

**Total estimated duration:** 12 weeks
