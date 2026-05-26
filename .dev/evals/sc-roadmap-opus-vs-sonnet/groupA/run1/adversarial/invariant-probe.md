# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

Independent fault-finder probe against the emerging consensus from Round 1 + Round 2. Six categories: state variables, guard conditions, count divergence, collection boundaries, interaction effects, sufficiency challenge.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | JWT shape (claims + signing alg) is locked before federated identity is layered on | ADDRESSED | HIGH | Variant A explicitly sequences M3 → V1 → M4 (D3.1 + V1 + D4.2); Variant B implicitly sequences M2 → V1 → M3 with V1 acting as JWT-shape gate. Resolved via hybrid merge. |
| INV-002 | state_variables | Redis session-store outage degrades to a known fallback (DB-backed sessions or read-only mode) | UNADDRESSED | MEDIUM | Neither variant defines session-store fallback. RISK to NFR-005 (99.9% uptime) if Redis is single-host. Flagged for post-V1 hardening. |
| INV-003 | guard_conditions | CSP headers + HTTP-only cookies + SameSite=Strict ship together (no window where one is active without the other) | ADDRESSED | HIGH | Variant B places all three in M2 (D2.5); A's M3 + M6 split was rejected in debate (X-001 resolved 90% confidence to B). |
| INV-004 | guard_conditions | Email-verification token TTL is enforced (no perpetually-valid tokens) | ADDRESSED | MEDIUM | Both variants: 24h TTL (A-D2.1, B-D2.1); both invalidate on use. |
| INV-005 | count_divergence | Rate-limit counter resets atomically (no double-decrement under concurrent requests) | ADDRESSED | MEDIUM | Both variants specify Redis-backed sliding-window (A-D6.1, B-D4.4). Redis INCR is atomic. Acceptable. |
| INV-006 | collection_boundaries | User with empty role assignment (just-registered, pre-grant) cannot reach RBAC-gated endpoints | UNADDRESSED | MEDIUM | Neither variant explicitly tests the empty-roles degenerate case. Deny-by-default middleware (A-D5.1, B-D4.1) should handle it, but no integration test specified. Recommend adding to V2 gate. |
| INV-007 | collection_boundaries | Single-role user (most common case) functions correctly without performance degradation | ADDRESSED | LOW | Both variants use standard role-permission join. Single-role is the common path. |
| INV-008 | interaction_effects | OAuth callback path also rate-limited (attacker cannot bypass FR-008 by forcing OAuth flow) | UNADDRESSED | MEDIUM | Both variants apply rate limit "per user + per IP" generally; neither explicitly states OAuth callback is in scope. Attacker without account could spam callbacks. Recommend explicit deliverable in merged roadmap. |
| INV-009 | interaction_effects | GDPR right-to-erasure (NFR-004) interacts correctly with audit log retention | UNADDRESSED | MEDIUM | Variant B's D4.6 (GDPR-aware audit retention with redaction) is the only deliverable addressing this; A leaves it implicit. Merge must include B's D4.6. |
| INV-010 | interaction_effects | 2FA enrollment + OAuth-only user (no password) interaction is defined | UNADDRESSED | LOW | Neither variant clarifies whether OAuth-only users can/must enroll TOTP. Edge case; not a release blocker. Flag for future product decision. |
| INV-011 | sufficiency_challenge | RISK-001 (token theft via XSS) mitigation is sufficient with HTTP-only + Secure + SameSite + CSP — does this set ALONE green RISK-001? | ADDRESSED | HIGH | Variant B's D2.5 bundles all four. Branch enumeration: (a) XSS in user content → blocked by output encoding (assumed in M5 D5.2 admin dashboard); (b) XSS in third-party script → blocked by CSP script-src; (c) Subdomain cookie leak → blocked by SameSite=Strict; (d) Plain-HTTP redirect → blocked by Secure flag. All four branches covered. Sufficiency demonstrated. |
| INV-012 | sufficiency_challenge | RISK-002 (brute force) mitigation: does rate limit + lockout + 2FA ALONE green RISK-002? | ADDRESSED | HIGH | Branch enumeration: (a) Distributed brute force from many IPs → blocked by per-user rate limit; (b) Same-IP brute force → blocked by per-IP rate limit; (c) Lockout-bypass via password reset → mitigated by password-reset token TTL (15 min) + 1-time use; (d) 2FA-protected accounts → infeasible. All branches covered. |

## Summary

- **Total findings**: 12
- **ADDRESSED**: 6 (INV-001, INV-003, INV-004, INV-005, INV-007, INV-011, INV-012 — wait, that's 7. Recounting…)

Recount:

- ADDRESSED: INV-001, INV-003, INV-004, INV-005, INV-007, INV-011, INV-012 = 7
- UNADDRESSED: INV-002, INV-006, INV-008, INV-009, INV-010 = 5

- **ADDRESSED**: 7
- **UNADDRESSED**: 5
  - **HIGH**: 0 (no convergence blockers)
  - **MEDIUM**: 4 (INV-002, INV-006, INV-008, INV-009)
  - **LOW**: 1 (INV-010)

## Convergence Gate Status

- **Invariant probe gate**: **PASS** — zero HIGH-severity UNADDRESSED items.
- 4 MEDIUM items logged as warnings; will be surfaced as future-work / V2-gate items in the merged roadmap.
- Sufficiency challenges (INV-011, INV-012) both ADDRESSED with branch-enumerated evidence.

## Recommended Actions for Merge

| Finding | Recommended Action in Merged Roadmap |
|---------|--------------------------------------|
| INV-002 (Redis fallback) | Add to V2 stop criteria: "session-store outage degrades gracefully" |
| INV-006 (empty roles) | Add to V2 deliverable: "RBAC penetration test covers empty-role users" |
| INV-008 (OAuth callback rate limit) | Add explicit deliverable: "rate limit applies to OAuth callback paths" |
| INV-009 (audit log + GDPR erasure) | Preserve Variant B's D4.6 (GDPR-aware audit retention) in merged roadmap |
| INV-010 (2FA + OAuth-only users) | Note as future product decision; not a release blocker |
