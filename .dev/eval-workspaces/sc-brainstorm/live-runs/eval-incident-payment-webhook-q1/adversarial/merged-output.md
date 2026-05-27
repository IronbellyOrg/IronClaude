# Merged Output — Q1 Incident Response Program for Payment Webhook Delivery Failures

(This file is the raw adversarial merge output. Canonical 6-section requirements with provenance are emitted as `../merged-requirements.md`.)

## Program Spine (waves)

### Wave 0 — Foundation (Week 0-1, four parallel lanes)

**Lane A — Stabilization (from V4 devops):**

- Pin HPA min-replicas to peak-hour capacity across 07:00-10:00 UTC for next 4 weeks (non-PCI).
- Raise connection-pool ceilings on top-50 merchant routes.
- Increase retry budget with explicit jittered backoff cap to prevent retry-amplification.
- Key-rotation hotfix: force-flush worker key cache on Vault rotation event; 30s dual-acceptance grace window. Treated as PCI emergency-change with full post-hoc evidence collection.

**Lane B — Telemetry hardening (from V1 analyzer):**

- Add signing-key-version trace tag on all worker-emitted spans.
- Per-merchant retry-amplification metric.
- Egress DNS resolution histogram by merchant CIDR (to rule out DNS hypothesis).
- Replay-attempt fan-out visualization in Grafana.
- Sampling-rate increase to 100% for failed deliveries.

**Lane C — Compliance infrastructure (from V3 security):**

- Stand up `incident-q1-2026/` controlled-access artifact repository.
- PCI scope-class mapping table for every proposed remediation.
- Submit key-id-in-header design doc to secure-change-review board by Day 3 (clears 2-week lead time for Week 4-5 deployment).

**Lane D — Comms infrastructure (from V5 scribe):**

- RCA narrative skeleton (sections: problem, evidence, root cause, remediation, prevention).
- Merchant comms template with legal-pre-reviewed boilerplate.
- Weekly steerco status template with RAG indicators + SLA-credit run-rate.
- Stakeholder map + cadence lock: weekly to merchants, weekly to VPs, milestone-based to auditor.

### Wave 1 — Stabilization Validation (Week 2-3)

- Daily SLO review against per-merchant + aggregate dashboards.
- Target: >=99.9% sustained by end of Week 2.
- Begin 14-day sustained validation window Week 3.

### Wave 2 — Durable Remediation (Week 3-5)

- Per-merchant SLO alerting deployed (mandated control 1).
- Key-rotation safety harness deployed (mandated control 2) — canary + automated rollback for signing-key propagation.
- Key-id-in-header durable deployment (V2 architect) Week 4-5 — supersedes Week 0 hotfix.

### Wave 3 — RCA Finalization (Week 5-6)

- RCA narrative populated against telemetry and remediation evidence.
- Three-hypothesis evidence: key-rotation race (ruled in or out); HPA cold-start (ruled in or out); merchant-side amplification (ruled in or out).
- VP Engineering sign-off Week 6.

### Wave 4 — Auditor Packaging (Week 6-7)

- Artifact bundle finalized: RCA, change records, test evidence, control deployment records.
- Independent verification by security engineering completed.
- Bundle delivered to SOC 2 auditor no later than Apr 12.

### Wave 5 — Merchant Comms + Validation Close (Week 7-8)

- Tier-1 SLA credits processed.
- Merchant comms artifact published (legal sign-off completed).
- 14-day sustained validation window closes; final SLO report.
- Program close report to VP steerco.

## Mandated Preventive Controls

- **Control 1 — Per-merchant SLO alerting:** Bounded alert-fatigue budget; SLO bounds tuned against 14-day baseline; paging integration through PagerDuty.
- **Control 2 — Key-rotation safety harness:** Canary deployment of signing-key updates with automated rollback on signature-verification failure rate spike. Underpinned by the key-id-in-header pattern (durable fix from V2).

## Comms + Artifact Discipline

- Single comms channel: customer success + legal jointly own merchant-facing communications. Customer success cannot speak directly to merchants without joint comms artifact.
- Weekly cadence: comms artifact draft Tuesday EOD -> legal sign-off Friday -> merchant publication Monday.
- Auditor evidence pipeline: every workstream produces artifact-repo entries continuously; SOC 2 auditor granted read access Week 6.

## Risk Register

- R1 — PCI emergency-change provision use (V4 hotfix). Mitigation: same evidence quality as standard board review; documented as transitional pending Week 4-5 durable deployment.
- R2 — Stabilization may mask root cause (V1 concern). Mitigation: parallel telemetry hardening Week 0-1; RCA hypothesis-testing runs through Week 5.
- R3 — Key-id-in-header is merchant-facing payload change (V2 concern). Mitigation: PCI board submission Week 0 with non-breaking default; opt-in or transparent variant decided by board.
- R4 — Legal sign-off SLA (5 days) on critical path (V3 concern). Mitigation: weekly batching; Tuesday EOD engineering output deadline.
- R5 — Customer success goes off-message before RCA signed (V5 concern). Mitigation: single comms channel + joint artifact; customer success accepts the constraint at kickoff.
- R6 — Q2 multi-region failover work conflict (seed brief). Mitigation: incident commander owns merge; week-0 joint design checkpoint.
- R7 — Scope creep past Apr 12 (V2 concern). Mitigation: hard deferral list (circuit breaker, HPA permanence) in scope-class table.

## Open / Deferred Questions

- O1 — HPA pin-up permanence (Q2 decision).
- O2 — Key-id-in-header opt-in vs. transparent (PCI board decision).
- O3 — Per-merchant circuit breaker timeline (Q2 decision).
- O4 — Retry-amplification root cause: our policy vs. merchant-side load (resolves via telemetry from Lane B).

## Convergence Note

Convergence score 0.79 against the 0.75 target. Synthesis is genuine — no single variant's stance is overruled; each contributes load-bearing structure.
