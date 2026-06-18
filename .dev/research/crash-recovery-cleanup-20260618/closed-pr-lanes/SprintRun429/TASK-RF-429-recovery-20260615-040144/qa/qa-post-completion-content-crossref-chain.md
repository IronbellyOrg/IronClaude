# QA Report — Post-Completion Cross-Phase QA (crossref-chain lens)

## VERDICT: FAIL

**Topic:** Sprint Run 429 / Account-Exhaustion Recovery (P1-P6)
**Date:** 2026-06-18
**Lens:** crossref-chain — verify the data/control hand-offs BETWEEN phases resolve to real symbols with matching names/types
**Authorization:** fix_authorization: false (report only — no edits applied)
**Stance:** Adversarial / zero-trust. Every claim verified against source; no reliance on the manifest's self-assertions.

---

## Summary

- Hand-offs verified: 6 / 6
- Hand-offs PASS (resolve cleanly end-to-end): 5
- Hand-offs with a dangling/incomplete link: 1 (hand-off #2 partial; hand-off #5 fully broken on one of two spawn paths)
- **CRITICAL findings: 1** (per-task spawn path never sets `SprintResult.halt_phase`, so the model-switch resume UX is dead on that path)
- IMPORTANT findings: 1 (test coverage gap masks the above — no end-to-end `execute_sprint` test exercises the per-task 429 → summary path)

The chain is well-built for the **single-session spawn path**. It is **broken for the per-task spawn path**, which is the path a real task-bearing sprint phase actually takes. Because the manifest's integrated-state fact #1 and the in-code comment at `executor.py:1893-1895` both explicitly claim parity "regardless of spawn path", this is a genuine cross-phase break, not an out-of-scope nicety.

---

## Hand-off results

| # | Hand-off | Result | Severity |
|---|----------|--------|----------|
| 1 | P1 `resolved_model` → P3/P5 alias suggestion | PASS | — |
| 2 | P2 persisted `failure_class`/`exhausted_model` → P5 halt UX AND P6 nominator exclusion | PARTIAL | CRITICAL (the P5 in-memory leg; see #5) |
| 3 | P5 4-hop CLI flag → P3 `SessionResetPolicy` | PASS | — |
| 4 | P3/P4 loops → P6 event emits | PASS | — |
| 5 | P4 `PROVIDER_EXHAUSTED` → P5 halt UX → single-line model-switch command | PASS (single-session) / **FAIL (per-task)** | CRITICAL |
| 6 | shared `completed_before_overrun_from_text` core consumed by live AND offline | PASS | — |

---

## Detailed verification (with file:line evidence)

### Hand-off #1 — `ProviderFailureSignal.resolved_model` → alias suggester — PASS

- Producer: `monitor._provider_failure_from_text` sets `resolved_model=cooldown.group("model")` ONLY for `ALL_ACCOUNT_COOLDOWN` (`monitor.py:326-329`); the named capture group `model` is defined in `_RE_ALL_ACCOUNT` (`monitor.py:41-43`). `SINGLE_ACCOUNT_LIMIT` and the bare-429 default carry `resolved_model=None` (`monitor.py:331,333`); `OPERATION_TIMEOUT`/`NONE` likewise default `None` (`monitor.py:336,338` via the dataclass default at `monitor.py:288`).
- Carrier: `ProviderFailureSignal.resolved_model: str | None = None` (`monitor.py:287-288`).
- Consumer (live): `executor.py:1089` `exhausted_model = signal.resolved_model or ""` (per-task HALT) and `executor.py:2139` (single-session). Persisted into `TaskResult.exhausted_model` (`executor.py:1144`) and `PhaseResult.exhausted_model` (`executor.py:1899, 2246`).
- Consumer (suggester): `SprintResult._exhaustion_halt` returns `halted.exhausted_model` (`models.py:874`); `resume_command`/`account_exhaustion_output` feed it to `suggest_alternate_model(exhausted_model)` (`models.py:887, 920`). `suggest_alternate_model` matches by alias OR resolved id (`aienv.py:107-108`) and is None-safe (`aienv.py:111-118`).
- Names/types match end-to-end. No dangling reference. **PASS.**

### Hand-off #2 — P2 persisted `failure_class`/`exhausted_model` → P5 halt UX + P6 nominator exclusion — PARTIAL

Two legs:

- **P6 nominator-exclusion leg — PASS.** `TaskResult.to_dict`/`from_dict` round-trip `failure_class` with `.get("failure_class", "")` back-compat (`models.py:223-224, 251-253`). `rerun_tasks.select_default_recoverable_tasks` reads `entry.get("failure_class") == "provider_exhaustion"` and skips it (`rerun_tasks.py:1188-1189`). The legacy transcript fallback in `run_rerun_tasks` ALSO filters `_status is not TaskStatus.FAIL_PROVIDER_EXHAUSTED` (`rerun_tasks.py:1468-1473`). Both nomination paths exclude — matches manifest claim. The offline classifier (`_classify_transcript`) emits `FAIL_PROVIDER_EXHAUSTED` (`rerun_tasks.py:605`) consistent with the persisted status. `_load_phase_result_view` reconstructs real `TaskResult.from_dict` objects (`rerun_tasks.py:1230`). **PASS.**
- **P5 halt-UX leg — BROKEN on the per-task path.** `SprintResult._exhaustion_halt` reads `halted.halt_reason`/`halted.exhausted_model`/`tr.failure_class` (`models.py:864-874`) — correct — BUT it short-circuits to `None` at `models.py:858` when `self.halt_phase is None`. On the per-task spawn path `halt_phase` is never set (see #5). So the persisted `failure_class`/`exhausted_model` reach the JSON but **never reach the live halt-UX** on that path. This is the same defect as #5; rated CRITICAL there.

### Hand-off #3 — P5 4-hop CLI flag → P3 `SessionResetPolicy` — PASS

Full chain resolves:

1. CLI option `--max-session-resets` → `run()` param `max_session_resets: int` (`commands.py:233-241, 267`).
2. `run()` → `load_sprint_config(..., max_session_resets=max_session_resets)` (`commands.py:347-365`, kwarg at `:364`).
3. `load_sprint_config` param → `SprintConfig(..., max_session_resets=max_session_resets)` (`config.py:298, 370`).
4. `SprintConfig.max_session_resets: int = 8` (`models.py:611`) → `SessionResetPolicy(max_session_resets=getattr(config, "max_session_resets", 8))` at BOTH the per-task call site (`executor.py:1356-1357`) and the single-session call site (`executor.py:1924-1925`).

`SessionResetPolicy.decide` honours the field: `attempt < self.max_session_resets` → `RETRY_NEW_SESSION` else `HALT_MODEL_SWITCH` (`recovery_policy.py:68-71`). Operator flag overrides the hardcoded 8. **PASS.**

### Hand-off #4 — P3/P4 re-spawn loops → P6 event emits — PASS

Both emit functions read the loop's own counters, signatures match call sites:

- `SprintLogger.write_session_reset(self, phase, task_id, attempt, exhausted_model)` (`logging_.py:251-252`) ← called per-task with `(phase.number, task.task_id, attempt, signal.resolved_model or "")` where `attempt = reset_policy._exhaustion_attempts` (`executor.py:1067-1068, 1075-1080`); single-session with `(phase.number, "", attempt, signal.resolved_model or "")` (`executor.py:2124-2136`). On `RETRY_NEW_SESSION` only. 4 args ↔ 4 params. ✓
- `SprintLogger.write_account_exhaustion_halt(self, phase, task_id, exhausted_model, session_resets)` (`logging_.py:273-274`) ← per-task `(phase.number, task.task_id, exhausted_model, session_resets)` with `session_resets = attempt` (`executor.py:1088, 1095-1100`); single-session `(phase.number, "", exhausted_model, attempt)` (`executor.py:2143-2148`). On the HALT branch only, emitted by the latch-tripping worker (so latch-precheck halts don't double-emit, `executor.py:1090-1093`). ✓

Counters are the loop's own (`_exhaustion_attempts` snapshot under guard), not re-derived. **PASS.**

### Hand-off #5 — P4 `PhaseStatus.PROVIDER_EXHAUSTED` → P5 halt UX → single-line model-switch command — PASS (single-session) / FAIL (per-task) — **CRITICAL**

- **Single-session path — PASS.** Loop sets `status = PhaseStatus.PROVIDER_EXHAUSTED` and `exhausted_model` (`executor.py:2138-2139`); `phase_result.halt_reason = "provider_exhaustion"` + `phase_result.exhausted_model` (`executor.py:2244-2246`); then sets `sprint_result.outcome = HALTED` AND `sprint_result.halt_phase = phase.number` (`executor.py:2293-2296`). `write_summary` gates on `if sprint.halt_phase:` (`logging_.py:336`) → calls `sprint.resume_command()` (`:338`) and `sprint.account_exhaustion_output()` (`:343`), both of which resolve `_exhaustion_halt()` (halt_phase set, halt_reason matches) → `build_account_exhaustion_halt` emits the SINGLE-LINE `--model {suggested}` resume command (`models.py:1219-1225`, single-line per the operator-cannot-paste-multiline constraint). `PROVIDER_EXHAUSTED ∈ is_terminal`, `∉ is_failure` (`models.py:435, 453-459`) so it skips the diagnostic-bundle branch (`executor.py:2298`) and TUI shows magenta `EXHAUSTED` (`tui.py:56, 73`). End-to-end intact.

- **Per-task path — FAIL.** When `_parse_phase_tasks(phase, config)` returns tasks (the normal case for any `### T<PP>.<TT>` phase), execution takes the per-task branch (`executor.py:1838-1839`). A 429 there is classified inside `_run_one_task` (`status = FAIL_PROVIDER_EXHAUSTED`, `failure_class = "provider_exhaustion"`, `executor.py:1086-1087`). Back in the phase loop, the phase status is collapsed to `PhaseStatus.ERROR` (`executor.py:1882`), and `phase_result.halt_reason`/`exhausted_model` are derived from per-task `failure_class` (`executor.py:1896-1900`) and persisted via `_write_phase_result_json` (`executor.py:1914`, writes `halt_reason`/`exhausted_model` at `:2818-2819`). **But the block then unconditionally `continue`s (`executor.py:1917`) without ever setting `sprint_result.halt_phase` or `sprint_result.outcome = HALTED`.** A grep of every `halt_phase`/`outcome` assignment in executor.py confirms `halt_phase` is set ONLY at `:2295` and `:2326` — both inside the single-session block (after the per-task `continue`).

  Consequence: on the per-task path the in-memory `SprintResult.halt_phase` stays `None`, `_exhaustion_halt()` returns `None` at `models.py:858`, and `write_summary` skips the entire exhaustion block (`logging_.py:336`). **The model-switch resume command — the load-bearing deliverable of P5 — is never emitted on the per-task path.** The post-phase ERROR status instead falls through to the generic ERROR outcome (`executor.py:2347`).

  The in-code comment at `executor.py:1893-1895` ("so the halt-UX can detect exhaustion regardless of spawn path (IP-3/IP-5)") and manifest integrated-state fact #1 both ASSERT this parity; the code only delivers it for the persisted-JSON consumer (rerun-tasks), not for the in-memory `SprintResult` halt-UX consumer. **Dangling control hand-off. CRITICAL.**

### Hand-off #6 — shared `completed_before_overrun_from_text` core, no live/offline divergence — PASS

Single definition in `monitor.py:390-430`. Live consumer: `executor._task_completed_before_overrun` is a thin wrapper that reads the file then calls `completed_before_overrun_from_text(content)` (`executor.py:2487-2510`, call at `:2510`); used at the per-task 429 gate (`executor.py:1055`) and the error_max_turns gate (`executor.py:1113`). Offline consumer: `rerun_tasks._classify_transcript` imports it (`rerun_tasks.py:45`) and calls `completed_before_overrun_from_text(text)` (`rerun_tasks.py:603`) on the same `FAIL_PROVIDER_EXHAUSTED` branch. Both also share `_provider_failure_from_text` (`executor.py` via `detect_provider_failure`; `rerun_tasks.py:44, 592`). Same function, same module, no forked copy → live and offline agree by construction. **PASS.**

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | CRITICAL | `executor.py:1882-1917` (per-task phase block) | A 429/account-exhaustion on a per-task (task-bearing) phase persists `halt_reason`/`exhausted_model` to `phase-N-result.json` but NEVER sets `sprint_result.halt_phase` / `sprint_result.outcome = SprintOutcome.HALTED`. `_exhaustion_halt()` returns `None` (`models.py:858`), so `write_summary` (`logging_.py:336`) emits NO model-switch resume block on the per-task path. Hand-off #5 (and the P5 leg of #2) is dangling for the spawn path real phases actually use. The code comment at `:1893-1895` claims spawn-path parity that the code does not deliver. | After the per-task derivation loop (`executor.py:1896-1900`), when `phase_result.halt_reason == "provider_exhaustion"`, set `sprint_result.outcome = SprintOutcome.HALTED` and `sprint_result.halt_phase = phase.number`, then `break` (do not `continue`) so the in-memory halt-UX chain fires exactly as the single-session path does at `:2293-2296`. Mirror the `PROVIDER_EXHAUSTED ∉ is_failure` no-diagnostic-bundle behavior. |
| 2 | IMPORTANT | `tests/sprint/test_executor.py:770-927` (per-task) vs `:437-531` (single-session) | The only end-to-end `execute_sprint` assertions of `halt_phase == 1` / `outcome == HALTED` use `_run_single_session_provider_cooldown` (`:437, 495, 521`). The per-task provider tests call `execute_phase_tasks` in isolation and only assert per-`TaskResult` status + a MANUALLY constructed `PhaseResult` round-trip (`:868-883`, `status=PhaseStatus.ERROR`). No test runs `execute_sprint` over a task-bearing 429 phase to assert the in-memory `SprintResult` halt wiring — which is exactly why issue #1 slipped past the suite. | Add an `execute_sprint` integration test on a per-task phase whose factory returns a 429 fixture, asserting `result.outcome == HALTED`, `result.halt_phase == <n>`, and that `write_summary` output contains the `--model` resume line. This test FAILS today, proving issue #1. |

---

## Notes on what is genuinely solid

The five passing hand-offs are tight: the 4-hop CLI flag, the shared detector/completion-evidence core (single source, no fork), the P6 event emits (arg/param shapes match, counters are the loop's own), the nominator double-exclusion, and the entire single-session halt-UX chain are all correctly wired with matching names and types. The defect is localized: one missing 2-line state assignment on the per-task branch, and the test gap that hid it. The persisted-JSON half of the contract works on both paths; only the in-memory `SprintResult` half is broken on the per-task path.

## QA Complete
