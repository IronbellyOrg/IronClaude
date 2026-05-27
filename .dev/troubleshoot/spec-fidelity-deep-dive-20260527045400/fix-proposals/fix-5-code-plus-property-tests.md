# Fix Proposal #5 — Tier 1 code + property-based + flatline-halt tests (Tier 2 / quality-engineer)

## Problem statement

The recurrent failure is enabled by a TEST-DESIGN DEFECT that ships the code defect undetected each release. Three coverage gaps allow the present TUIBBS shape (54 HIGH `phantom_id`, flatline 58→54→54, misleading TurnLedger halt) to be invisible in CI: (1) `test_structural_checkers.py` exercises `phantom_id` with one fixture (FR-99) and never with an asymmetric ID-form pair; (2) `test_convergence.py::decreasing_checkers` covers monotone descent but NO flatline-at-N>0 shape; (3) `test_remediate_executor.py` covers per-patch rejection but NO integration test for "when every fix exceeds 30%, halt verdict identifies structural ceiling not budget exhaustion." The minimum fix is the Tier 1 code change PLUS test expansion that closes all three gaps, including a property-based test that would have caught the comparator asymmetry at construction.

## Proposed change

**Layer A — code (identical to Fix Proposal #1):**

`structural_checkers.py` — add `_canonicalize_requirement_id` helper + modify phantom_id block at lines 372-391 + emit `id_schema_drift` as MEDIUM for canonical-match-but-form-differs cases. ~15 LOC. Pure function, NFR-4 compliant.

**Layer B — tests (the load-bearing new contribution):**

1. **Golden-fixture asymmetric-ID tests** in `tests/roadmap/test_structural_checkers.py` (~50 LOC):
   - `test_phantom_id_canonicalizes_zero_padded_d_ids` — spec={D1,D3,D5} roadmap={D01,D03,D05} → 0 HIGH, 3 MEDIUM
   - `test_phantom_id_genuine_phantom_still_emits_high` — spec={D1,D3} roadmap={D01,D99} → 1 HIGH + 1 MEDIUM
   - One fixture pair per family (FR/NFR/SC/G/D) covering D01↔D1 AND FR-7.1↔FR-7-1 styles

2. **Property-based comparator test** in NEW `tests/roadmap/test_structural_checkers_properties.py` (~40 LOC):
   - `pytest.importorskip("hypothesis")` guard (matches `tests/sprint/test_property_based.py` precedent — `hypothesis` is referenced in pyproject markers but not declared as dep)
   - `@given(id_form_pairs())` strategy yielding `(canonical, surface_variants)` tuples
   - Assert: for every `(c, v)`, `check_signatures` on spec-with-c + roadmap-with-v produces 0 HIGH `phantom_id`

3. **Flatline-halt integration test** in `tests/roadmap/test_convergence.py` (~30 LOC, sibling to `test_convergence_loop_three_runs:911`):
   - `test_flatline_halt_emits_structural_verdict` — driver returns 58 findings on n=1, 54 on n=2, 54 on n=3 (TUIBBS shape). Assert NOT passed AND halt-reason text contains structural-unfixability marker (e.g. `"id_schema_drift"` or `"no structural progress"`), NOT only `"Convergence not reached"`. After Layer A lands, same fixture passes on Run 1 (regression lock).

4. **Cross-cutting "all-findings-unfixable" integration test** in `tests/roadmap/test_remediate_executor.py` (~25 LOC, sibling to `test_large_change_rejected:708`):
   - `test_loop_reports_structural_when_all_remediations_exceed_diff_guard` — registry where every active finding's only candidate patch exceeds 30% guard; assert terminal verdict identifies structural ceiling, not budget exhaustion.

Total: ~15 production LOC + ~150 test LOC across 4 files (1 production, 1 new test, 3 modified tests).

## Evidence

- `src/superclaude/cli/roadmap/structural_checkers.py:380-391` — the comparator (Layer A target)
- `tests/roadmap/test_structural_checkers.py:152, 258` — current `phantom_id` test (FR-99 only)
- `tests/roadmap/test_spec_parser.py:191-192` — extract_requirement_ids test (no asymmetric-form pair)
- `tests/roadmap/test_convergence.py:923-950` — `decreasing_checkers` (monotone only)
- `tests/roadmap/test_remediate_executor.py:686-749` — per-patch tests (no integration test for all-fixes-rejected scenario)
- `tests/sprint/test_property_based.py` — `importorskip("hypothesis")` precedent
- `historical-context.md` Pattern 2 — distinct-shape recurrence (test gap fingerprint)

## Risks

- **`hypothesis` dependency posture**: proposal uses `pytest.importorskip` to avoid policy decision; test silently skips in environments without hypothesis. Risk: skipped tests provide no protection until hypothesis is installed in CI.
- **Over-canonicalization** (same as fix-1)
- **Flatline test fragility**: integration test asserts on halt-message shape; later refactors must update. Mitigation: switch to structured `result.halt_reason` enum once defined.
- **5 family-specific tests grow over time**: mitigated by family-agnostic property-based test (Layer B(2)).
- **Doesn't address LLM attention drift** (Pattern 1) — complementary 5-vote-consensus needed but separate hypothesis.

## Test plan

(Test plan IS the proposal — see Layer B above.)

## Documented constraints to honor

### Restrictions
1. Module ownership — Layer A code in `structural_checkers.py`; tests in `tests/roadmap/`. [COMPLIES]
2. Pure-function contract — Layer A helper pure; property-based tests pure. [COMPLIES]
3. 30% per-patch guard — Layer A ~15 LOC in 700-line file; test files exempt from production-patch guard. [COMPLIES]
4. Binary pass condition — Layer A demotes drift to MEDIUM; convergence.py unmodified. [COMPLIES]
5. Spec is input. [COMPLIES]
6. `max_runs=3`. [COMPLIES]
7. Canonicalization precedent. [LEVERAGED]

### Re-frame signals
1. No shipped fix has touched the comparator — this fix does AND adds tests that would have caught the bug at construction. [ADDRESSES]
2. Failure shape has shifted — property-based tests are family-agnostic and provide automatic coverage for next rule_id IF tied to `_REQUIREMENT_PATTERNS.keys()`. [PARTIAL — protects ID-class drift specifically; does not preclude next non-ID shape]
3. Chosen remediation surface is `structural_checkers.py`. [ALIGNED]
