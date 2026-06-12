# Atom 2 — Confirmed Signatures & Line Numbers

**Confirmed:** 2026-06-08, read directly from live source. No fabrication.

## `src/superclaude/cli/prd/prompts.py`

- `Path` imported at **line 17** (`from pathlib import Path`).
- `_load_json(path) -> dict` — **lines 37-39**, calls `path.read_text(...)` UNGUARDED.
- `_read_file(path, max_bytes=50_000) -> str` — **lines 42-47**, calls `path.read_text(...)` UNGUARDED.

### Five REQUIRED Stage-A reads (to convert)

| Line | Current statement | Helper type | Convert to | producer_step |
|------|-------------------|-------------|-----------|---------------|
| 158 | `parsed = _load_json(config.task_dir / "parsed-request.json")` (build_scope_discovery_prompt) | dict | `_load_json_required` | `"parse-request"` |
| 257 | `scope_content = _read_file(config.task_dir / "scope-discovery-raw.md")` (build_research_notes_prompt) | str | `_read_required` | `"scope-discovery"` |
| 258 | `parsed = _load_json(config.task_dir / "parsed-request.json")` (build_research_notes_prompt) | dict | `_load_json_required` | `"parse-request"` |
| 340 | `notes_content = _read_file(config.task_dir / "research-notes.md")` | str | `_read_required` | `"research-notes"` |
| 440 | `notes = _read_file(config.task_dir / "research-notes.md")` | str | `_read_required` | `"research-notes"` |

Type split confirmed: 257/340/440 are `_read_file` (str); 158/258 are `_load_json` (dict).
A single str helper CANNOT wrap 158/258 without corrupting their dict consumers.

### Four Stage-B `_derive_*` reads — LEAVE UNCHANGED (already guarded with `.is_file()`)

- 740: `notes = notes_path.read_text(...) if notes_path.is_file() else ""`
- 755: `if parsed_path.is_file():`
- 775: `notes = notes_path.read_text(...) if notes_path.is_file() else ""`
- 787: `scope_path.read_text(...)[:2000] if scope_path.is_file() else ""`

### Adjacent reads NOT to touch

- 441-445: `config.skill_refs_dir / ...` reads (build-request-template, agent-prompts, synthesis-mapping, validation-checklists, operational-guidance). Convert ONLY the `config.task_dir / "research-notes.md"` read at 440.
- 540: `_read_file(task_path)` — not a Stage-A required task_dir read in scope.
- 413: `if not artifact.is_file():` — a guard, not a target.

## `src/superclaude/cli/prd/executor.py`

- `_build_prompt` call site: **line 682** — `prompt = self._build_prompt(builder_name, step_id=step_id)`.
  **DRIFT: +10 lines** from the task's expected ~672 (report cites 672; live source is 682). Noted.
- This call is OUTSIDE any try/except.
- `except RuntimeError` (proc start/wait) at **lines 701-705** → returns `PrdStepResult(status=ERROR, exit_code=-1)`.
- `except OSError` (the `raw_output` read) at **lines 709-712** — a DIFFERENT region; catching `MissingArtifactError` at 682 will not collide with it.
- `prompts` is NOT imported at executor module top; it is imported locally inside `_build_prompt` (line 1212: `from . import prompts`). prompts.py does not import executor, so a local `from .prompts import MissingArtifactError` inside `_run_subprocess_step` is safe (no circular import) and mirrors the existing local-import pattern.

## ⚠️ Model-shape correction (load-bearing discovery)

The task Step 3.1 expected `halt_step`/`halt_reason` to be assignable fields on
`PrdStepResult` (claimed "verified in models.py ~221-252"). **This is inaccurate.**

- `PrdStepResult` (models.py 230-244) fields: `exit_code, output_bytes, error_bytes,
  artifacts_produced, agent_type, fix_cycle, qa_verdict` + inherited from `StepResult`
  (`step, status, attempt, gate_failure_reason, started_at, finished_at, remediated,
  remediations`). **No `halt_reason`, no `halt_step`.**
- `halt_step` / `halt_reason` are fields on the AGGREGATE `PrdPipelineResult`
  (models.py **261-262**), set by the Stage-A loop in `run()` from a template
  (`f"hard failure: {status.value}"`).

**Decision:** To give the Atom-2 HALT `PrdStepResult` a clear, artifact-specific reason
that the Step 3.9 unit test can assert on, ADD an optional field
`halt_reason: Optional[str] = None` to `PrdStepResult`. `Optional` is already imported in
models.py. This is backward-compatible (default None) and makes `halt_reason` a constructor
kwarg. The except branch returns:

```python
return PrdStepResult(
    status=PrdStepStatus.HALT,
    exit_code=-1,
    halt_reason=f"missing required artifact {exc.path.name} (producer: {exc.producer_step})",
)
```

The Stage-A halt block (Atom 1, PG-1-verified) is LEFT UNTOUCHED. For the reported
scenario (scope-discovery ERROR) the pipeline-level `result.halt_reason` remains
`"hard failure: error"` (Atom 1 template) with `halt_step == "scope-discovery"` — which is
what the Step 3.10 e2e test asserts. The step-level `halt_reason` (artifact name) is what the
Step 3.9 unit test asserts on the `_run_subprocess_step` return value. Both satisfied without
re-editing the locked Atom-1 loop.

## Drift summary

- prompts.py read sites: NO drift (158/257/258/340/440 exact; Stage-B 740/755/775/787 exact).
- executor.py `_build_prompt` call site: **+10 line drift** (682 vs expected 672).
- `PrdStepResult` halt_reason field: **does not exist** — adding it (see correction above).
