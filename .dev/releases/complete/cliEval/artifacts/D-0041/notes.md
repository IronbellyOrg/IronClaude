# D-0041 — Design notes

## Why patch `tempfile.mkdtemp` instead of building a real hostile filesystem

The natural way to exercise the nested-symlink-escape vector (slice 2) is to build a filesystem under `scratch_root` where `mkdtemp` would *organically* return a symlinked path — e.g. mount a hostile NAS, or pre-create a directory entry that `mkdtemp` would happen to pick. **D-0041 deliberately does not do this** because the standard-library `mkdtemp` resolves path collisions by retrying with a fresh random suffix, so making it return a *specific* symlink deterministically is brittle (and platform-specific).

Instead, the slice 2 tests patch `superclaude.cli.eval.isolation.tempfile.mkdtemp` to return a pre-created symlink path. The patch targets the import surface (where `isolation.py` references `tempfile.mkdtemp`), not the upstream `tempfile` module, so other tests in the suite are unaffected. The guard is the defense regardless of *how* a symlinked path appears in `mkdtemp`'s return — patching is the only realistic way to exercise the vector deterministically.

The trade-off accepted: this technique would not catch a regression where `HomeIsolation.setup` stopped calling `tempfile.mkdtemp` at all (e.g. switched to `tempfile.TemporaryDirectory`). That regression is already pinned by D-0029 / D-0030 (`test_path_containment.py` / `test_defense_in_depth.py`), which exercise the guard against real filesystem fixtures.

## Why use a permissive allowlist for vector 2 and a narrowed one for vector 1

Vector 1 (`scratch->HOME symlink`) and vector 2 (`nested symlink escape`) target two different guard checks:

| Vector | Failing check | Allowlist shape |
|---|---|---|
| 1 | check 2 (`scratch_root_allowlist`) | Allowlist excludes the symlink target |
| 2 | check 3 (`home_path_escape`) | Allowlist *includes* the scratch root so check 2 passes |

If vector 2 used a narrowed allowlist that excluded the scratch root, the failure that surfaces would be `check='scratch_root_allowlist'` (vector 1's bucket) — a false positive on a real vector-2 regression would never fire. The `permissive_config` fixture exists explicitly to disambiguate.

## Why use eval ids without underscores

`FR-SCH2` requires `eval_id` to match `^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$` — no underscores. Initial drafts of this module used readable ids like `E_aftermk`, `E_partial1`, `E_order1`; every test broke with `InvalidEvalId` from `__post_init__` before the symlink fixture could run. The fix was a mechanical rename to camel-cased variants: `Eaftermk`, `Epartial1`, `Eorder1`. Documented here because the same gotcha will bite any future symlink-class test author writing readable ids.

## Why the `_list_partial_homes` helper instead of reconstructing the HOME name

`tempfile.mkdtemp(prefix=f"{eval_id}-", ...)` appends a 6-character random suffix, so a test cannot reconstruct the per-eval HOME path from `eval_id` alone. The `_list_partial_homes(scratch_root, eval_id)` helper uses `scratch_root.glob(f"{eval_id}-*")` to find the leaked HOME by prefix. Sorting the result ensures deterministic ordering when multiple tests share a `tmp_path` (which they do not in practice — each test gets a fresh `tmp_path` fixture — but the helper is defensive against future fixture-sharing).

## Why spy on `containment_guard` directly in slice 5 case 3

The two `deploy_hooks_to`-spy tests (slice 5 cases 1 + 2) prove the BEFORE-hook-deploy half but cannot prove the AFTER-mkdtemp half independently — the spy fires *after* the guard refuses, by which time mkdtemp has long since run. Case 3 (`test_containment_guard_runs_after_mkdtemp`) closes the loop by patching the guard itself with a `side_effect` recorder that captures `home_path.exists()` at call time. The assertion `observed["home_existed_at_guard"] is True` proves the guard sees a real on-disk HOME — equivalent to but independent of the partial-HOME-observation technique used in slices 1+3.

Three independent proof techniques for the AFTER-mkdtemp ordering:
1. Partial-HOME scan (slices 1, 3)
2. `iso.is_set_up` slot inspection (slices 1, 3, 5)
3. `mock_mkdtemp.call_count == 1` + `containment_guard` spy (slice 2, slice 5)

A single regression in one technique will be caught by the other two.

## Why a non-containment exception test in slice 4

The TEST-003 AC bullet "setup_failed tag asserted" is ambiguous in the obvious reading — is the tag asserted to *exist* or to *not exist*? The atomic-setup contract (D-0033) is two-branched:

* `HomeContainmentViolation` → tag MUST NOT exist (the violation is the structured signal)
* Any other exception AFTER `mkdtemp` → tag MUST exist with the exception class name as the first line

The symlink attack class always surfaces as `HomeContainmentViolation`, so the no-write branch is what symlink-class tests naturally exercise. To pin the *write* branch under the same module — proving the wrapper still tags under symlink-class conditions when a non-containment exception is injected — slice 4 case 3 monkeypatches `containment_guard` to raise a synthetic `RuntimeError`. The assertion confirms the tag's first line is `"RuntimeError"`, which would catch a regression where the wrapper accidentally swallowed the exception class name.

This is the same dual-branch test pattern D-0033 uses for the wrapper's general case; D-0041 repeats it inside the symlink class to keep the contract self-contained.

## Why `iso.home_path` rather than reconstructing the resolved target

Several tests assert against `iso.home_path` (the symlink path as `mkdtemp` returned it) rather than the resolved escape target. This is intentional — the forensic payload preserves the verbatim path the operator's `mkdtemp` returned, so a reporter can render `"refused HOME: <symlink path>"` in the operator-facing error message. Asserting against the resolved target would let a regression silently rewrite the payload to expose the underlying target (a minor information-leak in the operator log).

## Why import `deploy_hooks_to` at module scope despite the patch

`HomeIsolation.setup` does not currently invoke `deploy_hooks_to` — slice 5 cases 1+2 patch the symbol as a forward-looking tripwire for the T02.14 / Phase 3 wiring. The naïve patch `patch("superclaude.cli.eval.hook_adapter.deploy_hooks_to")` silently passes today regardless of what the patched function is replaced with, *and* would silently pass under a future rename like `deploy_hooks_to → install_hooks_to` (the patch target no longer exists, but pytest does not surface that as a collection error by default).

The fix is the module-top reference `_DEPLOY_HOOKS_TO = hook_adapter_module.deploy_hooks_to`. The attribute access executes at import time — a rename surfaces as `AttributeError` during `pytest --collect-only`, not as a silent green. The unused-binding sentinel is intentional load-bearing infrastructure.

Same technique would apply if the symbol moves to a different module (e.g. `superclaude.cli.eval.hooks.deploy_hooks_to`) — update the import surface here and the `patch` strings simultaneously, or the contract drifts.

Similar import-style sensitivity applies to `superclaude.cli.eval.isolation.tempfile.mkdtemp` (slice 2): a refactor that switches to `from tempfile import mkdtemp` at module scope inside `isolation.py` would invalidate the patch path, the real `mkdtemp` would run instead of the symlink stub, and the tests would fail loudly with `DID NOT RAISE` rather than silently pass — so this is acceptable risk, but worth knowing for the next refactorer.

## Sub-agent review checkpoint

T02.22 is STRICT tier with `Sub-Agent Delegation: Required` (quality-engineer). Per phase-2-tasklist: "Run `uv run pytest tests/cli/eval/test_symlink_attacks.py -v` + sub-agent review." The pytest run is in `evidence.md`; sub-agent review note attached there.

## Sibling regression

After landing this module, the symlink-class-adjacent family
(`test_symlink_attacks.py` + `test_path_containment.py` +
`test_defense_in_depth.py` + `test_hard_guard_real_home.py` +
`test_atomic_setup.py`) runs clean. No drift in sibling deliverables.
