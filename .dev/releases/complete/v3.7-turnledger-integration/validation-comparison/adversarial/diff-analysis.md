# Diff Analysis: Validation Report Comparison

## Metadata
- Generated: 2026-03-23T00:00:00Z
- Variants compared: 2
- Variant A: Claude report (`v3.3-TurnLedger-Validation/validation/02-consolidated-report.md`)
- Variant B: GPT report (`ValidationGPT/02-consolidated-report.md`)
- Total differences found: 28
- Categories: structural (6), content (10), contradictions (7), unique contributions (5)

---

## Structural Differences

| # | Area | Variant A | Variant B | Severity |
|---|------|-----------|-----------|----------|
| S-001 | Domain decomposition | 7 domains + 2 cross-cutting (D1-D7, CC3-CC4) | 4 domains (Wiring E2E, Lifecycle & Modes, Reachability & Pipeline, Audit & Quality Gates) | High |
| S-002 | Gap ID scheme | GAP-H/M/L + [ADV] prefix for adversarial finds | GAP-H/M/L sequential, no adversarial separation | Medium |
| S-003 | Agent reports | 11 named agent files (D1-D7, CC1-CC4) | 8 agent files (D1-D4, CC1-CC4) | Medium |
| S-004 | Cross-cutting table | 4 agents with PASS/FAIL/WARNING detail | 5 concerns with narrative status | Medium |
| S-005 | Integration wiring audit | 9 integrations, all FULLY_WIRED | 9 integrations, 1 PARTIALLY_WIRED | Low |
| S-006 | Rejected findings section | Explicit REJECTED table (4 items with reasons) | No rejected findings section (0 rejections) | High |

---

## Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Severity |
|---|-------|-------------------|-------------------|----------|
| C-001 | Total requirements count | 84 atomic requirements | 62 atomic requirements | High |
| C-002 | Weighted coverage score | 93.5% | 84.7% | High |
| C-003 | Full coverage score | 91.7% (77/84) | 75.8% (47/62) | High |
| C-004 | HIGH finding count | 6 HIGH | 7 HIGH | Medium |
| C-005 | PARTIAL requirements | 3 PARTIAL | 9 PARTIAL | High |
| C-006 | CONFLICTING requirements | 0 CONFLICTING | 2 CONFLICTING | High |
| C-007 | Confidence interval | +/- 3% | +/- 4% | Low |
| C-008 | Verdict rationale | ">3 HIGH findings" | "weighted < 85% AND >3 HIGH" | Medium |
| C-009 | FR-7.1/7.3 treatment | Not flagged as gap | GAP-H005 (schema) + GAP-H006 (flush semantics) — both VALID | High |
| C-010 | FR-5.2 positive-case testing | Not flagged | GAP-M002 — VALID finding | Medium |

---

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Impact |
|---|-------------------|-------------------|-------------------|--------|
| X-001 | Requirement universe size | 84 total requirements | 62 total requirements | High — Ground truth: ~65 (47 FRs + 12 SCs + 6 constraints). Variant A over-counts; Variant B slightly under-counts. |
| X-002 | Wiring E2E domain count | 25 requirements, 100% covered | 23 requirements, 87.0% (3 MISSING) | High — Variant A claims 100% but later identifies 3 of the "missing" FRs (1.19, 1.20, 1.21) via adversarial pass, meaning the 100% D1 score is internally inconsistent. |
| X-003 | CONFLICTING findings | 0 conflicting | 2 conflicting (FR-7.1 schema, FR-7.3 flush) | High — Ground truth: Variant B is correct. Roadmap L47 lists 9-field schema omitting `duration_ms`; spec shows 10 fields. Roadmap L48 says "auto-flushes on session end"; spec says "auto-flushes after each test." These are genuine spec-roadmap conflicts. |
| X-004 | Integration wiring: `_run_checkers()` | FULLY_WIRED (implicit via Appendix A.6) | PARTIALLY_WIRED | Medium — Variant B is more precise; the checker test surface is partial per FR-5.2 positive-case gap. |
| X-005 | D1 Wiring E2E coverage | 25/25 COVERED | 20/23 COVERED, 3 MISSING | High — Same underlying data, different counting. Variant A counts FR-1.19/1.20/1.21 as "covered" in D1 but later catches them as MISSING in adversarial pass. Variant B catches them in the primary pass. |
| X-006 | PARTIAL count | 3 PARTIAL | 9 PARTIAL | Medium — Variant B identifies more requirements as partially covered rather than fully covered. |
| X-007 | NEEDS-SPEC-DECISION | 1 item (NSD-001: FR-7.1 vs FR-7.3 assertion_type ambiguity) | 0 items | Low — Variant A identifies a genuine spec ambiguity that Variant B missed. |

---

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | A | REJECTED findings section with adjudication rationale (4 CC4 false positives corrected) | High — Demonstrates validation rigor; prevents downstream confusion about false gap claims |
| U-002 | A | NEEDS-SPEC-DECISION section (NSD-001: FR-7.1 vs FR-7.3 `assertion_type` ambiguity) | Medium — Useful for spec hygiene; low implementation impact |
| U-003 | B | FR-7.1 schema conflict detection (GAP-H005: `duration_ms` omitted from roadmap) | High — Genuine spec-roadmap conflict that Variant A completely missed |
| U-004 | B | FR-7.3 flush semantics conflict detection (GAP-H006: session-end vs per-test flush) | High — Critical for audit trail crash-resilience; directly impacts FR-3.3 (interrupted sprint) |
| U-005 | B | FR-6.1/6.2 closure specificity critique (GAP-M003/M004) | Medium — Valid concern about implementability of vague task descriptions |

---

## Summary
- Total structural differences: 6
- Total content differences: 10
- Total contradictions: 7
- Total unique contributions: 5
- Highest-severity items: X-001, X-002, X-003, X-005, C-001, C-009, S-001, S-006
