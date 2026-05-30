# Refactor Plan — Merge Strategy

## Base: Variant A (unmediated direct-read)

## Integrations from non-base

### From Variant B
1. **B3 — Verdict-direction asymmetry**: integrate as Theory M3 (replacing A's T3 "stripped-context" framing OR adding as M3-alt; debate favors integration as a distinct fourth-mechanism candidate). Source: agent-B-theories.md lines 61-73. Target: third theory slot in merged output. Rationale: U-002 KEEP (debate confidence 0.90). Risk: Medium — overlaps partially with A's T2 fix.
2. **B's one-line systemic fixes**: B's `min(evidence_grounding, mean(other_four))` formula is more surgical than A's "cap at 0.75" — integrate as the primary fix wording for the arithmetic-mean problem.

### From Variant C
1. **C2 — Eval-suite silent-green coverage**: integrate as the **prevention mechanism** alongside the three diagnostic mechanisms. Source: agent-C-theories.md lines 59-71. Target: new "Prevention" subsection in cross-theory implications. Rationale: U-003 KEEP (debate confidence 0.85). Risk: Low — orthogonal to existing theories.
2. **C's recursion-of-anti-pattern observation**: integrate as meta-observation — calibrator fails the way pr86's code failed (silent-green coverage of structurally-unverifiable predicates). Source: agent-C-theories.md lines 106-107. Target: cross-theory implications. Risk: Low.

## Base weaknesses to address
1. A's T3 (stripped-context) has the weakest per-theory confidence (0.65). Both B and C offer alternative third mechanisms with higher confidence (B3=0.78, C3=0.45 — actually C's is lower). **Decision**: surface all three third-mechanism candidates in the merged output rather than pick one; the truth is likely a convex combination (A's information-channel + B's verdict-asymmetry are clearly orthogonal; C's anchoring is partial overlap with both).

## Changes NOT being made
- B's degraded-mode disclosure section (lines 9-23 of variant B): not integrated. The reflect channel failed; the meta-info about that failure is logged in B but does not improve the calibration-failure analysis.
- C's "Where the troubleshoot tiers landed" section (variant C lines 92-109): not integrated as a top-level section. The pipeline-execution detail is process-meta, not mechanism-claim. Only the substantive findings (C1, C2, C3) carry.
- A's "Cross-theory implications" paragraph about T2/T3 conflict: retained but tempered — the actual claim ("Falsification standard field could amplify well-written but wrong cards") is preserved as a known risk in the merged output.
