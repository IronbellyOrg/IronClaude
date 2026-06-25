# QA Report — Domain-Accuracy CONTENT lens (FR-RH2 R6)

**Topic:** Ensemble adversarial seam widening — field-disposition honesty
**Date:** 2026-06-22
**Phase:** doc-qualitative (domain-accuracy content lens)
**Fix cycle:** N/A (fix_authorization: false — REPORT ONLY)

---

## Overall Verdict: PASS

Zero inaccuracies found. Every claim about the verdict ladder, the adversarial-child
schema disposition, and the I12 test's healthy-ensemble guard was verified against the
ACTUAL source code (not the change-surface report's diff text, not assumptions) AND
confirmed by empirical execution of the real routing path.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | 4 deviation fields DEFAULTED CLEAN because score-only child cannot supply them — grep-true 0 hits | PASS | `grep -rn` over `src/superclaude/skills/sc-adversarial-protocol/` → EXIT=1 (no match), `grep -rln \| wc -l` → 0 files. Dir is real (128 KB SKILL.md + refs/). |
| 2 | I12 regression-routing targets the REAL HALTED rung: `_halted_reason` routes `regression_present is True` → "regression"; HALTED → exit 10 | PASS | contract.py:315-316 `if contract.get("regression_present") is True: return "regression"`. models.py:44-49 `Verdict.HALTED: 10`. |
| 3 | I12 keeps HEALTHY ensemble (`_distinct_stub`, `convergence_score=_FIXED_SCORE`=0.86 non-None) so no DEGRADE masks the HALT | PASS | test L508 `transport_for_slot=_distinct_stub`; L492 `convergence_score=_FIXED_SCORE`; L40 `_FIXED_SCORE = 0.86`. Empirically: `_degraded_reason(...) is None` for the I12 contract. |
| 4 | contract.py + models.py byte-unchanged (FR-RH2.7) — verdict ladder frozen | PASS | `git diff --stat -- contract.py models.py` → EMPTY. |
| 5 | Change-surface diff text matches actual repo diff (no report fabrication) | PASS | `git diff --stat` over the 3 files == reported stat byte-for-byte (163/86/43 lines; 271 ins / 21 del). |
| 6 | Defaulting mechanism in code matches the honesty claim (clean defaults, genuine bool) | PASS | ensemble.py:88-90 dataclass bool defaults `False`; :91-98 dict default all-zero; build_reflect_contract:520-523 threads through; clean-path None→all-zero at :493-499. |
| 7 | Load-bearing tests actually green | PASS | `uv run pytest` I12 + U11 + I1 → 3 passed in 0.16s. |

## Summary
- Checks passed: 7 / 7
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only)

## Issues Found
None.

---

## Adversarial trace — could a DEGRADE rung mask the I12 HALT? (the central attack)

The prompt's sharpest concern: `_halted_reason` runs at Stage 3, but `_degraded_reason`
runs at Stage 2 (first-match-wins, blocked→degraded→halted→pass). If ANY degrade trigger
fired for the I12 contract, the test would route DEGRADED (exit 11) and the regression HALT
would be silently masked — making the test a false witness.

I did not reason this from the docstring. I reproduced the exact I12 succeeded-worker set
(`stub_model_id(0..2)` = `qwen-stub-00`, `deepseek-stub-01`, `gpt-stub-02` — 3 distinct
vendor-distinct ids) through the REAL `build_reflect_contract` and dumped every
degrade-relevant field, then called the REAL `_degraded_reason`:

```
tier_reached: 2                          → degraded-tier1 NOT fired (not ==1)
reviewer_count: 3
t2_model_class_diversity: 'full'         → degraded-model-diversity NOT fired
t2_vendor_diversity: 'multi'             → single-vendor NOT fired
adversarial_unavailable: False           → adversarial-unavailable NOT fired
merge_method: 'adversarial'              → single-reviewer-fallback NOT fired
adversarial_convergence_score: 0.86      → null-convergence NOT fired (non-None at T2)
verification_ran: True                   → verification-skipped NOT fired
citations_dropped: 0                     → citations-dropped NOT fired
input_drift_detected: False              → input-drift NOT fired
degraded_components: []                  → degraded-components NOT fired
regression_present: True
status: 'success'

_degraded_reason(allow_single_vendor=False): None   ← ALL 14 triggers clean
_halted_reason: regression
VERDICT: Verdict.HALTED  exit: 10  reason: regression
```

Every one of the 14 FR-11 degrade triggers (contract.py:259-301) evaluates clean for the
I12 contract, so Stage 2 returns `None` and control reaches Stage 3, where
`regression_present is True` returns "regression" → HALTED → exit 10. The healthy-ensemble
guard is genuinely load-bearing, NOT decorative: the test's `assert contract[...] == "full"`
and `assert result.verdict is not Verdict.DEGRADED` correctly pin that no degrade masked the
HALT. Claim 3 is true under adversarial scrutiny.

Note also the type-trap avoidance: the I12 seam returns a genuine Python `bool` `True`
(test L492-493 comment is accurate). A non-bool (`"true"`/`1`) would hit the F2 guard
(contract.py:200-209, `_LOAD_BEARING_BOOL_FIELDS` includes `regression_present`) and route
BLOCKED/`malformed-contract-boolean` — a DIFFERENT non-PASS. The test asserting
`is Verdict.HALTED` + `reason == "regression"` (not merely `is not PASS`) correctly
distinguishes the right rung from this trap. Implementation honest here too.

## Field-disposition honesty — the core charge of this lens

Claim under review: "the 3 booleans + per-class counts are correctly DEFAULTED CLEAN
because the score-only /sc:adversarial child cannot supply them."

Verified true on both halves:

1. **The child genuinely cannot supply them.** `grep -rn` over the whole adversarial skill
   dir returns 0 hits for all four tokens (exit 1). Research 02 §4 corroborates: those
   tokens live ONLY in `sc-reflect-protocol/SKILL.md`, never the adversarial producer. The
   adversarial Mode-A child is score-only (convergence + merged path + status + 7 other
   fields, none of them deviation taxonomy). The code's docstrings (ensemble.py:77-84,
   327-333) state exactly this and are accurate.

2. **The code defaults them clean, not fabricated.** `run_adversarial_scorer` (the LIVE
   path) constructs `AdversarialResult(convergence_score=..., report_path=...)` only —
   leaving the 3 booleans + counts at their dataclass clean defaults (ensemble.py:350-353
   + :88-98). It NEVER auto-derives `regression_present` from a low convergence score
   (GAP-4 non-conflation), which is the correct domain semantics: low convergence is
   reviewer DISAGREEMENT → DEGRADE (`null-convergence`/score routing), not a regression
   HALT. The I12 regression signal is injected via the TEST seam (`_regression_score`),
   not by the live child — exactly the honest representation: the field is WIRED and
   verdict-load-bearing, but currently sourced clean from the real child pending a
   producer extension (OQ-PRODUCER). No silent-pass leak, no false regression manufacture.

## QA Complete — Self-Audit (MANDATORY)

1. **Factual claims independently verified against source code:** 7+ — the 4-field grep
   (0 hits, real dir), `_halted_reason` line 315-316, models.py exit-code map, contract.py
   + models.py empty diff, change-surface diff fidelity, the I12 `_distinct_stub` /
   `_FIXED_SCORE` literals, all 14 `_degraded_reason` triggers traced empirically, and the
   live-vs-test seam disposition.
2. **Files read:** ensemble.py (full), contract.py (full), models.py (exit_code block),
   test_ensemble_stub_integration.py (full), research 02 + 03, qa-input-surface.md.
   Executed: grep ×3, git diff ×2, pytest ×1, two real-routing Python reproductions.
3. **Why trust a PASS:** I did not accept the docstrings' or the change-surface report's
   word. The central adversarial concern (a Stage-2 DEGRADE masking the Stage-3 HALT) was
   refuted by RUNNING the real `_degraded_reason`/`derive_verdict` over the reproduced I12
   contract and observing `None` → "regression" → HALTED/exit 10. The grep claim was run,
   not assumed. The frozen-file claim was diffed, not trusted.
4. **Web research:** None performed (all verification is local-file/code-bound). Tavily
   precedence not engaged.

**Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 6 | Grep: 3 | Glob: 0 | Bash: 7 (3 grep/ls, 2 git diff, 1 pytest, 2 python repro — counted within Bash)
