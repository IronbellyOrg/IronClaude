# Variant 3 — sonnet:security (Compliance + Evidence Workstream Design)

**Stance:** The forcing function for this program is auditor sign-off and PCI DSS Level 1 change discipline. Engineering choices that ignore the evidence-collection model will fail at the Apr 12 gate even if they succeed technically.

## Proposed Program Structure

1. **Week 0 — Evidence-collection harness up front.** Stand up a dedicated `incident-q1-2026/` artifact repository with controlled access. Every change record, test result, RCA draft, and signed approval lands here with immutable timestamps. SOC 2 auditor will be granted read access at week 6.
2. **Week 0-1 — PCI scope mapping.** Classify every proposed remediation by whether it touches payload signing or replay-protection state. Submit week-1 changes to secure-change-review board no later than Day 3 to clear the 2-week lead time.
3. **Week 1-4 — Remediation execution (gated by scope class).**
   - Out-of-scope changes (telemetry, HPA tuning) deploy normally.
   - In-scope changes (key-rotation safety harness, any HMAC-related work) follow secure-change-review board cadence.
4. **Week 4-6 — Independent verification.** Security engineering runs a parallel verification of every preventive-control deployment; produces test evidence in the artifact repo.
5. **Week 6-8 — Auditor narrative + sign-off.** RCA + control deployment records + verification evidence delivered to auditor before Apr 12. VP Engineering + Director of Security co-sign.

## Risks Foregrounded

- 2-week PCI lead time eats one-quarter of the program calendar — change-batching is mandatory.
- Independent verification capacity is finite (security engineering is 4 FTE) — must protect their bandwidth.
- Customer-facing comms must be legal-reviewed; legal sign-off SLA (5 days) is on the critical path.

## Why This Wins

- Apr 12 auditor gate is the binary success criterion that determines whether the program "counts."
- Defends against the regulatory-inquiry worst case (PSD2 operational-resilience guidance) by demonstrating disciplined response.
- Generates artifacts that have residual value beyond Q1 — they become the template for the next incident.

## Why This Could Lose

- Pure compliance optimization can starve the engineering hardening work; needs explicit allocation.
- May feel slow to customer-success and engineering, creating internal political friction.
