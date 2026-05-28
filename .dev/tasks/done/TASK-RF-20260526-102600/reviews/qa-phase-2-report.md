# QA Report — Phase 2 (Implementation — PR A Steps 1-7)

**Topic:** TASK-RF-20260526-102600 PR A Identifier Canonicalization Fix (F1+F3+F5)
**Date:** 2026-05-26
**Phase:** phase-gate (post-implementation, pre-test-verification)
**Fix cycle:** 1
**Branch:** `fix/integration-contracts-mechanism-signature` @ sha `67ab0af5276317f83df05e25e1e620cfa59e7790` + Phase 2 edits
**Mode:** Zero-trust, adversarial stance, `fix_authorization: true`

---

## Overall Verdict: FAIL

The Phase 2 acceptance criteria for code-shape edits (each "ensuring..." clause) are met — every spec'd edit is present at the spec'd location with the spec'd content. HOWEVER, the implementation as spec'd has **introduced 2 regressions in pre-existing tests** (`test_t1` and `test_t7`) AND **1 ruff F401 violation** (`_extract_identifiers` imported but unused). These are CRITICAL/IMPORTANT downstream defects caused by the OQ-1 Option B resolution (`base_tokens = _extract_identifiers(text.upper())`) — the spec itself causes the regressions, so I cannot fix them under `fix_authorization` without violating the acceptance criteria. Escalation required.

---

## Items Reviewed (Acceptance-Criterion Verification)

| # | Acceptance Criterion (from Phase 2 "ensuring..." clauses) | Result | Evidence |
|---|------------------------------------------------------------|--------|----------|
| 2.1a | `TestExtractIdentifiersInvariants` class APPENDED at end of test file (not inserted mid-file) | PASS | Read `tests/roadmap/test_integration_contracts.py:394-410` — class is the final class in the file; no subsequent class definitions. |
| 2.1b | Class docstring is the verbatim single-line form per criterion | PASS | Line 395 contains the exact docstring `"""Behavior-pin tests asserting exact set equality. These are red→green acceptance signals for the canonicalization fix. Substring-based downstream assertions silently green-bar regardless of fix correctness; these pin tests close that gap."""`. Note: criterion-specified single-line form is used (merged-output.md showed a multi-line form; criterion overrides — single-line form is honored). |
| 2.1c | Test 1 is `test_hyphenated_requirement_id_emits_full_token` with body `assert _canonicalize_identifiers("FR-S10-02") == frozenset({"FR-S10-02", "S10"})` (uses `_canonicalize_identifiers`, NOT `_extract_identifiers`, per OQ-1 Option B) | PASS | Lines 397-398 verified exact match. |
| 2.1d | Imports `from superclaude.cli.roadmap.integration_contracts import _extract_identifiers, _canonicalize_identifiers` present in combined import block | PASS (with ruff conflict — see Findings) | Lines 12-18: import block now includes both symbols (alphabetically ordered: `IntegrationAuditResult`, `_canonicalize_identifiers`, `_extract_identifiers`, `check_roadmap_coverage`, `extract_integration_contracts`). |
| 2.2a | Test 2 is `test_mixed_case_canonicalized_via_helper` with body `assert _canonicalize_identifiers("fr-s10-02") == frozenset({"FR-S10-02", "S10"})` | PASS | Lines 400-401 verified exact match. |
| 2.2b | No duplicate import added | PASS | Read import block — only one `from superclaude.cli.roadmap.integration_contracts import (...)` block exists; no F811 redefinition. |
| 2.3a | Test 3 is `test_pascal_case_uppercases_consistently` with verbatim INV-003 guard comment (3 lines) and body `assert _canonicalize_identifiers("ConcreteStrategy") == frozenset({"CONCRETESTRATEGY"})` | PASS | Lines 403-407 verified: 3-line INV-003 comment preserved verbatim from merged-output.md, body matches. |
| 2.4a | Test 4 is `test_empty_text_yields_empty_frozenset` with body `assert _canonicalize_identifiers("") == frozenset()` | PASS | Lines 409-410 verified. |
| 2.4b | Class contains exactly 4 pin tests in order: hyphenated, mixed_case, pascal_case, empty_text. No extra methods. | PASS | Grep confirmed 4 `def test_*` methods within the class; order matches spec. |
| 2.5a | `_canonicalize_identifiers` helper appended after `_signature_subsumed` preceded by a blank line | PASS | `_signature_subsumed` ends at line 442; blank lines 443-444 separate; helper begins line 445. (Note: criterion mentioned "previously last function" — verified `_signature_subsumed` was indeed the last function before this addition.) |
| 2.5b | Helper has 3-invariant docstring verbatim per merged-output.md | PASS | Lines 446-457 contain verbatim docstring matching merged-output.md L131-143. |
| 2.5c | First body line is `base_tokens = _extract_identifiers(text.upper())` (mandatory per OQ-1 Option B) | PASS | Line 458 verified exact. |
| 2.5d | `hyphen_pattern = re.compile(r"\b(?:[A-Z][A-Z0-9]*-)+[A-Z0-9]+\b", re.IGNORECASE)` | PASS | Line 459 verified exact. |
| 2.5e | Return is `return frozenset(t.upper() for t in (base_tokens + hyphen_tokens))` | PASS | Line 461 verified exact. |
| 2.5f | No Args:/Returns: blocks; no `typing` imports added | PASS | Docstring contains only the 3 invariants prose; module-level imports unchanged (only existing `dataclass, field` from `dataclasses` + `re`). |
| 2.6 | Construction site at line 196 area now reads `idents = _canonicalize_identifiers(context)` — surgical single-line replacement, 12-space indent preserved | PASS | Line 196: `            idents = _canonicalize_identifiers(context)` — exactly 12 spaces of indent verified. |
| 2.7a | New line `window_upper = window_text.upper()` inserted between existing `window_text = ...` and `if not any(...)` lines | PASS | Lines 354 (window_text), 355 (window_upper), 356 (`if not any`) verified in correct order. |
| 2.7b | The `if not any(...)` now references `window_upper` instead of `window_text` | PASS | Line 356: `if not any(ident in window_upper for ident in contract_idents):` verified. |
| 2.7c | Original `window_text` assignment NOT removed | PASS | Line 354 retains `window_text = " ".join(roadmap_lines[window_start:window_end])`. |
| 2.7d | 24-space indent preserved | PASS (28-space — same depth as inner Layer 3 block which is correct) | Line 355 has the same indent as the surrounding lines in the inner Layer 3 stem-fallback loop (28 spaces inside `if contract_idents:` block, deeper than the 24-space outer Layer 3 — this matches the pre-existing block structure; the "24-space" mention in the criterion describes the outer block, and the inner inserted lines correctly use the deeper indent appropriate for their position). |
| 2.8a | `test_t1` filter at line 333 area now reads `and "FR-S10-02" in c.mechanism_signature[1]` (NOT `c.spec_evidence`) | PASS | Lines 333-337: list comprehension filter `if c.mechanism == "dispatch_table" and "FR-S10-02" in c.mechanism_signature[1]` — matches spec. (Note: line drifted from 333 to 336 — within "area" tolerance.) |
| 2.8b | Other `c.spec_evidence` occurrences at lines 280 and 300 UNCHANGED | PASS | Lines 283 and 303 (post-import-shift positions) retain `c.spec_evidence` in different test logic (`test_upper_snake_case_detected` and `test_detects_programmatic_runners_without_wiring`) — verified unchanged form. |
| 2.9a | F5 fixture comment at lines 129-132 area is the new 4-line version referencing `_canonicalize_identifiers` | PASS (line drift: actual 131-134, within "area" tolerance) | Lines 131-134 contain the verbatim 4-line replacement: "Synthetic fixture per RQ-1 Option A: TUIBBS-scp-inspired prose with shared" / "hyphenated requirement-ID token \`FR-S10-02\` (canonicalized via" / "\`_canonicalize_identifiers\` — see helper docstring for invariants) in every" / "hub-dispatch context window so \`_signature_subsumed\` fires deterministically." — matches merged-output.md L181-184 verbatim. |
| 2.9b | `TUIBBS_HUB_SPEC = """\` literal UNCHANGED | PASS | Line 135 retains `TUIBBS_HUB_SPEC = """\` followed by the original spec content lines 136-157 unchanged. |
| 2.10a | Grep audit output captured verbatim | PASS | `pr86-prA-grep-audit.md` lines 9-14 contain the exact 4-line grep output. Re-ran the grep myself: matches exactly (260 iterator, 262 Layer 2, 356 Layer 3, 461 helper return). |
| 2.10b | Audit file confirms only Layer 3 was case-sensitive pre-fix and is now remediated | PASS | `pr86-prA-grep-audit.md` lines 16-27 contain the comparison against R1's G3 audit with PASS verdict. |

**Code-shape acceptance criteria: 26/26 PASS.**

---

## Confidence Gate

- **Verified:** 26/26
- **Unverifiable:** 0
- **Unchecked:** 0
- **Confidence:** 100.0%
- **Tool engagement:** Read: 4 | Grep: 2 | Glob: 0 | Bash: 5 | tavily_search: 0 | tavily_extract: 0

Per-criterion verification used: full-file Read of `integration_contracts.py`, full-file Read of `test_integration_contracts.py`, full-file Read of `pr86-prA-grep-audit.md`, targeted Read of merged-output.md L95-205, grep for fixture marker, grep audit re-execution, pytest re-execution (full suite + isolated class), ruff check on touched files, git rev-parse for branch+sha confirmation.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | **CRITICAL** | `tests/roadmap/test_integration_contracts.py::TestHubDispatchRegression::test_t1_one_contract_per_hub_mechanism` (line 330) | **REGRESSION**: Pre-existing test fails post-PR-A. Expects `len(hub_contracts) == 1`, gets **6**. Root cause: `_canonicalize_identifiers(text.upper())` causes the existing `_extract_identifiers` regex (`\b[A-Z][A-Z0-9_]{2,}\b`) to match ALL common English words ≥3 chars (THE, FOR, ARE, USES, PRIORITY, PROCESSED, etc.) when input is upper-cased. The resulting bloated identifier sets prevent `_signature_subsumed` from collapsing 6 contracts down to 1, because each context window contains a slightly different set of common words. The TUIBBS_HUB_SPEC fixture is designed to produce 1 contract via subset-subsumption, and the PR A spec'd helper breaks this invariant. | **Spec-vs-test conflict — orchestrator decision required.** Either (a) re-spec the helper to filter common English stop-words before union, (b) revert OQ-1 Option B to `_extract_identifiers(text)` and accept Test 2 failure (re-open OQ-1), or (c) update TUIBBS_HUB_SPEC fixture + `_signature_subsumed` to handle the polluted token set. Cannot fix under `fix_authorization` without violating acceptance criterion 2.5c (`text.upper()` is mandatory per OQ-1 resolution). |
| 2 | **CRITICAL** | `tests/roadmap/test_integration_contracts.py::TestHubDispatchRegression::test_t7_stem_fallback_without_ident_overlap_uncovers` (line 378) | **REGRESSION**: Pre-existing test fails post-PR-A. Expects `result.uncovered_count >= 1`, gets `0`. Root cause: Spec text "The hub uses class-priority dispatch — FR-S10-02..." now canonicalizes to a token set including `DISPATCH`, `PRIORITY`, `CLASS` (among others). The Layer 3 overlap guard requires ≥1 token overlap with the roadmap window; roadmap text "Implement priority dispatch for logging events" — after `.upper()` — contains `PRIORITY` and `DISPATCH`, satisfying the overlap. The overlap guard now incorrectly matches because canonicalization extracted generic mechanism vocabulary from the contract spec as "identifiers". | Same orchestrator decision as Finding 1 — both fail for the same root cause (token-set pollution from `text.upper()` + permissive `_extract_identifiers` regex). |
| 3 | **IMPORTANT** | `tests/roadmap/test_integration_contracts.py:15` | **Ruff F401**: `_extract_identifiers` imported but unused (after OQ-1 Option B resolution removed direct calls to it from the pin tests). Acceptance criterion 2.1d explicitly mandates this import remain present, creating a spec-vs-lint conflict. | **Spec-vs-lint conflict — orchestrator decision required.** Either (a) drop `_extract_identifiers` from the import (violates acceptance criterion 2.1d), (b) add `# noqa: F401` suppression on the import line, (c) re-introduce a usage of `_extract_identifiers` somewhere in the test class (e.g., a test that directly inspects its return type), or (d) accept the lint failure. Cannot fix unilaterally — criterion 2.1d says the import "MUST be present (combined into the existing import block)". |
| 4 | MINOR | `tests/roadmap/test_integration_contracts.py:131-134` | Line drift: F5 fixture comment is at lines 131-134, not 129-132 as the criterion states. Two-line drift caused by the import-block expansion in Step 2.1 (added 2 import lines, shifting everything below). Criterion language hedges with "area" — within tolerance. | No fix required. Note for future criteria authors: use line ranges with explicit tolerance bands. |

---

## Detailed Regression Reproduction

```
$ uv run pytest tests/roadmap/test_integration_contracts.py -v --no-header 2>&1 | tail -3
FAILED tests/roadmap/test_integration_contracts.py::TestHubDispatchRegression::test_t1_one_contract_per_hub_mechanism - AssertionError: assert 6 == 1
FAILED tests/roadmap/test_integration_contracts.py::TestHubDispatchRegression::test_t7_stem_fallback_without_ident_overlap_uncovers - AssertionError: assert 0 >= 1
========================= 2 failed, 30 passed in 0.16s =========================
```

**Pin tests (the 4 PR A acceptance signals) PASS:**

```
PASSED tests/roadmap/test_integration_contracts.py::TestExtractIdentifiersInvariants::test_hyphenated_requirement_id_emits_full_token
PASSED tests/roadmap/test_integration_contracts.py::TestExtractIdentifiersInvariants::test_mixed_case_canonicalized_via_helper
PASSED tests/roadmap/test_integration_contracts.py::TestExtractIdentifiersInvariants::test_pascal_case_uppercases_consistently
PASSED tests/roadmap/test_integration_contracts.py::TestExtractIdentifiersInvariants::test_empty_text_yields_empty_frozenset
```

So the PR A intent (RED → GREEN on the 4 pin tests) is satisfied. The collateral damage is in two regression tests that were added to defend INV-001 (one-contract-per-mechanism) and the Layer 3 overlap-guard false-positive defense — both of which now misbehave because the spec'd canonicalization is over-eager.

**Ruff finding:**

```
$ uv run ruff check src/superclaude/cli/roadmap/integration_contracts.py tests/roadmap/test_integration_contracts.py
F401 [*] `superclaude.cli.roadmap.integration_contracts._extract_identifiers` imported but unused
  --> tests/roadmap/test_integration_contracts.py:15:5
```

---

## Actions Taken

**None.** `fix_authorization: true` allows fixing in-place, but the 3 issues above cannot be fixed without violating the explicit acceptance criteria provided in the spawn prompt:

- Finding 1 + 2 require either changing `_canonicalize_identifiers`'s body (violates criterion 2.5c which mandates `_extract_identifiers(text.upper())`) or changing the fixture/regression tests (out-of-scope edits not authorized).
- Finding 3 requires either dropping the import (violates criterion 2.1d) or modifying the spec'd test surface beyond what is authorized.

The QA agent's mandate is to FIND defects, not silently make decisions that contradict the upstream spec. These are spec-design defects that surfaced when the spec was executed, and they require orchestrator/user resolution. Reverting OQ-1 Option B, modifying the spec'd fixture, or weakening `_extract_identifiers` are all decisions that need the orchestrator to weigh trade-offs.

---

## Recommendations

1. **Block Phase 3 / Phase 4** — running `uv run pytest tests/roadmap/` (Step 3.2) and the rf-qa gate (Step 4.1) will FAIL because of Findings 1+2. Step 3.2's "Verdict: PASS if 0 failures" criterion cannot be satisfied. Step 3.3's "Verdict: PASS if 0 errors in PR A's touched files" criterion cannot be satisfied (F401 on test file).

2. **Re-open OQ-1.** The adversarial debate that resolved OQ-1 verified pin tests 1-4 would pass under Option B. It did NOT verify that pre-existing tests (`test_t1`, `test_t7`) would still pass. This is a missed adversarial vector. The debate transcript should be amended with the regression vector.

3. **Suggested resolution options for orchestrator:**
    - **Option α (minimum spec drift):** Change `_extract_identifiers` regex to require leading capital + at least one digit OR underscore, e.g., `\b[A-Z][A-Z0-9_]*[_0-9][A-Z0-9_]*\b`, so common words like THE/FOR/USES no longer match but UPPER_SNAKE constants and PascalCase still do. Re-verify pin tests + regressions.
    - **Option β (helper-local filter):** In `_canonicalize_identifiers`, apply a stop-words filter on `base_tokens` from `text.upper()` before unioning. Stop-words list = common 3-letter English words. Risk: arbitrary list.
    - **Option γ (revert + retest pin 2):** Revert to `_extract_identifiers(text)` (no `.upper()`), accept Test 2 fails on lowercase input, and either drop Test 2 or change it to use uppercase input. Re-verify pin tests + regressions.
    - **Option δ (fixture/regression rewrite):** Keep helper as-is, modify TUIBBS_HUB_SPEC + test_t1 + test_t7 to be tolerant of the bloated identifier set (e.g., assert `>= 1` instead of `== 1` for t1, change t7 roadmap to avoid common stem words). Risk: erodes the defense the regressions were guarding.

4. **Ruff F401 fix:** Once Findings 1+2 are resolved, the F401 may resolve itself if a regression-test fix re-introduces a direct call to `_extract_identifiers`. Otherwise add `# noqa: F401` with a comment explaining "exported for symmetric API even though not directly tested" or amend criterion 2.1d.

---

## Summary

- **Code-shape acceptance criteria:** 26/26 PASS (100%). Every spec'd edit is present at the spec'd location with verbatim content.
- **Downstream behavioral correctness:** **FAIL.** 2 pre-existing regression tests now fail; 1 ruff F401 violation introduced. All 3 are caused by the OQ-1 Option B resolution that mandated `_extract_identifiers(text.upper())`.
- **Pin tests (PR A's stated success signal):** 4/4 PASS — the helper does what merged-output.md intended for the 4 pin scenarios.
- **Fixes applied:** None — the defects are spec-design conflicts that cannot be resolved unilaterally by the QA agent under the existing acceptance criteria.

**Verdict: FAIL.** Phase 2 cannot be considered complete until the regressions are resolved by the orchestrator. Blocking Phase 3.

## QA Complete
