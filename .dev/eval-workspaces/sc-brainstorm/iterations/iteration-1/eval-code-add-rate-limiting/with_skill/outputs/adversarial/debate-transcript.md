# Debate Transcript — Rate Limiting for Public API Endpoints

**Variants**: P1 (opus:architect, "Policy-First Subsystem") vs P2 (sonnet:refactorer, "Smallest Viable Middleware")
**Convergence target**: 0.75
**Final convergence**: 0.78 (PASS)

## Tension 1 — Module Layout (subsystem vs single file)

**P1 (architect)**: Three algorithms day-1 is acknowledged as over-engineering, but the *package layout* with `policy.py`, `algorithms/`, `storage/`, `middleware.py`, `metrics.py`, `config.py` is the minimum honest seam structure for a feature that will accrete consumers. A single file becomes a 1200-line god module by month 3.

**P2 (refactorer)**: The god-module fear is real but speculative. We have zero evidence of a second consumer today. A single 200-line module with clear internal sections is reviewable, debuggable, and trivially refactored into a package the day the second consumer lands. The refactor cost is bounded; the speculative-design cost is not.

**Resolution**: Adopt P2's single-module starting point BUT name the file in a directory layout that admits future expansion: `src/superclaude/ratelimit/middleware.py` (not `middleware/rate_limit.py`). Same line count, same shape, but the package boundary already exists so the day-2 split is a file move, not an import rewrite across the repo.

## Tension 2 — Algorithm Choice (token-bucket vs fixed-window)

**P1**: Token-bucket better matches API traffic; one Redis INCR+EXPIRE per request is comparable cost; and we own the algorithm-protocol seam from day-1.

**P2**: Fixed-window is the cheapest to debug. The boundary-spike behavior is a known, bounded artifact (≤2x burst for ~1s). v1 question is "any rate limiting at all," not "the optimal one."

**Resolution**: Ship **token-bucket** (P1 wins on this point — the algorithm choice influences operator mental model and 429 timing semantics, and token-bucket's `Retry-After` is more meaningful to clients). Use a Lua script for atomicity per P1; keep it to one algorithm with no protocol abstraction yet, per P2. The "Algorithm protocol" arrives only when we need the second algorithm.

## Tension 3 — Feature Flag States (3-state vs boolean)

**P1**: `off / shadow / enforce` lets us tune limits against real traffic without user impact — the shadow state is what makes the canary rollout safe.

**P2**: Shadow mode is real value but adds state-machine complexity for a v1 we're trying to keep minimal; staging traffic should be sufficient signal.

**Resolution**: Adopt **3-state flag** (P1 wins). The cost is one extra enum value + one extra metric label (`decision=would_deny`), and it directly de-risks the production canary — which is in the seed brief's success criteria. P2's instinct ("staging is signal") is true for known endpoints but breaks for traffic-shape-sensitive limits like rate limiting, where dev/staging volume doesn't match prod.

## Convergence Notes

Both proposals agree on: per-IP + per-API-key scope, 429 + Retry-After, Prometheus metrics, Redis-as-default with in-memory fallback, deferring per-customer-tier to v2, endpoint-by-endpoint canary rollout. Disagreement is concentrated on three axes (layout, algorithm, flag states), all resolvable without a re-debate. Convergence score: 0.78.
