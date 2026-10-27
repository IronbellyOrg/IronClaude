# Tasklist: spec-fidelity Pipeline Crash Fix

> **Source**: Diagnostic from `/sc:troubleshoot` + adversarial debate refinement
> **Branch**: `feat/v3.65-prd-tdd-Refactor`
> **Scope**: 2 files, 3 surgical fixes

---

## Tasks

### T01: Guard empty `findings_by_file` in `execute_remediation`
- **Status**: pending
- **File**: `src/superclaude/cli/roadmap/remediate_executor.py`
- **Line**: 753 (after `all_target_files = list(findings_by_file.keys())`)
- **Action**: Add early-return guard with warning log
- **Code**:
  ```python
  if not all_target_files:
      _log.warning(
          "No target files for remediation — findings lack files_affected; "
          "skipping remediation and reporting as PARTIAL",
      )
      return "PARTIAL", []
  ```
- **Rationale**: Defense-in-depth — prevents `ThreadPoolExecutor(max_workers=0)` crash from any caller. Returns `("PARTIAL", [])` matching the documented return contract `(str, list)`.
- **Verification**: `uv run pytest tests/ -k remediat -v` (if tests exist), otherwise manual inspection of return type consistency with lines 822, 836, 847.

### T02: Guard empty `findings_by_file` in `_run_remediation`
- **Status**: pending
- **File**: `src/superclaude/cli/roadmap/executor.py`
- **Line**: 946 (after findings grouping loop, before `execute_remediation` call)
- **Action**: Add early-return guard with warning log including orphaned finding count
- **Code**:
  ```python
  if not findings_by_file:
      _log.warning(
          "spec-fidelity: %d active high findings have no file associations — "
          "skipping remediation",
          len(active_highs),
      )
      return
  ```
- **Rationale**: Caller-side guard — catches the data quality issue at the source and logs the count of orphaned findings for diagnostics. Belt-and-suspenders with T01.
- **Verification**: Confirm `_run_remediation` return value is not consumed (bare call at convergence.py:588).

### T03: Fix `run_semantic_layer` call signature mismatch
- **Status**: pending
- **File**: `src/superclaude/cli/roadmap/executor.py`
- **Lines**: 887-900 (inside `_run_checkers` closure)
- **Action**: Add `split_into_sections` import, parse spec/roadmap files into sections, fix call arguments
- **Code**: Replace lines 894-900 with:
  ```python
  from .spec_parser import split_into_sections
  
  # ... (existing structural_findings code stays) ...
  
  try:
      spec_sections = split_into_sections(spec_path.read_text())
      roadmap_sections = split_into_sections(roadmap_path.read_text())
      semantic_result = run_semantic_layer(
          spec_sections=spec_sections,
          roadmap_sections=roadmap_sections,
          output_dir=config.output_dir,
          structural_findings=structural_findings,
          registry=reg,
      )
      if semantic_result and semantic_result.findings:
          reg.merge_findings([], semantic_result.findings, run_number)
  except Exception as exc:
      _log.warning("Semantic layer failed: %s (continuing with structural only)", exc)
  ```
- **Rationale**: Fixes the `got an unexpected keyword argument 'spec_path'` error by correctly parsing files into `SpecSection` objects that `run_semantic_layer` expects. Uses `Path` objects directly (already `Path` type). Keeps existing `try/except` for graceful degradation.
- **Verification**: `uv run pytest tests/ -k semantic -v` (if tests exist), then full pipeline re-run.

### T04: Run tests and verify
- **Status**: pending
- **Action**: Run `uv run pytest tests/ -v --tb=short` to check for regressions, then verify the specific files compile cleanly.
- **Depends**: T01, T02, T03
