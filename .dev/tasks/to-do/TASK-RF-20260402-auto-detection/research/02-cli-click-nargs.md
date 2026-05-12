# Research: Click nargs=-1 Behavior and CLI Changes

**Researcher**: researcher-2
**Date**: 2026-04-01
**Scope**: `src/superclaude/cli/roadmap/commands.py` and Click library documentation
**Track Goal**: Change CLI to accept multiple positional file args that get auto-detected and routed

---

## 1. Current CLI State

**File**: `src/superclaude/cli/roadmap/commands.py`

### Current Argument Declaration (line 33)
```python
@click.argument("spec_file", type=click.Path(exists=True, path_type=Path))
```

### Current Function Signature (lines 134-151)
```python
def run(
    ctx: click.Context,
    spec_file: Path,          # single positional arg
    agents: str | None,
    ...
    input_type: str,          # line 148 — Choice(["auto", "tdd", "spec"])
    tdd_file: Path | None,    # line 149 — explicit --tdd-file option
    prd_file: Path | None,    # line 150 — explicit --prd-file option
) -> None:
```

### Current Model Field (models.py line 102)
```python
spec_file: Path = field(default_factory=lambda: Path("."))
```

### Current --input-type (line 107)
```python
type=click.Choice(["auto", "tdd", "spec"], case_sensitive=False)
```

### Key Downstream Consumers of `spec_file`
From `executor.py` grep results, `config.spec_file` is referenced in **30+ locations** including:
- `detect_input_type(spec_file)` (line 63) — auto-detection
- `spec_file.read_text()` (lines 319, 367) — content reading
- `hashlib.sha256(config.spec_file.read_bytes())` (lines 1708, 2109, 2310, 2333, 2647) — spec hashing for resume
- `config.spec_file.name` (line 633) — logging
- Step input lists (line 1174): `inputs=[config.spec_file] + ([config.tdd_file] if config.tdd_file else []) + ...`

**Impact assessment**: `config.spec_file` is deeply woven into executor.py. A rename to `input_files` on the model would require 30+ edits in executor.py alone. The safer approach is to keep `spec_file` on the model and do routing at the CLI layer.

---

## 2. Click nargs=-1 Behavior (from official docs)

### Core Mechanics
Source: [Click docs — arguments.md](https://github.com/pallets/click/blob/main/docs/arguments.md)

- `nargs=-1` makes a positional argument **variadic**: it consumes all remaining positional values.
- The result is passed to the function as a **tuple**, not a list.
- A variadic argument can only appear **once** per command, and must be the **last** `@click.argument`.
- `nargs=-1` can coexist with `nargs=1` arguments before it.

### Type Parameter with nargs=-1
```python
@click.argument('files', nargs=-1, type=click.Path())
```
The `type` applies to **each individual element** in the tuple. So `type=click.Path(exists=True, path_type=Path)` validates each file independently and converts each to a `Path` object. The function receives `tuple[Path, ...]`.

### Interaction with Options
From the Click documentation and examples:
- `@click.option(...)` decorators can appear in **any order** relative to `@click.argument(...)` — Click separates options (prefixed with `--`) from positional arguments at parse time.
- `nargs=-1` does NOT consume `--option value` pairs; Click's parser distinguishes them.
- Confirmed by the `timeit_args` example: `@click.option('-v', '--verbose', ...)` works alongside `@click.argument('timeit_args', nargs=-1, ...)`.

### Important: nargs=-1 Accepts Zero Arguments by Default
`nargs=-1` allows **zero or more** arguments. Passing zero files is valid and produces an empty tuple `()`. There is no built-in `required=True` semantic for variadic arguments — **validation of min/max count must be done manually in the function body**.

Note: Click does have `required=True` for `nargs=-1` which changes behavior to require at least 1 argument. From Click source: when `required=True` and `nargs=-1`, Click raises `MissingParameter` if zero values given.

### Backward Compatibility
`superclaude roadmap run single-file.md` still works because:
- One positional arg produces a tuple of length 1: `("single-file.md",)`.
- The function receives `input_files = (Path("single-file.md"),)`.
- Existing single-file usage maps to `input_files[0]`.

---

## 3. Exact Code Change for Argument Decorator

### Before (line 33)
```python
@click.argument("spec_file", type=click.Path(exists=True, path_type=Path))
```

### After
```python
@click.argument("input_files", nargs=-1, required=True, type=click.Path(exists=True, path_type=Path))
```

Key decisions:
- **`required=True`**: Ensures at least 1 file is provided (Click raises error on 0 files).
- **`type=click.Path(exists=True, path_type=Path)`**: Validates each file individually. Each element in the tuple is a resolved `Path` object.
- **Name `input_files`**: Descriptive of the multi-file intent.

---

## 4. Function Signature Change

### Before (line 134-136)
```python
def run(
    ctx: click.Context,
    spec_file: Path,
```

### After
```python
def run(
    ctx: click.Context,
    input_files: tuple[Path, ...],
```

The parameter name **must match** the `@click.argument` name exactly (Click maps by name).

---

## 5. Validation: 1-3 Files

Click's `required=True` handles the 0-file case. For the upper bound (max 3 files), add a manual check at the top of `run()`:

```python
def run(
    ctx: click.Context,
    input_files: tuple[Path, ...],
    ...
) -> None:
    """Run the roadmap generation pipeline on INPUT_FILES.

    INPUT_FILES are one to three markdown files (spec, TDD, PRD).
    Each file is auto-detected and routed to the appropriate pipeline role.
    """
    # Validate file count
    if len(input_files) > 3:
        raise click.UsageError(
            f"Expected 1-3 input files, got {len(input_files)}. "
            "Provide at most one spec, one TDD, and one PRD."
        )
```

Note: `click.UsageError` is the idiomatic Click way to report usage violations. It prints the error with the command's help text.

---

## 6. Interaction with --tdd-file and --prd-file Flags

### Current State
- `--tdd-file` (line 112-121): Explicit TDD file for supplementary context.
- `--prd-file` (line 122-132): Explicit PRD file for business context.

### Proposed Interaction Logic
The positional args and explicit flags should work together with a **merge-and-deduplicate** strategy:

```python
# After auto-detection routes positional args to roles...
# (detection logic is researcher-1/researcher-3's scope)

# Explicit flags override/supplement positional detection
if tdd_file is not None:
    # --tdd-file always wins for TDD role
    resolved_tdd = tdd_file
if prd_file is not None:
    # --prd-file always wins for PRD role
    resolved_prd = prd_file
```

### Conflict Resolution Rules
1. If a positional arg is detected as TDD AND `--tdd-file` is also provided: **error** (ambiguous).
2. If a positional arg is detected as PRD AND `--prd-file` is also provided: **error** (ambiguous).
3. Single positional + explicit flags: works exactly like today (backward compatible).

```python
# Conflict detection
if detected_tdd_from_positional and tdd_file is not None:
    raise click.UsageError(
        f"Conflict: '{detected_tdd_from_positional}' was auto-detected as TDD, "
        f"but --tdd-file='{tdd_file}' was also provided. "
        "Use --input-type to override detection, or remove the duplicate."
    )
```

---

## 7. --input-type Expansion

### Current (line 107)
```python
type=click.Choice(["auto", "tdd", "spec"], case_sensitive=False)
```

### Required Change
Add `"prd"` to the choice list:
```python
type=click.Choice(["auto", "tdd", "spec", "prd"], case_sensitive=False)
```

### Semantic Change
With multiple positional files, `--input-type` becomes ambiguous — it can't force all files to one type. Two options:

**Option A (Recommended)**: `--input-type` applies to the **first** positional file only. Additional files are always auto-detected. This preserves backward compatibility: `superclaude roadmap run file.md --input-type tdd` still works exactly as before.

**Option B**: Deprecate `--input-type` for multi-file mode and require explicit `--tdd-file`/`--prd-file` for overrides. This is cleaner but breaks the existing interface semantic.

**Recommendation**: Option A. It's backward compatible and intuitive for single-file usage.

### Model Change (models.py line 114)
```python
input_type: Literal["auto", "tdd", "spec", "prd"] = "auto"
```

---

## 8. Concrete Code Sketch: Modified commands.py

```python
@roadmap_group.command()
@click.argument("input_files", nargs=-1, required=True, type=click.Path(exists=True, path_type=Path))
@click.option(
    "--agents",
    default=None,
    help=(
        "Comma-separated agent specs: model[:persona]. "
        "Default: opus:architect,haiku:architect"
    ),
)
@click.option(
    "--output",
    "output_dir",
    type=click.Path(path_type=Path),
    default=None,
    help="Output directory for all artifacts. Default: parent dir of first input file.",
)
@click.option(
    "--depth",
    type=click.Choice(["quick", "standard", "deep"], case_sensitive=False),
    default=None,
    help="Debate round depth: quick=1, standard=2, deep=3. Default: standard.",
)
@click.option("--resume", is_flag=True, help="Skip steps whose outputs already pass their gates.")
@click.option("--dry-run", is_flag=True, help="Print step plan and gate criteria, then exit.")
@click.option("--model", default="", help="Override model for all steps.")
@click.option("--max-turns", type=int, default=100, help="Max agent turns per subprocess.")
@click.option("--debug", is_flag=True, help="Enable debug logging.")
@click.option("--no-validate", is_flag=True, help="Skip post-pipeline validation.")
@click.option("--allow-regeneration", is_flag=True, default=False, help="Allow patches exceeding diff-size threshold.")
@click.option(
    "--retrospective",
    type=click.Path(exists=False, path_type=Path),
    default=None,
    help="Path to retrospective file from prior release cycle.",
)
@click.option(
    "--input-type",
    type=click.Choice(["auto", "tdd", "spec", "prd"], case_sensitive=False),
    default="auto",
    help=(
        "Force input type for the first positional file. "
        "auto=detect from content. Additional files always auto-detected. "
        "Default: auto."
    ),
)
@click.option(
    "--tdd-file",
    type=click.Path(exists=True, path_type=Path),
    default=None,
    help="Explicit TDD file (overrides positional auto-detection for TDD role).",
)
@click.option(
    "--prd-file",
    type=click.Path(exists=True, path_type=Path),
    default=None,
    help="Explicit PRD file (overrides positional auto-detection for PRD role).",
)
@click.pass_context
def run(
    ctx: click.Context,
    input_files: tuple[Path, ...],
    agents: str | None,
    output_dir: Path | None,
    depth: str | None,
    resume: bool,
    dry_run: bool,
    model: str,
    max_turns: int,
    debug: bool,
    no_validate: bool,
    allow_regeneration: bool,
    retrospective: Path | None,
    input_type: str,
    tdd_file: Path | None,
    prd_file: Path | None,
) -> None:
    """Run the roadmap generation pipeline on INPUT_FILES.

    INPUT_FILES are 1-3 markdown files (spec, TDD, PRD) that are
    auto-detected and routed to the appropriate pipeline role.

    Examples:
        superclaude roadmap run spec.md
        superclaude roadmap run spec.md tdd.md
        superclaude roadmap run spec.md tdd.md prd.md
        superclaude roadmap run spec.md --tdd-file=tdd.md --prd-file=prd.md
    """
    from .executor import execute_roadmap, detect_input_type
    from .models import AgentSpec, RoadmapConfig

    # --- Validate file count (1-3) ---
    if len(input_files) > 3:
        raise click.UsageError(
            f"Expected 1-3 input files, got {len(input_files)}. "
            "Provide at most one spec, one TDD, and one PRD."
        )

    # --- Route positional files to roles ---
    # NOTE: Actual routing logic is researcher-3's scope.
    # This sketch shows the CLI-layer structure only.
    spec_file: Path | None = None
    detected_tdd: Path | None = None
    detected_prd: Path | None = None

    if len(input_files) == 1:
        # Single file: backward-compatible behavior
        spec_file = input_files[0]
        # input_type override applies to this file (existing behavior)
    else:
        # Multi-file: auto-detect and route each
        # (researcher-3 defines route_input_files() in executor.py)
        from .executor import route_input_files  # NEW function
        routing = route_input_files(input_files, input_type_override=input_type)
        spec_file = routing["spec"]
        detected_tdd = routing.get("tdd")
        detected_prd = routing.get("prd")

    # --- Conflict detection: positional vs explicit flags ---
    if detected_tdd is not None and tdd_file is not None:
        raise click.UsageError(
            f"Conflict: '{detected_tdd.name}' was auto-detected as TDD, "
            f"but --tdd-file='{tdd_file}' was also provided. Remove one."
        )
    if detected_prd is not None and prd_file is not None:
        raise click.UsageError(
            f"Conflict: '{detected_prd.name}' was auto-detected as PRD, "
            f"but --prd-file='{prd_file}' was also provided. Remove one."
        )

    # --- Merge: positional detection + explicit flags ---
    final_tdd = tdd_file or detected_tdd
    final_prd = prd_file or detected_prd

    # --- Resolve output directory ---
    # Default to parent of first input file (backward compatible)
    resolved_output = output_dir if output_dir is not None else input_files[0].parent

    # --- Build config (spec_file stays as primary, tdd/prd as supplements) ---
    # ... (rest of existing config_kwargs logic, replacing spec_file source)
    config_kwargs: dict = {
        "spec_file": spec_file.resolve(),
        "output_dir": resolved_output.resolve(),
        "work_dir": resolved_output.resolve(),
        "dry_run": dry_run,
        "max_turns": max_turns,
        "model": model,
        "debug": debug,
        "retrospective_file": retro_path,
        "allow_regeneration": allow_regeneration,
        "input_type": input_type,
        "tdd_file": final_tdd.resolve() if final_tdd is not None else None,
        "prd_file": final_prd.resolve() if final_prd is not None else None,
    }
    # ... remainder unchanged
```

---

## 9. Summary of All Changes Required

| File | Change | Lines Affected |
|------|--------|----------------|
| `commands.py` line 33 | `@click.argument("spec_file", ...)` -> `@click.argument("input_files", nargs=-1, required=True, ...)` | 1 line |
| `commands.py` line 107 | Add `"prd"` to `--input-type` Choice | 1 line |
| `commands.py` lines 134-136 | `spec_file: Path` -> `input_files: tuple[Path, ...]` | 1 line |
| `commands.py` lines 152-244 | Routing logic, conflict detection, merge | ~30 lines new |
| `commands.py` line 176 | Output dir default: `spec_file.parent` -> `input_files[0].parent` | 1 line |
| `models.py` line 114 | Add `"prd"` to `input_type` Literal | 1 line |
| `commands.py` help text | Update docstrings for new multi-file behavior | ~5 lines |

### NOT Changed (intentionally)
- **`models.py` `spec_file` field**: Stays as `spec_file: Path` to avoid 30+ changes in executor.py. The CLI routes the "primary spec" into this field regardless of how many positional files were given.
- **`executor.py` `detect_input_type()`**: Stays as-is. A new `route_input_files()` function wraps it for multi-file routing (researcher-3's scope).
- **`--tdd-file` and `--prd-file` options**: Kept for backward compatibility and explicit override use cases.

---

## 10. Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| Zero-file invocation | Low | `required=True` on nargs=-1 handles this |
| >3 files | Low | Manual validation in function body |
| Backward compatibility | Low | Single-file usage produces `(Path(...),)` tuple; `input_files[0]` maps to old `spec_file` |
| Options consumed by nargs=-1 | None | Click separates `--options` from positional args at parse time |
| Help text regression | Low | Update docstring examples to show multi-file usage |
| --input-type semantic ambiguity | Medium | Apply only to first file; document clearly |
| Positional vs flag conflict | Medium | Explicit conflict detection with clear error messages |
| Resume state compatibility | Medium | `config.spec_file` stays as primary; state.json still hashes one file. Multi-file hashing is a follow-on concern. |
