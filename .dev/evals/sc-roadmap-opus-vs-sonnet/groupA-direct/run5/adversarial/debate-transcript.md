# Adversarial Debate Transcript

## Metadata

- **Depth**: standard
- **Rounds executed**: Round 1 (parallel), Round 2 (sequential), Round 2.5 (invariant probe). Round 3 skipped (--depth standard).
- **Convergence achieved**: see assessment below
- **Convergence threshold**: 0.80
- **Focus areas**: All (no `--focus` constraint)
- **Advocate count**: 2 (V1=opus, V2=sonnet)
- **Fault-finder agent**: 1 (opus, independent)

---

## Round 1: Advocate Statements (Parallel)

### V1 Advocate (opus) — Round 1

**Position Summary**: V1 delivers a security-first, standards-grounded roadmap that satisfies OWASP/GDPR/NFRs with verifiable defaults (Argon2id, PKCE, family-revocation, k8s HPA+PDB, STRIDE threat model, burn-rate SLOs). V2 makes choices that are concrete and ergonomic but ship a measurably weaker security posture (bcrypt-12, no PKCE deliverable, unbounded audit retention) and an infrastructure topology (Docker Compose, 2 replicas, no HPA) that cannot simultaneously satisfy NFR-002, NFR-005, and rolling deploys.

**Steelman of V2**: V2's strongest case is execution readiness — pinned Python/FastAPI stack, 14-week timeline, per-PR Schemathesis contract gate, EXPLAIN ANALYZE query-plan CI, 50K-user admin-list latency gate, Redis Sentinel, email-change-keeps-old-email-valid. These are operationally sharp deliverables V1 lacks. bcrypt cost-12 is on the OWASP-acceptable list (just weaker).

**Strengths claimed for V1 (with evidence)**:

1. Argon2id m=64MB/t=3/p=4 per OWASP ASVS 4.0 §2.4 (V1 line 36) — OWASP's first recommendation.
2. RFC 9700 §2.2.2 refresh-token family revocation on reuse (V1 line 72-73, D2.5).
3. Explicit PKCE+S256 (V1 line 104) — RFC 9700 §2.1.1 mandates it; V2 omits.
4. STRIDE threat model as M1 gate D1.7 (line 39).
5. k8s HPA + PDB min-available=2 (line 183 D5.4) sized to NFR-002+NFR-005.
6. OWASP A01-A10 mapping table (line 208) — verification artifact NFR-003 demands.
7. Audit retention 13mo hot + S3 7yr object-lock (line 148 D4.7) — SOC2/GDPR-aligned.
8. GDPR 72h breach runbook (line 187 D5.8).

**Weaknesses identified in V2 (with evidence)**:

1. bcrypt cost-12 (V2 line 34) under NFR-003 — cannot claim "OWASP verified" without justifying rejection of Argon2id.
2. JWT-signed email-verification token + 15-min TTL (V2 line 36) — opaque random preferred; 15min hostile to email delivery.
3. No PKCE deliverable (V2 D2.1/D2.2 lines 68-69) — RFC 9700 §2.1.1 violation.
4. Docker Compose for production HA (V2 line 178) — 2 replicas + nginx cannot meet 99.9% + 10K + rolling deploys.
5. No audit retention policy (V2 D3.4 line 107) — GDPR Art. 5(1)(e) requires retention.
6. `suspended` conflated with role (V2 D3.1 line 104).
7. fastapi-limiter without Lua atomicity (V2 D2.6 line 73) — races at 10K concurrent.

**Concessions in V1**:

- 18 weeks is generous; V2's 14 weeks plausible for 12-FR surface.
- Framework-agnostic wording "substitute equivalents" creates real decision debt.
- V1 omits Schemathesis-style internal contract testing (only external OIDC discovery).
- Role taxonomy `support` is invented; V2's spec-aligned roles closer to truth.
- V1 doesn't specify pagination defaults.
- V1 omits 50K-user admin-list latency gate.

**Shared-Assumption Responses**:

- A-001 (10K = sessions): **ACCEPT**
- A-002 (RBAC sufficient): **ACCEPT with note** (ABAC scope creep)
- A-003 (single-tenant): **QUALIFY** (should be surfaced in exec summary)
- A-005 (email-reset blast radius): **REJECT** (2FA-on-reset for 2FA-enabled accounts missing)
- A-007 (session not device): **QUALIFY** (consistent with spec)
- A-009 (spec is closed): **REJECT** (schedule spec-refresh checkpoints M2, M4)
- A-010 (audit retention): **REJECT V2's silence; ACCEPT V1's 7-year**

---

### V2 Advocate (sonnet) — Round 1

**Position Summary**: V2 delivers a complete, implementable auth system in 14 weeks by shipping user-facing core auth in M1 rather than deferring all features for a foundation-only sprint. Concrete tech, versioned API paths, per-PR contract testing, operational-realism acceptance criteria. V1's security foundations are stronger in isolation, but V2 co-delivers security with features for earlier validated value.

**Steelman of V1**: V1 gets multiple important things right — foundation-only M1 philosophy, OWASP A01-A10 mapping, RFC 9700 family revocation, PKCE+S256, progressive lockout, 7-year audit retention with object-lock, HIBP breached-password check, k8s HPA+PDB. These are real strengths V2 should adopt in convergence.

**Strengths claimed for V2 (with evidence)**:

1. M1 ships functional core auth, not just infra (V2 D1.1-D1.8 in 3 weeks).
2. Concrete pinned stack (Python 3.11+, FastAPI, pyotp v2.x, google-auth v2.x, fastapi-limiter, Schemathesis).
3. API versioning `/api/v1/auth/*` from day one (C-018).
4. Schemathesis contract testing every PR (U-013).
5. EXPLAIN ANALYZE query-plan CI enforcement (U-018).
6. Admin <500ms@50K users performance gate (U-020).
7. Email-change keeps old email active until new verified (C-017, U-015).
8. Redis Sentinel for automatic failover (U-016).
9. Markdown table deliverable format scannable for sprint planning (S-004).
10. 4 weeks shorter with no requirements gap.

**Weaknesses identified in V1 (with evidence)**:

1. Foundation-only M1 delays value and integration feedback (no endpoints until week 4).
2. Framework-agnostic wording creates decision debt.
3. No API versioning (`/auth/*` unversioned).
4. Threat model sits unvalidated against running code for 14 weeks.
5. No admin performance criterion.
6. Missing Redis failover specification entirely.

**Concessions in V2** (substantive):

- bcrypt → Argon2id (OWASP ASVS 4.0 §2.4 ranks Argon2id first).
- Docker Compose → Kubernetes HPA+PDB (Docker Compose cannot guarantee 99.9% at 10K).
- No PKCE → explicit PKCE+S256 (RFC 9700 §2.1.1 compliance gap).
- `suspended` conflated with role → status separation (cleaner taxonomy).
- No audit retention → V1's 13mo hot + S3 7yr object-lock.
- Single-tier lockout → V1's progressive lockout.

**Shared-Assumption Responses**:

- A-001 (10K = sessions): **ACCEPT**
- A-002 (RBAC suffices): **QUALIFY** (current scope OK; migration path needed)
- A-003 (single-tenant): **ACCEPT**
- A-005 (email-reset blast radius): **QUALIFY** (15-min TTL limits window vs. V1's 24h)
- A-007 (session != device): **QUALIFY** (V2 data model accommodates extension)
- A-009 (spec is closed): **QUALIFY** (validate at M3 midpoint)
- A-010 (audit retention): **REJECT V2's silence** (must adopt V1 policy; legal requirement, not optional)

---

## Round 2: Rebuttals (Sequential)

### V1 Advocate (opus) — Round 2

**Response to V2's critiques**:

1. **M1 foundation-only delays value** — **Concession with mitigation**. V1 M1 has testable artifacts but lacks an integration-test surface. **Adopt**: D1.8 "walking-skeleton login" by end of week 2-3 (no schedule impact — crypto/schema is the long pole).

2. **Framework-agnostic wording** — **Concession with caveat**. V1 should pin a stack. V2's Python/FastAPI choice is *also* spec-unsupported but more confidently stated. **Adopt**: week-0 ADR pinning a single stack.

3. **No API versioning** — **Full concession**. Adopt `/api/v1/auth/*` across M2-M5. Trivial change, no schedule impact.

4. **STRIDE threat model unvalidated** — **Partial rebuttal**. Every M2/M3/M4 acceptance criterion (ZAP, circuit-breaker test, brute-force simulation) is a STRIDE validation against running code. **Adopt explicitly**: add "STRIDE row revalidation" to each milestone gate.

5. **No admin performance gate** — **Concession**. Adopt `<500ms@50K users` + EXPLAIN ANALYZE CI verbatim into M5 load test.

6. **Missing Redis failover** — **Concession with scope clarification**. V1 D1.2 says "Redis-backed" but never specifies HA topology. Adopt Sentinel for dev/test + managed Redis on k8s for prod (V2's Docker-Compose Sentinel pattern is itself weak).

**Acknowledgement of V2 concessions + integration notes**:

| Concession | Second-order effect |
|------------|---------------------|
| bcrypt → Argon2id | ~10× slower per hash; revalidate NFR-001 math (likely fine on modern hw) |
| Docker Compose → k8s | **Non-trivial schedule hit** ~1-2 weeks platform work V2 hasn't budgeted |
| No PKCE → PKCE+S256 | Trivial code change |
| `suspended` as role → orthogonal status | Schema migration in V2 M3 |
| No audit retention → 13mo+7yr | S3 lifecycle job ~2 days |
| Single-tier → progressive lockout | Trivial logic |

**Headline**: V2's 14-week claim does not survive its own concessions. Realistic V2 is 16-17 weeks vs. V1's 18 weeks.

**Updated position**: V1's position is **strengthened** by Round 1. V2 conceded 6 substantive items (security/operations fundamentals); V1's concessions are *tactical polish*, not architectural pivots. Merged roadmap should use V1's milestone structure with V2's contributions adopted as specific upgrades.

---

### V2 Advocate (sonnet) — Round 2

**Response to V1's outstanding critiques**:

1. **JWT email verification token** — **Full concession**. Opaque 32-byte base64url with 24h TTL (V1's pattern) is strictly better. Trivial swap.

2. **Sliding-window rate-limiter racing** — **Concession**. fastapi-limiter's INCR+EXPIRE is non-atomic; V1's Lua-script token-bucket is correct. ~1-2 days additional work.

3. **Timeline survival after concessions** — **Honest accounting**:

   | Concession | Schedule impact |
   |------------|----------------|
   | Argon2id | ~0 days |
   | Opaque email tokens | ~0 days |
   | PKCE+S256 | ~2-3 days |
   | Audit retention | ~1 day |
   | STRIDE threat model in M1 | ~3-4 days |
   | Redis Lua rate limiter | ~1-2 days |
   | Status separation | ~1 day |
   | Walking skeleton | 0 days (V2 already has) |

   Total: ~1.5-2 weeks. V2 stretches to **15-16 weeks**, not 16-17. V2 still has a 2-3 week schedule advantage but compressed milestones (M3=2w, M4=2w) become fragile under added scope.

**Response to V1's R2 concessions**:

- API versioning, admin perf gate, walking-skeleton: all clean adopts.
- Redis Sentinel: split — Sentinel for dev/test, managed Redis on k8s for prod.
- Framework ADR: V2's library pinning captured as reference implementation inside ADR.
- STRIDE per-milestone revalidation: specify reviewer role + max turnaround (suggest 2 business days) to prevent gate stalls.
- Walking skeleton: V1's version is described as minimal; V2's full M1 still has a richer integration surface.

**Final position**: **V1 should be the merge base.** V2 contributions should be folded as amendments. V2's role was to pressure-test V1's omissions and provide concrete implementation details — mission accomplished.

V2 contributions for V1 to adopt:

- `/api/v1/` versioned paths
- Admin <500ms@50K gate + query-plan CI
- Email-change keeps old email active
- Redis Sentinel (dev/test)
- Schemathesis contract testing on every PR
- Pagination semantics (default 50, max 200)
- FastAPI/Python library pinning in week-0 ADR (reference)

**Updated shared-assumption stances** (V2 final):

- A-010: **Resolved in V1's favor** — V2's silence was wrong; 13mo+7yr adopted.
- Other assumptions: unchanged from R1.

---

## Round 2.5: Invariant Probe

Independent fault-finder agent (opus, NOT advocating for either variant) probed the emerging consensus for invariant violations across 6 categories.

**Summary** (full table in `invariant-probe.md`):

- 16 findings total, all UNADDRESSED
- 6 HIGH severity (INV-001, INV-003, INV-010, INV-011, INV-013, INV-015)
- 8 MEDIUM, 2 LOW

**Top HIGH items**:

- INV-001: Pending-email state representation (V1 schema + V2 keep-old-email behavior collide)
- INV-003: Admin-promotion path bypasses mandatory-2FA invariant
- INV-010: pgcrypto AES-256-GCM email + unique btree mutually exclusive without blind-index
- INV-011: S3 object-lock 7yr vs. GDPR Art. 17 erasure — no PII redaction pre-archive
- INV-013: NFR-001 sufficiency — gates ignore Argon2id cold-process, RBAC cold-cache, decryption tax
- INV-015: NFR-005 sufficiency — SLO scope + serial-dependency availability product unbounded

---

## Round 3: SKIPPED

Skipped per `--depth standard` (Round 3 fires only at `--depth deep` AND convergence < threshold).

---

## Scoring Matrix

Per-point scoring (winner, confidence, evidence summary):

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|------------------|
| S-001 | V2 | 60% | Timeline (14w realistic given 12-FR surface); V1 stretches to 18 with foundation-only M1 |
| S-002 | Merged | 75% | Adopt V1's foundation depth + V2's walking-skeleton M1 = best of both |
| S-003 | V1 | 70% | Risk-mitigation placement more thorough in V1 |
| S-004 | V2 | 70% | Table format scannable; V2 advocate cited sprint-planning use |
| S-005 | Tie | 90% | Both variants align on top-level section structure |
| C-001 | V1 | 95% | Argon2id wins under OWASP ASVS 4.0 §2.4; V2 conceded |
| C-002 | V2 | 75% | Pinned stack better; V1 conceded; both flavors of arbitrary spec-wise |
| C-003 | V1 | 60% | 30-day TTL with family revocation acceptable; V2's 7-day defensible but reduces refresh-resilience |
| C-004 | V1 | 95% | PKCE+S256 explicit; V2 conceded |
| C-005 | V1 | 90% | STRIDE threat model gate; V2 conceded |
| C-006 | V1 | 95% | 13mo+7yr retention; V2 conceded |
| C-007 | V1 | 85% | Burn-rate alerts more rigorous; V2 has no SLO model |
| C-008 | V1 | 70% | Column-level pgcrypto more transparent (BUT see INV-010) |
| C-009 | V1 | 95% | k8s HPA+PDB; V2 conceded |
| C-010 | V2 | 70% | React 18 + TanStack specifics adopted by V1 |
| C-011 | V1 | 80% | Argon2id-hashed recovery codes (consistent with C-001) |
| C-012 | V1 | 85% | Progressive lockout; V2 conceded |
| C-013 | V1 | 90% | Lua-atomic; V2 conceded |
| C-014 | Tie | 80% | Both 30-day grace, substantively equivalent |
| C-015 | V1 | 90% | Opaque token; V2 conceded |
| C-016 | V1 | 85% | Status-orthogonal-to-role; V2 conceded |
| C-017 | V2 | 80% | Keep-old-email-valid (BUT see INV-001) |
| C-018 | V2 | 90% | `/api/v1/` versioning; V1 conceded |
| C-019 | V2 | 80% | Schemathesis per PR; V1 adopts as addition |
| C-020 | V2 | 85% | <500ms@50K gate; V1 conceded |
| X-001 | V1 | 95% | Argon2id; resolved by C-001 |
| X-002 | V1 | 95% | k8s HA; V2 conceded |
| X-003 | V1 | 95% | PKCE; V2 conceded |
| X-004 | V1 | 70% | Family-revocation mitigates 30-day TTL blast radius |
| U-001 | V1 | 90% | OWASP A01-A10 mapping; adopt |
| U-002 | V1 | 95% | RFC 9700 family revocation; adopt |
| U-003 | V1 | 90% | STRIDE threat model; adopt |
| U-004 | V1 | 90% | Audit retention; adopt |
| U-005 | V1 | 85% | Burn-rate alerts; adopt |
| U-006 | V1 | 85% | HIBP breached-password; adopt (BUT see INV-004) |
| U-007 | V1 | 80% | Mandatory 2FA for admin; adopt (BUT see INV-003) |
| U-008 | V1 | 85% | Chaos engineering acceptance tests; adopt |
| U-009 | V1 | 80% | GA readiness sign-off gate; adopt |
| U-010 | V1 | 85% | GDPR 72h breach runbook; adopt |
| U-011 | V1 | 65% | mTLS auth-api↔DB/Redis; adopt where topology supports |
| U-012 | V2 | 80% | Python library pinning; adopt as reference in ADR |
| U-013 | V2 | 85% | Schemathesis per-PR; adopt as addition |
| U-014 | V2 | 70% | React 18 + TanStack specifics; adopt |
| U-015 | V2 | 80% | Keep-old-email-valid; adopt with INV-001 resolution |
| U-016 | V2 | 75% | Redis Sentinel for dev/test; adopt |
| U-017 | V2 | 85% | `/api/v1/`; adopt |
| U-018 | V2 | 85% | EXPLAIN ANALYZE CI; adopt |
| U-019 | V2 | 80% | Pagination defaults; adopt |
| U-020 | V2 | 85% | Admin <500ms@50K gate; adopt |
| A-001 | Resolved | 90% | Both ACCEPT |
| A-002 | Resolved | 80% | Both ACCEPT with note/QUALIFY |
| A-003 | Resolved | 75% | V2 ACCEPT, V1 QUALIFY → surface in exec summary |
| A-005 | V1 | 70% | V1 REJECT (2FA-on-reset gap); V2 QUALIFY → adopt V1 |
| A-007 | Resolved | 80% | Both QUALIFY |
| A-009 | V1 | 75% | V1 REJECT (spec-refresh checkpoints); V2 QUALIFY → adopt V1 |
| A-010 | V1 | 95% | V2 explicitly resolved in V1's favor |

**Per-point summary**:

- V1 wins: 28 points (S-003, C-001, C-003, C-004, C-005, C-006, C-007, C-008, C-009, C-011, C-012, C-013, C-015, C-016, X-001, X-002, X-003, X-004, U-001-U-011, A-005, A-009, A-010 — corrected count)
- V2 wins: 11 points (S-001, S-004, C-002, C-010, C-017, C-018, C-019, C-020, U-012-U-020 grouped)
- Merged/Tie: 5 points (S-002, S-005, C-014, A-001, A-002, A-003, A-007 grouped as agreed)
- Total: 56 diff points

**Confidence calibration check**: No 100% confidences (rule respected). No <50% confidences. Range 60-95%. Average confidence ~82%.

---

## Convergence Assessment

- **Points with agreed winner or merged-best outcome**: 56 of 56
- **Alignment**: 100%
- **Threshold**: 80%
- **Diff-point convergence status**: **CONVERGED** (V2 advocate explicitly conceded base selection in R2)
- **Taxonomy coverage**: L1 ✓ (S-004, C-018, C-020), L2 ✓ (S-001, S-002, C-002, C-009, C-016), L3 ✓ (C-013, C-001, C-004, C-012, A-007) — all 3 levels covered
- **Invariant probe gate**: **BLOCKED BY INVARIANTS** — 6 HIGH UNADDRESSED items
- **Final status**: **BLOCKED_BY_INVARIANTS**

The diff-point debate fully converged with V1 as the agreed base. However, the invariant probe surfaced 6 HIGH-severity UNADDRESSED items that must be ADDRESSED in the refactor plan before the merged output can claim status=success. These items become mandatory items in the refactor plan; if any are deferred, they must be documented in the merged output's "Known Limitations" section with explicit accept-the-risk rationale.

Unresolved points: 0 from diff-point debate. 6 from invariant probe (INV-001, INV-003, INV-010, INV-011, INV-013, INV-015).
