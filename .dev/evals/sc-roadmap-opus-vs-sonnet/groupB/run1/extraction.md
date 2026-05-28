---
spec_source: /config/workspace/IronClaude/.dev/eval-roadmap/inputs/merged-prd-tdd-user-auth.md
generated: 2026-05-22T16:28:00Z
generator: sc:roadmap
functional_requirements: 7
nonfunctional_requirements: 7
total_requirements: 14
domains_detected: [backend, security, frontend, performance, testing, devops]
complexity_score: 0.48
complexity_class: MEDIUM
risks_identified: 7
dependencies_identified: 7
success_criteria_count: 8
extraction_mode: standard
input_format_detected: tdd
tdd_signal_score: 11
api_endpoint_count: 6
data_entity_count: 3
pipeline_diagnostics:
  prereq_checks:
    spec_validated: true
    output_collision_resolved: false
    adversarial_skill_present: true
    tier1_templates_found: 0
  contract_validation:
    fields_received: 9
    fields_defaulted: []
    convergence_score: 0.78
    routing_decision: pass
    file_guard_passed: true
  fallback_activated: false
---

# Extraction: User Authentication Service (Merged PRD + TDD)

## Source

- **File**: `/config/workspace/IronClaude/.dev/eval-roadmap/inputs/merged-prd-tdd-user-auth.md`
- **Lines**: 1252
- **Format detected**: TDD (signal score 11 ≥ 5 threshold; 28 numbered headings = +3, 8 TDD-specific section names = +8)
- **Content**: Section 1 = PRD (lines 17–417), Section 2 = TDD (lines 419–1252)

## Functional Requirements

| ID | Description | Domain | Priority | Source |
|----|-------------|--------|----------|--------|
| FR-001 | User login with email and password; returns JWT access + refresh tokens; account lockout after 5 failed attempts in 15 min | backend, security | P0 | L215, L652 |
| FR-002 | New user registration with email uniqueness, password strength enforcement, bcrypt hashing, UserProfile creation | backend, security | P0 | L216, L653 |
| FR-003 | JWT token issuance (15-min access TTL) and refresh (7-day refresh TTL) via TokenManager and JwtService | backend, security | P0 | L217, L654 |
| FR-004 | Authenticated user profile retrieval (`GET /auth/me`) returning UserProfile with id, email, displayName, roles, timestamps | backend | P0 | L218, L655 |
| FR-005 | Self-service password reset via two-step flow (request → email token → confirm with new password); 1-hour token TTL; invalidates all sessions | backend, security | P0 | L219, L656 |
| FR-006 | User logout — ends session immediately and redirects to landing page | backend, security | P1 | L309 |
| FR-007 | Audit event logging — all auth events logged with user ID, timestamp, IP, outcome; queryable by date range and user | backend, security | P1 | L256, L328 |

## Non-Functional Requirements

| ID | Category | Requirement | Constraint | Source |
|----|----------|-------------|------------|--------|
| NFR-001 | Performance | API response time | All auth endpoints < 200ms p95 | L225, L664 |
| NFR-002 | Performance | Concurrent throughput | Sustain 500 concurrent login requests | L225, L665 |
| NFR-003 | Reliability | Service availability | 99.9% uptime over rolling 30-day window | L226, L671 |
| NFR-004 | Security | Password hashing | bcrypt cost factor 12; never stored or logged plaintext | L227, L257, L677 |
| NFR-005 | Security | JWT signing | RS256 with 2048-bit RSA keys; quarterly rotation | L678, L1003 |
| NFR-006 | Compliance | SOC2 audit logging | All auth events logged with 12-month retention | L256 |
| NFR-007 | Compliance | GDPR consent + data minimization | Registration consent timestamp; collect only email, hashed password, displayName | L255, L258 |

## Dependencies

| ID | Description | Type | Affects | Source |
|----|-------------|------|---------|--------|
| DEP-001 | PostgreSQL 15+ for UserProfile + audit log persistence | infrastructure | FR-001 – FR-007 | L179, L788 |
| DEP-002 | Redis 7+ for TokenManager refresh-token storage and revocation | infrastructure | FR-003, FR-005 | L789, L1072 |
| DEP-003 | Node.js 20 LTS runtime | infrastructure | All FRs | L525, L1072 |
| DEP-004 | SendGrid (or equivalent SMTP/API) for password reset emails | external | FR-005 | L178, L723 |
| DEP-005 | bcryptjs library for PasswordHasher | library | FR-001, FR-002, FR-005, NFR-004 | L1074 |
| DEP-006 | jsonwebtoken library for JwtService | library | FR-001, FR-003, FR-004, NFR-005 | L1074 |
| DEP-007 | Frontend routing framework supporting client-side routing | internal | FR-001, FR-002, FR-004 | L163, L180 |

## Success Criteria

| ID | Criterion | Target | Measurable | Derived From | Source |
|----|-----------|--------|------------|--------------|--------|
| SC-001 | Registration conversion rate | > 60% | Yes | FR-002 | L60, L272, L641 |
| SC-002 | Login response time (p95) | < 200ms | Yes | FR-001, NFR-001 | L61, L273, L631 |
| SC-003 | Average session duration | > 30 minutes | Yes | FR-003 | L62, L274 |
| SC-004 | Failed login rate | < 5% of attempts | Yes | FR-001 | L63, L275 |
| SC-005 | Password reset completion rate | > 80% | Yes | FR-005 | L276 |
| SC-006 | Token refresh latency (p95) | < 100ms | Yes | FR-003 | L633 |
| SC-007 | Password hash time | < 500ms | Yes | NFR-004 | L635 |
| SC-008 | Daily active authenticated users | > 1000 within 30 days of GA | Yes | All FRs | L642 |

## Risks

| ID | Risk | Probability | Impact | Affected Reqs | Source |
|----|------|-------------|--------|---------------|--------|
| RISK-001 | Token theft via XSS allows session hijacking | Medium | High | FR-001, FR-003, NFR-005 | L1119 |
| RISK-002 | Brute-force attacks on login endpoint | High | Medium | FR-001, NFR-004 | L1120 |
| RISK-003 | Data loss during migration from legacy auth | Low | High | FR-002, DEP-001 | L1121 |
| RISK-004 | Low registration adoption due to poor UX | Medium | High | FR-002, SC-001 | L284 |
| RISK-005 | Security breach from implementation flaws | Low | Critical | All security FRs | L285 |
| RISK-006 | Compliance failure from incomplete audit logging | Medium | High | FR-007, NFR-006 | L286 |
| RISK-007 | Email delivery failures blocking password reset | Low | Medium | FR-005, DEP-004 | L287 |

## Domain Distribution

| Domain | Percentage | Representative Keywords |
|--------|-----------:|------------------------|
| backend | 35% | API, endpoint, service, controller, REST, schema, route, handler, request, response |
| security | 28% | authentication, authorization, JWT, bcrypt, RS256, OWASP, password, credential, audit log |
| frontend | 13% | LoginPage, RegisterPage, AuthProvider, component, form, validation, render |
| performance | 11% | latency, p95, throughput, concurrent, response time, optimization |
| testing | 8% | unit test, integration test, e2e, Jest, Playwright, Supertest, coverage |
| devops | 5% | monitoring, alerting, feature flag, rollout, runbook, on-call, dashboard |
| documentation | <1% | (mostly inline references; no dedicated docs scope) |

**Domains ≥ 10% representation**: backend, security, frontend, performance (4 domains)

## Complexity Scoring (TDD 7-Factor Formula)

| Factor | Raw | Normalized | Weight | Weighted |
|--------|----:|-----------:|-------:|---------:|
| requirement_count | 14 | 0.28 | 0.20 | 0.056 |
| dependency_depth | 4 (Login → TokenManager → JwtService → DB) | 0.50 | 0.20 | 0.100 |
| domain_spread | 4 / 7 | 0.571 | 0.15 | 0.086 |
| risk_severity | (1×3 + 4×2 + 2×1) / 7 = 1.857 → norm 0.429 | 0.429 | 0.10 | 0.043 |
| scope_size | 1252 lines | 1.000 | 0.15 | 0.150 |
| api_surface | 6 endpoints | 0.20 | 0.10 | 0.020 |
| data_model_complexity | 3 entities + 2 relationships = 5 | 0.25 | 0.10 | 0.025 |

**Total**: 0.480 → **MEDIUM** (0.4 ≤ 0.480 ≤ 0.7) → 5–7 milestones, 1:2 interleave ratio.

## Persona Activation

Confidence calculations:

| Persona | base × domain_weight × coverage_bonus | Confidence |
|---------|--------------------------------------|-----------:|
| backend | 0.7 × 0.35 × (1.0 + 0.1 × 2) | 0.294 |
| security | 0.7 × 0.28 × (1.0 + 0.1 × 1) | 0.216 |
| architect | safe-default generalist (none > 0.3) | n/a |

**Primary**: `architect` (no persona exceeds the 0.3 confidence floor; multi-domain security-critical service → architect is the safe default).
**Consulting**: `backend` (0.294), `security` (0.216).

Note: opus / sonnet variant agents in Wave 2 inherit `architect` as primary persona (per protocol Step 3b model-only expansion).

## TDD-Specific Extraction (Steps 9–15)

### Component Inventory (Step 9)

- **New**: `AuthService`, `TokenManager`, `JwtService`, `PasswordHasher`, `UserRepo`, `LoginPage`, `RegisterPage`, `AuthProvider`, `ProfilePage`
- **Modified**: API Gateway (rate-limit rules: 10/min login, 5/min register, 30/min refresh)
- **Deleted**: legacy auth endpoints (deprecated after Phase 3 GA)

### Migration Phases (Step 10)

| Stage | Environment | Criteria | Rollback Trigger |
|-------|-------------|----------|------------------|
| Phase 1: Internal Alpha | staging | All FR-AUTH-001..005 pass, 0 P0/P1 bugs, 1 week | n/a (staging) |
| Phase 2: Beta 10% | production behind `AUTH_NEW_LOGIN` | p95 < 200ms, error < 0.1%, 2 weeks | latency > 1000ms/5min OR error > 5%/2min |
| Phase 3: GA 100% | production, flags removed | 99.9% uptime over 7 days, 1 week | data corruption in UserProfile |

Rollback steps: disable `AUTH_NEW_LOGIN` → smoke-test legacy → root-cause via logs/traces → restore from backup if UserProfile corrupted → notify + post-mortem ≤ 48h.

### Release Criteria (Step 11)

**Definition of Done**: All FR-AUTH-001..005 verified with tests; ≥80% unit coverage for AuthService/TokenManager/JwtService/PasswordHasher; integration tests pass against real PostgreSQL + Redis; security review (bcrypt cost, RS256 rotation) completed; perf test confirms < 200ms p95 at 500 concurrent.

**Release Checklist**: AuthService deployed to staging + smoke-tested; LoginPage/RegisterPage functional in staging; AuthProvider token refresh verified with 15-min TTL; feature flags configured in prod; runbooks published; monitoring dashboards verified; rollback procedure tested in staging; UserProfile migration script validated; go/no-go sign-off from test-lead + eng-manager.

### Observability (Step 12)

- **Metrics**: `auth_login_total` (counter), `auth_login_duration_seconds` (histogram), `auth_token_refresh_total` (counter), `auth_registration_total` (counter)
- **Alerts**: login failure rate > 20% over 5 min; p95 latency > 500ms; TokenManager Redis connection failures
- **Tracing**: OpenTelemetry spans across AuthService → PasswordHasher → TokenManager → JwtService

### Testing Strategy (Step 13)

| Level | Coverage | Tools | Focus |
|-------|---------:|-------|-------|
| Unit | 80% | Jest, ts-jest | AuthService methods, PasswordHasher, JwtService, TokenManager, UserProfile validation |
| Integration | 15% | Supertest, testcontainers | API request/response cycles, DB ops, Redis token storage |
| E2E | 5% | Playwright | LoginPage flow, RegisterPage flow, AuthProvider refresh, full registration→profile journey |

Environments: Local (Docker Compose PG + Redis), CI (testcontainers), Staging (seeded test accounts).

### API Surface (Step 14)

6 endpoints:

- `POST /auth/login` (no auth, 10/min/IP)
- `POST /auth/register` (no auth, 5/min/IP)
- `GET /auth/me` (Bearer auth, 60/min/user)
- `POST /auth/refresh` (refresh token in body, 30/min/user)
- `POST /auth/reset-request` (no auth)
- `POST /auth/reset-confirm` (reset token in body)

### Data Model Complexity (Step 15)

- **Entities** (3): `UserProfile` (id PK, email UNIQUE, displayName, createdAt, updatedAt, lastLoginAt, roles[]), `AuthToken` (accessToken JWT, refreshToken opaque, expiresIn, tokenType), audit-log records
- **Relationships** (2): `UserProfile.id` ← `AuthToken.userId` (FK), `UserProfile.id` ← audit-log entries

## PRD-Supplementary Context (PRD section, lines 17–417)

| Storage Key | Captured |
|-------------|----------|
| `user_personas` | Alex (End User), Jordan (Platform Admin), Sam (API Consumer) |
| `user_stories` | 9 JTBD entries spanning AUTH-E1 (login/register/logout), AUTH-E2 (token mgmt), AUTH-E3 (profile/reset/audit logs) |
| `success_metrics` | 5 PRD metrics (conversion, p95 latency, session duration, failed login rate, reset completion) — already merged into Success Criteria above |
| `market_constraints` | GDPR (consent + data minimization), SOC2 Type II (audit log, 12-month retention), NIST SP 800-63B (password policy) |
| `release_strategy` | In-scope: register/login/logout/refresh/profile/reset. Out: OAuth/OIDC (v2.0), MFA (v1.1), RBAC (separate PRD), social login. |
| `stakeholder_priorities` | Product (Q2 ship blocks $2.4M personalization revenue), Engineering (clean abstractions for OAuth/MFA future), Security (NIST + SOC2), Compliance (Q3 audit) |
| `acceptance_scenarios` | 4 journeys: First-Time Signup, Returning Login, Password Reset, Profile Management |

## Adversarial Mode (Wave 2)

- **Mode**: multi-roadmap
- **Agents (expanded)**: `opus:architect`, `sonnet:architect`
- **Depth**: standard (2 debate rounds)
- **Orchestrator**: not added (agent count 2 < 3 threshold)
- **Convergence score**: 0.78 (PASS path, ≥ 0.6 threshold)
- **Base variant**: `opus:architect` (selected as base; sonnet contributions merged in)
- **Artifacts dir**: `/config/workspace/IronClaude/.dev/eval-roadmap/groupB/run1/adversarial/`
- **Fallback mode**: false

## Wave Provenance

- Wave 0: prerequisites validated (spec ✓, output dir ✓, sc:adversarial skill ✓, models ✓).
- Wave 1A: skipped (single spec, no `--specs`).
- Wave 1B: standard extraction over 1252-line spec (chunking not required given clear two-section structure — PRD + TDD — read in 4 ranged Reads).
- Wave 2: multi-roadmap adversarial run with opus + sonnet variants → merged.
- Wave 3: roadmap.md + test-strategy.md generated.
- Wave 4: SKIPPED (`--no-validate` flag).
