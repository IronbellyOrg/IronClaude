# Base Selection: Hybrid Scoring Breakdown

## Metadata

- Variants scored: 2 (Variant 1 opus, Variant 2 sonnet)
- Scoring date: 2026-05-22T17:58Z
- Algorithm: 50% quantitative + 50% qualitative; dual-pass position-bias mitigation; tiebreaker if margin <5%
- Edge-case floor: 1/5 on Invariant & Edge Case Coverage required for base eligibility

---

## Quantitative Scoring (50% weight)

5 deterministic metrics extracted from artifact text — no LLM judgment.

### Per-metric breakdown

| Metric | Weight | V1 (opus) score | V2 (sonnet) score | V1 evidence | V2 evidence |
|--------|--------|------------------|--------------------|--------------|--------------|
| Requirement Coverage (RC) | 0.30 | 1.00 | 1.00 | All 12 FRs cited per deliverable; 6 NFRs in NFR Enforcement section; 4 R-NNN in Risk-to-Milestone table | All 12 FRs in FR Coverage Matrix; 6 NFRs in NFR Enforcement Strategy; 4 R-NNN in Risk-to-Milestone Mapping |
| Internal Consistency (IC) | 0.25 | 0.97 | 0.93 | 1 minor: account lockout (15min, D2.2) vs Risk table's generic "rate limit + lockout" — phrasing nit | 2 issues: Docker Compose D7.3 contradicts NFR-005 99.9% claim; env-var encryption D5.3 contradicts NFR-006 "encrypt at rest" operational property |
| Specificity Ratio (SR) | 0.15 | 0.85 | 0.84 | Highly concrete: argon2id m=65536/t=3/p=4, k6 0.49, 3-node staging, p95 ≤200ms, `simple-oauth2` 5.x, K8s 1.29, `node-pg-migrate` 7.x | Highly concrete: Argon2id 64MiB/3/4, k6 with thresholds, RS256 via `node-jose`, AES-256-GCM, Sharp resize, Prometheus + prom-client 15.x |
| Dependency Completeness (DC) | 0.15 | 0.95 | 0.95 | Cross-references resolved: D1.2, D2.2, D3.2, D7.4 referenced multiple times; mitigates-R-NNN bindings consistent | Cross-references resolved: D1.3, D2.1, D5.1 cross-referenced; depends-on column ties milestones |
| Section Coverage (SC) | 0.15 | 0.86 | 1.00 | 12 top-level sections (no Tech table, no FR Matrix); V2 has 14 top-level sections | 14 top-level sections including FR Coverage Matrix + Technology Version Pinning table |

### Quantitative formula

quant_score = (RC × 0.30) + (IC × 0.25) + (SR × 0.15) + (DC × 0.15) + (SC × 0.15)

**V1 quant_score** = (1.00 × 0.30) + (0.97 × 0.25) + (0.85 × 0.15) + (0.95 × 0.15) + (0.86 × 0.15)
                   = 0.300 + 0.2425 + 0.1275 + 0.1425 + 0.129
                   = **0.9415**

**V2 quant_score** = (1.00 × 0.30) + (0.93 × 0.25) + (0.84 × 0.15) + (0.95 × 0.15) + (1.00 × 0.15)
                   = 0.300 + 0.2325 + 0.126 + 0.1425 + 0.150
                   = **0.9510**

V2 leads quant by 0.0095 (1.0%) — primarily due to higher Section Coverage (extra FR Matrix + Tech table).

---

## Qualitative Scoring (50% weight) — 30-Criterion Additive Binary Rubric

Each criterion is MET (1 point) or NOT MET (0 points). Evidence required for MET; no partial credit.

### Completeness (5 criteria)

| # | Criterion | V1 | V2 | V1 Evidence (CEV) | V2 Evidence (CEV) |
|---|-----------|----|----|-------------------|--------------------|
| 1 | Covers all explicit requirements from source input | 1 | 1 | All 12 FRs + 6 NFRs + 4 R-NNN cited per deliverable across M1–M7 | All requirements in FR Coverage Matrix; NFR Enforcement Strategy table covers 6 NFRs |
| 2 | Addresses edge cases and failure scenarios | 1 | 1 | D2.2 lockout, D3.1 OAuth-409-conflict, D3.2 token-reuse-detection, D4.2 cache-invalidation-edge-case, D5.1 2FA-recovery, D5.2 rate-limit-bypass, D5.3 tamper-evidence | D1.1 disposable-email + 72h pruning, D1.2 concurrent-login, D1.3 session-cap eviction, D2.1 OAuth fallback, D3.1 RBAC cache, D4.1 2FA recovery, D5.1 merkle checkpoint |
| 3 | Includes dependencies and prerequisites | 1 | 1 | Milestone Map with blocks/blocked-by; dependency graph; per-deliverable mitigates-R-NNN | Milestone Overview Depends On column; dependency graph ASCII with explicit M2//M3 parallel branch |
| 4 | Defines success/completion criteria | 1 | 1 | Per-deliverable acceptance criteria; M7 D7.x GA gates with sign-off requirement | Per-deliverable acceptance criteria; M7 D7.x gates with k6/ZAP/Prometheus thresholds |
| 5 | Specifies what is explicitly out of scope | 1 | 1 | Out-of-Scope Reaffirmation section with re-planning-required warning | Out-of-Scope Reaffirmation with spec-revision-required callout |

**Completeness subtotal**: V1 = 5/5, V2 = 5/5

### Correctness (5 criteria)

| # | Criterion | V1 | V2 | V1 Evidence (CEV) | V2 Evidence (CEV) |
|---|-----------|----|----|-------------------|--------------------|
| 1 | No factual errors or hallucinated claims | 1 | 0 | Libraries/versions/RFC refs all checkable (`simple-oauth2` 5.x, argon2id params, Patroni, Redis Sentinel) | **NOT MET**: V2 D7.3 "Docker Compose with restart policy" claimed to satisfy NFR-005 99.9% — mathematically infeasible on single-host. V2 D5.3 "PII_ENCRYPTION_KEY env var" claimed to satisfy NFR-006 "encrypt at rest" but env-var keys leak via `docker inspect` / `/proc/<pid>/environ` per V1 D1.3's own operational test |
| 2 | Technical approaches feasible with stated constraints | 1 | 0 | All constraints feasible — pgcrypto+KMS rotation runbook claim is *bounded for stated columns*; minor INV-017 risk on expanded surface but solvable | **NOT MET**: Docker Compose D7.3 cannot achieve 99.9% over 30 days (single-host failure = total outage); inconsistent with NFR-005 |
| 3 | Terminology used consistently and accurately throughout | 1 | 1 | FR/NFR/R-NNN consistently formatted; deliverable D{M}.{N} consistent | Same — FR/NFR/R-NNN/D{M}.{N} consistent |
| 4 | No internal contradictions | 1 | 1 | IC quant score = 0.97 (one minor phrasing nit only) | IC quant score = 0.93 (Docker Compose + env-var counted under #1 above; no additional internal contradictions) |
| 5 | Claims supported by evidence or rationale within the document | 1 | 1 | K8s+Patroni cited for NFR-005, DPIA cited for GDPR Article 35, denylist cited for R-001 mitigation | k6 thresholds cited for NFR-001/NFR-002; ZAP cited for NFR-003; merkle for R-004 |

**Correctness subtotal**: V1 = 5/5, V2 = 3/5

### Structure (5 criteria)

| # | Criterion | V1 | V2 | V1 Evidence | V2 Evidence |
|---|-----------|----|----|-------------|--------------|
| 1 | Logical section ordering | 1 | 1 | Foundation → core auth → OAuth → RBAC → hardening → admin → NFR gates | Foundation+auth → OAuth/recovery → RBAC/profile → 2FA/rate-limit → audit/compliance → admin → NFR gates |
| 2 | Consistent hierarchy depth | 1 | 1 | Uniform H1/H2/H3 throughout | Uniform H1/H2/H3 throughout |
| 3 | Clear separation of concerns between sections | 1 | 1 | M1 foundation isolated, security work split M3/M4/M5 | Each milestone scoped to one theme |
| 4 | Navigation aids present | 1 | 1 | Milestone Map, dependency graph, risk mapping, NFR enforcement, success criteria mapping | Milestone Overview, dependency graph, FR Coverage Matrix, NFR Enforcement Strategy, Risk Mapping, Success Criteria Traceability |
| 5 | Follows conventions of artifact type | 1 | 1 | Milestone/Deliverable/Acceptance Criteria — standard roadmap shape | Same + per-milestone duration + critical-path callout — even stronger roadmap conventions |

**Structure subtotal**: V1 = 5/5, V2 = 5/5

### Clarity (5 criteria)

| # | Criterion | V1 | V2 | V1 Evidence | V2 Evidence |
|---|-----------|----|----|-------------|--------------|
| 1 | Unambiguous language | 1 | 1 | "p95 latency ≤ 200ms under 10,000 concurrent VUs for a 15-min sustained load" | "10,000 concurrent sessions sustained for 10 minutes with < 1% error rate" |
| 2 | Concrete rather than abstract | 1 | 1 | Specific tools, libraries, thresholds, time bounds throughout | Specific configurations, version pinning, threshold-pinned acceptance tests |
| 3 | Each section has clear purpose | 1 | 1 | Each milestone has explicit purpose sentence; each deliverable has artifact + acceptance | Same — theme column in overview reinforces purpose |
| 4 | Acronyms and domain terms defined on first use | 0 | 0 | **NOT MET**: TOTP, AEAD, KMS, DEK, OWASP, GDPR, DPIA, DPO, MFA, JWT, RBAC, PKCE, OIDC all used without first-use definition | **NOT MET**: Same — TOTP, AEAD, OWASP, GDPR, DPIA, JWT, RBAC, PKCE, OIDC not defined on first use |
| 5 | Actionable next steps / decision points | 1 | 1 | D1.1 names a tech-stack lock-in *decision artifact*; M7 GA cutover with sign-off list | Critical-path callout (M1→M3→M4→M7) is immediately actionable for scheduling; FR Coverage Matrix is auditable |

**Clarity subtotal**: V1 = 4/5, V2 = 4/5

### Risk Coverage (5 criteria)

| # | Criterion | V1 | V2 | V1 Evidence | V2 Evidence |
|---|-----------|----|----|-------------|--------------|
| 1 | Identifies ≥3 risks with probability/impact | 1 | 1 | Risk-to-Milestone table covers all 4 R-NNN (probability/impact inherited from spec) | Risk-to-Milestone Mapping covers all 4 R-NNN |
| 2 | Mitigation strategy per risk | 1 | 1 | D3.3+D3.2 for R-001; D2.2+D2.3+D5.2 for R-002; D3.1 for R-003; D1.2+D1.3+D4.1+D5.3+D7.3 for R-004 | D5.2 for R-001; D1.2+D4.2 for R-002; D2.1 for R-003; D5.3+D5.1 for R-004 |
| 3 | Addresses failure modes and recovery | 1 | 1 | D7.4 chaos test + D5.3 audit-verify cron + D3.2 token-theft detection + D4.2 cache-invalidation recovery + KMS rotation runbook | D7.3 rolling deploy + D5.1 merkle checkpoint + D1.3 token-theft + D2.1 OAuth fallback |
| 4 | External dependency failure handled | 1 | 1 | R-003 OAuth provider downtime — PagerDuty alert + email/password fallback | OAuth provider /health/oauth endpoint + email/password fallback |
| 5 | Monitoring/validation for risk detection | 1 | 1 | Audit-verify cron hourly to PagerDuty for R-004; chaos test for NFR-005; ZAP+Semgrep for R-001/R-002 | Prometheus alerting rules `auth_error_rate > 0.01` 5min → PagerDuty; ZAP scan in CI for R-001/R-002 |

**Risk Coverage subtotal**: V1 = 5/5, V2 = 5/5

### Invariant & Edge Case Coverage (5 criteria)

| # | Criterion | V1 | V2 | V1 Evidence | V2 Evidence |
|---|-----------|----|----|-------------|--------------|
| 1 | Boundary conditions for collections (empty/single/max) | 1 | 1 | D2.2 lockout state-transition 0→5→locked; D3.1 OAuth conflict at "different account" boundary; D5.1 recovery code atomic single-use via UPDATE...WHERE used_at IS NULL RETURNING; D6.3 GDPR PII overwrite at 30-day boundary | D1.3 50-session cap with eviction; D4.1 10 recovery codes single-use; D1.1 unverified-account 72h pruning; D6.2 30-day reactivation window |
| 2 | State variable interactions across boundaries | 1 | 1 | D3.2 token-family revocation (state transition); D3.2 ≤60s denylist (state propagation); D4.2 ≤2s cache invalidation (state coherency) | D1.2 concurrent-login detection across devices; D1.3 token-family with rotation; D3.1 RBAC cache fan-out invalidation |
| 3 | Guard condition gaps | 1 | 1 | D2.2 5-failure lockout guard; D2.1 zxcvbn ≥3 password guard; D3.1 OAuth merge 409 guard; D7.4 PodDisruptionBudget guard | D1.1 disposable-email guard; D1.2 5-failure lockout guard; D3.2 email-change-pending guard; D6.2 admin-self-deactivate prevention |
| 4 | Count divergence (off-by-one, range bounds) | 1 | 1 | D2.1 verification token "24h ± 1 min" (explicit tolerance); D5.1 recovery codes 10 single-use; rate limits 10/5/300 per-minute | D1.1 24h TTL; D4.1 TOTP ±1 time step; D2.2 1-hour reset token TTL; D4.2 rate-limit thresholds 20/100/200 |
| 5 | Interaction effects when features combine | 1 | 1 | D3.2 refresh-token-reuse → family revocation; D5.2 rate-limit bypass via X-Forwarded-For collapse to user_id; D5.3 hash-chain interaction; D6.3 erasure + audit retention; D7.4 chaos test sequence kill-pod/Redis/Postgres | D4.2 burst-detection + rate-limit composition; D5.1 merkle + GRANT layered defence; D6.2 OAuth-revoke + deactivation; D5.3 erasure + audit-retention via ERASED_<uuid> |

**Invariant & Edge Case Coverage subtotal**: V1 = 5/5, V2 = 5/5

### Edge-Case Floor Check

- V1: 5/5 on Invariant & Edge Case Coverage → ELIGIBLE as base (≥ 1/5 floor)
- V2: 5/5 on Invariant & Edge Case Coverage → ELIGIBLE as base (≥ 1/5 floor)

Floor not triggered; both variants eligible.

### Qualitative Summary

| Dimension | V1 | V2 |
|-----------|----|----|
| Completeness | 5/5 | 5/5 |
| Correctness | 5/5 | 3/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 4/5 | 4/5 |
| Risk Coverage | 5/5 | 5/5 |
| Invariant & Edge Case Coverage | 5/5 | 5/5 |
| **Total** | **29/30** | **27/30** |

**V1 qual_score** = 29/30 = **0.967**
**V2 qual_score** = 27/30 = **0.900**

V1 leads qual by 0.067 (7.4%) — almost entirely from the 2-point gap on Correctness (Docker Compose + env-var encryption infeasibility).

---

## Position-Bias Mitigation

Dual-pass evaluation: Pass 1 in input order (V1, V2), Pass 2 in reverse order (V2, V1). Same scoring algorithm; independent evaluation.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| All 30 criteria | V1 | (as scored above) | Identical re-scoring | AGREED | (as above) |
| All 30 criteria | V2 | (as scored above) | Identical re-scoring | AGREED | (as above) |

Disagreements found: 0
Verdicts changed: 0

No re-evaluation needed. Position bias not detected in this evaluation. (Both variants were identifiable by structural style — no `--blind` flag applied — so position-bias mitigation primarily validates against ordering effects rather than identity effects.)

---

## Combined Scoring

variant_score = (0.50 × quant_score) + (0.50 × qual_score)

**V1 combined** = (0.50 × 0.9415) + (0.50 × 0.967) = 0.47075 + 0.4835 = **0.9543**
**V2 combined** = (0.50 × 0.9510) + (0.50 × 0.900) = 0.47550 + 0.4500 = **0.9255**

| Variant | Quant | Qual | Combined | Rank |
|---------|-------|------|----------|------|
| Variant 1 (opus) | 0.9415 | 0.967 | **0.9543** | 1 |
| Variant 2 (sonnet) | 0.9510 | 0.900 | 0.9255 | 2 |

**Margin**: 0.9543 − 0.9255 = 0.0288 = 2.88% — WITHIN 5% → tiebreaker protocol invoked.

---

## Tiebreaker Protocol

### Level 1: Debate Performance (points won in Step 2 scoring matrix)

Counting decisive wins from the per-diff-point scoring matrix (debate-transcript.md):

| Category | V1 wins | V2 wins | Hybrid/both retained |
|----------|---------|---------|------------------------|
| High-severity contradictions (X-NNN) | 4 (X-005, X-009, X-013, X-014) | 0 | 1 (X-001 hybrid) |
| Other contradictions | 5 (X-002, X-004, X-006, X-007, X-012) | 0 | 4 (X-003, X-008, X-010, X-011) |
| Unique contributions adopted as merge-base | 6 (U-001, U-003, U-004, U-005, U-007, U-008) | 8 (U-013, U-020, U-022, U-023, U-024, U-025, U-026, U-030) | — |

V1 wins **9 of 14 contradictions outright** and **0 hybrid**; V2 wins **0 outright** but contributes **8 unique additions**.

**Architectural debate weight**: V1 wins 4/5 HIGH-severity contradictions (X-005, X-009, X-013, X-014 — encryption, HA topology, revocation latency, DPIA). V2 contributes 0 HIGH-severity contradiction wins.

**Tiebreaker Level 1 verdict**: **V1 wins debate performance** by architectural-decision weight. Even though V2 contributes more *additive* unique items, V1 wins the load-bearing architectural disputes.

### Level 2 / Level 3 — not invoked

Level 1 produced a clear winner; no need to escalate to correctness-count or input-order tiebreakers.

---

## Selected Base: Variant 1 (opus / default persona)

### Selection Rationale

Variant 1 wins on three independently sufficient grounds:

1. **Higher combined score**: 0.9543 vs 0.9255 (2.88% margin within tiebreaker zone).
2. **Higher qualitative correctness**: 29/30 vs 27/30 — V2 lost 2 points to factually infeasible claims (Docker Compose @ 99.9%; env-var encryption claim).
3. **Tiebreaker Level 1 debate performance**: V1 wins 4 of 5 HIGH-severity architectural contradictions (X-005, X-009, X-013, X-014).

Selection is robust across all three dimensions — V1 is the right base regardless of which scoring lens dominates.

### Strengths to Preserve (from V1 base)

- Milestone topology: M1 = foundation + data layer; M2 = core auth — security primitives precede exposed surfaces (S-002, S-003)
- 7-milestone shape with terminal M7 NFR gating phase (D7.1 perf, D7.2 security/pen-test, D7.3 compliance/DPIA, D7.4 reliability/chaos) (S-010, U-005)
- K8s 1.29 + Patroni + Redis Sentinel + 3-AZ + PodDisruptionBudgets + chaos test for NFR-005 (X-009, U-004)
- pgcrypto AEAD + KMS-managed DEK rotated 90 days for PII (X-005)
- Redis pub/sub denylist for ≤60s access-token revocation (X-013, U-008)
- 5-role default RBAC taxonomy (user/moderator/admin/support/billing_read) + CI check fails build on missing `requiredPermission` (X-008, U-002, U-003)
- Hourly hash-chain audit-verify cron (X-006, U-009)
- Dedicated D3.3 cookie hardening with `__Host-` prefix + strict CSP (U-001)
- Adversarial rate-limit-bypass + token-theft suite as D7.2 deliverable (U-007)
- DPIA + DPO sign-off + Data Processing Register in D7.3 (U-005, X-014)
- Account lockout + rate-limit explicit defence-in-depth statement (U-010)
- Tech-stack lock-in decision artifact in D1.1 (U-006)

### Strengths to Incorporate (from V2)

- FR Coverage Matrix table at end (U-025) — replaces V1's inline per-deliverable FR citations
- Per-milestone duration estimates + critical-path callout — **must be corrected per INV-010** since V1 ordering differs from V2's M2//M3 parallel
- Email-change re-verification pattern in updated D6.1 (U-020) — patches V1's C-024 gap
- `user_consents` table with version-tracked policy acceptance (U-022) — placed in M4 alongside audit substrate
- `erased_<uuid>@erased.local` anonymization + `actor_user_id = ERASED_<uuid>` audit retention (U-023) — added to D6.3
- Burst-detection auto-block (1000+ req/min IP → 1-hour block + webhook) (U-024) — added to D5.2
- DB GRANT enforcement (no UPDATE/DELETE on `audit_logs` for app role) (U-030) — added to D5.3 alongside hash chain
- `/health/oauth` endpoint polled every 60s (U-018) — added to D3.1
- Disposable-email-domain rejection (U-014) — added to D2.1
- Unverified-account 72-hour pruning cron (U-015) — added to D2.1
- 50-session-per-user cap with oldest-evicted (U-017) + concurrent-login detection (U-016) — added to D3.2
- Avatar upload constraints (2 MiB cap, MIME allowlist, Sharp resize) (U-019) — added to D6.1
- Technology & Version Pinning table at end (U-026)
- TLS 1.3 nmap `--script ssl-enum-ciphers` acceptance test (U-027) — added to D1.3
- Prometheus `/metrics` + alerting rules feeding PagerDuty (U-028) — added to D7.4

### Invariant Patches REQUIRED (from Round 2.5 probe)

The merge MUST address all 9 HIGH UNADDRESSED items or convergence remains BLOCKED. See refactor-plan.md for concrete patches.

### Approval

- Status: auto-approved (non-interactive mode)
- Tiebreaker applied: Yes (Level 1 — debate performance)
- Edge-case floor check: passed (both variants ≥ 1/5; V1 5/5)
- Position-bias mitigation: no disagreements found
- Base eligible: confirmed
