# Variant 4 — haiku:devops (Stabilization-First Workstream Design)

**Stance:** Stop the bleeding first. SLA credit run-rate is $180K/week and four enterprise accounts are threatening renewal. The longer we sit in continuous SLO violation, the more political capital the program consumes before it even starts. Get to >=99.9% by Week 3 even with imperfect understanding, then harden behind the stabilization.

## Proposed Program Structure

1. **Week 0 — Operational triage.** Pin HPA min-replicas to peak-hour capacity across 07:00-10:00 UTC for the next 4 weeks (no PCI scope). Raise connection-pool ceilings on top-50 merchant routes. Increase retry budget with explicit jittered backoff cap to prevent retry-amplification.
2. **Week 0-1 — Key-rotation hotfix.** Force-flush worker key cache on Vault rotation event; add a defensive 30s grace window where workers accept both old and new key. Treat as P1 hotfix under PCI emergency-change provision (security-review post-hoc, evidence preserved).
3. **Week 1-3 — Validate stabilization.** Daily SLO review; expect >=99.9% by end of Week 2.
4. **Week 3-5 — Build durable preventive controls** (per-merchant SLO alerting; key-rotation safety harness as canary + automated rollback).
5. **Week 5-6 — RCA finalization** post-stabilization, drawing on telemetry collected during stabilization period.
6. **Week 6-7 — Auditor packaging.**
7. **Week 7-8 — Customer comms + 14-day validation window.**

## Risks Foregrounded

- PCI emergency-change provision has audit consequences if used carelessly. Must produce same evidence quality as standard board review, just post-hoc.
- Pinning HPA min-replicas costs ~$22K/month in cloud spend; defensible against $180K/week SLA exposure.
- Stabilization may mask the root cause, making Week 5-6 RCA harder. Telemetry hardening must accompany stabilization.

## Why This Wins

- Buys political capital with merchants and customer-success early.
- Reduces SLA credit exposure inside the program window.
- Makes the 14-day sustained validation window achievable inside the calendar.

## Why This Could Lose

- Acting before understanding risks deploying remediation that does not address root cause; auditor may flag "treated symptoms not causes."
- PCI emergency-change use must be justified — abuse erodes change-review credibility.
