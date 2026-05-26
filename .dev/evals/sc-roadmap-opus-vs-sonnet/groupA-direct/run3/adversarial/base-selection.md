# Base Selection: Hybrid Scoring & Selection

> **Pipeline**: sc:adversarial Mode B, Step 3
> **Variants**: V1 (opus-default, 618 lines), V2 (sonnet-default, 723 lines)
> **Source spec**: sample_spec.md (12 FRs, 6 NFRs, R-001..R-004, 5 success criteria)
> **Debate convergence**: NOT_CONVERGED (0.357 / 0.80 threshold; BLOCKED_BY_INVARIANTS with 9-10 HIGH-UNADDRESSED)
> **Selection method**: Forced combined-score selection per protocol no_convergence clause

---

## Quantitative Scoring (50% weight)

### Metric 1: Requirement Coverage (RC, weight 0.30)

Total scorable requirements: 22 (FR-001..FR-012 = 12, NFR-001..NFR-006 = 6, R-001..R-004 = 4).

**Variant 1:**

| Requirement Category | IDs Present | Count |
|---|---|---|
| FR-001 through FR-012 | All 12 explicitly mapped in traceability matrix (lines 482-493) and inline headers (M2 header line 117, etc.) | 12/12 |
| NFR-001 through NFR-006 | All 6 mapped in NFR traceability table (lines 499-504) | 6/6 |
| R-001 through R-004 | All 4 mapped in Risk traceability table (lines 510-513) and inline "Risks Addressed" sections | 4/4 |

**V1 RC = 22/22 = 1.000**

**Variant 2:**

| Requirement Category | IDs Present | Count |
|---|---|---|
| FR-001 through FR-012 | All 12 explicitly mapped in traceability matrix (lines 548-559) and FR mapping annotations per milestone | 12/12 |
| NFR-001 through NFR-006 | All 6 mapped in NFR traceability table (lines 565-570) | 6/6 |
| R-001 through R-004 | All 4 mapped in Risk Mitigations table (lines 576-579) | 4/4 |

**V2 RC = 22/22 = 1.000**

Both variants achieve perfect requirement coverage through explicit traceability matrices.

### Metric 2: Internal Consistency (IC, weight 0.25)

Intra-variant contradictions from diff-analysis.md X-NNN items:

**Variant 1:** X-001 only.

- X-001: Architectural Philosophy claims "2FA (FR-007) precedes OAuth" (line 11), but milestone table shows M5=OAuth, M6=2FA (lines 24-25). Soft sequencing note at line 563 acknowledges the reversal. V1 advocate conceded this as a "documentation defect."
- Estimated scorable substantive claims: ~80 (based on 618-line document with dense technical content).
- IC_V1 = 1 - (1/80) = **0.988**

**Variant 2:** X-002 and X-003.

- X-002: Summary line 24 claims "~77 days on the critical path" but calculation at line 628 shows 44 days. V2 fully conceded.
- X-003: Summary line 24 claims "8-9 weeks" wall-clock but detailed schedule at line 647 shows "~10-11 weeks." V2 fully conceded.
- Estimated scorable substantive claims: ~100 (based on 723-line document with tables, schemas, and explicit acceptance criteria).
- IC_V2 = 1 - (2/100) = **0.980**

No additional intra-variant contradictions were found on closer review beyond those documented in diff-analysis.md.

### Metric 3: Specificity Ratio (SR, weight 0.15)

Counting concrete indicators (numbers, named entities, thresholds, measurable criteria) versus vague indicators.

**Variant 1 concrete indicators (sampled):**
PostgreSQL 15.5, Redis 7.2, RS256, Argon2id m=64MB/t=3/p=4, HTTP-only Secure SameSite=Strict, 15min JWT, 30d refresh, 250ms hash, 99.9% SLO, 43.8min/month error budget, HSTS max-age 63072000, zxcvbn score >=3, 12-char minimum, 32-byte CSPRNG, SHA-256, CITEXT, UUID v7, RANGE partition, 10 failed/15min lockout, 50 failed/IP/1h, 7-year retention, 5 req/min/IP, 1000/min/user, 2x burst for 10s, RFC 6819 section 5.2.2.3, STRIDE, 4 ADRs, Vault, KMS, pgBackRest, RPO 1min, pgcrypto, LUKS, EBS gp3, k6, Locust, PgBouncer, OWASP ZAP, Semgrep, Trivy, cosign, FastAPI 0.115+, NestJS 10+, uid 10001, distroless, WORM, S3 Object Lock.
Count: approximately 55-60 concrete items.

**Variant 1 vague indicators:**
"appropriate" — 0 uses found. "as needed" — 0 uses found. "properly" — 0 uses found. "best practices" — not found as phrase. "reasonable" — used once ("GDPR's reasonable retention"). "suitable" — 0 uses. "where possible" — 1 use (line 44, "read-only root filesystem where possible").
Count: approximately 2 vague items.

**V1 SR = 58 / (58 + 2) = 0.967**

**Variant 2 concrete indicators (sampled):**
PostgreSQL 15, Redis 7, RS256 RSA 2048-bit, Argon2id m=65536/t=3/p=4, AES-256-GCM, HTTP-only Secure SameSite=Strict, 15min JWT, 7d refresh, <500ms hash, 99.9% uptime, 100 min/200 max connections, UUID gen_random_uuid(), PARTITION BY RANGE, TEXT NOT NULL, JSONB, INET, bcrypt-hashed recovery codes, 10 single-use codes, 5 req/min login, 60 req/min default, 429 Retry-After, CSP default-src 'none', HSTS max-age 31536000, TLS 1.2/1.3, __Host-auth-token,__Host-csrf-token, double-submit cookie, 5 failures/15min lockout, 30min auto-unlock, 2-year configurable, 18+ event types, 30-day grace, AES-256-GCM KMS envelope, golang-migrate/Flyway, k6, Locust, OWASP ZAP, Playwright, Cypress, Prometheus, Grafana, PagerDuty, pg_dump, PITR WAL, blue-green deployment, RTO <1h, RPO <5min, RSA 2048-bit.
V2 Technology Decisions table (lines 693-707) adds 11 rows of named-technology-with-rationale pairs.
Count: approximately 70-75 concrete items.

**Variant 2 vague indicators:**
"appropriate" — 0 uses. "as needed" — 0 uses. "properly" — 0 uses. "suitable" — 0 uses. "reasonable" — not found. V2 uses "e.g." extensively but with concrete examples. "or equivalent" appears 5 times (Prometheus "or equivalent", Playwright or Cypress, golang-migrate or Flyway).
Count: approximately 5 vague items.

**V2 SR = 72 / (72 + 5) = 0.935**

Both variants are highly specific. V1 edges slightly higher because it uses fewer "or equivalent" hedges. V2's Technology Decisions rationale table is a significant specificity boost that partially compensates for the hedges.

### Metric 4: Dependency Completeness (DC, weight 0.15)

Internal references checked for existence of referenced entity within the same document.

**Variant 1:**

- Milestone refs (M0-M9): all 10 milestones defined and cross-referenced. Milestone Summary Table (line 15) lists all with dependencies.
- Deliverable refs (D-M0.1 through D-M9.5): all deliverables defined within their milestone sections. Spot-checked D-M0.1 (line 41), D-M1.1 (line 84), D-M6.4 (line 317), D-M9.5 (line 464) — all present.
- Traceability matrix refs to FR/NFR/R: all resolve to defined sections.
- Risk refs (R-001 through R-004): defined in source spec and referenced throughout.
- ADR refs (ADR-001 through ADR-004): all defined at D-M0.4 (line 53).
- "M3 expansion" ref (line 146) resolves to M3 section.
- CI refs (Semgrep rule at line 102) are external, not internal.
- No orphaned internal references detected.

**V1 DC = 1.000**

**Variant 2:**

- Milestone refs (M1-M12): all 12 milestones defined. Milestone Summary (line 8) lists all.
- Deliverable refs (D-M1.1 through D-M12.8): all defined within milestone detail sections. Spot-checked D-M1.1 (line 92), D-M5.2 (line 294), D-M10.3 (line 476), D-M12.8 (line 534) — all present.
- Traceability matrix refs to FR/NFR/R: all resolve.
- Implicit Prerequisites table refs (D-M1.4, D-M3.5, etc.) resolve to deliverables.
- "M3-M8 feature-complete" ref at line 617 — M3 through M8 are all defined.
- No orphaned internal references detected.

**V2 DC = 1.000**

Both variants have excellent internal cross-referencing with no orphaned references.

### Metric 5: Section Coverage (SC, weight 0.15)

Count of top-level (H2) sections:

**Variant 1 (17 H2 sections):**

1. Architectural Philosophy
2. Milestone Summary Table
3. M0 — Foundations & Threat Model
4. M1 — Data Layer & Crypto Primitives
5. M2 — Core Auth: Registration + Login + JWT
6. M3 — Sessions, Refresh Tokens & Password Reset
7. M4 — RBAC & Authorization
8. M5 — OAuth2 (Google + GitHub)
9. M6 — 2FA, Rate Limiting & Audit Logging
10. M7 — Admin Dashboard & Operational Readiness
11. M8 — Verification: Load, Security, Compliance
12. M9 — Production Cutover & Hardening
13. Traceability Matrix
14. Sequencing & Critical Path
15. Verification & Success Criteria Summary
16. Implicit Prerequisites Surfaced
17. Risks Created by This Roadmap (Meta-Risks)

**SC_V1 = 17/17 = 1.000**

**Variant 2 (9 H2 sections):**

1. Milestone Summary
2. Critical Path
3. Implicit Prerequisites (Not in Source Spec)
4. Milestone Detail
5. Traceability Matrix
6. Sequencing & Critical Path Analysis
7. Verification & Success-Criteria Section
8. Technology Decisions & Rationale
9. Blast Radius Analysis

**SC_V2 = 9/17 = 0.529**

Note: V2 consolidates all 12 milestones under a single H2 "Milestone Detail" using H3 subsections. This is a valid structural choice but is penalized by this metric, which counts top-level structural breadth. V2 compensates with unique sections (Technology Decisions, Blast Radius Analysis) that V1 lacks. The 0.529 score reflects the flatter hierarchy, not inferior content.

### Quantitative Score Calculation

| Metric | Weight | V1 Score | V1 Weighted | V2 Score | V2 Weighted |
|---|---|---|---|---|---|
| RC (Requirement Coverage) | 0.30 | 1.000 | 0.300 | 1.000 | 0.300 |
| IC (Internal Consistency) | 0.25 | 0.988 | 0.247 | 0.980 | 0.245 |
| SR (Specificity Ratio) | 0.15 | 0.967 | 0.145 | 0.935 | 0.140 |
| DC (Dependency Completeness) | 0.15 | 1.000 | 0.150 | 1.000 | 0.150 |
| SC (Section Coverage) | 0.15 | 1.000 | 0.150 | 0.529 | 0.079 |
| **Total** | **1.00** | | **0.992** | | **0.914** |

**quant_score_V1 = 0.992**
**quant_score_V2 = 0.914**

---

## Qualitative Scoring (50% weight)

### Claim-Evidence-Verdict (CEV) Protocol

For each criterion: CLAIM states whether the criterion is met; EVIDENCE provides direct quote or "no evidence found"; VERDICT is MET (1) or NOT MET (0). No partial credit. If specific evidence cannot be cited, verdict defaults to NOT MET.

---

### Dimension 1: Completeness (5 criteria)

**Criterion 1.1: Covers all explicit requirements from source input**

| Variant | CEV |
|---|---|
| V1 | CLAIM: Met. EVIDENCE: Traceability Matrix (lines 482-513) maps all 12 FRs, 6 NFRs, 4 risks with explicit milestone+deliverable assignments. FR-001 through FR-012 each appear with milestone and deliverable IDs. VERDICT: **MET (1)** |
| V2 | CLAIM: Met. EVIDENCE: Traceability Matrix (lines 548-570, 576-579) maps all 12 FRs, 6 NFRs, 4 risks. Each FR/NFR/R has milestone, deliverable(s), and verification method. VERDICT: **MET (1)** |

**Criterion 1.2: Addresses edge cases and failure scenarios**

| Variant | CEV |
|---|---|
| V1 | CLAIM: Partially met. EVIDENCE: Password reuse detection (D-M3.1 reuse detection), Redis failure degradation (M3 exit criteria: "auth degrades to 'no new logins'"), timing-attack resistance (M3 exit criteria: "response time variance <5ms"), constant-time token comparison (D-M2.2), OAuth provider fallback (D-M5.5). However: no explicit null-email OAuth handling, no CSRF deliverable, no password history. Invariant probe found INV-005 (legitimate concurrent device refresh), INV-002 (null email), INV-003 (JWT post-deactivation) — edge cases unaddressed. VERDICT: **NOT MET (0)** — multiple edge cases unaddressed per invariant probe. |
| V2 | CLAIM: Partially met. EVIDENCE: Password history (D-M7.5: "cannot reuse last 5 passwords"), CSRF protection (D-M6.8: double-submit cookie), rate limit exhaustion handling (D-M6.5: "429 with Retry-After header"), account lockout with auto-unlock (D-M3.9: "auto-unlocks after 30min"). However: invariant probe found INV-001 (RBAC vacuum during parallel M4/M5), INV-002 (null email), INV-005 (concurrent device refresh), INV-009 (retention retroactive gap) — edge cases unaddressed. VERDICT: **NOT MET (0)** — multiple edge cases unaddressed per invariant probe. |

**Criterion 1.3: Includes dependencies and prerequisites**

| Variant | CEV |
|---|---|
| V1 | CLAIM: Met. EVIDENCE: Milestone Summary Table (lines 15-28) has explicit "Depends On" column for every milestone. Dependencies section (lines 516-523) maps PostgreSQL 15+, Redis 7.2, SendGrid, Docker to first-use and establishing milestones. "Implicit Prerequisites Surfaced" section (lines 591-603) lists 9 unstated prerequisites including NTP, TLS termination, DKIM/SPF/DMARC, CORS, mobile strategy, cost model. VERDICT: **MET (1)** |
| V2 | CLAIM: Met. EVIDENCE: Milestone Summary (lines 8-23) has "Depends On" column. "Implicit Prerequisites (Not in Source Spec)" section (lines 49-64) lists 10 implicit prerequisites with rationale, milestone, and deliverable mapping. M1 scope (line 86) explicitly addresses all four declared dependencies from the spec. VERDICT: **MET (1)** |

**Criterion 1.4: Defines success/completion criteria**

| Variant | CEV |
|---|---|
| V1 | CLAIM: Met. EVIDENCE: Every milestone has explicit "Exit Criteria" subsection (M0 lines 62-67, M1 lines 104-109, M2 lines 152-157, M3 lines 194-198, etc.). "Verification & Success Criteria Summary" section (lines 567-587) provides cross-cutting verification suites and compliance sign-offs. Launch gate at M9 (lines 585-587) specifies 14-day canary, incident drill, and backup drill. VERDICT: **MET (1)** |
| V2 | CLAIM: Met. EVIDENCE: Every milestone has explicit "Exit criteria" (M1 line 100, M2 line 207, M3 line 244, etc.). "Pre-Launch Verification Checklist" (lines 664-680) has 15 checkbox items. "Success Criteria Verification" table (lines 583-589) maps each criterion to verification method and milestone. VERDICT: **MET (1)** |

**Criterion 1.5: Specifies what is explicitly out of scope**

| Variant | CEV |
|---|---|
| V1 | CLAIM: Not met at document level. EVIDENCE: Source spec defines out-of-scope items (biometric, hardware keys, custom SSO). V1 references mobile/native client strategy as "not in scope for v1 but should be documented" (line 600). However, V1 does not have a dedicated out-of-scope section listing what the roadmap itself excludes. The Meta-Risks section (lines 607-614) identifies risks created by the roadmap but does not enumerate explicit exclusions beyond the mobile note. VERDICT: **NOT MET (0)** — no dedicated out-of-scope section or enumerated exclusions beyond one inline mention. |
| V2 | CLAIM: Not met at document level. EVIDENCE: No "Out of Scope" section found. V2 does not enumerate what the roadmap explicitly excludes. Searched all H2 sections and milestone scopes. The source spec's out-of-scope items (biometric, hardware keys, custom SSO) are not re-stated or extended. VERDICT: **NOT MET (0)** — no out-of-scope enumeration. |

**Dimension 1 Subtotal: V1 = 3/5, V2 = 3/5**

---

### Dimension 2: Correctness (5 criteria)

**Criterion 2.1: No factual errors or hallucinated claims**

| Variant | CEV |
|---|---|
| V1 | CLAIM: Substantially met with one defect. EVIDENCE: Technical claims (Argon2id parameters, RS256, JWT structure, Redis patterns, PostgreSQL features) are consistent with current standards. ADR-002 Argon2id m=64MB/t=3/p=4 matches OWASP recommendations. One factual issue: V1 R2 claimed V2 lacked reuse detection, but V2 D-M3.7 has it — this was an external claim in debate, not a claim in the roadmap itself. Within the roadmap document, no hallucinated libraries or version numbers detected. The X-001 contradiction (2FA sequencing claim vs actual ordering) is a consistency issue, not a factual error. VERDICT: **MET (1)** — no factual errors in the roadmap artifact itself. |
| V2 | CLAIM: Substantially met with one defect. EVIDENCE: Technical claims in Technology Decisions table are correct (Argon2id OWASP 2023 recommendation, RS256 asymmetric properties, AES-256-GCM properties). X-002 factual error: "~77 days on the critical path" contradicts the document's own calculation of 44 days — this is a factual error within the artifact. X-003 (8-9 vs 10-11 weeks) compounds it. VERDICT: **NOT MET (0)** — X-002 is a factual arithmetic error within the document. |

**Criterion 2.2: Technical approaches feasible with stated constraints**

| Variant | CEV |
|---|---|
| V1 | CLAIM: Mostly met. EVIDENCE: Argon2id at m=64MB/t=3/p=4 at ~250ms per hash is feasible on modern hardware. PostgreSQL 15 RANGE partitioning for audit events is standard. Redis session store with AOF persistence is standard practice. RS256 with JWKS endpoint is standard JWT architecture. However: INV-006 identifies that 250ms hash alone exceeds the 200ms NFR-001 p95 target — this is a feasibility tension. INV-008 identifies that DEK rotation destroys ALL users' data, not per-user — feasibility issue for GDPR individual erasure. VERDICT: **NOT MET (0)** — INV-006 and INV-008 represent feasibility gaps. |
| V2 | CLAIM: Mostly met. EVIDENCE: Similar feasible approaches. However: INV-006 also applies to V2 (<500ms hash exceeds 200ms NFR). INV-001/INV-004/INV-010 identify parallel M4/M5 sequencing as creating an infeasible authorization state during development. VERDICT: **NOT MET (0)** — INV-006 applies; M4/M5 parallel creates infeasible intermediate state. |

**Criterion 2.3: Terminology used consistently and accurately**

| Variant | CEV |
|---|---|
| V1 | CLAIM: Met. EVIDENCE: JWT terminology (access token, refresh token, jti, kid, JWKS) used consistently. RBAC terms (role, permission, resource:action) defined at D-M4.1 and used consistently through D-M4.2. "Opaque refresh token" used consistently vs "JWT access token." PostgreSQL-specific terms (CITEXT, UUID v7, RANGE partition) used correctly. Argon2id parameters named consistently. VERDICT: **MET (1)** |
| V2 | CLAIM: Met. EVIDENCE: JWT terminology consistent. RBAC terms defined at D-M5.1 and used consistently. Schema SQL uses correct PostgreSQL types (UUID, JSONB, INET, TIMESTAMPTZ). Technology Decisions table uses consistent terminology throughout. "Envelope encryption" used correctly in context of KMS. VERDICT: **MET (1)** |

**Criterion 2.4: No internal contradictions (cross-validated with IC metric)**

| Variant | CEV |
|---|---|
| V1 | CLAIM: Not met. EVIDENCE: X-001 — Architectural Philosophy (line 11) states "2FA (FR-007) precedes OAuth" but milestone ordering places M5=OAuth before M6=2FA. V1 advocate conceded this as a documentation defect. The "soft sequencing" note at line 563 acknowledges the reversal but does not resolve the contradiction in the philosophy statement. VERDICT: **NOT MET (0)** |
| V2 | CLAIM: Not met. EVIDENCE: X-002 — Summary line 24 claims "~77 days on the critical path"; critical path calculation at line 628 yields 44 days. X-003 — Summary line 24 claims "8-9 weeks" wall-clock; detailed schedule at line 647 shows "~10-11 weeks." Two independent internal contradictions. VERDICT: **NOT MET (0)** |

**Criterion 2.5: Claims supported by evidence/rationale within the document**

| Variant | CEV |
|---|---|
| V1 | CLAIM: Mostly met. EVIDENCE: ADRs provide rationale for key decisions (token strategy, hashing, schema, framework). "Architectural Philosophy" section provides rationale for security-first approach and sequencing. "Risks Addressed" subsections in each milestone link deliverables to specific risks. Exit criteria provide evidence expectations. However: 250ms hash target vs 150ms login p95 claim is not reconciled. 7-year retention is stated without citation to specific regulation (mentions "financial-services bar" without naming one). VERDICT: **MET (1)** — rationale is present for most claims; gaps are in precision, not absence. |
| V2 | CLAIM: Met. EVIDENCE: Technology Decisions & Rationale table (lines 693-707) provides explicit rationale for 11 technology choices. Blast Radius Analysis section (lines 712-720) provides rationale for 6 design decisions. Each milestone has risk mitigation subsections. "Implicit Prerequisites" section provides rationale for surfacing hidden dependencies. Exit criteria provide evidence expectations. VERDICT: **MET (1)** |

**Dimension 2 Subtotal: V1 = 2/5, V2 = 2/5**

---

### Dimension 3: Structure (5 criteria)

**Criterion 3.1: Logical section ordering**

| Variant | CEV |
|---|---|
| V1 | CLAIM: Met. EVIDENCE: Ordering follows: Philosophy → Summary → M0..M9 (chronological) → Traceability → Sequencing → Verification → Prerequisites → Meta-Risks. This follows standard roadmap convention: motivation, plan, cross-cutting verification, risks. Milestones are in dependency order (M0 before M1, etc.). VERDICT: **MET (1)** |
| V2 | CLAIM: Met. EVIDENCE: Ordering follows: Summary → Critical Path → Prerequisites → Milestone Detail (M1..M12 chronological) → Traceability → Sequencing → Verification → Tech Decisions → Blast Radius. Each milestone section follows consistent internal structure: Goal, Scope, Deliverables table, Risk mitigation, FR/NFR mapping, Exit criteria. VERDICT: **MET (1)** |

**Criterion 3.2: Consistent hierarchy depth**

| Variant | CEV |
|---|---|
| V1 | CLAIM: Met. EVIDENCE: Each milestone uses consistent H2 (##) with H3 (###) subsections for Deliverables, Exit Criteria, Risks Addressed. Milestone Summary Table at H2. Traceability Matrix at H2 with H3 subsections for FR, NFR, Risks, Dependencies, Success Criteria. No orphaned subsections detected. VERDICT: **MET (1)** |
| V2 | CLAIM: Met. EVIDENCE: All milestones under "Milestone Detail" H2 use H3 (###) for each milestone, with consistent internal structure: Goal, Scope, Deliverables table, Risk mitigation, FR mapping, Exit criteria. No orphaned subsections. VERDICT: **MET (1)** |

**Criterion 3.3: Clear separation of concerns between sections**

| Variant | CEV |
|---|---|
| V1 | CLAIM: Met. EVIDENCE: M0 = foundations, M1 = data layer, M2 = register/login, M3 = sessions/password reset, M4 = RBAC, M5 = OAuth, M6 = 2FA/rate/audit, M7 = admin/ops, M8 = verification, M9 = production. Each milestone has distinct scope. Traceability is separate from sequencing. Verification is separate from milestones. Implicit Prerequisites and Meta-Risks are their own sections. VERDICT: **MET (1)** |
| V2 | CLAIM: Met. EVIDENCE: M1 = infrastructure, M2 = schema, M3 = core auth, M4 = OAuth, M5 = RBAC, M6 = security hardening, M7 = user lifecycle, M8 = audit/GDPR, M9 = admin, M10 = load testing, M11 = security audit, M12 = launch. Each milestone has distinct scope with explicit Goal, Scope, Deliverables. Traceability separate from milestones. VERDICT: **MET (1)** |

**Criterion 3.4: Navigation aids (TOC, cross-references, or index)**

| Variant | CEV |
|---|---|
| V1 | CLAIM: Partially met. EVIDENCE: Milestone Summary Table (lines 15-28) serves as de facto TOC with IDs, names, durations, dependencies, deliverables, and risks. Traceability Matrix provides an index mapping requirements to locations. Sequencing section has ASCII diagram. However: no explicit Table of Contents at document start. No numbered section indices. Cross-references are by deliverable ID (D-M4.1) not by section number or link. VERDICT: **NOT MET (0)** — no explicit TOC; cross-references are implicit via deliverable IDs, not linked. |
| V2 | CLAIM: Partially met. EVIDENCE: Milestone Summary (lines 8-23) serves as TOC. Critical Path section has ASCII diagram. Dependency graph has ASCII diagram. However: no explicit Table of Contents. No internal hyperlinks or section numbers. Deliverable IDs (D-M3.1) provide implicit cross-referencing but no explicit navigation structure. VERDICT: **NOT MET (0)** — no explicit TOC; navigation relies on implicit structure. |

**Criterion 3.5: Follows conventions of the artifact type (roadmap)**

| Variant | CEV |
|---|---|
| V1 | CLAIM: Met. EVIDENCE: Roadmap conventions present: milestone-based phasing, dependency ordering, critical path analysis, traceability matrix, risk mapping, exit criteria per phase. Includes sequencing diagram, parallelization guidance, and launch gate criteria. VERDICT: **MET (1)** |
| V2 | CLAIM: Met. EVIDENCE: Roadmap conventions present: milestone-based phasing with 12 milestones, dependency graph, critical path calculation, traceability matrix, risk mitigations table, exit criteria per milestone, launch checklist, resource assignment. Includes explicit parallelization schedule with named roles. VERDICT: **MET (1)** |

**Dimension 3 Subtotal: V1 = 4/5, V2 = 4/5**

---

### Dimension 4: Clarity (5 criteria)

**Criterion 4.1: Unambiguous language (no 'should consider', 'might', 'as appropriate' without specifics)**

| Variant | CEV |
|---|---|
| V1 | CLAIM: Met. EVIDENCE: Imperative language throughout: "issues," "stores," "generates," "enforces," "returns." Exit criteria use measurable predicates: "p95 latency <150ms," "100% of test runs," "response time variance <5ms." One instance of "read-only root filesystem where possible" (line 44) — qualifier but scoped. Soft sequencing note uses "acceptable to swap if security review demands" (line 563) — conditional but specific about the condition. VERDICT: **MET (1)** |
| V2 | CLAIM: Met. EVIDENCE: Deliverable acceptance criteria are precise: "returns 201," "hash verification in <500ms," "detects reuse of revoked token." Exit criteria are specific: "10K active sessions; Redis memory within budget," "zero critical or high findings." Imperative language used for deliverables. VERDICT: **MET (1)** |

**Criterion 4.2: Concrete rather than abstract**

| Variant | CEV |
|---|---|
| V1 | CLAIM: Mostly met. EVIDENCE: Concrete endpoint paths (POST /api/v1/auth/register), concrete algorithms (Argon2id m=64MB/t=3/p=4), concrete libraries (argon2-cffi, node-argon2, ruff, Semgrep, k6). However: "application-layer envelope encryption with KMS-wrapped DEKs" (line 92) does not name a specific KMS provider (AWS KMS vs GCP KMS vs Vault Transit). Framework choice deferred to ADR-004. VERDICT: **MET (1)** — vast majority concrete; minor deferrals are explicitly flagged as decision points. |
| V2 | CLAIM: Met. EVIDENCE: Concrete endpoint paths (POST /auth/register), concrete schema SQL, concrete technologies in rationale table (argon2id, RS256, AES-256-GCM, Redis sliding window, TOTP, PostgreSQL partitioning). Concrete tool names (k6/Locust, OWASP ZAP, Playwright/Cypress, Prometheus, Grafana, PagerDuty). VERDICT: **MET (1)** |

**Criterion 4.3: Each section has a clear purpose**

| Variant | CEV |
|---|---|
| V1 | CLAIM: Met. EVIDENCE: Each milestone section states a "Goal:" paragraph that defines its purpose. Architectural Philosophy establishes principles. Traceability Matrix maps requirements. Sequencing shows dependencies. Verification defines testing strategy. Implicit Prerequisites surfaces hidden dependencies. Meta-Risks identifies risks introduced by the plan. VERDICT: **MET (1)** |
| V2 | CLAIM: Met. EVIDENCE: Each milestone has explicit "Goal:" statement. Milestone Summary provides overview. Critical Path shows dependency chain. Implicit Prerequisites explains rationale for each surfaced item. Technology Decisions provides rationale for each choice. Blast Radius Analysis justifies each isolation decision. VERDICT: **MET (1)** |

**Criterion 4.4: Acronyms and domain terms defined on first use**

| Variant | CEV |
|---|---|
| V1 | CLAIM: Partially met. EVIDENCE: TOTP is defined as "time-based one-time passwords" at first use in D-M6.1 (line 297). JWT is expanded at first use (line 7). RBAC is used without expansion — "Role-Based Access Control" expansion is implicit from context but not explicit. STRIDE is not expanded. CSP is not expanded (line 52). OWASP is not expanded. HIBP is not expanded (line 126). PKCE is not expanded (line 255). SLO is used without expansion. VERDICT: **NOT MET (0)** — multiple acronyms used without expansion on first use (STRIDE, CSP, HIBP, PKCE, SLO, OWASP). |
| V2 | CLAIM: Partially met. EVIDENCE: TOTP expanded as "time-based one-time passwords, RFC 6238" (line 311). JWT used at line 13 without prior expansion. CSP not expanded (line 313). OWASP not expanded. RBAC expanded parenthetically in source spec but not in roadmap itself. PKCE not expanded (line 253). CORS not expanded (line 59). VERDICT: **NOT MET (0)** — multiple acronyms used without expansion on first use (JWT, CSP, OWASP, PKCE, CORS, RBAC in the roadmap body). |

**Criterion 4.5: Actionable next steps or decision points clearly identified**

| Variant | CEV |
|---|---|
| V1 | CLAIM: Partially met. EVIDENCE: ADR-004 requires a framework decision ("pick one, document why"). M9.5 post-launch review generates "Backlog of M10+ improvements." Soft sequencing note identifies a decision point (2FA vs OAuth ordering). However: no explicit "open decisions" list or "next steps" section. No prioritized action items for the team starting work. The roadmap ends at M9 without post-launch action items. VERDICT: **NOT MET (0)** — decision points exist inline but are not consolidated; no explicit next-steps section. |
| V2 | CLAIM: Met. EVIDENCE: Pre-Launch Verification Checklist (lines 664-680) provides 15 actionable items. Ongoing Verification section (lines 684-688) provides daily/weekly/monthly/quarterly/annual cadence. Launch checklist at D-M12.7 has "30+ item checklist." Each milestone deliverable has acceptance criteria that serve as actionable items. Parallelization schedule assigns work by role and week. VERDICT: **MET (1)** |

**Dimension 4 Subtotal: V1 = 3/5, V2 = 4/5**

---

### Dimension 5: Risk Coverage (5 criteria)

**Criterion 5.1: Identifies at least 3 risks with probability and impact assessment**

| Variant | CEV |
|---|---|
| V1 | CLAIM: Partially met. EVIDENCE: V1 maps all 4 source-spec risks (R-001 through R-004) with explicit deliverable mitigations. Meta-Risks section (lines 607-614) identifies 4 additional risks (M0 scope creep, M6 bundle size, late blockers, provider API changes) with mitigations. However: neither the source-spec risks nor the meta-risks include explicit probability or impact ratings. The source spec has probability/impact for R-001..R-004 but V1 does not re-state or extend these ratings. VERDICT: **NOT MET (0)** — risks are identified with mitigations but without probability/impact ratings in the roadmap. |
| V2 | CLAIM: Not met. EVIDENCE: V2 maps all 4 source-spec risks (R-001 through R-004) with mitigations. Each milestone has a "Risk mitigation" subsection. However: V2 does not include probability or impact ratings for any risk. No risk matrix or heat map. No explicit probability assessment beyond the source spec. VERDICT: **NOT MET (0)** — risks identified but without probability/impact ratings. |

**Criterion 5.2: Provides mitigation strategy for each identified risk**

| Variant | CEV |
|---|---|
| V1 | CLAIM: Met. EVIDENCE: R-001 mitigation: D-M0.3 (CSP), D-M2.4 (HTTP-only cookies), D-M2.6 (headers), D-M3.1 (reuse detection) — lines 510. R-002 mitigation: D-M2.4 (prelim lockout), D-M6.2 (rate limit), D-M6.3 (lockout), D-M6.1 (2FA) — lines 511. R-003 mitigation: D-M5.5 (circuit breaker + fallback) — lines 512. R-004 mitigation: D-M1.2 (encryption), D-M4.4 (crypto erasure), D-M6.4 (tamper-evident audit) — lines 513. Meta-risks each have mitigations. VERDICT: **MET (1)** |
| V2 | CLAIM: Met. EVIDENCE: R-001 mitigation: D-M6.6 (CSP), D-M6.7 (HTTP-only cookies), D-M6.8 (CSRF) — lines 576. R-002 mitigation: D-M3.9 (lockout), D-M6.5 (rate limiting) — lines 577. R-003 mitigation: D-M4.5 (health check, graceful degradation) — lines 578. R-004 mitigation: D-M2.3 (AES-256-GCM), D-M6.9 (TLS), D-M8.4 (GDPR deletion), D-M8.5 (retention) — lines 579. VERDICT: **MET (1)** |

**Criterion 5.3: Addresses failure modes and recovery procedures**

| Variant | CEV |
|---|---|
| V1 | CLAIM: Met. EVIDENCE: Redis failure mode: M3 exit criteria specify "auth degrades to 'no new logins' but existing JWTs still validate." PostgreSQL failover: D-M8.5 chaos testing kills replicas. SendGrid failure: D-M2.3 circuit breaker + queued retry. OAuth failure: D-M5.5 circuit breaker + fallback to email/password. M7.5 runbooks cover: Redis outage, PostgreSQL primary failure, SendGrid outage, OAuth provider outage, credential leak, rate-limit storm, audit-log lag. Backup/restore: D-M7.6 pgBackRest with quarterly drill. VERDICT: **MET (1)** |
| V2 | CLAIM: Partially met. EVIDENCE: OAuth failure: D-M4.5 health check + graceful degradation. Rate limiter failure modes addressed in Blast Radius Analysis item 5 ("If rate limiting fails open..."). Backup/restore: D-M12.5 daily pg_dump + PITR with restore test. Redis failure: Blast Radius Analysis item 2 ("Redis failure degrades to slower DB lookups"). However: no explicit SendGrid circuit breaker (V2 D-M3.6 only mentions template IDs). No chaos testing deliverable. Runbooks listed as D-M12.4 but not detailed. VERDICT: **NOT MET (0)** — SendGrid failure mode not addressed; no chaos testing; runbook content not specified. |

**Criterion 5.4: Considers external dependencies and their failure scenarios**

| Variant | CEV |
|---|---|
| V1 | CLAIM: Met. EVIDENCE: SendGrid (D-M2.3 circuit breaker + retry queue, D-M8.5 SendGrid 503 injection test). OAuth providers (D-M5.5 health check + fallback, M5.5 60s circuit breaker). PostgreSQL (D-M7.6 pgBackRest + D-M8.5 replica kill test). Redis (D-M3.2 AOF persistence + M3 chaos test). TLS termination called out as prerequisite (line 72). VERDICT: **MET (1)** |
| V2 | CLAIM: Partially met. EVIDENCE: OAuth providers (D-M4.5 health check + fallback). PostgreSQL (D-M12.5 backup). Redis (Blast Radius Analysis item 2). However: SendGrid failure scenario not explicitly addressed beyond template configuration. No explicit circuit breaker for email. Email delivery failure mode is a gap acknowledged in INV-011. VERDICT: **NOT MET (0)** — SendGrid external dependency failure not addressed. |

**Criterion 5.5: Includes monitoring or validation mechanism for risk detection**

| Variant | CEV |
|---|---|
| V1 | CLAIM: Met. EVIDENCE: D-M7.2 Prometheus metrics (auth_logins_total{outcome}, auth_active_sessions, auth_rate_limit_hits_total). D-M7.3 Alertmanager rules (AuthErrorRateHigh, LoginLatencyP95High, RefreshTokenReuseDetected, OAuthProviderDown, AuditLogWriteFailure). D-M7.4 SLOs with error budgets. D-M7.3 burn-rate alerts using multi-window multi-burn-rate pattern. D-M6.4 hash-chain integrity verification job. VERDICT: **MET (1)** |
| V2 | CLAIM: Met. EVIDENCE: D-M12.2 Prometheus metrics (auth request rate, latency histogram, error rate, active sessions gauge, token issuance rate, rate limit rejections). D-M12.3 Alerting rules (error rate >1% for 2min, p95 >500ms for 5min, active sessions drop >20%, Redis connection failures, PostgreSQL replication lag >1s). D-M12.2 Grafana dashboards. Post-launch ongoing verification (daily smoke, weekly ZAP, monthly load test, quarterly pentest). VERDICT: **MET (1)** |

**Dimension 5 Subtotal: V1 = 4/5, V2 = 2/5**

---

### Dimension 6: Invariant & Edge Case Coverage (5 criteria) — CRITICAL DIMENSION

**Criterion 6.1: Addresses boundary conditions for collections (empty, single-element, max size)**

| Variant | CEV |
|---|---|
| V1 | CLAIM: Partially met. EVIDENCE: Account lockout counter boundary (D-M6.3: 10 failed / 15min) is specified but semantics ambiguous per INV-007. Refresh token reuse detection handles the "first reuse" boundary. Rate limit burst allowance (D-M6.2: 2x for 10s) addresses burst boundary. Session enumeration (D-M3.5) implies non-empty but empty-session case not addressed. INV-009 (V2) and INV-008 (V1) show partition boundaries not fully addressed. INV-005 shows concurrent refresh boundary not handled. VERDICT: **NOT MET (0)** — INV-007 (lockout semantics), INV-005 (concurrent refresh), INV-008 (DEK all-users scope) represent unaddressed collection boundaries. |
| V2 | CLAIM: Partially met. EVIDENCE: Account lockout at 5 failures (D-M3.9) — boundary ambiguous per INV-007. Rate limit thresholds specified per endpoint. Recovery code count (10 single-use) has explicit tracking of remaining count. Pagination in admin API implied but empty-result case not addressed. INV-009 (retention retroactive gap) and INV-001/INV-010 (empty-role set during parallel phase) represent unaddressed boundaries. VERDICT: **NOT MET (0)** — INV-007, INV-009, INV-001, INV-010 represent unaddressed collection boundaries. |

**Criterion 6.2: Handles state variable interactions across component boundaries**

| Variant | CEV |
|---|---|
| V1 | CLAIM: Partially met. EVIDENCE: RBAC-before-OAuth sequencing (line 11) is an explicit state interaction guard — M4 RBAC must exist before M5 OAuth creates users. Permission cache invalidation via Redis pub/sub (D-M4.2) handles RBAC state propagation. However: INV-003 (JWT post-deactivation access window of 15min) is an unaddressed cross-component state interaction between deactivation service and JWT middleware. INV-005 (concurrent device refresh triggers false-positive theft detection) is an unaddressed interaction between refresh rotation and multi-device state. VERDICT: **NOT MET (0)** — INV-003 and INV-005 are unaddressed cross-component state interactions. |
| V2 | CLAIM: Partially met. EVIDENCE: INV-001 (OAuth auto-provisioning creates user before RBAC default-role hook merges during parallel M4/M5) is an unaddressed cross-component state interaction. INV-004 (RBAC cache serves empty permissions for 5min during parallel phase) compounds it. INV-003 (JWT post-deactivation) same as V1. INV-005 (concurrent device refresh) same as V1. VERDICT: **NOT MET (0)** — INV-001, INV-004, INV-003, INV-005 are unaddressed cross-component state interactions. |

**Criterion 6.3: Identifies guard condition gaps (missing validation, unguarded type assumptions)**

| Variant | CEV |
|---|---|
| V1 | CLAIM: Not met. EVIDENCE: INV-002 (GitHub OAuth null email violates users.email NOT NULL constraint) — V1 has `email CITEXT UNIQUE` in schema (D-M1.1, line 85) but no null-check guard in OAuth callback. INV-012 (no emergency key-compromise procedure distinct from planned rotation) — guard gap in key lifecycle. V1 relies on SameSite=Strict for CSRF without explicit CSRF token validation — guard gap conceded in debate. VERDICT: **NOT MET (0)** — INV-002 (null email), INV-012 (key compromise), conceded CSRF gap. |
| V2 | CLAIM: Not met. EVIDENCE: INV-002 (same null email issue — `email TEXT NOT NULL` at line 123 but no null-check in D-M4.3 OAuth callback). INV-012 (same key compromise gap — D-M3.5 handles planned rotation only). INV-001/INV-010 (no guard preventing M4 OAuth from completing before M5 RBAC merges). VERDICT: **NOT MET (0)** — INV-002, INV-012, INV-001/INV-010 guard condition gaps. |

**Criterion 6.4: Covers count divergence scenarios (off-by-one, inclusive/exclusive ranges)**

| Variant | CEV |
|---|---|
| V1 | CLAIM: Not met. EVIDENCE: INV-007 (lockout counter: "10 failed login attempts in 15min" — ambiguous whether failure #10 triggers lockout or is the last allowed attempt). No explicit off-by-one specification for any counter. INV-006 (Argon2id 250ms hash exceeds NFR-001 200ms budget — count divergence between component-level timing and system-level SLO). VERDICT: **NOT MET (0)** — INV-007 and INV-006 represent count/threshold divergences. |
| V2 | CLAIM: Not met. EVIDENCE: INV-007 (same lockout ambiguity: "locks after 5 failures in 15min"). INV-006 (same hash-vs-NFR budget divergence, worse at <500ms upper bound). VERDICT: **NOT MET (0)** — INV-007 and INV-006. |

**Criterion 6.5: Considers interaction effects when features or components combine**

| Variant | CEV |
|---|---|
| V1 | CLAIM: Partially met. EVIDENCE: V1 explicitly considers the interaction of rate limiting + account lockout (D-M6.2 + D-M6.3 operate independently on different counters). INV-013 confirms these reinforce without interference. Blast Radius Analysis equivalent via architectural philosophy. However: INV-005 (refresh token reuse + multi-device interaction), INV-003 (deactivation + JWT self-validation interaction), INV-015 (crypto erasure + pseudonymization interaction on GDPR compliance) are unaddressed. VERDICT: **NOT MET (0)** — INV-005, INV-003, INV-015 interaction effects unaddressed. |
| V2 | CLAIM: Partially met. EVIDENCE: Blast Radius Analysis section explicitly analyzes 6 interaction effects. INV-013 (rate limit + lockout) confirmed as correctly reinforcing. However: INV-001/INV-004/INV-010 (OAuth + RBAC parallel interaction), INV-005 (refresh + multi-device), INV-011 (SendGrid + user experience interaction) are unaddressed. VERDICT: **NOT MET (0)** — INV-001/004/010, INV-005, INV-011 interaction effects unaddressed. |

**Dimension 6 Subtotal: V1 = 0/5, V2 = 0/5**

---

### Edge Case Floor Check

Per protocol: Variants scoring <1/5 on Dimension 6 are INELIGIBLE as base variant.

**V1 Dimension 6 score: 0/5 — INELIGIBLE**
**V2 Dimension 6 score: 0/5 — INELIGIBLE**

Both variants are formally ineligible under the Edge Case Floor Rule. The R2.5 invariant probe found 9-10 HIGH-UNADDRESSED items, confirming that neither variant adequately addresses invariant and edge case coverage. However, since convergence was NOT_CONVERGED and the protocol mandates forced selection by combined score, we proceed with scoring and note both variants' ineligibility. The assembly step must address these invariant gaps as a primary remediation priority.

---

## Qualitative Summary

### Dimension Subtotals

| Dimension | V1 Score | V2 Score |
|---|---|---|
| 1. Completeness | 3/5 | 3/5 |
| 2. Correctness | 2/5 | 2/5 |
| 3. Structure | 4/5 | 4/5 |
| 4. Clarity | 3/5 | 4/5 |
| 5. Risk Coverage | 4/5 | 2/5 |
| 6. Invariant & Edge Cases | 0/5 | 0/5 |
| **Total** | **16/30** | **15/30** |

**qual_score_V1 = 16/30 = 0.533**
**qual_score_V2 = 15/30 = 0.500**

---

## Position-Bias Mitigation

### Method

Each criterion-variant pair was evaluated in two passes:

- Pass 1: Evaluate [V1, V2] order
- Pass 2: Evaluate [V2, V1] order

### Disagreements Found

**Disagreement 1 — Criterion 2.1 (No factual errors):**

- Pass 1 (V1 first): V1 seemed cleaner, V2 had obvious X-002 error. V1 = MET, V2 = NOT MET.
- Pass 2 (V2 first): Same result. V2's arithmetic error is objectively present. V1 has X-001 but that is a consistency issue, not a factual error about external reality. No disagreement.
- Resolution: Consistent. V1 = MET, V2 = NOT MET.

**Disagreement 2 — Criterion 4.5 (Actionable next steps):**

- Pass 1 (V1 first): V1's ADR-004 decision point and soft-sequencing note felt sufficient. V1 = MET.
- Pass 2 (V2 first): After seeing V2's explicit pre-launch checklist, parallelization schedule, and ongoing verification cadence, V1's inline decision points appeared weaker. V1 = NOT MET is more defensible.
- Resolution: Disagreement resolved to V1 = NOT MET, V2 = MET. V2 has consolidated actionable checklists and role-assigned schedules that V1 lacks. V1's decision points are inline and not consolidated.

**Disagreement 3 — Criterion 5.3 (Failure modes and recovery):**

- Pass 1 (V1 first): V1's chaos testing, runbooks, circuit breakers, and quarterly restore drills stood out. V2 seemed adequate with Blast Radius. V2 = MET.
- Pass 2 (V2 first): After reading V2 first, the absence of SendGrid circuit breaker and chaos testing became more apparent. V2's D-M12.4 runbooks are listed but not detailed. V2 = NOT MET is more defensible.
- Resolution: Disagreement resolved to V2 = NOT MET. V1 is clearly stronger on failure-mode coverage (chaos testing, detailed runbook list, SendGrid circuit breaker).

**Disagreement 4 — Criterion 1.5 (Out of scope):**

- Pass 1 (V1 first): Neither variant has a dedicated out-of-scope section. V1 has one inline mention. V1 = NOT MET, V2 = NOT MET.
- Pass 2: Same result. No disagreement.

No other disagreements were found. All other criterion pairs produced consistent verdicts across both passes.

### Summary

4 disagreements examined, 2 resolved with verdict changes (Criteria 4.5 and 5.3). Final scores reflect the position-bias-corrected verdicts.

---

## Combined Scoring

### Final Score Calculation

```
variant_score = (0.50 x quant_score) + (0.50 x qual_score)
```

| Component | Weight | V1 | V2 |
|---|---|---|---|
| Quantitative | 0.50 | 0.992 | 0.914 |
| Qualitative | 0.50 | 0.533 | 0.500 |
| **Combined** | **1.00** | **0.763** | **0.707** |

**V1 score: 0.763**
**V2 score: 0.707**
**Margin: 0.056**

The margin exceeds 0.05, so no tiebreaker is required. V1 wins on combined score.

### Tiebreaker Analysis (for completeness)

| Level | Criterion | V1 | V2 | Winner |
|---|---|---|---|---|
| L1 | Debate scoring matrix winners | ~6 | ~7 | V2 (slight) |
| L2 | Correctness criteria count | 2/5 | 2/5 | Tie |
| L3 | Input order | V1 | — | V1 |

Tiebreaker would not change the outcome; V1 wins on combined score with margin > 0.05.

---

## Selected Base

### **Variant 1 (opus-default) is selected as the base variant.**

**Score: V1 = 0.763 vs V2 = 0.707 (margin 0.056)**

**Eligibility per Edge Case Floor: V1 INELIGIBLE, V2 INELIGIBLE.** Both variants score 0/5 on Dimension 6 (Invariant & Edge Case Coverage). Selection proceeds despite ineligibility per protocol no_convergence forced-selection clause. The assembly step MUST remediate these invariant gaps as its highest priority.

### Rationale

V1 wins on the strength of its quantitative dominance (0.992 vs 0.914), driven by perfect Section Coverage (17/17 H2 sections vs V2's 9/17) and slightly better Internal Consistency (1 contradiction vs 2). The quantitative margin (0.078) overcomes V2's slight qualitative edge on Clarity (4/5 vs 3/5). Qualitatively, V1 excels in Risk Coverage (4/5 vs 2/5) due to its chaos testing deliverable, explicit circuit breakers, detailed runbooks, and SendGrid retry queue — all of which V2 lacks. Both variants share the same 0/5 on Dimension 6, confirming the invariant probe's finding that neither variant adequately handles edge cases and state interactions.

### Strengths to Preserve from V1 (base)

1. **M0 Foundations & Threat Model milestone** — dedicated pre-implementation phase with STRIDE threat model, 4 ADRs, Vault integration, and CI/CD skeleton. This is structurally correct security-first sequencing.
2. **RBAC-before-OAuth hard sequencing constraint** — prevents the authorization vacuum that V2's parallel M4/M5 creates (INV-001/INV-010).
3. **Tamper-evident audit trail** — hash chain with daily Merkle root (D-M6.4) provides cryptographic tamper detection, not just prevention. Strictly stronger than V2's role-permission-only approach (INV-014).
4. **DPIA deliverable** — GDPR Article 35 requirement for high-risk processing; V2 omits this entirely.
5. **SRE-grade observability** — multi-window multi-burn-rate alerts, explicit error budget (43.8 min/month), detailed Alertmanager rules.
6. **Chaos / resilience testing** — dedicated D-M8.5 with PostgreSQL replica kill, Redis node kill, SendGrid 503 injection.
7. **Comprehensive failure-mode coverage** — SendGrid circuit breaker + retry queue, detailed runbook list (7 specific scenarios), quarterly backup restore drill.

### Strengths to Incorporate from V2 (non-base)

1. **CSRF protection as dedicated deliverable** — D-M6.8 double-submit cookie pattern with `__Host-csrf-token`. V1 conceded this gap.
2. **Password history enforcement** — D-M7.5 "cannot reuse last 5 passwords." V1 conceded this gap.
3. **Technology Decisions & Rationale table** — 11-row explicit table naming technologies with rationale. Adopt this format to increase specificity.
4. **Blast Radius Analysis section** — 6 named design choices that limit failure impact. This explicit failure-isolation reasoning complements V1's threat model.
5. **Pre-launch verification checklist** — 15-item structured checklist (lines 664-680). V1 has per-milestone exit criteria but no consolidated pre-launch gate list.
6. **Ongoing verification cadence** — daily/weekly/monthly/quarterly/annual post-launch verification schedule. V1 stops at M9 production cutover.
7. **Parallelization schedule with named roles** — week-by-week 3-person assignment table. V1 is team-agnostic; incorporating resource estimates improves executability.
8. **V2's Week-by-week schedule format** — actionable resource planning that V1's narrative approach lacks.

### Mandatory Remediation Priorities (from Invariant Probe)

The assembly step must address these HIGH-UNADDRESSED invariants regardless of which variant is base:

1. **INV-002**: Null-email handling in OAuth callback (both variants)
2. **INV-005**: Concurrent device refresh false-positive theft detection (both variants)
3. **INV-006**: Argon2id hash time vs NFR-001 200ms budget reconciliation (both variants)
4. **INV-008**: V1's DEK rotation destroys all users' PII, not per-user (base variant issue)
5. **INV-012**: No emergency key-compromise procedure distinct from planned rotation (both variants)
6. **INV-015**: V1's crypto erasure + pseudonymization may not satisfy strict GDPR Article 17 (base variant issue)

---

*End of base selection. Proceed to Step 4: Refactoring Plan.*
