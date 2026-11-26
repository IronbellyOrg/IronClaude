# V3 (architect) Round 2 rebuttal

SW, RL, MR as in `work/evidence-pack.md`. I re-read `analysis/analyze.py`, `briefs/*.txt`, `DESIGN.md` 273/563/788, `bin/freeze.sh`, `config/packages.json`, `results/owner-decisions.md`. I opened no ground-truth or score file.

## 1. What changed

Verdict unchanged (NO). Three of my Round 1 positions change:

- **Direction claim (ask a): weakened to a hypothesis.** F6 arithmetic: D2 needs SS minus Z0 (g) at least 0.12; D7 needs g minus k at least 0.04 (`gate_d7`, analyze.py 727-736), so with D2 passing D7 fails only if k (K minus Z0) exceeds about 0.08. A softer K lowers k, so "leans toward SS" holds only if the draft is really softer than a fair K. I cannot show that: "to look for" is already an instruction, and "in your own review" can make K stronger (the checks sit inside the protected half of CB-5). My table named a direction in row 1 and "unknowable" in row 2 for the same sentence; that was inconsistent. V2 is right that no neutral wording exists. I drop "established direction"; I keep "possible, unsized, unverified (F9)".
- **My replacement design is withdrawn as a recommendation.** "Apply each one to the plan" is as untested as the draft and may move K toward SS-lite (R-B).
- **Table row "time is not an input to D7" (ask b): wrong as written.** See section 2.

## 2. Claims of others I reject or correct

- **V1 is right against my row, but only in part.** `found_fraction` is `len(found_any)/gt_total` (analyze.py 253-254) and `gate_d7` reads only that through `_effect` (594-603); `elapsed_s` (318) is a separate series, not read by D7. So time is not a computed input. But a reviewer who splits a fixed clock differently finds a different set, so wording can move found fraction by behaviour. I overstated by turning "not an input" into "cannot change D7". Ruling: an unsized behavioural path, direction unknown, the same for any wording (mine too), so it is a note, not a blocker.
- **V2 "no neutral wording exists, so no direction":** accept for the apply verb. Reject that this makes the bias harmless: the bias is real in kind, only unsized.
- **V1 "the 0.08 bound concerns K's total gain, not the wording shift":** correct, and it cuts the other way too: a shift can only flip D7 if k_fair is above g minus 0.04 and k_draft is at or below it. MR 120 (k near 0) makes that band narrow. No arithmetic gives its width.

## 3. Rulings

- **R-A NOTE.** Strongest YES: a soft K flatters SS at D7 with no minimum effect size. It fails: direction is not established (above), the effect is confined to D7, the K-versus-RL row and the prompting share (D2 compares SS with Z0 and never reads K), and REQ-40 reports K minus Z0 openly (DESIGN 788). K still measures this paragraph's prompting share, not a best-possible checklist.
- **R-B NOTE.** An apply verb alone gives no location, tool line, question or ledger (F5); MR 36 names a structural unit of coverage. It still moves K toward SS (MR 1100). MR 1035 requires "plain words", not that verb. The draft is inside the owner's definition.
- **R-C NOTE (not blocking).** Verified: `no_source` is recorded (`scaffold/briefs.py` 177; DESIGN 563 promises "C2 reported as not applicable"); analyze.py has no filter (`class_reach` 344-355 tallies every item). Gates D2 and D7 use `found_fraction` only, so they are unchanged by C2 applicability. This is a reporting gap for all arms, not a K defect. K-only harm: definition (2) printed with no driving document named, so a reviewer may spend seconds on a vacuous check; a vacuous check cannot earn credit. All three packages in `config/packages.json` have a source (lines 8, 15, 22); the hold-out list is not here (UNVERIFIED). `freeze.sh` does not freeze analyze.py, so the filter can still be added before the first hold-out run. A lead-in fix ("skip a check that names a document you were not given") is a conditional, not a recipe, but it is not needed to make the experiment fair.
- **R-D NOTE.** Two readings with opposite pushes: checks inside the free half (K stronger) or a clash with CB-5 (K weaker or slower). SS states its separation outright (sheet-block.txt); K's does not, an asymmetry. Dropping "in your own review of" leaves CB-5 verbatim (REQ-05), but no evidence says it is better.
- **R-E NOT BLOCKING.** Only line 2 is approved; REQ-33 order holds (IMPLEMENTATION 14.3 decide, 14.5 freeze, 14.6 ground truth). Record it in `results/owner-decisions.md`: remove the "Still open" line, add date, the approved bytes and "definitions open until 14.5". Line 1 stays in the frozen file (pinned by test).
- **R-F NOT BLOCKING.** The rule judges the default. A FAIL is actionable only in SW (`k-lead.txt`, DESIGN 15.1, owner-decisions) and splits RL's byte-identical copy (DR-16); that is a cost, not a defect.
- **R-G NOTE.** "Eight" is test-pinned (`test_briefs.py` 190); DESIGN 724 is incomplete about extension. K ending on definition (8) versus SS ending on a per-item directive is the treatment (F5), not a shown confound.

## 4. Final

**Blocking: NO.** BD held: none. I tried R-A, R-C and R-D as breaks; none produced an unfair, unmeasurable, misleading or requirement-breaking default. Notes held: N-1 no apply verb (direction unverified, not established); N-2 "in your own review" beside CB-5, with a K-versus-SS asymmetry; N-3 word "checks" absent; N-4 no-source: definition (2) printed, analysis ignores `no_source` for all arms; N-5 approval covers line 2 only; N-6 draft marker stays in the frozen file. No replacement bytes.

## 5. Sentences to add to VERDICT.md (ask d)

"Read K minus Z0 as the effect of this one paragraph (the approved lead-in and the eight definitions as frozen), not as the most a plain checklist could add; no real-model K run exists and the wording was not tuned. Read SS minus K as the effect of the whole bundle SS adds (places, quoted text, search results, a question and a forced verdict per item, the ledger) over definitions alone, not as the effect of automation alone. Approval covers line 2 only; the definitions stay open until step 14.5. Before step 14.5, check the hold-out packages for `source: null`: K prints definition (2) there and the analysis does not filter class C2."
