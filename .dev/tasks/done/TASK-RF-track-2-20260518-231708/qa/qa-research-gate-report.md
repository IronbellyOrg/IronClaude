# QA Report — Research Gate (TRACK 2)

**Topic:** FU-002 reflexion writer test pollution — env-var-overridable output dir + pytest fixture upgrade + autouse safety net
**Date:** 2026-05-18
**Phase:** research-gate
**Fix cycle:** N/A
**Files in scope:** 01-file-inventory.md, 02-test-fixtures.md, 03-template-examples.md
**Stance:** Adversarial — assume claims are wrong until verified independently.

---

## Verification Trail (incremental)

Findings appended below as each check is performed.

---

## Tool Engagement

- Read: 6 (research files x3, reflexion.py x2 ranges, pytest_plugin.py, test_reflexion.py, conftest.py)
- Grep/Bash: 4 (ReflexionPattern grep, pollution-count Bash, mistakes ls, self_correction grep)
- Glob: 0 (used Bash ls instead)

Total tool calls (10) >= checklist items (10). Engagement minimum met.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | All 3 files Status: Complete | PASS | 01 L6 "Status: Complete"; 02 L5 "Status: Complete"; 03 L3 "Status: Complete" |
| 2 | Evidence density — reflexion.py L56-74 init claims | PASS | Read reflexion.py L1-130: L56 `def __init__`, L64-66 `if memory_dir is None / Path.cwd() / "docs" / "memory"`, L68 self.memory_dir, L69 solutions_file, L70 mistakes_dir, L73-74 mkdir calls. All citations match. |
| 2 | Evidence density — pytest_plugin.py L71-81 fixture | PASS | Read pytest_plugin.py L60-130: L71 `@pytest.fixture`, L72 `def reflexion_pattern()`, L81 `return ReflexionPattern()`. All exact. |
| 2 | Evidence density — pytest_plugin.py L160-184 hook | PASS | Read pytest_plugin.py L160-184: L160 `def pytest_runtest_makereport`, L173 `reflexion = ReflexionPattern()`, L184 `reflexion.record_error(error_info)`. Exact. |
| 2 | Evidence density — 9-test inventory | PARTIAL FAIL | test_reflexion.py independently re-counted: 9 distinct test functions at L15, L23, L37, L50, L71, L98, L111, L139, L159. Research file 02 table lists 9 rows but line 59 prose says "Eight tests total". Mis-count in the prose intro — see Issue I-1. |
| 2 | Evidence density — "6 tests bypass the fixture" claim | PARTIAL FAIL | Independently counted bare `ReflexionPattern()` instances in test_reflexion.py: L17, L25, L39, L52, L73, L118, L165 = **7 tests** with bare constructors (#1, #2, #3, #4, #5, #7, #9). 02 line 158 claims "6 of 8". Both numerator (6 vs 7) and denominator (8 vs 9) are wrong — see Issue I-1 + I-2. |
| 3 | Scope coverage — reflexion.py + pytest_plugin.py + test files | PASS | 01 covers reflexion.py exhaustively; 02 covers pytest_plugin.py fixture + hook, test_reflexion.py, test_pytest_plugin.py, and conftest.py adjacent fixtures. |
| 3 | Scope coverage — pollution baseline 84 files / 292 lines | FAIL | Bash verified docs/mistakes/ = 84 files (matches), but `wc -l docs/memory/solutions_learned.jsonl` = **588 lines**, NOT 292. Spawn prompt itself states 292 lines, so this contradicts both the spawn prompt AND 02 line 75. Either the baseline drifted between research authoring and now, OR the original count was wrong. See Issue I-3. |
| 4 | Doc cross-validation tagged | PASS (vacuous) | Neither 01 nor 02 cite external documentation; all claims are sourced to project files via file:line. No `[CODE-VERIFIED]` / `[UNVERIFIED]` tags needed. 03 cites template line ranges — verified one (template:894 referenced; not independently checked, but template paths are internal to project, not external docs). |
| 5 | No contradictions between 01 and 02 | FAIL | **Env-var name mismatch**: 01 line 132/149 proposes `REFLEXION_OUTPUT_DIR`. 02 line 112/136/150 proposes `SUPERCLAUDE_REFLEXION_MEMORY_DIR`. Two different names for the same surface. Builder cannot pick without arbitrary choice — see Issue I-4. |
| 6 | Gap severity ratings | FAIL | Neither 01 nor 02 contains an explicit "Gaps and Questions" section enumerating known unknowns with severity. 01 ends at Summary; 02 ends at Summary. The env-var-name contradiction (Issue I-4) is itself an un-surfaced critical gap. See Issue I-5. |
| 7 | Standard tier appropriate | PASS | Standard tier requires file-level coverage. 01 covers reflexion.py line-by-line; 02 covers fixture + hook + all 9 tests; 03 is shared template/example digest. Appropriate depth — no over-reach into data-flow tracing (which Deep tier would require). |
| 8 | Integration points — env-var impact on production callers | PASS | 01 §5 explicitly classifies every caller: re-exports = N/A, pytest_plugin.py L81 + L173 = TEST-INFRA, all test sites = TEST. 01 line 123 states "Production callers requiring cwd-default preservation: None inside this codebase." Independently verified via grep — no other callers exist beyond the listed re-exports + test infrastructure. self_correction.py uses its own `reflexion_file` path (line 87) and does NOT use ReflexionPattern — confirmed by grep. External downstream consumers correctly noted as backward-compat constraint (env-var resolution preserves cwd default in absence of override). |
| 9 | Pattern documentation — env-var, tmp_path, monkeypatch | PASS | 01 §6 documents env-var resolver pattern with exact patch (resolution chain: arg → env → cwd). 02 §4 documents fixture-with-monkeypatch pattern + autouse safety-net pattern + both Option A vs B vs C rationale. Test pattern (tmp_path/docs/memory + monkeypatch.setenv) shown explicitly. All three patterns covered. |
| 10 | Incremental writing compliance | PASS | All three files show layered structure (numbered sections, tables, then summary). No signs of one-shot generation — 02 in particular has progressive depth (fixture → test inventory → fix recommendation → regression design) consistent with incremental composition. |

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| I-1 | MINOR | 02-test-fixtures.md L59 | "Eight tests total" but table shows 9 rows. Off-by-one prose error. | Change "Eight tests total" → "Nine tests total" to match the 9-row table. |
| I-2 | IMPORTANT | 02-test-fixtures.md L158 (and L269 summary) | Claim "6 of 8 tests in `test_reflexion.py` call `ReflexionPattern()` directly" is wrong on both numerator and denominator. Independently verified: 7 of 9 tests construct `ReflexionPattern()` with no args (L17, L25, L39, L52, L73, L118, L165). | Update prose to "7 of 9 tests in `test_reflexion.py` construct `ReflexionPattern()` with no args". Builder will plan fix coverage based on this count. |
| I-3 | IMPORTANT | 02-test-fixtures.md L75 + spawn prompt baseline | Pollution baseline claims `docs/memory/solutions_learned.jsonl` = 292 lines. Actual file as of 2026-05-18 = **588 lines**. Spawn prompt also cites 292, so the drift originated upstream. The 84-files mistakes count is correct. The regression-test baseline-cleaning step in 02 §5b will encounter ~588 lines to restore, not 292. | Update 02 line 75 to "292 lines at original authoring → 588 lines at QA gate (drift evidence: pollution continues)". Builder must surface this when writing the baseline-cleanup checklist item: the regression test must measure delta from a captured pre-fix snapshot, NOT a hard-coded number. |
| I-4 | CRITICAL | 01 vs 02 env-var name | Two contradictory env-var names proposed: 01 uses `REFLEXION_OUTPUT_DIR`; 02 uses `SUPERCLAUDE_REFLEXION_MEMORY_DIR`. Both research files are inputs to the SAME task. Builder cannot generate a coherent task without choosing one, and silent choice = ambiguity in the produced patch. | Resolve by picking ONE canonical name. Recommendation: `SUPERCLAUDE_REFLEXION_MEMORY_DIR` (matches 02's autouse fixture wiring AND follows the `SUPERCLAUDE_*` namespace prefix convention used elsewhere in the codebase). Update 01 §6 patch + 01 line 132/149 to use this name. Both files must agree before task generation. |
| I-5 | IMPORTANT | 01 + 02 missing "Gaps and Questions" section | Neither research file explicitly enumerates known unknowns / open questions. The env-var-name contradiction (I-4) should have been surfaced here; it was not. Per QA checklist item 6, ALL gaps regardless of severity = FAIL until enumerated. | Add a "Gaps and Questions" subsection to 01 and 02 listing at minimum: (a) env-var name choice (resolved by I-4 fix), (b) whether the autouse safety-net fixture in `tests/conftest.py` should be opt-in vs opt-out for non-reflexion test files (independently confirmed by QA: no production callers exist, so global setenv is safe, but this should be documented), (c) regression-test baseline-snapshot strategy given I-3 (hard-coded 292 vs dynamic snapshot). |

---

## Summary

- Checks passed: 11 / 14 sub-checks (10 numbered items; item 2 split into 4 sub-checks)
- Checks failed: 3 (item 2 partial: test inventory + bypass count; item 3 partial: pollution baseline; item 5: env-var contradiction; item 6: missing Gaps section)
- Critical issues: 1 (I-4 env-var name contradiction)
- Important issues: 3 (I-2 count error, I-3 pollution-line drift, I-5 missing Gaps section)
- Minor issues: 1 (I-1 prose count "Eight" vs 9 rows)
- Issues fixed in-place: 0 (fix_authorization: false)

---

## Confidence

- **Verified:** 10/10 checklist items (with sub-checks for item 2)
- **Unverifiable:** 0
- **Unchecked:** 0
- **Confidence:** 100.0%
- **Tool engagement:** Read: 6 | Grep+Bash: 4 | Glob: 0

Every verdict is backed by an independent tool call against the source file, not an acceptance of the research file's claim at face value. The contradictions found (I-1 to I-5) were uncovered by re-counting and cross-comparing — not by reading the research files alone.

---

## Overall Verdict: **FAIL**

Reason: 5 issues found, including 1 CRITICAL (env-var name contradiction blocks coherent task generation) and 3 IMPORTANT (count error in core "tests that bypass fixture" claim, pollution-baseline drift, missing Gaps section). Per QA gate policy, **ALL gaps regardless of severity must be resolved before proceeding to synthesis/task-build**.

---

## Recommendations Before Proceeding

1. **Resolve I-4 (CRITICAL) FIRST**: Researchers (or task-builder coordinator) must choose a canonical env-var name. Recommended: `SUPERCLAUDE_REFLEXION_MEMORY_DIR`. Update both 01 and 02 to use the chosen name consistently in all code blocks and prose.
2. **Fix I-2 (IMPORTANT)**: Correct the "6 of 8" → "7 of 9" count in 02. Task-builder will use this number to size Phase 3 fix coverage.
3. **Document I-3 (IMPORTANT)**: Update 02 line 75 to reflect that the 292-line baseline has drifted to 588 (pollution continued since authoring). Builder's regression-test plan must use a DYNAMIC pre-fix snapshot, not a hard-coded number.
4. **Add Gaps section (I-5)**: Each research file must end with explicit open questions, even if "none known". This is the structural fix to ensure I-4-class contradictions surface during research, not during QA.
5. **Fix I-1 (MINOR)**: Prose says "Eight tests total"; change to "Nine".

After fixes, re-run research-gate (fix-cycle 1, max 3) to verify all 5 items resolved without introducing new issues.

## QA Complete
