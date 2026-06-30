# Phase 7 Gate A — Consolidated Final-Phase M3 Findings (whole change-set)

9 lens agents (3 structural + 3 content + 3 domain). 8 PASS, 1 FAIL (crossref).

| Lens | Verdict |
|---|---|
| final-conformance | PASS (no stubs/TODO) |
| final-consistency | PASS (counts agree end-to-end) |
| final-completeness | PASS (all deltas landed, 175→176) |
| final-actionability | PASS (mutation-tested, no vacuous tests) |
| final-domain-accuracy | PASS |
| **final-crossref** | **FAIL** (1 CRITICAL FR-9.5/T-1117 gap + 3 phantom T-IDs + 1 label) |
| final-INV-fidelity | PASS (INV-001 verbatim, 1 increment site, R1/R2/R3 traced) |
| final-closed-enum | PASS (37 + 6 end-to-end) |
| final-core-purity | PASS |

## TOP-LINE VERDICT: FAIL → fixes applied (INV-001 untouched)

The final crossref lens correctly caught what the per-phase gates had SCOPED AWAY: at the final
gate (all phases built), the §9 matrix demands a real test + real implementation per T-ID.

| # | Finding | Severity | Disposition |
|---|---|---|---|
| F1 | **FR-9.5/T-1117 "review-wins-over-decline" half-built** — the watermark handled the STALE-decline half (T-1118), but the same-window "attributed re-review wins over a co-occurring decline" half (EC-22) had NO arbiter and NO test. classify() did decline-first unconditionally. | **CRITICAL** | **FIXED** — added `_is_attributed_review` helper + FR-9.5 arbiter in classify(): at the S5 poll (watermark set), a genuine attributed re-review (review newer than watermark) WINS over a co-occurring decline; the initial poll (watermark=None) keeps decline-first (FR-9.1). Also fixed a related bug: a decline-shaped comment was being miscounted as a finding (excluded it from the findings-comment count). Added `test_t1117_ec22_attributed_rereview_wins_over_decline`. Verified: review-wins (findings + clean), decline-first at initial poll, S5-decline-only stays declined, stale-decline+clean→clean. |
| F2 | **3 phantom matrix T-IDs** (T-1114 FR-9.3, T-1116 FR-9.4, T-1113b FR-9.2) — behavior covered by differently-named tests; the matrix IDs didn't resolve (would trip the M4 phantom detector). | IMPORTANT | **FIXED** — added the T-ID tokens to the covering test names/docstrings: T-1113b→`test_t1110_t1113b_decline_at_initial_poll`, T-1114→`test_t1114_auggie_at_most_once`, T-1116→`test_t1116_fallback_findings_pass_verify_before_remediate`. All 4 previously-phantom IDs (incl. T-1117) now grep-resolve to a real test. |
| F3 | T-1121/1122/1125 label drift vs matrix intent (clamp/push-bound) | MINOR | **NO-FIX (documented)** — behavior fully covered (clamp=t1122, single-shot=t1123, frozen-counters=t1125, push-bound=t1121); the docstring T-IDs are reasonable. Not worth churn. |
| — | Benign observations: "32 vs 33 prior" prose internally coherent (32 §11.3 + 1 §12.1 = 33, +4 = 37); SKILL Output-Contract field naming; auggie-fallback.md re-entry verb list broader than core (SKILL does classify/re-grade) — all NO-FIX. | INFO | documented |

## ACTIONABLE FIXES (executor, single I20 writer) — applied
- F1: classifier.py FR-9.5 arbiter + decline-not-a-finding fix + T-1117 test.
- F2: phantom T-ID tokens on covering tests.
- 176 tests pass; ruff + format clean on touched files. INV-001 NOT touched (classifier change only).
