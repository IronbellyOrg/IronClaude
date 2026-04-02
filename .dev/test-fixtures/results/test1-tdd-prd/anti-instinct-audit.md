---
undischarged_obligations: 4
uncovered_contracts: 4
fingerprint_coverage: 0.69
total_obligations: 4
total_contracts: 8
fingerprint_total: 45
fingerprint_found: 31
generated: "2026-03-31T13:40:12.590317+00:00"
generator: superclaude-anti-instinct-audit
---

## Anti-Instinct Audit Report
### Obligation Scanner

- Total obligations detected: 4
- Discharged: 0
- Undischarged (gate-relevant): 4

**Undischarged obligations:**
- Line 68: `skeleton` in Phase 0: Foundation and Infrastructure (Week 0, 1 week) (**objective:** provision all infrastructure dependencies, finalize security policies, and establish the project skeleton so that component development can proceed without blockers.)
- Line 83: `skeleton` in Phase 0: Foundation and Infrastructure (Week 0, 1 week) (set)
- Line 85: `stubs` in Phase 0: Foundation and Infrastructure (Week 0, 1 week) (auth_new_login)
- Line 170: `stub` in Phase 1: Core Authentication (Week 1–3) (/auth/login)

### Integration Contract Coverage

- Total contracts: 8
- Covered: 4
- Uncovered: 4

**Uncovered contracts:**
- IC-001: strategy_pattern: - [x] Section 15: Testing Strategy — Complete (line 136)
- IC-002: strategy_pattern: 15. [Testing Strategy](#15-testing-strategy) (line 181)
- IC-006: strategy_pattern: ## 15. Testing Strategy (line 644)
- IC-007: strategy_pattern: ### 19.1 Migration Strategy (line 707)

### Fingerprint Coverage

- Total fingerprints: 45
- Found in roadmap: 31
- Coverage ratio: 0.69

**Missing fingerprints** (14):
- `complexity_class`
- `feature_id`
- `spec_type`
- `target_release`
- `quality_scores`
- `auth_login_total`
- `auth_login_duration_seconds`
- `auth_token_refresh_total`
- `auth_registration_total`
- `WHAT`
- `SMTP`
- `NULL`
- `NULLABLE`
- `OWASP`
