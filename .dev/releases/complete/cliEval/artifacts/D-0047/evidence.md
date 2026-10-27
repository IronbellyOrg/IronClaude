# D-0047 — EvalContext evidence

## Test execution

```
$ uv run pytest tests/cli/eval/test_eval_context.py -v
============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-9.0.3, pluggy-1.6.0
collected 29 items

tests/cli/eval/test_eval_context.py::test_eval_context_has_required_fields PASSED
tests/cli/eval/test_eval_context.py::test_eval_context_field_order_constant_matches_dataclass PASSED
tests/cli/eval/test_eval_context.py::test_eval_context_is_frozen PASSED
tests/cli/eval/test_eval_context.py::test_eval_context_every_field_is_frozen[eval_spec] PASSED
tests/cli/eval/test_eval_context.py::test_eval_context_every_field_is_frozen[home] PASSED
tests/cli/eval/test_eval_context.py::test_eval_context_every_field_is_frozen[home_path] PASSED
tests/cli/eval/test_eval_context.py::test_eval_context_every_field_is_frozen[artifacts_dir] PASSED
tests/cli/eval/test_eval_context.py::test_eval_context_every_field_is_frozen[run_dir] PASSED
tests/cli/eval/test_eval_context.py::test_eval_context_every_field_is_frozen[env] PASSED
tests/cli/eval/test_eval_context.py::test_eval_context_every_field_is_frozen[stdout_path] PASSED
tests/cli/eval/test_eval_context.py::test_eval_context_every_field_is_frozen[stderr_path] PASSED
tests/cli/eval/test_eval_context.py::test_eval_context_every_field_is_frozen[transcript_path] PASSED
tests/cli/eval/test_eval_context.py::test_eval_context_every_field_is_frozen[jsonl_paths] PASSED
tests/cli/eval/test_eval_context.py::test_eval_context_every_field_is_frozen[exit_code] PASSED
tests/cli/eval/test_eval_context.py::test_eval_context_every_field_is_frozen[stdout] PASSED
tests/cli/eval/test_eval_context.py::test_eval_context_every_field_is_frozen[stderr] PASSED
tests/cli/eval/test_eval_context.py::test_eval_context_every_field_is_frozen[duration_sec] PASSED
tests/cli/eval/test_eval_context.py::test_eval_context_every_field_is_frozen[artifacts] PASSED
tests/cli/eval/test_eval_context.py::test_eval_context_env_is_mapping_proxy PASSED
tests/cli/eval/test_eval_context.py::test_eval_context_jsonl_paths_is_mapping_proxy PASSED
tests/cli/eval/test_eval_context.py::test_eval_context_artifacts_is_mapping_proxy PASSED
tests/cli/eval/test_eval_context.py::test_eval_context_direct_construction_also_wraps_mappings PASSED
tests/cli/eval/test_eval_context.py::test_eval_context_factory_isolates_env_from_caller_mutation PASSED
tests/cli/eval/test_eval_context.py::test_from_runner_state_resolves_home_path_from_home PASSED
tests/cli/eval/test_eval_context.py::test_from_runner_state_raises_when_home_not_setup PASSED
tests/cli/eval/test_eval_context.py::test_from_runner_state_keyword_only_arguments PASSED
tests/cli/eval/test_eval_context.py::test_from_runner_state_is_deterministic PASSED
tests/cli/eval/test_eval_context.py::test_from_runner_state_field_values_round_trip PASSED
tests/cli/eval/test_eval_context.py::test_eval_context_reexported_from_package PASSED

============================== 29 passed in 0.14s ==============================
```

Raw run preserved at `.dev/releases/current/cliEval/evidence/T03.03/test-output.txt`.

## Regression sweep across sibling models

```
$ uv run pytest tests/cli/eval/test_eval_outcome.py tests/cli/eval/test_eval_result.py \
                tests/cli/eval/test_eval_context.py tests/cli/eval/test_expect_result.py \
                tests/cli/eval/test_expect_failure.py -q
94 passed in 0.22s
```

EvalOutcome (T03.01), EvalResult (T03.02), ExpectResult (T01.15), and ExpectFailure (T01.16) all continue to pass; the new `EvalContext` does not regress any sibling model.

## Manual validation (per task Validation step)

> Manual check: build an EvalContext via factory and assert immutability.

```python
>>> import tempfile
>>> from pathlib import Path
>>> from superclaude.cli.eval import EvalContext, EvalSpec, HomeIsolation
>>> from superclaude.cli.eval.config import EvalConfig
>>> root = Path(tempfile.mkdtemp())
>>> home = HomeIsolation(eval_id="E1", home_root=root, session_id="sess-001")
>>> _ = home.setup(config=EvalConfig(allowed_scratch_roots=(root,)))
>>> ctx = EvalContext.from_runner_state(
...     eval_spec=EvalSpec(id="E1", title="example"),
...     home=home,
...     run_dir=root,
...     artifacts_dir=home.home_path,
...     stdout_path=home.home_path / "stdout.log",
...     stderr_path=home.home_path / "stderr.log",
...     transcript_path=home.home_path / "pty.transcript",
...     jsonl_paths={},
...     env={"HOME": str(home.home_path)},
...     exit_code=0,
...     stdout="",
...     stderr="",
...     duration_sec=0.0,
...     artifacts={},
... )
>>> ctx.home_path == home.home_path
True
>>> try:
...     ctx.exit_code = 1
... except Exception as exc:
...     print(type(exc).__name__)
FrozenInstanceError
>>> try:
...     ctx.env["HOME"] = "/tmp/elsewhere"
... except Exception as exc:
...     print(type(exc).__name__)
TypeError
```

Both the frozen-attribute guard and the mapping-proxy guard fire as expected. The same shapes are exercised by `test_eval_context_is_frozen`, `test_eval_context_every_field_is_frozen[exit_code]`, and `test_eval_context_env_is_mapping_proxy`.

## Artifacts produced

- `src/superclaude/cli/eval/models.py` — new `EvalContext` frozen dataclass + `_EVAL_CONTEXT_FIELDS` constant + `EvalContext.from_runner_state` classmethod; new imports for `pathlib.Path`, `types.MappingProxyType`, and `TYPE_CHECKING`-guarded `HomeIsolation`.
- `src/superclaude/cli/eval/__init__.py` — `EvalContext` added to imports + `__all__`.
- `tests/cli/eval/test_eval_context.py` — 29 new tests (12 frozen-field parametrisations + 17 unique scenarios) covering field schema, frozen contract, mapping-proxy immutability, factory determinism, kwarg-only enforcement, home-path resolution, RuntimeError propagation, round-trip kwarg values, and package re-export.
- `.dev/releases/current/cliEval/artifacts/D-0047/{spec,notes,evidence}.md` — this deliverable.
- `.dev/releases/current/cliEval/evidence/T03.03/test-output.txt` — pytest verbose run.

## Acceptance criteria status

| Criterion (T03.03)                                                                                              | Status | Evidence |
|-----------------------------------------------------------------------------------------------------------------|--------|----------|
| Class `EvalContext` is frozen and exposes the 15 fields named in DM-010.                                        | PASS   | `test_eval_context_has_required_fields`, `test_eval_context_is_frozen` |
| `EvalContext` instances reject mutation (FrozenInstanceError on attempted set).                                 | PASS   | `test_eval_context_every_field_is_frozen[*]` (15 parametrisations) |
| `from_runner_state()` constructs an EvalContext from EvalSpec + HomeIsolation + run outputs deterministically.  | PASS   | `test_from_runner_state_is_deterministic`, `test_from_runner_state_field_values_round_trip`, `test_from_runner_state_resolves_home_path_from_home` |
| `TASKLIST_ROOT/artifacts/D-0047/spec.md` records the contract.                                                  | PASS   | `artifacts/D-0047/spec.md` (this deliverable) |
