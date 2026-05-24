# Round 1 — Variant 1 Advocate

**Role:** Advocate for Variant 1 (opus / default persona)
**Round:** 1
**Date:** 2026-05-22
**Opposing Variant:** Variant 2 (sonnet / default persona)

---

### Position Summary

Variant 1 delivers a defensible **security-first** roadmap that treats the auth system as a long-lived production substrate, not a feature checklist. It establishes audit on day one (M1), commits to the OWASP 2025 forward choice (Argon2id) rather than the legacy-acceptable bcrypt, and budgets explicit operational drills — chaos, DR with RTO/RPO numbers, key rotation, external pentest, IR playbook — that turn NFR-005 ("99.9% uptime") and NFR-003 ("OWASP compliance") from claims into evidence. V1's critical-path framing (14 weeks, single engineer) is tighter than V2's 17 weeks, despite covering strictly more security and operational ground.

---

### Steelman of Variant 2 — strongest version of V2's positions

Before critiquing, I owe V2 an honest reading. The places where V2 is genuinely stronger:

**1. Avatar upload (U-012, D4.2).** V1's FR-010 coverage is honest about profile fields (name, email, phone) but **never names the avatar upload path**. V2 explicitly carves `POST /auth/me/avatar` with S3/R2 + signed-URL delivery. FR-010 in the source spec says "user profile management" — an avatar field is the single most common profile attribute in any production system, and V2 is right to surface it as a deliverable rather than an implicit subtask. V1 has a coverage gap here.

**2. Explicit reactivation endpoint (U-013, D4.6).** V1 has a 30-day soft-delete window but treats reactivation as an implicit consequence of logging in during the grace period. V2 carves `POST /auth/reactivate` as a deliberate action — separating *passive grace* from *expressed intent to reactivate* is the cleaner UX model and the cleaner audit story (you get a `reactivated` event distinct from `login_during_grace`). This is good product design that V1 missed.

**3. Audit table DB-role enforcement (U-014, D3.9).** V2's "no UPDATE/DELETE grants for the application role — only INSERT and SELECT" on `audit_events` is a **stronger invariant than what V1 specifies**. V1 says "append-only" but never names the enforcement layer; V2 names the database role. A compromised application in V2's design **literally cannot tamper with audit history**. This is defense-in-depth at the right layer (the persistence boundary), and V1 should have specified it. This is the single strongest concrete win for V2.

**4. Longer soak (C-018, 4 hours vs 1 hour).** V2's 4-hour soak is more likely to surface memory leaks, connection-pool exhaustion, and Redis-key-expiry slow paths than V1's 1-hour window. The argument that "1 hour is enough because the system is stateless" is weaker than "4 hours is enough to catch the slow leaks that 1 hour misses." V2 is more conservative here in a way that aligns with NFR-005.

**5. Simpler RBAC (C-004, 4 static roles).** The source spec says **"RBAC"** — literally "role-based access control." It does not say "ABAC," "permission matrix," or "fine-grained permissions." V2's static 4-role hierarchy (`viewer → editor → admin → superadmin`) is **closer to the literal text of FR-004** than V1's dynamic `roles × permissions × role_permissions × user_roles` schema. V2 is right that you can extend the `user_roles` table with a `permissions` JSONB column later without breaking migrations — YAGNI cuts in V2's favor here.

**6. 14-day grace period (C-008).** V2's 14-day window aligns with **common industry practice** (Google: 20 days, Microsoft: 30 days, GitHub: 90 days for orgs but ~14 for individuals). V1's 30 days is more user-protective but also retains PII longer under GDPR — and GDPR Article 17 asks for "without undue delay." 14 days is defensible as a balance between user recovery and faster erasure compliance. V2's choice is not strictly worse; it just trades on a different axis.

**7. Sliding-window rate limit (C-006).** V2's sliding-window has **strictly better burst-rejection accuracy** than V1's token-bucket at the edge of the window. Token-bucket allows a 2× burst at the boundary (consume the entire bucket, then immediately refill); sliding-window does not. For an auth login endpoint where R-002 (brute force) is "High Impact / High Probability," sliding-window is arguably the more conservative choice. V1's token-bucket is correct for *user-facing* APIs where burst tolerance is a feature; it is debatable for security-critical endpoints.

These are real strengths. V2 is not a weak document.

---

### Strengths Claimed (Variant 1)

#### V1-only contributions — operational readiness

**Chaos engineering (U-001, D5.2).** V2 has a 4-hour soak; V1 has a soak **plus** chaos. V1 explicitly kills the Redis primary mid-traffic (failover within 10s expected), kills one API replica, and partitions the DB read-replica. **Without chaos, NFR-005 (99.9% uptime) is an unverified claim.** A system that survives steady-state load but cannot survive a single Redis primary failure does not meet 99.9% — a Redis primary failure during peak hours alone would consume the entire annual error budget (~8.76 hours). V2's "argue equivalence from architecture: multi-AZ, no single point of failure, automated failover" (D5.6) is **architectural hand-waving** when no failover has actually been triggered.

**DR runbook with RTO/RPO (U-002, D5.5).** V1 names numbers: **RTO 1 hour, RPO 5 minutes**, and requires a tabletop exercise. V2 has "Production deployment runbook" only — no RTO, no RPO, no tabletop. NFR-005 is "99.9% uptime" — that is **an availability commitment that implies recovery time bounds**. You cannot make a 99.9% commitment without RTO numbers; the math doesn't close. V2's roadmap leaves the SRE on call with no agreed contract.

**Key rotation drill (U-003, D5.6).** V1 explicitly rotates the JWT signing key (RS256 supports overlapping `kid`s) **and** the column-encryption key, in staging, with measurement of zero auth failures during the overlap window. V2 says "key rotation procedure documented" in D5.7 — documented, not exercised. A key-rotation procedure that has never been run is a procedure that will fail at the worst possible time.

**External pentest (U-004, D5.4).** V1 engages an external vendor (Cobalt or equivalent) with a 4-week lead and gates GA on findings. V2 runs OWASP ZAP only. **ZAP is a baseline scanner; it is not a pentest.** OWASP itself ([OWASP WSTG](https://owasp.org/www-project-web-security-testing-guide/)) distinguishes "automated scanning" from "manual testing" — ZAP catches the easy stuff. Auth-system vulnerabilities (race conditions in token rotation, OAuth state-parameter confusion, TOTP code-replay windows, recovery-code enumeration) often require human-driven testing. V2's NFR-003 "OWASP compliance" is **self-asserted**; V1's is third-party-validated.

**IR playbook (U-005, D5.7).** V1 ships an incident-response playbook covering the **72-hour GDPR breach notification timeline** (GDPR Article 33), audit-log forensic queries, and customer communication template. V2 has no IR playbook. If a breach occurs at 2am on a Friday, V2's team will be writing the GDPR notification in real-time under regulatory pressure with no template. **The IR playbook is GDPR Article 33 operationalized**; without it, NFR-004 ("GDPR compliance") is incomplete.

**STRIDE threat modeling (U-006).** V1 does a STRIDE pass at the start of M2, M3, and M4 — once per new surface. V2 has no equivalent. STRIDE catches design-time vulnerabilities before code is written; OWASP ZAP catches runtime symptoms after the fact. V1 catches early; V2 catches late.

#### V1-only contributions — protocol rigor

**Refresh-family rotation per OAuth BCP (U-007, D2.2).** V1 implements [IETF OAuth 2.0 Security BCP](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics) refresh-token rotation with **replay detection**: a re-used refresh token does not just fail — it revokes the entire family. V2 says "refresh token rotation with replay detection" in passing (D1.4 acceptance) but never specifies family-revocation semantics. V1 has 100ms detection latency as an acceptance criterion; V2 has no such guarantee. This matters: a refresh-token replay attack against V2 might rotate successfully and the attacker keeps a valid session while the legitimate user is logged out, with no detection.

**Permission propagation via denylist (U-008, D4.3).** V1: "admin removes `moderator` from user X → user X's next request with the old token returns 401 **within 1s** (denylist effective)." V2: "the change is immediately reflected in subsequent JWT refreshes." **These are not the same.** V2's user X, whose admin just fired them, retains their permissions for **up to the access-token TTL (15 minutes)** — they can still hit admin endpoints during that window. V1 closes this gap in <1s. For a fired admin who keeps full perms for 15 minutes after termination, V2's design is **a real security gap**, not a hypothetical one.

**Trusted-device cookie (U-009, D3.6).** V1 ships a 30-day "remember this device" flow, signed JWT bound to user agent + IP /24. V2 does not. This is a UX win without a security loss, and it reduces TOTP-fatigue (one of the leading causes of 2FA abandonment).

**Feature flags via unleash (U-010).** V1 explicitly flags OAuth, 2FA, and hard-delete rollouts behind unleash. V2 has no flagging strategy. If 2FA is deployed and causes a 5% login regression, V1 can flag it off in 30 seconds; V2 has to roll back the deploy.

**mTLS API↔Redis (U-011, D1.4).** V1: mTLS between API and Redis from M1 day one. V2: TLS termination at the reverse proxy, internal traffic "over TLS" but no client cert. NFR-006 says "encrypt PII in transit" — Redis carries refresh tokens (PII-equivalent in the auth domain). V1's mTLS makes the Redis traffic genuinely auth'd; V2's TLS does not authenticate the client.

#### Defending V1's wins on contradictions

**X-001 Argon2id over bcrypt.** Per [OWASP Password Storage Cheat Sheet (2025)](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html): "Argon2id is the recommended algorithm." bcrypt is listed as acceptable but with caveats. V1 picks the current recommendation; V2 picks the legacy-acceptable. Source spec says "OWASP compliance" — that means the current OWASP recommendation, not the 2010 one.

**X-005 Audit substrate in M1, not M3.** V2 introduces `audit_events` in M3. **This means M1 and M2 events are captured by event emission but cannot be queried during M1/M2 testing.** If a security bug is found in M2's login during M2 development, V2's team has no audit trail to investigate from. V1's M1 D1.5 ships the table day-one — every M1 event (register, verify, reset) lands in `auth_events` immediately. **This is the difference between "we logged it somewhere" and "we have an investigable record."**

**X-004 Dynamic RBAC with denormalized perms.** V1's `roles × permissions × role_permissions × user_roles` looks heavier than V2's static 4 roles, but V1 denormalizes the perms into the JWT claim at login time — so the per-request enforcement path is **identical** to V2's. The complexity is at admin-time (managing perms), not at request-time. The win: V1 can add a new permission (`audit:export`) without a code deploy; V2 must change the static permission map and redeploy.

**X-003 Bloom-filter access-token revocation.** V1's bloom filter on `jti` enables instant access-token revocation with **<0.1% false-positive rate** on 100k entries. V2 has "no revocation list needed for access tokens." V2's argument ("short TTL + refresh rotation") fails the fired-admin scenario above (U-008): a fired admin's access token remains valid for up to 15 minutes. V1's bloom filter closes that window to <1s. The bloom filter is small (~1.2MB for 1M entries at 0.1% FP), Redis-resident, and has been deployed in production at scale (e.g., Cloudflare's revocation lists). This is not exotic.

**C-009 2FA key separation.** V1 stores the TOTP secret AES-GCM-encrypted with a KMS key **distinct from the column-encryption key**. V2 stores it "encrypted in user_2fa table" with no key-separation. **If V2's database is exfiltrated and the column-encryption key is compromised in the same incident, the attacker has all TOTP secrets immediately** — 2FA provides no protection beyond what the password did. V1's design forces the attacker to compromise a second KMS key. This is the textbook definition of defense-in-depth.

**X-002 30-day refresh + family rotation.** V1's 30-day refresh TTL is longer than V2's 7 days — but V1's *family rotation with replay detection* (U-007) makes the long TTL safe. Any reuse triggers full-family revocation. V2's 7-day TTL without family rotation is more *fragile* than V1's 30-day with family rotation: V2 trades a longer detection window for a shorter exposure window, but V1's instant detection (replay → revoke family) means the exposure window is "until the next legit request, typically minutes." The IETF OAuth BCP supports either; V1's combo is operationally superior because it shifts UX cost (re-login frequency) down without raising security cost.

---

### Weaknesses in Variant 2

**1. bcrypt is the older standard (C-001).** OWASP's 2025 cheat sheet recommends Argon2id. bcrypt cost-12 was the 2015 recommendation. A roadmap promising "OWASP compliance" (NFR-003) that uses the 2015 recommendation is **using a stale interpretation of OWASP**.

**2. NFR-005 (99.9% uptime) is not verifiable without chaos (C-016).** V2 has a 4-hour soak and a Grafana dashboard. Neither tests failure. Production 99.9% means surviving Redis primary failure, API-replica failure, DB read-replica partition, and network blip — *all of which happen in any reasonable production year*. V2's NFR-005 evidence is essentially "we deployed it and watched the dashboard." That is not an availability commitment.

**3. NFR-003 (OWASP compliance) is self-asserted without external pentest (C-015).** OWASP ZAP is a scanner, not a pentest. Auth-specific vulnerabilities — TOTP replay, OAuth state confusion, refresh-token reuse races, recovery-code enumeration — typically pass ZAP and require manual testing. V2's "OWASP compliance" claim cannot be substantiated to a customer who asks "who did the pentest?"

**4. NFR-004 (GDPR compliance) lacks IR playbook (C-017 / U-005 absent).** GDPR Article 33 mandates 72-hour breach notification with specific content. Without a pre-built playbook + template + forensic query inventory, V2's team will improvise under regulatory pressure. **GDPR fines for late notification can reach 2% of global revenue.** The IR playbook is cheap insurance V2 chose not to buy.

**5. Permission propagation gap (U-008 absent in V2).** V2's fired admin retains permissions for up to 15 minutes (one access-token TTL). This is the most concrete, operationally consequential security gap in V2's roadmap. The OWASP A01:2021 (Broken Access Control) category includes "permission elevation that persists past authorization change" — V2 has this by design.

**6. 2FA key co-residence (C-009).** V2 encrypts the TOTP secret with the same key class as the column-encryption key. A single key compromise yields both PII and TOTP secrets. V1 separates them at the KMS-key boundary. This is defense-in-depth that costs nothing and that V2 declined to implement.

**7. No DR runbook (C-017).** "Production deployment runbook" ≠ "DR runbook." A deployment runbook tells you how to deploy; a DR runbook tells you how to recover when production has burned down. V2 has the former and lacks the latter. NFR-005 cannot be met without the latter.

**8. No key-rotation drill (U-003 absent).** Rotation procedures that have never been exercised will fail when first attempted. This is a known SRE failure mode — see [Google's SRE book, Chapter 17](https://sre.google/sre-book/testing-reliability/) on the necessity of exercising recovery procedures.

---

### Concessions

I will not pretend V1 is flawless. The honest weaknesses:

**1. No avatar upload (U-012).** V1's FR-010 deliverables (D4.4) name "name, email, phone" updates but **never specify the avatar path**. V2 is right; V1 has a coverage gap. The mitigation is trivial (`POST /users/me/avatar` to S3 with signed download), but V1's roadmap does not name it as a deliverable.

**2. No explicit reactivation endpoint (U-013).** V1 treats reactivation as implicit (log in during grace → reactivated). V2's explicit `POST /auth/reactivate` is the cleaner design — it separates intent from passive behavior and emits a distinct audit event. V1 should adopt this.

**3. No DB-role-level audit enforcement (U-014).** V1 says "append-only" but specifies the enforcement at the application layer (`AuditLogger` service). V2 enforces it at the database role level (no UPDATE/DELETE grants). **V2's enforcement is strictly stronger** because a compromised application cannot bypass it. V1 should adopt this verbatim.

**4. Shorter soak duration (C-018, 1hr vs 4hr).** V1's 1-hour soak is less likely to surface slow leaks than V2's 4-hour. The argument that "chaos compensates" is partial — chaos tests failure modes; soak tests degradation. They are complementary, not substitutes. V1 should extend to at least 2 hours, ideally match V2's 4.

**5. Dynamic RBAC may be over-engineered (C-004).** The source spec literally says "RBAC" (FR-004). It does not say "fine-grained permission matrix." V2's argument — "the spec requires RBAC, not ABAC" — is closer to the literal source text. V1's dynamic perm denormalization is defensible (extensibility) but **V2 is closer to the source's actual wording**. A faithful roadmap interpretation favors V2 here. V1's argument for the dynamic model rests on "we'll want extensibility later" — which is exactly the speculation the source spec disallows ("scope discipline: build what's asked").

**6. Argon2 m=64MB is heavy for some hardware (C-001 caveat).** V1's Argon2 params (m=64MB, t=3, p=4) calibrate to ~250ms on a c6i.large. On a t3.small or ARM-based small instance, these params can hit 500-800ms — eating into NFR-001's 200ms budget on the registration path. V2's bcrypt cost-12 is more portable across heterogeneous hardware. V1's choice is defensible on production-grade hardware but assumes the deployer is on production-grade hardware.

---

### Shared Assumption Responses

**A-001 (single-region, single-AZ-resilient deployment): ACCEPT.**
NFR-005 says "99.9% uptime" — that is **achievable single-region with proper failover and chaos drills**. A multi-AZ deployment with automated DB and Redis failover, chaos-tested, sits comfortably above 99.9%. Multi-region active-active would target 99.99%+ and is not required by the source spec. V1's M5 chaos pass (D5.2) plus DR runbook (D5.5) operationalizes this assumption. *Accept with the caveat that V1 should explicitly state "single-region multi-AZ" in the Out-of-Scope section.*

**A-002 (GDPR + OWASP only regulatory scope): QUALIFY.**
The source spec names **only** GDPR and OWASP. Both V1 and V2 honor this scope. But this is a planning assumption that **owes an explicit out-of-scope clarification** — a customer asking about HIPAA, PCI-DSS, CCPA, or SOC2 should see "explicitly out of scope; future v2." V1's Out-of-Scope section omits this. *Both variants should add: "No HIPAA, PCI-DSS, CCPA-specific controls, SOC2 evidence collection. These are explicit v2+ scope."*

**A-003 (REST only, no GraphQL/gRPC/native mobile SDK): ACCEPT.**
Source spec explicitly scopes "web auth" and the dependencies (FastAPI/Express implied) are REST-native. V2 surfaces this explicitly ("no native SDK"); V1 leaves it implicit. *Accept; V1 should add an explicit mention to match V2's clarity here.*

**A-004 (single team can absorb 14- or 17-week critical path): QUALIFY.**
V1 explicitly states "one engineer on the critical path; halve with two engineers." V2 is silent on staffing. **V1's estimate is conditional on staffing**, which is honest. But V1's 14 weeks with 1 engineer covering Argon2 calibration + KMS integration + bloom filter + RBAC denormalization + chaos drills + pentest coordination + IR playbook authoring is **optimistic**. The honest disclosure is: 14 weeks is a *budget*, not a *forecast*; a sensible buffer is +25% (≈ 18 weeks). *Qualify: V1's 14-week estimate is a critical-path floor, not a probable delivery date.*

**A-005 (p95 < 200ms measurement boundary): REJECT.**
This is a real ambiguity in both variants. V1's D2.7 says "p95 < 200ms for `/login`, `/refresh`, `/logout` against a seeded 100k-user DB" but **does not pin the measurement point** — is the timer started at TLS handshake completion, at the API ingress, after auth-context construction? V2 has the same gap. Per [Google SRE Workbook, Chapter 5](https://sre.google/workbook/implementing-slos/), an SLI without a defined measurement boundary is not an SLI. *Both variants must define: timer starts at the load balancer ingress (after TLS termination), stops at the response Last-Byte-Sent. The 200ms includes all downstream waits.* This is a valid criticism against both — neither variant is stronger.

---

### Summary of the Advocate's Case

V1 is **operationally more honest** than V2: it commits to drills, runbooks, and external validation rather than self-asserting. V1 is **cryptographically more current**: Argon2id (2025) over bcrypt (2015). V1 closes the **fired-admin permission-propagation gap** that V2 leaves open by design. V1 ships the **audit substrate before any auth event exists**, which is the only design that produces investigable records from day one.

V2 is right about three things V1 should adopt: avatar upload, explicit reactivation endpoint, and DB-role-level audit-table enforcement. V2's longer soak and simpler RBAC are defensible alternatives but not strict wins.

The merged final roadmap should be V1's structure with V2's three concrete additions and an extended soak window. The cryptographic, operational, and protocol choices belong to V1.

---

### Detailed Evidence Catalogue

This section consolidates the evidence base behind each contested position so the comparator can adjudicate without re-reading both source variants.

**On password hashing (X-001, C-001).** OWASP's Password Storage Cheat Sheet (current, 2024-2025) is unambiguous: *"Use Argon2id with a minimum configuration of 19 MiB of memory, an iteration count of 2, and 1 degree of parallelism."* V1's params (m=64MB, t=3, p=4) exceed this floor — appropriate for a forward-looking 2026 deployment with a 5-year operational life. The cheat sheet lists bcrypt as a fallback "If Argon2id is not available" — the *fallback* algorithm, not the recommendation. NIST SP 800-63B Rev 4 (draft 2024) similarly elevates memory-hard functions. A roadmap committed to "OWASP compliance" (NFR-003) for a system shipping in 2026 should use the 2024-2025 recommendation, not the 2015 fallback. V2's choice is not non-compliant, but it is meaningfully behind the curve.

**On refresh-token strategy (X-002, C-002, U-007).** RFC 6749 §10.4 and the OAuth 2.0 Security BCP (draft-ietf-oauth-security-topics, latest revision) jointly specify that refresh-token rotation *with replay detection* is the recommended pattern. The BCP §4.13.2 reads (paraphrased): "The authorization server MUST invalidate the refresh token chain on any indication of replay." V1's design implements this verbatim — replay detected within 100ms, family revoked, user forced to re-authenticate. V2's design rotates the token but does not specify family revocation on reuse. The practical difference: under V2, a stolen-and-then-rotated refresh token continues to work for the attacker until the *original* user happens to use the (now-invalidated) old token, at which point only that user's session breaks; the attacker keeps the active session. Under V1, the legitimate user's reuse of the old token immediately invalidates the entire family, ejecting the attacker. V1's design is BCP-conformant; V2's is partial.

**On audit substrate timing (X-005, S-004).** This is the most consequential structural disagreement. V2 introduces the `audit_events` table in M3 (D3.9) but emits audit events from M1 onwards. The events are written *somewhere* (logs? application memory? a buffer?), but the canonical queryable record does not exist until M3. During M1-M2 development and any incident investigation in that window, V2's team has no audit table to query. V1 ships D1.5 (table + AuditLogger interface) on day one of M1; M1's registration, verification, and reset events all land in the canonical table immediately. **The cost of V1's approach: a table migration and an interface scaffold in M1.** The cost of V2's approach: weeks of M1-M2 events that are not queryable from a canonical source. V1's choice is strictly better for forensic posture.

**On bloom-filter access-token revocation (X-003).** The math: 1M entries at 0.1% false-positive rate requires ~14.4 Mbits ≈ 1.8 MB of Redis memory. 100K entries needs ~144 KB. Lookup is O(k) where k = number of hash functions (typically 7-10) — single-digit microseconds. Cloudflare, Auth0, and Okta all use bloom filters or similar probabilistic structures for revocation lists in production. V2's claim "no revocation list needed for access tokens" is true only if you accept that revocation latency = access-token TTL = 15 minutes. For an auth system supporting RBAC role changes and account deactivation, 15-minute revocation latency is not acceptable for security-sensitive role changes. V1's bloom filter is the minimal additional infrastructure to close this gap.

**On 2FA key separation (C-009).** Defense-in-depth at the key-management layer is a NIST SP 800-57 Part 1 Rev 5 recommendation (§5.3.4): "Cryptographic keys protecting data of different sensitivity classes SHOULD be managed under separate key management policies." TOTP secrets and column-encryption keys protect different classes (the former enables authentication impersonation; the latter exposes data at rest). V1's separation is policy-aligned with NIST 800-57; V2's co-residence is not. The operational cost of separation is one additional KMS key (negligible on AWS KMS at $1/month/key); the security benefit is that a single KMS compromise yields only one class of secrets.

**On chaos engineering (U-001, C-016).** Netflix's "Principles of Chaos Engineering" (chaos-engineering.org) and Google SRE Book §5 both establish that *availability commitments require failure injection testing*. The argument is simple: a system claiming 99.9% must survive the failures that consume the 0.1% — Redis primary failover, network partition, replica lag, etc. If those failures have never been triggered, the 99.9% is a guess. V2's D5.6 ("argue equivalence from architecture: multi-AZ, no single point of failure, automated failover") is the explicit hand-wave: V2 *claims* equivalence without *demonstrating* it. V1's D5.2 demonstrates it.

**On DR runbook with named RTO/RPO (U-002, C-017).** ISO 27031 (Business Continuity for ICT) and NIST SP 800-34 (Contingency Planning) both require **named recovery objectives** for any system with a stated availability SLO. RTO and RPO are the two minimum metrics. NFR-005's 99.9% uptime budget is 8.76 hours/year; if a single DR event consumes more than ~9 hours (RTO > 9 hours), the SLO is automatically blown for that year. **V2 cannot meet NFR-005 without committing to an RTO well below 9 hours**, but V2 names no RTO. V1's RTO 1 hour leaves headroom for multiple incidents per year. The tabletop exercise (V1's D5.5 acceptance criterion) is the validation step — a runbook never exercised is a runbook that will fail.

**On external pentest (U-004, C-015).** PCI-DSS v4 §11.4, ISO 27001 Annex A.12.6.1, and most regulatory frameworks require **independent** security testing. OWASP's WSTG (Web Security Testing Guide) explicitly distinguishes "vulnerability scanning" (automated, what ZAP does) from "penetration testing" (manual, human-driven, what ZAP does not do). Auth-system vulnerabilities that routinely pass automated scans include: race conditions in concurrent token rotation; OAuth state-parameter confusion across providers; TOTP code reuse within tolerance windows; recovery-code enumeration via timing side-channels; refresh-token reuse during family-rotation gaps. Each of these requires a human pentester. V2's "OWASP compliance" claim, supported only by ZAP, is not defensible in a regulated industry or to a security-conscious enterprise customer.

**On IR playbook (U-005).** GDPR Article 33 mandates breach notification to the supervisory authority "without undue delay and, where feasible, not later than 72 hours after having become aware of it." The notification must include: nature of the breach, categories and approximate number of data subjects affected, likely consequences, measures taken. Building this notification from scratch at 2am during an active incident is operationally insane; a pre-built template, populated by pre-queried forensic data, is the responsible posture. V1 ships this (D5.7); V2 does not. The maximum GDPR fine for breach notification failure is the higher of €10M or 2% of global annual revenue — V2's omission of the IR playbook is an uncapped financial liability.

---

### Round 1 Conclusion

The advocacy for Variant 1 rests on three pillars:

1. **Operational evidence over architectural claim.** V1 commits to drills (chaos, DR, key rotation), external validation (pentest), and pre-built incident response (IR playbook). V2 substitutes architectural assertion for empirical verification.

2. **Current cryptographic standards.** Argon2id (2024-2025 OWASP), refresh-family rotation with replay detection (IETF OAuth BCP), 2FA key separation (NIST 800-57), and bloom-filter revocation (industry-standard probabilistic structure). Each of V1's cryptographic choices traces to a current standard; each of V2's traces to an older or partial implementation.

3. **State-mechanics correctness.** Audit substrate available day-one (X-005), permission propagation within 1s rather than 15 minutes (U-008), access-token revocation actually possible (X-003). These are state-machine invariants that V1 establishes and V2 leaves open.

The honest concessions to V2 — avatar upload, explicit reactivation endpoint, DB-role audit enforcement, longer soak, and the closer-to-source RBAC literalism — represent **localized improvements that V1 should adopt**, not structural challenges to V1's framework. The merge target is V1's roadmap structure, V1's security choices, V1's operational commitments, plus V2's three concrete deliverables and an extended soak window.

The shared assumption analysis (A-001 through A-005) identifies one genuine ambiguity (A-005, p95 measurement boundary) that both variants share and that the merge must resolve. The other four assumptions are tractable with explicit out-of-scope statements and honest staffing-buffer disclosure.

V1 is the stronger foundation. V2 contributes specific improvements. The merge should reflect that asymmetry.

---

*End of Round 1 Advocate document.*
