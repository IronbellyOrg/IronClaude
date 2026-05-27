# Base Selection

## Decision

**Base variant:** Variant 4 (haiku:devops — stabilization-first) elected as merge base.

## Rationale

The merge target is a Q1 incident-response program with three binding deadlines (Mar 28 change-freeze, Apr 12 auditor sign-off, 14 consecutive business days of >=99.9% delivery). Backsolving from the validation window deadline, stabilization must reach >=99.9% no later than Week 3 — and the only variant that proposes a credible Week 0-3 stabilization sequence is Variant 4. Variant 1 (analyzer) explicitly defers stabilization to post-RCA, which makes the validation window infeasible. Variant 2 (architect) does propose Week 1-2 quick wins but treats them as secondary to the key-id-in-header work. Variant 3 (security) and Variant 5 (scribe) are cross-cutting and not standalone calendar spines.

Variant 4 is also the variant most directly aligned to the dominant near-term risk (SLA credit run-rate, enterprise renewal threat), and its proposed PCI emergency-change approach for the key-rotation hotfix is the only path that gets a key-rotation safety mechanism into production inside the 8-week window without waiting for the full key-id-in-header overhaul.

The merge will overlay:

- Variant 1's telemetry hardening as a parallel Week 0-1 lane (precondition for defensible RCA without delaying stabilization).
- Variant 2's key-id-in-header as the durable fix, submitted to PCI board Week 0 and landing Week 4-5 after the Variant 4 hotfix has already stabilized delivery.
- Variant 3's PCI scope mapping + artifact repository as the calendar discipline layer.
- Variant 5's artifact spine + single-comms-channel cadence as the political risk hedge.

## Alternative Considered

Variant 2 (architect) was the leading alternative — it has the strongest durable-engineering story. Rejected as base because its Week 0-1 sequencing relies on joint design with the Q2 multi-region team, which introduces calendar coupling we cannot control inside this program. Variant 2's content is preserved as the durable-fix overlay.
