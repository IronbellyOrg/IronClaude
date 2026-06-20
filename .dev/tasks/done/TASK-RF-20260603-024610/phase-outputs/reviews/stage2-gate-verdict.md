# Stage 2 — rf-qa task-integrity Gate Verdict

**Phase:** task-integrity (Stage 2 / Phase 4, Steps 4.1–4.9)
**Date:** 2026-06-03
**Mode:** ADVERSARIAL — zero-trust; every fact re-derived by reading source on disk.
**fix_authorization:** true

---

## Overall Verdict: PASS

All 7 criteria verified PASS against actual source on disk. The Stage-2 resume
contract (H5 skip predicate + phase-qualified key + `--resume` CLI surface +
M5 back-compat degradation + L3 crash-consistency authority) is correctly
implemented. 10/10 Stage-2 tests pass; `make lint` clean; the only suite
failures are the 2 pre-existing `.stdin` baseline failures (confirmed by
signature, NOT regressions). Zero defects found; zero fixes required.

---

## Per-Criterion Checklist

### 1. Skip predicate (H5 item 1) — PASS

`is_validated_success` (`handoff.py:23-40`) returns True ONLY when
`record.status == TaskStatus.PASS.value` (line 34 early-returns False otherwise)
AND `GateOutcome(record.gate_outcome).is_success` (line 37). `GateOutcome.is_success`
(`models.py:71-73`) is True only for `GateOutcome.PASS`, so PASS-with-gate
fail/deferred/pending all return False. Every non-PASS `TaskStatus`
(FAIL_TERMINAL/FAIL_RECOVERABLE/INCOMPLETE/SKIPPED) returns False at line 34.
No None/dict branch: `gate_outcome` is always a `.value` string (the
`from_task_result` constructor at `models.py:369` derives it from
`result.gate_outcome.value`, never None/dict). The bare `ValueError` guard
(lines 38-40) defensively maps an unrecognized string to False — strictly
tighter than the contract, never looser.
Test `test_resume_contract.py:55-70` exhaustively pins all 8 status×gate cases.
**Evidence: handoff.py:34,37; models.py:71-73,369.**

### 2. Skip before budget debit + correct satisfied representation — PASS (CRITICAL sub-check verified)

The resume skip-check (`executor.py:1015-1034`) sits at the TOP of the
`for i, task in enumerate(tasks)` loop body (loop opens at line 999), BEFORE the
`can_launch` budget gate (line 1037) and BEFORE the `ledger.debit` pre-allocation
(line 1052-1053). A skipped task hits `continue` (line 1034) and never reaches
the debit — confirmed by `test_resume_contract.py:111` asserting
`ledger.consumed == ledger.minimum_allocation` (exactly ONE task's debit for the
one re-run, zero for the skip).

CRITICAL representation check: the skipped task is recorded as
`TaskResult(status=TaskStatus.PASS, gate_outcome=GateOutcome.PASS, turns_consumed=0)`
(`executor.py:1022-1033`). This is the CORRECT choice, NOT SKIPPED:
- `rerun_tasks._is_satisfied` (`rerun_tasks.py:453-460`) keys on
  `tr.status.is_success`, which is True ONLY for `TaskStatus.PASS`
  (`models.py:54-56`). A SKIPPED-status result would return False → dependents
  would be wrongly treated as unsatisfied.
- The pre-RC.1 inline `all_passed` aggregation (`executor.py:1441`) is
  `all(r.status == TaskStatus.PASS for r in task_results)`. A SKIPPED result
  would flip the phase to `PhaseStatus.ERROR` (line 1442).
Recording PASS makes both oracles treat the resumed-skip task as done, exactly
as the inline comment (`executor.py:1004-1007`) states. A SKIPPED-status result
WOULD have been mis-treated — the implementation correctly avoids that trap.
**Evidence: executor.py:999,1015-1034,1037,1052-1053,1441-1442;
rerun_tasks.py:453-460; models.py:54-56,71-73.**

### 3. `--resume` three layers — PASS

- Layer 1 (CLI): `commands.py:196-201` defines `@click.option("--resume",
  "resume_task_id", default="", ...)`; `run()` accepts `resume_task_id: str`
  (line 221) and passes it to `load_sprint_config(resume_task_id=resume_task_id)`
  (line 259).
- Layer 2 (loader): `config.py:281,296` — `load_sprint_config(...,
  resume_task_id: str = "")` forwards it into `SprintConfig(...,
  resume_task_id=resume_task_id)` (line 366).
- Layer 3 (config field): `models.py:580` — `resume_task_id: str = ""` on
  `SprintConfig`, all three layers defaulting to `""`.
Composition with `--start/--end` is documented at `models.py:575-579` (phase
range bounds the slice; validated-success skip suppresses done tasks within it)
and in the `--resume` help string (`commands.py:200`).
**Evidence: commands.py:196-201,221,259; config.py:281,296,366; models.py:575-580.**

### 4. resume_command reconciliation — PASS

- `build_resume_output` (`models.py:974-1028`) emits the resume command at
  line 1007: `superclaude sprint run {config.index_path} --resume {halt_task_id}
  --max-turns {budget_suggestion}`. The non-existent `--budget` is GONE —
  replaced by `--max-turns` (a real flag, `commands.py:89`). `--resume` is the
  real flag (`commands.py:197`). Grep for `--budget` across the entire sprint
  CLI returns ZERO matches (exit 1).
- `SprintResult.resume_command` (`models.py:807-814`) emits
  `--start {self.halt_phase} --end {end}` — both real click flags
  (`commands.py:75,82`).
All printed resume commands use only real `sprint run` flags.
**Evidence: models.py:1007,807-814; commands.py:75,82,89,197; grep --budget = no match.**

### 5. Back-compat degradation (H5/M5) — PASS

The skip-check guard (`executor.py:1015-1019`) is a 3-way AND:
`handoff_store is not None AND getattr(config,"resume_task_id","") AND
(config.results_dir / "handoff").exists()`. A missing `handoff/` dir
short-circuits the third clause → the entire skip block is bypassed → NO
per-task skipping, NO error, phase-granular behavior (every task runs the normal
path). `FileHandoffStore.read` (`handoff.py:62-71`) checks `path.exists()` and
returns `None` WITHOUT any mkdir — no lazy directory creation on read.
`handoff/` is created lazily ONLY on first write
(`FileHandoffStore.write`, `handoff.py:57`: `path.parent.mkdir(parents=True,
exist_ok=True)`). The dir-`exists()` check at `executor.py:1018` short-circuits
before any read.
Tests `test_resume_backward_compat.py:43-66` (no dir → all tasks run, no error)
and `:69-81` (read on missing dir → None, dir NOT created) both pass.
**Evidence: executor.py:1015-1019; handoff.py:57,62-71.**

### 6. Crash-consistency (L3) — PASS

`test_handoff_crash_consistency.py:47-91` constructs the exact asymmetric state:
it writes a validated-success `HandoffRecord` atomically via
`store.write` (lines 56-68) but emits NO `task_complete` journal event, then
asserts the asymmetry (handoff file present at line 71; no `task_complete` in the
JSONL at lines 73-77). It then drives `execute_phase_tasks` with a tracking
`_subprocess_factory` and asserts `ran == []` (line 90) — i.e. resume honored the
handoff file and skipped, treating it (not the JSONL) as authoritative — plus
`results[0].status == TaskStatus.PASS` (line 91). This exercises the real
skip-check at `executor.py:1015-1034`, which keys solely on the handoff
file via `handoff_store.read` and `is_validated_success`, never on the JSONL.
Test passes.
**Evidence: test_handoff_crash_consistency.py:47-91; executor.py:1015-1034.**

### 7. No-regression + lint — PASS

Independently re-ran (not trusting the summary):
- `uv run pytest test_resume_contract.py test_handoff_crash_consistency.py
  test_resume_backward_compat.py test_handoff_store.py -q` → **10 passed**.
- `make lint` (`uv run ruff check .`) → **"All checks passed!"** exit 0.
- Re-ran the 2 overlapping `test_multi_phase.py` failures
  (`test_three_phase_happy_path`, `test_halt_at_phase_three`) → both fail with
  `AttributeError: '_PassPopen' object has no attribute 'stdin'` — the EXACT
  pre-existing `.stdin` baseline root cause (`pre-change-baseline.md:31`,
  reached via the Path A single-session fallback, unrelated to the Path B resume
  code this stage wires). These are NOT regressions per the
  `pre-change-baseline.md:96-99` rule.
Known High follow-up (ruff-FORMAT version skew, local 0.15.14 vs CI) is NOTED
only — `make lint` (ruff check) is the task bar and is green. Per gate
instruction, the gate is NOT failed on ruff-format version skew, and no blanket
`ruff format` change was introduced.
**Evidence: pytest 10 passed; ruff check clean; multi_phase signature = `_PassPopen ... 'stdin'`; pre-change-baseline.md:31,96-99.**

---

## Issues Found

None. Zero defects across all 7 criteria. No fixes applied (fix_authorization
was available but unused — no real defect to fix).

## Actions Taken

None required. The implementation is correct as shipped.

## No-Regression Note

Independently confirmed: the only failures in the touched/overlapping suites are
the 2 pre-existing `.stdin` harness-double baseline failures in
`test_multi_phase.py`, both verified by the `AttributeError: '_PassPopen' object
has no attribute 'stdin'` signature matching `pre-change-baseline.md`. They reach
the broken `start()` path through the Path A single-session fallback, which is
orthogonal to the Path B per-task resume code wired in Stage 2. `make lint` is
clean. No new failure, no baseline failure flipping for a new reason.

## Confidence

Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool engagement: Read: 14 | Grep: 6 | Glob: 0 | Bash: 6
(Tavily/web: not applicable — all claims were source-local; no external lookup.)

## QA Complete
