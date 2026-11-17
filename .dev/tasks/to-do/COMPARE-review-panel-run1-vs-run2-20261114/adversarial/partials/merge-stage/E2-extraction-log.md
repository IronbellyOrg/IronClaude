# E2 extraction log (merge executor E2 of 4): transformed Variant 1 blocks

Status: DONE. Produced by `partials/merge-scripts/e2_v1_extract.py` (run with `uv run --no-project python`). Source: `variant-1-original.md` (read only). Plan: `refactor-plan.md` with reviews 2 and 3 (rule 3). All assertions in the script passed (counts, idempotence, 48 statuses, self-check).

## 1. Blocks written

| File | Change | V1 lines | V1 lines carried | Output lines |
|---|---|---|---|---|
| `v1-blocks/M03-sec2.md` | M-03 | 108-129, 131-238, 279-435 | 287 | 295 |
| `v1-blocks/M04-sec3.md` | M-04 | 483-492, 494-577 | 94 | 102 |
| `v1-blocks/M05-sec4-gaprows.md` | M-05 | 580-733 | 154 | 158 |
| `v1-blocks/M06-sec4-contradictions.md` | M-06 | 735-780 | 46 | 51 |
| `v1-blocks/M07-sec5.md` | M-07 | 784-1153 | 370 | 372 |
| `v1-blocks/M09-sec6.md` | M-09 | 1155-2807 | 1653 | 1659 |
| `v1-blocks/M11-sec7.md` | M-11 | 2809-3098 | 290 | 293 |
| `v1-blocks/M14-sec8-inventory.md` | M-14 | 3105-3821 | 717 | 723 |
| `v1-blocks/M16-sec8-migration.md` | M-16 | 3822-3908, 3910-4030 | 200 | 208 |
| `v1-blocks/M17-sec8-gates.md` | M-17 | 4031-4056 | 26 | 30 |
| `v1-blocks/M18-sec8-persisted.md` | M-18 | 3830, 3861, 3880, 3898 | 4 | 17 |
| `v1-blocks/M19-sec8-branch.md` | M-19 | 4057-4061 | 4 | 11 |
| `v1-blocks/M20-sec8-risk.md` | M-20 | 4071-4101, 4103-4122 | 50 | 55 |
| `v1-blocks/M21-sec9.md` | M-21 | 4125-4387 | 263 | 268 |
| `v1-blocks/M22-sec10.md` | M-22 | 4389-4476 | 88 | 90 |

## 2. Id pass test (sample probes, then idempotence)

| Input | Expected | Output | Second run unchanged |
|---|---|---|---|
| `DOC-01` | `R1-DOC-01` | `R1-DOC-01` | yes |
| `INV-014` | `R1-INV-014` | `R1-INV-014` | yes |
| `SC-10` | `R1-SC-10` | `R1-SC-10` | yes |
| `C13-22` | `R1-C13-22` | `R1-C13-22` | yes |
| `M1-01` | `R1-M1-01` | `R1-M1-01` | yes |
| `GQ C-05` | `GQ R1-CLS-05` | `GQ R1-CLS-05` | yes |
| `GQ:C-03` | `GQ:R1-CLS-03` | `GQ:R1-CLS-03` | yes |
| `D1-D16` | `R1-D1..R1-D16` | `R1-D1..R1-D16` | yes |
| `Closed item C-01` | `Closed item R1-CLS-01` | `Closed item R1-CLS-01` | yes |
| `closed item C-08` | `closed item R1-CLS-08` | `closed item R1-CLS-08` | yes |
| `C-001` | `R1-C-001` | `R1-C-001` | yes |
| `Decision D-1` | `Decision R1-D-1` | `Decision R1-D-1` | yes |
| `M3-A-044` | `R1-M3-A-044` | `R1-M3-A-044` | yes |
| `G-sync` | `R1-G-sync` | `R1-G-sync` | yes |
| `X1-X14` | `R1-X1..R1-X14` | `R1-X1..R1-X14` | yes |
| `H1-H38` | `R1-H1..R1-H38` | `R1-H1..R1-H38` | yes |
| `M1-M4` | `R1-M1..R1-M4` | `R1-M1..R1-M4` | yes |
| `C05-12 R21` | `R1-C05-12 R1-R21` | `R1-C05-12 R1-R21` | yes |
| `CI-1` | `R1-CI-1` | `R1-CI-1` | yes |
| `O-11` | `R1-O-11` | `R1-O-11` | yes |
| `ENS-01` | `R1-ENS-01` | `R1-ENS-01` | yes |
| ``D1`-`D16`` | ``D1`-`D16`` | ``D1`-`D16`` | yes |
| `panel.py:46,215` | `panel.py:46,215` | `panel.py:46,215` | yes |
| `UC-1 EV-1 GT1 R1..Rn` | `UC-1 EV-1 GT1 R1..Rn` | `UC-1 EV-1 GT1 R1..Rn` | yes |
| `https://arxiv.org/abs/2509.01494 C-01` | `https://arxiv.org/abs/2509.01494 R1-C-01` | `https://arxiv.org/abs/2509.01494 R1-C-01` | yes |

Idempotence on the real blocks (steps 1-3 run twice on every carried line; lines changed by the second run):

- `M03-sec2.md`: 287 lines, 0 changed
- `M04-sec3.md`: 94 lines, 0 changed
- `M05-sec4-gaprows.md`: 154 lines, 0 changed
- `M06-sec4-contradictions.md`: 46 lines, 0 changed
- `M07-sec5.md`: 370 lines, 0 changed
- `M09-sec6.md`: 1653 lines, 0 changed
- `M11-sec7.md`: 290 lines, 0 changed
- `M14-sec8-inventory.md`: 717 lines, 0 changed
- `M16-sec8-migration.md`: 200 lines, 0 changed
- `M17-sec8-gates.md`: 26 lines, 0 changed
- `M18-sec8-persisted.md`: 4 lines, 0 changed
- `M19-sec8-branch.md`: 4 lines, 0 changed
- `M20-sec8-risk.md`: 50 lines, 0 changed
- `M21-sec9.md`: 263 lines, 0 changed
- `M22-sec10.md`: 88 lines, 0 changed

Note: the pass is never run on new text. Run on `R25-INV-004` it would give `R1-R25-INV-004` (`R\d\d` matches `R25`); every new sentence (leads, legend lines, notes, status cells) is added after the pass (step 4).

## 3. Closed-item rename (rule 3, step 1)

| Kind | Count |
|---|---|
| GQ C-nn / GQ:C-nn | 43 |
| line pin (plan) | 3 |
| after 'closed item(s)' | 28 |
| line pin (extra, executor) | 4 |
| list V1:4260-4290 | 29 |
| **plan scope total (list + GQ + after 'closed item' + plan line pins)** | **103** (plan: 103) |

Reconciliation with the plan's split: the plan counts 27 tokens after the words `closed item` (V1:1529, 1982, 3712-3736) and 2 line-pinned tokens at V1:4476. The regex `(?i)(closed items?\s+\(?)C-(\d\d)` also matches V1:4476 "25 closed items (C-01", so the regex gives 28 and the V1:4476 line pin renames only `C-25`. Same 103 tokens.

**Extra, beyond the plan's 103 (flag for the orchestrator).** V1:3736 (inventory row R1-V-614, "Closed item C-25: eleven gaps ... answered by sibling files (C-01, C-02, C-04 to C-12)") holds 4 more closed-item tokens that the plan's enumeration does not list. Left to the main pass they would become `R1-C-01` etc. (conflict ids) in the same row as `R1-CLS-25`, the defect R3-B1 describes; the same list at V1:4290 is renamed by the plan. The script renames them by a line pin (`EXTRA_PINS` in the script; delete that one entry to revert). Total renamed: 107.

Left unchanged and logged: V1:3107 `` `GQ:C-01` to `GQ:C-25` `` (code span, protected). V1:2827 "(C-01 Cons" and V1:3841 "(C-05 Option D" are conflicts and go to the main pass (`R1-C-01`, `R1-C-05`). V1:114 legend `C-nn` is a placeholder in a code span.

All renames:

| V1 line | Kind | Before | After |
|---|---|---|---|
| 142 | GQ C-nn / GQ:C-nn | `GQ C-02` | `GQ R1-CLS-02` |
| 163 | GQ C-nn / GQ:C-nn | `GQ C-05` | `GQ R1-CLS-05` |
| 173 | GQ C-nn / GQ:C-nn | `GQ C-02` | `GQ R1-CLS-02` |
| 173 | line pin (plan) | `C-05` | `R1-CLS-05` |
| 199 | GQ C-nn / GQ:C-nn | `GQ C-09` | `GQ R1-CLS-09` |
| 200 | GQ C-nn / GQ:C-nn | `GQ C-10` | `GQ R1-CLS-10` |
| 238 | GQ C-nn / GQ:C-nn | `GQ C-09` | `GQ R1-CLS-09` |
| 238 | line pin (plan) | `C-10` | `R1-CLS-10` |
| 347 | GQ C-nn / GQ:C-nn | `GQ C-01` | `GQ R1-CLS-01` |
| 430 | GQ C-nn / GQ:C-nn | `GQ C-12` | `GQ R1-CLS-12` |
| 1529 | after 'closed item(s)' | `closed item C-08` | `closed item R1-CLS-08` |
| 1982 | after 'closed item(s)' | `closed item C-08` | `closed item R1-CLS-08` |
| 3428 | GQ C-nn / GQ:C-nn | `GQ:C-13` | `GQ:R1-CLS-13` |
| 3452 | GQ C-nn / GQ:C-nn | `GQ:C-08` | `GQ:R1-CLS-08` |
| 3574 | GQ C-nn / GQ:C-nn | `GQ:C-03` | `GQ:R1-CLS-03` |
| 3598 | GQ C-nn / GQ:C-nn | `GQ:C-03` | `GQ:R1-CLS-03` |
| 3665 | GQ C-nn / GQ:C-nn | `GQ:C-16` | `GQ:R1-CLS-16` |
| 3665 | GQ C-nn / GQ:C-nn | `GQ:C-16` | `GQ:R1-CLS-16` |
| 3667 | GQ C-nn / GQ:C-nn | `GQ:C-12` | `GQ:R1-CLS-12` |
| 3680 | GQ C-nn / GQ:C-nn | `GQ:C-23` | `GQ:R1-CLS-23` |
| 3687 | GQ C-nn / GQ:C-nn | `GQ:C-17` | `GQ:R1-CLS-17` |
| 3689 | GQ C-nn / GQ:C-nn | `GQ:C-20` | `GQ:R1-CLS-20` |
| 3712 | GQ C-nn / GQ:C-nn | `GQ:C-01` | `GQ:R1-CLS-01` |
| 3712 | after 'closed item(s)' | `Closed item C-01` | `Closed item R1-CLS-01` |
| 3713 | GQ C-nn / GQ:C-nn | `GQ:C-02` | `GQ:R1-CLS-02` |
| 3713 | after 'closed item(s)' | `Closed item C-02` | `Closed item R1-CLS-02` |
| 3714 | GQ C-nn / GQ:C-nn | `GQ:C-03` | `GQ:R1-CLS-03` |
| 3714 | after 'closed item(s)' | `Closed item C-03` | `Closed item R1-CLS-03` |
| 3715 | GQ C-nn / GQ:C-nn | `GQ:C-04` | `GQ:R1-CLS-04` |
| 3715 | after 'closed item(s)' | `Closed item C-04` | `Closed item R1-CLS-04` |
| 3716 | GQ C-nn / GQ:C-nn | `GQ:C-05` | `GQ:R1-CLS-05` |
| 3716 | after 'closed item(s)' | `Closed item C-05` | `Closed item R1-CLS-05` |
| 3717 | GQ C-nn / GQ:C-nn | `GQ:C-06` | `GQ:R1-CLS-06` |
| 3717 | after 'closed item(s)' | `Closed item C-06` | `Closed item R1-CLS-06` |
| 3718 | GQ C-nn / GQ:C-nn | `GQ:C-07` | `GQ:R1-CLS-07` |
| 3718 | after 'closed item(s)' | `Closed item C-07` | `Closed item R1-CLS-07` |
| 3719 | GQ C-nn / GQ:C-nn | `GQ:C-08` | `GQ:R1-CLS-08` |
| 3719 | after 'closed item(s)' | `Closed item C-08` | `Closed item R1-CLS-08` |
| 3720 | GQ C-nn / GQ:C-nn | `GQ:C-09` | `GQ:R1-CLS-09` |
| 3720 | after 'closed item(s)' | `Closed item C-09` | `Closed item R1-CLS-09` |
| 3721 | GQ C-nn / GQ:C-nn | `GQ:C-10` | `GQ:R1-CLS-10` |
| 3721 | after 'closed item(s)' | `Closed item C-10` | `Closed item R1-CLS-10` |
| 3722 | GQ C-nn / GQ:C-nn | `GQ:C-11` | `GQ:R1-CLS-11` |
| 3722 | after 'closed item(s)' | `Closed item C-11` | `Closed item R1-CLS-11` |
| 3723 | GQ C-nn / GQ:C-nn | `GQ:C-12` | `GQ:R1-CLS-12` |
| 3723 | after 'closed item(s)' | `Closed item C-12` | `Closed item R1-CLS-12` |
| 3724 | GQ C-nn / GQ:C-nn | `GQ:C-13` | `GQ:R1-CLS-13` |
| 3724 | after 'closed item(s)' | `Closed item C-13` | `Closed item R1-CLS-13` |
| 3725 | GQ C-nn / GQ:C-nn | `GQ:C-14` | `GQ:R1-CLS-14` |
| 3725 | after 'closed item(s)' | `Closed item C-14` | `Closed item R1-CLS-14` |
| 3726 | GQ C-nn / GQ:C-nn | `GQ:C-15` | `GQ:R1-CLS-15` |
| 3726 | after 'closed item(s)' | `Closed item C-15` | `Closed item R1-CLS-15` |
| 3727 | GQ C-nn / GQ:C-nn | `GQ:C-16` | `GQ:R1-CLS-16` |
| 3727 | after 'closed item(s)' | `Closed item C-16` | `Closed item R1-CLS-16` |
| 3728 | GQ C-nn / GQ:C-nn | `GQ:C-17` | `GQ:R1-CLS-17` |
| 3728 | after 'closed item(s)' | `Closed item C-17` | `Closed item R1-CLS-17` |
| 3729 | GQ C-nn / GQ:C-nn | `GQ:C-18` | `GQ:R1-CLS-18` |
| 3729 | after 'closed item(s)' | `Closed item C-18` | `Closed item R1-CLS-18` |
| 3730 | GQ C-nn / GQ:C-nn | `GQ:C-19` | `GQ:R1-CLS-19` |
| 3730 | after 'closed item(s)' | `Closed item C-19` | `Closed item R1-CLS-19` |
| 3731 | GQ C-nn / GQ:C-nn | `GQ:C-20` | `GQ:R1-CLS-20` |
| 3731 | after 'closed item(s)' | `Closed item C-20` | `Closed item R1-CLS-20` |
| 3732 | GQ C-nn / GQ:C-nn | `GQ:C-21` | `GQ:R1-CLS-21` |
| 3732 | after 'closed item(s)' | `Closed item C-21` | `Closed item R1-CLS-21` |
| 3733 | GQ C-nn / GQ:C-nn | `GQ:C-22` | `GQ:R1-CLS-22` |
| 3733 | after 'closed item(s)' | `Closed item C-22` | `Closed item R1-CLS-22` |
| 3734 | GQ C-nn / GQ:C-nn | `GQ:C-23` | `GQ:R1-CLS-23` |
| 3734 | after 'closed item(s)' | `Closed item C-23` | `Closed item R1-CLS-23` |
| 3735 | GQ C-nn / GQ:C-nn | `GQ:C-24` | `GQ:R1-CLS-24` |
| 3735 | after 'closed item(s)' | `Closed item C-24` | `Closed item R1-CLS-24` |
| 3736 | GQ C-nn / GQ:C-nn | `GQ:C-25` | `GQ:R1-CLS-25` |
| 3736 | after 'closed item(s)' | `Closed item C-25` | `Closed item R1-CLS-25` |
| 3736 | line pin (extra, executor) | `C-01` | `R1-CLS-01` |
| 3736 | line pin (extra, executor) | `C-02` | `R1-CLS-02` |
| 3736 | line pin (extra, executor) | `C-04` | `R1-CLS-04` |
| 3736 | line pin (extra, executor) | `C-12` | `R1-CLS-12` |
| 4266 | list V1:4260-4290 | `C-01` | `R1-CLS-01` |
| 4267 | list V1:4260-4290 | `C-02` | `R1-CLS-02` |
| 4268 | list V1:4260-4290 | `C-03` | `R1-CLS-03` |
| 4269 | list V1:4260-4290 | `C-04` | `R1-CLS-04` |
| 4270 | list V1:4260-4290 | `C-05` | `R1-CLS-05` |
| 4271 | list V1:4260-4290 | `C-06` | `R1-CLS-06` |
| 4272 | list V1:4260-4290 | `C-07` | `R1-CLS-07` |
| 4273 | list V1:4260-4290 | `C-08` | `R1-CLS-08` |
| 4274 | list V1:4260-4290 | `C-09` | `R1-CLS-09` |
| 4275 | list V1:4260-4290 | `C-10` | `R1-CLS-10` |
| 4276 | list V1:4260-4290 | `C-11` | `R1-CLS-11` |
| 4277 | list V1:4260-4290 | `C-12` | `R1-CLS-12` |
| 4278 | list V1:4260-4290 | `C-13` | `R1-CLS-13` |
| 4279 | list V1:4260-4290 | `C-14` | `R1-CLS-14` |
| 4280 | list V1:4260-4290 | `C-15` | `R1-CLS-15` |
| 4281 | list V1:4260-4290 | `C-16` | `R1-CLS-16` |
| 4282 | list V1:4260-4290 | `C-17` | `R1-CLS-17` |
| 4283 | list V1:4260-4290 | `C-18` | `R1-CLS-18` |
| 4284 | list V1:4260-4290 | `C-19` | `R1-CLS-19` |
| 4285 | list V1:4260-4290 | `C-20` | `R1-CLS-20` |
| 4286 | list V1:4260-4290 | `C-21` | `R1-CLS-21` |
| 4287 | list V1:4260-4290 | `C-22` | `R1-CLS-22` |
| 4288 | list V1:4260-4290 | `C-23` | `R1-CLS-23` |
| 4289 | list V1:4260-4290 | `C-24` | `R1-CLS-24` |
| 4290 | list V1:4260-4290 | `C-25` | `R1-CLS-25` |
| 4290 | list V1:4260-4290 | `C-01` | `R1-CLS-01` |
| 4290 | list V1:4260-4290 | `C-02` | `R1-CLS-02` |
| 4290 | list V1:4260-4290 | `C-04` | `R1-CLS-04` |
| 4290 | list V1:4260-4290 | `C-12` | `R1-CLS-12` |
| 4476 | after 'closed item(s)' | `closed items (C-01` | `closed items (R1-CLS-01` |
| 4476 | line pin (plan) | `C-25` | `R1-CLS-25` |

## 4. Range pre-pass (rule 3, step 2)

37 ranges (plan: 37). Each is a mechanical edit.

| V1 line | Before | After |
|---|---|---|
| 539 | `X1-X14` | `R1-X1..R1-X14` |
| 583 | `M1-M4` | `R1-M1..R1-M4` |
| 585 | `D1-D16` | `R1-D1..R1-D16` |
| 760 | `D1-D16` | `R1-D1..R1-D16` |
| 763 | `D1-D16` | `R1-D1..R1-D16` |
| 763 | `D1-D16` | `R1-D1..R1-D16` |
| 1879 | `C1-C4` | `R1-C1..R1-C4` |
| 1984 | `C1-C3` | `R1-C1..R1-C3` |
| 2517 | `D1-D16` | `R1-D1..R1-D16` |
| 2559 | `D1-D16` | `R1-D1..R1-D16` |
| 2574 | `X1-X13` | `R1-X1..R1-X13` |
| 2582 | `X1-X14` | `R1-X1..R1-X14` |
| 2602 | `X1-X13` | `R1-X1..R1-X13` |
| 2616 | `X1-X13` | `R1-X1..R1-X13` |
| 2827 | `X1-X13` | `R1-X1..R1-X13` |
| 2980 | `X1-X14` | `R1-X1..R1-X14` |
| 2980 | `X1-X13` | `R1-X1..R1-X13` |
| 3284 | `G1-G11` | `R1-G1..R1-G11` |
| 3286 | `H1-H38` | `R1-H1..R1-H38` |
| 3287 | `H1-H3` | `R1-H1..R1-H3` |
| 3287 | `H5-H13` | `R1-H5..R1-H13` |
| 3287 | `H22-H28` | `R1-H22..R1-H28` |
| 3287 | `H31-H36` | `R1-H31..R1-H36` |
| 3293 | `D1-D16` | `R1-D1..R1-D16` |
| 3293 | `D1-D16` | `R1-D1..R1-D16` |
| 3356 | `D2-D4` | `R1-D2..R1-D4` |
| 3356 | `D2-D4` | `R1-D2..R1-D4` |
| 3438 | `D1-D5` | `R1-D1..R1-D5` |
| 3577 | `X1-X13` | `R1-X1..R1-X13` |
| 3651 | `C1-C16` | `R1-C1..R1-C16` |
| 3673 | `X1-X13` | `R1-X1..R1-X13` |
| 3673 | `X1-X13` | `R1-X1..R1-X13` |
| 3680 | `G1-G11` | `R1-G1..R1-G11` |
| 3691 | `C1-C16` | `R1-C1..R1-C16` |
| 3828 | `D1-D16` | `R1-D1..R1-D16` |
| 3896 | `X1-X14` | `R1-X1..R1-X14` |
| 4166 | `C1-C2` | `R1-C1..R1-C2` |

## 5. Main id pass (rule 3, step 3): replacements per pattern

| Family | Pattern | Count |
|---|---|---|
| Cnn-nn | `C\d\d-\d\d` | 181 |
| C-nnn | `C-\d{3}` | 77 |
| X-nnn | `X-\d{3}` | 26 |
| S-nnn | `S-\d{3}` | 25 |
| A-nnn | `A-\d{3}` | 44 |
| U-nnn | `U-\d{3}` | 8 |
| Cn | `C\d{1,2}` | 605 |
| C-nn | `C-\d\d` | 524 |
| Q-nn | `Q-\d\d` | 286 |
| O-n | `O-\d{1,2}` | 132 |
| OD-n | `OD-\d+` | 49 |
| H-A..C | `H-[A-C]` | 50 |
| Hn | `H\d{1,2}` | 17 |
| W0n | `W0[1-4]` | 48 |
| Dn | `D\d{1,2}` | 643 |
| D-nn | `D-\d\d` | 464 |
| D-n | `D-\d` | 58 |
| G-nn | `G-\d\d` | 890 |
| Gn | `G\d{1,2}` | 96 |
| G-name | `G-(?:all|bench|exit|new|pr|replay|skills|sync)` | 16 |
| BL-nn | `BL-\d\d` | 160 |
| MS-nn | `MS-\d\d` | 188 |
| ENS-n | `ENS-\d{1,2}` | 99 |
| DOC-nn | `DOC-\d\d` | 247 |
| OPEN-nn | `OPEN-\d\d` | 21 |
| SC-n | `SC-\d{1,2}` | 98 |
| K-n | `K-\d{1,2}` | 17 |
| Mn-nn | `M[1-4]-\d\d` | 318 |
| Mn | `M[1-4]` | 383 |
| S0n | `S0[0-5]` | 159 |
| F-n | `F-\d{1,2}` | 27 |
| V-nnn | `V-\d{3}` | 789 |
| Xn | `X\d{1,2}` | 76 |
| A-nn | `A-\d\d` | 8 |
| INV-nnn | `INV-\d{3}` | 317 |
| Rnn | `R\d\d` | 529 |
| CI-n | `CI-\d` | 11 |
| **total** | | **7686** |

Exempted by line (rule 3: V1:169 `C3` combo run; probe labels M1-M4 at V1:2704, 2729, 2761):

- V1:169 `C3` kept bare
- V1:2704 `M1` kept bare
- V1:2704 `M1` kept bare
- V1:2704 `M2` kept bare
- V1:2729 `M3` kept bare
- V1:2729 `M2` kept bare
- V1:2761 `M1` kept bare

Prefixed tokens whose run 1 meaning is not the family meaning (kept prefixed, as the plan's final rule 3 does not exempt them; review 3 r3-m3 allowed either): 

- V1:159 `G3` -> `R1-G3` (context: "#530) pending | S04 §0.6; R03 G3; GQ O-5 |")
- V1:167 `G2` -> `R1-G2` (context: "d` has no implementation (R04 G2 [CODE-CONTRADICTED as an impl")
- V1:167 `G3` -> `R1-G3` (context: "e is consumed by nothing (R04 G3); the only served-model extra")
- V1:4270 `G4` -> `R1-G4` (context: "s a real value; `research/03` G4 and cross-validation X3 |")
- V1:4270 `X3` -> `R1-X3` (context: "h/03` G4 and cross-validation X3 |")
- V1:4170 `D5` -> `R1-D5` (context: "rt and undefined); G-37 (rule D5 `N_eff = min(--reviewers, ali")
- 9.11 closure-effort tags `C1`-`C3` -> `R1-C1`..`R1-C3`; the 9.11 note line states this meaning (rule 3).

## 6. Protected spans

- Code spans: 10225; URLs: 183; `file.ext[:line]` cites: 64 (counted on carried lines outside fences, after the pre-pass).
- Fenced blocks (protected whole; the legend lines cover their ids): V1:214-233, V1:295-318, V1:323-340, V1:389-399, V1:504-520, V1:2544-2555, V1:2886-2914, V1:2918-2942.
- Exception: the M-25 correction at V1:305 edits a fence line on purpose (step 4, not the id pass).

## 7. Spot check (20 replacements)

| Type | V1 line | Before | After | Context |
|---|---|---|---|---|
| DOC- | 583 | `DOC-20` | `R1-DOC-20` | estated as doc contradictions DOC-20, DOC-63, DOC-64 and DOC-65 in |
| INV- | 1172 | `INV-013` | `R1-INV-013` | ays open \| winner A (partial: INV-013 and INV-009 unaddressed, 4 di |
| SC- | 526 | `SC-1` | `R1-SC-1` | \| SC-1 \| Every consumer's findings v |
| C-nnn | 1383 | `C-001` | `R1-C-001` | nresolved diff points: S-007, C-001, C-006, X-003. Open decisions |
| debate row Cnn-nn | 2636 | `C13-01` | `R1-C13-01` | \| C13-01 Probe totals, gate result and |
| step Mn-nn | 539 | `M1-04` | `R1-M1-04` | the `coverage` field built in M1-04 and the per-mode rule built i |
| named gate | 3680 | `G-all` | `R1-G-all` | -43); gates R1-G1..R1-G11 and G-all in 8.3 \| |
| research file Rnn | 127 | `R04` | `R1-R04` | and model routing can change (R04 §7, GQ G-33). |
| inventory V-nnn | 2792 | `V-102` | `R1-V-102` | ort's earlier "absent" claim (V-102, V-407) is corrected in place |
| web file W0n | 3148 | `W03` | `R1-W03` | r from every scored reviewer (W03 recommendation 4) \| |
| hypothesis H-A | 165 | `H-A` | `R1-H-A` | \| T2 versus T1 recall (H-A) \| not measured \| pilot desig |
| CI-n | 2117 | `CI-1` | `R1-CI-1` | it decisive (Conditional item CI-1, not committed scope, because |
| decision D-n | 1183 | `D-1` | `R1-D-1` | f two as owner-gated Decision D-1; Phase 1 (flag advisory) cond |
| ENS- | 537 | `ENS-3` | `R1-ENS-3` |  `executor_model_class` while ENS-3 stays unwired), so the other  |
| exposure Xn | 536 | `X3` | `R1-X3` | `05` section 4; `research/10` X3; external context below \| |
| question Q-nn | 531 | `Q-05` | `R1-Q-05` | allowance is unchosen (owner: Q-05, to be fixed by the replay in |
| range | 539 | `X1-X14` | `R1-X1..R1-X14` | range pre-pass |
| GQ C- token | 142 | `GQ C-02` | `GQ R1-CLS-02` | closed-item rename |
| Closed item C- row | 3712 | `Closed item C-01` | `Closed item R1-CLS-01` | closed-item rename (inventory row) |
| closed list row | 4266 | `C-01` | `R1-CLS-01` | closed-item rename (9.3 list) |

## 8. Lines dropped, moved or excluded

| V1 line | Change | Why | Text (start) |
|---|---|---|---|
| 3829 | M-16 | ordering content (`**Dependencies:**` line of track M1), M-16 (1) | `**Dependencies:** none outside this track for M1-01 to M1-06; M1-07 and M1-08 depend on th` |
| 3830 | M-16 | moved: carried only in 8.6 (M-18), track M1 rule | `**Persisted formats and rollback (applies to every M1 step; [proposed] rule, not in code).` |
| 3860 | M-16 | ordering content (`**Dependencies:**` line of track M2), M-16 (1) | `**Dependencies:** M1-02, M1-06, M1-09, M1-10, M1-11 and M1-12 for the shared pieces; the S` |
| 3861 | M-16 | moved: carried only in 8.6 (M-18), track M2 rule | `**Rollback (M2; [proposed] rule).** Contract 1.8.0 stays byte-identical in every M2 step e` |
| 3879 | M-16 | ordering content (`**Dependencies:**` line of track M3), M-16 (1) | `**Dependencies:** M1-01, M1-09, M1-10, M1-11, M1-15 and M1-16 for the shared pieces; owner` |
| 3880 | M-16 | moved: carried only in 8.6 (M-18), track M3 rule | `**Rollback (M3; [proposed] rule).** M3-03 to M3-06 change the post-gate engine only and ke` |
| 3897 | M-16 | ordering content (`**Dependencies:**` line of track M4), M-16 (1) | `**Dependencies:** core: M1-01 to M1-06 and M1-09 (the open registry, location union, id gr` |
| 3898 | M-16 | moved: carried only in 8.6 (M-18), track M4 rule | `**Rollback (M4; [proposed] rule).** Adding a lens entry or a thin module is additive, so a` |
| 4115 | M-20 | PR-process checklist item dropped (M-20; PR plan out of scope) | `- [ ] Before any PR: git remote get-url origin prints the IronbellyOrg/IronClaude URL,` |
| 4057 | M-19 | heading replaced by `### 8.7 ...` (tagged Variant 1 (modified)) | `### 8.4 Branch-structure options` |
| 4062-4069 | M-19 | outside the range: layout table A-E is a branch plan (U-099 exemption, M-23) | table |
| 579, 783, 1154, 2808, 4124, 4388 | M-05, M-07, M-09, M-11, M-21, M-22 | V1 H2 lines outside the ranges, replaced by the new `###` headings | `## n.` |
| 4120 (clause) | M-20 | "and mark the steps that wait on each" removed (ordering) | see section 10 |

Blank lines: 10 blank V1 lines were not written because the line before was already blank (range starts after a new lead, double blanks at V1:781-782, 4121-4122 and the like): M05:V1:580, M07:V1:784, M07:V1:1153, M09:V1:1155, M09:V1:2807, M11:V1:2809, M19:V1:4058, M20:V1:4122, M21:V1:4125, M22:V1:4389. No text line is affected.

## 9. Step-status assignment (M-16, R25-INV-027)

Counts: {'CONFLICTS': 13, 'PARTLY COMPATIBLE': 14, 'COMPATIBLE': 21} (asserted 13 / 14 / 21; 48 distinct step ids M1-01..M1-22, M2-01..M2-10, M3-01..M3-09, M4-01..M4-07).

| Step | V1 line | Status | Cell text |
|---|---|---|---|
| R1-M1-01 | 3834 | CONFLICTS | CONFLICTS: Carried as the content of run 1's alternative; conflicts with run 2 outcome C-01; not plan input until re-adjudicated |
| R1-M1-02 | 3835 | PARTLY COMPATIBLE | PARTLY COMPATIBLE (R25-INV-027): re-adjudicate before use as plan input |
| R1-M1-03 | 3836 | COMPATIBLE | COMPATIBLE (R25-INV-027) |
| R1-M1-04 | 3837 | PARTLY COMPATIBLE | PARTLY COMPATIBLE (R25-INV-027): re-adjudicate before use as plan input |
| R1-M1-05 | 3838 | CONFLICTS | CONFLICTS: Carried as the content of run 1's alternative; conflicts with run 2 outcome C-10; not plan input until re-adjudicated |
| R1-M1-06 | 3839 | CONFLICTS | CONFLICTS: Carried as the content of run 1's alternative; conflicts with run 2 outcome C-01; not plan input until re-adjudicated |
| R1-M1-07 | 3840 | PARTLY COMPATIBLE | PARTLY COMPATIBLE (R25-INV-027): re-adjudicate before use as plan input |
| R1-M1-08 | 3841 | CONFLICTS | CONFLICTS: Carried as the content of run 1's alternative; conflicts with run 2 outcome C-02/C-03; not plan input until re-adjudicated |
| R1-M1-09 | 3842 | PARTLY COMPATIBLE | PARTLY COMPATIBLE (R25-INV-027): re-adjudicate before use as plan input |
| R1-M1-10 | 3843 | PARTLY COMPATIBLE | PARTLY COMPATIBLE (R25-INV-027): re-adjudicate before use as plan input |
| R1-M1-11 | 3844 | COMPATIBLE | COMPATIBLE (R25-INV-027) |
| R1-M1-12 | 3845 | CONFLICTS | CONFLICTS: Carried as the content of run 1's alternative; conflicts with run 2 outcome C-08; not plan input until re-adjudicated |
| R1-M1-13 | 3846 | CONFLICTS | CONFLICTS: Carried as the content of run 1's alternative; conflicts with run 2 outcome C-08; not plan input until re-adjudicated |
| R1-M1-14 | 3847 | COMPATIBLE | COMPATIBLE (R25-INV-027) |
| R1-M1-15 | 3848 | COMPATIBLE | COMPATIBLE (R25-INV-027) |
| R1-M1-16 | 3849 | PARTLY COMPATIBLE | PARTLY COMPATIBLE (R25-INV-027): re-adjudicate before use as plan input |
| R1-M1-17 | 3850 | PARTLY COMPATIBLE | PARTLY COMPATIBLE (R25-INV-027): re-adjudicate before use as plan input |
| R1-M1-18 | 3851 | COMPATIBLE | COMPATIBLE (R25-INV-027) |
| R1-M1-19 | 3852 | COMPATIBLE | COMPATIBLE (R25-INV-027) |
| R1-M1-20 | 3853 | COMPATIBLE | COMPATIBLE (R25-INV-027) |
| R1-M1-21 | 3854 | CONFLICTS | CONFLICTS: Carried as the content of run 1's alternative; conflicts with run 2 outcome X-14; not plan input until re-adjudicated |
| R1-M1-22 | 3855 | COMPATIBLE | COMPATIBLE (R25-INV-027) |
| R1-M2-01 | 3865 | COMPATIBLE | COMPATIBLE (R25-INV-027) |
| R1-M2-02 | 3866 | PARTLY COMPATIBLE | PARTLY COMPATIBLE (R25-INV-027): re-adjudicate before use as plan input |
| R1-M2-03 | 3867 | COMPATIBLE | COMPATIBLE (R25-INV-027) |
| R1-M2-04 | 3868 | PARTLY COMPATIBLE | PARTLY COMPATIBLE (R25-INV-027): re-adjudicate before use as plan input |
| R1-M2-05 | 3869 | COMPATIBLE | COMPATIBLE (R25-INV-027) |
| R1-M2-06 | 3870 | COMPATIBLE | COMPATIBLE (R25-INV-027) |
| R1-M2-07 | 3871 | COMPATIBLE | COMPATIBLE (R25-INV-027) |
| R1-M2-08 | 3872 | PARTLY COMPATIBLE | PARTLY COMPATIBLE (R25-INV-027): re-adjudicate before use as plan input |
| R1-M2-09 | 3873 | COMPATIBLE | COMPATIBLE (R25-INV-027) |
| R1-M2-10 | 3874 | PARTLY COMPATIBLE | PARTLY COMPATIBLE (R25-INV-027): re-adjudicate before use as plan input |
| R1-M3-01 | 3884 | PARTLY COMPATIBLE | PARTLY COMPATIBLE (R25-INV-027): re-adjudicate before use as plan input |
| R1-M3-02 | 3885 | CONFLICTS | CONFLICTS: Carried as the content of run 1's alternative; conflicts with run 2 outcome C24; not plan input until re-adjudicated |
| R1-M3-03 | 3886 | COMPATIBLE | COMPATIBLE (R25-INV-027) |
| R1-M3-04 | 3887 | COMPATIBLE | COMPATIBLE (R25-INV-027) |
| R1-M3-05 | 3888 | COMPATIBLE | COMPATIBLE (R25-INV-027) |
| R1-M3-06 | 3889 | COMPATIBLE | COMPATIBLE (R25-INV-027) |
| R1-M3-07 | 3890 | COMPATIBLE | COMPATIBLE (R25-INV-027) |
| R1-M3-08 | 3891 | COMPATIBLE | COMPATIBLE (R25-INV-027) |
| R1-M3-09 | 3892 | COMPATIBLE | COMPATIBLE (R25-INV-027) |
| R1-M4-01 | 3902 | CONFLICTS | CONFLICTS: Carried as the content of run 1's alternative; conflicts with run 2's adopted design (R25-INV-027 names no outcome id: the step edits `fsm.py`); not plan input until re-adjudicated |
| R1-M4-02 | 3903 | PARTLY COMPATIBLE | PARTLY COMPATIBLE (R25-INV-027): re-adjudicate before use as plan input |
| R1-M4-03 | 3904 | CONFLICTS | CONFLICTS: Carried as the content of run 1's alternative; conflicts with run 2's adopted design (R25-INV-027 names no outcome id: the step edits `severity_router.py`); not plan input until re-adjudicated |
| R1-M4-04 | 3905 | CONFLICTS | CONFLICTS: Carried as the content of run 1's alternative; conflicts with run 2 outcome C-10/C23; not plan input until re-adjudicated |
| R1-M4-05 | 3906 | CONFLICTS | CONFLICTS: Carried as the content of run 1's alternative; conflicts with run 2 outcome C-11; not plan input until re-adjudicated |
| R1-M4-06 | 3907 | PARTLY COMPATIBLE | PARTLY COMPATIBLE (R25-INV-027): re-adjudicate before use as plan input |
| R1-M4-07 | 3908 | CONFLICTS | CONFLICTS: Carried as the content of run 1's alternative; conflicts with run 2 outcome C-11; not plan input until re-adjudicated |

## 10. Corrections and per-change edits applied (before / after)

| V1 line | Block | Change | Before | After | Note |
|---|---|---|---|---|---|
| 133 | M-03 | M-25 | is three commits ahead (9874d63fb, c2e3347d3, 792cf8c52), and | is three commits ahead (9874d63fb, c2e3347d3, 792cf8c52) at the time of run 1; HEAD `ad8f57560` is now 5 commits past merge-base `d2d8a2d16`, and | stale 'three commits ahead' (checked: `git rev-list --count d2d8a2d16..HEAD` = 5, HEAD = ad8f57560, merge-base = d2d8a2d16) |
| 201 | M-03 | M-25 | audit D names 3 plus a merge that lost two blocking findings | audit D names 3 verdict flips (the third is the merge that lost two blocking findings, F1+F2) | verdict flips wording (audit D summary) |
| 204 | M-03 | M-25 | timed out 3 of 3 slots | timed out 3 of 4 runs | Qwen3.8-max '3 of 3 slots' corrected to '3 of 4 runs' (checked: `git show 4a22d742:.../combos/SPEC.md` line 3 'on 3 of 4 runs') |
| 305 | M-03 | M-25 | OR refs intersect | OR (refs intersect or both refs empty) | same_defect both-empty-refs branch (checked: `findings.py:367-379`, `if ra & rb or (not ra and not rb)`); line is inside a fence, tag on caption V1:319 |
| 381 | M-03 | M-25 | has 37 files and 353 tests | has 38 files and 353 tests | 37 corrected to 38 reflect test files (V1:381 only; checked by fault-finder row 6) |
| 410 | M-03 | M-25 (M-24 item 7) | 43 call sites in 11 skill files | 43 call sites in 11 skill files [unit not stated by run 1 and not reproducible by grep: `grep -rEn 'subagent_type: *"?rf-' src/superclaude/skills` gives 52 lines in 11 files, 44 of them in 8 `SKILL.md` files; Appendix E] | 43 call sites unit note (checked: 52 lines, 11 files, 44 in 8 SKILL.md) |
| 616 | M-05 | M-25 (M-24 item 7) | 43 spawning call sites in 11 skill files | 43 spawning call sites in 11 skill files [unit not stated by run 1 and not reproducible by grep: `grep -rEn 'subagent_type: *"?rf-' src/superclaude/skills` gives 52 lines in 11 files, 44 of them in 8 `SKILL.md` files; Appendix E] | 43 call sites unit note (checked: 52 lines, 11 files, 44 in 8 SKILL.md) |
| 624 | M-05 | M-25 (M-24 item 7) | 43 spawning call sites in 11 skill files | 43 spawning call sites in 11 skill files [unit not stated by run 1 and not reproducible by grep: `grep -rEn 'subagent_type: *"?rf-' src/superclaude/skills` gives 52 lines in 11 files, 44 of them in 8 `SKILL.md` files; Appendix E] | 43 call sites unit note (checked: 52 lines, 11 files, 44 in 8 SKILL.md) |
| 716 | M-05 | M-25 (M-24 item 7) | 43 call sites | 43 call sites [unit not stated by run 1 and not reproducible by grep: `grep -rEn 'subagent_type: *"?rf-' src/superclaude/skills` gives 52 lines in 11 files, 44 of them in 8 `SKILL.md` files; Appendix E] | 43 call sites unit note (checked: 52 lines, 11 files, 44 in 8 SKILL.md) |
| 2332 | M-09 | M-25 (M-24 item 5) | (or `claude -p --allowedTools`) | (or `claude -p` with `--tools <read-only set>` or `--restricted`, see the correction below the recommended resolution) | read-only mechanism |
| 2443 | M-09 | M-25 (M-24 item 7) | 43 rf-* spawning call sites | 43 rf-* spawning call sites [unit not stated by run 1 and not reproducible by grep: `grep -rEn 'subagent_type: *"?rf-' src/superclaude/skills` gives 52 lines in 11 files, 44 of them in 8 `SKILL.md` files; Appendix E] | 43 call sites unit note (checked: 52 lines, 11 files, 44 in 8 SKILL.md) |
| 2976 | M-11 | M-25 (M-24 item 7) | 43 spawning call sites in 11 skill files | 43 spawning call sites in 11 skill files [unit not stated by run 1 and not reproducible by grep: `grep -rEn 'subagent_type: *"?rf-' src/superclaude/skills` gives 52 lines in 11 files, 44 of them in 8 `SKILL.md` files; Appendix E] | 43 call sites unit note (checked: 52 lines, 11 files, 44 in 8 SKILL.md) |
| 3567 | M-14 | M-25 (M-24 item 7) | 43 spawning call sites in 11 skill files | 43 spawning call sites in 11 skill files [unit not stated by run 1 and not reproducible by grep: `grep -rEn 'subagent_type: *"?rf-' src/superclaude/skills` gives 52 lines in 11 files, 44 of them in 8 `SKILL.md` files; Appendix E] | 43 call sites unit note (checked: 52 lines, 11 files, 44 in 8 SKILL.md) |
| 3790 | M-14 | M-25 (M-24 item 7) | 43 call sites in 11 skill files | 43 call sites in 11 skill files [unit not stated by run 1 and not reproducible by grep: `grep -rEn 'subagent_type: *"?rf-' src/superclaude/skills` gives 52 lines in 11 files, 44 of them in 8 `SKILL.md` files; Appendix E] | 43 call sites unit note (checked: 52 lines, 11 files, 44 in 8 SKILL.md) |
| 4038 | M-17 | M-17 | and `:468-472` (final `verdict:` line) | and `:468-472` (final `verdict:` line) [conditional on run 1's verdict design, which is not adopted; these two pins belong on the rewrite list of run 2's C18 (R25-INV-026)] | R1-G2 must-not-change pins marked conditional |
| 4061 | M-19 | M-19 / M-25 | is 3 commits ahead of `origin/master` touching only | is 5 commits past merge-base `d2d8a2d16` (`origin/master` `d4d1662a8` is 3 commits past the merge-base), touching only | stale '3 commits ahead' (checked: `git rev-list --count` d2d8a2d16..HEAD = 5, d2d8a2d16..origin/master = 3; `git diff --stat d2d8a2d16 HEAD -- src tests scripts` = SKILL.md, refs/reviewer-spec.md, two reflect tests) |
| 4092 | M-20 | M-25 (M-24 item 7) | 43 call sites in 11 skill files | 43 call sites in 11 skill files [unit not stated by run 1 and not reproducible by grep: `grep -rEn 'subagent_type: *"?rf-' src/superclaude/skills` gives 52 lines in 11 files, 44 of them in 8 `SKILL.md` files; Appendix E] | 43 call sites unit note (checked: 52 lines, 11 files, 44 in 8 SKILL.md) |
| 4116 | M-20 | M-20 | Confirm the chosen branch layout of 8.4 does not create | Confirm the branch names (see 8.7 constraint) does not create | 'the chosen branch layout of 8.4' replaced by 'the branch names (see 8.7 constraint)' (text as the plan gives it) |
| 4120 | M-20 | M-20 |  and mark the steps that wait on each | (removed) | ordering clause dropped |
| 4348 | M-21 | M-25 (M-24 item 7) | 43 call sites | 43 call sites [unit not stated by run 1 and not reproducible by grep: `grep -rEn 'subagent_type: *"?rf-' src/superclaude/skills` gives 52 lines in 11 files, 44 of them in 8 `SKILL.md` files; Appendix E] | 43 call sites unit note (checked: 52 lines, 11 files, 44 in 8 SKILL.md) |
| 319 | M-03 | M-25 | caption | caption + `[Correction M-25: the `findings.cluster` line of the diagram now names the both-empty-refs branch of `same_defect` (`findings.py:367-379`).]` | the fence line V1:305 cannot carry an HTML tag |
| 2381 | M-09 | M-25 (M-24 item 5) | - | new paragraph after the line: the read-only correction | flag text per fault-finder row 27 |

Not corrected (logged): V1:3843 (R1-M1-10) and V1:3855 (R1-M1-22) name `--allowedTools` inside Details cells of 8.4, which M-16 forbids editing; V1:4170 (R1-Q-35) names it as an untested open question, not as a working restriction. V1:2347 is the `--disallowedTools` deny list (Option B), not an allowlist claim. The calibrator 5-vs-6 statement and run 1's "16 of 20 DECIDED-BY-EVIDENCE" stay as run 1 states them (M-25). V1:705 (37 attributed to research/12) is unchanged (M-25).

## 11. New text inserted

Every block starts with the provenance comment, the new `###` heading and the lead the plan prescribes (each lead line tagged `<!-- Source: new (lead per Change #M-nn) -->`). Other inserted lines:

- M-03, after V1:129: new line inserted after V1 line: In this merged copy, these ids carry the prefix `R1-` (Merge Notes, id rule). <!-- Source: new (legend line, rule 3) -->
- M-04, after V1:492: new line inserted after V1 line: In this merged copy, these ids carry the prefix `R1-` (Merge Notes, id rule). <!-- Source: new (legend line, rule 3) -->
- M-09, after V1:2381: new line inserted after V1 line: **Correction (M-24 item 5; R25-INV-006, R25-INV-007).** Where this block names `--allowedTools` as the restriction, the mechanism is `--tools <read-only set>` o
- M-14, after V1:3120: M-15 insertion marker (HTML comment), directly before the inventory table header: 
- M-16, after V1:3912: new line inserted after V1 line: This gap-coverage table keys on run 1 step ids (R1-M1-01 and so on), so each step it names carries the status given in the first column of the step tables above
- M-19, after V1:4059: new line inserted after V1 line: **The constraint in both reports and for the owner's prefix.** Both reports state it: `feat/review-panel` and `feat/review-panel/<name>` cannot both exist, in e
- M-21, after V1:4126: new line inserted after V1 line: In this merged copy, these ids carry the prefix `R1-` (Merge Notes, id rule). <!-- Source: new (legend line, rule 3) -->
- M-21, after V1:4126: new line inserted after V1 line: In this block `R1-Gn` means gap row n and `R1-C1` to `R1-C3` mean closure effort (V1:4126); closed items carry `R1-CLS-nn`. <!-- Source: new (9.11 id note, rule
- M-09: M-08 insertion marker (HTML comment) directly after the `### 6.13` heading, before the head note (plan M-08 Target: first block inside 6.13).
- M-18: the R25-INV-003 correction paragraph and the two versions as a list (text of plan M-18).

Heading demotion (M-27): 167 headings; `###` -> `####` and `####` -> `#####`, with `R1 ` before a heading that starts with a run 1 section number (for example `#### R1 2.1 E1: ...`, `##### R1 5.1.1 ...`, `#### R1 6.D ...`). Headings that start with an id or a word are demoted without `R1 ` (for example `#### R1-C-01: ...` after the id pass, `##### Option A: ...`, `##### Track R1-M1: ...`, `#### Codebase Research`). No V1 H2 line is carried.

## 12. Plan points not done, or done with a choice

1. **V1:3736 closed-item tokens**: renamed as an extra line pin (section 3); the plan's count of 103 is kept for its own enumeration. Revert by removing `EXTRA_PINS`.
2. **R1-M4-01 and R1-M4-03 conflict ids**: plan M-16 and R25-INV-027 give no run 2 outcome id for these two CONFLICTS rows (only "edits `fsm.py`" / "edits `severity_router.py`"). The cell names no id and says so instead of inventing one.
3. **M-06 "see M-20"**: the plan says the track names refer to "see M-20"; the steps of R1-M1..R1-M4 are in 8.4 (M-16), so the lead points at 8.4. Check whether M-20 was meant.
4. **M-17 "add those two pins to the rewrite list of V2 C18"**: that list is base text (run 2 C18), outside this executor's scope; the R1 block and its lead say the pins belong there (R25-INV-026). The base executor must add them to C18.
5. **M-20 V1:4116 text**: the plan's replacement gives "Confirm the branch names (see 8.7 constraint) does not create ..."; kept exactly as the plan words it (grammar "does" not changed).
6. **M-19 / M-20 residual references to the dropped layouts**: V1:4061 ("layouts C and D revert ...", "This section states layouts and trade-offs only") and V1:4086 (risk mitigation "8.4 layout choice") still mention run 1's layouts; the plan carries them with only the commit-count update, so they are unchanged.
7. **M-15 and M-08 tables**: not written (other executors); HTML-comment insertion markers are placed in `M14-sec8-inventory.md` (immediately before the inventory table header) and `M09-sec6.md` (after the heading).
8. **Legend lines**: added only under the three legends rule 3 names (V1:108-129, 483-492, 4126). Other carried key tables (V1:2810-2817 Section 7 conventions, V1:3109-3116 inventory abbreviations) get none, per the plan.
9. **M-19 ref check**: `git for-each-ref refs/heads refs/remotes` shows no `feat_review-panel*` or `feat/review-panel*` ref (only `ironbelly/eval-tasklist-review-panel`); `git ls-remote origin` was not run (network), so "on origin" rests on fault-finder row 31.
10. **Lead of M-22 (10.A)**: the plan prescribes none; none added. M-21 (9.11) has no lead beyond the kept source key, the legend line and the id note.

Read-only checks run for this log (no writes outside the outputs): `git rev-parse HEAD` (ad8f57560), `git merge-base HEAD origin/master` (d2d8a2d16), `git rev-list --count d2d8a2d16..HEAD` (5) and `..origin/master` (3), `git rev-parse --short origin/master` (d4d1662a8), `git diff --stat d2d8a2d16 HEAD -- src tests scripts` (4 files: reflect SKILL.md, refs/reviewer-spec.md, two reflect tests), `git show 4a22d742...:.dev/eval-workspaces/tasklist-review-panel/20261111-a1/combos/SPEC.md` (line 3: Qwen3.8-max timed out "on 3 of 4 runs"), `src/superclaude/cli/review/findings.py:367-379` (`same_defect`), `src/superclaude/cli/review/ledger.py:363-372` (`verdict()` returns `last["verdict"]`), `src/superclaude/cli/pipeline/process.py:140-160` (`reviewer_profile`), `grep -rEn 'subagent_type: *"?rf-' src/superclaude/skills` (52 lines, 11 files, 44 lines in 8 SKILL.md), `git for-each-ref` (section 12 item 9), V2:1102 and V2:4433 (read).

## 13. Final self-check (script)

| Block | (a) no V1 `## ` line | (b) no `Closed item R1-C-` / `GQ:R1-C-` / `GQ R1-C-` | (c) no deleted `**Dependencies:**` text |
|---|---|---|---|
| `M03-sec2.md` | PASS | PASS | PASS |
| `M04-sec3.md` | PASS | PASS | PASS |
| `M05-sec4-gaprows.md` | PASS | PASS | PASS |
| `M06-sec4-contradictions.md` | PASS | PASS | PASS |
| `M07-sec5.md` | PASS | PASS | PASS |
| `M09-sec6.md` | PASS | PASS | PASS |
| `M11-sec7.md` | PASS | PASS | PASS |
| `M14-sec8-inventory.md` | PASS | PASS | PASS |
| `M16-sec8-migration.md` | PASS | PASS | PASS |
| `M17-sec8-gates.md` | PASS | PASS | PASS |
| `M18-sec8-persisted.md` | PASS | PASS | PASS |
| `M19-sec8-branch.md` | PASS | PASS | PASS |
| `M20-sec8-risk.md` | PASS | PASS | PASS |
| `M21-sec9.md` | PASS | PASS | PASS |
| `M22-sec10.md` | PASS | PASS | PASS |

(d) all 48 step ids carry a status cell in `M16-sec8-migration.md`: PASS.
