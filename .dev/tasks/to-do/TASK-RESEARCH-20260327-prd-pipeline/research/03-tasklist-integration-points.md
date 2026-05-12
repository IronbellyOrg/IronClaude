# Research: Tasklist CLI Integration Points

**Investigation type:** Code Tracer
**Scope:** src/superclaude/cli/tasklist/commands.py, models.py, executor.py, prompts.py
**Status:** Complete
**Date:** 2026-03-27

---

## 1. commands.py -- CLI Flag Definition (Layer 1)

**File:** `src/superclaude/cli/tasklist/commands.py` (130 lines)
**Source:** Direct code read, 2026-03-27

### TDD Pattern Traced

The `--tdd-file` flag is defined at **lines 61-66** as a Click option on the `validate` command:

```python
@click.option(
    "--tdd-file",
    type=click.Path(exists=True, path_type=Path),
    default=None,
    help="Path to the TDD file used as an additional validation input.",
)
```

Key characteristics:
- **Type:** `click.Path(exists=True, path_type=Path)` -- Click validates the file exists at invocation time and converts to `pathlib.Path`
- **Default:** `None` (optional supplementary input)
- **Position in decorator stack:** Last `@click.option` before the function definition (line 67)

The `validate` function signature at **line 74** receives it as `tdd_file: Path | None`.

### Resolution Logic (lines 106-114)

The flag value is resolved and passed into `TasklistValidateConfig` at **line 114**:

```python
config = TasklistValidateConfig(
    ...
    tdd_file=tdd_file.resolve() if tdd_file is not None else None,
)
```

Pattern: conditional `.resolve()` to get absolute path, preserving `None` when not provided.

### PRD Equivalent

Add a `--prd-file` option immediately after `--tdd-file` (or before it, order is cosmetic):

```python
@click.option(
    "--prd-file",
    type=click.Path(exists=True, path_type=Path),
    default=None,
    help="Path to the PRD file used as an additional validation input.",
)
```

Add `prd_file: Path | None` to the `validate` function signature. Add resolution line:

```python
prd_file=prd_file.resolve() if prd_file is not None else None,
```

---

## 2. models.py -- Config Dataclass (Layer 2)

**File:** `src/superclaude/cli/tasklist/models.py` (26 lines)
**Source:** Direct code read, 2026-03-27

### TDD Pattern Traced

`TasklistValidateConfig` is a `@dataclass` extending `PipelineConfig` (from `..pipeline.models`). The TDD field is at **line 25**:

```python
@dataclass
class TasklistValidateConfig(PipelineConfig):
    output_dir: Path = field(default_factory=lambda: Path("."))
    roadmap_file: Path = field(default_factory=lambda: Path("."))
    tasklist_dir: Path = field(default_factory=lambda: Path("."))
    tdd_file: Path | None = None  # TDD integration: optional TDD file for enriched validation
```

Key characteristics:
- Simple `Path | None` type with `None` default
- No `field()` wrapper needed (unlike the Path fields which need `default_factory` to avoid mutable default)
- Comment documents intent

### PRD Equivalent

Add one line after `tdd_file`:

```python
prd_file: Path | None = None  # PRD integration: optional PRD file for enriched validation
```

---

## 3. executor.py -- Pipeline Step Builder (Layer 3)

**File:** `src/superclaude/cli/tasklist/executor.py` (~270 lines)
**Source:** Direct code read, 2026-03-27

### TDD Pattern Traced

The TDD wiring in the executor is in `_build_steps()` at **lines 188-211**.

**Step 1 -- Input list assembly (lines 190-194):**

```python
def _build_steps(config: TasklistValidateConfig) -> list[Step]:
    tasklist_files = _collect_tasklist_files(config.tasklist_dir)
    all_inputs = [config.roadmap_file] + tasklist_files
    # TDD integration: include TDD file in validation inputs when provided
    if config.tdd_file is not None:
        all_inputs.append(config.tdd_file)
```

The `all_inputs` list feeds into `Step.inputs`, which is later read by `_embed_inputs()` (line 112) to inline file contents into the prompt. This is the mechanism that makes the TDD file content available to the Claude subprocess.

**Step 2 -- Prompt builder call (lines 199-203):**

```python
Step(
    id="tasklist-fidelity",
    prompt=build_tasklist_fidelity_prompt(
        config.roadmap_file,
        config.tasklist_dir,
        tdd_file=config.tdd_file,
    ),
    ...
    inputs=all_inputs,
    ...
)
```

Two parallel paths:
1. `inputs=all_inputs` -- the file is embedded for the subprocess to read
2. `tdd_file=config.tdd_file` passed to prompt builder -- controls whether supplementary validation instructions are included in the prompt text

Both are required. Without (1), the subprocess has no file content. Without (2), the prompt doesn't instruct Claude to check TDD-specific concerns.

### PRD Equivalent

**Input list addition** (after the TDD block):

```python
if config.prd_file is not None:
    all_inputs.append(config.prd_file)
```

**Prompt builder call** -- add `prd_file` kwarg:

```python
prompt=build_tasklist_fidelity_prompt(
    config.roadmap_file,
    config.tasklist_dir,
    tdd_file=config.tdd_file,
    prd_file=config.prd_file,
),
```

### Both-Files Behavior

When both `--tdd-file` and `--prd-file` are provided:
- `all_inputs` contains: `[roadmap_file, *tasklist_files, tdd_file, prd_file]`
- Both files are embedded via `_embed_inputs()` as fenced code blocks
- The prompt builder activates both supplementary validation blocks (TDD and PRD sections are independent conditionals)
- No conflict: each block adds distinct MEDIUM-severity checks from different domains

---

## 4. prompts.py -- Prompt Builder (Layer 4)

**File:** `src/superclaude/cli/tasklist/prompts.py` (126 lines)
**Source:** Direct code read, 2026-03-27

### TDD Pattern Traced

**Function signature (lines 17-21):**

```python
def build_tasklist_fidelity_prompt(
    roadmap_file: Path,
    tasklist_dir: Path,
    tdd_file: Path | None = None,
) -> str:
```

**Conditional block (lines 110-123):**

```python
# TDD integration: append supplementary validation when TDD file is provided
if tdd_file is not None:
    base += (
        "\n\n## Supplementary TDD Validation (when TDD file is provided)\n\n"
        "A Technical Design Document (TDD) is included in the inputs alongside "
        "the roadmap and tasklist. Additionally check:\n"
        "1. Test cases from the TDD's Testing Strategy section ({S}15) should have "
        "corresponding validation or test tasks in the tasklist.\n"
        "2. Rollback procedures from the TDD's Migration & Rollout Plan section ({S}19) "
        "should have corresponding contingency or rollback tasks.\n"
        "3. Components listed in the TDD's Component Inventory ({S}10) should have "
        "corresponding implementation tasks.\n"
        "Flag missing coverage as MEDIUM severity deviations."
    )
```

Note: `{S}` above represents the section symbol in the actual code.

Key characteristics:
- Appended to `base` string before `_OUTPUT_FORMAT_BLOCK` (line 125: `return base + _OUTPUT_FORMAT_BLOCK`)
- Three numbered checks, each mapping a TDD section to expected tasklist coverage
- All flagged as MEDIUM severity (not HIGH)
- Block is self-contained -- does not modify existing comparison dimensions

**Return statement (line 125):**

```python
return base + _OUTPUT_FORMAT_BLOCK
```

The `_OUTPUT_FORMAT_BLOCK` (imported from `superclaude.cli.roadmap.prompts`) is always appended last. Supplementary blocks go between the base prompt and the output format block.

### PRD Equivalent

**Function signature change:**

```python
def build_tasklist_fidelity_prompt(
    roadmap_file: Path,
    tasklist_dir: Path,
    tdd_file: Path | None = None,
    prd_file: Path | None = None,
) -> str:
```

**Conditional PRD block** (after the TDD block, before `return`):

```python
if prd_file is not None:
    base += (
        "\n\n## Supplementary PRD Validation (when PRD file is provided)\n\n"
        "A Product Requirements Document (PRD) is included in the inputs alongside "
        "the roadmap and tasklist. Additionally check:\n"
        "1. **Persona Flow Coverage**: User personas and their primary flows "
        "defined in the PRD should have corresponding tasks ensuring each "
        "persona's journey is implemented end-to-end.\n"
        "2. **KPI Instrumentation**: Success metrics and KPIs defined in the PRD "
        "should have corresponding instrumentation, tracking, or analytics tasks "
        "in the tasklist.\n"
        "3. **Stakeholder & Compliance Tasks**: Regulatory requirements, compliance "
        "checks, and stakeholder sign-off gates from the PRD should have "
        "corresponding tasks.\n"
        "4. **UX Flow Alignment**: User experience flows, wireframe references, "
        "and interaction patterns from the PRD should be reflected in "
        "implementation and validation tasks.\n"
        "Flag missing coverage as MEDIUM severity deviations."
    )
```

Rationale for each check:
- **Persona Flow Coverage** -- PRDs define user personas and their workflows; the tasklist must cover them
- **KPI Instrumentation** -- PRDs define measurable success criteria; tasks must include measurement implementation
- **Stakeholder & Compliance** -- PRDs often include regulatory/legal requirements that need explicit tasks
- **UX Flow Alignment** -- PRDs reference wireframes and UX flows; these must map to implementation tasks

---

## 5. End-to-End Wiring Summary

```
CLI flag (commands.py)
  |
  v  click.Path(exists=True) -> Path | None
Config field (models.py)
  |
  v  TasklistValidateConfig.prd_file: Path | None
Executor (executor.py)
  |
  +--> all_inputs.append(config.prd_file)     # file content embedding
  |
  +--> build_tasklist_fidelity_prompt(         # prompt instruction injection
  |        prd_file=config.prd_file)
  v
Prompt builder (prompts.py)
  |
  v  if prd_file is not None: base += "## Supplementary PRD Validation ..."
Claude subprocess receives:
  - Embedded file content (from all_inputs)
  - Prompt instructions (from conditional block)
```

**Total changes required: 4 files, ~25 lines of code.**

---

## 6. Gaps and Questions

1. **Ordering in `all_inputs`**: TDD is appended after tasklist files. PRD should also be appended after (order: roadmap, tasklists, tdd, prd). The order matters for `_embed_inputs()` which produces fenced blocks in list order -- the prompt references "included in the inputs" but does not specify order, so this is cosmetic.

2. **Prompt size concern**: With both TDD and PRD files embedded, the composed prompt could exceed `_EMBED_SIZE_LIMIT` (100KB). The executor logs a warning but proceeds anyway (line 116-120). No functional issue, but worth noting for very large documents.

3. **No existing PRD validation checks in roadmap pipeline**: The roadmap pipeline (`src/superclaude/cli/roadmap/`) has `build_extract_prompt_tdd` but no PRD equivalent. The tasklist integration is independent, but the roadmap pipeline may also need PRD extraction if PRD-to-roadmap fidelity checking is desired.

4. **Test coverage**: `tests/roadmap/test_spec_fidelity.py` exists for roadmap validation. A corresponding `tests/tasklist/test_tasklist_fidelity.py` or extension of existing tests should verify that `--prd-file` activates the supplementary block.

5. **PRD section numbering**: The TDD block references specific sections (15, 19, 10). The PRD block above uses domain concepts instead of section numbers because PRD templates vary more. If the project has a canonical PRD template with fixed section numbers, those should be referenced explicitly.

---

## 7. Stale Documentation Found

- **None identified.** All findings are from direct code reads performed 2026-03-27. The code comments and docstrings accurately describe current behavior. The task description's line-number references (lines 62-66, 25, 193-194, 111-123) are accurate to the current codebase state.

---

## 8. Summary

The `--tdd-file` integration follows a clean 4-layer pattern: CLI flag -> config dataclass field -> executor input list + prompt builder kwarg -> conditional prompt block. Adding `--prd-file` replicates this pattern exactly with PRD-specific supplementary validation checks (persona flow coverage, KPI instrumentation, stakeholder/compliance tasks, UX flow alignment). Both flags can be active simultaneously without conflict -- they append independent input files and independent prompt sections. Total implementation: ~25 lines across 4 files.
