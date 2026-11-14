# Merge review 2: merged-spec.md (panel process redesign)

Reviewer: independent, did not produce the document and did not edit it. Document read in full (1,249 lines). Line numbers are lines of `nested/adversarial-1/merged-spec.md` as it stands now. All arithmetic was recomputed from the document's own inputs (a throwaway script, since deleted, plus hand checks). The first review was used only for the B-1..B-7 list.

## Verdict

**PASS.** 0 blocking findings, 3 medium, 5 minor.

All seven blocking findings of the first review are fixed in the text. I found no new blocking defect and no defect introduced by the edits that rises to blocking. Every checked number recomputes.

## Status of B-1..B-7

| # | Status | Evidence |
|---|---|---|
| B-1 ember item cap and time model | Fixed | S3 (l.393): caps "ember 8, luna 1 at most 8, luna 2 at most 8", sum 24. (b) table (l.477): "8 items under the cap, and the time model uses the same 8". Step tables (l.412, l.497): "8 items", about 60 s = 41 + 3 + 8 x 2 = 60. The assignment is feasible: 12 items x 2 replicas = 24 slots; ember takes 8 search items, so the 4 other items go to both lunas and 4 x 2 + 8 = 16 = 8 + 8. Haiku panel 6 + 9 + 9 = 24 and sonnet panel 6 + 9 + 9 = 24. Fallback (l.514): 6 + 6 + 12 = 24, with an explicit "In this fallback only, ember's cap is raised from 8 to 12", ember at 41 + 3 + 12 x 2 = 68 s, below luna's b of 100 or more. Critical path b + 25 = 8 + 1 + 3 + 12 + 1 recomputes. No "9 items" or "62 s" remains (grep). See M-N1 for the part of the fallback that is not carried into REQ-20 and REQ-32. |
| B-2 Redesign 2 token percentage | Fixed | 3.2(g) (l.898) and section 4 (l.966) both read "+23% to +40%". 5 / 21.3 = 23.5%, 8.5 / 21.3 = 39.9%. No "+25%" remains. |
| B-3 gate D5 | Fixed | D5 (l.1083) now reads "in plans. Spec generality rests on HO-5 and on the spec fixtures of REQ-37; no planted spec is run." The planted set (l.1009) is 6 plans and Stage 2 has no planted spec row, so the gate is now runnable. No "in specs" remains (grep). |
| B-4 power note | Fixed | l.1100: "about 36-40 items (HO-1 11, HO-2 4-8, HO-3 12, HO-4 9)". 11 + 4 + 12 + 9 = 36; 11 + 8 + 12 + 9 = 40. Matches l.1003-1006. No "25-30" remains. |
| B-5 REQ-45 wording | Fixed | REQ-45 (l.1193): "consistency is expected only for I4 and I7 (classes C4 and C8), and only for Redesign 1 at the high end of its range". It now agrees with 3.1(d) l.558 (I4 0.40-0.71, I7 0.34-0.62), 3.2(d) l.839 and section 4 l.961. No "C4, C5, C8" consistency wording remains. The only "C4, C5, C8" is the "Strong classes" row (l.954), which is not a consistency claim (minor note 2). |
| B-6 duplicated classes per panel | Fixed | R1 (l.678), the lens table caption (l.689), the failure row (l.929) and REQ-25 (l.1153) now say: primary C2 and C4, haiku C1, sonnet C1 and C7. I re-derived from the lens table (l.691-701). Primary: C2 in luna 1 and luna 2, C4 in ember and luna 2. Haiku: C1 in luna 1 and luna 2; C2, C4 and C3 appear once. Sonnet: C1 in luna 1 and luna 2, C7 in luna 1 and luna 2; C2 (sonnet only), C4 (luna 2 only) and C3 appear once. Every class sits in at least one lens on all three panels. The caps 14 / 14 / 14, 6 / 14 / 12, 8 / 12 / 12 recompute from the row budgets 4, 6, 4, 4, 4, 4, 4, 4. |
| B-7 REQ-12 split | Fixed | REQ-12 (l.1130) is split into (a) `fallback=true` for pre-pass or lens render failure and (b) `check_skipped=true` for a post-run ledger check failure, with a test for each of the three components. 3.0.7 (l.323), S1 (l.384), S5 (l.401), R3 (l.685), the failure row (l.662) and the guard rows agree. `fallback=true` now has one meaning (the isolated brief was run). |

## What I recomputed

All matched the document unless marked.

- **Structure.** Six numbered sections (1 to 6), plus the unnumbered Recommendation, "Not checked and unverified" and Provenance summary. Exactly two redesigns named in sections 3, 4 and 5. No "Redesign 3". K, SS and RL are arms. The four non-redesigns are listed at l.155-159. REQ-01..REQ-46: 5 + 12 + 7 + 4 + 4 + 4 + 2 + 8 = 46.
- **Time, Redesign 1, primary.** Path b + 29 (8 + 1 + b + 19 + 1). b = 100: 129, +29.0%. b = 122: 151, +23.77% (23.8). Pre-pass at kill: 10 + 1 + 119 + 1 = 131 (+31.0%); 12.2 + 1 + 141 + 1 = 155.2 (+27.2%). Break-even per item 2.75 s at b = 100 (135) and 3.71 s at b = 122 (164.7). Pre-pass break-even 14 s. Mean 116: 145, +25.0%. Sum 348: 435, +25.0%. Caps 135.0, 164.7, 156.6, 469.8. Fallback b + 25. Haiku b + 37: 257 (+16.8%), 275 (+15.5%), caps 297 and 321.3. Sonnet b + 31: 290 (+12.0%), 333 (+10.3%), caps 349.65 and 407.7.
- **Time, Redesign 2, primary.** 11 rows b + 28: 128 (+28.0%), 150 (+22.95, printed 23.0). 14 rows b + 34: 134 (+34.0%), 156 (+27.9%). Mean 116: 144 (+24.1%) and 150 (+29.3%). Sum 348: 432 and 450. Break-evens 29 / 14 = 2.07 and 29 / 12 = 2.42. Haiku b + 30: 250 (+13.6%), 268 (+12.6%). Sonnet b + 30: 289 (+11.6%), 332 (+9.9%). Every cell is at or under the cap of 1.35 b. Tightest cells: 131 s (R1) and 134 s (R2) against 135.0 s.
- **Fallback ember path.** 41 + 3 + 12 x 2 = 68 s against luna at 100 s or more. Even if ember's per-item cost equalled luna's measured cost c, ember stays below luna while c < 9.8 s. So the new text is consistent with the time break-evens.
- **Coverage matrix, Redesign 1.** Low products 0.9175 (0.92); high 2.73; midpoint of the printed 0.92 and 2.73 is 1.825 (1.83). Printed rounded rows add to 0.93 and 2.75, as the note says. I7: .40 x .85 = .34, .65 x .95 = .6175 (.62). (See minor note 1 on the unrounded midpoint.)
- **Coverage matrix, Redesign 2.** Low 0.63; high 2.465 (2.47); midpoint 1.5475 (1.55). Printed rows add to 0.64 and 2.48. I7: .20 x .55 = .11, .45 x .85 = .3825 (.38).
- **Gain tables (baseline 1.83 + harness share + net share).** R1 net 0.92 - 0.90 = 0.02, 1.83 - 0.50 = 1.33, 2.73 - 0.10 = 2.63. Totals 1.83 + 0.03 + 0.02 = 1.88; 1.83 + 0.14 + 1.33 = 3.30; 1.83 + 0.34 + 2.63 = 4.80. R2 net -0.27, 1.05, 2.37. Totals 1.59, 3.02, 4.54, printed 1.6, 3.0, 4.5. H table: .08 + .03 + .03 + 0 = .14, low .02 + .01 + .00 = .03, high .16 + .08 + .10 = .34.
- **Run counts.** Stage 1: 4 x 4 x 5 = 80, 3 x 5 = 15, total 95. Stage 2: 54 + 36 + 15 + 72 + 36 + 18 = 231. Total 326; 326 x 3 = 978 ("about 980").
- **Tokens.** Baselines 64k / 191k / 139k divided by 3 = 21.3k / 63.7k / 46.3k (seed line 23 gives 64k, 191k and 139k alongside 348 s "over 3 packages"). R1 6 / 21.3 = 28.2% and 9 / 21.3 = 42.3% (printed 28% to 42%). R2 5 / 21.3 = 23.5% and 8.5 / 21.3 = 39.9% (printed 23% to 40%). 6 / 63.7 = 9.4% and 6 / 46.3 = 13.0%. Section 4 equals 3.1(g) and 3.2(g).
- **Section 4 against 3.1 and 3.2.** Elapsed rows (all four panels, both b values), found of 14, harness share, gross and net share, I7, effort (R1 450-600 + 90 + 250-400 = 790-1,090, with 450 shared 1,240-1,540; R2 120 + 70 + 40 + 80 = 310, with 450 shared 760) and token rows are identical.
- **Leftover old values.** A grep for "9 items", "about 9", "62 s", "+25%", "25-30", "in specs", "C4, C5, C8" and "9 ledger" finds only the benign cases described above (haiku/sonnet luna "9 items" is correct; "C4, C5, C8" appears only in the "Strong classes" row).
- **Invariants.** INV-001..INV-014 each have a resolution in the text and in the closing table (l.1233-1248). The ones the edits touched, INV-003 and INV-011 (ember and fallback), INV-004 (REQ-45), INV-009 (D5) and INV-010 (lens duplication), are consistent with it.
- **findings.py.** Lines 90-121 match the document's statement of limits: id regex, anchor 12-200, claim at most 300, refs at most 8, MINOR not blocking, category required, more than one `findings-v1` block gives `ok=False`.
- **Consistency of the new text.** REQ-18 (serial pre-pass, kill at min(15 s, 0.10 b)) agrees with S1. REQ-20 ("caps summing to 24") holds for primary, haiku, sonnet and the fallback (6 + 6 + 12). REQ-32 and 5.5 name the fallback sizes only as "6 items per luna; 12 rows". The new text adds nothing that contradicts REQ-18, REQ-20 or REQ-32 as written; see M-N1 for what it does not carry.

## New blocking findings

None.

## New medium findings

- **M-N1. The ember cap raise in the fallback is not carried into the requirements or the assignment rule.** The fallback (l.514) raises ember to 12 items "in this fallback only", but S3 (l.393), REQ-20 (l.1143), REQ-32 (l.1165) and 5.5 check 1 (l.1057) give only "6 items per luna". A unit test for REQ-20 that keeps ember at its primary cap of 8 would also pass, and would leave 20 slots, not 24. The fallback also puts every one of the 12 items on ember (12 items, one luna each), so ember reviews reading-routed items (E5, E6, E7) that (b) routes only to the lunas; the fallback routing is not stated. Fix: add the fallback caps (6 / 6 / 12) and the "ember reviews all 12, each item has ember plus one luna" rule to S3 and REQ-20, and the ember 12 to REQ-32.
- **M-N2. The consistency threshold is applied unevenly between the redesigns.** Redesign 1's I7 (0.34-0.62) is "expected at the high end" because its top is 0.62, while Redesign 2's I4 (0.24-0.63) has a higher top and is "not expected" (l.839, l.961). REQ-45 now bakes the asymmetry into the mandated wording ("only for Redesign 1"). The conservative direction does not mislead, but the stated reason ("the best cell is I4 at 0.24-0.63") reads as if 0.63 were below the threshold of 0.6. Say that both tops are optimistic and that the wording is a pre-registered caution, or apply the same rule to both.
- **M-N3. Spec generality for Redesign 2 now rests on HO-5 alone.** After the D5 fix, "the spec fixtures of REQ-37" are fixtures for extractors E1, E2, E5, E4 and E1 (l.1180), which exist only in Redesign 1. For Redesign 2 the only spec evidence is D2 on HO-5 with a lower bound above 0, and HO-5 was tuned on by earlier work (l.1007). Section 4.1 Q4 (l.982) also cites "REQ-21, REQ-37, D5" as "planted and hold-out results", but REQ-21 and REQ-37 are fixture tests. State plainly that the spec claim is HO-5 only for Redesign 2.

## Minor notes

1. The midpoint of the unrounded products is 1.8238 (R1), which rounds to 1.82, not 1.83. The document states that 1.83 is "the midpoint of 0.92 and 2.73" (the printed endpoints, 1.825). The wording at l.551 says both "midpoint of 0.92 and 2.73" and "sum is taken from the unrounded products". No total changes (3.28 or 3.30 both print 3.3).
2. Section 4 row "Strong classes" lists C4, C5, C8 for Redesign 1 (l.954), while consistency is expected only for C4 and C8 (I5 reach 0.23-0.54). Not contradictory, but a reader may take "strong" as "consistent". Rename the row ("mechanical triggers") or add "I5 is not expected to be consistent".
3. The idle-time phrases were not updated for ember at 60 s: "idle slack 60-90 s" (l.412) and "40-60 s before the slowest luna" (l.481). Recomputed against the Redesign 1 luna path (b + 19) the gap is 59-81 s; against Z0's luna b it is 40-62 s. Both are defensible, but say which.
4. The 21.3k baseline is 64k divided by 3 packages. The document never states that the seed's 64k is a three-package total; add "(64k over three packages divided by 3)".
5. 5.6 lists "fallbacks" among the secondary metrics but not `check_skipped`, which REQ-12(b) now creates.

First-review items M-1..M-11 and N-1..N-13 were not re-listed. The ones the edits did not touch (for example M-3 the ember re-ask mechanism, M-4 promotion category and id, M-10 label clashes) are still open and are medium or minor, not blocking.
