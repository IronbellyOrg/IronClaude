# Analyst A: top 5 untried reviewer combos (source.md era only)

Source: COMBO-REPORT.md (read in full). Scoring: any/blocking out of 14/8 on the 2 defect-rich packages; wb = wrong blockers. All ranges are guesses from n=1 rows (UNVERIFIED as predictions).

## Corrections applied
- r2-sonnet-src = haiku x2 + grok + sonnet (4/14-4/8, 2 wb, 594k). r2-sonnet-ember = same 4 + ember as a 5th reviewer, so 4/14-4/8 to 2/14-1/8 is run-to-run variance plus an extra reviewer. It says nothing about muse. I treat ember-vs-wonder evidence as weak and use the other 5 ember rows only as noise-level evidence.
- n2-sonnet-src is 2/14-0/8 (the 8/14-5/8 score was a retracted judge failure). Not used as support.
- Blocking counts use the corrected parser (all models block). Per-run blocking rates, source.md era: luna 23 in 21 runs, muse 21/18, haiku 19/16, grok 19/15, sonnet 2/11, terra 8/3, sol 6/3.

## Per-model token cost (3 packages, derived; rough)
terra ~7k (terra-alone-src 7.2k). sol ~12k (11.6k). luna ~25k (b4-sonnet-luna2 140k minus sonnet; n5-muse-luna 64k). ember ~9k (2.5-3.5k/run). wonder ~35-50k. sonnet ~65-115k (b4-sonnet-terra 99k less terra = ~92k; r2-sonnet-src gives ~114k). haiku ~165k (n2-muse-haiku-grok-src 362k, n4-sonnet-src 311k). grok ~130-160k (c3-luna-grok-src 181k, r3-luna2-grok-src 170k). spark: UNVERIFIED, assume ~10-40k.

## Already-tried multisets (do not propose)
Src era: {muse,haiku,grok,sonnet} {haiku2,grok,sonnet} {muse,haiku,sonnet} {sonnet,luna2} {terra,muse,haiku} {terra,muse,luna} {luna,grok} {luna2,grok} {muse,haiku,grok} {muse,luna,sonnet} {sonnet,terra} {haiku,luna2} {muse,luna} {muse,luna,grok} {terra} {sol}; all ember variants and {ember,luna2}.
Earlier eras (invalid for luna/terra/sol, still counted as tried): {haiku2,grok} {muse,glm,haiku} {haiku,luna,grok} {haiku,luna2,grok} {haiku,grok} {haiku,luna} {muse,haiku,luna} plus every glm and B3 +terra/sol row. Arm B and C compositions: not in COMBO-REPORT (UNVERIFIED), so I avoided sonnet-alone-plus-obvious-adds only where listed.

## Ranked picks (expected ROI order)

### 1. terra x2 + luna  (2x pick)  ~40k tokens, ~15 min
- Expect: any 2-4/14, blocking 1-3/8, wb 3-6 (high risk: terra and sol alone each had 3-4 wb).
- Evidence: terra-alone-src 1/14, 1/8, 4 wb at 7k; sol-alone-src 1/14, 1/8, 3 wb at 12k; terra-luna-muse 3/14, 2/8 at 68k (best shortlist ROI); terra blocks at the highest per-run rate (8 in 3 runs) and luna next (23 in 21).
- Question: do two independent terra runs find different blockers (recall gain) or just repeat the same wrong ones? Cheapest test of 2x value.

### 2. luna + grok + terra  ~185k tokens
- Expect: any 3-5/14, blocking 2-4/8, wb 2-4.
- Evidence: c3-luna-grok-src 3/14, 3/8 (best blocking recall per token on the sheet except r2-sonnet-src) at 181k, 1 wb; r3-luna2-grok-src 3/14, 1/8, 4 wb at 170k (second luna did not help); terra adds ~7k and a high block rate.
- Question: does adding a cheap terra reviewer lift c3's 3/8 or only add wrong blockers? Note c3 is n=1; its 3/8 may be luck.

### 3. terra + sol + haiku  (no muse needed)  ~185k tokens
- Expect: any 2-4/14, blocking 1-3/8, wb 1-3.
- Evidence: terra-muse-haiku 3/14, 2/8, 0 wb anywhere at 234k, the only zero-wrong-blocker row; its ember version fell to 2/14-0/8 with 3 wb, and wonder is exhausted. haiku is the workhorse (19 blocking in 16 runs); sol/terra add blocker-prone cheap voices.
- Question: can the best-precision panel be rebuilt without muse by swapping in sol? Answers whether precision came from the terra+haiku pair or from muse.

### 4. sonnet x2 + luna  (2x pick)  ~215-290k tokens
- Expect: any 3-5/14, blocking 1-3/8, wb 1-3.
- Evidence: sonnet is in the 4 highest-coverage rows (r2-sonnet-src 4/14-4/8; n4-sonnet-src 4/14-2/8 at 311k, 1 wb; b4-sonnet-luna2 4/14-0/8 at 140k); sonnet's own blocking rate is low (2 in 11 runs), so a second sonnet may add coverage rather than blocking; luna carries the blocking rate.
- Question: was r2-sonnet-src's 4/8 about having a duplicated reviewer (haiku x2) or about sonnet? Sonnet x2 tests duplication on the model that adds the most findings.

### 5. spark + terra + luna  (SPECULATIVE, spark never tested)  ~50-80k tokens
- Expect: any 2-3/14, blocking 1-2/8, wb 2-3 (spark behaviour UNVERIFIED; this is a muse-slot swap into the best-ROI row).
- Evidence: terra-luna-muse 3/14, 2/8 at 68k; ember swap gave 2/14, 1/8 at 59k; wonder (exhausted) and ember are weaker or unavailable.
- Question: is spark a usable third voice (ember-class cost, wonder-class recall) so the 68k shortlist row survives wonder's absence?

## What I would NOT run
- Any 5-reviewer or glm panel: glm is excluded, and haiku x2 + grok + X rows cost 490-680k for 2-4/14, so more reviewers did not buy proportionally more (r2-sonnet-ember added a fifth and dropped).
- Another wonder or ember variant of the old top-5 panels: ember study showed noise-level changes (every row differs by 1-4 catches on n=1), so more ember rows cannot separate model from variance.
- Sonnet + luna + grok (next in line): it overlaps pick 2 (same luna+grok base) and costs ~270k; run only if pick 2 shows luna+grok is real.
- Any 2x grok or 2x haiku panel: 130-165k per extra reviewer with no evidence of independence gain beyond one r2-sonnet-src row whose 4/8 did not replicate (ember rerun 1/8).
- Re-judging or re-running rows to "fix" n=1 variance: use picks 1 and 2 with 2-3 repeats each instead of widening the model grid.

Not verified: arm B/C panel compositions, judge variance, per-run token costs (derived by subtraction from panel totals, +/- 30%), and spark behaviour.
