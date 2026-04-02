---
undischarged_obligations: 1
uncovered_contracts: 3
fingerprint_coverage: 0.78
total_obligations: 1
total_contracts: 6
fingerprint_total: 18
fingerprint_found: 14
generated: "2026-03-31T13:59:04.740652+00:00"
generator: superclaude-anti-instinct-audit
---

## Anti-Instinct Audit Report
### Obligation Scanner

- Total obligations detected: 1
- Discharged: 0
- Undischarged (gate-relevant): 1

**Undischarged obligations:**
- Line 95: `mock` in Phase 1: Foundation & Core Authentication (Weeks 1–3) (unit)

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
- Found in roadmap: 14
- Coverage ratio: 0.78

**Missing fingerprints** (4):
- `JIRA`
- `PASETO`
- `CSRF`
- `REST`
