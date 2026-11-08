| Status | Result |
|---|---|
| DONE | Verified disputed facts (a) to (d) against the live files. Final rebuttal and 22-row table are below. |
| NEXT | None. |

## Round 2 rebuttal, Variant 1

**Concessions.** My Round 1 had wrong line cites: `cycle.py:335-337` should be 1060-1062, and `:308` should be 693 and 1033. My header said "1 MEDIUM" when two rows were MEDIUM. I rated the skip sites Necessary LOW, which was wrong. I missed the late launch. I also did not read the register, tests or `spec-final.md` before arguing.

**(a) Crash exit 1 and the two added reasons.**
- Design line 722 requires a stderr fallback "used for a crash". Line 718 makes `line()` reject any name outside the table. So the design forced a name for the crash line, and it never gave one.
- `_EXIT_CRASH = 1` (`cli.py:35`) is Python's default for an uncaught exception. The task discloses the change (task 900, 905).
- AC-17 (design 890) is tested on normal outcomes. The crash path is not in it.
- Verdict: Necessary deviation LOW, plus Drift LOW because the design was never amended. It is not Regression. I withdraw my Round 1 MEDIUM, which was too high.

**(b) Root-guarded skips.**
- This does violate task line 188. The five sites (`test_record.py:739`, `test_cycle.py:735` and `:4694`, `test_cli.py:967` and `:1070`) are real, and the task graded them "minor" itself (task 908).
- The recorded runs (p8-g1, p8-g3, p9-g3) had 0 skipped, so the gate criterion was met. The skips only bite when the suite runs as root.
- Verdict: Drift MEDIUM, non-blocking. V2's "blocking" overstates it. V3's Regression is not warranted either, because no previously working behaviour broke.

**(c) V2's "Regression" labels.** Under the strict definition, none of X-001, X-002, X-010, C-013, C-017, C-026 or C-036 qualifies.
- X-010 is stale documentation, and the tests pin 59 names (`test_audit.py:215-219`).
- C-017 is only an implied conflict with the runbook, in a dangling-symlink corner case (setup 298, `record.py:421-431`).
- C-026 is a conflict inside the design itself: the 500-byte cap (design 218, 822) against the "anywhere" rule (634). It needs exit 0, a valid id, and the marker past byte 500.
- C-036 is reachable only through a hand-edited store.

I steelman V2 on C-013. The task did say "no skips", the skips are a clear drift, and V2 is right that they are more than cosmetic. I now agree with V2 on the category and disagree only on "blocking".

**(d) Late launch (X-007, C-014). My position changed.**
- `launch_allowed()` is checked at `cycle.py:1039`. Between 1048 and 1062 there is a git call, `mark_pending` and an fsync'd `_save()` (1060-1061), and no further cutoff check before `launcher.launch` at 1062.
- If the clock crosses 120 s during that window, a launch starts after the cutoff. That contradicts design 647 and the letter of AC-19.
- It is narrow. The save is a local fsync, the worst case is about 241 s of the 300 s budget, and at-most-once still holds.
- Verdict: Regression LOW, non-blocking. I now side with V3 on the label. V2's HIGH and blocking is too high. My Round 1 "advisory gap" was too low.
- Fix: snapshot `prev`, re-check the cutoff after `_save()`, then `_set(prev)`, `_save()`, and `raise _Skip("budget_exhausted")`. If the rollback save fails, the sweep turns the entry into `pending_orphan` with no launch. Add a slow-save test with a clock that passes 120 s inside `store.save`. Existing tests only cover 121 s and exactly 120 s (`test_cycle.py:1964`, `:1982`).

**New evidence on X-003.** `test_module_boundaries.py:20-22` records that `record` imports three functions and one type from `predicates`, where design 5.3 says "types only". The deviation is disclosed in the test. `valid_operation_id` stays the weakly disclosed piece.

**Other variants.** V3 is right that X-001 and X-002 also leave the design un-amended, and I now carry that as Drift LOW. V2 is right that the skips are Drift. I still disagree that either one is Regression.

## UPDATED POINT TABLE

"Changed" means changed since my Round 1. Evidence marked "not re-read" comes from the diff analysis only, and its confidence is capped.

| Point | Final classification | Backs | Conf | Evidence | Changed |
|---|---|---|---|---|---|
| X-001 | Necessary deviation LOW + Drift LOW (design not amended) | V1 category, V3 doc gap | 65% | `cli.py:35`, `122-129`; design 718, 722; task 905 | Yes (MEDIUM to LOW) |
| X-002 | Necessary deviation LOW | V3 | 70% | `audit.py:62-64`; `cycle.py:1134-1137`; `test_audit.py:215-219` | No |
| X-003 | Authorized LOW; `valid_operation_id` Necessary/Drift LOW | none | 60% | `test_module_boundaries.py:20-22`; `record.py:168-210`; design 239 | No |
| X-004 | Necessary deviation LOW + parity-test advisory gap | V3 | 60% | diff-analysis X-004 row (not re-read) | No |
| X-005 | Authorized expansion LOW | none | 75% | task 193 | No |
| X-006 | Drift MEDIUM, non-blocking | V2 category | 72% | skip sites above; task 188, 908 | Yes (Necessary LOW to Drift MEDIUM) |
| X-007 | Regression LOW, non-blocking | V3 | 62% | `cycle.py:1039`, `1048`, `1060-1062`; design 634, 647 | Yes (advisory gap to Regression LOW) |
| X-008 | Advisory correctness gap LOW | none | 50% | diff-analysis X-008 row (not re-read) | No |
| X-009 | Not a defect (second check exists) | none | 80% | `cycle.py:693`, `1033` | No |
| X-010 | Not a defect (stale doc, disclosed) | none | 75% | task 905; `test_audit.py:215-219` | No |
| C-014 | Regression LOW, non-blocking | V3 | 62% | same as X-007 | Yes |
| C-013 | Drift MEDIUM, non-blocking | V2 category | 72% | same as X-006 | Yes |
| C-016 | Advisory gap LOW (design-conformant) | none | 55% | not re-read | No |
| C-017 | Advisory gap LOW | V1, V3 | 65% | setup 298, 302; `record.py:421-431` | No |
| C-018 | Advisory gap LOW | none | 55% | not re-read | No |
| C-019 | Advisory gap, unverified | none | 50% | not re-read | No |
| C-024 | Advisory gap LOW-MEDIUM (reply shape unverified) | none | 60% | `launch.py:296-334` | No |
| C-026 | Advisory gap LOW | none | 65% | `launch.py:322`, `326-334`; design 218, 634, 822 | No |
| C-036 | Advisory gap LOW (near-unreachable) | none | 65% | `record.py:168-210` | No |
| C-037 | Advisory gap LOW | none | 60% | `cycle.py:1255-1290` | No |
| C-034 | Drift LOW (docs only); part (c) not a defect | none | 55% | `cli.py:164-182`; design 115, 726 | No |
| C-022 | Advisory gap LOW (fail-closed, spec-conformant) | none | 70% | `record.py:421-431`; setup 298 | No |

**Recommended action:** Treat X-007/C-014 as the only Regression, at LOW and non-blocking, and fix it with the re-check after `_save()` plus the slow-save test.
