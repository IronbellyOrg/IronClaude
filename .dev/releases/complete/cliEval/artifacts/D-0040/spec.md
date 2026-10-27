# D-0040 — TEST-002 containment unit tests

**Task**: T02.21 (Phase 2 — cliEval harness)
**Tier**: STRICT
**Risk**: High (security)
**Roadmap**: R-040 / TEST-002 (allowed roots accepted, non-allowlisted roots rejected, loader-bypass defense, exit-code-2 path)
**Cross-links**: D-0028 (HomeIsolation surface, T02.07), D-0029 (FR-ISO2 path containment guard, T02.08), D-0030 (NFR-SEC2 defense-in-depth, T02.09), AC12 / T01.19 (`resolve_scratch_root`), FR-SCH2 / T01.05 (`validate_eval_id`)

## Goal

TEST-002 is the **contract-layer readout** for the M2 exit checkpoint. The sibling deliverables (D-0029 unit, D-0030 attack matrix) prove the three checks of `containment_guard` and the four NFR-SEC2 attack vectors. D-0040 is the *first-class TEST item* the roadmap promises: one targeted pytest module, named after the boundary it pins (`test_containment.py`), whose every test maps directly to a TEST-002 acceptance-criterion bullet, so that the audit reviewing the M2 exit can read the file top-to-bottom and confirm the contract without spelunking through three sibling modules.

The module exercises **real canonical scratch roots** (`/tmp/eval-runs`, `.dev/eval-runs`) under the **default** `EvalConfig()` allowlist — not a narrowed test config — so the test would fail if either canonical root were ever removed from `EvalConfig.allowed_scratch_roots`. It also pins both exit-code constants (`INVALID_EVAL_ID_EXIT_CODE`, `SCRATCH_ROOT_VIOLATION_EXIT_CODE`) as `== 2` literals, so any drift on the exit-code contract surfaces here.

## Test matrix

| Slice | TEST-002 AC bullet | Test class | Cases |
|---|---|---|---|
| Allowed roots accepted | `repo .dev accepted`, `/tmp accepted` | `TestAllowedRootsAccepted` | 4 |
| Non-allowlisted roots rejected | `non-allowlisted root rejected` | `TestNonAllowlistedRootsRejected` | 7 (5 parametrized + 2) |
| Loader-bypass defense | `loader-bypass rejected` | `TestLoaderBypassDefense` | 12 (10 parametrized + 2) |
| Exit-code-2 path | `exit-2 path covered` | `TestExitCodeTwoPath` | 6 |
| Coverage pin | (meta) | `test_test_002_slice_coverage_is_complete` | 1 |
| **Total** | | | **30** |

### Slice 1 — `TestAllowedRootsAccepted` (4 cases)

- `test_tmp_eval_runs_accepted_under_default_config` — `HomeIsolation.setup(config=EvalConfig())` succeeds with a `/tmp/eval-runs/<unique>` subdir (real path created and torn down).
- `test_dev_eval_runs_accepted_under_default_config` — same, for `.dev/eval-runs/<unique>` (repo-anchored canonical root).
- `test_containment_guard_passes_for_tmp_eval_runs` — `containment_guard(...)` returns cleanly for an allowed root + resolved tempdir.
- `test_containment_guard_passes_for_dev_eval_runs` — same, for the repo-anchored canonical root.

### Slice 2 — `TestNonAllowlistedRootsRejected` (7 cases)

- `test_setup_rejects_root_outside_default_allowlist` (parametrized × 5): `~/.claude`-style user-home path, `/etc`-style system path, `/var/lib/eval-runs`, `/root/.claude`, `/tmp/other-runs`. Each must raise `HomeContainmentViolation(check="scratch_root_allowlist")` with `ScratchRootViolation` as `__cause__`.
- `test_containment_guard_rejects_root_outside_default_allowlist` — unit-level rejection via direct `containment_guard(...)` call against a non-allowlisted `tmp_path`.
- `test_narrowed_allowlist_rejects_canonical_tmp_eval_runs` — *inverse* assertion: when a caller narrows the allowlist (e.g. to repo `.dev` only), the canonical `/tmp/eval-runs` is rejected. Proves the allowlist is a *single source of truth* — not a hardcoded constant inside `containment_guard`.

### Slice 3 — `TestLoaderBypassDefense` (12 cases)

This is the highest-stakes slice — TEST-002 explicitly requires direct construction of `HomeIsolation` without `SuiteLoader` to confirm containment still applies.

- `test_direct_construction_rejects_loader_rejected_id` (parametrized × 10): for each FR-SCH2-rejected id (`../escape`, `/etc/passwd`, `E1/with/sep`, `..`, `9bad`, empty string, `with spaces`, `{{template}}`, `${shell}`, `E1\nE2`), constructing `HomeIsolation(eval_id=<bad>, ...)` directly (not through `SuiteLoader`) raises `InvalidEvalId` from `__post_init__` before any filesystem call.
- `test_direct_construction_with_post_init_disabled_is_caught_by_guard` — simulates a future refactor that removes the constructor check by monkeypatching `__post_init__` to a slot-only initializer; confirms `containment_guard`'s second-layer `validate_eval_id` call still rejects. Patches `__post_init__` (not `validate_eval_id`) so the two layers remain genuinely independent.
- `test_direct_construction_without_loader_still_hits_allowlist_check` — direct (non-loader) construction with a *valid* `eval_id` but a non-allowlisted scratch root: `HomeContainmentViolation(check="scratch_root_allowlist")` still fires, proving the allowlist check is not coupled to loader-mediated entry.

### Slice 4 — `TestExitCodeTwoPath` (6 cases)

- `test_invalid_eval_id_exit_code_is_two` — `INVALID_EVAL_ID_EXIT_CODE == 2` (literal pin).
- `test_scratch_root_violation_exit_code_is_two` — `SCRATCH_ROOT_VIOLATION_EXIT_CODE == 2` (literal pin).
- `test_exit_codes_are_aligned_with_each_other` — the two constants are equal (so CLI exit-code policy treats both rejection paths uniformly).
- `test_containment_failure_chains_exit2_cause_for_eval_id` — end-to-end: a real containment failure on a tampered `eval_id` chains `InvalidEvalId` as `__cause__`, and `InvalidEvalId`'s exit-code constant is 2.
- `test_containment_failure_chains_exit2_cause_for_scratch_root` — same, for a real containment failure on a non-allowlisted scratch root, chaining `ScratchRootViolation`.
- `test_direct_loader_bypass_exit_path_is_invalid_eval_id` — direct construction with a bad id raises `InvalidEvalId` whose exit-code is 2.

### Coverage pin — `test_test_002_slice_coverage_is_complete`

A meta-test that asserts each TEST-002 AC bullet has at least one corresponding test class in this module. Future drift in the AC list will break this test, forcing a coordinated spec + test update.

## Acceptance criteria

| AC | Source | Verified by |
|---|---|---|
| AC1 — repo `.dev` accepted | TEST-002 | `TestAllowedRootsAccepted::test_dev_eval_runs_accepted_under_default_config`, `…::test_containment_guard_passes_for_dev_eval_runs` |
| AC2 — `/tmp` accepted | TEST-002 | `TestAllowedRootsAccepted::test_tmp_eval_runs_accepted_under_default_config`, `…::test_containment_guard_passes_for_tmp_eval_runs` |
| AC3 — non-allowlisted root rejected | TEST-002 | `TestNonAllowlistedRootsRejected` (all 7 cases) |
| AC4 — loader-bypass rejected | TEST-002 | `TestLoaderBypassDefense` (all 12 cases) |
| AC5 — exit-2 path covered | TEST-002 | `TestExitCodeTwoPath` (all 6 cases) |
| AC6 — pytest exits 0 | TEST-002 | Evidence log: 30 passed in 0.16s |
| AC7 — direct construction without `SuiteLoader` still contained | TEST-002 | `TestLoaderBypassDefense::test_direct_construction_without_loader_still_hits_allowlist_check`, `…::test_direct_construction_with_post_init_disabled_is_caught_by_guard` |
| AC8 — `D-0040/spec.md` documents the test matrix | TEST-002 | this document |

## Why a new module instead of extending an existing one

| Existing module | Purpose | Why it can't be TEST-002 |
|---|---|---|
| `test_path_containment.py` | FR-ISO2 unit — three checks of `containment_guard` in isolation | Asserts *internal* guard behavior; doesn't pin `EvalConfig` defaults or exit-code contract |
| `test_defense_in_depth.py` (D-0030) | NFR-SEC2 attack matrix — four named vectors | Vector-oriented framing, not AC-oriented; loader-bypass slice is one vector among four |
| `test_scratch_root_allowlist.py` | AC12 unit — `resolve_scratch_root` standalone | Scoped to the allowlist resolver; doesn't cover `eval_id` or exit-codes |

TEST-002 is the *contract* — one module whose every test maps to an AC bullet, designed to be read by the M2-exit auditor. Folding it into any existing module would dilute the readout and re-introduce the same scattered-coverage problem the TEST-002 deliverable was created to fix.

## Public API touched

None. D-0040 is a test-only deliverable. Production surface was finalized by D-0028 / D-0029 / D-0030. The exit-code constants and the `default` `EvalConfig()` allowlist are now *load-bearing* for this module — any future change to either will surface here first.
