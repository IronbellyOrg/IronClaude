# Round 2 — Rebuttal for V2 (sonnet)

## Rebuttal Summary

V2 remains the stronger base after both rounds. V1's R2 rebuttal largely reaffirms positions from R1 with two notable escalations: reclassifying C-004/X-001 from "mixed" to "V1 stronger" based on V2's A-003 qualifier, and introducing four New Evidence items (NE-1 through NE-4). Of these, NE-1 (p99 invalidated by async audit) is a framing disagreement rather than a factual refutation, and NE-2 (hash-chain schedule cost) is inflated. NE-3 and NE-4 are genuine security gaps I address below. V1's seven conceded points (session cap, WATCH/MULTI/EXEC, pgcrypto, K8s specifics) remain conceded and mergeable. The decisive calculus is unchanged: V2 delivers the same FR scope 4 weeks sooner with materially more shippable operational artifacts, and V1's architectural-invariant strengths (hash-chain audit, GDPR tokenization, risk-register breadth) are additive grafts, not displacements requiring V1's structural skeleton.

---

## Response to V1's Criticisms of V2 (both rounds)

### V1 Round 1 Weaknesses Against V2

> **Criticism (V1 R1, item 1)**: V2 D6.2 synchronous audit write within 500ms + D2.5 per-user session cap + p99 < 200ms are jointly unverified. Write amplification at 10K concurrent sessions has no load-test scenario.
> **V2 Response**: This is a valid modeling gap in both variants. V1's A-003 response in its own R1 is also REJECT, acknowledging the same problem. V2's D6.2 already specifies "async fan-out to a separate read replica for dashboard queries" -- the primary write is synchronous to PG but the fan-out is async. The refinement I flagged in R1 (audit write should be async after response commit) is a D6.2 wording change, not a design rewrite. The primary PG insert for a single audit row (UUID + enum + two FKs + IP + JSONB metadata) is a sub-millisecond operation on a properly provisioned RDS instance. The 500ms budget in D6.2 is extremely conservative. At 10K concurrent sessions, worst-case audit throughput is approximately 30-50 writes/second (not 10K -- most sessions are idle), well within PG's capacity. The joint load-test gap is real but bounded; D6.6 already includes a 10K-session soak test that will surface the issue if it exists.
> **Verdict**: partially conceded (joint load-test gap is real but the severity claim is overstated; both variants share this weakness)

> **Criticism (V1 R1, item 2)**: V2 D6.1 audit table is not tamper-evident. "Append-only" is an application-level convention; a DBA with DELETE privilege defeats it.
> **V2 Response**: Conceded in R1 (Concession #1). V2 should adopt V1's hash-chain mechanism.
> **Verdict**: conceded (already conceded in R1)

> **Criticism (V1 R1, item 3)**: V2 R-007 mitigates JWT rotation with "multiple active signing keys" but never names JWKS or kid. Without a publication endpoint, downstream services can't validate new-key tokens without redeploy.
> **V2 Response**: V2 R-007 says "new tokens signed with new key, old tokens validated against key list." The mechanism is described functionally even if the protocol name (JWKS) is omitted. V2's D7.3 runbook includes "token rotation failure" as an incident scenario, and D2.1 specifies 15-min access-token TTL bounding blast radius. This is a specificity gap, not an architectural gap. The merge should adopt V1's explicit `/.well-known/jwks.json` + `kid` naming. However, I note V1's claim that "downstream services can't validate" is overstated: the key list is server-side configuration, and the 15-min TTL means even manual key rotation converges within one token lifetime. JWKS is the correct production mechanism, but its omission does not make V2's approach non-functional.
> **Verdict**: partially conceded (specificity gap conceded; claim of non-functionality is overstated)

> **Criticism (V1 R1, item 4)**: V2 D5.6 hard delete "removes PII, retains anonymized audit records" but D6.1 indexes actor_user_id. De-anonymization via correlation is unaddressed.
> **V2 Response**: Conceded in R1 (Concession #2). V2 should adopt V1's tokenized user_id approach.
> **Verdict**: conceded (already conceded in R1)

> **Criticism (V1 R1, item 5)**: V2 D1.4 password policy (12-char, mixed case, digit, symbol) is the NIST-deprecated composition-rule pattern.
> **V2 Response**: V1 is correct on the NIST guidance. Composition rules are deprecated in SP 800-63B section 5.1.1.2 in favor of breached-password checks and length-only minimums. This is a genuine weakness in V2's password policy. However, V2's D1.4 also specifies Argon2id hashing, which is the modern hashing standard. The password policy should be updated to remove composition rules and adopt zxcvbn + HIBP k-anonymity checks, consistent with V1's approach. This is a deliverable-level wording fix in D1.4, not a structural change to V2's milestone plan.
> **Verdict**: conceded (password policy should be updated; does not change milestone structure)

> **Criticism (V1 R1, item 6)**: V2 D1.3 hard-codes Python 3.12-slim without an ADR. This is process debt.
> **V2 Response**: Defended in R1 (Strength 2). V1's R2 rebuttal reiterates that the ADR is "correct sequencing." I maintain that V1's approach creates a real delay: M1 entry criteria require a merged ADR, which means M1 cannot start until the ADR is written, reviewed, and merged. In practice this is a 2-5 day delay on Week 1. V2's approach makes the call and proceeds; if the team has a strong Python preference (as most startups using SendGrid + PostgreSQL do), the ADR is documentation-after-fact, not a decision gate. The merged plan should include the ADR as an M1 deliverable while allowing the implementation to proceed in parallel -- a "decision and document" model rather than V1's "decide then act" model.
> **Verdict**: defended (V2's approach unblocks faster; ADR should be added as documentation, not a gate)

> **Criticism (V1 R1, item 7)**: V2 M7 (2 weeks) is implausible for production hardening. Must contain edge-case suite, Prometheus + Grafana, runbooks, K8s manifests, launch readiness, rollback rehearsal.
> **V2 Response**: This is the strongest criticism V1 raises against V2. I partially concede: pen-test vendor engagement (V1 D7.5) is a multi-week activity that V2's 2-week M7 does not realistically contain. However, V2's D6.5 already includes OWASP ZAP security scanning in M6 (Weeks 14-16), not M7. The automated scan is in the compliance milestone, not deferred to the launch milestone. V2's M7 then focuses on edge-case validation, monitoring configuration, runbooks, deployment manifests, and the launch checklist -- which is 2 weeks of operational work, not 5. The honest trade-off: V2 replaces a third-party pen-test with an automated OWASP ZAP scan. Some organizations accept this trade-off for initial launch (ZAP baseline + active scan catches the same categories V1's pen-test would flag, minus manual logic-flaw analysis). If the organization requires third-party pen-test, V2's M7 would need to grow to 3-4 weeks, narrowing the gap to 1-2 weeks, not 4. This does not change my recommendation that V2 is the base, because the pen-test scope difference is an "add to M7" change, not a structural rewrite.
> **Verdict**: partially conceded (pen-test omission is real; M7 is tighter than ideal but not "implausible" for non-pen-test scope; ZAP scan in M6 partially compensates)

> **Criticism (V1 R1, item 8)**: V2 R-005 says "accept login with direct PostgreSQL token validation (slower, but functional)" on Redis loss, but D4.4 rate limiting and D4.5 lockout both rely on Redis. Graceful degradation cannot exist without redesigning rate-limit/lockout to use PG.
> **V2 Response**: This is a valid internal consistency gap. V2's R-005 graceful-degradation path does not account for rate-limit and lockout dependencies on Redis. However, this is a runbook-level detail, not a milestone-structure issue. The fix is straightforward: during Redis outage, rate-limiting degrades to a per-instance in-memory sliding window (less accurate but functional), and lockout state falls back to a PG-based counter. V2's D7.3 runbook should document this fallback path. This does not change the milestone plan or the base selection.
> **Verdict**: partially conceded (consistency gap is real but bounded to runbook wording; not architectural)

> **Criticism (V1 R1, item 9)**: V2 D4.4 rate-limit key is `ratelimit:{user_id}:{endpoint_group}` -- keyed on user_id, which does not exist for /auth/login (the highest-value rate-limit target). V1 D3.3 uses (IP, email) composite, which is correct pre-auth scope.
> **V2 Response**: This is a genuine correctness gap. V2's D4.4 rate-limiting key is wrong for unauthenticated endpoints. The pre-auth rate limit must use a composite key based on IP and optionally email (for login) or IP alone (for registration). V2's D4.5 brute-force lockout already uses a different key structure (lockout counter in Redis keyed on email/account), which suggests the rate-limit key was an oversight rather than a design error. The fix: D4.4 should specify `ratelimit:{ip}:{endpoint_group}` for unauthenticated endpoints and `ratelimit:{user_id}:{endpoint_group}` for authenticated ones. This is a deliverable-level correction, not a structural change.
> **Verdict**: conceded (rate-limit key is incorrect for pre-auth; straightforward fix)

> **Criticism (V1 R1, item 10)**: V2 D3.3 OAuth account linking auto-links on email match without re-verification. Account-takeover vector: attacker registers Google account with victim's email, auto-link gifts them the existing account.
> **V2 Response**: This is the most serious security criticism V1 raises against V2, and V1 is correct that it was unrebutted in my R1 brief. The auto-link-on-email-match pattern is indeed vulnerable per OWASP ASVS V2.10.3. However, I note two mitigating factors within V2's existing design: (a) V2 D3.3 says "if OAuth email matches existing account, link provider to that account" -- this is a UX convenience that should require explicit user confirmation (as V1's D4.3 does), and (b) the attack requires the attacker to have a verified Google/GitHub account using the victim's email, which Google and GitHub both prevent through their own email verification. The practical exploitability is lower than the theoretical attack class suggests, but the defense-in-depth principle requires explicit confirmation regardless. The fix: D3.3 should be updated to require the existing account holder to confirm the link via email before it is established. This is a one-paragraph deliverable change, not a structural redesign.
> **Verdict**: conceded (auto-link is a security regression; explicit confirmation is the correct fix)

> **Criticism (V1 R1, item 11)**: V2 M5 lumps 2FA, password reset, profile, GDPR, account deactivation into 3 weeks (8 deliverables D5.1-D5.8). V1 splits into M5 (4w) and M6 (3w).
> **V2 Response**: V2's M5 delivers 8 items in 3 weeks, which is aggressive. However, several of these deliverables are structurally simpler than V1's analogous items: V2's D5.1-D5.2 (password reset) is a standard email-token flow (the session/token infrastructure already exists from M2); D5.5 (profile CRUD) is straightforward; D5.6-D5.7 (deactivation + GDPR) share the same soft-delete + hard-delete path. The two most complex items are D5.3-D5.4 (2FA enrollment + verification), which map to V1's D5.3-D5.5 in a 4-week M5. The delta is real: V1 gives 2FA 4 weeks, V2 gives it 3 weeks alongside 6 other deliverables. If M5 proves too compressed, the schedule risk is bounded because M5 is not on the critical path for any M6+ dependency -- M6 (audit + dashboard) can begin with partial M5 completion. This is a schedule-tightness risk, not an architectural deficiency.
> **Verdict**: partially conceded (M5 is tight; schedule risk is real but bounded by non-critical-path position)

> **Criticism (V1 R1, item 12)**: V2 only has 8 risks vs V1's 12. Missing explicit entries for several threat categories.
> **V2 Response**: Conceded in R1 (Concession #3). V2 should adopt the missing risk entries.
> **Verdict**: conceded (already conceded in R1)

### V1 Round 2 Responses to V2's Criticisms

> **Criticism (V1 R2, response to V2 R1 item 1)**: V1 partially concedes deployment topology vagueness but defends the "failure-mode contract" (multi-AZ, RDS multi-AZ, Redis replication group, chaos test <30s RTO) as more architecturally honest than V2's toolchain lock-in.
> **V2 Response**: V1's failure-mode contract is valuable but incomplete without implementation specifics. "Multi-AZ" is a deployment topology description, not a runbook. A team starting from zero cannot execute "multi-AZ" without answering: what orchestrator? what connection pooler? what Redis HA mechanism? V2 answers all three. V1's R2 concedes U-007 as mergeable, and I accept the conditional (ADR-dependent). The remaining disagreement is framing: V1 calls this "architectural honesty," I call it "incomplete specification." Both are partially correct. The merged plan should use V1's failure-mode language (the contract) backed by V2's toolchain specifics (the implementation).
> **Verdict**: partially conceded (V1's failure-mode contract is valuable; V2's toolchain is necessary; both should be in merged plan)

> **Criticism (V1 R2, response to V2 R1 item 3)**: V1 defends tech-stack deferral as "correct sequencing" via ADR. Claims V2 hard-codes Python without ADR as "process debt."
> **V2 Response**: I addressed this above (V1 R1 item 6). V1's framing of "decide then act" versus V2's "decide and document" is a process philosophy difference, not a correctness difference. V1's ADR-as-entry-criterion approach adds 2-5 days to M1 start. In a 22-week project, 2-5 days is not material. In an 18-week project, it is proportionally more significant. Neither approach is wrong; V2's is faster. The merged plan should include an ADR as an M1 deliverable written concurrently with D1.1-D1.7, not as a gate before them.
> **Verdict**: defended (disagreement is process philosophy, not correctness; V2's approach is faster)

> **Criticism (V1 R2, response to V2 R1 item 5)**: V1 partially concedes latency percentile, reframe as endpoint-coverage trade-off. V1 covers 4 endpoints at p95; V2 covers 3 at p99. Claims V2's p99 is "aspirational, not held by the variant as written" due to A-003 conflict.
> **V2 Response**: V1's endpoint-coverage framing is fair and I accept it: V2's p99 covers `/auth/login`, `/auth/refresh`, `/auth/profile` (3 endpoints in D6.6), while V1's p95 covers `/login`, `/register`, `/refresh`, `/oauth/*` (4 endpoints in Goals G1). The merged plan should specify p99 on critical-path endpoints and p95 on the broader surface. However, V1's claim that V2's p99 is "aspirational" mischaracterizes my R1 A-003 qualifier. I said "audit write should be async after response commit, not blocking the client response" -- this is a refinement to D6.2's wording, not a design change that breaks p99. A single audit-row INSERT to PG takes sub-millisecond; the 500ms budget is for the full fan-out pipeline, not the client-blocking portion. The p99 target is achievable as written if the audit write is synchronous to PG and the async fan-out happens after response commit. This is how most production audit systems work.
> **Verdict**: partially conceded (endpoint coverage gap is real; p99 achievability claim is defended, not conceded)

> **Criticism (V1 R2, response to V2 R1 item 7)**: V1 firmly defends 22-week schedule, arguing V2's 4-week savings omits pen-test (2-3 weeks vendor + remediation), hash-chain engineering, and bootstrap script. Claims "schedule inflation without functional value" is mis-stated.
> **V2 Response**: I addressed the pen-test point above (V1 R1 item 7): V2 includes OWASP ZAP scanning in M6 rather than deferring it to M7. The pen-test vs. automated scan trade-off is real but narrower than V1 implies. On the hash-chain point: V1's R2 NE-2 claims adding hash-chain to V2 requires 1-2 sprints. This is inflated. The hash-chain is: (a) add a `prev_hash` column to `audit_events` (schema migration), (b) canonical JSON serialization of the row (a `json.dumps` with sorted keys), (c) SHA-256 of prior row's canonical payload, (d) S3 export with object-lock (a daily cron job). This is 3-5 days of engineering work for an experienced team, not 1-2 sprints (10-20 days). V2's schedule can absorb this within M6's existing 3-week window without extension, particularly since D6.1 and D6.2 already specify the audit table and event emission -- only the chain mechanism is additive. On the bootstrap script: V2 can adopt this as a D1.7 sub-deliverable in M1 (a 1-day script). These are additive deliverables within existing milestones, not schedule-busting additions.
> **Verdict**: defended (schedule savings are real; hash-chain cost is inflated; pen-test vs. ZAP is a trade-off, not an omission)

---

## Response to V1's New Evidence

**NE-1 (V2's A-003 concession invalidates p99)**: V1 claims my A-003 QUALIFY response concedes that synchronous audit writes "cannot coexist" with p99 < 200ms. This misreads my response. I said the audit write *should be* async after response commit -- a design refinement to D6.2 that moves the fan-out off the client-blocking path. The primary PG insert (sub-millisecond) remains synchronous. The 500ms budget in D6.2 covers the full pipeline including async fan-out; the client sees only the PG insert latency. This refinement is compatible with p99 < 200ms. V1's claim that the p99 commitment is "aspirational, not held by the variant as written" is a framing choice, not a factual conclusion. V1's own A-003 response is REJECT, acknowledging the same modeling gap in V1's p95 plan. Neither variant has jointly load-tested audit-write amplification at 10K sessions; both share this weakness.

**NE-2 (V2 hash-chain concession contradicted by schedule)**: V1 claims adding hash-chain to V2 is "1-2 sprints of work" that V2's 18-week schedule "does not contain a slot for." This cost estimate is inflated. The hash-chain mechanism consists of: (a) schema migration adding `prev_hash` column (1 day), (b) canonical serialization function (0.5 day), (c) write-path hook computing SHA-256 of prior row (1 day), (d) daily S3 export cron (1 day), (e) replay verification tool (1 day). Total: approximately 4.5 engineering days, not 10-20. This fits within M6's 3-week window alongside existing D6.1-D6.8 deliverables. V1's estimate assumes building a full audit-log infrastructure from scratch; V2 already has the table, event emission, and read-replica fan-out -- only the chain mechanism is additive.

**NE-3 (V2 D3.3 OAuth auto-link takeover vector)**: Un-rebutted in R1, and I concede it here. The auto-link-on-email-match pattern is a security regression. D3.3 should require explicit user confirmation before linking an OAuth provider to an existing account. I note that the practical exploitability is bounded by Google/GitHub's own email verification (an attacker cannot create a verified Google account with a victim's email without controlling that email), but defense-in-depth requires explicit confirmation regardless. This is a one-paragraph deliverable fix, not a structural change.

**NE-4 (V2 D4.4 rate-limit key gap)**: Un-rebutted in R1, and I concede it here. The rate-limit key `ratelimit:{user_id}:{endpoint_group}` is incorrect for pre-authenticated endpoints. D4.4 should use `ratelimit:{ip}:{endpoint_group}` for unauthenticated endpoints and `ratelimit:{user_id}:{endpoint_group}` for authenticated ones. This is a deliverable-level correction.

---

## Updated Assessment of V1's Strengths

### V1-S1 (Hash-chain audit log, U-001/C-006)

R1 view: Conceded as genuinely valuable compliance control; V2 should adopt.
R2 view: Unchanged. V1's hash-chain is architecturally superior. My R1 concession stands. The only new element is V1's NE-2 claim that adopting hash-chain breaks V2's schedule, which I have rebutted above (estimated 4.5 days, not 1-2 sprints). The concession on the mechanism does not change the base-selection argument: hash-chain is an additive graft, not a structural dependency.

### V1-S2 (GDPR tokenization, U-004/C-013)

R1 view: Conceded; V2 should adopt V1's tokenized user_id approach.
R2 view: Unchanged. This is a ~2-day schema fix within V2's existing M5/M6, not a base-displacing architectural concern.

### V1-S3 (Risk-register breadth, 12 vs 8)

R1 view: Conceded; V2 should adopt missing risk entries.
R2 view: Unchanged. Risk-register entries are documentation additions, not structural changes.

### V1-S4 (Per-milestone edge cases, S-002)

R1 view: Conceded V1's inline blocks are superior for implementation guidance.
R2 view: Unchanged. V2 should adopt V1's per-milestone edge-case blocks while retaining D7.1 as a centralized regression gate.

### V1-S5 (M1 as pure scaffolding, X-004)

R1 view: V2's front-loading delivers value sooner.
R2 view after R1+R2: V1's argument -- that shipping auth endpoints before observability and ZAP baseline is a security risk -- has merit. However, V2's M1 (3 weeks) includes the same infrastructure scaffolding (Docker Compose, Redis, PG schema, health checks) as V1's M1 (2 weeks), plus registration/login/verify. The observability baseline (structured logging) is part of V2's M1 service skeleton. The ZAP scan runs in M6 regardless. The incremental risk of having auth endpoints in staging 2 weeks earlier (without ZAP) is bounded by staging network isolation. I maintain V2's front-loading is a net positive for stakeholder confidence.

### V1-S6 (Pen-test engagement, D7.5)

R1 view: V2's 2-week M7 does not contain third-party pen-test.
R2 view: Conceded that V2 omits third-party pen-test. V2's OWASP ZAP scan (D6.5) covers the automated side. Organizations that require manual pen-test should extend V2's M7 by 2-3 weeks (bringing total to 20-21 weeks, still 1-2 weeks shorter than V1). This is a product decision, not a structural deficiency.

---

## Final Concessions

After both rounds, V2 concedes (in order of severity):

1. **C-006 / U-001 (audit tamper-evidence)**: V2 should adopt V1's hash-chain + S3 object-lock mechanism. Estimated 4.5 engineering days within M6.

2. **C-013 / U-004 (GDPR erasure precision)**: V2 should adopt V1's tokenized user_id approach. Estimated 2 days within M5/M6.

3. **C-007 (password policy)**: V2's 12-char composition rules are NIST-deprecated. Should be replaced with zxcvbn + HIBP k-anonymity checks.

4. **V1 R1 item 10 / NE-3 (OAuth auto-link)**: D3.3 auto-link is a security regression. Must require explicit user confirmation.

5. **V1 R1 item 9 / NE-4 (rate-limit key)**: D4.4 rate-limit key is incorrect for pre-auth endpoints. Must use IP-based key for unauthenticated routes.

6. **C-008 / U-002 (JWT rotation specificity)**: V2 should adopt V1's explicit JWKS + kid naming for key rotation.

7. **Risk-register breadth**: V2 should adopt V1's R-008 (recovery-code abuse), R-009 (audit tampering), R-010 (GDPR conflict), R-011 (offline refresh theft), R-012 (TOCTOU role revocation).

8. **S-002 (edge-case placement)**: V2 should add per-milestone edge-case blocks alongside D7.1.

9. **U-005 (bootstrap admin)**: V2 should add a bootstrap admin script as a sub-deliverable in M1.

10. **M7 pen-test (partial)**: V2's M7 omits third-party pen-test. Organizations requiring this should extend M7 by 2-3 weeks.

11. **M5 tightness (partial)**: M5's 3-week window for 8 deliverables is aggressive. Schedule risk is real but bounded.

None of these concessions change my recommendation that V2 should be the base. All are additive deliverable-level changes within V2's existing milestone structure. None require restructuring milestones, reordering dependencies, or altering the 18-week timeline (except the optional pen-test extension).

---

## New Evidence Introduced

**NE-V2-1: V2's D6.5 OWASP ZAP scan runs in M6 (Weeks 14-16), not M7.** V1's R1 weakness #7 and R2 rebuttal both frame V2 as deferring security scanning to a 2-week M7. In fact, V2 runs the OWASP ZAP scan as D6.5 in M6 alongside the load test (D6.6), monitoring (D6.7), and PII verification (D6.8). The M7 milestone is for edge cases, runbooks, deployment manifests, and launch checklist -- operational work, not security scanning. This means V2 has 3 weeks of compliance validation (M6) plus 2 weeks of hardening (M7) = 5 weeks total for the security+compliance+operational phase, compared to V1's M6 (3w) + M7 (5w) = 8 weeks. The gap is 3 weeks, not the 3-week M7 compression V1 implies.

**NE-V2-2: V2's milestone sequencing produces earlier risk reduction.** V2 ships core auth (registration, login, JWT) in M1 (Week 3), rate limiting and lockout in M4 (Week 10), and security headers in M4. V1 ships core auth in M2 (Week 5), rate limiting in M3 (Week 7), and security headers in M7 (Week 18+). V2's ordering means the highest-risk surface (unauthenticated login) has brute-force protection and security headers 8 weeks earlier than V1. V1's "M1 as pure scaffolding" trades earlier risk reduction for a cleaner infrastructure foundation -- a valid trade, but not a clear win.

**NE-V2-3: V1's own A-003 is REJECT, sharing V2's audit-write-amplification weakness.** V1's R1 Shared Assumptions table marks A-003 as REJECT: "Synchronous audit writes at 10K concurrent + V2's p99 < 200ms + write amplification has no joint load test in either variant." V1 acknowledges the same weakness for its own p95 commitment. The audit-write-amplification concern is shared, not V2-specific.

---

## Updated Per-Point Verdicts

| Diff Point ID | R1 verdict | R2 verdict | R2 confidence | Change rationale |
|---|---|---|---|---|
| C-004 / X-001 | V2 stronger (p99 stricter) | Mixed | 0.65 (was 0.90) | V1's endpoint-coverage argument (4 endpoints p95 vs 3 endpoints p99) is fair; merged plan should specify both |
| C-007 | V1 stronger (HIBP superior) | V1 stronger | 0.88 (unchanged) | Password policy concession confirmed; no change in verdict |
| C-011 | Tied (different tradeoffs) | Tied | 0.65 (unchanged) | V1's family-tracking vs V2's revoke-all remain different tradeoffs; both should merge |
| C-010 | V2 stronger (shippable runbook) | Mixed | 0.75 (was 0.90) | V1's R2 defense of failure-mode contract has merit; V2's toolchain is necessary but not sufficient without the contract language |
| V2 D3.3 OAuth auto-link | (not rated in R1) | V1 stronger | 0.85 | New: conceded security regression |
| V2 D4.4 rate-limit key | (not rated in R1) | V1 stronger | 0.80 | New: conceded correctness gap |
| C-001 / X-003 | V2 stronger (4-week savings) | V2 stronger | 0.82 (was 0.92) | Confidence reduced by pen-test omission and M5 tightness; savings remain real |
| X-004 | V2 stronger (early value) | V2 stronger | 0.72 (was 0.82) | V1's security-posture argument has some merit; front-loading value still wins on balance |

No change after R2: 31 (S-001, S-002, S-003, C-002, C-003, C-005, C-006, C-008, C-009, C-012, C-013, X-002, X-005, U-001, U-002, U-003, U-004, U-005, U-006, U-007, U-008, U-009, A-001, A-002, A-003, A-004, A-005, A-006, A-007, A-008, V2 R-005 Redis inconsistency).

---

## Final Recommendation

V2 should remain the base, with V1's contributions grafted in as additive layers.

**Reasoning**: After two rounds, V2 has conceded 11 points to V1 -- primarily in compliance depth (hash-chain audit, GDPR tokenization), security specifics (JWKS naming, OAuth confirmation, rate-limit key), and risk-register breadth. All 11 concessions are deliverable-level additions within V2's existing 7-milestone structure. None require restructuring the dependency graph, reordering milestones, or extending the 18-week timeline (with the optional pen-test exception).

V2's remaining structural advantages over V1 are:

- **4-week schedule advantage** (confidence reduced from 0.92 to 0.82 but still positive), with the gap narrowing to 1-2 weeks if pen-test is added
- **Shippable deployment artifacts** (K8s manifests, PgBouncer config, Redis Sentinel topology) that V1 does not provide
- **Concurrency primitives** (WATCH/MULTI/EXEC, per-user session cap) that V1 itself concedes
- **Earlier risk reduction** through front-loading core auth into M1 and security controls into M4

V1's advantages are real and should be merged:

- Hash-chain audit log (4.5 days of engineering)
- GDPR user_id tokenization (2 days)
- JWKS + kid explicit naming (1 day)
- Per-milestone edge-case blocks (documentation)
- Risk-register entries (documentation)
- Bootstrap admin script (1 day)
- Pen-test engagement (optional 2-3 week extension)

The merged plan should use V2's milestone structure, dependency graph, and timeline as the skeleton, and graft V1's compliance controls, risk entries, and security specificity on top. This preserves V2's schedule efficiency and operational shippability while incorporating V1's superior cryptographic-invariant design.
