# Base Selection: Hybrid Quantitative + Qualitative Scoring

## Quantitative Scoring (50% weight)

5 deterministic metrics computed from artifact text (no LLM judgment).

| Metric | Symbol | Weight | V1 (opus) | V2 (sonnet) | V1 Evidence | V2 Evidence |
|--------|--------|--------|-----------|-------------|-------------|-------------|
| Requirement coverage | RC | 0.30 | 1.000 | 1.000 | All FR-001..FR-012, NFR-001..NFR-006, R-001..R-004 cited by ID (lines 244-269 verification matrix) | All FR/NFR/R cited by ID (lines 246-263 success criteria table) |
| Internal consistency | IC | 0.25 | 0.988 | 0.929 | 1 known intra-variant tension (30-day TTL × SameSite=Strict); ~80 substantive claims | 5 contradictions: bcrypt+OWASP unqualified claim, Docker Compose+99.9%+10K, encrypted email+unique btree (INV-010), suspended-as-role, JWT email-token+15min |
| Specificity ratio | SR | 0.15 | 0.903 | 0.909 | Concrete: Argon2id m=64MB/t=3/p=4, RS256/2048-bit, RFC 6238/7636/9106/9700, p95<200ms, 10K, 13mo+7yr, k6, ZAP; vague: "where topology supports", "speakeasy or pyotp" | Concrete: bcrypt 12, RS256, pyotp v2.x, google-auth v2.x, Redis 4GB, p99<200ms, Chrome 120+, Firefox 121+, OWASP ZAP v2.15; vague: "appropriate retention" implied |
| Dependency completeness | DC | 0.15 | 1.000 | 1.000 | All milestone deps + deliverable IDs (D1.1..D5.9) + FR/NFR/R cross-refs resolve | All milestone deps + deliverable IDs (D1.1..D5.8) + FR/NFR/R cross-refs resolve |
| Section coverage | SC | 0.15 | 1.000 | 1.000 | 5 H2 sections (Exec Summary, Milestones, Cross-Cutting, Risk Register, Success Criteria) | 5 H2 sections (same as V1) |

**Formulas**:

- V1 quant = (1.000 × 0.30) + (0.988 × 0.25) + (0.903 × 0.15) + (1.000 × 0.15) + (1.000 × 0.15) = 0.300 + 0.247 + 0.135 + 0.150 + 0.150 = **0.982**
- V2 quant = (1.000 × 0.30) + (0.929 × 0.25) + (0.909 × 0.15) + (1.000 × 0.15) + (1.000 × 0.15) = 0.300 + 0.232 + 0.136 + 0.150 + 0.150 = **0.968**

**Quantitative gap**: 0.014 (1.4% in V1's favor — driven by internal consistency)

---

## Qualitative Scoring (50% weight) — 30-Criterion Additive Binary Rubric

Each criterion is MET (1 pt) or NOT MET (0 pt). Evidence required per CEV protocol.

### Completeness (5 criteria)

**V1**:
| # | Criterion | Verdict | Evidence |
|---|-----------|---------|----------|
| 1 | Covers all explicit source requirements | MET | Success Criteria Verification Matrix (lines 244-269) cites every FR/NFR/R by ID with verification approach |
| 2 | Addresses edge cases and failure scenarios | MET | Chaos tests (M3 OAuth outage acceptance, M4 Redis failover, M5 DB failover); 30-day deactivation grace; R-001..R-004 mitigations per milestone |
| 3 | Includes dependencies and prerequisites | MET | Each milestone "Dependencies:" line names predecessors (e.g., M2 → M1) |
| 4 | Defines success/completion criteria | MET | Per-milestone "Acceptance criteria:" sections + D5.9 GA readiness review sign-off gate |
| 5 | Specifies what is explicitly out of scope | NOT MET | Source spec (lines 37-40) lists biometric, hardware keys, custom SSO as out-of-scope; V1 does not restate these |

**V1 Completeness: 4/5**

**V2**:
| # | Criterion | Verdict | Evidence |
|---|-----------|---------|----------|
| 1 | Covers all explicit source requirements | MET | Success Criteria table (lines 246-263) maps every FR/NFR to verification approach |
| 2 | Addresses edge cases and failure scenarios | MET | Recovery codes for 2FA, GitHub 5xx fallback, rate-limiter burst, deactivation grace |
| 3 | Includes dependencies and prerequisites | MET | Each milestone "Dependencies:" line names predecessors |
| 4 | Defines success/completion criteria | MET | Per-milestone "Acceptance Criteria" sections + D5 production readiness verification |
| 5 | Specifies what is explicitly out of scope | NOT MET | Same gap as V1 — source spec out-of-scope items not restated |

**V2 Completeness: 4/5**

### Correctness (5 criteria)

**V1**:
| # | Criterion | Verdict | Evidence |
|---|-----------|---------|----------|
| 1 | No factual errors / hallucinated claims | MET | All cited RFCs (6238, 7636, 9106, 9700) exist and are correctly described; OWASP ASVS 4.0 §2.4 correctly cited; Argon2id parameters per ASVS |
| 2 | Technical approaches feasible with constraints | MET | k8s HPA+PDB sized to NFR-002+NFR-005; no impossible combinations |
| 3 | Terminology consistent | MET | "refresh token", "JWT access token", "RBAC", "audit_events", "family_id" used consistently |
| 4 | No internal contradictions | MET | Cross-validated against IC=0.988; one noted friction (30-day TTL × SameSite=Strict) does not rise to contradiction |
| 5 | Claims supported by evidence/rationale | MET | Each cross-cutting concern justified with RFC/ASVS references; risk register has per-row rationale |

**V1 Correctness: 5/5**

**V2**:
| # | Criterion | Verdict | Evidence |
|---|-----------|---------|----------|
| 1 | No factual errors / hallucinated claims | NOT MET | "OWASP Top 10 compliance verified" (line 12) with bcrypt cost-12 (line 34) is misleading without justifying rejection of OWASP-preferred Argon2id; "google-auth library v2.x" mischaracterizes the Google Auth Library for Python which is generally not a full OAuth2 authorization-code-flow client (authlib or google-auth-oauthlib serves that role) |
| 2 | Technical approaches feasible with constraints | NOT MET | Docker Compose + 2 replicas + 99.9% uptime + 10K concurrent + rolling deploys is not simultaneously achievable (X-002); column-level AES-256-GCM + unique btree on `email` (D5.2 line 173) requires blind-index that is not defined (INV-010) |
| 3 | Terminology consistent | MET | Consistent use of API terminology, role names, deliverable IDs |
| 4 | No internal contradictions | NOT MET | bcrypt-12+OWASP-verified, Docker-Compose+99.9%+10K, encrypted-email+unique-btree, suspended-as-role+orthogonal-status |
| 5 | Claims supported by evidence/rationale | MET | Each deliverable describes purpose and approach |

**V2 Correctness: 3/5**

### Structure (5 criteria)

| # | Criterion | V1 | V2 | V1 Evidence | V2 Evidence |
|---|-----------|-----|-----|-------------|-------------|
| 1 | Logical section ordering (prerequisites before dependents) | MET | MET | Foundation → Core → Federation → Hardening → GA (dependency-ordered) | Core → OAuth+2FA → RBAC+Audit → Admin → Hardening (coherent ordering) |
| 2 | Consistent hierarchy depth | MET | MET | Per-milestone sub-structure identical | Per-milestone sub-structure identical |
| 3 | Clear separation of concerns | MET | MET | Milestones (temporal) / Cross-Cutting (system-wide) / Risk Register / Success Criteria | Same separation |
| 4 | Navigation aids | MET | MET | Section headings + deliverable IDs + FR/NFR/R cross-refs | Section headings + deliverable IDs in tables + cross-refs |
| 5 | Follows conventions of artifact type | MET | MET | Standard roadmap structure | Same standard structure |

**V1 Structure: 5/5 | V2 Structure: 5/5**

### Clarity (5 criteria)

| # | Criterion | V1 | V2 | V1 Evidence | V2 Evidence |
|---|-----------|-----|-----|-------------|-------------|
| 1 | Unambiguous language (no hedging) | NOT MET | MET | "Node.js 20 LTS (reference; substitute equivalents if implementing in Python/Go)" (line 7); "speakeasy or pyotp" (D4.1 line 142); "opossum or pybreaker" (D3.7) | Pinned Python 3.11+/FastAPI/pyotp v2.x throughout; no hedging |
| 2 | Concrete rather than abstract | MET | MET | Specific algorithms, parameters, RFCs, timeframes | Specific libraries, versions, parameters |
| 3 | Each section has clear purpose | MET | MET | Goal statement per milestone | Goal statement per milestone |
| 4 | Acronyms defined on first use | MET | MET | "two-factor authentication (2FA)", "role-based access control (RBAC)" defined | Same definitions present |
| 5 | Actionable next steps identified | MET | MET | Per-milestone deliverables + acceptance criteria + D5.9 GA gate | Per-milestone deliverables + acceptance criteria + D5 production readiness |

**V1 Clarity: 4/5 | V2 Clarity: 5/5**

### Risk Coverage (5 criteria)

| # | Criterion | V1 | V2 | V1 Evidence | V2 Evidence |
|---|-----------|-----|-----|-------------|-------------|
| 1 | ≥3 risks with probability + impact | MET | MET | 4 risks (R-001..R-004) with Impact + Probability columns | 4 risks with Impact + Probability columns |
| 2 | Mitigation strategy per risk | MET | MET | "Roadmap Mitigation" column with multiple deliverable refs per risk | "Mitigation" column with deliverable refs |
| 3 | Failure modes and recovery procedures | MET | MET | D5.8 runbook: token-compromise, mass password-reset, OAuth outage, PII-breach (GDPR 72h) | D5.8 runbook: OAuth outage, Redis failover, DB failover, token key rotation |
| 4 | External dependency failure scenarios | MET | MET | OAuth circuit breaker (D3.7); SendGrid bounce webhook (D2.3); chaos tests per external dep | GitHub 5xx fallback (D2.2); Google OAuth fallback (R-003); Redis Sentinel |
| 5 | Monitoring/validation for risk detection | MET | MET | SLO burn-rate alerts (D5.5), failed-login >3σ alert, audit-event-volume drop alert | Prometheus alerts on p99 latency, error rate, session memory, replication lag |

**V1 Risk Coverage: 5/5 | V2 Risk Coverage: 5/5**

### Invariant & Edge Case Coverage (5 criteria)

| # | Criterion | V1 | V2 | V1 Evidence | V2 Evidence |
|---|-----------|-----|-----|-------------|-------------|
| 1 | Boundary conditions for collections | MET | MET | 10K concurrent boundary, family revocation, lockout 5/15min, 3-cycle progression; pagination not bounded (gap) | Pagination default 50/max 200 explicit; rate limit 5/min login, 100/min general |
| 2 | State variable interactions across components | NOT MET | NOT MET | INV-001 (pending-email state), INV-002 (Redis-Sentinel counter survival) flagged unaddressed | INV-001 (single email column with keep-old-valid behavior unsolved), INV-010 (encrypted email + unique btree) |
| 3 | Guard condition gaps | MET | MET | Constant-time email-existence response (D2.7); parametrized queries; refresh-token reuse detection | bcrypt constant-time comparison (line 37); HTTP 422 validation; CSRF/CSP headers (D2.7) |
| 4 | Count divergence scenarios | NOT MET | NOT MET | INV-005 (cycle counter window unspecified) unaddressed | INV-006 (page-size 200 × per-user perm cache) not analyzed |
| 5 | Interaction effects across feature combinations | NOT MET | NOT MET | INV-003 (admin promotion bypasses 2FA), INV-008 (family semantics), INV-010, INV-011, INV-012 unaddressed | Same set + INV-016 (CSP × React SPA) |

**V1 Invariant & Edge Case: 2/5 | V2 Invariant & Edge Case: 2/5**

### Qualitative Summary

| Dimension | V1 | V2 |
|-----------|-----|-----|
| Completeness | 4/5 | 4/5 |
| Correctness | 5/5 | 3/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 4/5 | 5/5 |
| Risk Coverage | 5/5 | 5/5 |
| Invariant & Edge Case | 2/5 | 2/5 |
| **Total** | **25/30** | **24/30** |
| **qual_score** | **0.833** | **0.800** |

### Edge Case Floor Check

Threshold: 1/5. Both variants score 2/5 — both ≥ 1/5. **Both eligible**, no floor suspension.

---

## Position-Bias Mitigation (Dual-Pass)

Pass 1: Evaluated in input order (V1, V2). Pass 2: Evaluated in reverse order (V2, V1). Both passes use identical CEV protocol.

| Criterion | V1 Pass 1 | V1 Pass 2 | V2 Pass 1 | V2 Pass 2 | Disagreement | Final |
|-----------|-----------|-----------|-----------|-----------|--------------|-------|
| Completeness #5 | NOT MET | NOT MET | NOT MET | NOT MET | No | NOT MET both |
| Correctness #1 | MET | MET | NOT MET | NOT MET | No | V1: MET, V2: NOT MET (bcrypt+OWASP misleading claim is in the text regardless of evaluation order) |
| Correctness #2 | MET | MET | NOT MET | NOT MET | No | V1: MET, V2: NOT MET (Docker Compose+99.9%+10K infeasibility is text-anchored) |
| Correctness #4 | MET | MET | NOT MET | NOT MET | No | V1: MET, V2: NOT MET (contradictions are text-anchored) |
| Clarity #1 | NOT MET | NOT MET | MET | MET | No | V1: NOT MET, V2: MET (hedging is text-anchored) |

**Disagreements found**: 0 of 60 criterion-variant pairs.
**Verdicts changed**: 0.

Position bias is confirmed not to be driving the outcome.

---

## Combined Scoring

Formula: `variant_score = (0.50 × quant_score) + (0.50 × qual_score)`

| Variant | Quant | Qual | Combined |
|---------|-------|------|----------|
| V1 (opus) | 0.982 | 0.833 | **0.908** |
| V2 (sonnet) | 0.968 | 0.800 | **0.884** |

**Margin**: 0.024 (2.4%)

### Tiebreaker Protocol

Margin < 5% triggers tiebreaker.

**Level 1 — Debate Performance**: V1 won ~28 of 56 diff points outright; V2 won ~11; ~5 resolved as merged-best or tie. V1 wins debate-performance tiebreaker decisively.

Additionally, V2's advocate **explicitly conceded base selection** in Round 2: "V1 should be the merge base. V2 contributions should be folded into V1 as amendments."

Tiebreaker stops at Level 1. V1 wins.

---

## Selected Base: Variant 1 (opus)

**Final decision**: variant-1-opus-default.md is the merge base.

### Selection Rationale

1. **Higher combined score**: 0.908 vs. 0.884 (V1 margin 0.024, driven by IC and Correctness).
2. **Debate dominance**: V1 won the majority of diff points and X-001/X-002/X-003 contradictions outright.
3. **Explicit V2-advocate concession**: V2's advocate publicly conceded V1 as the merge base after Round 2.
4. **Standards grounding**: V1's choices (Argon2id, PKCE+S256, RFC 9700 family revocation, OWASP A01-A10 mapping, STRIDE threat model, k8s HPA+PDB, S3 object-lock retention) are *what the spec's NFR-003 (OWASP) and NFR-005 (99.9%) actually require*. V2 made simpler choices that conceded under standards scrutiny.

### Strengths to Preserve from Base (V1)

- Foundation-first M1 security depth (Argon2id, pgcrypto with KMS, threat model, OpenTelemetry, CI scanning) — but accept the walking-skeleton compromise
- RFC 9700 refresh-token family revocation
- PKCE+S256 OAuth2
- OWASP A01-A10 mapping table
- k8s HPA+PDB + burn-rate SLO alerts
- 13mo hot + S3 7yr object-lock audit retention
- Progressive lockout (5 fails→15min; 3 cycles→reset)
- GDPR 72h breach runbook
- GA readiness sign-off gate (D5.9)
- Mandatory 2FA for admin role
- HIBP breached-password check
- Chaos engineering acceptance tests

### Strengths to Incorporate from V2 (Refactor Plan Input)

| V2 Element | Integration Target |
|------------|---------------------|
| `/api/v1/` versioned API paths | All endpoint definitions in M2-M5 |
| Admin <500ms@50K users gate + EXPLAIN ANALYZE CI | M5 D5.2 |
| Pagination defaults (50/200) | All list endpoints in M4-M5 |
| Schemathesis contract testing per PR | Cross-Cutting Testing strategy |
| Email-change keeps old email active until new verified | D5.1 (with INV-001 resolution) |
| Redis Sentinel for dev/test environments | D1.2 |
| Python library pinning (pyotp, google-auth, fastapi-limiter, Schemathesis) | Week-0 ADR / D1.4 reference implementation |
| React 18 + TanStack Table specifics for admin SPA | D5.2 |
| Walking-skeleton login by week 2-3 | D1.8 (new) |
| Markdown table deliverable format | Adopt across milestones |
| Versioned-API deprecation policy hooks | Cross-Cutting documentation |

### Mandatory Items from Invariant Probe (must address in merged output)

These 6 HIGH UNADDRESSED items are NOT optional. The refactor plan must produce concrete resolutions or explicit accept-the-risk documentation in the merged output:

- INV-001 pending-email state representation
- INV-003 admin-promotion 2FA enrollment gate
- INV-010 pgcrypto + unique btree blind-index requirement
- INV-011 S3 object-lock vs GDPR erasure redaction policy
- INV-013 NFR-001 latency budget including Argon2id/decryption/cold-cache
- INV-015 NFR-005 SLO scope + serial-dependency availability product
