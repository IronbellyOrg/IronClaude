---
debate_round: 1
proposals: [proposal-1-architect, proposal-2-refactorer, proposal-3-qa]
convergence_score: 0.78
---

# Adversarial Debate Transcript

Three proposals were generated in parallel against `seed-brief.md`. Convergence score 0.78 reflects substantial agreement on the *what* (client headers, tiered limits, telemetry, log-only mode, webhook exemption) with sharp disagreement on the *how much scaffolding* axis and a partial but real disagreement on the threat-model scope.

## Tension 1 — Subsystem vs Single Module (Architect vs Refactorer)

**Architect's position**: Build `src/api/gateway/ratelimit/` as a 5-component subsystem with pluggable algorithms day one, on the theory that the requirements *already* imply extensibility (tiered plans, per-endpoint overrides, future self-service usage endpoint, webhook-specific behavior).

**Refactorer's pushback**: Speculative. Webhook exemption is *one config key*, not "an algorithm registry". A self-service usage endpoint is 20 lines added later. The architect is solving for an imagined v2; the team will ship the v1 the architect's design implies in late Q4, not Q3.

**Resolution**: **Lean refactorer with two architect concessions.** Ship a single module (`src/api/gateway/middleware/rate_limit.py`) wrapping `fastapi-limiter`. Concessions: (a) the `Decision` value-object pattern is adopted (cheap, ~15 lines) so headers and any future usage endpoint read from one source; (b) the per-endpoint exemption / algorithm-selector config key is included from day one, but with only one algorithm implemented (sliding-window-counter via the adopted library). This keeps the seam without paying the scaffolding cost. Architect's "secondary keys for botnet defense" seam is **dropped** — out of scope per refactorer + QA agreement.

## Tension 2 — Build vs Buy on the algorithm itself (Architect vs Refactorer)

**Architect's position**: Custom Redis-Lua sliding-window-counter, on the theory that the algorithm is small (~50 lines of Lua) and gives full control over header math.

**Refactorer's position**: `fastapi-limiter`, which already implements this correctly and has been in use at scale by other shops.

**Resolution**: **Adopt `fastapi-limiter`.** Refactorer is right on cost; the architect's "full control" argument is undercut by QA's point that the *failure-mode behavior* is what matters, not the algorithm shape, and that's testable regardless of build-vs-buy. **Caveat**: pin a specific version, vendor a fallback Lua script for the case where the library is ever yanked, document the choice in an ADR. (Architect concession: 1-page ADR captures the "what if we need to swap" path.)

## Tension 3 — Failure-mode policy (QA challenges both)

**QA's position**: Neither architect nor refactorer answers "what happens when Redis is briefly unavailable?" Fail-open and fail-closed are different products. Window-boundary doubling, clock skew across replicas, `X-Forwarded-For` spoofing — these aren't optional tests, they're the difference between a renewing customer and a SEV-2.

**Architect's reply**: Conceded. The `CounterStore` abstraction was supposed to make fail-open/closed configurable, but I didn't make it explicit. Yes, per-endpoint policy.

**Refactorer's reply**: Library default is fail-closed. Acceptable for v1 with documentation, but I'll add the per-endpoint policy hook QA wants — it's ~20 lines.

**Resolution**: **QA wins this entirely.** All eight failure modes QA enumerated become acceptance criteria. Per-endpoint fail-open vs fail-closed config is mandatory for v1. Test plan QA proposes (≥30 unit, ≥10 integration, ≥3 e2e, chaos coverage) is adopted as the test surface.

## Tension 4 — Threat-model scope (QA + Refactorer vs Architect)

**Architect's position**: Build the seam for secondary keys (IP, ASN, fingerprint) so botnet/distributed abuse can be added later without rework.

**Refactorer + QA position**: Botnet defense is a *different product* (WAF, bot management). Conflating gives you a worse version of both. Out of scope; state explicitly.

**Resolution**: **Refactorer + QA win.** Out of scope for this brainstorm. The merged requirements include an explicit "out of scope" line so the next person reading doesn't re-litigate this. (Architect concession: keep the principal-key field structured enough that a future secondary-key product can read from the same `Decision` object, but no API surface for it now.)

## Tension 5 — Plan-tier configuration location (Refactorer vs Architect)

**Architect**: Tiers in `config/gateway.yaml` for hot-reload + ops flexibility.

**Refactorer**: Tiers in code because they change quarterly (with pricing) and a code change has more review rigor than a config change.

**Resolution**: **Compromise.** Tier *definitions* in code (so a price change is a reviewed PR). Per-tier *limits* in `config/gateway.yaml` (so an ops-driven adjustment during an incident doesn't need a deploy). Per-endpoint *overrides* in `config/gateway.yaml`. This is one of the few places where the architect's "config layer" instinct lands cleanly.

## Remaining disagreements (logged for transparency)

- **Hot-reload via SIGHUP**: Architect wants it; refactorer says read at boot is fine because pod-roll is ~3 min. Not resolved — merged requirements flag as deferred to v1.1 unless an incident proves we need it sooner.
- **Burst allowance shape**: Open question from seed brief. No proposal had a definitive answer; merged requirements carry it forward as an open question with a recommended default (1.5× burst over 10s, configurable per tier).

## Convergence rationale

Three proposals, four of five tensions resolved with explicit positions. One tension partially deferred (hot-reload). Open questions reduced from 6 (seed brief) to 2 (merged). Convergence score **0.78** — solid PASS, with the residual disagreement being on cost/timing rather than on direction.
