# T02.08 — Evidence (Deliverable D-0029)

**Task**: Implement FR-ISO2 path containment guard (security-critical)
**Tier**: STRICT
**Risk**: High
**Sub-agent delegation**: Required (quality-engineer); review completed with PASS verdict on the blocker.

## Acceptance-criteria check

| Criterion | Result |
|---|---|
| `containment_guard(home_path, scratch_root, eval_id)` raises `HomeContainmentViolation` when any of the three checks fails | PASS — `src/superclaude/cli/eval/isolation.py:170-299` |
| Integrated into `HomeIsolation.setup()` AFTER mkdtemp, BEFORE hook deploy | PASS — `src/superclaude/cli/eval/isolation.py:447,466` |
| Three checks: (1) eval_id regex via `validate_eval_id`, (2) `home_path.is_relative_to(scratch_root)` after symlink resolution, (3) scratch_root not symlinked to non-allowlisted target | PASS — `containment_guard` implements all three with distinct `check` identifiers |
| Symlink resolution AFTER mkdtemp BEFORE hook deploy | PASS — `test_setup_runs_containment_guard_after_mkdtemp` spies on `home_path.exists()` at guard call time |
| Allowlist sourced from `EvalConfig.allowed_scratch_roots`, not hard-coded | PASS — `test_uses_evalconfig_allowed_scratch_roots_as_source_of_truth` |
| D-0029 spec.md records the method contract | PASS — `.dev/releases/current/cliEval/artifacts/D-0029/spec.md` |
| Quality-engineer review (STRICT tier) | PASS — re-review verdict on Issue #1 blocker; see `artifacts/D-0029/evidence.md` |

## Test results

`uv run pytest tests/cli/eval/test_path_containment.py tests/cli/eval/test_home_isolation_extend.py -v`

Result: **85 passed in 0.24s** — see `pytest-T02.08.log`.

Full eval suite (`uv run pytest tests/cli/eval/ -q`) — **449 passed in 1.01s**.

## Implementation note: bypass surface closed

A predecessor draft of `HomeIsolation.setup()` accepted `config: EvalConfig | None = None` and, when `None`, synthesized:

```python
EvalConfig(
    allowed_scratch_roots=(self.home_root, *EvalConfig().allowed_scratch_roots),
)
```

The quality-engineer correctly flagged this as defeating AC12: `HomeIsolation.__post_init__` does NOT validate `home_root`, so a caller could construct `HomeIsolation(eval_id="E1", home_root=Path("/home/user/.claude"), ...)` and have `setup()` inject `/home/user/.claude` into the allowlist, then trivially pass check 2.

**Fix**: `config` is now required (no `None` default, no fallback synthesis) on both `containment_guard` and `HomeIsolation.setup`. A missing argument is a `TypeError` at argument-binding time, before any filesystem operation runs. Asserted by `test_setup_requires_explicit_config`:

```python
with pytest.raises(TypeError, match=r"config"):
    iso.setup()
assert not any(scratch_root.iterdir())  # refusal-before-side-effects
```

## Files changed

* `src/superclaude/cli/eval/isolation.py` — module docstring extended; `HomeContainmentViolation` + `containment_guard` added; `HomeIsolation.setup` requires explicit `config` and invokes guard AFTER mkdtemp.
* `src/superclaude/cli/eval/__init__.py` — exports `HomeContainmentViolation`, `containment_guard`.
* `tests/cli/eval/test_path_containment.py` — new test module (47 tests).
* `tests/cli/eval/test_home_isolation_extend.py` — added `permissive_config` fixture + `_config_for` helper; updated 29 `iso.setup()` callsites to pass explicit `config=permissive_config` (mirrors production orchestrator wiring T03.16).
* `.dev/releases/current/cliEval/artifacts/D-0029/{spec,notes,evidence}.md` — D-0029 deliverable artifacts.

## Files NOT changed (confirms preservation)

* `src/superclaude/cli/sprint/executor.py` — `IsolationLayers` untouched (T02.05 probe still passes).
* `src/superclaude/cli/eval/config.py` — `EvalConfig` / `resolve_scratch_root` / `ScratchRootViolation` untouched.
* `src/superclaude/cli/eval/loader.py` — `validate_eval_id` / `InvalidEvalId` untouched.

## Reserved for follow-up tasks

| Open finding (from QA review) | Reserved to | Reason |
|---|---|---|
| Sequence-recording fake pinning hook-deploy ordering | T02.14 | Hook adapter doesn't exist yet. |
| TOCTOU rmdir-then-symlink test under Barrier | T02.13 | Atomic-setup wrapper is the natural place. |
| `_materialize_home` helper to use `mkdtemp(prefix=…)` | Minor / test ergonomics | Real `mkdtemp` path exercised via integration tests. |
| Runtime guard on `HomeContainmentViolation.home_path` field type | Low priority hardening | Constructor is internal-only. |
