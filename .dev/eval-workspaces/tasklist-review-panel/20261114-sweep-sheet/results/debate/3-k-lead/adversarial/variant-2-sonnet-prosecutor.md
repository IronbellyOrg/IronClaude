# Variant 2 (Sonnet prosecutor): K-arm lead-in (DD-14), default = approve `briefs/k-lead.txt` unchanged

Paths: SW = the sweep-sheet workspace; MR = the merged requirements. I re-read k-lead.txt, briefs.py, test_briefs.py, cards, freeze.sh, analyze.py and the MR sections. The orchestrator's facts F1-F9 held (151 chars, 33 words; RL copy byte-identical by `cmp`; D7 code at `analysis/analyze.py` 727-736). I found no error in the evidence pack.

## 1. Position

I looked for a blocking defect and did not find one. Verdict: no FAIL; approve as drafted. I offer no replacement text for line 2; line 1 (the draft marker) is a bookkeeping note (N-1), not a defect.

## 2. Steelman (defender's case)

Line 2 is neutral, short (151 of 1224 chars, 12%) and carries no document text, class name or hold-out detail (`briefs/k-lead.txt` line 2). The tone matches the base brief ("not a minimum number of findings", `briefs/base.txt`). K is "Z0 plus one paragraph naming the eight checks in plain words, no recipes, no sheet, no ledger" (MR 1035) and the generated paragraph is exactly that: one line, eight card definitions in order, pinned by `tests/test_briefs.py` 187-204. The definitions come from the cards, so one source governs class wording (DESIGN.md 73). Any text freezes by hash before ground truth (`bin/freeze.sh` 43; IMPLEMENTATION.md 160). K is conservative for D7: a stronger K only makes SS harder to adopt (MR 1091).

## 3. Q1-Q5

**Q1 Fair control?** Yes. K gives the reviewer the class definitions that SS never prints (SS shows id, location, text, tool lines, `question_template`; F5, DESIGN 6.1-6.3). It is not a strawman: it names all eight classes. It is weak only where MR 1035 says it must be (no locations, no tools). Not blocking.

**Q2 Leak?** None. Line 2 discloses only the number "eight". Definitions are target-neutral card fields (`cards/README.md`) and freeze before the hold-out ground truth (REQ-33, MR 1177). Caveat: the cards' `swap_test` is still empty (`cards/README.md`, open manual checks), so approving the lead-in does not approve the definitions. Not blocking.

**Q3 Length/tone vs SS?** K adds 1226 chars; SS adds 1712 plus a sheet of up to 16,000 chars (F3, DESIGN 6.3). Tone: K is descriptive; SS is imperative ("Do not skip an item", "Answer PROBLEM only when ...", `briefs/sheet-block.txt`). These differences are the treatment: D7 compares the bundles (MR 1091) and REQ-40 reports K minus Z0 as "prompting share" (MR 1194). Equalising length would be a different arm. Not blocking.

**Q4 "A plan may have none" discourages?** Weakly, if at all. Base already says "not a minimum number of findings" (`base.txt`), CB-2 pushes the other way ("Do not leave a defect out because it looks small", `cb2.txt`), and SS is the more suppressive text ("Most items are fine", `sheet-block.txt`). Hold-out plans hold 4-12 known items (MR 135-138), so "none" is the atypical case. Direction if real: lowers K, flatters SS; size UNVERIFIED (no real run, F9). Not blocking.

**Q5 Equivalent information to SS?** No, by design. K = definitions of every class; SS = place, text, tool output and a question for triggered classes only. Equivalence would erase the K test (MR 1035). Not blocking.

## 4. Verdict-rule tests

(a) Unfair to an arm: not shown. Same hash in RL (`cmp`), same Z0 base and clock (DESIGN 108, 437). The one directional risk (Q4) favours SS by an unknown amount.
(b) Unmeasurable: no. D7 is a point gain vs K (`analyze.py` 727-736); K is measured on the same documents and judge. The lead-in's own effect cannot be separated from the definitions, but REQ-40 asks only for the combined prompting share.
(c) Misleading: not as drafted. I could not make the lead-in change what a reader would conclude from K versus Z0 or SS.
(d) Breaks a requirement: no. REQ-05 covers CB-1 to CB-5 only (MR 1124); K is not a CB. REQ-23 concerns empty-sheet SS, which has no K text (`briefs.py` 110-121). REQ-33 order holds (decide 14.3, freeze 14.5, ground truth 14.6). MR 1035 shape holds (no newline pinned, test 187-204).

## 5. Strongest case against my position

The best counter-argument to "no defect" is wording friction. The lead-in says the eight kinds are for "your own review of the plan", while CB-5, placed before the paragraph in K, says "The checks you were given do not replace your own review" (`cb5.txt`; part order `briefs.py` 110-121). Read literally, the eight checks are inside the reviewer's own review in K, but separate from it in CB-5. The effect and its direction are UNVERIFIED, and CB-5 is verbatim and may not change (REQ-05). A fix would cost: a new K-only text no model has seen; a split from RL's byte-identical copy (RL DR-16, DESIGN 91; shared control); edits to DESIGN 15.1 and the test; and it moves K toward more instruction, not less. That cost exceeds an unmeasured, direction-unknown harm, so it is not a blocking defect.

## 6. Size of harm

- Lead-in share of K text: 151 of 1226 chars (12%).
- D2/D7 arithmetic (F6, derived): if D2 passes (SS - Z0 >= 0.12), D7 fails only when K - Z0 > 0.08. The lead-in must therefore push K by a margin that straddles that line to change adoption. UNVERIFIED: any shift from the lead-in alone; I have no real-model run (F9).
- Power: 5 runs x 4 documents, about 36-40 items (MR 5.9). A shift of 0.01-0.02 (my guess, UNVERIFIED) is below what these runs can resolve. A pass is "evidence, not proof" (MR 1106).

## 7. Blocking?

**NO.** No BD defect.

Non-blocking notes:
- **N-1 Draft marker stays.** Line 1 says "DRAFT, awaiting owner approval"; the test pins it (`test_briefs.py` 196-198) and `freeze.sh` does not check it, so the frozen, hashed file would still read as a draft after approval. Record the approval in `results/owner-decisions.md` with the date; changing line 1 needs a test edit and splits from RL.
- **N-2 "your own review" vs CB-5** (section 5).
- **N-3 "Eight" is hard-coded** in the lead-in, while the cards are the only class list and a new class "still enters arm K's paragraph" (DESIGN 724; `cards/README.md`). A ninth card would give "Eight kinds" over nine entries. No class is planned; low.
- **N-4 Definition (2)** names "the driving document" even where CB-1 is absent (`no_source`, DESIGN 273, 563). Whether any hold-out plan lacks a source is UNVERIFIED (hold-out list not in this folder). SS gives no C2 item there; K still names the rule.
- **N-5 Definitions not yet final** (empty swap tests); approve the lead-in only, and re-check the paragraph at the freeze.
- **N-6 Nothing tests the lead-in's text** until `freeze.json` exists (test 187-204 does not pin it). The freeze hash will.
- **N-7 No real-model K run exists** (F9). Any statement about the lead-in's effect is UNVERIFIED.
