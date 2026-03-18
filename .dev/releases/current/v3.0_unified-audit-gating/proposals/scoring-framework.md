# Proposal Scoring Framework — Unified Audit Gating v1.2.1

**Date**: 2026-03-17
**Purpose**: Standardized comparative evaluation of the five independent gating proposals.
**Reference incident**: cli-portify executor no-op bug — shipped across v2.24, v2.24.1, v2.25 with
all gates reporting SUCCESS because the pipeline returned `(exit_code=0, stdout="", timed_out=False)`
from a no-op fallback. Gate infrastructure validated document structure; no gate asked whether code
components were wired together.

---

## Scoring Axes

Each proposal is scored on six axes. **Higher is always better** — two axes are inverted so that the
worst outcome on each axis is 1, the best is 10.

---

### Axis 1 — Catch Rate (weight 25%)

**Definition**: How likely would this proposal have caught the cli-portify no-op bug **specifically**?

| Score | Meaning |
|-------|---------|
| 10 | Would have blocked the pipeline deterministically before any release |
| 8–9 | Would have caught it in ≥90% of realistic execution paths |
| 6–7 | Would have caught it with high probability given normal workflow adherence |
| 4–5 | Would have flagged a related symptom but not the root cause directly |
| 2–3 | Tangentially related; might detect the symptom only in edge cases |
| 1 | Would not have caught this specific bug class |

**Evidence anchor**: The bug's defining property is that `_execute_step()` returns `(0, "", False)`
for every step because `step_runner` is never passed to `PortifyExecutor`. A gate scores 10 on this
axis only if it would produce a deterministic FAIL output when this condition exists.

---

### Axis 2 — Generalizability (weight 25%)

**Definition**: How many other bug classes does this catch beyond the cli-portify no-op incident?

| Score | Meaning |
|-------|---------|
| 10 | Catches an entire category of integration bugs (unwired components, silent stubs, phantom success) |
| 8–9 | Catches 3+ other named bug classes with evidence from codebase |
| 6–7 | Catches 2 other named bug classes |
| 4–5 | Catches 1 other named bug class or prevents a class of future regressions |
| 2–3 | Applicable only to cli-portify-style patterns; low transfer to other modules |
| 1 | Single-bug fix with no generalizable detection mechanism |

**Evidence anchor**: The forensic report identifies three other "defined but not wired" instances:
`DEVIATION_ANALYSIS_GATE` (unwired from `_build_steps()`), `SprintGatePolicy` (stub in
`sprint/executor.py:47-90`), and `TrailingGateRunner` (never called from `execute_sprint()`).
A proposal scoring 8+ must address at least two of these.

---

### Axis 3 — Implementation Complexity (weight 20%, inverted)

**Definition**: How complex is the implementation? Score 10 = simplest (least complexity).

| Score | Meaning |
|-------|---------|
| 10 | Single file change; no new abstractions; < 50 lines of new code |
| 8–9 | 2–3 file changes; minimal new abstractions; < 200 lines |
| 6–7 | 4–6 file changes; 1–2 new abstractions; < 500 lines |
| 4–5 | 7–10 file changes; 3–5 new abstractions; moderate test coverage needed |
| 2–3 | Cross-cutting infrastructure change; new subsystem; significant test coverage |
| 1 | Requires new toolchain, external service, or major architectural restructure |

**Calibration reference**: Adding `validate_portify_config()` call in `commands.py` (Defect 2 fix)
scores 10. The full audit gating v1.2.1 phase plan (4 phases, 9+ files) scores approximately 2.

---

### Axis 4 — False Positive Risk (weight 15%, inverted)

**Definition**: How likely is this proposal to block legitimate work? Score 10 = lowest FP risk.

| Score | Meaning |
|-------|---------|
| 10 | Zero known FP scenarios; gate fires only on objectively wrong conditions |
| 8–9 | Rare FP scenarios possible; all escapable via documented override path |
| 6–7 | Occasional FP expected (5–10% of runs in normal operation); override available |
| 4–5 | Moderate FP rate (10–20%); requires tuning or threshold calibration |
| 2–3 | High FP rate; likely to generate developer friction in normal workflows |
| 1 | Would block majority of legitimate runs without significant tuning |

**Key FP scenarios to consider**:
- Intentional stub implementations (TDD red-phase, mock boundaries in tests)
- No-op steps that are legitimately optional (dry-run mode, skip flags)
- New step types that don't yet have dispatch implementations during scaffolding phases
- LLM-generated fidelity checks that hallucinate missing components

---

### Axis 5 — Integration Fit (weight 15%)

**Definition**: How well does this integrate with existing gate infrastructure?

| Score | Meaning |
|-------|---------|
| 10 | Directly extends existing gate pattern (`GateCriteria`, `ALL_GATES`); no new infrastructure |
| 8–9 | Reuses existing patterns with minor extensions; integrates with pipeline executor cleanly |
| 6–7 | Requires moderate new wiring but fits conceptually; uses adjacent infrastructure |
| 4–5 | Requires new hook points in executor but doesn't conflict with existing gates |
| 2–3 | Parallel gate system that must be reconciled with existing pipeline gate infrastructure |
| 1 | Standalone system that replaces or bypasses existing gate infrastructure |

**Key integration assets**:
- `pipeline/gates.py:20-69` — `GateCriteria` with `mode`, `semantic_checks`, two-tier dispatch
- `roadmap/gates.py:760-774` — `ALL_GATES` registry; add a gate entry to get blocking semantics free
- `pipeline/trailing_gate.py` — `TrailingGateRunner`; task-scope non-blocking evaluation loop
- `sprint/executor.py:47-90` — `SprintGatePolicy` stub; integration hook candidates at lines 668–787
- `audit/dead_code.py` — existing 3-tier dependency graph; potential reuse for reachability checks

---

## Composite Score Formula

```
Composite = (Catch_Rate × 0.25)
          + (Generalizability × 0.25)
          + (Complexity × 0.20)
          + (FP_Risk × 0.15)
          + (Integration_Fit × 0.15)
```

**Score bands**:

| Band | Range | Recommendation |
|------|-------|----------------|
| Tier 1 — Implement Immediately | 7.5–10 | High ROI; low risk; catches incident class |
| Tier 2 — Implement in Phase 2 | 6.0–7.4 | Good value; moderate complexity; schedule in next phase |
| Tier 3 — Consider After Phase 2 | 4.5–5.9 | Useful but complex or narrow; defer until core system stable |
| Tier 4 — Reconsider | < 4.5 | Low catch rate or high FP risk; needs redesign before adoption |

---

## Scoring Rubric Examples (Calibration)

### Calibration A — "Add `validate_portify_config()` call"
The Defect 2 fix (call `validate_portify_config()` from `commands.py`):
- Catch Rate: 3 (catches Defect 2 / config validation failure, not the no-op Defect 1)
- Generalizability: 2 (only config validation; narrow)
- Complexity: 10 (single line change)
- FP Risk: 10 (no false positives; only fires on actually invalid configs)
- Integration Fit: 10 (no infrastructure change)
- **Composite**: (3×0.25)+(2×0.25)+(10×0.20)+(10×0.15)+(10×0.15) = 0.75+0.5+2+1.5+1.5 = **6.25**

### Calibration B — "LLM step routing review"
Hypothetical: add a prompt asking Claude to review whether all STEP_REGISTRY entries are wired:
- Catch Rate: 6 (would likely notice the no-op, but LLM could miss it)
- Generalizability: 5 (applicable to other registries but LLM-dependent)
- Complexity: 8 (new prompt + gate check function)
- FP Risk: 4 (LLM may flag intentional stubs as unwired)
- Integration Fit: 7 (fits gate pattern but adds LLM call)
- **Composite**: (6×0.25)+(5×0.25)+(8×0.20)+(4×0.15)+(7×0.15) = 1.5+1.25+1.6+0.6+1.05 = **6.0**

---

## How Debates Should Use This Framework

Each Phase C debate agent must:

1. **State evidence** for each axis score, not just the score. E.g., "Catch Rate = 8 because the
   proposed AST check on `Optional[Callable]` parameters would flag `step_runner=None` at
   `executor.py:393` during static analysis."

2. **Acknowledge the strongest counter-argument** on the axis where the proposal is weakest.

3. **Score ± 2 from preliminary** if additional evidence emerges during debate; justify any shift.

4. **Do not change scoring axis definitions** — the framework is fixed. Debate within it.

5. **Compute composite score** using the exact formula above. No rounding until final composite.

---

## Preliminary Proposal Index

| File | Dimension | Key Question |
|------|-----------|-------------|
| `proposal-01-link3-code-fidelity.md` | Link 3: Tasklist→Code | How does task-level audit verify code satisfies acceptance criteria? |
| `proposal-02-spec-fidelity-hardening.md` | Link 1 hardening | What deterministic cross-references prevent roadmap from dropping spec requirements? |
| `proposal-03-code-integration-gate.md` | Code Integration Gate | How do we detect orphaned implementations and no-op fallbacks statically? |
| `proposal-04-smoke-test-gate.md` | Smoke Test Gate | How do we actually run the pipeline and verify real artifacts? |
| `proposal-05-silent-success-detection.md` | Silent Success | How do we distinguish real success from no-op success? |
