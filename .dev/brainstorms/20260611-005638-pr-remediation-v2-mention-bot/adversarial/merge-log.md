# Merge Log

## Metadata

- Base: Variant 2 (sonnet:security)
- Merge date: 2026-06-11
- Changes applied: 8 incorporations + 4 HIGH + 10 MEDIUM invariant resolutions
- Status: **success** (post-merge validation passed; all HIGH invariants closed)

## Changes Applied

| # | Change | Source | Target § | Provenance | Validation |
|---|--------|--------|----------|------------|------------|
| 1 | Split dispatcher/runner host | V2 (synthesis) | §1 | base | host roles separated; resolves X-001/X-003 |
| 2 | Component inventory (re-homed) | V1 | §2 | incorporated | 18 components, SoT paths |
| 3 | Control flow (two-phase) | V1 + synthesis | §3 | incorporated+modified | intent/outcome ordering |
| 4 | Parent resolution + integrity re-check | V1 + V2 | §4 | incorporated | INV-003 |
| 5 | Authz + bypass enumeration | V2 | §5 | base | 7 bypass classes |
| 6 | Injection-as-data + sandbox | V2 | §6 | base | INV-007/015 |
| 7 | ClaudeProcess reuse + allowlist env | V1/V2 | §7 | base+modified | INV-001/SC-7 |
| 8 | Autonomy (lattice-min + HALT) | V2 + INV-006 | §8 | base+modified | human-decision HALT |
| 9 | Two-phase ledger + push budget + SHA-corr | V1 + V3 + synthesis | §9 | incorporated+modified | INV-002/005/011/018 |
| 10 | Ledger-as-SoT + atomic write | V1 + V3 | §10 | incorporated | X-004 |
| 11 | Secret separation (3 creds) | V2 + V3 | §11 | base+modified | INV-001/012 |
| 12 | Reply/resolve (databaseId guards) | net-new + INV-010 | §12 | new | INV-010 |
| 13 | Rate-limit (ETag/backoff) | V3 | §13 | incorporated | NFR-2 |
| 14 | Audit ledger + alerts | V3 + V2 | §14 | incorporated | SC-1/3/4/7 |
| 15 | Deploy/rollback + offline venv | V3 + INV-017 | §15 | incorporated | INV-017 |

## Post-Merge Validation

- **Structural integrity:** ✅ heading hierarchy consistent; 21 sections + reuse map + handoff.
- **Internal references:** ✅ all §/INV/SC/AC/OQ cross-refs resolve.
- **Contradiction re-scan:** ✅ X-001..X-004 resolved (host split; two-phase order; ledger-SoT;
  no agent in daemon). No new contradictions introduced.
- **Invariant gate re-check:** ✅ 4 HIGH all resolved in §16; 0 HIGH-UNADDRESSED remain.

## Summary

- Planned: 15 change-groups · Applied: 15 · Failed: 0 · Skipped: 0.
- Rejected alternatives: V1 one-shot-for-all, V3 daemon-runs-agent, V3 in-memory round state,
  V1 commit-after-act (see refactor-plan §Changes NOT made).
