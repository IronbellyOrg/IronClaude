---
debate_round: 1
proposals: [proposal-1-agent-A, proposal-2-agent-B, proposal-3-agent-C, proposal-4-agent-D, proposal-5-agent-E]
convergence_score: 0.71
adversarial_status: pass
blind_mode: true
blind_labels: ["Agent A", "Agent B", "Agent C", "Agent D", "Agent E"]
---

# Adversarial Debate Transcript — Consolidate Duplicate Auth Modules (BLIND)

> **NOTE — `--blind` mode.** All five proposals submitted under anonymized labels (Agent A through Agent E). Model identifiers are deliberately withheld from the debate transcript and from the merge process. This validates that convergence comes from real disagreement of position, not from model-personality bias or "model X aligns with model X" pseudo-diversity. Mapping is stored separately and is not loaded during scoring.

Five proposals across two architectural visions (A vs B), one cross-cutting security frame (C), one test-surface scoping (D), and one rollout-operations frame (E). The productive tension is **A vs B on architecture**; C, D, E orient orthogonally to that axis and the merged output incorporates them across whichever architecture wins.

## Tension 1 — Architecture: Plugin Framework vs Policy-Only Consolidation (A vs B)

**Agent A's position**: One core with plugin-style flows (`oauth2_pkce`, `password_flow`, `api_key`, etc.) AND per-service adapters. Protocol-specific concerns are first-class extension points inside the core, not "leftover logic" in service-side facades. ~18 engineer-weeks for the engineering work; 5 phases over 4 calendar months.

**Agent B's pushback**: Speculative scaffolding. The measured drift incidents (Q5, Q12 of seed brief) are *primitive-level*, not flow-level — JWT-library CVE asymmetry, password-policy update missed. A 300-LOC shared policy module + 300-LOC unified audit emitter addresses both without forcing a plugin framework. Per-service flow code stays in service repos where ownership is honest. ~10 engineer-weeks total.

**Resolution**: **Lean toward Agent B, with two Agent A concessions.**

- The *primitive-level drift* is the documented harm; the *flow-level drift* is a hypothesis. Agent B's policy-only consolidation directly addresses the documented harm. **Adopted.**
- Concession 1 from Agent A: **the override registry pattern** (per-service overrides require documented sign-off from security review at config-load time). Adopted because it operationalizes "no silent divergence" — the structural property both proposals want. ~50 LOC; cheap.
- Concession 2 from Agent A: **the unified Kafka audit topic + 90-day legacy-shim consumers**. Adopted because it's the only design that hits the 90-day-overlap requirement cleanly. Same 300 LOC Agent B proposed, restructured slightly.
- Per-service flow code (CSRF, PKCE, api-key HMAC) **stays in service repos** per Agent B. If a future SAML/OIDC need emerges, evaluate plugin extraction then; do not pre-build the abstraction.

## Tension 2 — Migration Safety: Is "Two Code Paths In Parallel" Itself a Security Risk? (C vs implicit A/B)

**Agent C's challenge**: Both A and B treat migration as refactoring-that-happens-to-touch-auth. Migration of auth IS an auth change. Shadow-mode + canary phases create a class of risk that doesn't exist in either end state alone: divergent lockout state, divergent audit emission, leaked sensitive data via shadow-mode logging. C1 (unified lockout store from the start) and C2 (audit dual-write with idempotency UUIDs) are non-negotiable controls regardless of architecture.

**Agent A's reply**: Conceded. The plugin design's `policy/lockout_policy.py` SHOULD write to the existing `security_utils/lockout.py` Redis store from day one. C1 is correctly framed.

**Agent B's reply**: Conceded. My ~10-week estimate did not include shadow-mode-runner-sensitive-data redaction (C3) or per-phase pentest (C4) explicitly. Adds ~3 engineer-weeks to my estimate.

**Agent D's reply**: My test plan includes C1 enforcement explicitly in the lockout-policy test cases. Compatible.

**Resolution**: **C wins; all six controls (C1-C6) adopted as Acceptance Criteria / Mandatory Controls.** Pre-migration pentest + per-cutover pentest cadence becomes part of the rollout plan. Shadow-mode delta detector MUST redact at the runner, not at the log-storage layer. Lockout store is unified from Phase 0 (no per-service divergence during shadow mode).

## Tension 3 — Test Surface: Is It "Standard" Or Is It The Hard Part? (D vs implicit A/B)

**Agent D's challenge**: Both A and B understate the test surface by an order of magnitude. ≥120 unit + ≥150 contract + ≥90 integration + shadow-mode 50K-corpus delta detector + ≥30 E2E + ≥4 pentests. **+8 engineer-weeks on top of either architecture's cost.**

**Agent A's reply**: Accepted, with one note: the plugin architecture's contract-test surface is per-flow as well as per-service-boundary, so the contract count is closer to ~200 not ~150. A's revised estimate: 18 + 8 + ~1 (extra contracts) = ~27 engineer-weeks all-in (excluding C's controls).

**Agent B's reply**: Accepted. B's revised estimate: 10 + 8 = ~18 engineer-weeks all-in (excluding C's controls).

**Resolution**: **D's test plan adopted as Acceptance Criteria.** Test development runs in parallel with architecture build-out from Phase 0. Shadow-mode delta-detection runner is in the critical path; if it isn't ready, no service exits shadow mode. Pentest engagements scheduled before each cutover, not just at end-of-migration.

## Tension 4 — Rollout Operations: How-Do-We-Ship-It (E vs implicit A/B)

**Agent E's challenge**: Architecture (A, B), security controls (C), and tests (D) are the *what*. None of them ship without explicit operational scaffolding: per-service feature flags with sub-flag granularity (O1), promotion checklist as code (O2), dashboards-before-code (O3), per-phase runbook entries (O4), on-call briefings (O5), production-shadow alignment (O6), hard timer on 90-day overlap with reconciliation gate (O7), quarterly override-registry review (O8). +5 engineer-weeks parallel to app work, requires SRE/platform involvement.

**Agent A's reply**: Accepted. The plugin architecture's per-flow rollback granularity benefits especially from O1's sub-flag pattern.

**Agent B's reply**: Accepted. Smaller architecture = fewer sub-flags = O1 is slightly cheaper on B's path.

**Agent C's reply**: O7 (90-day timer + reconciliation gate) operationalizes my C2 dual-write requirement; agreed.

**Agent D's reply**: O3 (dashboards before code) is necessary for shadow-mode delta detection to be observable; agreed.

**Resolution**: **All of E's operational scaffolding adopted.** SRE/platform engagement required; not optional. Pre-1 (billing_core post-mortem reading session) is mandatory for anyone on the project.

## Tension 5 — Migration Ordering: API First, Web First, or Mobile First? (carried over from seed brief OQ6)

**Agent A's position**: api first (fewest behaviors, cheapest validation of adapter pattern), then web (most familiar), then mobile (largest blast radius).

**Agent B's position**: api first (smallest refactor scope), then web, then mobile (most test cases).

**Agent C's position**: api first because the test surface for OAuth2 client_credentials is the cleanest pentest validation of the new core's primitives before exposing customer-facing surfaces.

**Agent E's position**: api first because the smallest service has the smallest dashboard buildout and validates O3 (dashboards-before-code) cheapest.

**Agent D's position**: api first (smallest contract-test count for Phase 1).

**Resolution**: **Unanimous: api first.** Then web. Then mobile. No tension.

## Remaining disagreements (logged for transparency)

- **Plugin framework deferred-vs-deleted**: Agent A wanted a seam for future SAML/OIDC; Agent B wanted no scaffolding. **Merged compromise**: per-service flow code stays in service repos with override-registry discipline; if SAML/OIDC need emerges within 12 months of migration completion, evaluate plugin extraction at that point. The decision is *deferred*, not refused.
- **Pentest cadence**: Agent C wants 4 pentests (pre + per-cutover); Agent E's promotion checklist treats pentest as one of many checks. **Merged**: pentest is a *blocking* checklist item on each cutover promotion, not advisory. Findings ≥ MEDIUM block.
- **Override registry approval flow**: who is "security review"? **Open Question carried forward** — operationalize in Phase 0.
- **Shadow corpus collection**: Agent D acknowledges that production-traffic-alone may not cover rare-error paths; synthetic augmentation may be needed. Concrete shape TBD in Phase 0.

## Convergence rationale

Five proposals from five anonymized agents. One architectural tension (A vs B) resolved with primary direction + named concessions. Three cross-cutting frames (C, D, E) adopted in full and integrated across the merged plan. One unanimous decision (migration ordering). Two minor disagreements carried as Open Questions. Open-questions list reduced from 7 in seed brief to 4 in merged requirements.

Convergence score **0.71** — solid PASS. Lower than a 5-proposal three-persona run might be because the A-vs-B architectural disagreement is genuine and load-bearing; the resolution leans B but preserves A's two cheapest contributions. The blind labels successfully prevented the merge from gravitating to "the model usually right on these" — the merge reflects the **arguments**, not the agents.
