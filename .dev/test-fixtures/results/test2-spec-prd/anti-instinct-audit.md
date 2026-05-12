---
undischarged_obligations: 0
uncovered_contracts: 3
fingerprint_coverage: 0.67
total_obligations: 1
total_contracts: 6
fingerprint_total: 18
fingerprint_found: 12
generated: "2026-04-03T03:28:14.447775+00:00"
generator: superclaude-anti-instinct-audit
---

## Anti-Instinct Audit Report
### Obligation Scanner

- Total obligations detected: 1
- Discharged: 1
- Undischarged (gate-relevant): 0

### Integration Contract Coverage

- Total contracts: 6
- Covered: 3
- Uncovered: 3

**Uncovered contracts:**
- IC-004: middleware_chain: | `src/middleware/auth-middleware.ts` | Add Bearer token extraction and verification | Integrate token validation into request pipeline | (line 158)
- IC-005: middleware_chain: auth-middleware.ts (line 165)
- IC-006: middleware_chain: 4. auth-middleware.ts      -- depends on token-manager (line 212)

### Fingerprint Coverage

- Total fingerprints: 18
- Found in roadmap: 12
- Coverage ratio: 0.67

**Missing fingerprints** (6):
- `AUTH_SERVICE_ENABLED`
- `JIRA`
- `RBAC`
- `PASETO`
- `CSRF`
- `REST`
