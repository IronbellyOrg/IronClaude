# Plan Review, cycle 3 (final): refactor-plan.md

Reviewed file: `adversarial/refactor-plan.md` (219 lines, after the cycle-2 edits). Earlier reviews: `partials/plan-review.md` (cycle 1), `partials/plan-review-2.md` (cycle 2). Reviewer: independent agent, read-only except this file. Date: 2026-11-15.

## Verdict

**FAIL**: 1 blocking finding, 9 minor findings.

- N1 is fixed. Every outline Source cell now matches its change.
- N2 is mostly fixed. The families, the range pre-pass and the `GQ C-nn` rename all work, and the pass is idempotent. One blocking residual remains (R3-B1). The closed-item rename catches only the `GQ C-nn` form. 31 other closed-item tokens still become `R1-C-nn`, which is the conflict id. In 25 value-inventory rows this gives the same item two different ids in one row.
- All ten minor findings n1-n10 were applied (n5 only for the one cite it named; see r3-m6).
- The last edits added no roadmap, branch plan, PR plan or schedule, and no overlapping ranges.

## N1 and N2 verification

### N1: outline Source column against the change Source fields

| Outline row | Outline V1 source | Change Source | Match |
|---|---|---|---|
| §2 | 108-129, 131-238, 279-435 | M-03: 108-129, 131-174, 175-238, 279-384, 385-435 | yes |
| §3 | 483-492, 494-577 | M-04: 483-492, 494-577 | yes |
| §4 | 580-733, 735-780 | M-05: 580-733; M-06: 735-780 | yes |
| §5 | 784-1153 | M-07: 784-1153 | yes |
| §6 | 1155-2807 | M-09: 1155-2807 (M-08 is new text) | yes |
| §7 | 2809-3098 | M-11: 2809-3098 (M-10 uses V2:3586-3604) | yes |
| §8 | 3105-3908 minus 3829/3860/3879/3897, with 3830/3861/3880/3898 only in 8.6; 3910-4061; 4071-4101; 4103-4122 minus 4115 | M-14: 3105-3821; M-16: 3822-3908 (four lines deleted, four moved), 3910-4030; M-17: 4031-4056; M-18: the four lines; M-19: 4057-4061; M-20: 4071-4101, 4103-4122 minus 4115 (plus the 4120 clause and the 4116 rewrite) | yes. The 3910-4061 cell combines M-16, M-17 and M-19 with no gap. The layout table V1:4063-4069 is excluded. |
| §9 | 4125-4387 | M-21: 4125-4387 | yes |
| §10 | 4389-4476 | M-22: 4389-4476 | yes |

None of the six V1 H2 lines (579, 783, 1154, 2808, 4124, 4388) is inside a range, and neither is V1:3099 (`## 8.`). The sentence "The change Source fields govern; this column only summarises them." is at plan line 22. **N1 is fixed.**

### N2: rule 3 run as written

**How the test was run.** One `uv run python` script, in rule order:
1. Closed-item rename: `C-nn` -> `R1-CLS-nn` inside V1:4260-4290, plus every `GQ C-nn` / `GQ:C-nn`.
2. Range pre-pass over the seven listed families.
3. The main pass, using the full rule 3 alternation in the given order, anchored `(?<![\w-])(ALT)(?![\w])`.

Backtick spans, URLs and `file.ext:line` cites were protected. The input was the 16 carried V1 ranges listed in the task, minus V1:3829, 3860, 3879 and 3897: 4,248 lines in all.

**Counts:**
- 43 `GQ` closed-item renames and 29 renames inside 9.3 (both match the plan).
- 32 ranges (12 `Xn-Xn`, 12 `Dn-Dn`, 5 `Cn-Cn`, 2 `Gn-Gn`, 1 `Mn-Mn`). This matches the plan's "32 such ranges are expected".
- About 8,700 main-pass replacements. The largest families are `G-nn` 890, `V-nnn` 789, `C-nn` 571, `Rnn` 529, `D-nn` 464, `Dn` 422, `Mn` 400 and `Cnn` 335.

**(a) Compound-id corruption: none.** Probes:

| Input | Output |
|---|---|
| `DOC-01` | `R1-DOC-01` |
| `INV-014` | `R1-INV-014` |
| `SC-10` | `R1-SC-10` |
| `C13-22` | `R1-C13-22` |
| `M1-01` | `R1-M1-01` |
| `GQ C-05` | `GQ R1-CLS-05` |
| `GQ:C-03` | `GQ:R1-CLS-03` |
| `D1-D16` | `R1-D1..R1-D16` |
| `X1-X14` | `R1-X1..R1-X14` |
| `C1-C14` | `R1-C1..R1-C14` |
| `M1-M4` | `R1-M1..R1-M4` |
| `G1-G11` | `R1-G1..R1-G11` |
| `Decision D-1` | `Decision R1-D-1` |
| `C-001` | `R1-C-001` |
| `CI-1` | `R1-CI-1` |
| `C05-12 R21` | `R1-C05-12 R1-R21` |
| `panel.py:46,215` | unchanged (protected) |
| `` `D1`-`D16` `` | unchanged (protected) |

The pre-pass does not touch `C13-22` or `M1-01`. `M3-A-044` (10 tokens at V1:2780-2797) becomes `R1-M3-A-044`, so the compound id is prefixed once and stays whole. The rule would turn `R25-INV-004` into `R1-R25-INV-004`, but carried V1 text contains no `R2n-INV` token. Rule 3 applies only to carried blocks, so the compare ids in new text are safe.

**Residual range second ends:** 5, all in the `H` family at V1:3286-3287: `H1-H38`, `H1-H3`, `H5-H13`, `H22-H28` and `H31-H36` become `R1-H5-H13` and so on. `H` is not in the pre-pass list. See r3-m1.

**(b) Idempotence: yes.** A second run of the whole pipeline (rename, pre-pass and main pass) changes 0 of the 4,248 lines.

**(c) V1 families still bare that run 2 uses with a different meaning.** Counts are carried tokens outside the protected spans.

**Closed items in other forms (31 tokens): BLOCKING, see R3-B1.**
- `closed item C-08` at V1:1529 and 1982.
- `Closed item C-01` to `C-25` at V1:3712-3736.
- The list continuations `GQ C-02, C-05` (V1:173) and `GQ C-09, C-10` (V1:238).
- `25 closed items (C-01 to C-25)` at V1:4476.

All 31 become `R1-C-nn`, the run 1 conflict id.

**Short families with a different meaning in V2 (minor, r3-m2):**

| Family | Count | Run 1 meaning | Run 2 meaning |
|---|---|---|---|
| `W01`-`W04` | 48 | run 1's web files, e.g. V1:3148 "W03 recommendation 4" | run 2's own web files, 47 hits, e.g. V2:2156 "W01 to W04" |
| `V1`-`V4` | 40 | `panel verify` checks, V1:1379 | severity vocabularies, V2:1325; also the merged document's own "V1/V2 = variant" sense |
| `T1`-`T4` | 31 | card excerpt / tier, V1:165, 696 | tasklist stages, V2:668-671 |
| `S1`-`S5` | 26 | rf-qa text sections, V1:540 | strength grades S0-S3, V2:294 |
| `F1`-`F6` | 33 | audit-log rows F2/F3 (V1:651) and the F1 metric | proposal features, V2:355-359 |
| `A-1`, `A-2`, `A-4` | 7 | audit checks, V1:3176, 3658 | choices A-3..A-20, including the `A-9` that M-18 cites |
| `K1`-`K4` | 4 | MR kernel layers, V1:3434 | kill lines K1-K5, V2:3516 |
| `B-1`-`B-4` | 2 | Variant B stages, V1:2802 | brief defects, V2:1272 |
| `M5`, `M9`, `M12` | 13 | probe labels, V1:2704, 2729, 2761 | moves, V2:1326 |
| `P3-B1` style | some of 122 | run 1 QA fix ids | other `Pn` uses, V2:697, 1032 |

**Same meaning in both, so leaving them bare is correct:** `E1`-`E3`, `UC-1`/`UC-2`, `EV-1`, `L0`-`L7` (lint rules), `GT1`-`GT10`, `B1`-`B7`/`I2`/`I8`/`A1`-`A3` (E2 issue and combo ids), `T-1..T-10`, `S-0..S-5` (pilot-design thresholds and stop rule), and `Tier-1`/`Tier-2`.

**(d) Tokens prefixed wrongly (not the meaning the rule assigns). Minor, r3-m3.**
- `C1`-`C3` as closure-effort tags in 9.11 (32 tokens, e.g. "(C3)"; defined at V1:4126 "Closure effort: C1 = no new work ...") become `R1-C1`..`R1-C3`. The rule reads those as run 1 constraint ids.
- E2 combo run `C3` at V1:169 ("makes run C3 protocol-different") becomes `R1-C3`, while the combo ids A1-A3 and B1-B3 stay bare.
- Research-file-local ids, e.g. "R04 G2", "R03 G3" (V1:159, 167) and "cross-validation X3" (V1:4270), become `R1-G2`/`R1-X3`. Those read as a gate and an exposure.
- The probe labels `M1`-`M4` at V1:2704, 2729 and 2761 become tracks (`R1-M1 to M5`).

No English word, plain number, table count or file name is matched. Every alternative needs an upper-case letter prefix. The `SUSPICIOUS` scan of replacements next to "file", "heading" and ".md/.py" found only real ids.

There are 29 id tokens inside 8 fenced blocks (V1:214-233, 295-318, 323-340, 389-399, 504-520, 2544-2555, 2886-2914, 2918-2942). Rule 3 does not say whether fences are protected (r3-m4).

## n1-n10 applied?

| id | applied in | result |
|---|---|---|
| n1 | M-02 (plan line 56): `V1:<n>` allowed in new text and defined in the Baseline addendum | applied |
| n2 | M-00 (a): "10 split (3 real label disputes: C-005, C-076, X-051; 7 artefacts of cluster inheritance, see rule 4)" | applied. The figures add up: 218 + 6 + 10 = 234; 218/234 = 93.2%; 224/234 = 95.7%. |
| n3 | M-19 Source "V1:4057-4061" | applied. V1:4062 is blank, V1:4063 is the table header and V1:4070 is blank. |
| n4 | rule 3: `R1-CLS-nn` and `CI-\d` in the alternation | applied. `grep -c 'CLS-'` returns 0 in both variants. |
| n5 | M-18: "R1-C13-22 R1-INV-014" | applied for the cited case. The general check of other new-text cites was not added (r3-m6). |
| n6 | rule 3: compare-artifact id rule, with the V2:3509-3525 / 3586-3670 exception, stated for the Merge Notes | applied |
| n7 | M-24 locator rule: "log ... the pattern, the full hit list and, for each hit not edited, the reason" | applied |
| n8 | rule 3: one line under each carried legend (V1:108-129, 483-492, 4126) | applied |
| n9 | M-01: "the title is set by M-00; replace V2:5 ..." | applied |
| n10 | rule 3: the `R1-Rnn` (nn > 13) and bare `R1`..`R9` note | applied |

## New blocking findings

| id | plan section | problem | evidence | exact fix |
|---|---|---|---|---|
| R3-B1 | Rule 3, closed-item rename (N2(c) residual) | **What the rule covers.** The rename covers V1:4260-4290 and the `GQ C-nn` / `GQ:C-nn` form only ("namely ..."). **What it misses.** 31 more closed-item tokens in carried blocks are written another way, and the main pass turns them into `R1-C-nn`, which is run 1's conflict id. **Effect.** The merged document mislabels 31 closed items as conflicts, against its own id rule. In 25 value-inventory rows the same item gets two ids in one row: `Closed item R1-C-01: ... \| GQ:R1-CLS-01`. | Script output: `CLOSED_WORD_FORMS_NOW_R1-C 27`. The tokens: V1:1529 and 1982 ("closed item C-08"); V1:3712-3736 ("Closed item C-01" to "C-25", the R1-V-590.. rows, each also holding `GQ:C-nn`); V1:173 ("GQ C-02, **C-05**"); V1:238 ("GQ C-09, **C-10**"); V1:4476 ("25 closed items (**C-01** to **C-25**)"). V1:2827 ("closed tuples (C-01 Cons") and V1:3841 ("not closed here (C-05 Option D") are conflicts, so they are correctly left to the main pass. | **Rule 3 wording.** Replace "namely the closed-item list V1:4260-4290 and every `GQ C-nn` / `GQ:C-nn` reference to it (43 tokens ...)" with: "namely the list V1:4260-4290 (29 tokens), every `GQ C-nn` / `GQ:C-nn` reference (43 tokens), every `C-nn` directly after the words `closed item`/`Closed item` (27 tokens: V1:1529, 1982, 3712-3736), the list continuations V1:173 `C-05` and V1:238 `C-10`, and both ends of V1:4476 `C-01 to C-25` (2 tokens); 103 tokens in total." **Script.** Add the regex `(?i)(closed items?\s+(?:\(|)?)C-(\d\d)` -> `\1R1-CLS-\2`, plus a line-pinned rename for V1:173, 238 and 4476. **Spot check.** Add one `Closed item C-` row to the 20-replacement check. **Leave unchanged.** The backticked `` `GQ:C-01` to `GQ:C-25` `` at V1:3107 is code and stays unchanged; log it. |

## New minor findings

| id | plan section | problem | evidence | exact fix |
|---|---|---|---|---|
| r3-m1 | Rule 3 range pre-pass | The `H\d{1,2}` family is not in the pre-pass list. 5 ranges keep a bare second end (`R1-H5-H13` etc.), and `H3`/`H13` then read as base-family tokens (run 2 has H1-H4). | V1:3286 "(H1-H38)"; V1:3287 "H1-H3, H5-H13, ... H22-H28, H31-H36" | Add `H\d{1,2}` to the pre-pass family list and change "32 such ranges are expected" to 37. |
| r3-m2 | Rule 3 alternation / Merge Notes | Short run 1 families still bare that run 2 uses with another meaning: `W01`-`W04` 48 (run 1's web files; this is the same case as `R\d\d`), `V1`-`V4` 40, `T1`-`T4` 31, `S1`-`S5` 26, `F1`-`F6` 33, `A-1/A-2/A-4` 7, `K1`-`K4` 4, `B-1`-`B-4` 2, `M5`/`M9`/`M12` 13. They sit inside blocks that carry the Variant 1 provenance tag and lead, so a reader can still tell they are run 1's; that keeps this minor. | contexts in section (c) above | Add `W0[1-4]` to the alternation (it is a citation family like `R\d\d`). Add one Merge Notes sentence: "Inside a carried `R1-` block, a bare short label that the id rule does not list (for example V1-V4 `panel verify` checks, T1/T2, S1-S5 rf-qa sections, F2/F3 audit rows, A-1/A-4 audit checks, K1-K4 MR kernel layers, B-1..B-4 stages, M5-M12 probe labels, P3-B1 QA ids) keeps run 1's meaning and is not a base id." |
| r3-m3 | Rule 3 notes | The rule assigns the wrong meaning to some prefixed tokens: closure-effort `C1`-`C3` in 9.11 (32 tokens), combo run `C3` (V1:169), research-local `G2`/`G3`/`X3` (V1:159, 167, 4270), probe labels `M1`-`M4` (V1:2704, 2729, 2761). | V1:4126 "Closure effort: C1 = ..."; script samples | Extend the 9.11 note: "in 9.11 `R1-Gn` means gap row n and `R1-C1`..`R1-C3` mean closure effort (V1:4126)". Exempt V1:169 `C3` and the M-labels at V1:2704, 2729 and 2761 by line, and log them. Or keep them prefixed and add these cases to the logged mechanical edits. |
| r3-m4 | Rule 3 protected spans | The rule does not say whether fenced code blocks count as "backticks". 29 id tokens sit in 8 fences, including the ASCII diagrams. Prefixing them shifts the columns by 3 characters per id. | fence lines listed in section (d) | State one choice: "fenced blocks are protected; the legend line under them covers the ids", or "fenced ids are prefixed; diagram alignment is not repaired". |
| r3-m5 | M-14 / Changes NOT Being Made | V1:3101 (owner-scope paragraph) and V1:3103 ("**Binding facts carried into every step below.**") are in no change range and have no "Not made" row, so they are dropped silently. Every fact in V1:3103 is also in carried lines, so no content is lost. | grep: "34 of 38" at V1:754, 3438...; "OD-8" at V1:2647, 3824...; "escalation_figure_after_check" at V1:2107, 2821; "alias GT3" and "audits B, C, E, F" also elsewhere | Add a "Not made" row: "V1:3099-3104 (8 H2, owner scope, binding-facts preface): superseded by M-12's lead; each binding fact is carried in 6.13/8.4 (log the grep hits)". Or carry V1:3103 as the first block of 8.4. |
| r3-m6 | New text (M-08, M-10) — n5 residual | New text still cites run 1 ids bare. M-10 C-01 cell: "defect D6"; M-10 C-04 cell and M-08 C-17 row: "run 1's C-17", "ENS-1..ENS-5". V2 uses `D6` (5 hits) and `C-17` (2 hits) for other items. | plan lines 88, 99; V2 grep counts | Add to rule 3: "New text writes every run 1 id with `R1-` (R1-D6, R1-C-17, R1-ENS-1..R1-ENS-5); M-08's guidance column ids are run 1 conflicts and are written `R1-C-nn` in the table." |
| r3-m7 | M-19 / M-27 | The carried heading V1:4057 "### 8.4 Branch-structure options" becomes `#### R1 8.4 Branch-structure options`, but the options table under it is dropped. The heading then promises options the section does not contain. | V1:4057; M-19 drops V1:4063-4069 | Exclude V1:4057 (the new `### 8.7` heading replaces it), or retitle it `#### R1 8.4 Branch-structure constraint and facts (options table dropped, M-19)` with a `Variant 1 (modified)` tag. |
| r3-m8 | Rule 3, `O-\d` and `ENS-\d` | Two-digit forms stay bare: `O-11` (V1:3444 "R1-O-1..O-11", V1:3518) and `ENS-01 to ENS-09` (V1:760). Neither collides with V2, so the only problem is inconsistency. | script: `O-nn` 2, `ENS-nn` 2 | Use `O-\d{1,2}` and `ENS-\d{1,2}`. |
| r3-m9 | Rule 3 scope | The rule must never run over new text or Appendix D: `R25-INV-004` would become `R1-R25-INV-004` because `R\d\d` matches `R25`. The plan implies this ("inside a block carried from Variant 1") but does not say it for the script. | probe output | Add: "the id pass runs only over the extracted Variant 1 blocks, before they are joined to new text". |

## Checks performed

1. **Read in full:** `refactor-plan.md` (219 lines) and `plan-review-2.md`.
2. **N1:** compared each outline row (plan lines 26-40) with the Source field of M-03, M-04, M-05, M-06, M-07, M-09, M-11, M-14 to M-21 and M-22 (table above).
3. **Line checks** with `awk` on `variant-1-original.md`:
   - V1:108-129, 483-492, 4126 (the legends);
   - V1:3097-3106, 3905-3912, 4026-4033, 4054-4073, 4098-4104, 4112-4127, 4255-4292;
   - V1:3101 and 3103 in full;
   - V1:476-482, 578, 734, 781-782, 3909, 4070, 4102, 4123 (uncarried gap lines);
   - V1:173, 238, 2827, 3107, 3712, 3841, 4476 (closed-item contexts).
4. **Rule 3 script** (`/tmp/rule3_review3.py`, run with `uv run python`):
   - the exact alternation in plan order, the anchors, and the protected spans;
   - the closed-item rename first, then the range pre-pass, then the main pass;
   - 22 probe strings;
   - the 16 carried ranges minus the four `**Dependencies:**` lines (4,248 lines);
   - per-pattern counts, the range count, idempotence (second run), and detection of bare second ends;
   - a census of the bare-token families, cross-counted against V2.
5. **Second script** (`/tmp/rule3_ctx.py`): V1 and V2 contexts for the residual families. Third script (`/tmp/rule3_second.py`): an exact list of range second ends left bare (5 `H`, plus 10 `M3-A-nnn` compounds that are not corruption).
6. **Greps:**
   - `CLS-` (0 in both variants);
   - `GQ[ :]C-nn` (45 lines in V1; 43 tokens in carried ranges outside backticks);
   - the V1:3103 facts elsewhere in V1;
   - V2 counts for `D6`, `C-17`, `ENS-1` and `W03`.
7. **Fault-finder rows** 2, 3, 4, 27 and 31 in `partials/r25-fault-finder-notes.md` support the claims in M-00 (e), M-19, M-24 items 5 and 9 and M-25.
8. **New-defect scan of the cycle-2 edits:**
   - **Overlaps:** all change ranges are pairwise disjoint, and M-18's four lines are excluded from M-16.
   - **Rules against changes:** consistent, apart from r3-m6.
   - **Roadmap, branch plan, PR plan or schedule additions:** none.
   - **Numeric claims re-derived:** 13 + 14 + 21 = 48 step statuses; 11 + 8 = 19 gates; 234 points and the two convergence percentages.
9. **Not re-checked:** the M-08 starting-guidance rows against diff rows C-050..C-075 (the plan makes the executor do this), and the M-24 locator hit lists (checked in cycle 2 and unchanged).
