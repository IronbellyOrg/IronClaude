# Round 3 final arguments: V5 (sonnet, performance lens)

Citations: `V<n>:<line>` = `variant-<n>-original.md`; `R2-V5:<line>` = `round2-V5.md`; `R3-V<n>` = `round3-V<n>.md`; `INV-0nn` = `../invariant-probe.md`; `AG:<line>` = `round3-agenda.md`; `RR:<line>` = `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/tools/run-reviewer.sh`. I read R3-V1 to R3-V4 before writing. Every number below was recomputed.

## Final position

V4 stays the base and the slate stays F1, F4, F3, F6, F7. I take the same texts as the other four advocates: INV-001 and INV-003 = R3-V1, INV-005 = R3-V2, the other five ACCEPT. I add no new MODIFY text. The one defect in the shared text is a performance defect in my own Round 2 formula, and I concede it below. My lens adds three measured facts: k = 2 is the optimistic row, the common hang guard will bind in one sonnet cell, and the retry loop can double elapsed time in any arm.

## HIGH invariant resolutions

| INV | Verdict | Exact rule for the merged spec |
|---|---|---|
| INV-001 | MODIFY | **MODIFY = R3-V1.** I concede the 1.20 B term (R2-V5:77). Recomputed at B = 116 with turn and report 6.4 s: my min(1.20 B, 1.35 B - 12.8) = min(139.2, 143.8) = 139.2 s. INV-008's k = 2 plans an end of 116 + 2 + 2 x 2 x 6.4 = 143.6 s, so my signal would fire on the planned path and truncate luna's own isolated work in every typical run. The 1.20 B term binds only when T_report_p90 < 0.15 x 116 - 6.4 = 11.0 s, which is the regime I called likely. R3-V1's `PANEL_FINISH_AT = T0 + 1.35 B_f - turn_p90 - T_report_p90` gives 143.8 s, and the bound (143.8 + 12.8) is 156.6 s (+35.0%). Performance addendum: log `finish_would_fire` in A1 and A2 (R3-V2:33), because a signal that fires only in design arms is a hidden treatment. |
| INV-002 | ACCEPT | R3-V1:26 wording. One deadline T0 + 1.30 B_A1 covers resume or fallback, challenges and any H2 re-ask. A re-ask without one start plus one turn left is skipped. `reask_s` is logged in A1 and every arm. "Hard bound" means the phase-2 end only. |
| INV-003 | MODIFY | **MODIFY = R3-V1.** Recomputed: deadline 1.30 x 116 = 150.8 s; a launch at 116 leaves 34.8 s; n = floor(28.8/12.8) = 2 (end 116 + 6 + 25.6 = 147.6 s); for turn_p90 > 7.2 s, floor(28.8/14.4) = 2 only at exactly 7.2 and n = 1 above it. A fallback detected at 2 s: floor((32.8 - 16)/12.8) = 1 (end 118 + 16 + 12.8 = 146.8 s). Stream-json salvage is required because RR:48 writes `--output-format json` and RR:50 reads the one `result` object that exists only at exit. Cost note: stream-json with `--verbose` writes more output per run, but it is a local file write, not a model cost. |
| INV-004 | ACCEPT | Own-line Jaccard, ECHO on real-anchor slots, balanced online deal (R3-V2:20), alarm guard on own lines only. |
| INV-005 | MODIFY | **MODIFY = R3-V2.** Recomputed at r = c = 0: recipients (i + r) mod 2 = A, B, A, B; forms by (i + floor(i/2) + c) even = C, F, F, C. Luna A gets C, F and luna B gets F, C, so each luna sees both forms; R3-V1's alternation gives A: C, C and B: F, F, which confounds luna with form. Performance and power note: ember posts at most 2k cards at 3.2 s each, off the critical path. At k = 2 there are at most 12 x 3 x 4 = 144 cards (72 per form). At k = 1 there are 12 x 3 x 2 = 72 cards (36 per form) and each luna gets one card, so the contrast is across lunas, balanced by the seeded r and c. At k = 1 the form contrast is descriptive, and the spec must say so. |
| INV-006 | ACCEPT | R3-V1's (source, form, delivery point) criterion, with F3 injections naming a move only (R3-V2:22). F6 uses findings from finished peers, never telemetry. F2 differs from F7 in at most 1 of 3 and is not a replacement. |
| INV-007 | ACCEPT | = R3-V1:31 plus R3-V2:23. M2 and M4 get a listed signature or "unobservable". Luna injections are booked to the A2 static-kit share. F3's C is re-derived from ember rows only. |
| INV-008 | ACCEPT | = R3-V1:32 with k clamped at 0 (R3-V2:24 thresholds). Recomputed with hooks = 2 and turn 6.4: k = 2 needs T_report_p90 <= 0.35 B - 34. That is 6.6 s at B = 116, 1.0 s at designSpec's 100 (AG:13), 8.0 s at 120 and 8.7 s at 122. k >= 1 needs <= 0.35 B - 21.2: 19.4 s, 13.8 s, 20.8 s, 21.5 s. k >= 1 at all needs 0.35 B - 2 - 12.8 >= 12.8, so B >= 78.9 s (the probe's typical floor). For F6 (B = 273.7, turn 14): k = 2 needs <= 23.8 s, k >= 1 needs <= 51.8 s. Package medians are from runs without H; A1 carries H, so measured k can only rise. |

**Open points.**

- **k = 1 as the central row (V2, V3, V4) versus k = 2 (V1): I take k = 1.** k = 2 needs luna's output-heavy last turn at p90 to fit 6.6 s, about the mean turn of 6.4 s, and it is impossible on designSpec at the 100 s median. Both rows are planning values until Spike 4 publishes the per-package k. Planned ends at B = 116: k = 1 gives 116 + 2 + 12.8 = 130.8 s (+12.8%); k = 2 gives 143.6 s (+23.8%). F6: 303.7 s (+11.0%) and 331.7 s (+21.2%).
- **F3 injections name a move only: I agree.** Without it F3 and F6 share the form "move + Task" and differ in source only (1 of 3).
- **V4's two rules from RR: ACCEPT both, with one measured caveat.**
  - Retry loop (RR:61-64): attempt 2 re-runs the whole review, and `wall_s` is per attempt (RR:49). A failure at about B followed by a full retry gives about 2 B elapsed (100 + 116 = 216 s, +86%), regardless of design. `elapsed_s` sums attempts, `retry_s` is logged, and attempt 2 runs isolated (`retry_isolated`). Rows with a retry are reported in a separate column so that they do not hide a design effect.
  - Common hang guard, logged `hang_kill`, in A1 too: required for a fair elapsed comparison. Measured fit against AG:9-16 (max wall vs 1.5 x median): ember panels 123 vs 150, 171 vs 180, 155 vs 183 (never binds); haiku 305 vs 330, 285 vs 357, 297 vs 339 (never binds); sonnet DS 283 vs 388.5, AL 416 vs 453, **DE 440 vs 403.5, binds in 1 of 6 runs**. So the guard is symmetric but not free on the sonnet panel, and F6's SL2 arms must report `hang_kill` counts in both arms.

## MEDIUM invariants worth closing

- INV-009 to INV-012, INV-014, INV-018: adopt R3-V1:36-41.
- INV-015: sweeper timeout as a formula, PANEL_FINISH_AT - T0 - 2 x turn_p90 (R3-V4:49). Recomputed at planning values: 143.8 - 12.8 = 131.0 s after T0, instead of the absolute 85 s.
- INV-019 to INV-021: V2's decision table (R3-V2:30-32). Recomputed: with A1 at 1/12, 5/12 gives p = 0.077 and 6/12 gives 0.034 (agrees with R3-V2). The spec says plainly that the plan cannot detect the central H estimate 0.14/14 (R2-V5:20). Repairing the measurement does not create power.
- INV-013: an empty digest makes ECHO not applicable, not 0.

## Remaining disagreements

None. The k = 1 versus k = 2 label is a naming question that Spike 4's per-package k replaces.

## Final concessions

- R2-V5:77: the 1.20 B term. Dropped for R3-V1's 1.35 B form.
- R2-V5:35: "A5 vs A4 differs in message content only ... the cleanest possible test of SEED:47" was false (INV-005): sender session, content source, move type and targets all differ.
- R2-V5:51: "F1 is the only slot with a compliance-free hard bound" holds for the phase-2 end only, and only with the re-ask inside the deadline (INV-002, INV-022).
- R2-V5:46: n used the mean turn (INV-003); the p90 rule I applied to the finish time must apply to n as well.
- R2-V5:19: F1's input-token cost is a column in the S-004 table (resume replays about 16 turns of context).
- No Round 2 consensus winner changes.

## Final slate

| Slot | Family | Core | Grafts | Reason |
|---|---|---|---|---|
| 1 | F1 Between-phase cross-examination | V4-3 Axis-Flip Challenge | `contradiction` -> M7; gap card p = 1/3 booked to prompting; balanced anchor deal; per-attempt n with stream-json salvage; one phase-2 deadline incl. re-ask; V5-D5 HL2 shadow (+0%, worst +6.3%, no arm) | Only kill-enforced bound: phase-2 end <= 150.8 s (+30.0%). Luna B 147.6 s at n = 2 or 134.8 s at n = 1. C 0.06-0.63 |
| 2 | F4 Searcher-to-reader fact relay | V4-2 Idle-Shift Sweeper | Locators by balanced deal; harvest; witness kind; first-hand rule; k per INV-008; sweeper timeout formula; common hang guard | Cheap I7 path in ember's idle time. 130.8 s (k = 1) / 143.6 s (k = 2); signal bound 156.6 s; 174 s = breach |
| 3 | F3 Content-free coverage steering | V4-1 Move Radar | Observable signatures; move-only payload; luna kit booked to A2; skip rule; leak check; k | Telemetry timing versus static kit; C from ember rows only, may be near 0 |
| 4 | F6 Steering a running strong model | V4-5 Coverage Deflection on SL2 | Finished peers' (Task, category); uncovered-Task requests; no counts, telemetry or SendMessage; sonnet k | Runs only if sonnet T_report_p90 <= 51.8 s. 303.7 / 331.7 s; bound 369.5 s; ceiling 410.6 s |
| 5 | F7 Directed challenge | V4-4 Flag-and-Adjudicate, EL2, one way | Enum-only forms with R3-V2 online deal; cap 2k; snapshot; first-hand rule; overlap alarm stops the arm | Only slot that answers SEED:47, within one arm; timing as F4 |

Proposed base document: V4

## Per-point positions

| Point | Winner | Reason |
|---|---|---|
| S-001 | V4 | Per-design requirements plus a runbook |
| S-002 | V4 | Kill switch, baked settings, timing tables |
| S-003 | V2 | Gate funnel makes the H/C split structural |
| S-004 | V5 | Net collaboration, static-kit row, input tokens for resume |
| S-005 | V4 | One ID scheme with verification column |
| S-006 | V5 | Itemised unverified list, now incl. T_report_p90 |
| C-001 | V1 | Searcher/reader complementarity |
| C-002 | V5 | T2a/T2b decides routes to B1/B2/I4 |
| C-003 | V1 | Truncate, validate, re-ask inside the deadline |
| C-004 | V4 | Best-style column used by routing |
| C-005 | V4 | 12-200-character anchors plus V2's rules |
| C-006 | V4 | Process exit for phases; fail-closed snapshot mid-run |
| C-007 | V4 | Relative alarm on own lines |
| C-008 | V4 | Per-issue chains |
| C-009 | V5 | Three shares; C and H never summed |
| C-010 | V2 | Fresh A0, catalogue arm, A6 |
| C-011 | V2 | One reach endpoint, final-look Fisher, vs observed A1 |
| C-012 | V1 | Seed baseline per design |
| C-013 | V1 | Measured-reservation finish signal plus R-24 audit |
| X-001 | V5 | Bottom-up H 0.03-0.34 |
| X-002 | V1 | 0 on /14; control correction only |
| X-003 | V1 | GT6 = I1 |
| X-004 | V5 | HL2 shadow schedule +0% |
| X-005 | V1 | The slowest luna sets B |
| X-006 | V4 | One block, P2-F ids, origin stripped |
| X-007 | V2 | No free text; enum-only F7 cards |
| X-008 | V1 | Grading and judge held constant |
| X-009 | V1 | Truncate, validate, re-ask |
| X-010 | V5 | The kit may win; A2 is the comparator |
| X-011 | V5 | Anchor routes to B1/B2/I4 need the gap card |
| X-012 | V1 | Both scales defined most precisely |
| X-013 | V2 | 4/6 vs 0/6 = 15/495 = 0.030 |
| A-001 | V1 | REQ-S3 tests the act, incl. "finish now" |
| A-002 | V5 | Prices the kit's time |
| A-003 | V2 | Random labels plus sealed-report judging |
| A-004 | V4 | States the H-C interaction |
| A-005 | V5 | Per-package medians, not /3 |
| A-006 | V2 | Decoys via the gap card |
| A-007 | V4 | Spike, bounded fallback, `resume_fallback` metric |
| A-008 | V4 | Helpers write only under `$BOARD` |
| A-009 | V2 | Confirmation on two new packages |
| A-010 | V1 | States why EL2 is the base |
| A-011 | V5 | Cap gains against measured reach |
