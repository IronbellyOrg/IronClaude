# Variant 5 — sonnet:scribe (Narrative + Comms Workstream Design)

**Stance:** Q14 in the seed brief is right — the most likely program failure is political, not technical. The program will be judged in three audiences (auditor, merchants, internal VPs) by the quality of three artifacts: the RCA narrative, the merchant-comms package, and the steerco status report. Every engineering choice should be made with those artifacts in mind from Day 0.

## Proposed Program Structure

1. **Week 0 — Artifact spine.** Stand up three template artifacts on Day 1: (a) RCA narrative skeleton with sections for problem, evidence, root cause, remediation, prevention; (b) merchant comms template with legal-pre-reviewed boilerplate; (c) weekly steerco status template with RAG indicators and SLA-credit run-rate.
2. **Week 0-1 — Stakeholder map + comms cadence.** Decide who owns each audience: incident commander -> internal VPs; head of merchant success + legal -> merchants; security engineering lead + SOC 2 PM -> auditor. Lock the cadence: weekly to merchants, weekly to VPs, milestone-based to auditor.
3. **Week 1-7 — Continuous artifact maintenance.** Engineering workstreams feed evidence into the RCA and merchant comms artifacts weekly. Legal sign-off SLA (5 days) is on the comms artifact, batched weekly to avoid burning the legal team.
4. **Week 7-8 — Final artifact freeze.** RCA signed by VP Engineering; merchant comms finalized; auditor bundle delivered.

## Risks Foregrounded

- Narrative-first risk: writing the conclusion before the evidence is available. Mitigation: artifact skeletons remain skeletons until RCA evidence lands; no premature commitment.
- Legal SLA pressure: 5-day sign-off on weekly comms means engineering output must hit Tuesday EOD to clear by Friday.
- Customer-success risk: direct merchant communications without legal sign-off creates exposure. Single comms channel is mandatory.

## Why This Wins

- Addresses the dominant failure mode (political, not technical).
- Forces engineering to articulate findings continuously, surfacing ambiguity early instead of at week 7.
- Produces durable templates for future incidents.

## Why This Could Lose

- Risk of optimising for narrative over substance — could erode engineering trust.
- Heavy templating overhead in Week 0 may feel like bureaucratic drag to engineering workstreams.
