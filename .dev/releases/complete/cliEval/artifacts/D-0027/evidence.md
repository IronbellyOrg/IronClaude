# D-0027 — Evidence (T02.05)

## Pristine run (2026-05-20)

Command:

```
uv run pytest tests/cli/eval/test_isolation_layers_probe.py -v
```

Result: **13 passed in 0.17s** — full log at
`.dev/releases/current/cliEval/evidence/T02.05/pytest.log`.

Test inventory (13):

1. `test_isolation_layers_is_dataclass`
2. `test_isolation_layers_lives_in_sprint_executor_module`
3. `test_isolation_layers_field_names_and_order`
4. `test_isolation_layers_field_types[scoped_work_dir-Path]`
5. `test_isolation_layers_field_types[git_boundary-Path]`
6. `test_isolation_layers_field_types[plugin_dir-Path]`
7. `test_isolation_layers_field_types[settings_dir-Path]`
8. `test_isolation_layers_env_vars_is_property`
9. `test_isolation_layers_env_vars_return_annotation_is_str_dict`
10. `test_isolation_layers_layers_active_is_property`
11. `test_isolation_layers_layers_active_return_annotation_is_list_str`
12. `test_setup_isolation_signature_pin`
13. `test_setup_isolation_module_path`

## Mutation check (synthetic refactor)

Procedure: backed up `src/superclaude/cli/sprint/executor.py`, renamed
`def layers_active` → `def layers_activeX`, re-ran the probe, then
restored the original via byte-identical copy and re-verified with
`diff`.

Mutated-run result excerpt:

```
tests/cli/eval/test_isolation_layers_probe.py::test_isolation_layers_layers_active_is_property FAILED
tests/cli/eval/test_isolation_layers_probe.py::test_isolation_layers_layers_active_return_annotation_is_list_str FAILED
...
========================= 2 failed, 11 passed in 0.23s =========================
```

Both failures surfaced as `AttributeError: layers_active` from
`inspect.getattr_static`, confirming the probe detects upstream method
rename. Restoration was verified via `diff`-clean exit and the probe
returning to 13/13 green. The mutation was never committed.

## Read-only verification

`grep -n "IsolationLayers(" tests/cli/eval/test_isolation_layers_probe.py`
returns no instance constructions; all surface inspection runs through
`dataclasses.fields`, `inspect.getattr_static`, `inspect.signature`,
and `typing.get_type_hints`.

## Cross-links

* Spec: `D-0027/spec.md`.
* Notes: `D-0027/notes.md`.
* Pinned upstream: `src/superclaude/cli/sprint/executor.py`
  (IsolationLayers + setup_isolation; lines 107–182).
* Downstream consumer: COMP-006 / T02.07 / T02.11 HomeIsolation
  extension.
