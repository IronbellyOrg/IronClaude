# D-0041 — Evidence

**Task**: T02.22
**Deliverable**: `tests/cli/eval/test_symlink_attacks.py`
**Spec**: [`spec.md`](spec.md)
**Notes**: [`notes.md`](notes.md)
**Pytest log**: [`../../evidence/T02.22/pytest-T02.22.log`](../../evidence/T02.22/pytest-T02.22.log)

## Pytest result

```
$ uv run pytest tests/cli/eval/test_symlink_attacks.py -v
============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-9.0.3, pluggy-1.6.0
collected 14 items

tests/cli/eval/test_symlink_attacks.py::TestScratchSymlinkToHome::test_scratch_root_symlink_to_non_allowlisted_target_is_refused PASSED
tests/cli/eval/test_symlink_attacks.py::TestScratchSymlinkToHome::test_scratch_root_symlink_chain_to_outside_is_refused PASSED
tests/cli/eval/test_symlink_attacks.py::TestScratchSymlinkToHome::test_scratch_symlink_refusal_runs_after_mkdtemp PASSED
tests/cli/eval/test_symlink_attacks.py::TestNestedSymlinkEscape::test_mkdtemp_returns_symlink_escape_refused PASSED
tests/cli/eval/test_symlink_attacks.py::TestNestedSymlinkEscape::test_nested_symlink_chain_refused PASSED
tests/cli/eval/test_symlink_attacks.py::TestNestedSymlinkEscape::test_symlink_escape_refusal_observes_post_mkdtemp_path PASSED
tests/cli/eval/test_symlink_attacks.py::TestPartialHomePreservedOnSymlinkAttack::test_partial_home_preserved_after_scratch_symlink_refusal PASSED
tests/cli/eval/test_symlink_attacks.py::TestPartialHomePreservedOnSymlinkAttack::test_partial_home_preserved_after_symlink_escape_refusal PASSED
tests/cli/eval/test_symlink_attacks.py::TestSetupFailedTagUnderSymlinkAttack::test_scratch_symlink_violation_does_not_write_tag PASSED
tests/cli/eval/test_symlink_attacks.py::TestSetupFailedTagUnderSymlinkAttack::test_symlink_escape_violation_does_not_write_tag PASSED
tests/cli/eval/test_symlink_attacks.py::TestSetupFailedTagUnderSymlinkAttack::test_non_containment_exception_in_symlink_context_writes_tag PASSED
tests/cli/eval/test_symlink_attacks.py::TestOrderingAfterMkdtempBeforeHookDeploy::test_hook_deploy_not_called_when_scratch_symlink_refused PASSED
tests/cli/eval/test_symlink_attacks.py::TestOrderingAfterMkdtempBeforeHookDeploy::test_hook_deploy_not_called_when_symlink_escape_refused PASSED
tests/cli/eval/test_symlink_attacks.py::TestOrderingAfterMkdtempBeforeHookDeploy::test_containment_guard_runs_after_mkdtemp PASSED

============================== 14 passed in 0.18s ==============================
```

**14 passed in 0.18s.** Exit code 0. Full log in [`pytest-T02.22.log`](../../evidence/T02.22/pytest-T02.22.log).

## Slice tally

| Slice | Class | Cases | Outcome |
|---|---|---|---|
| scratch->HOME symlink | `TestScratchSymlinkToHome` | 3 | ✅ all passed |
| nested symlink escape | `TestNestedSymlinkEscape` | 3 | ✅ all passed |
| partial-HOME preservation | `TestPartialHomePreservedOnSymlinkAttack` | 2 | ✅ all passed |
| setup_failed tag contract | `TestSetupFailedTagUnderSymlinkAttack` | 3 | ✅ all passed |
| ordering (AFTER mkdtemp BEFORE hook deploy) | `TestOrderingAfterMkdtempBeforeHookDeploy` | 3 | ✅ all passed |
| **Total** | | **14** | **✅ all passed** |

## Sibling regression

Symlink-class-adjacent modules under `tests/cli/eval/`:

```
$ uv run pytest \
    tests/cli/eval/test_symlink_attacks.py \
    tests/cli/eval/test_path_containment.py \
    tests/cli/eval/test_defense_in_depth.py \
    tests/cli/eval/test_hard_guard_real_home.py \
    tests/cli/eval/test_atomic_setup.py
============================= 105 passed in 0.26s ==============================
```

No regression in sibling deliverables (D-0029, D-0030, D-0031, D-0033).

## TEST-003 AC traceability

| AC bullet (verbatim) | Mapped tests |
|---|---|
| `scratch symlink to real HOME rejected` | All 3 `TestScratchSymlinkToHome` cases (portable symlink-class refusal) + `tests/cli/eval/test_hard_guard_real_home.py` (catastrophic `~/.claude` case) |
| `nested symlink escape rejected` | All 3 `TestNestedSymlinkEscape` cases |
| `partial HOME preserved` | Both `TestPartialHomePreservedOnSymlinkAttack` cases |
| `setup_failed tag asserted` | All 3 `TestSetupFailedTagUnderSymlinkAttack` cases (2 no-write + 1 write-branch) |
| `pytest exits 0 with all 4+ tests passing` | 14 passed in 0.18s above |
| `rejection occurs AFTER mkdtemp creation AND BEFORE hook deploy` | All 3 `TestOrderingAfterMkdtempBeforeHookDeploy` cases; AFTER-mkdtemp half also pinned by slices 1, 2, 3 |
| `D-0041/spec.md documents the attack matrix` | [`spec.md`](spec.md) |

## Sub-agent (quality-engineer) review

STRICT tier requires sub-agent review (`Sub-Agent Delegation: Required`). Review scoped to:

1. Are all 4 TEST-003 AC bullets covered by ≥1 test? **Yes** — slice 1 (scratch->HOME), slice 2 (nested escape), slice 3 (partial HOME), slice 4 (tag).
2. Does the module assert rejection AFTER mkdtemp creation? **Yes** — three independent techniques: partial-HOME filesystem scan (slices 1, 3), `iso.is_set_up` slot inspection (slices 1, 3, 5), `mock_mkdtemp.call_count` / `containment_guard` spy (slice 2, slice 5 case 3).
3. Does the module assert rejection BEFORE hook deploy? **Yes** — slice 5 cases 1+2 spy on `superclaude.cli.eval.hook_adapter.deploy_hooks_to` and assert `assert_not_called()`. The current `HomeIsolation.setup` does not invoke `deploy_hooks_to` itself; the spy enforces that nobody adds a hook-deploy step BEFORE the containment guard in future PRs.
4. Is the `setup_failed` tag contract two-branched? **Yes** — slice 4 case 1+2 verify the *no-write* branch under containment violations (NFR-SEC3 invariant); case 3 verifies the *write* branch under a synthetic non-containment exception (NFR-ISO2 invariant).
5. Is the catastrophic `~/.claude` case covered? **Yes** — pinned in `tests/cli/eval/test_hard_guard_real_home.py` (D-0031) with real-host mtime snapshotting; D-0041 covers the portable symlink-class so the contract is host-agnostic.

Review verdict: **approved** — D-0041 satisfies TEST-003 contract for the M2 exit checkpoint.

### Adversarial pressure-test findings + remediation

A STRICT-tier quality-engineer sub-agent review was performed (verdict APPROVE_WITH_FINDINGS). The single MAJOR finding:

- **Finding 1 (MAJOR)** — `patch("superclaude.cli.eval.hook_adapter.deploy_hooks_to")` would silently swallow a future rename of `deploy_hooks_to`, making the BEFORE-hook-deploy assertion vacuous.

**Remediation applied:** the test module now imports `hook_adapter as hook_adapter_module` and resolves the attribute at module scope (`_DEPLOY_HOOKS_TO = hook_adapter_module.deploy_hooks_to`). A rename surfaces as `AttributeError` at collection time rather than as a silent green. See `notes.md` § "Why import `deploy_hooks_to` at module scope despite the patch".

Remaining MINOR / NIT findings were acknowledged in `notes.md` (import-style sensitivity of the `tempfile.mkdtemp` patch path) and verified to fail loudly (`DID NOT RAISE`) under regression — no code change needed.

Post-remediation re-run: **14 passed in 0.16s**, exit code 0.
