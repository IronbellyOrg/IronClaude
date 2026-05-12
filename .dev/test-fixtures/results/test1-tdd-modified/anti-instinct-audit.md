---
undischarged_obligations: 5
uncovered_contracts: 4
fingerprint_coverage: 0.76
total_obligations: 5
total_contracts: 8
fingerprint_total: 45
fingerprint_found: 34
generated: "2026-03-27T15:28:57.000379+00:00"
generator: superclaude-anti-instinct-audit
---

## Anti-Instinct Audit Report
### Obligation Scanner

- Total obligations detected: 5
- Discharged: 0
- Undischarged (gate-relevant): 5

**Undischarged obligations:**
- Line 88: `skeleton` in Phase 1 — Core Infrastructure, Persistence, and Security Primitives (tokenmanager)
- Line 96: `skeleton` in Phase 1 — Core Infrastructure, Persistence, and Security Primitives (tokenmanager)
- Line 96: `skeleton` in Phase 1 — Core Infrastructure, Persistence, and Security Primitives (jwtservice)
- Line 98: `skeleton` in Phase 1 — Core Infrastructure, Persistence, and Security Primitives (, )
- Line 129: `skeleton` in Phase 2 — Backend Auth Domain Services and API Surface (, )

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
- Found in roadmap: 34
- Coverage ratio: 0.76

**Missing fingerprints** (11):
- `complexity_class`
- `feature_id`
- `spec_type`
- `target_release`
- `quality_scores`
- `WHAT`
- `CORS`
- `SMTP`
- `PRIMARY`
- `AUTH_INVALID_CREDENTIALS`
- `OWASP`
