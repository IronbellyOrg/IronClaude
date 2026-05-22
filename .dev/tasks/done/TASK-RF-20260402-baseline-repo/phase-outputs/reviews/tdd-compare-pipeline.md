# TDD Comparison: Pipeline Step Execution (Test 1 vs Test 3)

**Generated**: 2026-04-02
**Purpose**: Compare pipeline step execution order and gate results from .roadmap-state.json

---

## Pipeline Step Order Comparison

### Test 1 (TDD) — .roadmap-state.json

| Step # | Step Name | Status | Attempt |
|---|---|---|---|
| 1 | extract | PASS | 1 |
| 2 | generate-opus-architect | PASS | 1 |
| 3 | generate-haiku-architect | PASS | 1 |
| 4 | diff | PASS | 1 |
| 5 | debate | PASS | 1 |
| 6 | score | PASS | 1 |
| 7 | merge | PASS | 1 |
| 8 | anti-instinct | FAIL | 1 |
| 9 | wiring-verification | PASS | 1 |

### Test 3 (Spec) — .roadmap-state.json

| Step # | Step Name | Status | Attempt |
|---|---|---|---|
| 1 | extract | PASS | 1 |
| 2 | generate-opus-architect | PASS | 1 |
| 3 | generate-haiku-architect | PASS | 1 |
| 4 | diff | PASS | 1 |
| 5 | debate | PASS | 1 |
| 6 | score | PASS | 1 |
| 7 | merge | PASS | 2 |
| 8 | anti-instinct | FAIL | 1 |
| 9 | wiring-verification | PASS | 1 |

---

## Step-by-Step Comparison

| Aspect | Test 1 (TDD) | Test 3 (Spec) | Match? |
|---|---|---|---|
| Total steps | 9 | 9 | YES |
| Step names (ordered) | extract, generate-opus-architect, generate-haiku-architect, diff, debate, score, merge, anti-instinct, wiring-verification | same | YES |
| Step order | Identical | Identical | YES |
| Schema version | 1 | 1 | YES |
| Agents | opus-architect, haiku-architect | opus-architect, haiku-architect | YES |
| Depth | standard | standard | YES |

---

## Gate Results Comparison

| Gate | Test 1 (TDD) | Test 3 (Spec) | Match? |
|---|---|---|---|
| extract | PASS | PASS | YES |
| generate-opus-architect | PASS | PASS | YES |
| generate-haiku-architect | PASS | PASS | YES |
| diff | PASS | PASS | YES |
| debate | PASS | PASS | YES |
| score | PASS | PASS | YES |
| merge | PASS (attempt 1) | PASS (attempt 2) | YES (both pass; Test 3 required retry) |
| anti-instinct | **FAIL** | **FAIL** | YES (both fail) |
| wiring-verification | PASS | PASS | YES |

---

## Anti-Instinct FAIL Confirmation

Both pipelines FAIL the anti-instinct gate:
- **Test 1**: fingerprint_coverage = 0.76 (with 5 undischarged obligations)
- **Test 3**: fingerprint_coverage = 0.67

The anti-instinct audit is a quality gate that checks roadmap fidelity against extraction fingerprints. Both runs fail this gate, confirming consistent pipeline behavior regardless of TDD vs spec input.

---

## Wiring-Verification as Trailing Step

Both pipelines execute wiring-verification as the final (9th) step, after anti-instinct. This confirms:
- wiring-verification runs regardless of anti-instinct gate status
- wiring-verification is a trailing diagnostic, not a blocking gate
- Both produce identical wiring results (166 files, 7 orphan modules, 0 blocking) because wiring-verification scans the codebase, not the roadmap artifacts

---

## Timing Comparison

| Metric | Test 1 (TDD) | Test 3 (Spec) |
|---|---|---|
| Spec file | test-tdd-user-auth.md | test-spec-user-auth.md |
| Total pipeline time | ~13 min 43 sec | ~28 min 49 sec |
| Extraction time | 158.6 sec | 73.3 sec |
| Merge attempts | 1 | 2 |

Test 1 extraction took longer (158.6s vs 73.3s) because the TDD source document is larger and produces more content. Test 3 merge required a retry (attempt 2).

---

## Verdict: **PIPELINE_EQUIVALENCE_CONFIRMED**

Both tests execute the same 9 steps in the same order. Both have anti-instinct FAIL as a gate result. Both have wiring-verification as a trailing step. The pipeline structure is identical regardless of whether the input is a TDD or spec document.
