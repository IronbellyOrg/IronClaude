# QA Report — Structural Conformance / Internal Consistency (FR-RH2 R6)

**Topic:** Widen reflect Tier-2 adversarial seam to an `AdversarialResult` result object
**Date:** 2026-06-22
**Phase:** report-validation (final QA gate, STRUCTURAL lens)
**Fix authorization:** false (REPORT ONLY)
**Lens:** template-conformance / internal-consistency

---

## Overall Verdict: PASS

Zero issues found across the five verification criteria. Adversarial stance applied: I assumed ≥10 defects and hunted field-by-field, traced every kwarg end-to-end against the live `contract.py` routing, and executed the load-bearing tests. The change is internally consistent and the dataclass/seam/builder/contract layers map 1:1.

---

## Criterion 1 — `AdversarialResult` dataclass: six fields, correct types/defaults

VERIFIED at `src/superclaude/cli/reflect/ensemble.py:72-99`.

| # | Field | Expected | Actual (line) | Result |
|---|-------|----------|---------------|--------|
| 1 | `convergence_score` | `float \| None`, no default (required positional) | `convergence_score: float \| None` (L87) — no default | PASS |
| 2 | `regression_present` | `bool` default `False` | `regression_present: bool = False` (L88) | PASS |
| 3 | `unauthorized_deviation_present` | `bool` default `False` | (L89) | PASS |
| 4 | `needs_human_decision` | `bool` default `False` | (L90) | PASS |
| 5 | `deviation_count_by_class` | `dict[str,int]`, `default_factory` → 4-key all-zero | `dataclasses.field(default_factory=lambda: {...})` (L91-98), keys `authorized/necessary/drift/regression` all `0` | PASS |
| 6 | `report_path` | `str \| None` default `None` | `report_path: str \| None = None` (L99) | PASS |

Field ORDER is valid: the only non-default field (`convergence_score`) precedes all defaulted fields, so the dataclass compiles (no "non-default argument follows default argument" error). The 4-key dict matches `_DEVIATION_KEYS = ("authorized","necessary","drift","regression")` at `contract.py:40` exactly.

## Criterion 5 (mutable-default sub-check, folded here) — no mutable-shared default

VERIFIED. `deviation_count_by_class` uses `dataclasses.field(default_factory=lambda: {...})` (ensemble.py:91-92), NOT a shared literal. Each `AdversarialResult()` instance gets its own dict — no cross-instance aliasing. The `build_reflect_contract` mirror default also avoids the trap: it declares `deviation_count_by_class: dict[str, int] | None = None` (L469) and rebuilds a fresh dict inside the body when `None` (L493-499). Both layers clean on the mutable-default axis.

---

## Criterion 2 — Seam-alias / scorer / builder signatures internally consistent (1:1 field trace)

VERIFIED. Type alias `AdversarialScoreFn = Callable[[list[str], Path], AdversarialResult | None]` (ensemble.py:103) is widened in lockstep with the dataclass return type and the default scorer signature `run_adversarial_scorer(...) -> AdversarialResult | None` (L319). The two seam call-sites in `run_tier2_ensemble` (default scorer L255-259; injected `adversarial_score_fn` L261-264) both assign to `adversarial_result: AdversarialResult | None` (L252) — call shapes match the alias `(list[str], Path)`.

End-to-end 1:1 trace of all 5 deviation/regression fields — `AdversarialResult` attribute → seam-call local → `build_reflect_contract` kwarg → returned contract dict key:

| Field | AdversarialResult attr | local (ensemble.py) | builder kwarg (call L304-308) | builder param (def L467-470) | returned dict key (L520-523) |
|-------|------------------------|---------------------|------------------------------|------------------------------|------------------------------|
| regression | `regression_present` | `regression_present` (L275-279) | `regression_present=` | `regression_present` | `"regression_present"` |
| unauth. dev. | `unauthorized_deviation_present` | (L280-284) | `unauthorized_deviation_present=` | `unauthorized_deviation_present` | `"unauthorized_deviation_present"` |
| human dec. | `needs_human_decision` | (L285-289) | `needs_human_decision=` | `needs_human_decision` | `"needs_human_decision"` |
| counts | `deviation_count_by_class` | (L290-294, `None` when no result) | `deviation_count_by_class=` | `deviation_count_by_class` | `"deviation_count_by_class"` |
| report | `report_path` | `adversarial_report_path` (L295-297) | `adversarial_report_path=` | `adversarial_report_path` | flows to `_select_report_path` → `"report_path"` |

No missing-kwarg-forwarding, no name drift, no orphaned param. The `convergence_score` field flows separately via the pre-existing `adversarial_convergence_score` path (L268-269 → L302 kwarg → L514 dict key) — also intact.

The seam-result-is-`None` (child failure) path is handled consistently: each local is a conditional defaulting to clean (`False` for the booleans, `None` for counts/report), preserving the null-convergence DEGRADE fallback per the in-code comments (L265-274). When `deviation_count_by_class` arrives as `None`, the builder rebuilds the all-zero dict (L493-499) — no `None` leaks to the contract.

## Criterion 3 — `user_decision_required` MIRRORS `needs_human_decision`

VERIFIED at `build_reflect_contract` return dict, ensemble.py:522-523:
```
"needs_human_decision": needs_human_decision,
"user_decision_required": needs_human_decision,
```
Both keys are bound to the SAME `needs_human_decision` local — exact value mirror, no independent `user_decision_required` parameter. This matches the contract.py routing where BOTH `needs_human_decision is True` (L319) and `user_decision_required is True` (L321) independently route HALTED, and the AUTO-FIXABLE/HUMAN-REQUIRED classifier reads both (L357-360). The mirror is corroborated by the U11 test assertion `clean["user_decision_required"] is False` alongside `clean["needs_human_decision"] is False` (test_ensemble_unit.py:327-328).

---

## Criterion 4 — I12 test reuses helpers + driver pattern; `_const_score` + U11 structurally consistent

VERIFIED at test_ensemble_stub_integration.py:474-531 and test_ensemble_unit.py:294-334.

I12 (`test_i12_seam_regression_does_not_pass`) helper reuse:
- Reuses `_config(temp_tasklist, reviewers=3)` (L505) — the existing module helper (def L98-105).
- Reuses `_distinct_stub` as `transport_for_slot` (L508) — the existing vendor-distinct factory (def L89-95).
- Drives the REAL pipeline: `run_tier2_ensemble(...)` → `parse_contract(config.contract_path)` → `derive_verdict(...)` (L506-517), matching the documented `_run` driver pattern (def L108-122). I12 inlines the driver (rather than calling `_run`) because it injects a custom `_regression_score` instead of `_const_score` — this is correct, since `_run` hard-codes `adversarial_score_fn=_const_score`. The inline form is the documented "real `run_tier2_ensemble`/`parse_contract`/`derive_verdict` driver pattern."
- Injects `AdversarialResult(regression_present=True)` via the `adversarial_score_fn` seam (L488-503, L509) — the production seam, never patching `ClaudeProcess`. Booleans are genuine Python `True` (not `"true"`/`1`), so the strict `is True` halt trigger fires rather than self-BLOCKing on `malformed-contract-boolean`.

I12 routing assertions are CORRECT against live `contract.py`: with 3 distinct-vendor survivors the contract has `t2_model_class_diversity=="full"` (no DEGRADE trigger 7), `t2_vendor_diversity=="multi"` (no trigger 8), `adversarial_unavailable=False` (no trigger 9), `merge_method=="adversarial"` (no trigger 10), `adversarial_convergence_score=0.86` non-None (no trigger 11). The DEGRADE chain is fully bypassed, so `_halted_reason` reaches `regression_present is True` → `"regression"` (contract.py:315-316) → `Verdict.HALTED`, exit 10. Assertions `result.verdict is Verdict.HALTED`, `exit_code == 10`, `reason == "regression"`, `result.verdict is not Verdict.PASS`, `result.verdict is not Verdict.DEGRADED` (L519-531) are all consistent with the routing. EXECUTED: test PASSES.

`_const_score` stub (L43-60) is structurally consistent with the widened seam: returns a clean-default `AdversarialResult` (`convergence_score=_FIXED_SCORE`, all 3 booleans `False`, all-zero counts, `report_path=None`). Signature `(_paths: list[str], _out: Path) -> AdversarialResult` matches `AdversarialScoreFn`. All three legacy injection sites (`_run`, I8 L351, I9 L376) consume this single widened stub transitively — no stale `-> float` stub remains. EXECUTED: I1 (which routes through `_const_score`) PASSES.

U11 companion (`test_u11_build_reflect_contract_threads_regression_fields`, L294-334) is the unit-level mirror: calls `build_reflect_contract` directly with the new kwargs and asserts both the flagged path (`regression_present is True`, `deviation_count_by_class["regression"] == 1`) and the clean-default path (all 4 booleans `False` incl. mirrored `user_decision_required`, all-zero counts). WorkerResult fixtures use only `index=/status=/model_id=` kwargs — confirmed valid against the `WorkerResult` dataclass (swarm/models.py:1027+, all three are declared fields with defaults). EXECUTED: U11 PASSES.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | AdversarialResult 6 fields/types/defaults | PASS | ensemble.py:87-99 field-by-field table; order valid; keys match _DEVIATION_KEYS |
| 2 | Seam alias / scorer / builder 1:1 consistency | PASS | alias L103, scorer L319, full 5-field trace attr→local→kwarg→param→dict-key |
| 3 | user_decision_required mirrors needs_human_decision | PASS | ensemble.py:522-523 same local; contract.py:319/321 dual routing; U11 L327-328 |
| 4 | I12 reuses _config/_distinct_stub + real driver; _const_score/U11 consistent | PASS | test L474-531, L43-60, L294-334; 3 tests EXECUTED green |
| 5 | No typos / type-mismatch / missing-forward / mutable-shared default | PASS | default_factory L91-92 + builder rebuild L493-499; all 4 bools in _LOAD_BEARING_BOOL_FIELDS contract.py:47-57 |

## Summary

- Checks passed: 5 / 5
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found

None. (Adversarial stance: I searched for ≥10 defects — field name typos, a bool emitted as str/int, a dropped kwarg, an un-mirrored `user_decision_required`, a mutable-shared dict default, a stale `-> float` stub, a DEGRADE trigger masking the I12 HALT, an invalid dataclass field order, a wrong assertion in I12/U11, and a WorkerResult kwarg mismatch. Each candidate was checked against source and refuted with the cited evidence above.)

## Confidence Gate

- **Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 5 | Grep: 0 | Glob: 0 | Bash: 5 (4 grep/sed verification calls + 1 pytest execution)
- No web research performed (all claims are local-source-truth; nothing external to verify).
- Every checklist item is VERIFIED with tool-cited evidence (file:line + 3 executed tests). No UNCHECKED, no UNVERIFIABLE items.

## QA Complete
