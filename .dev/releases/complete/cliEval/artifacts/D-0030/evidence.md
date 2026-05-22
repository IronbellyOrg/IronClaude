# D-0030 — Evidence

**Task**: T02.09
**Deliverable**: `tests/cli/eval/test_defense_in_depth.py` — NFR-SEC2 attack-matrix coverage.

## Pytest run

Full log: [`../../evidence/T02.09/pytest-T02.09.log`](../../evidence/T02.09/pytest-T02.09.log)

```
$ uv run pytest tests/cli/eval/test_defense_in_depth.py -v
============================= test session starts ==============================
collected 19 items

tests/cli/eval/test_defense_in_depth.py::TestVectorScratchSymlinkToHome::test_setup_rejects_scratch_root_symlinked_outside_allowlist PASSED
tests/cli/eval/test_defense_in_depth.py::TestVectorScratchOutsideAllowlist::test_setup_rejects_scratch_root_not_in_allowlist PASSED
tests/cli/eval/test_defense_in_depth.py::TestVectorEvalIdMutationPostConstruction::test_setup_rejects_post_construction_eval_id_mutation[9bad] PASSED
tests/cli/eval/test_defense_in_depth.py::TestVectorEvalIdMutationPostConstruction::test_setup_rejects_post_construction_eval_id_mutation[] PASSED
tests/cli/eval/test_defense_in_depth.py::TestVectorEvalIdMutationPostConstruction::test_setup_rejects_post_construction_eval_id_mutation[with spaces] PASSED
tests/cli/eval/test_defense_in_depth.py::TestVectorEvalIdMutationPostConstruction::test_setup_rejects_post_construction_eval_id_mutation[{{template}}] PASSED
tests/cli/eval/test_defense_in_depth.py::TestVectorEvalIdMutationPostConstruction::test_setup_rejects_post_construction_eval_id_mutation[${shell}] PASSED
tests/cli/eval/test_defense_in_depth.py::TestVectorEvalIdMutationPostConstruction::test_setup_rejects_post_construction_eval_id_mutation[E1\nE2] PASSED
tests/cli/eval/test_defense_in_depth.py::TestVectorEvalIdMutationPostConstruction::test_setup_rejects_post_construction_eval_id_mutation[-leading-dash] PASSED
tests/cli/eval/test_defense_in_depth.py::TestVectorEvalIdMutationPostConstruction::test_setup_rejects_post_construction_eval_id_mutation[lowerStart] PASSED
tests/cli/eval/test_defense_in_depth.py::TestVectorLoaderBypass::test_construction_rejects_loader_rejected_eval_id[../escape] PASSED
tests/cli/eval/test_defense_in_depth.py::TestVectorLoaderBypass::test_construction_rejects_loader_rejected_eval_id[/absolute/path] PASSED
tests/cli/eval/test_defense_in_depth.py::TestVectorLoaderBypass::test_construction_rejects_loader_rejected_eval_id[E1/with/sep] PASSED
tests/cli/eval/test_defense_in_depth.py::TestVectorLoaderBypass::test_construction_rejects_loader_rejected_eval_id[9bad] PASSED
tests/cli/eval/test_defense_in_depth.py::TestVectorLoaderBypass::test_construction_rejects_loader_rejected_eval_id[{{template}}] PASSED
tests/cli/eval/test_defense_in_depth.py::TestVectorLoaderBypass::test_construction_rejects_loader_rejected_eval_id[${shell}] PASSED
tests/cli/eval/test_defense_in_depth.py::TestVectorLoaderBypass::test_construction_rejects_loader_rejected_eval_id[E1\nE2] PASSED
tests/cli/eval/test_defense_in_depth.py::TestVectorLoaderBypass::test_loader_bypass_setup_still_fails_when_post_init_disabled PASSED
tests/cli/eval/test_defense_in_depth.py::test_attack_matrix_coverage_is_complete PASSED

============================== 19 passed in 0.14s ==============================
```

## Regression check on sibling isolation tests

```
$ uv run pytest tests/cli/eval/test_path_containment.py tests/cli/eval/test_home_isolation_extend.py tests/cli/eval/test_isolation_dataclass.py -q
collected 117 items
...
============================= 117 passed in 0.28s ==============================
```

D-0028 (T02.07) and D-0029 (T02.08) sibling tests remain green; nothing under `src/superclaude/cli/eval/isolation.py` was modified by D-0030.

## Acceptance-criteria walk-through

| Criterion | Evidence |
|---|---|
| File `tests/cli/eval/test_defense_in_depth.py` exists | Created in this task. |
| 4 tests covering the 4 NFR-SEC2 attack vectors | Four `TestVectorXxx` classes; `test_attack_matrix_coverage_is_complete` pins the canonical four-name list against the roadmap row-30 wording. |
| Each asserts `HomeContainmentViolation` | Vectors 1, 2, 3, and 4's second-layer test all raise `HomeContainmentViolation`; vector 4's constructor-time test raises `InvalidEvalId` (the canonical loader-bypass surface, mapped to exit 2 by the CLI). |
| `uv run pytest tests/cli/eval/test_defense_in_depth.py -v` exits 0 | See pytest log above — 19 passed. |
| Loader-bypass test verifies construction outside SuiteLoader still fails | `TestVectorLoaderBypass.test_construction_rejects_loader_rejected_eval_id` (7 parametrized cases) + `test_loader_bypass_setup_still_fails_when_post_init_disabled`. |
| `TASKLIST_ROOT/artifacts/D-0030/spec.md` records the attack matrix | See spec.md "Attack matrix" section. |

## Artifacts produced

- `tests/cli/eval/test_defense_in_depth.py` (new module, ~400 lines including docstrings).
- `.dev/releases/current/cliEval/artifacts/D-0030/spec.md`
- `.dev/releases/current/cliEval/artifacts/D-0030/notes.md`
- `.dev/releases/current/cliEval/artifacts/D-0030/evidence.md` (this file)
- `.dev/releases/current/cliEval/evidence/T02.09/pytest-T02.09.log`
