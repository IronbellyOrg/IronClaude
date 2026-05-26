# Round 2 — Variant 1 (Opus) Rebuttal

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
