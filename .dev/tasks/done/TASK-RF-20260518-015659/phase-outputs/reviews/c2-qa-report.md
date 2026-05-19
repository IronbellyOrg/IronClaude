# QA Report — task-integrity (C2)

**Topic:** C2 — per-task output/error file helpers + `_run_task_subprocess` migration
**Date:** 2026-05-18
**Phase:** task-integrity
**Fix cycle:** N/A (initial pass)
**fix_authorization:** false (report-only)

---

## Overall Verdict: PASS

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Existing `output_file`/`error_file` byte-identical to baseline (Q2 invariant) | PASS | `models.py:470-474` — bodies are exactly `return self.results_dir / f"phase-{phase.number}-output.txt"` and `…-errors.txt`; no docstring, no signature drift |
| 2 | New helpers follow existing method style | PASS | `models.py:476-480` — same 4-space indentation, no docstring (matches local style), `-> Path` return type, single-line body, forward-ref `"TaskEntry"` string |
| 3 | Path format `phase-{N}-task-{task_id}-output.txt` / `-errors.txt` | PASS | `models.py:477`: `f"phase-{phase.number}-task-{task.task_id}-output.txt"`; `models.py:480`: same with `-errors.txt`. Format string is verbatim — no fabrication |
| 4a | Executor migration limited to `_run_task_subprocess` (1086-1115) | PASS | `executor.py:1101` uses `config.task_output_file(phase, task)`; `:1102` uses `config.task_error_file(phase, task)`; `:1112` uses `config.task_output_file(phase, task)`. All 3 swaps present |
| 4b | Per-phase `ClaudeProcess(config, phase, env_vars=...)` at executor.py:1324 NOT modified | PASS | `executor.py:1324`: `proc_manager = ClaudeProcess(config, phase, env_vars=_phase_env_vars)` — unchanged from baseline |
| 4c | Sprint subclass `process.py:108-122` NOT modified | PASS | `sprint/process.py:108-121`: still calls `super().__init__(output_file=config.output_file(phase), error_file=config.error_file(phase), ...)` — phase-scoped paths preserved |
| 5 | Integration test uses verbatim `sys.executable -c "import sys; sys.stdout.write(sys.stdin.read())"` stand-in | PASS | `tests/pipeline/test_process.py:272-276` — identical pattern to the canonical `:179-183` and `:158-160` stand-in |
| 6 | Integration test load-bearing on C2 | PASS | `test_process.py:267-268` asserts `out_a != out_b` and `err_a != err_b` from `config.task_output_file()` BEFORE subprocesses run — if C2 helper returned phase-scoped paths, this would fail at line 267 before any process starts |
| 7a | Mock-capture test patches `pipeline.process.ClaudeProcess.__init__` (base class) | PASS | `test_executor.py:1542` — patches `"superclaude.cli.pipeline.process.ClaudeProcess.__init__"`, the base, not the sprint subclass |
| 7b | Mock-capture test pre-populates `_process`/`_stdout_fh`/`_stderr_fh` | PASS | `test_executor.py:1529-1531`: `self._process = MagicMock(returncode=0)`; `self._stdout_fh = None`; `self._stderr_fh = None` |
| 7c | Mock-capture test asserts kwarg replacements AND C3 timeout consistency | PASS | `test_executor.py:1558-1571`: asserts `output_file == config.task_output_file`, `error_file == config.task_error_file`, NEGATIVE assertions against phase-scoped, AND `timeout_seconds == config.max_turns * 120 + 300` (C3 canonical) |
| 8a | No C1 scope creep (startup_stall_timeout unchanged) | PASS | `models.py:370`: `startup_stall_timeout: int = 300` — present and unchanged, no C1 watchdog split made in C2 changes |
| 8b | No C3 scope creep (executor.py:86 unchanged) | PASS | `executor.py:86`: `timeout_seconds=self._config.max_turns * 120 + 300` — unchanged. (C2 also preserves this formula at `executor.py:1106` per the migration) |
| 8c | No C4 scope creep (per-task `write_phase_start` insertion unchanged) | PASS | `grep write_phase_start executor.py`: only 2 hits, at `:1264` (per-task branch, C4 territory) and `:1329` (per-phase). Neither is inside `_run_task_subprocess` (1086-1115). C2 did not touch them |
| 9 | Live pytest 5/5 PASS | PASS | `uv run pytest …` output: `5 passed in 0.17s`. All five test IDs verified by name in collected list |

## Summary
- Checks passed: 15 / 15
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization=false)

## Issues Found
_None._

## Confidence

**Verified:** 15/15 | **Unverifiable:** 0 | **Unchecked:** 0 | **Confidence:** 100.0%

**Tool engagement:** Read: 7 | Grep/Bash-grep: 4 | Bash (pytest): 1

Each tool call mapped to a specific check:
- `Read models.py` → checks 1, 2, 3, 8a
- `Read executor.py:1080-1130` → check 4a
- `Read executor.py:1315-1330` → check 4b
- `Read sprint/process.py:100-130` → check 4c
- `Read executor.py:80-92` → check 8b
- `Grep write_phase_start` → check 8c
- `Read test_models.py:1050-1095` → 3 helper tests structure
- `Read test_process.py:230-304` → checks 5, 6
- `Read test_process.py:155-194` → check 5 (canonical stand-in baseline)
- `Read test_executor.py:1505-1572` → checks 7a, 7b, 7c
- `Bash uv run pytest` → check 9 (live execution)

## Adversarial Findings Pursued (all cleared)

I deliberately tried to falsify the bundle:

1. **Did the new helpers leak a docstring or wrong return type?** No — single-line bodies, `-> Path` returned, style matches neighbors `output_file`/`error_file` exactly.
2. **Did the bundle misreport line numbers?** Bundle claimed insertion between L473 and L478; actual placement is L476-480 (helpers) with `result_file` at L482. Existing helpers are at L470 and L473, not L472-476 as bundle claimed. Line-number drift in the bundle's prose, but the **structural placement is correct** (between `error_file` and `result_file`) — this is a bundle prose discrepancy, not a code defect.
3. **Did the migration miss any reference to phase-scoped paths within `_run_task_subprocess`?** Re-read 1086-1115: 3 reference sites at 1101, 1102, 1112 — all swapped. No additional references in that block.
4. **Did the mock-capture test forget to populate any attribute that `_run_task_subprocess` reads post-init?** `_run_task_subprocess` reads `proc._process.returncode` at L1111. Test populates `_process = MagicMock(returncode=0)`. Also touches `_stdout_fh`/`_stderr_fh` defensively. The post-init code path is satisfied — confirmed by the live PASS.
5. **Could the cross-contamination guards (`"BBB" not in text_a`) trivially pass if both files were empty?** No — earlier assertions `text_a == "AAA"` and `text_b == "BBB"` force non-empty content of the expected value before the cross-guard runs.
6. **Did C2 accidentally drift the per-phase `process.py` subclass?** Verified `process.py:108-122` is unchanged — `super().__init__` still uses `config.output_file(phase)` and `config.error_file(phase)`.

## Recommendations

- **Minor (advisory):** The input bundle's prose line-number references (e.g. "inserted between `error_file` (L473) and `result_file` (L478)") are slightly off from the actual file (helpers are at L476-480; existing methods at L470/L473; result_file at L482). The structural claim is correct; only the literal line numbers are stale. Consider regenerating the bundle's prose against current file state if it will be used as a reference. **Not a C2 code defect — does not affect the verdict.**

## QA Complete

---

VERDICT: **PASS**
