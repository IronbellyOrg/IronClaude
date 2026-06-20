---
artifact: r1-3-validation-summary
phase: 8
release: R1.3
task: TASK-RF-20260531-042405
created_date: 2026-06-02
verdict: PASS
---

# R1.3 Validation Summary — `GateCriteria.code_assertions` + first `CodeAssertion`

Full raw output: `r1-3-validation.txt` (this directory).

## Verdict: PASS

| Check | Result |
| --- | --- |
| `tests/roadmap/test_dispatch_reachability.py` (NEW, 7 tests) | ✅ 7 PASS |
| `tests/roadmap/test_executor.py` (regression) | ✅ PASS |
| `tests/roadmap/test_certify_gates.py` (regression) | ✅ PASS |
| `tests/roadmap/test_certify_prompts.py` (regression) | ✅ PASS |
| `tests/roadmap/test_pipeline_integration.py` (regression) | ✅ PASS |
| Combined command total | **140 passed, 0 failed** |
| `ruff check` (5 files) | ✅ All checks passed |
| `ruff format --check` (5 files) | ✅ 5 files already formatted |

## New tests (Contract #2 enforcement)

`tests/roadmap/test_dispatch_reachability.py` — 7 tests:

1. **`test_certify_step_reachable`** (Step 8.4 required) — `assert_step_reachable`
   returns `None` (PASS) against the real production `executor.py` now that
   `build_certify_step` has a production caller (`_run_certify_after_remediate`,
   invoked by `execute_roadmap`).
2. **`test_unwired_step_caught`** (Step 8.4 required) — a synthetic `executor.py`
   (in `tmp_path`) whose `_build_steps` omits `certify` AND whose
   `build_certify_step` has no caller yields a HIGH `Finding`
   (`CA-DISPATCH-002`). This reproduces the master:§Flaw 1 pre-R1.3 state and
   confirms the assertion genuinely catches it.
3. **`test_wired_via_build_steps_literal_passes`** (supplementary) — the static
   dispatch shape (certify as a `Step(id="certify")` literal in `_build_steps`)
   also passes, proving the assertion accepts both legitimate wiring shapes.
4. **`test_executor_missing_yields_finding`** (supplementary) — a `repo_root`
   with no `executor.py` yields the `CA-DISPATCH-001` resolution-failure Finding
   (defensive path coverage).
5. **`test_all_strict_gates_have_assertions`** (Step 8.4 required, scoped) — every
   **STRICT**-tier gate in `ALL_GATES` has `semantic_checks` OR
   `code_assertions`; non-STRICT gates (`diff`, `score` are STANDARD) are
   asserted to remain non-STRICT. See "Interpretation note" below.
6. **`test_certify_gate_has_code_assertion`** (supplementary) — `CERTIFY_GATE`
   carries the `step_reachable` CodeAssertion.
7. **`test_codeassertion_signature_invariant`** (Step 8.4 required) — both public
   assertions (`assert_step_reachable`, `assert_envelope_artifacts_present`) plus
   the check_fn wired into `CERTIFY_GATE` have return annotation exactly
   `"Finding | None"` and leading params `(envelope, repo_root)` (§MVR §2
   widened access).

## Interpretation note (logged for PG8.1)

Step 8.4's `test_all_gates_have_assertions` literal wording is "every gate either
has semantic_checks OR code_assertions". Two gates — `diff` and `score` — are
**STANDARD** tier with neither: they gate on frontmatter fields + min_lines, which
is NOT a silent pass. The item's own parenthetical ("empty gates are silent PASS")
keys the invariant to **STRICT** gates, where missing checks degrade STRICT to
STANDARD behaviour (a genuine silent pass). The test therefore enforces the
invariant for STRICT gates and additionally guards that `diff`/`score` stay
non-STRICT (catching a future STRICT-promotion regression). This is the faithful
reading of the stated Contract #4 spirit, not a weakening.

## Regression integrity

- No regression in `test_executor.py` / `test_certify_gates.py` /
  `test_certify_prompts.py` / `test_pipeline_integration.py`.
- Broader sweep (`tests/roadmap/ tests/cli/`, run during Step 8.3): 3337 passed,
  19 failed, 16 skipped. All 19 failures are PRE-EXISTING, confirmed by stashing
  the 4 tracked source changes and re-running (identical failures on parent state
  90a8fa67). CORRECTED ATTRIBUTION (PG8.1 rf-qa): the 19 split as **16 in
  `tests/cli/`** (`test_install_hooks.py` + `tests/cli/eval/`) and **3 in
  `tests/roadmap/`** (`test_cli_contract.py::test_default_agents_when_not_provided`,
  `test_models.py::test_default_agents`, `test_validate_unit.py::test_default_agents_two`)
  — a default-agent-model drift (test expects `haiku`; config default is `sonnet`)
  independent of R1.3. None of the failing test files import an R1.3-modified
  module. The "entirely in tests/cli/" wording was inaccurate and is corrected here.

## Step-count budget (Acceptance gate #6)

`_build_steps` returns 13 Step constructions; `ALL_GATES` / `_get_all_step_ids`
list 14 (certify is the 14th). certify is constructed + executed dynamically
post-remediate (NOT added to `_build_steps`), so the live step count is 14 — ≤14,
budget satisfied. No consolidation required at R1.3.
