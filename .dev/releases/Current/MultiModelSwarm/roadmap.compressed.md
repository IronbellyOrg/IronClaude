---
spec_source: "merged-requirements.compressed.md"
complexity_score: 0.85
complexity_class: HIGH
primary_persona: architect
adversarial: true
base_variant: "A"
variant_scores: "A:81 B:74"
convergence_score: 0.55
---

# Multi-Model Swarm Orchestrator — Project Roadmap

## Executive Summary

This roadmap delivers `superclaude swarm`, a new top-level CLI verb that orchestrates N concurrent model workers against a single target through a deterministic four-wave pipeline (preflight → dispatch → normalize → reduce). It replaces the prior attention-mediated "single message, N tool calls" parallelism and the retired shell `swarm_dispatch.sh` with a code-enforced Python `ThreadPoolExecutor` invoked through the existing `superclaude.execution.parallel.ParallelExecutor`. The system is caller-agnostic: it carries zero Claude-Code-isms in its job spec, result contract, CLI surface, or monitoring contract, so any language can drive it via `subprocess.run(["superclaude", "swarm", "run", ...])`.

The architecture decomposes into 35+ components across six subsystems (orchestrator modules, recipe registry, lens registry, transport layer, templates, data models) and must carry forward five parent IMM invariants verbatim plus seven INV-xxx fault-finder remediations. The defining architectural tension is the **merge boundary**: `normalize+merge` mode performs mechanical concatenation only, and four structural guards (docstring contract, ≤30 LOC ceiling, PR-review discipline, boundary test) exist to prevent it from ever drifting into scoring, deduplication, or judging — that responsibility stays exclusively with the unchanged `/sc:adversarial` scored-merge pipeline.

**Business Impact:** Converts a fragile, attention-dependent multi-model review capability into a durable, resumable, observable CLI primitive reusable across 8 analytical lenses (bare-review, refactor-find, edge-case-hunt, spec-completeness, feasibility-probe, troubleshoot-hypothesis, doc-completeness, custom). It makes T2 swarm review a first-class, non-Claude-callable building block while migrating the existing `sc-bare-review` skill to a ~60-line thin caller with A/B-verified output parity, and lands first-class operational handoff (runbook, env readiness, rollback) so production adoption is not a byproduct of feature completion.

**Complexity:** HIGH (0.85) — driven by module breadth (14+ orchestrator modules plus recipes and lenses), cross-cutting integration (new CLI verb + ParallelExecutor integration + 10-phase skill migration), verbatim invariant enforcement (5 IMM + 7 INV + §11.5 across 3 prompt-input paths), concurrency correctness (lock-coordinated JSONL, atomic state transitions, resume with manifest rehydration), and a multi-rule schema/registry validation surface.

**Critical path:** M1 (data models + module shape) → M2 (preflight + lens registry + injection guard + INV-005/007 pool guards) → M3 (dispatch + concurrency) → M4 (normalize + recipes + per-lens templates) → M5 (reduce + merge + status) → M6 (resume + manifest) → M7 (observability + full CLI surface) → M8 (skill migration + enumerated migration items + per-IMM/INV test suite) → M9 (operational handoff). M2→M3→M4→M5 is the irreducible wave-pipeline spine; M6 depends on M5's merge regeneration, M8 cannot complete until pipeline and contract are stable, and M9 finalizes production handoff before release.

**Key architectural decisions:**

- Code-enforced parallelism via `ParallelExecutor`/`ThreadPoolExecutor` (IMM-3, INV-002), retiring shell dispatch and the PIPE_BUF assumption entirely.
- Mechanical-only merge isolated to a ≤30 LOC module behind four structural guards (FR-012, NFR-008/009, AC-011/012/018); no scoring engine is introduced.
- Manifest as durable source-of-truth for resume (INV-016): resume rehydrates the resolved lens verbatim and never re-resolves unless `--force-relens` is passed.
- Production handoff is a first-class milestone (M9), not a documentation afterthought — runbook, environment readiness check, rollback procedure, and lens contribution policy ship as named deliverables with owners.

**Open risks requiring resolution before M1:**

- T2 proxy endpoint availability and env-var contract (`T2ProxyUrl`/`T2ProxyKey`/`T2Model0N`) must be confirmed reachable in CI/dev before dispatch can be exercised end-to-end (Dependency #8); until then dispatch is validated only against the stub transport.
- OQ-006 (concurrent `--output` dir protection), OQ-008 (empty-pool failure contract), and OQ-009 (`caller_metadata.suspect` precedence) require named owners before M1 exit so the data models freeze cleanly.

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|----|-------|------|----------|--------|--------------|--------------|------|
|M1|Foundation, Module Shape & Data Models|Foundation|P0|L|—|29|LOW|
|M2|Preflight, Schema, Lens Registry & Injection Guard (Wave 0)|Core|P0|XL|M1|29|HIGH|
|M3|Dispatch & Concurrency (Wave 1)|Core|P0|XL|M2|26|MEDIUM|
|M4|Normalize & Recipe Registry (Wave 2)|Core|P0|L|M3|13|MEDIUM|
|M5|Reduce, Merge, Status & Result Contract (Wave 3)|Core|P0|L|M4|11|HIGH|
|M6|Resume, Crash Recovery & Manifest|Reliability|P1|M|M5|8|MEDIUM|
|M7|Observability, TUI, Detached & Full CLI Surface|Operability|P1|L|M5|17|LOW|
|M8|Migration, Test Discipline & Hardening|Migration|P1|M|M6,M7|13|MEDIUM|
|M9|Operational Handoff|Release|P1|S|M8|6|MEDIUM|

## Dependency Graph

```
M1 (Foundation) → M2 (Preflight/Lens/Guard) → M3 (Dispatch) → M4 (Normalize) → M5 (Reduce/Merge)
                                                                                    ├─→ M6 (Resume/Manifest) ─┐
                                                                                    └─→ M7 (Observability/CLI) ┤
                                                                                                              └─→ M8 (Migration) ─→ M9 (Operational Handoff)
```

- M1 has no prerequisites (foundation).
- M2 → M1 (data models, schema dataclasses).
- M3 → M2 (preflight + resolved lens entry feed dispatch).
- M4 → M3 (worker outputs feed normalization).
- M5 → M4 (normalized worker outputs feed reduce + merge).
- M6 → M5 (resume regenerates merge; needs reduce + manifest).
- M7 → M5 (full CLI surface + monitoring wrap a stable pipeline).
- M8 → M6, M7 (skill migration requires resumable pipeline + complete contract surface).
- M9 → M8 (operational handoff depends on migrated skill + validated release candidate).

## M1: Foundation, Module Shape & Data Models

**Objective:** Establish the `cli/swarm/` package mirroring `cli/sprint/`, the Click group entry point, and every dataclass the pipeline serializes. | **Duration:** Weeks 1–2 | **Entry:** repo green on `make verify-sync`; Python ≥3.10 + UV toolchain confirmed; named owners assigned for OQ-006/OQ-008/OQ-009 | **Exit:** all 20 data models defined and round-trip serializable; `superclaude swarm --help` lists the group; module tree matches sprint shape.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|AC-001|Python ≥3.10 + UV mandate|Enforce UV for all swarm operations; no `python -m`/`pip install`|build|—|all swarm scripts run via `uv run`; CI rejects bare pip/python invocations|S|P0|
|2|AC-002|New `superclaude swarm` CLI verb|Register swarm as top-level verb, not a sprint/roadmap subcommand|cli|—|`superclaude swarm` resolves; not nested under sprint/roadmap|S|P0|
|3|AC-003|Mirror sprint module shape|`cli/swarm/` file layout mirrors `cli/sprint/` for operator familiarity|cli|AC-002|module filenames map 1:1 to sprint equivalents where roles align|S|P0|
|4|AC-006|Click ≥8.0.0 CLI group|Use Click group + subcommands for the swarm verb|cli|AC-002|group + subcommand registration via Click ≥8.0.0|S|P0|
|5|AC-019|Source-of-truth discipline|Edits land in `src/superclaude/` then `make sync-dev`; never edit `.claude/` directly|build|—|`make verify-sync` passes; no direct `.claude/` edits|S|P0|
|6|NFR-015|Module shape mirror verification|Assert `cli/swarm/` mirrors `cli/sprint/` for operator familiarity|cli|AC-003|structural test confirms parallel module roles|S|P1|
|7|COMP-001|swarm_group|Click group entry point exporting subcommands|cli/swarm/__init__.py|AC-006|exports run/status/logs/attach/kill/scaffold/validate/validate-lenses placeholders|S|P0|
|8|COMP-003|SwarmConfig|Configuration dataclass + path resolution|cli/swarm/config.py|—|resolves output dir, env vars, defaults; immutable dataclass|S|P0|
|9|COMP-004|models module|Aggregates JobSpec/WorkerSpec/ResultContract/WorkerResult/SwarmState/EventRecord dataclasses|cli/swarm/models.py|—|all dataclasses importable; JSON round-trip lossless|M|P0|
|10|COMP-031|Transport Protocol|Protocol interface all transports implement|cli/swarm/transports/__init__.py|COMP-004|defines `send(prompt,timeout)->WorkerResult` contract|S|P0|
|11|DM-001|JobSpec|Top-level job specification dataclass|models|COMP-004|spec_version:str; job_id:str; created:str; caller:CallerInfo; lens:str; custom_prompt_dir:str?; workers:WorkerSpec; transport:TransportSpec; prompt:PromptSpec; target:TargetSpec; normalization:NormalizationSpec; output:OutputSpec; amalgamation_mode:enum(raw/normalize/normalize+merge); status_policy:StatusPolicy; recommended_next_command_template:str; recommended_next_command_substitutions:dict; runtime:RuntimeSpec|M|P0|
|12|DM-002|WorkerSpec|Worker configuration dataclass|models|COMP-004|count:int; models:list[str]; timeout_sec:int; temperature:float; retry.on_5xx:bool; retry.on_5xx_backoff_sec:int; retry.on_4xx:bool; retry.on_timeout:bool|S|P0|
|13|DM-003|TargetSpec|Target ingestion config|models|COMP-004|kind:str; path:str; truncation.line_cap:int; truncation.byte_floor:int; delimiters.open:str; delimiters.close:str; injection_guard.enabled:bool; injection_guard.required_substring:str|S|P0|
|14|DM-004|TransportSpec|Transport config|models|COMP-004|kind:str; base_url_env:str; api_key_env:str|S|P0|
|15|DM-005|PromptSpec|Prompt definition (verbatim system/user)|models|COMP-004|system:str(verbatim); user_template:str(verbatim); variables:dict|S|P0|
|16|DM-006|NormalizationSpec|Normalization config|models|COMP-004|recipe:str; template_path:str; schema_version:str; recipe_args:dict; on_parse_error.salvage:bool; on_parse_error.retain_raw:bool|S|P0|
|17|DM-007|OutputSpec|Output config|models|COMP-004|dir:str; filename_template:str; lens_name:str; atomic_write:bool; emit_meta_sidecar:bool|S|P0|
|18|DM-008|StatusPolicy|Status determination policy|models|COMP-004|floor:int; success_first:bool; partial_threshold:int|S|P0|
|19|DM-009|RuntimeSpec|Runtime config|models|COMP-004|mode:enum(inline/detached); log_level:str; on_completion.write_done_sentinel:bool; on_completion.print_contract_to_stdout:bool|S|P0|
|20|DM-010|LensEntry|Lens registry entry dataclass|models|COMP-004|name:str; description:str; system_prompt_fragment:str; user_template:str; output_template_path:str; recipe_name:str; default_workers:int; default_target_line_cap:int; suspect:bool; tier:str; recommended_next_command_template:str; acceptance_notes:str; stability:enum(stable/experimental)|M|P0|
|21|DM-011|ResolvedLensEntry|Snapshot of lens captured in manifest|models|DM-010|name:str; system_prompt_fragment:str; user_template:str; recipe_name:str; default_workers:int; suspect:bool; tier:str; recommended_next_command_template:str; stability:str|S|P0|
|22|DM-012|ResultContract|Final job result contract|models|COMP-004|contract_version:str; status:enum; job_id:str; started:str; finished:str; elapsed_ms:int; caller:CallerInfo; lens:str; lens_source:str; target.path:str; target.checksum:str; target.truncated:bool; target.truncation_line_cap:int; workers_requested:int; workers_succeeded:int; workers_failed:int; output_files:list[WorkerResult]; amalgamation_mode:str; merged_path:str?; caller_metadata:CallerMetadata; recommended_next_command:str; artifacts:Artifacts|M|P0|
|23|DM-013|WorkerResult|Per-worker output entry|models|COMP-004|index:int; path:str; raw_path:str; meta_path:str; model_id:str; model_label:str; bytes:int; status:enum; http_code:int?; attempts:int; elapsed_ms:int|S|P0|
|24|DM-014|SwarmState|Persistent state file dataclass|models|COMP-004|state:enum(preflight_ok/dispatching/normalizing/reducing/terminal); job_id:str; updated:str|S|P0|
|25|DM-015|EventRecord|JSONL event entry|models|COMP-004|event_type:enum(worker_start/worker_progress/worker_done/wave_transition/terminal); timestamp:str; worker_index:int?; payload:dict|S|P0|
|26|DM-016|Manifest|Preflight artifact|models|DM-011|contract_version:str; job_id:str; resolved_lens_entry:ResolvedLensEntry; preflight.target_checksum:str; preflight.workers_requested:int; preflight.transport_kind:str|S|P0|
|27|DM-017|DoneSentinel|Terminal marker (`done.json`)|models|COMP-004|atomic_write:bool(true); terminal_status:str; contract_path:str|S|P0|
|28|DM-018|Artifacts|Path bundle embedded in contract|models|DM-012|manifest_path:str; state_path:str; event_log_jsonl:str; event_log_md:str; done_sentinel:str|S|P0|
|29|DM-019|CallerInfo|Caller metadata|models|COMP-004|skill:str?; skill_version:str?; invocation_label:str; kind:enum(claude/cli/subprocess)|S|P0|

### Integration Points — M1

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|swarm_group (COMP-001)|Click group registry|Partial (placeholders)|M1|all subcommands (M2/M3/M7)|
|Transport Protocol (COMP-031)|Protocol interface|Defined|M1|openai_compat/stub transports (M3)|
|models module exports|Dataclass registry|Yes|M1|preflight, dispatch, reduce, contract emitters|

### Milestone Dependencies — M1

- None (foundation milestone).

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Data model churn forces downstream rewrites|MEDIUM|MEDIUM|Field changes ripple into schema, contract, manifest|Freeze DM field sets at M1 exit; version via spec_version/contract_version; review against §4/§5 before exit|architect|
|2|Module shape drifts from sprint, harming operator familiarity|LOW|LOW|Operator confusion, review friction|NFR-015 structural test asserts 1:1 role mapping|backend|
|3|OQ-006/008/009 left unresolved when models freeze|MEDIUM|MEDIUM|Schema fields locked without binding decisions, forcing M2 rework|Named owners assigned at M1 entry; resolution required for M1 exit|architect|

## M2: Preflight, Schema, Lens Registry & Injection Guard (Wave 0)

**Objective:** Build Wave 0 — JSON Schema validation, lens resolution/materialization, the 8-entry lens registry + validator, the §11.5 prompt-injection guard enforced identically across all 3 prompt-input paths, and the INV-005/INV-007 worker-pool guards. | **Duration:** Weeks 3–4 | **Entry:** M1 data models frozen | **Exit:** `swarm validate` and `swarm validate-lenses` pass on the bundled registry; injection guard enforced on lens / JSON-Schema / custom-prompt-dir paths; empty-target guard STOPs before dispatch; worker-vs-pool guard (INV-005) and empty-pool failure semantics (INV-007) operational; OQ-007/008/010 resolved.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-005|schema module|JSON Schema for job spec + cross-field validators + §11.5 required-substring rule|cli/swarm/schema.py|DM-001|validates all DM-001 subfields; enforces §11.5 substring on prompt.system|M|P0|
|2|COMP-006|preflight (Wave 0)|Lens resolution + materialization; custom-prompt-dir guard parity; state init|cli/swarm/preflight.py|COMP-005,COMP-022|resolves lens; materializes prompts; writes manifest; sets preflight_ok|L|P0|
|3|FR-019|Job spec JSON Schema validation|Validate job spec with cross-field rules incl. §11.5 required-substring on `prompt.system`|schema|COMP-005|invalid specs rejected pre-dispatch; §11.5 substring rule enforced|M|P0|
|4|FR-020|Lens-driven defaults expansion|`lens` field expands system/user_template/recipe/template_path/workers.count/line_cap/filename_template/lens_name/next_command_template/suspect/tier from LENSES[lens]|preflight|COMP-022|all listed fields populated from registry entry at preflight|M|P0|
|5|FR-021|Custom-prompt-dir escape hatch|When `lens==custom` AND `custom_prompt_dir` set, read `<dir>/system.txt`,`user.txt`,`meta.yaml`|preflight|FR-020|3 files read + materialized; missing file → failed contract|M|P0|
|6|§11.5|Prompt-injection guard|Target wrapped in `<<<TARGET>>>`/`<<<END TARGET>>>`; data-vs-instructions separation in system prompt; enforced across all 3 prompt-input paths|preflight|COMP-005|delimiters applied; required-substring present on lens, JSON-Schema, and custom-prompt-dir paths|M|P0|
|7|INV-003|Custom-prompt-dir identical guard|Custom-prompt-dir applies identical §11.5 substring check as lens-driven and schema paths|preflight|§11.5|`--custom-prompt-dir` preflight check rejects missing substring|S|P0|
|8|INV-014|Escape-hatch isomorphism|Lens-driven and `--custom-prompt-dir` paths have parity for injection-guard enforcement|preflight|INV-003|parity test: both paths reject identical guard violation|S|P0|
|9|INV-005|Worker-count vs model-pool guard|Validate `workers.count` against configured T2 model pool count; resolution semantics per OQ-007|preflight|DM-002,OQ-007|workers_exceed_pool detected; behavior matches OQ-007 resolution (warn-with-defaults vs STOP); test covers both branches|M|P0|
|10|INV-007|Empty-pool failure contract|When configured T2 model pool empty: write `failed`/`env-missing` contract when output dir creatable; pre-output abort otherwise|preflight|AC-017,OQ-008|empty pool detected pre-dispatch; structured failed contract emitted when output dir creatable; bare abort otherwise; resolves OQ-008|M|P0|
|11|IMM-4|Empty-target guard|Target with <50 non-whitespace bytes after truncation → write `failed`/`target-too-small` and STOP before dispatch|preflight|—|49-byte target produces failed contract; no dispatch occurs|S|P0|
|12|COMP-022|LENSES dict + helpers|Registry dict + LensEntry dataclass + helper accessors|cli/swarm/lenses/__init__.py|DM-010|registry loads 8 entries; helpers resolve by name|M|P0|
|13|COMP-023|_validate (lens validator)|Validator: file refs resolve; recipe registered; suspect↔suspect_files coupling; name uniqueness; §11.5 substring|cli/swarm/lenses/_validate.py|COMP-022|all 5 assertions enforced; non-conforming entry fails|M|P0|
|14|U-008|swarm validate-lenses logic|Iterate LENSES; assert file refs resolve; recipe_name registered; suspect:true entries include `{suspect_files}` in next-cmd template; name uniqueness; system_prompt_fragment contains §11.5 substring|_validate|COMP-023|all assertions run over bundled registry|M|P0|
|15|FR-009|Lens registry (8 entries)|Bundle bare-review, refactor-find, edge-case-hunt, spec-completeness, feasibility-probe, troubleshoot-hypothesis, doc-completeness, custom|lenses|COMP-022|8 entries present; 7 non-custom pass validator|S|P0|
|16|FR-007|swarm validate subcommand|Validate job-spec file without dispatching|commands|COMP-005|exits 0 on valid spec, non-zero with diagnostics on invalid|S|P0|
|17|FR-008|swarm validate-lenses subcommand|Validate bundled lens registry|commands|U-008|exits 0 when registry passes; reports first failure otherwise; failure semantics per OQ-010|S|P0|
|18|FR-024|--auto-inject-guard flag|Backward-compat: auto-prepend canonical §11.5 sentence for existing custom-prompt-dir users|preflight|FR-021,§11.5|flag prepends sentence; absent → required-substring still enforced|S|P1|
|19|COMP-024|bare_review lens|Unscaffolded native-instinct review lens; suspect:true; tier:T2; workers:3|lenses/bare_review.py|COMP-022|entry passes validator; suspect_files in next-cmd template|S|P0|
|20|COMP-025|refactor_find lens|Smallest cleanups for correctness/readability/efficiency; tier:T2-code; workers:3|lenses/refactor_find.py|COMP-022|entry passes validator; stability:experimental|S|P1|
|21|COMP-026|edge_case_hunt lens|"What inputs/states break this?"; tier:T2-edge; workers:4|lenses/edge_case_hunt.py|COMP-022|entry passes validator; default_workers=4|S|P1|
|22|COMP-027|spec_completeness lens|"What's missing in this spec?"; tier:T2-spec; workers:3|lenses/spec_completeness.py|COMP-022|entry passes validator|S|P1|
|23|COMP-028|feasibility_probe lens|"Would this approach work?"; tier:T2-feas; workers:3|lenses/feasibility_probe.py|COMP-022|entry passes validator|S|P1|
|24|COMP-029|troubleshoot_hypothesis lens|"Most likely root cause?"; tier:T2-tshoot; workers:4|lenses/troubleshoot_hypothesis.py|COMP-022|entry passes validator; default_workers=4|S|P1|
|25|COMP-030|doc_completeness lens|"What's missing in this doc?"; tier:T2-doc; workers:3|lenses/doc_completeness.py|COMP-022|entry passes validator|S|P1|
|26|DM-020|CallerMetadata (output)|Lens/caller-attached metadata resolved at preflight|preflight|DM-010,OQ-009|suspect:bool(from lens or caller); tier:str; precedence per OQ-009|S|P0|
|27|NFR-003|Security: prompt-injection enforcement|Injection-guard delimiters + required-substring enforced at preflight across all 3 paths|preflight|§11.5,INV-003|negative test: end-marker-containing target neutralized|M|P0|
|28|NFR-012|Lens-registry PR review discipline|Every new lens requires real caller, §11.5 substring, normalizer-output-shape alignment, real downstream command, extra scrutiny for suspect:true|process|COMP-023|review checklist documented; CI hook tracked under OQ-001|S|P1|
|29|AC-013|No Claude-Code-isms|Zero Claude tool names in job spec, result contract, CLI surface, monitoring contract|cli|—|grep audit finds no Claude-tool references in contract surfaces|S|P0|

### Integration Points — M2

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|LENSES dict (COMP-022)|Registry dict|Yes|M2|preflight (FR-020), validator (U-008), manifest snapshot (M1/M6)|
|recipe_name references in lenses|Cross-registry binding|Resolved at validate time|M2|recipe registry (M4) — validator asserts registration|
|JSON Schema cross-field validators (COMP-005)|Validator chain|Yes|M2|`swarm validate`, preflight|
|3 prompt-input paths (lens / schema / custom-dir)|Strategy paths|Yes|M2|injection-guard enforcement (§11.5, INV-003, INV-014)|
|T2 model pool env contract|Preflight guard binding|Yes|M2|INV-005 worker-vs-pool check, INV-007 empty-pool failure|

### Milestone Dependencies — M2

- M1 (DM-001 JobSpec, DM-010 LensEntry, DM-011 ResolvedLensEntry, COMP-005 schema target dataclasses).

### Open Questions — M2

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-001|Should `validate-lenses` run as a pre-commit hook by default?|Determines NFR-012 enforcement mechanism and CI wiring|devops|Before M2 exit|
|2|OQ-007|Workers > configured T2Models guard (INV-005): warn-on-exceed-with-defaults vs STOP?|Affects preflight worker-count handling and dispatch safety|architect|Before M2 exit (gates M3 entry)|
|3|OQ-008|Empty-pool failure path (INV-007): `failed`/`env-missing` contract when output dir creatable; pre-output abort otherwise|Determines preflight failure semantics when T2 pool empty|architect|Before M2 exit (resolved via INV-007)|
|4|OQ-009|`caller_metadata.suspect` propagation — lens-only or caller-overridable precedence?|Blocks DM-020 precedence rule|architect|Before M2 exit|
|5|OQ-010|`validate-lenses` failure semantics — exit code, blocking vs warning?|Blocks CI integration of FR-008/U-008|devops|Before M2 exit|

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Lens-registry sprawl: every new lens ships a built-in entry, registry bloats|MEDIUM|MEDIUM|Maintenance burden, untested speculative lenses|PR-review discipline requires real caller; entries without a real caller deferred to `custom-py:` + caller-side prompts|security|
|2|Custom-prompt-dir guard parity gap|MEDIUM|MEDIUM|Existing users' `system.txt` lacks §11.5 sentence → injection exposure|`--auto-inject-guard` flag for backward compatibility during migration; INV-014 parity test|security|
|3|Injection guard bypass via target containing end-marker|HIGH|LOW|Target data interpreted as instructions|Delimiters + required-substring + dedicated test (target-containing-end-marker)|security|
|4|INV-007 empty-pool path emits unclear failure to callers|MEDIUM|MEDIUM|Caller can't distinguish env-missing from other failure modes|Structured `failed`/`env-missing` contract with explicit reason field; documented in OPS-002 (M9)|architect|

## M3: Dispatch & Concurrency (Wave 1)

**Objective:** Build Wave 1 — true-parallel `ThreadPoolExecutor` dispatch via `ParallelExecutor`, the httpx + stub transports, per-worker timeout/retry, atomic state, and dual-format event logging. | **Duration:** Weeks 5–6 | **Entry:** M2 preflight emits resolved lens + manifest; OQ-007/008 resolved | **Exit:** N stub workers dispatch concurrently (IMM-3 verified); timeout/retry policy enforced; all writes atomic and confined to `--output`; `swarm run` executes Wave 0→1 end-to-end against stub.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-002|commands module|Click subcommands wiring run through preflight→dispatch (grows in M7)|cli/swarm/commands.py|COMP-006,COMP-007|`swarm run` invokes Wave 0→1; subcommand registered|M|P0|
|2|COMP-007|dispatch (Wave 1)|httpx ThreadPoolExecutor via ParallelExecutor; per-worker outcome recording|cli/swarm/dispatch.py|COMP-031,COMP-011,COMP-012|N workers dispatched concurrently; every worker outcome recorded|L|P0|
|3|COMP-011|state module|`.swarm-state.json` atomic read/write|cli/swarm/state.py|DM-014|state transitions via tmp+os.replace; never partial|S|P0|
|4|COMP-012|logging_ module|Dual JSONL (append-only, lock-coordinated) + Markdown event log|cli/swarm/logging_.py|DM-015|JSONL appends lock-coordinated; md log human-readable|M|P0|
|5|COMP-032|openai_compat transport|httpx implementation (Phase-1 reference transport)|cli/swarm/transports/openai_compat.py|COMP-031,AC-017|sends to T2 proxy; returns WorkerResult with http_code/attempts|M|P0|
|6|COMP-033|stub transport|Deterministic stub for tests|cli/swarm/transports/stub.py|COMP-031|fixed deterministic outputs; enables parallelism test|S|P0|
|7|FR-001|swarm run subcommand|Execute swarm job from spec file, stdin, or `--lens` shortcut|commands|COMP-002|all 3 input modes dispatch a job|M|P0|
|8|FR-017|Per-worker timeout + retry policy|180s default timeout; 5xx retry-once with backoff; 4xx/timeout/network no retry; always record outcome|dispatch|COMP-007|timeout aborts worker; 5xx retried once; 4xx not retried; outcome recorded|M|P0|
|9|FR-022|openai_compat transport (httpx)|Phase-1 reference transport via httpx|transports|COMP-032|reachable T2 proxy returns parsed body|M|P0|
|10|FR-023|stub transport|Deterministic stub transport for tests|transports|COMP-033|tests run without network|S|P0|
|11|FR-026|Dual-format log emission|`execution-log.jsonl` (append-only, lock-coordinated) + `execution-log.md` (human)|logging_|COMP-012|both files emitted; JSONL parseable; concurrent appends not interleaved|S|P0|
|12|IMM-3|True-parallel dispatch|One ParallelGroup, N workers, code-enforced parallelism replacing attention-mediated tool calls|dispatch|COMP-007,AC-004|stub-worker parallelism test: N workers overlap in wall-clock|M|P0|
|13|IMM-6|Atomic-write idempotency|Every output file via write-to-tmp + os.replace + deterministic filename|all writers|COMP-011|mid-write kill leaves no partial file; rerun idempotent|S|P0|
|14|INV-002|Python-only concurrency|`swarm_dispatch.sh` retired; ThreadPoolExecutor owns dispatch end-to-end; PIPE_BUF assumption deprecated|dispatch|AC-004|no shell dispatch path exists; concurrency purely Python|S|P0|
|15|NFR-001|Concurrency via ParallelExecutor|ThreadPoolExecutor only; invoked via `superclaude.execution.parallel.ParallelExecutor`|dispatch|AC-004|dispatch routes through ParallelExecutor, not raw threads|S|P0|
|16|NFR-002|Atomicity of state transitions|All transitions via tmp+os.replace; lock-coordinated JSONL via threading.Lock|state,logging_|COMP-011|no partial state files; appends serialized by lock|S|P0|
|17|NFR-010|Per-worker hard timeout|180s default, configurable via `workers.timeout_sec`|dispatch|FR-017|worker exceeding timeout aborted and recorded|S|P0|
|18|NFR-011|Retry policy|Single 5xx retry with backoff; 0 retries on 4xx/timeout/network|dispatch|FR-017|retry matrix matches policy exactly|S|P0|
|19|NFR-013|Filesystem constraint|No writes outside `--output` directory|all writers|—|attempted out-of-dir write rejected/tested|S|P0|
|20|NFR-014|No cross-invocation caching|Responses not cached across runs|dispatch|—|two identical runs both hit transport|S|P1|
|21|AC-004|ParallelExecutor invocation mandate|ThreadPoolExecutor invoked via `superclaude.execution.parallel.ParallelExecutor`|dispatch|—|no direct ThreadPoolExecutor instantiation in swarm code|S|P0|
|22|AC-005|httpx transport library|httpx is the HTTP transport for Phase-1 reference impl|transports|—|openai_compat uses httpx|S|P0|
|23|AC-010|No routing to Anthropic models|Dispatch never targets Anthropic models|dispatch|—|transport config audit shows no Anthropic endpoints|S|P0|
|24|AC-014|No writes outside --output|Enforce output-dir confinement|all writers|NFR-013|path guard rejects escapes|S|P0|
|25|AC-015|No cross-invocation response caching|No response cache layer|dispatch|NFR-014|no cache module present|S|P1|
|26|AC-017|T2 proxy endpoint env contract|T2 proxy via `T2ProxyUrl`/`T2ProxyKey`/`T2Model0N` env vars|transports|—|transport reads endpoint+key+model from env at Wave 0|S|P0|

### Integration Points — M3

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|ParallelExecutor (existing)|DI / executor injection|Yes|M3|dispatch (IMM-3, NFR-001)|
|Transport registry (Protocol impls)|Strategy selection|Yes|M3|dispatch selects openai_compat vs stub by TransportSpec.kind|
|threading.Lock JSONL coordinator|Callback/lock wiring|Yes|M3|logging_ append path (NFR-002)|
|`swarm run` (FR-001)|Click subcommand binding|Yes|M3|operators + non-Claude callers|

### Milestone Dependencies — M3

- M2 (preflight resolved lens entry + manifest feed dispatch; schema-validated WorkerSpec; OQ-007/008 resolved).
- M1 (DM-013 WorkerResult, DM-014 SwarmState, DM-015 EventRecord, COMP-031 Transport Protocol).

### Open Questions — M3

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-005|Per-model overrides (e.g., per-model temperature) within one swarm?|Affects WorkerSpec/dispatch model-dimension handling|architect|Defer until a real lens requires it|
|2|OQ-006|Concurrent-`--output`-dir protection?|Risk of two jobs clobbering one output dir|architect|Defer for v1; document caller-must-avoid|

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|ThreadPoolExecutor surprise: threading behavior unexpected by developers|LOW|MEDIUM|Subtle concurrency bugs in maintenance|Documented in dispatch.py docstring; tested with stub transport; routed through ParallelExecutor|backend|
|2|T2 proxy unreachable blocks end-to-end dispatch test|MEDIUM|MEDIUM|Wave 1 cannot be exercised against real transport|Validate against stub transport (COMP-033) as primary CI path; gate openai_compat tests behind env presence|devops|
|3|JSONL append interleaving under concurrency corrupts log|MEDIUM|LOW|Unparseable observability stream|threading.Lock-coordinated appends (NFR-002); concurrency append test|backend|

## M4: Normalize & Recipe Registry (Wave 2)

**Objective:** Build Wave 2 — the Recipe Protocol + REGISTRY with 6 normalizers, the custom-py dynamic loader, per-worker normalization with parse-error salvage, and the per-lens output templates. | **Duration:** Weeks 7–8 | **Entry:** M3 emits per-worker raw outputs | **Exit:** each worker output normalized by its lens recipe; parse_error→success salvage promotion works; raw/normalize/normalize+merge modes select correct recipe path; each non-custom lens has a matching output template that validator and normalize agree on.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-008|normalize (Wave 2)|Wave 2 dispatcher + Recipe Protocol invocation + recipe registry lookup|cli/swarm/normalize.py|COMP-015|selects recipe per worker; applies normalization; emits meta sidecar|M|P0|
|2|COMP-015|Recipe Protocol + REGISTRY|Protocol interface + REGISTRY dict + custom-py: loader|cli/swarm/recipes/__init__.py|DM-006|6 recipes registered; protocol enforces normalize signature|M|P0|
|3|COMP-016|bare_review_v1 recipe|Ports `t2_normalize.py` logic for bare-review lens|cli/swarm/recipes/bare_review_v1.py|COMP-015|output matches bare-review compressed-table shape|M|P0|
|4|COMP-017|findings_table_v1 recipe|Extracted shape for findings-table lenses|cli/swarm/recipes/findings_table_v1.py|COMP-015|produces findings-table normalized output|S|P1|
|5|COMP-018|hypothesis_table_v1 recipe|Hypothesis-table normalizer|cli/swarm/recipes/hypothesis_table_v1.py|COMP-015|produces hypothesis-table output|S|P1|
|6|COMP-019|verdict_only_v1 recipe|Verdict-only normalizer|cli/swarm/recipes/verdict_only_v1.py|COMP-015|produces verdict-only output|S|P1|
|7|COMP-020|passthrough recipe|Pass-through normalizer (raw-mode shape)|cli/swarm/recipes/passthrough.py|COMP-015|returns input unchanged (raw mode)|S|P0|
|8|COMP-021|custom (custom-py loader)|Dynamic `custom-py:module:func` loader|cli/swarm/recipes/custom.py|COMP-015|loads + invokes external recipe by module:func spec|M|P1|
|9|FR-010|Recipe Protocol registry (6 normalizers)|Register bare_review_v1, findings_table_v1, hypothesis_table_v1, verdict_only_v1, passthrough, custom-py dynamic loader|recipes|COMP-015|all 6 resolvable by name; custom-py loads dynamically|M|P0|
|10|FR-028|Parse-error salvage promotion|Wave 2 promotes `parse_error → success` on §7.4 salvage|normalize|COMP-008|salvageable parse_error reclassified success; meta records salvage|S|P0|
|11|COMP-034|bare-review output template|Compressed-markdown findings table template|refs/templates/bare-review-output.md|COMP-016|template renders bare-review findings table|S|P0|
|12|COMP-035|Per-lens output templates|Lens-specific output shape templates for each non-custom bundled lens (refactor-find, edge-case-hunt, spec-completeness, feasibility-probe, troubleshoot-hypothesis, doc-completeness)|refs/templates/<lens>-output.md|COMP-017,COMP-018,COMP-019|each non-custom lens has a matching output template; validator asserts recipe↔template alignment|M|P1|
|13|AC-011|No scoring/dedup/reorder in recipes|Recipes constrained to shape transforms; no scoring, deduplication, reordering, rewriting, or filtering|normalize|—|recipe output preserves all findings; no judging transforms applied|S|P0|

### Integration Points — M4

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Recipe REGISTRY dict (COMP-015)|Registry dict|Yes|M4|normalize (recipe selection), lens validator (M2 asserts registration)|
|custom-py:module:func loader (COMP-021)|Dynamic dispatch / plugin loader|Yes|M4|caller-supplied recipes via NormalizationSpec.recipe|
|recipe selection in normalize|Dispatch table (recipe_name→callable)|Yes|M4|Wave 2 per-worker normalization|
|amalgamation_mode→recipe path|Strategy branch (raw/normalize/normalize+merge)|Yes|M4|reduce (M5) consumes normalized outputs|
|Per-lens template ↔ recipe alignment|Registry cross-validation|Yes|M4|U-008 lens validator (M2) asserts template path resolves|

### Milestone Dependencies — M4

- M3 (per-worker raw outputs + WorkerResult records feed normalization).
- M2 (lens recipe_name references resolved against this registry).

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Recipe drifts toward scoring/filtering, violating AC-011|HIGH|LOW|Normalizer silently judges findings|Recipes constrained to shape transforms; boundary reinforced by AC-011; M5 merge guards independent|architect|
|2|custom-py loader executes arbitrary caller code|MEDIUM|MEDIUM|Untrusted recipe code runs in process|Loader scoped to explicit `custom-py:module:func`; documented trust boundary; no auto-discovery|security|
|3|Salvage promotion masks genuine worker failure|MEDIUM|LOW|parse_error wrongly counted as success, skewing IMM-5 status|Salvage limited to §7.4 conditions; meta sidecar records salvage provenance|backend|
|4|Per-lens template ↔ recipe drift|MEDIUM|MEDIUM|Downstream commands receive malformed tables|U-008 validator asserts template path resolves and recipe output shape matches template|backend|

## M5: Reduce, Merge, Status & Result Contract (Wave 3)

**Objective:** Build Wave 3 — success-first status determination, the ≤30 LOC mechanical-merge module behind four structural guards, the three amalgamation modes, and the final result contract emission. | **Duration:** Weeks 9–10 | **Entry:** M4 normalized outputs available | **Exit:** IMM-5 status matrix verified; merge produces all sections in slot-index order with provenance header only; `return-contract.yaml` emitted; boundary test green and CI-protected.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-009|reduce (Wave 3)|Status determination (IMM-5) + resume merge regen (INV-010)|cli/swarm/reduce.py|COMP-010,DM-012|computes status; emits contract; triggers merge in normalize+merge mode|M|P0|
|2|COMP-010|merge module|Mechanical concat only; ≤30 LOC; PR-review-discipline guarded|cli/swarm/merge.py|—|concats N sections in slot order with provenance header; no other transforms|S|P0|
|3|IMM-5|Success-first status determination|`M==N`→success; `2≤M<N`→partial; `M<2`→failed; `M==N==2`→success; floor+success_first configurable (floor=2, success_first=true)|reduce|DM-008|parametrized status test covers M==N / 2≤M<N / M<2 / M==N==2|M|P0|
|4|FR-011|Three amalgamation modes|`raw` (Wave 2 pass-through); `normalize` (default, Recipe per worker); `normalize+merge` (normalize + Wave 3 mechanical concat)|reduce|COMP-010|each mode produces correct artifact set|M|P0|
|5|FR-012|Mechanical merge module (4 guards)|Explicit allowed/disallowed ops in docstring; ≤30 LOC ceiling; PR-review boundary note; boundary test `test_merge_mechanical_only.py`|merge|COMP-010|all 4 guards present and enforced|M|P0|
|6|FR-018|Result contract emission|`return-contract.yaml` with status, job_id, lens, amalgamation_mode, output_files (index/paths/model_id/status/http_code/attempts), merged_path, caller_metadata, recommended_next_command, artifacts|reduce|DM-012|contract contains all listed fields; valid YAML|M|P0|
|7|NFR-008|Merge module ≤30 LOC|`swarm/merge.py` body ≤30 LOC (excluding imports + docstring)|merge|COMP-010|LOC count assertion passes in CI|S|P0|
|8|NFR-009|Boundary enforcement test|`tests/swarm/test_merge_mechanical_only.py` asserts 3-worker concat yields all 3 sections in slot-index order, provenance header only; CI flags PRs touching this file|merge|FR-012|boundary test green; CI rule active on file path|S|P0|
|9|AC-012|No new merge/diff/scoring engine|`/sc:adversarial` remains the scored-merge pipeline; swarm introduces none|merge|AC-011|no scoring/diff engine code in swarm|S|P0|
|10|AC-018|merge.py body ≤30 LOC|Hard LOC ceiling on merge module body|merge|NFR-008|enforced LOC ceiling|S|P0|
|11|AC-011|No scoring/dedup/reorder/rewrite/filter (merge)|No scoring, deduplication, reordering, rewriting, or filtering of worker findings in merge path|merge|—|merge output preserves every worker section verbatim+ordered|S|P0|

### Integration Points — M5

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|StatusPolicy (DM-008)|Config injection|Yes|M5|reduce status determination (IMM-5)|
|merged.md / return-contract.yaml|Output artifact emission|Yes|M5|callers, resume merge regen (M6), CLI status (M7)|
|recommended_next_command template|String-substitution wiring|Yes|M5|contract emission (FR-018), downstream `/sc:adversarial`|

### Milestone Dependencies — M5

- M4 (normalized per-worker outputs feed reduce + merge).
- M1 (DM-008 StatusPolicy, DM-012 ResultContract, DM-013 WorkerResult).

### Open Questions — M5

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-003|Should `recommended_next_command` ever be auto-executed via `--auto-handoff`?|Affects contract semantics and caller automation surface|architect|Defer for v1|

### Risk Assessment and Mitigation — M5

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Merge boundary erosion: normalize+merge drifts into judging via incremental PRs|HIGH|MEDIUM|Silent loss of caller-facing neutrality; trust violation|Four structural guards (docstring + ≤30 LOC + PR review + boundary test) + CI rule on boundary test|architect|
|2|Status determination edge cases (M==N==2 ambiguity)|MEDIUM|LOW|Wrong terminal status misleads callers|Parametrized IMM-5 test covers all branches incl. M==N==2→success|backend|
|3|Contract field omission breaks non-Claude callers|MEDIUM|LOW|Downstream parsing fails|FR-018 field-completeness test against DM-012 schema|backend|

## M6: Resume, Crash Recovery & Manifest

**Objective:** Make jobs resumable from the manifest as durable source-of-truth: rehydrate lens verbatim, skip succeeded workers, re-dispatch the rest, re-run Wave 2, and regenerate merge unconditionally. | **Duration:** Weeks 11–12 | **Entry:** M5 reduce + merge stable | **Exit:** `swarm run --resume` skips workers reporting `status: success`; merge regenerated when `amalgamation_mode==normalize+merge`; `--force-relens` re-resolves; lens mutations between runs do not affect resumed jobs.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|INV-001|Resume rehydrates lens from manifest|Resume reads `manifest.resolved_lens_entry` verbatim; does NOT re-resolve from current LENSES; `--force-relens` opts into re-resolution|reduce,preflight|DM-016|resumed job uses manifest lens; registry edits ignored unless --force-relens|M|P0|
|2|INV-010|Resume regenerates merged.md|Resume regenerates `merged.md` unconditionally after re-dispatched workers' Wave 2 completes when `amalgamation_mode==normalize+merge`|reduce|COMP-009|stale merge never persists; provenance reflects re-dispatch|S|P0|
|3|INV-016|Manifest as durable source-of-truth|Manifest is the record of "what this swarm was supposed to do"; resume honors it; lens-registry mutations between runs do not affect resumed jobs|preflight|DM-016|manifest immutable across resume; mutation test passes|S|P0|
|4|FR-015|Resume + crash recovery|`swarm run --resume <job_id>` re-runs Wave 0 in resume mode; skips workers whose `.meta.json` reports `status: success`; re-dispatches remaining; re-runs Wave 2; regenerates merge|commands,preflight|INV-001,INV-010|succeeded workers skipped; remaining re-dispatched; merge regenerated|L|P0|
|5|FR-016|Manifest emission|Emit manifest with `resolved_lens_entry` snapshot at preflight including verbatim system_prompt_fragment, user_template, recipe_name, defaults, suspect, tier, stability|preflight|DM-011,DM-016|manifest captures full resolved lens snapshot at Wave 0|M|P0|
|6|FR-025|--force-relens flag|On resume, ignore manifest's `resolved_lens_entry`, re-resolve from current registry|commands|INV-001|flag triggers re-resolution; default path uses manifest|S|P1|
|7|NFR-005|Crash recovery semantics|Resume from manifest with worker-level skip; merge regeneration on resume; manifest as source-of-truth|preflight,reduce|FR-015|kill-then-resume reaches terminal state with no duplicate work|M|P0|
|8|NFR-006|Schema evolution forward-compat|`spec_version` forward-compat best-effort; orchestrator at 1.1 loads specs at 1.0|schema|—|1.1 orchestrator loads 1.0 spec without error|S|P1|

### Integration Points — M6

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Manifest resolved_lens_entry (DM-016)|Durable source-of-truth snapshot|Yes|M6|resume rehydration (INV-001), preflight resume mode|
|`.meta.json` per-worker status|Skip-decision lookup|Yes|M6|resume worker-skip logic (FR-015)|
|--force-relens flag|Conditional re-resolution branch|Yes|M6|preflight (overrides manifest lens)|

### Milestone Dependencies — M6

- M5 (reduce + merge must exist before merge regeneration on resume).
- M1 (DM-011 ResolvedLensEntry, DM-016 Manifest).

### Open Questions — M6

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-002|Per-lens version pinning (`--lens-version v2`)?|Affects manifest snapshot + resume re-resolution semantics|architect|Defer until lens definitions mutate frequently in production|

### Risk Assessment and Mitigation — M6

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Resume + lens-mutation interaction breaks resume|MEDIUM|MEDIUM|Resumed job uses wrong lens, producing inconsistent output|`--resume` rehydrates from manifest by default; `--force-relens` opts into re-resolution; tests cover both paths|architect|
|2|Schema evolution drag: spec_version evolution breaks loaders|LOW|LOW|Old specs fail under new orchestrator|Forward-compat best-effort: 1.1 loads 1.0; version-skew test|backend|
|3|Stale merge provenance after partial re-dispatch|MEDIUM|LOW|Merge lies about which workers contributed|INV-010 unconditional merge regen on resume in normalize+merge mode|backend|

## M7: Observability, TUI, Detached & Full CLI Surface

**Objective:** Complete the operator surface — three-layer durable monitoring, the opt-in Rich TUI, tmux detached mode, the done sentinel, and the remaining swarm subcommands (status/logs/attach/kill/scaffold). | **Duration:** Weeks 13–14 | **Entry:** M5 pipeline + contract stable | **Exit:** all 8 subcommands functional; `--tui` opt-in only (non-TTY callers get no control sequences); detached jobs survive caller death; three monitoring patterns demonstrated.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-013|tui|Rich Live dashboard, flag-gated `--tui`, NOT default|cli/swarm/tui.py|AC-007|renders only when `--tui`; no control sequences on non-TTY|M|P1|
|2|COMP-014|tmux|Detached-run wrapper (mirrors sprint/tmux.py)|cli/swarm/tmux.py|AC-008|launches detached job; survives caller exit|M|P1|
|3|INV-012|TUI opt-in via --tui|TUI opt-in via `--tui` flag, NOT default; non-TTY callers do not get terminal control sequences|tui|COMP-013|default run emits plain output; `--tui` enables dashboard|S|P0|
|4|FR-002|swarm status subcommand|Show state of job (terminal or in-flight)|commands|COMP-011|reads `.swarm-state.json`; reports current phase/status|S|P0|
|5|FR-003|swarm logs subcommand|Tail or dump job's execution log|commands|COMP-012|tails JSONL / dumps md log|S|P0|
|6|FR-004|swarm attach subcommand|Re-attach to detached (tmux) job's TUI|commands|COMP-014|re-attaches to running detached session|S|P1|
|7|FR-005|swarm kill subcommand|Terminate running detached job|commands|COMP-014|terminates session; writes terminal state|S|P1|
|8|FR-006|swarm scaffold subcommand|Emit starter job-spec file for named lens|commands|COMP-022|writes valid starter spec for given `--lens`|S|P1|
|9|FR-013|Three monitoring patterns|`Bash run_in_background + until [ -f done.json ]`; `Monitor` tailing JSONL; `swarm status --watch`|commands,logging_|FR-027|all three patterns documented + demonstrated|S|P1|
|10|FR-014|Detached mode via tmux|tmux wrapper (mirrors sprint/tmux.py); `--detached` flag|tmux|COMP-014|`--detached` launches background job; inline remains default|M|P1|
|11|FR-027|Done sentinel emission|`done.json` on terminal state via atomic write|reduce,state|IMM-6|terminal state writes done.json atomically|S|P0|
|12|NFR-004|Observability: three-layer durable monitoring|`.swarm-state.json` + `execution-log.jsonl` + `execution-log.md` + `done.json`|state,logging_|FR-027|all four artifacts emitted and consistent|S|P0|
|13|NFR-016|Contract surface non-precluding|Zero Claude tool names in job spec/result contract/CLI/monitoring; detached mode guarantees caller-death survival|cli,tmux|AC-013|grep audit clean; detached job survives caller kill|S|P0|
|14|AC-007|Rich ≥13.0.0 for --tui|Rich for opt-in dashboard, NOT default|tui|INV-012|Rich used only behind `--tui`|S|P1|
|15|AC-008|tmux for detached mode|tmux required for detached (optional; inline default)|tmux|—|detached requires tmux; inline needs no tmux|S|P1|
|16|AC-009|No external framework integration|No openharness/openhands/OpenAI Assistants SDK/LangGraph/CrewAI; design non-precluding|cli|—|no such deps imported; integration seams documented|S|P1|
|17|AC-016|No streaming/function-calling/vision (Phase 1)|Phase 1 excludes streaming, function-calling, vision input (parent §7.3)|transports|—|transport rejects/omits these modes in Phase 1|S|P1|

### Integration Points — M7

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Click subcommand registration (COMP-002)|Subcommand registry|Yes|M7|status/logs/attach/kill/scaffold/run/validate/validate-lenses|
|done.json sentinel|Event binding / completion signal|Yes|M7|monitoring patterns (FR-013), non-Claude pollers|
|tmux session wrapper (COMP-014)|Process detachment wiring|Yes|M7|attach/kill subcommands, detached runs|
|Rich Live dashboard (COMP-013)|Flag-gated render binding|Yes|M7|`--tui` interactive sessions only|

### Milestone Dependencies — M7

- M5 (stable pipeline + contract; status/logs read reduce artifacts).
- M3 (COMP-002 commands, COMP-011 state, COMP-012 logging_ extended here).

### Open Questions — M7

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-004|Prometheus / OpenMetrics output at event boundaries?|Affects observability surface + event-record schema|devops|Defer for v1|

### Risk Assessment and Mitigation — M7

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Tmux dependency for detached mode|LOW|LOW|Detached unavailable without tmux|Detached optional; inline default (same posture as sprint)|devops|
|2|TUI control sequences leak into non-TTY caller output|MEDIUM|LOW|Corrupts machine-readable output for non-Claude callers|INV-012: `--tui` opt-in only; non-TTY path emits plain output|frontend|
|3|Claude-ism creeps into monitoring contract|MEDIUM|LOW|Breaks NFR-016 caller-agnosticism|grep audit in CI (AC-013/NFR-016); contract surface review|architect|

## M8: Migration, Test Discipline & Hardening

**Objective:** Migrate `sc-bare-review` to a ~60-line thin caller with A/B-verified output parity, prove non-Claude caller compatibility, land enumerated migration deliverables (source-first sync, package entry registration, legacy shell retirement, release notes), and land the full per-IMM / per-INV acceptance test suite as enumerated test items. | **Duration:** Weeks 15–16 | **Entry:** M6 (resumable pipeline) + M7 (complete CLI + contract surface) done | **Exit:** SKILL.md migrated; `scripts/*.sh` deleted only after A/B parity passes; non-Python caller produces identical contract; all enumerated TEST items green.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-029|SKILL.md migration|Rewrite sc-bare-review SKILL.md as ~60-line thin caller building `--lens bare-review` job spec, exec CLI, relay return contract|src/superclaude/skills/sc-bare-review/SKILL.md|FR-001, FR-018,COMP-016|thin caller ~60 lines; lens:bare-review; contract relayed; parity gate passes before legacy deletion|L|P1|
|2|FR-030|Non-Claude caller compatibility|Invocation via `subprocess.run(["superclaude","swarm","run","--detached",spec_path])` from any language|cli|FR-014, FR-018|non-Python subprocess produces identical result contract|M|P1|
|3|NFR-007|Test coverage (per-IMM + per-INV)|Per-IMM acceptance test + per-INV remediation test live in `tests/swarm/`; gated by enumerated TEST items below|tests/swarm/|all milestones|every IMM + INV has a passing dedicated test|L|P0|
|4|MIG-001|Source-first sync workflow|All migration edits land in `src/superclaude/` then `make sync-dev`; generated `.claude/` copies never edited directly|release|AC-019,FR-029|src updated; `make sync-dev` run; `make verify-sync` clean; no direct `.claude/` edits|M|P0|
|5|MIG-002|Package entry registration|Register swarm CLI package and command group in distributable CLI entry points|release|COMP-001,COMP-002|`superclaude swarm --help` lists subcommands; package imports clean; entry point installs cleanly|M|P0|
|6|MIG-003|Legacy shell retirement|Remove `scripts/*.sh` from `sc-bare-review` skill package after A/B parity gate passes|release|TEST-003|shell scripts removed; no legacy dispatch refs in skill; legacy code path absent|M|P1|
|7|MIG-004|Release notes + operator migration note|Document new CLI invocation, resume behavior, prompt guard requirement, custom prompt migration path|docs|MIG-001|run examples; resume notes; `--auto-inject-guard` migration; custom prompt path documented|S|P1|
|8|TEST-001|IMM acceptance suite|Validate IMM-3 parallelism (stub-worker overlap), IMM-4 empty-target STOP (49-byte), IMM-5 status matrix (M==N/2≤M<N/M<2/M==N==2), IMM-6 atomic-write mid-write kill, §11.5 end-marker target safety|tests/swarm/|IMM-3,IMM-4,IMM-5,IMM-6,§11.5|each IMM case has a dedicated passing test|L|P0|
|9|TEST-002|INV remediation suite|Validate INV-001 manifest lens rehydration; INV-002 Python-only dispatch (no shell); INV-003 custom-prompt-dir identical guard; INV-005 worker-vs-pool guard; INV-007 empty-pool failure contract; INV-010 resume merge regen; INV-014 escape-hatch isomorphism|tests/swarm/|all INV ids|each INV remediation has a dedicated passing test|L|P0|
|10|TEST-003|Bare-review parity test|Compare thin-caller output against current bare-review output on identical targets|tests/swarm/|FR-029,COMP-016|same target → equivalent normalized output; contract relayed; gates MIG-003|M|P0|
|11|TEST-004|Bundled lens validation gate|Run `swarm validate-lenses` against all non-custom bundled entries|tests/swarm/|U-008,FR-008, FR-009|7 non-custom entries pass validator in CI|M|P0|
|12|TEST-005|Non-Claude caller integration|Invoke CLI via subprocess from a non-Python harness; compare returned contract|tests/swarm/|FR-030,NFR-016|subprocess invocation succeeds; detached supported; contract identical to Claude invocation|M|P1|
|13|TEST-006|Mechanical merge boundary test|Assert 3-worker concat preserves slot order and applies no transforms beyond provenance header; CI flags PRs touching test file|tests/swarm/test_merge_mechanical_only.py|FR-012,NFR-009|3 sections in slot order; no transforms beyond header; CI rule active|M|P0|
|14|TEST-007|Resume crash recovery E2E|Verify successful workers skipped, remaining workers redispatched, Wave 2 reruns, merge regenerates|tests/swarm/|FR-015,NFR-005,INV-010|kill-then-resume reaches terminal state with no duplicate work; merge regenerated|L|P0|

### Integration Points — M8

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|sc-bare-review thin caller|Skill→CLI invocation binding|Yes|M8|Claude Code skill runtime; A/B harness (TEST-003)|
|return-contract.yaml (FR-018)|Caller-agnostic contract consumption|Yes|M8|non-Claude callers (FR-030), skill relay (FR-029)|
|src→.claude sync pipeline|Release pipeline binding|Yes|M8|`make sync-dev` / `make verify-sync` on every migration edit|
|Package CLI entry point|Distributable registration|Yes|M8|`superclaude swarm` discoverable post-install|

### Milestone Dependencies — M8

- M6 (resumable pipeline required for production-grade migration).
- M7 (full CLI surface + detached mode + complete contract required by thin caller and non-Claude callers).

### Risk Assessment and Mitigation — M8

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|A/B parity regression: thin caller output diverges from current bare-review|MEDIUM|MEDIUM|Migration blocked; behavior change for existing skill|TEST-003 parity test on identical targets gates MIG-003 legacy deletion|qa|
|2|Premature `scripts/*.sh` deletion before parity proven|MEDIUM|LOW|Loss of working fallback during migration|MIG-003 sequenced strictly after TEST-003 passes|architect|
|3|Non-Claude caller contract mismatch|MEDIUM|LOW|External integrations break|TEST-005 cross-language subprocess test asserts identical contract|backend|
|4|Skill migration bypasses source-of-truth rules|HIGH|LOW|Generated dev copies drift from source|MIG-001 source-first sync; `make verify-sync` gate; never stage generated `.claude/` content|release|
|5|Boundary test (TEST-006) becomes a weak gate|HIGH|LOW|Merge module begins filtering or rewriting findings|CI flags test changes; PR review treats boundary test as protected|architect|

## M9: Operational Handoff

**Objective:** Land first-class operational rollout deliverables — runbook, environment readiness check, observability procedure, rollback, lens contribution policy, and post-release metrics review — so production adoption is not a byproduct of feature completion. | **Duration:** Week 17 (explicit buffer: this milestone absorbs late-cycle slack rather than padding earlier milestones) | **Entry:** M8 release candidate available; A/B parity passed; all enumerated TEST items green | **Exit:** operators can run, monitor, resume, and troubleshoot swarm jobs using documented commands and contracts; rollback procedure validated.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|OPS-001|Operator runbook|Document run/status/logs/watch/resume/kill/attach workflows with single-line commands|docs|M7,M8|commands enumerated; single-line examples; contract paths explained; tested by ops reviewer|M|P1|
|2|OPS-002|Environment readiness check|Document and validate Python ≥3.10, UV, httpx, Click, Rich, tmux (optional), and T2 proxy prerequisites; align with INV-007 env-missing contract|ops|M2,M3|prerequisite checklist; readiness script; INV-007 env-missing path referenced; T2 env vars documented|S|P1|
|3|OPS-003|Observability procedure|Define how to monitor state file, JSONL log, Markdown log, done sentinel, and return contract; map artifacts to debugging workflows|ops|FR-013,NFR-004|four monitoring artifacts documented; debugging recipes provided|S|P1|
|4|OPS-004|Rollback procedure|Describe reverting skill caller to previous release; disabling detached rollout; preserving in-flight artifacts|ops|M8,MIG-003|skill rollback steps; detached disable steps; artifact preservation rules; rehearsed once|S|P1|
|5|OPS-005|Lens contribution policy|Document review requirements for adding/changing lens entries (real caller, §11.5 substring, recipe/template alignment, downstream command, suspect scrutiny)|docs|NFR-012,U-008|policy doc covers all 5 review criteria; references registry validator (U-008)|S|P1|
|6|OPS-006|Post-release metrics review|Review validation failures, env-missing contracts, resume usage, and custom prompt guard failures after rollout|ops|M8|metrics enumerated; review window scheduled post-release; findings feed backlog|S|P2|

### Integration Points — M9

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|runbook → CLI surface|Operator workflow binding|Yes|M9|operators; on-call|
|return-contract.yaml → troubleshooting|Diagnostic contract binding|Yes|M9|incident response; support|
|lens contribution policy → PR review|Governance hook|Yes|M9|future lens authors; validator (U-008)|
|post-release metrics → backlog|Feedback loop|Yes|M9|maintainers; next-iteration planning|

### Milestone Dependencies — M9

- M8 (release candidate must exist; A/B parity must pass before runbook finalization).
- M7 (CLI surface must be final before runbook documents commands).
- M2 (INV-007 env-missing contract referenced by OPS-002).

### Risk Assessment and Mitigation — M9

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Rollout starts without operator observability|MEDIUM|LOW|Incidents take longer to diagnose|Publish OPS-001 runbook and OPS-003 observability procedure before release|release|
|2|Documentation diverges from CLI contract|MEDIUM|MEDIUM|Operators run wrong commands or expect wrong artifacts|OPS-001 examples verified against final CLI flags; OPS-002 readiness script CI-tested|scribe|
|3|Environment readiness gaps surface in production|MEDIUM|MEDIUM|Jobs fail due to missing tmux or T2 env vars|OPS-002 readiness check; INV-007 structured env-missing contract|devops|
|4|Rollback procedure untested before incident|MEDIUM|LOW|Rollback fails when needed|OPS-004 rehearsed once during M9 (table-top exercise)|release|

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By Milestone|Status|Fallback|
|---|---|---|---|
|Python ≥3.10|M1|Available|None (hard requirement)|
|UV (build tool)|M1|Available|None (CLAUDE.md CRITICAL rule)|
|httpx|M3|Add to deps|None for openai_compat; stub transport covers tests|
|Click ≥8.0.0|M1|Available (existing dep)|None|
|Rich ≥13.0.0|M7|Available (existing dep)|Plain-text output when `--tui` not used|
|pytest ≥7.0.0|M3 (tests onward)|Available (existing dep)|None|
|tmux|M7|Available (optional)|Inline mode (default) needs no tmux|
|T2 proxy endpoint (`T2ProxyUrl`/`T2ProxyKey`/`T2Model0N`)|M3|Must confirm reachable|Stub transport for CI/dev; INV-007 structured env-missing contract at runtime|
|`superclaude.execution.parallel.ParallelExecutor`|M3|Available (internal)|None (AC-004 mandate)|
|Parent spec: bare-review v1.3.0-draft|M2, M8|Available|None (IMM invariants carry forward)|
|`/sc:adversarial`|M5 (next-cmd reference)|Available (downstream)|Referenced only; not invoked by swarm|

### Infrastructure Requirements

- CI runner with Python ≥3.10 + UV; network-isolated stub-transport test lane plus an opt-in live lane gated on T2 proxy env presence.
- CI rule to flag PRs touching `tests/swarm/test_merge_mechanical_only.py` (NFR-009 / TEST-006 boundary protection).
- Optional pre-commit hook for `swarm validate-lenses` (per OQ-001 / OQ-010 resolution at M2 exit).
- Filesystem write confinement: jobs write only under `--output` (NFR-013/AC-014); CI asserts no out-of-dir writes.
- Documentation pipeline that regenerates OPS-001 examples from final CLI `--help` output to prevent drift.

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|Mitigation|Owner|
|----|------|---------------------|-------------|--------|------------|-------|
|R-001|Data model churn forces downstream rewrites|M1|MEDIUM|MEDIUM|Freeze DM field sets at M1 exit; version via spec_version/contract_version|architect|
|R-002|OQ-006/008/009 unresolved when models freeze|M1|MEDIUM|MEDIUM|Named owners assigned at M1 entry; OQ-008 resolved via INV-007 at M2|architect|
|R-003|Lens-registry sprawl: every new lens ships built-in entry|M2|MEDIUM|MEDIUM|PR-review discipline; speculative lenses deferred to `custom-py:` + caller-side prompts|security|
|R-004|Merge boundary erosion: normalize+merge drifts into judging|M4,M5|MEDIUM|HIGH|Four structural guards + CI rule on TEST-006|architect|
|R-005|Resume + lens-mutation interaction breaks resume|M6|MEDIUM|MEDIUM|`--resume` rehydrates from manifest by default; `--force-relens` opts in|architect|
|R-006|Tmux dependency for detached mode|M7,M9|LOW|LOW|Detached optional; inline default|devops|
|R-007|ThreadPoolExecutor threading behavior surprises developers|M3|MEDIUM|LOW|Documented in dispatch.py docstring; stub-transport tests; routed via ParallelExecutor|backend|
|R-008|Custom-prompt-dir guard parity: existing `system.txt` lacks §11.5 sentence|M2,M8|MEDIUM|MEDIUM|`--auto-inject-guard` backward-compat flag; INV-014 parity test; MIG-004 release notes|security|
|R-009|Schema evolution drag: spec_version evolution breaks loaders|M6|LOW|LOW|Forward-compat best-effort; version-skew test|backend|
|R-010|T2 proxy unreachable blocks live dispatch validation|M3,M8,M9|MEDIUM|MEDIUM|Stub transport as primary CI path; live tests gated on env; INV-007 structured failure|devops|
|R-011|A/B parity regression in sc-bare-review migration|M8|MEDIUM|MEDIUM|TEST-003 parity test gates MIG-003; `bare_review_v1` ports `t2_normalize.py` verbatim|qa|
|R-012|custom-py loader executes untrusted caller code|M4|MEDIUM|MEDIUM|Explicit `custom-py:module:func` only; no auto-discovery; documented trust boundary|security|
|R-013|Validation-coverage gap (consolidated from B's R-014/R-015/R-016)|M8|MEDIUM|HIGH|TEST-001 through TEST-007 enumerated; per-IMM + per-INV cases each have a dedicated assertion|qa|
|R-014|Lens-registry PR review weakens over time|M2,M9|MEDIUM|MEDIUM|OPS-005 lens contribution policy + U-008 validator + NFR-012 enforcement|security|
|R-015|INV-007 empty-pool path emits unclear failure to callers|M2,M9|MEDIUM|MEDIUM|Structured `failed`/`env-missing` contract with reason field; OPS-002 documents env contract|architect|
|R-016|Operational readiness gap (rollback / runbook / env)|M9|MEDIUM|MEDIUM|M9 dedicated milestone: OPS-001/OPS-002/OPS-004 first-class deliverables; rollback rehearsed|release|
|R-017|TUI control sequences leak into non-TTY caller output|M7|LOW|MEDIUM|INV-012: `--tui` opt-in only; non-TTY path emits plain output|frontend|
|R-018|Skill migration bypasses source-of-truth rules|M8|LOW|HIGH|MIG-001 source-first sync; `make verify-sync` gate; never stage generated `.claude/` content|release|
|R-019|Documentation diverges from CLI contract|M9|MEDIUM|MEDIUM|OPS-001 examples regenerated from final `--help`; CI verifies parity|scribe|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|Milestone|
|---|---|---|---|---|
|All IMM-N acceptance tests pass|IMM-3/4/5/6 + §11.5 tests|100% pass|TEST-001 suite via `uv run pytest tests/swarm/ -m imm`|M3,M5,M8|
|All INV-xxx remediation tests pass|INV-001/002/003/005/007/010/014 tests|100% pass|TEST-002 suite via `uv run pytest tests/swarm/ -m inv`|M2,M3,M5,M6,M8|
|A/B parity: thin caller vs current bare-review|Output equivalence on identical targets|Byte/structure equivalence|TEST-003 A/B harness diff on shared corpus; gates MIG-003|M8|
|`swarm validate-lenses` passes for bundled registry|Non-custom entries passing|7/7 pass on `make verify-sync`|TEST-004 + `superclaude swarm validate-lenses` in CI|M2,M8|
|Non-Claude caller integration|Contract equivalence cross-language|Identical result contract|TEST-005 `subprocess.run` from non-Python lang|M8|
|Merge boundary mechanical-only invariant|3-worker concat: sections in slot order, provenance header only|0 non-mechanical transforms|TEST-006 boundary test + CI file-touch rule|M5,M8|
|Resume + crash recovery end-to-end|Succeeded workers skipped; merge regenerated|Skip + regen verified|TEST-007 kill-then-resume integration test|M6,M8|
|Migration completes through enumerated steps|MIG-001..MIG-004 all done; legacy shell removed|Production migration verified|MIG-001 source-first sync; MIG-002 entry point; MIG-003 post-parity deletion; MIG-004 notes|M8|
|Operational handoff complete|OPS-001..OPS-006 published and reviewed|Runbook + readiness + rollback + policy live|OPS reviewer sign-off; rollback rehearsal completed|M9|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|----------|--------|------------------------|----------|
|Concurrency model|Python ThreadPoolExecutor via ParallelExecutor (A:9 / B:7 on architectural fidelity)|Shell `swarm_dispatch.sh` (retired); attention-mediated tool calls|Code-enforced parallelism is deterministic and testable; removes PIPE_BUF fragility (IMM-3, INV-002, AC-004)|
|Milestone decomposition|Wave-aligned 8 milestones + dedicated M9 operational handoff|B's concern-bundled 8 milestones (A:9 / B:7)|A's wave-alignment traces 1:1 to architecture document and produces sharper exit criteria; B's M8 operational discipline grafted in as M9 to capture rollout discipline gap|
|Foundation scope|29-item M1 (A) with field-level types|45-item M1 enumerating all ACs (B:6 on coherence)|29 items at L effort is achievable in 2 weeks; AC declarations distributed across milestones where they bind to code|
|Amalgamation boundary|Mechanical concat only, ≤30 LOC, 4 guards (A:9 / B:9)|Scoring/dedup merge engine; reuse `/sc:adversarial`|Preserves caller-facing neutrality; scoring stays in `/sc:adversarial` (AC-011/012, FR-012, TEST-006)|
|Resume source-of-truth|Manifest `resolved_lens_entry` snapshot|Re-resolve from live LENSES each run|Manifest immunity to registry mutation; deterministic resume; `--force-relens` escape hatch (INV-001/016)|
|Injection guard surface|Enforce §11.5 across all 3 prompt-input paths|Lens-path-only enforcement|Escape-hatch isomorphism closes custom-prompt-dir bypass (INV-003/014, NFR-003)|
|Caller surface|Zero Claude-isms; subprocess-callable|Claude-tool-coupled contract|Enables non-Claude callers + detached survival (AC-013, NFR-016, FR-030)|
|TUI default|Opt-in `--tui` only|TUI default|Non-TTY callers must get clean machine-readable output (INV-012, AC-007)|
|Transport (Phase 1)|httpx openai_compat + stub|aiohttp; provider SDKs|httpx fits sync ThreadPool model; stub enables deterministic CI (AC-005, FR-022/023)|
|OQ-007/008 timing|Resolved at M2 exit (gates M3 entry)|Defer to architect decision (A) vs commit as M4 items (B:9 on OQ handling)|Pre-resolution prevents schema/dispatch rework; INV-005/INV-007 make resolutions actionable|
|Operational rollout|Dedicated M9 milestone (OPS-001..006) — grafts B's discipline (B:9 on ops rollout) onto A's wave spine|Distributed across M7/M8 (A:6 on ops)|Production handoff is engineering discipline, not byproduct; runbook+rollback get named owners|
|Validation strategy|Embedded per-wave IMM/INV tests + enumerated TEST-001..007 in M8 (B:8 on validation)|Single dedicated validation milestone (B) vs distributed only (A:7)|Convergent path: catch defects at wave introduction time, consolidate cross-cutting integration tests in M8 without a separate 2-week gate|
|Migration enumeration|MIG-001..MIG-004 explicit items in M8 (B's contribution)|Monolithic FR-029 (A elision)|Prevents "forgot to register package entry" / "deleted shell scripts before parity" failures|

## Timeline Estimates

|Milestone|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1|2 weeks|Week 1|Week 2|20 data models frozen; module shape mirrors sprint; OQ-006/008/009 owners assigned|
|M2|2 weeks|Week 3|Week 4|Wave 0 preflight; 8-lens registry + validator; §11.5 across 3 paths; INV-005/007 guards; OQ-007/008/010 resolved|
|M3|2 weeks|Week 5|Week 6|Wave 1 parallel dispatch; httpx + stub transports; atomic state + logs|
|M4|2 weeks|Week 7|Week 8|Wave 2 recipe registry (6 normalizers); salvage promotion; per-lens output templates|
|M5|2 weeks|Week 9|Week 10|Wave 3 status + ≤30 LOC merge (4 guards); result contract|
|M6|2 weeks|Week 11|Week 12|Resume from manifest; merge regeneration; `--force-relens`|
|M7|2 weeks|Week 13|Week 14|8 subcommands; opt-in TUI; tmux detached; three monitoring patterns|
|M8|2 weeks|Week 15|Week 16|sc-bare-review thin-caller migration; A/B parity; MIG-001..004; TEST-001..007 enumerated|
|M9 (explicit buffer)|1 week|Week 17|Week 17|Operational handoff: runbook, env readiness, rollback, lens contribution policy, post-release metrics|

**Total estimated duration:** 17 weeks (8 implementation milestones × 2 weeks + 1 dedicated operational-handoff week). Buffer is labeled explicitly via M9 rather than distributed as padding inside earlier milestones. M6 and M7 may overlap given both depend only on M5, compressing nominal duration to ~15 weeks if resourced in parallel.
