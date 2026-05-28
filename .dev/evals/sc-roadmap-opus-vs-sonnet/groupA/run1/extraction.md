---
artifact_type: extraction
artifact_version: 2.0.0
spec_source: /config/workspace/IronClaude/tests/sc-roadmap/fixtures/sample_spec.md
project_title: User Authentication System
generated_by: sc:roadmap
generated_at: 2026-05-22T16:27:38+00:00
extraction_mode: single-pass
complexity_score: 0.445
complexity_class: MEDIUM
primary_persona: security
primary_persona_confidence: 0.462
consulting_personas: [backend]
domain_distribution:
  security: 55
  backend: 25
  performance: 10
  frontend: 5
  ops: 5
requirement_counts:
  functional: 12
  non_functional: 6
  dependencies: 4
  success_criteria: 5
  risks: 4
pipeline_diagnostics:
  prereq_checks:
    spec_file_exists: true
    spec_file_readable: true
    spec_file_non_empty: true
    output_dir_writable: true
    output_collision: false
    adversarial_skill_installed: true
    multi_roadmap_auto_enabled: false
    agent_models_valid: true
  extraction_pipeline:
    steps_completed: 8
    chunked: false
    deduplication_applied: false
  contract_validation:
    wave_1a_invoked: false
    wave_2_invoked: true
    fields_received: 9
    fields_defaulted: []
    convergence_score: 0.857
    routing_decision: pass
    file_guard_passed: true
    artifacts_dir: /config/workspace/IronClaude/.dev/eval-roadmap/groupA/run1/adversarial/
    base_variant: sonnet:security
    unresolved_conflicts: 3
    invocation_method: skill-direct
  fallback_activated: false
adversarial:
  mode: multi-roadmap
  agents: [opus, sonnet]
  depth: standard
  debate_rounds: 2
  orchestrator_added: false
validation_status: SKIPPED
validation_score: 0.0
---

# Extraction: User Authentication System

## Project Overview

**Title**: User Authentication System
**Summary**: Implement a comprehensive user authentication system with OAuth2, JWT tokens, and role-based access control.
**Source**: `/config/workspace/IronClaude/tests/sc-roadmap/fixtures/sample_spec.md` (67 lines)

## Functional Requirements (12)

| ID | Description | Domain | Priority | Source |
|----|-------------|--------|----------|--------|
| FR-001 | User registration with email verification | security, backend | P1 | L9 |
| FR-002 | Login with JWT token generation | security, backend | P0 | L10 |
| FR-003 | OAuth2 integration (Google, GitHub) | security, backend | P0 | L11 |
| FR-004 | Role-based access control (RBAC) | security | P0 | L12 |
| FR-005 | Password reset via email | security, backend | P1 | L13 |
| FR-006 | Session management with refresh tokens | security, backend | P0 | L14 |
| FR-007 | Two-factor authentication (2FA) | security | P1 | L15 |
| FR-008 | API rate limiting per user | security, backend, performance | P1 | L16 |
| FR-009 | Audit logging for auth events | security, ops | P0 | L17 |
| FR-010 | User profile management | backend | P1 | L18 |
| FR-011 | Admin dashboard for user management | frontend, backend | P2 | L19 |
| FR-012 | Account deactivation workflow | security, backend | P1 | L20 |

## Non-Functional Requirements (6)

| ID | Description | Category | Constraint | Source |
|----|-------------|----------|------------|--------|
| NFR-001 | API response time | performance | <200ms for auth endpoints | L24 |
| NFR-002 | Concurrent session support | scalability | 10,000 concurrent | L25 |
| NFR-003 | OWASP Top 10 compliance | security | OWASP Top 10 | L26 |
| NFR-004 | GDPR compliance for user data | security | GDPR | L27 |
| NFR-005 | Auth service uptime | reliability | 99.9% | L28 |
| NFR-006 | PII encryption | security | At rest + in transit | L29 |

## Domain Distribution

- **Security**: ~55% (auth, encryption, OAuth, RBAC, 2FA, audit, OWASP, GDPR)
- **Backend**: ~25% (APIs, JWT, session management, rate limiting)
- **Performance**: ~10% (latency NFR-001, throughput NFR-002)
- **Frontend**: ~5% (admin dashboard FR-011)
- **Ops**: ~5% (audit logging, uptime)

## Dependencies (4 external)

| ID | Description | Type | Affected | Source |
|----|-------------|------|----------|--------|
| DEP-001 | PostgreSQL 15+ for user data storage | external | FR-001, FR-010, FR-012 | L47 |
| DEP-002 | Redis for session caching | external | FR-006, FR-008 | L48 |
| DEP-003 | SendGrid for email delivery | external | FR-001, FR-005 | L49 |
| DEP-004 | Docker for containerization | external | All FRs (deployment) | L50 |

**Internal dependency chains** (depth 3):

- DEP-003 → FR-001 (email verification) → FR-002 (login) → FR-006 (sessions)
- FR-002 → FR-007 (2FA layered on login)
- FR-004 → FR-011 (admin dashboard requires RBAC)

## Success Criteria (5)

| ID | Description | Derived From | Measurable | Source |
|----|-------------|--------------|------------|--------|
| SC-001 | All FR requirements implemented and tested | FR-001..FR-012 | Yes | L63 |
| SC-002 | OWASP compliance verified via security scan | NFR-003 | Yes | L64 |
| SC-003 | Load testing confirms 10K concurrent sessions | NFR-002 | Yes | L65 |
| SC-004 | OAuth2 flow works for Google and GitHub | FR-003 | Yes | L66 |
| SC-005 | Audit logs capture all auth events | FR-009 | Yes | L67 |

## Risks (4)

| ID | Description | Impact | Probability | Affected | Source |
|----|-------------|--------|-------------|----------|--------|
| RISK-001 | Token theft via XSS | High | Medium | FR-002, FR-006 | L56 |
| RISK-002 | Brute force attacks | High | High | FR-002, FR-008 | L57 |
| RISK-003 | OAuth provider downtime | Medium | Low | FR-003 | L58 |
| RISK-004 | Data breach of PII | Critical | Low | NFR-004, NFR-006 | L59 |

## Complexity Scoring (5-Factor)

| Factor | Raw | Normalized | Weight | Weighted |
|--------|-----|------------|--------|----------|
| requirement_count | 18 | 0.36 | 0.25 | 0.090 |
| dependency_depth | 3 | 0.375 | 0.25 | 0.094 |
| domain_spread | 3 | 0.60 | 0.20 | 0.120 |
| risk_severity | 2.75 | 0.875 | 0.15 | 0.131 |
| scope_size | 67 lines | 0.067 | 0.15 | 0.010 |

**Total complexity score: 0.445 → MEDIUM** (5-7 milestones, 1:2 interleave ratio)

## Persona Selection

- **Primary**: security (confidence 0.462) — dominant domain at 55%
- **Consulting**: backend (confidence 0.193 — domain at 25%)

## Out of Scope

- Biometric authentication
- Hardware security keys
- Custom SSO protocol implementation
