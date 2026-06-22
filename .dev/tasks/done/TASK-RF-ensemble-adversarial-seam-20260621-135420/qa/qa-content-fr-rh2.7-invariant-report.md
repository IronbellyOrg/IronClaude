# QA Report — FR-RH2.7-invariant-preservation (CONTENT lens)

**Topic:** FR-RH2 R6 — Tier-2 adversarial seam widening (`AdversarialResult`)
**Date:** 2026-06-22
**Phase:** doc-qualitative (content invariant-preservation lens)
**Fix cycle:** N/A (fix_authorization: false — REPORT ONLY)
**Stance:** ADVERSARIAL — assumed a backward-compat invariant was broken; hunted for it.

---

## Overall Verdict: PASS

Zero invariant breaks found across all four mandated checks. Every claim below
was independently re-verified with my own tool engagement (git diff re-run,
pytest re-run, Python runtime introspection of bool types) — NOT taken on the
recorded proof's word.

---

## Checks (4 mandated invariants)

| # | Check | Result | Evidence (independently produced) |
|---|-------|--------|-----------------------------------|
| 1 | `derive_verdict` + `Verdict` exit-code map byte-unchanged | PASS | `git diff -- src/superclaude/cli/reflect/contract.py src/superclaude/cli/reflect/models.py` → EMPTY (exit 0, zero stat rows). `git diff --stat` of the whole change shows ONLY `ensemble.py` + 2 test files; contract.py/models.py absent from the change set. |
| 2 | I1 clean-path PASS + U6 frozen-ordering guard still pass | PASS | Re-ran both myself: `3 passed` (`test_i1_positive_witness_real_fanout`, `test_u6_verdict_map_and_derive_ordering_are_unchanged`, plus I12/U11). Not relying on recorded summary. |
| 3 | GAP-4 non-conflation: `regression_present` NOT auto-derived from low/None convergence; null-convergence DEGRADE fallback preserved | PASS | ensemble.py:275-279 sources `regression_present` from `adversarial_result.regression_present` ONLY; never from `convergence_score`. The convergence value feeds ONLY `adversarial_convergence_score` (line 269). contract.py:284-285 `null-convergence` DEGRADE trigger unchanged (frozen by check 1). grep confirms no `regression`×`convergence` conflation line. |
| 4 | Load-bearing booleans emitted as genuine Python `bool` (never `"true"`/`1`) | PASS | Runtime introspection: dataclass defaults + builder-emitted contract fields ALL `isinstance(x, bool) == True`, `isinstance(x, str) == False` for both clean (`False`) and flagged (`True`) paths. Test stubs use literal `True`/`False`. |

---

## Detailed findings per invariant

### Invariant 1 — frozen-file diff (contract.py + models.py byte-unchanged)

I independently re-ran (NOT trusting `fr-rh2.7-diff-proof.md`):

```
git diff -- src/superclaude/cli/reflect/contract.py src/superclaude/cli/reflect/models.py
→ exit 0, ZERO output (empty diff)
git diff --stat (whole change) → only:
  src/superclaude/cli/reflect/ensemble.py            | 163 ++
  tests/cli/reflect/test_ensemble_stub_integration.py |  86 ++
  tests/cli/reflect/test_ensemble_unit.py            |  43 ++
```

contract.py and models.py are entirely absent from the change set. I also Read
both files in full: the `Verdict.exit_code` map (models.py:44-49) is
`PASS→0, HALTED→10, DEGRADED→11, BLOCKED→2`, and `derive_verdict`
(contract.py:130-246) retains the exact `blocked→degraded→halted→pass`
first-match-wins ladder. Both match the spec FR-RH2.7 acceptance bullet
(spec.md:303) verbatim. The fix is genuinely ensemble-side-only.

### Invariant 2 — I1 clean-path PASS + U6 frozen-ordering guard

I re-ran the named tests myself rather than trusting `pytest-summary.md`:
`3 passed in 0.16s` covering `test_i1_positive_witness_real_fanout`,
`test_u6_verdict_map_and_derive_ordering_are_unchanged`, and the new
`test_i12_seam_regression_does_not_pass` / `test_u11_*`. The U6 guard
(test_ensemble_unit.py:178) — the contract that pins the verdict ordering —
remains green, confirming the ladder semantics are unperturbed. I1
(test_ensemble_stub_integration.py:141) confirms a genuinely clean Tier-2 run
STILL routes PASS (NFR-RH2.6 backward-compat) — the seam widening did not break
the clean path.

### Invariant 3 — GAP-4 non-conflation (low convergence ≠ regression)

This was the adversarial hot-spot: a sloppy widening could have derived
`regression_present` from a low/None convergence score, conflating reviewer
DISAGREEMENT (a DEGRADE condition) with a regression FINDING (a HALT condition).
It does not.

- `regression_present` (ensemble.py:275-279) is the ternary
  `adversarial_result.regression_present if adversarial_result is not None else False`
  — it reads the seam result's OWN boolean, and has no dependency on
  `convergence_score`.
- The convergence value flows on a SEPARATE line (ensemble.py:269) into
  `adversarial_convergence_score` ONLY.
- `run_adversarial_scorer` (ensemble.py:314-353) populates ONLY
  `convergence_score` + `report_path` LIVE; the three deviation booleans default
  CLEAN on `AdversarialResult` (lines 88-90). A child-launch/parse failure still
  `return None` (line 348), which leaves `adversarial_convergence_score = None`,
  preserving the null-convergence DEGRADE fallback.
- The null-convergence DEGRADE trigger itself (contract.py:284-285,
  `tier_reached == 2 and adversarial_convergence_score is None → "null-convergence"`)
  is byte-frozen (Invariant 1) and therefore preserved unchanged.
- The docstring is correct and non-conflating: ensemble.py:330-333 explicitly
  states "`regression_present` is NEVER auto-derived from a low/None convergence
  score (GAP-4 non-conflation: low convergence is reviewer DISAGREEMENT → DEGRADE,
  not a regression)." Code matches docstring.
- I12 reinforces this empirically: it sets `convergence_score=0.86` (non-None) so
  the null-convergence DEGRADE does NOT fire and mask the regression HALT, then
  asserts the verdict is HALTED (not DEGRADED). The two signals are kept orthogonal.

### Invariant 4 — load-bearing booleans are genuine Python `bool`

Runtime introspection (executed, not reasoned):

```
AdversarialResult defaults:  regression_present=False / unauthorized_deviation_present=False
                             / needs_human_decision=False   →  all isinstance bool == True
build_reflect_contract clean: regression_present, unauthorized_deviation_present,
                             needs_human_decision, user_decision_required
                             →  all is_bool=True, is_str=False
build_reflect_contract flagged: regression_present=True, user_decision_required=True
                             →  all is_bool=True
```

- Dataclass field annotations are `bool = False` (ensemble.py:88-90); the builder
  params are `bool = False` (ensemble.py:467-468) and threaded straight into the
  contract dict (ensemble.py:520-523). `user_decision_required` correctly mirrors
  `needs_human_decision` (ensemble.py:523), preserving the prior coupling.
- Test stubs use literal Python `False`/`True` (test_ensemble_stub_integration.py
  `_const_score` and `_regression_score`; test_ensemble_unit.py U11) — never
  `"true"` or `1`. The I12 stub comment explicitly notes it returns genuine `True`
  so the strict-identity `is True` halt trigger fires rather than self-BLOCKing on
  a non-bool.
- This matters because contract.py's F2 guard (`_LOAD_BEARING_BOOL_FIELDS`,
  contract.py:47-57 + 200-209) routes any PRESENT non-None non-bool to
  BLOCKED/`malformed-contract-boolean`. Emitting genuine bool avoids self-inflicting
  a BLOCKED verdict. The producer side is clean.

---

## Self-Audit (adversarial honesty)

1. **Factual claims independently verified against source code:** 4/4 invariants,
   each with its own tool call — (1) re-ran `git diff` on the frozen pair AND the
   whole-change `--stat`; (2) re-ran the I1/U6/I12/U11 pytest set; (3) read
   ensemble.py:269/275-279/314-353 + contract.py:284-285 + grepped for any
   regression×convergence conflation line (none); (4) executed Python runtime
   `isinstance` checks on the dataclass defaults + builder output for clean AND
   flagged paths.
2. **Files Read in full:** ensemble.py, contract.py, models.py, spec.md (FR-RH2.7
   bullet, lines 288-317), research 03 §5, qa-input-surface.md, pytest-summary.md.
3. **Why trust this PASS:** I did not accept the recorded `fr-rh2.7-diff-proof.md`
   — I re-executed the diff (empty), re-executed the two named guard tests (green),
   and ran live `isinstance` introspection on the actual emitted bool values rather
   than reading type annotations. The adversarial hot-spot (GAP-4 conflation) was
   traced line-by-line: the regression boolean has zero data-dependency on the
   convergence score.
4. **Web research:** none required for this invariant lens (all checks are
   local-file / runtime bound). Tavily-first N/A.

**Tool engagement:** Read: 7 | Grep: 0 (folded into Bash grep) | Glob: 0 | Bash: 4
(git diff, pytest re-run, Python introspection, grep/diff-stat). Tool calls ≥
4 checks — engagement floor satisfied.

**Confidence:** Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

---

## Issues Found

None. Zero invariant breaks of any severity (CRITICAL / IMPORTANT / MINOR).

The change is a clean, additive, ensemble-side-only widening: `derive_verdict`
and the exit-code map are byte-frozen, the clean path still PASSes, low
convergence is not conflated with regression, and all load-bearing booleans are
genuine Python `bool`. FR-RH2.7 is preserved.

## QA Complete
