# Adversarial Diff Analysis — FIX-A vs FIX-B

| Aspect | FIX-A | FIX-B |
|--------|-------|-------|
| **Lines changed** | 1 (remove one kwarg) | ~10 across signature, body, callers, tests, docs |
| **Diagnosis** | output_dir self-reference at 1476 | same |
| **Surface area** | eval_run call site only | resolve_scratch_root signature + every caller |
| **Backward compatibility** | Preserved (kwarg still exists for legitimate uses) | Breaks documented `output_dir=` API |
| **Doc churn** | None (existing docs already correct) | Update scratch-roots.md:91-97; remove test_output_dir_is_call_scoped_not_persistent |
| **Threat surface closed** | This bug + future-equivalents at other call sites (still need parity test) | This bug + future-equivalents at API level (kwarg gone, can't be misused) |
| **Reversibility** | Easy (re-add kwarg) | Harder (re-add kwarg, re-add docstring, re-add test) |
| **Time-to-fix** | Minutes | Hour-scale + cross-tree audit |

**Shared elements**: same diagnosis; same regression test; same release-note implications for operators.
