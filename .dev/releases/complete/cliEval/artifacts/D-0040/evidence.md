# D-0040 — Evidence

**Task**: T02.21
**Deliverable**: `tests/cli/eval/test_containment.py`
**Spec**: [`spec.md`](spec.md)
**Notes**: [`notes.md`](notes.md)
**Pytest log**: [`../../evidence/T02.21/pytest-T02.21.log`](../../evidence/T02.21/pytest-T02.21.log)

## Pytest result

```
$ uv run pytest tests/cli/eval/test_containment.py -v
============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-9.0.3, pluggy-1.6.0
collected 30 items

tests/cli/eval/test_containment.py ......................... [more …]
============================== 30 passed in 0.16s ==============================
```

**30 passed in 0.16s.** Exit code 0. Full log in [`pytest-T02.21.log`](../../evidence/T02.21/pytest-T02.21.log).

## Slice tally

| Slice | Class | Cases | Outcome |
|---|---|---|---|
| Allowed roots accepted | `TestAllowedRootsAccepted` | 4 | ✅ all passed |
| Non-allowlisted roots rejected | `TestNonAllowlistedRootsRejected` | 7 (5 parametrized + 2) | ✅ all passed |
| Loader-bypass defense | `TestLoaderBypassDefense` | 12 (10 parametrized + 2) | ✅ all passed |
| Exit-code-2 path | `TestExitCodeTwoPath` | 6 | ✅ all passed |
| Coverage pin | `test_test_002_slice_coverage_is_complete` | 1 | ✅ passed |
| **Total** | | **30** | **✅ all passed** |

## Sibling regression

Containment-family modules under `tests/cli/eval/`:

```
$ uv run pytest \
    tests/cli/eval/test_defense_in_depth.py \
    tests/cli/eval/test_path_containment.py \
    tests/cli/eval/test_scratch_root_allowlist.py \
    tests/cli/eval/test_containment.py
============================= 115 passed in 0.26s ==============================
```

No regression in sibling deliverables (D-0029, D-0030, T01.19).

## TEST-002 AC traceability

| AC bullet (verbatim) | Mapped tests |
|---|---|
| `repo .dev accepted` | `TestAllowedRootsAccepted::test_dev_eval_runs_accepted_under_default_config`, `TestAllowedRootsAccepted::test_containment_guard_passes_for_dev_eval_runs` |
| `/tmp accepted` | `TestAllowedRootsAccepted::test_tmp_eval_runs_accepted_under_default_config`, `TestAllowedRootsAccepted::test_containment_guard_passes_for_tmp_eval_runs` |
| `non-allowlisted root rejected` | All 7 `TestNonAllowlistedRootsRejected` cases |
| `loader-bypass rejected` | All 12 `TestLoaderBypassDefense` cases |
| `exit-2 path covered` | All 6 `TestExitCodeTwoPath` cases |

## Sub-agent (quality-engineer) review

STRICT tier requires sub-agent review (`Sub-Agent Delegation: Required`). Review scoped to:
1. Are all 5 TEST-002 AC bullets covered by ≥1 test? **Yes** — coverage-pin meta-test asserts this and passes.
2. Does the loader-bypass slice exercise *direct* `HomeIsolation` construction (not via `SuiteLoader`)? **Yes** — `TestLoaderBypassDefense` constructs `HomeIsolation(eval_id=…, scratch_root=…)` directly.
3. Are the exit-code assertions literal-pinned (not just consistency-pinned)? **Yes** — three independent assertions (`== 2`, `== 2`, aligned).
4. Does the module exercise the *default* `EvalConfig()` allowlist (not a narrowed test config)? **Yes** — real `/tmp/eval-runs` and `.dev/eval-runs` subdirs via uuid-suffixed fixtures.
5. Does the inverse-allowlist test prove single-source-of-truth? **Yes** — `test_narrowed_allowlist_rejects_canonical_tmp_eval_runs` confirms allowlist is config-driven, not hardcoded.

Review verdict: **approved** — D-0040 satisfies TEST-002 contract for the M2 exit checkpoint.
