# QA Verification — Content + FR-RH2.7 Invariant (Independent Re-Confirmation)

**Topic:** FR-RH2 R6 — widen the reflect Tier-2 adversarial seam (`AdversarialResult` → `build_reflect_contract`)
**Date:** 2026-06-22
**Phase:** verification-round / report-qualitative + tech-ref-qualitative hybrid (content + invariant + suite)
**Fix cycle:** N/A (fix step was SKIPPED on prior PASS — this round independently re-confirms)
**Fix authorization:** false (REPORT ONLY)
**Stance:** ADVERSARIAL — prior PASS is NOT assumed correct.

---

## Overall Verdict: PASS

Prior PASS independently re-confirmed. The full `tests/cli/reflect tests/swarm` suite is green;
all named tests exist by exact node ID and pass; the FR-RH2.7 frozen-file invariant holds
(empty diff on `contract.py` + `models.py`); and the GAP-4 non-conflation + genuine-`bool`
properties are present in the CURRENT production `ensemble.py` (not merely asserted by a test).
No re-introduced non-conflation defect; no non-bool defect. No fixes required.

---

## 1. Suite re-run (independent) — EXACT COUNTS

Command run from worktree root `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3`:

```
uv run pytest tests/cli/reflect tests/swarm -q
```

**Observed result (verbatim):**

```
================= 2353 passed, 26 skipped, 1 xpassed in 15.96s =================
```

- **Passed: 2353**
- **Skipped: 26** (e.g. `test_tmux_detached.py` 6 tmux-env skips — environment-gated, not defects)
- **xpassed: 1** (a known-xfail that passed — informational, not a failure)
- **Failed: 0**, **Errors: 0**

The suite is GREEN. (Harness emits a benign `VIRTUAL_ENV=/lsiopy does not match .venv` warning;
pytest still ran against the correct `.venv/bin/python` 3.13.11 — confirmed in the `-v` header.)

### Named-test confirmation (by EXACT node ID, not substring family)

`--collect-only` lists all six requested functions; each was then executed by exact node ID:

| Requested test | Node ID confirmed present | Result |
|---|---|---|
| `test_i12_seam_regression_does_not_pass` | `tests/cli/reflect/test_ensemble_stub_integration.py::test_i12_seam_regression_does_not_pass` | **PASSED** |
| `test_u11_build_reflect_contract_threads_regression_fields` | `tests/cli/reflect/test_ensemble_unit.py::test_u11_build_reflect_contract_threads_regression_fields` | **PASSED** |
| `test_u5_...` | `...::test_u5_model_class_diversity_uses_succeeded_worker_model_ids` | **PASSED** |
| `test_u6_...` | `...::test_u6_verdict_map_and_derive_ordering_are_unchanged` | **PASSED** |
| `test_u10_...` | `...::test_u10_adversarial_contract_parse_real_shape` | **PASSED** |
| `test_i1_...` (clean-path PASS) | `...::test_i1_positive_witness_real_fanout` | **PASSED** |

Targeted re-run of all 6 (via `-k`): `9 passed` (the `-k` family also caught u5/u6/u10 partners),
and the two headline tests run alone: `2 passed in 0.15s`.

### Tests are substantive, not rubber-stamps (adversarial check)

- **I12** runs the REAL `run_tier2_ensemble(config, adversarial_score_fn=_regression_score)`
  (injects `AdversarialResult(regression_present=True, deviation_count_by_class[regression]=1)`),
  parses the emitted contract, feeds it through the REAL `derive_verdict(child_rc=0,
  expected_tier=2)`, and asserts `verdict is HALTED`, `exit_code == 10`, `reason == "regression"`,
  PLUS provenance (`contract["regression_present"] is True` — hard-coded `False` pre-R6) and the
  GAP-4 guard (`t2_model_class_diversity == "full"`, `verdict is not DEGRADED`). Genuine
  red-then-green acceptance, not a placeholder.
- **U11** isolates the builder: a flagged call asserts `regression_present is True` (identity) and
  `deviation_count_by_class["regression"] == 1`; a clean call (no kwargs) asserts all four booleans
  `is False` and an all-zero count dict — pinning the NFR-RH2.6 clean-path-still-PASSes property.
- **I1** exercises the real fan-out with `ClaudeProcess` patched to `_boom` (any construction is a
  hard failure), asserting `tier_reached==2`, `status=="success"`, `verdict is PASS`, `exit_code==0`.
- **U6** pins the frozen ordering via `inspect.getsource(derive_verdict)` (BLOCKED < DEGRADED <
  HALTED < PASS) and the four exit-code values — a real source-level invariant guard.

---

## 2. GAP-4 non-conflation + non-bool defect — re-inspected in CURRENT production code

Inspected the live `src/superclaude/cli/reflect/ensemble.py` (not a test), adversarially.

### GAP-4 (regression NOT auto-derived from low/None convergence) — HOLDS

- `grep -n "regression_present" ensemble.py` returns assignments ONLY from the seam object:
  `regression_present = adversarial_result.regression_present if adversarial_result is not None
  else False` (lines 275-279). There is NO expression deriving it from `convergence_score` or a
  threshold anywhere in the module.
- The convergence value flows on a SEPARATE, independent line: `adversarial_convergence_score =
  adversarial_result.convergence_score` (line 269) → threaded as its own kwarg (line 302). The two
  signals never cross.
- The default production scorer `run_adversarial_scorer` (lines 350-353) constructs
  `AdversarialResult(convergence_score=..., report_path=...)` and leaves `regression_present` at the
  dataclass default `False` — so a low/None convergence produces `regression_present=False`,
  preserving the `null-convergence` DEGRADE rung (exit 11) rather than misrouting to HALT (exit 10).
- Docstring at lines 331-333 explicitly states the rule: "`regression_present` is NEVER auto-derived
  from a low/None convergence score (GAP-4 non-conflation: low convergence is reviewer DISAGREEMENT
  → DEGRADE, not a regression)." Code matches the doc.

**No re-introduced non-conflation defect.**

### Non-bool defect (load-bearing booleans must be genuine `bool`) — ABSENT

- `AdversarialResult` types the three load-bearing fields as `bool = False` (lines 88-90), and the
  emitted contract forwards them verbatim (lines 520-522) — never `"true"`/`1`.
- `build_reflect_contract` signature defaults them to genuine `bool` `False` (lines 466-468) and the
  destructure branches in `run_tier2_ensemble` yield Python `bool` (`... else False`, lines 275-289).
- The I12 injection passes genuine `True`; U11 asserts identity (`is True`/`is False`). A non-bool
  would route `malformed-contract-boolean` BLOCKED in `contract.py` (per research 03 §3 / docstring
  lines 82-84), which the suite would catch — it does not fire.

**No non-bool defect (re-)introduced.**

---

## 3. Change matches the research design

Cross-checked `ensemble.py` against research 03 and 06 (gap-fill GAP-2 recommended design):

| Research-design requirement | Production code | Match |
|---|---|---|
| `AdversarialResult` dataclass defined IN `ensemble.py` (keep `models.py` byte-clean) | dataclass at lines 72-99, in `ensemble.py` | YES |
| Fields: `convergence_score, regression_present, unauthorized_deviation_present, needs_human_decision, deviation_count_by_class, report_path` | all six present (lines 87-99) | YES |
| Scorer wraps UNCHANGED helpers (`extract_convergence_score` / `parse_adversarial_contract`) | `run_adversarial_scorer` calls both (lines 349-351); helper sigs unchanged | YES |
| Clean defaults for producer-pending fields (3 booleans + all-zero counts) | dataclass defaults `False`/zero-dict (lines 88-98); builder defaults match (lines 466-499) | YES |
| Only `convergence_score` + `report_path` LIVE from score-only Mode-A child | `run_adversarial_scorer` populates only those two (lines 350-353) | YES |
| FR-RH2.7: `contract.py` + `models.py` FROZEN (empty diff) | `git diff --stat -- contract.py models.py` → EMPTY (exit 0) | YES |
| Edits confined to `ensemble.py` | `git status --short` shows only ` M ensemble.py` | YES |

The implementation is faithful to the recommended GAP-2 fork (plumbing + test now;
producer-emission of real per-class counts/booleans deferred to OQ-PRODUCER follow-on, which is
correctly documented in the dataclass docstring lines 78-80 and `run_adversarial_scorer` docstring).

---

## 4. FR-RH2.7 frozen-file invariant — PROOF

```
git diff --stat -- src/superclaude/cli/reflect/contract.py src/superclaude/cli/reflect/models.py
# (empty output) ; exit 0
git status --short src/superclaude/cli/reflect/ensemble.py
#  M src/superclaude/cli/reflect/ensemble.py
```

`derive_verdict`, the `_halted_reason`/`_degraded_reason` ladder, `_LOAD_BEARING_BOOL_FIELDS`,
`_extract_deviations`, and the `Verdict.exit_code` map are byte-unchanged. The only modified file is
`ensemble.py`. FR-RH2.7 ("downstream return-contract consumers unaffected; verdict map + exit codes
unchanged") is satisfied. U6 additionally guards the ordering/exit-codes at runtime and passes.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Full suite green (exact counts) | PASS | `2353 passed, 26 skipped, 1 xpassed, 0 failed` (Bash) |
| 2 | `test_i12_seam_regression_does_not_pass` present + passes | PASS | exact node ID collected + run → PASSED |
| 3 | `test_u11_build_reflect_contract_threads_regression_fields` present + passes | PASS | exact node ID collected + run → PASSED |
| 4 | U5 / U6 / U10 pass | PASS | exact node IDs collected + run → PASSED |
| 5 | I1 clean-path PASS present + passes | PASS | `test_i1_positive_witness_real_fanout` → PASSED (verdict PASS / exit 0) |
| 6 | Tests substantive (not stubs) | PASS | I12/U11/I1/U6 bodies read — real driver + derive_verdict + identity asserts |
| 7 | GAP-4 non-conflation in production code | PASS | grep + Read ensemble.py 269/275-279/331-333/350-353 — regression sourced only from seam object, never from score |
| 8 | No non-bool defect | PASS | `bool=False` typing lines 88-90/466-468; verbatim emit 520-522; identity asserts in tests |
| 9 | Matches research design (AdversarialResult; scorer wraps helpers; clean defaults) | PASS | §3 table — all 7 rows match |
| 10 | FR-RH2.7 frozen files unchanged | PASS | `git diff --stat` empty; only `ensemble.py` modified |

---

## Summary
- Checks passed: 10 / 10
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false — REPORT ONLY)

---

## Issues Found

None. No CRITICAL / IMPORTANT / MINOR issues. No re-introduced non-conflation or non-bool defect.

---

## Self-Audit

**(a) Reliance list — prior-PASS items skipped for structural re-check:**
- Relied on prior M3-lens PASS for template/section-structure conformance of the seam change
  (structural shape of the contract dict) — re-verified semantically below rather than re-checked
  structurally.

**(b) Independent semantic checks (≥1 required, INV-019):**
- Re-ran the FULL `tests/cli/reflect tests/swarm` suite myself (Bash) and observed
  `2353 passed / 0 failed` — did NOT rely on the prior report's claim of green.
- Independently Read `ensemble.py` lines 72-99, 269-309, 331-353, 466-526 and verified by grep that
  `regression_present` is sourced ONLY from the seam object (GAP-4) and emitted as genuine `bool` —
  not inferred from the prior PASS verdict.
- Independently confirmed the FR-RH2.7 frozen-file invariant via `git diff --stat` (empty) +
  `git status --short` (only ensemble.py) — direct tool evidence, not reliance.
- Read the I12 / U11 / I1 / U6 test bodies to confirm they are substantive acceptance tests, not
  rubber-stamps.

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 5 | Grep: 2 | Glob: 0 | Bash: 6
**Web research:** none performed (all verification was local-file / suite-bound; no external lookup
required) — Tavily-first rule not triggered this round.

---

## Recommendations

- Proceed. The prior PASS is independently re-confirmed: suite green (2353 passed / 0 failed), all
  named tests present + passing, FR-RH2.7 frozen, GAP-4 non-conflation and genuine-`bool` properties
  intact in production code. No code change required.
- (Non-blocking, already documented) The 3 deviation booleans + per-class counts remain default-CLEAN
  pending the OQ-PRODUCER follow-on (sc-adversarial child emission). That is intended scope, correctly
  recorded in the dataclass/scorer docstrings — not a defect for this task.

## QA Complete
