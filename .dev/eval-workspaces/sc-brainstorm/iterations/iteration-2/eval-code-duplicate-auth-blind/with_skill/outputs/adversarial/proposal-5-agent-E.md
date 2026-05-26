---
proposal_id: 5
agent_label: Agent E
persona: devops
blind_mode: true
lens: rollout safety, observability, on-call readiness, deploy mechanics
---

# Proposal 5 — Agent E: The Rollout Mechanics Are Where This Either Lands Cleanly Or Becomes The Story

## Position

Three of the prior proposals focus on the *what* (Agent A: plugin architecture; Agent B: policy-only consolidation; Agent C: security controls). One focuses on the *how-do-we-prove-it* (Agent D: test surface). None address the *how-do-we-ship-it* — the operational mechanics of a 4-service-touching, 3-phase-per-service, 90-day-overlap-audit-stream migration. This is the work that determines whether the project completes by end of Q3 or quietly slips into Q1 next year with two services migrated and the third stalled on operational concerns.

## Required operational scaffolding

- **O1** — **Per-service feature flag with sub-flag granularity.** Each service has flags for: `auth_core_enabled` (bool), `auth_core_canary_percent` (0-100), `audit_dual_write` (bool, default true during 90-day overlap), `shadow_mode_active` (bool), `lockout_store_unified` (bool — Agent C's C1, but operationalized). Sub-flags allow rollback of any specific behavior change without rolling back the whole migration. Default values reviewed by the EM before each phase promotion.
- **O2** — **Promotion checklist as a code artifact.** A YAML checklist per phase: pre-promotion checks (test green, shadow-delta zero, pentest pass, observability dashboards live, runbook updated, on-call briefed), in-flight checks (canary error rate, P99 latency, audit-stream divergence count), post-promotion checks (24h-of-clean-signal before next phase). Stored in `services/shared/auth_core/promotion-checklists/`; reviewed at PR time; promotion gated by checklist execution.
- **O3** — **Dashboards before code.** Login-success-rate, login-latency P50/P99, lockout-counter-divergence, audit-stream-divergence, per-flow error rate, per-service vs unified comparison views. All dashboards exist and have alerts wired BEFORE Phase 0 builds begin. Owners assigned per dashboard panel. (Lesson from the billing_core consolidation post-mortem cited in the enrichment doc: dashboards built after the fact missed the early-signal window on a regression that became a Sev-2.)
- **O4** — **Per-phase runbook entry.** Each promotion event has a runbook entry: how to roll back, who pages whom, what the kill-switch path is, what the expected dashboard signature looks like during/after promotion. Runbook entry is part of the promotion-checklist code artifact and reviewed.
- **O5** — **On-call briefing per phase.** 30-minute brief before each promotion: what's changing, what to watch, where to find the kill-switch. Recorded; available to anyone in the rotation. Lesson from billing_core: the engineer who ran the promotion was on PTO when the regression hit, and the on-call had to learn the new system from incident-response.
- **O6** — **Production-shadow environment alignment.** The shadow-mode runner needs production-shape traffic to be useful (Agent D's 50K-corpus claim). Coordinate with the existing production-shadow setup (already used for payments-webhook work per the cross-cutting refs) and ensure it can mirror auth traffic without violating PII boundaries.
- **O7** — **Hard timer on the 90-day audit-stream overlap.** Day 90 is a scheduled event; before it, run a reconciliation across legacy and unified streams to prove zero gaps; if reconciliation finds gaps, the 90-day clock pauses and resets. Decommission of legacy streams is itself a phase gated by a checklist.
- **O8** — **Quarterly review of the override registry** (Agent A's per-service-override mechanism, regardless of which architecture wins). An override that nobody re-justifies for two quarters auto-expires. Drift prevention is structural; this is its operational analog.

## Required pre-build investments

- **Pre-1** — billing_core consolidation post-mortem reading session. ~2 engineer-hours, mandatory for anyone touching this project.
- **Pre-2** — Production-shadow capacity review. The current setup is sized for payments; adding auth traffic may require scaling. ~1 engineer-week to validate or expand.
- **Pre-3** — Audit-stream Kafka topic provisioned with appropriate retention (matches PCI 7-year? probably not, but matches the dual-write window) and access controls. ~3 engineer-days.

## What I'd push back on

Agent A's "~18 engineer-weeks" and Agent B's "~10 engineer-weeks" do not include any of the operational scaffolding above. Realistically: Agent A is ~24 engineer-weeks all-in (architecture + tests per Agent D + operational scaffolding per this proposal + security controls per Agent C); Agent B is ~16 engineer-weeks all-in. **Either can land in Q3**, but only with explicit operational scaffolding from the start. Without it, the migration ships in Q1 next year, the compliance audit cycle finds the unchanged drift, the finding repeats, and we are back where we started with one more failed initiative on the team's reputation.

## What I'd concede

The architectural debate between Agent A and Agent B is real but secondary to whether the operational scaffolding is in place. With it, either ships. Without it, neither.

## Cost

O1-O8 + Pre-1 to Pre-3 together: ~5 engineer-weeks of platform / SRE-aligned work, parallel to the application work. Sustaining cost: ~5% of on-call's time on auth-migration support during the rollout phases. Total schedule impact: zero (parallel), but resourcing impact: requires SRE or platform-engineering involvement, not just app-team time.

## Confidence

High. Every recommendation above is a direct lesson from the billing_core consolidation referenced in the enrichment doc; not novel, just disciplined.
