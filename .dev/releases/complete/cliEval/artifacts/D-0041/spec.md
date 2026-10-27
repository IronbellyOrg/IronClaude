# D-0041 — TEST-003 symlink attack tests

**Task**: T02.22 (Phase 2 — cliEval harness)
**Tier**: STRICT
**Risk**: High (security)
**Roadmap**: R-041 / TEST-003 (symlink resolution catches scratch and HOME escape AFTER mkdtemp BEFORE hook deploy; partial HOME preserved; setup_failed tag asserted)
**Cross-links**: D-0029 (FR-ISO2 containment guard, T02.08), D-0030 (NFR-SEC2 defense-in-depth, T02.09), D-0031 (NFR-SEC3 hard guard real HOME, T02.10), D-0033 (NFR-ISO2 atomic setup, T02.13), D-0040 (TEST-002 contract pin, T02.21)

## Goal

TEST-003 is the **symlink-class contract readout** for the M2 exit checkpoint. Sibling deliverables already cover symlink attacks as one bucket inside a wider matrix:

- D-0029 (FR-ISO2 unit) exercises `containment_guard` checks in isolation against symlink-shaped inputs.
- D-0030 (NFR-SEC2 attack matrix) covers four named attack vectors at the `HomeIsolation.setup` boundary — symlinks are one vector among four.
- D-0031 (NFR-SEC3 hard guard) covers the catastrophic scratch->`$HOME`/`.claude` symlink case with real-host mtime snapshotting.
- D-0033 (NFR-ISO2 atomic setup) pins the partial-HOME preservation + `setup_failed` two-branch contract against synthetic injected failures, not symlink-shaped ones.

D-0041 is the **first-class symlink-class TEST item** the roadmap promises: one targeted pytest module, named after the attack class (`test_symlink_attacks.py`), whose every test maps directly to a TEST-003 acceptance-criterion bullet, so the audit reviewing the M2 exit can read the module top-to-bottom and confirm the symlink contract without cross-referencing four sibling modules.

The module exercises **every variant of the symlink attack class** (single-hop, multi-hop, scratch-rooted, per-eval-HOME-rooted) under both real filesystem fixtures and patched `tempfile.mkdtemp` injection, against `EvalConfig.allowed_scratch_roots` allowlists narrowed to the per-test scratch directory. It pins all four TEST-003 acceptance-criterion bullets (rejection AFTER mkdtemp, rejection BEFORE hook deploy, partial-HOME preservation, `setup_failed` tag contract) inside a single module so future symlink-class regressions surface here first.

## Test matrix

| Slice | TEST-003 AC bullet | Test class | Cases |
|---|---|---|---|
| scratch->HOME symlink | scratch symlink to real HOME rejected | `TestScratchSymlinkToHome` | 3 |
| nested symlink escape | nested symlink escape rejected | `TestNestedSymlinkEscape` | 3 |
| partial-HOME preservation | partial HOME preserved | `TestPartialHomePreservedOnSymlinkAttack` | 2 |
| setup_failed tag contract | setup_failed tag asserted | `TestSetupFailedTagUnderSymlinkAttack` | 3 |
| ordering (AFTER mkdtemp BEFORE hook deploy) | rejection after mkdtemp AND before hook deploy | `TestOrderingAfterMkdtempBeforeHookDeploy` | 3 |
| **Total** | | | **14** |

### Slice 1 — `TestScratchSymlinkToHome` (3 cases)

The declared scratch root is itself a symlink whose resolved target is not in `EvalConfig.allowed_scratch_roots`. Guard check 2 (`scratch_root_allowlist`) MUST refuse.

- `test_scratch_root_symlink_to_non_allowlisted_target_is_refused` — single-hop symlink (`scratch-symlink -> outside_target`) where `outside_target` is not allowlisted; raises `HomeContainmentViolation(check="scratch_root_allowlist")`. Asserts the forensic payload preserves the symlink path *verbatim* (not its resolved target), so a reporter renders the operator-facing path.
- `test_scratch_root_symlink_chain_to_outside_is_refused` — multi-hop chain (`scratch -> intermediate -> outside`); `Path.resolve(strict=False)` collapses the full chain in one shot, so multi-hop links must surface the same allowlist-miss as single-hop.
- `test_scratch_symlink_refusal_runs_after_mkdtemp` — confirms the refusal lands AFTER `tempfile.mkdtemp` materializes the per-eval HOME on disk (observable as a leaked partial HOME under the symlink target + populated `iso.is_set_up` slot).

### Slice 2 — `TestNestedSymlinkEscape` (3 cases)

The scratch root is real and allowlisted, but the path `tempfile.mkdtemp` returns for the per-eval HOME is itself a symlink (or contains a symlink chain) whose resolved target escapes the scratch root. Guard check 3 (`home_path_escape`) catches this via `Path.resolve(strict=True)`.

The vector is exercised by patching `superclaude.cli.eval.isolation.tempfile.mkdtemp` to return a pre-created symlink — `mkdtemp` itself does not produce symlinks, but a future filesystem-shim or hostile shared NAS could. The guard is the defense regardless of *how* the symlink appears.

- `test_mkdtemp_returns_symlink_escape_refused` — single-hop symlink whose target lives outside the scratch root; raises `HomeContainmentViolation(check="home_path_escape")`. Asserts the recorded `iso.home_path` is the symlink (verbatim).
- `test_nested_symlink_chain_refused` — multi-hop chain (`home -> intermediate -> outside`); `resolve(strict=True)` collapses every symlink component before the prefix check.
- `test_symlink_escape_refusal_observes_post_mkdtemp_path` — confirms `mkdtemp` was invoked exactly once and the violation's `home_path` matches the mkdtemp return value — pinning the AFTER-mkdtemp ordering without relying on monkey-patching the guard itself.

### Slice 3 — `TestPartialHomePreservedOnSymlinkAttack` (2 cases)

NFR-ISO2 requires every post-`mkdtemp` exception to leave the per-eval HOME on disk so a wrapper can route teardown through `teardown(keep=True)`. This slice proves the contract holds specifically under the symlink attack class, on both checks 2 and 3.

- `test_partial_home_preserved_after_scratch_symlink_refusal` — after vector 1 fires, the partial HOME exists under the resolved symlink target, `iso.is_set_up` is true, and `teardown(keep=True)` preserves the directory on disk.
- `test_partial_home_preserved_after_symlink_escape_refusal` — after vector 2 fires, the symlinked HOME remains under the scratch root, `iso.home_path` points at it, and `teardown(keep=True)` leaves the symlink intact.

### Slice 4 — `TestSetupFailedTagUnderSymlinkAttack` (3 cases)

The NFR-ISO2 / NFR-SEC3 two-branch tag contract from D-0033 is repeated here against the symlink attack class:

* `HomeContainmentViolation` (the surface form of every symlink attack) MUST NOT drop a `setup_failed` tag. Writing under a refused HOME could land inside the real `~/.claude/` when the scratch root or `mkdtemp` result symlinks there — the very catastrophic case NFR-SEC3 mitigates.
* A non-containment exception raised AFTER `mkdtemp` MUST drop the canonical `setup_failed` tag whose first line is the exception class name.

- `test_scratch_symlink_violation_does_not_write_tag` — vector 1 refusal leaves the partial HOME empty of the tag; the `.eval-meta` parent dir is also absent (defense-in-depth).
- `test_symlink_escape_violation_does_not_write_tag` — vector 2 refusal does not write the tag under the symlinked HOME; the `.eval-meta` dir under the resolved escape target is also absent (the catastrophic transparent-forwarding case).
- `test_non_containment_exception_in_symlink_context_writes_tag` — patches `containment_guard` to raise a synthetic `RuntimeError`; the wrapper drops the canonical tag whose first line is `RuntimeError`, and the tag lives under `iso.home_path` (never outside it).

### Slice 5 — `TestOrderingAfterMkdtempBeforeHookDeploy` (3 cases)

TEST-003 acceptance criterion 3 mandates rejection lands in the canonical "after mkdtemp, before hook deploy" window. This slice pins both ordering invariants for the symlink class.

`HomeIsolation.setup` does not currently invoke `deploy_hooks_to` itself (the wiring lands in T02.14 / Phase 3); the spy proves that nobody in this module's lifetime has changed that — a future caller that adds a hook-deploy step BEFORE the containment guard would break this assertion before it ships.

- `test_hook_deploy_not_called_when_scratch_symlink_refused` — spies on `superclaude.cli.eval.hook_adapter.deploy_hooks_to` while vector 1 fires; `assert_not_called()`. Also confirms the partial HOME exists under the symlink target (AFTER mkdtemp).
- `test_hook_deploy_not_called_when_symlink_escape_refused` — same spy under vector 2; `mock_mkdtemp.call_count == 1` proves mkdtemp ran exactly once before the guard refused.
- `test_containment_guard_runs_after_mkdtemp` — spies on `containment_guard` itself, recording `home_path.exists()` at guard-call time. The guard sees a real on-disk HOME — proving the ordering directly without relying on the symlink mock.

## Acceptance criteria

| AC | Source | Verified by |
|---|---|---|
| AC1 — scratch symlink to real HOME rejected | TEST-003 | All 3 `TestScratchSymlinkToHome` cases (symlink-class refusal) + the catastrophic `~/.claude` case is in D-0031 (`tests/cli/eval/test_hard_guard_real_home.py`) |
| AC2 — nested symlink escape rejected | TEST-003 | All 3 `TestNestedSymlinkEscape` cases |
| AC3 — partial HOME preserved | TEST-003 | Both `TestPartialHomePreservedOnSymlinkAttack` cases |
| AC4 — setup_failed tag asserted | TEST-003 | All 3 `TestSetupFailedTagUnderSymlinkAttack` cases (no-write branch ×2, write branch ×1) |
| AC5 — pytest exits 0 with ≥4 tests | TEST-003 | Evidence log: 14 passed in 0.18s |
| AC6 — rejection AFTER mkdtemp AND BEFORE hook deploy | TEST-003 | All 3 `TestOrderingAfterMkdtempBeforeHookDeploy` cases + the AFTER-mkdtemp half is re-pinned in 3 sibling slices |
| AC7 — `D-0041/spec.md` documents the attack matrix | TEST-003 | this document |

## Why a new module instead of extending an existing one

| Existing module | Purpose | Why it can't be TEST-003 |
|---|---|---|
| `test_path_containment.py` (D-0029) | FR-ISO2 unit — three checks of `containment_guard` in isolation | Asserts *internal* guard behavior; doesn't pin the AFTER-mkdtemp / BEFORE-hook-deploy ordering window or the partial-HOME-preservation contract |
| `test_defense_in_depth.py` (D-0030) | NFR-SEC2 attack matrix — four named vectors | Vector-oriented framing covering symlinks, nested symlinks, scratch-root violation, eval-id injection as siblings; symlink-specific coverage is partial |
| `test_hard_guard_real_home.py` (D-0031) | NFR-SEC3 catastrophic case — host-`$HOME` mtime snapshot | Scoped to a single catastrophic instance; does not exercise the nested-symlink, partial-HOME, or tag contracts |
| `test_atomic_setup.py` (D-0033) | NFR-ISO2 atomic-setup wrapper — partial HOME + tag two-branch contract | Uses synthetic injected failures; does not exercise the symlink attack class |
| `test_containment.py` (D-0040) | TEST-002 contract — allowed/non-allowed roots + exit-code-2 | Scoped to allowlist contract, not symlink attacks |

TEST-003 is the *symlink-class contract* — one module whose every test maps to an AC bullet, designed to be read by the M2-exit auditor. Folding it into any existing module would dilute the readout and re-introduce the same scattered-coverage problem the TEST-003 deliverable was created to fix.

## Public API touched

None. D-0041 is a test-only deliverable. Production surface was finalized by D-0029 / D-0030 / D-0031 / D-0033. The module *does* depend on:

- `superclaude.cli.eval.SETUP_FAILED_TAG_RELPATH` (constant)
- `superclaude.cli.eval.HomeContainmentViolation` (with `check`, `scratch_root`, `home_path` attributes)
- `superclaude.cli.eval.HomeIsolation` (with `setup`, `teardown`, `is_set_up`, `home_path`)
- `superclaude.cli.eval.isolation.tempfile.mkdtemp` (import surface, patched in vector 2)
- `superclaude.cli.eval.isolation.containment_guard` (monkeypatched in slice 4 case 3 + slice 5 case 3)
- `superclaude.cli.eval.hook_adapter.deploy_hooks_to` (import surface, spied in slice 5)

Any future change to these surfaces will surface here first — the module is intentionally a contract test, not an implementation test.

## Ordering window proof — detailed

The TEST-003 ordering requirement ("rejection AFTER mkdtemp creation AND BEFORE hook deploy") is the highest-value invariant in this deliverable. Three independent proof techniques are used so a single technique going stale will not silently mask drift:

1. **Partial-HOME observation** — `_list_partial_homes(target, eval_id)` finds the leaked HOME under the resolved scratch target (vector 1) or under the scratch root (vector 2) after the violation fires. The HOME existing on disk proves `mkdtemp` ran *before* the guard refused.
2. **`HomeIsolation.is_set_up` slot inspection** — the instance slot is populated only AFTER `mkdtemp` succeeds inside `HomeIsolation.setup`. Asserting `iso.is_set_up` after a violation proves the same ordering without relying on filesystem scans.
3. **`mock_mkdtemp.call_count == 1`** — when `tempfile.mkdtemp` is patched (vector 2), the spy records that mkdtemp was invoked exactly once before the guard ran.

The BEFORE-hook-deploy half is pinned by a single technique (spying on `deploy_hooks_to`), and the orthogonal `containment_guard`-spy test asserts the guard itself observes a real on-disk HOME at call time — closing the loop without requiring `deploy_hooks_to` to be wired into `setup` yet (T02.14 / Phase 3).
