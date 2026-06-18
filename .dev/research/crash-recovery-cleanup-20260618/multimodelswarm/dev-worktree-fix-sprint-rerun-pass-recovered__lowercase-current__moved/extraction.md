---
spec_source: merged-requirements.compressed.md
generated: 2026-05-29T15:26:30Z
generator: claude-opus-4-7-requirements-extractor
functional_requirements: 38
nonfunctional_requirements: 14
total_requirements: 52
complexity_score: 0.82
complexity_class: HIGH
domains_detected: [backend, cli, orchestration, concurrency, observability, security, devops, testing]
risks_identified: 7
dependencies_identified: 11
success_criteria_count: 16
extraction_mode: standard
pipeline_diagnostics: {elapsed_seconds: 234.0, started_at: "2026-05-29T15:26:25.858546+00:00", finished_at: "2026-05-29T15:30:19.884901+00:00"}
---

## Functional Requirements

### Mechanism Layer — Orchestrator (CLI)

**FR-001: New top-level CLI verb `superclaude swarm`**
Source: §1.4, §6, §14.1. Provide new top-level Click group `superclaude swarm` at `src/superclaude/cli/swarm/` separate from `sprint` and `roadmap`. The verb represents single-shot parallel fan-out (third primitive distinct from sequential-phase and generative-graph orchestration).

**FR-002: CLI subcommand `swarm run`**
Source: §6. Execute a swarm job from a spec file, stdin, or `--lens` shortcut. Endpoint/route: `superclaude swarm run <spec.yaml>`.

**FR-003: CLI subcommand `swarm status`**
Source: §6, §7. Show state of a job (terminal or in-flight). Endpoint: `superclaude swarm status [--watch]`. Watch mode refreshes every 1s via Rich-rendered status table.

**FR-004: CLI subcommand `swarm logs`**
Source: §6. Tail or dump a job's execution log. Endpoint: `superclaude swarm logs`.

**FR-005: CLI subcommand `swarm attach`**
Source: §6. Re-attach to a detached (tmux) job's TUI. Endpoint: `superclaude swarm attach <job_id>`.

**FR-006: CLI subcommand `swarm kill`**
Source: §6. Terminate a running detached job. Endpoint: `superclaude swarm kill <job_id>`.

**FR-007: CLI subcommand `swarm scaffold`**
Source: §6. Emit a starter job-spec file for a named lens. Endpoint: `superclaude swarm scaffold --lens <name>`.

**FR-008: CLI subcommand `swarm validate`**
Source: §6. Validate a job-spec file without dispatching. Endpoint: `superclaude swarm validate <spec.yaml>`.

**FR-009: CLI subcommand `swarm validate-lenses`**
Source: §3.5, §6, §13.1, §16 Phase 7. Validate the bundled lens registry: assert each entry's references resolve, `recipe_name` is a registered Recipe (including `custom-py:` dynamic resolution), `suspect: true` entries include `{suspect_files}` in next-cmd template, name uniqueness, `system_prompt_fragment` contains §11.5 required substring. Hookable via `make verify-sync` and pre-commit.

**FR-010: `swarm run --lens <name>` flag**
Source: §6.1, §14.2. Resolve lens-registry entry; caller may then omit prompt/recipe/template fields.

**FR-011: `swarm run --custom-prompt-dir <path>` flag**
Source: §4.3, §6.1. When `--lens custom`, point at directory containing `system.txt`, `user.txt`, `meta.yaml`.

**FR-012: `swarm run --auto-inject-guard` flag**
Source: §4.3, §6.1, §15.6. Backward-compat for custom-prompt-dir users; auto-prepends canonical §11.5 sentence.

**FR-013: `swarm run --amalgamation-mode {raw,normalize,normalize+merge}` flag**
Source: §6.1, §10.1. Default `normalize`.

**FR-014: `swarm run --tui` flag**
Source: §6.1, §7. Opt-in Rich Live dashboard (NOT default — INV-012); non-TTY callers do not get terminal control sequences.

**FR-015: `swarm run --force-relens` flag**
Source: §6.1, §9.2. On `--resume`, ignore manifest's `resolved_lens_entry` and re-resolve from current registry (default: rehydrate from manifest per INV-001 fix).

**FR-016: Exit codes**
Source: §6.2. `0` = run reached Wave 3 (status in contract); `2` = spec validation failure; `3` = preflight failure; `10` = orchestrator internal error.

### Wave 0 — Preflight

**FR-017: JSON Schema validation of job spec**
Source: §2 Wave 0, §11.5. Validate spec via JSON Schema + cross-field rules + §11.5 required-substring rule on `prompt.system`.

**FR-018: Lens resolution and materialization**
Source: §2 Wave 0, §3.6, §4.2. Resolve `--lens` against `cli/swarm/lenses/` registry; materialize `resolved_lens_entry` snapshot into `manifest.json` capturing name, system_prompt_fragment, user_template, recipe_name, default_workers, suspect, tier, recommended_next_command_template, stability.

**FR-019: Environment resolution**
Source: §2 Wave 0. Resolve env vars `T2ProxyUrl`, `T2ProxyKey`, `T2Model0N` defaults.

**FR-020: Target read, truncate, checksum (IMM-4)**
Source: §1.2, §2 Wave 0, §11.1. Read + truncate target; compute provenance checksum (sha256[:12]); enforce IMM-4 empty-target guard: target with <50 non-whitespace bytes after truncation → write `failed`/`target-too-small` contract and STOP before any dispatch.

**FR-021: Prompt composition with §11.5 injection-guard delimiters**
Source: §1.2, §2 Wave 0. Wrap target in `<<<TARGET>>>` / `<<<END TARGET>>>` delimiters; system-prompt explicitly states data-vs-instructions separation. Enforce across all three input paths (lens, JSON Schema, custom-prompt-dir) per INV-003/INV-014 fix.

**FR-022: Manifest + state emission at preflight**
Source: §2 Wave 0. Emit `manifest.json` + `.swarm-state.json` (state=`preflight_ok`).

**FR-023: Custom-prompt-dir guard parity (INV-003 fix)**
Source: §4.3, §11.1, §16.2. When `lens == 'custom'`, read `<dir>/system.txt`, `<dir>/user.txt`, `<dir>/meta.yaml`; §11.5 substring check applies identically to lens-driven and JSON-Schema paths. Default: STOP with actionable error if substring absent; `--auto-inject-guard` opts into auto-prepending.

### Wave 1 — Parallel Dispatch

**FR-024: True-parallel dispatch via ThreadPoolExecutor (IMM-3)**
Source: §1.2, §2 Wave 1, §8. Use single Python `ThreadPoolExecutor` invoked via `superclaude.execution.parallel.ParallelExecutor`; all N workers in one ParallelGroup; code-enforced parallelism replaces attention-mediated structural assertion.

**FR-025: Per-worker HTTP dispatch (httpx)**
Source: §2 Wave 1, §8. Each task: build HTTP request body via `json.dumps` (never shell-interpolated), POST via `httpx` with per-worker timeout, write `.raw` + `.meta.json` sidecar.

**FR-026: Retry policy**
Source: §2 Wave 1, §8. On 5xx: retry once after `retry.on_5xx_backoff_sec`. On 4xx / timeout / network: no retry. Always-record (no silent drops).

**FR-027: Per-worker hard timeout**
Source: §2 Wave 1, §11.1. Apply per-worker hard timeout (default 180s).

**FR-028: Event log emission (worker lifecycle)**
Source: §2 Wave 1, §8. Emit `worker_start` / `worker_progress` / `worker_done` events; appends under `threading.Lock`-guarded write.

### Wave 2 — Normalize

**FR-029: Recipe Protocol invocation per worker**
Source: §2 Wave 2. For each worker, invoke configured Recipe; atomic write to deterministic final path (IMM-6).

**FR-030: Parse-error salvage promotion**
Source: §2 Wave 2, §11.1. Promote `parse_error → success` if §7.4 salvage succeeds.

**FR-031: Recipe registry (open-class)**
Source: §2.1, §11.1. Provide `recipes/` registry with Recipe Protocol; ship `bare_review_v1.py`, `findings_table_v1.py`, `hypothesis_table_v1.py`, `verdict_only_v1.py`, `passthrough.py`, `custom.py` (custom-py: dynamic loader).

### Wave 3 — Reduce + Merge

**FR-032: Success-first status determination (IMM-5)**
Source: §1.2, §2 Wave 3. `M == N` → `success` first; `2 ≤ M < N` → `partial`; `M < 2` → `failed`. `M == N == 2` resolves to `success`. Floor and success-first ordering per-job configurable (defaults floor=2, success_first=true).

**FR-033: Three amalgamation modes**
Source: §10.1. Support `raw` (Wave 2 no-op), `normalize` (default, Recipe per worker), `normalize+merge` (normalize + mechanical concat).

**FR-034: Mechanical merge with structural guards (`swarm/merge.py`)**
Source: §10.2, §11.1, §11.2. Module ≤30 LOC; allowed: read each worker's `final_path`, strip frontmatter, prepend `## From {model_label} ({elapsed_ms}ms)` provenance header, concat in slot-index order; disallowed: no reorder/dedup/scoring/winner-selection/claim-rewriting. PR-review boundary preservation check + `tests/swarm/test_merge_mechanical_only.py` boundary test + CI rule flagging boundary-test changes.

**FR-035: Merge edge cases**
Source: §10.3. `M = 0` (failed): `merged_path = null`; `M = 1` (failed-by-floor): `merged_path = null`; `M ≥ 2`: `merged_path` populated with only successful workers; `--resume` + `normalize+merge`: ALWAYS regenerate `merged.md` after Wave 2 (INV-010 fix).

**FR-036: Return contract emission**
Source: §2 Wave 3, §5. Write `return-contract.yaml` with `contract_version`, `status`, `job_id`, timing, target info, worker counts, output_files array, `amalgamation_mode`, `merged_path`, `caller_metadata` (suspect, tier), `recommended_next_command`, artifacts paths.

**FR-037: Done sentinel emission**
Source: §2 Wave 3, §7. Write `done.json` sentinel atomically; emit final event; exit 0 (status lives in contract, not RC).

### Lens Registry

**FR-038: Bundled lens registry**
Source: §3.1, §3.2, §3.3. Provide registry at `cli/swarm/lenses/` with `LensEntry` dataclass (frozen) and 8 initial entries: `bare-review` (stable, suspect:true, T2), `refactor-find`, `edge-case-hunt`, `spec-completeness`, `feasibility-probe`, `troubleshoot-hypothesis`, `doc-completeness`, `custom`. All except `bare-review` and `custom` ship as `experimental`; promoted to `stable` only after a real caller wires in production.

**FR-039: Lens-driven defaults expansion**
Source: §4.2. When `lens` set, preflight expands defaults into spec: `prompt.system`, `prompt.user_template`, `normalization.recipe`, `normalization.template_path`, `workers.count`, `target.truncation.line_cap`, `output.filename_template`, `output.lens_name`, `recommended_next_command_template`, `caller_metadata.suspect`, `caller_metadata.tier`. Caller-supplied overrides lens; missing values → schema validation error.

**FR-040: Lens entry PR-review discipline**
Source: §3.4. PR reviewers verify: real caller exists, prompt fragment includes §11.5 injection-guard sentence, normalizer_strategy matches expected output shape, recommended_next_command_template references real downstream command, `suspect: true` entries get extra scrutiny.

### Concurrency Model (§8)

**FR-041: Python-only dispatch (INV-002 fix)**
Source: §8. Python threads call `httpx` directly; V2-style `swarm_dispatch.sh` shell script is **retired**. Python ThreadPoolExecutor owns dispatch end-to-end; eliminates dual-writer race with PIPE_BUF-atomic shell appends. PIPE_BUF assumption documented as deprecated in `docs/swarm-design-rationale.md`.

### Resume + Crash Recovery (§9)

**FR-042: Crash semantics**
Source: §9.1. Orchestrator crash mid-dispatch: `.swarm-state.json` retains last-known state; completed workers have `.meta.json` sidecars; no `done.json`.

**FR-043: `swarm run --resume <job_id>` workflow**
Source: §9.2. Re-run Wave 0 in resume mode: (1) lens rehydration from `manifest.resolved_lens_entry` verbatim (INV-001 fix); (2) skip workers with `status: success`; (3) re-dispatch remaining workers; (4) re-run Wave 2 (existing successes re-write deterministically, no-op); (5) regenerate `merged.md` unconditionally when `amalgamation_mode == normalize+merge` (INV-010 fix); (6) reduce + contract emit per IMM-5.

**FR-044: Manifest-as-source-of-truth (INV-016 fix)**
Source: §9.3. `manifest.resolved_lens_entry` is durable definition of "what this swarm was supposed to do"; `--resume` honors it; lens-registry mutations between runs do not affect resumed job.

### Monitoring Contract (§7)

**FR-045: Three durable observability layers**
Source: §7. Provide `.swarm-state.json` (atomic on transition), `execution-log.jsonl` (append-only, lock-coordinated), `execution-log.md` (human log), `done.json` (terminal sentinel).

**FR-046: Three monitoring caller patterns**
Source: §7. Support: (1) `Bash run_in_background` + `until [ -f done.json ]` (single-notification fire-and-wait); (2) `Monitor` tool tailing JSONL (one notification per significant event); (3) `swarm status --watch` (Rich-rendered status table refreshing every 1s).

### Atomic Write (IMM-6)

**FR-047: Atomic-write idempotency (IMM-6)**
Source: §1.2, §11.1. Every output file written via write-to-tmp + `os.replace` + deterministic filename.

### Detached Mode

**FR-048: Detached mode via tmux**
Source: §11.1, §16 Phase 6. Support `--detached` via tmux wrapper mirroring `sprint/tmux.py`; detached + `--resume` + `swarm attach` / `kill` lifecycle.

### Migration

**FR-049: sc-bare-review migration to thin caller**
Source: §16 Phase 8-9. Rewrite `sc-bare-review` SKILL.md as ~60-line thin caller building `--lens bare-review` job spec, exec'ing CLI, relaying return contract; A/B parity test against current bare-review output; `scripts/*.sh` deleted.

### Future-Harness Compatibility (§13)

**FR-050: Non-precluding contract surface**
Source: §13.1, §13.2. Job spec, result contract, CLI surface, monitoring contract have zero references to Claude tool names; `caller.kind` is informational only (`skill | command | harness | human`), never used for routing; `subprocess.run` callable from any language.

## Non-Functional Requirements

**NFR-001: Code-enforced parallelism (security/reliability)**
Source: §1.2, §8. Parallelism must occur inside Python process via ThreadPoolExecutor, NOT attention-mediated by Claude's tool calls.

**NFR-002: Prompt-injection guard enforcement (security)**
Source: §1.2, §11.5. §11.5 enforcement extended to three prompt-input paths: JSON Schema required-substring on `prompt.system`, lens registry validator at PR time, `--custom-prompt-dir` preflight substring check. STOP behavior on violation default; opt-in `--auto-inject-guard` for backward compatibility.

**NFR-003: No shell interpolation (security)**
Source: §8. HTTP request bodies built via `json.dumps` with target_content via `--arg`-equivalent — never shell-interpolated.

**NFR-004: Atomic-write durability (reliability)**
Source: §1.2, §8, §11.1. All output files atomically written; state transitions atomic; JSONL appends lock-coordinated; durable across crashes.

**NFR-005: Lock-coordinated append for event log (concurrency-correctness)**
Source: §8. JSONL writes under `threading.Lock`-guard; `.swarm-state.json` updates under lock + atomic rename.

**NFR-006: Merge module LOC ceiling (maintainability/boundary)**
Source: §10.2. `swarm/merge.py` body ≤30 LOC excluding imports + docstring; explicit allowed/disallowed ops in docstring; boundary test enforces mechanical-concat-only semantics.

**NFR-007: Module layout mirrors sprint (maintainability)**
Source: §2.1. Module shape mirrors `src/superclaude/cli/sprint/` so operators familiar with sprint immediately understand swarm.

**NFR-008: PR-review gates for lens entries (governance)**
Source: §3.4. Lens entries reviewed for real-caller existence, injection-guard presence, normalizer fit, downstream-command validity, suspect-flag justification.

**NFR-009: Backward compatibility migration path (compatibility)**
Source: §4.3, §15.6. `--auto-inject-guard` flag preserves existing `--custom-prompt-dir` callers during §11.5 substring enforcement rollout.

**NFR-010: Spec-version forward compatibility (evolution)**
Source: §15.7. Orchestrator at `1.1` can load specs at `1.0`; forward-compat best-effort.

**NFR-011: Cross-language callability (interoperability)**
Source: §13. `subprocess.run(["superclaude", "swarm", "run", ...])` works from any language; JSON / YAML stdlib-parseable contracts everywhere.

**NFR-012: TUI opt-in (output discipline)**
Source: §6.1, INV-012 fix. Rich Live dashboard NOT default; non-TTY callers do not receive terminal control sequences.

**NFR-013: Test coverage of invariants (verification)**
Source: §16.1, §16.2. Every IMM-N + INV-NNN invariant has acceptance test: IMM-3 (stub-worker parallelism), IMM-4 (49-byte target), IMM-5 (parametrized status), IMM-6 (mid-write kill), §11.5 (target-containing-end-marker), INV-001 (resume uses manifest lens), INV-002 (Python-only concurrency), INV-003 (custom-prompt-dir injection guard), INV-010 (resume regenerates merge), INV-014 (escape-hatch guard parity), §10.2 boundary.

**NFR-014: Idempotency on re-dispatch (reliability)**
Source: §9.2. Wave 2 re-runs over all `.raw` files; existing successes re-write deterministically (no-op outcome).

## Complexity Assessment

**Complexity Score: 0.82 (HIGH)**

Rationale by dimension:
- **Scope breadth (0.85):** New top-level CLI verb + 9 subcommands + 13 modules + 8-entry lens registry + 6-entry recipe registry + 2 transport implementations + migration of existing SKILL.md.
- **Concurrency (0.90):** Code-enforced parallelism, ThreadPoolExecutor with lock-coordinated JSONL append + atomic state rename; 6 distinct invariant remediations (INV-001/002/003/010/014/016).
- **Cross-cutting invariants (0.85):** IMM-3/4/5/6 + §11.5 must be preserved verbatim from parent spec; 6 invariant remediation tests required.
- **Security surface (0.80):** Prompt-injection guard enforced across 3 input paths; data-vs-instructions delimiter discipline; JSON-escape transport (no shell interpolation).
- **Resilience (0.85):** Detached mode + tmux + resume + manifest rehydration + merge regeneration on resume; durable observability with 3 monitoring patterns.
- **Migration risk (0.70):** sc-bare-review must achieve A/B parity post-migration; existing `--custom-prompt-dir` users need backward-compat path.
- **Schema evolution (0.65):** Forward-compat best-effort; JSON Schema + cross-field validators + registry validator must coexist.

Drivers pushing HIGH: code-enforced parallelism with multiple lock disciplines, 4 structural guards on merge boundary, dual prompt-input-path validation, INV remediations require test-first execution.

## Architectural Constraints

**AC-001: Mechanism / policy / caller three-layer separation**
Source: §1.1. Orchestrator owns mechanism (parallel dispatch, invariants, observability); lens registry + Recipe Protocol own policy (prompts, templates, normalizers); caller owns choice (lens selection, target supply, contract consumption).

**AC-002: CLI is orchestrator home (not SKILL.md)**
Source: §1.4. ThreadPoolExecutor enforces parallelism in code where SKILL.md prose cannot; `subprocess.run` callability extends to non-Claude callers; durable observability + detached + resume are first-class.

**AC-003: Lens registry bundled inside CLI package**
Source: §3.1. Policy curation lives at `cli/swarm/lenses/` as plain Python dataclasses, not as separate plugin system.

**AC-004: Module layout mirrors `cli/sprint/`**
Source: §2.1. Required for operator continuity.

**AC-005: ThreadPoolExecutor invoked via `superclaude.execution.parallel.ParallelExecutor`**
Source: §8. Reuses existing internal abstraction; no direct `concurrent.futures` usage in dispatch.py.

**AC-006: Transport layer pluggable**
Source: §2.1. Transport Protocol with `openai_compat.py` (Phase-1 reference, httpx-backed) and `stub.py` (deterministic stub for tests).

**AC-007: Recipe Protocol open-class with `custom-py:` dynamic loader**
Source: §2.1, §11.1. `custom-py:<module>:<callable>` is Python-only; non-Python harnesses use `passthrough` and post-process raw bodies.

**AC-008: No third-party agent-harness integration in scope**
Source: §1.3, §13. openharness/openhands/OpenAI Assistants/LangGraph/CrewAI integration explicitly out of scope; contract surface must remain non-precluding.

**AC-009: No scored merge / dedup / reorder in orchestrator**
Source: §1.3, §11.2. Scored merging remains `/sc:adversarial`'s job; `normalize+merge` mode mechanical-concat-only.

**AC-010: No streaming, function-calling, or vision input (Phase 1)**
Source: §1.3. Inherited from parent spec §7.3.

**AC-011: No Anthropic-model routing**
Source: §11.2. Workers route only to T2-proxy-compatible external models.

**AC-012: No file modification outside `--output`**
Source: §11.2. Orchestrator must not modify target file or any file outside `--output`.

**AC-013: No response caching across invocations**
Source: §11.2. Each invocation re-dispatches.

**AC-014: No auto-detection of lens from target**
Source: §11.2. Caller must explicitly pick lens.

**AC-015: No auto-execution of `recommended_next_command`**
Source: §11.2. Always a suggestion, never an action.

**AC-016: `caller.kind` is informational only**
Source: §13.2. Never used for routing.

**AC-017: Parent-spec IMM-N invariants carry forward verbatim or stronger**
Source: §1.2, §12. IMM-3/4/5/6 and §11.5 from bare-review v1.3.0-draft inherited; no weakening permitted.

## Component Inventory

### Services / Modules (COMP-xxx)

**COMP-001: `swarm_group` (Click group export)**
- Path: `src/superclaude/cli/swarm/__init__.py`
- Role: Public Click group entry point exposed at `superclaude swarm`.
- Dependencies: COMP-002 (commands)
- Source: §2.1

**COMP-002: `commands` module**
- Path: `src/superclaude/cli/swarm/commands.py`
- Role: Click subcommand definitions (run, status, logs, attach, kill, scaffold, validate, validate-lenses).
- Dependencies: COMP-003, COMP-004, COMP-005, COMP-006, COMP-007, COMP-008, COMP-009, COMP-010, COMP-011, COMP-012
- Source: §2.1, §6

**COMP-003: `config` module — `SwarmConfig` dataclass**
- Path: `src/superclaude/cli/swarm/config.py`
- Role: Path resolution + global config dataclass.
- Source: §2.1

**COMP-004: `models` module — domain models container**
- Path: `src/superclaude/cli/swarm/models.py`
- Role: Hosts JobSpec, WorkerSpec, ResultContract, WorkerResult, SwarmState, EventRecord dataclasses.
- Dependencies: DM-001 through DM-006
- Source: §2.1

**COMP-005: `schema` module**
- Path: `src/superclaude/cli/swarm/schema.py`
- Role: JSON Schema for job spec; cross-field validators; §11.5 required-substring rule on `prompt.system`.
- Dependencies: COMP-004
- Source: §2.1, §11.5

**COMP-006: `preflight` module (Wave 0)**
- Path: `src/superclaude/cli/swarm/preflight.py`
- Role: Lens resolution + materialization; custom-prompt-dir guard parity (INV-003); target ingest/checksum; IMM-4 empty-target guard.
- Dependencies: COMP-005, COMP-012 (lenses), COMP-010 (state)
- Source: §2 Wave 0, §2.1, §4.3

**COMP-007: `dispatch` module (Wave 1)**
- Path: `src/superclaude/cli/swarm/dispatch.py`
- Role: httpx-based ThreadPoolExecutor dispatch via `execution.parallel.ParallelExecutor`; per-worker timeout, 5xx retry, sidecar emission, event logging.
- Dependencies: COMP-013 (transports), COMP-011 (logging_), `superclaude.execution.parallel.ParallelExecutor`
- Source: §2 Wave 1, §2.1, §8

**COMP-008: `normalize` module (Wave 2 dispatcher + Recipe Protocol)**
- Path: `src/superclaude/cli/swarm/normalize.py`
- Role: Wave 2 dispatcher; hosts Recipe Protocol interface and recipe registry lookup.
- Dependencies: COMP-014 (recipes)
- Source: §2 Wave 2, §2.1

**COMP-009: `reduce` module (Wave 3)**
- Path: `src/superclaude/cli/swarm/reduce.py`
- Role: Status determination per IMM-5; resume merge regeneration (INV-010); contract emission.
- Dependencies: COMP-015 (merge), COMP-010 (state)
- Source: §2 Wave 3, §2.1, §9.2

**COMP-010: `state` module**
- Path: `src/superclaude/cli/swarm/state.py`
- Role: `.swarm-state.json` read/write (atomic).
- Source: §2.1

**COMP-011: `logging_` module**
- Path: `src/superclaude/cli/swarm/logging_.py`
- Role: Dual JSONL + Markdown event log; lock-coordinated append.
- Source: §2.1, §7

**COMP-012: `tui` module**
- Path: `src/superclaude/cli/swarm/tui.py`
- Role: Rich Live dashboard, flag-gated `--tui` (NOT default — INV-012).
- Source: §2.1, §6.1, §7

**COMP-013: `tmux` module**
- Path: `src/superclaude/cli/swarm/tmux.py`
- Role: Detached-run wrapper mirroring `sprint/tmux.py`.
- Source: §2.1, §11.1

**COMP-014: `recipes` package (normalizer registry)**
- Path: `src/superclaude/cli/swarm/recipes/`
- Role: Open-class normalizer registry exposing Recipe Protocol + REGISTRY dict + `custom-py:` loader.
- Sub-modules: `bare_review_v1.py` (ports `t2_normalize.py` logic), `findings_table_v1.py`, `hypothesis_table_v1.py`, `verdict_only_v1.py`, `passthrough.py`, `custom.py`.
- Source: §2.1

**COMP-015: `merge` module (NEW — mechanical concat)**
- Path: `src/superclaude/cli/swarm/merge.py`
- Role: Mechanical concat ONLY; body ≤30 LOC excluding imports/docstring; allowed/disallowed ops in docstring; PR-review-discipline guarded.
- Source: §2.1, §10.2

**COMP-016: `lenses` package (LENS REGISTRY)**
- Path: `src/superclaude/cli/swarm/lenses/`
- Role: Bundled-policy registry exposing `LENSES` dict + `LensEntry` dataclass + helpers.
- Sub-modules: `_validate.py` (validator), `bare_review.py`, `refactor_find.py`, `edge_case_hunt.py`, `spec_completeness.py`, `feasibility_probe.py`, `troubleshoot_hypothesis.py`, `doc_completeness.py`.
- Dependencies: DM-007 (LensEntry)
- Source: §2.1, §3

**COMP-017: `lenses._validate` validator submodule**
- Path: `src/superclaude/cli/swarm/lenses/_validate.py`
- Role: Validate lens registry: file refs resolve, recipe resolution including `custom-py:`, suspect→suspect_files coupling, name uniqueness, §11.5 substring presence.
- Source: §3.5

**COMP-018: `transports` package**
- Path: `src/superclaude/cli/swarm/transports/`
- Role: Transport Protocol interface.
- Sub-modules: `openai_compat.py` (httpx-based Phase-1 reference transport), `stub.py` (deterministic stub for tests).
- Source: §2.1

**COMP-019: Lens entry — `bare-review` (stable)**
- Path: `src/superclaude/cli/swarm/lenses/bare_review.py`
- Role: First-class stable lens for sc-bare-review migration; suspect:true, T2 tier, default workers=3; next-cmd `/sc:adversarial --compare {compare_files} --suspect-source {suspect_files}`.
- Source: §3.3

**COMP-020: Lens entry — `refactor-find`** (experimental, T2-code, default workers=3, suspect:false). Source: §3.3.

**COMP-021: Lens entry — `edge-case-hunt`** (experimental, T2-edge, default workers=4, suspect:false). Source: §3.3.

**COMP-022: Lens entry — `spec-completeness`** (experimental, T2-spec, default workers=3, suspect:false). Source: §3.3.

**COMP-023: Lens entry — `feasibility-probe`** (experimental, T2-feas, default workers=3, suspect:false). Source: §3.3.

**COMP-024: Lens entry — `troubleshoot-hypothesis`** (experimental, T2-tshoot, default workers=4, suspect:false). Source: §3.3.

**COMP-025: Lens entry — `doc-completeness`** (experimental, T2-doc, default workers=3, suspect:false). Source: §3.3.

**COMP-026: Lens entry — `custom`** (escape hatch; caller-supplied via `--custom-prompt-dir`). Source: §3.3.

**COMP-027: Recipe — `bare_review_v1`** — ports `t2_normalize.py` logic. Source: §2.1.

**COMP-028: Recipe — `findings_table_v1`** — extracted shape for findings-table lenses. Source: §2.1.

**COMP-029: Recipe — `hypothesis_table_v1`**. Source: §2.1.

**COMP-030: Recipe — `verdict_only_v1`**. Source: §2.1.

**COMP-031: Recipe — `passthrough`**. Source: §2.1.

**COMP-032: Recipe — `custom`** (dynamic loader for `custom-py:module:func`). Source: §2.1.

**COMP-033: `sc-bare-review` thin-caller SKILL.md (refactored)**
- Role: ~60-line skill that builds `--lens bare-review` job spec, exec'es `superclaude swarm run`, relays return contract.
- Dependencies: COMP-001 (swarm_group via CLI)
- Source: §16 Phase 8

### Data Models (DM-xxx)

**DM-001: `JobSpec`**
- Path: `src/superclaude/cli/swarm/models.py`
- Role: Validated job specification driving swarm dispatch.
- Source: §2.1, §4
- Fields:
  - `spec_version: str` (bumped on structural changes)
  - `job_id: str` (auto-generated `<ISO-timestamp>-<lens>-<short-hash>`)
  - `created: str` (ISO 8601)
  - `caller: dict` ({skill, skill_version, invocation_label, kind} — informational)
  - `lens: str | None` (lens name or 'custom' or null)
  - `custom_prompt_dir: str | None`
  - `workers: WorkerSpec` (DM-002)
  - `transport: dict` ({kind, base_url_env, api_key_env})
  - `prompt: dict` ({system: str, user_template: str, variables: dict})
  - `target: dict` ({kind: file|inline_text|inline_bytes_b64, path: str, truncation: {line_cap: int, byte_floor: int}, delimiters: {open: str, close: str}, injection_guard: {enabled: bool, required_substring: str}})
  - `normalization: dict` ({recipe: str, template_path: str, schema_version: str, recipe_args: dict, on_parse_error: {salvage: bool, retain_raw: bool}})
  - `output: dict` ({dir: str, filename_template: str, lens_name: str | None, atomic_write: bool, emit_meta_sidecar: bool})
  - `amalgamation_mode: Literal["raw","normalize","normalize+merge"]` (default `normalize`)
  - `status_policy: dict` ({floor: int, success_first: bool, partial_threshold: int | None})
  - `recommended_next_command_template: str`
  - `recommended_next_command_substitutions: dict`
  - `runtime: dict` ({mode: inline|detached, log_level: str, on_completion: {write_done_sentinel: bool, print_contract_to_stdout: bool}})

**DM-002: `WorkerSpec`**
- Path: `src/superclaude/cli/swarm/models.py`
- Role: Worker-fleet configuration.
- Source: §4.1
- Fields:
  - `count: int` (≥ status_policy.floor)
  - `models: list[str]` (explicit list; if absent env-resolved)
  - `timeout_sec: int` (default 180)
  - `temperature: float` (default 0.2)
  - `retry: dict` ({on_5xx: int=1, on_5xx_backoff_sec: int=2, on_4xx: int=0, on_timeout: int=0})

**DM-003: `ResultContract`**
- Path: `src/superclaude/cli/swarm/models.py`
- Role: Terminal-state return contract written to `return-contract.yaml`.
- Source: §5
- Fields:
  - `contract_version: str` ("1.0")
  - `status: Literal["success","partial","failed"]` (IMM-5 success-first)
  - `job_id: str`
  - `started: str` (ISO 8601)
  - `finished: str` (ISO 8601)
  - `elapsed_ms: int`
  - `caller: dict` ({skill, skill_version, invocation_label})
  - `lens: str | None`
  - `lens_source: Literal["registry","custom"] | None`
  - `target: dict` ({path, checksum, truncated, truncation_line_cap})
  - `workers_requested: int`
  - `workers_succeeded: int`
  - `workers_failed: int`
  - `output_files: list[WorkerResult]` (DM-004)
  - `amalgamation_mode: Literal["raw","normalize","normalize+merge"]`
  - `merged_path: str | None` (null when mode != normalize+merge OR M < 2)
  - `caller_metadata: dict` ({suspect: bool, tier: str})
  - `recommended_next_command: str` (rendered template)
  - `artifacts: dict` ({manifest_path, state_path, event_log_jsonl, event_log_md, done_sentinel})

**DM-004: `WorkerResult`**
- Path: `src/superclaude/cli/swarm/models.py`
- Role: Per-worker outcome element in result contract.
- Source: §5
- Fields:
  - `index: int`
  - `path: str | None` (null on hard failure)
  - `raw_path: str | None`
  - `meta_path: str`
  - `model_id: str`
  - `model_label: str`
  - `bytes: int`
  - `status: Literal["success","timeout","parse_error","proxy_error"]`
  - `http_code: int`
  - `attempts: int`
  - `elapsed_ms: int`

**DM-005: `SwarmState`**
- Path: `src/superclaude/cli/swarm/models.py`
- Role: `.swarm-state.json` durable run-state (atomic on transition).
- Source: §2.1, §7
- Fields:
  - `state: Literal["preflight_ok","dispatching","normalizing","reducing","terminal"]`
  - `job_id: str`
  - last-known transition timestamp, current wave, worker-progress map.

**DM-006: `EventRecord`**
- Path: `src/superclaude/cli/swarm/models.py`
- Role: JSONL event-log row (append-only, lock-coordinated).
- Source: §2.1, §8
- Fields: event_type (worker_start/worker_progress/worker_done/wave_transition/final), timestamp, worker_index (when applicable), payload.

**DM-007: `LensEntry`**
- Path: `src/superclaude/cli/swarm/lenses/__init__.py`
- Role: Frozen dataclass representing a single registered lens.
- Source: §3.2
- Fields:
  - `name: str` (kebab-case unique identifier)
  - `description: str` (one-line use case)
  - `system_prompt_fragment: str` (verbatim system-prompt content)
  - `user_template: str` (with `{target_content}` placeholder)
  - `output_template_path: str | None` (abs path to `refs/templates/<lens>-output.md`)
  - `recipe_name: str` (Recipe Protocol name or `custom-py:mod:func`)
  - `default_workers: int` (2-4)
  - `default_target_line_cap: int` (default 4000)
  - `suspect: bool`
  - `tier: str` (e.g., 'T2', 'T2-code', 'T2-spec')
  - `recommended_next_command_template: str` (with `{compare_files}` + optional `{suspect_files}`)
  - `acceptance_notes: str`
  - `stability: Literal["stable","experimental"]` (default "experimental")

**DM-008: `Manifest` (`manifest.json`)**
- Path: emitted per-job under `--output`
- Role: Durable definition of "what this swarm was supposed to do."
- Source: §3.6, §9.3
- Fields:
  - `contract_version: str`
  - `job_id: str`
  - `resolved_lens_entry: dict` (snapshot of LensEntry materialized at preflight: name, system_prompt_fragment, user_template, recipe_name, default_workers, suspect, tier, recommended_next_command_template, stability)
  - additional preflight-resolved fields.

**DM-009: `RecipeProtocol`**
- Path: `src/superclaude/cli/swarm/recipes/__init__.py`
- Role: Interface implemented by every normalizer + `REGISTRY` dict.
- Source: §2.1
- Methods: `normalize(raw_text: str, args: dict, template_path: str | None) -> tuple[str, dict]` (returns normalized markdown + metadata; raises ParseError on unsalvageable input).

**DM-010: `TransportProtocol`**
- Path: `src/superclaude/cli/swarm/transports/__init__.py`
- Role: Pluggable HTTP transport interface.
- Source: §2.1
- Methods: `dispatch(body: dict, timeout_sec: int) -> dict` (returns parsed JSON response or raises typed transport errors for 4xx/5xx/timeout).

## Risk Inventory

1. **Risk: Lens-registry sprawl (medium)** — Source: §15.1. Every new lens shipping a built-in entry bloats the registry. **Mitigation:** PR-review discipline requires a real caller; entries without a real caller deferred to `custom-py:` + caller-side custom prompts.

2. **Risk: Merge boundary erosion (high)** — Source: §15.2. `normalize+merge` mode could drift into judging via incremental PRs, blurring the boundary against `/sc:adversarial`. **Mitigation:** Four structural guards (docstring allowed/disallowed list + ≤30 LOC ceiling + PR-review boundary preservation note + `tests/swarm/test_merge_mechanical_only.py` boundary test) + CI rule flagging changes to the boundary test.

3. **Risk: Resume + lens-mutation interaction (medium)** — Source: §15.3. Lens registry mutation between original run and `--resume` could cause stale or inconsistent dispatch. **Mitigation:** Default rehydrates from `manifest.resolved_lens_entry` (INV-001 fix); `--force-relens` opts into re-resolution; tests cover both paths.

4. **Risk: Tmux dependency for detached mode (medium)** — Source: §15.4. Same risk as `sprint`. **Mitigation:** Detached mode is optional; inline mode is default.

5. **Risk: ThreadPoolExecutor surprise (low)** — Source: §15.5. Operators may expect process-based parallelism or async. **Mitigation:** Documented in `dispatch.py` docstring; tested with stub transport.

6. **Risk: Custom-prompt-dir guard parity backward-compat (medium)** — Source: §15.6. Existing `--custom-prompt-dir` users may need to add §11.5 sentence to `system.txt`. **Mitigation:** `--auto-inject-guard` flag for backward compatibility during migration window.

7. **Risk: Schema evolution drag (low)** — Source: §15.7. `spec_version` evolution complexity. **Mitigation:** Orchestrator at `1.1` can load specs at `1.0`; forward-compat best-effort.

## Dependency Inventory

1. **`superclaude.execution.parallel.ParallelExecutor`** — internal, mandated for ThreadPoolExecutor invocation (§8, AC-005).
2. **`httpx`** — external Python HTTP client for Phase-1 reference transport (§8, COMP-018).
3. **`click`** — CLI framework for Click group + subcommands (COMP-001, COMP-002).
4. **`rich`** — Live dashboard rendering for `--tui` flag (COMP-012) and `swarm status --watch` table (FR-003).
5. **`tmux`** — external system dependency for detached mode (COMP-013, §11.1, §15.4).
6. **`threading.Lock`** — Python stdlib for JSONL append + state-file coordination (§8).
7. **`os.replace`** — Python stdlib for atomic write (IMM-6, FR-047).
8. **T2 proxy** — external HTTP service exposing OpenAI-compatible API (env: `T2ProxyUrl`, `T2ProxyKey`, `T2Model0N`) (FR-019, §11.2).
9. **Lens template files** — `refs/templates/<lens>-output.md` per stable lens (DM-007).
10. **Parent spec `bare-review v1.3.0-draft`** — IMM-N invariants + §11.5 + §7.4 salvage semantics inherited (§1.2, §12).
11. **`/sc:adversarial` downstream command** — referenced by `bare-review` lens `recommended_next_command_template` (§12, COMP-019).
12. **`sprint/tmux.py`** — internal sibling whose detached-run pattern is mirrored (COMP-013).

## Success Criteria

1. **SC-001:** `superclaude swarm run --lens bare-review --target X --output Y --workers 3` produces a `return-contract.yaml` byte-for-byte equivalent (modulo timestamps + checksums) to today's `sc-bare-review` output. Source: §16 Phase 8 (A/B parity test).

2. **SC-002:** IMM-3 verified by stub-worker parallelism test: N stub workers complete within `max(per_worker_elapsed) + ε`, NOT `Σ(per_worker_elapsed)`. Source: §16.1.

3. **SC-003:** IMM-4 verified by 49-byte target test: target with <50 non-whitespace bytes triggers `failed`/`target-too-small` contract before any dispatch. Source: §16.1.

4. **SC-004:** IMM-5 verified by parametrized status test covering `M==N`, `M==N==2`, `2≤M<N`, `M<2` cases with `success_first=true` ordering. Source: §16.1.

5. **SC-005:** IMM-6 verified by mid-write kill test: process killed during output write leaves no partial file at the deterministic final path. Source: §16.1.

6. **SC-006:** §11.5 verified by target-containing-end-marker test: target text containing `<<<END TARGET>>>` literal does not allow injection past the delimiter. Source: §16.1.

7. **SC-007:** INV-001 verified by `tests/swarm/test_resume_uses_manifest_lens.py`: `--resume` reads `resolved_lens_entry` from manifest, ignores mutated registry. Source: §16.2.

8. **SC-008:** INV-002 verified by `tests/swarm/test_concurrency_python_only.py`: no shell-script dispatch path exercised; all parallelism via Python ThreadPoolExecutor. Source: §16.2.

9. **SC-009:** INV-003 verified by `tests/swarm/test_custom_prompt_dir_injection_guard.py`: `--custom-prompt-dir` without §11.5 substring STOPs with actionable error; with `--auto-inject-guard` prepends canonical sentence. Source: §16.2.

10. **SC-010:** INV-010 verified by `tests/swarm/test_resume_regenerates_merge.py`: `--resume` + `normalize+merge` always regenerates `merged.md` after Wave 2. Source: §16.2.

11. **SC-011:** INV-014 verified by `tests/swarm/test_escape_hatch_guard_parity.py`: escape-hatch (custom-prompt-dir) path enforces injection guard identically to lens-driven and JSON-Schema paths. Source: §16.2.

12. **SC-012:** Merge boundary verified by `tests/swarm/test_merge_mechanical_only.py`: 3-worker concat produces all 3 sections in slot-index order with no transformations beyond provenance header; merge module body remains ≤30 LOC. Source: §10.2, §16.2.

13. **SC-013:** `swarm validate-lenses` returns exit 0 on the bundled 8-entry registry and exit non-zero with diagnostics for: missing template files, unregistered recipe names, suspect:true entries missing `{suspect_files}` template substitution, duplicate names, missing §11.5 substring. Source: §3.5, §13.1.

14. **SC-014:** Detached mode + resume + `swarm attach` end-to-end demonstration: long-running job survives caller-process termination, resumes via `swarm run --resume`, attaches via `swarm attach`, terminates via `swarm kill`. Source: §11.1, §16 Phase 6.

15. **SC-015:** Non-precluding contract surface verified by header-grep audit: zero references to Claude tool names in `models.py`, `schema.py`, result-contract YAML output, and CLI `--help` text. Source: §13.

16. **SC-016:** Migration completeness: after Phase 9, `sc-bare-review` SKILL.md is ~60 lines (vs current), all `scripts/*.sh` are deleted, and production parity is observed across an A/B test window. Source: §16 Phases 8-9.

## Open Questions

1. **OQ-001:** Should `validate-lenses` run as a pre-commit hook by default? (Recommend yes; deferred to implementation tasklist for hook wiring.) Source: §17.

2. **OQ-002:** Per-lens version pinning (`--lens-version v2`)? Deferred until lens definitions mutate frequently in production. Source: §17.

3. **OQ-003:** Should `recommended_next_command` ever be auto-executed via `--auto-handoff`? Deferred. Source: §17.

4. **OQ-004:** Prometheus / OpenMetrics output at event boundaries? Deferred. Source: §17.

5. **OQ-005:** Per-model overrides (e.g., per-model temperature) within one swarm? Deferred until a real lens asks; relates to A-005 shared assumption (partially open). Source: §17.

6. **OQ-006:** Concurrent-`--output`-dir protection? Deferred; document caller-must-avoid for v1. Source: §17.

7. **OQ-007:** Workers > configured T2Models guard (INV-005) — adopt warn-on-exceed-with-defaults (V1 semantics) or STOP (V2 semantics)? Spec recommends warn; flagged for tasklist confirmation. Source: §17.

8. **OQ-008:** Empty-pool failure path (INV-007) — write `failed`/`env-missing` contract OR pre-output-dir abort? Spec recommends write-on-failure when output dir creatable, pre-output-dir abort otherwise; needs implementation confirmation. Source: §17.
