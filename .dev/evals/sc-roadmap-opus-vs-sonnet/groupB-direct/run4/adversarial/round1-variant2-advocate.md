# Round 1 — Variant 2 (Sonnet) Advocate Statement

## 1. Position Summary

Variant 2 produces a leaner, more realistic roadmap that ships in 9 weeks at 16 EW — a 3x efficiency gain over Variant 1's 48 EW / 11-week plan — without sacrificing any FR, NFR, or compliance gate. Its four-workstream taxonomy is simpler to coordinate, its micro-benchmark gates (JwtService <5ms, Redis <10ms) decompose the 200ms p95 budget into actionable sub-component targets, and it is the only variant that connects the roadmap to a measurable PRD success metric via R-006 (registration conversion < 60% contingency). Variant 2 ships faster with less budget risk while hitting every exit criterion the TDD requires.

## 2. Steelman of Variant 1 (Opus)

Before critiquing, I acknowledge what Variant 1 genuinely gets right:

1. **Dedicated M0 foundation milestone (U-001).** By front-loading infrastructure provisioning (PostgreSQL, Redis, RSA keys, SendGrid, OpenAPI contracts) into a 2-week M0, Variant 1 guarantees that M1 developers never wait on environment setup. This is a real coordination risk that Variant 2 folds into WS-C W1-W2 without a formal gate.

2. **Inter-workstream handoff matrix H1-H10 (U-002).** Ten explicit handoff points with artifact descriptions (e.g., H5: "AuthToken envelope from WS-2 to WS-3 at M2 end") eliminate ambiguity about who delivers what, when. Variant 2 has handoff prose but nothing this precise.

3. **Quantitative timing-variance acceptance tests AT-001..AT-016 (U-004).** Variant 1's CI-enforced +-15ms (login) / +-10ms (reset) variance budgets are the strongest anti-enumeration guarantee in either document. Variant 2 states the invariant ("no enumeration via timing differences" at M4) but provides no quantitative bound, making it harder to automate enforcement.

4. **Broader risk register (R-001..R-008).** Variant 1's R-008 (key rotation breaks in-flight tokens) and R-007 (M3+M4 simultaneous slip) surface risks that Variant 2 does not model. The 24-hour overlap window for key rotation is a genuinely useful operational detail.

5. **Component build-order table (U-003).** The 7-step internal dependency ordering (PasswordHasher -> UserRepo -> AuthService -> JwtService -> TokenManager -> re-wire -> AuthProvider) gives implementers a clear construction sequence, reducing integration surprises.

6. **YAML frontmatter and machine-readable structure.** Variant 1's structured metadata (id, title, target_release, variant, status) enables automated pipeline tracking that Variant 2's plain Markdown header cannot.

## 3. Strengths Claimed (with evidence)

1. **Leaner 16 EW estimate is more realistic for the stated team size.** Variant 2 scopes M1 at 4 EW (2 engineers x 2 weeks, M1 field table), M2 at 4 EW, M3 at 3 EW, M4 at 3 EW, M5 at 2 EW. Variant 1's M1 alone is 10 EW for nearly identical scope (login, registration, lockout, password policy, audit log). The diff analysis confirms this at X-008: "4 EW for nearly identical scope — 2.5x understatement at same scope" — but the counter-argument is that 10 EW for one milestone represents over-staffing, not that 4 EW is under-staffed. Two backend engineers for two weeks is a natural sprint cadence. Variant 1's 48 EW implies a 6-7 person full-time team for 11 weeks, which the PRD and TDD never state as available capacity.

2. **R-006 conversion-rate risk with A/B test contingency (U-008).** Variant 2's R-006 explicitly models the risk that registration conversion falls below 60% (the PRD success metric at S10.1) and prescribes an A/B test contingency: "Simplify registration to email + password only (remove displayName); add social proof or incentive messaging" (R-006 Contingency). This is the only risk in either variant that directly ties a roadmap decision to a measurable PRD outcome. Variant 1's risk register focuses on technical risks but never addresses whether users will actually use the system.

3. **Explicit micro-benchmark gates: JwtService <5ms, Redis <10ms (U-010).** Variant 2's performance gate table (S8.3) decomposes the 200ms p95 NFR into sub-component budgets. If JwtService sign/verify is <5ms and Redis ops are <10ms, the remaining budget (~185ms) is available for bcrypt hashing (~300-400ms at cost 12) and PostgreSQL I/O. This makes the 200ms target auditable at the component level rather than only at the endpoint level. Variant 1 has no sub-component budgets.

4. **Cleaner 4-workstream taxonomy avoids over-engineering.** Variant 2 merges Security+Release into WS-D and Observability+Compliance into WS-C, producing 4 workstreams (WS-A through WS-D) versus Variant 1's 5 (WS-1 through WS-5). For a service with 6 endpoints and 4 core components, 4 workstreams is the right granularity. Variant 1's separate WS-4 (Security) and WS-5 (SRE) create two single-contributor streams that may not justify standalone tracking overhead.

5. **Tighter rollout cadence reduces time-to-value.** Variant 2's Alpha 1w + Beta 1w + GA stabilization (S7.1-7.3) reaches 100% traffic 2 weeks faster than Variant 1's Alpha 1w + Beta 2w schedule. The Beta 10% phase in Variant 2 is 1 week (2026-06-02 through 2026-06-08) versus Variant 1's 2 weeks (2026-06-03 through 2026-06-09). If exit criteria are quantitative (p95 < 200ms, error rate < 0.1%), one week of production data at 10% traffic provides sufficient statistical confidence to proceed.

6. **Lockout cooldown semantics are more security-conservative.** Variant 2's 30-minute cooldown (S9 OQ #3) versus Variant 1's 15-minute auto-unlock window means an attacker must wait twice as long before retrying a brute-force campaign. Combined with the password-reset unlock path, this gives defenders more response time without locking legitimate users out indefinitely.

## 4. Weaknesses Identified in Variant 1 (with evidence)

1. **48 EW total (S1, C-001) is likely over-scoped and may delay ship.** Variant 1 allocates 48 engineer-weeks across 11 calendar weeks, requiring an average of 4.4 engineers continuously occupied. M1 alone claims 10 EW (M1 effort field). The TDD does not specify team size, so this estimate assumes headcount that may not exist. If the actual team is 2-3 engineers, Variant 1's timeline is aspirational rather than executable. Variant 2's 16 EW fits a 2-engineer team over 9 weeks.

2. **Dedicated M0 at 8 EW may double-count infrastructure already in TDD dependencies.** Variant 1's M0 deliverables include PostgreSQL provisioning, Redis provisioning, and RSA key generation (S2.M0 deliverables 1-3). However, the TDD S18 dependency list already accounts for these as prerequisites. If the platform team provisions infrastructure as part of their standard sprint work (not auth-team scope), then 8 EW for M0 includes effort that does not belong on the auth roadmap.

3. **85% line coverage targets (C-003) exceed the TDD baseline without justification.** Variant 1 sets M1/M2/M3 at >=85% lines, >=80% branches (S8.1 coverage table), while the TDD S15.1 target is 80%. The "headroom" rationale (M1 exit criterion note: "exceeds by 5pp to leave headroom") is reasonable in theory but adds testing effort that may not be necessary for a v1.0. If the TDD-gate is 80%, shipping at 80% is compliant.

4. **Component build-order table (U-003) may over-constrain implementation.** The 7-step ordered build sequence (S5 Internal Component Dependencies) assumes PasswordHasher must be fully complete before AuthService starts. In practice, AuthService can be developed with a PasswordHasher interface and a simple stub, then wired when the real implementation lands. Prescribing a fixed order removes developer flexibility without reducing risk.

5. **Quarterly RS256 rotation runbook (U-005) is premature for v1.0.** Variant 1 schedules the rotation runbook as an M2 deliverable (S2.M2 deliverable 10) and R-008 models rotation-breakage risk. Variant 2 defers to a "documented procedure" at S5.2 and S6 SEC-2. For v1.0, the key rotation procedure needs to exist as a document, but the quarterly cadence and 24-hour overlap window are operational details better finalized post-GA when actual key-management infrastructure is in place.

6. **16 acceptance tests AT-001..AT-016 (U-004) risk brittleness if variance margins drift.** The +-15ms login and +-10ms reset variance bounds (S2.M1 exit criterion 4, S2.M3 exit criterion 2) are measured in CI. On shared CI runners with variable load, timing-based tests are notoriously flaky. If CI infrastructure changes (e.g., migration to ARM runners, different container resource limits), these tests may fail non-deterministically, blocking merges without actual security regressions.

7. **M1 at 10 EW — potential padding rather than precision.** Variant 1's M1 scope (login, registration, PasswordHasher, lockout, audit log, password policy) is substantial but bounded. At 10 EW, this implies either very conservative estimation or scope that exceeds what the deliverables list describes. If the deliverables are accurate, 10 EW represents 2.5x Variant 2's estimate for the same work, which is a significant efficiency gap that warrants justification.

## 5. Concessions (genuine weaknesses in own variant)

1. **No dedicated foundation milestone creates infrastructure setup risk.** Variant 2 folds PostgreSQL and Redis provisioning into WS-C W1-W2 (S3 WS-C sequencing table) without a formal exit gate. If platform-team provisioning slips past W2, M1 developers have no database to test against. Variant 1's M0 gate (S2.M0 exit criterion 1: "make migrate applies schemas with zero errors") forces this to be proven before any feature code lands.

2. **16 EW total may understate effort if any FR encounters unexpected complexity.** Variant 2's estimates are aggressive: M3 at 3 EW for password reset + audit logging + GDPR consent + SendGrid integration is tight. If SendGrid sandbox configuration takes longer than expected, or if the audit-log schema requires revision, there is no buffer. Variant 1's larger estimates absorb this risk naturally.

3. **No inter-workstream handoff matrix creates coordination ambiguity.** Variant 2's handoff descriptions (S3 WS-A/WS-B handoffs) are prose-based ("W4 -> WS-B: Token refresh contract finalized") without the structured artifact tracking that Variant 1's H1-H10 table provides. In a multi-team setting, this increases the chance that a handoff is misinterpreted or missed entirely.

4. **Quantitative timing-variance acceptance criteria are weaker.** Variant 2 states "no enumeration via timing differences" as a milestone-4 exit criterion (S4 exit criteria) and Appendix A invariant table, but does not specify a numeric bound like Variant 1's +-15ms. This makes the criterion subjective and harder to enforce in CI.

5. **Missing component build-order may cause integration churn.** Variant 2's S5.3 internal component dependency diagram shows the compositional relationships but does not prescribe a build sequence. Without guidance, two engineers might build JwtService before PasswordHasher is testable, requiring rework when integration reveals interface mismatches.

## 6. Shared Assumption Responses

- **A-001:** QUALIFY — 7-day refresh TTL is reasonable for v1.0, but the "no remember me" deferral should be revisited promptly post-GA if user-session analytics show significant drop-off at the 7-day boundary.

- **A-002:** ACCEPT — bcrypt cost 12 balances security and latency well; both variants benchmark hash time <500ms, which fits within the 200ms p95 budget alongside other operations.

- **A-003:** QUALIFY — 200ms p95 is achievable but unstated-margin tight; Variant 2's micro-benchmark gates (JwtService <5ms, Redis <10ms at S8.3) partially address this by decomposing the budget, but neither variant performs a sensitivity analysis showing how bcrypt latency variance affects the composite p95.

- **A-004:** QUALIFY — SendGrid <60s p95 is historically reliable but vendor-dependent; Variant 2's R-004 mitigation (queue with retry, fallback support channel at S6 R-004) is adequate for v1.0, but neither variant bounds the failure-rate tail beyond the monitoring alert.

- **A-005:** QUALIFY — Redis-down forcing universal re-login is operationally acceptable for v1.0 scale, but the user-experience impact of a mass re-login event (potentially thousands of concurrent re-authentications) has not been modeled; Variant 2's R-005 (S6) acknowledges the risk with sentinel HA, which reduces likelihood but does not eliminate the blast radius.

- **A-006:** REJECT — 5-failed-attempt lockout in 15 minutes does enable a targeted per-account DoS vector; an attacker who knows a victim's email can lock them out every 15 minutes with just 5 requests. Variant 2's 30-minute cooldown (S9 OQ #3) mitigates this slightly compared to Variant 1's 15-minute auto-unlock, but neither variant adequately addresses the vector. Recommendation: add CAPTCHA after 3 failures rather than hard-lock at 5.

- **A-007:** QUALIFY — Quarterly RS256 rotation is standard practice, but the operational maturity required (overlap windows, key-version metadata in JWT headers, in-flight token handling) is non-trivial; Variant 2's approach of documenting the procedure (S5.2, S8.2 Checkpoint 2) without mandating quarterly execution in v1.0 is pragmatic — the first rotation should be a planned, supervised event rather than calendar-driven.

- **A-008:** ACCEPT — Legacy auth path as rollback target is viable throughout Beta+GA; both variants define feature-flag-based rollback procedures that redirect to the legacy path, and the TDD's parallel-running architecture (Phase 1+2) ensures the legacy path remains warm.
