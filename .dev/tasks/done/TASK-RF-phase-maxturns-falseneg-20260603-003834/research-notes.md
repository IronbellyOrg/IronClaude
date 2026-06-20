# Research Notes: Fix per-task `error_max_turns` false-negative phase failure in sprint executor

**Date:** 2026-06-03
**Scenario:** A (explicit — driving diagnosis is the troubleshoot REPORT.md)
**Depth Tier:** Quick
**Track Count:** 1

**Source diagnosis:** `/config/workspace/TUIBBS-scp/.dev/troubleshoot/phase6-gate-error-20260603/REPORT.md`
**Fix repo (source of truth):** `/config/workspace/IronClaude/` → `src/superclaude/cli/sprint/`

---

## EXISTING_FILES

- `src/superclaude/cli/sprint/executor.py` — sprint phase/task execution. Key symbols (line numbers confirmed 2026-06-03):
  - `execute_phase_tasks()` @927 — per-task delegation loop. Per-task status set @1016-1020: `exit 0 → PASS`, `exit 124 → INCOMPLETE`, `else → FAIL`. **This is the defect site** — no `error_max_turns` reclassification.
  - `_run_task_subprocess()` @1076 — returns `(exit_code, turns_consumed, output_bytes)`; does NOT currently return/expose the per-task output-file path the classifier would need.
  - phase aggregation @1278-1279: `all_passed = all(r.status == TaskStatus.PASS ...)` then `status = PhaseStatus.PASS if all_passed else PhaseStatus.ERROR`, `exit_code = 0 if all_passed else 1`.
  - `_determine_phase_status()` @2067 — the per-PHASE path that ALREADY does the right thing: `exit_code != 0` → `detect_prompt_too_long` → INCOMPLETE; checkpoint inference `_check_checkpoint_pass` → PASS_RECOVERED; `detect_error_max_turns` → INCOMPLETE. **This is the reference implementation to mirror.**
  - `run_post_task_wiring_hook()` @458 — can already flip task → FAIL (@570) or PASS (@596); orthogonal to this fix.
- `src/superclaude/cli/sprint/monitor.py` — `detect_error_max_turns(output_path)` @37, `detect_prompt_too_long(...)` @64. The detector to call from the per-task path.
- `src/superclaude/cli/sprint/models.py` — `TaskStatus` enum (PASS/FAIL/INCOMPLETE/SKIPPED), `PhaseStatus` enum (PASS/ERROR/INCOMPLETE/PASS_RECOVERED/...). Confirm whether a per-task "recovered/incomplete-but-complete" status already exists or whether phase aggregation must treat INCOMPLETE specially.
- `src/superclaude/cli/sprint/config.py` — `SprintConfig`, `max_turns` (default 100), `output_file(phase)` path helper. Need the per-TASK output path convention used to write `results/phase-N-task-TID-output.txt`.

## PATTERNS_AND_CONVENTIONS

- **Source-of-truth sync:** `src/superclaude/` is canonical; `make sync-dev` copies `src/` → `.claude/`; `make verify-sync` must pass before commit. Fix MUST be made in `src/`.
- **Test layout:** `tests/sprint/` (unit), `tests/integration/`. `execute_phase_tasks` is testable via the `_subprocess_factory` injection seam (a callable returning `(exit_code, turns, output_bytes)`) — see `execute_phase_tasks` signature @927 and existing `tests/sprint/test_*` that exercise it.
- **Gates:** `make lint`, `make test` (UV-based: `uv run pytest`). Per global CLAUDE.md: UV only, feature branch only, never commit to main.
- The per-phase recovery path is the in-repo precedent for the exact semantics wanted (distinguish "overran AFTER completing" → recover, vs "overran WITHOUT a result" → INCOMPLETE/HALT).

## GAPS_AND_QUESTIONS

1. Does `_run_task_subprocess` (or its caller) already know the per-task output-file path on disk? If not, it must be threaded out so the classifier can call `detect_error_max_turns(path)`. (Researcher 1.)
2. Does `execute_phase_tasks` have access to a per-task result/evidence file to implement a `PASS_RECOVERED`-equivalent (work-done check), or should `error_max_turns` simply map to INCOMPLETE and let phase aggregation decide? (Researcher 1 + 2.)
3. How does phase aggregation @1278-1279 treat a non-PASS-but-not-FAIL task (INCOMPLETE)? Today only `== PASS` counts as passed, so INCOMPLETE still fails the phase. The fix likely needs to also adjust the `all_passed` predicate or introduce a `PASS_RECOVERED` task status. (Researcher 1.)
4. Existing test patterns for injecting `error_max_turns` exit codes via `_subprocess_factory`. (Researcher 3.)

## RECOMMENDED_OUTPUTS

- `research/01-target-code-executor.md` — exact current code of execute_phase_tasks, _run_task_subprocess, phase aggregation; output-file-path availability; TaskStatus/PhaseStatus enums.
- `research/02-reference-recovery-and-conventions.md` — _determine_phase_status + detect_error_max_turns + checkpoint inference (the pattern to mirror); project sync/test/lint conventions.
- `research/03-tests-and-template.md` — executor test patterns (_subprocess_factory), MDTM template 02, prior TASK-RF examples.

## SUGGESTED_PHASES

- Researcher 1 (File Inventory / target code): `src/superclaude/cli/sprint/executor.py` (@927, @1016-1020, @1076, @1278-1279) + `models.py` enums + `config.py` output-path helper. Document exact code + whether per-task output path is reachable.
- Researcher 2 (Patterns / reference recovery): `_determine_phase_status` @2067, `monitor.py` detectors, `_check_checkpoint_pass`/`_check_contamination`; + project conventions (Makefile sync/lint/test, CLAUDE.md rules).
- Researcher 3 (Test & Template): `tests/sprint/` executor tests using `_subprocess_factory`; `.claude/templates/workflow/02_mdtm_template_complex_task.md`; prior `TASK-RF-*` examples in `.dev/tasks/to-do/`.

## TEMPLATE_NOTES

- **MDTM template 02 (complex)** — the fix involves discovery (confirm output-path reachability), code change across 2-3 files (executor.py, possibly models.py, _run_task_subprocess signature), unit tests, and verification gates (lint/test/sync). PER_PHASE-ish but small; FINAL_ONLY QA acceptable. Tier Quick.
- TESTING_REQUIREMENTS: UNIT (new test asserting an `error_max_turns` task that completed its work does NOT fail the phase).
- VALIDATION_REQUIREMENTS: `make lint`, `uv run pytest tests/sprint/`, `make verify-sync` all pass.

## AMBIGUITIES_FOR_USER

- **Recovery vs INCOMPLETE policy:** Two valid fix shapes — (a) map `error_max_turns` → INCOMPLETE and additionally make phase aggregation tolerant of a completed-but-overran task (requires a `PASS_RECOVERED` task status + evidence/result check), or (b) the minimal change: treat `error_max_turns` as INCOMPLETE and decide whether INCOMPLETE should fail the phase. The task file will present option (a) (mirrors the per-phase `PASS_RECOVERED` precedent, the faithful fix) as primary and document (b) as the minimal alternative, leaving final policy choice to the executor at implementation time.
- Otherwise intent is clear from the REPORT.md diagnosis.
