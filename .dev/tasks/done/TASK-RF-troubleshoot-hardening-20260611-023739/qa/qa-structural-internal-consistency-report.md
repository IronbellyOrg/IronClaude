# QA Report — Structural Internal Consistency (FINAL_ONLY gate, dedicated lens)

**Topic:** Pipeline Hardening Closure mode — cross-document field/verdict/FR/cross-ref consistency
**Date:** 2026-06-11
**Phase:** report-validation (structural internal-consistency lens)
**Fix cycle:** N/A
**Fix authorization:** false (REPORT ONLY — no files modified)

---

## Overall Verdict: FAIL

FAIL because at least one internal-consistency defect of non-zero severity was found (the H1 card "11-field" mislabel, present in two in-scope deliverables). Per the gate rule "FAIL if any issue of any severity," a single confirmed defect is sufficient. The remainder of the deliverable set is highly consistent; this is a narrow, localized count-drift defect, not a systemic failure.

> Note on the "assume ≥10 errors" framing: per QA Principle 9 (a false PASS is worse than a false FAIL, but findings must be evidence-cited and never fabricated to hit a quota), this report records only defects I could prove against the actual files. I verified the four prompt-specified consistency axes exhaustively (field-name spelling, H-status→verdict mappings, FR→test references, ref→ref cross-references). One genuine defect was found; the other axes are clean. I did not manufacture additional findings to reach a target count.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Field names match across SKILL.md / OC / report-template / remediation-handoff (`pipeline_hardening_verdict`, `waiver_status`, etc.) | PASS | grep across 4 files: `pipeline_hardening_verdict` ×14, `waiver_status` ×16, `off_path_review_decision` ×4, `backtest_status` ×3 + 1 prose `backtest-status` (table name). No misspelled variants. |
| 2 | Four `*_card_path`/`*_path` field names identical across SKILL / OC / report-template | PASS | `runtime_entrypoint_card_path`, `contract_ledger_path`, `unmask_sweep_path`, `effective_input_card_path` each present in SKILL (×3), OC (×1), report-template (×1) — spelled identically. |
| 3 | `known_escapes_caught` object shape `{escape_id, wave, card_path, status}` consistent | PASS | OC L23, report-template L230, SKILL L72 — identical 4-key shape. |
| 4 | H-status → verdict mappings consistent (truth table ↔ report-template blockers) | PASS | report-template L234–238 reproduces OC §5.4 Report-Language column (rows 2–6) verbatim; row 1 = collapsed not-applicable line, row 7 = pass (blocker omitted). |
| 5 | H5 decision-to-status mapping consistent (OC table ↔ closure.md prose) | PASS | OC L47–50 (`performed→PASS/none`, `not_required→PASS/none`, `required→FAIL/none`, `waived_with_rationale→N/A/latched`) ↔ closure.md L50–51 prose (valid waiver → latch + {blocked,advisory}; invalid → FAIL). No contradiction. |
| 6 | 4-token verdict enum identical everywhere | PASS | `pass \| blocked \| advisory \| not_applicable` in SKILL L64, OC L5/L15, closure.md L13, report-template (spaced + no-space forms), remediation-handoff L11/L35/L69. `advisory` never dropped. |
| 7 | Truth table = 7 rows, every row "Downstream Override Allowed? = No" | PASS | OC: 7 rows `\| 1..7 \|`; `\| No \|` count = 7. Matches inventory "7-row". |
| 8 | E-class → wave mapping consistent across per-wave refs and e2e scenarios | PASS | H1 closes E1/supports E4; H2 closes E4/supports E1; H3 closes E2+E3; H4 closes E5. e2e E1→H1(FR-3/4), E2→H3(FR-7/8), E3→H3(FR-7/8/9), E4→H2(FR-5), E5→H4(FR-10) — aligned. |
| 9 | FR→test references name tests that actually exist AND pass | PASS | FR-1…FR-13 referenced with no gaps; all 18 content-assertion tests collected & PASS (`18 passed`). Each test docstring's FR maps to the ref it reads. |
| 10 | Each per-wave ref points to hardening-output-contract.md for aggregation | PASS | runtime-entrypoint / contract-enumeration / unmask-and-sweep / effective-input each link `hardening-output-contract.md` ×1. |
| 11 | All 6 hardening refs present in SKILL.md Refs index | PASS | SKILL L580–585 index rows for all 6 refs; Wave 4.5 steps L405–411 cite each ref. |
| 12 | Inventory line-count claims vs actual `wc -l` (20 deliverables) | PASS | All 18 file line counts match inventory exactly (refs, SKILL=587, command=202, tests, e2e=50). |
| 13 | Inventory test-count claims (13 unit + 5 integration = 18) | PASS | Per-file `def test_` counts match inventory (h0=2,h1=1,h2=2,h3=3,h4=2,verdict=5,output_contract=3); split 13/5 confirmed. |
| 14 | Inventory schema-size claims (H0 6-field, H2 6-field, H3 10-field, H4 8-field, §5.5 11-field) | PASS | Row counts: H0=6, H2=6, H3=10, H4=8, OC §5.5=11. All match inventory's row-count convention. |
| 15 | Inventory schema-size claim — **H1 card "§5.6 11-field"** | **FAIL** | H1 card table = **10 rows / 12 distinct field tokens**. "11-field" matches neither. See Finding F1. |
| 16 | Enum-value-count claims (9-value boundary_type, 5 near-miss negatives, 4 controls, 4-rule grammar) | PASS | boundary_type=9 values; FR-8 near-miss list=5; FR-7 controls=4; §5.7 grammar=4 rules. |
| 17 | H0 trigger-list cardinality consistent (closure.md prose ↔ SKILL.md prose ↔ boundary_type enum) | PASS | 9 trigger items in closure.md L19, 9 in SKILL L401, 9 enum values in boundary_type — aligned. |
| 18 | Downstream no-override rule names same 4 stages everywhere | PASS | OC L54/L68, closure.md L44, report-template L304, remediation-handoff L11: task-builder / sc:reflect / sc:adversarial / report-rendering. |
| 19 | `success_with_hardening_*` token spelling consistent | PASS | `success_with_hardening_blocker` / `success_with_hardening_advisory` identical in OC L54, report-template L304, remediation-handoff L10/L36. |
| 20 | `contract_version` default (`1.0.0`) consistent | PASS | OC L13, OC L25, SKILL L62 all state default `1.0.0`. |

## Summary

- Checks passed: 19 / 20
- Checks failed: 1
- Critical issues: 0
- Important issues: 1
- Minor issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| F1 | IMPORTANT | `qa-input-inventory.md:14` AND `tests/troubleshoot/test_hardening_h1.py:17,21` | The H1 Runtime-Entrypoint Card schema (`refs/runtime-entrypoint-verification.md` L15–24) is labeled "§5.6 **11-field** card" in the inventory and "the **11-field** H1 card schema (§5.6)" in the test docstring/comment. The actual table has **10 rows** and **12 distinct field tokens** (rows 8 and 9 each pack two `_command`/`_result` fields: `negative_witness_command`/`negative_witness_result` and `positive_witness_command`/`positive_witness_result`). The test's own for-loop asserts **12** field tokens. "11" matches neither the 10-row count (the convention the inventory uses for H0=6, H2=6, H3=10, H4=8) nor the 12 distinct fields the schema/test enumerate. Under the inventory's own row-counting convention the correct label is "10-field"; under a distinct-field-token count it is "12-field". | Pick one convention and apply it consistently. Recommended: change "11-field" → "10-field" in `qa-input-inventory.md:14` and in `test_hardening_h1.py:17` and `:21` to match the 10-row H1 table (consistent with the row-count convention used for H0/H2/H3/H4). Do NOT alter the test's 12-token for-loop — it correctly enumerates all 12 fields; only the prose count is wrong. |

## Verification Detail for F1 (evidence)

H1 card schema (`refs/runtime-entrypoint-verification.md`, data rows L15–24, numbered):

1. `producer` · 2. `transformers` · 3. `consumer_or_evaluator` · 4. `boundary_crossed` · 5. `replay_command` · 6. `production_boundary_reach_proof` · 7. `forbidden_interpretation` · 8. `negative_witness_command` / `negative_witness_result` · 9. `positive_witness_command` / `positive_witness_result` · 10. `accepted_substitute_rationale`

= **10 table rows**, **12 distinct field tokens**. The "11-field" label is off-by-one against the row count and off-by-one against the field-token count.

Cross-reference confirming the inventory's row-count convention (so this is an isolated drift, not a convention difference):

- H0 boundary scan → inventory "6-field" → table = 6 rows ✓
- H2 ledger → inventory "6-field" → 6 rows ✓
- H3 card → inventory "10-field" → 10 rows ✓
- H4 manifest → inventory "8-field" → 8 rows ✓
- OC §5.5 output-contract → inventory "11-field" → 11 rows ✓ (this "11-field" is correct)
- **H1 card → inventory "11-field" → 10 rows ✗** (this is the defect)

## Actions Taken

None — `fix_authorization: false`. Reported only.

## Recommendations

- Before proceeding, correct the H1 "11-field" → "10-field" label in `qa-input-inventory.md:14`, `test_hardening_h1.py:17`, and `test_hardening_h1.py:21`. This is a documentation/comment fix only; no test logic (the 12-token assertion loop) changes, so the suite stays green.
- All other consistency axes (field-name spelling, verdict/H-status mappings, FR→test resolution, ref→ref cross-references, line/schema/enum/test counts) are clean and require no action.

## Confidence Gate

- **Confidence:** "Verified: 20/20 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%"
- **Tool engagement:** "Read: 12 | Grep: ~30 | Glob: 0 | Bash: 14"
- Every check above was verified with a cited tool action (Read of the source file + grep/wc evidence). The pytest suite was executed (`18 passed`) to confirm FR→test references resolve to real, passing tests. No web research was required (all claims are local-source-truth).
- No UNCHECKED items. No UNVERIFIABLE items.

## QA Complete

VERDICT: FAIL
