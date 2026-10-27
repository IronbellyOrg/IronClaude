# ISS-012 Refactoring Proposals

**Issue**: Convergence loop vs linear pipeline tension undocumented. FR-7 adds convergence as a "new phase" but the pipeline is single-pass (steps 1-9). Convergence needs up to 3 runs within step 8 (`spec-fidelity`), not a new pipeline phase.

**Source**: Compatibility Report Section 7a (Architectural Tensions)

**Severity**: MEDIUM (omission-type)

**Related Issues**:
- ISS-001 (CRITICAL): FR-7 greenfield language — already has proposals in `critical/ISS-001-proposals.md`
- ISS-010 (HIGH): Remediation ownership within convergence loop — not yet resolved, overlaps with this issue
- ISS-013 (MEDIUM): Step ordering when convergence replaces spec-fidelity gate — adjacent concern

---

## Problem Analysis

The spec (FR-7) describes convergence as if it is a standalone phase that sits alongside the existing pipeline. In reality:

1. **The pipeline is single-pass**: `_build_steps()` in `executor.py:420-541` constructs a linear list of 9 `Step` objects. `execute_pipeline()` iterates them sequentially.

2. **Step 8 is `spec-fidelity`**: A single `Step(id="spec-fidelity", ...)` at `executor.py:516-525`. When `convergence_enabled=true`, its gate is set to `None` (bypass), but it still runs exactly once as a Claude subprocess.

3. **Convergence needs multiple runs**: FR-7 specifies up to 3 runs (catch, verify, backup) with remediation between runs. This loop cannot happen by re-running the pipeline — it must happen within the step-8 execution boundary.

4. **Precedent exists**: The `wiring-verification` step (step 9, `executor.py:244-259`) already demonstrates the pattern of bypassing the Claude subprocess and running custom Python logic directly when `step.id == "wiring-verification"`. Convergence should use the same pattern.

5. **The spec never says HOW convergence integrates**: FR-7 describes what convergence evaluates and its pass/fail criteria, but never specifies where in the pipeline it runs or how it replaces the existing step-8 behavior.

---

## Proposal #1: Add "Pipeline Integration" Subsection to FR-7 (RECOMMENDED)

**Rationale**: The most targeted fix. Adds exactly the missing information — how convergence integrates with the existing pipeline — without rewriting FR-7's functional description, which is already correct. This is an omission-type issue; the fix is additive text.

### Spec Text to Add

**File**: `deterministic-fidelity-gate-requirements.md`

**Insert after** the Gate Authority Model paragraph (after line 365, before the Acceptance Criteria) — between the end of "The two authorities never coexist in the same execution mode." and the start of "**Acceptance Criteria**":

```markdown
**Pipeline Integration**: Convergence does NOT add a new pipeline phase.
In convergence mode, the existing step-8 (`spec-fidelity`) execution is
replaced with a self-contained convergence loop that runs up to 3 internal
iterations within the step-8 boundary. The step executor detects
`convergence_enabled=true` and delegates to
`execute_fidelity_with_convergence()` instead of spawning a Claude
subprocess. This follows the same bypass pattern used by step-9
(`wiring-verification`) at `executor.py:244-259`.

Each internal iteration within the convergence loop:
1. Runs structural checkers (FR-1) + semantic layer (FR-4) on current inputs
2. Updates the deviation registry (FR-6) with new/resolved findings
3. If pass (0 active HIGHs): mark step-8 PASS, proceed to step-9
4. If regression detected: trigger FR-8 parallel validation (counts as one iteration)
5. If fail + budget remaining: run edit-only remediation (FR-9) on the roadmap, then iterate
6. If fail + budget exhausted: mark step-8 FAIL, halt pipeline

The convergence loop is invisible to the outer pipeline executor —
step-8 returns a single `StepResult` regardless of how many internal
iterations occurred. The `ConvergenceResult` dataclass captures
internal iteration details for diagnostic reporting.
```

### Also Add One Acceptance Criterion

Append to the existing FR-7 acceptance criteria list:

```markdown
- [ ] Convergence loop runs within the step-8 boundary, not as a separate pipeline phase
- [ ] Step executor delegates to `execute_fidelity_with_convergence()` when `convergence_enabled=true` (same bypass pattern as wiring-verification)
- [ ] Each convergence iteration includes: checkers + semantic layer + registry update + remediation (if needed)
- [ ] Step-8 returns a single `StepResult` to the outer pipeline regardless of internal iteration count
```

### Files Affected
- `deterministic-fidelity-gate-requirements.md` (FR-7: new subsection + 4 new acceptance criteria)

### Risk: **LOW**
Purely additive. No existing text changes. The new ACs are testable and specific. The pipeline integration description is consistent with both the existing code (`executor.py` step bypass pattern) and the existing FR-7 functional description.

### Requires Code Changes: **No**
The code pattern already exists (wiring-verification bypass). The new spec text documents the intended integration point for the `execute_fidelity_with_convergence()` function that ISS-001 proposals already acknowledge must be built.

### Cross-Issue Interactions
- **ISS-001**: Proposals #2 and #5 in `critical/ISS-001-proposals.md` mention `execute_fidelity_with_convergence()` but do not specify where in the pipeline it runs. This proposal fills that gap.
- **ISS-010**: The loop description (step 5: "run edit-only remediation, then iterate") explicitly places remediation within the convergence loop, partially resolving ISS-010's concern about remediation ownership.
- **ISS-013**: The step ordering question (what happens after convergence replaces spec-fidelity) is answered: step-9 runs after step-8 returns, same as before.

---

## Proposal #2: Rewrite FR-7 Description to Frame Convergence as Step-8 Modifier

**Rationale**: Rather than adding a subsection, modify the FR-7 description paragraph itself to make the pipeline relationship explicit from the first sentence. More disruptive but eliminates the ambiguity at its source.

### Spec Text Change

**File**: `deterministic-fidelity-gate-requirements.md`, lines 337-343

**Before**:
```markdown
**Description**: The fidelity gate evaluates convergence based on registry
state with these criteria:
- **Pass**: Zero HIGH findings in registry (all FIXED or SKIPPED) — includes both structural AND semantic HIGHs
- **Monotonic progress**: Each run must have ≤ **structural** HIGHs than previous run. Semantic HIGH fluctuations are logged as warnings but do NOT constitute regression.
- **Hard budget**: Maximum 3 runs (catch → verify → backup)
- **Regression detection**: If run N+1 has MORE **structural** HIGHs than run N, trigger parallel validation (see FR-8)
```

**After**:
```markdown
**Description**: In convergence mode, step-8 (`spec-fidelity`) of the
pipeline is replaced by a self-contained convergence loop that runs up to
3 internal iterations within the step-8 execution boundary. The step
executor delegates to `execute_fidelity_with_convergence()` instead of
spawning a Claude subprocess (same bypass pattern as step-9's
wiring-verification). The convergence loop evaluates registry state with
these criteria:
- **Pass**: Zero HIGH findings in registry (all FIXED or SKIPPED) — includes both structural AND semantic HIGHs
- **Monotonic progress**: Each run must have ≤ **structural** HIGHs than previous run. Semantic HIGH fluctuations are logged as warnings but do NOT constitute regression.
- **Hard budget**: Maximum 3 runs (catch → verify → backup)
- **Regression detection**: If run N+1 has MORE **structural** HIGHs than run N, trigger parallel validation (see FR-8)

Each iteration: run checkers (FR-1) + semantic layer (FR-4) → update
registry (FR-6) → if fail + budget remaining, remediate (FR-9) and
iterate. The outer pipeline sees a single `StepResult` from step-8.
```

### Also Add Acceptance Criteria (same as Proposal #1)

```markdown
- [ ] Convergence loop runs within the step-8 boundary, not as a separate pipeline phase
- [ ] Step executor delegates to `execute_fidelity_with_convergence()` when `convergence_enabled=true` (same bypass pattern as wiring-verification)
- [ ] Each convergence iteration includes: checkers + semantic layer + registry update + remediation (if needed)
- [ ] Step-8 returns a single `StepResult` to the outer pipeline regardless of internal iteration count
```

### Files Affected
- `deterministic-fidelity-gate-requirements.md` (FR-7: Description rewrite + 4 new acceptance criteria)

### Risk: **MEDIUM**
Modifies existing description text rather than adding alongside it. If combined with ISS-001 proposals (which also modify FR-7 description text), the edits must be reconciled. However, the functional criteria (bullet points) are unchanged.

### Requires Code Changes: **No**

### Cross-Issue Interactions
- **ISS-001**: If ISS-001 Proposal #1 or #5 is also adopted, the description changes must be merged. Specifically, ISS-001 adds "extends existing convergence engine" language to the same paragraph this proposal rewrites. Both changes are compatible but must be applied together.

---

## Proposal #3: Add Convergence Integration to Appendix A Diagram + FR-7 Cross-Reference

**Rationale**: The Appendix A architecture diagrams (lines 576-611) are the most natural place to document pipeline flow. Add a convergence detail expansion to the "Proposed (to-be)" diagram, and add a one-line cross-reference from FR-7 to the appendix.

### Spec Text Change

**File**: `deterministic-fidelity-gate-requirements.md`

**Change #1** — FR-7 description (line 337-338), add one sentence:

**Before**:
```markdown
**Description**: The fidelity gate evaluates convergence based on registry
state with these criteria:
```

**After**:
```markdown
**Description**: The fidelity gate evaluates convergence based on registry
state within the step-8 execution boundary (see Appendix A, Convergence
Detail) with these criteria:
```

**Change #2** — Appendix A, after the "Proposed (to-be)" diagram (after line 599), insert:

```markdown
### Convergence Detail (Step-8 Internal Flow)
```
When `convergence_enabled=true`, step-8 bypasses the Claude subprocess
and delegates to `execute_fidelity_with_convergence()`. Internally:
```
Step-8 entry (single StepResult to outer pipeline)
  └─ Iteration 1 (catch):
       Structural Checkers (parallel) + Semantic Layer
       → Registry update → Pass? → exit step-8 as PASS
       → Fail? → Remediate (FR-9) → continue
  └─ Iteration 2 (verify):
       Re-run checkers on remediated roadmap
       → Registry update → Regression? → FR-8 parallel validation
       → Pass? → exit step-8 as PASS
       → Fail? → Remediate → continue
  └─ Iteration 3 (backup):
       Final check
       → Pass? → exit step-8 as PASS
       → Fail? → exit step-8 as FAIL (halt pipeline)
```
This is NOT a new pipeline phase. Steps 1-7 and step-9 are unaffected.
The outer `execute_pipeline()` sees step-8 return a single `StepResult`.
```

### Files Affected
- `deterministic-fidelity-gate-requirements.md` (FR-7: one-sentence addition; Appendix A: new subsection)

### Risk: **LOW**
One sentence change in FR-7 body. Appendix addition is purely informational. The diagram makes the convergence-within-step-8 pattern visually unambiguous.

### Requires Code Changes: **No**

---

## Ranking Summary

| Rank | Proposal | Disruption | Correctness | Completeness | Recommendation |
|------|----------|-----------|-------------|--------------|----------------|
| 1 | #1 (Pipeline Integration subsection) | Low | High | Highest | Best standalone fix. Adds all missing information without touching existing text. |
| 2 | #3 (Appendix A diagram + cross-ref) | Low | High | High | Best visual explanation. Good supplement to #1. |
| 3 | #2 (Description rewrite) | Medium | High | High | Best if FR-7 description is already being rewritten for ISS-001. |

**Recommended approach**: **#1 + #3** — the Pipeline Integration subsection provides the normative spec text, and the Appendix A diagram provides a visual reference. Together they fully resolve the "convergence loop vs linear pipeline tension" without modifying any existing FR-7 text.

**If ISS-001 Proposal #5 (full FR-7 rewrite) is adopted**: Use **#2** instead — fold the pipeline integration language directly into the rewritten description, since the entire section is already being replaced.

---

## Relationship to ISS-010 (HIGH: Remediation Ownership)

ISS-012 partially overlaps with ISS-010. Both proposals #1 and #2 explicitly place remediation (FR-9) within the convergence loop iterations. This addresses ISS-010's concern that remediation is currently post-pipeline but needs to run between convergence runs. However, ISS-010 also involves resolving the tension with `_check_remediation_budget()` and `_print_terminal_halt()` which assume external remediation — those functions need separate attention when ISS-010 is resolved.
