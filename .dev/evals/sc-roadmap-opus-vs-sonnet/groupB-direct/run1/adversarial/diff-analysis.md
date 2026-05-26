# Diff Analysis: Roadmap Variant Comparison

## Metadata

- Generated: 2026-05-22T16:50:00+00:00
- Source: merged-prd-tdd-user-auth.md (User Authentication Service v1.0)
- Variants compared: 2
  - Variant 1: opus:architect (4,841 words)
  - Variant 2: sonnet:analyzer (3,191 words)
- Total differences found: 36
- Categories: structural (8), content (9), contradictions (5), unique (10), shared assumptions (4)

---

## Structural Differences

| #     | Area                    | Variant 1 (opus:architect)                                                          | Variant 2 (sonnet:analyzer)                                                  | Severity |
|-------|-------------------------|-------------------------------------------------------------------------------------|------------------------------------------------------------------------------|----------|
| S-001 | Top-level sections      | 10 sections: Exec, Objectives, Milestones, Workstreams, Cross-Cutting, Risk, Deps Graph, Gates, Open Q | 11 sections: Exec, Metrics, Milestones, Sprint Breakdown, Validation, Risk Matrix, Perf Gates, Rollout, Out-of-Scope, Open Q | Medium   |
| S-002 | Milestone count         | 5 (M1-M5)                                                                           | 5 (M1-M5)                                                                    | Low      |
| S-003 | Milestone naming        | Foundations / Core Auth Backend / Token Lifecycle+Frontend / Hardening+Reset / GA  | Core AuthService / Token Management / Password Reset / Frontend Integration / GA | High     |
| S-004 | Per-milestone subsection structure | Scope / Deliverables / Exit Criteria / Architectural Risks / Dependencies | Goal / Deliverables / Validation / Metrics / Sprint Allocation               | Medium   |
| S-005 | Workstreams section     | Present — 5 named workstreams (Backend, Frontend, Security, Observability, Ops)    | Absent (replaced with Sprint-Level Breakdown table)                          | Medium   |
| S-006 | Cross-Cutting Concerns  | Present as dedicated section (Observability, Security, Perf, Data Integrity)        | Absent (concerns distributed into per-milestone deliverables)                | Medium   |
| S-007 | Validation Strategy     | Embedded in per-milestone Exit Criteria; dependency graph at end                   | Dedicated section with per-FR test-pyramid table (unit/integration/E2E)      | Medium   |
| S-008 | Success Metrics         | Embedded in Strategic Objectives prose                                              | Top-level table with 12 metrics, baseline, measurement method, source        | Medium   |

---

## Content Differences

| #     | Topic                              | Variant 1 Approach                                                                            | Variant 2 Approach                                                                       | Severity |
|-------|------------------------------------|-----------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|----------|
| C-001 | M1 scope                           | "Foundations": infra + ADRs + contracts; no feature code ships                                | "Core AuthService": login + register endpoints with bcrypt + lockout                     | High     |
| C-002 | Password reset milestone           | M4 (paired with hardening & observability)                                                    | M3 (dedicated milestone, before frontend)                                                | High     |
| C-003 | Frontend integration milestone     | M3 (parallel with token lifecycle, mid-stream)                                                | M4 (after all backend done, just before GA)                                              | High     |
| C-004 | M5 scope                           | Pen-test + remediation + runbooks + 4-stage rollout (1/10/50/100%)                            | Alpha → 10% Beta → 100% GA, flag removal, monitoring/alerts                              | Medium   |
| C-005 | ADR practice                       | Explicit ADR deliverables in M1 (D1.5: JWT-vs-sessions, bcrypt-vs-argon, Redis-storage, MFA-seams) | No explicit ADR deliverables; design decisions inherited from TDD                       | Medium   |
| C-006 | Observability deliverables         | Dedicated D4.6 (Prometheus metrics + OTel spans); discussed in Cross-Cutting                  | Listed as D5.5 (dashboards) + D2.8 (audit log) deliverable; no OTel tracing               | Medium   |
| C-007 | Pen-test                           | D5.1: external pen-test as a deliverable; D5.2 remediation; 2-day buffer                       | Not a deliverable; security review listed under M5 validation                            | High     |
| C-008 | Rollback procedure                 | Mentioned in M5 (rehearsed within 7 days); rollback honors refresh tokens issued during stages | Rollback triggers from TDD §19.4 enumerated explicitly (p95>1000ms, err>5%, Redis>10/min) | Low      |
| C-009 | Sprint mapping                     | Workstreams + dependency graph (no explicit sprint dates)                                     | Sprint S1-S6 table with date ranges and owner team                                       | Medium   |

---

## Contradictions

| #     | Point of Conflict                | Variant 1 Position                                                                | Variant 2 Position                                                                  | Impact  |
|-------|----------------------------------|-----------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|---------|
| X-001 | M1 target date                   | 2026-04-03 (≈3 weeks from project start, infra-only)                              | 2026-04-14 (4 weeks, ships login+register feature)                                  | High    |
| X-002 | M2 target date                   | 2026-04-24                                                                        | 2026-04-28                                                                          | Low     |
| X-003 | M3 target date                   | 2026-05-15                                                                        | 2026-05-12                                                                          | Low     |
| X-004 | M4 target date                   | 2026-05-29                                                                        | 2026-05-26                                                                          | Low     |
| X-005 | Workstream parallelism model     | Five parallel workstreams (Backend, Frontend, Security, Observability, Ops) progressing between gates | Strictly sequential single-team sprint cadence (S1-S6 each owned by one team)       | High    |

---

## Unique Contributions

| #     | Variant            | Contribution                                                                                                  | Value Assessment |
|-------|--------------------|---------------------------------------------------------------------------------------------------------------|------------------|
| U-001 | opus:architect     | "Foundations" milestone with explicit ADRs as deliverables before any feature work                            | High             |
| U-002 | opus:architect     | Five named workstreams with skill sets and ownership identified                                                | Medium           |
| U-003 | opus:architect     | Critical-path dependency graph with explicit blockers (D1.3→D2.3, D1.2→D3.1→D3.2→D3.4)                       | High             |
| U-004 | opus:architect     | Log scrubber gate: automated test grepping logs for credential substrings (D4.8)                              | High             |
| U-005 | opus:architect     | `kid` header strategy + overlapping key validity windows for JwtService rotation                              | High             |
| U-006 | opus:architect     | Account lockout DoS mitigation: lockout key composite of email+IP, not email alone                            | High             |
| U-007 | sonnet:analyzer    | Top-level Success Metrics table with 12 metrics, sources, baselines, measurement methods                       | High             |
| U-008 | sonnet:analyzer    | Per-FR validation table mapping each FR-AUTH-NNN to unit/integration/E2E test types                            | High             |
| U-009 | sonnet:analyzer    | Sprint S1-S6 table with explicit date windows, milestone mapping, primary deliverables per sprint              | Medium           |
| U-010 | sonnet:analyzer    | Out-of-Scope explicit table mapping each excluded capability to its deferral release (v1.1/v1.2/v2.0)          | Medium           |

---

## Shared Assumptions

| #     | Assumption                                                                                                  | Source Agreement                              | Classification | Promoted? |
|-------|-------------------------------------------------------------------------------------------------------------|-----------------------------------------------|----------------|-----------|
| A-001 | The 2026-06-09 GA date is firm and achievable given the available team capacity                              | Both variants commit M5 to 2026-06-09         | UNSTATED       | YES       |
| A-002 | Bcrypt cost 12 ships in production without forcing reduction (latency budget can absorb ~300ms hash time)    | Both lock cost factor 12, no contingency for reduction | UNSTATED  | YES       |
| A-003 | Frontend team is available to start work alongside backend (no resource contention)                          | Both schedule frontend work without team-capacity reasoning | UNSTATED | YES       |
| A-004 | SendGrid (or equivalent) is ready and reachable from the start of development; no procurement delay         | PRD assumption inherited by both; no contingency milestone | STATED   | NO        |

### A-001 Detail

**Promoted as synthetic diff point.** Both variants commit to 2026-06-09 GA but with materially different milestone shapes (V1 has a no-feature "Foundations" M1; V2 ships features in M1). Neither variant tests whether the 11-12-week window can absorb pen-test slip (V1 acknowledges 2-day buffer; V2 has none), bcrypt re-tuning, or a Phase 2 rollout extension. Convergence on the date masks divergence on feasibility.

### A-002 Detail

**Promoted as synthetic diff point.** Both variants commit to bcrypt cost 12 (NFR-SEC-001) and the 200ms p95 latency (NFR-PERF-001). V1 explicitly flags this tension ("bcrypt cost 12 may push hash time above 500ms on under-provisioned runtimes") and proposes horizontal scaling as the contingency. V2 acknowledges the tension in R-LATENCY but only via "connection pooling" — no scaling plan or cost-factor fallback. If hash time saturates CPU at 500 concurrent, neither plan reduces cost 12. Sufficiency challenge: would 500 concurrent + bcrypt 12 + ~300ms hash actually fit under p95 200ms with linear pod scaling alone?

### A-003 Detail

**Promoted as synthetic diff point.** V1 schedules frontend work in M3 (alongside backend token lifecycle); V2 schedules frontend in M4 (after all backend complete). Both assume the frontend team is available exactly when their plan requires. Neither variant tests cross-team scheduling, role-share, or contractor backfill scenarios.

### A-004 Detail

PRD §Assumptions explicitly states "Email delivery infrastructure (SendGrid or equivalent) is available before development begins." Both variants honor this as a stated precondition. **Not promoted** to synthetic diff point.

---

## Summary

- Total structural differences: 8 (1 High, 6 Medium, 1 Low)
- Total content differences: 9 (4 High, 4 Medium, 1 Low)
- Total contradictions: 5 (2 High, 3 Low)
- Total unique contributions: 10 (7 High, 3 Medium)
- Total shared assumptions surfaced: 4 (UNSTATED: 3 promoted, STATED: 1 not promoted)
- Highest-severity items: S-003, C-001, C-002, C-003, C-007, X-001, X-005
- Variants substantially similar threshold (10%) check: 36 differences across compact 2-variant comparison → NOT similar, full debate warranted
