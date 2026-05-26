# Base Selection

## Metadata

- Evaluator: skill-direct (orchestrator-computed, position-bias-mitigated)
- Source variants: variant-1-opus-default.md, variant-2-sonnet-default.md
- Edge case floor: 1/5 (active — both variants must score ≥1/5 on Invariant & Edge Case dimension)
- Tiebreaker zone: |score_A − score_B| < 0.05 → tiebreaker protocol applies

## Quantitative Scoring (50% weight)

5 deterministic metrics; running this section twice on the same input produces identical scores.

| Metric | Weight | V1 (opus) | V2 (sonnet) | V1 Evidence | V2 Evidence |
|--------|-------:|----------:|------------:|-------------|-------------|
| RC — Requirement Coverage | 0.30 | **1.00** | **1.00** | All 22 IDs (FR/NFR/R) mapped in milestones + risk register | All 22 IDs mapped via Success Criteria + Mapped requirements lines |
| IC — Internal Consistency | 0.25 | **0.98** | **0.94** | No internal contradictions; minor wording fuzz | p99 scope mismatch: Goals row 9 says "all /auth/* endpoints" but D6.6 only asserts for `/auth/login`, `/auth/refresh`, `/auth/profile` |
| SR — Specificity Ratio | 0.15 | **0.92** | **0.88** | Argon2id memCost 64MB, RS256, RFC 6238 SHA-1 30s 6-digit, k6, Snyk, Trivy, OWASP ASVS L2, AES-256 RDS, Vault | 12-char min, AES-256-GCM, PgBouncer, Redis Sentinel, HPA min 3 max 10, 70% CPU, pyotp; slightly more "default/configurable" placeholders |
| DC — Dependency Completeness | 0.15 | **1.00** | **1.00** | All D{M}.{N} references resolve; Critical Path defined entities | All D{M}.{N} references resolve |
| SC — Section Coverage | 0.15 | **1.00** | **1.00** | 8 H2 sections | 8 H2 sections (same) |

**Quant scores**:

- V1: (1.00 × 0.30) + (0.98 × 0.25) + (0.92 × 0.15) + (1.00 × 0.15) + (1.00 × 0.15) = **0.983**
- V2: (1.00 × 0.30) + (0.94 × 0.25) + (0.88 × 0.15) + (1.00 × 0.15) + (1.00 × 0.15) = **0.967**

## Qualitative Scoring (50% weight) — 30-Criterion Additive Binary Rubric

CEV protocol: every MET verdict cites specific evidence; no evidence ⇒ NOT MET.

### Completeness (5 criteria)

| # | Criterion | V1 verdict + evidence | V2 verdict + evidence |
|---|-----------|------------------------|------------------------|
| 1 | Covers all explicit requirements | MET — G6 "100% of FR-001 through FR-012", all NFRs in Goals, all R-NNN in Risk Register | MET — Success Criteria row 1 + Mapped requirements per milestone |
| 2 | Addresses edge cases and failure scenarios | MET — Per-milestone "Edge Cases Covered" blocks in M2/M3/M5 | MET — D7.1 dedicated edge-case validation test suite (broader scope but centralized) |
| 3 | Includes dependencies and prerequisites | MET — "Entry Criteria" per milestone + Critical Path callout | MET — "Entry criteria" per milestone + Explicit prerequisites list |
| 4 | Defines success/completion criteria | MET — Per-milestone "Exit Criteria" + Success Criteria table | MET — Per-milestone "Exit criteria" + Success Criteria table |
| 5 | Specifies what is explicitly out of scope | MET — Out of Scope with spec-mirrored + roadmap-deferred items | MET — Out of Scope with 9 explicit non-goals |

**Completeness**: V1 = 5/5, V2 = 5/5

### Correctness (5 criteria)

| # | Criterion | V1 verdict + evidence | V2 verdict + evidence |
|---|-----------|------------------------|------------------------|
| 1 | No factual errors or hallucinated claims | MET — RFC 6238, OWASP ASVS L2, Argon2id, JWKS all real | MET — pyotp, google-auth-library-oauthlib, Authlib, pgcrypto all real |
| 2 | Technical approaches feasible | MET — Multi-AZ + Redis cluster is proven; budgets believable | MET — K8s + HPA + PgBouncer + Sentinel is proven |
| 3 | Terminology used consistently | MET — "refresh token family" consistent throughout | MET — "refresh token rotation" + "reuse detection" consistent |
| 4 | No internal contradictions | MET — clean | **NOT MET** — Goals row 9 ("p99 < 200ms for all /auth/* endpoints") vs D6.6 ("p99 < 200ms for `/auth/login`, `/auth/refresh`, `/auth/profile`") narrows scope |
| 5 | Claims supported by evidence/rationale | MET — Each risk has explicit mitigation; deliverables cite RFCs/standards | MET — Risks cite specific deliverable IDs; mitigations concrete |

**Correctness**: V1 = 5/5, V2 = 4/5

### Structure (5 criteria)

| # | Criterion | V1 verdict | V2 verdict |
|---|-----------|------------|------------|
| 1 | Logical section ordering | MET — Exec Summary → Goals → Milestones → Deps → Risks → OpenQ → OutOfScope → Success | MET — same order |
| 2 | Consistent hierarchy depth | MET — H1/H2/H3 only; no heading-level gaps | MET — same |
| 3 | Clear separation of concerns | MET — each milestone has one primary theme | MET — M5 bundles 4 concerns ("Reset, 2FA, Profile, Lifecycle") but framed coherently as "user-facing auth features" |
| 4 | Navigation aids present | MET — Critical Path callout + cross-refs (D5.2 blocks D7.1, etc.) | MET — explicit prerequisites list + per-milestone cross-refs |
| 5 | Follows artifact conventions | MET — standard roadmap with M{N}, D{M}.{N}, R-NNN | MET — same |

**Structure**: V1 = 5/5, V2 = 5/5

### Clarity (5 criteria)

| # | Criterion | V1 verdict | V2 verdict |
|---|-----------|------------|------------|
| 1 | Unambiguous language | MET — deliverables avoid "should consider"/"as appropriate"; hedging only in Open Questions where appropriate | MET — concrete deliverables; minor hedging in Out of Scope ("could be added") |
| 2 | Concrete rather than abstract | MET — extreme concreteness (memCost 64MB, RS256, kid header, S3 object-lock) | MET — concrete (HPA min 3 max 10, AES-256-GCM, 70% CPU target) but slightly fewer named standards |
| 3 | Each section has clear purpose | MET — every milestone Goal explicit | MET — every milestone Goal explicit |
| 4 | Acronyms and domain terms defined | MET — RBAC introduced as "role-based access control" in Exec Summary; some assumption of domain literacy (JWKS, MFA) | MET — same level of domain assumption |
| 5 | Actionable next steps / decision points | MET — 12 Open Questions with explicit "Decision needed before X" framing | MET — 10 Open Questions with explicit "Confirm this is acceptable" framing |

**Clarity**: V1 = 5/5, V2 = 5/5

### Risk Coverage (5 criteria)

| # | Criterion | V1 verdict | V2 verdict |
|---|-----------|------------|------------|
| 1 | ≥3 risks with probability + impact | MET — 12 risks, each with Impact + Probability | MET — 8 risks, each with Impact + Probability |
| 2 | Mitigation strategy for each risk | MET — every risk has Mitigation column | MET — same |
| 3 | Addresses failure modes and recovery | MET — R-005..R-012 are recovery-rich (key rotation runbook, SES failover, family-invalidation alert, deny-by-default) | MET — R-005..R-008 present, less rich on recovery (V2 advocate conceded) |
| 4 | External dependency failure scenarios | MET — R-003 OAuth, R-006 SendGrid→SES, Redis HA implicit | MET — R-003 OAuth, R-005 Redis SPOF, R-006 SendGrid retry |
| 5 | Monitoring/validation mechanism for detection | MET — D7.4 ZAP+Snyk+pen-test, D1.6 observability baseline (OpenTelemetry, Prometheus) | MET — D7.2 Prometheus+Grafana, D6.7 health check, alerts on error rate >1% / p99 > 300ms |

**Risk Coverage**: V1 = 5/5, V2 = 5/5

### Invariant & Edge Case Coverage (5 criteria) — FLOOR APPLIES (1/5)

| # | Criterion | V1 verdict + evidence | V2 verdict + evidence |
|---|-----------|------------------------|------------------------|
| 1 | Boundary conditions for collections | MET — empty-DB bootstrap admin script (D2.7), refresh-token family-reuse, GDPR export 10K events <60s | MET — D7.1 explicit empty-DB / single-user / max-load tests |
| 2 | State variable interactions across boundaries | MET — clock skew on JWT iat/exp, Redis-as-authoritative-clock for rate-limit windows, JWT short-TTL bounds role-revocation staleness ≤15min, OAuth-issued sessions need RBAC | MET — D7.1 token expiry at exact boundary, refresh race; concurrent session eviction (D2.5) |
| 3 | Guard condition gaps identified | MET — R-007 "deny-by-default middleware"; R-008 2FA recovery + force re-enroll; R-009 audit-log tampering by privileged insider | MET — D4.2 implicit deny-by-default (403 if insufficient permission); R-002 lockout (after position-bias re-eval) |
| 4 | Count divergence (off-by-one, inclusive/exclusive) | **NOT MET** — count thresholds present (5 attempts / 15 min, 10 → 30 min, ±1 TOTP window) but no explicit off-by-one / boundary analysis | **NOT MET** — count thresholds present (5 failures / 15 min, 30-min lockout, 5-session cap, 10 backup codes) but no explicit boundary analysis |
| 5 | Interaction effects when features combine | MET — D5.2 blocks D7.1, D3.1 blocks D6.2, D6.4 blocks D7.1, D4.1/D4.2 block D5.4, D1.2 blocks every DB-touching deliverable — explicit interaction matrix | MET — "D3.3 account linking feeds into D4.2"; parallelism note for M3+M4; less rich interaction matrix than V1 |

**Invariant & Edge Case**: V1 = 4/5, V2 = 4/5 (after position-bias re-evaluation; pass 1 had V2 at 3/5, pass 2 reading D4.2 as implicit deny-by-default brought it to 4/5)

**Edge Case Floor Check**: Both ≥ 1/5 — both eligible as base.

### Qualitative Summary

| Dimension | V1 | V2 |
|-----------|---:|---:|
| Completeness | 5/5 | 5/5 |
| Correctness | 5/5 | 4/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 5/5 | 5/5 |
| Risk Coverage | 5/5 | 5/5 |
| Invariant & Edge Case | 4/5 | 4/5 |
| **Total** | **29/30** | **28/30** |
| **Qual score** | **0.967** | **0.933** |

## Position-Bias Mitigation

Dual-pass executed: Pass 1 evaluated in input order (V1, V2); Pass 2 evaluated in reverse (V2, V1).

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| Invariant #3 (guard condition gaps) | V2 | NOT MET (no explicit "deny-by-default" rule) | MET (D4.2 logic IS deny-by-default — 403 returned when no permission match, which is the definition) | Disagreement | Re-evaluated → MET (the evidence stands; D4.2 wording IS deny-by-default operationally) |
| Correctness #4 (no internal contradictions) | V2 | NOT MET (p99 scope mismatch between Goals row 9 and D6.6) | NOT MET (same evidence found) | Agreement | NOT MET |
| All other 28 V1 criteria + 28 V2 criteria | — | (agreed in both passes) | — | Agreement | (as scored above) |

**Disagreements found**: 1; **Verdicts changed by re-evaluation**: 1 (V2 Invariant #3 flipped NOT MET → MET, bringing V2 Invariant from 3/5 to 4/5).

## Combined Scoring

- **V1 combined** = (0.50 × 0.983) + (0.50 × 0.967) = 0.4915 + 0.4835 = **0.975**
- **V2 combined** = (0.50 × 0.967) + (0.50 × 0.933) = 0.4835 + 0.4665 = **0.950**

**Margin**: 0.975 − 0.950 = **0.025 (2.5%)** — within 5% tiebreaker zone.

## Tiebreaker Protocol Application

**Level 1 — Debate performance** (diff points won in scoring matrix):

- V1 wins on: C-006, C-007, C-008, C-011, C-013, S-002, U-001, U-002, U-003, U-004, U-005, X-004 — **12 points** (mostly high-impact: audit chain, GDPR resolution, JWT rotation, SES failover)
- V2 wins on: C-002, C-005, X-005, U-006, U-007, U-008, U-009 — **7 points** (mostly medium-impact: K8s, race condition, session cap, pgcrypto)
- Tied / disputed: 10 (C-001, C-003, C-004/X-001, C-009, C-010, C-012, X-002, X-003, S-001, S-003)

→ **V1 ahead on Level 1** by 5 points. Tiebreaker resolves.

(Levels 2 and 3 unused: Level 2 would also favor V1 — 5/5 vs 4/5 on Correctness count.)

## Selected Base: Variant 1 (opus default)

### Selection Rationale

V1 wins on combined score (0.975 vs 0.950) with a 2.5% margin that triggered the tiebreaker. Tiebreaker Level 1 (debate performance) breaks the near-tie in V1's favor by 12 to 7 diff-point wins, with V1's wins concentrated on high-impact security/compliance points (audit hash-chain, GDPR-vs-audit reconciliation, JWT rotation depth, SES failover) and V2's wins concentrated on medium-impact operational points that can be incorporated via merge.

V1 is also one criterion ahead on the Correctness dimension (5/5 vs 4/5) — V2's p99-scope internal contradiction (Goals row 9 vs D6.6) is a real correctness gap, while V1's claims are internally consistent.

The selection does NOT mean V2 is weaker overall. V2 produced 9 unique contributions (U-006 through U-009 + others) that the refactoring plan WILL incorporate into the merged output. The selection means V1 is the stronger SKELETON to incorporate V2's strengths into, not that V2's strengths should be discarded.

### Strengths to Preserve from V1 (base)

- Hash-chain audit log + S3 object-lock daily export (C-006, U-001) — keystone compliance design (subject to INV-001/007/019 fixes from invariant probe)
- GDPR-vs-audit reconciliation: tokenize user_id in audit table, crypto-shred PII at erasure (C-013, U-004, R-010)
- JWT signing-key rotation depth: RS256 + JWKS `kid` zero-downtime rotation runbook (C-008, U-002)
- SendGrid → AWS SES failover for verification + reset email (U-003, R-006)
- Refresh-token family tracking + family-reuse-detection-invalidates-family (C-011)
- zxcvbn + Argon2id + HIBP-k-anonymity password policy (C-007) — NIST SP 800-63B aligned
- Per-milestone "Edge Cases Covered" blocks (S-002) — makes invariants debuggable per-milestone
- Empty-DB bootstrap admin script in D2.7 (U-005)
- M1-as-pure-foundation structure (X-004) — hardened base before user-facing flows
- Explicit "Critical Path" callout in Dependency Graph + explicit blockers list
- Multi-AZ chaos test with <30s RTO (D7.6)
- 12-risk register with R-005 through R-012 covering JWT key compromise, RBAC misconfig, 2FA recovery abuse, audit tampering, GDPR conflict, refresh theft, TOCTOU on role revocation

### Strengths to Incorporate from V2

- **U-006 — Per-user concurrent session cap (default 5) with oldest-eviction** (V2 D2.5) — incorporate into V1's M3
- **U-007 — Kubernetes manifests + HPA + PgBouncer + Redis Sentinel** (V2 D7.4) — incorporate into V1's M7 D7.6; complements but does not replace multi-AZ chaos test
- **U-008 — Redis WATCH/MULTI/EXEC atomic refresh + explicit race-condition test** (V2 D7.1, R-008) — strengthen V1's M3 D3.1 family-tracking with explicit atomicity primitive
- **U-009 — pgcrypto column-level encryption for email** (V2 D6.8) — incorporate into V1's M1 D1.2 schema
- **V2 advocate's C-002 sequencing insight** — V2's M2→M3(OAuth)→M4(RBAC) means OAuth users get roles sooner; consider in V1's M4-vs-M5 ordering (V1 currently has OAuth M4 before RBAC M5; this is actually V2-aligned, so V1's existing ordering wins, but verify integration)
- **V2's Prometheus + Grafana + alerting specifics** (D7.2) — V1's D1.6 mentions observability baseline; absorb V2's alert thresholds (error rate > 1%, p99 > 300ms)
- **V2's k6/Locust load test with 10-min ramp + 30-min sustain** (D6.6) — V1's D3.6 has the soak; absorb V2's exact ramp pattern
- **V2's account deactivation 30-day grace period semantics** (D5.6) — V1 has 30-day grace at D7.3; absorb V2's explicit deactivated_at column + login-query filtering
- **V2's GDPR export-data + delete-account endpoints with re-auth requirement** (D5.7) — strengthen V1's D6.6 GDPR endpoints
- **V2's edge-case test suite consolidation in D7.1** — absorb as a final validation pass IN ADDITION to V1's per-milestone edge-case blocks (additive, not replacement)

### Carry-Forward Invariants (from invariant-probe.md)

The 10 HIGH+UNADDRESSED invariants from Round 2.5 are NOT resolvable by base selection alone. They must be addressed in the merge step (preferred) or documented as carry-forward risks in the merged roadmap's Risk Register:

- INV-001: Hash-chain genesis/canonicalization/tip-publication gaps → add D6.5 sub-deliverables
- INV-002: SameSite=Strict + OAuth callback interaction → add to D4.1/D4.2 design notes
- INV-007: Hash-chain writer-lock serialization cost → schedule impact disclosed in M6
- INV-017: Async audit write contradicts FR-009 100% capture → resolve via outbox pattern in D6.5
- INV-019: S3 Object Lock vs GDPR crypto-shred → add resolution to R-010 mitigation
- (5 more) → see invariant-probe.md
