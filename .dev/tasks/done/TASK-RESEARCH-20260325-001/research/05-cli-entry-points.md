# Research: CLI Entry Points and Models

**Investigation type:** Integration Mapper
**Scope:** roadmap/commands.py, tasklist/commands.py, roadmap/models.py, tasklist/models.py
**Status:** Complete
**Date:** 2026-03-25

---

## `roadmap/commands.py`

### Full `superclaude roadmap run` parameter table

| Kind | Name | Type | Default | Help |
|---|---|---|---|---|
| argument | `spec_file` | `click.Path(exists=True, path_type=Path)` | required | positional spec file |
| option | `--agents` | string | `None` | Comma-separated agent specs: model[:persona] |
| option | `--output` → `output_dir` | `click.Path(path_type=Path)` | `None` | Output directory. Default: parent dir of spec-file |
| option | `--depth` | `click.Choice(["quick","standard","deep"])` | `None` | Debate round depth: quick=1, standard=2, deep=3 |
| option | `--resume` | flag | `False` | Skip passed steps; resume at first failing |
| option | `--dry-run` | flag | `False` | Print step plan and exit |
| option | `--model` | string | `""` | Override model for all steps |
| option | `--max-turns` | `int` | `100` | Max agent turns per claude subprocess |
| option | `--debug` | flag | `False` | Enable debug logging |
| option | `--no-validate` | flag | `False` | Skip post-pipeline validation |
| option | `--allow-regeneration` | flag | `False` | Allow patches exceeding diff-size threshold |
| option | `--retrospective` | `click.Path(exists=False, path_type=Path)` | `None` | Advisory retrospective file from prior release |

**Confirmed: NO `--input-type` flag exists.**

Command docstring says: "SPEC_FILE is the path to a specification markdown file." — explicitly spec-first.

### Where `--input-type [spec|tdd]` would be added

Using existing Click style:
```python
@click.option(
    "--input-type",
    type=click.Choice(["spec", "tdd"], case_sensitive=False),
    default="spec",
    help="Type of input file for roadmap generation. Default: spec.",
)
```

Add `input_type: str` to function signature. Add `"input_type": input_type` to `config_kwargs`.

### CLI-to-pipeline call chain

```
superclaude roadmap run <spec_file> [flags]
-> roadmap.commands.run(...)
-> RoadmapConfig(**config_kwargs)
-> roadmap.executor.execute_roadmap(config, ...)
-> _build_steps(config)
-> pipeline.executor.execute_pipeline(steps, config, run_step=roadmap_run_step, ...)
```

---

## `tasklist/commands.py`

### Full `superclaude tasklist validate` parameter table

| Kind | Name | Type | Default | Help |
|---|---|---|---|---|
| argument | `output_dir` | `click.Path(path_type=Path)` | required | directory where report is written |
| option | `--roadmap-file` | `click.Path(exists=True, path_type=Path)` | `None` | Path to roadmap file. Default: {output_dir}/roadmap.md |
| option | `--tasklist-dir` | `click.Path(exists=True, path_type=Path)` | `None` | Path to tasklist directory. Default: {output_dir}/ |
| option | `--model` | string | `""` | Override model for validation steps |
| option | `--max-turns` | `int` | `100` | Max agent turns |
| option | `--debug` | flag | `False` | Enable debug logging |

**Confirmed: NO `--spec` flag, NO `--tdd-file` flag, NO `--spec-file` flag.**

### Where `--tdd-file` would be added

```python
@click.option(
    "--tdd-file",
    type=click.Path(exists=True, path_type=Path),
    default=None,
    help="Path to the TDD file used as an additional validation input.",
)
```

Add `tdd_file: Path | None` to function signature. Add `tdd_file=tdd_file.resolve() if tdd_file is not None else None` to config construction.

### CLI-to-pipeline call chain

```
superclaude tasklist validate <output_dir> [flags]
-> tasklist.commands.validate(...)
-> TasklistValidateConfig(...)
-> tasklist.executor.execute_tasklist_validate(config)
-> _build_steps(config)
-> pipeline.executor.execute_pipeline(steps, config, run_step=tasklist_run_step)
```

---

## `roadmap/models.py` — RoadmapConfig

`RoadmapConfig` extends `PipelineConfig`.

### Inherited PipelineConfig fields

| Field | Type | Default |
|---|---|---|
| `work_dir` | `Path` | `Path(".")` |
| `dry_run` | `bool` | `False` |
| `max_turns` | `int` | `100` |
| `model` | `str` | `""` |
| `permission_flag` | `str` | `"--dangerously-skip-permissions"` |
| `debug` | `bool` | `False` |
| `grace_period` | `int` | `0` |

### RoadmapConfig declared fields

| Field | Type | Default |
|---|---|---|
| `spec_file` | `Path` | `Path(".")` |
| `agents` | `list[AgentSpec]` | `[AgentSpec("opus","architect"), AgentSpec("haiku","architect")]` |
| `depth` | `Literal["quick","standard","deep"]` | `"standard"` |
| `output_dir` | `Path` | `Path(".")` |
| `retrospective_file` | `Path | None` | `None` |
| `convergence_enabled` | `bool` | `False` |
| `allow_regeneration` | `bool` | `False` |

### Fields needed for TDD support

```python
input_type: Literal["spec", "tdd"] = "spec"
tdd_file: Path | None = None
```

**Would adding these fields automatically make them available in executor.py?** YES — executor.py imports `RoadmapConfig` and receives an instance: `execute_roadmap(config: RoadmapConfig, ...)`. New fields are immediately accessible as `config.input_type`, `config.tdd_file`. But executor code must explicitly use them — no automatic behavior change.

### Existing backward-compatible extension pattern

```python
# v3.05 extensions (FR-3, FR-6) — all defaulted for backward compatibility
convergence_enabled: bool = False
allow_regeneration: bool = False
```

This confirms the project accepts additive defaulted fields as the extension pattern.

---

## `tasklist/models.py` — TasklistValidateConfig

`TasklistValidateConfig` extends `PipelineConfig`.

### Declared fields (only)

| Field | Type | Default |
|---|---|---|
| `output_dir` | `Path` | `Path(".")` |
| `roadmap_file` | `Path` | `Path(".")` |
| `tasklist_dir` | `Path` | `Path(".")` |

(Plus all 7 inherited PipelineConfig fields)

### Fields needed for TDD support

```python
tdd_file: Path | None = None
```

Optionally:
```python
input_type: Literal["spec", "tdd"] = "spec"
```

### Does ValidateConfig have spec-file reference?

NO. `ValidateConfig` (roadmap/models.py) has only `output_dir` and `agents` — no spec file. `validate_executor.py` reads only `_REQUIRED_INPUTS = ("roadmap.md", "test-strategy.md", "extraction.md")` from `output_dir`. Roadmap validation is entirely artifact-based.

---

## TODO / NotImplemented / Feature Flag Search

**Found in all 4 files:** None.
- No `TODO` comments
- No `NotImplemented` markers
- No feature-flag framework

The project's real extension mechanisms are:
1. Additive Click options in commands.py
2. `config_kwargs` dict assembly in command functions
3. Backward-compatible defaulted fields in dataclasses (confirmed by `convergence_enabled`, `allow_regeneration`)

---

## Exact Code Patterns for New Flags/Fields

### Add `--input-type` to roadmap run
```python
@click.option(
    "--input-type",
    type=click.Choice(["spec", "tdd"], case_sensitive=False),
    default="spec",
    help="Type of input file for roadmap generation. Default: spec.",
)
```

### Add fields to `RoadmapConfig`
```python
input_type: Literal["spec", "tdd"] = "spec"
tdd_file: Path | None = None
```

### Add `--tdd-file` to tasklist validate
```python
@click.option(
    "--tdd-file",
    type=click.Path(exists=True, path_type=Path),
    default=None,
    help="Path to the TDD file used as an additional validation input.",
)
```

### Add `tdd_file` to `TasklistValidateConfig`
```python
tdd_file: Path | None = None
```

---

## Gaps and Questions

1. `spec_file` is named spec-specifically in both the CLI argument (`spec_file`) and `RoadmapConfig` field — rename to `input_file` for Option B (auto-detect) or leave as-is for Option A (explicit --input-type flag)
2. If `--input-type tdd` is passed with `superclaude roadmap run`, does `spec_file` positional name remain? Semantically awkward but backward compatible
3. For tasklist, `tdd_file` alone may suffice if roadmap remains primary anchor and TDD is supplemental; `input_type` may be unnecessary there
4. `ValidateConfig` and `validate_executor.py` would only need changes if `roadmap validate` must also reference the original TDD source — currently they are purely artifact-based

## Summary

- `superclaude roadmap run` has a positional `spec_file` and no `--input-type` flag. Clean extension point via additive `@click.option`.
- `superclaude tasklist validate` has no `--spec` or `--tdd-file` flag. Clean extension point.
- `RoadmapConfig` is easily extended with `input_type` and `tdd_file` fields using the project's established backward-compatible defaulted-field pattern.
- `TasklistValidateConfig` is minimal and easily extended with `tdd_file`.
- New dataclass fields are immediately available to executors (which receive config instances) but require explicit usage code in executor and prompt-builder functions.
- `ValidateConfig` (roadmap validation) has no spec-file reference and does not need changes unless roadmap validation itself must reference TDD source.
