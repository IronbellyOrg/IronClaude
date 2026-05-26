# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

| ID      | Category               | Assumption                                                                                                          | Status     | Severity | Evidence                                                                                                       |
|---------|------------------------|---------------------------------------------------------------------------------------------------------------------|------------|----------|----------------------------------------------------------------------------------------------------------------|
| INV-001 | state_variables        | Frontend team capacity exists when V1 M3 + V2 M4 demand it; consensus picks V1 M3 timing, no resolution of A-003     | UNADDRESSED | HIGH     | diff-analysis.md A-003; V1 line 193 only mentions "frontend-team representative"; no headcount commitment       |
| INV-002 | state_variables        | SOC2 compliance reviewer available for M4 audit-log control-mapping sign-off; reviewer not booked or named           | UNADDRESSED | HIGH     | V1 line 146; V2 line 217; source spec line 89 SOC2 Q3 2026 dependency                                          |
| INV-003 | guard_conditions       | ASCII `.toLowerCase()` email normalization is sufficient; Unicode/IDNA/whitespace cases not guarded                  | UNADDRESSED | MEDIUM   | V1 line 206; V2 D1.3 line 54; source spec §Error Handling line 372                                              |
| INV-004 | guard_conditions       | Email+IP composite lockout key prevents distributed DoS; attacker rotating IP per request bypasses lockout entirely  | UNADDRESSED | HIGH     | V1 line 215; FR-AUTH-001 AC4 source line 652 specifies lockout per 5 attempts without IP partitioning           |
| INV-005 | guard_conditions       | Refresh-token rotation is atomic; flagged as risk note in V1 but not promoted to deliverable acceptance criterion   | UNADDRESSED | HIGH     | V1 line 121 (risk text only); no corresponding test in V1 exit criteria 111-117 nor V2 validation 87-95         |
| INV-006 | count_divergence       | 5-minute k6 run validates 99.9%/30-day SLO; insufficient duration for slow leaks, cache pollution, audit-log bloat   | UNADDRESSED | MEDIUM   | V1 line 138 vs source spec NFR-PERF-002 line 665                                                                |
| INV-007 | count_divergence       | 11-day M5 window accommodates pen-test + remediation + 4-stage rollout + 2-day buffer; arithmetic is infeasible       | UNADDRESSED | HIGH     | V1 lines 159-186 timeline; V1 line 214 ("2-week remediation") vs V1 line 183 (2-day buffer) self-contradiction  |
| INV-008 | count_divergence       | "99.9% uptime over first 7 days" is a GA-exit gate; actually measures retroactively GA+7, can't slip GA right        | UNADDRESSED | MEDIUM   | V2 line 231; V2 line 170; no rollback trigger for days 1-7 SLO breach                                          |
| INV-009 | collection_boundaries  | `revokeAll` is O(log N) on unlimited tokens/user; V1 keys by `{userId}:{tokenHash}` requires enumeration              | UNADDRESSED | MEDIUM   | V1 line 265 ("unlimited within 7-day TTL"); V1 D3.1 line 104 keying; V2 D3.5 line 110 no perf budget            |
| INV-010 | collection_boundaries  | JwtService handles single-key boot case (kid lookup before first rotation); pre-rotation state unspecified           | UNADDRESSED | LOW      | V1 line 275 OQ-7 discusses post-rotation only; V2 D2.1 line 78 no kid mention                                  |
| INV-011 | interaction_effects    | bcrypt + audit-log INSERT contend on same pg-pool; horizontal scaling multiplies pg clients past PG max (200)        | UNADDRESSED | HIGH     | V1 line 49 (pool 500) + V1 line 154 + V1 line 212 vs source spec line 1212 (PG cap 200)                        |
| INV-012 | interaction_effects    | Rate-limit (429) + lockout (423) + CAPTCHA (200-with-challenge) status-code interaction; frontend handles 401 only   | UNADDRESSED | MEDIUM   | V1 134-135 vs V2 R-002 line 214 (CAPTCHA only in V2 risk matrix, not deliverable); FE V1 D3.5 / V2 D4.1 401-only |
| INV-013 | interaction_effects    | 4-stage rollback "honors refresh tokens" while password-reset revokeAll fires; contracts directly contradict          | UNADDRESSED | HIGH     | V1 line 184 ("honor refresh tokens") vs V1 line 132 (revokeAll on reset); source spec FR-AUTH-005 AC + R-001     |

## Summary

- **Total findings**: 13
- **ADDRESSED**: 0
- **UNADDRESSED**: 13
  - HIGH: 7 (INV-001, INV-002, INV-004, INV-005, INV-007, INV-011, INV-013)
  - MEDIUM: 5 (INV-003, INV-006, INV-008, INV-009, INV-012)
  - LOW: 1 (INV-010)

## Convergence Gate Impact

Per `convergence_detection.invariant_probe_gate`:

```
CONVERGENCE BLOCKED: 7 HIGH-severity UNADDRESSED invariant(s) detected
Blocking items: INV-001, INV-002, INV-004, INV-005, INV-007, INV-011, INV-013
```

Diff-point convergence reached 0.806 (just over 0.80 threshold), but HIGH invariants block declaration of CONVERGED state. Pipeline proceeds with `status: partial`. These 7 items are promoted to required additions in the refactor plan (Step 4).

## Sufficiency Challenges to Emerging Consensus (Category 6)

**Consensus A** (V1 wins on architectural depth):

- Downstream falsifier: V1's email+IP composite lockout (INV-004) violates FR-AUTH-001 AC4 against any attacker with >1 IP. Adopting V1's depth without per-email backstop ships a regression.
- Downstream falsifier: log-scrubber gate (V1 D4.8) catches logged credentials but not timing-channel enumeration; FR-AUTH-001 AC3 requires constant-time verify which neither variant test-gates.

**Consensus B** (V2 wins on measurement/traceability):

- Downstream falsifier: V2's metrics table has 8/12 "baseline: N/A (greenfield)" — un-actionable without M1 baseline measurement which V1's M1 (no feature code) cannot provide.
- Downstream falsifier: V2's OQs front-load resolution by M3 start but several block M3 deliverables; escalation path is undefined beyond "escalate to eng-manager".

**Consensus C** (Merge ~60% V1 / 40% V2):

- Downstream falsifier: V1's M1 ships no feature code but V2's Success Metrics table requires baseline measurements; embedding leaves baselines un-measurable until M2.
- Downstream falsifier: V1's 5-workstream parallel model is incompatible with V2's single-team sprint cadence; merging structure-only leaves owner cells empty.

**Consensus D** (GA date 2026-06-09 firm; quality gates non-negotiable; date is dependent variable):

- Downstream falsifier: INV-007 — V1's M5 arithmetic doesn't fit pen-test + remediation + 4-stage rollout inside 11 days. The triple D+F+gates is inconsistent.
- Downstream falsifier: V2's "99.9% over first 7 days" gates at GA+7; date is not actually firm.

**Consensus E** (bcrypt 12 mandated; horizontal scaling is contingency):

- Downstream falsifier: INV-011 — horizontal scaling multiplies pg-pool past PostgreSQL connection cap; PgBouncer/read-replica absent.
- Downstream falsifier: bcrypt runs in libuv threadpool (default 4 threads); per-pod queueing dominates p95 above 4 concurrent. UV_THREADPOOL_SIZE tuning absent.

**Consensus F** (SOC2 Q3 2026 audit drives GA 2026-06-09):

- Downstream falsifier: SOC2 Type II requires minimum 6-month operating effectiveness observation window; 2026-06-09 GA + early-Q3 audit gives ~3 weeks of operating history, insufficient for Type II. Audit may be Type I, or GA must move earlier.
- Downstream falsifier: INV-002 — SOC2 control mapping sign-off requires named compliance reviewer; neither variant books one.
