# F2 Discovery Confirmation — malformed-artifact guard target

**Date:** 2026-06-08
**Files inspected (live source):** `src/superclaude/cli/prd/prompts.py`, `src/superclaude/cli/prd/executor.py`

## prompts.py — confirmed line ranges (observed, not approximate)

- `import json` at **line 15** (module top — confirms `json` already imported).
- `_load_json(path)` at **lines 37-39** — UNGUARDED:
  ```python
  def _load_json(path: Path) -> dict:
      """Load and parse a JSON file."""
      return json.loads(path.read_text(encoding="utf-8"))
  ```
- `MissingArtifactError(FileNotFoundError)` at **lines 50-64**, `__init__(self, path, producer_step)`:
  ```python
  def __init__(self, path: Path, producer_step: str) -> None:
      self.path = path
      self.producer_step = producer_step
      super().__init__(
          f"Required artifact {path.name} is missing — its producer step "
          f"'{producer_step}' did not complete successfully. Path: {path}"
      )
  ```
  Sets `self.path` and `self.producer_step`.
- `_load_json_required(path, producer_step)` at **lines 74-78** — the F2 target, current body:
  ```python
  def _load_json_required(path: Path, producer_step: str) -> dict:
      """Load a REQUIRED JSON artifact, raising MissingArtifactError if absent."""
      if not path.is_file():
          raise MissingArtifactError(path, producer_step)
      return _load_json(path)
  ```
  Guards `path.is_file()` ONLY; the `_load_json(path)` call is unguarded against a
  present-but-malformed file → an uncaught `json.JSONDecodeError` escapes.

## executor.py — call-site catch (confirmed)

`_run_subprocess_step` build-prompt block at **lines 692-704**:

```python
from .prompts import MissingArtifactError

try:
    prompt = self._build_prompt(builder_name, step_id=step_id)
except MissingArtifactError as exc:
    return PrdStepResult(
        status=PrdStepStatus.HALT,
        exit_code=-1,
        halt_reason=(
            f"missing required artifact {exc.path.name} "
            f"(producer: {exc.producer_step})"
        ),
    )
```

The handler builds the HALT from `exc.path.name` and `exc.producer_step`.

## Subclass-catch verdict

**The call-site `except MissingArtifactError` WILL catch a subclass unchanged.** A new
`MalformedArtifactError(MissingArtifactError)` that sets the same `self.path` and
`self.producer_step` attributes is caught here automatically (Python subclass catch),
and the `halt_reason` template references only `exc.path.name` / `exc.producer_step`
(both present on the subclass), so the existing HALT path works with NO change to
`executor.py`.

## Note on the optional message tweak (defer to Step 2.2)

The `halt_reason` template hardcodes the word **"missing"** (`f"missing required artifact ..."`).
A malformed (but present) file would read inaccurately as "missing required artifact". This is
the OPTIONAL engineer's-call tweak in Step 2.2 — derive a generic verb (e.g. "unusable required
artifact") if judged worthwhile. The exception MESSAGE itself (raised in prompts.py) is accurate;
only the executor's short halt_reason summary reuses "missing". Decision deferred to Step 2.2.
