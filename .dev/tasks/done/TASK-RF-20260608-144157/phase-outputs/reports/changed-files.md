# Changed-File Inventory — TASK-RF-20260608-144157 (F2/F4/F5)

**Date:** 2026-06-08 15:37
**Final validation verdict:** PASS — ruff clean on all edited files; `uv run pytest tests/cli/prd/ -v` → **160 passed** (baseline 158 + 2 new tests, zero regressions). Source: `final-summary.md`.

> **Scope note (IMPORTANT):** This task ran on branch `fix/prd-document-capture-hotfix`, whose
> working tree already contained UNCOMMITTED pre-existing changes from the prior document-capture /
> F1 / Atom hotfix work (confirmed at session start: `models.py`, `test_models.py`, `executor.py`,
> `prompts.py`, `test_e2e.py` were already `M` before this task began). `git diff HEAD` therefore
> shows the CUMULATIVE branch delta, not just this task's edits. The table below lists the files
> THIS task (F2/F4/F5) actually edited; `models.py` and `test_models.py` were **read-only** for this
> task and their diffs belong to the pre-existing branch work, not to F2/F4/F5.

## Files changed BY THIS TASK (F2/F4/F5)

| File | Finding | Change |
|---|---|---|
| `src/superclaude/cli/prd/prompts.py` | **F2** | Added `MalformedArtifactError(MissingArtifactError)` subclass (sets `path`/`producer_step`, accurate "malformed/unparseable" message); guarded `_load_json_required` with `try/except json.JSONDecodeError` raising `MalformedArtifactError(...) from exc`. |
| `src/superclaude/cli/prd/executor.py` | **F2 (optional tweak)** | `_run_subprocess_step` call site: import `MalformedArtifactError` alongside `MissingArtifactError`; derive the `halt_reason` verb (`"malformed"` vs `"missing"`) from the exception type. No HALT-behavior change; existing missing-artifact tests unaffected. |
| `tests/cli/prd/test_e2e.py` | **F2 + F5** | F2: added `test_malformed_required_artifact_yields_graceful_halt` (REAL builder path, no `_build_prompt` stub → graceful HALT). F5: strengthened `test_e2e_standard_tier_validation_fail_does_not_halt` to assert scope-discovery's recorded status == `PrdStepStatus.VALIDATION_FAIL` (mapped via `_STAGE_A_STEPS` order). |
| `tests/cli/prd/test_prompts.py` | **F4** | Added `test_required_read_call_sites_pin_to_step_artifact_files` pinning the inline REQUIRED-read `(producer_step, filename)` pairs to `_STEP_ARTIFACT_FILES` (imported in-test only; no circular import). Complements existing `test_prompt_executor_mapping_sync`. |

## F2 `MalformedArtifactError` / `_load_json_required` line range

In `src/superclaude/cli/prd/prompts.py`: `MalformedArtifactError` class at **lines 67-87**; guarded `_load_json_required` at **lines 98-112** (`try: return _load_json(path)` / `except json.JSONDecodeError: raise MalformedArtifactError(path, producer_step) from exc`).

## Finding → changed-file coverage check

- **F2** → `prompts.py` (guard + class) + `test_e2e.py` (malformed test) + `executor.py` (verb tweak). ✅
- **F4** → `test_prompts.py` (consistency-guard test). ✅
- **F5** → `test_e2e.py` (strengthened VALIDATION_FAIL assertion). ✅

Every finding maps to at least one file changed by this task.

## Files in the working tree NOT changed by this task (pre-existing branch work)

- `src/superclaude/cli/prd/models.py` — read-only for this task (consulted for `PrdStepStatus.VALIDATION_FAIL` and `PrdStepResult`/`StepResult` fields). Its `M` diff is pre-existing branch work.
- `tests/cli/prd/test_models.py` — not touched by this task. Pre-existing branch work.
