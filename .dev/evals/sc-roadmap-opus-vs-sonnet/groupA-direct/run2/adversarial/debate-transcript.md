# Adversarial Debate Transcript

## Metadata

- Depth: standard (Round 1 parallel + Round 2 sequential + Round 2.5 invariant probe; Round 3 skipped)
- Rounds completed: 2 + invariant probe
- Convergence achieved: 0.78 (43 agreed / 55 substantive debate points, with 9 HIGH invariant items blocking declared convergence)
- Convergence threshold: 0.80
- Focus areas: All (no `--focus` filter applied)
- Advocate count: 2 (opus / sonnet)
- Source spec: `tests/sc-roadmap/fixtures/sample_spec.md`
- Generated: 2026-05-22T17:58Z

---

## Round 1: Advocate Statements (Parallel)

Both advocates dispatched in parallel via Task tool. Both received identical inputs: own variant, opposing variant, diff-analysis.md. Both addressed all 15 A-NNN shared assumptions with ACCEPT/REJECT/QUALIFY verdicts. No omissions detected.

### Variant 1 Advocate (opus / default)

**Position Summary**: V1 is the stronger merge base because security primitives land before exposed surfaces (NIST SP 800-63B §5.1.1.2, OWASP ASVS V2.1), M7's terminal NFR gates are release-blocking, K8s+Patroni reliability story is the only topology that can satisfy NFR-005 99.9%, the GDPR DPIA artifact is named and DPO-signed, the per-request Redis pub/sub denylist provides bounded ≤60s access-token revocation latency, and the "every route has `requiredPermission`" CI check prevents authorization-by-default-allow drift.

**Top 10 Strengths Claimed** (all evidence-cited):

1. Security primitives precede exposed surfaces (S-002, S-003)
2. NFR gating is discrete release-blocking phase (S-010, S-012)
3. GDPR DPIA + DPO sign-off named (C-023, X-014, U-005)
4. K8s + Patroni + chaos test for NFR-005 (X-009, U-004)
5. ≤60s access-token revocation via Redis denylist (X-013, U-008)
6. CI fails build if any route lacks `requiredPermission` (U-003)
7. Adversarial rate-limit-bypass + token-theft suite (U-007)
8. Hourly hash-chain audit-verify cron vs 720× longer monthly merkle (X-006)
9. pgcrypto + KMS DEK vs env-var key (X-005)
10. Dedicated cookie hardening with `__Host-` prefix + strict CSP (U-001)

**Steelman of V2** (top 7 things V2 genuinely gets right):

- Critical-path callout (U-013)
- FR Coverage Matrix (U-025)
- DB GRANT enforcement for audit (U-030)
- Email-change re-verification (U-020)
- Consent tracking table (U-022)
- erased_uuid anonymization pattern (U-023)
- Duration estimates + parallel branch identification (U-012)

**Concessions** (V1 weaknesses honestly acknowledged):

- Silent on FR-010 email-change re-verification (C-024)
- No duration estimates or critical path (S-015, U-013)
- No FR Coverage Matrix table (S-017)
- No Technology & Version Pinning table (S-018)
- No avatar upload spec, disposable-email rejection, unverified pruning

**Shared Assumption Responses**: A-001 ACCEPT, A-002 QUALIFY, A-003 ACCEPT, A-004 ACCEPT, A-005 ACCEPT, A-006 QUALIFY, A-007 QUALIFY, A-008 ACCEPT, A-009 ACCEPT, A-010 QUALIFY, A-011 QUALIFY, A-012 QUALIFY, A-013 QUALIFY, A-014 ACCEPT, A-015 QUALIFY. 15/15 addressed.

### Variant 2 Advocate (sonnet / default)

**Position Summary**: V2 is the stronger merge base because it ships working auth in M1 (early integration testability), provides actionable PM scaffolding (durations, critical path, FR matrix), consolidates GDPR work in M5, and addresses FRs V1 silently omits (email-change re-verification, consent tracking, avatar upload).

**Top 10 Strengths Claimed**:

1. M1 ships working register/login/sessions (S-002, S-003)
2. Duration estimates and critical-path analysis (U-012, U-013)
3. FR Coverage Matrix (U-025)
4. PG-backed token-family sessions avoid hard Redis dependency (C-004)
5. DB GRANT INSERT-only for audit integrity (U-030)
6. Email-change re-verification (U-020, C-024)
7. user_consents table with version-tracked policy (U-022)
8. `erased_<uuid>@erased.local` audit-retention-compatible anonymization (U-023)
9. Burst-detection auto-block 1000+/min IP (U-024)
10. `/health/oauth` provider reachability endpoint (U-018)

**Steelman of V1** (top 7 things V1 genuinely gets right):

- Per-request token-revocation ≤60s bound (U-008)
- DPIA + DPO sign-off (U-005, X-014)
- 5-role RBAC taxonomy + CI-enforced `requiredPermission` (U-002, U-003)
- K8s + Patroni + chaos test (U-004)
- DB-layer pgcrypto + KMS-managed DEK (X-005)
- Adversarial test suite as named deliverable (U-007)
- Dedicated cookie hardening deliverable (U-001)

**Concessions** (V2 weaknesses honestly acknowledged):

- Docker Compose cannot achieve 99.9% uptime (X-009) — should adopt V1 HA
- No DPIA or DPO sign-off (X-014) — must be patched
- No per-request token-revocation denylist (X-013)
- App-layer env-var encryption weaker than DB-layer (X-005)
- Three-role RBAC coarser than five-role (X-008)

**Shared Assumption Responses**: A-001 ACCEPT, A-002 QUALIFY, A-003 ACCEPT, A-004 ACCEPT, A-005 ACCEPT, A-006 ACCEPT, A-007 QUALIFY, A-008 ACCEPT, A-009 ACCEPT, A-010 QUALIFY, A-011 QUALIFY, A-012 ACCEPT, A-013 ACCEPT, A-014 ACCEPT, A-015 QUALIFY. 15/15 addressed.

---

## Round 2: Sequential Rebuttals

V1 advocate rebutted first (input order), then V2 advocate (with visibility into V1's Round 2 rebuttal).

### V1 Advocate Rebuttal — Key Outcomes

**Concessions accepted point-by-point** to V2's 7 critiques:

1. **Duration estimates / critical path** — full concession; framed as PM scaffolding that bolts onto V1's structure without inverting ordering.
2. **M1 ships zero user-facing value** — REJECTED as a category error; cited NIST SP 800-63B §5.1.1.2, OWASP ASVS V2.1, CIS Controls v8 §6, and Verizon 2024 DBIR §AppSec ("68% of breached credential-store deployments had foundations bolted on post-launch").
3. **GDPR scattered M6+M7** — partial concession; counter-argued that GDPR has TWO dependency profiles (artifacts in M7, enforcement coupled to substrate in M3/M4); merge keeps M3/M4 enforcement gates + adds cross-cutting compliance-artifact register.
4. **OWASP at M7 not M5** — partial concession; framed as terminal release gate not testing-done-late; merge adopts BOTH shift-left (V2) AND terminal gate (V1).
5. **No FR coverage matrix** — full concession; merge adopts V2's matrix verbatim.
6. **Missing email-change re-verification** — full concession; merge adopts V2's pattern verbatim.
7. **Missing consent tracking** — concede the gap; merge places consent_table in M4 alongside audit substrate.

**Upgraded V2 strengths after Round 1+2**:

- FR Coverage Matrix: medium → high
- Email-change re-verification: low → medium-high
- Burst-detection auto-block: low → medium
- DB GRANT enforcement: medium → medium-high

**Downgraded V2 strengths after Round 1+2**:

- "M1 ships working auth": high → low (NIST/OWASP/CIS ordering)
- PG-token-family sessions "avoids hard Redis dependency": medium → low (V2 conceded no per-request denylist; PG sessions can't deliver ≤60s revocation)
- `/health/oauth` "proactive vs reactive": medium → low (probe vs probe-consumer is same control, different layer)
- erased_uuid pattern: medium → low-medium (only works if audit log doesn't store IP/user-agent/device, which it does)

**V1 advocate reaffirmed top-3 priorities**:

1. Security-primitive ordering (M1 = foundation, not M1 = auth surface) — load-bearing
2. M7 NFR terminal gate as release-blocking — shift-left is complement, not substitute
3. Bounded token-revocation latency via Redis denylist (V1 ≤60s) — V2's PG architecture cannot match without re-architecting

### V2 Advocate Rebuttal — Key Outcomes

**Concessions accepted point-by-point** to V1's 9 critiques + Round 2 rejoinders:

1. **M1 ships exposed auth before encryption baseline** — partial concession; merge handling: adopt V1's M1 scope, shift V2's auth endpoints to M2; plaintext-email window collapses to zero.
2. **Docker Compose can't deliver 99.9%** — FULL concession; merge adopts V1's D7.4 K8s + Patroni + chaos test verbatim.
3. **No DPIA artifact** — FULL concession; merge adopts V1's D7.3 compliance gate; V2's consent table feeds INTO that gate.
4. **Unbounded access-token revocation latency** — partial concession; merge adopts V1's Redis denylist; V1 overstates severity but property is real.
5. **App-layer env-var encryption** — FULL concession; merge adopts V1's pgcrypto + KMS DEK approach.
6. **OWASP gate inside M5 not GA** — partial concession; both needed — shift-left at M5 AND terminal at M7.
7. **Permission cache TTL 5 min fan-out cost** — pushed back; V1's 10-min TTL is staleness-worse but fan-out cost is bounded; merge adopts V1's 10-min TTL but keeps V2's invalidation mechanism.
8. **No defence-in-depth between lockout and rate-limit** — REJECTED as factually wrong; V2 has both controls; merge adds V1's explicit "lockout in addition to rate-limit" prose.
9. **3-role RBAC too coarse** — partial concession; merge adopts V1's 5-role default + V2's `POST /admin/roles` custom-role endpoint.

**Pushed back on V1's Round 2 framing**:

- NIST/OWASP/CIS appeal-to-authority overstates what standards actually mandate (both variants have encryption before GA; disagreement is *which milestone*, not whether-at-all).
- "PG sessions can't deliver ≤60s revocation" is conflated: V2's token-family is theft detection, V1's denylist is invalidation cache; not mutually exclusive.
- Verizon DBIR statistic describes orgs that shipped WITHOUT encryption — neither variant does that.

**V2 advocate reaffirmed top-3 priorities**:

1. Merge milestone topology: adopt V1's M1 scope (foundation + encryption), shift V2's auth endpoints to M2.
2. Hybrid session revocation: V1's Redis denylist + V2's token-family detection as complementary mechanisms; both retained.
3. Compliance + reliability: V1's D7.3 DPIA + D7.4 K8s/Patroni adopted; V2's consent-table + erasure-anonymization + INSERT-only GRANT retained as enforcement substrate.

---

## Round 2.5: Invariant Probe (Fault-Finder)

Per AD-1 protocol, fault-finder agent probed the emerging consensus against the 6-category checklist. See `invariant-probe.md` for full results.

**Findings summary**:

- Total findings: 24
- ADDRESSED: 0
- UNADDRESSED: 24 (HIGH: 9, MEDIUM: 9, LOW: 6)

**HIGH-severity UNADDRESSED items (blocking)**:

- INV-001: Redis pub/sub denylist semantics under Sentinel failover
- INV-002: Encrypted-column inventory doesn't enumerate V2-added tables
- INV-005: No guard binding V2-added PII-bearing tables to D1.2 encryption
- INV-009: ≤60s revocation arithmetic unverified (pub/sub delay + cache TTL + clock skew not enumerated)
- INV-010: 13-week duration claim doesn't survive V1-ordering merge
- INV-021: pgcrypto on `email` breaks email-lookup queries → NFR-001 violation
- INV-022: ≤60s revocation sufficiency depends on unstated local-cache TTL
- INV-023: pgcrypto key residency claim is technically false (DEK transits app memory + pg wire)
- INV-024: Plaintext-PII window enumeration lacks negative test guarantee

**Gate outcome**: CONVERGENCE BLOCKED on 9 HIGH + UNADDRESSED items. These MUST be patched in the refactor plan before the merge can declare success.

---

## Scoring Matrix (Per-Diff-Point)

Confidence calibration: never 100% unless unanimous concession; never <50%; concession boost +10%.

### High-Severity Contradictions (X-NNN)

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|------------------|
| X-001 (session storage) | V1 + V2 hybrid | 75% | Both advocates converge: V1's Redis denylist for ≤60s revocation + V2's PG-backed token-family as durable evidence layer. Not "V1 wins" — both retained. |
| X-005 (PII encryption layer) | V1 | 92% | V2 advocate full concession in Round 2; pgcrypto + KMS DEK strictly stronger than env-var. Note: INV-023 found V1's "key out of memory" claim partially false; merge must patch via per-request KMS unwrap. |
| X-009 (HA topology) | V1 | 98% | V2 advocate full concession; Docker Compose mathematically cannot meet 99.9%; merge adopts K8s + Patroni + chaos test. |
| X-013 (access-token revocation latency) | V1 | 88% | V2 advocate partial concession; V1's ≤60s denylist is a real security property V2 lacks. Note: INV-009 + INV-022 require explicit budget breakdown before claim holds. |
| X-014 (DPIA artifact) | V1 | 95% | V2 advocate full concession; GDPR Article 35 mandates DPIA; V2 omitted it. |

### Other Contradictions

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|------------------|
| X-002 (lockout duration) | V1 | 60% | V1 15-min vs V2 30-min — V1 less user-disruptive on accidental lockouts; not strongly debated. |
| X-003 (OAuth timeout) | Mixed | 55% | V1 3s aggressive, V2 10s/30s permissive; merge sets ≤3s for primary timeout (V1) + ≤30s total budget (V2). |
| X-004 (login rate limit) | V1 | 65% | V1 10/min stricter against brute force; V2 20/min permissive. Merge adopts 10/min for `/auth/login`. |
| X-006 (audit tamper scheme) | V1 | 70% | V1's hourly cron hash-chain has 720× better detection latency than V2's monthly merkle. Note: INV-004 + INV-019 require single-writer queue patch. |
| X-007 (cookie SameSite) | V1 | 65% | V1 SameSite=Lax + __Host- prefix more compatible with cross-origin login flow than V2 Strict. Note: INV-007 requires admin-subdomain guard. |
| X-008 (RBAC role taxonomy) | V1 | 75% | V1 5 roles + V2's custom-role endpoint = merge gets both. |
| X-010 (perm cache TTL) | V1 | 60% | V1 10-min + V2 fan-out invalidation = merge gets both. |
| X-011 (2FA recovery code format) | V1 | 65% | V1 128-bit argon2id-hashed more cryptographically defensible; V2's 8-char SHA-256 weaker. |
| X-012 (CSP style-src) | V1 | 78% | V1's strict CSP (no unsafe-inline) better protects against R-001 XSS. |

### High-Value Unique Contributions Adopted

| Diff Point | Winner | Confidence | Action |
|------------|--------|------------|--------|
| U-001 (Cookie hardening deliverable) | V1 | 88% | Retain V1 D3.3 |
| U-003 (requiredPermission CI check) | V1 | 95% | Retain V1 D4.1 |
| U-004 (K8s + Patroni + chaos) | V1 | 98% | Retain V1 D7.4 (replaces V2 D7.3) |
| U-005 (DPIA + DPO sign-off) | V1 | 95% | Retain V1 D7.3 |
| U-007 (adversarial test suite) | V1 | 90% | Retain V1 D7.2 |
| U-008 (Redis denylist ≤60s) | V1 | 88% | Retain V1 D3.2 (with INV patches) |
| U-013 (critical-path callout) | V2 | 80% | ADD to merge top-of-document table (adjusted for V1 ordering) |
| U-020 (email-change re-verification) | V2 | 92% | ADD to V1 D6.1 |
| U-022 (consent table) | V2 | 88% | ADD to merge as M4 deliverable alongside audit |
| U-023 (erased_uuid anonymization) | V2 | 85% | ADD to V1 D6.3 (improves audit integrity preservation) |
| U-024 (burst-detection auto-block) | V2 | 80% | ADD to V1 D5.2 |
| U-025 (FR Coverage Matrix) | V2 | 92% | ADD as new end-of-document table |
| U-026 (Tech version pinning table) | V2 | 75% | ADD as new end-of-document table |
| U-030 (DB GRANT INSERT-only) | V2 | 88% | ADD to V1 D5.3 alongside hash chain |

### Shared Assumption Convergence (A-NNN)

15/15 A-NNN points addressed by both advocates. Convergence on assumption verdicts:

| A-NNN | V1 Verdict | V2 Verdict | Final Resolution |
|-------|------------|------------|------------------|
| A-001 RS256 | ACCEPT | ACCEPT | ACCEPT |
| A-002 Argon2id @ m=64MiB fits 200ms | QUALIFY | QUALIFY | QUALIFY — add cold-start carve-out (per INV-011 / NFR-001 risk) |
| A-003 15-min access, 30-day refresh | ACCEPT | ACCEPT | ACCEPT |
| A-004 256-bit one-time tokens | ACCEPT | ACCEPT | ACCEPT |
| A-005 PKCE S256 mandatory | ACCEPT | ACCEPT | ACCEPT |
| A-006 Node + Fastify stack | QUALIFY | ACCEPT | ACCEPT (FastAPI alternative documented but Fastify selected) |
| A-007 SendGrid sole email provider | QUALIFY | QUALIFY | QUALIFY — flag as known SPOF; secondary provider out of scope but documented |
| A-008 RBAC1 role-permission | ACCEPT | ACCEPT | ACCEPT |
| A-009 Refresh-token reuse → family revoke | ACCEPT | ACCEPT | ACCEPT |
| A-010 10K sessions on single cluster | QUALIFY | QUALIFY | QUALIFY — multi-region marked as future scaling boundary |
| A-011 NFR-001 measured at steady state | QUALIFY | QUALIFY | QUALIFY — add cold-worker carve-out clause to D7.1 |
| A-012 Column-level encryption (not TDE) | QUALIFY | ACCEPT | QUALIFY — INV-021 mandates email_lookup_hash sidecar for query path |
| A-013 Audit retention vs erasure tension | QUALIFY | ACCEPT | QUALIFY — set retention period at 7 years with exception register |
| A-014 PagerDuty + on-call available | ACCEPT | ACCEPT | ACCEPT |
| A-015 OAuth `email_verified` sufficient | QUALIFY | QUALIFY | QUALIFY — require explicit "claim this account" re-auth before merge if local account exists |

---

## Convergence Assessment

- **Diff points debated**: 76 total (S=22, C=25, X=14, U=30, A=15)
- **Diff points resolved (agreed winner)**: 43
- **Diff points partial-resolution (both retained as complementary)**: 10
- **Diff points unresolved (single-direction win without consensus)**: 2 (rate-limit threshold X-004 — V1 stricter; OAuth timeout X-003 — merged budget)
- **Computed convergence**: 43 / 55 substantive points = **0.78** (below 0.80 threshold)
- **Threshold**: 0.80
- **Status (raw)**: NOT_CONVERGED on agreement count
- **Invariant gate**: BLOCKED on 9 HIGH UNADDRESSED items
- **Final status**: **BLOCKED_BY_INVARIANTS** — merge proceeds only after refactor-plan addresses INV-001, INV-002, INV-005, INV-009, INV-010, INV-021, INV-022, INV-023, INV-024.

Round 3 skipped (depth = standard; not deep). Force-select by score; merge plan must include invariant patches. Documented per FR-006 error handling (`no_convergence` path).

---

## Unresolved Points

| Point ID | Why unresolved | Action |
|----------|----------------|--------|
| X-004 (rate limit threshold) | V1=10/min, V2=20/min; convergence on "stricter is better" but no quantitative justification cited. | Merge adopts V1 10/min for `/auth/login`; documented as overridable per deployment. |
| X-003 (OAuth timeout) | V1=3s, V2=10s/30s; both have rationale; consensus on dual budget. | Merge adopts ≤3s primary timeout (V1) within a ≤30s total budget (V2). |
| INV-001..INV-024 (24 invariant findings) | All UNADDRESSED at end of Round 2.5. | Refactor plan must patch all 9 HIGH items; MEDIUM/LOW noted as known limits or planned follow-ups. |
