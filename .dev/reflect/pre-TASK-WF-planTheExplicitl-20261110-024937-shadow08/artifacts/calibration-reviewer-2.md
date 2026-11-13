# Calibration reviewer-2 (opus)
per_finding:
- F1: 0.75
- F2: 0.65
- F3: 0.4
card_score: 0.6
notes:
- F1: Plan line 43 reads "pass, or their actual failures are reported". A gate that allows "failures reported" as a pass is a concrete, fixable AC defect and the reword is actionable. MAJOR-minus: quick-depth plan, already done.
- F2: Citations resolve. Plan lines 30-31 use "clearly preserve"; COPIES at test line 8 holds only the two src files. Root CLAUDE.md has no test; gap real. Low impact: the AC cannot be made mechanical without a new test.
- F3: Plan line 39 says "where necessary"; the test already pins the worker-ban and banned phrases for the two distributable files; the hook message is pinned by exact equality at line 133. The card's own adjudication says the hook message is mechanically pinned, undercutting the claim. Vague-AC nit, scored lower.
