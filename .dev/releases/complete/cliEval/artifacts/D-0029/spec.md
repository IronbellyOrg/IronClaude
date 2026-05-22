# D-0029 — FR-ISO2 Path Containment Guard

**Task**: T02.08 (Phase 2 — cliEval harness)
**Tier**: STRICT
**Risk**: High (security-critical, defense-in-depth)
**Roadmap**: FR-ISO2 + NFR-SEC2 (loader-bypass / refusal-before-side-effects)
**Cross-links**: D-0028 (HomeIsolation method surface, T02.07), AC12 / T01.19 (resolve_scratch_root), FR-SCH2 / T01.05 (validate_eval_id)

## Goal

Provide a single helper, `containment_guard(home_path, scratch_root, eval_id, *, config)`, that the cliEval harness invokes AFTER `tempfile.mkdtemp` materialized a per-eval HOME and BEFORE any hook adapter writes a single byte under it. The guard fails closed: any of three independent checks raising surfaces a `HomeContainmentViolation`; the partial per-eval HOME is left on disk so the NFR-ISO2 atomic-setup wrapper (T02.13) can tag it as `setup_failed` for forensic inspection.

## Public API

### `HomeContainmentViolation(Exception)`

Single hard-failure exception type. Callers may catch the base class; branching on the underlying cause is forensics-only.

| Field | Type | Source |
|---|---|---|
| `check` | `str` | One of `"eval_id"`, `"scratch_root_allowlist"`, `"home_path_resolution"`, `"home_path_escape"`. Lets reporters bucket failures without parsing the message. |
| `home_path` | `Path` | Verbatim input (no resolution). |
| `scratch_root` | `Path` | Verbatim input. |
| `eval_id` | `object` | Verbatim input (`repr`-rendered); non-string scalars stay visible. |
| `detail` | `str` | Human-readable one-line cause. |

`__cause__` carries the underlying `InvalidEvalId`, `ScratchRootViolation`, or `FileNotFoundError` (chained via `raise ... from`).

### `containment_guard(home_path, scratch_root, eval_id, *, config: EvalConfig) -> None`

Three checks run in order. First failure short-circuits:

1. **eval_id regex (loader-bypass defense)** — re-applies `validate_eval_id` (T01.05) so a caller that bypassed `SuiteLoader` (programmatic test, future REPL) still hard-fails. Raises `HomeContainmentViolation(check="eval_id", ..., __cause__=InvalidEvalId)`.
2. **Scratch-root allowlist (AC12)** — re-routes through `resolve_scratch_root(scratch_root, config=config)`. Catches a scratch root that is a symlink to a non-allowlisted target (the helper resolves with `strict=False` so symlinks collapse). The allowlist is sourced exclusively from `config.allowed_scratch_roots`; the guard **refuses to synthesize a fallback** (NFR-SEC2 — see "Bypass surface closed" below). Raises `HomeContainmentViolation(check="scratch_root_allowlist", ..., __cause__=ScratchRootViolation)`.
3. **Post-mkdtemp symlink-resolved containment** — `home_path.resolve(strict=True)` collapses every symlink component and forces the HOME to exist on disk; the resolved form must equal or live beneath the resolved `scratch_root`. Raises `HomeContainmentViolation(check="home_path_resolution", ..., __cause__=FileNotFoundError)` when the HOME has not been materialized, or `check="home_path_escape"` when the resolved form is outside `scratch_root`.

### `HomeIsolation.setup(*, config: EvalConfig) -> Path`

Integrates the guard:

1. Raises `RuntimeError` if `setup` was already called on this instance and `teardown` has not run since (idempotency rule preserved from T02.07).
2. `mkdir(parents=True, exist_ok=True)` on `self.home_root` so the scratch root exists.
3. `tempfile.mkdtemp(prefix=f"{eval_id}-", dir=str(self.home_root))` mints the per-eval HOME. The path is stored on the private `_home_path` slot via `object.__setattr__`.
4. **`containment_guard(home_path=home, scratch_root=self.home_root, eval_id=self.eval_id, config=config)`** — the FR-ISO2 check runs here, AFTER the slot is populated, BEFORE return. Any failure surfaces verbatim; the slot stays populated so the NFR-ISO2 wrapper (T02.13) can find the partial HOME.

`config` is a required keyword-only argument. No default. No fallback. See "Bypass surface closed".

## Bypass surface closed (NFR-SEC2)

A predecessor draft of `setup()` accepted `config: EvalConfig | None = None` and, when `None`, synthesized:

```python
EvalConfig(
    allowed_scratch_roots=(self.home_root, *EvalConfig().allowed_scratch_roots),
)
```

The quality-engineer review flagged this as a security bypass: `HomeIsolation.__post_init__` validates `eval_id` (FR-SCH2) but does NOT validate `home_root`, so a caller could construct `HomeIsolation(eval_id="E1", home_root=Path("/home/user/.claude"), session_id="x")` and have `setup()` quietly inject `/home/user/.claude` into the allowlist before invoking the guard. Check 2 would then pass trivially against an attacker-controlled root.

The fix landed in this deliverable:

- `containment_guard`'s `config` parameter is required (no `None` default, no inline `EvalConfig()` fabrication).
- `HomeIsolation.setup`'s `config` parameter is required.
- The home_root-injection fallback is deleted.

Refusal-before-side-effects is preserved: a caller who omits `config` triggers Python's argument-binding `TypeError` BEFORE `setup`'s body executes, so the `mkdir(parents=True, exist_ok=True)` on `self.home_root` and the `mkdtemp` call never run. Asserted by `test_setup_requires_explicit_config` (assertion: `not any(scratch_root.iterdir())` after the `TypeError`).

## Acceptance criteria

| AC | Source | Verified by |
|---|---|---|
| `containment_guard` raises on FR-SCH2-rejected eval_id | T02.08 AC | `TestEvalIdReValidation.test_raises_on_unsafe_eval_id` (10 parametrized cases) |
| `containment_guard` raises on non-string eval_id | NFR-SEC2 | `TestEvalIdReValidation.test_non_string_eval_id_is_rejected` (12 parametrized cases: int, bool, None, Path, bytes, list, dict, tuple, float) |
| `containment_guard` raises when scratch root not in allowlist | AC12 | `TestScratchRootAllowlist.test_raises_when_scratch_root_outside_default_allowlist`, `test_uses_evalconfig_allowed_scratch_roots_as_source_of_truth` |
| `containment_guard` catches scratch root symlinked to non-allowlisted target | AC12 + symlink defense | `TestScratchRootAllowlist.test_raises_when_scratch_root_symlinked_outside_allowlist` |
| `containment_guard` raises when home_path missing (resolve `strict=True`) | T02.08 AC (ordering) | `TestSymlinkResolvedContainment.test_raises_when_home_path_not_created` |
| `containment_guard` catches home_path symlink escape | T02.08 AC | `TestSymlinkResolvedContainment.test_raises_when_home_path_symlink_escapes_scratch_root`, `test_raises_on_symlink_chain_escape` (A→B→outside) |
| Allowlist source-of-truth = `EvalConfig.allowed_scratch_roots` (no hard-coded copy) | AC12 / FR-ISO2 | `TestScratchRootAllowlist.test_uses_evalconfig_allowed_scratch_roots_as_source_of_truth` |
| `HomeIsolation.setup` invokes guard AFTER mkdtemp | T02.08 AC | `TestIntegrationWithHomeIsolationSetup.test_setup_runs_containment_guard_after_mkdtemp` (spy on `home_path.exists()` at guard call time) |
| `HomeIsolation.setup` requires explicit config (no home_root injection) | NFR-SEC2 (this deliverable) | `TestIntegrationWithHomeIsolationSetup.test_setup_requires_explicit_config` (asserts `TypeError` + refusal-before-side-effects) |
| Partial HOME preserved on guard failure | NFR-ISO2 forensics | `TestIntegrationWithHomeIsolationSetup.test_setup_failure_preserves_partial_home` |
| Three checks are layered, not "first match wins" | FR-ISO2 | `TestIntegrationWithHomeIsolationSetup.test_setup_catches_symlink_escape_under_explicit_config`, `test_setup_propagates_eval_id_check_from_guard` |
| `HomeContainmentViolation` payload contract | Forensics | `TestHomeContainmentViolationPayload` (4 tests: check identifier, verbatim inputs, str() rendering, __cause__ chaining) |
| Guard does not touch real `~` | NFR-SEC3 sanity | `test_guard_does_not_write_under_real_home` |

## Reserved for follow-up tasks

| Open finding | Reserved to | Reason |
|---|---|---|
| Hook-deploy ordering (T02.14 not yet landed) | T02.14 | A sequence-recording fake for the hook adapter requires the adapter to exist. |
| TOCTOU rmdir-then-symlink under Barrier | T02.13 (atomic-setup wrapper) | The atomic wrapper is the natural place to pin TOCTOU semantics; the guard itself runs synchronously within `setup`. |
| `_materialize_home` test helper uses `mkdir` not `mkdtemp(prefix=…)` | Minor; test ergonomics | The integration tests do exercise the real `mkdtemp` path via `HomeIsolation.setup`. |
| Runtime guard on `HomeContainmentViolation.home_path` type | Low priority hardening | Constructor is internal-only; misuse would surface as the test that calls it. |

## Files touched

| File | Change |
|---|---|
| `src/superclaude/cli/eval/isolation.py` | Added `HomeContainmentViolation` and `containment_guard`; updated `HomeIsolation.setup` to require explicit `config` and invoke the guard AFTER mkdtemp. |
| `src/superclaude/cli/eval/__init__.py` | Exported `HomeContainmentViolation`, `containment_guard`. |
| `tests/cli/eval/test_path_containment.py` | New module (45 tests). |
| `tests/cli/eval/test_home_isolation_extend.py` | Added `permissive_config` fixture + `_config_for` helper; updated 29 callsites to pass explicit config (T02.07 contract follows the same wiring as production after the T02.08 hardening). |
