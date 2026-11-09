### Variant 1 Advocate (opus, analyzer)

**Position summary.** V1 found the CI-breaking defect (C-001) and the widest set of correct minor findings (line budget, undefined counts, undeclared drops). It missed C-002 (real, blocking); X-002 and half of C-012 are weak. Best card = V1 coverage + V2's C-002 + V3's C-009 upgraded to blocking.

**Steelman V2.** source.md:46 retry absent from the literal block's reviewer text (source.md:120 handles 3/4/5/70; exit-2 only for the reviser at :127); plan:117 copies the block; coverage-matrix.json:269-272 wrongly credits Task 8. Only V2 caught it.
**Steelman V3.** C-001 with the decisive set-edit fix (precedent :29-32); C-008 whole-file order pin fails on spec-panel.md:262; C-009 importlib .pyc with the absolute path breaks plan:104 "prints nothing".

**Strengths claimed.** C-001 grounded (:647-648, :33; plan:124 omits it; plan:119 forces blocked). C-004: lines 451-462 removed (12), source.md:104-128 plus blank added (26), 486 - 12 + 26 = 500, Makefile:403 `-gt 500`, test.yml:135 runs lint-architecture. Only V1 found C-005, C-006, C-012 (plan:64 undefined terms).

**Weaknesses in others.** V2 missed C-001 with 0.96 self-confidence (calibrated 0.70); R2-F1's "false claim" is about the auditor's own matrix, not the plan (missing deliverable still real); R2-F2 low value. V3 graded C-009 minor though a literal AC fails; R3-F2 substring half wrong; R3-F5 already caught by plan:124.

**Concessions.** Missed C-002. X-002 withdrawn (no evidence). C-012 skill-path half covered by plan:104. V3's C-001 fix is more decisive. C-007, C-013 low impact.

**Shared assumptions.** A-001: QUALIFY — the /sc:implement final review does not re-run the full suite (sc-implement-protocol/refs/qa.md:3: "Do not re-run the full test suite as the review"); CI does (test.yml:47); the failure surfaces at the PR after the plan reports done; still blocking. A-002: REJECT — source.md:46 vs :120; spec-internal conflict copied without a recorded deviation; the fix needs owner sign-off because it edits text the spec calls literal.

**Per-point positions.**
- S-001 n/a — V1; S-002 n/a — tie V1/V3
- C-001 include-blocking — V3 (V1 also)
- C-002 include-blocking — V2
- C-003 include-minor — V2
- C-004 include-minor — V1
- C-005 include-minor — V1
- C-006 include-minor — V1
- C-007 include-minor — V1
- C-008 include-minor — V3
- C-009 include-blocking — V3
- C-010 include-minor — V3
- C-011 include-minor — V3
- C-012 include-minor — V1 (40-char half only)
- C-013 include-minor — V1
- X-001 include-minor — tie V2/V3
- X-002 exclude — V3
- A-001 include-blocking — tie V1/V3
- A-002 include-blocking — V2
