# D-0027 — IsolationLayers API surface probe spec

**Task:** T02.05 (Phase 2, Roadmap COMP-012 / R-027)
**Module:** `tests/cli/eval/test_isolation_layers_probe.py`
**Upstream pinned:** `src/superclaude/cli/sprint/executor.py` (IsolationLayers dataclass + `setup_isolation` factory; lines 107–182 at authoring time)
**Status:** Implemented 2026-05-20

## Purpose

COMP-012 is a read-only smoke test pinning the API surface of the existing
sprint `IsolationLayers` so the HomeIsolation extension (COMP-006 /
T02.07 / T02.11) fails fast if upstream renames a field, reorders the
record, drops a property, or changes the construction signature. The
probe constructs **no** `IsolationLayers` instance — every assertion
flows through `dataclasses.fields` and `inspect`, so the probe is safe
to run in parallel with any subprocess isolation work.

## Pinned surface

### `IsolationLayers` dataclass

| # | Field             | Annotated type | Source line (executor.py) |
|---|-------------------|----------------|---------------------------|
| 1 | `scoped_work_dir` | `pathlib.Path` | 120 |
| 2 | `git_boundary`    | `pathlib.Path` | 121 |
| 3 | `plugin_dir`      | `pathlib.Path` | 122 |
| 4 | `settings_dir`    | `pathlib.Path` | 123 |

Field order is asserted in `test_isolation_layers_field_names_and_order`
(tuple equality with the expected 4-tuple). Types are asserted per-field
via parametrised `test_isolation_layers_field_types`.

### Properties

| Property        | Type           | Annotated return  | Pinned by |
|-----------------|----------------|-------------------|-----------|
| `env_vars`      | `property`     | `dict[str, str]`  | `test_isolation_layers_env_vars_is_property` + `test_isolation_layers_env_vars_return_annotation_is_str_dict` |
| `layers_active` | `property`     | `list[str]`       | `test_isolation_layers_layers_active_is_property` + `test_isolation_layers_layers_active_return_annotation_is_list_str` |

Property detection uses `inspect.getattr_static(IsolationLayers, name)`
to avoid invoking the descriptor (no `IsolationLayers` instance is
required). Return annotations are read with `typing.get_type_hints` on
the underlying `fget`.

### `setup_isolation` factory

| Aspect             | Pin |
|--------------------|-----|
| Parameter names    | `("config",)` |
| Parameter kind     | `POSITIONAL_OR_KEYWORD` |
| Return annotation  | `IsolationLayers` |
| Module path        | `superclaude.cli.sprint.executor` |

Captured by `test_setup_isolation_signature_pin` and
`test_setup_isolation_module_path`.

### Module-identity pins

* `IsolationLayers.__module__ == "superclaude.cli.sprint.executor"`
  (`test_isolation_layers_lives_in_sprint_executor_module`).
* `dataclasses.is_dataclass(IsolationLayers) is True`
  (`test_isolation_layers_is_dataclass`).

## Acceptance criteria → implementation map

| AC bullet (T02.05) | Implementation site |
|--------------------|---------------------|
| File `tests/cli/eval/test_isolation_layers_probe.py` exists and asserts the IsolationLayers API surface against `cli/sprint/executor.py:107-182`. | `tests/cli/eval/test_isolation_layers_probe.py` — 13 tests across the field, property, and factory surfaces. |
| Test passes against the current tree and fails on a synthetic mutation of a pinned method signature. | Mutation test on 2026-05-20 renamed `layers_active` to `layers_activeX`; the two `layers_active` probes failed loudly (`AttributeError`). Mutation reverted; pristine run is green (see evidence). |
| Test is read-only (no IsolationLayers instances are constructed; uses `inspect`). | All assertions use `dataclasses.fields`, `typing.get_type_hints`, and `inspect.getattr_static` / `inspect.signature`. No `IsolationLayers(...)` call anywhere in the probe file. |
| `TASKLIST_ROOT/artifacts/D-0027/spec.md` records the pinned surface. | This file. |

## Failure interpretation playbook

If this probe fails after upstream refactor:

1. Re-read `src/superclaude/cli/sprint/executor.py` around the
   IsolationLayers definition; confirm whether the refactor is
   intentional and aligned with HomeIsolation extension.
2. If intentional, update the 4-field expectation in
   `_EXPECTED_FIELDS` and any drifted property/signature pin in lockstep
   with the new surface, then re-bump this spec.
3. If unintentional (rename slipped in during unrelated work), revert
   upstream rather than relaxing the probe.

## Out of scope for T02.05

* HomeIsolation extension behaviour (`setup`, `env`, `teardown`,
  `state_path`) — COMP-006 / T02.07 / T02.11.
* Containment guard / FR-ISO2 — T02.08.
* Construction of IsolationLayers instances or actual isolation effects
  (this probe is intentionally inert).
