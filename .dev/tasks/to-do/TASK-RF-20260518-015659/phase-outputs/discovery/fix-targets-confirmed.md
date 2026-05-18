# Fix Targets Confirmed (Phase 2 Discovery)

**Date:** 2026-05-18
**Method:** Direct Read of each touchpoint via sed-numbered output (cross-verified via Read in scope-discovery turn).

| Fix | File | Line(s) (expected → actual) | Expected code excerpt (short) | Actual matches expected | Notes |
|---|---|---|---|---|---|
| (a) C1 | `src/superclaude/cli/sprint/config.py` | 284 → **285** | `stall_timeout: int = 0,` (loader kwarg) | **yes** (content) | Off-by-one; loader kwarg now at L285, `stall_action: str = "warn"` at L286. Surrounding kwargs block intact. Edit uses string matching so OK. |
| (b) C2 add-helper | `src/superclaude/cli/sprint/models.py` | 469-476 → 469-476 | `output_file(self, phase: Phase) -> Path: return ... phase-{phase.number}-output.txt`; `error_file(self, phase: Phase)`; also adjacent `result_file(self, phase: Phase)` | **yes** | Exact match. New helpers insert AFTER `error_file` (ends L473) and BEFORE `result_file` (starts L475). |
| (c) C1 dataclass mirror | `src/superclaude/cli/sprint/models.py` | 369 → 369 | `stall_timeout: int = 0  # 0 = disabled` | **yes** | Adjacent fields: `debug` (L368), `stall_action` (L370), `phase_timeout` (L371). Insert `startup_stall_timeout` BETWEEN L369 and L370. |
| (d) C3 | `src/superclaude/cli/sprint/executor.py` | 86 → 86 | `timeout_seconds=self._config.max_turns * 60,` | **yes** | Inside `build_remediation_step` method per research IP-7 (zero production callers). |
| (e) C2 migration | `src/superclaude/cli/sprint/executor.py` | 1101-1102 → **1103-1104**; size read 1112 → **1114** | `output_file=config.output_file(phase),` / `error_file=config.error_file(phase),`; size `output_path = config.output_file(phase)` | **yes** (content) | Off-by-two; lines have drifted slightly. Construction uses `ClaudeProcess.__new__` + `_Base.__init__(proc, ...)` pattern (per Researcher 1 §3). Edit uses string matching so line drift OK. |
| (f) C4 insertion point | `src/superclaude/cli/sprint/executor.py` | 1262-1300 → 1262-1300 | per-task branch: `started_at = datetime.now(timezone.utc)` at L1264 (task said ~1263), `tui.update(...)` at L1266 (task said 1265). NO `logger.write_phase_start` in this branch. | **yes** | Insertion target: between L1264 (`started_at`) and L1266 (`tui.update`) i.e. at L1265. C4 root cause CONFIRMED — branch is missing the call. |
| (g) C4 reference (untouched) | `src/superclaude/cli/sprint/executor.py` | 1328 → 1328 | `logger.write_phase_start(phase, started_at)` | **yes** | Per-phase fallback reference — DO NOT MODIFY (matches Step 4.1 instruction). |
| (h) C1 watchdog | `src/superclaude/cli/sprint/executor.py` | 1365-1404 → 1365-1404 | watchdog gated on `config.stall_timeout > 0 AND ms.stall_seconds > config.stall_timeout AND ms.events_received > 0 AND not _stall_acted`; `[WATCHDOG] Stall detected (...)` stderr; `_stall_acted` reset at L1402-1404 | **yes** | Full structure matches; both kill-and-warn branches emit `[WATCHDOG] Stall detected` (need to disambiguate to `Mid-stall detected` per Step 5.4). |
| (i) C4 emitter (untouched) | `src/superclaude/cli/sprint/logging_.py` | 59-69 → 59-69 | `def write_phase_start(self, phase, started_at): self._jsonl({"event": "phase_start", "phase": ..., "phase_name": ..., "phase_file": ..., "timestamp": ...})` | **yes** | Body is correct as-is; Step 4.1 only inserts the call, not the body. |
| (j) C2 root-cause confirmation (untouched) | `src/superclaude/cli/pipeline/process.py` | 120-123 → 120-123 | `self._stdout_fh = open(self.output_file, "w")` and `self._stderr_fh = open(self.error_file, "w")` (note also a `tool_write_mode` branch at L120-121 using `.log` suffix) | **yes** | These lines are NOT edited per Q2 — fix lives in path resolution upstream. The tool_write_mode branch is a non-issue for the C2 fix. |

## SUMMARY

**All 10 targets confirmed: YES.**

**Line drift detected (cosmetic, content matches):**
- (a) `config.py` loader kwarg drifted +1 line (284 → 285). Edit uses literal string `stall_timeout: int = 0,` so drift is harmless.
- (e) `executor.py` `_run_task_subprocess` collision drifted +2 lines (1101-1102 → 1103-1104; size read 1112 → 1114). Edit uses literal string so drift is harmless.
- (f) `executor.py` per-task branch drifted +1 line for `started_at` (1263 → 1264) and `tui.update` (1265 → 1266). C4 insertion target is between L1264 and L1266 (line L1265 is the comment line `# Signal TUI that this phase is now active`).

**Critical confirmations:**
- C4 root cause: the per-task branch at L1262-1300 has NO `logger.write_phase_start` call. Only L1328 (per-phase fallback) has it. CONFIRMED — fix is correct shape.
- C2 collision: `_run_task_subprocess` at L1086-1115 writes both stdout and stderr to phase-scoped paths via `config.output_file(phase)` / `config.error_file(phase)`. CONFIRMED.
- C3 dead code: `build_remediation_step` at L82+ uses divergent `max_turns * 60`. CONFIRMED.
- C1 watchdog: single branch with `events_received > 0` guard. CONFIRMED — needs splitting per Step 5.4.

Proceeding to Phase 3 (C3) — drift adjustments will be handled implicitly by literal-string Edit operations.
