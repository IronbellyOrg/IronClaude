---
phase: 6
title: "Integration & Wiring"
tasks: 4
depends_on: [5]
parallelizable: false
---

# Phase 6: Integration & Wiring

Sequential execution. These tasks wire the new orchestration into the existing pipeline.

---

### T25: Wire convergence branch into roadmap_run_step() (FR-7)

**Tier**: moderate
**File**: src/superclaude/cli/roadmap/executor.py
**FR**: FR-7

**Action**: Add convergence mode branch to the spec-fidelity step execution:

1. In `roadmap_run_step()`, when step is `spec-fidelity` and `config.convergence_enabled`:
   - Instead of running ClaudeProcess for spec-fidelity, call `execute_fidelity_with_convergence()` (T22)
   - The convergence engine handles all runs internally
   - Write `spec-fidelity.md` as human-readable summary (existing behavior) but do NOT gate on it
2. Existing behavior when `convergence_enabled=False` is byte-identical to pre-v3.05

**Integration point**: executor.py already has `gate=None if config.convergence_enabled else SPEC_FIDELITY_GATE` at line 521. The convergence branch needs to also replace the ClaudeProcess call at the same step.

**Acceptance criteria**:
- [ ] Convergence mode calls execute_fidelity_with_convergence() instead of ClaudeProcess
- [ ] spec-fidelity.md still written as summary
- [ ] Legacy mode behavior unchanged (NFR-7)
- [ ] No changes to upstream steps 1-7

---

### T26: Add --convergence-enabled CLI flag

**Tier**: simple
**File**: src/superclaude/cli/roadmap/commands.py
**FR**: FR-7

**Action**: Add Click flag following existing `--allow-regeneration` pattern (commands.py:89-94):

```python
@click.option("--convergence-enabled", is_flag=True, default=False,
              help="Enable deterministic fidelity convergence engine (v3.05)")
```

Wire into RoadmapConfig construction.

**Acceptance criteria**:
- [ ] Flag exists as is_flag=True with default False
- [ ] Passed through to RoadmapConfig.convergence_enabled
- [ ] Without flag: legacy behavior preserved

---

### T27: End-to-end smoke test

**Tier**: moderate
**File**: New test file or script
**FR**: All

**Action**: Run the full convergence pipeline on the v3.05 spec as an integration test:

1. `superclaude roadmap run deterministic-fidelity-gate-requirements.md --convergence-enabled`
2. Verify: structural checkers produce findings
3. Verify: semantic layer handles residual checks
4. Verify: deviation registry is populated
5. Verify: convergence gate evaluates registry
6. Verify: remediation produces patches (if needed)
7. Verify: all artifacts written to output directory

This is a real pipeline execution, not a unit test.

**Acceptance criteria**:
- [ ] Pipeline completes without error (PASS or HALT with diagnostic)
- [ ] All expected artifacts produced
- [ ] Registry file is valid JSON/YAML
- [ ] No leaked temp directories

---

### T28: Document wiring step interaction

**Tier**: simple
**File**: deterministic-fidelity-gate-requirements.md or inline code comments
**FR**: §7d concern

**Action**: Document that when convergence_enabled=true:
- spec-fidelity step runs convergence engine (not SPEC_FIDELITY_GATE)
- wiring-verification step still runs normally (no dependency on spec-fidelity output)
- Step ordering is: spec-fidelity (convergence) → wiring-verification (unchanged)

**Acceptance criteria**:
- [ ] Interaction documented in spec or code
- [ ] No ambiguity about step ordering in convergence mode
