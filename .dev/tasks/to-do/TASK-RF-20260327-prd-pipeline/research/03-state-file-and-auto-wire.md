# Research 03: State File and Auto-Wire Feasibility

**Status**: Complete
**Researcher**: research-agent (state-file-autowire)
**Date**: 2026-03-27
**Scope**: `src/superclaude/cli/roadmap/executor.py` (state handling), `src/superclaude/cli/tasklist/executor.py` (config resolution)

---

## 1. Where `.roadmap-state.json` Is Written

### Function: `_save_state()`
**Location**: `src/superclaude/cli/roadmap/executor.py:1361-1473`

Called at `executor.py:1801` after `execute_pipeline()` returns results. Also called at `executor.py:2011` after resumed pipeline completion.

### Write mechanism
Uses `write_state()` at `executor.py:1623-1630` -- atomic write via tmp file + `os.replace()`:
```python
def write_state(state: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2), encoding="utf-8")
    _os.replace(str(tmp), str(path))
```

### Current Schema (schema_version: 1)
Composed at `executor.py:1421-1439`:
```json
{
  "schema_version": 1,
  "spec_file": "<absolute path to spec>",
  "spec_hash": "<sha256 hex of spec content>",
  "agents": [{"model": "opus", "persona": "architect"}, ...],
  "depth": "standard",
  "last_run": "<ISO 8601 UTC>",
  "steps": {
    "<step-id>": {
      "status": "<pass|fail|timeout|...>",
      "attempt": 1,
      "output_file": "<path>",
      "started_at": "<ISO 8601>",
      "completed_at": "<ISO 8601>"
    }
  }
}
```

### Conditionally preserved keys (merged from existing state)
- `validation` -- preserved at `executor.py:1448-1449`
- `fidelity_status` -- derived from spec-fidelity result or preserved, `executor.py:1452-1459`
- `remediate` -- `executor.py:1461-1465`
- `certify` -- `executor.py:1467-1471`
- `remediation_attempts` -- read at `executor.py:1284` (not written by `_save_state` directly)

### Key finding: `tdd_file` and `input_type` are NOT stored
Despite `RoadmapConfig` having `tdd_file: Path | None` (`models.py:115`) and `input_type` (`models.py:114`), the `_save_state()` function does NOT persist either field to the state file. This is a gap.

---

## 2. Where `.roadmap-state.json` Is Read

### Function: `read_state()`
**Location**: `src/superclaude/cli/roadmap/executor.py:1633-1643`

Graceful recovery on missing/malformed files (returns `None`).

### Read sites (all in `executor.py`):
| Line | Context | Purpose |
|------|---------|---------|
| 1280 | `_check_remediation_budget()` | Read `remediation_attempts` |
| 1391 | `_save_state()` | Merge with existing state |
| 1673 | `_restore_from_state()` | Restore agents/depth on --resume |
| 1844 | `execute_roadmap()` | Check if validation already completed |
| 1872 | `_apply_resume_after_spec_patch()` | Read state for resume cycle |
| 1962 | Remediate RMW cycle | Read-modify-write for remediation |
| 1983 | Post-write verification | Verify state was written |
| 2051 | `_save_validation_status()` | Update validation status |
| 2267 | `_auto_invoke_certify()` | Read certify status |

### Resume entry: `_restore_from_state()`
**Location**: `executor.py:1661-1719`
Called at `executor.py:1758` (inside `execute_roadmap`) when `resume=True`.
Restores `agents` and `depth` from state when CLI flags were not explicitly passed.
This is the model for how auto-wire restore should work.

---

## 3. Tasklist Executor: Current State

### File: `src/superclaude/cli/tasklist/executor.py`
This is a **validation** executor only (validates tasklist fidelity against a roadmap). It does NOT generate tasklists.

### Does it read `.roadmap-state.json`? **No.**
Zero references to `roadmap-state`, `state.json`, `read_state`, or any state file in the tasklist module.

### Current config resolution
- CLI flags in `commands.py:67-74`: `output_dir`, `roadmap_file`, `tasklist_dir`, `model`, `max_turns`, `debug`, `tdd_file`
- Defaults resolved at `commands.py:93-104`: roadmap defaults to `{output_dir}/roadmap.md`, tasklist dir defaults to `{output_dir}`
- Config object: `TasklistValidateConfig` at `models.py:15-25` -- has `tdd_file` field already

### Where auto-wire logic should go
The ideal insertion point is in `commands.py:validate()` function, between the default resolution block (line 93-104) and the config construction (line 106-115). This is where `roadmap_file` and `tasklist_dir` are resolved from defaults -- `tdd_file` and `prd_file` auto-wire should follow the same pattern.

**Specific insertion point**: After `executor.py:103` (resolved_tasklist_dir) and before `executor.py:106` (config construction).

---

## 4. Implementation Plan

### 4.1 State File Changes (roadmap executor)

**Add to `_save_state()` at `executor.py:1427` (inside the state dict literal):**
```python
"tdd_file": str(config.tdd_file) if config.tdd_file else None,
"input_type": config.input_type,
```

No schema_version bump needed (additive-only change; readers use `.get()` with defaults).

### 4.2 Auto-Wire Logic (tasklist commands)

**Add a helper function** in `tasklist/commands.py` or a new `tasklist/autowire.py`:
```python
def _autowire_from_state(output_dir: Path) -> dict:
    """Read .roadmap-state.json from output_dir and extract auto-wire fields."""
    state_file = output_dir / ".roadmap-state.json"
    # Reuse read_state from roadmap module
    from ..roadmap.executor import read_state
    state = read_state(state_file)
    if state is None:
        return {}
    return {
        "tdd_file": state.get("tdd_file"),
        "spec_file": state.get("spec_file"),
    }
```

**Insertion in `commands.py:validate()`** after line 104:
```python
# Auto-wire from .roadmap-state.json (explicit flags take precedence)
if tdd_file is None:
    wired = _autowire_from_state(resolved_output)
    if wired.get("tdd_file"):
        tdd_file = Path(wired["tdd_file"])
        if tdd_file.exists():
            click.echo(f"[tasklist validate] Auto-wired --tdd-file from .roadmap-state.json: {tdd_file}")
        else:
            click.echo(f"[tasklist validate] WARNING: Auto-wired tdd_file not found: {tdd_file}", err=True)
            tdd_file = None
```

### 4.3 Precedence Rules

1. **Explicit CLI flag** always wins (user passed `--tdd-file`)
2. **Auto-wired from `.roadmap-state.json`** used when flag is None
3. **None/absent** -- no TDD/PRD enrichment

This matches the precedence pattern already established by `_restore_from_state()` at `executor.py:1686`: "if not agents_explicit: ... restore from state".

### 4.4 Future: PRD File Auto-Wire

`RoadmapConfig` does not currently have a `prd_file` field (`models.py:94-115`). To support PRD auto-wire:
1. Add `prd_file: Path | None = None` to `RoadmapConfig`
2. Add `"prd_file"` to the state dict in `_save_state()`
3. Add `--prd-file` CLI option to `roadmap/commands.py`
4. Add `prd_file` to `TasklistValidateConfig` model
5. Wire it into auto-wire helper and tasklist prompts

### 4.5 Cross-Module Import Consideration

The tasklist module would import `read_state` from `roadmap.executor`. This creates a cross-module dependency. Two alternatives:
- **Option A (recommended)**: Extract `read_state`/`write_state` into `pipeline/state.py` (shared utility)
- **Option B**: Duplicate the 10-line `read_state` function in tasklist (violates DRY but avoids coupling)

---

## Summary of Key Findings

| Question | Answer |
|----------|--------|
| State file location | `{output_dir}/.roadmap-state.json` |
| Schema version | 1 (field at `executor.py:1422`) |
| Write function | `_save_state()` at `executor.py:1361`, uses `write_state()` at `executor.py:1623` |
| Read function | `read_state()` at `executor.py:1633` |
| tdd_file in state? | **No** -- gap; `RoadmapConfig.tdd_file` exists but is not persisted |
| Tasklist reads state? | **No** -- zero references to state file |
| Auto-wire insertion point | `tasklist/commands.py:104` (after default resolution, before config construction) |
| Precedence model | Explicit flag > auto-wired > None (matches `_restore_from_state` pattern) |
