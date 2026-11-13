# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | interaction_effects | If the timeline becomes unreadable after the PR is already draft, the run keeps the PR draft, continues pushing and reports held | UNADDRESSED | MEDIUM | source.md:67; TASK-WF-designSpec-20261107-075614.md:129,166-173 (AC covers unreadability at engage only) |
| INV-002 | sufficiency_challenge | User docs explain default-on at monitor 3 and what held means | UNADDRESSED | LOW | source.md:245; plan:195-199 (AC checks usage entry, clear command, release-gate statement only) |
| INV-003 | sufficiency_challenge | Passing the scenario tests proves the production orchestration applies the pure decisions in the required order | UNADDRESSED | MEDIUM | plan:166-173; source.md:15,257-280 (the driver applies the decisions itself) |

## Summary
- Total findings: 3
- ADDRESSED: 0
- UNADDRESSED: 3 (HIGH 0, MEDIUM 2, LOW 1)
