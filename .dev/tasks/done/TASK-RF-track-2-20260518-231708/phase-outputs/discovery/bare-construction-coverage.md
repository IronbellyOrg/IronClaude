# Bare-Construction Coverage — `tests/unit/test_reflexion.py`

**Step:** 2.6
**Timestamp:** 2026-05-19 02:32 UTC
**File:** `tests/unit/test_reflexion.py`

## (1) Call-site table (TB-Add-5 batch)

| Line | Test Name | Redirected By | Status |
|---:|---|---|---|
| 17  | `test_reflexion_initialization`            | autouse `_redirect_reflexion_writes` + env-var resolver in `ReflexionPattern.__init__` | OK |
| 25  | `test_record_error_basic`                  | autouse `_redirect_reflexion_writes` + env-var resolver in `ReflexionPattern.__init__` | OK |
| 39  | `test_record_error_with_solution`          | autouse `_redirect_reflexion_writes` + env-var resolver in `ReflexionPattern.__init__` | OK |
| 52  | `test_get_solution_for_known_error`        | autouse `_redirect_reflexion_writes` + env-var resolver in `ReflexionPattern.__init__` | OK |
| 73  | `test_error_pattern_matching`              | autouse `_redirect_reflexion_writes` + env-var resolver in `ReflexionPattern.__init__` | OK |
| 118 | `test_error_learning_across_sessions`      | autouse `_redirect_reflexion_writes` + env-var resolver in `ReflexionPattern.__init__` | OK |
| 165 | `test_reflexion_with_real_exception`       | autouse `_redirect_reflexion_writes` + env-var resolver in `ReflexionPattern.__init__` | OK |

## (2) Cwd-assertion audit

`grep -n "docs/memory\|docs/mistakes\|Path.cwd" tests/unit/test_reflexion.py` returns no matches in test bodies. None of the 7 bare-construction tests assert on `Path.cwd()`-rooted paths or hard-coded `docs/memory/` / `docs/mistakes/` substrings — so the env-var redirect to `tmp_path/docs/memory` does not break any explicit-path assertion.

(Line 100 — `test_solutions_persist_across_instances` — passes `memory_dir=temp_memory_dir` explicitly and is therefore not a bare call site; not in scope for this verification.)

## (3) Verdict

**NO CODE CHANGES required to any of the 7 call sites.** The autouse fixture (Step 2.4) plus the env-var resolver in `ReflexionPattern.__init__` (Step 2.1) redirect every bare construction to `<tmp_path>/docs/memory/` and the derived `<tmp_path>/docs/mistakes/` automatically. The TB-Add-5 batched verification is satisfied for all 7 lines.
