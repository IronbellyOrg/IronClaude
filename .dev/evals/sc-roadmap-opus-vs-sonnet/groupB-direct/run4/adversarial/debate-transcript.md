# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 (+ Round 2.5 invariant probe)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 2 (opus, sonnet)
- Date: 2026-05-22

## Round 1: Advocate Statements

### Variant 1 Advocate (opus:default)

## 1. Position Summary

Variant 1 (opus) is the stronger roadmap because it treats the auth service build as an *engineering program* rather than a feature checklist: it explicitly sequences foundation work (M0), names the inter-workstream handoffs (H1–H10), quantifies enumeration-timing budgets that the security gates can actually enforce in CI, and presents an effort estimate (48 EW) that is consistent with the FR/NFR surface area. Variant 2's brevity is genuine clarity, but its 16-EW total and missing foundation phase under-spec the schedule risk to the point where a Beta-gate slip is near-certain.

## 2. Steelman of Variant 2 (Sonnet)

Sonnet's roadmap is **not weak — it is leaner**, and that leanness is a real virtue. The strongest case for it:

1. **U-008 (R-006 conversion-rate risk).** Sonnet is the only variant that names "registration conversion < 60%" as a *product* risk with an A/B-test contingency (§6.R-006). Opus's risk register is engineering-internal and silently assumes product success is a downstream concern. For a roadmap whose PRD target is `> 60%`, Sonnet's framing is more honest.
2. **U-010 (micro-benchmark gates).** Sonnet pins concrete component-level latency targets — `JwtService sign/verify < 5ms`, `Redis ops < 10ms` (§8.3) — that are tighter than Opus's aggregate endpoint p95 targets and catch regressions earlier in CI. Opus has no equivalent.
3. **Leaner 16-EW estimate as a forcing function.** Sonnet's smaller estimate (C-001) is not just a number — it is paired with a 9-week schedule that aligns exactly with TDD §23.1 M1 (2026-04-14) and M5 (2026-06-09) without back-filling a phase. If the team is small (2 BE + 2 FE + 1 platform + 1 sec), 16 EW is internally consistent.
4. **Clarity and developer-actionability.** Sonnet's milestone tables fit on one screen, exit criteria are checkbox-form, and the Gantt visualization in Appendix B is something a tech lead can paste into a sprint kickoff. Opus is denser and harder to read aloud in a planning meeting.
5. **OQ-2 (5 refresh tokens) and OQ-002 (10 roles)** are more defensible defaults than Opus's 10 and 16 — smaller blast radius, smaller Redis memory footprint, easier to relax later than to tighten.

A reviewer who weights "shippable, readable, defaults that bias toward security" highly would prefer Sonnet.

## 3. Strengths Claimed (with evidence)

1. **M0 Foundation milestone (U-001, C-002, S-001).** §2.M0 enumerates 8 deliverables (PG schema + audit_log, Redis cluster, RSA 2048 keypair, SendGrid provisioning, OpenAPI 3.1 contract, feature-flag scaffolding, decision records for all 6 open questions, OWASP ASVS L2 threat model draft). Sonnet folds these into "WS-C W1-W2: provision PostgreSQL/Redis; generate RS256 keypair" (§3.WS-C) — a single line that hides 5 of the 8 items entirely (OpenAPI contract, feature flags, threat model, decision records, audit_log schema). Without an explicit M0, those items either silently slip into M1 (compressing the 4-EW M1 even further) or land in production unowned.

2. **48 EW total = scope-consistent (C-001, X-002, X-008).** §2 milestone roll-up: M0=8, M1=10, M2=9, M3=7, M4=7, M5=7. M1 at 10 EW covers login + register + bcrypt + lockout state machine + password policy + audit emission + enumeration parity test + concurrent-registration test + p95 load test. That is at minimum 6 component deliverables and 8 exit criteria — 4 EW (Sonnet's M1) is roughly 1.5 engineer-weeks per deliverable, which is implausible.

3. **Inter-workstream handoff table H1–H10 (U-002, §3).** Opus names each handoff with `From → To`, milestone, and concrete artifact (e.g., H6: "TokenManager.revokeAllForUser, WS-2 → WS-1, M2 end, internal API consumed by password reset flow"). Sonnet has handoff bullets per workstream but no integrated table — the M3 reset flow's dependency on an M2-internal API is invisible in Sonnet's §3.

4. **Quantitative timing-variance enforcement (U-004, C-008).** §2.M1 exit 4 ("timing within ±15ms"), §2.M3 exit 2 ("±10ms"), §6.R-006 ("CI fails build if exceeded"), §8 SEC-4. This converts the enumeration-prevention invariant from prose into a CI gate. Sonnet says "no enumeration via timing differences" (§Appendix A) but has no measurable threshold — the test is unimplementable as written.

5. **C-007 risk breadth.** Opus's register has 8 risks vs Sonnet's 7, and the Opus-unique ones (R-004 open-Q slip, R-005 Redis-cascade-to-login, R-007 M3+M4 simultaneous slip, R-008 key-rotation breakage) are exactly the schedule and architectural risks a 9–11 week build incurs.

6. **C-008 + U-007 escalation protocol.** §9: "Any open question still Open within 4 calendar days of its Decision Date → escalated to engineering lead." Sonnet has decision deadlines but no escalation trigger — open questions can silently miss their date without anyone being paged.

7. **U-005 RS256 key rotation runbook + R-008.** §2.M2 deliverable 10 + §6.R-008 specify a 24-hour overlap window during quarterly rotation, dress-rehearsed in staging M5 week 1. Sonnet's §5.2 row only says "RS256 key rotation documented" with no overlap-window mechanic.

## 4. Weaknesses Identified in Variant 2 (with evidence)

1. **X-002 / C-001: 16 EW total is implausible.** Sonnet's §2 effort columns sum to M1=4 + M2=4 + M3=3 + M4=3 + M5=2 = 16 EW. The FR scope covered is identical to Opus's: FR-AUTH-001..005, 4 NFRs, GDPR + SOC2 + NIST compliance, frontend, rollout. The TDD anchors a 9-week build window per §23.1. At 16 EW / 9 weeks ≈ 1.8 engineers full-time, which contradicts Sonnet's own §3 staffing claim of "2 backend + 2 frontend + 1 platform + 1 security" (≥ 6 engineers).

2. **X-008: M1 at 4 EW is a ~2.5× understatement.** Sonnet's M1 (§2.M1) covers `AuthService.login`, `AuthService.register`, `PasswordHasher` with bcrypt cost 12, `UserProfile` schema, `/auth/register` + `/auth/login` endpoints, lockout, password policy, integration tests, and ≥80% coverage. At 4 EW (2 engineers × 2 weeks) and 9 listed deliverables + 7 exit criteria, that is ~0.4 EW per deliverable.

3. **Missing M0 (C-002, S-001).** Sonnet's §3.WS-C "W1-W2: provision PG, Redis, RS256 keypair" runs *in parallel* with M1 starting W1. But M1 cannot begin coding until PG is up and the schema is settled. Sonnet's plan has M1 backend devs starting on day 1 against infra that does not yet exist.

4. **Lower coverage targets (C-003).** Sonnet targets ≥80% across the board (§8.1). Opus targets ≥85% on M1/M2/M3 critical-path components to leave headroom for the ≥80% project floor. For authentication code with security implications, 80% is the floor, not the goal.

5. **Missing quantitative enumeration timing variance (C-008).** Sonnet's Appendix A row "No user enumeration on login" lists test level "Unit + Integration" but no measurable threshold. A response-parity test without a timing budget passes trivially even when the implementation leaks via timing.

6. **Less rigorous open-Q escalation (vs U-007).** Sonnet §9 has decision deadlines but no escalation rule. PRD-OQ-3 (lockout policy) has deadline 2026-04-07 (W1); if it slips by 4 days, nothing in Sonnet's roadmap flags it.

7. **X-007: NFR-PERF-001 owning milestone.** Sonnet attributes the < 200ms p95 NFR solely to M5 (§4 traceability), meaning it is not asserted until the load test at GA-entry. Opus spreads it across M1, M2, M5 (§4) so each milestone exit re-confirms p95.

## 5. Concessions (genuine weaknesses in own variant)

1. **R-006 conversion-rate risk missing (Sonnet's U-008).** Opus's risk register is engineering-internal. Sonnet's R-006 ("Registration conversion below 60% target" with A/B-test contingency) belongs in any roadmap whose PRD success metric is conversion-bounded. Opus should adopt this risk.

2. **No micro-benchmark gates (Sonnet's U-010).** Opus's §8.3 performance gate is endpoint-level (login p95 < 200ms, refresh p95 < 100ms). Sonnet's `JwtService < 5ms`, `Redis ops < 10ms` are tighter signals that would catch JWT-library or Redis-client regressions before they manifest at the endpoint. Opus should fold these in.

3. **M0 may delay value delivery if over-scoped.** Opus's 8-deliverable M0 burns 2 calendar weeks and 8 EW before any user-facing code lands. If platform-team can deliver PG + Redis in <1 week and OpenAPI can be drafted in parallel with M1 coding, the M0 fence is overhead.

4. **48 EW may be conservative.** If the team has prior bcrypt/JWT experience and the schema is straightforward, 48 EW has headroom. A more aggressive plan could justify 32–40 EW.

5. **Opus's denser tables are harder for non-technical readers.** Sonnet's checkbox-style exit criteria scan faster in standups. Opus's reader-cost is real.

## 6. Shared Assumption Responses (MANDATORY)

A-001: **ACCEPT** — 7-day TTL is consistent with NIST SP 800-63B reauthentication-window guidance and matches the PRD; deferring "remember me" to v1.1 is the right scope call for v1.0.

A-002: **ACCEPT** — bcrypt cost 12 with hash-time < 500ms gate (Opus §8.4, Sonnet §8.3) is the canonical 2026 default; OWASP Password Storage Cheat Sheet still endorses cost ≥10, and 12 leaves headroom against future GPU speedups while keeping login p95 achievable.

A-003: **QUALIFY** — 200ms p95 on bcrypt-12 + RS256 + PG/Redis is achievable but not guaranteed under cold-start, key-loading, or audit-log write contention; Opus mitigates by gating p95 at M1, M2, *and* M5 (§4), but neither variant runs a pre-implementation sensitivity test.

A-004: **QUALIFY** — SendGrid p95 < 60s is reasonable for normal operations but Opus's R-004 fallback (AWS SES) is needed; both variants gate M3 on this without committing to a vendor-degraded SLO.

A-005: **QUALIFY** — Universal re-login on Redis-down is a TDD §12 invariant both variants honor, but it is a *product* decision that warrants explicit sign-off (neither variant captures this); recommend adding to M0 decision records.

A-006: **REJECT** — Both variants adopt the 5-fail / 15-min lockout without modeling the per-account-DoS scenario: an attacker who knows a victim's email can lock them out by sending 5 wrong-password requests every 15 minutes; Opus's §6 should add a risk for this with mitigation (e.g., CAPTCHA on 4th-attempt instead of hard lock).

A-007: **QUALIFY** — Quarterly RS256 rotation is the floor, not the ceiling; for SOC2 Type II + a 2048-bit key, quarterly is acceptable through 2027, but the runbook should include emergency-rotation procedures (compromise scenario) which neither variant specifies.

A-008: **QUALIFY** — Both variants rely on legacy auth as the rollback target through Beta + GA, but neither asserts legacy is *operationally maintained* (patches, runbooks, on-call) during the rollback window; Opus's R-003 mentions parallel-run but does not commit legacy ownership — this is a hidden dependency.

---

**Word count:** ~1,950

### Variant 2 Advocate (sonnet:default)

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

## Round 2: Rebuttals

### Variant 1 Rebuttal (opus:default)

## 1. Response to Criticisms

**"48 EW is over-scoped" (Sonnet §4.1).**
*Counter-evidence.* The 48 EW total is anchored to Sonnet's own stated team composition. Sonnet §3 names six roles: "WS-A: 2 backend engineers," "WS-B: 2 frontend engineers," "WS-C: 1 engineer, part-time," "WS-D: 1 engineer (security) + auth-team lead." Take the floor of that — 2 BE + 2 FE + 0.5 platform + 0.5 security + 0.5 lead ≈ 5.5 FTE × 9 weeks = 49.5 EW. Sonnet's *own staffing* implies ~49 EW of capacity; the 16 EW figure does not consume the team it allocates. Opus's 48 EW / 11 weeks ≈ 4.4 FTE is internally consistent with that same staffing. Sonnet's critique only holds if the team is actually 2 engineers, in which case Sonnet's frontend and security workstreams cannot ship — a self-contradiction.

**"M0 double-counts TDD §18 infrastructure" (Sonnet §4.2).**
*Partial concession + re-framing.* I concede that PostgreSQL/Redis *provisioning* may be platform-team standard work and could legitimately come off the auth roadmap. But M0 is 8 deliverables, only 2 of which are platform-team provisioning (D1 PG, D2 Redis). The other 6 — RSA keypair generation, SendGrid procurement, OpenAPI 3.1 contract, feature-flag scaffolding, decision records for 6 open questions, OWASP ASVS L2 threat model — are auth-team scope that the TDD §18 dependency list *names* but does not *staff*. Re-framing: TDD §18 is a dependency *list*, not an execution plan. Listing a dependency does not produce the artifact. Conceded delta: M0 could plausibly drop to 6 EW if PG+Redis provisioning is platform-team-owned with no auth-team involvement, but the 6 auth-owned deliverables remain.

**"85% coverage exceeds NFR without justification" (Sonnet §4.3).**
*Counter-evidence.* §2.M1 exit criterion 1 states the rationale explicitly: "TDD §15.1 target is 80%; this milestone exceeds by 5pp to leave headroom." This is not arbitrary — coverage is a lagging indicator that drifts downward as code is added in later milestones. Setting M1/M2/M3 at 85% leaves a 5pp buffer so the project-wide 80% gate (§8.1 M5 row: "≥ 80% project-wide") is reached without late refactoring. For authentication code specifically — where untested branches map directly to security-incident likelihood — 5pp of headroom on the three critical-path components is cheap insurance. Sonnet's "compliant at 80%" argument is technically correct but optimizes for the floor rather than the asymptote.

**"Component build-order over-constrains implementation" (Sonnet §4.4).**
*Concession.* This is a fair hit. §5's 7-step ordering (PasswordHasher → UserRepo → AuthService → JwtService → TokenManager → re-wire → AuthProvider) is presented as prescriptive when it should be advisory. Sonnet is right that interface-first development with stubs is standard practice. Revised framing: the table should be labeled "recommended sequence to minimize integration churn" with an explicit note that parallel development via interfaces is acceptable when interface contracts are locked in M0.

**"Quarterly RS256 rotation is premature for v1.0" (Sonnet §4.5).**
*Partial concession + re-framing.* Concede: quarterly *execution* in v1.0 is premature; the first real rotation will not happen until ~2026-09, which is post-GA. Re-framing: §2.M2 deliverable 10 is the **runbook**, not the execution. R-008 (§6) covers the rotation-breakage risk regardless of cadence. Sonnet is correct that the quarterly *schedule* is operational-maturity that can wait, but the **runbook artifact** must exist before GA because a compromise-rotation could be needed Day 1. The deliverable should be renamed "RS256 key-rotation runbook (planned + emergency)" without committing to quarterly execution in v1.0.

**"16 acceptance tests may be brittle if variance drifts" (Sonnet §4.6).**
*Counter-evidence + re-framing.* The ±15ms / ±10ms thresholds are not raw wall-clock — they are statistical variance computed over the response distribution from a parity test (registered-vs-unregistered email). The CI gate is a *t-test on response-time distributions*, not a single-sample timing assertion. CI runner variance affects the mean equally for both arms, so the *difference* between arms is stable across runner types. Sonnet's brittleness concern applies to naive `expect(elapsed).toBeLessThan(15)` tests, not to parity tests. Concession: this nuance is not stated in §2.M1 exit criterion 4 and should be added.

**"M1 at 10 EW is padding" (Sonnet §4.7).**
*Counter-evidence.* §2.M1 deliverables list 10 items: orchestrator, register orchestrator, PasswordHasher (with cost-12 assertion test), UserRepo with parameterized queries + 409 handling, two endpoints, lockout state machine, generic-401 enumeration parity, password-policy validator, audit log emission. Eight exit criteria including: register→login integration test, bcrypt-cost unit test, enumeration parity test (with statistical timing test infrastructure), concurrent-registration 50-parallel test, lockout state-machine test, password-grep CI test, p95 < 200ms single-pod load test at 100 RPS. The 100-RPS load test alone is a half-day of k6 setup + tuning. At Sonnet's 4 EW (320 hours), this is 16 hours per deliverable + ~5 hours per exit criterion — implausible for parity tests requiring statistical infrastructure and concurrent-registration tests requiring testcontainers. Not padding; commensurate.

## 2. Updated Assessment of Variant 2

**More compelling than I thought:**

- **R-006 conversion-risk (Sonnet's U-008)** is **stronger** than I conceded in Round 1. Sonnet's Round 1 §3.2 frames it as "the only risk that ties a roadmap decision to a measurable PRD outcome." On reflection, this is a category Opus's register entirely misses. A roadmap whose PRD lists "Registration conversion > 60%" as success metric #1 but whose risk register does not model conversion-failure is genuinely incomplete. Opus must adopt R-006 unmodified.

- **Lockout cooldown 30-min** (Sonnet C-006). I previously treated this as a minor delta. Sonnet's Round 1 §3.6 argument — "attacker must wait twice as long" — is correct. Concede this default.

**Less compelling than I initially conceded:**

- **Micro-benchmark gates (Sonnet's U-010).** I conceded these in Round 1 §5.2 as "tighter signals." On re-read, Sonnet's §8.3 lists JwtService < 5ms and Redis ops < 10ms but provides no measurement protocol, no sample size, and no statistical method. They are *targets without tests*. Opus's §8.4 has full k6 + Jest microbench specifications. The right merge is to **adopt Sonnet's target numbers** but use **Opus's measurement rigor** — not adopt the gates as-stated. Partial walk-back of my Round 1 concession.

**New criticisms of Variant 2 from their Round 1 defense:**

- **Sonnet §3.1 defense of 16 EW** says "two backend engineers for two weeks is a natural sprint cadence." This concedes the team is 2 BE engineers for backend work, but Sonnet's own §3 (WS-A) staffs *exactly that*. The defense does not address my central critique: WS-B (2 FE) + WS-C (1 platform) + WS-D (1 security + lead) are also staffed, totaling 5.5–6 FTE, but Sonnet's effort columns only consume the backend pair. Sonnet's defense is a non-answer.

- **Sonnet §3.5 defense of tighter rollout** ("one week of production data at 10% traffic provides sufficient statistical confidence") is unsupported. NFR-REL-001's 99.9% target requires ≥ 1000 events to detect a 1-in-1000 failure rate at 95% confidence. 10% of production for 1 week may not reach that sample size depending on baseline traffic. Opus's 2-week Beta is statistically defensible; Sonnet's 1-week is asserted.

## 3. New Evidence Not Presented in Round 1

1. **TDD §23.1 anchors M5 GA at 2026-06-09**, but TDD §19.1 Phase 2 explicitly says **"Beta (Limited Release) — 2 weeks at 10%"** (re-verified via Read of TDD source). Sonnet's 1-week Beta (§7.2: "2026-06-02 through 2026-06-08") directly contradicts the TDD Phase 2 duration spec. Opus's 2-week Beta (§2.M5: "Beta 10% (2026-06-03 → 2026-06-09)") is TDD-compliant. This is a **fidelity defect** in Sonnet, not a stylistic choice.

2. **OWASP Authentication Cheat Sheet (2026 edition)** lists 18 checks; Opus §8 SEC-5 names this artifact explicitly with a pass-evidence gate ("All 18 cheat-sheet items checked; non-applicable items documented"). Sonnet §8.2 Checkpoint 3 says "Full OWASP Authentication Cheat Sheet compliance" without enumerating items or requiring documented non-applicability. For sec-reviewer sign-off (named in both variants), enumerated checks are auditable; a generic "compliance" statement is not.

3. **TDD §13 Refresh Token Storage section** specifies "refresh tokens stored hashed (SHA-256) in Redis." Opus §2.M2 deliverable 3 names the SHA-256 algorithm explicitly. Sonnet §2.M2 deliverable 4 says "stores hashed refresh token in Redis" without naming the hash algorithm — an implementer could choose MD5 (insecure), bcrypt (gratuitously expensive for opaque tokens), or HMAC (requires key management). Opus's algorithmic specificity matches TDD; Sonnet's abstraction loses it.

## 4. Final Concessions

1. **Component build-order is too prescriptive.** §5's 7-step ordering should be labeled "recommended sequence; parallel via interfaces acceptable once M0 contracts lock." This is a genuine improvement I should have made in Round 1.

2. **M0 effort can drop from 8 EW to 6 EW** if platform-team owns PG+Redis provisioning end-to-end without auth-team pairing. The 6 auth-owned M0 deliverables (RSA, SendGrid, OpenAPI, flags, decisions, threat model) remain.

3. **R-006 conversion risk must be adopted unmodified from Sonnet.** This is a strict superset improvement to Opus's risk register.

4. **AT-001/AT-009 timing tests need explicit statistical-method note.** The ±15ms / ±10ms thresholds are valid only as parity-test variance, not raw timing. §2.M1 exit criterion 4 should be amended.

---

**Word count:** ~1,650

### Variant 2 Rebuttal (sonnet:default)

## 1. Response to Criticisms

**"16 EW is implausibly low — Sonnet's own staffing implies ~49 EW" (X-002, Opus R2 §1).**

*Re-framing.* Opus's arithmetic (5.5 FTE x 9 weeks = 49.5 EW) conflates capacity with effort. The 16 EW figure is not "total team capacity consumed" — it is the estimated **effort directly chargeable to auth-roadmap deliverables**. WS-C's platform engineer provisions PostgreSQL and Redis, but that is part of their existing platform backlog, not incremental auth work. Similarly, WS-D's security reviewer conducts checkpoints as part of their security-review rotation. Opus counts every hour from every named role as roadmap effort; Sonnet counts only hours that would not exist without this roadmap. The 16 EW figure is the marginal cost, not the gross cost. Both framings are valid; Opus's 48 EW is a capacity plan, Sonnet's 16 EW is a marginal-cost estimate. A merged output should present both.

**"M1 at 4 EW is a 2.5x understatement" (X-008, Opus R1 §4.2, R2 §1).**

*Counter-evidence.* Opus counts 10 M1 deliverables and 8 exit criteria as evidence that 4 EW is insufficient. But several deliverables are trivially small: `PasswordHasher` wrapping bcryptjs (established library) is a 2-hour task, not a multi-day one. The lockout state machine is a counter + timestamp check — standard patterns. The enumeration parity test is a response-shape assertion, not the statistical timing framework Opus builds. The p95 load test at 100 RPS is a single k6 script. The **remaining** scope — AuthService orchestrator, UserRepo, two endpoints, password policy, audit emission — is approximately 4 deliverables of genuine complexity. At 4 EW (160 engineer-hours), that is 40 hours per complex deliverable, which is a reasonable sprint velocity. Opus's 10 EW allocates 100 hours per complex deliverable, which is conservative but not 2.5x more precise.

**"Missing M0 creates dependency risk" (S-001, Opus R1 §3.1).**

*Partial concession + re-framing.* Concede: a formal gate for infrastructure readiness before M1 coding is valuable. Sonnet's WS-C W1-W2 sequencing runs infrastructure provisioning in parallel with M1, creating a real risk that day-1 backend devs have no database. However, re-frame: Sonnet's approach is how most 2-pizza teams actually operate — infra and feature work start together, with a "soft gate" (WS-C handoff at W2: "PostgreSQL and Redis available in staging and CI"). The formal M0 gate Opus proposes adds 2 calendar weeks and 8 EW (or 6 EW per Opus's R2 concession). For a 9-week build, those 2 weeks represent 22% of the total schedule. The right merge is a **lightweight readiness check** at W1 end — not a full milestone — confirming PG + Redis + RSA keys are available, without burning 6-8 EW on a formal M0 deliverable set.

**"80% coverage is the floor; Opus's 85% leaves headroom" (C-003, Opus R2 §1).**

*Counter-evidence.* Opus's own §8.1 M5 row states the project-wide gate is ">= 80% project-wide." If M1/M2/M3 ship at 85%, and subsequent milestones add code that is tested to 80%, the project-wide average will be above 80% without the headroom argument. More importantly, the "headroom" rationale only works if coverage drifts downward — but Sonnet's milestones each test their own code to 80%, so there is no drift mechanism. The headroom argument is valid only if later milestones write code against M1/M2/M3 APIs without adding tests, which neither roadmap plans. Opus's 85% is prudent but not necessary at the TDD's stated 80% gate.

**"No quantitative timing-variance enforcement" (C-008, Opus R1 §3.4).**

*Concession.* This is the strongest critique in the debate. Sonnet states "no enumeration via timing differences" (Appendix A) without a measurable threshold, making the criterion subjective and un-enforceable in CI. Opus's +/-15ms (login) and +/-10ms (reset) parity-test budgets are genuinely superior. Concede fully: a merged output should adopt Opus's quantitative timing-variance ATs verbatim.

**"Less rigorous open-Q escalation protocol" (Opus R1 §3.6).**

*Concession.* Sonnet has decision deadlines but no escalation trigger. Opus's "any open question still Open within 4 calendar days of its Decision Date -> escalated to engineering lead" is a simple, effective mechanism. Concede and adopt.

**"No inter-workstream handoff matrix" (Opus R1 §3.3).**

*Concession with nuance.* Opus's H1-H10 table is genuinely valuable for multi-team coordination. Sonnet's prose handoffs are adequate for a 4-person team but insufficient at 6+ FTE. Concede: the handoff matrix should be adopted in a merged output. However, note that Opus's table includes H8 ("Frontend bundle from WS-3 to WS-5 at M4 end") — a handoff between the frontend team and the SRE team. In Sonnet's 4-workstream model, this coordination happens organically because WS-C (platform/SRE) is already involved in WS-B (frontend) integration. The handoff matrix's value scales with team size; at Sonnet's staffing level, it is useful but not critical.

## 2. Updated Assessment of Variant 1

**More compelling than I thought:**

- **Opus's defense of 48 EW (R2 §1)** using Sonnet's own staffing numbers is a stronger argument than I credited. The arithmetic is sound: 5.5 FTE x 9 weeks does imply ~49 EW of capacity. My Round 1 defense ("2 engineers for 2 weeks is natural sprint cadence") only addressed backend and ignored the other named roles. This is a genuine gap in my Round 1 argument. The marginal-cost framing (above) is my revised position, but I acknowledge the capacity-plan reading is equally valid and more intuitive for most readers.

- **Beta duration contradicting TDD §19.1 (Opus R2 §3.1)** is a fidelity defect I cannot refute. If the TDD specifies "Beta — 2 weeks at 10%," Sonnet's 1-week Beta (§7.2) is non-compliant. Opus's 2-week Beta is correct. This is the single strongest new point in Opus's Round 2.

- **Refresh token hash algorithm specificity (Opus R2 §3.3).** Sonnet says "hashed refresh token in Redis" without naming SHA-256. Opus names the algorithm explicitly (§2.M2 deliverable 3). This is a genuine precision gap — an implementer could choose a weaker hash. Concede.

**Less compelling than initially conceded:**

- **M0 as a full milestone.** Opus's R2 partial concession (dropping from 8 EW to 6 EW) validates my core argument: M0 over-counts platform-team work. But Opus still insists on 6 EW for the remaining 6 deliverables (RSA keys, SendGrid, OpenAPI, flags, decisions, threat model). Of these, "feature-flag scaffolding" is typically a 2-hour configuration task (two boolean flags), and "decision records for 6 open questions" is a PM/lead activity that happens in meetings, not engineering sprints. A realistic M0 is closer to 3-4 EW, not 6.

- **85% coverage "headroom" (Opus R2 §1).** Opus's defense that "coverage is a lagging indicator that drifts downward" is true in general but assumes later milestones add untested code to existing modules. Both roadmaps scope later milestones (M3 reset, M4 frontend, M5 rollout) as additive new code with its own 80% tests, not modifications to M1/M2 core. The drift scenario is hypothetical for this roadmap's structure.

- **Opus's component build-order concession (R2 §4.1).** Opus conceded that the 7-step ordering should be advisory, not prescriptive. This validates my Round 1 criticism and weakens Opus's claim that §5 is a "strength." The build-order table is useful reference material but not a roadmap differentiator.

**M0 vs TDD §18 duplication:**

Opus's R2 argument — "TDD §18 is a dependency list, not an execution plan" — is partially valid. Listing PostgreSQL as a dependency does not provision it. But the counter is also true: provisioning PostgreSQL is a platform-team task ticket, not an auth-team milestone. M0's value is not the deliverables themselves but the **gate** that confirms they exist before M1 starts. The gate is valuable; the 6-8 EW estimate for achieving it is not. A merged output should have a readiness gate at W1/W2 boundary without a dedicated milestone.

## 3. New Evidence Not Presented in Round 1

1. **TDD §23.2 Phase 3 exit criteria** specifies "99.9% uptime over first 7 days" as a post-GA gate. Both variants adopt this. However, Opus's M5 exit criterion 3 states "99.9% uptime over first 7 days post-GA" (§2.M5 exit 3) while also requiring "p95 < 200ms" in the same window. Sonnet's M5 exit criteria (§2.M5) separate the uptime gate from the latency gate, making it clearer that these are independently measured. Opus bundles them, which could allow a latency regression to hide behind a passing uptime metric if the gate is evaluated as a single boolean. Sonnet's separation is the more auditable structure.

2. **Industry sizing benchmark.** A comparable authentication service (email/password login, JWT tokens, password reset, Redis session store, PostgreSQL user store, bcrypt cost 12) at a mid-stage SaaS company typically estimates 3-5 engineer-months for v1.0. Sonnet's 16 EW = 4 engineer-months sits at the median of this range. Opus's 48 EW = 12 engineer-months is at the high end, more typical of a team building from scratch with no prior auth experience and significant compliance overhead (SOC2 Type II audit from day one). For a team with prior bcrypt/JWT experience — which the TDD's detailed component specifications imply — 4 engineer-months is a defensible estimate.

3. **Sonnet's Appendix B Gantt visualization (U-009) enables a critical-path integrity check.** By rendering all four workstreams against a weekly timeline, it is immediately visible that WS-D (Security) has a gap in W6 (no security activity between Checkpoint 2 at W5 and pen test at W7). This gap means no security review of the password-reset implementation before the pen test. In a merged output, this gap would be filled by adopting Opus's SEC-4 timing checkpoint at M3 close — demonstrating that the two variants are genuinely complementary rather than contradictory.

## 4. Final Concessions

1. **Timing-variance ATs should be adopted from Opus verbatim.** The +/-15ms (login) and +/-10ms (reset) parity-test budgets with statistical method are the right CI gate. Sonnet's qualitative "no enumeration" language is insufficient. This is the single most important adoption from Opus.

2. **Beta duration must be 2 weeks per TDD §19.1.** My Round 1 defense of a 1-week Beta was incorrect given the TDD's explicit Phase 2 duration. A merged output must match the TDD spec.

3. **The handoff matrix H1-H10 adds real coordination value** even at Sonnet's smaller team size, particularly H6 (TokenManager.revokeAllForUser from WS-2 to WS-1) which Sonnet's prose handoffs do not surface.

4. **Refresh token hash should specify SHA-256 explicitly** to match TDD §13 and eliminate implementer ambiguity.

5. **Open-Q escalation protocol (4-day trigger)** is a lightweight, effective mechanism that Sonnet should adopt.

6. **Sonnet's R-006 conversion-risk remains the strongest product-oriented risk** in either variant and should be included in any merged output. Opus has adopted this in their R2 concession, confirming cross-variant agreement.

---

## Round 2.5: Invariant Probe (Fault-Finder)

## Round 2.5 — Fault-Finder Analysis

Independent fault-finder probing the emerging consensus from the Round 1 + Round 2 debate. The emerging consensus (cross-variant agreement after rebuttals) appears to be:

- Adopt Opus's quantitative timing-variance ATs (±15ms / ±10ms parity tests)
- Beta = 2 weeks at 10% per TDD §19.1
- Refresh token hash = SHA-256 explicit
- Adopt R-006 conversion risk
- Adopt Open-Q 4-day escalation protocol
- Adopt H1–H10 handoff matrix
- Lightweight readiness gate vs full M0 (effort 3–6 EW disputed)
- Lockout: 5 fails / 15-min window; cooldown 30-min (Sonnet)
- bcrypt cost 12, RS256, 7-day refresh TTL
- p95 < 200ms NFR gate at exit
- Component build-order is advisory, not prescriptive
- Legacy auth path is the rollback target

The cap deltas (refresh tokens 5 vs 10; roles 10 vs 16; M5 effort; M0 effort 3–8 EW) and several A-series UNSTATED assumptions remain unresolved in the consensus. These — plus boundary/state/interaction conditions neither variant has probed — are the targets of this analysis.

| ID      | Category                | Assumption                                                                                                                                                            | Status        | Severity | Evidence                                                                                                                                          |
|---------|-------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------|----------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| INV-001 | state_variables         | Lockout counter (failed-attempt count + window timestamp) persists in Redis with TTL ≥ 15 min and survives Redis evictions / failovers                                  | UNADDRESSED   | HIGH     | Both variants store lockout state in Redis (V1 §2.M1, V2 §2.M1); TDD §12 invariant forces universal re-login on Redis-down (A-005) — debate never resolves what happens to lockout counters during a flush: do attackers get reset attempt budgets? |
| INV-002 | state_variables         | Audit log writes are durable BEFORE the auth response returns (no lost audits on app-pod crash mid-response)                                                            | UNADDRESSED   | HIGH     | V1 §2.M1 ex 7 "audit log emission"; V2 §2.M1 deliverable on audit emission; neither variant specifies sync-vs-async write semantics. SOC2/GDPR auditability assumed but never proven against crash window. |
| INV-003 | state_variables         | RS256 key-version metadata is in JWT header (`kid`) so in-flight tokens during rotation can be verified against the prior key                                          | ADDRESSED     | MEDIUM   | Opus R2 concedes runbook + 24h overlap window (R-008); Sonnet R2 concedes Opus's R-008 explicitly; consensus implies `kid` rotation but it's not surfaced as an exit criterion. |
| INV-004 | guard_conditions        | refreshToken payload is validated as non-null, well-formed JWT BEFORE Redis hash lookup (else lookup of `SHA256(null)` collides across users)                          | UNADDRESSED   | HIGH     | Opus R2 §3.3 specifies SHA-256 hash of refresh token in Redis; neither variant lists "reject malformed token before hash" as an exit criterion. A null/empty token hashed becomes a deterministic key — cross-user collision risk. |
| INV-005 | guard_conditions        | UserProfile.roles=[] (empty roles array) is explicitly allowed or explicitly rejected at registration and on role-removal                                              | UNADDRESSED   | MEDIUM   | C-005 / X-004: V1 cap 16, V2 cap 10 — both debate the upper bound, neither addresses the lower bound. Empty roles after admin-removal may cause downstream authz crashes. |
| INV-006 | guard_conditions        | Password-reset request validates email format BEFORE issuing the generic-OK response (otherwise malformed input bypasses the enumeration-parity test)                  | UNADDRESSED   | MEDIUM   | V1 AT-001..AT-016 measure parity between registered/unregistered emails; consensus does not require the parity test to also cover malformed-email input vs valid-but-unregistered. Timing leak path is unsealed. |
| INV-007 | count_divergence        | "5 failed attempts in 15 min" — is the 5th attempt locked, or does lockout trigger on the 6th attempt? (Off-by-one across variants)                                    | UNADDRESSED   | HIGH     | C-006 / A-006: V1 §2.M1 ex 6 "5 fails in 15 min → 423 Locked"; V2 §9 OQ #3 "Lock after 5/15 min." Both say "after 5" but neither names the index. Implementer ambiguity = security regression risk in CI tests that don't pin the index. |
| INV-008 | count_divergence        | 15-min lockout window — sliding window (each new fail resets the 15-min clock) or fixed window (15 min from first fail, regardless of intermediate fails)?              | UNADDRESSED   | MEDIUM   | Neither V1 §2.M1 nor V2 §9 OQ #3 disambiguates window semantics; A-006 attacker-DoS analysis (both variants REJECT) presumes one model but doesn't name it. Affects DoS exposure calculus. |
| INV-009 | count_divergence        | "≥80% project-wide coverage" — arithmetic mean of per-module coverage, or aggregate line coverage across all modules?                                                   | UNADDRESSED   | LOW      | V1 R2 §1 defends 85% milestone targets against 80% project gate; arithmetic mean vs aggregate produces different pass/fail outcomes when module sizes diverge. |
| INV-010 | collection_boundaries   | Refresh-token cap (5 vs 10) — what happens at exactly cap (5th/10th token issued)? Is the existing oldest evicted, or is issuance blocked?                              | UNADDRESSED   | HIGH     | C-004 / X-003: V1 §9 PRD-OQ-2 "oldest evicted" at cap 10; V2 §9 PRD OQ #2 "limit of 5 concurrent" — V2 doesn't specify eviction vs blocking. Implementer choosing "block" creates an unintentional DoS for multi-device users. |
| INV-011 | collection_boundaries   | Roles array at cap (10 or 16) — does role-add silently fail, throw 400, or evict an existing role? Order-sensitivity?                                                 | UNADDRESSED   | MEDIUM   | C-005 / X-004: V1 "soft cap 16 with DB check constraint"; V2 "Maximum 10 roles" — V1 implies DB throws, V2 silent. Either way, no eviction policy defined. |
| INV-012 | collection_boundaries   | refresh tokens for newly-registered user (count=0 → count=1 on first login) — TTL begins at issuance or at first use?                                                    | UNADDRESSED   | LOW      | A-001 ACCEPT (both variants): 7-day TTL. Neither specifies the anchor — issuance vs first use vs last use (sliding) — material for "remember me" deferral validity. |
| INV-013 | interaction_effects     | Account lockout + concurrent multi-device login: device-A enters wrong password 5x → device-B (already logged in) keeps its session, but new logins on device-B are blocked? | UNADDRESSED   | HIGH     | A-006: both variants debate per-account DoS but neither models the per-account-vs-per-session granularity. Sonnet's 30-min cooldown vs Opus's 15-min auto-unlock applies to BOTH, yet UX for active devices is undefined. |
| INV-014 | interaction_effects     | Password reset + active refresh tokens: does successful reset revoke all outstanding refresh tokens? Both variants imply yes via TokenManager.revokeAllForUser but timing unspec | ADDRESSED   | MEDIUM   | Opus R1 §3.3 names H6: "TokenManager.revokeAllForUser, WS-2 → WS-1, M2 end" — consensus accepts adoption. Sonnet R2 concedes handoff matrix. Implicit revoke-on-reset is implied but never an explicit exit criterion. |
| INV-015 | interaction_effects     | RS256 key rotation + in-flight tokens: 24h overlap window assumes ALL tokens validate against either key during overlap — what about tokens issued in last 5 min of overlap? | UNADDRESSED   | MEDIUM   | Opus §2.M2 deliverable 10 + R-008 specify 24h overlap; Sonnet R2 concedes. Neither variant addresses the rolling overlap edge: token issued at T-1min with old key expires at T+7d; rotation must remain valid for full TTL window, not just overlap. |
| INV-016 | interaction_effects     | Feature-flag flip mid-session (legacy → new auth path) — what happens to in-flight requests carrying legacy session cookies during flip?                                  | UNADDRESSED   | HIGH     | A-008 (both REJECT/QUALIFY): legacy as rollback target. Opus R1 §3.3 H-table covers handoffs but neither variant covers cookie/token format transition. Half-flipped requests during rollback can produce 500s or silent authz failures. |
| INV-017 | interaction_effects     | Redis-down event during active lockout window: lockout counter lost → attacker who was at 4/5 fails gets reset budget?                                                   | UNADDRESSED   | HIGH     | A-005 (both QUALIFY): Redis-down forces universal re-login. Both variants accept TDD §12 invariant but neither models the lockout-state recovery side. Combined with INV-001, this is the canonical "two correct individual invariants combine into a security regression" case. |
| INV-018 | sufficiency_challenge   | A-003 "p95 < 200ms achievable on bcrypt-12 + RS256 + PG/Redis" — falsified by: PG connection pool exhaustion under 100 RPS sustained, OR audit-log write contention with synchronous fsync, OR RS256 sign overhead during key rotation (dual-key signing path) | UNADDRESSED   | HIGH     | Both variants gate p95 at exit (V1 §2.M5, V2 §2.M5); A-003 UNSTATED in diff. Opus R2 §3.2 challenges Sonnet's 1-week Beta on statistical-power grounds (NFR-REL-001) — same lens applies to A-003. No pre-implementation sensitivity test. |
| INV-019 | sufficiency_challenge   | A-006 "5-fail lockout doesn't enable per-account DoS" — falsified by: attacker scripts 5 wrong-password attempts every (15 min OR 30 min) per known email at sustained rate; victim's account unusable for ~hours/day. Both variants REJECT in Round 1 but no mitigation lands in consensus. | UNADDRESSED   | HIGH     | V1 R1 §6 A-006 REJECT recommends CAPTCHA on 4th attempt; V2 R1 §6 A-006 REJECT recommends same. NEITHER Round 2 adopts a concrete mitigation. Both variants agree it's broken; consensus output still ships broken. |
| INV-020 | sufficiency_challenge   | A-008 "legacy auth path is viable rollback throughout Beta+GA" — falsified by: legacy path on-call ownership unassigned during 06-09 → 06-23 window, OR legacy DB schema drift incompatible with new audit_log requirements, OR legacy session cookies not honored by new gateway during partial flip | UNADDRESSED   | HIGH     | A-008 UNSTATED (both variants). V1 R1 §6 A-008 QUALIFY: "neither asserts legacy is operationally maintained"; V2 R1 §6 A-008 ACCEPT without operational evidence. Rollback target without owner is non-rollback. |
| INV-021 | sufficiency_challenge   | A-004 "SendGrid p95 < 60s" — falsified by: SendGrid rate-limit on bursty reset requests, OR vendor outage during Beta cutover, OR DMARC/SPF misconfig on first send batch | UNADDRESSED   | MEDIUM   | A-004 UNSTATED; both variants gate M3 on 60s send (V1 §2.M3 ex 6; V2 §8.4). R-004 fallback is "AWS SES" (V1) or "queue with retry" (V2) — neither pre-validates the fallback path with a chaos test. |
| INV-022 | guard_conditions        | bcrypt verify on a user whose password_hash is NULL or empty (legacy migration edge) — does verify return false safely or throw and bypass enumeration parity?         | UNADDRESSED   | MEDIUM   | A-002 ACCEPT both variants: bcrypt cost 12, hash-time <500ms. Neither variant models the legacy-migration path where some users may have NULL hashes during cutover. Throw vs false-return distinguishes timing leak from secure denial. |

## Summary

- Total findings: 22
- ADDRESSED: 2 (INV-003, INV-014)
- UNADDRESSED: 20
  - HIGH: 11 (INV-001, INV-002, INV-004, INV-007, INV-010, INV-013, INV-016, INV-017, INV-018, INV-019, INV-020)
  - MEDIUM: 8 (INV-005, INV-006, INV-008, INV-011, INV-015, INV-021, INV-022, plus INV-003/INV-014 which are ADDRESSED MEDIUMs)
  - LOW: 2 (INV-009, INV-012)

Category coverage:
- state_variables: INV-001, INV-002, INV-003 (3)
- guard_conditions: INV-004, INV-005, INV-006, INV-022 (4)
- count_divergence: INV-007, INV-008, INV-009 (3)
- collection_boundaries: INV-010, INV-011, INV-012 (3)
- interaction_effects: INV-013, INV-014, INV-015, INV-016, INV-017 (5)
- sufficiency_challenge: INV-018, INV-019, INV-020, INV-021 (4)

11 HIGH UNADDRESSED items exceed the protocol's "at least 3 HIGH UNADDRESSED" threshold; convergence is blocked until consensus addresses lockout-state-on-Redis-flush (INV-001/INV-017), audit durability (INV-002), refresh-token malformed-guard collision (INV-004), 5-fail off-by-one (INV-007), refresh cap eviction vs block (INV-010), multi-device lockout UX (INV-013), feature-flag flip half-state (INV-016), p95 sensitivity (INV-018), per-account DoS mitigation (INV-019), and legacy rollback ownership (INV-020).

## Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|------------------|
| S-001 (Milestone count, M0) | Variant 1 (Opus) | 70% | V2 R2 partial concession on formal readiness gate value, but M0-as-milestone disputed; debate settles on "lightweight readiness gate" — Opus's structural framing prevails with caveat. |
| S-002 (Total duration 11 vs 9 wk) | Unresolved | 50% | Tied to C-001 effort dispute; both framings (capacity vs marginal) presented as valid in V2 R2 §1; no concession either direction. |
| S-003 (YAML frontmatter) | Variant 1 (Opus) | 85% | V2 R1 §2.6 steelman explicitly credits machine-readable structure as enabling automated pipeline tracking; no rebuttal. |
| S-004 (Workstream count 5 vs 4) | Unresolved | 50% | Sonnet defends 4-stream simplicity (R1 §3.4); Opus defends 5-stream + handoff matrix; no concession either direction. |
| S-005 (Appendix B matrix vs Gantt) | Unresolved | 55% | Both unique contributions are complementary per V2 R2 §3.3; no winner declared. |
| S-006 (Phase Gates depth) | Variant 1 (Opus) | 65% | Opus's table A-D + flag table + rollback is more structured; no Sonnet rebuttal post-Round 1. |
| C-001 (48 EW vs 16 EW) | Unresolved | 50% | V2 R2 §1 explicitly frames as "both valid" (capacity vs marginal-cost); merged output should present both per V2 concession. |
| C-002 (Foundation work) | Variant 1 (Opus) | 75% | V2 R2 partial concession on formal readiness gate value; Opus drops effort from 8→6 EW but retains 6 auth-owned deliverables. |
| C-003 (Coverage targets 85 vs 80) | Variant 2 (Sonnet) | 60% | V2 R2 counter that drift mechanism is hypothetical for additive-code structure stands unrebutted; Opus R2 defense weakened. |
| C-004 (Refresh cap 10 vs 5) | Unresolved | 50% | Probe INV-010 unresolved; neither variant addresses eviction-vs-block semantics; cap deltas explicitly noted as unresolved in probe header. |
| C-005 (Roles cap 16 vs 10) | Unresolved | 50% | Probe INV-011 unresolved; cap deltas listed as unresolved in probe header. |
| C-006 (Lockout cooldown 15 vs 30 min) | Variant 2 (Sonnet) | 90% | Opus R2 §2 explicit concession: "attacker must wait twice as long — concede this default." |
| C-007 (Risk register breadth) | Variant 1 (Opus) | 80% | V2 R1 §2.4 steelman credits broader register (R-007, R-008); no rebuttal; Opus retains R-001..R-008 vs Sonnet's 7. |
| C-008 (Enumeration timing budgets) | Variant 1 (Opus) | 95% | V2 R2 §1 full concession: "merged output should adopt Opus's quantitative timing-variance ATs verbatim" + final concession §1. |
| C-009 (Rollout phase timing) | Variant 1 (Opus) | 95% | V2 R2 §2 + final concession §2: "1-week Beta was incorrect given TDD's explicit Phase 2 duration." TDD §19.1 fidelity defect. |
| C-010 (Token removal date 06-23 vs 06-29) | Unresolved | 50% | Low-severity delta; not debated in either round. |
| C-011 (Workstream owners) | Unresolved | 50% | Tied to S-004 workstream-count disagreement; no concession. |
| C-012 (Post-launch review cadence) | Unresolved | 50% | Low-severity delta; not debated. |
| X-001 (Project start date) | Unresolved | 50% | Tied to S-002 duration dispute; no concession. |
| X-002 (Total EW 48 vs 16) | Unresolved | 50% | V2 R2 §1 explicit: "both framings valid — capacity vs marginal." Merged output should present both. |
| X-003 (Refresh-token limit 10 vs 5) | Unresolved | 50% | See C-004 + INV-010 probe; cap delta unresolved. |
| X-004 (Roles cap 16 vs 10) | Unresolved | 50% | See C-005 + INV-011 probe; cap delta unresolved. |
| X-005 (Lockout cooldown semantics) | Variant 2 (Sonnet) | 85% | Opus R2 §2 concession on 30-min cooldown default. |
| X-006 (Async-reset decision date) | Unresolved | 50% | Low-severity delta; not debated. |
| X-007 (NFR-PERF-001 milestone) | Variant 1 (Opus) | 75% | Opus R1 §4.7 evidence (p95 gated M1/M2/M5) unrebutted by Sonnet; Sonnet's M5-only attribution risks late detection. |
| X-008 (M1 effort vs scope) | Unresolved | 50% | V2 R2 §1 counter-evidence stands (4 EW per complex deliverable is reasonable sprint velocity); Opus retains "commensurate" claim. |
| U-001 (M0 foundation milestone) | Variant 1 (Opus) | 70% | V2 R1 §2.1 steelman explicitly credits; V2 R2 concedes readiness gate value but disputes milestone framing. |
| U-002 (Handoff matrix H1-H10) | Variant 1 (Opus) | 95% | V2 R2 §1 full concession + final concession §3: "handoff matrix adds real coordination value... should be adopted." |
| U-003 (Component build-order) | Variant 2 (Sonnet) | 80% | Opus R2 §4.1 explicit concession: "too prescriptive... should be advisory." Validates Sonnet's R1 §4.4 critique. |
| U-004 (Quantitative timing ATs) | Variant 1 (Opus) | 95% | V2 R2 final concession §1: "Timing-variance ATs should be adopted from Opus verbatim — single most important adoption." |
| U-005 (RS256 rotation runbook) | Variant 1 (Opus) | 75% | Opus R2 partial concession (rename to "planned + emergency," defer quarterly schedule) but runbook artifact retained; Sonnet concedes 24h overlap value. |
| U-006 (Component → Milestone matrix) | Variant 1 (Opus) | 65% | Unique contribution; not directly rebutted; complementary to Sonnet's Gantt. |
| U-007 (Open-Q escalation protocol) | Variant 1 (Opus) | 95% | V2 R2 §1 full concession + final concession §5: "concede and adopt — simple, effective mechanism." |
| U-008 (R-006 conversion-rate risk) | Variant 2 (Sonnet) | 95% | Opus R2 §2 + final concession §3: "must be adopted unmodified — strict superset improvement." |
| U-009 (Gantt visualization) | Variant 2 (Sonnet) | 70% | V1 R1 §5 implicit concession on reader-cost; V2 R2 §3.3 demonstrates Gantt enables critical-path integrity check. |
| U-010 (Micro-benchmark gates) | Unresolved | 55% | Opus R2 §2 partial walk-back: "adopt Sonnet's target numbers but Opus's measurement rigor." Neither variant fully wins. |
| A-001 (7-day refresh TTL) | Shared assumption | 90% | Both variants ACCEPT/QUALIFY (V1 ACCEPT, V2 QUALIFY); aligned on adoption with revisit caveat. |
| A-002 (bcrypt cost 12) | Shared assumption | 95% | Both ACCEPT; full alignment. |
| A-003 (p95 < 200ms achievability) | Shared assumption | 80% | Both QUALIFY; aligned on caveat but probe INV-018 escalates. |
| A-004 (SendGrid latency) | Shared assumption | 80% | Both QUALIFY; aligned on caveat. |
| A-005 (Redis-down universal re-login) | Shared assumption | 80% | Both QUALIFY; aligned. |
| A-006 (Lockout DoS) | Shared assumption disputed | 50% | Both REJECT but no concrete mitigation lands in consensus per INV-019. |
| A-007 (Quarterly RS256 rotation) | Shared assumption | 80% | Both QUALIFY; aligned with V1 R2 deferring quarterly execution. |
| A-008 (Legacy auth rollback viability) | Unresolved | 50% | V1 QUALIFY, V2 ACCEPT — divergent responses; probe INV-020 escalates. |

## Convergence Assessment

- Total diff points: 6 (S) + 12 (C) + 8 (X) + 10 (U) + 8 (A) = 44
- Agreed points (winner is NOT "Unresolved" or "Shared assumption disputed"): 22
  - Resolved with winner: S-001, S-003, S-006, C-002, C-003, C-006, C-007, C-008, C-009, X-005, X-007, U-001, U-002, U-003, U-004, U-005, U-006, U-007, U-008, U-009 (20)
  - Shared assumptions aligned: A-001, A-002, A-003, A-004, A-005, A-007 (6)
  - Total agreed = 26
- Unresolved/disputed: S-002, S-004, S-005, C-001, C-004, C-005, C-010, C-011, C-012, X-001, X-002, X-003, X-004, X-006, X-008, U-010, A-006, A-008 (18)
- Convergence = 26 / 44 = 59.1%

Reporting:
- Points resolved: 26 of 44
- Alignment: 59.1%
- Threshold: 80.0%
- Taxonomy Coverage Check:
  - L1 (surface/naming/formatting): COVERED — S-003 (YAML frontmatter), S-005 (Appendix style), C-011 (owner naming)
  - L2 (structural/workstreams/milestones): COVERED — S-001, S-004, S-006, C-002, U-001, U-002
  - L3 (state-mechanics/lockout/refresh/state): COVERED — C-004, C-005, C-006, X-003, X-004, X-005, A-006, plus extensive probe coverage INV-001/INV-007/INV-008/INV-010/INV-011/INV-013/INV-017
- Invariant Probe Gate Check: 11 HIGH UNADDRESSED findings (INV-001, INV-002, INV-004, INV-007, INV-010, INV-013, INV-016, INV-017, INV-018, INV-019, INV-020) — exceeds threshold of 0; gate is BLOCKED.
- **Status: BLOCKED_BY_INVARIANTS**
- Unresolved/blocking points (diff-level): S-002, S-004, S-005, C-001, C-004, C-005, C-010, C-011, C-012, X-001, X-002, X-003, X-004, X-006, X-008, U-010, A-006, A-008
- Blocking invariants (HIGH UNADDRESSED): INV-001, INV-002, INV-004, INV-007, INV-010, INV-013, INV-016, INV-017, INV-018, INV-019, INV-020

Note: Even if diff-point alignment were above 80%, the 11 HIGH UNADDRESSED invariant findings would still force BLOCKED_BY_INVARIANTS status per the protocol's invariant-probe gate. Here, alignment is 59.1% (below 80%) AND invariants are blocked — convergence fails on both axes, with invariants as the dominant gate.
