# BF-3: Semantic Non-Determinism Contaminates Monotonic Progress

## Bug Summary

Architecture Sec 4.5 step 6 checks `current_run.high_count > previous_run.high_count` using **total** HIGH counts (structural + semantic combined). Since the semantic layer is LLM-based and inherently non-deterministic, temperature variation produces different HIGH counts between runs on identical inputs. This triggers false regression detection, which spawns 3 parallel worktree agents (FR-8) -- an expensive operation that wastes token budget on phantom regressions.

### Relevant Spec References

| Reference | Text | Issue |
|-----------|------|-------|
| NFR-1 | "Same inputs -> identical structural findings" | Scoped to structural only; does NOT guarantee semantic determinism |
| FR-7 | "Each run must have <= HIGHs than previous run" | Ambiguous: does not specify structural-only or total HIGHs |
| FR-8 | Regression detection spawns 3 parallel worktree agents | Expensive operation triggered by false positives |
| Sec 4.5 step 6 | `run_n+1.highs > run_n.highs? -> REGRESSION` | Uses combined count, contaminated by semantic noise |

### Root Cause

The convergence algorithm in `convergence.py` (Sec 4.5) uses a single `high_count` field that sums structural and semantic HIGHs. Semantic findings can fluctuate +/- 1-3 HIGHs between runs due to LLM non-determinism, even on identical inputs. This fluctuation crosses the monotonic progress threshold and triggers the expensive 3-worktree parallel validation flow.

---

## Solution A: Split Tracking with Structural-Only Monotonic Enforcement

### Description

Track `structural_high_count` and `semantic_high_count` separately in the deviation registry. Monotonic progress enforcement (FR-7 step 6) applies ONLY to structural findings. Semantic fluctuations between runs do not trigger regression detection. The final gate still requires 0 total active HIGHs to pass.

### Design Changes

#### 1. Deviation Registry Schema Change (`deviation_registry.py`)

Each run record gains split counts:

```json
{
  "runs": [
    {
      "run_number": 1,
      "structural_high_count": 3,
      "semantic_high_count": 1,
      "total_high_count": 4,
      "structural_medium_count": 5,
      "semantic_medium_count": 3
    }
  ]
}
```

Each finding gains a `source_layer` field:

```json
{
  "a1b2c3d4e5f67890": {
    "source_layer": "structural",
    "severity": "HIGH"
  }
}
```

#### 2. Convergence Algorithm Change (`convergence.py` Sec 4.5 step 6)

```python
# BEFORE (current):
if current_run.high_count > previous_run.high_count:
    handle_regression(...)

# AFTER (proposed):
if current_run.structural_high_count > previous_run.structural_high_count:
    handle_regression(...)
# Semantic fluctuation logged but does NOT trigger regression
if current_run.semantic_high_count > previous_run.semantic_high_count:
    log.warning(
        "Semantic HIGH count increased (%d -> %d); "
        "not triggering regression (non-deterministic layer)",
        previous_run.semantic_high_count,
        current_run.semantic_high_count,
    )
```

#### 3. Gate Evaluation (unchanged)

The final pass/fail gate remains: `active_high_count == 0` (total, both layers). This preserves convergence guarantees -- semantic HIGHs must still reach 0, they just don't trigger the expensive regression machinery when they fluctuate.

#### 4. Progress Logging

Progress log format changes from:
```
Run 1: 4 HIGHs -> Run 2: 3 HIGHs
```
To:
```
Run 1: 3 structural + 1 semantic = 4 HIGHs -> Run 2: 2 structural + 2 semantic = 4 HIGHs
  Structural progress: 3 -> 2 (monotonic OK)
  Semantic delta: 1 -> 2 (fluctuation, not regression)
```

### Analysis

| Criterion | Assessment |
|-----------|-----------|
| **Prevents false regression triggers?** | YES. Structural counts are deterministic (NFR-1). Only structural increases trigger regression detection. Semantic fluctuation is explicitly tolerated. |
| **Maintains convergence guarantees (FR-7)?** | YES, with clarification. The gate still requires 0 total HIGHs. Structural convergence is enforced monotonically. Semantic convergence is achieved through adversarial debate (FR-4) which downgrades or confirms HIGHs, but is not subject to run-over-run monotonic enforcement. |
| **Token budget impact** | POSITIVE. Eliminates false regression triggers that spawn 3 worktree agents. Estimated savings: 15,000-50,000 tokens per false trigger avoided. |
| **NFR-1 alignment** | PERFECT. NFR-1 explicitly scopes determinism to structural findings. This solution respects that boundary by only enforcing monotonic progress on the deterministic layer. |

### Risks

1. Semantic HIGHs could persist across all 3 runs without triggering the regression safety net. Mitigation: the adversarial debate (FR-4) already validates every semantic HIGH individually.
2. Slightly more complex registry schema. Mitigation: backward-compatible addition (old registries without `source_layer` default to `"structural"`).

---

## Solution B: Pin Semantic Temperature to Zero with Fixed Prompts

### Description

Set the semantic layer's LLM temperature to 0 and use deterministic prompt templates (no dynamic ordering, no timestamp injection, no randomized few-shot examples). This makes semantic findings quasi-deterministic. Keep combined HIGH tracking and the current monotonic progress algorithm.

### Design Changes

#### 1. Semantic Layer Configuration (`semantic_layer.py`)

```python
def run_semantic_layer(
    spec: SpecData,
    roadmap: RoadmapData,
    structural_findings: list[Finding],
    registry: DeviationRegistry,
    config: PipelineConfig,
) -> list[Finding]:
    # Pin temperature to 0 for determinism
    process = ClaudeProcess(
        temperature=0.0,
        top_p=1.0,  # disable nucleus sampling
        seed=42,     # if API supports it
    )
    # Use fixed prompt template with sorted inputs
    prompt = build_semantic_prompt(
        request,
        sort_sections=True,      # deterministic ordering
        include_timestamp=False,  # no temporal variation
    )
```

#### 2. Prompt Stabilization

- Sort all input sections alphabetically before injection
- Remove any timestamp or run-number references from the semantic prompt
- Use a fixed system prompt (no dynamic preamble variation)
- Ensure structural findings context is sorted by stable_id

#### 3. Convergence Algorithm (unchanged)

The existing `current_run.high_count > previous_run.high_count` check remains, operating on combined totals.

### Analysis

| Criterion | Assessment |
|-----------|-----------|
| **Prevents false regression triggers?** | PARTIALLY. Temperature=0 reduces variation significantly but does NOT guarantee identical outputs. LLM APIs do not provide strict determinism guarantees even at temperature=0 (floating-point non-determinism, model updates, batching effects). Variation is reduced from +/- 1-3 HIGHs to +/- 0-1, but the edge case remains. |
| **Maintains convergence guarantees (FR-7)?** | YES. No changes to the convergence algorithm. FR-7 is satisfied by the existing combined-count logic. |
| **Token budget impact** | NEUTRAL to SLIGHTLY NEGATIVE. Temperature=0 does not reduce token usage. False regressions are reduced but not eliminated, so occasional unnecessary 3-worktree spawns still occur. |
| **NFR-1 alignment** | PARTIAL. NFR-1 says "Same inputs -> identical structural findings" -- this solution attempts to extend determinism to the semantic layer, but cannot fully achieve it. The NFR was deliberately scoped to structural only because full semantic determinism is not achievable. |

### Risks

1. **False sense of determinism**: Temperature=0 is not a determinism guarantee. API providers explicitly state this. Model updates, server-side batching, and floating-point arithmetic can still produce different outputs.
2. **Quality degradation**: Temperature=0 can produce less nuanced semantic analysis. The semantic layer exists precisely because some checks require judgment -- constraining the model's sampling may reduce the quality of that judgment.
3. **API dependency**: The `seed` parameter is not universally supported. If the underlying API changes or the model is updated, quasi-determinism breaks silently.
4. **Deferred failure**: This solution reduces false regression frequency but does not eliminate it. The problem resurfaces unpredictably, making debugging harder.

---

## Comparative Analysis

| Criterion | Weight | Solution A (Split Tracking) | Solution B (Pin Temperature) |
|-----------|--------|---------------------------|----------------------------|
| **False regression prevention** | 40% | Eliminates completely for structural layer; semantic fluctuation tolerated by design | Reduces frequency (~80-90%) but does not eliminate; edge cases remain |
| **Convergence guarantee** | 30% | Preserved: gate requires 0 total HIGHs; structural convergence enforced monotonically | Preserved: no algorithm changes; but relies on quasi-determinism that can break |
| **Implementation feasibility** | 30% | Moderate: registry schema change, convergence algorithm update, progress log format change. All changes are additive and backward-compatible | Simple: configuration change + prompt stabilization. But correctness is not guaranteed and failures are silent |

### Scoring

| Criterion | Weight | A Score (0-10) | B Score (0-10) | A Weighted | B Weighted |
|-----------|--------|---------------|---------------|-----------|-----------|
| False regression prevention | 0.40 | 10 | 6 | 4.00 | 2.40 |
| Convergence guarantee | 0.30 | 9 | 7 | 2.70 | 2.10 |
| Implementation feasibility | 0.30 | 7 | 8 | 2.10 | 2.40 |
| **Total** | | | | **8.80** | **6.90** |

### Winner: Solution A (Split Tracking with Structural-Only Monotonic Enforcement)

**Rationale**: Solution A addresses the root cause (mixing deterministic and non-deterministic signals in progress tracking) rather than attempting to suppress non-determinism at the source. It aligns with the existing NFR-1 scoping, provides a complete fix rather than a probabilistic reduction, and is implementable with backward-compatible additive changes. Solution B's reliance on temperature=0 quasi-determinism is fundamentally fragile -- it masks the problem rather than solving it.
