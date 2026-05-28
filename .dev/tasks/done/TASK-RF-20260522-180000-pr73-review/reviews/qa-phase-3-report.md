# QA Report — Phase 3: 3-Case Decomposition

**Topic:** PR #73 review-fix — Issue 2: Replace binary tiebreaker with 3-case decomposition
**Date:** 2026-05-22
**Phase:** fix-cycle (Phase 3 verification)
**Fix cycle:** N/A (single verification pass)

---

## Overall Verdict: PASS

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | AC1: SKILL.md derivation rule (line 69) replaces binary tiebreaker with 3-case decomposition | PASS | Read SKILL.md:69 — contains all three cases ("**Case A** (user expectation diverges)", "**Case B** (test contradicts docs+code consensus)", "**Case C** (code violates docs)") AND uses literal phrase "by construction (not by tiebreaker)". Each case explicitly lists trigger conditions and resulting flag values. |
| 2 | AC2: SKILL.md Output Contract row appends Case B clause (line 51) | PASS | Read SKILL.md:51 — row description ends with exact required clause: "When the failing artifact is a test (Case B in the derivation rule), `test_is_wrong=true` is the correct flag and this flag stays false — the docs are not the bug." |
| 3 | AC3: report-template.md rendering rule mutual-exclusion line (line 179) | PASS | Read report-template.md:179 — reads exactly "Mutually exclusive with `Test is wrong: true` **by construction, not by tiebreaker**." followed by 3-case summary (Case A → `behavior_is_documented=true`; Case B → `test_is_wrong=true`; Case C → both false). Closes with "Only one can be true." |
| 4 | AC4: report-template.md header HTML comment (line 18) | PASS | Read report-template.md:18 — comment includes both required clauses: "AND the recommended remediation is a SPEC/DOCS change (not a test change — that's the test_is_wrong=true case)" AND "Mutually exclusive with `Test is wrong: true` by construction (3-case decomposition: see SKILL.md derivation rule)". |
| 5 | AC5: All 4 grep gates emit OK | PASS | Bash grep results: `3-case decomposition` count=1 in SKILL.md (SKILL-3CASE OK), `Case B` count=2 in SKILL.md (SKILL-CASEB OK), `3-case decomposition` count=2 in report-template.md (TEMPLATE-3CASE OK), `by construction` count=2 in report-template.md (TEMPLATE-HEADER OK). All four gates emit the OK marker. |
| 6a | AC6: SKILL.md line 65 unchanged | PASS | Read SKILL.md:65 — reads "If the diagnosis says \"the test is incorrect but the code is also missing a guard\" — surface BOTH in `Files to change` but keep `test_is_wrong=false` since the code is the load-bearing fix." — byte-identical to pre-edit text. |
| 6b | AC6: SKILL.md line 69's earlier sentences (consistency_with_docs=aligned/conflicts) unchanged | PASS | Read SKILL.md:69 — preserved sentences: "set `behavior_is_documented=true` when the chosen hypothesis card's `consistency_with_docs=aligned`..." and "If `consistency_with_docs=conflicts`, the docs side with the user — keep the flag false and proceed with normal code remediation." both intact before the new 3-case clause appended. |
| 6c | AC6: SKILL.md line 71 ("This flag exists...") unchanged | PASS | Read SKILL.md:71 — reads "This flag exists so downstream automation knows to NOT auto-apply a code fix when the observed behavior is the contracted behavior — the remediation target is the spec, the docs, or a stakeholder discussion." — preserved. |
| 6d | AC6: report-template.md line 177 + earlier 3-condition list unchanged | PASS | Read report-template.md:173-177 — "Set `Behavior is documented: true`..." preamble plus 3-condition numbered list (Wave 1.5 doc card / consistency_with_docs=aligned / fix would require spec change) all intact. |
| 6e | AC6: report-template.md line 181 (### Rendering rules header) unchanged | PASS | Read report-template.md:181 — reads "### Rendering rules when `Behavior is documented: true`" — preserved. |
| 7 | Cross-site consistency of case labels A/B/C and triggers | PASS | Compared Case A/B/C across all 4 edit sites: SKILL.md:51 references "Case B in the derivation rule" (consistent with SKILL.md:69 Case B trigger "failing artifact IS a test"); SKILL.md:69 and report-template.md:179 both use Case A=user expectation diverges, Case B=test contradicts docs+code consensus, Case C=code violates docs. Triggers consistent: Case A flag outcomes match in both files; Case B `test_is_wrong=true` resolution matches header comment at line 18; Case C "both false" matches in both. No drift detected. |

## Summary

- Checks passed: 11 / 11
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (no fixes required)

## Issues Found

None.

## Actions Taken

No remediation required — all acceptance criteria satisfied.

## Confidence

- Verified: 11/11 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Tool engagement: Read: 5 | Grep: 0 | Glob: 0 | Bash: 2 (grep gates + label consistency)
- All 11 checks verified with direct tool-output evidence: file:line citations from Read, byte-count grep gates from Bash, cross-file label comparison from Bash grep -n. No item relies on inference.

## Recommendations

Green light to proceed to next phase. The 3-case decomposition is internally consistent across all 4 edit sites, surrounding paragraphs preserved exactly, and all 4 grep gates pass.

## QA Complete
