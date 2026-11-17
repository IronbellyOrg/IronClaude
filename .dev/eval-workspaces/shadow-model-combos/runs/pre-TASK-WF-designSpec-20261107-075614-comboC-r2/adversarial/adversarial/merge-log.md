# Merge Log

## Metadata
- Base: variant-2-original.md (reviewer-2, qa, claude-haiku-5-5)
- Plan: refactor-plan.md (15 merged findings, M-1 to M-15)
- Incorporated: variant-1-original.md, variant-3-original.md, invariant-probe.md
- Output: merged-output.yaml
- Verdict: not_ready (blocking M-1 and M-2, both with a spec-side origin); convergence_score 1.0
- Review status: auto-approved (non-interactive)

## Applied Changes
| M | Status | Provenance | Notes |
|---|---|---|---|
| M-1 | applied | V2:F1 | 5 citations copied verbatim from V2:F1. MAJOR, blocking, origin spec. |
| M-2 | applied | V2:F2 + V1:F2 | V2:F2 has 7 citations; the limit is 6, so spec 205 was dropped (spec 147-157 and 228-234 cover the same rows). V1:F2 lines (plan 124, 169, spec 315) are all included. |
| M-3 | applied | V2:F3 + V1:F3 | V2:F3 citations; V1:F3 cites the same lines. Re-graded non-blocking (Round 2). |
| M-4 | applied | V2:F4 | Citations verbatim. Re-graded non-blocking (Round 2). |
| M-5 | applied | V1:F5 + V2:F7 | Union of V1:F5 and V2:F7 citations (plan 166 is covered by range 166-169). |
| M-6 | applied | V1:F4 + V2:F12 | Union of both citation sets. V1's "edits proceed unguarded" claim was not carried (refuted by spec 274); the claim is limited to the resume path. |
| M-7 | applied | V2:F5 + V1:F1 | V1:F1's range plan 137-140 with its quote replaces V2's two single lines (137, 140). |
| M-8 | applied | V2:F8 | Citations verbatim. |
| M-9 | applied | V1:F7 | Citations verbatim. |
| M-10 | applied | V1:F6 | Citations verbatim. |
| M-11 | applied | V3:F4 + V2:F6 | V3:F4 citations; V2:F6 cites the same plan 33, 154 and spec 342. Severity MINOR, origin spec (Round 2 concession). |
| M-12 | applied | INV-011 | Citations from the Evidence column (SPEC:178-179, 262, 266; PLAN:124, 128-129, 166, 170). That is 7; spec 266 was dropped for the 6 limit. |
| M-13 | applied | V3:F6 + V2:F10 | V3:F6 citations; V2:F10 lines (plan 148, 190-193, 195) sit inside V3's ranges. |
| M-14 | applied | V3:F1, F2, F3, F5, F7, F8 + V2:F11 | Seven findings, 6-citation limit. One nearest line per finding was kept (plan 25, 90, 124, 153, 200, spec 196-206). Dropped: spec 6, 57, 80, 255, 301, 364, 369; plan 22, 56, 128, 150, 152-155, 60. The merged claim names all seven items. |
| M-15 | applied | INV-001, 003, 004, 009 | Evidence column: kept spec 194-206 (INV-001), spec 155-156 and plan 75 (INV-003), spec 166 and plan 76-77 (INV-004), spec 143 (INV-009). Dropped: SPEC:190, 108, 138-139, 107, 275, 109, 333; PLAN:70; `recovery.py` lines (not plan or spec). |

No planned change was skipped. No citation was invented. Where a merged finding had more than 6 source citations, the nearest lines were kept as shown above.

Planned non-changes honored: V2:F9 withdrawn; V1:F1 and V3:F4 severities lowered; V2:F3 and F4 flags dropped to non-blocking.

## Post-Merge Validation
- Structural integrity: PASS. `uv run python -I` loads the YAML. 15 findings (M-1 to M-15), blocking_findings is [M-1, M-2], each finding holds 1 to 6 citations (max found: 6), all claims are 300 characters or fewer.
- Citation paths: PASS. Both paths (the plan file and `source.md`) exist in the worktree.
- Categories: all in the allowed set (contradiction, missing-requirement, unpassable-check, safety, other).
- Contradictions: none new. The severity and blocking values follow the plan table. M-12 is a plan finding added after the debate, so it is recorded as undebated in unresolved_notes.
- Line numbers were not re-read against the plan and spec files; they are copied from the source findings and the probe.

## Summary
15 findings merged into merged-output.yaml on the V2 base, verdict not_ready, with two blocking findings (M-1, M-2). Dissent on C-005 and X-004 (resolved 2 of 3) is in unresolved_notes.
