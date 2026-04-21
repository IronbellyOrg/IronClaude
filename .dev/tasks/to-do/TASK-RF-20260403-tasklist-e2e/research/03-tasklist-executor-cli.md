# R03 -- Tasklist Executor & CLI

| Field      | Value |
|------------|-------|
| Researcher | r03   |
| Scope      | `src/superclaude/cli/tasklist/executor.py`, `commands.py`, `models.py`, `gates.py` |
| Status     | Complete |
| Created    | 2026-04-02 |

---

## 1. `tasklist validate` CLI Command

**Source**: `src/superclaude/cli/tasklist/commands.py`

### Command Signature

```
superclaude tasklist validate OUTPUT_DIR [OPTIONS]
```

### Positional Argument

| Argument     | Type         | Description |
|--------------|--------------|-------------|
| `OUTPUT_DIR` | `click.Path` (converted to `Path`) | Directory where the validation report will be written. Created if it does not exist (`mkdir(parents=True, exist_ok=True)`). |

### Flags / Options

| Flag              | Type      | Default              | Description |
|-------------------|-----------|----------------------|-------------|
| `--roadmap-file`  | Path (must exist) | `{OUTPUT_DIR}/roadmap.md` | Path to the roadmap file. |
| `--tasklist-dir`  | Path (must exist) | `{OUTPUT_DIR}/`           | Path to the directory containing tasklist `.md` files. |
| `--model`         | str       | `""` (empty string)  | Override model for validation steps. |
| `--max-turns`     | int       | `100`                | Max agent turns per Claude subprocess. |
| `--debug`         | flag      | `False`              | Enable debug logging. |
| `--tdd-file`      | Path (must exist) | `None`  | Path to TDD file as additional validation input. |
| `--prd-file`      | Path (must exist) | `None`  | Path to PRD file as additional validation input. |

### Help Text (group-level)

> Tasklist validation commands. Validate generated tasklists against their upstream roadmap. Catches fabricated traceability IDs, missing deliverables, and dependency chain errors.

### Help Text (validate subcommand)

> Validate tasklist fidelity against a roadmap. OUTPUT_DIR is the directory where the validation report will be written. Checks deliverable coverage, signature preservation, traceability ID validity, and dependency chain correctness. Exits with code 1 if HIGH-severity deviations are found.

### Exit Behavior

- **Exit 0**: No HIGH-severity deviations found (prints green "PASS" message).
- **Exit 1**: HIGH-severity deviations found, or pipeline step failed/timed out, or no report generated (prints red "FAIL" message).

---

## 2. Auto-Wire Logic (TDD/PRD from `.roadmap-state.json`)

**Source**: `commands.py` lines 113-159

When `--tdd-file` or `--prd-file` are **not** explicitly passed, the command reads `.roadmap-state.json` from the resolved output directory and attempts to restore them.

### State File Read

```python
from ..roadmap.executor import read_state
state = read_state(resolved_output / ".roadmap-state.json") or {}
```

`read_state()` (from `roadmap/executor.py`) returns `None` for missing, empty, or malformed JSON files. The `or {}` fallback ensures a dict is always available.

### TDD Auto-Wire (two paths)

**Path A -- Explicit `tdd_file` in state**:
1. Reads `state["tdd_file"]`.
2. If the path exists as a file, auto-wires it and logs to stderr.
3. If the path does NOT exist, logs a WARNING and skips.

**Path B -- `input_type == "tdd"` fallback**:
When the primary input to the roadmap was itself a TDD (i.e., `state["input_type"] == "tdd"`), the `tdd_file` key in state is `None` (because `--tdd-file` is the *supplementary* flag, not the primary). In this case:
1. Falls back to `state["spec_file"]` which IS the TDD.
2. If that path exists as a file, auto-wires it.

This handles the case where the user ran `superclaude roadmap run my-tdd.md` (single TDD input with no separate spec).

### PRD Auto-Wire

1. Reads `state["prd_file"]`.
2. If the path exists as a file, auto-wires it and logs to stderr.
3. If the path does NOT exist, logs a WARNING and skips.
4. There is NO `input_type == "prd"` fallback analogous to the TDD path.

### State File Schema (relevant keys)

The `.roadmap-state.json` is written by `_write_state()` in `roadmap/executor.py` and contains:

```json
{
  "schema_version": 1,
  "spec_file": "/absolute/path/to/spec.md",
  "tdd_file": "/absolute/path/to/tdd.md",     // null if not provided
  "prd_file": "/absolute/path/to/prd.md",     // null if not provided
  "input_type": "spec" | "tdd" | "prd",
  "spec_hash": "...",
  "agents": [...]
}
```

---

## 3. Validation Executor (`executor.py`)

### Pipeline Step Construction (`_build_steps`)

1. **Collects tasklist files**: `_collect_tasklist_files(config.tasklist_dir)` -- globs `*.md` in the tasklist directory, sorted for deterministic ordering. Raises `FileNotFoundError` if directory is missing or contains zero `.md` files.

2. **Assembles input list**: `[roadmap_file] + tasklist_files + [tdd_file?] + [prd_file?]`

3. **Builds exactly one Step**:
   - **id**: `"tasklist-fidelity"`
   - **prompt**: Built by `build_tasklist_fidelity_prompt(roadmap_file, tasklist_dir, tdd_file=..., prd_file=...)`
   - **output_file**: `{output_dir}/tasklist-fidelity.md`
   - **gate**: `TASKLIST_FIDELITY_GATE` (from `gates.py`)
   - **timeout**: 600 seconds (10 minutes)
   - **inputs**: The assembled input list (all files that get inline-embedded)
   - **retry_limit**: 1
   - **model**: from config (can be overridden)

### Step Execution (`tasklist_run_step`)

1. **Dry-run support**: If `config.dry_run`, returns PASS immediately without running anything.

2. **Inline embedding**: All input files are read and concatenated as fenced code blocks (`_embed_inputs`). The `--file` flag is explicitly NOT used (documented as a cloud download mechanism, not a local file injector). A warning is logged if the composed prompt exceeds 100KB.

3. **Claude subprocess**: Uses `ClaudeProcess` with:
   - `output_format="text"`
   - `permission_flag` from config
   - Any model override
   - The composed prompt (step prompt + embedded inputs)

4. **Cancellation**: Polls the subprocess in a 1-second loop, checking `cancel_check()` callback.

5. **Exit code handling**:
   - `124` = TIMEOUT
   - non-zero = FAIL
   - `0` = success (proceeds to sanitize)

6. **Output sanitization**: `_sanitize_output` strips any conversational preamble before the YAML frontmatter `---` delimiter. Uses atomic tmp + `os.replace`.

### Pipeline Orchestration (`execute_tasklist_validate`)

1. Builds steps via `_build_steps(config)`.
2. Delegates to `execute_pipeline(steps, config, run_step=tasklist_run_step)` from the shared pipeline module.
3. Checks for pipeline failures (FAIL or TIMEOUT status).
4. Parses `tasklist-fidelity.md` frontmatter for `high_severity_count` via `_has_high_severity()`.
5. Returns `True` (pass) or `False` (fail).

---

## 4. Fidelity Report Output

### Location

The report is always written to:
```
{OUTPUT_DIR}/tasklist-fidelity.md
```

Each run **overwrites** the previous report (the `ClaudeProcess` writes to `step.output_file` directly).

### Gate Criteria (`TASKLIST_FIDELITY_GATE`)

**Source**: `src/superclaude/cli/tasklist/gates.py`

Required frontmatter fields:
- `high_severity_count`
- `medium_severity_count`
- `low_severity_count`
- `total_deviations`
- `validation_complete`
- `tasklist_ready`

Minimum report length: 20 lines.

Enforcement tier: `STRICT`.

Semantic checks (reused from `roadmap/gates.py`):
1. **`_high_severity_count_zero`**: `high_severity_count` must be `0`.
2. **`_tasklist_ready_consistent`**: `tasklist_ready` must be consistent with severity counts and `validation_complete`.

### CLI Report Check

After `execute_tasklist_validate` returns, the CLI checks `report_path.exists()`:
- If report exists: prints path.
- If report missing: prints warning to stderr.
- If `_has_high_severity` is True (or report missing/malformed): exits with code 1.

### `_has_high_severity` Logic

Parses the report file manually (no YAML library dependency):
1. Checks for `---` frontmatter delimiter.
2. Scans for `high_severity_count:` line.
3. Returns `True` if value > 0, or if the field/frontmatter is missing/malformed.
4. Default assumption is failure (any parse error = HIGH severity assumed).

---

## 5. Running Validation: Explicit Flags vs Auto-Wire

### Fully Explicit (no state file needed)

```bash
superclaude tasklist validate ./output \
  --roadmap-file ./specs/roadmap.md \
  --tasklist-dir ./output/tasklists/ \
  --tdd-file ./specs/tdd.md \
  --prd-file ./specs/prd.md \
  --model claude-sonnet-4-20250514 \
  --max-turns 50
```

### Auto-Wire (relies on prior `roadmap run` having written state)

```bash
# If roadmap run was executed with: superclaude roadmap run tdd.md prd.md -o ./output
# Then .roadmap-state.json exists in ./output/ with tdd_file and prd_file populated
superclaude tasklist validate ./output
```

This auto-resolves:
- `--roadmap-file` defaults to `./output/roadmap.md`
- `--tasklist-dir` defaults to `./output/`
- `--tdd-file` auto-wired from state
- `--prd-file` auto-wired from state

### Partial Override

```bash
# Auto-wire TDD from state, but override PRD explicitly
superclaude tasklist validate ./output --prd-file ./updated-prd.md
```

Explicit flags always take precedence over auto-wire. The auto-wire only activates when the flag is `None`.

---

## 6. Edge Cases

### Missing Tasklist Directory

`_collect_tasklist_files()` raises `FileNotFoundError` if the directory does not exist. This bubbles up as an unhandled exception (the CLI does not catch it explicitly -- it will print a traceback).

### Empty Tasklist Directory (no .md files)

Same `FileNotFoundError` raised with message: "No markdown files found in tasklist directory: {path}".

### Missing Roadmap File

The `--roadmap-file` flag requires `exists=True` when explicitly passed, so Click validates it. When defaulted to `{OUTPUT_DIR}/roadmap.md`, the file might not exist -- this is NOT validated at the CLI level. It would fail during `_embed_inputs()` when `Path.read_text()` raises `FileNotFoundError`.

### Missing .roadmap-state.json

`read_state()` returns `None`, which is coerced to `{}`. All auto-wire paths are silently skipped. No error, no warning.

### State File References Non-Existent TDD/PRD

A WARNING is printed to stderr (e.g., "State file references --tdd-file X but file not found; skipping.") and the field remains `None`.

### Report Not Generated (subprocess failure)

The CLI prints "No report generated" to stderr and exits with code 1 (since `_has_high_severity` returns `True` for a missing report).

### Oversized Prompt (>100KB)

A warning is logged but embedding proceeds anyway. The `--file` fallback was intentionally removed because `--file` is a cloud download mechanism, not a local file injector.

### Preamble in Output

If the Claude subprocess produces conversational text before the YAML frontmatter, `_sanitize_output()` strips everything before the first `---` line. This prevents gate check failures due to non-YAML preamble.

---

## 7. Data Model

### `TasklistValidateConfig`

**Source**: `src/superclaude/cli/tasklist/models.py`

Extends `PipelineConfig` with:

| Field          | Type           | Default    |
|----------------|----------------|------------|
| `output_dir`   | `Path`         | `Path(".")` |
| `roadmap_file` | `Path`         | `Path(".")` |
| `tasklist_dir` | `Path`         | `Path(".")` |
| `tdd_file`     | `Path \| None` | `None`     |
| `prd_file`     | `Path \| None` | `None`     |

Inherits from `PipelineConfig`: `work_dir`, `max_turns`, `model`, `debug`, `dry_run`, `permission_flag`, etc.

---

## 8. Key Takeaways for Task Builder

1. **Single-step pipeline**: Validation is exactly one step (`tasklist-fidelity`). The prompt builder (`build_tasklist_fidelity_prompt`) is the sole interface for controlling what the Claude subprocess validates.

2. **TDD/PRD enrichment is additive**: The files are appended to the input list and embedded inline. The prompt builder receives them as keyword arguments and must integrate them into instructions.

3. **Auto-wire is transparent**: Users who ran `roadmap run` with TDD/PRD inputs get automatic enrichment on `tasklist validate` with zero additional flags. The `input_type=tdd` fallback ensures even single-TDD-input roadmap runs auto-wire correctly.

4. **Gate is strict**: The `TASKLIST_FIDELITY_GATE` requires specific frontmatter fields and enforces `high_severity_count == 0` for pass. The report format is tightly specified.

5. **No retry logic in executor**: `retry_limit=1` means only one attempt. If the subprocess fails, it fails. Retries would need to come from the shared `execute_pipeline` infrastructure.

6. **Output is deterministic**: Report always at `{OUTPUT_DIR}/tasklist-fidelity.md`, overwritten each run.
