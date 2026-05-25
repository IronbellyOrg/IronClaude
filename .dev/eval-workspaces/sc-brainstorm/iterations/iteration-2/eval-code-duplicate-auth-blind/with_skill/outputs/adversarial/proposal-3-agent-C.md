---
proposal_id: 3
agent_label: Agent C
persona: security
blind_mode: true
lens: STRIDE, audit/compliance evidence, threat model under migration
---

# Proposal 3 — Agent C: Migration Itself Is the Highest-Risk Auth Change of the Year — Treat It That Way

## Position

The technical proposals on either side of this debate (Agent A's plugin framework, Agent B's policy-only consolidation) are both **defensible end states**. Neither addresses the question that determines whether we ship without an incident: **how do we prove, at every phase, that the new code does not introduce a subtle auth weakness while we are migrating one of the most security-sensitive surfaces in the system?** Migration introduces a class of risk that does not exist in either end state alone: **two code paths running in parallel** (shadow mode and canary phases) where a subtle delta in lockout-state, audit emission, or session-handling can silently weaken the security posture for the duration of the migration.

## Required investigation steps

1. **Threat-model the migration itself**, not the end state. STRIDE applied to shadow-mode: can an attacker observe the *delta* between old and new paths to fingerprint the new code's behavior before it goes canonical? Can the canary's lockout state diverge from the legacy lockout state and create a window where an attacker is locked out on one path but not the other?
2. **Audit-trail forensics scenario**: if we get a customer-claim incident during the 90-day overlap, can we reconstruct exactly what the customer experienced from the legacy stream + the unified stream, even with eventual-consistency on the S3 path? Test this with a synthetic incident before any canary traffic flows.
3. **Pre-migration pentest** on the unified core in isolation, before any service cuts over. Catching a vulnerability after canary is exponentially worse than catching it before.
4. **Per-phase pentest on cutover** — not just end-of-migration. Each service's first 50% canary phase is its own ship event with its own attack surface.

## Required controls (regardless of which technical proposal is adopted)

- **C1** — **Lockout-state convergence guarantee.** During shadow mode, both old and new paths MUST read from and write to the *same* lockout state store (the canonical Redis lockout counter from `security_utils/lockout.py`). If they don't, an attacker can hit the rate limit on the old path while the new path's counter is at zero — exploitable. The simplest fix: new core writes to the existing lockout store unconditionally; no new lockout store is introduced until 100% cutover.
- **C2** — **Audit dual-write with idempotency.** During the 90-day overlap, every login event writes to both unified Kafka and the legacy destination. Each event carries a UUID so deduplication is possible during reconciliation. If unified emit succeeds and legacy emit fails (or vice versa), the result is alerted as a divergence — not silently absorbed.
- **C3** — **Sensitive-data redaction in shadow comparison.** Shadow-mode delta detection MUST NOT log raw passwords, tokens, or session IDs — even into our own observability. Delta detector compares hashed-and-salted outputs only. (Trivially overlooked; trivially catastrophic.)
- **C4** — **Per-phase regression gates.** Each phase (shadow / 5% / 50% / 100%) has explicit pass criteria: (a) zero delta between old and new path outcomes on the same input (for shadow); (b) error-rate delta < 0.1% (for canary phases); (c) zero new audit-stream divergences; (d) zero new login-latency outliers above the P99 budget. Failure on any criterion blocks promotion to the next phase.
- **C5** — **Compliance attestation alignment.** The Q3 audit cycle finding language ("inconsistent auth controls") must be addressed in the new core's documentation by an explicit per-policy mapping table (web before / api before / mobile before → unified). Engineering produces the table; compliance signs off; this becomes part of the audit packet.
- **C6** — **Threat-model the shadow-mode runner itself.** The runner has access to two parallel auth flows' inputs and outputs; it is a high-privilege piece of infrastructure. Pentest it. Restrict access. Decommission after 100% cutover — leaving the shadow runner alive past its useful life is asking for it to become a back door.

## What I'd push back on

Both Agent A and Agent B treat the migration as a refactor that happens to touch auth. **A migration of auth IS an auth change**, and changes to auth code paths are treated by compliance, by pen-testers, and by attackers as load-bearing events. Neither proposal's rollout plan currently includes a pre-migration pentest or per-phase pentest gates; both should.

## What I'd concede

I have no preference between Agent A and Agent B on the architecture itself. Either ships safely with the controls above; either ships dangerously without them. The argument should not be "which architecture", it should be "which architecture lets these controls land cheapest". On that metric, I lean toward Agent B — fewer moving parts means the shadow-mode runner has less to compare and the threat-model is smaller.

## Cost

C1-C6 together: ~3 engineer-weeks added on top of either Agent A's or Agent B's plan + pentest engagement (~2 weeks of external pentester time + ~1 week of internal remediation time per pentest, 4 pentest cycles = ~12 weeks total external scheduling but ~4 weeks of internal load). Non-negotiable; the migration is a high-risk auth change.

## Confidence

High on every control. The shadow-mode lockout-state divergence is the kind of thing that does not show up in unit tests; we will find it in pre-migration pentest if we look for it, and we will find it in production if we do not.
