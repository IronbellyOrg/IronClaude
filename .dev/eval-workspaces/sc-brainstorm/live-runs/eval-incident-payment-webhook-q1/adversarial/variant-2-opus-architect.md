# Variant 2 — opus:architect (Structural Hardening Workstream Design)

**Stance:** This is not a one-off incident — it is a structural debt collection event. The program must deliver durable architectural controls that prevent the same class of failure (key-rotation races, HPA cold-start, per-tenant noisy-neighbor) from recurring across Q2 multi-region failover and beyond. The RCA is necessary but not sufficient.

## Proposed Program Structure

1. **Week 0-1 — Joint design with Q2 multi-region team.** Avoid the political failure mode where stabilization conflicts with the in-flight failover work. Produce a shared architectural roadmap with explicit interface contracts.
2. **Week 1-2 — Stabilization quick wins (parallel).** Increase HPA min-replicas during European morning ramp (no PCI scope); raise per-merchant connection-pool ceilings for top-50 merchants by volume.
3. **Week 2-5 — Durable controls (canonical):**
   - **Key-id-in-header pattern** (HMAC-SHA256 with explicit `X-Webhook-Key-Id`) — eliminates the worker-cache race by making key version explicit in payload. Goes through secure-change-review board on week-2 submission, deploys week-5.
   - **Per-merchant SLO alerting** with bounded alert-fatigue budget; SLO bounds tuned against 14-day baseline.
   - **Per-merchant circuit breaker** preventing one merchant's degradation from consuming worker pool capacity.
4. **Week 5-7 — Validation + chaos exercise.** Synthetic key-rotation failure injected in staging; controlled recovery exercise.
5. **Week 7-8 — Auditor packaging + handover to Q2 team.** Architectural decision records for each control.

## Risks Foregrounded

- Key-id-in-header is a payload change — merchants on legacy verification libraries may need an opt-in flag with deprecation timeline. Adds merchant-comms scope.
- Per-merchant circuit breaker risks under-delivering to flapping merchants who would have recovered with one more retry. Tuning is non-trivial.
- Joint design with Q2 team adds calendar risk if their roadmap shifts.

## Why This Wins

- Durable: same patterns extend to Q2 multi-region work.
- Auditor sees a credible "we prevent recurrence" narrative, not just "we fixed this one."
- Reduces blast-radius surface across the worker pool.

## Why This Could Lose

- Higher upfront scope; risk of missing the Apr 12 auditor deadline if scope creeps.
- Key-id payload change is a merchant-facing breaking change — even with opt-in, comms cost is real.
