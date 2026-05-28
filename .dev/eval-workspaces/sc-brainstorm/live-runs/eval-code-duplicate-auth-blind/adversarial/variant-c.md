---
variant_id: C
advocate: Agent C
blind_mode: true
---

# Variant C — Highest-Coverage-Wins Baseline

## Approach

Select the legacy module with the strongest existing test coverage and hardening
posture as the canonical baseline. Port the missing behaviours from the other
two modules into it. Retire the two non-selected modules.

## Required Components

1. Coverage audit across the three modules (line, branch, mutation if
   available).
2. Hardening-posture audit (password hash algorithm and parameters, MFA
   enforcement, session timeout, audit-log completeness).
3. Per-module behavioural-equivalence matrix listing every behaviour the two
   non-selected modules carry that is not present in the baseline.
4. Port-and-test plan for each missing behaviour.
5. Retirement plan for the two non-selected modules including data and
   session-state migration.

## Risks

- Coverage is a proxy, not a guarantee of correctness.
- The selected baseline may codify an incident-derived bug.

## Mitigations

- Selection criteria include a written behavioural-equivalence audit, not
  coverage alone.
- Every incident-derived test case is re-validated against the canonical
  module, not assumed correct.
