---
complexity_class: HIGH
validation_philosophy: continuous-parallel
validation_milestones: 5
work_milestones: 5
interleave_ratio: 1:1
major_issue_policy: stop-and-fix
spec_source: test-tdd-user-auth.md
generated: "2026-04-20T16:53:56.154324+00:00"
generator: superclaude-roadmap-executor
---

# Test Strategy — User Authentication Service (AUTH-001)

## 1. Validation Milestones (1:1 Interleave with Work Milestones)

| Val ID | Pairs With | Window | Focus |
|---|---|---|---|
| V1 | M1 Foundation | 2026-04-08 → 2026-04-10 | Schema migrations, skeleton compilation, infra smoke, config validation |
| V2 | M2 Core Logic | 2026-04-22 → 2026-04-24 | FR-AUTH-001/002, PasswordHasher, UserRepo, enumeration/timing |
| V3 | M3 Integration | 2026-05-13 → 2026-05-15 | FR-AUTH-003/004/005, TokenManager/JwtService, frontend E2E |
| V4 | M4 Hardening | 2026-05-27 → 2026-05-29 | Pen-test, audit/compliance, observability, load, admin APIs |
| V5 | M5 Production | 2026-06-08 → 2026-06-12 | Phased rollout, rollback drills, post-GA telemetry, SLO verify |

## 2. Test Categories

| Category | Tooling (TDD §15.1) | Coverage Target | Scope |
|---|---|---|---|
| Unit | Jest, ts-jest | ≥80% lines/branches (COVERAGE-GATE) | AuthService, TokenManager, JwtService, PasswordHasher, UserRepo, validators |
| Integration | Supertest + testcontainers (PostgreSQL 15, Redis 7) | 15% pyramid share | API endpoints, DB/Redis wiring, async email worker, partition behavior |
| E2E | Playwright | 5% pyramid share | LoginPage→ProfilePage, RegisterPage→LoginPage redirect (CONFLICT-2), reset flow, silent refresh |
| Contract | OpenAPI 3 + Dredd/Schemathesis | 100% of 7 endpoints | API-001..006, API-009/010/011, error envelope schema |
| Performance | k6 | p95 <200ms at 50/100/250/500 RPS | NFR-PERF-001/002, LOAD-TEST-FULL mixed workload |
| Security | SAST (CI), external pen-test, custom timing probes | 0 High/Critical at V4 | SEC-005/006/AUDIT-TOKEN, OWASP Top 10, JWT confusion, enumeration |
| Compliance | SOC2 evidence replay, GDPR consent assertions | 100% events persisted | NC0, NFR-COMP-001/002/003, 12-mo retention |
| Chaos/Reliability | Toxiproxy / pod-kill | Graceful degradation | Redis-out, PST-out, SendGrid-out (RELIABILITY-READINESS) |
| Accessibility | axe-core on LoginPage/RegisterPage/ProfilePage | 0 serious/critical | Keyboard nav, label association, CAPTCHA fallback |

## 3. Interleaving Strategy & Ratio Justification

**Ratio 1:1 justified by HIGH complexity (0.78):** crypto primitives, dual-store persistence, 5-component orchestration, phased rollout with auto-rollback, and overlapping SOC2/GDPR/NIST frameworks. Every work milestone ships security-critical surface that cannot safely batch — delaying validation past each M# concentrates blast radius at GA.

Each validation window runs in parallel shadow during the work window (continuous) and gates the next milestone via a 2-3 day exit review (parallel). Tests authored in the **same PR** as the feature (TDD/BDD); no separate "test sprint."

## 4. Risk-Based Prioritization

| Priority | Risks Addressed | Test Investment |
|---|---|---|
| P0 (must pass every milestone) | R-002 brute-force, R-004 SOC2 gap, R-005 bcrypt latency, R-PRD-002 security breach | Unit + integration + perf + security across V2-V4 |
| P1 (must pass by V4) | R-001 XSS/token theft, R-003 migration data loss, R-006 key rotation, R-007 SendGrid | Chaos, E2E, rotation drill, DLQ assertion |
| P2 (must pass by V5) | R-010 clock skew, R-011 legacy sunset, R-016 on-call, R-019 refresh cap UX | Drift simulation, synthetic canary, runbook drill |
| P3 (track post-GA) | R-008 CAPTCHA, R-018 rate-limit friction, R-020 flag-debt | Telemetry + A/B in v1.1 |

## 5. Per-Milestone Validation

**V1: Foundation** | 3 days | Exit: migrations apply clean, skeletons compile, configs fail-fast
| Test | ID/Name | Validates |
|---|---|---|
| Migration apply/rollback | DM-001..004 DDL on empty PG15 | Schema parity |
| JWT config boot assertion | NFR-SEC-002 config test | RS256 + 2048-bit fail-fast |
| bcrypt cost boot assertion | NFR-SEC-001 config test | Rejects cost<10 |
| Redis TTL smoke | SET key EX 604800 | DEP-002 AOF persistence |
| CORS preflight | CORS-PREFLIGHT-TEST (M3 early) | INFRA-003 allow-list |
| Log redaction unit | NFR-SEC-003 middleware | password/token never serialized |
| Feature-flag toggle | MIG-004/005 runtime | No-redeploy gating |

Acceptance: all migrations idempotent; secrets mount verified; OQ-CONFLICT-1 closed; ≥90% skeleton coverage placeholders green.

**V2: Core Logic** | 3 days | Exit: FR-AUTH-001/002 green, coverage ≥80% on THS/PSS/SRR, p95 preliminary <200ms
| Test | ID/Name | Validates |
|---|---|---|
| TEST-001 | Unit: login valid credentials | FR-AUTH-001 AC1 |
| TEST-002 | Unit: login invalid credentials | FR-AUTH-001 AC2, counter increment |
| TEST-004 | Integration: register persists UserProfile | FR-AUTH-002 + bcrypt prefix $2b$12$ |
| TEST-DUP-EMAIL | Integration: 409 on duplicate | FR-AUTH-002 AC2, case-insensitive |
| TEST-WEAK-PWD | Integration: NIST rule array | FR-AUTH-002 AC3, SEC-003 |
| Enumeration timing | SEC-004 probe | <50ms variance known vs unknown |
| Bcrypt benchmark | NFR-SEC-001 perf | <500ms/hash on target hw |
| PERF-BASELINE | k6 at 10/25/50 RPS | p95 <200ms preliminary |
| Consent capture | NFR-COMP-001-stub | consentAccepted + timestamp persisted |

Acceptance (Alex persona P0): register in <60s with valid input; invalid→actionable 400 with rule list. Acceptance (KPI): registration success ≥99% in test harness.

**V3: Integration** | 3 days | Exit: FRT/004/005 E2E green; refresh cap=5 enforced; CONFLICT-2 redirect live
| Test | ID/Name | Validates |
|---|---|---|
| TEST-003 | Unit: refresh rotates pair | FR-AUTH-003 AC2 |
| TEST-005 | Integration: expired refresh → 401 | FR-AUTH-003 AC3 |
| TEST-REVOKE | Integration: revoked refresh → 401 | FR-AUTH-003 AC4 |
| TEST-RESET-FLOW | Integration: full reset + session invalidation | FR-AUTH-005 |
| TEST-006 | E2E: register→login→profile | FR-AUTH-001/002/004 |
| TEST-E2E-RESET | E2E: reset journey + old-session logout | FR-AUTH-005 |
| SEC-001 lockout | 5 failures/15min → 423 | PRD R-002, OQ-PRD-3 |
| Refresh cap=5 OE | C0 AC eviction test | OQ-PRD-2 RSL |
| CONFLICT-2 redirect | Playwright assertion | RE3 → /login?email= |
| Clock-skew sim | FE-CLOCK-SKEW | exp-60s refresh |
| NFR-PERF-001-M3 | k6 50/100/250 concurrent | p95 <200ms |
| NFR-PERF-002 | k6 500 concurrent /login | Sustained p95 <200ms |
| Session fixation | Concurrent login test | R-005 mitigation |
| JWT alg confusion | Signed-with-HS256 rejected | SEC-AUDIT-TOKEN |
| CORS-PREFLIGHT-TEST | Origin allow/deny | INFRA-003 |

Acceptance (Sam persona): programmatic refresh VRF via API-004; clear error codes returned; OpenAPI spec matches responses. Acceptance (KPI): reset completion ≥80% in synthetic funnel.

**V4: Hardening** | 3 days | Exit: pen-test 0 High/Critical, SOC2 sample pass, alerts tuned
| Test | ID/Name | Validates |
|---|---|---|
| SEC-005 security review | Formal written report | Token lifecycle + crypto |
| SEC-006 pen-test | External vendor, OWASP Top 10 + JWT | NFR-COMP-002 |
| SEC-AUDIT-TOKEN | RS256-only, iss/aud, revocation atomicity | R-001, R-006 |
| NC0 retention | Insert date+400d → partition pruned | 12-mo OQ-CONFLICT-1 |
| AUDIT-003 field coverage | Every event type to auth_audit_log | NFR-COMP-002, SOC2 |
| NFR-COMP-001 consent | DSAR stub returns consent + profile | GDPR |
| LOAD-TEST-FULL | k6 mixed 500 concurrent × 30 min | NFR-PERF-001/002 |
| RELIABILITY-READINESS | Redis/PST/SendGrid outage injection | TDD §12/§25.1 |
| ORT dry-run | 4 rollback triggers tested staging-shadow | Human-gated for 30d |
| API-009/010 admin lock/unlock | Jordan persona E2E | JTBD-gap-2 |
| API-011 /v1/health | Dep-down returns 503; degraded status | NFR-REL-001 |
| OPS-008-prep alert tuning | 48h shadow FP rate <10% | On-call fatigue |
| SEC-CSP | No inline scripts; report-uri fires | R-001 XSS |
| COVERAGE-GATE | CI gate ≥80% lines/branches | Quality gate |
| axe-core a11y | 0 serious/critical on auth pages | Alex persona |

Acceptance (Jordan persona): audit queries paginate + filter; lock/unlock actions emit audit events. Acceptance (compliance): SOC2 mapping checklist sign-off captured.

**V5: Production Readiness & GA** | 5 days | Exit: 99.9% 7-day uptime, rollback drill pass, post-GA metrics review scheduled
| Test | ID/Name | Validates |
|---|---|---|
| Phased rollout canary | 1%→5%→10% with auto-abort | MIG-002 + ORT |
| Rollback drill | Flag flip + DB restore dry-run | MIG-003 fallback |
| KPI telemetry probes | Registration conversion >60%, p95 <200ms, failed <5% | PRD §Success Metrics |
| Legacy sunset | 410 + Sunset: 2026-09-07 header | OQ-GOV-001, R-011 |
| On-call dry-run | PagerDuty page → 15-min ack | OPS-003 |
| RSA rotation drill | Staging overlap window verified | R-006, RSA-KEY-ROTATION |
| Flag removal CI check | No stale AUTH_NEW_LOGIN refs | FLAG-REMOVAL |
| Post-GA monitoring | 7-day uptime ≥99.9% | NFR-REL-001 |
| GA+30d auto-fire promotion | ORT human-gate → auto | OPS-008 |

Acceptance (release): TDD §24.2 checklist 100%; go/no-go sign-offs from test-lead + eng-manager + security + compliance.

## 6. Quality Gates Between Milestones

| Gate | Blocks | Severity Mapping |
|---|---|---|
| V1→M2 | Core Logic start | CRITICAL: migration fails, skeleton doesn't compile, secrets unmounted |
| V2→M3 | Integration start | CRITICAL: FR-AUTH-001/002 failing, PII in logs. MAJOR: coverage <80%, bcrypt >500ms |
| V3→M4 | Hardening start | CRITICAL: FRT broken, refresh cap bypassed. MAJOR: p95 >200ms at 250 RPS, E2E flakiness >5% |
| V4→M5 | GA rollout | CRITICAL: pen-test High/Critical open, SOC2 gap, rollback fails. MAJOR: alert FP >10%, audit write lag >100ms |
| V5→close | Post-GA-review sign-off | CRITICAL: uptime <99.9%, KPI miss >20%. MAJOR: runbook gaps, cap=5 friction alerts |

**Issue handling:** CRITICAL halts current milestone immediately (stop-and-fix); MAJOR blocks the next milestone (stop-and-fix before gate); MINOR enters v1.1 backlog (V1.1-BACKLOG); COSMETIC goes to grooming. Major-issue-policy: stop-and-fix — no gate bypass.

## 7. Persona & Compliance Coverage Matrix

| Persona / Requirement | V2 | V3 | V4 | V5 |
|---|---|---|---|---|
| Alex (end user, <60s register, seamless session) | TEST-004, TEST-WEAK-PWD | TEST-006, TEST-E2E-RESET | axe-core | KPI conversion probe |
| Jordan (admin audit + lockout) | — | SEC-001 | API-009/010, AUDIT-003 | on-call drill |
| Sam (API consumer programmatic) | — | TEST-003/005, OpenAPI contract | JWT algorithm audit | legacy sunset notice |
| GDPR consent (NFR-COMP-001) | NFR-COMP-001-stub | — | DSAR stub + consent export | — |
| SOC2 audit (NFR-COMP-002, 12-mo) | — | — | NC0 retention test | OPS-005 retention job |
| NIST SP 800-63B (NFR-COMP-003) | TEST-WEAK-PWD | — | conformance checklist | — |
