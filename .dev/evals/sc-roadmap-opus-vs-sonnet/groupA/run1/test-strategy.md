---
spec_source: /config/workspace/IronClaude/tests/sc-roadmap/fixtures/sample_spec.md
generated: 2026-05-22T16:27:38+00:00
generator: sc:roadmap
validation_philosophy: continuous-parallel
validation_milestones: 2
work_milestones: 6
interleave_ratio: "1:2"
major_issue_policy: stop-and-fix
complexity_class: MEDIUM
---

# Test Strategy: Continuous Parallel Validation

## Validation Philosophy

This test strategy implements **continuous parallel validation** — the assumption that work has deviated from the plan, is incomplete, or contains errors until validation proves otherwise.

**Core Principles**:

1. A validation agent runs in parallel behind the work agent, checking completed work against requirements
2. Major issues trigger a stop — work pauses for refactor/fix before continuing
3. Validation milestones are interleaved between work milestones (not batched at the end)
4. Minor issues are logged and addressed in the next validation pass
5. The interleave ratio is **1:2** (one validation milestone per two work milestones), derived from complexity class MEDIUM (score 0.445)

**Roadmap-specific placement**: V1 immediately follows M2 (after the JWT shape is set) so that federated identity (M3) cannot proceed until JWT-shape-lock is verified. V2 follows the parallel cluster (M3, M4a, M4b) and gates M5.

## Validation Milestones

| ID | After Work Milestone(s) | Validates | Stop Criteria |
|----|-------------------------|-----------|---------------|
| V1 | M2 (Core Authentication) | Core auth surface end-to-end; **JWT shape lock-in** before federated identity is introduced | Any Critical CVE; load test < 10K sessions; JWT signing-key handling unsafe; JWT schema not frozen |
| V2 | M3 (OAuth) + M4a (RBAC+Audit) + M4b (Defense) | Full pre-production surface composes correctly; resilience under Redis outage; OAuth callback rate-limited | Any High/Critical CVE; privilege escalation possible; audit log tamperable undetected; session-store outage causes total auth outage; OAuth callback bypasses rate-limit |

**Placement rule**: V1 sits between core auth and federated identity to enforce the JWT-shape-lock invariant. V2 sits between the parallel work cluster (M3/M4a/M4b) and the admin/GDPR milestone (M5) to ensure the full security surface is validated before user-facing admin features are added.

## Issue Classification

| Severity | Action | Threshold | Example |
|----------|--------|-----------|---------|
| Critical | Stop work immediately, fix before any further progress | Any occurrence | JWT signing key leak; SQL injection on auth endpoint; data-loss risk in account deactivation |
| Major | Stop work, refactor/fix before next milestone | >1 occurrence OR blocking | Missing CSP header; broken RBAC deny-by-default; OAuth callback not rate-limited |
| Minor | Log, address in next validation pass | Accumulated count > 5 triggers review | Inconsistent error message format; missing OpenAPI doc on edge endpoint; minor logging gap |
| Info | Log only, no action required | N/A | Optimization opportunity; alternative library available |

## Acceptance Gates

Per-milestone acceptance criteria derived from spec requirements and mapped to deliverables.

| Milestone | Gate Criteria | Pass Condition |
|-----------|--------------|----------------|
| M1 | All 7 deliverables shipped; STRIDE map covers OWASP Top 10; CI gates blocking on PRs; 90-day rotation policy in place | All deliverable ACs met; threat model reviewed by security persona |
| M2 | All 7 deliverables shipped; CSP+cookie protections active; P95 < 200ms | All ACs met; no Critical/Major issues from V1 |
| V1 | OWASP ZAP scan; 10K session load test; JWT-shape-lock ADR | Stop criteria all clear |
| M3 | OAuth Google + GitHub flows working; JWT conforms to V1-locked schema; fallback UI works on provider 5xx | SC-004 met; no JWT-shape drift |
| M4a | RBAC deny-by-default; tamper-evident audit log; GDPR-aware retention | Integration tests pass; SC-005 met |
| M4b | Rate-limit + lockout + 2FA functional; OAuth callback rate-limited | Brute-force simulation blocked at thresholds |
| V2 | Full OWASP re-scan; RBAC pentest (incl. empty-role users); audit integrity; Redis outage drill | All stop criteria clear |
| M5 | Profile + admin + deactivation + GDPR export + GDPR erasure all functional; erasure cascades audit per retention policy | All deliverable ACs met; no Critical/Major issues |

## Validation Coverage Matrix

| Requirement | Validated By | Milestone | Method |
|-------------|--------------|-----------|--------|
| FR-001 (Registration + email verify) | V1 DV1.1 (OWASP) | M2 | Functional + security scan |
| FR-002 (Login + JWT) | V1 DV1.3 + DV1.4 | M2 | Code review + schema freeze |
| FR-003 (OAuth2) | V2 DV2.1 | M3 | OWASP re-scan + SC-004 manual test |
| FR-004 (RBAC) | V2 DV2.3 | M4a | Penetration test (incl. empty-role users) |
| FR-005 (Password reset) | V1 DV1.1 | M2 | OWASP scan |
| FR-006 (Session mgmt) | V1 DV1.2 + V2 DV2.5 | M2 | Load test (10K) + Redis outage drill |
| FR-007 (2FA) | V2 DV2.2 | M4b | Brute-force simulation |
| FR-008 (Rate limiting) | V2 DV2.2 | M4b | Brute-force simulation (incl. OAuth path) |
| FR-009 (Audit logging) | V2 DV2.4 | M4a | Tamper-detection test |
| FR-010 (Profile mgmt) | M5 acceptance gate | M5 | Functional test |
| FR-011 (Admin dashboard) | M5 acceptance gate | M5 | Functional + audit-trail verification |
| FR-012 (Deactivation) | M5 acceptance gate | M5 | Functional + GDPR cascade test |
| NFR-001 (<200ms) | V1 DV1.2 | M2 | Load test P95 measurement |
| NFR-002 (10K concurrent) | V1 DV1.2 | M2 | Load test sustained 30 min |
| NFR-003 (OWASP) | V1 DV1.1 + V2 DV2.1 | M2, full | OWASP ZAP automated scan |
| NFR-004 (GDPR) | V2 DV2.3 + M5 gate | M4a, M5 | Retention policy + erasure cascade test |
| NFR-005 (99.9% uptime) | V2 DV2.5 + M1 D1.5 | M1, V2 | Observability baseline + Redis outage drill |
| NFR-006 (PII encryption) | V1 DV1.3 + V2 DV2.1 | M2 | Code review + OWASP scan |
| SC-001 (all FRs tested) | All gates | All | Cumulative validation |
| SC-002 (OWASP verified) | V1, V2 | Both | OWASP ZAP scans |
| SC-003 (10K load) | V1 DV1.2 | M2 | Load test |
| SC-004 (OAuth Google/GitHub) | M3 acceptance gate | M3 | End-to-end OAuth test |
| SC-005 (audit logs) | V2 DV2.4 | M4a | Tamper-detection + completeness test |
