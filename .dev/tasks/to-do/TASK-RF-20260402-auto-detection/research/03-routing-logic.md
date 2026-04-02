# Research 03: Routing Logic and Code Path Analysis

**Researcher**: researcher-3
**Scope**: `src/superclaude/cli/roadmap/executor.py` — detection, routing, guards, state file, execute_roadmap
**Goal**: Map all code paths that need changes for multi-file routing. Design `_route_input_files()`.

---

## 1. Current Architecture: Single-File Input

### 1.1 CLI Entry Point (commands.py)

The `run` command currently accepts a single positional argument:

```
@click.argument("spec_file", type=click.Path(exists=True, path_type=Path))
```
**File**: `src/superclaude/cli/roadmap/commands.py`, line 33

Plus two explicit supplementary flags:
- `--tdd-file` (line 112-120)
- `--prd-file` (line 122-132)
- `--input-type` with choices `["auto", "tdd", "spec"]` (line 106-109)

The CLI builds `config_kwargs` with:
- `spec_file` = positional arg resolved (line 195)
- `tdd_file` = `--tdd-file` resolved or None (line 205)
- `prd_file` = `--prd-file` resolved or None (line 206)
- `input_type` = `--input-type` value (line 204)

### 1.2 RoadmapConfig Data Model (models.py)

**File**: `src/superclaude/cli/roadmap/models.py`, lines 94-116

```python
@dataclass
class RoadmapConfig(PipelineConfig):
    spec_file: Path = field(default_factory=lambda: Path("."))
    input_type: Literal["auto", "tdd", "spec"] = "auto"
    tdd_file: Path | None = None
    prd_file: Path | None = None
    # ... other fields
```

Key observations:
- `input_type` is `Literal["auto", "tdd", "spec"]` — **needs "prd" added** if PRD-primary becomes supported
- `spec_file` is always required (no `None` allowed) — it's the "primary input" regardless of type
- `tdd_file` and `prd_file` are supplementary slots

### 1.3 detect_input_type() (executor.py, lines 63-133)

Classifies a single file as `"tdd"` or `"spec"` using weighted signals:
1. Numbered section headings (`## N.` pattern) — score +1 to +3
2. TDD-exclusive frontmatter fields (`parent_doc`, `coordinator`) — +2 each
3. TDD-specific section names (8 keywords) — +1 each
4. Frontmatter type field containing "Technical Design Document" — +2

Threshold: score >= 5 = TDD, else spec. Borderline warning at scores 3-6.

**Critical gap**: No PRD detection. The function returns only `"tdd"` or `"spec"`. A PRD file would be classified as `"spec"` (score likely 0-2).

---

## 2. execute_roadmap() Code Paths

**File**: `src/superclaude/cli/roadmap/executor.py`, lines 2061-2222

### 2.1 Auto-Resolution Block (lines 2113-2116)

```python
if config.input_type == "auto":
    resolved = detect_input_type(config.spec_file)
    _log.info("Resolved input_type=auto to '%s' for %s", resolved, config.spec_file)
    config = dataclasses.replace(config, input_type=resolved)
```

This resolves auto-detection on `config.spec_file` only. With multi-file input, this needs to iterate over all positional files.

### 2.2 Same-File Guard (lines 2124-2135)

```python
if (
    config.tdd_file is not None
    and config.prd_file is not None
    and config.tdd_file.resolve() == config.prd_file.resolve()
):
    _log.error(...)
    raise SystemExit(1)
```

Prevents `--tdd-file` and `--prd-file` from being the same file. This guard needs expansion to cover all file slot pairs (spec vs tdd, spec vs prd, tdd vs prd).

### 2.3 Redundancy Guard (lines 2139-2144)

```python
if config.input_type == "tdd" and config.tdd_file is not None:
    _log.warning(
        "Ignoring --tdd-file: primary input is already a TDD document."
    )
    config = dataclasses.replace(config, tdd_file=None)
```

When primary input is TDD, supplementary `--tdd-file` is redundant and nulled. This pattern should extend: if a positional file auto-detects as TDD and fills the `tdd_file` slot, an explicit `--tdd-file` is redundant.

### 2.4 TDD/PRD Logging (lines 2118-2122)

```python
if config.tdd_file is not None:
    _log.info("TDD file provided: %s", config.tdd_file)
if config.prd_file is not None:
    _log.info("PRD file provided: %s", config.prd_file)
```

Simple debug logging. Should be updated to log all resolved slots after routing.

### 2.5 Spec-Patch Resume Cycle (lines 2362-2364)

```python
if config.input_type == "auto":
    resolved = detect_input_type(config.spec_file)
    config = dataclasses.replace(config, input_type=resolved)
```

Duplicate auto-resolution in `_apply_resume_after_spec_patch`. Must also be updated for multi-file routing.

---

## 3. _build_steps() Code Paths

**File**: `src/superclaude/cli/roadmap/executor.py`, lines 1115-1306

### 3.1 Extract Step Routing (lines 1151-1176)

```python
Step(
    id="extract",
    prompt=(
        build_extract_prompt_tdd(...)
        if config.input_type == "tdd"
        else build_extract_prompt(...)
    ),
    gate=EXTRACT_TDD_GATE if config.input_type == "tdd" else EXTRACT_GATE,
    inputs=[config.spec_file] + ([config.tdd_file] if config.tdd_file else []) + ([config.prd_file] if config.prd_file else []),
)
```

The extract step's prompt builder and gate are selected based on `config.input_type`. The inputs list concatenates all available files.

### 3.2 Supplementary File Threading

`config.tdd_file` and `config.prd_file` are threaded through **every** downstream step:
- generate (lines 1181, 1191) — prompt builders and inputs
- score (line 1223) — prompt builder and inputs
- merge (line 1233) — prompt builder and inputs
- test-strategy (line 1253) — prompt builder and inputs
- spec-fidelity (line 1263) — prompt builder and inputs

Pattern: `tdd_file=config.tdd_file, prd_file=config.prd_file` is repeated in every prompt builder call. The inputs lists use `+ ([config.tdd_file] if config.tdd_file else [])` pattern.

**No changes needed to _build_steps() if routing sets config fields correctly before it's called.**

---

## 4. State Save/Restore Paths

### 4.1 _save_state() (lines 1650-1765)

```python
state = {
    "spec_file": str(config.spec_file),
    "tdd_file": str(config.tdd_file) if config.tdd_file else None,
    "prd_file": str(config.prd_file) if config.prd_file else None,
    "input_type": config.input_type,
    # ...
}
```
**Lines 1712-1715**: All three file slots and input_type are persisted.

### 4.2 _restore_from_state() (lines 1953-2058)

Restores:
1. **input_type** (lines 2017-2022): If saved value is not "auto" and current is "auto", restore saved value
2. **tdd_file** (lines 2024-2037): Auto-wire from state if CLI didn't provide `--tdd-file`; checks file existence
3. **prd_file** (lines 2039-2056): Auto-wire from state if CLI didn't provide `--prd-file`; checks file existence; explicit CLI overrides state with log

**No restoration of spec_file** — it's always provided as the positional argument.

For multi-file: If multiple positional files now fill the slots, the state file already has `tdd_file` and `prd_file`. Restoration logic just needs to handle the case where a positional file auto-detected as TDD might now be in the `tdd_file` slot from a previous run.

---

## 5. Inline Embedding Labels (roadmap_run_step)

**File**: `src/superclaude/cli/roadmap/executor.py`, lines 539-548

```python
labels = {}
if config.spec_file:
    labels[config.spec_file] = f"{config.spec_file} [Primary input - {config.input_type}]"
if config.tdd_file:
    labels[config.tdd_file] = f"{config.tdd_file} [TDD - supplementary technical context]"
if config.prd_file:
    labels[config.prd_file] = f"{config.prd_file} [PRD - supplementary business context]"
```

Labels are built from config fields. **No changes needed** if config fields are set correctly by the router.

---

## 6. Complete Reference Map

| Config Field | Used At (executor.py lines) | Purpose |
|---|---|---|
| `config.spec_file` | 490, 542-543, 628, 633, 671, 1158, 1165, 1174, 1247, 1263, 1267, 1274, 1358, 1708, 1712, 2109, 2114-2115, 2310, 2333, 2363, 2647 | Primary input, hash source, prompt builder primary arg |
| `config.input_type` | 543, 1163, 1172, 1715, 2020-2022, 2113-2116, 2139, 2362-2364 | Gate selection, prompt selection, state persistence |
| `config.tdd_file` | 544-545, 1160, 1167, 1174, 1181, 1185, 1191, 1195, 1223, 1227, 1233, 1237, 1253, 1257, 1263, 1267, 1713, 2025-2037, 2119-2120, 2126-2133, 2139-2144 | Supplementary TDD context |
| `config.prd_file` | 546-547, 1161, 1168, 1174, 1181, 1185, 1191, 1195, 1223, 1227, 1233, 1237, 1253, 1257, 1263, 1267, 1714, 2040-2056, 2121-2122, 2127-2128 | Supplementary PRD context |

---

## 7. Proposed _route_input_files() Design

### 7.1 Signature

```python
def _route_input_files(
    input_files: tuple[Path, ...],
    explicit_tdd: Path | None,
    explicit_prd: Path | None,
    explicit_input_type: str,  # "auto", "tdd", "spec"
) -> dict:
    """Route N positional files + explicit flags into pipeline slots.

    Returns:
        {
            "spec_file": Path,       # primary input (always set)
            "tdd_file": Path | None, # supplementary TDD
            "prd_file": Path | None, # supplementary PRD
            "input_type": str,       # resolved: "tdd" or "spec" (never "auto")
        }

    Raises:
        click.UsageError: on validation failures
    """
```

### 7.2 Algorithm

```
1. If len(input_files) == 0:
     raise UsageError("At least one input file required")

2. If len(input_files) > 3:
     raise UsageError("At most 3 input files (spec + tdd + prd)")

3. Classify each file:
     For each file in input_files:
       detected_type = detect_input_type(file)  # returns "tdd" or "spec"
       # NOTE: PRD detection needed — researcher-1's scope
       # For now, assume detect_input_type() returns "tdd", "spec", or "prd"

4. Apply explicit overrides:
     If explicit_input_type != "auto" and len(input_files) == 1:
       # Single file: honor the explicit type
       classifications[input_files[0]] = explicit_input_type

5. Validate no duplicates:
     Count by type: specs, tdds, prds
     If specs > 1: raise UsageError("Multiple files detected as spec")
     If tdds > 1: raise UsageError("Multiple files detected as TDD")
     If prds > 1: raise UsageError("Multiple files detected as PRD")

6. Validate primary input exists:
     If no spec and no tdd:
       raise UsageError("No primary input (spec or TDD) detected")
     If only prd(s) and nothing else:
       raise UsageError("PRD cannot be the sole primary input")

7. Assign slots:
     spec_file = first file classified as "spec", or first TDD if no spec
     tdd_file = file classified as "tdd" (if spec_file is the spec)
     prd_file = file classified as "prd"

8. Merge explicit flags:
     If explicit_tdd is not None:
       If tdd_file is already assigned from positional:
         raise UsageError("--tdd-file conflicts with positional TDD file")
       tdd_file = explicit_tdd
     If explicit_prd is not None:
       If prd_file is already assigned from positional:
         raise UsageError("--prd-file conflicts with positional PRD file")
       prd_file = explicit_prd

9. Determine input_type:
     If spec_file was classified as "tdd": input_type = "tdd"
     Else: input_type = "spec"
     # explicit_input_type overrides only for single-file case (step 4)

10. Apply redundancy guard:
      If input_type == "tdd" and tdd_file is not None:
        warn and null tdd_file

11. Apply same-file guard:
      Check all pairs: spec_file vs tdd_file, spec_file vs prd_file, tdd_file vs prd_file
      Raise on any match

12. Return dict
```

### 7.3 Primary Input Selection Priority

When multiple files are detected:
- **Spec always takes the `spec_file` slot** — it's the "primary" input
- **TDD goes to `tdd_file` when a spec is present** — supplementary
- **TDD goes to `spec_file` when no spec exists** — becomes primary, `input_type="tdd"`
- **PRD always goes to `prd_file`** — never primary

---

## 8. Edge Cases

### 8.1 Single PRD → Error
A lone PRD file has no spec or TDD to generate a roadmap from. The pipeline requires a spec or TDD as primary input.
**Action**: Raise `UsageError("PRD cannot be the sole primary input; provide a spec or TDD file")`

### 8.2 Two Files Both Detected as Spec → Error
Cannot determine which is primary vs supplementary.
**Action**: Raise `UsageError("Multiple files detected as spec type; use --input-type to disambiguate")`

### 8.3 Three Files: TDD + 2 Specs → Error
Same as 8.2 but with a valid TDD.
**Action**: Same error — two specs is always ambiguous.

### 8.4 Explicit --tdd-file + Positional TDD
User provides `superclaude roadmap run spec.md design.md --tdd-file other-tdd.md` where `design.md` auto-detects as TDD.
**Action**: Raise `UsageError("--tdd-file conflicts with positional file detected as TDD; remove one")`
**Rationale**: Explicit flag should not silently override positional detection (least-surprise principle).

### 8.5 Explicit --input-type tdd + Multiple Files
User says `--input-type tdd` with 2+ files. The `--input-type` flag was designed for single-file override.
**Action**: With multi-file, `--input-type` is ignored (log warning). Each file is classified independently. If user wants to force classification, they should use explicit `--tdd-file`/`--prd-file` flags.

### 8.6 Backward Compatibility: Single File
When `input_files` has exactly 1 element, behavior must match current code exactly:
- `spec_file = input_files[0]`
- `detect_input_type()` classifies it
- `--input-type` overrides classification
- `--tdd-file` and `--prd-file` work as before

---

## 9. Changes Required in execute_roadmap()

### 9.1 Replace Inline Routing with _route_input_files()

**Current code** (lines 2113-2144):
```python
# Auto-resolve
if config.input_type == "auto":
    resolved = detect_input_type(config.spec_file)
    config = dataclasses.replace(config, input_type=resolved)

# Logging
if config.tdd_file is not None: ...
if config.prd_file is not None: ...

# Same-file guard
if config.tdd_file is not None and config.prd_file is not None and ...: ...

# Redundancy guard
if config.input_type == "tdd" and config.tdd_file is not None: ...
```

**Proposed replacement**:
```python
# Route input files (auto-detect, validate, assign slots)
routing = _route_input_files(
    input_files=(config.spec_file,),  # future: tuple of positional args
    explicit_tdd=config.tdd_file,
    explicit_prd=config.prd_file,
    explicit_input_type=config.input_type,
)
config = dataclasses.replace(
    config,
    spec_file=routing["spec_file"],
    tdd_file=routing["tdd_file"],
    prd_file=routing["prd_file"],
    input_type=routing["input_type"],
)

# Log resolved routing
_log.info("Routing: spec=%s tdd=%s prd=%s type=%s",
          config.spec_file, config.tdd_file, config.prd_file, config.input_type)
```

This replaces lines 2113-2144 (auto-resolution, logging, same-file guard, redundancy guard) with a single function call.

### 9.2 Update _apply_resume_after_spec_patch()

The duplicate auto-resolution at line 2362 should also call `_route_input_files()`:
```python
# Current (line 2362-2364):
if config.input_type == "auto":
    resolved = detect_input_type(config.spec_file)
    config = dataclasses.replace(config, input_type=resolved)

# Replace with:
routing = _route_input_files(
    input_files=(config.spec_file,),
    explicit_tdd=config.tdd_file,
    explicit_prd=config.prd_file,
    explicit_input_type=config.input_type,
)
config = dataclasses.replace(config, **routing)
```

### 9.3 Update commands.py CLI Argument

**Not in my scope** (researcher-2 covers Click `nargs=-1`), but the interface must change from:
```python
@click.argument("spec_file", type=click.Path(exists=True, path_type=Path))
```
to something like:
```python
@click.argument("input_files", nargs=-1, type=click.Path(exists=True, path_type=Path))
```

The `config_kwargs` construction (lines 194-207) must be updated to call `_route_input_files()` and unpack the result into `spec_file`, `tdd_file`, `prd_file`, `input_type`.

---

## 10. Changes to _restore_from_state()

### 10.1 No Structural Changes Required

The current restore logic (lines 1953-2058) already handles `input_type`, `tdd_file`, and `prd_file` independently. When multi-file positional args are used, the state file will still contain these three fields with the same semantics.

### 10.2 One Semantic Consideration

On `--resume` with multi-file positional args, the user provides positional files again. The CLI layer would call `_route_input_files()` before `execute_roadmap()`, populating `config.tdd_file` and `config.prd_file` from positional args. Then `_restore_from_state()` would only auto-wire files that are `None` on config.

This means: if user provides positional files on resume, they override state. If user provides fewer files on resume, state fills in the gaps. This is the correct behavior (same as current `--tdd-file` / `--prd-file` override logic).

---

## 11. Changes to models.py input_type

### 11.1 Current Type

```python
input_type: Literal["auto", "tdd", "spec"] = "auto"
```

### 11.2 Recommendation

If PRD-as-primary is supported (unlikely based on pipeline design):
```python
input_type: Literal["auto", "tdd", "spec", "prd"] = "auto"
```

If PRD remains supplementary-only (recommended):
**No change needed.** The current `Literal["auto", "tdd", "spec"]` is sufficient. PRD files only fill the `prd_file` slot, never the `spec_file` slot, so `input_type` never needs to be `"prd"`.

---

## 12. Summary of Changes by File

| File | Change | Scope |
|---|---|---|
| `executor.py` | Add `_route_input_files()` function (~60 lines) | New function |
| `executor.py` | Replace lines 2113-2144 in `execute_roadmap()` with `_route_input_files()` call | 30 lines replaced with ~10 |
| `executor.py` | Replace lines 2362-2364 in `_apply_resume_after_spec_patch()` | 3 lines replaced with ~5 |
| `commands.py` | Change positional arg to `nargs=-1` (researcher-2 scope) | CLI layer |
| `commands.py` | Call `_route_input_files()` in config construction | ~15 lines |
| `models.py` | No change if PRD stays supplementary-only | None |
| `_build_steps()` | No change — already reads config fields | None |
| `_save_state()` | No change — already saves all three file slots | None |
| `_restore_from_state()` | No structural change needed | None |
| `roadmap_run_step()` labels | No change — reads config fields | None |
