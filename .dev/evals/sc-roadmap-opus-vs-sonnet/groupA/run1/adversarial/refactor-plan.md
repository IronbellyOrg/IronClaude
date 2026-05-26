# Refactoring Plan

## Overview

- **Base variant**: Variant B (sonnet:security)
- **Incorporated variants**: Variant A (opus:security) — specific strengths only
- **Change count**: 9 planned changes (7 incorporations + 2 structural modifications + 1 enrichment from invariant probe)
- **Overall risk**: Medium (one structural change: split M4 into M4a/M4b)
- **Review status**: Auto-approved (no --interactive flag)

## Planned Changes

### Change #1: Add STRIDE threat-model deliverable to M1

- **Source variant**: Variant A, D1.1
- **Target location**: Variant B M1 (Foundation & Infrastructure)
- **Integration approach**: Append as new deliverable D1.6 in M1
- **Rationale**: U-001 (High value) — produces a reference artifact each subsequent milestone updates. Hybrid resolution of X-002: STRIDE as deliverable, not separate milestone.
- **Risk level**: Low (additive, no restructuring)

### Change #2: Add secret/key rotation policy to M1

- **Source variant**: Variant A, D1.3
- **Target location**: Variant B M1
- **Integration approach**: Append as new deliverable D1.7 in M1
- **Rationale**: U-003 (Medium value) — A's "90-day rotation cycle" is more rigorous than B's "rotation procedure documented." Often deferred and forgotten.
- **Risk level**: Low (additive)

### Change #3: Make JWT-shape-lock at V1 explicit

- **Source variant**: Variant A (sequencing rationale from M3 → V1 → M4)
- **Target location**: Variant B V1 (Validation Gate — Core Auth)
- **Integration approach**: Add explicit stop criterion + deliverable note in V1
- **Rationale**: U-002 (High value) — mitigates known real-world bug class (token-shape drift between local and federated paths). Without the explicit JWT-shape-lock framing, V1's role as a gate is implicit and could be relaxed.
- **Risk level**: Low (clarifying existing gate)

### Change #4: Split M4 into M4a (Authorization & Audit) and M4b (Defense)

- **Source variant**: Conceded by Variant B in Round 2 (S-004); structural pattern from Variant A (M5 + M6 split)
- **Target location**: Variant B M4 (Authorization, Audit & Rate Limiting)
- **Integration approach**: Restructure — split M4 (6 deliverables, L effort, RISK-002 High/High) into:
  - **M4a: Authorization (RBAC) & Audit Logging** — D4.1 RBAC + D4.2 audit log + D4.3 audit query + D4.6 GDPR-aware retention (4 deliverables, M effort)
  - **M4b: Defense — Rate Limiting, Lockout, 2FA** — D4.4 rate limit + D4.5 lockout + (new) D4.7 2FA + (new) D4.8 OAuth-callback rate limit (4 deliverables, M effort)
- **Rationale**: S-004 won as Hybrid (both advocates agreed in Round 2). Wide-blast-radius L milestone with RISK-002 (High/High) is split for safer rollout. Reduces blast radius per release.
- **Risk level**: Medium (restructures dependency graph; V2 now depends on M3, M4a, M4b)

### Change #5: Move 2FA from M3 to M4b (defense framing)

- **Source variant**: Variant A (2FA paired with rate-limit as defense)
- **Target location**: Move D3.3 (TOTP 2FA) + D3.5 (strong-auth enforcement) from M3 to M4b
- **Integration approach**: Reassign deliverables; M3 retitled "OAuth2 Federated Identity" (no longer "Federated Identity & Strong Auth")
- **Rationale**: S-003 + X-003 won by A (72% / 70% confidence). B conceded in Round 2. 2FA mitigates RISK-002 (brute force), not federation. Co-locating with rate-limit + lockout creates a coherent defense milestone.
- **Risk level**: Low (deliverable move within sequenced milestones; no new dependencies introduced)

### Change #6: Add session-store outage stop criterion to V2

- **Source variant**: Round 2.5 invariant probe (INV-002)
- **Target location**: V2 stop criteria
- **Integration approach**: Append: "Session-store (Redis) outage degrades gracefully (read-only mode or DB-backed fallback)"
- **Rationale**: INV-002 MEDIUM UNADDRESSED. NFR-005 (99.9% uptime) risk if Redis is single-host. Surfaces the assumption A-004 for explicit handling.
- **Risk level**: Low (validation gate enrichment)

### Change #7: Add empty-roles test to V2 RBAC penetration test

- **Source variant**: Round 2.5 invariant probe (INV-006)
- **Target location**: V2 DV2.3 (RBAC penetration test)
- **Integration approach**: Append acceptance criterion: "Test covers empty-role users (just-registered, pre-grant) — deny-by-default holds"
- **Rationale**: INV-006 MEDIUM UNADDRESSED. Deny-by-default middleware should handle, but no test specified.
- **Risk level**: Low (test addition)

### Change #8: Add explicit OAuth-callback rate-limit deliverable to M4b

- **Source variant**: Round 2.5 invariant probe (INV-008)
- **Target location**: M4b (new D4.8)
- **Integration approach**: Add deliverable: "Rate limit applies to OAuth callback paths (attacker without an account cannot spam FR-003 endpoints)"
- **Rationale**: INV-008 MEDIUM UNADDRESSED. Neither variant explicitly stated OAuth callback was in rate-limit scope.
- **Risk level**: Low (deliverable addition)

### Change #9: Document 2FA + OAuth-only user interaction as out-of-scope

- **Source variant**: Round 2.5 invariant probe (INV-010)
- **Target location**: Decision Summary table
- **Integration approach**: Add row: "2FA + OAuth-only users → future product decision (deferred)"
- **Rationale**: INV-010 LOW UNADDRESSED. Edge case; not a release blocker.
- **Risk level**: Low (documentation)

## Changes NOT Being Made

Transparency — alternatives considered and rejected:

| Diff Point | Variant A Approach | Reason for Rejection |
|------------|--------------------|--------------------|
| S-001 (milestone count) | 7 work + 2 validation (9 total) | B's 5+2 (then split to 6+2) is closer to MEDIUM-complexity center; A's count not justified by complexity score 0.445 |
| S-006 (M2 scope) | Narrow M2 (identity primitives only, no login) | B's shippable-M2 won 78% — delivery-velocity strength A explicitly does not match |
| C-002 / X-001 (CSP timing) | CSP deferred to M6 (defense layer) | B won 88%/90% confidence — CSP and cookies are codependent; deferring leaves RISK-001 partially exposed |
| X-002 (threat-model as separate milestone) | Dedicated M1 = "Threat Model & Security Foundation" | Hybrid resolution: STRIDE as deliverable within M1 foundation, not separate milestone |
| C-001 (threat model framing) | "Foundation with threat model" milestone title | B's foundation-milestone framing kept; STRIDE added as deliverable instead of retitling |

## Risk Summary

| Change | Risk Level | Impact | Rollback |
|--------|-----------|--------|----------|
| #1 STRIDE deliverable | Low | Additive | Remove deliverable D1.6 |
| #2 Key rotation policy | Low | Additive | Remove deliverable D1.7 |
| #3 JWT-shape-lock at V1 | Low | Clarifying | Soften V1 acceptance criteria |
| #4 Split M4 → M4a/M4b | Medium | Restructures dependencies | Merge M4a/M4b back into M4 |
| #5 Move 2FA to M4b | Low | Deliverable move | Move D4.7 back to M3 |
| #6 Session-store stop criterion | Low | Validation enrichment | Remove from V2 |
| #7 Empty-roles test | Low | Test addition | Remove acceptance criterion |
| #8 OAuth-callback rate-limit | Low | Deliverable addition | Remove D4.8 |
| #9 2FA+OAuth-only doc | Low | Documentation | Remove decision row |

## Review Status

- **Approval**: Auto-approved (non-interactive mode)
- **Timestamp**: 2026-05-22T16:27:38+00:00
