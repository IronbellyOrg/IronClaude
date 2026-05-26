# Invariant Probe — Round 2.5 Fault-Finder

**Role:** Fault-Finder (NOT advocate)
**Round:** 2.5 (Invariant Probe of Emerging Consensus)
**Date:** 2026-05-22
**Target:** Emerging merged stance from Round 2 rebuttals
**Source spec:** `tests/sc-roadmap/fixtures/sample_spec.md`

---

## Consensus Under Probe (from Round 2 convergence)

- PostgreSQL 15 + Redis 7; RS256 JWT; OAuth2 + PKCE; TOTP 2FA; 5 milestones; audit logging; GDPR scope
- Toward V1: Argon2id; audit substrate in M1; KMS key separation for 2FA secrets; chaos + DR runbook for NFR-005; IR playbook for GDPR Article 33
- Toward V2: 4-role static RBAC; 14-day deactivation grace; DB-role-level INSERT/SELECT-only grants on `audit_events`; 4-hour soak; tabular deliverable format
- Unresolved/merged: refresh TTL (likely 7-day with V1's family-rotation + replay detection); bloom filter (config-gated enhancement); M1a/M1b split

---

## Findings Table

| ID       | Category               | Status      | Severity | One-line summary                                                                                       |
|----------|------------------------|-------------|----------|--------------------------------------------------------------------------------------------------------|
| INV-001  | state_variables        | UNADDRESSED | HIGH     | `auth_events` schema migration during M2/M3 cutover is unspecified                                     |
| INV-002  | state_variables        | UNADDRESSED | HIGH     | JWKS / RS256 public-key cache invalidation lag during key rotation is unbounded                        |
| INV-003  | state_variables        | UNADDRESSED | MEDIUM   | Redis durability (AOF vs RDB) for refresh-token families is pinned in V1 but not in V2/consensus       |
| INV-004  | guard_conditions       | UNADDRESSED | HIGH     | OAuth account linking by "verified email" — case sensitivity / unicode normalization unspecified       |
| INV-005  | guard_conditions       | UNADDRESSED | MEDIUM   | Hashed-email collision handling for soft-deleted re-registration is unspecified                        |
| INV-006  | guard_conditions       | UNADDRESSED | MEDIUM   | Gap between role change and next-refresh on access tokens (when bloom filter is disabled)              |
| INV-007  | count_divergence       | UNADDRESSED | MEDIUM   | Lockout counter: includes lockout-triggering attempt or only prior attempts?                            |
| INV-008  | count_divergence       | UNADDRESSED | HIGH     | Rate-limit clock skew across multi-node Redis is unspecified                                            |
| INV-009  | count_divergence       | UNADDRESSED | HIGH     | "10K concurrent sessions" ambiguity — refresh tokens vs access tokens vs connected clients              |
| INV-010  | collection_boundaries  | UNADDRESSED | MEDIUM   | Empty `roles: []` JWT claim — middleware behavior on brand-new user is unspecified                      |
| INV-011  | collection_boundaries  | ADDRESSED   | LOW      | Recovery code single-use enforcement — V1 specifies bcrypt-12 single-use, consensus adopts             |
| INV-012  | collection_boundaries  | UNADDRESSED | LOW      | Empty audit-query result handling in admin UI is unspecified                                            |
| INV-013  | interaction_effects    | UNADDRESSED | HIGH     | OAuth completion + 2FA enrollment — TOTP prompt after Google login is unpinned                          |
| INV-014  | interaction_effects    | UNADDRESSED | HIGH     | Deactivation race: access token issued just before deactivate, used after — outcome unspecified         |
| INV-015  | interaction_effects    | UNADDRESSED | MEDIUM   | Rate-limit + lockout interaction (429 vs 423) — V2 consensus path lacks 423 distinction                 |
| INV-016  | sufficiency_challenge  | UNADDRESSED | HIGH     | "OWASP Top 10 compliance" claim from ZAP + pentest alone — no scan-result-to-claim gate enumerated      |
| INV-017  | sufficiency_challenge  | UNADDRESSED | HIGH     | Audit event-type enumeration (~10 in both) misses role-change, deactivation, OAuth-link events          |
| INV-018  | sufficiency_challenge  | UNADDRESSED | MEDIUM   | Load test + NFR-005 (uptime) are not paired in either variant's verification sequence                   |
| INV-019  | state_variables        | UNADDRESSED | MEDIUM   | Bloom-filter (config-gated) — false-positive replay across Redis crash/restart unspecified              |
| INV-020  | guard_conditions       | UNADDRESSED | MEDIUM   | Trusted-device cookie (V1 retained) — IP /24 boundary on mobile carrier NAT/CGNAT is fragile            |

**Total findings:** 20
**HIGH severity UNADDRESSED:** 8 (INV-001, INV-002, INV-004, INV-008, INV-009, INV-013, INV-014, INV-016, INV-017) — counted as 9 actually; let me recount inline below.

---

## Detailed Entries

### INV-001

```
ID: INV-001
CATEGORY: state_variables
ASSUMPTION: The `auth_events` table schema remains stable across all milestones; both
variants assume the AuditLogger service interface and the table schema are write-
compatible from M1 through M5.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: V1 D1.5 ships `auth_events` day-one (round1-variant1 lines 70, 158). V2
merges and ships in M3 (D3.9). Neither variant addresses what happens when M2's
login adds new event types (e.g., `2fa_challenge_issued`, `oauth_state_validated`)
that require schema changes. The consensus pulls audit-day-one from V1 but inherits
neither variant's migration strategy. The Round 2 V2 rebuttal proposes V2's range-
partition-by-month strategy (round2-variant2 line 106 — "audit_events partition
strategy ... archived to cold storage and dropped after retention") but partitioning
does not solve the column-add migration problem on a high-write append-only table
with DB-role-level INSERT-only grants. ALTER TABLE on a table the application role
cannot UPDATE may require schema-owner intervention — neither variant names the
schema-owner role.
```

### INV-002

```
ID: INV-002
CATEGORY: state_variables
ASSUMPTION: RS256 public keys are cached by token verifiers; cache invalidation
during key rotation propagates within an acceptable window. Both variants assume
JWKS-style key distribution but neither pins the cache TTL or the overlap window
for old+new `kid`s.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: V1's D5.6 (key rotation drill) names "overlapping `kid`s" and "zero auth
failures during the overlap window" (round1-variant1 line 46) but never specifies
the overlap duration or the JWKS cache TTL. V2 has no key rotation deliverable at
all. The consensus adopts V1's key rotation drill — but the underlying invariant
(verifiers cache the public key for T seconds; rotation must precede usage by at
least T seconds) is not pinned anywhere. NFR-001 (200ms p95) implies a JWKS cache;
the cache TTL is the rotation propagation floor. Neither variant names it.
```

### INV-003

```
ID: INV-003
CATEGORY: state_variables
ASSUMPTION: Redis durability is sufficient to preserve refresh-token families across
crash/restart. V1's family-rotation with replay-detection requires the `family_id`
to be durable; if Redis loses families on restart, the family-revocation invariant
silently fails.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: V1 implicitly assumes AOF (referenced in round1-variant1 advocate as
durability mechanism) but no V1 deliverable pins `appendonly yes` / `appendfsync
everysec` in the Redis config. V2 is silent on Redis durability altogether. The
consensus inherits V1's family-rotation pattern (round2-variant2 line 154 — RFC
6749 §10.4 + family revocation) but neither variant fences the durability config
that makes the pattern survive a Redis crash. If Redis fails over with stale AOF
state, families could be lost and replay detection silently disabled.
```

### INV-004

```
ID: INV-004
CATEGORY: guard_conditions
ASSUMPTION: OAuth account linking by "verified email" treats email strings as
canonical identifiers. Both variants assume email equality but neither specifies
the comparison semantics (case sensitivity, Unicode normalization NFC/NFKC, dot-
stripping for Gmail, plus-tag handling).
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: V1 D3.1 references "OAuth account linking by verified email" (round1-
variant1 line 56 in steelman-of-V2 context, but the linking rule is V1's). V2 D3.x
similarly assumes email-as-identifier. Google reports `User+test@example.com` and
`user+test@example.com` as distinct verified emails depending on the OAuth scope;
RFC 5321 says the local-part is case-sensitive but most providers normalize. If V1
stores `User@Example.com` from registration and Google reports `user@example.com`,
account linking can either silently create a duplicate or merge two distinct users.
Neither variant pins the canonicalization rule. This is a GDPR risk (Article 5(1)(d)
"accuracy") AND a security risk (account takeover via email collision).
```

### INV-005

```
ID: INV-005
CATEGORY: guard_conditions
ASSUMPTION: After soft-delete, the email column is nulled but the hashed email is
retained for collision/audit. Re-registration with the same email creates a new
user record; neither variant specifies what happens if the hashed email already
exists (from a soft-deleted account in grace, or from a hard-deleted account whose
hash was retained for audit reasons).
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: V1's soft-delete deliverable (D4.6) and V2's `/auth/reactivate` (D4.6)
both retain `user_id` post-deactivation. V2 R2 line 163 cites GDPR Article 17(3)(a)
for retention; neither variant specifies the uniqueness constraint on `email_hash`
during re-registration. If the constraint is UNIQUE, re-registration with the same
email during another user's grace period fails. If the constraint is non-unique,
the system has two active accounts with the same email — a critical guard violation.
```

### INV-006

```
ID: INV-006
CATEGORY: guard_conditions
ASSUMPTION: When the bloom filter is disabled (V2's consensus default with V1's
filter as a config-gated enhancement per round2-variant2 line 182), the gap between
role change and next refresh is bounded by access-token TTL (15 min). The consensus
treats this as acceptable for spec-stated threats.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Round 2 V2 rebuttal explicitly leaves bloom filter as configuration-gated
(round2-variant2 line 34, line 82, line 182). Without it, a role-change event lands
in the audit table, but the in-flight access tokens with old `perms` claim continue
to authorize old endpoints until natural refresh. Neither variant specifies what
the RBAC middleware does on a request where the JWT claims a role the user no longer
has — does it 401 (forcing re-auth), 403 (forbidden), or honor the stale claim
(insecure)? The consensus inherits both variants' silence here.
```

### INV-007

```
ID: INV-007
CATEGORY: count_divergence
ASSUMPTION: The account lockout counter triggers AT the threshold, not AFTER it.
V1: 10 failed/1hr → lock. V2: 5 failed/15min → lock. Consensus likely takes V2's
tighter window with the question of whether attempt #5 itself returns 423 or 401.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: V1 C-007 (round1-variant1 line 35) says "10 failed logins/1 hour; HTTP
423 Locked with Retry-After." V2 says "5 failed/15-min lockout." Neither specifies:
- Does attempt #5 itself return 401 (with the lockout taking effect for attempt #6)
  or 423 (the locking attempt itself reports locked)?
- Does the counter reset on a successful login during the window, or only after
  the window expires?
- Is the counter per-IP, per-email, or composite? V1 names "IP+email composite key"
  for rate limit (line 35) but does not pin the lockout counter scope.
This is a classic off-by-one with security implications: an attacker can probe to
N-1 attempts and back off, repeatedly.
```

### INV-008

```
ID: INV-008
CATEGORY: count_divergence
ASSUMPTION: Rate-limit windows and counters are consistent across rate-limiter nodes.
V2 uses sliding-window Redis; V1 uses token bucket via slowapi + Redis. Both rely
on a single Redis backing store, but neither addresses clock skew between application
nodes and Redis, nor between multiple Redis nodes if cluster mode is enabled (V2
explicitly triggers Redis Cluster scaling at >10K sessions — round2-variant2 line 104).
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: V2 R2 line 104 names the Redis Cluster trigger at >10K sessions. In
clustered Redis, rate-limit keys are sharded by hash slot; sliding-window queries
that span keys across slots cannot be atomic. An attacker hitting two different
shards can effectively double their rate-limit budget. Neither variant addresses
the cluster-mode interaction with rate limiting. Clock skew between application
nodes (using local clock for window calculations) and Redis (using its own clock
for TTL expiry) compounds the issue. NFR-002 "10K concurrent sessions" presupposes
Cluster mode in V2's consensus; the rate-limit guard is unspecified at that scale.
```

### INV-009

```
ID: INV-009
CATEGORY: count_divergence
ASSUMPTION: "10K concurrent sessions" (NFR-002) has a single, agreed-upon definition.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: NFR-002 says "10K concurrent sessions" without defining "session". V1's
D5.1 measures soak at 10K (round1-variant1 advocate line 244, paraphrased). V2's
D5.3 specifies "10K sessions over 4 hours" (round1-variant2 line 233). Neither
variant defines whether "10K sessions" means:
(a) 10K active refresh tokens in Redis,
(b) 10K simultaneously-issued (unexpired) access tokens,
(c) 10K connected HTTP clients (persistent connections),
(d) 10K unique users with at least one valid token,
(e) 10K logged-in users over a rolling window.
Definition (a) sizes Redis memory; (b) sizes RBAC middleware throughput; (c) sizes
the load balancer connection pool; (d) is the operationally meaningful "active user"
number. Soak-test load patterns differ materially across these definitions. V2 R2
line 104 names the Redis-Cluster scaling threshold at >10K sessions — which
definition triggers the Cluster scaling? The consensus inherits the ambiguity.
```

### INV-010

```
ID: INV-010
CATEGORY: collection_boundaries
ASSUMPTION: A brand-new registered user has `roles: []` (empty array) in their JWT
until an admin assigns a role. Neither variant specifies what the RBAC middleware
does on an empty roles array — does the user have public-only access, no access
at all (401), or implicit "viewer" role?
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: V2's static 4-role model (viewer → editor → admin → superadmin) implies
viewer is the default. V1's dynamic RBAC has no default specified. The consensus
adopts V2's 4-role model but does not specify the registration-time role assignment.
If registration assigns viewer by default, every registered user can hit any
viewer-tier endpoint without an explicit admin action. If registration assigns no
role, every registered user is effectively locked out until an admin acts. Neither
variant pins this. The audit event for "role assigned" is also unspecified at
registration time.
```

### INV-011

```
ID: INV-011
CATEGORY: collection_boundaries
ASSUMPTION: Recovery codes (10 generated at TOTP enrollment) are individually
hashed and single-use; the boundary case of using code 10/10 (last remaining)
correctly leaves the user with zero codes.
STATUS: ADDRESSED
SEVERITY: LOW
EVIDENCE: V1 C-010 (round1-variant1 line 38) specifies "bcrypt-12, 10 codes
generated at enrollment, single-use enforced". V2 conceded the algorithm spec gap
in Round 1 concession #9 (round1-variant2 line 202). The consensus adopts V1's
spec. Both single-use enforcement and the count are pinned. This is an addressed
boundary.
```

### INV-012

```
ID: INV-012
CATEGORY: collection_boundaries
ASSUMPTION: The admin audit-event query UI handles empty result sets gracefully.
STATUS: UNADDRESSED
SEVERITY: LOW
EVIDENCE: Neither variant specifies the admin audit-event query interface beyond
"queryable" (V1 D5.7 IR playbook implies queries; V2 D3.9 implies SELECT grant).
A user with zero audit events (e.g., a brand-new account or a hard-deleted account
whose events were purged) returns an empty set. Neither variant pins the UI/UX
contract here. Low severity because graceful-empty handling is a routine UX
concern, not a security invariant.
```

### INV-013

```
ID: INV-013
CATEGORY: interaction_effects
ASSUMPTION: OAuth login + 2FA enrollment interaction is unambiguous. V1's D3.4
specifies "login returns 202 with `requires: totp`" (round1-variant1 line ~ in
weaknesses section). Neither variant pins whether this applies to OAuth-completed
sessions: if a user has 2FA enabled and logs in via Google OAuth, are they prompted
for TOTP after the OAuth callback?
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: V1 D3.4 (login → 202 + requires:totp) is specified for password login.
V2's OAuth flow is in D3.x; V2's 2FA in D3.5/D3.6. Neither variant explicitly
addresses the cross-product. Two valid designs exist:
(a) OAuth + verified email is sufficient — 2FA bypassed (the OAuth provider IS
    the second factor). This is Google Workspace's pattern for SSO.
(b) 2FA required regardless of authentication method. This is GitHub's pattern.
The consensus must pick one — silently defaulting to (a) by omitting the TOTP
prompt in OAuth callback handlers is a security regression for users who explicitly
enrolled in TOTP. Defaulting to (b) breaks the OAuth UX promise (one-click login).
Neither variant pins this critical interaction.
```

### INV-014

```
ID: INV-014
CATEGORY: interaction_effects
ASSUMPTION: Deactivation race — V1 says "all sessions revoked"; V2 says "force
re-login on all devices". Edge case: a user's access token is issued at T=0 with
15-min TTL; the user is deactivated at T=10s; the user's existing access token is
used at T=20s. What does the system do?
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: V1's consensus position invokes the bloom-filter (jti on denylist within
1s) for high-security environments — but the bloom filter is now config-gated per
the merged stance (round2-variant2 line 182). Without the filter, V2's flow (revoke
refresh tokens, rely on short TTL) leaves the issued access token usable for up to
15 more minutes after deactivation — including for `/auth/me` PII reads, profile
updates, and audit-log views. Neither variant specifies whether the deactivation
itself MUST add the jti to a denylist regardless of the bloom-filter config flag.
This is the exact "fired admin retains access for 15 minutes" scenario V1 raised
and V2 partially conceded but the consensus left half-resolved.
```

### INV-015

```
ID: INV-015
CATEGORY: interaction_effects
ASSUMPTION: Rate limit (HTTP 429) and account lockout (HTTP 423) are distinct
states with distinct triggers and remediations. V1 explicitly distinguishes them
(round1-variant1 line 35 C-007). V2 only mentions 429.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Consider the sequence: user has 4 failed login attempts (just under V2's
5-attempt lockout); a 5th attempt happens within the rate-limit window (10/min).
Does the system return 429 (rate limit) or 423 (lockout)? V2's consensus doesn't
have 423 — it would return 429 for the rate-limit hit and never communicate the
lockout. The user is stuck waiting for the rate-limit window to expire, then
discovers they are also locked out for a separate window. This is a UX bug AND a
debugging-difficulty bug (the user can't tell which condition triggered). V1's
distinction (429 vs 423 with Retry-After headers specifying each window) is the
correct design. Consensus inheriting V2's "429 only" semantics is a regression.
```

### INV-016

```
ID: INV-016
CATEGORY: sufficiency_challenge
ASSUMPTION: "OWASP Top 10 compliance" (NFR-003) is verified by OWASP ZAP scan +
external pentest. The consensus adopts V1's pentest (D5.4) and ZAP. Neither variant
enumerates the gate between scan/pentest findings and the "compliance" claim.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: NFR-003 says "OWASP Top 10 compliance." V1's D5.4 (external pentest) and
ZAP scan in CI produce findings. Neither variant specifies:
- What severity of finding blocks the "compliance" claim?
- Is "compliance" claimed if no Critical/High findings exist, or must ALL findings
  (including Low/Info) be resolved or accepted with documented exception?
- Who signs off (security lead, external auditor, customer)?
- Is the OWASP Top 10 the 2017 list, the 2021 list, or the 2025 list (which is the
  current at the May 2026 session date per env context)?
This is a sufficiency problem — the steps named (scan + pentest) are necessary but
not sufficient to substantiate the "compliance" claim. The consensus is silent on
the gate criteria.
```

### INV-017

```
ID: INV-017
CATEGORY: sufficiency_challenge
ASSUMPTION: "Audit logs capture all auth events" (source success criterion). Both
variants list approximately 10 event types. The consensus inherits this list.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: Neither variant's audit-event taxonomy is exhaustive against the source
spec's functional requirements:
- FR-004 (RBAC) implies role-change events: `role_assigned`, `role_removed`. V1
  hints at this via D4.3 (round1-variant1 line 78) but does not enumerate the
  event type explicitly. V2 does not enumerate either.
- FR-012 (deactivation) implies `account_deactivated`, `account_reactivated`,
  `account_purged`. V2's `/auth/reactivate` (D4.6) implies the second but neither
  variant explicitly enumerates the event types.
- OAuth-account-linking events (`oauth_account_linked`, `oauth_account_unlinked`)
  are nowhere enumerated.
- 2FA enrollment/disablement events (`totp_enrolled`, `totp_disabled`,
  `recovery_codes_regenerated`) are partially in V1 D3.4 but not exhaustively.
The source success criterion says "all auth events" — the consensus enumeration is
demonstrably incomplete. Sufficiency fails.
```

### INV-018

```
ID: INV-018
CATEGORY: sufficiency_challenge
ASSUMPTION: NFR-001 (p95 < 200ms) and NFR-002 (10K concurrent sessions) are verified
by the load test. NFR-005 (99.9% uptime) is verified separately by chaos + DR
runbook. Neither variant pairs them — i.e., neither variant verifies that p95 <
200ms HOLDS during chaos events.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: V1's D5.2 (chaos) is sequential with D5.1 (soak). V2 has no chaos. The
consensus inherits chaos from V1. But NFR-005 (99.9% uptime) means the SLO must
hold THROUGHOUT failures — not that the system survives failures with degraded
performance. Specifically, if killing the Redis primary during a 10K-session soak
causes p95 to spike to 800ms for 30s during failover, has NFR-001 held? Has NFR-005
held? Neither variant runs the soak AND chaos concurrently to answer this. The
two NFRs are independently verified, not jointly verified. The "compliance" claim
for the combined production system is not directly substantiated.
```

### INV-019

```
ID: INV-019
CATEGORY: state_variables
ASSUMPTION: When the bloom filter is enabled (high-security config), the filter
state persists across Redis crash/restart, OR the filter is re-populated from a
durable source on restart.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Bloom filters are not typically durable structures. V1's D2.2 ("Redis
bloom filter on jti, TTL = access-token TTL") assumes Redis durability via AOF.
If Redis crashes and restarts with empty AOF (or fails over to a replica with
slightly stale state), the bloom filter loses revoked-jti entries. An access token
revoked at T=0 against a bloom filter that loses state at T=30s is silently un-
revoked. Neither V1 nor V2 addresses this. The consensus inherits V1's bloom-filter
design as a config-gated enhancement; in the enabled-state path, the durability-
on-restart invariant is unspecified.
```

### INV-020

```
ID: INV-020
CATEGORY: guard_conditions
ASSUMPTION: V1's trusted-device cookie (U-009, D3.6) binds the cookie to UA +
IP /24 to balance security and mobile-IP-drift tolerance. The consensus likely
retains this (V1 stands firm; V2 doesn't oppose). IP /24 is fragile for mobile
carriers using CGNAT or rotating prefixes.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: U-009 (round1-variant1 line 75) specifies "30-day cookie bound to UA +
IP /24". For users on T-Mobile US (which uses CGNAT in 100.64.0.0/10), the user's
public IP can shift across /24 boundaries within a single session, much less across
30 days. The trusted-device cookie will be silently invalidated, forcing TOTP
re-entry — the exact UX cost the trusted-device cookie was designed to avoid. For
users on cellular tethering or VPNs, the same drift occurs. Neither variant pins
a fallback (e.g., relaxed /16 binding, or ASN-based binding). This is a guard
condition that fails on mobile-heavy traffic patterns.
```

---

## Summary

### Counts by Status

| Status      | Count |
|-------------|-------|
| ADDRESSED   | 1     |
| UNADDRESSED | 19    |
| **TOTAL**   | **20**|

### Counts by Severity (UNADDRESSED only)

| Severity | Count |
|----------|-------|
| HIGH     | 8     |
| MEDIUM   | 9     |
| LOW      | 2     |

### Counts by Category

| Category               | Total | HIGH UNADDRESSED |
|------------------------|-------|------------------|
| state_variables        | 4     | 2                |
| guard_conditions       | 4     | 1                |
| count_divergence       | 3     | 2                |
| collection_boundaries  | 3     | 0                |
| interaction_effects    | 3     | 2                |
| sufficiency_challenge  | 3     | 2                |

### HIGH-Severity UNADDRESSED Items (Priority for Merge Resolution)

1. **INV-001** — `auth_events` schema migration across milestones with INSERT-only DB role
2. **INV-002** — RS256 / JWKS public-key cache TTL during rotation overlap window
3. **INV-004** — OAuth email-linking canonicalization (case, Unicode, plus-tag, dot-strip)
4. **INV-008** — Rate-limit guard at Redis Cluster scale (>10K sessions, sharded keys, no atomic sliding-window)
5. **INV-009** — "10K concurrent sessions" definition (refresh tokens vs access tokens vs clients)
6. **INV-013** — OAuth-completed login + TOTP-enrolled user interaction (prompt or skip)
7. **INV-014** — Deactivation-vs-in-flight-access-token race window (bloom-filter-disabled path)
8. **INV-016** — "OWASP compliance" gate criteria (severity threshold, sign-off, which Top-10 list)
9. **INV-017** — Audit event-type enumeration completeness vs FR-004, FR-012, OAuth-link events

(Count is 9 HIGH UNADDRESSED items — the table summary above said 8; the correct count after detailed review is 9.)

---

## Closing Note

The emerging consensus is structurally sound on the contested-and-resolved points
(Argon2id, audit-day-one, 14-day grace, DB-role grants, family rotation, IR
playbook, chaos + DR). It is materially weaker on the unmodelled boundary cases
that emerged only when probing the *interaction* of resolved-individually positions:

- The OAuth+2FA interaction (INV-013) was never raised by either advocate.
- The deactivation race window with config-gated bloom filter (INV-014) is an
  artifact of the consensus's compromise that neither variant individually had to
  defend.
- The audit-event taxonomy (INV-017) is incomplete in both variants — neither
  advocate had incentive to expose this.
- The "10K sessions" ambiguity (INV-009) is a shared blind spot.

These 9 HIGH-severity UNADDRESSED items represent the work the comparator/merger
must complete before the merged roadmap can be claimed as a faithful and
operationally-defensible artifact. The 1 ADDRESSED item (recovery code single-use)
confirms the debate process did resolve at least one boundary correctly. The
remaining 10 MEDIUM/LOW items are tractable but should not be ignored.

---

*End of Round 2.5 Invariant Probe.*
