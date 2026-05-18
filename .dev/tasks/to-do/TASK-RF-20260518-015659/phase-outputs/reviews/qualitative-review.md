# QA Report — Task Qualitative Review (G5)

**Topic:** TASK-RF-20260518-015659 — Sprint Runner Deterministic Fixes (C1 + C2 + C3 + C4)
**Date:** 2026-05-18
**Phase:** task-qualitative
**Fix cycle:** 1
**Inherited Structural Verdict:** PASS across G1 (C3), G2 (C4), G3 (C1), G4 (C2) — structural items not re-verified.

---

## Overall Verdict: PASS

All four implemented fixes (C1 watchdog split, C2 per-task helpers + migration, C3 timeout reconciliation, C4 phase_start in per-task branch) would succeed operationally if a fresh sprint were run. All 13 new tests verified passing locally (16/16 PASS when sibling pre-existing tests in the same classes are run). Ruff clean on all 10 modified files. No CRITICAL, IMPORTANT, or MINOR issues found.

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run | none | PASS | Ran `uv run pytest` on the 6 new test files/classes — 16/16 PASS in 0.21s. Ran `uv run ruff check` on the 10 modified files — `All checks passed!`. |
| 2 | Project convention compliance | none | PASS | Files edited under `src/superclaude/cli/sprint/` and `src/superclaude/cli/pipeline/` — pure Python CLI, not under `.claude/{skills,agents,commands}`. No `make sync-dev` required (correctly stated in task at L71 and spawn prompt). UV-only confirmed (no `python -m` / bare `pip` in any change). Ruff line-length 88 verified by clean ruff run. |
| 3 | Intra-phase execution order simulation | none | PASS | Walked the four fix-cluster phases in order: C3 (executor.py:86) → C4 (executor.py:1264) → C1 (models field + config + commands + watchdog branches) → C2 (helpers + migration). Each fix is independent surface; no item depends on a later one. Phase 7 validation runs after all four. C2 depends on C3's `max_turns * 120 + 300` formula being present at executor.py:1106 — verified present (executor.py:1106). |
| 4 | Function signature verification | none | PASS | Read every modified function: `SprintGatePolicy.build_remediation_step` (executor.py:62-87) returns `Step` with new `timeout_seconds=self._config.max_turns * 120 + 300` at L86. `SprintConfig` dataclass adds `startup_stall_timeout: int = 300` at models.py:370 with sentinel comment. `task_output_file`/`task_error_file` methods at models.py:476-480 with `"TaskEntry"` forward-ref annotation. `load_sprint_config` signature at config.py:275-288 adds `startup_stall_timeout: int = 300` param. `_run_task_subprocess` at executor.py:1080-1115 swaps to `config.task_output_file(phase, task)`/`config.task_error_file(phase, task)` for output_file kwarg (L1101), error_file kwarg (L1102), and size read (L1112). All call sites compatible. |
| 5 | Module context analysis | none | PASS | Read full models.py SprintConfig dataclass (L356-484): field positioned correctly between `stall_timeout` and `stall_action` per task spec; existing dataclass conventions (inline `# 0 = disabled` sentinel comment, integer default) followed. Read executor.py module — watchdog branch at L1365-1444 sits inside the per-phase poll loop (L1340+) where `proc_manager`, `ms`, `_stall_acted`, `_timed_out`, `_dbg`, `monitor` are all in scope. The inline `import sys` calls (L1383, 1396, 1422, 1434) are stylistic, but consistent with the pre-existing TUI exception handler in the same scope (L1451). |
| 6 | Downstream consumer analysis | none | PASS | (a) `startup_stall_timeout`: 4 consumers identified — dataclass field (models.py:370), `load_sprint_config` (config.py:285,347), Click decorator + run() (commands.py:139,194,225), and watchdog conditional (executor.py:1368). All 4 wired correctly. (b) `task_output_file`/`task_error_file`: only `_run_task_subprocess` consumes these (executor.py:1101,1102,1112). Per-task subprocesses use `proc.start(); proc.wait()` synchronously (L1109-1110) — they do NOT use the `OutputMonitor` poll loop, which only fires in the per-phase fallback branch (L1313). So per-task paths do not invalidate the monitor's single-tail invariant. (c) `phase_start` emission in per-task branch: `write_phase_start` at L1264 fires before `execute_phase_tasks` at L1267, which means it precedes any `phase_complete` emission at L1298 (`write_phase_result`). JSONL ordering guarantee preserved. |
| 7 | Test validity | none | PASS | All 13 new tests exercise production code, not stubs: (a) `TestStartupStallTimeoutDefaults` calls real `load_sprint_config`; (b) `TestTaskOutputFileHelpers` calls real `SprintConfig.task_output_file`/`task_error_file`; (c) `TestStartupStallWatchdog` patches `subprocess.Popen` and `OutputMonitor` to drive `execute_sprint` end-to-end through the new watchdog branch, asserting `SprintOutcome.HALTED` and `exit_code == 124`; (d) `TestClaudeProcessOutputFileCollision` is load-bearing on `config.task_output_file()` — derives paths via helper at L263-266, asserts `out_a != out_b` at L267-268 BEFORE subprocesses run, then runs real subprocesses via `sys.executable -c "import sys; sys.stdout.write(sys.stdin.read())"` and verifies no cross-contamination; (e) `test_run_task_subprocess_uses_task_output_file` captures `ClaudeProcess.__init__` kwargs and asserts both kwarg substitutions PLUS the C3 timeout formula consistency; (f) `test_phase_start_emitted_for_per_task_branch` mocks `_parse_phase_tasks`/`execute_phase_tasks`/`run_post_phase_wiring_hook` to force the per-task branch, then asserts phase_start present in the JSONL file with all 4 required fields and that it precedes phase_complete; (g) `TestTimeoutFormulaConsistency` asserts the literal canonical formula across `max_turns ∈ {1, 50, 100, 500}`. |
| 8 | Test coverage of primary use case | none | PASS | Primary use case for each fix is covered: C3 (formula consistency across multiple max_turns), C4 (per-task branch end-to-end through execute_sprint), C1 (both startup-stall and mid-stall branches exercised in isolation via mutually-exclusive stall_timeout settings), C2 (real subprocess collision test with cross-contamination guard at L302-303 of test_process.py). |
| 9 | Error path coverage | none | PASS | `startup_stall_timeout=0` disabled sentinel covered (`test_startup_stall_timeout_zero_disables`); `stall_action="kill"` vs `"warn"` paths both exist in production (executor.py:1382 / 1394 / 1421 / 1432); test exercises "kill" with expected `SystemExit(1)` and HALTED outcome. Click `type=click.Choice(["warn", "kill"])` (commands.py:148) constrains user input. |
| 10 | Runtime failure path trace | none | PASS | Traced `execute_sprint` data flow: phase loop → `_parse_phase_tasks` → tasks present? → per-task branch: `write_phase_start` → `tui.update` → `execute_phase_tasks` → `run_post_phase_wiring_hook` → `write_phase_result` → `tui.update`. The added `write_phase_start` call at L1264 is structurally identical to the per-phase branch call at L1329 (same signature, same args). No new failure mode introduced. |
| 11 | Completion scope honesty | none | PASS | Task documents 3 deferred items (C5 --no-session-persistence, C6 axis-fan-out, C7 per-task watchdog coverage) in Follow-Up Items section — explicitly out of scope. All 4 phase gate verdicts (G1 PASS cycle 1, G2 PASS cycle 1, G3 PASS cycle 1, G4 PASS cycle 1) recorded as PASS with no falsified verdicts. Open Questions Q1 ("warn" default kept), Q2 (additive helpers — existing output_file unchanged), Q4 (`stall_timeout=0` default kept) all resolved with documented invariants and verified by tests. |
| 12 | Ambient dependency completeness | none | PASS | `startup_stall_timeout` wired through ALL touchpoints: dataclass field, config loader, Click option, run() parameter, run() pass-through, executor consumer. `task_output_file`/`task_error_file` consumers verified (single consumer is `_run_task_subprocess`). Imports verified: `TaskEntry` import added to `tests/sprint/test_regression_gaps.py` (per task L14 of summary). models.py uses `"TaskEntry"` forward-ref string to avoid circular import. |
| 13 | Kwarg sequencing red flags | none | PASS | No "add kwarg" items precede their corresponding "add parameter" items. `startup_stall_timeout` is added simultaneously across all 4 touchpoints. `task_output_file`/`task_error_file` helpers added in same file group before any caller uses them. |
| 14 | Function existence claims require verification | none | PASS | Grep-verified: `build_remediation_step` exists at executor.py:66 (dead code with zero production callers — verified: only construction at L1216 is a `__init__` side-effect, result discarded); `output_file`/`error_file` methods exist at models.py:470/473; `task_output_file`/`task_error_file` exist at models.py:476/479; `write_phase_start` exists at logging_.py:59; `_run_task_subprocess` exists at executor.py:1080; `OutputMonitor.reset` exists at monitor.py:293. |
| 15 | Cross-reference accuracy for templates | none | PASS | Task references MDTM template 02 — verified at `.claude/templates/workflow/02_mdtm_template_complex_task.md`. All research files referenced in `related_docs` (research-notes.md, 01-file-inventory.md … 05-test-and-verification.md) physically exist and are byte-readable. |

## Summary
- Checks passed: 15 / 15
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 0
- Issues fixed in-place: 0
- Tool engagement: Read: 16 | Grep: 9 | Bash: 4

## Confidence Gate

- Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Tool engagement: Read: 16 | Grep: 9 | Bash: 4 | Glob: 0 (total tool calls ≥ checklist items — satisfies engagement minimum)

## Targeted-Check Resolutions (from spawn prompt)

(a) **All 4 QA_GATE_REQUIREMENTS:PER_PHASE gates encoded.** Verified G1 (C3, task L183-203), G2 (C4, L215-235), G3 (C1, L263-283), G4 (C2, L307-327) are checklist items with both spawn steps (`Gx.2`) and conditional-proceed steps (`Gx.3`). All 4 ran PASS cycle 1 per the verdict files in `phase-outputs/plans/`.

(b) **Watchdog branches are functionally mutually exclusive.** Branch A (startup-stall, executor.py:1367-1403) is gated on `ms.events_received == 0`; Branch B (mid-stall, executor.py:1406-1440) is gated on `ms.events_received > 0`. The two predicates partition the integer domain of `events_received` (which is monotonically non-decreasing). The shared `_stall_acted` single-fire guard prevents double-fire even during the integer transition tick where `events_received` becomes >0 — because once either branch fires, `_stall_acted=True` and neither branch can re-fire until the reset clause at L1443 (`if _stall_acted and ms.stall_seconds == 0.0: _stall_acted = False`). The integer transition `0 → >0` is atomic from the watchdog's perspective (single poll-tick observation), so no race window exists. **Adversarial check passed.**

(c) **Per-task paths do not invalidate OutputMonitor's single-tail assumption.** `OutputMonitor` is only used in the per-phase fallback branch (`monitor.reset(output_path, phase_file=phase.file)` at executor.py:1313). The per-task branch at L1262-1300 invokes `execute_phase_tasks` which calls `_run_task_subprocess` (L1080) for each task. `_run_task_subprocess` uses `proc.start(); proc.wait()` synchronously (L1109-1110) — there is no `OutputMonitor` instantiation in the per-task path. The per-task output paths (`phase-{N}-task-{task_id}-output.txt`) are consumed only by a one-shot `output_path.stat().st_size` read at L1113. Single-tail concern is moot.

(d) **`phase_start` emission precedes `phase_complete`.** At executor.py:1262-1300, the order is: L1263 `started_at = datetime.now(timezone.utc)` → L1264 `logger.write_phase_start(phase, started_at)` → L1267 `execute_phase_tasks(...)` (synchronous, blocks until tasks complete) → L1280-1295 `PhaseResult` construction + `run_post_phase_wiring_hook` → L1298 `logger.write_phase_result(phase_result)` (emits `phase_complete`). `write_phase_start` is line 1264; `write_phase_result` is line 1298. JSONL append order guaranteed by line ordering and the fact that `SprintLogger` writes synchronously to the file.

(e) **C3 dead-code change is risk-free.** `grep -rn "build_remediation_step" src/` shows only the definition at executor.py:66 and an unrelated definition at pipeline/trailing_gate.py:254 (the BASE class). `grep -rn "SprintGatePolicy" src/` shows only the class definition at executor.py:56 and a single construction site at executor.py:1216 (`SprintGatePolicy(config)` — instance immediately discarded, comment at L1213-1215 documents that this is for test-side `__init__` patching only). No production caller invokes `build_remediation_step`. Confirmed dead code; formula change has zero blast radius outside the new test class.

(f) **C2 collision test is load-bearing on the helper.** `tests/pipeline/test_process.py::TestClaudeProcessOutputFileCollision` derives paths via `config.task_output_file(phase, task_a)` and `config.task_output_file(phase, task_b)` at L263-264, NOT hand-supplying paths. The test asserts `out_a != out_b` at L267 — if the helper regressed to a phase-only naming, this assertion would FAIL before any subprocess ran. Real-subprocess execution with cross-contamination guards at L302-303 (`assert "BBB" not in text_a` and `assert "AAA" not in text_b`) provides end-to-end coverage.

(g) **Pre-existing `.stdin AttributeError` workaround correct.** Both `_StartupStallPopen` (test_watchdog.py:294-308) and `_MidStallPopen` (test_watchdog.py:376-390) set `self.stdin = MagicMock()` in `__init__`. This is the documented workaround for the pre-existing commit-4799719 issue. The MagicMock does not mask any real bug because the watchdog code path under test does not write to stdin — it only reads `proc_manager._process.poll()`, `pid`, and `returncode`. The MagicMock satisfies attribute access without altering the watchdog's observable behavior.

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)

The spawn prompt declared rf-qa task-integrity PASS across G1/G2/G3/G4. I relied on the structural verdicts (section numbering, byte-exact match of inserted lines, scope-creep absence, indentation match) and applied my own tool engagement to the semantic counterparts below:

- Relied on rf-qa PASS for **G1 (C3 byte-exact formula match)** → semantic counterpart verified: I independently grepped `build_remediation_step` callers and confirmed dead-code claim (zero production callers, only test-side construction at executor.py:1216) — this is a semantic check (does the change interact with live code?) that goes beyond rf-qa's byte-match assertion.
- Relied on rf-qa PASS for **G2 (C4 insertion byte-exact match)** → semantic counterpart verified: I independently traced the per-task branch flow at executor.py:1262-1300 to confirm `write_phase_start` precedes `execute_phase_tasks` (JSONL ordering invariant), and that the per-phase branch at L1329 is untouched.
- Relied on rf-qa PASS for **G3 (C1 mutually-exclusive watchdog branches)** → semantic counterpart verified: I independently reasoned through the integer domain partition of `events_received` (0 vs >0) and the single-fire `_stall_acted` guard to prove no double-fire across the `0 → >0` transition tick.
- Relied on rf-qa PASS for **G4 (C2 additive helpers, byte-unchanged output_file/error_file)** → semantic counterpart verified: I independently traced the OutputMonitor consumer in monitor.py (only `monitor.reset(output_path, ...)` at executor.py:1313, which is per-phase only) and confirmed `_run_task_subprocess` uses synchronous `proc.start(); proc.wait()` with no monitor instantiation — so the new per-task paths don't invalidate the single-tail invariant.

Reliance is not verification. For each PASS item above, an independent semantic check was performed using grep and read tools against current source.

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- Relied on rf-qa PASS for **G1 (C3 byte-exact formula `max_turns * 120 + 300` match)**
- Relied on rf-qa PASS for **G2 (C4 insertion byte-exact match at executor.py:1264)**
- Relied on rf-qa PASS for **G3 (C1 watchdog split + 5 new field touchpoints byte-exact match)**
- Relied on rf-qa PASS for **G4 (C2 additive helpers + 3 kwarg-swap byte-exact match)**

**(b) Independent semantic checks (≥1 required, INV-019):**
- **Dead-code semantic check for C3** — verified by `grep -rn "build_remediation_step" src/` showing only the definition at executor.py:66 + an unrelated trailing_gate.py:254 base-class definition (no production callers), and `grep -rn "SprintGatePolicy" src/` showing only one construction site at executor.py:1216 where the instance is immediately discarded (comment at L1213-1215 documents the test-patching purpose).
- **JSONL ordering semantic check for C4** — verified by reading executor.py:1262-1300 and confirming the line ordering: `started_at` (L1263) → `write_phase_start` (L1264) → `execute_phase_tasks` (synchronous, L1267) → `write_phase_result` (L1298). Since `SprintLogger` writes synchronously, file append order matches source order.
- **Branch mutual-exclusion semantic check for C1** — verified by reading executor.py:1367-1444: branch A predicate `events_received == 0` and branch B predicate `events_received > 0` partition the integer domain; the shared `_stall_acted = True` single-fire latch on first fire and the reset clause `if _stall_acted and ms.stall_seconds == 0.0` (L1443) prevent double-fire even at the `0 → >0` boundary tick.
- **OutputMonitor single-tail invariance semantic check for C2** — verified by reading monitor.py:253-360 (only consumer is `monitor.reset(output_path, ...)`) and executor.py:1080-1115 (`_run_task_subprocess` uses `proc.start(); proc.wait()` synchronously with no `OutputMonitor` instantiation). The per-task paths from the new helpers are consumed only by a one-shot `output_path.stat().st_size` read at L1113, never tailed.
- **End-to-end test run semantic check** — independently ran `uv run pytest` on all 6 new test files/classes (16/16 PASS in 0.21s) and `uv run ruff check` on all 10 modified files (`All checks passed!`).

## Issues Found

None. The four fixes are semantically and operationally correct.

## Actions Taken

None — `fix_authorization: true` was available but no issues required fixing.

## Five Adversarial Axes — Sharpening Overlay

- **AX-1 Drift** — INACTIVE (no BUILD_REQUEST.GOAL verbatim was provided in the spawn prompt). However, the consolidated summary at `phase-outputs/reports/all-fixes-summary.md` was used as a proxy: production changes match the summary byte-for-byte (formula at executor.py:86 confirmed `max_turns * 120 + 300`; helpers at models.py:476-480 confirmed; watchdog split at executor.py:1365-1444 confirmed; `write_phase_start` at executor.py:1264 confirmed). No paraphrasing or scope narrowing detected.
- **AX-2 Contradictions** — None. All artifacts agree: task L67 says `phase-{N}-task-{task_id}-output.txt` format, models.py:477 matches; task L66 says `startup_stall_timeout: int = 300` default, models.py:370 matches, config.py:285 matches, commands.py:142 matches; task L68 says canonical formula `max_turns * 120 + 300`, executor.py:86 + 1106 + sprint/process.py:115 all match.
- **AX-3 Omissions** — None detected. All 4 QA_GATE_REQUIREMENTS:PER_PHASE gates (G1-G4) encoded; all 13 TESTING_REQUIREMENTS items implemented; ruff/pytest validation steps present (Phase 7); 3 deferred items (C5/C6/C7) explicitly documented as Follow-Up rather than silently omitted.
- **AX-4 Weakened criteria** — None. Acceptance criteria are concrete and observable: `out_a != out_b` assertion, `phase_start` event present in JSONL with 4 named fields, formula `== max_turns * 120 + 300` (literal integer comparison across 4 max_turns values), watchdog branch fires `SystemExit(1)` with `HALTED` outcome and `exit_code == 124`. No "may", "consider", or "if applicable" softening.
- **AX-5 Invented content** — None. Every file path, function name, line range, and config value referenced in the task is grep-verifiable in the current codebase. No invented Redis caches, no phantom modules, no unfounded scope inflation.

## QA Complete
