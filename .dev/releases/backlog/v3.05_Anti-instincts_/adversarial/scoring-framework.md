# Custom Scoring Framework — Anti-Instincts Adversarial Debate

**Replaces**: Default 30-criterion binary rubric (6 dimensions × 5 criteria)
**Source**: User-provided in invocation arguments

## 4-Dimension Scoring Matrix

### D1: Efficacy (weight 0.35)

How reliably would this catch the specific cli-portify bug class? Would it catch similar-but-different future bugs? What is the false negative rate?

**Scoring guide:**
- 9-10: Catches the cli-portify bug deterministically with <5% false negative rate; catches analogous bugs in other pipeline stages
- 7-8: Catches the cli-portify bug with high probability (>85%); catches most analogous bugs
- 5-6: Catches the cli-portify bug sometimes (50-85%); some analogous bugs slip through
- 3-4: Unreliable detection (<50%); narrow class coverage
- 1-2: Would not have caught the cli-portify bug; token gesture

### D2: Generalizability (weight 0.25)

Does this only catch the one bug pattern that motivated it, or does it protect against a broader class of LLM-generated roadmap failures? How well does it transfer to other pipeline stages (tasklist, sprint)?

**Scoring guide:**
- 9-10: Applies to any pipeline stage with spec-to-artifact fidelity requirements; catches entirely new failure classes
- 7-8: Applies to 2+ pipeline stages; catches several related failure classes
- 5-6: Primarily roadmap-specific; catches the motivated failure class only
- 3-4: Narrow applicability; specific to one spec style or naming convention
- 1-2: Works only for the exact cli-portify case

### D3: Implementation Complexity (weight 0.20)

How much code is required? How many files change? Does it integrate cleanly with existing gate infrastructure (MERGE_GATE, SPEC_FIDELITY_GATE) or require new pipeline steps? Prefer solutions that hook into existing patterns.

**Scoring guide (INVERTED — lower complexity = higher score):**
- 9-10: <100 LOC, 1-2 files changed, hooks into existing SemanticCheck pattern
- 7-8: 100-200 LOC, 2-3 files changed, uses existing gate patterns
- 5-6: 200-400 LOC, 3-5 files changed, needs minor pipeline model changes
- 3-4: 400+ LOC, 5+ files changed, requires new pipeline step types or state management
- 1-2: Major architectural change; new abstractions, new pipeline phases, cross-cutting changes

### D4: Determinism (weight 0.20)

Is the check fully deterministic (pure Python, no LLM involvement), semi-deterministic (LLM-assisted but with programmatic floor), or LLM-dependent? Higher determinism = higher score.

**Scoring guide:**
- 9-10: Pure Python, zero LLM calls, identical results on same input
- 7-8: Primarily deterministic with optional LLM augmentation (LLM failure is safe)
- 5-6: Hybrid — deterministic floor with LLM layer that adds value but is not required
- 3-4: Semi-deterministic — LLM generates structured output consumed by deterministic gate
- 1-2: Fully LLM-dependent; shares the same blindspots being mitigated

## Composite Score Formula

```
final_score = (D1 × 0.35) + (D2 × 0.25) + (D3 × 0.20) + (D4 × 0.20)
```

Range: 1.0 – 10.0

## Merge Directive

The top 2 scoring proposals become co-bases for the merged "Anti-Instincts Gate" specification. Complementary elements from the remaining 3 are cherry-picked based on:
1. Do they address a dimension where the co-bases score low?
2. Are they implementable as part of the same pipeline step?
3. Do they conflict with any co-base mechanism?
