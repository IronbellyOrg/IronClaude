# RESOLVED needs_human_decision — FX7 verdict-DEGRADE on reviewer shortfall

**Status:** ✅ RESOLVED 2026-07-03 — operator chose **Option A (keep visibility-only)**. NO verdict-degrade is shipped: `_DEGRADED_COMPONENTS_HALT_SET` stays byte-unchanged, the `reviewer-shortfall` token remains benign/visible-only, and FR-RH2.9 / `test_i3` are preserved. Decision informed by a code-grounded adversarial debate (system-architect) which confirmed a shortfall-degrade has no additive room (it necessarily reverses FR-RH2.9) and that the reviewer facet's visibility (`reviewers_verified` + token) genuinely varies with the real requested count, so it needs no amendment. No further code change required.

(Original PENDING analysis retained below for the record.)

## The discovery (two code-contradicted brief premises)
The brief (Step 3.2 / Objective 3 / Step 3.4c) states that populating `degraded_components` on a
`reviewer_count < reviewers_requested` shortfall makes the case "honestly degrade WITHOUT a consumer edit"
via `contract.py:259-260`. The actual code contradicts this:

1. **HALT_SET-gated trigger.** `contract.py:259` is
   `if any(token in _DEGRADED_COMPONENTS_HALT_SET for token in degraded_components)`. Only members of
   `_DEGRADED_COMPONENTS_HALT_SET = {"serena","auggie","env-aliases","evidence-validator","serena:context-excluded"}`
   (contract.py:31-33) degrade. A bare `"reviewer-shortfall"` token is BENIGN — proven by
   `test_benign_degraded_component_does_not_over_halt` (test_verdict_mapping.py:190-201). To make it degrade
   requires ADDING `"reviewer-shortfall"` to `_DEGRADED_COMPONENTS_HALT_SET` (a consumer edit).

2. **Degrading a shortfall REVERSES FR-RH2.9.** `test_i3_partial_two_of_three_distinct_pass_eligible`
   (test_ensemble_stub_integration.py:199-221) asserts a 2-of-3 outcome (reviewer_count=2 vs requested 3)
   routes **PASS / exit 0** ("M>=2 AND >=2 distinct classes → pass-eligible"). The M-space is fully
   partitioned: M>=2 → pass-eligible (FR-RH2.9); M<2 → already degrades via `single-reviewer-fallback`
   (Trigger 10). So a shortfall-degrade has NO additive room — it necessarily degrades M∈[2, requested-1]
   which FR-RH2.9 deliberately treats as pass-eligible, REGRESSING test_i3. This is NON-additive, exactly
   parallel to how degrade-on-any-unverified reverses R2-F2.

## Decision required (a human must choose)
- **Option A (shipped, additive):** surface the shortfall additively — thread `reviewers_requested`, add
  `reviewers_verified: false`, and append a VISIBLE/benign `"reviewer-shortfall"` token to
  `degraded_components` that does NOT flip the verdict. A 2-of-3 shortfall stays PASS-eligible (FR-RH2.9 /
  test_i3 preserved), but the shortfall is now observable.
- **Option B (deferred, non-additive):** make a shortfall degrade the verdict (add `"reviewer-shortfall"` to
  `_DEGRADED_COMPONENTS_HALT_SET`, or add a new trigger). REVERSES FR-RH2.9, regresses `test_i3`. Requires
  explicit human authorization to accept reversing a deliberate tested design + the test churn.

## What was auto-applied
ONLY Option A (visible accounting). Option B is NOT applied. `_DEGRADED_COMPONENTS_HALT_SET` is BYTE-UNCHANGED.
Step 3.4c was adapted to an additive-safety witness (a benign token does not over-degrade; FR-RH2.9 preserved)
rather than a DEGRADED-route test (which would encode Option B and contradict test_i3).
