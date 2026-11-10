### Variant 2 Advocate rebuttal (opus, qa)

**Response to criticisms.**
- (a) Conceded in full: V2 missed C-001 and C-009; 0.96 self-confidence does not fit; calibrated 0.70 is right. C-002 is unaffected.
- (b) Framing conceded: the wrong Task 8 credit is in the auditor's own matrix, not a plan claim. The grade stands on the missing deliverable: source.md:46 is normative; plan:117 copies source.md:120 (exits 3/4/5/70 only); a grep of the plan for "exit 2" / "own call" finds no reviewer-side retry. Under A-003, blocking.
- (c) Conceded: no new command exists before Task 5; running the tests there is a necessary but undeclared deviation (V3's framing); minor.
- (d) Partly conceded: the fix needs an owner ruling, but the plan already has the channel — plan:117 appends an owner-decision sentence to the same literal paragraph, and plan lines 21-25 record four more rulings. The conflict is inside the spec (source.md:46 vs :120); following line 46 implements the spec. Fix: one owner-decision sentence in Region 4 plus one pin in test_spec_panel_minfix.py.

**Updated assessment.** V1: broadest correct minor coverage; C-012 narrowed to the 40-char half (source.md:224); X-002 withdrawal correct. V3: most decisive blocking fixes; C-008 concession correct. All three agree on every inclusion level; only the filing of A-001 differed.

**New evidence.** plan:117 is a precedent for amending the "literal" block through an owner decision; plan grep confirms no task adds the reviewer-side exit-2 retry.

**Position changes.**
- C-003: include-minor — winner: V3 — necessary deviation, undeclared.
- A-001: include-blocking (qualifier on C-001) — winner: V3 — aligns with V1 and V3.
