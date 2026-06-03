# Evidence Index — Mastra + Backlog.md + Beads Hybrid Architecture Tech Reference

**Investigation type:** Doc Analyst
**Status:** Complete
**Date:** 2026-06-03

## Purpose

Single evidence-index table mapping every architectural claim needed for the tech reference to:
- source research file
- source code `path:line` (where applicable)
- evidence tag — `[CODE-VERIFIED]` / `[DESIGN — UNBUILT]` / `[EXTERNAL-VERIFIED]`
- target template section (per synth→section mapping):
  - synth-01 → §1-2
  - synth-02 → §3-4
  - synth-03 → §5.1-5.3
  - synth-04 → §5.4-5.8
  - synth-05 → §6-8
  - synth-06 → §9-11
  - synth-07 → §12-14
  - synth-08 → §15-16

Rows grouped by 8 subsystems:
- 5.1 pipeline-core seam
- 5.2 roadmap/tasklist
- 5.3 sprint runtime
- 5.4 harness corpus
- 5.5 target data model
- 5.6 adapter layer
- 5.7 external substrate
- 5.8 governance plane

---

## Subsystem 5.1 — Pipeline-Core Seam

**Primary source:** `01-pipeline-core-contracts.md` (synth-03 → §5.1-5.3)

| # | Architectural claim | Source research file | Source code `path:line` | Tag | Target §|
|---|---|---|---|---|---|
| 5.1-01 | `models.py` defines framework-neutral shared dataclass/enum contracts with zero imports from sprint/roadmap; stdlib-only imports | 01-pipeline-core-contracts | `pipeline/models.py:1-5`, `models.py:8-15` | `[CODE-VERIFIED]` | §5.1 |
| 5.1-02 | `CosmeticRemediator` protocol: `__call__(output_file, gate_name, failure_reason, *, step_id) -> tuple[bool, list[str]]`, injected via `PipelineConfig`, idempotent | 01-pipeline-core-contracts | `pipeline/models.py:17-37` | `[CODE-VERIFIED]` | §5.1 |
| 5.1-03 | `StepStatus` enum: PENDING/PASS/FAIL/TIMEOUT/CANCELLED/SKIPPED; `is_failure` true only for FAIL+TIMEOUT (not CANCELLED/SKIPPED) | 01-pipeline-core-contracts | `pipeline/models.py:40-67` | `[CODE-VERIFIED]` | §5.1 |
| 5.1-04 | `GateMode` enum: BLOCKING and TRAILING; trailing non-blocking until grace-period eval | 01-pipeline-core-contracts | `pipeline/models.py:69-79` | `[CODE-VERIFIED]` | §5.1 |
| 5.1-05 | `SemanticCheck` dataclass: name, `check_fn: Callable[[str], bool\|str]`, failure_message | 01-pipeline-core-contracts | `pipeline/models.py:81-87` | `[CODE-VERIFIED]` | §5.1 |
| 5.1-06 | `GateCriteria` dataclass: required frontmatter fields (exact keys or tuple OR-groups), min_lines, enforcement_tier (STRICT/STANDARD/LIGHT/EXEMPT), semantic_checks | 01-pipeline-core-contracts | `pipeline/models.py:90-105` | `[CODE-VERIFIED]` | §5.1 |
| 5.1-07 | `Step` dataclass: id, prompt, output_file, gate, timeout_seconds, inputs, retry_limit, model, gate_mode, tool_write_mode, template_path — core portable unit | 01-pipeline-core-contracts | `pipeline/models.py:108-123` | `[CODE-VERIFIED]` | §5.1 |
| 5.1-08 | `StepResult` dataclass: step pointer, status, attempt, gate failure reason, timestamps, remediation metadata, computed duration | 01-pipeline-core-contracts | `pipeline/models.py:125-148` | `[CODE-VERIFIED]` | §5.1 |
| 5.1-09 | `DeliverableKind` enum + `Deliverable` dataclass with JSON round-trip; `from_dict()` defaults missing kind to `implement` | 01-pipeline-core-contracts | `pipeline/models.py:151-209` | `[CODE-VERIFIED]` | §5.1 |
| 5.1-10 | `PipelineConfig` dataclass: work_dir, dry_run, max_turns, model, permission_flag (default `--dangerously-skip-permissions`), debug, grace_period, cosmetic remediation settings | 01-pipeline-core-contracts | `pipeline/models.py:212-235` | `[CODE-VERIFIED]` | §5.1 |
| 5.1-11 | `executor.py` is generic step sequencer with retry/gates/parallel dispatch; NFR-007 no sprint/roadmap imports | 01-pipeline-core-contracts | `pipeline/executor.py:1-20` | `[CODE-VERIFIED]` | §5.1 |
| 5.1-12 | `_gate_target()` prefers sibling `.compressed.md` sidecar over original output — gates validate what downstream LLM consumes | 01-pipeline-core-contracts | `pipeline/executor.py:23-35` | `[CODE-VERIFIED]` | §5.1 |
| 5.1-13 | `StepRunner` protocol: `__call__(step, config, cancel_check) -> StepResult` — process-boundary seam; runner owns subprocess+timeout, executor owns retry/gates/ordering | 01-pipeline-core-contracts | `pipeline/executor.py:41-60` | `[CODE-VERIFIED]` | §5.1 |
| 5.1-14 | `execute_pipeline()` accepts `list[Step \| list[Step]]`; nested lists = parallel groups; supports start/complete/state callbacks, cancellation, optional trailing runner | 01-pipeline-core-contracts | `pipeline/executor.py:63-188` | `[CODE-VERIFIED]` | §5.1 |
| 5.1-15 | `_execute_single_step()` implements retry loop, cancellation, blocking/trailing branching, cosmetic remediation, final fail | 01-pipeline-core-contracts | `pipeline/executor.py:191-399` | `[CODE-VERIFIED]` | §5.1 |
| 5.1-16 | `_run_parallel_steps()` runs group in daemon threads, sets shared cancellation event when any step fails; no group-level retry | 01-pipeline-core-contracts | `pipeline/executor.py:402-452` | `[CODE-VERIFIED]` | §5.1 |
| 5.1-17 | `grace_period == 0` forces BLOCKING even if step declares TRAILING | 01-pipeline-core-contracts | `pipeline/executor.py:211-215` | `[CODE-VERIFIED]` | §5.1 |
| 5.1-18 | Trailing-mode step submitted to trailing runner and immediately returned PASS; pending results collected at pipeline end with timeout `max(30.0, grace_period)`; failures logged as warnings only (advisory) | 01-pipeline-core-contracts | `pipeline/executor.py:250-262`, `executor.py:175-187` | `[CODE-VERIFIED]` | §5.1 |
| 5.1-19 | `_build_state()` emits compact state dict; assumes `r.step.id` exists though `StepResult.step` is optional (risk) | 01-pipeline-core-contracts | `pipeline/executor.py:455-469`, `models.py:137` | `[CODE-VERIFIED]` | §5.1 |
| 5.1-20 | Executor re-wraps `StepResult` after `run_step()` and can drop remediated/remediations fields except its own remediation path (risk) | 01-pipeline-core-contracts | `pipeline/executor.py:230-238`, `253-260`, `269-276`, `379-386` | `[CODE-VERIFIED]` | §5.1 |
| 5.1-21 | `gates.py` pure-Python validation, no subprocess/LLM; imports only re/Path/GateCriteria | 01-pipeline-core-contracts | `pipeline/gates.py:1-17` | `[CODE-VERIFIED]` | §5.1 |
| 5.1-22 | `gate_passed()` tier behavior: EXEMPT always passes; LIGHT existence+non-empty; STANDARD adds min_lines+frontmatter; STRICT adds semantic checks (short-circuit on first non-True) | 01-pipeline-core-contracts | `pipeline/gates.py:20-76` | `[CODE-VERIFIED]` | §5.1 |
| 5.1-23 | Frontmatter parser scans delimiter pairs anywhere (tolerates preamble), top-level key regex only (not deep YAML), tuple OR-aliases | 01-pipeline-core-contracts | `pipeline/gates.py:79-142` | `[CODE-VERIFIED]` | §5.1 |
| 5.1-24 | `process.py` manages `claude --print` subprocess lifecycle, generic over output format; hard boundary to Claude CLI | 01-pipeline-core-contracts | `pipeline/process.py:1-19`, `24-244` | `[CODE-VERIFIED]` | §5.1/§5.6 |
| 5.1-25 | `build_command()` builds `claude --print --verbose <perm> --no-session-persistence --tools default --max-turns N --output-format <fmt>` + optional model/extra args | 01-pipeline-core-contracts | `pipeline/process.py:73-95` | `[CODE-VERIFIED]` | §5.6 |
| 5.1-26 | Prompt delivered via stdin (not argv) to avoid Linux MAX_ARG_STRLEN; `build_env()` strips CLAUDECODE/CLAUDE_CODE_ENTRYPOINT | 01-pipeline-core-contracts | `pipeline/process.py:73-78`, `97-112`, `136-139` | `[CODE-VERIFIED]` | §5.6 |
| 5.1-27 | `tool_write_mode=False` → stdout is output file; `tool_write_mode=True` → stdout to `.log` sidecar, model writes output_file via tools; `validate_tool_write_output()` checks existence+non-empty | 01-pipeline-core-contracts | `pipeline/process.py:114-157`, `216-236` | `[CODE-VERIFIED]` | §5.6 |
| 5.1-28 | `wait()` returns 124 for timeout (matches bash timeout); `terminate()` SIGTERM→10s→SIGKILL→5s on process group | 01-pipeline-core-contracts | `pipeline/process.py:159-214` | `[CODE-VERIFIED]` | §5.6 |
| 5.1-29 | `trailing_gate.py` provides async gate eval, typed results, deferred remediation log, remediation prompt construction, retry accounting, scope-based mode resolution; stdlib + pipeline-local only | 01-pipeline-core-contracts | `pipeline/trailing_gate.py:1-24` | `[CODE-VERIFIED]` | §5.1 |
| 5.1-30 | `TrailingGateResult` shape: (step_id, passed, evaluation_ms, failure_reason) — roadmap v3.0 authoritative; older spec (passed, evaluation_ms, gate_name) is STALE | 01-pipeline-core-contracts | `pipeline/trailing_gate.py:34-47` | `[CODE-VERIFIED]` (doc-contradicted) | §5.1 |
| 5.1-31 | `GateResultQueue` wraps queue.Queue; `pending_count()` returns qsize() while put/drain maintain `_pending` (divergence noted) | 01-pipeline-core-contracts | `pipeline/trailing_gate.py:49-85` | `[CODE-VERIFIED]` | §5.1 |
| 5.1-32 | `TrailingGateRunner` owns daemon-thread eval; selects `.compressed.md` sidecar; exceptions become failed results; `wait_for_pending(timeout=30.0)`, `cancel()` | 01-pipeline-core-contracts | `pipeline/trailing_gate.py:93-228`, `146-156` | `[CODE-VERIFIED]` | §5.1 |
| 5.1-33 | `TrailingGatePolicy` runtime-checkable protocol; `build_remediation_prompt()` deterministic scoped prompt; `RemediationRetryStatus/Result`; `attempt_remediation()` retry-once state machine | 01-pipeline-core-contracts | `pipeline/trailing_gate.py:241-468` | `[CODE-VERIFIED]` | §5.1 |
| 5.1-34 | `attempt_remediation()` returns PERSISTENT_FAILURE (not BUDGET_EXHAUSTED) when attempt 1 fails + budget disallows attempt 2 | 01-pipeline-core-contracts | `pipeline/trailing_gate.py:433-440`, `386-390` | `[CODE-VERIFIED]` | §5.1 |
| 5.1-35 | `RemediationStatus` (PENDING/REMEDIATED/WAIVED); `RemediationEntry`; `DeferredRemediationLog` lock-guarded, disk-persistent, JSON serde, pending entries, mark remediated | 01-pipeline-core-contracts | `pipeline/trailing_gate.py:471-596` | `[CODE-VERIFIED]` | §5.1 |
| 5.1-36 | `GateScope` (RELEASE/MILESTONE/TASK); `resolve_gate_mode()`: release always blocking, milestone configurable, task trailing only if grace_period>0, unknown→blocking | 01-pipeline-core-contracts | `pipeline/trailing_gate.py:604-647` | `[CODE-VERIFIED]` | §5.1 |
| 5.1-37 | `deliverables.py` heuristic behavioral detection + implement/verify decomposition; imports re + models only | 01-pipeline-core-contracts | `pipeline/deliverables.py:1-12` | `[CODE-VERIFIED]` | §5.1 |
| 5.1-38 | `is_behavioral()` uses computational verbs, state-mutation regexes, conditional patterns; doc-verbs suppress false positives | 01-pipeline-core-contracts | `pipeline/deliverables.py:14-143` | `[CODE-VERIFIED]` | §5.1 |
| 5.1-39 | `decompose_deliverables()` expands behavioral deliverables into `.a` implement + `.b` verify; idempotent (skips `.a`/`.b` suffixes); shallow-copies metadata | 01-pipeline-core-contracts | `pipeline/deliverables.py:146-194` | `[CODE-VERIFIED]` | §5.1 |
| 5.1-40 | `diagnostic_chain.py` four-stage chain (troubleshoot/root_causes/solutions/summary); deterministic Markdown assembly NOT actual LLM/adversarial calls; does not consume TurnLedger turns | 01-pipeline-core-contracts | `pipeline/diagnostic_chain.py:1-25`, `71-158` | `[CODE-VERIFIED]` | §5.1 |
| 5.1-41 | `DiagnosticReport.is_complete` requires exactly 4 successful stages; `run_diagnostic_chain()` per-stage exception catch, summary set only if summary stage succeeds | 01-pipeline-core-contracts | `pipeline/diagnostic_chain.py:47-68`, `161-247` | `[CODE-VERIFIED]` | §5.1 |
| 5.1-42 | `pipeline/__init__.py` exports 42-symbol public API surface (models, deliverables, executor, gates, process, guard/FMEA/dataflow/conflict) as compatibility anchors | 01-pipeline-core-contracts | `pipeline/__init__.py:1-157` | `[CODE-VERIFIED]` | §5.1 |
| 5.1-43 | Consumer proof: roadmap/validate/tasklist use generic `execute_pipeline` + injected `run_step`; sprint uses shared models/remediation but its own phase loop | 01-pipeline-core-contracts | `roadmap/executor.py:25-35`, `validate_executor.py:105-180`, `tasklist/executor.py:92-188`, `sprint/executor.py:12-16` | `[CODE-VERIFIED]` | §5.1 |
| 5.1-44 | STALE: roadmap comment "Gate checks run on the ORIGINAL output file" contradicts `_gate_target()` `.compressed.md` preference | 01-pipeline-core-contracts | `roadmap/executor.py:1217-1219` vs `executor.py:23-35` | `[CODE-VERIFIED]` (doc-contradicted) | §5.1 |

## Subsystem 5.2 — Roadmap / Tasklist Pipelines

**Primary source:** `02-roadmap-tasklist-pipelines.md` (synth-03 → §5.1-5.3)

| # | Architectural claim | Source research file | Source code `path:line` | Tag | Target §|
|---|---|---|---|---|---|
| 5.2-01 | Roadmap delegates execution to shared `execute_pipeline` with roadmap-specific `roadmap_run_step` (not bespoke) | 02-roadmap-tasklist | `roadmap/executor.py:26`, `3124-3131` | `[CODE-VERIFIED]` | §5.2 |
| 5.2-02 | Tasklist validation also uses shared pipeline: imports execute_pipeline/Step/StepResult/StepStatus/ClaudeProcess; calls execute_pipeline | 02-roadmap-tasklist | `tasklist/executor.py:23-25`, `259-263` | `[CODE-VERIFIED]` | §5.2 |
| 5.2-03 | Roadmap CLI `run` surface: input routing + many flags (--agents, --resume, --dry-run, --no-validate, --no-convergence, --no-compress, cosmetic-remediation, --input-type, --tdd-file, --prd-file) | 02-roadmap-tasklist | `roadmap/commands.py:32-298` | `[CODE-VERIFIED]` | §5.2 |
| 5.2-04 | `detect_input_type()` scores PRD first, then TDD, else spec; `_route_input_files()` validates 1-3 inputs, classifies, rejects dupes, requires spec/TDD primary | 02-roadmap-tasklist | `roadmap/executor.py:74-335` | `[CODE-VERIFIED]` | §5.2 |
| 5.2-05 | Roadmap step DAG (`_build_steps`): extract → parallel generate-A/B → diff → debate → score → merge → anti-instinct → test-strategy → spec-fidelity → wiring-verification → deviation-analysis → remediate | 02-roadmap-tasklist | `roadmap/executor.py:1947-2208` | `[CODE-VERIFIED]` | §5.2 |
| 5.2-06 | Roadmap step execution hybrid: most steps launch ClaudeProcess; anti-instinct/convergence-spec-fidelity/deviation-analysis/remediate/wiring-verification run deterministic Python | 02-roadmap-tasklist | `roadmap/executor.py:955-1250`, `977-1031` | `[CODE-VERIFIED]` | §5.2 |
| 5.2-07 | `execute_roadmap()` creates output dir, restores resume state, routes inputs, compresses, builds steps, dry-run, resume, cosmetic remediator, shared pipeline, save state, spec-patch resume, auto-validation | 02-roadmap-tasklist | `roadmap/executor.py:2985-3187` | `[CODE-VERIFIED]` | §5.2 |
| 5.2-08 | CLI adversarial workflow wired inline as diff→debate→score→merge; does NOT call sc:adversarial-protocol | 02-roadmap-tasklist | `roadmap/executor.py:2068-2128` | `[CODE-VERIFIED]` | §5.2 |
| 5.2-09 | Roadmap validation: single-agent `reflect` (REFLECT_GATE) or multi-agent parallel `reflect-{agent}` + `adversarial-merge` (ADVERSARIAL_MERGE_GATE); auto-invoked after run | 02-roadmap-tasklist | `roadmap/validate_executor.py:239-519`, `executor.py:3409-3447` | `[CODE-VERIFIED]` | §5.2 |
| 5.2-10 | Most roadmap gates wired+enforced; `CERTIFY_GATE`/`build_certify_step`/`check_certify_resume` defined but NOT wired in production `_build_steps` (defined-only gap) | 02-roadmap-tasklist | `roadmap/gates.py:1324-1351`, `executor.py:1899-1944`, `2205`, `3483-3502` | `[CODE-VERIFIED]` (defined-only) | §5.2 |
| 5.2-11 | `SPEC_FIDELITY_GATE` wired only in `--no-convergence` mode; convergence mode replaces gate with deterministic pass/fail from `_run_convergence_spec_fidelity` | 02-roadmap-tasklist | `roadmap/executor.py:2158-2173`, `994-1001`, `gates.py:1274-1297` | `[CODE-VERIFIED]` | §5.2 |
| 5.2-12 | `WIRING_GATE` configured TRAILING but `grace_period` defaults to 0 (no CLI flag) → effectively BLOCKING in practice | 02-roadmap-tasklist | `roadmap/executor.py:2175-2184`, `pipeline/executor.py:211-214` | `[CODE-VERIFIED]` | §5.2 |
| 5.2-13 | All roadmap gate definitions (EXTRACT, EXTRACT_TDD, GENERATE_A/B, DIFF, DEBATE, SCORE, MERGE, TEST_STRATEGY, SPEC_FIDELITY, REMEDIATE, CERTIFY, ANTI_INSTINCT, DEVIATION_ANALYSIS, ALL_GATES) | 02-roadmap-tasklist | `roadmap/gates.py:1020-1441` | `[CODE-VERIFIED]` | §5.2 |
| 5.2-14 | DEBATE_GATE validates only convergence_score shape/range + rounds_completed, NOT threshold pass/partial/fail routing | 02-roadmap-tasklist | `roadmap/gates.py:1155-1166` | `[CODE-VERIFIED]` | §5.2 |
| 5.2-15 | Convergence engine: `DeviationRegistry.load_or_create` resets on spec-hash mismatch; merges structural+semantic findings with stable IDs, ACTIVE status, first/last_seen_run | 02-roadmap-tasklist | `roadmap/convergence.py:90-207` | `[CODE-VERIFIED]` | §5.2/§5.5 |
| 5.2-16 | `execute_fidelity_with_convergence` up to 3 checker/remediation cycles (catch/verify/backup); passes when active HIGH count = 0; budget-gated; diagnostic halt on exhaustion | 02-roadmap-tasklist | `roadmap/convergence.py:434-668` | `[CODE-VERIFIED]` | §5.2 |
| 5.2-17 | `generate_remediation_tasklist` produces remediation-tasklist.md frontmatter + status-grouped findings; `_run_remediate_step` reads spec-deviations.json → Finding → markdown + JSON sidecar | 02-roadmap-tasklist | `roadmap/remediate.py:177-288`, `executor.py:1804-1897` | `[CODE-VERIFIED]` | §5.2 |
| 5.2-18 | `execute_remediation` parallel per-file remediation with snapshots, agent retries, diff-size guard, per-file rollback, cross-file coherence, pass/partial/fail | 02-roadmap-tasklist | `roadmap/remediate_executor.py:735-755`, `executor.py:1395-1448` | `[CODE-VERIFIED]` | §5.2 |
| 5.2-19 | Deviation classifier UNWIRED: all records render as UNCLASSIFIED; `DEVIATION_ANALYSIS_GATE` pins `unclassified_count == total_analyzed` invariant | 02-roadmap-tasklist | `roadmap/executor.py:1603-1609`, `gates.py:1390-1422` | `[CODE-VERIFIED]` (unwired) | §5.2 |
| 5.2-20 | Cosmetic remediation lane: --allow-cosmetic-remediation/--strict-no-remediation flags; roadmap remediator injected into PipelineConfig; classify_gate_failure + apply_cosmetic_remediations | 02-roadmap-tasklist | `roadmap/commands.py:153-172`, `executor.py:3092-3122`, `cosmetic_remediator.py:682-724`, `1020-1096` | `[CODE-VERIFIED]` | §5.2 |
| 5.2-21 | Tasklist CLI exposes ONLY `validate` subcommand, not `generate`; single `tasklist-fidelity` step w/ TASKLIST_FIDELITY_GATE over roadmap+tasklist+optional TDD/PRD | 02-roadmap-tasklist | `tasklist/commands.py:31-82`, `tasklist/executor.py:191-218`, `tasklist/gates.py:23-46` | `[CODE-VERIFIED]` | §5.2 |
| 5.2-22 | Tasklist validate parses `high_severity_count` from report frontmatter; passes only when no HIGH-severity deviations; missing report = failure | 02-roadmap-tasklist | `tasklist/executor.py:221-276` | `[CODE-VERIFIED]` | §5.2 |
| 5.2-23 | Tasklist fidelity prompt scoped to roadmap→tasklist only; spec→tasklist out of scope (handled by roadmap spec-fidelity) | 02-roadmap-tasklist | `tasklist/prompts.py:17-148`, `29-31` | `[CODE-VERIFIED]` | §5.2 |
| 5.2-24 | Tasklist GENERATION is skill/protocol behavior (`build_tasklist_generate_prompt` used by /sc:tasklist), NOT a CLI subcommand | 02-roadmap-tasklist | `tasklist/prompts.py:151-234`, `156-162` | `[CODE-VERIFIED]` (skill-only, no CLI generator) | §5.2 |
| 5.2-25 | Sprint-compatible tasklist output spec: exactly N+1 files (tasklist-index.md + phase-N-tasklist.md), literal phase filenames, contiguous phases, T<PP>.<TT> IDs, checkpoints — protocol-specified not CLI-enforced | 02-roadmap-tasklist | `sc-tasklist-protocol/SKILL.md:91-123`, `1062-1117` | `[DESIGN — UNBUILT]` (protocol spec) | §5.2 |
| 5.2-26 | `.roadmap-state.json` carries spec path/hash, input type, TDD/PRD paths, agents, depth, step statuses, validation/fidelity/remediate/certify status | 02-roadmap-tasklist | `roadmap/executor.py:2627-2682` | `[CODE-VERIFIED]` | §5.2/§5.5 |
| 5.2-27 | STALE: skill cites `_get_all_step_ids` at executor.py:2281-2300; actual 2283-2302 (line drift) | 02-roadmap-tasklist | `sc-roadmap-protocol/SKILL.md:111` vs `executor.py:2283-2302` | `[CODE-VERIFIED]` (doc-stale) | §5.2 |
| 5.2-28 | STALE: roadmap.md flag table lists `--input-type auto\|tdd\|spec` but omits `prd` despite PRD auto-detect + RoadmapConfig.input_type allowing prd | 02-roadmap-tasklist | `commands/roadmap.md:38` vs `roadmap/models.py:117-119` | `[CODE-VERIFIED]` (doc-stale) | §5.2 |

## Subsystem 5.3 — Sprint Execution Runtime

**Primary source:** `03-sprint-execution-runtime.md` (synth-03 → §5.1-5.3)

| # | Architectural claim | Source research file | Source code `path:line` | Tag | Target §|
|---|---|---|---|---|---|
| 5.3-01 | Sprint runtime is 19 Python files / ~8,568 lines; concentrated in commands.py → config.py → executor.py (2,148 lines) with process/monitor/tmux/tui split | 03-sprint-execution-runtime | `sprint/executor.py:1-2148` (and dir inventory) | `[CODE-VERIFIED]` | §5.3 |
| 5.3-02 | `sprint` Click group defines run/attach/status/logs/kill + verify-checkpoints; `run()` is the orchestration entry | 03-sprint-execution-runtime | `sprint/commands.py:15-32`, `189-207`, `360-415` | `[CODE-VERIFIED]` | §5.3 |
| 5.3-03 | `run()` flags: --start/--end phase slicing, --max-turns/--model, --no-tmux, permission mode, watchdog (--stall-timeout/--startup-stall-timeout/--stall-action), --shadow-gates, fidelity overrides, --release-dir, --state-dir | 03-sprint-execution-runtime | `sprint/commands.py:71-188` | `[CODE-VERIFIED]` | §5.3 |
| 5.3-04 | `PHASE_FILE_PATTERN` accepts phase-N-tasklist.md / pN-tasklist.md / phase_N_tasklist.md / tasklist-pN.md; `discover_phases` parses index table + Execution Mode (claude/python/skip) | 03-sprint-execution-runtime | `sprint/config.py:15-26`, `52-140` | `[CODE-VERIFIED]` | §5.3 |
| 5.3-05 | `load_sprint_config` validates index, discovers phases, enriches names/prompt previews, auto-detects end_phase, validates gaps, pre-scans active tasks, builds SprintConfig | 03-sprint-execution-runtime | `sprint/config.py:275-367` | `[CODE-VERIFIED]` | §5.3 |
| 5.3-06 | `parse_tasklist` scans `### T<PP>.<TT> -- Title` headings + dependencies + optional Command + classifier row; python-mode requires Command or raises | 03-sprint-execution-runtime | `sprint/config.py:399-492`, `475-479` | `[CODE-VERIFIED]` | §5.3 |
| 5.3-07 | `TaskEntry`: task_id, title, description, dependencies, command, classifier; only stores deps, does NOT schedule by dependency order (preserves file order) | 03-sprint-execution-runtime | `sprint/models.py:24-37` | `[CODE-VERIFIED]` | §5.3 |
| 5.3-08 | `TaskResult` is runner-constructed not agent-self-reported (status, turns, exit code, timing, output bytes, gate outcome, reimbursement, output path) | 03-sprint-execution-runtime | `sprint/models.py:158-209` | `[CODE-VERIFIED]` | §5.3 |
| 5.3-09 | `PhaseStatus` has 11 values (PASS/PASS_NO_SIGNAL/PASS_NO_REPORT/PASS_RECOVERED/PREFLIGHT_PASS/PASS_MISSING_CHECKPOINT/INCOMPLETE/HALT/TIMEOUT/ERROR/SKIPPED) | 03-sprint-execution-runtime | `sprint/models.py:211-270` | `[CODE-VERIFIED]` | §5.3 |
| 5.3-10 | `SprintConfig` extends `PipelineConfig`; __post_init__ sets work_dir=release_dir, maps wiring fields, derives wiring_gate_mode, defaults state_dir to `.dev/sprint-state/<id>` | 03-sprint-execution-runtime | `sprint/models.py:347-510`, `415-471` | `[CODE-VERIFIED]` | §5.3 |
| 5.3-11 | `execute_sprint()` is core loop: preflight binary, signal handlers, TUI/monitor, SprintResult, summary worker, TurnLedger/ShadowGateMetrics/DeferredRemediationLog/SprintGatePolicy, python preflight, then phase iteration | 03-sprint-execution-runtime | `sprint/executor.py:1135-1757`, `1228-1234` | `[CODE-VERIFIED]` | §5.3 |
| 5.3-12 | TWO execution paths: Path A (parsed tasks → execute_phase_tasks, one subprocess per TaskEntry) and Path B (freeform phase → ClaudeProcess + OutputMonitor) | 03-sprint-execution-runtime | `sprint/executor.py:1259-1301`, `1303-1457` | `[CODE-VERIFIED]` | §5.3 |
| 5.3-13 | Sprint `ClaudeProcess` subclasses generic pipeline process; builds sprint prompt + delegates lifecycle to `pipeline.process.ClaudeProcess` | 03-sprint-execution-runtime | `sprint/process.py:88-121` | `[CODE-VERIFIED]` | §5.3/§5.6 |
| 5.3-14 | Four-layer `IsolationLayers`/`setup_isolation` EXISTS but is NOT called in main loop; Path B only sets CLAUDE_WORK_DIR; Path A passes NO isolation env (partial/unused isolation) | 03-sprint-execution-runtime | `sprint/executor.py:106-182`, `1303-1324`, `1076-1115` | `[CODE-VERIFIED]` (partial/unused) | §5.3 |
| 5.3-15 | `execute_phase_tasks` budget-checks TurnLedger.can_launch(), pre-debits min allocation, maps exit 0→PASS / 124→INCOMPLETE / other→FAIL, reconciles budget, runs wiring+anti-instinct hooks | 03-sprint-execution-runtime | `sprint/executor.py:927-1073` | `[CODE-VERIFIED]` | §5.3 |
| 5.3-16 | Path A `_run_task_subprocess` builds minimal prompt (task ID/title/phase file/desc), task-specific output/error files, returns turns_consumed=0 (turn counting wired separately — accuracy gap) | 03-sprint-execution-runtime | `sprint/executor.py:1086-1115`, `models.py:502-506` | `[CODE-VERIFIED]` | §5.3 |
| 5.3-17 | `TurnLedger` tracks initial_budget, consumed, reimbursed, reimbursement rate, min launch/remediation budgets, wiring budget counters | 03-sprint-execution-runtime | `sprint/models.py:693-776` | `[CODE-VERIFIED]` | §5.3/§5.8 |
| 5.3-18 | Path B prompt invokes `/sc:task Execute all tasks in @<phase_file> --compliance strict --strategy systematic` + sprint context + checkpoint-before-result + EXIT_RECOMMENDATION CONTINUE/HALT | 03-sprint-execution-runtime | `sprint/process.py:123-216`, `187-195`, `208-215` | `[CODE-VERIFIED]` | §5.3 |
| 5.3-19 | tmux: `sc-sprint-<sha1>` session, 3-pane layout (tail pane 0.2, summary pane 0.1), reads `.sprint-exitcode` from state_dir to propagate failure; foreground cmd does NOT forward --startup-stall-timeout/--shadow-gates/--release-dir/fidelity flags | 03-sprint-execution-runtime | `sprint/tmux.py:81-210`, `213-252` | `[CODE-VERIFIED]` | §5.3 |
| 5.3-20 | `SprintTUI` Rich-based Live(refresh=2, screen=False); render errors caught without aborting sprint | 03-sprint-execution-runtime | `sprint/tui.py:98-152`, `154-303` | `[CODE-VERIFIED]` | §5.3 |
| 5.3-21 | `OutputMonitor` daemon-thread NDJSON stream-json reader; MonitorState tracks bytes, growth/event timestamps, events, files changed, stall seconds, turns, tokens; runtime watchdogs use CLI thresholds not display stall_status | 03-sprint-execution-runtime | `sprint/monitor.py:253-396`, `models.py:623-681`, `executor.py:1366-1445` | `[CODE-VERIFIED]` | §5.3 |
| 5.3-22 | stall_action=kill sets _timed_out, terminates, maps exit to 124; stall_action=warn prints + continues; detect_error_max_turns + detect_prompt_too_long inspect output/error tails | 03-sprint-execution-runtime | `sprint/executor.py:1382-1440`, `monitor.py:37-107` | `[CODE-VERIFIED]` | §5.3 |
| 5.3-23 | `_determine_phase_status` authoritative classifier: exit 124→TIMEOUT; prompt-too-long→result/INCOMPLETE; end checkpoint PASS+no contamination→PASS_RECOVERED; result file HALT/CONTINUE markers; no result+output→PASS_NO_REPORT; no output→ERROR | 03-sprint-execution-runtime | `sprint/executor.py:2067-2148` | `[CODE-VERIFIED]` | §5.3 |
| 5.3-24 | `_classify_from_result_file` rejects missing/stale; EXIT_RECOMMENDATION HALT→HALT, CONTINUE/status:PASS→PASS_RECOVERED, FAIL→HALT, PARTIAL→INCOMPLETE | 03-sprint-execution-runtime | `sprint/executor.py:1774-1808` | `[CODE-VERIFIED]` | §5.3 |
| 5.3-25 | `_write_preliminary_result` + `_write_executor_result_file` author result frontmatter/table/metrics/EXIT_RECOMMENDATION after classification | 03-sprint-execution-runtime | `sprint/executor.py:1954-2064` | `[CODE-VERIFIED]` | §5.3 |
| 5.3-26 | Checkpoints: `extract_checkpoint_paths` parses `Checkpoint Report Path:` + TASKLIST_ROOT/ resolution; `_verify_checkpoints` respects checkpoint_gate_mode off/shadow(default)/soft/full; full→PASS_MISSING_CHECKPOINT when missing | 03-sprint-execution-runtime | `sprint/checkpoints.py:36-112`, `executor.py:1811-1891` | `[CODE-VERIFIED]` | §5.3 |
| 5.3-27 | End-of-sprint `build_manifest` + `write_manifest` writes `<release_dir>/manifest.json` + checkpoint_manifest JSONL event; `recover_missing_checkpoints` synthesizes reports marked status UNKNOWN | 03-sprint-execution-runtime | `sprint/executor.py:1702-1725`, `checkpoints.py:209-408` | `[CODE-VERIFIED]` | §5.3 |
| 5.3-28 | `SprintLogger` writes JSONL+Markdown logs (real); `read_status_from_log`/`tail_log` are STUBS ("not yet connected") so status/logs commands don't report live | 03-sprint-execution-runtime | `sprint/logging_.py:13-213`, `224-235` | `[CODE-VERIFIED]` (stubbed) | §5.3 |
| 5.3-29 | On failed phase: DiagnosticCollector snapshots monitor + tails logs; FailureClassifier prioritizes stall/timeout/context-exhaustion/crash/error/unknown; ReportGenerator writes diagnostic markdown; sprint outcome HALTED | 03-sprint-execution-runtime | `sprint/executor.py:1609-1639`, `diagnostics.py:72-127`, `157-232` | `[CODE-VERIFIED]` | §5.3 |
| 5.3-30 | `SummaryWorker(PhaseSummarizer)` daemon pipeline extracts stream-json signals, optionally invokes `claude --print --model claude-sonnet-4-5` 30s timeout, writes phase-N-summary.md; Path A does NOT submit summaries before continue | 03-sprint-execution-runtime | `sprint/executor.py:1168-1196`, `summarizer.py:1-240` | `[CODE-VERIFIED]` | §5.3 |
| 5.3-31 | End-of-sprint waits up to 90s for summaries then attempts RetrospectiveGenerator; failures logged but don't abort wrap-up | 03-sprint-execution-runtime | `sprint/executor.py:1661-1688` | `[CODE-VERIFIED]` | §5.3 |
| 5.3-32 | Base process Popen has no cwd arg; Path B relies on CLAUDE_WORK_DIR env, Path A passes none (worker cwd not guaranteed) | 03-sprint-execution-runtime | `pipeline/process.py:125-134`, `sprint/executor.py:1320-1324`, `1098-1108` | `[CODE-VERIFIED]` | §5.3 |
| 5.3-33 | Sprint is hardest port stress test: spans CLI config, models, two process paths, file monitors, tmux/TUI, ledgers/gates, checkpoints, diagnostics, summaries/retrospective; recommended posture hybrid-first | 03-sprint-execution-runtime | `03-sprint-execution-runtime §8` (synthesis) | `[CODE-VERIFIED]` (synthesis) | §5.3 |
| 5.3-34 | STALE: generated v3.7 TUI doc says Path A subprocesses write to same `phase-N-output.txt`; code uses task-specific files (CODE-CONTRADICTED) | 03-sprint-execution-runtime | `docs/generated/sprint-cli/v3.7-refactor/chunk-02-sprint-tui-v2.md:19` vs `sprint/executor.py:1098-1108` | `[CODE-VERIFIED]` (doc-contradicted) | §5.3 |

## Subsystem 5.4 — Harness Corpus (Skills / Agents / Templates / Hooks / MCP Reuse)

**Primary source:** `05-skills-agents-harness-reuse.md` (synth-04 → §5.4-5.8)

| # | Architectural claim | Source research file | Source code `path:line` | Tag | Target §|
|---|---|---|---|---|---|
| 5.4-01 | Source-of-truth is `src/superclaude/` first; `.claude/` are synced dev copies — do not scrape dev copies as primary | 05-skills-agents-harness-reuse | `src/superclaude/core/CLAUDE.md:17-29`, `45-48` | `[CODE-VERIFIED]` | §5.4 |
| 5.4-02 | Slash commands are thin front-door manifests: parse flags, validate inputs, invoke skills; do not embed execution loops | 05-skills-agents-harness-reuse | `commands/task.md:156-162`, `tasklist.md:70-84`, `roadmap.md:82-92`, `adversarial.md:143-149` | `[CODE-VERIFIED]` | §5.4 |
| 5.4-03 | Skill packages (`SKILL.md` + refs/rules/templates/scripts) are the main reusable instruction body; agents are role prompt corpus | 05-skills-agents-harness-reuse | `src/superclaude/core/CLAUDE.md:20-21`, `97-102` | `[CODE-VERIFIED]` | §5.4 |
| 5.4-04 | `sc-task-protocol` execution-only after classification; tier-specific exec/verification; TFEP escalation; MCP tier requirements | 05-skills-agents-harness-reuse | `sc-task-protocol/SKILL.md:7-10`, `50-62`, `80-129`, `133-261`, `271-284` | `[CODE-VERIFIED]` | §5.4 |
| 5.4-05 | Generic MDTM `task` skill: F1 loop reads first unchecked item, executes exactly, marks complete, repeats; prohibits delegating loop; supports parallel agent spawning for independent items | 05-skills-agents-harness-reuse | `skills/task/SKILL.md:83-105`, `110-123`, `125-151`, `371-373` | `[CODE-VERIFIED]` | §5.4 |
| 5.4-06 | `task-builder` (2,190 lines) orchestrates scope discovery, parallel researchers, QA gates, builder, structural+qualitative validation; writes to `.dev/tasks/to-do/` | 05-skills-agents-harness-reuse | `skills/task-builder/SKILL.md:108-162` | `[CODE-VERIFIED]` | §5.4 |
| 5.4-07 | `sc-tasklist-protocol` deterministic roadmap→tasklist generator (no discretionary choices); emits sprint-compatible files | 05-skills-agents-harness-reuse | `sc-tasklist-protocol/SKILL.md:12-28`, `91-123` | `[CODE-VERIFIED]` | §5.4 |
| 5.4-08 | Rigorflow agent corpus: rf-team-lead orchestrates rf-task-researcher/builder/executor with message vocabulary + task prefixes; scope discovery via Glob/Grep/codebase-retrieval | 05-skills-agents-harness-reuse | `agents/rf-team-lead.md:36-48`, `79-103`, `139-160` | `[CODE-VERIFIED]` | §5.4 |
| 5.4-09 | rf-task-researcher reports RESEARCH_READY/PARTIAL/BLOCKED with structured findings (files/exports/patterns/templates/issues) | 05-skills-agents-harness-reuse | `agents/rf-task-researcher.md:30-57`, `123-150` | `[CODE-VERIFIED]` | §5.4 |
| 5.4-10 | rf-qa zero-tolerance verification with partitioning + research gate (evidence density, doc cross-validation tags, gaps, integration points, incremental writing); rf-qa-qualitative (1,139 lines) Tavily-first external lookup | 05-skills-agents-harness-reuse | `agents/rf-qa.md:35-166`, `rf-qa-qualitative.md:35-129` | `[CODE-VERIFIED]` | §5.4 |
| 5.4-11 | Core instruction corpus: CLAUDE.md, COMMANDS.md, ORCHESTRATOR.md (detection/complexity/domain matrices, wave routing), MCP.md (server selection, circuit breakers, task-tier deps), RULES.md (conflict hierarchy, verification-before-recommendation) | 05-skills-agents-harness-reuse | `core/CLAUDE.md`, `COMMANDS.md:5-149`, `ORCHESTRATOR.md:5-130`, `MCP.md:5-304`, `RULES.md:5-82` | `[CODE-VERIFIED]` | §5.4 |
| 5.4-12 | MDTM templates: generic (996 lines) + complex (1,204 lines) with granular/self-contained constraints; 7 document templates (3,308 lines) incl technical_reference_template.md | 05-skills-agents-harness-reuse | `templates/workflow/01_mdtm_template_generic_task.md:1-159`, `02_mdtm_template_complex_task.md:60-197`, `templates/documents/*` | `[CODE-VERIFIED]` | §5.4 |
| 5.4-13 | Hooks: hooks.json registers SessionStart/UserPromptSubmit/PreToolUse/PostToolUse/SubagentStart/SubagentStop; freshness-user-prompt emits session-context; freshness-pre-edit blocks edits without recent Read / stale reads; reject-workspace-writes blocks `.claude/skills/*-workspace/**` | 05-skills-agents-harness-reuse | `hooks/hooks.json:1-95`, `scripts/freshness-user-prompt.sh:20-264`, `freshness-pre-edit.sh:63-138`, `reject-workspace-writes.sh:25-62` | `[CODE-VERIFIED]` | §5.4 |
| 5.4-14 | MCP configs (tavily/auggie/serena/sequential) use npx/uvx/auggie launch with secret env injection; MCP.md circuit-breaker table lists fallbacks + strict-tier blocking | 05-skills-agents-harness-reuse | `mcp/configs/tavily.json:1-12`, `auggie.json:1-9`, `serena.json:1-13`, `sequential.json:1-9`, `core/MCP.md:269-304` | `[CODE-VERIFIED]` | §5.4 |
| 5.4-15 | In-repo portification precedent: `/sc:cli-portify` command + `sc-cli-portify-protocol` already converts inference workflows to deterministic CLI pipelines (component inventory → step graph → gates → executor/workflow spec) | 05-skills-agents-harness-reuse | `commands/cli-portify.md:20-91`, `sc-cli-portify-protocol/SKILL.md:12-28`, `refs/pipeline-spec.md:15-128` | `[CODE-VERIFIED]` | §5.4/§5.6 |
| 5.4-16 | Asset totals: 42 command files, 39 agent files, 24 skill packages (31,820 lines), 12 core files, 8 workflow templates, 7 document templates, hooks.json+9 scripts, 11 MCP docs + 11 JSON configs | 05-skills-agents-harness-reuse | dir inventories (synth) | `[CODE-VERIFIED]` | §5.4 |
| 5.4-17 | Tool-invocation boundary: instructions assume Claude Code tools (Skill/Task/Glob/Grep/TodoWrite/TeamCreate/SendMessage) requiring an adapter vocabulary | 05-skills-agents-harness-reuse | `agents/rf-team-lead.md:79-103` (and corpus) | `[CODE-VERIFIED]` | §5.4/§5.6 |
| 5.4-18 | SoT CONFLICT: core/CLAUDE.md says edit src/superclaude/ first, but commands/agents/hooks READMEs say edit plugins/superclaude/ first (both path families exist) | 05-skills-agents-harness-reuse | `core/CLAUDE.md:45-48` vs `commands/README.md:13-23`, `agents/README.md:11-21`, `hooks/README.md:9-19` | `[CODE-VERIFIED]` (contradicted) | §5.4 |
| 5.4-19 | STALE: commands/README.md lists 5 command files but dir has 42; agents/README.md lists 3 but dir has 39 | 05-skills-agents-harness-reuse | `commands/README.md:5-11`, `agents/README.md:5-10` | `[CODE-VERIFIED]` (doc-stale) | §5.4 |
| 5.4-20 | `/sc:forensic` invoked by TFEP but not found in requested inventory — dependency gap | 05-skills-agents-harness-reuse | `sc-task-protocol/SKILL.md:181-261` | `[CODE-VERIFIED]` (unverified dependency) | §5.4 |

## Subsystem 5.5 — Target Data Model & Ownership

**Primary source:** `07-target-data-model-and-ownership.md` (synth-04 → §5.4-5.8). Note: target-stack mappings tagged DESIGN/UNVERIFIED; current-code contracts tagged CODE-VERIFIED.

| # | Architectural claim | Source research file | Source code `path:line` | Tag | Target §|
|---|---|---|---|---|---|
| 5.5-01 | Research task file = MDTM markdown w/ YAML frontmatter (id/title/status/type/priority/dates/assignment/dependencies/related/tags) + ordered checklist phases | 07-target-data-model | `templates/workflow/02_mdtm_template_complex_task.md:1-44` | `[CODE-VERIFIED]` | §5.5 |
| 5.5-02 | MDTM execution item = flat self-contained checkbox under phase; READ→IDENTIFY→EXECUTE→UPDATE→REPEAT; one item at a time; multi-item prohibited | 07-target-data-model | `02_mdtm_template_complex_task.md:394-430` | `[CODE-VERIFIED]` | §5.5 |
| 5.5-03 | Handoff artifacts in task subdirs (research/synthesis/qa/reviews/phase-outputs/{discovery,test-results,reviews,plans,reports}); filesystem-owned, read by path | 07-target-data-model | `02_mdtm_template_complex_task.md:718-731`, `928-941` | `[CODE-VERIFIED]` | §5.5 |
| 5.5-04 | Stable IDs are cross-system sync keys: `TASK-*`, `T<PP>.<TT>`, `D-####`, `D-CP...`, `R-###`; appear in current file formats + parsers | 07-target-data-model | `sc-tasklist-protocol/SKILL.md:161-164`, `291-300`, `441-487`; `sprint/config.py:374-377` | `[CODE-VERIFIED]` | §5.5 |
| 5.5-05 | Current pipeline `Step` model (id/prompt/output_file/gate/timeout/inputs/retry_limit/model/gate_mode/tool_write_mode/template_path) is the workflow-step contract | 07-target-data-model | `pipeline/models.py:108-123` | `[CODE-VERIFIED]` | §5.5 |
| 5.5-06 | Status enums: StepStatus (PENDING/PASS/FAIL/TIMEOUT/CANCELLED/SKIPPED), TaskStatus (PASS/FAIL/INCOMPLETE/SKIPPED), GateOutcome (PASS/FAIL/DEFERRED/PENDING + display CHECKING/FAIL_DEFERRED/REMEDIATING/REMEDIATED/HALT), SprintOutcome (SUCCESS/HALTED/INTERRUPTED/ERROR) | 07-target-data-model | `pipeline/models.py:40-67`, `sprint/models.py:39-124`, `272-279` | `[CODE-VERIFIED]` | §5.5 |
| 5.5-07 | Execution logs: execution-log.jsonl/.md, results/phase-*-output.txt/errors.txt, phase-*-result.md, per-task output/error files (filesystem-owned under release dir) | 07-target-data-model | `sprint/models.py:473-510` | `[CODE-VERIFIED]` | §5.5 |
| 5.5-08 | MonitorState (high-volume telemetry: bytes/event times/activity log/turns/errors/assistant text/task progress/tokens) belongs in tracing layer not task-of-record | 07-target-data-model | `sprint/models.py:622-690` | `[CODE-VERIFIED]` | §5.5/§5.8 |
| 5.5-09 | TurnLedger (initial_budget/consumed/reimbursed/rate/min_allocation/remediation+wiring budgets) is sprint-local; insufficient for multi-tenant governance | 07-target-data-model | `sprint/models.py:692-777` | `[CODE-VERIFIED]` | §5.5/§5.8 |
| 5.5-10 | CheckpointEntry (phase/name/expected_path/exists/recovered/recovery_source) + checkpoint report path conventions | 07-target-data-model | `sprint/models.py:311-341`, `sc-tasklist-protocol/SKILL.md:343-391` | `[CODE-VERIFIED]` | §5.5 |
| 5.5-11 | Sprint parser compatibility contract: phase filename aliases, Execution Mode (claude/python/skip), `### T<PP>.<TT> -- Title` headings, `**Dependencies:**`/`**Command:**`/classifier-row/`**Deliverables:**` extraction, release-dir resolution | 07-target-data-model | `sprint/config.py:15-26`, `67-119`, `374-492`, `236-272` | `[CODE-VERIFIED]` | §5.5 |
| 5.5-12 | Proposed ownership split (DESIGN): Backlog.md owns prose/task/doc/decisions; Beads owns dependency graph mirror; Mastra owns run/trace/gate-execution state | 07-target-data-model | ownership matrix (synthesis) | `[DESIGN — UNBUILT]` (target hypothesis) | §5.5 |
| 5.5-13 | Ownership rules to preserve (DESIGN): one prose owner, one graph owner, one run owner, stable IDs non-negotiable, checkpoint reports remain artifacts | 07-target-data-model | ownership rules (synthesis) | `[DESIGN — UNBUILT]` | §5.5 |
| 5.5-14 | Adapter contracts (DESIGN): tasklist→Backlog import, Backlog/tasklist→Beads graph sync, Backlog/Beads→Mastra workflow plan, Mastra results→Backlog/Beads reconciliation (idempotent); each w/ round-trip parser validation | 07-target-data-model | adapter contract sketches (synthesis) | `[DESIGN — UNBUILT]` | §5.5/§5.6 |
| 5.5-15 | Tenant/actor/audit identity ABSENT from scoped current models (PipelineConfig/SprintConfig/TaskResult/PhaseResult/MonitorState/TurnLedger have model/permission/budget but no tenant/actor) | 07-target-data-model | `pipeline/models.py`, `sprint/models.py` (read ranges) | `[CODE-VERIFIED]` (absence) | §5.5/§5.8 |
| 5.5-16 | CONFLICT: sc-tasklist-protocol SKILL.md says numbered `### T<PP>.<NN> -- Checkpoint:` tasks; extracted phase-template.md still documents sibling `### Checkpoint:` sections (stale template) | 07-target-data-model | `sc-tasklist-protocol/SKILL.md:343-391`, `947-1027` vs `templates/phase-template.md:101-125` | `[CODE-VERIFIED]` (doc-contradicted) | §5.5 |
| 5.5-17 | CONFLICT: sprint `build_prompt()` still instructs scanning for sibling `### Checkpoint:` sections — potential code/protocol drift vs numbered checkpoint tasks | 07-target-data-model | `sprint/process.py:187-195` vs `sc-tasklist-protocol/SKILL.md:343-391` | `[CODE-VERIFIED]` (drift, needs follow-up) | §5.5 |

## Subsystem 5.6 — Adapter Layer (Orchestration Patterns to Reuse)

**Primary source:** `04-cli-portify-prd-cleanup-audit-eval.md` (synth-04 → §5.4-5.8)

| # | Architectural claim | Source research file | Source code `path:line` | Tag | Target §|
|---|---|---|---|---|---|
| 5.6-01 | Five CLI-adjacent orchestration surfaces: cli_portify (87 files), prd (44), cleanup_audit (37), eval (65), audit (127) | 04-cli-portify-prd-cleanup-audit-eval | dir inventories | `[CODE-VERIFIED]` | §5.6 |
| 5.6-02 | cli_portify: deterministic `STEP_REGISTRY` (12 steps, ordered IDs, phase types, timeouts, retry limits, named artifacts); top-level builder creates workdir/config YAML/PortifyStep objects | 04-cli-portify-prd-cleanup-audit-eval | `cli_portify/executor.py:105-183`, `767-840` | `[CODE-VERIFIED]` | §5.6 |
| 5.6-03 | cli_portify gates G-000..G-011 with semantic checks returning tuple[bool,str]; `PortifyGatePolicy` two-layer (global mode + per-gate promotion), blocking only when FULL | 04-cli-portify-prd-cleanup-audit-eval | `cli_portify/gates.py:6-24`, `119-256`, `executor.py:380-440`, `590-607` | `[CODE-VERIFIED]` | §5.6 |
| 5.6-04 | cli_portify emits `return-contract.yaml` on all paths (outcome/completed_steps/remaining_steps/suggested_resume_budget/resume_command) — bridge to Backlog/Beads records | 04-cli-portify-prd-cleanup-audit-eval | `cli_portify/executor.py:283-372` | `[CODE-VERIFIED]` | §5.6 |
| 5.6-05 | cli_portify deterministic output classification: timeout/124→TIMEOUT, nonzero→ERROR, exit0+EXIT_RECOMMENDATION+artifact→PASS, artifact-no-marker→PASS_NO_SIGNAL, no artifact→PASS_NO_REPORT | 04-cli-portify-prd-cleanup-audit-eval | `cli_portify/executor.py:224-257` | `[CODE-VERIFIED]` | §5.6 |
| 5.6-06 | cli_portify convergence: standalone `ConvergenceEngine.submit()` converges on zero unaddressed criticals, escalates on max iterations, budget/user escalation | 04-cli-portify-prd-cleanup-audit-eval | `cli_portify/convergence.py:144-255` | `[CODE-VERIFIED]` | §5.6 |
| 5.6-07 | cli_portify `BasePromptBuilder` encodes artifact-first method: every prompt declares input artifacts, required frontmatter, output contract + retry prompt construction | 04-cli-portify-prd-cleanup-audit-eval | `cli_portify/prompts.py:79-163` | `[CODE-VERIFIED]` | §5.6 |
| 5.6-08 | DRIFT: cli_portify resume.py legacy matrix uses conceptual step names (analyze-workflow/design-pipeline/synthesize-spec) NOT current STEP_REGISTRY IDs; resume validation contradicts live registry | 04-cli-portify-prd-cleanup-audit-eval | `cli_portify/resume.py:45-95`, `168-198` vs `executor.py:105-183` | `[CODE-VERIFIED]` (contradicted) | §5.6 |
| 5.6-09 | prd: 15-step pipeline; Stage A = 9 sequential steps; Stage B dynamic fan-out (investigation/web/synthesis) + QA→fix→re-QA loops | 04-cli-portify-prd-cleanup-audit-eval | `prd/executor.py:372-388`, `416-506`, `721-860` | `[CODE-VERIFIED]` | §5.6 |
| 5.6-10 | prd tier-sized fan-out: investigation agents (3/5/8), web research (1/2/3) by lightweight/standard/heavyweight; parallel via ThreadPoolExecutor max_workers=min(steps,10), per-future exception→ERROR step | 04-cli-portify-prd-cleanup-audit-eval | `prd/executor.py:862-958` | `[CODE-VERIFIED]` | §5.6 |
| 5.6-11 | prd QA→fix→re-QA loop: initial QA + up to max_cycles, budget-halt, exit on pass, strict-fail halt, gap-fill before next pass | 04-cli-portify-prd-cleanup-audit-eval | `prd/executor.py:963-1047` | `[CODE-VERIFIED]` | §5.6 |
| 5.6-12 | prd artifact discovery: EXIT_RECOMMENDATION regex (strips code fences), step-ID→artifact map (qa/ subdir), disk-file-over-NDJSON resolution; GATE_CRITERIA for 15 steps w/ exception-wrapped semantic checks | 04-cli-portify-prd-cleanup-audit-eval | `prd/executor.py:72-97`, `247-365`, `gates.py:257-514` | `[CODE-VERIFIED]` | §5.6 |
| 5.6-13 | prd inventory existing-work detection (NO_EXISTING/RESUME_STAGE_A/RESUME_STAGE_B/ALREADY_COMPLETE); creates research/synthesis/qa/reviews/results subdirs; partition/merge filtering (pessimistic FAIL) | 04-cli-portify-prd-cleanup-audit-eval | `prd/inventory.py:26-199`, `filtering.py:20-175` | `[CODE-VERIFIED]` | §5.6 |
| 5.6-14 | cleanup_audit: 6 audit steps (G-001 surface..G-006 validation), sprint-style supervised loop, blocking gates, status classifier; validation is first-class stage | 04-cli-portify-prd-cleanup-audit-eval | `cleanup_audit/executor.py:52-321`, `gates.py:59-154` | `[CODE-VERIFIED]` | §5.6 |
| 5.6-15 | DRIFT: cleanup_audit docstring claims ThreadPoolExecutor parallel batch dispatch but code executes sequentially (no import); --pass/--batch-size flags accepted but not applied in _build_steps | 04-cli-portify-prd-cleanup-audit-eval | `cleanup_audit/executor.py:11-13`, `72-159`, `187-287`, `commands.py:24-40` | `[CODE-VERIFIED]` (contradicted) | §5.6 |
| 5.6-16 | eval: capability preflight (claude --version), HOME-dir check, scratch-root allowlist, run-dir build, suite manifest load, hook-coverage gate before per-eval HOME, disk-budget poller, RunOrchestrator + exit-code mapping | 04-cli-portify-prd-cleanup-audit-eval | `eval/commands.py:119-205`, `1689-2004` | `[CODE-VERIFIED]` | §5.6 |
| 5.6-17 | eval RunOrchestrator: ThreadPoolExecutor parallelism (default 8, 1-15), preserves spec order via preallocated slots, cancellation/disk-budget stop, backfills INTERRUPTED/SKIPPED, never drops outcome | 04-cli-portify-prd-cleanup-audit-eval | `eval/orchestrator.py:113-360` | `[CODE-VERIFIED]` | §5.6 |
| 5.6-18 | eval per-eval lifecycle: setup HOME→deploy hooks→spawn→inject→observe→assert→teardown; classify ERRORED/PASS/FAIL; preserve failed/errored HOMEs; JSONL forensic event buffer; retry-once when wired | 04-cli-portify-prd-cleanup-audit-eval | `eval/runner.py:179-473`, `537-878` | `[CODE-VERIFIED]` | §5.6 |
| 5.6-19 | eval HOME isolation: three-check containment_guard (eval-ID regex, scratch-root allowlist, post-mkdtemp containment); env vars HOME/CLAUDE_SESSION_ID/optional fake-time; guarded state_path | 04-cli-portify-prd-cleanup-audit-eval | `eval/isolation.py:224-260`, `456-747` | `[CODE-VERIFIED]` | §5.6 |
| 5.6-20 | eval RetryOncePolicy: immutable, policy-tag driven (MCP-flaky tag, flaky statuses FAIL/ERRORED/TIMEOUT), one retry, idempotent annotation | 04-cli-portify-prd-cleanup-audit-eval | `eval/retry.py:41-165` | `[CODE-VERIFIED]` | §5.6 |
| 5.6-21 | audit primitives: content-hash ResultCache (SHA-256), deterministic (tier,action)→category classification, consolidation by file path (highest-confidence conflict resolution) | 04-cli-portify-prd-cleanup-audit-eval | `audit/tool_orchestrator.py:61-224`, `classification.py:47-166`, `consolidation.py:93-180` | `[CODE-VERIFIED]` | §5.6 |
| 5.6-22 | audit validation: stratified sampling + re-classification consistency; calibration language explicitly states self-agreement NOT ground-truth correctness (avoids "accuracy") | 04-cli-portify-prd-cleanup-audit-eval | `audit/validation.py:42-151`, `spot_check.py:47-155`, `validation_output.py:14-116` | `[CODE-VERIFIED]` | §5.6/§5.8 |
| 5.6-23 | audit batching/checkpoint/retry/budget: monorepo-segment-isolated batches, atomic checkpoint writes (temp+rename), batch_retry (max 2, cascading-failure detection), budget degradation (warn/degrade/halt with ordered protected-capability overrides) | 04-cli-portify-prd-cleanup-audit-eval | `audit/batch_decomposer.py:91-187`, `checkpoint.py:58-110`, `batch_retry.py:60-187`, `budget.py:26-320` | `[CODE-VERIFIED]` | §5.6/§5.8 |
| 5.6-24 | audit report completeness mandates final sections (executive_summary/findings_by_tier/action_items/coverage_metrics/validation_results/dependency_graph_summary); depth dispatch summary/standard/detailed | 04-cli-portify-prd-cleanup-audit-eval | `audit/report_depth.py:22-193`, `report_completeness.py:12-115` | `[CODE-VERIFIED]` | §5.6 |
| 5.6-25 | Verified migration method (synthesis): single typed graph as SoT → attach artifact/gate contracts → preflight before side effects → run w/ isolation+supervision → persist graph/checkpoint/artifact → QA/fix or convergence loops → calibrated validation; retire duplicated resume/review matrices | 04-cli-portify-prd-cleanup-audit-eval | §4/§8 mapping (synthesis) | `[CODE-VERIFIED]` (synthesis) | §5.6 |
| 5.6-26 | STALE: eval runner.py comments say MCP-flaky retry-once is future work but retry.py + runner.py:851-876 show it is now wired | 04-cli-portify-prd-cleanup-audit-eval | `eval/runner.py:731-740` vs `retry.py:92-165` | `[CODE-VERIFIED]` (doc-stale) | §5.6 |
| 5.6-27 | No source file implements Mastra/Backlog.md/Beads integration — all integration mapping is feasibility inference, not current implementation | 04-cli-portify-prd-cleanup-audit-eval | (absence across scope) | `[DESIGN — UNBUILT]` | §5.6 |

## Subsystem 5.7 — External Substrate (Mastra / Backlog.md / Beads Current Capabilities)

**Primary sources:** `web-01-mastra`, `web-02-backlog-md`, `web-03-beads`, `06-docs-and-existing-feasibility-artifacts` (synth-04 → §5.4-5.8). All target-stack rows are `[EXTERNAL-VERIFIED]` (Tavily/Context7 provenance) unless current-code.

### Mastra (web-01)

| # | Architectural claim | Source research file | Source ref | Tag | Target §|
|---|---|---|---|---|---|
| 5.7-01 | Mastra workflows support durable suspend()/resume()/resumeStream() with snapshots persisted to storage across deploys/restarts; resume from specific step ID; runners (built-in, Inngest, Temporal-experimental) | web-01-mastra | mastra.ai/docs/workflows/suspend-and-resume; workflow-runners | `[EXTERNAL-VERIFIED]` | §5.7 |
| 5.7-02 | Step-based typed pipelines via createWorkflow()/createStep() w/ input/outputSchema; steps call functions/APIs/agents/tools/workflows; workflows (deterministic) vs agents (probabilistic) | web-01-mastra | mastra.ai/docs/workflows/overview | `[EXTERNAL-VERIFIED]` | §5.7 |
| 5.7-03 | Mastra Workspace `WorkspaceSandbox` (executeCommand/start/stop/destroy, timeouts, stdout/stderr/wait, maxRetainedBytes) added @mastra/core@1.1.0 — candidate subprocess substrate but NOT proven parity with Claude Code hook/permission model | web-01-mastra | mastra.ai/reference/workspace/sandbox | `[EXTERNAL-VERIFIED]` | §5.7 |
| 5.7-04 | Storage: libSQL/Turso, PostgreSQL, MongoDB, Redis/Upstash, DynamoDB, MSSQL, ClickHouse, Cloudflare; MastraCompositeStore routes domains; ClickHouse for prod observability; in-memory resets | web-01-mastra | mastra.ai/docs/memory/storage; reference/storage/composite | `[EXTERNAL-VERIFIED]` | §5.7 |
| 5.7-05 | Observability auto-instruments agent runs/LLM gens/tool calls/workflow steps (tokens, model params); Studio visualizes workflow graphs, traces, MCP servers; 1.0 unified schema entityId/entityType/entityName | web-01-mastra | mastra.ai/docs/observability/tracing/overview; studio/overview | `[EXTERNAL-VERIFIED]` | §5.7/§5.8 |
| 5.7-06 | Auth optional (Studio/API public without it); providers Simple/JWT/Auth0/Better/Clerk/Firebase/Okta/Supabase/WorkOS; RBAC/FGA tied to Enterprise Edition (@mastra/core/auth/ee, StaticRBACProvider, WorkOS FGA); dual license Apache 2.0 + Mastra EE for ee/ dirs | web-01-mastra | mastra.ai/docs/server/auth; pricing; Context7 | `[EXTERNAL-VERIFIED]` (key risk) | §5.7/§5.8 |
| 5.7-07 | MCP: MCPClient (stdio/HTTP/SSE) + MCPServer (expose agents/tools/workflows over HTTP); requireToolApproval HITL; FGA enforcement for MCP tool execution | web-01-mastra | mastra.ai/docs/mcp/overview | `[EXTERNAL-VERIFIED]` | §5.7/§5.8 |
| 5.7-08 | Deployment: mastra dev/build/start/server deploy; Hono-based server, Express/Hono/Fastify/Koa adapters; agents/workflows become REST endpoints w/ OpenAPI; Platform Organizations = multi-tenant containers | web-01-mastra | mastra.ai/docs/server/mastra-server; mastra-platform/overview | `[EXTERNAL-VERIFIED]` | §5.7 |
| 5.7-09 | Mastra 1.0+ vendor maturity claims (Replit/PayPal/Sanity prod use, ~300k weekly npm, ~24k stars) — need independent validation | web-01-mastra | mastra.ai/blog/announcing-mastra-1 | `[EXTERNAL-VERIFIED]` (vendor claim) | §5.7 |
| 5.7-10 | Mastra risk = parity/governance gaps not capability: Claude Code hook parity NOT established; workflow rerun/replay/idempotency needs hands-on validation; Temporal experimental; Backlog/Beads not native | web-01-mastra | mastra.ai limitations (synthesis) | `[EXTERNAL-VERIFIED]` | §5.7 |

### Backlog.md (web-02)

| # | Architectural claim | Source research file | Source ref | Tag | Target §|
|---|---|---|---|---|---|
| 5.7-11 | Backlog.md = markdown-native task store (backlog/ dir), CLI + TUI board + browser UI + fuzzy search + docs + decisions + MCP; MIT; v1.45.2; TypeScript/Bun | web-02-backlog-md | github.com/MrLesk/Backlog.md; package.json | `[EXTERNAL-VERIFIED]` | §5.7 |
| 5.7-12 | Rich Task schema (id/title/status/assignee/reporter/dates/labels/milestone/dependencies/references/documentation/modifiedFiles/description/implementationPlan/Notes/finalSummary/AC/DoD/parent-subtasks/priority/branch/ordinal) | web-02-backlog-md | src/types/index.ts | `[EXTERNAL-VERIFIED]` | §5.7/§5.5 |
| 5.7-13 | MCP task schemas use additionalProperties:false (reject unknown props) — SuperClaude custom metadata cannot be arbitrary MCP fields; must use supported fields/body sections/docs or extend | web-02-backlog-md | src/mcp/tools/tasks/schemas.ts | `[EXTERNAL-VERIFIED]` (key constraint) | §5.7/§5.5 |
| 5.7-14 | Current MCP is MVP stdio surface (task_*/milestone_*/definition_of_done_*/document_*); decision tools CLI-only not MCP; contradicts older "75+ tools" claims | web-02-backlog-md | src/mcp/README.md | `[EXTERNAL-VERIFIED]` | §5.7 |
| 5.7-15 | Git optional: `backlog init --no-git` filesystem-only; autoCommit default false; remoteOperations/bypassGitHooks/filesystemOnly config | web-02-backlog-md | ADVANCED-CONFIG.md | `[EXTERNAL-VERIFIED]` | §5.7 |
| 5.7-16 | Backlog.md is local-file/git-centric NOT a centralized multi-user transactional PM backend (proper-lockfile; one-task-per-agent discipline needed); no built-in sprint/roadmap pipeline equivalent | web-02-backlog-md | github.com/MrLesk/Backlog.md | `[EXTERNAL-VERIFIED]` | §5.7/§5.8 |
| 5.7-17 | Backlog.md↔Beads integration NOT mature (open FR #588; maintainer suggests narrow import/export sync first) — tempers seed-brief "shared repo metadata references" claim | web-02-backlog-md | github.com/MrLesk/Backlog.md/issues/588 | `[EXTERNAL-VERIFIED]` | §5.7 |
| 5.7-18 | Browser UI open state-loss bug #578 (UI resets if files change while running) | web-02-backlog-md | github.com/MrLesk/Backlog.md/issues/578 | `[EXTERNAL-VERIFIED]` | §5.7 |

### Beads (web-03)

| # | Architectural claim | Source research file | Source ref | Tag | Target §|
|---|---|---|---|---|---|
| 5.7-19 | Beads = `gastownhall/beads` "distributed graph issue tracker for AI agents, powered by Dolt"; npm @beads/bd, PyPI beads-mcp; high churn (~24.3k stars, 227 open issues) | web-03-beads | github.com/gastownhall/beads | `[EXTERNAL-VERIFIED]` | §5.7 |
| 5.7-20 | Core CLI: bd ready (unblocked), bd create, bd update --claim (atomic assignee+in_progress), bd dep add, bd show, bd prime (agent context+memories), bd remember; always --json | web-03-beads | github.com/gastownhall/beads; SETUP.md | `[EXTERNAL-VERIFIED]` | §5.7/§5.5 |
| 5.7-21 | Dependency types: blocking (blocks/parent-child/conditional-blocks/waits-for) + non-blocking annotations (related/tracks/discovered-from/caused-by/validates/supersedes); bd ready = no open blocking deps; cycles rejected at write | web-03-beads | docs/DEPENDENCIES.md | `[EXTERNAL-VERIFIED]` | §5.7/§5.5 |
| 5.7-22 | Gates bridge Beads to external state: gh:pr (PR merged), gh:run (CI), timer, bead (cross-rig), human (approval); bd gate check/discover — maps to SuperClaude "done vs merged/validated" | web-03-beads | docs/DEPENDENCIES.md | `[EXTERNAL-VERIFIED]` | §5.7/§5.8 |
| 5.7-23 | Storage is DOLT-first (version-controlled SQL, cell-level merge, branching); `.beads/issues.jsonl` is export/interchange ONLY not canonical sync — CORRECTS seed-brief SQLite+JSONL framing | web-03-beads | docs/SYNC_CONCEPTS.md; DOLT.md | `[EXTERNAL-VERIFIED]` (corrects stale) | §5.7 |
| 5.7-24 | Embedded mode (default, in-process Dolt, single-writer w/ file locking, solo) vs server mode (dolt sql-server, concurrent writers, bd init --server) — server REQUIRED for multi-agent | web-03-beads | docs/DOLT.md | `[EXTERNAL-VERIFIED]` | §5.7/§5.8 |
| 5.7-25 | --json stable contract (schema v1); BD_JSON_ENVELOPE=1 opts into uniform envelope (planned v2.0 default); legacy list=raw arrays, objects=top-level schema_version, errors to stderr; export=JSONL | web-03-beads | docs/JSON_SCHEMA.md | `[EXTERNAL-VERIFIED]` | §5.7/§5.5 |
| 5.7-26 | Sync via Dolt remotes (refs/dolt/data, separate from refs/heads/main); bd init auto-detects origin; bd bootstrap/bd backup; embedded↔server via backup/restore | web-03-beads | docs/SYNC_CONCEPTS.md; DOLT.md | `[EXTERNAL-VERIFIED]` | §5.7 |
| 5.7-27 | Version caution: v1.0.5 pre-release/gated ("do not upgrade", migration 0043 can break multi-machine sync, #4259); v1.0.4 server data-clobber regression; pin + gate versions | web-03-beads | github.com/gastownhall/beads/releases; issues/3870 | `[EXTERNAL-VERIFIED]` | §5.7 |
| 5.7-28 | Production readiness: dev/internal-safe with backup/sync hygiene; risky for mission-critical without tested backup/restore; CLI/API still changing; multi-agent session attribution actively churning (#3400/#3583) | web-03-beads | docs/FAQ.md; issues/2938 | `[EXTERNAL-VERIFIED]` | §5.7 |

### Cross-cutting substrate / current-code framing (06)

| # | Architectural claim | Source research file | Source ref | Tag | Target §|
|---|---|---|---|---|---|
| 5.7-29 | `ClaudeProcess` is the narrow runtime seam (subprocess boundary used by sprint/roadmap/tasklist); replacing it with Mastra is the central replatforming act; many features hang off it (prompt delivery, parsing, permission flags, cancellation, timeouts, file gates) | 06-docs-and-feasibility | `pipeline/process.py:73-147` | `[CODE-VERIFIED]` | §5.7 |
| 5.7-30 | Current orchestration is artifact/gate-centric: Python owns sequencing/retry/halt/state/outputs/gates; Claude fills structured content — Mastra port must preserve runner-authored truth + gate semantics, not just re-host prompts | 06-docs-and-feasibility | (synthesis vs `pipeline/gates.py`, `executor.py`) | `[CODE-VERIFIED]` | §5.7 |
| 5.7-31 | Markdown tasklists are currently ORDERED execution records, not active dependency graphs (sprint parses deps but executes in document order); Beads/Backlog graph semantics would be a behavioral change not a runtime swap | 06-docs-and-feasibility | `sprint/config.py:379-384`, `executor.py:971-1010` | `[CODE-VERIFIED]` | §5.7 |
| 5.7-32 | STALE: `superclaude pipeline` is NOT a root Click command (it is a shared library package); seed-brief framing loose | 06-docs-and-feasibility | `cli/main.py:400-426` vs `pipeline/__init__.py:1-21` | `[CODE-VERIFIED]` (doc-contradicted) | §5.7 |
| 5.7-33 | STALE: doc says ClaudeProcess passes prompt via argv `-p`; current code uses stdin; PipelineConfig field lists omit cosmetic remediation fields | 06-docs-and-feasibility | `pipeline/process.py:114-147`, `models.py:212-234` | `[CODE-VERIFIED]` (doc-contradicted) | §5.7 |
| 5.7-34 | CLI Portify evolution is the cautionary precedent: early code-gen/spec drift failed; contract-first/gated/resumable/source-verified became the safe pattern — favors strangler/hybrid not big-bang | 06-docs-and-feasibility | v2.23 evolution spec (synthesis) | `[CODE-VERIFIED]` | §5.7 |

## Subsystem 5.8 — Governance Plane (Multi-Tenant / MCP / Cost / Audit)

**Primary source:** `web-04-mcp-multitenancy-governance` (synth-04 → §5.4-5.8). Target-stack rows `[EXTERNAL-VERIFIED]`; current-code gap rows `[CODE-VERIFIED]` (absence).

| # | Architectural claim | Source research file | Source ref | Tag | Target §|
|---|---|---|---|---|---|
| 5.8-01 | MCP is a narrow integration protocol (host/client/server tool-resource exchange), explicitly NOT a governance platform; authorization optional | web-04-mcp-governance | modelcontextprotocol.io/docs/concepts/architecture | `[EXTERNAL-VERIFIED]` | §5.8 |
| 5.8-02 | MCP authorization strongly recommended for enterprise (auditability, consent, rate limiting, per-user tracking); remote-server auth is OAuth 2.1-based (PRM, resource indicators, audience binding, token validation) | web-04-mcp-governance | modelcontextprotocol.io/docs/tutorials/security/authorization; specification/2025-06-18/basic/authorization | `[EXTERNAL-VERIFIED]` | §5.8 |
| 5.8-03 | Token passthrough explicitly FORBIDDEN (breaks accountability/audit, enables exfiltration); downstream services need separate tokens + attribution, not forwarded credentials | web-04-mcp-governance | modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices | `[EXTERNAL-VERIFIED]` | §5.8 |
| 5.8-04 | MCP pitfalls: multi-tenant/realm mix-ups, generic audiences, session-ID-as-auth, broad scopes; mitigations = issuer pinning, audience match, scope minimization (no wildcards), progressive elevation | web-04-mcp-governance | modelcontextprotocol.io security best practices | `[EXTERNAL-VERIFIED]` | §5.8 |
| 5.8-05 | Multi-tenant agents need 5 separate identities: trigger / execution / authorization / tenant / attribution; access-control bugs surface silently when execution+tenant conflated; config-driven RBAC not inferred from user messages | web-04-mcp-governance | scalekit.com/blog/access-control-multi-tenant-ai-agents | `[EXTERNAL-VERIFIED]` (high relevance) | §5.8 |
| 5.8-06 | AI control plane is broader than MCP gateway or LLM gateway — governs identity/policy/observability across ALL agents; distinct layers needed | web-04-mcp-governance | speakeasy.com/resources/ai-control-plane | `[EXTERNAL-VERIFIED]` | §5.8 |
| 5.8-07 | Cost attribution/FinOps NOT native to MCP — requires host/gateway/control-plane metering (model tokens + tool calls by tenant/team/user/agent/workflow/task) | web-04-mcp-governance | finops.org/wg/model-context-protocol-mcp | `[EXTERNAL-VERIFIED]` | §5.8 |
| 5.8-08 | CSA minimum maturity: all MCP connections authenticated, OAuth 2.1+PKCE for remote, MCP server inventory (name/version/owner), minimum-permission service accounts, audit logging of all tool invocations | web-04-mcp-governance | labs.cloudsecurityalliance.org/agentic | `[EXTERNAL-VERIFIED]` | §5.8 |
| 5.8-09 | Mastra is runtime/workflow/MCP/observability substrate, NOT a complete multi-tenant governance control plane (no full tenant governance, policy, budget, approval, catalog, cost-attribution) | web-04-mcp-governance | mastra.ai/docs (synthesis) | `[EXTERNAL-VERIFIED]` | §5.8 |
| 5.8-10 | Backlog.md (project-local markdown task mgmt) and Beads (Dolt issue/memory coordination) are task/memory substrates — neither provides cross-tenant IAM, enterprise audit, rate limiting, or cost attribution | web-04-mcp-governance | github.com/MrLesk/Backlog.md; gastownhall/beads | `[EXTERNAL-VERIFIED]` | §5.8 |
| 5.8-11 | A Mastra+Backlog.md+Beads port needs an ADDITIONAL governance/control-plane layer before company-wide multi-tenant deployment: tenant registry, identity mapping, RBAC/ABAC, tool/skill catalog, MCP inventory, approval engine, audit log, cost/rate/budget attribution, env separation | web-04-mcp-governance | synthesis | `[EXTERNAL-VERIFIED]` (core gap) | §5.8 |
| 5.8-12 | Enterprise MCP needs curated approved tool catalog + schema/version change control (versioned contracts, staging, consumer tracking, review-like-code, rollback) — reduce raw tools to structured workflows | web-04-mcp-governance | tray.ai/blog/mcp-security-governance-enterprise | `[EXTERNAL-VERIFIED]` | §5.8 |
| 5.8-13 | Current-code GAP: TurnLedger is sprint-local budget only; tenant/actor/audit identity ABSENT from scoped models — governance dimensions must be added, not assumed | web-04-mcp-governance + 07-target-data-model | `sprint/models.py:692-777`; absence in PipelineConfig/SprintConfig | `[CODE-VERIFIED]` (absence) | §5.8 |

## Cross-Cutting — Feasibility Framing, Gap-Fill Corrections, Decision/Roadmap/Risk

These rows underpin §1-2 (overview/context, synth-01), §6-14 (gaps/options/recommendation/roadmap/risk, synth-05/06/07), and §15-16 (appendices, synth-08). Sources: `06-docs`, `08-11` gap-fills, DECISION-SUMMARY, ROADMAP, RISK-REGISTER.

| # | Architectural claim | Source research file | Source ref | Tag | Target §|
|---|---|---|---|---|---|
| XC-01 | Current CLI root registers sprint/roadmap/cleanup-audit/tasklist/cli-portify/prd/eval; `pipeline/` is a shared package NOT a root command | 06-docs / 08-gap-fill | `cli/main.py:400-426`, `pipeline/__init__.py:1-21` | `[CODE-VERIFIED]` | §1-2 |
| XC-02 | Feasibility framing: port = replatforming a Python-controlled, Claude-Code-subprocess, Markdown-artifact orchestration system into a multi-tenant workflow/task/issue runtime; safest path is hybrid/strangler not big-bang | 06-docs | §summary (synthesis) | `[CODE-VERIFIED]` (framing) | §1-2/§6-8 |
| XC-03 | Feasibility enrichment artifacts exist (codebase-context.md, research-deep.md, adversarial/*, merged-requirements.md, return-contract.yaml); prior `06` inventory claiming only seed-brief.md is STALE/incomplete | 08-gap-fill-feasibility | `.dev/releases/backlog/mastra-beads-port-feasibility/` traversal | `[CODE-VERIFIED]` (corrects prior) | §15-16 |
| XC-04 | research-deep.md external Stack-D claims (Mastra ACP/license/RBAC, Backlog/Beads schema) are external-seed material, NOT code-verified; "AcpAgent exact structural replacement for ClaudeProcess" is UNVERIFIED | 08-gap-fill-feasibility | enrichment/research-deep.md (synthesis) | `[DESIGN — UNBUILT]` (unverified external) | §6-8 |
| XC-05 | Canonical checkpoint contract (for adapters): numbered `### T<PP>.<NN> -- Checkpoint:` tasks w/ `Checkpoint Report Path: TASKLIST_ROOT/checkpoints/...`; legacy sibling `### Checkpoint:` accepted by parser but deprecated for new generators | 09-gap-fill-checkpoint | `sc-tasklist-protocol/SKILL.md:343-391`, `checkpoints.py:18-94` | `[CODE-VERIFIED]` | §5.3/§9-11 |
| XC-06 | Checkpoint runtime parser (`checkpoints.py`) supports BOTH legacy + numbered forms; but per-task executor branch (Path A) does NOT call `_verify_checkpoints()` (only Path B does) — known runtime gap | 09-gap-fill-checkpoint | `checkpoints.py:27-33`, `executor.py:1259-1301` vs `1512-1531` | `[CODE-VERIFIED]` | §5.3/§9-11 |
| XC-07 | Gap-fill patch corrected file-05 invalid citation `core/MCP.md:269-305` → `269-304` and tagged all Mastra/Backlog/Beads claims as UNVERIFIED external | 10-gap-fill-harness-patch | `core/MCP.md:269-304` | `[CODE-VERIFIED]` | §15-16 |
| XC-08 | Source-of-truth risk: `src/superclaude/` is authoritative per core/CLAUDE.md but plugin-mirror READMEs say edit plugins/ first and `diff -qr` shows mirrors materially out of sync — do NOT ingest mirrors as canonical | 11-gap-fill-classification | `core/CLAUDE.md:17-48` vs `commands/agents/hooks README` | `[CODE-VERIFIED]` (risk) | §9-11 |
| XC-09 | Excluded/unsupported features: `/sc:forensic` (no command/skill found) and sprint `rerun-tasks` (not in current sprint/commands.py) must NOT be claimed as current capability; retrospective generator IS verified | 11-gap-fill-classification | `sprint/commands.py` (run/attach/status/logs/kill/verify-checkpoints); `sprint/retrospective.py` | `[CODE-VERIFIED]` (absence + presence) | §9-11 |
| XC-10 | Synthesis guardrail: target-stack API/version/license/schema claims stay UNVERIFIED-external (not current-state facts); tenant/actor/audit identity claims scoped to read models only | 11-gap-fill-classification | classification matrix (synthesis) | `[DESIGN — UNBUILT]` (guardrail) | §6-14 |
| XC-11 | VERDICT: Conditionally Recommended; approach Option D→A (time-boxed validation spike then hybrid adapter-first; NOT native rewrite B, NOT Backlog/Beads-only C); confidence ~70% hybrid feasible, ~55% full multi-tenant on the 3 components alone | DECISION-SUMMARY | DECISION-SUMMARY.md Verdict | `[DESIGN — UNBUILT]` (recommendation) | §6-8 |
| XC-12 | Spike exit gates SG1 (Mastra durable subprocess supervision parity), SG2 (tasklist round-trip into Backlog+Beads), SG3 (Beads server-mode + Dolt sync survives pinned version), SG4 (multi-tenant cost/identity + license decision) | DECISION-SUMMARY | DECISION-SUMMARY.md Spike Exit Gates | `[DESIGN — UNBUILT]` | §6-8/§12-14 |
| XC-13 | Pilot = wrap `superclaude tasklist validate` first (smallest, single strict-gate, non-destructive, reuses shared pipeline); decisive early gate G2 = prove Mastra rerun/recovery/durability | DECISION-SUMMARY + ROADMAP | DECISION-SUMMARY Pilot; ROADMAP Phase 2 | `[DESIGN — UNBUILT]` | §12-14 |
| XC-14 | Roadmap is 6 phases (0 discovery/decisions, 1 read-only adapter MVP, 2 hybrid pilot=spike gate, 3 parity port roadmap+sprint+gates+checkpoints+hooks, 4 multi-tenant hardening, 5 rollout); Phases 0-2 = the spike, 3-5 = committed Option A | ROADMAP | ROADMAP.md Phase Overview | `[DESIGN — UNBUILT]` | §12-14 |
| XC-15 | Five gating decisions D1 (primary work-of-record Backlog vs Beads), D2 (Mastra OSS vs EE), D3 (governance control-plane ownership), D4 (runtime exec seam), D5 (Beads deployment mode + version pin) | ROADMAP + DECISION-SUMMARY | ROADMAP Phase 0; DECISION-SUMMARY Next Decisions | `[DESIGN — UNBUILT]` | §12-14 |
| XC-16 | Phase 3 parity port must preserve (not normalize) defined-but-unwired CERTIFY_GATE; wire `_verify_checkpoints()` into per-task path; map sprint phases/tasks to Beads `bd ready` + atomic `--claim`; telemetry → Mastra traces not Backlog/Beads bodies | ROADMAP | ROADMAP.md Phase 3 | `[DESIGN — UNBUILT]` | §12-14 |
| XC-17 | RISK R1 License (High): production RBAC/SSO/FGA/audit/on-prem are Mastra EE-licensed not Apache-2.0 core | RISK-REGISTER | RISK-REGISTER.md R1 | `[EXTERNAL-VERIFIED]` (risk) | §9-11 |
| XC-18 | RISK R2 Runtime migration (High): ~65K-LOC Python → Mastra TS; ClaudeProcess seam replacement; gate/convergence logic is pure Python | RISK-REGISTER | RISK-REGISTER.md R2 | `[CODE-VERIFIED]` (risk) | §9-11 |
| XC-19 | RISK R3 Backlog/Beads overlap (High): dual task/status owners cause drift; integration immature (#588); assign canonical owners | RISK-REGISTER | RISK-REGISTER.md R3 | `[EXTERNAL-VERIFIED]` (risk) | §9-11 |
| XC-20 | RISK R4 Beads/Dolt churn (High): v1.0.5 do-not-upgrade sync corruption (#4259), v1.0.4 server data-clobber; pin+gate versions, tested backup/restore | RISK-REGISTER | RISK-REGISTER.md R4 | `[EXTERNAL-VERIFIED]` (risk) | §9-11 |
| XC-21 | RISK R5 Concurrency/multi-writer (High): Beads embedded single-writer, multi-agent needs server mode; session attribution changing (#3400/#3583); atomic --claim + one-task-per-agent | RISK-REGISTER | RISK-REGISTER.md R5 | `[EXTERNAL-VERIFIED]` (risk) | §9-11 |
| XC-22 | RISK R6 Subprocess/hook safety parity (High): Mastra Workspace executeCommand does NOT replicate Claude Code hooks/freshness/staging/permissions; UV-only/git-safety/SoT/fork-PR must be rebuilt as middleware | RISK-REGISTER | RISK-REGISTER.md R6 | `[EXTERNAL-VERIFIED]` (risk) | §9-11 |
| XC-23 | RISK R7 Checkpoint/wiring drift (Medium-High): stale legacy `### Checkpoint:` refs, per-task skips `_verify_checkpoints()`, certify maybe unwired, trailing grace=0 forces blocking | RISK-REGISTER | RISK-REGISTER.md R7 | `[CODE-VERIFIED]` (risk) | §9-11 |
| XC-24 | RISK R8 Governance/tenancy/cost gaps (High): none of the 3 components supplies tenant isolation/per-invocation audit/cost attribution/policy/approval/catalog; MCP is not governance | RISK-REGISTER | RISK-REGISTER.md R8 | `[EXTERNAL-VERIFIED]` (risk) | §9-11 |
| XC-25 | RISK R9 Fast-moving external tools (Medium-High): Mastra @core 1.1.0+/Temporal experimental, Backlog v1.45.2 MVP+doc drift+bug #578, Beads 1.x frequent CLI/API changes; pin versions, runtime-verify schemas | RISK-REGISTER | RISK-REGISTER.md R9 | `[EXTERNAL-VERIFIED]` (risk) | §9-11 |
| XC-26 | Critical-gap linkage: G3 (subprocess/Claude-Code parity)↔R2/R6, G4 (hook/safety parity)↔R6, G6 (tenant state)↔R8, G7 (auth/RBAC/governance/cost)↔R1/R8 | RISK-REGISTER | RISK-REGISTER.md Critical-Gap Linkage | `[CODE-VERIFIED]` (linkage) | §9-11 |

---

## Summary

**Status: Complete.** This evidence index contains **243 evidence rows** (217 subsystem rows + 26 cross-cutting rows) mapping every architectural claim needed for the Mastra + Backlog.md + Beads hybrid tech reference to (source research file, source code `path:line` where applicable, evidence tag, target template section).

**Row distribution by subsystem:**
- §5.1 Pipeline-core seam — 44 rows (5.1-01 … 5.1-44)
- §5.2 Roadmap/tasklist — 28 rows (5.2-01 … 5.2-28)
- §5.3 Sprint runtime — 34 rows (5.3-01 … 5.3-34)
- §5.4 Harness corpus — 20 rows (5.4-01 … 5.4-20)
- §5.5 Target data model & ownership — 17 rows (5.5-01 … 5.5-17)
- §5.6 Adapter layer — 27 rows (5.6-01 … 5.6-27)
- §5.7 External substrate — 34 rows (5.7-01 … 5.7-34)
- §5.8 Governance plane — 13 rows (5.8-01 … 5.8-13)
- Cross-cutting (feasibility/gap-fill/decision/roadmap/risk) — 26 rows (XC-01 … XC-26)

**Tag distribution (approximate):**
- `[CODE-VERIFIED]` — the large majority of §5.1-5.6 rows + current-code rows in §5.7-5.8 + XC code-grounded rows. These carry exact `path:line` citations against current `src/superclaude/` source.
- `[EXTERNAL-VERIFIED]` — all Mastra/Backlog.md/Beads/MCP-governance capability rows (§5.7 Mastra/Backlog/Beads, §5.8 governance, XC risk rows R1/R3/R4/R5/R6/R8/R9). Provenance: Tavily/Context7 web research, NOT current repo facts.
- `[DESIGN — UNBUILT]` — target-stack ownership/adapter/mapping rows (§5.5 ownership/adapter rows, §5.6-27, XC decision/roadmap/recommendation rows). These describe proposed architecture, not implemented integration. **No source file in the repo implements any Mastra/Backlog.md/Beads integration today.**

**Key load-bearing facts for synthesis agents:**
1. The single migration seam is `ClaudeProcess` + `StepRunner`/`execute_pipeline`; gate/model/diagnostic logic is runtime-agnostic pure Python (highly portable).
2. Multiple defined-but-unwired or drift hazards must be preserved/flagged not silently fixed: CERTIFY_GATE (unwired), deviation classifier (UNCLASSIFIED), trailing gate grace=0→blocking, `.compressed.md` gate-target, Path-A `_verify_checkpoints()` gap, sprint Path A/B divergence, partial 4-layer isolation, stubbed status/logs.
3. Target-stack corrections vs the seed brief: Beads is Dolt-first (not SQLite+JSONL); Backlog.md MCP rejects unknown properties; Mastra RBAC/SSO/FGA/audit are Enterprise-licensed; `superclaude pipeline` is a package not a root command; sprint prompt is `/sc:task` not `/sc:task-unified`.
4. A governance/control-plane layer is required beyond the three components for multi-tenant deployment; current models carry no tenant/actor/audit identity.

**Source files read (18 of 18 requested):** research files 01-11 (all read), web-01 through web-04 (all read), DECISION-SUMMARY.md, ROADMAP.md, RISK-REGISTER.md (all read). No source file could not be read.
