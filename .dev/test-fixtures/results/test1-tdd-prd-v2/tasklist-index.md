# TASKLIST INDEX -- User Authentication Service Merged Project Roadmap

## Metadata & Artifact Paths

| Field | Value |
|---|---|
| Sprint Name | User Authentication Service — Merged Project Roadmap |
| Generator Version | Roadmap->Tasklist Generator v4.0 |
| Generated | 2026-04-03 |
| TASKLIST_ROOT | `.dev/test-fixtures/results/test1-tdd-prd-v2/` |
| Total Phases | 3 |
| Total Tasks | 44 |
| Total Deliverables | 52 |
| Complexity Class | HIGH |
| Primary Persona | Alex (End User) |
| Consulting Personas | Sam (API Consumer), Jordan (Platform Admin) |

**Artifact Paths**

| Asset | Path |
|---|---|
| This file | `.dev/test-fixtures/results/test1-tdd-prd-v2/tasklist-index.md` |
| Phase 1 Tasklist | `.dev/test-fixtures/results/test1-tdd-prd-v2/phase-1-tasklist.md` |
| Phase 2 Tasklist | `.dev/test-fixtures/results/test1-tdd-prd-v2/phase-2-tasklist.md` |
| Phase 3 Tasklist | `.dev/test-fixtures/results/test1-tdd-prd-v2/phase-3-tasklist.md` |
| Execution Log | `.dev/test-fixtures/results/test1-tdd-prd-v2/execution-log.md` |
| Checkpoint Reports | `.dev/test-fixtures/results/test1-tdd-prd-v2/checkpoints/` |
| Evidence Directory | `.dev/test-fixtures/results/test1-tdd-prd-v2/evidence/` |
| Artifacts Directory | `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/` |
| Validation Reports | `.dev/test-fixtures/results/test1-tdd-prd-v2/validation/` |
| Feedback Log | `.dev/test-fixtures/results/test1-tdd-prd-v2/feedback-log.md` |

## Phase Files

| Phase | File | Phase Name | Task IDs | Tier Distribution |
|---|---|---|---|---|
| 1 | phase-1-tasklist.md | Core Authentication — Internal Alpha | T01.01-T01.27 | STRICT: 12, STANDARD: 10, LIGHT: 2, EXEMPT: 3 |
| 2 | phase-2-tasklist.md | Password Reset, Compliance, and Beta | T02.01-T02.09 | STRICT: 5, STANDARD: 3, LIGHT: 0, EXEMPT: 1 |
| 3 | phase-3-tasklist.md | GA Rollout and Stabilization | T03.01-T03.08 | STRICT: 3, STANDARD: 2, LIGHT: 1, EXEMPT: 2 |

## Source Snapshot

- 3-phase roadmap for User Authentication Service (login, registration, JWT tokens, password reset, audit logging)
- Merged from adversarial debate between Opus Architect and Haiku Architect (convergence 0.72)
- 6-week timeline with progressive delivery (Alpha → Beta 10% → GA 100%)
- 5 functional requirements (FR-AUTH-001 through FR-AUTH-005), 8 NFRs, 7 API endpoints
- 9 components: AuthService, PasswordHasher, TokenManager, JwtService, UserRepo (backend); LoginPage, RegisterPage, AuthProvider, ProfilePage (frontend)
- PRD enrichment: 3 personas (Alex, Jordan, Sam), GDPR/SOC2 compliance, success metrics ($2.4M revenue, >60% conversion, <200ms p95)

## Deterministic Rules Applied

- Phases derived from explicit roadmap headings: Phase 1 (Core Auth), Phase 2 (Reset + Beta), Phase 3 (GA)
- Task IDs: T<PP>.<TT> zero-padded format (T01.01 through T03.08)
- 1 task per roadmap item by default; splits only when item contains independently deliverable outputs
- Checkpoints every 5 tasks + end-of-phase (cadence per Section 4.8)
- Deliverable IDs: D-0001 through D-0052 in global appearance order
- Effort computed via keyword matching per Section 5.2.1 (EFFORT_SCORE mapping)
- Risk computed via keyword matching per Section 5.2.2 (RISK_SCORE mapping)
- Tier classification via /sc:task-unified algorithm (STRICT > EXEMPT > LIGHT > STANDARD)
- Verification routing: STRICT → sub-agent, STANDARD → direct test, LIGHT → sanity check, EXEMPT → skip
- MCP requirements per tier (STRICT: Sequential + Serena required)
- Traceability: every R-### → T<PP>.<TT> → D-#### mapped
- TDD enrichment: component names (AuthService, PasswordHasher, TokenManager, JwtService, UserRepo), data models (UserProfile, AuthToken), API endpoints, test artifact IDs (UT-001, IT-001, E2E-001)
- PRD enrichment: persona references (Alex, Jordan, Sam), success metrics (conversion >60%, p95 <200ms, session >30min), compliance (GDPR, SOC2), customer journey verification

## Roadmap Item Registry

| Roadmap Item ID | Phase Bucket | Original Text (<= 20 words) |
|---|---|---|
| R-001 | Phase 1 | Provision PostgreSQL 15+ with UserProfile table schema including GDPR consent fields |
| R-002 | Phase 1 | Provision Redis 7+ cluster for refresh token storage |
| R-003 | Phase 1 | Configure feature flag infrastructure for AUTH_NEW_LOGIN and AUTH_TOKEN_REFRESH |
| R-004 | Phase 1 | Generate RS256 2048-bit RSA key pair for JwtService |
| R-005 | Phase 1 | Set up Docker Compose for local dev |
| R-006 | Phase 1 | Implement PasswordHasher with bcrypt cost factor 12 |
| R-007 | Phase 1 | Implement JwtService with RS256 sign/verify |
| R-008 | Phase 1 | Implement TokenManager for token issuance and refresh |
| R-009 | Phase 1 | Implement UserRepo with CRUD against PostgreSQL |
| R-010 | Phase 1 | Implement AuthService facade orchestrating login registration logout |
| R-011 | Phase 1 | Implement logout in AuthService — revoke refresh token |
| R-012 | Phase 1 | POST /auth/login endpoint with lockout and rate limiting |
| R-013 | Phase 1 | POST /auth/register endpoint with GDPR consent |
| R-014 | Phase 1 | POST /auth/refresh endpoint gated behind feature flag |
| R-015 | Phase 1 | GET /auth/me endpoint returning UserProfile |
| R-016 | Phase 1 | POST /auth/logout endpoint revoking refresh token |
| R-017 | Phase 1 | Audit logging foundation with 12-month retention |
| R-018 | Phase 1 | Implement LoginPage frontend component |
| R-019 | Phase 1 | Implement RegisterPage with GDPR consent checkbox |
| R-020 | Phase 1 | Implement AuthProvider context with silent refresh |
| R-021 | Phase 1 | Implement ProfilePage displaying user data |
| R-022 | Phase 1 | Configure route protection for authenticated pages |
| R-023 | Phase 1 | Configure API Gateway rate limiting per endpoint |
| R-024 | Phase 1 | Configure CORS for frontend origin |
| R-025 | Phase 1 | Implement monitoring: Prometheus metrics, Grafana dashboards, OpenTelemetry |
| R-026 | Phase 1 | Security checkpoint review of crypto components |
| R-027 | Phase 1 | Manual testing of all auth flows with bug fix |
| R-028 | Phase 2 | POST /auth/reset-request sends reset token via SendGrid |
| R-029 | Phase 2 | POST /auth/reset-confirm validates token and updates password |
| R-030 | Phase 2 | SendGrid email service integration via async queue |
| R-031 | Phase 2 | Admin audit log query API for persona Jordan |
| R-032 | Phase 2 | Compliance and audit readiness with SOC2 validation |
| R-033 | Phase 2 | Production deployment with AUTH_NEW_LOGIN=OFF |
| R-034 | Phase 2 | Beta 10% traffic shift with 7-day monitoring |
| R-035 | Phase 2 | Load testing: 500 concurrent logins, sustained traffic |
| R-036 | Phase 2 | Performance tuning if needed based on load test results |
| R-037 | Phase 3 | Pre-GA penetration testing by external firm |
| R-038 | Phase 3 | Traffic ramp 50% → 100% with AUTH_TOKEN_REFRESH enabled |
| R-039 | Phase 3 | Legacy auth deprecation and code removal |
| R-040 | Phase 3 | Feature flag cleanup: remove AUTH_NEW_LOGIN |
| R-041 | Phase 3 | Runbook validation and on-call rotation setup |
| R-042 | Phase 3 | Success metrics baseline establishment per PRD S19 |
| R-043 | Phase 3 | Documentation: runbook, API docs, troubleshooting, ADR |
| R-044 | Phase 3 | Post-GA stabilization: 99.9% uptime for 7 days |

## Deliverable Registry

| Deliverable ID | Task ID | Roadmap Item ID(s) | Deliverable (short) | Tier | Verification | Intended Artifact Paths | Effort | Risk |
|---:|---:|---:|---|---|---|---|---|---|
| D-0001 | T01.01 | R-001 | UserProfile table with GDPR fields | STRICT | Sub-agent | artifacts/D-0001/spec.md | L | High |
| D-0002 | T01.01 | R-001 | Audit log table with 12-month retention | STRICT | Sub-agent | artifacts/D-0002/spec.md | L | High |
| D-0003 | T01.02 | R-002 | Redis cluster with replication | STRICT | Sub-agent | artifacts/D-0003/spec.md | M | High |
| D-0004 | T01.03 | R-003 | Feature flag configuration | STANDARD | Direct test | artifacts/D-0004/spec.md | S | Low |
| D-0005 | T01.04 | R-004 | RS256 key pair in K8s secrets | STRICT | Sub-agent | artifacts/D-0005/spec.md | S | High |
| D-0006 | T01.05 | R-005 | Docker Compose config | LIGHT | Sanity check | artifacts/D-0006/spec.md | XS | Low |
| D-0007 | T01.06 | R-006 | PasswordHasher component | STRICT | Sub-agent | artifacts/D-0007/spec.md | M | High |
| D-0008 | T01.07 | R-007 | JwtService component | STRICT | Sub-agent | artifacts/D-0008/spec.md | M | High |
| D-0009 | T01.08 | R-008 | TokenManager component | STRICT | Sub-agent | artifacts/D-0009/spec.md | L | High |
| D-0010 | T01.09 | R-009 | UserRepo component | STRICT | Sub-agent | artifacts/D-0010/spec.md | M | Medium |
| D-0011 | T01.10 | R-010 | AuthService facade | STRICT | Sub-agent | artifacts/D-0011/spec.md | L | High |
| D-0012 | T01.11 | R-011 | Logout implementation | STRICT | Sub-agent | artifacts/D-0012/spec.md | S | Medium |
| D-0013 | T01.12 | R-012 | POST /auth/login endpoint | STRICT | Sub-agent | artifacts/D-0013/spec.md | M | High |
| D-0014 | T01.13 | R-013 | POST /auth/register endpoint | STRICT | Sub-agent | artifacts/D-0014/spec.md | M | High |
| D-0015 | T01.14 | R-014 | POST /auth/refresh endpoint | STRICT | Sub-agent | artifacts/D-0015/spec.md | M | High |
| D-0016 | T01.15 | R-015 | GET /auth/me endpoint | STANDARD | Direct test | artifacts/D-0016/spec.md | S | Low |
| D-0017 | T01.16 | R-016 | POST /auth/logout endpoint | STANDARD | Direct test | artifacts/D-0017/spec.md | S | Low |
| D-0018 | T01.17 | R-017 | Audit log writer + OTel spans | STRICT | Sub-agent | artifacts/D-0018/spec.md | M | High |
| D-0019 | T01.18 | R-018 | LoginPage component | STANDARD | Direct test | artifacts/D-0019/spec.md | M | Medium |
| D-0020 | T01.19 | R-019 | RegisterPage component | STANDARD | Direct test | artifacts/D-0020/spec.md | M | Medium |
| D-0021 | T01.20 | R-020 | AuthProvider context | STRICT | Sub-agent | artifacts/D-0021/spec.md | L | High |
| D-0022 | T01.21 | R-021 | ProfilePage component | LIGHT | Sanity check | artifacts/D-0022/spec.md | XS | Low |
| D-0023 | T01.22 | R-022 | Route protection config | STANDARD | Direct test | artifacts/D-0023/spec.md | S | Low |
| D-0024 | T01.23 | R-023 | Rate limiting config | STANDARD | Direct test | artifacts/D-0024/spec.md | M | Medium |
| D-0025 | T01.24 | R-024 | CORS configuration | STANDARD | Direct test | artifacts/D-0025/spec.md | XS | Low |
| D-0026 | T01.25 | R-025 | Prometheus metrics | STANDARD | Direct test | artifacts/D-0026/spec.md | M | Low |
| D-0027 | T01.25 | R-025 | Grafana dashboards | STANDARD | Direct test | artifacts/D-0027/spec.md | M | Low |
| D-0028 | T01.26 | R-026 | Security review report | STRICT | Sub-agent | artifacts/D-0028/spec.md | M | High |
| D-0029 | T01.27 | R-027 | Manual test report (13 scenarios) | STANDARD | Direct test | artifacts/D-0029/spec.md | L | Medium |
| D-0030 | T02.01 | R-028 | POST /auth/reset-request endpoint | STRICT | Sub-agent | artifacts/D-0030/spec.md | L | High |
| D-0031 | T02.02 | R-029 | POST /auth/reset-confirm endpoint | STRICT | Sub-agent | artifacts/D-0031/spec.md | M | High |
| D-0032 | T02.03 | R-030 | SendGrid integration + monitoring | STANDARD | Direct test | artifacts/D-0032/spec.md | M | Medium |
| D-0033 | T02.04 | R-031 | Admin audit log query API | STRICT | Sub-agent | artifacts/D-0033/spec.md | M | High |
| D-0034 | T02.05 | R-032 | Compliance validation report | STRICT | Sub-agent | artifacts/D-0034/spec.md | M | High |
| D-0035 | T02.06 | R-033 | Production deployment | STRICT | Sub-agent | artifacts/D-0035/spec.md | L | High |
| D-0036 | T02.07 | R-034 | Beta 10% traffic with routing | STRICT | Sub-agent | artifacts/D-0036/spec.md | XL | High |
| D-0037 | T02.07 | R-034 | 7-day monitoring report | STRICT | Sub-agent | artifacts/D-0037/spec.md | XL | High |
| D-0038 | T02.08 | R-035 | Load test report (k6) | STANDARD | Direct test | artifacts/D-0038/spec.md | L | Medium |
| D-0039 | T02.09 | R-036 | Performance tuning report | STANDARD | Direct test | artifacts/D-0039/spec.md | M | Medium |
| D-0040 | T03.01 | R-037 | Penetration test report | STRICT | Sub-agent | artifacts/D-0040/spec.md | L | High |
| D-0041 | T03.02 | R-038 | GA traffic ramp results | STRICT | Sub-agent | artifacts/D-0041/spec.md | M | High |
| D-0042 | T03.03 | R-039 | Legacy deprecation evidence | STRICT | Sub-agent | artifacts/D-0042/spec.md | M | High |
| D-0043 | T03.04 | R-040 | Feature flag cleanup | EXEMPT | Skip | artifacts/D-0043/spec.md | S | Low |
| D-0044 | T03.05 | R-041 | Runbook validation report | STANDARD | Direct test | artifacts/D-0044/spec.md | M | Medium |
| D-0045 | T03.05 | R-041 | On-call rotation schedule | STANDARD | Direct test | artifacts/D-0045/spec.md | M | Medium |
| D-0046 | T03.06 | R-042 | Success metrics baseline report | EXEMPT | Skip | artifacts/D-0046/spec.md | S | Low |
| D-0047 | T03.07 | R-043 | Operations runbook | STANDARD | Direct test | artifacts/D-0047/spec.md | M | Low |
| D-0048 | T03.07 | R-043 | API documentation (OpenAPI) | STANDARD | Direct test | artifacts/D-0048/spec.md | M | Low |
| D-0049 | T03.07 | R-043 | Troubleshooting guide | STANDARD | Direct test | artifacts/D-0049/spec.md | M | Low |
| D-0050 | T03.07 | R-043 | Architecture decision record | STANDARD | Direct test | artifacts/D-0050/spec.md | M | Low |
| D-0051 | T03.08 | R-044 | Stabilization report | STANDARD | Direct test | artifacts/D-0051/spec.md | L | Medium |
| D-0052 | T03.08 | R-044 | Post-mortem (if incidents) | STANDARD | Direct test | artifacts/D-0052/spec.md | L | Medium |

## Traceability Matrix

| Roadmap Item ID | Task ID(s) | Deliverable ID(s) | Tier | Confidence | Artifact Paths (rooted) |
|---:|---:|---:|---|---|---|
| R-001 | T01.01 | D-0001, D-0002 | STRICT | 95% | artifacts/D-0001/, artifacts/D-0002/ |
| R-002 | T01.02 | D-0003 | STRICT | 85% | artifacts/D-0003/ |
| R-003 | T01.03 | D-0004 | STANDARD | 80% | artifacts/D-0004/ |
| R-004 | T01.04 | D-0005 | STRICT | 95% | artifacts/D-0005/ |
| R-005 | T01.05 | D-0006 | LIGHT | 85% | artifacts/D-0006/ |
| R-006 | T01.06 | D-0007 | STRICT | 95% | artifacts/D-0007/ |
| R-007 | T01.07 | D-0008 | STRICT | 95% | artifacts/D-0008/ |
| R-008 | T01.08 | D-0009 | STRICT | 95% | artifacts/D-0009/ |
| R-009 | T01.09 | D-0010 | STRICT | 85% | artifacts/D-0010/ |
| R-010 | T01.10 | D-0011 | STRICT | 95% | artifacts/D-0011/ |
| R-011 | T01.11 | D-0012 | STRICT | 85% | artifacts/D-0012/ |
| R-012 | T01.12 | D-0013 | STRICT | 95% | artifacts/D-0013/ |
| R-013 | T01.13 | D-0014 | STRICT | 95% | artifacts/D-0014/ |
| R-014 | T01.14 | D-0015 | STRICT | 95% | artifacts/D-0015/ |
| R-015 | T01.15 | D-0016 | STANDARD | 80% | artifacts/D-0016/ |
| R-016 | T01.16 | D-0017 | STANDARD | 80% | artifacts/D-0017/ |
| R-017 | T01.17 | D-0018 | STRICT | 95% | artifacts/D-0018/ |
| R-018 | T01.18 | D-0019 | STANDARD | 80% | artifacts/D-0019/ |
| R-019 | T01.19 | D-0020 | STANDARD | 80% | artifacts/D-0020/ |
| R-020 | T01.20 | D-0021 | STRICT | 85% | artifacts/D-0021/ |
| R-021 | T01.21 | D-0022 | LIGHT | 85% | artifacts/D-0022/ |
| R-022 | T01.22 | D-0023 | STANDARD | 80% | artifacts/D-0023/ |
| R-023 | T01.23 | D-0024 | STANDARD | 80% | artifacts/D-0024/ |
| R-024 | T01.24 | D-0025 | STANDARD | 80% | artifacts/D-0025/ |
| R-025 | T01.25 | D-0026, D-0027 | STANDARD | 80% | artifacts/D-0026/, artifacts/D-0027/ |
| R-026 | T01.26 | D-0028 | STRICT | 95% | artifacts/D-0028/ |
| R-027 | T01.27 | D-0029 | STANDARD | 80% | artifacts/D-0029/ |
| R-028 | T02.01 | D-0030 | STRICT | 95% | artifacts/D-0030/ |
| R-029 | T02.02 | D-0031 | STRICT | 95% | artifacts/D-0031/ |
| R-030 | T02.03 | D-0032 | STANDARD | 80% | artifacts/D-0032/ |
| R-031 | T02.04 | D-0033 | STRICT | 95% | artifacts/D-0033/ |
| R-032 | T02.05 | D-0034 | STRICT | 85% | artifacts/D-0034/ |
| R-033 | T02.06 | D-0035 | STRICT | 85% | artifacts/D-0035/ |
| R-034 | T02.07 | D-0036, D-0037 | STRICT | 85% | artifacts/D-0036/, artifacts/D-0037/ |
| R-035 | T02.08 | D-0038 | STANDARD | 80% | artifacts/D-0038/ |
| R-036 | T02.09 | D-0039 | STANDARD | 65% | artifacts/D-0039/ |
| R-037 | T03.01 | D-0040 | STRICT | 95% | artifacts/D-0040/ |
| R-038 | T03.02 | D-0041 | STRICT | 85% | artifacts/D-0041/ |
| R-039 | T03.03 | D-0042 | STRICT | 85% | artifacts/D-0042/ |
| R-040 | T03.04 | D-0043 | EXEMPT | 95% | artifacts/D-0043/ |
| R-041 | T03.05 | D-0044, D-0045 | STANDARD | 80% | artifacts/D-0044/, artifacts/D-0045/ |
| R-042 | T03.06 | D-0046 | EXEMPT | 85% | artifacts/D-0046/ |
| R-043 | T03.07 | D-0047, D-0048, D-0049, D-0050 | STANDARD | 80% | artifacts/D-0047/ through D-0050/ |
| R-044 | T03.08 | D-0051, D-0052 | STANDARD | 80% | artifacts/D-0051/, artifacts/D-0052/ |
