# Research: 01 - Pipeline Core Contracts
**Investigation type:** Code Tracer / Integration Mapper
**Scope:** src/superclaude/cli/pipeline/ (models.py, executor.py, gates.py, process.py, trailing_gate.py, deliverables.py, diagnostic_chain.py) for Mastra + Backlog.md + Beads port feasibility
**Status:** Complete
**Date:** 2026-06-02
---

## Research Log

### Shared models (`src/superclaude/cli/pipeline/models.py`)

**File purpose and boundaries.** `models.py` defines shared dataclass/enum contracts for sprint and roadmap pipeline consumers. The module docstring explicitly states it has zero imports from `superclaude.cli.sprint` or `superclaude.cli.roadmap` and that all types are generic primitives (`models.py:1-5`). Imports are stdlib only: `dataclasses`, `datetime/timezone`, `Enum`, `Path`, and typing primitives/protocols (`models.py:8-15`).

**Key contracts.**
- `CosmeticRemediator` protocol (`models.py:17-37`): callable contract `__call__(output_file: Path, gate_name: str, failure_reason: str, *, step_id: str) -> tuple[bool, list[str]]`. It is injected through `PipelineConfig.cosmetic_remediator` and is expected to be idempotent (`models.py:20-27`).
- `StepStatus` enum (`models.py:40-67`): lifecycle states `PENDING`, `PASS`, `FAIL`, `TIMEOUT`, `CANCELLED`, `SKIPPED`; exposes `is_terminal`, `is_success`, and `is_failure`. Notably `is_failure` is true only for `FAIL` and `TIMEOUT`, not `CANCELLED` or `SKIPPED` (`models.py:64-67`).
- `GateMode` enum (`models.py:69-79`): `BLOCKING` and `TRAILING`; trailing steps are documented as non-blocking until grace-period evaluation (`models.py:72-74`).
- `SemanticCheck` dataclass (`models.py:81-87`): pure-Python content check with `name`, `check_fn: Callable[[str], bool | str]`, and `failure_message`.
- `GateCriteria` dataclass (`models.py:90-105`): required frontmatter fields, `min_lines`, `enforcement_tier` literal (`STRICT`, `STANDARD`, `LIGHT`, `EXEMPT`), and optional semantic checks. Required frontmatter fields support either exact keys or tuple OR-groups for aliases (`models.py:94-104`).
- `Step` dataclass (`models.py:108-123`): id, prompt, output file, gate, timeout, input paths, retry limit, model, gate mode, tool-write mode, and optional template path. This is the core unit Mastra/Beads would need to model as a task/job contract.
- `StepResult` dataclass (`models.py:125-148`): step pointer, status, attempt, gate failure reason, start/finish timestamps, remediation metadata, and computed duration.
- `DeliverableKind` enum and `Deliverable` dataclass (`models.py:151-209`): portable deliverable classification and JSON round-trip helpers. `Deliverable.from_dict()` defaults missing `kind` to `implement` for backward compatibility (`models.py:201-208`).
- `PipelineConfig` dataclass (`models.py:212-235`): work directory, dry-run, max turns, model, permission flag defaulting to `--dangerously-skip-permissions`, debug flag, grace period, and cosmetic remediation settings.

**Integration implications for Mastra + Backlog.md + Beads.** The pipeline model layer is already largely framework-neutral: it contains no Claude subprocess imports and no sprint/roadmap imports (`models.py:1-5`, `models.py:8-15`). A port can represent `Step` as a Mastra workflow step or Beads issue/task with explicit fields for output artifact path, gate criteria, retry limit, and gate mode. `GateCriteria` is a clean seam for preserving current gate behavior without porting the entire CLI runtime. `PipelineConfig.permission_flag` and `ClaudeProcess`-specific settings should be split from portable orchestration config in a new stack because `permission_flag` only makes sense for the current Claude CLI process boundary.

**Edge cases / risks.** `StepResult.step` is optional but executor state building assumes it is present (`executor.py:455-465`), so a port should avoid null-step results or explicitly handle them. `StepStatus.is_failure` excludes `CANCELLED`, which affects aggregate failure counts (`executor.py:467-469`); reproducing summaries in Beads must preserve that semantic or intentionally change it.

**Key Takeaways.** The shared data contracts are the strongest migration seam: `Step`, `GateCriteria`, `StepResult`, and `PipelineConfig` can be translated to Mastra workflow schemas and Beads task metadata with minimal dependency drag. The main risk is accidentally baking current Claude CLI process flags into the portable orchestration model.

### Generic executor (`src/superclaude/cli/pipeline/executor.py`)

**File purpose and boundaries.** `executor.py` is a generic step sequencer with retry, gates, and parallel dispatch (`executor.py:1-5`). It imports only logging/threading/datetime/path/typing plus pipeline-local `gate_passed`, models, and `TrailingGateRunner` (`executor.py:12-20`). The docstring states NFR-007: no sprint/roadmap imports (`executor.py:7`).

**Key functions and contracts.**
- `_gate_target(output_file: Path) -> Path` (`executor.py:23-35`): prefers a sibling `.compressed.md` sidecar named from `output_file.stem`; falls back to the original output. This is a critical hidden data-flow rule: gates validate what downstream LLM steps consume when compression sidecars exist (`executor.py:24-30`).
- `StepRunner` protocol (`executor.py:41-60`): `__call__(step, config, cancel_check) -> StepResult`. The runner owns subprocess execution and timeout status; executor owns retry, gates, and ordering (`executor.py:44-52`).
- `execute_pipeline(...) -> list[StepResult]` (`executor.py:63-188`): accepts steps as `list[Step | list[Step]]`, where nested lists represent parallel groups (`executor.py:75-78`). It supports callbacks for start, complete, and state update, cancellation, and optional trailing gate runner (`executor.py:63-72`).
- `_execute_single_step(...) -> StepResult` (`executor.py:191-399`): implements retry loop, cancellation, blocking/trailing gate mode branching, cosmetic remediation, and final fail result.
- `_run_parallel_steps(...) -> list[StepResult]` (`executor.py:402-452`): runs a group in daemon threads and sets a shared cancellation event when any step fails (`executor.py:413-423`).
- `_build_state(results) -> dict` (`executor.py:455-469`): emits a compact mutable state dictionary with per-step status/attempt/reason and aggregate total/passed/failed.

**Data flow.** `execute_pipeline()` iterates entries; sequential entries go through `_execute_single_step()` (`executor.py:124-135`), while list entries run through `_run_parallel_steps()` (`executor.py:108-123`). `_execute_single_step()` invokes the injected `run_step`, normalizes a new `StepResult` with the current attempt (`executor.py:230-238`), and then either trusts no-gate steps (`executor.py:240-243`), returns timeout/cancelled statuses without gates (`executor.py:245-248`), submits trailing gates (`executor.py:250-262`), or synchronously validates blocking gates against `_gate_target()` (`executor.py:264-278`). Gate failure can trigger cosmetic remediation (`executor.py:280-365`), retry (`executor.py:375-376`), or terminal fail (`executor.py:378-388`).

**Trailing gate behavior.** If `config.grace_period > 0`, `execute_pipeline()` creates a `TrailingGateRunner` when one is not provided (`executor.py:99-103`). `config.grace_period == 0` forces `GateMode.BLOCKING` even if the step declares `TRAILING` (`executor.py:211-215`). For trailing mode, the step is submitted to the trailing runner and immediately returned as `PASS` (`executor.py:250-262`). At pipeline end, pending trailing gate results are collected with timeout `max(30.0, float(config.grace_period))`, and failures are logged as warnings rather than converted into failed `StepResult`s (`executor.py:175-187`). Deferred trailing steps not reached because the main pipeline halted still execute after the halt (`executor.py:141-173`).

**Parallel behavior.** Parallel groups call `on_step_start()` for all steps first (`executor.py:108-112`), execute workers in daemon threads (`executor.py:425-432`), append all results, call `on_step_complete()`, and halt if any result is not `PASS` (`executor.py:113-123`). Inside workers, any non-PASS result sets a cancellation event for siblings (`executor.py:416-423`). There is no explicit retry logic at the group level; each worker delegates to `_execute_single_step()` with per-step retry semantics (`executor.py:420`).

**Integration implications for Mastra + Backlog.md + Beads.** The `StepRunner` protocol is the process-boundary seam: Mastra can provide an alternative runner that invokes agents, workflows, or Beads-backed tasks while reusing equivalent gate and retry semantics. The nested-list parallel-group structure can map to Mastra fan-out/fan-in nodes. The callbacks `on_step_start`, `on_step_complete`, and `on_state_update` are natural emitters for Beads status updates or Backlog.md task progress. Trailing gates are advisory/shadow checks in current code because failures log warnings but do not alter returned results (`executor.py:175-187`); a port must decide whether Beads should represent trailing failures as annotations, separate issues, or hard blockers.

**Edge cases / risks.** Current executor re-wraps `StepResult` after `run_step()` and drops `remediated/remediations` unless they are set in the executor's own remediation path (`executor.py:230-238`, `executor.py:253-260`, `executor.py:269-276`, `executor.py:379-386`). Deferred trailing execution also re-wraps and drops remediation fields (`executor.py:162-170`). `_build_state()` assumes `r.step.id` exists (`executor.py:455-465`). Trailing gate failures do not appear in returned state except through logs (`executor.py:175-187`). These are behavioral details a migration should either preserve for compatibility or explicitly fix with tests.

**Key Takeaways.** The executor cleanly separates orchestration from step execution. A Mastra port can keep the semantic contract: ordered entries, parallel groups, per-step retry, blocking gates, advisory trailing gates, cancellation, and callback-driven state. The largest migration risk is preserving subtle non-failing trailing-gate semantics and compressed-sidecar validation.

### Gate validation (`src/superclaude/cli/pipeline/gates.py`)

**File purpose and boundaries.** `gates.py` is pure Python validation with no subprocess or LLM invocation (`gates.py:1-9`). It imports only `re`, `Path`, and `GateCriteria` (`gates.py:12-17`).

**Key functions.**
- `gate_passed(output_file: Path, criteria: GateCriteria) -> tuple[bool, str | None]` (`gates.py:20-76`): enforces tiered validation and returns human-readable failure reasons.
- `_check_frontmatter(content: str, required_fields: list[str | tuple[str, ...]], output_file: Path) -> tuple[bool, str | None]` (`gates.py:91-142`): finds YAML frontmatter and validates required fields, including OR-groups.

**Gate tier behavior.** `EXEMPT` always passes (`gates.py:28-30`). `LIGHT`, `STANDARD`, and `STRICT` require the file to exist and be non-empty (`gates.py:32-39`). `LIGHT` stops after existence/non-empty (`gates.py:41-43`). `STANDARD` and `STRICT` enforce minimum line count (`gates.py:45-51`) and required frontmatter fields (`gates.py:53-60`). `STANDARD` stops there (`gates.py:61-63`). `STRICT` additionally runs semantic checks and short-circuits on the first non-`True` result (`gates.py:65-74`).

**Frontmatter parser behavior.** `_FRONTMATTER_RE` scans for delimiter pairs anywhere in content, not only at byte 0 (`gates.py:79-82`, `gates.py:111-120`). `_TOPLEVEL_KEY_RE` matches top-level keys and intentionally ignores nested list items or continuation lines (`gates.py:84-88`). `_check_frontmatter()` rejects delimiter pairs without a top-level key and accepts the first delimiter body with at least one top-level key (`gates.py:111-123`). Tuple fields express OR aliases; failure messages specify the missing aliases (`gates.py:127-135`).

**Integration implications for Mastra + Backlog.md + Beads.** Gate validation is highly portable. It can run as a Mastra validation step, a Beads acceptance check, or a Backlog.md artifact contract without invoking Claude. The tier model gives a clear compatibility matrix: preserve `EXEMPT/LIGHT/STANDARD/STRICT` exactly if migration needs current behavior. Failure reasons are already operator-readable and could become Beads comments or diagnostics entries.

**Edge cases / risks.** The parser tolerates preamble before frontmatter (`gates.py:103-104`, `gates.py:111-120`), so a stricter YAML parser in another stack may reject outputs that currently pass. Semantic checks can return a string; any string other than literal `True` causes failure and becomes the detail text (`gates.py:67-74`). Existing behavior does not parse YAML deeply; it only checks top-level key presence via regex (`gates.py:125-140`).

**Key Takeaways.** Gate validation is an excellent extraction target for a Mastra/Beads port because it is deterministic, local, and dependency-light. Preserve regex-based permissiveness unless deliberately tightening contracts.

### Process boundary (`src/superclaude/cli/pipeline/process.py`)

**File purpose and boundaries.** `process.py` manages `claude --print` subprocess lifecycle and is generic over output format (`process.py:1-9`). It imports logging, os, signal, subprocess, Path, and typing (`process.py:12-19`).

**Key class and methods.**
- `ClaudeProcess` (`process.py:24-244`): manages one child process with stdout/stderr redirected to files and optional lifecycle hooks (`process.py:24-35`).
- `__init__(...)` (`process.py:37-72`): accepts prompt, output/error files, max turns, model, permission flag, timeout, output format, extra args, spawn/signal/exit hooks, environment overrides, and `tool_write_mode`.
- `build_command() -> list[str]` (`process.py:73-95`): builds `claude --print --verbose <permission_flag> --no-session-persistence --tools default --max-turns <N> --output-format <format>`, plus optional `--model` and extra args.
- `build_env(...) -> dict[str, str]` (`process.py:97-112`): copies environment, removes `CLAUDECODE` and `CLAUDE_CODE_ENTRYPOINT`, then applies overrides.
- `start() -> subprocess.Popen` (`process.py:114-157`): creates output dirs, opens stdout/stderr files, starts process with stdin pipe and optional `os.setpgrp`, writes the prompt to stdin, closes stdin, and calls spawn hook.
- `wait() -> int` (`process.py:159-171`): waits with timeout, terminates on timeout, returns `124` for timeout, calls exit hook, and closes handles.
- `terminate() -> None` (`process.py:173-214`): sends SIGTERM to process group when available, waits 10 seconds, then SIGKILL and waits 5 seconds; calls signal/exit hooks.
- `validate_tool_write_output() -> bool` (`process.py:216-236`): for `tool_write_mode=True`, verifies the intended output file exists and is non-empty.

**Process data flow.** The prompt is delivered through stdin rather than argv to avoid Linux `MAX_ARG_STRLEN` limits (`process.py:73-78`, `process.py:136-139`). When `tool_write_mode=False`, stdout is the output file (`process.py:118-123`). When `tool_write_mode=True`, stdout goes to a `.log` sidecar and the model is expected to write `output_file` via tools (`process.py:118-121`, `process.py:216-236`). Child env removes nested Claude session markers (`process.py:97-112`).

**Integration implications for Mastra + Backlog.md + Beads.** This file is the current hard boundary to Claude CLI. A Mastra port likely replaces `ClaudeProcess` with a Mastra agent/action runner, but must preserve equivalent contracts: prompt input, artifact output path, stderr/log capture, timeout status, cancellation/termination, and lifecycle events. `tool_write_mode` is especially relevant for Backlog.md/Beads because it distinguishes stdout-captured artifacts from tool-authored files. Lifecycle hooks can map to diagnostic spans or Beads event comments.

**Edge cases / risks.** `wait()` assumes `start()` has initialized `_process`; a port should make lifecycle states explicit. Timeout returns code `124` to match bash timeout (`process.py:163-165`). `terminate()` may call `_close_handles()` without an exit hook if the process is already absent/exited (`process.py:173-177`). The current command always includes `--tools default` and `--no-session-persistence` (`process.py:79-91`), which are Claude CLI-specific and should not leak into Mastra-level contracts.

**Key Takeaways.** `ClaudeProcess` should be treated as replaceable infrastructure, not core orchestration logic. The portable contract is: run an agent with prompt/config, stream or materialize outputs to known artifact paths, enforce timeout/cancellation, capture logs, and emit lifecycle diagnostics.

### Trailing gates and remediation (`src/superclaude/cli/pipeline/trailing_gate.py`)

**File purpose and boundaries.** `trailing_gate.py` provides asynchronous gate evaluation, typed result collection, deferred remediation logging, remediation prompt construction, remediation retry accounting, and scope-based gate-mode resolution (`trailing_gate.py:1-7`). It imports only stdlib modules plus pipeline-local `gate_passed`, `GateCriteria`, `GateMode`, `Step`, and `StepResult` (`trailing_gate.py:11-24`). Its docstring states no sprint/roadmap imports (`trailing_gate.py:8`).

**Key result and queue contracts.**
- `TrailingGateResult` dataclass (`trailing_gate.py:34-47`): `step_id`, `passed`, `evaluation_ms`, and optional `failure_reason`. The docstring notes a spec deviation: an older spec expected `(passed, evaluation_ms, gate_name)`, while implementation uses `(step_id, passed, evaluation_ms, failure_reason)` and calls the roadmap v3.0 version authoritative (`trailing_gate.py:38-40`).
- `GateResultQueue` (`trailing_gate.py:49-85`): wraps `queue.Queue`; `put()` enqueues and increments an internal pending counter (`trailing_gate.py:61-65`), `drain()` drains available results and decrements pending (`trailing_gate.py:67-81`), and `pending_count()` returns `qsize()` rather than the internal `_pending` field (`trailing_gate.py:83-85`).

**Trailing runner contract.** `TrailingGateRunner` (`trailing_gate.py:93-228`) owns daemon-thread evaluation. `submit(step, gate_check=gate_passed)` returns an immediate pass result for steps without gates (`trailing_gate.py:126-136`), otherwise increments `_pending_count`, starts a daemon thread, selects a `.compressed.md` sidecar when present, runs the gate, enqueues `TrailingGateResult`, logs, and decrements `_pending_count` in `finally` (`trailing_gate.py:138-187`). Exceptions become failed `TrailingGateResult` entries with `failure_reason="Gate evaluation raised an exception"` (`trailing_gate.py:171-180`). `wait_for_pending(timeout=30.0)` joins active threads until a deadline and drains available results without hanging indefinitely (`trailing_gate.py:193-211`). `cancel()` sets a cancellation event, joins threads for up to one second each, and clears the thread list (`trailing_gate.py:213-222`).

**Deferred remediation and policy contracts.** `TrailingGatePolicy` is a runtime-checkable protocol that consumers implement to build remediation steps and report changed files (`trailing_gate.py:241-274`). `build_remediation_prompt(gate_result, original_step, file_paths=None) -> str` constructs a deterministic prompt with failure reason, acceptance criteria, file paths, and scoped instructions to fix only the gate failure (`trailing_gate.py:282-346`). `RemediationRetryStatus` and `RemediationRetryResult` model retry outcomes and turn accounting (`trailing_gate.py:354-370`). `attempt_remediation(...) -> RemediationRetryResult` performs a retry-once state machine with pre-budget checks, turn debits, `run_step`, and `check_gate` callbacks (`trailing_gate.py:373-468`).

**Persistent remediation log.** `RemediationStatus` has `PENDING`, `REMEDIATED`, and `WAIVED` values (`trailing_gate.py:471-477`). `RemediationEntry` serializes one failed gate result with remediation status (`trailing_gate.py:479-505`). `DeferredRemediationLog` keeps entries under a lock, appends failed gate results, persists to disk when configured, returns pending entries, marks entries remediated, serializes/deserializes JSON, loads from disk if present, and exposes `entry_count` (`trailing_gate.py:508-596`).

**Scope-based gate strategy.** `GateScope` values are `RELEASE`, `MILESTONE`, and `TASK` (`trailing_gate.py:604-610`). `resolve_gate_mode(scope, config_gate_mode=GateMode.BLOCKING, grace_period=0) -> GateMode` makes release gates always blocking, milestone gates configurable, task gates trailing only when grace period is positive, and unknown fallbacks blocking (`trailing_gate.py:612-647`).

**Integration implications for Mastra + Backlog.md + Beads.** This module provides multiple reusable seams: asynchronous validation can become Mastra background validation nodes; `TrailingGateResult` can become Beads issue comments or checklist annotations; `DeferredRemediationLog` can be replaced by Beads as the durable remediation ledger; `build_remediation_prompt()` can seed targeted agent tasks; `attempt_remediation()` can map to a Mastra bounded retry workflow with budget/debit hooks. The current port should preserve the same `.compressed.md` validation target rule (`trailing_gate.py:146-156`) to match executor behavior (`executor.py:23-35`).

**Doc/source staleness marker.** **[STALE DOC] [CODE-CONTRADICTED]** The inline `TrailingGateResult` docstring explicitly records a spec mismatch: a prior spec said `TrailingGateResult(passed, evaluation_ms, gate_name)`, but source implements `step_id`, `passed`, `evaluation_ms`, `failure_reason` (`trailing_gate.py:34-47`). Any external migration doc relying on the older shape is stale.

**Edge cases / risks.** `GateResultQueue.pending_count()` returns `qsize()` (`trailing_gate.py:83-85`), while `put()`/`drain()` also maintain `_pending` (`trailing_gate.py:57-65`, `trailing_gate.py:79-80`); this is harmless for current return value but could confuse a port. `TrailingGateRunner.submit()` increments `_pending_count` only for gated steps, while no-gate steps enqueue immediate results without incrementing that counter (`trailing_gate.py:126-140`). `attempt_remediation()` returns `PERSISTENT_FAILURE` rather than `BUDGET_EXHAUSTED` when attempt 1 fails and budget disallows attempt 2 (`trailing_gate.py:433-440`), preserving the comment that one attempt was already debited (`trailing_gate.py:386-390`).

**Key Takeaways.** Trailing gate infrastructure is portable but semantically advisory in the current executor. The most natural Beads migration is to externalize deferred remediation entries into beads/issues while preserving the exact `TrailingGateResult` shape and retry accounting.

### Deliverable decomposition (`src/superclaude/cli/pipeline/deliverables.py`)

**File purpose and boundaries.** `deliverables.py` provides heuristic behavioral detection and decomposition of deliverables into implement/verify pairs (`deliverables.py:1-6`). It imports `re` and pipeline model classes only (`deliverables.py:8-12`).

**Heuristic constants.** `_COMPUTATIONAL_VERBS` contains verbs such as `compute`, `extract`, `implement`, `validate`, `generate`, `dispatch`, `execute`, `build`, `create`, and `register` (`deliverables.py:14-53`). `_STATE_MUTATION_PATTERNS` looks for `self._\w+`, `counter`, `offset`, `cursor`, `mutate`, and `state` (`deliverables.py:55-63`). `_CONDITIONAL_PATTERNS` includes `guard`, `sentinel`, `flag`, `early return`, `bounded`, `retry`, `fallback`, `threshold`, `limit`, and `cap` (`deliverables.py:65-79`). `_DOC_VERBS` suppress false positives for documentation-oriented descriptions (`deliverables.py:81-97`).

**Key functions.**
- `is_behavioral(description: str) -> bool` (`deliverables.py:100-143`): returns false for empty descriptions, lowercases input, suppresses documentation verbs unless behavioral verb hits outnumber doc signals, then checks computational verbs, state mutation regexes, and conditional patterns.
- `decompose_deliverables(deliverables: list[Deliverable]) -> list[Deliverable]` (`deliverables.py:146-194`): expands behavioral deliverables into `.a` implement and `.b` verify deliverables, preserves metadata by shallow copy, passes non-behavioral deliverables through unchanged, and does not re-decompose IDs ending `.a` or `.b`.

**Integration implications for Mastra + Backlog.md + Beads.** This module is a candidate for a pre-orchestration transformation phase. Backlog.md items or Beads tasks could be expanded into implement/verify subitems before Mastra execution. The decomposition result is deterministic and relies on `Deliverable.to_dict()/from_dict()` from `models.py:191-209`, making it portable across JSON/YAML task formats.

**Edge cases / risks.** Documentation verbs can suppress behavioral classification even when a description contains one behavioral verb if doc signals are equal or greater (`deliverables.py:118-126`). IDs ending `.a` or `.b` are considered already decomposed regardless of kind or metadata (`deliverables.py:164-168`). Verification descriptions are hard-coded around internal correctness, input domain boundaries, operand identity, and post-condition assertions (`deliverables.py:178-184`), which may be too implementation-specific for a generic Beads task.

**Key Takeaways.** Deliverable decomposition is portable and deterministic but heuristic. If Mastra/Beads uses it, preserve idempotency and document that `.a`/`.b` suffixes have semantic meaning.

### Diagnostic chain (`src/superclaude/cli/pipeline/diagnostic_chain.py`)

**File purpose and boundaries.** `diagnostic_chain.py` implements a four-stage diagnostic chain for persistent remediation failures: troubleshoot, root causes, solutions, and summary (`diagnostic_chain.py:1-8`). It degrades gracefully and states runner-side execution does not consume TurnLedger turns; budget-specific halts skip it (`diagnostic_chain.py:9-14`). It imports only logging, dataclass/field, and Enum (`diagnostic_chain.py:19-25`) and states no sprint/roadmap imports (`diagnostic_chain.py:16`).

**Key contracts.**
- `DiagnosticStage` enum (`diagnostic_chain.py:28-35`): `TROUBLESHOOT`, `ROOT_CAUSES`, `SOLUTIONS`, `SUMMARY`.
- `StageResult` dataclass (`diagnostic_chain.py:37-45`): stage, output, success flag, optional error.
- `DiagnosticReport` dataclass (`diagnostic_chain.py:47-68`): list of stage results and summary; `is_complete` requires exactly four successful stages (`diagnostic_chain.py:54-58`), `stages_completed` counts successful stage results (`diagnostic_chain.py:60-62`), and `get_stage()` returns a matching stage result (`diagnostic_chain.py:64-68`).

**Stage implementations.** `_run_troubleshoot()` builds a Markdown analysis from failure reason and the first 500 characters of remediation output (`diagnostic_chain.py:71-89`). `_run_root_causes()` emits three static hypotheses using the failure reason (`diagnostic_chain.py:92-109`). `_run_solutions()` emits three static solution classes for the step (`diagnostic_chain.py:112-130`). `_run_summary()` compiles successful stage outputs and degraded stage errors (`diagnostic_chain.py:133-158`).

**Execution flow.** `run_diagnostic_chain(step_id, failure_reason, remediation_output="") -> DiagnosticReport` creates an empty report, executes each stage in sequence, catches exceptions per stage, appends failed `StageResult`s when needed, and sets `report.summary` only if summary stage succeeds (`diagnostic_chain.py:161-247`). Later stages receive empty strings when prior stages fail (`diagnostic_chain.py:197-219`).

**Integration implications for Mastra + Backlog.md + Beads.** The diagnostic chain is currently deterministic text generation, not actual LLM invocation. It can become a Mastra post-failure workflow that emits a Beads diagnostic comment or a Backlog.md report. Because it does not consume TurnLedger turns in current semantics (`diagnostic_chain.py:12-14`, `diagnostic_chain.py:171-172`), a port should keep diagnostics outside agent-turn budgets unless intentionally changing budget policy.

**Edge cases / risks.** Despite the docstring labels “adversarial,” the current implementation is static string assembly with no adversarial agent calls (`diagnostic_chain.py:92-130`). This matters for migration claims: porting should preserve current behavior unless the new stack intentionally upgrades diagnostics. `DiagnosticReport.is_complete` depends on exactly four stage results (`diagnostic_chain.py:54-58`); adding extra diagnostic stages would change completion semantics.

**Key Takeaways.** Diagnostic contracts are simple and portable. The key migration risk is overstating current intelligence: the code assembles deterministic Markdown diagnostics and catches failures; it does not run external troubleshoot/adversarial agents in this module.

### Public pipeline API (`src/superclaude/cli/pipeline/__init__.py`)

**File purpose and exports.** `__init__.py` defines a broad public API surface for the pipeline package, with its docstring advertising 42 symbols across models, deliverables, executor, gates, process, guard analysis, FMEA, dataflow, and conflict review (`__init__.py:1-21`). It imports and re-exports the investigated contracts: `decompose_deliverables`, `is_behavioral`, `DiagnosticReport`, `DiagnosticStage`, `StageResult`, `run_diagnostic_chain`, `execute_pipeline`, `gate_passed`, `Deliverable`, `DeliverableKind`, `GateCriteria`, `PipelineConfig`, `SemanticCheck`, `Step`, `StepResult`, `StepStatus`, `ClaudeProcess`, `DeferredRemediationLog`, `GateResultQueue`, `GateScope`, remediation types, `TrailingGatePolicy`, `TrailingGateResult`, `TrailingGateRunner`, `attempt_remediation`, `build_remediation_prompt`, and `resolve_gate_mode` (`__init__.py:40-89`). The `__all__` list exposes these same contracts as importable public API (`__init__.py:91-157`).

**Integration implications for Mastra + Backlog.md + Beads.** Because the pipeline package already centralizes its public surface, a port can define an equivalent “core contracts” module in the target stack. However, the API has grown beyond the seven files in this investigation; the exported guard/FMEA/dataflow/conflict symbols (`__init__.py:23-39`, `__init__.py:48-63`) may be relevant for other agents’ sections and should not be silently excluded from a full orchestration port.

**Key Takeaways.** The investigated contracts are public API, not private implementation details. Migration should treat names such as `Step`, `GateCriteria`, `execute_pipeline`, `ClaudeProcess`, `TrailingGateRunner`, and `DeferredRemediationLog` as compatibility anchors.

### Consumer data-flow mapping across current CLI commands

**Roadmap generation consumer.** `src/superclaude/cli/roadmap/executor.py` imports `decompose_deliverables`, `execute_pipeline`, `Step`, `StepResult`, `StepStatus`, and `ClaudeProcess` from pipeline modules (`roadmap/executor.py:25-35`). `roadmap_run_step()` wraps step prompts for incremental writes when `step.tool_write_mode` is enabled, including optional template content (`roadmap/executor.py:1088-1105`), then constructs `ClaudeProcess` with text output and `tool_write_mode=step.tool_write_mode` (`roadmap/executor.py:1107-1118`). It polls cancellation and returns `CANCELLED`, `TIMEOUT`, `FAIL`, or `PASS` `StepResult`s based on process outcome (`roadmap/executor.py:1120-1157`, `roadmap/executor.py:1243-1250`). For tool-write steps, it verifies output file presence/non-empty and separately checks merge completeness (`roadmap/executor.py:1159-1195`). Non-tool output is sanitized before gate validation (`roadmap/executor.py:1195-1197`). Post-step compression creates sidecars for downstream LLM inputs (`roadmap/executor.py:1217-1241`), while `execute_pipeline()` later gates via `_gate_target()` and may validate the compressed sidecar (`executor.py:23-35`, `executor.py:264-267`). `execute_roadmap()` builds steps, handles dry-run, resume gate pre-checks, wires a roadmap-owned cosmetic remediator into `PipelineConfig`, then calls `execute_pipeline(steps, config, roadmap_run_step, on_step_start, on_step_complete)` (`roadmap/executor.py:3075-3131`).

**Roadmap validation consumer.** `src/superclaude/cli/roadmap/validate_executor.py` reuses `ClaudeProcess` for validation steps: it composes prompt plus embedded inputs, constructs `ClaudeProcess` with text output, polls cancellation, maps exit code `124` to `TIMEOUT`, maps non-zero exit to `FAIL`, sanitizes output, and returns `PASS` (`validate_executor.py:105-180`). The file docstring says it reuses `execute_pipeline()` and `ClaudeProcess` (`validate_executor.py:7`), and source references confirm `ClaudeProcess` construction in the runner (`validate_executor.py:122-132`).

**Tasklist validation consumer.** `src/superclaude/cli/tasklist/executor.py` mirrors the validation runner: `tasklist_run_step()` composes embedded inputs, creates `ClaudeProcess` with text output, polls cancellation, maps timeout and non-zero exits to `StepResult`, sanitizes output, and returns `PASS` (`tasklist/executor.py:92-188`). `_build_steps()` creates a single `Step` named `tasklist-fidelity` with `TASKLIST_FIDELITY_GATE`, timeout 600, retry limit 1, and model from config (`tasklist/executor.py:191-218`). `execute_tasklist_validate()` calls `execute_pipeline(steps=steps, config=config, run_step=tasklist_run_step)` and then checks for failed/timeout results before inspecting report severity (`tasklist/executor.py:251-276`).

**Sprint consumer.** `src/superclaude/cli/sprint/executor.py` imports `Step`, `StepResult`, `DeferredRemediationLog`, and `TrailingGateResult` from pipeline modules (`sprint/executor.py:12-16`). `SprintGatePolicy` builds a focused remediation `Step` from a `TrailingGateResult`, using the failure reason and a remediation output directory under the sprint work dir (`sprint/executor.py:55-79`). `_resolve_wiring_mode()` imports `GateMode`, `GateScope`, and `resolve_gate_mode`, maps config scope strings to `GateScope`, and maps resolved `GateMode.BLOCKING` to wiring mode `full` and `GateMode.TRAILING` to wiring mode `shadow` (`sprint/executor.py:427-455`). `run_post_task_wiring_hook()` uses that mode to skip, shadow-log, soft-warn, or full-block findings; shadow mode logs findings to `DeferredRemediationLog`, while full mode can change task status to fail and perform inline remediation accounting (`sprint/executor.py:458-624`). `_log_shadow_findings_to_remediation_log()` creates synthetic `TrailingGateResult(step_id, passed=False, evaluation_ms=0.0, failure_reason=...)` entries and appends them (`sprint/executor.py:632-658`). The main sprint execution constructs `TurnLedger`, `ShadowGateMetrics`, and `DeferredRemediationLog(persist_path=config.results_dir / "remediation.json")` before phase execution (`sprint/executor.py:1198-1211`). For non-task phases, sprint still launches its own sprint-specific `ClaudeProcess` wrapper with isolation env vars (`sprint/executor.py:1320-1325`).

**Integration implications for Mastra + Backlog.md + Beads.** Current consumers already prove the seam: roadmap, validation, and tasklist use the generic executor plus injected `run_step`; sprint uses shared model/remediation contracts but has its own orchestration loop for phases and wiring hooks. A Mastra port could first recreate the generic executor path for roadmap/tasklist/validate, then separately model sprint’s phase/task loop and wiring gates. Beads can replace `DeferredRemediationLog` for shadow findings and remediation state; Backlog.md can own `Step`/deliverable declarations; Mastra can own `execute_pipeline` fan-out/fan-in and retry semantics.

**Edge cases / risks.** Roadmap code comments at `roadmap/executor.py:1217-1219` say “Gate checks run on the ORIGINAL output file,” but current generic executor prefers a `.compressed.md` sidecar when present (`executor.py:23-35`, `executor.py:264-267`). Because `roadmap_run_step()` may create compressed sidecars for `generate-*` or `merge` outputs (`roadmap/executor.py:1217-1241`), this comment is stale or at least misleading. This must be reconciled before writing migration docs.

**Key Takeaways.** The current architecture is not one monolith. Pipeline contracts are reused across commands, but process execution and remediation behavior vary by consumer. Migration should separate core contracts, generic executor semantics, consumer-specific runners, and sprint-specific wiring/remediation policy.

### Documentation cross-validation and staleness notes

**Tasklist analysis doc.** `docs/analysis-sc-tasklist.md` describes tasklist validation flow as CLI invocation → config → `_build_steps()` → `execute_pipeline(steps, config, tasklist_run_step)` → Claude subprocess → `tasklist-fidelity.md` → high-severity check (`docs/analysis-sc-tasklist.md:170-187`). **[CODE-VERIFIED]** Current source matches this: `_build_steps()` creates `tasklist-fidelity` with `TASKLIST_FIDELITY_GATE` (`tasklist/executor.py:191-218`), `execute_tasklist_validate()` calls `execute_pipeline(... tasklist_run_step)` (`tasklist/executor.py:251-263`), `tasklist_run_step()` constructs and runs `ClaudeProcess` (`tasklist/executor.py:130-157`), and high severity is checked after pipeline completion (`tasklist/executor.py:265-276`). The doc’s listed gate fields, strict tier, and 20-line minimum (`docs/analysis-sc-tasklist.md:197-202`) are **[CODE-VERIFIED]** by `TASKLIST_FIDELITY_GATE` (`tasklist/gates.py:23-46`).

**Sprint TUI reference doc.** `docs/developer-guide/sprint-tui-reference.md` says sprint process flow uses `ClaudeProcess: claude --print`, `--output-format stream-json`, stdout/stderr files (`docs/developer-guide/sprint-tui-reference.md:61-66`), and that `ClaudeProcess` writes NDJSON consumed by `OutputMonitor` (`docs/developer-guide/sprint-tui-reference.md:69-76`). **[CODE-VERIFIED]** for the generic process boundary: base `ClaudeProcess.build_command()` constructs `claude --print --verbose ... --output-format <format>` and stdout/stderr file redirection happens in `start()` (`process.py:73-95`, `process.py:118-134`). **[CODE-VERIFIED]** for sprint non-task phases: sprint executor launches a sprint-specific `ClaudeProcess(config, phase, env_vars=...)` and starts it (`sprint/executor.py:1320-1325`). **[STALE DOC] [CODE-CONTRADICTED]** for file inventory line counts: the doc lists `executor.py` as ~816 lines and `monitor.py` as ~264 lines (`docs/developer-guide/sprint-tui-reference.md:89-91`), but current files are 2148 and 571 lines respectively (`wc -l` on 2026-06-02). Treat inventory sizes as historical.

**Skill-vs-CLI divergence doc.** `docs/analysis/skill-vs-cli-divergence-roadmap.md` states the CLI has no MCP integration and uses subprocess LLM calls via `ClaudeProcess` (`docs/analysis/skill-vs-cli-divergence-roadmap.md:289-295`). **[CODE-VERIFIED]** for the investigated pipeline process boundary: `ClaudeProcess` builds a direct `claude` subprocess command (`process.py:73-95`), and roadmap/tasklist validation runners construct `ClaudeProcess` directly (`roadmap/executor.py:1107-1118`, `tasklist/executor.py:130-140`). This research did not inspect every CLI command for MCP usage, so the global “no MCP integration at all” statement is **[UNVERIFIED]** outside the investigated orchestration pipeline.

**Sprint deep dive doc.** `docs/sprint-cli-deep-dive.md` inventories sprint files and says `executor.py` is core orchestration plus quality gate hooks and `process.py` is a ClaudeProcess subprocess wrapper plus context injection (`docs/sprint-cli-deep-dive.md:77-92`). **[CODE-VERIFIED]** for current sprint executor imports and orchestration: `sprint/executor.py` imports sprint models, monitor, process, TUI, diagnostics, and pipeline remediation contracts (`sprint/executor.py:12-40`) and contains the main phase loop launching `ClaudeProcess` for non-task phases (`sprint/executor.py:1235-1325`). **[STALE DOC] [CODE-CONTRADICTED]** for line estimate: the doc says executor is ~1850 lines (`docs/sprint-cli-deep-dive.md:82`), but current `sprint/executor.py` is 2148 lines (`wc -l` on 2026-06-02).

**Inline code-comment contradiction.** **[STALE DOC] [CODE-CONTRADICTED]** `roadmap/executor.py` comments say “Gate checks run on the ORIGINAL output file” for compressed outputs (`roadmap/executor.py:1217-1219`), but current generic executor uses `_gate_target()` to prefer `.compressed.md` sidecars when present (`executor.py:23-35`) and blocking gate validation calls `gate_passed(gate_target, step.gate)` (`executor.py:264-267`). Trailing gates use the same sidecar preference (`trailing_gate.py:146-156`). This is an important migration hazard.

**Key Takeaways.** The tasklist flow docs are substantially current for the pipeline contract. Sprint docs are useful for architecture shape but stale on line counts. The roadmap compression/gating comment is materially contradictory and should be corrected before using it as migration evidence.

### Port feasibility mapping for report Sections 2, 4, 6, and 8

#### Section 2 — Current core pipeline contract

The verified core contract is: `Step` describes prompt, output artifact, gate, timeout, inputs, retry limit, model, gate mode, tool-write behavior, and template (`models.py:108-123`); `PipelineConfig` carries run-level settings (`models.py:212-235`); `execute_pipeline()` sequences `Step | list[Step]` entries, where lists are parallel groups (`executor.py:63-78`); `StepRunner` is injected and owns actual process/agent execution (`executor.py:41-60`); gates are deterministic `GateCriteria` checks (`gates.py:20-76`); results are `StepResult` records with status, attempt, failure reason, timestamps, and remediation metadata (`models.py:125-148`). This is feasible to recreate in Mastra as workflow schema plus executor/action wrappers, with Backlog.md or Beads storing step metadata and artifact references.

#### Section 4 — Migration seams and reusable units

Strong reusable seams:
- **Models:** `Step`, `GateCriteria`, `StepResult`, `Deliverable`, and `PipelineConfig` (`models.py:108-235`).
- **Gate engine:** `gate_passed()` and `_check_frontmatter()` (`gates.py:20-142`).
- **Executor semantics:** `execute_pipeline()` plus `_execute_single_step()` and `_run_parallel_steps()` (`executor.py:63-188`, `executor.py:191-452`).
- **Process adapter seam:** `StepRunner` protocol (`executor.py:41-60`) and `ClaudeProcess` replacement point (`process.py:24-244`).
- **Trailing/remediation seam:** `TrailingGateResult`, `TrailingGateRunner`, `DeferredRemediationLog`, `build_remediation_prompt()`, and `attempt_remediation()` (`trailing_gate.py:34-47`, `trailing_gate.py:93-228`, `trailing_gate.py:282-346`, `trailing_gate.py:373-596`).
- **Deliverable preprocessor:** `is_behavioral()` and `decompose_deliverables()` (`deliverables.py:100-194`).
- **Diagnostics:** `run_diagnostic_chain()` (`diagnostic_chain.py:161-247`).

For Mastra, the cleanest seam is to replace only `StepRunner`/`ClaudeProcess` first while preserving executor and gate semantics. For Beads, the cleanest seam is replacing `DeferredRemediationLog` and state callbacks with issue/task updates. For Backlog.md, the cleanest seam is expressing `Step`, `GateCriteria`, and deliverables in Markdown/YAML frontmatter and compiling them into workflow steps.

#### Section 6 — Risks, edge cases, and compatibility hazards

Key risks:
- **Compressed sidecar behavior:** gates prefer `.compressed.md` sidecars when present (`executor.py:23-35`, `trailing_gate.py:146-156`), contradicting at least one roadmap code comment (`roadmap/executor.py:1217-1219`).
- **Trailing failures are advisory:** trailing gate failures only log warnings at pipeline sync and do not change returned `StepResult` statuses (`executor.py:175-187`).
- **Result re-wrapping drops fields:** executor re-wraps runner results and can drop non-core fields except for its own remediation path (`executor.py:230-238`, `executor.py:253-260`, `executor.py:379-386`).
- **Optional step field assumption:** state building assumes `StepResult.step.id` exists even though `StepResult.step` is optional (`models.py:137`, `executor.py:455-465`).
- **Regex frontmatter permissiveness:** current gates accept frontmatter after preamble and use top-level-key regex rather than a YAML parser (`gates.py:79-142`); stricter parsers would change pass/fail behavior.
- **Diagnostic intelligence is limited:** diagnostic chain is deterministic text assembly, not actual LLM troubleshooting (`diagnostic_chain.py:71-158`).
- **Sprint is partially separate:** sprint uses shared remediation/model contracts but not the generic `execute_pipeline()` for its main phase loop (`sprint/executor.py:1235-1325`). A single generic Mastra pipeline will not cover all sprint behavior without additional modeling.

#### Section 8 — Recommended target-stack contract sketch

Recommended compatibility-preserving target shape:
1. Define a target-stack `PipelineStep` equivalent to `Step` with id, prompt/source prompt, output artifact, inputs, timeout, retry limit, model/agent selector, gate criteria, gate mode, and write mode (`models.py:108-123`).
2. Define a `PipelineRunConfig` equivalent to portable parts of `PipelineConfig`; keep Claude-specific permission flags in a runner-specific adapter config (`models.py:226-235`, `process.py:73-95`).
3. Implement a Mastra runner equivalent to `StepRunner` so process execution can be swapped without changing sequencing semantics (`executor.py:41-60`).
4. Port `gate_passed()` behavior exactly, including tier semantics and permissive frontmatter scanning (`gates.py:20-142`).
5. Preserve nested-list parallel groups or compile them into explicit fan-out/fan-in workflow nodes (`executor.py:75-78`, `executor.py:402-452`).
6. Represent trailing gate failures as non-blocking Beads issues/comments unless the migration intentionally strengthens semantics; current code logs warnings only (`executor.py:175-187`).
7. Store remediation state in Beads rather than JSON if Beads is the durable task/remediation ledger, but preserve `TrailingGateResult` fields (`trailing_gate.py:34-47`, `trailing_gate.py:508-596`).
8. Add compatibility tests for sidecar gate target selection, trailing warning-only behavior, retry counts, timeout `124`, frontmatter OR-groups, and cosmetic remediation pass-through.

**Key Takeaways.** A Mastra + Backlog.md + Beads port is feasible at the core contract layer because orchestration, gating, process execution, remediation, and diagnostics are already separated. The port should start by preserving `StepRunner` semantics and pure-Python gates, then gradually replace `ClaudeProcess` and JSON remediation logs with target-stack equivalents.

## Gaps and Questions

1. **Mastra/Backlog.md/Beads APIs not externally verified in this pass.** This investigation was a code tracer/integration mapper over current SuperClaude source. It did not fetch current Mastra, Backlog.md, or Beads documentation, so target-stack API claims are framed as integration implications, not verified implementation details.
2. **Global CLI “no MCP integration” is only partially verified.** The investigated pipeline path uses `ClaudeProcess` subprocesses (`process.py:73-95`; `roadmap/executor.py:1107-1118`; `tasklist/executor.py:130-140`). The broader doc claim that no CLI command uses MCP is **[UNVERIFIED]** outside this pipeline-focused scope.
3. **Roadmap compressed-gate target needs owner decision.** Current executor and trailing gates prefer `.compressed.md` sidecars for validation (`executor.py:23-35`; `trailing_gate.py:146-156`), while a roadmap comment says gates run on original output (`roadmap/executor.py:1217-1219`). Migration should preserve code behavior unless maintainers decide the comment reflects intended behavior and the code should change.
4. **Trailing gate result handling is under-specified for the target stack.** Current code logs trailing failures but returns overall step `PASS` (`executor.py:250-262`, `executor.py:175-187`). Beads could represent these as non-blocking issues, warnings, or blockers; preserving current behavior means non-blocking annotations.
5. **Sprint main loop requires separate modeling.** Sprint uses shared pipeline models/remediation contracts, but its main phase execution is a custom loop that launches sprint `ClaudeProcess` directly (`sprint/executor.py:1235-1325`). A generic `execute_pipeline` port does not fully recreate sprint orchestration.
6. **Diagnostic chain naming may overpromise.** The module names stages as troubleshoot/adversarial/solutions, but current code is static Markdown assembly with graceful exception handling (`diagnostic_chain.py:71-158`). A target-stack “agentic” diagnostic chain would be an enhancement, not a direct port.

## Stale Documentation Found

1. **[STALE DOC] [CODE-CONTRADICTED] `TrailingGateResult` historical spec shape.** Inline docstring states older spec expected `(passed, evaluation_ms, gate_name)`, but implementation uses `(step_id, passed, evaluation_ms, failure_reason)` (`trailing_gate.py:34-47`).
2. **[STALE DOC] [CODE-CONTRADICTED] Roadmap compression/gate comment.** `roadmap/executor.py` says gate checks run on original output for compressed outputs (`roadmap/executor.py:1217-1219`), but generic executor and trailing runner prefer `.compressed.md` sidecars when present (`executor.py:23-35`; `trailing_gate.py:146-156`).
3. **[STALE DOC] [CODE-CONTRADICTED] Sprint TUI reference line counts.** `docs/developer-guide/sprint-tui-reference.md` lists `sprint/executor.py` around 816 lines and `monitor.py` around 264 lines (`docs/developer-guide/sprint-tui-reference.md:89-91`); current counts are 2148 and 571 lines (`wc -l` on 2026-06-02).
4. **[STALE DOC] [CODE-CONTRADICTED] Sprint deep dive executor estimate.** `docs/sprint-cli-deep-dive.md` lists `sprint/executor.py` around 1850 lines (`docs/sprint-cli-deep-dive.md:82`); current file is 2148 lines (`wc -l` on 2026-06-02).
5. **[UNVERIFIED] Global no-MCP CLI claim.** `docs/analysis/skill-vs-cli-divergence-roadmap.md` says CLI has no MCP integration at all (`docs/analysis/skill-vs-cli-divergence-roadmap.md:289-295`). Pipeline paths in this scope are subprocess-based, but every CLI command was not audited.

## Summary

The SuperClaude CLI orchestration core is feasible to port or recreate in a Mastra + Backlog.md + Beads stack if the migration preserves the verified contracts rather than copying the Claude subprocess implementation wholesale. The key portable units are `Step`, `GateCriteria`, `StepResult`, `PipelineConfig`, deterministic gate validation, `execute_pipeline` sequencing, trailing gate result contracts, remediation prompt/retry structures, deliverable decomposition, and diagnostic report shapes.

The strongest migration seam is `StepRunner`: the current executor already delegates actual execution to an injected callable while retaining ordering, retry, gate, cancellation, parallel group, state callback, cosmetic remediation, and trailing gate behavior. Mastra can replace `ClaudeProcess` behind that seam. Backlog.md can declare steps/deliverables/gates. Beads can persist status updates, trailing-gate findings, remediation records, and diagnostics.

The main compatibility risks are subtle: compressed sidecar gate validation, warning-only trailing failures, permissive regex frontmatter parsing, optional-but-assumed step references, executor result re-wrapping, and sprint’s separate phase loop. Preserve these behaviors with tests before changing semantics.
