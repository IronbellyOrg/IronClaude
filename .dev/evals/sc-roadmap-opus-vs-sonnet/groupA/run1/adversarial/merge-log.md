# Merge Log

## Metadata

- **Base variant**: Variant B (sonnet:security)
- **Merge executor**: merge-executor (simulated single-agent)
- **Changes planned**: 9
- **Changes applied**: 9
- **Changes failed**: 0
- **Changes skipped**: 0
- **Status**: success
- **Timestamp**: 2026-05-22T16:27:38+00:00
- **Merged output**: `/config/workspace/IronClaude/.dev/eval-roadmap/groupA/run1/adversarial/merged-output.md`

## Changes Applied

| # | Change | Status | Provenance Tag | Validation |
|---|--------|--------|----------------|------------|
| 1 | Add STRIDE threat-model deliverable to M1 (D1.6) | Applied | `<!-- Source: Variant A D1.1 -->` (in M1 deliverable table) | Cross-ref to NFR-003 and Risk Register present |
| 2 | Add secret/key rotation policy to M1 (D1.7) | Applied | `<!-- Source: Variant A D1.3 -->` | 90-day cycle + KMS abstraction documented |
| 3 | Make JWT-shape-lock at V1 explicit (DV1.4) | Applied | `<!-- Source: Variant A sequencing rationale -->` | V1 stop criteria updated |
| 4 | Split M4 into M4a + M4b | Applied | `<!-- Source: Round 2 hybrid resolution of S-004 -->` | Dependency graph updated: M4a + M4b both depend on M2 + V1; V2 depends on M3 + M4a + M4b |
| 5 | Move 2FA (D3.3, D3.5) from M3 to M4b (D4b.3) | Applied | `<!-- Source: Variant A defense framing (S-003/X-003) -->` | M3 retitled "OAuth2 Federated Identity"; 2FA now mitigates RISK-002 alongside rate limit + lockout |
| 6 | Add session-store outage stop criterion to V2 (DV2.5) | Applied | `<!-- Source: Round 2.5 INV-002 -->` | NFR-005 risk surface explicit |
| 7 | Add empty-roles test to V2 RBAC test (DV2.3 ext.) | Applied | `<!-- Source: Round 2.5 INV-006 -->` | Deny-by-default boundary tested |
| 8 | Add OAuth-callback rate-limit deliverable to M4b (D4b.4) | Applied | `<!-- Source: Round 2.5 INV-008 -->` | Closes brute-force-via-OAuth bypass |
| 9 | Document 2FA + OAuth-only users as out-of-scope | Applied | `<!-- Source: Round 2.5 INV-010 -->` | Decision Summary row added |

## Post-Merge Validation

### Structural Integrity

- ✅ Heading hierarchy consistent (no H2 → H4 gaps; H1 → H2 → H3 → H4 properly nested)
- ✅ All milestones include all 4 required sections (Objective, Deliverables, Dependencies, Risk Assessment)
- ✅ Document opens with H1 title, follows roadmap conventions
- ✅ Milestone Summary table includes Effort column

### Internal References

- Total references: 38 (FR/NFR/RISK/SC IDs, M#/V#/D# cross-references)
- Resolved: 38
- Broken: 0
- ✅ PASS

### Contradiction Re-Scan

- Pre-merge contradiction count (across variants): 3 (X-001, X-002, X-003)
- New contradictions introduced by merge: 0
- All 3 pre-merge contradictions resolved in merged output:
  - X-001 (CSP timing): resolved to M2 timing (B's position adopted)
  - X-002 (threat-model milestone): resolved as hybrid (STRIDE deliverable inside foundation milestone)
  - X-003 (2FA placement): resolved to M4b defense framing (A's position adopted)
- ✅ PASS

### Frontmatter Discipline

- No frontmatter on merged-output.md (it is consumed by sc:roadmap Wave 3, which generates its own frontmatter on the final roadmap.md)
- ✅ Per spec sequencing: merged-output.md is the **source** for Wave 3, not the final artifact

## Summary

| Metric | Value |
|--------|-------|
| Changes planned | 9 |
| Changes applied | 9 |
| Changes failed | 0 |
| Changes skipped | 0 |
| New contradictions introduced | 0 |
| Pre-merge contradictions resolved | 3 / 3 |
| Final convergence | 85.7% (above 80% threshold) |
| Status | success |
