# D-0003: OQ-G/OQ-H/OQ-I Resolution — Executor Interface Questions

**Task:** T01.03
**Date:** 2026-03-16
**Status:** RESOLVED

---

## OQ-G Resolution — `build_remediate_step()` Module Location

**Search result:** `build_remediate_step` does **NOT exist** in the codebase.

**Disposition:** Requires creation in v2.26.

**Confirmed module location for creation:** `src/superclaude/cli/roadmap/remediate.py`

**Evidence:**
- `remediate.py` exists at `src/superclaude/cli/roadmap/remediate.py`
- Current contents: `RemediationScope` class, `format_validation_summary()`, `should_skip_prompt()`, `filter_findings()`, `generate_remediation_tasklist()`, `generate_stub_tasklist()`
- Imports only: `from .models import Finding` (no circular import risk)
- Placing `build_remediate_step()` here follows existing pattern — remediate.py is the natural home for remediation step construction

**Planned signature:**
```python
def build_remediate_step(findings: list[Finding], config: RemediationConfig) -> Step:
    """Build a pipeline Step for remediation based on filtered findings."""
```

---

## OQ-H Resolution — `roadmap_run_step()` Interface for Hash Injection

**File:** `src/superclaude/cli/roadmap/executor.py` (lines 159–266)

**Confirmed signature:**
```python
def roadmap_run_step(
    step: Step,
    config: PipelineConfig,
    cancel_check: Callable[[], bool],
) -> StepResult:
```

**Hook injection point:** There is already a post-step hook pattern in `roadmap_run_step()`. After step completion (exit_code == 0), the function calls `_sanitize_output()` then conditionally calls `_inject_pipeline_diagnostics()` if `step.id == "extract"`.

```python
# Line 255-258 in executor.py:
# Inject executor-populated fields into extract step frontmatter (FR-033)
if step.id == "extract" and step.output_file.exists():
    _inject_pipeline_diagnostics(step.output_file, started_at, finished_at)
```

**`roadmap_hash` injection strategy:** The `_inject_pipeline_diagnostics()` pattern provides the exact precedent for `roadmap_hash` injection. For v2.26, a similar conditional block can be added post-sanitization:

```python
if step.id in HASH_INJECTION_STEPS and step.output_file.exists():
    _inject_roadmap_hash(step.output_file, config)
```

The `roadmap_run_step()` function signature does **not need to change** — hash injection happens as a post-step side effect within the existing function body, following the established `_inject_pipeline_diagnostics` pattern.

---

## OQ-I Resolution — `token_count` Field Availability

**Search result:** No `token_count`, `input_tokens`, or `output_tokens` fields found in the CLI executor code or process module.

**`ClaudeProcess` in `src/superclaude/cli/pipeline/process.py`:** The process module launches Claude as a subprocess and captures output to a file. It does not parse Claude API response JSON — it captures stdout as text output.

**Disposition:** `token_count` is **NOT available** via the current subprocess execution model. Claude is launched as a CLI subprocess (`claude --output-format text`), not via the Python SDK. The subprocess exit code and output file are the only structured outputs.

**Best-effort fallback (per NFR-024):** Token count tracking for v2.26 should use output file size as a proxy metric (bytes of output ≈ rough token count), or be documented as "not available" and deferred to a future SDK-based execution model.

**Decision:** Token count availability = **best-effort fallback defined**: log output file size in bytes as a proxy; mark token_count field as Optional[int] = None in any diagnostic structs; no blocking dependency on actual token counts.

---

## Summary Table

| OQ | Question | Status | Finding |
|----|----------|--------|---------|
| OQ-G | `build_remediate_step()` location | Not found → create in `remediate.py` | `src/superclaude/cli/roadmap/remediate.py` |
| OQ-H | `roadmap_run_step()` hook injection point | Confirmed at lines 255-258 | Post-sanitize conditional block pattern |
| OQ-I | `token_count` field availability | Not available via subprocess | Best-effort fallback: output file size proxy |
