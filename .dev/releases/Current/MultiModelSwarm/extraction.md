---
spec_source: merged-requirements.compressed.md
generated: 2026-05-30T18:05:00Z
generator: requirements-extraction-agent
functional_requirements: 43
nonfunctional_requirements: 16
total_requirements: 59
complexity_score: 0.85
complexity_class: HIGH
domains_detected: [backend, devops, security, testing, cli, observability]
risks_identified: 7
dependencies_identified: 11
success_criteria_count: 8
extraction_mode: standard
pipeline_diagnostics: {elapsed_seconds: 208.0, started_at: "2026-05-30T18:03:26.877275+00:00", finished_at: "2026-05-30T18:06:54.905765+00:00"}
---

## Functional Requirements

| ID | Requirement | Source | Endpoint/Path/Route |
|----|----|----|----|
| IMM-3 | True-parallel dispatch via Python ThreadPoolExecutor (one ParallelGroup, N workers, code-enforced parallelism replacing attention-mediated "single message, N tool calls") | §1.2, §8 | `cli/swarm/dispatch.py` |
| IMM-4 | Empty-target guard: target with <50 non-whitespace bytes after truncation → write `failed`/`target-too-small` contract and STOP before dispatch | §1.2, §11.1 | preflight Wave 0 |
| IMM-5 | Success-first status determination: `M == N` → `success`; `2 ≤ M < N` → `partial`; `M < 2` → `failed`; `M == N == 2` resolves to `success`; floor + success_first configurable (default floor=2, success_first=true) | §1.2, §10.3 | `cli/swarm/reduce.py` |
| IMM-6 | Atomic-write idempotency: every output file via write-to-tmp + `os.replace` + deterministic filename | §1.2, §11.1 | all output writers |
| §11.5 | Prompt-injection guard: target wrapped in `<<<TARGET>>>` / `<<<END TARGET>>>` delimiters; system-prompt states data-vs-instructions separation; enforced across all 3 prompt-input paths (lens registry, JSON Schema `prompt.system` required-substring, `--custom-prompt-dir` preflight check) | §1.2, §4.3 | preflight Wave 0 |
| INV-001 | Resume rehydrates lens from `manifest.resolved_lens_entry` verbatim; does NOT re-resolve from current LENSES; `--force-relens` opts into re-resolution | §9.2, §9.3 | `swarm run --resume` |
| INV-002 | Python-only concurrency; shell-based `swarm_dispatch.sh` retired; Python ThreadPoolExecutor owns dispatch end-to-end; PIPE_BUF assumption deprecated | §8 | `cli/swarm/dispatch.py` |
| INV-003 | Custom-prompt-dir applies identical §11.5 substring check as lens-driven and JSON-Schema-validated paths | §4.3 | preflight Wave 0 |
| INV-010 | Resume regenerates `merged.md` unconditionally after re-dispatched workers' Wave 2 completes when `amalgamation_mode == normalize+merge` (prevents stale-merge provenance lies) | §9.2 step 5, §10.3 | `swarm run --resume` Wave 3 |
| INV-012 | TUI is opt-in via `--tui` flag, NOT default; non-TTY callers do not get terminal control sequences | §2.1, §6.1, §7 | `--tui` flag |
| INV-014 | Escape-hatch isomorphism: lens-driven and `--custom-prompt-dir` paths have parity for injection-guard enforcement | §4.3 | preflight |
| INV-016 | Manifest is durable source-of-truth for "what this swarm was supposed to do"; resume honors it; lens-registry mutations between runs do not affect resumed jobs | §9.3 | `manifest.json` |
| U-008 | Lens registry validator (`swarm validate-lenses`): iterates LENSES, asserts file refs resolve, asserts recipe_name registered, asserts `suspect:true` entries include `{suspect_files}` in next-cmd template, asserts name uniqueness, asserts `system_prompt_fragment` contains §11.5 substring | §3.5, §6 | `swarm validate-lenses` |
| FR-001 | `swarm run` subcommand: execute swarm job from spec file, stdin, or `--lens` shortcut | §6 | `superclaude swarm run` |
| FR-002 | `swarm status` subcommand: show state of job (terminal or in-flight) | §6 | `superclaude swarm status` |
| FR-003 | `swarm logs` subcommand: tail or dump job's execution log | §6 | `superclaude swarm logs` |
| FR-004 | `swarm attach` subcommand: re-attach to detached (tmux) job's TUI | §6 | `superclaude swarm attach` |
| FR-005 | `swarm kill` subcommand: terminate running detached job | §6 | `superclaude swarm kill` |
| FR-006 | `swarm scaffold` subcommand: emit starter job-spec file for named lens | §6 | `superclaude swarm scaffold` |
| FR-007 | `swarm validate` subcommand: validate job-spec file without dispatching | §6 | `superclaude swarm validate` |
| FR-008 | `swarm validate-lenses` subcommand: validate bundled lens registry | §6 | `superclaude swarm validate-lenses` |
| FR-009 | Lens registry with 8 initial entries (bare-review, refactor-find, edge-case-hunt, spec-completeness, feasibility-probe, troubleshoot-hypothesis, doc-completeness, custom) at `cli/swarm/lenses/` | §3.3 | `cli/swarm/lenses/` |
| FR-010 | Recipe Protocol registry with 6 normalizers (bare_review_v1, findings_table_v1, hypothesis_table_v1, verdict_only_v1, passthrough, custom-py:module:func dynamic loader) | §2.1 | `cli/swarm/recipes/` |
| FR-011 | Three amalgamation modes: `raw` (Wave 2 no-op), `normalize` (default; Recipe per worker), `normalize+merge` (normalize + Wave 3 mechanical concat) | §10.1 | `--amalgamation-mode` flag |
| FR-012 | Mechanical merge module (`swarm/merge.py`) with 4 structural guards: explicit allowed/disallowed ops in docstring, ≤30 LOC ceiling, PR-review boundary preservation note, boundary test `test_merge_mechanical_only.py` | §10.2 | `cli/swarm/merge.py` |
| FR-013 | Three monitoring patterns: `Bash run_in_background + until [ -f done.json ]`, `Monitor` tool tailing JSONL, `swarm status --watch` | §7 | `done.json`, `execution-log.jsonl`, `--watch` |
| FR-014 | Detached mode via tmux wrapper (mirrors sprint/tmux.py); supports `--detached` flag | §2.1, §16 Phase 6 | `cli/swarm/tmux.py` |
| FR-015 | Resume + crash recovery: `swarm run --resume <job_id>` re-runs Wave 0 in resume mode; skips workers with `.meta.json` reporting `status: success`; re-dispatches remaining; re-runs Wave 2; regenerates merge | §9.1-9.2 | `swarm run --resume` |
| FR-016 | Manifest emission with `resolved_lens_entry` snapshot captured at preflight (Wave 0) including verbatim system_prompt_fragment, user_template, recipe_name, defaults, suspect, tier, stability | §3.6 | `manifest.json` |
| FR-017 | Per-worker timeout (180s default) + retry policy (5xx retry-once with backoff, 4xx/timeout/network no retry); always-record outcome | §2, §8 step 3 | dispatch Wave 1 |
| FR-018 | Result contract emission (`return-contract.yaml`) with status, job_id, lens, amalgamation_mode, output_files (with index, paths, model_id, status, http_code, attempts), merged_path, caller_metadata, recommended_next_command, artifacts | §5 | `return-contract.yaml` |
| FR-019 | Job spec JSON Schema validation with cross-field rules including §11.5 required-substring rule on `prompt.system` | §4, §2 Wave 0 | `cli/swarm/schema.py` |
| FR-020 | Lens-driven defaults expansion: `lens` field expands prompt.system, prompt.user_template, normalization.recipe, normalization.template_path, workers.count, target.truncation.line_cap, output.filename_template, lens_name, recommended_next_command_template, caller_metadata.suspect, caller_metadata.tier from `LENSES[lens]` | §4.2 | preflight |
| FR-021 | Custom-prompt-dir escape hatch: when `lens == 'custom'` AND `custom_prompt_dir` set, preflight reads `<dir>/system.txt`, `<dir>/user.txt`, `<dir>/meta.yaml` | §4.3 | `--custom-prompt-dir` flag |
| FR-022 | openai_compat transport via httpx (Phase-1 reference transport) | §2.1 | `cli/swarm/transports/openai_compat.py` |
| FR-023 | Stub transport for deterministic tests | §2.1 | `cli/swarm/transports/stub.py` |
| FR-024 | `--auto-inject-guard` flag: backward-compat for existing custom-prompt-dir users; auto-prepends canonical §11.5 sentence | §4.3, §6.1 | `--auto-inject-guard` |
| FR-025 | `--force-relens` flag on resume: ignore manifest's `resolved_lens_entry`, re-resolve from current registry | §6.1, §9.2 | `--force-relens` |
| FR-026 | Dual-format log emission: `execution-log.jsonl` (append-only, lock-coordinated) + `execution-log.md` (human log) | §2, §7 | `cli/swarm/logging_.py` |
| FR-027 | Done sentinel emission (`done.json`) on terminal state via atomic write | §2, §7 | `done.json` |
| FR-028 | Parse-error salvage promotion: Wave 2 promotes `parse_error → success` on §7.4 salvage | §2 Wave 2 | `cli/swarm/normalize.py` |
| FR-029 | SKILL.md migration: sc-bare-review SKILL.md rewritten as ~60-line thin caller that builds `--lens bare-review` job spec, execs CLI, relays return contract; A/B parity test against current bare-review output; `scripts/*.sh` deleted | §16 Phase 8-9 | `.claude/skills/sc-bare-review/SKILL.md` |
| FR-030 | Non-Claude caller compatibility: invocation via `subprocess.run(["superclaude", "swarm", "run", "--detached", spec_path])` from any language | §13.1, §13.2 | `superclaude swarm` CLI |

## Non-Functional Requirements

| ID | Requirement | Source |
|----|----|----|
| NFR-001 | Concurrency: Python ThreadPoolExecutor only (no shell dispatch); invoked via `superclaude.execution.parallel.ParallelExecutor` | §8, INV-002 |
| NFR-002 | Atomicity: all state transitions via write-to-tmp + `os.replace`; lock-coordinated JSONL appends via `threading.Lock` | §8 step 5-6, IMM-6 |
| NFR-003 | Security (prompt injection): injection-guard delimiters + required-substring check enforced at preflight across all 3 prompt-input paths | §11.5, INV-003 |
| NFR-004 | Observability: three-layer durable monitoring (`.swarm-state.json` + `execution-log.jsonl` + `execution-log.md` + `done.json`) | §7 |
| NFR-005 | Crash recovery: resume from manifest with worker-level skip semantics; merge regeneration on resume; manifest as source-of-truth | §9.1-9.3, INV-016 |
| NFR-006 | Schema evolution: `spec_version` forward-compat best-effort; orchestrator at 1.1 loads specs at 1.0 | §15.7 |
| NFR-007 | Test coverage: per-IMM acceptance test (IMM-3 stub-worker parallelism, IMM-4 49-byte target, IMM-5 parametrized status, IMM-6 mid-write kill, §11.5 target-containing-end-marker) + per-INV remediation test | §16.1, §16.2 |
| NFR-008 | Module boundary: `swarm/merge.py` body ≤30 LOC (excluding imports + docstring) | §10.2 guard 2 |
| NFR-009 | Boundary enforcement: `tests/swarm/test_merge_mechanical_only.py` asserts 3-worker concat produces all 3 sections in slot-index order with no transformations beyond provenance header; CI rule flags PRs touching this file | §10.2 guard 4 |
| NFR-010 | Per-worker hard timeout (180s default, configurable via `workers.timeout_sec`) | §8 step 2 |
| NFR-011 | Retry policy: single 5xx retry with backoff; 0 retries on 4xx/timeout/network | §8 step 3 |
| NFR-012 | Lens-registry PR review discipline: every new lens entry requires real caller (not speculative), §11.5 substring inclusion, normalizer-output-shape alignment, real downstream command reference, extra scrutiny for `suspect:true` | §3.4 |
| NFR-013 | Filesystem constraint: no writes outside `--output` directory | §11.2 |
| NFR-014 | No cross-invocation caching: responses not cached across runs | §11.2 |
| NFR-015 | Module shape mirror: `src/superclaude/cli/swarm/` mirrors `src/superclaude/cli/sprint/` for operator familiarity | §2.1 |
| NFR-016 | Contract surface non-precluding: zero references to Claude tool names in job spec, result contract, CLI surface, monitoring contract; detached mode guarantees caller-death survival | §13.2 |

## Complexity Assessment

**Score: 0.85 (HIGH)**

Scoring rationale:
- **Module breadth (0.20):** 14+ new modules under `cli/swarm/` (commands, config, models, schema, preflight, dispatch, normalize, reduce, merge, state, logging_, tui, tmux) plus `recipes/` (6 normalizers) and `lenses/` (8 entries + validator).
- **Cross-cutting integration (0.15):** New top-level CLI verb, integration with existing `superclaude.execution.parallel.ParallelExecutor`, migration of existing `sc-bare-review` SKILL.md, mirrors sprint module shape, 10-phase migration plan.
- **Invariant enforcement (0.15):** 5 parent IMM invariants must carry verbatim + 6 INV-xxx remediations from fault-finder + §11.5 extended to 3 prompt-input paths.
- **Concurrency + correctness (0.15):** ThreadPoolExecutor with lock-coordinated JSONL appends, atomic state transitions, resume semantics with manifest rehydration, merge regeneration on resume.
- **Schema + validation (0.10):** JSON Schema for job spec with cross-field rules, registry validator with multiple coupling rules, schema versioning forward-compat.
- **Test discipline (0.05):** Acceptance tests per IMM + remediation tests per INV + boundary test for merge module + A/B parity test for bare-review migration.
- **Operator surface (0.05):** 8 CLI subcommands with flag matrix (`--lens`, `--custom-prompt-dir`, `--auto-inject-guard`, `--amalgamation-mode`, `--tui`, `--force-relens`, `--detached`, `--resume`).

## Architectural Constraints

| ID | Constraint | Source |
|----|----|----|
| AC-001 | Python ≥3.10 with UV for all operations (no `python -m`, no `pip install` direct) | CLAUDE.md (project) |
| AC-002 | New CLI verb `superclaude swarm` at `src/superclaude/cli/swarm/` (NOT sub-command of sprint/roadmap) | §14.1 |
| AC-003 | Module shape MUST mirror `src/superclaude/cli/sprint/` | §2.1 |
| AC-004 | ThreadPoolExecutor MUST be invoked via `superclaude.execution.parallel.ParallelExecutor` | §8 |
| AC-005 | httpx is the HTTP transport library for Phase-1 reference implementation | §2.1 |
| AC-006 | Click ≥8.0.0 for CLI group + subcommands | §2.1 |
| AC-007 | Rich ≥13.0.0 for `--tui` opt-in dashboard (NOT default) | §2.1, INV-012 |
| AC-008 | tmux required for detached mode (optional; inline is default) | §15.4 |
| AC-009 | NO integration with openharness, openhands, OpenAI Assistants SDK, LangGraph, CrewAI; design must be non-precluding for future integration | §1.3, §13 |
| AC-010 | NO routing to Anthropic models | §11.2 |
| AC-011 | NO scoring, deduplication, reordering, rewriting, or filtering of worker findings (even in normalize+merge mode) | §11.2 |
| AC-012 | NO new merge/diff/scoring engine; `/sc:adversarial` remains scored-merge pipeline | §1.3 |
| AC-013 | NO Claude-Code-isms in job spec, result contract, CLI surface, or monitoring contract | §13.2, NFR-016 |
| AC-014 | NO writes outside `--output` directory | §11.2 |
| AC-015 | NO cross-invocation response caching | §11.2 |
| AC-016 | NO streaming, function-calling, or vision input in Phase 1 (inherited from parent §7.3) | §1.3 |
| AC-017 | T2 proxy endpoint via `T2ProxyUrl` / `T2ProxyKey` / `T2Model0N` env vars | §2 Wave 0 |
| AC-018 | swarm/merge.py body MUST be ≤30 LOC | §10.2 guard 2 |
| AC-019 | Source-of-truth discipline: edits go to `src/superclaude/` then `make sync-dev`; never edit `.claude/` directly | CLAUDE.md (project) |

## Component Inventory

### Orchestrator Modules (cli/swarm/)

| ID | Name | Source File | Role | Dependencies | Source Ref |
|----|----|----|----|----|----|
| COMP-001 | swarm_group | `cli/swarm/__init__.py` | Click group entry point exporting subcommands | commands | §2.1 |
| COMP-002 | commands | `cli/swarm/commands.py` | Click subcommands: run, status, logs, attach, kill, scaffold, validate, validate-lenses | preflight, dispatch, normalize, reduce, state, tmux | §2.1, §6 |
| COMP-003 | SwarmConfig | `cli/swarm/config.py` | Configuration dataclass; path resolution | — | §2.1 |
| COMP-004 | models | `cli/swarm/models.py` | JobSpec, WorkerSpec, ResultContract, WorkerResult, SwarmState, EventRecord dataclasses | — | §2.1 |
| COMP-005 | schema | `cli/swarm/schema.py` | JSON Schema for job spec; cross-field validators; §11.5 required-substring rule | models | §2.1, §4 |
| COMP-006 | preflight | `cli/swarm/preflight.py` | Wave 0; lens resolution + materialization; custom-prompt-dir guard parity (INV-003) | schema, lenses, models, state | §2.1, §2 Wave 0 |
| COMP-007 | dispatch | `cli/swarm/dispatch.py` | Wave 1 (httpx ThreadPoolExecutor via ParallelExecutor) | transports, state, logging_, ParallelExecutor | §2.1, §8 |
| COMP-008 | normalize | `cli/swarm/normalize.py` | Wave 2 dispatcher + Recipe Protocol + recipe registry | recipes | §2.1 |
| COMP-009 | reduce | `cli/swarm/reduce.py` | Wave 3 (status determination per IMM-5 + resume merge regen per INV-010) | merge, models | §2.1 |
| COMP-010 | merge | `cli/swarm/merge.py` | Mechanical concat only; ≤30 LOC; PR-review-discipline guarded | — | §2.1, §10.2 |
| COMP-011 | state | `cli/swarm/state.py` | `.swarm-state.json` read/write (atomic) | — | §2.1 |
| COMP-012 | logging_ | `cli/swarm/logging_.py` | Dual JSONL + Markdown event log | — | §2.1 |
| COMP-013 | tui | `cli/swarm/tui.py` | Rich Live dashboard (flag-gated `--tui`, NOT default — INV-012) | Rich | §2.1, INV-012 |
| COMP-014 | tmux | `cli/swarm/tmux.py` | Detached-run wrapper (mirrors sprint/tmux.py) | tmux binary | §2.1 |

### Recipe Registry (cli/swarm/recipes/)

| ID | Name | Source File | Role | Source Ref |
|----|----|----|----|----|
| COMP-015 | Recipe Protocol | `cli/swarm/recipes/__init__.py` | Protocol + REGISTRY dict + custom-py: loader | §2.1 |
| COMP-016 | bare_review_v1 | `cli/swarm/recipes/bare_review_v1.py` | Ports `t2_normalize.py` logic for bare-review lens | §2.1, §12 |
| COMP-017 | findings_table_v1 | `cli/swarm/recipes/findings_table_v1.py` | Extracted shape for findings-table lenses | §2.1 |
| COMP-018 | hypothesis_table_v1 | `cli/swarm/recipes/hypothesis_table_v1.py` | Hypothesis-table normalizer | §2.1 |
| COMP-019 | verdict_only_v1 | `cli/swarm/recipes/verdict_only_v1.py` | Verdict-only normalizer | §2.1 |
| COMP-020 | passthrough | `cli/swarm/recipes/passthrough.py` | No-op normalizer (raw mode shape) | §2.1 |
| COMP-021 | custom (custom-py loader) | `cli/swarm/recipes/custom.py` | Dynamic `custom-py:module:func` loader | §2.1 |

### Lens Registry (cli/swarm/lenses/)

| ID | Name | Source File | Role | Stability | Source Ref |
|----|----|----|----|----|----|
| COMP-022 | LENSES dict + helpers | `cli/swarm/lenses/__init__.py` | Registry dict + LensEntry dataclass + helpers | n/a | §2.1, §3.2 |
| COMP-023 | _validate | `cli/swarm/lenses/_validate.py` | Validator: file refs, recipe resolution, suspect↔suspect_files coupling, name uniqueness, §11.5 substring | n/a | §3.5, U-008 |
| COMP-024 | bare_review lens | `cli/swarm/lenses/bare_review.py` | Unscaffolded native-instinct review (sc-bare-review's lens); suspect:true; tier:T2; workers:3 | stable | §3.3 |
| COMP-025 | refactor_find lens | `cli/swarm/lenses/refactor_find.py` | Smallest cleanups for correctness/readability/efficiency; tier:T2-code; workers:3 | experimental | §3.3 |
| COMP-026 | edge_case_hunt lens | `cli/swarm/lenses/edge_case_hunt.py` | "What inputs/states break this?"; tier:T2-edge; workers:4 | experimental | §3.3 |
| COMP-027 | spec_completeness lens | `cli/swarm/lenses/spec_completeness.py` | "What's missing in this spec?"; tier:T2-spec; workers:3 | experimental | §3.3 |
| COMP-028 | feasibility_probe lens | `cli/swarm/lenses/feasibility_probe.py` | "Would this approach work?"; tier:T2-feas; workers:3 | experimental | §3.3 |
| COMP-029 | troubleshoot_hypothesis lens | `cli/swarm/lenses/troubleshoot_hypothesis.py` | "Most likely root cause?"; tier:T2-tshoot; workers:4 | experimental | §3.3 |
| COMP-030 | doc_completeness lens | `cli/swarm/lenses/doc_completeness.py` | "What's missing in this doc?"; tier:T2-doc; workers:3 | experimental | §3.3 |

### Transport Layer (cli/swarm/transports/)

| ID | Name | Source File | Role | Source Ref |
|----|----|----|----|----|
| COMP-031 | Transport Protocol | `cli/swarm/transports/__init__.py` | Protocol interface for transports | §2.1 |
| COMP-032 | openai_compat transport | `cli/swarm/transports/openai_compat.py` | httpx implementation (Phase-1 reference) | §2.1 |
| COMP-033 | stub transport | `cli/swarm/transports/stub.py` | Deterministic stub for tests | §2.1 |

### Templates (refs/templates/)

| ID | Name | Source File | Role | Source Ref |
|----|----|----|----|----|
| COMP-034 | bare-review output template | `refs/templates/bare-review-output.md` | Compressed-markdown findings table template | §12 |
| COMP-035 | per-lens output templates | `refs/templates/<lens>-output.md` (per lens) | Lens-specific output shape | §3.4 |

### Data Models

| ID | Name | Role | Fields | Source Ref |
|----|----|----|----|----|
| DM-001 | JobSpec | Top-level job specification | spec_version, job_id, created, caller, lens, custom_prompt_dir, workers, transport, prompt, target, normalization, output, amalgamation_mode, status_policy, recommended_next_command_template, recommended_next_command_substitutions, runtime | §4 |
| DM-002 | WorkerSpec | Worker configuration | count, models, timeout_sec, temperature, retry (on_5xx, on_5xx_backoff_sec, on_4xx, on_timeout) | §4.1 |
| DM-003 | TargetSpec | Target ingestion config | kind, path, truncation (line_cap, byte_floor), delimiters (open, close), injection_guard (enabled, required_substring) | §4.1 |
| DM-004 | TransportSpec | Transport config | kind, base_url_env, api_key_env | §4.1 |
| DM-005 | PromptSpec | Prompt definition | system (verbatim), user_template (verbatim), variables | §4.1 |
| DM-006 | NormalizationSpec | Normalization config | recipe, template_path, schema_version, recipe_args, on_parse_error (salvage, retain_raw) | §4.1 |
| DM-007 | OutputSpec | Output config | dir, filename_template, lens_name, atomic_write, emit_meta_sidecar | §4.1 |
| DM-008 | StatusPolicy | Status determination | floor, success_first, partial_threshold | §4.1 |
| DM-009 | RuntimeSpec | Runtime config | mode (inline/detached), log_level, on_completion (write_done_sentinel, print_contract_to_stdout) | §4.1 |
| DM-010 | LensEntry | Lens registry entry dataclass | name, description, system_prompt_fragment, user_template, output_template_path, recipe_name, default_workers, default_target_line_cap, suspect, tier, recommended_next_command_template, acceptance_notes, stability | §3.2 |
| DM-011 | ResolvedLensEntry | Snapshot in manifest | name, system_prompt_fragment, user_template, recipe_name, default_workers, suspect, tier, recommended_next_command_template, stability | §3.6 |
| DM-012 | ResultContract | Final job result | contract_version, status, job_id, started, finished, elapsed_ms, caller, lens, lens_source, target (path, checksum, truncated, truncation_line_cap), workers_requested, workers_succeeded, workers_failed, output_files[], amalgamation_mode, merged_path, caller_metadata, recommended_next_command, artifacts | §5 |
| DM-013 | WorkerResult | Per-worker output entry | index, path, raw_path, meta_path, model_id, model_label, bytes, status, http_code, attempts, elapsed_ms | §5 |
| DM-014 | SwarmState | Persistent state file | (state machine: preflight_ok, dispatching, normalizing, reducing, terminal) | §2.1, §2 Wave 0 |
| DM-015 | EventRecord | JSONL event entry | event_type (worker_start/worker_progress/worker_done/etc.), timestamp, worker_index, payload | §2.1, §2 Wave 1 |
| DM-016 | Manifest | Preflight artifact | contract_version, job_id, resolved_lens_entry, ... | §3.6 |
| DM-017 | DoneSentinel | Terminal marker (`done.json`) | (atomic-write final indicator) | §2, §7 |
| DM-018 | Artifacts | Path bundle in contract | manifest_path, state_path, event_log_jsonl, event_log_md, done_sentinel | §5 |
| DM-019 | CallerInfo | Caller metadata | skill, skill_version, invocation_label, kind | §4.1 |
| DM-020 | CallerMetadata (output) | Lens/caller-attached metadata | suspect (from lens or caller), tier (string) | §5 |

## Risk Inventory

| # | Risk | Severity | Mitigation |
|----|----|----|----|
| 1 | Lens-registry sprawl: every new lens ships built-in entry, registry bloats | MEDIUM | PR-review discipline requires real caller; entries without real caller deferred to `custom-py:` + caller-side custom prompts (§15.1) |
| 2 | Merge boundary erosion: `normalize+merge` mode could drift into judging via incremental PRs | HIGH | Four structural guards (docstring + ≤30 LOC ceiling + PR review + boundary test) + CI rule on boundary test (§10.2, §15.2) |
| 3 | Resume + lens-mutation interaction: lens changes between runs could break resume | MEDIUM | `--resume` rehydrates from manifest (default); `--force-relens` opts into re-resolution; tests cover both paths (§9.2, §15.3) |
| 4 | Tmux dependency for detached mode | LOW | Detached is optional; inline is default (same risk/mitigation as sprint) (§15.4) |
| 5 | ThreadPoolExecutor surprise: developers may not expect threading behavior | LOW | Documented in `dispatch.py` docstring; tested with stub transport (§15.5) |
| 6 | Custom-prompt-dir guard parity: existing users may need to add §11.5 sentence to their `system.txt` | MEDIUM | `--auto-inject-guard` flag for backward compatibility during migration (§15.6) |
| 7 | Schema evolution drag: spec_version evolution may break loaders | LOW | Forward-compat best-effort: orchestrator at `1.1` can load specs at `1.0` (§15.7) |

## Dependency Inventory

| # | Dependency | Type | Purpose | Source |
|----|----|----|----|----|
| 1 | Python ≥3.10 | Runtime | Language runtime | CLAUDE.md, package info |
| 2 | UV | Build tool | All Python operations | CLAUDE.md (CRITICAL rule) |
| 3 | httpx | Library | HTTP transport (Phase-1 reference) | §2.1, §8 |
| 4 | Click ≥8.0.0 | Library | CLI group + subcommands | §2.1, package deps |
| 5 | Rich ≥13.0.0 | Library | `--tui` opt-in dashboard | §2.1, package deps |
| 6 | pytest ≥7.0.0 | Library | Test suite | package deps |
| 7 | tmux | External binary | Detached mode wrapper | §2.1, §15.4 |
| 8 | T2 proxy endpoint | External service | Model dispatch via `T2ProxyUrl`/`T2ProxyKey`/`T2Model0N` env | §2 Wave 0, §4.1 |
| 9 | `superclaude.execution.parallel.ParallelExecutor` | Internal module | ThreadPoolExecutor invocation | §2, §8 |
| 10 | Parent spec: bare-review v1.3.0-draft | Spec dependency | All IMM-N invariants carry forward | §12, parent_spec field |
| 11 | `/sc:adversarial` | Downstream caller | Scored-merge pipeline (referenced in `recommended_next_command_template`) | §3.3, §11 |

## Success Criteria

| # | Criterion | Acceptance Threshold |
|----|----|----|
| 1 | All IMM-N acceptance tests pass | IMM-3 (stub-worker parallelism), IMM-4 (49-byte target STOP), IMM-5 (parametrized status M==N/2≤M<N/M<2), IMM-6 (mid-write kill), §11.5 (target-containing-end-marker) — 100% pass (§16.1) |
| 2 | All INV-xxx remediation tests pass | INV-001 (resume uses manifest lens), INV-002 (concurrency Python-only), INV-003 (custom-prompt-dir injection guard), INV-010 (resume regenerates merge), INV-014 (escape hatch guard parity), §10.2 (merge mechanical only) — 100% pass (§16.2) |
| 3 | A/B parity test between thin sc-bare-review caller and current bare-review implementation | Output equivalence on identical targets (§16 Phase 8) |
| 4 | `swarm validate-lenses` passes for bundled registry | All 7 non-custom entries pass validator on default `make verify-sync` (§3.5, Open Q1) |
| 5 | Non-Claude caller integration | `subprocess.run` from non-Python language produces identical result contract as Claude-invoked call (§13.1, §13.2) |
| 6 | Merge boundary test enforces mechanical-only invariant | `tests/swarm/test_merge_mechanical_only.py` asserts 3-worker concat produces all 3 sections in slot-index order with no transformations beyond provenance header; CI flags PRs touching this file (§10.2 guard 4) |
| 7 | Resume + crash recovery end-to-end | Worker with `.meta.json` reporting `status: success` is skipped on resume; remaining workers re-dispatched; merge regenerated unconditionally when `amalgamation_mode == normalize+merge` (§9.2) |
| 8 | Migration completes through all 10 phases | sc-bare-review SKILL.md migrated to ~60-line thin caller; `scripts/*.sh` deleted; production migration verified (§16 Phase 8-9) |

## Open Questions

| # | Question | Source | Recommendation |
|----|----|----|----|
| 1 | Should `validate-lenses` run as a pre-commit hook by default? | §17 Q1 | Probably yes; defer to tasklist for hook wiring |
| 2 | Per-lens version pinning (`--lens-version v2`)? | §17 Q2 | Defer until lens definitions mutate frequently in production |
| 3 | Should `recommended_next_command` ever be auto-executed via `--auto-handoff`? | §17 Q3 | Defer |
| 4 | Prometheus / OpenMetrics output at event boundaries? | §17 Q4 | Defer |
| 5 | Per-model overrides (e.g., per-model temperature) within one swarm? | §17 Q5 | Defer until a real lens asks (relates to A-005 partially open) |
| 6 | Concurrent-`--output`-dir protection? | §17 Q6 | Defer; document caller-must-avoid for v1 |
| 7 | Workers > configured T2Models guard (INV-005): warn-on-exceed-with-defaults vs STOP? | §17 Q7 | Recommend V1's warn semantics; flag for tasklist confirmation |
| 8 | Empty-pool failure path (INV-007): write `failed`/`env-missing` contract OR pre-output-dir abort? | §17 Q8 | Recommend write-on-failure when output dir is creatable; pre-output-dir abort otherwise |
| 9 | Unaddressed: `caller_metadata.suspect` propagation — is it set by lens entry only, or can caller override? | §12 (inheritance) | Spec implies both (lens sets, caller can override); needs explicit precedence rule |
| 10 | Unaddressed: failure semantics for `validate-lenses` (exit code, blocking vs warning) | §3.5, §6 | Needs explicit failure-mode spec for CI integration |
