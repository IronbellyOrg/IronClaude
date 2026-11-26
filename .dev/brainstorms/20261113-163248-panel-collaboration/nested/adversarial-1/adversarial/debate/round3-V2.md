# Round 3 final arguments: V2 (opus, analyzer lens)

Citations: `V<n>:<line>` = `variant-<n>-original.md`; `R2-V<n>:<line>` = `round2-V<n>.md`; `R3-V1` = `round3-V1.md`; `INV-0nn` = `../invariant-probe.md`; `AG` = `round3-agenda.md` (orchestrator's per-package table); `RR:<line>` = `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/tools/run-reviewer.sh`. I read R3-V1 before writing. Every number below was recomputed this round.

## Final position

V4 stays the base, and the slate stays F1, F4, F3, F6, F7. The probe is right on all eight HIGH items. My own Round 2 figures "worst 150.0 s", "worst = expected" and "A5 vs A4 answers SEED:47" do not survive it. I adopt R3-V1's MODIFY texts for INV-001 and INV-003 unchanged, because both rest on checkable facts: the probe's two rules conflict at its own planning values, and RR:48 shows `--output-format json`. I accept INV-002, -004, -006, -007 and -008.

I cannot adopt R3-V1's INV-005 text. Its card-assignment clause contradicts itself. As written, each luna receives two cards of the same form, so luna and form are fully confounded. My replacement keeps V1's enum-only finding form and fixes only the dealing rule.

One analyzer finding changes what the spec should call "expected". k = 2 needs luna's final-report turn at p90 to be no longer than 6.6 s. The gain rows should therefore be reported at k = 1 as the central case.

## HIGH invariant resolutions

| INV | Verdict | Exact rule for the merged spec |
|---|---|---|
| INV-001 | MODIFY | **MODIFY = R3-V1.** Evidence, recomputed: the probe's `min(1.20 B, 1.35 B - turn_p90 - T_report_p90)` at B = 116 with 6.4/6.4 gives min(139.2, 143.8) = 139.2 s. Its own INV-008 k = 2 plans an end of 116 + 2 + 25.6 = 143.6 s > 139.2, so the probe's "B + W <= PANEL_FINISH_AT" fails under its own rules. The 1.20 B term binds only when T_report_p90 < 0.15 B - turn_p90 = 17.4 - 6.4 = 11.0 s. Dropping it therefore changes nothing in the regime the probe itself calls likely ("output-heavy"). |
| INV-002 | ACCEPT | Probe text, worded as in R3-V1: one wall-clock deadline T0 + 1.30 B_A1 covers resume or fresh fallback, challenges and any H2 re-ask. A re-ask that cannot fit one start plus one turn is skipped, and phase 1 stands. `reask_s` is logged in A1 and every mid-run arm, and the cap check uses measured elapsed time including it. "Compliance-free hard bound" is used only for the **phase-2 end**; panel elapsed = max(T1, deadline) (INV-022). |
| INV-003 | MODIFY | **MODIFY = R3-V1.** Evidence: RR:48 launches with `--output-format json --no-session-persistence`, and RR:50 extracts the single `type=="result"` object, which exists only at process exit. A killed phase 2 therefore leaves nothing to salvage unless it streams. Feasibility: the same `select(.type=="result")` filter works on stream-json read with `jq -s`. Recomputed: luna B n = floor(28.8 / (2 x 7.2)) = 2.0, so n = 1 for any turn_p90 > 7.2 s. Fallback detected at 2 s: box = 150.8 - 118 = 32.8, n = floor(16.8/12.8) = 1, end 118 + 16 + 12.8 = 146.8 s <= 150.8 s. |
| INV-004 | ACCEPT | Probe text plus R3-V1's mechanical peer tag. The CONVERGENCE Jaccard uses only `origin:"own"` lines (phase-1 or pre-delivery, excluding P2-F and peer-tagged lines). Phase-2 independence is judged by ECHO on real-anchor slots. Ember's qualifying F1 anchors go to the two lunas disjointly, using the balanced deal in INV-023 below rather than a raw hash. V2's "alarm in at most 2 of 12 runs" guard applies to own lines only. In F1, own lines are sealed by process exit, so this alarm should fire at A1's rate; a higher rate is an integrity failure, not a design effect. |
| INV-005 | MODIFY | Strike "A5 vs A4 isolates challenge vs shared findings". A5 vs A4 compares two whole designs that differ in sender session, content source, move type and target issues. SEED:47 is answered **within F7**: <br>(1) For every card it posts, ember records the `category` and `severity` enum values it would give. This is a scoped R-06 exception for F7 cards; `claim` and all other free-text fields stay forbidden. <br>(2) Each card is rendered in one of two forms. **Challenge form:** anchor plus a required finite check. **Finding form:** anchor plus ember's category and severity. <br>(3) **Dealing, online in posting order.** Card i is the i-th card ember posts (i = 0, 1, ...), and ember posts at most 2k cards (INV-008). Card i goes to luna (i + r) mod 2. Its form is challenge when (i + floor(i/2) + c) is even and finding otherwise. r and c are seeded 0/1 coins per run, logged. Result: at k = 2 each luna gets exactly one card of each form, and at k = 1 the two lunas get opposite forms. <br>(4) Logged per slot: form, conversion (the receiver's line overlaps the card anchor by at least 12 characters), judge-credited conversion and uncredited conversion. <br>(5) Pre-registered secondary analysis: conversion by form, two-proportion test, with the run-paired difference also reported. At most 12 x 3 x 4 = 144 cards (about 72 per form); fewer where k = 1. <br>**Why not R3-V1's text:** "round-robin over a seeded order, and forms alternate in that order" deals A, B, A, B and forms C, F, C, F, so luna A gets C, C and luna B gets F, F. That contradicts V1's own "at most one of each form", and luna becomes confounded with form. A pre-sorted order also cannot exist, because cards arrive one at a time mid-run. |
| INV-006 | ACCEPT | R3-V1's criterion, unchanged. Each slot is a triple (content source, content form, delivery point), and two slots are distinct when they differ in at least 2 of the 3. F6's source is the findings blocks of peers that have finished: (Task, category) at exit, rendered as requests for Tasks with no peer finding, ranked by the lunas' declared not-checked scope. Telemetry is never used. **Applying the criterion requires one statement R3-V1 leaves implicit.** F3 still carries "V2-D4 Task x move cells" (R3-V1 slate). If its injections name a Task, F3 and F6 share the form "move + Task" and differ only in source, which is 1 of 3 and fails. So F3's injection names a move only, plus a Task only when the triggering tool call's path names one. After INV-007, telemetry cannot attribute most moves to a Task anyway. F2 differs from F7 in at most 1 (both are a reviewing peer sending anchor + move mid-run, V4:466), so it is no replacement. |
| INV-007 | ACCEPT | = R3-V1. Note that ember's F3 set is M1, M2, M7, M4 (V4:201). The probe lists signatures for M1 and M7 only, so M2 and M4 must each get a listed signature or be marked unobservable. |
| INV-008 | ACCEPT | = R3-V1 (k clamped at 0; F6 uses SL2's B and sonnet's turns; Spike 4 publishes B_A1, turn_p90, T_report_p90, PANEL_FINISH_AT and k per package before any arm). **Required statement of the k thresholds**, from the same formula with hooks = 2 and turn = 6.4: <br>k = 2 needs T_report_p90 <= 0.35 B - 2 - 5 x 6.4. That is 6.6 s at B = 116, 8.0 s at AL's 120 and 8.7 s at DE's 122. At DS's 100 the bound is 1.0 s, so k = 2 is impossible there. <br>k >= 1 needs T_report_p90 <= 0.35 B - 2 - 3 x 6.4. That is 19.4 s at 116 and 13.8 s at DS's 100. <br>For F6 (B = 273.7, turn 14): k = 2 needs <= 23.8 s and k >= 1 needs <= 51.8 s. <br>The package medians are from AG (historical, no H); A1 carries H and may be slower, which raises k. Gain and time rows are reported at k = 1 (central) and k = 2 (optimistic). A package with k = 0 counts as isolated for that design, and that dilution is reported. |

## MEDIUM invariants worth closing

- INV-009, -010, -011, -012, -014, -018: adopt R3-V1's six lines. On INV-018 I withdraw my own mid-arm decoy (R2-V2:38).
- INV-023: every disjoint split (F1 anchors, F4 locators, F7 cards) uses the online balanced deal of INV-005 (3). Recipient = (i + r) mod 2; no hash.
- INV-019: the decision table is stated against the observed A1 reach. A1 0/12 needs X >= 4/12 (p = 0.047); A1 1/12 needs 6/12 (p = 11,880/346,104 = 0.034, while 5/12 gives 10,428/134,596 = 0.077); A1 2/12 needs 7/12 (p = 58,432/1,307,504 = 0.045).
- INV-020: adopt V5's stage-2 screen (R2-V5:126-129): hard credits per run, a one-sided permutation test at p < 0.05, and a margin over A2-SL2 of at least 1/3 of runs.
- INV-021: F6's 0.26-1.06 is withdrawn as a carried figure and re-derived on SL2. F6 runs only if Spike 4 gives sonnet a T_report_p90 of at most 51.8 s (k >= 1).
- New counterfactual, needed by INV-001 and -008: log `finish_would_fire` in A1 and A2 (luna still running at PANEL_FINISH_AT). Spread inside a package (AL 98-171 s, AG) means slow runs get the signal in design arms but not in A1. The truncation rate must be compared, not assumed equal.

## Remaining disagreements

1. **INV-005 dealing rule.** This is a fact about R3-V1's text, not a preference. Dealing A, B, A, B against forms C, F, C, F yields C, C and F, F per luna. My (3) is the minimal fix, and every other clause is R3-V1's. If the panel prefers V1's wording, it must at least replace "forms alternate in that order" with an alternation per luna.
2. **What "expected" means for F3, F4 and F7.** R3-V1 labels every row "valid only at B = 116 and k = 2". By the INV-008 thresholds, k = 2 requires luna's output-heavy final turn at p90 to be no longer than the 6.6 s mean-turn neighbourhood, and it is impossible on designSpec. That package holds F7's B5/I1/I4 targets (INV-017). Calling k = 2 "planning" overstates every mid-run gain. I ask that k = 1 be the central row. Planned luna B is then 116 + 2 + 12.8 = 130.8 s (+12.8%).
3. **F3's form** (INV-006 row). Without the move-only rule, F3 and F6 fail V1's own criterion.

## Final concessions

- R2-V2:44 and :86 ("worst 150.0 s, +29.3%") and R2-V2:223 ("worst = expected" for F3) are planned-path figures. V5's finish-signal structure is right (INV-001).
- R2-V2:125 ("A5 vs A4 answers SEED:47") was false: sender, content, move type and targets all differ (INV-005).
- R2-V2:58-61 used the mean turn for n, and my adoption of V1's box missed that the fallback is always killed (INV-003).
- R2-V2:108 ("drawn only from V2-D4's uncovered cells") pointed F6 at telemetry. The findings-derived source is correct (INV-006, -007).
- R2-V2:38: adding a decoy partway through an arm pools two treatments (INV-018). Stop and report instead.
- R2-V2:148: applied to all lines, my independence guard would fail F1 by construction (INV-004).
- R2-V2:176 found the 97.1 s threshold but did not turn it into a count rule. INV-008 does.
- R2-V2:221's F1 C 0.23-0.94 is superseded by 0.06-0.63, with the gap-card route booked to the prompting share (INV-014).
- R3-V1 is right on the 1.20 B term and on stream-json. I had no counter to either.

## Final slate

| Slot | Family | Core | Grafts | Reason |
|---|---|---|---|---|
| 1 | F1 Between-phase cross-examination | V4-3 Axis-Flip Challenge | V2-D2 `contradiction` -> M7 (I6 route); gap-card decoy p = 1/3, kind withheld, booked to the prompting share; balanced disjoint anchor deal; INV-003 n per launch attempt with stream-json salvage; one phase-2 deadline T0 + 1.30 B_A1 incl. re-ask; V4 combiner; sealed-report judging on the post-re-ask `p1.md`; V5-D5 HL2 shadow variant | Only bound enforced by a kill: phase-2 end <= 150.8 s (+30.0%). Planned luna B 147.6 s (+27.2%), or n = 1 if turn_p90 > 7.2 s. C 0.06-0.63 /14 |
| 2 | F4 Searcher-to-reader fact relay | V4-2 Idle-Shift Sweeper | V2-D1 locators (balanced deal); V1-R2 harvest incl. sweeper output; V2-D5 witness kind; V5-D3 first-hand rule + 10% stop; k per INV-008; fail-closed snapshot; mechanical peer tag; sweeper timeout; hang guard 1.5 B_A1 | Only cheap I7/T1 path, in ember's idle time. Planned 130.8 s (k = 1) / 143.6 s (k = 2). Signal bound T0 + 1.35 B_f = 156.6 s; 174 s = breach |
| 3 | F3 Content-free coverage steering | V4-1 Move Radar | Observable signatures only (INV-007); move-only injections (INV-006); luna injections booked as static (A2 share); V1-R1 hash order; V5-D4 skip rule; V3 leak check; k per INV-008 | No model authors anything. A6 vs A2 = telemetry-timed vs static kit; C re-derived from ember rows, may be near 0. Same three-number time block as F4 |
| 4 | F6 Steering a running strong model | V4-5 Coverage Deflection on SL2 | Finished peers' (Task, category), requests for Tasks with no peer finding, ranked by declared not-checked scope; no counts, telemetry or SendMessage; surface filter; V1-R5 line; k with sonnet's turns | Claude receiver, harness author. Planned 303.7 s (+11.0%, k = 1) / 331.7 s (+21.2%, k = 2); bound 369.5 s; ceiling 410.6 s. Runs only if sonnet's T_report_p90 <= 51.8 s; gain re-derived (INV-021) |
| 5 | F7 Directed challenge | V4-4 Flag-and-Adjudicate, EL2, one way | Enum-tagged cards in challenge or finding form, dealt online and balanced (INV-005 (3)); ember cap 2k; hook snapshot; V5 C-3; `flag_finding_overlap` stops the arm | Only slot that answers SEED:47, within one arm. Planned 130.8 / 143.6 s; C 0.08-0.77 at k = 2, lower at k = 1, and designSpec rows depend on k >= 1 |

Proposed base document: V4

## Per-point positions

| Point | Winner | Reason |
|---|---|---|
| S-001 | V4 | (a)-(h) per design plus a detection/action runbook |
| S-002 | V4 | Kill switch, baked board path, timing and baseline tables |
| S-003 | V2 | The gate funnel makes the H/C split structural |
| S-004 | V5 | Net collaboration, static-kit row, tokens per added issue incl. resumed input tokens |
| S-005 | V4 | One ID scheme with a verification column |
| S-006 | V5 | Itemised unverified list tied to each number (now incl. T_report_p90) |
| C-001 | V1 | Searcher/reader complementarity predicts a gain the kit cannot copy |
| C-002 | V5 | T2a/T2b decides which routes reach B1/B2/I4 |
| C-003 | V1 | Truncate, validate, re-ask; grading constant |
| C-004 | V4 | Best-style column used by routing |
| C-005 | V4 | 12-200-character anchors plus V2's rules |
| C-006 | V4 | Process exit for phases; fail-closed snapshot for mid-run |
| C-007 | V4 | Relative, ground-truth-free alarm, on own lines (INV-004) |
| C-008 | V4 | Per-issue chains |
| C-009 | V5 | Three shares, C and H never summed |
| C-010 | V2 | Fresh A0, catalogue arm, A6 |
| C-011 | V2 | One reach endpoint, final-look Fisher, +4 over A2, conditional on A1 reach (INV-019) |
| C-012 | V1 | Every design on a seed baseline |
| C-013 | V1 | Panel finish signal, measured-reservation form plus R-24 audit |
| X-001 | V5 | Bottom-up H 0.03-0.34 |
| X-002 | V1 | 0 on /14; control correction only |
| X-003 | V1 | GT6 = I1 |
| X-004 | V5 | HL2 shadow schedule +0% |
| X-005 | V1 | The slowest luna sets B |
| X-006 | V4 | One block, P2-F ids, origin stripped |
| X-007 | V2 | No free text, hence enum-only finding form |
| X-008 | V1 | Grading and judge held constant |
| X-009 | V1 | Truncate, validate, re-ask |
| X-010 | V5 | The kit may win; A2 is the comparator |
| X-011 | V5 | Anchor routes to B1/B2/I4 need the gap card |
| X-012 | V1 | Both scales and the label mapping defined most precisely |
| X-013 | V2 | 4/6 vs 0/6 = 15/495 = 0.030 |
| A-001 | V1 | REQ-S3 tests the act, also on "finish now" |
| A-002 | V5 | Prices the kit's time |
| A-003 | V2 | Random labels plus sealed-report judging |
| A-004 | V4 | States the H-C interaction |
| A-005 | V5 | Per-package values, not /3; AG confirms package spread |
| A-006 | V2 | Decoys via the gap card |
| A-007 | V4 | Spike, fallback, `resume_fallback` metric |
| A-008 | V4 | Helpers write only under `$BOARD` |
| A-009 | V2 | Confirmation on two new packages |
| A-010 | V1 | States why EL2 is the base |
| A-011 | V5 | c capped against measured reach |
