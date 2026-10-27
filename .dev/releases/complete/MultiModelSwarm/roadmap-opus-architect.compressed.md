---
spec_source: "merged-requirements.compressed.md"
complexity_score: 0.82
complexity_class: HIGH
primary_persona: architect
adversarial: false
base_variant: "none"
variant_scores: "none"
convergence_score: none
---
# MultiModel Swarm Orchestrator (`superclaude swarm`) — Project Roadmap

## Executive Summary

This roadmap delivers `superclaude swarm` — a new top-level CLI verb representing the third orchestration primitive in the SuperClaude framework: single-shot parallel fan-out, distinct from `sprint` (sequential-phase) and `roadmap` (generative-graph). The orchestrator dispatches N workers in true Python-process parallelism against external T2-proxy models, normalizes each worker's output through a pluggable Recipe Protocol, and emits a durable return contract. Policy (prompts, templates, normalizers) lives in a bundled lens registry; mechanism (parallel dispatch, invariants, observability) lives in the CLI package; the caller owns choice. The marquee migration target is `sc-bare-review`, which collapses from a script-driven SKILL.md to a ~60-line thin caller over `--lens bare-review`.

**Business Impact:** Converts attention-mediated parallelism (fragile, Claude-tool-call-dependent) into code-enforced ThreadPoolExecutor parallelism (deterministic, cross-language callable via `subprocess.run`). Establishes a reusable fan-out primitive that any current or future harness can drive, eliminates a class of dual-writer race conditions by retiring shell-script dispatch, and hardens prompt-injection defenses across all three prompt-input paths. Unlocks 7 additional review/analysis lenses on the same mechanism at marginal cost.

**Complexity:** HIGH (0.82) — driven by code-enforced concurrency with multiple lock disciplines (JSONL append + atomic state rename), four structural guards on the merge boundary, dual prompt-input-path validation, and six invariant remediations (INV-001/002/003/010/014/016) that require test-first execution. Cross-cutting invariants IMM-3/4/5/6 and §11.5 must carry forward verbatim or stronger from the parent bare-review spec.

**Critical path:** Foundation & domain models (M1) → Transport & Recipe layers (M2) → Lens registry (M3) → Wave 0 preflight (M4) → Wave 1 dispatch (M5) → Wave 2/3 normalize+reduce+merge (M6) → CLI surface & resilience (M7) → invariant test suite (M8) → sc-bare-review migration & A/B parity (M9). Concurrency (M5) and the merge boundary (M6) are the highest-risk segments; the migration gate (M9) cannot close until A/B parity is observed.

**Key architectural decisions:**

- Three-layer mechanism/policy/caller separation (AC-001): orchestrator owns mechanism, lens registry + Recipe Protocol own policy, caller owns choice — enforced by module boundaries, not convention.
- CLI is the orchestrator home, not SKILL.md (AC-002): ThreadPoolExecutor enforces parallelism in code where prose cannot; durable observability, detached mode, and resume become first-class.
- Manifest-as-source-of-truth for resume (INV-016/FR-044): `manifest.resolved_lens_entry` is the durable definition of "what this swarm was supposed to do"; registry mutations between runs never affect a resumed job.

**Open risks requiring resolution before M1:**

- OQ-007 (workers > configured T2Models guard: warn-vs-STOP) and OQ-008 (empty-pool failure path) shape the preflight contract and the WorkerSpec floor semantics; both should be confirmed before M4 dispatch design, ideally during M1 model design so `status_policy` and `WorkerSpec` fields are not reworked.

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|----|-------|------|----------|--------|--------------|--------------|------|
|M1|Foundation & Domain Models|Foundation|P0|L|—|18|Medium|
|M2|Transport & Recipe Layers|Foundation|P0|M|M1|13|Medium|
|M3|Lens Registry & Validator|Feature|P0|L|M1, M2|17|Medium|
|M4|Wave 0 — Preflight|Feature|P0|L|M1, M3|12|High|
|M5|Wave 1 — Parallel Dispatch|Feature|P0|XL|M2, M4|12|High|
|M6|Wave 2/3 — Normalize, Reduce, Merge|Feature|P0|XL|M2, M5|14|High|
|M7|CLI Surface, Observability, Resilience|Feature|P0|XL|M4, M6|34|Medium|
|M8|Invariant Test Suite & Verification|Quality|P0|L|M5, M6, M7|15|Medium|
|M9|sc-bare-review Migration & A/B Parity|Migration|P1|M|M8|5|Medium|

## Dependency Graph

```
M1 ──┬──► M2 ──┬──► M3 ──► M4 ──► M5 ──► M6 ──► M7 ──► M8 ──► M9
     │         │                  ▲       ▲       ▲       ▲
     └─────────┴──► M4 (schema)   │       │       │       │
               M2 ──► M5 (transport)      │       │       │
                         M2 ──► M6 (recipes)      │       │
                                   M4 ──► M7 (preflight/resume)
                                           M5,M6,M7 ──► M8 (invariant tests)
                                                       M8 ──► M9 (parity gate)
```

Critical path: M1 → M2 → M3 → M4 → M5 → M6 → M7 → M8 → M9. M3 and M2 share the M1 foundation; M3 additionally consumes M2 recipe names for `recipe_name` resolution. M5 forks on both M4 (preflight artifacts) and M2 (transport). M8 is a convergence point requiring M5/M6/M7 complete.

## M1: Foundation & Domain Models

**Objective:** Establish the `cli/swarm/` package mirroring `cli/sprint/`, all domain dataclasses, JSON Schema host, config, atomic state I/O, and the atomic-write utility (IMM-6). | **Duration:** 2 wk (W1–W2) | **Entry:** repo clean, parent bare-review v1.3.0-draft invariants reviewed | **Exit:** package importable; all DM dataclasses defined + round-trip serialize/deserialize; atomic-write utility passes mid-write kill test; `superclaude swarm` group resolves with no subcommands wired.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-001|`swarm_group` Click group export|Public Click group entry point exposed at `superclaude swarm` in `cli/swarm/__init__.py`|swarm/__init__|—|`superclaude swarm --help` resolves; group registered in CLI entrypoint; no subcommands required yet|S|P0|
|2|COMP-003|`SwarmConfig` dataclass + path resolution|Global config + output/job path resolution in `config.py`|config|—|resolves `--output` dir; job_id path layout deterministic; env-var names centralized|S|P0|
|3|COMP-004|`models` domain container module|Hosts all swarm dataclasses in `models.py`|models|DM-001..DM-006,DM-008|imports COMP-005-free; all dataclasses constructible; frozen where spec'd|S|P0|
|4|COMP-005|`schema` module — JSON Schema + validators|JSON Schema for job spec, cross-field validators, §11.5 required-substring rule on `prompt.system`|schema|COMP-004|schema loads; cross-field rule rejects floor>count; §11.5 substring rule wired (invoked in M4)|M|P0|
|5|COMP-010|`state` module — atomic state I/O|`.swarm-state.json` read/write with atomic rename in `state.py`|state|COMP-004|write→read round-trips; transitions atomic via os.replace; concurrent read never sees partial|S|P0|
|6|DM-001|`JobSpec` dataclass|Validated job specification driving dispatch|models|COMP-004|spec_version:str; job_id:str(`<ISO>-<lens>-<short-hash>`); created:str-ISO8601; caller:dict{skill,skill_version,invocation_label,kind}; lens:str\|None; custom_prompt_dir:str\|None; workers:WorkerSpec; transport:dict{kind,base_url_env,api_key_env}; prompt:dict{system,user_template,variables}; target:dict{kind,path,truncation{line_cap,byte_floor},delimiters{open,close},injection_guard{enabled,required_substring}}; normalization:dict{recipe,template_path,schema_version,recipe_args,on_parse_error{salvage,retain_raw}}; output:dict{dir,filename_template,lens_name,atomic_write,emit_meta_sidecar}; amalgamation_mode:Literal[raw,normalize,normalize+merge]=normalize; status_policy:dict{floor,success_first,partial_threshold}; recommended_next_command_template:str; recommended_next_command_substitutions:dict; runtime:dict{mode,log_level,on_completion{write_done_sentinel,print_contract_to_stdout}}|L|P0|
|7|DM-002|`WorkerSpec` dataclass|Worker-fleet configuration|models|DM-001|count:int(≥status_policy.floor); models:list[str](env-resolved if absent); timeout_sec:int=180; temperature:float=0.2; retry:dict{on_5xx:int=1,on_5xx_backoff_sec:int=2,on_4xx:int=0,on_timeout:int=0}|S|P0|
|8|DM-003|`ResultContract` dataclass|Terminal-state return contract → `return-contract.yaml`|models|DM-004|contract_version:str=1.0; status:Literal[success,partial,failed]; job_id:str; started:str-ISO8601; finished:str-ISO8601; elapsed_ms:int; caller:dict{skill,skill_version,invocation_label}; lens:str\|None; lens_source:Literal[registry,custom]\|None; target:dict{path,checksum,truncated,truncation_line_cap}; workers_requested:int; workers_succeeded:int; workers_failed:int; output_files:list[WorkerResult]; amalgamation_mode:Literal[raw,normalize,normalize+merge]; merged_path:str\|None; caller_metadata:dict{suspect,tier}; recommended_next_command:str; artifacts:dict{manifest_path,state_path,event_log_jsonl,event_log_md,done_sentinel}|M|P0|
|9|DM-004|`WorkerResult` dataclass|Per-worker outcome element in result contract|models|DM-001|index:int; path:str\|None; raw_path:str\|None; meta_path:str; model_id:str; model_label:str; bytes:int; status:Literal[success,timeout,parse_error,proxy_error]; http_code:int; attempts:int; elapsed_ms:int|S|P0|
|10|DM-005|`SwarmState` dataclass|`.swarm-state.json` durable run-state|models|COMP-010|state:Literal[preflight_ok,dispatching,normalizing,reducing,terminal]; job_id:str; last_transition_timestamp:str; current_wave:str; worker_progress_map:dict|S|P0|
|11|DM-006|`EventRecord` dataclass|JSONL event-log row (append-only)|models|DM-001|event_type:Literal[worker_start,worker_progress,worker_done,wave_transition,final]; timestamp:str; worker_index:int\|None; payload:dict|S|P0|
|12|DM-008|`Manifest` (`manifest.json`) model|Durable definition of intended swarm behavior|models|DM-007(field)|contract_version:str; job_id:str; resolved_lens_entry:dict{name,system_prompt_fragment,user_template,recipe_name,default_workers,suspect,tier,recommended_next_command_template,stability}; additional_preflight_resolved_fields:dict|M|P0|
|13|FR-047|Atomic-write idempotency utility (IMM-6)|Every output file written via write-to-tmp + `os.replace` + deterministic filename|state/util|COMP-003|tmp file in same dir; os.replace rename; mid-write kill leaves no partial at final path; deterministic filename|M|P0|
|14|NFR-004|Atomic-write durability guarantee|All output files atomically written; state transitions atomic; durable across crashes|state/util|FR-047|crash during write → previous content intact; no zero-byte finals|M|P0|
|15|NFR-007|Module layout mirrors `cli/sprint/`|Package shape mirrors sprint for operator continuity|swarm/*|COMP-001|file-by-file structural parity audit vs `cli/sprint/`; naming aligned|S|P0|
|16|AC-001|Mechanism/policy/caller three-layer separation|Orchestrator owns mechanism; lens registry + Recipe Protocol own policy; caller owns choice|swarm/*|COMP-001|no prompt/template literals in mechanism modules; policy isolated to lenses/+recipes/|S|P0|
|17|AC-002|CLI is orchestrator home (not SKILL.md)|ThreadPoolExecutor + observability + detached + resume are first-class in CLI package|swarm/*|COMP-001|orchestration logic absent from any SKILL.md; `subprocess.run`-callable entry confirmed|S|P0|
|18|AC-004|Module layout mirrors `cli/sprint/` (constraint)|Required for operator continuity; binds NFR-007|swarm/*|NFR-007|reviewer confirms 1:1 module-role correspondence with sprint|S|P0|

### Integration Points — M1

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`swarm_group` Click group|CLI group registration|Group created, registered in `superclaude` entrypoint; subcommands deferred|M1|M7 (COMP-002 attaches subcommands)|
|atomic-write utility|Shared utility|Defined in M1|M1|M4, M5, M6 (all output writers)|
|`SwarmState` serializer|State registry|Read/write wired in M1|M1|M4, M5, M6, M7|

### Milestone Dependencies — M1

- None (foundation milestone).

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Domain-model rework if OQ-007/OQ-008 resolved late|Medium|Medium|WorkerSpec/status_policy fields churn|Resolve OQ-007/OQ-008 during M1 design; design `status_policy` for both warn and STOP semantics|architect|
|2|Atomic-write utility incorrect on non-POSIX-rename filesystems|Medium|Low|IMM-6 violated silently|Restrict to same-dir tmp + os.replace; document filesystem assumption; mid-write kill test in M8|backend|

## M2: Transport & Recipe Layers

**Objective:** Build the pluggable Transport Protocol (httpx reference + deterministic test stub) and the open-class Recipe Protocol registry with all six normalizers and the `custom-py:` dynamic loader. | **Duration:** 1 wk (W3) | **Entry:** M1 models defined | **Exit:** `TransportProtocol.dispatch` + `RecipeProtocol.normalize` interfaces stable; REGISTRY dict resolves all six recipes; `custom-py:mod:func` loader resolves a sample callable; stub transport returns deterministic responses.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-018|`transports` package — Transport Protocol|Pluggable HTTP transport interface package|transports|DM-010|package exposes Protocol + selection by `transport.kind`|S|P0|
|2|DM-010|`TransportProtocol` interface|Pluggable HTTP transport contract|transports/__init__|COMP-018|`dispatch(body:dict, timeout_sec:int) -> dict`; returns parsed JSON or raises typed transport errors for 4xx/5xx/timeout|S|P0|
|3|COMP-014|`recipes` package — normalizer registry|Open-class registry exposing Recipe Protocol + REGISTRY dict + `custom-py:` loader|recipes|DM-009|REGISTRY maps name→callable; `custom-py:mod:func` dynamic import works; unknown name raises|M|P0|
|4|DM-009|`RecipeProtocol` interface|Interface implemented by every normalizer|recipes/__init__|COMP-014|`normalize(raw_text:str, args:dict, template_path:str\|None) -> tuple[str,dict]`; returns normalized markdown + metadata; raises ParseError on unsalvageable input|S|P0|
|5|COMP-027|Recipe `bare_review_v1`|Ports existing `t2_normalize.py` logic into Recipe Protocol|recipes|DM-009|byte-equivalent normalization vs `t2_normalize.py` on fixture set; returns (md,meta)|M|P0|
|6|COMP-028|Recipe `findings_table_v1`|Extracted findings-table shape normalizer|recipes|DM-009|emits findings-table markdown; meta includes row count|S|P1|
|7|COMP-029|Recipe `hypothesis_table_v1`|Hypothesis-table shape normalizer|recipes|DM-009|emits hypothesis-table markdown; meta populated|S|P1|
|8|COMP-030|Recipe `verdict_only_v1`|Verdict-only shape normalizer|recipes|DM-009|emits verdict block; meta populated|S|P1|
|9|COMP-031|Recipe `passthrough`|Identity normalizer for non-Python harness post-processing|recipes|DM-009|returns raw text unchanged + empty meta; never raises ParseError|S|P0|
|10|COMP-032|Recipe `custom` — dynamic loader|Dynamic loader for `custom-py:module:func`|recipes|COMP-014|resolves `custom-py:` spec to callable; import errors surface actionable message|S|P1|
|11|FR-031|Recipe registry (open-class)|Provide `recipes/` registry with Recipe Protocol; ship all six recipes|recipes|COMP-014,COMP-027..032|REGISTRY contains bare_review_v1, findings_table_v1, hypothesis_table_v1, verdict_only_v1, passthrough, custom; each conforms to Protocol|S|P0|
|12|AC-006|Transport layer pluggable|Transport Protocol with `openai_compat.py` (Phase-1 ref) + `stub.py` (test)|transports|COMP-018|transport selected by spec field; no httpx import in dispatch logic outside transport|S|P0|
|13|AC-007|Recipe Protocol open-class with `custom-py:` loader|`custom-py:<module>:<callable>` Python-only; non-Python harnesses use `passthrough`|recipes|COMP-014|open-class extension verified by adding a recipe without core edits; passthrough documented for non-Python callers|S|P0|

### Integration Points — M2

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Recipe `REGISTRY` dict|Registry (open-class)|Populated with 6 recipes in M2|M2|M3 (recipe_name resolution), M6 (Wave 2 invocation)|
|`custom-py:` dynamic loader|Dynamic dispatch|Loader wired in M2|M2|M3 (validator), M6|
|Transport selection by `transport.kind`|Strategy/dispatch|`openai_compat` + `stub` registered in M2|M2|M5 (dispatch), M8 (stub-driven tests)|

### Milestone Dependencies — M2

- M1 (domain models for `DM-009`, `DM-010`).

### Open Questions — M2

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-005|Per-model overrides (e.g., per-model temperature) within one swarm?|Shapes Transport/WorkerSpec arg threading; relates to A-005 shared assumption (partially open)|architect|Deferred until a real lens asks; revisit before M5 dispatch finalization|

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|`bare_review_v1` diverges from `t2_normalize.py`|High|Medium|M9 A/B parity fails|Port logic verbatim; fixture-based byte-equivalence test in M8; freeze `t2_normalize.py` as golden reference|backend|
|2|`custom-py:` loader becomes arbitrary-code-exec vector|Medium|Low|Security surface widened|Python-only, caller-supplied module path; document trust boundary; never auto-resolve from untrusted spec fields|security|

## M3: Lens Registry & Validator

**Objective:** Build the bundled lens registry (`LensEntry` frozen dataclass + 8 entries) and the `_validate` submodule, plus the `validate-lenses` validation that hooks into `make verify-sync` / pre-commit. | **Duration:** 2 wk (W4–W5) | **Entry:** M1 models + M2 recipe REGISTRY available | **Exit:** `LENSES` dict resolves 8 entries; validator passes on bundled registry; every entry's `recipe_name` resolves against M2 REGISTRY; §11.5 substring present in each `system_prompt_fragment`; `suspect:true` entries include `{suspect_files}` in next-cmd template.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-016|`lenses` package — LENS REGISTRY|Bundled-policy registry exposing `LENSES` dict + `LensEntry` + helpers|lenses|DM-007|`LENSES` resolves all entries; helpers return entry by name; KeyError actionable|M|P0|
|2|DM-007|`LensEntry` frozen dataclass|Single registered lens definition|lenses/__init__|COMP-016|name:str(kebab-unique); description:str; system_prompt_fragment:str(verbatim,§11.5 substring); user_template:str({target_content}); output_template_path:str\|None; recipe_name:str(Protocol name or `custom-py:mod:func`); default_workers:int(2-4); default_target_line_cap:int=4000; suspect:bool; tier:str; recommended_next_command_template:str({compare_files}+optional{suspect_files}); acceptance_notes:str; stability:Literal[stable,experimental]=experimental|S|P0|
|3|COMP-017|`lenses._validate` validator submodule|Validate registry: file refs resolve, recipe resolution incl `custom-py:`, suspect→suspect_files coupling, name uniqueness, §11.5 substring|lenses/_validate|COMP-016,COMP-014|detects missing templates, unregistered recipes, suspect-without-{suspect_files}, dupes, missing §11.5 substring; exit non-zero with diagnostics|M|P0|
|4|COMP-019|Lens `bare-review` (stable)|First-class stable lens for sc-bare-review migration|lenses/bare_review|DM-007,COMP-027|stable; suspect:true; tier T2; default_workers=3; recipe bare_review_v1; next-cmd `/sc:adversarial --compare {compare_files} --suspect-source {suspect_files}`; §11.5 present|S|P0|
|5|COMP-020|Lens `refactor-find` (experimental)|Refactor-opportunity finder lens|lenses/refactor_find|DM-007|experimental; tier T2-code; default_workers=3; suspect:false; recipe + template resolve; §11.5 present|S|P1|
|6|COMP-021|Lens `edge-case-hunt` (experimental)|Edge-case discovery lens|lenses/edge_case_hunt|DM-007|experimental; tier T2-edge; default_workers=4; suspect:false; recipe + template resolve; §11.5 present|S|P1|
|7|COMP-022|Lens `spec-completeness` (experimental)|Spec-gap discovery lens|lenses/spec_completeness|DM-007|experimental; tier T2-spec; default_workers=3; suspect:false; recipe + template resolve; §11.5 present|S|P1|
|8|COMP-023|Lens `feasibility-probe` (experimental)|Feasibility-assessment lens|lenses/feasibility_probe|DM-007|experimental; tier T2-feas; default_workers=3; suspect:false; recipe + template resolve; §11.5 present|S|P1|
|9|COMP-024|Lens `troubleshoot-hypothesis` (experimental)|Hypothesis-generation lens|lenses/troubleshoot_hypothesis|DM-007|experimental; tier T2-tshoot; default_workers=4; suspect:false; recipe hypothesis_table_v1; §11.5 present|S|P1|
|10|COMP-025|Lens `doc-completeness` (experimental)|Documentation-gap lens|lenses/doc_completeness|DM-007|experimental; tier T2-doc; default_workers=3; suspect:false; recipe + template resolve; §11.5 present|S|P1|
|11|COMP-026|Lens `custom` (escape hatch)|Caller-supplied lens via `--custom-prompt-dir`|lenses/custom|DM-007|reads system.txt/user.txt/meta.yaml; injection-guard parity enforced (INV-003); never ships prompt content|S|P0|
|12|FR-038|Bundled lens registry (8 entries)|Registry at `cli/swarm/lenses/` with `LensEntry` + 8 entries|lenses|COMP-016..026|8 entries present; only bare-review + custom non-experimental policy honored; all except bare-review+custom ship experimental|M|P0|
|13|FR-039|Lens-driven defaults expansion|When `lens` set, preflight expands defaults into spec|lenses|COMP-016|expands prompt.system, prompt.user_template, normalization.recipe, normalization.template_path, workers.count, target.truncation.line_cap, output.filename_template, output.lens_name, recommended_next_command_template, caller_metadata.suspect, caller_metadata.tier; caller overrides lens; missing→schema error|M|P0|
|14|FR-040|Lens entry PR-review discipline|PR reviewers verify real caller, §11.5 sentence, normalizer fit, downstream-cmd validity, suspect scrutiny|lenses|FR-038|CONTRIBUTING/PR-template checklist exists; reviewer sign-off required for new entries|S|P1|
|15|FR-009|`swarm validate-lenses` validation|Validate bundled registry incl `custom-py:` resolution, suspect coupling, uniqueness, §11.5 substring; hookable via verify-sync/pre-commit|lenses/_validate|COMP-017|exit 0 on valid registry; non-zero + diagnostics on each failure class; hook-invocable|M|P0|
|16|NFR-008|PR-review gates for lens entries|Governance gate for new lens entries|lenses|FR-040|gate enumerated in PR template; covers real-caller, injection-guard, normalizer-fit, downstream-cmd, suspect justification|S|P1|
|17|AC-003|Lens registry bundled inside CLI package|Policy curation lives at `cli/swarm/lenses/` as plain Python dataclasses, not a plugin system|lenses|COMP-016|no separate plugin loader; entries are in-package dataclasses|S|P0|

### Integration Points — M3

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`LENSES` dict|Registry|Populated with 8 entries in M3|M3|M4 (lens resolution), M7 (`scaffold`, `--lens`)|
|`validate-lenses` validator|Validation hook|Wired into `make verify-sync` + pre-commit (pending OQ-001)|M3|M7 (CLI command wrapper), CI|
|`recipe_name` → REGISTRY binding|Cross-registry reference|Each entry's recipe_name validated against M2 REGISTRY|M3|M6 (Wave 2)|

### Milestone Dependencies — M3

- M1 (`DM-007`, models); M2 (recipe REGISTRY for `recipe_name` resolution).

### Open Questions — M3

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-001|Should `validate-lenses` run as a pre-commit hook by default?|Determines CI/hook wiring of FR-009|architect|Recommend yes; confirm before M3 exit, wire in M7|
|2|OQ-002|Per-lens version pinning (`--lens-version v2`)?|Affects LensEntry schema + manifest rehydration|architect|Deferred until lens definitions mutate frequently in production|

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Lens-registry sprawl|Medium|High|Registry bloat; unused entries|PR-review requires real caller (FR-040/NFR-008); entries without caller deferred to `custom-py:` + caller-side prompts; ship 6 as experimental|architect|
|2|Experimental lenses promoted to stable without a real caller|Medium|Medium|Stability contract eroded|Promotion to `stable` gated on production caller wiring; default `experimental`|architect|

## M4: Wave 0 — Preflight

**Objective:** Implement the preflight wave: JSON Schema validation, lens resolution + manifest materialization, env resolution, target read/truncate/checksum with IMM-4 empty-target guard, §11.5-delimited prompt composition across all three input paths, and manifest + state emission. | **Duration:** 2 wk (W6–W7) | **Entry:** M3 lens registry + M1 schema available | **Exit:** valid spec → `manifest.json` + `.swarm-state.json (preflight_ok)`; 49-byte target → `failed/target-too-small` before any dispatch; custom-prompt-dir without §11.5 substring STOPs; manifest captures full `resolved_lens_entry`.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-006|`preflight` module (Wave 0)|Lens resolution + materialization; custom-prompt-dir guard parity (INV-003); target ingest/checksum; IMM-4 guard|preflight|COMP-005,COMP-016,COMP-010|orchestrates FR-017..023; emits manifest + state; STOPs on guard/IMM-4 failures|L|P0|
|2|FR-017|JSON Schema validation of job spec|Validate spec via JSON Schema + cross-field rules + §11.5 required-substring on `prompt.system`|preflight|COMP-005|invalid spec → exit 2; §11.5 substring rule enforced on `prompt.system`; cross-field rules run|M|P0|
|3|FR-018|Lens resolution + manifest materialization|Resolve `--lens` against registry; snapshot `resolved_lens_entry` into `manifest.json`|preflight|COMP-016,DM-008|manifest captures name, system_prompt_fragment, user_template, recipe_name, default_workers, suspect, tier, recommended_next_command_template, stability|M|P0|
|4|FR-019|Environment resolution|Resolve env vars `T2ProxyUrl`, `T2ProxyKey`, `T2Model0N` defaults|preflight|COMP-003|env vars resolved; missing→actionable error; model list expanded from `T2Model0N`|S|P0|
|5|FR-020|Target read, truncate, checksum (IMM-4)|Read + truncate target; sha256[:12] provenance checksum; IMM-4 empty-target guard|preflight|COMP-003|<50 non-whitespace bytes after truncation → `failed/target-too-small` contract, STOP before dispatch; checksum recorded|M|P0|
|6|FR-021|Prompt composition with §11.5 injection-guard delimiters|Wrap target in `<<<TARGET>>>`/`<<<END TARGET>>>`; system prompt states data-vs-instructions separation; enforce across all 3 input paths|preflight|FR-017|delimiters applied; system prompt contains separation statement; INV-003/INV-014 parity across lens, JSON-Schema, custom-prompt-dir paths|M|P0|
|7|FR-022|Manifest + state emission at preflight|Emit `manifest.json` + `.swarm-state.json (preflight_ok)`|preflight|COMP-010,DM-008|both files written atomically; state=preflight_ok|S|P0|
|8|FR-023|Custom-prompt-dir guard parity (INV-003 fix)|When `lens=='custom'`, read system.txt/user.txt/meta.yaml; §11.5 substring check identical to other paths|preflight|FR-021,COMP-026|absent substring → STOP with actionable error; `--auto-inject-guard` opts into auto-prepend|M|P0|
|9|FR-044|Manifest-as-source-of-truth (INV-016 fix)|`manifest.resolved_lens_entry` is durable definition; registry mutations don't affect resumed job|preflight|FR-018,DM-008|manifest is authoritative for resume; mutation test (M8) confirms isolation|S|P0|
|10|NFR-002|Prompt-injection guard enforcement|§11.5 enforced across JSON Schema (`prompt.system`), lens validator (PR-time), `--custom-prompt-dir` preflight|preflight|FR-021, FR-023|all 3 paths enforce substring; STOP default; `--auto-inject-guard` opt-in|M|P0|
|11|AC-012|No file modification outside `--output`|Orchestrator must not modify target file or any file outside `--output`|preflight|COMP-006|target opened read-only; writes confined to `--output`; audit test in M8|S|P0|
|12|AC-014|No auto-detection of lens from target|Caller must explicitly pick lens|preflight|COMP-006|no content-sniffing; missing lens → error, never inferred|S|P0|

### Integration Points — M4

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`manifest.json` (`resolved_lens_entry`)|Durable source-of-truth|Materialized at preflight in M4|M4|M5 (dispatch reads prompt), M7 (resume rehydration)|
|§11.5 substring check|Validation gate (3-path)|Wired across schema + custom-prompt-dir in M4; PR-time in M3|M4|M5, M8 (injection tests)|
|`.swarm-state.json` transition `preflight_ok`|State transition|Emitted in M4|M4|M5, M7 (status/watch)|

### Milestone Dependencies — M4

- M1 (schema module, state, models); M3 (lens registry for resolution).

### Open Questions — M4

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-007|Workers > configured T2Models guard (INV-005): warn-on-exceed-with-defaults (V1) or STOP (V2)?|Determines preflight worker-count handling + WorkerSpec semantics|architect|Spec recommends warn; confirm before M4 dispatch-spec finalization|
|2|OQ-008|Empty-pool failure path (INV-007): write `failed/env-missing` contract OR pre-output-dir abort?|Determines preflight failure-contract shape|architect|Spec recommends write-on-failure when output dir creatable, pre-output-dir abort otherwise; confirm in M4|

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Custom-prompt-dir guard parity backward-compat break|Medium|Medium|Existing `--custom-prompt-dir` callers STOP unexpectedly|`--auto-inject-guard` flag preserves callers during migration window; document required §11.5 sentence|backend|
|2|Resume + lens-mutation inconsistency|Medium|Medium|Stale/inconsistent dispatch on `--resume`|Default rehydrates from `manifest.resolved_lens_entry` (INV-001); `--force-relens` opts into re-resolution; both paths tested in M8|architect|
|3|IMM-4 byte-count miscounts whitespace-heavy targets|Medium|Low|False reject/accept of small targets|Count non-whitespace bytes post-truncation; 49-byte boundary test (SC-003) in M8|backend|

## M5: Wave 1 — Parallel Dispatch

**Objective:** Implement code-enforced true-parallel dispatch via `ParallelExecutor` (ThreadPoolExecutor), per-worker httpx HTTP dispatch with JSON-escaped bodies, retry policy, hard timeout, and lock-coordinated worker-lifecycle event logging. Retire the V2 shell dispatch script. | **Duration:** 2 wk (W8–W9) | **Entry:** M4 preflight artifacts + M2 transport available | **Exit:** N workers run in one ParallelGroup (elapsed ≈ max, not Σ); each worker writes `.raw` + `.meta.json`; 5xx retried once, 4xx/timeout/network never retried; no shell-script dispatch path exists.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-007|`dispatch` module (Wave 1)|httpx-based ThreadPoolExecutor dispatch via `execution.parallel.ParallelExecutor`; timeout, retry, sidecar, event logging|dispatch|COMP-018,COMP-011|all N workers in one ParallelGroup; per-worker timeout + retry honored; sidecars emitted|L|P0|
|2|FR-024|True-parallel dispatch via ThreadPoolExecutor (IMM-3)|Single Python ThreadPoolExecutor via `ParallelExecutor`; all N workers in one ParallelGroup|dispatch|COMP-007|stub-worker test: elapsed ≈ max(per_worker)+ε, not Σ; parallelism code-enforced not attention-mediated|L|P0|
|3|FR-025|Per-worker HTTP dispatch (httpx)|Build body via `json.dumps` (never shell-interpolated); POST via httpx with per-worker timeout; write `.raw` + `.meta.json`|dispatch|COMP-018|body JSON-escaped; httpx POST; `.raw` + `.meta.json` sidecar written atomically per worker|M|P0|
|4|FR-026|Retry policy|On 5xx: retry once after `retry.on_5xx_backoff_sec`; on 4xx/timeout/network: no retry; always-record|dispatch|FR-025|5xx→1 retry; 4xx/timeout/network→0 retry; every worker recorded (no silent drops)|M|P0|
|5|FR-027|Per-worker hard timeout|Apply per-worker hard timeout (default 180s)|dispatch|FR-025|worker exceeding timeout → `timeout` status, no retry; does not block siblings|S|P0|
|6|FR-028|Event log emission (worker lifecycle)|Emit `worker_start`/`worker_progress`/`worker_done` under `threading.Lock`-guarded append|dispatch|COMP-011|three event types emitted; append lock-guarded; ordering preserved per worker|M|P0|
|7|FR-041|Python-only dispatch (INV-002 fix)|Python threads call httpx directly; V2 `swarm_dispatch.sh` retired; PIPE_BUF assumption documented as deprecated|dispatch|FR-024|no shell-script dispatch path exists; dual-writer race eliminated; deprecation noted in `docs/swarm-design-rationale.md`|M|P0|
|8|NFR-001|Code-enforced parallelism|Parallelism inside Python process via ThreadPoolExecutor, NOT attention-mediated|dispatch|FR-024|IMM-3 stub-parallelism test passes; no Claude-tool-call dependency in dispatch|M|P0|
|9|NFR-003|No shell interpolation|HTTP bodies built via `json.dumps` with target via `--arg`-equivalent; never shell-interpolated|dispatch|FR-025|grep audit: no shell string interpolation of target/body; injection-resistant body construction|S|P0|
|10|NFR-005|Lock-coordinated append for event log|JSONL writes under `threading.Lock`; `.swarm-state.json` under lock + atomic rename|dispatch|COMP-011|concurrent appends never interleave; state updates atomic; stress test in M8|M|P0|
|11|AC-005|ThreadPoolExecutor via `ParallelExecutor`|Reuse `superclaude.execution.parallel.ParallelExecutor`; no direct `concurrent.futures` in dispatch.py|dispatch|COMP-007|grep audit: no `concurrent.futures` import in dispatch.py; ParallelExecutor used|S|P0|
|12|AC-011|No Anthropic-model routing|Workers route only to T2-proxy-compatible external models|dispatch|FR-025|no Anthropic endpoints; transport targets T2 proxy only|S|P0|

### Integration Points — M5

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`ParallelExecutor` ThreadPoolExecutor|Concurrency engine (DI)|All workers placed in one ParallelGroup in M5|M5|M6 (consumes `.raw` outputs), M8 (IMM-3 test)|
|`threading.Lock`-guarded JSONL appender|Callback/lock-coordinated writer|Wired into worker lifecycle in M5|M5|M7 (monitoring), M8 (lock stress test)|
|Transport `dispatch()` binding|Strategy selection|Bound from M2 transport per `transport.kind`|M5|M8 (stub-transport tests)|

### Milestone Dependencies — M5

- M4 (preflight artifacts: composed prompt, manifest); M2 (Transport Protocol).

### Open Questions — M5

This milestone has no unresolved open questions (OQ-005 tracked under M2).

### Risk Assessment and Mitigation — M5

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|ThreadPoolExecutor surprise (operators expect process/async)|Low|Medium|Misuse / wrong perf expectations|Document model in `dispatch.py` docstring; test with stub transport; rationale in `docs/swarm-design-rationale.md`|backend|
|2|Lock contention degrades parallelism under high N|Medium|Low|Throughput loss|Lock guards only append/state-write, not HTTP; measure under stub load; keep critical section minimal|performance|
|3|Residual shell-dispatch references survive retirement|Medium|Low|INV-002 violated; dual-writer race returns|`tests/swarm/test_concurrency_python_only.py` (SC-008) asserts no shell path exercised; grep-audit in CI|backend|

## M6: Wave 2/3 — Normalize, Reduce, Merge

**Objective:** Implement Wave 2 (Recipe invocation per worker, parse-error salvage promotion, atomic final write) and Wave 3 (IMM-5 success-first status, three amalgamation modes, mechanical merge ≤30 LOC with structural guards, return contract + done sentinel emission). | **Duration:** 2 wk (W10–W11) | **Entry:** M5 dispatch produces `.raw` files; M2 recipes available | **Exit:** Wave 2 normalizes each worker atomically; salvage promotes parse_error→success; IMM-5 status parametrized cases pass; `merge.py` body ≤30 LOC, mechanical-concat-only boundary test passes; `return-contract.yaml` + `done.json` emitted.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-008|`normalize` module (Wave 2 dispatcher)|Wave 2 dispatcher; hosts Recipe Protocol interface use + registry lookup|normalize|COMP-014|invokes configured Recipe per worker; atomic write to deterministic final path|M|P0|
|2|COMP-009|`reduce` module (Wave 3)|Status determination per IMM-5; resume merge regeneration (INV-010); contract emission|reduce|COMP-015,COMP-010|computes status; regenerates merge on resume; writes contract|M|P0|
|3|COMP-015|`merge` module (mechanical concat)|Mechanical concat ONLY; body ≤30 LOC; allowed/disallowed ops in docstring; PR-review guarded|merge|COMP-009|≤30 LOC excl imports/docstring; concat in slot-index order with provenance header; no reorder/dedup/score|M|P0|
|4|FR-029|Recipe Protocol invocation per worker|For each worker, invoke configured Recipe; atomic write to deterministic final path (IMM-6)|normalize|COMP-008,FR-047|each `.raw`→Recipe→final atomically; deterministic path; sidecar updated|M|P0|
|5|FR-030|Parse-error salvage promotion|Promote `parse_error → success` if §7.4 salvage succeeds|normalize|FR-029|salvageable parse_error → success; unsalvageable retains parse_error + raw retained|M|P0|
|6|FR-032|Success-first status determination (IMM-5)|`M==N`→success first; `2≤M<N`→partial; `M<2`→failed; `M==N==2`→success; floor/success_first per-job configurable|reduce|COMP-009|parametrized cases pass: M==N, M==N==2, 2≤M<N, M<2; defaults floor=2, success_first=true|M|P0|
|7|FR-033|Three amalgamation modes|Support `raw` (Wave 2 pass-through), `normalize` (default, Recipe per worker), `normalize+merge` (normalize + mechanical concat)|reduce|COMP-008,COMP-015|raw skips Recipe; normalize runs Recipe; normalize+merge runs Recipe then concat|M|P0|
|8|FR-034|Mechanical merge with structural guards|Module ≤30 LOC; read each `final_path`, strip frontmatter, prepend `## From {model_label} ({elapsed_ms}ms)`, concat in slot-index order; no reorder/dedup/scoring/winner/claim-rewriting|merge|COMP-015|boundary test passes; LOC ≤30; CI rule flags boundary-test changes|M|P0|
|9|FR-035|Merge edge cases|`M=0`/`M=1`→`merged_path=null`; `M≥2`→merged with only successful workers; `--resume`+`normalize+merge` ALWAYS regenerates `merged.md` (INV-010)|reduce|COMP-015|null on M<2; merged contains only successes; resume regenerates unconditionally|S|P0|
|10|FR-036|Return contract emission|Write `return-contract.yaml` with version, status, job_id, timing, target info, worker counts, output_files, amalgamation_mode, merged_path, caller_metadata, recommended_next_command, artifacts|reduce|DM-003|all ResultContract fields populated; YAML stdlib-parseable|M|P0|
|11|FR-037|Done sentinel emission|Write `done.json` atomically; emit final event; exit 0 (status lives in contract, not RC)|reduce|FR-047|`done.json` written last, atomically; final event emitted; exit 0 even on partial/failed status|S|P0|
|12|NFR-006|Merge module LOC ceiling|`merge.py` body ≤30 LOC excl imports + docstring; allowed/disallowed in docstring; boundary test enforces|merge|FR-034|LOC counter asserts ≤30; docstring lists allowed/disallowed; boundary test in M8|S|P0|
|13|NFR-014|Idempotency on re-dispatch|Wave 2 re-runs over all `.raw`; existing successes re-write deterministically (no-op outcome)|normalize|FR-029|re-run produces byte-identical finals; no duplicate side-effects|S|P0|
|14|AC-009|No scored merge / dedup / reorder in orchestrator|Scored merging stays `/sc:adversarial`'s job; `normalize+merge` mechanical-concat-only|merge|FR-034|grep/AST audit: no scoring/dedup/reorder ops in merge.py; boundary test guards|S|P0|

### Integration Points — M6

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Recipe invocation per worker|Registry dispatch|Wave 2 looks up `normalization.recipe` in REGISTRY in M6|M6|M9 (bare_review_v1 parity)|
|`return-contract.yaml` emitter|Output contract|Assembled from DM-003 in M6|M6|M7 (CLI relays), M9 (A/B parity)|
|`done.json` terminal sentinel|Completion signal|Written atomically last in M6|M6|M7 (monitoring `until [ -f done.json ]`)|

### Milestone Dependencies — M6

- M5 (Wave 1 `.raw` outputs); M2 (Recipe REGISTRY).

### Open Questions — M6

This milestone has no unresolved open questions.

### Risk Assessment and Mitigation — M6

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Merge boundary erosion (drift into judging)|High|Medium|Boundary vs `/sc:adversarial` blurred; scope creep|Four structural guards: docstring allowed/disallowed list + ≤30 LOC ceiling + PR-review boundary note + `test_merge_mechanical_only.py` (SC-012); CI rule flags boundary-test changes|architect|
|2|IMM-5 ordering bug at `M==N==2` boundary|High|Low|Wrong terminal status reported to caller|Success-first ordering explicit; parametrized status test (SC-004) covers M==N==2; defaults floor=2|backend|
|3|Resume fails to regenerate `merged.md` (INV-010)|Medium|Medium|Stale merge artifact on resume|Wave 3 regenerates `merged.md` unconditionally when mode==normalize+merge; `test_resume_regenerates_merge.py` (SC-010)|backend|

## M7: CLI Surface, Observability, Resilience

**Objective:** Wire all 9 Click subcommands and run flags onto the wave pipeline; deliver the three durable observability layers and three monitoring patterns; the opt-in TUI; detached (tmux) mode; crash recovery + resume; and the non-precluding contract surface. | **Duration:** 3 wk (W12–W14) | **Entry:** M6 wave pipeline complete; M4 preflight resume hooks available | **Exit:** all 9 subcommands functional; exit codes 0/2/3/10 correct; `--resume` skips successes + regenerates merge; detached job survives caller termination + `attach`/`kill` work; non-TTY callers receive no control sequences; header-grep audit shows zero Claude tool-name references.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-002|`commands` module|Click subcommand definitions (run, status, logs, attach, kill, scaffold, validate, validate-lenses)|commands|COMP-001,COMP-006,COMP-007,COMP-008,COMP-009|all subcommands registered under group; each dispatches to correct wave/module|L|P0|
|2|COMP-011|`logging_` module|Dual JSONL + Markdown event log; lock-coordinated append|logging_|DM-006|JSONL append-only lock-guarded; Markdown human log; both durable|M|P0|
|3|COMP-012|`tui` module|Rich Live dashboard, flag-gated `--tui` (NOT default — INV-012)|tui|COMP-011|dashboard renders worker progress; only on `--tui` + TTY; non-TTY → no control sequences|M|P1|
|4|COMP-013|`tmux` module|Detached-run wrapper mirroring `sprint/tmux.py`|tmux|COMP-002|spawns detached tmux session; reattach + kill lifecycle; mirrors sprint pattern|M|P1|
|5|FR-001|New top-level CLI verb `superclaude swarm`|Click group at `cli/swarm/` separate from sprint/roadmap; third primitive|commands|COMP-001|`superclaude swarm` resolves; distinct from sprint/roadmap|S|P0|
|6|FR-002|CLI subcommand `swarm run`|Execute a swarm job from spec file, stdin, or `--lens` shortcut|commands|COMP-002|`swarm run <spec.yaml>` dispatches full pipeline; stdin + `--lens` paths work|M|P0|
|7|FR-003|CLI subcommand `swarm status`|Show job state (terminal or in-flight); `--watch` refreshes every 1s via Rich table|commands|COMP-010|`swarm status [--watch]` reads `.swarm-state.json`; watch refreshes 1s|S|P0|
|8|FR-004|CLI subcommand `swarm logs`|Tail or dump a job's execution log|commands|COMP-011|`swarm logs` tails/dumps JSONL + Markdown logs|S|P0|
|9|FR-005|CLI subcommand `swarm attach`|Re-attach to a detached (tmux) job's TUI|commands|COMP-013|`swarm attach <job_id>` reconnects to tmux session|S|P1|
|10|FR-006|CLI subcommand `swarm kill`|Terminate a running detached job|commands|COMP-013|`swarm kill <job_id>` terminates session; state updated|S|P1|
|11|FR-007|CLI subcommand `swarm scaffold`|Emit a starter job-spec file for a named lens|commands|COMP-016|`swarm scaffold --lens <name>` writes valid starter spec|S|P1|
|12|FR-008|CLI subcommand `swarm validate`|Validate a job-spec file without dispatching|commands|COMP-005|`swarm validate <spec.yaml>` runs schema + cross-field; exit 2 on failure; no dispatch|S|P0|
|13|FR-010|`swarm run --lens <name>` flag|Resolve lens-registry entry; caller may omit prompt/recipe/template fields|commands|FR-018|`--lens` resolves; omitted fields filled from lens defaults|S|P0|
|14|FR-011|`swarm run --custom-prompt-dir <path>` flag|When `--lens custom`, point at dir with system.txt/user.txt/meta.yaml|commands|FR-023|`--custom-prompt-dir` read; guard parity enforced|S|P0|
|15|FR-012|`swarm run --auto-inject-guard` flag|Backward-compat; auto-prepends canonical §11.5 sentence|commands|FR-023|absent §11.5 substring + flag → auto-prepend; without flag → STOP|S|P0|
|16|FR-013|`swarm run --amalgamation-mode {raw,normalize,normalize+merge}` flag|Select amalgamation mode (default normalize)|commands|FR-033|flag selects mode; default normalize; invalid value rejected|S|P0|
|17|FR-014|`swarm run --tui` flag|Opt-in Rich Live dashboard (NOT default — INV-012)|commands|COMP-012|`--tui` enables dashboard; non-TTY callers unaffected|S|P1|
|18|FR-015|`swarm run --force-relens` flag|On `--resume`, ignore manifest's `resolved_lens_entry` and re-resolve from current registry|commands|FR-043|default rehydrates from manifest; `--force-relens` re-resolves|S|P1|
|19|FR-016|Exit codes|`0`=reached Wave 3; `2`=spec validation failure; `3`=preflight failure; `10`=orchestrator internal error|commands|COMP-002|all four codes returned in correct conditions; status lives in contract not RC|S|P0|
|20|FR-042|Crash semantics|Orchestrator crash mid-dispatch: state retains last-known; completed workers have sidecars; no `done.json`|state|COMP-010|post-crash inspection shows partial progress recoverable; no false `done.json`|M|P0|
|21|FR-043|`swarm run --resume <job_id>` workflow|Re-run Wave 0 in resume mode: rehydrate lens from manifest (INV-001); skip successes; re-dispatch rest; re-run Wave 2; regenerate merge (INV-010); reduce + contract|commands|FR-044,COMP-009|6-step resume path executes; successes skipped; merge regenerated when mode==normalize+merge|L|P0|
|22|FR-045|Three durable observability layers|`.swarm-state.json` (atomic on transition), `execution-log.jsonl` (append-only, lock-coordinated), `execution-log.md` (human), `done.json` (terminal sentinel)|logging_|COMP-011,COMP-010|all four artifacts emitted + durable across crash|M|P0|
|23|FR-046|Three monitoring caller patterns|`Bash run_in_background`+`until [ -f done.json ]`; `Monitor` tool tailing JSONL; `swarm status --watch` Rich table|logging_|FR-045, FR-003|all three patterns documented + functional against live job|M|P1|
|24|FR-048|Detached mode via tmux|`--detached` via tmux wrapper mirroring `sprint/tmux.py`; detached + `--resume` + `attach`/`kill` lifecycle|tmux|COMP-013|`--detached` job survives caller termination; full lifecycle works|M|P1|
|25|FR-050|Non-precluding contract surface|Job spec, result contract, CLI surface, monitoring contract have zero Claude tool-name references; `caller.kind` informational only; `subprocess.run`-callable|commands|DM-001,DM-003|header-grep audit (SC-015) passes; `caller.kind` never routes|M|P0|
|26|NFR-010|Spec-version forward compatibility|Orchestrator at `1.1` can load specs at `1.0`; forward-compat best-effort|schema|FR-017|1.1 orchestrator loads 1.0 spec; unknown future fields tolerated best-effort|S|P1|
|27|NFR-011|Cross-language callability|`subprocess.run(["superclaude","swarm","run",...])` from any language; JSON/YAML stdlib-parseable contracts|commands|FR-050|subprocess invocation from non-Python harness works; contracts stdlib-parseable|S|P0|
|28|NFR-012|TUI opt-in (output discipline)|Rich Live dashboard NOT default; non-TTY callers receive no terminal control sequences|tui|COMP-012|default run emits no control sequences; `--tui` + TTY required for dashboard|S|P0|
|29|AC-008|No third-party agent-harness integration in scope|openharness/openhands/Assistants/LangGraph/CrewAI out of scope; contract non-precluding|commands|FR-050|no harness-specific code; contract surface harness-agnostic|S|P0|
|30|AC-010|No streaming, function-calling, or vision input (Phase 1)|Inherited from parent spec §7.3|transports|COMP-018|transport rejects/ignores streaming/function-calling/vision in Phase 1|S|P1|
|31|AC-013|No response caching across invocations|Each invocation re-dispatches|dispatch|COMP-007|no cache layer; identical inputs re-dispatch|S|P1|
|32|AC-015|No auto-execution of `recommended_next_command`|Always a suggestion, never an action|reduce|FR-036|`recommended_next_command` printed only; never executed by orchestrator|S|P0|
|33|AC-016|`caller.kind` is informational only|Never used for routing|commands|FR-050|grep audit: `caller.kind` never branches control flow|S|P0|
|34|AC-017|Parent-spec IMM-N invariants carry forward verbatim or stronger|IMM-3/4/5/6 + §11.5 inherited from bare-review v1.3.0-draft; no weakening|swarm/*|—|all IMM-N + §11.5 tests (M8) pass; no invariant weakened vs parent|S|P0|

### Integration Points — M7

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|9 Click subcommands|CLI dispatch table|All subcommands registered onto `swarm_group` in M7|M7|M9 (thin caller exec's `swarm run`)|
|`run` flag set (8 flags)|CLI option binding|Flags bound to pipeline params in M7|M7|M9, human callers|
|tmux detached wrapper|Process-lifecycle binding|Wired in M7 (mirrors sprint/tmux.py)|M7|M8 (SC-014 end-to-end)|
|Monitoring patterns (3)|Observability callbacks|JSONL tail + done.json sentinel + status --watch wired in M7|M7|external callers, M8|

### Milestone Dependencies — M7

- M6 (wave pipeline + contract); M4 (preflight resume rehydration).

### Open Questions — M7

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-003|Should `recommended_next_command` ever be auto-executed via `--auto-handoff`?|Affects AC-015 boundary + CLI flag surface|architect|Deferred; AC-015 holds (suggestion-only) for v1|
|2|OQ-004|Prometheus / OpenMetrics output at event boundaries?|Affects observability layer + logging_ module|devops|Deferred beyond v1|
|3|OQ-006|Concurrent-`--output`-dir protection?|Affects state/lock model for shared output dirs|architect|Deferred; document caller-must-avoid for v1|

### Risk Assessment and Mitigation — M7

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Tmux dependency unavailable in caller environment|Medium|Medium|Detached mode fails|Detached mode optional; inline mode default; preflight detects tmux + actionable error|devops|
|2|Schema evolution drag as `spec_version` advances|Low|Low|Forward-compat maintenance burden|1.1 loads 1.0 best-effort; version-gate cross-field rules; document evolution policy|architect|
|3|TUI control sequences leak to non-TTY callers|Medium|Low|Corrupted contract output for `subprocess.run` callers|TUI strictly `--tui` + TTY gated (NFR-012/INV-012); non-TTY test in M8|frontend|
|4|Claude tool-name reference leaks into contract surface|Medium|Low|Non-precluding contract (NFR-011) violated|Header-grep audit `test` (SC-015) over models.py, schema.py, contract YAML, `--help`|architect|

## M8: Invariant Test Suite & Verification

**Objective:** Author the acceptance test for every IMM-N and INV-NNN invariant plus the merge-boundary, validate-lenses, detached-lifecycle, and non-precluding-surface checks. Every invariant gets a named test using the deterministic stub transport. | **Duration:** 1 wk (W15) | **Entry:** M5/M6/M7 complete | **Exit:** all SC-002..SC-015 tests pass green; full suite runs via `uv run pytest tests/swarm/`; CI rule guarding merge-boundary test active.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|NFR-013|Test coverage of invariants|Every IMM-N + INV-NNN invariant has an acceptance test|tests/swarm|—|tests exist for IMM-3/4/5/6, §11.5, INV-001/002/003/010/014, §10.2 boundary|M|P0|
|2|SC-002|IMM-3 stub-worker parallelism test|N stub workers complete within `max(per_worker_elapsed)+ε`, NOT `Σ`|tests/swarm|FR-024,COMP-018|elapsed asserts ≈ max + ε; defined-worker fleet via stub transport|S|P0|
|3|SC-003|IMM-4 49-byte target test|Target <50 non-whitespace bytes → `failed/target-too-small` before dispatch|tests/swarm|FR-020|49-byte target → failed contract; zero dispatch calls|S|P0|
|4|SC-004|IMM-5 parametrized status test|Cover `M==N`, `M==N==2`, `2≤M<N`, `M<2` with success_first=true ordering|tests/swarm|FR-032|all four cases assert correct terminal status|S|P0|
|5|SC-005|IMM-6 mid-write kill test|Process killed during output write leaves no partial file at deterministic final path|tests/swarm|FR-047|kill mid-write → no partial final; previous content intact|S|P0|
|6|SC-006|§11.5 target-containing-end-marker test|Target text containing `<<<END TARGET>>>` literal does not allow injection past delimiter|tests/swarm|FR-021|embedded end-marker neutralized; instructions not escaped|S|P0|
|7|SC-007|INV-001 resume-uses-manifest-lens test|`--resume` reads `resolved_lens_entry` from manifest, ignores mutated registry|tests/swarm|FR-043, FR-044|`test_resume_uses_manifest_lens.py`: mutated registry ignored on resume|S|P0|
|8|SC-008|INV-002 concurrency-python-only test|No shell-script dispatch path exercised; all parallelism via Python ThreadPoolExecutor|tests/swarm|FR-041|`test_concurrency_python_only.py`: no shell path; ParallelExecutor used|S|P0|
|9|SC-009|INV-003 custom-prompt-dir injection-guard test|`--custom-prompt-dir` without §11.5 substring STOPs; with `--auto-inject-guard` prepends canonical sentence|tests/swarm|FR-023, FR-012|`test_custom_prompt_dir_injection_guard.py`: STOP vs auto-prepend both verified|S|P0|
|10|SC-010|INV-010 resume-regenerates-merge test|`--resume` + `normalize+merge` always regenerates `merged.md` after Wave 2|tests/swarm|FR-035|`test_resume_regenerates_merge.py`: merge regenerated unconditionally|S|P0|
|11|SC-011|INV-014 escape-hatch-guard-parity test|Escape-hatch path enforces injection guard identically to lens-driven + JSON-Schema paths|tests/swarm|FR-021, FR-023|`test_escape_hatch_guard_parity.py`: parity across all 3 paths|S|P0|
|12|SC-012|Merge-boundary mechanical-only test|3-worker concat → all 3 sections in slot-index order, only provenance header added; module body ≤30 LOC|tests/swarm|FR-034,NFR-006|`test_merge_mechanical_only.py`: order preserved, no transforms; LOC ≤30; CI flags changes|S|P0|
|13|SC-013|`validate-lenses` exit-code test|Exit 0 on valid 8-entry registry; non-zero + diagnostics for missing templates, unregistered recipes, suspect-without-{suspect_files}, dupes, missing §11.5|tests/swarm|FR-009|all failure classes produce non-zero + diagnostic; valid registry → exit 0|S|P0|
|14|SC-014|Detached + resume + attach end-to-end test|Long-running job survives caller termination, resumes via `swarm run --resume`, attaches via `swarm attach`, terminates via `swarm kill`|tests/swarm|FR-048, FR-043|full detached lifecycle demonstrated end-to-end|M|P1|
|15|SC-015|Non-precluding contract-surface audit|Header-grep: zero Claude tool-name references in models.py, schema.py, result-contract YAML, CLI `--help`|tests/swarm|FR-050|grep audit returns zero matches across all four surfaces|S|P0|

### Integration Points — M8

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Stub transport fixture|Test DI/strategy|Deterministic stub bound for all invariant tests in M8|M8|CI, M9 (parity harness reuse)|
|Merge-boundary CI rule|CI guard|Flags any change to `test_merge_mechanical_only.py` in M8|M8|ongoing PR review|

### Milestone Dependencies — M8

- M5 (dispatch), M6 (normalize/reduce/merge), M7 (CLI/resume/detached).

### Open Questions — M8

This milestone has no unresolved open questions.

### Risk Assessment and Mitigation — M8

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Mid-write kill test (SC-005) flaky across OSes|Medium|Medium|CI instability|Use signal-based deterministic kill point; same-dir tmp guarantee; retry-tolerant assertion on final-path absence|qa|
|2|Detached lifecycle test (SC-014) requires tmux in CI|Medium|Medium|CI cannot run SC-014|Gate SC-014 behind tmux-available marker; provide local-run instructions; inline-mode fallback tests always run|qa|
|3|Stub transport drifts from real T2 proxy semantics|Medium|Low|Tests pass but production differs|Pin stub to documented OpenAI-compat response shape; periodic contract check against real proxy in M9|backend|

## M9: sc-bare-review Migration & A/B Parity

**Objective:** Rewrite `sc-bare-review` SKILL.md as a ~60-line thin caller over `--lens bare-review`, run an A/B parity test against current output, observe production parity across a window, and delete the legacy `scripts/*.sh`. | **Duration:** 1 wk (W16) | **Entry:** M8 invariant suite green | **Exit:** SKILL.md ~60 lines; `scripts/*.sh` deleted; A/B parity observed (byte-equivalent modulo timestamps/checksums); backward-compat path documented for `--custom-prompt-dir` users.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-033|`sc-bare-review` thin-caller SKILL.md|~60-line skill that builds `--lens bare-review` job spec, exec's `superclaude swarm run`, relays return contract|sc-bare-review|COMP-001,COMP-019|SKILL.md ~60 lines; builds spec; exec's CLI; relays contract; no orchestration prose|M|P1|
|2|FR-049|sc-bare-review migration to thin caller|Rewrite SKILL.md as thin caller; A/B parity test against current output; `scripts/*.sh` deleted|sc-bare-review|COMP-033|migration complete; A/B parity test exists + passes; legacy scripts removed|M|P1|
|3|SC-001|A/B parity acceptance|`swarm run --lens bare-review ... --workers 3` produces `return-contract.yaml` byte-equivalent (modulo timestamps + checksums) to today's sc-bare-review output|tests/swarm|FR-049,COMP-027|A/B harness asserts byte-equivalence modulo volatile fields|M|P1|
|4|SC-016|Migration completeness|After Phase 9: SKILL.md ~60 lines, all `scripts/*.sh` deleted, production parity observed across A/B window|sc-bare-review|FR-049,SC-001|line count ≤~60; zero `scripts/*.sh`; parity window observed clean|S|P1|
|5|NFR-009|Backward compatibility migration path|`--auto-inject-guard` preserves existing `--custom-prompt-dir` callers during §11.5 enforcement rollout|sc-bare-review|FR-012|documented migration window; flag preserves callers; sunset plan noted|S|P1|

### Integration Points — M9

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`sc-bare-review` thin caller|Caller→CLI binding|SKILL.md exec's `swarm run --lens bare-review` in M9|M9|production review workflow|
|A/B parity harness|Test/validation|Compares thin-caller output vs legacy in M9|M9|release gate|

### Milestone Dependencies — M9

- M8 (invariant suite must be green before migration cutover).

### Open Questions — M9

This milestone has no unresolved open questions.

### Risk Assessment and Mitigation — M9

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|A/B parity fails due to `bare_review_v1` normalization drift|High|Medium|Migration blocked; rollback needed|Port `t2_normalize.py` verbatim (M2); fixture byte-equivalence; keep legacy path until parity window closes clean|backend|
|2|Premature `scripts/*.sh` deletion before parity confirmed|Medium|Low|Loss of rollback path|Delete scripts only after parity window observed clean (SC-016); retain in git history|architect|
|3|Existing `--custom-prompt-dir` callers break on §11.5 enforcement|Medium|Medium|Caller-facing regression|`--auto-inject-guard` (NFR-009) during migration window; comms + docs before enforcement default|backend|

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By Milestone|Status|Fallback|
|---|---|---|---|
|`superclaude.execution.parallel.ParallelExecutor`|M5|Available (internal)|None — mandated by AC-005|
|`httpx`|M2, M5|Available (PyPI)|`requests` (would require transport rewrite)|
|`click`|M1, M7|Available (existing dep)|None|
|`rich`|M7|Available (existing dep)|Plain-text status fallback (TUI is opt-in)|
|`tmux`|M7|System dependency, may be absent|Inline mode default; detached gated on tmux presence|
|`threading.Lock` / `os.replace`|M1, M5|Python stdlib|None|
|T2 proxy (OpenAI-compatible, `T2ProxyUrl`/`T2ProxyKey`/`T2Model0N`)|M5|External service|Stub transport for tests; STOP with env-missing contract in prod|
|Lens template files (`refs/templates/<lens>-output.md`)|M3|To be authored per stable lens|Lens fails validation if missing|
|Parent spec `bare-review v1.3.0-draft` (IMM-N, §11.5, §7.4)|M1, M6, M8|Available (reference)|None — invariants inherited verbatim|
|`/sc:adversarial` downstream command|M3, M6|Available|Lens `recommended_next_command` is suggestion-only (AC-015)|
|`sprint/tmux.py` (mirrored pattern)|M7|Available (internal)|None|

### Infrastructure Requirements

- Python ≥3.10 with UV-managed environment; `uv run pytest tests/swarm/` as the test entrypoint.
- CI runner with optional tmux for SC-014 (detached lifecycle), gated behind a tmux-available marker.
- Network egress to the T2 proxy for production runs; deterministic stub transport for all CI/test runs (no live proxy in CI).
- `make verify-sync` + pre-commit hook surface for `validate-lenses` (OQ-001 wiring).
- CI rule that flags any change to `tests/swarm/test_merge_mechanical_only.py` (merge-boundary guard).

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|Mitigation|Owner|
|----|------|---------------------|-------------|--------|------------|-------|
|R-01|Merge boundary erosion (drift into judging/scoring)|M6, M8|Medium|High|Four structural guards (docstring allowed/disallowed + ≤30 LOC + PR-review note + boundary test SC-012) + CI rule flagging boundary-test changes|architect|
|R-02|Lens-registry sprawl|M3|High|Medium|PR-review requires real caller (FR-040/NFR-008); no-caller entries deferred to `custom-py:`; 6 entries ship experimental|architect|
|R-03|Resume + lens-mutation interaction|M4, M7|Medium|Medium|Default rehydrates from `manifest.resolved_lens_entry` (INV-001); `--force-relens` opt-in; both paths tested (SC-007)|architect|
|R-04|Tmux dependency for detached mode|M7, M8|Medium|Medium|Detached optional; inline default; tmux-presence preflight; SC-014 gated behind marker|devops|
|R-05|ThreadPoolExecutor surprise (process/async expectation)|M5|Medium|Low|Documented in dispatch docstring + design rationale; stub-tested (SC-002/SC-008)|backend|
|R-06|Custom-prompt-dir guard parity backward-compat|M4, M9|Medium|Medium|`--auto-inject-guard` flag during migration window (NFR-009); parity test SC-011|backend|
|R-07|Schema evolution drag (`spec_version`)|M7|Low|Low|1.1 loads 1.0 best-effort; version-gated cross-field rules; documented policy|architect|
|R-08|`bare_review_v1` normalization drift vs `t2_normalize.py`|M2, M9|Medium|High|Verbatim port; fixture byte-equivalence; legacy path retained until A/B window clean (SC-001)|backend|
|R-09|IMM-5 success-first ordering bug at boundaries|M6, M8|Low|High|Explicit success-first ordering; parametrized status test SC-004 incl M==N==2|backend|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|Milestone|
|---|---|---|---|---|
|SC-001 A/B parity|Contract byte-equivalence (modulo timestamps/checksums)|100% equivalent|A/B harness vs legacy bare-review|M9|
|SC-002 IMM-3 parallelism|Elapsed vs max(per-worker)|≈ max + ε (not Σ)|Stub-worker parallelism test|M8|
|SC-003 IMM-4 empty-target|49-byte target outcome|`failed/target-too-small`, zero dispatch|Boundary test|M8|
|SC-004 IMM-5 status|Status across M==N/M==N==2/2≤M<N/M<2|All correct, success-first|Parametrized status test|M8|
|SC-005 IMM-6 atomicity|Partial file after mid-write kill|None at final path|Mid-write kill test|M8|
|SC-006 §11.5 injection|Embedded `<<<END TARGET>>>` outcome|No injection past delimiter|End-marker test|M8|
|SC-007 INV-001 resume lens|Lens source on resume|Manifest, not mutated registry|`test_resume_uses_manifest_lens.py`|M8|
|SC-008 INV-002 python-only|Shell dispatch path exercised|None; ThreadPoolExecutor only|`test_concurrency_python_only.py`|M8|
|SC-009 INV-003 guard|Custom-prompt-dir without §11.5|STOP / auto-prepend with flag|`test_custom_prompt_dir_injection_guard.py`|M8|
|SC-010 INV-010 resume merge|`merged.md` on resume+normalize+merge|Always regenerated|`test_resume_regenerates_merge.py`|M8|
|SC-011 INV-014 parity|Guard enforcement across 3 paths|Identical|`test_escape_hatch_guard_parity.py`|M8|
|SC-012 merge boundary|Sections order + transforms + LOC|Slot order, provenance-only, ≤30 LOC|`test_merge_mechanical_only.py`|M8|
|SC-013 validate-lenses|Exit codes per failure class|0 valid / non-zero + diagnostics|Validator exit-code test|M8|
|SC-014 detached lifecycle|Survive termination + attach/kill|Full lifecycle works|End-to-end detached test|M8|
|SC-015 non-precluding surface|Claude tool-name references|Zero across 4 surfaces|Header-grep audit|M8|
|SC-016 migration completeness|SKILL.md lines + scripts + parity window|≤~60 lines, 0 scripts, clean window|Migration audit|M9|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|----------|--------|------------------------|----------|
|Orchestrator home|CLI package (`cli/swarm/`)|SKILL.md prose orchestration|Code enforces parallelism + invariants where prose cannot; `subprocess.run`-callable; durable observability/detached/resume first-class (AC-002)|
|Concurrency engine|Python ThreadPoolExecutor via `ParallelExecutor`|Shell `swarm_dispatch.sh`; asyncio; multiprocessing|Eliminates dual-writer race + PIPE_BUF assumption; reuses internal abstraction; I/O-bound HTTP fits threads (INV-002/AC-005)|
|Policy curation|Bundled in-package lens dataclasses|Separate plugin system|Simpler governance; PR-review discipline; no plugin loader surface (AC-003)|
|Merge semantics|Mechanical concat ≤30 LOC, 4 guards|Scored/dedup/winner-select merge|Keeps scoring as `/sc:adversarial`'s job; prevents boundary erosion (AC-009/R-01)|
|Resume source-of-truth|`manifest.resolved_lens_entry` (rehydrate)|Re-resolve from live registry|Registry mutations must not alter a resumed job; `--force-relens` opt-in (INV-001/INV-016)|
|Injection-guard policy|STOP by default, `--auto-inject-guard` opt-in|Always auto-inject; warn-only|Security-first across 3 input paths; backward-compat flag for migration (NFR-002/NFR-009)|
|TUI default|Opt-in `--tui` only|TUI on by default|Non-TTY callers must not receive control sequences (NFR-012/INV-012)|

## Timeline Estimates

|Milestone|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1 Foundation & Domain Models|2 wk|W1|W2|Package + all DM dataclasses + atomic-write utility|
|M2 Transport & Recipe Layers|1 wk|W3|W3|Transport + Recipe protocols + 6 recipes + custom-py loader|
|M3 Lens Registry & Validator|2 wk|W4|W5|8 lens entries + validator + validate-lenses|
|M4 Wave 0 — Preflight|2 wk|W6|W7|Schema + lens materialization + IMM-4 + §11.5 composition|
|M5 Wave 1 — Parallel Dispatch|2 wk|W8|W9|ThreadPoolExecutor dispatch + retry/timeout + event log; shell retired|
|M6 Wave 2/3 — Normalize, Reduce, Merge|2 wk|W10|W11|IMM-5 status + 3 amalgamation modes + mechanical merge + contract|
|M7 CLI Surface, Observability, Resilience|3 wk|W12|W14|9 subcommands + resume + detached + monitoring + non-precluding surface|
|M8 Invariant Test Suite & Verification|1 wk|W15|W15|SC-002..SC-015 all green; merge-boundary CI rule|
|M9 sc-bare-review Migration & A/B Parity|1 wk|W16|W16|Thin caller + A/B parity + scripts deleted|

**Total estimated duration:** 16 weeks (W1–W16)
