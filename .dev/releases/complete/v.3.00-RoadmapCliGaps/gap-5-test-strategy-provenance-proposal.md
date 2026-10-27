# Gap #5 — Test-Strategy Missing Provenance Fields: Implementation Proposal

## Problem Statement

The source protocol's `test-strategy.md` frontmatter schema (defined in `src/superclaude/skills/sc-roadmap-protocol/refs/templates.md`) specifies three provenance fields:

```yaml
spec_source: <path>
generated: <ISO-8601 timestamp>
generator: sc:roadmap
```

The CLI's `build_test_strategy_prompt()` in `prompts.py` only requests `validation_milestones` and `interleave_ratio`. The `TEST_STRATEGY_GATE` in `gates.py` likewise only validates those two fields. The provenance triple (`spec_source`, `generated`, `generator`) is entirely absent from both the prompt and the gate.

**Severity**: LOW -- these are metadata fields that do not affect correctness of the test strategy content itself. However, they are important for artifact traceability and audit trails.

---

## Analysis

### Question 1: Claude-produced vs. executor-injected?

**Recommendation: Executor-injected.** Three reasons:

1. **Precedent exists.** The executor already injects `pipeline_diagnostics` into the extraction step's frontmatter post-subprocess via `_inject_pipeline_diagnostics()` (lines 123-157 of `executor.py`). The pattern is proven. **Note**: The existing function uses plain `write_text()`, not atomic write (see Refactoring Notes).

2. **The LLM cannot reliably produce these values.** `generated` requires the real wall-clock timestamp of when the step completed (not when Claude "thinks" it is). `generator` is a fixed string (`sc:roadmap`) that the LLM might hallucinate variants of. `spec_source` is the original spec filename, which the executor already tracks as `config.spec_file`.

3. **Prompt simplicity.** Adding three more frontmatter instructions to the prompt increases token cost (~80 tokens) on every invocation for fields that are deterministic and known to the executor. The extract step already asks Claude to produce `spec_source`/`generated`/`generator`, and that works because Claude has direct access to the spec file content. For test-strategy, Claude doesn't see the original spec -- it sees the roadmap and extraction, so it would have to parrot a `spec_source` value from nested frontmatter, introducing a propagation-error risk.

### Question 2: Where in the pipeline code would injection happen?

In `roadmap_run_step()` in `executor.py`, immediately after the existing extract-step injection block (lines 256-258). The pattern would be:

```python
# Inject executor-populated fields into extract step frontmatter (FR-033)
if step.id == "extract" and step.output_file.exists():
    _inject_pipeline_diagnostics(step.output_file, started_at, finished_at)

# Inject provenance fields into test-strategy frontmatter
if step.id == "test-strategy" and step.output_file.exists():
    _inject_provenance_fields(
        step.output_file,
        spec_source=config.spec_file.name if hasattr(config, "spec_file") else "unknown",
        finished_at=finished_at,
    )
```

A new function `_inject_provenance_fields()` would:
1. Read the output file
2. Verify it starts with `---` (frontmatter present)
3. Find the closing `---` delimiter
4. Insert the three provenance lines before the closing delimiter
5. Write back to the file (plain `write_text()`, matching the existing `_inject_pipeline_diagnostics()` pattern)

This mirrors `_inject_pipeline_diagnostics()` exactly. **Note**: The existing pattern uses non-atomic `write_text()`. The proposed implementation below upgrades to atomic write (tmp + `os.replace()`), which is an improvement over the precedent but not strictly necessary for consistency. Either approach is acceptable; see Refactoring Notes.

### Question 3: Should the gate validate these fields regardless of who produces them?

**Yes.** The gate should validate presence of provenance fields regardless of their source. This is the defense-in-depth principle: if executor injection fails silently (e.g., file write error, frontmatter parsing edge case), the gate catches it.

However, since the gap is LOW severity and the test-strategy gate is `STANDARD` tier (not `STRICT`), adding the fields to `required_frontmatter_fields` is sufficient. No semantic checks are needed -- the existing `_frontmatter_values_non_empty` check can be optionally added but is not strictly necessary given that the executor produces deterministic non-empty values.

### Question 4: Tradeoff between prompt complexity and artifact completeness

| Approach | Prompt tokens | Reliability | Traceability |
|----------|--------------|-------------|--------------|
| Prompt-only | +~80 tokens/call | Medium (LLM may hallucinate `generator`, get `generated` wrong) | Full (if LLM complies) |
| Executor-only | +0 tokens | High (deterministic values) | Full |
| Both (prompt + executor override) | +~80 tokens/call | Highest (redundant) | Full |

**Winner: Executor-only.** Zero prompt overhead, highest reliability, and the precedent is already established in the codebase.

---

## Implementation Plan

### Changes Required

#### 1. `src/superclaude/cli/roadmap/executor.py`

Add a new function `_inject_provenance_fields()` and call it from `roadmap_run_step()`.

```python
def _inject_provenance_fields(
    output_file: Path,
    spec_source: str,
    finished_at: datetime,
) -> None:
    """Inject spec_source, generated, and generator into step frontmatter.

    These provenance fields are deterministic metadata the executor knows
    but the LLM cannot reliably produce. Uses atomic write.
    """
    import os

    content = output_file.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return

    end_idx = content.find("\n---", 3)
    if end_idx == -1:
        return

    provenance_lines = (
        f"spec_source: {spec_source}\n"
        f"generated: \"{finished_at.isoformat()}\"\n"
        f"generator: sc:roadmap"
    )

    new_content = (
        content[:end_idx]
        + "\n"
        + provenance_lines
        + content[end_idx:]
    )

    tmp_file = output_file.with_suffix(output_file.suffix + ".tmp")
    tmp_file.write_text(new_content, encoding="utf-8")
    os.replace(tmp_file, output_file)
```

In `roadmap_run_step()`, after line 258:

```python
# Inject provenance fields into test-strategy frontmatter
if step.id == "test-strategy" and step.output_file.exists():
    _inject_provenance_fields(
        step.output_file,
        spec_source=config.spec_file.name if hasattr(config, "spec_file") else "unknown",
        finished_at=finished_at,
    )
```

**Note on `config` type**: `roadmap_run_step` receives `config: PipelineConfig`, but at runtime it is always a `RoadmapConfig` (which has `spec_file`). The `hasattr` guard is defensive. Alternatively, the function signature could accept `RoadmapConfig` directly, but that would change the `StepRunner` protocol. The safer approach is the `hasattr` guard or a downcast with `isinstance`.

#### 2. `src/superclaude/cli/roadmap/gates.py`

Update `TEST_STRATEGY_GATE` to include the provenance fields:

```python
TEST_STRATEGY_GATE = GateCriteria(
    required_frontmatter_fields=[
        "spec_source",
        "generated",
        "generator",
        "validation_milestones",
        "interleave_ratio",
    ],
    min_lines=40,
    enforcement_tier="STANDARD",
)
```

#### 3. No prompt changes needed

`build_test_strategy_prompt()` remains unchanged. The provenance fields are not requested from Claude.

### Additional Template Fields Not Addressed

The template schema also includes fields not in the current gate or prompt:

- `validation_philosophy: continuous-parallel` -- fixed value, could be executor-injected
- `work_milestones: <count>` -- content-dependent, would need prompt addition
- `major_issue_policy: stop-and-fix` -- fixed value, could be executor-injected
- `complexity_class: <LOW|MEDIUM|HIGH>` -- available from extraction, could be executor-injected

These are out of scope for this gap but noted for future alignment work.

### Test Plan

1. **Unit test for `_inject_provenance_fields()`**: Create a temp file with valid frontmatter, call the function, verify `spec_source`, `generated`, and `generator` are present in the output.
2. **Unit test for missing frontmatter**: Verify function is a no-op when file has no `---` delimiters.
3. **Unit test for gate**: Verify `TEST_STRATEGY_GATE.required_frontmatter_fields` includes all five fields.
4. **Integration test**: Run a dry-run pipeline step and verify the gate definition includes provenance fields.

### Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Injection fails silently (no frontmatter in output) | Low | Low | Gate catches missing fields |
| `config` lacks `spec_file` attribute | Very Low | Low | `hasattr` guard with fallback |
| Existing tests break due to gate field additions | Medium | Low | Update test fixtures to include provenance fields |
| Atomic write fails (disk full, permissions) | Very Low | Medium | Exception propagates, step fails, retry handles it |

### Effort Estimate

- Implementation: ~30 minutes (one new function, two line changes)
- Tests: ~20 minutes (three unit tests)
- Total: ~50 minutes

---

## Decision Summary

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Who produces provenance? | Executor | Deterministic values, zero prompt overhead, existing precedent |
| Injection point | `roadmap_run_step()` after sanitize | Mirrors existing `_inject_pipeline_diagnostics` pattern |
| Gate validation? | Yes, add to `required_frontmatter_fields` | Defense-in-depth; catches injection failures |
| Semantic checks needed? | No | Values are deterministic; field-presence check is sufficient |
| Prompt changes? | None | Avoids token waste and LLM hallucination risk |

---

## Refactoring Notes

The following corrections were applied during code-level validation (2026-03-18):

### RN-1: Atomic write claim is inaccurate for the precedent function

**Issue**: The proposal stated that `_inject_pipeline_diagnostics()` is "atomic-write-safe" and uses tmp + `os.replace()`. This is incorrect. The actual implementation at line 157 of `executor.py` uses plain `output_file.write_text(new_content, encoding="utf-8")` -- a non-atomic write. Only `_sanitize_output()` (line 82) uses the atomic tmp + `os.replace()` pattern.

**Impact**: Low. The claim that the new function "mirrors `_inject_pipeline_diagnostics()` exactly" was misleading. The proposed `_inject_provenance_fields()` implementation actually upgrades to atomic write, which is a minor improvement over the precedent. Both approaches are acceptable since the file is not read concurrently during this phase.

**Resolution**: Updated the Analysis section (Questions 1 and 2) to accurately describe the existing write pattern. The proposed implementation retains atomic write as an improvement, but implementers may also use plain `write_text()` for strict consistency with the precedent.

### RN-2: Question 2 call-site signature mismatch (corrected)

**Issue**: The inline code in Question 2 showed `_inject_provenance_fields(step.output_file, config, finished_at)` but the function signature takes `spec_source: str`, not `config`. The Implementation Plan section had the correct call with `spec_source=config.spec_file.name`.

**Impact**: Cosmetic. Would cause confusion for implementers reading the Analysis section before the Implementation Plan.

**Resolution**: Updated the Question 2 code block to match the Implementation Plan's correct call-site pattern with `spec_source=` keyword argument and `hasattr` guard.

### RN-3: Execution order validation -- injection before gate is confirmed correct

**Verified**: The proposal's injection point (inside `roadmap_run_step()` at line 258, before the function returns `StepResult` with `StepStatus.PASS` at line 261) is correct. Gate checks run AFTER `roadmap_run_step()` returns, in `execute_pipeline._execute_step_with_retry()` at line 210 of `pipeline/executor.py`. Therefore:

1. `roadmap_run_step()` runs the subprocess, sanitizes output, injects fields, returns PASS
2. `_execute_step_with_retry()` receives the result, then calls `gate_passed()` on the output file

Adding `spec_source`, `generated`, and `generator` to `TEST_STRATEGY_GATE.required_frontmatter_fields` will NOT cause gate failures, because the fields are injected before the gate runs.

### RN-4: All line number references verified accurate

- `_inject_pipeline_diagnostics()`: lines 123-157 -- confirmed
- `roadmap_run_step()`: line 160 -- confirmed
- Extract injection block: lines 256-258 -- confirmed
- `RoadmapConfig.spec_file`: line 94 of `models.py` -- confirmed

## Validation Result

**PASS** -- The proposal is structurally sound. The core architectural decisions (executor-injected provenance, injection point after sanitize/before gate return, gate field additions) are all correct and verified against the actual source code. The four issues identified above (RN-1 through RN-4) are minor: one factual inaccuracy about atomic writes, one cosmetic signature mismatch, and two confirmations of correctness. All corrections have been applied inline.
