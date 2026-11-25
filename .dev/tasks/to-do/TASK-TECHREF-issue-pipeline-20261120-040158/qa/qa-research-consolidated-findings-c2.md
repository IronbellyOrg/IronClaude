# Gate 1 consolidated findings (cycle 2)

**Date:** 2026-11-20
**F_2 = 1** (BLOCKING: N-1; 0 synthetic)
Source: qa-research-verification-structural-c1.md (FAIL, 1 BLOCKING) and qa-research-verification-content-c1.md (PASS, 0 BLOCKING). Five findings of cycle 1 (B-1, B-2, B-3, F-1, F-2) are FIXED per the structural report.

| ID | Origin lens | Research location | Finding (copied from the structural verification report) | Required fix |
|---|---|---|---|---|
| N-1 | structural verification c1 (new; introduced by the gap-fill for F-2) | research/04-claim-flow-and-orca-worktree.md, section "Gap-fill c1 F-2", row F-2.1 for `skills/test_model_alias_policy.py`, "What it pins" item (5) (line ~554) | The row says "(5) The other eight tests are repository-wide alias policy and are not part of the claim path" and then lists seven tests (:139, :164, :176, :183, :199, :217, :231). The file has 11 test functions (`grep -n '^def test_'` gives lines 83, 104, 139, 164, 176, 183, 191, 199, 217, 231, 247); items (1) to (4) are four of them (:83, :104, :191, :247), so the others are seven, not eight. 11 - 4 = 7. | Append an erratum: "The other seven tests" (not eight) |

MINOR notes: M-c1-1 (the old wrong text remains in the research files under the erratum sections; erratum sections supersede it) and any others in the verification reports stay as notes.
