# Merge review: merged-spec.md (panel process redesign)

Reviewer: independent, did not produce the document. Document read in full (lines 1-1248). Line numbers below are lines of `nested/adversarial-1/merged-spec.md`.

## Verdict

**FAIL.** 7 blocking findings, 11 medium follow-up candidates, 13 minor notes.

The structure is right: six sections, exactly two redesigns, the four non-redesigns named as such, 46 requirements. Every time table, both coverage-matrix sums, both gain tables, the run counts, the effort sums and the invariant resolutions recompute or are present. The blocking findings are a set of real contradictions between sections, plus two numbers that do not recompute (Redesign 2 token percentage, the power note item count).

## What I checked (with recomputed numbers)

### 1. Time tables, 3.1(c) and 3.2(c)

Redesign 1, primary panel. Critical path = 8 + 1 + (b + 3 + 8x2) + 1 = b + 29.

| Check | Recomputed | Document | Result |
|---|---|---|---|
| b = 100 expected | 129, 29/100 = 29.0% | 129, +29.0% | OK |
| b = 122 expected | 151, 29/122 = 23.77% | 151, +23.8% | OK |
| Pre-pass at kill, b = 100 (10 + 1 + 119 + 1) | 131, +31.0% | 131, +31.0% | OK |
| Pre-pass at kill, b = 122 (12.2 + 1 + 141 + 1) | 155.2, 33.2/122 = +27.2% | 155.2, +27.2% | OK |
| Break-even per item, b = 100 | 8+1+100+3+22+1 = 135 (2.75 x 8) | 135 | OK |
| Break-even per item, b = 122 | 29.7/8 = 3.71; total 164.7 | 3.71, 164.7 | OK |
| Pre-pass break-even | 135 - 1 - 119 - 1 = 14 | 14 | OK |
| Three-package sum 348 | 3 x 29 = 87; 435; 87/348 = 25.0% | 435, +25.0% | OK |
| Mean 116 | 145, 29/116 = 25.0% | 145, +25.0% | OK |
| Caps | 1.35 x 100 = 135.0; x 122 = 164.7; x 116 = 156.6; x 348 = 469.8 | same | OK |
| Fallback b + 25 | 8 + 1 + 3 + 6x2 + 1 = 25 | b + 25 | OK |
| Haiku b + 37 | 8+1+3+24+1 = 37; 257 (+16.8%), 275 (+15.5%); caps 297, 321.3 | same | OK |
| Sonnet b + 31 | 8+1+3+18+1 = 31; 290 (+11.97%), 333 (+10.26%); caps 349.65, 407.7 | 12.0%, 10.3%, 350-408 | OK |

Redesign 2, primary panel. Critical path = 1 + (b + 4 + 2 x rows) + 1.

| Check | Recomputed | Document | Result |
|---|---|---|---|
| 11 rows | b + 28; 128 (+28.0%), 150 (28/122 = +22.95%) | same (+23.0%) | OK |
| 14 rows | b + 34; 134 (+34.0%), 156 (34/122 = +27.87%) | same (+27.9%) | OK |
| Mean 116 | 144 (+24.1%), 150 (+29.3%) | same | OK |
| Three-package sum | 348 + 84 = 432 (+24.1%); 348 + 102 = 450 (+29.3%) | same | OK |
| Break-evens | 29/14 = 2.07; 29/12 = 2.417 = 2.42; 29 = 135-1-100-4-1 | same | OK |
| Haiku | 6x4+4+2 = 30; 250 (+13.6%), 268 (+12.6%) | same | OK |
| Sonnet | 8x3+4+2 = 30; 289 (+11.58%), 332 (+9.93%) | 11.6%, 9.9% | OK |

The +35% limit holds in every stated cell. The tightest cells are 131 s (R1) and 134 s (R2) against 135.0 s.

### 2. Coverage matrices and gain tables

Redesign 1, unrounded act x s.

- Low products: .035 + .0525 + .08 + .0075 + .40 + .2275 + .02 + .035 + .06 = 0.9175, which rounds to 0.92. OK.
- High products: .245 + .28 + .315 + .075 + .7125 + .54 + .14 + .195 + .2275 = 2.73. OK.
- Midpoint (0.92 + 2.73) / 2 = 1.825, which rounds to 1.83. OK.
- Printed rounded rows add to 0.93-2.75, as the note at line 551 says. OK.
- I7: .40 x .85 = .34 and .65 x .95 = .6175, which rounds to .62. OK.

Redesign 2.

- Low products: .05 + .05 + .075 + .02 + .24 + .10 + .02 + .035 + .04 = 0.63. OK.
- High products: .255 + .255 + .28 + .14 + .63 + .36 + .14 + .195 + .21 = 2.465, which rounds to 2.47. OK.
- Midpoint = 1.55. OK.
- Printed rounded rows add to 0.64-2.48, as the note at line 832 says. OK.
- I7: .20 x .55 = .11 and .45 x .85 = .3825, which rounds to .38. OK.

Gain tables.

| Redesign | Net (gross minus displacement) | Totals | Result |
|---|---|---|---|
| 1 | 0.92-0.90 = 0.02; 1.83-0.50 = 1.33; 2.73-0.10 = 2.63 | 1.83+0.03+0.02 = 1.88; 1.83+0.14+1.33 = 3.30; 1.83+0.34+2.63 = 4.80 | OK |
| 2 | 0.63-0.90 = -0.27; 1.55-0.50 = 1.05; 2.47-0.10 = 2.37 | 1.59; 3.02; 4.54 | OK |

The H table recomputes: central .08 + .03 + .03 + 0 = .14, low .02 + .01 + .00 = .03, high .16 + .08 + .10 = .34. It matches `MR` lines 346-350.

I7 is outside every "of 14" sum. This holds in the 3.1(d) and 3.2(d) notes, the (f) tables, the section 4 table and the Conventions block (line 12). The "of 2" (section 2, line 102) against "of 1" (rows) distinction is explained. No finding.

### 3. Run counts

- Stage 1: 4x4x5 = 80, 3x5 = 15, total 95. OK.
- Stage 2: 6x3x3 = 54, 6x3x2 = 36, 1x3x5 = 15, 8x3x3 = 72, 4x3x3 = 36, 3x3x2 = 18. Sum = 231. OK.
- Total: 95 + 231 = 326. 326 x 3 = 978 reviewer runs, "about 980". OK.

### 4. Token percentages

Baseline per package: 21.3k, 63.7k, 46.3k. This matches the seed (64k, 191k, 139k, each divided by 3).

| Item | Recomputed | Document | Result |
|---|---|---|---|
| R1 +6k / +9k on 21.3k | 28.2% / 42.3% | +28% to +42% | OK |
| R2 +5k / +8.5k on 21.3k | **23.5%** / 39.9% | **+25%** to +40% | FAIL (finding B-2) |
| +6k on 63.7k | 9.4% | about +9% | OK |
| +6k on 46.3k | 12.96% | about +13% | OK |

### 5. Effort sums

- R1: 450-600 + 90 + 250-400 = 790-1,090. With 450 shared: 1,240-1,540. OK.
- R2: 120 + 70 + 40 + 80 = 310. With 450: 760. OK.

### 6. findings.py limits

I read `findings.py` lines 1-158 and the launcher lines 45-66.

- The id regex is `^[A-Za-z0-9][A-Za-z0-9._-]{0,15}$`. Anchor and anchor2 are 12-200 after flattening. Claim is at most 300. Refs are at most 8. MINOR cannot be blocking. More than one `findings-v1` block gives `ok=False`.
- CB-4 (line 211) states these limits correctly. The ledger schema (lines 268, 278-281) uses 12-200 for `quote_plan` and at most 300 for `problem`.
- `_blocks_after` scans only after the `## Findings block` heading and only for the `findings-v1` info string. A `ledger-v1` block placed above that heading is invisible to the parser. No quoted wording asks for a second `findings-v1` block, and promotion inserts inside the single block (line 311). OK.
- Launcher facts are correct. Line 50 keeps only the first `result` message. Line 57 greps `^```findings-v1`. Line 48 has `--no-session-persistence`. Citation nit: the retry loop is lines 61-64, not 61-63.
- Gap: the promotion rule (lines 306-313) does not say which `category` or `id` the harness assigns. `_check_finding` requires a valid category (finding M-4).

### 7. Leak check

I ran an automated 4-word-sequence comparison, with lowercase and punctuation split. It compared every quoted draft instruction (all `>` blocks: CB-1 to CB-5, ledger rule, sheet block, eight recipes, search-form line) plus the extractor and question tables against all 183 strings of the three `ground-truth.json` files. It found no real 4-word overlap. The one hit, "with the plan's" in R-C6, is a 3-word generic phrase. Word-level hints are in M-8.

### 8. Other checks

- REQ ids cited in the document are exactly REQ-01 to REQ-46. None is out of range.
- Group sizes are 5 + 12 + 7 + 4 + 4 + 4 + 2 + 8 = 46.
- No third redesign. The four non-redesigns are listed at lines 155-159. K is an arm, not a redesign.
- No Qwen or glm mention. Opus appears only as the blind judge.
- Reviewers are read-only. The launcher disallows Edit, Write and NotebookEdit.
- Labels HO-1..HO-6, Z0-raw, Z0, K, SS, RL, B1..I7 and C1-C8 are consistent, except the clashes in M-10. HO-n never clashes with H1-H4.

## Blocking findings

### B-1. Ember item count and caps contradict each other; the fallback breaks the cap

- **Location:** 3.1(a) S3 (line 393), 3.1(b) (line 477), step tables (lines 412, 497), fallback (line 514), REQ-20 (line 1143), REQ-32 (line 1165).
- **Evidence:**
  - S3: "Caps sum to 24. Primary panel: ember 8, luna 1 at most 8, luna 2 at most 8."
  - Line 477: "Ember takes ... about 9 in the time model, at most 8 under the cap."
  - Line 497: "S4 ember (9 items ...) about 62 (3 s sheet + 9 items x 2 s)." Nine ember items plus 8 + 8 lunas is 25 slots, not 24.
  - Line 514: "each luna's share drops to 6 items and ember takes the remainder (24 slots: 6 + 6 + 12)." Ember at 12 breaks its own cap of 8. Under the caps the fallback sums to 6 + 6 + 8 = 20.
- **Effect:** REQ-20 requires "caps summing to 24" and REQ-32 requires the 6-item fallback. The assignment algorithm (INV-011) cannot satisfy both as written, and the unit test for REQ-20 has no consistent target.
- **Suggested fix:** pick one ember number (8 or 9) for caps, tables and the time model. State the fallback caps explicitly. Either raise ember's cap to 12 in fallback with a stated reason, or change the fallback to 6 + 6 + 8 with 4 slots dropped to replica 1.

### B-2. Redesign 2 token overhead percentage does not recompute

- **Location:** 3.2(g) (line 898) and the section 4 table (line 966).
- **Evidence:** "+5k to +8.5k output (+25% to +40%)". Against the stated baseline of 21.3k, 5/21.3 = 23.5% and 8.5/21.3 = 39.9%. The same baseline gives the correct 28% and 42% for Redesign 1. The 25% appears to be 5k over a 20k baseline.
- **Suggested fix:** write "+23% to +40%" in both places.

### B-3. Gate D5 requires planted detection in specs, but no planted spec exists

- **Location:** 5.7 D5 (line 1083), planted set (line 1009), section 5.4 Stage 2 rows.
- **Evidence:**
  - D5 requires "Planted detection at least 0.40 on at least 3 of the 5 general classes ... in plans, and on at least 2 in specs."
  - The planted set is "6 full-size real plans" (line 1009), with clean twins of the same plans. No planted spec appears in 5.1 or in the Stage 2 table.
  - HO-5 is a spec, but it is a hold-out ledger of 20 real blocking rows, not planted material. D5's second sentence handles HO-5 differently (D2 with a lower bound above 0).
- **Effect:** the "in specs" clause of a pre-registered gate cannot be evaluated. A pre-registered rule that cannot be run is a defect in the decision rule.
- **Suggested fix:** either add a planted-spec set (arms, runs and counts in 5.4, and a recount of the totals), or delete the "and on at least 2 in specs" clause and state that spec generality rests on HO-5 and the fixtures (REQ-37) only.

### B-4. Power note item count does not recompute

- **Location:** 5.9 (line 1100).
- **Evidence:** "There are about 25-30 items." Stage 1 decision sets are HO-1 (11), HO-2 (4-8), HO-3 (12), HO-4 (9), per lines 1003-1006. The sum is 36-40 items.
- **Suggested fix:** correct to about 36-40 items. Note that HO-1 to HO-4 have 4 packages, as the section says.

### B-5. REQ-45 mandated wording contradicts the spec's own matrix

- **Location:** REQ-45 (line 1193) against 3.1(d) (line 558), 3.2(d) (line 839) and section 4 (line 961).
- **Evidence:**
  - REQ-45 requires the claim "consistency expected only for the mechanical classes C4, C5, C8".
  - Line 558 says consistency (reach at least 0.6) is expected only for I4 and I7 (C4 and C8), and "is not claimed for any other issue (INV-004, REQ-45)".
  - I5, the only C5 issue, has reach 0.23-0.54 in R1 and 0.10-0.36 in R2. It never reaches 0.6.
  - Line 839 and section 4 say no consistency is expected for Redesign 2.
- **Effect:** the report wording REQ-45 mandates overclaims relative to the spec's own numbers, and line 558 cites REQ-45 for the opposite. The wording was copied from the INV-004 resolution without reconciling it with the recomputed matrix.
- **Suggested fix:** change REQ-45 to "consistency expected only for I4 and I7 (C4, C8), and only for Redesign 1, at the high end", or drop C5 and add the per-redesign limit.

### B-6. "C2 and C4 are duplicated" is false for two of the three panels

- **Location:** R1 (line 678), REQ-25 (line 1153), lens table (lines 691-701).
- **Evidence:**
  - R1: "C2 and C4 are given to two reviewers." REQ-25: "C2 and C4 are duplicated." The test is "Parse the generated briefs".
  - Primary: C2 sits in luna 1 and luna 2, C4 in ember and luna 2. Duplicated.
  - Haiku panel: C2 only in luna 1, C4 only in luna 2. C1 is the duplicated class.
  - Sonnet panel: C2 only in sonnet, C4 only in luna 2. C1 and C7 are duplicated.
  - The lens table caption (line 689) and the failure-mode row (line 929) say C2 and C4 are duplicated only on the primary panel.
- **Effect:** REQ-25's test fails on generated haiku and sonnet briefs. The generic sentence at line 678 is wrong.
- **Suggested fix:** restrict REQ-25 and line 678 to the primary panel, or add the duplicate lenses to the other two panels and recheck the 12-row and 8-row caps.

### B-7. REQ-12 contradicts 3.0.7 for a ledger-check failure

- **Location:** REQ-12 (line 1130), 3.0.7 (line 323), S5 (line 401), R3 (line 685).
- **Evidence:**
  - REQ-12: "On failure of the pre-pass, the lens render or the ledger check, the harness runs the isolated brief with `fallback=true`."
  - 3.0.7: "The fallback decision is taken before any reviewer starts." A ledger check that fails "after the reviewers have finished skips demotion and promotion ... merges the findings block as the reviewers wrote it, and records `fallback=true`."
  - The ledger check runs after the reviewers finish, so it cannot run the isolated brief.
- **Effect:** the requirement and its test ("A forced exception") describe behavior the design excludes. The label `fallback=true` also means two different states (see N-12).
- **Suggested fix:** split REQ-12 in two. (a) Pre-pass or lens render failure runs the isolated brief with `fallback=true`. (b) Post-run ledger check failure merges as written and records a separate flag, for example `check_skipped=true`.

## Medium follow-up candidates

- **M-1. D2 threshold sits above the central planned gain.** D2 (line 1080) requires Z0 + 0.12 absolute found fraction. The central net redesign share is +1.33 of 14 = 0.095 (R1) and +1.05 of 14 = 0.075 (R2). Only the upper part of each range passes. The hold-out base rate differs, but the gate is stricter than the design's own central case. Say so, or justify 0.12.
- **M-2. Stage 2 entry rule and "passes" are undefined.** Line 1044: "arms that pass D1, D2 or D3". Passing the time gate D1 alone would admit a no-effect arm. Section 5.8 says "One passes: adopt it" without saying that "pass" means all of G0 and D1-D7. Define it as, for example, D1 and (D2 or D3) for entry, and all gates for adoption.
- **M-3. The ember re-ask has no working mechanism.** R3 (line 684) and REQ-27 allow an ember re-ask if `now + 30 s <= 1.35 b`. The launcher uses `--no-session-persistence` (run-reviewer.sh line 48), so `--resume` cannot work. A second fresh ember session is expressly not a redesign (line 157). 3.0.5 check 1 (line 299) also says "There is no re-ask (time)" for the shared scaffolding. Neither the launcher change nor the persistence change is in an effort table or a REQ.
- **M-4. Promotion leaves `category` and `id` unspecified.** Lines 306-313 and REQ-15 require validation by `_check_finding`, which needs a valid category and a unique id of at most 16 characters. The rule says only "the harness never writes a claim of its own". Specify the fixed category (for example `other`), the id scheme (for example `L` plus the row id) and a collision rule. Add them to the REQ-15 test.
- **M-5. The ledger instruction does not tell models to JSON-escape quotes.** The quotes are plan text with many double quotes, backslashes and wrapped lines. The wording says "Copy each quote exactly" (lines 285, 459, 727) inside JSON strings. Invalid JSON is a counted format error (line 288), so a large share of true rows may be lost. Add an escape sentence, or measure the invalid-JSON rate in the compliance spike (REQ-17).
- **M-6. R-C2 asks for more rows than its budget allows.** Line 734: "Take up to 10 rules ... For each, quote the candidate sentence ... For the three with the most conditions, trace ..." and "Write at most 6 rows". That is up to 13 row-steps in 6 rows. The text at line 711 says C2 gets 6 "because it can govern up to 10 rules". INV-010 said 10-13 rows were needed. B5 reach (C2) depends on this.
- **M-7. Pre-pass search scope is narrower than the extractors.** S1 (line 383) and REQ-24: "tests, root documents and the paths the plan names". E3 (line 424) greps "tests, scripts and docs". E4 (line 425) uses "whole-tree `git grep -F`". The 8 s pre-pass estimate and the I5 reach row assume whichever one is true.
- **M-8. Two word-level hints.** (a) "found" is in the set-word lists of R-C1 and E1 (lines 422, 732). It matches the wording of B2's criterion in the COMBO-REPORT legend. It is not a quantifier and appears in almost every criterion. (b) R-C5 and E4 name "changelogs" (lines 425, 740), the place of I5's stale claim. The 4-word lint (AO-1) cannot catch single words. Either justify them from the 6 delivered-text instances or drop "found".
- **M-9. REQ-40 names a third share the reports do not give.** REQ-40 (line 1188) lists H share, prompting share (K minus Z0) and redesign share. Lines 190, 618 and 892 give only "Z0 minus Z0-raw, and SS minus Z0" (or RL minus Z0). Align them.
- **M-10. Label clashes and dangling references.** Conventions (line 13) say "Sheet item ids are S1, S2". R1 steps are also S0-S6 (lines 376-403), and the ledger example uses `"item":"S3"` (line 268). S1 is both the pre-pass step and the first item id. "A4" (lines 394, 689) and "A7" (line 753) refer to Appendix numbers of an external plan that this document does not contain. Rename the item ids (for example `P1..P12`) and drop the appendix letters.
- **M-11. "Retried reviewer scored as zero" conflicts with the launcher.** REQ-30 (line 1163) and lines 329, 526: "A killed or retried reviewer is scored as zero findings". The launcher's retry loop (lines 61-64) exists to recover a missing block, and attempt 2 can succeed. Scoring a successful retry as zero throws away its findings and counts the loop's own repairs as misses. Score zero only for a reviewer that has no valid block after the final attempt, and report retries separately.

## Minor notes

- **N-1.** Line 262: the retry loop is lines 61-64 in run-reviewer.sh, not 61-63.
- **N-2.** Ember idle time is given as "60-90 s" (lines 412, 477), "finishes about 40-60 s before the slowest luna" (line 481), and 41 s against b = 100-122 gives 59-81 s. State one derivation.
- **N-3.** Ember cost per item is 2 s in the R1 table (line 497: "9 items x 2 s") against "about 0.4 s for ember" in the cost model (line 488). It is off the critical path, so no total changes.
- **N-4.** Line 683 says luna's report ends at "about b + 22 s". The R2 step table (lines 720, 779) says b + 26 for 11 rows. The conclusion (no luna re-ask) survives either way.
- **N-5.** Row token size is 75-90 in the cost model (line 488) and 40-90 in 3.1(g) (line 624). A PROBLEM row carries two quotes of up to 200 characters plus up to 300 characters of `problem`, which is more than 90 tokens. The +6k to +9k total cannot be derived from "8 ledger rows per luna" alone. It is marked unmeasured.
- **N-6.** D5 names "the 5 general classes" (C2, C4, C5, C6, C8). Section 4.1 Q1 (line 979) treats C7 in its broad form as general too.
- **N-7.** D7 needs a gain over K of at least 0.04. The 5.8 outcome "K within 0.03 of RL" leaves a gap from 0.03 to 0.04 with no stated action.
- **N-8.** Stage 2 rows "Haiku, 4 documents" and "Sonnet, 3 documents" (lines 1048-1049) do not say which documents.
- **N-9.** Line 29 says ember "opened 0 unnamed test files". Lines 29 and 37 give ember 8% for "touched a test file the plan never names". The first is the specific control-package file (PAT line 167); the sentence should say so.
- **N-10.** The failure-mode row at line 662 says "The cap is broken (break-even 14 s at b = 100)". The kill is at 10 s at b = 100, so the pre-pass alone cannot reach the break-even.
- **N-11.** INV-003's evidence said the 348 s figure is a sum of means and medians sum to at most 344, and that `wall_s` is per attempt only. Line 1207 keeps only the first half. The "one panel clock" (REQ-29) covers the second.
- **N-12.** `fallback=true` is used for two different states: the isolated brief was run (lines 323, 384, 685) and demotion and promotion were skipped after the run (lines 401, 685). See B-7.
- **N-13.** H2 here has no re-ask and no run-time validation step, but its gain row (+0.03) is copied unchanged from `MR` line 348, where H2 included a re-ask. The restated H2 (line 174) should carry its own justification.

## Invariant resolution map

All 14 findings have their adopted resolution written into the document. B-1 (INV-011/INV-003 fallback) and M-4 (INV-005) are defects in how two of them were written, not omissions.

| INV | Resolution found in | Notes |
|---|---|---|
| INV-001 | 3.1(a) "Offline selection-recall gate" (line 463), 3.0.8 (line 339), 5.7 G0 (line 1077), REQ-22 | S2 (line 390) logs all candidates; rank function frozen (AO-5) |
| INV-002 | 3.0.4 (lines 260-291), REQ-13, REQ-17 | Ledger in the final message; earlier messages diagnosis only (line 290) |
| INV-003 | 3.1(c) (lines 484-528), 3.2(c), 5.7 D1, REQ-29, REQ-31, REQ-32 | Break-evens 14 s and 2.75 s stated; kill at min(15 s, 0.10 b); one panel clock; 6-item fallback (but see B-1); the sum-of-means half is partial (N-11) |
| INV-004 | 3.0.8 (line 351), 3.1(d) (line 558), 3.2(d) (line 839), REQ-41, REQ-45 | Claim narrowed; per-class act bands pre-registered. REQ-45 wording conflicts with line 558 (B-5) |
| INV-005 | 3.0.5 Promotion (lines 306-313), REQ-15 | Own `problem` text, plan-side anchor, single block, log and skip. Category and id missing (M-4) |
| INV-006 | 3.1(d) (lines 535-552), 3.2(d) (lines 816-833) | Recomputed once, `s` is its own column; sums recompute |
| INV-007 | 3.0.4, 3.0.5 check 4 (line 302), REQ-14 | JSON lines, real parser, flattened tests, 0.914 squared = 0.835. JSON escaping gap (M-5) |
| INV-008 | 3.0.7 guard row (line 329), 3.1(c) and 3.2(c) "Enforced by structure", 5.7 D1, REQ-30 | 1.5 x (b + expected overhead) from launch; intention-to-treat. Retry scoring (M-11) |
| INV-009 | 5.1 planted set (line 1009), 5.7 D5, REQ-36 | Full-size real plans, at least 8 competing candidates per class. Spec clause cannot run (B-3) |
| INV-010 | 3.2(a) row budget (lines 703-711), no luna re-ask (line 683), failure-mode rows (lines 929, 934), REQ-26, REQ-27 | About 14 rows per lens; replicate a class only with evidence and idle ember. R-C2 budget (M-6); ember re-ask mechanism (M-3) |
| INV-011 | 3.1(a) S3 (lines 392-397), REQ-20 | Assignment over 24 slots; replica 1 without tool output; failures never raise survivors' load. Ember cap and fallback contradict (B-1) |
| INV-012 | 3.0.7 (line 323), 3.1(a) S1 (line 382), REQ-18 | Serial pre-pass is the single mode; parallel build is a later arm |
| INV-013 | 3.0.1 H1, 3.0.2 CB-1 (line 197), 3.0.7 guard row (line 332), REQ-01, REQ-03 | `no_source` logged; snapshot rule for documents without a commit |
| INV-014 | 3.0.2 CB-5 (line 213), 3.1(f) and 3.2(f) (displacement -0.90 / -0.50 / -0.10), 5.7 D6, REQ-42 | Range 0.1-0.9; free-review floor in the brief; D6 blocking |

The document's own closing table (lines 1233-1248) agrees with this map section by section.
