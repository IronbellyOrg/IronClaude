# Diff Analysis: Roadmap Comparison

## Metadata

- Generated: 2026-05-22T00:00:00Z
- Variants compared: 2 (variant-1-opus, variant-2-sonnet)
- Total differences found: 41
- Categories: structural (6), content (12), contradictions (8), unique (10), shared assumptions (5)

## Structural Differences

| #     | Area                          | Variant 1 (opus)                                                                  | Variant 2 (sonnet)                                              | Severity |
|-------|-------------------------------|-----------------------------------------------------------------------------------|-----------------------------------------------------------------|----------|
| S-001 | Milestone count               | 6 milestones: M0 (foundation, added) + M1–M5 (§2)                                 | 5 milestones: M1–M5; no M0 (§2)                                 | High     |
| S-002 | Total duration                | 11 weeks (2026-03-30 → 2026-06-15, §1)                                            | 9 weeks (2026-04-07 → 2026-06-09, §1)                           | High     |
| S-003 | YAML frontmatter              | Has `id`, `title`, `target_release`, `variant`, `status` (lines 1–10)             | Markdown-only header, no machine-readable frontmatter           | Medium   |
| S-004 | Workstream count + naming     | 5 workstreams (WS-1…WS-5) with explicit cross-cuts (§3)                           | 4 workstreams (WS-A…WS-D) merged Security+Release (§3)          | Medium   |
| S-005 | Appendices                    | Appendix A invariants + Appendix B component matrix (§§Appendix A/B)              | Appendix A invariants + Appendix B Gantt timeline (§§Appendix A/B) | Low      |
| S-006 | Section depth/breakdown       | Phase Gates table A–D + separate Feature Flag table + Rollback (§7)               | Phases 7.1/7.2/7.3 prose + 7.4 flag table + 7.5 procedures (§7) | Medium   |

## Content Differences

| #     | Topic                         | Variant 1 Approach                                                                                                       | Variant 2 Approach                                                                                | Severity |
|-------|-------------------------------|--------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------|----------|
| C-001 | Total effort estimate         | 48 EW total (M0=8, M1=10, M2=9, M3=7, M4=7, M5=7; §1 + §2 roll-up)                                                       | 16 EW total (M1=4, M2=4, M3=3, M4=3, M5=2; §2 fields)                                              | High     |
| C-002 | Foundation/infra work         | Dedicated M0 milestone with 8 specific deliverables (PG, Redis, RSA, SendGrid, OpenAPI, flags, threat model) (§2.M0)     | Folded into WS-C W1-W2 ("provision PostgreSQL/Redis; generate RS256 keypair") (§3.WS-C)            | High     |
| C-003 | Coverage targets              | M1/M2/M3 ≥85% lines, ≥80% branches "to leave headroom"; M4 ≥80% (§2 exit criteria, §8.1)                                 | All milestones ≥80% (§2 exit criteria, §8.1)                                                       | Medium   |
| C-004 | Refresh-token cap (PRD-OQ-2)  | Recommend cap of 10 active refresh tokens; oldest evicted (§9 PRD-OQ-2)                                                  | Recommend limit of 5 concurrent refresh tokens (§9 PRD OQ #2)                                      | Medium   |
| C-005 | UserProfile.roles cap (OQ-002)| Soft cap 16 with DB-level check constraint (§9 TDD-OQ-002)                                                               | Maximum 10 roles (§9 TDD OQ-002)                                                                   | Medium   |
| C-006 | Account lockout cooldown      | "5 fails in 15 min → 423 Locked; cooldown after 15 min unlocks" (§2.M1 exit criterion 6)                                 | "Lock after 5/15 min. Unlock after 30-minute cooldown or via password reset" (§9 OQ #3)            | Medium   |
| C-007 | Risk register breadth         | 8 risks: R-001..R-003 from TDD + R-004..R-008 (open-Q slip, Redis cascade, timing, M3/M4 slip, key rotation) (§6)         | 7 risks: R-001..R-005 plus R-006 conversion, R-007 race condition (§6)                             | Medium   |
| C-008 | Enumeration timing budgets    | Explicit ±15ms (login) / ±10ms (reset) variance CI-enforced (§2.M1, §2.M3, §6.R-006, §8.SEC-4)                          | Stated as invariant "no enumeration via timing differences" but no quantitative variance (§2.M4)   | Medium   |
| C-009 | Rollout phase timing          | Alpha 1w (05-27→06-02) + Beta 2w (06-03→06-09) + GA flag-flip 06-09 (§2.M5)                                              | Alpha 1w (05-26→06-01) + Beta 1w (06-02→06-08) + GA 06-09–06-15 stab. (§7.1–7.3)                  | Medium   |
| C-010 | AUTH_TOKEN_REFRESH removal    | 2026-06-23 (Phase 3 + 2 weeks per §7 Gate D)                                                                             | 2026-06-29 (Phase 3 + 2 weeks per §7.4 table)                                                      | Low      |
| C-011 | Workstream owners             | WS-4 Security owned by auth-team + security reviewer; WS-5 by platform-team (§3)                                         | WS-D owned by security-team + auth-team lead; WS-C platform-team part-time (§3)                    | Low      |
| C-012 | Post-launch review cadence    | T+7d (06-16), T+14d (06-23), T+30d (07-09) (§10 cadence)                                                                 | Week 1 (06-16), Week 2 (06-23), Week 4 (07-07), Day-30 (07-09) (§10.3)                              | Low      |

## Contradictions

| #     | Point of Conflict             | Variant 1 Position                                                                  | Variant 2 Position                                                       | Impact |
|-------|-------------------------------|-------------------------------------------------------------------------------------|--------------------------------------------------------------------------|--------|
| X-001 | Project start date            | "2026-03-30" (§1 phasing table Phase 0)                                             | "2026-04-07" (§1 phasing table W1)                                       | High   |
| X-002 | Total engineer-weeks          | 48 EW (§1 capacity, §2 roll-up)                                                     | 16 EW summed across milestones (§2 effort columns)                       | High   |
| X-003 | Refresh-token-per-user limit  | 10 active (§9 PRD-OQ-2 recommendation)                                              | 5 concurrent (§9 PRD OQ #2 recommendation)                                | Medium |
| X-004 | UserProfile.roles array cap   | 16 (§9 TDD-OQ-002)                                                                  | 10 (§9 TDD OQ-002)                                                        | Medium |
| X-005 | Lockout cooldown semantics    | Auto-unlock after 15-min window (§2.M1 exit 6)                                       | 30-min cooldown OR password reset (§9 OQ #3)                              | Medium |
| X-006 | Async-reset decision date     | 2026-04-22 (during M2) (§9 PRD-OQ-1)                                                 | 2026-04-07 (W1) (§9 PRD OQ #1)                                            | Low    |
| X-007 | NFR-PERF-001 owning milestone | Spread across M1, M2, M5 (§4 traceability)                                          | Solely M5 (§4 traceability table)                                         | Medium |
| X-008 | M1 effort vs scope            | 10 EW for login+register+lockout+policy+audit (§2.M1)                               | 4 EW for nearly identical scope (§2.M1) — 2.5× understatement at same scope | High   |

## Unique Contributions

| #     | Variant   | Contribution                                                                                                    | Value Assessment |
|-------|-----------|-----------------------------------------------------------------------------------------------------------------|------------------|
| U-001 | Opus      | Dedicated M0 foundation milestone with 8 explicit deliverables (§2.M0)                                          | High             |
| U-002 | Opus      | Inter-workstream handoff table H1–H10 (§3 Handoff Points)                                                       | High             |
| U-003 | Opus      | Internal Component build-order table (PasswordHasher → UserRepo → AuthService → JwtService → TokenManager) (§5) | Medium           |
| U-004 | Opus      | Quantitative timing-variance acceptance tests AT-001..AT-016 (§4, §6.R-006)                                     | High             |
| U-005 | Opus      | RS256 key-rotation runbook + R-008 rotation risk with 24h overlap window (§6.R-008, §2.M2)                      | Medium           |
| U-006 | Opus      | Appendix B Component → Milestone matrix (§Appendix B)                                                            | Medium           |
| U-007 | Opus      | Escalation protocol: "any open question still Open within 4 days of Decision Date → engineering lead" (§9)      | Medium           |
| U-008 | Sonnet    | R-006 conversion-rate risk (registration < 60%) with A/B test contingency (§6.R-006)                            | Medium           |
| U-009 | Sonnet    | Appendix B Gantt timeline ASCII visualization (§Appendix B)                                                     | Low              |
| U-010 | Sonnet    | Explicit micro-benchmark gates: JwtService <5ms sign/verify, Redis ops <10ms (§8.3)                              | Medium           |

## Shared Assumptions

| #     | Assumption                                                                                                | Source Agreement                                                              | Impact | Status        |
|-------|-----------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------|--------|---------------|
| A-001 | 7-day refresh-token TTL is fixed and sufficient for v1.0 (no "remember me")                              | Both variants codify 7-day TTL and defer remember-me (V1 §9 PRD-OQ-4; V2 §9 OQ #4) | Medium | STATED         |
| A-002 | bcrypt cost factor 12 is the correct hardness/latency trade-off through GA                                | Both lock cost=12 with hash-time <500ms (V1 §2.M1, §8.4 perf; V2 §2.M1, §8.3) | High   | STATED         |
| A-003 | NFR-PERF-001 p95<200ms is achievable on stated bcrypt-12 + RS256 + PG/Redis stack                        | Both treat 200ms as exit-criterion gate without sensitivity analysis           | High   | UNSTATED       |
| A-004 | SendGrid delivery latency stays under 60s p95 with no rate-limit or vendor outage                         | Both gate M3 on 60s send (V1 §2.M3 ex 6; V2 §8.4) without bound on failure rate beyond R-004 | Medium | UNSTATED      |
| A-005 | Redis-down forcing universal re-login (no stale tokens) is acceptable to product without explicit SLO    | Both adopt TDD §12 invariant as roadmap exit gate; neither captures product sign-off | Medium | UNSTATED      |
| A-006 | 5-failed-attempt lockout in 15-min window does not enable per-account DoS by an attacker                  | Both adopt lockout without mitigation for malicious-lock DoS scenario          | Medium | UNSTATED       |
| A-007 | Quarterly RS256 key rotation is sufficient for compliance and threat model                                | V1 explicitly schedules quarterly (§2.M2 deliverable 10); V2 only "documented" (§5.2 + §6 sec-2) | Medium | UNSTATED      |
| A-008 | Legacy auth path exists and is operationally viable as a rollback target throughout Beta + GA             | Both rely on legacy in R-003 mitigation + rollback runbook (V1 §6.R-003, §7; V2 §6.R-003, §7.5) | High   | UNSTATED       |

## Summary

- Total structural differences: 6
- Total content differences: 12
- Total contradictions: 8
- Total unique contributions: 10
- Total shared assumptions surfaced: 8 (UNSTATED: 6, STATED: 2, CONTRADICTED: 0)
- Highest-severity items: S-001, S-002, C-001, C-002, X-001, X-002, X-008, A-002, A-003, A-008
- Similarity check: NO — variants are >10% different (different milestone count, 3× effort delta, divergent OQ recommendations, distinct workstream taxonomies); full debate required, do NOT skip.
