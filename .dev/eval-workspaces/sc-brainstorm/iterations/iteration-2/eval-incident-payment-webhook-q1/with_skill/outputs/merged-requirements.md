---
spec_type: incident-remediation
domain: incident
strategy: enterprise
adversarial_status: pass
convergence_score: 0.74
proposal_count: 5
source_proposals: [proposal-1-analyzer-opus, proposal-2-analyzer-sonnet, proposal-3-security-opus, proposal-4-security-sonnet, proposal-5-devops-haiku]
debate_transcript: ./adversarial/debate-transcript.md
source_seed: ../seed-brief.md
---

# Merged Remediation Requirements: Q1 Payment Webhook Delivery Failures

## Problem Statement

Three Sev-2 incidents in Q1 2026 (Jan 18, Feb 9, Mar 27) share a common pattern — latency drift → backlog → retry storm → DLQ overflow → merchant-side reconciliation gap — but were PIR'd individually as discrete proximate causes. 412 merchants impacted, $1.4M delayed settlements, one Tier-1 enterprise renewal at risk, and a documented gap in PCI-DSS §10.2 evidence-chain claims (unbounded DLQ + over-counted "delivered" rate). Remediation is multi-dimensional: structural observability blindness (analyzer), architectural amplification across the 3-tier retry pipeline (analyzer), compliance evidence chain (security), and on-call operability of the system (devops). Single-tier "all merchants on the chain" is not viable; tiered posture is required. Disclosure-readiness review on past audit attestations is a non-negotiable precondition.

## Post-Mortem Framework (Required Investigation Steps)

- **I1** — **Re-PIR with latency-drift overlay.** Pull 7-day pre-incident latency P99 series for all three Q1 incidents; confirm or falsify the 36-hour upstream signal hypothesis empirically. *(P1 §investigation, ratified)*
- **I2** — **Cascading-failure flow model.** Trace each incident through the 3 retry tiers with timestamped queue depths. Compute upstream-tier-max-output vs downstream-tier-max-input ratios. *(P2 §investigation)*
- **I3** — **End-to-end evidence-chain audit, 100-transaction sample** across the three incidents. For each: dispatcher delivery-attempt record present? merchant reconciliation shows receipt? compliance posture? *(P3 §investigation)*
- **I4** — **Audit attestation history review.** What have we told PCI/SOC2 auditors about the evidence chain in the last two cycles? **Surface to legal before any remediation lands.** *(P4 §investigation, S6)*
- **I5** — **Runbook drift audit + on-call competence audit.** Compare current 3-year-old runbook to system today; score each rotation member's last-touched / tabletop-vs-real for this surface. *(P5 §investigation)*
- **I6** — **SLO contract reality check.** Public docs vs enterprise contracts vs delivered-quarterly. Identify any mismatch that triggers disclosure obligations. *(P5 §investigation, P4 §caveat)*

## Functional Requirements

- **FR1** — **Latency-drift alert**: P99 webhook-delivery-latency alert at +25% over 7-day rolling baseline, sustained 30 min, paging on-call with runbook link. *(P1 R1, ratified by all)*
- **FR2** — **Per-tier bulkhead queue isolation**: Tier-1 / Tier-2 / Tier-3 merchants get isolated dispatcher pipelines with allocated capacity. One slow merchant in Tier-2 does not starve Tier-1. *(P2 R1, sequencing per debate Tension 1)*
- **FR3** — **Bounded DLQ with chain-of-custody**: Tier-1 entries cryptographically signed at producer time, 18-month retention. Tier-2/3 entries audit-logged but not signed, 7-day TTL with audit-logged eviction. Replay produces a new chain entry, never mutates the original. *(P3 S1 + P4 S1' merged, debate Tension 2)*
- **FR4** — **Cross-tier back-pressure**: Each retry tier signals upstream at 80% capacity. Producer (API handlers) throttle when tier-1 in-process retry is saturated; tier-1 throttles when tier-2 Redis Streams is saturated; tier-2 throttles when DLQ is at 80% of its tier-specific max. *(P2 R3)*
- **FR5** — **Merchant-ack callback (Tier-1 launch, Tier-2 opt-in, Tier-3 not offered)**: Tier-1 merchants confirm processing via `POST /v1/webhooks/ack` with transaction ID + dispatcher receipt token; corroborates our "delivered" claim. *(P3 S2 + P4 S2' merged)*
- **FR6** — **HMAC signing-key quarterly rotation**: Forced 90-day rotation for all merchants with a 14-day overlap window. **Precondition**: historical log scan for prior key exposure must run **before** rotation announcement. *(P3 S3 + P4 S4 addition)*
- **FR7** — **DLQ access audit logging + per-merchant break-glass**: Every read of a webhook body in the DLQ produces an audit entry (operator, timestamp, transaction ID, justification, ticket reference). Break-glass access auto-notifies the merchant's account manager within 1 hour. *(P3 S5 + P4 S5 addition)*
- **FR8** — **Per-merchant SLO observability**: Self-serve dashboard per Tier-1 merchant displaying their delivery percentile, identical number to ours. *(P1 R2 + P5 D4 overlap)*
- **FR9** — **DLQ size telemetry**: Prometheus gauge with alerts at 100K and 500K rows per tier. *(P1 R3)*
- **FR10** — **Webhook-health primary dashboard for on-call**: Latency P50/P99, retry rate, DLQ size, top-10 contributing merchants, merchant error split (4xx vs 5xx). Defaulted-to-on-call-screen-from-page. *(P1 R4 + P5 D6)*
- **FR11** — **Runbook rewrite**: Step-by-step for each of the three Q1 incident patterns + Redis Streams operations + DLQ replay + per-merchant kill switch. Each entry dated, each entry has expected output, stale-after-6-months policy. *(P5 D1)*
- **FR12** — **Owner field on every dashboard panel and alert**: RACI documented in on-call workspace, quarterly review. No metric without an owner. *(P5 D6)*

## Non-Functional Requirements

- **NFR1** — Throughput SLO preserved: 8K/sec sustained, 25K peak, no regression at any rollout phase. *(seed brief constraints)*
- **NFR2** — Zero data loss for accepted webhooks across remediation rollout. *(seed brief)*
- **NFR3** — PCI-DSS §10.2 evidence-chain end-to-end coverage for Tier-1; documented best-effort for Tier-2/3 with corresponding attestation language narrowing. *(P3 + P4)*
- **NFR4** — Latency overhead from new controls (bulkhead routing + signing + back-pressure check) ≤ 5ms P99 added to per-webhook dispatch path; measured in production-shadow before each region rollout. *(P5 D5)*
- **NFR5** — Per-region rollout cadence: US-East → US-West → EU → APAC with 1 week minimum between regions. *(P5 D5, seed brief Q14)*
- **NFR6** — Public SLO and contracted SLO and delivered-quarterly published to an internal dashboard, exec-reviewed quarterly. *(P5 D3)*
- **NFR7** — All 4 on-call rotation members can solo-triage each Q1 incident pattern via tabletop drill within 2 quarters. *(P5 D2)*

## Acceptance Criteria

- **AC1** — All three Q1 incident patterns produce **zero Sev-2-or-worse** in Q2 and Q3. *(seed brief success criteria, ratified)*
- **AC2** — DLQ steady-state < 50K rows, peak < 500K rows under worst-quarter load; index-scan latency stays under 50ms P99 at peak. *(P2 R2 + P1 R3 metrics)*
- **AC3** — Latency-drift alert (FR1) fires on a re-played replay of the Mar 27 incident's pre-incident latency series; confirmed in chaos test. *(P1 R1 + P5 D5)*
- **AC4** — Bulkhead test: synthetic Tier-2 merchant generates 10x normal load; Tier-1 P99 latency does not degrade by more than 2ms. Verified in production-shadow. *(P2 R1)*
- **AC5** — Chain-of-custody: cryptographic signature verification on a Tier-1 DLQ replay produces a chain that an external auditor can verify with our public attestation key. Tested with internal compliance team prior to GA. *(P3 S1, P4 S1')*
- **AC6** — Merchant-ack callback: 5 Tier-1 merchants opt in to ack-callback during Q2; ack-rate vs. our delivery-rate within 0.01% over a 1-week window. *(FR5)*
- **AC7** — HMAC rotation dry-run: 5 merchants complete a key rotation within the 14-day overlap window with zero failed deliveries; one merchant deliberately fails to rotate and is gracefully cut over to the new-key-only enforcement window. *(FR6)*
- **AC8** — Runbook rewrite: each entry has been tabletop-validated by at least one on-call engineer who was not the author. 4/4 rotation members complete tabletop drills before Q2 close. *(FR11 + NFR7)*
- **AC9** — Owner field present on 100% of webhook-system dashboard panels and alerts before Q2 close. *(FR12)*
- **AC10** — Internal SLO dashboard published; first quarterly exec review held before Q3 start; surfaces any contracted-vs-delivered gap to legal for disclosure-readiness assessment. *(NFR6 + P4 S6)*

## Risks

- **R1** (severity: HIGH) — **Disclosure obligation surfacing during audit history review (I4).** If past attestations are inconsistent with the now-known evidence-chain gap, legal counsel is required and remediation may need to publish before completion. *Mitigation*: I4 runs first, in parallel with engineering kickoff, with a defined escalation path to GC.
- **R2** (severity: HIGH) — **Bulkhead rollout itself causes incident.** Per-tier queue routing is a critical-path change; a misconfiguration could route Tier-1 traffic into the wrong queue. *Mitigation*: production-shadow for ≥2 weeks; per-region feature-flagged rollout with explicit rollback triggers (P5 D5: rollback if P99 +10%, DLQ growth +2x, or any merchant kill-switch within 24h of rollout).
- **R3** (severity: MEDIUM) — **HMAC rotation reveals historical log exposure.** If the log scan (FR6 precondition) finds prior key strings in logs, every affected merchant needs immediate notification and emergency rotation. *Mitigation*: legal + customer-success looped in before the scan starts; pre-drafted notification copy ready.
- **R4** (severity: MEDIUM) — **Tier-2/3 merchants object to narrower attestation language.** "Documented best-effort" replacing implied chain-of-custody could trigger customer churn. *Mitigation*: customer-success messaging treats this as a transparency upgrade ("we now tell you exactly what we guarantee"), not a downgrade.
- **R5** (severity: MEDIUM) — **Per-merchant SLO observability dashboard cardinality.** 10K+ merchants × N metrics could overwhelm the metric store. *Mitigation*: sampling strategy + Tier-1-only initially; broader rollout subject to capacity review.
- **R6** (severity: LOW) — **Runbook drift recurrence.** A 6-month staleness policy works only if enforced. *Mitigation*: dashboard widget showing N runbook entries past staleness threshold; included in EM's weekly review.

## Open Questions

- **OQ1** — **Authentication-rotation contract**: do we require merchants to register a key-rotation webhook (P3 security position) or detect 401-streak heuristically and auto-notify (P5 operability position)? Resolution: pilot heuristic detection in Q2, evaluate adoption of required-registration in Q3 based on signal quality.
- **OQ2** — **Per-merchant bulkhead within Tier-1**: per-tier bulkhead is the Q2-Q3 ship; whether to subdivide Tier-1 into per-merchant queues depends on Q2-Q3 incident data. Carried forward.
- **OQ3** — **Cross-region failover posture**: current single-region-with-DR is the de facto position; active-active is a separate multi-quarter project not in scope here but should be on the roadmap. Decision: not in scope; flagged for product/platform planning.
- **OQ4** — **DLQ retention beyond 18 months for Tier-1 contractual customers**: some enterprise contracts may require longer retention. Resolution: case-by-case in customer-success workflow; chain-of-custody design supports arbitrary retention.

## Provenance

| Requirement | Origin |
|---|---|
| FR1 (latency-drift alert) | P1 R1; ratified by all five proposals; debate Tension 1 resolution |
| FR2 (per-tier bulkhead) | P2 R1; debate Tension 1 sequencing |
| FR3 (chain-of-custody DLQ, tiered) | P3 S1 + P4 S1' merger; debate Tension 2 |
| FR4 (cross-tier back-pressure) | P2 R3; ratified by P1 |
| FR5 (merchant-ack callback) | P3 S2 + P4 S2'; debate Tension 2 |
| FR6 (HMAC rotation + pre-scan) | P3 S3 + P4 S4 historical-scan addition |
| FR7 (DLQ access audit + break-glass) | P3 S5 + P4 S5 break-glass addition |
| FR8 (per-merchant SLO observability) | P1 R2 + P5 D4 + P3 S2 overlap |
| FR9 (DLQ size alerts) | P1 R3 |
| FR10 (webhook-health dashboard) | P1 R4 + P5 D6 |
| FR11 (runbook rewrite) | P5 D1 |
| FR12 (dashboard owner field) | P5 D6 |
| NFR1-NFR2 (throughput + zero loss) | Seed brief constraints |
| NFR3 (tiered PCI evidence) | P3 + P4 merger |
| NFR4 (latency overhead) | P5 D5 + production-shadow guidance |
| NFR5 (region rollout cadence) | P5 D5 + seed brief Q14 |
| NFR6 (SLO contract dashboard) | P5 D3 |
| NFR7 (tabletop drill coverage) | P5 D2 |
| AC1-AC10 | Cross-cutting; each maps to FR/NFR origin above |
| R1 (disclosure obligation) | P4 S6 disclosure-readiness check |
| R2 (bulkhead rollout risk) | P5 D5 + debate Tension 4 |
| R3 (log exposure during HMAC scan) | P4 S4 addition |
| R4 (Tier-2/3 attestation pushback) | P4 customer-success risk |
| R5 (cardinality) | P1 R2 own caveat |
| R6 (runbook drift recurrence) | P5 D1 enforcement |
| OQ1-OQ4 | Debate tensions remaining + seed brief open questions |
