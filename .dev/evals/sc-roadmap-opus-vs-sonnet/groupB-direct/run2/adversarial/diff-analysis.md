# Diff Analysis: Roadmap Comparison

## Metadata

- Generated: 2026-05-22T18:05:00Z
- Variants compared: 2 (variant-1-opus-architect, variant-2-sonnet-architect)
- Source: merged-prd-tdd-user-auth.md (AUTH-MERGED-PRD-TDD)
- Total differences found: 24 (S=4, C=8, X=5, U=12, A=7)
- Categories: structural (4), content (8), contradictions (5), unique (12), shared assumptions (7)

---

## Structural Differences

| # | Area | Variant 1 (Opus) | Variant 2 (Sonnet) | Severity |
|---|------|------------------|---------------------|----------|
| S-001 | Milestone count | 5 milestones (M1–M5) — combines schema + AuthService register/login + audit in M1 | 6 milestones (M1–M6) — splits infrastructure/schema (M1) from AuthService logic (M2) | High |
| S-002 | M1 scope granularity | Heavy M1: schema + audit + register + login + lockout + rate limit + first endpoints | Thin M1: schema + PasswordHasher + audit emitter + Redis + CI scaffolding only | High |
| S-003 | Architect's sequencing rationale section | Has dedicated "Sequencing Rationale (architect's note)" section enumerating 5 non-obvious sequencing decisions with rationale | No equivalent section | Medium |
| S-004 | Deliverable format | Bulleted lists with inline citations to TDD §/PRD § | Tables with explicit "Traceability" column linking each deliverable to source AC/section | Low |

---

## Content Differences

| # | Topic | Variant 1 (Opus) Approach | Variant 2 (Sonnet) Approach | Severity |
|---|-------|----------------------------|------------------------------|----------|
| C-001 | Lockout counter storage | Redis-backed from M1 ("Counter accuracy is a SOC2 control, not a performance optimization") with R-008 risk explicitly tracking horizontal-scale correctness | PostgreSQL `failed_login_count INT` + `locked_until TIMESTAMP` columns on `users` table (D1.1) | High |
| C-002 | Reset-token persistence | PostgreSQL table `reset_tokens` with `user_id FK, expires_at, used_at nullable` (D3.1) | Redis with hashed token, 1-hour TTL, keyed by email (D4.1) | High |
| C-003 | Pen-test scheduling | Scheduled in M4 (parallel with frontend), explicit R-010 mitigation: "1-week slack between pen-test and Phase 3" | Scheduled at start of M5 with 3-day buffer | Medium |
| C-004 | Audit-log retention semantics | Uses 90-day per TDD §7.2 with month-partition + cron drop; explicit OQ-7 flagging PRD-vs-TDD conflict for M5 SOC2 evidence review; proposes split-tables resolution | Uses 12-month per PRD Legal directly; conflict not flagged | Medium |
| C-005 | Constant-time enumeration defense (login) | Explicit "run `PasswordHasher.verify` against a constant dummy hash on miss" (R-002 mitigation) | Implicit only via M5 AC "response time variance <50ms between valid and invalid email" | Medium |
| C-006 | Constant-time enumeration defense (reset) | Explicit "always enqueue email job (drop in worker if unregistered) so request-side latency is identical" (M3 risks) | "identical 200 response; no email sent" — does not address timing-side-channel via downstream work | Medium |
| C-007 | Admin audit-log access | Deferred: "admin tools for Jordan persona… M5 or v1.1 depending on capacity; SOC2 audit access can be DB-direct for v1.0" | Explicit `GET /admin/audit-logs?user_id=&event_type=&from=&to=` endpoint as D4.7 with admin-role gating and pagination | Medium |
| C-008 | Auto-login post-registration | Implicit (PRD says "submit → logged in") but no explicit deliverable | Explicit D2.2: "auto-logs user in (returns access token)" + AC for redirect-to-dashboard <2s | Low |

---

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact |
|---|-------------------|---------------------|---------------------|--------|
| X-001 | Reset-token storage backend | PostgreSQL table (D3.1) | Redis with TTL (D4.1) | High — mutually exclusive design; both cite the spec but neither resolves storage choice |
| X-002 | Lockout-counter storage backend | Redis from M1 (D1.4 "back lockout counters with Redis from M1") | PostgreSQL columns on `users` table (D1.1) | High — drives horizontal-scale correctness AND audit-log accuracy |
| X-003 | Pen-test placement | M4 parallel with frontend ("late security finding that blocks GA is the single highest-impact schedule risk" — R-010) | M5 start with 3-day buffer | Medium — affects critical-path slack |
| X-004 | Audit-log retention period | 90-day on operational table, with proposed split to add 12-month SOC2 subset (OQ-7) | 12-month directly | Medium — V1 internally consistent with TDD §7.2; V2 internally consistent with PRD Legal; both cite their source faithfully |
| X-005 | Whether email + auto-login at registration is one milestone or split | Combined: M1 ships register endpoint, M4 ships UI; no auto-login mention | Split: M2 ships register endpoint with explicit auto-login deliverable; M5 ships UI consuming it | Low — both produce working end state but contract clarity differs |

---

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---------|--------------|-------|
| U-001 | V1 | Dedicated "Sequencing Rationale (architect's note)" section explaining 5 non-obvious sequencing decisions (audit-log in M1, lockout-on-Redis-from-M1, contract-freeze before frontend, pen-test in M4, constant-time anti-enumeration) | High |
| U-002 | V1 | Explicit constant-time path for reset request: "always enqueue email job (drop in worker if unregistered) so request-side latency is identical" | High |
| U-003 | V1 | Explicit constant-time login defense: "run `PasswordHasher.verify` against a constant dummy hash on miss" with 6th-attempt rejection without invoking verify | Medium-High |
| U-004 | V1 | OQ-7 PRD-vs-TDD retention conflict raised with proposed resolution (split-tables: 90-day operational + 12-month SOC2 subset) | High |
| U-005 | V1 | Token denylist of user IDs in Redis checked at `/me` for immediate revoke, with rationale "documented 15-minute residual exposure window" — explicitly deferred to v1.1 | Medium |
| U-006 | V1 | Pen-test scheduled M4 (parallel) — recovers 1-week of critical-path slack | High |
| U-007 | V1 | Bcrypt fallback: "Reduce cost to 11 with security sign-off, or scale `AuthService` horizontally; trade-off documented" (R-006) | Low-Medium |
| U-008 | V1 | Quarterly RS256 key-rotation runbook as M2 deliverable D2.7 with first rotation drill scheduled in M5 | Medium |
| U-009 | V1 | Explicit GDPR `consents` row written by `AuthService.register()` in M1 (database-side) plus M4 UI consent capture | Medium |
| U-010 | V2 | Explicit admin audit-log query endpoint `GET /admin/audit-logs?user_id=&event_type=&from=&to=` with admin-role gating, pagination, and index on `(event_type, timestamp)` — covers PRD admin AC directly | High |
| U-011 | V2 | Concurrent-registration race explicitly handled via DB unique constraint with dedicated AC #9: "Concurrent registration with identical email handled gracefully (first wins, second gets 409; no duplicate rows)" | Medium-High |
| U-012 | V2 | SendGrid pre-warming with SPF/DKIM/DMARC configuration before beta + multi-provider testing (Gmail/Outlook) as deliverability hardening | Medium |

---

## Shared Assumptions

Only UNSTATED preconditions promoted to [SHARED-ASSUMPTION] diff points appear here. STATED assumptions (PostgreSQL 15+, Redis 7+, bcrypt cost 12, RS256, 15-min access TTL, 7-day refresh TTL, etc.) are not promoted.

| # | Assumption | Source Agreement | Impact | Status |
|---|-----------|-------------------|--------|--------|
| A-001 | Single-region deployment is sufficient for v1.0 — Redis and PostgreSQL co-located with `AuthService` pods | Both variants discuss capacity (HPA, pool sizes) without any multi-region or geo-failover concern | Affects failure-domain analysis; SOC2 evidence may require multi-AZ at minimum | UNSTATED |
| A-002 | NTP / clock-sync across pods stays within the 5-second JWT skew tolerance under all conditions | Both variants accept TDD §12's 5-second tolerance without defining "what if NTP drifts beyond 5s during a partition" | If clock skew exceeds 5s, valid tokens reject as invalid — silent reliability hit | UNSTATED |
| A-003 | "5 attempts in 15-minute window" uses a **fixed** window starting at the first failure, not a sliding window | Both variants state the policy identically without defining the window semantics; V2's column `locked_until` + `failed_login_count` implies fixed, but does not say so | Sliding vs fixed materially changes attacker economics: fixed window allows bursts at window boundaries | UNSTATED |
| A-004 | Per-IP rate limits at the API Gateway are an acceptable defense, despite IP sharing via NAT/corporate proxy / mobile carrier-grade NAT | Both apply 10 req/min/IP login + 5 req/min/IP register without addressing legitimate shared-IP populations | Could lock out entire corporate office or carrier mobile cohort; SOC2 customer-impact incident risk | UNSTATED |
| A-005 | Redis AOF persistence is sufficient for refresh-token durability — losing the last N tokens after a Redis crash and forcing re-login is acceptable | Both variants treat Redis as the refresh-token store without addressing "what if Redis loses recent writes" beyond reject-and-force-re-login | Re-login storm at recovery is a non-trivial load event; not capacity-planned in either variant | UNSTATED |
| A-006 | Real-time revocation of access tokens within their 15-minute TTL is **not** required for v1.0 SOC2 compliance | V1 explicitly states this is a "documented 15-minute residual exposure window" and defers denylist to v1.1; V2 doesn't acknowledge it at all | If SOC2 auditor requires immediate revoke on credential compromise, denylist becomes M5-blocking, not v1.1 | UNSTATED (V1 acknowledges, V2 silent — promoted because V2 makes it a true implicit assumption) |
| A-007 | The frontend is a fresh SPA build with no incumbent auth provider — no migration of in-flight sessions from a legacy system to coordinate | Both have rollback-to-legacy in their plans (M5/M6) but neither defines what "legacy" actually is or whether there are migrated sessions | If legacy is real, M5/M6 rollback path is reality-checkable; if legacy is a placeholder, Phase 1 alpha becomes redundant | UNSTATED |

---

## Summary

- Total structural differences: 4 (1 High, 1 High, 1 Medium, 1 Low)
- Total content differences: 8 (2 High, 4 Medium, 2 Low)
- Total contradictions: 5 (2 High, 2 Medium, 1 Low)
- Total unique contributions: 12 (V1=9, V2=3)
- Total shared assumptions surfaced: 7 (UNSTATED: 7, STATED: 0, CONTRADICTED: 0)
- **Highest-severity items**: S-001, S-002, C-001, C-002, X-001, X-002, U-001, U-002, U-004, U-006, U-010, U-011

**Substantial differences:** ~24 differentiating points across 934 lines of variant output. Far above the 10% similarity threshold — debate is warranted.
