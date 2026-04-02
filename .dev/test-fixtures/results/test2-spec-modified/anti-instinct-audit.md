---
undischarged_obligations: 0
uncovered_contracts: 3
fingerprint_coverage: 0.72
total_obligations: 0
total_contracts: 6
fingerprint_total: 18
fingerprint_found: 13
generated: "2026-03-27T15:53:49.320190+00:00"
generator: superclaude-anti-instinct-audit
---

## Anti-Instinct Audit Report
### Obligation Scanner

- Total obligations detected: 0
- Discharged: 0
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
- Found in roadmap: 13
- Coverage ratio: 0.72

**Missing fingerprints** (5):
- `JIRA`
- `PASETO`
- `UUID`
- `REST`
- `OWASP`
