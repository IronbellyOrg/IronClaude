# combo-est-B: top 5 untried reviewer combos for /sc:workflow tasklist review (analyst B)
Basis: source.md-era rows only (-src, b4-*, sol/terra-alone-src, batch-6 *-ember); n=1 per row; read-only; no models run.

## 1. Per-model evidence (84+ valid reviewer runs; my own parse of cost.json / findings blocks, space-tolerant)
Tokens are per package per run; x3 gives the 3-package total the report uses (check: haiku x2 + grok + sonnet = 346+161+88 = 595k vs r2-sonnet-src 594k).

| Model | runs | tok/pkg (x3) | wall s | blk claims/run (defect-rich / control) | findings/run | GT hits the judge counted (src rows, by reviewer) |
|---|---|---|---|---|---|---|
| sonnet | 27 | 29.4k (88k) | 243 | 0.28 / 0.22 | 5.2 | designSpec GT3 in ~7 of 8 sonnet rows (the most reliable catch of any model); GT9 and GT5 only ever in sonnet rows; alias: 0 hits. Rarely says "blocking" |
| haiku | 33 | 57.5k (173k) | 276 | 1.00 / 1.27 | 8.6 | GT3, GT4 (r2-sonnet-src), GT7, GT2 (alias, n4-sonnet-src, b4-terra-muse-haiku); noisiest (8.6 findings) |
| grok | 21 | 53.6k (161k) | 845 | 1.29 / 1.00 | 3.7 | the ONLY source of GT6 (c3, r3) plus GT7; slow, expensive |
| luna | 51 | 4.7k (14k) | 99 | 1.12 / 1.88 | 1.3 | GT4 (r1 t4-2), GT1 and GT2 (alias, b4-terra-luna-muse, b4-muse-ember-luna2), GT7; thin but cheap |
| terra | 18 | 2.1k (6k) | 54 | 1.92 / 2.33 | 2.1 | GT3 (alone, with 2 wrong blockers), GT2 (terra-luna-muse-ember, b4-terra-muse-haiku); cheapest blocker per token |
| sol | 3 | 3.9k (12k) | 137 | 2.00 / 2.00 | 3.0 | n=3 runs only; sol-alone 1/14-1/8, 3 wb. Too little data to pick |
| wonder (muse) | 25 | 16.2k (49k) | 136 | 1.18 / 1.00 | 5.2 | GT2, GT7; in 4 of the 6 best-blocking rows. Exhausted this week |
| ember | 18 | 11.2k (33k) | 44 | 0.67 / 0.50 | 4.5 | weaker than wonder (batch 6); better control precision |

Findings that drive the picks:
- The hits are complementary, not additive. designSpec GT3 and GT7 are "easy" (nearly every panel gets them). The blocking-in-implement GTs (GT1-GT5; alias GT1-GT3) come from few reviewers: GT4 (haiku, luna), GT5 (sonnet, loosely haiku), GT6 (grok only), alias GT2 (wonder, haiku, luna, terra). Alias GT3 and GT4 were never caught by any src row, so alias recall is capped near 1-2/4 for every panel.
- Sonnet catches but labels non-blocking (0.28 claims/run). Blocking credit in sonnet rows came from a cheap blocker in the panel (r2-sonnet-src: haiku/grok; n5-sonnet-src: luna/wonder). So sonnet + cheap high-blocking-rate reviewers (terra, luna) is the cheapest way to get catch AND blocking.
- Luna/terra are the wrong-blocker engine: terra-alone 4 wb on defect-rich, sol-alone 3, luna-heavy rows 3-4. Every cheap panel below carries wb 3-4 risk; only wonder+terra+haiku (0 wb) and r2/n4-sonnet rows (1-2) were cleaner.
- Run-to-run variance is the same size as the effects: n4-sonnet 4/14 -> 0/14 and r2-sonnet 4/14-4/8 -> 2/14-1/8 on re-run with ember, so rank within +-1 GT is noise.

## 2. The five picks (ranked by expected ROI; exact multisets are all absent from the row list)
Token estimates = per-package mean x3 across 3 packages (comparable to the report). Ranges are my judgment from analog rows, not measured.

### Pick 1: sonnet + terra + luna  (~108k tokens, ~15 min wall)
- Expect defect-rich: any 2-4 /14, blocking 0-2 /8, wb 3-4. Control: 1/2, wb 1.
- Analogs: b4-sonnet-luna2 4/14-0/8 (140k, wb3), b4-sonnet-terra 2/14-0/8 (99k, wb3), b4-terra-luna-muse 3/14-2/8 (68k). Sonnet supplies GT3/GT5/GT9, terra+luna supply the blocking flags the sonnet rows lacked.
- Answers: does swapping the exhausted wonder slot of the best-ROI shortlist row for sonnet keep blocking recall at ~100k? Direct bridge between the sonnet rows and terra-luna-muse.

### Pick 2: wonder + 2x terra + luna  (~75k tokens)  [2x; NEEDS WONDER BACK]
- Expect: any 3-4, blocking 1-3, wb 3-4 (terra x2 doubles its wb exposure). Highest ROI on paper (~4-5 GT/100k) but cannot run this week.
- Evidence: terra-luna-muse 3/14-2/8 at 68k is the best ROI row; terra costs ~6k per 3 packages, so a second independent terra is nearly free (+6k). Terra blocks 1.9 claims/run.
- Answers: is a second independent terra run worth its 6k, i.e. do duplicate cheap blockers add distinct GT hits or only wrong blockers? Run Pick 3 first (same question, no wonder).

### Pick 3: sonnet + 2x terra  (~100k tokens)  [2x]
- Expect: any 2-3, blocking 0-1, wb 3-5 (worst wb risk of the five). Control 1/2.
- Evidence: sonnet-alone-style catch (GT3 in 7/8 rows), terra 1.9 blk claims/run, b4-sonnet-terra (single terra) 2/14-0/8 wb3. Terra-alone 1/14 hit GT3 only, so a second terra mostly repeats GT3 and adds wb. Honest ROI ~2.5/100k.
- Answers: the clean test of "2x of the same cheap model" with a fixed catcher: if 2x terra adds a new GT or blocking hit over Pick 1's terra+luna, duplicate runs beat model diversity.

### Pick 4: grok + terra + luna  (~181k tokens, ~25 min wall because of grok)
- Expect: any 2-4, blocking 2-3, wb 2-3. Control 1/2.
- Evidence: c3-luna-grok-src 3/14-3/8 (181k, wb1) is the best blocking-recall row under 200k; grok is the only reviewer that found designSpec GT6 (2 of 2 luna+grok rows) and GT7. r3-luna2-grok-src dropped to 1/8 with a second luna, so luna x2 did not help; terra is the untested substitute.
- Answers: does terra add blocking hits on top of luna+grok, or only wb? Not a pure ROI win (grok 54k/run) but has the best blocking evidence in the budget range.

### Pick 5: haiku + sonnet + terra  (~267k tokens)
- Expect: any 3-5, blocking 1-3, wb 2-3. Control 1-2/2.
- Evidence: haiku (GT4, GT7, GT2) is the only other model that finds the hard blocking items sonnet misses; r2-sonnet-src 4/14-4/8 (haiku x2+grok+sonnet, 594k) and n4-sonnet-src 4/14-2/8 (wonder+haiku+sonnet, 312k) both contain this core. Terra added as the cheap blocker.
- Answers: is the r2-sonnet-src leader reproducible at ~45% of its cost without grok, the second haiku and wonder? Lowest ROI of the five but highest upside (the only pick with a realistic shot at 4/8 blocking).

Not picked as a top-5: haiku x2 + terra and 2x sonnet + terra (high cost, 350k/180k, no cheap-blocker evidence beyond Pick 5). Optional single speculative add, if a 6th is wanted: terra + luna + spark (UNVERIFIED: spark untested, token cost unknown, assume ember/wonder-like 10-17k/run, ~70k total). Mark it speculation, not an estimate.

## 3. What I would NOT run
- Anything with 2x ember or ember as the only catcher: batch 6 shows ember drops 2-4 GT on every comparable row (n4-sonnet-ember 0/14), so it is cheap but uninformative; the exception worth a rerun is only n5-sonnet-ember (3/14).
- More haiku x2 / haiku-heavy panels (350k+): haiku is the noisiest reviewer (8.6 findings/run) and its wb contribution is not paid back below r2-sonnet-src's grok+sonnet partners.
- Another sonnet x2 combo: sonnet blocks at 0.28 claims/run, so a second sonnet adds catch (GT3 again) but not blocking recall.
- sol: only 3 valid runs; any sol-based pick would be extrapolating from n=3. Terra has 18 runs and the same profile.
- Any panel claiming ROI from alias GT3/GT4: no src row ever caught them, so alias recall cannot improve through model choice alone.
- Anything with 3+ grok/haiku in total or slow wall (>1500 s): token cost and wall time dominate; the data shows no blocking-recall premium.

## 4. Caveats (UNVERIFIED parts)
- Reviewer attribution of GT hits assumes the judge's R1..Rn labels are the reviewer ids sorted alphabetically (verified on r2-sonnet-src: R2=t3-1 F1 and R3=t4-1 F9 match merged-1.md). Rows whose notes cite only L-ids give no per-reviewer credit.
- Blocking-claim counts are claims in the findings block, not judge-matched; some are prose mentions.
- Per-package token means for terra/luna are small and skewed by a few long luna runs; the x3 totals are +-30%.
- All range estimates (any/blocking/wb) are judgment from n=1 analog rows; treat +-2 GT as noise.
