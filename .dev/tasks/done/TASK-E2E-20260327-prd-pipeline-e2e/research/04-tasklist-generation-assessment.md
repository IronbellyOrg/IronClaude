# Research Report: Data Flow Tracer — Tasklist Generation Assessment

| Field | Value |
|-------|-------|
| Researcher | researcher-04 |
| Date | 2026-03-27 |
| Status | Complete |
| Scope | `src/superclaude/cli/tasklist/` (all files), `src/superclaude/cli/roadmap/executor.py` (state file handling) |

---

## 1. Tasklist CLI Commands (`commands.py`)

### 1.1 Command Group Structure

**File:** `src/superclaude/cli/tasklist/commands.py`

The tasklist CLI defines a single Click group with **one** subcommand:

```python
@click.group("tasklist")
def tasklist_group():
    """Tasklist validation commands."""
    pass

@tasklist_group.command()
def validate(...):
    """Validate tasklist fidelity against a roadmap."""
```

### 1.2 CRITICAL FINDING: `superclaude tasklist generate` Does NOT Exist

**Answer: NO** -- there is no `generate` command in the tasklist CLI. The only subcommand is `validate`.

The `tasklist_group` Click group (line 15) has exactly one registered command: `validate` (line 31). There is no `generate`, `create`, `build`, or any other command. The group docstring says "Tasklist validation commands" -- not generation.

**Implication for E2E tests:** Tasklist *generation* is inference-only via the `/sc:tasklist` skill (see Section 6 below). Only tasklist *validation* (`superclaude tasklist validate`) is a CLI pipeline that can be tested with subprocess invocations.

### 1.3 `validate` Command Click Options

All options on the `validate` command (lines 31-81):

| Option | Type | Default | Help | Line |
|--------|------|---------|------|------|
| `output_dir` (argument) | `click.Path(path_type=Path)` | (required) | Positional arg for output dir | 32 |
| `--roadmap-file` | `click.Path(exists=True, path_type=Path)` | `None` | Path to roadmap file. Default: `{output_dir}/roadmap.md` | 33-38 |
| `--tasklist-dir` | `click.Path(exists=True, path_type=Path)` | `None` | Path to tasklist directory. Default: `{output_dir}/` | 39-44 |
| `--model` | `str` | `""` | Override model for validation steps | 46-49 |
| `--max-turns` | `int` | `100` | Max agent turns per claude subprocess | 50-55 |
| `--debug` | flag | `False` | Enable debug logging | 56-60 |
| `--tdd-file` | `click.Path(exists=True, path_type=Path)` | `None` | Path to TDD file for additional validation input | 61-66 |
| `--prd-file` | `click.Path(exists=True, path_type=Path)` | `None` | Path to PRD file for additional validation input | 67-72 |

**Key:** Both `--tdd-file` and `--prd-file` are already wired as CLI flags. They use `exists=True`, meaning Click validates file existence at invocation time.

### 1.4 `validate` Function Signature

```python
def validate(
    output_dir: Path,
    roadmap_file: Path | None,
    tasklist_dir: Path | None,
    model: str,
    max_turns: int,
    debug: bool,
    tdd_file: Path | None,
    prd_file: Path | None,
) -> None:
```

Both `tdd_file` and `prd_file` are resolved and passed to `TasklistValidateConfig` (lines 113-123).

---

## 2. Tasklist Executor (`executor.py`)

### 2.1 `_build_steps()` Function (lines 188-214)

This function assembles the single validation step:

```python
def _build_steps(config: TasklistValidateConfig) -> list[Step]:
    tasklist_files = _collect_tasklist_files(config.tasklist_dir)
    all_inputs = [config.roadmap_file] + tasklist_files
    # TDD integration: include TDD file in validation inputs when provided
    if config.tdd_file is not None:
        all_inputs.append(config.tdd_file)
    # PRD integration: include PRD file in validation inputs when provided
    if config.prd_file is not None:
        all_inputs.append(config.prd_file)

    return [
        Step(
            id="tasklist-fidelity",
            prompt=build_tasklist_fidelity_prompt(
                config.roadmap_file,
                config.tasklist_dir,
                tdd_file=config.tdd_file,
                prd_file=config.prd_file,
            ),
            ...
        ),
    ]
```

**Input assembly order:** roadmap -> tasklist files -> tdd_file -> prd_file

### 2.2 TDD Wiring (lines 192-194)

TDD is wired at two levels:
1. **Inputs list** (line 193-194): `config.tdd_file` is appended to `all_inputs` for `_embed_inputs()` -- the file content is available to the subprocess.
2. **Prompt builder** (line 205): `tdd_file=config.tdd_file` is passed to `build_tasklist_fidelity_prompt()`.

### 2.3 PRD Wiring -- FULLY IMPLEMENTED

> **QA CORRECTION (2026-03-27):** Original research incorrectly stated `prd_file` was not passed to the prompt builder. QA verified this is false -- see executor.py line 206 and prompts.py lines 21, 126-139.

**Currently implemented (as of this branch):**
- `config.prd_file` IS appended to `all_inputs` (lines 196-197) -- file content is embedded.
- `prd_file=config.prd_file` IS passed to `build_tasklist_fidelity_prompt()` (line 206).
- The prompt builder accepts `prd_file: Path | None = None` (line 21) and appends a conditional "Supplementary PRD Validation" block (lines 126-139) with 3 checks: persona coverage (S7), success metrics (S19), and acceptance scenarios (S12/S22), all flagged as MEDIUM severity.

**STATUS:** PRD wiring through the tasklist fidelity validation is complete end-to-end: CLI flag -> config -> executor inputs + prompt builder kwarg -> conditional PRD prompt block.

### 2.4 Auto-Wire Logic -- DOES NOT EXIST YET

There is no auto-wire logic anywhere in the current tasklist executor. The planned Phase 6 (from the PRD pipeline implementation plan) will add:
- Reading `.roadmap-state.json` from the roadmap output directory
- Auto-detecting `tdd_file` and `prd_file` from the state
- File existence verification
- Explicit flag precedence (CLI flags override auto-wire)
- Info message: `click.echo(f"[tasklist] Auto-wired {field} from roadmap state: {path}", err=True)`

### 2.5 Other Executor Functions

| Function | Lines | Purpose |
|----------|-------|---------|
| `_collect_tasklist_files()` | 37-49 | Glob `*.md` from tasklist dir, sorted, returns list |
| `_embed_inputs()` | 52-60 | Reads file paths into fenced code blocks for inline embedding |
| `_sanitize_output()` | 63-86 | Strips conversational preamble before YAML frontmatter |
| `tasklist_run_step()` | 89-185 | Executes a single step as a Claude subprocess (mirrors roadmap validate pattern) |
| `_has_high_severity()` | 217-244 | Parses report YAML frontmatter for `high_severity_count > 0` |
| `execute_tasklist_validate()` | 247-272 | Top-level orchestrator; returns bool (pass/fail) |

---

## 3. Tasklist Prompts (`prompts.py`)

### 3.1 Single Prompt Builder

**File:** `src/superclaude/cli/tasklist/prompts.py`

There is exactly ONE prompt builder function:

```python
def build_tasklist_fidelity_prompt(
    roadmap_file: Path,
    tasklist_dir: Path,
    tdd_file: Path | None = None,
    prd_file: Path | None = None,
) -> str:
```

**There is NO `build_tasklist_generate_prompt`** function. This confirms that tasklist generation is not a CLI pipeline operation.

### 3.2 TDD Block (lines 111-124)

When `tdd_file is not None`, the prompt appends a "Supplementary TDD Validation" section with 3 checks:
1. Test cases from TDD Testing Strategy (section 15) -> validation/test tasks
2. Rollback procedures from TDD Migration & Rollout Plan (section 19) -> contingency tasks
3. Components from TDD Component Inventory (section 10) -> implementation tasks

All missing coverage flagged as MEDIUM severity.

### 3.3 PRD Block -- FULLY IMPLEMENTED (lines 126-139)

> **QA CORRECTION (2026-03-27):** Original research incorrectly stated no PRD block exists. QA verified this is false -- the `prd_file` parameter and conditional PRD validation block are present in the current code.

The prompt builder accepts `prd_file: Path | None = None` (line 21). When `prd_file is not None`, it appends a "Supplementary PRD Validation" section (lines 126-139) with 3 checks:
1. User persona coverage from PRD User Personas section (S7) -- user-facing tasks should reference which persona is served
2. Success metrics from PRD Success Metrics section (S19) -- should have corresponding instrumentation/measurement tasks
3. Acceptance scenarios from PRD Scope Definition (S12) and Customer Journey Map (S22) -- should have corresponding verification tasks

All missing coverage flagged as MEDIUM severity.

### 3.4 Prompt Structure

The prompt follows the `base = (...); return base + _OUTPUT_FORMAT_BLOCK` pattern. It includes:
- Role definition ("You are a tasklist fidelity analyst")
- Validation layering guard (roadmap -> tasklist ONLY, NOT spec -> tasklist)
- Severity definitions (HIGH/MEDIUM/LOW with concrete examples)
- 5 comparison dimensions
- Output requirements (YAML frontmatter + deviation report format)

---

## 4. Tasklist Models (`models.py`)

### 4.1 `TasklistValidateConfig` (lines 15-26)

```python
@dataclass
class TasklistValidateConfig(PipelineConfig):
    output_dir: Path = field(default_factory=lambda: Path("."))
    roadmap_file: Path = field(default_factory=lambda: Path("."))
    tasklist_dir: Path = field(default_factory=lambda: Path("."))
    tdd_file: Path | None = None
    prd_file: Path | None = None
```

Both `tdd_file` and `prd_file` fields are already present. No changes needed for the model layer.

---

## 5. Roadmap State File (`.roadmap-state.json`)

### 5.1 `_save_state()` (executor.py lines 1361-1473)

The state dict is composed at lines 1421-1438:

```python
state = {
    "schema_version": 1,
    "spec_file": str(config.spec_file),
    "spec_hash": spec_hash,
    "agents": [{"model": a.model, "persona": a.persona} for a in config.agents],
    "depth": config.depth,
    "last_run": datetime.now(timezone.utc).isoformat(),
    "steps": { ... per-step results ... },
}
```

Plus preserved keys from existing state: `validation`, `fidelity_status`, `remediate`, `certify`.

### 5.2 CRITICAL FINDING: `tdd_file` and `prd_file` Are NOT in State

Neither `tdd_file` nor `prd_file` are currently written to `.roadmap-state.json`. The state file only stores: `schema_version`, `spec_file`, `spec_hash`, `agents`, `depth`, `last_run`, `steps`, and optional `validation`/`fidelity_status`/`remediate`/`certify`.

**The planned Phase 6 (step 6.1.1)** will add:
```python
"tdd_file": str(config.tdd_file) if config.tdd_file else None,
"prd_file": str(config.prd_file) if config.prd_file else None,
```

### 5.3 `read_state()` (executor.py lines 1633-1643)

```python
def read_state(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        text = path.read_text(encoding="utf-8")
        if not text.strip():
            return None
        return json.loads(text)
    except (json.JSONDecodeError, OSError):
        return None
```

Simple JSON reader with graceful failure. Returns `None` for missing, empty, or malformed files.

### 5.4 `write_state()` (executor.py lines 1623-1630)

Atomic write via tmp file + `os.replace()`.

---

## 6. Key Determinations for E2E Test Design

### 6.1 Does `superclaude tasklist generate` exist?

**NO.** Tasklist generation is inference-only via the `/sc:tasklist` skill (the sc-tasklist-protocol skill). The CLI pipeline only provides `superclaude tasklist validate`.

**Consequence:** E2E tests for "tasklist generation enrichment with TDD/PRD content" cannot test a CLI command. They would need to either:
- (a) Test the `/sc:tasklist` skill invocation (not a subprocess test)
- (b) Test `superclaude tasklist validate` with TDD/PRD enrichment (this IS testable as a CLI pipeline)

### 6.2 What Does the Auto-Wire Info Message Look Like?

**Not yet implemented.** The planned message (from Phase 6, step 6.2.4):
```
[tasklist] Auto-wired {field} from roadmap state: {path}
```
Written to stderr via `click.echo(..., err=True)`.

### 6.3 What Does the Redundancy Guard Warning Look Like?

**Not yet implemented.** The planned message (from Phase 5, step 5.6):
```
Ignoring --tdd-file: primary input is already a TDD document.
```
This is for the roadmap pipeline, not the tasklist pipeline. It fires when `config.input_type == "tdd" and config.tdd_file is not None`.

### 6.4 What Can Be Tested Today vs. After Implementation?

| Test Scenario | Testable Today? | Implementation Needed |
|--------------|----------------|----------------------|
| `tasklist validate` with `--tdd-file` | YES | None -- fully wired |
| `tasklist validate` with `--prd-file` (file embedding + prompt enrichment) | YES | Fully wired: file embedded in inputs AND prompt builder receives `prd_file` kwarg with conditional PRD validation block (3 checks: S7, S19, S12/S22) |
| Auto-wire from `.roadmap-state.json` | NO | Phase 6: save tdd/prd to state, add auto-wire logic to tasklist executor |
| Redundancy guard (input-type=tdd + --tdd-file) | NO | Phase 5, step 5.6 |
| CLI flag existence (`--prd-file` on validate) | YES | Already implemented |

---

## 7. Data Flow Diagrams

### 7.1 Current TDD Flow Through Tasklist Validate

```
CLI (--tdd-file) -> commands.py validate() -> TasklistValidateConfig.tdd_file
    -> executor.py _build_steps():
        1. Appends to all_inputs (file content embedded via _embed_inputs())
        2. Passes to build_tasklist_fidelity_prompt(tdd_file=...)
    -> prompts.py build_tasklist_fidelity_prompt():
        - Appends "Supplementary TDD Validation" block to prompt
    -> tasklist_run_step():
        - Composes prompt + embedded file contents
        - Launches Claude subprocess
```

### 7.2 Current PRD Flow Through Tasklist Validate (COMPLETE)

> **QA CORRECTION (2026-03-27):** Original research incorrectly showed this flow as incomplete. PRD wiring is fully implemented end-to-end.

```
CLI (--prd-file) -> commands.py validate() -> TasklistValidateConfig.prd_file
    -> executor.py _build_steps():
        1. Appends to all_inputs (file content embedded via _embed_inputs()) ✓
        2. Passes to build_tasklist_fidelity_prompt(prd_file=config.prd_file) ✓
    -> prompts.py build_tasklist_fidelity_prompt(prd_file=...):
        - Appends "Supplementary PRD Validation" block to prompt (3 checks: S7, S19, S12/S22) ✓
    -> tasklist_run_step():
        - Composes prompt + embedded file contents
        - Launches Claude subprocess
```

### 7.3 Planned Auto-Wire Flow (Phase 6, NOT implemented)

```
roadmap run --tdd-file T --prd-file P -> _save_state() writes to .roadmap-state.json:
    {"tdd_file": "/abs/path/T", "prd_file": "/abs/path/P", ...}

tasklist validate <output_dir> (no --tdd-file/--prd-file):
    -> executor reads .roadmap-state.json from output_dir
    -> if config.tdd_file is None and state has tdd_file and file exists:
        config.tdd_file = Path(state["tdd_file"])
        echo "[tasklist] Auto-wired tdd_file from roadmap state: /abs/path/T"
    -> same for prd_file
    -> proceeds with normal validation flow
```

---

## 8. Tasklist Gate (`gates.py`)

**File:** `src/superclaude/cli/tasklist/gates.py`

`TASKLIST_FIDELITY_GATE` defines:
- **Required frontmatter fields:** `high_severity_count`, `medium_severity_count`, `low_severity_count`, `total_deviations`, `validation_complete`, `tasklist_ready`
- **Min lines:** 20
- **Enforcement tier:** STRICT
- **Semantic checks:**
  1. `high_severity_count_zero` -- must be 0 to pass
  2. `tasklist_ready_consistent` -- must be consistent with severity counts and validation_complete

Both semantic check functions are imported from `roadmap/gates.py` (reused).

---

## 9. Summary of Findings

1. **`superclaude tasklist generate` does NOT exist.** Only `validate` is a CLI command.
2. **`--tdd-file` is fully wired** end-to-end: CLI -> config -> executor inputs -> prompt builder -> embedded content + prompt instructions.
3. **`--prd-file` is fully wired** end-to-end: CLI -> config -> executor inputs (embedded) AND prompt builder (`prd_file=config.prd_file` at line 206) -> conditional "Supplementary PRD Validation" block (prompts.py lines 126-139) with 3 checks (S7, S19, S12/S22), all MEDIUM severity.
4. **Auto-wire from `.roadmap-state.json` does not exist yet.** Neither `tdd_file` nor `prd_file` are saved to state, and no auto-wire reader exists in the tasklist executor.
5. **The gate criteria (TASKLIST_FIDELITY_GATE)** are agnostic to TDD/PRD -- they check the same frontmatter fields regardless. No gate changes needed for PRD integration.
6. **`read_state()` and `write_state()`** are simple JSON utilities. The state schema is version 1 with no current support for supplementary file paths.
