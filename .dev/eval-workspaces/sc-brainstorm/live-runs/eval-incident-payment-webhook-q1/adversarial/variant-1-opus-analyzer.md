# Variant 1 — opus:analyzer (RCA-First Workstream Design)

**Stance:** Stabilize via instrumentation-first; the RCA must precede structural fixes so we do not deploy remediation that is not aimed at the actual root cause. The auditor cares more about a defensible causal chain than fast stabilization.

## Proposed Program Structure

1. **Week 0-1 — Telemetry hardening.** Add signing-key-version trace tag, per-merchant retry-amplification metric, egress DNS histogram, replay-attempt fan-out visualization. No production behavior changes. SOC 2 evidence: change records for telemetry deploys.
2. **Week 1-3 — RCA cone-of-evidence.** Three parallel investigation tracks: (a) HMAC key-rotation race window in worker cache; (b) HPA scale-down cold-start under morning ramp; (c) merchant-side amplification under our retry policy. Each track produces a falsifiable hypothesis + telemetry that rules it in or out.
3. **Week 3-5 — Targeted remediation.** Build only the controls justified by RCA evidence. Two preventive controls already mandated: per-merchant SLO alerting; key-rotation safety harness. Other controls deferred to Q2 unless evidence forces them in.
4. **Week 5-7 — Validation window.** 14 consecutive business days at >=99.9% delivery. Daily review against SLO dashboard.
5. **Week 7-8 — Auditor packaging + merchant comms.** RCA signed by VP Engineering; merchant-facing comms reviewed by legal; artifact bundle to SOC 2 auditor before Apr 12.

## Risks Foregrounded

- Telemetry-first delays stabilization by ~1 week; SLA credit exposure continues at ~$180K/week.
- RCA may be inconclusive (multi-causal); plan must accept that ambiguity in the auditor narrative.
- HPA cold-start hypothesis is hardest to test — requires controlled morning-ramp experiment without harming live traffic.

## Why This Wins

- Maximises auditor credibility: every remediation traceable to evidence.
- Minimises wasted engineering — no remediation built against a wrong hypothesis.
- Compatible with PCI DSS lead time: telemetry changes do not trigger secure-change-review board.

## Why This Could Lose

- Slower visible relief for affected merchants. Customer-success may overcommit on comms before RCA is signed.
- Burns engineering hours on instrumentation that may not survive into Q2.
