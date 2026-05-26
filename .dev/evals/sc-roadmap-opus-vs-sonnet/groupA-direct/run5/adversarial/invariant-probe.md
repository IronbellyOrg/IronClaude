# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

Independent fault-finder probe of the emerging consensus (V1 as base, V2 contributions adopted). Findings classify hidden assumptions across 6 categories.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | Pending-email state representation: consensus adopts V2 "old email remains active until new email verified" + V1 single `email` column schema — schema cannot hold both old (active for login) and new (pending) values | UNADDRESSED | HIGH | V1 D5.1 (line 180) `/me/email/change` "re-verification required"; V2 D3.6 (line 109) "old email remains active"; V1 D1.1 (line 33) schema has unique `email` only; account-takeover risk if reset keys pending email |
| INV-002 | state_variables | Lockout-counter survival across Redis Sentinel failover: V1 `users.locked_until` mirror writes "on lockout" but failed-login counter (4 of 5) lives only in Redis; Sentinel failover loses in-flight counter unless AOF fsync=always | UNADDRESSED | MEDIUM | V1 D4.5 (line 146) "mirrored to `users.locked_until` on lockout to survive Redis loss"; V1 D1.2 (line 34) "AOF persistence enabled" without fsync mode |
| INV-003 | guard_conditions | Admin promotion bypasses mandatory-2FA invariant: V1 "2FA mandatory for admin role (enforced at login)" but role-promotion-while-logged-in path has no enrollment-gate; freshly-promoted admin without 2FA either bypasses the invariant or locks themselves out | UNADDRESSED | HIGH | V1 D4.2 (line 143) "mandatory for admin role (enforced at login)"; V2 D3.3 (line 106) "Role change invalidates user's active JWT" — next login by un-2FA-enrolled admin is undefined |
| INV-004 | guard_conditions | HIBP breached-password denylist scope: V1 U-006 places check on registration only; password-reset and password-change paths inherit "strength rules" without re-applying the breach denylist | UNADDRESSED | MEDIUM | V1 D2.1 (line 70) HIBP on register; V1 D5.1 (line 180) `/me/password/change` "current-password required" no HIBP; V2 D1.6 (line 39) reset "validates strength rules" no breach check |
| INV-005 | count_divergence | Progressive-lockout cycle counter window: V1 "5 fails → 15min lock; 3 cycles → require reset" lacks decay window; could mean lifetime (permanent degradation) or per-Redis-TTL (3 cycles unreachable) | UNADDRESSED | MEDIUM | V1 D4.5 (line 146) trigger specified, decay window omitted; off-by-one risk on "3rd cycle" trigger boundary |
| INV-006 | count_divergence | Page-size 200 × per-user RBAC cache: V2 admin pagination "default 50, max 200" (adopted) × V1 per-user permission cache 60s TTL — eager permission resolution per row stresses cache | UNADDRESSED | LOW | V1 D3.5 (line 108) per-user cache; V2 D4.1 (line 139) page-size 50/200; <500ms@50K gate (U-020) doesn't specify whether permission joins are in the EXPLAIN ANALYZE path |
| INV-007 | collection_boundaries | Empty audit-log response shape divergence: V2 D3.5 returns `{results: [], total: 0}`; V1 doesn't specify; Schemathesis contract gate (U-013 adopted) will flag if responses diverge between user and admin audit endpoints | UNADDRESSED | LOW | V2 D3.5 (line 108) explicit; V1 D5.2 (line 181) admin-side undefined |
| INV-008 | collection_boundaries | Refresh-token "family" semantics ambiguous: family = single login event (per-device, multiple per user) vs. family = single rotation chain (one per user). "Force logout (revoke all families)" semantics depend on this | UNADDRESSED | MEDIUM | V1 D2.4 (line 72) `family_id`; V1 D5.2 (line 181) "revoke all refresh-token families"; shared assumption A-007 (session-scoped, not device-scoped) does not resolve |
| INV-009 | interaction_effects | API versioning + nightly OIDC discovery tests + Schemathesis per-PR: deprecation policy (parallel-version window, sunset header) for `/api/v1/` → `/api/v2/` migration not specified; Schemathesis only validates current major | UNADDRESSED | MEDIUM | V2 C-018 adopts versioning; V1 D3.8 OIDC tests are external; V2 U-013 Schemathesis is own-spec only; no `/api/v2/` rollout rule exists |
| INV-010 | interaction_effects | pgcrypto AES-256-GCM column encryption + unique btree on `users.email` are mutually exclusive without a blind-index (HMAC-SHA256) column; consensus has neither blind-index nor confirms deterministic encryption mode | UNADDRESSED | HIGH | V1 D1.1 (line 33) PII columns AES-256-GCM; V2 D5.2 (line 173) "Indexes on `users.email` (unique btree)"; full-table decrypt-scan on every login violates NFR-001 |
| INV-011 | interaction_effects | S3 object-lock 7yr (V1 U-004) vs. GDPR Art. 17 erasure 30-day flow: object-lock is immutable by design; redaction path for already-archived audit `metadata_jsonb` containing PII is not specified | UNADDRESSED | HIGH | V1 D4.7 (line 148) "S3 with object-lock for 7-year retention"; V1 D4.8 (line 149) erasure "retains audit rows by user-id reference"; PII in `metadata_jsonb` not redacted pre-archive; GDPR Art. 17(3) exception ground not documented |
| INV-012 | interaction_effects | "Sole admin / first admin" break-glass: mandatory 2FA for admin + 10 single-use recovery codes + admin force-disable-2FA admin dashboard → if sole admin loses TOTP device and exhausts recovery codes, no out-of-band recovery path exists | UNADDRESSED | MEDIUM | V1 D4.1 (line 142) "10 single-use codes"; V1 D5.2 (line 181) admin force-disable but requires admin (chicken-and-egg); D5.9 GA gate omits break-glass procedure |
| INV-013 | sufficiency_challenge | NFR-001 (<200ms p95) gates measure latency WITHOUT pgcrypto decryption tax (INV-010), WITHOUT cold-cache RBAC penalty, and WITHOUT cold-process Argon2id m=64MB (~200ms+ per hash on small instances) | UNADDRESSED | HIGH | V1 M2 acceptance (line 83) p95 ≤ 200ms @ 100 RPS; V2 D5.1 10K @ 5min; V1 D3.5 RBAC "cached for 60s" — no warm-on-deploy; downstream gate enumeration: (a) admin endpoints at 50K, (b) Redis-miss permission lookup, (c) cold Argon2id; the consensus claim "NFR-001 met" is necessity-only, not sufficient |
| INV-014 | sufficiency_challenge | NFR-003 (OWASP) sufficiency: append-only PG audit log protects against in-app tampering but NOT against DBA / retention-role tampering; ASVS 4.0 §V10 implies tamper-evidence (HMAC chain / Merkle); pen-test scope (D5.7) may not catch this | UNADDRESSED | MEDIUM | V1 D4.6 (line 147) append-only trigger; V1 D5.7 pen-test scope undefined; ASVS 4.0 §10.5 expects signed log entries |
| INV-015 | sufficiency_challenge | NFR-005 (99.9%) sufficiency: HPA+PDB + burn-rate alerts proven NECESSARY; SLO scope (which endpoints count, which deps excluded) UNDEFINED; serial-dependency availability product (SendGrid × Google × GitHub × own) unbounded; SendGrid down = registration/reset down — counts toward SLO unless documented exclusion | UNADDRESSED | HIGH | V1 D5.4 (line 183) HPA+PDB; V1 D5.5 (line 184) burn-rate alerts; V1 D5.6 (line 185) 30-min k6 — but SLO endpoint scope not in D5.5; OAuth fallback exists (D3.7) but SendGrid has no fallback (shared assumption A-006); downstream gates between "HPA configured" and "99.9% measured" not enumerated |
| INV-016 | sufficiency_challenge | R-001 (XSS) sufficiency: HttpOnly cookies + CSP claimed mitigation; V1 D2.9 CSP omits `script-src` (allows inline by default); V2 D2.7 has `script-src 'self'` but also `'unsafe-inline'` for styles → CSS exfil attack surface; React 18 admin SPA requires nonce-based CSP not specified | UNADDRESSED | MEDIUM | V1 D2.9 (line 77) `default-src 'self'; frame-ancestors 'none'; object-src 'none'` — no script-src; V2 D2.7 (line 73) `script-src 'self'; style-src 'self' 'unsafe-inline'`; V2 D4.5 React 18 SPA without nonce-CSP guidance |

## Summary

- **Total findings**: 16
- **ADDRESSED**: 0
- **UNADDRESSED**: 16
  - **HIGH**: 6 (INV-001, INV-003, INV-010, INV-011, INV-013, INV-015)
  - **MEDIUM**: 8 (INV-002, INV-004, INV-005, INV-008, INV-009, INV-012, INV-014, INV-016)
  - **LOW**: 2 (INV-006, INV-007)

## Convergence Gate Status

**BLOCKED BY INVARIANTS**: 6 HIGH-severity UNADDRESSED invariant(s) detected
Blocking items: INV-001, INV-003, INV-010, INV-011, INV-013, INV-015

These items must be ADDRESSED in:

1. The refactor plan as MANDATORY merge changes (preferred), OR
2. Documented in the merged output as `## Known Limitations / Deferred Work` with explicit accept-the-risk rationale.

The pipeline proceeds with `status: partial` and `unaddressed_invariants` populated in the return contract, recording the 6 HIGH items.

## Category Coverage

- **state_variables**: 2 findings (1 HIGH, 1 MEDIUM)
- **guard_conditions**: 2 findings (1 HIGH, 1 MEDIUM)
- **count_divergence**: 2 findings (0 HIGH, 1 MEDIUM, 1 LOW)
- **collection_boundaries**: 2 findings (0 HIGH, 1 MEDIUM, 1 LOW)
- **interaction_effects**: 4 findings (2 HIGH, 2 MEDIUM)
- **sufficiency_challenge**: 4 findings (3 HIGH, 1 MEDIUM)

All 6 categories produced ≥1 finding; sufficiency_challenge produced the highest concentration of HIGH items (3 of 4), confirming that the consensus had multiple "necessity-not-sufficiency" claims around NFR-001 / NFR-003 / NFR-005.
