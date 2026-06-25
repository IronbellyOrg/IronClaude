# QA Report — Domain Advisory-Invariant Lens (Report Validation)

**Topic:** Pipeline Hardening Closure — `advisory` verdict invariant preservation
**Date:** 2026-06-11
**Phase:** report-validation (domain-lens / FINAL_ONLY gate)
**Fix cycle:** N/A (fix_authorization: false — REPORT ONLY)
**Stance:** Adversarial. Assumed at least one artifact dropped or weakened `advisory`. Verified the negative.

---

## Overall Verdict: PASS

The four-token enum `pass | blocked | advisory | not_applicable` is intact in every verdict-touching
artifact. The §5.4 truth table has all 7 rows with rows 5 AND 6 emitting `advisory` with the exact
report-language strings. `report-template.md`, `remediation-handoff.md`, and the verdict test all
carry the 4-token form and the advisory rows. No 3-token enum and no `advisory`-removal/forbid found
anywhere in the deliverable set.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `pipeline_hardening_verdict` is the 4-token enum `pass\|blocked\|advisory\|not_applicable` in `hardening-output-contract.md` | PASS | Read L5 (prose: "four-token enum … `advisory` … MUST NOT be removed … a three-token enum is a defect") + L15 schema row `enum pass\|blocked\|advisory\|not_applicable`. |
| 2 | §5.4 truth table has all 7 rows, ROW 5 + ROW 6 emit `advisory` with exact report-language | PASS | `grep -nE "^\| [0-9] \|"` returned exactly rows 1–7. Row 5 → `advisory` / `ADVISORY — closure relies on waived/substituted proof`; Row 6 → `advisory` / `ADVISORY — scoped closure with rationalized N/A`. All 7 rows "Downstream Override Allowed? = No". |
| 3 | `report-template.md` Closure verdict is the 4-token form | PASS | Read L209 `**Closure verdict**: <pass\|blocked\|advisory\|not_applicable>` + L301 rule "a three-token Closure verdict is a defect" + L237–238 both ADVISORY blocker lines present. |
| 4 | `remediation-handoff.md` carries 4-token verdict + `success_with_hardening_advisory` | PASS | Read L11 "four-token verdict (`pass \| blocked \| advisory \| not_applicable`) preserved end-to-end; `advisory` is never dropped"; L10 + L36 render `success_with_hardening_advisory`; BUILD_REQUEST L69 carries `pipeline_hardening_verdict: <pass\|blocked\|advisory\|not_applicable>`. |
| 5 | `test_verdict_aggregation_from_h_statuses` explicitly asserts BOTH advisory rows | PASS | Read L67–69: asserts `"ADVISORY — closure relies on waived/substituted proof"` (row 5) AND `"ADVISORY — scoped closure with rationalized N/A"` (row 6) AND `OC.count("\`advisory\`") >= 2`. Live `pytest` run: PASS. |
| 6 | `pipeline-hardening-closure.md` (mode skeleton) carries 4-token enum, advisory first-class | PASS | Read L13 "four-token enum `pass \| blocked \| advisory \| not_applicable`. `advisory` is a first-class outcome … never omitted." |
| 7 | `SKILL.md` verdict touchpoints all 4-token, advisory-inclusive | PASS | Grep L64 schema row `enum pass \| blocked \| advisory \| not_applicable`; L65 `{blocked, advisory}` latch; L411 + L435 render advisory. 5 advisory mentions, 0 three-token forms. |
| 8 | No 3-token enum (`pass\|blocked\|not_applicable` without advisory) anywhere | PASS | `grep -rn` across all refs + SKILL.md + command + tests/troubleshoot/ → "NO 3-token-without-advisory matches found". |
| 9 | `advisory` token present in every verdict-touching artifact | PASS | Per-file count: hardening-output-contract=10, pipeline-hardening-closure=3, report-template=7, remediation-handoff=7, SKILL.md=5, test_hardening_verdict=14, test_hardening_output_contract=11. Command=0 (correct — thin NFR-5 command advertises the mode generically, renders no verdict enum). |
| 10 | Live test suite green (advisory assertions actually pass) | PASS | `uv run pytest tests/troubleshoot/ -q` → 18 passed. Includes the 2 integration tests asserting advisory rows 5/6. |
| 11 | `backtest_status` advisory-until-complete invariant intact | PASS | Read OC L62–64: `not_run`/`partial` keep signoff `advisory` even when verdict=`pass`; only `complete` may mirror. `test_backtest_status_keeps_pipeline_health_advisory_until_complete` PASS. |

## Summary

- Checks passed: 11 / 11
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (REPORT ONLY)

## Issues Found

None. No artifact dropped, narrowed, or forbade `advisory`. The suspected regression
(3-token enum / removed advisory rows) was searched for adversarially and is absent.

## Notable strength signals (not defects)

- The contract ref proactively documents the invariant as a guard: "Any artifact that drops
  `advisory` or uses a three-token enum is a defect" (`hardening-output-contract.md` L5),
  mirrored in `report-template.md` L301 and `pipeline-hardening-closure.md` L13. The regression
  is guarded at the spec level, not just incidentally absent.
- The verdict test's docstring (L40, L57) names the exact regression it guards: "guards against
  the prior 3-token-enum regression" / "guards the FOUR-token advisory-inclusive enum" — the test
  is purpose-built as the regression sentinel and asserts both advisory rows individually plus a
  `count >= 2` floor.

## Confidence

**Confidence:** Verified: 11/11 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

**Tool engagement:** Read: 11 | Grep: 5 | Glob: 0 | Bash: 5 (incl. 1 live pytest run)

(Tool-call count ≥ checklist item count; every Read/Grep targeted a specific artifact's verdict
surface, and the advisory invariant was confirmed by an executed test run, not by claim-reliance.)

## Recommendations

- Green light on the advisory-invariant lens. No remediation required.

## QA Complete

VERDICT: PASS
