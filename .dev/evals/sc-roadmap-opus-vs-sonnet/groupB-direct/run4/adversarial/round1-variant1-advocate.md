# Round 1 — Variant 1 (Opus) Advocate Statement

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
