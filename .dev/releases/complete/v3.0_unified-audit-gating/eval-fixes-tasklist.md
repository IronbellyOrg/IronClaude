---
title: "v3.0 Eval Fixes — Implementation Tasklist"
date: 2026-03-19
tasks: 4
estimated_files_changed: 4
branch: v3.0-AuditGates
validation: "uv run superclaude roadmap run .dev/releases/current/v3.0_unified-audit-gating/eval-spec.md --output /tmp/eval-fix-verify/ --dry-run"
---

# v3.0 Eval Fixes — Implementation Tasklist

## Background

The v3.0 eval suite ran 4 pipeline executions. Both local runs (v3.0 branch) failed at the spec-fidelity gate because the LLM-generated roadmap contained fabricated requirement IDs (FR-001..FR-010) that don't match the spec's IDs (FR-EVAL-001.1..FR-EVAL-001.6). Root cause analysis traced this to the extraction prompt explicitly instructing ID renumbering, plus 3 secondary issues.

## Prerequisites

- Branch: `v3.0-AuditGates` (current)
- All changes are in `src/superclaude/` — run `make sync-dev` after all tasks complete
- Run `make test` to verify no regressions

---

## Task 1: Fix extraction prompt ID fabrication

**File**: `src/superclaude/cli/roadmap/prompts.py`
**Function**: `build_extract_prompt()` (starts at line 58)
**Root cause**: Lines 95-100 explicitly instruct the LLM to assign new FR-NNN / NFR-NNN IDs, destroying the spec's original identifiers. The instruction also says "extract every functional requirement, even implicit ones" which causes count inflation (6 FRs decomposed into 10).

### Exact change

Find this text on lines 95-100:

```python
        "## Functional Requirements\n"
        "Numbered list with FR-NNN IDs (e.g. FR-001, FR-002). "
        "Extract every functional requirement, even implicit ones.\n\n"
        "## Non-Functional Requirements\n"
        "Numbered list with NFR-NNN IDs (e.g. NFR-001, NFR-002). "
        "Include performance, security, scalability, maintainability.\n\n"
```

Replace with:

```python
        "## Functional Requirements\n"
        "Use the spec's exact requirement identifiers verbatim as primary IDs. "
        "Do NOT create a new numbering scheme (e.g., do NOT renumber as FR-001, FR-002). "
        "If a spec uses FR-EVAL-001.1, use FR-EVAL-001.1. "
        "If a requirement needs sub-decomposition, use suffixes on the original ID "
        "(e.g., FR-EVAL-001.1a, FR-EVAL-001.1b). "
        "If the spec has no requirement IDs, then use FR-NNN as a fallback. "
        "The functional_requirements frontmatter count must equal the number of "
        "top-level requirements in the spec, not sub-decompositions.\n\n"
        "## Non-Functional Requirements\n"
        "Use the spec's exact NFR identifiers verbatim. Do NOT renumber. "
        "If the spec has no NFR IDs, use NFR-NNN as a fallback. "
        "Include performance, security, scalability, maintainability.\n\n"
```

### Why this works
- The extraction is the first pipeline step that reads the spec. If it preserves original IDs, all downstream steps (generate, diff, debate, score, merge) propagate them correctly.
- The spec-fidelity step compares the final roadmap against the original spec. Matching IDs eliminates the 3 HIGH deviations (DEV-001: fabricated FR IDs, DEV-002: fabricated OQ IDs, DEV-003: resume/append contradiction based on fabricated OQ-004).
- The `functional_requirements` count instruction prevents inflation (10 → 6).
- The "fallback to FR-NNN" clause handles specs that genuinely have no IDs.

### Verification
After this change, run:
```bash
uv run superclaude roadmap run .dev/releases/current/v3.0_unified-audit-gating/eval-spec.md \
  --output /tmp/eval-fix-task1/ 2>&1 | head -5
```
Check `/tmp/eval-fix-task1/extraction.md` — the Functional Requirements section should use `FR-EVAL-001.x` IDs, not `FR-001` IDs. The frontmatter should show `functional_requirements: 6` (matching the spec's 6 FRs).

---

## Task 2: Add defense-in-depth to generate prompt

**File**: `src/superclaude/cli/roadmap/prompts.py`
**Function**: `build_generate_prompt()` (starts at line 130)
**Purpose**: Even with a fixed extraction, the generate LLM could still renumber IDs. This adds a guardrail.

### Exact change

Find this text on line 164:

```python
        "Use numbered and bulleted lists for actionable items. Be specific and concrete."
```

Replace with:

```python
        "Use numbered and bulleted lists for actionable items. Be specific and concrete.\n\n"
        "IMPORTANT: Preserve exact requirement IDs from the extraction document. "
        "Do NOT renumber, relabel, or create new requirement IDs. "
        "If the extraction uses FR-EVAL-001.1, your roadmap must use FR-EVAL-001.1."
```

### Why this works
- The generate step only receives the extraction, never the original spec. If extraction is fixed (Task 1), this instruction tells the generator to preserve whatever IDs the extraction provides.
- Defense-in-depth: even if extraction drifts in some edge case, the generate prompt reinforces ID preservation.

### Verification
After Tasks 1 and 2, check `/tmp/eval-fix-task1/roadmap-opus-architect.md` and `roadmap-haiku-architect.md`. Both should reference `FR-EVAL-001.x` IDs, not `FR-001` IDs.

---

## Task 3: Execute TRAILING-mode steps after pipeline halt

**File**: `src/superclaude/cli/pipeline/executor.py`
**Function**: `execute_pipeline()` (starts at line 55)
**Purpose**: When the pipeline halts (e.g., spec-fidelity FAIL), steps with `GateMode.TRAILING` should still execute because they are designed for advisory/shadow execution.

### Context
- The main loop at lines 87-122 breaks on any non-PASS result
- Wiring-verification is declared with `gate_mode=GateMode.TRAILING` at `roadmap/executor.py:537`
- The `TrailingGateRunner` already exists and handles TRAILING gate evaluation
- But the wiring-verification step itself never EXECUTES if a prior step fails — the break at line 121 skips it entirely
- The issue is that TRAILING refers to how the gate is evaluated (asynchronously), not whether the step runs

### Exact change

Find this code block at lines 121-137:

```python
            if result.status != StepStatus.PASS:
                break

    # Sync point: collect all trailing gate results at end of pipeline
    if _trailing is not None:
        trailing_results = _trailing.wait_for_pending(
            timeout=max(30.0, float(config.grace_period))
        )
        for tr in trailing_results:
            if not tr.passed:
                _log.warning(
                    "Trailing gate failed for step '%s': %s",
                    tr.step_id,
                    tr.failure_reason,
                )

    return all_results
```

Replace with:

```python
            if result.status != StepStatus.PASS:
                break

    # Deferred execution: run any not-yet-reached TRAILING-mode steps.
    # These steps are designed for advisory/shadow execution and should
    # run even when the main pipeline halts (e.g., wiring-verification).
    executed_ids = {r.step.id for r in all_results}
    remaining_steps = []
    for entry in steps:
        if isinstance(entry, list):
            for s in entry:
                if s.id not in executed_ids and s.gate_mode == GateMode.TRAILING:
                    remaining_steps.append(s)
        else:
            if entry.id not in executed_ids and entry.gate_mode == GateMode.TRAILING:
                remaining_steps.append(entry)

    for deferred_step in remaining_steps:
        if cancel_check():
            break
        _log.info(
            "Executing deferred TRAILING step '%s' after pipeline halt",
            deferred_step.id,
        )
        result = run_step(deferred_step, config, cancel_check)
        result = StepResult(
            step=result.step,
            status=result.status,
            attempt=1,
            gate_failure_reason=result.gate_failure_reason,
            started_at=result.started_at,
            finished_at=result.finished_at,
        )
        all_results.append(result)
        on_step_complete(deferred_step, result)
        on_state_update(_build_state(all_results))

    # Sync point: collect all trailing gate results at end of pipeline
    if _trailing is not None:
        trailing_results = _trailing.wait_for_pending(
            timeout=max(30.0, float(config.grace_period))
        )
        for tr in trailing_results:
            if not tr.passed:
                _log.warning(
                    "Trailing gate failed for step '%s': %s",
                    tr.step_id,
                    tr.failure_reason,
                )

    return all_results
```

### Why this works
- The wiring-verification step at `roadmap/executor.py:244-259` runs `run_wiring_analysis()` directly against source code — it does NOT depend on upstream pipeline artifacts being valid. It reads the codebase, not the roadmap.
- The `GateMode.TRAILING` contract already implies advisory/non-blocking semantics. This change makes the executor honor that contract for step execution, not just gate evaluation.
- The deferred step results are appended to `all_results` and saved to state, so they appear in `.roadmap-state.json` for scoring.
- Only TRAILING-mode steps are deferred. BLOCKING steps (remediate, certify) remain blocked as designed.

### Verification
After Tasks 1-3, run:
```bash
uv run superclaude roadmap run .dev/releases/current/v3.0_unified-audit-gating/eval-spec.md \
  --output /tmp/eval-fix-task3/
```
Even if spec-fidelity fails (possible with LLM variance), check that `wiring-verification.md` was still produced in the output directory. The pipeline log should show: `Executing deferred TRAILING step 'wiring-verification' after pipeline halt`.

---

## Task 4: Redefine R-8 metric to use artifact inspection

**File 1**: `.dev/releases/current/v3.0_unified-audit-gating/scoring-framework.md`
**File 2**: `scripts/eval_3.py`
**Purpose**: R-8 currently checks stdout for "trailing"/"shadow" strings that the executor never emits. Redefine to check authoritative sources.

### Change in scoring-framework.md

Find this row in the Impact 3 metrics table (Section 3.3):

```
| R-7 | GateMode.TRAILING wired in _build_steps() | code inspection | binary | Pipeline step is correctly configured |
| R-8 | Pipeline output references trailing/shadow | stdout/stderr | binary | Runtime execution path is correct |
```

Replace R-8 with:

```
| R-7 | GateMode.TRAILING wired in _build_steps() | code inspection | binary | Pipeline step is correctly configured |
| R-8a | wiring-verification.md contains rollout_mode field | artifact frontmatter | binary | Runtime artifact records mode metadata |
| R-8b | _build_steps() configures wiring step with GateMode.TRAILING | code inspection / dry-run | binary | Step scheduling uses correct gate mode |
```

### Change in eval_3.py

Find this code at lines 222-236 in `phase_b_pipeline_trailing_mode()`:

```python
    # 2. Assert: check stderr/stdout for TRAILING mode indicators
    combined_output = proc.stdout + proc.stderr
    trailing_indicators = [
        "TRAILING", "trailing", "shadow", "wiring-verification",
    ]
    has_trailing_ref = any(ind in combined_output for ind in trailing_indicators)
    result.assertions.append(
        assert_check(
            "trailing_mode_referenced",
            has_trailing_ref,
            "Pipeline output references trailing/shadow mode"
            if has_trailing_ref
            else "No trailing mode references in pipeline output",
        )
    )
```

Replace with:

```python
    # 2. Assert (R-8a): wiring-verification.md contains rollout_mode in frontmatter
    wiring_fm = {}
    if wiring_report.exists():
        wiring_fm = parse_frontmatter(wiring_report)
    has_rollout_mode = wiring_fm.get("rollout_mode") in ("shadow", "soft", "full")
    result.assertions.append(
        assert_check(
            "r8a_artifact_rollout_mode",
            has_rollout_mode,
            f"rollout_mode={wiring_fm.get('rollout_mode')}"
            if has_rollout_mode
            else "wiring-verification.md missing or lacks rollout_mode",
        )
    )
```

### Why this works
- R-8a checks the authoritative artifact (`wiring-verification.md` frontmatter) where `rollout_mode` is deterministically written by `emit_report()` in `wiring_gate.py`.
- R-8b is already checked at lines 238-285 of eval_3.py (the `_build_steps()` code inspection). No change needed for R-8b.
- This eliminates the fragile stdout text parsing that could never work (the executor doesn't emit those strings).

### Verification
Run `uv run pytest scripts/eval_3.py -v` (if eval scripts are pytest-compatible) or run:
```bash
uv run python scripts/eval_3.py --branch local
```
The `r8a_artifact_rollout_mode` assertion should PASS if wiring-verification.md was produced (depends on Task 3).

---

## Post-Implementation Checklist

1. Run `make sync-dev` to sync changes from `src/superclaude/` to `.claude/`
2. Run `make verify-sync` to confirm sync
3. Run `make test` to verify no regressions
4. Run a full pipeline test:
   ```bash
   uv run superclaude roadmap run \
     .dev/releases/current/v3.0_unified-audit-gating/eval-spec.md \
     --output /tmp/eval-fix-full-test/
   ```
5. Check extraction IDs: `head -30 /tmp/eval-fix-full-test/extraction.md`
   - Should show `FR-EVAL-001.x` IDs, not `FR-001`
   - Should show `functional_requirements: 6`
6. Check spec-fidelity: `head -10 /tmp/eval-fix-full-test/spec-fidelity.md`
   - `high_severity_count` should be 0 (or at most 1 if LLM finds a genuine deviation)
7. Check wiring-verification exists: `ls -la /tmp/eval-fix-full-test/wiring-verification.md`
   - Should exist even if spec-fidelity failed (Task 3 deferred execution)
8. Check wiring-verification frontmatter: `head -20 /tmp/eval-fix-full-test/wiring-verification.md`
   - Should contain `rollout_mode: soft`
