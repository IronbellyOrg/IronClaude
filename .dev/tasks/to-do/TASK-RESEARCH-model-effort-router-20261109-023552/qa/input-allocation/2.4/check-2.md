# QA Report: 2.4 allocation page check (check-2)

Verifier: rf-qa, report-only, Tier1b (claude-gw-tier1b). Run run_c974cafd0eb6. Date 2026-11-13. Object: topic 2.4 section of `qa/local-source-allocation.md` v2 (lines 62-70, plus shared lines 1-28, 101-107). Revision: worktree HEAD 933cf3a4f. Final permitted review round for this gate.

VERDICT: FAIL

Blocking findings: 2. Minor notes: 4.

## Inputs read
- TASK lines 140-161 (procedure, 22 lines), read first. Producer spec for 2.4: TASK line 230 (read from "PRODUCER-ONLY" onward, truncated at 2600 chars).
- `qa/input-allocation/2.4/check-1.md` (50), `qa/input-bindings.md` (32; no 2.4 rows, zero consuming additions, valid), manifest v2 lines 1-30, 62-70, 101-107.
- Metadata only: `wc -l`, numbered single-line prints and def/decorator greps at every range edge. No source body reads.

## Cycle-1 regression check (a)
| Cycle-1 finding | v2 status |
|---|---|
| B1 F10 split inside `with_note` | FIXED: slice-1 1-451, slice-2 452-906; 451 blank, 452 `def with_note`. F10 union 451+455 = 906, no gap/overlap. (Caller-to-callee edge declaration still missing, see B2 below.) |
| B2 ranges cut test bodies | PARTLY FIXED: F14 1018-1180 now whole (1018 `def test_no_backup`, 1174 blank, 1175-1178 `test_compact...` whole, ends before decorator 1181); F14 1553 blank before 1554 def; F15 1441-1483 whole (1466 decorator and 1467 def restore test whole; 1483 is only the next decorator). NOT fixed for three ranges, see B1. |
| B3 no aspects | FIXED: every slice has an Aspect line plus an obligation map (line 70). Spec keywords all mapped; "replay" has a source-backed negative. |
| B4 no unique outputs | FIXED: `research/source-slices/2.4/slice-{1..5}.md` (heading line 62), five distinct paths. |
| N1 F15 3136-3305 exclusion | Addressed with a stated reason (orca naming/tab tests owned by 2.5). Not source-verified (no source reads). |

## Checks
| Check | Result |
|---|---|
| (a) cycle-1 blocking findings corrected | FAIL: B2 only partly corrected (B1 below); B1 boundary fixed but edge declaration missing (B2 below) |
| (b) line coverage, def/test-edge boundaries | FAIL (B1): F10 PASS; F14 1018-1180 PASS; F15 1441-1483 PASS; three ranges cut bodies |
| (c) spec obligation to slice aspect | PASS (line 70 maps all 11 keywords; negative for replay) |
| (d) charged total <=1000 | PASS with note M1 |
| (e) unique per-slice output paths | PASS |
| (f) check-before-source | PASS with note M2 |
| (g) counterpart/shared-edge declarations | FAIL (B2) |

(d) arithmetic recomputed: s1 451+40+344 = 835; s2 455+30+344 = 829; s3 (234+83)+20+344 = 681; s4 (163+140)+30+344 = 677; s5 (43+42)+20+344 = 449. Range lengths 922-1155=234, 748-830=83, 1018-1180=163, 1414-1553=140, 1441-1483=43, 3445-3486=42, all correct. Even if fixed context is 404 (M1), maximum is 895. wc -l: F10 906, F14 3399, F15 4823, F05 1111, F01 1975 all match the manifest.

## Blocking findings
B1. Three ranges still cut a function/test the manifest calls "whole":
- slice-5 F15 3445-3486 ends mid-body of `test_orca_auto_named_session_is_listed_once_the_session_hook_records_it`, which starts at 3474 and runs to 3493 (next def `test_orca_terminal_title_keeps_claude_recognisable` at 3494). Lines 3487-3493 are excluded; line 3489 is still inside the `_hook(...)` call. The manifest says "whole tests". Fix: 3445-3493 (49 lines; slice-5 becomes 112 + 344 = 456).
- slice-3 F05 748-830 ends inside the docstring of `shim_upstream_problem` (def 822, body continues to 846; `resolve` at 847). Fingerprint functions end at 800 and `shim_port` ends at 821. Fix: 748-821 (74) or 748-846 (99), both far under budget.
- slice-4 F14 1414-1553 starts after the `@pytest.mark.parametrize(` decorator and its model list at 1411-1413 (def is 1414), so the parametrize values for `test_no_time_limit_once_a_reply_starts` are cut. The same range is used as the declared overlap in 2.3-slice-5 (manifest line 58). Fix: start both at 1411.
These repeat the cycle-1 B2 class (round every range to whole definitions), which the manifest claims is done "throughout" (line 101).

B2. Check (g): no cross-slice caller-to-callee edges are declared for 2.4 slice-1 and slice-2. Slice-1 owns the callees `switch_reason` 393, `retry_after_seconds` 404, `cool_down` 419, `cooling_until` 426, `clock` 432, `plain_body` 436 and `_cooldowns` 94; slice-2 owns the callers `with_note`, `_FirstByteResponse` and the Handler failover path (`_forward_tier` 723, `_stream` 841). Line 103 lists declared edges for 2.1, 2.2, 2.3 and the F14 1414-1553 overlap, but nothing for 2.4 slice-1 to slice-2 (cycle-1 B1 explicitly asked for these entry/exit edges; only the boundary was moved). Procedure line 152 requires cross-slice call counterpart edges, and line 154 makes undeclared cross-boundary facts UNVERIFIED. Fix: add a declared-edge line (slice-1 callees used by slice-2 callers, with each side attributed as counterpart), naming at least `switch_reason`, `cool_down`, `plain_body`, `with_note` and `cooling_until`.

## Minor notes (do not fail)
M1. Fixed-context arithmetic: 344 is described as "trims role/template to a 100-line excerpt", but 22+70+180+32+100 = 404, not 344 (344 = 22+70+180+32+40, i.e. role dropped). Understates every 2.4 slice by 60; maximum becomes 895, still <=1000. Fix when editing.
M2. v2 dropped the explicit check-before-source ordering statement that v1 had at lines 111-113. Ordering is still required by procedure lines 150-152 and by this gate's position; restate it in the Registration section.
M3. Manifest text "label-with-transcript resume 1441-1448" mislabels: 1441 is the missing-transcript test, 1449-1465 is the saved-transcript resume test; the 1441-1483 range itself covers both.
M4. Slice-2 (Handler failover path) charges only scope-02 rows, not scope-03 (the proxy digest the spec names first); acceptable if the brief carries the rows.

## Self-Audit
Attempted disproof of FAIL: re-read each range edge by numbered line (F14 1016-1019, 1173-1181, 1411-1416, 1551-1556; F15 1439-1442, 1481-1486, 3443-3446, 3484-3490; F05 748, 780, 785, 801, 821-832; F01 922, 1155-1157; F10 451-452, 479-480) and listed def/decorator lines around F15 1436-1490 and 3440-3520. Each B1 cut was confirmed from the numbered edge lines; B2 was confirmed by searching the manifest for any 2.4 edge declaration (line 103 has none). Passing items were attacked the same way (arithmetic, wc -l, F10 union, output uniqueness). Confidence denominator: 7 checks (a-g) across 5 slices and 11 spec keywords; 4 of 7 pass.

Not verified: relevance of F15 3136-3305 and F14 outside the chosen ranges (no source reads allowed); whether the full producer prompt is exactly 180 lines.

Note on loop budget: this is the third review of this gate (cycle 1, fix, cycle 2). Per the review-loop rule, a FAIL here escalates to the user with the open blocking findings B1 and B2 above.
