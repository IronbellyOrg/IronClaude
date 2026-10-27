# Diff Analysis: Validation Report Comparison

## Metadata
- Generated: 2026-03-23T00:00:00Z
- Variants compared: 2
- Total differences found: 23
- Categories: structural (4), content (8), contradictions (5), unique (4), shared assumptions (2)

## Structural Differences

| # | Area | Variant A (GPT) | Variant B (Sonnet) | Severity |
|---|------|-----------------|-------------------|----------|
| S-001 | Domain taxonomy | 4 domains (Wiring E2E, Lifecycle & Modes, Reachability & Pipeline, Audit & Quality Gates) | 7 domains + constraints/process (wiring_e2e_tests, turnledger_lifecycle, gate_rollout_modes, reachability_framework, pipeline_fixes, qa_gaps, audit_trail, constraints/process) | High |
| S-002 | Gap registry organization | Flat list (H001-H007, M001-M006, L001-L002) | Severity-grouped with horizontal rules and sub-headers per gap | Medium |
| S-003 | Validation Ledger Delta | ABSENT | Present — tracks gap persistence across runs with delta table | High |
| S-004 | Agent report detail | File list only (8 agents) | Table with domain and key findings columns (11 agents) | Medium |

## Content Differences

| # | Topic | Variant A (GPT) Approach | Variant B (Sonnet) Approach | Severity |
|---|-------|--------------------------|----------------------------|----------|
| C-001 | Requirement universe size | 62 total requirements | 71 total requirements | High |
| C-002 | Weighted coverage score | 84.7% | 82.7% | Medium |
| C-003 | Finding count | 15 findings (7H, 6M, 2L) | 21 findings (9H, 5M, 2L) + 5 internal consistency | Medium |
| C-004 | Missing requirements count | 4 missing | 3 missing | Medium |
| C-005 | Conflicting count | 2 conflicting | 1 conflicting | Medium |
| C-006 | FR-7.1 schema gap severity | VALID-HIGH (GAP-H005) | VALID-MEDIUM (GAP-M004) — reclassified because spec clarifies duration_ms is auto-computed | High |
| C-007 | FR-6.1/6.2 gap treatment | 2 MEDIUM findings (M003, M004) for weak language | 2 HIGH findings (H006, H007) + 2 cascading HIGH (H008 SC-1, H009 SC-8) | High |
| C-008 | Boundary/count inconsistency | GAP-H007 (HIGH) — roadmap claims 13 reqs vs 62 actual | ABSENT as standalone gap — subsumed by SC-1/SC-8 cascade analysis | Medium |

## Contradictions

| # | Point of Conflict | Variant A (GPT) Position | Variant B (Sonnet) Position | Impact |
|---|-------------------|--------------------------|----------------------------|--------|
| X-001 | Total requirement count | 62 requirements after decomposition | 71 requirements after decomposition | High — different decomposition methodologies produce different universes, affecting all coverage percentages |
| X-002 | FR-7.1 severity classification | HIGH (GAP-H005) — schema conflict is a blocking gap | MEDIUM (GAP-M004) — auto-computed field reduces severity | High — determines whether this gap blocks remediation priority |
| X-003 | FR-6.1/6.2 severity | MEDIUM — weak language is a specificity concern | HIGH — weak language allows zero new tests, cascades to SC-1/SC-8 failure | High — changes the remediation plan scope significantly |
| X-004 | Number of domains validated | 4 domains | 7 domains + constraints/process | Medium — different granularity may hide or surface coverage gaps |
| X-005 | Integration points checked | 9 integration points | 8 integration points (from Appendix A) | Low — minor count difference, likely same wiring surface |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | Variant B (Sonnet) | Validation Ledger Delta — tracks gap persistence across runs, identifies 6 persistent, 0 resolved, 1 new, 0 regressions | High — provides temporal context showing gaps are not being remediated between runs |
| U-002 | Variant B (Sonnet) | Cascade analysis — explicitly connects FR-6.1/6.2 weak language to SC-1 and SC-8 success criteria failures (GAP-H008, GAP-H009) | High — shows second-order impact of weak gap closure language |
| U-003 | Variant A (GPT) | Adversarial pass status header — notes adversarial re-read was completed | Low — process metadata, not substantive finding |
| U-004 | Variant A (GPT) | GAP-H007 boundary/count inconsistency as standalone finding — roadmap claims 13 requirements vs 62 actual atomic surface | Medium — valid observation about scoping disconnect, though Sonnet addresses this differently through cascade |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|-----------------|------------|---------------|----------|
| A-001 | Both variants agree on NO_GO verdict and same core gaps (FR-1.19, FR-1.20, FR-1.21, FR-2.1a, FR-7.3) | The spec's FR-1.19/1.20/1.21 requirements are correctly interpreted as requiring NEW roadmap tasks rather than being implicitly covered by existing broad tasks | UNSTATED | Yes |
| A-002 | Both variants treat the roadmap as a standalone document requiring explicit task-level traceability | A roadmap task that doesn't name a specific FR ID is assumed to not cover that FR, even if the task's scope could implicitly include it | UNSTATED | Yes |

## Summary
- Total structural differences: 4
- Total content differences: 8
- Total contradictions: 5
- Total unique contributions: 4
- Total shared assumptions surfaced: 2 (UNSTATED: 2, STATED: 0, CONTRADICTED: 0)
- Highest-severity items: S-001, S-003, C-001, C-006, C-007, X-001, X-002, X-003, U-001, U-002
