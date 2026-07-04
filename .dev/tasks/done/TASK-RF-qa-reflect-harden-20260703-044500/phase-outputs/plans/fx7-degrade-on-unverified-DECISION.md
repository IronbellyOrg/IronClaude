# RESOLVED needs_human_decision — FX7 aggressive "degrade on ANY unverified run"

**Status:** ✅ RESOLVED 2026-07-03 — operator chose **Option A (keep visibility-only)**. NO verdict-degrade is shipped: `_VERIFICATION_SKIP_EXEMPTIONS` stays byte-unchanged and the clean-run `verification_skip_reason` stays the exempt `"tool-unavailable"` (R2-F2 preserved; `test_r2f2`/`test_i1` green). A code-grounded adversarial debate (system-architect) confirmed a blanket degrade-on-unverified would fire on 100% of headless runs (a gate that is always red carries zero signal). **Noted weakness (non-blocking):** `verification_verified` is a hard-coded `False` on every headless run, so it is honest but informationally inert; if the auto-promotion path ever needs teeth, the additive follow-up is an **opt-in** `--require-verification` flag (default-off, caller-chosen non-exempt skip reason) — NOT a default flip. **Decisive open fact worth checking before any such follow-up:** whether the auto-promotion consumer actually acts on a DEGRADED verdict / reads `verification_verified` at all (if it treats any non-BLOCKED verdict as green, the whole question is moot at that seam). No code change shipped.

(Original PENDING analysis retained below for the record.)

## The tension
The ensemble builder ALWAYS emits `verification_ran: False` with the EXEMPT skip reason
`verification_skip_reason: "tool-unavailable"` (a member of `_VERIFICATION_SKIP_EXEMPTIONS`,
contract.py:36-38). This is the deliberate **R2-F2** design (`test_ensemble_unit.py:342-363`
`test_r2f2_build_reflect_contract_emits_honest_verification_fields`): a clean headless Tier-2 run runs
no verification triangle, so it emits the exempt reason so it does NOT spuriously degrade.

The aggressive alternative — "force DEGRADED whenever `verification_ran` is False, INCLUDING clean
full-reviewer runs" (e.g. by flipping the clean-run skip reason to a NON-exempt token, firing Trigger-12
at contract.py:288-291) — would degrade EVERY ensemble run, REVERSING R2-F2 and breaking `test_r2f2`
+ `test_i1_positive_witness_real_fanout` (clean PASS/exit-0). It is NON-additive.

## Decision required (a human must choose)
- **Option A (shipped, additive):** keep the exempt skip reason; surface vacuity additively via the new
  `verification_verified: false` visibility field. Clean unverified Tier-2 runs still route PASS (by design)
  but are now VISIBLE as unverified.
- **Option B (deferred, non-additive):** make an unverified run degrade (flip the skip reason / add a
  trigger). REVERSES R2-F2, breaks `test_r2f2` + `test_i1`. Requires explicit human authorization to accept
  the behavior change + test churn.

## What was auto-applied
ONLY Option A (the additive `verification_verified: false` visibility field). Option B is NOT applied.
`_VERIFICATION_SKIP_EXEMPTIONS` is BYTE-UNCHANGED. If honest-degrade were ever claimed to require editing
the exemption set, that too is a `needs_human_decision` HALT (write PENDING, do not auto-apply).

Rationale: driving-plan §3.4 — add NEW fields rather than repurposing existing routing.
