# V2 (prosecutor) Round 2 rebuttal

Roots as in `work/evidence-pack.md`; I re-read the cited files on disk.

## 1. What changed

Verdict unchanged (NO). I tried to break the PASS through R-A and R-C and failed (section 3). Two notes moved: old N-3 ("Eight" hard-coded) is a documentation gap, not a silent error (CORR-1: `test_briefs.py` line 190 asserts `len(cards) == 8`). Old N-4 (no source) is stronger: a designed case (DESIGN 273, 563) that `analyze.py` never reads for any arm (CORR-7). I withdraw my Round 1 guess of a 0.01-0.02 shift; it had no calculation.

## 2. Claims I reject

- V3 N-1, "toward SS looking better", as an established direction. V3's own section 7 says "Apply each one" could lift K above a plain checklist, "the same unfairness the other way". A direction needs a neutral wording, and none exists. The draft matches MR 1035; no real K run exists (F9).
- V3 table row 2, "time is not an input to D7". V1 is right that clock use can change found fraction; but it cuts both ways and is unmeasured, so it cannot make the default blocking.

## 3. Rulings

- **R-A NOTE.** Strongest YES: a soft K lowers K minus Z0 and flatters SS at D7 (MR 1091). It fails: (i) "to look for" is already an instruction; (ii) the cheapest fix, "Apply each one to the plan", carries the opposite risk (R-B); (iii) MR 120 predicts K minus Z0 near 0, so D7 rarely binds (F6: it flips only if K minus Z0 exceeds about 0.08, given D2 passes); (iv) REQ-40 reports K minus Z0, so a soft K is visible, not hidden.- **R-B NOTE.** An apply verb alone gives none of SS's units (locations, tool lines, ledger; F5, MR 36). It still moves K toward SS (MR 1100). Both directions are unsized; the draft is the owner's "plain words".
- **R-C NOTE.** Harm if any: a few seconds on (2), or a vacuous finding, on a no-source document. `grep` of `analyze.py` finds no `no_source` or "applicable", so C2 items count the same in Z0, K and SS. All three `packages.json` sources are non-null; the hold-out list is not in this folder (UNVERIFIED). REQ-01 holds: K does not name a source. The only lead-in fix is a conditional ("skip (2) if no driving document is named"), which is a recipe step beyond MR 1035; a card cannot be conditional.- **R-D NOTE.** "In your own review" can read as checks living inside the free half, or as a clash with CB-5. No contradiction; direction unknown. Deleting "in your own review of" would not touch CB-5, but no evidence favors either wording.
- **R-E NOT BLOCKING.** Approval covers line 2 only. REQ-33 order (14.3 decide, 14.5 freeze, 14.6 ground truth) holds. Record it in `results/owner-decisions.md` (remove the "Still open" line; note the definitions stay open to 14.2). Line 1 stays in the frozen file (test 196-198): a label blemish.
- **R-F NOT BLOCKING.** The rule judges the default. Still, any edit splits RL's byte-identical copy (DR-16) and this task may not edit RL: the fix would add a certain problem to cure an unproven one.
- **R-G NOTE.** "Eight" is test-enforced. K ending on definition (8), against SS's per-item directive, is the treatment (F5), not a shown confound.

## 4. Final

**Blocking: NO.** BD held: none. Smallest fixes tested: "Apply each one to the plan"; dropping "in your own review of". Neither is evidence-backed; each moves K in an unmeasured direction. A reasonable owner would not call the draft defective without them. No replacement bytes.

Notes held:
- N-1 Draft marker stays in the frozen file; record approval in owner-decisions.md.
- N-2 "In your own review" beside CB-5; direction unknown.
- N-3 No apply verb; report K minus Z0 next to D7.
- N-4 Definition (2) printed where C2 is not applicable; analysis ignores the mark (UNVERIFIED whether any document lacks a source).
- N-5 Approval does not cover the definitions (CORR-5).
- N-6 "Eight" hard-coded; DESIGN 724 incomplete.
- N-7 No test pins the lead-in text before the freeze; no real K run.
