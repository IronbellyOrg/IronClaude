---
spec_source: merged-requirements.compressed.md
complexity_score: 0.82
complexity_class: HIGH
primary_persona: architect
adversarial: false
base_variant: none
variant_scores: none
convergence_score: none
---

# MultiModelSwarm Orchestrator — Project Roadmap

## Executive Summary

Build `superclaude swarm` — a Python CLI orchestrator that dispatches parallel AI model calls through a lens/recipe system with code-enforced ThreadPoolExecutor parallelism, deterministic observability, crash-resume capability, and a mechanical merge pipeline. The system replaces shell-script dispatch (INV-002) with a Python-native architecture at `src/superclaude/cli/swarm/`, shipping with 8 bundled lenses, 5+ recipes, and 3 amalgamation modes. Four inherited invariants (IMM-N) and six new remediations (INV-N) govern all execution paths.

**Business Impact:** Enables true multi-model parallel review (3.5x+ speedup vs sequential), unifies all T2 skill callers under a single CLI surface with durable observability, crash-resume, and a future-harness-compatible contract (no Claude tool-name references).

**Complexity:** HIGH (0.82) — 56 functional requirements, 14 non-functional requirements, 34 components, 10 data models, 4 structural invariants, 3 prompt-input paths requiring uniform §11.5 enforcement, lock-coordinated concurrent state transitions, and a migration gate from legacy shell dispatch.

**Critical path:** Module layout + data models (M1) → JSON Schema + lens registry (M1) → state/logging infra (M2) → Wave 0 preflight (M2) → Wave 1 dispatch via ThreadPoolExecutor (M2) → Wave 2 normalize + recipe protocol (M2) → Wave 3 reduce + mechanical merge (M2) → return contract + observability (M3) → CLI surface (M3) → sc-bare-review migration + A/B parity (M4) → validation gates + release (M5).

**Key architectural decisions:**

- Python ThreadPoolExecutor (not attention-mediated) as single ParallelGroup for true-parallel dispatch (IMM-3, INV-002)
- Lens registry as bundled policy layer with manifest snapshot as durable resume source-of-truth (INV-001, INV-016)
- Mechanical merge ≤30 LOC, concat-only, no scoring/dedup/reorder — protected by four structural guards (§10.2)
- Transport Protocol with openai_compat (httpx) + stub; env-driven proxy routing via T2ProxyUrl/T2ProxyKey
- Module layout mirrors `cli/sprint/` for operator familiarity (NFR-MAINT-001)

**Open risks requiring resolution before M1:**

- OQ-007: Workers > configured T2Models guard — adopt V1 warn-on-exceed (recommended) or V2 STOP; blocks dispatch pool sizing logic
- OQ-008: Empty-pool failure path — define `failed`/`env-missing` contract shape; blocks Wave 0 preflight error handling
- OQ-010: `refs/templates/<lens>-output.md` location — determine whether templates live under `cli/swarm/refs/templates/` or a shared refs root; blocks lens entry path resolution

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|----|-------|------|----------|--------|--------------|--------------|------|
|M1|Foundation and Module Setup|Foundation|P0|High|None|30|Medium|
|M2|Execution Waves and Dispatch|Core Engine|P0|High|M1|30|High|
|M3|Observability and CLI Surface|Integration|P0|Medium|M2|28|Medium|
|M4|Migration and A/B Parity|Migration|P1|Medium|M2, M3|20|High|
|M5|Validation and Release Gates|Release|P0|Medium|M3, M4|18|Low|

## Dependency Graph

```
M1 (Foundation)
 ├── COMP-001 swarm_group, COMP-003 config, COMP-004 models
 ├── COMP-005 schema, DM-001..DM-008
 ├── COMP-022 lenses, DM-001 LensEntry, COMP-024..COMP-030 (8 lenses)
 ├── COMP-015 recipes, COMP-016..COMP-021 (6 recipes)
 ├── COMP-031 transports, COMP-032 openai_compat, COMP-033 stub
 └── NFR-MAINT-001 module layout, NFR-COMPAT-002 forward-compat
        │
        ▼
M2 (Execution Waves)
 ├── COMP-011 state, COMP-012 logging_, DM-006 SwarmState, DM-007 EventRecord
 ├── COMP-006 preflight → Wave 0 (IMM-4, FR-INJ-*, FR-SPEC-*)
 ├── COMP-034 ParallelExecutor, COMP-007 dispatch → Wave 1 (IMM-3, NFR-PERF-*)
 ├── COMP-008 normalize → Wave 2 (FR-REC-*)
 ├── COMP-009 reduce, COMP-010 merge → Wave 3 (FR-MERGE-*, IMM-5, IMM-6)
 └── OQ-007, OQ-008 resolution
        │
        ▼
M3 (Observability + CLI)
 ├── DM-005 ResultContract, FR-OBS-*, NFR-OBS-001, NFR-REL-*
 ├── COMP-002 commands (all 8 subcommands)
 ├── COMP-013 tui, COMP-014 tmux, FR-RES-*, NFR-SEC-*
 └── OQ-006 resolution
        │
        ▼
M4 (Migration + A/B Parity)
 ├── FR-MIG-*, sc-bare-review thin caller, script deletion
 ├── SC-008 A/B parity gate, SC-012 script cleanup
 └── OQ-009 caller_metadata.suspect override semantics
        │
        ▼
M5 (Validation + Release)
 ├── SC-001..SC-007, SC-009..SC-011 acceptance tests
 ├── FR-CLI-003 exit codes, FR-CLI-005 validate
 └── OQ-001 pre-commit wiring, OQ-004 Prometheus deferred
```

## M1: Foundation and Module Setup

**Objective:** Create module layout mirroring `cli/sprint/`, define all data models + JSON Schema, create lens registry (8 entries) + validator, create recipe protocol (6 recipes), create transport layer (Protocol + openai_compat + stub) | **Duration:** Weeks 1–2 | **Entry:** Requirements extraction approved | **Exit:** All 30 foundation deliverables pass unit tests; `swarm validate-lenses` exits 0 over bundled registry

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|NFR-MAINT-001|Module layout mirrors sprint|Create `src/superclaude/cli/swarm/` package layout mirroring `cli/sprint/` structure|COMP-001|—|Directory tree created; `__init__.py` with Click group stub; imports resolve|S|P0|
|2|COMP-001|swarm_group Click entry|Top-level Click group `superclaude swarm` entry point in `__init__.py`|COMP-001|NFR-MAINT-001|`superclaude swarm --help` shows 8 subcommand placeholders; exit 0|S|P0|
|3|COMP-003|SwarmConfig dataclass|Config dataclass with path resolution for output dir, state dir, log dir|COMP-003|NFR-MAINT-001|SwarmConfig(output_dir=…); resolves absolute paths; defaults sensible|M|P0|
|4|COMP-004|Core data models|JobSpec, WorkerSpec, ResultContract, WorkerResult, SwarmState, EventRecord dataclasses|COMP-004|COMP-003|All 6 dataclasses importable; frozen where appropriate; type hints complete|M|P0|
|5|DM-001|LensEntry frozen dataclass|Lens definition: name:str; description:str; system_prompt_fragment:str; user_template:str; output_template_path:str\|None; recipe_name:str; default_workers:int; default_target_line_cap:int; suspect:bool; tier:str; recommended_next_command_template:str; acceptance_notes:str; stability:Literal["stable","experimental"]|DM-001|COMP-004|All 13 fields present; frozen=True; defaults: stability="experimental"|S|P0|
|6|DM-002|JobSpec dataclass|Job spec model: spec_version; job_id; created; caller; lens; custom_prompt_dir; workers; transport; prompt; target; normalization; output; amalgamation_mode; status_policy; recommended_next_command_template; recommended_next_command_substitutions; runtime|DM-002|COMP-004|All 17 fields present; spec_version defaults "1.0"; job_id auto-generated pattern|S|P0|
|7|DM-003|WorkerSpec dataclass|Worker config: model_id; model_label; timeout_sec; temperature; retry_policy{on_5xx:1; on_5xx_backoff_sec:2; on_4xx:0; on_timeout:0}|DM-003|COMP-004|All fields present; defaults: timeout_sec=180; temperature=0.2; retry defaults match spec|S|P0|
|8|DM-004|WorkerResult dataclass|Worker outcome: index; path; raw_path; meta_path; model_id; model_label; bytes; status∈{success,timeout,parse_error,proxy_error}; http_code; attempts; elapsed_ms|DM-004|COMP-004|All 12 fields present; status is Literal enum|S|P0|
|9|DM-005|ResultContract dataclass|Return contract: contract_version="1.0"; status∈{success,partial,failed}; job_id; started; finished; elapsed_ms; caller; lens; lens_source; target{path,checksum,truncated,truncation_line_cap}; workers_requested; workers_succeeded; workers_failed; output_files; amalgamation_mode; merged_path; caller_metadata{suspect,tier}; recommended_next_command; artifacts{manifest_path,state_path,event_log_jsonl,event_log_md,done_sentinel}|DM-005|COMP-004|All 22 fields present; nested dataclasses for target/caller_metadata/artifacts|S|P0|
|10|DM-006|SwarmState dataclass|State file payload: state∈{preflight_ok,dispatching,normalizing,reducing,done,failed}; job_id; last_event timestamp|DM-006|COMP-004|All 3 fields present; state is Literal enum|S|P0|
|11|DM-007|EventRecord dataclass|JSONL event row: event_type; timestamp; worker_index; payload(dict)|DM-007|COMP-004|All 4 fields present; event_type is Literal enum|S|P0|
|12|DM-008|Manifest snapshot|Durable manifest.json: contract_version="1.0"; job_id; resolved_lens_entry(LensEntry snapshot)|DM-008|DM-001, DM-002|JSON serializable; round-trip via yaml/json; lens_entry matches LensEntry schema|S|P0|
|13|DM-009|Worker meta sidecar|Per-worker .meta.json: status; http_code; attempts; elapsed_ms; model_id; model_label|DM-009|DM-004|Written atomically alongside .raw; JSON schema matches WorkerResult subset|S|P0|
|14|DM-010|Done sentinel|Terminal done.json: timestamp; job_id; terminal_status|DM-010|DM-006|Written atomically; absent = incomplete (NFR-REL-003)|S|P0|
|15|COMP-005|JSON Schema + validators|JSON Schema for JobSpec with cross-field validators + §11.5 required-substring rule on prompt.system|COMP-005|COMP-004, DM-002|Valid spec passes; invalid spec rejected with actionable error; §11.5 substring enforced|M|P0|
|16|FR-SPEC-001|Spec version 1.0 + validators|JSON Schema-validated job spec with spec_version "1.0" and cross-field validators|COMP-005|COMP-005|FR-SPEC-001 AC: schema loads; v1.0 validates; cross-field validators fire|M|P0|
|17|FR-SPEC-002|Top-level job spec fields|All 17 top-level fields defined with correct types and defaults|COMP-005|DM-002|Every field from spec present in schema; job_id auto-format `<ISO>-<lens>-<hash>`|S|P0|
|18|FR-SPEC-003|Workers block schema|count≥floor; models list; timeout_sec=180; temperature=0.2; retry policy defaults|COMP-005|DM-003|Schema validates workers block; rejects count<floor; defaults applied|M|P0|
|19|FR-SPEC-004|Transport block schema|kind: openai_compat; base_url_env: T2ProxyUrl; api_key_env: T2ProxyKey|COMP-005|COMP-005|Schema validates transport block; env var names correct|S|P0|
|20|FR-SPEC-005|Target block schema|kind∈{file,inline_text,inline_bytes_b64}; path; truncation{line_cap:4000; byte_floor:50}; delimiters; injection_guard{enabled:true; required_substring}|COMP-005|COMP-005|Schema validates all target kinds; delimiter defaults correct; injection_guard defaults true|M|P0|
|21|FR-SPEC-006|Status policy schema|floor=2; success_first=true; partial_threshold=null defaults|COMP-005|COMP-005|Schema validates; defaults match spec|S|P0|
|22|FR-SPEC-007|Runtime schema|mode∈{inline,detached}; log_level; on_completion{write_done_sentinel:true; print_contract_to_stdout:true}|COMP-005|COMP-005|Schema validates; defaults match spec|S|P0|
|23|COMP-022|Lens registry module|LENSES dict + LensEntry dataclass + lookup helpers in `cli/swarm/lenses/__init__.py`|COMP-022|DM-001|LENSES dict importable; lookup by name returns LensEntry; case-insensitive match|S|P0|
|24|FR-LENS-001|Bundled lens registry|Python module at `src/superclaude/cli/swarm/lenses/` as open-class via plain dict|COMP-022|COMP-022|Module importable; LENSES dict has 8 entries; extensible via dict mutation|M|P0|
|25|FR-LENS-002|LensEntry field contract|13 fields per DM-001 with correct types and defaults|COMP-022|DM-001|All fields match spec; stability default "experimental"; frozen=True|S|P0|
|26|FR-LENS-003|8 initial lens entries|bare_review(stable); refactor_find; edge_case_hunt(4w); spec_completeness; feasibility_probe; troubleshoot_hypothesis(4w); doc_completeness; custom|COMP-022|FR-LENS-002|8 entries in LENSES dict; bare_review stability="stable"; others "experimental"; default_workers/tier set per spec|M|P0|
|27|COMP-024|bare_review lens|Stable lens: suspect=true; tier=T2; recipe=bare_review_v1; next-cmd template references {suspect_files}|COMP-024|COMP-022|Entry matches spec; stability="stable"; suspect=true; tier="T2"|S|P0|
|28|COMP-025|refactor_find lens|Experimental lens; tier T2-code; recipe=refactor_find|COMP-025|COMP-022|Entry present; stability="experimental"; tier correct|S|P1|
|29|COMP-026|edge_case_hunt lens|Experimental lens; tier T2-edge; default_workers=4|COMP-026|COMP-022|Entry present; default_workers=4; tier correct|S|P1|
|30|COMP-027|spec_completeness lens|Experimental lens; tier T2-spec|COMP-027|COMP-022|Entry present; tier correct|S|P1|
|31|COMP-028|feasibility_probe lens|Experimental lens; tier T2-feas|COMP-028|COMP-022|Entry present; tier correct|S|P1|
|32|COMP-029|troubleshoot_hypothesis lens|Experimental lens; tier T2-tshoot; default_workers=4|COMP-029|COMP-022|Entry present; default_workers=4; tier correct|S|P1|
|33|COMP-030|doc_completeness lens|Experimental lens; tier T2-doc|COMP-030|COMP-022|Entry present; tier correct|S|P1|
|34|COMP-023|Lens validator|_validate.py: file refs resolve; recipe resolution(incl custom-py:); suspect→{suspect_files} coupling; name uniqueness; §11.5 substring|COMP-023|COMP-022, COMP-015|Validator exits 0 on clean registry; exits 2 on missing ref/duplicate name/missing §11.5|M|P0|
|35|FR-LENS-006|validate-lenses subcommand|`swarm validate-lenses`: runs _validate.py over bundled registry|COMP-023|COMP-023|Exit 0 on clean; actionable errors on violations; wired to commands.py|S|P0|
|36|COMP-015|Recipe Protocol + REGISTRY|Open-class protocol with REGISTRY dict; `custom-py:module:func` dynamic loader via importlib|COMP-015|COMP-004|REGISTRY dict importable; resolve(name) returns recipe; custom-py: loader uses importlib|M|P0|
|37|FR-REC-001|Recipe protocol open-class|REGISTRY dict + custom-py dynamic loader|COMP-015|COMP-015|Protocol interface defined; custom-py: loader resolves module:func at runtime|M|P0|
|38|FR-REC-002|6 bundled recipes|bare_review_v1; findings_table_v1; hypothesis_table_v1; verdict_only_v1; passthrough; custom.py|COMP-015|COMP-015|All 6 recipes in REGISTRY; each callable with (raw_text, worker_meta) signature|M|P0|
|39|COMP-016|bare_review_v1 recipe|Ports t2_normalize.py logic into recipe format|COMP-016|COMP-015|Produces same output shape as legacy t2_normalize.py on identical input|M|P0|
|40|COMP-017|findings_table_v1 recipe|Findings-table normalizer shape|COMP-017|COMP-015|Parses findings from raw text; outputs structured table|M|P1|
|41|COMP-018|hypothesis_table_v1 recipe|Hypothesis-table normalizer|COMP-018|COMP-015|Parses hypotheses from raw text; outputs structured table|M|P1|
|42|COMP-019|verdict_only_v1 recipe|Verdict-only normalizer|COMP-019|COMP-015|Extracts verdict from raw text; minimal output|M|P1|
|43|COMP-020|passthrough recipe|Pass-through recipe for raw mode (no transformation)|COMP-020|COMP-015|Returns input text unchanged; used for amalgamation_mode=raw|S|P0|
|44|COMP-021|custom recipe loader|`custom-py:module:func` dynamic loader via importlib|COMP-021|COMP-015|Resolves arbitrary module:func at runtime; errors actionable|S|P0|
|45|COMP-031|Transport Protocol|Protocol definition for transport layer (send/receive)|COMP-031|COMP-004|Protocol class with send(system, user, config)→raw_text + meta signature|S|P0|
|46|COMP-032|openai_compat transport|httpx-based reference transport; env-driven T2ProxyUrl/T2ProxyKey/T2Model0N|COMP-032|COMP-031, NFR-SEC-005|httpx POST to proxy; reads env vars; returns (text, meta); no Anthropic routing|M|P0|
|47|COMP-033|stub transport|Deterministic stub for tests|COMP-033|COMP-031|Returns fixed response; configurable delay; no network calls|S|P0|
|48|FR-INJ-002|§11.5 substring in JSON Schema|Canonical §11.5 data-vs-instructions substring as required-substring on prompt.system via JSON Schema|COMP-005|COMP-005|Schema rejects system prompt without §11.5 substring; accepts with it|S|P0|
|49|FR-INJ-003|Lens registry §11.5 enforcement|Lens validator enforces §11.5 substring in every system_prompt_fragment at PR/CI time|COMP-023|FR-LENS-006|Validator rejects lens entries missing §11.5 substring|M|P0|
|50|NFR-COMPAT-001|Future-harness contract|Zero Claude tool-name references in job spec / result contract / CLI / monitoring surface|COMP-004, COMP-005|DM-002, DM-005|Grep for "tool|Tool" in schema/models yields zero Claude-specific matches|S|P0|
|51|NFR-COMPAT-002|Forward-compat spec loading|Spec version 1.1 orchestrator loads 1.0 specs (forward-compat best-effort)|COMP-005|FR-SPEC-001|Orchestrator at v1.1 accepts v1.0 spec without error|S|P1|
|52|OQ-010|Output template location|Determine whether `refs/templates/<lens>-output.md` lives under `cli/swarm/refs/templates/` or shared refs root|—|—|Decision documented; paths in lens entries resolve to actual files|M|P0|
|53|OQ-007|Workers > T2Models guard|Adopt V1 warn-on-exceed (recommended) or V2 STOP for workers exceeding configured model count|—|—|Decision documented; dispatch.py implements chosen behavior|M|P0|
|54|OQ-008|Empty-pool failure path|Define failed/env-missing contract when output dir is creatable; pre-output-dir abort otherwise|—|—|Decision documented; preflight.py implements both paths|M|P0|

### Integration Points — M1

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|LENSES dict|Registry|M1 complete|M1|preflight.py (M2), _validate.py (M1)|
|Recipe REGISTRY dict|Registry|M1 complete|M1|normalize.py (M2)|
|JSON Schema|Validation|M1 complete|M1|preflight.py (M2), validate subcommand (M3)|
|Transport Protocol|Interface|M1 complete|M1|dispatch.py (M2)|
|SwarmConfig|Config|M1 complete|M1|All commands (M3)|
|Data models (DM-001..DM-008)|Data contracts|M1 complete|M1|All modules (M2–M5)|
|LensEntry.stability field|Policy|M1 complete|M1|lens validator (M1), preflight (M2)|
|§11.5 canonical substring|Security policy|M1 complete|M1|JSON Schema (M1), lens validator (M1), preflight (M2)|

### Milestone Dependencies — M1

- None (foundation milestone)

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-007|Workers > configured T2Models guard — adopt V1 warn-on-exceed or V2 STOP?|Blocks dispatch pool sizing validation logic|Architect|End of M1|
|2|OQ-008|Empty-pool failure path — define failed/env-missing contract shape?|Blocks Wave 0 preflight error handling|Architect|End of M1|
|3|OQ-010|Output template location — cli/swarm/refs/templates/ vs shared refs root?|Blocks lens entry path resolution and file reference validation|Architect|End of M1|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R001 Lens-registry sprawl|Medium|Medium|Speculative lenses inflate registry without callers|PR-review discipline: require real caller; custom-py: + caller-side prompts for exploratory work|Architect|
|2|R003 Resume + lens-mutation interaction|Medium|Medium|Registry mutation between runs changes resume behavior silently|Manifest snapshot (DM-008) as durable source; --force-relens opt-in; test both paths|Architect|
|3|R007 Schema evolution drag|Low|Low|Forward-compat from spec 1.0→1.1 becomes maintenance burden|Forward-compat best-effort policy; defer 1.1 until real need|Architect|

## M2: Execution Waves and Dispatch

**Objective:** Create state management, logging, Wave 0 preflight, Wave 1 parallel dispatch (ThreadPoolExecutor), Wave 2 normalize (Recipe Protocol), Wave 3 reduce + mechanical merge | **Duration:** Weeks 3–4 | **Entry:** M1 exit criteria met; OQ-007, OQ-008, OQ-010 resolved | **Exit:** Full 4-wave execution cycle completes end-to-end with stub transport; all invariants (IMM-N) pass unit tests

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|55|COMP-011|State management|`.swarm-state.json` atomic read/write via tmp + os.replace|COMP-011|DM-006|Write is atomic; concurrent reads see consistent state; state transitions follow enum|M|P0|
|56|NFR-REL-002|Atomic state transitions|State file transitions atomic on every transition|COMP-011|COMP-011|Every state change writes atomically; no partial writes visible|S|P0|
|57|NFR-REL-001|Atomic file writes|All output files via tmp + os.replace (IMM-6)|COMP-011|COMP-011|No output file written directly; all via tmp + os.replace pattern|S|P0|
|58|IMM-6|Atomic-write idempotency|Every output file via write-to-tmp + os.replace + deterministic filename|COMP-011|NFR-REL-01|Deterministic filenames; idempotent re-runs produce same file content|M|P0|
|59|COMP-012|Dual logging system|JSONL append-only event log + Markdown human-readable log; threading.Lock-coordinated|COMP-012|DM-007|JSONL appends are lock-coordinated; Markdown log mirrors events; no interleaving|M|P0|
|60|FR-OBS-003|JSONL event log|Append-only, lock-coordinated (threading.Lock) execution-log.jsonl|COMP-012|COMP-012|Lock acquired per-append; file handles closed properly; events ordered by timestamp|M|P0|
|61|FR-OBS-004|Markdown human log|Dual human-readable execution-log.md|COMP-012|COMP-012|Readable format; mirrors JSONL events; timestamp + worker_index + event_type|M|P0|
|62|DM-006|SwarmState persistence|`.swarm-state.json` payload: state; job_id; last_event timestamp|COMP-011|DM-006, COMP-011|Read/write round-trip preserves all fields; last_event updated on transition|S|P0|
|63|DM-007|EventRecord serialization|JSONL event row: event_type; timestamp; worker_index; payload|COMP-012|DM-007|Each row is valid JSON; all 4 fields present; event_type from Literal enum|S|P0|
|64|FR-OBS-002|Atomic state file|`.swarm-state.json` written atomically on every state transition|COMP-011|NFR-REL-02|Observed: no partial state file on crash mid-write|S|P0|
|65|COMP-006|Wave 0 preflight|Validate job spec; resolve lens against registry; materialize resolved_lens_entry; resolve env vars; read+truncate target; checksum; IMM-4 guard; build prompts with delimiters; emit manifest.json + .swarm-state.json|COMP-006|COMP-005, COMP-022, COMP-011, COMP-012|Valid spec → preflight_ok state; invalid spec → exit 2; IMM-4 triggers on <50 bytes; manifest.json written atomically; state=preflight_ok|XL|P0|
|66|FR-EXEC-W0|Wave 0 preflight execution|Full Wave 0: spec validation, lens resolution, env resolution, target read+truncate, checksum, IMM-4 guard, prompt build, manifest + state emit|COMP-006|COMP-006|End-to-end preflight succeeds with valid spec; exits 2 on invalid spec; state=preflight_ok|XL|P0|
|67|IMM-4|Empty-target guard|Target with <50 non-whitespace bytes after truncation → write failed/target-too-small contract and STOP before any dispatch|COMP-006|FR-EXEC-W0|Target <50 bytes → contract written; no dispatch occurs; configurable via target.truncation.byte_floor|S|P0|
|68|FR-INJ-001|Target delimiters|Wrap target in `<<<TARGET>>>` / `<<<END TARGET>>>` delimiters before dispatch|COMP-006|FR-EXEC-W0|Prompt user text contains `<<<TARGET>` at start and `<<<END TARGET>>>` at end of target content|S|P0|
|69|FR-INJ-004|Custom-prompt-dir preflight|`--custom-prompt-dir` preflight performs substring check on system.txt identical to lens-driven and JSON-Schema paths; STOP on absence with actionable error|COMP-006|FR-EXEC-W0|Missing §11.5 in system.txt → actionable error + STOP; present → proceeds|S|P0|
|70|INV-014|Escape-hatch guard parity|`--custom-prompt-dir` path validates §11.5 identically to other prompt-input paths|COMP-006|FR-INJ-004|Same validation logic across all 3 paths; no path-specific exceptions|M|P0|
|71|FR-INJ-005|Auto-inject-guard flag|`--auto-inject-guard` opts into auto-prepending canonical §11.5 sentence for backward compat|COMP-006|FR-INJ-004|Flag present → §11.5 prepended to system.txt if missing; flag absent → error on missing|M|P0|
|72|INV-002|Python ThreadPoolExecutor dispatch|httpx called directly via ThreadPoolExecutor end-to-end; shell dispatch retired; PIPE_BUF deprecated|COMP-007|INV-002|No shell script dispatch; all HTTP via Python ThreadPoolExecutor; no PIPE_BUF assumptions|M|P0|
|73|COMP-034|ParallelExecutor wrapper|Shared ThreadPoolExecutor wrapper from `superclaude.execution.parallel.ParallelExecutor`|COMP-034|COMP-007|ParallelExecutor accepts tasks; executes in pool; returns results; thread-safe|M|P0|
|74|COMP-007|Wave 1 dispatch|httpx ThreadPoolExecutor via ParallelExecutor; one task per worker in one ParallelGroup; per-worker hard timeout; retry-once-on-5xx; always-record; events worker_start/worker_progress/worker_done|COMP-007|COMP-034, COMP-011, COMP-012, COMP-032|N workers → N parallel tasks; each writes .raw + .meta.json; timeout enforced; 5xx retried once; events emitted|M|P0|
|75|FR-EXEC-W1|Wave 1 parallel dispatch|ParallelExecutor one task per worker in one ParallelGroup; each httpx POST → write .raw + .meta.json sidecar; hard timeout; retry-once-on-5xx; always-record; events|COMP-007|COMP-007|All workers dispatched concurrently; raw + meta files written; timeout kills worker; 5xx retried; events logged|XL|P0|
|76|IMM-3|True-parallel dispatch|Single ThreadPoolExecutor + single ParallelGroup; parallelism is code-enforced (not attention-mediated)|COMP-007|FR-EXEC-W1|Code inspection: one ThreadPoolExecutor; one ParallelGroup; N concurrent HTTP calls; no sequential fallback|M|P0|
|77|NFR-PERF-001|Per-worker timeout + retry|Per-worker hard timeout 180s; retry-once-on-5xx with 2s backoff; 0 retries on 4xx/timeout|COMP-007|FR-EXEC-W1|Timeout=180s enforced; 5xx retried once with 2s delay; 4xx not retried; timeout not retried|S|P0|
|78|NFR-PERF-002|Single ParallelGroup|N parallel HTTP calls within one Python process, not sequential|COMP-007|IMM-3|Wall-clock for N workers ≈ max(individual times), not sum; verified with stub transport|S|P0|
|79|NFR-SEC-001|JSON payload transport|Target content passed as JSON payload via json.dumps (never shell-interpolated)|COMP-032|COMP-007|httpx POST body is json.dumps(...); no shell string interpolation of target content|S|P0|
|80|NFR-SEC-004|No response caching|No caching of responses across invocations|COMP-032|COMP-032|Each invocation makes fresh HTTP call; no cache headers used; no local cache|M|P0|
|81|NFR-SEC-005|No Anthropic routing|No routing to Anthropic models (proxy-routed external models only)|COMP-032|COMP-032|All calls go to T2ProxyUrl; no direct Anthropic endpoint references|S|P0|
|82|OQ-007|Workers > T2Models guard resolution|Implement chosen behavior (V1 warn-on-exceed recommended) in dispatch pool sizing|COMP-007|OQ-007|Guard fires when workers.count > len(T2Model0N list); chosen behavior implemented|M|P0|
|83|OQ-008|Empty-pool failure path resolution|Implement failed/env-missing contract in preflight for empty model pool|COMP-006|OQ-008|Empty pool → contract written; output dir check; pre-output-dir abort path|S|P0|
|84|COMP-008|Wave 2 normalize|Invoke configured Recipe per worker; atomic write to deterministic final path (IMM-6); promote parse_error→success if salvage succeeds|COMP-008|COMP-015, COMP-011, COMP-012|Recipe called per worker; output written atomically; parse_error promoted on salvage; state=normalizing|XL|P0|
|85|FR-EXEC-W2|Wave 2 normalize execution|Recipe Protocol invocation per worker; atomic write to final path; parse_error→success promotion on salvage|COMP-008|COMP-008|Each worker's raw text normalized; final path written atomically; salvage logic fires on parse_error|XL|P0|
|86|FR-REC-003|Three amalgamation modes|raw (W2 pass-through); normalize (default; W2 runs recipe); normalize+merge (W2 + W3 mechanical merge)|COMP-008|COMP-008|mode=raw → recipe skipped; mode=normalize → recipe runs; mode=normalize+merge → recipe + merge|M|P0|
|87|COMP-010|Mechanical merge module|swarm/merge.py: mechanical concat only; ≤30 LOC; read each final_path; strip frontmatter; prepend provenance header; concat in slot-index order|COMP-010|COMP-004|Module ≤30 LOC; 3-worker input → 3 sections in slot order; provenance headers present; no transforms|S|P0|
|88|FR-MERGE-001|Mechanical concat only|Read each final_path; strip frontmatter; prepend `## From {model_label} ({elapsed_ms}ms)`; concat in slot-index order|COMP-010|COMP-010|Output has N provenance sections in slot-index order; frontmatter stripped; no other transforms|M|P0|
|89|FR-MERGE-002|Merge disallowed operations|No reorder, dedup, scoring, winner selection, claim rewriting|COMP-010|COMP-010|Code review: no sorting, no dedup, no scoring logic, no content rewriting|S|P0|
|90|FR-MERGE-003|Merge LOC ceiling|Module body ≤30 LOC excluding imports + docstring|COMP-010|COMP-010|Line count ≤30; enforced by PR review|S|P0|
|91|FR-MERGE-004|Merge PR-review guard|Any change to swarm/merge.py requires "boundary preservation" review note|COMP-010|FR-MERGE-002|CI/PR checklist includes boundary preservation check for merge.py changes|S|P0|
|92|FR-MERGE-005|Merge boundary test|test_merge_mechanical_only.py: 3-worker concat → 3 sections in slot-index order with no transforms beyond provenance header; CI rule flags PRs touching this test|COMP-010|FR-MERGE-001|Test passes; CI rule configured; test file flagged in PR review|S|P0|
|93|FR-MERGE-006|Merge edge cases|M=0 → merged_path=null; M=1 → merged_path=null (failed by IMM-5); M≥2 → merged_path with only successful workers' files|COMP-010|FR-MERGE-001|Edge case logic correct; null for M<2; successful-only for M≥2|M|P0|
|94|COMP-009|Wave 3 reduce|Apply IMM-5 status determination; if normalize+merge run merge.py; write return-contract.yaml; write done.json atomically; emit final event; exit 0|COMP-009|COMP-010, COMP-011, COMP-012|Status determined per IMM-5; merge runs if applicable; contract written; done.json written; exit code correct|XL|P0|
|95|FR-EXEC-W3|Wave 3 reduce + merge|IMM-5 status determination; merge if normalize+merge; return-contract.yaml; done.json sentinel atomically; final event; exit 0|COMP-009|COMP-009|Full Wave 3 completes; contract valid; done.json present; exit code per FR-CLI-003|XL|P0|
|96|IMM-5|Success-first status determination|M==N→success; 2≤M<N→partial; M<2→failed. Edge M==N==2→success. Per-job configurable (floor=2, success_first=true defaults)|COMP-009|FR-EXEC-W3|Correct status for all combinations; M==N==2→success; floor and success_first configurable|M|P0|
|97|NFR-REL-003|Crash mid-dispatch resilience|Crash leaves .swarm-state.json with last-known state; completed workers retain .meta.json; absence of done.json indicates incomplete|COMP-011|COMP-011|Simulated crash → state file readable; meta files intact; done.json absent; resume possible|M|P0|

### Integration Points — M2

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|.swarm-state.json|State file|M2 complete|M2|CLI status (M3), resume (M4)|
|execution-log.jsonl|Event log|M2 complete|M2|CLI logs (M3), Monitor tailing (M3)|
|manifest.json|Durable snapshot|M2 complete|M2|Resume rehydration (M4)|
|.raw + .meta.json sidecars|Worker output|M2 complete|M2|Normalize (M2), Reduce (M2)|
|Recipe Protocol dispatch|Policy→Mechanism|M2 complete|M2|normalize.py invokes recipes per worker|M2|
|Mechanical merge|Provenance concat|M2 complete|M2|reduce.py calls merge.py in normalize+merge mode|M2|
|ThreadPoolExecutor dispatch|Concurrency|M2 complete|M2|True parallelism; lock-coordinated logging|M2|
|§11.5 delimiter wrapping|Security|M2 complete|M2|All prompt-input paths wrap target with delimiters|M2|

### Milestone Dependencies — M2

- M1 (all foundation deliverables complete)

### Open Questions — M2

- None (all M2-blocking OQs resolved in M1: OQ-007, OQ-008, OQ-010)

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R002 Merge boundary erosion|High|Medium|normalize+merge drifts into judging via incremental PRs|Four structural guards: docstring, ≤30 LOC, PR review, boundary test + CI flag|Architect|
|2|R005 ThreadPoolExecutor surprise|Low|Low|Engineers expect process-level parallelism|Docstring in dispatch.py explaining thread model; stub transport tests document behavior|Architect|
|3|R006 Custom-prompt-dir guard parity migration|Medium|Medium|Existing users need to add §11.5 sentence|--auto-inject-guard backward-compat flag during migration; migration guide|Architect|

## M3: Observability and CLI Surface

**Objective:** Create return contract serialization, CLI subcommands (run, status, logs, attach, kill, scaffold, validate, validate-lenses), Rich TUI dashboard, tmux detached-mode wrapper, security sandboxing | **Duration:** Weeks 5–6 | **Entry:** M2 exit criteria met; end-to-end stub execution works | **Exit:** All 8 CLI subcommands functional; return contract parseable by non-Claude caller; --tui dashboard shows live state; detached mode starts/attaches/kills

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|98|DM-005|ResultContract serialization|return-contract.yaml: all 22 fields from DM-005; YAML serialization|COMP-009|DM-005|Contract serializes to valid YAML; all fields present; contract_version="1.0"|S|P0|
|99|FR-OBS-001|Return contract emission|Emit return-contract.yaml with all required fields: contract_version, status, job_id, started/finished/elapsed_ms, caller, lens, lens_source, target, workers, output_files, amalgamation_mode, merged_path, caller_metadata, recommended_next_command, artifacts|COMP-009|DM-005|Contract contains all spec fields; values match execution; recommended_next_command template populated|M|P0|
|100|FR-OBS-005|Done sentinel|done.json terminal sentinel written atomically|COMP-009|COMP-011|done.json present after successful run; JSON valid with timestamp + job_id + status; atomic write|S|P0|
|101|FR-OBS-006|Three caller monitoring patterns|(a) Bash run_in_background + until -f done.json; (b) Monitor tailing JSONL; (c) swarm status --watch refreshing every 1s|COMP-002|COMP-009, COMP-011|All 3 patterns work: done.json detection; JSONL tail; status --watch refreshes every 1s|M|P0|
|102|NFR-OBS-001|Four-layer observability|State file + JSONL event log + Markdown human log + sentinel|COMP-011, COMP-012|FR-OBS-002, FR-OBS-003, FR-OBS-004, FR-OBS-005|All 4 layers written during execution; durable across crash|M|P0|
|103|NFR-SEC-003|Output directory sandboxing|Orchestrator must not write outside --output directory|COMP-006|COMP-003|All output paths resolved relative to --output; symlink escape blocked|S|P0|
|104|COMP-002|CLI commands module|Click subcommands: run, status, logs, attach, kill, scaffold, validate, validate-lenses|COMP-002|COMP-001, COMP-006, COMP-007, COMP-008, COMP-009, COMP-013, COMP-014|All 8 subcommands registered under swarm group; --help for each|XL|P0|
|105|FR-CLI-001|swarm CLI group|Top-level Click group `superclaude swarm` with 8 subcommands: run, status, logs, attach, kill, scaffold, validate, validate-lenses|COMP-002|COMP-002|`superclaude swarm --help` lists all 8; each has --help|M|P0|
|106|FR-CLI-002|swarm run flags|`--lens`, `--custom-prompt-dir`, `--auto-inject-guard`, `--amalgamation-mode {raw,normalize,normalize+merge}`, `--tui`, `--force-relens`|COMP-002|COMP-006|All flags accepted; defaults: amalgamation_mode=normalize, tui=false, auto-inject-guard=false|M|P0|
|107|FR-CLI-003|Exit codes|0=reached Wave 3 (status in contract); 2=spec validation failure; 3=preflight failure; 10=orchestrator internal error|COMP-002|COMP-006, COMP-009|Exit 0 on success; exit 2 on spec invalid; exit 3 on preflight fail; exit 10 on internal error|S|P0|
|108|FR-CLI-004|swarm scaffold|Emit a starter job-spec file for a named lens|COMP-002|COMP-022, COMP-005|`swarm scaffold --lens bare-review` writes valid job-spec YAML/JSON with lens defaults populated|S|P0|
|109|FR-CLI-005|swarm validate|Validate a job-spec file without dispatching|COMP-002|COMP-005|`swarm validate --spec <file>` exits 0 on valid spec; exits 2 with errors on invalid|S|P0|
|110|COMP-013|Rich TUI dashboard|Rich Live dashboard, opt-in via --tui (NOT default); shows live state, worker progress, events|COMP-013|COMP-011, COMP-012|Dashboard shows: current state; worker count/success/fail; elapsed time; event stream; non-TTY → no terminal control sequences|M|P1|
|111|FR-OBS-007|TUI opt-in behavior|`--tui` Rich Live dashboard inside inline-mode process; NOT default; non-TTY callers do not receive terminal control sequences|COMP-013|COMP-013|TUI only activates when --tui flag present and TTY detected; non-TTY → plain output|S|P1|
|112|COMP-014|tmux detached wrapper|Detached-run wrapper mirroring sprint/tmux.py|COMP-014|COMP-002|tmux session created with job name; process runs inside; session survives terminal close|S|P0|
|113|FR-RES-002|Detached mode + attach/kill|`swarm attach` re-attaches TUI; `swarm kill` terminates running detached job|COMP-002, COMP-014|COMP-014|attach reconnects to tmux session; kill terminates tmux session and child process|S|P0|
|114|FR-RES-001|Resume from manifest|`swarm run --resume <job_id>`: lens rehydration (INV-001), skip completed workers via .meta.json status=success, re-dispatch remaining, re-run Wave 2, regenerate merge (INV-010), apply IMM-5 + emit contract|COMP-002, COMP-006, COMP-009|COMP-006, COMP-007, COMP-008, COMP-009, DM-008|Resume rehydrates lens from manifest; skips completed workers; re-dispatches rest; merge regenerated if normalize+merge; contract valid|XL|P0|
|115|INV-001|Resume lens rehydration|`--resume` rehydrates lens definition from manifest.resolved_lens_entry; does NOT re-resolve from LENSES; `--force-relens` opts into re-resolution|COMP-006|FR-RES-001|Lens used on resume matches manifest snapshot; force-relens flag re-resolves from registry|M|P0|
|116|INV-010|Resume merge regeneration|On --resume + amalgamation_mode==normalize+merge, Wave 3 unconditionally regenerates merged.md from current final_paths after re-dispatched workers' Wave 2 completes|COMP-009|FR-RES-001|Resume with normalize+merge → merged.md regenerated from current final_paths, not from cache|M|P0|
|117|INV-016|Manifest as durable source|manifest.resolved_lens_entry is durable definition of swarm; lens-registry mutations between runs do not affect resumed job|COMP-006|INV-001|Registry mutated between runs; resume uses manifest entry, not mutated registry|S|P0|
|118|FR-LENS-004|Lens-driven defaults expansion|At preflight, lens-driven defaults expand into job spec: prompt.system, prompt.user_template, normalization.recipe, normalization.template_path, workers.count, target.truncation.line_cap, output.filename_template, output.lens_name, recommended_next_command_template, caller_metadata.suspect, caller_metadata.tier|COMP-006|FR-LENS-003|Lens defaults populate all spec fields; caller-supplied values override lens defaults|M|P0|
|119|FR-LENS-005|Lens snapshot in manifest|Snapshot resolved_lens_entry into manifest.json at preflight time|COMP-006|FR-LENS-004|manifest.json contains full LensEntry snapshot; matches lens at preflight time|S|P0|
|120|FR-SPEC-005|Filename template|Output filename template: "{lens}-{index:02d}-{model_slug}.md"|COMP-009|COMP-004|Output files follow template pattern; index is zero-padded 2 digits|M|P0|
|121|NFR-REL-002|Atomic state transitions|State file transitions atomic on every transition (reiterated from M2, validated with CLI)|COMP-011|COMP-002|CLI status reads consistent state during transitions|S|P0|
|122|OQ-006|Concurrent --output dir protection|Document caller-must-avoid for v1; no file-level locking on shared output dirs|—|—|Documentation updated; v1 scope note in CLAUDE.md|S|P1|

### Integration Points — M3

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|return-contract.yaml|Result contract|M3 complete|M3|Non-Claude callers (SC-010), downstream automation|
|done.json|Sentinel|M3 complete|M3|Monitoring pattern (a) file-wait detection|
|execution-log.jsonl|Event stream|M3 complete|M3|Monitoring pattern (b) JSONL tail; CLI logs subcommand|
|CLI subcommands (8)|User interface|M3 complete|M3|All user interaction; subprocess.run callability (NFR-COMPAT-001)|
|swarm status --watch|Polling interface|M3 complete|M3|Monitoring pattern (c) 1s refresh|
|tmux wrapper|Detached execution|M3 complete|M3|Detached mode; attach/kill commands|
|Rich TUI|Live dashboard|M3 complete|M3|Inline opt-in monitoring; event visualization|
|recommended_next_command_template|Next-cmd template|M3 complete|M3|Post-swarm caller handoff guidance|

### Milestone Dependencies — M3

- M2 (all execution waves complete)

### Open Questions — M3

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-006|Concurrent --output dir protection — document caller-must-avoid for v1?|Shared output dirs could corrupt state between concurrent runs|Architect|End of M3|

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R004 Tmux dependency for detached mode|Low|Low|tmux binary required for detached mode|Detached optional; inline default; graceful error when tmux absent|Architect|
|2|R006 Custom-prompt-dir guard parity migration|Medium|Medium|Existing users need to add §11.5 sentence|--auto-inject-guard backward-compat flag; migration guide in docs|Architect|
|3|R001 Lens-registry sprawl|Medium|Medium|Speculative lenses inflate registry without callers|PR-review discipline; custom-py: for exploratory work|Architect|

## M4: Migration and A/B Parity

**Objective:** Rewrite sc-bare-review SKILL.md as ~60-line thin caller building --lens bare-review job spec → execs CLI → relays return contract; run A/B parity test against legacy output; delete legacy shell scripts; resolve remaining open questions | **Duration:** Weeks 7–8.5 | **Entry:** M3 exit criteria met; CLI surface fully functional | **Exit:** A/B parity gate passes (SC-008); legacy scripts deleted (SC-012); thin-caller SKILL.md at ~60 LOC

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|123|FR-MIG-001|sc-bare-review thin caller|Rewrite sc-bare-review/SKILL.md as ~60-line thin caller: builds --lens bare-review job spec → execs CLI → relays return contract|COMP-002|COMP-002, FR-CLI-002|SKILL.md ~60 LOC; builds job spec; calls subprocess.run; relays contract output|S|P0|
|124|FR-MIG-002|Delete legacy shell scripts|Delete sc-bare-review/scripts/*.sh after production migration|—|FR-MIG-001|All .sh files removed from sc-bare-review/scripts/; no references remain|S|P0|
|125|FR-MIG-003|A/B parity test|A/B parity test of new thin-caller skill against today's bare-review output on fixed test target|—|FR-MIG-001|New output matches legacy output on fixed test target within acceptable tolerance|S|P0|
|126|SC-008|A/B parity gate|New sc-bare-review thin caller (--lens bare-review) produces output equivalent to today's bare-review skill on fixed test target|—|FR-MIG-003|Parity test passes; output equivalence verified on ≥3 fixed test targets|M|P0|
|127|SC-012|Script cleanup gate|scripts/*.sh removed from sc-bare-review after production migration; SKILL.md reduced to ~60 LOC thin caller|—|FR-MIG-002|No .sh files remain; SKILL.md ≤70 LOC; verify-sync passes|M|P0|
|128|OQ-009|caller_metadata.suspect override semantics|Can caller-supplied job spec override lens entry's suspect field without violating lens contract? Implied yes (caller overrides per §4.2)|—|—|Decision documented; spec schema allows override; behavior tested|S|P0|
|129|FR-SPEC-002|caller block|caller{skill,skill_version,invocation_label,kind} fields in job spec|COMP-005|DM-002|All 4 caller fields validated; kind informational only (NFR-COMPAT-001)|S|P0|
|130|FR-LENS-004|Lens default override|Caller-supplied values override lens defaults for all expanded fields|COMP-006|FR-LENS-004|Override behavior tested: caller value wins for workers.count, prompt.system, etc.|M|P0|
|131|FR-CLI-002|Amalgamation mode flag|`--amalgamation-mode {raw,normalize,normalize+merge}` default normalize|COMP-002|COMP-008|All 3 modes accepted via CLI flag; default is normalize|S|P0|
|132|FR-CLI-002|Force-relens flag|`--force-relens` opts into re-resolution from registry on resume|COMP-002|INV-001|Flag present → lens re-resolved; flag absent → manifest entry used|S|P0|
|133|INV-002|Shell dispatch retirement|V2-style swarm_dispatch.sh shell script retired; PIPE_BUF assumption deprecated|—|INV-002|No .sh dispatch scripts in codebase; all dispatch via Python ThreadPoolExecutor|S|P0|
|134|FR-EXEC-W1|Always-record behavior|Always record worker outcome regardless of success/failure|COMP-007|FR-EXEC-W1|.meta.json written for every worker even on failure; events emitted for all workers|S|P0|
|135|NFR-SEC-002|§11.5 uniform enforcement|§11.5 injection-guard substring enforced at preflight on all three prompt-input paths (JSON Schema, lens, custom-prompt-dir)|COMP-006|FR-INJ-002, FR-INJ-003, FR-INJ-004|All 3 paths enforce §11.5 identically; STOP on absence; --auto-inject-guard opt-in|M|P0|
|136|FR-INJ-001|Delimiter wrapping in prompts|Target wrapped in <<<TARGET>>> / <<<END TARGET>>> delimiters in all dispatched prompts|COMP-006|FR-INJ-001|All worker prompts contain correct delimiter markers around target content|S|P0|
|137|NFR-PERF-002|Parallelism verification|Single ParallelGroup with N parallel HTTP calls verified|COMP-007|NFR-PERF-002|Test confirms wall-clock ≈ max(individual times) for N workers|S|P0|
|138|COMP-008|Parse_error salvage promotion|Promote parse_error → success if §7.4 salvage succeeds|COMP-008|FR-EXEC-W2|Salvage logic fires on parse_error; successful salvage → status promoted to success|S|P0|
|139|FR-REC-001|custom-py dynamic loader|`custom-py:module:func` dynamic recipe loader via importlib|COMP-021|FR-REC-001|Custom recipe resolved at runtime from arbitrary module:func path|S|P1|
|140|NFR-COMPAT-001|subprocess.run callability|`subprocess.run(["superclaude","swarm","run",…])` callable from any language|COMP-002|FR-CLI-003|Non-Python caller can drive full swarm cycle via subprocess; exit codes match spec|S|P0|
|141|FR-RES-001|Resume skip-completed-workers|On resume, skip workers with .meta.json status=success; re-dispatch remaining|COMP-007|FR-RES-001|Resume correctly identifies completed workers; only re-dispatches incomplete ones|M|P0|
|142|INV-010|Resume merge regeneration test|Unconditionally regenerate merged.md on resume with normalize+merge mode|COMP-009|INV-010|Test confirms merged.md regenerated from current final_paths on resume|S|P0|

### Integration Points — M4

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|sc-bare-review SKILL.md|Thin caller|M4 complete|M4|Direct user invocation of bare-review via swarm|
|A/B parity test harness|Validation|M4 complete|M4|SC-008 gate; regression prevention|
|Legacy script removal|Cleanup|M4 complete|M4|Clean codebase; no dual-dispath confusion|
|Resume flow|Crash recovery|M4 complete|M4|Production reliability; SC-011|
|Caller metadata override|Policy override|M4 complete|M4|Advanced callers customize suspect/tier|

### Milestone Dependencies — M4

- M3 (CLI surface and observability complete)
- M2 (execution waves complete, for resume testing)

### Open Questions — M4

- None (OQ-009 resolved within M4)

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R002 Merge boundary erosion|High|Medium|Incremental PRs add judgment logic to merge.py|≤30 LOC ceiling; boundary test; CI rule flags touches; PR review checklist|Architect|
|2|R006 Custom-prompt-dir guard parity migration|Medium|Medium|Existing users need to add §11.5 sentence|--auto-inject-guard backward-compat flag; clear error messages; migration guide|Architect|
|3|R003 Resume + lens-mutation interaction|Medium|Medium|Registry mutation between runs silently changes resume behavior|Manifest snapshot as durable source; --force-relens opt-in; tests cover both paths|Architect|

## M5: Validation and Release Gates

**Objective:** Run all acceptance tests (SC-001 through SC-012); wire validate-lenses into pre-commit/make verify-sync; validate forward-compat; document deferred features (OQ-002..OQ-005) | **Duration:** Weeks 9–10 | **Entry:** M4 exit criteria met; A/B parity passes | **Exit:** All 12 success criteria pass; pre-commit hook wired; release-ready documentation

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|143|SC-001|IMM-N invariant tests|Every IMM-N invariant (IMM-3, IMM-4, IMM-5, IMM-6) has a passing acceptance test in tests/swarm/|—|COMP-007, COMP-006, COMP-009|4 tests pass: IMM-3 (parallel dispatch); IMM-4 (empty target); IMM-5 (status determination); IMM-6 (atomic write)|M|P0|
|144|SC-002|INV-001 resume lens test|tests/swarm/test_resume_uses_manifest_lens.py passes — INV-001 verified|—|FR-RES-001|Test passes; resume uses manifest entry not registry|M|P0|
|145|SC-003|INV-002 no shell dispatch test|tests/swarm/test_concurrency_python_only.py passes — INV-002 (no shell dispatch) verified|—|INV-002|Test passes; no .sh dispatch found; ThreadPoolExecutor only|M|P0|
|146|SC-004|INV-003 custom prompt dir test|tests/swarm/test_custom_prompt_dir_injection_guard.py passes — INV-003 verified|—|FR-INJ-004|Test passes; custom-prompt-dir validates §11.5|M|P0|
|147|SC-005|INV-010 resume merge test|tests/swarm/test_resume_regenerates_merge.py passes — INV-010 verified|—|INV-010|Test passes; resume with normalize+merge regenerates merged.md|M|P0|
|148|SC-006|INV-014 escape hatch parity test|tests/swarm/test_escape_hatch_guard_parity.py passes — INV-014 verified|—|FR-INJ-004|Test passes; §11.5 enforcement identical across all 3 paths|M|P0|
|149|SC-007|Merge boundary test|tests/swarm/test_merge_mechanical_only.py passes — 3-worker → 3 sections in slot-index order, no transforms beyond provenance header|—|FR-MERGE-005|Test passes; boundary preserved; provenance headers only transforms|M|P0|
|150|SC-009|validate-lenses exits 0|swarm validate-lenses exits 0 over bundled registry with no findings; wired into make verify-sync and/or pre-commit|—|FR-LENS-006|validate-lenses exits 0; pre-commit hook runs it; make verify-sync includes it|S|P0|
|151|SC-010|Non-Claude caller drives swarm|Non-Claude caller can drive full swarm cycle via subprocess.run and parse return-contract.yaml + done.json using only stdlib, with no Claude-tool-name references|—|FR-OBS-001, NFR-COMPAT-001|External script (bash/node) runs swarm; parses contract; zero Claude tool names found|S|P0|
|152|SC-011|Crash-resume verification|Crash during dispatch produces resumable state — swarm run --resume skips completed workers, re-dispatches rest, regenerates merge, writes valid contract|—|FR-RES-001, NFR-REL-003|Simulated crash → resume completes; no double-dispatch; valid contract|M|P0|
|153|SC-008|A/B parity gate (reiterated)|New sc-bare-review thin caller produces output equivalent to legacy on fixed test target|—|FR-MIG-003|Parity test passes (from M4, re-verified)|S|P0|
|154|SC-012|Script cleanup gate (reiterated)|Legacy scripts removed; SKILL.md reduced to ~60 LOC|—|FR-MIG-002|No .sh files; SKILL.md ≤70 LOC (from M4, re-verified)|S|P0|
|155|OQ-001|Pre-commit wiring|Wire swarm validate-lenses as pre-commit hook|—|SC-009|pre-commit config includes validate-lenses; hook runs on CI|S|P0|
|156|OQ-002|Per-lens version pinning deferred|Document --lens-version v2 semantics deferred until lens definitions mutate frequently in production|—|—|Decision recorded in docs; deferred to future milestone|S|P2|
|157|OQ-003|Auto-handoff flag deferred|Document --auto-handoff flag deferred; recommended_next_command never auto-executed in v1|—|—|Decision recorded in docs; deferred|S|P2|
|158|OQ-004|Prometheus output deferred|Document Prometheus/OpenMetrics output at event boundary deferred|—|—|Decision recorded in docs; deferred|S|P2|
|159|OQ-005|Per-model overrides deferred|Document per-model temperature/overrides within one swarm deferred until real lens requests it|—|—|Decision recorded in docs; deferred|S|P2|
|160|FR-CLI-003|Exit code integration test|Exit codes 0/2/3/10 all exercised in integration tests|COMP-002|FR-CLI-003|Tests confirm each exit code path fires correctly|S|P0|
|161|NFR-COMPAT-002|Forward-compat test|Spec version 1.1 orchestrator loads 1.0 specs without error|COMP-005|NFR-COMPAT-002|v1.1 spec loads v1.0 job spec; no errors|S|P1|
|162|FR-OBS-006|Monitoring patterns test|All 3 caller monitoring patterns verified: (a) done.json wait; (b) JSONL tail; (c) status --watch|COMP-002|FR-OBS-006|All 3 patterns tested and passing|S|P0|
|163|NFR-SEC-005|No Anthropic routing test|Verify no direct Anthropic endpoint references in codebase|COMP-032|NFR-SEC-005|Grep for anthropic.com/api keys yields zero results in swarm/ code|S|P0|
|164|NFR-MAINT-001|Module layout verification|Verify module layout mirrors cli/sprint/ for operator familiarity|COMP-001|NFR-MAINT-001|Directory structure comparison passes; naming conventions match|S|P1|
|165|FR-OBS-001|Result contract completeness|return-contract.yaml contains all required fields as specified in DM-005|COMP-009|DM-005|Contract validated against schema; all 22 fields present with correct types|M|P0|
|166|FR-SPEC-005|Target truncation verification|Truncation line_cap:4000 and byte_floor:50 enforced|COMP-006|FR-SPEC-005|Target truncated at line cap; byte floor checked before dispatch|S|P0|
|167|FR-LENS-006|Lens validation CI gate|validate-lenses wired into CI pipeline; fails CI on registry violations|—|FR-LENS-006|CI pipeline includes validate-lenses step; fails on invalid registry|S|P0|
|168|FR-MERGE-004|Merge PR-review checklist|PR-review checklist includes boundary preservation note for merge.py changes|—|FR-MERGE-004|CONTRIBUTING.md or PR template includes merge.py review checklist item|S|P0|

### Integration Points — M5

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Acceptance tests (SC-001..SC-012)|Test suite|M5 complete|M5|CI pipeline; release gate|
|pre-commit hook|CI/CD|M5 complete|M5|Developer workflow; CI pipeline|
|Deferred features doc|Documentation|M5 complete|M5|Future roadmap planning|
|Release documentation|User guide|M5 complete|M5|Operators; downstream teams|
|CONTRIBUTING.md update|Process|M5 complete|M5|PR reviewers (merge boundary)|

### Milestone Dependencies — M5

- M3 (CLI surface complete, for exit code and monitoring tests)
- M4 (migration complete, for A/B parity and script cleanup gates)

### Open Questions — M5

- None (all OQs resolved or formally deferred with documentation)

### Risk Assessment and Mitigation — M5

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R002 Merge boundary erosion|High|Medium|Post-release PRs add judgment logic to merge.py|Boundary test in CI; ≤30 LOC enforced; PR template checklist|Architect|
|2|R001 Lens-registry sprawl|Medium|Medium|Post-release, speculative lenses added without callers|PR-review discipline; validate-lenses in CI catches incomplete entries|Architect|
|3|R007 Schema evolution drag|Low|Low|Forward-compat maintenance becomes burden|Defer 1.1 spec until real production need|Architect|

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By Milestone|Status|Fallback|
|---|---|---|---|
|httpx|M1, M2|PyPI package|N/A — required for openai_compat transport|
|Click|M1, M2, M3|Already in project dependencies|N/A — core CLI framework|
|Rich|M3|Already in project dependencies|Plain text output if Rich unavailable; TUI degrades gracefully|
|tmux|M3|System binary (optional)|Detached mode unavailable; inline mode works without tmux|
|PyYAML|M1, M2, M3|Implicit dependency|N/A — required for job spec + contract serialization|
|JSON Schema validator|M1|jsonschema PyPI package|Fallback to manual validation (less robust)|
|superclaude.execution.parallel.ParallelExecutor|M2|Internal shared module|N/A — required for ThreadPoolExecutor orchestration|
|T2ProxyUrl / T2ProxyKey / T2Model0N env|M2, M3|External proxy service|stub transport for tests; no production fallback|
|Downstream commands (sc:adversarial, sc:code-review, sc:reflect, sc:research, sc:troubleshoot, sc:document)|M1|Existing skills|Next-cmd templates reference them; absence doesn't block swarm execution|

### Infrastructure Requirements

- Python 3.10+ runtime with ThreadPoolExecutor support
- T2Proxy endpoint accessible via T2ProxyUrl env var with T2ProxyKey authentication
- T2Model0N model identifiers available in runtime environment
- Filesystem with atomic write support (os.replace semantics)
- tmux binary (optional, for detached mode only)

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|Mitigation|Owner|
|----|------|---------------------|-------------|--------|------------|-------|
|R001|Lens-registry sprawl: speculative lenses inflate registry without real callers|M1, M3, M4, M5|Medium|Medium|PR-review discipline: require real caller; custom-py: + caller-side prompts for exploratory work|Architect|
|R002|Merge boundary erosion: normalize+merge drifts into judging via incremental PRs|M2, M4, M5|Medium|High|Four structural guards: docstring, ≤30 LOC ceiling, PR review checklist, test_merge_mechanical_only.py + CI flag|Architect|
|R003|Resume + lens-mutation interaction: registry mutation between runs silently changes resume behavior|M1, M2, M4|Medium|Medium|Manifest snapshot as durable source; --force-relens opt-in; tests cover both paths|Architect|
|R004|Tmux dependency for detached mode: tmux binary required|M3|Low|Low|Detached optional; inline default; graceful error when tmux absent|Architect|
|R005|ThreadPoolExecutor surprise: engineers expect process-level parallelism|M2|Low|Low|Docstring in dispatch.py explaining thread model; stub transport tests document behavior|Architect|
|R006|Custom-prompt-dir guard parity migration: existing users need to add §11.5 sentence|M2, M3, M4|Medium|Medium|--auto-inject-guard backward-compat flag during migration; clear error messages; migration guide|Architect|
|R007|Schema evolution drag: forward-compat from spec 1.0→1.1 becomes maintenance burden|M1, M5|Low|Low|Forward-compat best-effort policy; defer 1.1 until real production need|Architect|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|Milestone|
|---|---|---|---|---|
|SC-001|IMM-N invariant tests|4/4 passing|Pytest acceptance tests in tests/swarm/|M5|
|SC-002|INV-001 resume lens rehydration|Test passes|test_resume_uses_manifest_lens.py|M5|
|SC-003|INV-002 no shell dispatch|Test passes|test_concurrency_python_only.py; no .sh in swarm/|M5|
|SC-004|INV-003 custom-prompt-dir guard|Test passes|test_custom_prompt_dir_injection_guard.py|M5|
|SC-005|INV-010 resume merge regeneration|Test passes|test_resume_regenerates_merge.py|M5|
|SC-006|INV-014 escape-hatch parity|Test passes|test_escape_hatch_guard_parity.py|M5|
|SC-007|Merge boundary preservation|Test passes|test_merge_mechanical_only.py: 3 sections in slot order|M5|
|SC-008|A/B parity: thin caller vs legacy|Output equivalent|Fixed test target comparison; ≥3 targets|M4/M5|
|SC-009|validate-lenses exits 0|Exit 0, no findings|CLI execution over bundled registry; CI integration|M5|
|SC-010|Non-Claude caller drives full cycle|Full cycle completes|External script via subprocess.run; stdlib-only parsing|M5|
|SC-011|Crash-resume produces valid state|Resume completes|Simulated crash → resume → valid contract|M5|
|SC-012|Legacy scripts deleted; SKILL.md ≤60 LOC|0 .sh files; ≤70 LOC|File count + line count verification|M4/M5|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|----------|--------|------------------------|----------|
|Dispatch mechanism|Python ThreadPoolExecutor (INV-002)|Shell script dispatch (legacy), subprocess per-worker, async/asyncio|ThreadPoolExecutor: code-enforced parallelism (IMM-3), lock-coordinated state, no PIPE_BUF dependency, within single process|
|CLI placement|src/superclaude/cli/swarm/|SKILL.md wrapper, standalone script, plugin|CLI placement enables code-enforced parallelism, subprocess.run callability, durable observability, future-harness compatibility (§1.4)|
|Merge scope|Mechanical concat only, ≤30 LOC|Scoring, dedup, winner selection, AI re-write|Boundary preservation: merge is provenance-only; judgment belongs in recipes and downstream commands (§10.2)|
|Resume source-of-truth|manifest.resolved_lens_entry|Re-resolve from LENSES dict on every resume|Deterministic: registry mutations between runs invisible unless --force-relens (INV-001, INV-016)|
|§11.5 enforcement|Uniform across all 3 paths|Path-specific enforcement, opt-in per path|Security uniformity: no path is weaker; --auto-inject-guard backward-compat flag eases migration (§11.1)|
|Module layout|Mirrors cli/sprint/|New naming convention, flat layout|Operator familiarity: engineers who know sprint can navigate swarm (§2.1)|
|Transport|OpenAI-compatible Protocol with httpx|Anthropic SDK direct, custom HTTP|Future-harness: no Claude tool names; proxy-routed external models only (NFR-COMPAT-001, NFR-SEC-005)|
|TUI default|Opt-in via --tui (NOT default)|Default TUI for inline mode|Non-TTY compatibility: terminal control sequences break non-TTY callers; inline default preserves subprocess.run contract (INV-012)|

## Timeline Estimates

|Milestone|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1: Foundation and Module Setup|2 weeks|Week 1|Week 2|Module layout; data models; JSON Schema; lens registry (8 entries); recipe protocol (6 recipes); transport layer; 3 OQs resolved|
|M2: Execution Waves and Dispatch|2 weeks|Week 3|Week 4|State management; logging; Wave 0 preflight; Wave 1 dispatch; Wave 2 normalize; Wave 3 reduce + merge; all IMM-N enforced|
|M3: Observability and CLI Surface|2 weeks|Week 5|Week 6|Return contract; 8 CLI subcommands; TUI dashboard; tmux detached mode; resume flow; security sandboxing|
|M4: Migration and A/B Parity|1.5 weeks|Week 7|Week 8.5|Thin-caller SKILL.md; A/B parity gate; legacy script deletion; OQ-009 resolved|
|M5: Validation and Release Gates|1.5 weeks|Week 8.5|Week 10|12 success criteria tests; pre-commit wiring; deferred features documented; release-ready|

**Total estimated duration:** 10 weeks
