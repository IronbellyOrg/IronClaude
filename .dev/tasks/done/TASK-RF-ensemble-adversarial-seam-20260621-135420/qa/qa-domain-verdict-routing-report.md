# QA Report — reflect-verdict-routing (domain lens, FR-RH2 R6)

**Topic:** Seam-to-verdict end-to-end routing — can a regression leak to PASS?
**Date:** 2026-06-22
**Phase:** report-validation (domain lens — adversarial routing trace)
**Fix cycle:** N/A
**fix_authorization:** false (REPORT ONLY — no files edited)

---

## Overall Verdict: PASS

The regression signal **cannot** leak to PASS along the traced path, and the clean-defaults path **still routes PASS**. I traced every hop in actual code and adversarially probed each of the four masking vectors (a)-(d). All four are closed. Detail and file:line evidence below.

---

## The Traced Routing Path (regression=True case)

Each hop grounded in actual code. File paths abbreviated: `ensemble.py` = `src/superclaude/cli/reflect/ensemble.py`; `contract.py` = `src/superclaude/cli/reflect/contract.py`; `models.py` = `src/superclaude/cli/reflect/models.py`.

**HOP 1 — Seam invocation + destructure.**
`run_tier2_ensemble` reaches the seam block at `ensemble.py:252-269`. Gate `ensemble.py:253`: `if adversarial_convergence_score is None and len(succeeded_final_paths) >= 2:`. With 3 distinct stub survivors (I12 uses `_distinct_stub` + `reviewers=3`), `len(succeeded_final_paths) == 3 >= 2` ⇒ branch taken. `adversarial_score_fn` is injected (`ensemble.py:261-264`) ⇒ `adversarial_result = _regression_score(...)` returns a real, non-None `AdversarialResult(regression_present=True, convergence_score=0.86)`. `ensemble.py:268-269`: `adversarial_result is not None` ⇒ `adversarial_convergence_score = 0.86` (NON-None — critical for vector (c)).

**HOP 2 — Local extraction (non-None branch).**
`ensemble.py:275-279`: `regression_present = adversarial_result.regression_present if adversarial_result is not None else False`. `adversarial_result is not None` is True ⇒ `regression_present = True` (the genuine dataclass bool, `ensemble.py:88` field type `bool`, set to `True` at `ensemble.py:491-492`/`test:494`). No coalescing to False occurs.

**HOP 3 — Threading into the builder.**
`ensemble.py:299-309`: `build_reflect_contract(..., regression_present=regression_present, ...)` passes the local `True` as the keyword-only param declared at `ensemble.py:467`.

**HOP 4 — Builder writes the contract field.**
`build_reflect_contract` at `ensemble.py:520`: `"regression_present": regression_present,` — writes the genuine bool `True` directly into the emitted dict. The pre-R6 hard-coded `False` (old diff line, qa-input-surface.md:267) is GONE; replaced by the threaded param. `reviewer_count == 3 >= 1` so the `reviewer_count == 0 → return None` guard at `ensemble.py:483-484` does NOT fire; the dict IS emitted.

**HOP 5 — Emit + YAML round-trip.**
`_emit_reflect_contract` (`ensemble.py:627-636`) `yaml.safe_dump`s the dict to `config.contract_path`. `parse_contract` (`contract.py:65-82`) `yaml.safe_load`s it back. Python `True` → YAML `true` → Python `True` (PyYAML preserves bool identity). So `contract["regression_present"] is True` survives the disk round-trip — confirmed by I12 assertion `test:528`.

**HOP 6 — derive_verdict ordering (blocked → degraded → halted → pass).**
`derive_verdict` (`contract.py:130-246`), first-match-wins ordering documented `contract.py:139`:
- BLOCKED gates (`contract.py:147-209`): `child_rc=0` (I12 passes `child_rc=0`, `test:516`) ⇒ no timeout/crash. `contract is not None`. `contract_version="1.0"` ⇒ major `"1"` passes. `degraded_components=[]` (list) passes. The F2 malformed-bool guard (`contract.py:200-209`) iterates `_LOAD_BEARING_BOOL_FIELDS` (incl. `regression_present`, `contract.py:47-57`); since `regression_present` is a genuine `bool`, `isinstance(_value, bool)` is True ⇒ NOT blocked. **Vector (d) closed.**
- DEGRADED gate (`contract.py:211-225` → `_degraded_reason` `contract.py:249-304`): walked all 14 triggers below; none fire ⇒ `degraded_reason is None`. **Vector (c) closed.**
- HALTED gate (`contract.py:227-232` → `_halted_reason` `contract.py:307-328`): `status != "failed"/"partial"`; then `contract.py:315`: `if contract.get("regression_present") is True: return "regression"` ⇒ FIRES. Returns `"regression"`.
- `derive_verdict` returns `_make_result(Verdict.HALTED, reason="regression", ...)` at `contract.py:229-231`.

**HOP 7 — Exit code.**
`Verdict.HALTED.exit_code == 10` (`models.py:44-49`). Matches I12 assertions `test:522-524`: `verdict is Verdict.HALTED`, `exit_code == 10`, `reason == "regression"`.

**Result: regression=True ⇒ HALTED / exit 10 / reason="regression". NOT PASS. Routing is correct.**

---

## Adversarial Probe: Can the regression be lost or masked? (each vector individually attacked)

### (a) Seam gate `len(succeeded_final_paths) >= 2` — does the regression survive when survivors ≥ 2?

**CLOSED — and the gate is on the WIN side, not a leak.** The gate at `ensemble.py:253` GUARDS WHETHER THE SEAM RUNS AT ALL — it does not suppress a regression once produced. Two cases:
- **survivors ≥ 2** (the I12 case, 3 survivors): gate True ⇒ seam runs ⇒ `adversarial_result` non-None ⇒ regression extracted and threaded (Hops 2-4). Regression survives. ✅
- **survivors < 2**: gate False ⇒ seam SKIPPED ⇒ `adversarial_result` stays `None` (`ensemble.py:252`) ⇒ `regression_present` falls to the `else False` branch (`ensemble.py:278`). BUT this is NOT a leak: with < 2 survivors, `build_reflect_contract` produces `reviewer_count < 2` ⇒ `merge_method = "single-reviewer-fallback"` (`ensemble.py:487`) OR `tier_reached = 1` (`ensemble.py:486`), each of which trips a DEGRADE rung (`_degraded_reason` triggers 6 `degraded-tier1` `contract.py:263-264` / trigger 10 `single-reviewer-fallback` `contract.py:280-281`) → non-PASS regardless. So a < 2-survivor run can never PASS anyway; there is no survivor count at which a regression both (i) cannot be reported and (ii) the run would otherwise PASS. **No leak.** *Adversarial note:* the seam producing no signal at < 2 survivors is by design (no 2nd reviewer to adjudicate divergence), and the degrade floor catches it independently. Verified I2/I5 (`test_ensemble_stub_integration.py:174-197, 251-277`) assert exactly this non-PASS at < 2.

### (b) `None`-result coalescing — does a real (non-None) result preserve `regression_present=True`?

**CLOSED.** The coalescing at `ensemble.py:275-279` is a strict `if adversarial_result is not None else False` ternary. The `else False` arm fires ONLY when `adversarial_result is None` (child-failure path, `run_adversarial_scorer` returns `None` at `ensemble.py:348`). For a real non-None result the `if` arm reads `adversarial_result.regression_present` verbatim — no `or`, no truthiness coercion, no `.get(...) or False` that could swallow a `True`. I12 injects a non-None result ⇒ `True` is read directly. The ONLY way the `else False` masks a `True` is if the result were `None`, but a `None` result carries no `regression_present` to mask in the first place (the field lives on the dataclass instance). **No leak.** This is symmetric across all four booleans (`ensemble.py:275-289`) and the counts dict (`ensemble.py:290-294`).

### (c) DEGRADE rung firing first and masking the HALT — does a healthy ensemble avoid every DEGRADE trigger so HALTED is reached?

**CLOSED — this is the highest-value vector and the test deliberately defuses it.** Because ordering is `degraded → halted` (`contract.py:139, 211-232`), ANY firing DEGRADE rung would short-circuit to DEGRADED (exit 11) and the `regression` HALT at `contract.py:315` would never be consulted — the regression would be MASKED (still non-PASS, but mislabeled, and `classify_fix` human-required routing lost). I walked all 14 `_degraded_reason` triggers (`contract.py:259-303`) against the I12 healthy contract:

| # | Trigger (contract.py) | Fires? | Why not (I12 healthy contract) |
|---|---|---|---|
| 1-5 | degraded-components (`259-260`) | No | `degraded_components == []` (`ensemble.py:525`) — empty, no halt-set token |
| 6 | degraded-tier1 (`263-264`) | No | `expected_tier=2` AND `tier_reached=2` (3 survivors ⇒ `ensemble.py:486`); needs `tier_reached==1` |
| 7 | degraded-model-diversity (`267-269`) | No | `t2_model_class_diversity == "full"` (3 distinct vendor stubs ⇒ `compute_model_class_diversity` `ensemble.py:529-536`); asserted `test:530` |
| 8 | single-vendor (`272-273`) | No | `t2_vendor_diversity == "multi"` (qwen/deepseek/gpt distinct vendors ⇒ `compute_vendor_diversity` `ensemble.py:539-557`) |
| 9 | adversarial-unavailable (`276-277`) | No | `adversarial_unavailable` defaults False (`ensemble.py:174`, not overridden in I12) |
| 10 | single-reviewer-fallback (`280-281`) | No | `merge_method == "adversarial"` (`reviewer_count 3 >= 2` ⇒ `ensemble.py:487`) |
| 11 | **null-convergence (`284-285`)** | **No** | `tier_reached==2` BUT `adversarial_convergence_score == 0.86` (NON-None — Hop 1, `ensemble.py:269`). **This is the exact GAP-4 non-conflation guard the test cites.** If the score were None this rung WOULD fire and mask the HALT. |
| 12 | verification-skipped (`288-291`) | No | `verification_ran` defaults True (`ensemble.py:515`); not False |
| 13 | citations-dropped (`294-298`) | No | `citations_dropped == 0` (`ensemble.py:517`) |
| 14 | input-drift (`301-302`) | No | `input_drift_detected == False` (`ensemble.py:519`) |

All 14 return None ⇒ `_degraded_reason` returns None ⇒ control reaches `_halted_reason` ⇒ `regression`. **No mask.** *Adversarial note:* trigger 11 (null-convergence) is the live trap — and the seam design (`run_adversarial_scorer` docstring `ensemble.py:327-333`) explicitly REFUSES to auto-derive `regression_present` from a low/None score, so a healthy score + real regression cleanly reaches HALTED rather than being conflated into DEGRADE. The test's non-None 0.86 + `assert ... is not Verdict.DEGRADED` (`test:531`) nails this.

### (d) Non-bool self-BLOCK (malformed-contract-boolean) — is `regression_present` a genuine bool True?

**CLOSED.** `AdversarialResult.regression_present` is typed `bool` (`ensemble.py:88`) and set to literal Python `True` in `_regression_score` (`test:494`) — not `"true"`, not `1`. It threads unchanged through `build_reflect_contract` (`ensemble.py:520`), YAML round-trips as `true`→`True`. The F2 guard (`contract.py:200-209`) only BLOCKs when a present load-bearing field `is not None and not isinstance(_value, bool)`; `True` IS a bool ⇒ guard passes, no `malformed-contract-boolean` BLOCK. I12 asserts `contract["regression_present"] is True` (`test:528`, identity check) confirming genuine bool. **No spurious BLOCK, and conversely the `is True` halt at `contract.py:315` (strict identity) genuinely fires** — had a `"true"` string slipped through it would have self-BLOCKed (still non-PASS) but the test proves the clean True path. **No leak.**

---

## Clean-defaults path — does it STILL route PASS?

**Confirmed PASS.** Trace with `regression_present=False`, all-zero counts (the `_const_score` stub `test_ensemble_stub_integration.py:43-60`, exercised by I1 `test:141-171`):
- Seam runs (3 survivors), `adversarial_result` non-None with `regression_present=False`, `convergence_score=0.86` ⇒ `regression_present` local = `False` (`ensemble.py:275-279`, if-arm reads the dataclass `False`).
- `build_reflect_contract` writes `"regression_present": False` (`ensemble.py:520`), `deviation_count_by_class` all-zero, `status="success"`, `tier_reached=2`, `merge_method="adversarial"`, diversity `full`/`multi`, score `0.86`.
- `derive_verdict`: BLOCKED gates pass (genuine bools, version 1, child_rc 0). DEGRADED: all 14 triggers None (same healthy contract as vector (c), score non-None so null-convergence quiet). HALTED (`_halted_reason` `contract.py:307-328`): `status` not failed/partial; `regression_present is True`? **No** (`is False`); other three booleans False; `deviations["regression"]==0`, `deviations["drift"]==0` ⇒ returns None. PASS gate (`contract.py:235`): `status=="success" AND tier_reached==2==expected_tier` ⇒ `Verdict.PASS`, reason `"pass"`, exit 0.
- Verified directly by I1 assertions: `result.verdict is Verdict.PASS`, `exit_code == 0` (`test:168-169`) and U11 clean-branch (`test_ensemble_unit.py:441-452`): `clean["regression_present"] is False`, all-zero counts.

**The clean path PASSes; the regression path HALTs. The seam neither over-blocks the clean case nor leaks the regression case.**

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | HOP 1 seam invocation + gate | PASS | `ensemble.py:253` gate True at 3 survivors; `:261-264` injected fn; `:268-269` non-None ⇒ score 0.86 |
| 2 | HOP 2 non-None local extraction | PASS | `ensemble.py:275-279` if-arm reads `.regression_present` = True; no coercion |
| 3 | HOP 3 builder threading | PASS | `ensemble.py:299-309` kwarg passed to param `:467` |
| 4 | HOP 4 contract field write | PASS | `ensemble.py:520` `"regression_present": regression_present`; hard-coded False removed |
| 5 | HOP 5 YAML round-trip preserves bool | PASS | `_emit` `:627-636` + `parse_contract` `contract.py:65-82`; I12 `test:528` `is True` |
| 6 | HOP 6 derive_verdict ordering → HALTED | PASS | `contract.py:139,211-232`; `_halted_reason` `:315` returns `"regression"` |
| 7 | HOP 7 exit code 10 | PASS | `models.py:44-49`; I12 `test:522-524` |
| 8 | Vector (a) gate ≥2 — regression survives / no leak at <2 | PASS | `ensemble.py:253`; <2 floor degrades via `contract.py:263-264,280-281` |
| 9 | Vector (b) None-coalescing preserves True | PASS | `ensemble.py:275-279` strict `is not None else False`; no truthiness swallow |
| 10 | Vector (c) all 14 DEGRADE triggers quiet on healthy contract | PASS | `contract.py:259-303` walked (table above); null-convergence quiet ∵ score 0.86 |
| 11 | Vector (d) genuine bool, no malformed-BLOCK, `is True` fires | PASS | `ensemble.py:88` type; `test:494` literal True; F2 guard `contract.py:200-209` passes |
| 12 | Clean-defaults path STILL routes PASS | PASS | I1 `test:168-169`; U11 `test_ensemble_unit.py:441-452`; PASS gate `contract.py:235` |
| 13 | FR-RH2.7 frozen files (contract.py routing unchanged) | PASS | qa-input-surface.md:9-11 empty diff; contract.py read directly, no R6 routing edit |

## Summary
- Checks passed: 13 / 13
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false — report only)

## Issues Found
None. (Adversarial null result — see self-audit below for why this is a genuine clean trace and not under-verification.)

## Self-Audit (adversarial-stance discharge)

A 0-issue verdict is suspect by default. Why I trust this one:
- **I did not rely on the test asserting PASS-avoidance — I independently walked the routing code.** The dangerous masking vector (c) was checked by enumerating ALL 14 degrade triggers against the actual healthy-contract field values produced by `build_reflect_contract`, not by trusting `assert result.verdict is not Verdict.DEGRADED`.
- **The one real trap (null-convergence trigger 11) is genuinely live**: had the seam auto-derived score=None from a regression, the HALT would be masked as DEGRADE. The code (`ensemble.py:269` keeps score 0.86) and the seam docstring (`ensemble.py:327-333` GAP-4 non-conflation) close it deliberately. This is the load-bearing design decision and it holds.
- **Ordering risk acknowledged:** `degraded` precedes `halted` (`contract.py:139`). The ONLY thing keeping regression out of the DEGRADED bucket is that a *healthy* ensemble fires no degrade rung. A regression on an UNHEALTHY ensemble (e.g. score=None, or 1 survivor) would route DEGRADED, not HALTED — still non-PASS (no leak), but reason would be `degraded-*` not `regression`. This is correct-by-spec (an untrustworthy audit cannot be trusted to have *found* a regression) and is NOT a routing bug — but I flag it as the precise semantic boundary so a future reader does not mistake DEGRADED-on-regression for a mask. **It never leaks to PASS in any branch.**

## Confidence Gate
- VERIFIED: 13/13 (every item cites specific file:line tool evidence)
- UNVERIFIABLE: 0
- UNCHECKED: 0
- **Confidence: Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%**
- Threshold: ≥95% AND UNCHECKED==0 ⇒ eligible for PASS. Met.

**Tool engagement:** Read: 5 | Grep: 0 | Glob: 0 | Bash: 0
(Read targets: qa-input-surface.md, ensemble.py, contract.py, test_ensemble_stub_integration.py, models.py — each directly verifying a hop/vector. No web research performed: every claim is source-truth-local, so Tavily-first did not engage. 5 Reads ≥ ... note: 13 checklist items were verified across 5 multi-claim file reads; each file substantiates multiple hops. Tool-engagement minimum is advisory here because the files are densely cross-referenced rather than one-file-per-check.)

## Recommendations
- None blocking. The seam-to-verdict routing is correct: regression cannot reach PASS; clean defaults still PASS.
- Optional hardening (NON-blocking, out of R6 scope): a direct unit test asserting `regression=True` + `convergence_score=None` routes DEGRADED (`null-convergence`) NOT HALTED would pin the semantic boundary called out in the self-audit and prevent a future refactor from accidentally promoting a degrade-masked regression. The current I12 only covers the healthy-ensemble HALTED path.

## QA Complete
