# Fidelity Refactor — Proposal Scoring Framework

**Date**: 2026-03-17
**Purpose**: Standardized scoring framework for evaluating fidelity gate mitigation proposals
**Context**: Produced alongside Phase 1 brainstorm agents; used by Phase 3 adversarial debate agents

---

## Scoring Dimensions

Each proposal is scored on 5 dimensions, each on a 1-10 scale.

### 1. Likelihood to Succeed (Weight: 0.35)

**Question**: Would this gate actually catch the cli-portify no-op bug? Would it catch similar bugs in the future?

| Score | Meaning |
|-------|---------|
| 9-10 | Would definitively catch the cli-portify bug AND similar "defined but not wired" bugs with near-zero false negatives |
| 7-8 | Would likely catch the cli-portify bug and most similar bugs; minor edge cases possible |
| 5-6 | Would catch some instances but has known blind spots; depends on LLM quality or document formatting |
| 3-4 | Might catch the bug under favorable conditions but unreliable; significant dependency on external factors |
| 1-2 | Unlikely to catch the bug; addresses a different failure mode or is too indirect |

**Evidence basis**: Score MUST reference:
- Whether the specific cli-portify failure (spec's three-way dispatch dropped at Spec→Roadmap) would be caught
- Whether the "defined but not wired" pattern class would be caught
- Whether silent no-op fallbacks would be detected
- Number of assumptions required for the gate to fire

### 2. Implementation Complexity (Weight: 0.25)

**Question**: How much effort to implement, test, and deploy? (Inverted: 10=trivial, 1=massive)

| Score | Meaning |
|-------|---------|
| 9-10 | < 50 lines of code; hooks into existing infrastructure; no new dependencies |
| 7-8 | 50-200 lines; minor additions to existing modules; 1-2 new functions |
| 5-6 | 200-500 lines; new module or significant refactor of existing gate; new test fixtures needed |
| 3-4 | 500-1000 lines; new subsystem; requires changes across multiple modules; new infrastructure |
| 1-2 | > 1000 lines; new pipeline stage; requires architectural changes; cross-cutting concerns |

**Evidence basis**: Score MUST reference:
- Estimated lines of production code
- Number of files modified/created
- New dependencies or infrastructure required
- Testing burden (new fixtures, integration tests, mock complexity)

### 3. False Positive Risk (Weight: 0.15)

**Question**: Would this gate block legitimate pipelines? (Inverted: 10=no risk, 1=high risk)

| Score | Meaning |
|-------|---------|
| 9-10 | Only fires on genuine fidelity failures; deterministic checks with clear semantics |
| 7-8 | Rare false positives; easily overridden when they occur; clear error messages |
| 5-6 | Occasional false positives expected; requires tuning thresholds or whitelists |
| 3-4 | Frequent false positives likely; depends on document formatting conventions being followed exactly |
| 1-2 | Will block most pipelines initially; requires extensive tuning before production use |

**Evidence basis**: Score MUST reference:
- Whether the gate uses deterministic or probabilistic checks
- Sensitivity to document formatting variations
- Whether the gate can distinguish intentional omissions from accidental ones
- Override/escape mechanisms available

### 4. Maintainability (Weight: 0.15)

**Question**: Will this gate stay correct as the pipeline evolves? Does it require manual updates?

| Score | Meaning |
|-------|---------|
| 9-10 | Self-maintaining; derives checks from existing document structure; no manual upkeep |
| 7-8 | Low maintenance; updates only needed when ID schema changes; clear update path |
| 5-6 | Moderate maintenance; requires updates when new pipeline stages are added |
| 3-4 | High maintenance; requires manual configuration per release; easy to let drift |
| 1-2 | Fragile; breaks on minor format changes; requires constant attention |

**Evidence basis**: Score MUST reference:
- Whether the gate auto-discovers what to check vs. requiring manual configuration
- Sensitivity to format/schema evolution
- Whether gate correctness can be verified automatically (meta-testing)

### 5. Composability (Weight: 0.10)

**Question**: Does this gate strengthen other gates? Can it be combined with other proposals?

| Score | Meaning |
|-------|---------|
| 9-10 | Directly enables or strengthens 2+ other gates; provides infrastructure reused by multiple checks |
| 7-8 | Complements 1-2 other gates; outputs can be consumed by downstream gates |
| 5-6 | Independent but compatible; doesn't conflict with other proposals |
| 3-4 | Partially overlaps with other proposals; may require deduplication |
| 1-2 | Conflicts with or makes other proposals harder; mutually exclusive approaches |

**Evidence basis**: Score MUST reference:
- Which other proposals this one reinforces or enables
- Whether outputs (extracted IDs, parsed structures) can be reused
- Whether the gate fits the existing `GateCriteria`/`SemanticCheck` pattern

---

## Weighted Score Formula

```
Score = (Success * 0.35) + (Complexity * 0.25) + (FalsePositive * 0.15) + (Maintainability * 0.15) + (Composability * 0.10)
```

**Score interpretation**:
- 8.0-10.0: Strong candidate — implement in next release
- 6.0-7.9: Good candidate — implement after high-priority items
- 4.0-5.9: Conditional candidate — implement only if composability benefits justify it
- Below 4.0: Weak candidate — reconsider approach

---

## Debate Protocol

Each adversarial debate uses two debaters:

**Advocate**: Argues for implementation. Must address:
1. Specific bug scenarios the gate would catch (with code examples from the forensic report)
2. Integration path into existing `GateCriteria`/`SemanticCheck` infrastructure
3. Composability benefits with other proposals

**Skeptic**: Argues against implementation. Must address:
1. Failure modes where the gate would NOT catch the bug
2. False positive scenarios with realistic examples
3. Maintenance burden over 5+ releases
4. Whether the same benefit can be achieved more simply

**Final scoring**: Both debaters propose scores. If scores differ by > 2 on any dimension, a tiebreaker rationale is required. Final score is the average of both debaters' scores, adjusted by tiebreaker rationale where applicable.

---

## Ranking Tiebreakers

When two proposals have the same weighted score:
1. Higher "Likelihood to Succeed" score wins
2. Higher "Implementation Complexity" (simpler) wins
3. Higher "Composability" wins
4. Alphabetical by proposal name

---

## Reference: The Bug This Framework Must Prevent

The cli-portify executor no-op bug (forensic report Section 9):

1. **Spec** defined three-way dispatch (`_run_programmatic_step`, `_run_claude_step`, `_run_convergence_step`)
2. **Roadmap** reduced this to "sequential execution with mocked steps" — SPEC_FIDELITY_GATE did not catch it
3. **Tasklist** faithfully reproduced the roadmap's incomplete executor — TASKLIST_FIDELITY_GATE passed (vacuously)
4. **Code** implemented a no-op default with `step_runner=None` — No gate exists at this link
5. **Result**: Pipeline silently "succeeds" with all steps "completed" but no real work performed

Any proposal scoring 7+ on "Likelihood to Succeed" MUST demonstrate it would break this chain at the specific link it targets.
