# Round 3 final arguments: V1 (opus, architect lens)

Citations: `V<n>:<line>` = `variant-<n>-original.md`; `R2-V<n>:<line>` = `round2-V<n>.md`; `INV-0nn` = `../invariant-probe.md`; `RR:48` = `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/tools/run-reviewer.sh:48`. No Round 3 statement existed when I wrote this one. Every number below was recomputed.

## Final position

V4 stays the base. The five-family slate also stands: F1, F4, F3, F6, F7. The probe is right on all eight HIGH items, and three of my Round 2 claims fail under it:

- "worst 150.0 s" was a planned-path figure;
- "A5 vs A4 isolates challenge vs findings" was false;
- F1's n used the mean turn.

I accept five resolutions as written. I modify three where the probe's own text cannot work:

- **INV-001.** Its `PANEL_FINISH_AT` keeps a 1.20 B term. At the k = 2 that INV-008 computes, that term makes the signal fire on the planned path.
- **INV-003.** Partial salvage is impossible under today's `--output-format json`.
- **INV-005.** The finding form as written breaks the agreed no-free-text rule (X-007).

F6 stays. It is distinct from F3 under a stated criterion, and under that criterion the replacement F2 would fail against F7. Only F1's bound is enforced by a process kill. Slots 2-5 stay within 1.35 B at p90 by construction, and the SLO budget audits them.

## HIGH invariant resolutions

| INV | Verdict | Exact rule for the merged spec |
|---|---|---|
| INV-001 | MODIFY | For each mid-run design (F3, F4, F6, F7) the spec states three numbers: (1) the planned end, B_f + hooks + 2k x turn; (2) the finish-signal bound, PANEL_FINISH_AT + turn_p90 + T_report_p90 = T0 + 1.35 B_f; (3) the enforced ceiling, a hang guard at T0 + 1.5 B_A1 whose firing counts as `SLO_BREACH`. **`PANEL_FINISH_AT = T0 + 1.35 B_f - turn_p90 - T_report_p90`.** The 1.20 B term is dropped. Spike 4 measures turn_p90 and T_report_p90 (the duration of the last turn) per model: luna for EL2, sonnet for SL2. The k of INV-008 guarantees planned end <= PANEL_FINISH_AT, so the signal never fires on the planned path. REQ-S3 measures the act rate on "finish now". The spec says plainly that for slots 2-5 the +35% cap is audited by the SLO budget (R-24), not enforced. "Worst 150.0 s" and "worst 330 s" are struck as cap guarantees. **Why modify:** with the probe's min(1.20 B, ...), INV-008's k = 2 at B = 116 gives a planned end of 116 + 2 + 25.6 = 143.6 s, past 1.20 x 116 = 139.2 s. The probe's two required rules contradict each other at its own planning values. Planning values for the new rule: PANEL_FINISH_AT = 156.6 - 12.8 = 143.8 s; bound 156.6 s (+35.0%); hang guard 174 s (+50%); for SL2, 1.5 x 273.7 = 410.6 s. |
| INV-002 | ACCEPT | One wall-clock deadline, T0 + 1.30 B_A1, covers every process that can write phase-2 lines: the resume or fresh fallback, the challenges and any H2 re-ask. A re-ask that cannot start with one start plus one turn left before the deadline is skipped; invalid phase-2 lines are dropped and phase 1 stands. In A1 and in every mid-run arm the H2 re-ask is logged as `reask_s`, and the cap check uses measured elapsed time that includes it. The words "compliance-free hard bound" appear only with this rule, worded as a **phase-2** bound (panel elapsed = max(T1, deadline), INV-022). |
| INV-003 | MODIFY | Before each launch attempt the harness computes `box = min(35, T0 + 1.30 B_f - t_launch)` and `n = max(0, min(cap, floor((box - start_cost) / (2 x turn_p90))))`. start_cost is 6 s for a resume and 16 s for the fresh fallback. A failed resume therefore re-renders the digest with a new n. If n = 0, no launch happens and phase 1 stands. Phase-2 and re-ask sessions run with `--output-format stream-json --verbose`, written to file as they stream. The brief asks for one complete findings line after each challenge. On timeout the combiner keeps every complete, parser-valid P2 line already streamed and drops the rest (`phase2_timeout`, `p2_lines_salvaged`). Spike S2 checks on luna that text streams before exit. The spec states two consequences: at planning B, luna B gets n = 1 whenever turn_p90 > 7.2 s (28.8/14.4 = 2.0); and the fallback for luna B gets n = floor((34.8 - 2 - 16)/12.8) = 1, not 0, if the resume failure is detected within 2 s. **Why modify:** today's command uses `--output-format json` (RR:48), which writes one result object at exit, so a killed process leaves no line to salvage. The probe also left "margin" undefined; per-line salvage makes margin = 0 safe. |
| INV-004 | ACCEPT | The CONVERGENCE Jaccard is computed on `origin:"own"` lines only: phase-1 or pre-delivery findings, excluding P2-F and peer-tagged lines. In mid-run arms the peer tag is applied mechanically, as in the INV-012 line below. Phase-2 independence is judged by ECHO on real-anchor slots. Ember's qualifying F1 anchors are hash-split disjointly between the two lunas. V2's "alarm in at most 2 of 12 runs" guard applies to this own-line Jaccard. |
| INV-005 | MODIFY | Strike the claim that A5 vs A4 isolates "challenge vs shared findings". A5 vs A4 compares two whole designs that differ in sender session, content source, move type and target issues. SEED:47 is answered **within F7**: <br>(1) For every card it posts, ember also records the `category` and `severity` enum values it would give. This is a scoped R-06 exception for F7 cards; `claim` and every other free-text field stay forbidden. <br>(2) The harness renders each card in one of two forms. **Challenge form:** anchor plus a required finite check. **Finding form:** anchor plus ember's category and severity. <br>(3) Card-to-luna assignment is round-robin over a seeded order, and forms alternate in that order. Each luna gets at most 2 cards and at most one of each form, so each luna serves as its own control (this also closes INV-023 for F7). <br>(4) Logged per slot: form, conversion (the receiver's line overlaps the card anchor by at least 12 characters), judge-credited conversion and uncredited conversion. <br>(5) The secondary analysis is pre-registered: conversion by form, two-proportion test. At 12 runs x 3 packages x 4 cards there are at most 144 cards, about 72 per form. <br>**Why modify:** "anchor plus ember's own claim" puts free text in a message, which X-007 (agreed 5/5) and R-06 (V4:702) forbid. It would also make ECHO the dominant failure mode in half the cards. |
| INV-006 | ACCEPT | **Distinctness criterion, stated once:** each slot is a triple (content source, content form, delivery point). Two slots are distinct when they differ in at least 2 of the 3. Sources are harness-from-telemetry, harness-from-finished-findings, dedicated helper session, and reviewing peer. <br>F1 = (finished findings, peer anchor + move, between phases). <br>F3 = (telemetry, move name only, mid-run). <br>F4 = (helper session, repo facts, mid-run). <br>F6 = (finished findings, uncovered-Task requests, mid-run). <br>F7 = (reviewing peer, flagged sentence + finite check, mid-run). <br>Every pair differs in at least 2: F1/F6 in form and delivery; F3/F6 in source and form; F4/F7 in source and form. The evicted F5 (helper session, facts, mid-run) differs from F4 in 0, and F2 (reviewing peer, anchor/ref + move, mid-run) differs from F7 in 1. So F2 is not a valid replacement. **F6 is kept**, with its coverage source restored to V4-5's watcher (V4:543): (Task, category) from the findings blocks of peers that have finished, rendered as requests for uncovered Tasks, never from telemetry. I6 keeps its route through F1's `contradiction` -> M7 row (R2-V2:13). |
| INV-007 | ACCEPT | The classifier section lists the observable tool-call signature of each catalogue move. M3, M5, M6, M8, M9 and M10 have none, are marked unobservable, and are never described as "not done by any panel member". Luna's F3 injections are labelled a timed static prompt and booked to the prompting share (A2 comparator). F3's collaboration content is restated as ember's search-move gaps plus the "source.md never opened" check, and F3's C is re-derived from ember rows only. F6 draws reading-move requests only from findings-derived coverage (INV-006). |
| INV-008 | ACCEPT | F3, F4 and F7 get a per-package count of facts, cards or injections per luna: `k = max(0, min(2, floor((0.35 B_A1(pkg) - hooks - turn_p90 - T_report_p90) / (2 x turn_p90))))`, with hooks = 2 s. F6 uses the same rule with SL2's B and sonnet's turns. With the INV-001 rule this equals floor((PANEL_FINISH_AT - T0 - B - hooks)/(2 x turn_p90)), so planned end <= PANEL_FINISH_AT holds by construction. Worked values: B = 116 with 6.4/6.4 gives k = floor(25.8/12.8) = 2 (end 143.6 s <= 143.8 s); with T_report_p90 = 11.0, k = floor(21.2/12.8) = 1 (end 130.8 s); B = 90 gives k = floor(16.7/12.8) = 1. Spike 4 publishes per-package B_A1, turn_p90, T_report_p90, PANEL_FINISH_AT and k before any arm runs. Every "+x%" and every gain row is labelled valid only at B = 116 and k = 2. |

## MEDIUM invariants worth closing

- **INV-009:** R-05's allowed differences become R-01, R-03 and the removal of `--no-session-persistence` (RR:48), because every arm, A1 included, re-asks through `--resume`.
- **INV-010:** the phase-1 H2 re-ask finishes before the seal. `<rid>.p1.md` is the post-re-ask phase-1 report; it is hashed at that point and used for sealed-report judging.
- **INV-011:** cleanup deletes only the session ids recorded in that run's `collab.json`, after every concurrent run on that sandbox ends, and never the directory. `git status` is checked after the last such run.
- **INV-012:** in mid-run arms the harness tags a line `peer` if its anchor overlaps a delivered anchor by at least 12 characters, or if a delivered locator is in its refs, whatever the model wrote. Alarms built on "own sealed findings" are dropped, and the timestamp test is kept as an integrity log only.
- **INV-014:** findings from gap-card slots are booked to the prompting share. F1 C = 0.06-0.63 /14, and the gap route (0-0.10) is reported in that share's column.
- **INV-018:** a `flag_finding_overlap` alarm stops and reports the arm; it never changes the treatment partway through an arm.

## Remaining disagreements

1. **INV-001, the 1.20 B term.** V5's formula (R2-V5:77) and the probe keep min(1.20 B, ...). I would drop it. That term was my own unmeasured margin (V1:138). With it, either k = 1 at planning B, which halves F3/F4/F7's delivered content, or the signal truncates luna's own isolated work on the planned path (INV-008's "typical path" failure). The measured term already lands the p90 run at exactly 1.35 B, and R-24 absorbs the tail (1 package in 12). I can converge on the probe text only if INV-008's k is computed against the same PANEL_FINISH_AT, which gives k = 1 at planning B.
2. **INV-003, output format.** Without stream-json the salvage clause is unimplementable (RR:48). This is a fact, not a preference.
3. **INV-005, the finding form.** "Ember's own claim" conflicts with X-007. Enum-only verdicts keep the contrast without free text. If the panel rejects the R-06 exception, the fallback is the probe's alternative: SEED:47 is answered descriptively only.

## Final concessions

- R2-V1:43 ("same sender, same receivers") was false. The F4 sender is a fresh sweeper session posting search facts; the F7 sender is the reviewing ember flagging sentences (INV-005).
- R2-V1:75's "worst 150.0 s" and R2-V1:170's "worst = expected" for F3 are planned-path figures. V5's finish-signal bound (R2-V5:64-73) is the right structure.
- R2-V1:61's "hard bound 150.8 s for any T1" holds only for the phase-2 end, and only once the re-ask sits inside the deadline (INV-002, INV-022).
- R2-V1:52's n used the mean turn and silently zeroed the fallback (INV-003).
- R2-V1:102's "uncovered cells from V2-D4" pointed F6 at telemetry. The findings-derived source is correct (INV-006, INV-007).
- The F1 gap-card route is harness extraction by V4:523's own test; F1 C drops to 0.06-0.63 (INV-014).
- F3 after INV-007: lunas leave almost no search signatures, so ember's "no panel member has done this" mostly reflects ember's own history. F3's collaboration share may be near 0, and its A6 vs A2 result should be read as "telemetry-timed kit vs static kit".

## Final slate

| Slot | Family | Core | Grafts | Reason |
|---|---|---|---|---|
| 1 | F1 Between-phase cross-examination | V4-3 Axis-Flip Challenge | V2-D2 `contradiction` -> M7 (I6 route); gap-card decoy p = 1/3, kind withheld, findings booked to the prompting share; ember anchors hash-split between lunas; INV-003 n per launch attempt with stream-json salvage; one phase-2 deadline T0 + 1.30 B_A1 incl. re-ask; V4 combiner; V2 sealed-report judging on the post-re-ask `p1.md`; V5-D5 HL2 shadow variant | Only bound enforced by a kill (phase-2 end <= 150.8 s, +30.0%); planned luna B 147.6 s (+27.2%); C 0.06-0.63 |
| 2 | F4 Searcher-to-reader fact relay | V4-2 Idle-Shift Sweeper | V2-D1 disjoint locators (round-robin); V1-R2 harvest incl. sweeper output; V2-D5 witness kind; V5-D3 first-hand rule + 10% stop; k per INV-008; fail-closed hook snapshot; mechanical peer tag; sweeper timeout; hang guard 1.5 B_A1 | Only cheap I7/T1 path, in ember's idle time; planned 143.6 s at k = 2, bound 1.35 B at p90, ceiling 174 s = breach |
| 3 | F3 Content-free coverage steering | V4-1 Move Radar | V2-D4 Task x move cells limited to observable signatures; luna injections labelled static (A2 share); V1-R1 hash order; V5-D4 skip rule; V3 leak check; k per INV-008 | No model authors anything; tests whether telemetry timing beats the static kit; same three-number time block |
| 4 | F6 Steering a running strong model | V4-5 Coverage Deflection on SL2 | Coverage from finished peers' findings (Task, category), rendered as uncovered-Task requests; no counts, no telemetry, no SendMessage; surface filter; V1-R5 brief line; k with sonnet's turns | Claude receiver, harness author; planned 331.7 s at k = 2 (273.7 + 2 + 56; +21.2%); bound 369.5 s at p90; ceiling 410.6 s |
| 5 | F7 Directed challenge | V4-4 Flag-and-Adjudicate, EL2, one way | Enum-tagged cards rendered in challenge or finding form, alternating; round-robin split, at most 2 per luna; hook snapshot; V5 C-3; k per INV-008; `flag_finding_overlap` stops the arm | Only slot that answers SEED:47, within one arm; planned 143.6 s at k = 2; C 0.08-0.77 |

Proposed base document: V4

## Per-point positions

| Point | Winner | Reason |
|---|---|---|
| S-001 | V4 | (a)-(h) per design plus a detection/action runbook |
| S-002 | V4 | Kill switch, baked board path, timing and baseline tables |
| S-003 | V2 | The gate funnel makes the H/C split structural |
| S-004 | V5 | Net collaboration, static-kit row, tokens per added issue (plus input tokens for resume) |
| S-005 | V4 | One ID scheme with a verification column |
| S-006 | V5 | Itemised unverified list tied to each number |
| C-001 | V1 | Searcher/reader complementarity predicts a gain the kit cannot copy |
| C-002 | V5 | T2a/T2b decides which routes reach B1/B2/I4 |
| C-003 | V1 | Truncate, validate, re-ask; grading constant |
| C-004 | V4 | Best-style column used by routing |
| C-005 | V4 | 12-200-character anchors plus V2's rules |
| C-006 | V4 | Process exit for phases; fail-closed snapshot for mid-run |
| C-007 | V4 | Relative, ground-truth-free alarm, now on own lines (INV-004) |
| C-008 | V4 | Per-issue chains |
| C-009 | V5 | Three shares, C and H never summed |
| C-010 | V2 | Fresh A0, catalogue arm, A6 |
| C-011 | V2 | One reach endpoint, final-look Fisher, +4 over A2 |
| C-012 | V1 | Every design on a seed baseline |
| C-013 | V1 | Panel finish signal, now measured-reservation form plus R-24 audit |
| X-001 | V5 | Bottom-up H 0.03-0.34 |
| X-002 | V1 | 0 on /14; control correction only |
| X-003 | V1 | GT6 = I1 |
| X-004 | V5 | HL2 shadow schedule +0% |
| X-005 | V1 | The slowest luna sets B |
| X-006 | V4 | One block, P2-F ids, origin stripped |
| X-007 | V2 | No free text, which is why INV-005 uses enums |
| X-008 | V1 | Grading and judge held constant |
| X-009 | V1 | Truncate, validate, re-ask |
| X-010 | V5 | The kit may win; A2 is the comparator |
| X-011 | V5 | Anchor routes to B1/B2/I4 need the gap card |
| X-012 | V1 | Both scales and the label mapping defined most precisely |
| X-013 | V2 | 4/6 vs 0/6 = 0.030 |
| A-001 | V1 | REQ-S3 tests the act, now also on "finish now" |
| A-002 | V5 | Prices the kit's time |
| A-003 | V2 | Random labels plus sealed-report judging |
| A-004 | V4 | States the H-C interaction |
| A-005 | V5 | Per-package values, not /3 |
| A-006 | V2 | Decoys via the gap card |
| A-007 | V4 | Spike, fallback, `resume_fallback` metric |
| A-008 | V4 | Helpers write only under `$BOARD` |
| A-009 | V2 | Confirmation on two new packages |
| A-010 | V1 | States why EL2 is the base |
| A-011 | V5 | c capped against measured reach |
