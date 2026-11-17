# Plan Review, cycle 2: refactor-plan.md

Reviewed file: `adversarial/refactor-plan.md` (217 lines, after the cycle-1 edits). First review: `adversarial/partials/plan-review.md`. Reviewer: independent agent, read-only. Date: 2026-11-15.

## Verdict

**FAIL**: 2 blocking findings, 10 minor findings.

- Of the cycle-1 blocking findings, 7 are fixed (B2 to B8; B6 has a small leftover, logged as minor n2). B1 is only partly fixed.
- **B1 leftover (N2).** The rule 3 regex now handles the compound ids the lead named (`DOC-01`, `INV-014`, `SC-10`, `C13-22` all come out right). It still leaves ten run 1 id families unprefixed even though run 2 uses the same tokens with other meanings. It also prefixes only the first end of 32 hyphen ranges such as `D1-D16`. And the closed-item rename misses 43 `GQ C-nn` cross-references outside V1:4260-4290.
- **New blocking defect from the edits (N1).** The Target outline table still lists the old V1 ranges. Those ranges contradict the corrected change sources and bring back the B2 and B8 defects.
- All 17 minor findings were applied as claimed.

## B1-B8 verification

| id | fix present? | correct? | evidence checked |
|---|---|---|---|
| B1 | Yes (rule 3, line 14) | **Partly.** The compound-id cases work. Real collisions remain. See N2. | `uv run python` test of the exact rule 3 alternation with the stated anchors and protected spans (backticks, URLs, `file:line`). **Samples:** `DOC-01`->`R1-DOC-01`, `INV-014`->`R1-INV-014`, `SC-10`->`R1-SC-10`, `C13-22`->`R1-C13-22`, `C-01`->`R1-C-01`. Re-applying the regex to `R1-C13-22` leaves it unchanged, so a second pass is harmless. `panel.py:46,215` is protected. **Breaks:** `D1-D16`->`R1-D1-D16`, `X1-X14`->`R1-X1-X14`, `C1-C14`->`R1-C1-C14` (the second end stays bare, because the lookbehind rejects `-`). `Decision D-1` is not prefixed. **Over the 19 carried V1 ranges:** about 8,000 replacements, with the per-pattern counts logged. 32 same-family hyphen ranges keep a bare second end. Ten colliding families are not covered (N2). |
| B2 | Yes (M-03 V1:108-129; M-04 V1:483-492, 494-577 with the 3.1 table) | Yes | V1:108 "Citation key", V1:127 verification tags, V1:483 "Conventions used in Sections 3 and 4", V1:566 "3.1 External context", V1:577 is the last table row, V1:578 is blank. The Target outline was not updated (N1). |
| B3 | Yes (M-13) | Yes | The text matches the cycle-1 wording: tracked at `ad8f57560`, pointer `ad8f57560:<path>`, Q-35 answered, push not checked. |
| B4 | Yes (M-16 steps 1-4, M-18 source, Risk Summary row) | Yes | **Line content:** V1:3829, 3860, 3879, 3897 each start with `**Dependencies:**`. V1:3830 is "Persisted formats and rollback (applies to every M1 step...)". V1:3861, 3880 and 3898 are "Rollback (M2/M3/M4; [proposed] rule)". V1:3824 is the lead ("carry no order"). The table headers sit at V1:3832, 3863, 3882 and 3900. **Copy check:** M-18 is now the only change that carries the rollback lines, so nothing is copied twice. |
| B5 | Yes (M-10) | Yes | **Rows:** 15, keyed as in V2:3511-3525 (C-01..C-12, C-13 (X-13), C-14 (X-14), C-15 (X-15)). **Cells:** the three-word status vocabulary is used. C-04, C-09, C-11 and X-14 are "Changed ... (OPEN)", C-01 is Open, and no cell says "Stands ... OPEN". **C-01 cite:** "V1:594" is D6 "CONFIRMED on both stacks" (correct, but see n1). |
| B6 | Yes (rule 4, M-04 lead, M-11 lead) | Mostly | Rule 4 names the 3 real splits and the 7 inheritance artefacts. It cites `r2-advocate-V1.md:116`, which reads "V1 on the post gate; BOTH on the rest" (checked). **Leftover:** M-00 (a) still says "10 split" with no note on the 7 artefacts (n2). |
| B7 | Yes (M-24 items 1, 4, 8, 13, 14; M-25 V1:133) | Yes | **Item 4:** the locator `grep -nE '\b50\b.{0,40}(test\|tests/pr_submit)'` hits 710, 1202, 1335, 2973, 3357, 3496, 3735, 3797, 3804, 4436, 4479, 4593. All 10 listed sites are hit. 3797 ("50 files, 47 `test_*.py`") and 4436 (`:50-62`) are extra hits. They are harmless under the locator rule ("read each hit; edit only wrong sentences"). **Item 8:** ``grep -nF 'SKILL.md` (6)'`` returns V2:1331 only (correct). **Item 1:** `grep -n KeyError` returns 16 lines. All of them are listed or deliberately kept (545, 4312), including the new V2:940. **Item 13:** `grep -n '1,398'` returns exactly 874, 1027, 1368, 3743. **Item 14:** V2:3516 holds "dropped-blocking refusal" and V2:3638 holds "a fail-closed refusal"; neither says "closes" (the instruction is correct). **M-25:** V1:133 reads "three commits ahead (9874d63fb, c2e3347d3, 792cf8c52)" (hit). **Missing piece:** the cycle-1 requirement to log each locator with its full hit list in `merge-log.md` was not added (n7). |
| B8 | Yes (M-05, M-07, M-09, M-11, M-21, M-22; M-27 sentence) | Yes | `grep -n '^## '` on V1 returns 579, 783, 1154, 2808, 4124 and 4388 (all six confirmed). The new start lines are 580, 784, 1155, 2809, 4125 and 4389 (correct). V1:3099 (`## 8.`) is not inside any change range, because M-14 starts at 3105. The Target outline still cites the ranges that contain the H2 lines (N1). |

## Minor findings applied?

All 17 were applied as Review Status line 217 claims.

| id | applied in | result |
|---|---|---|
| m1 | M-27 (`#### R1 n.m`, Appendix F map) | applied |
| m2 | M-11 (V1:3008-3048, V1:3050-3097; verified headings at V1:3008, 3050) | applied |
| m3 | M-20 (16 items, the V1:4120 clause only, the V1:4116 rewrite) | applied |
| m4 | M-25 (V1:381 only; V1:381 says "37 files and 353 tests") | applied |
| m5 | M-09 (calibrator stays, X-030) | applied |
| m6 | M-24 item 2 (V2:2044 sentence quoted; 1650/2049 conditional); NOT-made row says "marked" | applied. The site list matches the 2606.19544/AE-1 hits (1647, 1648, 1650, 1655, 2044, 2049, 2072, 2078, 2829). |
| m7 | M-01 | applied |
| m8 | M-23, M-30 (U-099 exempt) | applied |
| m9 | M-21 (per-slot keys use the M-10 wording) | applied |
| m10 | M-24 item 5 (adds 1792, 2054, 3517, 3640, 3658, 4085) | applied |
| m11 | M-24 item 1 (append at V2:1177; V2:3636 clause gone) | applied |
| m12 | M-24 item 10 (diff-analysis X-027) | applied, but it adds a `V1:<line>` cite (n1) |
| m13 | M-24 item 3 (append to V2:1033, V2:3474) | applied |
| m14 | M-26 (replace V2:10-99; V2:100-101 blank, V2:102 `---`) | applied |
| m15 | M-24 item 6 (179, 892, 1255, 1430, 2703; all hit by `grep '32 keys'`) | applied |
| m16 | rule 3 (V1:4126 kept; `R1-Gn` = gap row n in 9.11) | applied |
| m17 | rule 6, M-09 and M-11 lead sentences | applied |

## New blocking findings

| id | plan section | problem | evidence | exact fix |
|---|---|---|---|---|
| N1 | Target outline table (lines 26-36) | The edits fixed the change Source fields but left the outline's Source column unchanged. The outline is headed "what the executors build". An executor or the M-29 provenance index that follows it would: drop the two legends and the 3.1 table (B2 again); carry six V1 H2 lines plus V1:3099 `## 8.` and V1:3099-3104 (B8 again); and carry the dropped layout table V1:4063-4069 (M-19). | Outline rows: §2 "V1:131-238, 279-435"; §3 "V1:494-564"; §4 "V1:579-780"; §5 "V1:783-1153"; §6 "V1:1154-2807"; §7 "V1:2808-3098"; §8 "V1:3099-4122"; §9 "V1:4124-4387"; §10 "V1:4388-4476". These contradict M-03, M-04, M-05, M-07, M-09, M-11, M-14 to M-21 and M-22. | Set the outline Source column to the change ranges. **Base:** keep the V2 ranges unchanged. **§2:** V1:108-129, 131-238, 279-435. **§3:** V1:483-492, 494-577. **§4:** V1:580-733, 735-780. **§5:** V1:784-1153. **§6:** V1:1155-2807. **§7:** V1:2809-3098. **§8:** V1:3105-3908 (minus V1:3829, 3860, 3879, 3897; V1:3830, 3861, 3880, 3898 only in 8.6), 3910-4061, 4071-4101, 4103-4122 (minus V1:4115). **§9:** V1:4125-4387. **§10:** V1:4389-4476. Add one sentence above the table: "The change Source fields govern; this column only summarises them." |
| N2 | Rule 3 (B1 leftover) | **(a) Uncovered families.** Ten run 1 id families in the carried ranges are not in the alternation, but run 2 (base) uses the same tokens with other meanings. Examples: run 1's own debate diff points `C-001`/`X-003`/`S-007`/`A-001` versus run 2's `C-001`/`X-001`/`S-002`/`A-001` debate points; run 1's `Decision D-1` versus run 2's defect `D-1`; run 1's slices `S02` versus run 2's slice `S02` (different folders); run 1's tracks `M1` to `M4` versus run 2's moves `M1` to `M10`; run 1's `F-18` versus run 2's facts `F-1` to `F-6`; run 1's `H16` versus run 2's harness fixes `H1` to `H4`. Carried text keeps these bare, so they read as base ids. This is the same defect B1 was raised for. **(b) Ranges.** Hyphen ranges prefix only the first end: `R1-D1-D16` (9), `R1-X1-X13` (8), `R1-X1-X14` (4), `R1-G1-G11`, `R1-C1-C16`, `R1-M1-M4` and others; 32 in total. The second end (`D16`, `C16`, `X14`) is a different base id. **(c) Closed items.** The closed-item rename (`C-nn` -> `R1-CI-nn`, V1:4260-4290 only) leaves 43 references to the same closed items elsewhere (`GQ C-05` V1:163, `GQ C-12` V1:430, `GQ:C-03` V1:3574, ...). They become `GQ R1-C-05`, which reads as conflict R1-C-05 and no longer matches `R1-CI-05`. | **Counts over the carried ranges (outside protected spans):** `C-\d{3}` 77, `X-\d{3}` 26, `S-\d{3}` 25, `A-\d{3}` 44, `U-\d{3}` 8, `D-\d` 58, `S0[0-5]` 159, `M[1-4]` 749, `F-\d{1,2}` 27, `H\d{1,2}` 22. **V1 examples:** V1:1383 "S-007, C-001, C-006, X-003"; V1:1541 "A-001"; V1:1183 "Decision D-1". **V2 base uses of the same tokens:** V2:3516 "C-001 ... C-002"; V2:3517 "X-001, X-006, A-003"; V2:3523 "S-004, D-1"; V2:553 "D-1" (clearing by absence); V2:3144 `S02`; V2:361 "H1-H4 ... M1-M10"; V2:3623 "F-1". **`GQ C-nn` tokens in carried ranges:** 43 outside backticks, 8 of them in V1:142-430 and 35 in the 8.1 inventory from V1:3428 onward. V1:467-469 are in the uncarried 2.6 matrix. | **Families:** add to the rule 3 alternation, longest first: `C-\d{3}`, `X-\d{3}`, `S-\d{3}`, `A-\d{3}`, `U-\d{3}` (place each before `C-\d\d` and `A-\d\d`); `D-\d` (after `D-\d\d`); `S0[0-5]`; `M[1-4]` (after `M[1-4]-\d\d`); `F-\d{1,2}`; `H\d{1,2}`. **Range pre-pass:** before the main pass, rewrite every hyphen pair whose two ends are the same single-token family (`D\d{1,2}`, `X\d{1,2}`, `C\d{1,2}`, `G\d{1,2}`, `R\d\d`, `S0[0-5]`, `M[1-4]`), for example `D1-D16` -> `R1-D1..R1-D16`. Log each rewrite as a mechanical edit. Tested: `C13-22` and `M1-01` are not matched. **Closed items:** run the closed-item rename first and apply it to every `GQ C-nn` / `GQ:C-nn` token in all carried blocks, as well as to V1:4260-4290. **Spot check:** add one `C-nnn`, one range and one `GQ C-` token to the 20-replacement check. |

## New minor findings

| id | plan section | problem | evidence | exact fix |
|---|---|---|---|---|
| n1 | M-02 vs M-09, M-10, M-24 items 10-12 | M-02 says "`V1:<line>` is not used inside the merged document". Four changes still put `V1:<line>` cites into new text: M-09 lead "V1:2622"; M-10 C-01 "V1:594"; M-24 item 10 "run 1 V1:162", item 11 "V1:163", item 12 "V1:414". The executor must break one instruction or the other, and the cites would not resolve. | plan lines 54, 91, 97, 163-165 | Amend M-02. Allow `V1:<n>` in new text (Merge Notes, lead sentences, notes, Appendix C-F), defined in the Baseline addendum as "line n of run 1's report (byte-identical copy `adversarial/variant-1-original.md`)". Carried blocks keep their own cites. |
| n2 | M-00 (a) (B6 leftover) | The text still says "6 both-open, 10 split" with no qualification. | plan line 45; rule 4 | Write "10 split (3 real label disputes: C-005, C-076, X-051; 7 artefacts of cluster inheritance, see rule 4)". |
| n3 | M-19 Source | The Source range V1:4057-4063 includes V1:4063, which is the header row of the layout table that the same change drops (V1:4063-4069). | V1:4061 facts paragraph, V1:4062 blank, V1:4063 `\| Option \| Branch layout \|...` | Write "V1:4057-4061". |
| n4 | Rule 3 (closed-item rename) | V1 already has a `CI-1` id ("Conditional item CI-1", V1:2117, 2699; 9 lines). It is not prefixed, so `CI-1` and `R1-CI-01` (closed item 1) appear in the same document with different meanings. | `grep 'CI-1'` in the carried ranges: 9 lines | Rename the closed items to `R1-CLS-nn` instead (V1 and V2 have no `CLS-` family), or add `CI-\d` to the alternation and keep `R1-CI-nn` with zero-padded numbers. |
| n5 | M-18 new text | M-18 writes "R1-C13-22 INV-014". The same id in the carried block becomes `R1-INV-014`, and a bare `INV-014` is also a run 2 id (V2 has 399 `INV-nnn` tokens). | plan line 133 | Write "R1-C13-22 R1-INV-014". Check every other new-text cite of run 1 ids the same way. |
| n6 | Rule 3 scope (compare-artifact ids) | Compare diff ids appear raw in new text: Appendix C X-001..X-063 (M-28), M-08's diff rows C-050..C-075, and M-10 and M-21 (C-084, X-043, ...). Appendix C's `X-001`, `X-004` and `X-006` collide with run 2's own debate-point ids `X-001`, `X-004`, `X-006` (V2:3517, 3524). | V2:3517, 3524; M-28 | State in the Merge Notes id rule that 3-digit `C-`/`X-`/`S-`/`A-`/`U-` ids in new text and in Appendix C are compare diff ids, except inside V2:3509-3525 and V2:3586-3670, where they are run 2's debate points. A `CMP-` prefix on compare ids is an alternative. |
| n7 | M-24 locator rule (B7 leftover) | Cycle 1 asked for "each item's locator pattern to be logged in `merge-log.md` with its full hit list". The plan does not require it. Item 4's locator returns 2 extra hits (3797, 4436) that the executor has to judge. | plan line 153; item 4 hits | Add to the locator rule: "log the pattern, the full hit list and, for each hit not edited, the reason". |
| n8 | M-03, M-04, M-21 legends | The carried legends define bare tokens in backticks (V1:113 `S00` to `S05`; V1:112 `R01`-`R13`; V1:492 `G-nn`, `D-nn`, `D1`-`D16`; V1:4126 `Gnn`, `Cnn`). The text they explain now shows `R1-` ids. | 13 backticked id spans in the carried ranges are left unprefixed | Add one line under each carried legend: "In this merged copy, these ids carry the prefix `R1-` (Merge Notes, id rule)". |
| n9 | M-00 vs M-01 | Both changes edit the title. M-00 retitles. M-01 says "replace the title and the effort/count line by: 'Run 2: ...'", which read literally replaces the title with the research-files sentence. | plan lines 44, 50 | In M-01, write "replace V2:5 (the research-files line) by: ...; the title is set by M-00". |
| n10 | Rule 3, `R\d\d` | The pattern also prefixes `R14` to `R22` in carried text (5 lines, for example V1:2735 "C05-12 R21", a debate risk id, not a research file), so the rule's gloss "R01-R13 research files" mislabels them. The bare single-digit `R1` to `R9` (anonymised reviewers, V1:184, 195) stay unprefixed and look like the provenance prefix `R1-`. | regex run over the carried ranges | In the Merge Notes, state that `R1-Rnn` with nn > 13 is a run 1 debate risk id and that a bare `R1`..`R9` is an anonymised reviewer id, never provenance. |

## Checks performed

1. **Read in full:** `plan-review.md` (cycle 1) and the edited `refactor-plan.md`.
2. **B1 regex test.** I wrote the rule 3 alternation exactly as the plan gives it, with the anchors `(?<![\w-])`/`(?![\w])`, and protected backticks, URLs and `file:line` cites. I ran it with `uv run python` on:
   - 13 sample strings: `DOC-01`, `INV-014`, `SC-10`, `C13-22`, `C-01`, `R1-C13-22` (second pass), `C1-C14`, `D1-D16`, `X1-X14`, `R25-INV-028`, `OD-6`/`O-10`, `Decision D-1`, `C-13/X-13`;
   - the 19 carried V1 ranges.
   I then built a token-family census of the carried text and compared it with V2. A second script counted the extra families and tested the range pre-pass, confirming that `C13-22` and `M1-01` are not caught.
3. **Line checks** (all line numbers printed with awk from both variant copies):
   - **B2:** V1:106-134, 481-495, 563-582.
   - **B4:** V1:3820-3832, 3858-3863, 3877-3882, 3895-3900.
   - **B8:** `grep -n '^## '` on V1, plus V1:733-736, 780-785, 1152-1167, 2806-2812, 3097-3106, 4121-4127, 4386-4390.
   - **m2, m3, M-19:** V1:3008, 3050, 4055-4072, 4100-4122.
   - **M-25 sites:** V1:133, 162-163, 201, 204, 305, 381, 414, 705, 2381, 2513, 2622, 2657.
   - **V2 sites:** V2:1-12, 97-106 (m14), 215-216, 1647-1656, 2044, 2049, 2072, 2078, 2829, 1792, 3509-3527, 3600-3606, 3626-3632, 3517, 3640, 3658, 4085, 4232-4240, 4686-4690.
4. **B7 locators run on the variant copies:**
   - item 4 regex (12 hits; 10 listed plus 2 harmless);
   - item 8 `grep -nF` (V2:1331);
   - `KeyError` (16 lines, all covered);
   - `1,398` (4 lines, all listed);
   - `(three|3) commits ahead` on V1 (133, 4061);
   - `allowedTools` on both copies;
   - `32 keys` (5 lines, all listed);
   - `2606.19544`/AE-1/"33 to 41" (sites match item 2);
   - "closes"/"fail-closed" around V2:3500-3700.
   No corrected locator returned no hit or a wrong hit.
5. **New-defect search:**
   - **Overlaps:** compared every change Source range against the others. Only M-19's off-by-one (n3) and the stale outline (N1) were found. M-16 and M-18 no longer overlap. M-04 (ends 577) and M-05 (starts 580) leave only V1:578 (blank) and V1:579 (H2) out.
   - **Rules vs changes:** n1, n9, N1.
   - **Added roadmap, branch plan, PR plan or schedule:** checked M-10, M-16, M-19, M-20 and M-21. None is added; M-10's cells report advocate positions, not an order of work.
   - **Unsupported claims:** none new. The M-10 C-01 cite (V1:594 "CONFIRMED on both stacks") was verified.
   - **Steps that cannot be executed:** N2(c) and n4.
6. **Spot checks:** `r2-advocate-V1.md:116` (B6), and the closed-item references `GQ C-nn` in V1 (49 tokens in the whole file; 43 in carried ranges outside backticks). Section 9 `C13`/`C14` tokens are debate and constraint ids, not closed items (V1 9.5 rows Q-47..Q-52).
7. **Not re-checked:** the M-08 starting-guidance rows against diff rows C-050..C-075 (the plan itself requires the executor to do this), and the M-16 enumeration (checked in cycle 1, unchanged).
