# Round 2.5 — Invariant Probe (Independent Fault-Finder)

**Role**: Independent fault-finder. NOT an advocate. Probing emerging consensus for state-mechanics violations, boundary errors, hidden assumptions.

**Source consensus** (synthesized from R1/R2 advocate transcripts):

- Hash-chain audit log (V1 origin, V2 conceded)
- Per-user concurrent session cap default=5, oldest-eviction (V2 origin, V1 conceded)
- GDPR `user_id` tokenization in audit table + crypto-shred PII (V1 origin, V2 conceded)
- Redis WATCH/MULTI/EXEC for refresh-token atomicity + family-tracking as defense-in-depth (joint adoption)
- HTTP-only + Secure + SameSite=Strict cookie for refresh token (both variants)
- pgcrypto column-level email encryption (V2 origin, V1 conceded)
- K8s + HPA + PgBouncer + Redis Sentinel (V2 origin, V1 conceded — conditional on ADR)
- JWKS + `kid` for RS256 rotation (V1 origin, V2 conceded)
- Explicit user confirmation for OAuth account linking (V2 conceded NE-3)
- IP-based rate-limit key for pre-auth endpoints (V2 conceded NE-4)
- zxcvbn + HIBP k-anonymity password policy (V2 conceded)
- Per-milestone edge-case blocks + centralized D7.1 regression suite (V2 conceded)
- Bootstrap admin script (V2 conceded)
- A-003 (synchronous audit write amplification at p99): both variants conceded the joint gap
- A-007 (token-binding race order): both variants conceded the joint gap

---

## Findings

```
ID: INV-001
CATEGORY: sufficiency_challenge
ASSUMPTION: Consensus claim that hash-chain audit (D6.5) + S3 object-lock provides tamper-evidence sufficient to defeat privileged-insider tampering and satisfy R-009.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: V1 D6.5 specifies "each row contains SHA-256 of prior row's canonicalized payload" but neither variant nor any rebuttal specifies: (a) where the GENESIS hash (first row's prev_hash) is anchored — if it's NULL or zero, an attacker can re-forge the chain from row 1 by computing fresh hashes top-to-bottom; (b) whether the canonicalization function is deterministic across JSONB key ordering — Postgres JSONB does not preserve insertion order, so `json.dumps(sorted_keys)` is required but unspecified; (c) where the latest-row "tip" hash is published externally — without an external commitment (e.g., notarized to S3 daily WITH the tip hash, or to a third-party timestamp service), a DBA who deletes rows N..M and re-chains rows M+1..end with adjusted prev_hash values produces a valid-looking chain. The S3 daily export with object-lock partially addresses this but only AT 24-HOUR GRANULARITY — a tampering event between exports is undetectable. Downstream falsifier: partial-row JSONB corruption (e.g., `metadata` field modified, prev_hash recomputed) defeats SHA-256 chain unless the canonicalization includes the entire row payload AND the chain is verified against the most recent export tip.
```

```
ID: INV-002
CATEGORY: interaction_effects
ASSUMPTION: The consensus combination of (a) HTTP-only + Secure + SameSite=Strict refresh cookie (D2.5/D1.6) and (b) explicit OAuth account-linking confirmation via email (NE-3 fix) interacts safely.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: SameSite=Strict cookies are NOT sent on cross-site top-level navigations (including OAuth callback returns from accounts.google.com / github.com). Per shared assumption A-001, the variants assume "browser is the primary client" with the API and frontend on the same registrable domain. But the OAuth callback (V1 D4.1 `/auth/oauth/google/callback`, V2 D3.1) is a top-level redirect from a 3rd-party origin; if the user is mid-flow and the refresh cookie has SameSite=Strict, the callback handler CANNOT read the refresh cookie to identify an existing logged-in session. This means the "explicit confirmation" flow (NE-3) cannot use the existing session — it must rely on a separate confirmation email or a SameSite=Lax cookie carve-out for OAuth callbacks. Neither variant nor rebuttal addresses this interaction. Downstream falsifier: a user who is logged in via password, then clicks "link Google account" while logged in, will appear unauthenticated on the callback handler under SameSite=Strict — the system either rejects the link (UX bug) or silently treats it as a NEW account creation (security regression that the NE-3 fix was supposed to close).
```

```
ID: INV-003
CATEGORY: collection_boundaries
ASSUMPTION: Per-user concurrent session cap of 5 with oldest-eviction (V2 D2.5, joint consensus) behaves correctly at the boundary N=0 (first login) and N=5+1 (eviction trigger).
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: V2 D2.5 says "Oldest session evicted when limit exceeded." Boundary issues neither variant addresses: (a) at N=5 exactly, is the 5th session permitted (≤5) or rejected (<5)? V2 says "default: 5" and "oldest session evicted when limit exceeded" — but "exceeded" is ambiguous between strict-greater-than (so 5 sessions are kept, 6th evicts oldest) and greater-or-equal. (b) For a concurrent burst of 5 simultaneous logins from different devices in a TLS handshake window, race conditions in the eviction logic can leave 6+ sessions (read-count-then-insert race even with WATCH/MULTI/EXEC on the refresh token row, because the session-list cardinality is a separate read). (c) Empty-session-list edge case: at N=0, the eviction code path must not be invoked — V1 advocate brief item 8 references "bootstrap admin path (D2.7)" but the cap-evict logic on first-ever login is not specified. Downstream falsifier: credential-stuffing attacker exploits the race window between concurrent logins to seed >5 sessions before any eviction commits.
```

```
ID: INV-004
CATEGORY: count_divergence
ASSUMPTION: Brute-force lockout threshold "5 consecutive failed attempts within 15 minutes" (V2 D4.5) vs V1's "10 failed attempts → 30-min lockout, exponential backoff" (V1 D3.4) and the rate-limit threshold "5 login attempts / 15 min per (IP, email)" (V1 D3.3) consistently bound the same threat.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: Three different counters in the consensus debate. V1 D3.3 says rate-limit at 5 attempts/15min per (IP,email) — the RATE-LIMIT trip would return 429. V1 D3.4 says lockout at 10 attempts → 30-min — this would never fire because the rate-limit at 5 already blocks the 6th-10th attempts. V2 D4.5 says lockout at 5 failures → 30min — collides exactly with V1's rate-limit threshold. No consensus resolution exists for: (a) does a 429 rate-limit response count toward the lockout failure counter? If yes, the rate-limit becomes a DoS amplifier (attacker triggers victim's lockout by exhausting their rate-limit). If no, the lockout never fires under V1's combined config because rate-limit pre-empts. (b) Sliding-window vs fixed-window semantics differ: V1 uses "sliding window" (D3.3) but V2 uses unspecified — at the 15-min boundary, a sliding window resets attempt-by-attempt while fixed resets cliff-edge. (c) Counter location: V2 D4.5 stores lockout counter in Redis "with TTL" but V1 D3.3 uses Redis as authoritative for rate-limit; both rely on Redis being up — see INV-005 for the Redis-degraded interaction. Downstream falsifier: an off-by-one between "5 failures triggers lockout" (count ≥5) vs "5 failures permitted, 6th triggers" (count >5) creates a one-attempt window for credential stuffing in the gap between rate-limit reset and lockout activation.
```

```
ID: INV-005
CATEGORY: state_variables
ASSUMPTION: Redis is available for rate-limiting (D3.3/D4.4), lockout state (D3.4/D4.5), session storage (D1.2), OAuth state parameter cache (D3.5/D4.5), AND the V2 R-005 "graceful degradation on Redis loss — accept login with direct PostgreSQL token validation" path is consistent.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: V2 R-005 explicitly says graceful degradation accepts logins on Redis loss. V1 rebuttal R1 weakness #8 flagged this as an internal inconsistency. V2 R2 conceded but said "fix is straightforward: during Redis outage, rate-limiting degrades to per-instance in-memory sliding window, lockout state falls back to a PG-based counter." This concession introduces new invariant violations: (a) per-instance in-memory rate-limit means a multi-pod K8s deployment (HPA min 3, max 10 — V2 D7.4) has 3-10 INDEPENDENT rate-limit counters. An attacker can multiply their effective rate-limit budget by 3-10x by load-balancing requests across pods. (b) The PG-based lockout fallback requires schema and code that neither variant ships — the table `account_lockouts` is not in V2 D1.1 nor V1 D1.2 migration list. (c) OAuth state-parameter validation (V2 D3.5) stores the CSRF state in Redis with 10-min TTL — graceful degradation has no fallback for this, meaning OAuth flows fail outright on Redis loss. The "graceful degradation" path is partial-availability that re-enables brute-force attacks during outage.
```

```
ID: INV-006
CATEGORY: guard_conditions
ASSUMPTION: A-007 joint weakness fix — token-binding race for one-time tokens (email verification, password reset) must use atomic mark-then-verify with single-row claim.
STATUS: ADDRESSED
SEVERITY: HIGH
EVIDENCE: V1 advocate R1 A-007 row proposes `UPDATE password_resets SET used_at = NOW() WHERE token_hash = $1 AND used_at IS NULL RETURNING id` as the atomic claim. V2 advocate R1 A-007 row REJECT also acknowledges the gap. However, the consensus fix is INCOMPLETE: it covers password reset tokens but not the OAuth state-parameter (V2 D3.5 stores in Redis with 10-min TTL — Redis SETNX semantics needed, not specified), nor 2FA recovery codes (V1 D5.5 says "single-use" but no atomic-claim guard specified). Probe extension: 2FA recovery codes are 10 codes per user; if the user submits 2 codes simultaneously (e.g., scripted attack), the lookup-then-mark sequence allows both to validate. Downstream falsifier: the V1 D5.5 hashed-storage with Argon2id means the verify step is slow (intentionally), widening the verify-then-mark race window to ~100ms. Without a SELECT FOR UPDATE or a CAS-style atomic claim, recovery-code reuse is exploitable.
```

```
ID: INV-007
CATEGORY: interaction_effects
ASSUMPTION: Hash-chain audit (D6.5) + async fan-out (A-003 refinement) + per-user session cap eviction (D2.5) preserve total event ordering required for the chain.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: The hash-chain invariant requires that prev_hash of row N+1 references the canonicalized payload of row N. This requires a TOTAL ORDER on audit writes. The consensus has three sources of concurrent audit writes: (a) login emits `auth.login.success` (D6.4); (b) eviction of oldest session emits an event (V2 D2.5 implies but doesn't specify); (c) refresh-token rotation emits an event (D2.1). Under the K8s+HPA topology (3-10 pods), multiple pods can attempt to write audit rows concurrently. The hash-chain requires serializing through a single writer or using a database-level advisory lock — V1 D6.5 specifies neither. The V2 R2 estimate "4.5 engineering days" for hash-chain adoption explicitly omits this serialization cost. If the chain uses Postgres `SERIAL`/`BIGSERIAL` for row ordering AND each writer reads-prev-then-inserts, two concurrent writers can read the same prev_hash → both compute hashes from the same prev → one insert succeeds, one fails-or-overwrites → chain breaks. Downstream falsifier: in a steady-state 30-50 writes/sec audit workload (V2 R2 estimate), the probability of concurrent writes within a millisecond at p99 latency is non-trivial — the chain breaks within hours without a writer lock.
```

```
ID: INV-008
CATEGORY: sufficiency_challenge
ASSUMPTION: Consensus claim that HTTP-only + Secure + SameSite=Strict refresh cookie ALONE mitigates R-001 (XSS-driven token theft).
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: Both variants treat the cookie hardening as sufficient for R-001. Downstream conditions that falsify the sufficiency claim, none of which the consensus addresses: (a) Subdomain takeover — if `api.example.com` issues the refresh cookie but the team loses control of `*.example.com` (e.g., dangling CNAME to a deprovisioned cloud resource), an attacker hosting at `evil.example.com` can read sibling-domain cookies because cookies default to scoping by registrable domain unless `Domain` attribute is set restrictively. V2 D4.6 lists "Strict-Transport-Security" and "Content-Security-Policy" but neither variant specifies the cookie `Domain` attribute scope. (b) Service-worker injection — if the access token is "kept in memory" per V1's frontend integration guide, a service worker registered by malicious JS (e.g., supply-chain attack on a vendored dependency) can intercept the Authorization header on outgoing requests. CSP `default-src 'self'` does not prevent first-party service-worker registration. (c) CSP gap on report-only or unsafe-eval — V1 D7.4 says "no `unsafe-inline`" but does not say "no `unsafe-eval`"; React with certain transpilation modes requires `unsafe-eval`, which would re-enable XSS-driven token-stealing JS. Downstream falsifier: subdomain takeover or service-worker injection bypasses the cookie hardening entirely.
```

```
ID: INV-009
CATEGORY: sufficiency_challenge
ASSUMPTION: Per-user concurrent session cap of 5 (D2.5) prevents credential-stuffing harvest.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: V1 advocate R1 V2-S2 conceded the cap as "limits credential-stuffing harvest size." Downstream conditions that falsify: (a) Multi-IP burst before cap: an attacker with 1,000 botnet IPs can attempt 1,000 simultaneous logins; if any 5 succeed, the attacker has 5 sessions per harvested credential — the cap doesn't prevent the harvest, only bounds the per-credential session count after the fact. (b) OAuth-issued sessions counted differently — V2 D2.5 says "configurable maximum concurrent sessions per user" but the OAuth flow (D3.1) issues tokens via D2.1 refresh-token logic; if OAuth-issued sessions skip the cap check (because the OAuth handler uses a different code path), the cap is bypassable via credential-stuffing the OAuth provider then auto-link. (c) Eviction-policy noise leaks signal — when the legitimate user is logged in and an attacker logs in with stolen credentials, the legitimate user's session is evicted. The "you've been silently evicted" event is a CONFIRMATION SIGNAL to the attacker that they have valid credentials (because eviction == capacity exceeded == auth succeeded). Downstream falsifier: attacker uses successful-eviction-implies-valid-credential as an oracle to harvest credentials at scale, even when the per-credential session count is capped.
```

```
ID: INV-010
CATEGORY: count_divergence
ASSUMPTION: Access-token TTL of 15 minutes (V1 D2.3, V2 D1.6) + refresh-token TTL of 7 days (both variants) consistently bound the role-revocation TOCTOU window (V1 R-012).
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: V1 R-012 claims "Access-token TTL ≤15min bounds staleness; admin force-logout (D7.1) invalidates refresh-token family immediately." This is OFF-BY-ONE on the boundary: a role change AT t=0 means the existing access token (issued at t=-14:59) remains valid until t=+0:01. Worst case: a user's role is REVOKED at t=0, and they have a valid access token good for another 15 minutes minus 1 second. The system says "≤15min bounds staleness" — but the 15-minute window is a HARD upper bound, not an average. For high-stakes role revocations (security incident, terminated employee), 15 minutes of residual privilege is a SOX/SOC 2 finding. Neither variant ships a "force-refresh-on-role-change" mechanism (V2 D4.3 just does `PUT /admin/users/{id}/role` without invalidating active sessions). V1 D7.1 admin force-logout exists but is a SEPARATE manual action — role change != force-logout in the consensus. Downstream falsifier: post-revocation actions during the 15-min window are auditable but not preventable; for a privileged role change (admin → none), this is unacceptable risk.
```

```
ID: INV-011
CATEGORY: state_variables
ASSUMPTION: JWKS endpoint `/.well-known/jwks.json` (V1 D2.4, consensus) is highly available and cached correctly across rotation events.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: V1 R-005 specifies JWKS + `kid` for zero-downtime rotation but does not specify: (a) CACHE TTL on the JWKS endpoint — downstream services (and the auth service itself when validating its own tokens) cache the JWKS response. If the cache TTL is longer than the access-token TTL (15 min), a new key published at t=0 won't be picked up by validators until cache expiry — meaning tokens signed with the new key fail validation. (b) RACE: during rotation, both old and new keys must be present in JWKS for at least one access-token TTL window. V1 doesn't specify this overlap window. (c) JWKS publication failure mode — if the JWKS endpoint returns 5xx during a multi-AZ failover, all token validation fails. V1 says "JWKS endpoint" but not "JWKS hosted on a separately scaling service" — under the consensus K8s topology, JWKS is served by the same pods that auth, so JWKS availability == auth availability. Downstream falsifier: a key rotation during a partial AZ outage causes a validation-failure cascade because the JWKS cache holds old keys but new tokens require new keys.
```

```
ID: INV-012
CATEGORY: collection_boundaries
ASSUMPTION: GDPR `DELETE /me` soft-delete with 30-day grace + tokenized `user_id` in audit (consensus from V1 U-004) preserves audit references AND respects right-to-erasure timing.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: V1 D6.6 says `DELETE /me` triggers "soft-delete + 30-day grace, then crypto-shred." V1 D7.3 says "30-day grace with cancel-link email; crypto-shred PII at grace expiry while preserving audit references via tokenized user_id." Boundary issues: (a) GDPR Article 17 requires erasure "without undue delay" — 30 days is the upper bound, but the consensus treats it as a hard 30-day delay regardless of the user's request. A user who explicitly says "delete immediately, do not retain" may be entitled to faster erasure under regulator interpretation. (b) Tokenization timing: if PII is crypto-shredded at t=+30 days but the audit table's `actor_user_id` was indexed by the original UUID, queries on `actor_user_id` still return rows for the deleted user — the tokenization must happen AT delete time (t=0) on the audit references, not at crypto-shred time (t=+30). V1 D7.3 conflates these timings. (c) Single-user-system edge case: when there is only ONE user (or only ONE admin) and they delete themselves, what happens to audit references where they are the actor on every row? The tokenization scheme produces a constant token for that single user, making the audit log a single-actor log — not meaningfully anonymized. Downstream falsifier: a small-tenant deployment (1-5 users) using tokenized audit IDs is trivially de-anonymizable by correlation; the GDPR claim fails on dataset cardinality grounds.
```

```
ID: INV-013
CATEGORY: interaction_effects
ASSUMPTION: V2's per-user session cap (D2.5, oldest-eviction) + V1's family-tracking refresh model (D3.1, reuse triggers family invalidation) combine cleanly when both are adopted in the consensus merge.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: V1 rebuttal R2 says "merge keeps both: V2's cap + V1's family-tracking." But the interaction is not analyzed. Consider: user has 5 active sessions (cap reached). Sixth login from a new device triggers oldest-eviction. The "evicted" session's refresh token is invalidated — but if that refresh token was the ROOT of a family-tracking chain, what happens to descendants? Two interpretations: (a) Eviction kills the family — then a legitimate long-lived background refresh on the evicted device causes the user to be logged out across all devices. (b) Eviction kills only the leaf — then family-tracking's reuse-detection cannot detect that a "replayed" eviction-victim refresh is a legitimate retry vs an attacker stealing the just-evicted token. Neither variant nor rebuttal specifies which semantics win. Downstream falsifier: combining the two controls creates a logical conflict where either legitimate users are punished (a) or the attack-detection signal is muddled (b).
```

```
ID: INV-014
CATEGORY: guard_conditions
ASSUMPTION: OAuth account linking with explicit user confirmation (NE-3 fix to V2 D3.3) requires the existing-account-holder to have verified their email AND prevents email-takeover-then-link attacks.
STATUS: ADDRESSED
SEVERITY: HIGH
EVIDENCE: V2 R2 NE-3 concedes "D3.3 should be updated to require the existing account holder to confirm the link via email before it is established." But the guard is INCOMPLETE: (a) If the existing account's email is currently controlled by an attacker (email takeover happened LAST WEEK and user hasn't logged in since), the "confirm via email" loop sends to the attacker. The guard must also require RE-AUTHENTICATION with password (or existing 2FA) in the active session — not just an email click. (b) For unverified accounts (V2 D1.1 has `email_verified` boolean default false), the OAuth linking flow shouldn't be permitted at all — neither variant gates linking on `email_verified=true`. An attacker can register with `victim@example.com`, never verify, then OAuth-link a Google account they control over the unverified account. Downstream falsifier: account-takeover via unverified-stub-account-then-link is a documented attack class (CWE-287) that the NE-3 fix as worded does not close.
```

```
ID: INV-015
CATEGORY: count_divergence
ASSUMPTION: V2 D5.4 "10 single-use backup codes, 8-char alphanumeric" provides sufficient entropy and the V1 D5.5 "force re-enroll after any use" is the consensus.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: 8 alphanumeric chars = log2(36^8) ≈ 41.4 bits of entropy per code; with 10 codes per user, an attacker brute-forcing recovery-code endpoint has 10/36^8 ≈ 3.6e-12 probability per attempt — fine in isolation, but: (a) is the recovery-code endpoint RATE-LIMITED under the same key as login? Neither variant specifies. V2 D4.4 rate-limit is keyed by `user_id` but recovery-code submission is pre-2FA-completion — the user is partially authenticated, so `user_id` is known. Still, the limit is "auth endpoints = 100 req/min" — at 100/min, 60 mins/hour, 24 hours = 144,000 attempts/day per user, well within brute-force range for an 8-char code if the attacker has 10 valid codes to hit. (b) V1 D5.5 says "force re-enroll after any use" — but does this mean re-enroll 2FA OR re-enroll ONLY the recovery codes? If the former, every legitimate recovery-code use locks the user out of TOTP until re-enrollment. If the latter, the 10-code budget shrinks by 1 per use but other 9 remain — which is the standard interpretation but contradicts V1's wording. Downstream falsifier: rate-limit gap on recovery-code endpoint enables brute-force; or alternatively, "force re-enroll" semantics force a bad UX or fail to mitigate post-use risk.
```

```
ID: INV-016
CATEGORY: sufficiency_challenge
ASSUMPTION: Consensus NFR-001 latency claim (V1 p95<200ms / V2 p99<200ms / merged: p99 on critical-path + p95 on broader surface) holds under the consensus's synchronous-PG-write audit design + pgcrypto column-level encryption.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: V2 R2 says "primary PG insert (sub-millisecond) remains synchronous; async fan-out happens after response commit." But: (a) pgcrypto column encryption (V2 D6.8, consensus) on the `users.email` column means EVERY login lookup `WHERE email = $1` becomes a SCAN unless a deterministic-encryption mode + indexed search hash column is added — V1 rebuttal R2 flagged this but the consensus has not adopted it as a deliverable. A SCAN on 100K+ users blows the p99 budget. (b) Hash-chain audit (consensus) requires READ-PREV-ROW + WRITE-CURRENT-ROW + serialized via writer lock (see INV-007). The "sub-millisecond PG insert" claim ignores the lock-wait time under concurrent load — at 30-50 writes/sec with a writer lock, contention queues build. (c) Argon2id with V1's memoryCost 64MB + parallelism 2 (D2.1) is a 100-200ms operation on a 4-vCPU node — NFR-001 p99<200ms includes this in the `/login` budget, leaving ~50ms for everything else (network, DB lookup, audit insert, response). Neither variant has joint-load-tested this. Downstream falsifier: pgcrypto without an indexed search hash forces a sequential scan on login; the p99 fails under realistic user counts.
```

```
ID: INV-017
CATEGORY: state_variables
ASSUMPTION: The consensus "async fan-out audit write after response commit" (V2 R2 NE-1 defense, joint A-003 refinement) preserves the AT-LEAST-ONCE audit invariant required for FR-009 (audit logs capture all auth events).
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: "Async after response commit" means: API returns 200 to client, THEN audit event is enqueued/written. State-mechanics violations: (a) Process crashes between response-commit and audit-write → audit event LOST. FR-009 requires 100% capture (V1 G7: "100% of auth events ... logged to immutable store"). (b) The hash-chain (D6.5) requires totally-ordered append; "async fan-out" implies a queue with potentially-reordering consumers, which breaks the chain order. (c) Synchronous-to-PG with replica fan-out (V2 D6.2 as originally written) gives at-least-once IF the PG write is in the request transaction — but V2 R2 says "async fan-out happens after response commit" which puts the write OUTSIDE the request transaction. If the request transaction commits and the audit write fails, there's no compensating action. Downstream falsifier: FR-009's "100% capture" requirement cannot be met by a fire-and-forget audit write; either the audit write is INSIDE the request transaction (blocking p99) or the system accepts <100% audit capture (failing FR-009).
```

```
ID: INV-018
CATEGORY: collection_boundaries
ASSUMPTION: Consensus 10K concurrent sessions (NFR-002) sustained for 30 minutes (V1 G2 / V2 D6.6) under the K8s HPA (min 3, max 10, CPU 70%) topology.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: HPA scales on CPU 70% — but the session-cap-eviction logic (D2.5), hash-chain audit (D6.5), and per-user lockout state (D4.5) are STATEFUL operations that don't necessarily peg CPU. A scenario: 10K sessions at low CPU (because they're idle, holding refresh tokens but not actively requesting), HPA scales DOWN to 3 pods, then a burst of 5K simultaneous refresh requests arrives — the 3 pods are under-provisioned. The HPA scale-up reaction time is 1-3 minutes (Kubernetes default); during that window, p99 latency explodes. Neither variant models the scale-up reaction latency in the NFR. Also: PgBouncer connection limit (V2 D7.4) is unspecified — typical PgBouncer transaction-pool default is 20-25 connections; at 10K concurrent sessions with audit-write fan-out, the pool will saturate. Downstream falsifier: the 30-minute soak test in D6.6 must hold at steady-state, but real production traffic patterns (burst at top-of-hour, business-hour ramp) violate the "sustained" assumption.
```

```
ID: INV-019
CATEGORY: interaction_effects
ASSUMPTION: Hash-chain audit's "daily S3 export with object-lock" (V1 D6.5) interacts cleanly with GDPR crypto-shred at t=+30 days (V1 D7.3) and with the tokenized-user_id audit references (V1 U-004).
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: S3 Object Lock in compliance mode is IMMUTABLE — once written, the object cannot be deleted or modified for the retention period (typically 7+ years for SOX-adjacent compliance, per V1 Open Q #5). This creates an UNRESOLVABLE conflict with GDPR Article 17: (a) the daily audit export to S3 with object-lock contains the user's PII (or tokenized references) at write time; crypto-shredding the PII keys at t=+30 days does NOT delete the S3 object — only renders the PII unreadable IF the encryption key was per-user and is also shredded. (b) The hash-chain itself is preserved in the S3 export, including the canonicalized payload of the row. If the payload contained PII at audit time, the S3 lock prevents removal. The "tokenized user_id" mitigates SOME PII (the user identifier itself) but the `metadata` JSONB field can contain arbitrary auth context (IP, user-agent, sometimes email in legacy formats). (c) Object Lock retention period vs GDPR grace period are configured independently — the consensus does not specify retention period, so there's no proof Object Lock < 30 days OR > 30 days is consistent with crypto-shred timing. Downstream falsifier: a regulator audit finds PII in S3-object-locked exports that cannot be erased; the GDPR claim fails.
```

```
ID: INV-020
CATEGORY: sufficiency_challenge
ASSUMPTION: Consensus combination of (a) NIST-aligned password policy (zxcvbn + HIBP, V2 conceded C-007), (b) Argon2id hashing, (c) breach-list check at registration AND reset is sufficient to meet "OWASP Top 10" zero High/Critical (NFR-003).
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Downstream conditions that falsify: (a) HIBP k-anonymity check has rate-limit/availability dependencies — if HIBP API is down at registration, does the system fail-open (accept any password including known-breached) or fail-closed (block registration)? Neither variant specifies. Fail-open re-enables breached-password registration; fail-closed blocks all new registrations during a third-party outage. (b) The zxcvbn check is client-side or server-side? If client-side only, an attacker bypassing the JS check submits any password. V1 D2.1 says "zxcvbn strength check" but doesn't specify locus. (c) Password CHANGE flow (V2 D5.5 `PUT /auth/password`) — does it re-check HIBP and zxcvbn, or only the registration flow? V2's D5.5 description is "authenticated password change requiring current password" — no mention of the breach-list check. A user can register with a strong password, then change to a weak/breached one if the change endpoint doesn't enforce. Downstream falsifier: any of these three gaps (fail-open HIBP, client-side-only zxcvbn, change-flow bypass) reintroduces the NIST-deprecated weak-password attack surface.
```

---

## Summary

**Total findings**: 20

**By status**:

- ADDRESSED: 2 (INV-006, INV-014 — both with caveats noting the address is incomplete)
- UNADDRESSED: 18

**By severity**:

- HIGH: 12 (INV-001, INV-002, INV-004, INV-005, INV-006, INV-007, INV-008, INV-012, INV-014, INV-016, INV-017, INV-019)
- MEDIUM: 8 (INV-003, INV-009, INV-010, INV-011, INV-013, INV-015, INV-018, INV-020)
- LOW: 0

**By category**:

- state_variables: 3 (INV-005, INV-011, INV-017)
- guard_conditions: 2 (INV-006, INV-014)
- count_divergence: 3 (INV-004, INV-010, INV-015)
- collection_boundaries: 3 (INV-003, INV-012, INV-018)
- interaction_effects: 4 (INV-002, INV-007, INV-013, INV-019)
- sufficiency_challenge: 5 (INV-001, INV-008, INV-009, INV-016, INV-020)

**HIGH + UNADDRESSED (blocking convergence)**: 10

- INV-001 (hash-chain genesis/canonicalization/tip-publication gaps)
- INV-002 (SameSite=Strict vs OAuth callback interaction)
- INV-004 (lockout vs rate-limit threshold collision and counter divergence)
- INV-005 (Redis-degraded multi-pod rate-limit bypass + missing PG lockout schema)
- INV-007 (hash-chain serialization requirement under K8s multi-pod writes)
- INV-008 (cookie hardening insufficient without subdomain/SW/CSP controls)
- INV-012 (tokenized user_id GDPR boundary timing + small-tenant de-anonymization)
- INV-016 (pgcrypto email lookup → SCAN breaks NFR-001 p99)
- INV-017 (async-after-commit audit violates FR-009 at-least-once)
- INV-019 (S3 Object Lock immutability conflicts with GDPR crypto-shred)

**Top blocking finding** (highest severity + most-likely-to-cascade): **INV-017** (async-after-commit audit write breaks FR-009's "100% of auth events" capture invariant). FR-009 is a hard functional requirement; the consensus's A-003 refinement to escape the p99-vs-synchronous-audit dilemma directly violates it. This is a foundational design contradiction the consensus has not resolved — both variants traded the audit-durability invariant to preserve the latency invariant, but neither budgeted for the trade-off in their roadmap. Resolution requires either (a) accepting <100% audit capture and amending FR-009, (b) accepting synchronous-in-transaction audit writes and amending NFR-001, or (c) introducing a durable queue (e.g., outbox pattern with WAL replay) as a NEW deliverable absent from both variants.

**Runners-up for top blocking**:

- INV-019 (S3 Object Lock vs GDPR crypto-shred): regulatory irreconcilability requires either dropping Object Lock OR accepting that GDPR erasure is partial.
- INV-001 (hash-chain forensic gaps): the tamper-evidence claim that R1/R2 made the keystone of V1's compliance argument is technically incomplete as specified.
- INV-007 (hash-chain serialization): the cryptographic invariant requires a writer lock that neither variant ships, undermining the "4.5 day" cost estimate V2 used to concede the chain.
