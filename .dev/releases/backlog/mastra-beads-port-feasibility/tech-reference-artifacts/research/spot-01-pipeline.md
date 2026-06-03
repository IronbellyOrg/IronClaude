# Spot-Check 01 — Pipeline-Core Seam

**Investigation type:** Code Tracer
**Status:** Complete
**Date:** 2026-06-03
**HEAD:** 9e864860

Confirm research file 01's key symbol/line claims for the pipeline-core seam against current source.

Research file: `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/research/01-pipeline-core-contracts.md`

---

## Delta Rows

Status legend: CONFIRMED = symbol present at the claimed/near-claimed line and shape matches; DRIFTED = present but at a different line or different shape (new location/shape noted); NOT-FOUND = absent.

### models.py (claimed ~234 lines; actual 235 lines)

| # | Claim (research file 01) | Research loc | Current code loc | Status |
|---|---|---|---|---|
| 1 | Module docstring: zero imports from sprint/roadmap, generic primitives | `models.py:1-5` | `models.py:1-6` | CONFIRMED |
| 2 | stdlib-only imports (dataclasses, datetime/timezone, Enum, Path, typing) | `models.py:8-15` | `models.py:8-14` | CONFIRMED |
| 3 | `CosmeticRemediator` Protocol, `__call__(output_file, gate_name, failure_reason, *, step_id) -> tuple[bool, list[str]]`, idempotent | `models.py:17-37` | `models.py:17-37` | CONFIRMED |
| 4 | `StepStatus` enum (PENDING/PASS/FAIL/TIMEOUT/CANCELLED/SKIPPED), `is_failure` true only for FAIL+TIMEOUT | `models.py:40-67` (`64-67`) | `models.py:40-66` (`is_failure` 64-66) | CONFIRMED |
| 5 | `GateMode` enum BLOCKING/TRAILING | `models.py:69-79` | `models.py:69-78` | CONFIRMED |
| 6 | `SemanticCheck` dataclass (name, check_fn: Callable[[str], bool\|str], failure_message) | `models.py:81-87` | `models.py:81-87` | CONFIRMED |
| 7 | `GateCriteria` (required_frontmatter_fields, min_lines, enforcement_tier literal STRICT/STANDARD/LIGHT/EXEMPT, semantic_checks) | `models.py:90-105` | `models.py:90-105` | CONFIRMED |
| 8 | `Step` dataclass core unit (id, prompt, output_file, gate, timeout, inputs, retry_limit, model, gate_mode, tool_write_mode, template_path) | `models.py:108-123` | `models.py:108-122` | CONFIRMED |
| 9 | `StepResult` dataclass (step, status, attempt, gate_failure_reason, timestamps, remediated/remediations, duration_seconds) | `models.py:125-148` | `models.py:125-148` | CONFIRMED |
| 10 | `DeliverableKind` + `Deliverable`; `from_dict()` defaults missing kind to `implement` | `models.py:151-209` (`201-208`) | `models.py:151-209` (`from_dict` 200-209, default 203) | CONFIRMED |
| 11 | `PipelineConfig` (work_dir, dry_run, max_turns, model, permission_flag default `--dangerously-skip-permissions`, debug, grace_period, cosmetic settings) | `models.py:212-235` | `models.py:212-234` | CONFIRMED |

### executor.py (claimed ~469 lines; actual 469 lines — exact)

| # | Claim | Research loc | Current code loc | Status |
|---|---|---|---|---|
| 12 | Module docstring NFR-007 no sprint/roadmap imports | `executor.py:7` | `executor.py:7` | CONFIRMED |
| 13 | imports: gate_passed, models, TrailingGateRunner | `executor.py:12-20` | `executor.py:12-20` | CONFIRMED |
| 14 | `_gate_target(output_file) -> Path` prefers `.compressed.md` sidecar by stem, falls back to original | `executor.py:23-35` | `executor.py:23-35` | CONFIRMED |
| 15 | `StepRunner` protocol `__call__(step, config, cancel_check) -> StepResult` | `executor.py:41-60` | `executor.py:41-60` | CONFIRMED |
| 16 | `execute_pipeline(...) -> list[StepResult]`, accepts `list[Step \| list[Step]]`, nested = parallel | `executor.py:63-188` (`75-78`) | `executor.py:63-188` (sig 63-72, parallel-list docstring 75-77) | CONFIRMED |
| 17 | grace_period > 0 creates `TrailingGateRunner` when none provided | `executor.py:99-103` | `executor.py:100-102` | CONFIRMED |
| 18 | Sequential entry → `_execute_single_step()`; list entry → `_run_parallel_steps()` | `executor.py:124-135` / `108-123` | `executor.py:124-136` / `108-123` | CONFIRMED |
| 19 | Deferred TRAILING steps run after halt | `executor.py:141-173` | `executor.py:141-173` | CONFIRMED |
| 20 | Sync point collects trailing results, timeout `max(30.0, float(grace_period))`, failures logged as warnings only | `executor.py:175-187` | `executor.py:176-186` | CONFIRMED |
| 21 | `_execute_single_step(...) -> StepResult` retry/cancel/gate-mode branch | `executor.py:191-399` | `executor.py:191-399` | CONFIRMED |
| 22 | grace_period == 0 forces BLOCKING regardless of declared TRAILING | `executor.py:211-215` | `executor.py:212-214` | CONFIRMED |
| 23 | Runner result re-wrapped with current attempt (drops remediation fields) | `executor.py:230-238` | `executor.py:230-238` | CONFIRMED |
| 24 | No-gate step trusts runner status | `executor.py:240-243` | `executor.py:240-243` | CONFIRMED |
| 25 | TIMEOUT/CANCELLED returned without gate check | `executor.py:245-248` | `executor.py:245-248` | CONFIRMED |
| 26 | TRAILING: submit to runner, return PASS immediately | `executor.py:250-262` | `executor.py:250-262` | CONFIRMED |
| 27 | BLOCKING: `gate_passed(_gate_target(output_file), step.gate)` | `executor.py:264-278` (`264-267`) | `executor.py:264-278` (target 266, call 267) | CONFIRMED |
| 28 | Cosmetic remediation lane | `executor.py:280-365` | `executor.py:280-364` | CONFIRMED |
| 29 | Retry on attempt < max | `executor.py:375-376` | `executor.py:375-376` | CONFIRMED |
| 30 | Terminal FAIL on exhausted retries | `executor.py:378-388` | `executor.py:378-388` | CONFIRMED |
| 31 | `_run_parallel_steps(...) -> list[StepResult]`, daemon threads, shared cancel event on any non-PASS | `executor.py:402-452` (`413-423`) | `executor.py:402-452` (worker 416-423, cancel_event 413) | CONFIRMED |
| 32 | `_build_state(results) -> dict`, assumes `r.step.id`, aggregate total/passed/failed via is_failure | `executor.py:455-469` | `executor.py:455-469` | CONFIRMED |

### gates.py (claimed ~142 lines; actual 142 lines — exact)

| # | Claim | Research loc | Current code loc | Status |
|---|---|---|---|---|
| 33 | Pure-Python, NFR-003 no subprocess / NFR-007 no sprint-roadmap; imports re, Path, GateCriteria | `gates.py:1-9` / `12-17` | `gates.py:1-10` / `12-17` | CONFIRMED |
| 34 | `gate_passed(output_file, criteria) -> tuple[bool, str\|None]` | `gates.py:20-76` | `gates.py:20-76` | CONFIRMED |
| 35 | EXEMPT always passes | `gates.py:28-30` | `gates.py:28-30` | CONFIRMED |
| 36 | LIGHT/STANDARD/STRICT require exist + non-empty | `gates.py:32-39` | `gates.py:32-39` | CONFIRMED |
| 37 | LIGHT stops after existence/non-empty | `gates.py:41-43` | `gates.py:41-43` | CONFIRMED |
| 38 | STANDARD/STRICT enforce min line count | `gates.py:45-51` | `gates.py:45-51` | CONFIRMED |
| 39 | STANDARD/STRICT required frontmatter | `gates.py:53-60` | `gates.py:53-59` | CONFIRMED |
| 40 | STANDARD stops there | `gates.py:61-63` | `gates.py:61-63` | CONFIRMED |
| 41 | STRICT semantic checks short-circuit on first non-True | `gates.py:65-74` | `gates.py:65-74` | CONFIRMED |
| 42 | `_FRONTMATTER_RE` scans anywhere (MULTILINE/DOTALL), not byte 0 | `gates.py:79-82` | `gates.py:79-82` | CONFIRMED |
| 43 | `_TOPLEVEL_KEY_RE` top-level keys, ignores nested/continuation | `gates.py:84-88` | `gates.py:84-88` | CONFIRMED |
| 44 | `_check_frontmatter(...)` rejects delimiter-only pairs, accepts first body w/ ≥1 top-level key, tuple OR-aliases | `gates.py:91-142` (`111-123`, `127-135`) | `gates.py:91-142` (loop 116-120, tuple 128-135) | CONFIRMED |

### process.py (claimed ~244 lines; actual 244 lines — exact) — THE runtime seam

| # | Claim | Research loc | Current code loc | Status |
|---|---|---|---|---|
| 45 | Manages `claude --print` subprocess, generic output format; imports logging/os/signal/subprocess/Path/typing | `process.py:1-9` / `12-19` | `process.py:1-10` / `12-19` | CONFIRMED |
| 46 | `ClaudeProcess` class manages one child, stdout/stderr to files, lifecycle hooks | `process.py:24-244` | `process.py:24-244` | CONFIRMED |
| 47 | `__init__(...)` (prompt, output/error files, max_turns, model, permission_flag, timeout, output_format, extra_args, hooks, env_vars, tool_write_mode) | `process.py:37-72` | `process.py:37-71` | CONFIRMED |
| 48 | `build_command() -> list[str]`: `claude --print --verbose <perm> --no-session-persistence --tools default --max-turns N --output-format <fmt>` + optional `--model` + extra args | `process.py:73-95` | `process.py:73-95` | CONFIRMED |
| 49 | `build_env(...)` copies env, removes CLAUDECODE + CLAUDE_CODE_ENTRYPOINT, applies overrides | `process.py:97-112` | `process.py:97-112` | CONFIRMED |
| 50 | `start() -> Popen`: mkdir, open stdout/stderr, stdin pipe + optional setpgrp, write prompt to stdin, close, spawn hook | `process.py:114-157` | `process.py:114-157` | CONFIRMED |
| 51 | `wait() -> int`: timeout terminate, returns `124` on timeout, exit hook, close handles | `process.py:159-171` (124 at `163-165`) | `process.py:159-171` (124 at 165) | CONFIRMED |
| 52 | `terminate()`: SIGTERM to pgroup, wait 10s, SIGKILL, wait 5s; signal/exit hooks | `process.py:173-214` | `process.py:173-214` | CONFIRMED |
| 53 | `validate_tool_write_output() -> bool`: tool_write_mode existence + non-empty | `process.py:216-236` | `process.py:216-236` | CONFIRMED |
| 54 | Prompt via stdin (bypass MAX_ARG_STRLEN) | `process.py:73-78` / `136-139` | `process.py:76-78` / `136-139` | CONFIRMED |
| 55 | tool_write_mode=True → stdout to `.log` sidecar; model writes output_file via tools | `process.py:118-121` / `216-236` | `process.py:118-120` / `216-236` | CONFIRMED |

### trailing_gate.py (claimed ~647 lines; actual 648 lines)

| # | Claim | Research loc | Current code loc | Status |
|---|---|---|---|---|
| 56 | Module: async gate eval; stdlib + pipeline-local gate_passed/GateCriteria/GateMode/Step/StepResult; no sprint/roadmap | `trailing_gate.py:1-7` / `8` / `11-24` | `trailing_gate.py:1-9` / `11-24` | CONFIRMED |
| 57 | `TrailingGateResult` (step_id, passed, evaluation_ms, failure_reason); docstring records SPEC-DEVIATION vs `(passed, evaluation_ms, gate_name)`, roadmap v3.0 authoritative | `trailing_gate.py:34-47` | `trailing_gate.py:34-46` | CONFIRMED |
| 58 | `GateResultQueue`: put increments _pending, drain decrements, pending_count returns qsize() | `trailing_gate.py:49-85` (`61-65`,`67-81`,`83-85`) | `trailing_gate.py:49-85` (put 61-65, drain 67-81, pending_count 83-85) | CONFIRMED |
| 59 | `TrailingGateRunner` (93-228); submit immediate pass for no-gate, else increment + daemon thread + sidecar select + enqueue + decrement in finally | `trailing_gate.py:93-228` (`126-136`,`138-187`) | `trailing_gate.py:93-228` (no-gate 126-136, thread 138-187) | CONFIRMED |
| 60 | Exception → failed result `failure_reason="Gate evaluation raised an exception"` | `trailing_gate.py:171-180` | `trailing_gate.py:171-180` | CONFIRMED |
| 61 | `wait_for_pending(timeout=30.0)` bounded join + drain | `trailing_gate.py:193-211` | `trailing_gate.py:193-211` | CONFIRMED |
| 62 | `cancel()` sets event, joins ≤1s each, clears list | `trailing_gate.py:213-222` | `trailing_gate.py:213-222` | CONFIRMED |
| 63 | `.compressed.md` sidecar preference in submit() (matches executor) | `trailing_gate.py:146-156` | `trailing_gate.py:146-155` | CONFIRMED |
| 64 | `TrailingGatePolicy` runtime_checkable protocol (build_remediation_step / files_changed) | `trailing_gate.py:241-274` | `trailing_gate.py:241-274` | CONFIRMED |
| 65 | `build_remediation_prompt(gate_result, original_step, file_paths=None) -> str` deterministic scoped prompt | `trailing_gate.py:282-346` | `trailing_gate.py:282-346` | CONFIRMED |
| 66 | `RemediationRetryStatus` + `RemediationRetryResult` | `trailing_gate.py:354-370` | `trailing_gate.py:354-370` | CONFIRMED |
| 67 | `attempt_remediation(...) -> RemediationRetryResult` retry-once state machine | `trailing_gate.py:373-468` | `trailing_gate.py:373-468` | CONFIRMED |
| 68 | Returns PERSISTENT_FAILURE (not BUDGET_EXHAUSTED) when attempt 1 fails + budget disallows attempt 2 (1 debited) | `trailing_gate.py:433-440` (comment `386-390`) | `trailing_gate.py:434-440` (state-machine comment 386) | CONFIRMED |
| 69 | `RemediationStatus` PENDING/REMEDIATED/WAIVED | `trailing_gate.py:471-477` | `trailing_gate.py:471-476` | CONFIRMED |
| 70 | `RemediationEntry` serializes one failed result | `trailing_gate.py:479-505` | `trailing_gate.py:479-505` | CONFIRMED |
| 71 | `DeferredRemediationLog` lock/append/persist/pending/mark/serialize/deserialize/load/entry_count | `trailing_gate.py:508-596` | `trailing_gate.py:508-596` | CONFIRMED |
| 72 | `GateScope` RELEASE/MILESTONE/TASK | `trailing_gate.py:604-610` | `trailing_gate.py:604-609` | CONFIRMED |
| 73 | `resolve_gate_mode(scope, config_gate_mode=BLOCKING, grace_period=0) -> GateMode` (release always blocking, milestone configurable, task trailing iff grace>0, fallback blocking) | `trailing_gate.py:612-647` | `trailing_gate.py:612-647` | CONFIRMED |

### deliverables.py (claimed ~194 lines; actual 194 lines — exact)

| # | Claim | Research loc | Current code loc | Status |
|---|---|---|---|---|
| 74 | Module: heuristic detect + decompose; imports re + model classes | `deliverables.py:1-6` / `8-12` | `deliverables.py:1-6` / `8-12` | CONFIRMED |
| 75 | `_COMPUTATIONAL_VERBS` (compute/extract/implement/validate/generate/dispatch/execute/build/create/register …) | `deliverables.py:14-53` | `deliverables.py:15-53` | CONFIRMED |
| 76 | `_STATE_MUTATION_PATTERNS` (self._\w+, counter, offset, cursor, mutate, state) | `deliverables.py:55-63` | `deliverables.py:56-63` | CONFIRMED |
| 77 | `_CONDITIONAL_PATTERNS` (guard/sentinel/flag/early return/bounded/retry/fallback/threshold/limit/cap) | `deliverables.py:65-79` | `deliverables.py:66-79` | CONFIRMED |
| 78 | `_DOC_VERBS` suppress false positives | `deliverables.py:81-97` | `deliverables.py:82-97` | CONFIRMED |
| 79 | `is_behavioral(description) -> bool`: empty→False, lowercase, doc-verb suppression, computational/state/conditional checks | `deliverables.py:100-143` | `deliverables.py:100-143` | CONFIRMED |
| 80 | `decompose_deliverables(...)`: .a implement + .b verify, shallow-copy metadata, pass-through non-behavioral, no re-decompose of .a/.b | `deliverables.py:146-194` (`164-168`,`178-184`) | `deliverables.py:146-194` (idempotency guard 166-168, verify desc 180-184) | CONFIRMED |

---

## ClaudeProcess as the single runtime seam — confirmation

CONFIRMED. `ClaudeProcess` (`process.py:24-244`) is the sole concrete process boundary to the `claude` CLI inside the pipeline package: it is the only class that constructs a `claude --print` argv (`build_command()`, `process.py:73-95`) and the only one that calls `subprocess.Popen` (`process.py:134`). The executor never touches a subprocess directly — it delegates all execution through the injected `StepRunner` protocol (`executor.py:41-60`, `execute_pipeline`'s `run_step` parameter). Gates (`gates.py`) and trailing-gate machinery (`trailing_gate.py`) are pure-Python (NFR-003: no subprocess import), so they do not constitute a runtime seam. Consumer runners (roadmap/tasklist/validate per research file 01 §"Consumer data-flow mapping") all route their actual LLM execution through `ClaudeProcess`. Therefore replacing `ClaudeProcess` behind the `StepRunner` seam is the single substitution point for swapping the Claude-CLI runtime, exactly as research file 01 asserts (`process.py:24-244`; Section 4 "Process adapter seam").

Note: "single runtime seam *within the pipeline package*" — research file 01 itself flags (and this spot-check does not re-investigate) that `sprint/executor.py` launches its own sprint-specific `ClaudeProcess` wrapper for non-task phases via a separate orchestration loop (`sprint/executor.py:1320-1325` per RF01). That is a separate consumer-side instantiation of the same `ClaudeProcess` class, not a second seam class.

## Summary

- **Total claims verified:** 80
- **CONFIRMED:** 80
- **DRIFTED:** 0
- **NOT-FOUND:** 0

Every load-bearing symbol/line claim in research file 01 for the pipeline-core seam holds at HEAD 9e864860. Line numbers match within 0-2 lines in all cases (minor ±1-2 offsets from docstring/blank-line counting; the ranges research file 01 cites are accurate and the cited symbols exist at those locations). File sizes match the research file's stated approximations: models.py 235 (~234), executor.py 469 (exact), gates.py 142 (exact), process.py 244 (exact), trailing_gate.py 648 (~647), deliverables.py 194 (exact). No code drift, no missing symbols. The `TrailingGateResult` SPEC-DEVIATION docstring (`trailing_gate.py:38-40`) is still present as research file 01 documented.

`ClaudeProcess` is CONFIRMED as the single runtime seam the port replaces — it is the only `subprocess.Popen` / `claude --print` boundary in the pipeline package, sitting behind the injected `StepRunner` protocol.

**Status: Complete**
