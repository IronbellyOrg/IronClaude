---
convergence_score: 0.68
rounds_completed: 2
---

# Structured Adversarial Debate: Opus vs Haiku Roadmap Variants

## Round 1: Initial Positions

### Variant A (Opus) — Opening Position

**On granularity and risk coverage:** 122 tracked items versus 83 is not overhead — it is traceability. Security-critical auth at complexity 0.78 with SOC2 and GDPR obligations demands decomposition. Per-metric observability tasks (OBS-001..009) let a reviewer confirm each alert rule exists before GA; bundling them obscures gaps. The 20-entry risk register catches frontend-specific failure modes (R-010 clock skew, R-017 admin PII, R-020 flag sprawl) that disappear when risks are aggregated.

**On operational hardening:** TOKEN-STUB in M2 is the correct sequencing. It decouples M2's login logic from Redis/JWT readiness, so if any piece of M3 slips, M2 value still ships. OBS-ROLLBACK-TRIGGERS with automated flag flips is non-negotiable at 99.9% SLA — human-gated rollback during a Sunday 3am incident costs uptime budget. RSA-KEY-ROTATION as a dedicated deliverable with overlap script addresses R-006 before the first rotation, not after an incident. DATA-MIG-SCRIPT protects against the "we forgot legacy users exist" class of bug.

**On timeline:** 11 weeks with a 3-day post-GA buffer absorbs Phase 2 beta surprises. Zero-slack plans against a fixed GA date are brittle.

**On OQ-PRD-2:** Unlimited-with-metric-observation preserves multi-device UX for power users; adding a cap now based on unmeasured behavior is premature optimization.

### Variant B (Haiku) — Opening Position

**On density and signal-to-noise:** 83 deliverables is not undersized — it is the minimum required to deliver the same functional outcome. Every item Opus adds beyond this is overhead: review cycles, status meetings, dependency-graph maintenance. Fine-grained decomposition creates the *illusion* of rigor while increasing the chance that reviewers miss the forest. The compact 10-row risk register and 6-row Decision Summary table are consumable by executives in five minutes; Opus's narrative ADRs and 20-risk register get skimmed.

**On conflict resolution:** Haiku explicitly resolves CONFLICT-2 (register auto-login) by honoring the TDD API contract and redirecting to LoginPage. Opus leaves this implicit — a reader of the roadmap cannot determine what happens on registration without cross-referencing two documents. Explicit resolution of contract collisions is a core roadmap responsibility.

**On admin completeness:** API-008/009/010 (query + lock + unlock) is the complete operational set Jordan needs for incident response. Opus ships ADMIN-001 query-only and omits the lock/unlock controls that the PRD incident-management story implies. Query without action is half a feature.

**On OQ-PRD-2:** Capping at 5 refresh tokens per user bounds Redis memory deterministically and improves revocation semantics. "Unlimited and observe" means Redis sizing is open-ended, and the first time a compromised user has 40 live refresh tokens across devices, revoke-all becomes operationally messy.

**On timeline:** 10 weeks aligned exactly with TDD commitments is the disciplined plan. Buffers invite scope creep.

## Round 2: Rebuttals

### Variant A (Opus) — Rebuttal

**On density:** Haiku's compactness is readability, not completeness. The admin scope Haiku rightly calls out (lock/unlock) is *exactly* the kind of gap that appears when decomposition is shallow — Opus missed it because admin was bundled into one task rather than decomposed into query/lock/unlock. The fix is not fewer items, it is better decomposition. Point conceded: Opus should add lock/unlock to ADMIN-001 scope.

**On CONFLICT-2:** Fair criticism. Opus's register flow implicitly follows the TDD contract but does not call out the PRD divergence. This is an actual gap — Opus should add an explicit CONFLICT-2 resolution note. However, Haiku's resolution ("TDD prevails, redirect to LoginPage") is arguably the weaker product outcome; PRD's auto-login expectation exists for conversion reasons. Both should flag this for v1.1 product review.

**On OQ-PRD-2:** Haiku's cap of 5 is a number without evidence. Where does 5 come from? A user with a phone, laptop, work laptop, tablet, and partner's device already hits the cap. The disciplined move is to deploy the metric first and set the cap in v1.1 based on observed p95 device count. Premature caps cause churn support tickets.

**On timeline buffer:** "Buffers invite scope creep" is a cultural claim, not a technical one. Buffers absorb known-unknowns. A 3-day buffer on an 11-week plan with a pen-test dependency on an external vendor is prudent risk management.

### Variant B (Haiku) — Rebuttal

**On operational hardening:** TOKEN-STUB is throwaway code. Throwaway code accumulates technical debt and creates code paths that must be tested and then deleted. Implementing the real TokenManager in M2 is not coupling — it is completing the work once. If Redis is a blocker, that is an infrastructure scheduling problem, not a sequencing problem. M1 provisions Redis; M2 should use it.

**On automated rollback:** Automated flag flips sound sophisticated but are dangerous at GA for a new service with no production baseline. False positives during a legitimate traffic spike will flip flags unnecessarily, creating user-visible regressions. Human-gated rollback with clear triggers is the more mature posture for the first 30 days. Automate later, once alert noise is characterized.

**On risk register size:** A 20-entry register where half the entries are Low/Low severity is noise. R-020 "feature flag sprawl" and R-017 "admin PII exposure" are real concerns but belong in ongoing ops hygiene, not the launch risk register. Haiku's 10 entries are the ones that can actually kill the launch.

**On granularity counter:** Opus concedes Haiku caught the admin lock/unlock gap — that *is* the point. Granularity does not catch gaps; clear functional thinking does. Opus decomposed observability into nine tasks but still missed admin completeness. Decomposition is not a substitute for requirement coverage.

**On OQ-PRD-2:** "Evidence-based" cuts both ways. No evidence supports unbounded Redis keys per user either. The cap of 5 is a reversible default: raise it if metrics show legitimate multi-device users clustering above it. Unlimited is the harder-to-reverse choice once users rely on many active sessions.

## Convergence Assessment

**Areas of strong agreement (high convergence):**
- Both variants converge on all 18 shared assumptions: complexity class, GA date, crypto choices, stores, transport, rollout phasing, coverage gate, NFR targets.
- Both resolve OQ-CONFLICT-1 (audit retention 12 months), OQ-PRD-3 (lockout 5/15min), OQ-PRD-4 (defer remember-me), OQ-001 (defer API-key), OQ-PRD-1 (async password reset) identically.
- Both add the missing `/auth/logout` endpoint as a PRD-gap-fill.

**Areas where Round 2 produced alignment:**
- Opus concedes admin scope should include lock/unlock (adopting Haiku's API-009/010).
- Opus concedes CONFLICT-2 should be explicitly resolved in the roadmap (adopting Haiku's pattern).
- Both agree a refresh-token cap is reversible policy; disagreement is over default value and timing.

**Remaining genuine disputes:**
1. **TOKEN-STUB vs real TokenManager in M2:** unresolved — engineering-culture question (ship-incrementally vs build-once).
2. **Automated vs human-gated rollback:** unresolved — operational-maturity question (Haiku's "automate after baseline" is defensible; Opus's "automate before incident" is also defensible).
3. **Refresh-token cap at 5 vs unlimited-with-metric:** unresolved — product/infra tradeoff awaiting data.
4. **Timeline buffer (3-day vs zero-slack):** unresolved — risk-tolerance question.
5. **Granularity level (122 vs 83 items):** partial — both acknowledge Opus's decomposition missed admin completeness, weakening the "more items = more coverage" claim; but Opus's observability/key-rotation/migration-script decomposition does add genuine operational value.

**Recommended merge posture:** Adopt Haiku's explicit CONFLICT-2 resolution, admin lock/unlock endpoints, and refresh-token cap as a reversible default. Adopt Opus's OBS-ROLLBACK-TRIGGERS (but flag as human-confirmed for first 30 days per Haiku's concern), RSA-KEY-ROTATION deliverable, DATA-MIG-SCRIPT, FE-CLOCK-SKEW, ASYNC-QUEUE, and the expanded risk register. Resolve TOKEN-STUB by committing to the real TokenManager in M2 if Redis provisioning holds on schedule, with TOKEN-STUB as a documented fallback if M1 infra slips. Keep the 3-day post-GA buffer; it costs nothing if unused.
