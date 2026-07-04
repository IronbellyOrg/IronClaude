# QA Report — Task Integrity (Gate B: Degrade-Mechanism Correctness)

**Topic:** FX7 reviewer-shortfall degrade deferral — is the executor's deferral code-justified?
**Date:** 2026-07-03
**Phase:** task-integrity
**Lens:** degrade-mechanism-correctness
**Fix cycle:** N/A
**Fix authorization:** false (REPORT ONLY)
**Stance:** ADVERSARIAL — verified independently against actual code, hunting for an additive degrade path the executor missed.

---

## Overall Verdict: PASS

The executor's deferral of the verdict-DEGRADE-on-reviewer-shortfall is **CODE-JUSTIFIED**. The FX7 brief premise ("populated `degraded_components` on a reviewer shortfall honestly degrades WITHOUT a consumer edit via contract.py:259-260") is **contradicted by the actual code**. No additive path exists to make a shortfall degrade the verdict without either editing `_DEGRADED_COMPONENTS_HALT_SET` or reversing FR-RH2.9 (regressing test_i3). The executor correctly shipped Option A (additive visible accounting) and deferred Option B (non-additive verdict flip) as a `needs_human_decision` PENDING.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | HALT_SET-gated trigger fires only for HALT_SET tokens; `reviewer-shortfall` NOT a member → benign | PASS | contract.py:31-33 HALT_SET = `{serena, auggie, env-aliases, evidence-validator, serena:context-excluded}` — no `reviewer-shortfall`. Trigger contract.py:265 `if any(token in _DEGRADED_COMPONENTS_HALT_SET for token in degraded_components)` = exact membership, NOT substring. Cross-check: test_verdict_mapping.py:190-201 `test_benign_degraded_component_does_not_over_halt` asserts benign tokens → PASS/exit 0. Test PASSED on run. |
| 2 | FR-RH2.9: 2-of-3 shortfall is PASS-eligible; M-space fully partitioned → shortfall-degrade is NON-additive | PASS | test_ensemble_stub_integration.py:199-221 `test_i3_...`: reviewer_count=2 vs requested 3, full diversity, tier_reached=2 → `Verdict.PASS` / exit 0. Test PASSED on run. M-space partition confirmed in ensemble.py: M=0→None (L522-523); M=1→single-reviewer-fallback degrades (L543, Trigger 10 @ contract.py:286); M≥2→adversarial/pass-eligible (L542-543). |
| 3a | Genuine shortfall populates `degraded_components` + `reviewers_verified=False` | PASS | ensemble.py:539-540 `if reviewers_requested is not None and reviewer_count < reviewers_requested: degraded_components.append("reviewer-shortfall")`; L535-536 `reviewers_verified = True if reviewers_requested is None else reviewer_count >= reviewers_requested` → False on shortfall. |
| 3b | Clean/full or kwarg-omitting call → `degraded_components == []` + `reviewers_verified True` | PASS | L538 initializes `[]`; L539 guard `reviewers_requested is not None` skips append when omitted or when count≥requested; L536 None-branch yields True. |
| 3c | `verification_skip_reason` stays EXEMPT `"tool-unavailable"` on ALL runs | PASS | ensemble.py:572 literal `"verification_skip_reason": "tool-unavailable"` (unconditional). `tool-unavailable` ∈ `_VERIFICATION_SKIP_EXEMPTIONS` (contract.py:36-38), so Trigger 12 (contract.py:294-297) never fires. |
| 4 | Two PENDING decision markers exist AND no code auto-applies them | PASS | Both files present (ls): `fx7-degrade-on-reviewer-shortfall-DECISION.md` (2827B), `fx7-degrade-on-unverified-DECISION.md` (2003B). `git diff HEAD` shows HALT_SET line byte-unchanged. `grep reviewer-shortfall src/.../reflect/` returns only ensemble.py comment+append (L528/533/540) — never added to HALT_SET, never a new trigger. |
| 5 | `reviewers_verified` is telemetry-only, not verdict-bearing (adversarial cross-check) | PASS | Only uses: ensemble.py:578 (emit), contract.py:131 (carried into `_make_result` visibility field), runner.py:121/240 (emit), models.py:159 (`bool = False` field). Zero occurrences inside any verdict-routing conditional in `derive_verdict`/`_degraded_reason`/`_halted_reason`. Confirms Option A is pure visibility. |

## Summary
- Checks passed: 5 / 5 (item 3 counted as 3a/3b/3c)
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only)

## Adversarial Finding Hunt (did the executor wrongly defer?)

**Question:** Could the shortfall degrade additively WITHOUT reversing FR-RH2.9 or editing HALT_SET?

**Answer: NO — proven by construction, not assumed.**

The set of "genuine shortfalls" is `reviewer_count < reviewers_requested`. With reviewer_count=0 short-circuiting to `None` (no contract, ensemble.py:522-523), the live shortfall domain is M ∈ {1, …, requested−1}:
- **M = 1** → `merge_method="single-reviewer-fallback"` (ensemble.py:543) → ALREADY degrades via Trigger 10 (contract.py:286) and Trigger 6 (contract.py:269). No new signal needed.
- **M ∈ [2, requested−1]** → `tier_reached=2`, `merge_method="adversarial"` → FR-RH2.9 deliberately treats this as PASS-eligible. `test_i3` is the canonical instance (M=2, requested=3).

Any rule keyed on `reviewer_count < reviewers_requested` fires on `test_i3` **by construction** (test_i3 IS a 2-of-3 shortfall). Therefore the shortfall-degrade set and the FR-RH2.9 pass-eligible set overlap precisely at M ∈ [2, requested−1] — there is **zero additive room**. Degrading the shortfall necessarily flips a case FR-RH2.9 marks pass-eligible, regressing test_i3. This is exactly the executor's stated rationale, and it holds against the actual code + the passing test.

The brief conflated two distinct notions:
- **Honest ACCOUNTING** (append a visible benign token + `reviewers_verified=False`) — IS additive. Shipped (Option A).
- **Honest DEGRADING** (flip the verdict on shortfall) — is NON-additive. Correctly deferred (Option B, PENDING).

The brief's claim that a populated `degraded_components` "honestly degrades WITHOUT a consumer edit via contract.py:259-260" is **false**: contract.py:265's trigger is HALT_SET-membership-gated, so a bare `reviewer-shortfall` token is inert until a consumer edit (adding it to HALT_SET) is made. The executor caught this correctly.

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| — | — | — | None. Executor deferral is code-justified; Option A additive accounting is correctly implemented and does not perturb the verdict. | — |

## Actions Taken
None (report-only, fix_authorization: false).

## Confidence Gate
- **Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 6 | Grep: 4 | Glob: 0 | Bash: 3 (2 grep-in-bash, 1 pytest, 1 git-diff)
- Every checklist item mapped to a specific file:line citation and, for the two load-bearing invariants, an executed pytest run (both PASSED) + a `git diff HEAD` proving HALT_SET is byte-unchanged.
- No UNCHECKED items. No UNVERIFIABLE items.

## Recommendations
- Green light: the FX7 deferral is sound. Option B (verdict-degrade-on-shortfall) remains a genuine `needs_human_decision` — it requires explicit human authorization to accept reversing FR-RH2.9 and the accompanying test_i3 churn. Do NOT auto-apply it.
- No further remediation required for this gate.

## QA Complete
