# Base Selection: Hybrid Scoring Results

## Selected Base: Variant 1 (opus / default persona)

**Combined Score:** V1 = **0.993**, V2 = 0.881 (margin: 11.2%, no tiebreaker required)

---

## Quantitative Scoring (50% weight)

5 deterministic metrics computed from artifact text:

| Metric | Weight | V1 (opus) | V2 (sonnet) | Notes |
|--------|--------|-----------|-------------|-------|
| **RC** Requirement Coverage | 0.30 | 1.00 | 1.00 | Both cover 22/22 source IDs (12 FR + 6 NFR + 4 R) |
| **IC** Internal Consistency | 0.25 | 0.99 | 0.99 | V1: 0 contradictions; V2: 1 weak (revocation claim vs FR-004 implication) |
| **SR** Specificity Ratio | 0.15 | 0.92 | 0.84 | V1 names libs+params throughout (python-jose, authlib, pyotp, slowapi, Argon2id m=64MB t=3 p=4, RTO 1hr/RPO 5min); V2 names some + uses more hedge-language |
| **DC** Dependency Completeness | 0.15 | 1.00 | 1.00 | All internal references resolve in both variants |
| **SC** Section Coverage | 0.15 | 1.00 | 0.923 | V1: 13 H2 sections (incl. Sprint Layout appendix); V2: 12 H2 sections |

**Quant Formula:** quant_score = (RC × 0.30) + (IC × 0.25) + (SR × 0.15) + (DC × 0.15) + (SC × 0.15)

- **quant_V1** = (1.00 × 0.30) + (0.99 × 0.25) + (0.92 × 0.15) + (1.00 × 0.15) + (1.00 × 0.15) = **0.985**
- **quant_V2** = (1.00 × 0.30) + (0.99 × 0.25) + (0.84 × 0.15) + (1.00 × 0.15) + (0.923 × 0.15) = **0.962**

---

## Qualitative Scoring (50% weight) — 30-Criterion Additive Binary Rubric

Claim-Evidence-Verdict format (abbreviated as CEV per row).

### Completeness (5 criteria)

| # | Criterion | V1 | V1 Evidence | V2 | V2 Evidence |
|---|-----------|----|----|----|----|
| 1.1 | All explicit source requirements covered | MET | 12/12 FR, 6/6 NFR, 4/4 R in coverage matrix (lines 346-365) | MET | 12/12 FR, 6/6 NFR, 4/4 R (lines 340-364) |
| 1.2 | Edge cases & failure scenarios addressed | MET | D5.2 chaos, D5.7 IR playbook, D3.2 OAuth fallback, family-rotation reuse detection | MET | D2.7 circuit breaker, D3.8 lockout, D4.6 reactivation grace |
| 1.3 | Dependencies & prerequisites included | MET | Per-milestone Dependencies section + external prereqs (PostgreSQL, Redis, SendGrid, KMS) | MET | Per-milestone Dependencies section |
| 1.4 | Success/completion criteria defined | MET | Per-milestone Acceptance Criteria with measurable thresholds | MET | Per-milestone Acceptance Criteria |
| 1.5 | Explicitly out-of-scope items specified | MET | Out of Scope section + extension points + additional clarifications (no SMS, no SAML) | MET | Out of Scope + future-consideration items |

**Completeness V1: 5/5 | V2: 5/5**

### Correctness (5 criteria)

| # | Criterion | V1 | V1 Evidence | V2 | V2 Evidence |
|---|-----------|----|----|----|----|
| 2.1 | No factual errors / hallucinations | MET | "OWASP 2025 recommendation" for Argon2id matches OWASP Password Storage Cheat Sheet | MET | bcrypt cost-12 is OWASP-acceptable; PKCE for OAuth is correct |
| 2.2 | Technical approaches feasible | MET | Bloom-filter <0.1% FP at 100k jti is empirically achievable; Argon2 250ms calibration realistic | MET | Redis sliding-window O(1) per request is feasible |
| 2.3 | Terminology consistent | MET | "denylist", "refresh-token family", "Argon2id" used uniformly | MET | "audit_events", "RBAC", "JWT", "RS256" uniform |
| 2.4 | No internal contradictions | MET | 0 contradictions found in cross-scan | NOT MET | "No revocation list needed for access tokens" (Cross-Cutting / Performance) contradicts FR-004 RBAC requirement for role-change responsiveness |
| 2.5 | Claims supported by evidence | MET | "IETF OAuth 2.0 Security BCP", "GDPR Article 12", "OWASP 2025", "RFC 6238" citations | MET | Justifications present in Opinionated Choices section but lighter citation density |

**Correctness V1: 5/5 | V2: 4/5**

### Structure (5 criteria)

| # | Criterion | V1 | V2 |
|---|-----------|----|----|
| 3.1 | Logical section ordering | MET — exec summary → overview → milestones → cross-cutting → mappings → out of scope → sprint appendix | MET — exec summary → milestones → cross-cutting → risk → success → out of scope → timeline → opinionated choices |
| 3.2 | Consistent hierarchy depth | MET — H1/H2/H3 only, no orphans | MET — H1/H2/H3 only |
| 3.3 | Clear separation of concerns | MET — Cross-Cutting is distinct from Milestones | MET — same |
| 3.4 | Navigation aids present | MET — Milestone Overview table, FR/NFR Coverage Matrix, Sprint Layout | MET — Timeline Summary ASCII, FR Coverage Matrix, NFR Coverage Matrix |
| 3.5 | Follows artifact-type conventions | MET — roadmap conventions (M-ID, D-ID, acceptance criteria) | MET — same conventions |

**Structure V1: 5/5 | V2: 5/5**

### Clarity (5 criteria)

| # | Criterion | V1 | V2 |
|---|-----------|----|----|
| 4.1 | Unambiguous language | MET — precise throughout | MET — mostly precise; minor hedge ("argue equivalence from architecture" in D5.6) but does not dominate |
| 4.2 | Concrete rather than abstract | MET — specific libs, params, URLs | MET — concrete on most items |
| 4.3 | Each section has clear purpose | MET — Goal/Outcome explicit per milestone | MET — Goal explicit per milestone |
| 4.4 | Acronyms defined or standard | MET — standard auth/security terms | MET — same |
| 4.5 | Actionable next steps identified | MET — Acceptance Criteria as checkboxes | MET — same |

**Clarity V1: 5/5 | V2: 5/5**

### Risk Coverage (5 criteria)

| # | Criterion | V1 | V2 |
|---|-----------|----|----|
| 5.1 | ≥3 risks with prob+impact | MET — 4 risks + residual-risk column | MET — 4 risks with prob/impact |
| 5.2 | Mitigation strategy per risk | MET — per-risk in Risk Register | MET — same |
| 5.3 | Failure modes & recovery procedures | MET — D5.5 DR runbook (RTO 1hr/RPO 5min), D5.7 IR playbook with 72-hr GDPR timeline, D5.2 chaos drill | NOT MET — no DR runbook with targets, no IR playbook, no chaos drill |
| 5.4 | External dependency failure scenarios | MET — D3.8 OAuth health check, D5.2 Redis failover drill, OAuth provider /healthz signal | MET — D2.7 OAuth circuit breaker |
| 5.5 | Monitoring/validation mechanism | MET — D5.3 SLO dashboard with security signals (refresh-token reuse rate, failed-login rate) | MET — D5.9 Prometheus+Grafana+PagerDuty with p95/error-rate alerts |

**Risk Coverage V1: 5/5 | V2: 4/5**

### Invariant & Edge Case Coverage (5 criteria — floor: ≥1/5 required for base eligibility)

| # | Criterion | V1 | V2 |
|---|-----------|----|----|
| 6.1 | Collection boundaries (empty, single, max) | MET — bloom-filter measured at 100k jti, k6 at 10K concurrent, per-event-type partial indexes for high-frequency events | NOT MET — no empty/single-element probing; no boundary tests on jwt-roles array, recovery-code count, or audit-query empty result |
| 6.2 | State variable interactions across boundaries | MET — admin role change → denylist propagation (D4.3); 2FA secret in KMS distinct from column key (D3.3); refresh-token family across crash via Redis AOF | NOT MET — refresh-token-family / 2FA / RBAC interactions not enumerated; no explicit cross-boundary state tracing |
| 6.3 | Guard condition gaps (input validation, type assumptions) | MET — D5.4 external pentest, D2.4 rate limit, D2.8 CSP, Pydantic v2 strict mode | MET — D3.11 OWASP hardening (CSP, X-Frame, input validation), D5.4 ZAP scan |
| 6.4 | Count divergence (off-by-one, inclusive/exclusive) | MET — explicit TTL semantics ("TTL = access-token TTL" for denylist), "10 single-use codes", recovery-code single-use enforcement test ("same code used twice returns 401") | NOT MET — "5 consecutive failed attempts" doesn't specify inclusive/exclusive counting; sliding-window-vs-token-bucket semantics for boundary cases unspecified |
| 6.5 | Interaction effects when features combine | MET — D4.3 token+role-change interaction, D5.2 component-failure interactions in chaos drill, OAuth+2FA implicit but addressed by 202 response pattern | NOT MET — no chaos drill, no explicit interaction tests, OAuth+2FA interaction unpinned, deactivation-during-active-token race unaddressed |

**Invariant V1: 5/5 | V2: 1/5**

**Edge case floor check:** V2 = 1/5 = exactly at floor (≥1/5 required). V2 **is eligible** as base variant (floor not violated). V1 is well above floor.

### Qualitative Summary

| Dimension | V1 (opus) | V2 (sonnet) |
|-----------|-----------|-------------|
| Completeness | 5/5 | 5/5 |
| Correctness | 5/5 | 4/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 5/5 | 5/5 |
| Risk Coverage | 5/5 | 4/5 |
| Invariant & Edge Case | 5/5 | 1/5 |
| **Total** | **30/30** | **24/30** |

- **qual_V1** = 30/30 = **1.00**
- **qual_V2** = 24/30 = **0.80**

---

## Position-Bias Mitigation (Dual Pass)

Per protocol AC: evaluate in input order (V1, V2) and reverse order (V2, V1). Both passes used the same 30-criterion rubric with CEV.

**Result:** Dual-pass produced identical verdicts on all 30 criteria for both variants. 0 disagreements requiring re-evaluation.

| Pass | V1 score | V2 score |
|------|----------|----------|
| Pass 1 (input order) | 30/30 | 24/30 |
| Pass 2 (reverse order) | 30/30 | 24/30 |
| Agreement | full | full |

The 30-criterion binary additive rubric with mandatory evidence citation is deterministic for these variants — position bias did not surface.

---

## Combined Scoring

**Formula:** `variant_score = (0.50 × quant_score) + (0.50 × qual_score)`

| Variant | quant × 0.50 | qual × 0.50 | **Combined** |
|---------|--------------|-------------|--------------|
| V1 (opus) | 0.4925 | 0.500 | **0.9925** |
| V2 (sonnet) | 0.481 | 0.400 | **0.881** |

**Margin:** 0.9925 − 0.881 = **0.1115 (11.2%)** — well above 5% tiebreaker trigger; **no tiebreaker required**.

---

## Selected Base: Variant 1 (opus / default persona)

### Selection Rationale

Variant 1 wins by a substantial margin (11.2%) on the combined score. The decisive differentiators are:

1. **Invariant & edge-case coverage (5/5 vs 1/5)** — V1 explicitly addresses collection boundaries (bloom-filter, k6 load), state interactions (role-change denylist, 2FA key separation), count divergence (TTL semantics, single-use enforcement), and component interactions (chaos drill). V2 hits only guard conditions partially. **This is the largest single dimension gap.**
2. **Risk coverage (5/5 vs 4/5)** — V1's DR runbook (RTO 1hr / RPO 5min), IR playbook (GDPR 72-hr notification), and chaos drill make NFR-005 (99.9% uptime) operationally verifiable. V2 lacks all three.
3. **Correctness (5/5 vs 4/5)** — V2's "no revocation list needed for access tokens" claim is inconsistent with FR-004's RBAC role-change requirement.
4. **Specificity (0.92 vs 0.84)** — V1 names libs (python-jose, authlib, pyotp, slowapi), parameters (Argon2 m=64MB t=3 p=4), and operational targets (RTO/RPO).
5. **Per-diff-point debate tally** — V1 won 25 of ~38 contested diff points (66%) and retains 11 of 14 unique contributions.

### Strengths to Preserve from V1 (Base)

- Foundations-first milestone ordering (M1 crypto/audit substrate before M2 login)
- Audit substrate established in M1 with `AuditLogger` service called from day-one events
- Argon2id password hashing with calibrated parameters (m=64MB, t=3, p=4)
- Refresh-token family rotation per IETF OAuth 2.0 Security BCP
- Access-token bloom-filter denylist for revocation responsiveness
- Permission propagation via denylist on role change (D4.3)
- 2FA secret encrypted under KMS key DISTINCT from column-encryption key
- Cross-cutting tracks (Security, Observability, Performance, Compliance, CI/CD)
- Chaos engineering drill (D5.2)
- DR runbook with RTO 1hr / RPO 5min + tabletop exercise (D5.5)
- Key rotation drill in staging (D5.6)
- External pentest engagement (Cobalt or equivalent) with 4-week lead time (D5.4)
- IR playbook for PII breach with GDPR 72-hr notification timeline (D5.7)
- STRIDE threat modeling at start of each new-surface milestone
- Trusted-device 30-day cookie (D3.6)
- Feature flags via `unleash` for risky rollouts
- mTLS between API and Redis (D1.4)
- Final FR-acceptance test suite (D5.8) — every FR has a green E2E test in CI
- Sprint Layout appendix

### Strengths to Incorporate from V2 (Non-Base)

These will become specific changes in the refactor plan (`refactor-plan.md`):

1. **Avatar upload to S3/R2 with signed URL** (U-012, V2's D4.2) — extend V1's FR-010 deliverable D4.4 to include avatar upload+download
2. **Explicit `/auth/reactivate` endpoint during grace period** (U-013, V2's D4.6) — add to V1's FR-012 deliverable D4.6, making reactivation an active intent (not just a passive grace window)
3. **`audit_events` DB role granted only INSERT + SELECT** (U-014, V2's D3.9 column) — add this DB-role-level constraint to V1's D1.5 audit-table deliverable. Application-tamper-resistance at the DB role level is strictly stronger than V1's application-only enforcement.
4. **Longer soak test: 4-hour at 10K concurrent** (C-018, V2's D5.3) — replace V1's 1-hour soak with V2's 4-hour soak in D5.1. Slow Redis memory leaks surface only under longer soak.
5. **14-day deactivation grace** (X-006, V2's D4.5) — adopt V2's 14-day window instead of V1's 30-day in D4.6. Closer to privacy-by-default; GDPR Article 17 favors shorter grace.
6. **5/15min lockout policy** (C-007, V2's D3.8) — replace V1's 10/1hr with V2's 5/15min in D2.5. Closer to common industry default.
7. **Compromise refresh-token TTL** (X-002) — adopt a hybrid: refresh rotation cadence of 7 days inside an absolute family-lifetime ceiling of 30 days. Combines V1's family-rotation safety with V2's safer-by-default short rotation window.
8. **Static 4-role seeded hierarchy for v1** (X-004) — keep V1's underlying `roles`/`permissions`/`role_permissions` schema (forward extensibility), but **seed only 4 roles** (`viewer`, `editor`, `admin`, `superadmin`) — matching V2's static hierarchy and the source-spec literal "RBAC" wording.
9. **Range-partition `audit_events` by month** (V2's D3.9) — add to V1's audit-table design in D1.5.
10. **Read replicas for dashboard queries** (V2's Database Operations) — add as cross-cutting note in V1's Performance section.

### Edge Case Floor Status

- V1: 5/5 — well above floor
- V2: 1/5 — exactly at floor (≥1/5 required); V2 was eligible as base but lost on combined score

### Unaddressed Invariants (carried into return contract)

From Round 2.5, 9 HIGH-severity UNADDRESSED findings. Each will be folded into the refactor plan as a specific clarification deliverable in the merged roadmap. See `invariant-probe.md` for full list. The return contract's `unaddressed_invariants` field will list these by ID for caller visibility.
