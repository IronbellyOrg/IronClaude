# T02.09 — NFR-SEC2 Defense-in-depth tests

**Deliverable**: `tests/cli/eval/test_defense_in_depth.py`
**Spec**: [`../../artifacts/D-0030/spec.md`](../../artifacts/D-0030/spec.md)
**Pytest log**: [`pytest-T02.09.log`](pytest-T02.09.log) — 19 passed in 0.14s

## Summary

19 tests across 4 vector classes + 1 coverage pin. All passing.

| Vector | Class | Cases |
|---|---|---|
| `scratch-is-symlink-to-HOME` | `TestVectorScratchSymlinkToHome` | 1 |
| `scratch-outside-allowlist` | `TestVectorScratchOutsideAllowlist` | 1 |
| `eval_id-mutation-post-construction` | `TestVectorEvalIdMutationPostConstruction` | 8 (parametrized) |
| `loader-bypass` | `TestVectorLoaderBypass` | 8 (7 parametrized + 1 second-layer) |
| Coverage pin | `test_attack_matrix_coverage_is_complete` | 1 |

Regression on D-0028 / D-0029 sibling modules: 117 passed in 0.28s.
