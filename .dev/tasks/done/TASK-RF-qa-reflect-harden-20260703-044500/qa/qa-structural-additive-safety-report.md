# QA Report — Task Integrity (Additive-Safety, Structural Lens)

**Topic:** FX3 + FX5 test artifacts for PR #209 RF-QA/reflect hardening (Phase 2)
**Date:** 2026-07-03
**Phase:** task-integrity (lens: additive-safety-structural)
**Fix cycle:** N/A (fix_authorization: false — REPORT ONLY)
**Worktree:** /config/workspace/IronClaude/.dev/worktrees/pr209-harden

---

## Overall Verdict: PASS

All five additive-safety claims were independently verified against the actual
files and confirmed TRUE. Zero additive-safety violations were found. Adversarial
stance was applied (assumed >=5 violations existed and searched hard for them,
including running the suite with the additions removed to prove the additions do
not break any previously-passing test). The one red-suite condition observed
(6 pre-existing failures) was proven to pre-date and be independent of these
additions — it is OUT-OF-SCOPE, not an additive-safety violation.

---

## Items Reviewed

| # | Check (claim) | Result | Evidence |
|---|---------------|--------|----------|
| 1 | 5 existing fixtures (`load_fixture`, `mock_gh`, `mock_monitor`, `fixture_findings`, `tmp_skill_dir`) preserved byte-for-byte; FX5 appended AFTER them; only new imports added | PASS | `git diff --numstat tests/pr_submit/conftest.py` → `173 0` (173 added, **0 deleted**). `git diff … | grep '^-[^-]'` → **zero deletion lines**. Read conftest.py: all 5 fixtures intact at lines 28–89 (unchanged bodies); new imports added at lines 12–15 (`ast, inspect, re`) + 20–23 (4 gate modules); FX5 block appended lines 92–255 after `tmp_skill_dir` (ends line 89). |
| 2 | No existing pr_submit test file modified (only 3 NEW files + conftest additions) | PASS | `git status --porcelain tests/pr_submit/` → only `M conftest.py` + `?? test_gate_helper_coverage.py`, `?? test_gate_helper_differentials.py`, `?? test_setup_questions_resolution.py`. No other tracked file shows `M`. `tests/pr_submit/__init__.py` is tracked & unmodified (pre-existing). |
| 3 | No unregistered `@pytest.mark` in the 3 new files or conftest (`--strict-markers` active); parametrize via `pytest_generate_tests`/`metafunc.parametrize` is marker-free | PASS | `pyproject.toml:111` = `"--strict-markers"` in `addopts`. `grep -rn '@pytest.mark|pytest\.mark'` across all 4 files → **NO matches** (only doc-comment prose mentions the word). Parametrization done via `metafunc.parametrize` (conftest:244), which requires no marker registration. |
| 4 | FX3 imports the REAL concrete package surface (`…contract_setup.questions` / `.evidence`), NOT the lazy package facade | PASS | `test_setup_questions_resolution.py:32-33` imports `from …contract_setup import evidence as evidence_mod` and `questions as questions_mod` (concrete submodules). Facade `__getattr__` exists at `src/superclaude/pr_submit/contract_setup/__init__.py:89` but is NOT used. AST parse reads `questions_mod.__file__` (line 50) — the real source file. |
| 5 | `pytest_generate_tests` scoped by `metafunc.function.__name__` so it cannot perturb unrelated collection; coexists with the global plugin hook | PASS | conftest:243 guards with `if metafunc.function.__name__ == "test_gate_helper_has_negative_and_differential":` → no-op for every other test. Global plugin defines `pytest_collection_modifyitems` (`src/superclaude/pytest_plugin.py:206`), a **different** hook from `pytest_generate_tests`; both run without conflict. research/05 §1 (lines 32-51) confirms the pr_submit conftest previously had NO hooks and pytest invokes all registered impls of a hook. |

## Supplementary Adversarial Checks (beyond the 5 claims)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| S1 | Drift-alarm `GATE_HELPER_DEF_PATTERN` matched set over the 4 modules' module-level defs EQUALS exactly the 9 registered module-level helpers (a superset would turn the drift alarm RED on the green tree) | PASS | Executed the exact pattern via `ast` over live `candidate/lockgate/diagnosis/validation`: MATCHED COUNT = 9, `set(matched) == registered-9` → **True**, superset-extras = `[]`. Confirms the Step 2.4 "narrowed pattern = strict subset of 11-registry" claim; no self-inflicted RED. |
| S2 | All 11 registered helpers (`GATE_LOAD_BEARING_HELPERS` / `HELPER_TEST_MAP` keys) actually resolve on the live source modules | PASS | `grep 'def <name>('` confirmed all 9 module-level helpers + `required_unobserved` (candidate.py:47) + `_negative_control_checks`. Referenced symbols also exist: `STATE_POLLING` (classifier.py:23), `classify`/`CheckResult` (validation.py:18), `_check` (lockgate.py:71). |
| S3 | The 3 new test files pass green (additions are valid, not RED stubs) | PASS | `uv run pytest` on the 3 files → **37 passed** (4 FX3 + 22 FX5 differential/negative + 11 FX5 coverage-parametrized). |
| S4 | Additions do NOT break any previously-passing test (core additive-safety proof) | PASS | Full `tests/pr_submit/` run → `6 failed, 311 passed`. Re-ran the 2 affected files with conftest change stashed AND the 3 new files moved out → **identical `6 failed, 12 passed`**. The 6 failures pre-exist and are caused by a missing unrelated file `src/superclaude/hooks/scripts/offer-pr-review.sh` (`FileNotFoundError` in `test_static_grep`/`test_hook_update`), NOT by FX3/FX5. Working tree restored cleanly afterward. |

## Summary

- Checks passed: 5 / 5 primary + 4 / 4 supplementary = 9 / 9
- Checks failed: 0
- Critical issues: 0
- Additive-safety violations: 0
- Issues fixed in-place: N/A (fix_authorization: false)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| — | INFO / OUT-OF-SCOPE | `tests/pr_submit/test_hook_update.py`, `tests/pr_submit/test_static_grep.py` | 6 pre-existing suite failures (missing `src/superclaude/hooks/scripts/offer-pr-review.sh`). PROVEN independent of this task's additions (same failures with additions removed). Not an additive-safety violation; noted only so the operator knows `make test` for this package is currently red for an unrelated reason. | Out of scope for FX3/FX5 additive hardening — do not fix here. Track separately if the missing hook script is expected to exist. |

## Confidence Gate

- **Confidence:** Verified: 9/9 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 5 | Grep: 6 | Glob: 0 | Bash: 8 (git diff/status, grep configs, symbol-existence, ast pattern exec, pytest runs, additions-removed control run)
- No UNCHECKED items. No UNVERIFIABLE items. Every PASS cites specific tool output (git numstat, file:line, ast match counts, pytest tallies).

## Recommendations

- Green light for the FX3/FX5 additive artifacts on the additive-safety-structural axis. The additions are purely additive: no existing fixture, test file, or previously-passing test is altered or broken.
- The 6 unrelated pre-existing failures are outside this task's scope; address them (or the missing `offer-pr-review.sh`) under a separate item so `make test` returns to green for the package.

## QA Complete
