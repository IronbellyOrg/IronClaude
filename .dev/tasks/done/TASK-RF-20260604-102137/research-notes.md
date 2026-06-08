# Research Notes: Fix PASS_RECOVERED couplings in sprint rerun/handoff success predicates

**Date:** 2026-06-04
**Scenario:** A (explicit — bug, fix shape, and test approach are pinned by prior QA)
**Depth Tier:** Standard
**Track Count:** 1

---

## EXISTING_FILES

- `src/superclaude/cli/sprint/rerun_tasks.py`
  - `def _rerun_targets_passed(phase_result_json, targets) -> bool` (~line 1165 on master) — gates rerun merge-back via `all(status_by_id.get(t) == "pass" for t in targets)` (PRIMARY BUG: misses `"pass_recovered"`).
  - `last_pass` tracking (~line 1192): `if tr.status is TaskStatus.PASS: last_pass = tr.task.task_id` (SECONDARY, same class — display-only `last PASS task` echo; lower severity).
  - Caller `rerun_succeeded = rerun_error is None and _rerun_targets_passed(...)` (~line 1370), gates `if rerun_succeeded and merge_back:`.
  - Already imports `TaskStatus` (has other `TaskStatus.PASS` refs) → no new import needed.
- `src/superclaude/cli/sprint/handoff.py`
  - `def is_validated_success(record) -> bool` (~line 23); body `if record.status != TaskStatus.PASS.value:` (~line 34) — compares the `.value` STRING (TERTIARY, same class; resume-skip predicate).
- `src/superclaude/cli/sprint/models.py` — `TaskStatus` enum (`is_success = self in (PASS, PASS_RECOVERED)`), `TaskResult.to_dict`/`from_dict` (status string round-trip), `HandoffRecord`.
- `src/superclaude/cli/sprint/resume/planner.py` — `_coerce_task_status` (the None-safe `TaskStatus(value)` coerce-tolerant pattern to MIRROR).
- Tests: `tests/sprint/test_rerun_tasks.py`, `tests/sprint/test_rerun_tasks_failure_modes.py`, `tests/sprint/test_rerun_tasks_e2e.py`, `tests/sprint/test_handoff_record.py`.

## PATTERNS_AND_CONVENTIONS

- Coerce-tolerant status parse: mirror `resume/planner.py._coerce_task_status` (`try: TaskStatus(value) except (ValueError, TypeError): return None`), then check `.is_success` with a None guard.
- The 6 resume/ sites just fixed in PR #124 use `is not None and is_success` ("done") / `is None or not is_success` ("not done") — same idiom applies here.
- Validation discipline: UV only; `uv run python -m py_compile`; `uv run pytest tests/sprint/ -q`; BOTH `uv run ruff check src/ tests/` and `uv run ruff format --check src/ tests/` (CI runs format-check separately from `make lint` — memory `reference_make_lint_vs_ci_ruff_format.md`).

## GAPS_AND_QUESTIONS

- Exact fixture shape to construct a `phase-N-result.json` with a `"pass_recovered"` target and call `_rerun_targets_passed` (or the higher-level rerun path) — researcher 2 to pin from existing rerun tests.
- Whether `is_validated_success` (handoff.py, string `.value` compare) and `last_pass` (display-only) should be fixed in the same task or scoped out — researcher 1 to assess blast radius; builder decides inclusion.
- Whether `_rerun_targets_passed`'s `status_by_id` values are raw strings (so coerce via `TaskStatus(value)`) vs already-`TaskStatus` — researcher 1 to confirm the exact read path.

## RECOMMENDED_OUTPUTS

- `research/01-rerun-handoff-coupling-sites.md` — File Inventory: exact functions, line numbers, read/serialization path, callers, import status, blast radius of each of the 3 sites.
- `research/02-test-surface-and-fixtures.md` — Test & Verification: existing rerun/handoff test fixture builders, how to construct a pass_recovered fixture, exact assertion + RED/GREEN shape.
- `research/03-template-validation-pr-discipline.md` — Template & Examples: MDTM template 02 structure, validation command set, branch/worktree/fork-PR discipline.

## SUGGESTED_PHASES

- Researcher 1 (File Inventory): rerun_tasks.py (`_rerun_targets_passed`, `last_pass`, caller) + handoff.py (`is_validated_success`) + models.py status round-trip. Output 01.
- Researcher 2 (Test & Verification): tests/sprint/test_rerun_tasks*.py + test_handoff_record.py fixture patterns; the exact pass_recovered RED/GREEN test shape. Output 02. (Does NOT cover source-fix sites — researcher 1 does.)
- Researcher 3 (Template & Examples): MDTM template 02 + validation/PR discipline. Output 03. (Does NOT cover code — researchers 1/2 do.)

## TEMPLATE_NOTES

- Template **02** (complex): discovery (locate exact lines post any drift) → fix (per-site) → test (RED/GREEN) → full validation → commit/push/PR phases with a final QA gate.
- Tier **Standard** (3 researchers, 0 web). Scope is small but spans 3 candidate sites + tests + PR discipline.
- QA_GATE_REQUIREMENTS: PER_PHASE (template 02). VALIDATION_REQUIREMENTS: py_compile + full sprint suite + both ruff gates. TESTING_REQUIREMENTS: UNIT (RED→GREEN regression).

## AMBIGUITIES_FOR_USER

- Scope breadth: fix only `_rerun_targets_passed` (the operationally-critical merge-back gate), or all three same-class sites (+ `is_validated_success` + `last_pass`). The build request recommends evaluating all three; the builder will scope based on blast-radius research. Not a blocker — the task file will state the chosen scope explicitly with rationale.
