# Research: Integration Points

**Status:** Complete
**Date:** 2026-06-15

---

## IP-1: `_run_one_task` per-task spawn + status ladder (executor.py)

**File:** `src/superclaude/cli/sprint/executor.py`

### Verified signature (`:963-975`) — CONFIRMED
```python
def _run_one_task(
    task,
    config: SprintConfig,
    phase,
    *,
    started_at,
    prior_context: str = "",
    ledger: TurnLedger | None = None,
    subprocess_factory=None,
    shadow_metrics: ShadowGateMetrics | None = None,
    remediation_log: DeferredRemediationLog | None = None,
    lock=None,
) -> tuple[TaskResult, TrailingGateResult | None]:
```
- Returns `tuple[TaskResult, TrailingGateResult | None]`.
- **New shared param (P3):** add `reset_policy: SessionResetPolicy | None = None` as a keyword-only param at the end of the `*,` block (after `lock=None`). It carries the shared `_latch_tripped` state across K>1 workers and is guarded by the SAME `lock` already passed in.

### Spawn point (`:986-993`) — CONFIRMED (this is the UNLOCKED concurrency win)
```python
    if subprocess_factory is not None:
        exit_code, turns_consumed, output_bytes = subprocess_factory(
            task, config, phase
        )
    else:
        exit_code, turns_consumed, output_bytes = _run_task_subprocess(
            task, config, phase, prior_context=prior_context
        )
```
- **Contract consumed:** `(task, config, phase[, prior_context])`.
- **Contract produced:** `(exit_code: int, turns_consumed: int, output_bytes: int)`.
- The transcript is at `config.task_output_file(phase, task)` (resolved at `:998` as `task_output_path`). The factory writes to that same path (test seam writes per-attempt transcripts there).
- **EXACT WRAP POINT (P3):** This `if subprocess_factory … else …` block is the re-spawn unit. Wrap `:986-993` in a bounded loop:
  1. check `reset_policy._latch_tripped` under `lock` BEFORE each spawn; if tripped, classify HALT and break;
  2. spawn (UNLOCKED — leave the `:986-993` block outside the lock);
  3. after the spawn, call `detect_provider_failure(task_output_path)` → feed `reset_policy.decide(signal, attempt)`;
  4. `RETRY_NEW_SESSION` → loop (re-spawn); `HALT_MODEL_SWITCH` → trip latch under `lock`, set status `FAIL_PROVIDER_EXHAUSTED`, break; `CONTINUE` → fall through to the existing status ladder.

### Status ladder (`:999-1015`) — CONFIRMED, line-exact
```python
    task_output_path = config.task_output_file(phase, task)   # :998
    if exit_code == 0:
        status = TaskStatus.PASS                              # :999-1000
    elif exit_code == 124:
        status = TaskStatus.INCOMPLETE                        # :1001-1002
    elif detect_error_max_turns(task_output_path) and _task_completed_before_overrun(
        task_output_path
    ):
        status = TaskStatus.PASS_RECOVERED                    # :1003-1011 (completion-evidence gate)
    elif _is_transient_failure(task_output_path):
        status = TaskStatus.FAIL_RECOVERABLE                  # :1012-1013
    else:
        status = TaskStatus.FAIL_TERMINAL                     # :1014-1015
```
- **INSERT POINT (P3):** New provider-failure branch goes BELOW the `:1003` completion gate (`PASS_RECOVERED`) and ABOVE `:1012` `_is_transient_failure`. Per spec §4 Layer 4 + edge case #1, gate the provider-failure branch behind `_task_completed_before_overrun(task_output_path)` so a clean-success-then-trailing-429 (where `detect_error_max_turns` is False so the `:1003` branch is skipped) still classifies `PASS_RECOVERED` and is NOT re-spawned. Detector order: `success-envelope → error_max_turns (PASS_RECOVERED) → provider-failure → transient → terminal`.
- NOTE: in the wrapped design, the actual *classification* of `FAIL_PROVIDER_EXHAUSTED` happens inside the re-spawn loop (when the policy returns HALT or the cap is hit). The ladder branch at `:1012`-ward is reached only when the policy returns `CONTINUE` (NONE / OPERATION_TIMEOUT) — i.e., the ladder remains the fall-through for non-429 outcomes.

### TaskResult construction (`:1027-1035`) — CONFIRMED (under the `lock` guard at `:1017-1018`)
```python
        result = TaskResult(
            task=task,
            status=status,
            turns_consumed=turns_consumed,
            exit_code=exit_code,
            started_at=started_at,
            finished_at=finished_at,
            output_bytes=output_bytes,
        )
```
- **INSERT POINT (P3):** add `failure_class=...`, `session_resets=...`, `exhausted_model=...` kwargs here, populated from the re-spawn loop's accumulated counters (e.g. `failure_class="provider_exhaustion"`, `session_resets=<attempt count>`, `exhausted_model=<resolved model from signal>`). This construction is already inside `with guard:` (the `lock`), so writing these from loop-local vars is race-safe.

### Call site K>1 parallel (`:1134-1145`) — CONFIRMED, `lock=lock`
```python
        result, gate_result = _run_one_task(
            task, config, phase,
            started_at=started_at,
            prior_context=prior_context,
            ledger=ledger,
            subprocess_factory=_subprocess_factory,
            shadow_metrics=shadow_metrics,
            remediation_log=remediation_log,
            lock=lock,                       # :1144
        )
```
- **EDIT (P3):** thread the new `reset_policy=<shared policy>` kwarg here. The shared `SessionResetPolicy` instance must be created ONCE per phase (alongside `ledger`/`shadow_metrics`) so its `_latch_tripped` is shared across all K>1 workers in the wave. Inside `_execute_phase_tasks_parallel` (`:1048-1062`), add a `reset_policy` param and pass it through; the per-phase caller constructs it.

### Call site K=1 sequential (`:1337-1348`) — CONFIRMED, `lock=None`
```python
        result, gate_result = _run_one_task(
            task, config, phase,
            started_at=started_at,
            prior_context=prior_context,
            ledger=ledger,
            subprocess_factory=_subprocess_factory,
            shadow_metrics=shadow_metrics,
            remediation_log=remediation_log,
            lock=None,                       # :1347
        )
```
- **EDIT (P3):** thread `reset_policy=<per-phase policy>`. With `lock=None`, the latch checks/trips fall through `contextlib.nullcontext()` (the existing `guard = lock if lock is not None else contextlib.nullcontext()` pattern at `:1017`), so no concurrency concern — the latch is effectively a simple bool here.

---

## IP-2: Single-session phase path — spawn + `_determine_phase_status` (executor.py)

**File:** `src/superclaude/cli/sprint/executor.py`

### Single-session spawn (`:1815-1816`) — CONFIRMED
```python
                proc_manager = ClaudeProcess(config, phase, env_vars=_phase_env_vars)   # :1815
                proc_manager.start()                                                     # :1816
```
- `_phase_env_vars` built at `:1808-1813` (CLAUDE_WORK_DIR / CLAUDE_SETTINGS_DIR / CLAUDE_PLUGIN_DIR isolation keys).
- `ClaudeProcess(config, phase, env_vars=…)` — see IP-7 (process.py) for the contract (`config.model → --model`, `env_vars` merges into `os.environ.copy()`).

### Poll loop + exit-code capture (`:1831-1956`) — CONFIRMED
- Poll loop `:1831-1948` (`while proc_manager._process.poll() is None`), watchdog/stall handling inside.
- Exit-code capture `:1950-1956`: `raw_rc = proc_manager._process.returncode`; `_timed_out → 124`; else `raw_rc if not None else -1`.
- `monitor.stop()` `:1957`; `finished_at` `:1958`.
- The phase transcript path is `config.output_file(phase)` (set at `:1792` as `output_path`, passed to `monitor.reset`). **This is the path `detect_provider_failure` reads** for the single-session 429 signal.

### `_determine_phase_status` call (`:1993-2001`) — CONFIRMED
```python
                status = _determine_phase_status(
                    exit_code=exit_code,
                    result_file=config.result_file(phase),
                    output_file=config.output_file(phase),
                    config=config,
                    phase=phase,
                    started_at=started_at.timestamp(),
                    error_file=config.error_file(phase),
                )
```
- **EXACT WRAP POINT (P4):** The re-spawn unit is the block **`:1815-1956`** (spawn `:1815-1816` → poll `:1831-1948` → exit-code capture `:1950-1956`). Wrap this in a bounded loop driven by `detect_provider_failure(config.output_file(phase))` + `SessionResetPolicy`:
  1. spawn + poll + capture exit_code;
  2. call `detect_provider_failure(config.output_file(phase))`;
  3. `SINGLE_ACCOUNT_LIMIT` + attempt < cap → re-spawn (loop back to `:1815`); **must `monitor.reset`/re-`setup_isolation` per attempt** since each attempt re-derives `output_path`/isolation;
  4. `ALL_ACCOUNT_COOLDOWN` (any attempt) OR cap-exhausted → set `status = PhaseStatus.PROVIDER_EXHAUSTED` and skip the normal `_determine_phase_status` call.
- The branch is inserted **after exit-code capture (`:1956`) and BEFORE the `_determine_phase_status` call (`:1993`)**. Note the `exit_code==0` preliminary-result write at `:1982-1990` sits between — a 429 transcript exits non-zero (the CLI's terminal envelope), so the preliminary-write guard (`if exit_code == 0`) is not triggered for an exhaustion attempt; safe to leave it.
- DO NOT route a 429 through `_determine_phase_status`: at `:2774` `exit_code != 0` would otherwise fall to `PhaseStatus.ERROR` (`:2795`) via the existing non-zero path — exactly the misclassification P4 fixes. The wrap must short-circuit to `PROVIDER_EXHAUSTED` before `:1993`.

### `_determine_phase_status` definition (`:2751-2832`) — CONFIRMED
- Signature `:2751-2760`: `(exit_code, result_file, output_file, *, config=None, phase=None, started_at=0.0, error_file=None) -> PhaseStatus`.
- Priority ladder: `124→TIMEOUT` (`:2772`), `exit!=0 → [prompt_too_long → INCOMPLETE | checkpoint → PASS_RECOVERED | ERROR]` (`:2774-2795`), result-file EXIT_RECOMMENDATION/status parsing (`:2797-2822`), output-only → PASS_NO_REPORT (`:2824-2830`), else ERROR (`:2832`).
- **No edit needed inside `_determine_phase_status`** — P4 short-circuits to `PROVIDER_EXHAUSTED` at the call site (`:1993`) rather than adding a branch here, because the function has no access to the 429 signal (it keys on exit_code + result/output files, not the stream-json 429 body). Adding `PROVIDER_EXHAUSTED` detection here would require re-reading the transcript and double-detecting; the wrap-at-call-site approach (spec §4 Layer 4) is cleaner. **PhaseStatus.PROVIDER_EXHAUSTED enum member is added in models.py (P4, IP-8).**

---

## IP-3: Phase-halt consumers — per-task vs single-session DIVERGENCE (executor.py)

**File:** `src/superclaude/cli/sprint/executor.py`

> **CORRECTION to research-notes line 31 / spec §4-Layer2.** Research-notes claims `executor.py:2103` (`if status.is_failure:`) "only halts the phase (desired)" and that `is_failure` "has no auto-remediation consumer in the live executor." **Both are imprecise.** Verified below.

### Two SEPARATE phase-completion paths

**(A) Per-task path (K=1 and K>1) — `:1752-1781`, then `continue`:**
```python
                phase_report = aggregate_task_results(
                    phase.number, task_results, remaining_task_ids=remaining
                )                                                       # :1752-1754
                all_passed = phase_report.status == "PASS"             # :1755
                status = PhaseStatus.PASS if all_passed else PhaseStatus.ERROR  # :1756
                phase_result = PhaseResult(... status=status ...)      # :1757-1764
                phase_result = run_post_phase_wiring_hook(...)         # :1767-1773
                sprint_result.phase_results.append(phase_result)       # :1775
                logger.write_phase_result(phase_result)                # :1776
                _write_phase_result_json(config, phase, phase_result)  # :1778
                ...
                continue                                               # :1781
```
- The per-task block **`continue`s at `:1781`** — it NEVER reaches the `:2103` `if status.is_failure:` diagnostic-bundle consumer. So **a per-task `FAIL_PROVIDER_EXHAUSTED` does NOT trigger DiagnosticCollector/FailureClassifier/ReportGenerator.** Contract #4 (no spurious product-bug bundle) is already satisfied for the per-task path by construction.
- **Rollup contract:** `aggregate_task_results` (`:354`) counts `tasks_passed` via `r.status.is_success`. `FAIL_PROVIDER_EXHAUSTED` is NOT in `TaskStatus.is_success` (`models.py:57-58`), so a provider-exhausted task drops `tasks_passed < tasks_total` → `AggregatedPhaseReport.status` returns `"FAIL"`/`"PARTIAL"` (`:248-252`) → `all_passed=False` → `status = PhaseStatus.ERROR` (`:1756`). The sprint then halts via `:2151` (`if not all(r.status.is_success ...) → SprintOutcome.ERROR`).
- **IMPLICATION for P3 (a wrinkle the builder must encode):** Because the per-task block collapses the phase to `PhaseStatus.ERROR` (not a distinct `PROVIDER_EXHAUSTED`), the *phase-level* infra signal would be lost on the per-task path **unless** the halt-UX reads the persisted `halt_reason`/`exhausted_model` from `phase-N-result.json` (IP-5) rather than from `PhaseStatus`. The per-task `TaskResult.failure_class=="provider_exhaustion"` (IP-1) IS preserved in `task_results` and serialized via `_write_phase_result_json` (`:2691` `"task_results": [tr.to_dict() …]`), so the halt-UX / resume command can detect exhaustion by scanning `task_results[*].failure_class`. **Recommended:** in the per-task block, after `aggregate_task_results`, if any `tr.failure_class == "provider_exhaustion"`, set `phase_result` top-level `halt_reason`/`exhausted_model` (IP-5) so the single persistence path carries the signal regardless of which spawn path produced it. (PhaseStatus stays ERROR for the per-task path; PROVIDER_EXHAUSTED is the single-session phase status only — consistent with spec §4 Layer 2 "PhaseStatus.PROVIDER_EXHAUSTED for the single-session path".)

**(B) Single-session path — `:2103-2132` `if status.is_failure:`:**
```python
                if status.is_failure:                                  # :2103 (PhaseStatus.is_failure, models.py:437)
                    try:
                        collector = DiagnosticCollector(config)        # :2106
                        bundle = collector.collect(phase, phase_result, monitor.state)  # :2107
                        classifier = FailureClassifier()               # :2108
                        bundle.category = classifier.classify(bundle)  # :2109
                        reporter = ReportGenerator()                   # :2110
                        diag_path = … f"phase-{phase.number}-diagnostic.md"  # :2111-2113
                        reporter.write(bundle, diag_path)              # :2114
                    except Exception: …
                    sprint_result.outcome = SprintOutcome.HALTED       # :2130
                    sprint_result.halt_phase = phase.number            # :2131
                    break                                              # :2132
```
- This consumer keys on **`PhaseStatus.is_failure`** (`models.py:437` = `{INCOMPLETE, HALT, TIMEOUT, ERROR}`), NOT `TaskStatus`. It **DOES run a diagnostic bundle** for any failing single-session phase before halting.
- **DECISION POINT for P4 (`PhaseStatus.PROVIDER_EXHAUSTED`):** If `PROVIDER_EXHAUSTED` is ADDED to `PhaseStatus.is_failure` (so the sprint halts via `:2103`/`:2151`), the `:2103` block WILL fire DiagnosticCollector for the infra failure — violating contract #4 ("never trips remediation/diagnostic-bundle machinery meant for product bugs"). **Two clean options the builder must encode (not silently pick):**
  - **(B1)** Add `PROVIDER_EXHAUSTED` to `is_failure` AND guard the `:2103` diagnostic block with `and status != PhaseStatus.PROVIDER_EXHAUSTED` (or `and not _is_provider_exhaustion(status, phase_result)`), so it halts but skips the bundle. This keeps the existing halt+break wiring.
  - **(B2)** Do NOT add `PROVIDER_EXHAUSTED` to `is_failure`; instead add an explicit halt branch BEFORE `:2103` (`if status == PhaseStatus.PROVIDER_EXHAUSTED: set HALTED + halt_phase + break` with no bundle). Then `is_failure` stays product-bug-only.
  - **Recommended: B1** — it reuses the single `is_failure → halt → break` path and `:2151` sprint-error rollup, with a one-line bundle guard. Note `PhaseStatus.is_terminal` (`models.py:410-423`) must ALSO include `PROVIDER_EXHAUSTED` regardless of option, or the sprint-wrap assertions treat it as non-terminal.

---

## IP-4: `_is_transient_failure` — must NOT swallow 429s (executor.py)

**File:** `src/superclaude/cli/sprint/executor.py`

### Definition (`:2267-2289`) — CONFIRMED line-exact
```python
def _is_transient_failure(output_path: Path) -> bool:
    try:
        text = output_path.read_text(errors="replace")
    except OSError:
        return False
    if "api_retry" in text or "ConnectionRefused" in text:   # :2278
        return True
    for line in reversed(text.splitlines()):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            obj = json.loads(stripped)
        except (ValueError, TypeError):
            return False
        return bool(obj.get("is_error") and obj.get("output_tokens", 1) == 0)  # :2288
    return False
```
- **COLLISION RISK (the builder MUST handle):** A single-account 429 transcript contains `api_retry` events (spec §2 event #1). So `_is_transient_failure` returns **True** at `:2278` on a 429 transcript. In the per-task ladder (IP-1), `_is_transient_failure` sits at `:1012` BELOW the new provider-failure branch — so as long as the provider-failure branch is inserted ABOVE `:1012` and returns/sets `FAIL_PROVIDER_EXHAUSTED` (or re-spawns), the 429 never reaches `:1012`. **Ordering is the fix; no edit to `_is_transient_failure` itself is required** for the per-task path.
- **But** the re-spawn loop's terminal classification must be reached BEFORE the ladder for a 429 — i.e. the loop's `detect_provider_failure` check runs each attempt, and only a `CONTINUE` (NONE / OPERATION_TIMEOUT) signal falls through to the `:999-1015` ladder. A NONE signal on an `api_retry`-bearing transcript that is genuinely transient (connection refused etc.) still correctly hits `:2278` → FAIL_RECOVERABLE. So `_is_transient_failure` is left UNCHANGED; the provider-failure branch's higher precedence is what prevents misclassification.
- **No signature change.** `_is_transient_failure(output_path: Path) -> bool` is consumed only at `:1012`.

---

## IP-5: Persistence — `_write_phase_result_json` + execution-log.jsonl events (executor.py + logging_.py)

**File:** `src/superclaude/cli/sprint/executor.py` (persistence) + `src/superclaude/cli/sprint/logging_.py` (events)

### `_write_phase_result_json` (`:2657-2701`) — CONFIRMED
```python
def _write_phase_result_json(config: SprintConfig, phase: Phase, result: PhaseResult) -> None:
    ...
    payload = {
        "phase": result.phase.number,
        "status": result.status.value,
        "exit_code": result.exit_code,
        "started_at": result.started_at.isoformat(),
        "finished_at": result.finished_at.isoformat(),
        "task_results": [tr.to_dict() for tr in result.task_results],   # :2691
        "recovery_history": result.recovery_history,
        "tasklist_sha256": _content_sha256_excluding_rerun_block(phase.file),
        "tasklist_sha256_ws": _content_sha256_ws_excluding_rerun_block(phase.file),
    }
    out = config.phase_result_json(phase)
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, indent=2) + "\n")
    tmp.replace(out)
```
- **INSERT POINT (P3):** add two top-level keys to the `payload` dict (`:2685-2696`):
  ```python
      "halt_reason": result.halt_reason,            # "provider_exhaustion" or ""
      "exhausted_model": result.exhausted_model,    # resolved model or ""
  ```
- **Where the values come from — TWO sources, ONE persistence path:**
  - **Single-session path (P4):** `PhaseResult` needs NEW fields `halt_reason: str = ""` and `exhausted_model: str = ""` (added to the dataclass at `models.py:729-753`, alongside `recovery_history`). The wrap loop (IP-2) sets them on `phase_result` before `_write_phase_result_json(config, phase, phase_result)` is called (`:2097` in the single-session path).
  - **Per-task path (P3):** the per-task block (`:1752-1781`) constructs `phase_result` at `:1757-1764`. After `aggregate_task_results`, derive `halt_reason`/`exhausted_model` from `task_results` (any `tr.failure_class == "provider_exhaustion"` → set them) and assign onto `phase_result` before `_write_phase_result_json(config, phase, phase_result)` at `:1778`. The per-task evidence is ALSO already carried per-task: `tr.to_dict()` at `:2691` serializes the new `TaskResult.failure_class`/`session_resets`/`exhausted_model` fields (IP-1 / models.py P2), so a consumer can recover the signal at task granularity too.
- **Back-compat:** `PhaseResult` new fields default to `""` so a phase with no exhaustion serializes `"halt_reason": ""`. The READ side is `rerun_tasks.py` / resume — they must `.get("halt_reason", "")` (not hard-key) for old `phase-N-result.json`. (Per-task `TaskResult.from_dict` back-compat is covered in models.py P2, IP-8.)

### Event emission — `SprintLogger._jsonl` (`logging_.py:295-301`) — CONFIRMED
- The emitter idiom is `logger._jsonl({"event": "<name>", ...})` (thread-safe via `self._jsonl_lock`, `:299`). Two precedents:
  - Named method (preferred): `write_task_complete` (`logging_.py:226-249`) builds the dict + calls `self._jsonl(...)`.
  - Direct call: `executor.py:2206` `logger._jsonl({"event": "checkpoint_manifest", ...})`.
- **INSERT (P6):** add two `SprintLogger` methods mirroring `write_task_complete`:
  - `write_session_reset(phase, task_id, attempt, exhausted_model)` → `{"event": "session_reset", "phase":…, "task_id":…, "attempt":…, "exhausted_model":…, "timestamp":…}`
  - `write_account_exhaustion_halt(phase, task_id, exhausted_model, session_resets)` → `{"event": "account_exhaustion_halt", …, "timestamp":…}`
- **Emit sites:** `write_session_reset` from inside the re-spawn loop (IP-1 per-task / IP-2 single-session) after each `RETRY_NEW_SESSION` decision; `write_account_exhaustion_halt` when the loop concludes `HALT_MODEL_SWITCH` or hits the cap. `logger` is already threaded into `_execute_phase_tasks_parallel` (`:1060`) and available in the single-session loop scope (`logger.write_phase_start` at `:1820`). **Note:** `logger` is `None`-guarded throughout (e.g. `:1146 if logger is not None`); the new emit calls must follow the same `if logger is not None:` guard.

---

## IP-6: Offline classifier — `_classify_transcript` + resume fallback (rerun_tasks.py)

**File:** `src/superclaude/cli/sprint/rerun_tasks.py`

### `_classify_transcript(text: str) -> TaskStatus` (`:547-593`) — CONFIRMED line-exact
```python
def _classify_transcript(text: str) -> TaskStatus:
    result_event: Optional[dict] = None
    total_output_tokens = 0
    for raw in text.splitlines():                       # :557 (parse loop)
        ...
        if event.get("type") == "result":
            result_event = event                        # :573-574
    if result_event is None:
        return TaskStatus.INCOMPLETE                     # :576-577
    subtype = str(result_event.get("subtype", ""))       # :579
    is_error = bool(result_event.get("is_error")) or subtype.startswith("error")  # :580
    if not is_error and total_output_tokens > 0:
        return TaskStatus.PASS                           # :582-583
    transient = ("api_retry" in text or "ConnectionRefused" in text or total_output_tokens == 0)  # :585-587
    if is_error and transient:
        return TaskStatus.FAIL_RECOVERABLE               # :588-589
    if is_error:
        return TaskStatus.FAIL_TERMINAL                  # :590-591
    return TaskStatus.INCOMPLETE                          # :592-593
```
- **Signature mismatch (the shared-core wrinkle):** detector `detect_provider_failure(output_path: Path)` reads a FILE; `_classify_transcript(text: str)` already has the body in memory. Per spec §4 Layer 1, factor a text-accepting inner `_provider_failure_from_text(text) -> ProviderFailureSignal` in monitor.py (P1); the path wrapper reads then delegates; `_classify_transcript` calls the inner on its existing `text`.
- **EXACT INSERT POINT (P2):** add the new branch **immediately after `:580`** (`is_error` is computed) and **ABOVE `:582`** (the PASS / transient / terminal ladder). Per spec §4 Layer 1: "placed ABOVE the existing `is_error`/transient branching (`:582-591`)." Concretely:
  ```python
      is_error = bool(result_event.get("is_error")) or subtype.startswith("error")   # :580 (unchanged)
      # NEW (P2): a 429 routing failure outranks the transient/terminal ladder.
      _sig = _provider_failure_from_text(text)
      if _sig.kind in (ProviderFailure.SINGLE_ACCOUNT_LIMIT, ProviderFailure.ALL_ACCOUNT_COOLDOWN):
          return TaskStatus.FAIL_PROVIDER_EXHAUSTED
      # OPERATION_TIMEOUT / NONE fall through to the existing ladder unchanged.
      if not is_error and total_output_tokens > 0:   # :582 (unchanged)
          ...
  ```
  - Placing it ABOVE `:582` matters because a single-account 429 has `is_error==true` AND contains `api_retry` (→ the `transient` test at `:585` is True), so without the new branch it returns `FAIL_RECOVERABLE` (tokens==0) or `FAIL_TERMINAL` (tokens>0) — exactly the misclassification §2 documents. The new branch intercepts first.
  - **Imports:** `_classify_transcript` must import `_provider_failure_from_text` + `ProviderFailure` from `.monitor`, and `FAIL_PROVIDER_EXHAUSTED` is already on `TaskStatus` (P2, models.py).

### `discover_failed_tasks_from_transcripts` (`:596-635`) — CONFIRMED, auto-covered
```python
        status = _classify_transcript(text)              # :623
        if status is not TaskStatus.PASS:
            failed.append((id_match.group(1), status))   # :624-625
```
- The hard-crash resume fallback routes EVERY transcript through `_classify_transcript` (`:623`) and appends any non-PASS as a rerun candidate (`:624`). Since `FAIL_PROVIDER_EXHAUSTED is not TaskStatus.PASS`, **once IP-6's `_classify_transcript` branch lands, a transcript-derived 429 is automatically discovered as a rerun candidate.** **No separate edit to `discover_failed_tasks_from_transcripts` is needed** (spec §4 Layer 2 / research-notes line 36 — VERIFIED).

### `retry_count_for_task` (`recovery.py:356-373`, imported here, called at `rerun_tasks.py:1482`) — CONFIRMED, SEPARATE budget
```python
def retry_count_for_task(phase_result: PhaseResult, task_id: str) -> int:
    """... Per TDD T8.2 the rerun engine caps retries at 3 ..."""
    history = getattr(phase_result, "recovery_history", []) or []  # :364
    for entry in history:
        ... if task_id in affected: count += 1
    return count
```
- Counts entries in `phase_result.recovery_history` (cross-run recovery BUNDLES). The rerun cap-3 abort at `rerun_tasks.py:1480-1487` compares `>= 3`.
- **NO edit (Q4 separation, VERIFIED):** the new `SessionResetPolicy` reset budget is **per-run / in-memory** (`SessionResetPolicy._exhaustion_attempts`, recovery_policy.py P3) and is NOT folded into `recovery_history`. So `retry_count_for_task` is untouched; session-reset attempts do NOT consume the cross-run cap-3, and a freed account on a later run gets a fresh reset budget. The two budgets are orthogonal: cap-3 = cross-run content reruns (bundles); `max_session_resets`(=8) = within-attempt account-rotation re-spawns.

---

## IP-7: Recovery nominators — `failure_class` exclusion (recovery.py)

**File:** `src/superclaude/cli/sprint/recovery.py`

### Nominator inventory — CONFIRMED (CORRECTS research-notes)
```python
class Nominator(Protocol):                      # :143
    def nominate(self, context: dict) -> list[str]: ...   # :146
class ManualNominator:                          # :149  (returns self.tasks verbatim, :160-161)
class ReflectReportNominator:                   # :164  (filters classification in (regression, drift), :225-230)
```
- **CORRECTION:** research-notes line 38 cites `ManualNominator(:152)`, `DriftNominator(:183, nominates classification=="drift")`, `ReflectReportNominator(:189+)`. **There is NO `DriftNominator`** — `grep "class.*Nominator"` returns exactly THREE symbols: `Nominator` (Protocol `:143`), `ManualNominator` (`:149`), `ReflectReportNominator` (`:164`). The "classification == drift" filter is a branch INSIDE `ReflectReportNominator.nominate` (`:226` `if cls in ("regression", "drift")`), not a separate class. Builder must target the real symbols.
- **Contract:** `nominate(self, context: dict) -> list[str]`. `ManualNominator` returns operator-supplied IDs unfiltered (`:160-161`); `ReflectReportNominator` reads a reflect-report file and nominates only `regression`/`drift` entries (`:189-230`, currently a v4.3.0 STUB returning `[]`).

### (G) deferred decision — `failure_class == "provider_exhaustion"` exclusion (P6)
- **Goal (UX contract #4):** prevent a re-routed infra failure from getting a spurious product-bug diagnostic bundle when an operator later runs `sprint rerun-tasks`.
- **Where:** the exclusion belongs in `ManualNominator.nominate` (`:160-161`) — the default `rerun-tasks --tasks …` path. Since `ManualNominator` returns IDs verbatim and has no access to per-task status, the exclusion requires reading `phase-N-result.json` `task_results[*].failure_class` from `context` (the `context: dict` passed to `nominate`). The builder must verify what keys `context` carries at the call site (see `run_rerun_tasks`, around `rerun_tasks.py:1470-1490`) — **UNVERIFIED here what `context` contains; the builder must trace the `nominate(context=…)` call site before implementing the filter.**
- **`needs_human_decision`-adjacent (per `feedback_human_decision_items_must_halt` + research-notes AMBIGUITIES (G)):** the spec offers TWO options and instructs the builder to encode the P6 nominator-exclusion as the implementation default AND document the fallback (scope contract #4 to the live auto-path) in the item Context — NOT silently pick. If the `context`-plumbing for `failure_class` proves non-trivial, the item writes the finding (PENDING) and proceeds with the documented default rather than shipping an unreviewed behavior change.
- **Note:** the per-task live path already does NOT trigger the bundle (IP-3 (A) — it `continue`s before `:2103`), so (G) only matters for the OPERATOR-invoked `rerun-tasks` re-entry, not the live sprint. This narrows the blast radius and supports deferring to P6.

---

## IP-8: Resume planner — `FAIL_PROVIDER_EXHAUSTED` auto-routing (resume/planner.py)

**File:** `src/superclaude/cli/sprint/resume/planner.py`

### `_coerce_task_status` (`:339-344`) — CONFIRMED line-exact (research-notes cited `:157`; the CALL is at `:157`, the DEF is at `:339`)
```python
    def _coerce_task_status(value: object) -> TaskStatus | None:
        """Map a persisted status string to TaskStatus, tolerant of junk."""
        try:
            return TaskStatus(value)        # :342
        except (ValueError, TypeError):
            return None
```
- **AUTO-RESOLVES the new member (VERIFIED, NO EDIT):** `TaskStatus(value)` is a value-lookup, so once `TaskStatus.FAIL_PROVIDER_EXHAUSTED = "fail_provider_exhausted"` exists (P2, models.py), a persisted `"status": "fail_provider_exhausted"` coerces to the new member automatically. No planner edit. Confirms spec §4 Layer 2 + research-notes line 39 (E).

### `rerun_task_ids` per-task seam (`:160-164`) — CONFIRMED line-exact
```python
            plan.rerun_task_ids = [
                bt.task_id
                for bt in boundary
                if bt.persisted_status is None or not bt.persisted_status.is_success   # :163
            ]
```
- **AUTO-RE-RUNS the exhausted task (VERIFIED):** the filter re-runs any task whose `persisted_status` is `None` OR `not is_success`. `FAIL_PROVIDER_EXHAUSTED` is NOT in `TaskStatus.is_success` (`models.py:57-58`), so `not bt.persisted_status.is_success` is True → the exhausted task is included in `rerun_task_ids`. No planner edit. (Resume-safety test in spec §6 asserts exactly this.)
- The `BoundaryTask.persisted_status` is set at `:157` from `_coerce_task_status(tr.get("status"))` — so the full chain `persisted "fail_provider_exhausted" → coerce → not is_success → rerun_task_ids` works once P2's enum member exists.

### Hard-crash fallback (`:165-171`) — CONFIRMED line-exact, auto-covered
```python
        else:
            # Hard crash / pre-v4.3.0: derive the failed set from transcripts.
            derived = discover_failed_tasks_from_transcripts(results_dir, interrupted)   # :167
            ...
            plan.rerun_task_ids = [task_id for task_id, _ in derived]   # :171
```
- Routes through `discover_failed_tasks_from_transcripts` → `_classify_transcript` (IP-6). Once IP-6's `_classify_transcript` returns `FAIL_PROVIDER_EXHAUSTED` for a 429 transcript, the transcript-derived resume path re-runs it too (it is non-PASS → appended at `rerun_tasks.py:624`). **No separate planner edit needed** (spec §4 Layer 2; research-notes line 39 (E) — VERIFIED). The P2 shared-detector alignment is what wires this path.

### Net: planner is ZERO-EDIT (the cleanest integration point)
Both resume seams (per-task `:157`/`:160-164` and hard-crash `:167`/`:171`) auto-resolve `FAIL_PROVIDER_EXHAUSTED` from the P2 enum + P2 `_classify_transcript` alignment. The builder must NOT add a planner edit item; instead, an explicit resume-safety TEST (spec §6) asserts the auto-routing holds.

---

## IP-9: process.py / pipeline base — `--model` injection + env inheritance (process.py)

**Files:** `src/superclaude/cli/sprint/process.py` (sprint subclass) + `src/superclaude/cli/pipeline/process.py` (base, where cmd/env actually live)

> **CORRECTION:** spec/research-notes cite `process.py:129-141` for "subprocess cmd: `claude --print … [--model M]`" and "`env_vars` merges into `os.environ.copy()`." **Those line numbers are in `src/superclaude/cli/sprint/process.py` but point at the `_make_exit_hook`/`ClaudeProcess.__init__` region, NOT the cmd/env assembly.** The actual cmd + env assembly is in the PIPELINE BASE class `src/superclaude/cli/pipeline/process.py` (imported as `_PipelineClaudeProcess` at `sprint/process.py:21`). Verified below.

### `ClaudeProcess.__init__` (sprint subclass) (`sprint/process.py:137-164`) — CONFIRMED
```python
class ClaudeProcess(_PipelineClaudeProcess):                  # :137
    def __init__(self, config, phase, *, env_vars=None):     # :146-152
        self.config = config
        self.phase = phase
        self._extra_env_vars = env_vars                       # :155
        prompt = self.build_prompt()
        super().__init__(
            prompt=prompt,
            output_file=config.output_file(phase),
            error_file=config.error_file(phase),
            max_turns=config.max_turns,
            model=config.model,                               # :162  ← config.model flows to base
            permission_flag=config.permission_flag,
            timeout_seconds=config.max_turns * 120 + 300,     # :164
        )
```
- **`config.model → model=` (`:162`):** the sprint config's `model` becomes the base's `self.model`, which the base turns into `--model` (below). **For the RESUME command (IP-10 / P5):** the halt UX builds a paste-ready `superclaude sprint run … --model <suggested>`; the `--model` value flows config → here → base `build_command` (`:140-141`). The detector's resolved exhausted model (from the cooldown body) is what the suggester diffs against to pick a DISTINCT model.

### Pipeline base `build_command` (`pipeline/process.py:121-143`) — CONFIRMED line-exact
```python
    def build_command(self) -> list[str]:
        cmd = [
            "claude", "--print", "--verbose",
            self.permission_flag,
            "--no-session-persistence",         # :132  ← every spawn is a fresh session (the re-route lever)
            "--tools", "default",
            "--max-turns", str(self.max_turns),
            "--output-format", self.output_format,
        ]
        if self.model:
            cmd.extend(["--model", self.model])  # :140-141  ← THE --model injection point
        cmd.extend(self.extra_args)
        return cmd
```
- **`--no-session-persistence` (`:132`)** is the infra ground truth: a new subprocess == a new session == a new CLIProxyAPI routing decision. The re-spawn loop (IP-1/IP-2) relies on this — each re-spawn is a genuine re-route, no extra flag needed.
- **`--model` (`:140-141`)** is conditional on `self.model` being truthy. The resume command (IP-10) sets `--model <suggested>`, which flows to `config.model` → `ClaudeProcess` (`:162`) → here.

### Pipeline base `build_env` (`pipeline/process.py:145-160`) — CONFIRMED line-exact
```python
    def build_env(self, *, env_vars=None):
        env = os.environ.copy()                 # :155  ← inherits ANTHROPIC_DEFAULT_* + proxy base URL
        env.pop("CLAUDECODE", None)
        env.pop("CLAUDE_CODE_ENTRYPOINT", None)
        if env_vars:
            env.update(env_vars)                # :158-159  ← isolation keys merged over inherited env
        return env
```
- **`os.environ.copy()` (`:155`)** is the env-inheritance contract the **alias suggester** (aienv.py, P5) depends on: the child inherits `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL` and the proxy base URL from the parent process env. The suggester reads `~/.aienv` to enumerate aliases, but the RUNTIME resolution (alias → resolved model) happens in the child via these inherited env vars — which is why the cooldown body reports a *resolved* model (`claude-opus-4-8`) even when `config.model` was an alias. **NO EDIT to process.py/pipeline base** — the suggester reads `~/.aienv` directly (aienv.py) and matches against the resolved model from the detector; it does not need to hook subprocess env assembly.
- **NET: process.py is ZERO-EDIT for this feature.** Both contracts (`--model` injection, env inheritance) already exist and are consumed read-only by IP-10's resume command and the aienv suggester respectively.

---

## IP-10: CLI flag — `--max-session-resets` registration + flow (commands.py → config.py → models.py)

**Files:** `src/superclaude/cli/sprint/commands.py` (flag) + `config.py` (loader) + `models.py` (SprintConfig field)

### The flag-flow chain (4 touch points) — ALL CONFIRMED
The `sprint run` flag flow is a 4-hop chain; `--max-session-resets` (P5) must touch ALL four, mirroring `--task-parallelism`:

1. **`commands.py` `@click.option` (`:202-209` is the `--task-parallelism` template):**
   ```python
   @click.option(
       "--task-parallelism", "task_parallelism",
       type=int, default=1, show_default=True,
       help="Number of tasks to execute concurrently per phase (1 = sequential).",
   )
   ```
   **INSERT (P5):** add a sibling `@click.option("--max-session-resets", "max_session_resets", type=int, default=8, show_default=True, help="...")` in the `run` command option stack (anywhere in `:74-232`, before `@click.pass_context` at `:233`).

2. **`run()` function param (`:234-258`):** add `max_session_resets: int,` to the signature (the params list `:236-257`). Click maps the option dest to this param.

3. **`load_sprint_config(...)` call (`commands.py:337-354`):** add `max_session_resets=max_session_resets,` to the call (the kwargs block `:339-353`).
   - And `load_sprint_config` DEF (`config.py:281-298`): add `max_session_resets: int = 8,` param (`:297` is `task_parallelism` template), and pass it into the `SprintConfig(...)` construction (`config.py:355-369`, where `task_parallelism=task_parallelism` is at `:368`).

4. **`SprintConfig` dataclass field (`models.py`):** add `max_session_resets: int = 8` (model `:590` is `task_parallelism: int = 1` template; `max_turns: int = 100` at `:536`, `model: str = ""` at `:537`).

### Consumption
- The new `config.max_session_resets` is read where the per-phase `SessionResetPolicy(max_session_resets=config.max_session_resets)` is constructed (P3) — i.e. in `execute_sprint` near the per-phase loop, threaded into `_run_one_task`/`_execute_phase_tasks_parallel` (IP-1) and the single-session loop (IP-2).

### doc⇆CLI parity (P5, per `feedback_doc_fanout_facts_sheet`)
- The halt-UX resume command (IP-10/P5 `build_account_exhaustion_halt`) emits `--model <suggested>` and the resume re-runs from the exhausted task. The doc⇆CLI parity TEST (spec §6) must assert `--model` and `--resume`/`--start` appear in `sprint run --help` AND that `--max-session-resets` (the new flag) is registered. `--model` already exists (`commands.py:94-98`); `--resume` flows via `resume_task_id` (param at `:254`) — builder should confirm the `--resume` flag's exact option name in the `:183-201` region (NOT shown in this excerpt — UNVERIFIED exact flag string; trace `resume_task_id` option decl).

---

## Cross-cutting integration summary

| Integration point | File | Edit? | Phase | Exact site |
|---|---|---|---|---|
| `_run_one_task` re-spawn loop + new `reset_policy` param + status branch | executor.py | **YES** | P3 | spawn `:986-993`; ladder insert above `:1012`; TaskResult `:1027-1035`; sig `:963-975` |
| K>1 / K=1 call sites thread `reset_policy` | executor.py | **YES** | P3 | `:1134-1145`, `:1337-1348` |
| Single-session re-spawn loop + `PROVIDER_EXHAUSTED` short-circuit | executor.py | **YES** | P4 | wrap `:1815-1956`; before `:1993` |
| Phase-halt consumer — bundle guard for `PROVIDER_EXHAUSTED` | executor.py | **YES (B1)** | P4 | `:2103` guard; `is_failure`/`is_terminal` in models.py |
| `_is_transient_failure` | executor.py | **NO** (ordering fixes it) | P3 | `:2267-2289` (unchanged) |
| Persistence `halt_reason`/`exhausted_model` | executor.py | **YES** | P3 | payload `:2685-2696`; per-task set near `:1757-1778`; single-session near `:2097` |
| `execution-log.jsonl` events | logging_.py | **YES** | P6 | new methods after `:249`; emit via `logger._jsonl` |
| `_classify_transcript` 429 branch | rerun_tasks.py | **YES** | P2 | insert above `:582`, after `:580` |
| `discover_failed_tasks_from_transcripts` | rerun_tasks.py | **NO** (auto-covered) | P2 | `:623-625` |
| `retry_count_for_task` (cap-3) | recovery.py | **NO** (Q4 separate budget) | — | `:356-373` |
| Recovery nominators `failure_class` exclusion | recovery.py | **YES (deferred/PENDING)** | P6 | `ManualNominator.nominate` `:160-161`; trace `context` first |
| Resume planner | resume/planner.py | **NO** (auto-resolves) | P2 | `_coerce_task_status` `:339`; `rerun_task_ids` `:160-164` |
| process.py `--model` + env | process.py / pipeline base | **NO** (read-only consumed) | P5 | `pipeline/process.py:140-141` (--model), `:155` (env) |
| `--max-session-resets` flag | commands.py + config.py + models.py | **YES** | P5 | 4-hop chain mirroring `--task-parallelism` |

**Key corrections to research-notes/spec citations:**
1. `:2103` DOES run a DiagnosticCollector bundle (not "only halts") — but ONLY on the single-session `PhaseStatus.is_failure` path; the per-task path `continue`s at `:1781` and never reaches it. P4's `PROVIDER_EXHAUSTED` must guard the bundle (option B1).
2. No `DriftNominator` exists in recovery.py — only `Nominator`/`ManualNominator`/`ReflectReportNominator`.
3. cmd/env assembly is in `pipeline/process.py:121-160`, not `sprint/process.py:129-141`.
4. `_coerce_task_status` DEF is at `planner.py:339`, not `:157` (the CALL is at `:157`).
5. process.py and resume/planner.py are ZERO-EDIT (auto-covered by enum + shared detector).

---

**Status:** Complete


---
